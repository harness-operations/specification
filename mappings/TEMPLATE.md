# Implementation Mapping Template

Use this template for a versioned Harness, client, control-layer, runtime, or decision-service mapping.

## Scope

- **System:**
- **Role:**
- **Interface/surface:**
- **Version / release / commit / hosted observation date:**
- **Deployment mode:**
- **Platform/environment:**
- **Plan/edition/features:**
- **Reviewed at:**

Do not combine materially different CLI, IDE, SDK/server, hosted, or plugin surfaces into one mapping.

## Primary sources

List authoritative documentation, source, release notes, and protocol specifications used.

## Native operational concepts

| Native concept | Native meaning | Harness Operations relationship | Notes |
| --- | --- | --- | --- |

## Capability observations

For each applicable capability ID from comparisons/data/landscape.json, record finding, delivery mechanism, prerequisites, documented evidence, tested evidence, limitations, and unknowns.

## Lifecycle and failure behavior

Describe documented and observed behavior for start/create, persistence/resume, cancellation/interruption, timeout, disconnect, restart/recovery, and revocation or policy change where applicable.

Do not infer one behavior from another.

## Governance and enforcement

Identify permission/approval surfaces, attributable decision points, advisory/model-mediated behavior, the mechanism that technically enforces a boundary, and where the effective boundary is unknown.

## Evidence and auditability

Identify what can be retained or reconstructed: stable identities, artifacts, events/logs, resolved configuration, approvals/decisions, usage, and redaction/privacy behavior.

## Live tests

For every live test, record exact version/configuration, commands or steps, expected result, observed result, and redacted evidence.

Fixture tests belong in example/test documentation and must not be presented as live integration support.

## Open questions and limitations

List unknowns explicitly. Missing documentation should remain unknown unless affirmative evidence establishes unsupported behavior.
