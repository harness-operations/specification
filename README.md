# Harness Operations

This repository is the canonical home of the emerging **Harness Operations Reference Model**.

**Status:** Reference Model 0.1 content-complete draft; publication pending.

> **Harness engineering makes an agent effective. Harness Operations makes agent systems operable.**

Harness Operations is a vendor-neutral, implementation-neutral, **harness-centric** reference model for operating one or more agent harnesses as a coherent system across their lifecycles, environments, work, and authorities.

It is complementary to the broader AgentOps / agent-operations space. Its narrower focus is the operational meaning carried by heterogeneous Harnesses: session lifecycle, context, capabilities, permissions, execution, governance, intervention, and evidence without forcing unlike Harnesses into false equivalence.

The project intentionally starts with a reference model rather than a new wire protocol. Existing standards, established operational disciplines, and native Harness capabilities should be composed where they already solve the problem.

## Reference Model 0.1

Canonical reference material lives under [`reference/`](reference/):

1. [What is Harness Operations?](reference/overview.md)
2. [Principles](reference/principles.md)
3. [Reference Model](reference/model.md)
4. [Governance](reference/governance.md)
5. [Standards Landscape](reference/landscape.md)

Shared scope and vocabulary are maintained in [Scope and Terminology](reference/terminology.md).

## Scope

Reference Model 0.1 is descriptive. It does **not** define:

- a Harness Operations wire protocol;
- a common Harness or Agent Session lifecycle;
- a registry or SDK;
- a conformance or certification program;
- a centralized control-plane requirement;
- a replacement for MCP, ACP, A2A, OpenTelemetry, AgentOps, DevOps/SRE, or native Harness interfaces.

The reference model should become smaller when an existing standard or established discipline already expresses a concern faithfully.

## Development process

Substantive design work begins in GitHub Issues and canonical reference material changes through Pull Requests.

- [Reference Model v0.1 roadmap](https://github.com/harness-operations/specification/issues/9)
- [Contribution guide](CONTRIBUTING.md)
- [Proposals](proposals/)

The five foundational documents and the adversarial/prior-art review have been completed as working drafts. Remaining v0.1 publication gates are tracked in the roadmap.

## License

Specification and reference content in this repository is licensed under the [Apache License 2.0](LICENSE).
