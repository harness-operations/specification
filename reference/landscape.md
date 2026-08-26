# Standards Landscape and Interoperability Boundaries

**Status:** Draft for Harness Operations Reference Model 0.1

## Purpose

Harness Operations does not begin from an empty standards landscape.

Existing protocols and observability standards already define important boundaries around AI applications, coding agents, independent agent systems, tools, context, tasks, artifacts, permissions, and telemetry. The goal of Harness Operations is not to rename or replace those semantics.

This document answers a narrower question:

> **Which existing standards already define relevant interoperability boundaries, and what operational concerns remain outside those boundaries?**

The landscape is intentionally selective. It is not a catalog of agent frameworks, products, or every protocol related to AI systems.

## Guiding rule: compose before inventing

Harness Operations should prefer this order:

1. use a native Harness capability when it already expresses the required semantics;
2. use or map an established open standard where it defines the relevant boundary;
3. adapt between different native or standardized semantics without erasing meaningful differences;
4. propose new interoperability semantics only when a demonstrated cross-harness gap remains.

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

## Model Context Protocol (MCP)

### Current scope

The Model Context Protocol is an open standard connecting AI applications to external systems that expose tools, resources, prompts, and related capabilities.

The current MCP specification revision, **2026-07-28**, moved the protocol core to a stateless request/response model and formalized an extension mechanism. Long-running work is available through the **Tasks extension**, while other extensions cover concerns such as applications and enterprise-managed authorization.

Current authoritative background:

