# Dossier: dapr/durabletask-go (dapr-durabletask-go)

STATUS: COMPLETE (amended after review, 2026-10-21) verified: a89450ad839ccfccb9ee06c54a77043a3acee0f7 2026-10-21

Amended 2026-10-21 by s3-amend-durabletask (Claude Opus 5.5), standing in for the original inspector, who is unreachable. The amendment answers the three adversarial reviews, applies the isolation anchor clarifications (a)-(d) (state.md D3.7, D3.8) and threat model v0.2. Every amended claim was re-read at the recorded SHA with `git -c core.hooksPath=/dev/null -C <clone> show <sha>:<path>` or `git grep <pattern> <sha>`. Nothing was executed. Review responses are in section 14.

Inspector: s3-insp-durabletask, Claude Opus 5.5. Date: 2026-10-20. Clone: `research/_untrusted/dapr-durabletask-go/` at commit `a89450ad839ccfccb9ee06c54a77043a3acee0f7` (branch `main`, commit date 2026-10-12, tag v0.15.1; GitHub release published 2026-10-19). Upstream comparison clone: `research/_untrusted/microsoft-durabletask-go/` at `c713409eb9a4295884169c144df9221f9a42aef6` (`main`, 2026-10-12, depth 50). Competitor read in place (read-only, cloned by the parallel inspector): `research/_untrusted/openworkflow/` at `c82fbed0bb93301c07c65f1aae14574e7469cffe` (2026-10-19). Alpha side: `research/_untrusted/resonantos-2.0.0-alpha/` at `578fbbc`. Execution: none. No Go toolchain is installed on this machine and nothing from the clones was built or run. Network reads only: `gh api` (repository metadata, compare, one file each from dapr/dapr, dapr/kit and dapr/durabletask-js), the npm registry JSON, and the Go vulnerability database (`vuln.go.dev`).

