"""
Predict For Life - HTTP Draw Source

Provides common HTTP functionality shared by all draw sources.

This class is responsible only for downloading content from remote
servers. It knows nothing about lottery draws.
"""

from __future__ import annotations

import requests

from automation.sources.base import DrawSource


class HttpDrawSource(DrawSource):
    """
    Base class for HTTP-based draw sources.
    """

    REQUEST_TIMEOUT = 10

    def get_json(self, url: str) -> dict:
        """
        Download a JSON document.

        Parameters
        ----------
        url
            Endpoint to download.

        Returns
        -------
        dict
            Parsed JSON document.
        """

        response = requests.get(
            url,
            timeout=self.REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()
    
    def get_html(self, url: str) -> str:
        """
        Download an HTML document.

        Parameters
        ----------
        url
            Endpoint to download.

        Returns
        -------
        str
            HTML document.
        """

        response = requests.get(
            url,
            timeout=self.REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.text    