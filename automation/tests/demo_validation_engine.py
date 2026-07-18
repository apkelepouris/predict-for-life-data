from datetime import date, datetime

from automation.core.validation_engine import ValidationEngine
from automation.models.draw import Draw
from automation.models.source_result import SourceResult
from automation.models.source_status import SourceStatus

database_draw = Draw(
    draw_date=date(2026, 7, 21),
    main_numbers=[5, 13, 24, 33, 40],
    life_ball=10,
)

source_draw = Draw(
    draw_date=date(2026, 7, 24),
    main_numbers=[6, 12, 18, 30, 44],
    life_ball=7,
)

different_draw = Draw(
    draw_date=date(2026, 7, 24),
    main_numbers=[1, 2, 3, 4, 5],
    life_ball=6,
)

source_results = [

    SourceResult(
        source_name="National Lottery",
        url="https://example.com",
        status=SourceStatus.SUCCESS,
        draw=source_draw,
        retrieved_at=datetime.now(),
    ),

    SourceResult(
        source_name="National-Lottery.com",
        url="https://example.com",
        status=SourceStatus.SUCCESS,
        draw=different_draw,
        retrieved_at=datetime.now(),
    ),

    SourceResult(
        source_name="LotteryStats",
        url="https://example.com",
        status=SourceStatus.SUCCESS,
        draw=database_draw,
        retrieved_at=datetime.now(),
    ),

]

engine = ValidationEngine()

result = engine.validate(
    database_draw,
    source_results,
)

print(result)