#!/usr/bin/env python3
"""Fail-closed certification of the reviewed Tinlance Acquisition System baseline."""

from __future__ import annotations

import json
from urllib.request import Request, urlopen

ROOT = "https://raw.githubusercontent.com"
TSIC_REVISION = "4c5b7d70c937ca8227ba8a9ebfe0d69b3e5c2bf8"
BASELINE_PATH = "policies/acquisition-system-baseline.json"

ADAPTER_REVISIONS = {
    "world-intelligence": "109d9bebd9d34cc1c920202c57958c7f0155c7ac",
    "tads": "eee3c96d0c7d00fa5441d9509873fbc9e7402edd",
    "sdea": "94e2abcc8c34bb91792791f101b72172dd7a2d16",
    "reconos": "a033a821e37f97f2d55466263b2a84daa9c6fb45",
    "fadereach": "4c5b7d70c937ca8227ba8a9ebfe0d69b3e5c2bf8",
}

SYSTEM_REPOSITORIES = {
    "world-intelligence": "LloydCoder/tinlance-world-intelligence",
    "tads": "LloydCoder/tinlance-tads",
    "sdea": "LloydCoder/tinlance-sdea",
    "reconos": "LloydCoder/reconos-ofe",
    "fadereach": "LloydCoder/fadereach",
}


def fetch_text(url: str) -> str:
    request = Request(url, headers={"Accept": "text/plain", "User-Agent": "tinlance-tsic-certifier"})
    with urlopen(request, timeout=20) as response:
        if response.status != 200:
            raise RuntimeError(f"fetch failed: HTTP {response.status} {url}")
        return response.read().decode("utf-8")


def fetch_json(url: str) -> dict:
    return json.loads(fetch_text(url))


def main() -> None:
    baseline = fetch_json(f"{ROOT}/LloydCoder/tinlance-system-integration/{TSIC_REVISION}/{BASELINE_PATH}")
    assert baseline["authority"] == "tsic"
    assert baseline["sequence"] == list(SYSTEM_REPOSITORIES)
    assert baseline["tsic"]["ref"] == TSIC_REVISION

    feedback = baseline["feedback"]
    assert feedback["from"] == "fadereach"
    assert feedback["through"] == [
        "sales",
        "fdse",
        "outcome",
        "evidence",
        "economic-attribution",
        "evaluation",
    ]
    assert feedback["returns_to"] == ["tads", "sdea"]
    assert feedback["rule"] == "feedback_is_learning_input_not_execution_authority"

    for system_id, repository in SYSTEM_REPOSITORIES.items():
        assert baseline["systems"][system_id]["repository"] == repository
        reviewed_ref = baseline["systems"][system_id]["ref"]
        assert reviewed_ref and len(reviewed_ref) == 40

        # Verify the reviewed repository revision is reachable and contains its
        # executable TSIC conformance gate.
        script_url = f"{ROOT}/{repository}/{reviewed_ref}/scripts/tsic_conformance.py"
        script = fetch_text(script_url)
        assert "TSIC_REVISION" in script
        expected_adapter_revision = ADAPTER_REVISIONS[system_id]
        assert expected_adapter_revision in script, (
            f"{system_id}: conformance gate is not pinned to {expected_adapter_revision}"
        )

        adapter = fetch_json(
            f"{ROOT}/LloydCoder/tinlance-system-integration/{TSIC_REVISION}"
            f"/integrations/{system_id}/adapter.json"
        )
        assert adapter["source_system"] == "tsic"
        assert adapter["target_system"] == system_id
        assert adapter["status"] == "reference-contract"
        assert adapter["authority"]["integration_contracts"] == "tsic"
        assert adapter["authority"]["execution_authority"] == "agent-platform"

    print(
        "PASS TSIC-25 Acquisition System certification: "
        f"baseline={baseline['baseline_id']} systems={len(SYSTEM_REPOSITORIES)}"
    )


if __name__ == "__main__":
    main()
