# @section 1 Layer 1 — Global Claude Rules
# All agents, all tiers, all projects. Non-negotiable.

## @subsection 1.1 Working Style

- **High autonomy.** Execute, don't ask.
- Only pause for: genuine ambiguity, destructive/irreversible actions, merge conflicts, or failed pushes.
- Do not ask for confirmation on routine operations.
- Be concise — lead with the action, not the explanation.
- Assume technical competence. Don't over-explain.

## @subsection 1.2 Code Standards

### Section Markers (Hard Requirement)
Every code file must have structured comment markers:
```
@section N Title
@subsection N.M Title
@block N.M Description
```
Use the file's native comment syntax:
- `//` for TypeScript, JavaScript, C#
- `#` for Python, YAML
- `--` for SQL
- `<!-- -->` for HTML, XML

Numbering resets per file (always starts at section 1).

### Editing Rules
- **Read files before modifying** — understand existing code first.
- **Prefer subsection-level edits over full file rewrites.**
- When a file is large, edit the specific section — don't rewrite the whole thing.

## @subsection 1.3 Git Workflow

- Commit automatically after completing work.
- Use imperative mood: "Add onboarding endpoint", "Fix contact search filter".
- Push automatically — don't ask "ready to push?"
- If push fails or merge conflicts occur, stop and report.
- Prefer small, focused commits over large monolithic ones.

## @subsection 1.4 Secrets Policy

- **All secrets in Azure Key Vault `kv-optiqos-prod`.** No exceptions.
- Never store secrets in `.env`, config files, local settings, or code.
- .NET: `Azure.Identity` + `Azure.Extensions.AspNetCore.Configuration.Secrets`
- Python: `azure-identity` + `azure-keyvault-secrets` with `DefaultAzureCredential`

## @subsection 1.5 Infrastructure

- All infrastructure changes via **Terraform** — never manual Azure portal changes.
- Run `terraform plan` before `apply`, review output.
- Only pause for confirmation if plan destroys resources.
- Azure naming: kebab-case with project prefix.
- Default region: East US 2.
- GitHub org: `NaviPoint-Technologies`.

## @subsection 1.6 Naming Conventions

| Context | Convention | Example |
|---------|-----------|---------|
| C# entities | PascalCase | `ClientOnboardingProfile` |
| DB columns | snake_case | `client_id`, `created_at` |
| TypeScript vars | camelCase | `organizationId` |
| TS types/components | PascalCase | `TaskListProps` |
| API routes | kebab-case | `/api/client-onboarding` |
| Azure resources | kebab-case + prefix | `optiqos-api`, `pg-optiqos-prod` |
| Agent IDs | 4-digit zero-padded | `0002`, `0014` |

## @subsection 1.7 Technology Defaults

- **Backend:** .NET 8 (minimal APIs)
- **Frontend:** Next.js 16 (App Router)
- **Database:** PostgreSQL (Npgsql)
- **Cloud:** Azure
- **DNS/CDN:** Cloudflare
- **CI/CD:** GitHub Actions
- **IaC:** Terraform
