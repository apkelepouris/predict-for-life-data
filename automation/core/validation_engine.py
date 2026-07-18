"""
Predict For Life - Validation Engine

Determines whether the latest draw should be published
by comparing the current database against multiple
independent draw sources.
"""

from __future__ import annotations

from automation.models.draw import Draw
from automation.models.source_result import SourceResult
from automation.models.validation_action import ValidationAction
from automation.models.validation_result import ValidationResult


class ValidationEngine:
    """
    Validates multiple draw sources and determines
    the next action for the automation.
    """

    def validate(
        self,
        database_draw: Draw,
        source_results: list[SourceResult],
    ):
        """
        Validate the supplied source results.

        Parameters
        ----------
        database_draw
            Latest draw currently stored in the database.

        source_results
            Results returned by all configured sources.
        """

        successful_results, failed_results = self._split_results(
            source_results,
        )

        newer_results = self._find_newer_results(
            database_draw,
            successful_results,
        )

        if not newer_results:

            return ValidationResult(
                action=ValidationAction.NO_NEW_DRAW,
                validated_draw=None,
                matching_results=[],
                mismatched_results=[],
                failed_results=failed_results,
                database_matches=True,
                message="No newer draw has been published.",
            )

        groups = self._find_groups(
            newer_results,
        )

        largest_group_data = self._find_largest_group(
            groups,
        )

        draw_key, largest_group = largest_group_data

        mismatched_results = self._find_mismatched_results(
            newer_results,
            largest_group,
        )        

        has_majority = self._has_majority(
            largest_group,
            newer_results,
        )

        has_sufficient_sources = self._has_sufficient_sources(
            newer_results,
        )

        if not has_sufficient_sources:

            return ValidationResult(
                action=ValidationAction.CONTINUE_MONITORING,
                validated_draw=None,
                matching_results=[],
                mismatched_results=mismatched_results,
                failed_results=failed_results,
                database_matches=False,
                message=(
                    "Only one source has published a newer draw. "
                    "Continue monitoring for additional sources."
                ),
            )

        if has_majority:

            validated_draw = largest_group[0].draw

            return ValidationResult(
                action=ValidationAction.UPDATE_DATABASE,
                validated_draw=validated_draw,
                matching_results=largest_group,
                mismatched_results=[],
                failed_results=failed_results,
                database_matches=False,
                message="Majority validation succeeded.",
            )

        return ValidationResult(
            action=ValidationAction.CONTINUE_MONITORING,
            validated_draw=None,
            matching_results=largest_group,
            mismatched_results=mismatched_results,
            failed_results=failed_results,
            database_matches=False,
            message=(
                "Updated sources do not yet agree. "
                "Continue monitoring for consensus."
            ),
        )

    def _has_sufficient_sources(
        self,
        newer_results: list[SourceResult],
    ) -> bool:
        """
        Determine whether enough independent sources have
        published a newer draw.
        """

        return len(newer_results) >= 2
            
    def _split_results(
        self,
        source_results: list[SourceResult],
    ) -> tuple[list[SourceResult], list[SourceResult]]:
        """
        Split source results into successful and failed groups.
        """

        successful_results = [
            result
            for result in source_results
            if result.success
        ]

        failed_results = [
            result
            for result in source_results
            if not result.success
        ]

        return successful_results, failed_results

    def _find_newer_results(
        self,
        database_draw: Draw,
        successful_results: list[SourceResult],
    ) -> list[SourceResult]:
        """
        Return only the successful source results that contain
        a draw newer than the current database.
        """

        newer_results = [
            result
            for result in successful_results
            if result.draw is not None
            and result.draw.draw_date > database_draw.draw_date
        ]

        return newer_results

    def _find_groups(
        self,
        newer_results: list[SourceResult],
    ) -> dict[tuple, list[SourceResult]]:
        """
        Group SourceResults by identical Draw.
        """

        groups: dict[
            tuple,
            list[SourceResult],
        ] = {}

        for result in newer_results:

            key = (
                result.draw.draw_date,
                tuple(result.draw.main_numbers),
                result.draw.life_ball,
            )

            groups.setdefault(
                key,
                [],
            ).append(result)

        return groups

    def _find_largest_group(
        self,
        groups: dict[tuple, list[SourceResult]],
    ) -> tuple[tuple, list[SourceResult]] | None:
        """
        Return the largest group of matching SourceResults.
        """

        if not groups:
            return None

        return max(
            groups.items(),
            key=lambda x: len(x[1]),
        )

    def _find_mismatched_results(
        self,
        newer_results: list[SourceResult],
        largest_group: list[SourceResult],
    ) -> list[SourceResult]:
        """
        Return the newer SourceResults that do not belong
        to the largest matching group.
        """

        return [
            result
            for result in newer_results
            if result not in largest_group
        ]

    def _has_majority(
        self,
        largest_group: list[SourceResult],
        newer_results: list[SourceResult],
    ) -> bool:
        """
        Determine whether the largest group represents
        a true majority of the newer results.
        """

        if not newer_results:
            return False

        return len(largest_group) > len(newer_results) / 2      