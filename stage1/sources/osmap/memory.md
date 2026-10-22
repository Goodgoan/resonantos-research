# OS Map - Memory / Living Archive

- Repo: ResonantOS 2.0.0 Alpha, clone `research/_untrusted/resonantos-2.0.0-alpha`, commit 578fbbc3c1c854b192318b3d2163b138fb45d8bd (branch dev)
- Verified: 2026-10-20, static reading only (file reads, grep, git log/show/blame). No code executed.
- Legend: [inspected] = read in code; [reported] = what docs/comments say; [hypothesis] = my inference. Confidence high/medium/low per claim.
- All paths below are relative to the clone root unless stated.

## Summary

The Alpha Living Archive is a Node host-side set of ~20 ESM modules under `browser-first/host/` that are wired into the bridge in `run-bridge-minimal.mjs:246-374` and exposed as 34 HTTP routes (`memory-host-service.mjs:10-215`). State is plain files under `~/ResonantOS_User/Memory` (markdown with pseudo-YAML frontmatter for content artifacts; JSON for manifests/history; JSONL for move ledgers). There is no database, no embeddings, no encryption.

What works (high confidence, covered by tests): source registration/scan, selected-file intake into `INTAKE/sources` with content-hash versioning (`CONFIG/source-file-versions.json` + content-addressed snapshots), audited move-on-import with JSONL ledger and rollback, manifest repair, keyword search over `AI_MEMORY`, wiki health/lint, browser intake into `INTAKE/browser`, review-request creation.

What is broken or hollow in the live service (high confidence from reading, no test exercises these paths): the review pipeline *draft -> verify -> revise -> promote* in `archive-review-service.mjs` was written against interfaces that do not match the modules it imports. Draft generation dereferences `.crossLinks` on a string and will throw a TypeError (`archive-review-service.mjs:316-322,363`); promotion passes a `{draft, verifier}` shape to a policy that destructures flat fields, so the first check always fails (`archive-review-service.mjs:669-684` vs `archive-promotion-policy.mjs:11-25`); the human-approval gate on review transitions is passed `toStatus` while the policy reads `nextStatus`, so the gate never fires (`archive-review-service.mjs:276-277` vs `archive-review-policy.mjs:27-31`). Consequently, through the Alpha bridge: no trusted wiki page can be promoted at all (fail-closed), and escalated review requests can be approved by any actor (fail-open). All unit tests of the policy modules pass because they call the policies directly with the correct argument names; the only end-to-end test (`living-archive-continuity-acceptance.test.mjs`) stops after `executeArchiveReviewRequest`.

The ADR-013 Human/External/AI domain separation exists on disk only as empty directories plus the move-on-import destination; the default copy-on-import path never writes to `HUMAN_KNOWLEDGE/` or `EXTERNAL_KNOWLEDGE/` and records ownership only as frontmatter metadata. The MCP server in `examples/` is a real stdio JSON-RPC server with 14 tools, but it is a standalone example, not wired into the bridge, and ADR-029 marks it "Alpha applicability: Deferred".

## Files/functions with line ranges

### Launcher wiring [inspected, high]
- `browser-first/host/run-bridge-minimal.mjs:90-119`: `userRoot()` = `RESONANTOS_BROWSER_FIRST_USER_ROOT` or `~/ResonantOS_User`; `memoryRoot()` = `<userRoot>/Memory`; settings `Memory/CONFIG/memory-settings.json`; audit `Memory/CONFIG/source-audit.md`; manifest `Memory/CONFIG/source-file-versions.json`; history paths from `memory-source-history.mjs`.
- `run-bridge-minimal.mjs:246-262` creates `memorySourceSettingsService`; `:283-290` `archiveReviewService` (receives `runArchiveIngestWriter`, `runArchiveSemanticVerifier` from `providerHostService`, `:165-178`); `:317-331` `memorySourceIntakeService` (receives `executeArchiveReviewRequest` so sync can auto-create review requests); `:339-374` `createMemoryHostService` collects all 34 executors; `:419` spreads `memoryBridgeRoutes` into bridge routes.

### Route table [inspected, high] - `browser-first/host/memory-host-service.mjs:10-215`
| Route | Capability |
|---|---|
| GET /memory/status, GET /memory/settings, GET /memory/wiki/health | memory-read |
| POST /memory/settings | memory-settings-write |
| POST /memory/source/browse | memory-source-browse |
| POST /memory/source/scan | memory-source-scan |
| POST /memory/source/action, POST /memory/source/versions/repair | memory-source-manage |
| POST /memory/source/move-preflight, move-execute, move-rollback | memory-source-move |
| POST /memory/source/review, /memory/wiki/lint, /memory/source/versions, /memory/source/diff | memory-source-review |
| POST /memory/source/intake | memory-source-intake |
| POST /memory/source/file-intake, /memory/source/sync | memory-source-file-intake |
| POST /memory/search, /memory/wiki/page/read, /archive/intake/list, /archive/intake/read, /archive/review/list, /archive/review/artifact/read, /archive/review/verification/read, /archive/review/promotions/list | archive-read |
| POST /archive/intake, /archive/review/request, /archive/review/transition, /archive/review/draft, /archive/review/artifact/verify, /archive/review/artifact/revise, /archive/review/artifact/promote, /archive/review/promotions/restore | archive-write |

Note: promotion (trusted wiki write) and restore share the same `archive-write` capability as browser intake; there is no separate "archive-promote" capability (`memory-host-service.mjs:131-136,197-202,209-214`). Capability map duplicated client-side in `browser-first/resonantos-side-panel-extension/src/lib/bridge-client.js:46-79` (same values).

