# ResonantOS 2.0.0-alpha — LLM Providers ("Provider Fabric") and Harness/DSH

- Repository: `research/_untrusted/resonantos-2.0.0-alpha` at `578fbbc3c1c854b192318b3d2163b138fb45d8bd` (branch `dev`, merge of PR #534 `feat/dsh-native-auth`)
- Verified: 2026-10-20, static reading only (no code executed). All paths below are relative to `browser-first/` unless noted.
- Legend: **[inspected]** = what the code does; **[reported]** = what the repo's docs/comments/tests claim; **[hypothesis]** = my inference. Confidence high/medium/low per claim.

## Summary

The "Provider Fabric" is a Node-only host module set (`host/provider-fabric-core.mjs`, `host/provider-bridge-service.mjs`, `host/provider-host-service.mjs`) that routes chat requests from the Chrome side-panel extension to OpenAI-compatible `/chat/completions` endpoints. **Every** upstream call in the host is an OpenAI-style POST with `Authorization: Bearer` [inspected, high]. Built-in providers are exactly three plus a local slot: MiniMax (`api.minimax.io`), "Z.AI GLM" (actually a hard-coded **localhost** proxy `127.0.0.1:18789`, labelled a cloud provider), OpenAI (`api.openai.com`), and `desktop-local` (Ollama at `127.0.0.1:11434`). Anthropic and Google appear only as account *presets* (and in the extension's template list) but there is no Anthropic Messages or Gemini wire implementation anywhere in the host, so direct Anthropic/Gemini accounts cannot work [inspected, high]. Many other vendors are listed as OpenAI-compatible presets (xAI, DeepSeek, Mistral, Qwen, OpenRouter, Together, Groq, Fireworks, NIM, LiteLLM, etc.), and one preset hard-codes a developer's LAN address (`192.168.1.77:30004`, "ASUS GX10").

Routing: five named strategies (augmentor-chat, agent-control, archive-ingest, routine-delegation, recovery-engineer) each with a primary + fallback chain. Manual model selection is preserved (no silent swap) in the main chat path and a fallback is flagged in the response (`routeFallback`, `routeNotice`) — this is genuinely enforced in the host and tested with stubbed `fetch`. However, the **Archive Ingest strategy card in the UI is decorative**: the archive verifier/writer use a hard-coded chain (gpt-5.5 → zai → MiniMax) and ignore the strategy, its hard-stop flag, and the allowed-model preferences [inspected, high]. The allowed-model ("disabled model") policy is likewise only enforced in `executeChat`; the inline assistant and agent-control planner bypass it.

Credentials: the alpha host keeps provider keys in an in-process `Map` plus process env vars; nothing is written to disk, and a legacy plaintext `~/ResonantOS_User/Secrets/provider-secrets.json` is detected but ignored [inspected, high]. Keys arrive from the extension as a JSON POST body (`/providers/credentials`) and are never returned; the extension has no `chrome.storage`/`localStorage` for credentials [inspected, high]. The weak points are: keys live in `process.env` and are therefore inheritable by any child process the bridge spawns; file permission hardening (`0o600`, `mode & 0o077` checks) is POSIX-only; provider error text is forwarded to the client unredacted.

Harness/DSH: an opt-in governance layer (`harness-*.mjs`) that can replace the default chat path with an "add-on" runtime once an operator installs a manifest and assigns the `primary-agent` slot. Three reviewed adapters exist: `provider-fabric-v1` (in-process wrapper around the same provider service, single attempt, no fallback), `openai-compatible-v1` (SSE bearer endpoint from an operator binding), and `dsh-typert-v1` (DeepSeek's `dsh` CLI "web" server, spoken to over its Typert JSON-RPC + WebSocket). PR #534 added `dsh-native-cookie`: the bridge itself spawns `node node_modules/@deepseek-ai/dsh/lib/bin.js --profile web --no-open --host 127.0.0.1 --port N` as a "bridge-owned child", scrapes the `dsh web: http://127.0.0.1:N/?token=…` line from the child's stdout, exchanges the token for a `dsh-auth-*` cookie, and passes `DEEPSEEK_API_KEY` from the bridge env into the child. It is **macOS/Linux only**, pinned to the exact package version `0.2.0-rc.2`, and its live certification drivers are conductor-only scripts not run by any CI workflow [inspected, high].

Tests: ~50 relevant files. All provider tests stub `globalThis.fetch`; no test makes a real provider call. The default lane (`npm run test:browser-first`, run by `verify:alpha` in `alpha-build.yml`) only picks `*.test.mjs`; the `*.live.mjs` DSH drivers and the harness-demo bridge lane require external binaries/keys and are not part of CI.

## Files and functions with line ranges

### `host/provider-fabric-core.mjs` (397 lines, pure data + routing functions) [inspected]
| Lines | Item | Notes |
|---|---|---|
| 1-28 | `providerProfiles` | `shared-minimax` (MiniMax-M3), `shared-zai-glm` (`apiBaseUrl: http://127.0.0.1:18789/v1`, role "OpenClaw/Z.AI GLM fallback provider"), `shared-openai` (gpt-5.5, gpt-5.4-mini) |
| 30-76 | `modelCatalog` | 5 entries; `batiai/gemma4-e2b:q4` on `desktop-local` ("last resort recovery") |
| 78-129 | `defaultRoutingStrategies` | 5 strategies; only `archive-ingest` has `hardStop: true` (L106) |
| 139-144 | `inferProviderType` | string-contains heuristics; anything unknown → `"minimax"` |
| 170-186 | `allowedModelsForProvider`, `isModelAllowed` | model-preferences policy |
| 196-207 | `normalizeRoutingStrategy` | override primary only if in catalog; fallbacks capped at 6 |
| 209-230 | `modelRuntimeState` | `configured` = secret present (or `localRuntimeUrl` for desktop-local) |
| 232-251 | `resolveRoutingStrategies` | `routeState: routable|unavailable` |
| 253-310 | `providerRouteForModel` | returns `null` for `__auto__`/`auto` (254-256); custom-account models with an `apiBaseUrl` route to their own endpoint (261-274); then prefix rules: `batiai/` → Ollama (275-284), `gpt-` → `https://api.openai.com/v1` (285-293), `zai/glm` → `http://127.0.0.1:18789/v1` (294-302); **default: anything else → `https://api.minimax.io/v1` with `wireModel = model`** (303-309) |
| 312-347 | `providerConnectivityTarget` | `/models` probe URLs for the four built-ins |
| 349-397 | `providerRouteForWorkload` | explicit model → `source: "manual"`, rejects with `reason: "model-disabled"` if not allowed (359-377); otherwise first `configured` entry of the strategy chain (378-396) |

### `host/provider-bridge-service.mjs` (1479 lines, the live implementation) [inspected]
| Lines | Item | Notes |
|---|---|---|
| 49 | `sessionProviderSecrets = new Map()` | the only credential store |
| 50-54 | `providerEnvKeys` | `MINIMAX_API_KEY`, `OPENAI_API_KEY`, `ZAI_API_KEY`/`GLM_API_KEY`/`ZHIPUAI_API_KEY` |
| 55-67 | timeouts | archive 60 s, chat attempt 90 s, inline 30 s; env-overridable (`RESONANTOS_PROVIDER_*_TIMEOUT_MS`), max 600 s |
| 73-138 | `fetchProviderResponse`, `readChatResponse` | AbortController timeout; body size cap only when `singleAttempt` (1 MiB, L1280) |
| 140-176 | `envProviderSecrets`, `readProviderSecrets` | env + `RESONANTOS_PROVIDER_SECRETS_JSON` (L152) merged under session Map |
| 186-193 | `credentialStoreStatus` | `persistence: "session-only"`, `legacyPlaintextDetected: existsSync(providerSecretsPath())` |
| 204-301 | endpoint policy | `isPrivateOrLocalHostname` (218-237), `allowsLocalProviderEndpoint` (239-252, env override `RESONANTOS_PROVIDER_ALLOW_LOCAL_ENDPOINTS=1` at L245), `normalizeProviderEndpointUrl` (254-292: https required unless local template; credential-bearing → no private hosts), `providerRequestUrl` (294-301) |
| 303-412 | `providerPreset` | openai (306-316); local presets ollama/lm-studio/dgx-spark/localai/llama-cpp/vllm/tgwui (319-336); openai-compatible presets incl. `openrouter` (346), `asus-gx10: http://192.168.1.77:30004/v1` (355); **anthropic preset `https://api.anthropic.com/v1`** (367-377); **google preset `https://generativelanguage.googleapis.com/v1beta`** (378-389); custom cohere/ai21/replicate (390-403); default minimax (404-411) |
| 430-483 | `normalizeProviderAccount` | endpoint validated at save time (L478); `apiBaseUrl` may be empty (not `required`) |
| 485-500 | `readProviderAccounts`, `writeProviderAccounts` | `~/ResonantOS_User/ProviderFabric/provider-accounts.json`, `mode: 0o600` + `chmod` |
| 502-529 | `allProviderProfiles`, `allModelCatalog` | built-ins merged with user accounts |
| 587-605 | `appendProviderDiagnosticHistory` | only place `redactDiagnosticText` is applied (L596); 30-entry history file |
| 623-663 | `executeProviderStatus` | `credentialPreview: "session"|"missing"` (L660); never returns key material |
| 665-735 | `executeProviderHealthCheck` | states ready/degraded/disabled/missing-credential/unreachable |
| 737-816 | `executeProviderConnectivityTest` | GET `/models` with `Authorization: Bearer` (L780), 7 s timeout (L776), records to history |
| 824-891 | model-preferences and routing-strategy save | both write JSON files under `ProviderFabric/` |
| 893-910 | `executeProviderCredentialSave` | min 8 chars (L900) → `rememberProviderSecret` (Map only) |
| 912-990 | account save/remove | remove also scrubs routing overrides that pinned the removed models (956-982) |
| 992-999 | `sanitizeAssistantContent` | strips `<think>…</think>` for MiniMax only |
| 1014-1032 | `providerRouteForWorkload` (async wrapper) | |
| **1034-1049** | `providerRouteForArchiveVerifier` | **hard-coded chain gpt-5.5 → zai/glm-5.2 → MiniMax-M3 keyed on secret presence; does not read strategies or preferences** |
| 1065-1157 | `runArchiveSemanticVerifier` | returns `semanticStatus: "unavailable"` on any failure (never throws) |
| 1159-1186 | `runArchiveIngestWriter` | delegates to `memory-ingest-writer.mjs` with `route` + raw `credential` |
| 1202-1203 | `executeBridgeChat` / `executeRawProviderChat` | raw = `singleAttempt: true` (used by harness adapter) |
| **1205-1331** | `executeChat` | route decision + errors (1207-1217); strategy chain of `configured` entries only (1224-1234); per-attempt loop (1244-1329): missing credential → manual: throw (1253) / strategy: record and continue (1255); fetch (1260-1282); transport error / `!response.ok` / empty reply → throw in manual or `singleAttempt`, else continue (1283-1308); `usedFallback = attemptModel !== strategy.primaryModel` (1313-1314); `routeNotice` text (1324-1326); exhausted → throw listing attempts (1330) |
| **1333-1427** | `executeInlineAssistant` | routes via `providerRouteForModel(payload.model)` **without `isModelAllowed`** (L1354); any error/HTTP failure/missing key → returns deterministic text with `providerId: "local-fallback"` (1357-1364, 1403-1419) |
| 1429-1451 | `fallbackInlineAssistant` | canned strings; "rewrite" just fixes "teh" and "i" |

### `host/provider-host-service.mjs` (122 lines) [inspected]
- L10-28: file paths under `os.homedir()/ResonantOS_User/{Secrets,ProviderFabric}/…`.
- L46: `createHarnessAdapter` → `createProviderFabricAdapter({ executeRawProviderChat })`.
- L47-120: route table with capabilities: `provider-diagnostics-read` (status/health/connectivity/history/GET routing), `provider-credential-write` (credentials, accounts, accounts/remove), `provider-routing-write` (POST routing-strategies, model-preferences), `provider-model-invoke` (`/augmentor/chat`, `/augmentor/inline`).

### `host/run-bridge-minimal.mjs` (launcher) [inspected]
- L164-177: `createProviderHostService({ redactDiagnosticText, extractJsonObject })`; destructures `providerBridgeRoutes` as `legacyProviderBridgeRoutes`, `readProviderSecrets`, `providerRouteForModel`, etc. and hands them to addon-delegation (L178+), agent-control (L386), browser-diagnostics (L399).
- L404-413: `createHarnessHostService({ userRoot, providerHost, bindings: JSON.parse(process.env.RESONANTOS_HARNESS_BINDINGS ?? "[]"), env })`; `providerBridgeRoutes = harnessService.composeProviderRoutes(legacyProviderBridgeRoutes)` — i.e. only `POST /augmentor/chat` is re-pointed at the harness (`harness-host-service.mjs:444-448`).

### Other call sites that talk to providers directly [inspected]
- `host/agent-control-host-service.mjs:259-306` (`executeControlPlan`) and `:329-390` (`executeNextAction`): `routeForModel(payload.model)` → `secrets[route.providerId]` → POST `${route.apiBaseUrl}/chat/completions` with Bearer. No `isModelAllowed`, no `providerRequestUrl`; a keyless local route throws "credential missing" (L262-264, L332-334), so local models cannot drive agent control.
- `host/memory-ingest-writer.mjs:105-121`: same shape; `if (!route || !credential)` → deterministic fallback.
- `host/browser-diagnostics-host-service.mjs:44-53`: reports boolean presence of the three built-in secrets.
- `host/addon-delegation-service.mjs` (Hermes/OpenCode delegation; other audit area) reads `readProviderSecrets()` at ~11 sites (L1133…2890) — out of scope here but relevant to env-key inheritance.

### Harness layer [inspected]
| File | Key lines |
|---|---|
| `host/harness-host-service.mjs` (458) | `compatibilityChatInput` 61-81 (strict shape; `workload` must be `augmentor-chat`); `createHarnessHostService` 115; `snapshotDshConfig` 122; `createHarnessCredentials` 130; reviewed adapter ids `['dsh-typert-v1','provider-fabric-v1','openai-compatible-v1']` 143; per-boot Ed25519 receipt signer 147-164 (prints fingerprint to stderr L162); demo manifests only when `RESONANTOS_HARNESS_DEMO === '1'` 165-166; `resolveAdapter` 173-265 (provider-fabric 175-181 with readiness = any configured+allowed model; DSH 182-216 incl. native readiness probe; openai-compatible 217-219); `harnessRoutes` 334-385 (`/addons/*`, `/agent/*`, capabilities `addon-runtime-read|control`, `loopbackHostOnly: true`); `executeBridgeChat` 387-405 → **if `!projection.governanceActivated` falls straight through to `providerHost.executeBridgeChat`** (389-392); `executeGovernedChat` 406-442 with a fixed **30 s** deadline (436-439); `composeProviderRoutes` 444-448 |
| `host/harness-registry.mjs` (284) | `bindingAllowed` 20-27 (manifest runtime must match an operator binding exactly; `authScheme: 'none'` + no endpoint needs none); boot-time rollback refusal via watermark 41-98; `eligible` 104-114 (adds adapter capability floor); `authorize` 115-120; `install` 199-218 (refuses manifests that understate the adapter floor, L209); `assignSlot` 261-273 (`governanceActivated = true` once `primary-agent` assigned, L270) |
| `host/harness-registry-store.mjs` (77) | `defaultHarnessStateRoot` 6-10 (win32 → `%LOCALAPPDATA%\ResonantOS`); registry at `<userRoot>/harness-governance/registry.json`, atomic temp+rename, 0o700/0o600 |
| `host/harness-policy.mjs` (75) | `ADAPTER_CAPABILITY_FLOOR` 17-26: provider-fabric → `providers`; openai-compatible/dsh → `network`; native DSH additionally `filesystem`, `shell` (31-33) |
| `host/harness-boundary.mjs` (218) | HMAC-signed session ids 14-24; `createSession` 115-149; `invoke` 158-187 (frames validated, `['final','cancelled','error']` terminal); `operationTimeoutMs` default 30000 (L8) |
| `host/harness-credentials.mjs` (187) | `readSecret` 11-37: source is exactly one of `{env: NAME}` or `{file: abs}`; file must be regular, ≤ 8192 B, `mode & 0o077 === 0`, owned by `process.getuid()` (L21-22); `createNativeCustody` 39-140 (per-epoch record holding `loginToken`, `cookie`, `providerKey`; all registered as redaction strings 48-58); `nativeRefreshByVersion` L142 (only `0.2.0-rc.2: true`); `acquire` 152-185 |
| `host/harness-transport.mjs` (281) | allowlisted routes L8 (`/api/augmentor`, `/api/session/{create,prompt,cancel,page,list,rename,selectModel,modelCatalog}`); `nativeExchange` 73-98 (GET `/?token=…` → expects 303 + one `dsh-auth-*` cookie); plugin-mode `authorize` 99-127 (`x-augmentor-token` → `/api/augmentor/auth` → `/?token=` → cookie); `request` 160-184 (one 401 retry, then `lease.fail`); `openStream` 185-272 (WebSocket `/api/remote.mux`) |
| `host/harness-adapter-contract.mjs` (57) | imports `HARNESS_OPERATIONS` and fixed public error messages from `packages/addon-sdk/src/contracts.ts`; `validateHarnessEvent` 37-57 (text ≤ 65536 B) |
| `host/agent-adapters/provider-fabric.mjs` (46) | wraps `executeRawProviderChat`; yields a single `final` or `error`/`cancelled` frame |
| `host/agent-adapters/openai-compatible.mjs` | `openTransport` 15-38: bearer `actionToken` from the credential lease; SSE reader with 64 KiB text / 1 MiB wire caps (L6) |
| `host/agent-adapters/dsh-typert.mjs` | Typert JSON-RPC (`/api/session/*`), `session/follow` stream; drops `reasoning` parts (L26) |
| `host/dsh-runtime.mjs` (342) | `snapshotDshConfig` 13-29: exactly one `dsh-native-cookie` binding, **platform must be darwin/linux (L18)**, endpoint must match `^http://127.0.0.1:(port)$` with port 1024-65535 and ≠ 19387 (21-22), env passed to child limited to `LANG, LC_ALL, TZ, DEEPSEEK_API_KEY` (L27); `validateDshPrefix` 30-95 (walks the whole npm prefix, ≤ 50000 entries, depth ≤ 64, every node owned by user/root and not group/other-writable; **exact version `0.2.0-rc.2`** L87); `prepareDshHome` 96-159 (managed home with owner marker + lock; child env sets `HOME`, `DSH_HOME`, XDG dirs, `PATH=<node dir>:/usr/bin:/bin`, `DSH_TELEMETRY_MODE: 'DISABLED'` 151-156); `createDshAnnouncement` 160-192 (parses `dsh web: <url>` line, token regex `[A-Za-z0-9._~-]{1,8192}`); spawn L285: `spawnImpl(process.execPath, [bin.js, '--profile','web','--no-open','--host','127.0.0.1','--port',N], { shell:false, cwd, env, stdio:['ignore','pipe','pipe'] })`; stop escalation SIGTERM→SIGKILL at 1 s/2 s/3 s (233-266); `acquire().use()` exposes `{ endpoint, loginToken, providerKey }` L333; 30 s startup deadline (271-273) |
| `host/harness-examples/*.json` | `deepseek-harness-native.json` (`dsh-native-cookie`, endpoint `http://127.0.0.1:3081`, binding `dsh.native`, requests `agent-runtime, network, chat-interface, filesystem, shell`; platforms macOS/linux); `deepseek-harness.json` (`dsh-action-token`, `:3080`, `dsh.main`; +windows); `provider-chat-demo.json` (`provider-fabric-v1`, `authScheme: none`) |

### Extension side (`resonantos-side-panel-extension/src/lib`) [inspected]
- `settings/provider-catalog.js` L22-247: `providerTypePresets` duplicates the host preset list (incl. `anthropic: https://api.anthropic.com` L37-43, `gemini` L44-50, `asus-gx10: http://192.168.1.77:30004/v1` L233-239). `providerRequiresCredential` L259-262: everything except `local` asks for a key.
- `settings/providers-section.js`: credential input is `type="password"`, `autocomplete="off"` (L87-91); "API base URL" field is editable only for custom/local/openai-compatible (L108-111) and is **not marked required**; POST `/providers/credentials` body `{ providerId, credential }` (L474-480); POST `/providers/accounts` with optional `credential` (L198-200, 561-563); model allow-list via `/providers/model-preferences` (L531); health/connectivity buttons (L611, 631). Copy at L697: "Alpha credentials stay in session-only host memory or environment configuration".
- `settings/routing-section.js` L36-153: per-strategy card with primary `<select>`, comma-separated fallback input, cost posture, hard-stop checkbox → POST `/providers/routing-strategies` (L131-141).
- `composer-runtime.js` L2, L44-86: model dropdown defaults to `__auto__` ("Auto route").
- `bridge-client.js` L31-44: route → capability table (mirrors host).
- `background.js` L329-339: inline assistant → POST `/augmentor/inline` with `sanitizeInlineAssistantBody(message.body)`.
- grep for `chrome.storage|localStorage` combined with `credential|secret|apiKey|provider` in `src/` → **no matches** (extension does not persist provider keys).

## Provider list and routing

**Built-in providers** [inspected, `provider-fabric-core.mjs:1-28, 253-347`; high]
| id | type | endpoint | credential | models |
|---|---|---|---|---|
| `shared-minimax` | minimax | `https://api.minimax.io/v1` | `MINIMAX_API_KEY` or session | MiniMax-M3 |
| `shared-zai-glm` | openai-compatible | **`http://127.0.0.1:18789/v1`** (role text: "OpenClaw/Z.AI GLM") | `ZAI_API_KEY`/`GLM_API_KEY`/`ZHIPUAI_API_KEY` or session; sent as Bearer to localhost | zai/glm-5.2 |
| `shared-openai` | openai | `https://api.openai.com/v1` | `OPENAI_API_KEY` or session | gpt-5.5, gpt-5.4-mini |
| `desktop-local` | openai-compatible/local | `RESONANTOS_LOCAL_RUNTIME_URL` or `http://127.0.0.1:11434/v1` | none | batiai/gemma4-e2b:q4 |

**User-addable account presets** [inspected, `provider-bridge-service.mjs:303-412`]: openai; local: ollama, lm-studio, dgx-spark, localai, llama-cpp, vllm, text-generation-webui; openai-compatible: xai, deepseek, mistral, qwen, zai, zai-glm, nvidia-nim, microsoft-azure (empty URL), openrouter, together, huggingface (empty), groq, fireworks, hyperbolic, cloudflare-ai-gateway (empty), litellm, bifrost (empty), asus-gx10, openai-compatible (empty); **anthropic**; **google/gemini**; custom: cohere, ai21, replicate.

**Wire format** [inspected, high]: every request in `provider-bridge-service.mjs` (L1099-1116, 1260-1274, 1379-1396), `agent-control-host-service.mjs` (L300-306, 382-388) and `memory-ingest-writer.mjs` (L117-121) is `POST <apiBaseUrl>/chat/completions`, headers `Authorization: Bearer <key>` (omitted for `none`/`local-runtime`), body `{ model, messages[, reasoning_effort for openai] }`. Response parsed as `choices[0].message.content` (L1051-1063). `grep -rn "x-api-key|anthropic-version|generateContent|/v1/messages" browser-first/host` → no matches. Therefore the `anthropic` and `google` presets produce requests Anthropic/Gemini will reject (wrong path, wrong auth header, wrong body) [hypothesis from the above, high]. Cohere/AI21/Replicate "custom" presets have non-OpenAI base URLs and will also fail for the same reason [hypothesis, high].

**Selection per request** [inspected, `provider-fabric-core.mjs:349-397`, `provider-bridge-service.mjs:1205-1234`; high]
1. If the payload names a model other than `__auto__`/`auto`/`strategy` → `source: "manual"`; must be in the (built-in + account) catalog and allowed by model-preferences, else `reason: "model-disabled"` → chat throws an actionable error (L1209-1214). Exactly one attempt; any failure is thrown (L1249-1253, 1285-1289, 1296-1297, 1304-1305).
2. Otherwise the strategy matching `payload.workload` (default `augmentor-chat`) is used; the chain is filtered to `configured` entries; each is tried in order; the first non-empty reply wins; `routeFallback: true` + `routeNotice` if the answering model ≠ declared primary (L1313-1326).
3. `providerRouteForModel` resolution (L253-310): custom account model with `apiBaseUrl` → own endpoint; else prefix rules; **else MiniMax**.

**Harness path** [inspected]: when a `primary-agent` owner exists (`governanceActivated`), `POST /augmentor/chat` goes to `executeGovernedChat` → `boundary.invoke` → the owner's adapter. For `provider-fabric-v1` that is `executeRawProviderChat` = one attempt, no fallback (`provider-bridge-service.mjs:1203`; `harness-provider-dispatch.test.mjs:168-198` asserts exactly this). Governed errors are reduced to fixed public codes (`Runtime unavailable.` etc.) rather than the provider message [inspected, `harness-adapter-contract.mjs:15-19`].

## Failure handling

- **No retries** anywhere in the provider service; "fallback" means advancing to the next configured route in strategy mode only [inspected, L1244-1331; high].
- Per-attempt timeout via `AbortController` (defaults 90 s chat / 30 s inline / 60 s archive; L55-67, 73-91); timeout error text "`<model> chat request timed out after Ns.`" is appended to the failure list.
- Chat (`executeChat`): manual → throw with Settings guidance; strategy → try next; exhausted → `No provider route returned a reply … Attempts: a | b` (L1330). Provider error message (`responsePayload.error.message`) is forwarded verbatim to the extension (L1294, 1297) — not passed through `redactDiagnosticText` [inspected; low-severity].
- Inline assistant: never throws on provider failure; returns canned text labelled `providerId: "local-fallback"`, `model: "local-inline-fallback"`, with the real error only in `usage.providerError` (L1403-1419). The extension's background handler forwards only `payload.reply` (`background.js:334`), so the user sees degraded text with no error [inspected + hypothesis on UI, medium].
- Archive semantic verifier: returns `semanticStatus: "unavailable"` on any error (L1124-1132, 1147-1156); ingest writer returns `writerStatus: "deterministic-fallback"` (`memory-ingest-writer.mjs:105-113`).
- Governed (harness) chat: 30 s hard deadline (`harness-host-service.mjs:436-439`) and `operationTimeoutMs` 30 s in the boundary (L8) vs 90 s in the legacy path — a governed turn to a slow model can time out where the legacy path would have waited [hypothesis, medium]. `harness-host-service.test.mjs:239` asserts a governed error never falls back to the legacy provider.
- DSH native: child exit → epoch fenced, in-flight turn fails with `runtime-unavailable`, prompt is **not** replayed (`dsh-runtime.mjs:287-295`; operator message `exit` L209); next explicit chat starts a new epoch (`dsh-native-integration.test.mjs:160`).

## Credentials

**Where keys come from** [inspected, high]
1. `process.env`: `MINIMAX_API_KEY`, `OPENAI_API_KEY`, `ZAI_API_KEY|GLM_API_KEY|ZHIPUAI_API_KEY` (`provider-bridge-service.mjs:50-54, 140-149`) and a JSON blob `RESONANTOS_PROVIDER_SECRETS_JSON` mapping any provider id → credential (L151-165).
2. Extension POST `/providers/credentials` or `/providers/accounts` (`credential` field) → `sessionProviderSecrets.set(providerId, credential)` (L178-180, 903, 932). Session values override env (L171-176).
3. Harness bindings (`RESONANTOS_HARNESS_BINDINGS`, operator env): per binding `source: {env: NAME}` or `source: {file: /abs/path}` (`harness-credentials.mjs:11-37`), used as the DSH plugin action token or the openai-compatible bearer.
4. DSH native: `DEEPSEEK_API_KEY` from the bridge env is forwarded into the child's env (`dsh-runtime.mjs:27, 151-152`) and exposed to the lease as `providerKey` (L333), registered as a redaction string (`harness-credentials.mjs:57`).

**Persistence / encryption** [inspected, high]: none for provider keys. `credentialStoreStatus` reports `"Session-only host memory / environment; no provider secrets are persisted by the alpha host."` (L189). The legacy path `~/ResonantOS_User/Secrets/provider-secrets.json` is only checked with `existsSync` to set `legacyPlaintextDetected` (L191) and is never read (test `provider-bridge-session-secrets.test.mjs:82-103`). Non-secret config (`provider-accounts.json`, `routing-strategies.json`, `model-preferences.json`, `diagnostics-history.json`) is written plaintext with `mode 0o600` + `chmod` (L495-500, 600-604, 853-856, 886-889). Harness registry: `<userRoot>/harness-governance/registry.json` plus a machine-local watermark.

**Do keys reach the extension?** [inspected, high] No. Status returns `credentialPreview: "session"|"missing"` (L660) and `configured` booleans; `provider-route-acceptance.test.mjs:117-128` asserts the raw credential string is absent from status/health/connectivity payloads. The key does traverse extension → bridge once, in the POST body (`providers-section.js:474-480`); transport security of the bridge (TLS/token) is another area (`bridge-tls.mjs`, `bridge-capability-tokens.mjs`).

**Redaction** [inspected]: `browser-first-host-utils.mjs:34-43` regexes (`sk-…`, `Bearer …`, `api_key=`, `token=`, `secret=`, home dir) are applied only to diagnostics-history `detail` (L596) and connectivity network errors (L809). Harness leases use `sanitizeOpenCodePayload` with the exact secret + base64/base64url forms (`harness-credentials.mjs:162-180`). No `console.*` calls in the three provider files (grep empty).

**Weaknesses (documented, not exploited)**
- W1 [inspected, high]: keys live in `process.env` of the bridge; any child process spawned by other host services (Hermes, OpenCode, DSH plugin mode) inherits env unless explicitly scrubbed. Native DSH explicitly limits inherited vars (`dsh-runtime.mjs:27`); whether Hermes/OpenCode spawns scrub them is outside this area (see `addon-delegation-service.mjs`).
- W2 [inspected, high]: the built-in `shared-zai-glm` profile sends a Bearer key to a hard-coded **localhost** port `18789` (`providerConnectivityTarget` L330-336 `sendsCredential: true`), relying on whatever process listens there (intended: an "OpenClaw" gateway). `allowsLocalProviderEndpoint` whitelists it by id (L247).
- W3 [inspected, medium]: `RESONANTOS_PROVIDER_ALLOW_LOCAL_ENDPOINTS=1` (L245) disables the private-host guard for all credential-bearing providers.
- W4 [hypothesis, medium]: POSIX permission hardening (`0o600`, `mode & 0o077`, `process.getuid()`) is a no-op or fails on Windows: `harness-credentials.mjs:21-22` guards `getuid` with `typeof` but Node on win32 reports `mode` without a meaningful 0o077 clear, so `{file: …}` secret sources would be refused on Windows; `dsh-runtime.mjs:11` calls `process.getuid()` unguarded (only reachable after the darwin/linux check at L18).
- W5 [inspected, low]: provider error bodies are relayed to the extension unredacted (L1294).
- W6 [inspected, medium]: any model string not in the catalog resolves to MiniMax (`provider-fabric-core.mjs:303-309`). In chat this is blocked by the catalog check; in the inline assistant (L1354) and agent-control (L259-262) it is not, so an arbitrary `model` value is sent to MiniMax with the MiniMax key. User accounts saved with an empty endpoint (azure/huggingface/cloudflare/bifrost/openai-compatible presets default to `""` and the UI field is not required) contribute catalog models that fall through to MiniMax too — a silent misroute to a different vendor with a different key. No test covers this.

## Tests table

Runner: `scripts/run-browser-first-extension-tests.mjs:11-14` collects only `*.test.mjs` under `browser-first/test` and runs `node --test --test-concurrency=1`. `npm run verify:alpha` (`scripts/verify-alpha.mjs:17`) invokes `test:browser-first`; `.github/workflows/alpha-build.yml:51` runs `verify:alpha`. `*.live.mjs` and `live-*.mjs` drivers are separate npm scripts (`package.json:18-21`) and are referenced by `agent-control-live.yml` path filters only; the DSH live drivers are referenced by no workflow (grep `DSH_LIVE|dsh-native.live` in `.github/` → none).

| File | Kind | Asserts (one line) | Skipped / mocked? |
|---|---|---|---|
| `provider-fabric-core.test.mjs` (208) | unit | strategy chain ordering, disabled-model blocking, hard-stop returns no route, local final fallback, connectivity targets | pure functions, no I/O |
| `provider-host-service.test.mjs` (38) | unit | route table has expected paths and capabilities | shape-only (near-tautological) |
| `provider-bridge-session-secrets.test.mjs` (317) | unit/integration (tmp dir) | session-only save, legacy plaintext ignored, env keys, endpoint policy, strategy timeout → next route, archive/inline timeout handling | `globalThis.fetch` replaced; env scrubbed |
| `provider-fallback-visibility.test.mjs` (129) | integration (tmp dir) | #231: manual model preserved; disabled/unknown model errors; `routeFallback`/`routeNotice` set when primary unconfigured or failing | fetch stub per URL (L42) |
| `provider-route-acceptance.test.mjs` (128) | integration | #233: status/health/connectivity states; chat with no route errors; no raw credential in payloads | fetch stub; "no live provider secrets" (L3) |
| `provider-fabric-routing-propagation.test.mjs` (162) | integration | #207: added account model appears in routing, persists as primary, chat hits the account's endpoint "not MiniMax", removal cleans overrides | fetch stub |
| `local-provider-chat.test.mjs` (219) | integration | keyless Ollama account routable, `/v1` normalization, inline routes to local provider, connectivity probe without key | fetch stub (L40) |
| `augmentor-chat-provider-boundary.test.mjs` (144) | integration | every route sends page context only inside a valid user turn; fallback attempts reuse same messages | fetch stubbed (L89) |
| `provider-catalog.test.mjs` (59) | unit (extension) | preset list contains categories; label/model parsing | none |
| `providers-section-modal.test.mjs`, `provider-dialog-lifecycle.test.mjs`, `settings-routing-drafts.test.mjs` | unit (extension DOM) | dialog stays open on error, drafts survive sibling saves | DOM via jsdom-like harness; bridge stubbed |
| `harness-provider-dispatch.test.mjs` (271) | integration | owner dispatches once, no fallback after denial; raw body > 1 MiB → bounded error; compatibility chat retains fallback | `t.mock.method(globalThis,'fetch')`, `fakeDsh` adapter (L50-55), `os.homedir` mocked |
| `harness-host-service.test.mjs` (705) | integration | routes enforce transport/addon authority; governed errors never retry/fall back; receipts signed; rollback refusal | `t.mock.fn` adapters, console mocked |
| `harness-registry.test.mjs` (805), `harness-boundary.test.mjs` (456), `harness-policy.test.mjs` (136), `harness-manifest.test.mjs` (101), `harness-event-bus.test.mjs` (74) | unit | registry CAS/rollback/watermark; boundary fencing; capability floor; manifest validation | in-memory stores; `t.mock.timers` |
| `harness-credentials.test.mjs` (71) | unit | binding names don't confer secrets; file source must be private regular file, bounded | tmp files; POSIX mode semantics |
| `harness-transport.test.mjs` (312) | unit | action token/cookie flow, pinned destinations, no redirect following, one 401 retry | injected `fetchImpl`/`WebSocketImpl` |
| `openai-harness-adapter.test.mjs` (240) | unit + loopback | SSE parsing bounds, redaction across frames, one real loopback HTTP server (L123) | mostly injected transport |
| `dsh-harness-adapter.test.mjs` (222), `dsh-harness-stream.test.mjs` (302) | unit | Typert request shapes, catalog decoding, reasoning parts dropped | fake transport |
| `dsh-native-runtime.test.mjs` (450), `-credentials` (168), `-transport` (241), `-host` (170), `-boundary` (126), `-policy` (93), `-readiness` (58), `-shutdown` (103), `-final-fixes` (125), `-browser-contract` (137) | unit | prefix validation, announcement parsing, lease/epoch semantics, stop clock, port refusal | `dsh-native-fake-child.mjs` stand-in; `spawnImpl` injected |
| `dsh-native-integration.test.mjs` (225) | integration | two sessions share one child; crash fails once, no replay; signed receipts | fake child process |
| `dsh-native-docs.test.mjs` (14) | docs check | `harness-adapter-demo.md` contains listed phrases | asserts documentation strings, not behaviour |
| `harness-swap-demo.test.mjs` (391) | unit/CLI | fixture evidence bundles verify; "Fixture evidence verified; not live proof" (L207) | self-described synthetic input (L61-62) |
| `harness-swap-demo-bridge.live.mjs` (32) | **live lane** | fixture demo through real bridge + Playwright Chromium, port 1430 | not in default gate (L14-15); "never skips: absent browser = red" |
| `dsh-native.live.mjs` (750), `dsh-native-browser.live.mjs` (538) | **conductor-only live drivers** | real `@deepseek-ai/dsh@0.2.0-rc.2` prefix, `DEEPSEEK_API_KEY`, Chrome for Testing | "NOT a node:test file" (header); not in CI |
| `live-sdk-lane.mjs` / `.test.mjs`, `live-harness.mjs` | live (OpenCode/Agent Control) | extension staging, leak scanning; not provider-specific | Playwright; `agent-control-live.yml` |

`grep -nE "\.skip|\.todo"` across provider/harness/dsh tests → no `skip`/`todo` markers; mocking is pervasive (fetch, spawn, homedir, timers).

## Downgrades found

1. **Anthropic / Google / Cohere / AI21 / Replicate presets are non-functional** [inspected + hypothesis, high]. Presets exist in host (`provider-bridge-service.mjs:367-403`) and extension (`provider-catalog.js:37-50, 86-99, 135-141`), but the only wire path is OpenAI `/chat/completions` + Bearer; no Anthropic/Gemini request code exists; no test exercises these presets. Direct Claude/Gemini use is only possible through an OpenAI-compatible gateway (OpenRouter, LiteLLM, etc.).
2. **"Archive Ingest" routing strategy and its hard-stop are not consulted** [inspected, high]. `providerRouteForArchiveVerifier` (L1034-1049) hard-codes gpt-5.5 → zai → MiniMax by secret presence; `runArchiveSemanticVerifier`/`runArchiveIngestWriter` (L1071, 1174) use it; nothing calls `providerRouteForWorkload("archive-ingest")` (grep). The UI card (`routing-section.js`) saves overrides that have no consumer for this workload. `memory-source-settings-service.mjs:30` labels cost posture `"use-archive-ingest-routing-strategy"`.
3. **Allowed-model policy enforced only in `executeChat`** [inspected, high]. Inline assistant (L1354), archive verifier (L1036), agent-control planner/next-action (`agent-control-host-service.mjs:259-262, 330-333`) route by raw model string. A model "disabled" in Settings is still callable via these routes.
4. **Harness governance is opt-in and off by default** [inspected, high]. Without an installed manifest + `primary-agent` assignment, `/augmentor/chat` is the legacy path (`harness-host-service.mjs:389-392`); demo manifests require `RESONANTOS_HARNESS_DEMO=1` (L165); bindings require operator env JSON (`run-bridge-minimal.mjs:409`). The signed-receipt/"certification" machinery therefore governs nothing in a stock install.
5. **Native DSH is macOS/Linux-only, exact-version-pinned, and live-certified only by out-of-CI scripts** [inspected, high]. `dsh-runtime.mjs:18` refuses win32; L87 refuses any version but `0.2.0-rc.2`; docs admit eligibility "in two of three conductor prerequisite runs" (`docs/addons/harness-adapter-demo.md` native section) [reported]. Commit `5b26f7c` claims "all 13 observations passing" [reported, unverifiable here].
6. **"Z.AI GLM" built-in is a localhost proxy, not a cloud endpoint** [inspected, high]. `apiBaseUrl: http://127.0.0.1:18789/v1` (`provider-fabric-core.mjs:16, 298, 333`) while catalog says `runtime: "cloud"` (L44). Without a local OpenClaw/GLM gateway the second hop of every default strategy is dead.
7. **Developer LAN host baked into shipped presets** [inspected, high]: `asus-gx10: http://192.168.1.77:30004/v1` (`provider-bridge-service.mjs:355`, `provider-catalog.js:237`).
8. **Silent misroute to MiniMax for unresolvable models** [inspected, medium] — see W6.
9. **Inline assistant degrades silently** [inspected, medium] — returns canned text labelled `local-fallback` on any provider error; extension forwards only `reply`.
10. **Unredacted provider error text to client** [inspected, low] — L1294/1297.
11. **Tests never touch a real provider** [inspected, high]; `provider-host-service.test.mjs` is a route-table shape test; `dsh-native-docs.test.mjs` tests doc wording; `harness-swap-demo.test.mjs` verifies self-generated fixtures.
12. **Governed path shortens the timeout to 30 s** [hypothesis, medium] — vs 90 s legacy.
13. **Duplicated preset catalogs** [inspected, high]: host `providerPreset` (L303-412) and extension `providerTypePresets` (`provider-catalog.js:22-247`) are maintained separately; they already differ (extension `anthropic` base `https://api.anthropic.com` vs host `…/v1`; extension `gemini` lacks `/v1beta`). Host is authoritative at save time.

## Coupling

- **Node-only**: `node:fs/promises`, `node:child_process` (`spawn`), `node:net`, `node:crypto` (Ed25519 sign, HMAC), `node:async_hooks` `AsyncLocalStorage`, `process.getuid`, global `fetch`, `AbortSignal.any`, `Response.headers.getSetCookie()`, `import.meta.dirname`; `package.json:42-43` requires `node >= 24.21.0`. Harness contract imports TypeScript sources directly (`harness-adapter-contract.mjs:3-4` → `packages/addon-sdk/src/*.ts`), implying Node type-stripping.
- **POSIX-only**: `dsh-runtime.mjs` (darwin/linux gate L18; uid/mode checks L11-12, 116-143; `PATH=…:/usr/bin:/bin` L155; walks to `/` L38); `harness-credentials.mjs:21-22` file-mode checks; `0o600` chmods in provider service are ineffective on NTFS.
- **Chrome-only**: extension side (`chrome.*` in `background.js`); host modules in this area have no Chrome dependency.
- **Hard-coded vendor/network constants**: `https://api.minimax.io/v1`, `https://api.openai.com/v1`, `http://127.0.0.1:18789/v1` (Z.AI/OpenClaw), `http://127.0.0.1:11434/v1` (Ollama), `http://192.168.1.77:30004/v1`, `http://dgx-spark.local:11434/v1`, plus ~20 vendor base URLs in `providerPreset`; DSH: `@deepseek-ai/dsh` `lib/bin.js`, Typert routes `/api/session/*`, `/api/remote.mux`, cookie prefix `dsh-auth-`, reserved desktop port `19387`, `DEEPSEEK_API_KEY`. Model names are vendor-specific strings (`gpt-5.5`, `MiniMax-M3`, `zai/glm-5.2`, `batiai/gemma4-e2b:q4`).
- **Env surface**: `RESONANTOS_PROVIDER_SECRETS_JSON`, `RESONANTOS_PROVIDER_ALLOW_LOCAL_ENDPOINTS`, `RESONANTOS_LOCAL_RUNTIME_URL`, `RESONANTOS_PROVIDER_{CHAT,INLINE,ARCHIVE}_TIMEOUT_MS`, `RESONANTOS_HARNESS_BINDINGS`, `RESONANTOS_HARNESS_DEMO`, `RESONANTOS_DSH_PACKAGE_ROOT`, `RESONANTOS_DSH_HOME`, vendor `*_API_KEY`.

## Open questions

1. Does the bridge transport (TLS, capability tokens — `bridge-tls.mjs`, `bridge-capability-tokens.mjs`) protect the one-time `/providers/credentials` POST adequately? (Other audit area.)
2. Do Hermes/OpenCode child spawns in `addon-delegation-service.mjs` inherit `OPENAI_API_KEY` etc. from `process.env`? (W1; other area.)
3. What does the native DSH child do with `DEEPSEEK_API_KEY` — is it the provider key for DeepSeek calls made by `dsh`? Docs say "No provider key is required for protocol readiness" [reported].
4. Does the extension UI ever send `model: "auto"` to `/augmentor/inline`? If so `providerRouteForModel` returns `null` and L1355 dereferences it (`route.authType`) → TypeError [hypothesis, low; `sanitizeInlineAssistantBody` not inspected].
5. Is there any consumer of the `agent-control`, `routine-delegation`, `recovery-engineer` strategies besides `executeChat`'s `payload.workload`? `compatibilityChatInput` only admits `workload: 'augmentor-chat'` on the governed path (`harness-host-service.mjs:64`); the legacy path accepts any workload string.
6. Were the PR #534 live observations (commit `5b26f7c`) recorded anywhere in-repo (e.g. `final-gate.json`)? Not found in this pass.
