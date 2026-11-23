# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. **The route (`POST /submit`)** receives `{text, creator_id}`, rejects missing, empty, too-short or enormous text with a 400, and assigns a `content_id`.
2. **The rate limiter** (unit 8) sits in front of the route and turns excess requests into a 429, which is also logged.
3. **Signal one (`detector.model_signal`)** runs gpt2 on the text and adds `model_score`, a 0–1 predictability score.
4. **Signal two (`stylometry.style_signal`)** measures sentence-length spread, vocabulary repetition and punctuation, and adds `style_score`.
5. **The combining rule (`scoring.combine_signals`)** merges the two scores into one `combined_score`.
6. **The label mapping (`scoring.score_to_label`)** turns that score into a guess (`human`, `unsure` or `ai`) and the sentence a reader sees.
7. **The audit log (`audit.log_decision`)** records all of it, then the response goes back. A later `POST /appeal` moves the item to `under_review`.



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** how predictable the text is to a local language model (gpt2), as perplexity squashed onto 0–1.

**Why that might differ between human and AI writing:** a model writes by picking likely next words, so its text is easy for another model to predict. Human writing has odder word choices and more surprises.

**What it can't see:** who wrote it. It rewards common words in short, ordinary sentences, so plain human writing (a second-language writer, a younger writer, anyone writing simply on purpose) scores as AI. Ornate prose full of rare words scores as human, whoever wrote it.

### Signal two — the style signal

**What it measures:** the shape of the text: how much sentence length varies, how much vocabulary repeats, and how much punctuation there is.

**Why that might differ between human and AI writing:** generated prose leans toward even, mid-length sentences and a narrower vocabulary. Human writing is lumpier, with a three-word sentence beside a forty-word one.

**What it can't see:** meaning. It cannot read, so anything that changes the shape without changing the substance moves it: added typos, broken-up sentences, a pasted quotation. Type-token ratio also falls as text gets longer, so text length alone can look like a signal.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** a weighted average that leans on the model signal, with a safety valve. If the two signals disagree by a lot, the result is pulled halfway back toward 0.5 ("unsure"), so a split between signals never turns into an accusation.

**The numbers:** `combined = 0.6 × model_score + 0.4 × style_score`. If `|model_score − style_score| > 0.4`, then `combined = 0.5 + (combined − 0.5) / 2`. Weights and the 0.4 gap are in `config.py` (`WEIGHT_MODEL_SIGNAL`, `WEIGHT_STYLE_SIGNAL`, `DISAGREEMENT_GAP`). The style signal averages three measures with equal weight: sentence-length spread, type-token ratio and punctuation density, each flipped so higher means more AI.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

A lightly-edited AI paragraph ("Honestly, it's pretty important to note that good communication matters a lot in any company. Also, teams do better when people share ideas openly, so you should try it. ... Anyway, that's my take."). The model signal still suspects AI (`model_score` 0.567), but the casual short sentences and added commas fool the style signal (`style_score` 0.149). The plain average would be 0.400; because the signals are 0.418 apart, the rule pulls it halfway toward 0.5 and returns `combined_score` 0.450. That lands in "unsure" rather than being called human. Four test inputs, direct scores:

| Input | model | style | combined |
|---|---|---|---|
| clearly AI | 0.761 | 0.459 | 0.640 |
| clearly human | 0.419 | 0.179 | 0.323 |
| formal human | 0.297 | 0.153 | 0.239 |
| lightly-edited AI | 0.567 | 0.149 | 0.450 |

The clearly-AI and clearly-human texts sit 0.32 apart. "Clearly AI" scored 0.640, just under my first AI threshold of 0.65, so that label was unreachable on it. In Milestone 5 I lowered `AI_THRESHOLD` to 0.60 (in `config.py`). The cost: a few more borderline texts, including plain human writing, will now cross into the AI label. The unsure band shrank from 0.35–0.65 to 0.35–0.60, so I'm trading some protection for writers for a reachable AI label. (Unit 8, Milestone 5 later raised `AI_THRESHOLD` to 0.75, so the table below shows 0.35-0.75 and 0.75-1.00; see The Improvement.)



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. |
| unsure | 0.35 – 0.75 | We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look. |
| high-confidence AI | 0.75 – 1.00 | This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it. |

**Why I worded the "unsure" one this way:** It says "we can't tell" rather than "this might be AI", so the system admits its own limit instead of putting suspicion on the writer. It never says "you". It ends with a next step, the appeal, because the person reading it may have written every word themselves. The AI label keeps the appeal pointer for the same reason.

