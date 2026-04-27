# Changelog

All notable changes to MediGuard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added — Phase 1 · Foundations

- Project scaffolded as a monorepo with `backend/`, `frontend/`, `docs/`, `scripts/`, and `.github/workflows/` directories.
- `.gitignore` covering Python, Node.js, Next.js, virtualenv, IDE, OS, and secret-file patterns.
- MIT License.
- `README.md` with problem statement, solution narrative, tech-stack table, project-structure overview, and roadmap.
- `NOTES.md` build journal with Day 1 entry covering scope, decisions, learnings, and next steps.
- `ARCHITECTURE.md` describing high-level components, data flow for the medication-add and interaction-check paths, deployment topology, and cross-cutting concerns.
- `CONTRIBUTING.md` with development workflow, branch naming, Conventional Commits guide, code style, testing expectations, and accessibility requirements.
- `SECURITY.md` with responsible-disclosure policy, in-scope and out-of-scope definitions, and safe-harbor language.
- `CHANGELOG.md` (this file) following the Keep a Changelog format.

### Decided

- Web app deployed as a PWA, rather than native iOS/Android, to maximize recruiter accessibility and stay within the chosen language stack.
- Monorepo over split repos for solo development and unified portfolio presentation.
- PostgreSQL in production, SQLite in development, with SQLAlchemy abstracting the difference.
- MIT license.
- `main` as the default branch.
- Conventional Commits as the commit-message standard.

---

## Release types

When versioning begins:

| Bump | When |
|---|---|
| `MAJOR` | Breaking API changes |
| `MINOR` | Backward-compatible feature additions |
| `PATCH` | Backward-compatible bug fixes |

---

[Unreleased]: https://github.com/jgohel9902/mediguard/commits/main