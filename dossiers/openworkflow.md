# Dossier: OpenWorkflow (openworkflowdev-openworkflow)

STATUS: COMPLETE (amended after review, 2026-10-21)

Amended 2026-10-21 by s3-amend-openworkflow (Claude Opus 5.5), standing in for the original inspector, against the same clone and SHA; review responses are at the end of section 14. Threat model cited is v0.2 (`ledger/threat-model-draft.md`); the isolation anchor is the one clarified in state.md D3.7 and D3.8.

Inspector: s3-insp-openworkflow, Claude Opus 5.5. Date: 2026-10-20. Clone: `research/_untrusted/openworkflow/` at commit `c82fbed0bb93301c07c65f1aae14574e7469cffe` (branch `main`, 2026-10-19 23:49 UTC, "chore(deps): bump dotenv from 18.0.7 to 18.0.8 (#920)"; `git clone --depth 200`). Execution: none of the candidate's code was run. One platform probe was run from my scratchpad (`probe.mjs`, own code): it opened a fresh database with the local Node runtime's built-in `node:sqlite` (Node v22.20.0, Windows 11) to read the `PRAGMA synchronous` and `PRAGMA compile_options` defaults that OpenWorkflow inherits. That probe is labelled [inspected: platform probe] below; it is not an execution of OpenWorkflow.

