#!/usr/bin/env python3
"""Forensically verify the TSIC-01 reference vertical slice and its CI pins."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ARTIFACTS = [
    "fixtures/agent-system/reference-agent.json",
    "scripts/agent_system_platform_server.py",
    "scripts/certify_agent_system_e2e.py",
    ".github/workflows/agent-system-e2e.yml",
    "integrations/agent-platform/adapter.json",
    "integrations/agent-platform-sdk/adapter.json",
    "integrations/agent-os/adapter.json",
    "integrations/agent-developer/adapter.json",
]
REQUIRED_REPOSITORIES = (
    "tinlance-agent-developer",
    "tinlance-agent-os",
    "tinlance-agent-platform-sdk",
    "tinlance-agent-platform",
)
REQUIRED_ACTIONS = {
    "actions/checkout",
    "actions/setup-python",
    "actions/setup-node",
    "actions/upload-artifact",
}
PINNED_ACTION = re.compile(
    r"^\s*uses:\s*([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)@([0-9a-f]{40})(?:\s|$)"
)


def main() -> None:
    missing = [path for path in REQUIRED_ARTIFACTS if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("FAIL phase1 artifacts: " + ", ".join(missing))

    fixture = json.loads((ROOT / REQUIRED_ARTIFACTS[0]).read_text(encoding="utf-8"))
    if fixture.get("apiVersion") != "tadl.tinlance.com/v1" or fixture.get("kind") != "Agent":
        raise SystemExit("FAIL phase1 reference fixture identity")

    workflow = (ROOT / ".github/workflows/agent-system-e2e.yml").read_text(encoding="utf-8")
    action_lines = [line for line in workflow.splitlines() if re.match(r"^\s*uses:", line)]
    pinned = {}
    for line in action_lines:
        match = PINNED_ACTION.match(line)
        if not match:
            raise SystemExit(f"FAIL unpinned or malformed action reference: {line.strip()}")
        action, revision = match.groups()
        if len(revision) != 40:
            raise SystemExit(f"FAIL action revision is not immutable: {action}")
        pinned.setdefault(action, set()).add(revision)

    missing_actions = REQUIRED_ACTIONS - pinned.keys()
    if missing_actions:
        raise SystemExit("FAIL missing required pinned actions: " + ", ".join(sorted(missing_actions)))

    for repository in REQUIRED_REPOSITORIES:
        if repository not in workflow:
            raise SystemExit(f"FAIL missing cross-repository checkout: {repository}")

    if "certify_agent_system_e2e.py" not in workflow or "test_agent_os_gateway.py" not in workflow:
        raise SystemExit("FAIL missing reference E2E certifier or governed gateway test")

    for path in REQUIRED_ARTIFACTS:
        artifact = ROOT / path
        if artifact.suffix in {".py", ".yml"} and not artifact.read_text(encoding="utf-8").strip():
            raise SystemExit(f"FAIL empty phase1 artifact: {path}")

    print(
        "PASS TSIC-01 post-phase forensic audit: "
        f"artifacts={len(REQUIRED_ARTIFACTS)} repositories={len(REQUIRED_REPOSITORIES)} "
        f"pinned_action_kinds={len(pinned)} action_references={len(action_lines)}"
    )


if __name__ == "__main__":
    main()
