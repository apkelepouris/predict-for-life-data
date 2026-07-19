"""
Predict For Life - Automation Entry Point

Runs one complete automation cycle.
"""

from __future__ import annotations

import sys

from automation.core.automation_runner import (
    AutomationRunner,
)


def main() -> None:
    """
    Execute one automation cycle.
    """

    database_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "set_for_life.csv"
    )

    runner = AutomationRunner(
        database_path=database_path,
    )

    result = runner.run()

    print()
    print("Automation completed")
    print("--------------------")
    print(f"Result : {result.action.name}")
    print(f"Message: {result.message}")

    if hasattr(result, "validated_draw"):

        if result.validated_draw is not None:

            print()
            print("Validated draw:")
            print(result.validated_draw)


if __name__ == "__main__":
    main()