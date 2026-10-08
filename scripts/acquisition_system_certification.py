#!/usr/bin/env python3
"""Fail-closed certification of the reviewed Tinlance Acquisition System baseline."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).parents[1]
TSIC_REVISION = "4c5b7d70c937ca8227ba8a9ebfe0d69b3e5c2bf8"
BASELINE_PATH = ROOT / "policies/acquisition-system-baseline.json"

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


def fetch_reviewed_file(repository: str, revision: str, path: str) -> str:
    owner, name = repository.split("/", 1)
    url = f"https://github.com/{owner}/{name}/raw/{revision}/{path}"
    request = Request(url, headers={"Accept": "text/plain", "User-Agent": "tinlance-tsic-certifier"})
    with urlopen(request, timeout=20) as response:
        if response.status != 200:
            raise RuntimeError(f"fetch failed: HTTP {response.status} {url}")
        return response.read().decode("utf-8")


def main() -> None:
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
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
        system = baseline["systems"][system_id.replace("-", "_")]
        assert system["repository"] == repository
        reviewed_ref = system["ref"]
        assert reviewed_ref and len(reviewed_ref) == 40

        try:
            conformance = fetch_reviewed_file(repository, reviewed_ref, "scripts/tsic_conformance.py")
        except Exception as exc:
            raise RuntimeError(
                f"{system_id}: unable to fetch reviewed conformance gate "
                f"{repository}@{reviewed_ref}: {exc}"
            ) from exc

        expected_adapter_revision = ADAPTER_REVISIONS[system_id]
        assert "TSIC_REVISION" in conformance
        assert expected_adapter_revision in conformance, (
            f"{system_id}: conformance gate is not pinned to {expected_adapter_revision}"
        )

        adapter_path = ROOT / "integrations" / system_id / "adapter.json"
        adapter = json.loads(adapter_path.read_text(encoding="utf-8"))
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
