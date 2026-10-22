# ResonantOS 2.0.0 Alpha - Add-on SDK, Add-on Loading, Delegation to External Agents

- Repository: `research/_untrusted/resonantos-2.0.0-alpha` at `578fbbc3c1c854b192318b3d2163b138fb45d8bd` (branch `dev`, merge of PR #534, 2026-10-18)
- Verification date: 2026-10-20. Static reading only (file reads, grep, git log). Nothing executed.
- Scope: `packages/addon-sdk/`, `src/sdk/addons/`, `public/addons/`, `browser-first/host/{addon-*,delegation-*,hermes-*,opencode-*,dsh-runtime}.mjs`, `addons/resonant-browser-host/`, `examples/`, extension add-on catalog, related tests, ADR-015/018/026/031, MCP/A2A/SKILL.md greps.
- Legend: **[inspected]** = what the code does, read at the cited lines. **[reported]** = what docs/comments/manifests say. **[hypothesis]** = my inference. Confidence high/medium/low per claim.

## 1. Summary

1. There are **three unrelated "add-on" systems** in the tree, and only one of them is live in the Alpha bridge path:
   - (a) The TypeScript Add-on SDK (`packages/addon-sdk/`, re-exported via `src/sdk/addons/` shims) plus the sixteen `public/addons/*.json` manifests. These are loaded by the Vite/React app in `src/` (`src/core/runtime.ts:150-162`) and by the bridge's harness registry validator (`browser-first/host/harness-adapter-contract.mjs:3-13`). The Vite app's sideload path is dead code (`hasCommandHost = () => false`, `src/core/runtime.ts:105`). **[inspected, high]**
   - (b) The bridge's delegation service (`browser-first/host/addon-delegation-service.mjs`, 2941 lines) which knows exactly five hard-coded add-ons (hermes, opencode, living-archive, email, calendar) with hard-coded "granted" capability lists that do not come from any manifest or grant store (`addon-delegation-service.mjs:2691-2760`). Its capability vocabulary (`filesystem-scoped`, `communication-draft`, `archive-knowledge-write`) is not the SDK's `ADDON_CAPABILITIES` enum (`packages/addon-sdk/src/contracts.ts:62-77`). **[inspected, high]**
   - (c) The Chrome extension's two `addon.json` files (`resonator`, `resonant-context`) with a third, incompatible schema (`mode`, `trust`, `contentScripts`, string `capabilities`). No code reads these files; the "add-ons" are ordinary content scripts statically listed in `manifest.json` and run in-process with full extension privileges (`browser-first/resonantos-side-panel-extension/manifest.json`, content_scripts block). **[inspected, high]**
2. **Manifests are validated, not signed.** The validator checks shape/enums only (`packages/addon-sdk/src/validation.ts:303-1273`). Nine bundled manifests self-declare `"provenance": {"tier":"curated-signed","verificationState":"verified","signed":true,"signer":"ResonantOS bundled catalog"}` with no signature value, no hash, and no verifier anywhere in the code (grep for `verifySignature|crypto.verify|subtle.verify|signatureRef` finds only type fields and the unrelated harness receipt signer). The registry copies the self-declared tier straight into `provenanceTier` (`packages/addon-sdk/src/registry.ts:61-69`). **[inspected, high]**
3. **Isolation of Hermes/OpenCode CLI delegation is macOS-only.** `resolveDelegationIsolation` returns `sandbox-exec` on darwin and `contract-only` (unconfined) on every other platform (`browser-first/host/delegation-isolation.mjs:61-68`). The sandbox profile is `(allow default)` with a file-write deny list and a small read deny list; network is not restricted (`delegation-isolation.mjs:71-85`). On Linux (the Raspberry Pi target mentioned in comments) and Windows, a delegated Hermes/OpenCode process runs with only env-allowlisting and a prompt asking it not to use tools. **[inspected, high]**
4. **The persistent "explicit enablement" gate can be bypassed per request.** `addonLocalCliExecutionEnabled` returns `true` if the request body has `enableHermesExecution: true` / `enableOpenCodeExecution: true`, before consulting the stored settings file (`addon-delegation-service.mjs:521-527`). The only barrier is the `addon-runtime-control` bridge token, which the extension holds. No non-test caller currently sends the flag. **[inspected, high]**
5. **The OpenCode proxy server (`opencode serve`) is spawned with the full bridge `process.env` and no sandbox wrapper** (`browser-first/host/run-bridge-minimal.mjs:224-233`, `opencode-client.mjs:281-285`), unlike the CLI delegation path, which allowlists env (`addon-delegation-service.mjs:2221-2249`). **[inspected, high]**
6. **Fixed-root executable discovery is real** for Hermes and OpenCode (`hermes-runtime.mjs:36-84, 110-147`; `opencode-runtime.mjs:34-70, 94-127`): candidates are absolute paths under `~/.hermes`, `~/.opencode/bin`, `~/.local/bin`, `/usr/local/bin`, `/usr/bin`, `/bin`, Homebrew, Program Files; realpath must stay inside the allowlisted roots; `HERMES_COMMAND`/`OPENCODE_COMMAND` overrides are honoured only when they equal a trusted candidate. The STATUS.md claim ("ambient PATH ... not executable sources", `docs/STATUS.md:72-74`) matches the code. Note `PATH` is still passed through to the child env (`addon-delegation-service.mjs:1601-1604`, `2222-2225`), so the child's own sub-processes do see ambient PATH. **[inspected, high]**
7. **Revocation is real only for the OpenCode proxy** (`opencode-boundary.mjs:105-127`, generation fence + latch). Hermes/OpenCode CLI delegations are one-shot child processes with a SIGTERM timeout (`addon-delegation-service.mjs:1710-1715`, `2282-2287`); there is no mid-run revoke. Add-on grant revocation in the harness registry (`harness-registry.mjs:238-251`) fences slots but there is no mechanism to stop an already-loaded extension content script. **[inspected, high]**
8. **MCP exists as an example only** (`examples/living-archive-mcp.mjs`, stdio JSON-RPC, protocol `2025-06-18`), explicitly excluded from release scope by `scripts/browser-first-release-scope-audit.mjs:382`. **No A2A code. No SKILL.md files.** "Skills" are markdown documents referenced by manifests (`documentPath`), rendered as prose for the agent, not executable skill packages. **[inspected, high]**
9. **The `resonant-browser-host` package is a standalone Playwright Chromium automation service** with stdio JSON-RPC, not imported by the bridge or extension (its README says so; grep confirms no importer outside its own folder). **[inspected, high]**
10. **No add-on path writes trusted wiki.** Delegation artifacts go to `BrowserFirst/DelegationArtifacts/{hermes,opencode}/` (`addon-delegation-service.mjs:1855-1859, 2412-2416`), not to `Memory/INTAKE` and not to `AI_MEMORY/wiki`. The service itself says intake files carry no add-on id (`addon-delegation-service.mjs:565`). Trusted-wiki protection is therefore by omission of a code path plus prompt text, not a capability check. **[inspected, high]**

## 2. Files / functions with line ranges

### packages/addon-sdk/ (public SDK, local-only)
| File | Lines | What it is [inspected] |
|---|---|---|
| `packages/addon-sdk/package.json` | 1-37 | `@resonantos/addon-sdk` 0.1.0, `"private": true`, exports point at `.ts` sources, `intent` field says "not yet published". Not in root workspaces; `tsconfig.json:21` includes `packages/addon-sdk/src`. |
| `packages/addon-sdk/src/index.ts` | 1-33 | Re-exports types from `src/core/contracts` (the SDK depends on the app core, not vice versa), plus `validateAddOnManifest`, `assertValidAddOnManifest`, `createAddOnRegistryEntry`, `createAddOnRegistrySnapshot`, `createAddOnSurfaceDockRoutes`, `ADDON_CAPABILITIES`, `ADDON_SERVICE_PROTOCOLS`. |
| `packages/addon-sdk/src/contracts.ts` | 24-90 | `ADDON_SDK_VERSION="0.1.0"`; `ADDON_CAPABILITIES` (14 names, lines 62-77); `ADDON_SERVICE_PROTOCOLS` (`stdio-json-rpc`, `http-json`, `websocket-json`, `host-command`, 79-84); `HARNESS_OPERATIONS` (86-88). |
| `packages/addon-sdk/src/validation.ts` | 303-1273 | `validateAddOnManifest(candidate, {source})` - pure shape/enum validator; provenance checks are warnings only (1242-1266). `assertValidAddOnManifest` (1275-1289) throws on errors. |
| `packages/addon-sdk/src/registry.ts` | 37-70, 89-149 | `sourceDefaults` copies manifest's self-declared `provenance.tier`/`verificationState` for bundled; forces `sideloaded-unverified` for sideload. `createAddOnRegistryEntry`, `createAddOnRegistrySnapshot`. |
| `packages/addon-sdk/src/surface-routing.ts` | 22-71 | `createAddOnSurfaceDockRoutes` - UI dock routes gated on `projection.installations[id].grantedCapabilities[].granted` (host projection is sole authority; local installations arg ignored, 25-32). |
| `src/sdk/addons/{index,contracts,validation,registry,surface-routing}.ts` | 7 lines each | `export * from "../../../packages/addon-sdk/src/..."` shims. |

### Importers of the SDK [inspected]
- `browser-first/host/harness-adapter-contract.mjs:3-4` imports `.ts` directly from `packages/addon-sdk/src/` (Node type-stripping). Used by `harness-registry.mjs` `install()` via `assertValidHarnessManifest` (`harness-registry.mjs:204`).
- `src/core/runtime.ts:100,160,170,178` (Vite app) and `src/App.tsx:165`, `src/modules/addons/AddOnsWorkspace.tsx:22`.
- Tests: `browser-first/test/dsh-native-policy.test.mjs:4`, `harness-provider-dispatch.test.mjs:10`, `harness-manifest.test.mjs:24`, `dsh-harness-stream.test.mjs:4`.
- The Chrome extension (`browser-first/resonantos-side-panel-extension/src/`) does **not** import the SDK (grep for `addon-sdk|sdk/addons` under that tree: zero hits).

### browser-first/host delegation stack
| File | Lines | Role [inspected] |
|---|---|---|
| `addon-delegation-service.mjs` | 167-2941 | `createAddonDelegationService(dependencies)` factory; returns 31 handlers (2908-2941). Inner functions: packet writer `executeDelegationRecord` (293-355), draft writer `executeAddonDraftRecord` (364-408), settings/gates (410-527), isolation prep (1284-1385), Hermes (1437-2073), OpenCode (2075-2632), drafts (2634-2689), status (2691-2760), settings (2762-2819), Hermes dashboard (2821-2906). |
| `addon-delegation-host-service.mjs` | 1-187 | Route table: 31 routes under `/addons/*`, `/hermes/*`, `/opencode/*`, `/goals`, each with `requiredCapability` in {`addon-runtime-read`, `addon-runtime-control`, `addon-execution-settings-write`, `addon-record-read`, `addon-record-write`}. |
| `delegation-isolation.mjs` | 47-69, 71-85, 141-173, 175-209, 211-216, 393-457 | `resolveDelegationIsolation`, `buildSandboxProfile` (SBPL), `writableRootsFor`, `readDenyRootsFor`, `wrapCommandForIsolation`, `createDelegationIsolationAdapter`. |
| `hermes-runtime.mjs` | 36-84, 110-147, 149-216, 229-343, 345-354 | Fixed-root candidate list, `resolveCandidate` realpath containment, `hermesRuntimeDiagnostics`, `hermesPythonRuntimeDiagnostics` (venv + `run_agent.py` containment), `hermesCommand`, `hermesHome`. |
| `opencode-runtime.mjs` | 34-70, 94-127, 151-201, 203-205 | Same pattern for `opencode`/`opencode-ai`; npm-global `lib/node_modules` sibling trusted (40-49). |
| `opencode-client.mjs` | 190-247, 249-338 | `ensureOpencodeServer` / `startOpencodeServer`: spawns `command serve --hostname 127.0.0.1 --port N` with `env: {...env, OPENCODE_SERVER_USERNAME, OPENCODE_SERVER_PASSWORD}` (281-285); random 32-byte password unless `OPENCODE_SERVER_PASSWORD` set (271-274); refuses to adopt a server that does not enforce auth (324). |
| `opencode-boundary.mjs` | 81-255 | `createOpenCodeBoundary`: generation fence, `gate()` polls `executionEnabled()` (120-127) and a 250 ms monitor (139); `revoke()` (115-119); payload sanitizer with credential key blocklist (24-50); fixed request-key allowlist per operation (60-72). `web` operation always refuses handoff (177). |
| `opencode-event-bus.mjs` | 17, 34, 100 | `eventSessionId`, `createOpenCodeSSEParser`, `createOpenCodeEventBus`. |
| `opencode-session-host-service.mjs` | 38-57, 59-90, 92-127 | `createOpenCodeWebUrlHandler` returns `{url:"", requiresCredential:true}` always (55); 13 `/opencode/session/*` routes, all `loopbackHostOnly` (88). |
| `dsh-runtime.mjs` | 13-29, 96-158, 212-300 | DSH native harness: spawns `process.execPath install.entry --profile web --no-open --host 127.0.0.1 --port N` (285) with a reserved HOME tree and `PATH` fixed to `${dirname(process.execPath)}:/usr/bin:/bin` (155); only `LANG`, `LC_ALL`, `TZ`, `DEEPSEEK_API_KEY` inherited (26). Linux/darwin only (18). (Harness internals belong to the provider agent.) |
| `addon-draft-connectors.mjs` | 1-83 | Builds `https://mail.google.com/mail/?view=cm&su=..&body=..` and `https://calendar.google.com/calendar/render?action=TEMPLATE..` URLs; appends a "Provider Handoff" audit section. Never sends. |
| `harness-host-service.mjs` | 334-357 | `/addons/registry`, `/addons/install`, `/addons/grants`, `/addons/enabled`, `/addons/remove`, `/addons/slots/assign` routes (client pushes the manifest in the body). |
| `harness-registry.mjs` | 104-114, 131-134, 199-218, 238-251 | `eligible()` capability gate, `assertOperation()`, `install()` (zeroes all `granted` flags, 214), `setGrants()` requires `consent === true` boolean in payload (242). |
| `bridge-capability-tokens.mjs` | 23-50, 62-73 | 26 bridge capabilities incl. `addon-runtime-read/control`, `addon-record-read/write`, `addon-execution-settings-write`; one token each, minted per launch or pinned by env/arg. |
| `bridge-server.mjs` | 119-129, 1201-1210 | Per-route check `isAuthorizedCapabilityRequest(request, bridgeCapabilityTokens, route.requiredCapability)`; `loopbackHostOnly` host check. |
| `run-bridge-minimal.mjs` | 200-240 | Wires delegation service, host service, `createOpenCodeBoundary` (`env: process.env`, 232), `subscribeOpenCodeExecution -> revoke()` (236-238). |

### Other
| File | Lines | Role |
|---|---|---|
| `addons/resonant-browser-host/src/browser-host.mjs` | 1-313 | Playwright `chromium.launch` (101), class `ResonantBrowserHost` (62), `handleJsonRpcLine` (272). Standalone; not wired. |
| `addons/resonant-browser-host/README.md` | 1-20 | [reported] "it is not the active Chrome extension UI or local bridge in the 2.0.0 Alpha runtime ... does not share a live session with the ResonantOS side-panel extension." |
| `examples/living-archive-mcp.mjs` | 1-870 | MCP stdio server (`protocolVersion "2025-06-18"`, 20), tools over Living Archive; readonly by default (554, 596, 731-776). |
| `examples/addons/{reference-memory,recursive-mas,openai-compatible-harness}.json` | - | Sideload example manifests, validated by `public-manifests.test.ts:78-96`. |
| `src/core/runtime.ts` | 131-183 | Vite app loads `/addons/index.json` (dev: `dev-index.json`) over `fetch`, asserts each manifest; `hasCommandHost = () => false` (105) so sideload functions return `[]` or throw. |
| `src/core/policies.ts` | 56-66 | `isCapabilityGranted(installation, capability, scope?)`. |

## 3. Manifest and capability model

**Schema (inspected, `validation.ts`):** required string fields `id,name,version,author,category,description,runtimeType` (324-326); `id` must match `/^addon\.[a-z0-9][a-z0-9-]*(\.[a-z0-9][a-z0-9-]*)*$/` (110, 330); `runtimeType` in {`ui-module`,`embedded-module`,`local-service`,`agent-addon`,`channel-addon`} (24); `surfaces[]` with `shellNavigation.requiredCapabilities` (339-397); `requestedCapabilities[]` of `{capability, scope, revocationBehavior, granted:boolean}` with capability in `ADDON_CAPABILITIES`, scope in {`none`,`self`,`workspace`,`shared`,`system`,`intake-only`}, revocation in {`hard-stop`,`degrade`,`hide-surface`} (403-420, 47-48); `systemSlots` must declare the slot's backing capability (1197-1240); plus many optional blocks (`service`, `tools`, `connectors`, `skills`, `hooks`, `install`, `audit`, `agentRuntime`, `memoryAccess`, `smokeTests`; `contracts.ts:26-43`).

**Capabilities (inspected, `contracts.ts:62-77`):** `filesystem, archive-read, archive-intake-write, chat-interface, memory-provider, providers, shell, network, ui-embedding, browser-control, agent-delegation, agent-runtime, notifications, device-integration`. Note there is **no** `archive-knowledge-write` / trusted-wiki capability in the enum at all; the only archive write is `archive-intake-write` whose only valid scope in practice is `intake-only`.

**Bundled manifests (inspected via field extraction of all 16 files in `public/addons/`):** every `requestedCapabilities[].granted` is `false` in every file. Nine files (augmentor-chat, browser, coherence-gate, heuristic-auditor, lia-verifier, living-archive, tts-enforcer, usage-tracker, plus `shield`? - no: shield has no provenance) carry `provenance: {tier:"curated-signed", verificationState:"verified", signed:true, signer:"ResonantOS bundled catalog"}`; seven (hermes, logician, obsidian, openclaw, opencode, r-awareness, shield, telegram-channel) have **no** provenance block. Requested capability highlights: `hermes.json` asks `network, notifications, providers, shell(self), ui-embedding, archive-read, archive-intake-write(intake-only)`; `opencode.json` asks `filesystem(workspace), shell(workspace), providers, archive-read, archive-intake-write, ui-embedding(system)`; `openclaw.json` asks `agent-delegation, shell(workspace)`; `shield.json` asks `filesystem(system)`.

**Signing / hashing / trust fields:** `src/core/contracts.ts:282-283` and `:698` define optional `signer?: string` and `signatureRef?: string`. No manifest in `public/addons` has a `signatureRef`. No code computes or verifies a signature or hash of a manifest. The validator's only provenance logic is two **warnings** (1242-1266): "provenance-incomplete" and, for `source:"sideload"`, "sideload-provenance-overridden". Therefore `"signed": true` is a self-assertion. **[inspected, high]**

**Where manifests are consumed:**
- Vite app: `fetch("/addons/index.json")` then `assertValidAddOnManifest(..., {source:"bundled"})` (`runtime.ts:150-162`). The app's add-on registry entries and grants live in browser state (`runtime.ts:1482-1535`) and the UI's grant buttons (`AddOnsWorkspace.tsx:455-456`).
- Bridge harness registry: the **client** POSTs a manifest to `/addons/install` (`harness-host-service.mjs:336-340`); `harness-registry.install()` validates it with the SDK validator (`harness-registry.mjs:204`), enforces size <= 256 KiB (206), requires that the named adapter's capabilities are all requested (209), and **resets every `granted` to false** (214). Grants are only set via `/addons/grants` with `consent: true` (238-242). This is the one place where grants are host-owned.

**Bridge delegation service model (separate, hand-coded):** `executeAddonsStatus` returns literal objects for `addon.hermes`, `addon.opencode`, `addon.living-archive`, `addon.email`, `addon.calendar` with literal `requestedCapabilities`/`grantedCapabilities`/`deniedCapabilities` arrays (`addon-delegation-service.mjs:2691-2760`), e.g. OpenCode "deniedCapabilities: `shell`" toggles only on the execution-settings boolean (2718). These strings are never compared against a manifest or against the harness registry. **[inspected, high]**

## 4. Which registry is live for the Alpha

| Registry | Location | Live in Alpha bridge+extension path? | Evidence |
|---|---|---|---|
| SDK validator + `public/addons/*.json` | `packages/addon-sdk`, `public/addons` | **Partly.** The validator is live inside the bridge's harness registry (`harness-adapter-contract.mjs:3-13`, `harness-registry.mjs:204`). The sixteen JSON files are consumed only by the Vite app in `src/`, which `docs/STATUS.md:129` [reported] distances from the Alpha runtime ("Tauri and Electron shells are historical or future work"); the extension never fetches `/addons/*.json` (grep: zero hits in extension `src/`). | inspected, high |
| Harness registry (`/addons/registry`, `/addons/install`, `/addons/grants`...) | `harness-host-service.mjs:334-357`, `harness-registry.mjs` | **Yes** - the extension's `bridge-client.js:82-87` lists these routes. Manifest is supplied by the client at install time. | inspected, high |
| Delegation service's five literal add-ons | `addon-delegation-service.mjs:2691-2760` | **Yes** - `GET /addons/status` and the `/hermes/*`, `/opencode/*`, `/addons/draft*`, `/addons/delegate*` routes are what the extension calls (`bridge-client.js:96-136`, `app-command-handlers.js:216,250,273`). | inspected, high |
| Extension `src/addons/{resonator,resonant-context}/addon.json` and identical copies in `browser-first/addons/` | extension tree | **Not loaded by code.** Content scripts are listed statically in `manifest.json` `content_scripts.js[]`. The `addon.json` files are descriptive only (`diff -q` shows the two copies are identical). | inspected, high |

**Verdict:** the Alpha's live add-on registry is the bridge's harness registry (for harness/agent-runtime add-ons such as DSH) plus the hand-coded delegation service (for Hermes/OpenCode/drafts). The SDK's manifest catalog in `public/addons/` is the Vite app's registry and is largely decoupled from what the extension does. **[inspected + hypothesis on "largely decoupled", medium-high]**

## 5. Isolation model

**Add-ons as code in the extension:** `resonator.js`, `resonant-context.js`, `context-plugins.js` etc. are content scripts in the MV3 manifest injected into `http://*/*` and `https://*/*` in all frames (`manifest.json` content_scripts). They run in the extension's content-script world with `host_permissions: ["http://*/*","https://*/*"]`. There is no loader, sandbox, or capability check between them and the rest of the extension. **[inspected, high]**

**Hermes/OpenCode CLI delegation (separate processes):**
- Spawned via `spawnProcess(wrapped.command, wrapped.args, {cwd, env, shell:false, stdio:["ignore","pipe","pipe"], windowsHide:true})` (`addon-delegation-service.mjs:1700-1706`, `2275-2281`).
- **Env scrubbing:** allowlist `HOME, PATH, SHELL, TERM, TMPDIR, TEMP, TMP, LANG, LC_ALL, XDG_*` plus `OPENAI_BASE_URL`, `HERMES_CONFIG` and the chosen provider's API-key names (`1599-1630`); OpenCode variant adds `OPENCODE_CONFIG/DATA/CACHE` and allowlisted `*_BASE_URL` keys (`2221-2249`, `42-55`). Provider secrets from the bridge's in-memory store are injected as env (`1770-1780`, `providerEnvFromSecrets` 103-108). So the delegated agent **does** receive a provider API key in its environment, contrary to the packet text "Provider secrets ... remain host-mediated" (`addon-delegation-service.mjs:343`). **[inspected, high]**
- **HOME override:** Hermes gets `HERMES_HOME: profileHome` (default `~/.hermes`, `hermes-runtime.mjs:349-354`); HOME itself is inherited, not overridden (1601). OpenCode: no HOME override. DSH: full HOME/XDG override into a reserved tree (`dsh-runtime.mjs:150-155`).
- **OS sandbox:** darwin only, `/usr/bin/sandbox-exec -f profile.sb cmd args` (`delegation-isolation.mjs:211-216`). Profile = `(allow default)`, `(deny file-write*)`, allow writes under workspace/profile/tmp/XDG roots, deny reads under `~/.ssh, ~/.gnupg, ~/.aws, ~/.azure, ~/.config/gcloud, ~/.kube, ~/.docker, Library/Keychains, Library/Cookies, browser profile dirs, ResonantOS_User/Secrets, ~/.netrc, bridge-config.generated.js` (`71-85`, `175-209`). Network: unrestricted. Process exec: unrestricted. `(allow default)` means everything not listed is allowed. **[inspected, high]**
- **Non-darwin:** `{mode:"contract-only", reason:"no-os-primitive:<platform>"}` (`delegation-isolation.mjs:68`) - the command runs unwrapped. The run audit records `isolation.mode` so the artifact says so (`isolationResultLines`, 1267-1282). Operators can force `contract-only` on darwin with `RESONANTOS_DELEGATION_ISOLATION=contract-only` (53-59). **[inspected, high]**
- **Hermes tool restriction is in-prompt and in-adapter:** generated Python adapter constructs `AIAgent(... enabled_toolsets=[], disabled_toolsets=[], skip_memory=False, skip_context_files=False ...)` (`addon-delegation-service.mjs:1655-1670`) and the prompt tells Hermes not to call tools (`1463-1485`); the result is rejected if it contains `<tool_call`, `tool_call`, `function_call` markers (`1487-1491`). Whether `enabled_toolsets=[]` disables tools depends on Hermes's own `run_agent.py`, which is out of tree. **[inspected; effect = hypothesis, medium]**
- **Change audit:** before/after tree snapshot of profileHome+tempDir (Hermes) or workspace (OpenCode) with 20k-entry / 3 s bounds (`delegation-isolation.mjs:314-358`), reported in the artifact. On darwin, `log show` is queried for `Sandbox: ... deny` lines (`248-308`). Detective, not preventive.

**OpenCode proxy session (`opencode serve`):** spawned by `ensureOpencodeServer` with `env: {...process.env, OPENCODE_SERVER_USERNAME, OPENCODE_SERVER_PASSWORD}` (`opencode-client.mjs:281-285`, env from `run-bridge-minimal.mjs:232`), no `sandbox-exec`, `cwd: directory`. The boundary enforces loopback origin, Basic auth, payload sanitization and a 1000-session limit, but OpenCode's own tools (shell, file edits) run with the bridge user's full privileges; approval is via `/opencode/session/permission` which forwards `{approved, remember}` to OpenCode (`opencode-boundary.mjs:213-215`). **[inspected, high]**

**DSH:** separate Node process, reserved HOME tree with mode 0700 checks (`dsh-runtime.mjs:140-156`), `PATH` pinned to node dir + `/usr/bin:/bin` (155), `DSH_TELEMETRY_MODE: 'DISABLED'`. Linux/darwin only. **[inspected, high]**

## 6. Grant check points (table)

| # | Check | File:lines | What is checked | Who can satisfy it | Verdict |
|---|---|---|---|---|---|
| G1 | Bridge route capability token | `bridge-server.mjs:127-128`, `1201-1210` | `x-resonantos-capability` token equals launcher-minted token for `route.requiredCapability` | The extension (receives all tokens via bootstrap, `1286-1288`) | Real auth boundary, but it is client-to-bridge auth, not an add-on grant |
| G2 | Loopback host | `bridge-server.mjs:129`, `opencode-session-host-service.mjs:88,119` | Host header is loopback | Any local client | Real |
| G3 | Local CLI execution enabled | `addon-delegation-service.mjs:521-527`, used at `1920`, `2491`, `2093-2094` | `payload.enable*Execution===true` OR env `RESONANTOS_{HERMES,OPENCODE}_EXECUTION` OR settings file `BrowserFirst/Settings/addon-execution.json` | Any holder of `addon-runtime-control` token can set the payload flag | **Bypassable per request**; the stored opt-in is advisory for CLI delegation |
| G4 | OpenCode proxy execution enabled | `addon-delegation-service.mjs:474-482`; `opencode-boundary.mjs:88, 120-127, 139` | settings file `opencode.localCliExecution===true` and not latched | Settings write via `POST /addons/execution-settings` (`addon-execution-settings-write` token) | Real; **not** bypassable by payload (no payload path into `openCodeProxyExecutionEnabled`) |
| G5 | Provider credential present | `addon-delegation-service.mjs:1934-1951`, `2500-2521` | provider key in bridge session secrets or env | Operator | Real precondition, not a permission |
| G6 | Runtime discovered at fixed root | `hermes-runtime.mjs:110-147`, `opencode-runtime.mjs:94-127` | realpath inside allowlisted roots; `.exe` on Windows; executable bit | Filesystem layout | Real |
| G7 | Writable root bounded | `delegation-isolation.mjs:106-139`; called `addon-delegation-service.mjs:1315-1331`, `1348-1363` | Hermes profileHome not `/`, not HOME, not ancestor of HOME, not inside/containing secrets or `BrowserFirst` | `payload.profileHome` attacker-controlled input | Real lexical + realpath check (darwin and non-darwin alike, since it runs before isolation mode branch? No: it runs only when `resolved.mode === "sandbox-exec"`, `1299-1307` return early otherwise) | **Non-darwin: not applied** (early return at 1299) |
| G8 | Delegation path containment | `addon-delegation-service.mjs:538-546` (`resolveDelegationPath`) | task path resolves under `Delegations/<target>` | Any token holder | Real |
| G9 | Harness registry slot eligibility | `harness-registry.mjs:104-114`, `131-134` | all required capabilities `granted:true` on entry; policy disabled ops | Grants set via `/addons/grants` with `consent:true` boolean | Real host-side grant gate for harness add-ons (DSH); `consent` is a request-body boolean, not a UI-bound proof |
| G10 | Install zeroes grants | `harness-registry.mjs:214`, `232` | manifest's `granted` booleans are ignored | - | Real ("trust never granted by omission") |
| G11 | Vite app `isCapabilityGranted` | `src/core/policies.ts:56-66`; callers `browser-tools.ts:91`, `logician.ts:68-74`, `delegation.ts:36-37,83` | browser-state grant | User clicks in `AddOnsWorkspace.tsx:455-456` | UI-layer only, in the Vite app, not reachable from the extension path |
| G12 | Surface dock routes | `packages/addon-sdk/src/surface-routing.ts:36-55` | host projection says installed+enabled+granted | - | UI visibility, not enforcement |
| G13 | Delegation service "granted" lists | `addon-delegation-service.mjs:2700-2731` | none - literals | - | **Display only**; never consulted by any handler |

## 7. Hermes / OpenCode / DSH spawn and boundary

**Task packet shape [inspected, `addon-delegation-service.mjs:309-346`]:** Markdown file `BrowserFirst/Delegations/<target>/<id>.md` with bullet fields `id, createdAt, source, sourceKind, sourceControlRunId?, status, trust: add-on agent..., allowedCapabilities: agent-delegation, archive-read-optional, forbiddenActions: provider-secrets, wallet-actions, trusted-memory-write, external-send, approvalRequiredBeforeExternalAction: true, expectedArtifacts: ...`; sections `## Mission`, `## Success Criteria`, optional `## Context Packet` (<= 24,000 chars, 296), `## Artifact Return Contract`, `## Boundary`. Targets: `hermes | opencode | engineer` (299). Status transitions are rewritten in-file (`writeDelegationStatus`, 1163-1173).

**Hermes start [inspected, 1893-2030]:** read packet -> status `running` -> blocked if no fixed-root CLI (1908-1919) -> blocked if execution not enabled (1920-1931) -> blocked if no provider credential (1932-1951) -> `adapter === "deterministic"` ? canned result (1437-1461) : `runHermesCliDelegation` (1743-1853): writes prompt + generated Python adapter into `BrowserFirst/Runtime/hermes-prompts/prompt-*/`, prepares isolation, spawns `<venv>/bin/python adapter.py prompt.md result.json` with `cwd: repoRoot` (1801), timeout 30 s..900 s (default 300 s), parses `result.json`, writes artifact `BrowserFirst/DelegationArtifacts/hermes/<id>-result.md` (1855-1891), appends execution audit (`appendDelegationExecutionAudit`, 1249-1265) to `BrowserFirst/Settings/addon-governance-audit.jsonl`.

**OpenCode start [inspected, 2453-2588]:** same gate order; `runOpenCodeCliDelegation` (2318-2410) spawns `opencode run ...` (args not shown above but `execOpenCodeCli(command, args)` 2260-2316) with `cwd` = resolved workspace (2126-2136), rejects `.cmd/.bat` shims and non-`.exe` on Windows (2263-2270); artifact `DelegationArtifacts/opencode/<id>-result.md` includes `Changed Files` and `Commands Run` as reported by the model (2412-2451).

**Deterministic adapter is selectable in production** via `payload.adapter === "deterministic"` or env `RESONANTOS_{HERMES,OPENCODE}_ADAPTER` (1900, 2460); it skips runtime, enablement and credential gates and writes a "completed" artifact whose text says it "proves lifecycle behavior; it does not claim ... real-world research" (1437-1461, 2138-2160). **[inspected, high]**

**Artifact return to intake:** none. Artifacts stay under `BrowserFirst/DelegationArtifacts/`; the extension reads them through `/hermes/delegation/artifact` (`2037-2059`). `grep DelegationArtifacts browser-first/host/*.mjs` outside the delegation service: zero hits. The memory intake writers do not record an add-on id (`addon-delegation-service.mjs:565`). **[inspected, high]**

**OpenCode proxy (`/opencode/session/*`):** `createOpenCodeBoundary.run(operation, payload)` validates exact key sets (60-72), `gate()` re-reads the settings-backed `executionEnabled()` on every call (120-127, 132, 236) and a 250 ms monitor retires the generation if it flips false (139). `ensureServer()` -> `ensureOpencodeServer` -> `opencode serve` child; `createClient` -> `createOpencodeHttpClient` with Basic auth header; events via SSE `GET /event?directory=` (161). Session permissions (OpenCode's own tool approvals) are proxied (213-215).

**DSH:** config requires exactly one `dsh-native-cookie` binding, loopback `http://127.0.0.1:<port>` endpoint, port != 19387 (`dsh-runtime.mjs:13-29`); package root validated for ownership and mode bits along the whole path (30-...); home tree reserved 0700 (140-146); child announces token on stdout (160-192, 300). Provider agent covers the harness side.

**Hermes dashboard proxy:** `/hermes/dashboard/{status,start,stop}` (`addon-delegation-host-service.mjs:35-52`) and `clientReachableProxyUrl` (`addon-delegation-service.mjs:260-271`) reverse-proxy a Hermes dashboard on `127.0.0.1:9119` through the bridge origin so the extension can iframe it (comment 260-265, "on the Pi"). Not traced further (2821-2906).

## 8. Revocation

| Mechanism | File:lines | Effect [inspected] |
|---|---|---|
| OpenCode proxy revoke | `opencode-boundary.mjs:105-127`; wired `run-bridge-minimal.mjs:236-238`; settings update notifies listeners before ack (`addon-delegation-service.mjs:494-512`, `2770-2819`) | Sets `disabledLatch`, bumps generation, aborts controller, closes SSE bus, SIGTERM->SIGKILL the owned `opencode serve` child (90-101), forgets singleton. Tests `opencode-execution-revocation.test.mjs` (9 tests) cover ordering, timeouts, re-enable. Real. |
| OpenCode latch in delegation service | `addon-delegation-service.mjs:470-482` | `openCodeDisabledLatch` short-circuits `openCodeProxyExecutionEnabled()`; set in settings update (not shown but referenced by test "revoke timeout persists disabled state"). |
| Hermes/OpenCode CLI delegations | `1710-1715`, `2282-2287` | Only timeout SIGTERM. `executeHermesDelegationCancel` (2061-2073) rewrites packet status to `cancelled`; it does **not** kill a running child (no handle is retained). **[inspected, high]** |
| Harness registry grant revocation | `harness-registry.mjs:238-251`, `notify()` 147-150 | Computes `revoked` capabilities, evaluates policy `hardStop`, fences slots synchronously, advances generation so in-flight `authorize` fails (`isCurrent`, 121-127). Real for harness sessions. |
| Extension content-script add-ons | - | No revocation mechanism exists; disabling requires an extension update/reload. **[inspected by absence, high]** |
| Manifest updates / trust changes | `packages/addon-sdk/src/registry.ts`, `harness-registry.mjs:199-218` | Reinstall replaces manifest; `ownedSlots(...).length` non-zero -> `ownership-conflict` (212-213), i.e. a slot-owning add-on cannot be replaced in place. No version/upgrade semantics, no update channel, no revocation list. |

## 9. MCP / A2A / SKILL.md verdicts with code pointers

| Term | Hit | Verdict |
|---|---|---|
| MCP | `examples/living-archive-mcp.mjs` (JSON-RPC stdio server, `initialize/tools/list/tools/call`, protocol `2025-06-18`, lines 20-23, 800-870); `examples/living-archive-memory-service.mjs:7` imports it; tests `examples/living-archive-mcp.test.mjs` (4) and `living-archive-memory-service.test.mjs` (7) | **Example only**, run by `scripts/verify-alpha.mjs:19` (`npm run test:living-archive-mcp`) but excluded from release scope (`scripts/browser-first-release-scope-audit.mjs:382` "needs separate release decision"). Not started by the bridge. |
| MCP | `browser-first/host/memory-schema.mjs:14,38` (`INTAKE/mcp` folder in the Living Archive schema) | Directory name only; no bridge code writes there. |
| MCP | `packages/addon-sdk/src/validation.ts:81`, `src/core/contracts.ts:349` (`connectorTypes` includes `"mcp-server"`) | Declarative manifest enum; no runtime that launches or connects to an MCP server. |
| MCP | `src/modules/settings/SettingsWorkspace.tsx:40,1115-1136` | Vite-app settings copy text telling users how to point external MCP clients at the example bridge. UI text only. |
| A2A / agent-to-agent | none in code (grep `\ba2a\b|agent-to-agent|agent2agent` excluding node_modules: zero hits) | **Not present.** |
| SKILL.md / skills/ | `find -iname SKILL.md`: **no files**. `skills` appear as manifest arrays (`public/addons/*.json` `skills[].documentPath`, `augmentorSkills[]`) pointing at markdown under `docs/architecture/addon-skills/*/` and `docs/addons/browser/skills/`; `public-manifests.test.ts:45-66` only asserts the files exist. | **Docs only.** "Skills" are prose instructions referenced by manifests, not loadable skill packages. |

**ADR intent vs built [reported vs inspected]:**
- **ADR-015** (Accepted, undated): "structured Delegation Packet as source of truth; `TASK.md` rendered for OpenClaw, Codex, Claude Code, OpenCode". Built: a markdown packet per delegation (`addon-delegation-service.mjs:309-346`) for `hermes|opencode|engineer` only. No OpenClaw/Codex/Claude Code runtime exists in `browser-first/host` (openclaw is a manifest in `public/addons/openclaw.json` only). **Partially built.**
- **ADR-018** (2026-04-27): SDK "lives under `src/sdk/addons`" - now shims to `packages/addon-sdk` (soft cutover per `package.json:29-30`). Built: validator/registry/surface-routing yes; "host-mediated tool contracts" and "safety rules that prevent add-ons from bypassing core authority" exist as manifest fields, enforced only in the harness registry path for harness add-ons. **Built as schema; enforcement partial.**
- **ADR-026** (2026-04-30): Augmentor Chat and Living Archive replaceable via system slots. Built: `systemSlots` validation (`validation.ts:1197-1240`), harness registry slot assignment (`harness-host-service.mjs:353-356`, `harness-registry.mjs:104-120`). Memory-provider swap in Vite app (`memory-provider.ts:335`). In the bridge, `executeAddonsStatus` still hard-codes `addon.living-archive` as the memory system (2721-2731). **Built in registry; delegation service ignores it.**
- **ADR-031** (2026-05-07): promote Hermes lessons into SDK contracts (`agentRuntime`, `memoryAccess`, `audit`, `embeddedWorkspace`, `smokeTests`). Built: those blocks exist in `AddOnSdkManifest` (`contracts.ts:37-42`) and `hermes.json` declares them. Runtime use: `agentRuntime` is read by harness registry (`eligible`, 111-112) and recorded in receipts (`harness-host-service.mjs:316-320`). `memoryAccess`, `audit`, `smokeTests` have no runtime consumer found in `browser-first/host` (grep `memoryAccess|smokeTests` in host: zero hits). **Declared, mostly unenforced.**

## 10. Tests table

| File | Kind | Asserts (one line) | Skipped / mocked? |
|---|---|---|---|
| `src/sdk/addons/validation.test.ts` (30 tests, 4 describes) | vitest unit | Validator accepts/rejects manifest shapes incl. harness contracts, revocation deps | Pure; no I/O |
| `src/sdk/addons/registry.test.ts` (10) | vitest unit | Registry entry defaults (provenance fallbacks, install state) | Pure |
| `src/sdk/addons/surface-routing.test.ts` (4) | vitest unit | Dock routes only for installed+enabled+granted in projection | Pure |
| `src/sdk/addons/public-manifests.test.ts` (6) | vitest fixture | All `index.json`/`dev-index.json` manifests validate with no errors; referenced skill docs exist; example sideloads validate | Reads repo files; **does not check signatures** (none exist) |
| `browser-first/test/addon-delegation-host-service.test.mjs` (2) | unit | Route table has expected paths/capabilities; missing handler throws | Pure |
| `addon-delegation-service-error-handling.test.mjs` (50, 2166 lines) | unit, injected deps | Gate ordering, blocked reasons, redaction, attacker profile roots rejected, isolation failures audited | **All spawns mocked** (`spawnProcess` fakes at 1100, 1154, 1231, 1362, 1400); fs real in temp dir |
| `addon-cli-execution-inprocess-self-test.test.mjs` (3) | in-process bridge smoke | Settings route round-trips; Hermes/OpenCode start routes complete | **deterministic adapter**; no runtime |
| `delegation-bridge-inprocess-self-test.test.mjs` (2) | in-process smoke | `/hermes|/opencode/delegation/*` route flow | **deterministic adapter** |
| `addon-draft-connectors.test.mjs` (4) | unit | Gmail/Calendar URL construction; unsupported provider rejected; audit appended | Pure |
| `addon-runtime-status.test.mjs` (4) | extension unit | Status text for missing CLI / ready / bridge failure | Bridge mocked |
| `delegation-guidance.test.mjs` (2), `delegation-status.test.mjs` (3), `delegation-lifecycle.test.mjs` (5) | extension unit | UI text/summary assembly from bridge responses | Bridge mocked |
| `delegation-isolation.test.mjs` (12) | unit | SBPL profile text, root lists, bounded-root rejections, denial-line parsing | Platform passed as parameter; no sandbox executed |
| `delegation-isolation-live.test.mjs` (1) | live | `sandbox-exec` actually denies writes/reads | **`t.skip` unless darwin with working nested sandbox-exec** (22-30, 65-67) |
| `hermes-runtime.test.mjs` (7) | unit | Ignores ambient PATH; realpath escapes rejected; venv symlink accepted only with in-root `pyvenv.cfg` | fs functions injected |
| `opencode-runtime.test.mjs` (6) | unit | Same for OpenCode; Windows `.exe` rule; npm-global symlink accepted | fs injected |
| `opencode-boundary.test.mjs` (24) | unit | Revocation fences, late-start cannot resurrect server, sanitizer | ensureServer/client faked |
| `opencode-client.test.mjs` (52) | unit + loopback | Port picking, auth enforcement check, pid record | `spawnImpl` faked; one `t.skip` when loopback listen denied (142) |
| `opencode-execution-revocation.test.mjs` (9) | unit | Disable closes SSE before ack; env/payload enable cannot override off; unrelated CLI gets no serve credential | spawn faked |
| `opencode-session-host-service.test.mjs` (21), `opencode-event-bus.test.mjs` (24), `opencode-proxy-transport.test.mjs` (22) | unit | Route shapes, SSE parsing/timeouts, transport | `t.mock.timers` |
| `addons/resonant-browser-host/test/browser-host.test.mjs` (4) | integration | Launches real Chromium via Playwright, navigates, clicks, screenshots | **Requires Playwright Chromium**; separate `npm run test:browser-host` |
| `addons/resonant-browser-host/test/path-contains.test.mjs` (9) | unit | Path containment incl. symlink escapes | Pure |
| `examples/living-archive-mcp.test.mjs` (4) | unit + live HTTP backend | tools/list, tools/call flow; proxy to memory service | In-process HTTP |
| `examples/harness-openai-compatible-relay.test.mjs` (21) | unit | Relay auth, SSE normalisation, credential scrubbing | Provider agent's area |

**No test anywhere spawns a real Hermes or OpenCode binary.** The "CLI execution" and "delegation bridge" smoke tests pass through the deterministic adapter. **[inspected, high]**

## 11. Downgrades

1. **"Signed" manifests are not signed.** `provenance.signed: true` is a JSON literal; no verifier, no signature bytes, no hash. Registry trusts the self-declared tier for bundled sources (`registry.ts:61-69`). Confidence high.
2. **Execution opt-in is bypassable by request body** for CLI delegation (`addon-delegation-service.mjs:522-523`) while the blocked message advertises it as "from a trusted Settings flow" (1928, 2498). Only the proxy path (`openCodeProxyExecutionEnabled`, 474-482) is immune. Confidence high.
3. **OS isolation is darwin-only and `(allow default)`.** Linux/Windows run unconfined; even on darwin, network and process exec are unrestricted (`delegation-isolation.mjs:61-85`). The Hermes writable-root bound check (G7) only runs in sandbox-exec mode (`1299-1307`). Confidence high.
4. **Provider API keys are handed to the delegated process** via env (`1770-1780`, `providerEnvFromSecrets`) despite packet text saying provider secrets stay host-mediated (343). Confidence high.
5. **`opencode serve` inherits the whole bridge environment**, no scrubbing, no sandbox (`run-bridge-minimal.mjs:232`, `opencode-client.mjs:283`). Confidence high.
6. **Deterministic adapter is reachable in production** by request payload or env (`1900`, `2460`) and writes `status: completed` artifacts. Confidence high.
7. **`GET /addons/status` capability lists are literals**, unconnected to any grant store (`2691-2760`). Confidence high.
8. **Extension "add-ons" are plain content scripts**; `addon.json` files are unread documentation. Confidence high.
9. **Vite-app sideloading is dead code** (`hasCommandHost = () => false`, `runtime.ts:105`), so the "sideload" branch of the validator and the `examples/addons/*.json` sideload tests exercise a path no runtime takes. Confidence high.
10. **No real-runtime tests.** All Hermes/OpenCode spawns are faked; the sandbox live test self-skips off macOS. Confidence high.
11. **Cancel does not kill.** `executeHermesDelegationCancel`/`executeOpenCodeDelegationCancel` only rewrite the packet status (2061-2073, 2620-2632). Confidence high.
12. **`consent: true` is a request boolean** (`harness-registry.mjs:242`); nothing binds it to a human UI action beyond possession of the `addon-runtime-control` token. Confidence high.
13. **ADR-015's OpenClaw/Codex/Claude Code runtimes do not exist**; `openclaw.json` is a manifest with no host runtime. Confidence high.
14. **Hermes tool disablement relies on an out-of-tree `run_agent.py` honouring `enabled_toolsets=[]`** plus a regex on output (1487-1491). Confidence medium (effect unverifiable statically).

## 12. Coupling

- `packages/addon-sdk/src/*` import types **from** `src/core/contracts` (`contracts.ts:3-22`, `registry.ts:4-14`, `validation.ts:3-14`): the "public SDK" cannot be extracted without the app core. `package.json:29` acknowledges this ("not yet published").
- `browser-first/host/harness-adapter-contract.mjs` imports `.ts` from `packages/addon-sdk/src/` at runtime (Node type stripping) - the bridge's manifest validation is coupled to the TypeScript SDK source.
- `addon-delegation-service.mjs` imports `dashboardProxyUrl` from `bridge-server.mjs` (line 14) and `bridge-server.mjs` is imported by `opencode-session-host-service.mjs:8` (`validateLoopbackHost`): circular-ish host wiring.
- `addon-delegation-service.mjs` and `memory-source-settings-service` share `executeAddonsStatus` (`run-bridge-minimal.mjs:201, 255`), so memory settings UI depends on the literal add-on list.
- `delegation-isolation.mjs` read-deny list hard-codes `browser-first/resonantos-side-panel-extension/src/bridge-config.generated.js` (206) and `ResonantOS_User/Secrets` paths (200-202): isolation policy knows the repo layout.
- Capability vocabularies: SDK `ADDON_CAPABILITIES` (14), bridge route tokens `BRIDGE_CAPABILITIES` (26, `bridge-capability-tokens.mjs`), delegation-service literals (`filesystem-scoped`, `communication-draft`, `provider-handoff`, `archive-knowledge-write`, ...), extension `addon.json` strings (`highlight`, `viewport-observer`, ...). Four unrelated vocabularies share the word "capability".
- Harness receipts are ed25519-signed (`harness-host-service.mjs:150-163`, provider agent's area) - the only signing in the repo; add-on manifests do not use it.

## 13. Open questions

1. Does `run_agent.py` (Hermes, out of tree) actually disable tools when `enabled_toolsets=[]`? If not, a Hermes delegation on Linux/Windows is an unsandboxed agent with a provider key and `skip_memory=False`.
2. What are the exact `opencode run` args and whether OpenCode's own permission prompts are auto-approved in non-interactive mode (`runOpenCodeCliDelegation`, 2318-2410, not read line-by-line)?
3. Is the Vite app in `src/` shipped at all in the Alpha, or only the extension + bridge? `docs/STATUS.md:129` [reported] suggests the latter; if so, `public/addons/*.json`, `AddOnsWorkspace.tsx` grant UI and ADR-026 slot replacement are not user-reachable.
4. Where does the extension obtain a manifest to POST to `/addons/install` (harness registry)? Not traced in extension `src/lib/*` within the time box; relevant for whether users can install arbitrary manifests.
5. Hermes dashboard proxy (`/hermes/dashboard/*`, 2821-2906) - what is proxied and is the upstream (`127.0.0.1:9119`) authenticated?
6. `browser.json` requests `browser-control` with `service` block - is any bridge code able to launch `addons/resonant-browser-host`? Grep says no; confirm with the browser-diagnostics agent.
7. Is `addon-governance-audit.jsonl` ever read back or surfaced, or append-only evidence nobody consumes?
