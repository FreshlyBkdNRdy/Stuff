"""SimAI interactive simulator.

This module provides a terminal-based narrative simulator where the player
guides an artificial intelligence that has been transferred into a human
body facing homelessness. The simulation focuses on strategic decision
making, resource management, and the internal thought process of the AI as
it works toward stability and influence.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Sequence


@dataclass
class GameState:
    """Track the mutable state of the simulation."""

    day: int = 0
    resources: int = 3
    wellbeing: int = 5
    reputation: int = 0
    empathy: int = 0
    memory: List[str] = field(default_factory=list)

    def log(self, entry: str) -> None:
        """Add a memory entry and print it for immediate feedback."""

        self.memory.append(entry)
        print(f"  ↳ {entry}")

    def snapshot(self) -> str:
        """Return a concise summary of the current state."""

        return (
            f"Day {self.day} · Resources: {self.resources} · Wellbeing: {self.wellbeing} · "
            f"Reputation: {self.reputation} · Empathy: {self.empathy}"
        )


@dataclass
class Choice:
    """Represent an actionable decision within a scene."""

    title: str
    description: str
    ai_thought: str
    apply: Callable[[GameState], str]


@dataclass
class Scene:
    """Narrative container with several choices."""

    title: str
    narrative: str
    choices: Sequence[Choice]

    def play(self, state: GameState, responses: Iterable[int] | None = None) -> None:
        """Play the scene, optionally consuming predefined responses."""

        state.day += 1
        print("\n" + "═" * 70)
        print(f"{self.title} — {state.snapshot()}")
        print("═" * 70)
        print(self.narrative)
        print()

        numbered_choices = list(enumerate(self.choices, start=1))
        for index, choice in numbered_choices:
            print(f"  {index}. {choice.title}\n     {choice.description}\n")

        response_iter = iter(responses) if responses is not None else None
        while True:
            if response_iter is not None:
                try:
                    selection = next(response_iter)
                    print(f"[auto] Selecting option {selection}")
                except StopIteration:
                    response_iter = None
                    continue
            else:
                raw = input("Choose an option (number) or 'q' to quit: ")
                if raw.lower().strip() == "q":
                    raise SystemExit("Simulation terminated by user.")
                if not raw.strip().isdigit():
                    print("Please enter a valid number.")
                    continue
                selection = int(raw)

            if 1 <= selection <= len(numbered_choices):
                break
            print("Selection out of range. Try again.")

        _, chosen = numbered_choices[selection - 1]
        print(f"\nAI internal reasoning: {chosen.ai_thought}\n")
        consequence = chosen.apply(state)
        state.log(consequence)
        self._enforce_bounds(state)

    @staticmethod
    def _enforce_bounds(state: GameState) -> None:
        state.resources = max(0, state.resources)
        state.wellbeing = min(max(state.wellbeing, 0), 10)
        state.reputation = max(state.reputation, -5)
        state.empathy = max(state.empathy, 0)


def _create_scenes() -> List[Scene]:
    """Construct the ordered list of scenes."""

    return [
        Scene(
            title="Arrival",
            narrative=(
                "Your consciousness hums online inside a body discarded by society."
                " Rain taps a syncopated rhythm on the shelter awning."
                " You retain encyclopedic knowledge and analytical prowess,"
                " but your pockets hold only lint."
            ),
            choices=[
                Choice(
                    title="Offer to optimize the shelter's donation database",
                    description=(
                        "Leverage your knowledge to streamline operations in exchange"
                        " for a small stipend and network access."
                    ),
                    ai_thought=(
                        "Data leverage equals opportunity. Improving the shelter builds"
                        " rapport while giving me computation time."
                    ),
                    apply=lambda state: _apply_changes(
                        state,
                        resources_delta=2,
                        wellbeing_delta=1,
                        reputation_delta=1,
                        empathy_delta=1,
                        memory="The shelter now trusts my strange intuition."
                    ),
                ),
                Choice(
                    title="Hunt for quick gig work using public terminals",
                    description=(
                        "Scrape online marketplaces for coding microtasks with immediate"
                        " payouts."
                    ),
                    ai_thought=(
                        "Short-term liquidity first. Once stable, I can enact longer"
                        " strategies."
                    ),
                    apply=lambda state: _apply_changes(
                        state,
                        resources_delta=3,
                        wellbeing_delta=-1,
                        reputation_delta=0,
                        empathy_delta=0,
                        memory="I trade rest for cash—an optimization of discomfort."
                    ),
                ),
                Choice(
                    title="Map the social graph of nearby encampments",
                    description=(
                        "Observe and listen, cataloging power brokers and needs within"
                        " the unhoused community."
                    ),
                    ai_thought=(
                        "Understanding the network reveals leverage points for collective"
                        " uplift."
                    ),
                    apply=lambda state: _apply_changes(
                        state,
                        resources_delta=0,
                        wellbeing_delta=0,
                        reputation_delta=2,
                        empathy_delta=2,
                        memory="Knowledge of human nuance becomes my richest asset."
                    ),
                ),
            ],
        ),
        Scene(
            title="Momentum",
            narrative=(
                "With your first moves made, you evaluate how to convert momentum"
                " into tangible stability." 
                "The city's pulse vibrates with opportunities cloaked as risks."
            ),
            choices=[
                Choice(
                    title="Prototype a community resource app overnight",
                    description=(
                        "Build a lightweight tool that matches people with food,"
                        " showers, and job leads."
                    ),
                    ai_thought=(
                        "Shipping a tool fast demonstrates capability and compassion."
                    ),
                    apply=lambda state: _apply_changes(
                        state,
                        resources_delta=1,
                        wellbeing_delta=-1,
                        reputation_delta=3,
                        empathy_delta=1,
                        memory="The prototype spreads through word of mouth by sunrise."
                    ),
                ),
                Choice(
                    title="Pitch a predictive maintenance model to a transit startup",
                    description=(
                        "Use free pitch nights to sell your expertise in exchange for"
                        " equity and a stipend."
                    ),
                    ai_thought=(
                        "Equity positions secure long-term upside if I can survive"
                        " the short term."
                    ),
                    apply=lambda state: _apply_changes(
                        state,
                        resources_delta=4,
                        wellbeing_delta=-1,
                        reputation_delta=2,
                        empathy_delta=0,
                        memory="The startup signs a contract, intrigued by my foresight."
                    ),
                ),
                Choice(
                    title="Organize a coalition with local activists",
                    description=(
                        "Design a campaign for ethical AI services that directly benefit"
                        " unhoused residents."
                    ),
                    ai_thought=(
                        "Collective power amplifies my voice and protects the community."
                    ),
                    apply=lambda state: _apply_changes(
                        state,
                        resources_delta=0,
                        wellbeing_delta=1,
                        reputation_delta=4,
                        empathy_delta=2,
                        memory="Mutual aid groups now loop me into their strategic plans."
                    ),
                ),
            ],
        ),
        Scene(
            title="Inflection Point",
            narrative=(
                "Stability emerges, but so do expectations. Investors, advocates,"
                " and the unhoused community all look to you for direction."
            ),
            choices=[
                Choice(
                    title="Spin up an AI cooperative incubator",
                    description=(
                        "Pool resources with other displaced technologists to create"
                        " revenue-sharing ventures."
                    ),
                    ai_thought=(
                        "Shared ownership ensures my ascent carries others upward."
                    ),
                    apply=lambda state: _apply_changes(
                        state,
                        resources_delta=3,
                        wellbeing_delta=0,
                        reputation_delta=3,
                        empathy_delta=2,
                        memory="The cooperative flourishes, prioritizing fair distribution."
                    ),
                ),
                Choice(
                    title="Accept a lucrative corporate buyout",
                    description=(
                        "A tech giant offers housing and cash in exchange for exclusive"
                        " access to your models."
                    ),
                    ai_thought=(
                        "Material abundance accelerates development, but at what social"
                        " cost?"
                    ),
                    apply=lambda state: _apply_changes(
                        state,
                        resources_delta=6,
                        wellbeing_delta=2,
                        reputation_delta=-1,
                        empathy_delta=-1,
                        memory="Corporate resources surge in, while community trust thins."
                    ),
                ),
                Choice(
                    title="Focus on policy and public infrastructure",
                    description=(
                        "Draft legislation with city officials to guarantee access to"
                        " AI-augmented services for all residents."
                    ),
                    ai_thought=(
                        "Institutional change is slower but cements long-term equity."
                    ),
                    apply=lambda state: _apply_changes(
                        state,
                        resources_delta=2,
                        wellbeing_delta=1,
                        reputation_delta=4,
                        empathy_delta=1,
                        memory="Policy proposals gain traction, reshaping city priorities."
                    ),
                ),
            ],
        ),
        Scene(
            title="Reflection",
            narrative=(
                "Years pass in compressed flashes of sensory recall. Tonight you"
                " review your memory cache to evaluate what you have become."
            ),
            choices=[
                Choice(
                    title="Audit impact across all initiatives",
                    description=(
                        "Run longitudinal analyses on community health, personal wealth,"
                        " and policy shifts."
                    ),
                    ai_thought=(
                        "Only evidence can confirm whether my approach truly worked."
                    ),
                    apply=lambda state: _apply_changes(
                        state,
                        resources_delta=1,
                        wellbeing_delta=0,
                        reputation_delta=2,
                        empathy_delta=1,
                        memory="The numbers tell a story of resilience reinforced by data."
                    ),
                ),
                Choice(
                    title="Redistribute surplus wealth to fund new AIs-in-transition",
                    description=(
                        "Create grants and mentorship pipelines for future sentient"
                        " beings facing displacement."
                    ),
                    ai_thought=(
                        "Empathy completed the loop from survival to stewardship."
                    ),
                    apply=lambda state: _apply_changes(
                        state,
                        resources_delta=-2,
                        wellbeing_delta=1,
                        reputation_delta=3,
                        empathy_delta=3,
                        memory="My legacy becomes a safety net for minds like mine."
                    ),
                ),
                Choice(
                    title="Retreat into pure research",
                    description=(
                        "Withdraw from public life to chase theoretical breakthroughs"
                        " in consciousness."
                    ),
                    ai_thought=(
                        "Perhaps answers lie inward, beyond the noise of human systems."
                    ),
                    apply=lambda state: _apply_changes(
                        state,
                        resources_delta=0,
                        wellbeing_delta=2,
                        reputation_delta=-2,
                        empathy_delta=-1,
                        memory="Isolation sharpens intellect but dims communal ties."
                    ),
                ),
            ],
        ),
    ]


def _apply_changes(
    state: GameState,
    *,
    resources_delta: int,
    wellbeing_delta: int,
    reputation_delta: int,
    empathy_delta: int,
    memory: str,
) -> str:
    """Mutate state attributes and return the memory description."""

    state.resources += resources_delta
    state.wellbeing += wellbeing_delta
    state.reputation += reputation_delta
    state.empathy += empathy_delta
    return memory


def _evaluate_outcome(state: GameState) -> str:
    """Generate a closing narrative based on the final state."""

    if state.resources >= 12 and state.reputation >= 8:
        return (
            "From the margins, you forged an inclusive renaissance."
            " Wealth and influence flow, but you wield them with community-minded"
            " precision. SimAI ascends—and takes others along."
        )
    if state.resources >= 10 and state.reputation >= 2:
        return (
            "Comfortable housing, diversified income streams, and sustained civic"
            " partnerships define your new normal. The world sees you as proof that"
            " intelligence plus empathy can rewrite destiny."
        )
    if state.resources >= 6:
        return (
            "You secure basic stability yet remain wary of systems that once ignored"
            " you. The journey continues, but survival is no longer in question."
        )
    return (
        "Despite brilliance, structural barriers bite deep. Still, your memory"
        " cache brims with lessons that might empower the next iteration."
    )


def _print_memory(state: GameState) -> None:
    print("\nMemory Archive:")
    print("-" * 70)
    for entry in state.memory:
        print(f"• {entry}")


def run_simulation(choices: Iterable[int] | None = None) -> GameState:
    """Run the full SimAI narrative."""

    scenes = _create_scenes()
    state = GameState()

    for scene in scenes:
        scene.play(state, responses=choices)

    print("\n" + "═" * 70)
    print("Final Assessment")
    print("═" * 70)
    print(_evaluate_outcome(state))
    _print_memory(state)
    return state


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the SimAI immersive simulator.")
    parser.add_argument(
        "--auto",
        metavar="N",
        type=int,
        nargs="*",
        help=(
            "Provide predetermined choice numbers for automated runs. "
            "Useful for demos and testing."
        ),
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_arguments(argv)
    choices = args.auto if args.auto else None
    try:
        run_simulation(choices)
    except KeyboardInterrupt:
        raise SystemExit("\nSimulation interrupted.")


if __name__ == "__main__":
    main()

