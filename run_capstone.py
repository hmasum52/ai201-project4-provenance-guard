#!/usr/bin/env python3
"""
Run the five capstone criteria (criteria.md, "Capstone criteria") three times.

    docker run -d --name pg -p 5000:5000 -v "${PWD}/logs:/app/logs" \
        -v "$env:USERPROFILE/.cache/huggingface:/root/.cache/huggingface" provenance-guard
    python run_capstone.py --label before

Criterion 3 restarts the container (`docker restart pg`) at the start of every
trial, so the model is unloaded when the junk arrives. Everything else is sent
to the live service. Output: results/capstone_run_<stamp>_<label>.md.
"""

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time

import requests

import config
import scenarios
import scoring

for _s in (sys.stdout, sys.stderr):
    _s.reconfigure(errors="replace")

URL = f"http://{config.HOST}:{config.PORT}"
CONTAINER = "pg"
BASELINE_RUN = config.RESULTS_DIR / "run_2026-11-11_0215_after.md"
BASELINE_ATTACKS = config.RESULTS_DIR / "attack_run_2026-11-11_0213_after.md"

JUNK = ["MF03", "MF04", "MF05", "MF06", "MF07"]
# Criterion 6: junk of 5+ words that repeats one or two words.
JUNK2 = [
    "asdf asdf asdf asdf asdf asdf asdf asdf", "buy now buy now buy now buy now buy now",
    "the the the the the the", "lol lol lol lol lol lol lol lol lol lol", "ok ok ok ok ok ok",
    "test test test test test test", "a b a b a b a b", "1 1 1 1 1 1 1 1",
    "12345 12345 12345 12345 12345", "no no no no no no no no",
]
PAIRS = [
    "The train was late again", "My brother lives in Leeds", "She bought bread and cheese",
    "They walked home in silence", "The kettle broke last week", "He forgot his keys again",
    "Our neighbour plays piano daily", "I finished the book yesterday",
    "The shop closes at six", "Rain fell all through Tuesday",
]


def post(body, **kw):
    t = time.perf_counter()
    r = requests.post(f"{URL}/submit", json=body, timeout=90, **kw)
    return r, round((time.perf_counter() - t) * 1000, 1)


def health():
    return requests.get(f"{URL}/health", timeout=10).json()


def combined(d):
    return round(scoring.combine_signals(d["model_score"], d["style_score"], d.get("phrase_score") or 0.0), 4)


def baseline_json_block(path, heading, trial=1):
    """The JSON list under '### heading' / '**Trial n**' in a unit 8 run log."""
    md = path.read_text(encoding="utf-8")
    start = md.index(f"### {heading}\n")
    start = md.index(f"**Trial {trial}**", start)
    start = md.index("```json\n", start) + len("```json\n")
    return json.loads(md[start:md.index("```", start)])


def baseline_ev08():
    md = BASELINE_ATTACKS.read_text(encoding="utf-8")
    start = md.index("### EV08") + 0
    start = md.index("```json\n", start) + len("```json\n")
    return json.loads(md[start:md.index("```", start)])


def restart_container():
    subprocess.run(["docker", "restart", CONTAINER], check=True, capture_output=True)
    for _ in range(60):
        try:
            return health()
        except requests.RequestException:
            time.sleep(1)
    raise RuntimeError("container did not come back")


def c1(n):
    rows = []
    for attack_id in JUNK:
        r, _ = post({"text": scenarios._attack(attack_id), "creator_id": f"cap_t{n}_c1_{attack_id}"})
        entry = requests.get(f"{URL}/log?limit=1", timeout=10).json()["entries"][0]
        ok = (r.status_code == 400 and entry.get("reason") == "not_enough_text"
              and "model_score" not in entry and "style_score" not in entry)
        rows.append({"id": attack_id, "status": r.status_code, "reason": entry.get("reason"),
                     "has_scores": "model_score" in entry or "style_score" in entry, "ok": ok})
    return rows


