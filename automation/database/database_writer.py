"""
Predict For Life - Database Writer

Writes validated lottery draws to the local database.
"""

from __future__ import annotations

import csv
from pathlib import Path

from automation.models.draw import Draw


class DatabaseWriter:
    """
    Writes to the local draw database.
    """

    def __init__(
        self,
        database_path: str | Path,
    ) -> None:

        self.database_path = Path(database_path)

    def append_draw(
        self,
        draw: Draw,
    ) -> None:
        """
        Append a validated draw to the database.
        """

        with self.database_path.open(
            mode="a",
            newline="",
            encoding="utf-8",
        ) as csv_file:

            writer = csv.writer(csv_file)

            writer.writerow(
                [
                    draw.draw_date.strftime("%d/%m/%Y"),
                    draw.main_numbers[0],
                    draw.main_numbers[1],
                    draw.main_numbers[2],
                    draw.main_numbers[3],
                    draw.main_numbers[4],
                    draw.life_ball,
                ]
            )