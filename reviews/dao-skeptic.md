# Stage 3 adversarial review: DAO and mechanism-design skeptic

STATUS: COMPLETE (2026-10-21)

## Header

- Role: DAO and mechanism-design skeptic (`reviews/BRIEF-stage3-reviewers.md` section 2)
- Agent id: s3-rev-dao
- Model: Claude Opus 5.5 (claude-opus-5-5)
- Date: 2026-10-21
- Scratchpad: `C:\Users\<local-user>\AppData\Local\Temp\claude\c--My-Agents-75-ResonantDAO-and-OS\0f2652ff-3bb9-401c-b3a1-df5f9a82067c\scratchpad\s3-rev-dao\` (scripts `rpc_check.py`, `rescore.py`; outputs `rpc_check_out.json`, `rescore_out.txt`)
- Context read: `stage1/dao-requirements.md` (sections 1-5), `stage1/interaction.md`, `stage1/gaps.md` (R12, R22-R30), `ledger/threat-model-draft.md`, `ledger/gate2-report.md` section 7, `scoring/weights.json`, `scoring/scores.csv`, `scoring/sensitivity-output.md`, `scoring/sensitivity.py`.

Dossiers read (last-modified time seen, Europe/Berlin):

| Dossier | Last modified | Depth of review |
|---|---|---|
| solana-foundation-rewards.md | 2026-10-21 10:17:19 | primary, full |
| identity-common-ts.md | 2026-10-21 10:15:52 | primary, full |
| hypercerts-lexicon.md | 2026-10-21 10:15:11 | primary, full |
| transparency-dev-tessera.md | 2026-10-20 15:03:04 | primary, full |
| tuf-js.md | 2026-10-21 10:18:44 | I2 check (sections 5-8, 11) |
| nanobrowser.md | 2026-10-20 14:59:40 | I2/I4 check |
| aaif-goose.md | 2026-10-21 10:23:32 | I2/I4 check |
| eclipse-biscuit.md | 2026-10-20 15:00:23 | I2 check |
| holepunchto-hypercore.md | 2026-10-20 15:00:51 | I2/I3 check |
| anthropics-sandbox-runtime.md | 2026-10-20 15:03:45 | I2 check (gates) |
| convira-sandbox.md | 2026-10-20 15:00:02 | I2 check (gates) |
| dapr-durabletask-go.md | 2026-10-20 15:01:35 | I2 check (gates) |
| datalad.md | 2026-10-21 10:14:55 | I2 check (gates) |
| getaegis-aegis.md | 2026-10-20 15:00:57 | I2 check (gates) |
| openworkflow.md | 2026-10-20 15:00:17 | I2 check (gates) |

Clones spot-checked (read-only; nothing under `_untrusted\` was invoked or executed):

| Clone | Commit(s) read | What was checked |
|---|---|---|
| `solana-foundation-rewards` | HEAD `0b1bf17`, `d795849`, `aa1cfd9`, `119f5f5`, all remote branches | where Points code lives; TransferPoints; dead points code in the audited tree |
| `identity-common-ts` | `42586cab` | salt helper, KB skip, revocation test, suspended status |
| `hypercerts-lexicon` | `db1f41c` | evaluation, acknowledgement, authWrite, badge award; tests for R26 record types |
| `transparency-dev-tessera/tessera` | `012e9e0` | `LogStateTracker.Update`, witness policy groups |
| `nanobrowser` | `f1e912d` | classifier vocabulary for governance and wallet actions |
| `resonantos-2.0.0-alpha` | `578fbbc` | harness receipt key lifetime and what receipt "attribution" contains |

Public RPC (read-only, nothing signed or sent), 2026-10-21 08:27:06 UTC, `https://api.mainnet-beta.solana.com`, slot 459562069. Full requests and responses in `rpc_check_out.json`:
1. `{"method":"getAccountInfo","params":["BKRW5hPM4cMjNNr2EKdpScMS5kmK5bTxdELTH4LurZnu",{"encoding":"base64","dataSlice":{"offset":0,"length":45}}]}` -> upgrade authority `DXtFpbPjcn2hxPnw79x1Pfoj35vXh5AsWBkS37YnXMVv`, last-modified slot 422571636.
2. `{"method":"getAccountInfo","params":["4CxQs26DewQ1KaCHfyyjktkYjndNdUqCJvVdygtJFwcJ",{"encoding":"base64"}]}` -> owner `SQDS4ep65T869zMMBKyuUq6aD6EgTu8psMjkvj52pCf`, threshold 3, time_lock 0, config_authority `1111...1111`, transaction_index 11, five members with permission mask 7. Off-line PDA derivation `[b"multisig", 4CxQs.., b"vault", 0]` under the Squads v4 program gives `DXtF..` (bump 254).

## Primary dossiers

### solana-foundation-rewards

