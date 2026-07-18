"""
Predict For Life - Database Validator

Validates the local database against the
validated lottery draw.
"""

from __future__ import annotations

from automation.models.database_action import DatabaseAction
from automation.models.database_validation_result import (
    DatabaseValidationResult,
)
from automation.models.draw import Draw


class DatabaseValidator:
    """
    Validates the current database state.
    """

    def validate(
        self,
        database_draw: Draw,
        validated_draw: Draw,
    ) -> DatabaseValidationResult:
        """
        Validate the local database against
        the validated draw.
        """

        if self._draws_match(
            database_draw,
            validated_draw,
        ):

            return DatabaseValidationResult(
                action=DatabaseAction.DATABASE_ALREADY_CURRENT,
                database_draw=database_draw,
                validated_draw=validated_draw,
                message="Database is already up to date.",
            )

        if self._database_is_behind(
            database_draw,
            validated_draw,
        ):

            return DatabaseValidationResult(
                action=DatabaseAction.DATABASE_UPDATE_REQUIRED,
                database_draw=database_draw,
                validated_draw=validated_draw,
                message="Database requires updating.",
            )

        if self._database_is_newer(
            database_draw,
            validated_draw,
        ):

            return DatabaseValidationResult(
                action=DatabaseAction.DATABASE_NEWER_THAN_VALIDATED,
                database_draw=database_draw,
                validated_draw=validated_draw,
                message=(
                    "Database is newer than the validated draw."
                ),
            )

        if self._database_conflict(
            database_draw,
            validated_draw,
        ):

            return DatabaseValidationResult(
                action=DatabaseAction.DATABASE_CONFLICT,
                database_draw=database_draw,
                validated_draw=validated_draw,
                message=(
                    "Database conflicts with the validated draw."
                ),
            )

        raise RuntimeError(
            "Unhandled database validation scenario."
        )

    def _draws_match(
        self,
        database_draw: Draw,
        validated_draw: Draw,
    ) -> bool:
        """
        Determine whether two Draw objects are identical.
        """

        return (
            database_draw.draw_date == validated_draw.draw_date
            and database_draw.main_numbers == validated_draw.main_numbers
            and database_draw.life_ball == validated_draw.life_ball
        )

    def _database_is_behind(
        self,
        database_draw: Draw,
        validated_draw: Draw,
    ) -> bool:
        """
        Determine whether the database is older than
        the validated draw.
        """

        return (
            database_draw.draw_date
            < validated_draw.draw_date
        )
    
    def _database_is_newer(
        self,
        database_draw: Draw,
        validated_draw: Draw,
    ) -> bool:
        """
        Determine whether the database is newer than
        the validated draw.
        """

        return (
            database_draw.draw_date
            > validated_draw.draw_date
        )
    
    def _database_conflict(
        self,
        database_draw: Draw,
        validated_draw: Draw,
    ) -> bool:
        """
        Determine whether the database contains a different
        draw for the same draw date.
        """

        return (
            database_draw.draw_date
            == validated_draw.draw_date
            and not self._draws_match(
                database_draw,
                validated_draw,
            )
        )