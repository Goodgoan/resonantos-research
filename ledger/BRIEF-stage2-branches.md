# Stage 2 branch-specific briefs (lead, 2026-10-20)

Each branch agent reads `BRIEF-stage2-common.md` first, then its own section here. "Owns" means the requirement where this branch is the lead searcher; "supports" means a requirement another branch leads where this branch must also contribute candidates from its own angle. Seed leads are search hypotheses, not endorsements; verify present status.

## Branch A: agent interoperability and composition (agent id s2-br-a)

Owns R06 (MCP client and server wired with approval gating), R07 (neutral agent-runtime adapter with caller attribution), R08 (provider abstraction with native multi-vendor wire protocols and honest failover), R09 (skill metadata and execution model). Supports R01 (how do agent runtimes model per-principal grants), R29 (which existing runtimes already deliver the Alpha's feature set; feed Branch H).

Seed leads: official MCP TypeScript SDK and the MCP authorization spec, FastMCP, mcp-proxy and MCP gateway projects, how Claude Desktop, VS Code, Cursor, Zed and Open WebUI gate tool execution behind consent; A2A, Agent Protocol, LangGraph, AutoGen, CrewAI, Mastra, OpenHands agent interface, OpenClaw gateway, Goose; LiteLLM, Vercel AI SDK provider packages, Portkey gateway, Bifrost, OpenRouter-compatible self-hosted gateways; Agent Skills / SKILL.md implementations, Semantic Kernel plugins, LangChain tools, OpenAI plugin manifests and successors.

Angle: the Alpha is Node 24 and TypeScript-adjacent; prefer TypeScript or embeddable components, but record Python and Go systems whose interface could be wrapped. For every runtime record whether a human-intervention point exists at the tool-call boundary and whether originating principal survives delegation. For provider routers record whether Anthropic Messages and Gemini native wire formats are implemented (not just OpenAI-compatible proxying), whether retries and fallback are visible to the caller, and whether telemetry is on by default.

## Branch B: capability security, containment and restart (agent id s2-br-b)

Owns R01 (per-principal expiring attenuable revocable grants), R02 (cross-platform containment for child processes), R03 (secret brokering), R04 (deterministic supervision, restart, known-good rollback), R05 (loopback attack surface). Supports R07, R10, R11, R15, R18, R19, R20, R21 from the security angle.

Seed leads: macaroons (libmacaroons and TS ports), Biscuit (biscuit-auth, Rust and JS), UCAN (ucanto, ucans), Cedar (cedar-policy, WASM build), Open Policy Agent (opa-wasm), Casbin, Zanzibar-style systems (SpiceDB, OpenFGA, Ory Keto), capability-based OS research (CHERI, seL4, Capsicum, Fuchsia, Pony, E, Cap'n Proto RPC capabilities), Agoric SES and Endo (hardened JavaScript compartments); gVisor, Firecracker, bubblewrap, Landlock, seccomp, Windows AppContainer and Job Objects, macOS sandbox-exec and App Sandbox, Wasmtime, WASI, Extism, Deno permissions, nsjail, minijail, Sandboxie; SPIFFE/SPIRE, Vault agent, Secretless Broker, Infisical, 1Password CLI and op connect, OS keychains, local egress proxies that inject credentials (e.g. mitmproxy patterns, Envoy with credential injection); Erlang/OTP supervisors, s6, runit, systemd user units, launchd, WinSW, NSSM, Tauri and Electron updaters with rollback, ostree, Nix generations; KeePassXC-Browser native messaging, Bitwarden, 1Password browser integration, Jupyter and VS Code loopback token binding, Docker Desktop local API, CSRF and DNS-rebinding defences for localhost servers.

Angle: for every candidate record the per-OS matrix (Windows, macOS, Linux) explicitly; "Linux only" is a fact, not a disqualifier, but it must be stated. Record whether revocation can take effect mid-session (R01) and whether a confined child can still reach a local HTTP port (R02). For R04 non-AI infrastructure counts fully.

## Branch C: durable execution and evidence (agent id s2-br-c)

Owns R10 (durable execution with checkpoint, replay, idempotent side effects), R11 (tamper-evident local audit ledger and host-side approval ledger), R12 (provenance records with human/AI attribution and selective disclosure). Supports R03, R13, R14, R23 from the evidence angle.

Seed leads: Temporal (incl. dev server and TypeScript SDK), Inngest, Restate, DBOS Transact, Dapr workflows, Effect workflows, BullMQ and SQLite-backed queues, Graphile Worker, Hatchet, Windmill; event sourcing libraries, outbox patterns, saga libraries; Trillian, Sigstore Rekor and its transparency-log library, immudb, Certificate Transparency libraries, Merkle tree libraries in TS and Go, Git-object-based append-only logs, QLDB-style verifiable ledgers, Hypercore; in-toto attestations and SLSA provenance, DSSE, Sigstore bundles and sigstore-js, W3C Verifiable Credentials with Data Integrity, SD-JWT and SD-JWT VC, BBS+ signatures, C2PA (c2pa-rs, c2pa-node), EAS off-chain attestations, OpenAttestation, Research Object Crate, PROV-O and PROV-JSON.

Angle: desktop footprint and embedded or single-process mode are the filter for R10 and R11; a server-only product is a `lead` for the pattern, not a `candidate`. For R12 record for each format whether it can express human versus AI authorship and tool identity, whether selective disclosure is native or bolted on, whether a maintained TypeScript implementation exists, and any case of off-chain verification plus public-chain anchoring in practice. Non-AI infrastructure counts fully.

## Branch D: memory, knowledge and sovereign local data (agent id s2-br-d)

Owns R14 (staged knowledge promotion with source preservation and append-only history), R15 (encrypted portable user-state root and secrets vault), R16 (local-first sync with selective sharing), R17 (offline retrieval). Supports R12, R13 from the data angle.

Seed leads: Letta/MemGPT, mem0, Khoj, Zep, Cognee, Obsidian and Logseq ecosystems, Dendron, Foam, Gollum, DataLad, git-annex, Research Object Crate, Zettelkasten tooling, LLM-wiki patterns; age/rage, libsodium, KDBX libraries, Bitwarden open formats, keyring crates and Node keychain bindings, gocryptfs and Cryptomator, SQLCipher; Automerge and automerge-repo, Yjs and y-sync providers, ElectricSQL, PowerSync, Evolu, Ditto, Syncthing, Loro, Jazz, Fireproof, TinyBase; sqlite-vec, LanceDB, tantivy and node bindings, Chroma embedded, Orama, Vectra, FTS5, Qdrant embedded.

Angle: check real security boundaries; a vector database does not solve privacy and a sync relay that sees plaintext is not end-to-end encrypted. For R14 distinguish reusable libraries from applications and record whether source material is kept separate from AI-generated derivations and whether a human review step is verifiable by a host. For R15 record audits and key-recovery design.

## Branch E: desktop, browser, workbench and add-on ecosystem (agent id s2-br-e)

Owns R18 (signed hash-pinned add-on manifests with certification and revocation), R19 (host-enforced per-site permissions and approval ceremonies for browser agents, robust to prompt injection), R20 (extension-to-native channel: native messaging versus loopback HTTP), R21 (isolation model for in-browser and in-process add-ons). Supports R02, R05, R06, R29.

Seed leads: The Update Framework (tuf-js, python-tuf), Sigstore and cosign bundle verification in JS, npm provenance and SLSA, Chrome CRX3 signing, VS Code marketplace signing, Firefox add-on signing and review (AMO), Obsidian plugin review, Raycast and Alfred extension stores; browser-use, Playwright MCP, Stagehand, Nanobrowser, Browserbase, Magentic-UI, Skyvern, Chrome's permission and user-activation model, WebDriver BiDi, browser-agent safety benchmarks (e.g. WebArena/ST-WebAgentBench/AgentDojo, InjecAgent, BrowserART), OWASP guidance on prompt injection; KeePassXC-Browser, Bitwarden, 1Password native messaging designs, CVEs on native messaging and localhost servers; sandboxed iframes with postMessage brokers, Extism, Wasmtime, VS Code extension host, Figma plugin sandbox (Realms/QuickJS), Obsidian plugin model, Deno permissions, Chrome sandboxed pages.

Angle: enforcement location is the question. For every browser-agent candidate record where the gate lives (page-side heuristics, extension service worker, native host, or separate process), whether adversarial injection tests exist and their measured results, and MV3 compatibility. For R18 record whether verification works offline with cached revocation data and whether it binds id, version and hash.

## Branch F: DAO execution, membership and credentials (agent id s2-br-f)

Owns R22 (non-transferable wallet-bound credentials on Solana with revocation and governed recovery), R23 (proof of key control and off-chain membership registry with anchored commitments), R24 (Solana governance with custom voter weights, multisig-timelocked authorities, custodian transition), R25 (human-versus-agent membership and per-right Sybil resistance). Supports R12, R26, R30.

Seed leads: Token-2022 extensions (NonTransferable, PermanentDelegate), Metaplex Core and Bubblegum, Solana Attestation Service, Civic Pass, Light Protocol, Underdog, Dialect, Sign-In-With-Solana, SIWE, W3C VC and DID methods on Solana (did:sol), OpenAttestation, EAS and Solana ports, Ceramic/ComposeDB, Merkle anchoring services; Realms/spl-governance and voter-weight plugins, Squads, MetaDAO, Tribeca, Marinade governance; Aragon OSx, DAO DAO, Snapshot strategies, Hats Protocol, Safe/Zodiac (as patterns, flagged EVM); Human Passport (Gitcoin Passport), BrightID, Proof of Humanity, Idena, World ID, Civic.

Angle: chain compatibility is mandatory in `notes` (`chain: solana|evm|agnostic|none`); an EVM-only system is a `lead` for the pattern unless a Solana port exists. Record audit reports with dates and firms, upgrade-authority design, and whether anything is deployed on mainnet versus devnet. For R25 record published false-reject or error rates and documented sponsorship or agent-farming abuse.

## Branch G: contribution accounting and community funding (agent id s2-br-g)

Owns R26 (outcome-based multi-dimensional contribution ledger with explanations, review tiers, appeals), R27 (collusion and farming resistance, reviewer independence, bounded appeals), R28 (attribution chains with governed decay). Supports R12, R23, R30.

Seed leads: SourceCred, Coordinape, Praise, Colony reputation, Karma3 OpenRank, Hypercerts, Optimism RetroPGF tooling and retrospectives, Drips, Gitcoin grants stack and Allo, Giveth, clr.fund, MACI, pairwise-bounded and cluster-matched QF papers and code, peer-prediction mechanisms, OpenReview and conference reviewer-assignment code, CRediT taxonomy tooling, tea.xyz, Open Source Collective, Thanks.dev, academic citation-credit models; documented failures and retrospectives (SourceCred's wind-down, RetroPGF rounds analyses, Gitcoin Sybil reports).

Angle: documented failures and incentive attacks are first-class findings; a post-mortem is as valuable as a repository. For each system record what it did about farming, capture and burnout, and which components are reusable off-chain by a small volunteer community. Record `chain:` in notes as Branch F does.

## Branch H: contrarian and minimalist architecture (agent id s2-br-h)

Owns R29 (thin integration layer versus bespoke runtime) and R30 (off-chain Phase 1 for the DAO with periodic anchoring and no tokens). Owns the counterexample hunt for every branch.

Seed leads for R29: OpenClaw, Open WebUI, LibreChat, Jan, AnythingLLM, Continue, Cline, Nanobrowser, browser-use, Mastra, Goose, LobeChat, Msty, Cherry Studio, Dify, Flowise, n8n. For each: does it already deliver the Alpha's working feature set (chat through OpenAI-compatible providers with routing and fallback, page context and inline assistant, workspaces, browser click/type/scroll, memory intake with versioning, delegation to external agents, diagnostics, preferences) with equal or better isolation and provider neutrality, and where does it fail sovereignty, containment and human-only requirements? Read `stage1\capability-matrix.md` rows A and B for the feature set.

Seed leads for R30: Loomio, Decidim, Open Collective and Open Source Collective, Git-based governance (Rust RFC process, Apache voting, Python PEP), transparency logs (Rekor) and OpenAttestation-style anchoring, Snapshot off-chain voting with on-chain anchoring, Gov4Git, Hypha DAO's off-chain components. Ask what an on-chain layer adds that these cannot, using their documented limits.

Counterexample hunt: pass 1 runs on the seed leads of all branches (BRIEF-stage2-branches.md, every section) because the other branches' ledgers do not exist yet; the lead will send you the actual candidate list in pass 2. For each, look for: abandonment, insecure defaults, CVEs and advisories, functional proprietary-ness (open core), complexity unsuited to a small team, compromises and incentive attacks. Record each as `disposition: counterexample`, `notes` starting `against: <url>`, with the source.

## JA/KO probe (agent id s2-probe-jako)

Purpose (master prompt section 5.6): a cheap tripwire that decides whether full Japanese or Korean language agents are worth their cost. Scope: the eight highest-priority requirements R01, R02, R10, R11, R12, R14, R19, R22 (P0 set, chosen for breadth across branches).

Task: (1) build a mini term bank for those eight requirements in Japanese and Korean using practitioner vocabulary verified in real repositories or articles, written to `glossary\ja-ko-probe.md` (same table shapes as the other glossary files, plus a Decision section). (2) Japanese: search GitHub with Japanese terms (`gh api search/repositories`), Qiita (`https://qiita.com/api/v2/items?query=TERM`), Zenn (`https://zenn.dev/search?q=TERM`), J-STAGE (`https://www.jstage.jst.go.jp/result/global/-char/ja?globalSearchKey=TERM`). Korean: GitHub with Korean terms, KCI (`https://www.kci.go.kr/kciportal/po/search/poArtiSearList.kci`; record the working query shape). Treat blog posts as leads to code, not evidence. (3) Record every search in your ledgers. (4) Decide per language: the tripwire fires when two or more relevant, independent leads point to real code that is not obviously already findable in English (a project with an English README on GitHub does not count). Write the decision and its evidence in the glossary file's Decision section and in your return message. Time box about 60-100 tool calls.
