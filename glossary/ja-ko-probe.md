# Japanese and Korean probe term bank (Stage 2 tripwire)

- Languages: Japanese (ja), Korean (ko)
- Date: 2026-10-20
- Agent: s2-probe-jako
- Scope: R01, R02, R10, R11, R12, R14, R19, R22 only (P0 breadth set)
- Status: probe complete (about 55 tool calls). Mini term bank plus a documented decision per language.

## Method summary

1. GitHub repository search with native terms (`gh api -X GET search/repositories -f q=...`). Note: `-f` without `-X GET` turns the call into a POST and returns 404. Multiword Japanese queries nearly always return 0 (no word segmentation); single words or two short words work. Shared 30/min search limit was hit several times (403); I waited and re-ran.
2. Qiita API (`https://qiita.com/api/v2/items?query=TERM&per_page=8`): works anonymously, returns JSON; multiword queries are ANDed.
3. Zenn: only `https://zenn.dev/api/search?q=TERM&source=articles&order=daily` filters by query (the `/api/articles?q=` form ignores `q` and returns the latest articles). Sparse results.
4. J-STAGE: `https://www.jstage.jst.go.jp/result/global/-char/ja?globalSearchKey=TERM` returns HTML (parse `<a href=".../article/...">`); works with a browser User-Agent. Result count appears as `N件`.
5. KCI: working query shape is a POST to `https://www.kci.go.kr/kciportal/po/search/poArtiSearList.kci` with form fields `poSearchBean.searType=all`, `poSearchBean.startPg=1`, `poSearchBean.docsCount=10`, `poSearchBean.queryText=TERM`, `poSearchBean.printKeyword=TERM`, `poSearchBean.isAdvanceSearch=false`, `searchLogBean.searchType=01`. A GET with an unknown parameter name returns the whole database (a total of 5000 shown is a cap, not a hit count). Titles are in hidden inputs `R_INDE_TITL`.
6. WebSearch (two Korean/Japanese queries) as a cross-check for what the web surfaces.
7. Candidate repositories were inspected through the API only: repository metadata, HEAD SHA, root listing, `tests/` listing, README head. Nothing cloned, nothing run.
8. Blog posts are leads to code, not evidence.

## Platforms consulted

| Platform | Result | Note |
|---|---|---|
| GitHub search/repositories (ja, ko) | ok, rate-limited | tokenisation weak for CJK; 30 searches/min shared |
| Qiita API v2 | ok (anonymous) | 60 requests/hour limit not reached (about 15 calls) |
| Zenn `/api/search` | ok, sparse | many valid queries return 0 |
| J-STAGE global search | ok (HTML) | results irrelevant for all 8 requirements |
| KCI poArtiSearList | ok via POST | titles only; no code links in anything returned |
| PyPI JSON | ok | used to check one package identity |
| WebSearch (ko, ja) | ok | surfaced English-language packages for the Korean R11 query |

## Table 1: core concepts (verified usage only)

Evidence tags: [I] opened, [R] snippet or listing. All seen 2026-10-20.

