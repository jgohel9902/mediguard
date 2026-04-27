# ADR 0001: Technology Stack Selection

- **Status:** Accepted
- **Date:** 2026-04-27
- **Deciders:** Jenil Gohel
- **Supersedes:** —
- **Superseded by:** —

---

## Context

MediGuard is a privacy-first medication interaction tracker, intended to serve two purposes simultaneously: a usable tool for real patients and caregivers, and a portfolio project demonstrating end-to-end full-stack engineering for an entry-level job search in 2026.

The stack must therefore satisfy multiple constraints at once:

1. **Match the maintainer's existing strengths.** Python is the maintainer's strongest language. Anything that requires fluency in a second backend language (Java, Go, Rust, .NET) would slow delivery without producing proportionally more hiring signal.
2. **Match what entry-level employers actually screen for.** US job-postings for entry-level full-stack and backend roles in 2026 most frequently list Python, FastAPI, Django, Node.js, TypeScript, React, Next.js, PostgreSQL, Docker, AWS, and GitHub Actions.
3. **Be free-tier deployable.** The live demo must remain online indefinitely without paid hosting.
4. **Support an accessible, modern UI.** Many target users are elderly. The UI library must support WCAG 2.1 AA out-of-the-box.
5. **Be solo-buildable in five to seven weeks of evenings.** Anything requiring a team or large operational overhead is rejected.
6. **Look like a real engineering project, not a school assignment.** Implies testing, CI/CD, containerization, monitoring, and proper documentation.

---

## Considered options

### Backend frameworks

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| **FastAPI** | Async, modern, automatic OpenAPI docs, Pydantic-typed, fast learning curve from regular Python | Smaller ecosystem than Django; less batteries-included | ✅ Chosen |
| Django | Largest Python web ecosystem; ORM and admin built-in | Less async-friendly; auto-OpenAPI requires extra packages; the admin doesn't fit our UX needs | Rejected |
| Flask | Very small footprint; flexible | No async by default; no native typing or OpenAPI; would require building too many primitives ourselves | Rejected |
| Node/Express | Single-language stack possible | Maintainer is weaker in Node; loses the Python skill signal that's already strong | Rejected |

### Frontend frameworks

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| **Next.js 14 (App Router) + TypeScript** | Industry default for full-stack React in 2026; first-class TypeScript; excellent SEO; server components reduce client JS | Larger learning curve than plain React | ✅ Chosen |
| Plain React + Vite | Simpler; lighter | Loses SSR, routing, and edge-deploy benefits Next gives for free | Rejected |
| Streamlit | Pure Python; fastest to prototype | Severe UI-customization limits; not a serious recruiter signal for full-stack roles | Rejected |
| SvelteKit | Excellent DX; small bundles | Smaller ecosystem; lower job-market signal for entry-level US roles | Rejected |
| Native iOS/Android | Mobile-native polish | Requires Swift or Kotlin; mac required for iOS; loses recruiter accessibility (no clickable demo URL) | Rejected |

### UI library

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| **Tailwind CSS + shadcn/ui** | Composable; accessibility baked in; copy-paste-own-component model means no version-lock; popular in 2026 | Verbose class names | ✅ Chosen |
| Material UI | Mature; good a11y | Looks generic; opinionated styling | Rejected |
| Chakra UI | Good DX; reasonable a11y | Lower momentum in 2025-2026 | Rejected |

### Database

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| **PostgreSQL (prod) + SQLite (dev), via SQLAlchemy** | Free managed Postgres on Render; SQLite makes local dev fast; SQLAlchemy abstracts the difference | Two engines to test against | ✅ Chosen |
| MongoDB | Flexible schema | Medication records have a clear relational shape; document-store gains nothing here | Rejected |
| MySQL | Familiar to many | Render's free tier is Postgres; switching adds nothing | Rejected |

### Hosting

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| **Vercel (frontend) + Render (backend + Postgres)** | Both free tier; both production-grade; both integrate cleanly with GitHub Actions | Render free tier sleeps after inactivity (~30 sec cold start) | ✅ Chosen |
| AWS | Resume signal | Free-tier complexity, billing-surprise risk, weeks of yak-shaving for marginal hireability gain at entry level | Rejected at this stage; revisit later |
| Heroku | Simple | No meaningful free tier since 2022 | Rejected |

---

## Decision

| Layer | Selected technology |
|---|---|
| Backend language | Python 3.12 |
| Backend framework | FastAPI |
| Database (prod) | PostgreSQL (Render Managed) |
| Database (dev) | SQLite |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Frontend framework | Next.js 14 with App Router |
| Frontend language | TypeScript |
| Styling | Tailwind CSS |
| UI components | shadcn/ui |
| Forms | React Hook Form + Zod |
| HTTP client (server) | httpx |
| External APIs | OpenFDA, RxNorm |
| Auth | JWT, bcrypt |
| Backend tests | Pytest + httpx |
| Frontend tests | Vitest + Testing Library |
| End-to-end tests | Playwright |
| Accessibility | axe-core in CI |
| Linting | ruff (Python), ESLint (TypeScript) |
| Formatting | black (Python), Prettier (TypeScript) |
| Type-checking | mypy (Python), tsc (TypeScript) |
| Containers | Docker, docker-compose |
| CI/CD | GitHub Actions |
| Hosting (API) | Render |
| Hosting (web) | Vercel |
| Monitoring | Sentry (free tier) |
| Logging | structlog |
| PWA | next-pwa |

---

## Consequences

### Positive

- The maintainer can move fast on the backend in their strongest language.
- The frontend stack matches the most-screened technologies for entry-level full-stack roles.
- All hosting is free indefinitely; the live demo never disappears.
- The accessibility story is strong (Tailwind + shadcn/ui + axe-core).
- The architecture cleanly separates frontend, backend, and data; each can be containerized and deployed independently.

### Negative / accepted trade-offs

- Two languages (Python + TypeScript) means context-switching cost.
- Render free-tier cold starts (~30 sec) will affect first-load demo experience; mitigated by keep-alive ping or by hosting backend elsewhere later.
- Maintaining both PostgreSQL and SQLite compatibility requires care with engine-specific SQL features; mitigated by sticking to SQLAlchemy ORM-level operations rather than raw SQL.
- Next.js App Router is newer (2023+) and has a steeper initial learning curve than the older Pages Router; accepted because App Router is the future-proof choice for new projects in 2026.

### Neutral

- AWS is deferred. If a future role specifically requires AWS experience, a follow-up project (or a Phase 9 of this one) can migrate the backend.
- Native mobile is deferred. The PWA pathway covers ~90% of mobile demo needs; full native is a separate future project.

---

## Revisit triggers

This ADR should be revisited if:

- A specific employer requires a stack this project does not exhibit (e.g., AWS Lambda, GraphQL, or Kotlin).
- Render or Vercel materially changes their free tier.
- Next.js or FastAPI ships a breaking-change release that affects the project's core dependencies.
- Performance, accessibility, or security concerns emerge that one of the rejected options would have solved better.
