# Gate 3 report: Stage 3 code inspection, review and scoring (lead, 2026-10-21)

Status: Gate 3 PASSED 2026-10-21 with the user's decisions D4.0 (section 7). Stage 3 complete including the R24 add-on inspection (16 dossiers). Next: architecture step and Stage 4 article on Fable 5.1 in a new lead session. Nothing third-party was executed; every finding is static inspection. Run log and decisions: `state.md` (D3.0-D3.14). Scores: `scoring/scores.csv` (19 rows) and `scoring/sensitivity-output.md` (regenerated 2026-10-21 after all amendments).

## 1. What was done

- 15 dossiers, all `STATUS: COMPLETE (amended after review, 2026-10-21)`, 14 sections each, each with a "Review responses" table in section 14. Six were written on 2026-10-21 by relaunched inspectors (D3.5); nine on 2026-10-20.
- Three fresh-context adversarial reviews (Opus 5.5): `reviews/security-engineer.md` (2 blockers, 32 major, 34 minor incl. threat model and weights), `reviews/code-archaeologist.md` (14 minor), `reviews/dao-skeptic.md` (1 blocker, 23 major, 19 minor).
- Every objection answered against the code (brief `reviews/BRIEF-stage3-amend.md`) by the six live inspectors and nine stand-in amenders. Across the fifteen dossiers almost all objections were accepted or partly accepted; three were disputed with evidence (two nanobrowser scoring majors, one openworkflow score-raise), and the remaining questions were settled by lead rulings D3.8-D3.13.
- Citation quality (archaeologist, 165 decision-carrying citations at the recorded SHAs): 158 PASS, 6 PARTIAL, 1 FAIL (fixed); 95.8% exact, 99.4% supporting.
- Threat model v0.2 (`ledger/threat-model-draft.md`): all 20 threat-model objections accepted; new T21-T24, A10-A11, V9-V10; section 4 properties rewritten.
- Scoring method corrected to the pre-registered fragility rule (D3.6); isolation anchor clarified (D3.7, D3.8, scale unchanged).
- Stage 2 closed: provenance FINAL v3, all verifier corrections applied or deliberately not applied (#10).

## 2. Results per codebase

Totals are 0-5 under the named profile; they rate the upstream artifact as inspected (D3.7 (c)), not the proposed Resonant layer.

| Requirement(s) | Codebase | Decision | Total (profile) |
|---|---|---|---|
| R01 | Eclipse Biscuit | wrap; Ed25519-only root, revoke on grant_id, revocation list in the bridge-only store | 3.28 (os_kernel) |
| R02 | anthropics/sandbox-runtime | wrap (Linux, macOS; Windows opt-in labelled bypassable) | 3.76 (os_kernel) |
| R03 | anthropics/sandbox-runtime (`srt proxy`) | conditional wrap: header-only standalone proxy with a Resonant decider in a separate process, plus response scrubbing; env-mask mode rejected (key reflection, blocker accepted) | 3.14 (os_kernel) |
| R02 (Windows) | Convira/convira-sandbox | vendor the Windows backend only; full review of 1,549 native lines and own builds; Linux adapter fails G2 | 3.02 (os_kernel) |
| R03, R01 | getaegis/aegis | learn and reimplement; unauthenticated all-interface stats listener (isolation 0, D3.11) | 2.20 (os_kernel) |
| R10 | OpenWorkflow | wrap core, pinned; effects never inside step.run; maximumAttempts does not stop re-execution after a crash | 3.08 (os_kernel) |
| R10, R11 | dapr/durabletask-go | learn the pattern; R10 fallback sidecar | 2.80 (os_kernel) |
| R11 | holepunchto/hypercore | rebuild the pattern; meets local tamper property (a) only; librocksdb writes not fsynced | 3.04 (os_kernel) |
| R11 / R30 | Tessera + tlog-witness | formats only for R11; adopt for the R30 witnessed log with 2-of-3 outside witnesses and signed receipts; candidate registry for R23 (not scored for R23) | 3.26 (os_kernel) / 3.28 (dao_contract) |
| R12 / R23 | identity-common-ts (@sd-jwt) | wrap behind a hardened adapter (key binding required, cnf checked, 128-bit salts) | 3.56 (R12) / 3.40 (R23) (dao_contract) |
| R14, R13 | DataLad | learn the pattern: plain git, signed approvals, run-record block; git-annex AGPL-3.0+ | 2.72 (user_facing_app) |
| R18 | tuf-js | adopt 6.0.0 pinned behind a wrapper with a Guardian-proof watermark; forceCache spec deviation confirmed | 3.74 (os_kernel) |
| R19 / R29 | Nanobrowser | learn the pattern, vendor pure modules; G5 fails for upstream as is, passes for the port under three conditions | 2.78 (os_kernel) / 2.60 (user_facing_app) |
| R22, R23 | solana-foundation/rewards | learn the pattern only; Points credential not on main, audited or deployed code; branch credential is issuer-movable; GHSA-8hgp-gwvv-wrjf | 2.08 (dao_contract) |
| R26, R12 | hypercerts-lexicon | learn the pattern and reimplement; owner-mutable records, forgeable reviewer identity | 2.66 (dao_contract) |
| R24 (added at Gate 3, D4.0) | Realms / spl-governance (Mythic-Project fork) vs Squads v4 | Phase 1: no on-chain governance stack (off-chain first); Realms reference only, Phase 2 only as a DAO-owned instance with delegation and electorate-authority blockers resolved; Squads v4 as later authority holder (AGPL-3.0, legal review). Shared GovER5.. instance fails T12: deployed source unknown (VERSION 3.1.7 vs public 3.1.3), 5-of-7 security council, hold-up 0, community veto disabled; governance CI failed 31 of 31 runs. Reviewed by reviews/dao-skeptic-r24.md (24 objections, 12 major; citation check 23 PASS, 1 PARTIAL of 24) | 2.54 (dao_contract) |
| R29, R06, R07 | Goose | wrap as one delegated runtime and MCP host over ACP stdio, fresh state per delegation; reject "ResonantOS as a layer over Goose" (no browser counterpart) | 3.52 (user_facing_app) |

Per-requirement competitor tables (sensitivity, any rank change counts): R01, R02, R03, R10, R12, R23, R29 stable; R11 fragile (tessera and hypercore swap when isolation is dropped). Whole-profile orders are indicative only and mostly fragile.

## 3. Findings that change the picture

1. No shortlisted codebase supplies an adoptable R22 membership credential; Phase 1 should be an off-chain signed record, no token (rewards dossier, DAO review).
2. The single most repeated defect: ten designs put security state where a delegated child can write it (security review X-1; threat T21).
3. Every approval design ends where the agent's own context can mint or misdisplay the approval (X-4; threat T22).
4. The R03 broker and the R02 containment conflict on the loopback port (X-5).
5. Human/AI attribution has no source anywhere: nothing in the Alpha produces the split, and the provenance key would be readable by the agent it attributes (DAO review C-6); T13 and T20 stay open.
6. No candidate's revocation meets DR-06 (reason, authority, evidence, appeal, reversible with history) (DAO review C-4).
7. Coverage gap: R24 is now covered (Gate 3 add-on); R25 and R27 have no dossier, and T13 (high) and T16 depend on them (DAO review C-7). The article states this limit.
8. Governance capture runs mostly through the authorities that define the electorate (realm authority, voting-mint, weight-plugin configuration, quorum denominator), not through program upgrades; threat model v0.2.1 adds them to T12 and requires insiders to hold at most k-1 and a veto reachable by someone other than the approving quorum (R24 review).

## 4. Contested points (unresolved; to be reported as contested if not decided)

- tuf-js revocation: suspend at once with a logged user override (inspector) versus user confirmation before a remote disable takes effect (threat model v0.2, T19).
- Tessera: a stable per-member ledger key versus DR-32.
- Score proposed integrations separately from upstream artifacts (security X-3), or keep library-only rankings with that label.
- dao_contract weights: add an authority_and_capture criterion and raise requirement_fit (DAO review C-2); security W-5 (surface-added criterion) and W-6 (score-perturbation pass). These change weights after results; the user decides.

## 5. Execution requests (none approved or executed)

The four sandboxed-execution requests from gate2-report section 7, plus requests written into the dossiers' section 11 during Stage 3, among them: tuf-conformance v2.5.0 against tuf-js (diamond-delegation cache flaw); DataLad B1 (signature survival on Windows adjusted branches); Convira A10 (ACL grants following junctions and symlinks; failure drops its isolation to 0); sandbox-runtime acceptance (h) with an echoing upstream; Aegis A2 echo case. Each needs a specific user approval (D1.5).

## 6. Decisions for the user at Gate 3

1. Model for the architecture decision and the Stage 4 article: continue on Opus 5.5 now, or wait for Fable 5.1 credits (D3.1).
2. Coverage gap: accept and state it in the article, or run one more inspector on Realms plus Squads v4 for R24 (and optionally one for R25/R27).
3. The contested points in section 4: decide, or let the article report them as contested.
4. Execution requests in section 5: approve any specific runs, or keep static-only.
5. The architecture decisions X-1 (one bridge-only, integrity-protected security-state store), X-4 (approval path the agent cannot drive) and X-5 (broker transport; R03 to `srt proxy` or an aegis-pattern reimplementation) are the first work of the architecture step and run on the model chosen in decision 1.

## 7. Decisions taken at Gate 3 (user, 2026-10-21; full text state.md D4.0)

1. Model: architecture step and Stage 4 article on Fable 5.1, effort high, in a new lead session; Opus 5.5 for inspection and the article's adversarial review; Sonnet 5.5 for citation checks.
2. Coverage: R24 inspected (done, row above); R25 and R27 stay uninspected and the article says so.
3. Contested points, decided by the lead on the user's delegation: add-on revocation split by reason (security suspends at once with a logged, warned override; policy delisting never disables; reason class logged in the R30 log); Tessera member key rotates per epoch with per-epoch counts by entry type (DR-32 honoured); proposed layers get acceptance checklists, not scores; weights unchanged, plus a labelled capture-weighted what-if table, a governance checklist per architecture and a score-perturbation pass as extra reporting.
4. Execution: none in this research; the requests become ranked acceptance tests for the team: (1) Convira A10, (2) sandbox-runtime (h) echoing upstream, (3) tuf-conformance v2.5.0, (4) DataLad B1, (5) Aegis A2; affected verdicts are marked "conditional on test X".
5. The architecture decisions X-1, X-4, X-5 are the first work of the new Fable session, which shows them to the user before writing the article.
