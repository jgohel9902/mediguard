# Architecture — MediGuard

This document describes the high-level system architecture of MediGuard. It is updated as the system evolves and is paired with detailed design notes under `docs/architecture/` and architecture decision records under `docs/decisions/`.

---

## Goals and constraints

| Goal | Why it matters |
|---|---|
| **Privacy first** | Health data must never leave the user's control without explicit consent. No third-party analytics, no behavioral telemetry. |
| **Authoritative data** | Drug information must come from public, citable sources (OpenFDA, RxNorm). No scraping, no untrusted aggregators. |
| **Accessible by default** | Many target users are elderly or caregivers under stress; WCAG 2.1 AA is the floor, not the ceiling. |
| **Reproducible builds** | Anyone (including future me) must be able to spin up the entire stack with one command. |
| **Free-tier deployable** | The full production system must run on free hosting tiers so the demo stays live forever. |

---

## High-level component diagram

```
                     ┌──────────────────────────────┐
                     │        End User (web)        │
                     │   browser, mobile PWA, etc.  │
                     └──────────────┬───────────────┘
                                    │ HTTPS
                                    ▼
                     ┌──────────────────────────────┐
                     │   Frontend  (Next.js 14)     │
                     │   TypeScript · Tailwind ·    │
                     │   shadcn/ui · App Router     │
                     │   Hosted on Vercel           │
                     └──────────────┬───────────────┘
                                    │ HTTPS / JSON
                                    ▼
                     ┌──────────────────────────────┐
                     │   Backend API (FastAPI)      │
                     │   Python 3.12 · async        │
                     │   JWT auth · Pydantic        │
                     │   Hosted on Render           │
                     └──┬───────────────────────┬───┘
                        │                       │
              SQLAlchemy│                       │ httpx
                        ▼                       ▼
            ┌────────────────────┐   ┌──────────────────────┐
            │   PostgreSQL       │   │   External APIs      │
            │   (managed)        │   │   • OpenFDA          │
            │   user data,       │   │   • RxNorm           │
            │   medication lists │   │                      │
            │   audit log        │   │   Cached responses   │
            └────────────────────┘   └──────────────────────┘
```

---

## Components

### Frontend (`frontend/`)
- **Next.js 14 App Router** for routing, server components for data-fetching where useful.
- **TypeScript** end-to-end for type safety with the backend's OpenAPI-generated client.
- **Tailwind CSS + shadcn/ui** for an accessible, themeable design system.
- **React Hook Form + Zod** for type-safe forms and validation.
- **next-pwa** for installable PWA experience on mobile.
- Static assets, manifest, and service worker served by Vercel's edge network.

### Backend (`backend/`)
- **FastAPI** async web framework, with **Pydantic v2** for request/response models.
- **SQLAlchemy 2.0** ORM with **Alembic** for versioned migrations.
- **httpx** as the async HTTP client for OpenFDA and RxNorm calls.
- **JWT-based authentication** with bcrypt password hashing.
- Layered structure: `api/` (routes) → `services/` (business logic) → `models/` + `schemas/` (data) → `db/` (persistence).

### Data layer
- **PostgreSQL** in production (Render Managed Postgres free tier).
- **SQLite** in local development for fast iteration.
- The same SQLAlchemy models target both; differences abstracted at the engine URL.
- Schema migrations versioned and stored under `backend/alembic/`.

### External integrations
- **OpenFDA Drug Adverse Events API** for post-market safety signals and event frequencies.
- **RxNorm API** for canonical drug naming (resolving brand → generic, dosage normalization).
- All external calls go through a thin client wrapper in `backend/app/services/` with retry, timeout, and a local response cache.

---

## Data flow — adding a medication and checking interactions

1. User authenticates, receives JWT, browser stores in `httpOnly` cookie.
2. User searches for a medication in the UI — frontend hits `GET /medications/search?q=...`.
3. Backend forwards a normalization query to **RxNorm**, returns canonical results.
4. User picks a result → frontend POSTs to `/medications` with the canonical ID.
5. Backend persists the medication on the user's profile in PostgreSQL.
6. Backend computes interaction risk by fetching adverse-event data from **OpenFDA** for every pair (and triple) in the user's list, scoring each via the interaction engine.
7. Backend returns the ranked interaction report to the frontend, which renders the dashboard with severity-coded cards.

---

## Cross-cutting concerns

| Concern | Approach |
|---|---|
| **Authentication** | JWT with short-lived access tokens, refresh tokens stored as `httpOnly` cookies. |
| **Authorization** | Resource-level checks at the service layer (a user can only read their own medications). |
| **Logging** | Structured JSON logs via `structlog`, request IDs propagated end-to-end. |
| **Error tracking** | Sentry captures unhandled exceptions in both frontend and backend. |
| **Secrets** | `.env` locally, GitHub Actions Secrets for CI, environment variables on Render and Vercel. |
| **Caching** | Backend caches RxNorm and OpenFDA responses (TTL-based) to stay under rate limits and improve latency. |
| **Rate limiting** | Per-user rate limit on interaction-check endpoints to prevent abuse. |
| **Accessibility** | axe-core runs in the CI pipeline; any new accessibility violation fails the build. |
| **Testing** | Pytest for backend (unit + integration); Vitest for frontend units; Playwright for end-to-end tests against the deployed staging URL. |

---

## Deployment topology

```
   Developer push to main
            │
            ▼
   GitHub Actions CI
   ├── lint (ruff, eslint)
   ├── typecheck (mypy, tsc)
   ├── test (pytest, vitest)
   ├── e2e (playwright)
   └── a11y (axe-core)
            │
   ┌────────┴────────┐
   ▼                 ▼
Render           Vercel
(API + DB)       (Web)
```

- A push to `main` triggers CI.
- If all checks pass, the backend is deployed to Render and the frontend to Vercel.
- Failed checks block deployment.

---

## What this document is not

- It is **not** a substitute for in-code documentation; modules are documented at the source level.
- It is **not** a frozen contract; this file is updated whenever significant architectural decisions are made or revised.
- Specific design *decisions* with their full reasoning live as separate Architecture Decision Records under `docs/decisions/`.