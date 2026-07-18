"""
Predict For Life - Fake Draw Source

Test implementation of DrawSource used for integration tests.
"""

from __future__ import annotations

from datetime import datetime

from automation.models.draw import Draw
from automation.models.source_result import SourceResult
from automation.models.source_status import SourceStatus
from automation.sources.base import DrawSource


class FakeDrawSource(DrawSource):
    """
    Returns a predefined draw.
    """

    def __init__(
        self,
        name: str,
        draw: Draw,
    ) -> None:

        self._name = name
        self._draw = draw

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return "https://fake.test"

    def fetch(self) -> SourceResult:

        return SourceResult(
            source_name=self.name,
            url=self.url,
            status=SourceStatus.SUCCESS,
            draw=self._draw,
            retrieved_at=datetime.now(),
        )