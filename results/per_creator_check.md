# Per-creator limit check

- Produced by: scratch script `per_creator.py` against `app.py::submit` (limiter key: `app.py::rate_limit_key`)
- Limits: 5 per minute, 50 per day, one address (127.0.0.1) · 2026-11-11 02:25
- A fresh server was started first, and a minute passed between observations.

## 1. Per-creator isolation (same address)

```
alice x6: 200 200 200 200 200 429
bob x1, straight after: 200
```

## 2. One script rotating creator_ids

```
12 different ids, one request each: 200 200 200 200 200 200 200 200 200 200 200 200
```

## 3. No usable creator_id (address fallback)

```
6 requests, field missing: 400 400 400 400 400 429
```
