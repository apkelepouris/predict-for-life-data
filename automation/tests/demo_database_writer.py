from datetime import date

from automation.database.database_writer import (
    DatabaseWriter,
)
from automation.models.draw import Draw

writer = DatabaseWriter(
    "test_database.csv",
)

writer.append_draw(
    Draw(
        draw_date=date(2026, 7, 21),
        main_numbers=[1, 2, 3, 4, 5],
        life_ball=6,
    )
)

print("Draw appended.")