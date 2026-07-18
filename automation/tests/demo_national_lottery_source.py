"""
Integration test for the National Lottery source.

This test connects to the official National Lottery API and verifies
that the latest Set For Life draw can be retrieved and validated.
"""

from automation.sources.national_lottery import NationalLotterySource


def main() -> None:
    """
    Run the integration test.
    """

    source = NationalLotterySource()

    result = source.fetch()

    assert result.success, (
        f"Source failed: {result.error_message}"
    )

    assert result.draw is not None

    assert len(result.draw.main_numbers) == 5

    assert result.draw.main_numbers == sorted(result.draw.main_numbers)

    assert 1 <= result.draw.life_ball <= 10

    print("✓ National Lottery integration test passed")

    print(result.draw)


if __name__ == "__main__":
    main()