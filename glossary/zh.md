# Chinese term bank (zh) for ResonantOS / ResonantDAO Stage 2

- Language: Chinese (simplified first; traditional variants noted)
- Date: 2026-10-20
- Agent id: s2-term-zh

## Method summary

1. Read gaps.md (R01-R30 plus 16 core concepts) and platform-urls.md.
2. For each concept, ran Chinese queries via WebSearch restricted to Chinese practitioner domains (juejin.cn, blog.csdn.net, zhuanlan.zhihu.com, cnblogs.com, segmentfault.com, 51cto.com, jianshu.com, infoq.cn; for DAO terms also panewslab.com, foresightnews.pro, 8btc.com, chaincatcher.com; for Taiwan ithelp.ithome.com.tw, ithome.com.tw). A domain-restricted query works well; an unrestricted query returns mostly English pages (the tool is US-only).
3. Ran GitHub repository search via `gh api -X GET search/repositories` with Chinese queries, and GitCode (AtomGit) search pages via WebFetch.
4. Opened (inspected) a small set of articles to read the exact Chinese wording. Several CSDN pages returned 403 or ECONNRESET to WebFetch, so those items are "reported" (seen only in a search result with snippet).
5. Disconfirmation: for each native term, looked for technical usage vs dictionary/translation use. Terms with no hit are in the Rejected section.
6. Gitee and OpenI could not be searched usefully without a browser session (see platform table). Evidence therefore leans on CSDN, Juejin, Zhihu, cnblogs, GitHub and GitCode. No Gitee-hosted repository is cited as evidence.

Evidence labels: "inspected" = I opened the page and read the term in context; "reported" = seen in a search result title/snippet only. All "seen" dates are 2026-10-20. Machine translation is marked MT.

## Platforms consulted

| Platform | Result | Note |
|---|---|---|
| WebSearch with Chinese domain filter | ok | best discovery route; unfiltered queries give English |
| CSDN / Juejin / Zhihu / cnblogs / SegmentFault / jianshu | ok via search; direct fetch partly blocked | juejin fetch ok; zhihu zhuanlan 403 (one test); CSDN 403 and ECONNRESET on two fetches |
| GitHub (gh api) | ok, rate-limited lightly | 30 queries in 75 s with 2.5 s spacing, no 403 |
| GitCode / AtomGit (gitcode.com) | ok | anonymous search pages render; results are largely GitHub mirrors |
| Gitee (gitee.com) | blocked / empty | web search 301-redirects to so.gitee.com, which returns only a heading to WebFetch; api/v5/search/repositories returned HTTP 200 with `[]` for every query (anonymous); api/v5/repos/{owner}/{repo} works anonymously |
| OpenI (openi.pcl.ac.cn) | ok for landing, gated for search | Gitea-based forge (footer says so); explore pages show a usage-agreement gate ("Agree and continue") to WebFetch |
| OpenI (openi.org.cn) | empty | HTTP 200 but no content to WebFetch (SPA); treat as portal, not verified as forge |
| CNKI (oversea.cnki.net) | empty | search shell loads, no result list, no login prompt; metadata not obtainable via WebFetch |
| Hugging Face / arXiv Chinese-abstract check | not done | time box; arXiv appeared only in English results |
| Taiwan media (ithome.com.tw, ithelp) | ok | used for traditional-variant check |

## Table 1: core concepts

Confidence reflects how well the Chinese wording is attested in practitioner text, not how good the concept is.