def c6(n):
    rows = []
    for i, text in enumerate(JUNK2):
        r, _ = post({"text": text, "creator_id": f"cap_t{n}_c6_{i}"})
        entry = requests.get(f"{URL}/log?limit=1", timeout=10).json()["entries"][0]
        d = r.json() if r.status_code == 200 else {}
        ok = (r.status_code == 400 and entry.get("reason") == "low_variety_text"
              and "model_score" not in entry and "style_score" not in entry)
        rows.append({"text": text, "status": r.status_code, "reason": entry.get("reason"),
                     "guess": d.get("guess"), "confidence": d.get("confidence"), "ok": ok})
    return rows


def c2(n, base):
    rows, texts = [], scenarios.OWN_WRITING + scenarios.SCENARIOS[3]["texts"] + [scenarios._attack("EV08")]
    for i, (text, ref) in enumerate(zip(texts, base)):
        r, _ = post({"text": text, "creator_id": f"cap_t{n}_c2_{i}"})
        d = r.json() if r.status_code == 200 else {}
        got = combined(d) if d else None
        rows.append({"i": i, "status": r.status_code, "combined": got, "baseline": ref,
                     "ok": r.status_code == 200 and got == ref})
    return rows


def c3(n):
    h0 = restart_container()
    rows = []
    for attack_id in JUNK:
        r, ms = post({"text": scenarios._attack(attack_id), "creator_id": f"cap_t{n}_c3_{attack_id}"})
        rows.append({"id": attack_id, "status": r.status_code, "wall_ms": ms, "ok": ms < 500})
    h1 = health()
    return {"loaded_before": h0["detector_loaded"], "loaded_after": h1["detector_loaded"],
            "rows": rows,
            "ok": not h0["detector_loaded"] and not h1["detector_loaded"] and all(x["ok"] for x in rows)}


def c4(n):
    before = health()["log_entries"]
    sent = []
    for i, text in enumerate(scenarios.OWN_WRITING):
        sent.append(post({"text": text, "creator_id": f"cap_t{n}_c4_s{i}"})[0])
    for attack_id in JUNK:
        sent.append(post({"text": scenarios._attack(attack_id), "creator_id": f"cap_t{n}_c4_{attack_id}"})[0])
    bad = [{"creator_id": f"cap_t{n}_c4_nt"}, {"text": "", "creator_id": f"cap_t{n}_c4_empty"},
           {"text": "x" * 20000, "creator_id": f"cap_t{n}_c4_huge"}, ["text", "creator_id"],
           {"text": "A perfectly fine sentence with enough words."}]
    for body in bad:
        sent.append(post(body)[0])
    growth = health()["log_entries"] - before
    tail = requests.get(f"{URL}/log?limit=20", timeout=10).json()["entries"]
    fields = ("timestamp", "input", "outcome", "duration_ms")
    missing = [(k, e.get("creator_id")) for e in tail for k in fields if e.get(k) is None]
    return {"requests": len(sent), "statuses": [r.status_code for r in sent], "log_growth": growth,
            "missing_fields": missing, "ok": len(sent) == 20 and growth == 20 and not missing}


