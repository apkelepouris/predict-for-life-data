"""
Predict For Life - CSV Reader

Loads the historical Set For Life database from the local CSV file.

The CSV is converted into a list of Draw objects. Each Draw validates
itself during construction, ensuring invalid data is detected
immediately.

The returned list is always sorted chronologically.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from automation.models.draw import Draw


def load_draw_history(csv_path: Path) -> list[Draw]:
    """
    Load the complete historical draw database.

    Parameters
    ----------
    csv_path
        Path to set_for_life.csv.

    Returns
    -------
    list[Draw]
        Historical draws sorted by draw date.
    """

    draws: list[Draw] = []

    with csv_path.open(
        mode="r",
        newline="",
        encoding="utf-8-sig"
    ) as csv_file:

        reader = csv.DictReader(csv_file)

        for row in reader:

            draw = Draw(
                draw_date=datetime.strptime(
                    row["Date"],
                    "%d/%m/%Y"
                ).date(),

                main_numbers=[
                    int(row["N1"]),
                    int(row["N2"]),
                    int(row["N3"]),
                    int(row["N4"]),
                    int(row["N5"]),
                ],

                life_ball=int(row["Life"]),
            )

            draws.append(draw)

    draws.sort(key=lambda draw: draw.draw_date)

    print(f"Loaded {len(draws)} historical draws.")

    if draws:
        print(f"Oldest : {draws[0].draw_date}")
        print(f"Latest : {draws[-1].draw_date}")

    return draws