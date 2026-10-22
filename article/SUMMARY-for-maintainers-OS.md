# ResonantOS: what we found and what we suggest

A plain-language summary of an independent research review, 21 October 2026.
From: Bartolomeo. A companion summary covers ResonantDAO. The full report and its evidence, covering both projects, are attached as `ARTICLE.md` and `APPENDIX.md`.

## Why you are receiving this

Over the past two days we studied ResonantOS and ResonantDAO in depth. This summary covers ResonantOS; a separate summary covers ResonantDAO. We wanted to know what already works, what is missing, and which existing open-source projects could save you work. The project is yours, and you know it far better than we do. Please read what follows as findings to check, not as verdicts. Where we are wrong, we would like to know.

## What we looked at, and how

- **ResonantOS:** the `2.0.0-alpha` repository at commit `578fbbc` (18 October 2026), its documents, and its test results on GitHub.
- **The wider world:** across both projects, we searched about 36 code platforms and research indexes in seven languages. That gave 586 relevant projects. We read 16 of them closely at a fixed version.

We only read code. We did not install or run any of it. Every claim in the full report points to the file and line it comes from, and independent reviewers re-checked those pointers.

## What is working well

The Alpha is a real, working product: a Chrome extension plus a small local service (the "bridge"). It has 114 actions, each protected by its own permission. Anything without a declared permission is refused by default. Its 2,424 automated tests all passed on the commit we studied, and a nightly test drives a real Chrome. Chat, page context, workspaces, browser control and memory intake all work and are tested. The token design is careful. This is a solid base to build on, not something to replace.

## Where the code and the documents disagree

Some features are described as finished but do not yet work as described. None of this is hidden; mostly the status pages have fallen behind the code.

1. **Promoting knowledge into the trusted wiki cannot run.** Since commit `4098e28` (2 June 2026), the promote step always fails because two pieces of code pass their information in different shapes. The capability list still says "Implemented". *Please fix this together with a real approval check (see the next section).* Once promotion works again, the only thing stopping an AI helper from promoting its own output would be a field it fills in itself.
2. **Per-site browser permissions are not enforced everywhere.** They are checked only in the side panel. "Ask before acting" and "trusted" behave the same, and "blocked" does not stop navigation.
3. **"Signed" add-ons carry no signature.** Eight add-on files say they are signed, but there are no signature bytes and no code checks them.
4. **The human-only rules are text matching.** Rules such as "only a human may publish or pay" work by looking for English words on the page. A plain link with the right wording can slip through.
5. **Isolation of AI helpers exists on macOS only.** On Linux and Windows, helper programs such as Hermes and OpenCode run with your full user rights. Your provider API keys are also handed to them in their environment.
6. **Seven local web addresses on the bridge need no password.** Any program on the same computer can reach them.
7. **The status page is about 190 commits behind.** It does not mention the vendored Augmentor app or the newer add-on harness. The Anthropic and Google provider presets also have no code behind them yet.

## The three design changes we recommend most

Across the sixteen projects we studied, the same three mistakes kept returning. We suggest settling them once, for everything:

1. **One protected place for security records.** Revocation lists, approval records, signing keys and "known-good version" markers should live in one folder outside the user's own documents. No AI helper and no bridge action may write there. Each record carries a check that reveals tampering or a restored old copy. Today those records would sit where the helpers they guard against can edit them.
2. **An approval window the AI cannot press.** Important actions, such as promoting knowledge or starting an AI helper with permission to run commands, should wait for a decision from a small separate program. That program shows the person exactly what will happen and records the answer before anything runs. There should be no "approve" address on the bridge at all, so no token can approve anything.
3. **A key-holding middleman.** AI helpers should never receive your provider API keys. A small separate program holds them, adds them to outgoing requests, and removes them from anything coming back. That last part matters because some providers echo a request back, key included.

**An honest limit.** On one user account these protections are strong against other accounts and against helpers that are properly isolated. They are not strong against a program that runs as you with no isolation. On Windows today, that describes every AI helper: it could click its own approval window and read the keys. That gap closes only when the core runs under its own account, a step we place six to twelve months out. Until then, we suggest the app say plainly on Windows: "unconfined: this helper can approve its own actions".

## The path we suggest for ResonantOS

- **Now (about four weeks):** correct the status pages; add the protected folder; add the key middleman and Linux and macOS isolation behind a switch; add the approval window for promotion and for starting helpers, with the promotion fix in the same change; require a password on the open web addresses.
- **Next (two to three months):** per-helper permissions that expire and can be withdrawn mid-session; a signature check for add-ons; jobs that survive a crash without repeating an action that may already have happened.
- **Later (six to twelve months):** move the security core into its own small program, piece by piece, so the "neutral baseplate" on your website exists in code. Add a supervisor that can restore a known-good version, and Windows and macOS test runs in CI.

