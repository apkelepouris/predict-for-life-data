"""
Simple demonstration of HttpDrawSource.

Verifies that the shared HTTP helper methods work correctly.
"""

from automation.sources.http_source import HttpDrawSource


class DemoSource(HttpDrawSource):

    @property
    def name(self) -> str:
        return "Demo"

    @property
    def url(self) -> str:
        return "https://example.com"

    def fetch(self):
        raise NotImplementedError


source = DemoSource()

html = source.get_html(source.url)

print(f"Downloaded {len(html)} characters.")