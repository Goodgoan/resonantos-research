Parallel subagents share one session scratchpad; each must work in its own subfolder named after its agent id, and the lead keeps its own helpers out of the root too.

Why: during Wave 2 on 2026-10-20 one branch agent overwrote another's meta.py at the scratchpad root and a third deleted four helper scripts there while cleaning up. The lead's validate_ledger.py survived by luck.

How to apply: every brief tells the agent to create <scratchpad>\<agent-id>\ and write only there; the lead's own scripts go in <scratchpad>\lead\. Ledger and glossary outputs are unaffected because each agent owns distinct files under research\.
