-- Dialect: MySQL 8. Table shapes: see schemas.sql.
-- Pattern thread: LAG/LEAD for "previous row", frames for rolling sums, row-number tricks for runs,
-- joining a cohort back to itself for retention.

-- 1. Running total and 3-day rolling sum per city.   [Set B: daily_rides]
--    SUM with ORDER BY inside OVER keeps a running total (without ORDER BY it is the grand total).
--    ROWS counts rows, not days: a missing day makes a 3-row window span more than 3 calendar days.
--    Fix by filling missing days first (calendar table + LEFT JOIN) or using a RANGE frame.
SELECT city_id,
       ride_date,
       completed_rides,
       SUM(completed_rides) OVER (PARTITION BY city_id ORDER BY ride_date) AS running_total,
       SUM(completed_rides) OVER (
           PARTITION BY city_id ORDER BY ride_date
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS rolling_3day
FROM daily_rides;

-- 2. Average idle minutes between a driver's rides (completed only; drivers with 1 ride excluded).   [Set B]
--    Filter to completed rides BEFORE LAG (a cancelled ride has no completed_at).
--    TIMESTAMPDIFF(unit, earlier, later): earlier first, or you get negatives.
WITH completed AS (
    SELECT driver_id, requested_at, completed_at
    FROM rides
    WHERE status = 'completed'
),
gaps AS (
    SELECT driver_id,
           requested_at,
           LAG(completed_at) OVER (PARTITION BY driver_id ORDER BY requested_at) AS prev_completed_at
    FROM completed
)
SELECT driver_id,
       ROUND(AVG(TIMESTAMPDIFF(MINUTE, prev_completed_at, requested_at)), 1) AS avg_idle_minutes
FROM gaps
WHERE prev_completed_at IS NOT NULL
GROUP BY driver_id;

-- 3. Completed rides per city in the last 24 hours of data.   [Set B]
--    Relative to the data: a scalar subquery gives the latest timestamp. Use >= so a ride exactly
--    24 hours earlier counts. In production: requested_at >= NOW() - INTERVAL 24 HOUR.
--    An index on requested_at lets the database skip old rows.
SELECT city_id,
       COUNT(*) AS completed_rides
FROM rides
WHERE status = 'completed'
  AND requested_at >= (SELECT MAX(requested_at) FROM rides) - INTERVAL 24 HOUR
GROUP BY city_id;

-- 4. Days since each rider's previous completed ride (first rides omitted).   [Set C]
--    One row per ride, so no GROUP BY; PARTITION BY lines rides up without collapsing them.
--    Order by requested_at, not ride_id. DATEDIFF counts calendar-day changes (22:00 -> 01:00 = 1);
--    TIMESTAMPDIFF(DAY, ...) counts full 24h periods (= 0).
WITH with_prev AS (
    SELECT rider_id,
           ride_id,
           requested_at,
           LAG(requested_at) OVER (PARTITION BY rider_id ORDER BY requested_at) AS prev_requested_at
    FROM rides
    WHERE status = 'completed'
)
SELECT rider_id,
       ride_id,
       DATEDIFF(requested_at, prev_requested_at) AS days_since_prev
FROM with_prev
WHERE prev_requested_at IS NOT NULL;

-- 5. Continuous ranges of IDs (gaps and islands).   [Set D: ride_logs]
--    Inside a run, log_id and ROW_NUMBER both go up by 1, so log_id - rn is constant; it jumps at a
--    gap. Group by that difference and take MIN/MAX. Breaks if IDs repeat (ask about uniqueness).
WITH numbered AS (
    SELECT log_id,
           ROW_NUMBER() OVER (ORDER BY log_id) AS rn
    FROM ride_logs
),
grouped AS (
    SELECT log_id, log_id - rn AS grp
    FROM numbered
)
SELECT MIN(log_id) AS start_id,
       MAX(log_id) AS end_id
FROM grouped
GROUP BY grp
ORDER BY start_id;

-- 6. Next-day retention by first-ride date (cohort self-join).   [Set D: ride_days]
--    LEFT JOIN keeps the whole cohort; put the next-day condition in ON, not WHERE.
--    COUNT(*) = cohort size; COUNT(d.rider_id) skips NULLs = returners.
--    Day-7: join on ride_date BETWEEN first_date + 1 AND first_date + 7 with COUNT(DISTINCT d.rider_id).
WITH first_day AS (
    SELECT rider_id, MIN(ride_date) AS first_date
    FROM ride_days
    GROUP BY rider_id
)
SELECT f.first_date AS cohort_date,
       COUNT(*) AS cohort_size,
       COUNT(d.rider_id) AS returned,
       ROUND(COUNT(d.rider_id) / COUNT(*), 2) AS retention
FROM first_day f
LEFT JOIN ride_days d
       ON d.rider_id = f.rider_id
      AND d.ride_date = DATE_ADD(f.first_date, INTERVAL 1 DAY)
GROUP BY f.first_date
ORDER BY f.first_date;
