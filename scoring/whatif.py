"""What-if reporting added at Gate 3 (state.md D4.0 (3)(d)); weights.json is unchanged.

Usage (from the research folder, with python -I):
    python -I scoring/whatif.py scoring/scores.csv scoring/weights.json > scoring/whatif-output.md

Two extra reports, clearly labelled as reporting only, not the decision weights:
1. The DAO skeptic's capture-weighted profile (reviews/dao-skeptic.md C-2) applied to the
   dao_contract rows: requirement_fit 0.22, isolation 0.24, maturity 0.16, maintenance 0.12,
   licence 0.06, integration 0.04, sovereignty 0.06, interoperability 0.04, operations 0.06.
2. The security review's W-6 score-perturbation pass: for every group that sensitivity.py
   reports, each candidate's isolation_and_security score is moved by +1 and by -1 (clamped to
   0..5) one candidate at a time; a rank that changes under either move is marked FLIPS.
The baseline totals and the grouping rule are the same as sensitivity.py (any rank change counts).
"""
import csv, json, sys

CAPTURE = {
    "requirement_fit": 0.22, "isolation_and_security": 0.24, "demonstrated_maturity": 0.16,
    "maintenance_sustainability": 0.12, "licence_suitability": 0.06, "integration_effort": 0.04,
    "sovereignty_and_portability": 0.06, "interoperability": 0.04, "operational_complexity": 0.06,
}

def load(scores_path, weights_path):
    with open(weights_path, encoding="utf-8") as f:
        w = json.load(f)
    rows = []
    with open(scores_path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return w["criteria"], w["profiles"], rows

def total(row, crit, weights):
    num = 0.0; den = 0.0
    for c in crit:
        v = str(row.get(c, "")).strip().lower()
        if v in ("na", "n/a", ""):
            continue
        s = 0.0 if v == "unknown" else float(v)
        num += s * weights[c]; den += weights[c]
    return num / den if den else 0.0

def rank(rows, crit, weights):
    scored = sorted(((r["codebase_id"], total(r, crit, weights)) for r in rows), key=lambda x: -x[1])
    return scored

def positions(ranked):
    return {cid: i for i, (cid, _) in enumerate(ranked)}

def groups(rows, profiles):
    for pname in profiles:
        prows = [r for r in rows if r.get("profile") == pname]
        if prows:
            yield f"Profile: {pname} (all requirements; cross-requirement order is indicative only)", pname, prows
    for pname in profiles:
        prows = [r for r in rows if r.get("profile") == pname]
        reqs = sorted({q for r in prows for q in str(r.get("requirement_ids", "")).split(";") if q})
        for q in reqs:
            qrows = [r for r in prows if q in str(r.get("requirement_ids", "")).split(";")]
            if len(qrows) >= 2:
                yield f"Requirement {q}, profile {pname} (competitors)", pname, qrows

def main():
    scores_path, weights_path = sys.argv[1], sys.argv[2]
    crit, profiles, rows = load(scores_path, weights_path)
    print("# What-if reporting (Gate 3, D4.0 (3)(d)): capture-weighted profile and score perturbation\n")
    print("These tables are reporting only. The decision weights in `weights.json` are unchanged, and no reference architecture or proposed layer is scored (D4.0 (3)(c)). Totals rate the upstream artifact as inspected (D3.7 (c)).\n")

    print("## 1. What if the DAO skeptic's capture-weighted profile were used for dao_contract?\n")
    print("Weights: requirement_fit 0.22, isolation_and_security 0.24, demonstrated_maturity 0.16, maintenance_sustainability 0.12, licence 0.06, integration 0.04, sovereignty 0.06, interoperability 0.04, operations 0.06 (reviews/dao-skeptic.md C-2). Baseline = the pre-registered dao_contract weights.\n")
    dao = [r for r in rows if r.get("profile") == "dao_contract"]
    base_w = {c: float(profiles["dao_contract"][c]) for c in crit}
    base = rank(dao, crit, base_w); basepos = positions(base)
    cap = rank(dao, crit, CAPTURE); cappos = positions(cap)
    print("| Capture rank | Codebase | Capture total | Baseline total | Baseline rank | Change |")
    print("|---|---|---|---|---|---|")
    bt = {cid: t for cid, t in base}
    for i, (cid, t) in enumerate(cap, 1):
        delta = basepos[cid] - cappos[cid]
        change = "same" if delta == 0 else (f"up {delta}" if delta > 0 else f"down {-delta}")
        print(f"| {i} | {cid} | {t:.2f} | {bt[cid]:.2f} | {basepos[cid]+1} | {change} |")
    print()
    print("Reading: the capture profile shifts weight from the five convenience criteria (licence, integration, sovereignty, interoperability, operations: 0.36 of the baseline) to requirement fit and isolation (0.46). Ranks that move under it are listed above; the article reports them beside the baseline, not instead of it.\n")

    print("## 2. W-6 score-perturbation pass (isolation_and_security +1 and -1 per candidate)\n")
    print("For each group below, each candidate's isolation score is moved by +1 and then by -1 (clamped to 0..5), one candidate at a time, with the pre-registered weights. FLIPS lists the moves that change that candidate's rank; a flip under a one-point change on the heaviest criterion is as fragile as a weight flip (reviews/security-engineer.md W-6).\n")
    for title, pname, prows in groups(rows, profiles):
        weights = {c: float(profiles[pname][c]) for c in crit}
        base = rank(prows, crit, weights); basepos = positions(base)
        flips = {cid: [] for cid, _ in base}
        for r in prows:
            v = str(r.get("isolation_and_security", "")).strip().lower()
            if v in ("na", "n/a", "", "unknown"):
                continue
            cur = float(v)
            for delta in (1, -1):
                new = min(5.0, max(0.0, cur + delta))
                if new == cur:
                    continue
                r2 = dict(r); r2["isolation_and_security"] = str(new)
                prows2 = [r2 if x is r else x for x in prows]
                for cid, pos in positions(rank(prows2, crit, weights)).items():
                    if pos != basepos[cid]:
                        flips[cid].append(f"{r['codebase_id']} iso {'+' if delta > 0 else '-'}1")
        print(f"### {title}\n")
        print("| Rank | Codebase | Baseline total | Isolation | Perturbation result |")
        print("|---|---|---|---|---|")
        iso = {r["codebase_id"]: r.get("isolation_and_security") for r in prows}
        for i, (cid, t) in enumerate(base, 1):
            flag = "FLIPS: " + "; ".join(sorted(set(flips[cid]))) if flips[cid] else "stable"
            print(f"| {i} | {cid} | {t:.2f} | {iso[cid]} | {flag} |")
        print()
    print("Totals are indicative. Read the dossiers' section 13 reasons before acting on a rank.")

if __name__ == "__main__":
    main()
