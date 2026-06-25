# Logging

## Purpose

The project uses **structured JSON logging** across all services.

All services share a single logging configuration from:

```text
core/observability/logging_config.py
```

The goal is to provide logs that are:

- Human-readable
- Machine-parseable
- Searchable
- Consistent across all services

---

# Log Structure

Every log contains a common set of fields.

## Standard Fields

| Field | Description |
|--------|-------------|
| `ts` | UTC timestamp |
| `level` | Log level |
| `logger` | Python logger name |
| `msg` | Human-readable message |

Example:

```json
{
  "ts": "...",
  "level": "INFO",
  "logger": "...",
  "msg": "Exchange synchronization started"
}
```

---

# Extra Fields

Application-specific fields are provided through the `extra` argument.

Example:

```python
logger.info(
    "Exchange synchronization started",
    extra={
        "service": "syncer-service",
        "event": "syncer.base_sync.exchanges_started",
        "status": "started",
        "operation": "sync_exchanges",
        "cycle_id": cycle_id,
    },
)
```

---

# Standard Extra Fields

The following fields should be used whenever applicable.

| Field | Purpose |
|--------|----------|
| `service` | Service name |
| `event` | Machine-readable event identifier |
| `status` | `started` / `success` / `partial_success` / `error` |
| `operation` | Logical operation being executed |
| `cycle_id` | Correlation identifier for a synchronization cycle |

Additional business-specific fields may be added when needed.

Examples:

- `exchange`
- `symbol`
- `interval`
- `market_type`
- `latency_ms`
- `added_count`
- `deleted_count`
- `inserted_count`

---

# Event Naming

Events follow a hierarchical naming convention.

Examples:

```text
syncer.base_sync.started
syncer.base_sync.exchanges_started
syncer.base_sync.exchanges_completed

syncer.scheduler_started

syncer.job_started
syncer.job_completed

syncer.unit_started
syncer.unit_completed
syncer.unit_failed
```

Events should remain stable because monitoring systems may depend on them.

---

# Exception Logging

Exceptions should always use:

```python
logger.exception(...)
```

instead of:

```python
logger.error(...)
```

This automatically includes:

- Exception type
- Exception message
- Full traceback

---

# Best Practices

- Keep `msg` short and human-readable.
- Put searchable information inside `extra`.
- Reuse the same `cycle_id` throughout a workflow.
- Prefer structured fields over formatted strings.
- Never log secrets, passwords, API keys, or sensitive user data.