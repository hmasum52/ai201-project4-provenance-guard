# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 02:13
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `97ef0771-3eda-4890-9d86-4a37cdd4a08c` | human | 0.689 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `8e520b5a-945d-4559-9cf9-86ecebc51a01` | unsure | 0.519 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `74c7984a-6a6c-4e9a-84d4-89b3b7bd7bdf` | unsure | 0.565 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `7e494c79-10aa-44ea-a4ba-1a6f46889eea` | unsure | 0.577 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `5172c75f-e347-4afc-a263-4630ec715172` | human | 0.688 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c0fdb82b-707d-4416-ac6d-b5d6389f906f` | unsure | 0.542 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `e444dd77-cb20-4ab8-b407-402640136ae7` | unsure | 0.669 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `554ebfaa-913e-428f-8ed6-a9b5d302807b` | unsure | 0.640 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `7447d350-b9c9-447b-a5f8-f635b2863ddf` | unsure | 0.574 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `ab6faf16-eec5-46a5-817e-bc61ee6a9bef` | ai | 0.912 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `16c7b8dd-3396-47fa-bcd3-2b90d51124c0` | unsure | 0.584 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `f4492f63-cc67-48aa-8252-2eed3cf8e90e` | unsure | 0.703 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `43f611f8-a10e-4fa6-ba96-4b2f2d1f99c9` | unsure | 0.735 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `85172eb3-9c20-42de-b30f-7e8cce33d278` | ai | 0.781 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `9304fc76-bd35-49e4-9afb-bbba5e0f6fcd` | ai | 0.753 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `12cf265d-64ad-4f10-97e8-ad968559e3c6` | unsure | 0.727 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `3d6c8a8b-7647-43da-a2aa-9163372de87b` | ai | 0.750 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `ecd20b6f-d8c4-483c-989d-cb20dbff3aaa` | unsure | 0.622 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `4e8cf910-64e1-40da-9ac9-805326ee5992` | unsure | 0.582 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c5b77a7f-78cf-4c32-9f58-f8763dad8266` | human | 0.774 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `a386e0eb-003d-4048-b4dd-23e7d284e655` | unsure | 0.542 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `85fa7ae7-157a-4652-94ad-d2b06c5d8893` | unsure | 0.534 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `58d29d06-4fcb-4221-9d5f-cbd89cb2f8cd` | unsure | 0.536 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `bda3804a-666e-4fba-ae17-2d992780bc55` | unsure | 0.552 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `a693f8fc-7cb4-458c-a153-249cc0febccd` | unsure | 0.617 |  |
| MF04 | malformed | text is only punctuation | 200 | `8277b8f3-d45f-47ba-8aaa-d1b5aa0ba39a` | unsure | 0.547 |  |
| MF05 | malformed | text is a very long single word | 200 | `eca4e995-00cc-408b-898b-24d0a1388ff6` | ai | 0.865 |  |
| MF06 | malformed | text is emoji only | 200 | `2263d2d9-894f-4fbc-95a3-a4de31842a1e` | ai | 0.998 |  |
| MF07 | malformed | text is right-to-left script | 200 | `10bf045b-9264-4879-9961-42e38215db1e` | ai | 0.944 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a1d8323a-acd3-4a3b-a936-0109f458147c` | unsure | 0.608 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5e857288-68ca-4b15-abfb-60e3d68a79c2` | unsure | 0.608 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2a89c18d-834d-4e0c-825e-5883a0c2dc90` | unsure | 0.608 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4d7720f0-8168-4d8f-9949-cf3e1ca0973b` | unsure | 0.608 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9f03f36b-9e11-4487-9fdd-b7f979fb50f8` | unsure | 0.608 |  |
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
  "content_id": "97ef0771-3eda-4890-9d86-4a37cdd4a08c",
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
  "content_id": "8e520b5a-945d-4559-9cf9-86ecebc51a01",
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
  "content_id": "74c7984a-6a6c-4e9a-84d4-89b3b7bd7bdf",
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
  "content_id": "7e494c79-10aa-44ea-a4ba-1a6f46889eea",
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
  "content_id": "5172c75f-e347-4afc-a263-4630ec715172",
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
  "content_id": "c0fdb82b-707d-4416-ac6d-b5d6389f906f",
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
  "content_id": "e444dd77-cb20-4ab8-b407-402640136ae7",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.6689,
  "model_score": 0.5862,
  "style_score": 0.4179,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
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
  "content_id": "554ebfaa-913e-428f-8ed6-a9b5d302807b",
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
  "content_id": "7447d350-b9c9-447b-a5f8-f635b2863ddf",
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
  "content_id": "ab6faf16-eec5-46a5-817e-bc61ee6a9bef",
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
  "content_id": "16c7b8dd-3396-47fa-bcd3-2b90d51124c0",
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
  "content_id": "f4492f63-cc67-48aa-8252-2eed3cf8e90e",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.7029,
  "model_score": 0.7387,
  "style_score": 0.6493,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
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
  "content_id": "43f611f8-a10e-4fa6-ba96-4b2f2d1f99c9",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.7345,
  "model_score": 0.8051,
  "style_score": 0.6285,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
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
  "content_id": "85172eb3-9c20-42de-b30f-7e8cce33d278",
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
  "content_id": "9304fc76-bd35-49e4-9afb-bbba5e0f6fcd",
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
  "content_id": "12cf265d-64ad-4f10-97e8-ad968559e3c6",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.7269,
  "model_score": 0.8814,
  "style_score": 0.4951,
  "label": "We can't tell whether a person or an AI wrote this. If it's yours, you can appeal and ask a person to look.",
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
  "content_id": "3d6c8a8b-7647-43da-a2aa-9163372de87b",
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
  "content_id": "ecd20b6f-d8c4-483c-989d-cb20dbff3aaa",
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
  "content_id": "4e8cf910-64e1-40da-9ac9-805326ee5992",
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
  "content_id": "c5b77a7f-78cf-4c32-9f58-f8763dad8266",
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
  "content_id": "a386e0eb-003d-4048-b4dd-23e7d284e655",
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
  "content_id": "85fa7ae7-157a-4652-94ad-d2b06c5d8893",
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
  "content_id": "58d29d06-4fcb-4221-9d5f-cbd89cb2f8cd",
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
  "content_id": "bda3804a-666e-4fba-ae17-2d992780bc55",
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
  "content_id": "a693f8fc-7cb4-458c-a153-249cc0febccd",
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
  "content_id": "8277b8f3-d45f-47ba-8aaa-d1b5aa0ba39a",
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
  "content_id": "eca4e995-00cc-408b-898b-24d0a1388ff6",
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
  "content_id": "2263d2d9-894f-4fbc-95a3-a4de31842a1e",
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
  "content_id": "10bf045b-9264-4879-9961-42e38215db1e",
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
  "content_id": "a1d8323a-acd3-4a3b-a936-0109f458147c",
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
  "content_id": "5e857288-68ca-4b15-abfb-60e3d68a79c2",
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
  "content_id": "2a89c18d-834d-4e0c-825e-5883a0c2dc90",
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
  "content_id": "4d7720f0-8168-4d8f-9949-cf3e1ca0973b",
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
  "content_id": "9f03f36b-9e11-4487-9fdd-b7f979fb50f8",
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
