# Contributing to Harness Operations

Harness Operations is being developed as a vendor-neutral, implementation-neutral reference model. Contributions should improve the shared operational model rather than encode the requirements of one product or architecture.

## Where changes start

Use a GitHub Issue when a proposed change:

- introduces or changes a core concept;
- affects more than one reference document;
- changes the scope or boundaries of the project;
- changes the relationship to an external standard;
- introduces a substantial new proposal.

Small editorial fixes that do not change semantics may go directly to a focused Pull Request.

## Pull Requests

Canonical reference content changes through Pull Requests.

A Pull Request should:

1. link the Issue or design discussion it implements when one exists;
2. explain the semantic change, not only the file change;
3. identify external standards or prior art affected by the change;
4. keep the change focused enough to review meaningfully;
5. resolve material review objections before merge.

## Reference-model guardrails

A concept belongs in the reference model only when it is justified by a cross-harness operational need. Concepts that exist only because one product, vendor, deployment, or architecture needs them should remain implementation details or examples until broader evidence supports inclusion.

Where an existing open standard already defines applicable semantics, Harness Operations should describe the relationship to that standard rather than create parallel semantics without a demonstrated gap.

Claims about external standards, established terminology, or industry practice should use current authoritative sources where practical.

## AI-assisted contributions

Material use of AI assistance should be disclosed in the Pull Request description. The contributor remains responsible for the accuracy, originality, licensing, and reviewability of the contribution regardless of the tools used to produce it.

## Proposals

The `proposals/` directory is reserved for changes that are too substantial to review effectively as an ordinary Issue and Pull Request.

The Harness Operations Reference Model does not define a formal RFC process, voting system, working groups, or standards-body procedure. Those mechanisms should be introduced only if real contributor scale and decision pressure justify them.

## Normative language

The Harness Operations Reference Model is descriptive. Do not use RFC 2119 or RFC 8174 `MUST`, `SHOULD`, or similar keywords as conformance requirements.

## Licensing

Unless explicitly stated otherwise, contributions to the specification repository are made under the Apache License, Version 2.0. By contributing, you affirm that you have the right to submit the contribution under that license.

## Project governance and system governance

This file describes how contributions to the project are reviewed.

Governance of Harness Operations systems—authority, ownership, policy, delegation, approval, exceptions, budgets, change control, and accountability—is a separate subject defined by the reference model.
