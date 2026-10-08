#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
patterns=[
re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
re.compile(r"(?i)\baws_secret_access_key\s*[:=]\s*[A-Za-z0-9/+=]{16,}"),
re.compile(r"(?i)\b(?:api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]")
]
hits=[]
for p in ROOT.rglob("*"):
    if not p.is_file() or ".git" in p.parts or p.suffix.lower() not in {".md",".json",".yaml",".yml",".py",".toml",".txt",".sh"}: continue
    t=p.read_text(encoding="utf-8",errors="ignore")
    if any(rx.search(t) for rx in patterns): hits.append(str(p.relative_to(ROOT)))
if hits: raise SystemExit("FAIL potential secret patterns: "+", ".join(hits))
print("PASS security baseline: configured high-risk secret patterns not detected.")
