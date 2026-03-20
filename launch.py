#!/usr/bin/env python3
# @section 1 Agent Launcher
"""Launch a code agent as a Claude Code session with the full instruction stack."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from core.instructions import assemble, list_agents

# @subsection 1.1 Agent Working Directories
# Maps agent names to the repo they operate in.
# Add new agents here as they're created.
AGENT_WORKDIRS: dict[str, str] = {
    "optiqos": r"C:\Dev\optiq-os",
    "agentops": r"C:\Dev\sme-vital-agents",
}


# @subsection 1.2 Launch
def launch(agent_name: str, extra_args: list[str] | None = None) -> None:
    """Assemble instructions and launch a Claude Code session.

    Args:
        agent_name: Agent folder name (e.g., 'optiqos').
        extra_args: Additional args to pass to claude CLI.
    """
    # Assemble the full instruction stack
    try:
        system_prompt = assemble(agent_name)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Determine working directory
    workdir = AGENT_WORKDIRS.get(agent_name)
    if not workdir:
        print(f"Warning: No working directory mapped for '{agent_name}'.", file=sys.stderr)
        print(f"  Add it to AGENT_WORKDIRS in launch.py", file=sys.stderr)
        print(f"  Launching in current directory.\n", file=sys.stderr)
        workdir = os.getcwd()

    workdir_path = Path(workdir)
    if not workdir_path.exists():
        print(f"Error: Working directory does not exist: {workdir}", file=sys.stderr)
        sys.exit(1)

    # Build the claude command
    cmd = [
        "claude",
        "--system-prompt", system_prompt,
        "--add-dir", str(Path(__file__).parent),  # give access to sme-vital-agents too
    ]

    if extra_args:
        cmd.extend(extra_args)

    print(f"🤖 Launching {agent_name} agent")
    print(f"   Working dir: {workdir}")
    print(f"   Instruction layers: 3 (global + code-agent + {agent_name})")
    print(f"   System prompt: {len(system_prompt):,} chars")
    print()

    # Launch claude in the agent's working directory
    try:
        result = subprocess.run(cmd, cwd=workdir)
        sys.exit(result.returncode)
    except FileNotFoundError:
        print("Error: 'claude' CLI not found. Is Claude Code installed?", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nSession ended.")
        sys.exit(0)


# @subsection 1.3 CLI
def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sva-launch",
        description="Launch a code agent as a Claude Code session",
    )
    parser.add_argument(
        "agent",
        nargs="?",
        help="Agent name to launch (e.g., 'optiqos')",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available agents",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Override the model (e.g., 'opus', 'sonnet')",
    )
    parser.add_argument(
        "--print",
        dest="print_mode",
        action="store_true",
        help="Run in non-interactive print mode",
    )
    parser.add_argument(
        "--prompt",
        default=None,
        help="Initial prompt to send (use with --print)",
    )

    args, extra = parser.parse_known_args()

    if args.list:
        agents = list_agents()
        if not agents:
            print("No agents defined. Create one in agents/<name>/AGENT.md")
        else:
            print("Available agents:")
            for name in agents:
                workdir = AGENT_WORKDIRS.get(name, "(no workdir mapped)")
                print(f"  {name:<20} {workdir}")
        return

    if not args.agent:
        parser.print_help()
        return

    # Build extra args for claude CLI
    extra_args = list(extra)
    if args.model:
        extra_args.extend(["--model", args.model])
    if args.print_mode:
        extra_args.append("--print")
    if args.prompt:
        extra_args.append(args.prompt)

    launch(args.agent, extra_args)


if __name__ == "__main__":
    main()
