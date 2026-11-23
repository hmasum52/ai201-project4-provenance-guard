# Latency breakdown

- Produced by: `latency_breakdown.py`, 2026-11-23 06:58
- 30 warm requests (10 texts x 3 passes) through `app.py::submit`, one fresh creator_id each
- Audit log copy had 1115 lines when the run started

| Stage | Mean ms | Median ms | p95 ms | Share of route |
|---|---|---|---|---|
| model signal (gpt2) | 126.70 | 120.70 | 182.42 | 92.0% |
| verified-human lookup (reads the log) | 8.69 | 8.55 | 11.82 | 6.3% |
| route overhead (JSON in/out, rest) | 1.69 | 1.68 | 2.00 | 1.2% |
| style signal | 0.29 | 0.29 | 0.38 | 0.2% |
| log write | 0.24 | 0.23 | 0.32 | 0.2% |
| guards (word count, distinct words) | 0.06 | 0.06 | 0.11 | 0.0% |
| phrase signal | 0.05 | 0.04 | 0.09 | 0.0% |
| combine | 0.01 | 0.00 | 0.01 | 0.0% |
| label | 0.00 | 0.00 | 0.00 | 0.0% |
| **whole route** | **137.73** | **132.19** | **192.70** | 100% |
