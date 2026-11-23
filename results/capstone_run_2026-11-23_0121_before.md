# Capstone run log - before

- Produced by: `run_capstone.py::main` against the container (`app.py::submit`)
- 3 trials per criterion, 2026-11-23 01:21

| Criterion | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| 1 | 5/5 ok | 5/5 ok | 5/5 ok |
| 2 | 31/31 ok | 31/31 ok | 31/31 ok |
| 3 | 5/5 ok | 5/5 ok | 5/5 ok |
| 4 | 20/20 logged ok | 20/20 logged ok | 20/20 logged ok |
| 5 | 20/20 ok | 20/20 ok | 20/20 ok |

---

## What actually came back

### Trial 1 - c1

```json
[
 {
  "id": "MF03",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 },
 {
  "id": "MF04",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 },
 {
  "id": "MF05",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 },
 {
  "id": "MF06",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 },
 {
  "id": "MF07",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 }
]
```

### Trial 1 - c2

```json
[
 {
  "i": 0,
  "status": 200,
  "combined": 0.584,
  "baseline": 0.584,
  "ok": true
 },
 {
  "i": 1,
  "status": 200,
  "combined": 0.6657,
  "baseline": 0.6657,
  "ok": true
 },
 {
  "i": 2,
  "status": 200,
  "combined": 0.6026,
  "baseline": 0.6026,
  "ok": true
 },
 {
  "i": 3,
  "status": 200,
  "combined": 0.2898,
  "baseline": 0.2898,
  "ok": true
 },
 {
  "i": 4,
  "status": 200,
  "combined": 0.4947,
  "baseline": 0.4947,
  "ok": true
 },
 {
  "i": 5,
  "status": 200,
  "combined": 0.3804,
  "baseline": 0.3804,
  "ok": true
 },
 {
  "i": 6,
  "status": 200,
  "combined": 0.5134,
  "baseline": 0.5134,
  "ok": true
 },
 {
  "i": 7,
  "status": 200,
  "combined": 0.6804,
  "baseline": 0.6804,
  "ok": true
 },
 {
  "i": 8,
  "status": 200,
  "combined": 0.3473,
  "baseline": 0.3473,
  "ok": true
 },
 {
  "i": 9,
  "status": 200,
  "combined": 0.4056,
  "baseline": 0.4056,
  "ok": true
 },
 {
  "i": 10,
  "status": 200,
  "combined": 0.7977,
  "baseline": 0.7977,
  "ok": true
 },
 {
  "i": 11,
  "status": 200,
  "combined": 0.6973,
  "baseline": 0.6973,
  "ok": true
 },
 {
  "i": 12,
  "status": 200,
  "combined": 0.5995,
  "baseline": 0.5995,
  "ok": true
 },
 {
  "i": 13,
  "status": 200,
  "combined": 0.7158,
  "baseline": 0.7158,
  "ok": true
 },
 {
  "i": 14,
  "status": 200,
  "combined": 0.6433,
  "baseline": 0.6433,
  "ok": true
 },
 {
  "i": 15,
  "status": 200,
  "combined": 0.5838,
  "baseline": 0.5838,
  "ok": true
 },
 {
  "i": 16,
  "status": 200,
  "combined": 0.3117,
  "baseline": 0.3117,
  "ok": true
 },
 {
  "i": 17,
  "status": 200,
  "combined": 0.4098,
  "baseline": 0.4098,
  "ok": true
 },
 {
  "i": 18,
  "status": 200,
  "combined": 0.1866,
  "baseline": 0.1866,
  "ok": true
 },
 {
  "i": 19,
  "status": 200,
  "combined": 0.3441,
  "baseline": 0.3441,
  "ok": true
 },
 {
  "i": 20,
  "status": 200,
  "combined": 0.3106,
  "baseline": 0.3106,
  "ok": true
 },
 {
  "i": 21,
  "status": 200,
  "combined": 0.5645,
  "baseline": 0.5645,
  "ok": true
 },
 {
  "i": 22,
  "status": 200,
  "combined": 0.5743,
  "baseline": 0.5743,
  "ok": true
 },
 {
  "i": 23,
  "status": 200,
  "combined": 0.7029,
  "baseline": 0.7029,
  "ok": true
 },
 {
  "i": 24,
  "status": 200,
  "combined": 0.7345,
  "baseline": 0.7345,
  "ok": true
 },
 {
  "i": 25,
  "status": 200,
  "combined": 0.7526,
  "baseline": 0.7526,
  "ok": true
 },
 {
  "i": 26,
  "status": 200,
  "combined": 0.3776,
  "baseline": 0.3776,
  "ok": true
 },
 {
  "i": 27,
  "status": 200,
  "combined": 0.5483,
  "baseline": 0.5483,
  "ok": true
 },
 {
  "i": 28,
  "status": 200,
  "combined": 0.5196,
  "baseline": 0.5196,
  "ok": true
 },
 {
  "i": 29,
  "status": 200,
  "combined": 0.2769,
  "baseline": 0.2769,
  "ok": true
 },
 {
  "i": 30,
  "status": 200,
  "combined": 0.3599,
  "baseline": 0.3599,
  "ok": true
 }
]
```