### Host modules
- `memory-schema.mjs:7-22` `memoryDomainRoots` (14 dirs); `:97-126` `ensureLivingArchiveSchema` mkdirs all and writes `AI_MEMORY/wiki/{AGENTS.md,index.md,log.md}` if missing (mode 0o600). Called from `executeMemoryStatus` (`memory-source-settings-service.mjs:114`) so the tree is created on first status read.
- `memory-source-settings-service.mjs:27-33` defaults (`activeMemoryAddon: "living-archive"`, `syncMode: "manual-review"`, `autoSync: false`); `:143-154` `readMemorySettings` (bare `JSON.parse`, throws on corrupt settings); `:156-187` `normalizeMemorySource` (kind folder|obsidian-vault; ownership human-knowledge|external-knowledge|mixed-library, default mixed-library; importMode copy-on-import|move-on-import|linked-readonly, default copy); `:201-216` markdown audit appender; `:276-301` settings save (move-on-import blocked by `memory-settings-policy.mjs:1-5` at `:288`); `:339-469` move preflight/execute/rollback wrappers (ledger containment via `isInsidePath` at `:425-428`); `:471-529` native folder picker (osascript / PowerShell FolderBrowserDialog / zenity|kdialog); `:531-550` file classifier by extension; `:552-597` scan.
- `memory-source-intake-host-service.mjs:69-150` `sourceReviewSnapshot` (hash-compares text files against manifest; caps candidates at 25); `:165-250` `executeMemorySourceIntake` writes a source-review summary into `INTAKE/sources/`; `:252-415` `executeMemorySourceFileIntake` (per file: containment -> classify -> hash -> `reserveSourceFileVersion` -> write intake md -> `writeSourceFileSnapshot` -> `recordSourceFileIntakeArtifact`; on failure `rm` intake + `rollbackSourceFileVersionReservation` `:378-387`; batch cap 200 `:30`); `:417-530` `executeMemorySourceSync` (auto-intake only when `autoSync && syncMode === "auto-intake-review"` `:425`; creates review requests per created artifact `:506-512`); `:532-538` search; `:540-555` health/lint; `:565-644` manifest repair (confirmation phrase `REPAIR SOURCE VERSIONS` `:569-571`); `:646-715` diff vs last snapshot.
- `memory-source-versioning.mjs:36-39` snapshot path `CONFIG/source-file-history/blobs/<2 hex>/<sha256>.txt`; `:41-79` snapshot write (hash re-verified `:49-52`, existing blob re-hashed `:55-59`, temp+rename `:68-71`); `:85-95` `readManifest` (bare `JSON.parse`); `:97-105` `writeManifest` temp+rename; `:132-191` reserve; `:193-241` rollback reservation; `:243-293` record artifact (path containment `:257-260`); `:295-319` naive positional line diff.
- `memory-source-history.mjs:24-34` history file paths (`CONFIG/source-sync-history.json`, `source-version-repairs.json`, `source-move-history.json`); `:62-69` reader (bare `JSON.parse`); `:71-76` writer caps 50 entries; `:36-60` path redaction to `~/<basename>` or `[path]/<basename>`.
- `memory-source-move.mjs:89-93` `memoryDomainForOwnership`; `:95-97` confirmation phrase `MOVE <sourceName>`; `:99-134` `assertSafeMoveSource` (rejects fs root, home, inside Memory, macOS protected roots, ~/Library); `:197-214` preflight fingerprint over content hashes; `:234-248` move = `rename`, fallback copy+verify+rm; `:367-424` preflight; `:426-631` execute (manifest.json + move-ledger.jsonl under `CONFIG/move-imports/<moveId>/`; `:470-493`; per-file hash verify `:549-550`; automatic rollback on any failure `:576-580`); `:633-719` `rollbackMoveImport` (phrase `ROLLBACK MOVE` `:642`; tolerates corrupt manifest if ledger has boundary record `:647-661`; refuses mismatched hashes `:319-340`).
- `memory-source-paths.mjs:11-36` relative-path normalization/containment; `:51-65` lstat (rejects symlink) + realpath containment.
- `memory-search.mjs:114-158` `searchMemoryWiki` (see Search).
- `memory-wiki-health.mjs:133-271` `computeWikiHealth`; `memory-wiki-lint.mjs:53-77` writes `REVIEW/lint/wiki-lint-<ts>.md` and appends `log.md`.
- `archive-review-host-service.mjs:4-19` `safeMemoryRelativePathForRoot` (prefix + resolve containment, no realpath/symlink check); `:21-29` `frontmatterValue` = regex `^key:\s*(.+)$` over the whole file (not limited to the frontmatter block); `:31-44` `writeFrontmatterValue`; `:93-120` factory.
- `archive-review-service.mjs:50-86` `executeArchiveIntake` -> `INTAKE/browser/<ts>-<slug>.md` + `INTAKE/browser/log.md`; `:88-120` list; `:122-137` intake read (24 KB cap); `:139-155` wiki page read; `:157-203` review request -> `REVIEW/requests/`; `:205-253` review list (joins draft state); `:255-291` transition; `:293-382` draft; `:384-407` artifact read; `:409-513` verify -> `REVIEW/verifications/`; `:515-631` revise; `:633-651` verification read; `:653-767` promote; `:769-805` promotions list; `:807-861` restore.
- `archive-promotion-policy.mjs:11-33`, `archive-review-policy.mjs:9-35`, `archive-promotion-guards.mjs:1-11`, `archive-promotion-paths.mjs:32-42` (`AI_MEMORY/backups/{promotions|restores}/<ts>/<slug>-<hash12>.md`), `archive-merge.mjs:45-96` (H2 section merge with idempotence marker), `:140-176` index upsert.
- `memory-ingest-draft.mjs:75-131` `buildDeterministicWikiDraft` returns a **string** (array `.join("\n")` at `:97-131`).
- `memory-ingest-writer.mjs:38-48` `validateWikiDraftContent` (>=300 chars and 7 required H2 sections); `:86-177` `runArchiveIngestWriterWithRoute` returns `{content, writerStatus, providerId, model, usage, fallbackReason}`.
- `provider-bridge-service.mjs:1034-1049` `providerRouteForArchiveVerifier`; `:1065-1157` `runArchiveSemanticVerifier`; `:1159-1183` `runArchiveIngestWriter`.

