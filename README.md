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

## Rate Limiting

**My limits:** 5 per minute, 50 per day (on `/submit`, `config.py`)

**Why those numbers and not others:** A real writer submits their own work a few times an hour, and might send a quick burst of revisions of one piece, so 5 a minute never gets in their way and 50 a day is far more than most writers produce. A script mapping my thresholds needs hundreds of variations, and scoring takes only 1-2 seconds, so with no limit it could send about 30 a minute. At 5 a minute and 50 a day it gets at most 50 probes per key per day, which is too few to map the 0.35 and 0.60 thresholds quickly. I did not go lower (3 a minute, 20 a day) because a writer revising a long essay several times could be locked out, and that is a real person being punished for the defense.

**What a caller counts as:** the `creator_id` in the request body, falling back to the IP address when there is none (`rate_limit_key` in `app.py`). The weakness: a script can rotate `creator_id` to get a fresh allowance every time, so this limits honest callers better than determined ones. Counting per IP would stop that but would lump a whole household or school together.

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

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