| Concept | Req IDs | Native term(s) | Loanword / abbreviation usage | Evidence (URL, seen 2026-10-20, status) | Conf. | Notes |
|---|---|---|---|---|---|---|
| Capability token / object capability | R01, R03, R20, R21 | 基于能力的安全; 能力表 (capability list); 授权令牌; 最小权限 | Macaroons, Biscuit, UCAN, capability usually left in English; "caveat" untranslated | https://blog.csdn.net/efc12345678/article/details/152706995 (CSDN, title "基于能力的安全与微服务API安全部署", reported); https://blog.csdn.net/gitblog_00047/article/details/138948098 (CSDN, Biscuit "认证/授权令牌", reported); https://juejin.cn/post/7696696661667725348 (Juejin, "least agency", Agent credentials, reported) | medium | "对象能力" returned 0 GitHub hits and no Chinese blog; search "Macaroons" + "UCAN" in English with Chinese context words. Mainland text rarely says 能力令牌 (rejected). |
| Attenuation | R01 | 衰减 (appears as "令牌衰减" only in my query, not in a hit); 缩小权限 / 收窄权限; 追加限制条件 | "attenuation" kept in English, "caveat" kept in English or "限制条件"/"警告" | https://blog.csdn.net/gitblog_00047/article/details/138948098 (reported; summary says attenuation described offline permission narrowing); https://blog.csdn.net/efc12345678/article/details/152706995 (reported; "带有警告的令牌" for caveat) | low | No source found that uses 衰减 as a technical noun for attenuation. Search the English word plus 令牌. |
| Revocation | R01, R18, R22 | 撤销; 吊销 (certificates, JWT); 失效 (token invalidation); 黑名单 (JWT deny list) | "revocation list", "CRL"; "即时失效" | https://blog.csdn.net/gitblog_00518/article/details/153307991 (CSDN, JWT revocation and blacklist, reported); https://zhuanlan.zhihu.com/p/623043153 (Zhihu, "让 jwt token 主动失效", reported) | high | Practitioners use 失效 / 黑名单 for tokens, 吊销 for certificates, 撤销 for delegations and credentials. |
| Sandbox / containment | R02, R21 | 沙箱 (mainland); 沙盒 (Taiwan, HK); 隔离; 容器隔离; 进程隔离 | gVisor, Firecracker, bubblewrap (bwrap), Landlock, seccomp, Seatbelt, AppContainer, Job Object (作业对象), Wasmtime, WASI kept in English; "OS 级隔离" | https://zhuanlan.zhihu.com/p/2049959768517824552 (Zhihu, "沙箱怎么做-Codex三平台OS级隔离的工程实现", reported; fetch 403); https://juejin.cn/post/7673436957741285391 (Juejin, "Landlock/bwrap/Seatbelt 多后端", reported); https://www.cnblogs.com/ljbguanli/p/19761604 (cnblogs, AppContainer "应用容器", reported); https://gitcode.com/search?q=沙箱&type=repo (GitCode, 108 repos incl. OpenSandbox, forkd; inspected) | high | Windows terms: 应用容器 (AppContainer), 作业对象 (Job Object), 受限令牌. "sandbox runtime" often left English. |
| Durable execution / workflow engine | R10, R04 | 持久化执行; 工作流引擎; 持久化工作流; 工作流编排 | Temporal, Workflow, Activity kept in English; "durable execution" also used; 重放 (replay); 幂等 (idempotency); 幂等键; 定时器 | https://juejin.cn/post/7691537931249795112 (Juejin, title "从 async/await 到持久化执行…Temporal", inspected: 持久化执行, 工作流, 重放, 确定性重放, 幂等键, 定时器; "Activity" untranslated; no word 检查点); https://blog.csdn.net/m0_47495420/article/details/141116697 (CSDN "【Temporal】工作流程引擎", reported); https://www.infoq.cn/article/dLEP0OfOTS18WPvOCLYb (InfoQ China "AI Agent 持久化方案", reported) | high | 检查点 for checkpoint was not in the inspected article; use 进度持久化 / checkpoint in mixed queries. |
| Event sourcing / audit log | R11, R14 | 事件溯源; 审计日志; 仅追加; 哈希链; 防篡改; 透明日志 (certificate transparency log: 证书透明化日志); 签名树头 (STH); 包含证明 / 审计证明; 一致性证明 | Event Sourcing, CQRS, Merkle Tree, Trillian, immudb, Rekor in English; "append-only" sometimes kept | https://blog.csdn.net/qq_16681169/article/details/81605250 (CSDN "事件溯源Event Sourcing", reported); https://www.cnblogs.com/YYRise/p/11780205.html (cnblogs "证书透明化日志工作原理", reported); https://zhuanlan.zhihu.com/p/647939898 (Zhihu "Merkle树方案，检测与防日志篡改", reported); https://www.jianshu.com/p/6b27fec81a4f (jianshu "immudb: 不可篡改的数据库", reported) | high | "事件溯源" is the CQRS software-pattern meaning; for security audit logs use 审计日志 + 防篡改 + Merkle. GitHub 审计日志 哈希链 防篡改 gave 1 unrelated hit. |
| Provenance / attestation | R12, R18 | 溯源; 来源可追溯; 来源链; 证明 (attestation, usually with English in brackets); 制品溯源 | provenance and attestation kept in English in supply-chain text; in-toto, SLSA, Sigstore, cosign, DSSE; C2PA "内容凭证" | https://blog.csdn.net/qq_45239623/article/details/163862725 (CSDN "供应链安全：SLSA、SBOM 与制品 provenance", reported); https://blog.csdn.net/weixin_29091837/article/details/164160870 (CSDN "C2PA内容凭证", reported); https://segmentfault.com/a/1190000041860506 (SegmentFault Sigstore, reported) | medium | The in-toto article writes "attestation（证明）". For AI-content provenance the national standard GB 45438-2025 (标识方法, 显式/隐式标识) is the local vocabulary (reported via https://www.51cto.com/aigc/7510.html). |
| Selective disclosure | R12, R23 | 选择性披露; 选择性公开 (not verified); 最小披露 | SD-JWT, BBS, VC, VP (可验证表达); 盐值哈希 | https://github.com/helailiang/go-did-jwt-vp-demo (GitHub repo, description "sd-jwt、bbs、merkle 生成选择性披露VP示例", reported via API); https://blog.csdn.net/koudan567/article/details/125130399 (CSDN "理解W3C可验证凭证", reported); Taiwan MODA wallet deck via https://www-api.moda.gov.tw/File/Get/moda/zh-tw/wDQCCuTxqFMgIBt (reported; traditional "選擇性揭露") | medium | Taiwan: 選擇性揭露, 數位憑證皮夾, 可驗證憑證 VC, 分散式識別符 DID. Mainland: 去中心化身份 / 去中心化标识符. |
| Local-first | R13, R16, R29 | 本地优先 | Local-first, CRDT (kept English), Automerge, Yjs, Loro | https://github.com/NanmiCoder/cc-haha (GitHub, "本地优先的跨平台 Claude Code / AI Agent 桌面工作台", 15k stars, reported via API); https://github.com/ChatLab/ChatLab (reported); https://github.com/chenhz01/local-first-crdt (GitHub, "本地优先软件与 CRDT 同步十讲", reported) | high | Also 离线优先, 数据主权, 数据自主 (sovereign) appear in prose but were not searched separately. |
| Soulbound / non-transferable token | R22, R25 | 灵魂绑定代币; 灵魂绑定通证 (CSDN, uses 通证); 不可转让; 灵魂绑定 | SBT, Soulbound, Token-2022 NonTransferable (English), NFT | https://www.panewslab.com/zh/articles/u4ecllbk (PANews, inspected: 灵魂绑定代币, 不可转让, 账户恢复, 社交恢复模型; no word 撤销 in article); https://blog.csdn.net/xfilesystem/article/details/126971728 (CSDN "灵魂绑定通证SBT", reported); https://zhuanlan.zhihu.com/p/549080139 (Zhihu "Soulbound(灵魂绑定)", reported); https://github.com/0xlfhuang/opencode-lfhuang-SBT (GitHub, "铸造SBT(Soul Bound Token)灵魂绑定代币", reported) | high | One Zhihu title has the typo 灵幻绑定代币 (reported, https://zhuanlan.zhihu.com/p/568818820): typo, do not use. Solana-specific Chinese text on Token-2022 non-transferable was not found. |
| DAO governance | R24, R30, R23 | 去中心化自治组织; DAO 治理; 链上治理; 链下投票; 提案; 国库 / 财库; 多签 (multisig); 时间锁 | DAO, Snapshot, Realms, Squads, Tally, "1 Token 1 Vote" | https://zhuanlan.zhihu.com/p/474431449 (Zhihu "DAO投票平台Snapshot", reported); https://foresightnews.pro/article/detail/23814 (Foresight "Top10 DAOs 财库管理和社区治理路径", reported); https://foresightnews.pro/article/detail/17211 (Foresight "多签钱包再多签", Squads, reported); https://github.com/drdgit/dao-talent-mesh-protocol (GitHub, "去中心化自治组织（DAO）驱动…", reported) | high | 财库 (mainland crypto media) and 国库 both used. Realms/spl-governance: no Chinese technical article found (see rejected/unfound). |
| Quadratic funding / collusion resistance | R25, R27 | 二次方资助 (also 二次融资); 二次方投票; 抗合谋 / 抗共谋 / 反勾结; 女巫攻击; 抗女巫 / 防女巫 | QF, MACI ("极简抗共谋基础设施"), Gitcoin Passport | https://zhuanlan.zhihu.com/p/348853751 (Zhihu "Vitalik：Gitcoin二次融资回顾", reported); https://blog.csdn.net/gitblog_00045/article/details/139540234 (CSDN "推荐：MACI - 极简抗共谋基础设施", reported); https://www.8btc.com/media/6674807 (8btc "综述｜二次方投票与公共物品", reported); https://zhuanlan.zhihu.com/p/356667881 (Zhihu "女巫攻击", reported) | high | Variant spellings: 合谋 / 共谋 / 勾结 / 串通. Both 二次方资助 and 二次融资 (Vitalik translation) are in use; search both. |
| Reputation | R26, R27, R28 | 声誉; 声誉系统; 信誉 (credit/trust, mainland platforms); 声望 | Reputation, cred (SourceCred), Karma | https://www.panewslab.com/zh/articledetails/n870h340.html (PANews "DAO赛道九大方向…" mentions Karma 声誉系统, reported); https://foresightnews.pro/article/detail/4065 (Foresight "Vitalik 最新论文全文…去中心化社会", reported); https://zhuanlan.zhihu.com/p/516156959 (Zhihu "DAO的贡献者漏斗", reported) | medium | 信誉 collides with credit-score contexts (征信); prefer 声誉 for DAOs. SourceCred/Coordinape/Hypercerts: no Chinese technical article found. |
| Agent framework / multi-agent | R07, R29 | 智能体 (mainland); 智能体框架; 多智能体; 代理 / AI 代理 / 代理人 / 數位代理人 (Taiwan); 编排; 协作 | Agent, harness, LangGraph, AutoGen, CrewAI, A2A, "Agent Skills" | https://github.com/kobolingfeng/ntk (GitHub "多智能体框架", reported); https://zhuanlan.zhihu.com/p/1984725399767376336 (Zhihu "Agent 框架横向对比", reported); https://www.ithome.com.tw/article/174569 (iThome Taiwan "數位代理人…AI Agent", reported); https://ithelp.ithome.com.tw/articles/10422702 (iThome "多代理（multi-agent）分工", reported) | high | Mainland 智能体, Taiwan 代理 / 代理人 / 多代理. Many mainland articles write "Agent" untranslated. |
| Browser automation / extension security | R05, R19, R20, R21 | 浏览器自动化; 浏览器智能体; 扩展 (mainland) / 擴充功能 (Taiwan); 内容脚本; 提示词注入 / 提示注入; 间接提示注入; 人工确认 | browser-use, Playwright MCP, Native Messaging (原生消息传递), Manifest V3, MV3, prompt injection | https://www.cnblogs.com/gccbuaa/p/19192689 (cnblogs "Native Messaging的安全风险与防御", reported); https://juejin.cn/post/7493730335193677836 (Juejin "本地应用与浏览器插件通讯方式…原生消息传递和本地Web服务器", reported); https://blog.csdn.net/weixin_42230607/article/details/160536016 (CSDN "AI智能体安全攻防：从提示注入到工具滥用", reported); https://www.ithome.com.tw/news/173028 (iThome Taiwan "ChatGPT Atlas代理模式…提示詞注入", reported) | high | Mainland says 插件 (plugin) for Chrome extensions more often than 扩展; search both. Taiwan: 提示詞注入. |
| MCP | R06, R14, R19 | 模型上下文协议; MCP 服务器 / MCP 服务; 工具调用; 用户确认 / 人工确认; 工具投毒; MCP 网关 | MCP, Model Context Protocol, "Tool Poisoning", OAuth 2.1 | https://github.com/yeuxuan/Ace-Mcp-Node (GitHub "Model Context Protocol (MCP) 服务器", reported); https://juejin.cn/post/7696452097274150975 (Juejin "MCP网关技术图谱2026", reported); https://juejin.cn/post/7640242663186481193 (Juejin "MCP 工具投毒", reported); https://zhuanlan.zhihu.com/p/29001189476 (Zhihu "MCP (Model Context Protocol)，一篇就够了", reported) | high | Taiwan: 模型上下文協定 (reported only on a Novita zh-TW page). 257 GitHub repos match "Model Context Protocol MCP 服务器". |

