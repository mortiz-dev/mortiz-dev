<p align="center">
  <img src="./assets/profile-banner.svg" alt="Miguel Ortiz — AI infrastructure engineer" width="100%">
</p>

I build AI infrastructure in TypeScript and Python: multi-provider SDKs,
durable agent runtimes, and MCP integrations. My background in banking
analytics shapes how I approach data quality, traceability, and reliable systems.

Founder of [Zhivex](https://github.com/Zhivex), building provider-agnostic AI tools,
coding-agent runtimes, TypeScript and Python SDKs, and MCP integrations. My public
work includes agent safety, persistence, provider integrations, and release validation.

## Selected work

### [Zhivex Harness / Code](https://github.com/Zhivex/zhivex-harness)

Work on a repository with a local coding agent. Review edits and consequential
actions through explicit permissions, and continue conversations across restarts.
Harness provides the runtime and terminal assistant; Code is a separate CLI on
that engine.

[Quickstart](https://github.com/Zhivex/zhivex-harness#quick-start) ·
[Permissions and limits](https://github.com/Zhivex/zhivex-harness#permissions-and-limits) ·
[Harness on npm](https://www.npmjs.com/package/@zhivex-ai/harness) ·
[Code on npm](https://www.npmjs.com/package/@zhivex-ai/code)

### [Zhivex AI SDK — TypeScript](https://github.com/Zhivex/zhivex-ai-sdk)

Build agents and AI applications around a shared model contract, with explicit
provider capabilities, tools, streaming, and durable execution.

**My contribution:** hardened retries, routing fallbacks, and agent generation
safety; added strict unknown-tool validation and recovery.
[Contribution](https://github.com/Zhivex/zhivex-ai-sdk/pull/90) ·
[Quickstart](https://github.com/Zhivex/zhivex-ai-sdk/blob/main/docs/QUICKSTART.md) ·
[Human approval example](https://github.com/Zhivex/zhivex-ai-sdk/blob/main/examples/agents/approval-hitl.ts) ·
[npm package](https://www.npmjs.com/package/@zhivex-ai/sdk)

### [Zhivex AI SDK — Python](https://github.com/Zhivex/zhivex-ai-sdk-py)

Build async agents with tools and a portable provider contract, then add durable
state, approvals, and observability as the application needs them.

**My contribution:** implemented durable onboarding and operational evidence,
including preservation of typed tool inputs when resuming after approval.
[Contribution](https://github.com/Zhivex/zhivex-ai-sdk-py/pull/41) ·
[Quickstart](https://github.com/Zhivex/zhivex-ai-sdk-py/blob/main/docs/QUICKSTART.md) ·
[Runnable agent](https://github.com/Zhivex/zhivex-ai-sdk-py/blob/main/examples/agents/quickstart_agent.py) ·
[PyPI package](https://pypi.org/project/zhivex-ai-sdk/)

### [MCP BCRA](https://github.com/mortiz-dev/mcp-bcra)

Connect agent tools to official APIs from Argentina's Central Bank. For example,
discover a public statistical series and retrieve its history with validated
inputs and structured responses.

**My contribution:** expanded BCRA API coverage and refactored the tools and shared
HTTP infrastructure.
[Contribution](https://github.com/mortiz-dev/mcp-bcra/commit/286095385fede60593989b588c021d70791ac5f7) ·
[Setup and tools](https://github.com/mortiz-dev/mcp-bcra#instalación-y-ejecución)

## Banking analytics & Power BI

I build and maintain Power BI dashboards for banking teams, combining semantic
modeling, DAX, SQL, Power Query, data quality checks, and operational reporting.
My work turns reporting requirements into defined KPIs and data models that
support executive and operational analysis.

Banking projects and their semantic models remain confidential. Public examples
are independent demonstrations created with synthetic data.

[Explore the synthetic analytics example](./case-studies/service-operations/README.md)
— dataset, SQL, a visual summary, and a Power BI modeling recipe.

## Try an agent approval flow

[Run the approval demo](./demos/agent-approval/README.md): an agent proposes a
simulated action, pauses for approval, and executes it only when you approve.
It uses the real Zhivex agent runtime with a scripted model, synthetic inputs,
and no API keys. You can also deny the action and verify that it never executes.

## Languages & tools

<p align="center">
  <img src="./assets/tech-stack.svg" alt="TypeScript, Python, SQL, Power BI, PostgreSQL, Bun, Node.js, MCP, and GitHub Actions" width="100%">
</p>

## Connect

Based in Buenos Aires, Argentina. I work in English and Spanish.

For conversations about AI infrastructure, SDK integrations, or data analytics,
connect with me on [LinkedIn](https://www.linkedin.com/in/mortiz94/) or
[X](https://x.com/mortiz_dev).

[Zhivex](https://www.zhivex.com) · [SDK documentation](https://sdk.zhivex.ai) ·
[Open-source projects](https://github.com/Zhivex)
