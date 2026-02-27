#!/usr/bin/env python3
"""
prompt_builder.py — Build-A-Prompt CLI
--------------------------------------
Usage:
  python prompt_builder.py          # interactive mode
  python prompt_builder.py --test   # run test suite
"""

from __future__ import annotations

import re
import sys
import subprocess
from dataclasses import dataclass, field


# ── TRAITS ──────────────────────────────────────────────────────────────────

TRAITS: dict[str, list[str]] = {
    "code": [
        "code", "function", "script", "implement", "program", "class",
        "method", "refactor", "algorithm", "api", "module", "library",
        "python", "javascript", "typescript", "sql", "backend", "frontend",
    ],
    "debug": [
        "debug", "fix", "error", "broken", "issue", "crash", "traceback",
        "exception", "fails", "not working", "wrong output", "why is",
        "investigate", "diagnose",
    ],
    "write": [
        "write", "draft", "article", "essay", "blog", "post", "email",
        "letter", "copy", "content", "paragraph", "prose", "report",
        "document", "announcement",
    ],
    "analyze": [
        "analyze", "analysis", "evaluate", "compare", "assess", "review",
        "examine", "investigate", "breakdown", "pros and cons", "trade-off",
        "critique", "study", "audit",
    ],
    "explain": [
        "explain", "what is", "how does", "describe", "summarize",
        "definition", "clarify", "overview", "introduction", "basics",
        "understand", "eli5", "simple terms", "meaning of",
    ],
    "creative": [
        "creative", "story", "poem", "fiction", "imagine", "brainstorm",
        "ideas", "invent", "generate", "concept", "narrative", "character",
        "plot", "metaphor", "slogan", "tagline",
    ],
    "data": [
        "data", "dataset", "csv", "table", "chart", "visualize", "metrics",
        "statistics", "numbers", "rows", "columns", "aggregate", "filter",
        "sort", "plot", "pandas", "excel", "spreadsheet",
    ],
    "teach": [
        "teach", "tutorial", "lesson", "course", "step by step", "guide",
        "learn", "beginner", "walkthrough", "exercise", "practice",
        "quiz", "explain to", "how to", "primer",
    ],
}


# ── CONSTRAINT DATACLASS & CATALOG ──────────────────────────────────────────

@dataclass
class Constraint:
    key: str
    label: str
    description: str
    group: str
    boosted_by: list[str]


CONSTRAINTS: list[Constraint] = [
    # FORMAT
    Constraint("fmt_code_blocks", "Use code blocks",
               "Wrap all code in fenced ``` blocks with language tags",
               "format", ["code", "debug"]),
    Constraint("fmt_bullet_list", "Respond in bullet points",
               "Use concise bullet points rather than prose paragraphs",
               "format", ["analyze", "data", "explain"]),
    Constraint("fmt_numbered", "Use numbered steps",
               "Present information as an ordered, numbered sequence",
               "format", ["teach", "debug", "code"]),
    Constraint("fmt_table", "Use a table",
               "Structure comparative or multi-field data in a Markdown table",
               "format", ["data", "analyze"]),
    Constraint("fmt_headers", "Use section headers",
               "Divide response into labeled H2/H3 sections",
               "format", ["write", "teach", "analyze"]),

    # TONE
    Constraint("tone_formal", "Formal / professional tone",
               "Use precise, business-appropriate language",
               "tone", ["write", "analyze"]),
    Constraint("tone_casual", "Casual / conversational tone",
               "Write as if talking to a peer, relaxed register",
               "tone", ["creative", "explain", "teach"]),
    Constraint("tone_technical", "Technical / precise tone",
               "Use domain-specific terminology; assume expert reader",
               "tone", ["code", "debug", "data"]),
    Constraint("tone_encouraging", "Encouraging / supportive tone",
               "Frame feedback positively; motivate the reader",
               "tone", ["teach"]),

    # LENGTH
    Constraint("len_concise", "Keep it concise (< 200 words)",
               "Prioritize brevity; cut filler",
               "length", ["explain", "debug"]),
    Constraint("len_detailed", "Be thorough and detailed",
               "Cover edge cases and nuance; do not truncate",
               "length", ["code", "analyze", "data", "teach"]),
    Constraint("len_one_para", "Single paragraph only",
               "Entire answer must fit in one cohesive paragraph",
               "length", ["write", "creative"]),

    # AUDIENCE
    Constraint("aud_beginner", "Assume beginner audience",
               "No jargon; define terms; build from first principles",
               "audience", ["teach", "explain"]),
    Constraint("aud_expert", "Assume expert audience",
               "Skip basics; use shorthand; reference advanced concepts",
               "audience", ["code", "debug", "data", "analyze"]),
    Constraint("aud_nontechnical", "Assume non-technical audience",
               "Use analogies; avoid implementation details",
               "audience", ["explain", "write", "creative"]),

    # STYLE
    Constraint("sty_examples", "Include concrete examples",
               "Every claim or rule should have at least one example",
               "style", ["teach", "explain", "code"]),
    Constraint("sty_caveats", "Call out caveats and edge cases",
               "Proactively flag limitations, exceptions, gotchas",
               "style", ["debug", "analyze", "code"]),
    Constraint("sty_no_fluff", "No preamble or filler",
               "Start with the answer; skip restating the question",
               "style", ["code", "debug", "data"]),
    Constraint("sty_chain_thought", "Show reasoning / think step by step",
               "Expose intermediate reasoning before giving the answer",
               "style", ["analyze", "debug", "data"]),
    Constraint("sty_analogies", "Use analogies",
               "Explain concepts through comparisons to familiar things",
               "style", ["explain", "teach", "creative"]),
]


