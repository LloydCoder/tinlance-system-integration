#!/usr/bin/env python3
"""Fail-closed certification of the reviewed Tinlance Acquisition System baseline."""

from __future__ import annotations

import base64
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
    url = f"https://api.github.com/repos/{repository}/contents/{path}?ref={revision}"
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "tinlance-tsic-certifier",
        },
    )
    with urlopen(request, timeout=20) as response:
        if response.status != 200:
            raise RuntimeError(f"GitHub contents API returned HTTP {response.status}: {url}")
        payload = json.load(response)
    if payload.get("type") != "file":
        raise RuntimeError(f"reviewed path is not a file: {url}")
    encoded = payload.get("content", "")
    return base64.b64decode(encoded.replace("\\n", "")).decode("utf-8")

