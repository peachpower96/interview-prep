# SQL patterns

Solutions are written for **MySQL 8**. Table shapes are in [schemas.sql](schemas.sql); there is no data here, so create a few rows (include edge cases) before trusting any query. These queries were carried over from practice drills that were run in a browser against a MySQL-compatibility layer; they have **not** been re-run against a real MySQL server in this repo.

| File | Patterns |
|---|---|
| `01_basics_dedupe_grouping.sql` | DISTINCT, MIN per group, group twice (CTE), LAG, window `MIN() OVER` |
| `02_ranking_top_n.sql` | ROW_NUMBER vs RANK vs DENSE_RANK, top-N per group, keep latest row per key, top-N with LIMIT |
| `03_joins.sql` | Join as lookup, anti-join (`LEFT JOIN ... IS NULL`), multi-table joins, fan-out |
| `04_conditional_aggregation_rates.sql` | `SUM(CASE ...)`, rates, two averages at different levels, aggregate before join, COALESCE |
| `05_windows_time_series.sql` | Running/rolling sums, LAG on timestamps, relative time windows, gaps and islands, cohort retention |
| `06_filters_having_ranges.sql` | WHERE vs HAVING, half-open timestamp ranges, two groupings in two steps |

## Order of execution (explains most errors)

`FROM / JOIN` → `WHERE` → `GROUP BY` → `HAVING` → window functions → `SELECT` → `ORDER BY` → `LIMIT`.
So: aggregates cannot be used in WHERE; a window alias cannot be filtered in the same SELECT; ORDER BY can use SELECT aliases.

## Seven shapes to recognize

1. Grouping and counting: sort into piles, count each.
2. First time: MIN per person, then count per date.
3. Removing duplicates: DISTINCT on the combination, or ROW_NUMBER and keep 1.
4. Top N per group: ROW_NUMBER / DENSE_RANK in a CTE, keep rank ≤ N.
5. Compare to the row above: LAG.
6. Running totals and rolling metrics: `SUM(...) OVER (ORDER BY ...)` plus a ROWS frame.
7. Streaks: gaps and islands (`id - ROW_NUMBER()` is constant within a run).

"How many X per Y, where Y is computed per X first" means group twice: first grouping in a CTE, then group its result.

## Questions to answer out loud

- **WHERE vs HAVING?** WHERE filters rows before grouping; HAVING filters groups after, so it can use aggregates. Filter in WHERE when you can.
- **INNER vs LEFT JOIN; when do row counts change?** INNER keeps matches; LEFT keeps every left row with NULLs. Rows multiply when the right side has several rows per key (fan-out), inflating SUM/COUNT.
- **COUNT(\*) vs COUNT(col) vs COUNT(DISTINCT col)?** Rows; non-NULL values; unique non-NULL values.
- **Window function vs GROUP BY?** GROUP BY collapses groups; a window keeps every row and adds a group-level value.
- **UNION vs UNION ALL?** UNION removes duplicates (costs a sort/hash); prefer UNION ALL unless you need the dedupe.
- **Why is NOT IN dangerous?** If the subquery returns any NULL, `x NOT IN (...)` is never true. Use NOT EXISTS or a LEFT JOIN ... IS NULL anti-join.
- **CTE vs subquery?** Usually the same speed; CTEs are for readability. Use one when there is a real step.
- **Keep only the latest row per key?** `ROW_NUMBER() OVER (PARTITION BY key ORDER BY updated_at DESC)`, keep `rn = 1`.
- **Query is slow; what do you check?** Read the plan (`EXPLAIN`); index join/filter columns; filter early; select only needed columns; do not wrap an indexed column in a function in WHERE (`DATE(ts) = ...` cannot use an index on `ts`; use a range). Large tables: partition by date; keep a pre-aggregated daily summary for repeated dashboards. In MySQL's EXPLAIN, `type: ALL` is a full scan; `Using filesort` / `Using temporary` signal expensive sorts or temp tables.
- **Correlated subquery that runs once per row?** Rewrite as a join to a pre-aggregated CTE.

## MySQL specifics

- `DATE_SUB(x, INTERVAL 1 DAY)`, `x - INTERVAL 24 HOUR`, `TIMESTAMPDIFF(MINUTE, a, b)` (earlier first), `DATEDIFF(later, earlier)`, `DATE_FORMAT(ts, '%Y-%m-01')`, `IFNULL`, `LIMIT offset, count`.
- `ONLY_FULL_GROUP_BY` is on by default in MySQL 8: a selected column that is neither grouped nor aggregated is an error.
- Dividing by 0 gives NULL; `/` gives a decimal. Writing `100.0 * ...` is the safe habit in every database.
- Postgres-only syntax to avoid: `::date`, `DATE_TRUNC`, `INTERVAL '1 day'`, `EXTRACT(EPOCH ...)`, `ILIKE`.
