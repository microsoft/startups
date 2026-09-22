# Startup-Scale Landing Zone

Use this path when a prototype is becoming a production workload and your team
needs a repeatable Azure foundation.

The [Startup-Scale Landing Zone baseline](https://github.com/ricmmartins/sslz)
is a community-maintained, custom landing zone implementation. Azure landing
zones include a platform foundation for governance, security, and shared
resources, plus application landing zones where workload teams deploy and
operate resources. Start with the
[Azure landing zone overview](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/)
for the Microsoft architecture and terminology.

## Who this is for

- Startup developers preparing a first production workload on Azure.
- A small team that owns both the cloud foundation and the application.
- Teams that want infrastructure as code they can review and adapt.

## When to use it

Use the baseline when you need an explicit starting point for resource
organization, identity, governance, networking, management, and security.
Review all
[Azure landing zone design areas](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-areas)
before deployment.

Choose the Microsoft
[Azure landing zone implementation options](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/implementation-options)
instead when your requirements call for the Microsoft platform landing zone
accelerator, Azure Verified Modules, or a portal-based deployment.

## Prerequisites

- An owner for platform decisions and an owner for the workload.
- An Azure tenant and the subscriptions that will receive the foundation.
- An identity with only the required
  [Azure RBAC scope](https://learn.microsoft.com/en-us/azure/role-based-access-control/scope-overview)
  for review and deployment.
- A reviewed choice between the Bicep and Terraform implementations in the
  published baseline.
- Written requirements for identity, resource organization, networking,
  security, management, governance, and deployment.

## Deployment and readiness flow

1. **Define requirements.** Record the decision owner and constraints for each
   Azure landing zone design area.
2. **Review the baseline.** Read the architecture, parameters, permissions, and
   resources in the published SSLZ repository. Change defaults that do not
   match your requirements.
3. **Preview the deployment.** Review the target scopes and proposed resource
   changes. For Bicep, use the
   [what-if operation](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-what-if)
   before deployment.
4. **Deploy and verify.** Start with a nonproduction environment. Verify
   resource organization, role assignments, policy results, networking, and
   monitoring before using the pattern for production.
5. **Review the workload.** Use the
   [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/)
   to review workload decisions across reliability, security, cost
   optimization, operational excellence, and performance efficiency.
6. **Revisit the foundation.** Reassess the design when workload, team,
   connectivity, regional, or governance requirements change.

## Responsibilities

| Owner | Responsibility |
|---|---|
| Founder or platform owner | Approve tenant, subscription, identity, governance, networking, and regional decisions |
| Workload owner | Deploy and operate the application resources inside the agreed foundation |
| Security and operations owner | Define controls, monitoring, recovery, and response requirements |
| Baseline maintainer | Maintain implementation code and document its supported scope |

One person can hold several roles. Keep each decision and operational duty
explicit.

## Boundaries

- SSLZ is a custom implementation. It is not the Microsoft Azure Landing Zones
  IaC accelerator and does not replace Microsoft Learn guidance.
- The baseline is a starting point, not proof of security, compliance,
  reliability, or production readiness.
- Workload architecture, data classification, recovery targets, service
  limits, and regional availability still require workload-specific review.
- Review infrastructure code and proposed changes before deployment. Use
  least-privilege access at the required scope.

The published baseline is deployable infrastructure code. Any agent-led
planning experience in the SSLZ project is optional and separate. It can help
organize decisions, but it is not the baseline, a deployment mechanism, or
evidence that the environment is ready.

## Canonical resources

[Canonical resources](./links.md)
