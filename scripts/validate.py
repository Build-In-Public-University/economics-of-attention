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
    ROOT / "docs/EXPERIMENT-ADJUDICATION-LIMITED-EXPLORATION.md",
    ROOT / "docs/EXPERIMENT-MODEL-C4.md",
    ROOT / "docs/EXPERIMENT-SEMANTIC-C4.md",
    ROOT / "docs/PAPER-QUALITY-GATES.md",
    ROOT / "src/attention_experiment.py",
    ROOT / "src/adjudication_experiment.py",
    ROOT / "artifacts/attention-v1/attention-regime-shift.json",
    ROOT / "artifacts/attention-v2/adjudication-limited-exploration.json",
    ROOT / "artifacts/attention-v3/model-c4-constrained-views.json",
    ROOT / "artifacts/attention-v4/semantic-c4-local.json",
    ROOT / "artifacts/attention-v4/semantic-c4-local-v41.json",
    ROOT / "artifacts/attention-v4/semantic-c4-codex-v41.json",
    ROOT / "artifacts/attention-v4/semantic-c4-provider.json",
    ROOT / "artifacts/quality-gates/paper-quality-gate.json",
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
    adjudication = json.loads((ROOT / "artifacts/attention-v2/adjudication-limited-exploration.json").read_text())
    assert adjudication["status"] == "synthetic_fixture_not_empirical"
    assert adjudication["config"]["adjudication_budget"] == 20
    model_c4 = json.loads((ROOT / "artifacts/attention-v3/model-c4-constrained-views.json").read_text())
    assert model_c4["status"] == "synthetic_fixture_not_empirical"
    assert model_c4["config"]["sampling_operations"] == 105
    for adapter in ("local", "provider"):
        semantic = json.loads((ROOT / f"artifacts/attention-v4/semantic-c4-{adapter}.json").read_text())
        assert semantic["status"] == "synthetic_fixture_not_empirical"
        assert semantic["adapter"] == adapter
    v41 = json.loads((ROOT / "artifacts/attention-v4/semantic-c4-local-v41.json").read_text())
    assert v41["config"]["claim_budget"] == 3
    assert all(row["candidate_count"] <= 3 for row in v41["rows"])
    codex = json.loads((ROOT / "artifacts/attention-v4/semantic-c4-codex-v41.json").read_text())
    assert codex["adapter"] == "codex"
    assert codex["config"]["claim_budget"] == 3
    quality = json.loads((ROOT / "artifacts/quality-gates/paper-quality-gate.json").read_text())
    assert quality["status"] == "pass"
    assert not quality["hard_failures"]
    assert not quality["claim_hard_failures"]
    print(f"validated {len(claims['claims'])} claims; no empirical results asserted")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
