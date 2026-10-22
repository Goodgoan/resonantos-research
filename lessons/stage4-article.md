# Lessons from the Stage 4 article (2026-10-21, Fable 5.1 lead)

- Copy threat, requirement and invariant ids from the source file at writing time; do not recall them. 24 of the 26 citation FAILs in the first draft were threat ids written from memory that did not match `ledger/threat-model-draft.md` section 4.
- Write the master prompt's per-section field lists (8.5 items 11, 12, 13, the Next 10 columns, 8.6) into the part skeleton before drafting prose; three of the seven adversarial blockers were missing fields, not missing research.
- A Bash heredoc longer than a few kilobytes is cut off by the shell on this machine ("unexpected EOF"); put edit scripts in the scratchpad with the Write tool and run them with `python -I <path>`.
- Keep the article in part files and concatenate; it lets reviewers read a frozen `ARTICLE.md` while fixes land in the parts.
- Launch the citation checkers and the adversarial reviewer together on the frozen draft; their findings overlap little (the reviewer found logic and scope faults, the checkers found pointers and ids) and the wall-clock saving is about an hour.
- An adversarial reviewer with a fresh context and the research base catches claims copied from the lead's own earlier files, which the lead cannot see as wrong (the store "detects" same-user tamper came from `decisions.md:40`, which contradicted `decisions.md:45`).