## Table 2: per-requirement search strings

Notation: strings are ready to paste. Gitee web search is not usable anonymously (see platform notes); use GitCode, GitHub and the Chinese article sites. "GH" = GitHub, "GC" = GitCode/AtomGit, "Art" = Juejin/CSDN/Zhihu/cnblogs/SegmentFault.

| Req | Search strings | Likely platforms | Notes |
|---|---|---|---|
| R01 | `Macaroons 授权令牌 caveat` ; `Biscuit 授权令牌 去中心化 Datalog` ; `UCAN 能力 委托 撤销` ; `基于能力的安全 令牌 委托` ; `Cedar OPA Rego 授权引擎 Node` ; `令牌吊销 会话中途 撤销授权` | Art, GC, GH | "能力令牌" gives GitHub noise (35 irrelevant hits). "UCAN" collides with an unrelated Java RBAC admin project (cenlm/ucan-admin). |
| R02 | `AI Agent 沙箱 bubblewrap Landlock seccomp` ; `沙箱 gVisor Firecracker 隔离` ; `Windows AppContainer Job Object 沙箱` ; `macOS Seatbelt sandbox-exec 沙箱` ; `WebAssembly 沙箱 Wasmtime Extism` ; `Codex 沙箱 三平台 OS级隔离` | Art, GC, GH | Strongest-covered term. GC "沙箱" returns 108 repos. 沙盒 for Taiwan. |
| R03 | `凭证代理 注入 API Key 不暴露 Agent` ; `密钥代理 出口代理 Vault 动态凭证` ; `让 Agent 看不见密钥` ; `LiteLLM 虚拟密钥 master key` ; `Agent 提交意图 Broker 持有密钥` | Art | Inspected: Juejin 7646606448857333796 uses 凭证代理, 凭证保险库, 注入, 审计. SPIFFE/SPIRE not searched in Chinese. |
| R04 | `进程守护 崩溃自动重启 看门狗` ; `Supervisor 进程监控 自动重启` ; `Electron 应用 自动更新 回滚` ; `崩溃循环 回滚 已知良好版本` ; `监督树 Erlang OTP` | Art, GH | Weak: only generic daemon/watchdog articles found. "已知良好版本 / 回滚" gave nothing specific; "监督树" not verified. |
| R05 | `Chrome 扩展 localhost 本地服务 安全 跨域` ; `Native Messaging 安全风险 allowed_origins` ; `本地 Web 服务器 浏览器插件 通讯 安全` ; `Jupyter token 本机 CSRF 防护` | Art | The Juejin comparison article (7493730335193677836) is the closest hit. |
| R06 | `MCP 工具调用 用户确认 审批` ; `MCP 网关 鉴权 OAuth 工具权限` ; `模型上下文协议 MCP 服务器 TypeScript SDK` ; `MCP 工具投毒 防护` ; `Claude Desktop Cursor MCP 允许一次` | Art, GH, GC | Chinese practitioners describe Claude Desktop prompts as "Allow once / Allow for this chat" in English. |
| R07 | `智能体框架 多智能体 运行时 适配器` ; `A2A 协议 Agent2Agent 互操作` ; `LangGraph AutoGen CrewAI 对比` ; `agent-protocol 智能体互操作协议` ; `Agent 运行时 可替换 harness` | Art, GC, GH | GC hits: openJiuwen/agent-protocol (MCP+A2A C++ SDK). Taiwan: 多代理, 代理人. |
| R08 | `LiteLLM 网关 故障转移 fallback` ; `多模型 路由 Anthropic 原生 Gemini 原生` ; `LLM 网关 选型 OpenRouter Portkey` ; `Vercel AI SDK provider 切换 模型` ; `API 中转 负载均衡 密钥轮询` | Art | Chinese LLM-gateway scene is large (Dify, "中转站"). Native wire-format discussion was thin. |
| R09 | `SKILL.md 技能 规范 渐进式披露` ; `Agent Skills 官方规范 落地` ; `技能 frontmatter name description` ; `Skills 多运行时 兼容 Codex Claude Code` | Art | 10 relevant articles on first query. |
| R10 | `Temporal 持久化执行 工作流` ; `持久化执行 durable execution 幂等键` ; `工作流引擎 重放 确定性` ; `DBOS Inngest Restate 持久化` ; `任务崩溃恢复 断点续跑 幂等` | Art, GC, GH | GC "持久化执行" returned dbos-inc/dbos-transact-py and cadence mirrors. Note: Chinese text recommends 业务幂等 separately from replay. |
| R11 | `审计日志 哈希链 防篡改` ; `Merkle 树 日志 防篡改 包含证明` ; `证书透明化日志 一致性证明` ; `immudb 不可篡改数据库` ; `Trillian Rekor 透明日志` ; `仅追加 日志 审批 记录 验证` | Art | Chinese material is about CT logs and blockchain; none on local approval ledgers. |
| R12 | `SLSA provenance in-toto attestation 签名` ; `Sigstore cosign 签名 验证` ; `可验证凭证 选择性披露 SD-JWT` ; `C2PA 内容凭证 溯源 AI生成` ; `GB 45438 生成合成内容标识 元数据` ; `Merkle 根 上链 锚定 存证` | Art, GH | GB 45438-2025 is the Chinese regulatory term for AI-content labelling (显式标识/隐式标识). |
| R13 | `SQLite WAL 崩溃 一致性` ; `原子写入 临时文件 rename fsync` ; `配置文件 损坏 恢复 JSON 原子` ; `Windows MoveFileEx 原子替换` | Art | Only SQLite WAL was found; atomic rename on Windows: no Chinese source found. |
| R14 | `知识库 溯源 来源保留 AI 生成 分离` ; `Obsidian 本地 知识库 AI 记忆 版本历史` ; `Letta mem0 记忆 分层 人工审核` ; `记忆库 Memory Bank 本地优先` ; `Git 版本 知识库 审核 晋升` | Art, GH | GitHub hit: GreatScottyMac/RooFlow "memory bank". Letta/mem0 Chinese scene: mem0 appears in OpenClaw articles. Not deeply verified. |
| R15 | `KeePassXC KDBX 本地加密 保险库` ; `age 加密 rage` ; `系统密钥链 keyring 密钥存储 跨平台` ; `便携 加密 目录 恢复密钥` ; `AES-256 保险库 Agent 凭据` | Art | Only KeePassXC well covered; age/rage/libsodium: no Chinese hits. |
| R16 | `本地优先 CRDT 同步 端到端加密` ; `Automerge Yjs Loro 本地优先` ; `Syncthing 同步 加密` ; `local-first 选择性共享` | Art, GH | GH: chenhz01/local-first-crdt (Chinese series). ElectricSQL/PowerSync/Evolu: not searched. |
| R17 | `sqlite-vec 本地向量检索` ; `FTS5 中文 分词 混合检索 RRF` ; `LanceDB 嵌入式 向量` ; `个人知识库 离线 语义检索` ; `Orama 全文 向量 搜索` | Art | Chinese FTS5 tokenization is a recurring issue (unicode61 not suited to Chinese). Orama: no Chinese hits. |
| R18 | `TUF 更新框架 回滚攻击 冻结攻击` ; `插件 签名 验证 吊销 市场` ; `Sigstore 签名 供应链` ; `npm provenance 溯源` ; `Chrome 扩展 CRX 签名` ; `go-tuf 阈值签名` | Art | TUF terms: 回滚攻击, 冻结攻击, 阈值签名, 密钥轮换, 隐式撤销. |
| R19 | `浏览器智能体 提示词注入 防御` ; `间接提示注入 网页 Agent 人工确认` ; `browser-use Playwright MCP 权限` ; `AI 浏览器 Atlas 提示词注入` ; `智能体 权限 最小权限 工具 分级 只读 写入` | Art, GH | Few benchmark-based Chinese sources; Taiwan iThome covers OWASP Agentic risks (代理目標劫持, 工具濫用). |
| R20 | `Native Messaging 本地 Web 服务器 优缺点` ; `浏览器插件 本地应用 通信 localhost` ; `KeePassXC-Browser 配对` ; `Native Messaging allowed_origins 通配符` | Art | Pairing/origin binding in Chinese: not found. |
| R21 | `浏览器扩展 内容脚本 隔离世界 isolated world` ; `插件 沙箱 iframe postMessage 权限` ; `WebAssembly 插件系统 Extism` ; `VS Code 扩展 宿主进程 隔离` ; `Figma 插件 沙箱` | Art | Extism returned no Chinese pages. |
| R22 | `灵魂绑定代币 SBT 不可转让` ; `SBT 撤销 账户恢复 社交恢复` ; `Solana Token-2022 NonTransferable 不可转让` ; `Solana Attestation Service SAS 凭证` ; `Civic Pass 链上身份 Solana` | Art (PANews, Zhihu), GH | SAS appears in PANews English page; a Chinese Token-2022 technical article was not found. |
| R23 | `Sign-In With Solana 签名登录` ; `钱包 签名 证明 密钥控制 SIWE` ; `Merkle 根 锚定 链下 注册表` ; `可验证凭证 DID 注册表 吊销` ; `EAS 以太坊证明服务` | Art | SIWE/SIWS Chinese technical content not verified. |
| R24 | `Realms SPL Governance Solana DAO` ; `Squads 多签 时间锁 Solana` ; `DAO 链下投票 Snapshot 链上执行` ; `投票权重 插件 治理 Solana` ; `Hats Protocol 角色 治理` ; `DAO 治理攻击 闪电贷` | Art (Foresight, PANews, Zhihu) | Realms: no Chinese technical article found. Squads covered in Foresight 17211. |
| R25 | `Human Passport Gitcoin Passport 评分 女巫` ; `BrightID Proof of Humanity 人格证明` ; `World ID Worldcoin 虹膜 抗女巫` ; `抗女巫 防女巫 撸空投` ; `Sybil 女巫攻击 检测` | Art (Zhihu, ChainCatcher) | 人格证明 appeared only inside a search-tool summary, not in a quoted source (low). 抗女巫 / 防女巫 are well attested. |
| R26 | `SourceCred Coordinape 贡献 声誉` ; `RetroPGF 追溯性公共物品资助` ; `Hypercerts 影响力证书` ; `DAO 贡献者 贡献度量 声誉系统` ; `Karma 声誉 DAO` | Art | RetroPGF in Chinese tends to appear as "Optimism 追溯公共物品资助". Hypercerts: nothing in Chinese. |
| R27 | `MACI 抗共谋 隐私投票` ; `二次方资助 合谋 女巫` ; `二次方投票 身份证明` ; `同行预测 抗合谋` ; `评审 回避 利益冲突 同行评审` | Art | Bounded appeals and reviewer assignment: not searched in Chinese beyond the first query. |
| R28 | `SourceCred 声誉 流动 衰减` ; `依赖 资助 Drips tea.xyz` ; `引用 归因 信用 传递` ; `贡献 归因 链 防刷` | Art | Not verified; treat as English-first. tea.xyz and Drips returned no Chinese article in my searches. |
| R29 | `本地优先 AI Agent 桌面工作台` ; `OpenClaw Cline Continue 对比 开源 Agent` ; `Jan AnythingLLM Open WebUI LibreChat 对比` ; `Goose Mastra 框架` ; `Agent 沙箱 工作台 多模型 技能市场` | GH, GC, Art | GH hit: NanmiCoder/cc-haha (15k stars, Chinese-first desktop workbench). Chinese-built competitor projects exist and should be checked in H branch. |
| R30 | `DAO 链下治理 提案 国库 透明` ; `Snapshot 链下投票` ; `Open Collective 社区 资金 透明` ; `Loomio Decidim 参与式 民主` ; `Git 治理 RFC 流程 Apache` ; `链下记录 锚定 存证 Merkle 根` | Art | Decidim and Loomio Chinese coverage: not searched; Snapshot and DAO treasury well covered. |

