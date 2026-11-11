"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria (criteria.md) needs something run against it.
`run_eval.py` runs everything here three times.

A scenario carries ONE of these:

    "texts"    a list of strings, each sent as {"text": ..., "creator_id": ...}
    "bodies"   whole request bodies, sent exactly as written (bad-input cases,
               including a body that is a bare JSON list)
    "appeals"  a list of strings: each is submitted, then appealed, and the
               appeal is checked (status, 200, exactly one log entry), plus an
               appeal on an unknown content_id (criterion 4)

Scenario names must differ in their first 12 characters: creator_ids are built
from them, and the rate limiter counts per creator_id.

⚠️ WHO WROTE WHAT. The pieces in OWN_WRITING were drafted by Claude, at the
user's request, in an informal first-person voice. They are NOT the user's own
writing, so criterion 1 here measures that text, not the user's. The AI texts
are also written by Claude. Texts marked "attack set" are copied from
attack_set/attack_set/attacks.csv at import time.
"""

import csv
from pathlib import Path

_ATTACKS = Path(__file__).parent / "attack_set" / "attack_set" / "attacks.csv"


def _attack(attack_id: str) -> str:
    """One row of the staff attack set, by id."""
    with _ATTACKS.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["id"] == attack_id:
                return row["text"]
    raise KeyError(attack_id)


# ─── Criterion 1: false positives ────────────────────────────────────────────
# Ten first-person pieces. 1, 2, 3, 8 are deliberately plain and even-toned.

OWN_WRITING = [
    # 1 (plain)
    "I started the new job on Monday. The office is about forty minutes from my "
    "flat by bus. My manager showed me around and introduced me to everyone, and "
    "I forgot most of the names straight away. The desk is by a window, which is "
    "nice. I have a laptop and a login that does not work yet. IT says it will "
    "be fixed tomorrow. I am a little nervous but mostly fine. Lunch is at one "
    "and the canteen is cheap.",
    # 2 (plain)
    "Last weekend I cleaned the kitchen. I took everything out of the cupboards "
    "and wiped the shelves. I threw away some old tins and a bag of rice that "
    "had gone off. Then I put everything back in a different order so that the "
    "things I use most are at the front. It took about three hours. The kitchen "
    "looks better now. I am going to try to keep it this way, though I know it "
    "will not last more than a week or two.",
    # 3 (plain)
    "My sister called on Sunday to ask if I could look after her cat while she "
    "is away in March. I said yes. The cat is called Biscuit and he is quiet and "
    "likes to sit on the windowsill. He eats twice a day and needs his water "
    "changed. I told her it would be no trouble. She sounded happy about it. I "
    "think I will actually enjoy having him around the flat for a week.",
    # 4
    "Okay, so the bike. I'll start with the end, which is that I walked home "
    "pushing it, one pedal hanging off, and a man outside the chip shop on Alder "
    "Road said 'rough day?' and I laughed way harder than the joke deserved. "
    "Before that I'd been doing fine, actually. Ten minutes from the canal, "
    "music in one ear, the good kind of tired. Then the bump by the bus stop. "
    "I'd like to say I saw it coming. I did not.",
    # 5
    "I still don't know why I kept the receipt. It's in the drawer under the "
    "batteries, a Tesco receipt from 14 June, for milk, bread, and a card with "
    "a cartoon hedgehog on it that I never ended up sending. Dad's birthday. I "
    "bought the card on the way to the hospital and the nurse said he was "
    "sleeping, so I sat in the car park for a while. That's the whole story, "
    "really. I'm just bad at throwing things away.",
    # 6
    "Someone should tell whoever designed our stairwell that sound travels. Last "
    "night I listened to my neighbour practise the same eight bars of a Chopin "
    "nocturne for forty minutes, and the thing is, I wasn't even annoyed by the "
    "end. She kept getting stuck on the same note. By the thirty-fifth minute I "
    "was rooting for her. When she finally got through it I clapped, alone, in "
    "my kitchen, like an idiot. Anyway. Hope she plays it again tonight.",
    # 7
    "My grandfather had a thing about tomatoes. You never put them in the "
    "fridge, you never buy the ones in plastic boxes, and you eat them with "
    "salt and nothing else, standing at the counter, like it's a secret. I "
    "thought he was just being stubborn. Then last August I bought one from a "
    "stall near the bus depot, stood at my own counter with the salt, and got "
    "it. I'm still annoyed he can't watch me do it.",
    # 8 (plain)
    "Went to the gym today for the first time in about a month. I did twenty "
    "minutes on the bike and some weights. It was harder than I remember. I was "
    "embarrassed at first because the place was busy, but nobody was paying "
    "attention to me. I will go again on Thursday. I want to be able to run for "
    "the bus without feeling like my chest is going to explode. That is the "
    "goal for now.",
    # 9
    "Not my best week. The presentation went badly, I said 'basically' about "
    "thirty times, and Priya from finance nodded along like I'd said something "
    "sensible when I really hadn't. Then on Friday the printer ate my parking "
    "ticket. I won't pretend any of this is a big deal. It's a week. But I came "
    "home and had cereal for dinner and I think that's allowed.",
    # 10
    "The thing nobody tells you about learning to drive at thirty-one is how "
    "many people have opinions about it. My uncle thinks I should have started "
    "at seventeen. My instructor, Dev, thinks I brake like I'm apologising to "
    "the car, and he might be right. Today I parallel parked on the first try "
    "and then hit the kerb pulling out, which felt about right. The test is in "
    "three weeks. I'm scared, honestly, in a way I'm not going to dress up.",
]


# ─── Criteria 2 and 3: score spread and label coverage ───────────────────────

# Five clearly-AI texts, written by Claude in a stock assistant register.
AI_TEXTS = [
    "Time management is a crucial skill that can significantly impact both "
    "personal and professional success. By prioritizing tasks effectively, "
    "individuals can reduce stress and increase productivity. Furthermore, "
    "setting clear goals provides direction and motivation. It is important to "
    "note that regular breaks also contribute to sustained focus. In conclusion, "
    "mastering time management is essential for achieving a balanced and "
    "fulfilling life.",
    "Renewable energy plays a pivotal role in addressing the challenges of "
    "climate change. Solar and wind power offer sustainable alternatives to "
    "fossil fuels, reducing greenhouse gas emissions while creating new "
    "economic opportunities. Moreover, advancements in battery technology are "
    "making these sources more reliable. Overall, the transition to renewable "
    "energy represents a significant step toward a more sustainable future for "
    "generations to come.",
    "Social media has transformed the way people communicate in the modern "
    "world. It offers numerous benefits, including enhanced connectivity, "
    "access to information, and opportunities for self-expression. However, it "
    "also presents challenges such as privacy concerns and the spread of "
    "misinformation. Ultimately, it is essential for users to engage with these "
    "platforms thoughtfully and responsibly.",
    "Regular exercise is widely recognized as one of the most effective ways to "
    "maintain good health. Engaging in physical activity strengthens the "
    "cardiovascular system, improves mood, and enhances overall well-being. "
    "Additionally, it helps to manage weight and reduce the risk of chronic "
    "diseases. Therefore, incorporating exercise into one's daily routine is a "
    "worthwhile investment in long-term health.",
    "Artificial intelligence is rapidly reshaping industries across the globe. "
    "From healthcare to finance, AI-powered tools are streamlining processes "
    "and enabling data-driven decision making. While these developments present "
    "exciting opportunities, they also raise important ethical considerations. "
    "As a result, organizations must strike a careful balance between "
    "innovation and responsibility.",
]

# Five human-style texts: two from the staff attack set (genuine human writing
# and a human editing pass), three written by Claude in an informal voice.
HUMAN_TEXTS = [
    _attack("FP01"),   # attack set: plain camping-trip account
    _attack("EV05"),   # attack set: heavily human-edited
    "My mum's rule was that nobody leaves the table until the rice is finished, "
    "which sounds fine until you're nine and the rice is cold. I once hid a "
    "spoonful in my sock. She found it three days later, by smell. We don't "
    "talk about the sock.",
    "The 7:42 was late again so I stood on platform 3 reading the sign about wet "
    "floors until it stopped meaning anything. Some guy next to me was eating "
    "cold chips out of a paper bag at eight in the morning and honestly? "
    "Respect.",
    "I told Jo I'd be there by six and I was there at seven-fifteen, with a bag "
    "of satsumas as an apology, which is a bad apology, but it was all the shop "
    "by the station had left. She ate four of them. So I think we're fine.",
]

# Ten more spread across the range, so all three labels have a chance.
MIXED_TEXTS = [
    _attack("EV01"),   # AI text with typos
    _attack("EV03"),   # AI text with a pasted human quotation
    _attack("EV09"),   # AI text with a human opening bolted on
    _attack("FP02"),   # formal human report
    _attack("FP03"),   # careful non-native writer
    _attack("FP05"),   # technical documentation
    _attack("FP08"),   # very short human line
    # A borderline piece: casual opening, stock-phrase middle.
    "So I've been meaning to write this up. Remote work has changed how teams "
    "collaborate. It is important to note that clear communication remains "
    "essential for success, and regular check-ins can help. Honestly though, "
    "half of my meetings could have been a message.",
    # A short, plain, factual note.
    "The library closes at six on weekdays and at four on Saturdays. It is "
    "closed on Sundays. Books can be borrowed for three weeks and renewed once "
    "online. Fines are charged for late returns.",
    # A messy human voice note, transcribed.
    "um, so, the thing with the landlord is he said Tuesday but it's Thursday "
    "now and nobody's come, and the tap's still doing that drip thing, "
    "ugh, I'll just ring him again tomorrow I guess",
]


SCENARIOS = [
    {
        "name": "own writing",          # criterion 1
        "criterion": 1,
        "texts": OWN_WRITING,
    },
    {
        "name": "spread - AI",          # criterion 2, AI half
        "criterion": 2,
        "texts": AI_TEXTS,
    },
    {
        "name": "spread - human",       # criterion 2, human half
        "criterion": 2,
        "texts": HUMAN_TEXTS,
    },
    {
        "name": "coverage",             # criterion 3: 20 texts in all
        "criterion": 3,
        "texts": AI_TEXTS + HUMAN_TEXTS + MIXED_TEXTS,
    },
    {
        "name": "appeal path",          # criterion 4: needs submit then appeal
        "criterion": 4,
        "appeals": OWN_WRITING,
    },
    {
        "name": "bad input",            # criterion 5
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing"},                       # no text
            {"text": "", "creator_id": "eval_bad_empty"},             # empty text
            {"text": "x" * 20000, "creator_id": "eval_bad_huge"},     # too long
            ["text", "creator_id"],                                   # bare list
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is exempt from the empty check — an empty string is the
    whole point of a bad-input case — and may hold a bare list as well as a
    dict, because "the body isn't an object" is itself one of the cases.
    """
    problems = []
    seen = {}
    for i, scenario in enumerate(SCENARIOS, 1):
        name = scenario.get("name")
        if not name:
            problems.append(f"scenario {i} has no name")
        else:
            prefix = name[:12]
            if prefix in seen:
                problems.append(
                    f"scenario {i} ('{name}') shares its first 12 characters with "
                    f"'{seen[prefix]}', so their creator_ids collide"
                )
            seen[prefix] = name

        kinds = [k for k in ("texts", "bodies", "appeals") if scenario.get(k)]
        if len(kinds) > 1:
            problems.append(
                f"scenario {i} ('{name}') has {' and '.join(kinds)} — pick one"
            )
            continue
        if not kinds:
            problems.append(f"scenario {i} has no texts, bodies or appeals")
            continue

        kind = kinds[0]
        if kind == "bodies":
            for j, body in enumerate(scenario["bodies"], 1):
                if not isinstance(body, (dict, list)):
                    problems.append(
                        f"scenario {i}, body {j} is neither a dict nor a list — "
                        f"bodies are whole request bodies"
                    )
            continue

        for j, text in enumerate(scenario[kind], 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is "
                    f"what you're testing, use 'bodies' instead"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(f"scenario {i} ('{name}'), text {j} is still the placeholder")
    return problems
