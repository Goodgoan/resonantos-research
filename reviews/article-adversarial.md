STATUS: COMPLETE

# Adversarial review of article/ARTICLE.md and article/APPENDIX.md

- Date: 2026-10-21
- Agent: s4-rev-adversarial (fresh context, static inspection only; nothing executed, nothing fetched, `_untrusted/` read only through `git -C ... ls-tree/show`)
- Model: Opus 5.5
- Read in full: master prompt sections 6.5, 6.6, 8.5, 8.6, 9; `article/ARTICLE.md` (581 lines); `article/APPENDIX.md` (197 lines).
- Read in part (the lines cited per objection): `state.md` (D1.3, D3.6, D4.0-D5.4), `stage1/capability-matrix.md`, `stage1/interaction.md` section 6, `stage1/os-map.md`, `stage1/census-notes.md`, `ledger/threat-model-draft.md` section 4, `ledger/coverage-matrix.md` (a), `ledger/discovery-s2-lang-fr.jsonl`, `ledger/discovery-s2-lang-de.jsonl`, `ledger/gate2-report.md` (outline), `reviews/security-engineer.md` (cross-cutting, threat model, weights), `reviews/dao-skeptic.md` (C-1..C-8, TM), `reviews/dao-skeptic-r24.md` (summary), `reviews/gate3-report.md`, `dossiers/tuf-js.md`, `dossiers/convira-sandbox.md`, `dossiers/transparency-dev-tessera.md`, `dossiers/realms-spl-governance.md`, `dossiers/anthropics-sandbox-runtime.md`, `dossiers/getaegis-aegis.md`, `dossiers/hypercerts-lexicon.md` (accrual), `architecture/decisions.md`, `architecture/reference-architectures.md`, `architecture/acceptance-backlog.md`, `architecture/governance-checklists.md`, `architecture/risk-register.md`, `scoring/sensitivity-output.md`, `scoring/sensitivity.py`.
- Line numbers below refer to ARTICLE.md unless another file is named.

Severity scale: BLOCKER = the article states something false, or the deliverable fails a master-prompt requirement; MAJOR = a reader would be misled or a decision rests on it; MINOR = wording, clarity, consistency.

(Objections follow; blockers first.)

## Blockers

### 1. BLOCKER - Section 12 does not contain four of the five experiments the master prompt names

- **Where:** section 12, line 500: "Five experiments." The five are PoC 1 (Windows junction test), PoC 2 (echo), PoC 3 (tuf-js conformance), PoC 4 (declared attribution), PoC 5 (witnessed ledger).
- **Problem:** master prompt 8.5 item 12 requires "a hostile-component isolation test, a delegated-grant revocation test, a crash/restart test with an uncertain side effect, a consent-bounded OS-to-DAO attestation test and a contribution-fraud and appeal simulation". The article has no grant-revocation experiment (Biscuit revoke on an open SSE stream), no crash/restart experiment (effect journal, `indeterminate`), no consent-bounded attestation experiment (child-planted provenance refused, no export without `approvalRef`), and no appeal at all (PoC 4 measures reviewer detection only). The only isolation test is Windows-only (PoC 1); nothing tests a hostile add-on against srt on Linux or macOS. The evidence base already has the right mapping: `architecture/acceptance-backlog.md:64-72` ("Mapping to the master prompt's proof-of-concept portfolio"), with B-d, B-d2, X5-c (revocation), O-F1..F9, D-A7 (crash), I-a..k and X4-a (attestation), Hc-1..8 and G-F1..F12 (fraud and appeal), each with a falsifier. The article replaced that mapping with the user's ranked execution list (D4.0), which answers a different question ("which runs change a recorded verdict").
- **Fix:** restructure section 12 as the five named experiments from `acceptance-backlog.md` section 5, each with hypothesis, setup, measurement, falsifier and action; keep PoC 1-3 as "ranked confirmation tests" in a short sub-list. Replacement opening: "Five experiments, one per class the master prompt names (hostile component, grant revocation, crash with an uncertain side effect, consent-bounded attestation, contribution fraud and appeal). The user's ranked confirmation tests (Convira A10, the echo test, tuf-conformance v2.5.0) follow as section 12.6."

### 2. BLOCKER - The developer backlog lacks six of the fields the master prompt requires per issue

- **Where:** section 11, line 466: table columns "Id | Issue | Property (threat) | Files | Test | Size".
- **Problem:** master prompt 8.5 item 11 requires, per issue, "title, scope, repository and module, upstream project and version, dependencies, size (S/M/L with assumptions), skill level, acceptance tests, security constraints and definition of done". Missing for all 25 rows: upstream project and version (for example BL-09 should name `@biscuit-auth/biscuit-wasm` 0.6.0 at `80cceed`), dependencies (BL-03 depends on BL-01 and BL-07; BL-04 on BL-01 and BL-05; none is stated), size assumptions (only a global S/M/L legend), skill level (only "first contribution" on five rows), security constraints (for example BL-07 "reject mask entries, never `tlsTerminate`"; BL-12 "never execute `[RESONANT DERIVATION]`"), and a definition of done distinct from the test. The repository is implicit: `2.0.0-alpha` is never named in the table, and BL-22 and BL-24 belong to a DAO repository that does not exist yet.
- **Fix:** render the backlog as 25 short issue cards (or a wide table in the appendix) with all ten fields; the material exists in the dossiers' sections 7 and 11 and in `acceptance-backlog.md` section 4.

### 3. BLOCKER - The "Next 10 Engineering Moves" table lacks four required columns

- **Where:** lines 570-581: columns "# | Move | Property gained | Depends on | Backlog | Size".
- **Problem:** master prompt 8.5 requires "action, target repository and module, reusable external codebase or pattern, estimated effort, dependencies, principal risk, testable definition of done and likely benefit". Missing: target repository and module (only a backlog id), reusable external codebase or pattern (move 3 should name sandbox-runtime 0.0.81 and the Aegis broker pattern), principal risk (move 5: "same-user synthetic input drives the native dialog"), and a testable definition of done.
- **Fix:** add the four columns. Example, move 2: Target `2.0.0-alpha` `browser-first/host/security-state-store.mjs` and `delegation-isolation.mjs`; Reuse: the existing atomic writer `harness-registry-store.mjs:23-70` and a pinned keyring binding; Risk: the credential store is readable by every same-user process, so only level (a); Done when: X1-a and X1-c pass on the Linux lane and a new Windows lane.