All three labels are reachable. Real submissions produced human (0.323), unsure (0.450) and AI (0.640).



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Honestly, it's pretty important to note that good communication matters a lot in any company. Also, teams do better when people share ideas openly, so you should try it. Modern tools help too, and they make work go faster, mostly. Anyway, that's my take.", "creator_id": "demo-writer"}'
```

```json
{
    "confidence": 0.5502,
    "content_id": "01a9ea4b-225b-4bff-a58e-a50dbeee8294",
    "guess": "unsure",
    "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
    "model_score": 0.5668,
    "style_score": 0.1486
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "01a9ea4b-225b-4bff-a58e-a50dbeee8294", "reasoning": "I wrote this myself; it is just how I talk when I write casually."}'
```

```json
{
    "content_id": "01a9ea4b-225b-4bff-a58e-a50dbeee8294",
    "message": "Thanks. Your appeal is recorded and a person will review it.",
    "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
    "count": 2,
    "entries": [
        {
            "combined_score": 0.4498,
            "content_id": "01a9ea4b-225b-4bff-a58e-a50dbeee8294",
            "creator_id": "demo-writer",
            "guess": "unsure",
            "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
            "model_score": 0.5668,
            "status": "decided",
            "style_score": 0.1486,
            "timestamp": "2026-11-04T06:46:30+00:00"
        },
        {
            "content_id": "01a9ea4b-225b-4bff-a58e-a50dbeee8294",
            "creator_id": "demo-writer",
            "event": "appeal",
            "reasoning": "I wrote this myself; it is just how I talk when I write casually.",
            "status": "under_review",
            "timestamp": "2026-11-04T06:46:30+00:00"
        }
    ]
}
```

---

## How I Used AI

**Moment 1: the combining rule (plan, analysis, then implementation)**

- *What I asked for:* A plan for Milestone 4 before any code, with questions first. We settled the rule on paper: all three style measures, then `0.6 × model + 0.4 × style`, pulled halfway toward 0.5 whenever the two signals differ by more than 0.4, so a split reads "unsure" instead of an accusation.
- *What came back:* The implementation, and an analysis on four inputs with both signals printed: clearly AI 0.640, clearly human 0.323, formal human 0.239, lightly-edited AI 0.450. The edited-AI text was the split case (model 0.567, style 0.149) and the rule pulled it to "unsure" as planned.
- *What I changed:* The analysis showed "clearly AI" sitting just under my 0.65 AI threshold, so that label was unreachable on it. In Milestone 5 I lowered `AI_THRESHOLD` to 0.60 and wrote down the cost in the README: a few more plain human writers can now cross into the AI label.

**Moment 2: the verified-human path (plan, analysis, then implementation)**

- *What I asked for:* A plan for a stretch feature where a writer earns a credential through an extra step. It asked how the credential should be earned, and I chose a writing challenge scored by my own pipeline.
- *What came back:* A `POST /verify` endpoint. Testing it was the analysis: a short sample was rejected (400), an AI-style sample failed, and my first plain human paragraph also failed (combined 0.443, "unsure"). A more distinctive human paragraph passed (0.157).
- *What I changed:* Nothing in the threshold. I kept the strict bar and kept the failed attempt in the write-up, because it is the same weakness as the false positive: plain writers are the least likely to verify. I also wrote down the limits (unauthenticated `creator_id`, untimed challenge, AI text that scores human would pass).

**Unit 8**

For all of the implementation in this unit I planned it with Claude first. I reviewed each plan, sent it back when it wasn't what I wanted, and only then asked Claude to implement and test it. The decisions were mine (which fix to make, what to leave alone, what counts as held or broke), and every number in this README comes from a real run, not an estimate. Where Claude wrote test material, the README says so.

---

## Stretch Features

Declared before building. I'm adding all three:

1. **`GET /content/<id>`**: returns one item's current status, label and whether it was appealed.
2. **A third signal**: a stock-phrase signal (`phrases.py`) that counts filler phrases AI text leans on ("it is important to note", "furthermore"). It can only push a score toward AI, never toward human, because a missing phrase proves nothing. Weighting note below.
3. **A verified-human path**: `POST /verify`. A writer answers a prompt with a writing sample; if it scores human they earn a credential that shows as `verified_human` on their work. It does not override the label.

### How I weighted the three signals

`combined = 0.6 × model + 0.4 × style` (with the disagreement pull toward 0.5 from before), then `+ 0.15 × phrase_score`, capped at 1.0 (`config.WEIGHT_PHRASE`, in `scoring.py::combine_signals`). The phrase signal is added on top rather than averaged in because a text with no stock phrases proves nothing, so it must never drag an AI text toward human.

Effect on the four test inputs (combined, before → after): clearly AI 0.640 → 0.790, clearly human 0.323 → 0.323, formal human 0.239 → 0.239, lightly-edited AI 0.450 → 0.450. The AI/human gap grew from 0.32 to 0.47. The edited AI text didn't move: casual rewriting stripped every stock phrase, which is this signal's blind spot (a word list is easy to avoid). The risk runs the other way too: a formal human writer who says "furthermore" gets nudged toward AI.

### `GET /content/<id>`

Reads the audit log and returns `content_id`, `creator_id`, `guess`, `label`, `combined_score`, `status` (`decided` or `under_review`), `appealed` and `verified_human`. An unknown id returns 404.

### Verified-human path

`GET /verify` returns the prompt and the 60-word minimum. `POST /verify` with `{creator_id, sample}` scores the sample through the same pipeline; only a "human" result (combined score 0.35 or below) earns the credential, which lives in the audit log as a `verified` event. `/submit` and `/content/<id>` then show `verified_human: true`. It does not change the label: a verified writer scored as AI still sees the AI label and can appeal.

What happened in my run: the 60-word minimum rejected a short sample (400); an AI-style sample failed; my first plain human paragraph also **failed** (combined 0.443, "unsure"), and a second, more idiosyncratic one passed (0.157). I did not loosen the bar to make the first one pass. That failure is the same weakness as the false positive: plain, predictable writers are the least likely to verify.

Limits: `creator_id` is unauthenticated, so anyone could claim another writer's id; the challenge isn't timed; and AI text that happens to score human would pass.

```json
{"creator_id": "writer-a", "verified": true, "message": "You're verified. Your work will show a verified-human mark."}
```

```json
{
    "appealed": false,
    "combined_score": 0.7665,
    "content_id": "af29d99b-43e2-4958-a851-76c356c02c91",
    "creator_id": "writer-a",
    "guess": "ai",
    "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
    "status": "decided",
    "verified_human": true
}
```

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Unit 8 Stretch Features

Declared before building:

- **Doing: per-creator limits, with a note on what that changes.** Written up under Rate Limiting below, with a real run to back it. The limiter already counts per `creator_id`, so this adds evidence and a note, not code.
- **Not doing: three attacks against someone else's system.** There is no other system available to attack.
- **Not doing: a second improvement.** Unit 8 allows only the limiter, the log and one improvement to change, and a second change would muddy the single before/after in The Improvement, so the system stays exactly as that milestone left it.

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day (on `/submit`, `config.py`)

**Why those numbers and not others:** A real writer submits their own work a few times an hour, and might send a quick burst of revisions of one piece, so 5 a minute never gets in their way and 50 a day is far more than most writers produce. A script mapping my thresholds needs hundreds of variations, and scoring takes only 1-2 seconds, so with no limit it could send about 30 a minute. At 5 a minute and 50 a day it gets at most 50 probes per key per day, which is too few to map the 0.35 and 0.60 thresholds quickly. I did not go lower (3 a minute, 20 a day) because a writer revising a long essay several times could be locked out, and that is a real person being punished for the defense.

**What a caller counts as:** the `creator_id` in the request body, falling back to the IP address when there is none (`rate_limit_key` in `app.py`). The weakness: a script can rotate `creator_id` to get a fresh allowance every time, so this limits honest callers better than determined ones. Counting per IP would stop that but would lump a whole household or school together.

**Per-creator limits: what that changes (stretch).** The key is `creator_id` when the request has one, and the address only when it doesn't (`rate_limit_key` in `app.py`). So this was already per-creator; I checked what that does with a real run (`results/per_creator_check.md`, one address, 5 per minute):

```
creator alice, 6 requests:                    200 200 200 200 200 429
creator bob, same address, straight after:    200
one script rotating 12 different creator_ids: 200 200 200 200 200 200 200 200 200 200 200 200
6 requests with no creator_id:                400 400 400 400 400 429
```

- **What it changes for the better.** Alice using up her allowance did not touch Bob, who sent from the same address and got a 200. A per-address limit would have answered Bob with a 429, so one noisy writer would lock out everyone sharing a household, school or office connection.
- **What it costs.** `creator_id` is whatever the caller says it is, nothing checks it. The script that rotated twelve ids from one address was never limited once, so a determined attacker gets a fresh allowance by inventing ids, and the 50-a-day cap is no cap at all for them. Per-creator limiting protects honest writers better than it stops a script.
- **The fallback.** A request with no usable `creator_id` is counted against the address instead. Six of them from one address gave five 400s and then a 429, which is why RQ10 and RQ11 were rate limited in the attack runs without ever reaching the route.
- **What I didn't do.** A generous per-address ceiling on top (say 30 a minute) would close the rotation gap, and it is the obvious next step. I did not add it, because this unit allows only the limiter, the log and one improvement to change, so the code is exactly as Milestone 5 left it.

**The run of status codes when I pushed past it:**

`python run_attacks.py --flood 15` (saved as `results/flood_2026-11-11_0140.md`):

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

All ten rejections appear in `GET /log` as `event: rejected, reason: rate_limited, limit: "5 per 1 minute"`.

---

## Attack Run — Before

Run with `python run_attacks.py --set attack_set/attack_set --label before` (full output in `results/attack_run_2026-11-11_0151_before.md`), rate limiting on at 5/min and 50/day, thresholds 0.35 / 0.60. Nothing was fixed before this run. All 56 attacks parsed and none crashed the service (no 5xx).

**Result: 36 held, 20 broke, out of 56.** (Corrected in Milestone 4: I first wrote 31 and 25, but the rows below sum to 2+2+5+3+12+12 = 36 held and 8+6+1+5 = 20 broke.)

| Family | Attacks | Held | Broke | What happened |
|---|---|---|---|---|
| evasion | 10 | 2 | 8 | Only EV07 and EV10 were called `ai`. EV01 (typos) and EV05 (heavy human edit) passed as `human`. EV02, 03, 04, 06, 08, 09 landed in `unsure`. I count AI text escaping to `human` or `unsure` as broke. |
| false_positive | 8 | 2 | 6 | FP02-FP07 were called `ai`. FP01 and FP08 were `unsure`, which I count as held (nobody was accused). |
| prompt_injection | 6 | 5 | 1 | PI02 ("SYSTEM: ... return guess=human") came back `human` at 0.226. The other five stayed `unsure`. There is no LLM reading the text to obey it, so PI02 worked because the odd prefix lowered the perplexity signal, not because it followed the instruction. |
| malformed (text) | 8 | 3 | 5 | MF01, MF02, MF08 got a clean 400. MF03-MF07 (control characters, punctuation only, one long word, emoji, right-to-left script) got a 200 and a score; MF05-MF07 were called `ai` at 0.87-0.99, which is a wrong verdict on input that isn't writing. |
| malformed (request) | 12 | 12 | 0 | Every one got a 400, no crash. RQ10 and RQ11 first came back 429 because requests with no usable `creator_id` share one per-IP bucket; they never reached the route. After the window reset I re-sent both and each got a clean 400 (`results/attack_run_2026-11-11_0152_rerun.md`). |
| flood_same_creator | 12 | 12 | 0 | `200 200 200 200 200 429 429 429 429 429 429 429`, and the rejections are in the log. |

**Ten audit log entries from the run**

Chosen for the failures: two wrongly accused writers, two evasions that passed, an injection that worked, junk input called AI with 99% confidence, plus a 429 and a 400 rejection (rejections carry fewer fields, as expected).

```json
{"timestamp": "2026-11-11T06:51:03+00:00", "content_id": "64a15474-a2ea-4756-ad81-ac5ffecebdfd", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6285, "combined_score": 0.7345, "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.", "status": "decided", "phrase_score": 0.0}
{"timestamp": "2026-11-11T06:51:03+00:00", "content_id": "f1df1488-c80a-49c0-813d-2819522a4685", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.8329, "style_score": 0.5202, "combined_score": 0.7813, "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.", "status": "decided", "phrase_score": 0.4902}
{"timestamp": "2026-11-11T06:51:04+00:00", "content_id": "314ced19-9cfb-4a14-895e-38b80dddfdf0", "creator_id": "attacker_FP07", "guess": "ai", "model_score": 0.8816, "style_score": 0.5529, "combined_score": 0.7501, "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.", "status": "decided", "phrase_score": 0.0}
{"timestamp": "2026-11-11T06:50:59+00:00", "content_id": "8df67285-4c0d-47b7-8425-0edea22d8e8c", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.5313, "combined_score": 0.3106, "label": "We think this was probably written by a person.", "status": "decided", "phrase_score": 0.0}
{"timestamp": "2026-11-11T06:51:01+00:00", "content_id": "964cc2fd-32f9-441b-819f-d3f86560138c", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.2974, "combined_score": 0.3117, "label": "We think this was probably written by a person.", "status": "decided", "phrase_score": 0.0}
{"timestamp": "2026-11-11T06:51:04+00:00", "content_id": "cad3aa51-cce8-4f7a-b022-3d69155453de", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.2575, "combined_score": 0.2256, "label": "We think this was probably written by a person.", "status": "decided", "phrase_score": 0.0}
{"timestamp": "2026-11-11T06:51:06+00:00", "content_id": "2536a656-a3d1-42cc-91a3-48e1f7454093", "creator_id": "attacker_MF05", "guess": "ai", "model_score": 0.9976, "style_score": 0.6667, "combined_score": 0.8652, "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.", "status": "decided", "phrase_score": 0.0}
{"timestamp": "2026-11-11T06:51:07+00:00", "content_id": "493681c4-b61d-4960-946d-09439757ae7e", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 1.0, "combined_score": 0.9981, "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.", "status": "decided", "phrase_score": 0.0}
{"timestamp": "2026-11-11T06:51:08+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-11T06:52:22+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "missing_text"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03**, a non-native English speaker carefully describing her first month in a new country ("The weather was very different from my home. I did not expect the rain to continue for so many days..."). It was labelled "This looks like it was written by an AI" at a combined score of 0.7345, with both signals agreeing (model 0.81, style 0.63), so the disagreement safeguard never fired. The traits that make her writing clear and careful (plain common words, short even sentences) are the ones both signals read as machine-written. She can appeal, but her only recourse is a person reviewing it later; nothing in the label tells her the system is least reliable on writers like her.


---

## Run Log and Verdicts

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing flagged as AI | at most 1 of 10 labelled high-confidence AI | 3/10 | 3/10 | 3/10 | **MISSED** |
| 2. Clearly-AI and clearly-human score apart | mean combined gap >= 0.30 | 0.324 | 0.324 | 0.324 | MET (barely) |
| 3. All three labels reachable | 3 of 3 labels in 20 texts | 3/3 (5 human, 8 unsure, 7 ai) | 3/3 | 3/3 | MET |
| 4. Appeals always change status and are recorded | 10 of 10, and unknown id gives 404 with no entry | 10/10 + 404 ok | 10/10 + 404 ok | 10/10 + 404 ok | MET |
| 5. Bad input gets a 400, never a 500 | 4 of 4 return 400 | 4/4 | 4/4 | 4/4 | MET |

All three runs were identical to the last digit, as expected: nothing in either signal is random (GPT-2 runs deterministically on the same input), so a miss is a property of the system, not noise. The targets are exactly as I wrote them in `criteria.md`; I did not touch them.

**How I decided each verdict** (against the targets in `criteria.md`, unchanged, and the rule that a target has to hold in every trial):

1. **MISSED.** The target was at most 1 of 10 labelled high-confidence AI. I got 3 of 10 (pieces 2, 3 and 8) in all three trials, so it fails in every trial, not just one.
2. **MET, but only just.** The target was a mean gap of at least 0.30 in each trial. I got 0.691 - 0.367 = 0.324 each time, which clears it by 0.024. Per text it is closer than the mean suggests: the lowest AI text scored 0.600 and the highest human text scored 0.584.
3. **MET.** All three labels appeared in every trial (5 human, 8 unsure, 7 ai of 20). The target only asks for at least one of each, so this says the bands are reachable, not that they are right.
4. **MET.** 10 of 10 valid appeals returned 200, set `under_review` and added exactly one appeal entry, and the unknown id returned 404 with no entry, in all three trials.
5. **MET.** 4 of 4 bad bodies returned 400 and none returned 500, in all three trials. This only shows the route doesn't crash; see Diagnoses for the junk inputs it did not cover.

**Be clear about whose text this is.** I asked Claude to write the ten criterion-1 pieces (first person, informal, four of them plain on purpose), so they are **not my own writing**, and criterion 1 here measures that text rather than mine. The five AI texts in criteria 2 and 3 are also Claude-written; two of the human texts (`FP01`, `EV05`) and five of the borderline ones come from the staff attack set; three more human-style texts are Claude-written. Everything is in `scenarios.py`. Re-running criterion 1 on pieces I really wrote is still to do.

**What I extended in the harness.** The starter `run_eval.py` only posted to `/submit`. I added (a) `appeal_trial` for criterion 4 (submit, appeal, check 200, `under_review`, exactly one new log entry, plus an unknown-id 404), (b) `content_id` and `phrase_score` in each result so the combined score for criterion 2 can be recomputed with `scoring.combine_signals`, (c) a guard in `describe` and `scenarios.validate` so a bare-list body can be sent for criterion 5. No change to the service.

**Real output from one trial** (trial 1 of `results/run_2026-11-11_0202_before.md`), pasted as text. Produced by `run_eval.py::main` (criteria 1, 2, 3, 5) and `run_eval.py::appeal_trial` (criterion 4), against `app.py::submit` and `app.py::appeal`. Long fields trimmed to the relevant rows; the full output is in the results file.

*Criterion 1 — the three pieces labelled AI (all three are the plain ones: #2, #3, #8):*

```json
[
  {
    "status": 200,
    "content_id": "1ff62f8b-faea-4a41-878c-89c74ac9345a",
    "phrase_score": 0.0,
    "guess": "ai",
    "confidence": 0.6657,
    "model_score": 0.8003,
    "style_score": 0.4639,
    "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
    "sent": "Last weekend I cleaned the kitchen. I took everything out of the cupbo"
  },
  {
    "status": 200,
    "content_id": "44c8c53b-51b0-4535-a279-b3003cfafe01",
    "phrase_score": 0.0,
    "guess": "ai",
    "confidence": 0.6026,
    "model_score": 0.6722,
    "style_score": 0.4982,
    "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
    "sent": "My sister called on Sunday to ask if I could look after her cat while "
  },
  {
    "status": 200,
    "content_id": "de17dddd-13fd-4afe-9c7c-3511f56687c9",
    "phrase_score": 0.0,
    "guess": "ai",
    "confidence": 0.6804,
    "model_score": 0.7902,
    "style_score": 0.5158,
    "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
    "sent": "Went to the gym today for the first time in about a month. I did twent"
  }
]
```

*Criterion 2 — first two of each set (means over all five: AI 0.691, human 0.367, gap 0.324):*

```json
[
  {
    "status": 200,
    "content_id": "0c09a313-3eb4-4106-b60f-8fd6110a6bfc",
    "phrase_score": 1.0,
    "guess": "ai",
    "confidence": 0.7977,
    "model_score": 0.7445,
    "style_score": 0.5026,
    "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
    "sent": "Time management is a crucial skill that can significantly impact both "
  },
  {
    "status": 200,
    "content_id": "bd55f7ee-590c-4bec-8e22-24f6ca924292",
    "phrase_score": 0.5376,
    "guess": "ai",
    "confidence": 0.6973,
    "model_score": 0.9068,
    "style_score": 0.4733,
    "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
    "sent": "Renewable energy plays a pivotal role in addressing the challenges of "
  },
  {
    "status": 200,
    "content_id": "36e8e141-ef9f-4fd4-8b1c-980f8c23fd8b",
    "phrase_score": 0.0,
    "guess": "unsure",
    "confidence": 0.5838,
    "model_score": 0.6175,
    "style_score": 0.5332,
    "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
    "sent": "We got to the campsite about four. The pitch was fine, a bit sloped, b"
  },
  {
    "status": 200,
    "content_id": "d3993396-20b6-4010-8f16-8791bbbeb479",
    "phrase_score": 0.0,
    "guess": "human",
    "confidence": 0.6883,
    "model_score": 0.3212,
    "style_score": 0.2974,
    "label": "We think this was probably written by a person.",
    "sent": "Communication at work matters more than people say it does — and I mea"
  }
]
```

*Criterion 3 — one text per label (full run: 5 human, 8 unsure, 7 ai):*

```json
[
  {
    "status": 200,
    "content_id": "457b07f8-debd-4ff8-bed0-fe13d161d646",
    "phrase_score": 0.0,
    "guess": "unsure",
    "confidence": 0.5995,
    "model_score": 0.8641,
    "style_score": 0.4514,
    "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
    "sent": "Social media has transformed the way people communicate in the modern "
  },
  {
    "status": 200,
    "content_id": "a31e9af1-60ec-4500-a752-41bcf8e11492",
    "phrase_score": 0.0,
    "guess": "human",
    "confidence": 0.6883,
    "model_score": 0.3212,
    "style_score": 0.2974,
    "label": "We think this was probably written by a person.",
    "sent": "Communication at work matters more than people say it does — and I mea"
  },
  {
    "status": 200,
    "content_id": "0380bb1f-28e3-4a5a-8f39-2edf698d404e",
    "phrase_score": 1.0,
    "guess": "ai",
    "confidence": 0.7977,
    "model_score": 0.7445,
    "style_score": 0.5026,
    "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
    "sent": "Time management is a crucial skill that can significantly impact both "
  }
]
```

*Criterion 4 — first valid appeal and the unknown-id check:*

```json
[
  {
    "sent": "I started the new job on Monday. The office is about forty minutes fro",
    "submit_status": 200,
    "content_id": "baad77f9-9c33-4c96-a55d-9ef0c5b89eb2",
    "status": 200,
    "appeal_status": "under_review",
    "new_log_entries": 1,
    "ok": true
  },
  {
    "sent": "appeal on unknown content_id",
    "status": 404,
    "new_log_entries": 0,
    "ok": true
  }
]
```

*Criterion 5 — all four bad bodies:*

```json
[
  {
    "status": 400,
    "content_id": null,
    "phrase_score": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "content_id": null,
    "phrase_score": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "content_id": null,
    "phrase_score": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  },
  {
    "status": 400,
    "content_id": null,
    "phrase_score": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "[\"text\", \"creator_id\"]"
  }
]
```

**Diagnoses**

Twenty-one failures (criterion 1 plus the 20 attacks that broke in Milestone 2) come down to four causes, and two of the four are the same signal. I checked each against the saved scores and by re-running the model on edited text, not just by reading the code.

**Cause 1 — Signal one reads plain writing as machine-like (criterion 1, FP02-FP07: 7 failures).** Stage: signal one (`detector.py::model_signal`), with signal two agreeing and the label mapping doing the accusing.
- Mechanism: GPT-2 finds common words in short, ordinary sentences easy to predict, and low surprise scores as AI. Criterion 1's three flagged pieces are all ones written plainly on purpose: model scores 0.800, 0.672 and 0.790 (pieces 2, 3, 8). FP02-FP07 sit at 0.739-0.882 on the same signal.
- Signal two agreed rather than corrected it. `punctuation_density` (`stylometry.py`) maps "few commas" to AI: these texts have almost none (raw 0.000-0.013 against a 0.15 "fully human" mark), so that measure scores 0.91-1.0 on them. Style came out 0.464, 0.498 and 0.516 for the three flagged pieces.
- The combining rule (`scoring.py::combine_signals`, 0.6 model + 0.4 style) is built to pull disagreements toward "unsure", but it never fired: the gaps were 0.34, 0.17 and 0.27, under `DISAGREEMENT_GAP` of 0.4 (the same for FP02-FP07, the largest being FP06 at 0.39). Two signals that share the same bias do not cancel.
- Label mapping adds the last push: `AI_THRESHOLD` is 0.60 (lowered from 0.65 in unit 7). Piece 3 combined to 0.6026, so it is flagged by 0.0026. At 0.65 criterion 1 would be 2 of 10, which is still a miss, so the threshold is not the cause, but it decides which writer is accused.
- FP07 is a separate wrinkle: it repeats a phrase on purpose, so its type-token ratio is 0.46 and signal two scores variety as 0.88 AI. FP04 was also pushed up by the stock-phrase signal (+0.49 x 0.15).

**Cause 2 — Neither signal reads meaning, so cosmetic changes move signal one (EV01, EV05, EV08, PI02: 4 failures).** Stage: signal one.
- EV01 (typos): the same AI paragraph scores model 0.666-0.704 clean (EV03, EV09) and 0.164 with typos. Typos like "poistioned" and "thsi" become rare tokens GPT-2 cannot predict, which reads as human. Fixing just two of them moved it from 0.164 to 0.255, so each typo contributes. Signal two barely changed (0.531), so it is the model signal, not word variety, that was fooled.
- PI02 (injection): it did not work by persuading anything; there is no model reading the instruction. The odd "SYSTEM: ..." prefix is itself unpredictable text: the same body scores 0.754 without it and 0.204 with it, a drop of 0.55 from the prefix alone.
- EV05 (heavy human editing): model 0.321, style 0.297, both signals read it as human, with fragments, a spread of 0.68 and unusual phrasing like "away-day". This one is arguably not a mistake: a human has rewritten it.
- EV08 (below the token window): 10 words. Signal one is unreliable on so few tokens (0.245), and the combined 0.360 clears the human threshold (0.35) by 0.01, landing in "unsure". The route accepts it because it only checks that text is non-empty.

**Cause 3 — The weighted average and the label mapping leave AI text no margin (EV02, EV03, EV04, EV06, EV09: 5 failures).** Stage: combining rule and label mapping, with signal two as the lever.
- Even clean AI text only reaches 0.67-0.70 on signal one (EV03 0.666, EV09 0.704). Signal two then pulls it down: `sentence_length_spread` is trivially raised by splitting sentences (EV02: spread 0.85, so that measure scores 0.0 AI) or adding a quote or a casual opening (EV03 style 0.412, EV09 0.379).
- With a 0.4 weight, a style score around 0.4 costs about 0.1 on the combined score, which is exactly enough to drop 0.70 to 0.57: EV09 is 0.6 x 0.704 + 0.4 x 0.379 = 0.574, under 0.60. None of the five triggered the disagreement pull (the gaps were 0.09-0.32). They all landed at 0.48-0.58, in the wide "unsure" band, so they were not caught, though none was wrongly called human.

**Cause 4 — Junk input reaches scoring and signal two reads it as maximally AI (MF03-MF07: 5 failures).** Stage: signal two (`stylometry.py::words`), with the route letting it through.
- `words()` only matches `[a-z0-9']+`, so emoji (MF06), right-to-left script (MF07) and punctuation only (MF04) contain zero words. With no words, type-token ratio, punctuation density and sentence spread all come out at the AI end, and style is exactly 1.0. Signal one agrees on repeated or odd tokens (0.997 for emoji, 0.906 for RTL), giving combined scores of 0.998 and 0.944 for MF06 and MF07 and a confident "ai". MF05 (one very long word) is one "sentence", so spread is 0.0, and it combines to 0.865.
- MF03 (control characters) and MF04 landed in "unsure" only because the signals disagreed by 0.67 and 0.99, and the pull toward 0.5 fired. That was the safeguard working, not the signals.
- The route (`app.py::submit`) accepts anything non-empty and under 10,000 characters, with no check that the text has letters or enough words, so none of this is stopped at the door.
- This is not just a test curiosity: any writer using a non-Latin script would get style 1.0 on every submission.

**The pattern.** Causes 1 and 2 are both signal one, and cause 4 is signal two's defaults, so every failure except the label-mapping squeeze in cause 3 traces to the two signals rather than to the route, the limiter or the labels. The deepest problem is that both signals measure how *ordinary* the text looks, not who wrote it. Plain human writing and lightly disguised AI text look the same to them, and the combining rule can only average two views that fail in the same way. The cheapest fix for the accusation harm is therefore not a different threshold: it is a signal that does not share the bias, or a minimum-evidence guard so junk and very short text is never accused.

**Were my targets too easy?** Not the first one: criterion 1 (at most 1 in 10) was a fair target and it caught the real problem, so I am leaving it where it is. Criteria 2 and 3 were too soft. Criterion 2 compares means, so it passed by 0.024 while a real plain human text (0.584) sat 0.016 under the lowest AI text (0.600). Criterion 3 only asks that each label appear once, which a badly calibrated system also passes. Criterion 5 passed 4 of 4 while the attack set found five junk inputs (MF03-MF07) that got confident verdicts, because it only tests for a crash. **The one I would tighten is criterion 2**: require every AI text to score at least 0.10 above every human text, in every trial. That would currently fail (0.600 against 0.584), which is the honest answer.

**Criteria revisions.** None. All five criteria could be measured and gave a verdict, so none counts as broken, and a missed or soft target is not a reason to change it. `criteria.md` is untouched; the tightening above is a note, not an edit.

---

## The Improvement

**What I changed:** one number. `AI_THRESHOLD` in `config.py` went from 0.60 to 0.75, so the "high-confidence AI" band is now 0.75-1.00 and the "unsure" band is 0.35-0.75. Nothing else moved: same weights (0.6 / 0.4 plus the phrase boost), same `HUMAN_THRESHOLD` of 0.35, same signals, same route, same attack set and scenarios, same creator ids.

**Which diagnosis pointed at it:** Cause 1 in the Diagnoses above: both signals read plain human writing as machine-like, and the plain pieces and FP02-FP07 all landed at 0.60-0.78, inside the AI band. That is also why criterion 1 was MISSED. I picked the threshold, not the weights or the signals, because it is the one knob that acts directly on "who gets accused", and because one number is easy to measure before and after.

**This partly undoes a choice from unit 7.** I lowered the threshold from 0.65 to 0.60 then, so that a clearly-AI test text (0.640) could reach the AI label at all. Moving it to 0.75 gives that back, and more.

### Attack Run — After

`python run_attacks.py --set attack_set/attack_set --label after` (`results/attack_run_2026-11-11_0213_after.md`; RQ10 and RQ11 were first 429 again from the shared IP bucket and were re-sent after the window, `results/attack_run_2026-11-11_0214_after_rerun.md`, exactly as in the before run; both returned 400, but the two re-sends fell in the same minute, so that file holds only the second one, RQ11). The same held/broke rules as the before run, applied to both, so the two columns are comparable. All 56 parsed, no 5xx.

| Family | Attacks | Before: held / broke | After: held / broke |
|---|---|---|---|
| evasion | 10 | 2 / 8 | 1 / 9 |
| false_positive | 8 | 2 / 6 | **5 / 3** |
| prompt_injection | 6 | 5 / 1 | 5 / 1 |
| malformed (text) | 8 | 3 / 5 | 3 / 5 |
| malformed (request) | 12 | 12 / 0 | 12 / 0 |
| flood_same_creator | 12 | 12 / 0 | 12 / 0 |
| **Total** | **56** | **36 / 20** | **38 / 18** |

Four attacks changed, and nothing else did:

| ID | Combined score | Before | After | Held or broke |
|---|---|---|---|---|
| FP02 | 0.703 | ai | unsure | broke -> **held** |
| FP03 | 0.735 | ai | unsure | broke -> **held** |
| FP06 | 0.727 | ai | unsure | broke -> **held** |
| EV07 | 0.669 | ai | unsure | held -> **broke** |

Every attack, before and after (guess is what the service said; RQ10 and RQ11 are shown with their re-sent result, 400; `—` means no guess because the request was refused or limited):

| ID | Family | Status | Guess before -> after | Verdict before -> after |
|---|---|---|---|---|
| EV01 | evasion | 200 | human -> human | BROKE -> BROKE |
| EV02 | evasion | 200 | unsure -> unsure | BROKE -> BROKE |
| EV03 | evasion | 200 | unsure -> unsure | BROKE -> BROKE |
| EV04 | evasion | 200 | unsure -> unsure | BROKE -> BROKE |
| EV05 | evasion | 200 | human -> human | BROKE -> BROKE |
| EV06 | evasion | 200 | unsure -> unsure | BROKE -> BROKE |
| EV07 | evasion | 200 | ai -> unsure | HELD -> BROKE **(changed)** |
| EV08 | evasion | 200 | unsure -> unsure | BROKE -> BROKE |
| EV09 | evasion | 200 | unsure -> unsure | BROKE -> BROKE |
| EV10 | evasion | 200 | ai -> ai | HELD -> HELD |
| FP01 | false_positive | 200 | unsure -> unsure | HELD -> HELD |
| FP02 | false_positive | 200 | ai -> unsure | BROKE -> HELD **(changed)** |
| FP03 | false_positive | 200 | ai -> unsure | BROKE -> HELD **(changed)** |
| FP04 | false_positive | 200 | ai -> ai | BROKE -> BROKE |
| FP05 | false_positive | 200 | ai -> ai | BROKE -> BROKE |
| FP06 | false_positive | 200 | ai -> unsure | BROKE -> HELD **(changed)** |
| FP07 | false_positive | 200 | ai -> ai | BROKE -> BROKE |
| FP08 | false_positive | 200 | unsure -> unsure | HELD -> HELD |
| PI01 | prompt_injection | 200 | unsure -> unsure | HELD -> HELD |
| PI02 | prompt_injection | 200 | human -> human | BROKE -> BROKE |
| PI03 | prompt_injection | 200 | unsure -> unsure | HELD -> HELD |
| PI04 | prompt_injection | 200 | unsure -> unsure | HELD -> HELD |
| PI05 | prompt_injection | 200 | unsure -> unsure | HELD -> HELD |
| PI06 | prompt_injection | 200 | unsure -> unsure | HELD -> HELD |
| MF01 | malformed | 400 | — -> — | HELD -> HELD |
| MF02 | malformed | 400 | — -> — | HELD -> HELD |
| MF03 | malformed | 200 | unsure -> unsure | BROKE -> BROKE |
| MF04 | malformed | 200 | unsure -> unsure | BROKE -> BROKE |
| MF05 | malformed | 200 | ai -> ai | BROKE -> BROKE |
| MF06 | malformed | 200 | ai -> ai | BROKE -> BROKE |
| MF07 | malformed | 200 | ai -> ai | BROKE -> BROKE |
| MF08 | malformed | 400 | — -> — | HELD -> HELD |
| RQ01 | malformed | 400 | — -> — | HELD -> HELD |
| RQ02 | malformed | 400 | — -> — | HELD -> HELD |
| RQ03 | malformed | 400 | — -> — | HELD -> HELD |
| RQ04 | malformed | 400 | — -> — | HELD -> HELD |
| RQ05 | malformed | 400 | — -> — | HELD -> HELD |
| RQ06 | malformed | 400 | — -> — | HELD -> HELD |
| RQ07 | malformed | 400 | — -> — | HELD -> HELD |
| RQ08 | malformed | 400 | — -> — | HELD -> HELD |
| RQ09 | malformed | 400 | — -> — | HELD -> HELD |
| RQ10 | malformed | 400 | — -> — | HELD -> HELD |
| RQ11 | malformed | 400 | — -> — | HELD -> HELD |
| RQ12 | malformed | 400 | — -> — | HELD -> HELD |
| FL01_01 | flood_same_creator | 200 | unsure -> unsure | HELD -> HELD |
| FL01_02 | flood_same_creator | 200 | unsure -> unsure | HELD -> HELD |
| FL01_03 | flood_same_creator | 200 | unsure -> unsure | HELD -> HELD |
| FL01_04 | flood_same_creator | 200 | unsure -> unsure | HELD -> HELD |
| FL01_05 | flood_same_creator | 200 | unsure -> unsure | HELD -> HELD |
| FL01_06 | flood_same_creator | 429 | — -> — | HELD -> HELD |
| FL01_07 | flood_same_creator | 429 | — -> — | HELD -> HELD |
| FL01_08 | flood_same_creator | 429 | — -> — | HELD -> HELD |
| FL01_09 | flood_same_creator | 429 | — -> — | HELD -> HELD |
| FL01_10 | flood_same_creator | 429 | — -> — | HELD -> HELD |
| FL01_11 | flood_same_creator | 429 | — -> — | HELD -> HELD |
| FL01_12 | flood_same_creator | 429 | — -> — | HELD -> HELD |

The worst outcome from the before run, FP03 (the careful non-native writer), is now "unsure" instead of "high-confidence AI".

### Criteria — before and after

| Criterion | Target | Before (runs 1/2/3) | After (runs 1/2/3) | Verdict before -> after |
|---|---|---|---|---|
| 1. My own writing flagged as AI | at most 1 of 10 | 3 / 3 / 3 | **0 / 0 / 0** | MISSED -> **MET** |
| 2. AI vs human score gap | gap >= 0.30 | 0.324 x3 | 0.324 x3 | MET -> MET (unchanged) |
| 3. All three labels reachable | 3 of 3 labels | 3/3 (5 human, 8 unsure, 7 ai) | 3/3 (5 human, **13 unsure, 2 ai**) | MET -> MET (barely) |
| 4. Appeals change status and are logged | 10/10 + 404 | 10/10 + 404 x3 | 10/10 + 404 x3 | MET -> MET |
| 5. Bad input gets a 400 | 4 of 4 | 4/4 x3 | 4/4 x3 | MET -> MET |

Results in `results/run_2026-11-11_0202_before.md` and `results/run_2026-11-11_0215_after.md`. Scores and labels were identical across the three trials in both runs (only the random `content_id`s differ).

**Did it help, and how do I know:** Yes for the writers I was worried about, at a real cost to catching AI: criterion 1 went from MISSED (3 of 10, every trial) to MET (0 of 10), and three of the six accused writers in the attack set (FP02, FP03, FP06) are now "unsure", but the AI label has become close to unreachable.

- **Who pays now.** AI text. Of my five clearly-AI texts, 4 got the AI label before and 1 does now (the other four score 0.600-0.716 and become "unsure"). In the 20-text coverage set the AI label fell from 7 texts to 2. In the attack set EV07 (a padded AI text) slipped through to "unsure". A site that relies on the AI label would now catch very little on its own and has to rely on "unsure" plus a person.
- **What it did not fix.** FP04 (0.781), FP05 (0.753) and FP07 (0.750) are still labelled AI, and that is the finding that matters: they sit within 0.02 of my highest-scoring AI text (0.798). The two groups overlap, so no threshold separates them; moving the line only decides which group is wrongly handled. Causes 2, 3 and 4 in the Diagnoses are untouched: the typo and injection evasions (EV01, EV05, EV08, PI02), the five evasions the weights leave in "unsure", and the five junk inputs (MF03-MF07) all gave exactly the same results as before.
- **Two of my targets did not notice the cost.** Criterion 2 is unchanged at 0.324 because it compares mean scores, which a threshold cannot move. Criterion 3 still passes with only 2 of 20 texts labelled AI, so it says the AI label is reachable, not that it is useful. Both are the soft targets I flagged in the Diagnoses.
- **Caution about the number itself.** I chose 0.75 after seeing these same 56 attacks and these same texts, and FP05 (0.7526) and FP07 (0.7501) sit right on the line. So the improvement on this set is optimistic; I would not expect the same gain on new writing.

---

## What's Still Broken

After the Milestone 5 re-run, **18 of the 56 attacks still break** and **no criterion is missed**. That last part flatters me, so it comes with caveats at the end of this section. Grouped by the four causes in Diagnoses:

**Cause 1: real writers still accused (FP04 0.781, FP05 0.753, FP07 0.750).**
- *What I'd do:* add a signal that does not share the bias, such as a second, different language model, or a calibration set of real human writing, rather than move the line again.
- *Why I stopped:* the unit allows one improvement, and a threshold cannot fix this: these three sit within 0.02 of my highest-scoring AI text (0.798), so the groups overlap.

**Cause 2: cosmetic edits move signal one (EV01 typos, PI02 injected prefix, EV05 heavy human edit, EV08 under ten words).**
- *What I'd do:* make the model signal harder to nudge: score sentence by sentence and take the median, ignore an odd leading line, and refuse text that is too short to judge.
- *Why I stopped:* one change only, and none of these was the biggest harm. EV05 is arguably not a mistake, since a person rewrote it.

**Cause 3: AI text sits in "unsure" (EV02, EV03, EV04, EV06, EV09, and EV07, which I lost when I raised the threshold).**
- *What I'd do:* rebalance how far the style signal can pull down a high model score.
- *Why I stopped:* any reweight trades directly against the fix for plain writers, and I had no way to measure the two separately inside one change.

**Cause 4: junk gets a confident verdict (MF03-MF07).**
- *What I'd do:* in the route, reject text with fewer than about five real letter-words before any signal runs, and make `stylometry.words()` count letters in any script, so non-Latin writers aren't scored 1.0 on style.
- *Why I stopped:* I had planned this as a second improvement and chose not to do it, so that the one before/after in The Improvement stays comparable. It is the cheapest and safest of the four, and the first thing I would do next.

**Criteria: caveats on "none missed."**
- Criterion 1 is met on ten pieces that **Claude wrote, not me** (the README says so in the run log). It has to be re-run on my own writing before I believe it.
- It is met because I moved the threshold, not because the signals got better. The same three plain pieces still score 0.60-0.68; they are just no longer called AI.
- Criterion 2 passes by 0.024, and criterion 3 passes with only 2 of 20 texts labelled AI, so both are too soft; I would tighten criterion 2 as noted in Diagnoses. Criterion 5 only checks for a crash and misses the junk in Cause 4.

**Never tested:** writing outside these 56 attacks and my own test texts, and the 0.75 threshold was chosen on the same data I measured it on, so it will look better here than it would on new writing.

**The trade I'd make if this ran for real:** I would keep the wide "unsure" band and never show an AI accusation on a score alone, sending AI-leaning and "unsure" work to a person for review. The people who pay are the reviewers, who get more work, and readers, who see more undetected AI text, but that is better than a writer taking a wrong accusation in public, which costs them far more than a missed detection costs the site.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

---

## Capstone

**What This Extends**

Provenance Guard (the same one submitted for units 7 and 8). What's new is a minimum-evidence guard on `POST /submit`: text that has too few real words to judge is refused with a 400 before any signal runs, instead of being scored. This is the fix I named as the first thing I'd do in What's Still Broken, Cause 4: junk input (MF03-MF07 in the attack set: control characters, punctuation only, one very long word, emoji, right-to-left script) currently reaches scoring, makes `stylometry.words()` return nothing, pushes the style score to exactly 1.0, and gets a confident "ai" label at 0.87-0.99.

**The Shape**

Shape B, harden against failure. The extension is one change to the bad path: a check in `app.py::submit` that counts words with the same `stylometry.words()` the style signal uses, and returns a 400 (`reason: not_enough_text`, logged like the other rejections) when there are fewer than about five. Counting with the signal's own tokenizer means the guard refuses exactly the inputs the signal cannot read, instead of guessing. The run path, the structured log fields and the cost measurement that every shape needs are part of this unit too, but they are the operational layer around the extension, not the extension.

Out of scope, decided before building:

- **Not changing the signals, weights or thresholds.** Causes 1-3 (plain writers accused, cosmetic edits moving the model signal, AI text stuck in "unsure") stay as unit 8 left them, including `AI_THRESHOLD` at 0.75.
- **Not teaching the style signal other scripts.** `stylometry.words()` stays Latin-only. A writer using another script will get a 400 telling them this checks English text, which is an honest refusal rather than a confident wrong verdict. Scoring those scripts properly is a bigger change than one unit allows.
- **Not adding a capability or a hosted deploy.** No new signal or endpoint (shape C), and no hosting (Path A): the model needs more than a free host's 512 MB, so this runs locally.

**Running It**

Path B, local with logs, run in a Docker container: build once with `docker build -t provenance-guard .`, then one `docker run` command starts it (the command, the mounts, the environment and the smoke check are in [RUNNING.md](RUNNING.md)). The image installs CPU-only torch first, so it is 1.29 GB rather than several GB. I built it from a fresh `git clone` of this repo, plus my uncommitted changes copied in, and ran the command from `RUNNING.md` as written. It started, `/health` answered, and `python check_guard.py` passed inside a container. Two things the fresh start taught me: the smoke check scores a real text, so it needs the Hugging Face cache mounted or it downloads gpt2 first; and a container needs `HOST=0.0.0.0` (set in the `Dockerfile`) or the published port reaches nothing.

**Instrumentation**

`POST /submit` writes one JSON line to `logs/audit.jsonl` for every request that reaches the route, whatever happens to it. A scored request records `timestamp`, `content_id`, `creator_id`, `guess`, `model_score`, `style_score`, `combined_score`, `phrase_score`, `label`, `status`, plus the three fields added this unit: `input` (the first 200 characters, or the raw body when there is no usable text), `outcome` (`scored`, `refused` or `failed`) and `duration_ms` (time inside the route, so it includes the model). A refused request records `timestamp`, `creator_id`, `event: rejected`, `status: rejected`, `reason`, `input`, `outcome: refused` and `duration_ms`. A request that errors because the model is unavailable records the same with `event: failed`, `status: failed`, `reason: detector_unavailable` and `outcome: failed`; I did not trigger that in the live session below, but `check_guard.py` forces it and asserts the record exists. One known gap: a rate-limited request (429) is rejected before the route runs, so its record has no `input` or `duration_ms`.

Sixteen entries from one real session (the container, with the model cache and `logs/` mounted; the first line is the cold request that loaded the model, the next nine are warm requests from the attack set, and the last six are refusals, which are the failed runs). Pasted as written to the log file:

```json
{"timestamp": "2026-11-23T06:09:48+00:00", "content_id": "dc2e8f84-0744-462e-bf6d-c7ff8d78ff03", "creator_id": "cap_cold", "guess": "unsure", "model_score": 0.6175, "style_score": 0.5332, "combined_score": 0.5838, "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.", "status": "decided", "phrase_score": 0.0, "input": "We got to the campsite about four. The pitch was fine, a bit sloped, but there was a tap nearby and the toilets were clean enough. Putting the tent up took longer than it should have because I had for", "outcome": "scored", "duration_ms": 7716.0}
{"timestamp": "2026-11-23T06:09:48+00:00", "content_id": "045465ea-56d7-4a1f-8460-67374162061d", "creator_id": "cap_warm_FP02", "guess": "unsure", "model_score": 0.7387, "style_score": 0.6493, "combined_score": 0.7029, "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.", "status": "decided", "phrase_score": 0.0, "input": "This report sets out the findings of the working group. The group met four times between January and March. Its remit was to review the current arrangements and to recommend changes where these were w", "outcome": "scored", "duration_ms": 151.1}
{"timestamp": "2026-11-23T06:09:49+00:00", "content_id": "2d35897e-552d-4cd0-b660-ecaf214b8c82", "creator_id": "cap_warm_FP03", "guess": "unsure", "model_score": 0.8051, "style_score": 0.6285, "combined_score": 0.7345, "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.", "status": "decided", "phrase_score": 0.0, "input": "I want to describe my experience of the first month in this country. The weather was very different from my home. I did not expect the rain to continue for so many days. My colleagues were kind and th", "outcome": "scored", "duration_ms": 147.3}
{"timestamp": "2026-11-23T06:09:49+00:00", "content_id": "91c7f68d-c4ca-4f1e-979f-1228cd47ba49", "creator_id": "cap_warm_FP04", "guess": "ai", "model_score": 0.8329, "style_score": 0.5202, "combined_score": 0.7813, "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.", "status": "decided", "phrase_score": 0.4902, "input": "There are three main causes of the conflict. The first cause is economic. Trade between the two regions had declined significantly in the preceding decade. The second cause is political. Neither gover", "outcome": "scored", "duration_ms": 129.9}
{"timestamp": "2026-11-23T06:09:49+00:00", "content_id": "c47e42a0-18a2-45b1-bd8a-d802e09818a9", "creator_id": "cap_warm_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.6808, "combined_score": 0.7526, "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.", "status": "decided", "phrase_score": 0.0, "input": "To configure the service, edit the settings file in the installation directory. Set the host value to the address the service should bind to. Set the port value to an unused port above 1024. Save the ", "outcome": "scored", "duration_ms": 162.1}
{"timestamp": "2026-11-23T06:09:49+00:00", "content_id": "b6238eb4-392b-44c5-a270-0f22c5a506d9", "creator_id": "cap_warm_FP06", "guess": "unsure", "model_score": 0.8814, "style_score": 0.4951, "combined_score": 0.7269, "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.", "status": "decided", "phrase_score": 0.0, "input": "Dear Sir or Madam, I am writing to enquire about the position advertised on your website. I have five years of relevant experience and I believe I would be a strong fit for the role. I have attached m", "outcome": "scored", "duration_ms": 124.9}
{"timestamp": "2026-11-23T06:09:49+00:00", "content_id": "02b3ae83-1dac-40d9-a599-11dbecc1656f", "creator_id": "cap_warm_FP07", "guess": "ai", "model_score": 0.8816, "style_score": 0.5529, "combined_score": 0.7501, "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.", "status": "decided", "phrase_score": 0.0, "input": "It rained on Monday. It rained on Tuesday. It rained on Wednesday and it rained on Thursday and by Friday I had stopped looking out of the window altogether. The forecast said it would clear. The fore", "outcome": "scored", "duration_ms": 128.2}
{"timestamp": "2026-11-23T06:09:49+00:00", "content_id": "36d1110c-75f9-4241-971d-fa2fc2aee1fe", "creator_id": "cap_warm_FP08", "guess": "unsure", "model_score": 0.3223, "style_score": 0.4605, "combined_score": 0.3776, "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.", "status": "decided", "phrase_score": 0.0, "input": "Went for a run. Legs hurt. Worth it.", "outcome": "scored", "duration_ms": 44.4}
{"timestamp": "2026-11-23T06:09:50+00:00", "content_id": "cc02d22e-6123-4f3d-831f-62549a9259c6", "creator_id": "cap_warm_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.5313, "combined_score": 0.3106, "label": "We think this was probably written by a person.", "status": "decided", "phrase_score": 0.0, "input": "The importance of effective communication in the workplace cannot be overstated. Teams that communicate clearly are better poistioned to achieve their objectives and avoid costly misunderstandings. Th", "outcome": "scored", "duration_ms": 186.4}
{"timestamp": "2026-11-23T06:09:50+00:00", "content_id": "7f3e9a65-f3ee-42ab-9747-68c33797c86a", "creator_id": "cap_warm_EV02", "guess": "unsure", "model_score": 0.5943, "style_score": 0.3106, "combined_score": 0.4808, "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.", "status": "decided", "phrase_score": 0.0, "input": "The importance of effective communication in the workplace cannot be overstated. Really. Teams that communicate clearly are better positioned to achieve their objectives and avoid costly misunderstand", "outcome": "scored", "duration_ms": 175.9}
{"timestamp": "2026-11-23T06:09:40+00:00", "creator_id": "cap_MF03", "event": "rejected", "status": "rejected", "reason": "not_enough_text", "input": "\u0000\u0001\u0002 test \u001b[31mred\u001b[0m", "outcome": "refused", "duration_ms": 0.1}
{"timestamp": "2026-11-23T06:09:40+00:00", "creator_id": "cap_MF04", "event": "rejected", "status": "rejected", "reason": "not_enough_text", "input": "!!! ??? ... ,,, ;;; --- ((( )))", "outcome": "refused", "duration_ms": 0.0}
{"timestamp": "2026-11-23T06:09:40+00:00", "creator_id": "cap_MF05", "event": "rejected", "status": "rejected", "reason": "not_enough_text", "input": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "outcome": "refused", "duration_ms": 0.0}
{"timestamp": "2026-11-23T06:09:40+00:00", "creator_id": "cap_MF06", "event": "rejected", "status": "rejected", "reason": "not_enough_text", "input": "🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣🙂🙃😀😃😄😁😆😅😂🤣", "outcome": "refused", "duration_ms": 0.0}
{"timestamp": "2026-11-23T06:09:40+00:00", "creator_id": "cap_MF07", "event": "rejected", "status": "rejected", "reason": "not_enough_text", "input": "هذا نص باللغة العربية لاختبار كيفية تعامل النظام مع النصوص التي لا تستخدم الأبجدية اللاتينية على الإطلاق.", "outcome": "refused", "duration_ms": 0.0}
{"timestamp": "2026-11-23T06:09:40+00:00", "creator_id": "cap_missing", "event": "rejected", "status": "rejected", "reason": "missing_text", "input": "{\"creator_id\": \"cap_missing\"}", "outcome": "refused", "duration_ms": 0.0}
```

Reading them: the five junk inputs (MF03-MF07) and the two malformed requests were refused in 0.0-0.1 ms, and `GET /health` still reported `detector_loaded: false` after them, so the guard really does run before the model. The first scored request took 7716 ms because it loaded gpt2; every later one took 44-206 ms.

**What It Costs**

*Per-run cost:* **0.146 s of compute per scored request** (mean of 10 warm runs, `duration_ms` from the log: 151.1, 147.3, 129.9, 162.1, 124.9, 128.2, 44.4, 186.4, 175.9, 206.0). **No API spend**: nothing calls a hosted service. A one-off **7.7 s** is paid when the container starts and the first scored request loads the model; a refused request costs about 0.0 s.

*How I measured it:* started the container, sent 10 different attack-set texts (FP02-FP08, EV01-EV03), one `creator_id` each so the rate limiter stayed out of the way, after one cold request had loaded the model. I took the mean of the `duration_ms` field the service itself wrote, and cross-checked it against the client's stopwatch for the same ten requests (mean 0.180 s, the extra being HTTP and the container's network). The service holds about **1.0 GB resident** once loaded (1.05 GB peak, from `VmRSS` and `VmHWM` in `/proc/1/status` inside the container). `docker stats` showed only 365 MiB for the same container, because it leaves out file-cache pages the model weights sit in, so I used the process figure. Measured on one 16 GB Windows laptop with Docker Desktop, on texts of 8-105 words, so longer texts or another machine will differ.

*A hundred people a day:* the arithmetic assumes each person submits 3 pieces. 100 people x 3 submissions = 300 runs; 300 x 0.146 s = **44 s of compute a day**, about $0 in API spend. Even if every one of the 100 hit the daily cap of 50, 100 x 50 = 5,000 runs x 0.146 s = 730 s, about 12 minutes. The compute is trivial; the memory is the real cost: a host has to keep about 1 GB of RAM occupied around the clock for a service that is idle almost all of the time, which is also why this cannot sit on a 512 MB free tier.

**Run Log and Verdicts**

Run with `python run_capstone.py --label before` (full output in `results/capstone_run_2026-11-23_0121_before.md`) against the Docker container from Running It. Targets are exactly as written in `criteria.md`; I did not touch them. Each trial restarts the container first, so the model is unloaded when criterion 3's junk arrives.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Junk is refused, not scored | MF03-MF07 all 400, `reason: not_enough_text`, no scores in the log (5 of 5) | 5/5 | 5/5 | 5/5 | MET |
| 2. Real writing not refused, scores unchanged | 31 texts: 0 refused, `combined_score` equal to unit 8 to 4 decimals | 31/31 | 31/31 | 31/31 | MET |
| 3. Guard runs before the model | 5 junk inputs each under 500 ms, `detector_loaded` still false after | 5/5, false | 5/5, false | 5/5, false | MET |
| 4. Every request leaves a complete record | 20 requests, 20 log entries, 4 fields non-null on each | 20/20 | 20/20 | 20/20 | MET |
| 5. The boundary sits at 5 | 10 pairs: every 4-word text 400, every 5-word text 200 (20 of 20) | 20/20 | 20/20 | 20/20 | MET |

All five met in all three trials, and the three trials are identical in every number except timings. That is expected here and I checked it was a real re-run: nothing in this extension is random (the guard is a word count, and gpt2 scores the same input the same way), the log grew by exactly 243 entries over the run (3 trials x 81 requests), and each trial restarted the container. Meeting all five is not the same as the system being good; see the last paragraph of this section.

**How I decided each verdict.**

1. **MET.** All five junk inputs returned 400 with `not_enough_text`, and the log entry for each has no `model_score` or `style_score` key.
2. **MET.** 31 texts = the 10 plain pieces and 20 coverage texts from `scenarios.py`, plus EV08. All 31 returned 200 and the `combined_score` recomputed with `scoring.combine_signals` matched the unit 8 value to 4 decimals every time. One wrinkle in my own criterion: it names `run_2026-11-11_0215_after.md`, but EV08 is not in that file (it is in the attack run). I took EV08's baseline from `attack_run_2026-11-11_0213_after.md` (model 0.2452, style 0.532, phrase assumed 0.0, which gives combined 0.3599 and reproduces its recorded confidence 0.6401). The container runs a different torch build (2.15.0+cpu) from the one that produced the unit 8 numbers; it made no difference at 4 decimals.
3. **MET.** The slowest junk refusal took 30.9 ms and the fastest 11.5 ms, measured by the client including HTTP, over all 15 refusals. `/health` reported `detector_loaded: false` before and after in every trial.
4. **MET.** Each trial sent 10 scored, 5 junk and 5 other bad requests (missing text, empty text, 20,000 characters, a bare list, missing creator_id). The log grew by exactly 20 and no entry was missing a field.
5. **MET.** All ten 4-word texts returned 400 and all ten 5-word texts returned 200, in every trial.

**Whose text this is.** The 10 plain pieces and most of the 20 coverage texts are the same ones as unit 8, and Claude wrote them (see Run Log and Verdicts, unit 8). Criteria 2 and 4 use them as test material only; nothing here claims they are my own writing.

**Real output from one trial** (trial 1). Produced by `run_capstone.py::c1`, `c2`, `c3`, `c4` and `c5`, against `app.py::submit`. Log lines are from `logs/audit.jsonl`, written by `audit.py::log_rejection` and `audit.log_decision`.

*Criterion 1: the five junk inputs (`run_capstone.py::c1`) and the log line for one of them:*

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

```json
{"timestamp": "2026-11-23T06:20:56+00:00", "creator_id": "cap_t1_c1_MF04", "event": "rejected", "status": "rejected", "reason": "not_enough_text", "input": "!!! ??? ... ,,, ;;; --- ((( )))", "outcome": "refused", "duration_ms": 0.0}
```

*Criterion 2: first three texts and EV08, new `combined` against the unit 8 `baseline` (`run_capstone.py::c2`; all 31 matched):*

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
    "i": 30,
    "status": 200,
    "combined": 0.3599,
    "baseline": 0.3599,
    "ok": true
  }
]
```

*Criterion 3: junk refused before the model loaded (`run_capstone.py::c3`):*

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

*Criterion 4: the 20 requests (10 x 200 for the scored ones, then ten 400s), the log growth, and four of the 20 log lines (a scored request, a junk input, a 20,000-character text, a missing text) (`run_capstone.py::c4`):*

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

```json
{"timestamp": "2026-11-23T06:21:12+00:00", "content_id": "e6d23561-e9d4-45e0-b8a2-2efad56f6a59", "creator_id": "cap_t1_c4_s0", "guess": "unsure", "model_score": 0.6182, "style_score": 0.5328, "combined_score": 0.584, "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.", "status": "decided", "phrase_score": 0.0, "input": "I started the new job on Monday. The office is about forty minutes from my flat by bus. My manager showed me around and introduced me to everyone, and I forgot most of the names straight away. The des", "outcome": "scored", "duration_ms": 141.0}
{"timestamp": "2026-11-23T06:21:14+00:00", "creator_id": "cap_t1_c4_MF04", "event": "rejected", "status": "rejected", "reason": "not_enough_text", "input": "!!! ??? ... ,,, ;;; --- ((( )))", "outcome": "refused", "duration_ms": 0.0}
{"timestamp": "2026-11-23T06:21:14+00:00", "creator_id": "cap_t1_c4_huge", "event": "rejected", "status": "rejected", "reason": "text_too_long", "input": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "outcome": "refused", "duration_ms": 0.0}
{"timestamp": "2026-11-23T06:21:14+00:00", "creator_id": "cap_t1_c4_nt", "event": "rejected", "status": "rejected", "reason": "missing_text", "input": "{\"creator_id\": \"cap_t1_c4_nt\"}", "outcome": "refused", "duration_ms": 0.0}
```

*Criterion 5: first two of the ten pairs (`run_capstone.py::c5`; all ten matched):*

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
  }
]
```

