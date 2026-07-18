"""
Predict For Life - National-Lottery.com Source

Downloads the latest Set For Life draw from
National-Lottery.com.
"""

from __future__ import annotations

from datetime import datetime

import requests

from bs4 import BeautifulSoup

from automation.models.draw import Draw
from automation.models.source_result import SourceResult
from automation.models.source_status import SourceStatus
from automation.sources.http_source import HttpDrawSource
from automation.utils.date_parser import parse_uk_date


class LotteryStatsSource(HttpDrawSource):
    """
    National-Lottery.com results source.
    """

    @property
    def name(self) -> str:
        return "LotteryStats"

    @property
    def url(self) -> str:
        return "https://www.lotterystats.co.uk/set_for_life/results"

    def fetch(self) -> SourceResult:
        """
        Download the latest results page.
        """

        try:

            html = self.get_html(self.url)

            soup = BeautifulSoup(
                html,
                "html.parser",
            )

            latest_result = soup.find(
                "div",
                class_="w3-padding-16 w3-center w3-mobile",
            )

            date_text = latest_result.find(
                "span",
                class_="testDate",
            ).get_text(strip=True)

            draw_date = parse_uk_date(date_text)

            ball_elements = latest_result.select("span.lotteryNum")

            drawn_numbers = [
                int(ball.get_text(strip=True))
                for ball in ball_elements
            ]

            main_numbers = drawn_numbers[:5]

            life_ball = drawn_numbers[5]

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

        except (
            ValueError,
            AttributeError,
            IndexError,
        ) as ex:

            return SourceResult(
                source_name=self.name,
                url=self.url,
                status=SourceStatus.DATA_ERROR,
                error_message=str(ex),
            )