-- Dialect: MySQL 8. Table shapes: see schemas.sql (Set C).
-- Pattern thread: WHERE filters rows before grouping, HAVING filters groups after; timestamps use
-- half-open ranges; two different groupings need two steps.

-- 1. Completed rides by California drivers in Q2 2026 priced $20-$40 (list, so no GROUP BY).
--    BETWEEN is safe on prices (both ends included) but not on timestamps, which is why the dates
--    use >= and <. Filter on state, not name (two drivers can share a name).
SELECT r.ride_id, d.name, r.price_usd
FROM rides r
JOIN drivers d ON d.driver_id = r.driver_id
WHERE d.state = 'CA'
  AND r.status = 'completed'
  AND r.price_usd BETWEEN 20 AND 40
  AND r.requested_at >= '2026-04-01'
  AND r.requested_at <  '2026-07-01';

-- 2. "VIP" riders in the last 6 months of data: at least 2 completed rides AND at least $80 spent.
--    Run order: FROM, WHERE (rows), GROUP BY (piles), HAVING (piles), SELECT.
--    Aggregates cannot go in WHERE. Both conditions must hold: AND, not OR.
SELECT rider_id,
       COUNT(*)       AS completed_rides,
       SUM(price_usd) AS total_spent
FROM rides
WHERE status = 'completed'
  AND requested_at >= (SELECT MAX(requested_at) FROM rides) - INTERVAL 6 MONTH
GROUP BY rider_id
HAVING COUNT(*) >= 2
   AND SUM(price_usd) >= 80;

-- 3. Monthly average rating for "trusted" drivers (3+ reviews in total).
--    Two groupings: total reviews per driver (who is trusted) and reviews per driver per month
--    (the average). Putting HAVING COUNT(*) >= 3 in the monthly query would check 3 per month.
--    A review at 23:00 Jan 31 and one at 01:00 Feb 1 land in different months.
WITH trusted AS (
    SELECT driver_id
    FROM reviews
    GROUP BY driver_id
    HAVING COUNT(*) >= 3
)
SELECT r.driver_id,
       DATE_FORMAT(r.submitted_at, '%Y-%m-01') AS month,
       ROUND(AVG(r.stars), 2)                  AS avg_stars
FROM reviews r
JOIN trusted t ON t.driver_id = r.driver_id
GROUP BY r.driver_id, DATE_FORMAT(r.submitted_at, '%Y-%m-01');