| Concept | Req IDs | Japanese (verified in use) | Korean (verified in use) | Loanword / English kept | Evidence | Conf. |
|---|---|---|---|---|---|---|
| Capability token / attenuation / delegation | R01 | none for object-capability; 権限委譲, 委譲, 認可 appear in generic authorization posts | none found | Capability, Macaroons, Biscuit, UCAN, Cedar, OPA all stay English | Qiita/Zenn hits for Macaroons and UCAN: 0 relevant; ケーパビリティ on GitHub = Linux process capabilities only [I] | low |
| Revocation | R01, R22 | 失効 (token, certificate), 取り消し | 폐기 (credential), 폐지 | Revoke | github Byeongwook-Heo/vault-security-portal "자격증명 요청·승인·폐기·감사" [R]; claude-context-guard "プロンプトキャッシュ失効" [R] (unrelated sense) | medium |
| Sandbox / containment | R02 | サンドボックス, 隔離, 子プロセス | 샌드박스, 격리 | Seatbelt, Landlock, bubblewrap, gVisor, Firecracker, microVM | https://zenn.dev/libercraft/articles/20260918-agent-sandbox-seatbelt-landlock [I]; github fukui-yuto/agentbox [I] | high (JA); medium (KO) |
| Durable execution / workflow engine | R10 | 耐久実行 (title of a Qiita post on Temporal), 冪等性, チェックポイント, 再開 | none found (워크플로 엔진 0 hits) | Temporal, Durable Execution, Workflow | https://qiita.com/Yushi88/items/feff904869406839eee7 [R]; https://qiita.com/Ikegamik_genee/items/a628f20cd7fe262cbeb4 [I] (heartbeat, resume) | medium (JA); low (KO) |
| Audit log / tamper evidence | R11 | 監査ログ, 改ざん検知, 改ざん耐性, ハッシュチェーン, 台帳, 証跡 | 감사 로그, 변조 방지, 해시 체인 | Audit trail, append-only, Merkle | github totsuka-code/checksum-registry [I] ("SHA-256台帳"); USHIKUNDESUYO/sekisho ("ハッシュチェーン証跡") [I]; egoring/browser-guard-mcp ("감사 로그") [I] | high |
| Provenance / attestation | R12 | 来歴 (not used in software hits), プロベナンス (geology only on J-STAGE), 署名, 証明 | 출처 증명 (0 hits), 프로비넌스 (0) | Provenance, SLSA, in-toto, Sigstore, npm provenance ("provenance 付き" in a Qiita title) | https://qiita.com/kai_kou/items/d5439854aa8ac19bf5f3 [R] | low |
| Selective disclosure | R12 | 選択的開示 (medicine and accounting on J-STAGE; ZKP demo uses ゼロ知識証明) | 선택적 공개 (0 hits) | Selective Disclosure, SD-JWT, mDL, ZKP | github grandchildrice/longfellow-demo [R]; J-STAGE 15 irrelevant hits | low |
| Staged knowledge promotion | R14 | 昇格 (Promotion), ナレッジ, 出典 | none found | Promotion, Knowledge base | github hyt-sasaki/ai-knowledge-promoter [R] | low |
| Browser-agent action gating | R19 | 承認ゲート/承認フロー, プロンプトインジェクション, ブラウザ操作 | 승인 게이트, 허용목록 (allowlist), 읽기 전용, 프롬프트 인젝션 | Prompt injection (katakana), allowlist, MCP, Playwright | github egoring/browser-guard-mcp [I]; KCI 6 prompt-injection papers [R] | medium (KO), low (JA) |
| Soulbound / non-transferable token | R22 | ソウルバウンドトークン (SBT), 譲渡できないNFT, NTT (ERC-4671) | 소울바운드 (0 hits), 양도 불가 (0 hits) | SBT, ERC-4671, ERC-5516, Token-2022 | https://qiita.com/cardene/items/7acca8927401cbe8491c [R]; https://zenn.dev/tailorworks_pd/articles/a45572d9fdd6a4 [R]; EVM only | medium (JA); low (KO) |

## Table 2: search strings per requirement

Tested = returned results as noted in the ledgers.

| Req | Japanese | Korean | Best platforms |
|---|---|---|---|
| R01 | `ケーパビリティ トークン 失効` (Qiita, 2 hits); `権限委譲 エージェント` (GitHub 0) | `권한 위임 폐기 토큰` (GitHub 0; KCI empty) | none productive; use English on global platforms |
| R02 | `サンドボックス エージェント` (GitHub 5); `サンドボックス Landlock` (Zenn 1) | `샌드박스 에이전트` (GitHub 4; KCI returns regulatory sandbox papers, add `격리`) | GitHub, Zenn |
| R10 | `Temporal 耐久実行` (Qiita 9); `冪等性 チェックポイント エージェント` | `워크플로 엔진 재시작` (0) | Qiita (commentary only) |
| R11 | `ハッシュチェーン` (GitHub 2); `監査ログ 改ざん` (GitHub 2); `改ざん検知 監査ログ ハッシュチェーン` (Qiita 8) | `감사 로그` (GitHub 16); `감사 로그 해시` (0) | GitHub (single words) |
| R12 | `選択的開示` (0 relevant); `ゼロ知識証明` (GitHub 10); `Sigstore 来歴` (Qiita 8) | `선택적 공개 자격증명` (0) | GitHub (ZKP), Qiita (supply-chain commentary) |
| R14 | `ナレッジ 昇格` (GitHub 1) | `승인 게이트 에이전트` (GitHub 6, generic) | GitHub |
| R19 | `プロンプトインジェクション ブラウザ` (0); `ブラウザエージェント プロンプトインジェクション` (Qiita 6) | `브라우저 자동화 허용목록` (GitHub 1, browser-guard-mcp); `프롬프트 인젝션` (KCI 6) | GitHub (KO), KCI (papers) |
| R22 | `ソウルバウンドトークン` (Qiita 8, EVM); `譲渡不可` (0) | `소울바운드` (0); `양도 불가 토큰` (0) | Qiita (EVM explainers only) |

## Rejected terms

| Term | Reason |
|---|---|
| ケーパビリティ (as object capability) | GitHub hits are Linux process capabilities and a game; J-STAGE hits are manufacturing/business capability |
| 내구성 실행 (durable execution, ko) | no use; KCI returns unrelated education papers |
| 来歴 / プロベナンス (provenance) in software | J-STAGE hits are geology; no software provenance texts found; practitioners write "provenance" or "SLSA" in English |
| 소울바운드, 양도 불가 토큰, 선택적 공개 (ko) | 0 repositories, 0 papers |
| 샌드박스 alone (ko) on KCI | dominated by 규제샌드박스 (regulatory sandbox) law papers |
| 選択的開示 (ja) | in use only in medicine and accounting; ZKP demos say ゼロ知識証明 |
| `-f` GitHub search without `-X GET` | not a term; a method note: it POSTs and returns 404 |