### 4. BLOCKER - No discovery chain starts from a non-English source, and the count is inconsistent

- **Where:** APPENDIX section I heading "Three complete discovery chains" (line 179) followed by four chains; Chain 1 labelled "(non-English start)", Chain 2 "(non-English route to an English project)"; ARTICLE line 566: "three discovery chains, one through a non-English source"; `state.md` D5.4: "four discovery chains with two non-English starts".
- **Evidence:** the Chain 1 HAL row has `"search_language": "en"`, query `.../search/?q=Belenios` (a proper noun) and `"project_doc_language": "en"` (`ledger/discovery-s2-lang-fr.jsonl` line 26); the gitlab row (line 25) is `fr` only by agent label and again queries "Belenios". Chain 2's Helmholtz rows are `search_language` `en` with the query `brand_name.ilike.*agent*` (`ledger/discovery-s2-lang-de.jsonl`, Terok rows), and the appendix itself calls the Helmholtz index "English-only" (APPENDIX line 85). Master prompt 8.6 asks for a chain "that starts from a non-English source". A genuine one is in the ledger: the French query "sandboxer agents IA bubblewrap Landlock agents de code confinement" on linuxfr.org -> LinuxFr news "J'ai mis un proxy entre claude et Internet" (page language fr) -> `GreyhavenHQ/greywall` and `GreyhavenHQ/greyproxy` -> `docs/credential-protection.md` (`ledger/discovery-s2-lang-fr.jsonl`, Greyproxy and Greywall rows).
- **Fix:** relabel Chain 1 "French-language agent, English source" (or drop it); add the LinuxFr -> Greywall/Greyproxy -> release -> tests chain as the non-English start; make the heading, ARTICLE section 14 and `state.md` agree on the count.

### 5. BLOCKER - The tuf-js conformance claims are wrong in three places, and PoC 3 would declare its own expected result a falsification

- **Where:** line 12: "107 of 108 conformance tests pass, with one spec deviation guarded by a no-network fetcher"; line 105: "tuf-js passes the TUF conformance suite"; PoC 3, lines 520-524: "passes the TUF conformance suite v2.5.0 except the one known deviation ... Measurement: pass count out of 108 ... Falsified if: more than one test fails"; APPENDIX A.2 line 32: "6.0.0; conformance suite v2.5.0".
- **Evidence:** `dossiers/tuf-js.md:52-54`: the 108 are tuf-conformance **v2.4.0**, and the one non-passing case is the declared expected failure `test_artifact_cache` (an optional cache test), not the forceCache deviation; `:59-60`: "What conformance does not exercise: `forceCache`"; `:63`: v2.5.0 adds ML-DSA keys, more key types and path cases, so its total is not 108; `:266-270`: the diamond-delegation cache flaw is expected to fail the v2.5.0 test; `architecture/acceptance-backlog.md:11` (ranked test 3): expected result "the diamond-delegation test fails ... every other case passes as at v2.4.0", verdict change "no score change either way".
- **Consequence:** (a) the executive summary tells the reader the one failing test is the deviation the wrapper guards, which is false; (b) PoC 3 counts against the wrong total and, because the predicted outcome is the xfail plus the diamond failure, "more than one test fails" fires on the predicted result; (c) line 500 says ranked tests 1-3 "change recorded verdicts", while the backlog says test 3 changes none; (d) the appendix records a suite version that was never run.
- **Fix:** line 12: "107 of 108 tuf-conformance v2.4.0 tests pass in upstream CI (one optional cache test is an expected failure); conformance does not exercise the offline `forceCache` path, whose root-rotation deviation the wrapper guards with a no-network fetcher." PoC 3 hypothesis: "At v2.5.0 every test passes except the expected `test_artifact_cache` and, as predicted from `updater.ts:318-320`, the diamond-delegation test; separately, a wrapper unit test shows root rotation is never skipped offline." Falsified if: "any other test fails, or the wrapper accepts stale root metadata offline." APPENDIX A.2: "6.0.0; conformance v2.4.0 (upstream CI run 39558085285)".

### 6. BLOCKER - The witness residual is stated wrongly (one colluding witness suffices, not two), and PoC 5 tests an attack that cannot succeed anyway

- **Where:** 9.4, line 421: "The outside witnesses are three volunteers; if two collude with the log host, the ledger can fork." PoC 5, lines 536-539: "rejects a forked checkpoint presented to one witness ... Measurement: whether the fork gets two cosignatures".
- **Evidence:** `dossiers/transparency-dev-tessera.md:163`: "any two sets that satisfy `outside 2` share at least one outside witness, so a split view needs that witness to collude"; `:212`: the policy "needs one outside witness to collude before a split view is possible"; `:107`: split-view resistance holds only if "a witness in that intersection is honest". With 2-of-3, fork A cosigned by {EA, EB} and fork B by {EB, EC} needs only EB dishonest. Conversely, a fork shown to one honest witness can never collect two cosignatures, so PoC 5's measurement cannot fail. The dossier's own acceptance design (`:254-267`, case 5: "the gossip check, fed both forks, must alarm") is the meaningful test.
- **Fix:** line 421: "If one of the three outside witnesses colludes with the log host, two disjoint groups of members can be shown different forks, each with two valid cosignatures; only the members' gossip check across witnesses detects it." PoC 5: make one witness malicious (it cosigns both forks), serve fork A to members M1-M10 with {EA, EB} and fork B to M11-M20 with {EB, EC}; falsified if the gossip check in `tlog-verify.mjs` does not alarm within one epoch, or the omitted entry's receipt holder cannot prove omission.

### 7. BLOCKER - The security-state store is said to "detect" same-user tamper; the decision record says no local design does

- **Where:** 7.1, line 214: "on one OS account this is tamper evidence against anyone who is not the same user and against confined children; against another same-user process it detects and cannot prevent, until the core runs under its own account (A2)."
- **Evidence:** `architecture/decisions.md:42`: the MAC key is in the OS credential store and "the item is readable by any process of the same user ... This gives level (a), not (b)"; `:43`: "An attacker who can also rewrite the credential-store item defeats this"; `:45`: "On one OS account, no local design detects a same-user attacker who can read the key"; `acceptance-backlog.md` X1-b: a restore of `security/` plus the credential item is "not detected on one account". `dossiers/getaegis-aegis.md:157`: on Windows any same-user process can `CredRead` the item, and an agent "with a shell, which is what Hermes, OpenCode and DSH are" defeats it. (`decisions.md:40` says "detects tamper and rollback but cannot prevent it"; that sentence contradicts `:45`, and the article copied it.)
- **Consequence:** on Windows (unconfined by default) and on Linux or macOS whenever the srt flag is off, every delegated child is a same-user process; the store then gives no detection against the adversary it was built for (T21 by V3).
- **Fix:** "On one OS account this is tamper evidence against other accounts, offline disk changes and confined children (level (a)). A same-user process, which includes every unconfined delegated child (the Windows default today), can read the key from the credential store and rewrite records and head undetected (level (b) is not met). Only the separate-account core of A2, or a user-held external checkpoint (`exportHead()`), closes this." Correct `decisions.md:40` the same way.

