# Load observation

- Produced by: `load_observation.py`, 2026-11-23 02:02

| Phase | Sent | Status codes | Median ms | p95 ms | Worst ms | Completed (200) per min |
|---|---|---|---|---|---|---|
| normal (10/min) | 10 | {'200': 10} | 174.4 | 227.9 | 236.8 | 11.1 |
| 10x (100/min), 40 creators | 200 | {'200': 200} | 174.9 | 238.6 | 327.1 | 100.3 |
| 10x (100/min), one creator | 100 | {'200': 5, '429': 95} | 164.4 | 196.2 | 202.6 | 5.0 |

- Requests sent: 310. Log entries added: 310.
- Peak memory of the service (VmHWM): 959 MB before the phases, 1019 MB after.
