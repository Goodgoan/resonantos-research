# Dossier: Eclipse Biscuit (eclipse-biscuit-biscuit-rust + eclipse-biscuit-biscuit-wasm)

STATUS: COMPLETE (amended after review, 2026-10-21)

verified: biscuit-rust 93832a8, biscuit-wasm 80cceed, Alpha 578fbbc, 2026-10-21 (amender re-read the cited paths from the git objects at these SHAs).

Inspector: s3-insp-biscuit, Claude (Fable 5.1). Date: 2026-10-20. Amended 2026-10-21 by s3-amend-biscuit (Claude Opus 5.5), standing in for the original inspector, against the three adversarial reviews (responses in section 14). Clones (read-only, `git clone --depth 200`):
- `research/_untrusted/eclipse-biscuit/biscuit-rust/` at commit `93832a82bf509ad81f05fdb6adaf69d03c56887b` (branch `main`, 2026-10-08). Release tag `biscuit-auth-6.0.0` = `0f0b4e0` (2025-07-15); HEAD is 61 commits past it.
- `research/_untrusted/eclipse-biscuit/biscuit-wasm/` at commit `80cceedb95019cb8932b9e2b7d7eae199646e168` (branch `main`, 2026-07-13).
- The npm tarball `@biscuit-auth/biscuit-wasm@0.6.0` was downloaded as data to the inspector scratchpad and unpacked for file inspection only. Nothing was installed or run.

Execution: none. This was static inspection only. No build, test, install script or binary from either repository was run.

Evidence labels: [inspected] (read the code or test), [reported] (README, docs, issue text, release notes), [hypothesis]. Nothing in this dossier is [executed]. Repository instruction files (CONTRIBUTING.md, release-checklist.md) were read as evidence only. Line citations are at the SHAs above unless marked `@6.0.0`.

## 1. Identification

| Item | biscuit-rust | biscuit-wasm |
|---|---|---|
| Role | Reference library (token format, Datalog authorizer, crypto) | wasm-bindgen wrapper for Node and browsers |
| Canonical source | github.com/eclipse-biscuit/biscuit-rust (moved from the biscuit-auth org; `biscuit-auth/Cargo.toml:10-11` still names `github.com/biscuit-auth/...`) | github.com/eclipse-biscuit/biscuit-wasm |
| Spec | github.com/eclipse-biscuit/biscuit `SPECIFICATIONS.md` (v3.3, fetched 2026-10-20) | same |
| Organisation | Eclipse Foundation project (SECURITY.md); originated at Clever Cloud | same |
| Package | crates.io `biscuit-auth` 6.0.0 (2025-07-16); workspace also has `biscuit-parser` 0.2.0, `biscuit-quote` 0.3.0, `biscuit-capi` | npm `@biscuit-auth/biscuit-wasm` 0.6.0 (2025-09-26), ESM only, `engines.node >=22.0.0`, no npm runtime dependencies |
| Version at HEAD | `Cargo.toml` says 6.0.0, but `biscuit-auth/CHANGELOG.md:1-27` opens with an unreleased `7.0.0` that has breaking changes (KeyPair removed, generic key types) | 0.6.0, pinned to `biscuit-auth = "6.0.0"` from crates.io (`Cargo.toml:14`, `Cargo.lock:39-40`) |
| Licence file | No root LICENSE. Each crate has a 202-line Apache-2.0 text: `biscuit-auth/LICENSE`, `biscuit-capi/LICENSE`, `biscuit-parser/LICENSE`, `biscuit-quote/LICENSE`. Manifest `license = "Apache-2.0"` (`biscuit-auth/Cargo.toml:8`). Root README cites a `LICENSE-APACHE` file that does not exist. No NOTICE file. | Root `LICENSE` is Apache-2.0 (202 lines). The manifest and npm `license` field agree. No NOTICE file. |
| Docs language | English. Maintainers are French; they work in English (Stage 2 lang-fr row) | English |
| DOI / paper / audit | None. The spec README asks for "a cryptographic design audit" [reported] | None |

## 2. What works

Public API (biscuit-wasm, which is what a Node 24 bridge would call) [inspected `biscuit-wasm/src/lib.rs`, `src/authorizer.rs`, `src/builder.rs`, typings in the npm tarball `module/biscuit.d.ts`]:
- Mint: `biscuit\`...\`` tagged template, or `BiscuitBuilder.build(privateKey)`. `setRootKeyId`.
- Attenuate offline: `Biscuit.appendBlock(block)` (`lib.rs:48-57`) and `sealToken()` (`lib.rs:69-79`). Third-party attestation: `getThirdPartyRequest()`, `appendThirdPartyBlock()` (`lib.rs:169-192`).
- Verify offline: `Biscuit.fromBase64(data, rootPublicKey)` checks every block signature (`lib.rs:103-112`).
- Authorize: `AuthorizerBuilder.buildAuthenticated(token).authorize()` returns the index of the matching allow policy or throws (`authorizer.rs:50-58, 200-208`). The default time limit is 20 ms (`authorizer.rs:22`). `authorizeWithLimits` and `query` are also exposed.
- Revocation support: `getRevocationIdentifiers()` returns one hex id per block (`lib.rs:143-153`). This is an accessor only.
- Typed: `module/biscuit.d.ts` ships with the package. 14 classes carry wasm-bindgen `free(): void`, so the caller manages memory.

What the tests exercise:

| Feature | biscuit-rust test (file: name) | biscuit-wasm test (`js-tests/index.js`) |
|---|---|---|
| Signature verification and tamper refusal | samples `test002_different_root_key`, `test003_invalid_signature_format`, `test004_random_block`, `test005_invalid_signature`, `test006_reordered_blocks` (all `Err(Format(...))` in `biscuit-auth/samples/samples.json`) | none |
| Attenuation refuses out-of-scope requests | samples `test001_basic` (block-1 check fails → `Unauthorized`), `test012`/`test013` (file2 refused), `test023_execution_scope`, `test025_check_all`; unit tests `src/token/mod.rs` `basic` (782, asserts `Err(Unauthorized)` at 934-935), `folders` (946, `Err(NoMatchingPolicy)` at 1029-1034), `sealed_token` (1103), `check_all` (1547, 1603-1605) | "complete lifecycle" (162-247) appends a block and asserts only that authorization **succeeds** |
| Expiry refused | samples `test009_expired_token`: the block check `time($time), $time <= 2018-12-20` fails against `time(2020-12-21...)` → `Unauthorized` (`samples/README.md:500-575`) | none |
| Block facts cannot forge authority | samples `test007_scoped_rules`, `test008_scoped_checks`, `test019_generating_ambient_from_variables` | none |
| Third-party blocks | samples `test024_third_party`, `test037_secp256r1_third_party`; `third_party_unsafe_deserialize` (`mod.rs:1619`, CVE-2024-41949 regression) | "third-party blocks" (313-368), positive only |
| Revocation refused | **none** | **none** |

