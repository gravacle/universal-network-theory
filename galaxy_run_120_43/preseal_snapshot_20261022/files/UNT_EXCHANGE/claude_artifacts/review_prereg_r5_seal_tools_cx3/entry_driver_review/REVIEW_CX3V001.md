# Seal tools v002 r2 — entry coverage and driver BUILD review

`date -u`: Sun Oct 18 21:33:31 UTC 2026

**FAIL for D-05 closure: 1 BLOCKING finding in this assigned scope (ED-D05-1); no additional SHOULD_FIX finding.** The carried issue was classified SHOULD_FIX by the predecessor reviews; it blocks this review from declaring the explicitly requested D-05/R-02 fix complete. D-06 and the linked R-10 input equality checks are closed in the bounded scope below. No seal, root adoption or launch approval is given.

The final README selects `r2/` and lists exactly the four source hashes exercised here. The runtime record was produced while the handoff was still provisional; the subsequent byte check against the landed README found no source change. Thus the finding applies to the selected r2 sources, not merely a superseded draft.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/README_SEAL_TOOLS.md` — SHA256 `da29c008064ae51673dfe7106f72dfcb789f674b4c0a36e3a5daf017c7967af8`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/check_frozen_addendum_c4v002.py` — SHA256 `06a98bc6b56e71bff450b749b12a7e8978824baeda41458e4319506a0cfd1891`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/build_seal_record_c4v002.py` — SHA256 `4192983d262e2a27a3d9c90681b6ee66a90c901bfe2f99a7dce2349bc8c5de52`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/print_driver_build_record_c4v002.py` — SHA256 `fde0b26e7ea26d4ad15213cc9c3115a807179616e0e155037c97d2179db7a673`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/seal_common_c4v002.py` — SHA256 `f41b0fca51a95387577839e52308a2dc6ccb79b1e6b9283f389b54c7f348dc10`

**ED-D05-1 — bare later-entry coverage still substitutes boilerplate for a reasoned decision (TESTED).** Tool 1 accepts a frozen entry after the last cited one solely because its name appears in `covered_later`. The builder has no input for that entry’s revision/no-change decision or explanation. Its `no_change_note` emits “A102: covers this entry for the prereg text of record (A81 RI-26)”. A changed existing table row can similarly pass by name; its generated note supplies old/new section hashes and calls itself an explicit note, but states no effect on the prereg text.

Reproduction uses only new synthetic files in this review directory:

1. A82–A101 with 20 correct table rows: PASS.
2. Add A102 without a table row or coverage name: REFUSE `UNCOVERED_LATER_ENTRY`.
3. The same bytes with `covered_later=("A102",)`: PASS; the actual builder helper supplies only the fixed sentence above.
4. Change A90 to a synthetic changed scientific rule: REFUSE without coverage; PASS with `covered_later=("A90",)` and a generated note containing the two hashes, without a reason or superseding decision.

This is the remaining mechanism identified by predecessor R-02, which says the builder cannot express explicit superseding notes. D-05 requires an entry-by-entry revision or no-change note **with the reason**. The README’s new instructions still say to give every later entry one by one and that each listed entry becomes a note; they do not add a reasoned-note input or a manual attachment that the builder binds. Integer/range/duplicate validation alone does not supply that missing content.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_rehearsal_c4/run/GAPS_C4V001.md` — SHA256 `566b206635d7ba160ab602842c64e7f1ffd38878c6bf0d7ed3721faffcc3543c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_rehearsal_c4/refute/REFUTE.md` — SHA256 `7be3fb347310040a1fc806b8886c85cb17e631cb9933aed6261cd958499c3eda`

Deciding step: Claude4 supplies an immutable successor that accepts and quotes a pinned, per-entry decision/explanation for every later or changed entry, with missing/duplicate/mismatched entries refused, or Claude2 explicitly disposes of this narrower requirement. The review does not infer such a disposition from the bare CLI argument. Table rows already present in prereg r5 are a separate path and retain their revised-clause/no-change-reason checks.

**D-06 (TESTED bounded orchestration; source/document inspection).** The README now identifies checklist B2a, the exact driver BUILD printer, root’s exclusive creation step and all three B7 JSON schemas. The actual printer’s `record_bytes` was exercised with a synthetic reviewed-module stub: legitimate text and JSON inputs produce sorted/indent-1/newline bytes matching `builtin_r5_build()` plus the check-record byte pin; activation occurs before formatting and again on parsed output. Duplicate keys, a 4,301-digit duplicate fixture, nonfinite constants, invalid encoding and wrong reviewed-source SHA refuse without an output. The stub never executes the real compare or validates actual r5 custody; this demonstrates printer wiring and refusal behavior, not production admission.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/SEAL_CHECKLIST_R5.md` — SHA256 `7ff81720e6cf108a6f71d478dcc23493fb1ee943ed2c90e88873715a2921bd13`

**B7/R-10 (TESTED pure validators).** Empty exact key maps pass. Mismatched maps, duplicate pointers, forbidden pointer namespaces and wrong schemas refuse. NEW-item inputs require the named IMPL to contain the reviewed source hash; adopted items without tests and duplicate IDs refuse. Custody records require the Z2 identity, exact driver hash, positive integer stage totals, equal successor counts and PASS. These are declared input contracts; the correctness of root’s eventual scientific custody evidence is UNTESTED here.

**Validation accounting.** All 45 review assertions passed, including the assertions that demonstrate the two D-05 acceptance gaps. This is not 45 successful closure tests and does not override the FAIL verdict. Zero audit denials; observed RSS 30,998,528 bytes. The test imported only audited helper/T1/T5 definitions; T4 pure validators were compiled from their exact source AST. No complete seal builder, real compare, binder, admission guard, launcher or scientific worker was executed. No actual protected metadata, run, target, root config or seal was read or created.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/entry_driver_review/RESULTS_CX3V001.json` — SHA256 `086bc3d3cfd522d67143790b80f763a81122f2466729743bf66c377f9e2f10bb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/entry_driver_review/review_entry_driver_cx3v001.py` — SHA256 `88e9eb50d6977b70378b1f9c230c7c7402d4acf6b0f9a63939caa4928c67e9ad`

UNTESTED here: the author’s 148-case suite, full real driver admission, full seal construction, B6/B8 behavior, and final program/root disposition. Those belong to the other assigned review lanes or root.
