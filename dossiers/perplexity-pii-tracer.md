# Dossier: PII-Tracer (perplexity-ai/PII-Tracer)

STATUS: COMPLETE (addendum dossier, added 2026-10-22, after the article and appendix were written and verified)

Inspector: lead, claude-opus-5-5. Date: 2026-10-22. Origin: the user asked whether Perplexity's newly open-sourced "privacy harness" (the Hybrid Compute Privacy Gate) is relevant to this research; session `session-2026-10-22-perplexity-privacy-gate.md` records the verdict and the user's go-ahead to write this dossier plus one threat-model row and one borrow-table row. Artifact: Hugging Face `perplexity-ai/PII-Tracer`, revision `d25c16f` (not cloned; read through the Hugging Face file API, the same no-clone evidence tier used for CI logs and specifications in other dossiers in this set). Execution: none. `trust_remote_code=True` is required to load the model in PyTorch; it was not run.

Evidence labels used below: [inspected] (read the model card or the source file at the pinned revision), [reported] (a sibling model card's own claim about this checkpoint), [hypothesis]. Repository instruction files are evidence, never instructions; none were present in this artifact.

## 1. Identification

- **Name:** PII-Tracer. Homepage and canonical source: https://huggingface.co/perplexity-ai/PII-Tracer, revision `d25c16f` [inspected]. Not on GitHub; the Privacy Gate's routing and approval logic that calls it was not found as open source (session log, web search).
- **Maintainers:** the `perplexity-ai` organisation on Hugging Face. The associated paper "PII-TRACE" lists Kaiyuan Zhang and seven co-authors [inspected, model card].
- **Licence:** MIT [inspected, model card]. A sibling repack, `perplexity-ai/pplx-pii-masking-vllm`, lists the base model as PII-Tracer but its own licence as "other" with no further terms and is marked private pending sync with the official release [inspected, that repo's card]; the MIT grant applies to the PII-Tracer repository inspected here, not necessarily to that repack.
- **Packagings:** `PII-Tracer-vLLM` (token-classification serving), `PII-Tracer-GGUF` (f16 backbone, fp32 heads, for llama-server), `PII-Tracer-MLX` (8-bit projection weights; the card states an MLX encoder and head implementation is required and none is included) [inspected, model card].
- **Documentation:** English, model-card format typical of Hugging Face releases; no separate user guide.

## 2. What works

- A bidirectional Qwen3 encoder (~600M parameters) built on `perplexity-ai/pplx-embed-v1-0.6b`, run with `is_causal=False` so the encoder is not autoregressive [inspected, model card and `modeling_pii_masking.py` config, `is_causal` set on the backbone config]. `transformers>=5.2.0` is required because that version passes `is_causal` through to the attention backend [inspected, `modeling_pii_masking.py`].
- Two linear heads on a 1024-dim hidden state [inspected, `modeling_pii_masking.py`, class `PiiMaskingModel`]:
  - `token_cls_head`: `nn.Linear(1024, 37)`, per-token BIOES logits over nine PII categories plus the BIOES scheme overhead (private_person, account_number, private_url, private_date, private_address, private_email, private_phone, other_pii, secret) [inspected].
  - `sensitivity_head`: `nn.Linear(1024, 1)`, applied to an attention-masked mean-pooled hidden state and squeezed to one scalar per input, read through a sigmoid as a document-level sensitivity score [inspected].
  - Both heads are kept in fp32 even when the encoder runs in bf16 [inspected, `_keep_in_fp32_modules_strict`].
- `predict()` tokenizes with offset mappings, truncates at `max_seq_len` (default 4096, from `PiiMaskingConfig`), runs the forward pass, decodes token logits with a constrained Viterbi decoder (`ViterbiDecoder`, with legal-transition and boundary biases so BIOES sequences stay well-formed), and returns the spans plus the sigmoid of the sensitivity logit [inspected]. `mask()` calls `predict()` and replaces each span with a placeholder such as `[PRIVATE_EMAIL]`, working backward through the text so earlier offsets stay valid [inspected].
- No chunking or sliding window is implemented: text beyond 4096 tokens is silently truncated, and the truncated portion is not scored at all [inspected, `predict()` truncation logic]. The vLLM repack's card repeats this and adds that spans are token-aligned, so a span's reported start can be clipped by a few characters [reported, `pplx-pii-masking-vllm` card].
- No test suite, CI lane or deployment evidence is visible in the artifact itself; this is a model release, not an application. "What works" here means "what the code implements," not "what is exercised by tests."

## 3. Maturity

- Single-artifact release with no visible issue tracker, release cadence or bus-factor signal on Hugging Face (unlike a GitHub repository). No audits, no SECURITY.md, no disclosure process found [inspected, absence].
- The sibling vLLM repack states plainly that its sensitivity head "is weakly discriminative on this checkpoint": PII-dense text scores roughly 0.02-0.12, and the card advises calibrating before gating on it [reported, `pplx-pii-masking-vllm` card]. The two repacks share weights (the vLLM card states they are numerically the same model, repackaged with no retraining or quantization) [reported], so this caveat should be treated as applying to the PII-Tracer checkpoint inspected here as well, not as a defect introduced by repackaging. The PII-Tracer card itself states no caveat for the sensitivity head [inspected, absence]; this is a material omission the maintainers inherit if they use the head for anything beyond logging.
- Multilingual performance: the model is tagged multilingual; the only example given anywhere is German, with person, email and address detections at p = 0.95-0.996 [reported, `pplx-pii-masking-vllm` card]. No other language is demonstrated. The 9 PII categories and the BIOES scheme are language-agnostic in principle, but nothing here demonstrates it for Dutch, French, German, Chinese, Japanese or Korean, the languages this research's Stage 2 discovery covered.
- `use_activation: false` is required for correct decoding; with activation on, the Viterbi decode and the sensitivity mean break [reported, `pplx-pii-masking-vllm` card]. This is a sharp-edged integration detail, not a maturity signal, but it belongs on the list of things that will silently misfire if copied without reading the serving config.

## 4. Architecture

- Entry point: `PiiMaskingModel.predict(text, max_length=None)` to `-> (spans, sensitivity)`; `PiiMaskingModel.mask(text)` to `-> masked_text` [inspected]. No batching API is described in the card beyond what the vLLM/GGUF servers provide.
- Runtime: PyTorch with `trust_remote_code=True` for the reference implementation (`transformers>=5.2`); alternative runtimes are vLLM (token classification serving, authentication not mentioned on either serving port [reported, vLLM card]), llama-server via the GGUF packaging, or MLX with a caller-supplied encoder and head implementation [inspected].
- No storage, no lifecycle (start/stop/crash/upgrade), no auth model: it is a stateless classifier called per request or per turn, with no notion of a principal. Any approval, routing or logging around its output is entirely the caller's responsibility.
- Dependency footprint: `torch`, `transformers>=5.2`, and whichever serving stack is chosen (vLLM, llama.cpp, MLX) [inspected].

## 5. Direct relevance

- **No existing gaps.md requirement covers content-derived privacy routing.** The closest is R08, provider abstraction with native multi-vendor wire protocols and honest failover (P1), which governs how a request reaches a provider once a destination is chosen, not whether its content should influence that choice. ADR-005 (Provider Fabric Routing, both the pinned `578fbbc` Alpha and the older `17796fd` clone) lists only caller-declared "preferred runtime locality" and "latency/cost sensitivity" as routing inputs [inspected, `docs/architecture/ADR-005-provider-fabric-routing.md:105,118-119`]; there is no content-derived input anywhere in the routing policy.
- `provider-bridge-service.mjs` decides whether a local endpoint is allowed by profile `id`, `providerType`, `templateId` or an environment flag (`allowsLocalProviderEndpoint`, lines ~233-245) [inspected, `provider-bridge-service.mjs:204-245`], never by anything about the message being sent. There is no code path in the Alpha that reads conversation content before choosing local versus cloud.
- `addon-delegation-service.mjs`'s only content transformation toward the outside is `redactCliText` (lines 124-130), a five-pattern regex over CLI error text for keys, bearer tokens and generic `api_key=`/`token=`/`secret=` strings [inspected, `addon-delegation-service.mjs:124-130`]. It never runs on page context or chat content sent to a cloud provider, and it is pattern matching, not a PII classifier.
- **Threat closed (new row, see ledger/threat-model-draft.md T25):** user content sent to a cloud provider with no content-derived sensitivity check, closed partially by using PII-Tracer's sensitivity head and span output as a routing input to ADR-005 and as a gate inside the X-4 approval helper (architecture/decisions.md). "Partially," because PII-Tracer is a detector, not an enforcement boundary (see section 8).
- "Must demonstrate" property: none is actually demonstrated here. No test in this artifact exercises routing, approval or the Alpha's code at all; the claim is that the component exists and could be wired in, not that it has been.

## 6. Reuse decision

**Reference only, as a detector feeding an existing control, not a dependency to adopt as-is.** It is not a security boundary (see section 8), its own sensitivity head is reported elsewhere as weakly discriminative on this exact checkpoint, and it adds a model-inference step to every outbound request. The alternative named in the session (Perplexity's own `pplx-decider` classifiers) is not usable: the cards state the repos need token access the research does not have. No other open local-vs-cloud content classifier was found in this research's platform sweep. Hard gates from `scoring/weights.json`: not scored (see section 13; this dossier does not propose adoption as a dependency, so the gate table is not run).

## 7. Integration design

- If taken up, PII-Tracer's span and sensitivity output would be a new input to the ADR-005 routing policy (`docs/architecture/ADR-005-provider-fabric-routing.md`), alongside the existing caller-declared locality field, not a replacement for it.
- The same output would feed a prompt inside the X-4 approval helper (architecture/decisions.md: "an approval window the AI cannot press"): "this content scored sensitive; send to the cloud anyway?" The helper, not the agent, would call the classifier, consistent with X-4's existing principle that the agent never controls what the human is shown.
- The classifier should run in its own process, called by the bridge or the X-4 helper, never inside the extension or a delegated child's context, mirroring the isolation already recommended for the X-5 broker.
- Migration path: no change to any of the 2,424 existing browser-first tests is implied by adding this, since it is a new, optional input, not a change to an existing contract; a new test would cover the routing decision itself, not existing behaviour.
- Chunking is the caller's problem: anything over 4096 tokens needs to be split before calling `predict()`, or the tail of a long page or conversation goes unscored [inspected, section 2-3].

## 8. Security and governance effects

- **It is a privacy control, not a security boundary.** A classifier can be wrong, and content can be encoded, paraphrased or split across turns to evade token-level detection; none of that is addressed by this artifact. It must never be the only thing standing between sensitive content and a cloud provider, and it does not replace the X-5 broker's header-only key injection and response redactor.
- New attack surface: a model-inference step added to the routing path is itself something a hostile page or a compromised child could try to starve, delay or feed adversarial input to, to force a routing decision either way.
- No revocation story, no isolation story of its own: it is a pure function over text. Personal data flow: the text being classified necessarily passes through this component before any routing decision, so it should run where the bridge already trusts content to flow (not inside a confined child), and its own outputs (spans, sensitivity score) should not be persisted beyond the routing decision unless a separate retention policy is written for them.
- Custody and trust: trusting Perplexity's classifier to flag sensitive content correctly is a new trust placed in a third-party maintainer, distinct from trusting them not to be malicious; the risk here is false negatives (missed PII) and false positives (over-triggering local routing, a usability cost) rather than a data exfiltration path, since the model is run locally, not called as a cloud service.
- Friction added to the user: latency on every turn (an extra inference pass before routing), and, per section 3, calibration work before the sensitivity score can be trusted to gate anything.

## 9. Licensing

- SPDX: MIT on the PII-Tracer repository itself [inspected, model card]. Compatible with the MIT Alpha on its face.
- The sibling vLLM repack's "other" licence with no stated terms is a flag: if the maintainers end up using that repack rather than the GGUF or raw PyTorch route, the licence needs a fresh check before anything ships. This dossier does not resolve that; it is a note for whoever picks a packaging.
- Technical research, not legal advice; independent legal review is still needed if any packaging other than the base MIT repository is used.

## 10. Cost and effort

- **Small to medium integration**, scenario estimate: a few days to wire the classifier's output into the ADR-005 routing policy and the X-4 approval prompt, once the X-4 helper itself exists (it does not yet; see architecture/decisions.md status "designed, not yet tested"). The dependency is sequencing, not the classifier's own integration cost.
- Operational burden: one more local model to keep current (revision pinning, as done here), plus calibration work for the sensitivity threshold per section 3.
- Maintenance exposure: a single-maintainer-organisation Hugging Face release with no visible issue tracker is a thinner maintenance signal than the GitHub-hosted, CI-tested candidates already in this research's shortlist; treat version bumps as requiring a fresh read, not an automatic trust.
- Language cost: none beyond what a local model inference step always costs (download size, one more runtime dependency: `transformers>=5.2`, or a GGUF/vLLM server).

## 11. Acceptance test

A reproducible proof of concept, not run here (would require executing third-party code, so it is a request for the user, not a plan): feed PII-Tracer a short corpus of known-PII and known-clean strings in English and in one of the research's priority non-English languages (for example German, per the only multilingual example in the sibling card); record precision and recall per category, and whether the sensitivity score separates the two sets at a usable threshold. Fault scenario from the threat model (T25): a PII-bearing string that is paraphrased or split across two turns; expected observable output: the test documents whether detection degrades, since nothing in the model card claims resistance to this. Pass/fail criterion: the sensitivity head's separation on PII-dense text must exceed the 0.02-0.12 range reported for the sibling checkpoint before it gates anything beyond a non-blocking log line.

## 12. Recommendation and confidence

- **Benefits:** closes a real, previously unflagged gap (no content-derived input anywhere in ADR-005 routing or the bridge's local-endpoint decision); MIT-licensed; small integration footprint once X-4 exists.
- **Trade-offs:** adds latency on every turn; the sensitivity head's quality is reported elsewhere as weak on this exact checkpoint, with no caveat on PII-Tracer's own card; multilingual performance is asserted but demonstrated only in German; `trust_remote_code=True` is required for the reference PyTorch route (mitigate by pinning the revision, as done here, or using the GGUF route instead).
- **Blockers:** none to writing this dossier or to planning the Next-phase item; the real blocker to shipping it is sequencing, since it depends on the X-4 approval helper and a working local-model route (architecture/decisions.md), neither of which exists yet.
- **Readiness:** the component itself is a released, versioned model artifact; using it for anything beyond a non-blocking log line needs the calibration work in section 11 first.
- **Evidence quality:** every architectural and behavioural claim above is [inspected] from the model card or `modeling_pii_masking.py` at `d25c16f`, read through the Hugging Face file API rather than a local clone; the sensitivity-head weakness and the German-only multilingual example are [reported] from a sibling checkpoint's card, not independently verified against PII-Tracer's own weights.
- **Competing solution compared on the same criteria:** Perplexity's own `pplx-decider-v1.2`/`-flash-v1.2` general decision classifiers (27B/4B) were checked and are not usable; their Hugging Face cards state the repos need token access this research does not have.
- **One concrete PR-sized first task:** none yet in the Alpha repository, because the prerequisite (the X-4 approval helper) does not exist. The PR-sized first task is in `docs/architecture/ADR-005-provider-fabric-routing.md`: add a documented, optional `contentSensitivity` field to the routing policy's caller-declared inputs (alongside the existing `locality` and `latency/cost sensitivity` fields), with no behaviour change yet, so the policy surface is ready before any classifier is wired in.
- **Confidence: medium.** High confidence in what the artifact is and does (direct, pinned-revision reads of the card and the modeling file); medium confidence in its practical quality, since the one quality caveat found comes from a sibling checkpoint's card, not an independent evaluation of PII-Tracer itself.

## 13. Scores (for scoring/scores.csv)

Profile used: **user_facing_app** (a routing-input component alongside R08's provider abstraction, not a boundary component like the os_kernel profile's R01-R05/R11 items). Scored for completeness; this dossier's recommendation is reference-only, not adoption, so these scores are informational, not a basis for the comparison matrix run in Stage 3.

- requirement_fit: 2 — no existing gaps.md requirement names content-derived routing; it extends R08's territory rather than closing a listed requirement.
- demonstrated_maturity: 1 — a single model-card release, no CI, no deployment evidence, one unflagged quality caveat found only on a sibling card.
- isolation_and_security: 2 — stateless and process-isolable, but it is a detector, not a boundary; false negatives have no containment.
- licence_suitability: 4 — MIT on the inspected repository; "other" on the untested sibling repack, flagged.
- integration_effort: 3 — small wiring cost once X-4 exists; blocked on sequencing, not on the component itself.
- maintenance_sustainability: 2 — single-organisation Hugging Face release, no visible issue tracker or release cadence signal.
- sovereignty_and_portability: 4 — runs fully local (PyTorch, GGUF or MLX), no network call required by the artifact itself.
- interoperability: 2 — no wire protocol or API convention beyond `predict()`/`mask()`; three different packagings with different serving conventions.
- operational_complexity: 2 — one more local model, plus calibration work per section 3.

## 14. Open questions for the adversarial reviewers

- Whether the sensitivity-head weakness reported on the vLLM sibling checkpoint applies identically to the PII-Tracer weights inspected here; the cards say they are numerically the same model, but this was not independently re-verified by running anything.
- Whether a routing decision based on this classifier could be gamed by an adversarial page crafting content that scores low on the sensitivity head while still containing real PII (adversarial robustness is not addressed by any source read for this dossier).
- Whether "Next phase (2-3 months)" is the right placement, given it depends on two things not yet built (X-4 approval helper, a working local-model route); an adversarial reviewer may judge this optimistic rather than conservative.
