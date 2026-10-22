# ResonantDAO: what we found and what we suggest

A plain-language summary of an independent research review, 21 October 2026.
From: Bartolomeo. A companion summary covers ResonantOS. The full report and its evidence, covering both projects, are attached as `ARTICLE.md` and `APPENDIX.md`.

## Why you are receiving this

Over the past two days we studied ResonantOS and ResonantDAO in depth. This summary covers ResonantDAO; a separate summary covers ResonantOS. We wanted to know what already works, what is missing, and which existing open-source projects could save you work. The project is yours, and you know it far better than we do. Please read what follows as findings to check, not as verdicts. Where we are wrong, we would like to know.

## What we looked at, and how

- **ResonantDAO:** the whitepaper (v0.6), the Contribution Economy specification and the website. We also read the public test-network records.
- **The wider world:** across both projects, we searched about 36 code platforms and research indexes in seven languages. That gave 586 relevant projects. We read 16 of them closely at a fixed version.

We only read code and public documents. We did not install or run anything. Every claim in the full report points to the file and line, or the page, it comes from, and independent reviewers re-checked those pointers.

## What we found

The DAO is a specification today, with no live code. We suggest starting **off-chain**:

- a public, append-only record of contributions, countersigned by three outside witnesses;
- signed membership records that carry reasons and an appeal route;
- advisory votes that anyone can recount.

None of this needs a token, a smart contract, an audit or a custody arrangement. We suggest no token and no binding on-chain vote until an audit, a custody policy and a test-network trial of the exact program exist. Whatever members accrue in this first phase should be described as a record of reviewed contribution, with no promise of later conversion.

Three related findings:

- **The shared Solana governance service should not be used.** It runs a version whose source we could not find, under a 5-of-7 council, with no waiting period and no community veto.
- **The test-network tokens describe an older model.** They also have single-key control. We suggest switching those keys off or labelling the tokens as old test material.
- **Some linked documents are missing.** Three architecture documents and the Symbiotic Licence page that the whitepaper links to are not reachable. Republishing them would let readers check the governance claims.

## What you can borrow

| Need | Project | How |
|---|---|---|
| The DAO's public record | Tessera with witnesses | on one Linux server |

*Disclosure:* this research was carried out with Anthropic's Claude models.

## What we could not do

- **We ran nothing.** Every finding here comes from reading public documents and code, not from running anything.
- **We did not study proof-of-personhood or collusion resistance in depth.**
- **No tool anywhere measures how much of a piece of work was done by a human and how much by AI.** The DAO's rules depend on that number. Until a measurement exists, we suggest treating it as a claim that a reviewer countersigns.

## Two specific notes for the maintainers

These items came up during the research. We share them openly, in keeping with the community's way of working. Each says what we saw, why it may matter, and what we suggest. (ResonantOS has two more, in its own summary.)

**1. A file that may contain members' personal details.**
- **What we saw:** the public `resonant-hub` repository includes a database file, `community.db`, whose table names suggest it holds community member records. We did not open the records, so we do not know whether they are real people or demo data.
- **Why it may matter:** if the file holds real people's details, those details are public, and they stay in the repository history even after the file is deleted.
- **What we suggest:** check the file. If it holds real details, remove it from the repository history (not only from the latest version), and replace it with clearly made-up sample data.

**2. Missing documents on the DAO website.**
- **What we saw:** the whitepaper links to three architecture documents and to the Symbiotic Licence page. None of them loads.
- **Why it may matter:** readers cannot check the governance and licence claims the whitepaper makes, and we had to judge the DAO from the whitepaper alone.
- **What we suggest:** republish the documents, or mark them as withdrawn.

## Where the details are

- `ARTICLE.md`: the full report, covering both projects. Section 13 holds twelve decisions for you, including the DAO ones.
- `APPENDIX.md`: the evidence, the search record, and our own error rates.
- The companion summary covers ResonantOS, including its own two notes and the three design changes it recommends.

We are happy to answer questions, and we will correct anything you show us is wrong.
