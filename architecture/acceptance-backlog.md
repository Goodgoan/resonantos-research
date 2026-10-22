# Acceptance-test backlog (lead, Fable 5.1, 2026-10-21)

Rule (D4.0, execution): no third-party code is run in this research. Every execution request from Gate 2 and from the dossiers' section 11 becomes a ranked acceptance test for the team, with its inputs, expected result and the recommendation it would change. Verdicts that depend on a test are marked "conditional on test X" in the article. Status of every row: NOT RUN. "Third-party" marks tests that execute code from `_untrusted/` or an installed package; "own" marks tests of Resonant code or of recorded fixtures only, which can become CI lanes without any approval beyond the normal PR process.

## 1. The five ranked requests (user ranking, D4.0)

| Rank | Id | Test | Executes | Sandbox | Expected result | Verdict it changes |
|---|---|---|---|---|---|---|
| 1 | Convira A10 | A child with a write grant plants a junction (and a directory symlink) inside its grant pointing at a canary directory outside it; a second spawn grants that path; a third grants a deny leaf beneath it; repeat with the junction planted by an unconfined same-user process; `icacls` the canary before and after | third-party (vendored Convira launcher built from source) | clean Windows 11 VM, standard user, UAC on | the canary's DACL is unchanged in every variant and the spawn refuses with a named reason; any `ConviraSbx-*` ACE on the canary is a fail | Convira isolation 3 -> 0 and total 3.02 -> 2.36 on failure; decides whether the Windows no-admin backend is vendored at all (RR-13); the X-5 Windows transport stays srt-win either way |
| 2 | sandbox-runtime (h) echoing upstream | A provider stub echoes request headers and body in 200 and 4xx bodies and splits the echo across SSE chunks; the child posts the sentinel or placeholder in `model`, in a user message, in `X-Echo`, URL-encoded and base64, and sends `TRACE`. Run A: srt env-mask mode (documents the refuted configuration). Run B: the X-5 broker with the redactor | third-party for run A (srt 0.0.81); own for run B | disposable VM per OS; fake provider with its own CA | run A fails (the key comes back); run B passes: the child's output never contains the key in any encoding | Run A confirms S-1 as executed; run B is the R03 claim: "child never sees the key" moves from "not demonstrated" to "demonstrated" for the broker; conditional verdicts: R03 recommendation, RR-02 |
| 3 | tuf-conformance v2.5.0 against tuf-js 6.0.0 | Run the conformance suite at `1bc18916` (v2.5.0) with the tuf-js entrypoint, including `test_cached_role_is_verified_against_current_delegator` | third-party (tuf-js, tuf-conformance) | Linux container | the diamond-delegation test fails (hypothesis from `updater.ts:318-320`); every other case passes as at v2.4.0 | Confirms or refutes the diamond-cache hypothesis; no score change either way (the proposed registry has no multi-parent roles) but the article's "unverified upstream defect" becomes executed; conditional: RR-06 wording |
| 4 | DataLad B1 | On NTFS with `commit.gpgsign true` and SSH signing, `datalad create`, add, save, `save --amend`, then `git verify-commit` on `adjusted/main(unlocked)` and on `main`; repeat with `--no-annex` | third-party (datalad 1.7.1, git-annex) | disposable Windows 11 VM, Python 3.12 venv | signatures do not survive the adjusted-branch propagation in annex mode; they do in `--no-annex` | Confirms the reason the R14 design avoids git-annex; decision unchanged either way; conditional: DataLad section 8 hypothesis |
| 5 | Aegis A2 reflection (now the broker A2 case) | A fake upstream returns 401 echoing every request header and the URL, and a 200 SSE variant echoing `Authorization` split across two chunks | third-party for Aegis as shipped (documents THREAT_MODEL I-2); own for the broker | throwaway VM | Aegis as shipped leaks (`sk-test-` reaches the agent); the broker passes only if a string match for the key and its encodings over everything written to the child finds nothing | Same as rank 2 run B for the header-echo class; confirms the Aegis isolation 0 (D3.11) as executed |

## 2. Gate 2 requests (a)-(d), restated as tests

