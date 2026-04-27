# Contributing to MediGuard

Thanks for considering a contribution. MediGuard is currently maintained as a solo educational and portfolio project, but issues, suggestions, and pull requests from the community are welcome.

---

## Code of conduct

Be respectful. Be patient. Assume good intent. Disagreements are expected; rudeness is not. Harassment of any kind is grounds for being banned from participation.

---

## Ways to contribute

- **Report a bug.** Open a GitHub issue with reproduction steps, expected vs. actual behavior, and your environment (OS, Python version, Node version, browser).
- **Suggest a feature.** Open a GitHub issue describing the *user problem* you'd like solved, not just the proposed solution. Better suggestions start with a real user, not a feature idea.
- **Improve documentation.** Typo fixes, clarifications, and additional examples are always welcome and reviewed quickly.
- **Submit code.** See the workflow below.

---

## Development workflow

### Prerequisites

- Python 3.12 or higher
- Node.js 20 or higher, with npm 10 or higher
- Git 2.40 or higher
- Docker and docker-compose (optional but recommended for matching production)

### Local setup

> Detailed local-setup instructions are added to the [README](./README.md) as the project becomes runnable. The build journal in [NOTES.md](./NOTES.md) tracks current progress.

### Branches

| Branch | Purpose |
|---|---|
| `main` | Always deployable. Protected — accepts PRs only, no direct pushes. |
| `feat/<short-name>` | New features |
| `fix/<short-name>` | Bug fixes |
| `docs/<short-name>` | Documentation-only changes |
| `chore/<short-name>` | Tooling, dependency bumps, behavior-neutral refactors |
| `test/<short-name>` | Test-only additions |
| `ci/<short-name>` | CI/CD pipeline changes |

### Commit messages — Conventional Commits

```