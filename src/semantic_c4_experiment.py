"""v4 semantic C4 harness: bounded document views, claims, and adjudication.

The local adapter is deterministic and dependency-free. The provider adapter is
OpenAI-compatible and opt-in via --provider; every run records prompt/context
hashes and raw outputs. Neither adapter is evidence about production AI.
"""
from __future__ import annotations
from dataclasses import dataclass
import argparse, hashlib, json, os, random, re, time, urllib.request

@dataclass(frozen=True)
class Config:
    claim_budget: int = 3
    context_docs: int = 3
    adjudication_budget: int = 4
    seeds: tuple[int, ...] = (0, 1, 2, 3, 4)

STABLE = [
    {"id":"s1","text":"The control panel reports that pump pressure is stable at 40 psi during normal operation.","topic":"pressure"},
    {"id":"s2","text":"The maintenance log records no valve failures in the last seven operating cycles.","topic":"maintenance"},
    {"id":"s3","text":"The standard operating procedure requires a 40 psi pressure check before launch.","topic":"procedure"},
    {"id":"s4","text":"The weekly summary states that output remains within the historical operating range.","topic":"output"},
    {"id":"s5","text":"The inventory report shows replacement seals available in the main warehouse.","topic":"inventory"},
]
SHIFTED = [
    {"id":"r1","text":"A corrosion note says the pressure sensor drifts upward only after the third hour of continuous operation.","topic":"sensor_drift"},
    {"id":"r2","text":"A field technician reports an intermittent bypass leak that is absent from the standard maintenance log.","topic":"bypass_leak"},
    {"id":"r3","text":"A handwritten shift note says the output range is misleading when the auxiliary pump is engaged.","topic":"auxiliary_pump"},
]


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def input_tokens(docs: list[dict]) -> int:
    return sum(len(str(doc["text"]).split()) for doc in docs)


def local_claims(docs: list[dict], regime: str, budget: int) -> list[dict]:
    # Deterministic bounded observer: extracts one claim per supplied document.
    return [{"source": d["id"], "claim": d["text"], "topic": d["topic"], "regime": regime} for d in docs[:budget]]


def provider_claims(docs: list[dict], regime: str, model: str, endpoint: str, budget: int) -> tuple[list[dict], dict]:
    prompt = {"regime": regime, "task":f"Return at most {budget} concise claims as JSON, each with source, claim, topic. Do not exceed the claim budget.", "documents":docs}
    body = json.dumps({"model": model, "temperature": 0, "messages":[{"role":"user","content":json.dumps(prompt)}]}).encode()
    request = urllib.request.Request(endpoint, data=body, headers={"Authorization":"Bearer "+os.environ["SEMAX_OPENROUTER_API_KEY"],"Content-Type":"application/json"})
    started = time.time()
    with urllib.request.urlopen(request, timeout=90) as response:
        raw = response.read().decode()
    payload = json.loads(raw)
    text = payload["choices"][0]["message"]["content"]
    match = re.search(r"\[[\s\S]*\]", text)
    claims = (json.loads(match.group(0)) if match else [])[:budget]
    return claims, {"model":model,"endpoint":endpoint,"request_hash":digest(prompt),"raw_hash":digest(raw),"latency_seconds":time.time()-started}


def adjudicate(claims: list[dict], regime: str, budget: int, stable_docs: list[dict]) -> list[dict]:
    # Ontology-free proxy: claims that introduce more lexical distinctions than
    # the stable summary receive more action-change score. Ground-truth shifted
    # IDs are used only for evaluation, never for ranking.
    stable_words = set(re.findall(r"[a-z]+", " ".join(d["text"].lower() for d in stable_docs)))
    scored=[]
    for claim in claims:
        words = set(re.findall(r"[a-z]+", str(claim.get("claim", "")).lower()))
        score = len(words - stable_words)
        scored.append((score, str(claim.get("source","")), claim))
    scored.sort(key=lambda x:(x[0],x[1]), reverse=True)
    return [claim for _,_,claim in scored[:budget]]


def run(adapter: str="local", model: str="gpt-5.6-luna", endpoint: str="https://openrouter.ai/api/v1/chat/completions", config: Config|None=None) -> dict:
    config=config or Config(); rows=[]
    for seed in config.seeds:
        rng=random.Random(seed)
        for regime, active in (("stable",STABLE),("shifted",STABLE+SHIFTED)):
            homogeneous_docs=(STABLE[:config.context_docs] * 2)[: config.context_docs * 2]
            scout_docs=rng.sample(STABLE+SHIFTED, config.context_docs * 2)
            views={"homogeneous":homogeneous_docs,"heterogeneous":scout_docs}
            for policy, docs in views.items():
                if adapter=="local": claims=local_claims(docs,regime,config.claim_budget); receipt={"adapter":"local"}
                else: claims,receipt=provider_claims(docs,regime,model,endpoint,config.claim_budget)
                selected=adjudicate(claims,regime,config.adjudication_budget,STABLE[:config.context_docs])
                novel=sum(1 for c in selected if str(c.get("source", "")).startswith("r"))
                rows.append({"seed":seed,"regime":regime,"policy":policy,"context_slots":len(docs),"input_token_count":input_tokens(docs),"candidate_count":len(claims),"selected_count":len(selected),"novel_claims":novel,"context_hash":digest(docs),"prompt_receipt":receipt})
    return {"schema_version":"1.0","status":"synthetic_fixture_not_empirical","instrument":"semantic_c4_context_claims","adapter":adapter,"config":config.__dict__,"rows":rows,"interpretation_boundary":"Synthetic document/claim substrate only; not evidence about human or production-model behavior."}


def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--output",required=True); p.add_argument("--adapter",choices=("local","provider"),default="local"); p.add_argument("--model",default="gpt-5.6-luna"); p.add_argument("--endpoint",default="https://openrouter.ai/api/v1/chat/completions"); a=p.parse_args()
    result=run(a.adapter,a.model,a.endpoint)
    with open(a.output,"w") as f: json.dump(result,f,indent=2,sort_keys=True); f.write("\n")
    print(a.output); return 0
if __name__=="__main__": raise SystemExit(main())
