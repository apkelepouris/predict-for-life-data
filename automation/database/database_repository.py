"""
Predict For Life - Database Repository

Provides access to the local lottery draw database.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from automation.models.draw import Draw


class DatabaseRepository:
    """
    Reads the local draw database.
    """

    def __init__(
        self,
        database_path: str | Path,
    ) -> None:

        self.database_path = Path(database_path)

    def latest_draw(self) -> Draw:
        """
        Return the latest draw stored in the database.
        """

        with self.database_path.open(
            newline="",
            encoding="utf-8",
        ) as csv_file:

            rows = [
                row
                for row in csv.DictReader(csv_file)
                if row["Date"].strip()
            ]

        last_row = rows[-1]

        return Draw(
            draw_date=datetime.strptime(
                last_row["Date"],
                "%d/%m/%Y",
            ).date(),
            main_numbers=[
                int(last_row["N1"]),
                int(last_row["N2"]),
                int(last_row["N3"]),
                int(last_row["N4"]),
                int(last_row["N5"]),
            ],
            life_ball=int(last_row["Life"]),
        )