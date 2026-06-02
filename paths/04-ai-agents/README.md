# 04 · AI agents

## Who this is for
Startup developers building AI-powered products — agents, copilots,
LLM-backed workflows, or agentic SDLC automation — using Azure AI
Foundry, GitHub, and related Microsoft tooling.

## What you will accomplish
- Understand the Azure AI Foundry model and agent service
- Choose the right model and agent framework for your workload
- Build a basic agent with tool use and memory
- Understand how to take an agent to production safely
- Know how to connect your agent to enterprise systems

## The path 

1. **Start with Azure AI Foundry**
   [Foundry] (https://learn.microsoft.com/en-us/azure/ai-foundry/) is the production AI layer: model catalog, agent creation,
   inference, and observability. Start here before picking a framework.

2. **Choose your model**
   Startup credits coverage varies by [model](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/model-catalog-overview). Check the official source
   for current eligibility before building.

3. **Build your first agent**
   [AI Agents for Beginners — microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners)
   15 lessons, working code, Foundry-native. Start here for
   course-style onboarding.
   https://learn.microsoft.com/en-us/azure/ai-services/agents/

4. **Add tool use and MCP**
   [Understanding MCP](https://modelcontextprotocol.io/)
   [Azure MCP Server](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/overview)
   [MCP server guide](../../index/mcp.md)

5. **Design for enterprise-grade agents**
   Enterprise buyers expect: identity model, scoped permissions,
   audit logging, and policy alignment.
   [Enterprise readiness](../05-enterprise-readiness/)
   [Building trustworthy AI agents — ai-agents-for-beginners lesson 6](https://github.com/microsoft/ai-agents-for-beginners)

6. **Connect to GitHub workflows**
   [GitHub Copilot CLI + autopilot mode](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/)
   Agents that operate inside developer workflows (GitHub, VS Code)
   reduce friction and stay in the flow developers already use.

## Real-world example
**Overcut** — agentic SDLC automation built on AKS, Azure OpenAI,
Key Vault, Event Hubs, and ACR. Architecture designed for controlled
autonomy inside enterprise environments.
[Microsoft for Startups blog](https://startups.microsoft.com/blog)

## Canonical resources
[Canonical resources](./links.md)

## Ownership + freshness
[Ownership + freshness](./owners.md)
