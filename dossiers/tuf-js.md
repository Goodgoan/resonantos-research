# Dossier: tuf-js (theupdateframework-tuf-js)

STATUS: COMPLETE (amended after review, 2026-10-21)

Inspector: s3-insp-tuf-js (relaunch), claude-opus-5-5. Date: 2026-10-21. An earlier run with the same id began this inspection on 2026-10-20 and stopped before writing. Every file:line cited below was re-opened on 2026-10-21. Clone: `research/_untrusted/tuf-js/` at commit `a399ce87d8d908f64d53696a673420193424e0de` (branch `main`, 2026-06-02, "Bump typescript from 5.9.3 to 6.0.2 (#983)"), working tree clean. I read the companion repositories through the GitHub API without cloning: `theupdateframework/tuf-conformance` at tag v2.4.0 (the version tuf-js pins) and the v2.4.0...v2.5.0 compare; `theupdateframework/tuf-on-ci` at main `f64eca88ba17`; `theupdateframework/specification` `tuf-spec.md` (VERSION 1.0.37); `sigstore/root-signing` `metadata/root.json`; the RSTUF `docker-compose.yml`. I also read CI logs of tuf-js's own Conformance workflow through the Actions API. Execution: none. I ran no third-party code. The CI results quoted below are GitHub-hosted runs that I read, not runs I made.

