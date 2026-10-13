# Stoupons Agents

An AI multi-agent system that runs the Stoupons home-services process from first inquiry to installation, payment, maintenance and referral. A **Manager Agent** coordinates 16 specialized **worker agents**, and policy, approvals and audit logs keep everything grounded in real business data.

This repo is also a learning curriculum. The agents are built in order from easiest to hardest, and each one teaches new Forward Deployed Engineer (FDE) skills.

## Start here

1. [docs/PHASE0_SETUP.md](docs/PHASE0_SETUP.md): install the tools and make your first Claude API call
2. [docs/ROADMAP.md](docs/ROADMAP.md): the 52-week plan, phase by phase, with exit checklists
3. [docs/AGENTS.md](docs/AGENTS.md): all 17 agents, what they do, their tools, and how to build each one
4. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): how the pieces fit together
5. [docs/MANAGER_DESIGN.md](docs/MANAGER_DESIGN.md): the Manager Agent, guardrails, RAG and fine-tuning
6. [docs/TOOLS_AND_PRICING.md](docs/TOOLS_AND_PRICING.md): free tools, alternatives and prices

## Folder layout

| Folder | What goes here |
|---|---|
| `agents/` | One folder per agent (`agents/knowledge/`, `agents/lead_qualification/`, …) |
| `core/` | Shared code: LLM client, tool registry, guardrails, tracing, approval queue |
| `data/mock/` | Fake JSON data you use until real APIs and databases exist |
| `knowledge/` | Approved Stoupons documents (manuals, FAQs, warranty text) for RAG |
| `evals/` | Golden test cases for each agent |
| `tests/` | Automated tests (pytest) |
| `app/` | Chat UI and Admin Dashboard (Streamlit) |

## Golden rules

1. Data from the system of record beats model memory.
2. An LLM never invents prices, slots, payment status or availability. Those come from tools.
3. Every action that changes business data goes through a typed tool that checks permissions.
4. Risky actions go to a human (you) through the approval queue.
5. Every step is logged and traced.
6. When required data is missing, escalate. Never guess.