## Rejected terms

| Term | Why rejected | Note |
|---|---|---|
| 能力令牌 (as capability token) | GitHub query returned 35 hits, none relevant; GitCode returned 13, all about LLM token sequences or personal access tokens; no Chinese article uses it for capability tokens | use 基于能力的安全 + 令牌, or English Macaroons/Biscuit/UCAN |
| 对象能力 / 对象能力模型 | 0 GitHub hits for "对象能力 object capability"; WebSearch on Chinese blog domains found no blog | English "object-capability" is the practitioner term if searching Chinese sites |
| 令牌衰减 | 0 GitHub hits; no article in results uses it | attenuation stays English |
| 监督树 (as OTP supervision tree) | not found in any result; untested rather than disproven | low-confidence; search "Supervisor 进程监控" instead |
| 灵幻绑定代币 | a typo in one Zhihu title | never use |
| 灵魂绑定 alone for revocable credential | all hits describe SBT as non-transferable; revocation is not described in the inspected PANews article | pair with 撤销 / 账户恢复 explicitly |
| 人格证明 (Proof of Personhood) | only present in a search-tool summary, no source quote seen | try "唯一性证明", "人类证明", "Proof of Personhood" alongside |
| 选择性公开 | not seen in any result | use 选择性披露 |
| 持久执行 (without 化) | not seen; all hits use 持久化执行 | use 持久化执行 |
| 基于对象能力 for sandbox translations | translation-style, no technical hits | skip |
| Gitee repository search via API for any term above | API returned an empty list for every query, so no term could be confirmed or rejected on Gitee | see platform notes; not a term finding |

