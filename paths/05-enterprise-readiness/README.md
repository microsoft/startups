# 05 · Enterprise readiness

## Who this is for
Startup developers preparing to pass enterprise security reviews,
complete compliance assessments, or onboard their first large
enterprise customers.

## What you will accomplish
- Implement zero-trust identity and access patterns
- Harden secrets management and eliminate static credentials
- Add structured audit logging enterprise buyers can review
- Understand compliance frameworks relevant to your vertical
- Know what enterprise procurement teams evaluate technically

## The path (recommended order)

1. **Implement zero-trust identity**
   → [Zero-trust security on Azure — Microsoft Learn](https://learn.microsoft.com/en-us/startups/)
   → https://learn.microsoft.com/en-us/entra/identity/
   → https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview
   No static credentials. Workload identity for service-to-service.

2. **Harden secrets management**
   → https://learn.microsoft.com/en-us/azure/key-vault/
   → Inject secrets via workload identity + External Secrets Operator.
     Do not store secrets in environment variables or config files.

3. **Add audit logging**
   Enterprise buyers need: who did what, when, and why.
   → https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/activity-log
   → https://learn.microsoft.com/en-us/azure/defender-for-cloud/

4. **Understand compliance frameworks for your vertical**
   → [Health & Life Sciences vertical](../../verticals/regulated-industries/healthcare-life-sciences.md)
   → [Financial services vertical](../../verticals/regulated-industries/fintech.md)
   → [Cybersecurity vertical](../../verticals/security-privacy-trust/)
   → https://learn.microsoft.com/en-us/azure/compliance/

5. **Prepare your enterprise readiness brief**
   Buyers commonly ask for:
   - A one-paragraph identity model explanation
   - A permission matrix (default scopes vs optional scopes)
   - A data residency statement
   - An audit log export example
   - A rollback and incident response plan

6. **Review the Azure Marketplace technical requirements**
   Required for co-sell and enterprise GTM motions.
   → [Sell more](../03-sell-more/)

## Canonical resources
[Canonical resources](./links.md)

## Ownership + freshness
[Ownership + freshness](./owners.md)