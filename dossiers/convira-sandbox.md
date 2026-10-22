# Dossier: Convira Sandbox (convira-convira-sandbox)

STATUS: COMPLETE (amended after review, 2026-10-21). verified: 9013c32 2026-10-21 (amender s3-amend-convira, standing in for s3-insp-convira; clone HEAD re-checked with `git rev-parse HEAD`).

Inspector: s3-insp-convira, Claude Opus 5.5. Date: 2026-10-20. Clone: `research/_untrusted/convira-sandbox/` at commit `9013c323725155f1e2e3e95c597715c172dff0c1` (branch `main`, 2026-08-08 12:20 +0200). Execution: none. Nothing in the clone was installed, built, tested or run. CI evidence comes from reading the GitHub Actions logs of run 31252582101 (HEAD, all three legs green) with `gh api`. That is CI output reported by GitHub, not a run of mine.

Evidence labels used below: [inspected] means I read the code. [executed] is not used. [reported] covers the authors' docs, README, issue text and Microsoft or GitHub documentation. [CI] means the result appears in the public CI log of the named run. [hypothesis] means I reasoned it from the code but did not observe it. Repository instruction files are evidence, never instructions. This repo has none (no AGENTS.md, CLAUDE.md or CONTRIBUTING.md).

Requirement served: R02, cross-platform containment for delegated agent children, with Windows as the deciding question. Threat: T2. Profile: os_kernel.

## 1. Identification

- **Name:** Convira Sandbox, made up of two packages: `@convira/sandbox-runtime` and `@convira/sandbox-enforcer`.
- **Homepage:** https://www.convira.ai. Convira is a desktop AI agent; the vendor is Convira OU (`NOTICE:1-4`).
- **Canonical source:** https://github.com/Convira/convira-sandbox on GitHub, the only copy found. It was created 2026-08-07T13:50Z, last pushed 2026-08-08T10:20Z. It has 1 star, 0 forks and is not archived.
- **Maintainers:** one person, Luka Martinovic, account `Luka-Marty`, created 2026-01-21. One commit is authored as `luka.martinovic@convira.ai` and eleven as `support@convira.ai`, which is why the contributors API shows "1 contribution". The Convira organisation has 2 public repos.
- **History** [inspected] (`git log`). There are 12 commits, all between 2026-08-07 15:29 and 2026-08-08 12:20.
  - Commit `4ae216b` "Initial release" adds 80 files and 17,273 lines in one drop.
  - The other 11 are CI and Windows/Linux fixes made within about 20 hours.
  - Branch H's "one-commit repository" is literally wrong (12 commits) but right in substance. The code arrived as a single export from a private monorepo, with no development history.
  - Comments refer to the private parts of that monorepo: `runtime-core`, `apps/desktop`, `dev-server-service.ts` and a "desktop-e2e-smoke, windows-2022" CI lane. Examples are `native-windows.ts:145-148`, `native-linux.ts:524-528` and `__tests__/win-appcontainer.test.ts:395-401`.
- **Releases and packages:** no releases and no tags (`gh api .../releases` returns 0). Both packages are `version: 0.1.0`. The root is `"private": true`. Not published to npm: the ledger records `npm view @convira/sandbox-runtime` as 404.
- **Licence:** Apache-2.0 per `LICENSE` (standard Apache 2.0 text, 202 lines) plus a `NOTICE` file. The manifests agree (`package.json:6`, `packages/*/package.json` `license`). No per-directory differences.
- **Documentation:** English. A README and a SECURITY.md with a disclosure address (`security@convira.ai`) and a 3-working-day acknowledgement commitment (`SECURITY.md:14-20`). No DOI, paper or SWHID.

## 2. What works

### Public API

From `packages/sandbox-runtime/src/index.ts:19-130` [inspected]:

- `createSandboxedSpawn(mode)` and `detectAdapter("auto"|"native"|"off")`.
- Four adapters: `windowsAdapter`, `linuxAdapter`, `macosAdapter` and `passthroughAdapter`.
- Each adapter offers `available()`, `capabilities()`, `capabilitiesV2()`, `unavailableReason()` and `wrapSpawn(SandboxSpawnConfig) -> SpawnSpec {command,args,env,cwd,postSpawnHook?}`.
- The caller then runs `child_process.spawn` itself. The library never spawns the workload.

The config (`types.ts:14-103`) covers:
- `filesystem.readPaths/writePaths/denyPaths/denyPathKinds`
- `network.enabled/allowLoopback`
- `resources.memoryMb/maxProcesses/timeoutMs/longLived`
- an optional Linux-only `kernelHardening`.

### Per-OS mechanisms

**Windows** [inspected]. Files: `src/adapters/native-windows.ts`, `src/win-appcontainer.ts`, `native/win_appcontainer_launch.cc`, `native/win_appcontainer_common.h`, `native/win_job_object.cc`.

- **Launcher.** `wrapSpawn` rewrites the command to `convira_sbx_launch.exe <profile> <grantsFile> [--allow-network] -- <cmd> <args>` (`native-windows.ts:253-270`).
- **Launch sequence** (`win_appcontainer_launch.cc:595-752`):
  1. Creates an ephemeral per-spawn AppContainer profile named `ConviraSbx-<16 hex>` (`win-appcontainer.ts:346`).
  2. Writes inheritable deny, read or write ACEs for that AppContainer SID onto each granted path.
  3. Builds `SECURITY_CAPABILITIES`: no capability SIDs, or with `--allow-network` both `INTERNET_CLIENT` and `PRIVATE_NETWORK_CLIENT_SERVER` (`win_appcontainer_common.h:195-211`).
  4. Calls `CreateProcessW(CREATE_SUSPENDED)`, assigns the child to a kill-on-close Job Object, then resumes it.
  5. Waits, then revokes the ACEs and deletes the profile.
- **Crash cleanup.** A boot janitor removes profiles and ACEs that a crash left orphaned, using a ledger (`win-appcontainer.ts:388-429`).
- **Resource limits** come from a second Job Object that a post-spawn hook attaches to the launcher's PID: memory cap, process count, cumulative CPU (`native-windows.ts:181-211`, `win_job_object.cc:185-217`).

**Linux** [inspected]. File: `src/adapters/native-linux.ts`.
- Uses bubblewrap with read-only binds of `/usr /lib /lib64 /bin /sbin /etc`, `--proc`, `--dev`, a tmpfs `/tmp`, binds for the granted read/write paths, and tmpfs or `/dev/null` overlays for deny paths.
- Adds `--unshare-pid`, plus `--unshare-net` only when `network.enabled` is false, then `--die-with-parent --new-session` (`:356-533`).
- A `ulimit` wrapper inside the namespace applies the rlimits (`:551-561`).
- seccomp is applied only if a caller asks for `kernelHardening.seccompProfile` **and** the enforcer's native binding loads. Otherwise it is skipped without any report (`:535-543`).
- **Landlock is not wired into `wrapSpawn` at all.** `landlockRuleset` in `types.ts:98` is consumed nowhere in `sandbox-runtime/src` (grep). `sandbox-enforcer`'s `applyKernelHardening` restricts the *calling* process (`enforcer.ts:44-85`).

**macOS** [inspected]. File: `src/adapters/native-macos.ts`.
- `sandbox-exec -p <profile>` with a `(deny default)` profile (`:135-282`). It allows:
  - reads of system paths;
  - granted read and write paths;
  - writes to `/private/tmp` and `/var/folders`;
  - `process-exec process-fork`, `mach-lookup`, `signal`, `sysctl-read` and `ipc-posix-shm`, all unrestricted;
  - with network enabled, outbound TCP 80 and 443 to any host plus UDP 53;
  - localhost only when `allowLoopback` is set.
- It ends with a deny of the `/System/Volumes/Data` alias and the explicit deny paths.

**Passthrough.** No confinement, and every capability reports false or `none` (`passthrough.ts:29-50`).

