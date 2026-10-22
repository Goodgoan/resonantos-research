## 9. Failure analysis

The threat model names 24 threats (T1-T24) across ten adversaries (V1-V10) and eleven assets. The register (`architecture/risk-register.md`, RR-01 to RR-30) places each guardrail in the core, the adapter, user confirmation, an off-chain reviewer or an on-chain contract. This section gives the failures that decide the design, with the dependency they rest on and the counter-measure's placement.

### 9.1 Where the designs would have failed, and what changed

Five findings from the Stage 3 adversarial review (`reviews/gate3-report.md`) are the ones a reader should remember, because each recurred across independent dossiers:

- **Security state in the user folder (X-1).** Ten security-state placements across nine of the fifteen dossiers the security review read put revocation sets, keys, watermarks, ledgers or job state under the user folder, the agent's own configuration directory or the harness state root, reachable by the `archive-write` family and by unconfined children. A single Guardian or child write then rolled revocation back. Countered in the core by the store (8.1) and in every adapter by the deny root. Residual: any same-user process, including every unconfined delegated child, can read the store's key and rewrite it undetected until A2's separate account (level (b) not met).
- **Approval in the agent's own context (X-4).** Seven approval designs in six dossiers ended in a bridge route or an extension prompt that the planner's own context could call with a token it already holds. Countered by the helper process with no route. Residual: the helper runs as the same user; an unconfined delegated agent, which is every delegated agent on Windows today, can drive the dialog with synthetic input, which is the (b) limit of the whole local design.
- **Keys reach the child (T2).** Provider keys are in Hermes (`addon-delegation-service.mjs:1770-1780`) and OpenCode (`:2221-2248, 2331`) environments today, and sandbox-runtime's masking would have returned them through echoing or error-reflecting upstreams. Countered by the broker (8.2) at the containment boundary. Residual: a provider that reflects the key inside a compressed or base64-nested body beyond the redactor's encoders; ranked test 2 measures this.
- **Loopback is the attack surface, not the internet (T3, T6).** Seven proxy prefixes need no token; sandbox-exec allows loopback; Convira's Linux adapter ignores `allowLoopback:false`; Aegis and durabletask-go open unauthenticated listeners; the MCP SDK ships with host validation off. Countered by the srt adapter's proxy-port-only allow, the broker's own port, and the R05 rule (Origin and Host rejection, which stops web pages and DNS rebinding, plus one exempt prefix that local processes can still reach until the Hermes iframe takes a token). Residual: Windows unconfined by default.
- **Rollback beats revocation (T6, T21).** No candidate kept a watermark the revoked party could not reset; hypercore keeps the signing key in the data store; sigstore-js has no rollback concept. Countered by the TUF watermark and revoked set in the store, with a second copy in the harness registry record. Residual: a restored full OS snapshot predating the revocation, which only a remote status check (hourly recheck) catches.

### 9.2 Failure modes by family