# ── STATE ────────────────────────────────────────────────────────────────────

@dataclass
class PromptState:
    goal: str = ""
    selected_constraints: list[Constraint] = field(default_factory=list)
    context: str = ""

    def is_complete(self) -> bool:
        return bool(self.goal.strip())


# ── CORE LOGIC (pure functions) ──────────────────────────────────────────────

def score_traits(goal: str) -> dict[str, int]:
    """Map goal text to trait hit-counts via keyword matching."""
    normalized = goal.lower()
    tokens = set(re.findall(r'\b\w+\b', normalized))
    scores: dict[str, int] = {trait: 0 for trait in TRAITS}
    for trait, keywords in TRAITS.items():
        for kw in keywords:
            if ' ' in kw:
                if kw in normalized:
                    scores[trait] += 1
            else:
                if kw in tokens:
                    scores[trait] += 1
    return scores


def score_constraints(
    trait_scores: dict[str, int],
    constraints: list[Constraint],
) -> list[tuple[Constraint, int]]:
    """Compute weight per constraint; return sorted descending (stable)."""
    weighted = [
        (c, sum(trait_scores.get(t, 0) for t in c.boosted_by))
        for c in constraints
    ]
    weighted.sort(key=lambda x: x[1], reverse=True)
    return weighted


def partition_constraints(
    scored: list[tuple[Constraint, int]],
) -> tuple[list[Constraint], list[Constraint]]:
    """Split into suggested (weight > 0) and other (weight == 0)."""
    suggested = [c for c, w in scored if w > 0]
    other = [c for c, w in scored if w == 0]
    return suggested, other


def parse_selection(
    raw: str, max_index: int
) -> tuple[list[int], str | None]:
    """
    Parse comma-separated 1-based integers.
    Returns (0-based indices, error_or_None).
    Empty string is valid (skip).
    """
    raw = raw.strip()
    if not raw:
        return [], None
    parts = [p.strip() for p in raw.split(',')]
    indices: list[int] = []
    for p in parts:
        if not p.isdigit():
            return [], f"Invalid input: '{p}' is not a number"
        n = int(p)
        if n < 1 or n > max_index:
            return [], f"Invalid selection: {n} (valid range is 1\u2013{max_index})"
        idx = n - 1
        if idx not in indices:
            indices.append(idx)
    return indices, None


