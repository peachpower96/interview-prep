# Real-time supply/demand pipeline

Example company: **RideCo**, a ride-hailing marketplace (fictional).

## The question

"Pricing depends on supply and demand in each small area of a city. Design the system that computes a supply/demand signal for every area of every city, in near real time, and serves it to the pricing service. Drivers send location pings. Riders send app-open and ride-request events."

## 1. Requirements

Functional:

1. Ingest driver location pings and rider demand events.
2. Compute a supply/demand ratio per cell, every ~10 seconds.
3. Pricing can read the latest ratio for any cell.
4. Keep 2 years of history in a data lake.

Non-functional:

| Area | Target |
|---|---|
| Scale | ~305k events/s (250k driver pings + 55k rider events); 3× spikes in a few cells |
| Freshness | refreshed every ~10 s, never staler than 30 s |
| Read latency | under 10 ms, ~20k reads/s |
| Consistency | a few percent error is fine; duplicates removed; the ratio always has a value, even if stale |
| Availability | reads stay up even if the pipeline is down (serve the last value) |
| Fault tolerance | a crash must not lose counts; recover within about a minute |

Numbers behind the scale line: 1M active drivers at peak, one ping every 4 s → 250k pings/s; at ~100 B each that is ~25 MB/s.

## 2. Core entities

An entity is the data the system handles, not the people sending it: `DriverPing`, `RiderEvent`, `Cell`, `SupplyDemandRatio`. Driver and rider are actors.

## 3. API

- `POST /driver-pings` `{ event_id, driver_id, lat, lng, timestamp, status }`
- `POST /rider-events` `{ event_id, rider_id, lat, lng, timestamp, type }`
- `GET /ratios/{cell_id}` → `{ cell_id, supply, demand, ratio, window_end }`

Apps send new data, so POST. Pricing reads, so GET.

Stored value (Redis, key = `cell_id`, overwritten every 10 s): `WindowEnd` (datetime), `DriversAvailable` (int), `RiderEvents` (int), `Ratio` (float). 100,000 cells × ~50 B ≈ 5 MB, so it fits in memory easily.

## 4–5. Data flow and high-level design (one stage)

```
apps → load balancer → ingest service (adds cell ID) → Kafka (key = cell ID)
     → counting service (many workers) → Redis → pricing reads
                       Kafka also feeds → data-lake writer → object storage
```

- **Ingest service:** receives events, computes the cell ID, publishes to Kafka.
- **Kafka:** events sit in partitions; same key → same partition → same worker.
- **Counting service:** each worker reads some partitions and counts its cells in memory per 10-second window; when a window closes it writes each cell's ratio to Redis.
- **Redis:** latest ratio per cell, replicated, for fast reads.
- **Data lake:** every window's results (optionally raw events), for history and model training.
- **Spark Structured Streaming** is a natural implementation: the same DataFrame code as batch, reading from Kafka; `window("timestamp", "10 seconds")` is the window, `withWatermark` is the late-data rule, checkpoints save progress.

## 6. Deep dives

### Cells

A cell is a calculated postal code. A grid library (for example H3 hexagons) turns lat/lng into a cell ID: same input, same ID, on any machine. Nobody assigns or stores the list. Ingest and pricing use the same library at the same resolution, so they agree. City boundaries are small reference data loaded at startup, not read from a database per event.

The cell ID does two jobs: it is the unit of the answer (one ratio per cell) and the unit of work split (one cell → one partition → one worker).

### Why Kafka (four jobs)

1. Buffer: bursts wait instead of being dropped.
2. Routing: the key sends a cell's events to one worker.
3. Replay: events stay on disk for days, so a crashed worker rereads from where it stopped.
4. Many readers: counting workers and the lake writer read the same events independently.

### Why count in memory

A database would need ~305k writes/s (one node takes ~10k). RAM is far faster than a network round trip, and each worker's state is small. Count in memory and write only results: 100k rows every 10 s ≈ 10k writes/s.

Input is ~305k events/s; output is 100k rows per 10 s. Aggregation shrinks it ~30×, so serving is cheap. The risk is ingestion and grouping, which is why events are partitioned by cell ID.

### Windows, watermark, dedup

- **Windows:** fixed 10-second tumbling buckets `[0–10), [10–20), …`. A ping goes into the bucket its timestamp falls in. Tumbling (no overlap) counts each ping once and is cheapest for "right now".
- **Watermark:** a setting on the counting service, not a field on the ping. Each bucket waits a few extra seconds for late pings, then closes. A ping counts if it arrives before its bucket's end + watermark. Example: bucket 0–10 with watermark 5 is final at 15; a ping stamped 8 arriving at 13 counts, arriving at 17 does not.
- **Later than the watermark** (for example 3 minutes after a tunnel): skip the live count but still write it to the data lake so history stays complete.
- **Dedup:** supply is a set of distinct driver IDs per cell, so duplicate pings cannot add drivers. For rider events, skip any `event_id` already seen in the window; clear the set when the window closes.
- **Cell edge:** a driver may land in two cells in one window, a small error within tolerance. If it mattered, count each driver only at their latest ping.
- The 30 s is how stale a read may be; the watermark is a separate, smaller number.

### Hot cell (a concert ends)

With one stage, all of a cell's events go to one partition and one worker, which falls behind, so that cell goes stale exactly when pricing needs it.

Fix: split that cell's events across a few workers, have each count its share, then add the counts together (two-stage aggregation: count, then combine; like a Spark `groupBy` with a shuffle).

Trade-off: one stage is simpler and faster; two stages spread hot cells but add a hop, more parts, and wait on the slowest worker. Use two stages only for hot cells.

### Failures

- **Redis node dies:** a replica takes over. Even if Redis is lost entirely, the next window rewrites every cell within 10 s, and pricing uses its last value or "no surge" in the meantime. No database copy is needed for data this short-lived.
- **Counting worker crashes:** it restarts from its last checkpoint (saved counts + position in Kafka) and replays Kafka from there. Checkpointing the counts and the offset together is what prevents double counting.
- **Resilience terms to be able to say in one sentence each:** rate limiting at ingest, circuit breakers on downstream calls, graceful degradation (serve the last value), retries with backoff, dead-letter queue for events that cannot be parsed.

### Sentences worth having ready

- "You said refresh every 10 seconds, so I'll use 10-second tumbling windows."
- "This works functionally, but one service and Postgres cannot take 305k events/s. In the deep dive I'll add Kafka keyed by cell and split the counting across workers."
- "Redis serves the latest value and is the fallback during outages. Recovery comes from checkpoints and Kafka replay. The lake is for history, not recovery."

## Still to practice

- Deep dive: a counting worker crashes for 2 minutes. What does pricing see, and how do you recover without double counting?
- A one-minute wrap-up summary of the whole design.
