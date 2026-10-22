# Evidence appendix

Companion to `ARTICLE.md`. Every path is relative to `research/`. Dates are access dates in Europe/Berlin time. Nothing third-party was executed anywhere in this research (master prompt section 9; user decision D4.0 (4)).

## A. Source index

### A.1 Project sources (Stage 1)

| Source | Identity | Accessed | Where recorded |
|---|---|---|---|
| ResonantOS/2.0.0-alpha | commit `578fbbc3c1c854b192318b3d2163b138fb45d8bd`, branch `dev`, 2026-10-18; read-only clone under `_untrusted/resonantos-2.0.0-alpha` | 2026-10-20 | `stage1/os-map.md`, `stage1/capability-matrix.md` (63 rows), `stage1/verification.md` |
| CI for that commit | `alpha-build` run 39097845387 (success, 17 `verify:alpha` lanes, vitest 724), `agent-control-live` run 39225094790 (success); read through the GitHub Actions API | 2026-10-20 | `stage1/verification.md` line 5 |
| The other seven ResonantOS repositories and the two official-adjacent ones | census rows with contributor, fork, issue and PR counts from the API | 2026-10-20 | `stage1/census.jsonl` (23 rows), `stage1/census-notes.md`, `stage1/sources/census/` |
| Branch and tag history, ADR index, website claims | 16 registered discrepancies | 2026-10-20 | `stage1/timeline.md` |
| resonantdao.com whitepaper v0.6 (2026-08-30), Contribution Economy v2, membership portal, Symbiotic Licence (404), three cited architecture documents (404) | WebFetch summaries | 2026-10-20 | `stage1/sources/lead/*.md`, `stage1/dao-requirements.md` (DR-01 to DR-62, 17 inconsistencies) |
| Solana devnet and mainnet reads (mints, program, upgrade authority) | public RPC, one call each, two agents | 2026-10-20 and 2026-10-21 | `stage1/dao-requirements.md` section 8; `dossiers/realms-spl-governance.md`, `dossiers/solana-foundation-rewards.md` |

### A.2 Inspected codebases (Stage 3), pinned commits

| Dossier | Upstream and commit | Version | Accessed | Citation check |
|---|---|---|---|---|
| `dossiers/eclipse-biscuit.md` | eclipse-biscuit/biscuit-rust `93832a8`; biscuit-wasm `80cceed` | npm `@biscuit-auth/biscuit-wasm` 0.6.0 | 2026-10-20 | archaeologist pass |
| `dossiers/anthropics-sandbox-runtime.md` | anthropics/sandbox-runtime `c40cf14a65d025e3cd27f071f13a73c12b3b1f92` | v0.0.81, npm 0.0.81 (2026-10-20) | 2026-10-20 | pass |
| `dossiers/convira-sandbox.md` | Convira/convira-sandbox `9013c323725155f1e2e3e95c597715c172dff0c1` | no release; HEAD 2026-08-08 | 2026-10-20 | pass |
| `dossiers/getaegis-aegis.md` | getaegis/aegis `f1321b3` | v1.0.5 | 2026-10-20 | pass |
| `dossiers/dapr-durabletask-go.md` | dapr/durabletask-go `a89450a` (fork of microsoft/durabletask-go, 333 ahead, 37 behind) | v0.15.1 | 2026-10-20 | pass |
| `dossiers/openworkflow.md` | openworkflowdev/openworkflow `c82fbed` | 0.11.0 | 2026-10-20 | pass |
| `dossiers/holepunchto-hypercore.md` | holepunchto/hypercore `9c9cc3d` | 11.39.0 | 2026-10-20 | pass |
| `dossiers/transparency-dev-tessera.md` | transparency-dev/tessera `012e9e0821ec2ade495d32c9c9a3f08bd348ff7d` (main HEAD, 2026-10-19); witness, merkle, formats, C2SP specs at the SHAs in the dossier | latest release v1.0.4 = `6bca8e8d` (2026-07-16); the recommendation pins v1.0.4 | 2026-10-20 | pass |
| `dossiers/identity-common-ts.md` | openwallet-foundation-labs/identity-common-ts `42586ca` | `@sd-jwt/*` 0.23.0, token-status-list 0.5.0 | 2026-10-21 | pass |
| `dossiers/datalad.md` | datalad/datalad `77de8d9` | 1.7.1 | 2026-10-21 | pass (one FAIL fixed) |
| `dossiers/tuf-js.md` | theupdateframework/tuf-js `a399ce8` | 6.0.0; tuf-conformance v2.4.0 in its own CI (run 39558085285: 107 passed, 1 expected failure); v2.5.0 not run | 2026-10-21 | pass |
| `dossiers/nanobrowser.md` | nanobrowser/nanobrowser `f1e912d` | v0.3.0 | 2026-10-20 | pass |
| `dossiers/solana-foundation-rewards.md` | solana-foundation/rewards audited `aa1cfd9`, HEAD `0b1bf17`, unmerged Points branch | mainnet program and Squads vault read by RPC | 2026-10-21 | pass |
| `dossiers/hypercerts-lexicon.md` | hypercerts-org/hypercerts-lexicon `db1f41c` | v1.5.1 | 2026-10-21 | pass |
| `dossiers/aaif-goose.md` | aaif-goose/goose `9920efa` | v1.55.0 | 2026-10-21 | pass |
| `dossiers/realms-spl-governance.md` | Mythic-Project/solana-program-library (governance) `00fa982`; governance-program-library `1abc998`; Squads-Protocol/v4 `af94153`; shared instance `GovER5...` read by RPC | spl-governance 3.1.3 public, 3.1.7 deployed | 2026-10-21 | 23 PASS, 1 PARTIAL of 24 |

Every dossier has fourteen sections, a section 11 with execution requests (none run) and a review-response section after the Stage 3 adversarial reviews (`reviews/security-engineer.md`, `reviews/code-archaeologist.md`, `reviews/dao-skeptic.md`, `reviews/dao-skeptic-r24.md`; amendments per `reviews/BRIEF-stage3-amend.md`).

### A.3 Research artefacts

`stage1/gaps.md` (R01-R30), `stage1/interaction.md` (invariants, exchanges, consent tiers), `stage1/gate1-report.md`, `ledger/gate2-report.md`, `reviews/gate3-report.md`, `ledger/threat-model-draft.md` (v0.2.1; v0.1 kept as `threat-model-draft-v0.1.md`), `scoring/weights.json` (profiles fixed 2026-10-20 before any dossier), `scoring/scores.csv`, `scoring/sensitivity.py` and `sensitivity-output.md`, `scoring/whatif.py` and `whatif-output.md`, `architecture/decisions.md`, `architecture/reference-architectures.md`, `architecture/risk-register.md`, `architecture/governance-checklists.md`, `architecture/acceptance-backlog.md`, `state.md` (decision log D0.1 to D5.5; ids appear in the order they were written, not sorted), `PLAN.md` (agent rosters), `lessons/`.

## B. Coverage matrix (final quality gate, master prompt 8.6)

Full tables: `ledger/coverage-matrix.md` (FINAL v3, 2026-10-21; 1,155 discovery rows, 1,298 negative rows, 13 ledger pairs, 586 unique codebases). A purposeful search is a distinct (platform, language, requirement, query). Each platform from master prompt sections 4.1 and 4.2 is listed; none was skipped.

### B.1 Global platforms (4.1)

| Platform | Searches | Languages | Codebases / candidates | Outcome and limits |
|---|---|---|---|---|
| GitHub | 1,318 | de, en, fr, ja, ko, nl, zh | 426 / 159 | carried the load; 30-per-minute search quota hit repeatedly, retried; `gh api -X GET` needed for search |
| GitLab (gitlab.com) | 25 | en, fr, nl | 6 / 1 | one endpoint failure; self-hosted instances counted separately below |
| Codeberg | 50 | de, en, fr, nl | 3 / 1 | mostly empty |
| SourceForge | 5 | en | 2 / 0 | stale snapshots, name collisions |
| Hugging Face (models, datasets, Spaces) | 10 | en, zh | 5 / 3 | the two attack benchmarks for R19 |
| arXiv | 42 | en | 14 / 0 | API returned 429 all day for every agent (shared egress); OpenAlex and HF Papers substituted |
| ACL Anthology | 4 | en | 0 / 0 | client-rendered search, unusable without a browser; documented no-result |
| Papers with Code (archived) | substituted by HF Papers: 18 | en | 10 / 0 | substitution recorded per the master prompt |
| PyPI | 7 | en, ja, ko | 7 / 2 | - |
| npm | 65 | en, zh | 43 / 31 | second source of candidates |
| crates.io | 6 | en | 5 / 3 | - |
| Go modules | 2 | en | 2 / 2 | Go candidates were found on GitHub first |
| Maven Central | 11 | en | 3 / 0 | search timed out on most calls; index lags GitHub |
| NuGet | 14 | en | 7 / 0 | Windows AppContainer libraries and the Durable Task engine as leads |
| Software Heritage | 3 | en | 1 / 0 | no snapshot of any ResonantOS repository |
| Zenodo | 12 | en | 5 / 1 | - |
| OpenAlex (aid) | 7 | en | 3 / 0 | shared daily budget notice in pass 2 |
| Semantic Scholar (aid) | 6 | en | 0 / 0 | anonymous rate limit; blocked |

### B.2 Regional and language platforms (4.2)

