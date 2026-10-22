# Stage 3 adversarial review: code archaeologist

STATUS: COMPLETE (2026-10-21)

Role: code archaeologist. Agent id: s3-rev-archaeologist. Model: Claude Opus 5.5 (claude-opus-5-5). Date: 2026-10-21.

## Header

**Method.** I extracted every backticked `path:line` citation from each dossier with a small read-only script (`<scratchpad>\s3-rev-archaeologist\cites.py`). From each list I picked the citations that carry a reuse decision, a hard-gate verdict, a property verdict or a score reason. I read the cited lines from the git object at the dossier's recorded SHA with `git -c core.hooksPath=/dev/null -C "<clone>" show <sha>:<path>` (helper `show.py`), so working-tree drift cannot affect a result. I re-ran counts with `git grep` or `git ls-tree` at the same SHA. One supporting file outside `research\_untrusted\` (hypercore-storage) came from a read-only `gh api repos/holepunchto/hypercore-storage/contents/index.js?ref=dc65f66` GET, saved under `<scratchpad>\s3-rev-archaeologist\ext\`. Nothing from any clone was executed, installed or built. I also compared `scoring\scores.csv` with each dossier's section 13 mechanically (`s13.py`).

**Verdict scale.** PASS means the cited lines say what the dossier says they say. PARTIAL means the claim is right but the citation is off by a few lines, or points at a comment, README or permission set rather than the code that carries the claim. FAIL means the cited lines do not contain the claimed content.

**Dossiers read** (last-modified time as seen on 2026-10-21):

| Dossier | Modified | Clone and SHA checked | HEAD equals recorded SHA |
|---|---|---|---|
| aaif-goose.md | 2026-10-21 10:23 | `aaif-goose` 9920efa | yes |
| anthropics-sandbox-runtime.md | 2026-10-20 15:03 | `anthropics-sandbox-runtime` c40cf14 | yes |
| convira-sandbox.md | 2026-10-20 15:00 | `convira-sandbox` 9013c32 | yes |
| dapr-durabletask-go.md | 2026-10-20 15:01 | `dapr-durabletask-go` a89450a | yes |
| datalad.md | 2026-10-21 10:14 | `datalad` 77de8d9 | yes |
| eclipse-biscuit.md | 2026-10-20 15:00 | `eclipse-biscuit/biscuit-rust` 93832a8, `eclipse-biscuit/biscuit-wasm` 80cceed | yes (two sub-clones) |
| getaegis-aegis.md | 2026-10-20 15:00 | `getaegis-aegis` f1321b3 | yes |
| holepunchto-hypercore.md | 2026-10-20 15:00 | `holepunchto-hypercore` 9c9cc3d; hypercore-storage dc65f66 via gh api | yes |
| hypercerts-lexicon.md | 2026-10-21 10:15 | `hypercerts-lexicon` db1f41c | yes |
| identity-common-ts.md | 2026-10-21 10:15 | `identity-common-ts` 42586ca | yes |
| nanobrowser.md | 2026-10-20 14:59 | `nanobrowser` f1e912d | yes |
| openworkflow.md | 2026-10-20 15:00 | `openworkflow` c82fbed | yes |
| solana-foundation-rewards.md | 2026-10-21 10:17 | `solana-foundation-rewards` HEAD 0b1bf17, branch commit 119f5f5 | yes (HEAD; branch citations read at 119f5f5) |
| transparency-dev-tessera.md | 2026-10-20 15:03 | `transparency-dev-tessera/tessera` 012e9e0 | yes |
| tuf-js.md | 2026-10-21 10:18 | `tuf-js` a399ce8 | yes |

Every clone's working tree was clean (`git status --porcelain` empty) except the two parent folders, which are not repositories: `eclipse-biscuit\` and `transparency-dev-tessera\`.

**Headline.** I checked 165 decision-carrying citations: 158 PASS, 6 PARTIAL, 1 FAIL. That is 95.8 % exact and 99.4 % substantively right. No checked citation contradicts the claim it supports. I re-ran 14 counts and 11 reproduced. In four dossiers the line numbers have drifted by 1 to 14 lines. Two dossiers label as `[inspected]` behavioural claims that are sourced from a README. Of the six relaunched dossiers, five are clean. In the sixth, datalad, one citation inherited from the first run fails, although the dossier header says the findings were "re-opened and re-confirmed".

---

## aaif-goose

