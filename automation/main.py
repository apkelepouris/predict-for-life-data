"""
Predict For Life - Automation Entry Point

Runs one complete automation cycle.
"""

from __future__ import annotations

import sys

from time import perf_counter

from automation.core.automation_runner import (
    AutomationRunner,
)

from automation.core.schedule_guard import (
    ScheduleGuard,
)

from automation.core.report_writer import (
    ReportWriter,
)

from automation.core.email_notifier import (
    EmailNotifier,
)

from automation.core.monitoring_state import (
    MonitoringState,
)


def main() -> None:
    """
    Execute one automation cycle.
    """

    database_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "set_for_life.csv"
    )

    guard = ScheduleGuard()

    if not guard.should_run():

        if guard.is_draw_day():

            print(
                "Outside active monitoring window."
            )

            print(
                "Running draw-day recovery check."
            )

        else:

            print(
                "Outside monitoring window."
            )

            return

    start_time = perf_counter()

    try:

        runner = AutomationRunner(
            database_path=database_path,
        )

        result = runner.run()

        if result is None:
            return

        duration = perf_counter() - start_time

        monitoring_state = MonitoringState()

        if hasattr(result, "validated_draw"):

            if result.validated_draw is not None:

                monitoring_state.reset_for_new_draw(
                    result.validated_draw.draw_date,
                )

        if result.awaiting_final_source:

            state = monitoring_state.load()

            state["awaiting_final_source"] = True

            monitoring_state.save(state)

    except Exception as error:

        duration = perf_counter() - start_time

        notifier = EmailNotifier()

        notifier.send(
            subject="[Predict For Life] CRITICAL - Automation Failed",
            body=(
                "The Predict For Life automation "
                "encountered an unexpected error.\n\n"
                f"Error:\n{error}\n\n"
                f"Duration: {duration:.2f} seconds"
            ),
        )

        raise

    notifier = EmailNotifier()

    if result.action.name != "NO_NEW_DRAW":

        writer = ReportWriter()

        writer.write(
            timestamp=guard._current_london_datetime().strftime(
                "%d/%m/%Y %H:%M:%S %Z"
            ),
            trigger="Automation",
            result=result.action.name,
            message=result.message,
            duration_seconds=duration,
        )

    if result.action.name == "DATABASE_UPDATE_REQUIRED":

        state = monitoring_state.load()

        if not state["database_update_email_sent"]:

            notifier = EmailNotifier()

            notifier.send(
                subject="[Predict For Life] Database Updated",
                body=(
                    "Database updated successfully.\n\n"
                    "App users can now download the latest results."
                ),
            )

            state["database_update_email_sent"] = True

            monitoring_state.save(state)

    if result.action.name == "DATABASE_CONFLICT":

        notifier = EmailNotifier()

        notifier.send(
            subject="[Predict For Life] CRITICAL - Database Conflict",
            body=(
                "The validated draw conflicts with the "
                "current database.\n\n"
                "No automatic update has been performed.\n\n"
                "Manual investigation is required."
            ),
        )

    if result.action.name == "DATABASE_NEWER_THAN_VALIDATED":

        notifier = EmailNotifier()

        notifier.send(
            subject="[Predict For Life] WARNING - Database Newer Than Validated Draw",
            body=(
                "The local database contains a newer draw "
                "than the validated sources.\n\n"
                "No automatic update has been performed.\n\n"
                "Please investigate."
            ),
        )

    if result.action.name == "VALIDATION_FAILED":

        notifier = EmailNotifier()

        notifier.send(
            subject="[Predict For Life] CRITICAL - Validation Failed",
            body=(
                "The automation could not validate the "
                "latest draw.\n\n"
                "No database update has been performed.\n\n"
                "Manual investigation is required."
            ),
        )

    print()
    print("Automation completed")
    print("--------------------")
    print(f"Result : {result.action.name}")
    print(f"Message: {result.message}")

    if hasattr(result, "validated_draw"):

        if result.validated_draw is not None:

            print()
            print("Validated draw:")
            print(result.validated_draw)


if __name__ == "__main__":
    main()