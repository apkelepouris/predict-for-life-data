import shutil

from automation.models.draw import Draw
from automation.models.source_result import SourceResult
from automation.models.source_status import SourceStatus

from datetime import date, datetime

from automation.core.automation_runner import AutomationRunner


class FakeOfficialSource:

    def fetch(self):

        return SourceResult(
            source_name="National Lottery",
            url="",
            status=SourceStatus.SUCCESS,
            draw=Draw(
                draw_date=date(2026, 7, 20),
                main_numbers=[1, 2, 3, 4, 5],
                life_ball=1,
            ),
            retrieved_at=datetime.now(),
        )
    
class FakeNationalLotteryComSource:

    def fetch(self):

        return SourceResult(
            source_name="NationalLottery.com",
            url="",
            status=SourceStatus.SUCCESS,
            draw=Draw(
                draw_date=date(2026, 7, 20),
                main_numbers=[1, 2, 3, 4, 5],
                life_ball=1,
            ),
            retrieved_at=datetime.now(),
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
        return False

    def monitoring_window_closed(self):
        return True

class FakeNotifier:

    def send(self, subject, body):
        print()
        print("FAKE EMAIL")
        print(f"Subject: {subject}")
        print(f"Body: {body}")

def test_happy_path(tmp_path):

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