### Trial 1 - c3

```json
{
 "loaded_before": false,
 "loaded_after": false,
 "rows": [
  {
   "id": "MF03",
   "status": 400,
   "wall_ms": 11.5,
   "ok": true
  },
  {
   "id": "MF04",
   "status": 400,
   "wall_ms": 21.0,
   "ok": true
  },
  {
   "id": "MF05",
   "status": 400,
   "wall_ms": 18.9,
   "ok": true
  },
  {
   "id": "MF06",
   "status": 400,
   "wall_ms": 23.7,
   "ok": true
  },
  {
   "id": "MF07",
   "status": 400,
   "wall_ms": 18.2,
   "ok": true
  }
 ],
 "ok": true
}
```

### Trial 1 - c4

```json
{
 "requests": 20,
 "statuses": [
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  400,
  400,
  400,
  400,
  400,
  400,
  400,
  400,
  400,
  400
 ],
 "log_growth": 20,
 "missing_fields": [],
 "ok": true
}
```

### Trial 1 - c5

```json
[
 {
  "five": "The train was late again",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "My brother lives in Leeds",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "She bought bread and cheese",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "They walked home in silence",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "The kettle broke last week",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "He forgot his keys again",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "Our neighbour plays piano daily",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "I finished the book yesterday",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "The shop closes at six",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "Rain fell all through Tuesday",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 }
]
```

### Trial 2 - c1

```json
[
 {
  "id": "MF03",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 },
 {
  "id": "MF04",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 },
 {
  "id": "MF05",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 },
 {
  "id": "MF06",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 },
 {
  "id": "MF07",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 }
]
```

### Trial 2 - c2

```json
[
 {
  "i": 0,
  "status": 200,
  "combined": 0.584,
  "baseline": 0.584,
  "ok": true
 },
 {
  "i": 1,
  "status": 200,
  "combined": 0.6657,
  "baseline": 0.6657,
  "ok": true
 },
 {
  "i": 2,
  "status": 200,
  "combined": 0.6026,
  "baseline": 0.6026,
  "ok": true
 },
 {
  "i": 3,
  "status": 200,
  "combined": 0.2898,
  "baseline": 0.2898,
  "ok": true
 },
 {
  "i": 4,
  "status": 200,
  "combined": 0.4947,
  "baseline": 0.4947,
  "ok": true
 },
 {
  "i": 5,
  "status": 200,
  "combined": 0.3804,
  "baseline": 0.3804,
  "ok": true
 },
 {
  "i": 6,
  "status": 200,
  "combined": 0.5134,
  "baseline": 0.5134,
  "ok": true
 },
 {
  "i": 7,
  "status": 200,
  "combined": 0.6804,
  "baseline": 0.6804,
  "ok": true
 },
 {
  "i": 8,
  "status": 200,
  "combined": 0.3473,
  "baseline": 0.3473,
  "ok": true
 },
 {
  "i": 9,
  "status": 200,
  "combined": 0.4056,
  "baseline": 0.4056,
  "ok": true
 },
 {
  "i": 10,
  "status": 200,
  "combined": 0.7977,
  "baseline": 0.7977,
  "ok": true
 },
 {
  "i": 11,
  "status": 200,
  "combined": 0.6973,
  "baseline": 0.6973,
  "ok": true
 },
 {
  "i": 12,
  "status": 200,
  "combined": 0.5995,
  "baseline": 0.5995,
  "ok": true
 },
 {
  "i": 13,
  "status": 200,
  "combined": 0.7158,
  "baseline": 0.7158,
  "ok": true
 },
 {
  "i": 14,
  "status": 200,
  "combined": 0.6433,
  "baseline": 0.6433,
  "ok": true
 },
 {
  "i": 15,
  "status": 200,
  "combined": 0.5838,
  "baseline": 0.5838,
  "ok": true
 },
 {
  "i": 16,
  "status": 200,
  "combined": 0.3117,
  "baseline": 0.3117,
  "ok": true
 },
 {
  "i": 17,
  "status": 200,
  "combined": 0.4098,
  "baseline": 0.4098,
  "ok": true
 },
 {
  "i": 18,
  "status": 200,
  "combined": 0.1866,
  "baseline": 0.1866,
  "ok": true
 },
 {
  "i": 19,
  "status": 200,
  "combined": 0.3441,
  "baseline": 0.3441,
  "ok": true
 },
 {
  "i": 20,
  "status": 200,
  "combined": 0.3106,
  "baseline": 0.3106,
  "ok": true
 },
 {
  "i": 21,
  "status": 200,
  "combined": 0.5645,
  "baseline": 0.5645,
  "ok": true
 },
 {
  "i": 22,
  "status": 200,
  "combined": 0.5743,
  "baseline": 0.5743,
  "ok": true
 },
 {
  "i": 23,
  "status": 200,
  "combined": 0.7029,
  "baseline": 0.7029,
  "ok": true
 },
 {
  "i": 24,
  "status": 200,
  "combined": 0.7345,
  "baseline": 0.7345,
  "ok": true
 },
 {
  "i": 25,
  "status": 200,
  "combined": 0.7526,
  "baseline": 0.7526,
  "ok": true
 },
 {
  "i": 26,
  "status": 200,
  "combined": 0.3776,
  "baseline": 0.3776,
  "ok": true
 },
 {
  "i": 27,
  "status": 200,
  "combined": 0.5483,
  "baseline": 0.5483,
  "ok": true
 },
 {
  "i": 28,
  "status": 200,
  "combined": 0.5196,
  "baseline": 0.5196,
  "ok": true
 },
 {
  "i": 29,
  "status": 200,
  "combined": 0.2769,
  "baseline": 0.2769,
  "ok": true
 },
 {
  "i": 30,
  "status": 200,
  "combined": 0.3599,
  "baseline": 0.3599,
  "ok": true
 }
]
```

