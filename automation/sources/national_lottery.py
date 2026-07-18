"""
Predict For Life - National Lottery Source

Downloads the latest Set For Life draw from the official
National Lottery website.
"""

from __future__ import annotations

from datetime import datetime

import requests

from automation.models.draw import Draw
from automation.models.source_result import SourceResult
from automation.models.source_status import SourceStatus
from automation.sources.http_source import HttpDrawSource


class OfficialNationalLotterySource(HttpDrawSource):
    """
    Official National Lottery results source.
    """

    API_URL = (
    "https://api-dfe.national-lottery.co.uk/"
    "draw-game/results/3"
    )

    @property
    def name(self) -> str:
        return "National Lottery"

    @property
    def url(self) -> str:
        return (
            "https://www.national-lottery.co.uk/results/"
            "set-for-life/draw-history"
        )

    def fetch(self) -> SourceResult:
        """
        Download the latest Set For Life draw from the official
        National Lottery API and return it as a SourceResult.
        """

        try:

            data = self.get_json(self.API_URL)

            latest = data["drawResults"][0]

            draw_date = datetime.fromisoformat(
                latest["drawDate"].replace("Z", "+00:00")
            ).date()

            drawn_numbers = latest["drawnNumbers"]["drawnNumbers"]

            main_numbers = drawn_numbers["primaryNumbers"]

            life_ball = drawn_numbers["secondaryNumbers"][0]

            draw = Draw(
                draw_date=draw_date,
                main_numbers=main_numbers,
                life_ball=life_ball,
            )

            return SourceResult(
                source_name=self.name,
                url=self.url,
                status=SourceStatus.SUCCESS,
                draw=draw,
                retrieved_at=datetime.now(),
            )

        except requests.RequestException as ex:

            return SourceResult(
                source_name=self.name,
                url=self.url,
                status=SourceStatus.NETWORK_ERROR,
                error_message=str(ex),
            )

        except (ValueError, KeyError, IndexError) as ex:

            return SourceResult(
                source_name=self.name,
                url=self.url,
                status=SourceStatus.DATA_ERROR,
                error_message=str(ex),
            )        