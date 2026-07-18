"""
Predict For Life - Draw Source Interface

Defines the common interface implemented by every draw source.

Every source (National Lottery, LotteryStats, National-Lottery.com, etc.)
must inherit from DrawSource and return a SourceResult containing a validated Draw.

The rest of the automation never needs to know where the data came from.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from automation.models.source_result import SourceResult

class DrawSource(ABC):
    """
    Abstract base class for all draw result sources.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable name of the source.
        """
        ...

    @property
    @abstractmethod
    def url(self) -> str:
        """
        URL used to retrieve the latest results.
        """
        ...

    @abstractmethod
    def fetch(self) -> SourceResult:
        """
        Retrieve the latest published draw.

        Returns
        -------
        SourceResult
            Result of querying the draw source.
        """
        ...