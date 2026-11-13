# Bot HQ — External Capability Benchmark

**Programme:** Tinlance Agent Systems (TAS) / TSIC  
**Reference:** https://github.com/nickvasilescu/bot-hq  
**Product site:** https://bops.bot (separate product reference; do not conflate with this repository)  
**Classification:** Approved external product/implementation benchmark  
**Disposition:** Benchmark only. No fork, import, deployment, production dependency, infrastructure provisioning or spend is authorized by this record.  
**Inspection date:** 2026-11-13  
**Repository licence reported by GitHub:** MIT. Preserve copyright and licence notices; re-check the exact revision and all bundled assets/dependencies before any reuse.  
**Repository status reported by README:** Experimental.

## 1. Purpose

Evaluate Bot HQ as a practical reference for a multi-agent workforce interface built around persistent Hermes agents, per-agent screens/workspaces, application integrations, voice, routines and human supervision.

Bot HQ is a continuation/successor-style reference related to the earlier Grokbot Clone research. Treat it as a distinct benchmark record because its implementation and integration surface add further evidence; do not double-count shared lineage as independent proof of the same capability.

## 2. Product and implementation observations

The public README and architecture material describe:

- A team of conversational AI agents, each with a name, role, memory, model configuration, tasks and a screen.
- Hermes Agent as the underlying agent engine, with a gateway per additional agent.
- Orgo providing a cloud Linux computer and screens; the README describes one shared computer with a screen per bot and a maximum of four screens/bots.
- Separate Hermes homes/gateways for additional bots, including separate model configuration, sign-in, memory, browser profile and files.
- A Node/Hono server, React client and SQLite-backed application state.
- MCP endpoints exposed by the application for agent tools, including connected applications, tasks, routines, library functions and bot-to-bot messaging.
- Composio integrations, with approval cards for app write actions such as sending, posting or deleting.
- xAI realtime voice and X search integration.
- Recurring routines, task lists, generated-file library, bot-to-bot messages, live screen viewing and human mouse/keyboard takeover.
- The first bot can use an already-running Hermes agent; additional bots receive separate homes and gateways.

These are README/architecture claims and source-level observations, not independent runtime acceptance. The benchmark must pin an exact repository commit before repeatable evaluation and distinguish documented, code-verified and runtime-tested behavior.

## 3. Benchmark dimensions

1. **Agent identity and lifecycle:** provisioning, stable IDs, roles, model profiles, per-agent home, activation, shutdown, deletion and recovery.
2. **Workspace and computer model:** per-agent screen, browser profile, filesystem, process namespace, shared host boundaries, resource allocation and concurrent operation.
3. **Harness integration:** Hermes gateway lifecycle, HTTP/SSE and MCP boundaries, provider/model selection, restart behavior and compatibility with alternative harnesses.
4. **Agent collaboration:** bot-to-bot messaging, task delegation, routing, shared context, loop/cycle prevention, bounded delegation and result handback.
5. **Application integrations:** Composio OAuth, tool discovery, read/write separation, approval UX, credential storage, revocation and audit.
6. **Computer use:** browser/desktop control, shell access, live viewing, takeover/handback, session isolation and command mediation.
7. **Memory and continuity:** per-agent memory, browser/profile persistence, files, task context, provenance, retention, deletion and cross-agent sharing.
8. **Routines and durable tasks:** scheduling, timezone correctness, retries, missed-run behavior, pause/resume, cancellation, idempotency and event history.
9. **Voice and multimodal UX:** realtime voice, dictation, tool handoff, session continuity and consistent governance across modalities.
10. **Operational visibility:** streaming task steps, status, elapsed time, tool history, artifacts, logs, errors and cost attribution.
11. **Security and tenant boundaries:** authentication, allowlists, session management, MCP bearer-token scope, browser/shell authorization, credential inheritance, shared-computer isolation, prompt injection, SSRF/DNS rebinding, network egress and audit completeness.
12. **Reliability and economics:** concurrency, four-screen ceiling, startup/restart time, gateway health, SQLite durability, resource contention, provider fallback and cost per completed task.

## 4. Security findings and TAS design implications

The initial source review identified important patterns to test and controls TAS must not inherit without remediation:

