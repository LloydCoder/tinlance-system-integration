#!/usr/bin/env python3
"""Verify exact semantic parity between TSIC's canonical AaaS catalog and Tinlance.com."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL TSIC-18 site sync: " + message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-root", required=True, help="Checkout root for LloydCoder/Tinlance")
    args = parser.parse_args()
    site = Path(args.site_root).resolve()
    canonical = load(ROOT / "catalog/capabilities/aaas-offers.json")
    generated = load(site / "apps/web/lib/platform/aaas-offers.generated.json")
    require(canonical == generated, "website generated catalog differs from canonical TSIC catalog")
    require(canonical["commercial_surface"]["public_route"] == "/agent-as-a-service", "canonical route mismatch")
    require(canonical["commercial_surface"]["generated_catalog_path"] == "apps/web/lib/platform/aaas-offers.generated.json", "generated catalog path mismatch")

    route = site / "apps/web/app/agent-as-a-service/page.tsx"
    header = site / "apps/web/components/site-header.tsx"
    mobile = site / "apps/web/components/mobile-nav.tsx"
    sitemap = site / "apps/web/app/sitemap.ts"
    llms = site / "apps/web/app/llms.txt/route.ts"
    assessment = site / "apps/web/app/assessment/page.tsx"
    tests = site / "apps/web/tests/aaas-catalog.test.ts"
    required_files = [route, header, mobile, sitemap, llms, assessment, tests]
    missing = [str(path.relative_to(site)) for path in required_files if not path.is_file()]
    require(not missing, "website integration files missing: " + ", ".join(missing))

    route_text = route.read_text(encoding="utf-8")
    require("aaas-offers.generated.json" in route_text, "public page does not consume the generated catalog")
    require('href={`/assessment?capability=${encodeURIComponent(offer.name)}`}' in route_text, "offer CTA does not prefill the assessment")
    require("/agent-as-a-service" in header.read_text(encoding="utf-8"), "desktop navigation missing AaaS route")
    require("/agent-as-a-service" in mobile.read_text(encoding="utf-8"), "mobile navigation missing AaaS route")
    require("/agent-as-a-service" in sitemap.read_text(encoding="utf-8"), "sitemap missing AaaS route")
    require("https://tinlance.com/agent-as-a-service" in llms.read_text(encoding="utf-8"), "llms.txt missing AaaS route")
    assessment_text = assessment.read_text(encoding="utf-8")
    require("requestedCapability" in assessment_text and "window.location.search" in assessment_text, "assessment does not prefill the selected offer")
    test_text = tests.read_text(encoding="utf-8")
    require("FAS-Bench" in test_text or "fas-bench" in test_text, "site tests do not protect evaluation/runtime separation")
    require(len(canonical["offers"]) == 7, "canonical AaaS offer count changed; reconcile product copy and tests")
    require(all(offer["pricing"]["public_price"] is None for offer in canonical["offers"]), "unapproved public price found")
    print("PASS TSIC-18 site sync: canonical/generated catalog parity, route, navigation, sitemap, llms.txt, CTA and governance tests")


if __name__ == "__main__":
    main()
