# Standards Landscape and Interoperability Boundaries

**Status:** Draft for Harness Operations Reference Model 0.1

## Purpose

Harness Operations does not begin from an empty standards or operational landscape.

Existing protocols already define important boundaries around AI applications, coding agents, independent agent systems, tools, context, tasks, artifacts, permissions, and telemetry. Existing operational disciplines also address many of the production concerns of AI agents. The goal of Harness Operations is not to rename or replace those semantics or practices.

This document answers a narrower question:

> **Which existing standards and adjacent disciplines already define relevant boundaries, and what harness-specific operational concerns remain?**

The landscape is intentionally selective. It is not a catalog of agent frameworks, products, or every protocol related to AI systems.

## Guiding rule: compose before inventing

Harness Operations should prefer this order:

1. use a native Harness capability when it already expresses the required semantics;
2. use or map an established open standard where it defines the relevant boundary;
3. reuse established operations, security, and governance practice rather than renaming it;
4. adapt between different native or standardized semantics without erasing meaningful differences;
5. propose new interoperability semantics only when a demonstrated cross-harness gap remains.

A new Harness Operations protocol is therefore not an assumption of Reference Model 0.1.

## Boundary map

The standards described here operate at different boundaries and can coexist in one system.

```text
                         Operators
                            │
                            │
                  Harness Operations model
             lifecycle · governance · evidence
               routing · limits · intervention
                            │
           ┌────────────────┼────────────────┐
           │                │                │
           ▼                ▼                ▼
      coding client     control layer    other clients
           │                                 │
          ACP                         native Harness APIs
           │                                 │
           ▼                                 ▼
       Harness / agent systems / Harness Instances
           │                │                │
           ├──── MCP ───────┼──► tools, context, services
           │                │
           ├──── A2A ───────┼──► independent agent systems
           │                │
           └── telemetry ───┴──► OpenTelemetry
```

This diagram is illustrative, not a required architecture. A Harness Operations system may use none, one, or several of these standards.

## AgentOps and broader agent operations

`AgentOps` and `agent operations` already describe a broad production-operations space around AI agents. The terminology is established enough that Harness Operations should not claim to have discovered “operations for agents,” but current usage is not uniform enough to treat AgentOps as one normative reference model.

Examples of current usage include:

- AWS describes AgentOps as the operational discipline for deploying, managing, and continuously improving AI agents in production, spanning governance and security, build and operations, evaluation, and observability.
- The AgentOps project emphasizes testing, debugging, deployment, observability, monitoring, cost tracking, and evaluation for AI agents and LLM applications.
- Published research has used AgentOps primarily as a taxonomy and discipline for observability of LLM agents.

Background:

- [AWS: AgentOps — operationalize agentic AI at scale](https://aws.amazon.com/blogs/machine-learning/agentops-operationalize-agentic-ai-at-scale-with-amazon-bedrock-agentcore/)
- [AgentOps documentation](https://docs.agentops.ai/v2/introduction)
- [AgentOps: Enabling Observability of LLM Agents](https://arxiv.org/abs/2411.05285)

### Relationship to Harness Operations

Harness Operations is deliberately narrower and **harness-centric**.

It uses the Harness as the primary operational unit because the Harness concretely mediates session lifecycle, context, tools, permissions, execution, persistence, and other runtime semantics. This is especially relevant when an operator must work across Harnesses that expose materially different session models, permission mechanisms, capabilities, execution environments, or persistence behavior.

Harness Operations can therefore be understood as complementary to, or a specialization within, broader agent-operations practice. It should borrow ordinary production practices from AgentOps, DevOps, SRE, platform engineering, security engineering, and AI governance rather than rename them.

The remaining value of the reference model is not a claim to own agent operations. It is to give heterogeneous Harnesses a shared descriptive operational vocabulary while preserving their native semantics.

## Model Context Protocol (MCP)

### Current scope

The Model Context Protocol is an open standard connecting AI applications to external systems that expose tools, resources, prompts, and related capabilities.

The current MCP specification revision, **2026-07-28**, moved the protocol core to a stateless request/response model and formalized an extension mechanism. Long-running work is available through the **Tasks extension**, while other extensions cover additional concerns.

Current authoritative background:

- [MCP 2026-07-28 specification release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [MCP specification](https://modelcontextprotocol.io/specification/2026-07-28)

### Relationship to Harness Operations

MCP can provide important operational building blocks, including tool and service Capabilities, external context and resources, authorization boundaries associated with MCP servers, long-running protocol interactions through Tasks, and capability/extension discovery.

Harness Operations should use those semantics where MCP is the actual integration boundary.

An MCP tool can map to a Capability available to an Agent Session. An MCP Task may map to part of a Run—or to the Run itself—when their operational lifecycles are genuinely equivalent.

### What Harness Operations should not redefine

Harness Operations should not create parallel wire semantics for MCP tool invocation, resources, prompts, authorization, Tasks, or capability discovery when MCP is in use.

### What remains outside MCP's core purpose

MCP does not, by itself, define the complete operational model for heterogeneous Harness Instances and Agent Sessions across unrelated Harnesses. Harness Operations additionally describes concerns such as cross-harness lifecycle and attention state, routing and placement, governance Authority and Delegation, cross-system Limits and Usage, human intervention across different native permission models, and historical execution evidence.

MCP is evolving quickly. These boundaries must be reviewed against future specification releases rather than treated as permanent territory.

## Agent Client Protocol (ACP)

### Current scope

The Agent Client Protocol standardizes communication between code editors or interactive clients and coding agents.

ACP defines a client/agent boundary including session lifecycle, prompts and updates, tool-call presentation, permission requests, configuration, and other coding-agent interactions.

As of Reference Model 0.1 development, **ACP v1 is the stable protocol family** while protocol v2 remains an explicitly unstable/draft evolution.

Current authoritative background:

- [ACP repository](https://github.com/agentclientprotocol/agent-client-protocol)
- [ACP changelog](https://github.com/agentclientprotocol/agent-client-protocol/blob/main/CHANGELOG.md)

### Relationship to Harness Operations

Where a coding Harness is exposed through ACP:

- an ACP agent implementation can represent or front a Harness;
- ACP Session semantics can map to Harness Operations Agent Session;
- ACP permission interactions can provide native execution-control or Approval inputs depending on their governance meaning;
- ACP updates can contribute operational Events and state;
- the client can act as an operational interface without becoming a universal Control Plane.

### Preserve ACP Session semantics

Harness Operations `Agent Session` is deliberately broader than ACP `Session`.

An implementation using ACP should retain the ACP session identifier and lifecycle as native semantics. It should not translate ACP into a different generic lifecycle merely for consistency with another Harness.

A broader Harness Operations Run may contain or correlate one or more ACP Sessions when the operational objective extends beyond an individual ACP session.

### What remains outside ACP's core purpose

ACP primarily defines interaction between a client and a coding agent. It does not attempt to define a general operational model for multiple unrelated Harness products, cross-harness workflows, fleet placement, governance across environments, or general-purpose non-coding Harnesses.

Harness Operations should therefore compose ACP rather than replace it.

## Agent2Agent Protocol (A2A)

### Current scope

The Agent2Agent Protocol is an open standard for communication and interoperability between independent, potentially opaque agent systems.

A2A **1.0** defines normative concepts including:

- `AgentCard` for discovery, identity, skills, supported interfaces, and security requirements;
- `Message` for communication;
- `Task` as the stateful unit of work with a defined lifecycle;
- `Artifact` as task output;
- streaming and push notification mechanisms;
- protocol extensions.

Current authoritative background:

- [A2A Protocol Specification](https://github.com/a2aproject/A2A/blob/main/docs/specification.md)
- [A2A changelog](https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md)

### Relationship to Harness Operations

A2A is particularly relevant when one Harness or agent system delegates to or collaborates with another independent agent system over a network boundary.

Possible mappings include:

- A2A AgentCard capabilities and skills informing Capability or routing decisions;
- an A2A Task mapping to a Run when the Task and operational lifecycle have the same scope;
- an A2A Task representing one child execution within a broader Run when the larger operational objective spans multiple Tasks or Harnesses;
- an A2A Artifact mapping directly to a Harness Operations Artifact when A2A is the producing boundary;
- A2A Messages remaining native communication objects.

### Task and Run are not automatically equivalent

A2A `Task` is a normative protocol object. Harness Operations `Run` is a broader descriptive concept for operational identity.

Implementations should not create both objects without need. If one A2A Task fully represents the lifecycle operators need to govern and observe, it can serve as the operational Run identity. A separate Run becomes useful only when the lifecycle is genuinely broader.

### Artifact semantics

A2A explicitly separates Messages from Artifacts and defines Artifact as task output. When A2A is used, those semantics are authoritative. Harness Operations should add only operational provenance or governance relationships rather than redefine the protocol representation.

## OpenTelemetry

### Current scope

OpenTelemetry provides vendor-neutral APIs, SDKs, protocols, and semantic conventions for traces, metrics, logs, events, and related observability data.

Generative-AI semantic conventions are actively evolving. The dedicated OpenTelemetry GenAI semantic-conventions project currently marks its conventions as **Development** and covers model calls, agent invocation, workflow invocation, planning, tool execution, memory operations, metrics, and events.

Current authoritative background:

- [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)
- [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai)

### Relationship to Harness Operations

OpenTelemetry should be the first place to look when implementations need common telemetry representation.

Potential mappings include:

- Event facts to OTel logs/events/spans where applicable;
- Usage measurements to OTel GenAI metrics or other resource metrics;
- Agent Session and Run correlations to traces, spans, attributes, or linked telemetry without requiring that the reference-model identity equal one span;
- native Harness model/tool/workflow telemetry to existing GenAI conventions.

### Run is not a trace

A Harness Operations Run is an operational lifecycle identity. An OpenTelemetry trace is telemetry context used to correlate observability signals.

A Run may correspond neatly to one trace in some implementations, but the reference model does not require it. A Run may outlive telemetry retention, span multiple traces, include human Approval intervals, or aggregate systems whose trace contexts are not continuous.

### Event is not an OpenTelemetry Event schema

Harness Operations uses Event as the abstract fact of an observable operational occurrence. Implementations should map that fact to current OpenTelemetry signal guidance rather than invent a second generic telemetry schema.

### Maturity matters

The GenAI semantic conventions are currently Development status. Harness Operations should track and prefer them where useful without describing evolving attributes or span shapes as permanently stable.

## Open Agent Management Protocol (OpAMP)

### Why it appears in this landscape

OpenTelemetry also defines the **Open Agent Management Protocol (OpAMP)**, currently Beta.

Despite the name, OpAMP's “Agents” are data-collection/telemetry agents such as collectors and log forwarders, not AI agent Harnesses.

OpAMP is therefore not an AI-agent interoperability standard and should not be confused with A2A or Harness Operations.

It is nevertheless valuable prior art because it addresses a structurally similar operational problem: remote management of a heterogeneous fleet of independently implemented agents.

OpAMP includes concepts such as stable instance identity, capability negotiation, status and health reporting, heartbeats, effective versus remote configuration, partial interoperability, local restrictions on remote configuration, and package/update state.

Current authoritative background:

- [Open Agent Management Protocol](https://opentelemetry.io/docs/specs/opamp/)

### Lessons rather than mappings

Harness Operations Reference Model 0.1 does not map AI Agent Sessions or Harness Instances directly to OpAMP Agents.

Instead, OpAMP provides useful design precedent:

- heterogeneous fleet management benefits from capability negotiation rather than assuming uniform support;
- effective configuration can differ from desired remote configuration;
- local restrictions should remain enforceable against remote control;
- partial implementations need explicit interoperability behavior;
- instance identity and health are fundamental operational concerns.

If future AI Harnesses adopt OpAMP or an OpAMP extension for management, that should be evaluated as a concrete interoperability proposal rather than assumed by the reference model.

## Native Harness APIs and protocols

Open standards are not the only valid operational surfaces.

Many Harnesses expose native CLIs, APIs, event streams, local databases, plugins, permission mechanisms, or SDKs that contain richer semantics than a common protocol. Harness Operations explicitly treats native interfaces as first-class inputs.

An implementation should prefer a faithful native capability over a lossy common abstraction when no applicable standard exists. Interoperability should not require semantic erasure.

## Boundary summary

| Boundary or concern | Existing standard / discipline / surface | Harness Operations relationship |
| --- | --- | --- |
| Broad production operation of AI agents | AgentOps / agent operations | Complementary and overlapping. Harness Operations narrows the lens to heterogeneous Harnesses and their native operational semantics. |
| AI application ↔ tools/context/services | MCP | Compose MCP primitives and extensions; do not redefine tool/resource/task wire semantics. |
| Editor/client ↔ coding agent | ACP | Preserve ACP Session, permission, and update semantics; map to broader operational concepts only where needed. |
| Independent agent system ↔ agent system | A2A | Preserve AgentCard, Task, Message, Artifact, and protocol lifecycle semantics. |
| Telemetry representation | OpenTelemetry | Prefer OTel signals and GenAI semantic conventions where applicable; do not create a competing generic telemetry protocol. |
| Telemetry/data-collection agent fleet management | OpAMP | Adjacent operational prior art; not an AI agent protocol. Reuse lessons, not names by assumption. |
| Harness-specific lifecycle/capabilities | Native Harness interfaces | Preserve native semantics and adapt rather than flatten. |
| Cross-harness descriptive lifecycle, governance, routing, limits, human intervention, and evidence model | No single normative model identified in v0.1 | Described by the Harness Operations reference model; protocol work remains deferred unless a concrete interoperability gap is demonstrated. |

## Areas of overlap that require care

### Tasks and Runs

MCP Tasks and A2A Tasks both overlap with Harness Operations Run.

The rule is simple: **do not create an extra Run merely because the reference model contains the word.**

Use the native Task as the operational identity when its scope is sufficient. Introduce a broader Run only when one execution genuinely spans several native tasks, sessions, Harnesses, approvals, or environments.

### Sessions

ACP and individual Harnesses may define concrete session semantics. Harness Operations Agent Session is an operational umbrella concept, not a replacement lifecycle.

### Artifacts

A2A defines Artifact normatively. Harness Operations uses Artifact descriptively. When A2A is used, the A2A Artifact is authoritative and Harness Operations adds only operational relationships or evidence around it.

### Capabilities

MCP discovery, A2A AgentCards, ACP initialization, native Harness APIs, and OpAMP expose different notions of capabilities.

Harness Operations Capability should not force them into one schema. A common capability model should emerge only where implementations demonstrate faithful equivalence.

### Permissions and Approvals

ACP, Harness-native permission systems, MCP authorization, environment policy, and Harness Operations Approval can interact but are not interchangeable.

A low-level permission request becomes an Approval only when it carries governance meaning: attributable Authority, a defined decision scope, and operational effect.

## Criteria for a future Harness Operations interoperability proposal

Reference Model 0.1 does not define a wire protocol.

A future proposal for new interoperability semantics should demonstrate all of the following:

1. **Multiple independent Harnesses or operating systems need the same boundary.**
2. **Existing standards and native interfaces cannot express the requirement faithfully enough.**
3. **The proposed semantics are implementation-neutral.**
4. **At least two independent implementations or prototypes can validate the model.**
5. **The proposal maps cleanly to existing MCP, ACP, A2A, OpenTelemetry, identity, and infrastructure standards instead of competing unnecessarily.**
6. **The operational benefit exceeds the cost of introducing another interoperability surface.**

Until those conditions exist, adapters and reference-model mappings are preferable to a new protocol.

## Standards and disciplines change over time

This landscape is time-sensitive.

MCP, ACP, A2A, OpenTelemetry GenAI conventions, AgentOps practice, and adjacent standards continue to evolve. The reference model should record the version or maturity assumed when making a mapping and revisit boundaries when those projects change materially.

Harness Operations should become smaller when another open standard or established discipline successfully absorbs a problem, not defend territory for its own sake.

That is a feature of the project, not a failure.
