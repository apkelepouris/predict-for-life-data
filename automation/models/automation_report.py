"""
Predict For Life - Automation Report

Represents the outcome of one automation run.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from automation.models.automation_trigger import (
    AutomationTrigger,
)


@dataclass
class AutomationReport:
    """
    Represents one automation execution.
    """

    timestamp: datetime

    trigger: AutomationTrigger

    outcome: str

    message: str

    duration_seconds: float