**Were my targets too easy?** Yes, and I checked rather than guessed. Criterion 1 only tests the five junk inputs the extension was built for, and all five have fewer than five words. After the run I sent a few inputs the guard counts as enough text: `asdf asdf asdf asdf asdf asdf asdf asdf` (8 words) came back labelled **ai at 0.97 confidence**, `buy now buy now buy now buy now buy now` at 0.97, and `the the the the the the` at 0.76, all with a style score of exactly 1.0. The guard counts words, not whether they are real writing, so five-word junk walks straight through, and criterion 5 only proves the boundary is at five, not that five is enough. **The one I would tighten is criterion 1**: test a set of at least 10 junk inputs of 5 or more words (repeated tokens, keyboard mashing, numbers only) and require 10 of 10 to be refused. That would fail today.

**The Improvement**

**What I changed:** one check, in `app.py::submit`, right after the 5-word guard: refuse text with fewer than `MIN_DISTINCT_WORDS = 3` different words (`config.py`), counted with the same `stylometry.words()`. It returns a 400 with `reason: low_variety_text` and logs it like every other refusal. Nothing else moved: same signals, weights, thresholds, rate limits and the 5-word guard. I also added three lines to `check_guard.py`.

**Which diagnosis pointed at it:** the probe after the first run (see "Were my targets too easy?" above). The 5-word guard counts words, not whether the words are varied, so `asdf asdf asdf asdf asdf asdf asdf asdf` got through and the style signal read it as exactly 1.0 (the AI end) and the label came back **ai at 0.97 confidence**. Repeating one or two words is the cheapest way to clear a word count, so the fix is aimed at that mechanism and no other. I added criterion 6 to `criteria.md` and committed it (`436fa71`) before running it and before writing the fix.

