# Standards Landscape and Interoperability Boundaries

**Status:** Draft for Harness Operations Reference Model 0.1

## Purpose

Harness Operations does not begin from an empty standards or operational landscape.

Existing protocols already define important boundaries around AI applications, coding agents, independent agent systems, tools, context, tasks, artifacts, permissions, and telemetry. Existing operational disciplines already cover many production concerns. Harness Operations should compose those standards and practices rather than rename or replace them.

This document asks a narrower question:

> **Which existing standards and adjacent disciplines already define relevant boundaries, and what harness-specific operational problem remains?**

The landscape is intentionally selective. It is not a catalog of agent frameworks, products, or every protocol related to AI systems.

## Guiding rule: compose before inventing

Harness Operations should prefer this order:

1. use a native Harness capability when it already expresses the required semantics;
2. use or map an established open standard where it defines the relevant boundary;
3. reuse established operations, security, and governance practice rather than renaming it;
4. adapt between different native or standardized semantics without erasing meaningful differences;
5. propose new interoperability semantics only when a demonstrated cross-harness gap remains.

Reference Model 0.1 therefore does not define a Harness Operations wire protocol.

## Boundary map

```text
                         Operators
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

`AgentOps` and `agent operations` are emerging umbrella terms for production practices around AI agents. Current usage is materially non-uniform:

- some usage centers observability, testing, debugging, evaluation, and cost tracking;
- some expands into deployment, lifecycle management, governance, security, and fleet operations;
- vendors and research use the term with different boundaries.

Examples include AWS's broad AgentOps operational framing, the AgentOps product/project's observability and evaluation tooling, and research using AgentOps as an observability taxonomy.

Background:

- [AWS: AgentOps — operationalize agentic AI at scale](https://aws.amazon.com/blogs/machine-learning/agentops-operationalize-agentic-ai-at-scale-with-amazon-bedrock-agentcore/)
- [AgentOps documentation](https://docs.agentops.ai/v2/introduction)
- [AgentOps: Enabling Observability of LLM Agents](https://arxiv.org/abs/2411.05285)

### Relationship to Harness Operations

The v0.1 prior-art review did **not** identify a broadly adopted common AgentOps specification or reference model. Harness Operations therefore does not treat AgentOps as a parent specification, standardized taxonomy, or authoritative model that Harness Operations must fit inside.

Harness Operations is **adjacent to and overlapping with** broader AgentOps / agent-operations practice while addressing a more specific systems problem.

The Harness is the primary operational unit because it concretely mediates session lifecycle, context, tools, permissions, execution, persistence, and other runtime semantics. This matters when operators work across Harnesses that expose materially different session models, permission mechanisms, capabilities, execution environments, or persistence behavior.

Harness Operations is not an attempt to own the phrase “agent operations.” Its purpose is to provide a coherent model for operating heterogeneous Harnesses and their executions without erasing those native differences.

## Model Context Protocol (MCP)

### Current scope

The Model Context Protocol is an open standard connecting AI applications to external systems that expose tools, resources, prompts, and related capabilities.

The current MCP specification revision, **2026-07-28**, uses a stateless request/response core with a formal extension mechanism. Long-running work is available through the **Tasks extension**.

Authoritative background:

- [MCP 2026-07-28 specification release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [MCP specification](https://modelcontextprotocol.io/specification/2026-07-28)

### Relationship to Harness Operations

MCP can provide tool and service Capabilities, external context and resources, authorization boundaries, long-running Tasks, and capability/extension discovery.

Harness Operations should use those semantics where MCP is the actual integration boundary. An MCP Task may serve as a Run when its lifecycle already supplies the operational identity required.

Harness Operations should not create parallel wire semantics for MCP tools, resources, prompts, authorization, Tasks, or capability discovery.

MCP does not by itself define the complete operational model for heterogeneous Harness Instances across unrelated Harnesses: cross-harness lifecycle, placement, Authority and Delegation, human intervention, Limits, and historical execution evidence remain separate concerns.

MCP is evolving quickly. These boundaries are time-sensitive and should shrink if MCP absorbs them successfully.

## Agent Client Protocol (ACP)

### Current scope

The Agent Client Protocol standardizes communication between code editors or interactive clients and coding agents. ACP includes session lifecycle, prompts and updates, tool-call presentation, permission requests, configuration, and related coding-agent interactions.

As of Reference Model 0.1 development, **ACP v1 is stable** while protocol v2 remains explicitly unstable/draft.

Authoritative background:

- [ACP repository](https://github.com/agentclientprotocol/agent-client-protocol)
- [ACP changelog](https://github.com/agentclientprotocol/agent-client-protocol/blob/main/CHANGELOG.md)

### Relationship to Harness Operations

Where a Harness is exposed through ACP:

- ACP Session semantics can map to Harness Operations Agent Session;
- ACP permission interactions can provide execution-control or Approval inputs depending on governance meaning;
- ACP updates can contribute Events and state;
- the client can act as an operational interface without becoming a universal Control Plane.

Harness Operations should preserve ACP Session semantics rather than force a common lifecycle. A broader Run is useful only when the operational objective extends beyond an individual ACP Session.

## Agent2Agent Protocol (A2A)

### Current scope

A2A is an open standard for communication and interoperability between independent, potentially opaque agent systems.

A2A **1.0** defines normative concepts including `AgentCard`, `Message`, `Task`, `Artifact`, streaming, push notifications, and extensions.

Authoritative background:

- [A2A Protocol Specification](https://github.com/a2aproject/A2A/blob/main/docs/specification.md)
- [A2A changelog](https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md)

### Relationship to Harness Operations

A2A is relevant when one Harness or agent system delegates to or collaborates with another independent system.

Possible mappings include:

- AgentCard capabilities and skills informing Capability or routing decisions;
- an A2A Task serving as a Run when the lifecycle scopes are equivalent;
- several A2A Tasks participating in a broader Run when one operational objective spans multiple Tasks, Harnesses, or Approvals;
- an A2A Artifact mapping directly to a Harness Operations Artifact when A2A is the producing boundary.

A2A's normative Task, Message, and Artifact semantics remain authoritative when A2A is used. Harness Operations should add operational relationships or provenance rather than redefine them.

## OpenTelemetry

### Current scope

OpenTelemetry provides vendor-neutral APIs, SDKs, protocols, and semantic conventions for traces, metrics, logs, events, and related observability data.

The dedicated OpenTelemetry GenAI semantic-conventions project currently marks its conventions as **Development** and covers model calls, agent invocation, workflow invocation, planning, tool execution, memory operations, metrics, and events.

Authoritative background:

- [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)
- [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai)

### Relationship to Harness Operations

OpenTelemetry should be the first place to look when implementations need common telemetry representation.

A Harness Operations Run is not required to equal an OpenTelemetry trace. A Run may outlive telemetry retention, span several traces, include human Approval intervals, or aggregate systems whose trace contexts are not continuous.

Similarly, Harness Operations Event is an abstract operational occurrence, not a competing OpenTelemetry event schema. Implementations should map applicable telemetry to OpenTelemetry rather than invent a second generic telemetry standard.

## Open Agent Management Protocol (OpAMP)

OpenTelemetry also defines the **Open Agent Management Protocol (OpAMP)**, currently Beta.

Despite the name, OpAMP's “Agents” are data-collection/telemetry agents such as collectors and log forwarders, not AI agent Harnesses. It is not an AI-agent interoperability standard.

It is nevertheless valuable fleet-management prior art. OpAMP includes stable instance identity, capability negotiation, health reporting, heartbeats, effective versus remote configuration, partial interoperability, local restrictions on remote configuration, and package/update state.

Authoritative background:

- [Open Agent Management Protocol](https://opentelemetry.io/docs/specs/opamp/)

Harness Operations does not map AI Agent Sessions or Harness Instances directly to OpAMP Agents. The value is in the operational lessons: capability negotiation, effective-versus-desired configuration, local restrictions, instance identity, health, and explicit partial support.

## Native Harness APIs and protocols

Open standards are not the only valid operational surfaces.

Harnesses may expose native CLIs, APIs, event streams, local stores, plugins, permission mechanisms, or SDKs that carry richer semantics than any common protocol. Harness Operations treats those native interfaces as first-class inputs.

A faithful native capability is preferable to a lossy common abstraction when no applicable standard exists. Interoperability should not require semantic erasure.

## Boundary summary

| Boundary or concern | Existing standard / discipline / surface | Harness Operations relationship |
| --- | --- | --- |
| Broad production operation of AI agents | AgentOps / agent operations | Adjacent and overlapping emerging practice; no broadly adopted common specification identified in v0.1. |
| AI application ↔ tools/context/services | MCP | Compose MCP primitives and extensions; do not redefine tool/resource/task semantics. |
| Editor/client ↔ coding agent | ACP | Preserve ACP Session, permission, and update semantics. |
| Independent agent system ↔ agent system | A2A | Preserve AgentCard, Task, Message, Artifact, and protocol lifecycle semantics. |
| Telemetry representation | OpenTelemetry | Prefer OTel signals and GenAI conventions; do not create a competing generic telemetry protocol. |
| Telemetry/data-collection agent fleet management | OpAMP | Adjacent operational prior art; reuse lessons, not names by assumption. |
| Harness-specific lifecycle/capabilities | Native Harness interfaces | Preserve native semantics and adapt rather than flatten. |
| Cross-harness lifecycle, governance, routing, limits, human intervention, and evidence | No broadly adopted common model identified in v0.1 | Described by Harness Operations; protocol work remains deferred unless a concrete interoperability gap is demonstrated. |

## Areas of overlap that require care

### Tasks and Runs

MCP Tasks and A2A Tasks overlap with Harness Operations Run.

**Do not create an extra Run merely because the reference model contains the word.** Use the native Task when its scope is sufficient. Introduce a broader Run only when execution genuinely spans multiple native tasks, sessions, Harnesses, Approvals, or environments.

### Sessions

ACP and individual Harnesses may define concrete session semantics. Harness Operations Agent Session is an operational umbrella concept, not a replacement lifecycle.

### Artifacts

A2A defines Artifact normatively. Harness Operations uses Artifact descriptively. At an A2A boundary, the A2A Artifact remains authoritative.

### Capabilities

MCP discovery, A2A AgentCards, ACP initialization, native Harness APIs, and OpAMP expose different notions of capability. Harness Operations should not force them into one schema unless implementations demonstrate faithful equivalence.

### Permissions and Approvals

ACP, Harness-native permission systems, MCP authorization, environment policy, and Harness Operations Approval can interact but are not interchangeable.

A low-level permission request becomes an Approval only when it carries governance meaning: attributable Authority, a defined decision scope, and operational effect.

## Criteria for future interoperability work

A future Harness Operations interoperability proposal should demonstrate all of the following:

1. multiple independent Harnesses or operating systems need the same boundary;
2. existing standards and native interfaces cannot express the requirement faithfully enough;
3. the proposed semantics are implementation-neutral;
4. at least two independent implementations or prototypes can validate the model;
5. the proposal maps cleanly to MCP, ACP, A2A, OpenTelemetry, identity, and infrastructure standards;
6. the operational benefit exceeds the cost of introducing another interoperability surface.

Until those conditions exist, adapters and reference-model mappings are preferable to a new protocol.

## Standards and disciplines change over time

This landscape is time-sensitive.

MCP, ACP, A2A, OpenTelemetry GenAI conventions, AgentOps practice, and adjacent standards will continue to evolve. Harness Operations should become smaller when another standard or established discipline successfully absorbs a concern rather than defending conceptual territory for its own sake.

That is a feature of the project, not a failure.
