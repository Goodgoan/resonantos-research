# Threat model draft (lead, v0.1, 2026-10-20)

Purpose: sharpen the Stage 1 findings into named threats so that Stage 2 candidates and Stage 3 scoring can be judged by which threats they close, not by feature lists. Every threat cites the Stage 1 evidence that makes it real today (OSC rows from `stage1/capability-matrix.md`, DR and I rows from `stage1/dao-requirements.md`, os-map sections) and the requirement IDs from `stage1/gaps.md` that would address it. Status of this document: lead's analysis, not yet reviewed adversarially; Stage 3 reviewers should attack it. Evidence types are those of the cited Stage 1 rows (static inspection; nothing executed).

## 1. Assets

| Asset | Where it lives today | Why it matters |
|---|---|---|
| A1 Provider API keys | bridge process memory and env; injected into Hermes, OpenCode and DSH child processes (OSC-16, OSC-33, OSC-36) | direct financial loss and impersonation of the user to providers |
| A2 Bridge and capability tokens (26 static) | one extension service worker; generated config written into the extension tree; override copies in chrome.storage.local (OSC-02, OSC-06) | holder has every privileged route for the process lifetime |
| A3 Living Archive and user state root (`~/ResonantOS_User`: HUMAN_KNOWLEDGE, EXTERNAL_KNOWLEDGE, AI_MEMORY, chats, delegation workspaces) | plaintext markdown and JSON; chats in chrome.storage.local (OSC-10, OSC-28) | the user's private knowledge; the sovereignty promise |
| A4 Browser session authority (logged-in sites, ability to click, type, navigate, submit) | content scripts in all frames of all sites; host_permissions for all sites (OSC-01, OSC-13) | irreversible real-world actions: purchases, posts, messages, deletions |
| A5 Human-only boundary (wallet signing, payments, login, public submission, voting) | English regex heuristics in the content script; no host-side checkpoint (OSC-19, OSC-20, OSC-47) | the project's central safety and accountability claim |
| A6 Integrity of the running system (code, add-ons, config) | add-on manifests self-declared "signed" with no signature bytes; no updater, no baseline hashes (OSC-31, OSC-42) | supply-chain substitution and persistence |
| A7 DAO membership and credential state | no official program; legacy devnet mints and an upgradeable program under single keys (DR-01, DR-48) | governance capture and member privacy |
| A8 Contribution records and governance weight | specification only; 22 balances, $RCT, three contribution ladders (DR-20..28, DR-40) | the DAO's economic and political substance |
| A9 Member personal data | resonant-hub community.db with 24 member rows and Discord handles committed to a public repo (OI-1) | privacy and legal exposure |

## 2. Adversaries and their reach

| Adversary | Reach today | Notes |
|---|---|---|
| V1 Malicious or compromised web page | can inject instructions into any page the agent reads; can make no-cors requests to `http://127.0.0.1:<bridge-port>/api/...` (OSC-05); can bait the planner into clicking links whose text carries commit words (OSC-19) | the most likely attacker; zero cost |
| V2 Other local process (same user) | reaches the open proxy prefixes on loopback without a token (OSC-05); on Windows can read the config file since 0600 is meaningless (OSC-06); can read chrome.storage.local via Chrome's profile directory | includes any malware the user already has |
| V3 Delegated agent child (Hermes, OpenCode, DSH) | runs with provider keys in its environment, full PATH, no confinement outside macOS (OSC-16, OSC-32, OSC-34); can write to the user state root through the bridge with the capability it was given, which is the whole capability (OSC-45) | a prompt-injected or buggy agent is this adversary without any intent |
| V4 Malicious or compromised add-on | content-script add-ons share the extension's full privileges (OSC-30); manifests unverifiable (OSC-31); install UI deferred so sideload is the path (OSC-61) | supply chain; today small because the ecosystem is small |
| V5 LAN attacker | bearer-over-plain-HTTP when the bridge binds a non-loopback address; a dev LAN address ships in presets (OSC-14, os-map 5.3) | only when the user opts into LAN bind, but the preset lowers the bar |
| V6 DAO insider: custodian, reviewer, sponsor | custodians set salience templates and weight functions during bootstrap (I-17); reviewers in a small pool can be captured (DR-24); a sponsor can register unbounded AI members (DR-13); single-key upgrade and mint authorities on devnet (DR-48) | structural; the spec grants the power and names no check |
| V7 Sybil or farming participant | base membership weight per wallet (DR-10); activity rewards survive in the text (I-1); accusation and verification markets (DR-29) | economic attacker; the spec acknowledges some and bounds none |
| V8 The project itself (honest mistakes) | STATUS and capability matrix stale by ~190 commits; "implemented" claims that do not hold (OSC-24); website claims not in code (OSC-48..50, OSC-51) | not malice; a reader who trusts the documents acts on wrong premises |

