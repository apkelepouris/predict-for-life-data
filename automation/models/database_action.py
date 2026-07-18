"""
Predict For Life - Database Action

Possible outcomes of validating the local database
against the validated lottery draw.
"""

from __future__ import annotations

from enum import Enum, auto


class DatabaseAction(Enum):
    """
    Possible database validation actions.
    """

    DATABASE_ALREADY_CURRENT = auto()

    DATABASE_UPDATE_REQUIRED = auto()

    DATABASE_CONFLICT = auto()

    DATABASE_NEWER_THAN_VALIDATED = auto()