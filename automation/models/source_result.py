"""
Predict For Life - Source Result

Represents the outcome of querying a results source.

Every source returns a SourceResult, whether successful or not.

This gives the validator complete visibility over:
- which source was queried
- whether it succeeded
- which draw was found
- when it was retrieved
- any error that occurred
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from automation.models.source_status import SourceStatus

from automation.models.draw import Draw


@dataclass(slots=True)
class SourceResult:
    """
    Result returned by a draw source.
    """

    source_name: str
    url: str

    status: SourceStatus

    draw: Draw | None = None

    retrieved_at: datetime | None = None

    error_message: str | None = None

    @property
    def success(self) -> bool:
        """
        Convenience property indicating whether the source completed
        successfully.

        This allows callers to continue using:

            if result.success:

        while the underlying implementation uses SourceStatus.
        """

        return self.status is SourceStatus.SUCCESS    