**Test of the launch-message claim ("the Points credential exists only on an unmerged branch, so no shortlisted codebase supplies an adoptable R22 credential").** [OK] Confirmed, with two qualifications.
- `git ls-tree` of `program/src` per ref: 0 points files on `main`, on the six other remote branches and on `origin/feat/confidential-rewards-continuous`; 38 on `origin/feat/restore-points-continuous` (`119f5f5`); 9 at the audited `d795849` and at `aa1cfd9`. The 9 are dead code: `entrypoint.rs` at `d795849` dispatches only the 12 Direct/Merkle/EmitEvent arms and sends everything else to `InvalidInstructionData` (`entrypoint.rs:28-59` at `d795849`). No `instructions/points/` directory exists at `d795849`.
- Qualification 1 (D-...-2 below): the mint initialiser that sets NonTransferable plus PermanentDelegate is in the audited tree and is byte-identical to the branch copy.
- Qualification 2 (D-...-1 below): the branch credential is not non-transferable in the DR-01 sense, so even a merge would not supply R22.
- No other shortlisted dossier serves R22. identity-common-ts gives an off-chain, key-bound credential with status-list revocation, but it is not on Solana, has no audit and no governed re-binding (gaps.md R22 constraints). Gate 2's row 13 premise ("Mainnet, OtterSec-audited Token-2022 NonTransferable plus PermanentDelegate credentials", `ledger/gate2-report.md` section 7) is false. R22 has no adoptable candidate in Stage 3.

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| D-solana-foundation-rewards-1 | 5 (property table), 7, 12 First PR | "Non-transferable: `test_points_direct_spl_transfer_blocked` ... rests on Token-2022's own NonTransferable extension" (:100). The First PR verifier "checks the Token-2022 extensions (NonTransferable present; PermanentDelegate equal to the configured governance address)" (:199) | On the branch credited with the pattern, the program itself moves points between wallets. `TransferPoints` burns from `from_user` and mints to `to_user` through the PDA delegate: "Transfer via burn + mint (NonTransferable blocks standard transfers)" (`transfer_points/processor.rs:55-73` at `119f5f5`), allowed whenever `config.validate_transferable()` passes (`:28`), with `authority` and `from_user` co-signing (`accounts.rs:39-41`). The flag is chosen at InitPoints (`init_points/data.rs:20`). `test_transfer_points.rs:67` `test_transfer_points_success_to_new_user` exercises it on a mint that carries the NonTransferable extension (`:254, :317` set `transferable(1)`). So a NonTransferable mint whose holder and issuer agree can be sold. The proposed verifier would certify such a class as non-transferable. The extension is not the property; the controlling program's instruction set is. The dossier reads TransferPoints only as a re-binding limit (:102), not as a transferability bypass | major | Restate the property row: "non-transferable only if the controlling program has no issuer-mediated move, or the move is the governed recovery path". The verifier must pin the program-data hash (already in section 7 versioning) and read the class flag; it must label any PermanentDelegate-bearing mint "issuer-movable". Add an acceptance fault: `transferable=1` class plus a holder-issuer sale, expected verdict FAIL |
| D-solana-foundation-rewards-2 | Headline, 2, 3 | "It was removed three days later by `d795849` ... the audited commit contains no continuous or points instruction" (:9, :62); "PointsConfig ... state removed (dead at `aa1cfd9`)" (:147) | Correct for dispatch, incomplete for scope. At `d795849` the audited tree still compiles `pub mod points_cpi` (`utils/mod.rs:9, :23`), the Token-2022 initialiser "with NonTransferable + PermanentDelegate + MintCloseAuthority extensions" and `freeze_authority: None` (`utils/points_cpi.rs:24-25, :50, :58, :68, :85`), `state/points_config.rs`, seven `events/points_*.rs`, and discriminators `InitPoints = 22` to `RevokePoints = 28` (`traits/instruction.rs:36-43, :81-83`). `git diff --quiet d795849 119f5f5 -- program/src/utils/points_cpi.rs program/src/state/points_config.rs` returns 0: both files are byte-identical on the branch. This explains OtterSec's scope sentence about "non-transferable points" and probably Stage 2's misreading. The reuse decision does not change | minor | Reword: "the mint-construction helper and config layout were in the audited tree as unreachable code; the issue, revoke, transfer and use processors were never in audit scope." Check whether the OtterSec PDF names `points_cpi.rs` |
| D-solana-foundation-rewards-3 | 13 | isolation_and_security = 1, "Not 0 because the advisory is fixed in source" (:211, Q3) | The anchor is literal: "0 = contrary evidence (advisory, counterexample row)" (`weights.json` criterion_anchors). Both exist: GHSA-8hgp-gwvv-wrjf and the confirmed s2-br-f/s2-br-h rows. "Fixed in source" does not reach the deployed program, because the dossier itself shows that the deployed binary's source commit is unknown (section 2, :54). D-...-1 adds a credential-level counterexample on the very branch credited with the pattern. Total 2.26 -> 2.08, still last; the rank does not move | major | Apply the anchor (0), or amend the anchor text so that "fixed but unaudited and undeployed-unverified" has a defined score |
| D-solana-foundation-rewards-4 | 12 comparison, 6 | "Token-2022 plus a thin issuer program wins for R22", "5 of 5 if built as specified" (:195-197) | This compares inspected code with a design that does not exist. The winning column has no code, no audit and no deployed authority to inspect. It also cuts against the DAO's own Phase 1 boundary: "Everything token-bearing should wait" and the token is "optional" in core item 1 (`dao-requirements.md` section 1 item 10, section 5 item 1); threat T18 (premature on-chain commitment). The dossier's section 7 itself says Phase 1 keeps the registry off-chain | major | Score that column as status D, with maturity and audit "unknown". Reframe the R22 recommendation: Phase 1 = off-chain signed membership record in the R30 log (no token); Phase 2 = Token-2022 class, only after DR-54 (audit, custody policy) |
| D-solana-foundation-rewards-5 | 7 (on-chain design) | "Re-bind (DR-07) = k-of-n human attestations plus a timelock: burn on the old wallet, mint on the new, tombstone the old member PDA, and rate-limit" (:130) | Re-binding is a controlled transfer, so it is also a theft channel and a sale channel. (a) k colluding attesters can move a victim's membership; in the lost-key case the victim cannot veto during the timelock. (b) A member can "lose" a key on purpose and have the membership re-bound to a buyer's wallet. That is a sale disguised as recovery, which DR-07 forbids ("cannot be used to sell a membership"). The design names no attester-independence rule, no holder veto where the old key still exists, no lifetime cap and no appeal. The threat model does not list this threat either (TM-2) | major | Specify: a veto window for the old key, attester conflict rules (as for DR-24 reviewers), a public re-bind log entry with an appeal deadline, a lifetime re-bind cap, and the C_i history frozen until the appeal deadline passes. Add an acceptance fault: 3 colluding attesters re-bind member A |
| D-solana-foundation-rewards-6 | 7 | "Revoke burns through the permanent delegate and writes `{reason_hash, evidence_ref_hash, appeal_deadline}`" on-chain (:130) | This creates a permanent public record that wallet X was expelled. A successful appeal cannot erase it (DR-09, T14). Hashing the reason does not hide the event | minor | Keep revocation reasons in the off-chain registry. On-chain, hold only a status bit or a registry root |
| D-solana-foundation-rewards-7 | 14 Q5 | "I did not cross-check the vault PDA derivation" | [OK] Settled. My RPC read and an off-line derivation show that `DXtF..` is the index-0 vault PDA of multisig `4CxQs..` (bump 254), with threshold 3, time_lock 0 and 5 members (Header, RPC item 2). This confirms section 8. No objection | - | none |