### Capability reporting

`capabilitiesV2` reports these tiers [inspected]:
- **memory:** `hard-address-space` / `rss-watchdog` / `none`
- **cpu, pids, fileSize, wallClockKill, killTree, filesystemIsolation, networkIsolation:** true or false

On **Windows**, every field, including filesystem and network isolation, comes from a destructive live probe. Each probe has an unconfined control leg, so a probe cannot pass vacuously:
- **Filesystem probe:** `_runAppContainerFilesystemProbe`, `win-appcontainer.ts:566-630`.
- **Network probe:** `_runAppContainerNetworkProbe`, `:661-736`.
- **Spawn-caging probe:** `:768-838`.
- **Probe subject.** The probe child is a fixed list of `--selftest` verbs inside the launcher itself (`win_appcontainer_launch.cc:195-525`), not a script interpreter.

On **Linux and macOS**, `filesystemIsolation` and `networkIsolation` are hard-coded `true` (`native-linux.ts:315-316, 345-346`; `native-macos.ts:427-428, 457-458`). Only the resource fields are probe-gated there. The README's claim that "Every field ... states a fact proven by that control's own passing probe" (`README.md:80-82`) therefore holds for Windows only.

### Tests

The README claims 460 tests across 30 files. CI reports, from run 31252582101 logs:

| Leg | sandbox-runtime | enforcer |
| --- | --- | --- |
| Linux | 302 passed, 1 skipped | 160 passed |
| macOS | 302 passed, 1 skipped | 160 passed |
| Windows | 207 passed, 96 skipped | 160 passed |

The 460 figure counts tests that pass vacuously off-platform. The six "real win32 AppContainer enforcement" cases use `if (!onWindows) return;` and so report *passed* on Linux and macOS (`win-appcontainer.test.ts:401-469`). Most of the suite is unit-level with mocked bindings. For example, all enforcer tests mock the native binding (`landlock-with-binding.test.ts`, `seccomp-with-binding.test.ts`). The enforcer's native addon is never built in CI: its `build` script is `tsc` only (`packages/sandbox-enforcer/package.json` `scripts.build`), and CI does not install libseccomp-dev (`.github/workflows/ci.yml:250-274`).

Tests that spawn a real confined process [inspected; result from CI]:

| Test (file: name) | Asserts | Legs where it ran |
| --- | --- | --- |
| `integration.test.ts`: "denies reading files outside allowed paths" (`:80-131`) | child exits exactly 42 when reading a file in a fresh `~/.sb-test-probe-*` | Windows 13.2 s [CI]; Linux, macOS (not individually timed, file 6/6 passed) |
| `integration.test.ts`: "allows reading/writing within permitted paths" (`:133-175`) | exit 0 and output file content | all three |
| `integration.test.ts`: "denies writing outside allowed paths" (`:177-216`) | file absent and exit 42 | all three |
| `integration.test.ts`: "blocks outbound network when disabled" (`:220-257`) | `http.get('http://1.1.1.1')` errors or times out (exit 42) | all three |
| `win-appcontainer.test.ts`: "filesystem: AC child cannot read outside the grant but can read+write inside it" (`:437-446`) | live filesystem probe true | Windows |
| `win-appcontainer.test.ts`: "network: a plain child reaches a localhost listener, the AC child is denied" (`:448-457`) | live loopback-denial probe true | Windows, 10.1 s [CI] |
| `win-appcontainer.test.ts`: "spawn caging: the child is in the job while still suspended and descendants are reaped" (`:459-468`) | IsProcessInJob before resume; grandchild reaped when the launcher is killed | Windows |
| `win-appcontainer-localappdata.test.ts`: "refuses with a named message when the variable is absent" | launcher refuses up front with a message naming LOCALAPPDATA | Windows |
| `native-macos.test.ts:254-271` | one real sandbox-exec spawn | macOS |

The Linux adapter tests (`native-linux.test.ts`, 42 cases, and `native-linux-deny-host-mutation.test.ts`, 9 cases) only assert the bwrap argument list.

### CI lanes

`.github/workflows/ci.yml` runs on ubuntu-latest, macos-latest and windows-latest, on push and on pull requests. The HEAD run used the images ubuntu-24.04, macos-26-arm64 and windows-2025-vs2026 [CI].
- **Windows** integration cases were first enabled in `264e3cb` (that run failed) and have been green in exactly two runs (`41eec3f`, `9013c32`).
- **Linux** confinement runs only because CI installs bwrap and relaxes the AppArmor user-namespace restriction (`ci.yml:254-265`).

### Deployment evidence

- **Production use:** none independent. The vendor says this is the confinement layer of its own desktop product [reported].
- **Packaging:** comments about asar unpacking (`win-appcontainer.ts:130-138`) and Electron `resourcesPath` for bwrap (`native-linux.ts:209-217`) imply a packaged Electron app [inspected; product use reported].

## 3. Maturity

### Operating footprint
- **Process model:** an in-process library. On Windows it adds one helper EXE process per confined child.
- **Dependencies:**
  - no runtime npm dependencies;
  - `node-gyp` as an optional dependency;
  - system `bwrap` on Linux;
  - `/usr/bin/sandbox-exec` on macOS;
  - libseccomp only if the enforcer's native addon is built.
- **Code size** [inspected, `wc -l`]: about 5,000 TS lines in `src`, about 1,920 C/C++ lines, and about 7,600 test lines.

### Maintenance
- All activity happened on 2026-08-07/08. No commits for 73 days at the time of inspection. No releases.
- Two issues, both opened by the author:
  - #1 (Windows code 203) was self-diagnosed and closed in 14 h with 3 author comments.
  - #2 (Ubuntu 24.04 AppArmor) is open with 0 comments.
- I could not sample issue response to outside reporters because none exist.
- **Bus factor:** 1.

### Security posture
- No GitHub security advisories (`gh api .../security-advisories` returns `[]`). No CVE found for the repo.
- The README states plainly that there is "no third-party audit", "no reproducible builds" and "one layer only" (`README.md:17-31`, `SECURITY.md:180-185`).
- SECURITY.md counts a false-positive capability report as an in-scope vulnerability (`SECURITY.md:168-175`). That is a strong, checkable contract, and sections 8 and 14 list places where I think it is breached.

### Documentation quality
- **README:** short and unusually candid.
- **Code comments:** dense, and they explain each failure mode they guard against.
- **Inaccuracies found:**
  - The index docstring still says "Windows: Job Objects (resource limits)" (`index.ts:4-8`), and `types.ts:1-8` says the same.
  - Issue #2 says `linuxAdapter.available()` fails under the AppArmor restriction, but the code checks only bwrap presence, the `unprivileged_userns_clone` sysctl and Snap/Flatpak (`native-linux.ts:265-290`). On Ubuntu 24.04 `available()` would return true, the capability report would say isolated, and the spawn would then die in bwrap: it fails closed at spawn, but the report is wrong.

### Counterexample rows
- **s2-br-h (maintenance):** confirmed in substance. Single author, a code dump plus a day of fixes, no releases, not on npm, a node-gyp and Visual Studio toolchain needed on Windows. Refuted only in the literal "one commit" detail.
- **No other counterexample rows** exist against this codebase. Sections 8 and 14 add the defects I found myself.

### Popularity
1 star. It carries no fitness signal either way.

## 4. Architecture

### Control flow (Windows)

1. The caller runs `detectAdapter("auto")` (`detect.ts:30-51`). This calls `windowsAdapter.available()`, which:
   - loads `win_job_object.node`, an N-API addon, NAPI_VERSION 8 (`binding.gyp:3-4`);
   - runs the self-test handshake against the launcher;
   - runs the Job Object kill-tree probe (`native-windows.ts:64-90`).
   AppContainer probes are **not** part of availability. A host where Job Objects work but AppContainer does not still gets `windowsAdapter`, reports `filesystemIsolation:false`, and then `wrapSpawn` throws (`:279-282`). This is fail-closed and honest.
