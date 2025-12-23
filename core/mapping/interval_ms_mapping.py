# core/mapping/interval_ms_mapping.py

from core.models.enums import Interval

INTERVAL_MS_MAPPING: dict[Interval, int] = {
    Interval.M1: 60_000,
    Interval.M5: 5 * 60_000,
    Interval.M15: 15 * 60_000,
    Interval.H1: 60 * 60_000,
    Interval.H4: 4 * 60 * 60_000,
    Interval.D1: 24 * 60 * 60_000,
    Interval.W1: 7 * 24 * 60 * 60_000,
}
