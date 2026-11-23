"""
Capstone smoke check for the minimum-evidence guard on POST /submit.

    python check_guard.py

Runs against a temporary audit log (the committed logs/audit.jsonl is not
touched) and fails loudly if the guard or the new log fields break.
"""

import csv
import pathlib
import sys
import tempfile

import config

tmp = pathlib.Path(tempfile.mkdtemp())
config.LOG_DIR, config.AUDIT_LOG = tmp, tmp / "audit.jsonl"

import app  # noqa: E402  (after config is pointed at the temp log)
import audit  # noqa: E402
import detector  # noqa: E402

client = app.app.test_client()
attacks = {
    r["id"]: r["text"]
    for r in csv.DictReader(
        open(config.ROOT / "attack_set/attack_set/attacks.csv", encoding="utf-8", newline="")
    )
}


def submit(text, creator):
    return client.post("/submit", json={"text": text, "creator_id": creator})


# 1. Junk is refused with a 400, and the model never loads.
for attack_id in ("MF03", "MF04", "MF05", "MF06", "MF07"):
    r = submit(attacks[attack_id], f"check_{attack_id}")
    assert r.status_code == 400, (attack_id, r.status_code)
assert detector._model is None, "guard ran after the model loaded"

# 2. The boundary: 4 words refused, 5 words scored.
assert submit("one two three four", "check_b4").status_code == 400
assert submit("one two three four five", "check_b5").status_code == 200

# 3. Every request left one complete record.
entries = audit.read_entries()
assert len(entries) == 7, len(entries)
for e in entries:
    for field in ("timestamp", "input", "outcome", "duration_ms"):
        assert e.get(field) is not None, (field, e)
assert [e["reason"] for e in entries[:5]] == ["not_enough_text"] * 5
assert entries[-1]["outcome"] == "scored"

# 4. A run that errors (model unavailable) returns 503 and still leaves a record.
real_signal = detector.model_signal


def unavailable(_text):
    raise detector.DetectorUnavailable("model not downloaded")


detector.model_signal = unavailable
try:
    assert submit("one two three four five six", "check_503").status_code == 503
finally:
    detector.model_signal = real_signal
failed = audit.read_entries()[-1]
assert failed["reason"] == "detector_unavailable" and failed["outcome"] == "failed", failed
assert failed["duration_ms"] is not None and failed["input"], failed

print("check_guard: all checks passed")
sys.exit(0)
