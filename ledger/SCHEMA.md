# Stage 2 ledger schema (lead, 2026-10-20)

Binding for every Stage 2 agent. One JSON object per line, UTF-8, no trailing commas, no comments. Field order as listed. Every field present in every row; use `null` for unknown, never omit the key and never write an empty string to mean unknown. Dates are `YYYY-MM-DD`. Write files with the Write tool (append by rewriting the whole file or by `Edit` at the end); never with Bash heredocs.

## discovery-<agent-id>.jsonl (one row per source record)

A source record is one place where one codebase appears (a GitHub repo, its npm package, its paper, its Gitee mirror are four rows). Deduplication into codebases happens later in `codebases.jsonl`; agents do not deduplicate across agents, but they do set `duplicates_or_mirrors` when they know of another record.

| Field | Type | Allowed values / format |
|---|---|---|
| requirement_id | string | `R01`..`R30`, or `R00` for a counterexample or cross-cutting record that no single requirement owns |
| capability | string | short English phrase naming what the record offers for that requirement |
| platform | string | one of: `github`, `gitlab`, `codeberg`, `sourceforge`, `huggingface`, `arxiv`, `acl`, `hf-papers` (Papers with Code substitute), `pypi`, `npm`, `crates`, `go`, `maven`, `nuget`, `swh`, `zenodo`, `gitee`, `gitcode`, `openi`, `cnki`, `framagit`, `codegouvfr`, `hal`, `opencode-de`, `helmholtz`, `rsd-nl`, `4tu`, `dev-overheid`, `qiita`, `zenn`, `jstage`, `kci`, `openalex`, `semanticscholar`, `web` (any other page; name the host in notes), `university-gitlab` (name the host in notes) |
| search_language | string | ISO 639-1: `en`, `zh`, `fr`, `de`, `nl`, `ja`, `ko`, other |
| search_terms_or_query | string | the exact query string or API call that produced the hit |
| search_date | string | date |
| result_url | string | the URL that was hit |
| artifact_type | string | `repo`, `package`, `model`, `space`, `paper`, `archive`, `dataset`, `doc` (design document, spec, audit report, blog post) |
| canonical_source_url | string or null | the authoritative source repository for the codebase, after following links; null if not yet established |
| project_doc_language | string or null | primary language of README and code comments (ISO 639-1); `multi` if bilingual |
| upstream_status | string | capability status of the thing the record claims, using the master prompt classes: `A` implemented and exercised, `B` implemented but insufficiently proven, `C` partial or experimental, `D` design or specification only, `E` planned, `F` unknown or inaccessible, `G` superseded or abandoned |
| package_or_release_version | string or null | latest release or package version seen, with its date in notes |
| commit_sha_or_swhid | string or null | default-branch HEAD SHA at inspection, or SWHID |
| doi_or_paper_id | string or null | DOI, arXiv id, ACL id |
| license_code | string or null | SPDX identifier for the code; `NOASSERTION` if no licence file; `OTHER:<name>` for non-SPDX text |
| license_data | string or null | licence of data, weights or content if separate; else null |
| license_model | string or null | licence of model weights if the record is a model; else null |
| tests_or_benchmarks | string or null | one line: what test suites, CI lanes, audits or benchmarks exist and whether you inspected them |
| maintenance | string or null | one line: last commit date, release cadence, open issues trend, bus factor signals, maintainer organisation |
| duplicates_or_mirrors | string or null | other URLs you know refer to the same codebase, comma-separated |
| evidence_level | string | `inspected` (you opened code, manifest, tests or the page itself), `reported` (search snippet, README claim, third-party description), `hypothesis` |
| disposition | string | `candidate` (worth evaluating for the requirement), `lead` (points to something else; follow-up needed), `counterexample` (evidence against a candidate; say which in notes), `excluded` (reason in notes), `duplicate` (of a record you already wrote; name it) |
| found_by_agent | string | your agent id, e.g. `s2-br-b`, `s2-lang-zh`, `s2-probe-jako` |
| notes | string | free text; original-language quotes go here with English translation and `[MT]` if machine translated; name the host for `web`; say "official-adjacent" for ManoloRemiddi/* records (state.md D1.2) |

### Conventions

- `disposition: candidate` requires `evidence_level: inspected` for at least the manifest or README of the canonical source, and a non-null `license_code`.
- Write the Solana/EVM question into `notes` for every Branch F and G chain record: `chain: solana`, `chain: evm`, `chain: agnostic`, `chain: none`.
- A paper row and its code row are two rows; cross-reference them in `duplicates_or_mirrors`.
- Counterexamples (Branch H and anyone who finds one): `requirement_id` of the gap the candidate was proposed for, `disposition: counterexample`, and `notes` containing `against: <canonical_source_url of the candidate>`. Amended 2026-10-20: the marker may be preceded by `pass2` or `pass2;`, so the merge matches `against:` anywhere in notes, not only at the start.
- No stars, download counts or popularity statements in `maintenance` unless paired with a fitness observation.

## negative-<agent-id>.jsonl (one row per search that produced nothing usable, or that was blocked)

| Field | Type | Allowed values / format |
|---|---|---|
| requirement_id | string | `R01`..`R30` or `R00` |
| platform | string | same list as above |
| search_language | string | ISO 639-1 |
| query | string | exact query |
| search_date | string | date |
| outcome | string | `empty` (no results), `irrelevant` (results, none relevant), `blocked` (403, login wall, captcha, rate limit), `paywalled`, `defunct` (platform or endpoint gone) |
| inspected | string | what you looked at before deciding (e.g. "first 30 results, opened 4") |
| reason | string | why excluded or what blocked you |
| found_by_agent | string | your agent id |

## Minimal example rows

```
{"requirement_id":"R01","capability":"attenuable bearer tokens with caveats","platform":"github","search_language":"en","search_terms_or_query":"gh api search/repositories -f q=\"macaroons caveats attenuation language:TypeScript\"","search_date":"2026-10-20","result_url":"https://github.com/EXAMPLE/EXAMPLE","artifact_type":"repo","canonical_source_url":"https://github.com/EXAMPLE/EXAMPLE","project_doc_language":"en","upstream_status":"B","package_or_release_version":"1.2.0","commit_sha_or_swhid":"0123456789abcdef0123456789abcdef01234567","doi_or_paper_id":null,"license_code":"MIT","license_data":null,"license_model":null,"tests_or_benchmarks":"vitest suite covers caveat verification; no revocation test seen (inspected test/ directory)","maintenance":"last commit 2026-09-30; 3 releases in 2026; single maintainer","duplicates_or_mirrors":"https://www.npmjs.com/package/EXAMPLE","evidence_level":"inspected","disposition":"candidate","found_by_agent":"s2-br-b","notes":"placeholder row; replace"}
{"requirement_id":"R22","platform":"gitee","search_language":"zh","query":"不可转让 凭证 Solana","search_date":"2026-10-20","outcome":"irrelevant","inspected":"first 20 results, opened 2","reason":"results are generic Solana SDK forks with no credential logic","found_by_agent":"s2-lang-zh"}
```

## File ownership

Each agent writes exactly `discovery-<id>.jsonl` and `negative-<id>.jsonl` (plus `glossary/ja-ko-probe.md` for the probe). The provenance agent alone writes `codebases.jsonl` and `coverage-matrix.md`. The lead alone writes `gate2-report.md`, `threat-model-draft.md` and this file.