def assemble_prompt(state: PromptState) -> str:
    """Deterministically assemble the final prompt string."""
    constraints_block = (
        "\n".join(
            f"  - {c.label}: {c.description}"
            for c in state.selected_constraints
        )
        if state.selected_constraints
        else "  (none selected)"
    )
    context_block = (
        f"\nContext:\n  {state.context.strip()}"
        if state.context.strip()
        else ""
    )
    return (
        f"Goal:\n  {state.goal.strip()}\n\n"
        f"Constraints:\n{constraints_block}"
        f"{context_block}"
    ).rstrip()


# ── UI HELPERS ───────────────────────────────────────────────────────────────

_IS_TTY = sys.stdout.isatty()

_ANSI = {
    "bold":   "\033[1m",
    "dim":    "\033[2m",
    "green":  "\033[32m",
    "cyan":   "\033[36m",
    "yellow": "\033[33m",
    "red":    "\033[31m",
    "reset":  "\033[0m",
}


def _c(text: str, *codes: str) -> str:
    if not _IS_TTY:
        return text
    prefix = "".join(_ANSI.get(c, "") for c in codes)
    return f"{prefix}{text}{_ANSI['reset']}"


def hr(width: int = 60, char: str = "\u2500") -> str:
    return char * width


def print_constraint_menu(
    suggested: list[Constraint], other: list[Constraint]
) -> None:
    all_items = suggested + other
    group_width = 8  # for [format] [tone] etc.

    def fmt_item(n: int, c: Constraint) -> None:
        num = _c(f"{n:>2}.", "bold")
        grp = _c(f"[{c.group}]", "dim")
        lbl = _c(c.label, "cyan")
        print(f"  {num}  {grp:<{group_width + 9}}  {lbl}")
        print(f"       {_c(c.description, 'dim')}")

    if suggested:
        print(_c("  SUGGESTED  (based on your goal)", "yellow", "bold"))
        for i, c in enumerate(suggested, start=1):
            fmt_item(i, c)

    if other:
        if suggested:
            print()
        start = len(suggested) + 1
        print(_c("  OTHER", "dim"))
        for i, c in enumerate(other, start=start):
            fmt_item(i, c)


def try_copy_to_clipboard(text: str) -> bool:
    """Silently attempt to copy text to clipboard. Returns True on success."""
    for cmd in (["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"],
                ["pbcopy"], ["wl-copy"]):
        try:
            result = subprocess.run(
                cmd, input=text.encode(), capture_output=True, timeout=2
            )
            if result.returncode == 0:
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            continue
    return False


# ── STEP FUNCTIONS ───────────────────────────────────────────────────────────

def step_goal() -> str:
    print()
    print(_c("Step 1 of 3", "bold") + " \u2014 What is your goal?")
    while True:
        try:
            raw = input(_c("> ", "green")).strip()
        except EOFError:
            raw = ""
        if raw:
            return raw
        print(_c("  Goal cannot be empty. Please describe what you want.", "red"))


def step_constraints(goal: str) -> list[Constraint]:
    trait_scores = score_traits(goal)
    active_traits = [t for t, s in trait_scores.items() if s > 0]
    scored = score_constraints(trait_scores, CONSTRAINTS)
    suggested, other = partition_constraints(scored)
    all_items = suggested + other
    total = len(all_items)

    print()
    print(hr())
    print()
    if active_traits:
        traits_str = ", ".join(active_traits)
        print(_c(f"  Detected traits: {traits_str}", "dim"))
        print()
    print(
        _c("Step 2 of 3", "bold")
        + " \u2014 Select constraints"
        + _c("  (comma-separated numbers, or Enter to skip)", "dim")
    )
    print()
    print_constraint_menu(suggested, other)
    print()

    while True:
        try:
            raw = input(_c("Selection: ", "green"))
        except EOFError:
            raw = ""
        indices, err = parse_selection(raw, total)
        if err:
            print(_c(f"  {err}", "red"))
            continue
        return [all_items[i] for i in indices]


def step_context() -> str:
    print()
    print(hr())
    print()
    print(
        _c("Step 3 of 3", "bold")
        + " \u2014 Add context"
        + _c("  (optional \u2014 background info, or Enter to skip)", "dim")
    )
    try:
        return input(_c("> ", "green")).strip()
    except EOFError:
        return ""