| Family | Failure that defeats it | Where it bites today | Counter-measure and placement | Depends on |
|---|---|---|---|---|
| Authorization | one holder keeps every capability; nothing expires or attenuates | OSC-02: 26 tokens in one service worker | Biscuit grants per principal with TTL (adapter); revocation set and stream registry (core) | X-1 store |
| Authorization | a revoked grant keeps an open SSE stream alive | no revocation exists | stream terminators called on revoke (core) | `writeBridgeEventStream` registry |
| Containment | child reaches the bridge port and uses the open prefixes | sandbox-exec allow-default; Linux and Windows unconfined | srt netns with the proxy ports only (adapter); Convira Windows after review, for network-free tasks | shared case X5-b; ranked test 1 (Windows) |
| Containment | a confined child exfiltrates the workspace to an allowlisted host under its own credentials | any allowlist | per-delegation allowlist limited to the virtual host by default; `CONNECT` only when the task needs it; per-call audit with byte counts (broker) | X-5 |
| Containment | reparse-point in a granted path extends an ACE to the real target | Convira Windows backend (hypothesis) | refuse grant paths with reparse points (adapter) | ranked test 1 |
| Secrets | provider echoes the key back into the child | srt env-mask; Alpha env injection | broker with header-only injection and redactor (core process) | ranked test 2 |
| Secrets | a stock client sends `Authorization`, the broker forwards it | Aegis custom header | strip credential headers before injection (broker) | none |
| Security state | the defended-against party writes the file | nine dossiers | store outside user folder; deny roots; HMAC chain with credential-store head (core); level (a) only on one account | credential store per OS; A2 for level (b) |
| Security state | restore from backup rewinds the chain | any file store | head mirror in the credential store; fail closed with alarm (core) | credential store reliability (falsification 4) |
| Approval and audit | the agent approves its own action | any approval route; `actorType:"human"` client-asserted (`archive-review-policy.mjs:18-36`) | helper process, WYSIWYS digest, no route (core) | X-4 |
| Approval and audit | ledger tail truncated by the same user | durabletask signed history, hypercore, git | signed head in the store; later a user-chosen external checkpoint (export, second device or a witness the user picks; off by default) (core) | X-1 |
| Approval and audit | the action runs when the append fails | none today | append-then-act; fail closed (core) | CATP pattern |
| Component surface | a new listener without authentication | Aegis, durabletask gRPC, srt in-process proxies, Hermes dashboard proxy | listener audit test on the route table; stdio or inherited pipes only (core) | `bridge-route-capability-audit.test.mjs` |
| Browser gating | the page or a sibling tab defeats a DOM heuristic | OSC-19, OSC-20 | worker-side classifier (adapter); execution tickets from the core (A2 seam 3) | nanobrowser port; A2 |
| Browser gating | Block keyed by exact host is bypassed by a subdomain | nanobrowser upstream | registrable-domain match (adapter) | public-suffix list offline |
| Durability | crash after the side effect, replay repeats it | OpenWorkflow at-least-once; durabletask | effect journal with `indeterminate` and `maximumAttempts: 1` (core) | X-1 store; crash test |
| Durability | cancel does not abort the running step | OpenWorkflow | abort signal threaded into runners (adapter) | `agent-control-runner.js` |
| Supply chain | a manifest that says "signed" with no bytes | OSC-31 | TUF verifier at install, start and hourly (core); tombstones with reason class | tuf-js; publisher keys |
| Supply chain | forceCache skips root rotation when the timestamp expired | tuf-js `updater.ts:85-94` | no-network fetcher when offline; online `forceCache:false` (adapter) | tuf-js test T-8 (forceCache regression); ranked test 3 covers the separate diamond-delegation hypothesis |
| Provenance | the attributed agent forges its own attribution | no producer exists; SD-JWT carries only `declared` | receipts from the in-process sink; `method` restricted; reviewer second signer (core; DAO) | R12 adapter; DAO review |
| Credentials | a NonTransferable credential is moved by co-signing | rewards `TransferPoints` | no holder-plus-issuer move instruction; governed re-binding with veto window (contract) | Phase 2 program |
| Governance | one key changes the electorate | Realms shared instance; rewards vault `time_lock 0`; devnet single upgrade key | every authority under a multisig with a seven-day timelock; insiders at most k-1 (off-chain policy, later contract) | custodian recruitment |
| Governance | reviewer and signer differ, so the ledger records what no one checked | hypercerts evaluators | reviewer equals signer; one acknowledgement per contributor (DAO ledger) | Tessera personality |
| Accounting | activity farmed into reward | tea.xyz; `$RES` for calls (I-1) | outcome-only accrual with explanation records and appeal; per-epoch caps (DAO) | lexicon; review tiers |
| Accounting | collusion rings undetectable from bids | reviewer-assignment literature | no self-review, rotating reviewer draw from the ledger, sponsor caps (DAO) | R27 uninspected |
| Sybil and personhood | one person registers many members, or a sponsor farms AI members with a self-declared human share | I-17: no per-sponsor agent cap, no delegation rule; R25 and R27 not inspected | per-sponsor caps and reviewer-vouched admission in the membership registry; the pilot admits members by named invitation only; no technical personhood answer exists (policy) | R25 decision; R27 inspection |
| Privacy | a status-list fetch tells the issuer who verified what, when | SD-JWT status lists | offline fetcher with a maximum status age; batch fetch of whole lists (adapter) | R12 adapter |
| Privacy | a public revocation record stigmatises a member for ever | Realms on-chain records; TM-9 "no revocation reason on-chain" | reason class and appeal reference in the off-chain ledger only; on-chain state carries commitments, never reasons (DAO) | A3 Phase 1 |
| Privacy | per-epoch member keys defeat the auditability that unlinkability was meant to balance | DR-32 against D4.0 (3)(b) | typed per-epoch counts committed to the ledger; a member can prove continuity by opening a commitment (DAO) | lexicon |
| Privacy | the extension's local stores are plaintext | `chrome.storage.local`, markdown and JSON under the user folder | R15 vault over the store (6-12 months); until then the honest label "local, plaintext" | R15 |
| Minimal architecture | a rewrite stalls and the Alpha stays unprotected | ADR-037 | A1 before A2; seams, not rewrites | backlog order |

