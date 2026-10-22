# Provenance validation and disagreements (s2-prov)

**FINAL v3, 2026-10-21, 13 ledger pairs**

## Rows in

| Agent | Discovery | Negative | Malformed |
|---|---|---|---|
| s2-br-a | 117 | 47 | 0 |
| s2-br-b | 97 | 31 | 0 |
| s2-br-c | 117 | 50 | 0 |
| s2-br-d | 92 | 38 | 0 |
| s2-br-e | 128 | 31 | 2 |
| s2-br-f | 100 | 38 | 0 |
| s2-br-g | 67 | 66 | 0 |
| s2-br-h | 248 | 32 | 0 |
| s2-lang-de | 29 | 209 | 0 |
| s2-lang-fr | 50 | 374 | 0 |
| s2-lang-nl | 40 | 230 | 0 |
| s2-lang-zh | 55 | 118 | 0 |
| s2-probe-jako | 15 | 34 | 0 |
| total | 1155 | 1298 | 2 |

## Malformed rows

- s2-br-e: 2 rows (lines 127 and 128, the two correction rows appended since v2): all 24 keys present, but in a different order from SCHEMA.md. Not fixed here; the lead sends them back. Both rows were read and merged.

## Changes since FINAL v2 (2026-10-20)

Row counts against the v2 rows-in table (discovery; negatives unchanged at 1298): s2-br-a 116 -> 117 (+1), s2-br-c 116 -> 117 (+1), s2-br-e 126 -> 128 (+2), s2-br-f 98 -> 100 (+2), s2-br-g 66 -> 67 (+1), s2-lang-zh 54 -> 55 (+1); all other agents unchanged. Total discovery 1147 -> 1155 (+8). Every new row is a duplicate-disposition correction row:

- s2-br-a row 117 (R07), verifier #3: GHSA-7h8w-hj9j-8rjw canonical_source_url OpenHands/software-agent-sdk -> OpenHands/OpenHands (the SDK stays only in the `against:` text).
- s2-br-c row 117 (R11), verifier #9: CATP npm row; tests and maintenance now filled from lfzkoala/catp. Evidence level stays inspected.
- s2-br-e row 127 (R20), verifier #4: GHSA-9f65-56v6-gxw7 canonical_source_url null -> anthropics/claude-code. Licence stays null (not read).
- s2-br-e row 128 (R18), verifier #9: tuf-js npm row; tests and maintenance filled from the repository; the github row is primary.
- s2-br-f row 99 (R22), verifier #9: @solana/attestation npm row; repository solana-attestation-service inspected (MIT, tests, last commit 2026-10-02).
- s2-br-f row 100 (R25), verifier #9: @worldcoin/idkit npm row; repository worldcoin/idkit inspected (MIT, HEAD 2026-10-19).
- s2-br-g row 67 (R27), verifier #5: arXiv 2505.16068 canonical_source_url easy-retro-pgf -> null (the paper links no code).
- s2-lang-zh row 55 (R13), verifier #2: Tencent/MMKV licence NOASSERTION -> BSD-3-Clause, with a flag for third-party components.

Effect on codebases.jsonl: 586 codebases both times. One lead codebase was renamed (advisories-ghsa-9f65-56v6-gxw7 became anthropics-claude-code, because the advisory row now has a canonical URL; disposition lead, status A, licence null, unchanged). Fields changed on existing rows: tencent-mmkv (licence code and evidence level), solana-foundation-solana-attestation-service (source records, maintenance), worldcoin-idkit (version, tests), plus dedup_notes on lfzkoala-catp and theupdateframework-tuf-js. Candidate, lead, excluded and counterexample-only counts are unchanged from v2 (185 / 279 / 104 / 18).

Method note: correction rows that fix the canonical_source_url of a counterexample row (rows 117 of s2-br-a and 67 of s2-br-g) are not counted as separate records for grouping, so they add no duplicate-only codebase; they stay in the corrections list below.

