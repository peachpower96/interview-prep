-- Dialect: MySQL 8. Table shapes: see schemas.sql (Set A).
-- Pattern thread: dedupe -> one value per group -> group twice -> compare to previous row.

-- 1. One row per rider per day with a completed ride (dedupe with DISTINCT).
--    DISTINCT applies to the whole row; convert the timestamp to a date FIRST so 08:15 and 18:30
--    on the same day collapse to one row.
SELECT DISTINCT
       rider_id,
       DATE(requested_at) AS ride_date
FROM rides
WHERE status = 'completed';

-- 2. Each rider's first completed ride date (one value per group).
--    WHERE runs before grouping, so cancelled rides never reach MIN.
SELECT rider_id,
       MIN(DATE(requested_at)) AS first_ride_date
FROM rides
WHERE status = 'completed'
GROUP BY rider_id;

-- 3. New riders per day (group twice: build one row per rider in a CTE, then group that by date).
WITH first_rides AS (
    SELECT rider_id,
           MIN(DATE(requested_at)) AS first_ride_date
    FROM rides
    WHERE status = 'completed'
    GROUP BY rider_id
)
SELECT first_ride_date AS ride_date,
       COUNT(*) AS new_riders
FROM first_rides
GROUP BY first_ride_date
ORDER BY first_ride_date;

-- 4. Riders who also rode the previous calendar day, per day (LAG).
--    Dedupe first, or two rides on one day make LAG compare a day with itself.
--    Compare against DATE_SUB(ride_date, INTERVAL 1 DAY), not day numbers (month boundaries).
--    SUM(CASE ...) keeps days whose count is 0; a WHERE filter would drop them.
WITH rider_days AS (
    SELECT DISTINCT rider_id,
           DATE(requested_at) AS ride_date
    FROM rides
    WHERE status = 'completed'
),
with_prev AS (
    SELECT rider_id,
           ride_date,
           LAG(ride_date) OVER (PARTITION BY rider_id ORDER BY ride_date) AS prev_date
    FROM rider_days
)
SELECT ride_date,
       SUM(CASE WHEN prev_date = DATE_SUB(ride_date, INTERVAL 1 DAY)
                THEN 1 ELSE 0 END) AS consecutive_day_riders
FROM with_prev
GROUP BY ride_date
ORDER BY ride_date;

-- 5. New riders AND consecutive-day riders per day, in one pass.
--    MIN(...) OVER labels every row with the rider's first date without collapsing rows.
--    The alternative (join query 3 onto query 4) needs LEFT JOIN + COALESCE(new_riders, 0)
--    to keep zero days; say that trade-off out loud.
WITH rider_days AS (
    SELECT DISTINCT rider_id,
           DATE(requested_at) AS ride_date
    FROM rides
    WHERE status = 'completed'
),
labeled AS (
    SELECT rider_id,
           ride_date,
           MIN(ride_date) OVER (PARTITION BY rider_id) AS first_date,
           LAG(ride_date) OVER (PARTITION BY rider_id ORDER BY ride_date) AS prev_date
    FROM rider_days
)
SELECT ride_date,
       SUM(CASE WHEN ride_date = first_date THEN 1 ELSE 0 END) AS new_riders,
       SUM(CASE WHEN prev_date = DATE_SUB(ride_date, INTERVAL 1 DAY)
                THEN 1 ELSE 0 END) AS consecutive_day_riders
FROM labeled
GROUP BY ride_date
ORDER BY ride_date;