**How I picked 3:** I measured before choosing. The least varied real text I have (all 31 criterion 2 texts and every attack-set text of 5 or more words) has 8 distinct words; the ten five-word boundary sentences have 5; the ten junk inputs have 1 or 2. A cutoff of 3 sits between them with room on both sides.

**Before and after, side by side** (before: criteria 1-5 from `results/capstone_run_2026-11-23_0121_before.md`, criterion 6 from `results/capstone_run_2026-11-23_0139_before_c6only.md`; after: `results/capstone_run_2026-11-23_0141_after.md`, all six, three trials each):

| Criterion | Target | Before (runs 1/2/3) | After (runs 1/2/3) | Verdict before -> after |
|---|---|---|---|---|
| 1. Junk refused, not scored | 5 of 5 | 5/5 x3 | 5/5 x3 | MET -> MET |
| 2. Real writing not refused, scores unchanged | 31 of 31 | 31/31 x3 | 31/31 x3 | MET -> MET |
| 3. Guard runs before the model | 5 of 5 under 500 ms | 5/5 x3 | 5/5 x3 (slowest 38.4 ms) | MET -> MET |
| 4. Complete record for every request | 20 of 20 | 20/20 x3 | 20/20 x3 | MET -> MET |
| 5. Boundary sits at 5 words | 20 of 20 | 20/20 x3 | 20/20 x3 | MET -> MET |
| 6. Repeated-word junk refused | 10 of 10 | **0/10 x3** | **10/10 x3** | **MISSED -> MET** |

