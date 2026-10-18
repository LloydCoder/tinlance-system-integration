import json
from pathlib import Path


def test_canonical_ecosystem_p10_recovery_contract_preserves_authority_and_production_boundary() -> None:
    path = Path(__file__).resolve().parents[1] / "contracts/recovery/ecosystem-p10-recovery.json"
    contract = json.loads(path.read_text(encoding="utf-8"))

    assert contract["contract"] == "ecosystem-p10-recovery-certification/v1"
    assert contract["canonical_ecosystem_phase"] == "P10"
    assert contract["authority_plane"] == "LloydCoder/tinlance-agent-platform"
    assert "worker_crash" in contract["failure_modes"]
    assert "duplicate_delivery" in contract["failure_modes"]
    assert "recovery-objectives-rto-rpo" in contract["required_evidence"]
    assert any("sole consequential" in item for item in contract["invariants"])
    assert "repository conformance does not imply deployed production readiness" in contract["invariants"]
    assert "observed-failover-rto-rpo" in contract["production_evidence_required"]
    assert "incident-response-owner-signoff" in contract["production_evidence_required"]
    assert "TSIC-00 through TSIC-19" in contract["phase_namespace_note"]
