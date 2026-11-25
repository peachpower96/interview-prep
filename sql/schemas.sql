-- Table shapes assumed by the queries in this folder (MySQL 8 style, columns only).
-- Data is not included; create a few rows yourself to try a query, including edge cases
-- (midnight boundaries, cancelled rows, ties, users with no rows).

-- Set A: event-style rides
-- rides(ride_id, rider_id, driver_id, requested_at, status)          -- 01_basics_dedupe_grouping.sql

-- Set B: rides + drivers + cities
-- rides(ride_id, driver_id, rider_id, city_id, requested_at, completed_at, status, fare_usd)
-- drivers(driver_id, city_id, signup_date)
-- cities(city_id, city_name)
-- daily_rides(city_id, ride_date, completed_rides)

-- Set C: drivers, rides, reviews, bonuses
-- drivers(driver_id, name, state, signup_date)
-- rides(ride_id, driver_id, rider_id, requested_at, status, price_usd)   -- cancelled rides keep their quoted price
-- reviews(review_id, driver_id, submitted_at, stars)
-- bonuses(bonus_id, driver_id, bonus_date, amount_usd)

-- Set D: single-purpose tables
-- driver_tenure(driver_id, start_date, end_date, yearly_salary)    -- end_date IS NULL while still active
-- ride_logs(log_id)                                                -- unique IDs, not in order
-- users(id, name); trips(id, user_id, distance)
-- rider_profiles(profile_id, email, updated_at)                    -- duplicate emails
-- ride_days(rider_id, ride_date)                                   -- one row per rider per day ridden
