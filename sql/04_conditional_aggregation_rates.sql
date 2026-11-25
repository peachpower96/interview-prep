-- Dialect: MySQL 8. Table shapes: see schemas.sql.
-- Pattern thread: SUM(CASE WHEN ... THEN 1 ELSE 0 END) turns a condition into a count;
-- COUNT(col) skips NULLs while COUNT(*) does not; use 100.0 * ... so division is decimal everywhere.

-- 1. Cancellation rate per city.   [Set B]
--    No WHERE: the total needs every ride. Divide by zero cannot happen (a city only appears
--    if it has at least one ride). For zero-ride cities, start from cities and LEFT JOIN rides.
SELECT city_id,
       COUNT(*) AS total_rides,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_rides,
       ROUND(100.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*), 1) AS cancel_rate_pct
FROM rides
GROUP BY city_id;

-- 2. Each driver's average fare vs their city's average (two averages at two levels).   [Set B]
--    The city average must be over rides, not an average of driver averages (which weights every
--    driver equally). Group the driver average by city too: a driver can work in two cities.
--    Window alternative: AVG(fare_usd) OVER (PARTITION BY city_id) on completed rides.
WITH completed AS (
    SELECT driver_id, city_id, fare_usd
    FROM rides
    WHERE status = 'completed'
),
driver_avg AS (
    SELECT driver_id, city_id, AVG(fare_usd) AS avg_fare
    FROM completed
    GROUP BY driver_id, city_id
),
city_avg AS (
    SELECT city_id, AVG(fare_usd) AS city_avg_fare
    FROM completed
    GROUP BY city_id
)
SELECT d.driver_id,
       d.city_id,
       ROUND(d.avg_fare, 2)      AS avg_fare,
       ROUND(c.city_avg_fare, 2) AS city_avg_fare
FROM driver_avg d
JOIN city_avg c ON c.city_id = d.city_id;

-- 3. Rides per price band for every state that has a driver.   [Set C]
--    "Every state" => start FROM drivers and LEFT JOIN rides, with the status condition in ON.
--    A WHERE on rides after a LEFT JOIN turns it back into an inner join and states whose drivers
--    have no completed rides vanish. Bands must not overlap or leave gaps: < 20, 20..40, > 40.
SELECT d.state,
       SUM(CASE WHEN r.price_usd < 20 THEN 1 ELSE 0 END)              AS low_rides,
       SUM(CASE WHEN r.price_usd BETWEEN 20 AND 40 THEN 1 ELSE 0 END) AS mid_rides,
       SUM(CASE WHEN r.price_usd > 40 THEN 1 ELSE 0 END)              AS high_rides
FROM drivers d
LEFT JOIN rides r
       ON r.driver_id = d.driver_id
      AND r.status = 'completed'
GROUP BY d.state;

-- 4. Churn rate: share of drivers with a recorded end date.   [Set D]
--    COUNT(end_date) skips NULLs; COUNT(*) does not. Do NOT filter with WHERE end_date IS NOT NULL:
--    that shrinks the denominator too and the answer becomes 1.
SELECT COUNT(end_date) / COUNT(*) AS churn_rate
FROM driver_tenure;

-- 5. Ride earnings and bonus total per driver, labelled by bonus share.   [Set C]
--    Aggregate each table in its own CTE BEFORE joining, or a driver with 2 rides and 2 bonuses
--    gets 4 rows and every total doubles (fan-out). LEFT JOIN from drivers keeps drivers with no
--    rides or bonuses; COALESCE(x, 0) stops NULL from making the comparison silently false.
WITH earnings AS (
    SELECT driver_id, SUM(price_usd) AS ride_earnings
    FROM rides
    WHERE status = 'completed'
      AND requested_at >= '2026-02-01'
      AND requested_at <  '2026-11-01'
    GROUP BY driver_id
),
bonus AS (
    SELECT driver_id, SUM(amount_usd) AS bonus_total
    FROM bonuses
    WHERE bonus_date >= '2026-02-01'
      AND bonus_date <  '2026-11-01'
    GROUP BY driver_id
)
SELECT d.driver_id,
       COALESCE(e.ride_earnings, 0) AS ride_earnings,
       COALESCE(b.bonus_total, 0)   AS bonus_total,
       CASE WHEN COALESCE(b.bonus_total, 0) > 0.5 * COALESCE(e.ride_earnings, 0)
            THEN 'bonus-heavy' ELSE 'standard' END AS label
FROM drivers d
LEFT JOIN earnings e ON e.driver_id = d.driver_id
LEFT JOIN bonus    b ON b.driver_id = d.driver_id;
