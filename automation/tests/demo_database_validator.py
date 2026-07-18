from datetime import date

from automation.core.database_validator import DatabaseValidator
from automation.models.draw import Draw

database_draw = Draw(
    draw_date=date(2026, 7, 24),
    main_numbers=[5, 13, 24, 33, 40],
    life_ball=10,
)

validated_draw = Draw(
    draw_date=date(2026, 7, 21),
    main_numbers=[6, 12, 18, 30, 44],
    life_ball=7,
)

validator = DatabaseValidator()

result = validator.validate(
    database_draw,
    validated_draw,
)

print(result)