## What practitioners keep in English

Capability/attenuation names (Macaroons, Biscuit, UCAN, Cedar), Temporal/Durable Execution, Sigstore/SLSA/in-toto, SD-JWT/mDL, MCP, Playwright, Seatbelt/Landlock/bubblewrap/gVisor/Firecracker. Katakana and Hangul transliterations (プロンプトインジェクション, 프롬프트 인젝션, サンドボックス, 샌드박스) are the native form for concepts that came with the 2023-2026 agent wave.

## Platform notes

- GitHub: Japanese or Korean words match the repository description only when a word is a whole token in the description; two-word queries are ANDed and usually return 0. Prefer one word per call. Low-star hobby repositories dominate every hit list (all repositories found have 0-1 stars, one maintainer, and a single day of commits).
- Qiita: the query is ANDed; titles are commentary on English-language tools. Open the article body through `GET https://qiita.com/api/v2/items/ID` and regex for `github.com` links; the two articles checked had no relevant code link (one linked to a hobby app, Kurari).
- Zenn: only the `/api/search` endpoint filters.
- J-STAGE: HTML only; treat every hit as a paper that must carry a code link to count; none did.
- KCI: see Method item 5.

## Decision

### Japanese: tripwire does NOT fire (borderline on the literal rule)

Leads that point to real code with a Japanese-only README, found only through Japanese queries:

1. totsuka-code/checksum-registry (R11, R12). Local FastAPI hash ledger with Ed25519 signatures and anchor output, pytest suite, no licence file, one day of commits.
2. fukui-yuto/agentbox (R02). Docker/gVisor/Firecracker Python sandbox, Apache-2.0, tests per backend; PyPI package identity unverified; Python code execution, not child-process confinement from Node.
3. USHIKUNDESUYO/sekisho (R11, R19 flavour). Hash-chain trail plus human pass token, MIT; depends on Gemini and Cloud Run.
4. hyt-sasaki/ai-knowledge-promoter (R14). Firestore-backed, no licence; excluded.

Why this does not fire: counted literally, items 1 to 3 satisfy "two or more independent real-code leads with a non-English README". They are not what the rule is meant to detect: each is a single-author, single-day hobby or hackathon repository (0 stars, no releases), each is outclassed or matched by an English-findable alternative the English branches already search (Trillian, Rekor, immudb, bubblewrap, Landlock, Extism), none meets a requirement constraint (Node embeddable, three desktop OSes, no cloud), and none came from J-STAGE, Qiita or Zenn leads (those produced commentary on English-language tools and no code). No Japanese government, research-lab or company project with serious maintenance turned up for any of the eight requirements. Recommendation: no full Japanese language agent in pass 2. If the lead wants a cheap safeguard, one 10-15 call sweep reusing the single-word GitHub queries in Table 2 for R01, R10 and R22, where the probe found nothing at all, is enough. Reversal condition: a Japanese-only repository with 12 months of history or an institutional maintainer appears for any P0 requirement.

Queries run: 22 Japanese GitHub queries (about 8 rate-limited and re-run), 15 Qiita API queries, 7 Zenn queries, 12 J-STAGE queries, 1 WebSearch. All recorded in `ledger/negative-s2-probe-jako.jsonl` or as rows in `ledger/discovery-s2-probe-jako.jsonl`.

### Korean: tripwire does NOT fire

Leads: egoring/browser-guard-mcp (R19: allowlist, read-only default, audit log; tests and CI; MIT; one month of history) has a `README.en.md`, so by the rule it is already findable in English and does not count; devcy0922/aegis-llm (R19) is a keyword-matching prototype with no licence (excluded); OmniOneID (Korean government-backed Open DID stack, Apache-2.0, 42 repositories, active in October 2026) has an English README with Korean twin, so it does not count but is a real lead for R12/R23 (Java, DID/VC/VP; selective-disclosure support unverified; Hyperledger Fabric and Besu, not Solana). A Korean R11 web query returned only English-language packages (halo-record, Sasana, RootSign). KCI returned papers on prompt injection, a DAO reward model and regulatory sandboxes, with no code links in any of them. Fewer than two Korean-only code leads exist. Recommendation: no full Korean language agent. Hand OmniOneID and browser-guard-mcp to the English-side branch agents (F/C for OmniOneID, E for browser-guard-mcp).

Queries run: 13 Korean GitHub queries (some rate-limited and re-run), 10 KCI queries, 1 WebSearch. Recorded in the ledgers.

### Caveats

- GitHub recall for CJK is poor, so absence is weak evidence; the decision rests on the quality of what was found and on the absence of serious projects in the cross-checks (WebSearch, Qiita, KCI), not on emptiness alone.
- I did not search Gitee-like Japanese or Korean forges (Japanese: none known; Korean: no anonymous national forge identified) or Velog, Naver D2, Tistory, Note.com (HTML-only, bot-walled risk; not probed).
- README contents of longfellow-demo and ai-knowledge-promoter were not opened.