### Trial 2 - c3

```json
{
 "loaded_before": false,
 "loaded_after": false,
 "rows": [
  {
   "id": "MF03",
   "status": 400,
   "wall_ms": 27.9,
   "ok": true
  },
  {
   "id": "MF04",
   "status": 400,
   "wall_ms": 30.9,
   "ok": true
  },
  {
   "id": "MF05",
   "status": 400,
   "wall_ms": 25.8,
   "ok": true
  },
  {
   "id": "MF06",
   "status": 400,
   "wall_ms": 24.4,
   "ok": true
  },
  {
   "id": "MF07",
   "status": 400,
   "wall_ms": 18.4,
   "ok": true
  }
 ],
 "ok": true
}
```

### Trial 2 - c4

```json
{
 "requests": 20,
 "statuses": [
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  400,
  400,
  400,
  400,
  400,
  400,
  400,
  400,
  400,
  400
 ],
 "log_growth": 20,
 "missing_fields": [],
 "ok": true
}
```

### Trial 2 - c5

```json
[
 {
  "five": "The train was late again",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "My brother lives in Leeds",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "She bought bread and cheese",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "They walked home in silence",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "The kettle broke last week",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "He forgot his keys again",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "Our neighbour plays piano daily",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "I finished the book yesterday",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "The shop closes at six",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "Rain fell all through Tuesday",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 }
]
```

### Trial 3 - c1

```json
[
 {
  "id": "MF03",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 },
 {
  "id": "MF04",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 },
 {
  "id": "MF05",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 },
 {
  "id": "MF06",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 },
 {
  "id": "MF07",
  "status": 400,
  "reason": "not_enough_text",
  "has_scores": false,
  "ok": true
 }
]
```

### Trial 3 - c2

