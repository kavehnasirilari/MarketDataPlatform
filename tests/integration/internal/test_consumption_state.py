import pytest

from api_service.app.api.flow.consumption.snapshot import ConsumptionState


def test_consumption_state_creates_new_record_and_returns_snapshot(monkeypatch):
    monkeypatch.setattr(
        "api_service.app.api.flow.consumption.snapshot.time.time",
        lambda: 1000.0,
    )

    state = ConsumptionState(window_seconds=60)

    snapshot = state.observe_and_update(
        consumer_ref="ip:127.0.0.1",
        units=1,
    )

    assert snapshot.consumer_ref == "ip:127.0.0.1"
    assert snapshot.consumed_units == 1
    assert snapshot.remaining_window_seconds == 60


def test_consumption_state_accumulates_units_inside_same_window(monkeypatch):
    current_time = 1000.0

    monkeypatch.setattr(
        "api_service.app.api.flow.consumption.snapshot.time.time",
        lambda: current_time,
    )

    state = ConsumptionState(window_seconds=60)

    state.observe_and_update("ip:127.0.0.1", units=1)
    snapshot = state.observe_and_update("ip:127.0.0.1", units=2)

    assert snapshot.consumed_units == 3
    assert snapshot.remaining_window_seconds == 60


def test_consumption_state_tracks_consumers_independently(monkeypatch):
    monkeypatch.setattr(
        "api_service.app.api.flow.consumption.snapshot.time.time",
        lambda: 1000.0,
    )

    state = ConsumptionState(window_seconds=60)

    first = state.observe_and_update("ip:127.0.0.1", units=2)
    second = state.observe_and_update("ip:10.0.0.1", units=1)

    assert first.consumed_units == 2
    assert second.consumed_units == 1
    assert len(state.records) == 2


def test_consumption_state_resets_after_window_expiration(monkeypatch):
    now = 1000.0

    monkeypatch.setattr(
        "api_service.app.api.flow.consumption.snapshot.time.time",
        lambda: now,
    )

    state = ConsumptionState(window_seconds=60)

    state.observe_and_update("ip:127.0.0.1", units=5)

    now = 1061.0

    snapshot = state.observe_and_update("ip:127.0.0.1", units=1)

    assert snapshot.consumed_units == 1
    assert snapshot.remaining_window_seconds == 60


def test_consumption_snapshot_is_immutable(monkeypatch):
    monkeypatch.setattr(
        "api_service.app.api.flow.consumption.snapshot.time.time",
        lambda: 1000.0,
    )

    state = ConsumptionState(window_seconds=60)

    snapshot = state.observe_and_update("ip:127.0.0.1", units=1)

    with pytest.raises(Exception):
        snapshot.consumed_units = 999


def test_consumption_state_allows_zero_unit_observation(monkeypatch):
    monkeypatch.setattr(
        "api_service.app.api.flow.consumption.snapshot.time.time",
        lambda: 1000.0,
    )

    state = ConsumptionState(window_seconds=60)

    snapshot = state.observe_and_update(
        consumer_ref="ip:127.0.0.1",
        units=0,
    )

    assert snapshot.consumed_units == 0
    assert snapshot.remaining_window_seconds == 60
