# ResonantOS 2.0.0 Alpha — Browser control (non-agent), per-site permissions, content scripts, user data, diagnostics, extension prefs

- Repo: `_untrusted/resonantos-2.0.0-alpha` @ `578fbbc3c1c854b192318b3d2163b138fb45d8bd` (branch dev). Verified 2026-10-20, static reading only (no npm/node run).
- Paths below are relative to `browser-first/` unless prefixed. `ext/` = `browser-first/resonantos-side-panel-extension/`.
- Legend: **[inspected]** = code read; **[reported]** = what docs/comments claim; **[hypothesis]** = my inference. Confidence high/medium/low per claim.
- Scope exclusion: agent-control-*, control-step-executor, browser-job-* are covered by another agent and only mentioned where they share a gate.

## 1. Summary

The extension is MV3 with broad `host_permissions` (`http://*/*`, `https://*/*`) and a content script injected into every http(s) page and every frame (`ext/manifest.json:14-15,25-33`) **[inspected, high]**. Non-agent page actions available from the side panel are: open URL, web/news search, read page (merged across frames), get selection, detect forms, click visible text/control ref, type into a field (optionally `requestSubmit`), scroll, visual "Resonator" overlays, and a control-session overlay (`ext/src/lib/browser-page-actions.js:168-218, 391-521`; `ext/src/content.js:1434-1548`).

Per-site permission has four string modes (`blocked`, `read-only`, `ask-before-action` (default), `trusted-for-safe-actions`) stored in `chrome.storage.local["augmentorSitePermissions"]` keyed by hostname-sans-www (`ext/src/lib/site-permission-store.js:7-13,54-59`). **Enforcement lives in the side-panel/main-workspace page code (`sendContentAction`, `browser-page-actions.js:322-338`) and in the content script for the inline-assistant UI only (`content.js:1068-1078, 1239-1243`). The background service worker enforces nothing per-site; its `action_request` handler is advisory (`background.js:362-374`).** Only `blocked` and `read-only` have behaviour; `ask-before-action` and `trusted-for-safe-actions` are indistinguishable for direct `/browser click|type|scroll` commands — no confirmation ceremony exists on that path (`side-panel-browser-action-controller.js:87-96`) **[inspected, high]**. Navigation (`openBrowserUrl`, `searchBrowser`) and `/dao` helper tab-scanning bypass site permission entirely (`browser-page-actions.js:168-218; 684-698` with `includeBlocked: true`).

Hard-coded human-only boundaries (submit-like controls, credential/payment/login/personal fields, destructive verbs) are enforced in the content script and cannot be bypassed by `userApproved` (`content.js:448-532, 796-860`; `content-field-safety.js:44-116`) **[inspected, high]** — these are the strongest guards in this area. They are heuristic (label/attribute regexes) so a mislabeled control defeats them **[hypothesis, medium]**.

User data: ~30 `chrome.storage.local` keys (chats, messages, attachments, site permissions and audit, consents, prefs); nothing in `storage.session`/`storage.sync`; no encryption at rest in the extension (no `crypto`/`encrypt` hits in `ext/src`). Bridge host writes under `~/ResonantOS_User/{Memory,BrowserFirst,ExtensionPrefs,Secrets}`; several JSON files are written with `mode: 0o600` (a no-op on Windows) but no encryption. Deletion/export: per-chat delete exists; a "diagnostics report export" writes a redacted JSON to `~/ResonantOS_User/BrowserFirst/Diagnostics/`; there is no retention policy, purge, or data-export feature for chats/permissions/history.

Incognito: not excluded anywhere except the `/history ... tabs` listing (`app-command-handlers.js:372`). Manifest has no `incognito` key, so behaviour follows Chrome's default (`spanning`) if the user enables the extension in incognito **[inspected, high]**.

Freshness: there is no DOM hash / "page changed since plan" check in the non-agent path. The only `MutationObserver` schedules a *telemetry* snapshot to the background (`content.js:135-143`); the side panel's cached snapshot is invalidated only by tab id/URL change (`browser-page-actions.js:356-389`) **[inspected, high]**.

## 2. Files / functions with line ranges

