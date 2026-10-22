# Gate 1 report: what exists, what is actually needed

Written 2026-10-20 by the lead (Claude Fable 5.1) for a reader who did not watch the run. Research date 2026-10-20. ResonantOS Alpha inspected at commit 578fbbc3c1c854b192318b3d2163b138fb45d8bd (branch dev, 2026-10-18). DAO sources fetched 2026-10-20. Nothing was executed; all code findings are static inspection plus GitHub Actions results read through the API ("reported by CI").

## Outcome

Stage 1 is complete: the ResonantOS Alpha is a working single-user Chrome-plus-Node runtime with careful token plumbing and strong deterministic tests, but several of its own "implemented" claims do not hold at the code level, and the ResonantDAO is specification only, with no official code, program or deployment anywhere public. The gap list has 30 requirements ready for Stage 2 discovery.

## What I need from you (RUN_MODE is gated, so I paused here)

1. **Approve or prune the gap list** in `stage1/gaps.md` (30 requirements, R01-R30; 14 marked P0). Discovery effort scales with it. My recommendation: keep all 30 and let the P0 set drive the Stage 3 shortlist.
2. **Scope of "our own repositories".** The active Augmentor source (ManoloRemiddi/augmentor-agent) and the DAO website source (ManoloRemiddi/ResonantDAO.com) live in a personal account, not in the organisations. My recommendation: treat them as official-adjacent, in scope for inspection, and label them as such in the article.
3. **Three findings the maintainers should hear before the article is finished.** The research boundaries forbid me from opening issues or contacting anyone, so this is your call. (a) `resonant-hub` commits a SQLite file with 24 member rows plus Discord handles; the rows were not read, but personal-data exposure is plausible. (b) The Living Archive promotion path has been unable to execute since a June 2026 commit, while the project's capability matrix lists it as implemented. (c) The vendored Augmentor inside the Alpha is MIT, but its upstream was relicensed on 2026-09-23 with a resale restriction; this needs legal review. Options: I draft a short maintainer note as a file for you to send, or we hold everything for the article.
4. **Inaccessible DAO design documents.** The whitepaper cites three architecture documents and the Symbiotic Licence; all return 404. Only the maintainers can republish them. Do you want to ask them, or should the research proceed treating that design as unknown (status F)?
5. **Stage 2 plan confirmation** (section 6 below): about 19 Sonnet agents in three waves of at most 10. Say "autonomous" if you want Gate 2 to run without a pause.

Everything else below is supporting detail.

## What was established (with confidence)

### The ResonantOS Alpha (high confidence unless noted)

- **What runs today.** A Chrome Manifest V3 extension (0.1.14) and a loopback Node.js 24 bridge exposing 114 capability-gated routes, one bootstrap route and an unauthenticated reverse proxy. Working and tested paths: chat through OpenAI-compatible providers with routing and visible fallback, page context and inline assistant, chat and project workspaces, Agent Control click/type/scroll with a real-Chrome nightly lane, memory source intake with hashing, versioning and audited move/rollback, Hermes/OpenCode delegation with an OpenCode revoke latch, diagnostics, preferences. CI on this commit passes every deterministic lane (browser-first 2414 of 2424 tests, 10 environment skips). No CI lane calls a real language model.
- **Capability matrix.** 63 claims classified: 9 demonstrably implemented and exercised (A), 22 implemented but insufficiently proven (B), 14 partial (C), 12 design only (D), 3 planned (E), 1 unknown (F), 2 superseded (G). File: `stage1/capability-matrix.md`.
- **Downgrades of the project's own claims** (each with file and line evidence in the matrix):
  - Living Archive promotion, draft and revise cannot execute: service and policy modules disagree on argument names, the human-approval gate is a no-op, and no test covers the path (OSC-24).
  - Per-site browser permissions are enforced in one extension page; the "ask before action" and "trusted" modes behave identically; "blocked" does not stop navigation (OSC-13). Human-only boundaries are English regex heuristics in the content script with no host-side checkpoint (OSC-19, OSC-47). The LLM planner is never exercised by any test; a public-submit regression in the live lane reports "passed with gates", not failure (OSC-18, OSC-20).
  - Isolation of delegated agents is macOS-only and permissive; on Linux and Windows it is "contract-only"; the persisted execution opt-in is bypassable per request; provider API keys are injected into child processes (OSC-32, OSC-33, OSC-16).
  - Seven proxy prefixes on the bridge port need no token on loopback (OSC-05).
  - Add-on manifests self-declare "signed" with no signature bytes or verifier (OSC-31). Anthropic and Google presets have no wire code (OSC-15). MCP is an unwired example; A2A and SKILL.md do not exist in code (OSC-48 to OSC-50).
