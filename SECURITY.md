# Security Policy

MediGuard handles information related to medications and patient health. Even as an educational project, security is taken seriously.

---

## Supported versions

This project is in active development and does not yet have stable releases. Security fixes are applied to the `main` branch as the only currently supported version.

| Version | Supported |
|---|---|
| `main` | ✅ |
| Pre-release branches | ❌ |

---

## Reporting a vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.** Public disclosure before a fix is ready puts users at risk.

### How to report

Use one of the following channels:

1. **Preferred:** Open a [GitHub Security Advisory](https://github.com/jgohel9902/mediguard/security/advisories/new) — this creates a private discussion thread.
2. **Alternative:** Email the maintainer at the address listed on the [GitHub profile](https://github.com/jgohel9902) with the subject line beginning `[SECURITY] MediGuard:`.

### What to include

A useful report contains:

- A description of the vulnerability and its potential impact.
- Step-by-step reproduction instructions.
- Affected versions, branches, or commits.
- Any proof-of-concept code or screenshots.
- Your suggested remediation, if you have one.
- Whether you'd like to be credited in the fix announcement.

### What you can expect

| Stage | Target timing |
|---|---|
| Acknowledgement of report | Within 5 business days |
| Initial assessment of severity | Within 10 business days |
| Fix or mitigation plan | Within 30 days for high-severity issues |
| Public disclosure (after fix is deployed) | Coordinated with reporter |

---

## Scope

### In scope

- Vulnerabilities in the source code in this repository.
- Dependency vulnerabilities that affect the running application (`pip` or `npm` packages).
- Configuration issues in CI/CD that could expose secrets.
- Issues with the deployed demo instance (if one is live).

### Out of scope

- Vulnerabilities in third-party services we depend on (OpenFDA, RxNorm, Render, Vercel, GitHub) — please report those upstream.
- Social engineering or physical attacks against the maintainer.
- Denial-of-service attacks against demo deployments.
- Findings from automated scanners without a working proof of concept.

---

## Safe-harbor

Good-faith research conducted under this policy is considered authorized. The maintainer will not pursue legal action against researchers who:

- Make a reasonable, good-faith effort to avoid privacy violations and disruption.
- Do not exfiltrate any data beyond what is necessary to demonstrate the vulnerability.
- Give the maintainer a reasonable opportunity to remediate before any public disclosure.

---

## Hall of fame

Reporters who responsibly disclose valid vulnerabilities will, with their consent, be credited in the project changelog and in this section.

_(This list is currently empty — be the first.)_