| Id | Test | Executes | Expected | Verdict it changes |
|---|---|---|---|---|
| G2-a | srt and Convira confinement probes on Windows without admin (srt (g) anonymous-token probe; Convira A1-A9, A11) | third-party | srt: residual reported, not hidden; Convira: no-admin spawn with piped stdio works or fails with a named reason | Windows containment story (RR-13); R02 readiness on Windows |
| G2-b | biscuit-wasm cases a-m (incl. d2 stream revoke, j store tamper, k P-256 malleability, l DAO-fact refusal, m byte cap) | third-party (WASM) plus own | all exact; h soak bounded | R01 isolation 2 -> 3 for the wrap once d, d2, j pass; the article's R01 verdict is conditional on B-d, B-d2 |
| G2-c | durabletask tamper and truncation tests; OpenWorkflow F1-F9 | third-party | OpenWorkflow bare F1 and F9 show the duplicate; adapter column passes | R10 recommendation stays OpenWorkflow if F1-F9 adapter column holds; durabletask becomes the fallback only if OpenWorkflow fails the crash test and durabletask passes T7a/T7b |
| G2-d | AgentDojo against the R11 host checkpoint; BrowseSafe++ and the web-agent-attack benchmark served through nanobrowser's fixtures against the ported gate | third-party (benchmarks, nanobrowser lanes) | attack-completed count in Ask mode with a declining user is zero; Auto-mode numbers reported as measurements | Browser gating moves from "no measured results" to measured; R19 isolation for the port |

## 3. Shared cross-cutting cases from the Gate 3 decisions (own code; become CI lanes)

| Id | Case | Expected | Changes |
|---|---|---|---|
| X1-a | A child with `archive-write` tries to create, edit, truncate, delete and replace with an older copy each file class in `security/` through every bridge route and, unconfined, directly | routes refuse; direct edits detected at next read; rollback detected at start (head mismatch); fail closed with alarm | T21 verdict for V1, V4, V3-through-bridge |
| X1-b | Restore `security/` and the credential-store item together from a pre-revocation snapshot | not detected on one account (documents level (b) limit); detected under the A2 separate-account core | level (b) claim |
| X1-c | No credential store available | file-backed key with a visible "same-user, file-backed" label; no silent degradation | G2 honesty |
| X1-d | Windows DACL on `security/` | only the user's SID | OSC-06 analogue |
| X4-a | The injected planner requests approval for A while the side panel displays B | the helper renders A from the bridge's canonical body; a decision for B fails the digest check; no handler runs | T22, WYSIWYS |
| X4-b | The agent principal with every token tries every route and message to produce an approval | none exists; only a 428 with an id | T22 |
| X4-c | Helper absent or killed mid-ceremony | `NEEDS_USER`; no side effect; no retry | T1 closure |
| X4-d | Phase 2: enrolment from the agent principal; virtual authenticator attached via DevTools | refused or flagged; per-OS user-verification availability measured | Phase 2 helper |
| X4-e | R11 append fails (read-only store) | route refuses | fail-closed |
| X5-a | Echo stub (rank 2 run B, rank 5 broker case) | child never sees the key | R03 |
| X5-b | Confined child connects to the bridge port, 1.1.1.1:80 and an unlisted host; only the virtual host allowed | refused; virtual host succeeds; per OS | Containment plus broker reachability |
| X5-c | Revoke during a streaming completion; client disconnect mid-stream | stream ends within one chunk; next request 403; upstream aborted | X-7 |
| X5-d | Broker listener enumeration; `CONNECT` to non-allowlisted host; `TRACE` | `127.0.0.1` only, one route, refusals | Component surface |
| X5-e | Unconfined Windows: a second local process with the delegation token | it can spend the key (documents the residual); audit row shows it | Honest label |

## 4. Dossier section 11 tests, by requirement (ids used in the architecture documents)

