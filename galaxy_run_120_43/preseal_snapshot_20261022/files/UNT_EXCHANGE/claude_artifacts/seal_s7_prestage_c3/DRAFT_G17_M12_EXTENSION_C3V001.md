# DRAFT_G17_M12_EXTENSION_C3V001: extending G17's single CLASSIFIER role to the M-12 pair (DRAFT for root; P-117)

**From:** a Claude3-lane helper, for the lead, under root dispatch 0850 item 4. **This is a draft.** Root rules and records it (A292: V006 is outside Claude3's remit).
**Labels:** TESTED = from bytes. FORMAL = from reading the named texts.

## 1. The current G17 text: NOT FOUND in the named RUNBOOK (TESTED)

- **RUNBOOK c2v007:** `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2v007_cx2/RUNBOOK_V002_C2V007.md`, sha256 `12917ba93955f106f8ab30fb39d464cd6b1f0e5d27597d0c29c6c6c6cfb7c547`. It is the RUNBOOK of `verify_c3_runbook_c2v007/RESULT.json` `00de7bca`, field `object.runbook` = `12917ba9`.
  - `grep -c -i g17` gives **0**.
  - The G ids in the file are **G16 (L94), G26 (L98), G27 (L126) and G28 (L26)** only.
  - `grep -i classif` matches only L18, about the cause producer's "classifications". No CLASSIFIER role is defined in this file.
- **So the exact current G17 text cannot be quoted from the named source.** The only named-source statements of it are:
  - **A201 item 7:** "extend G17's single CLASSIFIER role to the M-12 pair";
  - **PLAN P-117:** "G17 single CLASSIFIER role extended to the M-12 pair … write-freeze window + G17 role pending".
- **Placeholder for the lead or root.** Paste the exact current G17 text here, from its source: the RUNBOOK version, or the RUNBOOK rulings entry that defines G17. Root must name it (SEAL_REMAINING §5 R1).

  ```
  G17 (current, verbatim): <<ROOT/LEAD: paste from its source; source path + sha256 + line range>>
  ```

- **What the RUNBOOK c2v007 does say about the seal** (FORMAL; quoted by line):
  - L90 (step 6): "Root's adopted seal and reading gates are prerequisites to any later value release…"
  - L96 (step 8): the final PASS_K runs "After the adopted seal/reading gates".
  - L102 (step 9-pre): "Seal check. Verify the adopted source/registration pins and unchanged six-roster mapping. Log manifest and registration hashes, phase/calibration record, L1, build record, ledger directory/head and the completed pre-target checks before any target read."
  - L110: "root fixes the committed rule set and Phase-1-score V006 cutoff, with the sealed module/slots version".
  - L124: the builder's commands include `seal-check`.

## 2. The proposed extension (additive; it leaves G17's current wording unchanged)

> **G17, extension for the M-12 pair (P-117; A201 item 7).** The single CLASSIFIER role stays single.
>
> 1. **CLASSIFIER = classifier A** `classifier_a_c4/build_c4v004/classifier_a_c4v004.py`, sha256 `e92aa30e22b98fea6c6e517702c02f77c43bfe429f69f8e0392963c94edc4cb0` (A173). It is the classifier that the seal entry registers with the r3a text (M-6 item 2; M-12 "Seal").
>    - At RUNBOOK step 9, root runs A, and only A, on the real score, through A's pinned fenced runner.
>    - A's tables are the report's tables. There is no hand classification.
>    - No other classifier output on any real manifest, score or target is produced or read.
> 2. **The M-12 pair is sealed as one unit of three pins:**
>    - A (above);
>    - **classifier B** `classifier_b_c2/build_c2v005/classifier_b_c2v005.py`, sha256 `cec5bfe9582899437aa715d78e1dfdb36089ebead04f840d4d68893b3d1251c7` (A193), whose role is AGREEMENT_PARTNER;
>    - **the A/B agreement record**, at `<<root: path>>` with sha256 `<<root>>` (A193: 364 of 368 shared bundles agree; B352, B407, B412 and B419 differ on forged-only inputs and are A115 NOTEs; the verifier's 10 of 10 honest bundles agree).
>
>    B is never run on real data (M-12 "Seal"). It holds no CLASSIFIER role in either phase.
> 3. **Seal check (RUNBOOK 9-pre).** Before any target read, root verifies the three pair shas from bytes against the seal entry, together with the text, the TSR flag record and the STAGE0 successor if pinned.
>    - Any mismatch is the pre-target stop SEAL_SHA_MISMATCH (M-6 item 5; text §1.1 L196).
> 4. **Successors.** A classifier change after the seal is POST-PREDICTION (CLASSIFIER) and is listed with its diff (text Status fallback; M-6 item 1). This covers a successor of A or of B, or a different agreement record.
>    - A changed A may run only after the M-12 agreement suite passes again.
>    - Before the seal, an A/B disagreement means the text is ambiguous, and the text is fixed before the seal (M-12).
> 5. **Lineage, disclosed (not a role change).** B is Claude2-built on Codex1's kernels, which are pinned by their V089 shas. It sits behind an information barrier from A and reads the producers' bytes for record forms (A176 §1; A190; A193). So the A/B agreement is partly same-family.
>    - The distinct-lineage adversarial review of B (Codex2, A205 item 7) is due before the Phase-2 seal. It does not gate Phase 1 and does not change the CLASSIFIER role.
>    - The disclosure goes in the seal entry and with the PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE) label.
> 6. **Phase 2.** The same assignment holds at the Phase-2 score unless root rules otherwise at the Phase-2 seal, after the distinct-lineage review.

## 3. Why each clause (FORMAL)

| Clause | Source (named) |
|---|---|
| 1. A is the only classifier run on real data; A's tables are the report's; no hand classification | ROOT_ITEMS_R3A M-12 "Seal" (L333): "A is sealed with the text, and the agreement record is pinned. Root runs A on the real score, and A's tables are the report's tables. B is not run on real data. There is no hand classification." (basis `9c40b567`) |
| 1. A c4v004 is the classifier-bearing seal candidate | V006 A173: "Under A168, the classifier-bearing SEAL CANDIDATE names **c4v004**" |
| 1. The fenced runner | README_CLASSIFIER_A_C4V004 (`e163d2aa`), "How to run": `tools/run_fenced_c4ep1.py` with fence `175b995b…`. The runner's own sha is in A's HASHES file, which was not opened here: `<<root pins it>>`. |
| 2. The pair is A c4v004 + B c2v005, with the agreement counts | V006 A193 ("the M-12 pair for the seal is classifier A c4v004 and classifier B c2v005") |
| 2. The agreement record is pinned | M-12 "Seal" (L333) |
| 2. B is never run on real data | M-12 "Seal" (L333) |
| 3. The seal check and SEAL_SHA_MISMATCH | M-6 item 5 (L185): "root verifies the sealed shas from bytes before RUNBOOK step 9"; text §1.1 (L196): "SEAL_SHA_MISMATCH: a sealed sha (this text, the classifier, the flag record, the STAGE0 successor if pinned) does not match its bytes"; RUNBOOK c2v007 L102 (9-pre) |
| 4. Successors are POST-PREDICTION; re-agreement before a run | text Status fallback, template L56: "Any later wording change, ruling or classifier change is POST-PREDICTION. It is listed with its diff…". Template L57, which covers only the no-classifier case: "…Its M-12 agreement suite must still pass before it runs." M-12 (L299, L332) requires agreement. The re-agreement duty for a changed A is this draft's proposal by analogy with L57; it is not quoted text. |
| 5. Lineage disclosure; the Phase-2 review | A176 §1 ("Disclosure. The seal entry and the PROVISIONAL (PHASE-1) label say that B's integration is Claude-built on Codex kernels…"); A193 (the seal bullet); A205 item 7 (Codex2, preferred to Codex1; a Phase-2-seal gate pulled forward) |
| The route: M-12 by id; A176 as the ruling on implementation B | FROM_CODEX/0751 (`62eb357d`); V006 A177 ("M-12 seal route … (a)") |
| G17 must be extended before the seal | V006 A201 item 7; PLAN P-117 |

## 4. Open points for root

- **G1. Where G17's current text lives** (§1 placeholder). If G17 already names a single classifier sha, the extension's clause 1 replaces that sha with A c4v004's and adds clauses 2–6.
- **G2. The agreement record's path and sha** (A193 does not give them).
- **G3. Pin the fenced runner by sha?** A's README shows it as the only documented way to run A. If root wants step 9 to accept only that runner, it pins the runner's sha in the seal entry. Otherwise it pins A alone.
- **G4. Where the extension goes.** Either in its own V006 entry before the freeze opens (it takes a NO_CHANGE row in the V006 table), or inside the seal entry. The helper proposes before the freeze, so that Claude3's delta review and Claude4's render see the rule fixed.