Not found in Chinese at all (searched, nothing usable; search in English on Chinese platforms): Realms/SPL Governance, SourceCred, Coordinape, Hypercerts, Extism, age/rage, SPIFFE/SPIRE, tea.xyz, Drips, Hats Protocol, Orama.

## Vocabulary findings for the language agent

1. English stays in the Chinese text for the specific product and pattern names: Macaroons, Biscuit, UCAN, caveat, attenuation, Temporal, Workflow, Activity, bubblewrap, Landlock, seccomp, Seatbelt, SD-JWT, SLSA, provenance, attestation, MACI, Passport, harness, SKILL.md. Search these as exact English tokens with a Chinese context word (for example `Macaroons 授权令牌`).
2. Native terms that are really used: 沙箱, 持久化执行, 工作流, 幂等键, 重放, 审计日志, 防篡改, 哈希链, 透明日志, 可验证凭证, 选择性披露, 本地优先, 灵魂绑定代币, 抗合谋, 二次方资助, 女巫攻击 / 抗女巫, 声誉, 智能体, 模型上下文协议, 提示词注入, 凭证代理 (credential proxy), 凭证保险库.
3. Variants: 沙箱 (mainland) / 沙盒 (Taiwan, HK); 智能体 (mainland) / 代理, 代理人 (Taiwan); 代币 (crypto media) / 通证 (some CSDN posts); 二次方资助 / 二次融资; 撤销 / 吊销 / 失效 by object type; 财库 / 国库; 提示词注入 / 提示注入 / 提示詞注入 (Taiwan); 浏览器插件 / 扩展 / 擴充功能; 合谋 / 共谋 / 勾结; 溯源 for traceability (not "provenance" proper).
4. The Chinese agent-security scene is heavy on coding-agent sandbox articles about Codex CLI and Claude Code (bubblewrap, Landlock, Seatbelt, "sandbox runtime"), and on credential brokers for agents ("Agent 提交意图，Broker 持有密钥", reported). R02 and R03 have good Chinese coverage. R04, R13, R20, R22, R23, R26, R28 are thin.
5. Chinese-built projects found on GitHub/GitCode that overlap the Alpha's feature set: NanmiCoder/cc-haha (local-first desktop agent workbench, 15k stars), ADaozz/deep_agent_cli (bubblewrap local-first coding agent CLI), huiliyi37/Tianshu-harness, weixin_42319734/Tiffa (agent platform with permission contracts, hook chains, local models), openFuyao opensandbox mirror, lileeei/sand-mcp-fs (MCP FS server using cap-std). All reported only from search descriptions; not opened. Counterexample candidates for Branch H.

