# flow/consumption/state.py

import time
from dataclasses import dataclass
from typing import Dict


@dataclass
class ConsumptionRecord:
    """
    Internal mutable record for a single consumer.
    This is an implementation detail of the Flow layer.
    """
    window_start: float
    consumed_units: int


@dataclass(frozen=True)
class ConsumptionSnapshot:
    """
    Immutable snapshot of consumption state,
    passed from Flow to Policy for decision making.
    """
    consumer_ref: str
    consumed_units: int
    remaining_window_seconds: int


class ConsumptionState:
    """
    In-memory consumption state manager.

    Responsibilities:
    - Track consumption per consumer_ref
    - Apply fixed-window logic
    - Lazily reset expired windows
    - Produce ConsumptionSnapshot for Policy
    """

    def __init__(self, window_seconds: int):
        self.window_seconds = window_seconds
        self.records: Dict[str, ConsumptionRecord] = {}

    def observe_and_update(self, consumer_ref: str, units: int) -> ConsumptionSnapshot:
        """
        Observe a consumption event and update internal state.

        This method:
        - creates record if not exists
        - resets window if expired
        - increments consumed units
        - returns a snapshot for policy evaluation
        """
        now = time.time()

        record = self.records.get(consumer_ref)

        if record is None:
            record = ConsumptionRecord(
                window_start=now,
                consumed_units=0,
            )
            self.records[consumer_ref] = record

        # Check if current window expired (fixed window)
        if now - record.window_start >= self.window_seconds:
            record.window_start = now
            record.consumed_units = 0

        # Update consumption
        record.consumed_units += units

        return self._make_snapshot(consumer_ref, record, now)

    def _make_snapshot(
        self,
        consumer_ref: str,
        record: ConsumptionRecord,
        now: float,
    ) -> ConsumptionSnapshot:
        remaining = int(
            max(0, self.window_seconds - (now - record.window_start))
        )

        return ConsumptionSnapshot(
            consumer_ref=consumer_ref,
            consumed_units=record.consumed_units,
            remaining_window_seconds=remaining,
        )
