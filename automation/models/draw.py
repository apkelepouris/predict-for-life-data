"""
Predict For Life - Draw Model

Defines the standard Draw object used throughout the automation.

Every results source (National Lottery, Lotto.net, etc.) must return
exactly one Draw object for each draw found.

Using a common model means the validator, updater and notifier never
need to know where the data originated.
"""

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class Draw:
    """
    Represents a single Set For Life draw.

    Attributes
    ----------
    draw_date
        Date the draw took place.

    main_numbers
        The five main numbers in ascending order.

    life_ball
        The Life Ball.
    """

    draw_date: date
    main_numbers: list[int]
    life_ball: int

    def __post_init__(self) -> None:
        """
        Validate the draw immediately after creation.

        This prevents invalid data entering the automation and catches
        parsing errors as early as possible.
        """

        if len(self.main_numbers) != 5:
            raise ValueError(
                "A Set For Life draw must contain exactly five main numbers."
            )

        if sorted(self.main_numbers) != self.main_numbers:
            raise ValueError(
                "Main numbers must be sorted in ascending order."
            )

        if len(set(self.main_numbers)) != 5:
            raise ValueError(
                "Duplicate main numbers detected."
            )

        for number in self.main_numbers:
            if not 1 <= number <= 47:
                raise ValueError(
                    f"Invalid main number: {number}"
                )

        if not 1 <= self.life_ball <= 10:
            raise ValueError(
                f"Invalid Life Ball: {self.life_ball}"
            )
        
    def __str__(self) -> str:
        """
        Return a human-readable representation of the draw.
        """

        numbers = " ".join(str(n) for n in self.main_numbers)
        return (
            f"{self.draw_date.isoformat()} | "
            f"{numbers} | "
            f"Life Ball {self.life_ball}"
        )        