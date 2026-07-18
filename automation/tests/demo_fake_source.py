from datetime import date

from automation.models.draw import Draw
from automation.tests.fakes.fake_draw_source import (
    FakeDrawSource,
)

source = FakeDrawSource(
    "Fake Source",
    Draw(
        draw_date=date(2026, 7, 23),
        main_numbers=[6, 12, 18, 30, 44],
        life_ball=7,
    ),
)

print(source.fetch())