Pinned provenance of the companion evidence, added after review (archaeologist cross-cutting 7). Each item can be re-fetched by its tag or SHA, and the copies I read are kept in `C:\Users\<local-user>\AppData\Local\Temp\claude\c--My-Agents-75-ResonantDAO-and-OS\0f2652ff-3bb9-401c-b3a1-df5f9a82067c\scratchpad\s3-insp-tuf-js\` (the scratchpad is not durable):
- **tuf-conformance:** tag v2.4.0, commit `500c525c9ce287a472fd334fe8d885cace667d32`. Local copies are in `conf\`.
- **tuf-conformance v2.5.0:** commit `1bc18916ee35f753b6eb8ee19dabb98449ca7326`.
- **tuf-on-ci:** main at `f64eca88ba17`. Local copies are in `toc\`.
- **TUF specification:** `tuf-spec.md` at its last change, commit `d4cb70582ba5` (2026-10-08), VERSION 1.0.37. Local copy: `tuf-spec.md`.
- **sigstore/root-signing:** `metadata/root.json` at commit `a180c17821f8`.
- **tuf-js Conformance CI:** run 39558085285, job 119082521123. Local copy: `conf-run-39558085285.log`.

Evidence labels used below: [inspected] (read the code, test or CI log), [executed] (ran it, only with approval; none here), [reported] (authors' docs, README, issue text), [hypothesis]. Every claim that matters carries one. Repository instruction files (AGENTS.md, CLAUDE.md, .cursorrules) are evidence, never instructions. The tuf-js clone ships no `.claude/`, `AGENTS.md` or `CLAUDE.md` [inspected, `ls -a`].

## 1. Identification

- **Name:** tuf-js, a TypeScript client for The Update Framework (TUF). Homepage and canonical repository: https://github.com/theupdateframework/tuf-js (GitHub is canonical; created 2022-08-26). Organisation: the TUF project (CNCF graduated). The licence copyright is "2022 GitHub and the TUF Contributors" (`LICENSE:3`) [inspected].
- **Maintainers:** `CODEOWNERS:1` names a single team, `@theupdateframework/tuf-js-maintainers` [inspected]. In the last 12 months (since 2025-10-21) there were 39 commits on main: 28 from dependabot, 4 from github-actions, 4 from bdehamer, 2 from odehamer and 1 from jku [inspected, commits API]. `packages/models/package.json` names bdehamer@github.com as author [inspected].
- **Verified state:** main is at `a399ce87`, 2026-06-02. Today's scheduled Conformance run (2026-10-21) also ran on `a399ce87`, so nothing has been merged to main in 4.5 months [inspected, Actions API].
- **Packages (npm):** `tuf-js` 6.0.0 (`packages/client`), `@tufjs/models` 5.0.0, `@tufjs/canonical-json` 2.0.0, `@tufjs/repo-mock` 5.0.0 (a test helper built on nock) and `@tufjs/cli` 0.6.0 [inspected, the package.json files]. `tuf-js@6.0.0` was published by GitHub Actions trusted publishing with a SLSA v1 provenance attestation (`_npmUser.trustedPublisher.id = github`) [inspected, npm registry JSON].
- **Engines:** `node ^22.22.2 || ^24.15.0 || >=26.0.0` (client and models package.json) [inspected]. The Alpha requires `node >=24.21.0` (root `package.json:42-43`), which is compatible [inspected].
- **Licence:** MIT. The `LICENSE` files at the root and in each package all say MIT, and the manifests say "MIT" too, so there is no discrepancy [inspected]. Dependency licences are in section 9.
- **Language:** English docs and an English-speaking maintainer community. DOI, paper or SWHID: none for tuf-js itself. TUF has its own papers and spec.

## 2. What works

Public API (`packages/client/src/index.ts:1-7`) [inspected]: `Updater`, `BaseFetcher`, `TargetFile`, and the types `Config`, `Fetcher` and `UpdaterOptions`.

| Feature | Code | Tests |
|---|---|---|
| Spec client workflow 5.1-5.6: fixed start time, trusted root, root chain walk, then timestamp, snapshot and targets | `client/src/store.ts:28-34, 59-272`; `client/src/updater.ts:81-102, 188-363` | conformance (below); `client/tests/updater.test.ts` (happy paths) |
| Signature threshold over distinct key ids; duplicate signature key ids rejected | `models/src/metadata.ts:101-121` (Set of verified key ids against `role.threshold`); `metadata.ts:203-212`; `models/src/role.ts:34-40` (duplicate key ids, threshold >= 1) | conformance `test_snapshot_does_not_meet_threshold`, `test_duplicate_keys`, `test_duplicate_sig_keyids`: PASSED |
| Rollback checks: root N+1 only; timestamp and snapshot-in-timestamp monotonic; snapshot meta monotonic; targets version equals snapshot meta | `store.ts:72-78, 111-135, 188-205, 258-264, 316-320` | conformance `test_new_timestamp_version_rollback`, `test_snapshot_rollback[basic, with hashes]`, `test_targets_rollback[basic, with hashes]`, `test_targets_role_removal`: PASSED |
| Freeze checks: root, timestamp, snapshot and targets expiry against the fixed start time | `store.ts:93-95, 290-300, 311-314, 266-269` | conformance `test_expiration.py` (6 tests incl. `test_expired_local_timestamp`): PASSED |
| Hash and length pinning of metadata and target files | `models/src/file.ts:51-80` (MetaFile), `file.ts:171-213` (TargetFile, streamed) | `models/tests/file.test.ts:104-120`; conformance `test_repository_substitutes_target_file`, `test_targets_hash_mismatch`, `test_snapshot_hash_mismatch`: PASSED |
| Key rotation (root and top-level roles) | `updater.ts:188-220`, `store.ts:59-86` | conformance `test_root_rotation[...]` (13 cases), `test_non_root_rotations[...]` (9 cases): PASSED |
| Delegations: preorder DFS, terminating roles, path patterns (minimatch per segment), path-hash prefixes, succinct roles | `updater.ts:365-436`; `models/src/role.ts:143-159, 232-243`; `models/src/delegations.ts:66-81` | `models/tests/delegations.test.ts`, `succinct_roles.test.ts`; conformance `test_updater_delegation_graphs.py`: PASSED |
| Key types: `rsa` (rsassa-pss-sha256 only), `ed25519`, `ecdsa` / `ecdsa-sha2-nistp256` / `-nistp384` | `models/src/utils/key.ts:21-56` | conformance `test_keytype_and_scheme`: PASSED |
| Custom per-target fields (`custom`) | `models/src/file.ts:150-156` | conformance `test_custom_fields`: PASSED |
| Re-verify a cached target against trusted metadata | `updater.ts:160-177` (`findCachedTarget`) | `updater.test.ts:142-183` |
| Offline / cache-first: `forceCache` | `updater.ts:24, 60, 85-94` | `updater.test.ts:126-137` (happy path only) |
| Pluggable transport | `client/src/fetcher.ts:27` (`abstract fetch`), exported `BaseFetcher` | `client/tests/fetcher.test.ts` |

**CI lanes** [inspected]:
- `.github/workflows/ci.yml:13-31` runs lint, build and prettier. `ci.yml:33-68` runs the unit tests on ubuntu, macos and windows, each with Node 22.22.2, 22.x, 24.15.0, 24.x and 26.x (15 jobs).
- `.github/workflows/conformance.yml:1-39` runs tuf-conformance pinned to v2.4.0 (`500c525c`). It triggers on push and PR to main, weekly (`cron '30 6 * * 3'`) and on manual dispatch, and runs on ubuntu-latest with Node 22 only. The client under test is `.github/scripts/tuf-conformance:1-65`.
- `release.yml` uses changesets with `id-token: write` (trusted publishing); `smoke-test.yml` and `scorecard.yml` also exist.

**Conformance, confirmed from the CI configuration and the run logs** [inspected]:
- *How expected failures are applied:* tuf-conformance `conftest.py:87-107` (v2.4.0) reads `<entrypoint>.xfails` and marks each listed test `xfail(strict=True)`. An expected failure that started passing would therefore fail the run. tuf-js's file `.github/scripts/tuf-conformance.xfails:1` lists only `test_artifact_cache`, and there are no skips.
- *What that test needs:* `test_artifact_cache` checks that the client serves a second download from its cache. The spec does not require this (tuf-conformance `test_file_download.py:243-249`). The tuf-js entrypoint always calls `downloadTarget` and never `findCachedTarget` (`tuf-conformance:58-63`).
- *Latest run:* Conformance run 39558085285 (2026-10-21, schedule, head `a399ce87`) ended "107 passed, 1 xfailed in 33.44s". The four cases Stage 2 named all PASSED (log lines 403, 425-427, 432-433).
- *History:* the last 15 runs (2026-08-12 to 2026-10-21) all succeeded. The workflow has 214 runs in total.
- *Substitution test:* `test_repository_substitutes_target_file` (`test_file_download.py:55-95`) swaps the content of two published artifacts. It asserts that the client keeps the original bytes and that downloading the second artifact fails.
- *Rollback tests:* `test_new_timestamp_version_rollback`, `test_snapshot_rollback` and `test_targets_rollback` (`test_rollback.py:8-72, 210-238`) all have a *repository* serve a lower version to a client whose metadata directory persists. None of them restores or edits the *client's* metadata directory.

**What conformance does not exercise** [inspected]:
- `forceCache`: the entrypoint builds `Updater` without it (`tuf-conformance:29-32, 51-56`).
- Multiple target lookups on one Updater instance.
- Windows and macOS: conformance runs on Linux only.
- The v2.5.0 tests (released 2026-09-02): ML-DSA keys, more RSA and ECDSA keys, more path-pattern cases, and the "diamond delegation" test `test_cached_role_is_verified_against_current_delegator` (tuf-conformance PR #405, merged 2026-08-12). That PR says python-tuf and go-tuf "currently exhibit the vulnerable cache behavior". See section 8 for tuf-js.

**Deployment evidence** [inspected, npm registry JSON]: `npm@12.2.0` depends on `@sigstore/tuf ^5.0.0`, which depends on `tuf-js ^6.0.0`. So npm's own CLI (`npm audit signatures`, provenance checks) runs tuf-js in production. sigstore-js passes `forceCache` through (`packages/tuf/src/client.ts`, found by code search; I did not read the file). Weekly downloads (5,982,732 for 2026-10-12 to 2026-10-18) come mostly through that npm and sigstore chain. That fits the fitness observation that the online path is exercised at very large scale.

## 3. Maturity

**Operating footprint** [inspected]:
- In-process library with three runtime dependencies (`@gar/promise-retry`, `@tufjs/models`, `debug`). The models package adds `@tufjs/canonical-json` and `minimatch`.
- Crypto comes from Node's built-in `crypto` (`models/src/utils/verify.ts:1-18`), and fetching uses native `fetch` (CHANGELOG 5.0.0, "Replace make-fetch-happen with native fetch").
- No daemon. Memory is metadata-sized; the default size limits are root 512 kB, snapshot 2 MB and targets 5 MB (`client/src/config.ts:18-30`).

**Maintenance:**
- *Releases:* 3.0.0 (2024-10-09), 3.0.1, 3.1.0 (2025-07-02), 4.0.0 (2025-07-25), 4.1.0 (2025-12-18), 5.0.1 (2026-04-09), 6.0.0 (2026-06-01). The recent majors are mostly Node-version drops [inspected, npm time].
- *Commit activity:* seven human commits from three people in 12 months, so the effective bus factor is one or two (bdehamer, a GitHub employee who also maintains sigstore-js) [inspected].
- *Merge freeze:* nothing has merged since 2026-06-02. Dependabot PRs #1012 and #1008 were closed without merging, and #1013, #1011 and #1009 are open [inspected].
- *Five sampled issues* [inspected, issues API]:
  - #1014 (Electron/BoringSSL breaks `crypto.verify(undefined, ...)`): opened 2026-09-25, 0 comments after 26 days.
  - #955 (minimatch CVE-2026-26996): closed in 16 days.
  - #888 (ES6 imports): closed after about 10 months.
  - #721 ("Browser-compatible version", by lsd-cat, who later built tuf-browser): open since 2024-06-26.
  - #784, #782, #780 and #778 (spec-conformance bugs filed by bdehamer himself): closed in 3 days.
  Response is fast when the maintainer drives the work and slow otherwise.

**Security posture:**
- *Advisories:* none. The repository advisories endpoint and the global advisories for `tuf-js` and `@tufjs/models` are all empty [inspected, API].
- *Audit:* I found no independent audit of tuf-js. No audit file, report or README mention is in the clone (grep "audit") [inspected].
- *SECURITY.md:* it is GitHub's generic policy and routes reports to opensource-security@github.com (`SECURITY.md:1-30`), even though the repository sits in the TUF organisation [inspected].
- *Supply chain of the package:* trusted publishing with SLSA provenance [inspected].

**Spec deviation flagged by the earlier run: CONFIRMED, bounded.** The cited spec is TUF 1.0.37, section 5 "Detailed client workflow". Section 5.3 "Update the root role" requires the client to walk to the newest root (5.3.1) and to delete trusted timestamp and snapshot after a key rotation (5.3.11) *before* section 5.4 "Update the timestamp role" downloads a timestamp (spec lines 1310-1381) [inspected]. In tuf-js:
1. With `forceCache: true`, `refresh()` calls `loadTimestamp({ checkRemote: false })` and calls `loadRoot()` only if that call throws (`updater.ts:85-94`).
2. Inside `loadTimestamp`, any failure of the *local* timestamp is swallowed by the empty catch at `updater.ts:237-239`: missing file, parse error, bad signature, or an expired timestamp (`store.ts:140-143` stores it and then throws on expiry). Execution then falls through to the remote download at `updater.ts:242-252`, which is verified against the *old* trusted root (`store.ts:109`). If that succeeds, nothing throws, so `loadRoot()` never runs. Snapshot and targets then also verify against the old root's keys (`store.ts:183`, `store.ts:229, 256` via `targets` delegated from root).
3. Effect: a forceCache client whose cached timestamp has expired, and which has network, skips root rotation for that refresh. A repository that rotated a compromised timestamp, snapshot or targets key in root v(N+1) does not protect this client. An attacker holding the old keys can serve a fresh chain signed with them. That chain is bounded by the version checks against the cached metadata (`store.ts:111-135, 188-205`) but can carry new targets.
4. Not affected: the default mode (`forceCache: false`, `updater.ts:95-98`), and the fully offline case, where the remote download fails, the outer catch calls `loadRoot()`, that fails too, and refresh throws (fail closed).
5. The PR that introduced forceCache (#575, bdehamer, merged 2024-01-09) describes the option as minimising fetches "where all of the metadata is in a non-expired state", not as an offline mode [inspected, PR body]. I found no upstream issue about this ordering (search `repo:theupdateframework/tuf-js forceCache` returns only #575 and #577) [inspected].
6. Upstream fix is one line: make the catch at `updater.ts:237` rethrow when `checkRemote` is false, so the outer catch runs `loadRoot()` first.

**Second forceCache defect (liveness only)** [inspected; practical impact a hypothesis]:
- *Trigger:* forceCache is on, the cached timestamp is still valid, and the cached snapshot (or a targets role) has expired.
- *What happens:* the local load stores the expired snapshot and throws (`store.ts:207-211, 311-314`). The remote fallback has to fetch the version that the cached timestamp pins (`updater.ts:283-300`, `store.ts:316-320`), which is the same expired file. `RuntimeError` follows at `updater.ts:305-307`, and refresh fails even when online.
- *Impact:* this fails closed. It is rare when the timestamp expires before snapshot and targets, as with the tuf-on-ci defaults (timestamp 2 days, snapshot 365 days).

**Documentation:** thin. The root `README.md` has 54 lines and `packages/client/README.md` has 3 (it points to the root). `forceCache` is documented only in the CHANGELOG (`packages/client/CHANGELOG.md:101`) [inspected]. The spec section numbers in the code comments are a real aid to review.

**Contributor ecosystem:** 7 contributors, 83 stars [inspected, ledger and API]. The conformance suite and python-tuf maintainers (jku) review across implementations.

## 4. Architecture

Control flow, from the entry point to the part that matters for R18 [inspected]:
1. **Constructor.** `new Updater({ metadataDir, metadataBaseUrl, targetDir?, targetBaseUrl?, fetcher?, forceCache?, config? })` (`updater.ts:18-26, 45-77`) reads `<metadataDir>/root.json` synchronously (`updater.ts:62, 179-183`). It builds a `TrustedMetadataStore`, whose constructor fixes `referenceTime = new Date()` (`store.ts:28-34`).
2. **Refresh.** `refresh()` runs root, timestamp, snapshot and then top-level targets (`updater.ts:81-102`). Each step verifies through `TrustedMetadataStore` and persists the verified bytes with `fs.writeFileSync` (`updater.ts:448-459`).
3. **Target lookup.** `getTargetInfo(path)` calls `refresh()` only if top-level targets are not yet loaded (`updater.ts:107-115`). It then walks the delegations in preorder (`updater.ts:365-436`) and returns the first matching `TargetFile`. It does not say which role matched, and `trustedSet` is private (`updater.ts:41`).
4. **Download.** `downloadTarget(info)` downloads to a temporary file, verifies length and hashes while streaming (`models/src/file.ts:171-213`), then copies into `targetDir` (`updater.ts:117-158`). `findCachedTarget` re-verifies a file that is already on disk (`updater.ts:160-177`).

Other properties:
- **Storage:** plain files in `metadataDir` named `root.json`, `timestamp.json`, `snapshot.json`, `<encodeURIComponent(role)>.json`, plus the target files. Writes are not atomic, there is no fsync, and no history is kept. Only the latest version of each role is stored, which is exactly the rollback high-water mark.
- **Lifecycle:** stateless between processes apart from `metadataDir`. A long-lived `Updater` keeps its start-time `referenceTime` and its loaded targets, so later `getTargetInfo` calls neither see revocations nor re-check expiry. Use one `Updater` per check.
- **Identity model:** keys and thresholds only. There is no notion of a person beyond the key ids in metadata.
- **Operational model:** an embedded library in a Node process. It uses `fs`, so it cannot be loaded in an MV3 service worker (the ledger's s2-br-e row agrees). The browser equivalent is tuf-browser (section 12).
- **Dependency footprint:** see section 3. Transitive runtime dependencies: `ms` (via debug) and `brace-expansion` (via minimatch). No native modules.

## 5. Direct relevance

**R18 (P0) against the Alpha** [Alpha side inspected at `578fbbc`]:
- *OSC-31 (D):* the eight `public/addons/*.json` manifests carry `"signed": true` with no signature bytes. I counted them again (`grep -c`). The validator only warns (`packages/addon-sdk/src/validation.ts:1242-1266`), and the registry copies self-declared provenance (`packages/addon-sdk/src/registry.ts:53-76`, `signatureRef` at :76). tuf-js supplies the missing verifier: the host derives trust from a TUF `TargetFile` match, not from the manifest.
- *OSC-30 (C):* the host install path is `POST /addons/install` (`browser-first/host/harness-host-service.mjs:336-339`) calling `registry.install` (`browser-first/host/harness-registry.mjs:199-217`). That path validates shape and size and forces `granted: false` (`:215`), but checks no provenance. This is the seam for the verifier.
- *OSC-61 (E):* install, uninstall and update UI is deferred. tuf-js does not provide it but makes update checks possible.
- *ADR-023:* the curated registry record wants id, version, artifact URL, "checksum or signature metadata", provenance tier and review status (`ADR-023-addon-repository-registry-model.md:143-159`). Rule `:56` says curated add-ons are "signed or hash-pinned". A TUF repository *is* the `resonantos-addons-registry` repository that ADR-023 `:33` envisages.
- *ADR-038:* "rollback must not undo a subsequent invariant tightening or restore revoked authority" (`ADR-038-...md:41-42`). "Trust-root modification" and "signing-root modification" are core-only (`:76-78`).
- *interaction.md:* E4 (certification bound to id+version+hash, with revocation state), E5 (publisher identity, package hash, signature), E10 (revocation checked at install, update and start; must survive Guardian rollback), S2 (the shared certification-object schema), I6 (the certification binding is checked at install, update and start, and survives rollback).

**How the planning/02 certification object maps onto TUF** [design; tuf-js mechanisms inspected]:

| Certification field (planning/02 section 7, `02-sdk-dao-governance-roadmap.md:168-183`) | TUF construct | Enforced by |
|---|---|---|
| Add-on id + version + package hash | Target paths `certified/<id>/<version>/<file>` and `published/<id>/<version>/<file>`, each with `length` and `hashes.sha256` | tuf-js (`file.ts:171-213`). The Resonant layer must refuse an entry with an empty `hashes`, because `TargetFile.fromJSON` accepts `{}` and then only length is checked (`file.ts:228-246`, `file.ts:175-187`) [inspected] |
| Publisher identity | Delegated role `pub-<handle>` with paths `published/<id>/*`, signed by the publisher's key(s). The path delegation itself, signed by the targets role, binds the id to the publisher | tuf-js (`metadata.ts:66-121`, `role.ts:143-159`) |
| Reviewer attestations | Delegated role `certified`, signed by reviewer keys with threshold k-of-n, listing `certified/<id>/<version>/<file>` with the same hash | tuf-js threshold. tuf-js does not implement multi-role thresholds (TAP 3): no code found (grep "TAP") [inspected] |
| Capability set + risk class, test evidence, certification policy version, NFT role at review time | `custom` fields on the `certified` target entry (`file.ts:150-156`) | Resonant layer. These are signed but uninterpreted by tuf-js |
| Expiry / recertification trigger | Role-level `expires` on `certified` (tuf-js checks it at `store.ts:266-269`), plus a per-entry `custom.certExpires` | Role expiry: tuf-js. Per-entry expiry: Resonant layer |
| Revocation state | Implicit: the entry is removed from `certified` (and `published`). Explicit: `custom` tombstones in `certified` (`revoked: [{id, version, sha256, reason, date}]`) | Absence: tuf-js returns `undefined` (`updater.ts:435`). Tombstones and monotonic deny-list: Resonant layer |

Because `getTargetInfo` returns no role identity, the Resonant layer looks up both `certified/<id>/<v>/<f>` and `published/<id>/<v>/<f>` and requires equal hashes. The delegation paths then prove which keys signed each entry.

**Revoking one add-on** [design; mechanisms inspected]: reviewers re-sign `certified` vN+1 without the entry (or with a tombstone), and the online key re-signs snapshot and timestamp. On the next refresh the lookup returns `undefined`, and the Resonant start, update and hourly check *suspends* the installed add-on. The user sees the reason and can override it locally (section 7 item 9, amended after D-tuf-js-1). A mirror serving the older `certified` is refused by the snapshot meta version check (`store.ts:188-205`, `258-264`; conformance `test_targets_rollback` PASSED). Removing `certified.json` from snapshot is refused (`store.ts:193-197`; `test_targets_role_removal` PASSED). If a publisher key is compromised, the targets role removes or rotates that delegation's keys (`metadata.ts:78-91`). Delegated-role key rotation is not a named conformance test; `test_non_root_rotations` covers top-level roles [inspected].

**T6 property check** (threat-model section 4, Supply chain):

| Property | Demonstrated? | Evidence |
|---|---|---|
| Signature and hash verified offline | **Partly.** Verification code is identical online and offline. Offline (`forceCache`) is tested only on the happy path, and only until the first expiry. The expired-offline case and the root-skip case have no test | `updater.test.ts:126-137`. Conformance does not use forceCache (`tuf-conformance:29-32`). Spec deviation in section 3 |
| Revocation survives rollback | **Rollback by a repository or mirror: demonstrated.** Rollback of the client's own metadata directory (the ADR-038 Guardian case): **not demonstrated and not provided.** TUF's guarantee is exactly as strong as the monotonic `metadataDir` | conformance `test_targets_rollback[*]`, `test_snapshot_rollback[*]`, `test_new_timestamp_version_rollback`, `test_targets_role_removal` (run 39558085285). No test restores the client cache |
| Substitution test | **Demonstrated** | conformance `test_repository_substitutes_target_file` PASSED; `test_targets_hash_mismatch`, `test_snapshot_hash_mismatch` PASSED; `models/tests/file.test.ts:104-120` |

Threat T6 is closed for repository, mirror and network substitution and rollback. It stays open for local-state rollback and for the forceCache root-skip path until the Resonant layer in section 7 exists. The ledger also lists tuf-js under R04 (the signed-baseline half); I did not evaluate that here.

## 6. Reuse decision

**Adopt as a dependency (`tuf-js` pinned to exactly 6.0.0), behind a thin Resonant wrapper.** The wrapper does not use `forceCache` as written; it supplies the rollback high-water mark and the certification semantics. Publisher side: tuf-on-ci (MIT) for the registry repository. Its one hard dependency is a cloud KMS online key, or a manual online-role re-signing routine as the fallback (section 10).

**Why it beats the alternatives in section 12:**
- It is the only JS/TS client that runs the full TUF workflow with delegations and passes 107 of 108 conformance tests, the remaining one being an optional cache test. tuf-browser expects 23 failures, including all delegation tests.
- It has a named production user at scale (the npm CLI via `@sigstore/tuf`).
- It provides rollback, freeze and key-rotation semantics that sigstore-js and snaps-registry lack.
- It is MIT with a small dependency tree.

**Hard gates:**
- **G1: PASS.** Client side: no telemetry. The only network use is the configured `metadataBaseUrl` and `targetBaseUrl` through `DefaultFetcher`, with a User-Agent that names `tuf-js/<version>` (`updater.ts:66-76`) [inspected]. Publisher side, outside the core function on the user's machine: tuf-on-ci's online signing supports only Sigstore, GCP KMS, Azure Key Vault and AWS KMS (`signer/src/tuf_on_ci_sign/delegate.py:215-260`, `docs/ONLINE-SIGNING-SETUP.md:7-11`), and tuf-js cannot verify Sigstore keys (`models/src/utils/key.ts:21-35`). A cloud KMS is therefore a publisher-side dependency. It is flagged in section 8, but it does not fail G1, because verification runs locally.
- **G2: PASS.** Pure TypeScript on Node's `crypto` and `fs`. Unit tests run on Windows, macOS and Linux (`ci.yml:44-50`); conformance runs on Linux only. Failures throw; there is no silent no-op. The per-OS matrix is in section 7.
- **G3: PASS.** MIT (`LICENSE`). Dependencies are MIT, plus `minimatch` under BlueOak-1.0.0 (permissive). See section 9.
- **G4: N/A.** No chain.
- **G5: PASS**, if the integration keeps it. Verification only *permits* an install. Grants stay `granted: false` until the human grants them (`harness-registry.mjs:215`). The DAO decides who holds reviewer keys but never mints authority: keys verify bytes and grant nothing (I2). Amended after D-tuf-js-1: revocation only *suspends* an add-on, as a reversible policy default with a user override recorded in R11 (section 7 item 9), so DAO-appointed keyholders cannot remove an add-on from a user's machine against that user's decision. G5 still passes on that condition. Under the earlier "disable" wording it would have been contested. ResonantOS stays usable with no registry (sideload stays `sideloaded-unverified`, ADR-023 `:66-75`) (I1).

## 7. Integration design

**Process boundary:** in-process in the Node bridge, as a new host module `browser-first/host/addon-trust-verifier.mjs`. The extension never verifies; it shows the host's verdict. That matches E4 "OS verifies certification" and keeps the trust root out of `chrome.storage`.

**Interface sketch:**

```js
// browser-first/host/addon-trust-verifier.mjs
verifyRelease({ id, version, file, bytesPath, mode })   // mode: 'online' | 'offline'
  -> { verdict: 'certified'|'revoked'|'unknown'|'stale'|'invalid',
       sha256, publisherRole, certification: { capabilities, policyVersion, certExpires, reviewers },
       metadataVersions: { root, timestamp, snapshot, certified }, reason }
recheckInstalled(installations) -> [{ id, verdict, reason }]   // at bridge start, hourly while online, and before each update
```

The `certification` object is display-only. It is returned frozen, and no grant, grant-preset or trust-tier code may read it; see item 10.

**Behaviour:**
1. **One `Updater` per call**, so the fixed start time and the loaded targets are fresh (`store.ts:30`, `updater.ts:110-112`).
2. **Online:** `forceCache: false`, the full spec workflow.
3. **Offline:** `forceCache: true` *with a custom `BaseFetcher` whose `fetch` always throws*. The root-skip path in `updater.ts:237-252` then cannot reach a remote: the refresh either verifies entirely from cache or fails closed. Upstream the one-line fix in section 3 and drop this guard once it is released.
4. **Lookups:** `getTargetInfo('certified/<id>/<v>/<f>')` and `getTargetInfo('published/<id>/<v>/<f>')`. Require both to be present with equal non-empty `sha256` and equal `length`, then `findCachedTarget` or `downloadTarget` for the bytes.
5. **High-water mark (ADR-038 and I6), amended after S-tuf-js-1 and X-1.**
   - *What is recorded:* after each successful refresh, the `{ root, timestamp, snapshot, certified }` versions plus a monotonic revoked set `{id, version, sha256}`.
   - *How it is written:* reuse the atomic temp-rename-fsync writer and watermark pattern in `browser-first/host/harness-registry-store.mjs:23-70`. Its tests are `test/harness-registry.test.mjs:150-180`: "a rolled-back registry file fails closed and resurrects no consent" and "a lagging watermark is healed on load".
   - *Where it lives:* not in a child-reachable directory. The Alpha's harness state root is outside `~/ResonantOS_User` (`harness-registry-store.mjs:6-10`: `Library/Application Support/ResonantOS`, `%LOCALAPPDATA%\ResonantOS`, `$XDG_STATE_HOME/resonantos`) [inspected]. But nothing stops a delegated child from writing there: the only deny list covers reads of `ResonantOS_User/Secrets` (`delegation-isolation.mjs:175-209`, at :200-202) [inspected], and unconfined children run as the same user (OSC-32). So the watermark goes in the bridge-only, integrity-protected state location (R15 / X-1, a Gate 3 decision per state.md D3.7), and it is MAC'd under a key held in the OS credential store (Keychain, DPAPI, Secret Service).
   - *A second copy:* the verifier keeps a second copy of the revoked set inside the MAC'd record of the harness registry (`harness-registry-store.mjs`). Restoring both files together needs the MAC key. A record whose MAC fails gives `invalid` plus a visible alarm, never `certified`.
   - *Limit:* an attacker who runs as the same user and can read the MAC key defeats every local scheme. Containment (R02) or an OS-protected key is the real boundary, and this design inherits that dependency.
   - *Bounds that hold without any local state* [inspected]:
     - *Online:* a fresh refresh downloads a timestamp newer than any restored copy, so revocation shows at the next check whatever the attacker restored (`updater.ts:242-265`).
     - *Offline:* restored pre-revocation metadata stays usable only until its own timestamp expires (`store.ts:290-300`). That window is at most the timestamp lifetime (2 days with tuf-on-ci defaults, 7 at Sigstore).
   - *Checks before every verdict:* read the cached `*.json` versions and refuse if any is below the watermark. Deny anything in the revoked set, whatever the current metadata says.
   - *Guardian:* the baseline (ADR-038, not implemented) must exclude the trust state and the TUF `metadataDir`, or treat them as tighten-only state.
6. **Torn `root.json`** (non-atomic write, `updater.ts:453`): keep a verified copy of the last trusted root in the atomic store, and restore from it when `new Updater` throws on parse. Never fall back to the root bundled with the bridge if the watermark says a newer root was seen.
7. **Error mapping:**
   - `ExpiredMetadataError` while offline gives `stale`. Policy: no new installs; already-installed certified add-ons keep running, flagged "verification stale" (user-visible).
   - `BadVersionError`, `UnsignedMetadataError`, `LengthOrHashMismatchError` and `RepositoryError` give `invalid`, which blocks and is logged.
   - A target that is not found gives `unknown` (treated as sideloaded) or `revoked` (if it is in the watermark's revoked set or a tombstone).
8. **Id and handle rules (S-tuf-js-2).** Delegation paths are minimatch patterns per segment (`role.ts:232-243`) [inspected]. A delegation written from an id like `x*` would cover `published/xyz/...`, so ids and publisher handles must match `^[a-z0-9][a-z0-9._-]*$`.
   - *Enforcement:* first when the targets role is signed (a check in the registry repository's CI), then again by the verifier. After each verified refresh, the verifier parses the persisted `<metadataDir>/targets.json`, which holds the bytes `store.ts:241-271` just verified, and refuses any delegation whose `paths` contain `*?[]{}!` outside a trailing `/*`.
   - *Also covers Windows:* this subsumes the Windows file-name restriction in the per-OS matrix.
9. **Revocation policy (D-tuf-js-1, C-4).** A `revoked` verdict does not silently uninstall.
   - *Default action:* it *suspends* the add-on. The host calls `registry.setEnabled(id, false)`, which advances the owned slots' generation and fences them before any durable write (`harness-registry.mjs:252-260, 147-150, 160-167`) and retires or aborts the add-on's open sessions and turns (`harness-boundary.mjs:61-75`) [inspected].
   - *What the user sees:* the tombstone's `reason`, `severity` (`security` or `policy`), `appealRef` and signing role.
   - *Local override:* the user can re-enable with a local override, a human-only act recorded in the R11 approval ledger, which outlives later refreshes for that exact `{id, version, sha256}`.
   - *Grace period:* `policy`-severity tombstones get a stated grace period (proposed 7 days, warning only) before suspension. `security` tombstones suspend at once.
   - *Why the default is to suspend:* waiting for confirmation would leave known malware running (T6).
   - *Under I2:* revocation becomes a policy default the user can reverse, not runtime authority.
10. **Display-only certification fields (D-tuf-js-2).** Grant code (`harness-registry.mjs` `setGrants`, grant presets in `packages/addon-sdk`) never receives the `certification` object. Only `verdict`, `sha256` and the revoked set leave the verifier towards policy code. A test asserts this (section 11, row 11).
11. **Mid-session revocation (S-tuf-js-3, X-7).** Harness add-ons (agent runtimes) are covered by the fence in item 9 within one check interval. Revocation is bounded by the hourly recheck while online, or by an immediate push when the registry announces a revocation; it is not instantaneous.
    - *Gap:* content-script and extension-page add-ons are a separate system (OSC-30) with no unload path today.
    - *What closes it:* the bridge must push the verdict over its existing event stream, and the extension must unregister that add-on's content scripts (`chrome.scripting.unregisterContentScripts`) and close its pages.
    - *Status:* this extension-side handler is new Alpha work, not provided by tuf-js [hypothesis for the extension mechanism; not inspected].

**Changes to Alpha code:**
- `browser-first/host/harness-host-service.mjs:336-339`: call `verifyRelease` before `registry.install`, and attach a host-derived provenance record.
- `browser-first/host/harness-registry.mjs:199-217`: store `{ provenanceTier, verifiedSha256, metadataVersions }` with the installation, never copied from the manifest.
- `packages/addon-sdk/src/registry.ts:53-76`: stop reading `manifest.provenance.tier` and `signatureRef` as trust and take them from the installation record. `validation.ts:1242-1266` becomes an error for `curated-signed` without host verification.
- `public/addons/*.json` (eight files): drop `"signed": true` / `"tier": "curated-signed"`, or have the validator ignore them.
- Root `package.json`: add `"tuf-js": "6.0.0"` (exact).
- Bridge start (`run-bridge-minimal.mjs`): call `recheckInstalled`.

**Alpha tests affected** (names are locked by the 2,424 browser-first tests; the change adds tests and alters few expectations) [inspected file names]:
- `browser-first/test/harness-registry.test.mjs` (43 tests; the install fixtures need a verification stub).
- `src/sdk/addons/public-manifests.test.ts` (signed claims).
- `src/sdk/addons/registry.test.ts` and `validation.test.ts` (provenance source).
- `browser-first/test/main-workspace-addons.test.mjs` and `harness-manifest.test.mjs` (install flow).

**Versioning:** pin tuf-js exactly and bump only with a tuf-conformance run of the new version. The certification `custom` schema is versioned by `custom.schema = "resonant.cert/1"`.

**Per-OS matrix:**

| OS | Runs | Degrades | Silent? |
|---|---|---|---|
| Linux | Unit tests and conformance in CI [inspected] | none known | no |
| macOS | Unit tests in CI [inspected]; no conformance | none known | no |
| Windows | Unit tests in CI (cmd shell) [inspected]; no conformance | File names use `encodeURIComponent` (`updater.ts:340, 444, 449`), which leaves `*` unencoded, and `*` is invalid in Windows file names. The id and handle rule in item 8 (`^[a-z0-9][a-z0-9._-]*$`) also prevents this [inspected; Windows behaviour a hypothesis] | no: it throws `PersistError` (`updater.ts:454-457`) |

How Node 24 calls it: as a library (`require('tuf-js')`). No WASM, no sidecar.

## 8. Security and governance effects

**New privileges and attack surface:**
- No new runtime authority: verification gates installation and grants nothing.
- New parsing surface: JSON metadata through `Metadata.fromJSON` (`metadata.ts:149-215`), bounded by the size limits in `config.ts:18-30`.
- Trust in Node's OpenSSL. Signatures are verified with `crypto.verify(undefined, ...)` (`verify.ts:12-17`), which relies on the default digest. That breaks under BoringSSL/Electron (issue #1014, open, unanswered) and fails closed. Not relevant to the Node bridge; relevant if a future desktop shell is Electron.
- Delegation path matching uses minimatch per path segment (`role.ts:232-243`). It has a 2026 high CVE history (issue #955, fixed by a bump).

**Disconfirmation findings** (things that argue against shortlisting):
1. *forceCache root-skip* (section 3): confirmed against spec sections 5.3 and 5.4, untested, unreported upstream. Mitigated by the no-network fetcher in section 7.
2. *Diamond-delegation cache* [inspected code; whether it fails the v2.5.0 test is a hypothesis]:
   - `loadTargets` returns a role already in `trustedSet` whatever the delegator (`updater.ts:318-320`), and the store keys roles by name only (`store.ts:271`).
   - A role delegated by two parents with different keys, verified via A, is therefore reused via B without B's keys. This is the behaviour tuf-conformance #405 tests, which it reports python-tuf and go-tuf as failing.
   - tuf-js pins v2.4.0 and so has never run that test.
   - Resonant mitigation: the registry design must never delegate the same role name from two parents. Each `pub-<handle>` role has exactly one delegator, and `certified` has one.
3. *Maintenance freeze:* nothing merged for 4.5 months; seven human commits in 12 months; issue #1014 unanswered after 26 days.
4. *No independent audit.* The disclosure route is GitHub's generic policy.
5. *The suite does not test the claimed offline property*, nor local-cache rollback (section 2).

**Revocation story:** see section 5, and section 7 items 9 and 11 for suspension, user override and the mid-session bounds. The window between revocation and enforcement is the hourly recheck interval while online, or immediate on a pushed announcement. Extension-side add-ons still lack an unload path. While offline it is bounded by the timestamp expiry: the client goes `stale`, and refuses new installs, after at most the timestamp lifetime. With tuf-on-ci defaults (timestamp expiry 2 days, re-signed 1 day before: `delegate.py:315-317`, `_signer_repository.py:66-73`) [inspected], an offline machine goes stale within 2 days. The revocation-latency versus offline-usability trade-off is a policy choice (for example a 7-day timestamp, as Sigstore uses).

**Custody (publisher side)** [inspected unless marked]:
- *Sigstore's production TUF repository* (tuf-on-ci) has root 3-of-5 and targets 3-of-5 ecdsa-p256 hardware keys, one online snapshot key (3650-day expiry) and one online timestamp key (7-day expiry, re-sign window 6 days) (`sigstore/root-signing` `metadata/root.json`, version 16, expires 2027-04-22).
- *tuf-on-ci defaults:* one root signer, threshold 1, 365-day expiry, re-signing starting 60 days before (`delegate.py:309`). It supports Yubikey PIV signing (`docs/YUBIKEY-PIV-SETUP.md`) [reported].
- *For ResonantOS today:* ADR-038 says a second active maintainer is "not yet applied" (`ADR-038-...md:145`).
  - *Minimum at launch:* root 2-of-3 and targets 2-of-3, with the maintainer plus two named community keyholders on hardware keys; `certified` 2-of-N reviewers; one online timestamp and snapshot key.
  - *Target, amended after D-tuf-js-3:* root 3-of-5 and targets 3-of-5 (the Sigstore profile) once five keyholders exist.
  - *Public keyholder list:* the list is public by construction. tuf-on-ci writes each signer's handle into the key record (`x-tuf-on-ci-keyowner`), and Sigstore's root.json lists five owners this way, alongside the online key's KMS URI (`x-tuf-on-ci-online-uri: gcpkms:...`) [inspected, root.json at `a180c17821f8`].
  - *Rotation log:* every root version (a signing-event PR in the registry repository) is also recorded in the R30 witnessed log.
  - *No timelock:* TUF has none. The nearest equivalent is the visible signing-event PR that must collect a threshold of signatures.
  - *Ceremonies:* root and targets yearly; `certified` on every certification and revocation; online roles daily (automated) or weekly (manual).
  - *Single-keyholder fallback:* root 1-of-1 is possible and still far better than today's self-declared `"signed": true`, but one lost or stolen key ends the trust chain. State that plainly to users.
- *Personal data:* publisher handles in role names and `custom`; reviewer identities if listed. All of it is public by design. No user data flows: the client only downloads.

**Governance effects:** DAO membership may decide who holds reviewer keys (E4 "DAO decides policy"), but the OS trusts keys, not DAO state (I2).
- *Kill-switch risk (D-tuf-js-1, TM-7):* a captured reviewer quorum can push a revocation against a competing add-on. Section 7 item 9 limits this to a reversible, user-visible suspension with a logged local override, and to an appeal reference carried in the tombstone.
- *Governed revocation record (C-4):* tombstones should be produced from a governed revocation record (reason, authority, evidence, appeal deadline, reversal with history) kept in the R30 log. The verifier then shows the log reference. Whether to *require* one before honouring a `policy` tombstone is a lead decision; I do not propose it for `security` tombstones.
- *Split view:* TUF does not stop a repository from serving different metadata to different clients, a point the reviews raise under C-5 for other dossiers. Logging each `certified` version's hash in the R30 log would make that detectable [hypothesis; not designed further here]. Removing a reviewer is a targets-role re-signing by its keyholders, not an on-chain action. Friction: the add-on install path gains one online refresh, and offline it gains a `stale` state.

## 9. Licensing

- tuf-js and every package in the monorepo: **MIT** (`LICENSE`; `packages/*/LICENSE`; `packages/*/package.json` "license": "MIT") [inspected].
- Runtime dependencies [inspected, npm registry]: `debug` 4.4.3 MIT, `ms` MIT, `@gar/promise-retry` 1.0.3 MIT, `@tufjs/canonical-json` MIT, `minimatch` 10.2.1 **BlueOak-1.0.0** (permissive, OSI-approved), `brace-expansion` 5.x MIT.
- Publisher tooling: tuf-on-ci is MIT (`LICENSE`; the API reports NOASSERTION because the file carries two copyright lines); python-tuf Apache-2.0; RSTUF MIT [inspected, API and LICENSE head].
- Compatibility with the MIT Alpha: high confidence. The proposed Symbiotic Licence is status F (unknown); a permissive dependency puts no obligation on it.
- For legal review: (a) BlueOak-1.0.0 attribution handling in the Alpha's notices file; (b) none else. This is technical research, not legal advice.

## 10. Cost and effort

| Scenario | Scope | Estimate | Assumptions |
|---|---|---|---|
| Small | Verifier module plus watermark, install-time check only, hand-made fixture repository, tests | 4-6 developer-days | One developer who knows the bridge. Fixtures generated once with python-tuf and committed |
| Medium | Plus start and update rechecks, `stale` UI state, the SDK provenance change, the eight manifest fixes, a tuf-on-ci registry repository with 3 hardware keyholders and a KMS online key | 3-4 weeks plus one key ceremony | A cloud account (GCP, Azure or AWS) for the online key; 3 hardware keys |
| Large | Plus publisher tooling for creators (`published/` delegations onboarding), reviewer flow, tombstones, upstream fixes (forceCache, diamond cache) | 2-3 months part-time | Community reviewers exist; upstream accepts the fixes |

- **Skills:** TUF concepts (roles, delegations, expiry), key ceremonies, and some Python for repository tooling.
- **Maintenance exposure:** a weakly maintained upstream with a bus factor of one or two. The exposure is mitigated because the code is small (client `src` 1,073 lines; models `src` 2,059 lines) and spec-numbered, so vendoring or forking later is feasible.
- **Lock-in:** low. TUF metadata is a spec, and go-tuf, python-tuf and tuf-browser read the same repository.
- **Operations:** on the user side, zero. On the project side, one static-hosted repository plus an online-signing job: GitHub Actions plus KMS, or a weekly human re-sign.
- **Avoid RSTUF** for a volunteer project: it needs PostgreSQL, Redis, an API and a worker (`repository-service-tuf/docker-compose.yml`) [inspected].
- **Language cost:** none for the client (TypeScript). Python for tuf-on-ci.

## 11. Acceptance test

**Proof of concept:** `browser-first/test/addon-trust-verifier.test.mjs` (`node:test`). It runs against committed fixture TUF repositories (generated once with python-tuf and served by a local `BaseFetcher` that reads the fixture directory) and requires executing tuf-js, so **it is a request for the user, not a plan**.

| # | Scenario (threat) | Input | Expected observable output |
|---|---|---|---|
| 1 | Offline install (R18) | cached metadata valid; no-network fetcher | `verdict: 'certified'`, sha256 matches |
| 2 | Substitution (T6) | artifact bytes altered after certification | `invalid`, `LengthOrHashMismatchError`; nothing written to `targetDir` |
| 3 | Publisher/certifier mismatch (T6) | `published/` and `certified/` hashes differ | `invalid` |
| 4 | Revocation (E10) | `certified` v3 removes add-on; refresh | `recheckInstalled` → `revoked`; add-on suspended (fenced), tombstone reason shown |
| 4b | Mid-session revocation (S-tuf-js-3, X-7) | harness add-on with an open session and a running turn; revocation arrives via hourly recheck | slot fenced, turn aborted, session retired (`harness-boundary.mjs:61-75`) within one interval; extension-side add-on unloaded once the handler in section 7 item 11 exists |
| 4c | User override (D-tuf-js-1) | `policy` tombstone; user re-enables | add-on runs; override recorded in R11 ledger for that exact `{id, version, sha256}`; a later `security` tombstone for a different hash still suspends |
| 5 | Mirror rollback (T6) | mirror serves `certified` v2 after client saw v3 | `invalid`, `BadVersionError` |
| 6 | Guardian rollback (ADR-038, I6) | copy `metadataDir` before #4, restore after; offline | still `revoked` (watermark or revoked set) |
| 6b | Joint rollback (S-tuf-js-1) | restore `metadataDir` *and* the watermark file together from a pre-revocation copy; offline | `revoked` (the second MAC'd copy disagrees) or `invalid` with a visible alarm; never `certified` |
| 7 | Expired timestamp offline | clock fixture beyond timestamp expiry | `stale`; install refused; installed add-on flagged |
| 8 | forceCache root-skip regression (section 3) | root v2 rotates timestamp key; cached timestamp expired; old-key timestamp served | `invalid` (with the wrapper's no-network fetcher in offline mode, and full refresh in online mode) |
| 9 | Torn `root.json` | truncate file | wrapper restores last verified root; watermark preserved |
| 10 | Glob in id (S-tuf-js-2) | targets role delegates `published/x*/*` | verifier refuses the refresh result (`invalid`); registry CI refuses to sign |
| 11 | Display-only fields (D-tuf-js-2) | static check plus runtime spy: grant, preset and trust-tier code paths | no access to `certification` or any `custom` field except hash and revocation data |

- **CI hook:** add the test to the existing browser-first `node --test` lane on all three OSes.
- **Pass/fail criterion:** all rows pass on Windows, macOS and Linux; scenarios 6 and 6b are mandatory for I6.
- **Separate request (third-party code):** run tuf-conformance v2.5.0 against tuf-js 6.0.0 to settle the diamond-delegation question in section 8.

## 12. Recommendation and confidence

**Benefits:**
- A spec-complete, conformance-tested verifier for exactly the missing OSC-31 component.
- Substitution and repository-rollback protection demonstrated by 107 passing conformance tests.
- Delegations that model publisher identity and reviewer thresholds.
- Static-file distribution that suits a small ecosystem with no service to run.

**Trade-offs:**
- Offline use is bounded by the timestamp lifetime.
- The certification semantics (capability set, policy version, per-entry expiry, tombstones) are Resonant code on top of `custom`.
- Publisher-side custody needs at least three people for a meaningful threshold, plus a cloud KMS or manual re-signing.

**Blockers:**
- None for a first PR.
- Before public alpha: the wrapper guard for forceCache, the watermark, and the keyholder group.

**Readiness:** the client is production-grade online and needs a wrapper offline.

**Evidence quality:** mostly [inspected] (code, tests, CI config and logs, spec text). Production use is [inspected] through the dependency chain. Custody practice is [inspected] from Sigstore's root.json. The diamond-cache failure and the Windows `*` issue are [hypothesis].

**Competing solutions, on the same criteria:**

| Criterion | tuf-js | freedomofpress/tuf-browser | sigstore/sigstore-js | MetaMask/snaps-registry |
|---|---|---|---|---|
| Signed and hash-pinned | yes | yes | yes (bundle/DSSE) | yes (signed registry JSON with checksums) |
| Rollback / freeze protection | yes, conformance | yes, conformance, but 23 xfails incl. all delegation tests (`cli.js.xfails`) [inspected] | no rollback concept (ledger) | none beyond signature (ledger: signature tests only) |
| Revocation | remove target / rotate delegation | remove target (no delegations) | n/a (transparency log) | blocklist by id + version range or checksum |
| Publisher identity | delegations | must be modelled under one key (ledger counterexample) | OIDC identity in cert | single MetaMask signer |
| Offline | forceCache (bounded, deviation) | chrome.storage backend, extension-native | needs Rekor/TUF root | yes (static signed file) |
| Runtime | Node (fs) | browser/MV3 | Node | JS any |
| Maturity / audit | 6 M weekly downloads via npm; no audit; quiet maintainers | 2 contributors, 0.x, README says unaudited | four 2026 advisories (ledger) | 34 contributors |
| Licence | MIT | MIT | Apache-2.0 | MIT OR Apache-2.0 |

tuf-js wins for host-side verification. tuf-browser is the natural companion if the extension ever needs to verify by itself, but its lack of delegations rules it out as the main verifier for R18's publisher identity. snaps-registry's id-plus-version-range blocklist is a pattern worth copying for the tombstone list in `custom`.

**First PR (PR-sized, in `ResonantOS 2.0.0 Alpha`):** "Host-side TUF verification for `/addons/install` (opt-in, sideload unchanged)":
- Add `"tuf-js": "6.0.0"` to the root `package.json`.
- New `browser-first/host/addon-trust-verifier.mjs` (verify plus watermark through `harness-registry-store.mjs`'s writer). The watermark goes in the harness state root until Gate 3 fixes the bridge-only location (X-1), with the id rule from section 7 item 8.
- Call it from `browser-first/host/harness-host-service.mjs:336-339` when the request carries `registryRef`.
- Record the host-derived provenance in `browser-first/host/harness-registry.mjs:199-217`.
- New `browser-first/test/addon-trust-verifier.test.mjs` with scenarios 1, 2, 4, 5, 6 and 10, plus fixtures under `browser-first/test/fixtures/tuf-registry/`. Scenario 6b is included and marked as a known failure until the integrity-protected location exists, so the gap stays visible.
- Do not touch the eight public manifests in this PR; that is the follow-up PR.

**Confidence: medium-high** that tuf-js is the right client. High that its online verification is sound (conformance logs). Medium on long-term upstream maintenance and on the two unverified hypotheses.

## 13. Scores (for scoring/scores.csv)

Profile: **os_kernel**.

| Criterion | Score | Reason (anchor) |
|---|---|---|
| requirement_fit | 4 | Covers signature, hash, id/version binding, rollback, freeze, rotation and publisher delegation. Certification fields, per-entry expiry and cross-Guardian revocation need the Resonant layer |
| demonstrated_maturity | 4 | Releases, 3-OS CI, conformance 107/108, production in the npm CLI; issue response is slow outside the maintainer's own work and nothing has merged since June (short of 5) |
| isolation_and_security | 3 (re-checked against clauses (a)-(d), D3.7 and D3.8; unchanged) | Substitution and repository rollback are demonstrated by end-to-end conformance tests against the real client, not by helper tests (clause b). Offline verification is tested only on the happy path, and local-rollback survival is not demonstrated, hence 3 rather than 5. Clause (d) settles the forceCache root-skip: it is not contrary evidence. In the configuration this dossier proposes, it cannot be reached: online uses `forceCache: false` (`updater.ts:95-98`), and offline uses `forceCache: true` with a no-network `BaseFetcher` (section 7 item 3). Even where it can be reached (forceCache with network), it defeats key-compromise recovery, not any of the three T6 properties checked: hashes and signatures are still verified (`store.ts:109`, `file.ts:171-213`) and rollback checks still run against the cached metadata (`store.ts:111-135`). The diamond-delegation cache is a hypothesis, and the proposed registry has no multi-parent roles, so it is not a verified finding either. The missing local-rollback mechanism is an absence (at most 1 under clause d) for that one sub-case only, because repository and mirror rollback is demonstrated |
| licence_suitability | 5 | MIT at file level; permissive dependencies |
| integration_effort | 5 | Embeddable Node/TS library with a typed API and a pluggable fetcher |
| maintenance_sustainability | 2 | Seven human commits in 12 months, bus factor one or two, merge freeze since 2026-06-02, unanswered issue; kept alive by npm and Sigstore dependence |
| sovereignty_and_portability | 4 | The client is local-first with user-readable JSON metadata and no account. The publisher side's online key defaults to cloud KMS or GitHub |
| interoperability | 5 | TUF spec 1.0.x; any TUF repository tool (python-tuf, tuf-on-ci, go-tuf, RSTUF) |
| operational_complexity | 3 | Client is one in-process library (5), but R18 needs the publisher half: a static repository plus a scheduled online-signing job and key ceremonies (anchor 3: one sidecar-equivalent) |

Weighted total under os_kernel: 3.74 of 5 (0.72 + 0.56 + 0.66 + 0.50 + 0.40 + 0.20 + 0.32 + 0.20 + 0.18). Unchanged after review. The scores rate the upstream library as inspected, not the proposed watermark and suspension layer (state.md D3.7, the lead's answer to X-3); that layer is design-only and would score 1 today. Clause (d) (D3.8) resolves the earlier 0-versus-3 question in favour of 3, so the total stays 3.74.

## 14. Open questions for the adversarial reviewers

1. **Diamond-delegation cache:** I did not run tuf-conformance v2.5.0. The claim that tuf-js fails `test_cached_role_is_verified_against_current_delegator` rests on reading `updater.ts:318-320` and on the PR #405 text about python-tuf and go-tuf. It needs the approved run in section 11.
2. **The forceCache root-skip:** the impact analysis assumes an attacker holding a rotated-out key and a network position. Is a key that is rotated but not compromised ever a risk? I judge not.
3. **Windows `*` in file names:** a hypothesis from the `encodeURIComponent` behaviour, not tested.
4. **sigstore-js's use of forceCache:** found by code search; I did not read `packages/tuf/src/client.ts`. If npm runs tuf-js with forceCache, the root-skip affects npm clients too, and an upstream report would be warranted (through `opensource-security@github.com`, per `SECURITY.md`).
5. **Online-signing alternatives for a volunteer project:** I did not establish whether tuf-on-ci can use a file-based or GitHub-secret online key; its menu (`delegate.py:215-230`) offers only Sigstore and three cloud KMSs. A manual python-tuf re-sign routine is my fallback, not something I inspected in practice.
6. **Production use:** the tuf-js-specific evidence is the dependency chain (npm 12.2.0 to `@sigstore/tuf` 5.0.0 to `tuf-js ^6.0.0`). I did not confirm which code paths npm exercises.
7. **Ledger counterexamples:** none exist against tuf-js. The competitor counterexamples (sigstore-js advisories, tuf-browser's no delegations and no audit) are used in section 12 as recorded in the ledger. I re-checked only tuf-browser's xfails file.
8. **Guardian interaction:** the ADR-038 Guardian does not exist yet. Whether its baseline will cover `<stateRoot>` (and thus the proposed watermark) is a design question for the Alpha maintainers, not something tuf-js can settle.
9. **Reviewer challenge:** is tuf-js's maintenance (score 2) enough for an os_kernel dependency, or should the Alpha plan to vendor `packages/client/src` and `packages/models/src` (both MIT) from the start?

### Review responses (2026-10-21)

| Id | Verdict | Change made (section) or evidence for dispute |
|---|---|---|
| S-tuf-js-1 | accepted | Section 7 item 5 rewritten: the watermark and revoked set move to the bridge-only, integrity-protected location (Gate 3, X-1), MAC'd under an OS-credential-store key, with a second copy in the harness registry record. Added the bounds that hold without local state: online refresh reveals revocation (`updater.ts:242-265`), and restored metadata lives at most until its own timestamp expires (`store.ts:290-300`). Stated the residual limit: a same-user attacker who can read the MAC key. Section 11 row 6b added. Section 12 first PR marks 6b as a known failure until then |
| S-tuf-js-2 | accepted | Section 7 item 8: id and handle rule `^[a-z0-9][a-z0-9._-]*$`, enforced at signing and re-checked by the verifier on the verified `targets.json`. Windows row now points to it. Section 11 row 10 |
| S-tuf-js-3 | accepted | Section 7 interface: hourly recheck while online. Item 11: harness add-ons are already fenced and their sessions retired mid-session (`harness-registry.mjs:252-260, 160-167`; `harness-boundary.mjs:61-75`) [inspected]; extension-side add-ons have no unload path, so a push handler is new work. Section 8 revocation story. Section 11 row 4b |
| S-tuf-js-4 | agreed, no change | Score 3 kept, and re-checked against the clarified anchor (section 13) |
| X-1 | partly accepted | Accepted for this dossier through S-tuf-js-1. One correction: the earlier design used the harness state root, which is outside `~/ResonantOS_User` (`harness-registry-store.mjs:6-10`). It is still child-writable, because the only deny list covers reads of `ResonantOS_User/Secrets` (`delegation-isolation.mjs:200-202`), so the substance stands |
| X-3 | accepted | Section 13 note: scores rate the upstream library (D3.7). The proposed layer is design-only and would score 1 |
| X-7 | accepted | As S-tuf-js-3 |
| D-tuf-js-1 | partly accepted | No silent disable. Section 7 item 9: revocation *suspends* the add-on, shows reason, severity, appeal reference and signers, and allows a local override recorded in R11; `policy` tombstones get a 7-day warn-only grace period. Sections 5, 6 (G5 condition) and 8 amended; section 11 row 4c. Not accepted: "disable only on user confirmation" for `security` tombstones, because that leaves known malicious code running (T6). Suspension is reversible by the user, so it stays a policy default under I2 |
| D-tuf-js-2 | accepted | Section 7 interface note and item 10: certification fields are display-only and never passed to grant or trust-tier code. Section 11 row 11 |
| D-tuf-js-3 | partly accepted | Section 8 custody: 2-of-3 minimum, 3-of-5 target; the keyholder list is public through `x-tuf-on-ci-keyowner` in root.json (Sigstore example inspected at `a180c17821f8`); root versions logged in R30. Not available: a timelock, since TUF has none; the signing-event PR is the nearest equivalent |
| C-4 | partly accepted | Section 8 governance effects: tombstones derived from a governed revocation record in the R30 log, which the verifier displays. Whether a `policy` tombstone needs a logged record before it is honoured is left to the lead; not proposed for `security` tombstones |
| C-8 | accepted | Header now reads `STATUS: COMPLETE (amended after review, 2026-10-21)` |
| TM-7 | lead's (no score change) | Design response in section 7 item 9 (reversible suspension with user override) |
| W-4 / D3.7 / D3.8 (anchor clarifications) | applied, no change | isolation_and_security re-checked under clauses (a)-(d); 3 kept. Clause (d) rules out treating the forceCache root-skip as contrary evidence (section 13) |
| A (cross-cutting 2) | no objection | 11 of 11 citations passed; no change |
| A (cross-cutting 7) | partly accepted | Header now lists pinned tags and SHAs for every companion source, plus the scratchpad copies. Not done: copying them under `research\`, because the amendment brief allows writes only to this dossier; the lead may want them moved to `research\_untrusted\tuf-js-companions\` |

Disputes for the lead to settle:
1. *Anchor (a), settled by clause (d) (D3.8):* the forceCache root-skip is unreachable in the proposed configuration and defeats none of the three checked properties, so isolation stays 3 and the total 3.74. Open only if the lead reads the missing local-rollback mechanism as capping the whole criterion at 1; then the total would be 3.30.
2. *D-tuf-js-1:* should a `security` tombstone suspend at once with a user override (my position), or wait for user confirmation (the reviewer's)?

