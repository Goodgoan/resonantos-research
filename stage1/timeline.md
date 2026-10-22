# Stage 1 - Governing documents, timeline, generations, discrepancies (agent s1-timeline)

Verification date 2026-10-20. Alpha repo: `dev` HEAD 578fbbc3c1c854b192318b3d2163b138fb45d8bd (2026-10-18), 1056 commits, inspected read-only. Evidence labels: [I] inspected, [R] reported by authors, [H] hypothesis.

## Summary
1. Alpha runtime is governed by docs/architecture/ALPHA_RUNTIME_BOUNDARY.md (normative) plus docs/STATUS.md (facts); both name "Chrome MV3 extension + authenticated local Node bridge" as the only two components. Confidence high.
2. The "next-generation architecture" has NO ratified single document. Best candidates: ADR-038 (Accepted, 2026-09-15, Guardian/Core-only invariants) and docs/planning/ (explicitly "planning material, proposals"; Phases 6-11 "undecided"). Confidence high that it is unratified.
3. DAO authority: resonantdao.com whitepaper v0.6 draft (2026-08-30) is declared "source of truth" for DAO design (resonantos-website archive, commit 0eed256 2026-06-02); contribution-economy is a "working specification v2". No DAO code is public (ResonantDAO org: 0 repos). Confidence medium-high.
4. Generations verdict: the OS website's "baseplate" and the public Alpha are different generations/scopes, not one runtime; the site itself says "designed on paper". Confidence high (site text + git); lineage to Guardian/Authority Plane planning is medium [H].
5. The repo shows overlapping lineages: pre-import Tauri/Rust/Electron design (ADRs 001-037, Apr-May 2026), browser-first MV3+bridge (shipped, from 2026-05-26), and the DSH-based Augmentor imported 2026-09-14/15 (apps/augmentor, own history, absent from STATUS/README).
6. Repo "2.0.0-alpha" / package `resonantos-vnext` 2.0.0-beta.1 mismatch is explained by the docs (alpha gate met 2026-07-21, beta.1 prepared 2026-08-22) but nothing is tagged or released on GitHub and there is no `main` branch. "Released" and "deployed" are unverified for the runtime.
7. 23 timeline entries, 16 discrepancies; largest: STATUS and CAPABILITY_MATRIX lag the harness subsystem (PRs #469-#490, #534) and apps/augmentor.

## Governing documents
Last changed = `git log -1` for that path on dev.

| Domain | Document | Path / URL | What declares it authoritative | Last changed | Confidence |
|---|---|---|---|---|---|
| Alpha runtime (boundary) | Alpha Runtime Boundary | docs/architecture/ALPHA_RUNTIME_BOUNDARY.md | Self: "Normative Boundary ... exactly two required runtime components"; MODULE-OWNERSHIP.md: "defines what ships"; ADR-001/037 alpha notes point to it | 1f5b6d8 2026-09-11 | high |
| Alpha runtime (current facts) | STATUS | docs/STATUS.md | Self: "current status source of truth"; docs/README.md | 16fe456 2026-09-14 (stale: ~190 commits since) | high that it governs; medium that it is current |
| Alpha capabilities | Capability Matrix | docs/reference/CAPABILITY_MATRIX.md | docs/README.md and STATUS link it; separates "implemented" from "release proof" | 5bed4fa 2026-07-31 (predates harness and #441 SDK move) | medium |
| Alpha code ownership | Module Ownership | docs/architecture/MODULE-OWNERSHIP.md | Self: "normative contributor-facing ownership contract" | d63f7b2 2026-10-15 (current; lists dsh-runtime, harness-*) | high |
| Release scope / schedule | GitHub Project 2 (external, not inspected), docs/ROADMAP.md, docs/PROJECT_GOVERNANCE.md | https://github.com/orgs/ResonantOS/projects/2 | ROADMAP: "Project 2 is the release planning authority"; README; AGENTS.md | ROADMAP 653de26 2026-09-06; GOVERNANCE abc8c1f 2026-10-06 | medium (authority outside repo; unverified) |
| Beta.1 scope | RELEASE_NOTES_BETA1.md | docs/RELEASE_NOTES_BETA1.md | Self; version bump in ca9e6d1 | ca9e6d1 2026-08-22 | medium |
| Contributor process | AGENTS.md (+README, INSTALL, CONTRIBUTING) | AGENTS.md | docs/README.md: "canonical contributor path". Described process = evidence only | c3de457 2026-07-10 | high |
| Decision records | ADR set 001-038 with "Alpha applicability" field | docs/architecture/ADR-*.md, README.md index | Metadata added in 305d154 2026-07-10 | ADR-038 eaadd34 2026-09-15; rest 2026-07-10 or earlier | high |
| Next-gen (accepted piece) | ADR-038 Guardian / Core-only invariants | docs/architecture/ADR-038-guardian-engineer-core-only-invariants.md | "Decision status: Accepted; Alpha applicability: Partial"; says Guardian and confined DSH runtime are NOT implemented | eaadd34 2026-09-15 | high |
| Next-gen (direction) | planning set | docs/planning/README.md, 02-sdk-dao-governance-roadmap.md, 03-master-implementation-plan.md | README: "planning material: proposals and schedules, not shipped runtime facts"; 02 calls itself "authoritative future direction"; 03 calls Tom's 2026-09-16 sync "authoritative current direction" and DAO/NFT/marketplace scope "undecided" | 4f1ef1a 2026-09-20; 3e459f6 2026-09-18 | medium; labels contradict |
| Next-gen (website) | "neutral baseplate" | https://resonantos.com/ ; resonantos-website index.html | Site: "designed on paper", "Before one line of code ships" | 0f9f927 2026-09-03 | high that it is aspirational |
| Older native design | ADR-001/009/025/035/036 (Tauri, Electron, wallet browser) | docs/architecture | Superseded or Partial per metadata; STATUS: "historical or future work, not Alpha runtime" | 305d154 2026-07-10 | high |
| DAO design | ResonantDAO whitepaper v0.6 draft | https://resonantdao.com/whitepaper/ | resonantos-website archive/astro-src whitepaper.astro and about.astro: "source of truth for the DAO" | page dated 2026-08-30 | medium-high |
| DAO contribution / rewards | Contribution Economy working spec v2 | https://resonantdao.com/contribution-economy/ | Self: "Working specification"; $RCT "Formula pending calibration" | undated | medium |
| DAO membership entry | /start/, /build/ | https://resonantdao.com/start/ , /build/ | Site pages; "No wallet, no NFT, no gate to start"; labels from shipped work | undated | medium |
| DAO research (non-binding) | resonantos-economy-research | repo | Self: "local-research-only", "standalone research authority" | 652d12a 2026-07-18 | high that it is non-binding |
| Values / legal reuse | Augmentatism manifesto; Symbiotic Licence | https://augmentatism.com | Manifesto: anti-capture, consent. Licence: only described as an NFT credential; archive site: "canonical text and hash remain a mainnet requirement". Alpha repo licence: MIT | augmentatism.com a00cb7b 2026-03-22 | licence text not found: low |

Superseded or deprecated: ADR-017 (by 025), ADR-025 (by 035), ADR-035 and 036 (by 037), ADR-011 partly (by 013). ADR-037 (Chromium-fork direction) is Accepted but "Partial", and the Alpha is explicitly not that. The older ResonantOS whitepaper on the archived site is marked legacy (two-engine Oracle/Logician, RC-SL name). planning/01 ("Fused Augmentor") is superseded by 02 (Guardian/Engineer). [I]

## Timeline
M = merged to dev, R = released, D = deployed. GitHub shows no releases, no `main` branch, one tag (archive/pr-198-blackboard-experiment, 7fb6c3e); so R is never confirmed for the runtime.

| Date | Change | Evidence | M/R/D | Significance |
|---|---|---|---|---|
| 2026-03-31 to 04-13 | rcode: fork of Claw Code (instructkr); 4 of 497 commits by ResonantOS author | rcode 507c246..136d9fc | public repo | Not a runtime predecessor [I] |
| 2026-04-23 to 05-13 | ADR-001..034 decided (Tauri+Rust+React; add-on SDK ADR-006/018; Living Archive ADR-007/011/012/013; provider fabric ADR-005; minimal kernel ADR-026) | decision dates in docs/architecture/ADR-*.md; text arrived in 589c6bd | design only | Generation 1: native desktop + add-on aggregator [I] |
| 2026-05-24 | resonant-hub PWA starts | resonant-hub fad2343 | public repo | Separate community product |
| 2026-05-26 | First commit in alpha repo: 491 files, 137k lines (src, src-tauri, electron-host, browser-first, addons, 37 ADRs), author Manolo Remiddi; earlier history not present (import) | 589c6bd | M | Project start in this repo; browser-first agent control already present [I] |
| 2026-05-26..31 | Browser-first modularisation; Living Archive LLM-wiki workflow, lint, move-import | d382760..a91a33b; 6bd1ec9 (05-29); ca595db (05-31) | M | Living Archive in bridge (ADR-007/027) [I] |
| 2026-06-08..06-14 | Security hardening; security pipeline (supply chain, runtime hardening) | 93d81fe, 6a4d3d5, 3027099 (06-14); PR #173 | M | Security pipeline [I] |
| 2026-06-21 | "scope alpha to chrome extension": deletes src-tauri and electron-host (-58,998 lines) | 74199ab; PR #182 | M | Decisive pivot; ADRs 001/009/035 become historical [I] |
| 2026-06-25 | Module ownership map | PR #189 5b89332 | M | Ownership contract [I] |
| 2026-06-26..29 | Blackboard add-on experiment (PR #198) unmerged, branch tagged; #238 Plane task board closed experiment | tag archive/pr-198-blackboard-experiment 7fb6c3e; ce4024a; ROADMAP "Closed Context" | abandoned | Abandoned experiments [I] |
| 2026-07-10 | Docs cleanup: 77 obsolete docs removed; ADR status metadata; STATUS, ROADMAP, CAPABILITY_MATRIX, GOVERNANCE created | e476b94, 305d154, 33725f4, 817c09f | M | Birth of current governing-doc set [I] |
| 2026-07-20 | Non-bypassable human-only public-submit handoff; live Agent Control certification lane | PR #268 3b07e63; #269 | M | Agent Control safety [I] |
| 2026-07-21 | Alpha MVP gate declared met (#209) | PR #275 8a00370; 016ed9d | M | Doc claim; issue state not inspected [R] |
| 2026-08-22/23 | beta.1 prepared: CHANGELOG, release notes, package.json 2.0.0-beta.1 | PR #325 530b753; ca9e6d1 | M only; no tag/release | "Prepared", not released [I] |
| 2026-09-04..07 | OpenCode ephemeral port + credential; every bridge route requires a capability; default-deny | #339 12f5d65; #375 5d12d3c; #416 59927a0 | M | Bridge capability model [I] |
| 2026-09-07..08 | Add-on uninstall lifecycle (#180) | #417, #424-#428 | M | Add-on lifecycle [I] |
| 2026-09-10 | Add-on SDK relocated to packages/addon-sdk behind re-export shims | #441 43a4718 | M | SDK extraction [I] |
| 2026-09-14..15 | Subtree import of Manolo's Augmentor (DSH, native messaging; own history from 0a4af06 2026-08-22) as apps/augmentor | 5550432; #448 6281d97; #450 1bf8a24 | M | Second extension lineage in repo; absent from STATUS/README [I] |
| 2026-09-15 | ADR-038 Guardian / Core-only invariants | #452 7c913e1; eaadd34 | M (design only) | First next-gen decision [I] |
| 2026-09-16..26 | SDK/DAO governance planning set; "Fused Augmentor" superseded | #453 6cf259b; docs/planning | M (proposal) | Next-gen direction, unratified [I] |
| 2026-09-21..10-18 | Harness subsystem: contract, registry, DSH adapter, host-signed receipts; native DSH auth | #469 c8b51e7 .. #490 0e73598; #534 578fbbc | M | Largest recent change; missing from CAPABILITY_MATRIX [I] |
| 2026-08-30 | DAO whitepaper v0.6 draft published | resonantdao.com/whitepaper | web | Testnet/devnet claims; mainnet Q4 2026 target [R] |
| 2026-09-03 | resonantos.com relaunched with baseplate narrative | resonantos-website 0dd62a5 | D (GitHub Pages; live fetch 2026-10-20) | Marketing generation [I/R] |

## Generations hypothesis
Verdict: supported. Confidence high on "different generations/scopes", medium on exact lineage.
- Generation 1 (Apr-May 2026): native desktop, Tauri/Rust, add-on aggregator, minimal kernel; ADRs 001-037. Abandoned from Alpha scope on 2026-06-21 (74199ab). [I]
- Generation 2 (shipping): Chrome MV3 + loopback Node bridge per ALPHA_RUNTIME_BOUNDARY.md; version 2.0.0-beta.1. [I]
- Generation 2b: apps/augmentor + harness layer (DSH as AI engine), imported September 2026. [I]
- Generation 3 (proposed): Guardian, Authority Plane, Ground-0, REF, certification, DAO NFTs (docs/planning, ADR-038). Its "minimal kernel / restartable Guardian" language is the closest in-repo match to the site's "small, restartable core". The site says the baseplate is "designed on paper", lists no version/download and says the tech team is "forming now". So the hypothesis that the baseplate is an implemented in-repo runtime is rejected. That it is a later conceptual generation seeded by ADR-026/038 is a hypothesis [H]. Contradicting: the site relaunch (2026-09-03) precedes ADR-038 (2026-09-15) by 12 days, so the site is not derived from ADR-038; it may rest on unpublished design work.

## Discrepancy register
| # | Claim | Source | Contradicting evidence | Status |
|---|---|---|---|---|
| 1 | Repo "2.0.0-alpha" vs package `resonantos-vnext` 2.0.0-beta.1 | repo name; package.json | STATUS/CHANGELOG: alpha gate met 07-21, beta.1 prepared 08-22 (ca9e6d1); CHANGELOG [2.0.0-beta.1] dated 2026-08-22; no tag/release | Resolved with explanation; "released" unverified |
| 2 | "Treat main as release-stable" | AGENTS.md lines 46-47 | gh api: no main/master branch; default is dev | Unresolved |
| 3 | Baseplate "designed on paper"; no code | resonantos.com | Alpha repo: 1056 commits, tester build | Resolved: different generations |
| 4 | Site: restartable core with containment | resonantos.com | ADR-038: Guardian and confined runtime "not implemented" | Unresolved gap (design vs code) |
| 5 | DAO "testnet/devnet work"; "Solana mainnet Q4 2026" | whitepaper v0.6 | ResonantDAO org has 0 public repos; no contract code or addresses in any clone; "mainnet" hits in economy-research are Bitcoin (D-13) | Unresolved; DAO code class F |
| 6 | DAO home/start make no chain claims | resonantdao.com | whitepaper and archived site do | Resolved: claims live only in whitepaper |
| 7 | STATUS = "current status source of truth" | docs/STATUS.md | Last change 2026-09-14; zero mentions of apps/augmentor or DSH; harness, packages/addon-sdk later | Unresolved (stale) |
| 8 | Capability matrix maps all capabilities | CAPABILITY_MATRIX.md (2026-07-31) | 1 line mentions harness/DSH; rows cite src/sdk/addons/*.ts which are now re-export shims of packages/addon-sdk | Unresolved |
| 9 | CHANGELOG [Unreleased] | CHANGELOG.md (2026-09-04) | Omits harness, ADR-038, SDK move, Augmentor import | Unresolved |
| 10 | SDK shim cites ADR-055 and ADR-056 | src/sdk/addons/registry.ts header | docs/architecture ends at ADR-038; planning: "new ADRs start at 039"; 3e459f6 "ADR-039/040 drafted" but no such files in tree | Unresolved (dangling) |
| 11 | Alpha excludes native hosts | README/STATUS | addons/resonant-browser-host still in tree; ADR-037 Accepted says ResonantOS "must become" a Chromium browser | Partly resolved: labelled non-Alpha |
| 12 | planning/ "working source of truth" vs STATUS "source of truth" | docs/planning/README vs STATUS | Two source-of-truth claims; planning README itself says proposals only | Resolved by hierarchy; wording conflicts |
| 13 | 02-roadmap "authoritative future direction" vs 03 "DAO/NFT scope undecided" | docs/planning/02, 03 | Internal contradiction | Unresolved |
| 14 | economy-research "private/internal until public-export scrub" | its README | gh api visibility=public | Unresolved |
| 15 | Project 2 is release authority | ROADMAP, AGENTS.md | External; not inspectable | Unverified |
| 16 | Wallet/DAO helpers "implemented read-only; public acceptance blocked" | CAPABILITY_MATRIX | Whitepaper treats wallet-bound NFT membership as core; no on-chain client found in Alpha (not exhaustively searched) | Unresolved; class C/D |

## Open questions
- Is there private DAO or contract code, or a Solana devnet deployment? Not discoverable; no explorer or package search performed.
- Where is the Symbiotic Licence text and legal status? Not on augmentatism.com or in the Alpha repo (MIT).
- Pre-2026-05-26 history (ADR dates from 2026-04-23) is not in this repo.
- Is beta.1 distributed anywhere (store, release asset)? No evidence.
- Project 2 and issue states not inspected; the "alpha gate met" claim is reported by authors.
- Were ADR-039/040 written on unmerged branches? Not examined.
- Subtree import dates vs PR merge dates (5550432 2026-09-14 vs #448 2026-09-15) differ; cause not examined.
- Website text came via a summarising fetch tool, not raw HTML (local repo index.html confirms "baseplate", "designed on paper").

## Sources
In stage1/sources/timeline/: alpha-git-log-dev.txt (full git log, 2026-10-20), alpha-prs-closed-dev.tsv (closed PRs on dev, gh api), git-facts-other-repos.md, web-resonantos-com.md, web-resonantdao-com.md, web-resonantdao-whitepaper.md, web-resonantdao-contribution-economy.md, web-augmentatism-com.md.