## Majors

### 8. MAJOR - The first recommended move makes agent self-promotion into the trusted wiki possible before any host approval exists

- **Where:** Next 10 move 1, line 572: "Correct the status documents and fix promotion | honest surface; the first human-reviewable route works | nothing"; BL-06 marked **first contribution** (line 473); 10.1 Now (line 432); OI-2 wording (line 560): "BL-06 is a two-day fix".
- **Evidence:** `stage1/capability-matrix.md:34` (OSC-24): promote "always throws" today, so the path is dead; `:57` (OSC-47): "archive gate no-op (`archive-review-policy.mjs:27-31`); no route requires an approval proof"; ARTICLE 9.2 line 393 itself: "`actorType:"human"` client-asserted (`archive-review-policy.mjs:18-36`)". Any holder of the `archive-write` token (the service worker holds all 26, OSC-02; children reach `archive-write` routes through the bridge, `security-engineer.md:221`) could promote into `AI_MEMORY/wiki` once BL-06 lands. The article's own sequencing in 8.10 step 3 (line 361) ships "the promotion fix (8.7)" together with the helper, ledger and gate; `reference-architectures.md:300` does the same. Move 1, BL-06 and OI-2 contradict that.
- **Fix:** move 1 becomes "Correct the status documents" only; BL-06 gains "Depends on: BL-04, BL-05 (promotion must stay refused without an X-4 record)", loses the first-contribution mark (replace with BL-02 or a docs-only item), and its test adds "promote with `archive-write` and `actorType:'human'` but no approval record returns 428". OI-2 wording: "...A service-level test would catch this; we suggest fixing it only together with a host-side approval check, because once promote executes, the client-asserted `actorType` is the only gate."

### 9. MAJOR - On Windows today every delegated child is a same-user process, so X-1, X-4 and X-5 protect against far less than the article implies; Phase 1 fails the threat model's own requirement

- **Where:** 7.1 X-4 (line 216) and 9.1 (line 376): "Residual: the helper runs as the same user; an attacker with same-user code execution can drive the dialog"; 9.4 (line 421): "Same-user code execution defeats the local design until A2's separate account".
- **Evidence:** `architecture/decisions.md:14` X-4 residual: "Synthetic input by V2 or an unconfined V3"; `:70`: Phase 1 dialogs are PowerShell WinForms, `osascript`, `zenity`, with "no resistance to synthetic input from a same-user process"; `decisions.md:100`: unconfined is "the Windows default today"; `ledger/threat-model-draft.md:85`: "Phase 1 needs (b) for anything that gates T1 or T22"; `decisions.md:45`: "routes that gate T1 or T22 rely on R02 containment for V3 and declare V2 on the same machine out of scope". `dossiers/getaegis-aegis.md:157`: a broker "protects keys from an agent that only speaks HTTP, not from an agent with a shell, which is what Hermes, OpenCode and DSH are".
- **Problem:** the article phrases the residual as an outside "attacker with same-user code execution". On Windows (all users, by default) and on Linux or macOS with the srt flag off, the delegated LLM agents themselves are that attacker: they can click the approval dialog, read the credential-store key, and read the bridge's and broker's memory and environment. The selected Phase 1 therefore does not meet the threat model's stated Phase 1 property for T1 and T22, and the scope was narrowed (V2 declared out of scope) without the article saying so.
- **Fix:** add to 9.4: "On Windows, where children run unconfined by default, the approval helper, the store and the broker give no protection against a hostile delegated agent: it runs as the user and can drive the dialog, read the store key and read the broker's memory. Phase 1 therefore does not meet the threat model's requirement of level (b) for routes that gate T1 and T22; the decision records narrow the attacker model to confined children until A2. Until then, the delegation UI on Windows should say 'unconfined: this agent can approve its own actions'." Add the same sentence to section 1's weakest evidence.

### 10. MAJOR - A passing Windows confinement test would not make LLM delegation confined: AppContainer children cannot reach the broker

- **Where:** PoC 1 "On pass" (line 508): "BL-19 enters Next; the Windows story becomes 'confined'"; 10.3 (line 449); 9.3 item 1 (line 413).
- **Evidence:** `architecture/decisions.md:122`: "AppContainer can never be granted loopback ... and a network-enabled AppContainer child gets Internet plus LAN with no proxy, so under Convira a child either cannot reach any provider or holds the key itself ... Convira stays the no-admin Windows option for tasks that need no network"; `dossiers/convira-sandbox.md:306-318`: "A loopback HTTP credential broker on the bridge ... is unreachable from a Windows AppContainer child"; `acceptance-backlog.md:9`: "the X-5 Windows transport stays srt-win either way".
- **Fix:** PoC 1 "On pass": "Convira becomes the Windows confinement for network-free tasks; delegations that call a provider (Hermes, OpenCode, Goose) stay on srt-win (opt-in, elevated install, labelled bypassable) or unconfined until a pipe transport exists." Repeat in 10.3 and 9.3 item 1.

### 11. MAJOR - "Keys never enter child environments" is not achieved by the blueprint, and on unconfined OSes the key is readable anyway

