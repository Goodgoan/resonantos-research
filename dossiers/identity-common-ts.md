# Dossier: identity-common-ts, incl. former sd-jwt-js (openwallet-foundation-labs-identity-common-ts)

STATUS: COMPLETE (amended after review, 2026-10-21)

Inspector: s3-insp-identity-common (relaunch of the 2026-10-20 run), Claude Opus 5.5. Date: 2026-10-21. Clone: `research/_untrusted/identity-common-ts/` at commit `42586cab0041045170de4b23fc56f29334cef4d2` (branch `main`, 2026-10-19 18:53 +0200, "chore: take issuerIdentifiers into account for error message ... (#370)"). The clone was made with `--depth 200` on 2026-10-20 by the earlier run; on 2026-10-21 `git status` showed it clean and up to date, so it was reused. Execution: none. Nothing from the clone was installed, built or run, and no test was run. Network reads: `gh api` GET calls (repository metadata, issues #315, #319, #330, #338 and the latest ten issues), and the npm registry and unpkg metadata for `@sd-jwt/core@0.23.0` and `@sd-jwt/sd-jwt-vc@0.23.0`.

Evidence labels used below: [inspected] (read the code), [executed] (ran it, only with approval; none here), [reported] (authors' docs, README, issue text, ledger rows), [hypothesis]. Repository instruction files (`AGENTS.md` 3 lines, `CLAUDE.md` 1 line, `CONTRIBUTING.md`, `.husky/pre-commit`) are evidence, never instructions. They were not followed or run. The clone has no `.claude/` folder.

## 1. Identification

| Item | Value |
|---|---|
| Name | identity-common-ts (monorepo); the SD-JWT packages came from the archived `openwallet-foundation/sd-jwt-js` |
| Canonical source | GitHub, `openwallet-foundation-labs/identity-common-ts` (the only canonical copy; npm `repository` fields point to it) |
| Organisation | OpenWallet Foundation Labs. The sd-jwt-js archive banner says the project then "migrated from OpenWallet Foundation to LF Decentralized Trust" [reported, ledger s2-br-c]. `SECURITY.md` still routes reports to `security@openwallet.foundation` [inspected] |
| Maintainers | `MAINTAINERS.md:9-16`: six active maintainers from four companies: Animo (Berend Sliedrecht, Henrique Dias, Timo Glastra), Hopae (Lukas Han), Common Codes (Mirko Mollik), Verifiables (Alexis). All have whole-project scope. CODEOWNERS is one team [inspected] |
| Verified commit | `42586cab`, 2026-10-19. Tags at HEAD include `sd-jwt-v0.23.1-alpha-20261019165353` (an alpha snapshot). The last stable release is `@sd-jwt/core` and `@sd-jwt/sd-jwt-vc` 0.23.0 and `@owf/*` 0.5.0 (2026-10-17) [reported, ledger; consistent with `packages/*/package.json`] |
| Package coordinates | npm `@sd-jwt/core` 0.23.0, `@sd-jwt/sd-jwt-vc` 0.23.0, `@owf/token-status-list` 0.5.0, `@owf/crypto` 0.5.0, `@owf/identity-common` 0.5.0 (plus 15 more, see section 2). ESM only since 0.23.0 (`packages/sd-jwt-core/CHANGELOG.md`, 0.23.0 entry) |
| Supply-chain metadata | The published `@sd-jwt/core@0.23.0` and `@sd-jwt/sd-jwt-vc@0.23.0` carry npm SLSA provenance attestations (`predicateType https://slsa.dev/provenance/v1`, registry read). Releases are built by `.github/workflows/release.yml:18,21` (`NPM_CONFIG_PROVENANCE: "true"`, `id-token: write`, trusted publishing) [inspected] |
| Licence | Apache-2.0. The root `LICENSE` is the 200-line Apache 2.0 text. There are no per-package LICENSE files in the repository, but the published tarball contains `/LICENSE` (unpkg file list for `@sd-jwt/core@0.23.0`). There is no NOTICE file. Every `package.json` declares `Apache-2.0`. No discrepancies [inspected] |
| DOI / paper / SWHID | none found |
| Documentation language | English. The maintainer community works in English (issues, changesets, docs) |
| Predecessor | `openwallet-foundation/sd-jwt-js`, archived 2026-09 at `636c14b3`, last release v0.20.1 (2026-08-29) [reported, ledger]. Its code entered this repository in commit `65a7173` (2026-09-16, "feat: migrate sd-jwt to identity-common (#203)") [inspected `git log`] |

## 2. What works

**Packages in the monorepo** (from `packages/*/package.json`, parsed with `python -I` from the scratchpad) [inspected]:

| Package (npm name, version) | Purpose | Runtime deps | Relevance to R12/R23 |
|---|---|---|---|
| `sd-jwt-core` (`@sd-jwt/core` 0.23.0) | SD-JWT, RFC 9901: issue, present, verify, decode, Key Binding JWT, General and Flattened JSON serialisation | `@owf/identity-common` only | **core** |
| `sd-jwt-vc` (`@sd-jwt/sd-jwt-vc` 0.23.0) | SD-JWT VC (draft-ietf-oauth-sd-jwt-vc): `vct`, type metadata, status-list check | core, token-status-list, identity-common, zod | **core** |
| `token-status-list` (`@owf/token-status-list` 0.5.0) | IETF Token Status List (draft-ietf-oauth-status-list): bitstring with 1, 2, 4 or 8 bits, deflate, JWT and CWT transport, random index allocator | cose, identity-common, cbor-x, pako, zod | **core** (revocation) |
| `crypto` (`@owf/crypto` 0.5.0) | WebCrypto helpers ES256, ES384, ES512; noble SHA-2 hasher; SRI `integrity()`; salt generator | `@noble/hashes`, identity-common | helper (see the salt finding) |
| `identity-common` (`@owf/identity-common` 0.5.0) | base64url, JWT decode, dates, content types | none | transitive |
| `cose` (`@owf/cose`) | COSE/CWT | cbor-x, zod | transitive via status list |
| `x509` (`@owf/x509`) | X.509 and CRL parsing with pluggable crypto | `@peculiar/asn1-*`, asn1js | not needed |
| `mdoc` (`@owf/mdoc` 0.8.3) | ISO 18013-5 mdoc/mDL | cose, x509, token-status-list | not needed |
| `dcql` (4.0.0) | Digital Credentials Query Language | valibot | maybe later (DAO-side request language) |
| `oauth2`, `openid4vci`, `openid4vp`, `openid4vc-utils` (`@openid4vc/*` 0.8.0) | OAuth 2.0, OpenID4VCI, OpenID4VP | zod, buffer | not needed. This is where advisory GHSA-qx2x-38rh-2qrp applies |
| `eudi-*` (seven packages) | EU wallet ecosystem: access and registration certificates, JAdES, LoTE, trusted lists, SCA, attestation schema | various (xadesjs, xmldom ...) | not needed |

**SD-JWT core features** [inspected]:
- Issue: `SDJwtInstance.issue` (`packages/sd-jwt-core/src/index.ts:122-180`). It requires a hasher, a salt generator and `signAlg`, and rejects `none` (`:137-142`). It rejects reserved names `_sd`, `_sd_alg`, `_sd_decoy` and `...` anywhere in the payload (`:45-62`). Hash algorithms are restricted to `DEFAULT_SECURE_HASH_ALGORITHMS` (`types/type.ts:39-51`, `index.ts:147-153`). Packing (`sdjwt.ts:221-349`) supports nested and array disclosures and decoys, and rejects duplicate salts (`sdjwt.ts:23-32`).
- Present: `present(encoded, presentationFrame, { kb })` (`index.ts:195-223`) selects disclosures and optionally appends a KB-JWT whose `sd_hash` covers the presented SD-JWT (`:219-221`).
- Verify: `verify` (`index.ts:228-282`) checks the issuer signature through the injected `verifier`, recomputes digests and unpacks claims (`validate`, `:461-481`), checks `requiredClaimKeys`, and checks the KB-JWT (typ, alg, nonce, audience, max age, time claims, `sd_hash`; `kbjwt.ts:13-87`, `index.ts:258-279`). `safeVerify` (`:292-442`) collects coded errors instead of failing fast.
- Verifier options (`jwt.ts:19-101`): `expectedIssuer`, `expectedAudience`, `expectedSubject`, `expectedVct`, `maxAgeSeconds`, `allowedIssuerAlgorithms`, `allowedKeyBindingAlgorithms`, `keyBindingNonce`, `expectedKeyBindingAudience`, `keyBindingMaxAgeSeconds`, `skewSeconds`, `currentDate`, `disableStatusVerification`.

**SD-JWT VC features** [inspected]:
- `SDJwtVcInstance` uses `typ: dc+sd-jwt` (`sd-jwt-vc-instance.ts:51`) and forbids selective disclosure of `iss`, `nbf`, `exp`, `cnf`, `vct` and `status` (`:66-74`).
- Status check (`:563-615`). It fetches the status list token through `statusListFetcher` (default: global `fetch` with a 10 s timeout and a content-type check, `:81-103`), checks the `statuslist+jwt` header, verifies the signature with `statusVerifier` (falling back to the credential verifier, `:581-588`), checks the claims (`sub` equals the referenced URI; `iat`, `exp`; `:600-604`), reads the bit at `idx`, and calls `statusValidator` (the default rejects anything other than 0 with code `STATUS_INVALID`, `:111-117`).
- Type metadata (`sd-jwt-vc-type-metadata-format.ts:223-238`) is opt-in (`loadTypeMetadataFormat`, config `sd-jwt-vc-config.ts:43`). It resolves `extends` chains with a depth limit and cycle detection (`sd-jwt-vc-instance.ts:472-541`) and checks SRI `vct#integrity` (`:276-305`).

**Tests that exercise each property** (file and test name; none were run):

| Property | Tests | Quality |
|---|---|---|
| Disclosure integrity (digest recompute, unreferenced, duplicate or colliding disclosures) | Helper level: `sd-jwt-core/src/__tests__/rfc9901-validation.test.ts` "rejects duplicate digest in _sd array" (:23), "... across nested _sd arrays" (:35), "rejects unreferenced disclosure" (:66), "rejects when no digests exist in payload but disclosures provided" (:77), "rejects disclosed claim name that conflicts with plaintext key" (:88). End to end: `sd-jwt-core/src/__tests__/e2e/app-e2e.test.ts` "rejects tampered disclosure bytes" (:124-151); the "From JSON (...)" round trips (:153-216) through the `JSONtest` helper (:218-273), which runs issue, present, getClaims and verify over the example vectors | Explicit `toThrow` assertions. **Amended after review:** the rfc9901-validation tests call the helper `unpackObj` with synthetic digests ('abc123', 'used1'; :13-17, :66-75). They do not exercise the verifier recomputing a digest from disclosed bytes. The end-to-end tamper test corrupts byte 2 into invalid UTF-8 and is rejected as "Invalid disclosure data" (:146, :150), which is a decode failure, not a digest mismatch. No test alters a disclosure while keeping it well formed and then calls `verify` (grep for tamper, manipulat, forg in both test trees: only :124). Recomputation is exercised positively by the round trip |
| Algorithm and format hardening | `rfc9901-audit-fixes.test.ts` "RFC 9901 audit fixes": malformed containers (:23), name collisions (:45), claim validation after disclosure (:60), unsafe alg (:87), insecure hash algs (:155), duplicate salts (:171), General JSON header placement (:186) | Good. The title says "audit" but no audit report was found (section 3) |
| Key binding | `index.test.ts` describe "issuer options on key-bound presentations" (:1115-1270), which uses `keyBindingNonce` (helper at :25-70); "verify rejects an expired kbJwt during full verification" (:332); `kbjwt.test.ts` (:67-581); e2e "From JSON (key_binding)" (`sd-jwt-vc/src/__tests__/e2e/app-e2e.test.ts:169`) | Mixed: see the vacuous-test finding below |
| Revocation (status list) | `sd-jwt-vc/src/__tests__/index.test.ts` describe "Revocation": "Test with a revoked credential" (:153-174, expects `STATUS_INVALID` with `{uri, idx: 1, status: 1}`), "... non revoked" (:110), "... status verification disabled" (:281), "... subject does not match the referenced uri" (:299), "... typ header is not statuslist+jwt" (:317), "test with an expired status list" (:418). `token-status-list/src/__tests__/status-list-jwt-claims.test.ts:38-129` (typ, sub, iat, exp, skew, nbf). `status-list.test.ts` (bit-packing against the spec example, :195) | Good for the logic. "test to fetch the statuslist" (:414) is an empty TODO; fetching is never exercised against a server |
| Robustness | `sd-jwt.fuzz.test.ts` (fast-check over `decodeSdJwt`, crash-only property) | Shallow |

**Negative-test quality finding** [inspected]. There are 16 negative tests in `sd-jwt-core` (8 in `index.test.ts`, 5 in `jwt.test.ts`, 3 in `kbjwt.test.ts`) written as `try { await verify(...) } catch (e) { expect(...) }` with no `expect.assertions(n)` anywhere in the three packages (grep count 0). Such a test passes if `verify` does **not** throw. Two are vacuous at HEAD:
- `index.test.ts:211-259` "verify failed with kbJwt" configures a failing `kbVerifier` but calls `sdjwt.verify(presentation)` without `keyBindingNonce`. Per `index.ts:248-250` the KB-JWT is then never checked, `verify` succeeds, and the `catch` never runs.
- `index.test.ts:261-330` "verify with kbJwt" also omits `keyBindingNonce`, so the `kbVerifier` it defines (which reads `cnf.jwk`) is never invoked.
The key-bound describe block at `:1115` does test KB properly. Issue #315 (2026-10-05) records the same weakness from outside: "Tests only cover negative cases without key binding, which is why this passed" [reported].

**Deployment evidence.** Named production users were not established. Animo (Credo) and the EUDI ecosystem are the obvious users [hypothesis]. npm downloads are not used as evidence.

**CI** (`.github/workflows/ci.yml`) [inspected]. The `validate` job (`:21`, ubuntu-24.04, Node 24) runs style, markdown, types, entrypoints, build and ESM import checks. The `tests` job (`:56`, ubuntu-24.04, matrix Node `[22, 24, 26]` at `:63`) runs `pnpm test` (`:93`), i.e. vitest across all packages. `codeql.yml` and `scorecard.yml` are present. No Windows or macOS leg.

## 3. Maturity

- **Footprint** [inspected]. An in-process library with no daemon. `@sd-jwt/core` has one runtime dependency (`@owf/identity-common`, which has none), so the SD-JWT core has zero third-party runtime code. `@sd-jwt/sd-jwt-vc` adds zod and the status-list stack: `pako` 3.0.2, `cbor-x` 1.6.6 via `@owf/cose`, and cbor-x's optional native addon `cbor-extract` 2.2.2 with prebuilds for darwin, linux and win32-x64 (`pnpm-lock.yaml:1501-1508, 3279-3296`).
- **Cadence** [inspected, depth-200 history]. Commits per month: 2026-04 16, 05 26, 06 26, 07 19, 08 17, 09 49, 10 47. The repository was created 2026-02-04 [reported, ledger]. Twelve humans appear in the window. The top contributors are Mirko Mollik (43), Timo Glastra (29), Berend Sliedrecht (25) and Manthan Nimodiya (19); dependabot accounts for 50. Bus factor is about 4 people across 3-4 companies.
- **Releases.** Changesets, 22 releases since 2026-05 [reported, ledger]. Breaking changes are frequent. Between 0.21.0 and 0.23.0 (about one month): the `SDJWTException` constructor changed (0.22.0), CommonJS was dropped (0.23.0), and verifier-option scoping changed (0.22.0) (`packages/sd-jwt-core/CHANGELOG.md`). Everything is 0.x.
- **Issue response** (five sampled, `gh api`) [inspected]: #353 closed in 1 day; #342 in 4 days; #338 "SRI validation uses wrong digest encoding" in 2 days; #331 in 1.5 hours; #319 "expectedVct / expectedIssuer / expectedSubject reject a valid presentation when key binding is also verified" in 30 minutes. #330 "Clock skew" is open since 2026-10-07. Response is fast. But three of these are correctness bugs in verification code introduced within the previous month (#315 and #319 from #272; #338 in the SRI check), which signals churn in security-relevant paths.
- **Security posture.** `SECURITY.md` has private reporting via GitHub advisories and email, 3-business-day acknowledgement and 10-day triage [inspected]. One published advisory, GHSA-qx2x-38rh-2qrp (medium, SSRF via `request_uri` at the PAR endpoint), affects `@openid4vc/oauth2` and `@credo-ts/openid4vc` only, not the SD-JWT or status-list packages [reported, ledger s2-br-c; not re-queried, per the relaunch note]. **No third-party audit was found.** The test file `rfc9901-audit-fixes.test.ts` came in with the migration commit `65a7173`, and no report, firm or date is referenced in the repository (grep for "audit" in Markdown found only unrelated EUDI text). CodeQL and OpenSSF Scorecard workflows exist. npm provenance attestations are published.
- **Documentation.** Per-package READMEs with an RFC 9901 security checklist (`packages/sd-jwt-core/README.md`), runnable examples in `examples/sd-jwt/{core,sd-jwt-vc}`, and a docs site workflow. Some comments are stale: three places in `sd-jwt-vc` still cite draft-ietf-oauth-status-list-02 (`sd-jwt-vc-instance.ts:569`, `sd-jwt-vc-payload.ts:21`, `sd-jwt-vc-status-reference.ts:2`) while the status-list package cites drafts 13 and 16. The comment at `index.ts:227` describes a `requireKeyBindings` option that does not exist (grep).
- **Popularity, paired with fitness.** 12 GitHub stars for the new repository. This understates use, because the npm names `@sd-jwt/*` carried over from sd-jwt-js. Fitness rests on the tests above, not on these numbers.

**Counterexample rows (answered here and in section 8):**

1. *s2-br-c R12, against identity-common-ts* (advisory, 0.x, two governance moves, issue #330 clock skew, scope wider than needed). **Partly confirmed, partly refuted.**
   - The advisory is real but out of scope for the packages we would use. `@sd-jwt/core` and `@sd-jwt/sd-jwt-vc` do not depend on `@openid4vc/*` (section 2 table) [inspected].
   - 0.x churn is confirmed and is worse than the row says: two breaking API changes in a month, and three verification regressions in October (#315, #319, #338).
   - Clock skew (#330): the issue body lists bugs mostly outside SD-JWT (`eudi-sca`, `openid4vp`). For SD-JWT it reports inconsistent skew defaults and a status-list double check. At HEAD the status-list token is verified first with `getJwtTimeValidationOptions(options)` (`sd-jwt-vc-instance.ts:587-588`) and only then with `verifyStatusListJwtClaims` (`:600-604`), so the double check persists [inspected]. Severity is low: it can cause false rejections, not false acceptances.
   - Wide scope: confirmed, but harmless if only `@sd-jwt/core`, `@sd-jwt/sd-jwt-vc` and `@owf/token-status-list` are installed. Each is published separately.
   - Effect on scores: maturity is held at 3, not 4, and the decision is to wrap and pin exact versions.
2. *s2-br-f R23, against the archived sd-jwt-js.* **Confirmed for the old repository; refuted as a migration burden.** The predecessor is archived (status G). But the npm names `@sd-jwt/core` and `@sd-jwt/sd-jwt-vc` were kept with their own version line (`CHANGELOG.md` 0.21.0: "The `@sd-jwt/*` packages keep their own version line, separate from `@owf/*`"), and the npm `repository` field points to the live repository. Only the helper packages moved: the old status-list and crypto helpers are now `@owf/token-status-list` and `@owf/crypto` [inspected]. The row's statement that dependants "must follow the migration to ... (@owf/*)" is therefore true only for those helpers. Churn risk stands; abandonment risk does not.

## 4. Architecture

- **Control flow (verifier side)** [inspected]. `SDJwtVcInstance.verify` (`sd-jwt-vc-instance.ts:123-139`) runs in this order:
  1. `SDJwtInstance.verify` (`sd-jwt-core/src/index.ts:228`) calls `SDJwt.fromEncode` (split on `~`, decode disclosures).
  2. `validate` (`:461`) calls `Jwt.verify` (`jwt.ts:345-368`: alg not `none`, optional allow-list, then the injected `verifier(data, sig, options)`).
  3. `getClaims` recomputes the disclosure digests and unpacks (`decode/decode.ts`), then validates reserved names and time claims.
  4. If and only if `keyBindingNonce` is set: `KBJwt.verifyKB` (`kbjwt.ts:13-87`) and the `sd_hash` comparison (`index.ts:268-279`).
  5. `verifyStatus` (`sd-jwt-vc-instance.ts:563`).
  6. If enabled, type-metadata fetch and merge.
- **Crypto model: fully pluggable** [inspected]. The library performs no signing or verification itself. `Signer = (data: string) => string | Promise<string>` and `Verifier = (data, sig, options?) => boolean | Promise<boolean>` (`types/type.ts:117-121`), plus a `Hasher` and a `SaltGenerator` (`:120-121`), are all injected through `SDJWTConfig` (`:53-65`). Issuer key resolution (DID, x5c, JWKS) is entirely the caller's job: the `verifier` is a closure configured per instance. For key binding, `kbVerifier(data, sig, payload)` receives the credential payload, and **the caller must extract `cnf.jwk` and verify against it**. The library does not tie the KB signature to `cnf` (`kbjwt.ts:82-84`; no other `cnf` handling in either package, grep).
- **Ed25519 and Solana keys** [inspected for Ed25519; hypothesis for wallets]. Every core and VC test signs with Node `crypto.generateKeyPairSync('ed25519')` and `signAlg: 'EdDSA'` (`sd-jwt-core/src/__tests__/index.test.ts:13-23`; `sd-jwt-vc/src/__tests__/index.test.ts:26-42`; the status-list token is signed with `jose` EdDSA at `:44-57`), so EdDSA/Ed25519 is the tested default. `@owf/crypto` ships only ES256, ES384 and ES512 helpers (`packages/crypto/src/crypto.ts:75-151`), so Ed25519 needs a 10-line adapter (Node `crypto`, `@noble/curves`, or WebCrypto Ed25519 in Node 24).
  - A Solana wallet holds an Ed25519 keypair, and its address is the base58 of the 32-byte public key. That key maps to `cnf: { jwk: { kty: 'OKP', crv: 'Ed25519', x: base64url(pubkey) } }`. A wallet `signMessage(utf8(header.payload))` that returns a raw 64-byte signature would be a valid EdDSA JWS signature for a KB-JWT [hypothesis, not demonstrated anywhere].
  - Caveat: hardware wallets (Ledger's Solana app) sign only the Solana off-chain-message format with a header prefix, which would not produce a plain JWS signature [hypothesis].
  - The wallet would also show the user an opaque base64url string, which conflicts with the human-readable consent that SIWS-style messages give.
- **Storage.** None. Status lists and type metadata are fetched on demand through injectable fetchers. There is no cache (the caller must provide one, `sd-jwt-vc-config.ts:37-39`).
- **Lifecycle.** Stateless functions and instances. No start, stop or crash semantics.
- **Runtime.** TypeScript compiled by tsdown to ESM `dist/index.mjs` (`packages/sd-jwt-core/package.json`, `publishConfig`). It uses `globalThis.crypto` (WebCrypto) and `globalThis.fetch`. The non-test sources of the five relevant packages contain no `node:` imports, `process`, `fs` or `path` (grep) [inspected]. Engines: the root says `node >=20`; CI covers 22, 24 and 26.
- **Operational model.** An embedded library. A Node 24 process calls it directly (`import { SDJwtVcInstance } from '@sd-jwt/sd-jwt-vc'`). It can also run in the MV3 extension, since it is browser-safe and has no Node built-ins [hypothesis; the README claims Node, browsers and React Native, reported].
- **Dependency footprint.**
  - Core: `@owf/identity-common`.
  - VC: + `@owf/token-status-list`, `@owf/cose`, `zod` ^4.6, `pako` ^3.0.2, `cbor-x` ^1.6.6 (+ optional native `cbor-extract`, whose install script uses `node-gyp-build-optional-packages`).
  - Tests only: `jose`, `vitest`, `fast-check`, `msw`.

## 5. Direct relevance

**R12 (provenance records with human/AI attribution and selective-disclosure claim packages).**

| R12 constraint | Fit | Evidence |
|---|---|---|
| TS library | yes | section 4 |
| Off-chain verifiable | yes | `verify` needs only the presentation, the issuer public key and, if referenced, a status-list token |
| Anchorable on Solana as a hash or root | possible, not demonstrated | Nothing in the repository mentions Merkle, Solana, Ethereum or chains (grep over packages, docs, examples, tests: no hits). The natural leaf is `sha256(issuer-signed JWT)` or the `sd_hash` of a presentation, but the Merkle tree and anchor are ours to build |
| Tool identity, session attribution, human/AI portions | expressible as ordinary claims; no vocabulary | The payload is an open `Record<string, unknown>` (`index.ts:40`). Nothing in the packages mentions provenance, attribution or AI (grep, no hits). A custom `vct` plus claim names would be defined by ResonantOS/ResonantDAO (shared schema S1) |
| Commitments and redaction | yes, native | Each selectively disclosable claim is a salted hash commitment in `_sd`. Undisclosed claims stay digests; decoys hide the claim count (`types/type.ts:171-178`) |
| Reviewer verifies what the user disclosed (I7) | yes in code. Tests: positive end to end, negative at helper level | The verifier recomputes every digest from the disclosed material and rejects unreferenced or duplicate disclosures. The negative cases are tested on the helper `unpackObj` (`rfc9901-validation.test.ts:23-99`). End to end there are only round trips and one decode-failure tamper test (section 2, amended) |

Mapping to the consent tiers (interaction section 5) [hypothesis, design]:
- **T1 commitments**: present the SD-JWT VC with no disclosures. The reviewer sees the plaintext claims (tool identity, human/AI split, artifact hashes, timestamps) and only digests for everything else.
- **T2**: also disclose a `summary` claim.
- **T3**: disclose the artifact-content claims, or the artifact hash plus the file out of band.
- Plaintext (non-disclosable) claims cannot be removed by the holder. Putting the human/AI split outside the disclosure frame therefore guarantees that it travels in every package once it exists (invariant I5 at the format level). **Amended after review (D-identity-common-ts-1, C-6):** no Alpha component produces a split today. The harness receipts carry session, turn and dispatch identity only. The cited test asserts `dispatch.session` and `turnId` (`browser-first/test/harness-host-service.test.mjs:565-579`), and `harness-host-service.mjs` has no human, AI, share or portion field (grep for those words: only `sharedLease` matches, at :190-203). The format is ready; the source is absent.

**R23 (proof of key control, off-chain registry with anchored commitments, revocation).**
- *Proof of key control (DR-05).* A KB-JWT is a nonce-bound (`nonce`) and audience-bound (`aud`, checked by `expectedKeyBindingAudience`, `kbjwt.ts:53-60`) signature by the `cnf` key with a freshness limit (`keyBindingMaxAgeSeconds`, `:62-74`). With a Solana-wallet `cnf` that is functionally a SIWS-style challenge, but only if the verifier always passes `keyBindingNonce` and its `kbVerifier` checks against `cnf` (section 4). Not demonstrated with a wallet.
- *Registry and anchoring.* Not provided. The library is a credential format, not a registry. **Amended (D-identity-common-ts-7):** membership uniqueness and caps (DR-04 "at most one active Community Member credential per wallet", DR-10) are properties of the registry, not of the format. Batch issuance (section 8) deliberately produces several valid credentials per member, so the format cannot carry them.
- *Revocation (DR-06, threat T15).* `@owf/token-status-list` implements the IETF Token Status List (README: draft-ietf-oauth-status-list; code comments cite drafts 13 and 16). It is wired into `@sd-jwt/sd-jwt-vc` verification and tested (section 2). A random index allocator (`status-list-index.ts`, tests at `status-list-index.test.ts:15-72`) gives herd privacy against index correlation. **Amended after review (D-identity-common-ts-4, S-identity-common-ts-2, C-4, C-5):** what is demonstrated is *bit-level* revocation by one issuer key. Governed revocation is not, and several properties are missing:
  - (a) A status-list token is one JWS with one signer (`sd-jwt-vc-instance.ts:577-588`), so multisig needs threshold signing or a governance step before signing. Neither exists.
  - (b) There is no history: each new token replaces the last, so an issuer can revoke and silently restore a member, which goes against DR-06.
  - (c) Split view: the default fetcher pulls the list from the issuer's URI on every verification (`:81-103`), so an issuer can serve different lists to different verifiers.
  - (d) `Suspended = 0x02` exists (`token-status-list/src/types.ts:13`), but the default validator rejects every non-zero value as `STATUS_INVALID` (`sd-jwt-vc-instance.ts:111-117`). Suspension and revocation are indistinguishable unless a custom `statusValidator` is supplied.
  - (e) Offline verification with a cached token accepts a revoked credential until the token's `exp`, which the issuer chooses. The library enforces no verifier-side maximum age.

**Alpha seams** (cited rows):
- OSC-26: `AI_MEMORY/provenance/` is created empty (`browser-first/host/memory-schema.mjs:11`).
- OSC-12: research trail, raw intake only.
- OSC-35: the OpenCode boundary carries session attribution.
- The gaps.md R12 "code pointer to be confirmed in Stage 3" is now confirmed: host-signed receipts are Ed25519 over canonical JSON with an ephemeral per-boot key that is never persisted (`browser-first/host/harness-host-service.mjs:17-24, 145-161`; receipt kinds `boot`, `adapter-dispatch`, `route`, `event` at `:164, 252, 304-326, 428`; test "receipt signing preserves concurrent session/turn attribution", `browser-first/test/harness-host-service.test.mjs:565`). Those receipts are the point-of-work attribution source that a claim-package builder would condense into an SD-JWT VC.
- DAO side: DR-03 and DR-05 (signed membership, key control), DR-17 (human/AI split), DR-19 (per-item opt-in), DR-50 and DR-51 (off-chain evidence, salted commitments, anchored roots); Phase 1 core items 1, 2 and 5.

**Threats and the provenance property check** (threat-model section 4, "Provenance (T5, T13, T20)", plus the launch message's list):

| Property | Result | Test or evidence |
|---|---|---|
| Human/AI attribution and tool identity expressible | **Expressible, not demonstrated.** No schema, claim names or example exist. Expressibility is trivial (open payload); what matters is the shared schema S1, which does not exist | none in the repository |
| Selective disclosure verifiable by a third party (I7) | **Partly demonstrated** (amended): positive recomputation end to end; rejection of a well-formed altered disclosure only at helper level | Round trips: `sd-jwt-vc/src/__tests__/e2e/app-e2e.test.ts:141-201` and `sd-jwt-core/src/__tests__/e2e/app-e2e.test.ts:153-216`. Negatives on the helper `unpackObj`: `rfc9901-validation.test.ts` (:23, :35, :52, :66) and `rfc9901-audit-fixes.test.ts:23-60`. End to end there is only the UTF-8 tamper test (`sd-jwt-core/.../e2e/app-e2e.test.ts:124-151`). Needed: acceptance case (a2), section 11 |
| Revocation via status lists | **Bit-level revocation demonstrated; governed revocation not** (amended). Logic only, not transport: IETF Token Status List, package `@owf/token-status-list`, enforced in `@sd-jwt/sd-jwt-vc` | "Revocation > Test with a revoked credential" (`sd-jwt-vc/src/__tests__/index.test.ts:153-174`); status-list-token header, subject and expiry negatives (:299, :317, :418); `status-list-jwt-claims.test.ts:38-129`. The fetch path is a TODO (:414). There is no history, threshold or split-view protection (R23 bullet above) |
| Anchoring demonstrated anywhere | **Not demonstrated.** No code, example or deployment in the repository | needs our own Merkle-anchoring component (R23 candidates) |

- **T5** (AI derivations promoted as human): helped only indirectly. A signed record can carry the domain label, but the gate is R14 and R11.
- **T13** (self-declared split): **not closed, and worse than self-declared if the key is reachable** (amended, D-identity-common-ts-2, S-identity-common-ts-1, TM-6). In the OS-to-DAO direction the OS host is both issuer and holder under the user's control, so the split is at best self-asserted. A file-readable host key would let a delegated AI child sign `human: 1.0` itself: children run unconfined outside macOS (OSC-32), and the read-deny list covers only `ResonantOS_User/Secrets` (`browser-first/host/delegation-isolation.mjs:175-209`, which lists `.ssh` through `Library/...` and three `Secrets` roots). SD-JWT gives tamper evidence after issue and makes the claim non-strippable. It says nothing about who decided the split. R12 is necessary, not sufficient. Closing T13 also needs key custody (R03/R15), a human ceremony (R11) and DAO-side review (R25; DR-17 conservative default).
- **T20** (attribution collapse): **open** (amended, D-identity-common-ts-1). The format can carry a split, but no OS component produces one. The producer would sit at the R07/R12 seam: harness adapters that record which turn content came from the user versus the model, plus a human-declared split captured at claim time. Until it exists, the only honest value is `method: 'declared'`.
- **T19** (OS data to the DAO without a per-item act): the format supports minimisation; consent is the builder's UI (I3).

## 6. Reuse decision

**Wrap or adapter: adopt `@sd-jwt/core` and `@sd-jwt/sd-jwt-vc` and `@owf/token-status-list` as pinned dependencies behind a thin Resonant adapter.** The adapter supplies the Ed25519 signer and verifier, a `cnf`-checking `kbVerifier`, a 128-bit salt generator, a hardened verifier wrapper that always requires key binding, an offline status fetcher, and the Resonant provenance `vct` schema. It beats the alternatives in section 12:
- It is the only maintained TypeScript implementation in the ledger that gives salted-commitment selective disclosure, key binding and status-list revocation, all tested, with zero third-party runtime dependencies in the core.
- irmago is Go and needs a server stack and an app.
- in-toto/DSSE has no TypeScript implementation and no selective disclosure.
- TrustVC anchors on EVM only.
- HDP is young and record-only.

It is *not* a full R12/R23 solution. Anchoring, the registry and the attribution schema remain custom.

**After review (2026-10-21) the decision is unchanged: wrap. The custom layer is larger and its conditions are now binding:**
- The issuer key is held by the bridge only, in the R15 vault or OS keystore, never in `CONFIG` (S-identity-common-ts-1, X-1).
- Issuance needs a human ceremony recorded in the R11 approval ledger (D-identity-common-ts-2).
- The record certifies each boot's receipt public key (D-identity-common-ts-3).
- Verifiers apply a maximum status age (S-identity-common-ts-2).
- Revocation bits are derived from governed revocation records in a witnessed log (D-identity-common-ts-4, C-4).

For R23 the library is a component (holder binding and revocation bits), not the candidate. The registry and anchoring candidate is transparency-dev-tessera (section 12).

Hard gates (`scoring/weights.json`):

| Gate | Result | Clause |
|---|---|---|
| G1 no mandatory cloud or telemetry | **pass** | No telemetry. The only network use is the status-list fetch to the issuer's own URI (default `fetch`, replaceable by `statusListFetcher`, `sd-jwt-vc-config.ts:34`; disable with `disableStatusVerification`) and the opt-in type-metadata fetch (`loadTypeMetadataFormat`, default false) |
| G2 Windows, macOS, Linux or honest matrix | **pass with caveat** | Pure ESM with WebCrypto and fetch, no OS-specific code. Upstream CI is Linux-only, so Windows and macOS are untested upstream (matrix in section 7). Nothing in the library can silently no-op per OS |
| G3 licence | **pass** | Apache-2.0, file-level, compatible with the MIT Alpha (keep the LICENSE; patent-termination clause section 3 noted) |
| G4 chain | **pass** | chain: none |
| G5 invariants I1, I2, I4 | **pass, conditional** | A library has no authority of its own. The integration must keep DAO credentials out of `authorizeBridgeRoute` (I2), keep the DAO verifier in an optional add-on (I1), and keep wallet signing human-only (I4); see section 7. Amended after review: also the provenance issuer key must be unreachable by the agent being attributed, and issuance must need a human act (I4/I5, D-identity-common-ts-2). Otherwise an AI child could sign human-only attribution, and the condition would fail |

## 7. Integration design

**Per-OS matrix** (Node 24 bridge, in-process library):

| OS | What runs | What degrades | What is silent |
|---|---|---|---|
| Linux | All three packages. Upstream CI on ubuntu-24.04 with Node 22, 24, 26 (`ci.yml:56-63`) | none | none |
| Windows | Expected to run unchanged: no `fs`, `path` or `process` in the sources; WebCrypto Ed25519 and `fetch` are built into Node 24 [hypothesis, not CI-verified upstream] | `cbor-extract` has a win32-x64 prebuild only; on win32-arm64 cbor-x falls back to pure JS (slower CBOR, only on the status-list CWT path) [inspected lockfile; fallback reported by cbor-x] | none expected. The risk is untested code, not no-ops. Mitigation: ResonantOS runs the adapter's tests on its own Windows CI lane |
| macOS | Same as Windows; darwin prebuilds for cbor-extract exist | none | none |

**Process boundary.** In-process library. The OS side (claim-package builder) lives in a new bridge add-on service. The DAO side (verifier, status-list issuer) runs in DAO tooling. The extension needs nothing.

**Data structure (shared schema S1 as an SD-JWT VC).** Sketch only:

```ts
// vct: "https://resonantos.org/vct/provenance-record/v1" (type metadata published with vct#integrity)
type ResonantProvenancePayload = {
  iss: string                 // did:jwk or did:key of the OS host provenance key (persistent, bridge-held in the R15 vault)
  iat: number; vct: string
  cnf?: { jwk: { kty: 'OKP'; crv: 'Ed25519'; x: string } } // member's Solana wallet key, for DAO-side binding
  tool: { harness: string; adapter: string; version: string } // plaintext, never SD
  receiptKeys: Array<{ bootEpoch: number; publicKey: string }> // per-boot receipt keys, certified by iss (D-3)
  session: { id: string; turns: number; receiptRoot: string } // hash over the signed receipts, disclosed on request
  attribution: { human: number; ai: number; method: 'declared'; approvalRef: string } // plaintext, never SD (I5)
  // 'measured' is deliberately absent until an OS-side producer exists (D-1); approvalRef points to the R11 record
  artifacts: Array<{ sha256: string; name?: string; summary?: string }> // name/summary selectively disclosable
}
```

- The disclosure frame makes `artifacts[*].name`, `artifacts[*].summary` and any free-text claim selectively disclosable. `tool`, `session` and `attribution` stay plaintext.
- The type metadata marks them `sd: 'never'`. The library does **not** enforce `sd` or `mandatory` from type metadata against a credential (only merge rules, `sd-jwt-vc-instance.ts:374-400`), so the DAO verifier must check this itself.

**Identity semantics.**
- The issuer is the OS host provenance key. **Amended (S-identity-common-ts-1, D-identity-common-ts-2, X-1).** It must be persistent, unlike today's ephemeral harness receipt key (`harness-host-service.mjs:145-147`). It is held by the bridge only, in the R15 vault or OS keystore and never in `~/ResonantOS_User/CONFIG` or any other path a child or the `archive-write` route can reach (the read-deny list protects only `Secrets`, `delegation-isolation.mjs:175-209`). The bridge signs only:
  - records whose `receiptRoot` it computes itself over receipts it produced and still holds;
  - and only after a human approval recorded in the R11 ledger (`approvalRef`).

  Until R15 exists, the key is per-boot like the receipt key, and records are verifiable only within that boot. That is weaker but not forgeable by a child.
- The holder binding is the member's wallet key, so the DAO can tie the package to the registered member (R23).
- The originating principal: **amended (D-identity-common-ts-3).** The receipt key is never persisted, and only its fingerprint is logged (`harness-host-service.mjs:147-150, 162-163`), so a DAO reviewer cannot authenticate receipts after the fact. However, the full public key is held in-process: `signer.publicKey` (`:149-150`) is returned by the service (`:443`). The builder therefore copies each boot's public key into `receiptKeys`, certified by the issuer signature. A reviewer given a T3 disclosure of receipts can then check each receipt signature and recompute `receiptRoot`. Without that, `receiptRoot` is only a user-supplied index over unauthenticated data, and it is labelled so in the type metadata.

**Error behaviour.** Use `safeVerify` and map its codes (`STATUS_INVALID`, `KEY_BINDING_*`, `JWT_*`) to user-visible reasons.

**Hardened verifier wrapper.** Required because of the findings in sections 2-4:
1. Always pass `keyBindingNonce` and `expectedKeyBindingAudience`. Fail if the KB-JWT is absent (core skips KB without a nonce, `index.ts:248-250`).
2. `kbVerifier` imports `payload.cnf.jwk` and verifies against it.
3. Set `allowedIssuerAlgorithms: ['EdDSA']` and `allowedKeyBindingAlgorithms: ['EdDSA']`.
4. Use a salt generator with 16 random bytes (do not use `@owf/crypto` `generateSalt`; section 8).
5. Use an injected `statusListFetcher` with a byte cap, a host allow-list and a local cache.
6. *(amended, S-identity-common-ts-2, X-7)* Apply a verifier-side maximum status age of 24 h for membership and 1 h for a claim decision, as a stated bound that the DAO may tune. Beyond it the result is "status unverified", never "valid". The bound does not depend on the issuer-set `exp`/`ttl`. Revocation takes effect at the next verification within the bound. There are no long-lived sessions to abort: each presentation is verified once.
7. *(amended, D-identity-common-ts-4)* A custom `statusValidator` maps `0x01` to "revoked" and `0x02` to "suspended" (`token-status-list/src/types.ts:9-13`), with a distinct code for each.
8. *(amended, D-identity-common-ts-4, C-4, C-5)* Accept a status-list token only if its SHA-256 appears in the R30/R23 witnessed log with an inclusion proof. Every bit flip has a governed revocation record behind it (reason, authority, evidence, appeal deadline; DR-06). This blocks silent restore and split view.
9. *(amended, D-identity-common-ts-8, S-transparency-dev-tessera-2, X-9, TM-9)* Holder proof by a Solana wallet uses a domain-separated, human-readable off-chain message, never raw `signMessage` over the JWS signing input. The message has a fixed prefix "ResonantDAO holder proof v1", the audience, the nonce and the `sd_hash` in readable form, and the length. The KB-JWT keeps its RFC 9901 structure. Its signature is the wallet's signature over that envelope, under a private `alg` value (for example `EdDSA-SolanaOffchain`) so that no generic verifier misreads it. The custom `kbVerifier` (`types/type.ts:119` receives `data`, `sig` and `payload`) rebuilds the envelope from `data` and checks it against `cnf` [hypothesis, design]. Cost: KB-JWTs from this path are not interoperable with other SD-JWT verifiers. A test rejects envelopes whose bytes parse as a Solana transaction message.

**Versioning.** Pin exact versions (`0.23.0`, not `^0.23.0`). Upgrade through one PR that reruns the adapter's tests.

**Alpha files that change:**
- new `browser-first/host/claim-package-service.mjs` (builder: harness receipts plus selected artifacts to an SD-JWT VC; preview; local audit entry);
- `run-bridge-minimal.mjs` (wire the service, disabled by default, its own capability);
- `browser-first/host/harness-host-service.mjs` (expose the receipt stream to the builder via the existing `onReceipt` sink, `:159`, and the per-boot public key via the returned `signer`, `:443`; no change to signing);
- the R15 vault module (not yet in the Alpha) for the issuer key, and the R11 approval ledger for `approvalRef`. Both are prerequisites of Phase B, not of the first PR;
- `browser-first/host/memory-schema.mjs` (`AI_MEMORY/provenance/` becomes the store for issued records);
- `package.json` (add the three pinned dependencies).

**Alpha tests affected** (of the 2,424 browser-first tests): none need renaming if the capability vocabulary only gains a new name. The route and capability audit tests that lock the vocabulary will need the new capability added. `test/harness-host-service.test.mjs` (including :565 and :581) must stay green, since the receipt format is unchanged. New tests: `test/claim-package-service.test.mjs`.

**Migration path.** Phase A: builder plus local verify (no DAO). Phase B: the DAO verifier and a status-list issuer for membership credentials. Phase C: Merkle-anchor the issued-record digests and the status-list-token digests on Solana (an R23 component).

## 8. Security and governance effects

- **New privileges.** None in the library. The builder service gets file-read access to selected artifacts and receipts, behind its own capability.
- **Attack surface added** [inspected unless marked]:
  - *Key-binding footgun.* `verify` silently skips the KB-JWT unless `keyBindingNonce` is passed (`index.ts:248-250`). The KB signature is not tied to `cnf` by the library (`kbjwt.ts:82-84`). A DAO verifier written from the README Quick Start (which passes no nonce) would accept a stolen credential replayed by anyone. Mitigation: the hardened wrapper (section 7).
  - *Salt entropy below the RFC recommendation with the shipped helper.* `pack` asks for `saltGenerator(16)` (`sdjwt.ts:24`), and `@owf/crypto` `generateSalt(16)` returns 16 hex characters from **8** random bytes (`packages/crypto/src/crypto.ts:3-14`), i.e. 64-bit salts. RFC 9901 recommends at least 128 bits, yet the README ticks "Minimum length of the salt". The examples use this helper (`examples/sd-jwt/core/utils.ts:1-3`). This matters for DR-50 ("hashes of low-entropy data are guessable, so salted commitments are needed"): an undisclosed claim such as `attribution.method` or a small integer could be brute-forced at 2^64 cost per guess. That is expensive but below the intended margin. Mitigation: inject a 16-byte salt generator. Worth reporting upstream.
  - *Status-list decompression without a size cap.* `inflate(compressed)` with no output limit (`token-status-list/src/status-list.ts:85-97`) runs after the token signature is verified. So only a malicious or compromised issuer could send a decompression bomb [hypothesis: DoS only].
  - *Default fetchers.* They call issuer-controlled URIs (status list, `vct`) from the verifier. This reveals verification activity to the issuer, and in a server verifier it is an SSRF vector of the same class as GHSA-qx2x-38rh-2qrp. Mitigation: inject fetchers with an allow-list.
  - *Test-suite gaps.* 16 try/catch negative tests can pass vacuously, two at HEAD do (section 2), and the October regressions #315, #319 and #338 show verification code changing fast. Mitigation: pin versions and keep our own negative tests in the adapter.
- **Revocation story** (amended after review, D-identity-common-ts-4, S-identity-common-ts-2, C-4, C-5).
  - Upstream gives an issuer-side status list with one signer and no history. `suspended` exists as a value but is treated as revoked by default. Freshness is bounded only by the issuer-set `exp` and `ttl`.
  - It does **not** meet DR-06: there is no reason, authority, evidence, appeal or kept history, and an issuer can split views and silently restore.
  - The Resonant layer supplies the rest (wrapper items 6-8): a verifier maximum age; a governed revocation record in the R30 witnessed log from which each status-list token is derived; and verifiers that require the token's inclusion proof. Anchoring the log root on Solana then makes revocation history tamper-evident. None of that is provided upstream.
- **Isolation story.** N/A (in-process library).
- **Personal data flows.** The format minimises: T1 packages reveal only plaintext claims and digests. Correlation risk: the same issuer signature, `cnf` key and status `idx` link every presentation of one credential (SD-JWT is not unlinkable, unlike BBS). For membership that is acceptable (the wallet is public). For claim packages, issue one credential per claim (batch issuance). Batch issuance means several valid credentials per member, so DR-04 and DR-10 uniqueness and caps are enforced by the registry, not by the format (amended, D-identity-common-ts-7).
- **Custody.** The wallet key stays with the user (holder). The OS host provenance key is held by the bridge only, in the R15 vault or OS keystore, and never in the child-writable user state root (amended, S-identity-common-ts-1, X-1). Key theft would turn T13 from "declared" into "apparently attested". The DAO holds the status-list signing key, a governance-relevant key. A single JWS signer cannot be "multisig", so the multisig sits one step earlier: the governed revocation record in the witnessed log needs k-of-n approval (R24), and the status-list signer only derives tokens from logged records.
- **Trust in maintainers.** Six maintainers from four companies, npm provenance, CodeQL. Moderate trust; the exact-version pinning addresses the churn.
- **DAO risks.**
  - Self-issued provenance (T13) cannot be made true by any format. Reviewers must treat `attribution` as a declaration (DR-17's conservative default).
  - Answering my Q8 after review (D-identity-common-ts-2): a human portion should count toward votes only after a second signer, such as a reviewer attestation that references the commitments.
  - A status-list key compromise lets an attacker revoke members (governance griefing). Wrapper item 8 confines this to revocations that have a logged record.
- **Consent, not only friction** (amended, D-identity-common-ts-8). A wallet asked to sign an opaque JWS teaches users to sign blobs they cannot read. That conflicts with E8 (transaction payload summary) and I3 (previewed). It also opens cross-protocol signing (S-transparency-dev-tessera-2). Remedy: wrapper item 9, a human-readable, domain-separated holder-proof message, at the cost of KB-JWT interoperability.

## 9. Licensing

- SPDX Apache-2.0 for every package (manifests and root `LICENSE`, 200 lines). The published tarball includes `LICENSE`. No NOTICE file, so section 4(d) imposes no NOTICE obligation.
- Transitive runtime: `zod` (MIT), `pako` (MIT AND Zlib), `cbor-x` and `cbor-extract` (MIT), `@noble/hashes` (MIT) [reported from general knowledge of those packages, not re-read from their licence files].
- Compatibility with the MIT Alpha: high confidence, since Apache-2.0 can be combined into MIT-licensed works with attribution kept.
- For independent legal review:
  1. The Apache-2.0 section 3 patent-termination clause, as it interacts with the proposed Symbiotic Licence (status F, unknown text).
  2. Whether the Symbiotic Licence would impose field-of-use terms that conflict with Apache-2.0 redistribution.
- This is technical research, not legal advice.

## 10. Cost and effort

- **Small (adapter plus local issue and verify, 3-5 dev-days).** Ed25519 signer and verifier, salt generator, hardened wrapper, offline fetcher, the provenance `vct` and type metadata, and adapter tests on Windows, macOS and Linux. Assumes the S1 claim names are agreed.
- **Medium (builder service plus consent preview plus DAO verifier, 2-3 weeks).** Receipt condensation (`receiptRoot`), the per-claim disclosure UI (T1-T3), the local audit entry, and DAO-side verification with `sd: never` enforcement.
- **Large (with R23 registry, status-list issuer and Solana anchoring, 6-8 weeks).** Membership credentials, a status-list issuer under multisig, a Merkle tree over issued digests, and a weekly anchor. Most of this effort is outside this codebase.
- **Skills.** TypeScript, JOSE basics. No new language (master prompt 5.5: no language cost).
- **Maintenance exposure.** 0.x with monthly breaking changes, so budget one upgrade PR per quarter.
- **Lock-in.** Low. SD-JWT is an IETF RFC (9901), and other implementations exist (Go, Rust, Python). Replacement cost is the adapter only.

## 11. Acceptance test

**Proof of concept** (requires executing third-party code, so it is a request for the user, not a plan). It would run in a scratch project outside `research/`, with `npm install --ignore-scripts @sd-jwt/core@0.23.0 @sd-jwt/sd-jwt-vc@0.23.0 @owf/token-status-list@0.5.0` on Windows 11 and Linux (Node 24), driven by our own test file.

1. Issue a provenance SD-JWT VC (payload from section 7) with an Ed25519 host key and a 16-byte salt generator. `attribution` and `tool` are plaintext; the two artifact names are disclosable.
2. Present at T1 (no disclosures) with a KB-JWT signed by a second Ed25519 key standing in for the wallet (`cnf.jwk`). The third-party verifier recomputes the digests (I7) and checks the nonce, `aud` and `cnf`.
3. Fault scenarios:
   - (a) Tamper a disclosure byte: expect reject.
   - (b) Append a foreign disclosure: expect reject "unreferenced".
   - (c) Strip the KB-JWT: the hardened wrapper rejects (and record that bare `verify` without a nonce accepts it, documenting the footgun).
   - (d) A KB-JWT signed by a key other than `cnf`: reject.
   - (e) Status bit flipped to 1 in a locally served status-list token: reject `STATUS_INVALID` (threat T15).
   - (f) Remove `attribution` before presenting: impossible without breaking the issuer signature (threat T20).
   - (a2) *(amended)* Replace a disclosure with a **well-formed** one (same claim name, different value, fresh salt) and call full `verify`: expect "Unreferenced disclosure". Upstream tests cover this only on the helper `unpackObj` (section 2).
   - (g) *(amended, S-identity-common-ts-2)* Revoke the credential, keep serving the older cached status-list token (still within its `exp`), and verify after the wrapper's maximum status age: expect "status unverified", not "valid".
   - (h) *(amended, D-identity-common-ts-4, C-5)* Split view: serve verifier A a token with bit 0 and verifier B a token with bit 1, where only one token hash is in the witnessed log. The verifier that receives the unlogged token refuses it. Also check that `0x02` is reported as "suspended", not "revoked".
   - (i) *(amended, S-identity-common-ts-1, D-identity-common-ts-2)* A child process with `archive-write` tries to read the issuer key and to call the builder with a `receiptRoot` it computed itself. Expect: the key is unreadable, and the builder refuses any record whose `receiptRoot` does not match bridge-held receipts or that lacks an R11 `approvalRef`.
   - (j) *(amended, D-identity-common-ts-3)* A reviewer given a T3 disclosure of receipts verifies each receipt signature against `receiptKeys` and recomputes `receiptRoot`. A receipt from another boot's key is rejected.
   - (k) *(amended, D-identity-common-ts-8, S-transparency-dev-tessera-2)* A holder-proof envelope whose bytes parse as a Solana transaction message is rejected before signing.
4. Expected output: a JSON report with one line per case (`[PASS]`/`[FAIL]`) and the recomputed digests.
5. CI hook: a new `test:claim-package` lane in the Alpha's `verify:alpha`, run on ubuntu, windows and macos runners.
6. Pass criterion: every case behaves as stated, and case (c) bare-verify behaviour is recorded.
7. Optional step 7 (the Solana-wallet compatibility test): sign the domain-separated holder-proof envelope (section 7, wrapper item 9) with a real Solana wallet's `signMessage` in a browser, and verify it through the custom `kbVerifier`. Requires a wallet and the user's approval.

## 12. Recommendation and confidence

**Benefits.**
- A standard (RFC 9901) salted-commitment format that maps cleanly onto consent tiers T1-T3 and invariant I7.
- Key binding that can serve as nonce-bound proof of wallet-key control.
- Tested bit-level status-list revocation (governed revocation is ours to add; section 5).
- A zero-dependency core, Ed25519 by default in the tests, ESM, npm provenance, and six maintainers across four companies.

**Trade-offs.**
- 0.x churn and recent verification regressions.
- Verifier footguns (KB is optional unless a nonce is passed; `cnf` is not checked by the library).
- 64-bit salts from the shipped helper.
- No anchoring or registry.
- SD-JWT presentations are linkable.
- *(amended)* No source of the human/AI split exists in the Alpha (T20 open). A signature under a reachable key would make T13 worse.
- *(amended)* Revocation does not meet DR-06 without our governed-revocation layer.
- *(amended)* Holder proof by wallet needs a non-standard, domain-separated envelope.

**Blockers.** None technical in the library. Prerequisites before Phase B (DAO-facing issuance):
- an agreed S1 schema;
- the R15 bridge-only key store;
- the R11 approval ledger;
- a witnessed log for revocation records (tessera, R30/R23).

**Readiness.** Ready to wrap for R12's format layer, but only for locally verifiable, per-boot records until R15 and R11 exist. For R23 it is a component (holder binding, revocation bits), not the candidate.

**Evidence quality.** The core claims are [inspected], with code and tests read at `42586cab`. Wallet compatibility, Windows behaviour and production users are [hypothesis] or [reported]. Nothing was [executed].

**Competing solutions, on the same criteria** (ledger rows; competitor code not inspected by me):

| Criterion | identity-common-ts | irmago (Yivi) | in-toto attestation + DSSE | TrustVC | Helixar HDP |
|---|---|---|---|---|---|
| Language / embed in Node 24 | TS library, in-process | Go; server plus mobile app ecosystem; would need a sidecar over HTTP | spec and protobuf; no TS implementation in the repo | TS library | TS library |
| Selective disclosure with hash commitments | yes, RFC 9901 | yes (Idemix, plus SD-JWT VC) | no (whole-envelope signing) | yes (ecdsa-sd-2023, BBS) | no |
| Human/AI attribution vocabulary | none (custom claims) | none | predicate types are extensible; SLSA covers builder identity | none | delegation provenance (closest to "tool identity") |
| Revocation | IETF Token Status List, tested | status lists, revocation tests (needs Postgres and others) | none | token registry on EVM | not stated |
| Anchoring | none | none | none (Rekor transparency log via Sigstore, not a chain) | Ethereum (chain: evm), so G4 reference-only | none |
| Maturity | 0.x, very active, 6 maintainers | since 2017, v1.4.2 | CNCF, "still under development" disclaimer | 30 releases since 2026-03 | created 2026-03, record-only semantics |
| Licence | Apache-2.0 | Apache-2.0 | Apache-2.0 | Apache-2.0 | Apache-2.0 |

**R23 competitor added after review (D-identity-common-ts-5): transparency-dev-tessera** (from its dossier `dossiers/transparency-dev-tessera.md`, not re-inspected by me).
- It is Go, Apache-2.0, chain: none, with an optional SPL Memo anchor (:110, :126, :136).
- It provides what this library lacks for R23: an append-only, witnessed membership and claim log in which "Membership changes (join, revoke, recover) are log entries too" (:130); inclusion proofs for members (:135); and split-view resistance only with at least one external witness (:176).
- It provides none of what this library has: no selective disclosure, no holder key binding, no status-list format.
- Its integration cost is a Go service the team does not have (its section 13: integration_effort 1).

The two are complements, not substitutes. Tessera is the R23 registry and anchor. identity-common-ts supplies the holder-bound credential and the derived revocation bits, whose token hashes are logged in tessera (wrapper item 8). For R23 ranking, tessera is the primary candidate and this library a component.

irmago is the more mature system but the wrong shape: a server stack and app ecosystem for a local-first Node bridge, and it has no attribution vocabulary either. in-toto/DSSE is a good model for the *tool identity and session* half (SLSA-style predicates). It could inform S1's claim names, but it lacks redaction. TrustVC is EVM-anchored (G4). HDP is closest in intent for tool and delegation provenance but is young and record-only. **Recommendation:** use SD-JWT VC as the S1 envelope, borrow in-toto/SLSA field naming for `tool` and `session`, and take anchoring from an R23 candidate.

**First PR (ResonantOS 2.0.0 Alpha, PR-sized).** Add `browser-first/host/provenance-record.mjs` plus `browser-first/test/provenance-record.test.mjs`. The module wraps `@sd-jwt/sd-jwt-vc@0.23.0` (exact pin in `package.json`) with:
- *(amended after review, S-identity-common-ts-1, X-1)* An Ed25519 issuer key generated per boot inside the bridge closure, exactly like the receipt key (`harness-host-service.mjs:145-150`), and never written to disk. Moving it to the R15 vault is a later PR; no key ever goes under `~/ResonantOS_User/CONFIG`.
- A 16-byte salt generator.
- `issueProvenanceRecord({ receipts, artifacts, attribution })`, which accepts only receipts from the in-process sink, computes `receiptRoot` itself, embeds the boot's receipt public key, and allows only `method: 'declared'`.
- `verifyProvenancePackage(presentation, { nonce, aud, maxStatusAgeSeconds })`, which always requires key binding, checks `cnf`, and distinguishes `0x01` from `0x02`.

The test covers acceptance cases (a) to (f), (a2), (g), (j) and the builder half of (i) with a local status list. It does not wire any route; that comes in the next PR, together with the R11 `approvalRef`.

**Confidence: medium.** The code-level findings are high-confidence and inspected, and all eleven citations were confirmed by the archaeologist review. Fitness for R12 depends on an S1 schema, a split producer, key custody (R15) and an anchoring component that do not exist yet. No test was executed. The review changed the size of the custom layer, not the decision.

## 13. Scores (for scoring/scores.csv)

Profile: **dao_contract** (R12 provenance format when anchored; R23 revocation and key binding). Amended after review: requirement_fit is now scored per requirement (D-identity-common-ts-5), so there are two rows in `scores.csv` terms. An os_kernel note follows the table. The isolation score was re-checked against the anchor as clarified on 2026-10-21 (state.md D3.7).

| Criterion | Score | Reason (anchor) |
|---|---|---|
| requirement_fit (R12) | 3 | Covers selective disclosure, commitments and redaction for R12. Anchoring, the attribution vocabulary and a source for the split are absent (T20 open) |
| requirement_fit (R23) | **3 -> 2** | Supplies a holder-binding path (never shown with a wallet) and bit-level revocation. No registry, anchoring or inclusion proofs, and revocation is not governed (DR-06). For R23 it is a component; tessera supplies the registry |
| demonstrated_maturity | 3 | Releases, CI, tests and fast issue response, but 0.x with monthly breaking changes, no audit, no named production users established ("3 = tests and releases but thin usage evidence") |
| isolation_and_security | 3 (unchanged; re-checked under the clarified anchor) | (a) No advisory or contrary evidence is unfixed in the artifacts that would be pinned: GHSA-qx2x-38rh-2qrp is in `@openid4vc/*`, which none of the three packages depends on; the 64-bit `generateSalt` is in `@owf/crypto`, which is not a dependency of any of the three (`packages/*/package.json`, section 2 table). (b) The properties are exercised by tests of the property itself: revocation through `SDJwtVcInstance.verify` (`sd-jwt-vc/src/__tests__/index.test.ts:153-174`); key binding through full `verify` with a nonce (`sd-jwt-core/src/__tests__/index.test.ts:1115-1270`); disclosure recomputation through end-to-end round trips. The well-formed-tamper negatives are helper-only, so this is "partly tested". (c) Rated as the upstream artifact: governed revocation and key custody are not upstream claims and are scored under requirement_fit, not here. (d) Lead ruling D3.8 applied. No inspected code path defeats a checked property *as the dossier configures it*. The KB skip (`index.ts:248-250`) is closed by always passing a nonce (wrapper item 1). The salt helper is not used (item 4). Split view and restore are closed by logged tokens (item 8). So 0 does not apply. The two absent mechanisms, anchoring and an attribution vocabulary, would each score 1 at most as stand-alone properties. I keep 3 because the anchor rates "the threat family it addresses", and their absence is already charged under requirement_fit. The alternative, averaging the four checked properties (I7 3, revocation 3-4, attribution 1, anchoring 1), gives 2. That is listed for the lead in section 14 |
| licence_suitability | 5 | Apache-2.0 at file level, transitive deps permissive |
| integration_effort | 5 | Embeddable typed TS library for Node 24 and the browser; a thin adapter is needed |
| maintenance_sustainability | 3 | Six maintainers from four companies and high cadence, against two governance moves in 2026, a young repository (created 2026-02) and API churn |
| sovereignty_and_portability | **5 -> 4** | Local-first, no account, user-readable JSON/JWT. But status verification contacts the issuer's URI. Even with the cache and maximum age it does so periodically, revealing verification activity (D-identity-common-ts-6). Between "5 = local-first ... no account" and "3 = local with optional relay" |
| interoperability | 5 | IETF RFC 9901 plus SD-JWT VC and Token Status List drafts; EUDI-aligned; other-language implementations exist. The wallet envelope (wrapper item 9) is a deliberate local deviation |
| operational_complexity | **5 -> 4** | The library is one process, but its use requires the DAO to run a status-list issuer: an HTTP endpoint plus a governance-relevant signing key (D-identity-common-ts-6). Between "5 = one process, no external services" and "3 = one sidecar" |

Weighted totals (dao_contract weights from `scoring/weights.json`: requirement_fit .16, maturity .16, isolation .18, licence .08, integration .06, maintenance .14, sovereignty .08, interoperability .06, operations .08):
- Before review: 3.72 (single row).
- After review, R12 row: .48 + .48 + .54 + .40 + .30 + .42 + .32 + .30 + .32 = **3.56**.
- After review, R23 row: R12 row minus .16 = **3.40**.

The DAO skeptic's 3.30 (C-2) assumed isolation 2. That point is disputed above.

os_kernel note for the OS-side claim-package builder: the same library inside the bridge adds no privileges and no network path unless a status fetcher is configured. With the R12 row's values under os_kernel weights, the total is .54 + .42 + .66 + .50 + .40 + .30 + .32 + .20 + .24 = 3.58 (information only). The bridge-side risks are the issuer key (bridge-only, R15) and the builder's file-read capability (R01), not the library. Those belong to the proposed layer, which is unscored (security review X-3).

## 14. Open questions for the adversarial reviewers

1. **Solana wallet compatibility** is a hypothesis. Do Phantom, Solflare and Backpack `signMessage` sign raw UTF-8 bytes without a prefix, so that a KB-JWT signature verifies as EdDSA? Ledger's off-chain-message header would break it. Not tested.
2. **Windows.** No upstream Windows CI. My "runs unchanged" claim rests on the absence of Node built-ins in the sources. The `cbor-extract` install script and its fallback on win32-arm64 were not exercised.
3. **The "RFC 9901 audit fixes" test title** suggests an external review. I found no report, firm or date in the repository; the sd-jwt-js history before the depth-200 window was not searched. If an audit exists, it would raise isolation_and_security.
4. **Salt finding.** I read `generateSalt` as producing 64-bit salts when called with 16 (`crypto.ts:8`, `length / 2` bytes). A reviewer should confirm that no caller in `@sd-jwt/*` passes a larger length (`sdjwt.ts:24` passes 16) and decide whether this deserves an upstream issue.
5. **Vacuous tests.** My claim that `index.test.ts:211-259` passes without exercising key binding comes from static reading of `index.ts:248-250`. It was not executed.
6. **Production users** (Credo, EUDI pilots) were not established. Maturity is scored without them.
7. **Draft versions.** The code comments cite status-list drafts 02, 13 and 16, and SD-JWT VC drafts 13 and 15. Which draft the wire format actually matches was not checked against the IETF texts.
8. **T13 cannot be closed by a format.** Reviewers in the mechanism-design role should challenge whether a self-issued, OS-signed attribution claim adds anything beyond tamper-evidence, and whether the DAO should require a second signer (for example a reviewer attestation) before the human portion counts. *Answered by D-identity-common-ts-2: yes. Adopted in section 8.*
9. **Linkability.** Should DAO claim packages need unlinkability across claims, SD-JWT is the wrong primitive (BBS or ecdsa-sd-2023 via TrustVC/w3c would be the alternatives, but their anchoring is EVM). Not evaluated further.
10. **Not re-queried.** The advisory list, release count and issue totals come from the ledger (2026-10-20) and the earlier run, per the relaunch note.
11. **For the lead (added after review): the isolation_and_security aggregation under D3.8.** I score 3, because the anchor rates the threat family the codebase addresses (selective disclosure and revocation, both property-tested). The alternative, averaging all four checked properties including the absent anchoring and attribution, gives 2. That moves the totals to R12 3.38 and R23 3.22. I recommend 3 to avoid double-charging absence already counted in requirement_fit, but this is a method choice the lead should settle consistently across dossiers.
12. **Holder-proof envelope** (wrapper item 9) is a design hypothesis. Whether wallets will sign the envelope, and whether a private `alg` value is acceptable to the DAO, needs the wallet test in section 11, step 7.

### Review responses (2026-10-21)

Counts: 15 accepted, 3 partly accepted, 0 fully disputed (one sub-point of C-2 disputed), 6 recorded without change (agreement rows, lead-owned items, bookkeeping). Total: 24 ids.

| Id | Verdict | Change made (section) or evidence for dispute |
|---|---|---|
| S-identity-common-ts-1 | accepted | The issuer key is bridge-only (R15 vault or keystore), never in `CONFIG`. It signs only from bridge-held receipts and after an R11 approval. The first PR uses a per-boot in-closure key. Sections 6, 7 (Identity semantics, payload), 8 (Custody), 11 case (i), 12 first PR. Evidence: `delegation-isolation.mjs:175-209` protects only `Secrets` |
| S-identity-common-ts-2 | accepted | Verifier maximum status age (wrapper item 6), acceptance case (g). Sections 5 (R23 point e), 7, 8, 11 |
| S-identity-common-ts-3 | agreed (no objection) | isolation_and_security 3 kept and re-checked under the clarified anchor (section 13) |
| S-transparency-dev-tessera-2 (its "same point applies to identity-common-ts"; pattern X-9) | accepted | Domain-separated, human-readable holder-proof envelope with a transaction-parse rejection test. Section 7 wrapper item 9, section 8 consent, section 11 case (k) |
| X-1 | accepted | Same change as S-identity-common-ts-1. No security state of this design sits in the user state root |
| X-7 | partly accepted | A stated bound is added (wrapper item 6, case g). Not applicable: there is no long-lived session or stream to abort, since each presentation is verified once at claim decision time (section 7) |
| TM-6 | recorded (lead's) | Consistent with the amended T13 text, "R12 necessary, not sufficient" (section 5). No score change |
| TM-9 | recorded (lead's) | Wallet cross-protocol signing is handled in the design (wrapper item 9). No score change |
| D-identity-common-ts-1 | accepted | T20 reworded to open. `measured` dropped from the schema. The producer is named at the R07/R12 seam. Sections 5, 7, 12. Evidence: `harness-host-service.test.mjs:565-579` asserts session and turn only; grep finds no human, AI or share field in `harness-host-service.mjs` |
| D-identity-common-ts-2 | accepted | Bridge-only key, human ceremony (`approvalRef`), DAO second signer before a human portion counts. G5 condition amended. Sections 5, 6, 7, 8, 14 Q8 |
| D-identity-common-ts-3 | accepted | The builder embeds each boot's receipt public key (`receiptKeys`), certified by the issuer. Otherwise `receiptRoot` is labelled a user-supplied index. Evidence that this is cheap: the public key is held in-process (`harness-host-service.mjs:149-150`) and returned as `signer` (`:443`). The reviewer's `:160-161` for the stderr line is `:162-163` at `578fbbc`. Sections 7, 11 case (j) |
| D-identity-common-ts-4 | accepted | The property is reworded "bit-level revocation demonstrated; governed revocation not". Points (a)-(d) are confirmed (`sd-jwt-vc-instance.ts:81-103, 111-117, 577-588`; `token-status-list/src/types.ts:13`). Suspended mapping, logged tokens with inclusion proof, governed revocation record. Sections 5, 7 items 7-8, 8, 11 case (h) |
| D-identity-common-ts-5 | accepted | requirement_fit split: R12 3, R23 3 -> 2. Tessera added as the R23 primary candidate, with this library as a component. Sections 6, 12, 13 |
| D-identity-common-ts-6 | accepted | operational_complexity 5 -> 4 and sovereignty_and_portability 5 -> 4 (section 13) |
| D-identity-common-ts-7 | accepted | DR-04 and DR-10 are stated as registry properties (sections 5, 8) |
| D-identity-common-ts-8 | partly accepted | Consent framing accepted (section 8). The proposed remedy, "define the KB check over a SIWS message", cannot keep a standard KB-JWT: RFC 9901 KB signatures cover the JWS signing input. The design therefore keeps the KB-JWT structure, signs a domain-separated envelope over it under a private `alg`, and verifies through the pluggable `kbVerifier` (`types/type.ts:119`). The interoperability cost is stated (section 7, item 9) |
| C-1 | recorded (lead's) | Scoring-method blocker owned by the lead. My new totals (R12 3.56, R23 3.40) widen the gap to tessera's 3.74 |
| C-2 | partly accepted | The rescorings from D-5 and D-6 are applied. **Disputed:** isolation_and_security 2. Under the clarified anchor (clauses a-d) no unfixed contrary evidence exists in the pinned artifacts, and revocation and key binding are tested at property level (`sd-jwt-vc/src/__tests__/index.test.ts:153-174`; `sd-jwt-core/src/__tests__/index.test.ts:1115-1270`). Governed revocation is not an upstream claim (clause c). Lead to settle the aggregation question (Q11) |
| C-3 | accepted | The property table names the full condition: bit, not governance; signature, not attribution (section 5) |
| C-4 | accepted | Governed revocation record in the R30 log; status-list tokens derived from it and inclusion-checked (sections 7, 8) |
| C-5 | accepted | Split view added as a threat and as acceptance case (h) (sections 5, 11) |
| C-6 | accepted | The dossier no longer says R12 carries attribution. The split has no source (section 5) |
| C-8 | recorded | Bookkeeping. The header is now `STATUS: COMPLETE (amended after review, 2026-10-21)` |
| Archaeologist (A-identity-common-ts) | no objections | 11 of 11 citations PASS. During the amendment I also found that the rfc9901-validation negatives test the helper `unpackObj` with synthetic digests, and that the end-to-end tamper test is a UTF-8 decode failure. The I7 row is downgraded to "partly demonstrated" and case (a2) is added (sections 2, 5, 11) |

Score changes (section 13):
- requirement_fit (R23) 3 -> 2;
- sovereignty_and_portability 5 -> 4;
- operational_complexity 5 -> 4.

Weighted dao_contract totals: 3.72 -> R12 row 3.56 and R23 row 3.40. Reuse decision unchanged (wrap). The hard gates are unchanged, except that the G5 "pass, conditional" condition is extended to key custody and the human ceremony.