| File | Key functions (lines) | Role |
|---|---|---|
| `ext/manifest.json` | permissions 14; host_permissions 15; CSP 16-18; content_scripts 25-33 (`all_frames: true`, `document_idle`) | MV3 manifest; `clipboardRead/Write`, `history`, `scripting`, `sidePanel`, `storage`, `tabs`, `webNavigation`, `activeTab` |
| `ext/src/background.js` (378) | `loadBridgeConfig` 8-28; `rebindAndHydrate` 86-114; `rememberResonantContextSnapshot` 222-241; `onMessage` 287-378 (`action_request` 362-374) | SW: bridge client bootstrap, side-panel open/handoff, context snapshot cache (max 40 tabs, 236-239), message router |
| `ext/src/lib/background-message-policy.js` (237) | `redactSecrets` 9-24; `safeUrl` 34-48; `isTopFrameSender` 180-182; `sanitizeInlineAssistantBody` 184-193; `sanitizeResonantContextSnapshot` 195-237 | Bounds/redacts payloads from content scripts before caching/forwarding |
| `ext/src/content.js` (1550) | SDK init + snapshot scheduler 26-145; `isSubmitLikeElement` 448-466; `isHardRestrictedElement` 468-496; `clickElement` 507-559; `setNativeValue` ~740-749; `formIsSafeToAutoSubmit` 754-794; `typeIntoPage` 796-871; `scrollPage` 873-890; `currentSitePermission` 1068-1078; inline assistant action handler ~1225-1312; `onMessage` 1434-1548 | Page-side executor for all DOM reads/mutations and the inline selection assistant |
| `ext/src/lib/browser-page-actions.js` (1117) | `readOnlyAllowedContentActions` 14-20; `activeTab` 137-166; `openBrowserUrl` 168-185; `searchBrowser` 187-218; `sendContentActionToFrames` 245-268; `injectContentScripts` 282-289; `readSpecificTabPage` 291-320; `sendContentAction` 322-354; `hydrateCachedTabSnapshot` 364-389; `typeIntoActivePage` 431-454; `clickActivePageText` 456-476; `scrollActivePage` 478-492; `detectWalletState` 567-637 (MAIN-world `executeScript` 589-615); `prepareDaoWorkflowGuidance` 664-729; `saveResearchTrailToArchive` 921-1013 | Side-panel-side orchestration + the per-site gate |
| `ext/src/lib/site-permission-store.js` (95) | `siteKeyForUrl` 7-13; `readSitePermissions` 20-30 (fails closed with code `site-permissions-unavailable`); `appendAudit` 37-52 (20 entries/site); `permissionForUrl` 54-59; `setSitePermission` 61-70; `resetSitePermission` 72-84 | Storage wrapper, no validation of `mode` string (66) |
| `ext/src/lib/side-panel-command-router.js` (156) | `respondToCommand` 20-151 | Slash + natural-language dispatch; `/site` 51, `/history` 53, `/wallet` 54-57, `/browser` 71 |
| `ext/src/lib/side-panel-browser-action-controller.js` | `/browser` subcommands 78-100 | click 87-91, type 92-96 (submit if text matches `submit|press enter|hit enter|search`), scroll 97-100 — no confirmation |
| `ext/src/lib/app-command-handlers.js` (669) | `sitePermissionModeFromText` 90-96; `runSitePermissionCommand` 308-328; `runHistorySearchCommand` 345-420 | `/site`, `/history` (uses `chrome.history.search`, excludes incognito tabs 372, can save to archive 394-420) |
| `ext/src/lib/side-panel-lifecycle-controller.js` | site-permission `<select>` change handler 153-170 | UI setter for mode |
| `ext/src/lib/resonator.js` (295) | `injectStyles` 35-69; `highlight` 118-137; `arrow` 139-183; `spotlight` 185+; `clear` 105-116 | Visual guidance overlays (outline/arrow/spotlight), inline styles, `data-resonantos-owned` |
| `ext/src/lib/control-overlay.js` (228) | `ensureControlOverlay` 48-115; `pulseControlOverlay` 143-186; `setControlSessionOverlay` 187-215 | Fixed-position overlay/toast with Stop button (104-106), `pointer-events: none` except toast |
| `ext/src/lib/content-field-safety.js` (121) | `classifyEditableField` 44-116 | Field risk classes: credential/payment/login/personal-contact (not typeable), search-query (type+submit), document-edit (type only), unknown (refuse) |
| `ext/src/lib/content-inline-actions.js` (28) | action list 3-14 | Inline assistant buttons incl. `send`, `insert` |
| `ext/src/lib/content-inline-action-surface-gate.js` (44) | `inlineActionAllowedForLocationGate` 24-34 | Refuses chrome://, about:, extension pages etc. |
| `ext/src/lib/content-control-refs.js` (46) | `createControlRefStore` 8-40 | Writes `data-resonantos-control-ref` attributes onto page elements (DOM mutation) |
| `ext/src/lib/tab-context-controller.js` (233) | `bindMentionedTab` 50-60 (activates tab 54); `consumeInlineDraft` 62-75 (removes `augmentorInlineDraft`); listeners 92-96 | @tab mentions, inline draft handoff |
| `ext/src/lib/resonant-context.js` (924) | form tracking 185-300 (`ALWAYS_IGNORE` password 185); redaction 343-390; session history w/ `sessionStorage` 400-584 | Page-side context SDK; persists nav/click trail in page `sessionStorage` (redacted) |
| `ext/src/lib/context-plugins.js` (360) | domain plugins | Per-domain selectors for context |
| `ext/src/lib/trace-redaction-core.js` (105) | `redactTraceText` 44-60+ | Shared redaction for durable traces |
| `ext/src/lib/chat-session-store.js` (894) | `persist` ~195-212; hydrate 218-268; `deleteSession` 661 | Chats/messages/attachments in `chrome.storage.local` |
| `ext/src/lib/prefs-sync.js` (289) | `DEFAULT_SYNCED_KEYS` 30-34+ | Mirrors `augmentorUserProfile`, `augmentorConfig`, `augmentorModel`, `augmentorThinkingDepth` (+ more, 30-40) to bridge `/settings/extension-prefs` |
| `host/run-bridge-minimal.mjs` (509) | `userRoot` 90-92; `memoryRoot` 94-96; `browserFirstRoot` 122-124; diagnostics wiring 376-390; prefs wiring 403 | Host entry; `RESONANTOS_BROWSER_FIRST_USER_ROOT` override |
| `host/extension-prefs-host-service.mjs` (176) | `prefsFilePath` 26-28; `scheduleWrite` 84-108 (150 ms debounce, `mode: 0o600`); routes 161-174 | `~/ResonantOS_User/ExtensionPrefs/extension-prefs.json`, 1 MB cap (24) |
| `host/bridge-server.mjs` | `writeBridgeConfig` 1169-1199 | Writes `ext/src/bridge-config.generated.js` with `bridgeUrl`, `httpsBridgeUrl`, `bridgeToken`, `capabilityBootstrapToken` (mode 0o600) |
| `host/browser-diagnostics-host-service.mjs` (121) | `executeSystemStatus` 43-62; routes 82-119 | `/status`, `/workspace/inspect`, `/browser/downloads`, `/browser/launch-diagnostics`, `/browser/downloads/action`, `/diagnostics/report` |
| `host/browser-diagnostics-service.mjs` (505) | `diagnosticsRoot` 114-116; `browserDownloadsRoot` 118-120 (`~/Downloads`); `resolveDownloadFile` 142-157; `executeDiagnosticsReport` ~395-415; `executeBrowserDownloadAction` 467-495 | Reads repo/extension metadata, lists `~/Downloads`, opens/reveals files via `spawn` (39-76) |
| `host/browser-first-host-utils.mjs` | `redactPathForDiagnostics` 30-32; `redactDiagnosticText` 34-42 | Path/secret redaction used by diagnostics |
| `host/browser-profile-service.mjs` (126) | `chromeProfileRoots` 19-40; `findChromiumExtension` 42-62; `seedPinnedExtensions` 68-88; `seedResonantStartupExperience` 90-114 (writes Chrome `Preferences`) | Launch-profile seeding |
| `host/browser-launch-config.mjs` (98) | `ephemeralProfileRoot` 19-25; `resolveBrowserProfile` 43-69; `resolveRemoteDebugging` 77-98 | Pure helpers; default profile is ephemeral under `~/ResonantOS_User/BrowserFirst/Profiles/ephemeral/` |
| `host/provider-host-service.mjs` | 11 | Provider secrets path: `~/ResonantOS_User/Secrets/provider-secrets.json` (detail owned by another agent) |
| `scripts/health-check.mjs` (249) | `parseDefaults` 106-126; `runHealthCheck` 128-190 | **Static**: parses `src/core/defaults.ts` text; does not contact the bridge (no fetch/http in file) |

