#!/usr/bin/env python3
"""Dependency-free structural checks for the paper repository."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ROOT / "README.md",
    ROOT / "papers/draft.md",
    ROOT / "claims/claims.json",
    ROOT / "docs/ARGUMENT-MAP.md",
    ROOT / "docs/RESEARCH-BOUNDARY.md",
    ROOT / "docs/HUB-CONNECTION.md",
    ROOT / "docs/RELATED-WORK-LEDGER.md",
    ROOT / "docs/FOUNDATIONAL-CITATIONS.md",
    ROOT / "docs/FORMAL-MODEL.md",
    ROOT / "docs/EXPERIMENT-ATTENTION-REGIME-SHIFT.md",
    ROOT / "src/attention_experiment.py",
    ROOT / "artifacts/attention-v1/attention-regime-shift.json",
]

def main() -> int:
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.is_file()]
    if missing:
        raise SystemExit(f"missing required files: {missing}")
    claims = json.loads((ROOT / "claims/claims.json").read_text())
    assert claims["status"] == "conceptual_draft_no_empirical_results"
    assert claims["claims"]
    ids = {c["id"] for c in claims["claims"]}
    for claim in claims["claims"]:
        for key in ("id", "type", "wording", "evidence_status", "falsifier", "evidence_ceiling"):
            assert claim.get(key), f"{claim['id']} missing {key}"
        if "evidence_receipt" in claim:
            assert (ROOT / claim["evidence_receipt"]).is_file(), f"{claim['id']} receipt missing"
        assert set(claim.get("depends_on", [])) <= ids | {d["id"] for d in claims["definitions"]}
    draft = (ROOT / "papers/draft.md").read_text()
    for marker in ("## Abstract", "## 3. Meaning", "## 8. Propositions", "No empirical result"):
        assert marker in draft, f"draft missing marker: {marker}"
    boundary = (ROOT / "docs/RESEARCH-BOUNDARY.md").read_text()
    assert "Not established" in boundary and "empirical" in boundary
    receipt = json.loads((ROOT / "artifacts/attention-v1/attention-regime-shift.json").read_text())
    assert receipt["status"] == "synthetic_fixture_not_empirical"
    assert set(receipt["claim_targets"]) == {"C1", "C4"}
    print(f"validated {len(claims['claims'])} claims; no empirical results asserted")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
