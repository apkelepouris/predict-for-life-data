"""
Predict For Life - Monitoring State

Stores monitoring state between
automation runs.
"""

from __future__ import annotations

import json

from datetime import date
from pathlib import Path


class MonitoringState:
    """
    Reads and writes the monitoring state.
    """

    STATE_FILE = Path(
        "automation/state/monitoring_state.json"
    )

    def __init__(
        self,
        state_file: str | Path | None = None,
    ) -> None:
        """
        Initialise monitoring state storage.
        """

        self.state_file = (
            Path(state_file)
            if state_file is not None
            else self.STATE_FILE
        )

    def load(self) -> dict:
        """
        Load the monitoring state.
        """

        if not self.state_file.exists():

            self.state_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self.save(
                {
                    "draw_date": None,
                    "awaiting_final_source": False,
                    "pending_source": None,
                    "database_update_email_sent": False,
                    "third_source_warning_sent": False,
                    "third_source_confirmation_sent": False,
                    "validation_timeout_sent": False,
                }
            )

        with self.state_file.open(
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    def save(
        self,
        state: dict,
    ) -> None:
        """
        Save the monitoring state.
        """

        with self.state_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                state,
                file,
                indent=4,
            )

    def reset_for_new_draw(
        self,
        draw_date: date,
    ) -> None:
        """
        Reset the monitoring state if a new
        draw is detected.
        """

        state = self.load()

        if state["draw_date"] == draw_date.isoformat():

            return

        state["draw_date"] = draw_date.isoformat()

        state["awaiting_final_source"] = False
        state["pending_source"] = None

        state["database_update_email_sent"] = False
        state["third_source_warning_sent"] = False
        state["third_source_confirmation_sent"] = False
        state["validation_timeout_sent"] = False

        self.save(state)

    def begin_follow_up(
        self,
        pending_source: str,
    ) -> None:
        """
        Mark that follow-up monitoring is
        required for the current draw.
        """

        state = self.load()

        state["awaiting_final_source"] = True
        state["pending_source"] = pending_source

        self.save(state)

    def end_follow_up(
        self,
    ) -> None:
        """
        Mark that follow-up monitoring has
        finished.
        """

        state = self.load()

        state["awaiting_final_source"] = False
        state["pending_source"] = None

        self.save(state)

    def validation_timeout_sent(
        self,
    ) -> bool:
        """
        Return True if the validation timeout
        notification has already been sent.
        """

        state = self.load()

        return state["validation_timeout_sent"]

    def mark_validation_timeout_sent(
        self,
    ) -> None:
        """
        Record that the validation timeout
        notification has been sent.
        """

        state = self.load()

        state["validation_timeout_sent"] = True

        self.save(state)

    def is_follow_up_active(
        self,
    ) -> bool:
        """
        Return True if follow-up monitoring
        is currently active.
        """

        state = self.load()

        return state["awaiting_final_source"]