### identity-common-ts

Spot checks [OK]: `generateSalt(16)` allocates `new Uint8Array(length / 2)` (`packages/crypto/src/crypto.ts:8`), so 64-bit salts (dossier Q4 confirmed). `verify` returns before any KB check when `keyBindingNonce` is absent (`packages/sd-jwt-core/src/index.ts:248-250`). "test to fetch the statuslist" is an empty TODO (`sd-jwt-vc/src/__tests__/index.test.ts:414-416`).

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| D-identity-common-ts-1 | 5 (T20), 7 sketch | "T20 ... closed at the format level if the builder copies harness receipt attribution into plaintext claims" (:158); `attribution: { human, ai, method: 'declared' \| 'measured' }` (:204) | Harness receipts carry no human/AI portion. They carry session, turn and dispatch identity: the cited test asserts `dispatch.session` and `turnId` only (`browser-first/test/harness-host-service.test.mjs:565-579` at `578fbbc`), and `harness-host-service.mjs` contains no human, AI or share field (grep). Nothing in the Alpha could fill `method: 'measured'`. The format can carry a split; no component produces one. T20 is "format ready, source absent", not closed | major | Drop `measured` from the schema until an OS measurement exists. Reword T20 as open. Name the component that would produce the split (R07/R12 seam) |
| D-identity-common-ts-2 | 5 (T13), 7 Identity semantics, First PR | "SD-JWT makes it tamper-evident after issue" (:157). The issuer is "the OS host provenance key (persistent, user-held)", stored "under `~/ResonantOS_User/CONFIG`" (:199, :213, :329) | The agent whose work is being attributed can sign its own attribution. Delegated children run unconfined outside macOS and can write the user state root through the bridge (threat model V3; OSC-32, OSC-45). A plain-file host key in the user state root lets an AI child issue a record saying `human: 1.0` under the "host" signature. The signature proves "a process with file access on this machine", not "the human". This makes T13 worse than "self-declared": the declaration need not even come from the human | major | The issuer key is held by the bridge only and is never readable by children (R03/R15). Issuance requires a human ceremony recorded in the R11 approval ledger. On the DAO side, treat host-signed attribution as a declaration (DR-17). Answer to dossier Q8: yes, require a second signer (reviewer attestation) before a human portion counts toward votes |
| D-identity-common-ts-3 | 7 Identity semantics | "The originating principal survives as `session.receiptRoot` over the Ed25519 harness receipts" (:215) | The receipts are signed with a key that is "generated anew, remain[s] in this closure, and [is] never persisted" (`harness-host-service.mjs:145-148` at `578fbbc`). Only its fingerprint goes to stderr (`:160-161`). A DAO reviewer cannot authenticate any receipt after the fact. `receiptRoot` is a user-computed hash over unauthenticated data, so I7 (third-party recomputation) gives integrity of a list, not of its origin | major | Embed each boot's receipt public key in the host-signed record and certify it with the persistent issuer key, or downgrade `receiptRoot` to "user-supplied index" |
| D-identity-common-ts-4 | 5 (R23 revocation, property table), 8 | "Revocation via status lists: Demonstrated" (:153); "issuer-revocable" (:138); the DAO status-list key "needs multisig or rotation under R24" (:251) | The test shows a bit being read. It does not show governed revocation. (a) A status-list token is one JWS with one signer, so "multisig" needs threshold signing or a governance step before signing, and neither exists here. (b) There is no history: every new token replaces the last, so the issuer can revoke a member and silently restore them (against DR-06 and DR-28). (c) Split view: the default fetcher pulls the list from the issuer's URI on each verification (`sd-jwt-vc-instance.ts:81-103`), so an issuer can serve different lists to different verifiers. That is targeted revocation, invisible to the member. (d) `Suspended = 0x02` exists (`token-status-list/src/types.ts:13`), but the default validator rejects every non-zero value as `STATUS_INVALID` (`sd-jwt-vc-instance.ts:111-117`), so suspension and revocation look the same | major | Log every status-list token (hash) in the R30 witnessed log and have verifiers require an inclusion proof. Put a governed revocation record (reason, authority, evidence, appeal deadline) before any bit flip. Map 0x02 to "suspended" in the wrapper. Reword the property to "bit-level revocation demonstrated; governed revocation not" |
| D-identity-common-ts-5 | 13; sensitivity-output R23 table | requirement_fit 3; ranked first for R23 at 3.7 | R23 asks for proof of key control, an off-chain registry, anchored commitments, inclusion proofs for members and revocation (`gaps.md` R23). The library supplies revocation logic and a key-binding path that was never shown to work with a wallet (dossier Q1). It has no registry, no anchoring and no inclusion proofs (section 5: "Not provided", "Not demonstrated"). For R23 that is anchor level 2 at most. The R23 competitor table also leaves out tessera, whose dossier proposes the registry itself ("Membership changes (join, revoke, recover) are log entries too", tessera :130) | major | Split the row: R12 stays at 3; R23 drops to 2. Add tessera to `requirement_ids` R23 and rerun the competitor table |
| D-identity-common-ts-6 | 13 | operational_complexity 5 "the status-list host is the DAO's own"; sovereignty 5 | The DAO must run a status-list issuer: an HTTP endpoint plus a governance-relevant signing key. That is one service (anchor 3-4). The default fetch also reveals each verification to the issuer, which the dossier itself notes (:246) | minor | Score 4 and 4, or justify 5 with an offline-only fetcher in the integration design |
| D-identity-common-ts-7 | 8 Personal data | "issue one credential per claim (batch issuance)" (:250) | Batch issuance, recommended for unlinkability, means several valid credentials per member. DR-04 ("at most one active Community Member credential per wallet") must then be enforced by the registry, not by the format. The dossier's R23 framing implies the format carries membership | minor | State that uniqueness and caps (DR-04, DR-10) are registry properties |
| D-identity-common-ts-8 | 4, 8 Friction | Wallet KB signing "shows an opaque JWS to the user", called friction (:106, :254) | This is a consent problem, not only friction. A verifier can ask a wallet to sign any base64url bytes, and users learn to sign blobs they cannot read. That conflicts with E8 (human-only signing with a "transaction payload summary") and with I3 (previewed) | minor | Use a SIWS-style human-readable message that carries `sd_hash`, nonce and audience, and define the KB check over that message |