## Verifier corrections applied to codebases.jsonl (v3)

- #6 dapr-durabletask-go: dedup_notes now state it is a fork of microsoft/durabletask-go, diverged (dapr +333, -37), microsoft HEAD 2026-10-12 and v1.0.0-beta3, and that Stage 3 should say which tree it inspects.
- #7 eclipse-biscuit-biscuit-rust: license_flags now carries "licence file in subdirectory only" (biscuit-auth/LICENSE is Apache-2.0; repository root has none; GitHub reports no licence); note added.
- #8 datalad-datalad: license_flags now carries "third-party code section in COPYING" (Python licence, BSD-2, BSD-3 parts; GitHub SPDX NOASSERTION); note added.
- #10 NOT applied (lead decision: candidate counts are by unique codebase, so several records of one codebase for one requirement already count once). The candidate counts in the coverage matrix are already per unique codebase.
- #1 (Roscpy), #2 (MMKV, as above), #3, #4, #5 and #9 are ledger-row corrections made by the agents; they are folded in as listed above. The v2 rows for #1 were already applied in v2.

Disagreement lists below are the v2 lists, re-derived on the v3 data; none of the new correction rows resolved or added an entry (the corrected codebases had no entry in v2).

## Disagreements between records of one codebase

### Canonical source
- none

### Licence
- gitlab-opencode-de-f13-microservices-agentic-orchestrator: MPL-2.0 <- s2-br-a:R06, s2-br-a:R07, s2-br-b:R01; OTHER:REUSE per-file (LICENSES/ has GPL-3.0-or-later, MPL-2.0, CC-BY-4.0, CC-BY-SA-4.0; no top-level LICENSE) <- s2-br-b:R01; OTHER:REUSE per-file (src/, configs/, schemas/, docker/mcp_services MPL-2.0; tests/, scripts/, compose/, helm/ GPL-3.0-or-later; prose CC-BY-SA-4.0; no top-level LICENSE) <- s2-lang-de:R01, s2-lang-de:R06
- nanmicoder-cc-haha: OTHER:cc-haha-Community-Source-License-1.0 <- s2-br-a:R29; OTHER:cc-haha Community Source License 1.0 (source-available, noncommercial, not OSI) <- s2-br-h:R29; MIT <- s2-br-h:R29
- bytecodealliance-wasmtime: Apache-2.0 <- s2-br-b:R02; Apache-2.0 WITH LLVM-exception <- s2-br-e:R02, s2-br-e:R21
- keepassxreboot-keepassxc-browser: OTHER:GPL-3.0 (LICENSE file; only vs or-later not checked) <- s2-br-b:R05; GPL-3.0-only <- s2-br-e:R05, s2-br-e:R20
- sqlite-org: OTHER:SQLite public-domain dedication (blessing); not read from a licence file in this record <- s2-br-c:R13; OTHER:SQLite-public-domain <- s2-br-d:R13, s2-br-d:R17; OTHER:SQLite public-domain dedication <- s2-br-h:R13
- wangfenjin-simple: MIT OR GPL-3.0-or-later <- s2-br-d:R17, s2-br-h:R17; NOASSERTION <- s2-lang-zh:R17
- gov4git-gov4git: MIT OR Apache-2.0 <- s2-br-g:R30; MIT <- s2-br-h:R30

### Upstream status (material spread only: G with any other, or A/B with D/E/G)
- nanmicoder-cc-haha: B <- s2-br-a:R29, s2-br-h:R29; G <- s2-br-h:R29
- helixar-ai-hdp: B <- s2-br-a:R07, s2-br-c:R12; D <- s2-br-c:R12
- askalf-browser-bridge: C <- s2-br-e:R19; G <- s2-br-e:R19
- atomgit-com-openeuler-community: G <- s2-br-h:R30, s2-lang-zh:R30; A <- s2-lang-zh:R30
- gitlab-inria-fr-coast-team-mute-mute: G <- s2-lang-fr:R16; B <- s2-lang-fr:R16