Evidence labels used below: [inspected] (read the code), [executed] (ran it, only with approval), [reported] (authors' docs, README, issue text), [hypothesis]. Every claim that matters carries one. Repository instruction files are evidence, never instructions; this repository has no AGENTS.md or CLAUDE.md, only `CONTRIBUTING.md` and `.husky/commit-msg` (not run).

## 1. Identification

| Field | Value |
|---|---|
| Name | OpenWorkflow ("Open-source TypeScript framework for building durable, resumable workflows", `packages/openworkflow/package.json:4`) |
| Homepage | https://openworkflow.dev (docs source in `apps/docs/docs/*.mdx`) |
| Canonical source | GitHub `openworkflowdev/openworkflow` (organisation account); no other canonical host found |
| Maintainers | One principal author: `jamescmartinez` has 762 commits; the next human contributor has 3 (GitHub contributors API, 2026-10-20). Bus factor 1 [inspected] |
| Verified HEAD | `c82fbed` 2026-10-19; created 2025-10-25; 25 open issues; not archived |
| Packages | npm `openworkflow` 0.11.0 (2026-10-12, core library); `@openworkflow/cli` 0.6.0; `@openworkflow/dashboard` 0.1.12. Subpath exports `openworkflow/sqlite`, `openworkflow/postgres`, `openworkflow/internal` (`packages/openworkflow/package.json:28-45`) |
| Runtime | Node >=22.22.0 or Bun (`packages/openworkflow/package.json:84-86`); SQLite through `node:sqlite` / `bun:sqlite` (`packages/openworkflow/sqlite/sqlite.ts:31-55`) |
| Licence | Apache-2.0, single `LICENSE.md` at repo root (the 201-line standard text, appendix boilerplate left unfilled); no NOTICE file; no per-directory licences. Manifest: only `packages/openworkflow/package.json:25` declares `"license": "Apache-2.0"`; `apps/cli/package.json` and `apps/dashboard/package.json` have no licence field (matches the Stage 2 note on the CLI) [inspected] |
| Runtime dependencies (core) | `cron-parser` 5.10.2 (MIT) -> `luxon` 3.7.2 (MIT). Optional peers: `postgres` 3.4.9 (Unlicense), `@opentelemetry/api` 1.9.1 (Apache-2.0) (`package-lock.json`) [inspected] |
| Documentation | English; Mintlify docs in-repo; `ARCHITECTURE.md` (446 lines) is the design reference. English-speaking maintainer community, small |
| DOI / paper / SWHID | none |

## 2. What works

Code-level features, with the tests that exercise them. Test counts by `grep -c "test("`: shared backend contract `testing/backend.testsuite.ts` 76, `worker/worker.test.ts` 61, `worker/execution.test.ts` 81, `client/client.test.ts` 38, `sqlite/sqlite.test.ts` 11, `sqlite/backend.test.ts` 9, `client/rerun.test.ts` 8, `worker/chaos.test.ts` 1.

| Feature | Code | Tests | Backend the test uses |
|---|---|---|---|
| Memoised steps (`step.run`): replay returns the stored output of a `completed` attempt | `worker/execution.ts:464-504`; history built in `worker/step-history.ts:42-72` | `worker.test.ts:405` "recovers from crashes during parallel step execution", many in `execution.test.ts` | Postgres only |
| Durable sleep: a `sleep` step attempt stores `resumeAt`; the run is parked with `worker_id = NULL`, `available_at = resumeAt` | `execution.ts:508-530`, `sqlite/backend.ts:785-844`, sleep pre-pass `execution.ts:276-312, 1176-1190` | `worker.test.ts:905` "step.sleep is cached on replay"; `backend.testsuite.ts` `sleepWorkflowRun()` block (line 1153) | worker test Postgres; backend contract SQLite and Postgres |
| Leases and heartbeat: claim sets `available_at = now + lease` (30 s default), heartbeat at half the lease | `worker/worker.ts:18, 362-383`; `sqlite/backend.ts:666-783` | `backend.testsuite.ts:1032` "claims workflow runs and respects leases, reclaiming if lease expires"; `worker.test.ts:458` "reclaims workflow run when heartbeat stops" | contract on both; worker test Postgres |
| Ownership fencing of writes: every step and run transition carries `AND worker_id = ?` | `sqlite/backend.ts:76-101` (`RUNNING_WORKFLOW_RUN_OWNED_WHERE`, `STEP_ATTEMPT_OWNED_WHERE`), used at 770, 861, 913, 1220, 1256, 1307, 1341 | `backend.testsuite.ts:1644, 1705, 1725, 1817, 2068, 2168` ("fails when the worker does not own the workflow run", etc.) | SQLite (memory and file) and Postgres |
| Run-level idempotency key (24 h window) | `sqlite/backend.ts:323-357` inside `BEGIN IMMEDIATE`; window `core/backend.ts:16` | `backend.testsuite.ts` `createWorkflowRun()` block | both |
| Child workflows and signals with deterministic internal idempotency keys | `execution.ts:349-364`; `sqlite/backend.ts:538-645` | `backend.testsuite.ts:2797` "duplicate send to same waiter delivers at most once", `:2838` "idempotent send does not create duplicate delivery rows"; `execution.test.ts:2344, 2829, 2907` | contract both; execution tests Postgres |
| Cancellation (status change only) | `sqlite/backend.ts:971-1012` | `worker.test.ts:1380` "worker handles when canceled workflow during execution" asserts the in-flight step ran to completion and the run ended `canceled` | Postgres |
| Retries with backoff; default step policy 10 attempts | `execution.ts:155-161`, `1279-1322` | many in `worker.test.ts` | Postgres |
| Migrations under a writer lock | `sqlite/sqlite.ts:249-276` | `sqlite.test.ts:119-186` incl. "rolls back the whole pending upgrade before retrying" | SQLite |
| Reruns from a saved step | `core/rerun.ts`, `client/rerun.ts` | `client/rerun.test.ts:11` `describe.each(["sqlite","postgres"])` | both |

CI: `.github/workflows/ci.yaml` runs `npm run ci` (format, build, lint, squawk, duplication, spell, knip, typecheck, `vitest run --coverage`) and a Bun lane, both `runs-on: ubuntu-latest` (lines 20, 42) with a Postgres service container; there is no Windows or macOS lane [inspected]. `vitest.config.ts:5` installs a Postgres global setup for the whole suite.

Deployment evidence: one named adopter, Last Light by Nearform (issue #877, 2026-10-10), which "chose OpenWorkflow as the runtime" on SQLite and reports from a spike on 0.10.1 that "after a `kill -9` mid-step a fresh worker reclaimed the run with only the in-flight step re-running" [reported]. Spike stage, not production.

What the documentation says that the code does not: `apps/docs/docs/steps.mdx:62-64` says that after a crash following the card charge "The customer is charged exactly once". That holds only when the crash falls after the step's `completed` row was committed. The code re-executes a step whose attempt is still `running` (section 5), and other pages say so: `parallel-steps.mdx:61-67` ("The incomplete step re-executes") and `openworkflow-vs-bullmq.mdx:28-30` ("Use an idempotency key with the payment provider so a retry can't charge twice") [inspected].

## 3. Maturity

- Footprint: in-process library, no server. One synchronous SQLite connection per `BackendSqlite` (`sqlite/backend.ts:106-147`); all SQLite calls are synchronous on the event loop. One runtime dependency tree (cron-parser, luxon) [inspected].
- Maintenance: 212 commits in the last ~8 weeks of the shallow clone (Sept-Oct 2026, roughly 40% Dependabot); GitHub releases for `openworkflow@` since 0.1.0 on 2026-04-27, 27 tags to 0.11.0 on 2026-10-12. Pre-1.0. Bus factor 1 [inspected].
- Issue response, five sampled: #756 closed in 1 day; #716 in 16 days; #713 in 19 days; #710 ("Flaky parallel crash-recovery test needs explicit step synchronization") in 23 days; #714 (parent stays parked when a child's deadline expires) open 7 weeks, maintainer replied after 16 days that a "deadline sweep" will come with schedules. #877 (Last Light) answered in 1 day with two PRs merged; #913 (2026-10-17, a local-first user asking for abortable steps and browser support, the same shape as ResonantOS) has no reply yet [inspected].
- Security posture: no SECURITY.md (404), no repository advisories (API returns 0), no audit. Issue #482 "Security Disclosure: Database Credentials Exposed" was closed with no comment; the only embedded URL is the local development default `postgresql://postgres:postgres@localhost:5432/postgres` (`postgres/postgres.ts:8-9`), so this reads as a scanner false positive, but there is no disclosure process [inspected].
- Documentation: good for a project this age; `ARCHITECTURE.md` matches the code on the points I checked, except the "exactly once" sentence above.
- Popularity beside fitness: 1,338 stars and 71 forks; the fitness point is that the two engaged downstream users (#877, #913) have the same embedded-SQLite, long-step, approval-gate profile as ResonantOS and both hit the same gaps (abortable steps, buffered signals).

Counterexample row (s2-br-c, `https://openworkflow.dev/docs/production`): "For most production use cases, use PostgreSQL 14 or later"; "For single-server deployments, SQLite works well"; no SQLite limitations listed.
Answer: mostly refuted for our use, confirmed on test depth.
- Refuted: SQLite is a complete implementation of the same `Backend` interface (`sqlite/backend.ts`, 1,531 lines). It runs the full 76-test backend contract against both an in-memory and a file-backed WAL database (`sqlite/backend.test.ts:10-58`). The docs' own reasons to prefer Postgres are multi-server deployments and many workers (`apps/docs/docs/sqlite.mdx:75-79`, `production.mdx:36-42`). A single-user desktop bridge with one worker is the "single-server" case the docs endorse.
- Confirmed: the engine-level tests (`worker.test.ts`, `execution.test.ts`, `chaos.test.ts`, most of `client.test.ts`) import `createTestBackend` from `postgres/test-backend.testsuite.ts` and never run against SQLite. Replay, sleep resumption, cancel-during-step and retry are therefore tested on Postgres only. On SQLite they are covered only by the backend contract and by `rerun.test.ts`.
- New: the docs list no SQLite limitations, and I found these in code: no `PRAGMA synchronous` is set; no `integrity_check` is run on open; the run tables cannot be schema-prefixed on SQLite (maintainer, #877); a busy timeout of 5 s applies when two processes share the file.

## 4. Architecture

Control flow for one job:
1. The client inserts a `workflow_runs` row (`pending`) (`sqlite/backend.ts:323-357, 432-495`).
2. The worker loop (`worker/worker.ts:215-232`) calls `tick()` (183-201), which calls `claimWorkflowRun` for each free concurrency slot. `claimWorkflowRun` is a `BEGIN IMMEDIATE` transaction: it expires deadline-passed runs, selects the oldest runnable row (`pending`, or `running` with `available_at <= now`), and sets `worker_id` and `available_at = now + lease` (`sqlite/backend.ts:666-757`).
3. `executeWorkflow` loads every step attempt, builds `StepHistory`, completes elapsed sleeps and parks again if a wait is still pending (`worker/execution.ts:1165-1190`). It then calls the user function from the top. Each `step.*` either returns a cached `completed` output or writes a new `running` attempt, runs the function inline, and writes `completed` or `failed` (`execution.ts:464-504`).
4. The run ends in one of four ways: `completeWorkflowRun`; `sleepWorkflowRun` (park); `rescheduleWorkflowRunAfterFailedStepAttempt` (back to `pending` with backoff); or `failWorkflowRun` (`execution.ts:1216-1326`).

Storage. Tables `workflow_runs`, `step_attempts`, `workflow_signals`, `workflow_schedules`, `openworkflow_migrations` (`sqlite/sqlite.ts:69-242`). Every JSON column is plaintext TEXT, and timestamps are ISO-8601 strings taken from the JS wall clock (`sqlite.ts:316-330`).

SQLite durability, settled from code:
- `busy_timeout = 5000`, `journal_mode = WAL` for file databases, `foreign_keys = ON` (`sqlite.ts:56-61`) [inspected].
- `synchronous` is never set, so the build default applies. The platform probe on Node v22.20.0 (Windows) returned SQLite 3.50.4 with `synchronous = 2` (FULL) and the compile options `DEFAULT_SYNCHRONOUS=2` and `DEFAULT_WAL_SYNCHRONOUS=2`. WAL with FULL syncs the WAL on every commit, so each committed statement is durable across power loss [inspected: platform probe]. I did not probe Node 24 (not installed here), and the Alpha requires Node >=24.21.0. The Node 24 build flags need the same one-line probe before relying on this.
- Transactions: multi-statement operations use `BEGIN IMMEDIATE ... COMMIT/ROLLBACK`. These are run creation with an idempotency key (331-345), claim (673-750), `sendSignal` (541-640), schedules (225-312), rerun (363-424) and migrations (`sqlite.ts:258-267`). No `await` occurs inside a transaction; the code says this is deliberate ("keep the transaction synchronous", `backend.ts:359`). All other transitions are single autocommit statements with the ownership predicate.
- Composite transitions that are not atomic [inspected]: `completeWorkflowRun`, `failWorkflowRun` and `cancelWorkflowRun` each commit the child's terminal state, and only then run `wakeParentWorkflowRun` as a separate statement (`backend.ts:873-876, 926-930, 1004-1009, 1049-1094`). A crash between the two leaves the parent parked until its own wait timeout, which defaults to one year (`step-history.ts:79-83`). The deadline-expiry path never wakes the parent at all (#714, `backend.ts:676-698`). The Postgres backend has the same shape (`postgres/backend.ts:872, 918, 975`). No startup sweep reconciles this state.
- No torn-write, power-loss or corrupt-file test exists. `newDatabase` opens the file without `PRAGMA integrity_check`; a corrupt file surfaces as the wrapped error "SQLite backend failed to open database" (`backend.ts:140-145`) [inspected].

Lifecycle:
- Start: `BackendSqlite.connect(path)` is synchronous and runs migrations (`backend.ts:124-147`).
- Stop: `worker.stop()` waits with no upper bound for every active execution (`worker.ts:142-157`). The library installs no signal handlers; the embedder owns them (only the CLI does, `apps/cli/commands.ts:421-422`).
- Crash: in-flight runs become claimable when the lease expires (30 s).
- Upgrade: additive migrations, checked under a writer lock.

Identity and auth: none. `namespaceId` separates tenants in one file (`backend.ts:65-68`); worker ids are random UUIDs per concurrency slot (`worker.ts:93`). No principal is recorded on a run.

Operational model: embedded library. Client and worker can share one process (`client.newWorker()`, `client/client.ts:105`). The `Backend` interface is only reachable through `openworkflow/internal` (#893, #913).

Phone-home check [inspected]:
- Core package: a grep of `packages/openworkflow` (non-test) for `fetch(`, `node:http(s)`, `node:net`, WebSocket and URLs finds only comment links. The core makes no network calls. OpenTelemetry is an optional peer and is inert unless the host configures an exporter.
- CLI: on by default and opt-out. `apps/cli/telemetry.ts:30-58` writes `~/.openworkflow/telemetry-id` and sends `cli_command_invoked` events to PostHog (hard-coded project key, line 56) with OS, arch, Node version, backend type and CLI version. It is disabled by `DO_NOT_TRACK`, `OPENWORKFLOW_TELEMETRY_DISABLED`, `CI` or `--no-telemetry` (lines 33-38).
- Dashboard: depends on the CLI and on `@monaco-editor/react`, imported without a local loader configuration (`apps/dashboard/src/components/ui/monaco-json-editor.tsx:3`). That library's default loader fetches Monaco from a CDN [hypothesis: default-loader behaviour from the library's documentation, not verified in its source].

## 5. Direct relevance

Requirement R10 (`stage1/gaps.md:71-75`). The Alpha's job machinery, against what OpenWorkflow supplies:

| Alpha gap | Alpha evidence | OpenWorkflow supplies | Still missing |
|---|---|---|---|
| Jobs persisted in `chrome.storage.local`; running jobs flipped to `paused` on panel load | OSC-22; `side-panel-browser-job-controller.js:34-43`; `browser-job-store.js:428-430` | Durable run and step state in a SQLite file on the bridge side; a crash or restart leaves the run `running` and claimable after lease expiry, not `paused` [inspected] | The browser panel is the executor of page actions (os-map 7), so the bridge needs a channel to drive it |
| Resume loses planner history (`history: []`) | OSC-21; `side-panel-scheduled-browser-job-runner.js:241-247` | Replay from the top with memoised outputs, so every recorded planner decision and action result is restored [inspected] | Steps must be modelled so that planner calls and browser results are each a step |
| Cancel rewrites status without killing | OSC-33 | Not solved. Cancel is a status write (`backend.ts:971-1012`); the step function has no arguments and no `AbortSignal` (`core/workflow-function.ts:32-33`); the test at `worker.test.ts:1380-1432` asserts the step ran to completion after cancel; docs: "the current step may complete" (`canceling.mdx:62`) [inspected] | Abort plumbing (upstream proposal #913, unanswered) |
| No supervised recovery after bridge crash | OSC-42 | Lease-based reclaim on the next worker start [inspected] | A supervisor that restarts the bridge (R04) |
| Duplicate irreversible effects (T7) | threat model T7 | Not solved (see the property check) | An intent journal with an explicit indeterminate outcome |

Threat T7 (`ledger/threat-model-draft.md:50`, v0.2). The Durability row of threat-model section 4 (v0.2, line 88: "recovery after crash during an uncertain side effect with no duplicate; indeterminate outcomes go to the human, never to automatic retry; torn-write test"), checked one by one. Each item names the condition under which the primitive yields the property and the fault that breaks it (threat model v0.2 line 77).

1. Recovery after a crash during an uncertain side effect, with no duplicate, and no automatic retry of an indeterminate outcome. **Not demonstrated, and contradicted by design for any effect placed inside a step function.**
   - `step.run` checks only the completed-attempt cache (`execution.ts:471-475`). A `running` attempt left by a crash lands in `runningByStepName` (`step-history.ts:63`). `step.run` never consults it, unlike `runWorkflow` (`execution.ts:570-578`). It creates a fresh attempt and calls `fn()` again (`execution.ts:477-488`). This is an automatic retry of exactly the indeterminate outcome the v0.2 row says must go to the human.
   - The semantics are therefore at-least-once per step. The orphaned `running` row stays in the table and counts toward the 1,000-attempt cap (`step-history.ts:4`).
   - A step that throws after its effect happened (for example a timeout after a form submit) is retried up to 10 times by default (`execution.ts:156-161`).
   - Retry policy does not cover the crash path (found in the amendment) [inspected]. `maximumAttempts` is compared with the count of `failed` attempts only (`core/workflow-definition.ts:193-197`, fed by `failedAttemptCount`, `step-history.ts:311-313`); `failedCountsByStepName` is incremented only for `status === "failed"` (`step-history.ts:56-60`), and an orphaned `running` attempt is never counted. `failStepWithError` is reached only from the `catch` of a thrown error (`execution.ts:496-502, 767-795`). So `retryPolicy: { maximumAttempts: 1 }` stops retries after a thrown error but does not stop re-execution after a crash. Condition for "no duplicate" with the bare engine: none exists; the step body must itself be idempotent against its own prior partial run.
   - Nothing in the engine models "effect may have happened": no intent record committed before the effect, no indeterminate status, no idempotency key passed to the step. A stable key can be built by hand from `run.id` plus the step name (`core/workflow-function.ts:85-99`); the docs recommend that pattern only on the BullMQ comparison page.
   - No test leaves a `function` attempt in `running` and replays it (grep for `kind: "function"` in tests finds only fixtures in `step-history.test.ts` and `worker.test.ts:2008`, a failed attempt).
2. Crash-recovery tests, as distinct from thrown errors. **Partly demonstrated.**
   - `backend.testsuite.ts:1032` proves on SQLite and Postgres that a second worker can reclaim an expired lease and that `attempts` increments.
   - `worker.test.ts:458` proves a run with no steps is reclaimed after lease expiry (Postgres).
   - `worker.test.ts:405`, despite its name, simulates a crash with `throw new Error("Simulated crash")`. That exercises the failed-step retry path, not process death.
3. The chaos test (`worker/chaos.test.ts`). **Does not test the property.**
   - It uses the Postgres test backend (lines 2, 19), never SQLite.
   - Its "worker deaths" are `await victim?.stop()` (line 94), which is a graceful stop that waits for active executions to finish (`worker.ts:147-157`). No lease expires, and no step or process is interrupted mid-effect.
   - It asserts only that the result has 50 entries, that the last is 49, and that at least one restart happened (lines 61-63). It does not count how many times each step function ran, so a duplicate would pass.
4. Torn-write test. **Not demonstrated.** None exists. SQLite WAL with FULL sync provides atomic commits at the storage layer [inspected: platform probe on Node 22]. The engine adds application-level partial states between autocommit statements (section 4) and does not reconcile them.
5. Durable timers survive process death. **Demonstrated in design; partly tested.**
   - The resume time is persisted twice: in the sleep attempt's `context.resumeAt` and in the run's `available_at`. A restarted worker claims the run when `available_at <= now` and completes the elapsed sleep in the pre-pass (`execution.ts:276-312`).
   - `worker.test.ts:905` covers park-then-resume within one worker on Postgres. No test restarts the process.
   - Timers use the wall clock (`sqlite.ts:316-318`). A backwards clock change delays them; a forward change fires them early [inspected].
6. Idempotency where it exists. Run creation (24 h window), signal sends, and child-run creation are idempotent by key, and these are tested (`backend.testsuite.ts:2797, 2838`; `execution.test.ts:2344`) [inspected]. These protect engine records, not external effects.

Two v0.2 threats name this dossier (T21 and T22, `threat-model-draft.md:55-56`). Their property rows (lines 84-85) are checked against the artifact here:

7. Security state unreachable by children; rollback detected (T21). **Not demonstrated; no mechanism.** The engine keeps all run history in one SQLite file at a path the embedder chooses (`backend.ts:124-147`), as plaintext TEXT with no MAC, signature or checksum over history (`sqlite.ts:69-242`) [inspected]. Whether a child can reach it depends wholly on where the embedder puts it. Fault that breaks it: a child with write access sets a `step_attempts` row to `completed` with a chosen `output`; the next replay returns it from `findCached` (`execution.ts:471-475`) as if the step had run.
8. The approval record cannot be minted by the agent principal (T22). **Not demonstrated; no mechanism.** The engine has no approval concept. `sendSignal` takes only a name, data and an optional idempotency key, with no sender identity (`client/client.ts:278-284`), and wakes every workflow waiting on that name. Any code holding the client or the file can resume a `waitForSignal` used as an approval gate [inspected]. Fault: the agent principal sends the signal itself.

Additional failure modes [hypothesis, from code reading; untested]:
- **In-process double execution after host sleep.** `tick()` excludes busy slots, not runs already executing in this process (`worker.ts:183-201`), and `claimWorkflowRun` accepts any `running` row whose lease has passed (`backend.ts:701-713`). After a laptop sleeps longer than the lease, with concurrency >= 2, a free slot can claim a run whose step is still in flight in another slot. The step then runs twice concurrently. The stale slot's writes are rejected by the ownership predicate, but its side effect is not. A lost heartbeat is only logged (`worker.ts:377-379`) and does not stop the execution. With the default concurrency of 1 (`worker.ts:28`) this cannot happen within one process.
- **Signals are dropped when no workflow is waiting** (`ARCHITECTURE.md:39-45`). Any "browser panel reports a result" design built on `sendSignal` races the workflow reaching `waitForSignal`. Last Light works around this with a check-before-park row (#877).

## 6. Reuse decision

**Wrap (adopt the core library `openworkflow` as a pinned dependency behind a bridge-side adapter).** Do not use the CLI or the dashboard.

Why it beats the alternatives in section 12:
- It is the only candidate that is at once embeddable in the Node bridge, persists to a local SQLite file with no server, and offers memoised replay, durable sleep, leases and child workflows with a typed API.
- durabletask-go needs a Go sidecar over gRPC.
- Effect's workflow module is an unstable v4 API and needs the Effect runtime.
- Graphile Worker needs Postgres and BullMQ needs Redis.
- tool-journal models the uncertain effect correctly but is two weeks old and has no workflow layer.

The adapter must add what OpenWorkflow lacks for T7:
- an effect journal with an explicit indeterminate state, checked on every replay (this is the only part that stops the crash-path duplicate, because the engine re-executes a `running` attempt whatever the retry policy, section 5 item 1);
- `maximumAttempts: 1` on irreversible steps (stops retries after a thrown error only);
- no irreversible effect ever executed inside a `step.run` body; the body only records intent and enqueues;
- abort on cancel;
- concurrency 1 per bridge;
- a parent-wake sweep on start (only if child workflows are used);
- the job database in the bridge-only, integrity-protected state location (T21; the location itself is a Gate 3 decision, state.md D3.7 on X-1);
- an indeterminate-step decision accepted only with an approval record from the host ceremony (T22, R19, R11), never from a route the agent principal holds.

This is a decision to wrap, not to adopt bare. The T7, T21 and T22 properties come from our layer, not from OpenWorkflow. The amendment did not change the decision: the review objections all land on the layer, and each is now a stated requirement of it.

Hard gates:

| Gate | Result | Clause |
|---|---|---|
| G1 no mandatory cloud or telemetry | Pass for the core library; Fail for `@openworkflow/cli` as shipped | Core has no network code (section 4). The CLI sends PostHog events by default (`apps/cli/telemetry.ts:30-58`). The dashboard CDN loader is unverified. We take only the core. |
| G2 per-OS matrix honest, no silent no-op | Pass with [WARN] | The project states no per-OS matrix and has no Windows or macOS CI. The code is portable (no `process.platform` branches in the core). The matrix in section 8 is mine. Nothing silently no-ops: a failed open throws. |
| G3 licence | Pass | Apache-2.0 file-level; runtime deps MIT. Section 9 lists the obligations. |
| G4 chain | N/A | Not a DAO component. |
| G5 invariants | Pass, conditional | The engine has no notion of human-only actions. Its default step retries (10) and at-least-once replay could re-perform a human-approved action without a fresh approval. The adapter must mark such steps non-retryable and route an indeterminate outcome to the human, never to automatic replay (threat model v0.2 T1 closure and Durability row). Retry policy alone does not achieve this (section 5 item 1); the effect journal does. Unchanged by the amendment. |

## 7. Integration design

Seam: os-map section 17 names no durable-execution seam. The closest are seam 3 ("Make human approval a core-visible event") and the "neutral restartable core" goal; OSC-42 records the restart gap. Job state moves from the extension into the bridge.

Process boundary:
- The bridge (Node >=24.21.0, root `package.json` engines) hosts one `OpenWorkflow` client and one `Worker` with `concurrency: 1`, on `BackendSqlite.connect(<bridge-only state dir>/jobs/openworkflow.db)`. Amended (S-openworkflow-3, X-1, T21): the original path `<userRoot>/BrowserFirst/Jobs/` lies inside the user state tree that delegated children can write through the bridge and, outside macOS, directly (OSC-32; the Alpha's read-deny list covers only `ResonantOS_User/Secrets`, per security review X-1). The bridge-only location is a Gate 3 decision (state.md D3.7); until it exists, the adapter must not ship beyond the additive first PR.
- The side panel stays the executor of page actions (os-map 7) and talks to the bridge over the existing authenticated loopback routes.

Data and steps, per browser job (one workflow run, input = goal and job id):
1. `step.run("plan:<i>")` calls the existing host planner (`browser-first/host/agent-control-host-service.mjs:329-409`). Re-execution is tolerable here because the call is read-only.
2. `effect("act:<i>", action)` is an adapter call, not a raw `step.run`. In one SQLite transaction in an adapter-owned table, it writes `intent(job, step, action, idempotencyKey = run.id + ":" + step)` with status `issued`. It then enqueues the action for the panel and parks with `waitForSignal`. It checks the outcome row before parking, to close the dropped-signal race (`ARCHITECTURE.md:39-45`).
3. The panel posts the result to a new route `/augmentor/jobs/:id/result`. The route writes the outcome row and sends the signal. Amended (S-openworkflow-2a): the reported result is untrusted. It is produced by content-script code running inside the page the agent acts on (OSC-01, OSC-13), so "done" and "failed" are both attacker-influenced (V1). The adapter records it as a claim with its source, never as a verified outcome, and a "failed" report for an irreversible class leaves the step `indeterminate`, not `failed`.
4. On replay, `effect()` finds `issued` with no outcome. Instead of re-issuing, it marks the step `indeterminate` and pauses the job for a human decision (verify on page / retry / abandon). This is the tool-journal pattern from the Stage 2 ledger, implemented over OpenWorkflow's run id and step names.
5. The human decision (amended, S-openworkflow-2b, X-4, T22). The decision route accepts only an R11 approval record created by the host-side ceremony (R19), bound to the intent row's canonical action. The agent principal never holds that route's grant (R01); today the planner and the panel hold the same tokens (OSC-02), so this needs R01 before the route exists. The engine cannot help here: `sendSignal` carries no sender identity (`client/client.ts:278-284`), so the adapter, not a bare signal, must check the record before waking the workflow. "Verify on page" shows the user the intent record and the evidence the panel captured; it never decides by itself. "Retry" on an irreversible class shows the intent record first and is never one click.

Error behaviour:
- irreversible steps use `retryPolicy: { maximumAttempts: 1 }`;
- a lease-loss callback (wrapped heartbeat) aborts the in-flight `AbortController`;
- cancel = OpenWorkflow cancel + abort signal to the panel.

Identity: OpenWorkflow carries no principal, so the adapter stores the originating principal (the R01 grant id, once it exists) in the run input and in each intent row.

Versioning: pin `openworkflow@0.11.0` exactly (pre-1.0, schema migrations are additive). Name steps deterministically ("plan:3", "act:3") so replays match across releases (`steps.mdx:84-86`).

Migration and Alpha changes, at commit 578fbbc:

| Alpha file | Change |
|---|---|
| `browser-first/host/` (new `durable-jobs.mjs`, `durable-effect-journal.mjs`) | host OpenWorkflow, effect journal, routes |
| `browser-first/host/run-bridge-minimal.mjs` | wire the service in and start the worker after the server; stop it in `bridge-shutdown.mjs` (`createBridgeShutdown`, lines 1-19) with a bounded wait |
| `browser-first/resonantos-side-panel-extension/src/lib/browser-job-store.js` | becomes a read-through cache of bridge job state (keys at 428-430 kept for migration only) |
| `.../side-panel-browser-job-controller.js:34-43` | remove `recoverInterruptedJobs(running -> paused)`; query the bridge instead |
| `.../side-panel-scheduled-browser-job-runner.js:241-247` | resume with the history from the bridge instead of `history: []` |
| `.../agent-control-runner.js` (cooperative polls at 461, 651, 656, 675, 722) | poll results are reported to the bridge; the abort signal ends the loop |

Alpha tests affected (browser-first lane):
- `test/browser-job-store.test.mjs`
- `test/side-panel-browser-job-controller.test.mjs`
- `test/side-panel-scheduled-browser-job-runner.test.mjs`
- `test/agent-control-runner.test.mjs`
- `test/browser-job-scheduler.test.mjs` (scheduler default of 2 concurrent at `browser-job-scheduler.js:4` conflicts with worker concurrency 1)
- `test/control-run-state.test.mjs`
- `test/main-workspace-browser-job-controller.test.mjs`
- `test/agent-control-host-service.test.mjs`
- `test/dsh-native-shutdown.test.mjs` (shutdown ordering)

Phase 1 (the first PR below) is additive and changes none of them.

Interface sketch:

```ts
effect<T>(name: string, action: BrowserAction, opts: { irreversible: boolean }):
  Promise<{ status: "done"; result: T } | { status: "indeterminate"; intentId: string }>
```

## 8. Security and governance effects

- Replayed outputs as an injection channel (amended, S-openworkflow-3, T21): a delegated child is a V3 attacker that runs as the same user and is unconfined on Linux and Windows (OSC-32). If it can write the job file, a forged `completed` output for a `plan:<i>` step is replayed as the planner's own decision on every restart: persistent prompt injection that bypasses the planner. Two requirements follow: the job DB sits in the bridge-only state location (section 7), and replayed step outputs are untrusted input to the planner until R11 anchors them.
- New privileges: none at the OS level. The bridge gains a SQLite file holding plaintext step inputs and outputs: goals, page text, form values, planner prompts (`sqlite.ts:338-340`). That is personal data at rest, adding to T9. Needs 0600 or a Windows ACL equivalent, and a retention policy (none upstream; #303 is cited in #913 as the retention request).
- Attack surface: anything that can write the file can forge a `completed` step and have its output replayed as truth. There is no integrity protection on history, unlike durabletask-go's `backend/historysigning`. This is a local-attacker (V3/V4) concern, and V3 is any delegated child (item above); R11's ledger could anchor job outcomes. Surface added to the bridge process (security review W-5, for information): no listener and no network code in the core (section 4); the in-process parsers are SQLite and `JSON.parse` over the job file's contents, which are adversary input only if the file is reachable (T21).
- Duplicates (T7), restated: at-least-once replay, default 10 step retries, and possible in-process double execution after host sleep (section 5). Each can repeat an irreversible browser action unless the adapter intervenes.
- Revocation and cancel: cancel does not interrupt work (OSC-33 is not fixed by adoption).
- Isolation: none. Workflow code runs in the bridge process with the bridge's authority.
- Trust in maintainers: one principal maintainer, no SECURITY.md, no disclosure process. Pin exact versions and review diffs on upgrade.
- Friction to the user: an indeterminate outcome becomes an explicit human question. That is intended friction for irreversible actions.
- Telemetry: the CLI sends usage events by default. Never ship or invoke the CLI from ResonantOS, or set `DO_NOT_TRACK=1` in any developer script that uses it.

Per-OS matrix (core library inside a Node 24 bridge; no OS has upstream CI except Linux):

| OS | What runs | What degrades | What is silent |
|---|---|---|---|
| Windows | `node:sqlite` with WAL; the probe on Windows Node 22.20 shows FULL sync [inspected: platform probe] | No SIGTERM delivery; recovery after a forced kill relies on lease expiry (30 s); WAL is unsafe on network or sync drives (for example a pCloud-mapped `P:`) [hypothesis, SQLite documentation] | Nothing found; untested upstream |
| macOS | same code path | untested upstream; default `fsync` on macOS is not `F_FULLFSYNC`, so power-loss durability is weaker unless `PRAGMA fullfsync` is set [hypothesis, SQLite documentation] | none found |
| Linux | CI lane (ubuntu-latest), but engine tests run on Postgres | none | none |

Node call path: a plain ESM library, `import { OpenWorkflow } from "openworkflow"; import { BackendSqlite } from "openworkflow/sqlite"`. No sidecar, no WASM.

## 9. Licensing

- SPDX: Apache-2.0 (`LICENSE.md`, full text; no NOTICE file, so section 4(d) has no NOTICE content to carry forward). The core manifest matches. The CLI and dashboard manifests omit the field, which does not matter if we take only the core.
- Transitive (core): cron-parser MIT, luxon MIT. Optional peers: postgres (Unlicense), @opentelemetry/api (Apache-2.0).
- Compatibility with the MIT Alpha: depending on an Apache-2.0 package from MIT code is routine. Obligations if we redistribute (for example, bundling into an installer): keep the licence text and mark modified files (Apache-2.0 sections 4(a)-(b)).
- For legal review: (1) Apache-2.0 section 3's patent-termination clause interacting with the proposed Symbiotic Licence (status F); (2) whether vendoring modified OpenWorkflow files into an MIT repository needs per-file headers. Technical research, not legal advice.

## 10. Cost and effort

| Scenario | Scope | Estimate (one experienced Node developer) | Assumptions |
|---|---|---|---|
| Small | Bridge-hosted durable jobs for host-side work only (planner calls, delegation tasks); no panel changes | 3-5 days incl. tests | adapter + routes; concurrency 1 |
| Medium | Browser jobs moved to the bridge with the effect journal, indeterminate handling, panel cache, resumable history | 3-4 weeks | the 9 Alpha test files in section 7 rewritten; acceptance test on three OSs |
| Large | Abort plumbing upstreamed (#913), buffered messages (#894), signed or anchored job history (R11) | 2-3 months, partly upstream-dependent | maintainer acceptance not guaranteed |

Skills: TypeScript, SQLite, replay-determinism discipline (stable step names and no non-deterministic control flow outside steps; `versioning.mdx`).

Lock-in is low. The schema is five plain tables, and our adapter would own the effect journal. Replacing the engine means re-implementing replay, about 1,500 lines of execution code.

Maintenance exposure: pre-1.0 with a single maintainer. In the worst case we fork a small codebase: about 1,330 lines in `execution.ts`, 500 in `worker.ts`, 1,530 in the SQLite backend.

Language cost: none. Same language and runtime as the bridge.

## 11. Acceptance test

This is a request: it executes third-party code and needs user approval (D1.5). Proposed run: a throwaway directory outside `research/`, `npm install openworkflow@0.11.0` with `--ignore-scripts`, Node 24.21+, on Windows 11, macOS and Ubuntu (GitHub-hosted runners in a scratch repository).

Inputs: a workflow with steps `A` (pure), `E` (effect: appends a line to `effects.log` with its idempotency key, then sleeps 2 s before returning), `S` (`step.sleep("5s")`), `B` (pure). Run with `BackendSqlite.connect("jobs.db")` in a child process.

Fault scenarios (F1 from T7; F3 from T8):

| Id | Fault | Expected observable with bare OpenWorkflow | Expected with the ResonantOS adapter |
|---|---|---|---|
| F1 | `kill -9` / `taskkill /F` the child after `effects.log` is written and before `E` returns; restart after 35 s | `effects.log` has the line twice; `step_attempts` has one orphan `running` and one `completed` row for `E` (documents at-least-once) | one line; the job is `indeterminate` and awaits the user |
| F2 | kill during `S`; restart 10 s later | run completes; `B` runs once; total elapsed >= 5 s | same |
| F3 | kill during a burst of 1,000 `createWorkflowRun` calls; then `PRAGMA integrity_check` and reopen; repeat with the `-wal` file truncated by a random number of bytes | `integrity_check = ok`; the reopen succeeds or fails with the wrapped error, never with silent row loss of a committed run | same, plus the adapter refuses to start on `integrity_check != ok` |
| F4 | concurrency 2, lease 2 s, suspend the child (SIGSTOP or Windows debugger break) for 5 s while `E` is in flight | the hypothesis from section 5 is confirmed or refuted by counting `effects.log` lines | adapter forces concurrency 1, so it cannot occur |
| F5 | cancel while `E` is in flight | `E` completes and the run is `canceled` (matches `worker.test.ts:1380`) | `E` receives an abort; the panel stops |
| F6 (added, S-openworkflow-2) | the effect happens, then the page-side reporter posts "failed" | a raw `step.run` that throws on the report is retried, up to 10 attempts by default (`execution.ts:156-161`) | the step stays `indeterminate`; the user is shown the intent record and evidence; no one-click retry for an irreversible class |
| F7 (added, X-4, T22) | the agent principal calls the decision route, or sends the resume signal directly, with no approval record | the waiting workflow wakes (signals carry no sender identity) | refused; the workflow stays parked |
| F8 (added, X-1, T21) | a child with `archive-write` edits the job file to mark `plan:1` `completed` with a chosen output | the forged output is replayed as the planner's decision | the child cannot reach the file; if the file is altered anyway, the adapter's integrity check refuses to start |
| F9 (added in amendment) | `E` with `retryPolicy: { maximumAttempts: 1 }`, killed as in F1 | `E` runs twice: the orphaned `running` attempt is not counted (section 5 item 1) | one line; `indeterminate` |

CI hook: a `durable-jobs.acceptance.mjs` lane in the Resonant repository with an OS matrix.

Pass/fail criterion:
- The adapter column must hold on all three OSs.
- The bare column of F1 must show the duplicate. If it does not, my reading of `execution.ts:464-504` is wrong and section 5 must be revised.
- F3 must never lose a run whose `createWorkflowRun` promise resolved.
- The bare column of F9 must show the duplicate; if it does not, section 5 item 1's reading of the retry counter is wrong.
- F7 and F8 adapter columns depend on R01 and the Gate 3 state location; until those exist they are expected to fail, and the adapter must not leave the additive phase.

## 12. Recommendation and confidence

Benefits:
- the smallest embeddable durable-execution core in TypeScript;
- local SQLite with WAL and per-commit sync (on the Node build probed);
- leases with write fencing tested on SQLite;
- durable sleep;
- replay that restores planner history (fixes OSC-21 and OSC-22);
- no network code in the core;
- Apache-2.0.

Trade-offs:
- at-least-once steps with no model of an uncertain effect, and a retry policy that does not apply to the crash path;
- cancel does not abort;
- engine-level tests and the chaos test run on Postgres only, and the chaos test injects graceful stops, not crashes;
- non-atomic parent-wake;
- the CLI phones home;
- bus factor 1;
- pre-1.0.

Blockers: none for a wrap. Adopting it bare would leave T7 open. Dependencies added by the review (not blockers to the first PR, which is additive): the job DB needs the Gate 3 bridge-only state location (T21), and the indeterminate-step decision route needs R01 (agent principal without that grant) and the R19/R11 ceremony (T22) before any browser job moves to the bridge (Medium scenario).

Readiness: Small scenario now; Medium after the acceptance test passes.

Evidence quality: about 80% [inspected] code and tests, one platform probe, and the rest [reported] (docs, issues #877 and #913) or [hypothesis] (in-process double claim, macOS fsync, Windows network drives, the dashboard CDN). Nothing [executed].

Competing solutions on the same criteria:

| Criterion | OpenWorkflow 0.11.0 | dapr/durabletask-go (`a89450a`, parallel clone, read only for these rows) | Effect workflow (`effect-smol` v4 beta) | Graphile Worker / BullMQ | tool-journal (RaycarlLei, v0.3.1) |
|---|---|---|---|---|---|
| Embedding in Node 24 | library [inspected] | Go sidecar over gRPC; JS client compatibility unverified (ledger) | library, requires the Effect runtime [reported] | library, but needs Postgres (Graphile) or Redis (BullMQ) [reported] | library, Node >=24.15, not on npm [reported, ledger] |
| Storage | SQLite WAL, FULL sync (probe) | SQLite via modernc, no pragmas set, rollback journal by default, `SetMaxOpenConns(1)` (`backend/sqlite/sqlite.go:85-90, 100-119`) [inspected] | SQL incl. sqlite-node [reported] | server databases | SQLite [reported] |
| Uncertain side effect | re-executes (at-least-once) [inspected] | activities re-dispatched after `LockExpiration` (`sqlite.go:1004-1030`), at-least-once [inspected] | Activity, at-least-once [hypothesis] | at-least-once job retry | intent before execution; `indeterminate` outcome; kill test in `tests/` [reported, ledger] |
| Durable timers | yes | yes | DurableClock [reported] | delayed jobs | no |
| History integrity | none | `backend/historysigning` (signed history) [inspected: directory] | none known | none | integrity tests [reported] |
| Licence | Apache-2.0 | Apache-2.0 | MIT | MIT | MIT |
| Ops | one process | bridge + sidecar | one process | + DB server | one process |
| Maturity | 12 months, 1 maintainer | CNCF/Dapr maintainers, Linux-only CI | unstable namespace | mature | 2 weeks, 1 author |

Reading: OpenWorkflow and durabletask-go share the at-least-once activity model. durabletask-go adds signed history at the cost of a Go sidecar. tool-journal has the right semantics for the uncertain effect but no workflow engine. The recommended composition is OpenWorkflow for replay and timers plus a tool-journal-style effect journal of about 200 lines that we own.

First PR (ResonantOS Alpha repository):
- **Title:** "durable-jobs: host-side OpenWorkflow service with an effect journal (additive)".
- **Files:** `package.json` (add `openworkflow@0.11.0`, pinned), `browser-first/host/durable-jobs.mjs` (connects `BackendSqlite` at a path passed in by the caller, so that the Gate 3 bridge-only state location can be wired in without changing the module; the PR's test uses a temp directory and no user-root default is shipped; `concurrency: 1`, bounded stop wired into `browser-first/host/bridge-shutdown.mjs`), `browser-first/host/durable-effect-journal.mjs` (the `effect()` call from section 7), `browser-first/test/durable-effect-journal.test.mjs`.
- **Tests:** deterministic. A child process is killed between intent and outcome, and the test asserts `indeterminate` and a single effect; a second case reports "failed" after the effect and asserts the step stays `indeterminate` (F6). No decision route in this PR (it waits for R01 and R19).
- **Scope:** no extension changes, and no existing test changes.

Confidence: **medium**. The code reading of replay, fencing and SQLite settings is direct and cited. The duplicate-on-crash conclusion matches the project's own parallel-steps doc and the Last Light report. Confidence is not high because nothing was executed, Node 24's SQLite defaults were not probed, and upstream has no Windows or macOS lane.

## 13. Scores (for scoring/scores.csv)

Profile used: os_kernel.

| Criterion | Score | Reason (anchor) |
|---|---|---|
| requirement_fit | 3 | Checkpoint, replay, durable timers, embedded Node and survival of process restarts are present; idempotent side effects and abort-on-cancel, both explicit in R10, are absent |
| demonstrated_maturity | 3 | Releases, CI and 285+ tests (section 2 counts), but thin usage evidence (one adopter at spike stage), pre-1.0, bus factor 1 (anchor 3) |
| isolation_and_security | 1 (unchanged; reason rewritten against the D3.7/D3.8 anchor) | Rates the upstream artifact, not our effect journal (clause c). The core T7 mechanism (intent record, indeterminate status, no automatic retry) is absent, and so are the T21 and T22 mechanisms (no integrity on history, no sender identity on signals): absence scores 1 at most (clause d). No upstream test exercises the property; the lease-reclaim test (`backend.testsuite.ts:1032`) exercises a helper, and the chaos test uses graceful stops on Postgres (clause b rules out 3, and nothing designed into the artifact supports 2). Not 0: the inspected re-execution path (`execution.ts:464-504`, which retry policy does not reach) does defeat the Durability property, but only for an effect run inside a `step.run` body, and the dossier as proposed never puts one there (section 7 step 2, section 6); no advisory or counterexample row defeats a checked property. If the dossier proposed raw `step.run` for irreversible actions, this would be 0. Surface added: no listener, no network code |
| licence_suitability | 5 | Apache-2.0 file-level; MIT runtime deps (anchor 5) |
| integration_effort | 4 | Embeddable typed Node library (anchor 5), minus one: the `Backend` type is only in `/internal`, the panel-executor model needs a signal bridge with a dropped-signal race, and the effect journal must be written |
| maintenance_sustainability | 3 | Very active (weekly commits, releases every 2-4 weeks, fast PR merges), but one principal maintainer, no SECURITY.md, a 7-week-open correctness issue (#714) |
| sovereignty_and_portability | 5 | Core is local-first, data in a user-readable SQLite file, no account, no network (anchor 5); CLI telemetry excluded by using only the core |
| interoperability | 2 | No standard protocol or cross-language SDK; own schema; OTel traces optional; pluggable backend interface not public |
| operational_complexity | 5 | One process, in-process SQLite, no external service (anchor 5) |

Weighted total (os_kernel weights in `scoring/weights.json`): 0.18x3 + 0.14x3 + 0.22x1 + 0.10x5 + 0.08x4 + 0.10x3 + 0.08x5 + 0.04x2 + 0.06x5 = **3.08**, unchanged by the amendment. The score is library-only (state.md D3.7 clause c); the proposed effect journal, which is where the T7, T21 and T22 properties would come from, is unscored.

## 14. Open questions for the adversarial reviewers

1. Node 24 SQLite defaults. The FULL-sync finding comes from Node v22.20.0 on Windows. Does Node 24.21's bundled SQLite keep `DEFAULT_WAL_SYNCHRONOUS=2`? (One-line probe; not run because Node 24 is not installed here.)
2. The in-process double-claim after host sleep (section 5) is a code-reading hypothesis. Acceptance test F4 would settle it. Could timer ordering on wake make it impossible in practice?
3. I read `step.run` as never consulting `runningByStepName`. A reviewer should check for any path in `execution.ts` (for example the rerun indices in `core/rerun.ts`) that pre-marks or cleans orphaned `function` attempts. I found none.
4. The Last Light "kill -9" report (#877) is [reported]; I did not read their spike code.
5. Whether `@monaco-editor/react` in the dashboard fetches from a CDN by default is [hypothesis]; it does not matter if only the core is used.
6. The parent-wake non-atomicity applies only to child workflows. If ResonantOS never uses `step.runWorkflow`, it does not matter. Reviewers may argue it should not move the score.
7. The docs sentence "charged exactly once" (`steps.mdx:64`): is it an error, or a scoped claim about crashes after the step result was saved? I treated it as overstated, because the page does not state the scope.
8. durabletask-go rows in section 12 come from a quick read of a parallel inspector's clone; its own dossier should take precedence where they differ.

Answers found in the amendment: question 3 is now settled further. Besides `step.run` never consulting `runningByStepName`, the retry counter ignores orphaned `running` attempts (section 5 item 1), so no configuration of the bare engine prevents the crash-path re-execution. Questions 1, 2 and 4 remain open; nothing was executed.

### Review responses (2026-10-21)

All citations below are at `c82fbed`, in `packages/openworkflow/` unless stated. Nothing was executed.

| Id | Verdict | Change made (section) or evidence for dispute |
|---|---|---|
| S-openworkflow-1 | partly accepted | Accepted that one T7 rule must apply and that the old reason ("not 0 because the counterexample row is refuted") was not anchored. Re-scored against the clarified anchor (D3.7, D3.8): stays **1**, reason rewritten in section 13. Disputed that it should rise to 2: clause (d) caps "mere absence of a mechanism" at 1, and the artifact has no intent record, indeterminate status, history integrity or signal sender identity (section 5 items 1, 7, 8); clause (c) excludes our layer; clause (b) rules out credit for the lease-reclaim helper test. The missing listener and advisories are real differences from durabletask-go, but they are not one of the properties this dossier checks; they are recorded as "surface added" (sections 8, 13) pending W-5 at Gate 3. |
| S-openworkflow-2 | accepted | Section 7 steps 3 and 5: panel reports are untrusted claims (V1) and "failed" for an irreversible class stays `indeterminate`; the decision route takes only an R11 record from the R19 host ceremony, and the agent principal never holds its grant (R01, OSC-02); "verify" shows evidence, "retry" is never one click. Added that `sendSignal` carries no sender identity (`client/client.ts:278-284`), so a bare signal cannot be the approval. Section 11 F6 and F7 added; section 12 first PR tests F6 and ships no decision route. |
| S-openworkflow-3 | accepted | Section 8: forged `completed` output for `plan:<i>` is persistent prompt injection from a V3 child; replayed outputs are untrusted until R11 anchors them. Section 7: DB moved from `<userRoot>/BrowserFirst/Jobs/` to the Gate 3 bridge-only state location; section 12 first PR takes the path from the caller. Section 5 item 7 and section 11 F8 added. |
| X-1 (security) | accepted | Same changes as S-openworkflow-3; recorded as T21 in sections 5, 6, 7, 8, 11. The location itself is the lead's Gate 3 decision (state.md D3.7). |
| X-3 (security) | accepted (lead decision applied) | Section 13 states the score is library-only and the effect journal is unscored (D3.7 clause c). |
| X-4 (security) | accepted | Same changes as S-openworkflow-2; recorded as T22 in sections 5 (item 8), 6, 7 (step 5), 11 (F7). The shared approval-path design is the lead's Gate 3 item. |
| X-10 (security) | partly accepted | See S-openworkflow-1: the score now rests on the anchor text, not on a refuted counterexample. It stays 1. |
| TM-10 (security) | accepted (lead's; already in threat model v0.2) | Section 5 cites the v0.2 Durability row and T1 closure; section 6 G5 line notes that retry policy alone cannot route indeterminate outcomes to the human. No score change. |
| W-2 (security) | partly accepted | One rule, applied from the anchor text: OpenWorkflow 1, total **3.08** unchanged (section 13). Whether durabletask-go's artifact carries a mechanism for a checked property that lifts it above the clause (d) cap is for its amender and the lead; I did not re-read its clone. |
| W-5 (security) | noted (lead's; deferred to Gate 3, D3.7) | "Surface added: no listener, no network code" added as a sub-reason in section 13 and in section 8. No score change. |
| Archaeologist citation spot-check (8 rows) | no objection | All 8 PASS; no line drift to fix. Counts in section 2 already name their pattern (`grep -c "test("`). |
| Archaeologist cross-cutting 6 (STATUS lines) | accepted | Header STATUS line added. |
| D C-8 (DAO skeptic, status lines) | accepted | Header STATUS line added. |
| D C-1 (DAO skeptic, two-candidate tables cannot show FRAGILE, incl. R10) | noted (lead's scoring method) | No change to this dossier's scores. The R10 margin to durabletask-go (3.08 versus 3.02) is the lead's to report. |
| D (OS dossiers, I2 check) | no objection | Reviewer confirms the G4/G5 lines; G5 line kept, wording extended (section 6). |

New finding from the amendment (no reviewer raised it): `retryPolicy: { maximumAttempts: 1 }` does not stop re-execution after a crash, because `maximumAttempts` is compared with the count of `failed` attempts only (`core/workflow-definition.ts:193-197`, `worker/step-history.ts:56-60, 311-313`). Sections 5, 6, 11 (F9) and 12 amended. It strengthens the case that the T7 property must come from the effect journal, and it does not change any score.
