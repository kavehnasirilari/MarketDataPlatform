## Syncer / Core Refactor TODOs

- [ ] Add `status` column to `canonical_symbols`
      - Required for safe logical deletion
      - Currently using hard DELETE in sync_symbols

- [ ] Make candle persistence idempotent
      - Current ingestion persistence is NOT idempotent
      - Duplicate candle inserts may raise IntegrityError
        and rollback the entire ingestion unit transaction
      - Required for safe re-runs and crash recovery
      - Expected solution:
        - PostgreSQL: INSERT ... ON CONFLICT DO NOTHING
        - or equivalent safe deduplication strategy
      - Blocking for Phase 4C (backfill / retry support)
      