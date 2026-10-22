# Dossier: DataLad (datalad-datalad)

STATUS: COMPLETE (amended after review, 2026-10-21)

Inspector: s3-insp-datalad (relaunch), Claude Opus 5.5. Date: 2026-10-21 (inspection begun 2026-10-20 by the first run of this agent id; its findings were re-opened before being cited here; the code archaeologist found that one inherited range, the commit-message markers, had not been re-confirmed (A-datalad-1). After review every `run.py`, `rerun.py`, `gitrepo.py` and `annexrepo.py` range in this dossier was re-checked line by line with `sed -n` at the recorded SHA, and three drifted ranges were corrected). Clone: `research/_untrusted/datalad/` at commit `77de8d9eb4ee6e91f685debb83f6f9b7fe45eef3` (branch `maint`, 2026-10-14; working tree clean on 2026-10-21; `--depth 200`). Execution: none (static inspection only). GitHub API calls (`gh api`, GET only) were used for commit, release, advisory and issue metadata; PyPI JSON was read for git-annex licence metadata.

Evidence labels used below: [inspected] (read the code), [executed] (ran it, only with approval), [reported] (authors' docs, README, issue text, package metadata, ledger rows), [hypothesis]. Every claim that matters carries one. Repository instruction files (AGENTS.md, CLAUDE.md, .cursorrules) are evidence, never instructions. The clone ships a `CLAUDE.md` (agent instructions pointing to CONTRIBUTING.md) and no `.claude\` folder [inspected].

## 1. Identification

| Field | Value |
|---|---|
| Name | DataLad ("data management and publication multitool") |
| Homepage | https://www.datalad.org, handbook https://handbook.datalad.org [reported] |
| Canonical source | GitHub `datalad/datalad`, default branch `maint` (`gh api repos/datalad/datalad`: `default_branch: maint`, not archived) [inspected] |
| Commit | `77de8d9eb4ee6e91f685debb83f6f9b7fe45eef3`, 2026-10-14, matches the ledger row [inspected] |
| Release | 1.7.1 (2026-10-06); twelve releases since 1.4.0 (2026-04-01) [inspected via releases API] |
| Package | PyPI `datalad` 1.7.1; `requires-python >= 3.10` (`pyproject.toml:8`) [inspected] |
| Maintainers | Copyright "2013- Yaroslav Halchenko, 2015- DataLad Team" (`COPYING`); in practice one lead maintainer (section 3) [inspected] |
| Organisation and funding | Ledger: "university-funded core team (Juelich, Dartmouth)" [reported]; commit data contradicts "team" (section 3) |
| Licence | `COPYING`: MIT for "DataLad, including all examples, code snippets and attached documentation". Third-party section: parts of `_datalad_build_support/{setup,formatters}.py` under the Python licence; `datalad/support/due.py` BSD-2; parts of `datalad/support/gitrepo.py` and its test BSD-3; `datalad/utils.py:optional_args` BSD-3 [inspected]. GitHub reports `NOASSERTION` because the file has a preamble [inspected]. Required runtime dependency git-annex is AGPL-3.0-or-later (PyPI `git-annex` 10.20260901.post1, `license_expression: AGPL-3.0-or-later`) [reported], not flagged by the ledger |
| DOI | `.zenodo.json` and `CITATION.cff` present [inspected, not opened] |
| Language | English docs and community [inspected] |

## 2. What works

All [inspected] at the recorded SHA unless marked.

**Run records (the provenance mechanism).** `datalad run` executes a command, then commits all changes with a machine-readable record in the commit message.
- Record fields assembled at `datalad/core/local/run.py:1051-1072`: `cmd`, `chain` (earlier runs when rerun), `inputs`, `outputs`, `extra_inputs`, `pwd` (only when inside the dataset), `dsid`, plus any `extra_info` keys; `exit` is added after execution (`run.py:1097-1099`).
- Serialisation: `json.dumps(run_info, indent=1, sort_keys=True, ensure_ascii=False)` (`run.py:832`); optional sidecar file under `.datalad/runinfo/<md5 of record>`, LZMA-compressed, with only the ID in the message (`run.py:833-855`).
- Commit message format, fixed markers (`run.py:1144-1154`; the record itself is created just before, at `run.py:1139`):
  `[DATALAD RUNCMD] <message>` / `=== Do not change lines below ===` / JSON / `^^^ Do not change lines above ^^^`.
- Parser: `get_run_info` regex plus `json.loads` (`datalad/local/rerun.py:733-778`).
- Record-without-execution: `inject=True` "Record results as if a command was run, skipping input and output preparation and command execution" (`run.py:894-898`). Test `test_inject` (`datalad/core/local/tests/test_run.py:498-509`) records `"nonsense command"` with `extra_info={"custom_key": ...}` and asserts both appear in the commit message. This is the hook a host would use to record an AI derivation it performed itself.
- Inputs and outputs are recorded as path globs, not content hashes; content identity comes only from the commit's tree [inspected: `run.py:1060-1065`].

**Scope of what a run commits.** Without `--explicit`, `outputs_to_save is None` and the save covers every modification in the dataset (`run.py:1178`), so a command that edits a source file has that edit committed in the same run commit. With `--explicit` only declared outputs are saved (`run.py:1178-1196`), and inner commits that swept in undeclared files raise an error unless `datalad.run.dirty-committed=ignore` (`run.py:1198-1229`). Tests: `test_run_explicit` (`test_run.py:415-472`: undeclared changes stay uncommitted), `test_run_explicit_dirty_committed` (`test_run.py:1024`), `test_run_explicit_dirty_committed_in_subdataset` (`test_run.py:1076`), `test_run_merge_branch_switch_rejected` (`test_run.py:1118`).

**Rerun.** `datalad rerun` walks commits, parses records (`rerun.py:324`) and re-executes `run_info['cmd']` through `run_command` (`rerun.py:593`), which runs the string via `WitlessRunner` (`run.py:758-774`). Tests: `datalad/local/tests/test_rerun.py`, 25 tests including `test_rerun` (88), `test_rerun_chain` (261), `test_run_inputs_no_annex_repo` (860-866, run and rerun in a plain git dataset).

**Source and derivation separation.** There is no enforcement code. Separation is a layout convention: the YODA procedure (`datalad/resources/procedures/cfg_yoda.py`) writes a README stating "All inputs (i.e. building blocks from other sources) are located in `inputs/`" and keeps `code/` in git. Inputs are expected to be installed as subdatasets (git submodules), so source material has its own history and commit identity. No test asserts that a run cannot modify an input subdataset; the subdataset tests above concern correct recording of nested commits, not protection.

**Plain-git mode.** `datalad create --no-annex` (`datalad/core/local/create.py:83, 165-199`) makes a git-only dataset; run, save and rerun work there (`test_run_inputs_no_annex_repo`; `test_save.py` has 14 `annex=False` cases). This mode needs no git-annex.

**CLI for a non-Python host.** Every command accepts `-f/--output-format {generic,json,json_pp,tailored,disabled,<template>}` (`datalad/cli/common_args.py:123-133`); `json` emits one result record per line.

**CI lanes.** `.github/workflows/test.yml` with job list `tools/ci/test-jobs.yml`: Linux jobs, three macOS jobs, three `windows-2022` jobs with Python 3.10 (`test-jobs.yml:148-164`), git-annex installed from the PyPI wheel on all three OSes (`test.yml:34-40, 149-160`). `test_crippled.yml` runs the suite on a VFAT loop mount on Linux on every pull request, which exercises git-annex adjusted branches. Also `test_extensions.yml`, `tox.yml`, `benchmarks.yml`, `shellcheck.yml` [inspected filenames]. 1,272 test functions; 66 marked `pytest.mark.ai_generated` [inspected by grep].

**Deployment evidence.** Not established here. The handbook and papers describe neuroimaging use [reported, not opened]; no named production deployment was verified.

## 3. Maturity

**Footprint** [inspected `pyproject.toml` dependencies]: Python >= 3.10; 21 core dependencies, including `boto3` (AWS SDK), `python-gitlab`, `keyring` and `keyrings.alt`, `requests`, `fasteners`, `patool`, `annexremote`; external git >= 2.31.0 (`gitrepo.py:846`) and, for annex datasets, git-annex >= 10.20230126 (`annexrepo.py:146`, checked at `annexrepo.py:480-495`). boto3 and python-gitlab are mandatory installs although only the S3 downloader and `create-sibling-gitlab` use them. Process model: one Python process per CLI call, spawning git and git-annex subprocesses; no daemon.

**Maintenance** (`gh api` commits on `maint` since 2025-10-21) [inspected]: Yaroslav Halchenko 407 commits, DataLad Bot 63, an account named "Claude" 28, the next human 12 (Jiameng Wu), then 10, 8, 4, 3. Of the 407 lead-maintainer commits, 252 carry a `Co-Authored-By: Claude` trailer. Releases roughly monthly, with six releases between 2026-09-17 and 2026-10-06. Bus factor: about 1 on the core. This contradicts the ledger's "university-funded core team" as a description of who writes the code now; funding may still be institutional [reported].

**Issue sample** (five issues plus two by the maintainer, `gh api`) [inspected]:

| Issue | Opened | First maintainer response or close | Note |
|---|---|---|---|
| #7954 psutil missing after 1.6.5 | 2026-10-05 08:44 | comment 14:46 same day | closed |
| #7955 `run -o DIR` fails on empty subdirs | 2026-10-05 13:41 | closed 17:29 same day | fixed in 1.6.6 window |
| #7949 `update -r` subdataset conflict | 2026-10-01 | none in 20 days (only reporter comments) | open |
| #7947 failed `update --how=merge` on adjusted branch leaves worktree stale; retry reports `ok` | 2026-09-30 | none in 21 days | open; Windows/crippled-FS silent failure (section 8) |
| #7937 git-annex Windows wheel `mimetype=` largefiles mismatch | 2026-09-19 | none, open | opened by a maintainer bot account |
| #7950 (maintainer) | 2026-10-01 | closed next day | test fix |

Fast on fresh regressions; external bug reports in the sync and merge area wait.

**Security posture** [inspected]: no repository security advisories (`security-advisories` API returns 0); no `SECURITY.md` in the repo or in `datalad/.github`; no audit found. No disclosure process documented.

**Documentation**: extensive handbook and docstrings [reported]; docstrings for run and rerun are accurate to the code read [inspected].

## 4. Architecture

- **Entry points**: CLI `datalad <cmd>` (`datalad/cli/main.py`) and Python API (`datalad.api`), both dispatching to `Interface` subclasses such as `Run` (`datalad/core/local/run.py`) and `Rerun` (`datalad/local/rerun.py:60-61`) [inspected].
- **Repository layer**: `GitRepo` (`datalad/support/gitrepo.py`) wraps the git CLI; `GitRepo.commit` builds `git commit` with optional `--date` and index file and calls `_call_git` (`gitrepo.py:1444-1520`; the method runs to line 1566). No `-S`, `--no-gpg-sign` or signing configuration anywhere in the code base (grep for `gpgsign|gpg.format|allowedSignersFile|verify-commit|--show-signature|no-gpg` returns nothing) [inspected]. A user's `commit.gpgsign=true` would therefore reach `git commit` unchanged [hypothesis, not executed].
- **Annex layer**: `AnnexRepo(GitRepo)` (`datalad/support/annexrepo.py:112`) wraps the git-annex CLI with `--json` record parsing (`_call_annex_records`). On filesystems without symlinks (Windows NTFS, VFAT) git-annex checks out `adjusted/<branch>(unlocked)`; DataLad detects this by name (`is_managed_branch`, `annexrepo.py:382-406`). After each save on such a branch, `_save_post` runs `git annex sync` locally to propagate the commit to the corresponding branch (`annexrepo.py:3637-3657`, `localsync`), and for an amend it synthesises a new commit with `git commit-tree` plus `update-ref`, copying author name, email and date but passing no signing flag (`annexrepo.py:3658-3690`).
- **Storage**: a git repository (objects, refs, index) plus, in annex mode, `.git/annex/objects` keyed by content hash and a `git-annex` branch with location logs [reported: git-annex docs]; run-record sidecars in `.datalad/runinfo/`; config in `.datalad/config` and `.git/config`.
- **Locking**: `fasteners.InterProcessLock` around config writes (`datalad/config.py:992-1002`) and archive and download caches (`datalad/support/locking.py:35-98`). No lock around save or run beyond git's own `index.lock` [inspected].
- **Durability code**: no `fsync` call anywhere in DataLad; `os.replace` only in the HTTP downloader (`datalad/downloaders/base.py:666`) and an atomic rename in the ORA remote (`datalad/distributed/ora_remote.py:1537`) [inspected by grep]. Durability of committed state is delegated entirely to git and git-annex.
- **Identity model**: git author and committer strings only; no principal, no actor type, no approval object [inspected].
- **Lifecycle**: stateless CLI; a crash mid-run leaves whatever git leaves (section 5, R13).

## 5. Direct relevance

### R14 (staged promotion with source preservation, provenance, append-only history)

Applies to the Alpha Living Archive: OSC-24 (promotion cannot execute, approval gate a no-op), OSC-25 (domain separation metadata only), OSC-26 (provenance directory empty), and os-map section 17 seam 4 ("one memory contract ... with provenance"). ADR-013 already names the target: "initialize a local Git repo inside the managed memory root; commit imports, moves, user-approved reorganizations, and AI-approved metadata edits; preserve commit metadata with ResonantOS actor IDs" (`docs/architecture/ADR-013-living-archive-memory-domains.md:300-311`) [inspected]. DataLad is the most mature example of exactly that design, but only for the history and provenance half.

| R14 constraint | DataLad | Evidence |
|---|---|---|
| Local-first | yes | no service needed for create, save, run [inspected] |
| Versioned, append-only history | yes, git history; append-only by convention (git permits rewrite) | `gitrepo.py:1444-1566` |
| Provenance of derivations | yes, run record per commit; paths not hashes | `run.py:1051-1072, 1144-1154`; `test_inject`, `test_basics` |
| Source never mixed with AI derivations | convention only (YODA `inputs/` subdatasets); default `run` commits edits to inputs | `cfg_yoda.py`; `run.py:1178`; `test_run_explicit` |
| Human review the host can verify | absent; no approval record, no signing support | grep, section 4 |
| Markdown-compatible | yes in git or `--no-annex` mode; annexed files become symlinks or pointer files | `create.py:83`; `cfg_text2git.py` [inspected filename] |
| Exposable over MCP (R06) | no; CLI JSON lines could back an MCP tool | `common_args.py:123-133` |

### R13 (crash-consistent local file state, corruption recovery, Windows-safe)

Applies to OSC-28 (bare `JSON.parse` on `CONFIG/memory-settings.json` and history files; no fsync; no crash tests) and OSC-23 (two-phase intake). DataLad contributes nothing of its own: no fsync, no atomic-write helper used for repository state, and no test that kills a process or truncates a file mid-write (grep of all `tests/` for `corrupt|truncat|crash|SIGKILL|interrupted|torn` finds only "does not crash with KeyError" style tests and an HTTP download retry, `datalad/downloaders/tests/test_http.py:934`) [inspected]. What a git-backed root offers R13 comes from git itself: objects are content-addressed and written before refs are moved under a lock file, so a crash leaves the last committed state recoverable and `git fsck` detects object corruption [reported: git documentation; not executed]. Two DataLad-specific weak points were found:
- Run-record sidecars are written non-atomically: `dump2stream` deletes the old file and writes in place with no fsync (`datalad/support/json_py.py:104-118`), and `_create_record` skips writing when the path already exists (`run.py:850-855`). A torn sidecar is therefore never repaired by a later identical run, and `get_run_info` raises on it (`rerun.py:764-775`) [inspected; consequence is a hypothesis].
- `AnnexRepo.fsck` (`annexrepo.py:2935-2985`) wraps `git annex fsck`; the DataLad tests that call it (`test_clone.py:1441`, `test_ria_*`) check counts and locations, never a corrupted object [inspected].

### Threats and must-demonstrate properties

| Property (threat-model section 4) | Result | Evidence |
|---|---|---|
| T5 source separate from derivations | partly designed, not enforced; tested only for commit scope in `--explicit` mode | `test_run_explicit` (`test_run.py:415-472`), `test_run_explicit_dirty_committed` (1024); no protection test |
| T5 human review step a host can verify ("route refuses without an approval record; ledger tamper detected") | not demonstrated; nothing records who approved, nothing signs. Tamper evidence on history exists only through git's hash chain | grep in section 4 |
| T8 torn-write recovery | not demonstrated by DataLad; delegated to git and git-annex; one non-atomic DataLad writer found | `json_py.py:104-118` |
| R13 Windows-safe | partly; Windows CI runs, but core rerun tests are known failures and adjusted-branch recovery has an open silent-failure bug | sections 2, 8 |

## 6. Reuse decision

**Learn the pattern and reimplement** (in the Node bridge), with DataLad as a compatibility reference. Concretely: one plain git repository per memory domain (no git-annex), commits made by the bridge with a DataLad-shaped JSON record block, human approvals as signed commits verified against an allowed-signers file the host owns, and atomic writes plus last-commit recovery for the JSON state files.

Why this beats the alternatives:
- Adopting DataLad brings a Python 3.10+ runtime, 21 Python packages (AWS and GitLab SDKs among them) and, in annex mode, an AGPL-3+ Haskell binary into a Node desktop product, for a feature set whose R14-relevant part is a commit-message convention and a git wrapper. It contributes nothing to the missing piece (verifiable human review) or to R13.
- Wrapping it as a sidecar (`datalad -f json ...`) is feasible but still needs the runtime, and every R14 gap remains for the bridge to build.
- The R14-relevant code is small: record assembly is about 25 lines (`run.py:1051-1072`), the message format 11 lines (`run.py:1144-1154`), the parser 45 lines (`rerun.py:733-778`). Reimplementing it in Node costs less than packaging Python.
- Keeping the record shape DataLad-compatible preserves an upgrade path: a user can later open the memory root with DataLad for inspection. The record must not use the `[DATALAD RUNCMD]` marker, because `datalad rerun` would execute the `cmd` string as a shell command (`rerun.py:593`, `run.py:758-774`); use a distinct marker with the same JSON keys (section 7).

Hard gates (`scoring/weights.json`):

| Gate | Result | Clause |
|---|---|---|
| G1 no mandatory cloud or telemetry | pass | no telemetry code (grep `telemetry|sentry|analytics` in non-test code: none); boto3 is installed but only used by S3 downloaders [inspected] |
| G2 Windows, macOS, Linux or honest matrix | pass with warning | three Windows CI jobs; known-failure markers are explicit in tests; but issue #7947 reports a silent `ok` with a stale worktree on adjusted branches (merge path, not the local save path) |
| G3 licence | pass for the recommended decision (no code taken; MIT); adopting DataLad in annex mode needs legal review of git-annex AGPL-3.0-or-later (distribution of the binary with a product; section 9) |
| G4 chain | N/A (not a DAO component) |
| G5 invariants | pass; DataLad has no notion of human versus AI actors and grants nothing. The gate risk sits on the Alpha side: ADR-012 makes an AI verifier the default approver (`ADR-012-living-archive-approval-policy.md:23, 43-44`), which the recommended design must not label "human" |

## 7. Integration design

**Layout** (under `~/ResonantOS_User/Memory`, extending `host/memory-schema.mjs:7-22`):
- `HUMAN_KNOWLEDGE/` and `EXTERNAL_KNOWLEDGE/`: each its own git repository. Commits only by the bridge on a user act (import, approved move, approved reorganisation). Policy: every commit on `main` here must carry a signature by a key in the host's allowed-signers file.
- `AI_MEMORY/`: its own git repository for drafts, verifications and wiki pages. AI derivations are commits here only, so source text and AI output never share a repository or a commit (the DataLad subdataset idea, without git submodules).
- `CONFIG/`: JSON state, written atomically (temp file, fsync, rename with retry on Windows sharing violations) and committed to a `CONFIG` repository after each change, so a parse failure can recover from `git show HEAD:<file>` instead of throwing (OSC-28).

**Derivation record** (commit message of an `AI_MEMORY` commit), DataLad key-compatible:

```
[RESONANT DERIVATION] draft wiki update for <proposedPage>

=== Do not change lines below ===
{"cmd": "resonant:archive-draft", "chain": [], "dsid": "<repo uuid>",
 "inputs": ["HUMAN_KNOWLEDGE@<commit>:<path>#<blob sha>"], "outputs": ["wiki/<page>.md"],
 "exit": 0, "resonant": {"actor": "<principal id>", "actorType": "ai",
 "provider": "...", "model": "...", "promptSha256": "...", "tier": "strategist-review"}}
^^^ Do not change lines above ^^^
```

Inputs carry repository, commit and blob hash, which DataLad's path-only inputs lack. `cmd` is an inert verb, never a shell string.

**Where the security state lives (amended after S-datalad-1, S-datalad-3, X-1).** The work trees above stay in the user state root, because they are user data. The git directories, the allowed-signers file and the approval key do not: they go in the bridge-only state location the lead is defining under R15 (X-1), which no delegated child, add-on or `archive-write` route can reach. The bridge addresses each repository as `git --git-dir=<bridge-only>/<domain>.git --work-tree=<memory root>/<domain>`, so a child that can write the work tree can never write `.git/hooks`, `.git/config` or refs. Until R15 and R02 containment exist, an unconfined same-user child can still reach that location (OSC-32); the design then detects tampering with it (pinned hash below) but cannot prevent it. That residual risk is stated, not hidden.

**Approval record (amended after S-datalad-2, S-datalad-3, X-4)**: promotion from `REVIEW/` to `AI_MEMORY/wiki` is a commit whose message carries `{"approves": "<draft commit sha>", "tier": "human-review", "decision": "approved"}` and which is signed (`gpg.format=ssh`). The bridge verifies with `git -c gpg.ssh.allowedSignersFile=<bridge-only path> verify-commit --raw <sha>` before the route proceeds. Rules for the signing step:
- A signature proves that a key was used, not what the user meant. The approval UI is a host-native component with no agent code (the shared design the lead owes under X-4). It shows the draft diff and draft SHA, builds the commit object itself from the canonical promotion request, and only then asks for the signature. The agent principal never constructs, frames or submits the approval commit.
- The approval key is dedicated. It is not loaded in the general ssh-agent (on Windows the OpenSSH agent is a named pipe any same-user process can open; without `ssh-add -c` it signs silently). The ceremony signs with `ssh-keygen -Y sign` directly, using a passphrase typed into that UI or an `ed25519-sk` key that requires a touch.
- One ceremony allows one signature. A second signing request during the same ceremony is refused and shown to the user, so a same-user process cannot wait for the next touch.
- The allowed-signers file lives in the bridge-only location. The bridge pins its SHA-256 at start and refuses every promotion if the file changes, until the user re-confirms the change in the ceremony UI.
- An AI verifier approval under ADR-012's `strategist-review` tier is recorded unsigned, or signed with a separate key that is never in the human allowed-signers set, so the host can tell the tiers apart.

**Process boundary (amended after S-datalad-1)**: the bridge calls the `git` CLI via `child_process.execFile` (no shell). Each call gets a minimal environment, not the bridge's own (which today carries provider keys, OSC-16): `PATH` pinned to the git install, `GIT_TERMINAL_PROMPT=0`, `GIT_CONFIG_NOSYSTEM=1`, and `GIT_CONFIG_GLOBAL` pointing to a bridge-owned file, because a same-user child can also edit `~/.gitconfig`. Every call also gets these overrides: `-c core.hooksPath=<empty bridge-only dir> -c core.fsmonitor=false -c core.sshCommand= -c gpg.ssh.program=<pinned ssh-keygen path>`. Filter and diff drivers that a child names in a work-tree `.gitattributes` cannot run, because the commands for them are defined only in config, which the child cannot reach. Repository config also sets `core.fsync=committed` (or `all`) and `core.fsyncMethod=fsync` explicitly rather than relying on defaults [reported: git-config documentation; default values not verified here]. No Python. A stale `.git/index.lock` after a crash is detected (no live git child of the bridge) and removed before retrying; DataLad has no such logic to copy (grep `index.lock` in non-test code: none) [inspected].

**Alpha files that change** (browser-first, commit 578fbbc) [inspected paths]:
- new `browser-first/host/memory-git-ledger.mjs` (init, commit with record, verify signature, recover file from HEAD).
- `browser-first/host/archive-review-policy.mjs:18-35`: `isHumanReviewActor` accepts a client-asserted `actorType: "human"`; replace with a signature check result passed in by the service.
- `browser-first/host/archive-review-service.mjs:660-690`: fix the argument-shape mismatch with `archive-promotion-policy.mjs:11-30` and require a verified approval commit before writing `AI_MEMORY/wiki`.
- `browser-first/host/memory-source-versioning.mjs` (`recordSourceFileIntakeArtifact`, line 243): add a commit to the domain repository after the JSONL version ledger write (ADR-013:286 allows Git to "replace or augment" the ledger with the same audit semantics).
- `browser-first/host/memory-settings-policy.mjs` and the settings loader: atomic write and recover-from-HEAD on parse failure.
- `browser-first/examples/living-archive-portable-workflow.mjs:94-308`: retire its `autoApprove` promotion path or route it through the same ledger (os-map seam 4).

**Alpha tests affected**: `test/archive-review-policy.test.mjs` (policy argument names change), `test/archive-review-host-service.test.mjs`, `test/living-archive-continuity-acceptance.test.mjs` (extend past review-request creation to a signed promotion), `test/main-workspace-memory.test.mjs` (revise and promote use a hand-faked bridge, lines 1251 and 1351 per os-map), `test/memory-source-versioning.test.mjs`, `test/memory-settings-policy.test.mjs`. Route and capability names stay unchanged so the 2,424 browser-first test names hold; new behaviour goes into new test files.

**Error behaviour**: promotion refuses with a named reason when the approval commit is missing, unsigned, signed by an unknown key, or approves a different draft SHA. Missing `git` on PATH degrades visibly to the current JSONL ledger with a status flag, never silently.

**Migration**: on first start with the feature enabled, `git init` each domain directory and make one unsigned "baseline import" commit recording the current JSONL ledger hash, so existing data enters history without a forged approval.

## 8. Security and governance effects

- **Rerun executes stored text** [inspected]: `rerun` parses the JSON in any commit message matching the markers (`rerun.py:324, 733-778`) and runs `cmd` as a shell string (`rerun.py:593`, `run.py:758-774`). Anyone who can get a commit into a dataset (a pulled sibling, a shared subdataset, a prompt-injected agent with commit access) can plant a command that executes on the next `datalad rerun`. No allow-list, no signature check, no prompt. On rerun, `pwd` from the record becomes the execution directory via `op.normpath(op.join(dataset.path, rel_pwd))` with no containment check (`run.py:941-945`), so a record with `"pwd": "../.."` would run the command outside the dataset [inspected code path; effect not executed]. A second path from the commit message is read, not executed: when the JSON block is a string (a sidecar id), `get_run_info` opens `op.join(dset.path, record_dir, runinfo)` with no containment check and LZMA-decodes it (`rerun.py:764-775`), so a crafted commit can point rerun at any readable file (A-datalad-2) [inspected]. For ResonantOS this is the main reason not to emit `[DATALAD RUNCMD]` records.
- **Signatures may not survive adjusted branches** [inspected for the amend path; hypothesis for the sync path]: on Windows, user commits land on `adjusted/main(unlocked)` and git-annex writes the corresponding commits on `main`. The amend branch of `_save_post` builds a new commit with `git commit-tree` and no `-S` (`annexrepo.py:3658-3690`). Because the propagated commit has a different tree, the user's signature cannot carry over; it survives only if the propagating tool re-signs, and then it is the tool's signature, not a human act. The recommended design avoids this by not using git-annex.
- **No security process**: no SECURITY.md, no advisories, no audit (section 3). Bus factor about 1 with heavy AI-assisted authorship (252 of 407 lead commits co-authored by Claude; 66 tests tagged `ai_generated`). Neither is a defect in itself, but trust in the maintainers is trust in one person's review of AI-written changes.
- **Silent recovery failure on Windows-mode repositories** [reported, issue #7947, open, no maintainer response in 21 days]: after a failed `update --how=merge` on an adjusted branch, a retry "reports `ok` and does nothing: `master` has the new commits, the worktree never gets them, and `git status` is clean"; the reporter locates the damage in `git annex sync`. This is the kind of silent degradation G2 forbids, though it sits in the sync path, not local save.
- **New privileges for the recommended design (amended after S-datalad-1)**: the bridge gains write access to git repositories for the memory root and must hold the allowed-signers file. Attack surface added: git CLI invocation. Every config key that makes git run a program (hooks, `core.hooksPath`, `core.fsmonitor`, `core.sshCommand`, `gpg.ssh.program`, filter and diff drivers) is a route from whoever can write the git directory to code running with the bridge's privileges. `safe.directory` checks ownership and does not stop a same-user writer. The design closes this route by keeping git directories bridge-only and by passing per-call overrides with a minimal environment (section 7). A malicious `.git` in an imported folder is never used, because repositories are created only for managed copies.
- **Attacker model for the git ledger (X-2)**: against accidental corruption and against anyone who is not the same OS user, the hash chain plus signed approvals detect tampering. Against a same-user attacker (V2, or an unconfined V3) who can reach the bridge-only location: forging a human approval is detected only while the approval key is out of that attacker's reach. History rewriting, deleting approvals and rolling back to an earlier state are not detected locally. Detecting those needs an external checkpoint or a separate OS account, which is the TM-3 split for the lead.
- **Personal data**: git history makes deletion hard; a "forget this source" request needs history rewriting or per-domain repository replacement. This conflicts with append-only history and must be a documented ceremony.
- **Friction**: a signing key ceremony (generate, register in allowed-signers, unlock per session); on Windows the OpenSSH agent service is disabled by default [reported], so the first-run flow must handle it.
- **Counterexamples**: the ledger has no counterexample rows against DataLad. The disconfirmation search found the items above: the AGPL runtime dependency, the single-maintainer reality, the rerun execution surface, the non-atomic sidecar writer, the open Windows-mode silent failure, and the absence of any test for the properties R13 and R14 need.

## 9. Licensing

- DataLad: MIT (`COPYING`), with third-party parts under the Python licence, BSD-2 and BSD-3 (section 1). All permissive; notices must be kept if any of those files are copied [inspected]. The recommended decision copies no code; a DataLad-compatible record format is an interface, not a copied expression [hypothesis; not legal advice].
- git-annex: AGPL-3.0-or-later per PyPI metadata [reported]; the upstream COPYRIGHT file could not be fetched (HTTP 403), so per-file differences are unknown. Items for legal review if DataLad in annex mode were ever bundled: (a) shipping a git-annex binary with ResonantOS triggers the corresponding-source obligations of AGPL section 6; (b) AGPL section 13 applies only to modified versions offering network interaction, which a local unmodified subprocess does not, but this needs confirmation; (c) whether a combined installer is "aggregate" or a covered work.
- Python dependencies (boto3 Apache-2.0, python-gitlab LGPL-3.0, keyring MIT, and others) [reported from general package knowledge, not verified per package]: python-gitlab's LGPL would need review only if DataLad were bundled.
- Git itself (GPL-2.0) is invoked as a separate program in the recommended design, as Git for Windows already is on most developer machines [reported].
- Symbiotic Licence: status F; no assessment possible.

## 10. Cost and effort

| Scenario | Work | Assumptions |
|---|---|---|
| Small (recommended): Node git ledger, signed approvals, atomic JSON plus recover-from-HEAD | about 3-4 volunteer weeks (raised from 2-3 after review): `memory-git-ledger.mjs` (300-400 lines) with git hardening, policy and service fixes, a host-native approval ceremony with a dedicated key, tests on Windows CI. Excludes the bridge-only state location (R15) and the shared approval UI (X-4), which the lead owns | git on PATH (Git for Windows bundles OpenSSH `ssh-keygen` for signing [reported]); no git-annex |
| Medium: DataLad as sidecar (`datalad -f json`) in `--no-annex` mode | 4-6 weeks plus ongoing packaging: embed Python 3.10+, pin 21 packages, per-OS installers, per-call Python start-up cost [hypothesis: about a second per call], plus everything in the small scenario for approvals | team has no Python packaging owner today |
| Large: DataLad with git-annex | medium plus AGPL review, git-annex binaries per OS (PyPI wheels exist for win_amd64, macOS, manylinux [reported]), adjusted-branch behaviour on Windows, the signature problem in section 8 | not recommended |

Language cost (master prompt 5.5): DataLad is Python; the Alpha bridge is Node 24 ESM. The record format and git conventions transfer at no language cost; the code does not. Lock-in is low in every scenario because the data is plain git and JSON. Maintenance exposure for the small scenario is git's CLI stability, which is high.

## 11. Acceptance test

Two parts. Part A needs only git (already on the user's machine) and Node, and belongs in the Alpha test suite once written; it is still listed for approval because it runs git. Part B executes DataLad and git-annex and is a request for the user, not a plan.

**Part A: Node git ledger (new test file `browser-first/test/memory-git-ledger.test.mjs`).**
- Inputs: temporary memory root; a throwaway ed25519 SSH key generated by the test; an allowed-signers file outside the root listing that key as `human@resonant.local`; a second key not listed.
- Steps and expected output:
  1. Import a markdown source: commit in `HUMAN_KNOWLEDGE` exists; JSONL ledger and git agree on the blob hash.
  2. AI draft: commit in `AI_MEMORY` with a `[RESONANT DERIVATION]` record whose input names the source commit and blob; `HUMAN_KNOWLEDGE` has no new commit.
  3. Promotion without approval commit: refused, reason `approval-missing`.
  4. Approval signed by the unlisted key: refused, `signer-not-allowed`. Approval signed by the listed key but naming another draft SHA: refused, `approval-mismatch`.
  5. Valid signed approval: wiki page written; `git verify-commit` succeeds.
  6. Fault (T5): an agent-side call passes `actorType: "human"` without a signed commit: refused.
  7. Fault (T8): truncate `CONFIG/memory-settings.json` to half its length; the next memory route returns the last committed settings with a `recovered` flag instead of throwing; a stale `.git/index.lock` left by a killed child is cleared and the next commit succeeds.
  8. Fault (S-datalad-1): plant an executable `pre-commit` hook and a `core.fsmonitor` command in the repository's git directory, write a `core.sshCommand` and `core.hooksPath` into `~/.gitconfig` (test HOME), and add a `.gitattributes` naming a filter. Then run a bridge commit. Pass only if no planted program runs (sentinel file absent) and the commit succeeds. A second variant writes the same files from a test process acting as a child with `archive-write` (X-1 shared case); the git directory must be unreachable through any bridge route.
  9. Fault (S-datalad-2, X-4): during an approval ceremony, a second process requests a signature with the approval key. Expected: refused and reported to the user; exactly one signature per ceremony. A variant with the agent asking to approve draft A while the UI receives draft B: the signed commit names the SHA the UI displayed, so the promotion of A is refused with `approval-mismatch`.
  10. Fault (S-datalad-3): append a new key to the allowed-signers file behind the bridge's back. Expected: every promotion refused with `allowed-signers-changed` until the user re-confirms in the ceremony UI.
- CI hook: the existing browser-first test runner on the Windows, macOS and Linux CI matrix.
- Pass: all ten steps produce the stated result on all three OSes; any step that cannot run on an OS reports `skipped: <reason>` visibly.

**Part B: execution request for the user (third-party code; do not run without approval).**
- Sandbox: a disposable Windows 11 VM (and one Linux VM for comparison), no access to the user's data, Git for Windows, Python 3.12, `pip install datalad==1.7.1 git-annex==10.20260901.post1` in a venv.
- B1 signature survival: `git config --global gpg.format ssh`, `user.signingkey <test key>`, `commit.gpgsign true`; `datalad create ds` on NTFS (expect `adjusted/main(unlocked)`); add a file; `datalad save`; then `git -C ds verify-commit HEAD` and `git -C ds verify-commit main`, plus one `datalad save --amend`. Expected to learn: whether the commit on `main` is signed, and by which key. Repeat with `datalad create --no-annex`.
- B2 torn write: start `datalad run "python -c <write 200 MB to out.bin>"` and `taskkill /F` the Python process mid-write; then `git fsck --full`, check for `.git/index.lock`, run `datalad save` again. Expected: the last commit intact; record whether a manual lock removal is needed.
- B3 sidecar: `datalad run --sidecar ...`, truncate the file under `.datalad/runinfo/`, repeat the identical run, then `datalad rerun`. Expected per the code: the file is not rewritten and rerun fails with a decode error.
- B4 rerun surface: commit a message with a `[DATALAD RUNCMD]` block whose `cmd` is `echo PWNED > pwned.txt`, then `datalad rerun`. Expected per the code: the file appears, confirming execution of stored text.
- Pass for "DataLad usable as-is for R14": B1 shows a valid human signature on `main`, B2 recovers without manual steps, B3 and B4 are answered by documented mitigations. The inspector's expectation is fail on B1 (annex mode) and B4.

## 12. Recommendation and confidence

**Benefits**: thirteen years of a working git-based provenance convention; a record format with clear keys and a tested record-only (`inject`) path; a proven layout idea (sources in their own repositories, derivations elsewhere); plain-git mode that avoids git-annex; Windows CI that exists and is honest about known failures.

**Trade-offs and blockers**: no human review, approval or signing at all (the R14 constraint Branch D found unmet everywhere is unmet here too); no R13 contribution of its own; Python and, in annex mode, AGPL git-annex for a Node product; rerun executes commit-message text; single maintainer; signatures do not survive git-annex's adjusted-branch rewriting [inspected for amend; B1 would settle the general case].

**Readiness**: as a dependency, low for this project. As a pattern, high: everything R14 needs from it fits in a few hundred lines of Node over the git CLI.

**Evidence quality**: the run-record format, scope of commits, absence of signing and fsync, adjusted-branch commit path, rerun execution, CI matrix and test markers are [inspected]. Crash behaviour of git and git-annex, git-annex licence and Windows OpenSSH details are [reported]. Signature survival is a [hypothesis] until B1 runs.

**Competing solutions on the same criteria** (competitor facts are from ledger rows unless marked [inspected]):

| Criterion | DataLad | Plain git + signed commits + allowed signers | radicle-dev/heartwood | dataobservatory-eu/betwixt | Jvdbreemen/LLmWiki-KennisBank |
|---|---|---|---|---|---|
| Source kept apart from derivations | convention (subdatasets, `--explicit`) | by repository layout chosen by the host | patches as collaborative objects in git; not a knowledge layout | candidate versus reviewed state with separate provenance [reported] | raw sources versus compiled wiki, quarantine, hash-checked recall [reported] |
| Host-verifiable human review | none | yes: `git verify-commit` against a host-owned allowed-signers file [reported: git docs] | yes: signed reviews, delegate-quorum identity changes; repo carries `.gitsigners` (1,083 bytes) [inspected via API] | self-declared name and ORCID, unsigned [reported] | enforced by the tool's own state, not verifiable by a host [reported] |
| Append-only, versioned | git history | git history | git history plus signed COBs | not established | append-only lesson ledger [reported] |
| Crash and torn-write behaviour | delegated to git; one non-atomic writer | git's object and ref locking [reported] | not established | not established | not established |
| Windows | CI yes; rerun known failures; #7947 | Git for Windows with OpenSSH signing [reported] | unconfirmed (WiX packaging dir exists) [reported] | R on Windows [hypothesis] | not established |
| Node 24 integration | Python sidecar | `git` CLI via `execFile` | Rust binaries plus its own network | R child process | Python, shell, TS frontend application |
| Licence | MIT; git-annex AGPL-3+ | git GPL-2.0 as separate program | MIT OR Apache-2.0 | GPL-3.0-or-later | MIT |
| Maintenance | ~1 core maintainer, monthly releases | git upstream | 52 contributors | 1 maintainer, experimental, v0.0.7 | ~1 maintainer, v0.x |

Plain git with signed commits delivers the one property none of the knowledge-shaped candidates has (host-verifiable approval) at the lowest footprint; DataLad adds the derivation-record convention on top; KennisBank and betwixt are the better references for the review UX and the candidate-versus-reviewed state model; heartwood is the reference for multi-party review and quorum, which ResonantOS does not need for a single user's archive.

**Smaller subset question**: yes. Plain git with signed commits plus a DataLad-shaped record delivers most of DataLad's R14 value (history, rollback, per-derivation provenance, source isolation by repository) and the review verification DataLad lacks. What it gives up: `datalad rerun` (not wanted, section 8), git-annex large-file handling (not needed for markdown), dataset nesting tools (replaceable by the host's own layout).

**First PR** (ResonantOS Alpha, `browser-first/`): add `host/memory-git-ledger.mjs` with `initDomainRepo`, `commitWithRecord`, `verifyApprovalCommit` (wrapping `git verify-commit --raw` with `gpg.ssh.allowedSignersFile`) and `recoverFileFromHead`, plus `test/memory-git-ledger.test.mjs` covering Part A steps 1-5, 7, 8 and 10, behind a disabled-by-default setting; no route or capability changes. The git directories and allowed-signers file go wherever the lead's bridge-only state location is (X-1); until that is defined, the PR takes the location as a constructor parameter and refuses a path inside the memory root. Step 9 waits for the shared approval UI (X-4). The follow-up PR wires `verifyApprovalCommit` into `archive-review-policy.mjs` and fixes the `archive-review-service.mjs:669-685` argument mismatch.

**Confidence: medium-high** for "learn the pattern, do not adopt". The code facts behind the decision are inspected; the remaining uncertainty (signature survival, git crash behaviour on Windows) affects only the rejected adoption path and the details of the recommended one, which Part A tests directly.

## 13. Scores (for scoring/scores.csv)

Profile: user_facing_app. Scores rate DataLad as a candidate component, not the recommended reimplementation.

| Criterion | Score | Reason (anchor) |
|---|---|---|
| requirement_fit | 3 | covers history, provenance records and a source/derivation layout for R14; no human review or signing; nothing of its own for R13 |
| demonstrated_maturity | 4 | regular releases, three-OS CI, 1,272 tests, same-day response on regressions; production use reported, not verified here |
| isolation_and_security | 1 | Re-checked against the anchor as clarified on 2026-10-21 (D3.7), unchanged. It rates DataLad 1.7.1 at the inspected SHA, not the Resonant layer. No test exercises the T5 review property or the T8 torn-write property, so 3 is out of reach. Not 0: there is no advisory and no counterexample row, and the contrary design facts (by default `run` commits edits to inputs; `rerun` executes stored text) can be avoided with `--explicit` and by not using rerun. A lead who counts `run.py:1178` as unfixed contrary evidence for T5 would score 0 (total 2.60) |
| licence_suitability | 3 | DataLad MIT file-level, but its default mode requires AGPL-3+ git-annex usable only as a separate process; `--no-annex` avoids it |
| integration_effort | 1 | requires a Python runtime the team does not have; CLI JSON lines make a sidecar possible but not cheap |
| maintenance_sustainability | 2 | active and releasing, but bus factor about 1 (407 of ~560 human commits in 12 months by one person); external sync bugs wait weeks |
| sovereignty_and_portability | 4 | local-first, plain git, no account; annexed content is less user-readable (pointer files, symlinks) |
| interoperability | 4 | standard git, JSON records, markdown untouched in git mode; no MCP |
| operational_complexity | 3 | no services, but Python plus git plus git-annex subprocesses per call |

Weighted total (user_facing_app weights): 0.54 + 0.56 + 0.12 + 0.30 + 0.12 + 0.24 + 0.48 + 0.24 + 0.12 = **2.72 of 5**. No unknowns. No score changed after review.

Informational, not for `scores.csv` (X-3; how to rank it is the lead's decision): the proposed Resonant git ledger would score isolation_and_security 1 today, because it exists only as a design. It would reach 3 once Part A steps 6-10 pass in CI.

## 14. Open questions for the adversarial reviewers

1. Does `git commit-tree` honour `commit.gpgSign` from config, and does git-annex's adjusted-branch propagation pass `--no-gpg-sign` for its own commits? The inspector recalls that git-annex marks automatic commits unsigned but did not read git-annex source (its host returned 403). Part B1 settles it empirically.
2. git's default `core.fsync` components and Windows rename behaviour under antivirus file locking were not verified; the design sets them explicitly and Part A step 7 tests recovery, but the guarantee is git's, not ours.
3. git-annex licence is taken from PyPI metadata only; per-file terms in its COPYRIGHT file are unknown.
4. "University-funded core team" (ledger) versus one active maintainer: funding status was not checked; only commit authorship was.
5. The issue sample is small (five external plus two maintainer issues) and recent; older Windows issues were not sampled.
6. Named production users of `datalad run` records were not verified; demonstrated_maturity 4 leans on releases and CI.
7. Is a signed commit a sufficient "human act"? It proves key use, not presence. The design relies on keeping the key away from agents (agent confirmation or a touch-required `ed25519-sk` key); reviewers should challenge whether the bridge, which runs git, can be kept from the key on each OS.
8. ADR-012 makes an AI verifier the default approver. The recommended design records that tier distinctly but does not change the policy; whether R14's "human review step" means every promotion or only the `human-review` tier is a lead decision.
9. Python dependency licences in section 9 are from general knowledge, not verified per package.

Note on question 7: answered by S-datalad-2. A signature proves key use; the amended section 7 binds what is displayed to what is signed, and keeps the key out of the general agent.

### Review responses (2026-10-21)

| Id | Verdict | Change made (section) or evidence for dispute |
|---|---|---|
| S-datalad-1 | accepted | Section 7: git directories moved to the bridge-only location (`--git-dir`), per-call `-c` overrides for hooks, fsmonitor, sshCommand and gpg.ssh.program, minimal env, `GIT_CONFIG_NOSYSTEM` and a bridge-owned `GIT_CONFIG_GLOBAL`. Section 8: execution route described; `safe.directory` claim corrected. Section 11: Part A step 8. Residual risk without R02/R15 stated |
| S-datalad-2 | accepted | Section 7: host-native ceremony builds and displays the signed commit, dedicated key outside the general agent, one signature per ceremony. Section 11: Part A step 9. Section 14 q7 answered |
| S-datalad-3 | accepted | Section 7: allowed-signers file in the bridge-only location, SHA-256 pinned at start, promotion refused on change. Section 11: Part A step 10 |
| S-datalad-4 | agreed (no objection) | none; isolation score 1 confirmed under the clarified anchor (section 13) |
| A-datalad-1 | accepted | Markers corrected to `run.py:1144-1154` in sections 2, 5 and 6 (re-read with `sed -n 1142,1155p`). All other inherited ranges re-checked; two more drifts fixed: explicit save `1178-1195` -> `1178-1196`, dirty-committed guard `1197-1225` -> `1198-1229`. `GitRepo.commit` range widened to `1444-1566` (method end found with awk); sidecar parse `765-776` -> `764-775`. Header corrected |
| A-datalad-2 | accepted | Section 8: sidecar-id path read without containment (`rerun.py:764-775`), read-only surface; no decision change |
| X-1 | accepted | Covered by S-datalad-1 and S-datalad-3 (section 7); first PR takes the location as a parameter and refuses paths inside the memory root (section 12) |
| X-2 | partly accepted | Section 8: attacker model stated. Signed approvals still detect forgery by a same-user attacker who cannot use the key, so the ledger is not only good for accidents. Rollback and deletion are not detected locally; that needs the TM-3 split, which is the lead's |
| X-3 | partly accepted | Section 13 already rated the upstream artifact, which is what the clarified anchor (c) requires. An informational isolation score for the proposed layer (1 now, 3 after Part A steps 6-10) has been added. Ranking treatment is the lead's decision |
| X-4 | accepted | Covered by S-datalad-2 (section 7, Part A step 9); depends on the shared approval-UI design the lead owns |

Counts: 7 accepted, 2 partly accepted, 0 disputed, 1 agreed with no objection. The DAO skeptic raised no objection against this dossier (`dao-skeptic.md:148-150`), and no C-pattern names it. No score changed; the weighted total stays 2.72. The reuse decision and hard gates are unchanged; the effort estimate for the small scenario rose to 3-4 weeks (section 10).