### 9.3 Five serious negative findings

These are the article's five for a reader deciding what to do next; the Stage 3 register's five (srt masking returns the key; no adoptable R22 credential; the shared Realms instance; every R11 design keeps the key beside the ledger; the X-1 and X-4 placements) are in `architecture/risk-register.md` section 3 and surface in 9.1 and section 5.

1. **Windows containment is unmeasured, and a pass would not cover delegation.** Nothing in the evidence shows a no-admin Windows sandbox that confines a Node child with piped stdio; the one measurement found (restricted tokens) shows breakage. Even if ranked test 1 passes, an AppContainer child can never be granted loopback and a network-enabled one gets the Internet with no proxy, so Convira covers network-free tasks only; delegations that call a provider stay on srt-win (opt-in, elevated install, labelled bypassable) or unconfined until a named-pipe transport exists. If ranked test 1 fails as well, the honest Windows story is "token-only, unconfined, labelled", and the article says so.
2. **Human/AI attribution has no source.** Every accounting and governance rule that depends on I5 (voting weight, contribution ladders, the human-only electorate) rests on a self-declaration. The research found no format, library or measurement that produces it. Section 12's PoC 4 tests the only honest option: declared attribution, counter-signed by a reviewer, with the DAO treating it as a claim.
3. **The devnet artifacts contradict the specification.** The `$RES` supply exceeds the plan, the mint authority is live, the program's upgrade authority is one wallet, and the model is superseded. Devnet is a test network where over-supply is normal, but readers of it see an earlier test model, not the current design. The maintainers should either set the authorities to none or label the artifacts as superseded test material.
4. **The shared Realms instance fails the DAO's own invariants.** Unpublished source, 5-of-7 council, no hold-up, veto disabled, delegation undisableable. Using it would make DR-54's "binding vote" a council decision. The verifier in 8.9 returns `fails` for it by design.
5. **The Alpha's own trust claims are ahead of its code.** Promotion cannot run (OSC-24), per-site permissions do not block (OSC-13), manifests are not signed (OSC-31), the human-only boundary is regex (OSC-19). None of this is hidden; it is the gap between `docs/STATUS.md` and `HEAD`. One of the first contributions in section 11 (BL-23) is correcting the status documents.

### 9.4 Residual risks the selected path accepts

On Windows, where children run unconfined by default, and on any OS with the containment flag off, the approval helper, the store and the broker give no protection against a hostile delegated agent: it runs as the user and can drive the dialog, read the store key and read the broker's memory. Phase 1 therefore does not meet the threat model's requirement of level (b) for routes that gate irreversible browser actions (T1) and approvals (T22); the decision records narrow the attacker model to confined children until A2, and the delegation UI on Windows should say "unconfined: this agent can approve its own actions". Same-user code execution of any other kind defeats the local design until A2's separate account, and even then it defeats the browser half. A compromised provider learns everything the user sends it; the broker protects the key, not the prompt. Containment limits where data can go, not what an allowed destination receives. If one of the three outside witnesses colludes with the log host, two disjoint groups of members can be shown different forks, each with two valid cosignatures; only the members' gossip check across witnesses detects it. The TUF root is only as good as its keyholders' hardware tokens. Nothing here protects against a malicious maintainer who ships a bad release that passes certification; the certification protects against unauthorised releases, not bad authorised ones. Personhood (R25) remains a policy question with no technical answer in this research.

### 9.5 Friction the protections cause

| Protection | Who bears the friction | Mitigation |
|---|---|---|
| Linux and Windows confinement (srt needs bubblewrap, socat, ripgrep and an AppArmor sysctl on Ubuntu 24.04; srt-win needs an elevated install) | every user who wants bounded delegation | a first-run setup script with one administrator prompt; the delegation UI shows "unconfined" until it has run |
| Approval dialog per delegation start and per promotion | every user, several times a day | one-shot approvals only for the classes that matter (promotion, delegation with execution, credential writes); no approval for reads |
| Certification staleness offline (tuf-on-ci defaults expire timestamps within two days; new installs refuse) | offline and travelling users | longer timestamp expiry for the Resonant registry; installed add-ons keep running; only new installs wait |
| Per-item consent for claim packages (T0-T3, preview every package) | contributors filing many claims | batch preview of several items at one tier; defaults remembered per project, never implied |
| Per-epoch member keys | every DAO member, once per epoch | the claim-package builder rotates and re-binds in one step; continuity provable by opening a commitment |
| Suspend-on-security-revocation of an add-on | users of the suspended add-on | notice with reason class, appeal reference and a logged local override |

## 10. Roadmap

