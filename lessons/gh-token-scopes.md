The gh token here lacks read:packages and read:project, so GitHub Packages and Projects v2 (Project 2, the release authority) cannot be inspected; GitHub code search is rate-limited after a handful of queries.

Why: census agent hit both on 2026-10-20. Project 2 is declared the release planning authority by docs/ROADMAP.md, so its state stays "reported by authors".
How to apply: do not promise Project 2 or GHCR evidence; use local grep over clones instead of code search where possible; batch code-search queries and wait on 403.
