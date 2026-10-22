# Stage 1 Census Notes (agent s1-census)

Verified 2026-10-20. Rows: `census.jsonl` (23 rows, 20 keys each). Raw outputs: `sources/census/` (URL/date at top where the format allows; JSON files are raw `gh api` output fetched 2026-10-20). Nothing was executed from any clone; static reading and git history only. CI statements are "reported by CI".

## 1. Method
- `gh api` for org, repo, runs, workflows, releases, tags, contributors, forks, issue/PR counts (search API). Local clones: `git rev-list --count` for 90/365-day cadence (90d = since 2026-07-22).
- Registries via public JSON APIs with curl (read-only GET/POST of search queries, not third-party code). Websites via WebFetch/curl status. Solana via public JSON-RPC read calls.
- Python used only in my own scripts (`python -I`) from outside clones; the committed SQLite file in resonant-hub was opened read-only for table row counts only.

## 2. GitHub organisations
- github.com/ResonantOS (created 2026-03-13, blog resonantos.com): 8 public repos, 0 archived, 0 forks (GitHub-flagged), 1 listed member (Arfitz, public). Packages API blocked (token lacks read:packages); Projects v2 GraphQL blocked (token lacks read:project). Discussions disabled on all 8. Releases: 0 on all 8. Org-wide issues: 262 found by search.
- github.com/ResonantDAO (created 2026-06-04, name "Resonant DAO", blog resonantdao.com, email resonantdao@proton.me): **0 public repos, 0 public members**. `gh api orgs/ResonantDAO/repos` empty; `users/ResonantDAO` is an organisation. The DAO's site source lives in a personal account instead (ManoloRemiddi/ResonantDAO.com).
- Disconfirmation (a) result: the org list IS incomplete. Canonical or related code lives at: ManoloRemiddi (ResonantDAO.com, augmentor-agent, augmentor-app-sdk, archived Open-Toolkit and Augmentor predecessors), tompennington (pre-org copy of alpha, design-token fork), vrondelli (living-archive, fork of vNext), plus community repos (vonstegen, simongonzalezdc, michelnavarra, vijayee). npm package dsh-augmentor is the only registry artifact.
- Per repo (details in census.jsonl): R01 2.0.0-alpha (class B), R02 website (B), R03 augmentatism.com (B), R04 rcode (G), R05 resonant-hub (C), R06 economy-research (D), R07 coordination hub (D), R08 akashic-records (C).
- Disconfirmation (c): "active" repos. Only 2.0.0-alpha (585 commits in 90d) is truly active; ResonantDAO.com (personal) 129; augmentor-agent 401. The seven other org repos have 0 commits in the last 80+ days (website: 7 in 90d). rcode is >95% upstream ClawCode commits and dormant since 2026-04-13.
- Disconfirmation (d): licences.
  - 7 of 8 org repos have NO licence file (website, augmentatism.com, rcode, resonant-hub, economy-research, coordination hub, akashic-records); only 2.0.0-alpha has MIT. rcode additionally derives from third-party code (legal review).
  - apps/augmentor inside alpha is plain MIT (Manolo Remiddi). Its upstream ManoloRemiddi/augmentor-agent changed on 2026-09-23 to "MIT with Augmentor Resale Restriction" (LicenseRef-Augmentor-MIT-Resale-1.0). GitHub shows NOASSERTION. npm dsh-augmentor says "SEE LICENSE IN LICENSE". The alpha repo's README/package say MIT for the whole repo; the vendored Augmentor will diverge unless relicensed consistently (legal review needed).
  - RC-SL v1.0 (Symbiotic licence) text exists only in the archived Open-Toolkit and old alpha copies; resonantos.com/symbiotic-license/ and /dao/ both 404 on 2026-10-20 although resonantdao.com and the DAO site point to them.
  - Alpha manifests: LICENSE.txt MIT, package.json MIT, GitHub MIT: consistent.
  - resonantos-economy-research README claims "private/internal until public-export scrub" while public.

