# TSIC Architecture Overview

TSIC provides the integration control plane for a distributed Tinlance ecosystem.

It owns:
- system registry;
- integration contracts;
- compatibility policy;
- conformance requirements;
- verification tooling;
- certification evidence.

It does not own domain runtime execution.

## Layer model

Registry → Contracts → Integration → Compatibility → Conformance → Verification → Certification.

## Principle

Distributed implementation + explicit authority + canonical contracts + executable verification.

## Persistent compute placement

The Persistent Agent Computer is a runtime substrate integrated beneath Agent Platform. It owns workspace and compute lifecycle mechanics, but it does not own tenant authorization, policy, approvals, capability grants, budgets, secret release or authoritative audit. Agent Platform remains the sole execution authority; Agent OS orchestrates lifecycle; TSIC governs the integration and certification contracts.

The current W2 work is non-production feasibility evidence; rootfs independent-build reproducibility remains open pending the `ldconfig` auxiliary-cache exclusion and independent rebuild gate. See [ADR-0004](decision-records/ADR-0004-persistent-agent-computer.md), the [Persistent Agent Computer threat model](persistent-agent-computer-threat-model.md) and the [Phase 2 benchmark plan](persistent-agent-computer-benchmark-plan.md).
