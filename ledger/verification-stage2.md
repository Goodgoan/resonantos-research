# Stage 2 verification (s2-verify, 2026-10-20)

Independent check of the Stage 2 discovery ledgers. No ledger was edited. No cloning, execution, issues or comments. Public APIs only.

## Method and reproduction

- Copy time: 2026-10-20 14:36:59 WEDT. All 13 `discovery-*.jsonl` copied to the scratchpad subfolder `s2-verify\d\`. Rows read from the copies in alphabetical file order (s2-br-a..h, s2-lang-de, s2-lang-fr, s2-lang-nl, s2-lang-zh, s2-probe-jako), numbered from 1.
- N seen at copy time: **1099** (equals `records_in` in the codebases.jsonl header). A re-count at 14:45 WEDT found 1147 rows on disk, so s2-br-h (or another agent) appended 48 rows after the copy; those rows are not in the sample frame.
- Seed 20261020, sample size round(0.10 * 1099) = **110**.
- Reproduction: `python -I -c "import random; random.seed(20261020); print(sorted(random.sample(range(1,1100),110)))"` (the script used `random.sample(range(1,N+1),k)` after `random.seed(20261020)`; numbering is over the 1099-row concatenation).
- Selected row numbers: 6, 14, 23, 33, 37, 49, 66, 80, 95, 102, 104, 128, 131, 135, 168, 173, 185, 186, 187, 189, 191, 195, 226, 234, 238, 266, 284, 286, 298, 304, 315, 322, 325, 332, 349, 354, 360, 371, 392, 393, 403, 417, 419, 423, 424, 429, 436, 438, 442, 444, 450, 456, 458, 462, 489, 505, 524, 547, 552, 564, 577, 590, 621, 639, 643, 654, 657, 661, 681, 712, 731, 749, 752, 776, 777, 782, 796, 806, 814, 819, 824, 834, 864, 875, 891, 900, 910, 911, 919, 924, 931, 938, 942, 951, 954, 975, 978, 982, 986, 996, 1002, 1012, 1015, 1020, 1033, 1037, 1042, 1068, 1070, 1081
- Coverage: the sample missed s2-probe-jako entirely. Lowest-numbered probe row **1085** (checked, marked "added for coverage", outside the rate calculation).
- Scoring: PASS 1, PARTIAL 0.5, FAIL 0 per check; N/A rows (documents, papers, advisories with no licence field to compare) are excluded from that check. Failure rate = 1 - mean score. Commands per row are in the table; GitHub rows use `gh api` (authenticated, `-X GET` where search), others use curl with User-Agent `resonantos-research`.
- Duplicate-check rule applied: same agent, same requirement, same canonical, both rows candidate/lead/excluded, identical result_url = FAIL; different result_url and no `duplicate` marker = PARTIAL; same canonical recorded by another agent with no row-level cross-reference = PARTIAL (brief: expected between agents). Counterexample rows beside a candidate row are not duplicates.
- Not done: stale-HEAD comparison. Most rows were written the same day, so `commit_sha_or_swhid` equals or trails HEAD by hours to days; that is not scored.

## Failure rates (sample of 110, row 1085 excluded)

| Check | PASS/PARTIAL/FAIL/N-A | Failure rate |
|---|---|---|
| URL resolves | 110/0/0/0 | 0.0% |
| Canonical source right | 107/3/0/0 | 1.4% |
| Licence right | 101/0/2/7 | 1.9% |
| Not an unmarked duplicate | 52/58/0/0 | 26.4% |

**Overall failure rate: 7.5%.** If the 46 cross-agent-only duplicate PARTIALs (expected between agents, no row can cross-reference another agent) are counted as PASS, the duplicate-check rate falls to 5.5% and overall to 2.2%.

Hard FAILs: 2 of 433 scored cells (both licence). No URL failures; no unmarked same-URL duplicates.

### Per agent (overall failure rate, then per check)

| Agent | Rows | URL | Canonical | Licence | Duplicate | Overall |
|---|---|---|---|---|---|---|
| s2-br-a | 11 | 0.0% | 4.5% | 0.0% | 27.3% | 8.0% |
| s2-br-b | 11 | 0.0% | 0.0% | 0.0% | 18.2% | 4.8% |
| s2-br-c | 11 | 0.0% | 0.0% | 0.0% | 40.9% | 10.5% |
| s2-br-d | 10 | 0.0% | 0.0% | 0.0% | 30.0% | 7.5% |
| s2-br-e | 14 | 0.0% | 3.6% | 0.0% | 21.4% | 6.5% |
| s2-br-f | 8 | 0.0% | 0.0% | 0.0% | 31.2% | 8.1% |
| s2-br-g | 4 | 0.0% | 12.5% | 0.0% | 25.0% | 9.4% |
| s2-br-h | 19 | 0.0% | 0.0% | 0.0% | 44.7% | 11.2% |
| s2-lang-de | 5 | 0.0% | 0.0% | 0.0% | 10.0% | 2.5% |
| s2-lang-fr | 6 | 0.0% | 0.0% | 20.0% | 0.0% | 4.3% |
| s2-lang-nl | 5 | 0.0% | 0.0% | 0.0% | 10.0% | 2.5% |
| s2-lang-zh | 6 | 0.0% | 0.0% | 16.7% | 8.3% | 6.2% |

Failures sit with: s2-lang-fr (row 986, licence), s2-lang-zh (row 1068, licence). PARTIALs on canonical: s2-br-a (row 80), s2-br-e (row 489), s2-br-g (row 681). Most duplicate PARTIALs are s2-br-c, s2-br-h, s2-br-f, s2-br-d (several candidate rows for one codebase, or the same codebase found by several branches).

### Extra check: candidate rows with `evidence_level: inspected`

26 sampled candidate rows. Not evidenced from the repository itself (scored outside the rate): row 304 (npm record for catp; tests empty, maintenance generic), row 423 (tuf-js npm row; both fields empty), row 552 (SAS npm row; "see repo row", registry date only), row 621 (idkit npm row; notes admit worldcoin/idkit was not opened; tests "not inspected"). Rows 6, 173 (web doc) and 505 (tests empty but commit date given) pass on a lenient reading.

## Sampled rows

| # | Agent | Req | result_url | URL | Canon | Licence | Dup | Reason | Command |
|---|---|---|---|---|---|---|---|---|---|
| 6 | br-a | R06 | https://github.com/vercel/ai/blob/main/content/docs/03-ai-sdk-core/16-mcp-tools.mdx | PASS | PASS | PASS | PARTIAL | dup: same agent and requirement, same canonical as row(s) 4,5 with different result_url, not marked duplicate | `gh api repos/vercel/ai/contents/content/docs/03-ai-sdk-core/16-mcp-tools.mdx; gh api repos/vercel/ai; /license; /commits?per_page=1` |
| 14 | br-a | R06 | https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/managing-tools/tool-permissions.md | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/aaif-goose/goose; /license; /commits?per_page=1` |
| 23 | br-a | R07 | https://github.com/deepseek-ai/deepseek-harness | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h,lang-zh; no row-level cross-reference (expected between agents) | `gh api repos/deepseek-ai/deepseek-harness; /license; /commits?per_page=1` |
| 33 | br-a | R07 | https://github.com/i-am-bee/acp | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2025-08-25, archived=True | `gh api repos/i-am-bee/acp; /license; /commits?per_page=1` |
| 37 | br-a | R08 | https://github.com/vercel/ai/tree/main/packages/anthropic | PASS | PASS | PASS | PARTIAL | dup: same agent and requirement, same canonical as row(s) 38,39 with different result_url, not marked duplicate | `gh api repos/vercel/ai/contents/packages/anthropic; gh api repos/vercel/ai; /license; /commits?per_page=1` |
| 49 | br-a | R08 | https://codeberg.org/jbousquie/llm-proxy | PASS | PASS | PASS | PASS | non-GitHub record read and matches | `curl codeberg.org/api/v1/repos/OWNER/REPO and /contents, /raw/LICENSE.md` |
| 66 | br-a | R29 | https://github.com/deepseek-ai/deepseek-harness | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h,lang-zh; no row-level cross-reference (expected between agents) | `gh api repos/deepseek-ai/deepseek-harness; /license; /commits?per_page=1` |
| 80 | br-a | R07 | https://github.com/advisories/GHSA-7h8w-hj9j-8rjw | PASS | PARTIAL | PASS | PASS | canon: advisory GHSA-7h8w-hj9j-8rjw belongs to OpenHands/OpenHands (package openhands-ai); canonical field holds software-agent-sdk, the candidate it is against | `gh api advisories/GHSA-7h8w-hj9j-8rjw` |
| 95 | br-a | R09 | https://github.com/agentskills/agentskills | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2026-08-09, archived=False | `gh api repos/agentskills/agentskills; /license; /commits?per_page=1` |
| 102 | br-a | R09 | https://github.com/jdutton/vibe-agent-toolkit | PASS | PASS | PASS | PASS | licence MIT (API MIT), HEAD 2026-10-11, archived=False | `gh api repos/jdutton/vibe-agent-toolkit; /license; /commits?per_page=1` |
| 104 | br-a | R08 | https://github.com/vercel/ai/blob/main/packages/ai/src/util/retry-with-exponential-backoff.test.ts | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/vercel/ai/contents/packages/ai/src/util/retry-with-exponential-backoff.test.ts; gh api repos/vercel/ai; /license; /commits?per_page=1` |
| 128 | br-b | R01 | https://github.com/ucan-wg/ts-ucan | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/ucan-wg/ts-ucan; /license; /commits?per_page=1` |
| 131 | br-b | R01 | https://github.com/apache/casbin-node-casbin | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2026-10-09, archived=False | `gh api repos/apache/casbin-node-casbin; /license; /commits?per_page=1` |
| 135 | br-b | R01 | https://github.com/advisories/GHSA-75rw-34q6-72cr | PASS | PASS | N/A | PARTIAL | lic: advisory row; no licence field applicable; dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api advisories/GHSA-75rw-34q6-72cr` |
| 168 | br-b | R04 | https://github.com/winsw/winsw | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/winsw/winsw; /license; /commits?per_page=1` |
| 173 | br-b | R05 | https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging | PASS | PASS | N/A | PASS | lic: web documentation page | `curl -sL URL, grep quoted claim` |
| 185 | br-b | R02 | https://github.com/Convira/convira-sandbox | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2026-08-08, archived=False | `gh api repos/Convira/convira-sandbox; /license; /commits?per_page=1` |
| 186 | br-b | R02 | https://github.com/yoke233/yj-sandbox | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2026-09-09, archived=False | `gh api repos/yoke233/yj-sandbox; /license; /commits?per_page=1` |
| 187 | br-b | R02 | https://github.com/yzyyohh/dsh-windows-sandbox-0xc0000142 | PASS | PASS | PASS | PASS | licence MIT (API MIT), HEAD 2026-09-15, archived=False | `gh api repos/yzyyohh/dsh-windows-sandbox-0xc0000142; /license; /commits?per_page=1` |
| 189 | br-b | R02 | https://www.nuget.org/packages/RestrictedProcess.NET | PASS | PASS | PASS | PASS | licence MIT (API MIT), HEAD 2026-08-25, archived=False | `curl api.nuget.org/v3-flatcontainer/ID/index.json and .nuspec` |
| 191 | br-b | R02 | https://www.nuget.org/packages/hhnl.ProcessIsolation | PASS | PASS | PASS | PASS | non-GitHub record read and matches | `curl api.nuget.org/v3-flatcontainer/ID/index.json and .nuspec` |
| 195 | br-b | R05 | https://github.com/tailscale/tailscale/blob/main/ipn/localapi/localapi.go | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-e; no row-level cross-reference (expected between agents) | `gh api repos/tailscale/tailscale; /license; /commits?per_page=1` |
| 226 | br-c | R10 | https://arxiv.org/abs/2608.03836 | PASS | PASS | N/A | PASS | lic: paper, no code | `curl export.arxiv.org/api/query?id_list=ID` |
| 234 | br-c | R11 | https://github.com/kanson1996/agent-audit-trail | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/kanson1996/agent-audit-trail; /license; /commits?per_page=1` |
| 238 | br-c | R11 | https://github.com/sigstore/sigstore-js | PASS | PASS | PASS | PARTIAL | dup: same agent and requirement, same canonical as row(s) 276,325 with different result_url, not marked duplicate | `gh api repos/sigstore/sigstore-js; /license; /commits?per_page=1` |
| 266 | br-c | R12 | https://github.com/helailiang/go-did-jwt-vp-demo | PASS | PASS | PASS | PASS | licence NOASSERTION (API None), HEAD 2025-07-07, archived=False | `gh api repos/helailiang/go-did-jwt-vp-demo; /license; /commits?per_page=1` |
| 284 | br-c | R10 | https://github.com/resonatehq/resonate/issues/1070 | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/resonatehq/resonate/issues/1070; gh api repos/resonatehq/resonate; /license; /commits?per_page=1` |
| 286 | br-c | R10 | https://github.com/vercel/workflow/issues/679 | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/vercel/workflow/issues/679; gh api repos/vercel/workflow; /license; /commits?per_page=1` |
| 298 | br-c | R12 | https://github.com/TrustVC/trustvc | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/TrustVC/trustvc; /license; /commits?per_page=1` |
| 304 | br-c | R11 | https://www.npmjs.com/package/@catp-protocol/cli | PASS | PASS | PASS | PARTIAL | dup: same agent and requirement, same canonical as row(s) 303,323 with different result_url, not marked duplicate | `curl registry.npmjs.org/PKG/latest` |
| 315 | br-c | R12 | https://github.com/Helixar-AI/HDP | PASS | PASS | PASS | PARTIAL | dup: same agent and requirement, same canonical as row(s) 316 with different result_url, not marked duplicate | `gh api repos/Helixar-AI/HDP; /license; /commits?per_page=1` |
| 322 | br-c | R11 | https://github.com/transparency-dev/tessera/blob/main/storage/posix/files.go | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/transparency-dev/tessera/contents/storage/posix/files.go; gh api repos/transparency-dev/tessera; /license; /commits?per_page=1` |
| 325 | br-c | R11 | https://github.com/sigstore/sigstore-js/blob/main/packages/verify/src/__tests__/tlog/merkle.test.ts | PASS | PASS | PASS | PARTIAL | dup: same agent and requirement, same canonical as row(s) 238,276 with different result_url, not marked duplicate | `gh api repos/sigstore/sigstore-js/contents/packages/verify/src/__tests__/tlog/merkle.test.ts; gh api repos/sigstore/sigstore-js; /license; /commits?per_page=1` |
| 332 | br-d | R14 | https://github.com/letta-ai/letta-code | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/letta-ai/letta-code; /license; /commits?per_page=1` |
| 349 | br-d | R14 | https://github.com/getzep/graphiti/security/advisories | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/getzep/graphiti/security-advisories; gh api repos/getzep/graphiti; /license; /commits?per_page=1` |
| 354 | br-d | R15 | https://www.npmjs.com/package/age-encryption | PASS | PASS | PASS | PARTIAL | dup: same agent and requirement, same canonical as row(s) 409 with different result_url, not marked duplicate | `curl registry.npmjs.org/PKG/latest` |
| 360 | br-d | R15 | https://github.com/cryptomator/cryptolib | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/cryptomator/cryptolib; /license; /commits?per_page=1` |
| 371 | br-d | R16 | https://github.com/evoluhq/evolu | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/evoluhq/evolu; /license; /commits?per_page=1` |
| 392 | br-d | R17 | https://github.com/huggingface/transformers.js | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/huggingface/transformers.js; /license; /commits?per_page=1` |
| 393 | br-d | R17 | https://github.com/qdrant/qdrant | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2026-10-05, archived=False | `gh api repos/qdrant/qdrant; /license; /commits?per_page=1` |
| 403 | br-d | R14 | https://github.com/google/git-appraise | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2023-08-12, archived=False | `gh api repos/google/git-appraise; /license; /commits?per_page=1` |
| 417 | br-d | R16 | https://github.com/ueberdosis/hocuspocus | PASS | PASS | PASS | PASS | licence MIT (API MIT), HEAD 2026-10-15, archived=False | `gh api repos/ueberdosis/hocuspocus; /license; /commits?per_page=1` |
| 419 | br-d | R17 | https://github.com/breuert/scrydb | PASS | PASS | PASS | PASS | licence MIT (API MIT), HEAD 2026-08-27, archived=False | `gh api repos/breuert/scrydb; /license; /commits?per_page=1` |
| 423 | br-e | R18 | https://www.npmjs.com/package/tuf-js | PASS | PASS | PASS | PARTIAL | dup: same agent and requirement, same canonical as row(s) 422,543 with different result_url, not marked duplicate | `curl registry.npmjs.org/PKG/latest` |
| 424 | br-e | R18 | https://github.com/freedomofpress/tuf-browser | PASS | PASS | PASS | PARTIAL | dup: same agent and requirement, same canonical as row(s) 544 with different result_url, not marked duplicate | `gh api repos/freedomofpress/tuf-browser; /license; /commits?per_page=1` |
| 429 | br-e | R18 | https://github.com/sigstore/sigstore-js/security/advisories/GHSA-52v5-jr5w-gjxr | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-c; no row-level cross-reference (expected between agents) | `gh api repos/sigstore/sigstore-js/security-advisories/GHSA-52v5-jr5w-gjxr` |
| 436 | br-e | R18 | https://github.com/theupdateframework/python-tuf | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2026-10-14, archived=False | `gh api repos/theupdateframework/python-tuf; /license; /commits?per_page=1` |
| 438 | br-e | R18 | https://github.com/theupdateframework/go-tuf | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2026-10-15, archived=False | `gh api repos/theupdateframework/go-tuf; /license; /commits?per_page=1` |
| 442 | br-e | R18 | https://code.visualstudio.com/docs/configure/extensions/extension-runtime-security | PASS | PASS | N/A | PASS | lic: web documentation page | `curl -sL URL, grep quoted claim` |
| 444 | br-e | R18 | https://github.com/mozilla/remote-settings | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2026-10-20, archived=False | `gh api repos/mozilla/remote-settings; /license; /commits?per_page=1` |
| 450 | br-e | R18 | https://github.com/obsidianmd/obsidian-releases | PASS | PASS | PASS | PASS | licence NOASSERTION (API None), HEAD 2026-10-20, archived=False | `gh api repos/obsidianmd/obsidian-releases; /license; /commits?per_page=1` |
| 456 | br-e | R19 | https://github.com/browser-use/browser-use | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/browser-use/browser-use; /license; /commits?per_page=1` |
| 458 | br-e | R19 | https://github.com/browserbase/stagehand | PASS | PASS | PASS | PASS | licence MIT (API MIT), HEAD 2026-10-20, archived=False | `gh api repos/browserbase/stagehand; /license; /commits?per_page=1` |
| 462 | br-e | R19 | https://github.com/askalf/browser-bridge | PASS | PASS | PASS | PASS | licence MIT (API MIT), HEAD 2026-10-19, archived=False | `gh api repos/askalf/browser-bridge; /license; /commits?per_page=1` |
| 489 | br-e | R20 | https://github.com/advisories/GHSA-9f65-56v6-gxw7 | PASS | PARTIAL | N/A | PASS | canon: canonical null while advisory source_code_location is github.com/anthropics/claude-code; lic: advisory row | `gh api advisories/GHSA-9f65-56v6-gxw7` |
| 505 | br-e | R21 | https://github.com/Aaronius/penpal | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/Aaronius/penpal; /license; /commits?per_page=1` |
| 524 | br-e | R19 | https://github.com/egoring/browser-guard-mcp | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by probe-jako; no row-level cross-reference (expected between agents) | `gh api repos/egoring/browser-guard-mcp; /license; /commits?per_page=1` |
| 547 | br-f | R22 | https://github.com/solana-program/token-2022 | PASS | PASS | PASS | PARTIAL | dup: same agent and requirement, same canonical as row(s) 548,633 with different result_url, not marked duplicate | `gh api repos/solana-program/token-2022; /license; /commits?per_page=1` |
| 552 | br-f | R22 | https://www.npmjs.com/package/@solana/attestation | PASS | PASS | PASS | PARTIAL | dup: same agent and requirement, same canonical as row(s) 551,624 with different result_url, not marked duplicate | `curl registry.npmjs.org/PKG/latest` |
| 564 | br-f | R22 | https://github.com/nborovic/metaplex-permanent-burn-delegate-bug-bounty | PASS | PASS | PASS | PASS | licence None (API None), HEAD 2024-10-14, archived=False | `gh api repos/nborovic/metaplex-permanent-burn-delegate-bug-bounty; /license; /commits?per_page=1` |
| 577 | br-f | R23 | https://github.com/decentralized-identity/veramo | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2026-10-06, archived=False | `gh api repos/decentralized-identity/veramo; /license; /commits?per_page=1` |
| 590 | br-f | R24 | https://github.com/Squads-Protocol/v4 | PASS | PASS | PASS | PARTIAL | dup: same agent and requirement, same canonical as row(s) 591,623,626 with different result_url, not marked duplicate | `gh api repos/Squads-Protocol/v4; /license; /commits?per_page=1` |
| 621 | br-f | R25 | https://www.npmjs.com/package/@worldcoin/idkit | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `curl registry.npmjs.org/PKG/latest` |
| 639 | br-f | R23 | https://github.com/OmniOneID/did-core-sdk-server | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by probe-jako; no row-level cross-reference (expected between agents) | `gh api repos/OmniOneID/did-core-sdk-server; /license; /commits?per_page=1` |
| 643 | br-f | R25 | https://arxiv.org/pdf/2011.02412 | PASS | PASS | N/A | PASS | lic: paper row | `curl export.arxiv.org/api/query?id_list=ID` |
| 654 | br-g | R26 | https://github.com/JoinColony/colonyNetwork | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/JoinColony/colonyNetwork; /license; /commits?per_page=1` |
| 657 | br-g | R12 | https://github.com/hypercerts-org/hypercerts-lexicon | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-h; no row-level cross-reference (expected between agents) | `gh api repos/hypercerts-org/hypercerts-lexicon; /license; /commits?per_page=1` |
| 661 | br-g | R28 | https://github.com/drips-network/contracts | PASS | PASS | PASS | PASS | licence GPL-3.0-only (API GPL-3.0), HEAD 2026-04-29, archived=False | `gh api repos/drips-network/contracts; /license; /commits?per_page=1` |
| 681 | br-g | R27 | https://arxiv.org/abs/2505.16068 | PASS | PARTIAL | PASS | PASS | canon: paper row names gitcoinco/easy-retro-pgf as canonical; the paper links no code (arXiv abstract page), repo is only the target of "against:" | `curl export.arxiv.org/api/query?id_list=ID` |
| 712 | br-h | R29 | https://github.com/nanobrowser/nanobrowser | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-e; no row-level cross-reference (expected between agents) | `gh api repos/nanobrowser/nanobrowser; /license; /commits?per_page=1` |
| 731 | br-h | R29 | https://github.com/langgenius/dify | PASS | PASS | PASS | PASS | licence OTHER:Dify Open Source License (Apache-2.0 with additional conditions) (API NOASSERTION), HEAD 2026-10-20, archived=False | `gh api repos/langgenius/dify; /license; /commits?per_page=1` |
| 749 | br-h | R30 | https://github.com/regent-protocol/regent-solana-programs | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-f; no row-level cross-reference (expected between agents) | `gh api repos/regent-protocol/regent-solana-programs; /license; /commits?per_page=1` |
| 752 | br-h | R29 | https://github.com/LibreChat-AI/LibreChat/security/advisories | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by lang-nl; no row-level cross-reference (expected between agents) | `gh api repos/LibreChat-AI/LibreChat/security-advisories; gh api repos/LibreChat-AI/LibreChat; /license; /commits?per_page=1` |
| 776 | br-h | R22 | https://github.com/solana-labs/solana-program-library | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-f; no row-level cross-reference (expected between agents) | `gh api repos/solana-labs/solana-program-library; /license; /commits?per_page=1` |
| 777 | br-h | R22 | https://github.com/solana-foundation/solana-attestation-service | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-f; no row-level cross-reference (expected between agents) | `gh api repos/solana-foundation/solana-attestation-service; /license; /commits?per_page=1` |
| 782 | br-h | R27 | https://github.com/privacy-ethereum/maci | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-g; no row-level cross-reference (expected between agents) | `gh api repos/privacy-ethereum/maci; /license; /commits?per_page=1` |
| 796 | br-h | R12 | https://github.com/ChartRunner/chartrunner-onchain | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-f; no row-level cross-reference (expected between agents) | `gh api repos/ChartRunner/chartrunner-onchain; /license; /commits?per_page=1` |
| 806 | br-h | R30 | https://github.com/gov4git/gov4git | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-g; no row-level cross-reference (expected between agents) | `gh api repos/gov4git/gov4git; /license; /commits?per_page=1` |
| 814 | br-h | R14 | https://github.com/NORTHTEKDevs/genome | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-d; no row-level cross-reference (expected between agents) | `gh api repos/NORTHTEKDevs/genome; /license; /commits?per_page=1` |
| 819 | br-h | R11 | https://github.com/pametan/audit-log | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-c; no row-level cross-reference (expected between agents) | `gh api repos/pametan/audit-log; /license; /commits?per_page=1` |
| 824 | br-h | R30 | https://github.com/sigstore/rekor-tiles | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2026-10-19, archived=False | `gh api repos/sigstore/rekor-tiles; /license; /commits?per_page=1` |
| 834 | br-h | R03 | https://github.com/Brooooooklyn/keyring-node | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-b,br-d; no row-level cross-reference (expected between agents) | `gh api repos/Brooooooklyn/keyring-node; /license; /commits?per_page=1` |
| 864 | br-h | R08 | https://github.com/maximhq/bifrost | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-a; no row-level cross-reference (expected between agents) | `gh api repos/maximhq/bifrost; /license; /commits?per_page=1` |
| 875 | br-h | R15 | https://github.com/FiloSottile/typage | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-d; no row-level cross-reference (expected between agents) | `gh api repos/FiloSottile/typage; /license; /commits?per_page=1` |
| 891 | br-h | R16 | https://github.com/automerge/automerge | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-d; no row-level cross-reference (expected between agents) | `gh api repos/automerge/automerge; /license; /commits?per_page=1` |
| 900 | br-h | R17 | https://github.com/tobi/qmd | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-d; no row-level cross-reference (expected between agents) | `gh api repos/tobi/qmd; /license; /commits?per_page=1` |
| 910 | br-h | R10 | https://github.com/resonatehq/resonate-sdk-ts | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-c; no row-level cross-reference (expected between agents) | `gh api repos/resonatehq/resonate-sdk-ts; /license; /commits?per_page=1` |
| 911 | br-h | R10 | https://github.com/RaycarlLei/tool-journal | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-c; no row-level cross-reference (expected between agents) | `gh api repos/RaycarlLei/tool-journal; /license; /commits?per_page=1` |
| 919 | lang-de | R07 | https://gitlab.opencode.de/public-sector-dev-crew/lotse/bootsmann | PASS | PASS | PASS | PASS | non-GitHub record read and matches | `curl https://gitlab.opencode.de/api/v4/projects/NS%2FREPO?license=true and /repository/tree` |
| 924 | lang-de | R11 | https://gitlab.opencode.de/bmi/eudi-wallet/relying-party-registrar | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-f; no row-level cross-reference (expected between agents) | `curl https://gitlab.opencode.de/api/v4/projects/NS%2FREPO?license=true and /repository/tree` |
| 931 | lang-de | R03 | https://helmholtz.software/software/oidc-agent | PASS | PASS | PASS | PASS | licence MIT (API MIT), HEAD 2026-10-07, archived=False | `curl -sL URL; gh api repos/indigo-dc/oidc-agent` |
| 938 | lang-de | R30 | https://gitlab.opencode.de/open-government-community-builder/OGCB | PASS | PASS | PASS | PASS | non-GitHub record read and matches | `curl https://gitlab.opencode.de/api/v4/projects/NS%2FREPO?license=true and /repository/tree` |
| 942 | lang-de | R02 | https://gitlab.gwdg.de/glissmann/sandbox-agent | PASS | PASS | PASS | PASS | non-GitHub record read and matches | `curl https://gitlab.gwdg.de/api/v4/projects/NS%2FREPO?license=true and /repository/tree` |
| 951 | lang-fr | R06 | https://github.com/gilmry/sluis | PASS | PASS | PASS | PASS | licence MIT (API MIT), HEAD 2026-10-19, archived=False | `gh api repos/gilmry/sluis; /license; /commits?per_page=1` |
| 954 | lang-fr | R03 | https://github.com/xtrem21-source/ApiVault_Proxy | PASS | PASS | PASS | PASS | licence MIT (API MIT), HEAD 2026-10-19, archived=False | `gh api repos/xtrem21-source/ApiVault_Proxy; /license; /commits?per_page=1` |
| 975 | lang-fr | R25 | https://hal.science/hal-05644727 | PASS | PASS | N/A | PASS | lic: paper record on HAL | `curl api.archives-ouvertes.fr/search/?q=halId_s:hal-05644727` |
| 978 | lang-fr | R10 | https://github.com/kestra-io/kestra | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2026-10-20, archived=False | `gh api repos/kestra-io/kestra; /license; /commits?per_page=1` |
| 982 | lang-fr | R02 | https://github.com/GreyhavenHQ/greywall/issues/55 | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2026-08-13, archived=False | `gh api repos/GreyhavenHQ/greywall/issues/55; gh api repos/GreyhavenHQ/greywall; /license; /commits?per_page=1` |
| 986 | lang-fr | R06 | https://github.com/Roscpy/server-mcp | PASS | PASS | FAIL | PASS | lic: license_code "MIT OR Apache-2.0" but repo has no LICENSE file (contents: .github, Cargo.toml, README.md, src ...); only Cargo.toml and README declare it; row notes disclose this, SCHEMA says NOASSERTION | `gh api repos/Roscpy/server-mcp; /license; /commits?per_page=1` |
| 996 | lang-nl | R11 | https://github.com/oomny-nl/agent-levenscyclus | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-c,br-e,br-f,br-h; no row-level cross-reference (expected between agents) | `gh api repos/oomny-nl/agent-levenscyclus; /license; /commits?per_page=1` |
| 1002 | lang-nl | R01 | https://gitlab.com/rinis-oss/fsc/open-fsc | PASS | PASS | PASS | PASS | non-GitHub record read and matches | `curl https://gitlab.com/api/v4/projects/NS%2FREPO?license=true and /repository/tree` |
| 1012 | lang-nl | R23 | https://oss.developer.overheid.nl/repositories?q=wallet&publiccode=false | PASS | PASS | PASS | PASS | licence NOASSERTION (API NOASSERTION), HEAD 2023-03-17, archived=False | `curl -sIL URL; gh api repos/SURFnet/SURF-SSI-wallet-app` |
| 1015 | lang-nl | R04 | https://code.overheid.nl/MinBZK/DAWO-Sextant | PASS | PASS | PASS | PASS | non-GitHub record read and matches | `curl code.overheid.nl/api/v1/repos/MinBZK/DAWO-Sextant (+raw/LICENSE)` |
| 1020 | lang-nl | R11 | https://github.com/WimLee115/dpo-fg-tool/tree/main/crates/dpofg-audit | PASS | PASS | PASS | PASS | licence OTHER:all-rights-reserved (API NOASSERTION), HEAD 2026-08-21, archived=False | `gh api repos/WimLee115/dpo-fg-tool/contents/crates/dpofg-audit; gh api repos/WimLee115/dpo-fg-tool; /license; /commits?per_page=1` |
| 1033 | lang-zh | R02 | https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md | PASS | PASS | PASS | PARTIAL | dup: same canonical also recorded by br-a,br-h; no row-level cross-reference (expected between agents) | `gh api repos/deepseek-ai/deepseek-harness/contents/SAFETY.md; gh api repos/deepseek-ai/deepseek-harness; /license; /commits?per_page=1` |
| 1037 | lang-zh | R02 | https://github.com/xcanwin/manyoyo | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2026-10-18, archived=False | `gh api repos/xcanwin/manyoyo; /license; /commits?per_page=1` |
| 1042 | lang-zh | R08 | https://github.com/wanghr0318-dotcom/deepresearch-sandbox-go-python | PASS | PASS | PASS | PASS | licence MIT (API MIT), HEAD 2026-10-12, archived=False | `gh api repos/wanghr0318-dotcom/deepresearch-sandbox-go-python; /license; /commits?per_page=1` |
| 1068 | lang-zh | R13 | https://github.com/Tencent/MMKV | PASS | PASS | FAIL | PASS | lic: license_code NOASSERTION but LICENSE.TXT exists and says BSD 3-Clause (with third-party exceptions); notes say "not verified" | `gh api repos/Tencent/MMKV; /license; /commits?per_page=1` |
| 1070 | lang-zh | R19 | https://github.com/bytedance/UI-TARS-desktop | PASS | PASS | PASS | PASS | licence Apache-2.0 (API Apache-2.0), HEAD 2026-10-09, archived=False | `gh api repos/bytedance/UI-TARS-desktop; /license; /commits?per_page=1` |
| 1081 | lang-zh | R04 | https://github.com/pandarayc/dsh-release-guard | PASS | PASS | PASS | PASS | licence MIT (API MIT), HEAD 2026-08-17, archived=False | `gh api repos/pandarayc/dsh-release-guard; /license; /commits?per_page=1` |
| 1085 (added for coverage) | probe-jako | R11 | https://github.com/totsuka-code/checksum-registry | PASS | PASS | PASS | PASS | licence NOASSERTION (API None), HEAD 2026-02-21, archived=False | `gh api repos/totsuka-code/checksum-registry; /license; /commits?per_page=1` |

