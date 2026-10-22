# Gap list: requirements for Stage 2 discovery (lead, 2026-10-20)

Status: approved unchanged by the user at Gate 1 on 2026-10-20 (state.md D1.1). The P0 set drives the Stage 3 shortlist. The DAO design documents cited by the whitepaper remain inaccessible and are treated as status F (D1.4); requirements that lean on them (R22-R26, R30) are evaluated against the whitepaper text alone.

Thirty concrete missing or weak capabilities, derived from the Stage 1 evidence at ResonantOS Alpha commit 578fbbc and the DAO sources fetched 2026-10-20. Each gap has a requirement ID, the Stage 1 evidence that establishes it (OSC rows from `capability-matrix.md`, DR rows from `dao-requirements.md`, T from `timeline.md`, C from `census-notes.md`, I from `interaction.md`), the constraints a candidate must satisfy, a testable discovery question, the Stage 2 branches that own it, and a priority: P0 (blocks the architecture decision or a security boundary), P1 (high value, needed for the roadmap), P2 (useful, can be deferred).

Standing constraints for every gap (from §9 of the master prompt and the project's own invariants): candidates must run locally on Windows, macOS and Linux or have a documented per-OS matrix; must not require a cloud service or telemetry; must be compatible with the MIT licence of the Alpha (flag copyleft and source-available licences for legal review); must preserve human-only actions, opt-in evidence, the option to run ResonantOS without the DAO, and no DAO credential becoming runtime authority (I2, DR-11).

Summary by priority: P0 = R01, R02, R03, R10, R11, R12, R14, R18, R19, R22, R23, R26, R29, R30 (14). P1 = R04, R05, R06, R07, R08, R13, R15, R20, R21, R24, R25, R27 (12). P2 = R09, R16, R17, R28 (4).

## Branch B: capability security, containment and restart

### R01 Per-principal, expiring, attenuable, revocable grants for a local bridge (P0)
Evidence: OSC-02 (26 static capability tokens for the process lifetime, all requested by one service worker), OSC-43 (no revocation except the OpenCode latch), OSC-44 (no expiry), OSC-45 (no attenuation, no principal identity in requests), OSC-46 (no multi-principal isolation); os-map section 17 seam 1.
Constraints: embeddable in a Node >= 24 process with no network service; keeps the existing route/capability vocabulary that 2424 tests lock; grants must be verifiable offline; revocation must take effect for in-flight sessions.
Question: Which proven open-source authorization system (object-capability tokens such as macaroons, Biscuit or UCAN, or an embeddable policy engine such as Cedar or OPA/Rego with a grant store) supports delegation with attenuation, expiry and mid-session revocation, runs inside a Node process, and has tests demonstrating that a revoked or attenuated grant is refused?
Branches: B (lead), A.

### R02 Cross-platform containment for delegated agent children (P0)
Evidence: OSC-32 (sandbox-exec on macOS only with allow-default profile; contract-only on Linux/Windows; live test skipped in CI), OSC-33 (persisted CLI-execution opt-in bypassable per request), OSC-34 (PATH passed to children; opencode serve spawned with full process.env), roadmap #326 open.
Constraints: child processes spawned from Node (Python Hermes, OpenCode server, DSH); filesystem, network and exec restriction; no root or admin required for the user; must degrade honestly (report "unconfined") where unavailable.
Question: Which proven sandboxing system (gVisor, Firecracker, bubblewrap, Landlock, seccomp profiles, Windows AppContainer or Job Objects, macOS seatbelt profiles, WebAssembly/WASI hosts such as Wasmtime or Extism) can confine a child process launched from Node on all three desktop OSes or with a documented per-OS matrix, and has tests or audits showing filesystem, network and exec escapes are blocked?
Branches: B (lead), E.

### R03 Secret brokering so children and add-ons never hold provider keys (P0)
Evidence: OSC-16 contradiction (provider key injected into Hermes/OpenCode child env, `addon-delegation-service.mjs:1770-1780`; DEEPSEEK_API_KEY forwarded to the DSH child, OSC-36), OSC-15/17 (routing only in the bridge), ADR-022 vault deferred.
Constraints: keys stay in one broker process; children get scoped, short-lived or proxied access; auditable per call; works for OpenAI-compatible HTTP APIs.
Question: Which proven system or pattern (local egress proxy that injects credentials, SPIFFE/SPIRE workload identity, Vault agent sidecar, secretless broker, OS keychain plus per-call approval) lets a local orchestrator give child processes model access without exposing the key, with an audit trail and tests?
Branches: B (lead), C.

### R04 Deterministic supervision, restart and known-good rollback for the core (P1)
Evidence: OSC-42 (no uncaughtException handlers; manual restart after crash; port fallback only), ADR-038 Guardian "not implemented", website claims "it comes back whole" (OSC-51), T discrepancy 4.
Constraints: no model in the loop; baseline hashes of installed versions and config; restart and rollback only, no capability authority; desktop footprint.
Question: Which proven supervisor or recovery system (Erlang/OTP-style supervision trees, s6, runit, systemd user units, launchd, Windows service wrappers, NixOS/ostree-style atomic rollback, Tauri/Electron updater rollback) provides health watch, restart and rollback to a hashed baseline for a local desktop service, and has tests for partial-failure recovery?
Branches: B (lead), C, H.

### R05 Loopback attack surface: unauthenticated proxy prefixes and local-process access (P1)
Evidence: OSC-05 (seven proxy prefixes on the bridge port need no token on loopback), OSC-04 (Origin not an authorization input for JSON routes; IP allowlist empty), OSC-06 (0600 meaningless on Windows; override tokens in chrome.storage.local), os-map 5.3 (bearer-over-plain-HTTP on LAN bind).
Constraints: must keep the Hermes dashboard iframe working or replace it; defend against other local processes and no-cors web requests; cross-platform.
Question: Which proven local-application security models (Chrome native messaging host pairing as used by KeePassXC-Browser, 1Password and Bitwarden; Jupyter/VS Code/Docker Desktop loopback token and origin binding; CSRF defences for localhost servers; Unix sockets and Windows named pipes with ACLs) close the localhost attack surface for an extension-to-bridge channel, and what evidence (CVEs, audits, tests) shows they work?
Branches: B, E.

## Branch A: agent interoperability and composition

### R06 MCP client and server wired into the bridge with user-approval gating (P1)
Evidence: OSC-48 (MCP is a standalone stdio example, not wired; no MCP client; ADR-029 deferred), website claim "we adopt MCP".
Constraints: TypeScript or Node; tool calls must pass the bridge's capability check and a human-approval checkpoint (R11); no cloud dependency; licence compatible.
Question: Which production MCP client and server implementations (official TypeScript SDK, FastMCP, mcp-proxy, gateway projects) support authorization, per-tool capability scoping and approval hooks, have integration tests, and how do existing hosts (Claude Desktop, VS Code, Cursor, Zed, Open WebUI) gate MCP tool execution behind user consent?
Branches: A (lead), E.

### R07 Neutral agent-runtime adapter with caller attribution and runtime swapping (P1)
Evidence: OSC-30 (three unrelated add-on systems), OSC-33/35/36 (bespoke runtime modules per agent: Hermes, OpenCode, DSH), harness adapter contract "governs nothing in a stock install", OSC-49 (A2A absent), planning/02 "caller attribution remains mandatory".
Constraints: typed interface; preserves originating principal through delegation; human intervention points; must wrap at least two existing runtimes without forking them.
Question: Which proven agent-interoperability layer or protocol (A2A, Agent Protocol, LangGraph, AutoGen, CrewAI, Mastra, OpenHands' agent interface, OpenClaw's gateway) lets an orchestrator swap agent runtimes behind typed interfaces with caller attribution and human intervention, and has integration tests across at least two runtimes that survive version upgrades?
Branches: A (lead), B.

### R08 Provider abstraction with native multi-vendor wire protocols and honest failover (P1)
Evidence: OSC-14 (all calls OpenAI-style; no retries; unresolvable model falls through to MiniMax with the MiniMax key), OSC-15 (Anthropic and Google presets without wire code), OSC-17 (manual selection errors instead of swapping), dev LAN address shipped in presets.
Constraints: local library, no hosted gateway requirement, no telemetry; Anthropic Messages and Gemini native formats; fallback with visible reasons; streaming; keys never leave the bridge.
Question: Which proven provider-routing library or gateway (LiteLLM, Vercel AI SDK provider packages, OpenRouter-compatible self-hosted gateways, Portkey gateway, Bifrost, llm-proxy projects) implements native Anthropic and Gemini wire formats, retries and fallback with reasons, runs embedded or locally without telemetry, and has tests for failover under injected faults?
Branches: A (lead).

### R09 Skill metadata and execution model (SKILL.md and equivalents) (P2)
Evidence: OSC-50 (template only; zero SKILL.md files), website claim.
Constraints: declarative; validated; executed under R01/R02 constraints; compatible with MCP tools.
Question: Which proven skill or plugin description formats and loaders (Agent Skills / SKILL.md implementations, Claude Code skills, OpenAI plugin manifests and their successors, Semantic Kernel plugins, LangChain tools) exist with schema validation and sandboxed execution, and which have been adopted by more than one runtime?
Branches: A.

## Branch C: durable execution and evidence

### R10 Durable job execution with checkpoint, replay and idempotent side effects (P0)
Evidence: OSC-21 (resume loses planner history; cooperative stop), OSC-22 (jobs become paused on panel load; state in chrome.storage.local), OSC-33 (cancel rewrites status without killing), OSC-42 (no supervised recovery), threat model "duplicate irreversible effects".
Constraints: embeddable in a local Node process or a sidecar with persistence under the user root; survives bridge and browser restarts; exactly-once or idempotency keys for browser mutations; no cloud.
Question: Which proven durable-execution engine or library (Temporal and its lite/dev-server mode, Inngest, Restate, DBOS Transact, Dapr workflows, SQLite-backed job queues, Effect workflows) can run embedded for a single-user desktop with checkpoint, replay, durable timers and idempotency, and has tests for recovery after a crash during an uncertain side effect?
Branches: C (lead), B.

### R11 Tamper-evident local audit ledger and host-side human-approval ledger (P0)
Evidence: OSC-47 (no route requires an approval proof; archive approval gate is a no-op; approvals are DOM heuristics), OSC-20 (public-submit regression counts as pass), ADR-022 `Logs/audit-ledger.jsonl` not implemented, os-map seam 3, interaction I3/I4/R-cand-5.
Constraints: append-only, hash-chained, user-readable, exportable; inclusion proofs; verifiable by the bridge before privileged routes execute; local-only by default.
Question: Which proven append-only or transparency-log components (Trillian, Sigstore Rekor patterns, immudb, Merkle-tree libraries, Git-object-based logs, Certificate Transparency libraries in JS/Go) fit a desktop footprint and allow a local service to require and verify an approval record before executing an action, with tests for tamper detection?
Branches: C (lead), B.

### R12 Provenance records with human/AI attribution and selective-disclosure claim packages (P0)
Evidence: harness host-signed receipts exist for one subsystem (T timeline 2026-09-21..10-18; code pointer to be confirmed in Stage 3), OSC-26 (provenance directory created empty), OSC-12 (research trail raw intake), DR-17 (human/AI split self-declared), DR-19 (no OS emitter; opt-in required), DR-50/51 (off-chain evidence, anchored roots), interaction S1 and T1-T3.
Constraints: TS library; off-chain verifiable; anchorable on Solana as a hash or root; expresses tool identity, session attribution and human/AI portions; supports commitments and redaction so a reviewer can verify what the user chose to disclose.
Question: Which proven attestation and provenance formats (in-toto attestations and SLSA provenance, W3C Verifiable Credentials with Data Integrity or SD-JWT selective disclosure, C2PA manifests, Sigstore bundles, DSSE envelopes, EAS off-chain attestations) can carry human/AI attribution and support selective disclosure with hash commitments, have maintained TypeScript implementations, and have been verified off-chain and anchored to a public chain in practice?
Branches: C (lead), F, G.

### R13 Crash-consistent local file state and corruption recovery (P1)
Evidence: OSC-28 (bare JSON.parse on settings and history makes every memory route throw; no fsync; no crash tests), OSC-23 (two-phase intake exists), os-map section 8.
Constraints: keep markdown and JSON human-readable under `~/ResonantOS_User`; atomic writes; recovery without data loss; Windows-safe rename semantics.
Question: Which proven local storage approaches (SQLite WAL as index with files as source of truth, LMDB, atomic-write libraries, journaling patterns, Automerge or Yjs persistence, Git-backed stores) provide atomic updates and corruption recovery for a file-based knowledge root, with tests simulating crashes and partial writes?
Branches: C, D.

## Branch D: memory, knowledge and sovereign local data

### R14 Staged knowledge promotion with source preservation, provenance and append-only history (P0)
Evidence: OSC-24 (promotion, draft and revise cannot execute; approval gate no-op; two independent promotion implementations), OSC-25 (domain separation is metadata only), OSC-26, ADR-007/012/013 targets (Human/External/AI separation, copy-on-import, version history), T discrepancy 8.
Constraints: local-first; source text never mixed with AI derivations; human review step that the host can verify (R11); versioned; exposable over MCP (R06); markdown-compatible.
Question: Which proven knowledge or memory systems (Letta/MemGPT, mem0, Khoj, Obsidian- and Logseq-compatible tooling, Dendron, Foam, Git-backed wikis such as Gollum, scientific provenance platforms such as Research Object Crate or DataLad, Zettelkasten tools) implement intake, review and promotion with append-only history and keep source material separate from AI-generated content, and which parts are reusable as libraries rather than applications?
Branches: D (lead), C.

### R15 Encrypted portable user-state root and secrets vault (P1)
Evidence: ADR-022 encrypted vault deferred; OSC-16 (keys in process memory or env; lost on restart), OSC-10 (chats plaintext in chrome.storage.local), user-data table in os-map section 10.
Constraints: cross-platform; portable folder the user can copy; OS keychain integration optional; recovery hints; no custodial service.
Question: Which proven local vault and encryption components (age/rage, libsodium sealed boxes, KeePassXC KDBX libraries, Bitwarden's open formats, OS keychain bindings such as keyring crates or Node bindings, filesystem encryption patterns) deliver a portable encrypted state root with key recovery on Windows, macOS and Linux, and have independent audits or tests?
Branches: D (lead), B.

### R16 Local-first sync and multi-device portability with selective sharing (P2)
Evidence: ADR-022 "copy this folder to a new computer"; OSC-40 (prefs only); interaction T1-T3 and I3.
Constraints: encrypted end to end; selective sharing of chosen artifacts; works offline; no mandatory relay.
Question: Which local-first sync systems (Automerge and automerge-repo, Yjs with y-sync providers, ElectricSQL, PowerSync, Evolu, Ditto, Syncthing as a transport) provide end-to-end encrypted selective sharing with a real security boundary rather than a relay that sees plaintext, and what do their threat models and tests show?
Branches: D.

### R17 Offline retrieval beyond substring search (P2)
Evidence: OSC-27 (case-insensitive substring scoring over markdown; no index or embeddings).
Constraints: fully offline; local embeddings optional; respects domain separation; small footprint.
Question: Which proven local search and retrieval engines (sqlite-vec, LanceDB, tantivy and its Node bindings, Chroma embedded, Orama, Vectra, FTS5) run offline in a Node desktop context with provenance-aware filtering, and what evidence exists for their quality on personal knowledge bases?
Branches: D.

## Branch E: desktop, browser, workbench and add-on ecosystem

### R18 Signed, hash-pinned add-on manifests with certification and revocation checks (P0)
Evidence: OSC-31 (manifests self-declare "signed" with no signature bytes or verifier), OSC-30 (grantedCapabilities literals never consulted), OSC-61 (install/uninstall UI deferred), ADR-023 registry and ADR-024 store, planning/02 certification object, interaction E4/E5/E10 and S2, I6.
Constraints: offline verification with cached revocation data; binds to id+version+hash; small ecosystem without a central server; revocation honoured across rollback (ADR-038); publisher identity.
Question: Which proven signing and update frameworks (The Update Framework and its JS implementations, Sigstore/cosign and its bundle verification in JS, npm provenance, Chrome CRX3 signing, VS Code marketplace signature verification, Obsidian and Firefox add-on review and signing pipelines) provide signed manifests with hash-pinned releases, certification metadata and revocation that a local host can verify offline, and have audits or tests for substitution attacks?
Branches: E (lead), B, F.

### R19 Host-enforced per-site permissions and approval ceremonies for browser agents, robust to prompt injection (P0)
Evidence: OSC-13 (modes enforced in one extension page; ask and trusted modes identical; blocked does not stop navigation; bypassable via tabs.sendMessage), OSC-18 (planner never exercised in tests), OSC-19 (English regex heuristics; links with commit words clickable), OSC-20 (regression counted as pass), os-map section 7.
Constraints: enforcement outside the DOM heuristics (host-side checkpoint, R11); per-action ceremony for ask mode; adversarial tests with injected page content; MV3-compatible.
Question: Which proven browser-agent frameworks or extension security patterns (browser-use, Playwright MCP, Stagehand, Nanobrowser, Chrome's permission and user-activation model, WebDriver BiDi, Microsoft's Magentic-UI, academic browser-agent safety benchmarks) enforce action gating at a trusted boundary rather than in page-side heuristics, include adversarial prompt-injection test suites, and report measured results?
Branches: E (lead), B, H.

### R20 Secure extension-to-native channel: native messaging versus loopback HTTP (P1)
Evidence: Alpha uses loopback HTTP with bearer tokens (OSC-02, OSC-05); `apps/augmentor` uses nativeMessaging (OSC-59); generated config written into the extension source tree (os-map section 4); T lineage 2b.
Constraints: Chrome MV3; pairing and origin binding; works on Windows; no plaintext secrets on disk.
Question: What is the evidence (audits, CVEs, design docs, tests) comparing Chrome native messaging hosts with loopback HTTP servers for extension-to-local-bridge channels, and which open-source implementations (KeePassXC-Browser, Bitwarden, 1Password's documented model, Tailscale or Docker Desktop local APIs) model pairing, origin binding and secret storage well enough to reuse?
Branches: E (lead), B.

### R21 Isolation model for in-browser and in-process add-ons (P1)
Evidence: OSC-30 (extension "add-ons" are content scripts with full extension privileges; three schemas), OSC-01 (content scripts in all frames of all sites), ADR-006 SDK, planning/02 capability classes.
Constraints: capability-scoped API; third-party code never shares the extension's privileges; MV3 constraints on eval and remote code; cross-platform.
Question: Which proven plugin architectures isolate third-party code inside an extension or desktop app with capability-scoped APIs (sandboxed iframes with postMessage brokers, WebAssembly plugins via Extism or Wasmtime, VS Code's extension host process, Figma and Obsidian plugin sandboxes, Deno permissions, Chrome's own sandboxed pages), and what evidence shows escapes are blocked?
Branches: E (lead), B.

## Branch F: DAO execution, membership and credentials

### R22 Non-transferable wallet-bound credentials on Solana with issuer revocation and governed recovery (P0)
Evidence: DR-01 (legacy devnet NFTs are Token-2022 NonTransferable; hub minter never freezes), DR-02 (member record is the source of truth; no program source), DR-06 (no revocation for human credentials), DR-07/08 (no recovery or freeze), DR-10 (caps), census D01-D03 (no official program, IDL or mint).
Constraints: Solana target as stated by the whitepaper (flag if a candidate is EVM-only); revocation and re-binding without transferability; privacy of membership (DR-09); audited code.
Question: Which proven Solana programs and standards (Token-2022 NonTransferable with permanent delegate or burn paths, Metaplex Core and Bubblegum soulbound patterns, Solana Attestation Service, Civic Pass, Light Protocol compressed accounts, Underdog or other credential issuers) implement non-transferable credentials with issuer revocation and governed re-binding to a new wallet, have audits, and are maintained?
Branches: F (lead), G.

### R23 Proof of key control and an off-chain membership and claim registry with anchored commitments (P0)
Evidence: DR-05 (hub registers a bare wallet string), DR-03 (Manifesto has no published hash), DR-50/51 (off-chain ledger with anchored roots; evidence never on-chain), DR-02, Phase 1 core items 1-2.
Constraints: Solana-compatible signatures; off-chain registry with periodic Merkle roots; privacy by default; inclusion proofs for members; small-team operability.
Question: Which proven systems (Sign-In-With-Solana and SIWE-style challenge signing, W3C Verifiable Credentials and DIDs, OpenAttestation, EAS off-chain attestations and their Solana ports, Ceramic/ComposeDB, Merkle-anchoring services) deliver proof of key control plus an off-chain registry whose roots are anchored on Solana, and have tests and deployments showing inclusion proofs and revocation?
Branches: F (lead), C, H.

### R24 Solana governance with custom voter weights, multisig-timelocked authorities and custodian transition (P1)
Evidence: DR-43 (contextual weight function undefined), DR-46 (custodian transition has no triggers), DR-47 (emergency powers absent), DR-48 (devnet program and mints controlled by single keys), DR-49, I-11 (two governance systems).
Constraints: Solana (flag EVM-only designs as patterns); voter-weight plugins; timelocks; audited; off-chain advisory voting acceptable in Phase 1 (DR-43 replay).
Question: Which proven governance stacks on Solana (Realms/spl-governance with voter-weight plugins, Squads multisig and timelocks, MetaDAO futarchy, Tribeca) and which cross-chain patterns (Aragon OSx, DAO DAO, Snapshot strategies, Hats Protocol roles, Safe/Zodiac modules) support dimension-weighted voting, multisig-timelocked upgrade and mint authorities, and staged custodian-to-community transition, and which have audits and documented failures?
Branches: F (lead), G, H.

### R25 Human-versus-agent membership and per-right Sybil resistance (P1)
Evidence: DR-12 to DR-18 (sponsor link, no per-sponsor cap, self-declared human/AI split, human registration flow undefined, no per-vote presence check), I-17.
Constraints: no centralised KYC where possible (whitepaper); per-right assurance levels; published false-reject data; Solana-compatible or chain-agnostic; accessibility.
Question: Which proven identity and personhood systems (Human Passport, BrightID, Proof of Humanity, Idena, World ID, Civic Pass, Gitcoin Passport scoring, Hats Protocol eligibility modules) provide per-right assurance with published error rates and anti-collusion properties, which run on Solana, and what is documented about agent farming and sponsorship abuse?
Branches: F (lead), G.

## Branch G: contribution accounting and community funding

### R26 Outcome-based multi-dimensional contribution ledger with explanation records, review tiers and appeals (P0)
Evidence: DR-20 to DR-28 (all D), DR-35/36 (non-conflation), I-1/I-4 (contradictory definitions of contribution), Phase 1 core items 2-4, no official implementation (dao-requirements summary 7).
Constraints: off-chain first; append-only with reversible corrections; null distinct from zero; five separated events; reproducible from record plus calibration version; small-community review capacity.
Question: Which proven contribution-accounting systems (SourceCred, Coordinape, Praise, Colony reputation, Karma3 OpenRank, Hypercerts, Optimism RetroPGF tooling, Drips, Gitcoin grants stack, scholarly peer-review and credit systems such as CRediT) implement evidence-based multi-dimensional credit with review and appeal, what did they document about farming, capture and burnout, and which components are reusable off-chain?
Branches: G (lead), F.

### R27 Collusion and farming resistance, reviewer independence and bounded appeals (P1)
Evidence: DR-13 (no per-sponsor agent cap), DR-24/25 (reviewer independence and reviewer credit tension), DR-26 (appeal flooding), DR-29 (collusion rings), DR-60 (operators gain weight over the rules), unaddressed attacks list in dao-requirements section 7.
Constraints: small volunteer community; explainable; low burden; privacy-preserving where possible.
Question: Which proven mechanisms and tools (pairwise-bounded or cluster-matched quadratic funding, MACI private voting, collusion-resistant peer prediction, Sybil detection used by Gitcoin Passport, reviewer assignment with conflict constraints as in conference systems such as OpenReview, reputation decay models) have code and published evaluations showing reduced collusion or farming, and at what cost in burden and false positives?
Branches: G (lead), H.

### R28 Attribution chains with governed decay (P2)
Evidence: DR-30 (chain settlement along informed-by links; stuffing risk acknowledged), interaction E3.
Constraints: reviewable links; self-link prohibition; bounded depth; explainable.
Question: Which proven credit-flow systems (SourceCred cred flow, Drips dependency splits, tea.xyz, Open Source Collective dependency funding, academic citation-credit models) implement upstream attribution with decay, and how were they gamed or abandoned?
Branches: G.

## Branch H: contrarian and minimalist architecture

### R29 Thin integration layer versus bespoke runtime (P0)
Evidence: os-map section 16-17 (duplicate implementations; four seams), OSC-58/59 (parallel dev app and vendored unrelated extension), census licence conflict (augmentor upstream relicensed), T generations hypothesis, planning/02 "Augmentor de-fused".
Constraints: must keep the Alpha's working features (OSC A/B rows) and the human-only boundaries; MIT-compatible; local-first; evaluate what would be lost.
Question: Which existing open-source extensible agent runtimes or workbenches (OpenClaw, Open WebUI, LibreChat, Jan, AnythingLLM, Continue, Cline, Nanobrowser, browser-use, Mastra, Goose) already deliver the Alpha's working feature set with equal or better isolation and provider neutrality, such that ResonantOS could become an integration layer plus the components no one else builds, and what evidence shows where each fails the sovereignty, containment and human-only requirements?
Branches: H (lead), A, E.

### R30 Off-chain Phase 1 for the DAO with periodic anchoring and no tokens (P0)
Evidence: dao-requirements section 5 (feasible core), DR-51, DR-56, economy-research "block bounty-first design", I-2/I-8 (on-chain claims versus ledger-first; mainnet target with no artifact), census (no official chain code).
Constraints: membership, claim ledger, advisory votes and treasury transparency without minting tokens; anchoring to Solana later; auditable by members; operable by a small team.
Question: Which proven off-chain governance and record systems (Loomio, Decidim, Open Collective and Open Source Collective, Git-based governance such as the Rust RFC or Apache processes, transparency logs such as Rekor, OpenAttestation-style anchoring) deliver membership, contribution records and advisory voting with public auditability, and what exactly would an on-chain layer add that these cannot, as evidenced by their documented limits?
Branches: H (lead), F, G.

### Standing task for Branch H: counterexample hunt
For every leading candidate surfaced by branches A-G, find evidence that it is abandoned, insecure by default, functionally proprietary (open core with the needed part closed), too complex for a small team, or has had a compromise or incentive attack. Record each in the negative ledger with the source.

## Notes for the term-bank agents
Core concepts needing native-language terms (per §5): capability token / object capability; attenuation; revocation; sandbox / containment; durable execution / workflow engine; event sourcing / audit log; provenance / attestation; selective disclosure; local-first; soulbound / non-transferable token; DAO governance; quadratic funding / collusion resistance; reputation; agent framework / multi-agent; browser automation / extension security; MCP.