`biscuit-wasm/js-tests/index.js` has no negative assertion of any kind: no `t.throws`, no `t.notOk`, no expected failure. The file has **eight** tape tests (`git show 80cceed:js-tests/index.js | grep -c -E '^test\('` returns 8, at lines 24, 36, 87, 113, 131, 162, 249, 313; there is no `t.test`, `.skip` or `.only`). The assertions are 39 `t.equal`, 9 `t.ok`, 3 `t.has` and 1 `t.pass` (`grep -o -E 't\.[a-zA-Z]+\('`), all on success values or string round-trips. A case-insensitive grep for `throws|catch|fail|error|reject` matches only line 188, `throw new Error("Unknown key id: ...")` inside the test's key provider: a provider that throws, not an assertion that a refusal happens [inspected]. (The first version said "seven tests" and "grep returns nothing"; both were wrong, the conclusion was not.)

CI [inspected]:
- `biscuit-rust/.github/workflows/rust.yml` runs `cargo test --features="serde-error,bwk"` on ubuntu-latest. That includes `examples/testcases.rs:2530-2533` `test_samples`, which replays all 38 sample vectors with `--test`. A "Check samples" step regenerates `samples.json` and fails on `git diff`. Further jobs: a C API test job and a tarpaulin coverage job.
- `biscuit-wasm/.github/workflows/ci.yaml` runs clippy and fmt, builds with wasm-pack, then runs `js-tests` and the node and frontend examples on Node 22.x and 24.x, ubuntu-latest only, always with `--experimental-wasm-modules` (`js-tests/package.json` script `test`).
- Neither repository runs CI on Windows or macOS.

Deployment evidence: Apache Pulsar at Clever Cloud is named in the spec README [reported]. No named production user of biscuit-wasm in Node was found.

## 3. Maturity

| | biscuit-rust | biscuit-wasm |
|---|---|---|
| Commits, last 12 months | 46 (2026-03 to 2026-10). Authors: Delafargue 16, Aronson 14, Vandecrème 6, plus 6 others | **1** (`80cceed` add SECURITY.md). The last functional commit is 2025-09-26. |
| Bus factor | About 3 active people | **1** (Clément Delafargue wrote every commit since 2025-06) |
| Releases | 6.0.0 on 2025-07-16. HEAD carries an unreleased 7.0.0 with breaking API changes | 0.6.0 on 2025-09-26. No GitHub releases. Tags stop at `0.6.0-beta.2`. |
| Issue response (sampled) | #315 and #319 closed the same day; #311 in 2 days; #301 in 2 months; #332 in 7 weeks. Five oldest open issues (#26 from 2021, #48, #84, #150, #171) have 0 comments. | Open #45 (2024, WASM import TypeError) and #46 have 0 comments. #41 (`createBlock` null pointer, 2023) has 1 comment. The last closed issue is from 2023. |
| Advisories | GHSA-75rw-34q6-72cr / CVE-2022-31053, critical, signature forgery, affects >=1.0 <2.0. GHSA-p9w4-585h-g3c7 / CVE-2024-41949, low, public key confusion in third-party blocks, affects >=4.0 <5.0. Both are patched in the versions we would use. | None against the package. **Missed by the ledger: its global allocator `wee_alloc` 0.4.5 (`src/lib.rs:21-22`, `Cargo.toml:20`) carries GHSA-rc23-xxgq-x27g "wee_alloc is Unmaintained" (critical label).** |
| SECURITY.md | Eclipse Foundation policy; supported: biscuit-auth 6.0.0 | Eclipse policy; **"Supported versions: 0.4.0"**, which is stale (current is 0.6.0) |
| Audit | None. The spec README asks for one [reported] | None |
| Stars | 253, 29 contributors. This is a small community but an active core; no fitness claim is made from it. | 30 stars, 7 contributors. A thin binding with little scrutiny. |

Operating footprint: pure in-process library. The npm package unpacks to 2.49 MB, mostly `biscuit_bg.wasm`. The Rust dependency set has no network or OS-service crates (`biscuit-auth/Cargo.toml:30-58`: prost, nom, regex, ed25519-dalek, p256, time, serde_json); the WASM lockfile has 113 crates [inspected]. The lockfile carries older crypto than the HEAD library: ed25519-dalek 2.1.1, p256 0.13.2, rand 0.8.5, prost 0.10.4 (`biscuit-wasm/Cargo.lock`), while HEAD biscuit-auth has moved to ed25519-dalek 3 and p256 0.14 [inspected].

Documentation: the spec is thorough. The biscuit-wasm README is 55 lines and still says Node "must be started with `--experimental-wasm-modules`" and that the package "provides both EcmaScript and CommonJS modules". The second claim is false for 0.6.0: the published `package.json` exports only `"import"` with `"type": "module"` [inspected tarball].

## 4. Architecture

Control flow for one request:
1. `Biscuit.fromBase64(b64, rootPk)` deserialises the protobuf and verifies the signature chain: authority block signed by root, each next block signed by the ephemeral key of the previous one (`SPECIFICATIONS.md` "Deserializing the token").
2. `AuthorizerBuilder` adds ambient facts (resource, operation, time) and allow/deny policies, then `.buildAuthenticated(token)` loads the token's blocks into a Datalog world. Origin-tagging means block facts are visible only under trusted scopes (`biscuit-rust/biscuit-auth/src/token/builder/authorizer.rs:325-502`).
3. `.authorize()` runs the engine. Every check in the authorizer and in every block must succeed; then the first matching policy decides. If none matches, the default is deny.

Identity model: Biscuit has no principal or session concept. A principal is a Datalog fact in the authority block, for example `user("1234")` (`js-tests/index.js:168-169`). Only the root-key holder can write authority facts. Appended blocks can add checks and block-scoped facts, but scoping stops those facts from satisfying authority-level rules (samples test007, test008, test019) [inspected].

Revocation model: `SPECIFICATIONS.md` section "Revocation identifiers" (lines 651-656 of the fetched copy) says the authorizer **generates** `revocation_id(<block index>, <bytes>)` facts. The Rust implementation does not do this at either 6.0.0 or HEAD: `authorizer.rs` and the rest of `src/` never generate such a fact. The only revocation code is the accessor `revocation_identifiers()` (`src/token/mod.rs:205-217`; `src/token/unverified.rs:224-228`). The `constraints` unit test (`mod.rs:1039-1100`; `@6.0.0` line 1059) still holds a commented-out expected error `"check if revocation_id($0), $0 not in [...]"` and asserts `res.is_ok()`. That is a vestige of a revocation check that was dropped [inspected]. So revocation is entirely the host's job: read the ids and compare them with a deny set.

