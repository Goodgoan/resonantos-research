# ResonantOS 2.0.0 Alpha — Legacy layers, test lanes, CI, module ownership, restartability

- Repo: `research/_untrusted/resonantos-2.0.0-alpha` @ `578fbbc3c1c854b192318b3d2163b138fb45d8bd` (branch `dev`, merge of PR #534, 2026-10-18)
- Verified: 2026-10-20, static reading only (file reads, grep, `git log`). Nothing executed.
- Labels used below: **[inspected]** = what the code does; **[reported]** = what the authors' docs say; **[hypothesis]** = my inference. Confidence high/medium/low per claim.
- LOC counts are `wc -l` over `*.ts,*.tsx,*.js,*.mjs` only (no css/md/html), so they differ from the brief's figures.

## Summary

1. The Alpha runtime is exactly the Chrome MV3 extension (`browser-first/resonantos-side-panel-extension/`, 33.6k LOC) plus the Node bridge (`browser-first/host/`, 22.2k LOC). The extension imports nothing from `src/`, `packages/` or `apps/` (grep over extension `src/`, zero hits) **[inspected, high]**. The host imports exactly two files from the TypeScript tree (`packages/addon-sdk/src/contracts.ts`, `validation.ts` via `browser-first/host/harness-adapter-contract.mjs:3-4`) **[inspected, high]**.
2. `src/` (React 19 + Vite dev page at 127.0.0.1:1430, 16.1k core + 28.6k modules + 1.4k sdk LOC) is a parallel, dev-only client of the *same* bridge. It carries its own second bridge client (`src/core/web-transport.ts`), a second provider catalog/routing layer, a second memory broker, and a Tauri-era command vocabulary of which only 16 commands are routable; everything else throws "not available in the browser-first Chrome extension alpha" (`src/core/web-transport.ts:134-137`) **[inspected, high]**. Authors agree it is "supporting source", "not an Alpha entrypoint" (`docs/architecture/MODULE_MAP.md:70-80`; `ALPHA_RUNTIME_BOUNDARY.md:140-151`) **[reported]**.
3. `apps/augmentor/` (12.5k LOC) is a *third*, unrelated MV3 extension ("Augmentor Agent powered by DSH" 0.1.33, `nativeMessaging` + a native-messaging host `pipe.mjs` + a DSH plugin), vendored by git subtree on 2026-09-14 (`5550432`). It is not mentioned in the Alpha boundary doc, the module map, or the ownership contract, and none of its 14 test/e2e files are run by any root npm script or workflow **[inspected, high]**.
4. Development activity since 2026-07-01: `browser-first/` 304 commits vs `src/` 38 (since 2026-09-01: 196 vs 33). Every `src/` commit since 2026-09-23 is `feat(harness)` work wiring the React shell to the bridge's `/addons/*` and `/agent/*` routes **[inspected, high]**.
5. Test lanes: 206 `node --test` files in `browser-first/test/` (top-level only; `*.live.mjs`, helpers and two `*/run-certification.mjs` subdir scripts excluded), 48 vitest files in `src/`, 13 `scripts/*.test.mjs` (12 wired), 10 security-pipeline tests, 3 `examples` tests (2 wired), 2 browser-host tests, 6+8 augmentor tests (0 wired). No `describe.skip/it.skip/.only/todo` anywhere; 13 runtime `t.skip` sites, all environment-conditional **[inspected, high]**.
6. "Strict security certification" (`run-check.mjs --certify`) requires 7 registry checks to return `pass` with no `skipped`/`warn`. Only `subprocess-no-shell-string` and `committed-private-key-material` scan actual source text; the four runtime-hardening checks score hand-written spawn *records* in `.github/security-pipeline/checks.yml`, not the code (a test only asserts the records' source anchors still exist). Verdict: a lint/documentation gate with one real heuristic static scanner, not a security test **[inspected, high]**.
7. Restartability: no `uncaughtException`/`unhandledRejection` handlers in the host; SIGINT/SIGTERM run an ordered drain then `exit(0)`; port falls back to an ephemeral port on `EADDRINUSE`; tokens are regenerated on every start and rewritten into the unpacked extension's `src/bridge-config.generated.js`. The extension has no alarms/reconnect loop, but on a 401 it re-fetches the generated config with cache busting, re-mints capability tokens and retries once, so a same-machine unpacked install re-bootstraps without user action. A remote/override target keeps its stored token and needs the user to re-enter it after a token-rotating restart **[inspected, high; override consequence medium]**.
8. Drift flags: `package.json` is named `resonantos-vnext` version `2.0.0-beta.1` while docs call this the 2.0.0 Alpha; `prompts/sdk-demo-prompt.md` tells agents to run `examples/sdk-prototype/...`, a path that does not exist in the checkout **[inspected, high]**.

## Role of each non-extension surface

| Path | What it is | Alpha runtime? | Evidence (file:line) | Activity (commits since 2026-07-01 / last) |
| --- | --- | --- | --- | --- |
| `index.html` + `src/main.tsx` + `src/App.tsx` | Vite entry for the React 19 "ResonantOS vNext" shell; CSP allows `connect-src http://127.0.0.1:* ws://127.0.0.1:*`. Not in the shipped zip (zip is only the extension dir). | No — dev page | `index.html:7,14`; `.github/workflows/alpha-build.yml:54-56`; `MODULE_MAP.md:76` ("Not an Alpha entrypoint") | `src/`: 38 / 2026-10-15 |
| `vite.config.ts` | Dev server pinned to 127.0.0.1:1430 strictPort, `fs.strict`, denies `bridge-config.generated.js`; mounts `devBridgeConfigPlugin()`; vitest `include: src/**/*.test.ts(x)` only | No — dev/test tooling | `vite.config.ts:7,32-54`; `src/dev-server-policy.ts:3` | part of root |
| `scripts/vite-dev-bridge-config.mjs` | Opt-in authenticated delivery of the bridge's generated config to the dev page (`/__resonantos_dev_bridge__/config.mjs`, Basic-auth page key, nonces, loopback-only) | No — dev tooling | `scripts/vite-dev-bridge-config.mjs:16-33`; `docs/STATUS.md:138-147` | scripts: 107 / 2026-10-07 |
| `src/core/` (16,113 LOC, 18 non-test files) | Shared TS contracts, provider/memory/compute/delegation policy, UI-state hydration, and the React-side bridge transport. Each file opens with an "Intent citation" to an ADR. | No — "supporting source; not a separate runtime process" | `MODULE_MAP.md:72`; file list below | included above |
| `src/modules/` (28,577 LOC, 15 dirs) | React workspaces: addons, archive, browser, chat, compute, delegation, hermes, obsidian, opencode, overview, paperclip, recovery, settings, shell, strategist | No — "feature reservoir ... not the MV3 Alpha UI unless explicitly imported by the extension" (it is not) | `MODULE_MAP.md:75`; zero extension imports (grep) | included above |
| `src/sdk/addons/` (1,400 LOC incl. tests) | Five one-line re-export shims to `packages/addon-sdk/src/*` plus their vitest files | Indirectly — host imports the canonical `packages/addon-sdk` contracts/validation | `src/sdk/addons/{contracts,index,registry,surface-routing,validation}.ts:7`; `browser-first/host/harness-adapter-contract.mjs:3-4` | packages: 8 / 2026-10-17 |
| `apps/augmentor/` (12,519 LOC) | Separate product: MV3 extension `extension/` (manifest v0.1.33, permissions incl. `nativeMessaging`), native messaging host `pipe.mjs`, DSH plugin `plugin/`, installer `install-native-host.sh`, own `package.json` (`augmentor` 0.1.0, deps `ws`, `fflate`), own AGENTS.md with mandatory MIT header rule (author Manolo Remiddi). Vendored via `git subtree` 2026-09-14. | No — and undocumented in boundary/map/ownership docs; only `browser-first-release-scope-audit.mjs:234` knows the path | `apps/augmentor/README.md:1-45`; `apps/augmentor/extension/manifest.json`; `apps/augmentor/package.json`; commit `5550432` | 7 / 2026-10-06 (dependabot + small fixes) |
| `scripts/engineer-runner.mjs` | "Deterministic guardrails around local coding agents": loads a task-contract JSON (`repo`, `goal`, `allowedFiles`, `requiredCommands`), `prompt` prints an OpenCode prompt, `verify` runs required commands via `spawnSync` argv and checks changed-file scope | No — dev tooling; its unit test is in `verify:alpha` | `scripts/engineer-runner.mjs:1-7,139,228,281-282`; `package.json` scripts `engineer:*`, `test:engineer-runner` | scripts: see above |
| `disciplines/` | Process-governance catalog: `DISCIPLINES.md` (1 row: `development-package-promotion-gate`) + 1 card; validated by `scripts/validate-discipline-catalog.mjs` (`npm run discipline:validate`, **not** in `verify:alpha`) | No — docs | `disciplines/README.md:1-30`; `disciplines/DISCIPLINES.md:10-13`; `scripts/verify-alpha.mjs:10-38` (absent) | 1 / 2026-07-10 |
| `prompts/` | One file, `sdk-demo-prompt.md`: an agent prompt (Codex/DSH/oh-my-pi) to "verify, present, build" an SDK demo at `examples/sdk-prototype/` — **that directory does not exist** in this checkout | No — stale doc | `prompts/sdk-demo-prompt.md:1-30`; `ls examples/` (no `sdk-prototype`) | 3 / 2026-09-20 |
| `run-bridge-minimal.mjs` (root) | 3-line shim: `import "./browser-first/host/run-bridge-minimal.mjs"` | Yes — launcher entry for `npm run browser-first:bridge` | `run-bridge-minimal.mjs:1-3`; `package.json` `browser-first:bridge` | — |
| `examples/` | MCP + memory-service examples, an OpenAI-compatible relay example, a portable workflow | No — "never required Alpha runtime" | `MODULE_MAP.md:78`; `ls examples/` | 6 / 2026-10-01 |
| `addons/resonant-browser-host/` | Optional browser-host add-on package with its own `npm ci` and 2 tests | No — "not a required Alpha host" | `MODULE_MAP.md:77`; `alpha-build.yml:40-44` | 4 / 2026-09-14 |

### `src/core/` files (one line each; sizes in lines) **[inspected]**

| File | Lines | Role (from exports / intent citation) |
| --- | --- | --- |
| `browser-tools.ts` | 120 | Browser-tool result types (ADR-006) |
| `chat.ts` | 334 | Chat-rail message/thread shapes (ADR-004) |
| `compute-fabric.ts` | 626 | Compute Fabric model (ADR-032) — out of Alpha scope per boundary doc |
| `context-memory.ts` | 575 | Context-memory compaction (ADR-016) |
| `contracts.ts` | 2,961 | Cross-cutting TS contracts: add-on manifests, harness ops/events, provider types (ADR-005) |
| `defaults.ts` | 990 | Default state, catalog and provider profiles incl. local endpoints `http://127.0.0.1:18789/v1` (`:132,230`) |
| `delegation.ts` | 777 | Delegation packet validation / markdown rendering (ADR-015) |
| `goal-workspace.ts` | 519 | Goal workspace normalization (ADR-015) |
| `harness-client.ts` | 100 | `useSyncExternalStore` projection of the bridge's harness registry; all commands go through `web-transport` (`:26-28`) |
| `logician.ts` | 684 | Add-on SDK v0 logic (ADR-018) |
| `memory-provider.ts` | 352 | Memory broker: `livingArchiveMemoryProvider`, `httpJsonMemoryProvider`, `unsupportedMemoryProvider` (`:170-330`) |
| `model-strategy.ts` | 144 | Model/workload strategy (ADR-005) |
| `policies.ts` | 364 | Provider routing policies (ADR-005) |
| `provider-credentials.ts` | 13 | `providerNeedsStoredCredential` helper |
| `provider-service.ts` | 314 | Route resolution: `resolveAgentChatRoute`, `resolveWorkloadRoute`, `resolveArchiveIngestRoute`... (`:79-193`) |
| `runtime.ts` | 1,937 | UI-state hydration + `invoke()` wrappers for ~40 Tauri-era commands (`list_sideloaded_addons`, `save_provider_secret`, `telegram_*`, `compute_*`, `hermes_*`, `archive_*`, `engineer_recovery_turn`) (`:106,168-504`) |
| `system-slots.ts` | 30 | System slot ids (ADR-026) |
| `web-transport.ts` | 295 | React-side bridge client: 16-entry `commandRouteMap`, capability bootstrap via `POST /api/capability-tokens`, SSE reader for `/agent/events` (`:19-50,73,127-137,207-295`) |

### `src/modules/` directories **[inspected]**

addons (12 files, 5,423 LOC: AddOnsWorkspace, Hermes/Obsidian panels, controller) · archive (20, 5,992: Living Archive UI) · browser (2, 880: legacy browser workspace) · chat (25, 6,252: StrategistChatRail, harness-turn, thread-controller) · compute (5, 970: Compute Fabric UI — deferred) · delegation (3, 472) · hermes (2, 336; default dashboard `http://127.0.0.1:9119`) · obsidian (7, 1,508 — deferred) · opencode (2, 460) · overview (1, 436) · paperclip (2, 409; `http://127.0.0.1:3100`) · recovery (4, 424) · settings (7, 3,566) · shell (6, 1,123: controller, selectors, system-slots) · strategist (3, 326).

## Duplicated layers (src vs browser-first/host)

| Concern | TypeScript side (`src/`) | Host side (`browser-first/host/`) | Assessment |
| --- | --- | --- | --- |
| **Bridge client** | `src/core/web-transport.ts` (295 lines): reads `globalThis.__RESONANTOS_BRIDGE_CONFIG__`, sends `X-ResonantOS-Bridge-Token` / `-Capability-Bootstrap-Token` / `-Bridge-Capability-Token`, bootstraps at `/api/capability-tokens`, retries once on 403 (`:73-78,139-172`) | Extension `src/lib/bridge-client.js` (672 lines): same three headers, same bootstrap endpoint, plus `chrome.storage` override and 401 rebind (`:20-26,401-403,639-649`) | Two independent implementations of the same wire protocol; no shared module. **[inspected, high]**; drift risk **[hypothesis, medium]** |
| **Provider catalog / routing** | `src/core/defaults.ts` (provider profiles, endpoints), `provider-service.ts` (route resolution), `model-strategy.ts`, `policies.ts` | `provider-fabric-core.mjs`: `providerProfiles`, `modelCatalog`, `defaultRoutingStrategies`, `providerRouteForModel`, `providerRouteForWorkload` (`:1-349`); `provider-host-service.mjs`, `provider-bridge-service.mjs` | Second, parallel provider layer. The React one only reaches a provider through `provider_service_chat_completion` -> `POST /augmentor/chat` (`web-transport.ts:20-33`); its own routing tables are not consulted by the host. **[inspected, high]** |
| **Memory layer** | `src/core/memory-provider.ts` broker (Living Archive vs HTTP-JSON vs unsupported) dispatching to the acknowledged slot owner (`:41,170-330`) | `memory-host-service.mjs`, `memory-source-*.mjs`, `archive-review-host-service.mjs` (route owners per `ALPHA_RUNTIME_BOUNDARY.md:75`) plus `examples/living-archive-memory-service.mjs` | Client-side abstraction vs server; a second *abstraction* but not a second store. **[inspected, medium]** |
| **Add-on registry** | `packages/addon-sdk/src/registry.ts` (`createAddOnRegistrySnapshot`, pure) re-exported by `src/sdk/addons/registry.ts`; `src/core/runtime.ts:131-160` loads bundled manifests from `/addons/index.json` | `harness-registry.mjs` `createHarnessRegistry({store, reviewedAdapterIds, bindings})` + `harness-registry-store.mjs` durable file | Since Sep 2026 the React side is explicitly a *projection consumer* ("No local state ... can establish host governance", `harness-client.ts:24-25`; commits `d104ba5` "remove client governance authority"). Residual: bundled-manifest loading on the client. **[inspected, high]** |
| **Second bridge?** | None — `src/` never listens; it only calls the bridge | — | No second bridge. The only other server is the Vite dev server + its config plugin. **[inspected, high]** |
| **Dead command vocabulary** | `runtime.ts` wraps ~40 `invoke()` commands; only 16 are in `commandRouteMap` (2 provider + 14 harness). The rest (`save_provider_secret`, `telegram_*`, `compute_*`, `hermes_*`, `archive_*`, `recovery_*`) throw at `web-transport.ts:134-137` | — | Tauri/Electron-era residue kept compiling; UI paths relying on them are non-functional in web mode. **[inspected, high]** |

Cross-import topology **[inspected, high]**: extension -> nothing outside itself; host -> `packages/addon-sdk/src/{contracts,validation}.ts` only; `src/sdk/addons/*` -> `packages/addon-sdk`; `src/` -> no `browser-first/` imports.

## Module ownership table

Source: `docs/architecture/MODULE-OWNERSHIP.md` (209 lines). Note: "owner" in this document is a *responsibility statement*, never a person or team; the only named steward anywhere is "ResonantOS maintainers" (`disciplines/DISCIPLINES.md:4`). There is no CODEOWNERS file in the checkout (`ls .github` shows only `workflows/` and `security-pipeline/`). **[inspected, high]**

### Alpha ownership (`MODULE-OWNERSHIP.md:15-56`)

| Path | Owns (abridged) |
| --- | --- |
| `browser-first/resonantos-side-panel-extension/src/background.js` | Extension lifecycle, privileged Chrome API message mediation |
| `.../src/content.js`, `src/lib/content-*.js` | Page observation, bounded in-page interaction |
| `.../src/side-panel.js`, `src/lib/side-panel-*.js` | Side-panel composition, conversation, command routing, browser jobs, approvals |
| `.../src/main-workspace.js`, `src/lib/main-workspace-*.js` | New-tab workspace composition |
| `.../src/lib/trace-redaction-core.js`, `trace-redaction.js` | Strict redaction policy |
| `.../src/lib/resonant-context.js` | Page context tracking, `rc_session` persistence |
| `.../src/lib/browser-job-store.js` | Durable browser-job sanitation/identity |
| `.../src/lib/bridge-client.js` | Bridge target URL policy, transport, scoped capability acquisition |
| `.../src/lib/browser-page-actions.js`, `src/lib/control-*.js` | Governed observation/plan/consent/execute/verify |
| `.../src/lib/research-trail.js` | Research-trail intake formatting |
| `browser-first/host/run-bridge-minimal.mjs` | Composition root, token creation, startup/shutdown |
| `browser-first/host/bridge-server.mjs` | HTTP transport, auth, capability checks, CORS, dispatch |
| `browser-first/host/bridge-tls.mjs` | TLS cert lifecycle, OpenSSL resolution |
| `browser-first/host/provider-host-service.mjs`, `provider-bridge-service.mjs` | Provider profiles, session credentials, routing, model invocation |
| `browser-first/host/agent-adapters/provider-fabric.mjs` | In-process provider harness lifecycle |
| `browser-first/host/harness-examples/` | Opt-in declarative DSH/provider manifests |
| `browser-first/host/agent-control-host-service.mjs` | Plan/next-action decisions, bounded web reads |
| `browser-first/host/memory-host-service.mjs`, `memory-*.mjs` | Memory settings, sources, intake, sync, search, wiki checks |
| `browser-first/host/archive-review-host-service.mjs` + archive policy modules | Archive review, verification, promotion, restore |
| `browser-first/host/addon-delegation-host-service.mjs`, `addon-delegation-service.mjs`, `delegation-isolation.mjs`, `hermes-runtime.mjs`, `opencode-runtime.mjs` | Optional add-on status/control, scoped delegation, isolation, goals |
| `browser-first/host/bridge-shutdown.mjs` | Signal and shutdown ordering |
| `browser-first/host/dsh-runtime.mjs` | DSH native configuration, boot parser, child epochs |
| `browser-first/host/harness-credentials.mjs` | Exact binding and shared epoch custody |
| `browser-first/host/harness-transport.mjs` | Plugin/native authentication, Typert transport |
| `browser-first/host/agent-runtime-endpoint.mjs` | Outbound harness endpoint guards (loopback, DNS, redirects) |
| `browser-first/host/agent-adapters/openai-compatible.mjs` | OpenAI-compatible chat-completions transport |
| `examples/addons/openai-compatible-harness.json` | Declarative harness example |
| `browser-first/host/agent-adapters/dsh-typert.mjs` | DSH Typert envelopes, streams, cancellation |
| `browser-first/host/harness-adapter-contract.mjs` | Harness op/event validation, canonical SDK manifest validation entry |
| `browser-first/host/harness-host-service.mjs` | Harness routes (`/agent/*`, `/addons/enabled`), readiness, signed receipts |
| `scripts/harness-swap-demo.mjs`, `browser-first/test/harness-swap-demo.test.mjs` | Operator-driven certification demo |
| `browser-first/host/harness-policy.mjs` | Incumbent replacement/revocation policy |
| `browser-first/host/harness-registry.mjs` | Installation, grants, slot ownership, generations, boot epochs |
| `browser-first/host/harness-registry-store.mjs` | Atomic durable governance records |
| `browser-first/host/harness-boundary.mjs` | Authorized session identity and retirement |
| `browser-first/host/harness-event-bus.mjs` | Session-local event provenance/queues |
| `browser-first/host/opencode-boundary.mjs`, `opencode-event-bus.mjs`, `opencode-session-host-service.mjs`, `opencode-client.mjs` | OpenCode session proxy, credential custody, revocation |
| `browser-first/host/browser-diagnostics-host-service.mjs`, `browser-diagnostics-service.mjs` | Redacted diagnostics, download open/reveal |
| `browser-first/host/extension-prefs-host-service.mjs` | External persistence of extension prefs |
| `browser-first/test/` | Behavioural contracts and Alpha scope proof |

### Shared source ownership (`MODULE-OWNERSHIP.md:75-111`)

| Path | Primary owner (responsibility) |
| --- | --- |
| `src/core/harness-client.ts` | In-memory host projection, acknowledgements, event delivery |
| `src/core/defaults.ts` | Catalog and recommended-request suggestions |
| `src/core/runtime.ts` | UI-state hydration/serialization |
| `src/modules/shell/system-slots.ts` | Host-projected slot selection |
| `src/core/memory-provider.ts` | Memory transport adapter for the acknowledged owner |
| `src/modules/shell/selectors.ts` | Chat availability / displayed slot identity |
| `packages/addon-sdk/src/surface-routing.ts` | Manifest surface dock routes |
| `src/core/` | Shared contracts and pure cross-domain policy |
| `packages/addon-sdk/src/`, `src/sdk/addons/` | Canonical add-on manifests, capability vocabulary, validation |
| `src/modules/addons/AddOnsWorkspace.tsx`, `controller.ts`, `src/modules/addons/` | Harness management presentation / add-on mutations |
| `src/modules/archive/` | Living Archive UI |
| `src/modules/browser/` | Shared/legacy browser workspace presentation |
| `src/modules/chat/harness-turn.ts`, `thread-controller.ts`, `src/modules/chat/` | Harness session reuse / Stop dispatch / conversation UI |
| `src/modules/compute/` | Deferred Compute Fabric UI model |
| `src/modules/delegation/` | Delegation monitoring |
| `src/modules/hermes/`, `opencode/`, `paperclip/` | Optional / development-only add-on workspaces |
| `src/modules/obsidian/` | Deferred notes and vault workspace |
| `src/modules/overview/` | Overview framing |
| `src/modules/recovery/` | Recovery workflow |
| `src/modules/settings/` | Shared settings UI |
| `src/modules/shell/controller.ts`, `src/modules/shell/` | Shell boot / hydration |
| `src/modules/strategist/` | Strategist identity, channels, threads |
| `src/App.tsx` | React composition only |
| `public/addons/` | Bundled manifest/catalog data |
| `addons/resonant-browser-host/` | Optional browser-host add-on package |
| `examples/` | Optional examples |
| `scripts/` | Repository validation and dev tooling |
| `scripts/vite-dev-bridge-config.mjs` | Opt-in dev-page config delivery |

Paths with **no** row anywhere: `apps/augmentor/`, `disciplines/`, `prompts/`, `src/components/`, `src/ui/`, `browser-first/addons/` (two `addon.json`), `browser-first/host/opencode-version.json` **[inspected, high]**.

### What `scripts/module-ownership-doc.test.mjs` enforces (`:16-68`) **[inspected, high]**

- `MODULE-OWNERSHIP.md` exists; for every directory under `src/modules/` a table row `| \`src/modules/<name>/\`` exists (`:20-31`).
- Headings `## State And Data Flow`, `## Host And IPC Boundary`, `## Pull Request Checklist Hook` present (`:33-39`).
- Doc mentions `browser-first/host/`, contains a sentence matching `src-tauri/src/.*not present`, and contains three exact literal strings for the addon-delegation row, the diagnostics row and the `bridge-tls.mjs` row (`:41-57`).
- `CONTRIBUTING.md` links to `docs/architecture/MODULE-OWNERSHIP.md#pull-request-checklist-hook` (`:60-67`).
- It does **not** check that listed host files exist, that every `browser-first/host/*.mjs` has a row, or that `apps/` is covered. It is a presence lint on the document.

## Test lanes

| Lane | Command | Discovery rule | File count | Runs in workflow |
| --- | --- | --- | --- | --- |
| Extension + bridge contracts | `npm run test:browser-first` -> `scripts/run-browser-first-extension-tests.mjs` | `readdir(browser-first/test)` **non-recursive**, keep `endsWith(".test.mjs")`, sorted, `node --test --test-concurrency=1` (`:11-21`). Excludes `*.live.mjs` (3), 11 helper/lane `.mjs`, and `agent-control-certification/run-certification.mjs`, `hrr033-certification/run-certification.mjs` | 206 | alpha-build (via `verify:alpha`) |
| React/TS unit (vitest) | `npm test` (= `vitest run`); `verify:alpha` runs `npm test -- --run` | `vite.config.ts:51-54` `include: ["src/**/*.test.ts","src/**/*.test.tsx"]`, env `node` | 48 (incl. `src/sdk/addons/*.test.ts`, the only tests covering `packages/addon-sdk`, which has 0 of its own) | alpha-build |
| Dev bridge config | `npm run test:dev-bridge-config` | 2 explicit files | 2 | alpha-build |
| Docs/repo policy | `npm run test:docs` | 7 explicit `scripts/*.test.mjs` | 7 | alpha-build |
| Health / engineer-runner / module-ownership | `test:health`, `test:engineer-runner`, `test:module-ownership` | 1 explicit file each | 3 | alpha-build |
| Security pipeline unit | `npm run test:security-pipeline` | `scripts/security-pipeline/checks/*.test.mjs` + `disclosure-baseline.test.mjs` | 10 | alpha-build; `security.yml` also runs two of them directly |
| Browser host add-on | `npm run test:browser-host` | `addons/resonant-browser-host/test/*.test.mjs` | 2 | alpha-build |
| Examples | `test:living-archive-mcp`, `test:living-archive-memory-service` | 2 explicit files | 2 of 3 | alpha-build |
| Live Agent Control certification | `npm run test:browser-first:live` -> `browser-first/test/agent-control-live.mjs` (plain script, not `node --test`) | Playwright/CDP against stable Chrome under `xvfb-run`; profile `agent-control` when `CI` (`:18-19`) | 1 script + fixtures | agent-control-live.yml job 1 |
| Settings shapes | `npm run test:browser-first:settings-shapes` | plain script, headless when `CI` | 1 | agent-control-live.yml job 1 (`continue-on-error`) |
| Harness swap demo | `npm run test:browser-first:harness-demo` -> `node --test browser-first/test/harness-swap-demo-bridge.live.mjs` | explicit | 1 | agent-control-live.yml job 1 |
| Live SDK | `npm run test:browser-first:live-sdk` + `node --test browser-first/test/live-sdk-lane.test.mjs` | plain script + 1 test; installs pinned `opencode-ai` into `$HOME/.local` | 2 | agent-control-live.yml job 2 |
| DSH native live | none (`dsh-native.live.mjs`, `dsh-native-browser.live.mjs`) | manual; needs `DSH_LIVE_PREFIX`, `DSH_LIVE_PLUGIN_PREFIX`, `DSH_LIVE_PLUGIN_TARBALL`, `DSH_LIVE_CHROME_EXECUTABLE`, `DSH_LIVE_FINAL_GATE`, optional `DSH_LIVE_MODEL` (`dsh-native-browser.live.mjs:271-285`; `dsh-native.live.mjs:347-357,519`) | 2 | **none** (grep of workflows/package.json: no hits); notes in `docs/planning/dsh-native-auth-execution-notes.md` |
| Augmentor (vendored) | none at root; `apps/augmentor/AGENTS.md:30-40` lists `node test/install-proof.mjs` and an e2e battery needing "the real local DSH app" | — | 6 `*.test.mjs` + 8 e2e/proof scripts | **none** |
| Orphans | — | `scripts/default-branch-drift.test.mjs`, `examples/harness-openai-compatible-relay.test.mjs` referenced by no npm script | 2 | none |

`verify:alpha` sequence (`scripts/verify-alpha.mjs:10-38`, fail-fast, `shell:false`): `repo:hygiene`, `docs:check`, `test:docs`, `build` (tsc + vite build), `test -- --run`, `test:dev-bridge-config`, `test:browser-first`, `test:browser-host`, `test:living-archive-mcp`, `test:living-archive-memory-service`, `test:health`, `test:engineer-runner`, `test:security-pipeline`, `test:module-ownership`, `node scripts/security-pipeline/run-check.mjs --certify`, `pre-release:scan`, `browser-first-release-scope-audit.mjs --committed --strict`. Not included: `discipline:validate`, augmentor tests, DSH live lanes.

## Skipped / gated tests

No `describe.skip`, `it.skip`, `test.skip`, `.only`, `todo(` or `SKIP` constants in any test file under `browser-first/test`, `src`, `apps`, `scripts`, `examples`, `addons`, `packages` **[inspected, high]**. All 13 hits are conditional `t.skip(...)` at runtime:

| File:line | Condition |
| --- | --- |
| `browser-first/test/bridge-server.test.mjs:520` | loopback bind denied in sandbox (bridge bootstrap behaviour) |
| `browser-first/test/bridge-server.test.mjs:592` | loopback bind denied in sandbox (capability behaviour) |
| `browser-first/test/delegation-isolation-live.test.mjs:24` | not macOS (`sandbox-exec` is macOS-only) — always skipped on `ubuntu-latest` |
| `browser-first/test/delegation-isolation-live.test.mjs:30` | `/usr/bin/sandbox-exec` unavailable |
| `browser-first/test/delegation-isolation-live.test.mjs:67` | nested `sandbox-exec` unavailable |
| `browser-first/test/live-sdk-lane.test.mjs:56` | skip unless Chrome path resolvable and `CI`/`GITHUB_ACTIONS` true (`:31,50`) |
| `browser-first/test/memory-source-move.test.mjs:272` | symlink unavailable |
| `browser-first/test/memory-source-move.test.mjs:709` | symlink unavailable |
| `browser-first/test/opencode-client.test.mjs:142` | loopback listen denied |
| `examples/living-archive-mcp.test.mjs:55` | loopback bind denied |
| `examples/living-archive-memory-service.test.mjs:49` | loopback bind denied |
| `addons/resonant-browser-host/test/browser-host.test.mjs:92` | loopback bind denied |
| `addons/resonant-browser-host/test/browser-host.test.mjs:156` | loopback bind denied |

Env gates: `CI`, `RESONANTOS_LIVE_PROFILE`, `RESONANTOS_LIVE_CHROME_PATH`, `RESONANTOS_LIVE_ARTIFACT_DIR`, `RESONANTOS_LIVE_FORCE_UNAVAILABLE`, `RESONANTOS_LIVE_CDP_TIMEOUT_MS` (`agent-control-live.mjs:18-73,983`); `RESONANTOS_LIVE_SDK_MODEL`, `RESONANTOS_LIVE_SDK_FAULT` (`live-sdk-lane.mjs:87-92`): in CI without `RESONANTOS_LIVE_SDK_MODEL` the lane runs in `"ci"` mode (`:91`). `agent-control-live.yml` references no `${{ secrets.* }}`, so the "live" certification runs without any provider credential **[inspected, high]**; what "ci" mode proves vs "local" mode I did not trace **[open]**.

## Security pipeline verdict

**[inspected, high]** `scripts/security-pipeline/run-check.mjs` (246 lines) loads `.github/security-pipeline/checks.yml` (JSON despite the extension), validates `id/family/policy/adapter`, runs each adapter's `run({check, repoRoot})`, and fails the process when a result `shouldFail`: in `--certify` mode any `skipped|warn|fail` fails (`:205-209`); otherwise only `policy === "block" && status === "fail"`.

Registered checks (7): `npm-lockfiles` (supply-chain, block), `committed-private-key-material` (secrets-hygiene, block), `subprocess-no-argv-secret`, `subprocess-env-clear`, `subprocess-pinned-roots`, `subprocess-terminal-allowlist` (runtime-hardening, **observe**), `subprocess-no-shell-string` (runtime-hardening, block).

What they actually check:
- The four runtime-hardening adapters are 13-line wrappers (`checks/subprocess-env-clear.mjs:1-13`) over "cores" that score **spawn records supplied by the config** (`checks/lib/adapter-util.mjs:43-48`: "Spawn descriptors ... come from `check.records` (config- or test-injected)"). The 18 records in `checks.yml` `recordSets.browser-first-production-spawns` are hand-written JSON (`program`, `args`, `shell:false`, `env_clear:true`, `env_vars[...]`) with `sources[].anchor` strings. `runtime-hardening-registry.test.mjs:943` asserts each anchor string still appears in the named source file; nothing verifies that the record's `env_clear`/`env_vars` match what the code does. So these are **documentation-consistency checks**, not code analysis.
- `subprocess-no-shell-string.mjs` (695 lines) is a genuine regex-based static scanner over tracked JS/TS for `exec/execSync`, `shell:` options and template-literal commands, with string/comment masking; its header enumerates known evasions (options object in a variable, `Reflect.apply`, aliasing) and states "it stops the pattern being introduced by accident, not an author deliberately evading it" (`:1-50`).
- `committed-private-key-material.mjs` (132 lines): content grep over tracked files for key material.
- `npm-lockfiles.mjs` (69 lines): lockfile integrity presence check.
- `scripts/pre-release-scan.sh`: `grep -E` over the zip/dist for API-key shapes (`sk-`, `gsk_`, `rpa_`, `AKIA`, `xai-`), founder home paths, and `"installed|enabled|trusted": true` add-on defaults (`:10-12`).

Verdict: "strict security certification" = all seven static checks green with no skips. One real (heuristic) scanner, one secrets grep, one lockfile check, four self-reported spawn-record scorecards. No dynamic testing, no dependency CVE gate inside the pipeline itself (the `npm audit --audit-level=high` steps live in `alpha-build.yml:37-44`). It is a lint/documentation gate. In `security.yml` the full registry runs in observe mode with `continue-on-error: true` (`:33`); only three single-check jobs gate.

## CI workflows

| Workflow | Triggers | Jobs / runner / Node | Runs | Secrets |
| --- | --- | --- | --- | --- |
| `alpha-build.yml` ("Build Chrome extension alpha") | `workflow_dispatch`; PR and push to `main`, `dev` | 1 job, `ubuntu-latest`, Node from `.nvmrc` = 24.21.0, `fetch-depth: 0` | `npm ci`; `npm audit --audit-level=high`; `npm ci --prefix addons/resonant-browser-host` + audit; `npm run verify:alpha` with `RESONANTOS_BROWSER_HOST_CHANNEL=chrome`, `RESONANTOS_SCOPE_BASE/HEAD`; zip extension dir excluding `src/bridge-config.generated.js`; `pre-release:scan`; upload artifact 14 days (`:18-66`) | none |
| `agent-control-live.yml` | `workflow_dispatch` (input `public_submit_contract`); PR to `dev` on a path list that includes `browser-first/host/**`, extension `src/**`, `src/App.tsx`, `src/core/harness-client.ts`, `src/modules/{addons,chat}/**`, lockfiles; cron `17 3 * * *` | `agent-control-live` (20 min) and `live-sdk` (15 min), both `ubuntu-latest`, `.nvmrc`, stable Chrome via `browser-actions/setup-chrome`, `xvfb-run` | job 1: settings-shapes (soft), `test:browser-first:live` (soft), `test:browser-first:harness-demo`, upload evidence, "Reject uncertified run" if either soft step failed (`:86-126`). job 2: `npm install -g --prefix $HOME/.local opencode-ai@<pinned>`, `live-sdk-lane.test.mjs` (soft), `test:browser-first:live-sdk` (soft), upload, reject (`:153-191`) | none referenced; `CI=true` selects ci profile |
| `security.yml` ("security-observe") | PR/push `dev`; dispatch | 4 jobs, `ubuntu-latest`; action SHAs pinned differently (`checkout@11bd719…`, `setup-node@39370e3…`) from the other workflows (`@34e1148…`, `@49933ea…`) | `run-check.mjs --config .github/security-pipeline/checks.yml` (observe, `continue-on-error`); `committed-private-key-material` test+check (gating); `npm ci --ignore-scripts` + `check-repo-hygiene.test.mjs` + `repo:hygiene` (gating); `subprocess-no-shell-string` test+check (gating) | none |
| `security-drift.yml` | cron every 6 h; dispatch | 1 job, `contents:read, actions:read` | `node scripts/default-branch-drift.mjs` with `GITHUB_TOKEN`: flags un-PR'd commits on `dev`, workflows outside `WORKFLOW_ALLOWLIST`, stalled/`action_required` runs, and branch rules missing `required_status_checks` for "Build Chrome extension alpha" (`default-branch-drift.mjs:9-40`) | `GITHUB_TOKEN` only |
| `project-issue-sync.yml` | `issues` events; `pull_request_target` events; cron every 6 h; dispatch (`dry_run`) | 1 job, environment `project-sync`, checks out the **default branch** with `persist-credentials: false` | if `PROJECT_SYNC_TOKEN` unset -> warn and skip; else `gh project item-list 2 --owner ResonantOS`, `project:check-roadmap`, `sync-project-issue-labels.mjs` (`:42-91`) | `PROJECT_SYNC_TOKEN` (optional) |

Observations **[inspected, high]**: no Windows/macOS runners anywhere; Node 24.21.0 everywhere via `.nvmrc`; the only live-browser lane is Linux + stable Chrome + xvfb; `pull_request_target` is used but with default-branch checkout and no PR-head code execution, which limits the usual risk **[hypothesis, medium]**.

## Restartability / crash recovery

**Host (bridge) [inspected, high]**
- No `process.on('uncaughtException')` or `'unhandledRejection'` anywhere in `browser-first/host/*.mjs` (grep). An unhandled error therefore terminates the bridge with Node's default behaviour; there is no in-process supervisor or auto-restart. The launcher is a foreground `node run-bridge-minimal.mjs` (`package.json` `browser-first:bridge`).
- Graceful shutdown: `createBridgeShutdown` (`bridge-shutdown.mjs:1-20`) is idempotent; on first call it synchronously invokes `closeHarness`, `closeOpenCode`, `flushPrefs`, `unsubscribe`, waits `allSettled`, then `closeServer`. `installBridgeSignals` (`:22-31`) binds SIGINT/SIGTERM to `shutdown().finally(() => process.exit(0))`. Wired at `run-bridge-minimal.mjs:502-509` (closes harness service, OpenCode boundary, flushes extension prefs, closes HTTP server).
- Second signal handler: `opencode-client.mjs:406-424` `installShutdownHooks` registers its own SIGINT/SIGTERM handlers that `killAll()` children and `process.exit(130|143)` immediately, if `installSignalHandlers` is true. Whether that flag is set in the bridge path I did not trace; if it is, the immediate exit can race the ordered drain **[open, medium]**.
- Child processes are terminated with SIGTERM (`addon-delegation-service.mjs:1714,2289`; `delegation-isolation.mjs:277`; `dsh-runtime.mjs:251`; `opencode-boundary.mjs:99`).
- Port: `startBridgeServerWithFallback` tries `port` then `fallbackPorts=[0]` (OS-assigned) only on `EADDRINUSE`, other errors rethrow (`bridge-server.mjs:1556-1618`); result carries `requestedPort/attemptedPort/actualPort/recovered`, logged as `browser.first.bridge_started` (`run-bridge-minimal.mjs:490-499`).
- Tokens: `bridgeToken` and `capabilityBootstrapToken` are freshly minted by `createBridgeToken()` on every start unless passed via `--bridge-token`/`--capability-bootstrap-token` or `RESONANTOS_BROWSER_FIRST_BRIDGE_TOKEN` (`run-bridge-minimal.mjs:426-430`). Per-route capability tokens are minted in memory (`buildBridgeCapabilityTokens`, `:430`) and never written to disk (`bridge-server.mjs:1180-1182`). `writeBridgeConfig` rewrites `<extensionRoot>/src/bridge-config.generated.js` (mode `0600`) with `bridgeUrl`, `httpsBridgeUrl`, `bridgeToken`, `capabilityBootstrapToken` (`:1177-1198`). The built-in `POST /api/capability-tokens` requires bridge token + bootstrap token and returns only requested capabilities (`:1279-1290`).

**Extension [inspected, high]**
- No `chrome.alarms`, no reconnect/backoff loop, no heartbeat (grep over extension `src/`; only a settings status string mentions "Reconnecting").
- Bootstrap points: top-level `void initCapabilityTokens()` plus `rebindAndHydrate()` at service-worker load, and again on `chrome.runtime.onInstalled` / `onStartup` (`background.js:112,246-255`). Because MV3 service workers are terminated when idle, the module-level token cache (`bridge-client.js:606`) is lost and rebuilt on every wake **[hypothesis from MV3 semantics, high]**.
- Config resolution order: `chrome.storage.local["bridgeTargetOverride"]` > generated config (`globalThis.__RESONANTOS_BRIDGE_CONFIG__`) > default `http://127.0.0.1:47773` (`bridge-client.js:1-20,288-308`).
- 401 recovery: `currentBridgeRequest` catches `isUnauthorizedBridgeError` (status 401 or the "Unauthorized browser-first bridge request." message), calls `rebindAndHydrate({ refreshGenerated: true })`, which `fetch`es `chrome.runtime.getURL("src/bridge-config.generated.js")` with a cache-busting query and `cache: "no-store"`, re-parses it, re-creates the client, re-mints capability tokens, and retries the request once (`background.js:118-134`; `bridge-client.js:240-275,288-299,376-380`). Side panel and main workspace have the same pattern (`side-panel.js:149-187`; `main-workspace.js:117-172`).
- Capability-route 403: handled on the React side by a one-shot re-bootstrap (`web-transport.ts:149-172`); on the extension side `initCapabilityTokens` failures only log a DevTools breadcrumb and routes keep 403ing until the next rebind (`background.js:92-105`).
- Bridge unreachable (connection refused): `bridgeNetworkError` -> "Bridge is unreachable ... Start the ResonantOS browser-first bridge or update Settings > Bridge Target." (`bridge-client.js:313-320`). No automatic retry; the next user-initiated request re-attempts.

**What happens when the bridge dies and restarts** (synthesis):
1. Same-machine default (unpacked extension loaded from the directory the bridge writes to): the restarted bridge mints new tokens, possibly a new port, and rewrites the generated file. The extension's first request fails with 401 (or a network error until the bridge is up); on 401 it refreshes the generated file, re-mints capability tokens and retries. **The user does not re-copy anything** **[inspected, high]**. If the bridge chose a fallback port, the new URL is also in the regenerated file **[inspected, high]**.
2. Packaged install (the CI zip) or a bridge on another machine, configured via Settings > Bridge Target: the override's stored `token`/`capabilityBootstrapToken` take precedence (`bridge-client.js:292-298`) and are not rewritten by the bridge, so after a token-rotating restart the user must re-enter the new token, unless the operator pins tokens via `--bridge-token`/`RESONANTOS_BROWSER_FIRST_BRIDGE_TOKEN` so they survive restarts **[inspected for precedence, high; operational consequence hypothesis, medium]**.
3. Host-side durable state survives a crash by design of the stores (`harness-registry-store.mjs` atomic records; prefs flushed on shutdown only via `flushPendingExtensionPrefs`) — a hard crash before flush can lose pending prefs **[hypothesis, medium]**. In-memory provider credentials entered via Settings are lost on every restart by design (`ALPHA_RUNTIME_BOUNDARY.md:104-106`) **[reported]**.

## Open questions

1. `opencode-client.mjs:406-424` installs an immediate-exit SIGINT/SIGTERM handler when `installSignalHandlers` is true; does the bridge path enable it, and if so does it pre-empt the ordered drain in `bridge-shutdown.mjs`?
2. `agent-control-live.yml` references no secrets and `live-sdk-lane.mjs:91` selects `"ci"` mode without a model: what does the "ci" profile actually certify versus the "local"/"full" profile (which seem to need a real model)?
3. Why do `src/core/runtime.ts` and `src/modules/*` still carry ~24 unroutable Tauri-era commands (telegram, compute, hermes install/dashboard, recovery) that throw in web mode? Are the corresponding UI paths reachable from `App.tsx` and simply error at runtime?
4. `apps/augmentor` (a second MV3 extension with `nativeMessaging`) is absent from the boundary, module map and ownership docs; is it intended as the future "Augmentor" replacement for the side-panel extension, or an archived import? Its README says 0.1.33 targets DSH 0.1.5-rc.1 and the plugin "is its own package".
5. `prompts/sdk-demo-prompt.md` directs agents to `examples/sdk-prototype/` which does not exist; was it removed (check `git log --diff-filter=D -- examples/sdk-prototype`)?
6. `package.json` version `2.0.0-beta.1` and `docs/RELEASE_NOTES_BETA1.md` vs the "2.0.0 Alpha" repo/branding: which is the current release label?
7. The runtime-hardening "spawn records" are self-reported; is there any test that derives `env_clear`/`env_vars` from the real `spawnProcess(...)` call sites rather than from `checks.yml`?
8. Two of the three `*.live.mjs` lanes (`dsh-native*.live.mjs`) have no npm script and no workflow; are they run manually before merges touching `dsh-runtime.mjs`/`harness-*.mjs` (PR #534 claims "all 13 observations passing", commit `5b26f7c`)?
9. The two `*/run-certification.mjs` scripts under `browser-first/test/` subdirectories are invisible to the non-recursive runner; what invokes them?
10. `src/modules` has 15 directories and the ownership doc lists each, but `src/components/` and `src/ui/` are not covered by the ownership test's `src/modules/*` loop; intentional?
