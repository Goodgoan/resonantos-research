Write large Markdown files with the Write tool, not a Bash heredoc; a 150-line heredoc with mixed quotes and backticks failed with "unexpected EOF while looking for matching quote" on 2026-10-20.

Why: the Bash tool wrapper on this Windows Git Bash setup appears to pre-parse the command text, and long heredocs with backticks and apostrophes break it.
How to apply: use Write/Edit for files over ~40 lines or containing backticks; keep heredocs for short config snippets.