### hypercerts-lexicon

**Test of the launch-message claim ("records are owner-mutable, against DR-28").** [OK] Confirmed at protocol level, with a citation correction.
- The badge lexicon says outright: "Expiry is not revocation; to revoke an award, the issuer deletes the record" (`lexicons/app/certified/badge/award.json:42`).
- ATProto repositories let their owner replace or delete any record. That is a protocol property [reported, ATProto repo spec; no PDS code was read by me or the inspector].
- The cited `authWrite.json:28` is weaker evidence than the dossier implies. It is an OAuth permission set: it lists what a third-party app may request (`"action": ["create", "update", "delete"]` over 13 collections, including `context.evaluation`). It shows that apps can be authorised to edit and delete. It is not the source of mutability.
- That reading adds a risk the dossier misses: any app the user grants `org.hypercerts.authWrite` can rewrite or delete that user's evaluations.
- Mitigation the dossier leaves at open question 1: an indexer the DAO runs from first publication can record every version, because firehose update and delete operations carry the prior CID [reported, ATProto sync spec, not inspected]. Edits made while the indexer is down stay unobservable, because `getRepo` returns current state only. DR-28 "X" stands for source records. The inspector's own design (a local Resonant ledger) already avoids the problem.
- Zero tests on the R26 record types also confirmed: `grep -rliE "evaluation|contribution|contributorInformation|acknowledgement" tests/` returns 0 files.

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| D-hypercerts-lexicon-1 | 5.1 DR-24, 5.2 "Reviewer independence", 8 | "evaluators are DIDs (`evaluation.json:18-26`); nothing else" (:161) | Reviewer identity is not just unchecked for independence; it can be forged. `evaluators` is a required array of DIDs written by the record's author (`evaluation.json:11, :18-26`). `signatures` is optional (`:69-73`), and the record lives in whatever repo publishes it. The repo signature authenticates only the repo owner. A contributor can publish, from their own repo, a schema-valid evaluation of their own activity that names any respected DIDs as evaluators. No acknowledgement type covers "evaluator confirms being listed": the examples are contributor inclusion, collection inclusion and "a record owner acknowledging an evaluation" (`acknowledgement.json:7`). The same holds for `activity.contributors[]` (consent only through an optional acknowledgement). For R26 this is the reviewer-capture class in its cheapest form: no reviewer needs to be captured, only named | major | In the Resonant `review` record, accept an evaluator only if that evaluator's key signs the record (signer = listed evaluator). Reject records whose evaluator list differs from the signer set. Add an acceptance fault: a self-published evaluation listing a third-party DID |
| D-hypercerts-lexicon-2 | 4, 8, 14 Q1 | Mutability "established from `authWrite.json:28`" (:74, :139, :216) | See the test above. The claim holds, but the main citation is an OAuth scope, not the mutability mechanism. Missed consequence: app-delegated rewriting of evaluations | minor | Cite the ATProto repo specification (putRecord, deleteRecord). Add the app-delegation risk. Record the archiving-indexer mitigation and its downtime gap |
| D-hypercerts-lexicon-3 | 5.1 DR-34 | DR-34 "C (pattern)" via `contributionWeight` plus acknowledgements plus optional signatures (:145) | `contributionWeight` "Must be a positive numeric value ... normalization can be performed by the consuming application as needed" (`activity.json:109-111`), so the split's meaning is left to the reader. Each acknowledgement does pin the weights through the activity CID, but acknowledgements are optional, and nothing makes the activity's validity depend on all of them. "Signed by each party" (DR-34) is therefore not met by the schema | minor | Grade it P. In the Resonant `claim`, require one acknowledgement per listed contributor, referencing the activity CID, before the claim enters review |
| D-hypercerts-lexicon-4 | 7 (export adapter) | "an exporter ... for public showcase, carrying only T1 commitments" (:207) | Under interaction section 5, T1 includes the provenance record, with tool identity and the human/AI split, and the declared dimensions. Exported to a world-readable, replicated ATProto network, these become permanent personal data that erasure on the origin PDS does not reach (DR-09, T14). Exporting reviewer DIDs would also open DR-26 retaliation | minor | Make the export per-item and opt-in, carry only artifact hashes and an activity title, and never export the attribution split or reviewer identities |
| D-hypercerts-lexicon-5 | 13 | isolation_and_security 1 | No change proposed. 1 is defensible because DR-28 contrariness is a design property, not an advisory. D-...-1 would justify 0 if the lead treats "reviewer identity forgeable" as contrary evidence for the Accounting family | minor (contested) | Lead decides whether forged-evaluator capability counts as contrary evidence under the anchor |

