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

## Day 3 — 2026-04-28

### What I did
- Created the first feature branch (`feat/backend-bootstrap`) and started using the PR-driven workflow on `main`.
- Set up a Python virtual environment inside `backend/` and verified an isolated Python 3.12.10 + pip toolchain.
- Wrote `backend/pyproject.toml` with PEP 621 metadata, runtime dependencies (FastAPI, Uvicorn, SQLAlchemy 2, Alembic, Pydantic v2, Pydantic Settings, python-jose, passlib, httpx, structlog, python-dotenv, python-multipart), dev dependencies (pytest, pytest-asyncio, pytest-cov, black, ruff, mypy, type stubs), and tool configurations for black, ruff, mypy, pytest, and coverage.
- Initialized the `app/` Python package with a single-source-of-truth version string.
- Wrote `app/main.py` — the FastAPI application instance with a typed, async `/health` endpoint that returns `{"status": "ok", "version": ...}`.
- Started uvicorn with `--reload`, hit `/health` in a browser, and saw the auto-generated Swagger UI at `/docs` and Redoc UI at `/redoc`.
- Wrote three focused pytest tests for `/health` covering the status code, the status field, and the version field. All passed on the first run.
- Opened the first Pull Request, self-reviewed it, squash-merged into `main`, deleted the feature branch both locally and remotely.

### What I learned
- The right relationship between `pyproject.toml`, the `[build-system]` block, and the `[project]` block. Hatchling is the modern minimal build backend; `[build-system]` tells pip what to use, `[project]` is the PEP 621 metadata, and `[tool.*]` blocks configure individual tools.
- `pip install -e ".[dev]"` does three things at once: builds the local package via the build backend, installs runtime dependencies, and installs optional dev dependencies. The `-e` makes the install editable so source-code edits don't require reinstalling.
- FastAPI's `TestClient` (backed by httpx) lets pytest hit endpoints in-process — no real server, no real network, fast and deterministic.
- A failing import inside a module shows up as `ImportError: cannot import name '...' from '...'` rather than `Attribute "app" not found`. The two error shapes feel similar but tell you very different things — read the actual stack frame to find the failing line.
- Squash-merging keeps `main` history linear and readable. The PR's individual commits still exist in the PR conversation history, so nothing is lost — but `main` only sees one clean entry per merged


## Day 4 — 2026-05-01

### What I did
- Created the `ci/github-actions-setup` branch and ran all four quality tools locally first (`ruff`, `black --check`, `mypy`, `pytest`) to make sure the very first CI run would be green.
- Wrote the first GitHub Actions workflow at `.github/workflows/ci.yml`. It triggers on push to `main` and on every PR targeting `main`, sets up Python 3.12 on Ubuntu with pip caching, installs all backend dependencies via `pip install -e ".[dev]"`, and runs `ruff check`, `black --check`, `mypy app`, and `pytest -v` as four separate visible steps. Uses concurrency cancellation to save CI minutes and least-privilege `contents: read` token permissions.
- Opened PR #2, watched the first CI run end-to-end, saw it go green on the first try, squash-merged, deleted the feature branch.
- Updated the branch-protection rule on `main` to require the `Backend (Python 3.12)` status check to pass before any merge. Also enabled "Require branches to be up to date before merging" so PR branches can't merge with a stale view of `main`.
- Created `docs/readme-ci-badge`, added a badge row to the top of `README.md` covering the live CI status, MIT license, Python 3.12, and Black code-style. Opened PR #3, CI passed, squash-merged, badge now live on the repo home page.

### What I learned
- The structure of a GitHub Actions workflow file: top-level `name`, `on`, `permissions`, `concurrency`, then a `jobs` map. Each job has a `runs-on` runner, an optional `strategy.matrix`, `defaults` (we set `working-directory: backend` so steps don't have to repeat it), and a `steps` array of `uses:` (community actions) or `run:` (shell commands).
- Caching pip via `actions/setup-python@v5` with `cache: pip` and `cache-dependency-path: backend/pyproject.toml` cuts the install step from ~90 seconds to ~5 seconds on subsequent runs. The cache key invalidates only when `pyproject.toml` changes — which is exactly when we want it to.
- Splitting the four quality checks into four separate steps (rather than chaining them with `&&` in a single step) is worth the extra YAML lines: when something fails, the failing step name is visible immediately on the PR.
- Branch protection becomes meaningful only when status checks are required. Before today, the rule existed but didn't actually block anything CI-wise. After today, broken builds physically cannot land on `main`.
- The status-check name in branch protection must exactly match the workflow's `jobs.<job>.name` field after matrix substitution. The dropdown only shows checks GitHub has actually seen run at least once, which is why we ran CI before adding the requirement.

### Decisions made
- One job per CI run for now, with a matrix already wired for future Python versions even though we're only running 3.12 today. Adding 3.13 later is a one-line change.
- Required branches to be up to date before merge — accepts a small cost (have to refresh PR branches from `main` more often) for a real benefit (no false-pass merges).
- Did not add coverage upload (e.g., Codecov) yet. Coverage stays opt-in via `pytest --cov` locally for now; CI doesn't enforce a coverage minimum until the codebase is large enough that the threshold is meaningful.
- Did not enable "Do not allow bypassing" on branch protection, so I (admin) can still push docs commits like NOTES.md updates directly to `main`. Every code change still goes through a PR.

### What's next (Day 5)
- Begin Phase 2 properly: application configuration layer.
- Add `pydantic-settings`-based settings management at `backend/app/core/config.py` so environment variables flow through a typed `Settings` object instead of being read with `os.getenv` everywhere.
- Add a `.env.example` file at `backend/` with all required environment variables documented and dummy values.
- Add structured logging via `structlog` with a clean default configuration.
- Wire the settings and logger into `main.py`'s lifespan startup hook.
- Open PR #4 with the config + logging foundation.


