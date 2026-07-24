from unittest.mock import MagicMock, patch

from automation import main


def test_draw_day_outside_window_runs_recovery():

    fake_guard = MagicMock()
    fake_guard.should_run.return_value = False
    fake_guard.is_draw_day.return_value = True

    fake_runner = MagicMock()

    fake_result = MagicMock()
    fake_result.action.name = "NO_NEW_DRAW"
    fake_result.message = "No new draw."

    fake_runner.run.return_value = fake_result

    with patch.object(
        main,
        "ScheduleGuard",
        return_value=fake_guard,
    ), patch.object(
        main,
        "AutomationRunner",
        return_value=fake_runner,
    ), patch.object(
        main,
        "EmailNotifier",
    ), patch.object(
        main,
        "ReportWriter",
    ), patch.object(
        main,
        "MonitoringState",
    ):

        main.main()

    fake_runner.run.assert_called_once()


def test_non_draw_day_outside_window_exits():

    fake_guard = MagicMock()
    fake_guard.should_run.return_value = False
    fake_guard.is_draw_day.return_value = False

    with patch.object(
        main,
        "ScheduleGuard",
        return_value=fake_guard,
    ), patch.object(
        main,
        "AutomationRunner",
    ) as fake_runner_class:

        main.main()

    fake_runner_class.assert_not_called()