"""
Predict For Life - Automation Trigger

Defines what initiated an automation run.
"""

from __future__ import annotations

from enum import Enum, auto


class AutomationTrigger(Enum):
    """
    Defines the trigger for an automation run.
    """

    DRAW_MONITOR = auto()

    HEARTBEAT = auto()

    MANUAL = auto()