Notes on specific verdicts: GitHub reports NOASSERTION for vercel/ai (rows 6, 37, 104) and gov4git (806), but the LICENSE text is Apache-2.0 and dual MIT/Apache-2.0 respectively, so the row values are right. Row 752 (LibreChat-AI/LibreChat): the old danny-avila/LibreChat name now resolves to the same repository. Row 14/66: block/goose redirects to aaif-goose/goose. Rows 49/1002: Codeberg and GitLab APIs read; llm-proxy LICENSE.md is Licence Ouverte 2.0 and the rflores copy is a fork correctly named as a mirror.

## Shortlist full check (16 codebases, outside the rate)

Per codebase: canonical URL resolves via `gh api repos/OWNER/REPO` and is the upstream; licence read via `gh api repos/OWNER/REPO/license` and the file; recorded SHA fetched with `gh api repos/OWNER/REPO/commits/SHA`; releases via `gh api repos/OWNER/REPO/releases?per_page=1` and registry JSON; archived flag and HEAD date from the repo object.

| codebase_id | Upstream (not mirror) | Licence file vs license_code | SHA exists / release | Archived, last commit | Verdict |
|---|---|---|---|---|---|
| eclipse-biscuit-biscuit-rust | yes (crates.io repository field still names old org biscuit-auth/biscuit-rust, redirects) | Apache-2.0 matches biscuit-auth/LICENSE; no LICENSE at repo root, GitHub shows no licence; not flagged | 93832a8 exists, = HEAD (2026-10-08); crates.io biscuit-auth 6.0.0 2025-07-16 matches | no; 2026-10-08 | PARTIAL |
| eclipse-biscuit-biscuit-wasm | yes | Apache-2.0 matches | 80cceed exists, = HEAD; npm @biscuit-auth/biscuit-wasm 0.6.0 2025-09-26 confirmed; no GitHub releases | no; 2026-07-13 | PASS |
| anthropics-sandbox-runtime | yes | Apache-2.0 matches | c40cf14 exists, = HEAD; release v0.0.81 2026-10-20 matches | no; 2026-10-20 | PASS |
| convira-convira-sandbox | yes | Apache-2.0 matches | 9013c32 exists, = HEAD; no releases (row null, correct) | no; 2026-08-08 | PASS |
| getaegis-aegis | yes | Apache-2.0 matches | f1321b3 exists, = HEAD; v1.0.5 2026-08-06 matches | no; 2026-08-06 | PASS |
| dapr-durabletask-go | NO: dapr/durabletask-go is a fork of microsoft/durabletask-go (diverged: 333 ahead, 37 behind; microsoft has v1.0.0-beta3 2026-10-12, dapr v0.15.1). Source row 311 names microsoft as upstream; codebases dedup_notes does not | Apache-2.0 matches | a89450a exists (2026-10-12); v0.15.1 2026-10-19 matches | no; 2026-10-12 | PARTIAL |
| openworkflowdev-openworkflow | yes | Apache-2.0 matches (LICENSE.md) | c82fbed exists, = HEAD; release tag matches | no; 2026-10-19 | PASS |
| holepunchto-hypercore | yes | MIT matches | 9c9cc3d exists, = HEAD; v11.39.0 2026-10-14 matches | no; 2026-10-14 | PASS |
| transparency-dev-tessera | yes | Apache-2.0 matches | 012e9e0 exists, = HEAD; v1.0.4 2026-07-16 matches | no; 2026-10-19 | PASS |
| openwallet-foundation-labs-identity-common-ts | yes | Apache-2.0 matches (monorepo root; per-package licences not opened) | 42586ca exists, = HEAD; v0.5.0 2026-10-17 matches | no; 2026-10-19 | PASS |
| datalad-datalad | yes | MIT matches COPYING, but COPYING has a "3rd Party Code" section (Python licence, BSD-2, BSD-3 parts); GitHub SPDX NOASSERTION; license_flags empty | 77de8d9 exists, = HEAD; 1.7.1 2026-10-06 matches | no; 2026-10-14 | PARTIAL |
| theupdateframework-tuf-js | yes | MIT matches | a399ce8 exists, = HEAD; tuf-js 6.0.0 2026-06-01 matches | no; 2026-06-02 | PASS |
| nanobrowser-nanobrowser | yes | Apache-2.0 matches | f1e912d exists, = HEAD; v0.3.0 2026-10-15 matches | no; 2026-10-15 | PASS |
| solana-foundation-rewards | yes | MIT matches | 0b1bf17 exists, = HEAD; no tagged release (row says so) | no; 2026-10-05 | PASS |
| hypercerts-org-hypercerts-lexicon | yes | MIT matches | db1f41c exists, = HEAD; v1.5.1 2026-10-14 matches | no; 2026-10-14 | PASS |
| aaif-goose-goose | yes (block/goose redirects here) | Apache-2.0 matches | 9920efa exists, = HEAD; v1.55.0 2026-10-16 matches | no; 2026-10-20 | PASS |