```json
[
 {
  "i": 0,
  "status": 200,
  "combined": 0.584,
  "baseline": 0.584,
  "ok": true
 },
 {
  "i": 1,
  "status": 200,
  "combined": 0.6657,
  "baseline": 0.6657,
  "ok": true
 },
 {
  "i": 2,
  "status": 200,
  "combined": 0.6026,
  "baseline": 0.6026,
  "ok": true
 },
 {
  "i": 3,
  "status": 200,
  "combined": 0.2898,
  "baseline": 0.2898,
  "ok": true
 },
 {
  "i": 4,
  "status": 200,
  "combined": 0.4947,
  "baseline": 0.4947,
  "ok": true
 },
 {
  "i": 5,
  "status": 200,
  "combined": 0.3804,
  "baseline": 0.3804,
  "ok": true
 },
 {
  "i": 6,
  "status": 200,
  "combined": 0.5134,
  "baseline": 0.5134,
  "ok": true
 },
 {
  "i": 7,
  "status": 200,
  "combined": 0.6804,
  "baseline": 0.6804,
  "ok": true
 },
 {
  "i": 8,
  "status": 200,
  "combined": 0.3473,
  "baseline": 0.3473,
  "ok": true
 },
 {
  "i": 9,
  "status": 200,
  "combined": 0.4056,
  "baseline": 0.4056,
  "ok": true
 },
 {
  "i": 10,
  "status": 200,
  "combined": 0.7977,
  "baseline": 0.7977,
  "ok": true
 },
 {
  "i": 11,
  "status": 200,
  "combined": 0.6973,
  "baseline": 0.6973,
  "ok": true
 },
 {
  "i": 12,
  "status": 200,
  "combined": 0.5995,
  "baseline": 0.5995,
  "ok": true
 },
 {
  "i": 13,
  "status": 200,
  "combined": 0.7158,
  "baseline": 0.7158,
  "ok": true
 },
 {
  "i": 14,
  "status": 200,
  "combined": 0.6433,
  "baseline": 0.6433,
  "ok": true
 },
 {
  "i": 15,
  "status": 200,
  "combined": 0.5838,
  "baseline": 0.5838,
  "ok": true
 },
 {
  "i": 16,
  "status": 200,
  "combined": 0.3117,
  "baseline": 0.3117,
  "ok": true
 },
 {
  "i": 17,
  "status": 200,
  "combined": 0.4098,
  "baseline": 0.4098,
  "ok": true
 },
 {
  "i": 18,
  "status": 200,
  "combined": 0.1866,
  "baseline": 0.1866,
  "ok": true
 },
 {
  "i": 19,
  "status": 200,
  "combined": 0.3441,
  "baseline": 0.3441,
  "ok": true
 },
 {
  "i": 20,
  "status": 200,
  "combined": 0.3106,
  "baseline": 0.3106,
  "ok": true
 },
 {
  "i": 21,
  "status": 200,
  "combined": 0.5645,
  "baseline": 0.5645,
  "ok": true
 },
 {
  "i": 22,
  "status": 200,
  "combined": 0.5743,
  "baseline": 0.5743,
  "ok": true
 },
 {
  "i": 23,
  "status": 200,
  "combined": 0.7029,
  "baseline": 0.7029,
  "ok": true
 },
 {
  "i": 24,
  "status": 200,
  "combined": 0.7345,
  "baseline": 0.7345,
  "ok": true
 },
 {
  "i": 25,
  "status": 200,
  "combined": 0.7526,
  "baseline": 0.7526,
  "ok": true
 },
 {
  "i": 26,
  "status": 200,
  "combined": 0.3776,
  "baseline": 0.3776,
  "ok": true
 },
 {
  "i": 27,
  "status": 200,
  "combined": 0.5483,
  "baseline": 0.5483,
  "ok": true
 },
 {
  "i": 28,
  "status": 200,
  "combined": 0.5196,
  "baseline": 0.5196,
  "ok": true
 },
 {
  "i": 29,
  "status": 200,
  "combined": 0.2769,
  "baseline": 0.2769,
  "ok": true
 },
 {
  "i": 30,
  "status": 200,
  "combined": 0.3599,
  "baseline": 0.3599,
  "ok": true
 }
]
```

### Trial 3 - c3

```json
{
 "loaded_before": false,
 "loaded_after": false,
 "rows": [
  {
   "id": "MF03",
   "status": 400,
   "wall_ms": 13.7,
   "ok": true
  },
  {
   "id": "MF04",
   "status": 400,
   "wall_ms": 26.2,
   "ok": true
  },
  {
   "id": "MF05",
   "status": 400,
   "wall_ms": 19.6,
   "ok": true
  },
  {
   "id": "MF06",
   "status": 400,
   "wall_ms": 29.7,
   "ok": true
  },
  {
   "id": "MF07",
   "status": 400,
   "wall_ms": 27.5,
   "ok": true
  }
 ],
 "ok": true
}
```

### Trial 3 - c4

```json
{
 "requests": 20,
 "statuses": [
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  400,
  400,
  400,
  400,
  400,
  400,
  400,
  400,
  400,
  400
 ],
 "log_growth": 20,
 "missing_fields": [],
 "ok": true
}
```

### Trial 3 - c5

```json
[
 {
  "five": "The train was late again",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "My brother lives in Leeds",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "She bought bread and cheese",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "They walked home in silence",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "The kettle broke last week",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "He forgot his keys again",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "Our neighbour plays piano daily",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "I finished the book yesterday",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "The shop closes at six",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 },
 {
  "five": "Rain fell all through Tuesday",
  "status_4_words": 400,
  "status_5_words": 200,
  "ok": true
 }
]
```
