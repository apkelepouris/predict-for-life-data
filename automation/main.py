"""
Predict For Life - Automation Entry Point

Runs one complete automation cycle.
"""

from __future__ import annotations

from automation.core.automation_runner import (
    AutomationRunner,
)


def main() -> None:
    """
    Execute one automation cycle.
    """

    runner = AutomationRunner()

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