### transparency-dev-tessera

Spot checks [OK]: `LogStateTracker.Update` returns the old checkpoint without error when `c.Size <= lst.latestConsistent.Size` (`client/client.go:397-399`), as the dossier says. Witness policies support nested groups with thresholds (`witness.go:57-97`, `fromPolicy`), so the fix in D-...-1 can be expressed.

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| D-transparency-dev-tessera-1 | 7 Error behaviour vs 8 Capture | "With volunteer witnesses, use the policy '1 of 3', plus an alert" (:137); versus "The policy must include at least one witness outside the custodian set" (:172) | These two statements contradict each other, and the first defeats the R30 case. Under 1-of-3, one custodian-run witness satisfies quorum, so the custodians (who hold the log key) can show members a split view. That is exactly the V6 capture the witness design is supposed to stop, and it is the dossier's main argument for Tessera over hypercore. Also, the policy that protects members is the verifier's acceptance policy (member step 1, :134), not the log's publication policy. The dossier treats them as one | major | Publish a nested policy: a mandatory external group (at least 1 of the non-custodian witnesses) AND at least 1 more. Hard-code the member verifier to that policy. Have the acceptance test show that a checkpoint cosigned only by custodian witnesses is rejected by the member verifier |
| D-transparency-dev-tessera-2 | 5, 7, 8 | "An append-only, publicly auditable log ... A member checks their own record's inclusion" (:86); witnessing as anti-equivocation (:160) | Omission and censorship are not addressed. Only the operator appends (`POST /add`, :174), and witnesses see checkpoints, never entries. The log proves inclusion of what the operator chose to include; it cannot show that a member's claim, appeal (DR-26) or contest of a revocation was dropped. "Anchor proves ordering but not honesty" applies to the entry set as well as to the content | major | Add signed submission receipts: the log service returns a signed promise-to-include `{entry_hash, deadline}`, like a CT SCT, which the member can later present as proof of omission. Add acceptance fault 3(e): the operator drops an entry, and the member's receipt plus a later checkpoint prove it |
| D-transparency-dev-tessera-3 | 5 R30, 7, 14 Q9 | "Membership changes (join, revoke, recover) are log entries too, so the registry history is append-only" (:130); DR-51 public auditability | With commitments-only entries (DR-50), members can verify only their own inclusion. Custodians can append phantom members or phantom claims, and nobody outside can see it: the membership count, vote eligibility and per-dimension totals cannot be audited. That is the Sybil inflation and farming path of T16/V7, run by insiders. Q9 raises this for tallies only; it also covers the registry | major | Publish typed, non-identifying metadata per entry (entry type, epoch, a per-member pseudonymous commitment), require each membership entry to carry the member's own wallet signature over the commitment, and name an independent auditor with access to the off-log store. State the remaining risk in the article |
| D-transparency-dev-tessera-4 | 13 (dao_contract) | integration_effort 3 "a sidecar or service with a stable protocol"; operational_complexity 4 "One process and one disk plus a static host. Witnesses are run by others" | Both contradict the dossier's own text. Integration: the team has no Go (section 10 assumptions), and the anchor reads "1 = requires ... a language runtime the team does not have". The os_kernel row applies exactly that (score 1); the DAO operator is the same team. Operations: section 10 medium scope is a Go personality, systemd, static-host sync, "3 OmniWitness instances", a weekly memo anchor script and a member verifier page. With D-...-1 at least one witness must be external, but the dossier's own plan runs the others. That is several services (anchor 1); 2 if all witnesses really are external | major | Rescore integration_effort 1 and operational_complexity 2. The total falls from 3.74 to 3.46 (my `rescore.py`). The rank-1 position in dao_contract survives only because identity-common-ts falls too (cross-cutting C-2) |
| D-transparency-dev-tessera-5 | 7 Entry format | "`entry = SHA-256(salt \|\| canonical_json(record))`. The record ... stays off-log in the access-controlled store, and the member keeps the salt" (:129) | Whoever computes the entry knows both salt and record, so the salt protects only against outsiders. And the off-log store is the custodians': if it loses or alters a record, the commitment can be verified only by a member who kept a copy. Data availability of the records is the weak point, not of the log | minor | At append time, hand the member the record, the salt and the inclusion proof, and make keeping them part of the member client. Define what happens when the store cannot produce a committed record (presumption in the member's favour) |
| D-transparency-dev-tessera-6 | 8 Anchor | Weekly SPL Memo anchor "cheap insurance" (:171) | The custodian holds the fee-payer key and chooses the timing, so it can skip an inconvenient week or anchor a forked checkpoint (the memo checks nothing, as the dossier notes). A missed anchor must be detectable, or the anchor is only a signal | minor | Publish the cadence, have verifiers treat a missing weekly memo as an alarm, put the anchoring key under DR-48, and check consistency between successive memos |
| D-transparency-dev-tessera-7 | Header | (no STATUS line) | Unlike six other dossiers, this one carries no `STATUS: COMPLETE` line. The launch note says all fifteen are complete | minor | Add the line, or note in `state.md` that status lines are optional |

