"""
Predict For Life - Schedule Guard

Determines whether the automation should
run based on the current UK date and time.
"""

from __future__ import annotations

from datetime import datetime, time
from zoneinfo import ZoneInfo


class ScheduleGuard:
    """
    Determines whether the automation
    should execute.
    """

    DRAW_DAYS = {0, 3}  # Monday, Thursday
    HEARTBEAT_DAYS = {1, 2, 4, 5, 6}  # Tue, Wed, Fri, Sat, Sun

    DRAW_START = time(19, 43)
    DRAW_END = time(21, 30)

    HEARTBEAT_TIME = time(12, 0)

    def should_run(self) -> bool:
        """
        Return True if the automation should run.
        """

        current_datetime = (
            self._current_london_datetime()
        )

        is_draw_day = self._is_draw_day(
            current_datetime,
        )

        is_heartbeat_day = self._is_heartbeat_day(
            current_datetime,
        )

        is_within_draw_window = (
            self._is_within_draw_window(
                current_datetime,
            )
        )

        if is_draw_day:

            return is_within_draw_window

        if is_heartbeat_day:

            return True

        return False

    def is_draw_day(
        self,
    ) -> bool:
        """
        Return True if today is a draw day
        in London.
        """

        return self._is_draw_day(
            self._current_london_datetime()
        )

    def is_active_monitoring_time(
        self,
    ) -> bool:
        """
        Return True if the current London
        time is inside the active draw
        monitoring window.
        """

        now = self._current_london_datetime()

        return (
            self._is_draw_day(now)
            and self._is_within_draw_window(now)
        )

    def _current_london_datetime(self) -> datetime:
        """
        Return the current date and time in London.
        """

        return datetime.now(
            ZoneInfo("Europe/London")
        )

    def _is_draw_day(
        self,
        current_datetime: datetime,
    ) -> bool:
        """
        Determine whether today is a draw day.
        """

        return (
            current_datetime.weekday()
            in self.DRAW_DAYS
        )

    def _is_heartbeat_day(
        self,
        current_datetime: datetime,
    ) -> bool:
        """
        Determine whether today is a heartbeat day.
        """

        return (
            current_datetime.weekday()
            in self.HEARTBEAT_DAYS
        )

    def _is_within_draw_window(
        self,
        current_datetime: datetime,
    ) -> bool:
        """
        Determine whether the current time
        is within the draw monitoring window.
        """

        current_time = current_datetime.time()

        return (
            self.DRAW_START
            <= current_time
            < self.DRAW_END
        )
    
    def monitoring_window_closed(
        self,
    ) -> bool:
        """
        Return True if the active monitoring
        window has ended on a draw day.
        """

        now = self._current_london_datetime()

        return (
            self._is_draw_day(now)
            and now.time() >= self.DRAW_END
        )