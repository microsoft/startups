# 01 · Build fast

## Who this is for
Early-stage startup developers shipping a first production workload
on Azure — web apps, APIs, serverless functions, or data pipelines.

## What you will accomplish
- Deploy a working application to Azure
- Set up a CI/CD pipeline with GitHub Actions
- Apply cost-aware architecture patterns from day one
- Understand which Azure services fit common startup build patterns

## The path (recommended order)

1. **Choose your compute pattern**
   → https://learn.microsoft.com/en-us/azure/app-service/ — web apps and APIs
   → https://learn.microsoft.com/en-us/azure/container-apps/ — containerized microservices
   → https://learn.microsoft.com/en-us/azure/azure-functions/ — serverless event-driven workloads

2. **Set up your database**
   → https://learn.microsoft.com/en-us/azure/postgresql/
   → https://learn.microsoft.com/en-us/azure/cosmos-db/ — for global scale or NoSQL patterns

3. **Connect GitHub to Azure for CI/CD**
   → https://learn.microsoft.com/en-us/azure/developer/github/github-actions

4. **Apply cost-aware defaults**
   → https://learn.microsoft.com/en-us/azure/cost-management-billing/
   → Start on consumption-based tiers. Reserve capacity only when usage is predictable.

5. **Add observability from the start**
   → https://learn.microsoft.com/en-us/azure/azure-monitor/

## Canonical resources
→ ./links.md

## Ownership + freshness
→ ./owners.md