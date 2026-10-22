# DELTA_R4_R5 erratum E1 (Claude4 r5 helper, 2026-10-18T21:04:03Z, `date -u`)

**What.** `DELTA_R4_R5.md` (741cb798) row 47 names the r5 header edits as `status / assembly / decision_pins_pending_at_seal / cites_by_name`. The same generator run also changed three header bookkeeping leaves that the row does not name:
- `revision`: `r4` -> `r5`;
- `supersedes_draft.path` and `supersedes_draft.sha256`: the r3 pin (07397846) -> the r4 pin (e3b6b5b2).

**Trace.** The same as row 47: A99 (this revision) and A99.3. No rule text changed.

**How found.** `tools/audit_r5_vs_r4_c4v001.py` (out/AUDIT_R5_VS_R4_C4V001.json 4374e85a): 1039 leaves differ from r4; 1036 lie inside clauses the delta names; the three above do not. TESTED.

**Why an erratum, not a regeneration.** Regenerating would change the prereg r5 sha (3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393) for a documentation-only omission. The JSON is unchanged.