## On-disk layout and domain separation

Root: `~/ResonantOS_User/Memory` (override `RESONANTOS_BROWSER_FIRST_USER_ROOT`) [inspected, high: `run-bridge-minimal.mjs:90-96`].

Directories created by `ensureLivingArchiveSchema` [inspected, high: `memory-schema.mjs:7-22`]: `HUMAN_KNOWLEDGE/`, `EXTERNAL_KNOWLEDGE/`, `AI_MEMORY/wiki/`, `AI_MEMORY/provenance/`, `AI_MEMORY/backups/`, `INTAKE/browser/`, `INTAKE/mcp/`, `INTAKE/review-queue/`, `REVIEW/requests/`, `REVIEW/artifacts/`, `REVIEW/verifications/`, `CONFIG/`, `LOGS/`, `MANIFESTS/`.

Who writes where [inspected, high]:
| Path | Writer | Format |
|---|---|---|
| `INTAKE/browser/*.md`, `INTAKE/browser/log.md` | `executeArchiveIntake` (`archive-review-service.mjs:56-80`) | markdown + frontmatter (`source, actor, title, createdAt, url, sourceMessageId`) |
| `INTAKE/sources/*-source-review.md` | `executeMemorySourceIntake` (`intake-host-service.mjs:177-233`) | markdown |
| `INTAKE/sources/<slug>/*.md` | `executeMemorySourceFileIntake` (`:287-377`) | markdown; frontmatter carries `sourceId, sourcePath, sourceFile, ownership, importMode, sourceModifiedAt, sourceContentHash, sourceVersion, previousSourceContentHash` + full file content under `## Content` |
| `INTAKE/imports/mixed/<slug>-<hash>/` or `HUMAN_KNOWLEDGE/sources/...` or `EXTERNAL_KNOWLEDGE/sources/...` | move-on-import only (`memory-source-move.mjs:89-93,378-382`) | original files relocated |
| `REVIEW/requests/*.md` | `executeArchiveReviewRequest` (`:163-189`) | markdown, `type: "archive-review-request"`, `status` |
| `REVIEW/artifacts/*-draft.md`, `*-revised-draft.md` | draft/revise (`:312-369, 609-615`) | markdown, `type: "archive-draft-wiki-update"` |
| `REVIEW/verifications/*-verification.md` | verify (`:468-505`) | markdown |
| `REVIEW/lint/wiki-lint-*.md` | `runWikiLint` (`memory-wiki-lint.mjs:60-64`) | markdown |
| `AI_MEMORY/wiki/*.md`, `index.md`, `log.md`, `AGENTS.md` | promote/restore/lint/schema | markdown |
| `AI_MEMORY/backups/promotions|restores/<ts>/*.md` | promote/restore (`:708-721, 834-842`) | page copies |
| `CONFIG/memory-settings.json` | settings service | JSON |
| `CONFIG/source-file-versions.json` | versioning | JSON manifest |
| `CONFIG/source-file-history/blobs/xx/<sha256>.txt`, `.../repairs/*.json` | versioning / repair | content blobs, manifest backups |
| `CONFIG/source-audit.md` | `appendMemorySourceAudit` | markdown log |
| `CONFIG/source-sync-history.json`, `source-version-repairs.json`, `source-move-history.json` | history | JSON, capped 50 |
| `CONFIG/move-imports/<moveId>/manifest.json`, `move-ledger.jsonl`, `rollback-report.json` | move | JSON / JSONL |

Dirs created but never written by any host module (grep of `browser-first/host/*.mjs`): `LOGS/`, `MANIFESTS/`, `AI_MEMORY/provenance/` (the MCP example writes `AI_MEMORY/provenance/review-artifacts/*.json`, see MCP section), `INTAKE/mcp/`, `INTAKE/review-queue/` (MCP example only) [inspected, high].

Domain separation vs ADR-013 [reported vs inspected]:
- ADR-013 (`docs/architecture/ADR-013-living-archive-memory-domains.md:15-27, 112-160`) says three first-class domains, copy-on-import default makes "the managed copy the canonical source", target tree with `HUMAN_KNOWLEDGE/{sources,versions,metadata}`, `INDEX/archive.db`, `LOGS/*.jsonl`, `CONFIG/permissions.json`. It flags "Alpha applicability: Applies" (`:7`).
- Code [inspected, high]: `ownership` is a per-source setting (`memory-source-settings-service.mjs:162-164`) copied into intake frontmatter (`intake-host-service.mjs:325`). Only move-on-import maps ownership to a domain directory (`memory-source-move.mjs:89-93`). Copy-on-import (the default) copies nothing into `HUMAN_KNOWLEDGE`/`EXTERNAL_KNOWLEDGE`; the "copy" is the intake artifact under `INTAKE/sources` plus the content-addressed blob under `CONFIG/source-file-history`. `linked-readonly` is accepted as a value but no code branches on it (grep `linked-readonly` -> only the allow-list at `:165`). No `INDEX/`, no `archive.db`, no `permissions.json`, no per-domain `versions/`.
- Verdict [hypothesis, high]: domain separation is metadata plus empty folders for the default path; the ADR tree is aspirational for Alpha.

