from datetime import datetime
from zoneinfo import ZoneInfo

from automation.core.schedule_guard import ScheduleGuard


LONDON = ZoneInfo("Europe/London")


class FakeScheduleGuard(ScheduleGuard):

    def __init__(self, fake_datetime):
        self.fake_datetime = fake_datetime

    def _current_london_datetime(self):
        return self.fake_datetime


def make_guard(year, month, day, hour, minute):
    return FakeScheduleGuard(
        datetime(
            year,
            month,
            day,
            hour,
            minute,
            tzinfo=LONDON,
        )
    )


def test_monday_before_monitoring_window():
    guard = make_guard(2026, 7, 20, 19, 42)

    assert guard.is_draw_day() is True
    assert guard.is_active_monitoring_time() is False
    assert guard.should_run() is False
    assert guard.monitoring_window_closed() is False


def test_monday_at_monitoring_start():
    guard = make_guard(2026, 7, 20, 19, 43)

    assert guard.is_draw_day() is True
    assert guard.is_active_monitoring_time() is True
    assert guard.should_run() is True
    assert guard.monitoring_window_closed() is False


def test_monday_during_monitoring():
    guard = make_guard(2026, 7, 20, 20, 30)

    assert guard.is_draw_day() is True
    assert guard.is_active_monitoring_time() is True
    assert guard.should_run() is True
    assert guard.monitoring_window_closed() is False


def test_monday_at_monitoring_end():
    guard = make_guard(2026, 7, 20, 21, 30)

    assert guard.is_draw_day() is True
    assert guard.is_active_monitoring_time() is False
    assert guard.should_run() is False
    assert guard.monitoring_window_closed() is True


def test_monday_after_monitoring_window():
    guard = make_guard(2026, 7, 20, 21, 31)

    assert guard.is_draw_day() is True
    assert guard.is_active_monitoring_time() is False
    assert guard.should_run() is False
    assert guard.monitoring_window_closed() is True


def test_thursday_during_monitoring():
    guard = make_guard(2026, 7, 23, 20, 30)

    assert guard.is_draw_day() is True
    assert guard.is_active_monitoring_time() is True
    assert guard.should_run() is True


def test_wednesday_is_not_draw_monitoring():
    guard = make_guard(2026, 7, 22, 20, 30)

    assert guard.is_draw_day() is False
    assert guard.is_active_monitoring_time() is False
    assert guard.monitoring_window_closed() is False