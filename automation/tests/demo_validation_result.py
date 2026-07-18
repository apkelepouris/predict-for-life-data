from datetime import date, datetime

from automation.models.draw import Draw
from automation.models.source_result import SourceResult
from automation.models.source_status import SourceStatus
from automation.models.validation_action import ValidationAction
from automation.models.validation_result import ValidationResult

draw = Draw(
    draw_date=date(2026, 7, 16),
    main_numbers=[5, 13, 24, 33, 40],
    life_ball=10,
)

source_result = SourceResult(
    source_name="National Lottery",
    url="https://example.com",
    status=SourceStatus.SUCCESS,
    draw=draw,
    retrieved_at=datetime.now(),
)

result = ValidationResult(
    action=ValidationAction.UPDATE_DATABASE,
    validated_draw=draw,
    matching_results=[source_result],
    mismatched_results=[],
    failed_results=[],
    database_matches=False,
    message="Validated by majority.",
)

print(result)