File permissions: intake-from-source, settings, manifests, history, snapshots, move ledgers use mode `0o600`; everything written by `archive-review-service.mjs` (browser intake, review requests, drafts, verifications, promoted wiki pages, index) uses default mode (`archive-review-service.mjs:80,189,285,369,505,615,734,756`) [inspected, high]. Encryption: none (grep `encrypt|cipher` across memory-*/archive-* -> no hits) [inspected, high].

## Provenance and versioning

- Provenance for browser intake: frontmatter `source/actor/title/createdAt/url/sourceMessageId` (`archive-review-service.mjs:61-68`). For source-file intake: `sourceId`, `sourceFile`, `sourceModifiedAt`, `sourceContentHash`, `sourceVersion`, `previousSourceContentHash` (`intake-host-service.mjs:319-333`). Review request records `artifactPath`; draft records `requestPath`, `artifactPath`, `proposedPage`, `providerId`, `model`; verification records `semanticProviderId/Model`; promoted page records `reviewArtifact`, `sourceArtifact` (`:725-731`) and the merge marker `<!-- resonantos-browser-first-promote:<slug> -->` (`archive-merge.mjs:46`). All provenance is pseudo-YAML frontmatter read by regex over the whole file (`archive-review-host-service.mjs:21-29`); a body line like `status: promoted` would shadow the frontmatter if it appears first - actually the regex has flag `m` and `exec` returns the first match, so the frontmatter wins when present, but a key missing from frontmatter can be satisfied by body text [inspected, medium].
- Versioning (`source-file-versions.json`): one entry per `sourceId::relativeFile`, `latestHash/latestVersion/latestIntakePath/latestSnapshotPath`, `history[]` capped at 100 (`versioning.mjs:159-182`). Two-phase: reserve (bump version) -> write artifact -> record; rollback restores previous entry only if the reservation is still latest and unfinalized (`:193-241`). Snapshot blobs are content-addressed and re-verified on reuse (`:55-59`). Writes are temp+rename (`:68-71, 100-103`) - atomic on POSIX; on Windows `rename` over an existing file is also replace semantics in Node, but no fsync anywhere [inspected, high; crash-safety hypothesis medium].
- No versioning of `AI_MEMORY/wiki` pages beyond promotion backups (one copy per promotion/restore). `log.md` is append-only chronology; `index.md` is rewritten whole on each promotion (`archive-review-service.mjs:748-756`).
- Git-style history promised by ADR-013 (`:29`) does not exist; the "append-only version ledger" alternative is partly realized by the JSON manifest + blobs [inspected, high].

## Recovery/restore

Present [inspected, high]:
1. Promotion restore: `executeArchivePromotionRestore` (`archive-review-service.mjs:807-861`) copies `backupPath` back over the page after guards (`archive-promotion-guards.mjs:1-11`: must be `promoted`, not already `restored`, must have a backup) and containment (`backupPath` must be under `AI_MEMORY/backups/promotions`, `:827-828`); the current page is first copied to `AI_MEMORY/backups/restores/` (`:834-842`). Only one restore per promotion (`rollbackStatus === "restored"` blocks). A page whose first promotion created it (no prior content) has no backup and cannot be restored/removed via this route (`:708-721` sets `backupPath` only if the page existed).
2. Move rollback: ledger-driven, hash-verified per file, tolerant of a corrupt `manifest.json` when the ledger carries a boundary record (`memory-source-move.mjs:633-719`), refuses symlinked ledgers (`:638-641`), reports partial results and keeps the source registered on partial rollback (`settings-service.mjs:437-439`).
3. Manifest repair: `executeMemorySourceVersionsRepair` (`intake-host-service.mjs:565-644`) backs up an unparseable `source-file-versions.json` to `CONFIG/source-file-history/repairs/` and resets `files: {}` - i.e. recovery means *forgetting all version history*, not reconstructing it from blobs or intake artifacts; blobs remain on disk but orphaned [inspected, high].
4. Per-file intake rollback on write failure (`:378-387`).
5. Automatic move rollback when any file move fails (`move.mjs:576-607`).

Absent [inspected, high]:
- No recovery for corrupt `memory-settings.json`, `source-*-history.json` (bare `JSON.parse`, `settings-service.mjs:148`, `history.mjs:66`); a corrupt settings file makes every memory route throw.
- No integrity check of `AI_MEMORY/wiki` beyond link/index lint; no checksum of pages; no detection of partially written drafts/verifications (no temp+rename in `archive-review-service.mjs`).
- No crash-recovery test: the only corruption tests are (a) corrupt manifest -> `version-manifest-unavailable` -> repair (in-process self-test, `memory-source-file-intake-inprocess-self-test.test.mjs:53-65`, driving `browser-first-self-test-service.mjs:2019-2042`), (b) corrupt snapshot blob rejected (`memory-source-versioning.test.mjs:141-158`), (c) corrupt move manifest tolerated / rejected (`memory-source-move.test.mjs:725-790`), (d) corrupt destination bytes refused on rollback (`:624-652`). Nothing simulates a crash mid-promotion, a half-written review artifact, or a truncated `index.md`.

