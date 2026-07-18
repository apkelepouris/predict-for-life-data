"""
Predict For Life - Source Status

Defines the possible outcomes when querying a draw source.
"""

from __future__ import annotations

from enum import Enum, auto


class SourceStatus(Enum):
    """
    Status returned by a draw source.
    """

    SUCCESS = auto()

    NETWORK_ERROR = auto()

    PARSE_ERROR = auto()

    DATA_ERROR = auto()