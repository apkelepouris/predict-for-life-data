"""
Predict For Life - Automation Runner

Coordinates a complete validation cycle by querying all
configured draw sources and passing the results through
the validation pipeline.
"""

from __future__ import annotations

from automation.core.database_validator import DatabaseValidator
from automation.core.validation_engine import ValidationEngine
from automation.models.validation_result import ValidationResult
from automation.models.validation_action import ValidationAction
from automation.sources.lottery_stats import LotteryStatsSource
from automation.sources.national_lottery import (
    OfficialNationalLotterySource,
)
from automation.sources.national_lottery_com import (
    NationalLotteryComSource,
)
from automation.database.database_repository import (
    DatabaseRepository,
)
from automation.database.database_writer import (
    DatabaseWriter,
)
from automation.models.database_action import (
    DatabaseAction,
)


class AutomationRunner:
    """
    Coordinates one complete automation run.
    """

    def __init__(self) -> None:

        self.sources = [
            OfficialNationalLotterySource(),
            NationalLotteryComSource(),
            LotteryStatsSource(),
        ]

        self.validation_engine = ValidationEngine()

        self.database_validator = DatabaseValidator()

        self.database_repository = DatabaseRepository(
            "set_for_life.csv",
        )

        self.database_writer = DatabaseWriter(
            "set_for_life.csv",
        )

    def run(self):
        """
        Execute one complete automation cycle.
        """

        source_results = [
            source.fetch()
            for source in self.sources
        ]

        database_draw = self.database_repository.latest_draw()

        validation_result = self.validation_engine.validate(
            database_draw,
            source_results,
        )

        if validation_result.action != ValidationAction.UPDATE_DATABASE:

            return validation_result
        
        database_validation = self.database_validator.validate(
            database_draw,
            validation_result.validated_draw,
        )

        if (
            database_validation.action
            == DatabaseAction.DATABASE_UPDATE_REQUIRED
        ):

            self.database_writer.append_draw(
                validation_result.validated_draw,
            )

        return database_validation