Use `gh api` (authenticated) for all GitHub lookups; raw curl to api.github.com is capped at 60 requests per hour and has no GraphQL.

Why: Stage 0 check on 2026-10-20 showed core 60/h, code_search 60/h and graphql 0 for unauthenticated calls. Census and discovery agents make hundreds of calls.
How to apply: `gh api repos/OWNER/REPO`, `gh api -X GET search/repositories -f q=...`, `gh api -X GET search/code -f q=...`, `gh api graphql -f query=...`. Paginate with `--paginate`. The `-X GET` matters: `-f` alone switches gh to POST and the search endpoints answer 404 (found by s2-br-h, 2026-10-20). The search endpoints share a 30-requests-per-minute limit across every agent using this token; back off 60 s on 403.