## 3. Chrome API tally (grep `chrome\.` across `ext/src`, all 106 lib files + entry points) **[inspected, high]**

| API | Count (call sites) | Where / purpose |
|---|---|---|
| `chrome.storage` (`.local.get/set/remove`, `.onChanged`) | 41 generic + 17 `.local` + 1 `.get` | chat store, site permissions, prefs sync, content.js 1073/1245, background 138 |
| `chrome.tabs.query` | 15 | tab selection (`browser-page-actions.js:145,152,159,684,926`; `tab-context-controller.js:38,110,172`; history 371) |
| `chrome.tabs.update` | 6 | navigate/activate tab (`browser-page-actions.js:174,195`; `background.js:217`; `tab-context-controller.js:54`) |
| `chrome.tabs.create` | 3 | open URL (`browser-page-actions.js:177,198`) |
| `chrome.tabs.sendMessage` | 1 | to content script per frame (`browser-page-actions.js:252`) |
| `chrome.tabs.get` / `.reload` | 2 / 1 | controlled tab lookup 140; reload fallback 350 |
| `chrome.tabs.onActivated/onUpdated/onRemoved` | 1 each in background (270-285) + tab-context-controller 94-95 | side panel enable, snapshot invalidation |
| `chrome.scripting.executeScript` | 1 direct + 1 feature check | re-inject content scripts (282-289); **MAIN-world wallet probe** (589-615) |
| `chrome.webNavigation.getAllFrames` | 2 | frame enumeration for subframe actions (246) |
| `chrome.runtime.sendMessage/onMessage/getURL/id` | 3/2/2/1 | content→background snapshots and inline requests; side panel router (`side-panel.js:1218`) |
| `chrome.sidePanel.open/setOptions/setPanelBehavior` | 2/1/1 | background 167,199,215,249 |
| `chrome.history.search` | 1 | `/history` (`app-command-handlers.js:364`) |
| `chrome.windows.getCurrent` | 2 | background 265,348 |
| `chrome.commands.onCommand`, `chrome.action.onClicked` | 1 each | Alt+Shift+A / toolbar click |
| `chrome.debugger`, `chrome.cookies`, `chrome.downloads`, `chrome.storage.session/sync`, `externally_connectable` | **0** | not used / not declared |

Note: `clipboardRead`/`clipboardWrite` are declared in the manifest (line 14) but no `navigator.clipboard`/`chrome.clipboard` call was found in the grep; **[hypothesis, medium]** they are vestigial or used via DOM `execCommand` elsewhere (not found by `execCommand` grep in content.js).

## 4. Mutations possible on a web page (non-agent path) **[inspected, high]**

| Mutation | Code | Guard |
|---|---|---|
| Navigate active/controlled tab to arbitrary http(s) URL; create tab | `browser-page-actions.js:174-178,195-199`; `background.js:217` (`browser_control_handoff` from any content script, URL unvalidated beyond `typeof string`) | **No site-permission check**; `normalizeBrowserUrl` only |
| Click element matched by visible text or `data-resonantos-control-ref` | `content.js:507-559` dispatches pointerdown/mousedown/pointerup/mouseup/click + `element.click()` | `isHardRestrictedElement` 468-496, `isSubmitLikeElement` 448-466 (unconditional human-only); ambiguity refusal 569-576; 650 ms spotlight dwell 501-505 |
| Set value of input/textarea/contenteditable (native setter + `input`/`change` events) | `content.js:~740-749, 821` | `classifyEditableField` must return `safeToType` |
| `form.requestSubmit()` | `content.js:859` | field `safeToSubmit` (search only) AND `formIsSafeToAutoSubmit` (same-origin GET, no commit verbs, no formaction/formmethod override) 754-794 |
| Scroll window (`scrollBy`), `scrollIntoView` | `content.js:882; 523,533,819` | none (read-only mode blocks `scroll_page` at side panel 336) |
| Inline assistant: insert/replace text into the active editable field | `content.js:1256-1287` (`setRangeText`, `range.insertNode`) | only when selection came from an editable field; blocked mode hides UI |
| Inject overlays/styles: control overlay + toast + bubbles; Resonator outline/arrow/spotlight; `<style>` tags | `control-overlay.js:48-115`; `resonator.js:35-69,118-183` | `read-only` still allows `control_overlay` and `resonator` (`browser-page-actions.js:14-20`) |
| Write `data-resonantos-control-ref="rN"` attributes onto page elements | `content-control-refs.js:18-26` | none (side effect of read/click) |
| Write `sessionStorage[STORAGE_KEY]` in page origin (nav/click trail) | `resonant-context.js:439-446, 551-568` | redacted via trace-redaction; disabled if redaction API missing |
| MAIN-world script execution (wallet probe reads `window.phantom/solana/ethereum`) | `browser-page-actions.js:589-615` | blocked-mode check only (582); read-only not consulted (it is a read) |
| Content-script re-injection into a tab that lacks the receiver, else `tabs.reload` | `browser-page-actions.js:282-289, 349-352` | triggered by error-string match 312, 345 |