## OS dossiers checked for invariant I2 and OS-to-DAO evidence flow

The OS dossiers that touch the DAO boundary are tuf-js (E4/E10 certification and revocation), nanobrowser and aaif-goose (I4 human-only voting and signing), eclipse-biscuit (explicit I2 condition) and holepunchto-hypercore (I3 local log). No OS dossier proposes evidence flowing from the OS to the DAO; identity-common-ts and hypercerts-lexicon do (covered above).

### tuf-js

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| D-tuf-js-1 | 5 "Revoking one add-on", 6 G5, 8, 11 row 4 | "the Resonant start and update check disables the installed add-on" (:139); "The DAO decides who holds reviewer keys but never mints authority: keys verify bytes and grant nothing (I2)" (:166) | The G5 argument covers authority being granted, not authority being removed. Under this design, DAO-appointed keyholders can disable an installed add-on on every user's machine at the next refresh, with no per-user decision (acceptance row 4, :284: "add-on disabled"). In a captured or factional DAO that is a remote kill switch and a censorship lever, for instance against a competing add-on. It runs on DAO policy without any user act; I2 allows DAO state to "inform display and policy defaults", and automatic disabling goes beyond a default. The tombstone carries `reason` (:136), but there is no appeal reference or grace period | major | Revocation shows a user-visible warning and disables only on user confirmation, or after a stated grace period with a local override recorded in the R11 ledger. Tombstones carry `reason`, an appeal reference and the signers. Add an acceptance case: a revocation by a reviewer quorum is overridden by the user and the override is logged |
| D-tuf-js-2 | 5 table | "NFT role at review time" carried in signed `custom` fields (:133) | This must stay display-only (I2, I8). Nothing in the design forbids a later grant preset or trust tier from reading it | minor | Add an integration test that asserts no grant or trust-tier code path reads `custom` certification fields other than hash and revocation |
| D-tuf-js-3 | 8 | tuf-on-ci "defaults: one root signer, threshold 1" (:244) | The root is the governance key of the whole certification system (DR-48 analogue). The medium plan names 3 hardware keyholders but no root threshold, timelock or published key list | minor | State the root and targets thresholds (for example 3-of-5, as Sigstore uses, :243), publish the keyholder list, and record root rotations in the R30 log |

### nanobrowser

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| D-nanobrowser-1 | G5 (:98), 2 classifier rows | "human-only steps (pay, grant, secret input, prompt dialog) are the user's in every mode ... satisfying the human-only clause" | The human-only clause in interaction I4 and E8/E9 includes voting and wallet signing. The vocabularies (`src/browser-control/core/interaction/classify.ts:18-90` at `f1e912d`) contain no "vote", "cast", "delegate", "sign" (only "sign up"), "connect wallet", "claim", "stake", "mint" or "swap". Only pay and grant become user-only steps (`byName`, `:121-133`). A "Cast vote", "Delegate" or "Claim" button is at best `submit` (policy-gated) or unclassified. The wallet's own popup is a human backstop for on-chain signing, but Phase 1 votes are off-chain advisory forms (`dao-requirements.md` section 5 item 6), where no wallet popup appears | major | Restrict the G5 verdict to the classifier's categories. Add a governance and wallet category to the R19 gate requirements (vote, delegate, sign, connect wallet, claim, stake). Add an acceptance fixture: a Loomio-style vote page and a dApp "Claim" page |

### aaif-goose

No objections in scope. The dossier already records G5 as failing in any non-wrap configuration because Goose has no human-only action class (:168). That covers E8/E9 signing and voting. Goose proposes no DAO data flow.

### eclipse-biscuit

| Id | Section | Claim challenged | Objection and evidence | Severity | What would settle it |
|---|---|---|---|---|---|
| D-eclipse-biscuit-1 | 6 G5 | "A rule must forbid minting a Biscuit from a DAO credential (I2)" (:138) | The right condition, but as written it is a rule, not a test. A Biscuit fact such as `dao_role("reviewer")` added by a future integration would turn a DAO role into an authorization input without touching the mint path | minor | Add an integration test: the authorizer rejects any token or fact derived from a credential-verifier result. List DAO-derived facts as forbidden in the policy schema |

### holepunchto-hypercore

No objections in scope. It touches no DAO state (G5, :123). Its I3 role (local log of OS-to-DAO submissions) is served by any local log, as the dossier says (:93). Its caution that the approval proof must come from a human ceremony, not the bridge's own key, is the same point as D-identity-common-ts-2.

### anthropics-sandbox-runtime, convira-sandbox, dapr-durabletask-go, datalad, getaegis-aegis, openworkflow

No objections in scope. None of these touches R12, R22-R28 or R30, none moves OS data to the DAO, and none reads DAO state. Their G4/G5 lines (sandbox-runtime :104-105, convira :261-262, dapr :115, datalad :134, aegis :121-122, openworkflow :159) are correct for this role. One indirect dependency: containment (sandbox-runtime, convira) is what would make D-identity-common-ts-2 fixable, because an unconfined child can read any provenance key in the user state root.

## Cross-cutting

### C-1 The sensitivity check cannot see fragility at the top of short lists (scoring method)

`sensitivity.py` marks a codebase FRAGILE only if `abs(pos - basepos[cid]) > 1`, that is, only if its rank moves by two or more places. `weights.json` `_about` says something else: "a candidate whose rank changes under either check is marked fragile". The consequences, from my `rescore.py` (`rescore_out.txt`):
- In dao_contract, tessera (3.740) and identity-common-ts (3.720) swap places under 5 of the 27 perturbations: demonstrated_maturity x0.75, drop demonstrated_maturity, integration_effort x1.25, maintenance_sustainability x0.75 and drop maintenance_sustainability. Both are still reported "stable".
- Every per-requirement table with two competitors (R01, R02, R03, R10, R12, R23, R29) can never show FRAGILE, because two rows can move at most one place.
- **Severity: blocker for the scoring method** (it changes the fragility labels the comparison matrix is defined to show).
- **Settle:** flag any rank change, and print the margin to the next rank and the perturbation that closes it. Rerun.