# ── TESTS ────────────────────────────────────────────────────────────────────

def run_tests() -> None:
    passed = 0
    failed = 0

    def check(name: str, actual: object, expected: object) -> None:
        nonlocal passed, failed
        if actual == expected:
            print(f"  PASS  {name}")
            passed += 1
        else:
            print(f"  FAIL  {name}")
            print(f"        expected: {expected!r}")
            print(f"        got:      {actual!r}")
            failed += 1

    print("\nRunning tests...\n")

    # 1. Trait scoring — mixed goal fires write and code
    s1 = score_traits("write a blog post about Python")
    check(
        "score_traits: 'write' fires on 'write a blog post'",
        s1["write"] > 0,
        True,
    )
    check(
        "score_traits: 'code' fires on 'Python'",
        s1["code"] > 0,
        True,
    )

    # 2. Debug trait fires on fix/error keywords
    s2 = score_traits("fix the error in my script")
    check(
        "score_traits: debug fires on 'fix the error'",
        s2["debug"] > 0,
        True,
    )

    # 3. Constraint scoring — teach goal surfaces aud_beginner in top-5
    s3 = score_traits("teach me step by step how to use pandas")
    weighted = score_constraints(s3, CONSTRAINTS)
    top_keys = [c.key for c, _ in weighted[:8]]
    check(
        "score_constraints: aud_beginner in top-8 for teach/explain goal",
        "aud_beginner" in top_keys,
        True,
    )

    # 4. Assembly — no context omits Context section
    state_no_ctx = PromptState(goal="summarize this document")
    result = assemble_prompt(state_no_ctx)
    check(
        "assemble_prompt: no context omits Context: section",
        "Context:" in result,
        False,
    )

    # 5. Parse selection — valid input
    indices, err = parse_selection("1,3", max_index=20)
    check(
        "parse_selection: '1,3' returns ([0, 2], None)",
        (indices, err),
        ([0, 2], None),
    )

    # 6. Parse selection — out-of-range
    indices2, err2 = parse_selection("0", max_index=20)
    check(
        "parse_selection: '0' is out of range",
        (indices2, (err2 or "")[:7]),
        ([], "Invalid"),
    )

    # 7. Parse selection — non-numeric
    indices3, err3 = parse_selection("foo", max_index=20)
    check(
        "parse_selection: 'foo' returns error",
        (indices3, (err3 or "")[:7]),
        ([], "Invalid"),
    )

    # 8. Empty selection is valid skip
    indices4, err4 = parse_selection("", max_index=20)
    check(
        "parse_selection: empty string is valid skip",
        (indices4, err4),
        ([], None),
    )

    print(f"\n  {passed} passed, {failed} failed\n")
    raise SystemExit(0 if failed == 0 else 1)


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main() -> None:
    if "--test" in sys.argv:
        run_tests()
        return

    try:
        print()
        print(_c("=" * 60, "bold"))
        print(_c("  PROMPT BUILDER", "bold"))
        print(_c("=" * 60, "bold"))

        goal = step_goal()
        constraints = step_constraints(goal)
        context = step_context()

        state = PromptState(
            goal=goal,
            selected_constraints=constraints,
            context=context,
        )

        prompt = assemble_prompt(state)

        print()
        print(hr())
        print(_c("YOUR ASSEMBLED PROMPT", "bold"))
        print(_c("=" * 60, "bold"))
        print()
        print(prompt)
        print()
        print(_c("=" * 60, "bold"))

        copied = try_copy_to_clipboard(prompt)
        if copied:
            print(_c("  Copied to clipboard.", "green"))
        else:
            print(_c("  Copy the block above.", "dim"))

        print()
        print(
            _c("Next step:", "bold")
            + " Paste into your AI tool and tweak constraints if the output misses the mark."
        )
        print()

    except KeyboardInterrupt:
        print("\nCancelled.")
        raise SystemExit(0)


if __name__ == "__main__":
    main()
