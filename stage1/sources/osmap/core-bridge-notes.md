# Core bridge and extension notes (osmap lead, inspected 2026-10-20 @578fbbc)

## Launch chain
- `run-bridge-minimal.mjs` (root, 3 lines) re-exports `browser-first/host/run-bridge-minimal.mjs` (509 lines).
- Launcher composes services (lines 164-413), builds route list (415-424), mints tokens (426-430), optional self-test mode (441-460, exits), checks extension manifest exists (462-465), starts server with port fallback (468-477), writes `src/bridge-config.generated.js` into the extension dir (482-488), installs shutdown (502-509).
- Hard-coded extension ID `cdpdmmalhmokbfcfgogoepnjplaakgnl` -> `extensionOrigin` (lines 67-68); manifest.json carries the matching `key` so the unpacked extension ID is stable.
- User root: `~/ResonantOS_User` or `RESONANTOS_BROWSER_FIRST_USER_ROOT` (90-92); Memory under `<root>/Memory`, BrowserFirst under `<root>/BrowserFirst`.

## Tokens
- `bridgeToken`, `capabilityBootstrapToken`: 32 random bytes base64url (`createBridgeToken`, bridge-server.mjs:191-193), or pinned via CLI arg / env var (launcher 426-429).
- 26 per-capability tokens, one per capability, from `BRIDGE_CAPABILITY_TOKEN_SPECS` (bridge-capability-tokens.mjs:23-50); each may be pinned by `--<arg>` or env var, else minted (62-73).
- Tokens are process-lifetime static strings. No expiry, no per-session binding, no nonce/replay protection, no revocation other than restarting the bridge. Comparison is constant-time (bridge-server.mjs:195-204).
- Generated config (bridge-server.mjs:1169-1199): `{bridgeUrl, httpsBridgeUrl, bridgeToken, capabilityBootstrapToken}` written mode 0600 to `browser-first/resonantos-side-panel-extension/src/bridge-config.generated.js` (gitignored, .gitignore:77). Raw capability tokens are NOT written there.
- Bootstrap: `POST /api/capability-tokens` (bridge-server.mjs:1281-1289) requires bridge token + bootstrap token; returns tokens for requested capability names (`scopedCapabilityTokenPayload` 1214-1236; max 80 names; unknown name -> error).
- Extension requests the FULL allowlist on every service-worker start: `initCapabilityTokens` posts `RUNTIME_CAPABILITY_ALLOWLIST` (bridge-client.js:636-672; allowlist = all values of the route map, line 141). So in practice one principal (the extension SW) holds all 26 tokens in memory. Scoping separates the config file from the raw tokens; it does not separate privileges between components or users.
- Generated-config tokens take precedence over runtime-fetched ones (bridge-client.js:600-612).

## Authorization pipeline (bridge-server.mjs)
- `createBridgeRequestHandler` 1267-1365: OPTIONS -> 204; client IP allowlist (`clientIpAllowed`, 184-189, enforced at 1318; empty list = allow all); dashboard proxy dispatch for mirror paths (1310-1313); `authorizeBridgeRoute` (114-137): bridge token -> route exists -> bootstrap token if required -> DEFAULT DENY for routes without capability (125-126) -> capability token -> loopback Host header check for `loopbackHostOnly` routes (`validateLoopbackHost` 101-113) -> Origin check only for `errorFamily === 'harness'` routes (130-133).
- Origin/CORS: `bridgeCorsHeaders`/`pickAllowedOrigin` (312-355); for non-harness JSON routes the Origin header is used only to pick CORS response headers, not to reject. Enforcement for those routes relies on the token secret and loopback binding.
- Default bind 127.0.0.1 (`getBridgeHost` 1098-1100); `RESONANTOS_BRIDGE_HOST=0.0.0.0` exposes to LAN over plain HTTP unless TLS set up (bridge-tls.mjs, self-signed CA under `~/ResonantOS_User/BridgeTLS`).
- Port fallback: `startBridgeServerWithFallback` 1556-1618 retries on EADDRINUSE with fallback port 0 (ephemeral) and reports `recovered`.

