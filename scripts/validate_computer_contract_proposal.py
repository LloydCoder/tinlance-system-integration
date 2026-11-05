#!/usr/bin/env python3
"""Validate the non-canonical Phase 1 persistent-computer contract proposal."""
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "contracts/proposals/computer/v1/computer-lifecycle.schema.json"


def valid_examples() -> list[dict[str, object]]:
    common_time = "2026-11-05T12:00:00Z"
    return [
        {
            "schema_version": "computer-profile.v1",
            "profile_id": "profile-browser",
            "isolation_tier": "microvm",
            "image_digest": "sha256:" + "a" * 64,
            "resources": {
                "vcpus": 2,
                "memory_mib": 2048,
                "disk_gib": 20,
                "max_processes": 128,
                "wall_clock_seconds": 3600,
            },
            "network_profile": "egress-allowlist",
            "persistence_class": "workspace-durable",
            "data_residency": "eu-west",
            "retention_class": "standard-30d",
            "browser": True,
            "risk_class": "high",
            "data_classification": "confidential",
            "requested_capabilities": ["browser.navigate", "filesystem.workspace"],
        },
        {
            "schema_version": "computer-operation.v1",
            "operation_id": "operation-restore-1",
            "operation": "restore",
            "tenant_id": "tenant-a",
            "workspace_id": "workspace-a",
            "request_id": "request-restore-1",
            "idempotency_key": "restore-idempotency-key-001",
            "expected_generation": 3,
            "requested_by": "subject-a",
            "created_at": common_time,
            "profile_id": "profile-browser",
            "reason": "resume user workspace",
        },
        {
            "schema_version": "execution-grant.v1",
            "grant_id": "grant-1",
            "issuer": "agent-platform",
            "audience": "tinlance-compute-adapter",
            "tenant_id": "tenant-a",
            "subject_id": "subject-a",
            "agent_id": "agent-a",
            "workspace_id": "workspace-a",
            "run_id": "run-a",
            "capability": "browser.navigate",
            "policy_revision": "policy-2026-11",
            "resource_envelope": {
                "cpu_seconds": 120,
                "memory_bytes": 536870912,
                "max_processes": 32,
                "max_output_bytes": 1048576,
            },
            "issued_at": common_time,
            "expires_at": "2026-11-05T12:05:00Z",
            "nonce": "0123456789abcdef",
            "idempotency_key": "grant-idempotency-key-001",
            "fencing_token": 7,
            "signature": {
                "alg": "EdDSA",
                "kid": "platform-grant-key-2026-01",
                "value": "A" * 64,
            },
        },
        {
            "schema_version": "computer-lease.v1",
            "lease_id": "lease-a",
            "tenant_id": "tenant-a",
            "workspace_id": "workspace-a",
            "instance_id": "instance-a",
            "owner": "subject-a",
            "generation": 3,
            "fencing_token": 7,
            "issued_at": common_time,
            "expires_at": "2026-11-05T13:00:00Z",
            "renewal_policy": "manual",
            "max_concurrency": 1,
        },
        {
            "schema_version": "computer-instance.v1",
            "instance_id": "instance-a",
            "provider": "firecracker-adapter",
            "provider_reference": "opaque-provider-ref",
            "tenant_id": "tenant-a",
            "workspace_id": "workspace-a",
            "state": "ready",
            "generation": 3,
            "image_digest": "sha256:" + "b" * 64,
            "profile_id": "profile-browser",
            "attestation_reference": "evidence://attestation/instance-a",
            "created_at": common_time,
            "updated_at": common_time,
        },
        {
            "schema_version": "computer-evidence.v1",
            "evidence_id": "evidence-1",
            "tenant_id": "tenant-a",
            "workspace_id": "workspace-a",
            "instance_id": "instance-a",
            "run_id": "run-a",
            "trace_id": "trace-a",
            "kind": "attestation",
            "digest": "sha256:" + "c" * 64,
            "created_at": common_time,
            "source": "external-evidence-service",
            "storage_reference": "evidence://computer/attestation/1",
        },
    ]


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    examples = valid_examples()
    for index, example in enumerate(examples, start=1):
        errors = list(validator.iter_errors(example))
        if errors:
            details = "; ".join(error.message for error in errors)
            raise SystemExit(f"FAIL valid proposal example {index}: {details}")

    invalid_cases = [
        ({**examples[2], "issuer": "agent-os"}, "non-Platform grant issuer"),
        ({**examples[2], "fencing_token": 0}, "non-positive fencing token"),
        ({**examples[0], "unexpected_authority": True}, "unknown authority field"),
        ({**examples[4], "image_digest": "sha256:not-a-digest"}, "invalid image digest"),
    ]
    for instance, label in invalid_cases:
        if not list(validator.iter_errors(instance)):
            raise SystemExit(f"FAIL invalid proposal case was accepted: {label}")

    print(
        "PASS persistent computer proposal schema: "
        f"schema=Draft2020-12 examples={len(examples)} negative_cases={len(invalid_cases)} "
        "status=proposal-not-canonical"
    )


if __name__ == "__main__":
    main()
