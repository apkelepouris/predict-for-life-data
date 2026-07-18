"""
Predict For Life - Validation Action

Defines the action that should be taken after
validating the latest draw results.
"""

from __future__ import annotations

from enum import Enum, auto


class ValidationAction(Enum):
    """
    Action returned by the Validation Engine.
    """

    NO_NEW_DRAW = auto()

    CONTINUE_MONITORING = auto()

    UPDATE_DATABASE = auto()

    DATABASE_ALREADY_UPDATED = auto()

    DATABASE_MISMATCH = auto()

    VALIDATION_FAILED = auto()