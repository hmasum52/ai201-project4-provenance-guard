#!/usr/bin/env python3
"""
Capstone stretch: where does the time go in one scored POST /submit?

    docker run --rm -v "${PWD}/logs:/app/logs:ro" \
        -v "$env:USERPROFILE/.cache/huggingface:/root/.cache/huggingface" \
        provenance-guard python latency_breakdown.py

Each stage function the route calls is wrapped with a timer, then 30 requests
go through the real route (Flask's test client, so no HTTP). The audit log is
a temporary COPY of logs/audit.jsonl, so the real log is never written to but
the verified-human lookup still reads a log of realistic size.
"""

import csv
import datetime as dt
import pathlib
import shutil
import statistics
import sys
import tempfile
import time

import config

real_log = config.AUDIT_LOG
tmp = pathlib.Path(tempfile.mkdtemp())
config.LOG_DIR, config.AUDIT_LOG = tmp, tmp / "audit.jsonl"
if real_log.exists():
    shutil.copy(real_log, config.AUDIT_LOG)
log_lines = len(config.AUDIT_LOG.read_text(encoding="utf-8").splitlines()) if config.AUDIT_LOG.exists() else 0

import app  # noqa: E402
import audit  # noqa: E402
import detector  # noqa: E402
import phrases  # noqa: E402
import scoring  # noqa: E402
import stylometry  # noqa: E402

samples = {}


def timed(module, name, label):
    fn = getattr(module, name)

    def wrapper(*a, **kw):
        t = time.perf_counter()
        try:
            return fn(*a, **kw)
        finally:
            samples.setdefault(label, []).append((time.perf_counter() - t) * 1000)

    setattr(module, name, wrapper)


timed(detector, "model_signal", "model signal (gpt2)")
timed(stylometry, "style_signal", "style signal")
timed(phrases, "phrase_signal", "phrase signal")
timed(scoring, "combine_signals", "combine")
timed(scoring, "score_to_label", "label")
timed(audit, "is_verified", "verified-human lookup (reads the log)")
timed(audit, "log_decision", "log write")

ids = ["FP02", "FP03", "FP04", "FP05", "FP06", "FP07", "FP08", "EV01", "EV02", "EV03"]
rows = {r["id"]: r["text"] for r in csv.DictReader(
    open(config.ROOT / "attack_set/attack_set/attacks.csv", encoding="utf-8", newline=""))}
texts = [rows[i] for i in ids]
client = app.app.test_client()

# Warm-up: loads the model, and is not counted.
client.post("/submit", json={"text": texts[0], "creator_id": "lb_warm"})
samples.clear()

totals, guards = [], []
for n in range(30):
    text = texts[n % len(texts)]
    t = time.perf_counter()
    r = client.post("/submit", json={"text": text, "creator_id": f"lb_{n}"})
    totals.append((time.perf_counter() - t) * 1000)
    assert r.status_code == 200, r.status_code
    # the two guards in app.py::submit, timed on their own (they run inline)
    t = time.perf_counter()
    len(stylometry.words(text)) < config.MIN_WORDS
    len(set(stylometry.words(text))) < config.MIN_DISTINCT_WORDS
    guards.append((time.perf_counter() - t) * 1000)

stages = dict(samples)
stages["guards (word count, distinct words)"] = guards
summed = [sum(stages[k][i] for k in stages) for i in range(30)]
stages["route overhead (JSON in/out, rest)"] = [max(totals[i] - summed[i], 0.0) for i in range(30)]


def p95(xs):
    return statistics.quantiles(xs, n=20, method="inclusive")[18]


rows_out = []
mean_total = statistics.mean(totals)
for name, xs in sorted(stages.items(), key=lambda kv: -statistics.mean(kv[1])):
    rows_out.append((name, statistics.mean(xs), statistics.median(xs), p95(xs), 100 * statistics.mean(xs) / mean_total))

lines = [
    f"| Stage | Mean ms | Median ms | p95 ms | Share of route |",
    "|---|---|---|---|---|",
] + [f"| {n} | {m:.2f} | {md:.2f} | {p:.2f} | {s:.1f}% |" for n, m, md, p, s in rows_out] + [
    f"| **whole route** | **{mean_total:.2f}** | **{statistics.median(totals):.2f}** | **{p95(totals):.2f}** | 100% |",
]
header = [
    f"# Latency breakdown",
    "",
    f"- Produced by: `latency_breakdown.py`, {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
    f"- 30 warm requests (10 texts x 3 passes) through `app.py::submit`, one fresh creator_id each",
    f"- Audit log copy had {log_lines} lines when the run started",
    "",
]
out = "\n".join(header + lines) + "\n"
config.RESULTS_DIR.mkdir(exist_ok=True)
path = config.RESULTS_DIR / f"latency_breakdown_{dt.datetime.now().strftime('%Y-%m-%d_%H%M')}.md"
path.write_text(out, encoding="utf-8")
print(out)
print("wrote", path.relative_to(config.ROOT))
sys.exit(0)
