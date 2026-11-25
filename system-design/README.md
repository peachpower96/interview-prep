# System design

Write-ups follow the delivery framework: requirements → core entities → API → data flow → high-level design → deep dives.

| Step | Minutes (of ~50 in a 60-minute round) | What you produce |
|---|---|---|
| 1. Requirements | 5 | About 3 functional, 3–5 non-functional (quantified) |
| 2. Core entities | 2 | The nouns the system handles (data, not the people who send it) |
| 3. API | 5 | Endpoints and event fields |
| 4. Data flow | 3–5 | Numbered steps for one event, input to output; each step becomes a box |
| 5. High-level design | 10–15 | The simplest design that meets the functional requirements |
| 6. Deep dives | 15–20 | Harden it against the non-functional requirements; at senior level, raise the problems yourself |

Estimate numbers only where a number changes a decision ("one database cannot take 305k writes/s, so...").

## Designs

- [realtime-supply-demand-pipeline](realtime-supply-demand-pipeline/README.md): streaming pipeline that turns location pings and demand events into a per-area ratio served at low latency.
