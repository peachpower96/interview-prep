-- Dialect: MySQL 8. Table shapes: see schemas.sql.
-- Pattern thread: a join is a dictionary lookup; LEFT JOIN + IS NULL finds what is missing;
-- watch fan-out (one-to-many joins multiply rows, inflating SUM and COUNT).

-- 1. Completed rides per city, by name.   [Set B]
--    cities has one row per city_id, so the join adds a column without adding rows.
--    A plain JOIN drops cities with no rides.
SELECT c.city_name,
       COUNT(*) AS completed_rides
FROM rides r
JOIN cities c ON c.city_id = r.city_id
WHERE r.status = 'completed'
GROUP BY c.city_name;

-- 2. Drivers with no completed rides (anti-join).   [Set B]
--    Filter to completed rides BEFORE the join; otherwise a driver whose only ride was cancelled
--    still matches and disappears. "= NULL" never works; use IS NULL.
WITH completed AS (
    SELECT ride_id, driver_id
    FROM rides
    WHERE status = 'completed'
)
SELECT d.driver_id
FROM drivers d
LEFT JOIN completed c ON c.driver_id = d.driver_id
WHERE c.ride_id IS NULL;

-- 3. Drivers who signed up in 2026: per city, how many completed rides there and total fare.   [Set B]
--    After the joins there is still one row per ride, so COUNT(DISTINCT driver_id) counts drivers
--    while SUM(fare) correctly adds every ride. Filter early and join on indexed keys.
SELECT c.city_name,
       COUNT(DISTINCT r.driver_id) AS new_drivers,
       SUM(r.fare_usd) AS total_fare_usd
FROM rides r
JOIN drivers d ON d.driver_id = r.driver_id
JOIN cities  c ON c.city_id   = r.city_id
WHERE r.status = 'completed'
  AND d.signup_date >= '2026-01-01'
GROUP BY c.city_name;

-- 4. Texas drivers with at least one completed ride of $30 or more.   [Set C]
--    "or more" is >= 30. Never group by name alone (two drivers can share a name); use driver_id.
--    WHERE EXISTS (...) avoids duplicate rows altogether and is a good optimization to mention.
SELECT DISTINCT d.driver_id, d.name
FROM drivers d
JOIN rides r ON r.driver_id = d.driver_id
WHERE d.state = 'TX'
  AND r.status = 'completed'
  AND r.price_usd >= 30;