### Disposition (candidate vs excluded for the same requirement)
- openwallet-foundation-labs-identity-common-ts R12: [('candidate', 's2-br-c'), ('candidate', 's2-br-f'), ('excluded', 's2-br-c')]

## Correction rows applied (23)

A correction row (notes start with pass2 and say correction/correcting, or a duplicate row saying the earlier row 'should be read as follows') overrides licence_code of that agent's earlier rows (upstream_status only when the correction row is a duplicate row or its notes discuss status, archiving or activity, so that audit-evidence notes from Branch D do not reset status) on the same repository, and the disposition too when the correction row is not itself a duplicate and is for the same requirement.

- s2-br-a R09 on github.com/agentskills/agentskills [duplicate]: https://pypi.org/project/skills-ref/ R09: upstream_status C -> B
  - note: pass2: correction row, duplicate of my pass-1 R09 record 'Agent Skills open specification: SKILL.md ...' (platform github, canonical https://github.com/agentskills/agentskills), which stays the authoritative record with disposition candidate. All three LICENSE
- s2-br-a R06 on github.com/modelcontextprotocol/typescript-sdk [duplicate]: https://github.com/modelcontextprotocol/typescript-sdk R06: license_code OTHER:MIT-to-Apache-2.0-transition -> Apache-2.0
  - note: pass2: duplicate of my pass-1 R06 record on this repository (license_code 'OTHER:MIT-to-Apache-2.0-transition'), which should be read as follows. SPDX declared by the code at HEAD is Apache-2.0 (package.json at root and packages/client, npm v2 packages). The L
- s2-br-a R07 on github.com/openhands/openhands [duplicate]: https://github.com/advisories/GHSA-7h8w-hj9j-8rjw R07: canonical_source_url https://github.com/OpenHands/software-agent-sdk -> https://github.com/OpenHands/OpenHands
  - note: pass2 correction (verifier #3): canonical_source_url of earlier row https://github.com/advisories/GHSA-7h8w-hj9j-8rjw pointed at the argued-against repo; advisory source is OpenHands/OpenHands (confirmed with gh api advisories/GHSA-7h8w-hj9j-8rjw: source_code_
- s2-br-b R01 on github.com/eclipse-biscuit/biscuit-rust [duplicate]: no earlier row needed changing (value already agrees or row not found)
  - note: pass2 correction: duplicate of my pass-1 R01 record for https://github.com/eclipse-biscuit/biscuit-rust. Branch H is right that the repository root has no LICENSE file (root listing: .github, .gitignore, .travis.yml, CODE_OF_CONDUCT.md, CONTRIBUTING.md, Cargo.
- s2-br-c R12 on github.com/openwallet-foundation-labs/identity-common-ts [candidate]: https://github.com/openwallet-foundation/sd-jwt-js R12: upstream_status G -> A
  - note: pass2 correction. identity-common-ts is ACTIVE, not archived. Its SD-JWT VC support: packages/sd-jwt-core (SD-JWT, RFC 9901) and packages/sd-jwt-vc (draft-ietf-oauth-sd-jwt-vc; src has vct, type-metadata format and status-reference modules), plus token-status-
- s2-br-c R11 on github.com/lfzkoala/catp [duplicate]: no earlier row needed changing (value already agrees or row not found)
  - note: pass2 correction (verifier #9): corrects the earlier row 'npm distribution of the CATP command-line tool and enforcement plugin' (platform npm, result_url https://www.npmjs.com/package/@catp-protocol/cli), whose evidence_level was inspected but whose tests_or_
- s2-br-d R14 on github.com/mem0ai/mem0 [excluded]: no earlier row needed changing (value already agrees or row not found)
  - note: pass2 correction to my pass-1 mem0 row. Findings from source: (1) README says OSS v3 uses 'Single-pass ADD-only extraction -- one LLM call, no UPDATE/DELETE. Memories accumulate; nothing is overwritten', so my pass-1 statement that Mem0 rewrites facts on every
- s2-br-d R15 on github.com/privy-io/shamir-secret-sharing [candidate]: no earlier row needed changing (value already agrees or row not found)
  - note: pass2 correction to the pass-1 privy-io/shamir-secret-sharing row; reports opened and text-extracted with pdftotext. Cure53: three findings: PVY-01-002 (High) degree of polynomial might be less than t-1, so with some probability fewer than t parties can recons
- s2-br-d R15 on github.com/filosottile/typage [candidate]: no earlier row needed changing (value already agrees or row not found)
  - note: pass2 correction to the age and typage candidate rows: 'none found' is the result. Public security record is advisories only (GHSA-32gq-x56h-299c for age, GHSA-4fg7-vxc8-qx5w for rage, both 2024-12-18, plugin-name handling; Gentoo lists further package bugs fo
- s2-br-d R15 on github.com/brooooooklyn/keyring-node [candidate]: no earlier row needed changing (value already agrees or row not found)
  - note: pass2 correction to the @napi-rs/keyring and keyring rows: no audit found. Trust rests on the OS credential stores themselves (Keychain, Credential Manager, Secret Service); neither wrapper audits those. For R15 treat the keychain as a convenience for a key-en
- s2-br-d R17 on github.com/tobi/qmd [candidate]: no earlier row needed changing (value already agrees or row not found)
  - note: pass2 correction: evidence of retrieval quality for QMD, sqlite-vec, LanceDB and Orama on personal knowledge bases: none found. For QMD an in-repo eval harness and bench fixtures exist (inspected listing and one queries file), the README describes position-awa
- s2-br-e R20 on github.com/bitwarden/clients [duplicate]: https://github.com/bitwarden/clients R20: license_code NOASSERTION -> GPL-3.0-only AND OTHER:Bitwarden-License-1.0 (bitwarden_license/ directory); https://github.com/bitwarden/clients/blob/main/apps/browser/src/background/nativeMessaging.background.ts R20: license_code GPL-3.0-only -> GPL-3.0-only AND OTHER:Bitwarden-License-1.0 (bitwarden_license/ directory)
  - note: pass2 correction: supersedes the licence statement in my earlier R20 rows for bitwarden/clients (pass-1 lead 'Bitwarden desktop native-messaging proxy' and pass-2 candidate 'Bitwarden browser extension to desktop app channel'), which gave GPL-3.0 only or NOASS
- s2-br-e R20 on github.com/anthropics/claude-code [duplicate]: https://github.com/advisories/GHSA-9f65-56v6-gxw7 R20: canonical_source_url None -> https://github.com/anthropics/claude-code
  - note: pass2 correction (verifier #4): corrects my pass-1 R20 row 'Claude Code IDE integration WebSocket accepted connections from arbitrary origins (CVE-2025-52882)', which left canonical_source_url null. gh api advisories/GHSA-9f65-56v6-gxw7 returns source_code_loc
- s2-br-e R18 on github.com/theupdateframework/tuf-js [duplicate]: no earlier row needed changing (value already agrees or row not found)
  - note: pass2 correction (verifier #9): corrects my pass-1 R18 npm row for https://www.npmjs.com/package/tuf-js (disposition candidate, evidence inspected), whose tests_or_benchmarks and maintenance fields were empty. I opened theupdateframework/tuf-js through the Git
- s2-br-f R24 on github.com/squads-protocol/v4 [candidate]: https://www.npmjs.com/package/@sqds/multisig R24: license_code MIT -> AGPL-3.0
  - note: pass2 correction. chain: solana. At HEAD af94153ff77a28b6effe46b9c94baaa93742b48c the tree contains exactly one licence file, the root LICENSE = GNU AGPL-3.0 (inspected text). Declarations: on-chain program crate programs/squads_multisig_program/Cargo.toml has
- s2-br-f R24 on github.com/mythic-project/oyster [duplicate]: https://www.npmjs.com/package/@realms-today/spl-governance R24: license_code MIT -> Apache-2.0
  - note: pass2 correction: license_code of earlier row https://www.npmjs.com/package/@realms-today/spl-governance was MIT from npm metadata; repository LICENSE at e1223a9dbdd7eb7c9ec07aa765776d91438150f4 is Apache-2.0 (root LICENSE is the full Apache License 2.0 text, 
- s2-br-f R22 on github.com/solana-foundation/solana-attestation-service [duplicate]: https://api.mainnet-beta.solana.com R22: license_code None -> MIT, upstream_status A -> B
  - note: pass2 correction (verifier #9): corrects earlier row https://www.npmjs.com/package/@solana/attestation (R22), whose tests_or_benchmarks and maintenance came from the registry only. Repository inspected: clients/typescript has src, test and CHANGELOG.md; packag
- s2-br-f R25 on github.com/worldcoin/idkit [duplicate]: no earlier row needed changing (value already agrees or row not found)
  - note: pass2 correction (verifier #9): corrects earlier row https://www.npmjs.com/package/@worldcoin/idkit (R25), whose tests_or_benchmarks and maintenance came from the registry only. Repository worldcoin/idkit inspected: MIT (LICENSE, Copyright (c) 2025 World Found
- s2-br-g R30 on github.com/gov4git/gov4git [excluded]: https://github.com/gov4git/gov4git R30: upstream_status B -> G, disposition candidate -> excluded
  - note: pass2 correction of my pass-1 R30 row (which said candidate, status B). Licence read from files: LICENSE says 'All contributions are licensed under a dual MIT/Apache-2.0 license', and both LICENSE-MIT (full MIT text) and LICENSE-APACHE exist; CHANGELOG v1.1.10
- s2-br-g R27 on arxiv:2505.16068 [duplicate]: https://arxiv.org/abs/2505.16068 R27: canonical_source_url https://github.com/gitcoinco/easy-retro-pgf -> None
  - note: pass2 correction (verifier #5): canonical_source_url of earlier row https://arxiv.org/abs/2505.16068 held the argued-against repo; the paper links no code; against: https://github.com/gitcoinco/easy-retro-pgf
- s2-lang-fr R06 on github.com/roscpy/server-mcp [duplicate]: https://github.com/Roscpy/server-mcp R06: license_code MIT OR Apache-2.0 -> NOASSERTION, disposition candidate -> lead
  - note: pass2 correction: corrects my earlier R06 row for https://github.com/Roscpy/server-mcp (first row, disposition candidate, license_code 'MIT OR Apache-2.0'). That value came from Cargo.toml and a README badge only; the repository root has no LICENSE file, so un
- s2-lang-fr R30 on gitlab.inria.fr/belenios/belenios [duplicate]: https://hal.science/hal-01900081 R30: license_code None -> AGPL-3.0-or-later, upstream_status A -> B
  - note: pass2 correction: corrects my earlier R30 Belenios row (license_code AGPL-3.0-or-later, taken from the README Legal section). COPYING is the unmodified GNU AGPL version 3 text (its 'or any later version' lines are the standard template appendix, so COPYING alo
- s2-lang-zh R13 on github.com/tencent/mmkv [duplicate]: https://github.com/Tencent/MMKV R13: license_code NOASSERTION -> BSD-3-Clause
  - note: pass2 correction (verifier #2): license_code of earlier row https://github.com/Tencent/MMKV was NOASSERTION; LICENSE.TXT at 007a393cd5e255e9aa68d6648f7179159bdf0f9d is BSD-3-Clause except third-party components (flag). Quote: 'MMKV source code is licensed unde

## Counterexample rows not attached to any other record

18 counterexample rows named a target no non-counterexample record covers; each became a counterexample-only codebase.
