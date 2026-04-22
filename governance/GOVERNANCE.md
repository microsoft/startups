# Governance — microsoft/startups

## Principle

This repo orchestrates paths and routes to authoritative sources.
It does not own technical truth.

---

## What requires a pull request

- Adding or updating any content in `/paths/`
- Adding or updating any content in `/verticals/`
- Adding or updating links in `/index/`
- Adding or updating AEO pages in `/aeo/`
- Adding a new workshop drop in `/workshops/`

## What can be merged by the content owner

- Fixing broken links (with working replacement confirmed)
- Updating `owners.md` files
- Fixing typos that do not change meaning

## PR requirements

All PRs must satisfy the checklist in
../.github/PULL_REQUEST_TEMPLATE.md.

## Monthly publishing model

Each month, a contributor adds one Featured Drop under
`paths/featured/YYYY-MM-topic/` using the folder template:
- `README.md` — narrative and step-by-step flow
- `links.md` — canonical link list
- `owners.md` — who maintains accuracy and review cadence

## CODEOWNERS

Review assignments are defined in
../.github/CODEOWNERS.