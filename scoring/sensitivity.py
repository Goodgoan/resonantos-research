"""Stage 3 scoring and sensitivity check (master prompt 8.4).

Usage (from the research folder, with python -I):
    python -I scoring/sensitivity.py scoring/scores.csv scoring/weights.json > scoring/sensitivity-output.md

scores.csv columns: codebase_id, profile, requirement_ids, then one column per criterion in
weights.json "criteria" order, values 0-5, "NA" or "unknown". Unknown scores 0 and is flagged;
NA drops the criterion for that row and renormalises the remaining weights.

Output: baseline ranking per profile with weighted totals and reasons column passthrough,
then two perturbation checks: every weight +-25 percent (one at a time), and drop one
criterion at a time. A codebase whose baseline rank changes under any perturbation is
marked FRAGILE (weights.json _about; corrected 2026-10-21 from "more than one place", D3.6). Totals are shown to one decimal; the decision is the reasons.
"""
import csv, json, sys, itertools

def load(scores_path, weights_path):
    with open(weights_path, encoding="utf-8") as f:
        w = json.load(f)
    crit = w["criteria"]
    rows = []
    with open(scores_path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return crit, w["profiles"], rows

def total(row, crit, weights):
    num = 0.0; den = 0.0; unknown = []
    for c in crit:
        v = str(row.get(c, "")).strip().lower()
        if v in ("na", "n/a", ""):
            continue
        wgt = weights[c]
        if v == "unknown":
            unknown.append(c); s = 0.0
        else:
            s = float(v)
        num += s * wgt; den += wgt
    return (num / den if den else 0.0), unknown

def rank(rows, crit, weights):
    scored = []
    for r in rows:
        t, unk = total(r, crit, weights)
        scored.append((r["codebase_id"], t, unk))
    scored.sort(key=lambda x: -x[1])
    return scored

def positions(ranked):
    return {cid: i for i, (cid, _, _) in enumerate(ranked)}

def groups(rows, profiles):
    """Yield (title, profile_name, rows): one group per profile, then one per
    (profile, requirement) where at least two codebases compete for the same requirement."""
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
    print("# Scoring and sensitivity output\n")
    for title, pname, prows in groups(rows, profiles):
        prof = profiles[pname]
        weights = {c: float(prof[c]) for c in crit}
        base = rank(prows, crit, weights)
        basepos = positions(base)
        fragile = {cid: [] for cid, _, _ in base}
        for c in crit:
            for factor in (0.75, 1.25):
                w2 = dict(weights); w2[c] = weights[c] * factor
                for cid, pos in positions(rank(prows, crit, w2)).items():
                    if pos != basepos[cid]:
                        fragile[cid].append(f"{c} x{factor}")
        for c in crit:
            w2 = dict(weights); w2[c] = 0.0
            for cid, pos in positions(rank(prows, crit, w2)).items():
                if pos != basepos[cid]:
                    fragile[cid].append(f"drop {c}")
        print(f"## {title}\n")
        print("| Rank | Codebase | Weighted total (0-5) | Unknown criteria | Sensitivity |")
        print("|---|---|---|---|---|")
        for i, (cid, t, unk) in enumerate(base, 1):
            flag = "FRAGILE: " + "; ".join(sorted(set(fragile[cid]))) if fragile[cid] else "stable"
            print(f"| {i} | {cid} | {t:.1f} | {', '.join(unk) or '-'} | {flag} |")
        print()
    print("Totals are indicative. Read the dossiers' section 13 reasons before acting on a rank.")

if __name__ == "__main__":
    main()
