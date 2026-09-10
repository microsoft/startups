# Security and content safety checks

This repository publishes code samples, demos, and developer guidance. Treat
every contribution as content that can be copied into a real workload. The CI
controls below reduce common risks, but they do not replace security, privacy,
legal, or Responsible AI review.

## Automated checks

| Check | What it covers | Workflow |
|---|---|---|
| Content safety | High-confidence secrets, personal data indicators, cloud identifiers, internal links, confidential markings, risky files, notebook outputs, and unsafe AI-control settings | `content-safety.yml` |
| Trivy | Secrets, vulnerable dependencies, and infrastructure-as-code misconfigurations | `content-safety.yml` |
| Microsoft DevSkim | Insecure coding patterns across common sample languages | `content-safety.yml` |
| CodeQL | Semantic code scanning for every supported language detected in the repository | `codeql.yml` |
| Dependency review | New vulnerable dependencies and dependency license information | `dependency-review.yml` |
| zizmor | GitHub Actions security, including dangerous triggers, permissions, and unpinned actions | `workflow-security.yml` |
| Markdown lint | Structural Markdown problems while preserving the existing content style | `markdownlint.yml` |
| Link checker | Broken links in published Markdown | `link-checker.yml` |
| PR attestation | Human confirmation for public data, privacy, credentials, Responsible AI, and sample safety | `pr-attestation.yml` |

The content safety scanner is intentionally repository-native and uses only the
Python standard library. Run it locally:

```bash
python -m unittest discover -s .github/scripts -p "test_*.py"
python .github/scripts/content_safety.py
```

The scanner never prints a suspected secret's value.

## Responsible AI review

Pattern matching cannot determine whether an AI system is responsible or safe.
For AI samples and demos, reviewers must apply the Microsoft Responsible AI
lifecycle:

1. **Identify:** Document the intended use, affected users, foreseeable misuse,
   limitations, and potential harms.
2. **Measure:** Include representative evaluations for quality, safety,
   groundedness, fairness, and prompt-injection or jailbreak resistance as
   appropriate.
3. **Mitigate:** Keep platform safety controls enabled, minimize data sent to
   models, protect system prompts and tools, constrain agent permissions, and
   add human review for consequential actions.
4. **Operate:** Explain monitoring, feedback, incident response, model or prompt
   versioning, and how users can recognize AI-generated output.

Higher-risk scenarios, including biometric identification, social scoring,
emotion recognition, predictive policing, or autonomous decisions in
employment, credit, health, or legal contexts, require explicit specialist
review before publication.

Use synthetic evaluation data. Do not commit real customer prompts, model
outputs, transcripts, support records, tenant identifiers, or production logs.

## Privacy and confidential information

Before publication:

- Replace names, email addresses, phone numbers, account identifiers,
  subscription IDs, tenant IDs, and local usernames with clearly synthetic
  values.
- Remove notebook outputs and execution counts.
- Do not include internal Microsoft links, screenshots, telemetry, customer
  architecture, private meeting content, or material marked internal only.
- Preserve only the minimum sample data needed to explain the scenario.
- Confirm that images and document metadata contain no private information.

## Credentials and secrets

Use placeholders such as `<your-api-key>` and load runtime credentials from a
managed identity, workload identity, secret store, or environment variable.
Never commit a real credential, even temporarily. If one is committed, revoke
or rotate it immediately; deleting it in a later commit is not sufficient.

The repository administrators should enable these GitHub settings:

- Secret scanning, validity checks, and push protection.
- Dependabot alerts and security updates.
- Code scanning and code-scanning merge protection.
- A ruleset for `master` that requires pull requests, CODEOWNERS review, and all
  CI checks in this document.

## Exceptions and false positives

Prefer synthetic content or a safer rewrite. If a non-secret finding is
intentional, add a narrowly scoped inline suppression on the same line or the
line immediately before it:

```text
content-safety: allow RULE_ID -- reason of at least eight characters
```

Path-wide rule exceptions belong in
`.github/content-safety-allowlist.json` and require review from the owners of
`.github/`. Secret findings cannot be suppressed or excluded. Do not add real
secrets as scanner test fixtures; construct synthetic values at test runtime
instead.

## Adding a new sample

Every sample should include:

- Setup and teardown instructions.
- The minimum permissions required.
- A `.env.example` or equivalent with placeholders only.
- Pinned direct dependencies and a lock file when the ecosystem supports one.
- Tests for the behavior and failure modes demonstrated.
- Security, privacy, cost, and production-readiness limitations.
- For AI samples, scenario-specific evaluations and documented safety
  mitigations.