- **Where:** 8.10 step 2 (line 360): "removes keys from child environments on every OS"; Next 10 move 3 (line 574): "keys never enter child environments"; 10.1 (line 434): "keys absent from child env in the inverted tests"; 9.1 residual (line 377) names only compressed or base64-nested echoes.
- **Evidence:** `stage1/os-map.md:198`: "`opencode serve` is spawned with full `process.env` and no sandbox (`run-bridge-minimal.mjs:232`, `opencode-client.mjs:281-285`)"; `os-map.md:166`: keys can come from the bridge's own environment (`OPENAI_API_KEY`, `MINIMAX_API_KEY`, `ZAI_API_KEY`); 8.2 changes only `addon-delegation-service.mjs:1770-1782`, the OpenCode CLI env and "`dsh-runtime.mjs:27` later"; `risk-register.md:49` (RR-12): DSH and `opencode serve` "stay unconfined"; `risk-register.md:39` (RR-02) residual: "Unconfined Windows: token-only barrier; a local process with the token can spend the key"; `security-engineer.md:95`: env values are readable by same-uid processes via `/proc/<pid>/environ`.
- **Fix:** 8.10 step 2: "removes provider keys from Hermes and OpenCode CLI environments; `opencode serve` and DSH keep inheriting the bridge environment until RR-12 is closed, and on unconfined OSes a child can still read keys from the bridge's or broker's process." Add to BL-03's files `run-bridge-minimal.mjs:232` and `opencode-client.mjs:281-285` (strip key variables from the spawned env), or state the exception in the move.

### 12. MAJOR - Data exfiltration by a confined child through the broker's allowlist is not named anywhere

- **Where:** 9.4 (line 421): "A compromised provider learns everything the user sends it; the broker protects the key, not the prompt."
- **Evidence:** `architecture/decisions.md:102`: any `CONNECT` or absolute-URI target "is checked against the bridge-chosen domain allowlist"; 8.2 (line 327): "`CONNECT` only to allowlisted hosts". `risk-register.md:10` covers "T2 key exfiltration" only; no row covers workspace exfiltration.
- **Problem:** a hostile child does not need the user's key or a compromised provider. With `CONNECT` to an allowlisted provider host it can upload the user's workspace to the attacker's own account at that provider using the attacker's key, or to any other allowlisted host (code hosts, package registries). This is the main post-containment exfiltration route for agent sandboxes and it is absent from 9.2 and 9.4.
- **Fix:** add a 9.2 row: "Containment | a confined child exfiltrates data to an allowlisted host under its own credentials | any allowlist | per-delegation allowlist limited to the virtual host by default; `CONNECT` only when the task needs it; per-call audit with byte counts (broker) | X-5". Add to 9.4: "Containment limits where data can go, not what an allowed destination receives."

### 13. MAJOR - "Loopback no longer an open surface" overstates what Origin and Host checks do

- **Where:** Next 10 move 4 (line 575): "loopback no longer an open surface (T6)"; BL-08 (line 475): "one exempt prefix"; 9.1 (line 378).
- **Problem:** after BL-08 one prefix still needs no token, and Origin and Host rejection stops web pages and DNS rebinding (V1), not local processes, which set any Host header and send no Origin. Unconfined children (the Windows default) and other local processes still reach the exempt prefix.
- **Fix:** move 4 property: "web pages and DNS rebinding can no longer reach the bridge (V1); one token-free prefix stays reachable by local processes until the Hermes iframe takes a token (A2 seam 2)."

### 14. MAJOR - Biscuit "dual mode" keeps all 26 static tokens valid, so OSC-02 is not countered, and no milestone retires them

- **Where:** 9.2 row 1 (line 385): "one holder keeps every capability ... OSC-02 | Biscuit grants per principal with TTL"; Next 10 move 6 (line 577): "per-principal, expiring, attenuable authority"; 8.4 (line 335): "the extension's `bridge-client.js:646-656` keeps working unchanged".
- **Problem:** in dual mode the service worker still holds every static capability token for the process lifetime; per-principal grants exist beside it, not instead of it. `reference-architectures.md:24` and `:172` keep the grants "dual mode with the static tokens"; neither that file nor the article schedules retiring them.
- **Fix:** move 6 property: "per-principal, expiring grants for new principals (children, add-ons); the extension's static tokens remain until they are retired"; add a backlog item and a 6-12 month roadmap entry "retire static capability tokens; extension requests Biscuit grants at startup".

### 15. MAJOR - The executive conclusion over-claims about the four "missing properties" and is unfair to the Alpha

- **Where:** line 7: "it lacks every property its own website promises about isolation, revocation and 'coming back whole' ... none of the four properties that matter most: ... a rollback of the desktop service to a hashed known-good baseline, and per-right personhood assurance. Those four are small to build, and they are where the research found the design errors that would have undone everything else."
- **Evidence:** personhood (R25) was not inspected (line 32; `dao-skeptic.md` C-7; D4.0 (2)), and 9.4 (line 421) says it "remains a policy question with no technical answer in this research", so it is neither "small to build" nor a place where design errors were found. The hashed-baseline supervisor sits in 6-12 months (`reference-architectures.md:303`), not "small". The website's promises describe the baseplate, which the article itself calls a different generation "designed on paper" (line 80); the Alpha does have macOS `sandbox-exec`, an OpenCode revoke latch (line 58) and a graceful drain (`capability-matrix.md:52`, OSC-42 is class C).
- **Fix:** "The Alpha is a working single-user Chrome extension plus a loopback Node bridge ... The isolation, revocation and recovery properties the website describes belong to the baseplate design, which has no code yet; the Alpha has partial forms (macOS-only isolation, an OpenCode revoke latch, a graceful shutdown). The open-source world supplies most building blocks, but not three properties: a privileged route that refuses to run without a human's approval record, a host-verifiable review of knowledge promotion, and supervised rollback to a hashed baseline. The first two are small to build and are where the research found the design errors that would have undone the rest; the third is a 6-12 month item. Per-right personhood assurance is a fourth gap that this research did not inspect."

### 16. MAJOR - Failure analysis has no privacy family and no Sybil-resistance analysis, and the DAO pilot is scheduled before either is addressed

- **Where:** 9.2 (lines 383-409) families: Authorization ... Minimal architecture; no Privacy and no Sybil row. 9.4 one sentence on personhood. 10.3 (line 451): "DAO Phase 1 pilot ... twenty members".
- **Evidence:** master prompt 8.5 item 9: "security, privacy, economic and governance, including ... Sybil resistance, flawed reputation proxies and risky token complexity". The evidence base has the privacy material: status-list fetches reveal verification (6.3 line 200), permanent public vote and revocation records (`realms-spl-governance.md:217`; `dao-skeptic.md` TM-9 "no revocation reason on-chain"), per-epoch keys versus auditability (D4.0 (3)(b), DR-32), `chrome.storage.local` plaintext (os-map line 208). For Sybil: I-17 "no per-sponsor agent cap" (line 88), R25 and R27 uninspected, `reference-architectures.md:303` schedules "R25 and R27 inspections" in the same 6-12 month window as the pilot; the article schedules the pilot earlier (months 4-6) and drops the inspections.
- **Fix:** add a "Privacy" family (status-fetch correlation, public revocation stigma, per-epoch unlinkability, local plaintext stores) and a "Sybil and personhood" family (one person registering many members, sponsor-farmed AI members, the counter-measure placement: per-sponsor caps and reviewer-vouched admission in the registry, and the residual that no technical answer exists); state that the pilot admits members only by named invitation until R25 is decided.

