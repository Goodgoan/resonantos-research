# Platform URL check (lead, 2026-10-20, curl -L, 20s timeout)

All section 4 platform URLs were probed. Results:

| Platform | URL probed | HTTP | Effective URL / note |
|---|---|---|---|
| GitHub | https://github.com/ | 200 | ok |
| GitLab | https://gitlab.com/ | 200 | redirects to about.gitlab.com (marketing); gitlab.com/explore works for search |
| Codeberg | https://codeberg.org/ | 200 | ok |
| SourceForge | https://sourceforge.net/ | 200 | ok |
| Hugging Face | https://huggingface.co/ | 200 | ok |
| arXiv | https://arxiv.org/ | 200 | ok |
| ACL Anthology | https://aclanthology.org/ | 200 | ok |
| Papers with Code | https://paperswithcode.com/ | 200 | redirects to https://huggingface.co/papers/trending (confirms sunset; record substitution in coverage matrix) |
| PyPI | https://pypi.org/ | 200 | ok |
| npm | https://www.npmjs.com/ | 200 | ok |
| crates.io | https://crates.io/ | 404 (root, curl) | SPA root blocks plain curl; API https://crates.io/api/v1/crates?q=... returns 200 with a descriptive User-Agent (crates.io policy requires one) |
| Go modules | https://pkg.go.dev/ | 200 | ok |
| Maven Central | https://central.sonatype.com/ | 200 | ok |
| NuGet | https://www.nuget.org/ | 200 | ok |
| Software Heritage | https://archive.softwareheritage.org/ | 200 | ok |
| Zenodo | https://zenodo.org/ | 200 | ok |
| Gitee | https://gitee.com/ | 200 | ok |
| GitCode | https://gitcode.com/ | 200 | ok |
| OpenI | https://openi.pcl.ac.cn/ and https://openi.org.cn/ | 200 / 200 | both resolve; establish which is the forge in Stage 2 |
| CNKI | https://www.cnki.net/ | 200 | redirected to oversea.cnki.net (metadata only, paywalled) |
| Framagit | https://framagit.org/ | 200 | redirects to /public/projects |
| code.gouv.fr | https://code.gouv.fr/ | 200 | /fr/ |
| HAL | https://hal.science/ | 200 | ok |
| openCode.de | https://opencode.de/ | 200 | /de |
| Helmholtz RSD | https://helmholtz.software/ | 200 | ok |
| Research Software Directory (NL) | https://research-software-directory.org/ | 200 | ok |
| 4TU.ResearchData | https://data.4tu.nl/ | 200 | ok |
| developer.overheid.nl | https://developer.overheid.nl/ | 200 | ok (verified as requested) |
| Qiita | https://qiita.com/ | 200 | ok |
| Zenn | https://zenn.dev/ | 200 | ok |
| J-STAGE | https://www.jstage.jst.go.jp/ | 200 | ok |
| KCI | https://www.kci.go.kr/ | 200 | ok |
| OpenAlex API | https://api.openalex.org/works?search=test | 200 | ok |
| Semantic Scholar API | https://api.semanticscholar.org/graph/v1/paper/search?query=test | 200 | ok (rate-limited without key) |