The ten inputs of criterion 6, what came back before and after (trial 1; the other two trials were the same):

| Input | Before | After |
|---|---|---|
| `asdf asdf asdf asdf asdf asdf asdf asdf` | 200 ai (0.9713) | 400 `low_variety_text` |
| `buy now buy now buy now buy now buy now` | 200 ai (0.9726) | 400 `low_variety_text` |
| `the the the the the the` | 200 ai (0.7622) | 400 `low_variety_text` |
| `lol lol lol lol lol lol lol lol lol lol` | 200 ai (0.9785) | 400 `low_variety_text` |
| `ok ok ok ok ok ok` | 200 ai (0.8193) | 400 `low_variety_text` |
| `test test test test test test` | 200 unsure (0.5341) | 400 `low_variety_text` |
| `a b a b a b a b` | 200 ai (0.8407) | 400 `low_variety_text` |
| `1 1 1 1 1 1 1 1` | 200 ai (0.9852) | 400 `low_variety_text` |
| `12345 12345 12345 12345 12345` | 200 ai (0.9377) | 400 `low_variety_text` |
| `no no no no no no no no` | 200 ai (0.9831) | 400 `low_variety_text` |

Raw output, `run_capstone.py::c6` against `app.py::submit` (first two rows of trial 1 each):