Not possible from this path: keyboard events (comment 846-848 says synthetic Enter is never dispatched — confirmed, no `KeyboardEvent` in grep), cookie access, downloads, debugger.

## 5. Per-site permission enforcement

Modes and defaults: `ask-before-action` default (`site-permission-store.js:57-58`); UI/slash parse accepts `blocked|block`, `read-only|readonly|read only`, `trusted`, else default (`app-command-handlers.js:90-96`). The store does **not** validate `mode` on write (`site-permission-store.js:66`), so the `<select>` value or any caller string is persisted as-is **[inspected, high]**.

| Mode | Enforced at (file:line) | Effect | Bypassable from UI / elsewhere? |
|---|---|---|---|
| `blocked` | `browser-page-actions.js:301-303` (`readSpecificTabPage`, unless `includeBlocked`), `333-335` (`sendContentAction`), `582-586` (`detectWalletState`); `content.js:1082-1086, 1240-1243, 1478-1483` (inline assistant UI) | refuses read/click/type/scroll/overlay/selection to that host; hides inline button | **Yes**: `/dao` helper scans other tabs with `includeBlocked: true` (`browser-page-actions.js:687`); `openBrowserUrl`/`searchBrowser` navigate regardless (168-218); background `browser_control_handoff` navigates regardless (`background.js:216-218`); the content script's own `read_page` handler has no permission check (`content.js:1442-1451`) — any extension context messaging it directly (e.g. main-workspace, agent runner) gets the snapshot; Resonant Context SDK telemetry snapshots are sent to background on every page regardless of mode (`content.js:115-143`) |
| `read-only` | `browser-page-actions.js:336-338` only (allow-list `control_overlay, detect_forms, get_selection, read_page, resonator` 14-20) | refuses `click_text`, `type_text`, `scroll_page`, `show_inline_assistant_for_text` | **Yes**: content script does not know about read-only (`content.js:1068-1078` only distinguishes `blocked`), so the inline assistant `insert` action (1256-1287) can still mutate an editable field on a read-only site; MAIN-world wallet probe runs (it only checks `blocked`); navigation unaffected |
| `ask-before-action` (default) | **nowhere** on the direct path. Only consumer outside agent control is display (`monitor-progress.js:3-4`, `mode-status-section.js`) and `control-preflight.js:17,24,37` (agent control, other agent's scope) | identical to `trusted-for-safe-actions` for `/browser click|type|scroll` (`side-panel-browser-action-controller.js:87-100` calls actions with no prompt) | n/a — there is no ceremony to bypass |
| `trusted-for-safe-actions` | nowhere on the direct path (same as above); `saveResearchTrailToArchive:938` only lists it as a known mode | same as default | n/a |

Confirmation ceremonies on the non-agent path: none for click/type/scroll/navigate. The only "approval" semantics are the content script's `approvalRequired/humanHandoff` **refusals** (`content.js:511-517, 525-531, 809-816, 825-857`), which hand the action to the human and cannot be overridden by `userApproved` (comment 519-521 and code: `userApproved` is accepted as a parameter but never read in `clickElement`/`typeIntoPage`) **[inspected, high]**. The background `action_request` handler (`background.js:362-374`) returns a flag for six action names but gates nothing; grep found no caller of `action_request` in `ext/src` **[inspected, medium]** (hypothesis: dead/advisory code).

Audit trail: `augmentorSitePermissionAudit` keeps last 20 entries per site with `source` (`human`, `slash-command`, `site-permission-panel`, `settings`) (`site-permission-store.js:37-52`; callers `app-command-handlers.js:318-321`, `side-panel-lifecycle-controller.js:157-160`, `settings/browser-control-section.js:286`).

Fail-closed behaviour (positive): if `chrome.storage.local.get` throws or is missing, `permissionForUrl` throws `site-permissions-unavailable` and the side panel refuses capture (`browser-page-actions.js:296-300, 327-332`); content script treats unreadable storage as `blocked` (`content.js:1072-1076`). Tests cover this (`test/browser-page-actions.test.mjs:904-932`; `test/content-inline-action-gate-enforcement.test.mjs:186-262`).

## 6. Message policy (content script <-> background <-> side panel) **[inspected, high]**

- Channels: content→background uses `type: "resonant-context-snapshot"` (no channel) and `channel: "resonantos.browser_first"` (`content.js:124, 1300-1302`); side panel→content uses `channel: "resonantos.browser_first.content"` via `tabs.sendMessage` (`browser-page-actions.js:305, 340`); side panel listens on `channel: "resonantos.browser_first.side_panel"` for a single type `cancel_control_run` (`side-panel-message-router.js:1-25`, wired `side-panel.js:1218`).
- Background sender check: `sender.id !== chrome.runtime.id` → reject (`background.js:288-291`). This admits **every** extension context including content scripts on any page (content scripts carry the extension id). There is no `sender.url`/origin allow-list and no `externally_connectable`, so web pages cannot message directly; all exposure is via the content script running in the page's isolated world **[inspected, high]**.
- Top-frame check: only `resonant-context-snapshot` requires `frameId === 0` (`background-message-policy.js:180-182`; `background.js:223-225`). `inline_assistant_request`, `open_side_panel`, `browser_control_handoff`, `active_tab_context`, `action_request` are accepted from any frame **[inspected, high]**. `browser_control_handoff` lets any frame's content script open the side panel and navigate the sender tab to an arbitrary `targetUrl` string (`background.js:354-360, 203-220`) — only reachable from extension code, but a compromised/injected content-script path would have it **[hypothesis, low-medium]**.
- Allowed background message types: `resonant-context-snapshot`, `active_tab_context`, `inline_assistant_request`, `open_side_panel`, `browser_control_handoff`, `action_request`; unknown → `{ok:false}` (`background.js:297-377`).
- Payload sanitising: inline body limited to 6 actions / 1200-char prompt / 8000 selection / 5000 pageContext with secret redaction (`background-message-policy.js:184-193, 9-32`); snapshots bounded (sections 8, forms 20, fields 40, text 7000) and sensitive keys redacted (195-237, key pattern 2).
- Content script receiver: ignores `_sender` entirely (`content.js:1434`); filters only by channel and, for visual-only types, top-window (1435-1440). Accepts `click_text`, `type_text`, `scroll_page`, `detect_forms`, `read_page`, `get_selection`, `show_inline_assistant_for_text`, `resonator`, `control_overlay`.
- Side-panel response contract mismatch **[inspected, high]**: background replies to `active_tab_context` with `contextSnapshot` (`background.js:318`) but `hydrateCachedTabSnapshot` reads `response?.snapshot` (`browser-page-actions.js:380`). In production the cached background snapshot can therefore never hydrate the side panel; the unit test passes only because its fake background returns `snapshot` (`test/browser-page-actions.test.mjs:179-187`). Functional bug, not a security issue, but it means the "cached context" feature is untested against the real wire shape.

## 7. User data inventory

### 7a. Extension (`chrome.storage.local`; no `session`/`sync` usage found; no encryption) **[inspected, high]**

| Datum | Key | Format | Mode/encryption | Retention / export / delete |
|---|---|---|---|---|
| Chat sessions, messages, forks, projects, folders, attachments, active id, writer tag | `augmentorBrowserSessions`, `augmentorBrowserMessages`, `augmentorBrowserForks`, `augmentorBrowserProjects`, `augmentorBrowserFolders`, `augmentorBrowserAttachments`, `augmentorActiveBrowserSessionId`, `augmentorChatWriter` (`chat-session-store.js:200-211`) | JSON arrays | plaintext in profile | per-session delete (`deleteSession` 661), archive/restore; no cap/retention found; no export |
| Model / thinking depth / regeneration mode / config / user profile / appearance | `augmentorModel`, `augmentorThinkingDepth`, `augmentorRegenerationMode`, `augmentorConfig`, `augmentorUserProfile`, `augmentorAppearancePreferences` | JSON | plaintext | subset mirrored to bridge via prefs-sync (`prefs-sync.js:30-40`) |
| Site permissions + audit | `augmentorSitePermissions`, `augmentorSitePermissionAudit` | `{host: mode}`, `{host: [20 entries]}` | plaintext | reset per site; audit capped 20/site |
| Task consents + audit (agent control) | `augmentorTaskConsents`, `augmentorTaskConsentAudit` | JSON | plaintext | other agent's scope |
| Browser jobs / active job / control preflight | `augmentorBrowserJobs`, `augmentorActiveBrowserJob`, `augmentorControlPreflight` | JSON | plaintext | other agent's scope |
| Inline draft (selected page text + sanitised URL + title) | `augmentorInlineDraft` (`content.js:1245-1252`) | JSON | plaintext | removed when consumed (`tab-context-controller.js:74`) |
| Pending sidebar prompt, session summary artifact, UI state | `augmentorPendingSidebarPrompt`, `augmentorSessionSummaryArtifact`, `augmentorRailWidth`, `augmentorMainWorkspace`, `augmentorJobMonitorCollapsed`, `augmentorContextDockExpanded`, `augmentorStarterPromptsHidden` | JSON/scalars | plaintext | none |
| Bridge target override | `bridgeTargetOverride` (`background.js:139`) | JSON (url/token) | plaintext | user-editable in Settings |
| Synced prefs mirror / config reload flag | `resonantosSyncedPrefs`, `resonantosConfigReload` | JSON | plaintext | none |
| In-memory only: per-tab context snapshots (max 40) | `resonantContextSnapshots` Map (`background.js:51, 235-239`) | sanitised JSON | SW memory | cleared on URL change/tab close (274-285) |
| Page-origin `sessionStorage` nav/click trail | `resonant-context.js:439-446, 568` | redacted JSON | per-site sessionStorage | cleared by browser session end |

### 7b. Bridge host (`userRoot = $RESONANTOS_BROWSER_FIRST_USER_ROOT || ~/ResonantOS_User`, `run-bridge-minimal.mjs:90-92`) **[inspected, high unless noted]**

| Datum | Path | Format | Mode/encryption | Retention / export / delete |
|---|---|---|---|---|
| Extension prefs document | `~/ResonantOS_User/ExtensionPrefs/extension-prefs.json` (`extension-prefs-host-service.mjs:21-28`) | JSON ≤ 1 MB | `writeFile mode 0o600` (94-98); no encryption; **on Windows the mode is ignored** [hypothesis, high — Node fs semantics] | overwritten whole; no history |
| Memory / Living Archive | `~/ResonantOS_User/Memory/` (`CONFIG/memory-settings.json`, `source-audit.md`, `source-file-versions.json`, …) (`run-bridge-minimal.mjs:94-120`) | JSON/Markdown | not inspected here (memory agent) | archive intake from browser actions lands here via `/archive/intake` |
| BrowserFirst state | `~/ResonantOS_User/BrowserFirst/` incl. `Goals/*.json`, `Delegations/*.md` (`browser-diagnostics-host-service.mjs:46-47`), `downloads-state.json` (`browser-diagnostics-service.mjs:122-139`, 0o600), `Diagnostics/diagnostics-<ts>.json` (409-410, 0o600) | JSON/MD | 0o600 on POSIX only | diagnostics report retained indefinitely; downloads "clear-history" only writes `clearedAt`, deletes nothing (469-476) |
| Browser profiles | `~/ResonantOS_User/BrowserFirst/Profiles/main` (persistent, opt-in) and `.../Profiles/ephemeral/session-*` (`browser-launch-config.mjs:19-25, 43-69`; `run-bridge-minimal.mjs:382`) | Chromium profile | Chromium's own | ephemeral dirs: no cleanup code found in these files [inspected, medium] |
| Provider secrets | `~/ResonantOS_User/Secrets/provider-secrets.json` (`provider-host-service.mjs:11`) | JSON | not inspected (secrets agent) | — |
| Generated extension bridge config | `<extensionRoot>/src/bridge-config.generated.js` (`bridge-server.mjs:1177`) | JS: `globalThis.__RESONANTOS_BRIDGE_CONFIG__ = Object.freeze({bridgeUrl, httpsBridgeUrl, bridgeToken, capabilityBootstrapToken})` (1183-1195) | `mode 0o600` (1196); **contains the bridge token and the capability bootstrap token in plaintext inside the extension source tree**; gitignored per comment (`background.js:1-6`) | rewritten each bridge start |

No encryption-at-rest primitive was found anywhere in `host/` other than TLS key material handling (`bridge-tls.mjs`) and the `dsh-runtime.mjs` 0o700/0o600 ownership checks (POSIX-only `getuid`). No `export`, `purge`, or `retention` feature for user chats/permissions exists in `ext/src` beyond `/diagnostics/report` and per-item deletes **[inspected, high]**.

## 8. Diagnostics and redaction **[inspected, high]**

- Routes (`browser-diagnostics-host-service.mjs:82-119`): all GETs need capability `bridge-diagnostics-read`; `/browser/downloads/action` needs `browser-download-action`; `/diagnostics/report` needs `diagnostics-report-export`.
- `/status` reports provider presence as booleans only (`Boolean(secrets[...])`, 50-54) — no secret values.
- `/workspace/inspect` reads `package.json`, extension `manifest.json`, lockfile presence (`browser-diagnostics-service.mjs:169-178, 294-315`); self-described as "Read-only metadata inspection" (332) — that string is **[reported]**; the code paths read are consistent with it.
- `/browser/downloads` lists `~/Downloads` filenames (118-120, 437-460); `/browser/downloads/action` `open|reveal` spawns the OS opener on a file confined to `~/Downloads` by `path.relative` check (142-157) and `clear-history` only stamps state (469-476).
- `/diagnostics/report` serialises a report, runs `redactDiagnosticText` over the whole JSON (407), writes to `BrowserFirst/Diagnostics/` (409-410).
- Redaction (`browser-first-host-utils.mjs:30-42`): home-dir → `~` (string replace of `os.homedir()`), `sk-…` keys, `Bearer …`, `api_key=`, `token=`, `secret=` assignments. **Narrow**: does not cover JWTs, `AKIA`, `gh*_`, PEM, card numbers that the extension-side redactors do (`background-message-policy.js:3-7`; `trace-redaction-core.js:18-42`). Also `redactPathForDiagnostics` replaces only the exact `os.homedir()` string; paths under a different user root (`RESONANTOS_BROWSER_FIRST_USER_ROOT`) or Windows 8.3 variants pass through [hypothesis, medium].
- `scripts/health-check.mjs`: purely static — reads `src/core/defaults.ts` text (`DEFAULTS_PATH` 20, `parseDefaults` 106-126), extracts provider URLs and known model ids, redacts secret-looking values in its own output (44-65, 157-187). It never contacts the bridge or any network (no `fetch`/`http` in file). Its test spawns the script as a subprocess (`scripts/health-check.test.mjs:217-293`) — a real process run but still offline.
- `browser-launch-config.mjs` is pure (comment 10-12 **[reported]**, code confirms: no `spawn`/`fs`); the "cdp-proof predicate" is asserted statically in `test/browser-launch-config.test.mjs:131`.
- `browser-profile-service.mjs` writes to the Chrome profile `Preferences` file (`seedPinnedExtensions` 87, `seedResonantStartupExperience` 113) with default mode, no 0o600.

## 9. Freshness **[inspected, high]**

- Content script: `MutationObserver` on `document.body` (`content.js:135-143`) only debounces a *context snapshot send* to background (≥500 ms, ~1.5 s cadence 115-128). No DOM hashing, no snapshot id echoed back on actions, no "page changed since read" check. Click targets are re-resolved by visible text or by `data-resonantos-control-ref` at action time (`content.js:561-594`); refs are attributes on live elements so a re-rendered element loses its ref and the action fails with "No clickable element matched ref" (588) — a weak, incidental freshness guard **[hypothesis, medium]**.
- Side panel: `sameContextTab` compares only `tabId` or exact URL (`browser-page-actions.js:356-362`); `lastSnapshot` is reused by `summarizeSnapshot`, `saveCurrentPageToArchive`, `saveWalletDaoAuditToArchive`, `summarizeCurrentPageToArchive` without re-reading (640, 732, 840, 1016), so archive intake can capture a stale snapshot after SPA navigation that keeps the URL **[hypothesis, medium]**. Background clears its cache on `changeInfo.url` only (`background.js:274-277`).
- Agent-control `control-page-observer.js` exists but is out of scope here (other agent).

## 10. Tests (all `browser-first/test/` unless noted; runner `node:test`, no shared fake-chrome helper found — each file builds its own `chrome` object) **[inspected, high]**

| File | Kind | Asserts (one line) | Skipped / mocked? |
|---|---|---|---|
| `browser-page-actions.test.mjs` (46 tests) | unit, hand-rolled fake `chrome` (12-50) + JSDOM for two tests loading the REAL `content.js` (819, 888) | read-only blocks `type_text` (305-313) but allows overlay (315-329); blocked site refused (915); unreadable permissions fail closed (904-932); research-trail counts; URL secret stripping (243) | no `.skip`; bridge is a stub; `permissionForUrl` is a stub returning the override string (67) — the real store is not exercised; cached-snapshot test (177-195) uses a fake background shape that differs from real (`snapshot` vs `contextSnapshot`) → tautological |
| `site-permission-store.test.mjs` (9) | unit, in-memory storage stub | default mode, persistence, reset, fail-closed read (105), never-write-after-failed-read (120) | mocked storage; no test that invalid mode strings are rejected (they are not) |
| `side-panel-command-router.test.mjs` (17) | unit, handler spies | slash dispatch incl. `/site`, `/history`, Resonator; wallet-term gate (297) | pure dispatch; asserts only that handler names are called |
| `resonator.test.mjs` (2) | JSDOM, loads real `resonator.js` | exposes commands; idempotent; `clear` restores | no chrome needed |
| `tab-context-controller.test.mjs` (14) | unit, fake chrome (storage/tabs 23-48) | mention parse, bind + activate tab, inline draft consumption + storage remove, listener wiring | mocked |
| `app-command-handlers.test.mjs` (22) | unit, fake chrome incl. `history.search` and `tabs.query` with an `incognito: true` tab (86) | `/history` excludes incognito (363, 378); `/site` modes parse (125); status/memory/capabilities messages (334) | mocked; incognito exclusion asserted only for the `/history ... tabs` listing |
| `chat-session-store.test.mjs` (23) | unit, in-memory storage | hydrate/validate, create/switch/rename/delete/pin/fork/trim | mocked |
| `background-message-policy.test.mjs` (6) | pure unit | inline body sanitising, defaults to summarize, snapshot bounding, top-frame check (56), nested secret redaction | none |
| `content-inline-action-gate-enforcement.test.mjs` (12) | JSDOM + `window.eval` of real content libs and `content.js` (20, 72), fake `chrome.storage` (34-46) | restricted schemes denied; blocked/unreadable storage hides button and refuses `send` without writing draft (186-262) | storage faked; `tabs.sendMessage` not involved |
| `content-inline-action-surface-gate.test.mjs` (5) | pure unit (imports classic script) | scheme list parity with `control-target-classification`; denies chrome://, empty | none |
| `content-redaction.test.mjs` (31) | JSDOM + `vm.runInNewContext` of real content scripts | field-safety classes (243); snapshot redaction of values/URL secrets (291, 323); subframe behaviour (406, 427); ambiguous click refusal (462) | the word "live" appears only in fake secret strings (9-11); fully offline |
| `content-scripts-parse-as-classic.test.mjs` (2) | `vm.Script` parse | manifest content scripts parse as classic (no ESM) | none |
| `browser-diagnostics-host-service.test.mjs` (7) | unit, tmpdir, stubbed deps; `launchDiagnosticDownload` with injected `spawnImpl` | OS opener pinning per platform (46-105); routes/capabilities (145); status has no secrets (159); workspace inspect metadata only (174) | spawn mocked |
| `browser-profile-service.test.mjs` (4) | unit, tmpdir real fs | seeds startup URLs, leaves newtab alone; pins unique ids; override discovery + cache clear; platform roots | writes real temp files |
| `browser-launch-config.test.mjs` (10) | pure unit | ephemeral default, persistent only by opt-in, debug port forced to 0+loopback, "cdp-proof predicate" (131) | static argv assertions only (no launch) |
| `extension-prefs-host-service.test.mjs` (1) | unit, tmpdir | **only** asserts routes exist and capability names (9-26) | never writes/reads a prefs doc; 0o600 and 1 MB cap untested |
| `resonant-context-storage.test.mjs` (8) | JSDOM, loads real SDK | sessionStorage payload redacted; disabled persistence writes nothing; reload retention | offline |
| `context-plugins.test.mjs` (4) | JSDOM | domain selection without suffix spoofing; URL sanitiser strips query/hash | offline |
| `trace-redaction.test.mjs` (19), `trace-redaction-packaging.test.mjs` (5) | unit / vm | redaction patterns; frozen versioned global; ESM adapter parity | `spawnSync` used in packaging test for a classic-load check |
| `prefs-sync-storage.test.mjs` (9), `prefs-sync-events.test.mjs` (2) | JSDOM + fake storage/bridge | failed pull/push ordering; only synced keys pushed; no saved bridge credentials in body (147) | bridge mocked |
| `settings-diagnostics-recovery.test.mjs` (4) | JSDOM | timeouts/retry; diagnostics export body excludes override credentials (85) | mocked |
| `scripts/health-check.test.mjs` (~30) | unit + `spawnSync` of the script | redaction helpers; `--json` shape; exit codes | runs the script as a subprocess against repo `defaults.ts` (offline) |

Not found: any test of `background.js`'s `onMessage` router itself (sender check, `browser_control_handoff`, `action_request`) — only the pure policy helpers are tested. Not found: a test that `openBrowserUrl`/`searchBrowser` respect `blocked`. Not found: a test of `prepareDaoWorkflowGuidance`'s `includeBlocked: true` behaviour (test 456 asserts "without wallet automation" only). No `.skip`/`todo` markers in the surveyed files (grep hits for "skip" were data fields).

## 11. Downgrades (claims that should be weakened)

1. **"Per-site permission modes" → effectively two modes.** `ask-before-action` and `trusted-for-safe-actions` have no enforcement on the direct `/browser` path; no prompt exists (`side-panel-browser-action-controller.js:87-100`; `browser-page-actions.js:322-338`). The names imply a consent ceremony that is not implemented outside agent control. [high]
2. **"Blocked" is not blocking navigation or DAO scans.** `openBrowserUrl`/`searchBrowser` (`browser-page-actions.js:168-218`), background `browser_control_handoff` (`background.js:216-218`), and `/dao` cross-tab read with `includeBlocked: true` (687) ignore it. The research-trail path does honour it (953-960). [high]
3. **Enforcement is in the extension *page* (side panel), not in the background or content script.** The content script's `read_page/click_text/type_text` handlers check nothing site-related (`content.js:1442-1544`); any extension context that calls `tabs.sendMessage` directly (main-workspace, agent runner, future code) bypasses the gate. [high]
4. **`read-only` does not reach the inline assistant's `insert`.** Content script only knows `blocked` (`content.js:1068-1078`), so text insertion into an editable field is possible on a read-only site via the in-page UI (1256-1287). [high]
5. **Cached-context hydration is broken against the real wire shape** (`contextSnapshot` vs `snapshot`, `background.js:318` vs `browser-page-actions.js:380`); the passing unit test fakes the shape (`test:179-187`). [high]
6. **Incognito "excluded" is a `/history` listing detail only** (`app-command-handlers.js:372`); page reads/actions/snapshots do not check `tab.incognito`, and the manifest sets no `incognito` mode. [high]
7. **0o600 claims are POSIX-only**; on Windows (this reviewer's platform and a supported target per `browser-profile-service.mjs:27-33`) `mode` is ignored, so prefs, diagnostics, downloads state and the generated bridge config (`bridge-server.mjs:1196`) rely on NTFS user-profile ACLs only. [high]
8. **Generated bridge config puts `bridgeToken` and `capabilityBootstrapToken` in a JS file inside the extension source dir** (`bridge-server.mjs:1183-1195`), readable by any process with the user's rights and shipped if the gitignore is lost; the comment "Raw route capability tokens are never written" (1180-1182) is true but the bootstrap token that mints them is. [high; detail owned by secrets agent]
9. **Diagnostics redaction is narrower than the extension's own redactors** (`browser-first-host-utils.mjs:34-42` vs `background-message-policy.js:3-7`); JWT/AWS/GitHub/PEM patterns absent. [medium]
10. **`extension-prefs-host-service.test.mjs` is a smoke test** (routes exist). The 1 MB cap, debounce coalescing, and file write are untested. [high]
11. **`sendContentAction` string-matches error text to decide to inject or reload a tab** (`browser-page-actions.js:312, 344-352`); a `tabs.reload` of the user's tab is a side effect triggered by an error message regex. [medium]
12. **`health-check.mjs` is a config lint, not a health check** — it never contacts the bridge (`scripts/health-check.mjs:10-20,106-190`). [high]
13. **Safety boundaries are regex heuristics** on labels/attributes (`content.js:444-447, 495`; `content-field-safety.js:75-98`). A control labelled "Continue" that performs a purchase, or an unlabeled icon button, passes `isSubmitLikeElement` unless it is `type=submit`/inside a form. [medium]
14. **`site-permission-store.setSitePermission` does not validate `mode`** (66); a corrupted or hand-edited value (e.g. `"trusted "`) silently acts as the default on the side panel (any unknown string ≠ `blocked`/`read-only` is allowed through 333-338). [high]

## 12. Coupling

- `browser-page-actions.js` depends on `chat-turn-controller.js` (sanitisers), `research-trail.js`, `readable-tab-ranking.js`, `browser-command-parser.js`, `wallet-dao-audit-markdown.js`, `wallet-state.js`, `summary-templates.js` (1-12) and on bridge routes `/web/news`, `/augmentor/chat`, `/archive/intake`, `/archive/review/request`.
- The content-script file order is duplicated in two places and must stay in sync: `manifest.json:27` and `CONTENT_SCRIPT_FILES` (`browser-page-actions.js:270-280`); note the manifest list includes `augmentor-shortcut-controller.js` and `content-inline-action-surface-gate.js` which the re-injection list omits → re-injected tabs lack the inline surface gate (`content.js:25, 1232-1234` then refuses with "surface gate did not load") **[inspected, high]**.
- Site-permission gate is instantiated separately in `side-panel.js:368-369` and `main-workspace.js:293-309` (the latter passes `renderSitePermissionPanel: async () => undefined`); both call the same `createBrowserPageActions`.
- Background ↔ side panel coupling on `active_tab_context` shape is broken (see §6).
- Host diagnostics depend on `readProviderSecrets` (presence booleans) and memory/addon status services (`browser-diagnostics-host-service.mjs:11-14, 43-61`).
- `prefs-sync.js` couples `chrome.storage.local` keys to `/settings/extension-prefs` (capabilities `extension-prefs-read/write`).

## 13. Open questions

1. Who, if anyone, sends `action_request` to the background (`background.js:362-374`)? No caller found in `ext/src`; if none, this is dead advisory code that docs may still cite as a gate.
2. Is `clipboardRead/clipboardWrite` used anywhere (no API call found)? If not, the permission is over-declared.
3. Does the agent-control runner call `tabs.sendMessage` directly or always via `sendContentAction`? (Determines whether downgrade 3 is theoretical or exploited in-tree — other agent.)
4. Is there any cleanup of `BrowserFirst/Profiles/ephemeral/session-*` directories, and of `BrowserFirst/Diagnostics/*.json`? None found in the files read.
5. Do docs/ADR-036/037 (referenced in comments `content-field-safety.js:1`, `background.js:179, 210`) promise an "ask before action" ceremony for direct browser commands? If so, that is a doc-vs-code gap to record.
6. On Windows, what protects `bridge-config.generated.js` and `extension-prefs.json` beyond default profile ACLs? (0o600 is a no-op.)
7. Why does `hydrateCachedTabSnapshot` read `response.snapshot` while background returns `contextSnapshot`? Regression or never worked? `git log` for these two files would settle it (not run in this time box).
