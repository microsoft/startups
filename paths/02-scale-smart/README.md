# 02 · Scale smart

## Who this is for
Startup developers moving a working product toward production-grade
architecture — multi-tenant, observable, resilient, and cost-efficient.

## What you will accomplish
- Move from single-tenant to multi-tenant architecture on Azure
- Implement identity and access patterns using Microsoft Entra
- Add observability, alerting, and structured logging
- Apply Kubernetes-based scaling when appropriate
- Prepare infrastructure for enterprise customer onboarding

## The path (recommended order)

1. **Design your multi-tenant architecture**
   → https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/overview
   Choose your isolation model (pooled, siloed, or hybrid) before scaling.

2. **Implement identity with Microsoft Entra**
   → https://learn.microsoft.com/en-us/entra/identity/
   → https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview

3. **Scale container workloads with AKS**
   → https://learn.microsoft.com/en-us/azure/aks/
   → https://learn.microsoft.com/en-us/azure/aks/best-practices

4. **Add observability**
   → https://learn.microsoft.com/en-us/azure/azure-monitor/containers/container-insights-overview
   → https://learn.microsoft.com/en-us/azure/azure-monitor/app/distributed-trace-data

5. **Harden your secrets management**
   → https://learn.microsoft.com/en-us/azure/key-vault/
   → Use workload identity + External Secrets Operator instead of static credentials.

6. **Plan for resilience**
   → https://learn.microsoft.com/en-us/azure/reliability/

## Canonical resources
[Canonical resources](./links.md)

## Ownership + freshness
[Ownership + freshness](./owners.md)