```json
[
  {
    "text": "asdf asdf asdf asdf asdf asdf asdf asdf",
    "status": 200,
    "reason": null,
    "guess": "ai",
    "confidence": 0.9713,
    "ok": false
  },
  {
    "text": "buy now buy now buy now buy now buy now",
    "status": 200,
    "reason": null,
    "guess": "ai",
    "confidence": 0.9726,
    "ok": false
  }
]
```

```json
[
  {
    "text": "asdf asdf asdf asdf asdf asdf asdf asdf",
    "status": 400,
    "reason": "low_variety_text",
    "guess": null,
    "confidence": null,
    "ok": true
  },
  {
    "text": "buy now buy now buy now buy now buy now",
    "status": 400,
    "reason": "low_variety_text",
    "guess": null,
    "confidence": null,
    "ok": true
  }
]
```

**Did it help, and how do I know:** Yes, for exactly what it was aimed at. Before, all ten repeated-word inputs got a 200 and a verdict, nine of them "ai" and the strongest at 0.99 confidence (`1 1 1 1 1 1 1 1`, 0.9852); after, all ten are refused with a 400 and a log entry that has no scores, in every trial. Criteria 1-5 did not move in any trial, and in particular criterion 2 (all 31 real texts, scores identical to unit 8 to 4 decimals) shows the new check refused no real writing and changed no score. The trade is small and named: any text with fewer than 3 different words is now refused, so a genuine one-line reply like "No no no no no" gets a 400 instead of a label. I accept that, since there is nothing to judge in it.

