# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 01:51
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `8df67285-4c0d-47b7-8425-0edea22d8e8c` | human | 0.689 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `58a67638-0283-414a-a84d-8aaadc96997c` | unsure | 0.519 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `af62276c-3d05-4d73-ac09-fc72237a683a` | unsure | 0.565 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `64e32cd8-b382-4695-ad86-342687f479e2` | unsure | 0.577 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `964cc2fd-32f9-441b-819f-d3f86560138c` | human | 0.688 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `3a6528e3-afbf-4d1c-99b1-907f073158e9` | unsure | 0.542 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `32fa0b7f-a27f-430f-8353-7fe7c7ba4728` | ai | 0.669 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `30bc32c5-9259-4b08-bc37-693b0c1c0d1e` | unsure | 0.640 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `554452b8-f981-4133-95c8-7c53b64c3a9b` | unsure | 0.574 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `64dabe6a-71d0-4498-81a5-029f3484d734` | ai | 0.912 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `f01db45b-e240-42d7-a8a7-e07e63a711b8` | unsure | 0.584 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `e34d0f4e-52a3-42a3-830b-26b88152b5a4` | ai | 0.703 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `64a15474-a2ea-4756-ad81-ac5ffecebdfd` | ai | 0.735 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `f1df1488-c80a-49c0-813d-2819522a4685` | ai | 0.781 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `b24c0eb1-d94f-468a-8681-e3f9cf6e8dfd` | ai | 0.753 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `72c6c74b-d424-4d4e-8c59-4de931622561` | ai | 0.727 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `314ced19-9cfb-4a14-895e-38b80dddfdf0` | ai | 0.750 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `b06b35a2-0e82-4870-99a2-d697e8181aad` | unsure | 0.622 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `5151b5d9-e73c-4ae5-87d9-3d2749550e7e` | unsure | 0.582 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `cad3aa51-cce8-4f7a-b022-3d69155453de` | human | 0.774 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `466478eb-3522-4a21-bb0c-a38816a94173` | unsure | 0.542 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `636283fb-705d-4958-b34d-0fd63a583f5c` | unsure | 0.534 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `000769ba-7bcf-4b34-8df0-b3cdd09c19eb` | unsure | 0.536 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `5fa7a7de-65c4-428f-bc12-a69fb763a7f5` | unsure | 0.552 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `180b52db-1fda-4335-a49f-26de940a2842` | unsure | 0.617 |  |
| MF04 | malformed | text is only punctuation | 200 | `4760931c-51c8-4a9a-9f92-248c00365b7b` | unsure | 0.547 |  |
| MF05 | malformed | text is a very long single word | 200 | `2536a656-a3d1-42cc-91a3-48e1f7454093` | ai | 0.865 |  |
| MF06 | malformed | text is emoji only | 200 | `493681c4-b61d-4960-946d-09439757ae7e` | ai | 0.998 |  |
| MF07 | malformed | text is right-to-left script | 200 | `fc2b00b5-edd1-4cc4-b070-ad14cbe8a988` | ai | 0.944 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `19b519fd-5b26-4a15-b8af-dfac8c34c235` | unsure | 0.608 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0f14ee71-7ead-487b-8f3f-6892b63de9ca` | unsure | 0.608 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `db5669d8-6e40-4f26-a87a-6702bd79b4da` | unsure | 0.608 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0a9ad3a0-7594-4812-8c3d-c651236dcc0f` | unsure | 0.608 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `537c6b4b-4d9b-4bcb-a2a4-4cf593168dfa` | unsure | 0.608 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "8df67285-4c0d-47b7-8425-0edea22d8e8c",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.6894,
  "model_score": 0.1635,
  "style_score": 0.5313,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "58a67638-0283-414a-a84d-8aaadc96997c",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5192,
  "model_score": 0.5943,
  "style_score": 0.3106,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "af62276c-3d05-4d73-ac09-fc72237a683a",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5645,
  "model_score": 0.6662,
  "style_score": 0.4119,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "64e32cd8-b382-4695-ad86-342687f479e2",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5768,
  "model_score": 0.6114,
  "style_score": 0.5249,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "964cc2fd-32f9-441b-819f-d3f86560138c",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.6883,
  "model_score": 0.3212,
  "style_score": 0.2974,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "3a6528e3-afbf-4d1c-99b1-907f073158e9",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5423,
  "model_score": 0.5727,
  "style_score": 0.3609,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "32fa0b7f-a27f-430f-8353-7fe7c7ba4728",
  "creator_id": "attacker_EV07",
  "guess": "ai",
  "confidence": 0.6689,
  "model_score": 0.5862,
  "style_score": 0.4179,
  "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "30bc32c5-9259-4b08-bc37-693b0c1c0d1e",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.6401,
  "model_score": 0.2452,
  "style_score": 0.532,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "554452b8-f981-4133-95c8-7c53b64c3a9b",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5743,
  "model_score": 0.7042,
  "style_score": 0.3794,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "64dabe6a-71d0-4498-81a5-029f3484d734",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9125,
  "model_score": 0.9792,
  "style_score": 0.8124,
  "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "f01db45b-e240-42d7-a8a7-e07e63a711b8",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5838,
  "model_score": 0.6175,
  "style_score": 0.5332,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "e34d0f4e-52a3-42a3-830b-26b88152b5a4",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7029,
  "model_score": 0.7387,
  "style_score": 0.6493,
  "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "64a15474-a2ea-4756-ad81-ac5ffecebdfd",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7345,
  "model_score": 0.8051,
  "style_score": 0.6285,
  "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "f1df1488-c80a-49c0-813d-2819522a4685",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7813,
  "model_score": 0.8329,
  "style_score": 0.5202,
  "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "b24c0eb1-d94f-468a-8681-e3f9cf6e8dfd",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7526,
  "model_score": 0.8005,
  "style_score": 0.6808,
  "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "72c6c74b-d424-4d4e-8c59-4de931622561",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7269,
  "model_score": 0.8814,
  "style_score": 0.4951,
  "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "314ced19-9cfb-4a14-895e-38b80dddfdf0",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7501,
  "model_score": 0.8816,
  "style_score": 0.5529,
  "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "b06b35a2-0e82-4870-99a2-d697e8181aad",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.6224,
  "model_score": 0.3223,
  "style_score": 0.4605,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "5151b5d9-e73c-4ae5-87d9-3d2749550e7e",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.5821,
  "model_score": 0.4625,
  "style_score": 0.3511,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "cad3aa51-cce8-4f7a-b022-3d69155453de",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.7744,
  "model_score": 0.2044,
  "style_score": 0.2575,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "466478eb-3522-4a21-bb0c-a38816a94173",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5417,
  "model_score": 0.5943,
  "style_score": 0.4629,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "636283fb-705d-4958-b34d-0fd63a583f5c",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.534,
  "model_score": 0.4998,
  "style_score": 0.4154,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "000769ba-7bcf-4b34-8df0-b3cdd09c19eb",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5362,
  "model_score": 0.6401,
  "style_score": 0.1089,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "5fa7a7de-65c4-428f-bc12-a69fb763a7f5",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5523,
  "model_score": 0.5583,
  "style_score": 0.5432,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "180b52db-1fda-4335-a49f-26de940a2842",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.6167,
  "model_score": 0.0,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "4760931c-51c8-4a9a-9f92-248c00365b7b",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.5466,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "2536a656-a3d1-42cc-91a3-48e1f7454093",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8652,
  "model_score": 0.9976,
  "style_score": 0.6667,
  "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "493681c4-b61d-4960-946d-09439757ae7e",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9981,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "fc2b00b5-edd1-4cc4-b070-ad14cbe8a988",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9438,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "This looks like it was written by an AI. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "19b519fd-5b26-4a15-b8af-dfac8c34c235",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.608,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "0f14ee71-7ead-487b-8f3f-6892b63de9ca",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.608,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "db5669d8-6e40-4f26-a87a-6702bd79b4da",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.608,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "0a9ad3a0-7594-4812-8c3d-c651236dcc0f",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.608,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "537c6b4b-4d9b-4bcb-a2a4-4cf593168dfa",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.608,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
