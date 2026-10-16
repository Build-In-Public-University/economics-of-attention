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
    hard_failures = [x for x in checks if x["hard"] and x["status"] != "pass"]
    report = {"status": "pass" if not hard_failures else "fail", "hard_failures": [x["gate"] for x in hard_failures], "checks": checks, "boundary": "Mechanical gate only; passing does not establish scholarly correctness."}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if hard_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
