"""
Predict For Life - Automation Runner

Coordinates a complete validation cycle by querying all
configured draw sources and passing the results through
the validation pipeline.
"""

from __future__ import annotations

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

    def __init__(
        self,
        database_path: str = "set_for_life.csv",
        sources=None,
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

        self.monitoring_state = MonitoringState()

        self.notifier = EmailNotifier()

        self.schedule_guard = ScheduleGuard()

    def run(self):
        """
        Execute one complete automation cycle.
        """

        if self.monitoring_state.is_follow_up_active():

            self._run_follow_up()

            return None

        database_draw = self.database_repository.latest_draw()

        source_results = [
            source.fetch()
            for source in self.sources
        ]

        validation_result = self.validation_engine.validate(
            database_draw,
            source_results,
        )

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

            pending_source = validation_result.failed_results[0].source_name

            self.monitoring_state.begin_follow_up(
                pending_source,
            )

        return database_validation
    
    def _run_follow_up(
        self,
    ) -> None:
        """
        Execute one follow-up monitoring cycle.
        """

        state = self.monitoring_state.load()

        pending_source = state["pending_source"]

        database_draw = self.database_repository.latest_draw()

        source = next(
            result
            for result in [
                source.fetch()
                for source in self.sources
            ]
            if result.source_name == pending_source
        )

        if not source.success:

            if self.schedule_guard.monitoring_window_closed():

                self.notifier.send(
                    subject="[Predict For Life] Third Source Not Published",
                    body=(
                        f"{pending_source} did not publish the "
                        "validated draw before the monitoring "
                        "window closed."
                    ),
                )

                self.monitoring_state.end_follow_up()

                return

            return

        if source.draw == database_draw:

            self.notifier.send(
                subject="[Predict For Life] Third Source Confirmed",
                body=(
                    "The delayed source has now published "
                    "the validated draw.\n\n"
                    "All three validation sources are now in agreement."
                ),
            )

            self.monitoring_state.end_follow_up()

            return

        self.notifier.send(
            subject="[Predict For Life] WARNING - Third Source Disagreement",
            body=(
                f"{pending_source} has published a draw that "
                "does not match the validated result.\n\n"
                "The database has not been changed.\n"
                "Please investigate."
            ),
        )

        self.monitoring_state.end_follow_up()

        return