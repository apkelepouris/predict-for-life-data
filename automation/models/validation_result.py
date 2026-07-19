"""
Predict For Life - Validation Result

Represents the outcome of validating the latest
draw results.
"""

from __future__ import annotations

from dataclasses import dataclass

from automation.models.draw import Draw
from automation.models.source_result import SourceResult
from automation.models.validation_action import ValidationAction


@dataclass(slots=True)
class ValidationResult:
    """
    Result returned by the Validation Engine.
    """

    action: ValidationAction

    validated_draw: Draw | None

    awaiting_final_source: bool

    matching_results: list[SourceResult]

    mismatched_results: list[SourceResult]

    failed_results: list[SourceResult]

    database_matches: bool

    message: str