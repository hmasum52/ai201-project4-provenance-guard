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

The clearly-AI and clearly-human texts sit 0.32 apart. "Clearly AI" scored 0.640, just under my first AI threshold of 0.65, so that label was unreachable on it. In Milestone 5 I lowered `AI_THRESHOLD` to 0.60 (in `config.py`). The cost: a few more borderline texts, including plain human writing, will now cross into the AI label. The unsure band shrank from 0.35–0.65 to 0.35–0.60, so I'm trading some protection for writers for a reachable AI label.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. |
| unsure | 0.35 – 0.60 | We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look. |
| high-confidence AI | 0.60 – 1.00 | This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it. |

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

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



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
