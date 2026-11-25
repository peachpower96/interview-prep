-- Dialect: MySQL 8. Table shapes: see schemas.sql.
-- Pattern thread: number or rank rows in a CTE, then filter on the rank in the next step
-- (WHERE runs before SELECT, so a window alias does not exist yet in the same query).

-- 1. The 2 most expensive completed rides per city (ROW_NUMBER; never ties).   [Set B]
WITH numbered AS (
    SELECT city_id, ride_id, fare_usd,
           ROW_NUMBER() OVER (PARTITION BY city_id ORDER BY fare_usd DESC) AS rn
    FROM rides
    WHERE status = 'completed'
)
SELECT city_id, ride_id, fare_usd
FROM numbered
WHERE rn <= 2
ORDER BY city_id, rn;

-- 2. Top 3 ranks of drivers per city by completed rides, with ties (group, THEN rank).   [Set B]
--    counts 3,2,2,1:  ROW_NUMBER 1,2,3,4   RANK 1,2,2,4   DENSE_RANK 1,2,2,3
--    Say which you chose and why; "tie for third" is a classic follow-up.
WITH driver_counts AS (
    SELECT city_id, driver_id, COUNT(*) AS completed_rides
    FROM rides
    WHERE status = 'completed'
    GROUP BY city_id, driver_id
),
ranked AS (
    SELECT city_id, driver_id, completed_rides,
           DENSE_RANK() OVER (PARTITION BY city_id ORDER BY completed_rides DESC) AS driver_rank
    FROM driver_counts
)
SELECT city_id, driver_id, completed_rides, driver_rank
FROM ranked
WHERE driver_rank <= 3
ORDER BY city_id, driver_rank;

-- 3. Top 10 users by total distance (join, SUM per user, ORDER BY, LIMIT).   [Set D]
--    INNER JOIN drops users with no trips (a LEFT JOIN would bring them back with NULL totals).
--    ORDER BY may use the alias (it runs after SELECT); WHERE/HAVING may not.
--    Ask about ties at position 10 before writing LIMIT.
SELECT u.id AS user_id,
       u.name,
       SUM(t.distance) AS total_distance_traveled
FROM users u
INNER JOIN trips t ON u.id = t.user_id
GROUP BY u.id, u.name
ORDER BY total_distance_traveled DESC
LIMIT 10;

-- 4. Keep the latest row per email (dedupe with ROW_NUMBER).   [Set D]
--    The second ORDER BY key is the tie-break; without it tied rows come back in unpredictable order.
--    GROUP BY email + MAX(updated_at) then joining back breaks on ties (two rows match the max).
--    To delete duplicates instead: same numbering, delete where rn > 1.
WITH ranked AS (
    SELECT profile_id, email, updated_at,
           ROW_NUMBER() OVER (PARTITION BY email
                              ORDER BY updated_at DESC, profile_id DESC) AS rn
    FROM rider_profiles
)
SELECT profile_id, email, updated_at
FROM ranked
WHERE rn = 1
ORDER BY email;

-- 5. Top earner per state in a date range, ties included (RANK).   [Set C]
--    Half-open range (>= start, < day after end) includes all of the last day;
--    BETWEEN '2026-02-01' AND '2026-10-31' would cut Oct 31 at midnight.
WITH earnings AS (
    SELECT r.driver_id, d.state, SUM(r.price_usd) AS earnings
    FROM rides r
    JOIN drivers d ON d.driver_id = r.driver_id
    WHERE r.status = 'completed'
      AND r.requested_at >= '2026-02-01'
      AND r.requested_at <  '2026-11-01'
    GROUP BY r.driver_id, d.state
),
ranked AS (
    SELECT state, driver_id, earnings,
           RANK() OVER (PARTITION BY state ORDER BY earnings DESC) AS rnk
    FROM earnings
)
SELECT state, driver_id, earnings
FROM ranked
WHERE rnk = 1;