Relaunched dossier. Citations checked at 9920efa:

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | `crates/goose/src/permission/permission_inspector.rs:159-161` | Auto mode allows before any user permission (NeverAllow ignored) | PASS (line 161 `GooseMode::Auto => InspectionAction::Allow` precedes the user-permission lookup at 164) |
| 2 | `crates/goose/src/acp/server/tools.rs:111-114` | ACP `tools/call` only in Auto mode, no inspector | PASS |
| 3 | `crates/goose/src/acp/server/tools.rs:154-168` | any ACP client rewrites tool permissions | PASS |
| 4 | `crates/goose/src/posthog.rs:42-52` | telemetry opt-in in code | PASS |
| 5 | `crates/goose-cli/src/commands/configure.rs:211` | CLI consent prompt defaults yes | PASS (`.initial_value(true)`) |
| 6 | `ui/desktop/src/components/onboarding/OnboardingSuccess.tsx:51` | desktop checkbox defaults yes | PASS (`useState(true)`) |
| 7 | `crates/goose-cli/src/cli.rs:1811-1825` | `serve` refuses without secret unless `--dangerously-unauthenticated` | PASS |
| 8 | `crates/goose/src/config/base.rs:1279-1285` | mode resolves to Auto when unset | PASS |
| 9 | `crates/goose/src/agents/extension_manager/stdio.rs:30-35` | stdio child inherits parent env | PASS (no `env_clear`) |
| 10 | `.github/workflows/ci.yml:269-290` | Windows gets `cargo build` only, push to main only | PASS (`if:` at 272) |
| 11 | `crates/goose/src/security/mod.rs:58-73` | security inspector default false | PASS |
| 12 | `crates/goose/src/tool_inspection.rs:170-261` | non-permission inspectors only tighten | PASS |
| 13 | `crates/goose/src/subprocess.rs:34-45` | `git_command()` sets `safe.bareRepository=explicit`, `core.fsmonitor=false` | PASS |
| 14 | `crates/goose/src/posthog.rs:556-604` | `emit_event` does not check consent | PASS |
| 15 | `crates/goose/tests/git_command_security.rs` `#[cfg(unix)]` on the last two tests | Windows not covered | PASS (`:47`, `:87`) |

Counts: 4,443 `#[test]`/`#[tokio::test]` attributes PASS; 114 desktop test files PASS; top five authors with 92 of 200 commits PASS; 39 integration test files does not reproduce (see 1).

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| A-aaif-goose-1 | 3 | "39 integration test files in `crates/goose/tests/`" (L90) | `git ls-tree --name-only 9920efa crates/goose/tests/` gives 34 top-level `.rs` files. Counting recursively gives 38. Neither is 39. | minor | State the command used, or correct the figure. |
| A-aaif-goose-2 | 14, 6 (G1) | "who calls the consent-unchecked `emit_event` path is not established" (L306 area) | This can be settled now. The only Rust callers are `scheduler/full.rs:941, 1061` (`schedule_job_started`, `schedule_job_completed`). `emit_event` drops both because only `onboarding_*` and `telemetry_preference_set` pass (`posthog.rs:562-566`). The onboarding names occur only in `ui/desktop/src/utils/analytics.ts:37-45, 252-282`, whose sender is a no-op "during the ACP migration" (`analytics.ts:4-5, 12-17`). So nothing is sent before consent at HEAD. But the code states the intent to do so: "These bypass the telemetry check so we can track the funnel before the user makes their choice" (`posthog.rs:560-561`). | minor | Close the open question in section 14. Keep the G1 WARN, and name the latent pre-consent funnel as a re-check item for every goose upgrade. |
| A-aaif-goose-3 | 3 (counterexample row) | "every goose-initiated git call goes through `git_command()`" plus three regression tests (L92) | `git_command()` neutralises fsmonitor and implicit bare repositories only. Nothing in it covers `diff.external` (`subprocess.rs:34-45`). That protection is a per-call `--no-ext-diff` flag in `review/handler.rs:369, 400, 424`. The test `does_not_execute_repository_diff_external` adds `--no-ext-diff` itself (`git_command_security.rs:134-135`), so it tests git's flag, not goose's call sites. Any future `git diff` call that omits the flag is unprotected, and no test would catch it. | minor | Reword: "fsmonitor and bare-repo hardening is central; ext-diff hardening is per call site." |
| A-aaif-goose-4 | header, 2 | Claims marked "[inspected by h1]" or "h2" | Two helper agents traced many decision-carrying rows (provider fallback, keyring fallback, diagnostics redaction, `AGENT_SESSION_ID`). The spot-checks above that touched helper rows (9, 14) passed. Still, the article's evidence-quality figure should count these rows as second-hand inspection, not first-hand. | minor | The lead decides how to count them; no dossier change needed. |

## anthropics-sandbox-runtime

