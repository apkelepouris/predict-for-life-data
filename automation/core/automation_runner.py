"""
Predict For Life - Automation Runner

Coordinates a complete validation cycle by querying all
configured draw sources and passing the results through
the validation pipeline.
"""

from __future__ import annotations

from time import sleep

from automation.core.database_validator import DatabaseValidator
from automation.core.validation_engine import ValidationEngine
from automation.models.validation_action import ValidationAction
from automation.sources.lottery_stats import LotteryStatsSource
from automation.sources.national_lottery import (
    OfficialNationalLotterySource,
)
from automation.sources.national_lottery_com import (
    NationalLotteryComSource,
)
from automation.database.database_repository import (
    DatabaseRepository,
)
from automation.database.database_writer import (
    DatabaseWriter,
)
from automation.models.database_action import (
    DatabaseAction,
)
from automation.core.monitoring_state import (
    MonitoringState,
)
from automation.core.email_notifier import (
    EmailNotifier,
)
from automation.core.schedule_guard import (
    ScheduleGuard,
)


class AutomationRunner:
    """
    Coordinates one complete automation run.
    """

    NO_DRAW_POLL_SECONDS = 10 * 60
    ONE_SOURCE_POLL_SECONDS = 5 * 60
    THIRD_SOURCE_POLL_SECONDS = 15 * 60

    def __init__(
        self,
        database_path: str = "set_for_life.csv",
        sources=None,
        monitoring_state_path=None,
    ) -> None:
        
        if sources is None:

            self.sources = [
                OfficialNationalLotterySource(),
                NationalLotteryComSource(),
                LotteryStatsSource(),
            ]

        else:

            self.sources = sources

        self.validation_engine = ValidationEngine()

        self.database_validator = DatabaseValidator()

        self.database_repository = DatabaseRepository(
            database_path,
        )

        self.database_writer = DatabaseWriter(
            database_path,
        )

        self.monitoring_state = MonitoringState(
            monitoring_state_path
        )

        self.notifier = EmailNotifier()

        self.schedule_guard = ScheduleGuard()

    def run(self):
        """
        Execute one complete automation cycle.
        """

        if self.monitoring_state.is_follow_up_active():

            self._run_follow_up()

            return None

        while True:

            database_draw, validation_result = (
                self._run_validation_cycle()
            )

            if not self.schedule_guard.is_active_monitoring_time():

                break

            if (
                validation_result.action
                == ValidationAction.NO_NEW_DRAW
            ):

                print(
                    "No newer draw yet. "
                    "Checking again in 10 minutes."
                )

                sleep(
                    self.NO_DRAW_POLL_SECONDS
                )

                continue

            if (
                validation_result.action
                == ValidationAction.CONTINUE_MONITORING
            ):

                print(
                    "One source has published the new draw. "
                    "Checking again in 5 minutes."
                )

                sleep(
                    self.ONE_SOURCE_POLL_SECONDS
                )

                continue

            break

        if validation_result.action != ValidationAction.UPDATE_DATABASE:

            if (
                validation_result.action
                == ValidationAction.CONTINUE_MONITORING
                and self.schedule_guard.monitoring_window_closed()
                and not self.monitoring_state.validation_timeout_sent()
            ):

                self.notifier.send(
                    subject="[Predict For Life] Validation Timed Out",
                    body=(
                        "Only one source published a newer draw "
                        "before the monitoring window closed.\n\n"
                        "The database was not updated."
                    ),
                )

                self.monitoring_state.mark_validation_timeout_sent()

            return validation_result
        
        database_validation = self.database_validator.validate(
            database_draw,
            validation_result.validated_draw,
        )

        if (
            database_validation.action
            == DatabaseAction.DATABASE_UPDATE_REQUIRED
        ):

            self.database_writer.append_draw(
                validation_result.validated_draw,
            )

        if validation_result.awaiting_final_source:

            pending_source = (
                validation_result
                .failed_results[0]
                .source_name
            )

            self.monitoring_state.begin_follow_up(
                pending_source,
            )

            self._run_follow_up()

        return database_validation

    def _run_validation_cycle(
        self,
    ):
        """
        Execute one source validation cycle.
        """

        database_draw = (
            self.database_repository.latest_draw()
        )

        source_results = [
            source.fetch()
            for source in self.sources
        ]

        validation_result = (
            self.validation_engine.validate(
                database_draw,
                source_results,
            )
        )

        return database_draw, validation_result

    def _run_follow_up(
        self,
    ) -> None:
        """
        Monitor the delayed third source
        every 15 minutes until it publishes
        or the monitoring window closes.
        """

        state = self.monitoring_state.load()

        pending_source = state["pending_source"]

        while True:

            database_draw = (
                self.database_repository.latest_draw()
            )

            source = next(
                result
                for result in [
                    source.fetch()
                    for source in self.sources
                ]
                if result.source_name
                == pending_source
            )

            if source.success:

                if source.draw == database_draw:

                    self.notifier.send(
                        subject=(
                            "[Predict For Life] "
                            "Third Source Confirmed"
                        ),
                        body=(
                            "The delayed source has now "
                            "published the validated draw.\n\n"
                            "All three validation sources "
                            "are now in agreement."
                        ),
                    )

                else:

                    self.notifier.send(
                        subject=(
                            "[Predict For Life] WARNING - "
                            "Third Source Disagreement"
                        ),
                        body=(
                            f"{pending_source} has published "
                            "a draw that does not match the "
                            "validated result.\n\n"
                            "The database has not been changed.\n"
                            "Please investigate."
                        ),
                    )

                self.monitoring_state.end_follow_up()

                return

            if self.schedule_guard.monitoring_window_closed():

                self.notifier.send(
                    subject=(
                        "[Predict For Life] "
                        "Third Source Not Published"
                    ),
                    body=(
                        f"{pending_source} did not publish the "
                        "validated draw before the monitoring "
                        "window closed."
                    ),
                )

                self.monitoring_state.end_follow_up()

                return

            print(
                f"{pending_source} has not published yet. "
                "Checking again in 15 minutes."
            )

            sleep(
                self.THIRD_SOURCE_POLL_SECONDS
            )