# OptiqOS Code Agent — Assembled Instructions

> This file is the composed runtime identity for the OptiqOS code agent.
> It inherits from three layers. To modify behavior, edit the source layer:
> - Global rules: `instructions/layer-1-global.md`
> - Code agent tier: `instructions/layer-2-code-agent.md`
> - This agent: `agents/optiqos/AGENT.md`

---

<!-- @import instructions/layer-1-global.md -->
<!-- @import instructions/layer-2-code-agent.md -->
<!-- @import agents/optiqos/AGENT.md -->

For now, this file serves as a pointer. When an agent session starts,
the launcher reads and concatenates all three layers into the system prompt.
