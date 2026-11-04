"""
Signal two: the style signal.

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures ───────────────────────────────────────────────────────
# Direction of each raw measure: HIGHER = MORE HUMAN. style_signal flips them.

def sentence_length_spread(text: str) -> float:
    """
    Coefficient of variation of sentence length (stdev / mean, in words).
    Higher = lumpier = more human. Typical: ~0.2 even/AI-like, ~0.7+ lumpy.

    Fewer than two sentences has no spread, so it returns 0.0 — the AI-like
    end. A one-sentence submission therefore leans "AI" on this measure.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    return statistics.stdev(lengths) / statistics.mean(lengths)


def type_token_ratio(text: str) -> float:
    """Unique words / total words, 0–1. Higher = more varied. 0.0 if no words."""
    w = words(text)
    return len(set(w)) / len(w) if w else 0.0


def punctuation_density(text: str) -> float:
    """
    Commas, semicolons, colons and dashes per word. Higher = more human.
    Full stops are left out: every writer uses them. Semicolons and dashes
    vary the most between writers, so they carry the signal.
    """
    w = words(text)
    if not w:
        return 0.0
    marks = len(re.findall(r"[,;:—–]|--|\s-\s", text))
    return marks / len(w)


# ── Combining them ───────────────────────────────────────────────────────────

# The raw value at which each measure reads as "fully human" (score 0.0).
# At or below the floor it reads fully AI (1.0). Rough guesses, tune in M4.
SPREAD_HUMAN = 0.7    # sentence-length CV
TTR_FLOOR = 0.4       # type-token ratio that reads fully AI
TTR_HUMAN = 0.9       # type-token ratio that reads fully human
PUNCT_HUMAN = 0.15    # marks per word


def _ai_score(value: float, human_at: float, ai_at: float = 0.0) -> float:
    """Linear map: ai_at -> 1.0 (AI-like), human_at -> 0.0, clamped."""
    t = (value - ai_at) / (human_at - ai_at)
    return 1.0 - min(max(t, 0.0), 1.0)


def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Each raw measure is higher-is-more-human, so each is flipped onto an
    AI-score and the three are averaged with equal weight:

        spread      0.0 -> 1.0 (AI),  >= 0.7  -> 0.0
        TTR         <= 0.4 -> 1.0,    >= 0.9  -> 0.0
        punctuation 0.0 -> 1.0,       >= 0.15 -> 0.0
    """
    parts = [
        _ai_score(sentence_length_spread(text), SPREAD_HUMAN),
        _ai_score(type_token_ratio(text), TTR_HUMAN, TTR_FLOOR),
        _ai_score(punctuation_density(text), PUNCT_HUMAN),
    ]
    return round(sum(parts) / len(parts), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