## Search

`memory-search.mjs:114-158` [inspected, high]: walks up to 600 markdown files under `AI_MEMORY/` (not INTAKE, not HUMAN/EXTERNAL), case-insensitive substring match. Score: +80 if the query appears on an `index.md` line that links the page, +40 title, +20 path, +min(30, 6*occurrences) in content. No tokenization, no stemming, no embeddings, no index persistence; every search re-reads every file. Requires >=2 chars. Capped at 50 results. The MCP portable fallback in `examples/living-archive-mcp.mjs:448-521` does a similar substring scan over all domains with score `1000 - matchIndex`. ADR-029 calls this "index-first LLM Wiki query pattern" [reported]; in code it is a keyword grep with an index bonus [inspected, high].

## LLM use in archive

Two LLM calls, both routed through `provider-bridge-service.mjs` and both optional [inspected, high]:
1. Ingest writer (`runArchiveIngestWriter` `:1159-1183` -> `memory-ingest-writer.mjs:86-177`): OpenAI-style `/chat/completions`, system prompt at `:58-67`, source truncated to 18 000 chars, index to 8 000. Output accepted only if >=300 chars and all 7 H2 sections present (`:38-48`); otherwise deterministic fallback string. **In the live service the result object's `content` field is never read** - `archive-review-service.mjs:354-366` reads `writer.summary/proposedPage/proposedContent/crossLinks/contradictionsOrCaveats`, none of which exist on the returned object. So even when a provider answers, the LLM draft is discarded [inspected, high].
2. Semantic verifier (`runArchiveSemanticVerifier` `:1065-1157`): prompt asks for strict JSON `{status: verified|needs-revision, summary, findings}` (`:1082-1089`); any HTTP error, missing provider, or parse failure yields `semanticStatus: "unavailable"` which **does not block** (`archive-review-service.mjs:464-466` blocks only on `needs-revision`). Caller may also pass `skipSemantic: true` (`:447-456`).
3. Route selection (`providerRouteForArchiveVerifier` `:1034-1049`): requested model if its secret exists, else `gpt-5.5` -> `zai/glm-5.2` -> `MiniMax-M3` -> null. The `archive-ingest` routing strategy with `hardStop: true` in `provider-fabric-core.mjs:99-108` ("stop if no trusted model is available") is **not consulted** by this function; the deterministic path proceeds when no model is available [inspected, high; "not consulted" based on grep of `archive-ingest|knowledge_promotion` in provider-bridge-service.mjs returning no hits].

What "verification" means in code (`archive-review-service.mjs:420-446`): take first 4 000 chars of source and proposed content, split into tokens >4 chars, count proposed tokens absent from source (first 8 unique); flag if >5 such tokens or proposed content <80 chars. That is the entire deterministic check; it is passed as `verified` by default. Semantic verification is an optional LLM opinion. Promotion then requires the verifier artifact to match the draft (policy) - but see Downgrades for why that call cannot succeed.

In the MCP/portable example, "verification" is a static checklist of four strings with empty findings (`examples/living-archive-portable-workflow.mjs:147-155`); no model is called anywhere in `examples/living-archive-*.mjs` (grep `fetch(` only in the proxy helper) [inspected, high].

## Host vs UI enforcement

Host-side (real) [inspected, high]: capability tokens per route (`memory-host-service.mjs`); path containment for every relative path (`safeMemoryRelativePathForRoot`, `memory-source-paths.mjs`); file-type gates (markdown only for review artifacts); confirmation phrases for move (`MOVE <name>`, `ROLLBACK MOVE`) and manifest repair; preflight fingerprint for move; `assertMemorySettingsSourceCanSave` blocks move-on-import via plain settings save; promote target must start with `AI_MEMORY/wiki/` (`archive-review-service.mjs:309-311, 690-692`); restore guards.

Host-side but ineffective [inspected, high]:
- Human-approval gate: `assertArchiveReviewTransitionAllowed` is called with `{metadata, fromStatus, toStatus, actor, actorType}` (`archive-review-service.mjs:266-280`) but its signature is `{metadata, nextStatus, actor, actorType}` (`archive-review-policy.mjs:27`); `nextStatus` is therefore `""`, the early return at `:29-31` fires, and escalated requests can be approved/rejected by any actor. Moreover the actor is whatever the client sends; the extension hardcodes `actor: "human", actorType: "human"` (`main-workspace-memory.js:546-556`). Even if the gate worked, "human" is self-asserted.
- Promotion policy: `assertPromotionVerifierMatchesDraft({draftPath, draft:{...}, verifier:{...}})` (`archive-review-service.mjs:669-684`) vs destructured flat parameters (`archive-promotion-policy.mjs:11-22`); `artifactVerificationStatus` is `undefined` -> throws "Draft promotion requires artifact verification status verified." on every call (`:23-25`). Net effect: no promotion can ever succeed through the bridge, so `AI_MEMORY/wiki` can only be populated by schema bootstrap, lint log appends, or external tools.
- Draft/revise: `buildDeterministicWikiDraft` returns a string (`memory-ingest-draft.mjs:97-131`) but is used as an object (`archive-review-service.mjs:332,354,360,363,366,600,606,609,612`); `deterministic.crossLinks` is `undefined`, so `.map` throws `TypeError` at `:363` before any artifact is written. Draft generation therefore fails for every request (the request file is also left untouched because the write at `:369-376` is never reached). [inspected, high. Caveat: I did not run the code; this is a static reading of two files written by the same commit 4098e28 (2026-06-02) with no later edits - `git log` shows one commit for each.]