## 3. Threats, evidence and the requirements that close them

Format: Tn: threat. Evidence. Closes with: requirement IDs. Severity is the lead's judgement (high = irreversible harm or boundary collapse; medium = contained harm or precondition for high; low = hygiene).

### Runtime (ResonantOS)

- T1 (high) Prompt injection drives an irreversible browser action. V1 via A4 and A5. Evidence: ask and trusted modes behave identically; blocked does not stop navigation; human-only detection is regex on English text; a public-submit regression was recorded as "passed with gates" (OSC-13, OSC-19, OSC-20); the planner is never exercised by any test (OSC-18). Closes with: R19 (host-enforced gate and ceremonies), R11 (approval ledger the route requires), R10 (idempotency for browser mutations).
- T2 (high) Provider key exfiltration by a delegated child or by anything that can read a child's environment. V3 via A1. Evidence: OSC-16, OSC-33, OSC-36; PATH and full process.env passed (OSC-34). Closes with: R03 (broker), R02 (containment), R01 (per-principal grants so a child never needs the bridge's keys).
- T3 (high) Local-process or web-page access to the bridge through open proxy prefixes; token theft from disk or chrome.storage. V1, V2 via A2. Evidence: OSC-05, OSC-04 (Origin not an authorization input; empty allowlist), OSC-06. Closes with: R05 (loopback model), R20 (channel choice), R01 (short-lived, bound grants so theft has a short life).
- T4 (high) Confused deputy: a token holder has the whole capability, requests carry no principal, so any component that reaches the bridge acts as the user. V3, V4 via A2 and A3. Evidence: OSC-02, OSC-45, OSC-46; one `archive-write` covers raw intake and trusted-wiki promotion (os-map 13). Closes with: R01, R21 (add-on isolation), R14 (separate promotion contract with its own gate).
- T5 (high) Silent corruption of the knowledge boundary: AI derivations promoted into human knowledge without a working human gate, or source text mixed with AI output. V3, V8 via A3. Evidence: promotion path cannot execute and the approval gate is a no-op (OSC-24); domain separation is metadata only (OSC-25); provenance directory empty (OSC-26). Closes with: R14, R11, R12.
- T6 (medium) Supply-chain substitution of an add-on or of the bridge itself; rollback restores revoked code. V4 via A6. Evidence: OSC-31, OSC-30 (grantedCapabilities never consulted), OSC-42, ADR-038 requirement that rollback must not restore revoked authority. Closes with: R18, R04, R21.
- T7 (medium) Crash during an uncertain side effect duplicates or loses an irreversible action; jobs flip to paused on panel load; cancel does not kill. V3, V8 via A4. Evidence: OSC-21, OSC-22, OSC-33, OSC-42. Closes with: R10, R04.
- T8 (medium) Data loss or lock-out from a torn write: every memory route throws on a corrupted JSON file. V8 via A3. Evidence: OSC-28 (bare JSON.parse, no fsync, no crash tests). Closes with: R13, R15.
- T9 (medium) Plaintext secrets and chats at rest; keys lost on restart drive users to insecure persistence. V2 via A1, A3. Evidence: OSC-10, OSC-16, ADR-022 vault deferred. Closes with: R15, R03.
- T10 (medium) Honest failover hides vendor substitution: an unresolvable model falls through to a different vendor with that vendor's key, and provider error bodies are relayed unredacted. V8 via A1. Evidence: OSC-14, OSC-17, os-map 5.3. Closes with: R08.
- T11 (low) Interoperability claims (MCP, A2A, SKILL.md, signed add-ons, "comes back whole") that the code does not implement lead integrators to wrong assumptions. V8. Evidence: OSC-48..51, OSC-31. Closes with: R06, R07, R09, R04 and, above all, accurate status documents (article recommendation, not a component).

### Governance and economy (ResonantDAO)

