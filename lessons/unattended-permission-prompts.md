# Lesson: unattended agents stall on permission prompts (2026-10-20)

What happened: after a usage-limit pause, ten agents were resumed at 17:54 while the user stepped away. Within two minutes each one issued a tool call that needed approval (compound `cd ... && grep ...` chains, reads in `_untrusted\`, a ledger validation heredoc) and waited. Nothing progressed for four and a half hours; the prompts were then declined as the user left. No dossier was written, and two inspectors lost their findings except for what they put in their stop reports.

Rules that follow:
- Write the output file early (all section headings, "STATUS: PARTIAL") and fill it as you go, so any stop leaves a partial file rather than nothing.
- Prefer single, simple read-only commands (`git -C`, `grep`, `ls`, `head`, `gh api` GET, `python -I` scripts in your own scratchpad) over long `cd ... && ... |` chains; unusual commands are the ones that prompt.
- A declined tool call while the user is leaving is not a judgement on the work; the lead records it as an event, not as a decision.
- The lead checks for stalls by looking for gaps in the subagent transcripts, not by trusting the roster status.