- [MCP 2026-07-28 specification release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [MCP TypeScript SDK v2 documentation](https://ts.sdk.modelcontextprotocol.io/v2/)

### Relationship to Harness Operations

MCP can provide important operational building blocks, particularly:

- tool and service Capabilities;
- external context and resources;
- authorization and access boundaries associated with MCP servers;
- long-running protocol interactions through Tasks;
- discoverable server capabilities and extensions.

Harness Operations should use those semantics where MCP is the actual integration boundary.

For example, an MCP tool can map to a Capability available to an Agent Session. An MCP Task may map to a portion of a Run—or in a simple architecture, to the Run itself—when their lifecycles are genuinely equivalent.

### What Harness Operations should not redefine

Harness Operations should not create parallel wire semantics for:

- MCP tool invocation;
- MCP resource or prompt access;
- MCP authorization;
- MCP Tasks when an implementation is using that extension;
- MCP capability discovery.

### What remains outside MCP's core purpose

MCP does not, by itself, define the complete operational model for a heterogeneous fleet of Harness Instances and Agent Sessions across unrelated Harnesses. Harness Operations additionally reasons about concerns such as:

- operational identity across multiple Harnesses or sessions;
- routing and placement across Harness Instances and Execution Environments;
- cross-harness lifecycle and attention state;
- governance Authority, Ownership, Delegation, Approval, and Exceptions;
- cross-system Limits and Usage;
- historical execution truth and audit evidence;
- human intervention across heterogeneous native permission models.

MCP is evolving quickly, including work on agent communication and enterprise concerns. This boundary should therefore be reviewed against each future MCP specification release rather than treated as permanent.

## Agent Client Protocol (ACP)

### Current scope

The Agent Client Protocol standardizes communication between code editors or interactive clients and coding agents.

ACP defines a client/agent interaction boundary that includes session lifecycle, prompts and updates, tool-call presentation, permission requests, configuration, and other coding-agent UX and execution interactions.

As of Reference Model 0.1 development, **ACP v1 is the stable protocol family** while protocol v2 remains an explicitly unstable/draft evolution.

Current authoritative background:

- [ACP repository](https://github.com/agentclientprotocol/agent-client-protocol)
- [ACP changelog](https://github.com/agentclientprotocol/agent-client-protocol/blob/main/CHANGELOG.md)

### Relationship to Harness Operations

Where a coding Harness is exposed through ACP:

- an ACP agent implementation can represent or front a Harness;
- ACP Session semantics can map to Harness Operations Agent Session;
- ACP permission interactions can provide native execution-control or Approval inputs depending on governance meaning;
- ACP updates can contribute operational Events and state;
- the client can act as an operational interface without becoming a universal Control Plane.

### Preserve ACP Session semantics

Harness Operations `Agent Session` is deliberately broader than ACP `Session`.

An implementation using ACP should retain the ACP session identifier and lifecycle as native semantics. It should not translate ACP into a different generic lifecycle merely for consistency with another Harness.

A broader Harness Operations Run may contain or correlate one or more ACP Sessions when the operational objective extends beyond an individual ACP session.

### What remains outside ACP's core purpose

ACP primarily defines interaction between a client and a coding agent. It does not attempt to define a general operational model for:

- multiple unrelated Harness products;
- cross-harness workflows and Runs;
- governance across environments;
- fleet-level placement, Limits, and Usage;
- durable cross-harness audit evidence;
- general-purpose non-coding Harnesses.

Harness Operations should therefore compose ACP for the client/coding-agent boundary rather than replace it.

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

- A2A AgentCard capabilities and skills informing Harness Operations Capability or routing decisions;
- an A2A Task mapping to a Run when the Task and operational lifecycle have the same scope;
- an A2A Task representing one child execution within a broader Run when the larger operational objective spans multiple Tasks or Harnesses;
- an A2A Artifact mapping directly to a Harness Operations Artifact when A2A is the producing boundary;
- A2A Messages remaining native communication objects rather than being redefined by Harness Operations.

### Task and Run are not automatically equivalent

A2A `Task` is a normative protocol object. Harness Operations `Run` is a broader reference-model concept intended for operational identity.

Implementations should not create both objects without need.

If one A2A Task fully represents the lifecycle that operators need to govern and observe, it can serve as the operational Run identity. A separate Run becomes useful only when the operational lifecycle is broader—for example, when it coordinates several A2A Tasks, local Agent Sessions, Approvals, or Harnesses as one execution.

### Artifact semantics

A2A explicitly separates Messages from Artifacts and defines Artifact as task output.

When A2A is used, those semantics should be preserved. Harness Operations should add operational provenance or governance references around an A2A Artifact rather than redefine its protocol representation.

### What remains outside A2A's core purpose

A2A does not require an organization to operate every local Harness through A2A. It also does not by itself define a complete fleet-management, policy-governance, environment-placement, budgeting, or cross-harness audit model.

Harness Operations should therefore treat A2A as a strong agent-to-agent interoperability boundary, not as something to duplicate.

## OpenTelemetry

### Current scope

OpenTelemetry provides vendor-neutral APIs, SDKs, protocols, and semantic conventions for traces, metrics, logs, events, and related observability data.

Generative-AI semantic conventions are actively evolving. The current dedicated OpenTelemetry GenAI semantic-conventions project defines **Development-status** conventions for model calls, agent invocation, workflow invocation, planning, tool execution, memory operations, metrics, and events. Reference implementations exercise those conventions against multiple current agent frameworks and providers.

Current authoritative background:

- [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)
- [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai)
- [GenAI agent and framework spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md)

### Relationship to Harness Operations

OpenTelemetry should be the first place to look when Harness Operations implementations need common telemetry representation.

Potential mappings include:

- Harness Operations Event facts to OTel logs/events/spans where an applicable convention exists;
- Usage measurements to OTel GenAI metrics or other resource metrics;
- Agent Session and Run correlations to traces, spans, attributes, or linked telemetry without requiring that the reference-model identity equal one span;
- native Harness tool/model/workflow telemetry to existing GenAI semantic conventions.

### Run is not a trace

A Harness Operations Run is an operational lifecycle identity. An OpenTelemetry trace is telemetry context used to correlate observability signals.

A Run may correspond neatly to one trace in some implementations, but the reference model does not require that relationship. A Run may outlive telemetry retention, span multiple traces, include human Approval intervals, or aggregate work from systems whose tracing contexts are not continuous.

### Event is not an OpenTelemetry Event schema

Harness Operations uses Event as the abstract fact of an observable operational occurrence. Implementations should map that fact to current OpenTelemetry signal guidance where appropriate rather than invent a second generic telemetry schema.

The OpenTelemetry event model itself is evolving, including a shift toward log-based events. Harness Operations should avoid binding the reference-model Event concept to one OTel API representation.

### Maturity matters

The GenAI semantic conventions are currently marked **Development**. Harness Operations should track and prefer them, but should not describe evolving attributes or span shapes as permanently stable.

## Open Agent Management Protocol (OpAMP)

### Why it appears in this landscape

OpenTelemetry also defines the **Open Agent Management Protocol (OpAMP)**, currently Beta.

Despite the name, OpAMP's “Agents” are **data-collection/telemetry agents** such as collectors and log forwarders, not AI agent Harnesses.

OpAMP is therefore not an AI agent interoperability standard and should not be confused with A2A or Harness Operations.

It is nevertheless valuable prior art because it addresses a structurally similar operational problem: remote management of a heterogeneous fleet of independently implemented agents.

OpAMP includes concepts such as:

- stable instance identity;
- capability negotiation;
- status and health reporting;
- heartbeats;
- effective versus remote configuration;
- partial interoperability;
- remote configuration with local restrictions;
- package management and update state.

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

If future AI Harnesses adopt OpAMP or an OpAMP extension for their own management, that should be evaluated as a concrete interoperability proposal rather than assumed by the reference model.

## Native Harness APIs and protocols

Open standards are not the only valid operational surfaces.

Many Harnesses expose native CLIs, APIs, event streams, local databases, plugins, permission mechanisms, or SDKs that contain richer semantics than any common protocol.

Harness Operations explicitly treats native interfaces as first-class inputs.

An implementation should prefer a faithful native capability over a lossy common abstraction when no applicable standard exists. Interoperability should not require semantic erasure.

## Boundary summary

| Boundary or concern | Existing standard / surface | Harness Operations relationship |
| --- | --- | --- |
| AI application ↔ tools/context/services | MCP | Compose MCP primitives and extensions; do not redefine tool/resource/task wire semantics. |
| Editor/client ↔ coding agent | ACP | Preserve ACP Session, permission, and update semantics; map to broader operational concepts only where needed. |
| Independent agent system ↔ agent system | A2A | Preserve AgentCard, Task, Message, Artifact, and protocol lifecycle semantics. |
| Telemetry representation | OpenTelemetry | Prefer OTel signals and GenAI semantic conventions where applicable; do not create a competing generic telemetry protocol. |
| Telemetry/data-collection agent fleet management | OpAMP | Adjacent operational prior art; not an AI agent protocol. Reuse lessons, not names by assumption. |
| Harness-specific lifecycle/capabilities | Native Harness interfaces | Preserve native semantics and adapt rather than flatten. |
| Cross-harness lifecycle, governance, routing, limits, human intervention, and audit model | No single standard identified in v0.1 | Described by the Harness Operations reference model; protocol work is deferred unless an interoperability gap is demonstrated. |

## Areas of overlap that require care

### Tasks and Runs

MCP Tasks and A2A Tasks both create overlap with Harness Operations Run.

The rule is simple: **do not create an extra Run merely because the reference model contains the word.**

Use the native Task as the operational identity when its scope is sufficient. Introduce a broader Run only when one execution genuinely spans several native tasks, sessions, Harnesses, approvals, or environments.

### Sessions

ACP and individual Harnesses may define concrete session semantics. Harness Operations Agent Session is an operational umbrella concept, not a replacement lifecycle.

### Artifacts

A2A defines Artifact normatively. Harness Operations uses Artifact descriptively. When A2A is used, the A2A Artifact is authoritative and Harness Operations adds only operational relationships or evidence around it.

### Capabilities

MCP discovery, A2A AgentCards, ACP initialization, native Harness APIs, and OpAMP all expose different notions of capabilities.

Harness Operations Capability should not force them into one schema. A common capability model should emerge only where implementations demonstrate faithful equivalence.

### Permissions and Approvals

ACP, Harness-native permission systems, MCP authorization, environment policy, and Harness Operations Approval can interact but are not interchangeable.

A low-level permission request becomes an Approval only when it carries governance meaning: attributable Authority, a defined decision scope, and operational effect.

## Criteria for a future Harness Operations interoperability proposal

Reference Model 0.1 does not define a wire protocol.

A future proposal for new Harness Operations interoperability semantics should demonstrate all of the following:

1. **Multiple independent Harnesses or operating systems need the same boundary.**
2. **Existing standards and native interfaces cannot express the requirement faithfully enough.**
3. **The proposed semantics are implementation-neutral.**
4. **At least two independent implementations or prototypes can validate the model.**
5. **The proposal maps cleanly to existing MCP, ACP, A2A, OpenTelemetry, identity, and infrastructure standards instead of competing with them unnecessarily.**
6. **The operational benefit exceeds the cost of introducing another interoperability surface.**

Until those conditions exist, adapters and reference-model mappings are preferable to a new protocol.

## Standards change over time

This landscape is time-sensitive.

MCP, ACP, A2A, OpenTelemetry GenAI conventions, and adjacent standards continue to evolve. The reference model should record the version or maturity assumed when making a mapping and revisit the boundary when those projects change materially.

Harness Operations should become smaller when another open standard successfully absorbs a problem, not defend territory for its own sake.

That is a feature of the project, not a failure.