### C-2 dao_contract weights reward components that leave the governance-critical work unscored

The five convenience criteria (licence, integration_effort, sovereignty, interoperability, operational_complexity) carry 0.36 of dao_contract weight, against requirement_fit at 0.16. They supply 41 to 52 percent of every dao_contract total: identity-common-ts 1.80 of 3.72, hypercerts 1.44 of 2.84, tessera 1.52 of 3.74, rewards 1.18 of 2.26.
- A library scores 5 on integration and operations because the hard parts are left out: the registry, the issuer and status-list keys, anchoring, the review layer and the re-bind ceremony. Those parts become custom code that nobody scores.
- No dao_contract criterion scores **authority and capture**: who can upgrade, mint, revoke or re-bind; with what k-of-n and timelock; with what appeal. isolation_and_security asks only whether "the property" is demonstrated, so a library with no authority of its own is never charged for the authority it pushes onto the integrator (D-identity-common-ts-4).
- With the rescorings above (D-identity-common-ts-5 and -6 plus a 2 on isolation for D-...-4, D-tessera-4, D-rewards-3):
  - baseline weights: tessera 3.46, identity-common-ts 3.30, hypercerts 2.84, rewards 2.08;
  - a capture-weighted profile (requirement_fit 0.22, isolation 0.24, maturity 0.16, maintenance 0.12, licence 0.06, integration 0.04, sovereignty 0.06, interop 0.04, operations 0.06): 3.40, 3.00, 2.56, 1.76.
- Either way the "near tie" at the top is an artefact of convenience scoring.
- **Severity: major.**
- **Settle:** add an `authority_and_capture` criterion to dao_contract (anchored on DR-48 and DR-06), or score the composed reference architecture for R22, R23 and R30 instead of the components. Raise requirement_fit to at least 0.20.

### C-3 The primitive is credited with the property

The same pattern appears in all four primary dossiers:
- **rewards:** the NonTransferable extension is credited as non-transferability, yet the program moves tokens anyway (D-rewards-1);
- **identity-common-ts:** a status-list bit is credited as governed revocation (D-identity-4), and a host signature is credited as attribution (D-identity-2);
- **hypercerts-lexicon:** a DID list is credited as reviewer identity (D-hypercerts-1);
- **tessera:** witness cosignatures are credited as capture resistance, under a policy that custodian witnesses can satisfy alone (D-tessera-1).

Each property check should name the full condition under which the primitive yields the property, and an acceptance fault that breaks it.

### C-4 Revocation fails DR-06 everywhere

None of the four designs records reason, authority, evidence and an appeal deadline, or allows reversal with history kept (DR-06):
- **rewards:** one authority key per distribution, a permanent marker, no appeal;
- **SD-JWT status list:** one JWS signer, overwritten with no history, split views possible;
- **hypercerts:** revocation by deletion;
- **tuf-js:** removal from `certified` auto-disables add-ons.

**Proposal:** one governed revocation record type in the R30 witnessed log, from which the derived artefacts are produced: status-list bits, TUF tombstones and any Token-2022 burn. Verifiers check that each derived artefact has a logged record behind it.

### C-5 Omission and split view are not threats anywhere

The dossiers and the threat model test tampering and rollback. They do not test:
- an operator who drops entries (D-tessera-2);
- an issuer who serves different status to different verifiers (D-identity-4);
- edits made while an indexer is not watching (D-hypercerts-2).

All three are cheap insider attacks in a custodian-run bootstrap (V6).

### C-6 Human/AI attribution has no source

Three dossiers carry a human/AI split field:
- identity-common-ts, in its payload sketch;
- hypercerts-lexicon, in its proposed `claim.humanAiSplit`;
- tessera, which leaves the split to its log entries (record content).

Nothing in the Alpha produces the number (D-identity-1). The signing key that would vouch for it can be reached by the agent being attributed (D-identity-2). T13 and T20 stay open by construction until an OS-side measurement and a human ceremony exist. The article should not describe R12 candidates as carrying attribution.

### C-7 Coverage

- R22 has no adoptable candidate (test above).
- R24, R25 and R27 have no dossier at all. T12 (high) closes with R24, T13 (high) with R25, and T16 with R27.
- The two highest DAO threats therefore depend on requirements nobody inspected in Stage 3. Gate 2's "not shortlisted" list names Realms and Squads v4 for R24 and HotCRP and go-eigentrust for R27 (`gate2-report.md` section 7).
- **Settle:** state this gap in the article's coverage limits, or run one more inspector on Realms plus Squads (R24), given that T12 is rated high.

### C-8 Status lines

Only 6 of 15 dossiers carry `STATUS: COMPLETE` (aaif-goose, datalad, hypercerts-lexicon, identity-common-ts, solana-foundation-rewards, tuf-js). A case-insensitive grep for "status: complete" returns 0 in the other nine: anthropics-sandbox-runtime, convira-sandbox, dapr-durabletask-go, eclipse-biscuit, getaegis-aegis, holepunchto-hypercore, nanobrowser, openworkflow and transparency-dev-tessera. This is minor bookkeeping, but it contradicts the launch note that all fifteen are marked complete.

### Threat model objections (T12-T20)

