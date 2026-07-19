from datetime import date, datetime

from automation.core.automation_runner import AutomationRunner
from automation.models.draw import Draw
from automation.models.source_result import SourceResult
from automation.models.source_status import SourceStatus


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
            source_name="National-Lottery.com",
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
            error_message="Simulated timeout",
        )


runner = AutomationRunner(
    sources=[
        FakeOfficialSource(),
        FakeNationalLotteryComSource(),
        FakeLotteryStatsSource(),
    ],
)

result = runner.run()

print(result)