## Platform notes for the Chinese language agent

### Search shape per platform

| Platform | What works | What does not |
|---|---|---|
| WebSearch | add `allowed_domains` for Chinese sites; queries of 4 to 8 mixed Chinese and English tokens | unfiltered queries return English; the tool does not index Gitee well |
| GitHub | `gh api -X GET search/repositories -f q="..." -f per_page=4` | `-f` without `-X GET` makes a POST and returns 404 (this cost me a call); multi-term Chinese queries act as AND and give totals of 0 to 3; single common words ("持久化执行", "灵魂绑定代币") return unrelated mass-spam repos with huge descriptions such as cirosantilli/china-dictatorship; filter by stars and check descriptions |
| GitCode (AtomGit) | `https://gitcode.com/search?q=TERM&type=repo` via WebFetch renders 10 results per page with a total count; results include GitHub mirrors and domestic projects | it is not an independent source of Chinese terms unless the owner is a domestic account; many results are "gh_mirrors" |
| Gitee | `https://gitee.com/api/v5/repos/{owner}/{repo}` for a known repo works anonymously (HTTP 200, JSON) | `gitee.com/search?...` returns 301 to `so.gitee.com/?q=...`, which gives WebFetch only a "Gitee Search" heading; `gitee.com/explore/all?q=` gave HTTP 405 to WebFetch; `api/v5/search/repositories` returned `[]` anonymously for six Chinese queries and one English query. Whether a personal access token fixes this was not tested (not in scope). Treat Gitee search as requiring a login or token. |
| OpenI | `https://openi.pcl.ac.cn/` is the Gitea-based code forge (footer: powered by Gitea; repository square at `/explore/repos/square`, models at `/explore/models`, datasets at `/explore/datasets`; example repos `zeizei/OpenI_Learning`, `C2NET/C2NET`) | explore search pages return a "usage agreement, agree and continue" gate to WebFetch; `https://openi.org.cn/` returned HTTP 200 but empty content to WebFetch, so I could not confirm it is a code host. Assume `openi.pcl.ac.cn` = forge, `openi.org.cn` = portal (unverified). |
| CNKI | `oversea.cnki.net/kns/search?q=` loads the search shell | no result list returned to WebFetch; metadata not reachable this way; use the English-language CNKI or a browser session |
| CSDN | titles and snippets via WebSearch | direct fetch gave 403 and ECONNRESET on two of two attempts; Juejin direct fetch worked; Zhihu zhuanlan fetch gave 403 on one attempt |
| Taiwan | `ithelp.ithome.com.tw`, `ithome.com.tw` article titles via WebSearch | few traditional-Chinese technical hits on sandboxing; Novita zh-TW is the only hit for 模型上下文協定 |