- **Shared-computer boundary:** separate screens and Hermes homes do not prove OS-level isolation. Test cross-agent filesystem, process, browser-profile, network and credential access.
- **Browser/shell authorization:** app integration approval cards do not establish that browser and shell actions are governed by the same approval path. Trace every consequential action to the central Platform authorization boundary.
- **Credential inheritance:** inspect agent creation and provisioning paths for copied provider credentials, auth files or inherited sessions. TAS must use explicitly scoped, revocable credentials and must not silently copy secrets between agent identities.
- **MCP authentication versus authorization:** a bearer token alone is not fine-grained permissioning. Require per-agent, per-tool, per-resource and per-action scopes, budgets, expiry, revocation and audit.
- **Public exposure and authentication configuration:** verify allowlist defaults, setup flow, session security, webhook validation and reverse-proxy assumptions. Do not expose a local or development server as a production service.
- **Persistent state:** validate SQLite durability, backup/restore, concurrent writes, corruption recovery, tenant separation and audit retention before considering production suitability.
- **Experimental maturity:** the README labels the project experimental. Do not infer enterprise readiness from a polished interface or feature breadth.

These are benchmark risks and validation targets, not a claim that every listed weakness has been independently reproduced in a live deployment.

## 5. What TAS should evaluate for adoption as concepts

- Agent roster/contact-card UX and per-agent configuration.
- Live task-step streaming and a human-readable execution timeline.
- Screen viewing and explicit human takeover/handback.
- Per-agent workspaces and browser profiles, provided true isolation is independently established.
- Persistent per-agent tasks, routines and generated-artifact library.
- Bot-to-bot messaging and structured delegation.
- Voice-to-durable-task continuity.
- Composio-style connector onboarding and explicit write-approval UX.
- A harness adapter pattern that keeps the agent engine replaceable.

Any adoption must preserve TAS authority boundaries:

**TADL declares → OS composes → SDK transports → Platform authorizes and executes → TSIC verifies.**

All computer, shell, browser, MCP, connector, voice, routine and delegation actions must pass through the Agent Platform's centralized policy and authorization controls. Models, harnesses, memory and UI approval cards cannot independently grant authority.

## 6. FCP traceability

- **FCP-03:** threat-model comparison, shared-host boundaries, authentication, credential handling, network controls and evidence requirements.
- **FCP-04:** agent identity, lifecycle, workspaces, harness adapters, durable tasks and delegation.
- **FCP-05:** MCP, application integrations, OAuth, browser/computer tools and human takeover.
- **FCP-06:** per-agent memory, files, provenance, retention, deletion and skill/context continuity.
- **FCP-07:** routines, scheduling, event-driven execution, retries and cancellation.
- **FCP-08:** roster, conversations, task timeline, voice, screen viewer and human handoff UX.
- **FCP-09:** concurrency, resource consumption, latency, reliability and unit economics.
- **FCP-10:** independent security assessment, tenant isolation, authorization bypass, recovery and end-to-end acceptance.

The benchmark is queued behind the existing serial phase gate. FCP-03 remains active/incomplete; FCP-04–FCP-10 remain gated. This record does not authorize pulling future-phase implementation forward.

## 7. Benchmark execution protocol

Before scoring:
1. Record the exact Bot HQ commit SHA, dependency lockfiles and inspection timestamp.
2. Map every claim to README, architecture docs, source locations or reproducible tests.
3. Build a capability matrix with status values: documented, code-verified, runtime-tested, independently verified, not supported, or unknown.
4. Test at least two agents attempting cross-agent filesystem, browser, process, MCP and credential access.
5. Trace app writes, shell commands, browser actions, scheduled jobs and delegated actions through the same authorization and audit path.
6. Test credential creation, inheritance, rotation, revocation and deletion.
7. Test interrupted tasks, gateway restart, host restart, routine retry, duplicate execution and cancellation.
8. Record latency, concurrency limits, failure modes and cost per successfully completed task.
9. Review licence and third-party asset/dependency terms before any code reuse.

## 8. Explicit exclusions

- No code copying, fork, dependency, deployment or production coupling.
- No changes to Agent Platform, Agent OS, SDK, TADL, TSIC, Tinlyt, FusionOps, ThreatFade or other production systems.
- No new cloud resources, credentials, paid services or spend.
- No phase transition or acceptance claim.
- No claim of production security, tenant isolation or enterprise readiness based solely on source inspection.

**Acceptance note:** Adding Bot HQ to the benchmark registry authorizes evaluation as a reference only. It does not approve reuse or adoption of its implementation.