UI-only [inspected, high]: button enable/disable logic in `memory-review-renderers.js:171,183,189,195,201,245,250` and `main-workspace-memory.js:660,677,684` (draft only when `approved`, promote only when `verified`, restore only when backup exists). These mirror host rules but are not the enforcement; a direct bridge call bypasses them. The pipeline text "Promote ... blocked until verified" (`memory-review-renderers.js:62`) is a rendering of frontmatter, not a check.

Docs-only [reported]: ADR-012's tiered `auto-approve / strategist-review / human-review` policy (`docs/architecture/ADR-012-living-archive-approval-policy.md:15-24`) - the only code trace is the metadata sniffing in `archive-review-policy.mjs:9-16`, which nothing in the host ever sets (no writer emits `humanReviewRequired`, `reviewGate`, `escalationStatus` - grep across `browser-first/host` finds them only in the policy and the transition reader).

## MCP example verdict

- `examples/living-archive-mcp.mjs` is a real MCP server: JSON-RPC 2.0 over stdio via `readline` (`:874-897`), `protocolVersion "2025-06-18"` (`:19`), handles `initialize`, `notifications/initialized`, `tools/list`, `tools/call` (`:836-871`), returns `content[]` + `structuredContent` (`:826-834`). 14 tools (`:217-388`): status, search, read, write_intake, request_ingest, review_queue, review_artifacts, process_ingest_request, decide_review, promote_review_artifact, maintenance_cycle, background_cycle, lint, semantic_lint. No `@modelcontextprotocol/sdk` dependency; hand-rolled, no resources/prompts, no capability negotiation beyond `tools: {}` [inspected, high].
- Two backends (`:390-399`): `host-http` proxying `POST <url>/memory/<operation>` with optional bearer token (`:88-114`), or `portable-folder` operating directly on a Memory root. Portable writes are limited to `INTAKE/mcp/<bucket>` and `INTAKE/review-queue` (`:553-650`); `--readonly`/`RESONANTOS_MCP_READONLY=1` disables writes.
- Portable promotion path (`examples/living-archive-portable-workflow.mjs:94-308`) is a **second, independent promotion implementation**: JSON review artifacts under `AI_MEMORY/provenance/review-artifacts/`, static "verification" checklist, decision by any `actorId` (default `strategist.core`, `:196`), `maintenanceCycle({autoApprove:true})` approves and promotes without any human (`:319-340`). It reuses `buildDeterministicWikiDraft`, `mergePromotedMarkdownBody`, `upsertWikiIndexCatalogEntry`, `searchMemoryWiki`, `computeWikiHealth` from `browser-first/host` and - unlike the bridge service - calls `buildDeterministicWikiDraft` correctly as a string (`:125-131`). So the only promotion code that can actually write `AI_MEMORY/wiki` in this repo is the *example*, not the Alpha bridge [inspected, high].
- `examples/living-archive-memory-service.mjs` is the loopback HTTP side (`POST /memory/<op>`, port 4888, refuses non-loopback without `--unsafe-host`, requires bearer token for the 7 write ops, falls back to readonly without a token, `:270-290`). It is the "live" backend the MCP server proxies to; it wraps the same portable bridge (`:142-170`), so "live mode" here means the same portable code behind HTTP, not the Alpha bridge.
- Wiring: not referenced anywhere in `browser-first/host` (grep `living-archive-mcp|memory-service` in `run-bridge-minimal.mjs` -> none). `package.json:12-14` exposes `npm run memory-service` and two test scripts; `scripts/verify-alpha.mjs:19-20` runs both test suites. ADR-029 (`docs/architecture/ADR-029-living-archive-mcp-bridge.md:5-10`): "Decision status: Accepted; Alpha applicability: Deferred; Optional external MCP services are not required Alpha runtime." It also describes Tauri IPC commands in `src-tauri/src/memory_service.rs` (`:27`) - **no `src-tauri/` directory exists in this clone** [inspected, high].
- The MCP operation contract (`status/search/read/intake-write/...`) is unrelated to the bridge's `/memory/*` and `/archive/*` routes; nothing translates between them [inspected, high].

## Tests table

CI reference: `stage1/sources/osmap/ci-alpha-build-39097845387-verify-log.txt` shows `test:browser-first` 2424 tests / 2414 pass / 0 fail / 10 skipped and both example suites passing (lines 3315-3390). Skips seen in code: symlink unavailable (`memory-source-move.test.mjs:272,709`), sandbox localhost denied (`examples/*.test.mjs`).

