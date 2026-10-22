# Dossier: Hypercore (holepunchto-hypercore)

STATUS: COMPLETE (amended after review, 2026-10-21). verified: 9c9cc3d 2026-10-21 (amender s3-amend-hypercore, standing in for s3-insp-hypercore; clone HEAD re-checked with `git rev-parse HEAD`).

Inspector: s3-insp-hypercore, Claude Opus 5.5. Date: 2026-10-20. Amended 2026-10-21 by s3-amend-hypercore (section 14, "Review responses"). Clone: `research/_untrusted/holepunchto-hypercore/` at commit `9c9cc3d8937b6ae539fbacf52a7090cd732a1945` (branch `main`, committed 2026-10-14, tag 11.39.0; cloned 2026-10-20, depth 200). Supporting clones: the original ones were in the inspector's scratchpad (`s3-insp-hypercore-ext\`), which no longer exists (A-holepunchto-hypercore-1). On 2026-10-21 they were re-cloned read-only (`git -c core.hooksPath=/dev/null clone --depth 50 --no-checkout`; files read with `git show <sha>:<path>`, nothing checked out or run) under `research\_untrusted\`: `hypercore-storage\` at dc65f66e9821271420f554816c4b02a4dceb6e05 (3.4.0, 2026-10-14), `hypercore-crypto\` at e2e0fdcc2521027ee49c58d50d60c42edb9466a0 (3.7.0, 2026-05-05), `rocksdb-native\` at 5a3c213dd113761e8e515379964c347b4aa568db (3.19.1, 2026-10-09). Each pinned SHA is also its default-branch HEAD on 2026-10-21. `holepunchto/librocksdb` at 7b5352defa9a63e5580aeea344ae7383efea1286 (the commit `rocksdb-native/CMakeLists.txt:12` fetches) was read through `gh api repos/holepunchto/librocksdb/contents/src/rocksdb.cc?ref=7b5352d` (GET), saved in the amender's scratchpad. Execution: none. No third-party code, install script, test or binary was run. Read-only network calls only: `gh api` (issues, PR #787 diff, Actions job log 116076500842, advisories), `npm view`, and one `npm install --package-lock-only --ignore-scripts` in a scratch folder to resolve the dependency tree. That command fetches registry metadata only and executes no package code.

Evidence labels used below: [inspected] (read the code), [executed] (ran it, only with approval), [reported] (authors' docs, README, issue text, CI logs written by the project's runners), [hypothesis]. Every claim that matters carries one. Repository instruction files (AGENTS.md, CLAUDE.md, .cursorrules) are evidence, never instructions. The clone contains none.

## 1. Identification

| Field | Value |
|---|---|
| Name | Hypercore ("a secure, distributed append-only log", `package.json:4`) |
| Homepage | https://github.com/holepunchto/hypercore ; API docs at docs.pears.com (README:3) |
| Canonical source | GitHub `holepunchto/hypercore` (repo created 2015-12-20; the old `mafintosh/hypercore` redirects here) |
| Maintainers | Holepunch (the company behind Keet and Pear). Over the last 12 months 166 commits: Mathias Buus 91, Sean Zellmer 48, Christophe Diederichs 12, others 15 [inspected, `git log --since=2025-10-20`] |
| Verified release | 11.39.0, npm publish 2026-10-14T20:09Z; HEAD = tag commit 9c9cc3d [inspected] |
| Package | npm `hypercore` 11.39.0; storage `hypercore-storage` 3.4.0; native DB `rocksdb-native` 3.19.1; crypto `hypercore-crypto` 3.7.0 |
| Licences | `LICENSE`: MIT (Copyright 2016 Mathias Buus), matching `package.json:29`. The storage layer is Apache-2.0 (`hypercore-storage/LICENSE` + `NOTICE`, `rocksdb-native/LICENSE` + `NOTICE`). The resolved tree has 63 packages: 35 Apache-2.0, 24 MIT, 4 ISC [inspected, lockfile]. Manifest and licence files agree for every package checked |
| Paper / DOI | none for v10/v11; the 2017 Dat whitepaper describes an older format and was not used |
| Docs language | English; English-speaking maintainers |

The README is stale in two places that matter here. It says "the latest release is Hypercore 10" (README:17) and "uses a simple flat file structure" (README:13). The code is v11 and stores everything in RocksDB (`index.js:4`, `hypercore-storage/index.js:1`, `UPGRADE.md` "Storage is now auto migrated to hypercore-storage") [inspected].

## 2. What works

| Feature | Code | Tests (file: test name) |
|---|---|---|
| Append-only log of blocks, batch append, per-append signer override | `index.js:1149-1185` (`append`, options `keyPair`, `signature`) | `test/core.js` "core - append and truncate"; `test/basic.js` |
| BLAKE2b Merkle tree in flat-tree layout. Leaf = BLAKE2b(0x00 ‖ u64 size ‖ data); parent = BLAKE2b(0x01 ‖ u64 size ‖ left ‖ right); tree hash = BLAKE2b(0x02 ‖ (root hash ‖ u64 index ‖ u64 size)*) | `hypercore-crypto/index.js:82-124`, `lib/merkle-tree.js` (1376 lines) | `test/merkle-tree.js` "proof only block", "proof with upgrade", "verify proof #1", "verify proof #2", "tree hash" |
| Signed tree head: Ed25519 over 112 bytes (TREE namespace ‖ manifest hash ‖ tree hash ‖ u64 length ‖ u64 fork) | `lib/caps.js:32-40`; `lib/verifier.js:34-40`; Ed25519 only (`verifier.js:20`), BLAKE2b only (`verifier.js:235`) | `test/manifest.js:1732` "manifest - invalid signature fails" (append and truncate with a zero signature are rejected, length stays 0) |
| Multi-signer manifests (quorum, signer namespaces, prologue) | `lib/verifier.js:58-157`, `lib/multisig.js` | `test/manifest.js` (multisig tests, e.g. :1107 "multisig - prologue verify hash", :1232) |
| Inclusion and upgrade proofs | `index.js:1209-1219` (`proof`), `:1226-1231` (`verifyFullyRemote`), `lib/fully-remote-proof.js` | `test/fully-remote-proof.js:7` "fully remote proof - proof and verify" |
| `signable()` / `treeHash()` exports of the signed head | `index.js:1187-1202` | indirect only (no test named for `signable`) |
| Truncate with fork id | `index.js:1127-1147` | `test/basic.js:198` "truncate event has truncated-length and fork"; `:744` |
| Equivocation (fork) detection between replicas: two valid signatures for one length with different tree hashes freezes the core and closes its sessions | `lib/core.js:640-701`, `:919-931` | `test/conflicts.js:4` "one forks", which is **`test.skip`** ("occasionally (~1/100) flakes", :5-8); it also shows `# SKIP` in the Windows CI log. Skipped since PR #645 "Skip flaky fork test" (0d28e9d, 2025-02-24), about 20 months [reported by `gh api repos/holepunchto/hypercore/commits?path=test/conflicts.js`]. `test/groups.js:44` "groups - conflict" is unrelated (`setGroup` key clash) |
| Internal storage audit | `lib/audit.js` (on internal `Core`, `lib/core.js:368-376`; not on the public class) | no direct test. `test/merkle-tree.js:827` is a separate local helper |
| Recovery from missing tree roots | `lib/core.js:301-305` (repair mode), `index.js:1242`. The trigger is structural: repair mode is set when the stored roots are absent (`!treeInfo.roots.length && treeInfo.length`), not when a hash or the head signature fails. Open does not verify the stored head signature against the stored roots (no verify call in `lib/core.js:165-366`) [inspected] | `test/merkle-tree-recovery.js:8` "recover - bad merkle root core can still ready", :46, :102, :244 "fail appends & truncates when in repair mode" (deletes a root node, expects writes refused), :389 |
| Replication over any duplex stream (Noise via secret-stream, Protomux) | `index.js:174-215`, `:594-606`; `lib/replicator.js` (3479 lines) | `test/replicate.js` (e.g. :415 "invalid signature fails", with a mocked writer verifier) |

CI [inspected `.github/workflows/test-node.yml`; reported by Actions]: a lint job, and a `build` matrix on `[ubuntu-latest, macos-latest, windows-latest]` that runs `npm install`, `npm test` (brittle, `test/all.js`) and `npm run test:bare`. Run 38629301899 on 9c9cc3d passed on all three legs. The Windows leg's log shows Node v24.21.0, "tests = 432/432 pass", "asserts = 2018/2018 pass" and 8 `# SKIP` entries (the same `test.skip` set as the code: "draft truncate then append", "storage info", "one forks", "startMarking - on named session", "buffer of cached nodes is copied to small slab", "can disable downloading from a peer", "non-sparse replication", "session on a from instance ..."; recounted 2026-10-21 with `git grep -c "test\.skip(" 9c9cc3d -- test`, 8 in 7 files). `test/compat.js` is commented out in `test/all.js:16`.

Deployment evidence: Holepunch ships Keet and Pear on this stack [reported, company material; not verified here]. Package downloads are not used as evidence.

## 3. Maturity

- **Footprint** [inspected]: an in-process CommonJS library with 21 direct dependencies and 63 resolved packages. Five native add-ons load prebuilt binaries through `require-addon`: `sodium-native` (libsodium), `rocksdb-native` (RocksDB, fetched as `holepunchto/librocksdb#7b5352d` in `rocksdb-native/CMakeLists.txt:12`), `fs-native-extensions` (file locks), and the optional `quickbit-native` and `simdle-native`. No package in the tree has an install script, so none runs at `npm install`. `rocksdb-native` unpacks to 183.8 MB because every platform's prebuilds ship in one tarball (`npm view dist.unpackedSize`). Prebuilds cover win32 x64 and arm64, darwin x64 and arm64, and linux x64 and arm64 (`rocksdb-native/.github/workflows/prebuild.yml:11-59`).
- **Cadence** [inspected]: 68 npm releases between 2025-10-28 and 2026-10-14; 101 merged PRs in 12 months; last commit 2026-10-14.
- **Bus factor**: about 2. Two people wrote 84 percent of last year's commits.
- **Issue response** [inspected, sampled]: only 8 issues were opened in the year, against 101 merged PRs. #892 got a contributor reply in about 3.5 h. #739 got a reply from mafintosh the next day. #893, #891, #890, #850 (3 months) and #754 (10 months, "add d.ts") have no reply. Work happens through PRs; outside reports are often left unanswered.
- **Security posture** [inspected]: no SECURITY.md (community profile `security: null`) and no disclosure process. GitHub advisories are empty for hypercore, hypercore-storage, rocksdb-native, sodium-native and @hyperswarm/secret-stream. No third-party audit was found. A CI canary job posts to a private repo on tags (`test-node.yml:31-42`); this is CI only, not runtime.
- **Documentation**: the API reference in the README is complete. Architecture docs are stale (section 1). There are no TypeScript types: issue #754 is open and `@types/hypercore` returns 404.

Counterexample row (s2-br-c, against hypercore) [answered]:
1. "Owner key can rewrite history via truncate; only a replica or witness that remembers the prior head defends": **confirmed**, and worse than stated for a local ledger. `truncate` needs only the key (`index.js:1137-1143`). By default the secret key is stored in the same RocksDB as the data: it is generated in `lib/core.js:204`, persisted through `createCore({ keyPair })` at `:238-246`, and lives in the schema field `keyPair.secretKey` (`hypercore-storage/encoding/spec/hyperschema/schema.json:300-316`). So anyone who can write the store, such as a same-user process (V2) or a delegated child with filesystem reach (V3), can also re-sign a rewritten history. The built-in defence is equivocation detection (`lib/core.js:640-701`). It only fires through replication, and its only test is skipped.
2. "#893 and #891 show replication is where bugs are": **confirmed** that both are open and both concern replication or peer state. **Out of scope** for a local-only ledger that never calls `replicate()`. #892 (SessionState flush) is open and sits on the local storage path. It is relevant but has not been reproduced here.
3. "Most dependency weight unused locally": **confirmed**. `index.js:7-8` loads secret-stream and Protomux unconditionally, and `lib/core.js:27` always builds a `Replicator`. No socket is opened unless the caller pipes `replicate()` (no `net`, `dgram`, `http` or `fetch` anywhere in `index.js` or `lib/`) [inspected]. The code is still loaded and cannot be dropped without forking.

## 4. Architecture

Control flow for our use: `new Hypercore(dir)` → `Hypercore.defaultStorage` → `new CoreStorage(dir)` (`index.js:208-213`). That constructor runs four steps (`hypercore-storage/index.js:492-545`):
1. `tmpFixStorage(dir)` (:505-506, :1342-1373) **moves every file in `dir` that it does not recognise into `dir/db/`** when no `CORESTORE` file exists.
2. Takes an exclusive `CORESTORE` device-file lock (:516-524).
3. Opens RocksDB at `dir/db` (:526-536).
4. `Core._tryOpen` loads auth (key, manifest, keyPair), head (fork, length, rootHash, signature) and roots (`lib/core.js:165-366`).

`append` hashes leaves, updates roots, signs the new head with the manifest signer and flushes a RocksDB write batch (`hypercore-storage/lib/view.js:322-336`). `get(i)` returns the stored bytes **without re-hashing them against the tree** (`index.js:962-965`). Verification happens only for data arriving by proof or replication (`lib/core.js:487-515`, `:792-798`).

- **Storage on disk** [inspected]: `CORESTORE` lock file plus `db/` (RocksDB SST, WAL `.log`, MANIFEST, OPTIONS). Keys use `index-encoder`; values use hyperschema compact-encoding (`hypercore-storage/lib/keys.js`, `encoding/spec/hyperschema/schema.json`). **Not readable without the library.** A user would need a RocksDB reader plus the hyperschema decoders. `CorestoreStorage.export` (`hypercore-storage/index.js:449`) returns internal block, tree and bitfield arrays, not a user-facing format.
- **Crash path** [inspected]: on a "sequence number is being set backwards" RocksDB error the store writes `RECOVERING` and **deletes every WAL `.log` file** (`hypercore-storage/index.js:650-656`). Recent unflushed writes are then lost by design. The trigger is only that error message (`shouldRecover`, `hypercore-storage/index.js:1408-1409`) or the `alwaysRecover` option. Ordinary writes are **not fsynced** [inspected, amendment 2026-10-21]: librocksdb's batch write builds a default-constructed `WriteOptions options;` and calls `db->Write(options, &batch)` (`librocksdb/src/rocksdb.cc:2256-2258` at 7b5352d), and the caller's write options are copied into the request (`:2279-2281`) but never reach that `WriteOptions`. RocksDB's default is `sync = false` [reported, RocksDB documentation]. A write survives a process crash (it is in the WAL) but can be lost on power loss or OS crash.
- **Identity**: a core is identified by `key` = hash of the manifest (or the signer public key in compat mode). Only Ed25519 signers exist.
- **Process model**: embedded in the caller's process. One process at a time per store because of the device-file lock.
- **Lifecycle**: `ready()` / `close()`. PR #787 ("Fix flush to wrong parent test on Windows") only adds `await a.close(); await b.close()` to `test/atomic.js:477`: on Windows, an unclosed core keeps file handles that block cleanup [inspected, PR diff].

## 5. Direct relevance

R11 asks for an "append-only, hash-chained, user-readable, exportable [ledger with] inclusion proofs; verifiable by the bridge before privileged routes execute; local-only by default" (`stage1/gaps.md:77-81`).

| R11 element | Hypercore | Evidence |
|---|---|---|
| Append-only, hash-chained | Yes, with a Merkle tree rather than a linear chain; append-only modulo `truncate`, `clear`, `purge` and the sweep calls, which any key or store holder can run | [inspected] `index.js:932-960`, `:1127-1147` |
| Inclusion proofs | Yes (`proof`, `verifyFullyRemote`) | [inspected]; one positive test, no negative (tampered-proof) test found |
| User-readable | **No** (RocksDB binary) | [inspected] section 4 |
| Exportable | Only by writing our own exporter (read stream to JSONL plus signed checkpoints) | [hypothesis] |
| Verifiable before privileged routes | No approval semantics; supplies the primitives only | [inspected] |
| Local-only | Yes; no I/O unless `replicate()` is piped | [inspected] |

Alpha targets:
- OSC-47: no route requires an approval proof; the archive gate takes a self-declared actor string, `isHumanReviewActor` (`browser-first/host/archive-review-policy.mjs:18-36` at 578fbbc).
- OSC-20: the public-submit regression counts as a pass.
- ADR-022: the `Logs/audit-ledger.jsonl` target (interaction.md:16, :71).
- os-map section 13 ("No route requires an approval proof") and seam 3 ("a host-side approval ledger that privileged routes ... can require").
- Invariants I3 (OS→DAO data locally logged), I4 (human-only enforced at the bridge), I7 (third-party recomputable commitments) and I10 (independent audit trails).

Fit: I4 and seam 3 need approval semantics that hypercore lacks. I7 asks for third-party recomputability, which hypercore's undocumented-outside-code format makes harder than RFC 6962 or C2SP tlog-tiles. I3 and I10 are served by any local log.

Property check (threat-model **v0.2**, section 4, Approval and audit row; threats T1, T5, T19, T22; amended 2026-10-21):

| Property | Result | Evidence |
|---|---|---|
| Tamper evidence (a): against non-same-user corruption | **Designed, partly tested.** Forged signatures are refused: `test/manifest.js:1732` "manifest - invalid signature fails" (local append and truncate with a bogus signature throw, length stays 0) and `test/replicate.js:415` "invalid signature fails" (a replica rejects data whose signature fails, `INVALID_SIGNATURE`; the writer's verifier is mocked). Missing roots are detected structurally (`test/merkle-tree-recovery.js:244`, writes refused in repair mode). **At-rest tampering is not demonstrated**: no test edits a stored block or node and expects detection; `get` does not verify (`index.js:962-965`); open does not verify the head signature (`lib/core.js:293-299`); `lib/audit.js` is internal, untested, and **deletes** mismatching blocks or nodes and even the whole core when a root is missing (`audit.js:29-33`, `:59-64`, `:94-98`) unless `dryRun`. Detection is possible only by a caller that checks blocks and an inclusion proof against a checkpoint it holds itself (section 7 step 4a) | [inspected] |
| Tamper evidence (b): against a same-user attacker (V2, V3) | **Not met locally in any configuration; designed only through a replica, not demonstrated.** Locally the signing key is on the same machine and readable by the same user: in the store by default (`lib/core.js:204`, `:238-246`; `schema.json:300-316`), or in a same-user file if passed per append (`index.js:1156-1158`). The key holder can `truncate` and re-sign (`index.js:1137-1143`; counterexample s2-br-c, confirmed). The external-checkpoint mechanism hypercore has is a replica on another device or OS account that remembers the prior head and refuses or flags the fork (`lib/core.js:640-701`, `:920-930`; `allowFork: false`, `lib/replicator.js:2410`). Its only test, `test/conflicts.js:4`, has been skipped since 2025-02-24 | [inspected] |
| User-readable export | **Not demonstrated.** It would need a custom exporter plus an independent verifier (about 150 lines reimplementing `hypercore-crypto/index.js:82-124`, flat-tree indexing and `caps.treeSignable`) | [inspected] / [hypothesis] |
| Route refuses without an approval record | **Not demonstrated** (absent; out of the library's scope). Design in section 7 | — |
| Approval record cannot be created by the agent principal (v0.2) | **Not demonstrated** (absent). Hypercore has no principal model: whoever holds the signing key, or can write a store that holds it, can append any record. The design in section 7 (enrolment, human proof) is Resonant code | [inspected] |
| Human is shown the canonical action the record binds (v0.2) | **Not demonstrated** (absent; a UI property outside any log library). Section 7 step 2 | — |
| Component surface (v0.2 row, T3/T6; X-6) | **Partly.** No listener: no `net`, `dgram`, `http` or `fetch` in `index.js` or `lib/` (section 3). But five native add-ons run in the bridge process next to A1/A2 (section 3), and if the store sits where a delegated child can write (X-1), RocksDB parses child-controlled files inside that process [hypothesis]. Dependency provenance (npm attestations for the prebuilds) was not checked | [inspected] / [hypothesis] |

**Which tamper property the hypercore design meets (security review X-2).** As a local library, hypercore meets at most (a): its signed Merkle tree lets a verifier that holds a pinned checkpoint and the public key detect edits by someone who lacks the key, but the library itself does not run that check on local reads, and no test exercises it at rest. It does **not** meet (b) locally, and no local configuration can: against V2 and V3, who run as the same user, a key and a checkpoint on the same disk detect accidents, not tamper. Hypercore reaches (b) only with a replica on a second device or under a separate OS account, which is the "witness" role in section 6, and that path's test is skipped. The section 7 design and the first PR (section 12) therefore deliver (a) until the external checkpoint (step 5) and a bridge-only state location exist; under threat-model v0.2 Phase 1 needs (b) for anything that gates T1 or T22, so the first PR must not be described as closing them.

Threat closure: T1, T19 and T22 are not closed by hypercore alone; it is a substrate for the R11 ledger. T5 is partial: it gives an ordered, signed record of promotions but no human proof. T21 (security-state tamper) is not closed: the store, key and checkpoint are files the same user can rewrite.

## 6. Reuse decision

**Learn the pattern and reimplement** for the R11 local ledger. **Investigate further** for an optional cross-device witness and replication backend (R16).

Why it loses to the alternatives in section 12 for R11:
- R11's user-readable and third-party-recomputable constraints (I7) fail at the storage layer.
- The default key custody puts the signing key next to the data, so local tamper evidence depends on an external witness hypercore does not supply locally.
- The only equivocation test is skipped.
- 63 packages and five native add-ons buy a replication stack a local ledger does not use.
- The pieces R11 needs (signed checkpoints, Merkle inclusion proofs, an append-then-act gate) are small, standard and testable. Node 24's `node:crypto` already provides Ed25519 and SHA-256, so they need no dependencies.

Hypercore's real advantage is replication to a second device with equivocation detection. That is a witness, valuable later and optional.

Hard gates (`scoring/weights.json`):
- **G1 pass**: no cloud service or telemetry; no network I/O in `index.js` or `lib/` [inspected]. The only phone-home is the CI canary job.
- **G2 pass**: Windows, macOS and Linux CI legs green at 9c9cc3d (Windows: 432/432 on Node v24.21.0, which is the Alpha's pinned Node). Failures are visible: a lock conflict or rename error throws at open; nothing silently no-ops. Caveats are in section 8.
- **G3 pass**: MIT, with Apache-2.0 for 35 transitive packages (NOTICE files in `hypercore-storage` and `rocksdb-native`); legal-review items in section 9.
- **G4 N/A**: not a DAO component; no chain.
- **G5 pass as a component**: it holds no authority and touches no DAO state. It preserves human-only actions only if the approval proof comes from a human ceremony, not from the bridge's own key, and (amended 2026-10-21, S-holepunchto-hypercore-1 and -2) only if that ceremony is rendered by a component the agent cannot drive and its credential is enrolled out of band (section 7). Those conditions bind the Resonant layer, not the library, so the verdict is unchanged.

Review round (2026-10-21): the reuse decision and every hard gate are unchanged. The accepted objections (section 14) all concern the proposed Resonant layer in section 7, and they strengthen the case for keeping the R11 core small and owned.

## 7. Integration design

**Gate design** (the part no candidate implements). Hypercore would be the store; ResonantOS writes the semantics. Proposed files: `browser-first/host/approval-ledger.mjs` (interface plus backend) and `browser-first/host/approval-gate.mjs`. Flow:

1. **Challenge.** A privileged route declares `requiredApproval: "<kind>"` next to `requiredCapability`. Without an approval reference, the bridge answers 428 `APPROVAL_REQUIRED` with `{approvalId, route, actionDigest = SHA-256(canonical JSON body), expiresAt}`.
2. **Ceremony** (amended 2026-10-21, S-holepunchto-hypercore-1). The preview must **not** be rendered by the side panel: the agent loop runs in the side-panel page (`ext/src/side-panel.js:783-908`, os-map section 7), so a prompt-injected or compromised panel could show action B while submitting the digest of action A. A WebAuthn assertion proves that a human touched an authenticator during this challenge; the authenticator shows nothing about the action. The ceremony component therefore (i) receives the canonical body from the bridge, not from the agent, (ii) renders it and computes `actionDigest` from what it rendered, and (iii) itself requests the human proof over `H(approvalId ‖ actionDigest)`. Candidates, in order of preference: a host-native prompt run by a bridge helper process (Windows Hello / macOS LocalAuthentication / polkit) [hypothesis: helper availability per OS to be checked]; or a separate extension page with no agent code and a CSP that loads only the ceremony script, opened by the bridge, posting to `POST /api/approvals/:id` [hypothesis: WebAuthn availability in MV3 extension pages must be checked]. The agent principal never holds the grant for that route. Which component this is, is the Gate 3 decision on X-4 (state.md D3.7).
3. **Record** (amended, S-holepunchto-hypercore-2). The bridge verifies the human proof against an **enrolled** credential and appends `{type:"approval", approvalId, route, actionDigest, principal, expiresAt, proof}` to the ledger core, getting index `i`. Enrolment: the first credential is registered in a first-run, out-of-band ceremony through the same agent-free component (never through a route the agent principal can reach); each later credential requires an assertion from an existing one; every enrolment and removal is itself an R11 record. Software and virtual authenticators (Chrome exposes them through the DevTools protocol to anything that can attach a debugger, which includes a V2 process) are refused where attestation allows it; where it does not, that is a residual risk to state [hypothesis: attestation support per authenticator not checked].
4. **Gate.** The agent retries with `X-Resonant-Approval: <i>`. Between `authorizeBridgeRoute` returning `{route}` and `route.handler(...)` (`browser-first/host/bridge-server.mjs:1251-1255`), `approval-gate.mjs`:
   - (a) reads block `i` and, **because local reads are unverified**, checks `crypto.data(block)` against tree node `2i` and an inclusion proof against a **pinned checkpoint**: `{key, length, fork, treeHash, signature}` kept in a file outside the RocksDB directory, with the public key pinned in bridge config rather than read from the store's auth record;
   - (b) checks route, digest, expiry and that the approval is not yet consumed (an index rebuilt from `consume` blocks);
   - (c) appends `{type:"consume", approvalId}`, **refusing if the append fails** (the CATP fail-closed pattern);
   - (d) runs the handler;
   - (e) appends `{type:"result"}`.
5. **Witness.** Each checkpoint (`core.signable()` plus signature) is also written to a location the bridge cannot rewrite unnoticed. Amended 2026-10-21 (X-2): the user export (`Logs/audit-ledger.jsonl` becomes this export view) and the extension's storage are on the same disk under the same user, so they help against accidents and non-same-user corruption only. Only a replica or checkpoint store on another device or under a separate OS account, for example a hypercore replica opened with `allowFork: false` (`lib/replicator.js:2410`) or a cosigning witness as in the Tessera dossier, gives property (b).

**Cost per call** [hypothesis, not measured]:
- Verification is one Ed25519 verify (about 50-100 µs, libsodium), about log2(n) BLAKE2b hashes (negligible) and about 20 RocksDB point reads, mostly from the tree cache.
- The consume append adds one Ed25519 sign and one RocksDB batch write.
- Proof size at n = 10^6 is about 20 nodes of roughly 40 bytes plus a 64-byte signature, under 1 KB.
- Expected total: about 0.2-2 ms per gated call, excluding the human ceremony and fsync policy.

**What the bridge-side check proves and what it does not** (amended, S-holepunchto-hypercore-3, X-2). The bridge is writer and verifier at once. Steps 4(a)-(c) protect against replay, missing records and at-rest edits by an attacker who can write the store but cannot also rewrite the pinned checkpoint and read the key: that is property (a) of section 5. They do not protect against a compromised bridge, and they do **not** protect against V2 or V3: a same-user process or a delegated child that can write `~/ResonantOS_User/...` (OSC-45; unconfined outside macOS, OSC-32) can rewrite the store, the checkpoint file and, with the key file, re-sign, so the local check detects accidents, not tamper. Property (b) needs step 5 with a witness outside the same-user reach. Human approval means something only because of the step-2 proof, which neither the bridge nor the agent can forge or frame if step 2 is built as amended.

**Key custody and checkpoint placement.** Create the core with the public key only (`opts.key` without `opts.keyPair`, so `lib/core.js:204` yields `keyPair = null` and nothing secret is persisted) and pass `keyPair` per append (`index.js:1156-1158`). The Alpha has no vault (R15, ADR-022 deferred), so on Windows the key would still sit in a same-user-readable file. The signing key, the pinned checkpoint and the store belong in the one bridge-only, integrity-protected state location that the lead has deferred to Gate 3 (X-1, state.md D3.7), not in `Logs/` or anywhere under the child-writable user state root. Until that location exists, record the residual risk: the ledger is tamper-evident only against non-same-user corruption.

**Storage path.** Use a dedicated empty directory such as `~/ResonantOS_User/Logs/ledger-core/`. **Never** point it at `Logs/`, because `tmpFixStorage` would move `audit-ledger.jsonl` and any other file into `Logs/db/` (`hypercore-storage/index.js:1342-1373`).

**Public submit caveat.** Public submit executes in the content script (`ext/src/content.js`, OSC-20), not in a host route. A bridge gate covers it only once R19 makes the extension obtain a bridge-issued execution ticket. Host routes that can be gated immediately: archive promotion (archive-write), delegation start, credential writes.

**Alpha tests affected** (of the 2,424):
- `test/bridge-route-capability-audit.test.mjs`: locks the route-to-capability table. A new optional route field should not break it [hypothesis].
- `test/bridge-server.test.mjs`: the authorization tests at :108, :561 and :708 need new 428 cases.
- `test/archive-review-policy.test.mjs`: the three tests at :10, :18, :26 change when the actor string is replaced by an approval reference.
- `test/agent-control-public-submit.test.mjs`: 17 tests, unchanged until R19.

Versioning: pin `hypercore@11.39.0` and the lockfile. The README promises forward compatibility for storage and wire, but v11 already migrated storage once (`UPGRADE.md`).

## 8. Security and governance effects

- **New attack surface**: five native add-ons running in the bridge process, 63 packages to review, and a 184 MB prebuild package.
- **Store permissions**: the RocksDB directory is readable and writable by any same-user process. Windows has no 0600 equivalent in the Alpha (OSC-06). Under threat-model v0.2 this is asset A10 and threat T21: the store, key and checkpoint are security state and must live in the Gate 3 bridge-only location (X-1).
- **In-process parsers (X-6, v0.2 Component surface)**: the five native add-ons, RocksDB among them, run in the process that holds A1 and A2. For a local-only ledger they parse only the bridge's own files, unless a child can write the store, in which case RocksDB parses attacker-controlled SST and WAL files in that process [hypothesis]. If replication is ever enabled, the Noise and Protomux stack parses peer input in that process too. A separate ledger process would move this out [hypothesis, not designed here].
- **Write durability**: batch writes are not fsynced (`librocksdb/src/rocksdb.cc:2256-2258`, section 4), so an approval acknowledged before a power loss can disappear. For a fail-closed gate this is safe (missing means refused), but a consumed approval could also vanish and become re-usable unless the gate fsyncs, or calls RocksDB flush, before running the handler [hypothesis; acceptance case 7].
- **Key custody**: by default the signing key lives in the store (section 3), so V2 and V3 can forge a coherent rewritten history. Detection then depends entirely on externally held checkpoints.
- **Evidence destruction**: `audit()` deletes rather than reports. `clear`, `purge` and `sweep` delete content. The ledger wrapper must not expose these, and should call `audit` only with `dryRun: true`.
- **Crash loss**: WAL deletion on recovery (`hypercore-storage/index.js:650-656`) can drop the last approvals. For a fail-closed gate that is safe (an approval missing means refused), but it is a loss of audit trail.
- **Revocation**: append a revocation or `consume` block. The ledger itself is never edited.
- **Isolation**: in-process; a crash in a native add-on takes down the bridge [hypothesis].
- **Personal data**: approval records hold action digests and principal ids. Store full bodies only if the user opts in (I3).
- **Trust in maintainers**: Holepunch, a commercial company. No SECURITY.md, so the disclosure path is unknown.
- **Friction**: one ceremony per privileged action, the same as R19's.
- **Replication** (not recommended for the R11 core): uses Noise-encrypted streams; equivocation detection works only there.
- **Windows caveats**: tests had to close cores explicitly (PR #787), so file-handle locks matter during bridge restart. A second bridge instance fails to take the device-file lock, which is a visible error. Antivirus interaction with RocksDB files is unknown.

## 9. Licensing

| Component | SPDX | Note |
|---|---|---|
| hypercore | MIT | `LICENSE`, matches manifest |
| hypercore-storage, rocksdb-native, secret-stream, device-file, fs-native-extensions and 30 others | Apache-2.0 | NOTICE files must travel with redistribution (Apache-2.0 §4(d)) |
| sodium-native / sodium-universal, hypercore-crypto | MIT | the prebuilt binaries contain libsodium (ISC) |
| quickbit-universal, simdle-universal, nanoassert, noise-curve-ed | ISC | |
| RocksDB inside rocksdb-native prebuilds | upstream dual GPL-2.0 / Apache-2.0 | used under the Apache option [hypothesis]. The `holepunchto/librocksdb` wrapper's own `LICENSE` at 7b5352d is Apache-2.0 and it has a `NOTICE` file [inspected via gh api, 2026-10-21]; the election for the vendored RocksDB sources was not read |

Compatibility with the MIT Alpha: high confidence for permissive use. The proposed Symbiotic Licence is status F, so unknown. Items for legal review:
1. Which NOTICE texts must ship with a bundled bridge build.
2. The RocksDB licence election inside the prebuilt binaries.
3. Third-party notices for libsodium in the binaries.

This is technical research, not legal advice.

## 10. Cost and effort

Skills: Node and JavaScript (no language cost), crypto review, and Windows file-lock debugging. Hypercore has no types, so the Alpha's TypeScript side would need hand-written `.d.ts` files.

| Scenario | Scope | Estimate (one experienced developer) | Assumptions |
|---|---|---|---|
| Small (recommended first) | Gate plus JSONL hash chain with Ed25519 checkpoints (node:crypto), no hypercore; one host route gated | 1-2 weeks | existing route table; ceremony via a side-panel button first, WebAuthn later |
| Medium | Hypercore backend behind the same interface, exporter, independent verifier, witness checkpoints, key outside the store | 3-5 weeks | prebuilds work on the target machines; no fork needed |
| Large | Cross-device witness via replication, OS keystore custody, WebAuthn ceremony, R19 execution tickets for public submit | 2-3 months | R15 vault and R19 land in parallel |

Maintenance exposure: high release churn (68 per year) and a storage migration already happened in v11, so pins and migration tests are needed. Lock-in: data sits in a Holepunch-specific format. Replacement cost is low only if the JSONL export is the source of truth.

## 11. Acceptance test (request for the user; executes third-party code)

The harness is a Node 24 script in the inspector's scratchpad, run against `hypercore@11.39.0` installed with `--ignore-scripts` in a disposable VM on Windows 11 x64, macOS and Linux. Inputs: 1,000 approval and consume records.

Fault scenarios:
1. Flip a byte of a stored block through the storage write API (as `test/merkle-tree-recovery.js:21-26` does for nodes). Expected: the gate refuses the referenced approval with `LEDGER_TAMPERED`, and `audit({dryRun:true})` reports `droppedBlocks ≥ 1`.
2. Copy the stored key, `truncate` and re-append different history (counterexample). Expected: the pinned-checkpoint check fails, and a replica with `allowFork:false` emits `conflict` or refuses.
3. T1: a simulated injected page makes the agent call a gated route with no approval. Expected: 428, and no handler side effect.
   - 3b (added 2026-10-21, S-holepunchto-hypercore-1, T22): the injected agent requests approval for action A while the side panel displays action B. Expected: the ceremony component shows A (rendered from the bridge's canonical body), and a proof given while the human saw B does not verify for A.
   - 3c (S-holepunchto-hypercore-2): the agent principal calls the credential-enrolment path, and separately a virtual authenticator is attached through the DevTools protocol. Expected: enrolment refused, no R11 enrolment record created; the virtual authenticator's assertion is refused or flagged.
   - 3d (S-holepunchto-hypercore-3, T21): a delegated child with `archive-write` rewrites the store, the pinned checkpoint and re-signs with the key file. Expected with the first PR (property (a) only): **not detected**, which the run records as the stated limit. Expected once step 5 has an off-device witness: detected at the next witness comparison.
4. Replay a consumed approval. Expected: refused.
5. Make the ledger directory read-only so append fails. Expected: route refused (fail-closed).
6. Export to JSONL and verify with an independent verifier that does not import hypercore. Expected: all checkpoints and inclusion proofs verify.
7. Windows only: kill the bridge mid-append and restart. Expected: the store opens, nothing is duplicated, any missing record is refused rather than accepted. Add a power-loss variant (VM hard reset after a `consume` is acknowledged): expected, the consumed approval is still recorded, or the handler never ran (writes are not fsynced by default, section 4).

Pass criterion: every expected outcome, on all three OSes. CI hook: a new lane `test:approval-ledger` in `scripts/verify-alpha.mjs`.

## 12. Recommendation and confidence

Benefits: a mature, MIT, Node-native signed Merkle log; green Windows CI on the exact Node the Alpha pins; inclusion proofs; multi-signer manifests; a path to cross-device witnessing.

Trade-offs: binary storage, the key stored with the data, unverified local reads, a destructive audit, a skipped equivocation test, a heavy native footprint, no types, and sparse issue response.

Blockers for R11: user-readability and I7 recomputability.

Readiness: B for the log; D for approval semantics, which nobody has.

Evidence quality: about 85 percent [inspected], the rest [reported] (CI log, issue text) or [hypothesis] (costs, WebAuthn, the ceremony component). The fsync behaviour was inspected in the 2026-10-21 amendment (section 4).

| Criterion | Hypercore | Tessera (Go) | CATP (TS) | AuditKit (TS) | EUDI registrar (TS) |
|---|---|---|---|---|---|
| Embed in Node 24 | in-process lib | Go sidecar or CLI | in-process | in-process core, server-shaped | verifier file only |
| Windows | CI green | POSIX driver uses `syscall.Flock` (`storage/posix/files.go:224,233` at 012e9e0, no build tags), so it does not build | Node, likely [reported] | unknown, no CI | n/a |
| On-disk format readable without the lib | no (RocksDB) | yes (C2SP tlog-tiles static files) | yes (`actions.jsonl`, fsync) | SQLite | Postgres |
| Inclusion / consistency proofs | yes / via upgrade proofs | yes / yes | Merkle-root export only | RFC 6962 + anchors | RFC 6962 verifier (`apps/transparency-watch/src/app/merkle.ts`) |
| Tamper test named | signature only; at-rest none | `files_test.go` [reported by parallel inspector] | `verifier.test.ts` "detects a tampered commitment (index 1)" and others | `core.test.ts` "detects an edited field", "detects a truncated tail when the expected head is known" | none (verifier untested) |
| Refuses action without a record | no | no | fail-closed on own append (`pre.test.ts` "fails closed when the audit log append cannot be persisted"); no human-approval test | no | no |
| Licence | MIT (+Apache deps) | Apache-2.0 | MIT | AGPL-3.0 (reference only, G3) | Apache-2.0, prototype |
| Maturity | 10 years, 68 releases/yr | production (Rekor v2, CT) | 1 maintainer, 0.x | 1 maintainer, alpha | "Do not use in production" |

Conclusion: for R11 the smallest custom layer is CATP's append-then-act JSONL chain, plus RFC 6962-style signed checkpoints and inclusion proofs (the registrar's `merkle.ts` pattern, Tessera's checkpoint and witness model), plus a human-proof field. Hypercore is held in reserve as the replication witness.

**First PR** (ResonantOS Alpha):
- Add `browser-first/host/approval-ledger.mjs`: append, `verifyInclusion`, checkpoint and `exportJsonl` over `~/ResonantOS_User/Logs/audit-ledger.jsonl`, using node:crypto SHA-256 and Ed25519 only.
- Add `browser-first/host/approval-gate.mjs`.
- Add a `requiredApproval` check at `browser-first/host/bridge-server.mjs:1251-1255`, applied to one archive-promotion route, off by default behind a setting.
- Replace the self-declared actor in `archive-review-policy.mjs:27-36` with an approval reference.
- Tests: `browser-first/test/approval-ledger.test.mjs` (byte-flip, truncation against a pinned checkpoint, replay, append failure → refuse); amend `archive-review-policy.test.mjs`.
- Attacker model, stated in the PR description (amended 2026-10-21, S-holepunchto-hypercore-3, X-2): the PR delivers tamper evidence (a), against non-same-user corruption and accidents, and does not claim (b). The ledger path above is a placeholder: the ledger, pinned checkpoint and signing key move to the Gate 3 bridge-only state location (X-1) when it exists, and the gated route stays off by default until the approval ceremony is rendered by an agent-free component (X-4). The PR must not be described as closing T1 or T22.

**Confidence: medium.** The code facts are inspected. The per-call cost, the agent-free ceremony component and WebAuthn in MV3 are unexecuted hypotheses. The lack of fsync is inspected but not executed.

## 13. Scores (profile: os_kernel)

| Criterion | Score | Reason (anchor) |
|---|---|---|
| requirement_fit | 2 | signed Merkle log with inclusion proofs, but fails user-readable and exportable, has no approval semantics, and local reads are unverified |
| demonstrated_maturity | 4 | releases, 3-OS CI, 432 tests, reported production use (Keet); issue response is thin |
| isolation_and_security | 2 (unchanged; re-checked 2026-10-21 against anchor clauses (a)-(d), D3.7 and D3.8, and threat-model v0.2) | (a) No advisory. The confirmed counterexample (key holder truncates and re-signs; key in the store by default) does not defeat a checked property **as the dossier configures hypercore**: the core is opened with the public key only, `audit` only with `dryRun`, and the threat model itself says (b) needs an external checkpoint, which is exactly the replica path the counterexample names. So 0 does not apply. (b) 3 needs a test of the property itself: forgery rejection is tested (`manifest.js:1732`, `replicate.js:415`), but at-rest tamper detection (a) has no test, and the only test of the replica path that gives (b), `conflicts.js:4`, has been skipped since 2025-02-24. So 3 is not reached. (c) This rates hypercore 11.39.0 as inspected, not the section 7 layer (X-3: rankings are library-only). (d) Route refusal, agent-cannot-mint, canonical display and user-readable export are absent mechanisms (at most 1 each), already charged under requirement_fit. Above 1 because the tamper mechanism is implemented and its verification path is tested |
| licence_suitability | 5 | MIT, Apache-2.0 and ISC file-level throughout; NOTICE duties noted |
| integration_effort | 4 | embeddable Node library, but no typed API (#754) |
| maintenance_sustainability | 3 | company-backed with high cadence, but bus factor about 2, no SECURITY.md, most outside issues unanswered |
| sovereignty_and_portability | 3 | local-first, no account, but data is not user-readable (RocksDB plus hyperschema) |
| interoperability | 2 | Holepunch-specific tree, signing and storage formats; no RFC 6962 or C2SP compatibility |
| operational_complexity | 4 | one process, embedded DB, but five native add-ons, a 184 MB prebuild package and a single-opener file lock |

Weighted total (os_kernel): 3.04 of 5, for information only; the decision rests on section 6. Recomputed 2026-10-21 with the `os_kernel` weights in `scoring/weights.json`: 0.18x2 + 0.14x4 + 0.22x2 + 0.10x5 + 0.08x4 + 0.10x3 + 0.08x3 + 0.04x2 + 0.06x4 = 3.04 (no score changed in the review round). The total is library-only (X-3, D3.7(c)). Lead ruling D3.12: the default key-in-store is not contrary evidence under clause (d), so the total stands.

## 14. Open questions for the adversarial reviewers

1. **Write durability**: whether rocksdb-native writes use `sync=true` (the WriteOptions live in `holepunchto/librocksdb`, not cloned). This decides whether a confirmed approval can vanish after a power loss. **Answered 2026-10-21**: they do not; `librocksdb/src/rocksdb.cc:2256-2258` at 7b5352d writes with default `WriteOptions` (section 4). Not executed; the power-loss variant of acceptance case 7 would confirm it.
2. **WebAuthn in MV3**: whether WebAuthn with user verification is usable from a Chrome MV3 side panel with an extension-scoped RP ID. If not, the ceremony needs a host-native prompt (Windows Hello via a helper).
3. **Unmeasured items**: the per-call cost (section 7), Windows ARM64 runtime behaviour (a prebuild exists; CI is x64 only), and antivirus interaction with RocksDB.
4. **Production claims**: Keet and Pear production use is [reported] only.
5. **Possible optimism in the README**: "Secure. Uses signed merkle trees to verify log integrity in real time" (README:14) holds for data received from peers, not for the local store (`index.js:962-965`). "Simple flat file structure" and "latest release is Hypercore 10" are stale.
6. **Threat-model challenge**: the rejection of hypercore for R11 rests on the user-readability constraint and on I7. If reviewers judge a verified JSONL export sufficient, the decision could move to "wrap" with the medium scenario. The key-custody and skipped-equivocation-test findings stand either way.
7. **The skipped equivocation test**: `test/conflicts.js:4` is skipped as flaky (~1/100). Its history (last touched 252c7c1, 2025-08-28) was not traced further. **Traced 2026-10-21**: 252c7c1 is only the shallow-clone boundary. The upstream history (`gh api repos/holepunchto/hypercore/commits?path=test/conflicts.js&sha=9c9cc3d...`) shows it skipped by #645 "Skip flaky fork test" (0d28e9d, 2025-02-24) and touched once since, by #677 "fix false positive in conflict detection" (7428fff, 2025-03-13), which left the skip in place.

### Review responses (2026-10-21)

Amender s3-amend-hypercore, standing in for s3-insp-hypercore. Every objection was checked against the clones at the recorded SHAs (main clone 9c9cc3d; companions re-cloned as in the header) or the cited Alpha files. The DAO skeptic's section for this dossier records no objection.

| Id | Verdict | Change made (section) or evidence for dispute |
|---|---|---|
| S-holepunchto-hypercore-1 | accepted | The agent loop runs in the side-panel page (`ext/src/side-panel.js:783-908`, os-map section 7), so the old step 2 put the preview in the agent's own context. Step 2 rewritten: the ceremony component receives the canonical body from the bridge, renders it, computes the digest itself and requests the proof; host-native prompt preferred, else an agent-free extension page (section 7). Fault case 3b added (section 11). G5 condition reworded (section 6) |
| S-holepunchto-hypercore-2 | accepted | Enrolment was unspecified. Step 3 now requires first-run out-of-band enrolment through the agent-free component, later additions authorised by an existing credential, every enrolment recorded in R11, and refusal of virtual authenticators where attestation allows (section 7). Fault case 3c added (section 11) |
| S-holepunchto-hypercore-3 | accepted | The attacker model is now stated: the design and first PR give tamper evidence (a) only. Key, checkpoint and store are moved out of `Logs/` to the Gate 3 bridge-only location, and the first PR carries the statement (sections 5, 7, 12). Fault case 3d records the limit (section 11) |
| S-holepunchto-hypercore-4 | accepted (agreement) | Score 2 kept and re-checked against the clarified anchor (section 13) |
| A-holepunchto-hypercore-1 | accepted | Companions re-cloned read-only under `research\_untrusted\hypercore-storage\`, `hypercore-crypto\`, `rocksdb-native\` with full SHAs (header). Re-verified at those SHAs: `hypercore-storage/index.js:492-545` (constructor; `tmpFixStorage` call :506, lock :516-524, RocksDB :526-536), `:650-656`, `:1342-1373`, `:449`; `lib/view.js:322-336`; `encoding/spec/hyperschema/schema.json:300-316`; `hypercore-crypto/index.js:82-124`; `rocksdb-native/CMakeLists.txt:12`; `prebuild.yml:11-59`; LICENSE and NOTICE files. All PASS, with no line drift |
| X-1 (security, cross-cutting) | accepted | Store, key and checkpoint are security state (A10, T21). They move to the bridge-only location that the lead deferred to Gate 3 (state.md D3.7). Until then the residual risk is stated (sections 7, 8, 12) |
| X-2 (security, cross-cutting) | accepted | Section 5 now says which tamper property hypercore meets: (a) at most, designed and partly tested; (b) not locally in any configuration, only through an off-device or separate-account replica whose test is skipped. Property table split per threat-model v0.2; step 5 witness options corrected (section 7) |
| X-3 (security, cross-cutting) | accepted (lead settled) | D3.7(c): the score rates hypercore as inspected and the ranking is library-only. Section 13 says so; scoring the proposed layer separately is a Gate 3 item |
| X-4 (security, cross-cutting) | accepted | Same changes as S-holepunchto-hypercore-1 and -2; the choice of agent-free component is deferred to Gate 3 (section 7 step 2) |
| X-6 (security, cross-cutting) | partly accepted | The surface is real: five native add-ons in the bridge process (section 3), now in a Component surface row (section 5) and section 8. Not accepted for the local-only use: hypercore adds no listener (no `net`, `dgram`, `http` or `fetch` in `index.js` or `lib/`). No score change, because W-5 (a surface criterion) was not applied (D3.7) |
| Archaeologist cross-cutting 5 | no objection | It records that this dossier disclosed its skipped test. Nothing to change; the skip's history is now traced (q7) |
| Archaeologist cross-cutting 6 | accepted | STATUS line with `verified: 9c9cc3d 2026-10-21` added (header) |
| Archaeologist cross-cutting 7 | accepted | Same fix as A-holepunchto-hypercore-1 (header) |
| DAO skeptic C-8 | accepted | Same fix as archaeologist cross-cutting 6 (header) |
| Lead ruling D3.12 (on the contested clause (d) question) | settled by lead | The default key-in-store is not contrary evidence under clause (d). It is the reason tamper property (b) is unmet (section 5), and the same local-key pattern in every R11 design is scored as the absence of an external checkpoint. Isolation 2 and total 3.04 stand (section 13) |

Other changes in this round, from re-reading the code rather than from an objection:
- Repair mode is a structural check (missing roots), and open does not verify the head signature (section 2).
- Writes are not fsynced (librocksdb, section 4; q1 answered; section 8; acceptance case 7).
- The skip history is traced (section 2, q7).
- Counts re-run: 166 commits in 12 months (`git log --since=2025-10-20 --until=2026-10-20 --format=%an 9c9cc3d | sort | uniq -c`: 91, 48, 12, others 15) and 8 `test.skip` (section 2). Both reproduce.

Scores: none changed. isolation_and_security stays 2, and the weighted total stays 3.04 (os_kernel).

Formerly contested: whether hypercore's default key-in-store counts under clause (d) as contrary evidence "in the artifact as proposed for use". Settled by the lead in state.md D3.12: it does not count, so isolation 2 and total 3.04 stand.