### 17. MAJOR - The roadmap contradicts the reference-architecture milestones it claims to follow

- **Where:** 10.3 (lines 447-451) and 10.4 (lines 455-457).
- **Evidence:** `architecture/reference-architectures.md:302-303`: execution tickets for submit, pay, grant and governance classes in 90-180 days (article: 6-12 months); supervisor with hashed baseline in 6-12 months (article: months 4-6); DAO Phase 1 pilot in 6-12 months (article: months 4-6); the reference plan also schedules "DSH and OpenCode on a reverse channel", "R15 vault over the store" and "R25 and R27 inspections", none of which appears in the article's roadmap.
- **Fix:** align the article with `reference-architectures.md` section 6 (or update that file and record the change in `state.md`), and add the three missing items to 10.4.

### 18. MAJOR - Backlog sizes contradict the integration costs in section 6.3

- **Where:** section 11 legend (line 464): "M under 2 weeks"; BL-03 and BL-07 M, BL-12 M, BL-15 M, BL-24 M; Next 10 move 9 M.
- **Evidence:** 6.3 (lines 193-205): sandbox-runtime "2-3 weeks plus the broker process"; DataLad "pattern: 3-4 weeks for the Node ledger"; nanobrowser "2-4 weeks port"; Tessera "3-5 weeks for the DAO service"; `dossiers/transparency-dev-tessera.md:243`: 3-5 weeks for the first deployment.
- **Fix:** BL-03 plus BL-07 L (or split), BL-12 L, BL-15 L, BL-24 L, move 9 L; state each size's assumptions (master prompt item 11).

### 19. MAJOR - Phase 1 "no token" is asserted while the ledger records accruals and payment decisions whose future value is unstated

- **Where:** 1 (line 28): "no token until an audit ..."; 7.4 (line 265); 8.9 (line 355): lexicon types "claim, proposal, review, accrual, paymentDecision, appeal, correction, revocation, dimension".
- **Evidence:** `stage1/dao-requirements.md` DR-22 (accrual and payment as separate events of a `$RES` economy) and DR-54 ("Assets earned on test networks migrate only under published, anti-abuse-reviewed rules"); `reference-architectures.md:204`.
- **Problem:** if Phase 1 accruals are later convertible into `$RES`, the witnessed ledger is an off-chain token balance from day one, with the farming, Sybil and securities questions of a token but none of its audit gate. If they are not convertible, members are told nothing about what they accrue. The article does not say which.
- **Fix:** add to 7.4: "Phase 1 accruals are records of reviewed contribution with no promised conversion; any later conversion is a Phase 2 decision under DR-54's migration rule, published before the pilot opens. `paymentDecision` records in Phase 1 refer only to payments made outside the ledger (grants, bounties) by named people."

### 20. MAJOR - The add-on registry is drawn as DAO infrastructure, which puts a DAO-run revocation over OS add-ons

- **Where:** diagram 2, lines 287, 296, 300 (`D_REG` inside "DAO infrastructure"; "WAL -. publish release .-> D_REG"); 7.4 (line 265): the TUF registry listed among DAO Phase 1 components.
- **Evidence:** `architecture/governance-checklists.md:29-35` places TUF root, targets and `certified` under "Project-level off-chain trust roots (shared by A1, A2 and A3)", held on hardware keys; 8.5 (line 339): "Publisher side: tuf-on-ci with hardware keys"; `dao-skeptic.md` TM-7: certification revocation is "DAO state removing capability without a user act"; `stage1/interaction.md:76` (I2): certification "can inform display and policy defaults but never mint capability tokens". Security revocations suspend at once (D4.0 (3)(a)).
- **Fix:** move `D_REG` into a third subgraph "Project trust roots (maintainers and named keyholders)"; replace the wallet arrow with "hardware keys -> sign targets"; add to 7.4: "The DAO may set certification policy and propose reviewers (E4); the keys belong to the project, and the OS trusts keys, not DAO state (I2). A security revocation suspends with notice and override; this is a deliberate trade against TM-7."

### 21. MAJOR - The invariants are presented as the project's contracts, but most are the research's own proposals

