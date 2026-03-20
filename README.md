# sme-vital-agents

Multi-framework agent factory — agents that build standalone agents. **No Claude API dependency.**

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   CLI (TypeScript)               │
│   sva create │ sva run │ sva list │ sva export   │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│                 Core (Python)                    │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Backends │  │  Agents  │  │    Tools      │  │
│  │ ┌──────┐ │  │ ┌──────┐ │  │ ┌───────────┐ │  │
│  │ │Ollama│ │  │ │ Base │ │  │ │ read_file │ │  │
│  │ ├──────┤ │  │ ├──────┤ │  │ ├───────────┤ │  │
│  │ │Claude│ │  │ │Factor│ │  │ │write_file │ │  │
│  │ │ Code │ │  │ │  y   │ │  │ ├───────────┤ │  │
│  │ └──────┘ │  │ └──────┘ │  │ │  shell    │ │  │
│  └──────────┘  └──────────┘  │ └───────────┘ │  │
│                              └───────────────┘  │
└─────────────────────────────────────────────────┘
                       │
              ┌────────▼────────┐
              │  Exported Agent │
              │  (standalone)   │
              │  - agent.yaml   │
              │  - main.py      │
              │  - Dockerfile   │
              └─────────────────┘
```

## Quick Start

```bash
# Install Python core
pip install -e .

# Install CLI
cd cli && npm install && npm run build
npm link

# Create an agent
sva create my-agent

# Run it
sva run my-agent

# Export as standalone package
sva export my-agent
```

## Backends

| Backend      | Description                         | Requires      |
|-------------|-------------------------------------|---------------|
| `ollama`     | Local LLMs via Ollama               | Ollama running |
| `claude-code`| Claude Code CLI (no API key needed) | `claude` CLI   |

## Creating Agents

Agents are defined in YAML:

```yaml
name: code-reviewer
description: Reviews code for bugs and style issues
backend_name: ollama
model: llama3.1
system_prompt: |
  You are an expert code reviewer. Analyze code for bugs,
  security issues, and style problems. Be specific and actionable.
tools:
  - read_file
  - shell
max_turns: 10
temperature: 0.3
```

## Exporting Standalone Agents

`sva export` generates a self-contained directory:

```
exported-agents/code-reviewer/
  ├── agent.yaml        # Agent config
  ├── main.py           # Entrypoint
  ├── requirements.txt  # Python deps
  ├── Dockerfile        # Container support
  └── manifest.json     # Metadata
```

Run standalone: `python main.py`
Or containerized: `docker build -t code-reviewer . && docker run -it code-reviewer`