| File | Kind | Asserts (one line) | Skipped/mocked? |
|---|---|---|---|
| test/memory-host-service.test.mjs:46-99 | unit | route list + capability per route; throws if handler missing | handlers are no-op stubs |
| test/memory-ingest-draft.test.mjs:6 | unit | deterministic draft contains required sections/terms | none |
| test/memory-ingest-writer.test.mjs:41-113 | unit | prompt text; accepts valid provider draft; falls back on malformed | provider `fetchImpl` mocked |
| test/memory-schema.test.mjs:9-62 | unit (tmpdir) | creates 14 dirs + 3 files; does not overwrite | none |
| test/memory-search.test.mjs:9-63 | unit (tmpdir) | index hits outrank content hits; content fallback | none |
| test/memory-settings-policy.test.mjs | unit | move-on-import rejected on plain save | none |
| test/memory-single-file-intake.test.mjs | unit (extension lib) | text wraps as intake; binary -> metadata stub; size limits | none |
| test/memory-source-file-intake-inprocess-self-test.test.mjs | in-process self-test (spawns `run-browser-first.mjs --...-inprocess-self-test`) | 200-file batch, snapshot recorded, escape rejected, sync modes, corrupt manifest -> repair, redaction | real bridge in sandbox home; no LLM |
| test/memory-source-intake-host-service.test.mjs | unit | dependency fail-fast; disabled source blocked | all deps stubbed |
| test/memory-source-move-inprocess-self-test.test.mjs | in-process self-test | 403 without capability, stale preflight 500, move, rollback, partial rollback keeps registration, outside ledger 500 | real bridge in sandbox |
| test/memory-source-move.test.mjs (34 tests) | unit (tmpdir, real fs) | preflight guards, fingerprint, ledger rollback, hash mismatch refusal, corrupt manifest handling, confirmation phrase | 2 `t.skip` when symlinks unavailable |
| test/memory-source-paths.test.mjs | unit | containment + symlink rejection | none |
| test/memory-source-settings-service.test.mjs | unit | native picker argv/env hygiene on 3 platforms | `execFileStdout` mocked |
| test/memory-source-versioning.test.mjs (9) | unit (tmpdir) | version bump only on change; snapshot immutability; corrupt blob rejected; rollback of unfinalized reservation; path containment | none |
| test/memory-wiki-health.test.mjs (5) | unit (tmpdir) | broken links, orphans, dup titles/index, missing provenance, missing root | none |
| test/memory-wiki-lint.test.mjs (3) | unit (tmpdir) | writes REVIEW/lint artifact; appends log only if present | none |
| test/archive-merge.test.mjs (5) | unit | section merge, idempotence marker, index upsert dedupe | none |
| test/archive-promotion-guards.test.mjs (4) | unit | restore guard cases | none |
| test/archive-promotion-paths.test.mjs (3) | unit | backup filename/category | none |
| test/archive-promotion-policy.test.mjs (5) | unit | policy accepts/rejects with **flat** args | none - never called with the shape the service uses |
| test/archive-review-host-service.test.mjs (3) | unit | frontmatter helpers; containment; factory returns functions | `typeof === "function"` only; promote/draft never invoked |
| test/archive-review-policy.test.mjs (4) | unit | human gate with `nextStatus` | none - never called with `toStatus` as the service does |
| test/living-archive-continuity-acceptance.test.mjs:128-302 | integration (tmpdir, real service) | session store survives restart; intake + review request written; secret redacted | `runArchiveIngestWriter/Verifier` stubbed; stops before draft |
| test/main-workspace-memory.test.mjs (9) / -dom.test.mjs (4) | extension DOM unit | workspace renders and calls routes; revise/promote handoff flows | `bridgeRequest` fully faked (`:58-130`, `:1251-1413`) |
| test/settings-memory-save-refresh.test.mjs (4) | extension unit | save/refresh state machine | bridge faked |
| examples/living-archive-mcp.test.mjs (4) | integration (tmpdir; one spawns stdio server) | full portable loop incl. **decide + promote succeed** (`:124-139`); proxy via injected transport; stdio JSON-RPC flow | live HTTP test `t.skip` if localhost denied |
| examples/living-archive-memory-service.test.mjs (7) | integration | evaluator + HTTP flow; bearer token required for writes; readonly default | HTTP tests skip if localhost denied |

Crash/corruption recovery coverage: corrupt manifest (repair), corrupt blob, corrupt move manifest, tampered ledger - yes. Crash mid-write, partial artifact, corrupt settings/history JSON, corrupt wiki page - **no test** [inspected, high].

## Downgrades

1. **Promotion cannot succeed through the Alpha bridge** - `archive-review-service.mjs:669-684` vs `archive-promotion-policy.mjs:11-25` argument-shape mismatch; always throws. No test calls `executeArchiveReviewArtifactPromote` (grep across tests/scripts: only wiring in `run-bridge-minimal.mjs:298,371`). [high]
2. **Draft and revise always throw TypeError** - `deterministic` is a string; `.crossLinks.map` at `:363/:609`. No test calls `executeArchiveReviewDraft`/`Revise`. The extension tests "can revise a draft after verifier findings" and "focuses a promoted-page handoff" (`main-workspace-memory.test.mjs:1251,1351`) run against a hand-written fake bridge that returns success. [high]
3. **Human-approval gate is a no-op** - `toStatus` vs `nextStatus` (`archive-review-service.mjs:277`, `archive-review-policy.mjs:27`). Policy unit tests pass because they use the right name. Also no host code ever sets the escalation metadata the gate looks for, and `actorType: "human"` is client-asserted (`main-workspace-memory.js:552`). [high]
4. **"Verification" is a token-overlap heuristic**; LLM semantic check is optional and `unavailable` counts as pass (`archive-review-service.mjs:432-466`). [high]
5. **LLM writer output discarded** even when valid (`:354-366` read fields the writer never returns). [high]
6. **`archive-ingest` strategy `hardStop: true` not enforced** for archive routes (`provider-fabric-core.mjs:99-108` unused by `providerRouteForArchiveVerifier`). [high on code; medium that this is unintended]
7. **Domain separation is metadata** for the default import mode; `HUMAN_KNOWLEDGE/`, `EXTERNAL_KNOWLEDGE/`, `LOGS/`, `MANIFESTS/`, `AI_MEMORY/provenance/` are empty dirs in the bridge path. [high]
8. **Search is substring grep**, not semantic. [high]
9. **Manifest "repair" = reset**; version history is lost, blobs orphaned. [high]
10. **No fsync, no temp+rename** for review/wiki writes; frontmatter parsed by whole-file regex. [high]
11. **ADR-029 refers to `src-tauri/src/memory_service.rs`** which does not exist; MCP is Deferred for Alpha and unwired. [high]
12. **Single capability `archive-write`** covers browser intake and trusted-wiki promotion/restore alike. [high]
13. All review-pipeline code (`archive-*.mjs`, `memory-host-service.mjs`, intake/settings services) landed in one 25k-line commit `4098e28` "Stabilize browser-first release slice" (2026-06-02) and has not been edited since; the mismatches above are consistent with modules extracted from a larger file without an integration test. [hypothesis, medium]