| Platform | Searches | Languages | Codebases / candidates | Outcome and limits |
|---|---|---|---|---|
| Gitee | 11 | zh | 2 / 0 | repository search closed to anonymous callers; lookup by name works; blocked recorded |
| GitCode (AtomGit) | 14 | zh | 4 / 1 | API needs a token (401); web pages fetched; openEuler governance found |
| OpenI | 2 | zh | 0 / 0 | agreement gate, not bypassed |
| CNKI | 2 | zh | 0 / 0 | host unreachable; overseas mirror returns nothing |
| Juejin, CSDN, Zhihu, ithome (as `web`) | within 132 web searches | zh | leads only | several CSDN pages 403 to the fetcher |
| Framagit | 94 | en, fr | 3 / 0 | mostly irrelevant |
| code.gouv.fr | 63 | fr | 2 / 1 | inventory data file dated 2024-09-18 |
| HAL | 122 | en, fr | 8 / 0 | HTML bot-walled, API works; Belenios papers |
| openCode.de | 110 | de, en | 15 / 1 | code search inside a project needs login; EUDI registrar and public-sector audit work |
| Helmholtz RSD | 30 | de, en | 3 / 0 (Terok counted under GitHub) | English-only index; the Terok route |
| University and institute GitLabs | 108 | de, en, fr, nl | 4 / 0 | one bot wall, one rate limit; gitlab.inria.fr hosts Belenios |
| Research Software Directory (NL) | 49 | en, nl | 2 / 0 | English-only |
| 4TU.ResearchData | 23 | en, nl | 2 / 0 | description search times out after 20 s |
| developer.overheid.nl | 50 | en, nl | 2 / 0 | the route to Yivi irmago |
| Qiita, Zenn, J-STAGE (probe) | 16 | ja | 3 / 0 | commentary on English tools; no institutional code |
| KCI (probe) | 7 | ko | 1 / 0 | papers without code links |

Language by requirement: no unexplored cell for English, Chinese, French or German; Dutch has one (R20); Japanese 22 and Korean 21 by decision D2.1 (probe tripwire did not fire; reversal condition recorded in `glossary/ja-ko-probe.md`). Thinnest requirements after dedup, four candidates each: R13, R22, R24, R25, R27.

### B.3 Representative queries per platform

Two or three exact `search_terms_or_query` values per platform, chosen to show different languages where they were used, with the ledger kind (discovery = a result was recorded; negative = an empty, irrelevant or blocked search). The full list is in the 26 JSONL ledgers; counts in B.1 and B.2.

