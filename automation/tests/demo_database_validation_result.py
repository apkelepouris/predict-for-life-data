from datetime import date

from automation.models.database_action import DatabaseAction
from automation.models.database_validation_result import (
    DatabaseValidationResult,
)
from automation.models.draw import Draw

database_draw = Draw(
    draw_date=date(2026, 7, 16),
    main_numbers=[5, 13, 24, 33, 40],
    life_ball=10,
)

validated_draw = Draw(
    draw_date=date(2026, 7, 24),
    main_numbers=[6, 12, 18, 30, 44],
    life_ball=7,
)

result = DatabaseValidationResult(
    action=DatabaseAction.DATABASE_UPDATE_REQUIRED,
    database_draw=database_draw,
    validated_draw=validated_draw,
    message="Database requires updating.",
)

print(result)