- **Capabilities the research needs that the Alpha lacks entirely:** grant expiry, revocation, delegation attenuation, multi-principal isolation, a host-verifiable approval ledger, supervised crash recovery (OSC-42 to OSC-47).
- **Four seams for a neutral, restartable core** (os-map section 17): the authorization point in the bridge; lifting the Hermes proxy and process launching out of the transport layer; a core-visible human-approval event; one memory promotion contract. Confidence medium: these are the lead inspector's judgement, not yet reviewed adversarially.

### Governing documents and timeline (high confidence)

- The Alpha runtime is governed by `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md` plus `docs/STATUS.md`; STATUS is stale by about 190 commits and never mentions the vendored Augmentor or the harness subsystem.
- No ratified next-generation document exists. ADR-038 (Guardian and core-only invariants, accepted 2026-09-15) is design only; the planning folder calls itself proposals and contradicts itself on authority.
- The website's "neutral baseplate" and the shipped Alpha are different generations; the site says the baseplate is "designed on paper". Native shells were deleted on 2026-06-21. The repo has no main branch, no releases and no beta.1 tag; "released" is unverified. 16 discrepancies are registered in `stage1/timeline.md`.

### Census (high confidence)

- ResonantOS organisation: 8 public repos, only 2.0.0-alpha active and licensed (MIT). Seven repos have no licence file. ResonantDAO organisation: 0 public repos, 0 public members. The organisation list is incomplete (personal-account repos above). 23 census rows in `stage1/census.jsonl`; platform sweep across npm, PyPI, crates.io, Hugging Face, Zenodo, Software Heritage, Docker Hub, GitLab, Codeberg, Gitee, Chrome Web Store found nothing official beyond one npm package (dsh-augmentor). GitHub lists a `verify` workflow with no file in any ref.

### The DAO (high confidence in the verdict, low in any mechanism)

- Status: specification only (D). The membership portal says "Design page, not live yet". 62 verifiable requirements derived (DR-01 to DR-62) in `stage1/dao-requirements.md`, with a non-conflation map of the 22 balances, $RCT, $RES, governance weight and the three competing contribution ladders.
- Legacy devnet artifacts from a superseded token model exist: a non-transferable $RCT mint, a $RES mint whose supply exceeds the whitepaper's plan with a live mint authority, and an upgradeable program controlled by a single key. Nothing on testnet or mainnet. The Q4 2026 mainnet target has no public artifact behind it.
- 17 internal inconsistencies, the most serious: $RES earned for calls and Discord participation versus "outcome, never activity"; "contribution is measured on-chain" versus ledger-first; three incompatible contribution ladders; and the DAO spec's "the software logs every member action", which conflicts with the project's opt-in evidence principle.
- Absent from the official texts: vote delegation rules, emergency powers, upgrade and admin key policy, revocation of human credentials, key recovery, membership privacy. Unaddressed attacks: collusion rings, reviewer capture, agent farming (no per-sponsor cap), verification spam, accusation markets, appeal flooding, Sybil amplification of base voting weight.

### OS-DAO interaction architecture (lead, medium confidence)

`stage1/interaction.md` defines ten exchanges between the systems, four consent tiers, ten invariants, and separates shared requirements (provenance format, signed manifests and certification, credential verification, revocation distribution) from ones that must stay apart (capability enforcement, scoring, token economics, memory, voting). Two project principles are preserved as invariants: ResonantOS stays fully useful without the DAO, and no DAO credential becomes runtime authority.

## Verification