Summary: **13 PASS, 3 PARTIAL (biscuit-rust licence location, dapr-durabletask-go fork, datalad third-party code), 0 FAIL.** No archived repo, every recorded SHA exists, every canonical URL resolves, every license_code matches the licence file at HEAD.

## Corrections for the lead to send back

| # | Agent | Row / codebase | Field | Current | Correct | Evidence |
|---|---|---|---|---|---|---|
| 1 | s2-lang-fr | row 986 github.com/Roscpy/server-mcp (also row 950 same repo) | license_code | MIT OR Apache-2.0 | NOASSERTION (keep the Cargo.toml/README declaration in notes) | `gh api repos/Roscpy/server-mcp/contents` lists no LICENSE, LICENSE-MIT or LICENSE-APACHE; Cargo.toml line 5 `license = "MIT OR Apache-2.0"`; SCHEMA: NOASSERTION if no licence file |
| 2 | s2-lang-zh | row 1068 github.com/Tencent/MMKV | license_code | NOASSERTION | BSD-3-Clause (flag: third-party components under other terms) | `gh api repos/Tencent/MMKV/contents/LICENSE.TXT`: source "is licensed under the BSD 3-Clause License, except for the third-party components" |
| 3 | s2-br-a | row 80 GHSA-7h8w-hj9j-8rjw | canonical_source_url | https://github.com/OpenHands/software-agent-sdk | https://github.com/OpenHands/OpenHands (keep the SDK only in the `against:` text) | `gh api advisories/GHSA-7h8w-hj9j-8rjw` source_code_location = OpenHands/OpenHands, package openhands-ai |
| 4 | s2-br-e | row 489 GHSA-9f65-56v6-gxw7 | canonical_source_url | null | https://github.com/anthropics/claude-code | `gh api advisories/GHSA-9f65-56v6-gxw7` source_code_location = anthropics/claude-code |
| 5 | s2-br-g | row 681 arXiv 2505.16068 | canonical_source_url | https://github.com/gitcoinco/easy-retro-pgf | null (the paper links no code; keep easy-retro-pgf in the `against:` text) | arXiv API for 2505.16068 shows no code link; row notes say no repository is linked |
| 6 | s2-prov (codebases.jsonl) | dapr-durabletask-go | dedup_notes / license_flags | 3 source records merged (github) | Add: fork of microsoft/durabletask-go, diverged (dapr +333, -37); microsoft HEAD 2026-10-12 and v1.0.0-beta3; Stage 3 should state which tree it inspects | `gh api repos/dapr/durabletask-go` parent=microsoft/durabletask-go; `gh api repos/dapr/durabletask-go/compare/microsoft:main...main` status diverged |
| 7 | s2-prov (codebases.jsonl) | eclipse-biscuit-biscuit-rust | license_flags | [] | Licence file lives at biscuit-auth/LICENSE only; repo root has none and GitHub reports no licence | `gh api repos/eclipse-biscuit/biscuit-rust/license` 404; `.../contents/biscuit-auth/LICENSE` is Apache-2.0 |
| 8 | s2-prov (codebases.jsonl) | datalad-datalad | license_flags | [] | MIT with a 3rd-party code section in COPYING (Python licence, BSD-2, BSD-3 parts); GitHub SPDX NOASSERTION | `gh api repos/datalad/datalad/contents/COPYING` lines 32-47 |
| 9 | s2-br-c / s2-br-e / s2-br-f | rows 304, 423, 552, 621 | evidence_level | inspected | reported (or open the repository and fill tests_or_benchmarks / maintenance from it) | tests and maintenance fields are empty, "see repo row" or registry-date only; row 621 notes say the repository was not opened |
| 10 | s2-br-a, s2-br-c, s2-br-d, s2-br-f | rows 4/5/6, 37/38/39, 238/276/325, 303/304/323, 315/316, 354/409, 547/548/633, 551/552/624, 590/591/623/626 | disposition | several `candidate` rows per codebase and requirement, different result_url | mark the extra records `duplicate` of the primary record (or merge them in codebases.jsonl so candidate counts per requirement are not inflated) | rows share requirement_id and canonical_source_url within one agent |

Total corrections proposed: 10.

## Worst findings

1. Row 986 (s2-lang-fr, Roscpy/server-mcp): a licence string recorded where no LICENSE file exists; the agent noted it in prose but the field stays "MIT OR Apache-2.0".
2. Row 1068 (s2-lang-zh, Tencent/MMKV): NOASSERTION recorded although LICENSE.TXT is plainly BSD-3-Clause; notes admit it was not verified.
3. Shortlist: dapr/durabletask-go is a diverged fork recorded as canonical without that being stated in codebases.jsonl; plus the licence-file location (biscuit-rust) and third-party code section (datalad) are unflagged.

Also: the duplicate check is where most credit is lost (cross-agent overlap is widespread: 46 of 110 sampled rows have the same canonical in another agent's ledger, and 12 have several candidate rows from one agent), which is a counting problem for candidate tallies, not a correctness problem for the data.