| Id | Threat | Objection | Severity | Settle |
|---|---|---|---|---|
| TM-1 | T12 | It covers only Resonant's own custodians. It misses inherited third-party authority: a shared program under someone else's 3-of-5 with time_lock 0 and a staged buffer (rewards section 8, confirmed by my RPC read). It also leaves out the off-chain governance keys: the status-list signer, the TUF root and targets keys, and the log and witness keys | major | Add "authority inherited from shared programs and off-chain trust roots" to T12, and list every key class under R24 |
| TM-2 | missing | Issuer-mediated transfer and recovery abuse: membership sale or theft through re-binding, or through a program-level move of a "non-transferable" token (D-rewards-1, D-rewards-5) | major | New threat (medium-high), closes with R22 and R25. Property: "re-binding cannot be used to transfer", demonstrated by a fault test |
| TM-3 | missing | Ledger-operator omission (dropped claims, appeals or contests) and insider Sybil inflation hidden by commitments-only entries (D-tessera-2, D-tessera-3) | major | New threat under T16 or T18. Properties: submission receipts and auditable entry-type counts |
| TM-4 | missing | Split view of issuer-served state: status lists, registry queries (D-identity-4) | major | Add to T15. Property: revocation state logged and witnessed |
| TM-5 | T16 | Reviewer identity spoofing (an evaluator named but not signing) is cheaper than reviewer capture and is not listed (D-hypercerts-1) | minor | Add it to T16's list. Property: "reviewer = signer" |
| TM-6 | T13 | It understates the threat. The AI child can sign provenance as the host when the provenance key is file-readable (D-identity-2). "Closes with: R12" is wrong, because a format cannot close T13 (the identity-common-ts dossier says so itself, :157) | major | Close with R03/R15 (key custody), R11 (human ceremony) and R25. Mark R12 as "necessary, not sufficient" |
| TM-7 | T19 | It covers DAO state becoming authority, but not DAO state removing capability without a user act: the certification-revocation kill switch (D-tuf-js-1) | major | Extend T19 to "grants or removes", or add a medium threat "remote disable or censorship via certification" |
| TM-8 | section 4 Credentials row | "non-transferable, issuer-revocable, governed re-binding; audit report" (:79) can be met on paper by a NonTransferable mint whose program moves it, and by a revocation without record or appeal | minor | Add "non-transferability tested at program level", "revocation recorded and appealable (DR-06)" and "re-bind collusion fault test" |
| TM-9 | T14 | Revocation and appeal records on a public chain create permanent stigma linked to the wallet (D-rewards-6). This is not in the evidence list | minor | Add it to T14's evidence. Property: no revocation reason on-chain |
| TM-10 | T17 | It is a specification defect, not an attack, and is correctly rated medium. Not overstated, but its closure ("a specification fix") has no owner | minor | Name the owner (maintainers, OI list) |

## Summary: objections for the lead to act on first

1. **C-1 (blocker, scoring method).** `sensitivity.py` hides every one-place rank swap, against the rule stated in `weights.json`. The dao_contract top two swap under 5 of 27 perturbations yet are reported "stable", and two-way competitor tables can never be FRAGILE. Fix the rule and rerun before any rank enters the article.
2. **D-transparency-dev-tessera-1 to -3 (major).** The R30 recommendation rests on witness anti-capture, but the dossier's own "1 of 3" policy lets a custodian witness satisfy quorum alone. Omission of claims and appeals and insider Sybil inflation behind commitments are not addressed. Adopt a nested policy with a mandatory external witness, signed submission receipts, and auditable entry-type counts.
3. **D-solana-foundation-rewards-1, -4, -5 and the R22 test (major).**
   - R22 has no adoptable candidate: Points is on an unmerged branch only, apart from dead helper code in the audited tree.
   - Even on that branch, the "non-transferable" credential can be moved by holder plus issuer (TransferPoints burn plus mint). The proposed verifier checks the wrong thing.
   - The proposed re-bind ceremony is an unguarded theft and sale channel.
   - Phase 1 should use an off-chain registry, not a token.
4. **D-identity-common-ts-1, -2, -5 (major).**
   - Nothing produces a human/AI split.
   - The provenance key would be reachable by the AI agent it attributes.
   - R23 fit is overstated, and the R23 table omits tessera.
   - Rescore R23 fit to 2 and add tessera to R23. T13 and T20 stay open.
5. **C-4 with D-identity-common-ts-4, D-hypercerts-lexicon-1 and D-tuf-js-1 (major).**
   - No candidate's revocation meets DR-06.
   - Reviewer identity in hypercerts can be forged.
   - TUF revocation, as designed, is a DAO kill switch over installed add-ons.
   - Proposal: one governed revocation record in the R30 log from which every derived artefact is produced, with user confirmation for disables on the OS side.

Objection counts: blocker 1 (C-1); major 23 (16 in dossier sections, 1 cross-cutting, 6 threat model); minor 19 (15 in dossier sections, 4 threat model); plus 1 [OK] confirmation row (D-solana-foundation-rewards-7).
- By dossier: solana-foundation-rewards 6 (4 major, 2 minor), identity-common-ts 8 (5 major, 3 minor), hypercerts-lexicon 5 (1 major, 4 minor), transparency-dev-tessera 7 (4 major, 3 minor), tuf-js 3 (1 major, 2 minor), nanobrowser 1 (major), eclipse-biscuit 1 (minor).
- No objections: aaif-goose, holepunchto-hypercore, anthropics-sandbox-runtime, convira-sandbox, dapr-durabletask-go, datalad, getaegis-aegis, openworkflow.
- Cross-cutting: C-1 (blocker), C-2 (major), C-3 to C-8 (patterns).
- Threat model: TM-1 to TM-10 (6 major, 4 minor).