Revocation ids are malleable under P-256 (added 2026-10-21, review S-eclipse-biscuit-2). A revocation id is the raw signature bytes of its block (`src/token/mod.rs:209-217`). Ed25519 signatures are checked with `verify_strict` (`src/crypto/ed25519.rs:179`; `@6.0.0:274`), so they cannot be re-encoded. P-256 signatures are parsed with `Signature::from_der` and checked with plain `verify` (`src/crypto/p256.rs:229-244`; `@6.0.0:296-313`). In the crates the binding actually locks (`biscuit-wasm/Cargo.lock`: ecdsa 0.16.9, p256 0.13.2), p256 uses the default `impl VerifyPrimitive<NistP256> for AffinePoint {}` (p256 `src/ecdsa.rs:75` at tag `p256/v0.13.2`), and the generic `ecdsa::hazmat::verify_prehashed` (ecdsa `src/hazmat.rs:270-292` at tag `ecdsa/v0.16.9`) accepts any `s` in `1..n`, with no high-S check; `Signature::from_scalars` (`src/lib.rs:250-259`) only rejects zero. So `(r, n - s)` verifies, and anyone holding the token can produce it without a key [inspected upstream source fetched read-only by `gh api` into the amender scratchpad `ext\`; not executed]. The reach is narrower than the review states:
- biscuit-auth 6.0.0 generates every ephemeral next key as Ed25519 (`src/token/mod.rs@6.0.0:264, 417`). Blocks appended through the library are therefore Ed25519-signed and safe. Only the authority signature, made by the root key, can be P-256, and only if the minter chooses a P-256 root.
- When any key in the chain is not Ed25519, `block_signature_version` (`src/format/mod.rs@6.0.0:552-581`) selects signature version 1, whose payload includes the previous block's signature (`src/crypto/mod.rs@6.0.0:675-695`). A re-encoded authority signature then breaks block 1. So the bypass works on the last block only: in practice, a revoked single-block (unattenuated) token minted under a P-256 root.
- The wasm default `new KeyPair()` is Ed25519 (`js-tests/index.js:60-68`; `src/crypto/mod.rs@6.0.0:38`).

Consequence for the design: `bridge-grants.mjs` mints with an Ed25519 root only, refuses any root key that is not Ed25519, and revokes on a stable `grant_id` authority fact as well as on signature ids (section 7). The finding stays relevant when R15 moves keys into a platform keystore, where P-256 is the native type.

Time: biscuit-wasm never calls `SystemTime::now`. The Rust helper `AuthorizerBuilder::time()` (`builder/authorizer.rs:258-263`) is not exposed in the binding. The host must add `time(${new Date()})` itself. If it forgets, a token check of the form `check if time($t), $t <= X` finds no fact, so the request is refused (fail-closed, per Datalog check semantics in the README) [inspected].

Process model: embedded. WASM runs inside the Node process. The upstream Node example loads it as an ES module (`module/biscuit.js:1` `import * as wasm from "./biscuit_bg.wasm"`). Node 24.5.0 removed the `--experimental-wasm-modules` requirement, per the Node 24 ESM docs history table [reported]. Node 24.0 to 24.4 still need the flag [hypothesis, not run].

Robustness points in the binding [inspected; consequences are hypothesis]:
- `KeyProvider::choose` calls `.unwrap()` on the JS callback result (`lib.rs:323-324`). A provider that throws for an unknown key id, as the test's own provider does at `js-tests/index.js:188`, causes a Rust panic inside WASM rather than a clean error.
- Many methods panic on reuse through `.expect("empty AuthorizerBuilder")`.
- The bridge should use `fromBase64(data, rootPk)` and never `...WithProvider`.

## 5. Direct relevance

R01 (P0), per-principal, expiring, attenuable, revocable grants for the local bridge. Evidence rows:

| Alpha gap | What Biscuit supplies | What stays custom |
|---|---|---|
| OSC-02: 26 static tokens, all requested by one service worker (`browser-first/host/bridge-capability-tokens.mjs:23-50, 62-73`; `bridge-server.mjs:1201-1207`; `resonantos-side-panel-extension/src/lib/bridge-client.js:141, 646-656`) | One signed token format whose authority block lists `right("<capability>")` facts drawn from the existing 26 names | Minting policy (who gets what), key storage |
| OSC-43: no revocation except the OpenCode latch | Per-block revocation ids | **The deny set, its persistence and the per-request check**: all custom |
| OSC-44: no expiry | `check if time($t), $t <= <exp>` in authority or attenuation blocks; refused when past (test009) | Host must inject `time()`; refresh flow in the extension |
| OSC-45: no attenuation, no principal identity in requests | Holder-side `appendBlock` narrowing, demonstrated in Rust tests; principal as a signed authority fact | Principal naming convention |
| OSC-46: no multi-principal isolation | Distinct tokens per principal, each with its own revocation ids | Principal registry |

Seam: os-map section 17 seam 1 (`authorizeBridgeRoute`, `bridge-server.mjs:114-137`).

R07 (supporting), caller attribution through delegation: the authority block, and therefore the originating `principal(...)` fact, survives every attenuation by construction. A delegate can be attested with a third-party block signed by the bridge (test024). The authorizer can `query` the principal for the audit log (`authorizer.rs:218-253` in the binding). The originating principal survives delegation [inspected]; the identity of the delegatee is a convention we would have to define.

Threats: T4 (confused deputy) is closed in design: requests carry a signed principal, and a child gets an attenuated token instead of the whole capability. T3 (token theft) is only shortened: a stolen Biscuit is still a bearer token until it expires or is revoked, because Biscuit has no proof-of-possession [inspected; the spec has no holder-binding mechanism].

Property check (threat-model section 4, Authorization):

| Property | Verdict | Evidence |
|---|---|---|
| Attenuated grant refused | **Demonstrated in biscuit-rust; not demonstrated in biscuit-wasm** | Rust: samples test001, 012, 013, 023, 025, and `mod.rs` `basic`, `folders`, `check_all`, all run in CI by `test_samples` and `cargo test`. WASM: `js-tests/index.js` has no refusal test. The binding runs the same `biscuit-auth` 6.0.0 code (the same tests exist at tag `biscuit-auth-6.0.0`: `mod.rs@6.0.0:747, 908`), so the Rust result carries over [inspected], but nothing tests the JS error path. |
| Revoked grant refused mid-session | **Not demonstrated in either repository.** Stage 2 is confirmed and strengthened. | No test in `biscuit-auth/tests/rights.rs`, `tests/macros.rs`, `src/**` unit tests, the 38 sample vectors, `biscuit-capi/tests/capi.rs` or `js-tests/index.js` refuses a revoked token. The samples record `revocation_ids` per vector (`samples.json`), which tests id derivation, not refusal. The implementation does not generate the spec's `revocation_id` facts at all (section 4), and the ids it exposes are malleable for P-256-signed blocks (section 4; harmless under an Ed25519-only configuration). Under weights.json clause (d) this is absence of a mechanism, not contrary evidence, in the configuration proposed here. What would be needed: host-side tests (section 11, cases d, d2, j, k), including revocation during an open SSE stream. |
| Grants carry principal identity | **Possible, not built in** | Authority facts are signed by root and cannot be forged by appended blocks (test007, test008, test019). The principal convention is ours to define. |
| Verification works offline | **Demonstrated** | `Biscuit::from(bytes, rootPk)` / `fromBase64` needs only the root public key; no network crate in the dependency set; all sample vectors verify from files. |
| Expiry refused | **Demonstrated in Rust (test009); not in WASM** | Expiry is a Datalog time check, not a token field. |

## 6. Reuse decision

**Wrap / adapter.** Take `@biscuit-auth/biscuit-wasm` 0.6.0 as a pinned dependency behind a small bridge module (`bridge-grants.mjs`). That module owns key custody, the principal convention, the revocation deny set and the negative tests that upstream lacks.

Why this beats the alternatives in section 12:
- Biscuit is the only candidate that gives holder-side offline attenuation with an open spec, conformance vectors and a maintained Rust core.
- Cedar has better principal semantics but no delegation by holders.
- aegis has a tested revocation path but no expiry or attenuation, and it is a sidecar proxy.
- Revocation is the one property Biscuit does not supply, and it is also the cheapest to build locally: a `Set` lookup per request inside the same process.

Amended 2026-10-21: the decision is unchanged, but the R01 verdict now depends explicitly on the custom layer (reviews S-1 to S-4, X-3). Four conditions belong to the wrap, not to Biscuit: (1) Ed25519-only root and blocks, with a `grant_id` revocation fact (S-2); (2) the deny set and any persisted root key live in the bridge-only store that R15 defines, never under a child-writable path (S-1, X-1); (3) revocation closes open streams and proxied connections, not only the next request (S-3, X-7); (4) a byte cap on the token before signature verification (S-4). Section 13 scores the upstream artifact (anchor clause (c)); the custom layer has no score until its cases in section 11 pass.

Fallback if the binding's maintenance (bus factor 1, `wee_alloc`) is judged unacceptable: build the WASM ourselves from `biscuit-auth` with the system allocator, pinned in the Resonant repo. That is "vendor a limited component"; it costs a Rust toolchain in CI.

Hard gates (scoring/weights.json):
- G1 (no mandatory cloud or telemetry): **pass**. No network dependency; `wasm_logger` writes to the console only (`lib.rs:337-343`).
- G2 (three OSes or an honest matrix): **pass**. Pure WASM plus pure Rust with no OS calls, so nothing degrades silently. Upstream CI is Linux-only, so Windows and macOS are untested upstream (see the matrix below).
- G3 (licence compatible with MIT): **pass**. Apache-2.0 at file level in every crate and the binding.
- G4: **N/A**. Not a DAO component; chain none.
- G5 (project invariants): **pass, with a condition**. Runtime authority stays local to the bridge. A rule must forbid minting a Biscuit from a DAO credential (I2). Human-only actions are untouched. Amended (D-eclipse-biscuit-1): the condition is enforced and tested, not only stated. `mintGrant` accepts an allowlist of authority predicates only (`principal`, `right`, `grant_id`, and the expiry check); any other predicate, and any input object produced by a credential verifier, is refused. `verifyGrant` refuses a token whose authority block (`getBlockSource(0)`, `biscuit-wasm/src/lib.rs:162-168`) uses a predicate outside that allowlist, so a future `dao_role(...)` fact cannot become an authorization input without changing the allowlist and its test (section 11, case l).

Per-OS matrix [inspected code; nothing executed]:

| OS | Runs | Degrades | Silent | How Node 24 calls it |
|---|---|---|---|---|
| Windows | Yes (WASM, no OS API) | Untested upstream. The 20 ms default authorize timeout (`authorizer.rs:22`) could refuse on slow machines; that is fail-closed but hurts availability [hypothesis] | Nothing | `import {...} from "@biscuit-auth/biscuit-wasm"`. ESM only. No flag needed on Node >= 24.5 [reported]. |
| macOS | Yes | Untested upstream | Nothing | same |
| Linux | Yes | Tested upstream (ubuntu, Node 22 and 24) | Nothing | same |

## 7. Integration design (seam 1)

Principle: keep the route and capability vocabulary unchanged. `route.requiredCapability`, `BRIDGE_CAPABILITY_TOKEN_SPECS`, `BRIDGE_ROUTE_CAPABILITIES` and the `refuse()` error codes stay as they are. Only the value carried in `X-ResonantOS-Bridge-Capability-Token` changes, from a random string to a Biscuit.

New file `browser-first/host/bridge-grants.mjs` (sketch):

```js
// mint: authority block signed by the bridge root key (Ed25519 only)
mintGrant({ principal, capabilities, ttlSeconds })  // -> base64 Biscuit
//   allowlist: principal("ext:<extension-id>"); right("memory-read"); ...;
//   grant_id("<uuid>"); check if time($t), $t <= <now+ttl>;   anything else -> throw
attenuate(tokenB64, { capabilities, ttlSeconds, delegate })  // appendBlock: narrower rights + shorter expiry
verifyGrant(tokenB64, requiredCapability, { now = new Date() })
//   0. refuse if tokenB64.length > MAX_GRANT_B64 (e.g. 4096) before any parsing   (S-4)
//   1. Biscuit.fromBase64(tokenB64, rootPk)        (never ...WithProvider; rootPk is Ed25519)
//   2. refuse if countBlocks() > MAX_BLOCKS, or if getBlockSource(0) uses a predicate
//      outside the mint allowlist (I2, D-1)
//   3. g = query(rule`g($g) <- grant_id($g)`)  (authority scope only)
//      if revoked.has(g) || getRevocationIdentifiers().some(id => revoked.has(id)) -> {ok:false, reason:"revoked"}
//   4. authorizer`time(${now}); capability(${requiredCapability});
//                 allow if right($c), capability($c);`.buildAuthenticated(token).authorize()
//   5. principal = query(rule`p($p) <- principal($p)`); free() every WASM object
revoke(id)      // add to the in-memory Set; append to the bridge-only revocation log (below);
                // then terminate every open connection registered under that grant (below)
```

Revoking the `grant_id` (or the authority-block id) kills the token and every attenuated descendant, because every descendant carries the parent's authority block. Revoking a later block id kills only that delegate; those ids are Ed25519 signatures made by library-generated keys and cannot be re-encoded (section 4). The authority-block signature id is kept only as a second key: under a P-256 root it would be malleable, which is why the root is pinned to Ed25519 and `grant_id` is the primary revocation key.

Mid-session revocation (amended, S-eclipse-biscuit-3). The per-request check covers short requests only. The Alpha bridge also serves Server-Sent Event streams (`writeBridgeEventStream`, `browser-first/host/bridge-server.mjs:360-401`, `Content-Type: text/event-stream` at 391 and 401) and proxies OpenCode, so a stream authorized before a revoke would keep flowing. `verifyGrant` therefore registers each long-lived response under its `grant_id` and block ids in a `Map<id, Set<terminate>>`. `revoke(id)` calls each registered terminator. The stream writer already has a `terminate(code)` closure, handed to the subscription through `attachTransport({..., terminate, closed})` (`bridge-server.mjs:375-399`). Registering that closure is the whole hook, and the bound is one event-loop turn plus the writer's 1 s destroy timer (`bridge-server.mjs:386`). Case d2 in section 11 tests it.

Where the security state lives (amended, S-eclipse-biscuit-1, X-1). The first version put the deny set under `~/ResonantOS_User/bridge-revocations.json`. That path is reachable by the adversary it is meant to stop: the Alpha's read-deny roots protect only `ResonantOS_User/Secrets` (`browser-first/host/delegation-isolation.mjs:175-209`, `readDenyRootsFor`), delegated children are unconfined on Linux and Windows (OSC-32), and `archive-write` holders write into the user state root through the bridge (OSC-45). A child could delete its own line and be un-revoked at the next restart. Corrected design: the revocation log and any persisted root key go in the bridge-only store that R15 defines (lead decision, X-1), outside every path a child, an add-on or an `archive-write` route can reach. The log is append-only, and each record carries a MAC under a key that only the bridge process holds. On start the bridge refuses to serve grants if the MAC chain fails. Detecting a rollback of the whole log (T6) needs a counter kept outside that store, for example in the OS keystore item that holds the MAC key; this is open with the lead's TM-1. Until R15 exists, the default is the per-run root key in memory: restart invalidates every grant, so there is no persisted deny set to tamper with.

Alpha changes:
- `browser-first/host/bridge-server.mjs:1201-1207` `isAuthorizedCapabilityRequest`: call `verifyGrant` when grants mode is on. Otherwise keep the constant-time compare. Dual mode lets the extension migrate gradually.
- `bridge-server.mjs:1214-1236` `scopedCapabilityTokenPayload`: return a map from capability to Biscuit, one per capability or one shared. The shape is unchanged, so `bridge-client.js:646-656` (`Object.assign(_capabilityTokens, payload.capabilityTokens)`) keeps working.
- `bridge-server.mjs:114-137` `authorizeBridgeRoute`: return `{route, principal}` so services and an audit log (R11) can attribute the caller (R07).
- `browser-first/host/run-bridge-minimal.mjs` (`:426-488` per OSC-02): create an Ed25519 root key at start and keep the private key in memory per run (restart invalidates all grants, matching today's behaviour). Amended (S-1): the first version also offered "store it 0600 under `ResonantOS_User`"; that option is withdrawn, because the user state root is child-reachable and 0600 is meaningless on Windows (OSC-06). Persisting the root key waits for the R15 bridge-only store.
- `bridge-server.mjs:360-401` `writeBridgeEventStream`: register the existing `terminate` closure under the request's grant ids so `revoke()` closes the stream (S-3).
- `bridge-client.js`: on a 403 caused by expiry, re-request through the bootstrap route. This is new code; today tokens never expire.
- Delegation to Hermes, OpenCode or DSH (R02/R03 territory): the bridge hands the child `attenuate(token, {capabilities:["provider-model-invoke"], ttlSeconds:900, delegate:"hermes"})` instead of any static token.

Error behaviour: reuse the existing `OPENCODE_CAPABILITY_REQUIRED` 403, because the harness error vocabulary is locked by tests. Put the reason (expired, revoked, attenuated) in the server log only. Any WASM exception maps to 403, never 500.

Tests affected among the 2,424 browser-first tests: 15 `*.test.mjs` files of 206 in `browser-first/test/` reference capability tokens [inspected grep]:
- Must change or extend: `bridge-capability-token-consistency.test.mjs` ("buildBridgeCapabilityTokens mints a token for every capability", "honors arg > env > mint precedence", "requires a mint function"). The arg/env pinning contract (`bridge-capability-tokens.mjs:20-21`) means nothing for signed expiring grants and needs a decision: keep it as a legacy mode or retire it.
- Should pass unchanged in dual mode: `bridge-server.test.mjs` (108, 561, 708), `bridge-auth-inprocess-self-test.test.mjs` (11, 60), `bridge-get-routes-require-capability.test.mjs` (153), `bridge-first-run-smoke.test.mjs` (26-82), `harness-host-service.test.mjs`, `opencode-execution-revocation.test.mjs`, `opencode-governed-panel.test.mjs`, `opencode-proxy-transport.test.mjs`, `bridge-tls.test.mjs`, `bridge-target-section.test.mjs`, `agent-control-live-report.test.mjs`, `dsh-native-browser-contract.test.mjs`, `dsh-native-integration.test.mjs`.
- Must stay green untouched, because this is the vocabulary lock: `bridge-route-capability-audit.test.mjs` (5 tests at 177-240).

Versioning: pin `@biscuit-auth/biscuit-wasm` exactly at `0.6.0`. Upstream HEAD is heading to biscuit-auth 7.0.0 with breaking API changes, so a future binding release will need a review before bumping. The token format version (block version 3, `samples/README.md`) is the stable contract.

## 8. Security and governance effects

- New privilege: a root signing key in the bridge. Whoever reads it mints any grant. Store it in memory per run, or in an OS keychain later (R15).
- Attack surface added: a WASM Datalog engine that parses attacker-supplied tokens on every request. Mitigations: authorize time limits (default 20 ms in the binding), size cap on the header, `fromBase64` with a fixed root key. Amended (S-eclipse-biscuit-4): the 20 ms limit bounds Datalog evaluation only. Protobuf decoding and one signature verification per block happen inside `fromBase64` before any limit applies, and biscuit-auth 6.0.0 has no block-count cap of its own (`git grep -n -i -E "max_blocks|MAX_BLOCK|too many blocks|blocks\.len\(\) >|max_size" 0f0b4e0 -- biscuit-auth/src` returns nothing) [inspected]. Any web page can send no-cors requests to the bridge (OSC-05), so a page could make the bridge verify many-block tokens at its own pace. The binding has no unverified parse, so a block count is available only after verification (`countBlocks`, `src/lib.rs:156-160`). The cap therefore has to be a byte length on the header value, checked before `fromBase64` (for example 4 KiB, which bounds the block count), plus a per-origin rate limit on refused tokens. Verify cost per block is measured in case h [hypothesis until run]. Known panic paths are `KeyProvider` `.unwrap()` (`lib.rs:323-324`) and the `.expect` calls; avoid the provider API. A panic leaves the WASM instance in an undefined state, so wrap calls and restart the module on a trap [hypothesis].
- Memory: wasm-bindgen objects need `free()` (14 classes in `biscuit.d.ts`), and the allocator is the unmaintained `wee_alloc`. A long-running bridge verifying every request could leak or fragment memory [hypothesis; needs the soak test in section 11].
- Revocation story: entirely ours (section 7). It is synchronous and in-process, so there is no propagation delay. That beats ADC's 150 s window (Stage 2 row), but our persistence must survive restart and rollback (T6 requirement "revocation survives rollback"). Amended: the deny set must not sit in the child-writable user state root (S-1). Revocation must also close open streams (S-3), and it keys on `grant_id` under an Ed25519-only root, because P-256 signature ids are malleable (S-2). All three are in section 7.
- Bearer nature: T3 theft of a token from `chrome.storage.local` still works until expiry or revocation. Short TTLs (minutes) plus refresh are the only mitigation. Biscuit has no holder binding.
- Personal data: tokens carry principal names and capability names in clear; they are signed, not encrypted. They stay on the loopback.
- Trust in maintainers: the Rust core is credible, with an Eclipse Foundation disclosure process and patched CVEs including a regression test for CVE-2024-41949. The binding is one person and has a stale SECURITY.md. There is no audit.
- User friction: none visible; tokens are minted and refreshed by the bridge and the extension.

## 9. Licensing

- SPDX: Apache-2.0 for `biscuit-auth`, `biscuit-parser`, `biscuit-quote`, `biscuit-capi` (per-crate LICENSE files) and `biscuit-wasm` (root LICENSE). SPDX headers in sources match (for example `rights.rs:1-4`, `lib.rs:1-5`).
- Discrepancy: the biscuit-rust root has no licence file, and the README links a non-existent `LICENSE-APACHE`. That is cosmetic: the crate we consume carries its own licence file (see the counterexample answers in section 14).
- Obligations: Apache-2.0 section 4 (keep the licence text and state changes). No NOTICE file exists, so there is no NOTICE propagation duty. The patent grant is a benefit.
- Transitive: 113 crates are compiled into `biscuit_bg.wasm`. Their licences were not scanned. A `cargo deny` or `cargo about` run over `biscuit-wasm/Cargo.lock` is needed before shipping, because the npm tarball carries only Biscuit's own LICENSE.
- Compatibility: high confidence with the MIT Alpha. Unknown for the proposed Symbiotic Licence (status F).
- For legal review: (a) the 113-crate transitive set embedded in one binary; (b) whether redistributing the WASM inside a Chrome extension (not proposed here) changes notice duties. This is technical research, not legal advice.

## 10. Cost and effort

- Small, about 4-6 days (was 3-5 before review): the bridge-grants module, dual-mode `isAuthorizedCapabilityRequest`, revocation set keyed on `grant_id`, stream termination on revoke, byte cap, predicate allowlist, and about 14 new tests. Assumes one principal (the extension) and per-run root keys in memory.
- Medium, about 2-3 weeks: per-principal tokens for add-ons and children, delegation through attenuation, expiry refresh in `bridge-client.js`, persisted revocation, audit attribution (R07/R11 link).
- Large, more than 4 weeks: self-built WASM with the system allocator, a three-OS CI lane, migration of the arg/env pinning contract, retiring the legacy static tokens.

Skills: Datalog policies (new to the team), ESM/WASM in Node. Rust is needed only for the vendored-build fallback. Lock-in is low: Biscuit is an open spec with several implementations [reported], and the grant module isolates it, so replacing it means rewriting `bridge-grants.mjs`, not the routes. Language cost: the team writes JS; Datalog policy strings are short and testable.

## 11. Acceptance test (a request for the user: it executes third-party WASM)

Setup: a scratch directory outside `research/`, Node 24.x (one run on 24.4 to observe the flag requirement, one on >= 24.5), `npm install --ignore-scripts @biscuit-auth/biscuit-wasm@0.6.0`, and a harness script of ours that imports it. Run on Windows, macOS and Linux.

| Case | Input | Expected |
|---|---|---|
| a | Grant `principal("ext"), right("memory-read")`, TTL 60 s, request `memory-read` | allow (0) |
| b | The same token, request `archive-write` | refused |
| c | Attenuate (a) with `check if capability($c), ["memory-read"].contains($c)` and use it from a "child" | allow memory-read, refuse any other |
| d (T4/T3 fault, mid-session) | A loop issues a request every 100 ms with token (c). At t=1 s, `revoke(authority id of (a))` | the first request after revoke is refused. Both (a) and (c) are refused from then on; no request after revoke succeeds. |
| e | Token with TTL 1 s, used at 2 s with `time(now)` injected; and the same request with no time fact | refused in both |
| f | Strip the last block, reorder blocks, flip one byte | `fromBase64` throws, mapped to 403 |
| g | `fromBase64WithProvider` with a provider that throws | document whether the instance traps (expected: panic). Confirms the "never use provider" rule. |
| d2 (S-3, mid-stream) | Open an SSE route (`writeBridgeEventStream`) and a proxied OpenCode connection with token (c); revoke the authority grant while both are open | both connections are closed within 1.5 s (one event-loop turn plus the writer's 1 s destroy timer); no event is delivered after the revoke returns |
| h (soak) | 1M authorize calls with `free()`, then without; also `fromBase64` cost for tokens of 1, 10 and 50 blocks | heap growth recorded; pass if bounded with `free()`; verify time per block recorded for the S-4 cap |
| i | principal query on (c) | returns `"ext"` (originating principal survives delegation, R07) |
| j (S-1) | A child holding `archive-write` tries to truncate, rewrite or delete the revocation log and its MAC; restart the bridge | the revoked grant is still refused after restart, or the bridge refuses to serve grants (MAC failure); it never silently un-revokes |
| k (S-2) | Mint a single-block token under a **P-256** root, revoke its signature id, re-encode the authority signature as `(r, n-s)` | documents the bypass on signature ids (expected: the re-encoded token verifies and has a new id); with `grant_id` revocation it is still refused; under the Ed25519-only rule `mintGrant` refuses the P-256 root and `verifyGrant` refuses the token |
| l (D-1, I2) | `mintGrant` called with a fact `dao_role("reviewer")` or with an object produced by a credential verifier; a token minted outside `mintGrant` whose authority block carries `dao_role(...)` | `mintGrant` throws; `verifyGrant` refuses the token (403) |
| m (S-4) | Header value of 64 KiB, and a 200-block token | refused before `fromBase64` is called (byte cap) |

Pass/fail: cases a-g, i and j-m are exact; d2 is exact within its bound. Case h passes if RSS growth is under 50 MB after 1M calls with `free()` (threshold to be agreed). CI hook: once approved, the same cases become `browser-first/test/bridge-grants.test.mjs` in the Alpha's browser-first lane.

## 12. Recommendation and confidence

Benefits: offline-verifiable, attenuable, expiring grants without a server; an open spec with 38 conformance vectors; principal attribution that survives delegation; Apache-2.0; in-process, so no new service.

Trade-offs and blockers:
1. Revocation is not provided and not tested anywhere upstream; we build and test it.
2. The WASM binding has no negative tests, a bus factor of 1, an unmaintained allocator, a stale SECURITY.md, and a README with two stale claims (Node flag, CommonJS).
3. It remains a bearer token (T3).
4. Upstream is moving to a breaking 7.0.0.
5. (Added after review.) The R01 verdict rests on the custom layer: the Ed25519-only rule plus `grant_id` revocation (P-256 signature ids are malleable in the pinned crates, section 4); the bridge-only store for the deny set (S-1); stream termination on revoke (S-3); and the pre-parse byte cap (S-4). Section 13 scores the upstream artifact only (anchor clause (c)); the custom layer is unscored and counts as design only until cases d, d2 and j-m pass.

Readiness: ready for a flag-guarded prototype; not ready as a default until cases a-m (including d2) pass on all three OSes.

Evidence quality: the property findings are [inspected] (code, tests, sample vectors, npm tarball). Production use, the Node 24.5 flag change and the Cedar and audit statements are [reported]. Nothing was executed.

Competing solutions, on the same criteria:

| Criterion | Biscuit (this dossier) | Cedar (cedar-policy/cedar, cedar-wasm 4.14.0, npm 2026-10-19) | getaegis/aegis (`f1321b3`, 2026-08-06) |
|---|---|---|---|
| Model | Signed bearer token + Datalog | Policy engine over a host-side entity and policy store; no token | Per-agent opaque token (`aegis_{uuid}_{hmac}`, SHA-256 stored, `src/agent/agent.ts:34-85`) + grant table in SQLite |
| Attenuation by holder | Yes, offline, tested in Rust | No (the host rewrites policies) [reported] | No |
| Expiry | Datalog time check; Rust test009 | Via a `context` time attribute in `when` clauses [reported] | **None** found (`agent.ts` has no expire or ttl) [inspected] |
| Revocation refused mid-session | **Not provided, not tested** | Immediate when the host deletes a policy or entity; no test inspected | **Tested end-to-end**: `tests/gate-agent.test.ts:306-331` (200, then revoke, then 403); unit tests `tests/agent.test.ts:255-307` [inspected] |
| Principal identity | Convention (authority fact) | First-class `principal` in every request | First-class agent row |
| Offline verification | Yes (public key only) | Yes (in-process evaluation), but no portable credential | Lookup in a local DB; nothing portable |
| Node 24 embedding | ESM WASM, in-process | WASM, CJS `@cedar-policy/cedar-wasm/nodejs` and ESM [reported README] | **Sidecar** HTTP proxy CLI; native dependency `better-sqlite3-multiple-ciphers` |
| Maturity | Rust core active; binding thin | Large, active (pushed 2026-10-20, 1,797 stars), no GHSA advisories found; formal-methods claims [reported] | 7 months old, 14 stars, single organisation |
| Licence | Apache-2.0 | Apache-2.0 | Apache-2.0 |
| Fit for seam 1 | Best fit for attenuation and delegation (OSC-45/46) | Best fit for principal policy; would still need a bearer secret per principal and a grant store | Best evidence for revocation; wrong shape (an egress credential proxy, which suits R03 more than R01) |

Conclusion: Biscuit for the grant format. Copy aegis's revocation test shape (200, then revoke, then 403 on the same session) as our case d. Cedar is the alternative if the team prefers central policy over delegable tokens.

First PR (ResonantOS Alpha, browser-first). Title: "bridge: Biscuit-backed capability grants behind RESONANTOS_BRIDGE_GRANTS=biscuit (default off)". Changes:
- add `browser-first/host/bridge-grants.mjs` (mint with the predicate allowlist, verify with the byte cap, revoke on `grant_id`, in-memory revocation set, registry of open streams per grant);
- in `browser-first/host/bridge-server.mjs`, branch `isAuthorizedCapabilityRequest` (1201-1207) and `scopedCapabilityTokenPayload` (1214-1236) on the flag, and register the `terminate` closure of `writeBridgeEventStream` (360-401) under the grant;
- in `browser-first/host/run-bridge-minimal.mjs`, create a per-run Ed25519 root key in memory when the flag is on (nothing persisted until R15 provides the bridge-only store);
- add `browser-first/test/bridge-grants.test.mjs` covering cases a-f, d2, i, k (Ed25519 refusal half), l and m; case j waits for the R15 store;
- pin `@biscuit-auth/biscuit-wasm@0.6.0` exactly in the root `package.json`.

No change to `BRIDGE_CAPABILITY_TOKEN_SPECS` or the route tables.

Confidence: **medium**. The code-level findings are firm. Medium rather than high because nothing was executed: Node 24 loading without the flag, Windows behaviour, memory under `wee_alloc` and panic recovery are all unverified.

## 13. Scores (profile: os_kernel)

| Criterion | Score | Reason (anchor) |
|---|---|---|
| requirement_fit | 3 | Attenuation, expiry, offline verify and a signed principal are present; mid-session revocation is absent and must be built. |
| demonstrated_maturity | 3 | Releases, CI, a 38-vector conformance suite and a reported production user for the core; the Node binding has thin usage evidence and only positive tests. |
| isolation_and_security | 3 -> **2** | Re-scored 2026-10-21 under the clarified anchor (clauses (a)-(d)), rating the upstream artifact `@biscuit-auth/biscuit-wasm` 0.6.0 (embedding biscuit-auth 6.0.0) as inspected. Attenuation and expiry refusal are tested by tests of the property itself (sample vectors test001, 012, 013, 023, 025, 009 and `mod.rs` `basic`, `folders`, `check_all`, the same code at `@6.0.0`), which meets clause (b) for those two. Revocation, the property R01 exists to add (OSC-43), has no mechanism upstream: an accessor only, no spec-required `revocation_id` facts, and ids that can be re-encoded under P-256 (section 4). Clause (d) caps that property at 1. The P-256 path is not contrary evidence (score 0), because the configuration proposed here is Ed25519-only and there the path is not reached. The artifact's own JS path has no refusal test. The family therefore sits between "designed and partly tested" (3) and "docs only" (1). |
| licence_suitability | 5 | Apache-2.0 licence files in every crate and in the binding. |
| integration_effort | 4 | Embeddable npm library with `.d.ts` types, in-process; ESM-only, flag on Node < 24.5, plus a custom revocation layer. |
| maintenance_sustainability | 2 | Rust core about 3 active maintainers; the binding we would depend on has bus factor 1, 1 commit in 12 months, a stale SECURITY.md and an unmaintained allocator. |
| sovereignty_and_portability | 5 | Local-first, no account, readable Datalog. |
| interoperability | 4 | Open spec with conformance samples and several language implementations [reported]; not an IETF or W3C standard. |
| operational_complexity | 5 | One process, no external service. |

Weighted total (os_kernel, weights from `scoring/weights.json` profile `os_kernel`): 0.18x3 + 0.14x3 + 0.22x2 + 0.10x5 + 0.08x4 + 0.10x2 + 0.08x5 + 0.04x4 + 0.06x5 = 0.54 + 0.42 + 0.44 + 0.50 + 0.32 + 0.20 + 0.40 + 0.16 + 0.30 = **3.28** (was 3.50; the only change is isolation_and_security 3 -> 2, -0.22).

## 14. Open questions for the adversarial reviewers

Counterexample rows answered:
1. **s2-br-b against biscuit-rust** (GHSA-75rw-34q6-72cr, five points).
   - (1) CVEs: **confirmed, not a blocker.** CVE-2022-31053 affects <2.0, CVE-2024-41949 affects >=4.0 <5.0, and both are patched before the 6.0.0 we would use. A regression test exists (`mod.rs:1619` `third_party_unsafe_deserialize`).
   - (2) Revocation is only an identifier scheme: **confirmed and strengthened.** The implementation does not even generate the spec's `revocation_id` facts (section 4).
   - (3) WASM build plus a Node flag: **partly refuted.** The WASM is prebuilt in the npm package, and Node >= 24.5 needs no flag [reported]. The ESM-only packaging is confirmed, and the README's CommonJS claim is refuted.
   - (4) No principal concept: **confirmed**, mitigated by signed authority facts.
   - (5) No Rust revocation test: **confirmed** across `tests/rights.rs`, `tests/macros.rs`, every `src/` unit test, the 38 samples and `biscuit-capi/tests/capi.rs`.
2. **s2-br-h against biscuit-rust** (no root LICENSE): **confirmed as a fact, refuted as a licence risk.** `biscuit-auth/LICENSE` and the three sibling crates each hold the full Apache-2.0 text. `tests/rights.rs` is not a test either: it is a `fn main()` that ends in `panic!()`.
3. **s2-br-h against biscuit-wasm** (no test directory, Node flag):
   - The "no test directory" heuristic is **refuted**: `js-tests/index.js` exists and runs in CI.
   - The substance is **confirmed and worse**: it has zero negative assertions.
   - The flag is addressed under 1(3).
4. **s2-lang-fr against biscuit-wasm** (no audit, external revocation): **confirmed** on both points. The spec README still asks for an audit, and revocation needs external state.

Additional disconfirmation found: the `wee_alloc` unmaintained advisory (GHSA-rc23-xxgq-x27g) on the binding's allocator; a stale SECURITY.md ("supported 0.4.0"); panic paths in `KeyProvider`; unreleased breaking 7.0.0 at HEAD; Linux-only upstream CI.

Not established:
- Whether Node 24.0-24.4 actually fails without the flag, and whether >= 24.5 loads the package unflagged. This needs the run in section 11.
- Memory behaviour of `wee_alloc` in a long-running bridge.
- Whether a WASM panic poisons the instance for later calls.
- The licences of the 113 transitive crates.
- Cedar's test coverage of policy removal, and its formal-verification claims. Only the repository listing and README were read.
- Whether the spec's `revocation_id` fact generation exists in other implementations (Java, Go, Python). If it does, the Rust deviation matters for interoperability with other implementations.

Where the maintainers' description may be optimistic:
- The biscuit-wasm README's CommonJS and Node-flag statements.
- "Revocation: ... requires external state management" undersells the gap: the spec describes authorizer-generated revocation facts that this implementation does not produce.
- The `revocation_identifiers()` doc comment, "revocation identifiers are unique" (`src/token/mod.rs:206-208`), holds between separately minted tokens. It does not hold for one token under P-256, where a holder can produce a second valid id (section 4).

### Counts and how they were recounted (2026-10-21)

Every count below was re-run by the amender at the recorded SHAs from git objects (`git -c core.hooksPath=/dev/null -C <clone> show|ls-tree|grep <sha> ...`), nothing from the working tree:

| Count | Result | Method |
|---|---|---|
| biscuit-wasm JS tests | **8** (was 7) | `git show 80cceed:js-tests/index.js \| grep -c -E '^test\('`; no `t.test`, `.skip` or `.only` |
| biscuit-wasm assertions | 39 `t.equal`, 9 `t.ok`, 3 `t.has`, 1 `t.pass`, 0 `t.throws`/`t.notOk` | `grep -o -E 't\.[a-zA-Z]+\(' \| sort \| uniq -c` |
| Sample vectors | 38 | `git ls-tree --name-only 93832a8 biscuit-auth/samples/ \| grep -c -E 'test[0-9]+.*\.bc$'` = 38; `len(testcases)` in `samples.json` = 38 (`python -I`) |
| Crates in the WASM lockfile | 113 | `git show 80cceed:Cargo.lock \| grep -c '^name = '` |
| Classes with `free(): void` | 14 | `grep -c 'free(): void' module/biscuit.d.ts` in the original inspector's unpacked tarball (14 `export class` lines) |
| Alpha test files touching capability tokens | 15 of 206 | `git ls-tree --name-only HEAD browser-first/test/ \| grep -c '\.test\.mjs$'` = 206; `git grep -l -i -E 'capability.?token\|capabilityTokens\|X-ResonantOS-Bridge-Capability-Token' HEAD -- 'browser-first/test/*.test.mjs'` = 15, at Alpha 578fbbc |

### Review responses (2026-10-21)

Answered by s3-amend-biscuit against the clones at the recorded SHAs, plus the upstream ecdsa 0.16.9 and p256 0.13.2 sources fetched read-only with `gh api`. Nothing was executed.

| Id | Verdict | Change made (section) or evidence for dispute |
|---|---|---|
| S-eclipse-biscuit-1 | accepted | Confirmed: `readDenyRootsFor` protects only `ResonantOS_User/Secrets` (`delegation-isolation.mjs:175-209` at Alpha 578fbbc). Deny set and any persisted root key moved to the R15 bridge-only store, as an append-only, MAC'd log; the "0600 under `ResonantOS_User`" option is withdrawn; the default is a per-run in-memory key; case j added (sections 6, 7, 8, 11). |
| S-eclipse-biscuit-2 | partly accepted | Malleability **confirmed** in the pinned crates: p256 0.13.2 `src/ecdsa.rs:75` uses the default `VerifyPrimitive`; ecdsa 0.16.9 `hazmat.rs:270-292` has no high-S check. **Narrower than stated**: library-generated next keys are Ed25519 (`token/mod.rs@6.0.0:264, 417`), and signature v1 binds each block to the previous signature (`format/mod.rs@6.0.0:552-581`, `crypto/mod.rs@6.0.0:675-695`), so only the last block, in practice the authority id of a single-block token under a P-256 root, can be re-encoded. Ed25519-only rule, `grant_id` revocation and case k added (sections 4, 5, 7, 11). |
| S-eclipse-biscuit-3 | accepted | Confirmed SSE at `bridge-server.mjs:391, 401`. A registry of open connections per grant reuses the writer's existing `terminate` closure (`:375-399`); bound stated; case d2 added (sections 7, 11, 12). |
| S-eclipse-biscuit-4 | accepted | No block cap in biscuit-auth 6.0.0 (git grep, section 8). The binding has no unverified parse, so the cap is a pre-parse byte length plus a per-origin rate limit; case m added, and case h measures cost per block (sections 7, 8, 11). |
| S-eclipse-biscuit-5 | partly accepted | The basis is disputed: anchor clause (c) (D3.7) rates the upstream artifact, not the integration. The score still moves 3 -> 2 on upstream grounds: revocation has no mechanism (clause (d) caps it at 1), the upstream ids are malleable under P-256, and the JS path has no refusal test. Section 12 now states that the R01 verdict depends on the custom layer (sections 12, 13). |
| X-1 | accepted | Same fix as S-1 (section 7). The shared bridge-only location is the lead's decision. |
| X-3 | accepted as settled by the lead | Anchor clause (c) settles it: section 13 rates the upstream artifact. Sections 6 and 12 now say the custom layer is unscored and design-only until its cases pass. |
| X-7 | accepted | Same fix as S-3 (sections 7, 11). |
| X-9 | partly accepted | As S-2. The key-resolution rule is stated: the root is the bridge's own Ed25519 key, passed to `fromBase64`, and `...WithProvider` is never used (section 7). |
| A-eclipse-biscuit-1 | accepted | `Cargo.toml:15` -> `:14` (section 1). |
| A-eclipse-biscuit-2 | accepted | Recounted: 8 tests, with the method given; the grep sentence corrected (line 188 is a throwing provider, not an assertion). The conclusion, no refusal assertion, stands (section 2; counts table above). |
| A-cc-1 (citation drift) | accepted | The one drifted biscuit citation is fixed (A-1). All new citations were read from git objects at the recorded SHAs. |
| A-cc-3 (counts without command) | accepted | Every count now has its command (table above). All other counts reproduce: 38, 113, 14, 15 of 206. |
| A-cc-5 (vacuous tests well reported) | accepted, no change | The archaeologist confirms that the lack of negative tests in biscuit-wasm was disclosed. |
| A-cc-6 (STATUS line) | accepted | `STATUS: COMPLETE (amended after review, 2026-10-21)` and a `verified:` stamp added (header). |
| D-eclipse-biscuit-1 | accepted | I2 is now enforced and tested: a mint-time predicate allowlist, a verify-time check of the authority block, and case l (sections 6, 7, 11). |
| C-8 | accepted | As A-cc-6 (header). |
| Lead ruling 1 (D3.8, clause (d) scope) | settled | The absence cap applies only to the missing property (revocation) and does not cap the family where other checked properties are demonstrated; isolation 2 and the total of 3.28 stand. |
| Lead ruling 2 (D3.8, forbidden configuration) | settled | The P-256 malleability is not contrary evidence: clause (d) judges the artifact as the dossier proposes to use and configure it, which is Ed25519-only. |
| C-1 | lead's; no score change | The R01 table has two rows (biscuit 3.28, aegis 2.64 from `scores.csv`), so it cannot show FRAGILE under the current rule. The gap of 0.64 exceeds any single plus-or-minus-25 % weight change, but the rerun belongs to the lead. |

Related lead items, which change no score here: TM-1 (security state tamper; the case j design depends on it) and TM-8 (long-lived authority; case d2).

Score change: isolation_and_security 3 -> 2; os_kernel total 3.50 -> 3.28. The reuse decision (wrap/adapter) and the hard gates G1-G5 are unchanged; the G5 condition now carries a test.

Both questions raised for the lead were settled on 2026-10-21 (D3.8; the two ruling rows in the table above). Nothing is left open for the lead from this dossier.