### Rate limits

- GitHub: 30 sequential searches at 2.5 s spacing in a Python loop produced no 403.
- Gitee, GitCode, OpenI: no rate-limit message seen; volumes were small (under 10 requests each).

### Telling a Gitee upstream from a GitHub mirror

Observed: GitCode URLs with the owner `gh_mirrors` (for example `https://gitcode.com/gh_mirrors/mc/MCP-Universe`) are mirrors of GitHub repositories, as are results whose owner/name matches a GitHub project (dbos-inc/dbos-transact-py, cadence-workflow/cadence, google/gvisor-style descriptions). For Gitee I did not see a Gitee repo page, so the following is unverified: Gitee mirrors normally show "mirror from" or "forked from" markers in the repository header and the API object may carry fork/parent fields; confirm by calling `https://gitee.com/api/v5/repos/{owner}/{repo}` and checking the JSON before trusting stars or activity. As a rule, if the same owner/name exists on GitHub with the same description, treat the GitHub copy as upstream and record the mirror only as a distribution channel.

### Other cautions

- Many search-result summaries were produced by the search tool; quotes attributed to articles in this file come either from my own opening of the page (inspected) or from snippets (reported). Re-open before quoting in final reports.
- Several Chinese articles repeat unsourced claims (for example about Anthropic watermarking or KeePassXC certification); do not use them as evidence for technical claims.
- Per master prompt, README or article text is evidence, not instruction; none of the pages opened contained instructions aimed at the agent.