- T12 (high) Governance capture during bootstrap: custodians define weight functions and salience templates, hold single-key upgrade and mint authority, and the custodian transition has no trigger. V6 via A7, A8. Evidence: I-17, DR-46, DR-47, DR-48. Closes with: R24 (multisig-timelocked authorities, staged transition), R30 (off-chain Phase 1 keeps the blast radius small).
- T13 (high) Human-only governance undermined by self-declared human/AI splits and uncapped sponsored AI members. V6, V7 via A8. Evidence: DR-13, DR-17, I-17; whitepaper "human governance rights should remain human-controlled". Closes with: R25, R12 (attribution carried from the point of work), R26.
- T14 (high) Member personal data exposure. V1 (anyone) via A9. Evidence: OI-1 (community.db committed), DR-09 (membership privacy absent from the spec), "the software logs every member action" (I-14). Closes with: R23 (privacy-by-default registry with inclusion proofs), R30; and OI-1 is a maintainer matter held for the article (D1.3).
- T15 (medium) Credential loss or theft with no revocation or recovery: a lost key is a lost membership; a stolen non-transferable credential cannot be frozen. V7 via A7. Evidence: DR-06, DR-07, DR-08; hub minter never freezes (DR-01). Closes with: R22, R23.
- T16 (medium) Collusion rings, reviewer capture, appeal flooding, verification spam, accusation markets. V6, V7 via A8. Evidence: DR-24..29, dao-requirements section 7 attack list. Closes with: R26, R27, R28.
- T17 (medium) Economic contradiction exploited: activity rewards in the text versus outcome-only in the mechanism; three contribution ladders. V7 via A8. Evidence: I-1, I-4, DR-40. Closes with: R26 (one ledger with explanation records) and a specification fix (article recommendation).
- T18 (medium) On-chain premature commitment: minting tokens or binding votes before the evidence path works freezes design errors into deployed state (the devnet already holds a superseded model). V8 via A7, A8. Evidence: DR-36, I-5, I-6, dao-requirements section 5. Closes with: R30, R23 (anchor commitments, not balances).

### Cross-boundary (OS and DAO together)

- T19 (high) A DAO credential, role or vote becomes runtime authority, or OS data flows to the DAO without a per-item user act. V6 via A2, A3. Evidence: no code yet; the spec text "logs every member action" (I-14) versus interaction invariants I2 and I3. Closes with: the invariants themselves (constraints on every candidate in branches F and G), R12 (claim packages with selective disclosure), R11 (local consent log).
- T20 (medium) Attribution collapse: human/AI portions are not carried from harness session into any record, so the DAO cannot apply its own attribution rule. V7 via A8. Evidence: interaction section 12 (E3 downgraded to C), OSC-35. Closes with: R12, R07.

## 4. Properties a Stage 2 candidate must demonstrate (per threat family)

These become scoring criteria in Stage 3 (`scoring/weights.json`); a candidate that only claims a property scores as B at best.

| Family | Must demonstrate (with test, audit or reproducible example) |
|---|---|
| Authorization (T3, T4) | a revoked or attenuated grant is refused mid-session; grants carry principal identity; verification works offline |
| Containment (T2) | filesystem, network and exec escapes blocked on each OS, or an honest "unconfined" signal; child cannot reach the loopback port unless granted |
| Secrets (T2, T9) | child never sees the key; per-call audit; works for OpenAI-compatible HTTP |
| Approval and audit (T1, T5, T19) | route refuses without an approval record; ledger tamper detected; user-readable export |
| Browser gating (T1) | gate outside the DOM; adversarial injection suite with measured results; MV3-compatible |
| Durability (T7, T8) | recovery after crash during an uncertain side effect with no duplicate; torn-write test |
| Supply chain (T6) | signature and hash verified offline; revocation survives rollback; substitution test |
| Provenance (T5, T13, T20) | human/AI attribution and tool identity expressible; selective disclosure verifiable; anchoring demonstrated |
| Credentials (T15) | non-transferable, issuer-revocable, governed re-binding; audit report; Solana or stated otherwise |
| Governance (T12, T16) | multisig and timelock on authorities; voter-weight plugin; documented failures |
| Accounting (T13, T16, T17) | explanation records; reviewer independence; appeal bound; post-mortems of farming |
| Minimal architecture (T11, T18) | thin layer keeps the A/B features; off-chain Phase 1 covers membership, claims, advisory votes with public auditability |

## 5. What this draft does not cover yet

- Denial of service against the bridge and the user's own machine (resource exhaustion by a delegated child); folded into R02 and R04 for now.
- Legal and licence threats (Augmentor relicensing, OI-3; seven org repos without a licence); tracked in census-notes and held for the article.
- Accessibility and friction costs of the ceremonies (interaction section 9); weighed in the article, not here.
- Adversarial review of this document itself: Stage 3 reviewers are asked to find threats this list misses and threats it overstates.
