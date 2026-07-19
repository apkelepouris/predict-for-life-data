"""
Predict For Life - Report Writer

Writes a human-readable automation report.
"""

from __future__ import annotations
from pathlib import Path



class ReportWriter:
    """
    Writes automation reports.
    """

    def write(
        self,
        timestamp: str,
        trigger: str,
        result: str,
        message: str,
        duration_seconds: float,
    ) -> None:
        """
        Write one automation report.
        """

        report_directory = Path("automation/reports")
        report_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_file = (
            report_directory
            / "latest_report.txt"
        )

        with report_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                "=============================================\n"
            )
            file.write(
                "Predict For Life Automation Report\n"
            )
            file.write(
                "=============================================\n\n"
            )

            file.write(f"Time     : {timestamp}\n")
            file.write(f"Trigger  : {trigger}\n")
            file.write(f"Result   : {result}\n")
            file.write(f"Message  : {message}\n")
            file.write(
                f"Duration : {duration_seconds:.2f} seconds\n"
            )