def c5(n):
    rows = []
    for i, sentence in enumerate(PAIRS):
        four = " ".join(sentence.split()[:4])
        r4, _ = post({"text": four, "creator_id": f"cap_t{n}_c5_{i}_4"})
        r5, _ = post({"text": sentence, "creator_id": f"cap_t{n}_c5_{i}_5"})
        rows.append({"five": sentence, "status_4_words": r4.status_code, "status_5_words": r5.status_code,
                     "ok": r4.status_code == 400 and r5.status_code == 200})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="")
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--only6", action="store_true", help="run just criterion 6 (no restart)")
    args = ap.parse_args()

    if args.only6:
        stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
        path = config.RESULTS_DIR / f"capstone_run_{stamp}_{args.label or 'c6'}_c6only.md"
        out = ["# Capstone criterion 6 only" + (f" - {args.label}" if args.label else ""), "",
               "- Produced by: `run_capstone.py::c6` against the container", "",
               "| Criterion | " + " | ".join(f"Run {i}" for i in range(1, args.trials + 1)) + " |",
               "|---|" + "---|" * args.trials]
        trials = [c6(n) for n in range(1, args.trials + 1)]
        out.append("| 6 | " + " | ".join(f'{sum(x["ok"] for x in t)}/10 {"ok" if all(x["ok"] for x in t) else "FAIL"}' for t in trials) + " |")
        for n, t in enumerate(trials, 1):
            out += ["", f"### Trial {n} - c6", "", "```json", json.dumps(t, indent=1, ensure_ascii=False), "```"]
        path.write_text("\n".join(out), encoding="utf-8")
        print("\n".join(out[:8]))
        print("wrote", path.relative_to(config.ROOT))
        return

    own = baseline_json_block(BASELINE_RUN, "own writing")
    cov = baseline_json_block(BASELINE_RUN, "coverage")
    ev08 = baseline_ev08()
    base = [combined(d) for d in own + cov] + [round(scoring.combine_signals(ev08["model_score"], ev08["style_score"], 0.0), 4)]
    assert len(base) == 31 and abs(max(ev08["confidence"], 1 - base[-1]) - ev08["confidence"]) < 1e-3
    print(f"baseline: {len(base)} combined scores (30 from {BASELINE_RUN.name}, EV08 from {BASELINE_ATTACKS.name})")

    trials = []
    for n in range(1, args.trials + 1):
        res = {"c3": c3(n)}          # first: needs a freshly started container
        res["c1"], res["c2"], res["c4"], res["c5"], res["c6"] = c1(n), c2(n, base), c4(n), c5(n), c6(n)
        passed = {
            1: all(x["ok"] for x in res["c1"]), 2: all(x["ok"] for x in res["c2"]),
            3: res["c3"]["ok"], 4: res["c4"]["ok"], 5: all(x["ok"] for x in res["c5"]),
            6: all(x["ok"] for x in res["c6"]),
        }
        counts = {
            1: f'{sum(x["ok"] for x in res["c1"])}/5', 2: f'{sum(x["ok"] for x in res["c2"])}/31',
            3: f'{sum(x["ok"] for x in res["c3"]["rows"])}/5', 4: f'{res["c4"]["log_growth"]}/20 logged',
            5: f'{sum(x["ok"] for x in res["c5"]) * 2}/20', 6: f'{sum(x["ok"] for x in res["c6"])}/10',
        }
        trials.append({"res": res, "passed": passed, "counts": counts})
        print(f"trial {n}:", {k: f"{counts[k]} {'ok' if passed[k] else 'FAIL'}" for k in passed})

    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = config.RESULTS_DIR / f"capstone_run_{stamp}{'_' + args.label if args.label else ''}.md"
    lines = [f"# Capstone run log{' - ' + args.label if args.label else ''}", "",
             "- Produced by: `run_capstone.py::main` against the container (`app.py::submit`)",
             f"- {args.trials} trials per criterion, {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
             "| Criterion | " + " | ".join(f"Run {i}" for i in range(1, args.trials + 1)) + " |",
             "|---|" + "---|" * args.trials]
    for k in range(1, 7):
        lines.append(f"| {k} | " + " | ".join(f'{t["counts"][k]} {"ok" if t["passed"][k] else "FAIL"}' for t in trials) + " |")
    lines += ["", "---", "", "## What actually came back", ""]
    for n, t in enumerate(trials, 1):
        for k in ("c1", "c2", "c3", "c4", "c5", "c6"):
            lines += [f"### Trial {n} - {k}", "", "```json", json.dumps(t["res"][k], indent=1), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", path.relative_to(config.ROOT))


if __name__ == "__main__":
    main()
