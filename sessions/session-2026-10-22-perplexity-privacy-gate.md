# Session Log — 2026-10-22

## Tool

Claude Code (VS Code extension), session model Claude Opus 5.5 (`claude-opus-5-5`); this save ran under the `save-session` skill on Claude Sonnet 5.5.
Working directory: `C:\My_Agents\75_ResonantDAO and OS`

## Full Conversation Transcript

### Turn 1

**User:** "Perplexity just released a privacy harness with which is open source. Look at that open source and determine whether it's relevant for this current research. Give me your advice after analysis."

**Assistant (work done):**
- Listed the project folder. Found the finished ResonantOS/ResonantDAO deep-research run (`research/state.md`: Final DONE 2026-10-21, article and appendix pending the user's read, nothing published) and a new file `Harness-Demo-Runbook-2026-09-23.pdf` (ResonantOS harness swap demo for Andrew, DSH add-on). Read the PDF; it is unrelated to Perplexity.
- Read `research/article/SUMMARY-for-maintainers.md` and `research/architecture/decisions.md` (X-1 security-state store, X-4 approval helper, X-5 key-holding broker).
- Web search found nothing named "privacy harness". Candidates: Numbat (agent endpoint monitoring), Privacy Gate (on-device PII check in Hybrid Compute), SPACE (Firecracker microVM sandbox).
- `gh repo list perplexityai`: SPACE (Rust, Apache-2.0), numbat (Go, Apache-2.0), browsesafe-plus-plus (MIT). Downloaded READMEs to the scratchpad.

### Turn 2 (mid-turn message)

**User:** "So the privacy harness decides whether information is private and should stay locally, on local LLMs, or should go to the cloud. This would seem to be relevant for the current resonant OS. But give me your verdict."

**Assistant (work done):**
- Identified the target as Perplexity Hybrid Compute's Privacy Gate (launched 2026-09-01). The open-source part is the detector model `perplexity-ai/PII-Tracer` on Hugging Face (MIT, revision `d25c16f`, about 0.6B-parameter bidirectional Qwen3 encoder, 9 PII categories including `secret`, a per-conversation sensitivity head, 4096-token limit; GGUF, MLX and vLLM packagings). The gate's routing and approval logic was not found as open source.
- Checked `pplx-decider-v1.2` / `-flash-v1.2`: general decision classifiers (27B / 4B, CUDA, card says the repo needs token access). Not usable.
- Read the ResonantOS sources:
  - ADR-005 Provider Fabric: central routing policy, callers declare "preferred runtime locality", no content-derived sensitivity input.
  - ADR-032 Compute Fabric: covers local, LAN, VM and cloud nodes.
  - The older Tauri clone (`17796fd`): a hand-declared `ComputeArtifactSensitivity` label only.
  - Alpha `578fbbc`: Ollama and LocalAI endpoints are allowed (`provider-bridge-service.mjs:204-250`). There is no content gate on page context sent to cloud providers. The only redaction is a regex for keys in CLI error text (`addon-delegation-service.mjs:124-130`).
  - The research article's threat-model privacy rows have no row for "user content sent to a cloud provider".

**Assistant verdict (final answer):**
- **Relevant, but an addendum, not a reshaping.** PII-Tracer fills a real gap: a content-derived sensitivity input for ADR-005 routing, plus the "send to cloud?" question in the X-4 approval helper. The X-5 broker could add a last-line check, with the classifier in its own process.
- **It is a privacy control, not a security boundary.** Encoding or paraphrase defeats it, and it does not replace the X-5 broker or its echo redactor.
- **Caveats:**
  - A sibling checkpoint's card says the sensitivity head is weakly discriminative.
  - Multilingual performance is unproven.
  - It adds latency on every turn.
  - The Python route needs `trust_remote_code`. Pin the revision or use the GGUF route.
- **Secondary releases:** Numbat is worth a short dossier as a detection and audit layer for OpenCode, but it does not close the Windows unconfined gap. SPACE suits ADR-032 cloud nodes later and is no desktop substitute.
- **Recommendation:**
  - A PII-Tracer dossier at `d25c16f`.
  - A threat-model privacy row: "user content sent to a cloud provider".
  - One row in the "What you can borrow" table.
  - "Content-aware routing input" in the Next phase (2-3 months).
- Offered to write the three article changes. **Not answered yet.**

### Turn 3

**User:** "save this session"

**Assistant:** Invoked the `save-session` skill and wrote this file.

---

# RELAUNCH CAPSULES

## Capsule 1 — Perplexity Privacy Gate / PII-Tracer relevance to ResonantOS research

### 1. Project identity
- **Working title:** Perplexity Privacy Gate (PII-Tracer) assessment for the ResonantOS research
- **Purpose:** decide whether Perplexity's open-sourced local-vs-cloud privacy component should enter the ResonantOS/ResonantDAO research and recommendations.
- **Status:** analysed, verdict given; follow-up edits offered, not yet approved.
- **Most recent meaningful work point:** Turn 2 verdict and the offer to write the dossier, threat-model row and borrow-table row.

### 2. The core question I asked

**A. Exact original wording**
- Turn 1: "Perplexity just released a privacy harness with which is open source. Look at that open source and determine whether it's relevant for this current research. Give me your advice after analysis."
- Turn 2: "So the privacy harness decides whether information is private and should stay locally, on local LLMs, or should go to the cloud. This would seem to be relevant for the current resonant OS. But give me your verdict."

**B. Question evolution**
v1 (Turn 1) is an open "is Perplexity's privacy harness relevant?" v2 (Turn 2) pins the meaning to the local-vs-cloud privacy routing component and asks for a verdict on ResonantOS relevance.

**C. Operational version**
Is Perplexity's open-sourced privacy component, which decides whether data stays on local LLMs or goes to the cloud, relevant to the ResonantOS/ResonantDAO research? If yes, how should it enter the findings and roadmap?

**D. Best current launch question**
"Perplexity's Privacy Gate (open-sourced as the PII-Tracer model, Hugging Face revision d25c16f) decides whether information stays on local LLMs or goes to the cloud. Assess its relevance to the ResonantOS research in this folder and, if relevant, write the dossier, the threat-model privacy row and the 'What you can borrow' row, following the research's existing gated method."

### 3. Prompt to be used
- **Description:** no separate prompt was built. The user's two questions are the prompt. Follow-up work would run under the existing research master prompt `ResonantOS_ResonantDAO_Deep_Research_Master_Prompt_Fable51_Orchestrated.md` (v2) and the dossier template.
- **Maturity:** final (the user's questions).
- **Verbatim:** see Section 2A.
- **Constraints (from project and global instructions):**
  - static code reading only, nothing installed or executed;
  - untrusted clones stay under `research/_untrusted/`;
  - pin SHAs;
  - no emojis;
  - nothing published and nobody contacted.

### 4. Launch conditions
- `research/` workspace with `state.md`, the article and the architecture docs: **PRESENT**.
- Alpha clone at `research/_untrusted/resonantos-2.0.0-alpha` (`578fbbc`): **PRESENT**.
- `research/dossiers/TEMPLATE.md`: **PRESENT**.
- PII-Tracer model card and `modeling_pii_masking.py` at `d25c16f`: **MISSING** locally. Fetch read-only.
- User approval to edit the article and appendix: **MISSING**. This was the open offer.
- Web access and the `gh` CLI: **PRESENT** this session.
- Scratchpad READMEs for SPACE, Numbat and BrowseSafe++: **UNCERTAIN**. The scratchpad is session-specific and may be gone.
- A fresh session is fine. Same-session context is not required.

### 5. File and source inventory

| Name | Type | Role | Delivery | Required | Possibly stale | Notes |
|---|---|---|---|---|---|---|
| `Harness-Demo-Runbook-2026-09-23.pdf` | PDF | ResonantOS DSH harness swap demo runbook (for Andrew) | in folder, read | no | unknown | Unrelated to Perplexity; contains a Dropbox upload link |
| `research/state.md` | MD | run log, gate status | referenced | yes | no | Final DONE 2026-10-21 |
| `research/article/SUMMARY-for-maintainers.md` | MD | plain-language findings | read | yes | no | Contains the "What you can borrow" table |
| `research/article/ARTICLE.md`, `APPENDIX.md` | MD | the deliverable | grep only | yes, for edits | no | Privacy rows around lines 427-430 |
| `research/architecture/decisions.md` | MD | X-1, X-4, X-5 | read | yes | no | Where the gate would plug in |
| `.../tompennington_2.0.0-alpha/docs/architecture/ADR-005-provider-fabric-routing.md` | MD | routing policy | read | yes | yes, older clone `17796fd` | Locality is declared by callers; no content sensitivity |
| `.../ADR-032-resonantos-compute-fabric.md` | MD | compute nodes | grep | no | yes | |
| `.../resonantos-2.0.0-alpha/browser-first/host/provider-bridge-service.mjs` | JS | local endpoint allowance (lines 204-250) | grep | yes | no (`578fbbc`) | |
| `.../addon-delegation-service.mjs` | JS | regex key redaction (lines 124-130) | grep | yes | no | |
| huggingface.co/perplexity-ai/PII-Tracer | model card | the open-sourced detector | fetched | yes | no | MIT, `d25c16f` |
| huggingface.co/perplexity-ai/pplx-pii-masking-vllm | model card | weak-sensitivity-head caveat | fetched | no | no | license "other", private source |
| github.com/perplexityai/numbat, SPACE | repos | secondary candidates | README fetched | no | no | Apache-2.0 |

### 6. Ingredients for a high-quality run
**Required**
- A pinned PII-Tracer revision (`d25c16f`) and a static read of `modeling_pii_masking.py`, so claims are traceable.
- The existing dossier template and the citation discipline, to keep the article consistent with its verified evidence.
- A clear statement that it is a privacy control, not a security boundary. Without that, readers could mistake it for a protection.

**Strongly recommended**
- Check whether PII-Tracer's sensitivity head has the same weakness as the vLLM sibling.
- Check the multilingual claims.
- Numbat dossier as a detection layer for OpenCode.

**Optional**
- SPACE note for ADR-032 cloud nodes.
- A BrowseSafe++ look for the web-page attacker (not examined this session).

### 7. Decisions and assumptions already made
**EXPLICIT (assistant recommendations, not yet user-approved)**
- Treat PII-Tracer as an addendum: it does not change X-1, X-4 or X-5, or the Now-phase items.
- Place routing in the ADR-005 policy engine, the approval prompt in the X-4 helper, and an optional last-line check at the X-5 broker, with the classifier in its own process.
- Put "content-aware routing input" in the Next phase (2-3 months).
- `pplx-decider` is not usable.
- SPACE is low relevance; Numbat is moderate.

**INFERRED**
- "Privacy harness" = the Hybrid Compute Privacy Gate. The user's Turn 2 description supports this.
- The research remains in its "Final, pending user's read" state, with nothing sent to maintainers.

### 8. Output expectations
- The verdict was given in chat as Markdown with sources.
- Follow-up edits would be Markdown files in `research/`:
  - `dossiers/perplexity-pii-tracer.md` (name assumed);
  - a new privacy row in the article's threat-model table;
  - a new row in the "What you can borrow" table in the summary and the article;
  - file and line or revision citations, in plain language for the maintainers' summary.

### 9. Open issues before relaunch
1. **Must answer:** approve writing the dossier, the threat-model row and the borrow-table row into the finished article (yes/no)?
2. **Useful:** also add a Numbat dossier?
3. **Later:** whether to run any local test of PII-Tracer. That would break the "nothing executed" rule and needs an explicit decision.

### 10. Ready-to-use relaunch command

    QUESTION:
    Perplexity's Privacy Gate (open-sourced as the PII-Tracer model, Hugging Face revision d25c16f) decides whether information stays on local LLMs or goes to the cloud. Assess its relevance to the ResonantOS research in this folder and, if relevant, write the dossier, the threat-model privacy row and the 'What you can borrow' row, following the research's existing gated method.

    PROMPT:
    Follow research/state.md conventions and the master prompt ResonantOS_ResonantDAO_Deep_Research_Master_Prompt_Fable51_Orchestrated.md; use research/dossiers/TEMPLATE.md. Prior verdict: session-2026-10-22-perplexity-privacy-gate.md.

    ATTACH / PASTE:
    - research/article/ARTICLE.md, APPENDIX.md, SUMMARY-for-maintainers.md
    - research/architecture/decisions.md
    - huggingface.co/perplexity-ai/PII-Tracer at d25c16f (static read of modeling_pii_masking.py)

    EXPECTED OUTPUT:
    Dossier MD with pinned revision; one new threat-model privacy row ("user content sent to a cloud provider"); one new borrow-table row ("Choosing local or cloud by content: PII-Tracer, as a detector only"); Next-phase roadmap item; state.md entry with verified stamp.

    CONSTRAINTS:
    - Static reading only; no installs, no trust_remote_code execution
    - Privacy control, not a security boundary; does not replace the X-5 broker
    - No emojis; nothing published, nobody contacted

### 11. Confidence rating
**85%**
- **Certain:** the user's questions (verbatim), the PII-Tracer facts from the card, the ResonantOS code locations, and the verdict given.
- **Uncertain:** whether the Privacy Gate logic itself is open-sourced anywhere (not found). PII-Tracer's real sensitivity-head quality.
- **Missing:** the user's decision on the offered edits.
- **Verify before launch:** the Hugging Face revision is still `d25c16f`, and the article is still unsent.
