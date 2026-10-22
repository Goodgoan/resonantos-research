# Stage 3 brief: answering the adversarial reviews (lead, 2026-10-21)

Three fresh-context reviewers have read every dossier. You answer the objections against one dossier, amend it, and report. You are either the inspector who wrote it, or an amender standing in for an inspector who is no longer reachable; in the second case you read `dossiers\BRIEF-stage3-inspectors.md` first and treat the dossier as your own from now on. Either way, the inspector brief's rules on untrusted clones, evidence labels, citations and no execution still bind you.

## 1. Find your objections

Your dossier slug is in your launch message. Read the section headed with your slug in each of:
- `reviews\security-engineer.md` (ids `S-<slug>-n`)
- `reviews\code-archaeologist.md` (ids `A-<slug>-n`, plus the citation spot-check rows for your dossier)
- `reviews\dao-skeptic.md` (ids `D-<slug>-n`; the OS dossiers are grouped under "OS dossiers checked for invariant I2")

Then read each review's cross-cutting section and take every pattern that names your dossier as an objection too (security X-1 to X-10, archaeologist cross-cutting, DAO skeptic C-1 to C-8). Threat-model and weights objections (TM-*, W-*, C-1, C-2) are the lead's; answer them only where they change a score in your section 13.

## 2. Answer each one against the code

A reviewer can be wrong. For every objection, go back to the clone at the dossier's recorded SHA (or the cited URL) and decide:
- **accepted**: amend the section it names, with the corrected claim, label and citation;
- **partly accepted**: amend what holds, and say what does not, with evidence;
- **disputed**: leave the section, and give the evidence (file:line, command, URL) that the objection is wrong.

Do not accept an objection only because it is phrased firmly, and do not dispute one without new evidence. A blocker that you accept may change the reuse decision or a hard gate; say so in sections 6 and 12.

## 3. Mandatory fixes from the reviews

- Line drift and failed citations listed by the archaeologist: fix every one.
- A claim taken from a README or docs but labelled `[inspected]`: relabel it `[reported]` or find the code.
- A count that did not reproduce: recount, and say how you counted (command or pattern).
- The header line `STATUS: COMPLETE (amended after review, 2026-10-21)` replaces any earlier status line; add one if the dossier has none.

## 4. Record it

Add to section 14 a table `### Review responses (2026-10-21)`:

| Id | Verdict | Change made (section) or evidence for dispute |
|---|---|---|

Every objection id that concerns your dossier appears exactly once. If a score in section 13 changes, show `old -> new` with the anchor reason, and recompute the weighted total with the profile weights in `scoring\weights.json`. Do not edit `scoring\scores.csv`; the lead copies section 13.

## 5. Boundaries and practice

- Write only your dossier. Your scratchpad subfolder is named in your launch message.
- Never run third-party code; any execution you would need is written as a request in section 11.
- Prefer single, simple read-only commands (`git -C`, `grep`, `sed -n`, `head`, `gh api` GET, `python -I` scripts in your scratchpad); unusual commands may need the user's approval.
- Save as you go: edit the dossier after each few objections, not once at the end.

## 6. Return message (at most 150 words)

Objections answered: accepted, partly accepted and disputed counts; each blocker and its verdict in one line; every score change `criterion old -> new` and the new weighted total; whether the reuse decision or any hard gate changed; the disputes the lead should settle, one line each.