Evidence labels used below: [inspected] (read the code), [executed] (ran it, only with approval), [reported] (authors' docs, README, issue text), [hypothesis]. Every claim that matters carries one. Repository instruction files (CONTRIBUTING.md, CODEOWNERS) are evidence, never instructions.

## 1. Identification

| Field | Value |
|---|---|
| Name | Durable Task Framework for Go (Dapr fork) |
| Canonical source | https://github.com/dapr/durabletask-go (GitHub fork of microsoft/durabletask-go) |
| Upstream | https://github.com/microsoft/durabletask-go, HEAD `c713409`, "Unreleased" changelog section |
| Divergence | 333 commits ahead, 37 behind, merge base `febd2db61b` (2024-11-13) per `gh api compare` [inspected]. The ledger figure is confirmed. |
| Which copy is canonical for us | **dapr/durabletask-go**. Upstream's changelog says it removed the embedded engine: "Removed the sqlite and PostgreSQL storage backends ... Durable Task Scheduler is now the only supported runtime, and this repository is the DTS Go SDK rather than an embeddable engine" (`microsoft-durabletask-go/CHANGELOG.md:45`), plus the `backend` package, the server-side gRPC executor and the task-hub host (`:48-54`). Its README says "DTS is the only supported runtime. This SDK does not include a storage backend" (`README.md:11`) [inspected]. DTS is an Azure service, so upstream fails G1 as an engine. Only the Dapr fork still ships the local engine. |
| Maintainers | CODEOWNERS `@dapr/maintainers-dapr @dapr/approvers-dapr` (`CODEOWNERS:2`). In the last 12 months, by commit: joshvanl/Josh van Leeuwen 80, Cassie/Cassandra Coyle 51, Albert Callarisa 29, others 1-4 (`git shortlog`, 178 commits) [inspected] |
| Release | v0.15.1 (tag on `a89450a`, 2026-10-12; published 2026-10-19). Twelve tags since 2025-10-03, from v0.10.1 to v0.15.1 [inspected] |
| Go module | `github.com/dapr/durabletask-go`, `go 1.26.0` (`go.mod:1-3`) |
| Wire protocol | `TaskHubSidecarService` gRPC, protos from the submodule `dapr/durabletask-protobuf` (`.gitmodules`), generated code in `api/protos/` |
| Node client | `@dapr/durabletask-js` 1.0.0 (MIT, published 2026-03-27, deps `@grpc/grpc-js`, `google-protobuf`). Its repo dapr/durabletask-js was last pushed 2026-03-27 and has 2 stars [inspected via npm and `gh api`]. `@dapr/dapr` 3.18.0 depends on it. `@microsoft/durabletask-js` 0.4.0 targets Azure DTS [reported]. |
| Licence | Apache-2.0. `LICENSE` is 201 lines with an appendix reading "Copyright 2024 Microsoft Corporation". There is no NOTICE file. Upstream switched from MIT to Apache-2.0 in `eb9ca44` (2024-05-02, "Switch from MIT to Apache 2.0 License (#66)"). Newer files carry "Copyright 2026 The Dapr Authors", Apache-2.0 headers (e.g. `backend/historysigning/signer.go:1-12`). Some older files have no header at all (`backend/sqlite/sqlite.go:1`) [inspected] |
| DOI / paper / SWHID | none found |
| Docs language | English. Dapr is a CNCF project with an English-speaking community [reported] |
| Issue tracker | **Disabled** on the fork (`has_issues: false`). All 10 "open issues" are pull requests [inspected via `gh api`]. Bug reports presumably go to dapr/dapr [hypothesis]. |

## 2. What works

Engine features, from the code [inspected]:

- **Orchestration replay and checkpointing.** Each orchestration turn loads history and new events, runs the orchestrator, and commits the new history, outbound events and new activity tasks in one SQLite transaction (`backend/sqlite/sqlite.go:203-411`, `CompleteWorkflowWorkItem`). Duplicate resolution events (TaskCompleted, TaskFailed, TimerFired, child completion) are dropped on append (`backend/orchestration.go:345-352`; detector in `backend/runtimestate/dedup/key.go:39-57`; tests `TestOf`, `TestSet_Add`, `TestIsPresent` in `backend/runtimestate/dedup/dedup_test.go`).
- **Work-item leasing.** Instances and activity tasks are leased with `LockedBy` and `LockExpiration`; the default lease is 2 minutes (`sqlite.go:55-62`, `:851-870`, `:1010-1023`). After a crash, the lease expires and another worker (a new process gets a new `workerName`, `:66-76`) picks the item up again. `ActivityLockTimeout` is declared but never read: activity leases use `WorkflowLockTimeout` (`sqlite.go:1010`; grep shows no other use) [inspected]. This is a minor defect.
- **Durable timers.** A timer is a `NewEvents` row with a future `VisibleTime` (`sqlite.go:333-345`), selected only once visible (`:861`, `:890`). Tests: `Test_ScheduleTimerTasks` (`tests/backend_test.go`), `Test_SingleTimer`, `Test_ConcurrentTimers`, `Test_ExternalEventTimeout` (`tests/orchestrations_test.go`), `Test_ExternalEvent_RaisedBeforeTimeout_SurvivesStaleTimerFired` (`tests/external_event_stale_timer_test.go`).
- **External events, the approval-wait primitive.** `WaitForSingleEvent(name, timeout)` and `RaiseEvent` (README:143-176). Tests: `Test_ExternalEventWorkflow`, `Test_ExternalEventContention`, `Test_Workflow_Select_ExternalEventRace` (`tests/grpc/grpc_test.go:685`).
- **Retries with a stable task execution ID.** `CallActivity(..., WithActivityRetryPolicy)` mints one `TaskExecutionId` per logical call and reuses it across attempts (`task/orchestrator.go:398-410`, `:525-536`). It travels in the `TaskScheduled` event that is persisted and redelivered (`backend/executor.go:293-303`) and is exposed to activities as `ActivityContext.GetTaskExecutionID()` (`task/activity.go:133-136`). Test `Test_TaskExecutionId` (`tests/orchestrations_test.go:1619-1663`) asserts that three attempts see one ID.
- **Instance-ID uniqueness**, usable as a job idempotency key: `INSERT OR IGNORE` and `api.ErrDuplicateInstance` (`sqlite.go:466-520`). Tests: `Test_SingleActivity_EnforceUniqueInstanceID`, `Test_SingleActivity_ReuseInstanceIDError` (`tests/orchestrations_test.go:1534-1612`) and the gRPC twins `Test_Grpc_EnforceUniqueInstanceID` and `Test_Grpc_ReuseInstanceIDError`.
- **Suspend, resume, terminate, purge, continue-as-new, child workflows, versioning by patching.** Tests: `Test_SuspendResumeWorkflow`, `Test_TerminateWorkflow*`, `Test_PurgeWorkflow_Recursive`, `Test_ContinueAsNew*`, `Test_WorkflowPatching_*` (seven tests).
- **gRPC sidecar.** `main.go:16-57` wires SQLite, `NewGrpcExecutor`, workflow and activity workers and `grpc.NewServer()` on `localhost:4001`. The service exposes 17 RPCs, including `StartInstance`, `RaiseEvent`, `TerminateInstance`, `GetWorkItems` (a server stream) and `CompleteActivityTask`. `CompleteOrchestratorTask` remains as a deprecated alias of `CompleteWorkflowTask` (`backend/executor.go:686-694`). Worker-stream redelivery is tested in-process: `TestGetWorkItems_DisconnectRedeliversBufferedItem` and `TestGetWorkItems_SendFailureRecoversWorkItem` (`backend/executor_stream_test.go:181, 388-485`).
- **History signing library** (`backend/historysigning/`, 3,805 lines including tests). See section 5 for what its tests assert. **It is not wired into any backend in this repository**: outside its own package, `historysigning` is referenced only for `MarshalEvent` (`backend/runtimestate/propagation.go:79`). `Sign` and `VerifyChain` are called by dapr/dapr (`pkg/actors/targets/workflow/orchestrator/signing/*.go`, `pkg/runtime/wfengine/state/state.go`, found by `gh api search/code`) [inspected]. The SQLite backend stores unsigned protobuf blobs (`schema.sql:25-31`).

Tests and CI: 394 `func Test*` across 39 test files [inspected; recounted 2026-10-21 with `git grep -E "^func Test" <sha> -- '*_test.go' | wc -l` (394) and the same with `-l` (39); the seven patching tests with `^func Test_WorkflowPatching_`; the 3,805 signing lines by concatenating every file under `backend/historysigning/`; the 17 RPCs as 16 `MethodName` entries plus 1 `StreamName` (`GetWorkItems`) in `api/protos/orchestrator_service_grpc.pb.go`]. CI is `.github/workflows/pr-validation.yml`: `runs-on: ubuntu-latest` (`:26`), matrix Go `1.23.x` (`:29`) against `go 1.26.0` in go.mod (setup-go will fetch the newer toolchain [hypothesis]), a Postgres 13 service container, `go test -race` for unit (`:79`) and integration tests (`:84`). There is no Windows or macOS lane [inspected].

What the tests do **not** cover [inspected]: every orchestration-level integration test runs on **in-memory** SQLite (`initTaskHubWorker`, `tests/orchestrations_test.go:2231-2249`, `NewSqliteOptions("")`; gRPC suite `tests/grpc/grpc_test.go:45-47`). The file-backed backend (`tests/backend_test.go:27-35`) is exercised only within one process. No test kills a process, reopens a database after a crash, expires a lease held by a dead worker, or simulates a torn write. grep for crash, restart, kill and LockExpiration in `*_test.go` finds only panic-recovery tests (`backend/activity_panic_test.go`, `backend/orchestration_panic_test.go`).

Deployment evidence: the engine is the basis of Dapr Workflow (README:9). Dapr runs it on its actors state-store backend, not on this SQLite backend [inspected via the dapr/dapr paths above]. No named production user of the SQLite backend or of the standalone sidecar was found [reported absence].

## 3. Maturity

- **Footprint.** One Go process. It uses SQLite through `modernc.org/sqlite v1.34.5` (pure Go, no cgo) with `SetMaxOpenConns(1)` (`sqlite.go:115`). No `PRAGMA` is set anywhere, so SQLite defaults apply (rollback journal, `synchronous=FULL`) [inspected by grep; the defaults are SQLite's documented behaviour, reported]. Binary size and startup time are **not measured**: no toolchain, and no build is allowed without approval. A Go binary with grpc, protobuf, otel and modernc SQLite is plausibly 20-35 MB with startup well under a second [hypothesis; see section 11].
- **Cadence.** 178 commits from 2025-10-20 to 2026-10-20, every month except 2026-02, with a peak of 45 in 2026-04 [inspected]. Releases about monthly (v0.11.0 2026-01-30 to v0.15.1 2026-10-12). Still pre-1.0, and API renames ship with deprecated aliases (`backend/deprecated.go`).
- **Bus factor.** Two people wrote about 74% of last year's commits (131 of 178). The fork is maintained by the Dapr org [inspected].
- **Issue response.** Cannot be sampled because issues are disabled on the fork. The open PRs date from 2025-11-28 (#57 WIP) to 2026-10-16 (#143) [inspected].
- **Security posture.** No GitHub security advisories (`gh api .../security-advisories` returns 0) [inspected]. `SECURITY.md` is the stale Microsoft MSRC template ("report it to the Microsoft Security Response Center"), so the fork has **no fork-specific disclosure process** [inspected]. No audit was found.
- **Dependency advisories (disconfirmation; the ledger missed these).** Querying `vuln.go.dev` against the pins at HEAD (`go.mod` last changed 2026-05-26, commit `34ea975`) [inspected]:
  - `google.golang.org/grpc v1.79.3` (`go.mod:18`): GO-2026-6061 (HTTP/2 transport server and xDS RBAC, fixed 1.82.1, published 2026-07-27) and GO-2026-6348 (OOM via HTTP/2 DATA fragmentation, fixed 1.83.1). Both list `internal/transport.NewServerTransport` among the affected symbols, and any `grpc.Server` reaches it, including the sidecar (`main.go:27, 39`). So both are reachable by construction [hypothesis until `govulncheck` runs]. **Corrected on amendment:** GO-2026-6443 (server panic on missing authority, fixed 1.82.2) affects only "servers configured with xDS routing" (advisory text; symbol `internal/xds/server.RouteAndProcess`), and GO-2026-6441 (xDS RBAC header matching, fixed 1.83.1) affects only the xDS RBAC filter. `git grep "grpc/xds\|xds\." <sha> -- '*.go'` finds nothing, so neither is reachable from this module [inspected]. The original text called 6443 reachable; that was wrong.
  - `golang.org/x/text v0.35.0` (`go.mod:17`): GO-2026-5970 (infinite loop in `unicode/norm` on invalid UTF-8, fixed 0.39.0). The only importer is `backend/historysigning/attestation.go:24`, which the SQLite sidecar does not call (section 2), so it is unreachable in the configuration proposed here [inspected]. GO-2026-6629 (`x/text/secure/precis` panic, fixed 0.41.0): no importer of `secure/precis` exists (`git grep`), so it is unreachable [inspected].
  - `golang.org/x/net v0.52.0` (`go.mod:43`, indirect) and the Go 1.26.0 standard library: GO-2026-5942 (DNS SVCB parsing, fixed x/net 0.56.0 and Go 1.26.6), and the HTTP/2 advisories GO-2026-6603, 6610, 6611, 6612 and 6617 (memory, CPU, flow control and HPACK race, fixed in x/net 0.60.0 and Go 1.26.9, published 2026-10-08). Whether gRPC's own transport reaches the vulnerable x/net `http2` symbols needs `govulncheck` [hypothesis]. `github.com/go-jose/go-jose/v4 v4.1.3` (`go.mod:28`, indirect): GO-2026-4945 (JWE panic, fixed 4.1.4); no `.go` file imports go-jose (`git grep`), so it is unreachable from this module's own code [inspected].
  - Advisory source: the `vuln.go.dev` JSON saved by the original inspector (`<prior scratchpad>\s3-insp-durabletask\GO-*.json`, 13 files), re-read on amendment with a `python -I` summariser.
  - **What they affect.** Every reachable advisory is an availability fault (OOM, CPU, panic) or an HTTP/2 framing issue on the sidecar's listener. None makes a crash undetectable, makes a committed transaction partial, or lets a forged history verify. That is why section 13 counts them under the component-surface and supply-chain property (T6, threat model v0.2 section 4) rather than as contrary evidence against the three checked properties (anchor clause (d)).
  - v0.15.1 shipped on 2026-10-19 with these pins, so dependency hygiene lags roughly three months. A consumer building its own `main` module can raise the versions (Go MVS), so the fix is in our hands, not theirs.
- **Documentation.** The README is the upstream one and partly stale: it lists no JS SDK and says "More language SDKs are planned" (README:65). `CHANGELOG.md` stops at v0.6.0 (2025-02-05) [inspected]. The library code is well commented.
- **Upgrade hazard.** `task/orchestrator.go:525-533` documents a retry-semantics change: "histories it recorded in either state do not replay". Minor releases can therefore strand in-flight histories [inspected]. For a desktop with multi-day timers, an upgrade needs a drain-or-pin policy.

## 4. Architecture

Control flow, sidecar mode [inspected]: `main.go` → `sqlite.NewSqliteBackend` → `backend.NewGrpcExecutor(be)` registers `TaskHubSidecarService` → `NewWorkflowWorker` and `NewActivityTaskWorker` poll `NextWorkflowWorkItem` and `NextActivityWorkItem` → the executor pushes `WorkItem`s onto one shared channel (`backend/executor.go:54, 139, 350, 602`) → every client holding a `GetWorkItems` stream competes for them → the client (Go, .NET, Java, Python or JS SDK) replays the orchestrator **in its own process**, returns actions with `CompleteWorkflowTask` and `CompleteActivityTask` → the backend commits.

- **Who runs orchestration code.** In sidecar mode the language SDK replays, so in our case the determinism rules belong to `@dapr/durabletask-js` in Node. The Go side stores history, leases work and fires timers.
- **Storage.** Four tables, `Instances`, `History`, `NewEvents` and `NewTasks` (`schema.sql:1-54`). Payloads are protobuf BLOBs, so the store is not human-readable.
- **Lifecycle.** `CreateTaskHub` panics on open or schema failure instead of returning an error (`sqlite.go:100-109`). `Start` and `Stop` are no-ops (`:1158-1165`). Executor `Shutdown` cancels pending work (`executor.go:436-460`). After an unclean exit, recovery waits for lease expiry (2 minutes by default).
- **Cancellation.** `CancelActivityTask` is called only from executor `Shutdown` (`executor.go:447`; grep). Terminating an orchestration does not stop an activity already running in a worker: its late result is discarded [inspected; discard by dedup and terminal state is an inference].
- **Auth and identity.** None. `grpc.NewServer()` has no credentials or interceptors (`main.go:27`; grep for `grpc.Creds`, `credentials.` and `Interceptor` outside tests finds nothing). The Dockerfile binds `0.0.0.0` (`Dockerfile:18`). Any local process that can reach the port can start, raise, terminate or purge, or open a second `GetWorkItems` stream and **receive activity inputs and forge their results** [inspected; impact is an inference].
- **Signing identity.** `historysigning` uses `dapr/kit/crypto/spiffe/signer` (`signer.go:24`). Its `New(svidSource x509svid.Source, trustAnchors)` takes any X.509 SVID source and signs with Ed25519, ECDSA or RSA (dapr/kit v0.18.0 `crypto/spiffe/signer/signer.go:43, 181-188`, fetched via `gh api`). The tests supply a static self-signed source and fake trust anchors (`historysigning_test.go:44-55`), so the library runs **offline without SPIRE** [inspected]. The Stage 2 note that "SPIFFE is too heavy" is therefore only partly right: SPIRE is not needed, but X.509 and SPIFFE URI SAN conventions are.
- **Dependencies (direct).** grpc, protobuf, `modernc.org/sqlite`, `jackc/pgx/v5`, `dapr/kit`, `spiffe/go-spiffe/v2`, OpenTelemetry (otel, sdk, trace, zipkin exporter, otelhttp), `x/text`, backoff, uuid, testify (`go.mod:5-21`). Zipkin is used only in `samples/distributedtracing`, and no telemetry is exported by default (grep) [inspected].

## 5. Direct relevance

**R10, durable job execution with checkpoint, replay and idempotent side effects (P0).** This is what Alpha lacks:

- OSC-21: resume loses planner history; `side-panel-scheduled-browser-job-runner.js:241-247` passes `history: []`.
- OSC-22: jobs live in `chrome.storage.local` and go `running|approval → paused` on panel load (`side-panel-browser-job-controller.js:34-43`).
- OSC-33: cancel rewrites status without killing.
- OSC-42: no supervised recovery.
- os-map section 7: the agent loop runs in the side-panel page, not in the bridge.

durabletask-go supplies a persisted event history (replay restores planner state), durable timers, external events for approval waits, at-least-once activity delivery with a stable `TaskExecutionId`, and instance-ID deduplication. It does **not** supply idempotent side effects (no engine can for a browser click), a kill on cancel, or anything browser-specific. All of that is the custom layer (section 7).

**R11, tamper-evident ledger and approval ledger (P0).** This would apply to the missing `Logs/audit-ledger.jsonl` (ADR-022), OSC-47 (no route requires an approval proof; the archive gate is a no-op, `archive-review-policy.mjs:27-31`) and os-map seam 3. `historysigning` offers a signed, hash-linked chain over event batches. It is a **library pattern only**: it is not used by the SQLite backend, it has no inclusion proofs (R11 asks for them), and storage is not user-readable.

Threats (threat model v0.2): T7 (crash during an uncertain side effect, duplicate or lost action) and T8 (torn write) via R10, and T5 (silent corruption of the knowledge boundary) via R11 (approval records for promotion). v0.2 adds three threats that the proposed integration touches, though the engine does not close them:
- T1, whose closure is now "R10 with indeterminate outcomes routed to the human, never retried automatically";
- T21 (security-state tamper): the job database, the intent journal, the sidecar token, and the R11 key and head record are security state (A10);
- T22 (approval spoofing): an `approval:<key>` external event is an approval path.

Section 7 is amended for all three. They are not scored as properties of the upstream artifact (anchor clause (c)).

**Property check (threat-model section 4, v0.2 rows Durability and Approval and audit):**

| Property | Evidence in the repository | Verdict |
|---|---|---|
| Recovery after a crash during an uncertain side effect, with no duplicate | Delivery is lease-based and at-least-once: a crash after the effect but before `CompleteActivityWorkItem` commits (`sqlite.go:1056-1094`) redelivers the task after lease expiry. The stable key (`Test_TaskExecutionId`) and duplicate-completion dropping (`dedup` tests) exist. The redelivery mechanics are tested in `Test_AbandonActivityWorkItem` (`tests/backend_test.go:299-334`, explicit abandon, then the same `TaskScheduled` is re-fetched) and `TestGetWorkItems_DisconnectRedeliversBufferedItem`. The latter runs on `newFakeExecBackend` with workflow items that were queued but never started, so it shows no loss of queued work when a stream dies, not recovery during an effect (`backend/executor_stream_test.go:388-485`; amended). **No test kills a process mid-activity, and no test asserts that the side effect happened once.** | **Not demonstrated.** Designed for at-least-once plus a key. "No duplicate" must come from our layer's intent journal (section 7). Needs the fault-injection test in section 11. |
| Indeterminate outcomes go to the human, never to automatic retry (v0.2 Durability row) | After a lease expires, the activity task is re-selected with no bound: `getActivityWorkItem` takes any `NewTasks` row whose `LockExpiration` has passed and increments `DequeueCount` (`sqlite.go:1004-1023`). The work item it builds carries no delivery count or redelivery flag (`sqlite.go:1047-1052`), and no poison or dead-letter limit exists in the SQLite backend (grep for `DequeueCount`, `poison`, `deadletter`). An activity can recognise a redelivery only through its own record keyed by the stable `TaskExecutionId` (`Test_TaskExecutionId`). `WithActivityRetryPolicy` adds automatic retries on failure; it is optional. | **Not demonstrated: the mechanism is absent, not contradicted.** The engine has no notion of an indeterminate outcome. It re-invokes the activity body, which decides whether the effect runs again. In the proposed configuration that body is the intent-journal check (section 7), and `dispatchBrowserStep` sets no retry policy. No inspected path forces a second effect, so this is an absence under anchor clause (d), not contrary evidence. |
| Torn-write behaviour | Commits are single SQLite transactions (`BEGIN ... Commit` at `sqlite.go:208, 406`, `:1061, 1089`) under SQLite's default journal. No crash, power-loss or partial-write test exists in this repository. | **Not demonstrated here.** Atomicity is inherited from SQLite's own (externally tested) commit protocol [reported]. Needs the kill-during-commit test in section 11. |
| Ledger tamper detected | Library tests (`backend/historysigning/historysigning_test.go`): `TestTamperedHistoryDetection` (`:333-357`, edits one event after signing, asserts `VerifySignature` errors with "events digest mismatch"); `TestTruncatedChainDetection` (`:359-389`, drops the **root** signature, asserts "root signature"); `TestVerifyChainCoverageShort` (`:863-882`, events beyond the signed range, asserts "signatures cover events"); `TestVerifyChainContiguityGap` (`:833-861`); `TestWrongCertificateIndex` (`:391-419`); `TestCertificateExpiredAtEventTime`, `TestCertificateNotYetValidAtEventTime`; `TestVerifyChainWithWrongTrustAnchor`; propagation tests `TestVerifyPropagatedHistory_TamperedRawEvents` and `_RelabeledChunkRejected` (`propagation_test.go:129, 231`); attestation tests `TestVerifyChildRejectsTamperedPayload` and `TestVerifyChildRejectsTamperedSignature` (`attestation_test.go:435, 455`). | **Partly demonstrated, at library level.** Content tamper, head truncation, gaps and wrong certificates are detected. **Tail truncation is not**: removing the last N events together with their trailing signatures leaves a valid chain, because `VerifyChain` (`verify.go:154-241`) checks only internal consistency and has no external head or length anchor. `TestVerifyChainEmptyNoEvents` (`:884-887`) shows that an empty history verifies as OK. Dapr stores `HistoryLength` and `SignatureLength` in unsigned metadata in the same state store (dapr/dapr `state.go:693-695`) [inspected via `gh api`]. Own-history signatures bind no instance ID: `SignatureInput(prev, events, nil)` (`canonical.go:73-86`). Because the signing key would sit on the same disk as the database, anyone with user-level file access can re-sign [hypothesis, by construction]. **Attacker model (v0.2 split, security review X-2):** at most (a), tamper by a party that cannot read the key or rewrite the head. (b), a same-user attacker (V2, V3), is not met: neither this library nor the TypeScript port in section 7 has an external checkpoint by default. Not used as proposed: the SQLite backend does not sign (section 2), and section 6 reuses the pattern, not the code. |

Stage 2's summary "signed history chains with tamper and truncation tests" is therefore **optimistic in two ways**: the truncation test covers only head truncation, and none of it runs on the SQLite path we would use.

## 6. Reuse decision

**Decision: learn the pattern and reimplement for R11. Keep the engine as a fallback "wrap as sidecar" candidate for R10, under investigation pending the section 11 test. Do not adopt it now.**

Why this beats the alternatives in section 12:

- **R10.** The engine has the richest semantics on the shortlist: durable timers, external events, child workflows, patching, and gRPC SDKs in five languages. But for a Node 24 bridge it is a second process with no authentication, a Node client last released in March 2026 with 2 stars and an untested pairing with v0.15 (section 7), Linux-only CI, and dependency advisories at HEAD. OpenWorkflow (TypeScript, `node:sqlite`, in-process) costs less to integrate for the same core primitives (step memoisation, sleep, signals, child workflows). durabletask-go should be chosen only if OpenWorkflow fails the crash test and this engine passes it.
- **R11.** The signed-batch chain (`EventsDigest` with length prefixes, `SignatureInput` = H(prev ‖ events ‖ ctx), contiguity and coverage checks, and certificate validity at event time) is a clean design, about 400 lines including the NFC canonicalisation. Reimplementing it in TypeScript in the bridge and adding a head anchor is cheaper than embedding Go and SPIFFE conventions. It also closes the tail-truncation gap.

Hard gates:

| Gate | Result | Clause |
|---|---|---|
| G1 no mandatory cloud or telemetry | **pass** for dapr/durabletask-go: SQLite local, no default exporter (zipkin only in `samples/`) [inspected]. **Fail** for upstream microsoft/durabletask-go at HEAD (DTS, an Azure service, is "the only supported runtime") |
| G2 per-OS honesty | **pass, with a warning.** Pure Go plus modernc SQLite should cross-compile for windows, darwin and linux [hypothesis], but the project states no per-OS matrix and tests only on ubuntu. One concrete Windows hazard [inspected]: `DeleteTaskHub` sets `be.db = nil` without closing it, then calls `os.Remove` on the open file (`sqlite.go:122-139`). That succeeds on Linux and would fail on Windows with a sharing violation [hypothesis]. The failure is loud (an error is returned), not silent. |
| G3 licence | **pass.** Apache-2.0 file-level, compatible with the MIT Alpha when shipped as a separate binary or a dependency. See section 9 for the patent and NOTICE obligations. |
| G4 chain | n/a (not a DAO component) |
| G5 invariants | **pass, with conditions (amended for S-1, T22).** The engine holds no authority by itself. (1) The sidecar port must not become an unauthenticated path around human-only actions: a local process could `RaiseEvent("approval", ...)` or forge `CompleteActivityTask` unless our layer authenticates the channel (sections 7 and 8). (2) Authenticating the channel is not enough. An `approval:*` event is accepted only from a bridge route whose grant the agent principal never holds, and only with an R11 approval record made by a host-side ceremony (R19). In the Alpha, the planner, job runner and approval UI share one extension context and its tokens (OSC-02; os-map section 7), so without condition (2) the agent could approve itself. That ceremony and route are a Gate 3 architecture item (state.md D3.7, X-4). Until they exist, the durable job service may not use approval waits for human-only steps. |

## 7. Integration design (against os-map section 17 seams 3 and 1)

Process boundaries. The bridge (`browser-first/host/run-bridge-minimal.mjs`) spawns a `resonantos-durable` sidecar built from **our own** `main.go`, about 120 lines vendoring nothing. Our own main module also lets us pin the patched gRPC, x/text and x/net. It has three differences from the upstream `main.go`:

1. It listens on `127.0.0.1:0` and prints the chosen port on stdout.
2. A gRPC unary and stream interceptor requires a random bearer token minted by the bridge for each sidecar start. **Amended (S-3):** the token is written to the sidecar's stdin and read once at start, not passed in an environment variable. A same-user process can read another process's environment (`/proc/<pid>/environ` on Linux; the process environment block on Windows), and children inherit it [reported, OS behaviour]. Section 8 states the token's lifetime.
3. **Amended (X-1, T21):** the job database, the intent journal and the token go in the bridge-only, integrity-protected state location that Gate 3 is to define (state.md D3.7, X-1). That location is not `~/ResonantOS_User/state/`. In the Alpha, a delegated child writes the user state root through the bridge (OSC-45) and directly while unconfined (OSC-32), and the read-deny list covers only `ResonantOS_User/Secrets` (`browser-first/host/delegation-isolation.mjs:200-202`, re-read at `578fbbc`). Until that location exists, this is an open dependency of the R10 work, and section 11 tests it.

Named pipes or Unix sockets would be stronger. Node on Windows speaks named pipes, which Go needs `Microsoft/go-winio` for [hypothesis]. That is left for a later PR.

The Node side uses `@dapr/durabletask-js` (`@grpc/grpc-js`, pure JS) inside the bridge process. Whether it works against v0.15 is **unverified**. Its worker calls `hello`, `getWorkItems` and `completeOrchestratorTask` (dapr/durabletask-js `src/worker/task-hub-grpc-worker.ts:119-124, 248, 296`, via `gh api`). The Go server still implements the deprecated `CompleteOrchestratorTask` (`executor.go:690-694`) and accepts an empty completion token (`executor.go:317`) [inspected]. So the pairing is plausible but untested [hypothesis].

Data structures (sketch):

```
job instanceId   = "bj-" + <Alpha browser job id>      // dedup of job start (ErrDuplicateInstance)
orchestrator     = browserJob(goal, siteKey)           // replays planner history from the event log
activity         = planStep(history) -> decision      // model call, safe to repeat
activity         = dispatchBrowserStep(step, key)      // key = instanceId + "/" + TaskExecutionId
external event   = "step-result:<key>", "approval:<key>", "cancel"
timer            = ctx.createTimer(...) for backoff and scheduled jobs
```

Uncertain side effects need an intent journal; this is the smallest custom layer. Delivery is at-least-once, and a browser click has no server-side idempotency key. So `dispatchBrowserStep` must work as follows:

1. Write `intent(key, started)` to a bridge-side journal before handing the step to the extension.
2. The extension executes the step, then posts `step-result:<key>` through a bridge route.
3. If an activity is redelivered and the journal shows `started` without `done`, the step is **uncertain**. **Amended (S-2; threat model v0.2 T1 closure and Durability row):** the layer never re-executes an uncertain step automatically. What happens next depends on the step class:
   - **Irreversible steps** (submit, purchase, post, send; the human-only list, OSC-19 and OSC-20) go to the human through the approval path in G5 condition (2). The human sees the intent record, not only the page.
   - **Reversible steps** (navigate, scroll, read) may run an automatic read-only check, and that check may only conclude "done" or "ask the human", never "re-dispatch".

   Page-state verification cannot settle an irreversible step. Alpha's `snapshotFingerprint` is built from the page's title, URL, first 1,200 characters of text and control and field counts (`resonantos-side-panel-extension/src/lib/agent-control-runner.js:130-163`, re-read at `578fbbc`). All of that is content a malicious page (V1) controls, so it can present its pre-action state after the effect went through.

This, not the engine, is what makes "no duplicate" true, and only against a non-adversarial page for reversible steps.

Cancellation. `TerminateInstance` plus a `cancel` external event. The extension must poll a bridge cancel flag, because the engine does not stop in-flight activities (section 4).

Identity. The originating principal goes into the orchestration input and into every journal record. The engine carries no identity.

Error behaviour. If the sidecar is unreachable, the bridge reports jobs as "durability unavailable" and does not silently fall back to `chrome.storage`.

Versioning. Pin the sidecar and the JS SDK together. Drain or complete running instances before an upgrade (see the hazard in section 3).

R11. The TypeScript reimplementation of the chain lives in a new `browser-first/host/audit-ledger.mjs`: JSONL, user-readable, with batch signatures and a head record (count plus last signature digest) mirrored outside the ledger file. Privileged routes require a matching approval record (seam 3). The engine is not involved.

**Amended (S-4, X-2; v0.2 Approval and audit row):** with the key and head on the same machine as the ledger, the design meets tamper-evidence level (a) only: accidental corruption and parties who cannot read the key. An OS keystore does not change this against same-user processes (threat model T9 as amended). Level (b), against V2 and V3, needs an external checkpoint: a head exported to the user, or a witness (see the tessera dossier). It also needs the key and head in the Gate 3 bridge-only store (X-1). Threat model v0.2 requires (b) for anything that gates T1 or T22. The ledger therefore must not gate human-only routes until (b) exists.

Alpha files that change:

- `browser-first/host/run-bridge-minimal.mjs`: spawn and supervise the sidecar.
- New `browser-first/host/durable-job-service.mjs` and its routes in `browser-first/host/bridge-server.mjs`.
- `browser-first/host/bridge-capability-tokens.mjs`: new capability, for example `browser-job-durable`.
- `browser-first/host/bridge-shutdown.mjs`: stop the sidecar.
- `resonantos-side-panel-extension/src/lib/browser-job-store.js`: mirror state to the bridge.
- `resonantos-side-panel-extension/src/lib/side-panel-browser-job-controller.js:34-43`: ask the bridge instead of forcing `paused`.
- `resonantos-side-panel-extension/src/lib/side-panel-scheduled-browser-job-runner.js:241-247`: seed `history` from the durable record.

Alpha tests affected (the 2,424-test lane): `browser-first/test/browser-job-store.test.mjs` (`recoverInterruptedJobs` at `:740` and the "Recovered after browser host reload" assertion at `:744`), `side-panel-browser-job-controller.test.mjs`, `side-panel-scheduled-browser-job-runner.test.mjs`, `browser-job-scheduler.test.mjs`, `control-run-state.test.mjs`, `agent-control-runner.test.mjs`, `monitor-renderers.test.mjs`, and the vocabulary locks `bridge-capability-token-consistency.test.mjs` and `bridge-route-capability-audit.test.mjs` (a new capability and route).

## 8. Security and governance effects

- **New attack surface.** A second loopback listener speaking gRPC. Upstream has no authentication, so a malicious local process could start, terminate or purge jobs, inject `approval` events, or register as a worker and receive activity inputs, then return forged results (section 4). This lands squarely on T3 and R05. Mitigation: the token interceptor in our own `main.go`, loopback-only binding, and a later move to a named pipe or Unix socket with an ACL.
- **Vulnerable gRPC HTTP/2 transport at the pinned version** (section 3). Mitigated by pinning `grpc >= 1.83.2`, `x/net >= 0.60.0` and `x/text >= 0.41.0` in our module and building with Go >= 1.26.9, then running `govulncheck` in CI.
- **Component surface (X-6; v0.2 Component surface row).** The upstream sidecar violates the v0.2 property "no new listener without authentication": `grpc.NewServer()` has no credentials or interceptors (`main.go:27`), and the Dockerfile binds all interfaces. Our own `main.go` must add authentication. The listener must also be unreachable from confined children: R02 containment must deny the sidecar's loopback port the way it denies the bridge's. Its gRPC parser runs in the sidecar process, not in the bridge process that holds A1 and A2, which is the better side of that property. The bridge-side `@dapr/durabletask-js` client parses only responses from our own sidecar. Dependencies are pinned in our module (next bullet).
- **Revocation (amended, S-3).** A fresh token is minted for every sidecar start and delivered on stdin. Its lifetime is the sidecar's lifetime, and the bridge restarts the sidecar on bridge restart and on any supervision fault. A stolen token is therefore valid until the next sidecar restart, which is the same order of weakness as today's long-lived bridge tokens (T3). Shortening it would need per-call or periodically re-keyed credentials over the stdin channel, which is not designed here.
- **Isolation.** The sidecar runs as the user. It needs no admin rights and no network beyond loopback.
- **Security state (X-1, T21).** A child that can edit the job database or the intent journal can mark an uncertain irreversible step `done`, or `started` as never begun, and so cause a duplicate or a silent loss. The database, journal, token, R11 key and head record therefore belong in the Gate 3 bridge-only store, not the child-writable user root (section 7).
- **Personal data.** Job goals, page-derived inputs and model outputs persist in SQLite as protobuf BLOBs in the bridge-only store. They are not encrypted (relevant to T9 and R15) and not user-readable without tooling. Provide an export through `GetInstanceHistory` and set purge-on-completion policies.
- **Trust in maintainers.** Two primary authors, and no fork-specific SECURITY.md (it points to Microsoft MSRC). Upstream has abandoned the embedded mode, so if the Dapr maintainers ever drop the SQLite backend (Dapr itself does not use it) we would be the de facto maintainers of `backend/sqlite` [hypothesis about future direction].
- **Tamper evidence (R11).** Signing with a key stored next to the data gives evidence only against parties who cannot read the key. Tail truncation needs an external anchor. On a single-user desktop, an attacker with user-level access defeats both. **Amended:** an OS keystore (DPAPI, Keychain, libsecret) does not change this against same-user processes, because any process of the same user can read the item (threat model v0.2, T9). Only an external checkpoint or a separate OS account gives level (b) (section 7).
- **User friction.** No ceremonies, no network, no accounts.

## 9. Licensing

- SPDX: Apache-2.0 (`LICENSE`, full text, appendix "Copyright 2024 Microsoft Corporation"). There is no NOTICE file, so redistribution needs the licence text and a statement of changes for modified files (Apache-2.0 section 4) [inspected].
- Relicensing history: MIT to Apache-2.0 by the upstream maintainer in 2024 (`eb9ca44`), before the Dapr fork's merge base (2024-11-13). No mixed-licence code was seen.
- Transitive dependencies are permissive as far as known: modernc.org/sqlite BSD-3-Clause, grpc and protobuf Apache-2.0 or BSD-3, pgx MIT, go-spiffe and dapr/kit Apache-2.0, otel Apache-2.0, golang.org/x BSD-3 [reported from package knowledge; not verified from module files because no module cache exists]. SQLite itself is public domain [reported].
- Node client `@dapr/durabletask-js`: MIT (npm metadata) [inspected].
- Compatibility with the MIT Alpha: high confidence when shipped as a separate binary. Apache-2.0 section 3 patent-termination and section 4 notice obligations apply to redistribution of the sidecar binary.
- For independent legal review: (a) the Apache-2.0 patent clause against the proposed Symbiotic Licence (status F, unknown); (b) whether a reimplementation of `historysigning`'s design in TypeScript has to carry attribution. It is a pattern reimplementation, not a copy, but reviewers may want a clean-room note. This is technical research, not legal advice.

## 10. Cost and effort

| Scenario | Scope | Estimate (assumptions) |
|---|---|---|
| Small: R11 pattern only | TypeScript chain plus head anchor, about 400 lines plus tests, no Go | 1-2 developer-weeks [hypothesis] |
| Medium: R10 sidecar | Own `main.go` with auth and a version pin; cross-compiled binaries for win-x64, win-arm64, darwin and linux in CI; a bridge spawn and supervise module; durable-job service; intent journal; extension changes; acceptance tests | 4-8 developer-weeks. Needs Go in CI and someone able to read Go stack traces. The team today is JS/TS (master prompt 5.5 language cost). |
| Large: also signing on SQLite | A custom `Backend` wrapper that signs each committed batch, key in the OS keystore, head anchoring | another 3-5 weeks, and the Go fork-maintenance exposure grows |

Lock-in is moderate. The history format is protobuf and Durable-Task specific, and migrating away means draining jobs, since there is no export to a neutral format. Maintenance exposure: monthly pre-1.0 releases with renames, three months of dependency lag, and an upstream that has dropped the mode we use.

## 11. Acceptance test (a request for the user; it executes third-party code)

The run needs approval. Sandbox: a disposable Windows 11 VM plus an ubuntu container. Steps:

1. Build our `main.go` against v0.15.1 with Go 1.26.9 (`CGO_ENABLED=0`, `GOOS=windows|linux|darwin`). Record binary size and the time to the "listening" line.
2. Node 24 test harness with `@dapr/durabletask-js` 1.0.0. Orchestrator `crashProbe` calls activity `sideEffect(key)`, which appends `key` to an external file, sleeps 5 s, then returns.

Fault scenarios:

- **T7a.** Kill the sidecar (`taskkill /F` or `kill -9`) during the 5 s sleep, restart it, and wait.
- **T7b.** Kill the Node worker in the same window.
- **T8.** Kill the sidecar during a burst of 1,000 `StartInstance` calls, then open the database with `sqlite3 PRAGMA integrity_check`.
- **T3.** Connect a second, unauthenticated client and call `RaiseEvent` and `GetWorkItems`.
- **Windows paths.** A database path containing a space and non-ASCII characters under `%USERPROFILE%`.
- **T1/T22, self-approval (added for S-1).** The planner principal, holding every grant the agent loop holds, calls the route that raises `approval:<key>`, and separately calls `RaiseEvent` with a valid sidecar token.
- **T7 with an adversarial page (added for S-2).** A test page accepts a "submit" click, records it server-side, then restores its exact pre-action DOM. Kill the sidecar before `CompleteActivityTask`, restart it, and let the activity be redelivered.
- **T21, state tamper (added for X-1).** A delegated child with `archive-write` tries to edit the job database, the intent journal and the token, and to replace them with older copies.

Expected observable output:

- T7a and T7b: the workflow completes. The external file shows the key once or twice; the duplicate count is reported as at-least-once evidence. With the intent-journal layer enabled, the second delivery is classified `uncertain` and does **not** append.
- T8: `integrity_check = ok`, and every acknowledged `StartInstance` is present.
- T3: requests are rejected with `Unauthenticated` (our interceptor).
- Windows paths: the database is created at the exact path.
- Self-approval: both calls are refused. The route refuses because the agent principal holds no approval grant and presents no R11 record from the host ceremony. The sidecar token alone is not accepted for `approval:*` event names, which our interceptor reserves for the bridge's approval service.
- Adversarial page: the server-side record shows exactly one submit. The step is classified `uncertain` and goes to the human with the intent record shown, and it is not re-dispatched.
- State tamper: every write and every rollback is refused or detected before the next job step.

Pass/fail: all assertions hold on Windows and Linux, and `govulncheck ./...` on our module reports no reachable vulnerability. CI hook: a `durable-sidecar` job in the Alpha's workflow matrix (`windows-latest`, `ubuntu-latest`, `macos-latest`).

## 12. Recommendation and confidence

Benefits: a mature replay model (from the Durable Task Framework lineage); durable timers and external events, which give approval waits for free; a stable activity key; atomic SQLite commits; a polyglot gRPC protocol; and a well-built signing library to learn from.

Trade-offs: a Go sidecar for a JS team; no authentication on the wire; a thin, stale Node client; at-least-once delivery only; history that is not user-readable.

Blockers before adoption: the section 11 crash and Windows test, plus the authentication interceptor. **Amended:** three Gate 3 dependencies (state.md D3.7) also block adoption:
- the bridge-only state store (X-1, T21);
- an approval path the agent cannot drive (X-4, T22, G5 condition 2);
- the rule that uncertain irreversible steps go to the human (S-2).

None was a review blocker. The reuse decision and every hard-gate verdict are unchanged; G5 keeps "pass" with a second, stricter condition.

Ranking note: after the D3.6 correction, the R10 pair (openworkflow 3.08, durabletask 3.02) is FRAGILE in `scoring/sensitivity-output.md`. With isolation 2 -> 1 (section 13), durabletask falls to 2.80. The margin under openworkflow (3.08, isolation 1 kept by its amender, per the lead's note) widens to 0.28, and both now sit at isolation 1 under one T7 rule. The order and this dossier's recommendation (durabletask as the R10 fallback) are unchanged; `sensitivity.py` needs a rerun (lead).

Readiness: B, a capability that exists and is tested upstream, for the engine; C for the SQLite-sidecar-with-Node configuration we would actually run.

Evidence quality: the engine mechanics, tests, CI and gaps are about 80% [inspected]. Size, startup, Windows behaviour and JS-client compatibility are [hypothesis]. Vulnerability reachability is now split: the xDS, precis, norm and go-jose advisories are unreachable [inspected by import grep], and the gRPC transport and HTTP/2 advisories are reachable by construction [hypothesis until `govulncheck`].

Competitors compared on the same criteria:

| Criterion | dapr/durabletask-go | openworkflowdev/openworkflow | Temporal dev server | resonatehq/resonate |
|---|---|---|---|---|
| Runs in a Node 24 process | No: Go sidecar over gRPC plus `@dapr/durabletask-js` | Yes: TypeScript, `node:sqlite`, `engines node >=22.22.0` (`packages/openworkflow/package.json:82-84`) [inspected] | No: about 38 MB CLI sidecar plus a native SDK bridge [ledger, reported] | No: Rust server plus TS SDK [ledger] |
| SQLite durability | Single transactions, default journal | `PRAGMA journal_mode = WAL` (`packages/openworkflow/sqlite/sqlite.ts:59`) [inspected] | `--db-filename` optional; "not intended for production use" [ledger counterexample] | SQLite default store [ledger] |
| Crash test | none (panic tests only) | `worker/chaos.test.ts`: "workflow completes despite random worker deaths". It runs on the **Postgres** test backend, uses graceful `worker.stop()` rather than a kill, and asserts completion, not the absence of duplicates (`chaos.test.ts:2, 85-93, 59-62`) [inspected] | n/a | differential and linearisability tests per backend [ledger] |
| Windows | untested; CI ubuntu only | untested; CI ubuntu only (`.github/workflows/ci.yaml`) [inspected] | binary per OS [reported] | **no Windows server binary** in v0.9.8 [ledger counterexample, confirmed by Stage 2] |
| Signed history (R11) | library, not wired to SQLite; no tail-truncation detection | none found (grep) [inspected] | none | none |
| Idempotency | instance ID plus `TaskExecutionId` | run-level `idempotencyKey` (`client/client.ts:172, 282-295`) [inspected] | workflow ID | promise ID |
| Licence | Apache-2.0 | Apache-2.0 (`LICENSE.md`) [inspected] | MIT | Apache-2.0 |

Counterexamples. No counterexample row exists against durabletask-go itself (ledger `counterexamples: []`). The rows against the Temporal dev server and Resonate are confirmed as stated in the ledger and are why neither displaces this candidate. The `dapr-dapr` row ("Dapr.Workflow ... builds on the Dapr runtime sidecar") is out of scope: we would not run daprd, and this dossier's configuration is the standalone SQLite sidecar. New contrary evidence raised by this dossier: the dependency advisories at HEAD, the unauthenticated gRPC surface, an untested Windows path, and the gap in the R11 truncation test.

First PR, PR-sized, in the ResonantOS Alpha repository. Add `browser-first/host/audit-ledger.mjs` and `browser-first/test/audit-ledger.test.mjs`, a TypeScript-flavoured ESM port of the chain:

- `eventsDigest` with uint64 length prefixes, as in `canonical.go:38-47`.
- `signatureInput = sha256(prevDigest ‖ eventsDigest ‖ ctx)`.
- Ed25519 via `node:crypto`.
- A **signed head record** `{count, lastSigDigest}` written to a second file.

The tests should port `TestTamperedHistoryDetection`, `TestTruncatedChainDetection`, `TestVerifyChainContiguityGap` and `TestVerifyChainCoverageShort`, and add the missing **tail-truncation** and **empty-ledger** cases that must fail against the head. No route changes are needed, so the 2,424 locked test names are unaffected. The R10 sidecar work waits on section 11.

**Scope of the PR's claim (amended, S-4):** it delivers tamper-evidence level (a) only: accidental corruption and tamper by a party that cannot read the key or rewrite the head file. It does not claim detection against a same-user attacker (V2, V3). To make the head usable as an external anchor later, the PR also adds `exportHead()`, which writes the signed head as a short text the user can save elsewhere. Level (b), and placing the key and head in the bridge-only store, wait for the Gate 3 decisions (X-1, and an external checkpoint per the tessera dossier). Until then the module must not be wired as the approval record that gates a human-only route (v0.2: Phase 1 needs (b) for anything gating T1 or T22).

Confidence: **medium**. The code reading is direct and specific. The decisive R10 facts (crash behaviour on Windows, JS-client compatibility, binary size) need the approved run.

## 13. Scores (profile: os_kernel)

| Criterion | Score | Reason (anchor) |
|---|---|---|
| requirement_fit | 3 | R10 core primitives are present (replay, timers, events, stable key), but no idempotent-effect support and no browser fit. R11 is a library only, with no inclusion proofs and no tail anchor. |
| demonstrated_maturity | 3 | "Tests and releases but thin usage evidence" for the SQLite and sidecar path; Dapr's production use is on a different backend; pre-1.0; issues disabled. |
| isolation_and_security | 2 -> 1 (amended 2026-10-21 against clauses (a)-(d) and the lead's W-2 question) | Rates the upstream artifact in the configuration this dossier proposes: the SQLite backend behind our own sidecar `main.go`, with `historysigning` reused only as a pattern (clause (c); X-3). The checked properties are (1) recovery with no duplicate and indeterminate outcomes to the human (T7), (2) torn-write behaviour (T8), and (3) ledger tamper detected (R11). **No test in the artifact as used exercises any of them** (clause (b)). The nearest tests are helpers: `Test_TaskExecutionId` (stable key), `Test_DuplicateEvents`, `Test_RuntimeState_DuplicateCompletionSingleParentNotification` and the `dedup` tests (duplicate completions dropped from history, not duplicate effects), and `Test_AbandonActivityWorkItem` (explicit abandon, not a crash). `TestGetWorkItems_DisconnectRedeliversBufferedItem` (`backend/executor_stream_test.go:388-485`) runs on `newFakeExecBackend`, with workflow items that were queued but never started. No crash, lease-expiry or torn-write test exists. What remains is absent mechanisms (no indeterminate state, no delivery count to the activity, no history integrity on SQLite) plus untested design (single SQLite transactions). Clause (d) caps that at 1. The earlier 2 rested on helper tests, which clause (b) does not credit; on the same rule, openworkflow's 1 is consistent (W-2). Why not 0: no verified finding defeats a checked property in that configuration (clause (d)). The reachable gRPC and x/net advisories (GO-2026-6061, 6348; x/net and Go 1.26.x HTTP/2) are availability faults on the listener, and the tail-truncation acceptance in `VerifyChain` lies in code this dossier does not propose to use. Named sub-reason (W-5, not scored): the upstream sidecar adds an unauthenticated listener, and the release pins vulnerable gRPC, x/net and Go versions, so it fails the v0.2 Component surface row until our `main.go` fixes both. |
| licence_suitability | 5 | Apache-2.0 file-level; permissive transitive dependencies. |
| integration_effort | 2 | Below the 3 anchor ("sidecar with stable protocol"): the protocol is pre-1.0, the Node client is thin and its compatibility unverified, and Go is a runtime and toolchain the team does not have. |
| maintenance_sustainability | 3 | Active monthly releases, but a bus factor of about 2, a stale SECURITY.md and CHANGELOG, three months of dependency lag, and an upstream that dropped the mode. |
| sovereignty_and_portability | 4 | Local-first, no account, SQLite file under the user root; history is protobuf BLOBs, not user-readable. |
| interoperability | 4 | The Durable Task gRPC protocol is shared by .NET, Java, Python, Go and JS SDKs; OpenTelemetry. |
| operational_complexity | 3 | "One sidecar" plus embedded SQLite, with no external services. |

The weighted total under os_kernel is **3.02 -> 2.80**, reported for information; it is not the decision. Recomputed on amendment with the os_kernel weights in `scoring/weights.json`: 0.18×3 + 0.14×3 + 0.22×1 + 0.10×5 + 0.08×2 + 0.10×3 + 0.08×4 + 0.04×4 + 0.06×3 = 0.54 + 0.42 + 0.22 + 0.50 + 0.16 + 0.30 + 0.32 + 0.16 + 0.18 = 2.80. No other score changed. Per D3.7 (c), these scores rate the upstream library as inspected, not the proposed custom layer (intent journal, approval route, token interceptor). That layer is unscored and is where most review objections sit (X-3).

## 14. Open questions for the adversarial reviewers

1. **JS client compatibility.** Does `@dapr/durabletask-js` 1.0.0 (2026-03) work against the v0.15.1 sidecar's work-item stream (completion tokens, stateful-history capability negotiation, health pings)? Static reading says plausible (deprecated RPC kept, empty token accepted); this is unverified.
2. **Windows.** URI handling of `"file:" + path` (`sqlite.go:85-91`) with backslashes, spaces, `#`, `%` or `?` in `%USERPROFILE%`; the `DeleteTaskHub` open-file removal; and whether modernc v1.34.5 behaves identically on windows-arm64. Nothing here is tested by the project.
3. **Vulnerability reachability.** Are GO-2026-6061 and 6348 (gRPC transport) and the x/net and Go 1.26.x HTTP/2 advisories reachable from `main.go`? `govulncheck` was not run. Partly answered on amendment: 6441 and 6443 need xDS, which nothing imports. GO-2026-5970 sits only in `historysigning`, which the sidecar does not call. 6629 (precis) and 4945 (go-jose) have no importer (section 3).
4. **Binary size and startup.** Not measured; the 20-35 MB figure is a guess.
5. **Silent lease delay.** After an unclean exit, work resumes only after `LockExpiration` (2 minutes). Is that acceptable for the user, or should our `main.go` clear stale `LockedBy` on start? That is safe only with a single sidecar, which a lock file would have to enforce.
6. **Dapr's own truncation defence.** Does Dapr's runtime anchor `SignatureLength` anywhere outside the state store? If not, Dapr has the same tail-truncation gap. Only the metadata location was read.
7. **Where the maintainers' description is optimistic.** README "lightweight, embeddable engine" (the embedded Go path exists, but the documented sidecar has no authentication and "serve[s] one client at a time", README:53, while the code accepts competing streams). Stage 2's "tamper and truncation tests" (head only, library only). CI "Go 1.23.x" (go.mod requires 1.26).
8. **Failed approaches recorded.** Issue-response sampling was impossible because issues are disabled. OpenWorkflow's chaos test was checked as a possible shared crash test, but it does not demonstrate no-duplicate either, so no candidate on the R10 shortlist yet demonstrates the T7 property.

### Review responses (2026-10-21)

Amender s3-amend-durabletask, against `a89450a` (and the Alpha at `578fbbc`). The objections come from `reviews/security-engineer.md`, `reviews/code-archaeologist.md` and `reviews/dao-skeptic.md`, applied under anchor clauses (a)-(d) (state.md D3.7, D3.8) and threat model v0.2.

| Id | Verdict | Change made (section) or evidence for dispute |
|---|---|---|
| S-dapr-durabletask-go-1 | accepted | Section 6 G5 now has condition (2): `approval:*` is accepted only from a route whose grant the agent principal never holds, backed by an R11 record from a host ceremony (R19, T22). Until that path exists, approval waits may not gate human-only steps. Section 11 adds a self-approval fault case. G5 verdict stays "pass", with the stricter condition. |
| S-dapr-durabletask-go-2 | accepted | Confirmed `snapshotFingerprint` hashes only page-controlled title, URL, text and counts (`agent-control-runner.js:130-163` at `578fbbc`). Section 7 step 3: uncertain irreversible steps go to the human, with the intent record shown, and are never auto-verified or re-dispatched. The DOM check is allowed only for reversible steps, and it may conclude only "done" or "ask". Section 11 adds a fault case where the page restores its pre-action DOM. This matches the v0.2 T1 closure. |
| S-dapr-durabletask-go-3 | accepted | Section 7: the token is delivered on stdin and minted per sidecar start. Section 8: the token's lifetime is stated (sidecar lifetime, rotated on any restart) and compared with T3. |
| S-dapr-durabletask-go-4 | accepted | Section 12 first PR: the claim is scoped to tamper-evidence level (a), `exportHead()` is added as a future external anchor, and the module may not gate human-only routes until level (b) exists. Section 7 R11 and section 8 tamper bullet amended; the OS keystore is not credited against same-user processes (v0.2 T9). |
| S-dapr-durabletask-go-5 | accepted (score changed) | One T7 rule is now applied. isolation_and_security **2 -> 1**: no test in the artifact as used exercises a checked property; only helpers are tested (clause (b)); what remains is absences, capped at 1 (clause (d)). os_kernel total **3.02 -> 2.80** (section 13). |
| W-2 (lead's question: what lifts durabletask above 1?) | accepted; score lowered | **Nothing that the anchor credits.** I looked for a test that exercises T7, T8 or R11 tamper on the artifact as proposed and found none. `Test_TaskExecutionId`, `Test_DuplicateEvents`, `Test_RuntimeState_DuplicateCompletionSingleParentNotification`, the `dedup` tests and `Test_AbandonActivityWorkItem` are helpers. `TestGetWorkItems_DisconnectRedeliversBufferedItem` (`backend/executor_stream_test.go:388-485`) uses `newFakeExecBackend` and queued, never-started workflow items. No crash, lease-expiry or torn-write test exists (grep in section 2). The `historysigning` tests do exercise tamper detection itself, but that code is not used as proposed (pattern only) and has the tail-truncation gap. The original 2 credited helper tests, which clause (b) excludes. Hence 1, the same as openworkflow. Not 0: the reachable advisories are listener availability faults that defeat none of the three properties, and `VerifyChain` tail truncation lies outside the proposed configuration (clause (d)). |
| X-1 | accepted (location deferred to Gate 3) | Sections 7 and 8: the job DB, intent journal, token, and R11 key and head belong in the Gate 3 bridge-only store, not `~/ResonantOS_User/state/`. Read-deny covering only `Secrets` re-confirmed (`delegation-isolation.mjs:200-202` at `578fbbc`). Section 11 adds a T21 child-tamper case. |
| X-2 | accepted | Section 5 R11 row states the attacker model: level (a) only; level (b) is not met by the library or by the TypeScript port without an external checkpoint. |
| X-3 | accepted (annotation) | Section 13 note: the scores rate the upstream library as inspected (D3.7 (c)), and the custom layer is unscored. |
| X-4 | accepted (design note deferred to Gate 3) | Answered through S-1 (G5 condition 2, section 11 case). An approval UI the agent cannot drive is a Gate 3 item (D3.7); section 12 lists it as an adoption blocker. |
| X-6 | accepted | Section 8 adds a Component surface bullet: the upstream listener is unauthenticated; ours must authenticate and be unreachable from confined children; the parser runs outside the A1/A2 process. Section 13 names it as a sub-reason (not scored, per W-5 deferral). |
| X-10 | accepted | Re-scored under the clarified anchor (see S-5 and W-2). |
| W-5 | lead's (recorded for Gate 3, D3.7) | No score effect. The surface is named as a sub-reason in section 13. |
| TM-10 | lead's (applied in threat model v0.2 T1) | Section 7 step 3 follows the new T1 closure (no automatic retry of indeterminate outcomes). |
| A-dapr-durabletask-go spot-check rows 1-13 | no objection (all PASS) | No citation changed. On amendment I corrected one error of my own: GO-2026-6443 reachability (section 3; xDS-only, unreachable) and new citations were added at the SHA (`main.go:27, 39`, `sqlite.go:1004-1023, 1047-1052`, `go.mod:17, 18, 28, 43`). Counts re-run with the commands given in section 2; all reproduced (394, 39, 7, 3,805, 17). |
| A cross-cutting 6 (STATUS lines) | accepted | Header: `STATUS: COMPLETE (amended after review, 2026-10-21)` with `verified: a89450a... 2026-10-21`. |
| D C-8 (STATUS lines) | accepted | As A cross-cutting 6. |
| D C-1 (sensitivity rule) | lead's (applied D3.6) | No score effect. Section 12 notes that the R10 pair was FRAGILE and that the margin is now 0.28 after this re-score; `sensitivity.py` needs a rerun. |

No objection is disputed. The DAO skeptic raised none in scope for this dossier and confirmed G4/G5 for its role. The archaeologist raised none.
