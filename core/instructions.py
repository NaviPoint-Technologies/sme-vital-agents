# @section 1 Instruction Assembler
"""Composes the three-layer instruction stack into a single system prompt."""

from __future__ import annotations

from pathlib import Path


# @subsection 1.1 Constants
REPO_ROOT = Path(__file__).parent.parent
INSTRUCTIONS_DIR = REPO_ROOT / "instructions"
AGENTS_DIR = REPO_ROOT / "agents"

LAYER_1 = INSTRUCTIONS_DIR / "layer-1-global.md"
LAYER_2 = INSTRUCTIONS_DIR / "layer-2-code-agent.md"


# @subsection 1.2 Assembler
def assemble(agent_name: str) -> str:
    """Compose a full system prompt from the three-layer stack.

    Args:
        agent_name: Folder name under agents/ (e.g., 'optiqos').

    Returns:
        Concatenated instruction text ready to use as a system prompt.
    """
    agent_dir = AGENTS_DIR / agent_name
    layer_3 = agent_dir / "AGENT.md"

    layers: list[tuple[str, Path]] = [
        ("LAYER 1 — GLOBAL RULES", LAYER_1),
        ("LAYER 2 — CODE AGENT TIER", LAYER_2),
        (f"LAYER 3 — {agent_name.upper()} AGENT", layer_3),
    ]

    parts: list[str] = []
    for label, path in layers:
        if not path.exists():
            raise FileNotFoundError(f"Missing instruction layer: {path}")
        content = path.read_text(encoding="utf-8").strip()
        parts.append(f"{'=' * 60}\n{label}\n{'=' * 60}\n\n{content}")

    return "\n\n\n".join(parts)


# @subsection 1.3 List Agents
def list_agents() -> list[str]:
    """Return names of all agents with an AGENT.md file."""
    if not AGENTS_DIR.exists():
        return []
    return [
        d.name
        for d in sorted(AGENTS_DIR.iterdir())
        if d.is_dir() and (d / "AGENT.md").exists()
    ]


# @subsection 1.4 CLI
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        agents = list_agents()
        print("Available agents:", ", ".join(agents) if agents else "(none)")
        print("Usage: python -m core.instructions <agent_name>")
        sys.exit(1)

    agent_name = sys.argv[1]
    try:
        prompt = assemble(agent_name)
        print(prompt)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