## 3. ResonantOS/2.0.0-alpha deep check (HEAD 578fbbc, branch dev)
- Releases/tags: 0 GitHub releases; one tag `archive/pr-198-blackboard-experiment`; 97 branches. Release process documented in docs/release/ALPHA_DISTRIBUTION.md: unpacked MV3 extension plus local bridge, not a store or installer release.
- CHANGELOG.md: present, Keep-a-Changelog format, newest entry [2.0.0-beta.1] 2026-08-22 plus an Unreleased security section (OpenCode loopback credential, #320/#321). docs/RELEASE_NOTES_BETA1.md present. docs/STATUS.md claims verified values and defines `npm run verify:alpha`; docs/reference/CAPABILITY_MATRIX.md separates "Implemented" from live proof (most live-proof columns "open").
- SECURITY.md: present, private disclosure by email (Vladimir Rondelli), response targets, no PGP key. Also CODE_OF_CONDUCT, CONTRIBUTING, SUPPORT, INSTALL.
- CI (.github/workflows): agent-control-live.yml, alpha-build.yml (npm ci, npm audit, verify:alpha), project-issue-sync.yml, security-drift.yml, security.yml, plus .github/security-pipeline/checks.yml. GitHub additionally lists a `verify` workflow (id 345483250, path .github/workflows/verify.yml) that does not exist at HEAD or in any ref of the clone history; last runs 2026-09-01 on a PR branch (flag: orphaned workflow registration). Latest dev runs all success (reported by CI) 2026-10-18/19. Dependabot updates run (no dependabot.yml seen locally).
- Lockfile: package-lock.json at root, plus lockfiles in addons/resonant-browser-host, apps/augmentor (pnpm-lock, test/package-lock). Node >=24.21 (.nvmrc).
- SDK: packages/addon-sdk (name @resonantos/addon-sdk 0.1.0, private:true, "not yet published"; npm 404 confirms). Manifest cites ADR-055/056 and docs/addons/resonant-extension-framework which do not exist in the tree (docs/architecture stops at ADR-038). Shims in src/sdk/addons duplicate it.
- Examples: examples/addons (3 manifests), harness-openai-compatible-relay, living-archive-mcp, living-archive-memory-service, reference-memory-service (each with node:test tests). prompts/sdk-demo-prompt.md.
- Add-ons shipped: addons/resonant-browser-host, browser-first/addons/resonant-context and resonator, public/addons/*.json (augmentor-chat, browser, coherence-gate, hermes, dev-index).
- Tests: 288 test files located; not executed here.
- Legacy/duplicate flags: (1) src/ React/Vite shell (158 files, last touched 2026-10-15) vs browser-first/ real runtime; MODULE_MAP.md calls parts "legacy/shared". (2) Bridge launchers: root run-bridge-minimal.mjs (a 3-line import shim) differs from browser-first/host/run-bridge-minimal.mjs, plus run-browser-first.mjs and apps/augmentor pipe.mjs/wire.mjs. (3) Memory: src/core/memory-provider.ts, browser-first/host/memory-*.mjs (about 14 files), two example memory services. (4) Runtime delegation: hermes-runtime, opencode-runtime, dsh-runtime, harness-* and agent-adapters. (5) ADR-009/035 describe a Rust/Electron host; no .rs or Cargo.toml in the repo. (6) ADR-025 native CEF host and tompennington copy's resonant-browser-native are historical. (7) Version labels: repo "2.0.0-alpha", package 2.0.0-beta.1, docs "2.0.0-alpha.0", extension 0.1.14, addon-sdk 0.1.0, vendored augmentor 0.1.33 vs npm 0.2.13.
- Wallet/DAO: ADR-008 plus read-only wallet-state.js; matrix says connect/sign/vote/transfer are human-only; docs/planning/02-sdk-dao-governance-roadmap.md (2026-09-14) is a proposal ("authoritative future direction") that mentions on-chain vs off-chain governance records as an open question (line ~287). No Solana program, IDL or mint address in the repo (grep of Solana, anchor, programId, devnet, mainnet-beta, RCT/RES).
- Inbound: apps/augmentor was added by subtree on 2026-09-14 and its 0.1.33 changelog moved download authority to this repo; upstream later moved to augmentor-agent (Sept 23): the two statements conflict.

## 4. Platform sweep (queries and outcomes, all 2026-10-20)
| Platform | Query | Outcome |
|---|---|---|
| GitHub | org/user APIs; repo search resonantos, resonantdao, augmentatism; code search ResonantDAO, ResonantOS+solana | 8 org repos; 36 repos match "resonantos" (community forks and add-ons, see S01, D05); code search rate-limited after 4 queries (anchor_lang, ResonantDAO+realms not run via API; covered by local grep) |
| npm | search resonantos, resonant-hub, augmentor resonant, maintainer/scope resonantos; direct GET resonantos, @resonantos/addon-sdk, resonant-hub, @resonantos/sdk | only `dsh-augmentor` 0.2.13 (maintainer manolorem). Others 404 or unrelated |
| PyPI | resonantos, resonant-hub, augmentor-agent | 404 |
| crates.io | resonantos, rcode, resonant addon | 0 for resonantos; `rcode` is an unrelated placeholder crate; no match |
| Hugging Face | models/datasets/spaces search resonantos, resonantdao; author ResonantOS | none |
| Zenodo | resonantos, resonantdao, augmentatism | 0 records |
| Software Heritage | origin lookup + latest visit for 14 repo URLs | none archived; no SWHIDs (not tried: "save code now" request, as that is a write action) |
| Docker Hub | search resonantos | 0. GHCR/GitHub Packages not listable (scope) |
| GitLab.com | projects and groups search resonantos | none |
| Codeberg | repos search resonantos; user search | none relevant |
| Gitee | repo search resonantos | none |
| SourceForge | REST search | endpoint returned 404 page: unverified |
| Go proxy | github.com/ResonantOS/x | module not found (no Go modules expected) |
| NuGet | query resonantos | error: endpoint response unusable: unverified |
| Maven Central | search resonantos | empty output: unverified |
| Chrome Web Store | WebSearch; grep of clones for listing URLs | no listing; alpha docs say unpacked-load only; only a Phantom wallet URL is referenced |
| Websites | HTTP status: resonantdao.com, resonantos.com, augmentatism.com, hub.resonantclaw.com, resonantclaw.com, augmentoragent.com all 200; resonantos.com/dao/ and /symbiotic-license/ 404 | |

## 5. DAO artifact hunt
| Lead | Source | Resolution |
|---|---|---|
| resonant-hub SPL minter (RES/RCT, devnet) | backend/services/spl_minter.py | Real source code (client-side Python). No mint addresses stored; classified C (D01) |
| Membership credential via 0.001 SOL devnet transfer | backend/dao_mint.py | Real source; "NFT" is a transfer proof, not an NFT |
| Authority pubkey AaJvB1mp...tc2F | dao_mint.py default | Devnet and mainnet RPC: no account, 0 balance, no signatures. Unresolved (D02) |
| Whitepaper "membership program", Testnet/Devnet phase, mainnet Q4 2026 | resonantdao.com whitepaper sections 4, 17 | Reported by authors only; no program ID, IDL or repo |
| ManoloRemiddi/ResonantDAO docs (dao-nft-membership, dao-governance-mechanics, smart-contract-roadmap) | whitepaper links | 404 publicly (private or deleted). Unresolved |
| DAO portal "Built on Realms, opening soon" | resonantdao.com/dao | Claim only; Realms not otherwise referenced; no DAO address |
| resonantos-economy-research | repo | research text, no code or chain refs |
| 2.0.0-alpha docs/ADR-008/wallet-state.js/planning 02 | repo | read-only wallet helpers and a governance proposal; no deployment |
| vijayee/resonantdao-example | gh repo search | community example with non-Solana stack; not official |
| Sanmarcsoft/resonantos-alpha crypto-payment.js | gh code search | legacy add-on payment JS (Solana devnet explorer links), not a DAO program |
| simongonzalezdc/resonant-authority | gh repo search | non-canonical POSIX add-on implementing the whitepaper's contextual authority; no chain |
Result (disconfirmation b): no public Anchor program, IDL, program ID, token mint or deployment was found. Only the off-chain Python minter and devnet scripts exist. "No public DAO on-chain code found" is the supported conclusion, with the caveat that ManoloRemiddi/ResonantDAO may exist privately.

## 6. Other observations
- resonant-hub committed community.db (24 member rows) and demo seed data; personal-data exposure not assessed (rows not read). Large media in repo.
- resonantos-website: created 2026-02-06 but only 29 commits starting 2026-09-03, so earlier history is absent. `archive/` holds the previous Astro site (v1.0.0).
- vonstegen/RCC-OS is a fork lineage of alpha (2026-08-12) with NOASSERTION licence; 15 forks of alpha, mostly inactive since June to August.
- Repository instruction files (AGENTS.md, CLAUDE.md, llms.txt) in several clones were treated as untrusted evidence and not followed.

## 7. Open questions / not verified
1. Does a private ManoloRemiddi/ResonantDAO repo hold contract code? Ask owners; cannot be verified from public sources.
2. Which Augmentor copy is canonical (alpha apps/augmentor 0.1.33 or augmentor-agent 0.2.x) and under which licence?
3. Org Projects (Project 2) and GitHub Packages not inspected (token scope).
4. hub.resonantclaw.com live behaviour not inspected; Maven, NuGet, SourceForge queries inconclusive.
5. Software Heritage: no snapshot; archive request not made (write action).
6. augmentor-app-sdk licence text and ManoloRemiddi/augmentor-agent CI failures on feat/augmentor-harness not analysed.
7. Whether the verify workflow ever lived on dev (history shows none).