## Duplicates/legacy

- **Live for Alpha**: `browser-first/host/memory-*.mjs` + `archive-*.mjs` behind the bridge; extension UI `browser-first/resonantos-side-panel-extension/src/lib/main-workspace-memory*.js`, `memory-review-renderers.js`, `memory-source-renderers.js`, `memory-single-file-intake.js`, `main-workspace-review-handoff.js`. `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md:75` names exactly these for `/memory/*`, `/archive/*`.
- **Example/duplicate promotion layer**: `examples/living-archive-portable-workflow.mjs` + `living-archive-mcp.mjs` + `living-archive-memory-service.mjs` (JSON artifacts under `AI_MEMORY/provenance/review-artifacts`, different review states `pending/approved/rejected/escalated/promoted`). Shares helper modules with the host but not the route layer. Last touched 2026-06-20 (`git log`). `examples/reference-memory-service.mjs` is a canned-response stub.
- **Legacy Vite/Tauri layer**: `src/core/memory-provider.ts` (broker over Tauri `invoke("archive_search")` etc., `src/core/runtime.ts:1045-1050`, throws "available only through the local bridge" when no command host), `src/core/context-memory.ts`, `src/modules/archive/*.tsx` (ArchiveWorkspace, ReviewDesk, SourceRegistry, LibraryImporter...), `src/modules/chat/archive-*.ts`. No import in either direction between `src/` and `browser-first/` (grep). `ALPHA_RUNTIME_BOUNDARY.md:140-143`: `src/` "does not add a third required Alpha runtime component"; `README.md:42`: "Shared TypeScript and React implementation used by development surfaces". Still edited as late as 2026-09-24 (`memory-provider.ts`) for the "harness projection" work, so it is maintained but not shipped in the Chrome-extension Alpha [inspected, high].
- Three `safeFileSlug`, two `listMarkdownFiles`, two `compactExcerpt`, two `markdownTitle` implementations across host modules (e.g. `archive-merge.mjs:3`, `browser-first-host-utils.mjs:182`, `memory-search.mjs:7`, `memory-wiki-health.mjs:8`) - harmless but a sign of copy-paste extraction.

## Coupling

- Memory depends on: provider bridge (`runArchiveIngestWriter`, `runArchiveSemanticVerifier`), host utils (`isInsidePath`, `listFilesRecursive`, `safeFileSlug`, `expandUserPath`, redaction), addon status (`executeAddonsStatus` for `memoryAddons` list, `settings-service.mjs:261,269`), capability tokens (`bridge-capability-tokens.mjs` references INTAKE per grep).
- Depends on memory: extension memory workspace; browser page actions (`browser-page-actions.js:748,896,974,1024`, `app-command-handlers.js:396` call `/archive/intake` to deposit research captures); self-test service (`browser-first-self-test-service.mjs:249-349, 1793-2042`); addon delegation receives `memoryRoot` (`run-bridge-minimal.mjs:190`) - not traced further here.
- Examples depend on host modules (`memory-search`, `memory-wiki-health`, `memory-ingest-draft`, `archive-merge`, `memory-schema`) - a reverse dependency from "optional example" into Alpha host code.

## Open questions

1. Does anything in the repo (scripts, addons, Hermes/OpenCode delegation) write to `AI_MEMORY/wiki` or `REVIEW/` outside `archive-review-service.mjs`? `grep INTAKE` in host lists `bridge-capability-tokens.mjs` and the delegation service receives `memoryRoot`; not traced.
2. Was the draft/promote pipeline ever exercised manually? Issue tracker references (#228 continuity, #94 "living-archive-copy" branch in CI log line 169) might show. The three interface mismatches would surface on the first click of "Draft".
3. `frontmatterValue` scanning the whole file: can a source document containing a line `status: promoted` or `verificationStatus: verified` in its body spoof review state when the frontmatter lacks the key? Static reading says yes for missing keys; not tested.
4. Windows: `chmod 0o600` is a no-op and `rename` atomicity differs; the move path's `rename` fallback to copy+rm is tested only on POSIX CI (`ubuntu` in log).
5. Is the `archive-ingest` routing strategy meant to be used by `providerRouteForArchiveVerifier`? Only the generic strategy plumbing references `hardStop`.
6. What does the extension show when `/archive/review/draft` returns a 500 TypeError - is there any telemetry? (UI catches and prints `error.message`, `main-workspace-memory.js:577-579`.)
