# Build Journal — MediGuard

A running log of what I built, what I learned, decisions I made, and what's next.

This document is written for two audiences: my future self, so I remember why decisions were made, and anyone — including hiring managers — who wants to understand how I think and work.

---

## How I'm working

- **Workflow:** SDLC-aligned phases (Foundations → Backend → Integrations → Frontend → Features → Polish → Production → Ship).
- **Commits:** Conventional Commits (`feat`, `fix`, `docs`, `chore`, `style`, `refactor`, `test`, `ci`, `build`, `perf`). Roughly one logical change per commit.
- **Cadence:** ~1–2 hours on weekdays, more on weekends. Sustained pace over five to seven weeks beats a single weekend sprint.
- **Documentation:** Updated alongside the code, not at the end.

---

## Day 1 — 2026-04-27

### What I did
- Defined the project: MediGuard, a privacy-first medication interaction tracker for patients on multiple prescriptions.
- Selected the tech stack: Python 3.12 + FastAPI + PostgreSQL on the backend; Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui on the frontend; Docker, GitHub Actions, Render + Vercel for DevOps and hosting; Sentry for monitoring; axe-core for accessibility enforcement.
- Verified local environment: Python 3.12.10, Git 2.51.1, Node 22.21.0, npm 11.7.0, VS Code installed.
- Created the project folder at `~/OneDrive/Desktop/Projects/mediguard` so OneDrive provides free off-site backup automatically.
- Scaffolded the monorepo directory structure: `backend/`, `frontend/`, `docs/`, `scripts/`, `.github/workflows/`.
- Created an empty GitHub repository at github.com/jgohel9902/mediguard (public, MIT-licensed) without auto-generated files, so the first push wouldn't conflict.
- Initialized git locally with `main` as the default branch.
- Committed the first three foundational files in three separate Conventional Commits:
  - `chore: add .gitignore for Python, Node, and IDE artifacts`
  - `chore: add MIT license`
  - `docs: add initial README with problem statement, stack, and roadmap`
- Linked the local repo to the GitHub remote and pushed `main` upstream.

### What I learned
- The difference between **Visual Studio** (the full Microsoft IDE built around .NET) and **Visual Studio Code** (the lightweight cross-language editor). NuGet is the .NET package manager and does not apply to a Python + Node project — for this stack the package managers are `pip` and `npm`.
- Why `git push` fails on a fresh branch with no upstream, and what `-u origin main` actually does: it sets the local branch's "tracking" link to the remote branch so future `git push` and `git pull` calls don't need arguments.
- Why creating an empty GitHub repo *without* the auto-generated README/license/gitignore avoids merge conflicts on the first push from a local repo that already has those files.
- The Conventional Commits format and why it matters — scannable history, automatic CHANGELOG generation later, and clear semantic versioning hooks.

### Decisions made
- **Web app (PWA) over native iOS/Android.** A web app installable as a PWA gives shareable URLs to recruiters, avoids learning Swift or Kotlin, and keeps me in my Python lane. Trade-off accepted: no access to native phone APIs that aren't exposed to web.
- **Monorepo over split repos.** Backend and frontend live in one repository. Easier to coordinate changes and showcase as a single portfolio piece.
- **PostgreSQL in production, SQLite for local dev.** SQLAlchemy abstracts the difference, keeping the dev loop fast while still demonstrating knowledge of a real production-grade database.
- **MIT license.** Most permissive, most common, signals open-source literacy without legal complexity.
- **`main` as the default branch.** Industry standard since 2020.
- **OneDrive-backed Desktop for the project root.** Free off-site backup for free.

---


## Day 2 — 2026-04-27

### What I did
- Added `.editorconfig` to enforce consistent indentation, line endings, and whitespace across editors and operating systems.
- Created `.vscode/extensions.json` with the recommended extensions for the project (Python, TypeScript, Tailwind, Docker, GitLens, GitHub Actions, EditorConfig, spell-checker, Markdown tooling, YAML, TOML).
- Wrote ADR 0001 — Technology Stack Selection — at `docs/decisions/0001-technology-stack-selection.md`. It documents every major stack choice (FastAPI, Next.js, PostgreSQL, Tailwind + shadcn/ui, Render + Vercel) along with the rejected options, the trade-offs accepted, and the triggers that would cause us to revisit the decision.
- Configured a branch-protection rule on `main` via the GitHub UI: requires a pull request to merge, requires conversation resolution, requires linear history, blocks force pushes, blocks deletions. Status-check enforcement is left for once CI exists.

### What I learned
- The Michael Nygard ADR format (Status, Context, Decision, Consequences) is short by design but forces structured trade-off thinking. Writing the rejected options down was harder than writing the chosen one — and that's the point.
- Branch protection has more knobs than I expected. For a solo developer, the right mix is: require PRs, zero required approvals, allow admin bypass, block force pushes, block deletions. Each setting has a real reason.
- VS Code's `extensions.json` is honored automatically: when anyone opens the project, VS Code prompts to install the recommended extensions. This is how onboarding works on real engineering teams.
- `editorconfig` is not redundant with `prettier` and `black` — it covers behavior (indentation, line endings, final newline) for *every* file type, not just the ones a formatter handles.

### Decisions made
- `main` is now protected. Direct pushes are temporarily allowed for foundation docs (admin bypass, no review possible since I'm solo), but feature work starts on branches and merges through PRs.
- ADRs live under `docs/decisions/` and use the `NNNN-kebab-case-title.md` naming convention. Each one is numbered, dated, and includes a "Revisit triggers" section so future-me knows when to reopen the decision.
- VS Code is the editor of record for this project (not full Visual Studio); recommended extensions are committed to the repo so any contributor — including future-me on a different machine — gets the same setup.