Each item names an owner role (M maintainer, C contributor, D DAO operating team), an output and the signal that moves it from "designed" to "tested". Estimates assume one maintainer plus two to three contributors part-time, and are planning ranges, not promises.

### 10.1 Now (next cycle, weeks 1-4)

| Item | Owner | Output | Done when |
|---|---|---|---|
| Correct `docs/STATUS.md`, the capability matrix and ADR-038's status | M | docs PR | the status page matches `HEAD` and marks OSC-24, OSC-13, OSC-31, OSC-19 as open |
| Security-state store and deny roots (8.1) | C | PR behind nothing (additive) | `security-state-store.test.mjs` green on the Linux lane; Windows and macOS cases run by hand until those lanes exist (BL-27) |
| Provider broker and srt adapter (8.2) | C | PR behind `RESONANTOS_DELEGATION_ISOLATION=srt` | echo stub test green; keys absent from the Hermes and OpenCode CLI env in the inverted tests |
| Approval helper, ledger and gate on `archive-promote` and delegation start (8.3), with the promotion fix (8.7) in the same change | C | PR | 428 cases green on the Linux lane; native dialogs demonstrated by hand on three OSes; promote refused without a record |
| Narrow the proxy exemption (R05) | C | PR | Origin and Host rejection tested; one exempt prefix |
| Run ranked tests 1-3 in a throwaway VM (section 12) | M | test reports | verdicts recorded in `acceptance-backlog.md` |
| Resolve OI-1 to OI-4 (section 13) | M | decisions | each item has a dated answer |

### 10.2 Next (weeks 5-12; 30/60/90 days)

The windows follow `architecture/reference-architectures.md` section 6; the helper lands at the end of the Now window above.

- **Day 30:** the Now items merged behind flags; Windows and macOS CI lanes added to `alpha-build` (BL-27) so the three-OS claims become tested.
- **Day 60:** Biscuit grants in dual mode (8.4); TUF verifier on `/addons/install` with a test registry and 2-of-3 root (8.5); the eight manifests corrected; durable jobs additive (8.6) with the crash test (PoC 6); approval ledger `exportHead()`.
- **Day 90:** memory git ledger with signed promotion (8.7); provenance records per boot (8.8); classifier port with the governance category and registrable-domain Block; Goose adapter with a fake ACP child; a listener-audit test on the route table (`bridge-route-capability-audit.test.mjs`: no new listener without authentication); `tlog-verify.mjs`; DAO authority and credential verifiers with recorded fixtures (8.9).

### 10.3 Later (days 90-180)

- A2 seam 1: grant model and store out of `authorizeBridgeRoute` into an authority core; the isolation broker as its own process.
- A2 seam 3: execution tickets for the browser's submit, pay, grant and governance classes (BL-20), with the sibling-leak test.
- Phase 2 user verification in the helper (Windows Hello, Touch ID, polkit) with out-of-band enrolment.
- Browser jobs move to the durable engine; abort signals threaded.
- Windows containment decision from ranked test 1 and the srt-win residual check: Convira Windows backend vendored for network-free tasks if the test passed; otherwise Windows stays labelled.
- Static capability tokens retired; the extension requests grants at startup (BL-26).

### 10.4 Six to twelve months

- Supervisor per OS (systemd user unit, launchd agent, Windows service wrapper) with a hashed baseline that excludes `security/` (R04); separate OS account for the core and broker (level (b)); A2 seam 2 (Hermes proxy and launcher into add-on-owned components) and seam 4 (one promotion contract over MCP); the baseplate the website describes exists in code.
- DSH and `opencode serve` on the reverse channel (RR-12); the R15 vault over the store; R25 and R27 inspections, which the DAO's admission and review rules wait for.
- DAO Phase 1 pilot: Tessera personality, three witnesses recruited, `authorities.json` published and logged, advisory vote replay, members on per-epoch keys admitted by named invitation only (twenty is a planning figure); devnet artifacts retired.
- DAO Phase 2 decision gate: audit, custody policy, devnet test of the exact program; only then a Token-2022 class and a Squads vault.
- Ecosystem: a certified add-on registry with public keyholders; a second delegated runtime behind the same adapter interface; an injection measurement suite run in CI against the ported classifier (PoC 7).

### 10.5 Dependencies and what moves the dates

The store (8.1) gates everything. The broker (8.2) gates removing keys from children, which gates calling delegation "bounded". Ranked test 1 decides whether Windows containment is a Now item or a Later one. Three outside witnesses gate the DAO pilot; without them Phase 1 is a signed log with no split-view protection, and the article would not call it witnessed. An audit gates Phase 2 entirely.
