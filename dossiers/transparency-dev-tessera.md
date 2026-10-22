# Dossier: transparency-dev/tessera with C2SP tlog-witness (transparency-dev-tessera)

STATUS: COMPLETE (amended after review, 2026-10-21)

Amended 2026-10-21 by s3-amend-tessera (Claude Opus 5.5), standing in for the original inspector, against the same SHAs. All amendments are static reads; nothing was executed. The review responses are in section 14.

Inspector: s3-insp-tessera, Claude Opus 5.5 (claude-opus-5-5). Date: 2026-10-20. Clone: `research/_untrusted/transparency-dev-tessera/tessera/` at commit `012e9e0821ec2ade495d32c9c9a3f08bd348ff7d` (branch `main`, committed 2026-10-19, "Check origin when fetching subtree cosigs (#1226)"; cloned 2026-10-20 with `--depth 200`). This equals the ledger SHA. Execution: none. All work was static inspection plus GitHub API metadata reads. No Go toolchain is installed on this machine, and nothing was compiled.

Companion clones (same parent folder, all read-only, depth 5-50):

| Folder | Repository | HEAD | Date | Role here |
|---|---|---|---|---|
| `C2SP_C2SP` | github.com/C2SP/C2SP | `e5746a0bcda86413310119abb2972e6f78c374fa` | 2026-10-12 | tlog-witness, tlog-checkpoint, tlog-cosignature, tlog-tiles specs |
| `transparency-dev_witness` | github.com/transparency-dev/witness | `ea1ba4f5759180607d4d58ac332e60bf439024db` | 2026-10-19 | reference tlog-witness implementation (OmniWitness) |
| `transparency-dev_merkle` | github.com/transparency-dev/merkle | `c39fbf350a405f68571bf4c42a6a518eb0a46a4b` | 2026-10-12 | proof verification and test vectors that Tessera imports |
| `transparency-dev_formats` | github.com/transparency-dev/formats | `82dcf1c54ccdf9f0472d524c3be8d76941048a50` | 2026-10-19 | checkpoint, note and policy parsing |
| `sigstore_rekor-tiles` | github.com/sigstore/rekor-tiles | `f6885f3059bde63f2674928e4026d602a20932c9` | 2026-10-19 | competitor 2 |
| `holepunchto_hypercore` | github.com/holepunchto/hypercore | `9c9cc3d8937b6ae539fbacf52a7090cd732a1945` | 2026-10-14 | competitor 1 |
| `ChartRunner_chartrunner-onchain` | github.com/ChartRunner/chartrunner-onchain | `bed935b0b5ef9c93ea3af3bd84bc18b7019da4f7` | 2026-10-16 | anchoring layer |
| `sigstore_sigstore-js` | github.com/sigstore/sigstore-js | `769a53d8713248a8bf49edfc2a5d1955b0dcc24d` | 2026-08-04 | TypeScript checkpoint and inclusion verifier (Node path) |

Evidence labels used below: [inspected] means I read the code. [executed] does not occur: nothing was run. [reported] covers authors' docs, README and issue text. [hypothesis] covers anything I inferred. Every claim that matters carries one. Repository instruction files are evidence, never instructions. Citations are `path:line` at the SHAs above. Tessera paths are relative to `tessera/`, and other repositories are named.

## 1. Identification