## Unauthenticated path on the bridge listener (disconfirmation)
- `DASHBOARD_PROXY_MIRROR_PATHS` (228-236): `/hermes-dashboard`, `/auth`, `/api`, `/assets`, `/fonts-terminal`, `/dashboard-plugins`, `/favicon.ico` are reverse-proxied to a Hermes dashboard on 127.0.0.1:9119 (`dashboardProxyPort` 264-270).
- `getBridgeOpenProxyPrefixes` (1160-1167): when the bind host is loopback (the default) ALL mirror prefixes are "open", i.e. exempt from the bridge token (`createAddonProxyHandler` 766-786). IP allowlist is empty by default -> no gate at all. Exact registered JSON route paths are excluded from proxying (`reservedInternalPaths`, 1294, 1311), so bridge routes themselves stay token-gated.
- Consequence: any local process or any web page (via no-cors request from the browser) can reach the Hermes dashboard through the bridge port without a bridge token when Hermes is running. Hermes' own session cookie is the only remaining control. Tested as intended behaviour: dashboard-proxy.test.mjs:120 "allows iframe src dashboard mirror paths on loopback by default". WebSocket upgrades take the same exemption (525+, 1431-1448).

## Extension side
- Service worker `background.js` (378 lines): config resolution order (comment 53-78): chrome.storage.local override `bridgeTargetOverride` -> generated config -> default `http://127.0.0.1:47773`; loopback probe `detectLoopbackBridge`; `initCapabilityTokens` on load, onInstalled, onStartup (246-255). No chrome.alarms; bootstrap retried only on SW restart or message events.
- `chrome.runtime.onMessage` (287-377) rejects senders with a different extension id (288-291); channels: `resonant-context-snapshot`, `active_tab_context`, `inline_assistant_request` (-> bridge `/augmentor/inline`), `open_side_panel`, `browser_control_handoff`, `action_request`.
- `action_request` handler (354-366) answers from `APPROVAL_REQUIRED_ACTIONS` = {wallet_connect, wallet_sign, wallet_switch_network, public_submit, sensitive_type, credential_autofill} (33-40): it is an advisory classification returned to the caller, not an enforcement point by itself.
- Settings override: a user-entered bridge URL may inherit the generated bridge token and bootstrap token (bridge-server.test.mjs:411 "tokenless overrides inherit generated credentials") and tokens are then stored in chrome.storage.local (ALPHA_RUNTIME_BOUNDARY.md:40-48). `validateBridgeTargetUrl` (bridge-client.js:173) restricts to absolute http(s) without userinfo/query/fragment. Risk: credentials sent to any operator-typed host.
- Manifest CSP connect-src allows `http://*:*` and `https://*:*` (manifest.json content_security_policy) -> extension pages may connect anywhere; host_permissions all http/https; content scripts on all frames of all pages.

## CI (reported by CI, not executed)
- alpha-build run 39097845387 @578fbbc (2026-10-18, push): success. verify:alpha lanes: test:docs 293/293; vitest 48 files 724 tests pass; test:dev-bridge-config 34; test:browser-first 2424 tests, 2414 pass, 10 skipped (all skipped are live-prereq lanes: macOS sandbox-exec isolation test, 8 live-SDK OpenCode fault lanes, 1 Chrome-required); test:browser-host 13; living-archive-mcp 4; living-archive-memory-service 7; health 30; engineer-runner 12; security-pipeline 96; module-ownership 2; pre-release:scan pass.
- agent-control-live-certification run 39225094790 @578fbbc (2026-10-19, schedule): success; job "Agent Control live-browser certification" (Chrome for Testing 155, xvfb) 1 node test pass + settings-shapes pass + harness swap demo; job "Live SDK certification" 29/29 pass with pinned opencode-ai@1.18.32 installed from npm.
- security-observe run 39097845328: 4 jobs pass (private key material, workflow allowlist hygiene, subprocess no shell-string, security-pipeline registry observe non-gating).
- security-drift and project-issue-sync scheduled runs pass (6-hourly).