- **Where:** section 2 (line 36): "The project's own documents state the contracts; the research turns them into testable form"; line 40: "Invariants (I1-I10, `stage1/interaction.md` section 6, adopted at Gate 1)"; anti-goals G1-G5 (line 44).
- **Evidence:** `stage1/gate1-report.md:53`: "`stage1/interaction.md` defines ... ten invariants"; `gate1-report.md:37`: "No ratified next-generation document exists"; `interaction.md:165`: the official DAO text ("The software logs every member action") conflicts with I3, and the research "keeps I3". G1-G5 are the research's hard gates (`gate2-report.md` section 3). Master prompt section 9: "Do not convert community philosophy into a technical restriction the official project has not adopted."
- **Fix:** add a source column or tag per invariant: official (ADR-038, ADR-008, the roadmap quote, #240), derived from official text, or proposed by this research; replace "adopted at Gate 1" with "adopted by the research owner at Gate 1 as working assumptions; the maintainers have not adopted them". Say the same for G1-G5.

### 22. MAJOR - Section 7's "alternatives" are stages of one path; no rewrite and no DAO alternative is assessed

- **Where:** 7.2-7.6. A2 "Reached from A1 along the four seams" (line 261); A3 is the DAO (line 265); A4 rejected (line 309); a Rust or Chromium rewrite is dismissed in one clause (line 313).
- **Problem:** master prompt 8.5 item 7 asks for three or more alternatives with diagrams and a justified selection. The selected path is A1 then A2 plus A3, i.e. every alternative except A4; there is no competing DAO architecture (for example on-chain first with a DAO-owned Realms and Squads, or a legal cooperative using Loomio or Belenios with no ledger), and the only diagrams are one OS before-and-after and one OS/DAO flow. A reader cannot see what was traded away.
- **Fix:** present OS alternatives as A1-only, A1-then-A2 (selected), rewrite (ADR-037), Goose layer (A4); present DAO alternatives as off-chain ledger (selected), on-chain first, and no-ledger cooperative; one paragraph each with the deciding evidence.

### 23. MAJOR - Section 5 has no compact table of the longlist

- **Where:** section 5 (lines 115-146): the 16 inspected codebases, a prose list of about 40 "suitable, not shortlisted", and counterexamples.
- **Evidence:** master prompt 8.5 item 5: "a compact table for the whole longlist"; the longlist is 586 codebases with 185 candidates (`ledger/gate2-report.md:78`, `ledger/codebases.jsonl`).
- **Fix:** add an appendix table of the 185 candidates (codebase, requirement, disposition, one-line reason, ledger id), or at minimum a per-requirement table of candidate names; point to it from section 5.

### 24. MAJOR - Section 13 does not say who may decide each item or what evidence would settle it

- **Where:** line 545: "The research recommends; the maintainers decide." Items 1-9.
- **Evidence:** master prompt 8.5 item 13: "concise ADR proposals, contested trade-offs, who is authorised to decide, and what evidence is needed". Several items are not maintainer decisions: item 3 and 6 belong to the DAO operating team or the whitepaper authors; item 5 is a user-facing policy; Squads v4's AGPL licence needs legal review (D4.1) and is not listed; the Biscuit token-pinning contract "needs a decision" (8.4, line 335) and is not listed.
- **Fix:** give each item three lines: decider (Alpha maintainer, DAO operating team, legal reviewer, community vote), contested trade-off (for example item 5: revocation latency versus user autonomy; item 6: auditability versus DR-32 unlinkability), and evidence needed (for example item 7: PoC 1 and X5-b on Windows).

### 25. MAJOR - The appendix does not list the queries per platform

- **Where:** APPENDIX B (lines 45-93): searches counted per platform, languages, outcomes; no queries.
- **Evidence:** master prompt 8.6: "confirm in the appendix, for each platform ... the queries and languages actually used". `ledger/coverage-matrix.md` section (a) also has counts only; queries live only in the JSONL rows.
- **Fix:** add a "Representative queries" column with two or three exact queries per platform (from `search_terms_or_query` in the discovery and negative ledgers), plus the pointer to the JSONL for the full list.

### 26. MAJOR - OI-1 publicises a possible personal-data exposure and asserts details the research did not read

- **Where:** 3.6 (line 90): "`resonant-hub` commits `community.db` with 24 member rows plus Discord handles (rows not read; personal-data exposure plausible)"; 13 (line 559).
- **Evidence:** `stage1/census-notes.md:75`: "community.db (24 member rows) and demo seed data; personal-data exposure not assessed (rows not read)". "Discord handles" appears first in `state.md` D1.3, with no source showing how it was known without reading rows.
- **Problem:** an article meant for wider reading names the file and its probable content before the owner has been told privately, and the "Discord handles" detail is unsupported; the file may be demo seed data.
- **Fix:** remove the file name and row count from the article body; in 3.6 write "One repository may contain personal data; the research did not read it and has passed the detail privately to the owner (OI-1)". Keep the specifics in a private note to the research owner; in the held message say "a `community.db` file whose table names suggest member records; we did not open the rows, and they may be demo data".

### 27. MAJOR - The Realms CI and source statements omit the dossier's own caveats

- **Where:** 5.1 (line 138): "governance CI failed 31 of 31 runs"; 6.3 (line 207): "CI never green"; line 20: "it runs code with no public source".
- **Evidence:** `dossiers/realms-spl-governance.md:83`: the workflow's push trigger names `master` while the default branch is `main`; `:399`: "The CI failure cause (0 steps in 96 s) suggests a workflow or runner problem rather than failing tests [hypothesis]"; `:21`: "I found no public source for 3.1.4 to 3.1.7".
- **Fix:** "the governance workflow failed all 31 recorded runs, apparently before any step ran (a workflow or runner fault is likely; no test result exists either way)"; "runs version 3.1.7, for which no public source was found".

### 28. MAJOR - Linux confinement friction is hidden, and the article does not evaluate the friction of its protections

- **Where:** section 4 (line 97): "Linux and macOS are solved many times over"; 7.2 and 10.1 present srt on Linux as a flag flip.
- **Evidence:** `dossiers/anthropics-sandbox-runtime.md:271`: srt "Needs system packages on Linux (bwrap, socat, ripgrep, an AppArmor sysctl on Ubuntu 24.04)", i.e. an administrator step on the most common desktop distribution; `:173` user friction; `dossiers/tuf-js.md` section 8: with tuf-on-ci defaults "an offline machine goes stale within 2 days" and refuses new installs. Master prompt section 9: "Evaluate the friction these protections cause."
- **Fix:** add a short "Friction" subsection to section 9: admin step for Linux and Windows confinement, approval dialogs per delegation start, offline staleness of certification, per-item consent for claim packages, per-epoch keys; for each, who bears it and the mitigation (for example "first-run setup script with one sudo prompt; delegation UI shows 'unconfined' until done").

### 29. MAJOR - Diagram 1 draws unbuilt components as solid, and diagram 2 lets an add-on write into the bridge-only store

- **Where:** lines 237, 243, 244, 256 (`P_EXT` "ported classifier, executes ticketed actions", `P_CH` "base URL + token, confined where supported", `P_USR` "work trees only", `LLM` are not in the `proposed` class); line 279: `L_CPB -. "signed, approvalRef" .-> L_STORE`.
- **Evidence:** master prompt 8.5: "Draw any component without a verified implementation as proposed, not shipped." Execution tickets, the classifier port and token-only children do not exist (BL-15, BL-20, BL-03). X-1 (line 214): the store is "unreachable by bridge routes and confined children", and the add-on builder is an add-on.
- **Fix:** add `P_EXT,P_CH,P_USR` to the `proposed` class (or split `P_EXT` into an existing and a proposed node); route `L_CPB` through `L_BR` ("request signature") instead of writing to `L_STORE`.

## Minors

### 30. MINOR - Dossier counts in the X-1 and X-4 claims

- **Where:** line 24: "Ten of the sixteen inspection dossiers"; line 25 and line 376: "Seven dossiers had ended their approval design ...".
- **Evidence:** `reviews/security-engineer.md:221`: X-1 lists ten dossiers out of the fifteen that existed (Realms was added later, D4.1); `:224`: X-4 lists seven finding ids from six dossiers (durabletask, openworkflow, hypercore twice, datalad, goose, nanobrowser), and says they end "in a bridge route or a prompt rendered by the extension", not only in the extension context.
- **Fix:** "Ten of the fifteen OS and DAO dossiers reviewed at Gate 3"; "Six dossiers ended their approval design in a bridge route or an extension prompt the agent's own context could reach."

### 31. MINOR - The Stage 1 re-check rate is misquoted

- **Where:** line 30: "a 20 percent partial rate on a seeded re-check with zero failures".
- **Evidence:** APPENDIX G line 159: 9 PASS, 6 PARTIAL of 15, "20.0 percent (partial counts half)"; 6 of 15 is 40 percent.
- **Fix:** "6 of 15 rows partial (a 20 percent weighted error rate, partials counted as half), none failed".

### 32. MINOR - "42 platforms" has no source

- **Where:** line 93: "Stage 2 searched 42 platforms in seven languages".
- **Evidence:** `ledger/coverage-matrix.md` section (a) has 35 platform rows including `web`, `university-gitlab` and the two citation aids; APPENDIX B lists 34 rows. No file in the research base states 42.
- **Fix:** "Stage 2 searched 33 named platforms plus general web search and university GitLab instances" (or whatever count the coverage matrix supports).

### 33. MINOR - A tool name leaked into the roadmap

- **Where:** line 443: "`fewer-permission` style listener audit test on the route table".
- **Fix:** "a listener audit test over the route table (no new listener without authentication)".

### 34. MINOR - Realms is "Phase 2" in section 5 and "Phase 3" in section 7

- **Where:** line 138: "Phase 2 only as a DAO-owned instance"; line 265: "Phase 3 only if binding member votes are adopted: a DAO-owned Realms instance".
- **Evidence:** `reference-architectures.md` (A3, "Phase 2 and 3"): Phase 3 replaces the custodian multisig by a DAO-owned Realms instance; D4.1 says "Phase 2".
- **Fix:** use "Phase 3" in line 138 and footnote that D4.1's "Phase 2" predates the three-phase split.

### 35. MINOR - "Lacks entirely" includes a partial capability

- **Where:** line 76: "Capabilities the Alpha lacks entirely ... supervised crash recovery (OSC-42 to OSC-47)".
- **Evidence:** `capability-matrix.md:52`: OSC-42 is class C (SIGINT/SIGTERM drain exists); the matrix's own list of absent capabilities is "OSC-43 to OSC-47, OSC-49, OSC-50" (`:81`).
- **Fix:** "(OSC-43 to OSC-47; crash recovery, OSC-42, is partial: a graceful drain, no supervisor)".

### 36. MINOR - Several matrix cells are more generous than the dossiers

- **Where:** 6.1, lines 164, 167, 168.
- **Evidence:** durabletask "Ledger tamper detected (a): U (library)" while 5.1 (line 127) says "tail truncation not" detected and the library "is not wired to the SQLite backend" -> P. tuf-js "Signature and hash verified offline ...: U (repo, mirror)" while `dossiers/tuf-js.md:153` rates offline verification "Partly" (forceCache tested only on the happy path, root-skip untested) -> U for repository rollback, P for offline. "No new listener: U" for OpenWorkflow, SD-JWT and tuf-js records the absence of a listener, which no test "demonstrates" per the legend.
- **Fix:** durabletask P; split the tuf-js cell "U (repo and mirror rollback), P (offline), D (local cache)"; use a separate mark (for example "n/l: no listener by construction") for libraries.

### 37. MINOR - The sensitivity summary for dao_contract does not match the output file, and "pre-registered" needs its qualifier

- **Where:** line 184: "top two fragile against each other"; APPENDIX F and J: "a pre-registered sensitivity script".
- **Evidence:** `scoring/sensitivity-output.md` dao_contract: rank 1 identity-common-ts R12 "stable", ranks 2 (identity-common-ts R23) and 3 (Tessera) FRAGILE; the "top two swap" is from the what-if perturbation (`state.md` D5.2). `scoring/sensitivity.py:13`: the fragility rule was "corrected 2026-10-21 from 'more than one place', D3.6", after the DAO skeptic's C-1.
- **Fix:** "R23 and Tessera fragile against each other; the R12 lead is stable under weights but swaps with R23 under a one-point isolation move"; "pre-registered, with the fragility rule corrected once after review (D3.6)".

### 38. MINOR - ADR numbers without a basis

- **Where:** line 547: "as ADR-059 to ADR-061 in the Alpha's numbering".
- **Evidence:** the highest ADR file at `578fbbc` is ADR-038 (`git -C _untrusted/resonantos-2.0.0-alpha ls-tree -r --name-only HEAD`); the article itself says ADR-055 and ADR-056 "do not exist" (line 80).
- **Fix:** "as three new ADRs (numbers assigned by the maintainers)".

### 39. MINOR - Done-when criteria presuppose CI lanes the Alpha does not have

- **Where:** line 433: "`security-state-store.test.mjs` green on three OS lanes"; BL-01 "Windows DACL"; BL-19 "`windows-latest` lane".
- **Evidence:** `.github/workflows/alpha-build.yml:20` at `578fbbc`: `runs-on: ubuntu-latest`, the only verify lane (`stage1/sources/osmap/ci-alpha-build-39097845387-jobs.tsv`: one job).
- **Fix:** add a backlog item "add `windows-latest` and `macos-latest` legs to `alpha-build`" with dependency links from BL-01, BL-07, BL-19; or change the done-when to "green on the Linux lane; Windows and macOS cases run by hand until the lanes exist".

### 40. MINOR - Undefined labels make the executive summary and section 7 unreadable without the research files

- **Where:** section 1 uses T21, T22, T2, T7, R25, R27, X-1, X-4, X-5, C2SP, CATP and "Ed25519-only root" before any definition (lines 17-32); section 6.3 "KB skipped" (line 200); 7.1 "WYSIWYS", "level (a)"; 7.6 "the Component surface property"; 8.9 "EA EB EC"; BL-22 "A.9 field fixtures"; "srt" is never expanded; PoC 1 "Convira A10".
- **Fix:** a ten-line "How to read this" box after the title (R = requirement, T = threat, V = adversary, OSC = capability-matrix row, DR = DAO requirement, I = invariant, X = cross-cutting decision, BL = backlog item, level (a)/(b) = tamper evidence against other users / against the same user), expand srt, KB (key binding) and WYSIWYS on first use, and in section 1 replace ids with words ("security state tamper (T21)").

### 41. MINOR - Appendix inconsistencies

- **Where:** APPENDIX A.3 and J: "decision log D0.1 to D5.3" (D5.4 exists); G line 163: Stage 4 rate "see those files" (master prompt 6.5 requires the rate in the appendix); H line 177: "the CI lane claims for third-party projects beyond sandbox-runtime, which rest on workflow listings and README statements".
- **Evidence:** `dossiers/tuf-js.md:13, 54` and `dossiers/convira-sandbox.md:5` read Actions logs through the API, so H understates the CI evidence for those two and overstates it for the rest.
- **Fix:** "D0.1 to D5.4" (or the final id); fill the Stage 4 row with the checkers' counts before handover; H: "CI claims rest on Actions logs for sandbox-runtime, tuf-js and Convira, and on workflow listings or READMEs for the others".

### 42. MINOR - The vendor disclosure belongs next to the recommendation

- **Where:** APPENDIX I Chain 4 (line 187): "Anthropic also makes the models that ran this research"; the top reuse recommendation is `@anthropic-ai/sandbox-runtime` (line 11) and the highest os_kernel score (line 182).
- **Fix:** add one sentence to section 1 and to the srt row in 5.1: "Disclosure: the models that ran this research are made by the same company as sandbox-runtime; the dossier's blocker against its masking mode stands."

### 43. MINOR - PoC 4 cannot falsify at the stated sample size, and PoC 1 omits the child-planted junction

- **Where:** PoC 4 (lines 529-531): twenty packages, half wrong, thresholds 70 and 20 percent; PoC 1 (line 505): a pre-existing junction in the grant.
- **Evidence:** with ten wrong packages, 70 percent means 7 of 10, so one reviewer decision moves the verdict; `acceptance-backlog.md:9` (A10): the junction is planted by the confined child in a first spawn, then by an unconfined same-user process, plus a symlink and a deny-leaf variant.
- **Fix:** PoC 4: at least 100 packages and a stated confidence interval, or call it a pilot that cannot falsify. PoC 1: use the A10 variants verbatim, starting with the child-planted junction.

### 44. MINOR - DAO verifiers add an untrusted parser to the bridge process and are not stated as off by default

- **Where:** 8.9 (line 355): "Bridge side: `host/dao-authority-verifier.mjs` and `host/dao-credential-verifier.mjs` decoding `GovernanceV2` ... from two RPC endpoints".
- **Evidence:** threat model section 4 Component surface: "parsers of child or page input run outside the process holding A1 and A2"; `security-engineer.md` TM-9: the RPC operator is an adversary (V9); `interaction.md:75` (I1): every DAO-facing module is "an optional add-on or a disabled-by-default bridge service".
- **Fix:** "Both verifiers run in a separate low-privilege child of the bridge, are disabled by default, and contact RPC endpoints only when the user opens `/dao audit`."

### 45. MINOR - The OS ledger's "witness or anchor (DAO)" reads as an OS-to-DAO flow

- **Where:** 9.2 line 394: "signed head in the store; later a witness or anchor (core; DAO) | X-1; A3 witness".
- **Evidence:** `architecture/decisions.md:45`: the external checkpoint is a user-kept export, "off by default, I1 and I3"; I10: "neither trail is the other's source of truth".
- **Fix:** "later a user-chosen external checkpoint (export, second device or a witness the user picks; off by default)".

### 46. MINOR - Minor wording on the devnet artifacts and attribution

- **Where:** line 550: "Burn and close the `$RES` mint authority and the sector mints"; line 415: "Anyone reading the chain learns a different DAO than the whitepaper describes"; line 15: "the attribution they carry has no source yet".
- **Evidence:** a mint authority is set to none, not burned; devnet is a test network where over-supply is normal; `dao-skeptic.md` C-6: "The article should not describe R12 candidates as carrying attribution."
- **Fix:** "Set the mint authorities of `$RES` and the sector mints to none and the program's upgrade authority to none, or label them on the DAO site as superseded test artifacts"; "Readers of devnet see an earlier test model, not the current design"; "the format can carry a declared attribution field; nothing produces the value yet".

## What held up

Checked and found consistent with the evidence base, so not objected to: the capability-matrix counts (A 9, B 22, C 14, D 12, E 3, F 1, G 2; `capability-matrix.md:77`); the Stage 3 citation figures (165 archaeologist plus 24 R24 = 189; 181 PASS, 7 PARTIAL, 1 FAIL; `gate3-report.md:10`, D4.1); the codebase totals (586 = 185 + 279 + 104 + 18); the platform list (every 4.1 and 4.2 platform appears in APPENDIX B); the Convira CI cells of 6.1 (`convira-sandbox.md:228-232`); the X-1 and X-4 decisions being user-approved (D5.3); the honest labelling of nothing executed (D4.0); the Realms authority facts (5-of-7, hold-up 0, community veto disabled; `realms-spl-governance.md:34, 194`); the R24 decision (off-chain Phase 1, DAO-owned instance only later).

## Counts

| Severity | Count | Objections |
|---|---|---|
| BLOCKER | 7 | 1-7 |
| MAJOR | 22 | 8-29 |
| MINOR | 17 | 30-46 |
| Total | 46 | |

## Verdict

The article cannot go to the owner as it stands. The prose is careful and most numbers trace to the research base, but four master-prompt items fail outright (section 12's named experiments, the backlog fields, the Next 10 columns, a non-English discovery chain), three statements are false in a way that changes how safe the design looks (the tuf-js conformance claim, the witness collusion threshold, the store "detecting" same-user tamper), and the first recommended move would open a self-promotion path into the trusted wiki.

The three changes that matter most:

1. **Fix the security story for the adversary that actually exists today (objections 7, 8, 9, 10, 11).** State plainly that on Windows, and anywhere srt is off, every delegated agent is a same-user process that can drive the approval dialog, read the store key and read provider keys, so Phase 1 does not meet the threat model's level (b) requirement; re-sequence BL-06 behind the approval gate; correct "keys never enter child environments" and the Convira "confined" outcome.
2. **Rebuild sections 11, 12 and the Next 10 table to the master prompt's fields (objections 1, 2, 3).** The material already exists in `architecture/acceptance-backlog.md` sections 4-5 and the dossiers' sections 7 and 11; this is restructuring, not new research.
3. **Correct the false statements and the appendix chain (objections 4, 5, 6).** tuf-js: 107/108 is v2.4.0 and the failure is an optional cache test; PoC 3 must expect the diamond failure. Witnesses: one colluding witness suffices; PoC 5 must test it. Add the LinuxFr -> Greywall/Greyproxy chain as the non-English start.

STATUS: COMPLETE
