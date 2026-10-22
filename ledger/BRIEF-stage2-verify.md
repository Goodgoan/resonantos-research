# Stage 2 verifier brief (lead, 2026-10-20) for agent s2-verify

Purpose (master prompt 6.5): a fresh-context check that the Stage 2 ledgers say true things. You did not write any of them. About 10 percent of discovery rows are sampled and each is checked for four facts: the URL resolves, the canonical source is right, the licence is right, and the row is not an unmarked duplicate. Failures are logged in `state.md` by the lead and the failure rate goes into the article appendix. Your verdicts must be reproducible, so record the exact command or URL behind each one.

Read first: `ledger/SCHEMA.md` (what rows mean), `ledger/BRIEF-stage2-common.md` sections 3, 4, 7 and 8 (standards, platform access, boundaries, output discipline including the per-agent scratchpad subfolder `<scratchpad>\s2-verify\`), `lessons\*.md` (gh api needs `-X GET`; regional platform access).

## Sample

1. Concatenate every `ledger/discovery-*.jsonl` (branches a-h, lang zh/fr/de/nl, probe) in alphabetical file order, number the rows from 1, and draw the sample with `python -I -c "import random; random.seed(20261020); ..."` taking `round(0.10 * N)` rows without replacement. Record N, the seed and the selected row numbers in your report so the lead can regenerate the sample.
2. Stratify nothing; the seed decides. If the sample happens to miss an agent entirely, add that agent's row with the lowest number as an extra, marked "added for coverage", outside the rate calculation.
3. Also check every row in `ledger/codebases.jsonl` whose `disposition_summary` is `candidate` and that appears in the lead's proposed shortlist (the lead will give you the list of codebase_ids in the launch message); those are checked in full, outside the 10 percent rate, because they go to Stage 3.

## Checks per sampled row

| Check | Method | PASS | PARTIAL | FAIL |
|---|---|---|---|---|
| URL resolves | `curl -sIL -A "resonantos-research" <result_url>` or `gh api repos/OWNER/REPO` for GitHub; WebFetch where curl is bot-walled | 200 (or 301 to the same project) | resolves only through a different host or after a rename; note the new URL | 404, 410, parked, or a different project |
| Canonical source right | follow repository links from package metadata (`registry.npmjs.org/NAME`, `pypi.org/pypi/NAME/json`, `crates.io/api/v1/crates/NAME`), the paper's code link, the mirror's README; compare with `canonical_source_url` | same repository | same project, but a fork/mirror/moved org was recorded as canonical, or canonical is null while discoverable | different project, or canonical points to a mirror while an upstream with newer commits exists |
| Licence right | read the LICENSE file at the canonical source (`gh api repos/OWNER/REPO/license` gives SPDX; open the file for non-SPDX text); compare with `license_code`; also check whether `notes` flags dual licences, "plus restriction" clauses and NOASSERTION correctly | matches | SPDX matches but a restriction, dual licence or licence-file-versus-metadata conflict is unflagged | wrong SPDX, or a licence recorded where no LICENSE file exists |
| Not an unmarked duplicate | search all discovery ledgers for the same canonical_source_url or the same repository under another host; check `duplicates_or_mirrors` and `disposition` | unique, or duplicate correctly marked | another row for the same codebase exists in another agent's ledger and neither cross-references it (expected between agents; count as PARTIAL) | the same agent recorded the same codebase twice for the same requirement without `disposition: duplicate` |

Additionally, for rows with `disposition: candidate`, confirm `evidence_level: inspected` is plausible: the row's `tests_or_benchmarks` or `maintenance` field should name something only visible from the repository itself (a test directory, a CI file, a commit date). If both fields are generic, record PARTIAL with reason "inspected claim not evidenced".

Rate: PASS 1, PARTIAL 0.5, FAIL 0, per check; report the failure rate per check and overall as (1 - mean score). Report which agents' rows carry the failures.

## Output

`ledger/verification-stage2.md`, the only file you may write, with: method and sample reproduction line; a table of sampled rows (row number, agent, requirement, result_url, four verdicts, one-line reason, command used); the shortlist full-check table; failure rates per check, per agent and overall; a list of concrete corrections the lead should send back to agents (agent id, row identifier, field, current value, correct value with evidence). Do not edit any ledger yourself.

Boundaries: master prompt section 9. No cloning, no execution, no issues or comments anywhere. Public APIs and pages only; back off on 403/429.

Time box: 80-150 tool calls. Return message (at most 250 words): N, sample size, failure rates, count of corrections, the three worst findings, file path.