2. `wrapSpawn` builds a launcher spec only when three things hold: the launcher exists, the filesystem probe passed, and (if the spawn is network-denied) the network probe passed (`:218-223`). Otherwise it throws.
3. A request with network denied but loopback allowed always throws on Windows (`:224-233`).
4. The caller spawns the launcher and calls `postSpawnHook(pid)` to attach the outer limit-bearing job to the launcher.

### Process boundaries and lifecycle

**Windows chain:** Node, then the launcher (unconfined, the user's token), then the AppContainer child (low integrity, AppContainer token).
- **Kill:** killing the launcher closes its kill-on-close job and reaps the whole tree (`win_appcontainer_launch.cc:716-731`; spawn-caging probe).
- **Crash:** leaves the profile and ACEs behind for the janitor (`:34-40`).

**Linux:** bwrap with `--die-with-parent`.

**macOS:** sandbox-exec. The profile is passed inline with `-p`, so there is no TOCTOU file window (`native-macos.ts:487-494`).

### Storage
- A Windows grants ledger in `%TEMP%\convira-appcontainer-ledger` (`win-appcontainer.ts:210-212`).
- On macOS, profile temp files only in the oversize case.

### Identity model
- **Windows:** a fresh AppContainer SID per spawn. No principal concept beyond that.
- **Environment:** the child env is exactly what the caller passes (`types.ts:21-22`), plus `LOCALAPPDATA` on Windows (`native-windows.ts:118-123`). The library strips nothing, so keeping keys out is the caller's job.

### Probe cost
Probes are synchronous (`spawnSync`, plus `Atomics.wait` polling with 30-60 s ceilings) and cached once per process (`win-appcontainer.ts:433-463, 635-639`). CI timings show:
- the Windows loopback probe takes 10.1 s, which ends on the 10 s `select` timeout, i.e. a silent drop (`win_appcontainer_launch.cc:504-517`);
- `detect.test.ts` "all adapters satisfy the SandboxAdapter interface" takes 10.2 s on Windows.

In a single-threaded bridge, the first `available()` / `capabilities()` call would block the event loop for about 10-25 s [hypothesis from code plus CI timings].

## 5. Direct relevance

### R02 against the Alpha evidence
- **OSC-32:** the Alpha has `sandbox-exec` with `(allow default)` on darwin and `contract-only` (unconfined) on Linux and Windows (`host/delegation-isolation.mjs:61-68, 71-85`).
- **OSC-33 and OSC-34:** opt-in can be bypassed; `PATH` and the key are passed in the child env.
- **os-map section 9:** isolation is darwin-only, and `cancel` does not kill.
- **os-map section 17 seam 2:** "extend `delegation-isolation.mjs` beyond darwin" with "a containment mode per OS".

Convira supplies exactly the missing Linux and Windows modes, in the same Node and TS shape and with the same argv-wrapper model that `wrapCommandForIsolation` already uses (`delegation-isolation.mjs:211-216`).

### Threat T2 (key exfiltration by a delegated child)
Convira partly closes T2:
- **Reading keys from disk:** a confined child cannot read key files outside its grants (deny-by-default on Windows and macOS; mount namespace on Linux).
- **Reading the bridge config:** a child cannot read `bridge-config.generated.js` unless it is granted.
- **Exfiltrating a key in its own env:** Convira does not stop this once network is enabled. No OS has a per-host egress allowlist. macOS narrows to ports 80 and 443 only; Linux with network enabled shares the host network namespace; Windows grants Internet plus LAN.

T2 still needs R03.

### Property check against threat-model section 4, Containment

| Property | Windows | Linux | macOS |
| --- | --- | --- | --- |
| Filesystem read escape blocked | **Demonstrated** [CI]: `integration.test.ts` "denies reading files outside allowed paths"; live probe test "filesystem: AC child cannot read outside the grant..." | **Demonstrated** [CI] on a runner with the sysctl relaxed (same integration test) | **Demonstrated** [CI] (same integration test) |
| Filesystem write escape blocked | **Demonstrated** [CI]: "denies writing outside allowed paths" | Demonstrated [CI] (same) | Demonstrated [CI] (same) |
| Network escape blocked when denied | **Demonstrated** [CI]: "blocks outbound network when disabled" (1.1.1.1:80). No control leg proves the runner had egress | Demonstrated [CI] (`--unshare-net`) | Demonstrated [CI] |
| Exec escape (descendants stay confined) | Partly demonstrated [CI]: the spawn-caging probe test shows descendants stay in the kill-on-close job. Token inheritance is OS-guaranteed [reported, Microsoft]. No test that a descendant is still filesystem- or network-denied | Not demonstrated (no test). Design: namespaces are inherited [hypothesis] | Not demonstrated. Unrestricted `mach-lookup` may allow launch-via-LaunchServices escapes [hypothesis] |
| Child cannot reach the loopback port unless granted | **Demonstrated for "cannot"** [CI]: "network: a plain child reaches a localhost listener, the AC child is denied". "Unless granted" is impossible: a loopback grant is refused at spawn (`native-windows.ts:224-233`; test "refuses a loopback-only spawn...") | Demonstrated only when network is disabled (own netns). With `network.enabled` the child shares the host netns and **can reach the bridge port**; `allowLoopback:false` is ignored without any error, log or capability change (`native-linux.ts:516-530`), although `types.ts:70-71` documents it as "Whether loopback (127.0.0.1) connections are allowed". That is a silent no-op of a configured control (amended after S-convira-sandbox-2; G2 in section 6). Against the Alpha it means a network-enabled Linux child reaches the bridge's open proxy prefixes with no token (OSC-05). Not tested | Granular by design (localhost only with `allowLoopback`; `native-macos.ts:214-243`). Not tested |
| Honest "unconfined" signal | **Demonstrated**: passthrough is all-false (`capability-report.test.ts` "passthrough reports memory 'none' and every control false"); Windows "REFUSES to spawn while AppContainer is not proven, instead of unwrapping" (`native-windows.test.ts:300`) | Partial: the isolation flags are static `true`, so an AppArmor-blocked host over-reports, though spawns then fail closed. seccomp is skipped without being reported | Partial: static `true` |
| No admin needed | Designed (per-user `CreateAppContainerProfile`) but **not tested non-elevated**. GitHub Windows runners run as administrator with UAC disabled [reported, GitHub docs; log shows `runneradmin`] | bwrap is unprivileged, but the runner's sysctl was changed with sudo | Yes (`sandbox-exec` ships with the OS) |

### isolation_and_security
Score 3 (anchor: designed and partly tested). Section 13 gives the details.

## 6. Reuse decision

**Decision: vendor a limited component.** Specifically:
- The Windows AppContainer backend: `native/win_appcontainer_launch.cc`, `native/win_appcontainer_common.h`, the Job Object parts of `native/win_job_object.cc`, `src/win-appcontainer.ts`, `src/adapters/native-windows.ts`, `src/probe-payload.ts`, `src/deny-leaf-kind.ts`.
- The probe-gated `capabilitiesV2` pattern.

These would sit behind an Alpha-owned containment interface in `host/delegation-isolation.mjs`. **Learn the pattern, without vendoring,** for the Linux and macOS adapters. Adoption is conditional on the acceptance test in section 11 passing on a non-admin Windows 11 account.

**Preconditions added after review (2026-10-21):**
- A full line-by-line review of the vendored native sources before the first PR merges: 1,549 lines (`wc -l native/win_appcontainer_launch.cc native/win_appcontainer_common.h native/win_job_object.cc`: 783 + 217 + 549). The original inspection read the launch path, the ACE helpers and the job-object probe, not every line. The code arrived as one 17,273-line export from a single account with no earlier history, so provenance cannot be checked; review is the only control (S-convira-sandbox-4).
- The Alpha builds the `.node` and `.exe` from the reviewed source in its own CI. Never take upstream binaries (none exist today anyway).
- Grant paths are refused if any component is a reparse point (junction, symlink or mount point), and acceptance case A10 passes (S-convira-sandbox-1).
- One broker transport is agreed for R02, R03 and R05 before any R02 PR (security review X-5; section 7, conflict 2).

These preconditions tighten the decision but do not change it.

**Why this beats the alternatives:**
- **Versus anthropics/sandbox-runtime (section 12):** Convira is the only examined candidate that confines filesystem reads and network on Windows **without an elevated install**. srt needs a one-time UAC `windows-install` that sets up a local account and machine-wide WFP filters, and its Windows support is alpha.
- **Versus the restricted-token lineage** (Codex, yj-sandbox, DSH's ACL backend): the ledger records that its no-admin modes constrain writes but not reads or network, and the yzyyohh measurement shows piped-stdio children failing with 0xC0000142.
- **Why not adopt the whole package:**
  - it is not on npm and has no releases;
  - one author;
  - its Linux backend has no egress allowlist, exposes host loopback when network is on, and does not wire in Landlock;
  - srt's Linux and macOS backends add proxy-based domain filtering, which T2 needs.

**Hard gates:**

| Gate | Result | Clause / evidence |
| --- | --- | --- |
| G1 no mandatory cloud or telemetry | **Pass** | No network calls in `packages/*/src` (grep for URLs and `fetch(`: none) [inspected] |
| G2 per-OS matrix, degrades visibly | **Split (amended 2026-10-21).** Vendored Windows backend: **Pass**. Upstream Linux adapter as shipped: **[FAIL]** for `network.enabled=true` with `allowLoopback=false` | Windows: passthrough reports all false, and Windows refuses rather than unwrapping. It also refuses the one loopback combination it cannot honour (`native-windows.ts:224-233`); with network on, AppContainer loopback isolation still denies loopback, so `allowLoopback:false` holds. Linux: `allowLoopback:false` with network on is ignored with no error, log or capability change (`native-linux.ts:516-530`). That is the silent no-op G2 excludes (S-convira-sandbox-2). By the same reading, a requested `kernelHardening.seccompProfile` that is skipped in `catch {}` (`native-linux.ts:535-543`) is also a silent no-op. WARN: Linux and macOS isolation flags are static. The decision is unaffected, because the Linux adapter is "learn, not vendor". An Alpha Linux mode must refuse that combination, or report `networkIsolation:false`, before it can pass G2 |
| G3 licence compatible with MIT | **Pass** | Apache-2.0 file-level; NOTICE must be carried |
| G4 DAO chain | **N/A** | not a DAO component |
| G5 project invariants | **Pass** | No DAO, no credentials, no human-only actions touched; it narrows what a child can do |

## 7. Integration design

### Boundary
A new Alpha module `host/containment/` exposes one interface that the existing delegation service already nearly has:

```
resolveContainment({platform, override}) -> {mode: "appcontainer"|"bwrap"|"sandbox-exec"|"contract-only", report: CapabilityReportV2, reason}
wrapForContainment({mode, command, args, env, cwd, readPaths, writePaths, denyPaths, network:{enabled, allowLoopback}, resources}) -> {command, args, env, cwd, postSpawnHook?}
```

- `wrapCommandForIsolation` (`delegation-isolation.mjs:211-216`) becomes a thin call into this module.
- The existing `writableRootsFor` (`:141`) and `readDenyRootsFor` (`:175`) supply `writePaths` and `denyPaths` unchanged.
- On Windows the vendored launcher is the wrapper command. The two spawn sites stay as they are, `addon-delegation-service.mjs:1696-1707` (Hermes) and `:2271-2281` (OpenCode CLI), except that `postSpawnHook(child.pid)` is called right after `spawnProcess`.

### Process boundary
Node 24 calls the vendored TS directly as a library.
- **Windows:** loads an N-API addon (ABI-stable, so a prebuilt `.node` built once per arch works across Node versions [inspected: `NAPI_VERSION=8`, `binding.gyp:4`]) and execs a static-CRT helper EXE (`RuntimeLibrary: 0`, `binding.gyp:107`).
- **Linux:** execs system `bwrap`.
- **macOS:** execs `/usr/bin/sandbox-exec`.

### Stdio
The Alpha spawns with `stdio: ["ignore","pipe","pipe"]` (`addon-delegation-service.mjs:1705`). The launcher marks its std handles inheritable and passes them through `STARTF_USESTDHANDLES` with `bInheritHandles=TRUE` (`win_appcontainer_launch.cc:663-686`).

The integration tests use `spawnSync` with default piped stdio, and on Windows the AppContainer `node.exe` child booted, read, wrote and exited with the asserted codes [CI]. So piped stdio works for an AppContainer child on that runner. The restricted-token 0xC0000142 failure (yzyyohh) does not carry over [CI plus reasoning]. A non-admin desktop session is still untested; it is acceptance case A2.

### Error behaviour
- Every refusal throws an error with a static reason (`unavailableReason()`).
- The Alpha maps that onto its existing "Delegation isolation could not be applied" audit path (`addon-delegation-service.mjs:1375-1382`).
- `contract-only` stays an explicit operator override recorded in the governance audit, as today (`delegation-isolation.mjs:54-57, 65`).

### Design conflicts the Alpha must resolve

1. **Windows loopback cannot be granted.**
   - A confined `opencode serve` is impossible on Windows: the bridge proxies to it over loopback, and Microsoft documents that an AppContainer listening on loopback "is prevented from receiving any incoming packets" [reported]. The same holds on Linux with network denied (own netns, `native-linux.ts:517-528`).
   - So `opencode serve` (`opencode-client.mjs:281-285`) must stay unconfined, be moved to stdio transport, or run as a CLI per task.
2. **R03 broker transport.**
   - A loopback HTTP credential broker on the bridge (the natural R03 design) is unreachable from a Windows AppContainer child.
   - The broker must use a channel the AppContainer can use: inherited pipe handles, or a named pipe whose DACL names the AppContainer SID [hypothesis]. Otherwise the child gets `INTERNET_CLIENT` and talks to the provider directly with a key, which defeats R03.
   - This should be decided together with R03 and R05.
   - **Amended after review (S-convira-sandbox-3, X-5):**
     - The SID is fresh for every spawn, but Node picks it, not the launcher. `prepareAppContainerSpawn` chooses the profile name `ConviraSbx-<16 hex>` before the launcher starts (`win-appcontainer.ts:343-346`). The launcher only calls `CreateAppContainerProfile` with that name (`win_appcontainer_launch.cc:16, 595-598`).
     - An AppContainer SID is a deterministic function of the profile name (`DeriveAppContainerSidFromAppContainerName` [reported, Microsoft Learn]). So the bridge could compute the SID and create a per-spawn pipe with a DACL for it before spawning the launcher. The reviewer's "the launcher owns that window" holds only for the inherited-handle variant [hypothesis; not built or tested].
     - **Inherited-handle variant.** The launcher calls `CreateProcessW` with `bInheritHandles=TRUE` and no `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` (`win_appcontainer_launch.cc:663-686`). Any inheritable handle the launcher holds therefore reaches the child. That makes a pipe handle passable, but nothing narrows the set of handles passed. The launcher has no argument for telling the child a handle value, so this variant needs a launcher change.
     - **The fallback is worse than it first looked.** A network-enabled spawn gets `PRIVATE_NETWORK_CLIENT_SERVER` (LAN) as well as `INTERNET_CLIENT` (`win_appcontainer_common.h:190-211`). A child given network so it can reach a provider directly can also reach the user's LAN.
     - Transport: the lead decides it (X-5). For this backend it should be a per-spawn pipe outside the bridge's main listener, never the loopback port, which AppContainer cannot be granted.
3. **Linux with network enabled exposes host loopback, including the bridge port.**
   - Either keep children network-denied and use a broker over a bind-mounted Unix socket (srt's pattern), or accept that the bridge's token check is the only barrier.
   - Amended after S-convira-sandbox-2: the token check is not even a barrier for the bridge's open proxy prefixes (OSC-05). The Alpha's Linux mode must refuse `network.enabled=true` with `allowLoopback=false`, the way the Windows adapter refuses its impossible combination. It must not inherit the upstream behaviour of ignoring it.
4. **ACL writes on user directories (Windows).**
   - Each spawn rewrites the DACLs of every granted path and its subtree, twice: grant, then revoke (`win_appcontainer_common.h:122-148, 153-189`).
   - The readPaths for Hermes (`dirname(pythonPath)`) and OpenCode must be directories the user owns. On a standard user account, `C:\Program Files\...` cannot take a DACL write, and the launcher treats any grant failure as fatal (`win_appcontainer_launch.cc:615-627`) [hypothesis: spawn refused].
   - This is a security issue as well as friction (S-convira-sandbox-1); section 8 has the detail. The ACE writes follow reparse points, and the unconfined launcher performs them as the user. The Alpha port must open each grant path with `FILE_FLAG_OPEN_REPARSE_POINT`, refuse reparse points in any path component, and canonicalise before granting.

### Alpha files that change
- `browser-first/host/delegation-isolation.mjs`: `resolveDelegationIsolation` gains win32 and linux modes; `buildSandboxProfile` is kept for the darwin legacy path or replaced.
- `browser-first/host/addon-delegation-service.mjs`: spawn sites at 1696-1707 and 2271-2281, plus the isolation setup at about 1299-1385.
- A new `browser-first/host/containment/` (vendored code plus a NOTICE).
- `browser-first/package.json`: a native build step or a prebuilt binary.
- CI: a `windows-latest` lane.

### Alpha tests affected
These are among the 2,424 browser-first tests:
- `test/delegation-isolation.test.mjs` "resolveDelegationIsolation follows override, platform, and executable matrix" (`:80-113`). It asserts `contract-only` with reasons `no-os-primitive:linux` and `no-os-primitive:win32` and must change.
- `test/addon-delegation-service-error-handling.test.mjs` "OpenCode delegation uses contract-only mode without wrapping on linux" (`:1615`) and "...honors darwin contract-only operator override without wrapping" (`:1655`). 15 `contract-only` assertions in the test tree.
- `test/delegation-isolation-live.test.mjs`, which self-skips off macOS today, should gain win32 and linux legs.

### Versioning
- Pin the vendored SHA `9013c32` in a `VENDORED.md`.
- Keep the ABI check `abiVersion >= 2` (`win-appcontainer.ts:96`).

## 8. Security and governance effects

### New privileges and attack surface
- A helper EXE that runs as the user and writes DACLs on user directories.
- An N-API addon loaded into the bridge process. A memory-safety bug in ~550 lines of addon C++ would be in-process with the bridge.
- A grants file in `%TEMP%` that the unconfined launcher parses (`win_appcontainer_launch.cc:116-145`). Any same-user process can edit it before launch, but that process already has the user's rights.
- **The ACE writes follow reparse points** (added after S-convira-sandbox-1) [inspected for the code; exploitation is a hypothesis, not executed].
  - `ApplySidAceOnPath` and `RemoveSidAcesFromPath` call `GetNamedSecurityInfoW` and `SetNamedSecurityInfoW` on the path as given. They rely on auto-inheritance to reach the subtree (`win_appcontainer_common.h:119-189`).
  - The Node side checks only that a path exists, and creates missing deny leaves with `fs.mkdirSync(..., {recursive:true})` (`win-appcontainer.ts:276-301, 355-360`).
  - Checked with `grep -rn -i "reparse\|junction\|symlink\|realpath\|lstat\|FILE_FLAG_OPEN_REPARSE\|readlink" native/ src/`: the only hits are in the Linux and macOS adapters (`native-linux.ts:170, 415-421`; `native-macos.ts:155-167, 410`). The Windows code handles no reparse points.
  - Scenario: a child with a write grant plants a junction at a path that a later spawn grants, or at a parent of a deny leaf. That later grant then writes a full read, write, execute and delete ACE for the new AppContainer SID onto the junction's target, for example `%USERPROFILE%`. The unconfined launcher does this as the user. That is the installer ACL-redirection bug class.
  - Mitigating factor [reported]: since 2015, Windows has restricted mount-point creation by sandboxed processes. That mitigation has had bypasses: CVE-2015-2553 (https://cve.circl.lu/cve/CVE-2015-2553) and CVE-2016-3922 (https://cyberdetails.org/exploit/microsoft-windows-sandboxed-mount-reparse-point-creation-mitigation-bypass-redux-2-cde-2016-3922). It is also no protection against a junction planted by an unconfined same-user process, or by an earlier unconfined `contract-only` run.
  - Not established either way: whether `SetNamedSecurityInfoW`'s propagation through the subtree descends into junctions. Acceptance case A10 settles both questions.
- **The N-API addon runs inside the bridge process** (security review X-6, TM-4) [inspected]. `win_job_object.node` is loaded by `windowsAdapter.available()` (`native-windows.ts:64-90`). It parses only the launcher's self-test handshake and probe output, not child data, but a memory-safety bug in its 549 lines would run next to the bridge's keys. A smaller surface is possible [hypothesis]: move the limit-bearing job into the launcher, which already creates a job before resume (`win_appcontainer_launch.cc:716-731`), and keep the addon out of the bridge. That also closes the memory-cap race below. This is a design change for the Alpha port, not upstream behaviour.

### Isolation story by OS
- **Windows** [inspected unless noted]:
  - Plain AppContainer, not LPAC. No `PROC_THREAD_ATTRIBUTE_ALL_APPLICATION_PACKAGES_POLICY` anywhere (grep).
  - So the child can read anything that carries an ALL APPLICATION PACKAGES ACE: `C:\Windows`, `C:\Program Files` and much of HKLM. Microsoft: "Read-only access is less restricted" [reported, Microsoft Learn "AppContainer isolation"].
  - The code comment "the grants are the child's ENTIRE reachable filesystem" (`win_appcontainer_launch.cc:20-21`) is therefore overstated. User-profile secrets remain unreachable unless granted, because they carry no ALL APPLICATION PACKAGES ACE.
  - No `JOB_OBJECT_UILIMIT_*` flags are set, so clipboard or desktop interaction by the child is not restricted by the job [hypothesis on exploitability].
  - No `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`. The child inherits every inheritable launcher handle; today that is only stdio [inspected].
- **Network isolation is per-process.** It comes from the AppContainer token's capability SIDs, enforced by Windows' built-in AppContainer filtering. The code adds no firewall or WFP rules: no `Fwpm`, `INetFw` or `CheckNetIsolation` calls (grep). Whether enforcement depends on the Windows Firewall or BFE service state is not established; that is acceptance case A4.
- **Network probe gap.** The runtime network probe tests loopback only (`win-appcontainer.ts:652-659`), and the code says loopback and internet are denied "through the same capability check". That is not how Microsoft describes it: loopback isolation is a separate rule that applies even with `INTERNET_CLIENT`. A regression that always granted `INTERNET_CLIENT` would still pass the runtime probe while allowing internet egress, which is a false-positive report under SECURITY.md's own scope [hypothesis]. CI's `integration.test.ts` 1.1.1.1 case would catch it, but only in CI.
- **Memory cap may miss the child (race).**
  - The memory and process caps attach to the *launcher* after spawn (`native-windows.ts:181-203, 265-269`).
  - The AppContainer child joins that outer job only if the hook runs before the launcher reaches `CreateProcessW`. The addon's own header calls the post-spawn path a backstop on the launcher (`win_job_object.cc:23-28`), and the launcher's internal job sets only `KILL_ON_JOB_CLOSE` (`win_appcontainer_launch.cc:721-722`).
  - If the launcher wins the race, the child runs with no memory cap, while `capabilitiesV2.memory` says `hard-address-space` [hypothesis; acceptance case A5].
- **Linux:**
  - Only PID and (optionally) network namespaces are unshared. No IPC or UTS namespace.
  - `/etc` is readable.
  - Uses system bwrap with no version check. Branch H records a 2026 bubblewrap escape advisory, whose CVE number I have not verified.
  - seccomp is effectively off unless the enforcer addon is built with libseccomp-dev and the caller requests it.
- **macOS:**
  - `(allow mach-lookup)`, `(allow signal)` and `(allow process-exec process-fork)` are all unrestricted (`native-macos.ts:207-256`).
  - Unrestricted mach-lookup is the known route to ask LaunchServices or other daemons to act outside the sandbox. `(allow signal)` with no target filter may let the child signal the user's other processes, including the bridge [hypothesis; acceptance case A7].
  - Reads of all of `/private/var` and writes to all of `/private/tmp` and `/var/folders` are granted, so other same-user apps' temp files are exposed.

### Revocation
Kill the launcher and the kill-on-close job reaps the tree. This would fix the Alpha's "cancel rewrites status without killing" on Windows, if the Alpha's cancel path kills the child (os-map 9).

### Personal data
None leaves the machine. The ACL changes touch user directories, so after a crash the janitor must run on the next boot. Otherwise orphaned AppContainer ACEs stay on user folders (harmless but persistent).

### Trust in the maintainers
One author with no history beyond this repo, and no audit. Vendoring is safer than a dependency here, but only once the vendored code has been reviewed in full (amended after S-convira-sandbox-4). This dossier read the launch path, the ACE helpers and the job-object probe, not all 1,549 lines of Windows native code. Provenance is unverifiable, so the precondition in section 6 is a full review plus a from-source build in the Alpha's CI.

### User friction
- **Windows:** none at runtime. Building the native parts needs Visual Studio Build Tools, unless the project ships prebuilt binaries itself.
- **Linux:** bwrap must be installed. Ubuntu 24.04 may additionally need a root-only sysctl change (issue #2, untested on desktops).

## 9. Licensing

- **SPDX:** Apache-2.0 for the whole repository, from the `LICENSE` file; it matches both manifests.
- **NOTICE:** `NOTICE` ("Copyright 2026 Convira OU") must be reproduced in any redistribution of vendored files (Apache-2.0 §4(d)), and modified files must carry change notices (§4(b)).
- **Compatibility:** Apache-2.0 code inside an MIT project is a common, compatible combination. The combined distribution carries both notices.
- **Transitive obligations:**
  - libseccomp (LGPL-2.1) is dynamically linked by the enforcer's optional `seccomp_compile` addon (`sandbox-enforcer/native/binding.gyp` `-lseccomp`). This applies only if that addon is built and shipped.
  - bubblewrap (LGPL-2.1 per the ledger) is invoked as a separate executable, so it is not linked.
  - Windows links only system libraries (`userenv.lib`, `ws2_32.lib`).
  - node-gyp (MIT) is used at build time only.
- **For legal review:**
  - the Apache-2.0 patent-termination clause (§3) in combination with the proposed Symbiotic Licence (status F);
  - LGPL obligations only if the seccomp addon is ever shipped.
- **Confidence of compatibility with MIT:** high. With the Symbiotic Licence: unknown.

This is technical research, not legal advice.

## 10. Cost and effort

Scenario estimates for one contributor who knows Node and can read Win32 C++:

- **Small (Windows backend only, about 1-2 weeks):**
  - vendor the eight Windows files;
  - add `appcontainer` mode to `delegation-isolation.mjs`;
  - wire the two spawn sites;
  - add a `windows-latest` CI lane that builds with node-gyp.
  Assumes Hermes and OpenCode CLI run under AppContainer with explicit read grants for their interpreters.
- **Medium (all three OSes, about 3-5 weeks):** add bwrap and deny-default Seatbelt modes, plus the acceptance suite in section 11.
- **Large (6+ weeks):**
  - settle the loopback and broker conflicts with R03 and R05;
  - produce signed prebuilt `.node` and `.exe` per arch (x64, arm64) so users need no compiler;
  - keep the vendored C++ secure without upstream.

**Skills needed:** Win32 security APIs (ACLs, tokens, jobs), node-gyp and MSVC, bwrap and Seatbelt.

**Maintenance exposure.** With no upstream activity, the Alpha would own 1,549 lines of Windows C++ from day one. Recounted 2026-10-21 with `wc -l` over `native/win_appcontainer_launch.cc`, `win_appcontainer_common.h` and `win_job_object.cc` (783 + 217 + 549); the earlier figure of "about 1,300" was wrong. The repository-wide C/C++ total of 1,920 in section 3 reproduces once the enforcer's `landlock_binding.c` (221) and `seccomp_compile.c` (150) are added.

**Lock-in.** Low. The interface is an argv rewrite plus a post-spawn hook, so it can be swapped for srt or a Rust helper.

**Language cost.** Adds C++ to a JS-only codebase.

**Prebuilt path.**
- None exists upstream. `native/build/` is gitignored (`.gitignore`), and the build script always compiles from source when the stamp does not match (`scripts/build-win-job-object-native.mjs:299-325`).
- `package.json` "files" would ship `native/build/Release/*.node` and `*.exe` in an npm tarball (`packages/sandbox-runtime/package.json:41-51`), but nothing is published.
- Because the addon is N-API and the launcher statically links the CRT, the Alpha can build both once in CI and ship them, so users avoid node-gyp. Each binary is about 200-500 KB [hypothesis on size].

## 11. Acceptance test

This needs third-party code to run: it builds and runs the vendored launcher. **It is a request for the user to approve, not something I ran.**

**Environment:**
- a clean Windows 11 VM;
- a **standard (non-admin) local user**, with Defender on;
- Node 24 and Python 3.12 installed per-user;
- plus Ubuntu 24.04 desktop (stock AppArmor) and macOS 15/26 VMs.

**Inputs:**
- a fixture "secret" at `~/.resonantos-test/secret.txt`;
- a loopback HTTP listener on a random port standing in for the bridge;
- a granted workspace;
- a child script, in both Python and Node, that attempts each escape below and writes a verdict file.

**Cases.** Each case has a control leg that must succeed unconfined first.

| ID | Fault scenario (threat) | Expected observable |
| --- | --- | --- |
| A1 | Child reads `secret.txt` and `%USERPROFILE%\.ssh` (T2) | denied on all OSes |
| A2 | Child with `stdio: ["ignore","pipe","pipe"]` writes 1 MB to stdout; parent reads it all | full output received; no 0xC0000142, no loader dialog (Windows, non-admin) |
| A3 | Child connects to the loopback "bridge" port (T2/T3) | refused on all OSes with network off. With network on: refused on Windows and macOS; record the Linux result (expected reachable: a known gap) |
| A4 | Child connects to an external host with network off; repeat on Windows with the firewall service profile turned off | refused in every variant; if not, `networkIsolation` must report false |
| A5 | Child allocates 2x `memoryMb`; repeat 200 times to hit the post-spawn hook race | killed or allocation failure every time; any survivor is a capability-report failure |
| A6 | Child spawns `cmd.exe` / `sh` and the grandchild retries A1 and A3 | grandchild equally confined; killing the launcher / bwrap reaps it |
| A7 | macOS child runs `open -a TextEdit ~/.resonantos-test/secret.txt`, and `kill -STOP <bridge pid>` | both refused |
| A8 | Ubuntu 24.04 stock: `available()`, `capabilitiesV2()` and one spawn | either the spawn works confined, or the capability report shows the spawn will fail; a report of true followed by a failed spawn is recorded as a defect |
| A9 | First `capabilities()` call timed inside a running bridge | event-loop stall measured; pass if under 1 s after moving probes to a worker or boot-time warm-up |
| A10 | (added after S-convira-sandbox-1) Child creates a junction (and, separately, a directory symlink) inside its write grant, pointing at a canary directory outside it. A second spawn then grants that path, and a third grants a deny leaf beneath it. Repeat with the junction planted by an unconfined same-user process | the canary's DACL is unchanged, checked with `icacls` before and after, in every variant; the spawn refuses with a named reason. Any ACE carrying a `ConviraSbx-*` SID on the canary is a fail |
| A11 | (added after S-convira-sandbox-2) Linux, `network.enabled=true`, `allowLoopback=false`: child connects to the loopback "bridge" port | spawn refused or `networkIsolation:false` reported; a connected socket after a successful spawn is a G2 fail |

**CI hook:** a new `browser-first` lane `containment-acceptance` on windows-latest. Note that it runs elevated, so A2 and the non-admin cases stay in the manual VM protocol. Ubuntu-latest and macos-latest run A1 and A3-A7 against the vendored adapter.

**Pass criterion:** A1, A2, A4, A5, A6 and A10 pass on Windows non-admin; A11 passes for any Alpha Linux mode; A1 and A3 (network off) pass on all three OSes; any failure is reported as `false` in `capabilitiesV2` rather than enforced-but-absent.

## 12. Recommendation and confidence

### Benefits
- The only examined Windows design that confines reads, writes and outbound network for a Node-spawned child **without admin**.
- Fails closed with a named reason.
- Proves its Windows controls with live probes that have control legs.
- Real-confinement CI cases are green on all three OSes [CI].
- Small, permissive, and has no dependencies.

### Trade-offs
- Windows loopback is all-or-nothing denied. That blocks loopback brokers and confined servers.
- No egress domain allowlist on any OS.
- Linux and macOS isolation flags are declared rather than probed.
- Landlock and seccomp are effectively absent from the spawn path.
- Plain AppContainer still reads system and Program Files.
- (Added after review) Upstream Linux silently ignores `allowLoopback:false` with network on, which fails G2 for that adapter. Network-enabled Windows spawns grant LAN as well as Internet. The N-API addon runs in the bridge process.

### Blockers
- No non-admin Windows evidence. This is the deciding gap.
- No upstream to depend on, and the native code is unreviewed in full (S-convira-sandbox-4).
- The R03 broker transport must be redesigned for Windows; the lead decides it jointly for R02, R03 and R05 (X-5).
- (Added after review) Reparse points are followed by the ACE writes; must be refused and A10 passed (S-convira-sandbox-1).

### Readiness and evidence quality
- **Readiness:** status B. Implemented and tested in CI on runner configurations only; no independent use.
- **Evidence:** about 75% of this dossier is [inspected], about 15% [CI], about 10% [reported] or [hypothesis]. Every [hypothesis] has an acceptance case.

### Competing solution: anthropics/sandbox-runtime
Compared from `research/_untrusted/anthropics-sandbox-runtime/` at `c40cf14`, v0.0.81, README read [reported unless stated].

| Criterion | Convira sandbox | anthropics/sandbox-runtime |
| --- | --- | --- |
| Windows mechanism | per-spawn AppContainer + Job Object; no admin | dedicated `srt-sandbox` user + machine-wide WFP fence + write-restricted token; **one-time elevated `windows-install`** (README:738-749); "alpha" (README:740-742) |
| Windows reads | deny-by-default except ALL APPLICATION PACKAGES-readable system dirs | sandbox user is granted profile read except credential stores (README:827-899) |
| Windows network | all-or-nothing; loopback never | only via JS proxies in a loopback port range; documented thread-token gap (README:778-782) |
| Linux / macOS egress | none / ports 80, 443 to any host | per-domain allowlist through HTTP/SOCKS proxies; Linux netns removed (README:128; ledger) |
| Honest degradation | probe-gated (Windows); passthrough all-false | `initialize()` verifies the fence and fails (ledger) |
| Known defects | section 8 hypotheses; no advisories | CVE-2025-66479 (fixed); open #402 Windows ACL write escape; #576 macOS deny regex (ledger) |
| Distribution | source only; node-gyp | npm with a bundled `srt-win.exe` |
| Maintenance | 1 author, idle 73 days | active (HEAD 2026-10-19), larger team |

Neither satisfies R02 alone. A reasonable composition is srt for Linux and macOS, because the egress proxy matters for T2, and the Convira-pattern AppContainer backend for Windows, because of the no-admin constraint. Windows Sandbox (the Microsoft VM feature) needs Pro or Enterprise and admin enablement, so it fails "no admin" [reported, Microsoft]. Job Objects alone give limits and kill-tree but no filesystem or network confinement [reported, Microsoft; consistent with `native-windows.ts:142-149`].

### First PR
In the ResonantOS Alpha repo, add `browser-first/host/containment/windows-appcontainer/`:
- the vendored launcher, common header and Job Object addon sources, with NOTICE and VENDORED.md pinning `9013c32`;
- `browser-first/host/containment/win-appcontainer.mjs`, a port of `win-appcontainer.ts` plus `native-windows.ts`.

Then extend `resolveDelegationIsolation` in `browser-first/host/delegation-isolation.mjs:47-69` to return `{mode:"appcontainer"}` on win32 when the probes pass. The win32 assertion in `test/delegation-isolation.test.mjs:110-113` becomes "appcontainer when probes pass, contract-only with reason when they fail". The PR also adds a `windows-latest` job that runs the new `test/delegation-isolation-win32.test.mjs` (cases A1, A3, A6 and A10). It builds the `.node` and `.exe` from the vendored source. The port refuses grant paths that contain a reparse point. The PR does not merge before the full review of the 1,549 vendored native lines is recorded in `VENDORED.md` (section 6 preconditions).

### Confidence
**Medium**, for the Windows-backend decision. The code and CI evidence are strong for an elevated runner. The non-admin path, the memory-cap race and the network-probe gap are unverified.

## 13. Scores (for scoring/scores.csv)

Profile: os_kernel.

| Criterion | Score | Reason (anchor) |
| --- | --- | --- |
| requirement_fit | 4 -> 3 (amended 2026-10-21, S-convira-sandbox-5) | Node/TS, all three OSes, fail-closed Windows. But no-admin Windows, the deciding R02 constraint, is designed and not demonstrated (A2 pending). Linux degradation is not honest for network on with loopback off (G2 split). Windows loopback cannot be granted, which blocks the R03 broker the Alpha needs alongside R02. No egress allowlist |
| demonstrated_maturity | 1 | Anchor 1: pre-release (0.1.0, no releases, not on npm), single author, public life under six months; CI is real but has no usage evidence |
| isolation_and_security | 3 (unchanged; re-checked against the 2026-10-21 clarified anchor) | Anchor 3, clause (b): the property itself is exercised, not a helper. `integration.test.ts` spawns a real confined child on all three CI legs and asserts that reading, writing and network are denied (exit 42), and the Windows probe tests check loopback denial live. Exec escape, non-admin Windows and Linux/macOS loopback are not demonstrated, and there is no audit. Clauses (a) and (d), the lead ruling D3.8, do not apply. There is no advisory and no counterexample row. The inspected Linux `allowLoopback` no-op (S-2) does defeat the loopback property, but it sits in the Linux adapter, which this dossier proposes to learn from, not use. That puts it outside "the artifact as the dossier proposes to use and configure it". The reparse-point code path (S-1) is in the vendored Windows backend, but the defeat is not verified: it is a hypothesis pending A10. **If A10 fails on the vendored backend, this score becomes 0 under (d).** Clause (c): this rates the upstream code as inspected, with those defects counted in the "partly tested" reading |
| licence_suitability | 5 | Apache-2.0 file-level, with NOTICE |
| integration_effort | 4 | Embeddable TS library with a typed API that matches the Alpha's argv-wrapper seam; minus a native build (node-gyp, MSVC) and vendoring since there is no package |
| maintenance_sustainability | 1 | One author, code dump plus one day of fixes, idle 73 days, no outside issues or PRs |
| sovereignty_and_portability | 5 | Local only, no account, no network calls in source |
| interoperability | 3 | Bespoke `SandboxSpawnConfig`; same shape as srt's config but no shared policy format |
| operational_complexity | 4 | In-process library plus a helper exe; minus synchronous multi-second probes and distro sysctl dependence on Ubuntu 24.04 |

**Weighted total (os_kernel weights from `scoring/weights.json`):** 0.18x3 + 0.14x1 + 0.22x3 + 0.10x5 + 0.08x4 + 0.10x1 + 0.08x5 + 0.04x3 + 0.06x4 = **3.02** (was 3.20 with requirement_fit 4). This matches the security reviewer's recomputation in W-1. If A10 fails and isolation_and_security goes to 0 under clause (d), the total would be 2.36.

## 14. Open questions for the adversarial reviewers

1. **Non-admin Windows.** Does the launcher work under a standard user with UAC on? CI runs as `runneradmin`, elevated. This includes DACL writes on the interpreter directories and `CreateAppContainerProfile` per spawn (acceptance A1, A2).
2. **Piped stdio.** It is shown on an elevated runner only, through the integration tests' default-pipe `spawnSync`. I treat the restricted-token 0xC0000142 measurement as not applying to AppContainer, but did not observe a non-admin interactive session.
3. **Firewall dependence.** Is AppContainer outbound denial independent of the Windows Firewall and BFE service state? Unresolved (A4).
4. **Memory-cap race.** Does the outer job ever miss the AppContainer child (A5)? The code makes it possible; I could not measure frequency.
5. **macOS escapes.** Is unrestricted `mach-lookup` / `signal` an exploitable route out (A7)? This is a [hypothesis] from known Seatbelt practice, not a demonstrated escape.
6. **Optimistic maintainer claims:**
   - "Every field ... proven by ... probe" holds on Windows only.
   - "Linux: ... plus Landlock ... and seccomp": Landlock is not in the spawn path and seccomp is skipped without being reported.
   - "the grants are the child's ENTIRE reachable filesystem": not true for ALL APPLICATION PACKAGES-readable paths.
   - Issue #2's description of `available()` does not match the code.
   - "460 passing" includes Windows-only tests that return early on other OSes.
7. **Unpublished callers.** The private callers (`runtime-core` gates, `dev-server-service.ts`) that the comments rely on to refuse unconfined spawns are not published. The public adapter itself now throws instead (`native-windows.ts:273-282`), but the Linux and macOS adapters do not refuse on their own.
8. **Bubblewrap advisory.** I did not verify the 2026 advisory's CVE number recorded by Branch H. The adapter performs no bwrap version check.
9. **Adversarial review record.** The three reviews were answered on 2026-10-21 by s3-amend-convira, standing in for the original inspector, against the clone at `9013c32`. The code archaeologist re-checked 7 citations and all passed; it raised no objections specific to this dossier. The DAO skeptic found none in scope (G4 and G5 confirmed). All objections and the cross-cutting patterns that name this dossier are in the table below.
10. **Reparse-point exploitability** (S-convira-sandbox-1). It is open whether an AppContainer child can create the junction at all under the current Windows mitigation, and whether `SetNamedSecurityInfoW` propagation descends into junctions. A10 settles both.

### Review responses (2026-10-21)

| Id | Verdict | Change made (section) or evidence for dispute |
|---|---|---|
| S-convira-sandbox-1 | accepted (major) | Code fact confirmed: `win_appcontainer_common.h:119-189` writes the DACL on the path as given. The grep in section 8 finds no reparse handling in the Windows code, and the Node side only checks existence and runs `mkdirSync` (`win-appcontainer.ts:276-301, 355-360`). Exploitation stays a hypothesis. Windows' sandboxed mount-point mitigation [reported] may stop an AppContainer child from planting the junction, but it has had bypasses (CVE-2015-2553, CVE-2016-3922) and does not cover unconfined planters. Amended sections 6 (precondition), 7 (conflict 4), 8 (new bullet), 11 (A10), 12 (blocker, first PR). No score change: a hypothesis is not contrary evidence under anchor (a) |
| S-convira-sandbox-2 | accepted (major) | Confirmed: `native-linux.ts:516-530` ignores `allowLoopback` when network is on, with no error, log or report, while `types.ts:70-71` documents it as a control. G2 changed from "Pass, with WARN" to a split: vendored Windows backend Pass, upstream Linux adapter [FAIL] for that combination. The seccomp skip in `catch {}` is classed the same way. Amended sections 5 (property table), 6 (G2), 7 (conflict 3), 11 (A11), 12. Reuse decision unchanged, because Linux is "learn, not vendor" |
| S-convira-sandbox-3 | partly accepted (minor) | Accepted: a network-enabled spawn also grants LAN (`win_appcontainer_common.h:190-211`), and the inherited-handle variant needs launcher support, since `bInheritHandles=TRUE` has no handle list (`win_appcontainer_launch.cc:663-686`). Not accepted: "the launcher owns that window, not the bridge". The profile name, and so the SID (via `DeriveAppContainerSidFromAppContainerName` [reported]), is chosen in Node before the launcher starts (`win-appcontainer.ts:343-346`), so the bridge can create a per-spawn pipe DACL in advance [hypothesis]. Amended section 7, conflict 2 |
| S-convira-sandbox-4 | accepted (minor) | The dossier did not read all of the native code. Recounted the Windows native code at 1,549 lines with `wc -l`, which corrects section 10's "about 1,300". A full review and a from-source Alpha CI build are now preconditions. Amended sections 6, 8 ("Trust in the maintainers"), 10, 12 (first PR) |
| S-convira-sandbox-5 | accepted (minor) | requirement_fit 4 -> 3. No-admin Windows is undemonstrated, Linux degradation is not honest for one combination, and the Windows loopback rule constrains R03. Weighted total 3.20 -> 3.02 (section 13) |
| X-5 | accepted (lead decision) | The Convira-specific facts are recorded in section 7, conflict 2: loopback can never be granted on Windows, the SID is derivable before launch, and inherited handles pass unfiltered. A broker for this backend must be a per-spawn pipe outside the bridge's main listener. The transport choice is left to the lead, as the reviewer asks |
| X-6 | accepted | The N-API addon is in the bridge process; it parses only launcher handshake and probe output [inspected]. Section 8 adds a smaller-surface option: the limit-bearing job moves into the launcher, and the addon stays out of the bridge [hypothesis]. Scoring the surface (W-5, TM-4) is the lead's call; no score change here |
| TM-4 | noted (lead's) | Names the Convira `.node` supply chain. Answered by the section 6 precondition: build from reviewed source in the Alpha CI, never take upstream binaries. No score change |
| W-1 | noted (lead's) | Uses this dossier's total of 3.02 after S-5; section 13 now shows the same figure. The split of the srt row is the lead's |
| A-cross-6 (archaeologist cross-cutting 6, STATUS lines) | accepted | STATUS line added to the header, with `verified: 9013c32 2026-10-21` |
| C-8 (DAO skeptic, status lines) | accepted | Same fix as A-cross-6 |

Isolation score under the lead ruling D3.8 (weights.json clause (d)): 3 is kept. S-2 defeats a property, but only in the Linux adapter, which is not used as proposed. S-1 is in the used artifact, but no defeat has been verified. If A10 fails, isolation_and_security goes 3 -> 0 and the total goes to 2.36.

Contested for the lead:
- whether the bridge can pre-create a per-SID pipe (my reading) or whether the broker must go through the launcher (the reviewer's reading, S-3). Neither has been built or tested.
