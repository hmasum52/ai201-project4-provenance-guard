# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives stay rare

Of 10 pieces I wrote myself, at least 3 of them written plainly, at most 1 is
labelled high-confidence AI, in each of 3 trials.

**Why this target:** On a writing site a wrong accusation costs a real person
far more than a missed detection costs the site. The plain-writing pieces are
included on purpose, because plain human writing is the known blind spot of the
model signal.

---

## 2. Clearly-AI and clearly-human text score apart

Over 5 clearly-AI and 5 clearly-human texts, the mean combined score of the AI
set is at least 0.30 above the mean of the human set, in each of 3 trials.

**Why this target:** 0.30 is about one label band. If the two sets sit closer
than that, the signals aren't telling them apart and the labels are noise.

---

## 3. Every label is reachable

Across a set of 20 texts, each of the three labels (high-confidence human,
unsure, high-confidence AI) is produced at least once, in each of 3 trials.

**Why this target:** A label no score can produce means a gap in the ranges, so
a reader would never see it. It is also an easy mistake to make while the style
signal is still a stub.

---

## 4. Appeals always change status and always get recorded

10 of 10 appeals on valid `content_id`s return 200, set the status to
`under_review` and add exactly one appeal entry to the log. An appeal on an
unknown `content_id` returns 404 and adds no appeal entry.

**Why this target:** The appeal is the only recourse a wrongly accused writer
has, so it must never fail silently. 10 of 10 because there is no acceptable
rate of lost appeals.

---

## 5. Bad input gets a 400, never a crash

4 of 4 bad bodies sent to `/submit` return 400 and never 500: missing `text`,
empty `text`, a 20,000-character `text`, and a body that is JSON but not an
object (a bare list).

**Why this target:** A crash on malformed input is one of the most common real
failures, and unit 8's attack set will probe it. 4 of 4 because each case is a
single deterministic check.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Capstone criteria

Written before building the extension and before any capstone results exist. The extension is the minimum-evidence guard on `POST /submit` (fewer than 5 words from `stylometry.words()` gets a 400 before any signal runs). The five above are the unit 7 criteria and are left untouched.

## 1. Junk is refused, not scored

All 5 junk attacks (MF03 control characters, MF04 punctuation only, MF05 one very long word, MF06 emoji only, MF07 right-to-left script) return 400. The log entry for each shows `reason: not_enough_text` and has no `model_score` or `style_score`. 5 of 5, in each of 3 trials.

**Why this target:** The check is a deterministic word count, so there is no noise to allow for. A single miss is a confident "ai" label at 0.87-0.99 on text that isn't writing.

## 2. Real writing is not refused, and nothing it scored before changes

Over the 20 coverage texts, the 10 plain pieces and EV08 (31 texts), 0 return 400, and each `combined_score` equals the one in `results/run_2026-11-11_0215_after.md` to 4 decimals, in each of 3 trials.

**Why this target:** The guard must not become a new false accusation, and the original system has to still work. Scoring is deterministic, so any difference at all is a regression, not noise.

## 3. The guard runs before the model

On a freshly started service where `GET /health` reports `detector_loaded: false`, all 5 junk inputs return within 500 ms, and `detector_loaded` is still `false` afterwards. 5 of 5, in each of 3 trials (restart between trials).

**Why this target:** Loading the model takes 10+ seconds, so a refusal slower than 500 ms means the guard is not ahead of it. It would also mean junk input can force a model load.

## 4. Every request leaves a complete record, including refusals

Send 20 requests: 10 scored, 5 junk and 5 other bad inputs. Each one leaves exactly one log entry with `timestamp`, `input` (first 200 characters), `outcome` and `duration_ms` all present and non-null, and the log grows by exactly 20. 20 of 20, in each of 3 trials.

**Why this target:** A failure that shows up only as a missing log line cannot be found afterwards. 20 of 20 because a log that is complete most of the time cannot be trusted to explain any one request.

## 5. The boundary sits where I said it does

10 pairs of texts, each pair the same sentence at 4 words and at 5 words. All ten 4-word texts return 400 and all ten 5-word texts return 200. 20 of 20, in each of 3 trials.

**Why this target:** "Fewer than five" is a number I chose and wrote in the README, and this tests it behaves as stated. An off-by-one would silently refuse real writers, or let junk through.