A fresh-context verifier (Sonnet 5.5) re-checked 15 capability-matrix rows chosen by a seeded random sample (seed 20261020; rows OSC-03, 04, 06, 10, 14, 21, 30, 31, 32, 42, 48, 50, 51, 53, 60) against the clone at 578fbbc, plus five census and chain facts. Report: `stage1/verification.md`.

| Checked | PASS | PARTIAL | FAIL | Failure rate (PARTIAL counts half) |
|---|---|---|---|---|
| 15 matrix rows | 9 | 6 | 0 | 20 percent |
| 5 facts (no main branch, zero releases, orphaned verify workflow, devnet $RCT non-transferable and $RES supply, program on devnet only) | 5 | 0 | 0 | 0 percent |

No claim was unsupported. The six partials are two line-number offsets, one status judged one class too low (OSC-10, the verifier says it meets the A definition), one pointer to a re-export shim instead of the real file, a manifest count of eight rather than nine, and one stale test-file pointer. The matrix owner has applied all six corrections (OSC-10 is now class A; counts are A 9, B 22); the CI re-check agreed with the matrix (17 lanes and 724 vitest tests passed; the live lane succeeded). None of the partials affects a Gate 1 conclusion or a gap-list entry.

## What is unresolved

- Whether private DAO or contract code exists (only the maintainers can say).
- Which Augmentor copy is canonical and under which licence.
- Project 2 (declared release authority) and GitHub Packages could not be inspected: the token lacks the scopes.
- Whether the harness "host-signed receipts" are a usable provenance format (Stage 3 code read).
- All Stage 1 code findings are static. Any execution (for example reproducing the broken promotion path) needs your approval at Gate 2 and a disposable sandbox.

## Stage 2 plan

Goal: find systems that already solve the 30 gaps, across the global platforms and the Chinese, French, German and Dutch ecosystems, with a Japanese/Korean probe.

| Wave | Agents | Model and effort | Output |
|---|---|---|---|
| 1 | Term-bank ZH, FR, DE, NL (4) | Sonnet 5.5, medium | `glossary/<lang>.md` with evidence per term |
| 2 | Branches A-H (8) + JA/KO probe (1) | Sonnet 5.5, high (probe medium) | `ledger/discovery-<id>.jsonl`, `negative-<id>.jsonl` |
| 3 | Language agents ZH, FR, DE, NL (4) + provenance/dedup agent (1) | Sonnet 5.5, high (provenance medium) | language ledgers; `ledger/codebases.jsonl`, `coverage-matrix.md` |
| 4 | Pass 2 via messages to the same agents (no new agents); Stage 2 verifier (1) | Sonnet 5.5, medium | thin-cell fills; 10% ledger sample check |

Roughly 19 agents, all Sonnet, in waves of at most 10. Gate 2 deliverable: deduplicated longlist of 30-50 projects, coverage matrix, proposed shortlist of 8-15 codebases for deep inspection, and any sandboxed-execution requests. The lead works in parallel on the Stage 2 coverage review and on sharpening the threat model from the Stage 1 findings.

## Files produced in Stage 1

`research/state.md`, `research/PLAN.md`, `research/lessons/` (3), `research/ledger/platform-urls.md`, `research/stage1/census.jsonl`, `census-notes.md`, `timeline.md`, `os-map.md`, `capability-matrix.md`, `dao-requirements.md`, `interaction.md`, `gaps.md`, `verification.md`, `gate1-report.md`, and `research/stage1/sources/{census,timeline,osmap,dao,lead}/`. Read-only clones of 14 repositories are under `research/_untrusted/`.

## Decisions taken at Gate 1 (user, 2026-10-20)

1. Gap list approved unchanged; the 14 P0 requirements drive the Stage 3 shortlist (D1.1).
2. The personal-account repositories are official-adjacent: inspected and labelled as such (D1.2).
3. The three maintainer findings are held for the article; no note is sent (D1.3).
4. The inaccessible DAO design documents are treated as status F. A request to the maintainers to republish them is needed and is recorded as open item OI-4 in `state.md`; it is not sent now (D1.4).
5. Stage 2 plan confirmed; Gate 2 runs autonomously for the shortlist decision. Sandboxed execution of third-party code still needs explicit approval per run (D1.5).

Gate 1 is closed. Stage 2 started the same day under a new lead session (D1.6).