Citations checked at c40cf14:

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | `src/sandbox/windows-sandbox-utils.ts:4230` | library always passes `--write-restricted-token` | PASS |
| 2 | `src/sandbox/sandbox-manager.ts:2626-2643` | network restriction whenever `allowedDomains` is defined | PASS |
| 3 | `src/sandbox/linux-sandbox-utils.ts:1343-1355` | bwrap check warns only below 0.5.0 | PASS |
| 4 | `src/sandbox/sandbox-manager.ts:1634-1635` | unsupported platform fails closed | PASS |
| 5 | `vendor/srt-win-src/src/token.rs:29-42` | restricting SIDs exclude Users and Authenticated Users | PARTIAL (see 1) |
| 6 | `src/sandbox/windows-sandbox-utils.ts:4250-4262` | child env limited to PATH, PATHEXT and generated vars | PASS |
| 7 | `.github/workflows/integration-tests.yml:16-37` | six legs, including Windows x64 and arm64 | PASS |
| 8 | `src/utils/config-loader.ts:20, 78` | only the config loader validates the schema | PASS (`git grep SandboxRuntimeConfigSchema` finds no call in `initialize`) |
| 9 | `vendor/srt-win-src/src/job.rs:22-76` | kill-on-close Job | PASS |
| 10 | `vendor/srt-win-src/src/launch.rs:167-169` | child Job has `breakaway_ok = false` | PASS |
| 11 | `README.md:772-780` | WFP `ALE_AUTH_CONNECT` filters, under an "[inspected]" heading | PARTIAL (see 2) |

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| A-anthropics-sandbox-runtime-1 | 3 (#402) | "restricting SIDs exclude `Users` and `Authenticated Users` (`token.rs:29-42`)" (L53) | The cited lines are a module doc comment, not code. The code is `restricting_sid_list` (`token.rs:93-106`). It lists the session capability SIDs, the sandbox user, `SID_EVERYONE` and `SID_RESTRICTED`, which confirms the claim. It also shows that Everyone-writable locations stay writable. The dossier does record that residual elsewhere (property table, README 797). | minor | Cite `token.rs:93-106` alongside or instead of the doc comment. |
| A-anthropics-sandbox-runtime-2 | 2 (per-OS backends, labelled [inspected]) | Windows network and filesystem mechanisms cited only to `README.md:772-780, 784-793` (L27) | The row heading says [inspected], but these two mechanisms are cited to the README. The code exists and agrees: `vendor/srt-win-src/src/wfp.rs` (1,224 lines) has `FWPM_LAYER_ALE_AUTH_CONNECT_V4/_V6` (`:74, :427-428`), the loopback permit weight (`:392-421`) and the open-loopback port range (`:104-109`). | minor | Cite `wfp.rs` and `acl.rs`, or mark these two sentences [reported]. |

## convira-sandbox

Citations checked at 9013c32, all in `packages/sandbox-runtime/`:

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | `src/adapters/native-linux.ts:315-316, 345-346` | Linux isolation flags hard-coded true | PASS |
| 2 | `src/adapters/native-linux.ts:516-530` | `allowLoopback` ignored; `enabled` shares host netns | PASS |
| 3 | `src/adapters/native-linux.ts:539-542` | seccomp silently skipped | PASS (`catch { // degrade gracefully }`) |
| 4 | `src/adapters/native-windows.ts:224-233` | loopback-only grant refused at spawn | PASS |
| 5 | `src/adapters/native-windows.ts:273-282` | Windows adapter now throws instead of unwrapping | PASS |
| 6 | `__tests__/win-appcontainer.test.ts:401-469` | Windows enforcement tests `return` early off-platform, so they report passed | PASS (`if (!onWindows) return;` at 403 and following) |
| 7 | `src/win-appcontainer.ts:652-659` | network probe tests loopback only | PASS |

No objections. Every checked citation matches, and the dossier already reports the off-platform early-return tests and the hard-coded Linux and macOS flags.

## dapr-durabletask-go

Citations checked at a89450a:

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | `backend/sqlite/sqlite.go:1010` | activity leases use `WorkflowLockTimeout` | PASS (`ActivityLockTimeout` is only declared, at `:39, :60`) |
| 2 | `backend/sqlite/sqlite.go:55-62` | 2-minute default leases | PASS |
| 3 | `main.go:27` | `grpc.NewServer()` with no credentials | PASS |
| 4 | `backend/sqlite/sqlite.go:122-139` | `DeleteTaskHub` removes an open file | PASS |
| 5 | `backend/sqlite/sqlite.go:100-109` | `CreateTaskHub` panics | PASS |
| 6 | `backend/runtimestate/propagation.go:79` | `historysigning` used only for `MarshalEvent` | PASS (`git grep historysigning` outside its package) |
| 7 | `backend/executor.go:447` | `CancelActivityTask` called only on shutdown | PASS |
| 8 | `backend/sqlite/sqlite.go:115` | `SetMaxOpenConns(1)`; no PRAGMA | PASS (`git grep -i pragma backend/sqlite` is empty) |
| 9 | `backend/historysigning/verify.go:154-241` | empty history verifies; tail truncation undetected | PASS (`:155-157`; coverage check `expectedStart == len(events)` at about 236) |
| 10 | `backend/historysigning/canonical.go:73-86` | own-history signatures bind no instance id | PASS (`ctx == nil` path) |
| 11 | `tests/orchestrations_test.go:2231-2249` | orchestration tests use in-memory SQLite | PASS |
| 12 | `tests/grpc/grpc_test.go:45-47` | gRPC suite in-memory | PASS |
| 13 | `tests/backend_test.go:27-35` | file-backed backend only in the backend suite | PASS |

No objections.

## datalad

Relaunched dossier. Citations checked at 77de8d9:

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | `datalad/core/local/run.py:1051-1072` | run-record fields | PASS |
| 2 | `run.py:1097-1099` | `exit` added after execution | PASS |
| 3 | `run.py:832` | `json.dumps(..., sort_keys=True)` | PASS |
| 4 | `run.py:1132-1141` | commit-message markers `[DATALAD RUNCMD]` ... | **FAIL**: the lines are output-glob expansion and `_create_record`; the markers are at `run.py:1144-1151` |
| 5 | `run.py:850-855` | sidecar not rewritten when the path exists | PASS |
| 6 | `run.py:894-898` | `inject=True` docstring | PASS |
| 7 | `datalad/core/local/tests/test_run.py:498-509` | `test_inject` | PASS |
| 8 | `run.py:1178` | without `--explicit` the save covers everything | PASS |
| 9 | `run.py:941-945` | rerun `pwd` joined without containment | PASS |
| 10 | `datalad/local/rerun.py:593` | rerun executes `run_info['cmd']` | PASS |
| 11 | `run.py:758-774` | executed as a shell string | PASS (`WitlessRunner`; `nonasyncrunner.py:395` `shell=True if isinstance(cmd, str)`) |
| 12 | `rerun.py:733-778` | regex plus `json.loads` parser | PASS |
| 13 | `datalad/support/json_py.py:104-118` | non-atomic sidecar writer | PASS |
| 14 | `tools/ci/test-jobs.yml:148-164` | three `windows-2022` jobs | PASS |
| 15 | `datalad/support/annexrepo.py:146`, `gitrepo.py:846` | version floors | PASS |
| 16 | `datalad/cli/common_args.py:123-133` | `-f/--output-format` | PASS |

Counts: 25 tests in `test_rerun.py` PASS; 1,272 `def test_` PASS; Windows known-failure markers in rerun tests PASS (4 in `test_rerun.py`, 2 in `test_run.py`).

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| A-datalad-1 | 2 | "Commit message format, fixed markers (`run.py:1132-1141`)" (L32) | At 77de8d9 the markers are at `run.py:1144-1151` (`git show 77de8d9:datalad/core/local/run.py`, lines 1144-1151). The cited range is glob expansion and the `_create_record` call. This is the reused-citation failure mode: the header says the first run's findings were "re-opened and re-confirmed before being cited here". The same 10-line span recurs in the "Provenance of derivations" row (L96) and in the R14 effort estimate (L124, "the message format 10 lines"). | minor | Correct all three occurrences to `run.py:1144-1151` and re-verify any other inherited range. |
| A-datalad-2 | 8 (rerun executes stored text) | The rerun attack surface covers `cmd` and `pwd` only (L179) | `get_run_info` has a second path-from-commit-message input. When the JSON is a string (a sidecar id), it opens `op.join(dset.path, record_dir, runinfo)` with no containment check and LZMA-decodes it (`rerun.py:764-775`). A crafted commit can point rerun at any readable file. This is a read-only parsing surface, not execution, and the recommended design does not use `datalad rerun`. | minor | Add one sentence to section 8. It is for the security reviewer's tally, not a decision change. |

## eclipse-biscuit

Citations checked at biscuit-wasm 80cceed and biscuit-rust 93832a8:

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | wasm `src/lib.rs:21-22` | `wee_alloc` global allocator | PASS |
| 2 | wasm `Cargo.toml:20` | `wee_alloc = "0.4.5"` | PASS |
| 3 | wasm `Cargo.toml:15` | `biscuit-auth = "6.0.0"` | PARTIAL: it is at `:14` |
| 4 | wasm `Cargo.lock:39-40` | locked 6.0.0 from crates.io | PASS |
| 5 | wasm `src/lib.rs:323-324` | `KeyProvider` `.unwrap()` panics | PASS |
| 6 | wasm `src/lib.rs:143-153` | revocation ids accessor only | PASS |
| 7 | wasm `src/authorizer.rs:22` | 20 ms default timeout | PASS |
| 8 | wasm `src/lib.rs:337-343` | logger to console only (G1) | PASS |
| 9 | rust `biscuit-auth/src/token/mod.rs:205-217` | `revocation_identifiers()` is the only revocation code | PASS |
| 10 | rust `biscuit-auth/src/token/mod.rs:1619` | CVE-2024-41949 regression test | PASS |
| 11 | rust `biscuit-auth/src/token/builder/authorizer.rs:258-263` | `time()` helper uses `SystemTime::now` | PASS |

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| A-eclipse-biscuit-1 | 1 | `biscuit-auth = "6.0.0"` at `Cargo.toml:15` (L21) | Off by one: the line is 14 at 80cceed. | minor | Correct the line. |
| A-eclipse-biscuit-2 | 2 | `js-tests/index.js` has "no negative assertion ... (grep for `throws|catch|fail|error` returns nothing). Every one of its seven tests ..." (L47) | Two parts of the sentence do not reproduce. A case-insensitive grep matches `js-tests/index.js:188` (`throw new Error("Unknown key id: ...")`), which the dossier itself cites at L89. And the file has eight `test(` calls (`:24, 36, 87, 113, 131, 162, 249, 313`), not seven. The substantive claim holds: line 188 is a provider throwing, not an assertion, and no test asserts a refusal. | minor | Reword the grep sentence and correct the count to eight. |

## getaegis-aegis

Citations checked at f1321b3:

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | `src/gate/gate.ts:315` | `listen(this.port, cb)` with no host | PASS |
| 2 | `src/gate/gate.ts:153` | `requireAgentAuth` default true | PASS |
| 3 | `src/gate/gate.ts:1143-1153` | header stripping | PASS |
| 4 | `src/gate/gate.ts:1299-1309` | upstream always port 443 unless the test hook | PASS |
| 5 | `src/dashboard/dashboard-server.ts:183` | dashboard binds all interfaces | PASS |
| 6 | `src/dashboard/dashboard-server.ts:236-239` | `Access-Control-Allow-Origin: *` | PASS |
| 7 | `src/mcp/mcp-server.ts:961` | MCP HTTP binds 127.0.0.1 | PASS |
| 8 | `src/key-storage/credential-manager-windows.ts:77-79` | master key on the `cmdkey /pass:` argv | PARTIAL: `setKey` starts at 79; the `cmdkey` call is at `:81` |
| 9 | `.github/workflows/release.yml:98-101` | silent publish without provenance | PASS |
| 10 | `src/gate/gate.ts:516-522` | `/_aegis/stats` unauthenticated | PASS |

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| A-getaegis-aegis-1 | 8 | `cmdkey /pass:<master key>` at `credential-manager-windows.ts:77-79` (L147) | Line drift: the `execFileSync('cmdkey', [..., '/pass:${key}'])` call is at `:81`. The claim is correct. | minor | Cite `:79-83`. |

## holepunchto-hypercore

Citations checked at 9c9cc3d. hypercore-storage was read at dc65f66 through gh api.

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | `index.js:962-965` | `get` returns stored bytes without re-hashing | PASS |
| 2 | `index.js:1137-1143` | `truncate` needs only the key | PASS |
| 3 | `lib/core.js:204` | key pair generated by default | PASS |
| 4 | `test/conflicts.js:4` | equivocation test is `test.skip` | PASS |
| 5 | `index.js:1156-1158` | per-append `keyPair` override | PASS |
| 6 | `lib/audit.js:29-33` | audit deletes the core unless `dryRun` | PASS |
| 7 | `lib/verifier.js:20` | Ed25519 only | PASS |
| 8 | hypercore-storage `index.js:650-656` | on recovery, writes RECOVERING and deletes WAL `.log` files | PASS |
| 9 | hypercore-storage `index.js:1342-1373` | `tmpFixStorage` moves unknown files into `db/` | PASS |

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| A-holepunchto-hypercore-1 | header, 3, 8 | Supporting clones "kept outside `research\` in the inspector's scratchpad (`s3-insp-hypercore-ext\`)" (L3) | That folder no longer exists: the current session scratchpad has no `s3-insp-hypercore-ext`. So the decision-carrying WAL-deletion and `tmpFixStorage` citations cannot be reproduced from `research\_untrusted\`. I verified both through `gh api` at dc65f66, and both pass. The objection is to reproducibility only. | minor | Clone hypercore-storage, hypercore-crypto and rocksdb-native under `research\_untrusted\holepunchto-hypercore-ext\` at the recorded SHAs, or record the gh api commands in the dossier. |

## hypercerts-lexicon

Relaunched dossier. Citations checked at db1f41c:

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | `lexicons/org/hypercerts/authWrite.json:8-28` | permission set grants create, update and delete on evaluation and others | PASS |
| 2 | `authWrite.json:28` | "Authority over a record is the repo owner's" | PARTIAL (see 1) |
| 3 | `lexicons/app/certified/badge/award.json:42` | "Expiry is not revocation; to revoke an award, the issuer deletes the record" | PASS |
| 4 | `lexicons/org/hypercerts/context/evaluation.json:11` | `evaluators`, `summary`, `createdAt` required | PASS |
| 5 | `evaluation.json:13-17` | `subject` optional | PASS |
| 6 | `lexicons/org/hypercerts/context/acknowledgement.json:7` | created in the acknowledging actor's repo | PASS |
| 7 | `lexicons/app/certified/signature/defs.json:17-31` | CIDv1 signing recipe | PASS |
| 8 | `.github/workflows/test.yml:11` | Linux-only CI | PASS (`blacksmith-4vcpu-ubuntu-2404`) |
| 9 | `test.yml:25-27` | `sed` patch of lex-cli | PASS |
| 10 | `docs/design/permission-sets.md:79-81` | records world-readable | PASS (labelled "[inspected doc]") |
| 11 | `tests/validate-signing-example.test.ts:247-254` | single round-trip signature test | PASS |
| 12 | `README.md:331-340` | validators do not reject values outside `knownValues` | PARTIAL (see 2) |

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| A-hypercerts-lexicon-1 | 4, 5 (DR-28), 8 | "Authority over a record is the repo owner's: the owner may create, update and delete (`authWrite.json:28`)" (L74, also L139, L216, L297) | `org.hypercerts.authWrite` is an OAuth permission set: it says what a third-party app may be granted on the user's repo ("Create, edit, and delete your Hypercerts records", `:8`). The owner's power to edit and delete comes from ATProto repo semantics, not from this file, and holds whatever the permission set says. The conclusion (owner-mutable, deletable evaluations) stands. The citation proves something narrower: that apps can be granted mutation rights too. | minor | Cite ATProto repo semantics [reported], and keep `authWrite.json` as evidence that third-party apps can also mutate. |
| A-hypercerts-lexicon-2 | 2 (cross-cutting semantics, labelled [inspected]) | "`knownValues` are open vocabularies, not enums; validators do not reject other values (`README.md:331-340`)" (L47) | This is a behavioural claim about `@atproto/lexicon`, sourced from README prose under an [inspected] label. No test in `tests/` submits a value outside `knownValues`. The only reference, `tests/validate-location.test.ts:35`, checks that the list contains a value. The claim matters for section 8(d), "any validator-based check on `contentType` ... is advisory". | minor | Relabel [reported], or cite the `@atproto/lexicon` validator source for string `knownValues`. |

## identity-common-ts

Relaunched dossier. Citations checked at 42586ca:

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | `packages/sd-jwt-core/src/index.ts:248-250` | KB-JWT skipped unless `keyBindingNonce` | PASS |
| 2 | `packages/sd-jwt-core/src/kbjwt.ts:82-84` | KB signature not tied to `cnf` by the library; payload handed to `kbVerifier` | PASS |
| 3 | `kbjwt.ts:53-60` | audience check only when `expectedKeyBindingAudience` is set | PASS |
| 4 | `packages/sd-jwt-core/src/sdjwt.ts:24` | `saltGenerator(16)` | PASS |
| 5 | `packages/crypto/src/crypto.ts:3-14` | 16 hex characters from 8 random bytes | PASS (`new Uint8Array(length / 2)`) |
| 6 | `packages/token-status-list/src/status-list.ts:85-97` | `inflate` without output cap | PASS |
| 7 | `packages/sd-jwt-core/src/__tests__/index.test.ts:211-259` | vacuous test (try/catch, no nonce) | PASS |
| 8 | `.github/workflows/ci.yml:56-63` | ubuntu-24.04, Node 22, 24 and 26 | PASS |
| 9 | `MAINTAINERS.md:9-16` | six maintainers, four companies | PASS |
| 10 | `packages/crypto/src/crypto.ts:75-151` | only ES256, ES384 and ES512 helpers | PASS |
| 11 | `packages/sd-jwt-vc/src/sd-jwt-vc-instance.ts:587-588` | status-list token verified with time options | PASS |

No objections. All eleven citations pass, including the two security findings (the vacuous test and 64-bit salts). For precision only, the README Quick Start uses `randomBytes(16)` (128-bit, `packages/sd-jwt-core/README.md:45`), so the 64-bit salt issue is confined to `@owf/crypto` and the examples, exactly as the dossier says.

## nanobrowser

Citations checked at f1e912d:

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | `.github/workflows/ci.yml:1-2` | browser and model checks run by hand, not in CI | PASS |
| 2 | `ci.yml:36` | unit tests in CI | PASS |
| 3 | `src/browser-control/core/interaction/classify.ts:175-187` | unlabelled payment control falls through to `null` | PASS |
| 4 | `src/store/settings.ts:56-57` | analytics on by default | PASS |
| 5 | `src/store/settings.ts:118-119` | keys stored plaintext in `nb.keys` | PASS |
| 6 | `src/extension/prompt-broker.ts:129-130` | "always allow" writes a permanent rule | PASS |
| 7 | `src/browser-control/core/probe-client.ts:49-62` | isolated world, `grantUniversalAccess: false` | PASS |
| 8 | `src/browser-control/core/interaction/gate.ts:178-197` | pay and grant throw `USER_STEP` | PASS, with condition (see 2) |
| 9 | `wxt.config.ts:28` | `<all_urls>` | PASS |

Counts: 73 test files PASS; 228 `defineScenario` PASS; 55 `defineCheck` PASS; 522 `it(` cases does not reproduce (see 1).

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| A-nanobrowser-1 | 2 | "73 test files, 522 `it(` cases" (L37) | At f1e912d, 509 lines match `^\s*it\(` and 516 match once `it.each`, `it.skip`, `it.only` and `it.todo` are included. A bare substring grep for `it(` overcounts because it also matches `submit(`. 522 is not reproduced by any of these. | minor | State the regex used or correct the figure. |
| A-nanobrowser-2 | 2 (feature table) | "`178-197` protected steps throw `USER_STEP`" (L25) | Both branches are conditioned on `session.handover` (`gate.ts:179, 190`). In a non-handover session (the test panel), pay and grant fall through to the fixed confirmation policy (`gate.ts:209-212`). The control-flow paragraph (L55) states the condition, but the feature table, which readers are likely to quote, does not. | minor | Add "in a handover (agent) session" to the table row. |

## openworkflow

Citations checked at c82fbed, in `packages/openworkflow/` unless stated:

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | `sqlite/sqlite.ts:56-61` | `busy_timeout`, WAL for files, `foreign_keys = ON` | PASS |
| 2 | `core/workflow-function.ts:32-33` | step function has no arguments and no `AbortSignal` | PASS |
| 3 | `worker/step-history.ts:79-83` | default wait timeout one year | PASS |
| 4 | `worker/worker.ts:142-157` | `stop()` waits with no upper bound | PASS |
| 5 | `apps/docs/docs/steps.mdx:62-64` | doc claims "charged exactly once" | PASS |
| 6 | `sqlite/backend.ts:76-101` | ownership fencing `AND worker_id = ?` | PASS |
| 7 | `apps/cli/telemetry.ts:30-58` | CLI telemetry opt-out | PASS |
| 8 | `worker/execution.ts:155-161` | default step retry, 10 attempts | PASS |

No objections. The dossier already separates the documentation claim from the code at L44.

## solana-foundation-rewards

Relaunched dossier. Citations checked at HEAD 0b1bf17 unless stated:

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | `program/src/traits/distribution.rs:29-34` | `validate_authority` is plain equality | PASS |
| 2 | `program/src/state/revocation.rs:12-24` | revocation marker PDA | PASS |
| 3 | `program/src/instructions/merkle/claim/processor.rs:35-45` | leaf over claimant; `verify_not_revoked` | PASS |
| 4 | `program/src/instructions/direct/revoke_recipient/accounts.rs:40` | single authority signer | PASS |
| 5 | `program/src/state/direct_distribution.rs:27` | authority in PDA seeds | PASS |
| 6 | `audits/AUDIT_STATUS.md:12` | "resolved and re-reviewed in PRs #32-#37" | PASS |
| 7 | `audits/AUDIT_STATUS.md:14-18` | "immutable tags/releases" promised | PASS (`git tag` is empty) |
| 8 | `tests/integration-tests/src/test_revoke_merkle_claim.rs:356` | `test_claim_after_revocation_fails` | PASS |
| 9 | `program/src/lib.rs:33` | program id | PASS |
| 10 | `.github/workflows/release.yml:151, 171` | Doppler `SQUADS_VAULT`; CI key is fee payer only | PASS |
| 11 | `program/src/utils/points_cpi.rs:85` at 119f5f5 | `freeze_authority: None` | PASS |
| 12 | `revoke_points/accounts.rs:33` at 119f5f5 | single authority signer | PASS |
| 13 | `transfer_points/accounts.rs:39-41` at 119f5f5 | authority and `from_user` must sign | PASS |

Counts: 219 integration `#[test]` and 315 unit `#[test]` PASS.

No objections. Every check against HEAD and against the unmerged branch passes, and the dossier marks each branch citation with its commit.

## transparency-dev-tessera

Citations checked at 012e9e0:

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | `storage/posix/files.go:224` | `syscall.Flock(..., LOCK_EX)` | PASS |
| 2 | `storage/posix/files.go:233` | `LOCK_UN` | PASS |
| 3 | `.github/workflows/go_test.yml:10-14` | `os: [ubuntu-latest]` only | PASS |
| 4 | `client/client.go:397-399` | equal or smaller checkpoint silently accepted | PASS (returns the cached state before any root comparison) |
| 5 | `append_lifecycle.go:1250-1255` | `FailOpen` "will be disabled and/or removed" | PASS |
| 6 | `integration/fault/posix/fault_test.go:15` | `//go:build linux` | PASS |
| 7 | `storage/posix/file_ops.go:44` | `syscall.O_DIRECTORY` | PASS |
| 8 | `storage/posix/file_ops.go:130` | `os.Link` | PASS |
| 9 | `log.go:45` | `type Driver any` | PASS |

No objections. The Windows non-buildability claim rests on these lines plus a reading of the Go standard library through gh api. It is correctly labelled "[inspected stdlib source; not compiled]".

## tuf-js

Relaunched dossier. Citations checked at a399ce8, in `packages/` unless stated:

| # | Citation | Claim | Result |
|---|---|---|---|
| 1 | `client/src/updater.ts:85-94` | forceCache loads local timestamp, root only on throw | PASS |
| 2 | `client/src/updater.ts:237-239` | empty catch swallows local failure | PASS |
| 3 | `client/src/updater.ts:242-252` | falls through to remote, verified against the old root | PASS |
| 4 | `client/src/updater.ts:305-307` | `RuntimeError` on snapshot | PASS |
| 5 | `client/src/updater.ts:318-320` | cached role returned whatever the delegator | PASS |
| 6 | `models/src/file.ts:228-246` | `TargetFile.fromJSON` accepts `{}` hashes | PASS |
| 7 | `models/src/file.ts:175-187` | digests built from `Object.keys(hashes)` (so empty means length only) | PASS |
| 8 | `models/src/metadata.ts:101-121` | threshold over a set of distinct verified key ids | PASS |
| 9 | `models/src/utils/key.ts:21-35` | no Sigstore key type | PASS |
| 10 | `.github/workflows/ci.yml:44-50` | unit tests on ubuntu, macOS and Windows | PASS |
| 11 | `client/src/store.ts:140-143` | timestamp stored before the freeze check | PASS |

No objections. The root-skip finding (section 3) is the most consequential code claim in the DAO-adjacent set, and every link of its chain checks out at a399ce8.

---

## Cross-cutting

1. **Citation quality is high.** 158 of 165 checked citations are exact, 6 are substantively right with drift or an indirect source, and 1 fails. None contradicts its claim. Drift is small (1 to 14 lines) and limited to datalad, eclipse-biscuit, getaegis-aegis and, as indirect sources, anthropics-sandbox-runtime and hypercerts-lexicon. For the article: "95.8 % of 165 spot-checked decision-carrying citations matched exactly at the recorded SHA; 99.4 % supported the claim."
2. **The reused-citation risk was real but small.** Five of the six relaunched dossiers (goose, identity-common-ts, tuf-js, solana-foundation-rewards, hypercerts-lexicon) passed every exact-line check. datalad carries one inherited range that fails (A-datalad-1) despite its header saying the findings were re-confirmed. tuf-js's explicit "every file:line cited below was re-opened" is borne out by its 11 of 11.
3. **Counts lack the command that produced them.** Of 14 counts re-run, 11 reproduce and 3 do not: goose "39 integration test files", nanobrowser "522 `it(`" and biscuit-wasm "seven tests". In each case the dossier does not say how it counted. One line in each dossier naming the `git grep` or `ls-tree` used would make every count checkable.
4. **"[inspected]" sometimes covers README text.** anthropics-sandbox-runtime (Windows WFP and ACL mechanisms) and hypercerts-lexicon (validator behaviour for `knownValues`) put README-sourced behavioural claims under an [inspected] label. Several other dossiers use [inspected] for statements about what a document says (MAINTAINERS, CHANGELOG, AUDIT_STATUS, THREAT_MODEL). That use is legitimate, but the evidence-quality figure should not count those rows as code inspection. goose also delegates many [inspected] rows to helper traces (h1, h2).
5. **Tests that do not run, or run vacuously, are well reported.** Every case I probed was already disclosed by its inspector: goose's Rust tests never run on Windows, datalad's Windows known-failure markers, convira's early-return Windows tests that pass off-platform, hypercore's skipped equivocation test, nanobrowser's manual autorun, biscuit-wasm's lack of negative tests, identity-common-ts's vacuous KB test, and Linux-only CI for tessera and hypercerts. I found no dossier that calls a property "demonstrated by test" while citing a skipped test.
6. **State drift: STATUS lines.** The launch message says all fifteen dossiers carry STATUS: COMPLETE. Only the six relaunched dossiers do (`grep -c '^STATUS'`). The nine 2026-10-20 dossiers (anthropics-sandbox-runtime, convira-sandbox, dapr-durabletask-go, eclipse-biscuit, getaegis-aegis, holepunchto-hypercore, nanobrowser, openworkflow, transparency-dev-tessera) have no STATUS line at all. Following the state-discipline rule (the filesystem wins), the lead's record of their status is unstamped.
7. **Supporting evidence is not always under `research\`.** hypercore's companion clones lived in a previous session's scratchpad and are gone (A-holepunchto-hypercore-1). tuf-js read its companions through the API only. tessera's companions are under `research\_untrusted\transparency-dev-tessera\`, which is the pattern to copy.
8. **Scores transcribe correctly.** A mechanical comparison of all 17 rows of `scoring\scores.csv` with each dossier's section 13 (`s13.py`) finds no transcription error. The one apparent difference (nanobrowser R29 view, requirement_fit 2) matches the dossier's prose line under its table.
9. **Score against anchor (one note for the lead).** aaif-goose `demonstrated_maturity` 4 rests partly on "large documented user base [reported]". The anchor's top tier needs documented production use, and the score is held below 5 for other reasons, so 4 is consistent. Still, it is the only maturity score in the user_facing_app ranking that leans on a [reported] usage claim, and that ranking puts goose first (3.5). I re-read `scoring\sensitivity-output.md` after the lead regenerated it under D3.6 (file time 2026-10-21 10:37). goose is still first at 3.5 and "stable". datalad and nanobrowser are now marked FRAGILE, which does not affect this note.

## Summary for the lead

The three to five objections I would most want acted on, in order:

1. **A-datalad-1**: fix the failed marker citation (`run.py:1132-1141` should be `1144-1151`, which recurs at L32, L96 and L124). Ask the datalad inspector to re-verify every other range inherited from the first run, because the header's "re-confirmed" statement is demonstrably not true for at least one.
2. **Cross-cutting 3**: require each dossier to state the command behind every count. Correct the three non-reproducing counts (A-aaif-goose-1, A-nanobrowser-1, A-eclipse-biscuit-2) before any of them reaches the article.
3. **Cross-cutting 4**: in the evidence-quality figure, treat the README-sourced rows labelled [inspected] (A-anthropics-sandbox-runtime-2, A-hypercerts-lexicon-2) and goose's helper-trace rows (A-aaif-goose-4) as [reported] or second-hand. Ask the two inspectors to cite the code (`wfp.rs`) or relabel.
4. **Cross-cutting 6**: stamp STATUS (with `verified: <sha> <date>`) on the nine 2026-10-20 dossiers, or correct the record that says all fifteen are marked.
5. **A-aaif-goose-2**: close the telemetry open question with the caller evidence above, and add the pre-consent onboarding funnel (`posthog.rs:560-561`) to the G1 re-check list for goose upgrades.

Objection counts: 14 objections in total, all minor; none is a blocker or major. By dossier: aaif-goose 4, anthropics-sandbox-runtime 2, datalad 2, eclipse-biscuit 2, hypercerts-lexicon 2, nanobrowser 2, getaegis-aegis 1, holepunchto-hypercore 1. No objections for convira-sandbox, dapr-durabletask-go, identity-common-ts, openworkflow, solana-foundation-rewards, transparency-dev-tessera or tuf-js.

Citation spot-check tally: 165 checked, 158 PASS, 6 PARTIAL, 1 FAIL. Counts re-run: 14, of which 11 reproduce.