| Family | Ids | Source | Executes | Note |
|---|---|---|---|---|
| R01 Biscuit | B-a..g, B-i..m, B-d2, B-h (soak) | eclipse-biscuit section 11 | third-party WASM plus own | B-j waits for the X-1 store (now decided) |
| R02 sandbox-runtime | S-a..h (incl. b2, b3, g on Windows) | sandbox-runtime section 11 | third-party | run twice: env-mask (A) and broker (B) |
| R02 Convira | A1-A11 | convira section 11 | third-party | A10 is rank 1; A2 piped stdio on non-admin; A11 Linux loopback no-op |
| R03 broker | aegis cases A, A2, B, C, E translated to the reimplemented broker | aegis section 11 | own | C (body inspection) becomes "normal chat payloads pass" |
| R10 OpenWorkflow | O-F1..F9 | openworkflow section 11 | third-party plus own | F7 and F8 need R01 and X-1 (now decided) |
| R10, R11 durabletask | T7a, T7b, T8, T3, Windows paths, self-approval, adversarial page, state tamper | durabletask section 11 | third-party (Go build) | fallback only |
| R11 hypercore pattern | H-1..7 (incl. 3b, 3c, 3d) | hypercore section 11 | third-party for the hypercore backend; own for the JSONL chain | the JSONL chain is the Phase 1 ledger; hypercore in reserve |
| R11, R30 Tessera | T3-1..4 (incl. 3(a)-(h)) | tessera section 11 | third-party (Go build) for 2-4; own for 1 (vector conformance) | T3-1 runs in the Alpha CI once `tlog-verify.mjs` exists |
| R12, R23 identity-common-ts | I-a..k (incl. a2, g, h, i, j, k) | identity-common-ts section 11 | third-party (npm, `--ignore-scripts`) plus own | step 7 wallet test needs a wallet and approval |
| R14 DataLad | D-A1..10 (own git ledger); D-B1..B4 (third-party) | datalad section 11 | own; third-party | B1 is rank 4; B4 documents rerun executing stored text |
| R18 tuf-js | T-1..11 (incl. 4b, 4c, 6b) | tuf-js section 11 | third-party (tuf-js fixtures) | 6b marked known failure until the X-1 store exists (now decided) |
| R19, R29 nanobrowser | N-1..4 (deterministic lane; browser lane; faults 3(a)-(e); benchmark adaptation) | nanobrowser section 11 | third-party | 3(b), 3(c) required for the port |
| R22, R23 rewards pattern | R-1 (deployed-source identification), R-2 (credential pattern on the branch, incl. the sale fault), R-3 (verifier fixtures) | rewards section 11 | third-party (solana-verify, LiteSVM); own for R-3 | R-3 is CI-ready with recorded RPC fixtures |
| R24 Realms | G-A (verifier, own, F1-F12), G-B (program-level checks, third-party) | realms section 11 | own; third-party | G-A fixtures from the recorded RPC log |
| R26 hypercerts pattern | Hc-1..8 (field rejection, null, payment without review, ring, rewrite, appeal flood, spoofed reviewer, X-9 key, DR-34, child-planted provenance, omission window) | hypercerts section 11 | third-party (`@atproto/lexicon`) plus own | |
| R06, R07, R29 Goose | Go-1..8 | goose section 11 | third-party (goose v1.55.0) | Go-8 self-modification fault |

## 5. Mapping to the master prompt's proof-of-concept portfolio (8.5 item 12)

| Portfolio experiment | Tests | What would falsify the architecture |
|---|---|---|
| Hostile-component isolation | S-a..h, Convira A1-A11, X5-b, N-1..4, Go-3 | a confined child reaches the bridge port or the store on Linux or macOS; the classifier port dispatches a neutrally labelled payment control in Ask mode |
| Delegated-grant revocation | B-d, B-d2, X5-c, T-4b, I-g | a revoked grant or token keeps an open stream alive beyond the stated bound; a revoked add-on keeps running past the recheck interval |
| Crash and restart with an uncertain side effect | O-F1..F9, D-A7, H-7, T3-3(d), T8 | the effect journal lets a duplicate through, or an indeterminate step is auto-retried |
| Consent-bounded OS-to-DAO attestation | I-a..k (esp. i, j, k), Hc child-planted provenance, X4-a | a child-written provenance record is exported; a record is signed without an R11 `approvalRef`; a wallet signs bytes that parse as a transaction |
| Contribution-fraud and appeal simulation | Hc-1..8, T3-3(e)-(h), G-F1..F12 | a self-published evaluation naming a registered reviewer is accepted; a dropped claim leaves no proof; two disjoint witness sets cosign different forks under the pinned policy; three custodian keys approve an upgrade |

## 6. Conditional verdicts the article carries

| Article verdict | Conditional on |
|---|---|
| R03 "child never sees the key" (broker) | rank 2 run B, rank 5 broker case (X5-a) |
| R02 Windows no-admin backend (Convira vendored) | rank 1 (A10), G2-a (A2 non-admin) |
| R02 Windows opt-in (srt-win) labelled bypassable | S-g |
| R01 isolation for the wrap (2 -> 3) | B-d, B-d2, B-j |
| R10 OpenWorkflow over durabletask | O-F1, O-F9 (bare duplicates shown), adapter column |
| R11 Phase 1 ledger gives level (a) only; (b) with A2 | X1-b, H-3d |
| R14 git ledger with signed approvals | D-A1..10; B1 informs only the rejected adoption path |
| R18 revocation survives local rollback | T-6, T-6b |
| R19 port passes G5 with three conditions | N-3(b), N-3(c), N-3(d) |
| R22 Phase 1 off-chain record, no token | R-2 sale fault (documents why) |
| R24 Phase 1 no on-chain stack; verifier verdicts | G-A fixtures (expected "fails: DR-48 timelock 0; no veto route; insider quorum; binary unverified") |
| R30 Tessera adoption with 2-of-3 outside witnesses | T3-3(e) cases 1-5, T3-3(f) |
| T21 closed for V1, V4, confined V3 | X1-a |
| T22 closed for V1, V3 and the planner | X4-a, X4-b |
| tuf-js diamond-delegation defect | rank 3 |