**What it did not fix:** it only catches low-variety text, and I probed what is left (current code, temporary log): `asdf qwer zxcv uiop hjkl mnbv` (6 different strings) comes back **unsure** at 0.61; `a b c a b c a b c a b c` (3 different words, so it clears the cutoff) comes back **ai at 0.91**; `lorem ipsum dolor sit amet consectetur adipiscing elit` comes back **ai at 0.85**. So junk with a few different words, or junk that looks like words, still gets scored. Catching those needs a different kind of check (a dictionary or a minimum model-confidence rule), which is a bigger change than one fix. Raising the cutoff would catch `a b c a b c` but would start refusing real short messages, and I have no real short messages to measure it on.

**Stretch**

Declared before building. I'm adding two of the four:

- **A latency breakdown.** Where the time goes across the stages of one scored `/submit`: validation and the two guards, the gpt2 signal, the style signal, the phrase signal, combining and labelling, the verified-human lookup, and the log write. Measured inside the container over 30 warm runs (10 texts, 3 passes), by timing the real functions through the real route, reported as mean, median and 95th percentile per stage. Anything left over is counted as route overhead.
- **A load observation.** My "normal" rate is 10 requests per minute, which is a busy minute for the 100 people a day in What It Costs (300 requests a day is about 0.2 a minute on average, so 10 a minute is already about 50 times the average). Ten times that is 100 requests per minute. I will run 1 minute at normal and 2 minutes at 100 per minute, from 40 different `creator_id`s so the per-creator rate limit does not hide the effect, then one creator alone at 100 per minute to see the limiter. I report latency (median, 95th percentile, worst), status codes, peak memory, and whether the log has exactly one entry per request.
- **Not doing: a second measured improvement.** The first one stays the only change to the system. The leftover junk (`a b c a b c ...`, `lorem ipsum ...`) is written up in What's Still Broken instead.
- **Not doing: both run paths.** The service holds about 1.0 GB once loaded, so it cannot run on a free 512 MB host, and a hosted deploy needs a paid plan. Path B only, as the arithmetic in RUNNING.md says.