We do not suggest a rewrite. Each step is a normal-sized pull request, and the existing tests keep passing.

## A late addition: choosing local or cloud by what is actually being sent

On 21 October 2026, after the review above was otherwise finished, Perplexity open-sourced part of their own privacy system: a small local model, PII-Tracer, that reads a piece of text and flags whether it looks sensitive. We looked at it and think it is worth one addition to the roadmap, though it does not change anything else in this review.

Today, ResonantOS decides whether to use a local model or send something to the cloud based only on things like "this provider prefers local" or "this one is faster." It never looks at what is actually being said. So a page full of someone's private medical notes and a page of public news get routed the same way.

PII-Tracer could add one more input to that decision: a quick local check of "does this look sensitive?" before the content goes anywhere. We suggest wiring it into the same approval window described above (the one the AI cannot press), so a person, not the AI, sees the flag and decides. It should not go in first; it depends on that approval window existing and on local models being wired up properly, so it belongs about two to three months in, not in the first month's work. We have added it to the full report as a new item (T25 in the threat list) and written a short technical note on the model itself (`dossiers/perplexity-pii-tracer.md`).

**An honest caveat:** a sibling release of the same model states plainly that its own sensitivity score is weak and needs calibration before anyone relies on it. Treat this as a useful extra signal to show a person, not as something that silently decides anything by itself.

## What you can borrow

| Need | Project | How |
|---|---|---|
| Isolating AI helpers on Linux and macOS | `@anthropic-ai/sandbox-runtime` | for isolation only; never its key-masking mode |
| Signed, revocable add-ons | `tuf-js` 6.0.0 | behind a small wrapper |
| Permissions that expire and can be narrowed | Biscuit (Eclipse) | withdrawal is ours to build |
| Jobs that survive a crash | OpenWorkflow 0.11.0 | plus a small record that prevents double actions |
| Shareable evidence with selective disclosure | `@sd-jwt` 0.23.0 | behind a strict wrapper |
| One more AI helper and tool host | Goose | as one helper, not as the product's base |
| Choosing local or cloud by content | PII-Tracer (Perplexity, open-sourced 21 October 2026) | as a detector only, added after this review was finished; see "A late addition" below |

We also suggest copying a few good ideas rather than adopting the projects that hold them: Aegis's key middleman, and nanobrowser's action checks.

*Disclosure:* this research was carried out with Anthropic's Claude models. Anthropic also makes `sandbox-runtime`. We found a real flaw in its key-masking mode, and we recommend the library for isolation only.

## Good first tasks for contributors

Each of these takes under two days and needs no design decision:

- correct the status pages;
- block the protected folder from AI helpers;
- require a password and a same-site check on the open bridge addresses;
- hide provider presets that have no code behind them;
- write the memory settings file safely, so a crash cannot corrupt it.

## What we could not do

- **We ran nothing.** Every "this works" is based on reading tests that already run in your CI.
- **Windows isolation without administrator rights is unproven.** We wrote down the test that would settle it.

## Two specific notes for the maintainers

These items came up during the research. We share them openly, in keeping with the community's way of working. Each says what we saw, why it may matter, and what we suggest. (ResonantDAO has two more, in its own summary.)

**1. Knowledge promotion has not worked since June.**
- **What we saw:** since commit `4098e28` (2 June 2026), the step that promotes reviewed notes into the trusted wiki always fails. Two pieces of code pass their information in different shapes, and the approval check reads a field name the caller does not send. No test calls this step end to end. The capability list still says "Implemented".
- **Why it may matter:** users and contributors are told a core feature works when it does not. Once it is fixed, the only gate left would be a field that the caller fills in itself, so an AI helper could promote its own output.
- **What we suggest:** fix it in the same change that adds a real approval check, and add a test that calls the promote step from start to finish.

**2. Two different licences on the Augmentor app.**
- **What we saw:** the Alpha includes a copy of the Augmentor app (version 0.1.33) labelled MIT. On 23 September 2026 the original Augmentor repository changed its licence to "MIT with Augmentor Resale Restriction". The copy inside the Alpha and the original now carry different terms.
- **Why it may matter:** it is unclear which terms apply to the copy inside the Alpha, and so what people who reuse the Alpha may do with it. That is a legal question, and we are not lawyers.
- **What we suggest:** decide between you which terms apply to the copy, take legal advice if needed, and state the answer in the Alpha's licence notes.

## Where the details are

- `ARTICLE.md`: the full report, covering both projects. Section 11 holds 25 ready-to-file issues; section 12 holds eight experiments; section 13 holds twelve decisions for you.
- `APPENDIX.md`: the evidence, the search record, and our own error rates.
- The companion summary covers ResonantDAO, including its own two notes and three related findings.

We are happy to answer questions, and we will correct anything you show us is wrong.