| Platform | Language | Query (verbatim from the ledger) | Kind |
|---|---|---|---|
| 4tu | en | POST https://data.4tu.nl/v2/articles/search {"search_for":":title: reputation"} ; DataCite API for the DOI | discovery |
| 4tu | nl | POST https://data.4tu.nl/v2/articles/search {"search_for":":title: mandaat","page_size":8} | negative |
| acl | en | https://aclanthology.org/search/?q=human-in-the-loop tool use agent | negative |
| acl | en | https://aclanthology.org/search/?q=agent tool approval permission | negative |
| arxiv | en | OpenAlex works?search=agent interoperability protocol A2A MCP survey; then https://arxiv.org/abs/2603.24775 | discovery |
| arxiv | en | OpenAlex works?search=agent interoperability protocol A2A MCP survey; then https://arxiv.org/abs/2606.31498 | discovery |
| cnki | zh | https://kns.cnki.net/kns8s/defaultresult/index?kw=智能体 溯源 审计 | negative |
| cnki | zh | 智能体 溯源 审计 (native-language R12 request from Branch C) | negative |
| codeberg | de | GET https://codeberg.org/api/v1/repos/search?q=KI-Agenten%20Sandbox&limit=12&sort=updated | negative |
| codeberg | en | https://codeberg.org/api/v1/repos/search?q=crdt | discovery |
| codeberg | fr | GET https://codeberg.org/api/v1/repos/search?q=llm-proxy&limit=6&sort=updated | discovery |
| codegouvfr | fr | python -I filter of code.gouv.fr/data/repositories.json (stale 2024-09-18) with regex 'rust.*(secure\|memory)\|...'; gh api repos/cea-sec/usbsas | discovery |
| codegouvfr | fr | python -I regex over code.gouv.fr repositories.json 'encrypt\|chiffr\|\bage\b\|keepass\|keyring\|libsodium\|gpg\|pgp'; gh api repos/ANSSI-FR/MLA | discovery |
| crates | en | https://crates.io/api/v1/crates?q=age encryption rage | discovery |
| crates | en | https://crates.io/api/v1/crates?q=keyring | discovery |
| dev-overheid | en | GET https://oss.developer.overheid.nl/repositories?q=ledger&publiccode=false | negative |
| dev-overheid | nl | https://oss.developer.overheid.nl/repositories?q=wallet&publiccode=false | discovery |
| framagit | en | GET https://framagit.org/api/v4/projects?search=macaroon and search=biscuit | negative |
| framagit | fr | https://framagit.org/api/v4/projects?search=local-first | discovery |
| gitcode | zh | https://gitcode.com/search?q=持久化执行&type=repo (WebFetch, 21 results) | discovery |
| gitcode | zh | WebFetch https://gitcode.com/openJiuwen/agent-protocol | discovery |
| gitee | zh | GET https://gitee.com/api/v5/repos/NanmiCoder/cc-haha (resolve by name after GitHub discovery, per lessons/regional-platform-access.md) | discovery |
| gitee | zh | GET https://gitee.com/api/v5/repos/openeuler/community (403); GET https://gitee.com/openeuler/community/raw/master/LICENSE | discovery |
| github | de | gh api -X GET search/repositories -f q="MCP Server Freigabe" | discovery |
| github | en | gh api search/repositories -f q="modelcontextprotocol typescript sdk"; gh api repos/modelcontextprotocol/typescript-sdk | discovery |
| github | fr | WebSearch linuxfr.org 'sandboxer agents IA bubblewrap Landlock' -> LinuxFr news 'J'ai mis un proxy entre claude et Internet' -> repo; gh api repos/... | discovery |
| gitlab | en | GET https://gitlab.com/api/v4/projects?search=transparency%20log&order_by=last_activity_at ; project API, tree and README | discovery |
| gitlab | fr | GET https://gitlab.inria.fr/api/v4/projects/belenios%2Fbelenios (+ tree, README, COPYING) | discovery |
| gitlab | nl | GET https://gitlab.com/api/v4/groups/digilab.overheid.nl%2Fecosystem%2Flogboek-dataverwerkingen/projects?include_subgroups=true ; /projects/ldv-ref... | discovery |
| go | en | GET https://proxy.golang.org/github.com/maximhq/bifrost/core/@latest | discovery |
| go | en | GET https://proxy.golang.org/github.com/transparency-dev/tessera/@latest | discovery |
| hal | en | https://api.archives-ouvertes.fr/search/?q="CRDT" encryption&fq=producedDate_s:[2021 TO *] | discovery |
| hal | fr | https://api.archives-ouvertes.fr/search/?q="local-first"&fq=language_s:fr&fq=producedDate_s:[2019 TO *] | discovery |
| helmholtz | de | GET helmholtz.software/api/v1/software?or=(...ilike.*Provenienz*...) and Berechtigung, Nachvollziehbarkeit, Sandbox, Herkunft, lokal (glossary run,... | negative |
| helmholtz | en | https://helmholtz.software/api/v1/software?or=(brand_name.ilike.*provenance*,short_statement.ilike.*provenance*) | discovery |
| hf-papers | en | GET https://huggingface.co/api/papers/search?q=agent%20skills%20SKILL.md | discovery |
| hf-papers | en | GET https://huggingface.co/api/papers/search?q=multi-agent%20delegation%20accountability%20provenance%20principal (and two sibling queries) | discovery |
| huggingface | en | https://huggingface.co/api/models?search=multilingual-e5-small&sort=downloads | discovery |
| huggingface | zh | Chinese-authored papers on agent authorization, hash-chained audit and sandboxing (WebSearch limited to arxiv.org and huggingface.co, one query) | negative |
| jstage | ja | サンドボックス (globalSearchKey) | negative |
| jstage | ja | 改ざん検知 監査ログ; ハッシュチェーン | negative |
| kci | ko | POST https://www.kci.go.kr/kciportal/po/search/poArtiSearList.kci poSearchBean.queryText=소울바운드 토큰 | discovery |
| kci | ko | poSearchBean.queryText=권한 위임 토큰 폐기 | negative |
| maven | en | GET https://search.maven.org/solrsearch/select?q=a:spring-ai-mcp&rows=8&wt=json; q=a:langchain4j-core; q=mcp | discovery |
| maven | en | pass2: https://search.maven.org/solrsearch/select?q=g:org.axonframework (38 artifacts); gh api repos/AxonIQ/AxonFramework; README grep | discovery |
| npm | en | GET https://registry.npmjs.org/@modelcontextprotocol%2Fclient | discovery |
| npm | zh | GET https://registry.npmjs.org/-/v1/search?text=agentskills | discovery |
| nuget | en | GET https://azuresearch-usnc.nuget.org/query?q=model context protocol&take=10; packageid:ModelContextProtocol; packageid:ChilliCream.ModelContextPr... | discovery |
| nuget | en | GET https://azuresearch-usnc.nuget.org/query?q=Microsoft.Extensions.AI; gh api search/code -f q="ApprovalRequiredAIFunction repo:dotnet/extensions" | discovery |
| openalex | en | GET https://api.openalex.org/works?search=model context protocol security tool poisoning authorization | discovery |
| openalex | en | GET https://api.openalex.org/works?search=decentralized society soulbound tokens | discovery |
| opencode-de | de | GET https://gitlab.opencode.de/api/v4/projects?search=MCP | discovery |
| opencode-de | en | https://gitlab.opencode.de/api/v4/projects?search=local-first | negative |
| openi | zh | https://openi.pcl.ac.cn/explore/repos?q=持久化执行 | negative |
| openi | zh | https://openi.pcl.ac.cn/explore/repos (R12 request from Branch C) | negative |
| pypi | en | GET https://pypi.org/pypi/fastmcp/json | discovery |
| pypi | ja | GET https://pypi.org/pypi/agentbox/json | discovery |
| pypi | ko | WebSearch: AI 에이전트 감사 로그 해시 체인 변조 방지 오픈소스 GitHub 구현 | discovery |
| qiita | ja | https://qiita.com/api/v2/items?query=Temporal 耐久実行 | discovery |
| qiita | ja | https://qiita.com/api/v2/items?query=ソウルバウンドトークン | discovery |
| rsd-nl | en | GET https://research-software-directory.org/api/v1/software?or=(brand_name.ilike.*sandbox*,short_statement.ilike.*sandbox*,description.ilike.*sandb... | discovery |
| rsd-nl | nl | GET https://research-software-directory.org/api/v1/software?select=slug,brand_name,short_statement&or=(brand_name.ilike.*mandaat*,short_statement.i... | negative |
| semanticscholar | en | GET https://api.semanticscholar.org/graph/v1/paper/search?query=agent tool permission user confirmation safety&venue=ACL,EMNLP,NAACL,EACL,Findings&... | negative |
| semanticscholar | en | https://api.semanticscholar.org/graph/v1/paper/search?query=selective disclosure provenance verifiable credentials AI-generated content ; query=hum... | negative |
| sourceforge | en | https://sourceforge.net/directory/?q=daemontools; https://sourceforge.net/rest/p/daemontools/; https://sourceforge.net/projects/daemontools/files/ | discovery |
| sourceforge | en | https://sourceforge.net/directory/?q=winsw; https://sourceforge.net/projects/windows-serv-wrap-perm.mirror/ | discovery |
| swh | en | GET https://archive.softwareheritage.org/api/1/origin/https://github.com/sourcecred/sourcecred/visit/latest/?require_snapshot=true | discovery |
| swh | en | GET https://archive.softwareheritage.org/api/1/origin/https://github.com/{openworkflowdev/openworkflow, RaycarlLei/tool-journal, lfzkoala/catp, Aud... | negative |
| university-gitlab | de | GET https://git.rwth-aachen.de/api/v4/projects?search=agent / MCP / sandbox | negative |
| university-gitlab | en | GET https://gitlab.mpcdf.mpg.de/api/v4/projects?search=ai-cli-agents | discovery |
| university-gitlab | fr | https://gitlab.inria.fr/api/v4/projects?search=MCP&order_by=last_activity_at&per_page=12&simple=true (host gitlab.inria.fr) | negative |
| web | de | GET https://zenodo.org/api/records?q=Anerkennung Forschungssoftware Beitrag&size=8 (host zenodo.org) | discovery |
| web | en | curl https://nodejs.org/docs/latest-v24.x/api/permissions.html | discovery |
| web | fr | WebSearch allowed_domains linuxfr.org: 'sandboxer agents IA bubblewrap Landlock agents de code confinement'; WebFetch of the news page | discovery |
| zenn | ja | https://zenn.dev/api/search?q=サンドボックス Landlock&source=articles | discovery |
| zenn | ja | ケーパビリティ トークン; Biscuit 認可; UCAN | negative |
| zenodo | en | https://zenodo.org/api/records?q=selective disclosure provenance attestation&type=software ; gh api repos/jerrylin96/git-signoff | discovery |
| zenodo | en | https://zenodo.org/api/records?q=agent memory provenance human review&type=software | discovery |

## C. Provenance ledger pointers

- `ledger/codebases.jsonl`: 586 rows after dedup (`records_in` 1,155), one per codebase, with `codebase_id`, canonical source, requirement ids, branches, source records, platforms, languages found in, documentation language, upstream status A-G, licence and flags, chain, commit or SWHID, version, maintenance and test summaries, counterexamples, evidence level, disposition, dedup notes. Dispositions: candidate 185, lead 279, excluded 104, counterexample-only 18. Documentation language: en 490, multi 28, zh 19, de 18, fr 10, nl 10, ja 7, others 4.
- `ledger/discovery-s2-*.jsonl` (13 files) and `ledger/negative-s2-*.jsonl` (13 files): row schema in `ledger/SCHEMA.md`; every row carries the query, platform, language, date, result URL, evidence level (`inspected` or `reported`) and the agent id.
- `ledger/prov-validation.md`: malformed rows, 23 correction rows applied, licence and status disagreements between agents (seven licence disagreements remain, eight at Gate 2; none touches a shortlisted codebase).
- `ledger/pass2-targets.md` and `ledger/platform-urls.md`: pass-2 targeting and the platform list with verified endpoints.

## D. Paper-to-code and package-to-upstream mappings

### D.1 Paper to code (candidates and leads with a paper identity)

| Paper | Code | Requirement | Note |
|---|---|---|---|
| arXiv 2610.22697 Intact (2026-10-15) | github.com/llm-platform-security/intact `e237f38`; dataset huggingface.co/datasets/umariqbal/web-agent-attack-benchmark `961bc7f` (CC-BY-4.0) | R19 | measured 12.8 percent versus 73.1 percent attack success; 16 pytest files; Python and Playwright, days old |
| arXiv 2607.14166 "Stop Means Stop" | no code link | R19, R11 | sibling-leak finding used as an acceptance test design |
| hal-01900081, hal-01576379 (Belenios proofs) | gitlab.inria.fr/belenios/belenios `8888045`, release 3.0 (2024-10-08) | R30 | AGPL-3.0-or-later verified from COPYING |
| arXiv 2207.09950 MeritRank | github.com/grimadas/meritrank | R26-R28 | research code; pattern only |
| arXiv 2603.24775 | github.com/sunilp/aip | R01, R07, R12 | candidate, status B; not shortlisted |
| HF Papers 2604.04522 | github.com/helixar-ai/hdp; npm `@helixar_ai/hdp` | R07, R12 | status spread between agents, recorded in `prov-validation.md` |
| arXiv paper rows without code (22 rows in the codebase ledger carry a paper URL as canonical) | - | various | recorded as `paper` artefacts, status F, never scored |

### D.2 Package to upstream (35 codebases with both an npm and a GitHub record; the ones the article relies on)

| Package | Upstream | Version pinned | Checked |
|---|---|---|---|
| `@anthropic-ai/sandbox-runtime` | anthropics/sandbox-runtime | 0.0.81 = tag v0.0.81 = `c40cf14a` | registry and tag match; CI result for the commit confirmed via the Actions API |
| `@biscuit-auth/biscuit-wasm` | eclipse-biscuit/biscuit-wasm `80cceed` over biscuit-rust `93832a8` | 0.6.0 | binding depends on an unmaintained WASM allocator (dossier) |
| `tuf-js`, `@tufjs/models` | theupdateframework/tuf-js `a399ce8` | 6.0.0 | used by npm itself |
| `openworkflow` | openworkflowdev/openworkflow `c82fbed` | 0.11.0 | CLI telemetry on by default; core wrapped only |
| `hypercore` | holepunchto/hypercore `9c9cc3d` | 11.39.0 | five native add-ons, 184 MB prebuild |
| `@sd-jwt/core`, `@sd-jwt/sd-jwt-vc`, `@owf/token-status-list` | openwallet-foundation-labs/identity-common-ts `42586ca` | 0.23.0, 0.5.0 | continuation of the archived sd-jwt-js |
| `@cedar-policy/cedar-wasm` | cedar-policy/cedar | compared, not adopted | - |
| `@napi-rs/keyring` | brooooooklyn/keyring-node | R15 stack | no audit found |
| `age-encryption` | FiloSottile/typage | R15 stack | no audit found |
| `ses` | endojs/endo | R21 | pattern |
| `@contentauth/c2pa-node` | contentauth/c2pa-js | R12 candidate with a Windows-binary defect (issue #243) | not shortlisted |
| `@deepseek-ai/dsh` | deepseek-ai/deepseek-harness | already wrapped by the Alpha | unaudited |
| `@agentclientprotocol/sdk` | agentclientprotocol/typescript-sdk | R07 | Goose adapter transport |
| `dsh-augmentor` 0.2.13 | ManoloRemiddi/augmentor-agent | the only ResonantOS registry artefact | relicensed upstream 2026-09-23 (OI-3) |

## E. Term bank summary

Files: `glossary/zh.md`, `fr.md`, `de.md`, `nl.md` (16 core concepts and R01-R30 each, with evidence per term marked inspected or reported, and rejected terms), `glossary/ja-ko-probe.md`.

| Language | Headline | Native terms that found code | Platforms where they worked |
|---|---|---|---|
| Chinese | practitioners keep English for agent and DAO vocabulary; native terms for containment and durability | 沙盒, 持久化执行, 幂等键, 抗共谋, 可验证凭证 | GitHub (search in Chinese), GitCode, domain-restricted web search; Gitee and OpenI closed |
| French | English loanwords dominate (MCP, workflow, sandbox, token, proxy); one strong native security term | bac à sable, confinement (with process words), journal d'audit, révocation | HAL API, LinuxFr, Framagit, gitlab.inria.fr |
| German | English nouns in technical text; native vocabulary in public-sector and research texts | Berechtigungen, Protokolle, Widerruf, Nachweis, Freigabe, Provenienz | openCode.de, Helmholtz RSD, BSI texts |
| Dutch | English for almost every concept; one native cluster in public-sector identity and logging | logboek, verantwoording, mandaat, intrekking, machtiging | developer.overheid.nl, Logius and VNG material, RSD |
| Japanese, Korean | probe only: eight P0 requirements, about 55 calls | mini term banks in the probe file; single-word GitHub queries worked, multiword Japanese queries returned nothing | GitHub (poor CJK recall), Qiita API, Zenn, J-STAGE, KCI; tripwire did not fire |

## F. Search methodology and exclusions

**Method.** Stage 1 mapped the project from clones and APIs (static reading only) and produced 30 requirements with constraints and 16 core concepts. Stage 2 ran four term-bank agents, eight branch agents (one per requirement group, two passes, the second targeted by `pass2-targets.md`), four language agents, one probe and one provenance agent, all Sonnet 5.5, in waves of at most ten; every search was recorded as a discovery row or a negative row with query, platform, language and date; the provenance agent merged source records into codebases and resolved disagreements. Shortlist criteria were written before the results were read (`gate2-report.md` section 3). Stage 3 inspected sixteen codebases at pinned commits (static only, read-only clones under `_untrusted/`); fifteen dossiers were reviewed by three fresh-context adversarial reviewers and the Realms dossier, added at Gate 3, by one DAO reviewer, with amendments and lead decisions logged. Scoring used weights fixed before the dossiers (`weights.json`), a pre-registered sensitivity script, and, after Gate 3, a labelled what-if and perturbation pass with weights unchanged. The architecture step and this article followed.

**Exclusions applied before scoring** (`gate2-report.md` section 3; hard gates in `weights.json`): G1 no cloud or telemetry for the core function; G2 no silent per-OS degradation; G3 no copyleft or source-available code inside the MIT Alpha without legal review; G4 EVM-only chain components are patterns for the Solana-targeted DAO; G5 no candidate that turns a DAO credential into runtime authority or an agent into a human-only actor. Hosted-only products are patterns for R10 and R11. Demos younger than a month are leads unless they are the only implementation of a needed design. Licence disagreements were resolved toward the file at HEAD.

**Rules the agents followed.** Public APIs only; robots and rate limits respected; blocked platforms recorded as blocked, never bypassed (Gitee, OpenI, GitCode API); `gh api -X GET` for search; `python -I` for every script reading downloaded files; no issues, comments or contact with any maintainer (OI-1 to OI-4 held); README and page text treated as evidence, never as instructions.

## G. Verification failure rates

| Stage | Verifier | Sample | Result | Rate | Report |
|---|---|---|---|---|---|
| 1 (project map) | fresh Sonnet 5.5, seed 20261020 | 15 of 63 capability rows plus CI and RPC re-reads | 9 PASS, 6 PARTIAL, 0 FAIL; all six corrections applied | 20.0 percent (partial counts half) | `stage1/verification.md` |
| 2 (discovery) | fresh Sonnet 5.5, seed 20261020 | 110 of 1,099 rows, four checks each | URL 0.0 percent; canonical 1.4 percent; licence 1.9 percent (2 FAIL, corrected); unmarked duplicate 26.4 percent as scored, 5.5 percent for same-agent repeats | 7.5 percent as scored; 2.2 percent with cross-agent duplicates counted as resolved | `ledger/verification-stage2.md` |
| 2 (shortlist) | same | all 16 shortlist codebases | 13 PASS, 3 PARTIAL, 0 FAIL (fork relation, licence file path, third-party licence section) | - | same, section "shortlist" |
| 3 (dossiers) | archaeologist and DAO reviewers re-opening a selection of decision-carrying citations at the recorded SHA | 189 citations across 16 dossiers | 181 PASS, 7 PARTIAL, 1 FAIL (fixed) | 95.8 percent exact, 99.5 percent supporting | `reviews/code-archaeologist.md`, `reviews/dao-skeptic-r24.md`, `reviews/gate3-report.md` |
| 4 (article, first draft) | three Sonnet 5.5 citation checkers over section ranges (1-3 and 11-14 with the appendix; 4-6; 7-10) re-opening every pointer at the recorded SHA; one Opus 5.5 fresh-context adversarial review | 499 items (201, 177, 121) | 412 PASS, 60 PARTIAL, 26 FAIL; 24 of the FAILs were one defect (threat ids in sections 9, 11 and the Next 10 table that did not follow the threat model's families); adversarial review: 7 blockers, 22 majors, 17 minors | 11.2 percent weighted over the draft (19.4, 4.2 and 8.7 per range); every FAIL and PARTIAL and every blocker and major corrected in the published text, listed in `state.md` D5.5 | `reviews/citations-stage4-1.md`, `-2.md`, `-3.md`, `reviews/article-adversarial.md` |

## H. Open questions and unverified claims

Open questions carried from the gates (`gate2-report.md` section 8, `gate3-report.md`, `threat-model-draft.md` section 5):

1. Whether any child process can be confined on Windows without administrator rights from a Node parent (ranked test 1 decides).
2. Whether the approval-gated route (R11) and the host-verifiable promotion review (R14) should be one mechanism; the blueprints keep them as one ledger with two record types.
3. Whether a redactor can keep a key from an echoing upstream across encodings (ranked test 2).
4. Whether the credential-store head mirror is reliable across the three OS stores (falsification condition 4).
5. R25 personhood and R27 collusion resistance were not inspected at code level; the DAO rules that depend on them are policy.
6. Audit reports for the proposed R15 vault stack (typage, keyring-node) were not found.
7. Eight licence disagreements between agents remain listed in `prov-validation.md`; none affects a shortlisted codebase.

Unverified claims in the article, each labelled where it appears: every "designed, not yet tested" property of the proposed layers (section 6.1 marks D); Convira's no-admin Windows claim and junction behaviour; sandbox-runtime's Windows residuals (read from code, not measured); the Realms shared instance's deployed source (VERSION 3.1.7 with no matching public tag, read by RPC); the rewards program's deployed binary matching no public commit; the `community.db` row contents (not read); on-chain facts, which were read on 2026-10-20 and 2026-10-21 and can change; the CI claims for third-party projects, which rest on Actions logs read through the API for sandbox-runtime, tuf-js and Convira, and on workflow listings or READMEs for the others. Every verdict that depends on a test is listed with its conditional in `architecture/acceptance-backlog.md`.

## I. Four complete discovery chains

**Chain 1 (French-language agent, English-language records): HAL to Inria GitLab to release to tests.** The French language agent queried the HAL API for `Belenios` (a proper noun, so the query and the records are in English even though the route is a French research platform) (20 papers, among them hal-01900081, machine-checked privacy and verifiability proofs) on 2026-10-20; the paper's software reference led to `gitlab.inria.fr/belenios/belenios` (no GitHub mirror: `gh api repos/belenios/belenios` returns 404); the project API gave commit `8888045` and releases 2.5.1 (2024-06-28) and 3.0 (2024-10-08); the tree showed `tests/` (debian-votes, scaling, tool, webdriver) and `.gitlab-ci.yml`; a pass-2 correction row verified the licence as AGPL-3.0-or-later from COPYING and per-file headers. Disposition: candidate for R30 advisory voting as a separate AGPL service; counterexample row for operator-run trustee roles and no weighted voting. Rows: `ledger/discovery-s2-lang-fr.jsonl` lines 25, 26, 47, 50.

**Chain 2 (German research index, English-language records): Helmholtz RSD to GitHub to version to tests.** German language agent queried the Helmholtz Research Software Directory API for `agent` and found slug `terok` (developed at CASUS, HZDR); `gh api repos/terok-ai/terok-sandbox` gave commit `2f8f0c1`, release terok v0.9.1 (2026-09-29), 93 unit-test entries plus integration tests (`test_vault_stories.py`, `test_vault_container_transport.py`), Apache-2.0, REUSE-compliant, no advisories; the README's credential-vault statement ("the container receives short-lived phantom tokens and never sees the real credentials") is the R03 pattern. Branch H's pass-2 sweep added the counterexample: Linux and rootless Podman only. Disposition: candidate for R03 as a design reference; absent from every English branch. Rows: `ledger/discovery-s2-lang-de.jsonl` (R03, R02), `ledger/discovery-s2-br-h.jsonl` (counterexample).

**Chain 0 (non-English start): a French query on LinuxFr to GitHub to release to tests.** The French language agent searched linuxfr.org with the French query `sandboxer agents IA bubblewrap Landlock agents de code confinement` on 2026-10-20, read the French-language LinuxFr news article "J'ai mis un proxy entre claude et Internet" (published 2026-03-18 by the maintainer, CC BY-SA; quote: "Greywall est un bac à sable deny-by-default pour les agents IA", a deny-by-default sandbox for AI agents), followed its repository link to `github.com/GreyhavenHQ/greywall` (commit `60ab1b5`, release v0.3.7 of 2026-06-01, Apache-2.0, Go test files for the Linux and macOS sandboxes, a 90-day disclosure policy, and a closed same-day escape issue #55) and its companion `GreyhavenHQ/greyproxy` (v0.4.5, MIT). Branch H's pass-2 sweep added the counterexample: Greyproxy installs a machine-wide trusted MITM certificate with sudo and has no Windows path. Disposition: candidate for R02 and R03 as patterns (container-free deny-by-default sandbox; placeholder-swapping proxy); absent from every English branch. Rows: `ledger/discovery-s2-lang-fr.jsonl` (Greywall repo row and the LinuxFr document row), `ledger/discovery-s2-br-h.jsonl` (Greyproxy counterexample).

**Chain 3 (paper to code to dataset to tests): HF Papers to arXiv to GitHub to Hugging Face dataset.** Branch E searched HF Papers for `browser extension isolation`, found arXiv 2610.22697 (Intact, 2026-10-15), followed the code link to `github.com/llm-platform-security/intact` at `e237f38` (16 pytest files, last commit 2026-10-19) and the README's dataset link to `huggingface.co/datasets/umariqbal/web-agent-attack-benchmark` at `961bc7f` (CC-BY-4.0, 1,091 pages). The measured results (12.8 percent versus 73.1 percent) were taken from the abstract, not re-run. Disposition: candidate for R19 as a gate design and an acceptance corpus; not adoptable (Python, Playwright, one LLM call per element). Rows: `ledger/discovery-s2-br-e.jsonl`.

**Chain 4 (registry to tag to commit to CI to dossier): npm to GitHub tag to Actions API.** Branch B's seed lead for bubblewrap and Seatbelt reached `anthropics/sandbox-runtime`; npm `@anthropic-ai/sandbox-runtime` 0.0.81 (2026-10-20) matched tag v0.0.81 and commit `c40cf14a`; the test tree listed about 130 files (nested user namespaces, seccomp, PID namespace, symlink boundary, Seatbelt, winsrt, proxy-only, credential-mask); the Stage 3 inspector confirmed the CI result for that commit through the GitHub Actions API and produced `dossiers/anthropics-sandbox-runtime.md` with the env-mask echo finding (`body-substitution.ts:58-94`) that section 7's X-5 rests on. Vendor disclosure: Anthropic also makes the models that ran this research; the finding against its masking mode is recorded as a blocker accepted by the inspector.

## J. Reproducible research trail

- Decision log: `state.md` D0.1 to D5.5 (who decided, when, and what changed), with the gate table and the corrections table.
- Agent rosters, models, efforts and outputs per stage: `PLAN.md`.
- Seeds: Stage 1 and Stage 2 verifiers used `random.seed(20261020)` with the commands quoted in their reports.
- Scripts: `scoring/sensitivity.py` (pre-registered; any rank change under plus or minus 25 percent weight or a dropped criterion is FRAGILE), `scoring/whatif.py` (capture profile and plus or minus one isolation perturbation), the provenance merge script in the s2-prov scratchpad (its outputs are the ledger files). All run with `python -I` over the ledger files.
- Briefs given to agents: `ledger/BRIEF-stage2-*.md`, `reviews/BRIEF-stage3-reviewers.md`, `reviews/BRIEF-stage3-amend.md`.
- Lessons recorded for the next run: `lessons/` (Write tool over heredocs for large files; `gh api -X GET` for search; agents stall on permission prompts, so write output early with `STATUS: PARTIAL`; one scratchpad subfolder per agent; never invoke skills from under `_untrusted/`; `python -I` for scripts over downloaded files; regional platform access limits).
- Held communications: OI-1 to OI-4 in `ARTICLE.md` section 13; none sent.

## K. Compact table of the longlist: the 185 candidate codebases

Generated from `ledger/codebases.jsonl` (disposition `candidate`; 185 rows). Columns: requirements, upstream status (A active and released, B active, C young or thin, D design only, E planned, F document only, G archived or dead), licence, documentation language, one-line summary from the ledger, and whether a Stage 3 dossier exists. The 279 leads, 104 excluded and 18 counterexample-only rows are in the same file with their reasons.

| Codebase | Reqs | Status | Licence | Doc lang | Ledger summary | Dossier |
|---|---|---|---|---|---|---|
| cedar-policy/cedar | R01 | A | Apache-2.0 | en | HEAD 2026-10-19; frequent releases (v4.14.0 on 2026-10-17); AWS-led; 180 open issues |  |
| eclipse-biscuit/biscuit-rust | R01 | A | Apache-2.0 | en | HEAD 2026-10-08; Eclipse Foundation project moved from the biscuit-auth org; last crates.io release 2025-07-16; 39 open issues | yes |
| eclipse-biscuit/biscuit-wasm | R01 | B | Apache-2.0 | en | HEAD 2026-07-13; npm 0.6.0 2025-09-26; no GitHub releases; 10 open issues | yes |
| getaegis/aegis | R01, R03 | B | Apache-2.0 | en | last commit 2026-08-06; 0 open issues (sweep 2026-10-20); archived=False; repo created 2026-03-08; 0 contributors (top: n/a) | yes |
| novavey/attenuated-delegation-chain | R01 | C | Apache-2.0 | en | 15 commits between 2026-09-08 and 2026-09-18, two author names that look like one person/organisation (Tyler Pepitone, Nova Vey Engineeri... |  |
| oomny-nl/agent-mandaat | R01, R07, R19 | C | EUPL-1.2 | nl | last commit 2026-10-19 (sha 39fddbb); created 2026-10-17; 0 open issues; no releases; Dependabot enabled; actions pinned by SHA; single a... |  |
| oomny-nl/agent-mandaatbewijs | R01, R12, R13, R19, R23 | C | EUPL-1.2 | nl | created 2026-10-17, pushed 2026-10-19; Oomny B.V.; 0 issues |  |
| open-policy-agent/npm-opa-wasm | R01 | B | Apache-2.0 | en | HEAD 2026-07-10; last npm release 2024-11-08 (about 23 months before inspection); 16 open issues; OPA core (open-policy-agent/opa v1.21.3... |  |
| openai/codex | R01, R02, R03 | A | Apache-2.0 | en | HEAD 2026-10-20, daily commits; about 23,000 open issues (very large project); OpenAI |  |
| openclaw/openclaw | R01, R07, R29 | B | MIT | en | last commit 2026-10-20; releases several per month; steward is the OpenClaw Foundation (501(c)(3) per README); very high issue volume (ab... |  |
| openjiuwen-ai/agent-protocol | R01, R06, R07, R11 | B | Apache-2.0 | multi | created 2026-02-26; last commit 2026-10-20 on branch develop; 22 open issues; openJiuwen ecosystem (organisation behind it not further id... |  |
| sunilp/aip | R01, R07, R12 | B | Apache-2.0 | en | last commit 2026-10-10; 1 open issues (sweep 2026-10-20); archived=False; repo created 2026-03-22; 1 contributors (top: sunilp:157) |  |
| vercel/ai | R01, R06, R07, R08 | C | Apache-2.0 | en | monorepo last commit 2026-10-20 with daily releases; about ten adapter packages (harness-claude-code, -codex, -opencode, -cursor, -cline,... |  |
| anthropics/sandbox-runtime | R02, R03 | B | Apache-2.0 | en | HEAD 2026-10-20; release 0.0.81 the same day; README labels it 'Beta Research Preview'; vendor is Anthropic (the model vendor behind this... | yes |
| bytecodealliance/wasmtime | R02, R21 | A | Apache-2.0 \|\| Apache-2.0 ... | en | HEAD 2026-10-20; Extism core v1.41.0 2026-10-09 (BSD-3-Clause) but extism/js-sdk HEAD 2025-05-14 (stale) |  |
| containers/bubblewrap | R02 | A | OTHER:LGPL-2.1 (COPYING and... | en | HEAD 2026-10-14; release 2026-10-14; Flatpak/Containers project; 207 open issues |  |
| convira/convira-sandbox | R02 | B | Apache-2.0 | en | HEAD 2026-08-08 (2.5 months); 1 open issue; vendor is Convira (a desktop AI agent product); not published to npm (npm view @convira/sandb... |  |
| deepseek-ai/deepseek-harness | R02, R03, R07, R09, R10, R29 | C | MIT | multi | last commit 2026-10-17; release candidates; README banner: 'developer preview ... THERE WILL BE COMPATIBILITY-BREAKING CHANGES'; organisa... |  |
| fencesandbox/fence | R02 | B | Apache-2.0 | en | created 2025-12-18; last commit 2026-09-10, pushed 2026-10-14; 40 open issues; repo moved from Use-Tusk/fence to fencesandbox/fence (GitH... |  |
| greyhavenhq/greywall | R02, R03 | B | Apache-2.0 | en | repo created 2026-03-04; last default-branch commit 2026-08-13, GitHub pushed_at 2026-10-17; latest release v0.3.7 on 2026-06-01 (release... |  |
| nolabs-ai/nono | R02, R03 | B | Apache-2.0 | en | HEAD 2026-10-19; 261 open issues; 312 forks; company project |  |
| superradcompany/microsandbox | R02, R03 | B | Apache-2.0 | en | HEAD 2026-10-19; 121 open issues; company-backed (superrad.company) |  |
| brooooooklyn/keyring-node | R03, R15 | F | MIT | en | last commit 2026-10-19; 2 open issues (sweep 2026-10-20); archived=False; repo created 2023-02-25; 8 contributors (top: renovate[bot]:96,... |  |
| greyhavenhq/greyproxy | R03 | B | MIT | en | created 2026-03-03; last commit 2026-06-02 (about 4.5 months before inspection); 4 open issues; same organisation as greywall |  |
| indigo-dc/oidc-agent | R03 | A | MIT | en | KIT/Helmholtz (Karlsruhe) project, 20 contributors on the GitLab mirror; GitHub last push 2026-10-07 is newer than the Helmholtz GitLab l... |  |
| infisical/agent-vault | R03 | B | MIT | en | HEAD 2026-10-01; last push 2026-10-18; 96 open issues; Infisical Inc. |  |
| terok-ai/terok-sandbox | R03 | C | Apache-2.0 | en | terok created 2025-11-22, pushed 2026-10-20, 63 open issues; terok-sandbox pushed 2026-10-19, 6 open issues; developed at CASUS, an insti... |  |
| wanghr0318-dotcom/deepresearch-sandbox-go-python | R03, R08, R10 | B | MIT | multi | created 2026-09-28, last push 2026-10-12, 0 stars, single maintainer, 16 open issues |  |
| xtrem21-source/apivault_proxy | R03 | B | MIT | fr | created 2026-10-19 (one day old at inspection); last commit 2026-10-19; one author; bilingual FR/EN docs; v1.0.0 to v1.0.4 in one day |  |
| keith.github.io/xcode-man-pages/launchd.plist.5.html | R04 | A | NOASSERTION | en | mirror page; Apple developer.apple.com not fetched (JavaScript site) |  |
| systemd/systemd | R04 | A | OTHER:GPL-2.0 text (LICENSE... | en | HEAD 2026-10-20; host freedesktop.org for the page; 3572 open issues |  |
| theupdateframework/tuf-js | R04, R18 | A | MIT | en | last commit 2026-06-02; 5 open issues (sweep 2026-10-20); archived=False; repo created 2022-08-26; 7 contributors (top: dependabot[bot]:4... | yes |
| weiming88888/dsh-guardian | R04 | C | MIT | multi | HEAD 2026-10-03; 1 open issue; single author; English README plus Chinese README and guide |  |
| winsw/winsw | R04 | B | MIT | en | HEAD 2026-05-30; no release since 2023-01; 275 open issues; .NET Framework 4.6.1+ per README |  |
| developer.chrome.com/docs/extensions/develop/concepts/nat... | R05, R20 | A | NOASSERTION | en | host developer.chrome.com |  |
| jupyter-server/jupyter_server | R05 | A | BSD-3-Clause | en | HEAD 2026-09-15 |  |
| keepassxreboot/keepassxc-browser | R05, R20 | F | GPL-3.0-only \|\| OTHER:GPL... | en | last commit 2026-10-14; community project, active |  |
| microsoft/vscode | R05, R06 | A | MIT | en | HEAD 2026-10-20; Microsoft |  |
| modelcontextprotocol/typescript-sdk | R05, R06 | A | Apache-2.0 | en | licence transition commit 5ce4b5ef086045629e1ad444785d2d1fdb137a09 'chore: update licensing to Apache 2.0 for new contributions (#1377)' ... |  |
| parksben/opensider | R05, R20 | B | MIT | en | last commit 2026-10-16; 0 open issues (sweep 2026-10-20); archived=False; repo created 2026-09-02; 1 contributors (top: parksben:331) |  |
| tailscale/tailscale | R05, R20 | A | BSD-3-Clause | en | last commit 2026-10-19; 4748 open issues (sweep 2026-10-20); archived=False |  |
| aaif-goose/goose | R06, R07, R29 | B | Apache-2.0 | en | last commit 2026-10-20; frequent releases; GOVERNANCE.md; part of the Agentic AI Foundation at the Linux Foundation (README); 1 published... | yes |
| gethelio/helio | R06 | B | Apache-2.0 | en | created 2026-05-19, last commit 2026-10-19, 135 open issues, one npm maintainer (olivrg) |  |
| jiangkoumo/toolfence | R06 | B | MIT | en | repository created 2026-08-17, last commit 2026-09-07, single maintainer, 0 open issues, no security advisories |  |
| punkpeye/fastmcp | R06 | A | MIT | en | last commit 2026-10-20; 1 open issues (sweep 2026-10-20); archived=False |  |
| sunblaze-ucb/progent | R06, R19 | C | MIT | en | last commit 2026-09-24; 1 open issues (sweep 2026-10-20); archived=False; repo created 2025-04-17; 1 contributors (top: stneng:4) |  |
| a2aproject/a2a-js | R07 | A | Apache-2.0 | en | a2a-js last commit 2026-10-19, 53 open issues; spec repo under Linux Foundation governance (GOVERNANCE.md); Python SDK a2a-sdk 1.2.3 on PyPI |  |
| agentclientprotocol/agent-client-protocol | R07 | A | Apache-2.0 | en | last commit 2026-10-20; GOVERNANCE.md and MAINTAINERS.md present; SDKs in Rust, TypeScript, Python |  |
| agentclientprotocol/typescript-sdk | R07 | A | Apache-2.0 | en | last commit 2026-10-19; 3 open issues; npm maintainers benbrandt, aguzubiaga, cirwin; v1 and v2 protocol shapes both shipped |  |
| helixar-ai/hdp | R07, R12 | D | Apache-2.0 | en | created 2026-03-25; last commit 2026-10-08; 7 open issues; one npm maintainer (siri_helixar); backed by a company (Helixar-AI), open-core... |  |
| openhands/software-agent-sdk | R07 | B | MIT | en | created 2025-08-23; last commit 2026-10-20; 741 open issues; the legacy OpenHands/OpenHands repo had a command-injection advisory GHSA-7h... |  |
| sunilp/aip-node | R07 | C | Apache-2.0 | en | last commit 2026-04-25; 0 open issues (sweep 2026-10-20); archived=False; repo created 2026-04-25; 1 contributors (top: sunilp:27) |  |
| berriai/litellm | R08 | A | OTHER:MIT-with-enterprise-d... | en | last commit 2026-10-20; 5534 open issues; repository description says 'Rust core with Python SDK'; at least 30 advisories (see counterexa... |  |
| earendil-works/pi | R08, R09 | A | MIT | en | last commit 2026-10-20; v1.3.0 2026-10-15; 372 open issues; maintainers mitsuhiko and badlogic on npm; new issues from new contributors a... |  |
| maximhq/bifrost | R08 | B | Apache-2.0 | en | created 2025-03-19; last commit 2026-10-19; 1264 open issues; commercial vendor Maxim AI behind it |  |
| musistudio/claude-code-router | R08 | B | MIT | en | last push 2026-10-10; 1155 open issues; README_zh.md; single-owner project with large community |  |
| remorses/ai-fallback | R08 | B | MIT | en | last commit 2026-07-07; 3 open issues (sweep 2026-10-20); archived=False; repo created 2024-11-28; 7 contributors (top: remorses:62,durac... |  |
| agentskills/agentskills | R09 | B | Apache-2.0 | en | root Apache-2.0 LICENSE added 2026-02-05 (commit 505cd8efa8, PR 122); copyright holder filled in 2026-02-17 (commit 752b29a0a1, PR 163); ... |  |
| jdutton/vibe-agent-toolkit | R09 | B | MIT | en | last commit 2026-10-11; 32 open issues (sweep 2026-10-20); archived=False; repo created 2025-12-27; 5 contributors (top: jdutton:299,davi... |  |
| supermarioyl/skillprov | R09, R18 | B | Apache-2.0 | multi | last commit 2026-10-17; 0 open issues (sweep 2026-10-20); archived=False; repo created 2026-06-15; 2 contributors (top: SuperMarioYL:22,y... |  |
| uctoocom/agentskills-runtime | R09 | C | MIT | en | created 2026-02-16; last commit 2026-10-18; 0 open issues on the GitHub mirror; primary repository on atomgit.com/uctoo (not fetched); LI... |  |
| webmcp-org/agent-skills-ts-sdk | R09 | B | MIT | en | created 2026-05-21; last commit 2026-09-17; 0 open issues; single npm maintainer (miguelspizza); older sibling package @mcp-b/agent-skill... |  |
| dapr/durabletask-go | R10, R11 | B | Apache-2.0 | en | last commit 2026-10-12; 10 open issues (sweep 2026-10-20); archived=False; repo created 2024-11-15; 26 contributors (top: JoshVanL:147,ci... | yes |
| openworkflowdev/openworkflow | R10 | B | Apache-2.0 | en | last commit 2026-10-19; created 2025-10-25; 12 open feature-style issues, none about crash loss; npm release 2026-10-12; small team, pre-1.0 | yes |
| raycarllei/tool-journal | R10 | B | MIT | en | created 2026-09-07; last commit 2026-09-08; 6 releases in two days; single author; 7 open issues |  |
| resonatehq/resonate | R10 | B | Apache-2.0 | en | repo pushed 2026-10-20, last default-branch commit 2026-09-22; SDK last commit 2026-09-08; 45 open issues; company-backed (Resonate) |  |
| resonatehq/resonate-sdk-ts | R10 | B | Apache-2.0 | en | 2 dependencies; repository pushed 2026-10-19 |  |
| vercel/workflow | R10 | C | Apache-2.0 | en | last commit 2026-10-19; created 2025-10-23; 421 open issues; one published advisory (GHSA-9r75-g2cr-3h76, medium, 2026-03-05) |  |
| auditkitdev/auditkit | R11, R23 | C | AGPL-3.0-only | en | created 2026-03-09; last commit 2026-10-06 on branch v2; single organisation; 0 open issues; npm names @auditkit/core and @auditkit/verif... |  |
| bmi/eudi-wallet/relying-party-registrar | R11, R23, R30 | C | Apache-2.0 | en | created 2025-01-14, last commit 2026-10-15 (Mirko Mollik); 3 contributors; no tags or releases; publisher is the German Federal Ministry ... |  |
| frank2673/engagement-ledger | R11 | B | MIT | zh | last commit 2026-09-25; 0 open issues (sweep 2026-10-20); archived=False; repo created 2026-09-24; 1 contributors (top: Frank2673:13) |  |
| holepunchto/hypercore | R11, R16 | A | MIT | en | closed Windows issues #787 'Fix flush to wrong parent test on Windows', #210 'test filesystem compatibility, esp for windows', #281 'Hand... | yes |
| kanson1996/agent-audit-trail | R11 | C | Apache-2.0 | multi | created and last pushed 2026-03-13 (7 months without commits); single maintainer; no issues |  |
| lfzkoala/catp | R11 | B | MIT | en | last commit 2026-09-26; 0 open issues (sweep 2026-10-20); archived=False; repo created 2026-04-20; 1 contributors (top: lfzkoala:208) |  |
| ljunp/stinkycobbler | R11 | B | Apache-2.0 | zh | last commit 2026-09-20; 0 open issues (sweep 2026-10-20); archived=False; repo created 2026-08-10; 1 contributors (top: LJunP:59) |  |
| oomny-nl/agent-levenscyclus | R11, R19, R25 | C | EUPL-1.2 | nl | last commit 2026-10-19; created 2026-10-17; 0 issues; single author; same maintenance caveats as the series (see oomny.nl row) |  |
| pametan/audit-log | R11 | C | MIT | en | created and last pushed 2026-05-26; no releases; not published to npm under @pametan/audit-log (registry 404); single maintainer |  |
| sigstore/sigstore-js | R11, R12, R18 | A | Apache-2.0 | en | repo pushed 2026-10-19; last release 2026-08-04; 24 open issues; four published advisories in 2026 |  |
| transparency-dev/tessera | R11, R30 | A | Apache-2.0 | en | last commit 2026-10-19; 48 open issues; 'Library instead of microservice architecture' per README; maintained by the transparency-dev com... | yes |
| chartrunner/chartrunner-onchain | R12, R23, R30 | C | Apache-2.0 | en | HEAD 2026-10-16; created 2026-10-06; 0 open issues; single-product maintainer |  |
| contentauth/c2pa-js | R12 | B | MIT | en | 11 dependencies; open issue contentauth/c2pa-js#243 (2026-10-20) says this release is missing Windows x64 and Linux x64 binaries |  |
| contentauth/c2pa-rs | R12 | A | MIT OR Apache-2.0 | en | c2pa-rs last commit 2026-10-16, 285 open issues; c2pa-js last commit 2026-10-19 (sha 7036c209469116a0a19232b7c19fe5e14e67370b, MIT) |  |
| digitalbazaar/ecdsa-sd-2023-cryptosuite | R12 | B | BSD-3-Clause | en | last commit 2024-08-26 (about 26 months before inspection); bbs-2023-cryptosuite last commit 2024-08-26; digitalbazaar/vc last commit 202... |  |
| git-ai-project/git-ai | R12 | B | Apache-2.0 | en | created 2025-07-02; last commit 2026-09-09; 246 open issues; 30 releases since 2026-07; VC-backed company with a paid teams product |  |
| hypercerts-org/hypercerts-lexicon | R12, R23, R26 | C | MIT | en | last commit 2026-10-14; 13 open issues (sweep 2026-10-20); archived=False; repo created 2025-09-16; 13 contributors (top: aspiers:319,s-a... | yes |
| identity-common-ts (incl. former sd-jwt-js) | R12, R23 | B | Apache-2.0 | en | not archived; last commit 2026-10-19; created 2026-02-04; 22 releases since 2026-05; 52 open issues; one medium advisory (GHSA-qx2x-38rh-... |  |
| in-toto/attestation | R12 | A | Apache-2.0 | en | last commit 2026-09-14; 89 open issues; CNCF-hosted |  |
| inflexa-ai/tsprov | R12, R14 | B | Apache-2.0 | en | last commit 2026-09-27; 8 open issues (sweep 2026-10-20); archived=False; repo created 2026-06-18; 3 contributors (top: vivere-dally:58,r... |  |
| privacybydesign/irmago | R12, R23 | B | Apache-2.0 | en | created 2017-07-22; last commit 2026-10-16; releases v1.3.1 (2026-09-01), v1.4.0 (09-21), v1.4.1 (10-06), v1.4.2 (10-16); 99 open issues;... |  |
| researchobject/ro-crate | R12 | A | Apache-2.0 | en | last commit 2026-10-15; 144 open issues (sweep 2026-10-20); archived=False; repo created 2019-02-13; 39 contributors (top: stain:1278,eli... |  |
| researchobject/ro-crate-py | R12 | A | Apache-2.0 | en | last commit 2026-10-14; 16 open issues (sweep 2026-10-20); archived=False; repo created 2019-10-21; 17 contributors (top: simleo:571,stai... |  |
| trustvc/trustvc | R12, R23 | B | Apache-2.0 | en | created 2024-09-30; last commit 2026-09-16; 6 open issues; 30 releases since 2026-03; maintained under the TradeTrust (Singapore) ecosyst... |  |
| fabiospampinato/atomically | R13 | B | MIT | en | last commit 2026-07-17; 3 open issues (sweep 2026-10-20); archived=False; repo created 2020-07-02; 5 contributors (top: fabiospampinato:7... |  |
| SQLite | R13, R17 | A | OTHER:SQLite public-domain ... | en | core SQLite maintained by the SQLite team for decades |  |
| wiselibs/better-sqlite3 | R13 | A | MIT | en | last commit 2026-08-10; 76 open issues (sweep 2026-10-20); archived=False |  |
| datalad/datalad | R14 | A | MIT | en | created 2013, last commit 2026-10-14, release 2026-10-06, university-funded core team (Juelich, Dartmouth), 586 open issues | yes |
| dataobservatory-eu/betwixt | R14 | C | GPL-3.0-or-later | en | created 2026-06-17, last commit 2026-10-15, one maintainer (Daniel Antal, Data Observatory Foundation, EU), 6 open issues |  |
| dexio-wiki/llm-wiki-skills | R14 | C | MIT | en | last commit 2026-10-07; 0 open issues (sweep 2026-10-20); archived=False; repo created 2026-09-28; 1 contributors (top: forrestzhang107:4) |  |
| getzep/graphiti | R14 | B | Apache-2.0 | en | last commit 2026-10-20, frequent releases, Zep company-backed, 488 open issues |  |
| guozi-lab/llm-wiki-skill | R14 | C | MIT | zh | created 2026-09-03 and last commit the same day, no releases beyond v1.0.0, 0 open issues, single author group |  |
| jvdbreemen/llmwiki-kennisbank | R14 | B | MIT | en | created 2026-05-07; last commit 2026-10-12; releases v0.37.0 (2026-08-19) to v0.40.0 (2026-09-25); 0 open issues; 4 contributors, one (rv... |  |
| letta-ai/letta-code | R14 | B | Apache-2.0 | en | last commit 2026-10-19, releases about weekly, Letta Inc; 552 open issues |  |
| northtekdevs/genome | R14 | B | Apache-2.0 | en | created 2026-07-14, last commit 2026-10-01, one organisation (NORTHTEK), 6 open issues |  |
| radicle-dev/heartwood | R14 | B | MIT OR Apache-2.0 | en | last commit 2026-10-18; 6 open issues (sweep 2026-10-20); archived=False; repo created 2022-09-13; 52 contributors (top: cloudhead:1380,F... |  |
| xiplatform/governed-runtime-standards | R14 | C | Apache-2.0 | en | GitHub repository created 2026-10-15 (specs dated 2026-09-03), last commit 2026-10-15, single vendor (Renly, XiPlatform Pty Ltd, Australi... |  |
| anssi-fr/mla | R15 | B | LGPL-3.0 | en | created 2020-07-03; last commit 2026-10-01; releases in 2026; 12 open issues; maintained by ANSSI (French national cybersecurity agency);... |  |
| cryptomator/cryptolib | R15 | A | AGPL-3.0 | en | last commit 2026-10-14, Cryptomator organisation (Skymatic GmbH), 1 open issue |  |
| filosottile/age | R15 | A | BSD-3-Clause | en | last commit 2026-08-29, releases through 2026, one lead maintainer (Filippo Valsorda) plus Go team background |  |
| filosottile/typage | R15 | F | BSD-3-Clause | en | last commit 2026-08-28; 9 open issues (sweep 2026-10-20); archived=False |  |
| jedisct1/libsodium | R15 | A | ISC | en | last commit 2026-10-15; 0 open issues (sweep 2026-10-20); archived=False |  |
| open-source-cooperative/keyring-rs | R15 | A | Apache-2.0 | en | last commit 2026-10-18; 4 open issues (sweep 2026-10-20); archived=False |  |
| privy-io/shamir-secret-sharing | R15 | B | Apache-2.0 | en | last commit 2026-04-03; 11 open issues (sweep 2026-10-20); archived=False; repo created 2023-01-19; 7 contributors (top: benjreinhart:29,... |  |
| rfjakob/gocryptfs | R15 | A | MIT | en | last commit 2026-10-01, single maintainer (rfjakob), 67 open issues |  |
| sqlcipher/sqlcipher | R15 | A | BSD-3-Clause | en | last commit 2026-09-06; 9 open issues (sweep 2026-10-20); archived=False |  |
| str4d/rage | R15 | B | Apache-2.0 | en | last commit 2026-07-14, one maintainer (str4d) plus contributors, 72 open issues |  |
| automerge/automerge | R16 | A | MIT | en | last commit 2026-10-16; 113 open issues (sweep 2026-10-20); archived=False |  |
| automerge/automerge-repo | R16 | C | MIT | en | last commit 2026-10-18; 103 open issues (sweep 2026-10-20); archived=False |  |
| evoluhq/evolu | R16 | B | MIT | en | last commit 2026-10-20, SECURITY.md: 'This project is maintained by a single volunteer', 17 open issues |  |
| inkandswitch/keyhive | R16 | C | Apache-2.0 | en | last commit 2026-10-19; 26 open issues (sweep 2026-10-20); archived=False; repo created 2024-08-13; 7 contributors (top: jtfmumm:96,exped... |  |
| p2panda/p2panda | R16 | B | MIT OR Apache-2.0 | en | last commit 2026-10-20; 201 open issues (sweep 2026-10-20); archived=False |  |
| syncthing/syncthing | R16 | A | MPL-2.0 | en | last commit 2026-10-19; 389 open issues (sweep 2026-10-20); archived=False |  |
| worm-blossom/willow_rs | R16 | B | MIT OR Apache-2.0 | en | last commit 2026-09-23 ('Fix delegations encoding in EncodeMeadowcapAuthorisationToken'), repository updated 2026-10-16, 11 open issues; ... |  |
| alibaba/zvec | R17 | C | Apache-2.0 | en | last push 2026-10-20; 86 open issues; frequent beta releases; Alibaba-owned |  |
| asg017/sqlite-vec | R17 | C | Apache-2.0 | en | last commit 2026-05-18 (5 months), single author, 217 open issues, release line still alpha |  |
| breuert/scrydb | R17 | B | MIT | en | last commit 2026-08-27; 1 open issues (sweep 2026-10-20); archived=False; repo created 2026-07-27; 1 contributors (top: breuert:32) |  |
| huggingface/transformers.js | R17 | A | Apache-2.0 | en | last commit 2026-10-06; 279 open issues (sweep 2026-10-20); archived=False |  |
| lancedb/lancedb | R17 | A | Apache-2.0 | en | last commit 2026-10-19, company-backed (LanceDB Inc), 751 open issues, pre-1.0 versioning |  |
| oramasearch/orama | R17 | A | Apache-2.0 | en | last commit 2026-07-03, pushed 2026-10-18, company-backed (OramaSearch Inc), last release 2025-12-19, 35 open issues |  |
| quickwit-oss/tantivy | R17 | A | MIT | en | last commit 2026-10-17, Quickwit organisation, 484 open issues |  |
| stevenic/vectra | R17 | B | MIT | en | last commit 2026-05-25; 28 open issues (sweep 2026-10-20); archived=False |  |
| stffns/vstash | R17 | B | MIT | en | last commit 2026-09-02; 14 open issues (sweep 2026-10-20); archived=False; repo created 2026-03-20; 3 contributors (top: stffns:513,depen... |  |
| tobi/qmd | R17 | B | MIT | en | created 2025-12-08, last commit 2026-10-15, individual maintainer, 231 open issues |  |
| wangfenjin/simple | R17 | B | MIT OR GPL-3.0-or-later \|\... | zh | last commit 2026-05-17; 23 open issues (sweep 2026-10-20); archived=False |  |
| freedomofpress/sigstore-browser | R18 | B | Apache-2.0 | en | last commit 2026-09-28; 0 open issues (sweep 2026-10-20); archived=False; repo created 2025-11-11; 2 contributors (top: sachaservan:80,ls... |  |
| freedomofpress/tuf-browser | R18 | B | MIT | en | last commit 2026-02-14; 0 open issues (sweep 2026-10-20); archived=False; repo created 2025-07-15; 2 contributors (top: sachaservan:50,ls... |  |
| metamask/snaps-registry | R18 | A | MIT OR Apache-2.0 | en | last commit 2026-09-22; 36 open issues (sweep 2026-10-20); archived=False; repo created 2022-12-21; 34 contributors (top: Montoya:222,kha... |  |
| theupdateframework/tuf-conformance | R18 | A | MIT | en | last commit 2026-10-19; 19 open issues (sweep 2026-10-20); archived=False; repo created 2023-06-30; 9 contributors (top: jku:226,dependab... |  |
| ethz-spylab/agentdojo | R19 | A | MIT | en | last commit 2026-06-02; 80 open issues (sweep 2026-10-20); archived=False |  |
| huggingface.co/datasets/perplexity-ai/browsesafe-bench | R19 | B | MIT | en | dataset last modified 2025-12-04; Perplexity |  |
| huggingface.co/datasets/perplexity-ai/browsesafe-plus-plus | R19 | B | CC-BY-4.0 | en | dataset updated 2026-10-18; Perplexity |  |
| huggingface.co/datasets/umariqbal/web-agent-attack-benchmark | R19 | B | CC-BY-4.0 | en | dataset updated 2026-10-20 |  |
| llm-platform-security/intact | R19 | C | Apache-2.0 | en | last commit 2026-10-19; academic group (llm-platform-security); paper published 2026-10-15 |  |
| nanobrowser/nanobrowser | R19, R29 | B | Apache-2.0 | en | last commit 2026-10-15; v0.3.0 is a rewrite (WXT, Node 24, pnpm 10); 331 of roughly 370 contributions by one maintainer (contributors API... | yes |
| segev-shlomov/st-webagentbench | R19 | B | Apache-2.0 | en | last commit 2026-03-12 |  |
| bitwarden/clients | R20 | A | GPL-3.0-only AND OTHER:Bitw... | en | last commit 2026-10-19; company-backed; licence split flagged for legal review |  |
| keepassxreboot/keepassxc | R20 | A | GPL-2.0-only OR GPL-3.0-only | en | last commit 2026-10-20; 934 open issues (sweep 2026-10-20); archived=False |  |
| aaronius/penpal | R21 | A | MIT | en | last commit 2026-08-14; 0 open issues (sweep 2026-10-20); archived=False |  |
| endojs/endo | R21 | A | Apache-2.0 | en | HEAD 2026-10-14; 544 open issues; backed by Agoric and MetaMask (README says both rely on it to sandbox third-party plugins and mitigate ... |  |
| extism/extism | R21 | A | BSD-3-Clause | en | last commit 2026-10-09; releases frequent; Dylibso-backed [reported] |  |
| jetbrains/websandbox | R21 | B | Apache-2.0 | en | last commit 2026-10-08; 14 open issues (sweep 2026-10-20); archived=False; repo created 2016-01-13; 4 contributors (top: andrey-skl:204,J... |  |
| justjake/quickjs-emscripten | R21 | A | MIT | en | last commit 2026-07-23; 51 open issues (sweep 2026-10-20); archived=False |  |
| lavamoat/lavamoat | R21 | A | MIT | en | last commit 2026-10-09; 223 open issues (sweep 2026-10-20); archived=False |  |
| metaplex-foundation/mpl-core | R22 | A | OTHER:Metaplex-NFT-Open-Sou... | en | HEAD 2026-10-10; release 2026-10-07; 45 open issues; org metaplex-foundation |  |
| solana-foundation/rewards | R22 | B | MIT | en | HEAD 2026-10-05 (pushed 2026-10-15); created 2026-02-03; 2 open issues; org solana-foundation | yes |
| solana-foundation/solana-attestation-service | R22, R23 | B | MIT | en | last commit on clients/typescript 2026-10-02; repo HEAD 2026-10-06; 1 open issue |  |
| solana-labs/solana-program-library | R22, R24 | A | Apache-2.0 | en | Mythic copy HEAD 2026-03-10 (pushed 2026-10-02); upstream archived 2025-03-11 |  |
| solana-program/token-2022 | R22 | A | Apache-2.0 | en | HEAD 2026-10-20; releases 2026-10; org solana-program (Anza); 39 open issues |  |
| anza-xyz/wallet-standard | R23 | A | Apache-2.0 | en | last commit 2026-10-05; 10 open issues (sweep 2026-10-20); archived=False; repo created 2022-10-14; 13 contributors (top: jordaaash:709,o... |  |
| phantom/sign-in-with-solana | R23 | B | MIT | en | HEAD 2025-02-13; spec repo, stable; 6 open issues |  |
| regent-protocol/regent-solana-programs | R23, R30 | F | Apache-2.0 | en | search result shows last push 2026-10-04, 0 stars, created recently; nothing else checked |  |
| mythic-project/governance-program-library | R24, R26 | B | Apache-2.0 | en | HEAD 2026-03-23; 2 open issues; Mythic-Project | yes |
| mythic-project/oyster | R24 | A | Apache-2.0 | en | registry updated 2025-10-03 |  |
| squads-protocol/v4 | R24 | A | AGPL-3.0 | en | HEAD 2026-08-20 (pushed 2026-10-19); 26 open issues; no GitHub releases | yes |
| worldcoin/idkit | R25 | B | MIT | en | last commit 2026-10-19; 16 open issues (sweep 2026-10-20); archived=False; repo created 2025-10-28; 21 contributors (top: Takaros999:131,... |  |
| worldcoin/world-id-protocol | R25 | B | MIT | en | HEAD 2026-10-19; 74 open issues; World Foundation / Tools for Humanity |  |
| worldcoin/world-id-protocol-solana | R25 | C | MIT | en | HEAD 2026-10-19; created 2026-07-22; 0 open issues; Tools for Humanity org |  |
| continuous-foundation/credit-roles | R26 | B | MIT | en | last commit 2026-04-29; 2 open issues (sweep 2026-10-20); archived=False; repo created 2023-01-01; 1 contributors (top: rowanc1:15) |  |
| coordinape/coordinape | R26 | B | AGPL-3.0-only | en | HEAD commit 2026-01-09 (9 months before inspection); 99 open issues; no releases; funding.json present |  |
| givepraise/praise | R26 | B | GPL-3.0-only | en | HEAD commit 2024-10-14 (24 months before inspection); last release v0.13.1 2023-01-20; 80 open issues; used by TEC, Commons Stack, Giveth... |  |
| grimadas/meritrank | R26, R27, R28 | C | BSD-3-Clause | en | HEAD commit 2022-10-23; research code; poetry project |  |
| joincolony/colonynetwork | R26, R28 | B | GPL-3.0-only | en | HEAD commit 2026-03-24; 53 open issues; JoinColony org; colonyDapp client last commit 2024-01-04 |  |
| sourcecred/sourcecred | R26 | G | MIT OR Apache-2.0 | en | HEAD commit 2022-07-30; npm 0.11.2 published 2022-07-31; organisation wound down 2022; no maintainer activity since |  |
| jmiller4/plural-qf | R27 | C | NOASSERTION | en | HEAD commit 2023-12-04; single author (Joel Miller, per paper); research prototype |  |
| karma3labs/go-eigentrust | R27 | B | MIT | en | HEAD commit 2025-08-31; release v1.0 2023-05-31; 0 open issues; Karma3 Labs |  |
| kohler/hotcrp | R27 | A | MIT | en | HEAD commit 2026-10-16; single principal author (Eddie Kohler); in use at many conferences (not verified by me) |  |
| openreview/openreview-matcher | R27 | A | NOASSERTION | en | HEAD commit 2026-08-26; releases v2.0.6 and v2.0.7 on 2026-03-04; OpenReview production use for ML conferences (README says integration w... |  |
| deepfunding/dependency-graph | R28 | C | MIT | en | HEAD commit 2026-01-07; sibling repo deepfunding/oss-evals (MIT) pushed 2026-09-17; deepfunding/scoring pushed 2025-02-02 |  |
| drips-network/gardener | R28 | B | MIT | en | last commit 2026-09-28; 0 open issues (sweep 2026-10-20); archived=False; repo created 2025-09-11; 1 contributors (top: w-winter:38) |  |
| intersubjective/meritrank-rust | R28 | B | MIT | en | last commit 2026-10-06; 6 open issues (sweep 2026-10-20); archived=False; repo created 2023-12-06; 5 contributors (top: ichorid:242,autom... |  |
| huiliyi37/tianshu-harness | R29 | B | Apache-2.0 | multi | last commit 2026-10-19; v3.34.0 released 2026-10-19; 1,141 stars; 37 open issues; no published advisories; GitHub plus AtomGit mirror |  |
| atomgit.com/openeuler/community | R30 | G | MulanPSL-2.0 | multi | page showed newest change to sig/ about 23 hours old (relative time only); about 11,150 commits; 491 open issues, 57 pull requests |  |
| belenios/belenios | R30 | B | AGPL-3.0-or-later | en | created 2012 copyright line, last commit 2026-10-16; releases 2.5.1 and 3.0 in 2024; maintained by Inria and CNRS (French public research... |  |
| loomio/loomio | R30 | A | AGPL-3.0 | en | last commit 2026-10-19; release 2026-10-15; 65 open issues; run by the Loomio Cooperative (loomio-coop-handbook repository) |  |
| rust-lang/rfcs | R30 | A | Apache-2.0 | en | last commit 2026-10-05; 800 open issues (sweep 2026-10-20); archived=False |  |
| sigstore/rekor-tiles | R30 | B | Apache-2.0 | en | last commit 2026-10-19; 27 open issues; part of Sigstore (OpenSSF); the design and proposal documents are in access-controlled Google Doc... |  |
