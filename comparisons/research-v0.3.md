# Broader landscape research scope

**Reviewed:** September 25, 2026

This v0.3 research pass adds role-separated comparison rows beyond the two detailed Harness mappings.

## Rows

- **Cursor CLI** — rolling first-party hosted documentation, observed September 25, 2026. No immutable binary build is asserted.
- **OpenCode** — v1.18.32 CLI/headless server.
- **Agent Executor (AX)** — v0.3.0, `ax.io/v1alpha1`, execution-runtime role.
- **TypeSafe Jev** — System One API 0.2.0, decision-service role.
- **Paseo** — v0.9.2 client/control-layer role.

These rows are documentation/source-backed research observations, not full implementation mappings and not independent live compatibility tests.

## Role separation

The rendered matrix must not treat unlike rows as substitutable competitors:

- Harness rows answer how an agent Harness exposes lifecycle, permissions, delegation, and evidence.
- AX answers execution-runtime/isolation/resource questions.
- Jev answers decision-service questions; enforcement capabilities are intentionally marked not applicable where the service only produces judgments.
- Paseo answers client/control-layer questions and preserves provider-native semantics.

## Directed compatibility

Paseo v0.9.2 source contains concrete adapters for Codex, Claude Code, OpenCode, and Cursor ACP. Those records are marked **partial**, not demonstrated, because Harness Operations has not independently run those product pairs during v0.3.

A shared protocol or an implemented adapter does not establish every lifecycle/governance behavior.
