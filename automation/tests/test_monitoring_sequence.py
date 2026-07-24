import shutil

from datetime import date, datetime

from automation.core.automation_runner import AutomationRunner
from automation.models.draw import Draw
from automation.models.source_result import SourceResult
from automation.models.source_status import SourceStatus


OLD_DRAW = Draw(
    draw_date=date(2026, 7, 16),
    main_numbers=[5, 13, 24, 33, 40],
    life_ball=10,
)

NEW_DRAW = Draw(
    draw_date=date(2026, 7, 20),
    main_numbers=[1, 2, 3, 4, 5],
    life_ball=1,
)


def success_result(source_name, draw):
    return SourceResult(
        source_name=source_name,
        url="",
        status=SourceStatus.SUCCESS,
        draw=draw,
        retrieved_at=datetime.now(),
    )


class FakeOfficialSource:

    def __init__(self):
        self.calls = 0

    def fetch(self):
        self.calls += 1

        if self.calls == 1:
            return success_result(
                "National Lottery",
                OLD_DRAW,
            )

        return success_result(
            "National Lottery",
            NEW_DRAW,
        )


class FakeNationalLotteryComSource:

    def __init__(self):
        self.calls = 0

    def fetch(self):
        self.calls += 1

        if self.calls <= 2:
            return success_result(
                "NationalLottery.com",
                OLD_DRAW,
            )

        return success_result(
            "NationalLottery.com",
            NEW_DRAW,
        )


class FakeLotteryStatsSource:

    def fetch(self):
        return SourceResult(
            source_name="LotteryStats",
            url="",
            status=SourceStatus.NETWORK_ERROR,
            error_message="Simulated failure",
        )


class FakeScheduleGuard:

    def is_active_monitoring_time(self):
        return True

    def monitoring_window_closed(self):
        return True


class FakeNotifier:

    def send(self, subject, body):
        print()
        print("FAKE EMAIL")
        print(f"Subject: {subject}")
        print(f"Body: {body}")


def test_monitoring_sequence(tmp_path):

    database_path = (
        tmp_path / "test_database.csv"
    )

    shutil.copy(
        "automation/tests/data/test_database.csv",
        database_path,
    )

    state_path = (
        tmp_path / "monitoring_state.json"
    )

    runner = AutomationRunner(
        database_path=database_path,
        sources=[
            FakeOfficialSource(),
            FakeNationalLotteryComSource(),
            FakeLotteryStatsSource(),
        ],
        monitoring_state_path=state_path,
    )

    # Accelerate all waits for testing.
    runner.NO_DRAW_POLL_SECONDS = 0
    runner.ONE_SOURCE_POLL_SECONDS = 0
    runner.THIRD_SOURCE_POLL_SECONDS = 0

    runner.schedule_guard = FakeScheduleGuard()
    runner.notifier = FakeNotifier()

    result = runner.run()

    assert result is not None

    assert (
        result.action.name
        == "DATABASE_UPDATE_REQUIRED"
    )

    assert result.validated_draw is not None

    assert (
        result.validated_draw.draw_date
        == date(2026, 7, 20)
    )