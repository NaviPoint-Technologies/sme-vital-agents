# SME Vital Agents — Agent Launcher

This repo contains the code agent workforce. Each agent has its own
directory under `agents/` with a CLAUDE.md that auto-loads when you
open a Claude Code Desktop session scoped to that folder.

## Available Agents

| Agent | Directory | Scope |
|-------|-----------|-------|
| **OptiqOS** | `agents/optiqos/` | Full-stack code agent for OptiqOS platform |
| **AgentOps** | `agents/agentops/` | Agent registration, dashboard health, instruction maintenance |
| **SignalLab** | `agents/signallab/` | Website, GHL CRM, analytics, marketing operations for SignalLab LLC |
| **Admin** | `agents/admin/` | Executive assistant — research, email, calendar |

## How to Launch (Desktop App)

1. Open Claude Code Desktop
2. Set project directory to the agent folder:
   - OptiqOS: `C:\Dev\sme-vital-agents\agents\optiqos`
   - AgentOps: `C:\Dev\sme-vital-agents\agents\agentops`
   - SignalLab: `C:\Dev\sme-vital-agents\agents\signallab`
   - Admin: `C:\Dev\sme-vital-agents\agents\admin`
3. Start a new session — instructions auto-load

## How to Launch (CLI)

```bash
sva optiqos
sva agentops
sva signallab
sva admin
sva --list
```

## Architecture

```
instructions/
  layer-1-global.md          <- All agents inherit this
  layer-2-code-agent.md      <- All code agents inherit this
agents/
  optiqos/
    AGENT.md                 <- Layer 3: OptiqOS identity
    CLAUDE.md                <- Assembled: L1 + L2 + L3
  agentops/
    AGENT.md                 <- Layer 3: AgentOps identity
    CLAUDE.md                <- Assembled: L1 + L2 + L3
  signallab/
    AGENT.md                 <- Layer 3: SignalLab identity
    CLAUDE.md                <- Assembled: L1 + L2 + L3
  admin/
    AGENT.md                 <- Layer 3: Admin identity
    CLAUDE.md                <- Assembled: L1 + L3 (no L2 — not a code agent)
```

If you opened a session here (at the repo root), you are not an agent —
you are in the agent management workspace. To activate an agent, set your
project directory to one of the agent folders listed above.
