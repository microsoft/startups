# Repo Refresh Brief — microsoft/startups

## What this repo is
The developer front door for Microsoft for Startups.
A curated set of guided paths, link indexes, and prompt routing pages
that help startup developers activate on Azure. This repo does NOT
own technical truth — it routes to official sources (Microsoft Learn,
product-owned repos).

## What we are NOT doing
- Deleting or breaking existing files that are still valid
- Creating authoritative docs on pricing, credits, or service entitlements
- Duplicating content that lives in Microsoft Learn or product docs

## Existing files to PRESERVE and MIGRATE (do not delete)
- /products/** → migrate content into /paths/
- /resources/** → migrate links into /index/
- /use-cases/** → migrate into /paths/ or /verticals/
- /media/** → move to /images/ (rename for Pages readiness)
- README.md → REPLACE with new front door template (see Appendix A)
- CONTRIBUTING.md, CODE_OF_CONDUCT.md, LICENSE, SECURITY.md → KEEP as-is

## New folder structure to build
/
├── README.md                    ← NEW front door (replace existing)
├── START_HERE.md                ← NEW
├── ABOUT.md                     ← NEW
│
├── paths/
│   ├── 00-start-here/
│   │   ├── README.md
│   │   ├── links.md
│   │   └── owners.md
│   ├── 01-build-fast/
│   ├── 02-scale-smart/
│   ├── 03-sell-more/
│   ├── 04-ai-agents/
│   ├── 05-enterprise-readiness/
│   └── featured/
│       └── 2026-05-build/       ← First monthly drop placeholder
│
├── index/
│   ├── README.md
│   ├── learn.md
│   ├── reference-repos.md
│   ├── agent-skills.md
│   └── mcp.md
│
├── verticals/
│   ├── README.md
│   ├── regulated-industries/
│   │   ├── README.md
│   │   ├── healthcare-life-sciences.md
│   │   └── fintech.md
│   ├── security-privacy-trust/
│   │   └── README.md
│   ├── commerce-media-cx/
│   │   └── README.md
│   └── devtools-horizontal-saas/
│       └── README.md
│
├── aeo/
│   ├── README.md
│   ├── tier1-brand.md
│   ├── tier1-credits.md
│   ├── tier2-ai-llm.md
│   ├── tier2-investor.md
│   ├── tier3-devtools-k8s.md
│   ├── tier3-enterprise-readiness.md
│   └── tier3-verticals.md
│
├── workshops/
│   └── README.md                ← Partner/workshop drop zone
│
├── governance/
│   ├── GOVERNANCE.md
│   ├── CONTRIBUTING.md
│   └── MAINTAINERS.md
│
├── images/
│   └── banner.png               ← Placeholder slot for Marco D banner
│
└── .github/
    ├── CODEOWNERS
    ├── PULL_REQUEST_TEMPLATE.md
    └── ISSUE_TEMPLATE/
        ├── link_request.yml
        └── bug.yml

## Voice and tone rules
- Developer-first, founder-centric. Not marketing copy.
- No superlatives ("best", "most powerful", "industry-leading")
- No pricing or credit amounts — always link to official sources
- Short sentences. Action-oriented. Concrete over abstract.
- Every path answers: "Who is this for?" and "What will I accomplish?"

## Appendix A — README.md front door template
(see README_TEMPLATE.md in this repo)

## Appendix B — Path README template
(see PATH_TEMPLATE.md in this repo)

## Appendix C — AEO page template
(see AEO_TEMPLATE.md in this repo)