# interview-prep

Personal reference for software engineering interview prep: coding patterns with tested solutions, and system design write-ups.

## Layout

- `coding/` – design-style problems that grow in stages (stores, caches, readers): one folder per problem, a solution file plus pytest tests. See [coding/README.md](coding/README.md).
- `patterns/` – short algorithm problems grouped by pattern (hashing, stacks/queues, intervals/heaps, graphs/trees, strings, arrays/sorting, state machine), with tests.
- `sql/` – SQL patterns for MySQL 8, grouped by technique, with notes. See [sql/README.md](sql/README.md).
- `system-design/` – design write-ups, following requirements → core entities → API → data flow → high-level design → deep dives.

## Run the tests

```bash
pip install pytest
pytest coding patterns
```

SQL files are not run by the test suite.

All problems are generic practice patterns (many mirror public LeetCode problems, referenced by number).
