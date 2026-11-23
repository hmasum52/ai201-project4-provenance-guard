#!/usr/bin/env python3
"""
Capstone stretch: what changes at ten times the normal rate?

    docker run -d --name pg -p 5000:5000 -v "${PWD}/logs:/app/logs" \
        -v "$env:USERPROFILE/.cache/huggingface:/root/.cache/huggingface" provenance-guard
    python load_observation.py

"Normal" is 10 requests a minute (declared in the README before this ran). Phases:

    normal         10/min for 60 s, spread over 40 creator_ids
    10x            100/min for 120 s, spread over 40 creator_ids
    10x, one user  100/min for 60 s from a single creator_id (the rate limiter)

Requests are sent on a fixed schedule whether or not earlier ones have finished
(open loop), so a slow service cannot quietly slow the load down.
"""

import csv
import datetime as dt
import statistics
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

import config

URL = f"http://{config.HOST}:{config.PORT}"
CONTAINER = "pg"
ids = ["FP02", "FP03", "FP04", "FP05", "FP06", "FP07", "FP08", "EV01", "EV02", "EV03"]
rows = {r["id"]: r["text"] for r in csv.DictReader(
    open(config.ROOT / "attack_set/attack_set/attacks.csv", encoding="utf-8", newline=""))}
TEXTS = [rows[i] for i in ids]


def one(creator, text):
    t = time.perf_counter()
    try:
        r = requests.post(f"{URL}/submit", json={"text": text, "creator_id": creator}, timeout=120)
        return r.status_code, (time.perf_counter() - t) * 1000
    except requests.RequestException as exc:
        return type(exc).__name__, (time.perf_counter() - t) * 1000


def phase(name, per_minute, seconds, creators):
    n = int(per_minute * seconds / 60)
    gap = 60 / per_minute
    start = time.perf_counter()
    futures = []
    with ThreadPoolExecutor(max_workers=200) as pool:
        for i in range(n):
            delay = start + i * gap - time.perf_counter()
            if delay > 0:
                time.sleep(delay)
            futures.append(pool.submit(one, f"{creators}_{i % (40 if creators != 'load_single' else 1)}",
                                       TEXTS[i % len(TEXTS)]))
        results = [f.result() for f in futures]
    wall = time.perf_counter() - start
    return {"name": name, "per_minute": per_minute, "sent": n, "results": results, "wall_s": wall}


def hwm_mb():
    out = subprocess.run(["docker", "exec", CONTAINER, "sh", "-c", "grep VmHWM /proc/1/status"],
                         capture_output=True, text=True).stdout.split()
    return round(int(out[1]) / 1024) if len(out) > 1 else None


def summarise(p):
    ok = [ms for code, ms in p["results"] if code == 200]
    codes = {}
    for code, _ in p["results"]:
        codes[str(code)] = codes.get(str(code), 0) + 1
    q = (lambda xs: statistics.quantiles(xs, n=20, method="inclusive")[18]) if len(ok) >= 2 else (lambda xs: xs[0] if xs else float("nan"))
    return {
        "phase": p["name"], "rate_per_min": p["per_minute"], "sent": p["sent"], "codes": codes,
        "median_ms": round(statistics.median(ok), 1) if ok else None,
        "p95_ms": round(q(ok), 1) if ok else None,
        "max_ms": round(max(ok), 1) if ok else None,
        "done_per_min": round(len(ok) / (p["wall_s"] / 60), 1),
    }


def main():
    try:
        requests.get(f"{URL}/health", timeout=5)
    except requests.RequestException:
        sys.exit("Nothing answering. Start the container first (see the docstring).")

    one("load_warm", TEXTS[0])          # loads the model; not part of any phase
    log0 = requests.get(f"{URL}/health").json()["log_entries"]
    mem0 = hwm_mb()
    phases = [
        phase("normal (10/min)", 10, 60, "load_a"),
        phase("10x (100/min), 40 creators", 100, 120, "load_b"),
        phase("10x (100/min), one creator", 100, 60, "load_single"),
    ]
    time.sleep(2)
    log1 = requests.get(f"{URL}/health").json()["log_entries"]
    mem1 = hwm_mb()
    sent = sum(p["sent"] for p in phases)

    summ = [summarise(p) for p in phases]
    lines = ["| Phase | Sent | Status codes | Median ms | p95 ms | Worst ms | Completed (200) per min |",
             "|---|---|---|---|---|---|---|"]
    for s in summ:
        lines.append(f"| {s['phase']} | {s['sent']} | {s['codes']} | {s['median_ms']} | {s['p95_ms']} | "
                     f"{s['max_ms']} | {s['done_per_min']} |")
    lines += ["", f"- Requests sent: {sent}. Log entries added: {log1 - log0}.",
              f"- Peak memory of the service (VmHWM): {mem0} MB before the phases, {mem1} MB after."]
    out = "\n".join([f"# Load observation", "",
                     f"- Produced by: `load_observation.py`, {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}", ""] + lines) + "\n"
    config.RESULTS_DIR.mkdir(exist_ok=True)
    path = config.RESULTS_DIR / f"load_observation_{dt.datetime.now().strftime('%Y-%m-%d_%H%M')}.md"
    path.write_text(out, encoding="utf-8")
    print(out)
    print("wrote", path.relative_to(config.ROOT))


if __name__ == "__main__":
    main()
