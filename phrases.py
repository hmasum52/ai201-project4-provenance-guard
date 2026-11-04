"""
Signal three: the stock-phrase signal.

Counts filler phrases that generated prose leans on ("it is important to
note", "furthermore", "plays a crucial role"). Higher means more likely AI.

It can only ever ADD suspicion: a text with none of these phrases is not
evidence of a person, so a score of 0.0 means "no evidence", not "human".
`scoring.combine_signals` uses it that way.

⚠️ Blind spot: it reads a word list, nothing more. Anyone can strip the phrases
out of AI text, and a formal human writer who says "furthermore" gets nudged
toward AI for it.

    python phrases.py "some text to look at"
"""

import re

STOCK_PHRASES = [
    "it is important to note",
    "it is worth noting",
    "in conclusion",
    "furthermore",
    "additionally",
    "moreover",
    "plays a crucial role",
    "plays a vital role",
    "a wide variety of",
    "in today's fast-paced world",
    "delve into",
    "navigate the complexities",
    "it is essential to",
    "significantly enhance",
    "overall productivity",
]

# Hits per 100 words at which the signal reaches 1.0.
SATURATION_RATE = 3.0


def phrase_signal(text: str) -> float:
    """0–1 score, higher = more stock phrases per 100 words."""
    lowered = text.lower()
    word_count = len(re.findall(r"[a-z0-9']+", lowered))
    if word_count == 0:
        return 0.0
    hits = sum(lowered.count(p) for p in STOCK_PHRASES)
    rate = hits / word_count * 100
    return round(min(rate / SATURATION_RATE, 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "In conclusion, it is important to note that communication plays a "
        "crucial role. Furthermore, teams benefit."
    )
    print(f"phrase_signal   {phrase_signal(text)}   (higher = more likely AI)")
