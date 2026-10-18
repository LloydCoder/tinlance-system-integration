"""Validate the versioned TWI source-evidence schema and negative cases."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "twi-source-evidence.schema.json"


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    valid = {
        "schema_version": "1.0.0",
        "source_system": "tinlance-web-intelligence",
        "tenant_ref": "a" * 64,
        "source_job_id": "job-123",
        "claim_id": "claim-001",
        "statement": "The source reports a verifiable statement.",
        "source_url": "https://example.com/article",
        "source_url_redacted": False,
        "retrieved_at": "2026-10-18T12:00:00Z",
        "media_type": "text/html",
        "artifact_sha256": "b" * 64,
        "quote": "A verifiable quote from the source.",
        "quote_sha256": "c" * 64,
        "verifier_version": "twi-citation-verifier/1.0.0",
        "report_sha256": "d" * 64,
    }
    errors = list(validator.iter_errors(valid))
    if errors:
        raise SystemExit(f"valid source-evidence example rejected: {errors[0].message}")

    invalid_samples = []
    missing_digest = copy.deepcopy(valid)
    del missing_digest["artifact_sha256"]
    invalid_samples.append(missing_digest)
    invalid_tenant = copy.deepcopy(valid)
    invalid_tenant["tenant_ref"] = "not-a-digest"
    invalid_samples.append(invalid_tenant)
    wrong_authority = copy.deepcopy(valid)
    wrong_authority["source_system"] = "agent-platform"
    invalid_samples.append(wrong_authority)
    unknown_property = copy.deepcopy(valid)
    unknown_property["canonical_world_state"] = True
    invalid_samples.append(unknown_property)

    for sample in invalid_samples:
        try:
            validator.validate(sample)
        except ValidationError:
            continue
        raise SystemExit("invalid source-evidence sample unexpectedly passed validation")

    print("TWI source-evidence JSON Schema and negative cases verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
