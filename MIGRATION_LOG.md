# Migration log

**Migration date:** April 22, 2026
**Branch:** repo-refresh-2026

---

## Files migrated

| Original file | Migrated to | Notes |
|---|---|---|
| products/azure-products-free-trial.md | paths/01-build-fast/links.md, paths/04-ai-agents/links.md | Valid canonical links appended to new structure |
| products/azure-products-free.md | paths/01-build-fast/links.md, paths/04-ai-agents/links.md | Valid canonical links appended to new structure |
| products/azure-products.md | paths/01-build-fast/links.md, paths/04-ai-agents/links.md | Valid canonical links appended to new structure |
| resources/learning-resources.md | index/learn.md | Valid Learn modules appended to new index |
| use-cases/chat-bots.md | paths/04-ai-agents/links.md | Valid bot service links appended to new structure |

---

## Links skipped

| URL | Original file | Reason skipped |
|---|---|---|
| https://www.youtube.com/watch?v=Wmc7C4RRjBI | resources/learning-resources.md | Not authoritative source (YouTube video) |
| https://azure.microsoft.com/pricing/details/bot-service/?WT.mc_id=startups-github-cxa | use-cases/chat-bots.md | States pricing or entitlements |

---

## Files not migrated

| File | Reason |
|---|---|
| media/ (all files) | Image files with no migratable content |
| products/README.md (original) | File did not exist; created deprecation notice instead |
| resources/README.md (original) | File did not exist; created deprecation notice instead |
| use-cases/README.md (original) | File did not exist; created deprecation notice instead |

---

## Folders pending deletion

The following folders are deprecated and pending removal
after review:

- /products/
- /resources/
- /use-cases/

Do not delete until the migration log has been reviewed
and approved by the content owner.