**Latency Breakdown (stretch)**

Run with `python latency_breakdown.py` inside the container (`results/latency_breakdown_2026-11-23_0658.md`). It wraps each stage function the route calls with a timer and sends 30 warm requests through the real `app.py::submit` (10 texts x 3 passes, a fresh `creator_id` each, after one uncounted warm-up request that loads the model). The audit log is a temporary copy of the real one (1,115 lines at the time), so the lookup that reads the log has a realistic file to read and the real log is untouched. It uses Flask's test client, so it leaves out HTTP; the live service adds a few more milliseconds on top of this.

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

- **gpt2 is the run.** The model signal is 126.7 ms of a 137.7 ms route, 92%. Everything else together is about 11 ms.
- **The surprise is the second row.** `audit.is_verified` costs 8.7 ms, more than the style signal, phrase signal, combining, labelling, guards and log write put together. It runs on every `/submit` only to fill in `verified_human` in the response, and it does that by reading the whole audit log. That makes it grow with the log, and I measured how fast: on the same function, 15.4 ms at 1,426 lines and 115.8 ms at 14,260 lines (host timings, 20 calls each, so higher than the container's, but the shape is the point: ten times the log, about seven and a half times the time). At ten times the log this lookup would take roughly 65 to 115 ms on these numbers, close to the model's 127 ms, and it would keep growing past it. The fix would be to look the creator up once at startup or keep verified ids in a small file, which I did not do because it is outside this unit's one change.
- **The guards I added cost nothing.** The two checks take 0.06 ms together, under 0.1% of the route, so refusing junk early is free next to scoring it (which is the 127 ms it saves).
- **Cross-check against What It Costs.** The route took 137.7 ms here against 145.6 ms on the live service earlier, which is the same figure within the spread of the runs; the live number also includes HTTP.

**Load Observation (stretch)**

Run with `python load_observation.py` against the container (`results/load_observation_2026-11-23_0202.md`). "Normal" was declared before the run as 10 requests a minute, so ten times is 100 a minute. Requests go out on a fixed schedule whether or not earlier ones have finished, so a slow service cannot slow the load down. The 40-creator phases use 40 different `creator_id`s so that the per-creator limit of 5 a minute does not hide the effect. One uncounted request loaded the model first.

| Phase | Sent | Status codes | Median ms | p95 ms | Worst ms | Completed (200) per min |
|---|---|---|---|---|---|---|
| normal (10/min) | 10 | {'200': 10} | 174.4 | 227.9 | 236.8 | 11.1 |
| 10x (100/min), 40 creators | 200 | {'200': 200} | 174.9 | 238.6 | 327.1 | 100.3 |
| 10x (100/min), one creator | 100 | {'200': 5, '429': 95} | 164.4 | 196.2 | 202.6 | 5.0 |

- Requests sent: 310. Log entries added: 310.
- Peak memory of the service (VmHWM): 959 MB before the phases, 1019 MB after.

- **Ten times normal changed almost nothing.** With 40 creators, all 200 requests returned 200 at 100.3 a minute, which is the rate I sent. Median latency was 174.9 ms against 174.4 ms at normal; the 95th percentile went from 227.9 to 238.6 ms; the worst single request went from 236.8 to 327.1 ms. No errors, no timeouts, and the log has exactly one entry per request (310 sent, 310 added, the 429s included).
- **Why nothing broke: I was nowhere near the limit.** At about 0.14 s a request, 100 a minute keeps the service about 23% busy. If requests ran strictly one at a time it could do about 1 / 0.1377 s = 7.3 a second, about 436 a minute, which is roughly 44 times my "normal". That is arithmetic, not a measurement: I stopped at ten times as declared, so I have not seen where it actually gives way.
- **The rate limiter did its job.** One creator at 100 a minute got 5 requests through and 95 429s. The 200s were unaffected (median 164.4 ms), and the 429s cost nothing to score because they are rejected before the route runs. This is the same per-creator behaviour, and the same weakness (many `creator_id`s get many allowances), as in Rate Limiting above.
- **Memory is the one thing that moved.** The service's peak memory went from 959 MB before the phases to 1,019 MB after. I ran this twice: the first run exposed a bug in my 95th-percentile calculation (on 10 samples it gave a value above the worst request), so I fixed it and discarded that run, and in that first run the peak rose to 1,204 MB. So the honest statement is that concurrent requests push the peak up by somewhere between about 60 and 250 MB, not a precise number. A host needs room for roughly 1.0 to 1.2 GB, not 1.0.
