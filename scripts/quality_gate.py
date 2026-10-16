#!/usr/bin/env python3
"""Mechanical scholarly quality gates for the Economics of Attention draft."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = (ROOT / "papers/draft.md").read_text()
CLAIMS = json.loads((ROOT / "claims/claims.json").read_text())


def gate(name: str, passed: bool, hard: bool, evidence: str) -> dict:
    return {"gate": name, "status": "pass" if passed else "fail", "hard": hard, "evidence": evidence}


def main() -> int:
    checks = [
        gate("lineage", all(term in DRAFT for term in ("Shannon", "Hayek", "Grossman", "Transformer")), True, "found named inherited frameworks"),
        gate("mechanism", all(term in DRAFT for term in ("X_t\\rightarrow A_t", "action", "feedback")), True, "control loop and action pathway present"),
        gate("cost", all(term in DRAFT for term in ("C_i(A)", "sensing", "adjudication", "cost")), True, "operating and downstream costs named"),
        gate("partition", all(term in DRAFT for term in ("partition", "support", "operationally invisible")), True, "visibility and retained support are explicit"),
        gate("compression", all(term in DRAFT for term in ("lossy", "discard", "blind spot")), True, "loss and regime-dependent blindness are explicit"),
        gate("consequence", all(term in DRAFT for term in ("action", "value", "utility")), True, "meaning is tied to action value"),
        gate("evidence_level", all(term in DRAFT for term in ("synthetic", "external systems", "production AI")), True, "synthetic-to-external boundary is stated"),
        gate("negative_boundary", all(term in DRAFT for term in ("does not establish", "does not imply", "not evidence")), True, "stronger readings are rejected"),
        gate("falsification", "falsifier" in DRAFT and all(c.get("falsifier") for c in CLAIMS["claims"] if c["type"] != "definition"), True, "claim ledger and draft expose falsifiers"),
        gate("citation_lineage", all(term in DRAFT for term in ("Shannon", "Hayek", "Grossman–Stiglitz")), True, "foundational lineage named; bibliographic verification remains ledger-bound"),
        gate("concrete_example", False, False, "no single running empirical case is yet carried through every section"),
        gate("faithful_compression", "boxed" in DRAFT and "rightarrow" in DRAFT, False, "equations and transformation chains present"),
    ]
    bounded = [c for c in CLAIMS["claims"] if c["type"] != "definition"]
    claim_matrix = []
    for claim in bounded:
        wording = claim["wording"].lower()
        row = {
            "claim": claim["id"],
            "lineage_presence": {"status": "pass" if claim.get("depends_on") else "fail", "basis": "depends_on registered"},
            "mechanism": {"status": "pass" if any(term in wording for term in ("when", "as ", "improves", "loses", "update")) else "fail", "basis": "claim wording contains a process relation"},
            "cost": {"status": "pass" if any(term in wording for term in ("cost", "budget", "value", "private excess")) else "fail", "basis": "cost/value language appears in claim wording"},
            "partition": {"status": "pass" if any(term in wording for term in ("attention", "label", "category", "signal")) else "fail", "basis": "visibility/filter language appears in claim wording"},
            "consequence": {"status": "pass" if any(term in wording for term in ("action", "detection", "value", "decay", "update")) else "fail", "basis": "consequence language appears in claim wording"},
            "boundary": {"status": "pass" if claim.get("evidence_ceiling") else "fail", "basis": "evidence ceiling registered"},
            "falsifier": {"status": "pass" if claim.get("falsifier") else "fail", "basis": "falsifier registered"},
            "source_support": {"status": "manual_review", "basis": "mechanical presence is not source-to-claim support"},
            "concrete_example": {"status": "fail", "basis": "no running example is mapped claim-by-claim yet"},
        }
        claim_matrix.append(row)
    claim_hard_gates = ("lineage_presence", "mechanism", "cost", "partition", "consequence", "boundary", "falsifier")
    claim_hard_failures = [f"{row['claim']}:{gate_name}" for row in claim_matrix for gate_name in claim_hard_gates if row[gate_name]["status"] != "pass"]
    hard_failures = [x for x in checks if x["hard"] and x["status"] != "pass"]
    report = {"status": "pass" if not hard_failures and not claim_hard_failures else "review_required", "hard_failures": [x["gate"] for x in hard_failures], "claim_hard_failures": claim_hard_failures, "checks": checks, "claim_matrix": claim_matrix, "boundary": "Mechanical gate only; passing does not establish scholarly correctness. Source support remains manual."}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if hard_failures or claim_hard_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
