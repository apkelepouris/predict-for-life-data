"""
Predict For Life - Database Validation Result

Represents the outcome of validating the local
database against a validated lottery draw.
"""

from __future__ import annotations

from dataclasses import dataclass

from automation.models.database_action import DatabaseAction
from automation.models.draw import Draw


@dataclass
class DatabaseValidationResult:
    """
    Result returned by the DatabaseValidator.
    """

    action: DatabaseAction

    database_draw: Draw | None

    validated_draw: Draw | None

    message: str