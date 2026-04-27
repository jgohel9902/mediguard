# MediGuard

> A privacy-first medication interaction tracker for patients on multiple prescriptions.

---

## The Problem

In the United States, over 40% of adults aged 65 and older take five or more prescription medications daily — a condition known as **polypharmacy**. Drug–drug interactions account for an estimated 1.3 million emergency room visits annually, and the risk grows non-linearly with each additional medication added to the regimen.

Existing tools fall short:

- **Pairwise lookup tools** (Drugs.com, GoodRx) check one drug against another, not against a full medication profile.
- **Pharmacy-managed systems** are siloed by chain — Walgreens cannot see what CVS dispensed.
- **Medication-reminder apps** (Medisafe, Mango Health) focus on adherence, not interaction analysis.

There is no free, privacy-respecting tool that takes a complete medication list — including over-the-counter drugs and supplements — and continuously flags interaction risks across the entire profile.

---

## The Solution

MediGuard lets a patient (or a caregiver managing someone else's care) maintain a single source of truth for everything they take, then continuously checks that profile against authoritative data sources:

- **OpenFDA Adverse Events Database** — real-world post-market safety signals
- **RxNorm Normalized Names** — standardizes drug names across brand, generic, and dosage variations
- A **risk-scoring engine** that prioritizes interactions by severity, contraindication likelihood, and patient-specific risk factors (age, kidney function, pregnancy status)

User health data stays under user control. No analytics, no tracking, no monetization of medical records.

---

## Status

**Phase 1 — Foundations.** This project is being built publicly as a portfolio piece, following the full software development lifecycle end-to-end. See the [Roadmap](#roadmap) for current progress and [NOTES.md](./NOTES.md) for the build journal.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2 |
| Database | PostgreSQL (production), SQLite (development), Alembic migrations |
| Frontend | Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui |
| External APIs | OpenFDA, RxNorm |
| Auth | JWT, bcrypt |
| Testing | Pytest, Vitest, Playwright (end-to-end) |
| CI/CD | GitHub Actions |
| Containerization | Docker, docker-compose |
| Hosting | Render (API), Vercel (web) |
| Monitoring | Sentry |
| Accessibility | WCAG 2.1 AA, enforced via axe-core in CI |

---

## Project Structure

mediguard/
├── backend/              FastAPI Python backend
│   ├── app/
│   │   ├── api/          HTTP route handlers
│   │   ├── core/         Config, security, JWT
│   │   ├── db/           Database session and engine
│   │   ├── models/       SQLAlchemy ORM models
│   │   ├── schemas/      Pydantic request/response schemas
│   │   └── services/     Business logic — interaction engine, API clients
│   └── tests/            Pytest test suite
├── frontend/             Next.js 14 frontend (to be scaffolded in Phase 4)
├── docs/                 Long-form documentation
│   ├── architecture/     System diagrams and data models
│   ├── decisions/        Architecture Decision Records (ADRs)
│   └── api/              API contract documentation
├── scripts/              Utility scripts (seed data, deploy helpers)
└── .github/workflows/    CI/CD pipelines

---

## Architecture

A detailed architecture document will live at [docs/architecture/](./docs/architecture/) once the system design is documented in Phase 2. The headline shape: a stateless FastAPI service backed by PostgreSQL, fronted by a Next.js application, with external API calls to OpenFDA and RxNorm proxied and cached at the backend layer.

---

## Getting Started

> The application is under active development. Local setup instructions will be added to this section as the project becomes runnable. See [NOTES.md](./NOTES.md) for the current build journal and per-phase setup notes.

---

## Roadmap

- [x] Phase 1 — Foundations: repo scaffold, documentation skeleton, license
- [ ] Phase 2 — Backend MVP: FastAPI app, database models, JWT authentication
- [ ] Phase 3 — API integrations: OpenFDA, RxNorm, interaction engine
- [ ] Phase 4 — Frontend MVP: Next.js shell, design system, authentication flow
- [ ] Phase 5 — Core features: medication CRUD, interaction checker, alerts
- [ ] Phase 6 — Polish: WCAG 2.1 AA audit, performance, PWA install, mobile UX
- [ ] Phase 7 — Production: Docker, deploy, monitoring, seed data
- [ ] Phase 8 — Ship: README polish, demo video, public launch

---

## Documentation

- [NOTES.md](./NOTES.md) — Build journal: what was done, what was learned, what's next
- [ARCHITECTURE.md](./ARCHITECTURE.md) — System architecture overview
- [CONTRIBUTING.md](./CONTRIBUTING.md) — Contribution guidelines and dev workflow
- [SECURITY.md](./SECURITY.md) — Responsible vulnerability disclosure
- [CHANGELOG.md](./CHANGELOG.md) — Version history

---

## Disclaimer

MediGuard is an educational and informational tool. It does **not** provide medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional before making medication decisions. Drug interaction data is derived from public datasets and may not reflect the most current clinical guidance.

---

## License

Released under the [MIT License](./LICENSE).

---

## Author

**Jenil Gohel** — built as an end-to-end portfolio project demonstrating full-stack engineering, healthcare-domain modeling, accessibility, and production-grade DevOps practices.

- GitHub: [@jgohel9902](https://github.com/jgohel9902)