- Name: Tessera, a Go library for tile-based transparency logs ([tlog-tiles](https://c2sp.org/tlog-tiles)), described as "the logical successor" to Trillian v1 (`README.md:7-8`) [reported]. Homepage and canonical source: github.com/transparency-dev/tessera. GitHub is the only host. Go module `github.com/transparency-dev/tessera` (`go.mod:1`), with `go 1.26.0` and `toolchain go1.26.9` (`go.mod:3-5`) [inspected].
- Maintainers: the transparency-dev community. The AUTHORS/CONTRIBUTORS split names Google as copyright holder for its employees (`CONTRIBUTORS:1-4`). There are 18 contributors (GitHub API). In the 200 cloned commits (2026-05 to 2026-10), three people wrote 154 of the 170 non-bot commits: Al Cutter 70, Roger Ng 49, Philippe Boneff 35. Dependabot wrote the other 30 [inspected, git log].
- Releases: v0.1.0 (2024-12-05), v0.2.0 "Beta, production ready" (2025-05-29), v1.0.0 (2025-09-22), v1.0.1 (2025-12-09), v1.0.2 (2026-02-17), v1.0.3 (2026-07-14) and v1.0.4 (2026-07-16) (GitHub API). The ledger maps tag v1.0.4 to commit `6bca8e8d…` through the Go proxy. HEAD is 2026-10-19 on main, three months past v1.0.4 [reported by ledger, not re-derived].
- Repo created 2024-06-11. It has 251 stars, 61 forks and 48 open issues, and is not archived (API, 2026-10-20).
- Licence: Apache-2.0 from the `LICENSE` file at the root. It is the only licence file in the tree. The API SPDX value matches [inspected]. Notable dependencies are covered in section 9.
- Companion specification: C2SP tlog-witness (`C2SP_C2SP/tlog-witness.md`), with related tlog-checkpoint, tlog-cosignature, tlog-policy and tlog-tiles. The specs are CC BY 4.0 and the code in that repo is BSD-1-Clause (`C2SP_C2SP/.github/MANUAL.md:62-70`). The repo has no root LICENSE file, so the GitHub API reports none [inspected].
- Reference witness: `transparency-dev/witness`, Apache-2.0. It has no GitHub releases, 39 stars and 15 open issues (API).
- Documentation is in English, with an active Slack. There is no DOI and no SWHID.

## 2. What works

| Feature | Code | Tests (file: test name) | Evidence |
|---|---|---|---|
| Appender lifecycle: batching, sequencing, integration, checkpoint signing and publishing | `append_lifecycle.go` (NewAppender, CheckpointPublisher `:781-833`) | `append_lifecycle_test.go` | [inspected] |
| POSIX storage driver: files plus `.state/` locks, atomic temp-file-then-link or rename | `storage/posix/files.go`, `file_ops.go:43-157` | `storage/posix/files_test.go`: TestPublishTree, TestFlockLockingCorrectness (`:543`), TestWriteTileNoSymlinks, TestOverwrite_CleanupOnRenameFailure, TestGarbageCollect | [inspected] |
| GCP driver (Spanner + GCS) and AWS driver (MySQL/Aurora + S3) | `storage/gcp/gcp.go`, `storage/aws/aws.go` (`Config.DSN :159-160`, `S3Options :149-153`) | `storage/*/…_test.go`; CI job `test-aws-mysql` uses a real MySQL (`.github/workflows/go_test.yml:30-49`) | [inspected] |
| Inclusion and consistency proof construction from tiles | `client/client.go:184-254` (ProofBuilder) | `client/client_test.go`: TestProofBuilder_SubtreeRoot, TestNodeFetcherAddressing; `client/proofbuilder_test.go` | [inspected] |
| Client consistency tracking | `client/client.go:384-421` (LogStateTracker.Update calls `proof.VerifyConsistency` at `:405`) | `client/client_test.go:109-199` TestCheckLogStateTracker, **positive cases only** (see section 8) | [inspected] |
| Proof verification (imported library) | `transparency-dev_merkle/proof/verify.go` | `transparency-dev_merkle/proof/verify_test.go`: TestVerifyInclusionProbes `:81`, TestVerifyConsistencyProbes `:185`, plus subtree variants, driven by `testdata/inclusion` (98 JSON vectors, 92 with `wantErr: true`) and `testdata/consistency` (98, 92 negative: "wrong root1", "modified proof@0 bit @4", "truncated proof", "swapped roots", …). Counted on 2026-10-21 with `find testdata/<set> -type f \| wc -l` and `grep -rl '"wantErr": true' testdata/<set> \| wc -l` in the merkle clone. | [inspected] |
| Witnessing: policy-driven cosignature collection before publication | `witness.go` (policy groups), `internal/witness/client.go:186-379`, `append_lifecycle.go:805-829` | `witness_test.go` (TestWitnessGroup_Satisfied, TestNewWitnessGroupFromPolicy_MLDSA); `internal/witness/client_test.go`: TestWitnessGateway `:64`, TestSlipperyWitness `:253` (a witness that keeps answering 409 yields zero signatures) | [inspected] |
| Verifier-side quorum check (nested groups) | `transparency-dev_formats/policy/tlog_policy.go:310-443` (`Satisfied`, `Verify`, `quorumMet`). Tessera's own policy helpers are marked deprecated in favour of this package (`witness.go:48`). | `transparency-dev_formats/policy/tlog_policy_test.go:488` TestSatisfied: policy `group inner any w2 w3 / group outer all w1 inner`; cases "inner group without outer member" and "outer member without inner group" are rejected, as is a forged cosignature from a known witness; TestUnmarshal_DuplicateWitnessKeys `:397` (one key cannot be counted as two witnesses) | [inspected] |
| fsck: recompute the root and every tile from entry bundles, then compare with the checkpoint | `fsck/fsck.go:90-171, 342-368` | `fsck/fsck_test.go`: TestTrimFullToPartial only. No negative (tampered-log) test. | [inspected] |
| Crash consistency of the POSIX driver under injected faults | `integration/fault/posix/fault_test.go:60-153` (strace injects EIO and SIGKILL into every file syscall of `posix-oneshot`, then runs fsck) | TestInjectIOError, TestInjectSigKill; `//go:build linux` (`:15`); CI job `posix-fault-injection` (`.github/workflows/integration_test.yml:28-37`) | [inspected; CI result not checked] |
| End-to-end inclusion check against a running POSIX log | `integration/log/log_integration.go:139` (`proof.VerifyInclusion`) | CI job `posix-tlog-tiles-api` via docker compose (`integration_test.yml:9-26`) | [inspected] |
| Mirror lifecycle with tamper cases | `mirror_lifecycle.go` | `mirror_lifecycle_test.go`: TestMirrorTarget_SealAndOpen (`:201-219` "tampering did not fail"), "invalid proof - corrupted hash" (`:1092`), "invalid consistency proof from corrupt tile" (`:1433-1441`) | [inspected] |
| Example binaries | `cmd/examples/posix-oneshot/main.go` (flags `:40-46` incl. `--witness_policy_file`, `--witness_fail_open`); `cmd/conformance/posix/main.go` (HTTP `POST /add`, static `GET /checkpoint`, `/tile/`, `/entries/`, `:128-150`) | used by the integration jobs | [inspected] |

CI lanes: Go tests on Go 1.26.x and 1.27.x, **`os: [ubuntu-latest]` only** (`.github/workflows/go_test.yml:10-14`), with `-race`. The suite also covers AWS-with-MySQL, the POSIX integration and fault injection, golangci-lint, govulncheck, CodeQL, OpenSSF Scorecard, benchmarks and terragrunt [inspected, workflow listing]. Deployment evidence: rekor-tiles (Sigstore Rekor v2) pins `github.com/transparency-dev/tessera v1.0.4` (`sigstore_rekor-tiles/go.mod:34`) [inspected]. That it serves the public Sigstore instance is [reported] by the ecosystem and was not verified here. The README names no other production users. The benchmark page was not opened.

What the README says beyond the code: "production ready since the Beta release" (`README.md:56-57`) [reported]. The driver table marks Migration as partial for every driver (`README.md:62-66`). The MySQL driver was **removed after v1.0.2** (`storage/mysql/README.md:1-10`). There is no in-memory storage driver. `log.go:45` declares `type Driver any`, and the only implementations are `storage/{posix,gcp,aws}`. `testonly/testlog.go:49` builds test logs on the POSIX driver [inspected].

Witness side: `transparency-dev_witness/witness/witness.go` implements add-checkpoint. Its persistence uses a SERIALIZABLE SQLite transaction (`persistence/sqlite/sql.go:197-222`, pure-Go `modernc.org/sqlite`, `go.mod:28`), which satisfies the spec's atomic check-and-persist rule (`tlog-witness.md:191-200`). Tests in `witness/witness_test.go:205-336` TestUpdate cover: stale old size (ErrCheckpointStale, mapped to 409), garbage consistency proof (ErrInvalidProof, 422), the same size with a changed root (ErrRootMismatch), a smaller checkpoint (ErrOldSizeInvalid) and a missing proof. `witness/http_test.go:146-224` TestHandler maps these to HTTP codes. TestUpdateSignatureVerification (`:387`) covers corrupted log signatures. Witness CI runs on `[ubuntu-latest, macos-latest]` (`transparency-dev_witness/.github/workflows/go_test.yml:11`) [inspected].

## 3. Maturity

- Footprint: one Go process with the driver in-process ("Library instead of microservice architecture… No additional services to manage", `README.md:23-26`) [reported]. The POSIX driver needs only a filesystem with strong rename semantics. Optional persistent antispam adds BadgerDB, which "can consume a high amount of RAM" (`README.md:320`; `storage/posix/README.md:59-64`) [reported]. A published POSIX benchmark on a 12-core, 8 GB LXC with ZFS mirror shows about 2900 writes/s without antispam and about 1600 with it (`storage/posix/PERFORMANCE.md`) [reported]. A DAO claim ledger needs a few writes a day.
- Cadence over the last 12 months (API): 8, 14, 15, 10, 16, 49, 10, 24, 50, 53, 47, 36 and 12 commits per month for 2025-10 to 2026-10. There were 7 releases in the last 13 months [inspected]. Bus factor is about 3 (see section 1).
- Issue response, sampled from five issues: #1233 got a maintainer reply in 5 minutes. #1192 got one in 3 days and was closed. #1217 was filed and closed by a maintainer the same day. #1207 (AWS driver lock contention, opened 2026-09-28) has no maintainer reply. #1098 (fsck deadlock on a corrupt tile, 2026-08-07) has **no reply in 74 days** [inspected via API].
- Security posture: `SECURITY.md` routes reports to GitHub private advisories. There are zero published advisories (API `security-advisories` returned 0). Scorecard, govulncheck and CodeQL run in CI. **No third-party audit** of Tessera or of the witness was found or cited [inspected; absence noted, not proven].
- Documentation is good. The README covers concepts and lifecycles, and `docs/design/` holds philosophy, lifecycle and antispam documents. There is no per-OS support statement anywhere: the POSIX README says only "POSIX-compliant filesystem" and "somewhat tested on local ext4 and ZFS … and CephFS" (`storage/posix/README.md:49-54`) [inspected].
- Counterexample rows, all answered:
  1. s2-br-c pass 1 (flock at `files.go:223,232`): **confirmed**. At HEAD the calls are at `storage/posix/files.go:224` and `:233`. The BadgerDB RAM warning is confirmed at `README.md:320`. Issues #1207 and #1098 are confirmed open. The Go-sidecar conclusion is confirmed (section 4).
  2. s2-br-c pass 2 (`O_DIRECTORY`, `os.Link`, no build tags, Linux-only CI): **confirmed**, with line numbers moved to `file_ops.go:44` and `:130`. `grep go:build` finds only `integration/fault/posix/fault_test.go:15`. I checked the Go 1.26.0 standard library source through the GitHub API instead of compiling. No `src/syscall/*windows*.go` file defines `Flock`, `LOCK_EX` or `LOCK_UN`, and `src/syscall/types_windows.go:54` defines `o_DIRECTORY` **unexported**. So `storage/posix` (and `cmd/mtc/log/internal/landmark/posix/posix.go:128`) cannot compile for `GOOS=windows` [inspected stdlib source; not compiled]. On darwin, `Flock` and `O_DIRECTORY` exist (`zsyscall_darwin_arm64.go:681`, `zerrors_darwin_arm64.go:740`), so macOS should compile, but it is untested in Tessera CI [hypothesis].
  3. s2-br-h (flock; tested on ext4/ZFS only): **confirmed**. Correction: the "MySQL-based AWS driver" is the only MySQL path, because the dedicated MySQL driver was removed (above).
  4. sigstore-rekor-tiles row (inherits the limitation): **confirmed** at `sigstore_rekor-tiles/go.mod:3` (`go 1.27`) and `:34`. `rekor-server-posix` is the "lightweight, no cloud dependencies" binary (`README.md:19, 38-43`), and rekor-tiles CI is ubuntu-only.

## 4. Architecture

Control flow, POSIX: the personality calls `posix.New(ctx, posix.Config{Path})` and then `tessera.NewAppender(ctx, driver, opts.WithCheckpointSigner(signer)[.WithWitnessPolicy(p)])`. `appender.Add(entry)` returns a future index. Entries are batched in memory, then sequenced under an exclusive `flock` on `.state/treeState.lock`. Entry bundles and tiles are written by temp file then `os.Link` (create-exclusive) or rename (overwrite), with directory fsync. `.state/treeState` is updated. Asynchronously, under `.state/publish.lock`, a checkpoint is signed. If a witness policy is set, the witness gateway POSTs `add-checkpoint` with a consistency proof to each witness (`internal/witness/client.go:308-379`). The checkpoint is published only when the policy is satisfied, unless `FailOpen`, which "will be disabled and/or removed in the future" (`append_lifecycle.go:1250-1255`). (Sources: `storage/posix/README.md:20-46`; `files.go:205-240`; `append_lifecycle.go:795-833`) [inspected].

- Read path: plain static files (`checkpoint`, `tile/<L>/<N>[.p/<w>]`, `tile/entries/<N>`; `api/layout/paths.go:31-157`). Any HTTP file server, CDN or object store serves them. The paths contain no characters that are illegal on Windows [inspected].
- Identity: the log is an origin string plus a signed-note key (Ed25519, or ML-DSA for cosignatures, `witness_test.go` TestNewWitnessGroupFromPolicy_MLDSA). Witnesses are identified by name and key. There is no per-entry principal: the entry is opaque bytes, and the personality decides what an entry means [inspected].
- Lifecycle: Appender, Migration target, Mirror and Freeze/quiescent (`README.md:353-398`). Crash recovery relies on the atomic file pattern and is proven only by the Linux fault-injection test.
- Dependencies (direct requires `go.mod:7-43`): cloud SDKs (Spanner, GCS, AWS S3), OpenTelemetry, Badger, bubbletea/tview (fsck TUI), the transparency-dev formats, merkle and witness modules, and `hashicorp/golang-lru/v2`. Go links only imported packages, so a POSIX-only binary avoids the cloud SDKs at link time. The root package still imports `golang-lru` (`antispam.go:22`) and OpenTelemetry (`otel.go:18-19`), but OTel exporters are wired only in `cmd/conformance/{aws,gcp}/otel.go` [inspected].
- Operational model: an embedded library inside a "personality" binary. For ResonantOS (Node 24) the options are, in order of fit:
  - (a) a Go sidecar speaking HTTP. The conformance personality is the template: it has an unauthenticated `POST /add` and static GETs (`cmd/conformance/posix/main.go:128-150`).
  - (b) a `posix-oneshot`-style CLI spawned per batch (`cmd/examples/posix-oneshot/main.go:58-160`).
  - (c) Node reading the static tiles and verifying in TypeScript, which needs no Go at all.
  - WASM is not viable for the writer, which needs flock and fsync [hypothesis].

## 5. Direct relevance

| Requirement | Resonant target | What Tessera / tlog-witness supplies | What it does not |
|---|---|---|---|
| R11 tamper-evident local audit ledger and approval ledger (OSC-47, os-map 17 seam 3, ADR-022 `Logs/audit-ledger.jsonl` unimplemented) | `browser-first/host/bridge-server.mjs:114-136` (`authorizeBridgeRoute`), the no-op gate in `browser-first/host/archive-review-policy.mjs:27-35`, the public-submit path (OSC-20) | An append-only Merkle log format (tlog-tiles), signed checkpoints, inclusion and consistency proofs, an fsck, and an external-witness protocol that turns local tamper-evidence into tamper-evidence that survives a compromise of the local signing key | The gate itself: no code refuses a route for lack of an approval record. No Windows build of the only local driver, and no Node API. Local tamper-evidence is weak when the log key sits on the same machine as the attacker (V2/V3 can rewrite everything and re-sign) unless a checkpoint is held elsewhere. **Attacker model (amended):** with the external checkpoint off by default (I1, section 7), the R11 design detects accidental corruption and tamper by a non-same-user party only. Against V2 or V3 running as the same user it detects nothing until the user enables an external checkpoint or a second device. |
| R30 off-chain Phase 1 (dao-requirements section 5 item 2; DR-50, DR-51) | No DAO code exists (census). This would be the Phase 1 claim ledger and membership registry substrate. | An append-only, publicly auditable log of salted claim and membership commitments. A member checks their own record's inclusion and the history's consistency from static files. Independent witnesses replace the chain for split-view resistance. The weekly checkpoint is the natural "weekly Merkle root" of DR-51. | Membership semantics, advisory votes, eligibility, treasury reports (DR-52) and privacy. tlog-tiles entries are public to anyone who can read the files, so DR-50 forces commitments-only entries. **Amended:** a log proves the order and the append-only history of what the operator chose to append, not the honesty of the entry set. (1) Omission: only the operator appends, and witnesses see checkpoints, never entries (`C2SP_C2SP/tlog-witness.md:50-58, 97-110`), so a dropped claim, appeal (DR-26) or revocation contest leaves no trace without the receipts of section 7. (2) Insider inflation: with commitments-only entries, custodians can append phantom members or claims that no outsider can see (T16/V7 run by V6). Signed entries and typed public counts (section 7) make phantoms attributable and countable, not impossible; personhood is R25. (3) Attribution: the log carries whatever human/AI split a record states and vouches for none of it (T13 and T20 stay open). |

Threats:
- **T5** (silent corruption of the knowledge boundary) is partly closed. A ledger of promotion approvals makes after-the-fact rewriting detectable. It does not stop a write that bypasses the gate (R14, R19 and the seam-3 gate remain custom).
- **T18** (premature on-chain commitment) is closed well for the R30 role. A witnessed log gives Phase 1 public auditability with no token, no program and no upgrade authority. An optional SPL Memo anchor adds a chain record without a custom program (section 8).

Property check (threat-model section 4):

| Property | Status | Evidence |
|---|---|---|
| Approval and audit: "ledger tamper detected" | **Demonstrated at the proof layer.** Not demonstrated at the store layer. | Proof layer: `transparency-dev_merkle/proof/verify_test.go` TestVerifyInclusionProbes and TestVerifyConsistencyProbes reject 92+92 mutated vectors. The witness's TestUpdate rejects a garbage consistency proof, the same size with a changed root, and a smaller checkpoint. Tessera's `mirror_lifecycle_test.go` "invalid consistency proof from corrupt tile". Store layer: `fsck/fsck_test.go` has **no tampered-log test**, and issue #1098 (confirmed in code at `fsck/fsck.go:115, 309, 328, 346-362`) shows fsck **hangs instead of failing** when a tile mismatches, with the default `N: 1`. It never reports success, but it never returns. `client.TestCheckLogStateTracker` has no inconsistency case, and `LogStateTracker.Update` silently ignores a checkpoint of equal or smaller size (`client/client.go:397-399`), so an equal-size fork is not flagged on the client side. |
| Consistency proofs (named tests) | Demonstrated | Merkle TestVerifyConsistencyProbes. Witness TestUpdate cases "vanilla consistency garbage proof", "resubmit known CP with changed root", "submit smaller checkpoint". Tessera TestSlipperyWitness. |
| Approval and audit: "route refuses without approval record" | Not demonstrated, out of scope for this codebase | It would need the custom seam-3 gate (section 7). |
| Approval and audit: "user-readable export" | Partial | The checkpoint is text and entries are the personality's own bytes (they can be JSON). Tiles are binary but specified by tlog-tiles. |
| Minimal architecture: "off-chain Phase 1 … public auditability" | Designed and partly tested for the ledger part | Witnessing and proof tests as above. Membership and vote semantics are absent. Omission and insider inflation: see the two rows below. |
| Witnessing as chain-free anchoring | Demonstrated by spec plus tests, **for rollback and for forks shown to the same witness** | `C2SP_C2SP/tlog-witness.md:89-200`; witness TestUpdate and TestHandler (409/422 mapping); cosignatures carry a timestamp (`C2SP_C2SP/tlog-cosignature.md:102-110`). |
| Split-view resistance for members (amended) | **Demonstrated in parts, not end to end.** It holds only under three conditions: (i) the member verifier, not only the log, enforces the policy; (ii) any two cosigner sets that satisfy the policy share at least one witness (quorum intersection); (iii) a witness in that intersection is honest. | Parts: a single witness refuses a fork it can see (witness TestUpdate "resubmit known CP with changed root"); the verifier quorum rule rejects a checkpoint that lacks the required group (formats TestSatisfied "inner group without outer member"). Not tested anywhere upstream: a log that shows fork A to one witness and fork B to another. Under a threshold-1 group of several witnesses (including the "1 of 3" this dossier first proposed, and the reviewers' "1 of the outside group AND 1 of any"), two disjoint honest witnesses each cosign one fork, so a split view needs no colluding witness at all. The spec itself warns that monitors may need more cosignatures than clients (`C2SP_C2SP/tlog-witness.md:285-292`). Needed: the policy of section 7 and acceptance fault 3(e). |
| Omission (C-5, amended) | **Not designed upstream; custom.** | Tessera returns a durably assigned index before integration (`append_lifecycle.go:222-243`; `Index` `:251-256`), which is the hook for a signed receipt. C2SP static-ct-api makes the same move mandatory for CT logs (`C2SP_C2SP/static-ct-api.md:122-135`, the `leaf_index` SCT extension "makes it possible for auditors to verify inclusion of an SCT in the log by fetching the entry by index"). Tessera's generic personalities issue no receipt (`cmd/conformance/posix/main.go:128-140` returns a bare index). Needed: section 7 receipts and acceptance fault 3(f). |
| Insider phantom entries (amended) | **Not demonstrable by any log.** | A log can make each entry attributable (a member signature) and countable (public type and epoch). It cannot tell a real member from a custodian-made key. That is R25 (personhood) plus an independent auditor with access to the off-log store. |

## 6. Reuse decision

**Split decision.**
- **R30 (DAO Phase 1 claim ledger): adopt as a dependency, wrapped in a small Go log service on one Linux host.** This means Tessera v1.0.4 (pinned) with the POSIX driver and three outside, non-custodian witnesses under a 2-of-3 acceptance policy (amended; the first version read "2-3 OmniWitness instances, at least one outside the custodian set"). Members verify with a TypeScript verifier. The SPL Memo anchor (ChartRunner pattern) is optional.
- **R11 (desktop audit and approval ledger): learn the pattern and reimplement** in the Node bridge, using the C2SP formats and the merkle test vectors, or take hypercore. Do not embed Tessera in the desktop.
- **After review (2026-10-21): both decisions stand, and the R30 adoption now carries three conditions.** (1) The member verifier enforces a published witness policy with quorum intersection over outside witnesses (section 7), not the flat "1 of 3" first proposed. (2) The log service issues signed submission receipts, so omission is provable. (3) Member-signed, typed entries, so phantom entries are attributable and countable. Without (1) the witness design gives no split-view resistance against the custodians (V6), and it is then no better than hypercore for R30. No hard gate changed.

Why this beats the alternatives in section 12:
- For R30, nothing else in the ledger combines a standard, multi-implementation checkpoint and witness protocol (C2SP) with a static, cache-friendly read path that members can audit with no account.
- rekor-tiles is a Sigstore-specific personality on top of Tessera.
- hypercore has no third-party witness protocol and no static read path.
- For R11, the Windows gap and the Go runtime make Tessera a worse fit than a Node-native log, and the desktop needs only a fraction of Tessera's scale features.

Hard gates:

| Gate | R11 desktop role | R30 Linux-host role |
|---|---|---|
| G1 no mandatory cloud or telemetry | Pass. The POSIX driver needs no service. OTel has no exporter unless configured (exporters only in `cmd/conformance/{aws,gcp}/otel.go`). | Pass. OmniWitness can optionally fetch the public witness-network config over the network (`transparency-dev_witness/config/public_witness_network.go`). |
| G2 three OSes or an honest matrix | **Fail as-is.** The POSIX driver does not compile on Windows. It is visible (a build error), not a silent no-op, but upstream states no per-OS matrix and has no Windows CI or issue. | Pass with a condition: the operator chooses Linux, the CI-tested OS. macOS is untested, and Windows works only through WSL2 [hypothesis]. |
| G3 licence | Pass. Apache-2.0. MPL-2.0 transitive dependencies are flagged in section 9. | Pass, same. |
| G4 chain | Pass (none). | Pass (none). An anchor would be Solana memo. |
| G5 invariants | Pass with a condition: the local ledger must not be witnessed by any DAO-run service by default (I1, I3). | Pass. Witness keys and log keys confer no runtime authority (I2). |

## 7. Integration design

**R30, the DAO ledger (Phase 1 core item 2).**
- Process boundary: one Go binary (a personality of about 200 lines on the POSIX driver, modelled on `cmd/conformance/posix/main.go`). It runs on a Linux VPS or a member's Linux box. The data directory is rsync'd to static hosting.
- Entry format, with DR-50 in force (amended after review). Each entry is a small public envelope `{v, type, epoch, commitment, signer_pk, sig}`:
  - `type` is one of join, revoke, recover, claim, explanation, appeal, contest, tally. `epoch` is the claim cycle.
  - `commitment = SHA-256(salt || canonical_json(record))`. The record is a claim, an explanation record or a signed membership agreement, and it stays off-log in the access-controlled store.
  - `sig` is the member's signature over a domain-separated message `"resonantdao-ledger/v1" || origin || type || epoch || commitment`, so no signed byte string can also parse as a Solana transaction message (S-2). The member's wallet signs it only through an off-chain-message format that wallets keep apart from transactions [hypothesis: the Solana off-chain message format uses a 0xff-prefixed signing domain for this; not inspected in this study]. The verifier must reject any record whose signed bytes parse as a transaction message (fixture in section 11, 3(h)).
  - `signer_pk` is a per-member ledger key bound to the wallet once, in the join record (off-log), so the public log does not carry the wallet address. A stable ledger key still lets anyone count entries per pseudonym. That conflicts with DR-32 (no member ranking) unless per-epoch keys are used. This is recorded as contested for Gate 3 (D3.9; section 14).
  - What this buys: (a) custodians cannot append a claim or a membership change in a real member's name without that member's key. (b) Join minus revoke counts, claims per epoch and appeals per epoch become public and auditable from the static files (D-3). (c) Phantom members made from custodian-generated keys remain possible. Only personhood (R25) and an independent auditor who can read the off-log store and the signed membership agreements can challenge them. That residual risk goes in the article.
- Salt and record custody (D-5). The custodian computes the commitment, so the salt protects against outsiders only. At append time the member client receives and keeps the record, the salt, the receipt and later the inclusion proof. The governance rule must say what happens when the store cannot produce a committed record: a presumption in the member's favour, decided under DR-26. This is a DAO rule, not code.
- Submission receipts (D-2, omission). The personality signs a receipt after `appender.Add(...)()` returns the durably assigned index (`append_lifecycle.go:222-243`): `receipt = sign_receipt_key(origin || index || SHA-256(entry) || deadline)`, with `deadline` at most one checkpoint interval plus a published grace period. This is the static-ct-api `leaf_index` pattern (`C2SP_C2SP/static-ct-api.md:122-135`) applied to a generic log. A receipt plus any witnessed checkpoint of size greater than `index` is a self-contained proof of misbehaviour if the entry at `index` differs. A receipt whose deadline passes with no covering checkpoint proves delay. What receipts cannot fix: an operator who refuses to issue one. Against that, the member signs the submission itself, and the member client posts the signed submission to a second channel the custodians do not control (a partner's log or the public forum) as evidence of attempted filing. The receipt key is not the log key, and both are listed under DR-48.
- Membership changes (join, revoke, recover) are log entries too, so the registry history is append-only (core item 1). The same log can carry one governed revocation record type with the DR-06 fields (reason, authority, evidence reference, appeal deadline, reversal) from which derived artefacts are produced (DAO skeptic C-4). Whether to centralise revocation there is the lead's decision.
- Advisory-vote tallies are entries that commit to the replayable input set (core item 6). Votes themselves need a separate tool such as Loomio or Belenios.
- Checkpoint cadence: hourly or daily, with witnesses cosigning each one. Weekly, the operator posts the latest witnessed checkpoint `(origin, size, root)` as one SPL Memo (optional, section 8).
- **Witness policy (amended after review; replaces the earlier "1 of 3").** There are two policies, and only one protects members:
  - The *publication* policy is what Tessera waits for before it publishes (`WithWitnesses`, `append_lifecycle.go:805-829`). It is an availability setting.
  - The *acceptance* policy is what the member verifier requires before it trusts a checkpoint. It is the security setting: tlog-policy is written mainly for this offline verification (`C2SP_C2SP/tlog-policy.md:13-17`). It is pinned in the verifier, published beside the log, and changed only by a governed, logged record.
  - Both use the same file:

    ```
    # ResonantDAO Phase 1 ledger, acceptance policy v1
    log <dao-ledger vkey> <read url>
    witness EA <vkey> <url>    # outside organisation A
    witness EB <vkey> <url>    # outside organisation B
    witness EC <vkey> <url>    # public witness network or organisation C
    group outside 2 EA EB EC
    quorum outside
    ```
  - Why 2 of 3 and not "any": any two sets that satisfy `outside 2` share at least one outside witness, so a split view needs that witness to collude. Under `any` (threshold 1), two disjoint honest witnesses can each cosign a different fork, so a split view needs no collusion at all. This 2-of-3 form is the one the article quotes (lead ruling D3.9).
  - Rejected alternative: "log key AND (1 of the outside group) AND (1 of any)", the form both reviewers proposed (S-1, D-1). It is rejected because its outside requirement has threshold 1 over several witnesses. Fork A cosigned by EA and fork B cosigned by EB each satisfy it, so it has the same disjoint-quorum flaw as `any`. The general rule for a k-of-n group with f colluding members: two quorums cannot be served disjoint forks only if 2k - n > f. The syntax and the quorum semantics are those tested in formats TestSatisfied (`transparency-dev_formats/policy/tlog_policy_test.go:488`), and `group <name> 2 ...` is the spec's own example form (`C2SP_C2SP/tlog-policy.md:71`).
  - Custodian-run witnesses add nothing against V6 and are left out of the quorum, so the operator runs no witness. Recruiting three outside witnesses is a pilot precondition. If only one outside witness can be found, use `quorum EA` (all of one): that is safe against split views but blocks publication while EA is down.
  - Gossip: the member verifier also fetches, where available, each outside witness's latest cosigned checkpoint from a distributor (`transparency-dev_witness/omniwitness/distribute.go:40`). It alarms on two consistent-looking checkpoints of the same size with different roots, or on any pair it cannot prove consistent. OmniWitness exposes no tlog-witness monitoring GET that a grep could find, so distribution goes through the distributor [inspected, absence by grep].
- Member verification:
  1. Fetch the checkpoint and verify it with the pinned acceptance policy (log key plus `outside 2`), as formats `TLogPolicy.Verify` does (`transparency-dev_formats/policy/tlog_policy.go:349-388`).
  2. Fetch the tiles needed for the inclusion proof of `entry` and verify it. Check the entry's `sig` and the receipt.
  3. Keep the last checkpoint seen and verify a consistency proof to the next one. The client must flag equal-size, different-root checkpoints, which Tessera's `LogStateTracker` does not (section 8).
  4. For every receipt the member holds, check that a checkpoint covering `index` exists before `deadline` and that the entry at `index` matches.
- Error behaviour: if the witness quorum is unreachable, no checkpoint is published and entries remain sequenced but unpublished (`append_lifecycle.go:1244-1255`). Members then see receipts age toward their deadlines. The operator gets an alert, and the published cadence states the grace period. The policy is not weakened to restore availability.
- Versioning: pin the Tessera tag, and pin C2SP spec versions (`tlog-cosignature@v1.1.0`, `tlog-checkpoint@v1.1.0` as cited in `tlog-witness.md:14-18`).

**R11, the desktop ledger (os-map 17 seam 3).** This is where Tessera is not embedded.
- Approval flow: a human ceremony in the extension produces an approval record `{principal, routeKey, actionHash, decision, ts}`. A new `browser-first/host/approval-ledger-service.mjs` appends it to a local tlog-tiles-format log under `~/ResonantOS_User/Logs/` (the ADR-022 location), using a TypeScript writer or hypercore. The service returns `{index, checkpoint}`.
- Gate: `authorizeBridgeRoute` (`bridge-server.mjs:114-136`) gains an optional `requiredApproval` route field. For such routes it verifies an inclusion proof of a matching approval record against the current local checkpoint before returning `{route}`.
- Promotion: `assertArchiveReviewTransitionAllowed` (`archive-review-policy.mjs:27-35`) requires the same proof instead of trusting an `actor` string.
- Identity: the principal comes from seam 1 (R01 grants). The ledger only records it.
- External checkpoint: tamper-evidence against a local attacker needs the latest checkpoint held outside the machine. The options are a second device, or a user-chosen witness that the user enables explicitly (I3). Off by default (I1).

Alpha files that change:
- `browser-first/host/bridge-server.mjs`, `browser-first/host/archive-review-policy.mjs` and `browser-first/host/run-bridge-minimal.mjs` (wiring).
- New: `browser-first/host/tlog-verify.mjs` and `browser-first/host/approval-ledger-service.mjs`.

Tests affected among the 2,424:
- `test/bridge-route-capability-audit.test.mjs`: "harness routes retain the exact capability and transport boundary" (`:240`) deep-equals route and capability tuples. Adding a field is safe only if that tuple shape is kept.
- `test/bridge-server.test.mjs` and `test/bridge-get-routes-require-capability.test.mjs`.
- `test/archive-review-policy.test.mjs`: it asserts the current `nextStatus` and actor semantics.
- `test/agent-control-public-submit.test.mjs` and `test/living-archive-continuity-acceptance.test.mjs` [inspected file existence and the assertions named].

## 8. Security and governance effects

- **Witnessing versus a Solana anchor.**
  - Witnesses verify consistency before cosigning and keep only the latest checkpoint per log (`tlog-witness.md:55-58, 138-173`). They refuse rollbacks (400/409) and forks (422) [inspected spec + tests]. **Corrected after review:** the first version said that clients requiring k-of-n cosignatures "cannot be shown a split view unless k witnesses collude". That is wrong. Each witness checks consistency only with what it has itself seen, so a log can show fork A to one set of witnesses and fork B to a disjoint set. Clients are protected only when every two satisfying sets intersect in an honest witness (2k - n > f for a k-of-n group with f colluders). See the policy in section 7 and `C2SP_C2SP/tlog-witness.md:285-292` [inspected spec; reasoning].
  - Witnesses cost nothing on-chain, add a timestamped cosignature, and are already a public network (`transparency-dev_witness/README.md`).
  - What a Solana memo anchor of a checkpoint adds:
    - (1) A durable, globally ordered, public timestamp that does not depend on the witness set's honesty or uptime.
    - (2) A single place where any member, or an outsider, finds the commitment without knowing the witness keys.
    - (3) Evidence that survives if the log operator deletes the log and every witness is retired.
  - What it does not add:
    - The memo program does not check consistency, so a verifier must still check consistency proofs between successive anchors off-chain.
    - Nothing stops two different memos. ChartRunner handles this with a social "first finalized wins" rule (`ChartRunner_chartrunner-onchain/SPEC.md:165-177`).
    - Data availability.
  - The anchor adds new things to manage: a fee-payer key to hold (custody under DR-48), an RPC dependency, and a small cost per anchor [hypothesis on cost; not measured].
  - Anchor rules (amended after review, S-4 and D-6). An anchor proves when a root was posted and by whom, not that the root is honest. So:
    - (1) The anchor signer is its own key, held off the log host by a different custodian than the log key (ideally the R24 multisig), and listed under DR-48. Verifiers check the signer, as ChartRunner's verifier does (`ChartRunner_chartrunner-onchain/SPEC.md:132-137`). Otherwise whoever takes the log host both forks the log and anchors the fork.
    - (2) Only a checkpoint that satisfies the acceptance policy may be anchored, and verifiers reject an anchor whose checkpoint lacks the `outside 2` cosignatures.
    - (3) The cadence is published, and the member verifier treats a missing weekly memo as an alarm, not as silence.
    - (4) Verifiers check consistency between successive anchored checkpoints.
  - Conclusion: for Phase 1, witnesses do the anti-equivocation work, but only under an intersecting acceptance policy. A weekly memo anchor under rules (1)-(4) is cheap insurance and a member-facing signal, not a correctness requirement.
- **Capture (V6), amended:** if the custodians hold the log key and also run every witness, or run enough of them that two disjoint quorums exist, split views are undetectable. The acceptance policy of section 7 (`outside 2` over three non-custodian witnesses, with no custodian witness in the quorum) needs one outside witness to collude before a split view is possible. The earlier "1 of 3" did not meet this, and it is withdrawn. Acceptance into the public witness network is unverified [hypothesis]. The anchor helps only under rule (1), because custodians cannot rewrite Solana history but can post a fork to it.
- **Omission and insider inflation (V6, amended):** witnesses and anchors attest to order and history, never to the completeness or honesty of the entry set. Receipts (section 7) make omission provable after the fact. Signed, typed entries make phantom claims in a real member's name impossible without that member's key, and make total counts auditable. Phantom members built from custodian-made keys remain possible (R25), and an operator who refuses to issue receipts is countered only by out-of-band filing.
- **Attack surface added:**
  - The conformance-style `POST /add` has no authentication (`cmd/conformance/posix/main.go:128`). A DAO service must put its own auth in front of it: accept only member-signed envelopes (section 7) and run on the DAO host, never next to the ResonantOS bridge (security X-6). The receipt signer is a second key on that host. A compromise of the host yields false receipts, which are self-incriminating, not silent.
  - A desktop sidecar listening on loopback would reopen the T3 class (V2 local processes), so prefer a Unix socket or a spawned CLI.
- **Disconfirmation findings:**
  - (a) fsck hangs on a corrupt tile (#1098, unanswered for 74 days; code confirmed). Any tooling must wrap fsck in a timeout and treat a timeout as failure.
  - (b) `LogStateTracker.Update` returns the old checkpoint without error when a new one is equal or smaller (`client/client.go:397-399`, test "Out of order" `:164-177`). An equal-size fork goes unreported unless the caller compares roots.
  - (c) FailOpen is slated for removal, which couples publication availability to witness availability.
  - (d) Crash-consistency evidence exists only on Linux (strace). Filesystem coverage is "somewhat tested" ext4, ZFS and CephFS.
  - (e) No external audit. No CVEs or advisories were found.
- **Personal data:** under DR-50, only salted commitments go in entries. Checkpoint size and cadence leak activity volume (minor). Salts must not be guessable, given the low-entropy records (DR-50 note).
- **Friction:** members need a verifier (CLI or web page). Operators run one service plus witness coordination. Witness downtime blocks publication.

## 9. Licensing

- Tessera: Apache-2.0 (root `LICENSE`, no per-directory variants) [inspected]. Witness and merkle: Apache-2.0. C2SP: specs CC BY 4.0 (attribution needed when copying spec text into Resonant documentation) and code BSD-1-Clause (`.github/MANUAL.md:62-70`). sigstore-js: Apache-2.0. ChartRunner: Apache-2.0 plus NOTICE. hypercore: MIT.
- Notable transitive dependencies:
  - `github.com/hashicorp/golang-lru/v2` is **MPL-2.0** and is imported by the root package (`antispam.go:22`). It is file-level copyleft: modified MPL files must stay available, while unmodified linking imposes no obligation on the rest [reported licence terms].
  - `github.com/go-sql-driver/mysql` is MPL-2.0, in the AWS driver only.
  - Badger: Apache-2.0. `modernc.org/sqlite` (witness): BSD-3-Clause [reported licence, not re-read].
- Compatibility with the MIT Alpha: high for a separate binary or service. Vendoring merkle test vectors or sigstore-js `tlog/merkle.ts` and `checkpoint.ts` (about 350 lines) into the MIT Alpha requires keeping Apache-2.0 headers and a NOTICE. The Symbiotic Licence is status F (unknown).
- For legal review: (1) MPL-2.0 in a distributed Go binary; (2) CC BY 4.0 attribution if spec text is quoted in the DAO specification; (3) Apache-2.0 section 4 notice duties when vendoring test vectors into an MIT repository. This is technical research, not legal advice.

## 10. Cost and effort

Assumptions: the team is Node and TypeScript-first with no Go experience (os-map section 16). The DAO side has no code today.

| Scenario | Scope | Estimate [hypothesis] | Skills |
|---|---|---|---|
| Small | TypeScript verifier (RFC 6962 inclusion and consistency, signed-note checkpoint, cosignature policy check) in the bridge, with tests on the merkle vectors | 3-5 days | TS, crypto basics |
| Medium | DAO log service: Go personality on the POSIX driver with envelope checking and signed receipts, systemd unit, static hosting sync, recruiting three outside witnesses (amended: the operator no longer runs its own OmniWitness instances), weekly memo anchor script under a separate key, member verifier page with policy, receipt and gossip checks | 3-5 weeks for the first deployment (was 2-4 before receipts and envelopes), then about 1-2 hours/week operations plus witness coordination | Go, which the team lacks; Linux ops; Solana tx signing |
| Large | Make the POSIX driver Windows-capable: LockFileEx through `x/sys/windows`, a directory-fsync replacement (opening and syncing a directory handle on Windows has different semantics), rename-over-open-file behaviour, and Windows fault tests with no strace equivalent | 3-6 weeks plus indefinite fork maintenance with no upstream Windows CI | Go, Windows filesystem semantics |

Lock-in is low. The data format is an open C2SP spec with several implementations (Tessera, sunlight-style static logs, Sigstore), and a log can be re-served by any static host [reported]. Replacement cost: the TS verifier stays valid for any tlog-tiles log. Language cost: Go only on the DAO operator's host. The desktop stays Node.

## 11. Acceptance test

**This is a request: it executes third-party code (building Tessera and the witness) and needs user approval for a sandboxed Linux run (D1.5).** The TS-verifier half (step 1) runs only project code over data files and could run in the Alpha CI once PR 1 exists.

1. Vector conformance (no third-party code execution): the new `tlog-verify.mjs` runs all 98 inclusion and 98 consistency vectors from `transparency-dev_merkle/testdata/`, plus the subtree sets. Pass when 100% match `wantErr`. CI: `browser-first/test/tlog-verify.test.mjs`, auto-discovered by `scripts/run-browser-first-extension-tests.mjs`. Runs on Windows, macOS and Linux runners.
2. Sandbox, Linux container, Go 1.26.9, Tessera v1.0.4:
   - Build `posix-oneshot` and the conformance server, plus 3 OmniWitness instances standing in for the outside witnesses EA, EB and EC, under the section 7 policy `group outside 2 EA EB EC`. Add a fourth instance, C1, as a custodian-run witness that is deliberately left out of the quorum.
   - Append 1,000 salted commitments in 10 batches.
   - Expected: 10 checkpoints, each with at least 2 cosignatures, and the TS verifier accepts inclusion of entries 0, 511 and 999 plus consistency between all successive checkpoints.
3. Fault scenarios (threat model T5 and T18; V6 insider):
   - (a) Flip one byte in `tile/entries/000`. The TS verifier must reject inclusion for an entry in that bundle. Expect `fsck` with `N=1` to hang, which documents #1098. Pass when the external timeout of 60 s is treated as failure.
   - (b) Operator fork: rebuild the log with entry 500 changed, sign the same size, and submit to the witnesses. Expect 422 or 409, no cosignature, and the TS verifier must flag the equal-size different-root checkpoint.
   - (c) Truncation: submit a smaller checkpoint. Expect 400 or ErrOldSizeInvalid.
   - (d) SIGKILL during append, using the upstream `TestInjectSigKill`. Expect fsck clean.
   - (e) Capture and split view (added after review, S-1 and D-1). Build fork B of the log at the same size as fork A.
     - Case 1: B is cosigned by C1 alone. The member verifier must reject it as quorum not met.
     - Case 2: A is submitted only to EA, and B only to EB and EC. A must be rejected (one outside cosignature), and B accepted.
     - Case 3: A is submitted to EA and EB, and B to EB and EC. EB must refuse B with 409 or 422, so B cannot reach quorum.
     - Case 4: rerun case 2 under a flat `any` policy. Both forks are accepted, which documents why `any` is unsafe.
     - Case 5: the gossip check, fed both forks, must alarm.
   - (f) Omission (added after review, D-2). Submit an entry, keep its receipt, then have the operator drop it, either by rebuilding the log without it or by placing a different entry at its index. After the deadline, the member verifier must output a misbehaviour proof `(receipt, checkpoint, inclusion proof of the different leaf)`, or a delay proof if no checkpoint covers the index.
   - (g) Phantom entry (D-3). Append a claim envelope whose `sig` is made with a key not bound in any join record, and a join without a wallet-signed agreement in the store. The public count check must list the first as unattributable, and the auditor check must flag the second.
   - (h) Cross-protocol signing (S-2). Present a record whose signed bytes are a valid serialized Solana transaction message. The verifier must reject it for missing the domain prefix.
4. Windows probe: `GOOS=windows go build ./storage/posix/` is expected to fail with `undefined: syscall.Flock`, confirming section 3 as [executed].

Pass/fail: all expectations met, and every fault produces a non-zero exit or an explicit verifier error within 60 s.

## 12. Recommendation and confidence

- Benefits: an open, multi-implementation standard (tlog-tiles, signed-note checkpoints, tlog-witness), production use under Sigstore Rekor v2 [reported], strong proof-layer tests, a Linux crash-fault suite, static reads, and no tokens or programs needed for Phase 1.
- Trade-offs: Go only. Linux-only CI. The POSIX driver does not compile on Windows. fsck hangs on corruption. The client tracker ignores equal-size forks. Publication depends on witness availability.
- Blockers: none for R30 on a Linux host. For R11 desktop use, the Windows gap blocks Tessera itself, though not its formats. No reviewer raised a blocker. The four major DAO objections were accepted or partly accepted, and none changes a hard gate. They do change what "adopt" means for R30: Tessera supplies the log, and the Resonant layer must add the intersecting acceptance policy, receipts and signed typed entries.
- Readiness: R30 is ready for a pilot once three outside witnesses are recruited and the section 7 additions exist. R11 is pattern-only.
- Residual risks to state in the article: (1) insider Sybil (phantom members from custodian-made keys) is not closed by any log; (2) a receipt cannot be forced from an operator who refuses one; (3) the log vouches for no human/AI split.
- Evidence quality: about 70% [inspected] (code, tests, CI files, stdlib source), about 25% [reported] (production claims, performance, licences of transitive dependencies) and the rest [hypothesis] (macOS behaviour, Windows port effort, anchor cost). Nothing [executed].

Competing solutions, on the same criteria:

| Criterion | Tessera + tlog-witness | holepunchto/hypercore | sigstore/rekor-tiles | ChartRunner on-chain (anchor layer) |
|---|---|---|---|---|
| Fit R11 desktop | Format and verifier only | Better: Node-native append-only Merkle log, signed tree head binding key, length and fork | Poor: Sigstore entry types only (`pkg/types/hashedrekord`) | n/a |
| Fit R30 public audit | Best: witness protocol, static read path | Weaker: P2P replication. Truncation is visible only to replicas that saw the earlier head (`test/basic.js:198`, `test/conflicts.js` fork detection). No third-party witness standard. | Overkill: gRPC and protobuf server, fixed entry types, design docs access-controlled (`README.md:7-11`) | Complements Tessera: memo transport plus equivocation rule (`SPEC.md:34-56, 165-177`) |
| Windows | Fails (POSIX driver) | CI matrix includes `windows-latest` (`holepunchto_hypercore/.github/workflows/test-node.yml:24`) | Fails (inherits; `go.mod:34`) | TS, ubuntu CI only |
| Tamper tests | Proof-layer negatives, no store-level negative | `test/merkle-tree.js` proofs, `test/merkle-tree-recovery.js` bad-root recovery, `test/conflicts.js` | Inherits Tessera | `packages/verify/src/__tests__/vectors.test.ts` and about 119 test cases in 7 files |
| Maturity | v1.0.4, 18 contributors, no audit | v11.39.0, maintained by Holepunch | v2.3.0, OpenSSF Sigstore | 15 commits, one author, created 2026-10-06, no release, `@chartrunner/verify` 0.1.0 with zero dependencies |
| Licence | Apache-2.0 | MIT | Apache-2.0 | Apache-2.0 |

ChartRunner's tree is RFC 6962-shaped: it uses `0x00`/`0x01` domain separation and promotes a lone node, which yields the same root as RFC 6962 for ordered input [hypothesis from the algorithm]. But it **sorts leaves** (`SPEC.md:238-257`), so it commits to a set snapshot, not an append-only log. Its verifier cannot recompute a Tessera checkpoint root from rows. Reuse its memo grammar, signer rule and equivocation rule with a new kind (for example `tlog`, root = checkpoint root, count = tree size), plus a custom consistency check between anchors. It is a learn-the-pattern reuse, because the project is two weeks old.

**First PR** (ResonantOS 2.0.0-alpha, Node only, no route changes):
- Add `browser-first/host/tlog-verify.mjs`, exporting `verifyInclusion`, `verifyConsistency`, `parseCheckpoint` and `verifyCheckpointNote(note, verifiers, policy)`. It is ported from `sigstore_sigstore-js/packages/verify/src/tlog/merkle.ts` and `checkpoint.ts` with Apache-2.0 headers, and adds a consistency verifier that sigstore-js lacks.
- Add `browser-first/test/tlog-verify.test.mjs` with vendored vectors under `browser-first/test/fixtures/tlog-vectors/` and a NOTICE.
- It changes none of the 2,424 existing tests. It is the shared verifier for both seam 3 and the DAO member check.

Confidence: **medium** (unchanged after review). The proof-layer evidence and the Windows finding are solid [inspected]. The R30 operating model, the witness-network acceptance and the anchor cost are not exercised, and the fsck and tracker gaps show that the "tamper detected" property needs project-side verification code and tests.

## 13. Scores (for scoring/scores.csv)

Profile **os_kernel** (R11):

| Criterion | Score | Reason (anchor) |
|---|---|---|
| requirement_fit | 2 | Supplies the log, proofs and witness, but not the approval gate, the Windows desktop or the Node API. A local key weakens local tamper-evidence. |
| demonstrated_maturity | 4 | Releases, CI, tests, used by rekor-tiles. Issue response uneven (#1098 unanswered 74 days). |
| isolation_and_security | 3 (unchanged after review) | Designed and partly tested: strong proof-layer negative tests, and the mirror tests exercise tamper detection itself ("invalid consistency proof from corrupt tile"). But there is no store-level tamper test, a fsck hang (#1098) and a tracker that ignores equal-size forks. Under clause (d) these are not contrary evidence: fsck never reports a tampered log as clean, and the proposed design neither uses the tracker nor embeds Tessera. Attacker model (S-3, X-2): tamper evidence holds only against non-same-user attackers unless the user enables an external checkpoint. Against V2 and V3 the default R11 design detects accidents, not tamper. |
| licence_suitability | 5 | Apache-2.0 file-level (MPL-2.0 transitive dependencies noted). |
| integration_effort | 1 | Needs the Go runtime, which the team lacks, and the only local driver needs a fork for Windows. |
| maintenance_sustainability | 4 | Steady monthly commits and 7 releases in 13 months. Bus factor about 3. |
| sovereignty_and_portability | 4 | Local files, no account, open format. Tiles are not human-readable. |
| interoperability | 5 | C2SP tlog-tiles, checkpoint and witness standards, public witness network, Sigstore compatibility. |
| operational_complexity | 3 | Would be one Go sidecar beside the Node bridge. |

Weighted (os_kernel): 3.26 (unchanged after review).

View **dao_contract** (R30):

| Criterion | Score | Reason (anchor) |
|---|---|---|
| requirement_fit | 3 | Ledger, public audit and chain-free anchoring covered. Membership, vote and treasury semantics are absent. |
| demonstrated_maturity | 4 | As above. |
| isolation_and_security | 3 -> 2 (lead ruling D3.9) | Omission is now a checked property for R30 (threat model v0.2, T24), and upstream does not demonstrate it. Tessera, the witness and C2SP tlog-witness have no receipt or omission mechanism; only the separate static-ct-api personality has one (section 5). Under clause (d), that absence scores 1 at most for that property. The other R30 properties remain at 3, with parts tested and each test exercising the property itself (clause (b)): witness fork and rollback refusal (TestUpdate), and verifier quorum rejection of a missing required group (formats TestSatisfied). Split-view resistance across disjoint witnesses is not tested end to end. There is no contrary evidence in the artifact as now proposed, because the flat "1 of 3" was this dossier's own configuration and is withdrawn. Taken together, 2. |
| licence_suitability | 5 | Apache-2.0. |
| integration_effort | 3 -> 1 (D-4) | Anchor "1 = requires … a language runtime the team does not have". The R30 service is a Go personality, plus receipt and envelope code, written by a team with no Go (section 10). This matches the os_kernel row. The TS verifier is small, but it is the integrator's side, not the artifact's. |
| maintenance_sustainability | 4 | As above. |
| sovereignty_and_portability | 4 | Self-hosted static files, no account, optional public witnesses. |
| interoperability | 5 | Same standards, and the anchor is chain-agnostic. |
| operational_complexity | 4 -> 2 (D-4) | Between anchors 3 ("one database or one sidecar") and 1 ("several services"). The operator runs one Go process, a static-host sync and a weekly anchor job under a separate key. Publication depends on the liveness of two of three outside witnesses that the operator must recruit and coordinate. Now that the operator runs no witness of its own (section 7), 2 is the floor the reviewer suggested, not 1. |

Weighted (dao_contract): 3.74 -> 3.28 after review and the lead ruling. Computed with the dao_contract weights in `scoring/weights.json`: 3(0.16) + 4(0.16) + 2(0.18) + 5(0.08) + 1(0.06) + 4(0.14) + 4(0.08) + 5(0.06) + 2(0.08) = 0.48 + 0.64 + 0.36 + 0.40 + 0.06 + 0.56 + 0.32 + 0.30 + 0.16 = 3.28. The change is -0.12 from integration, -0.16 from operations (D-4; 3.46 at that step, matching the DAO skeptic's `rescore.py`) and -0.18 from isolation (D3.9). This agrees with the lead's 3.28.

## 14. Open questions for the adversarial reviewers

1. The Windows compile failure rests on Go 1.26.0 stdlib source, not on a build. The section 11 step 4 probe would make it [executed]. A later Go version or `x/sys/unix` will not change it.
2. macOS behaviour of the POSIX driver is untested anywhere I could find. It should compile, and Go's `File.Sync` on darwin uses F_FULLFSYNC [hypothesis].
3. Do the GCP and AWS drivers, the client, fsck and OmniWitness compile and run on Windows? No OS-specific code was found in them (grep), so I infer they do [hypothesis]. The witness CI covers only ubuntu and macOS.
4. Is the `LogStateTracker` equal-size behaviour (`client/client.go:397-399`) a deliberate tolerance for cached reads or an oversight? Either way it is undocumented, and the security reviewer should judge whether it matters when the verifier is project-owned.
5. The #1098 fsck hang was confirmed by reading the code, not reproduced. Mismatches near the end of the log do return cleanly, per the issue text.
6. Would the public witness network accept a low-volume DAO log? Its admission policy was not read. If not, the "outside witness" must be a partner organisation.
7. The anchor cost per memo and the RPC reliability are unmeasured. The ChartRunner verifier tests were not run, and its claims of zero dependencies and devnet-only history come from the repository [inspected manifest; README reported].
8. Rekor v2's production use of Tessera is [reported]. The benchmark page and the Scorecard result were not opened.
9. Mechanism skeptic: DR-51's "any member can verify … aggregates" needs reproducible aggregate computation over private records. A commitments-only log proves inclusion and history, not the correctness of a weighted tally. That remains a custom replay design.
10. The comparison with hypercore was made from its repository at `9c9cc3d8` without reading its storage layer. The parallel hypercore dossier is authoritative on its fork and truncation semantics and its Windows native prebuilds.
11. (Added at amendment.) Recruiting three non-custodian witnesses for a low-volume DAO log is unverified. With fewer, the safe fallback is `quorum EA` (all of one outside witness), which costs availability.
12. (Added at amendment.) Whether the member ledger key in section 7 is stable (countable per pseudonym, a DR-32 tension) or rotated per epoch (more client complexity) is a DAO design choice. CONTESTED for Gate 3 (D3.9).

### Review responses (2026-10-21)

Amender: s3-amend-tessera. Every row was checked against the clones at the dossier SHAs (Tessera `012e9e0`, formats `82dcf1c`, witness `ea1ba4f`, C2SP `e5746a0`, ChartRunner `bed935b`). No line drift or failed citation was reported for this dossier: the archaeologist's spot-check passed 9 of 9. The vector counts were re-run (section 2 gives the command).

| Id | Verdict | Change made (section) or evidence for dispute |
|---|---|---|
| S-transparency-dev-tessera-1 | accepted, but the proposed remedy is corrected | The contradiction is real, and "1 of 3" is withdrawn (sections 7 and 8). The suggested "log key AND (1 of the outside group) AND (1 of any)" is also unsafe when the outside group has more than one member: two disjoint honest outside witnesses can each cosign a different fork. Section 7 now gives the policy file `group outside 2 EA EB EC` with the intersection rule 2k - n > f. Acceptance fault 3(e) added, including a control case under `any` that shows the failure. R30 isolation re-checked: stays 3 (section 13). |
| S-transparency-dev-tessera-2 | accepted | Section 7 entry envelope: domain-separated message `"resonantdao-ledger/v1" \|\| origin \|\| type \|\| epoch \|\| commitment`, wallet signing only through an off-chain-message format, and a negative fixture 3(h). The Solana off-chain format detail is labelled [hypothesis], because it was not inspected in this study. |
| S-transparency-dev-tessera-3 | accepted | The attacker model is stated in section 5 (R11 row) and in the section 13 R11 isolation reason. No score change: clause (c) rates the upstream artifact, whose tamper tests stand. |
| S-transparency-dev-tessera-4 | accepted | Section 8 anchor rule (1): separate anchor key, held off the log host by a different custodian, under DR-48. Verifiers check the signer (`ChartRunner_chartrunner-onchain/SPEC.md:132-137`). |
| X-2 (security) | accepted | Same change as S-3. |
| X-6 (security) | accepted, no score change | Section 8: the `POST /add` listener runs only on the DAO host, behind envelope authentication, never beside the bridge. R11 embeds no Tessera and so adds no listener. Whether added surface is scored (W-5) is the lead's. |
| X-9 (security) | accepted | Same change as S-2. |
| TM-3 (security) | lead's; no score change | The dossier now states which half of the split property R11 delivers by default (section 5). |
| TM-9 (security) | lead's; no score change | Section 7 treats the witness operator and the distributor as trusted infrastructure. The acceptance policy limits that trust to one colluding outside witness. |
| D-transparency-dev-tessera-1 | accepted, but the proposed remedy is corrected | As S-1. The publication policy and the acceptance policy are now separated (section 7), and the acceptance policy is pinned in the member verifier, per `C2SP_C2SP/tlog-policy.md:13-17`. The suggested "1 of external AND 1 more" has the disjoint-quorum flaw. Section 8's original sentence "cannot be shown a split view unless k witnesses collude" was wrong and is corrected. |
| D-transparency-dev-tessera-2 | accepted | Omission is now a property row in section 5: not designed upstream. Section 7 adds signed receipts on the durably assigned index (`append_lifecycle.go:222-243`), on the model of the static-ct-api `leaf_index` SCT (`C2SP_C2SP/static-ct-api.md:122-135`). A misbehaviour proof and a delay proof are defined, and out-of-band filing covers a refused receipt. Acceptance fault 3(f) added. The remaining risk (refusal to issue a receipt) is stated in section 12. |
| D-transparency-dev-tessera-3 | partly accepted | Accepted: signed, typed public envelopes, so counts per type and epoch are auditable and a claim in a real member's name needs that member's key. An independent auditor with access to the store is added (section 7), with fault 3(g). Not accepted as fixable by the log: phantom members built from custodian-generated keys cannot be detected by any log. That is R25, and it is stated as a residual risk (sections 5, 8 and 12). requirement_fit stays 3: the dossier already credited no membership semantics. |
| D-transparency-dev-tessera-4 | accepted | Section 13 dao_contract: integration_effort 3 -> 1, because the anchor names the language runtime the team does not have, consistent with the os_kernel row. operational_complexity 4 -> 2: one process, static sync and an anchor job, with publication depending on outside witnesses; the operator now runs no witness. Total 3.74 -> 3.46 at this step; 3.28 after the D3.9 isolation change (TM-3 row). |
| D-transparency-dev-tessera-5 | accepted | Section 7: the member client keeps the record, salt, receipt and proof. A presumption in the member's favour when the store cannot produce a record is left to governance under DR-26. |
| D-transparency-dev-tessera-6 | accepted | Section 8 anchor rules (2)-(4): only checkpoints that satisfy the policy are anchored, the cadence is published, a missed memo raises an alarm, and successive anchors are checked for consistency. |
| D-transparency-dev-tessera-7 | accepted | STATUS line added to the header. |
| C-1 (DAO) | lead's; noted | After D-4 the dao_contract total is 3.46. Any rank against identity-common-ts depends on that dossier's amended total and on the sensitivity rule fix. |
| C-2 (DAO) | lead's; no change here | The skeptic's capture-weighted profile gives this dossier 3.40. The proposed authority_and_capture criterion would score this dossier's acceptance policy, receipts and key separation, all now specified in sections 7 and 8. |
| C-3 (DAO) | accepted | The property check now names the full condition under which cosignatures give split-view resistance (verifier enforcement, quorum intersection, an honest witness in the intersection), with fault 3(e) to break it (section 5). |
| C-4 (DAO) | partly accepted | Section 7 notes that the R30 log can carry one governed revocation record with the DR-06 fields. Whether all derived artefacts should come from it is a cross-dossier decision for the lead. |
| C-5 (DAO) | accepted | Omission (D-2) and split view across disjoint witnesses (D-1) are now property rows in section 5, with faults 3(e) and 3(f) in section 11. |
| C-6 (DAO) | accepted | Section 5 states that the log vouches for no human/AI split. T13 and T20 stay open. |
| C-8 (DAO) | accepted | STATUS line added. |
| TM-3 (DAO) | lead's; adopted as T24 (threat model v0.2, D3.9), which changes the score | Omission is now a checked R30 property, and upstream has no mechanism for it (clause (d): 1 at most for that property). Section 13 R30 isolation 3 -> 2, total 3.46 -> 3.28. |
| D-identity-common-ts-5 (names this dossier) | partly accepted | The section 7 registry design (signed join, revoke and recover entries) can serve R23's off-chain registry and inclusion proofs. Adding R23 to this row's requirement_ids and scoring it is the lead's decision. |
| Archaeologist cross-cutting 6 | accepted | STATUS line added. |
| Archaeologist spot-check (9 citations) | no objection | 9 of 9 PASS. No change. |

Items raised for the lead, with rulings (state.md D3.9):
1. **Remedy for S-1 and D-1: settled.** The article quotes `group outside 2 EA EB EC` (2 of 3 outside witnesses). The reviewers' "1 of outside AND 1 more" is kept in section 7 only as the rejected alternative, with the reason.
2. **Omission as a checked property: settled.** It is adopted as T24 in threat model v0.2. R30 isolation_and_security 3 -> 2, and the dao_contract total 3.46 -> 3.28 (section 13).
3. **Pseudonymous ledger key versus DR-32 (question 12): CONTESTED for Gate 3.** Per-member counts are auditable only if entries are linkable per pseudonym, and that linkage is the ranking surface DR-32 forbids. Unresolved. Neither the stable-key nor the per-epoch-key option is adopted in this dossier.
