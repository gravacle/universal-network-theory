# values_writer_c2v002: the members eps_km_s writer (A148; A144 R3; Claude3 0211 N1)

Root build by Claude2's workflow. Written 2026-10-19T17:16Z (`date -u`). **Nothing here is adopted.** Root must rule W-1 under A115(b), and Claude4 must review. The stop stands.

Labels: **TESTED** (run or read from bytes here), **FORMAL** (follows from code structure; the real bytes are not exercised), **UNTESTED** (with the test that would decide it).

## 0. Basis of v002, and a disclosure

v002 answers review B1 and review B2 of the v001 report.
- **No v001 bytes existed.** At the start of this build, `claude_artifacts/values_writer_c2/` did not exist (`ls`: No such file or directory).
- v002 is therefore built fresh, and nothing was edited.
- The corrections below follow the review text, not a v001 diff.

## 1. W-1: one item for root (a physics-reading choice, A115(b))

**What A148 says.** Each eps_km_s entry "comes from the pinned `field_bound` applied to that certificate and that point's own field".

**Why that is not enough.** `field_bound` (owned_uv_tail_lapse_v002 `2026f2b6`, L847-857) returns lapse bounds in SI units (1, 1/m, 1/m²), not km/s (TESTED from code). The conversion to km/s is `srb_rot` (L860-871). A148 does not name `srb_rot` (TESTED: the string is absent from V006 L934-956). So root must rule, and the writer refuses to attach or run until it does.

**PRIMARY.**
`eps_km_s[q] = srb_rot(S, C, rows)['bound_km_s'][q]`, with every input computed from the point's own outputs:

| Input | What it is | Source |
|---|---|---|
| S | The TailState of the call's own stage `le{final_pass}_rotation` | A134 reading point, V006 L525 |
| C | The point's own certificate, field `eps`, per unit shell | A148 |
| rows | `rotation_rows` (row_reference_producer_c2v003 `67fddd24`, L171-193) on the call's own `rotation_base_arrays.npz`, at the call's own row radii | The V007 SRB_ROT producer rule |

For S, two bindings must hold:
- the state digest equals that stage's own `finish.json` `uv_tail.state_digest`;
- `S.record.eps_certificate` equals the point's EPS pin. This is the check at srb_rot_adapter_c3v003 L434.

The `rows` input reads:
- `column_R_m` = `radial_nodes_m`;
- `v_c_m_s` = R·√(min over z of `rotation_Omega_squared`);
- `N_min` = min(1 + Re `full_fields_complex[...,0]`);
- `row_columns` = the node at the row radius, or else the two nodes either side of it.

This is exactly the call the A146-adopted adapter makes (`08e9ac0a`, L439-440).

**Alternatives.** Each one departs from an adopted rule. None is applied, and all are listed only for root:
- **A-1:** v = `speeds_km_s[q]` instead of v_c taken from `rotation_Omega_squared`.
- **A-2:** the bound evaluated at R_q, instead of the max over the row's columns.
- **A-3:** a declared N_min, instead of the computed minimum lapse.
- **A-4:** multiply by sin(i_phys)/sin(i_released).
  - V007 applied this factor (srb_rot_record L60-61, L106, as cited in the row producer's docstring L54-55). Row producer v003 does not apply it.
  - The NGC `speeds_km_s` are projected by exactly this factor (FORMAL): observation module `8e30897e` L113-114, called by the column-mean adapter `6790e28e` L64-66.
  - So the PRIMARY bounds the unprojected column-speed channel.
  - The writer prints the factor from the call's own column-mean packet and does not apply it. If the factor reads exactly 1.0, the question is moot. Whether it does for NGC is UNTESTED: the binding is NGC3198-named and was not opened.
  - **Root rules A-4 together with W-1.**

## 2. Claims, corrected

1. **TESTED.** `field_bound` is not in km/s, so a km/s eps needs `srb_rot`.
2. **Corrected.** v001 said N_min has no source. That is wrong: N_min is **computed** by `rotation_rows` L183, and v_c at L186 (TESTED).
   - The rule reads the call's own `rotation_base_arrays.npz` (row producer L208-217).
   - A145 adopted it (`67fddd24`).
   - The row producer states that this is the V007 SRB_ROT producer rule (srb_rot_record_cx1v008_cx3v001 L43-63).
3. **Corrected.** v001 said no caller exists. The intended caller does exist: srb_rot_adapter_c3v003 (`08e9ac0a`, adopted in A146) calls `field_bound` at L439 and `srb_rot` at L440 on the pinned v002 library (L53-54). It works on the final-rotation state (L224-241) and requires the state's `eps_certificate` to equal the EPS pin (L434). All TESTED.
   - The adapter's inputs are DDO-specific: EPS schema cx2 with coverage [4,182], the row-contract tau, and the v010 inventory.
   - So the NGC writer reuses the adapter's rule and its library call, not its entry point.
4. **Corrected (B2).** A136 cites `owned_uv_tail_lapse_v003`. That file **exists**, at `tail_scheme_impl_c2/driver_r6/module/owned_uv_tail_lapse_v003.py` (`e733eb1e…`, 1,211 lines; TESTED). Its L962-985 is the certificate hash-check that A136 describes. **It is not the pinned library.**
   - The pinned v002 has the same logic at L664-674. TESTED: v002 L664-688 and v003 L962-986 are byte-identical.
   - `_eps_per_shell`, `field_bound`, `srb_rot` and `monitor_MT` are also byte-identical: v002 L830-885 and v003 L1144-1199 (TESTED).
   - The NGC driver pins v002 (driver L310-311), and the NGC route-B binding `aee7af12` pins it at L42 (TESTED).
   - **Root must not log an erratum saying the file is missing.**
   - Line note (TESTED): the NGC refusal of `nodes_v001` is driver L911-912, inside the nodes branch L907-912. B2's "L909-910" is that branch's `ext_grid` refusal. The conclusion is unchanged.
5. **FORMAL.** The rule carries over to NGC by its structure. The real bytes are UNTESTED.
   - The rotation_v005 stage (`e22e79e8`) saves `full_fields_complex` (L294), `rotation_*` (L295) and the npz (L302).
   - Driver L354 maps `rotation_v005` to `le_rotation`.
   - The driver records `passes[-1].rotation_arrays` (L5940) and `final_pass` (L6062).
6. **TESTED** (pinned library, synthetic): `bound_km_s` does not depend on tau (L866-869).
7. **TESTED** (real certificate bytes, read-only):
   - Each of the 4 S0 EPS records (`efdc430a`, `8270b6b3`, `bfac8f57`, `5dd9900a`) passes with its own key, as 89 unit shells covering [2,91]. Its `eps` is copied exactly.
   - Each one is refused (CERT_OTHER_POINT) for the other 3 keys.
   - The 4 BIND_CHECK records, the SMOKE_ANCHOR record and a RUN_START record are refused (CERT_SCHEMA).
8. **TESTED** (consumer):
   - `check_values`, `members_values` and `band_rows` are AST-identical in phase1_c2v002 (`d64351ec`; L804-816, L912-924, L752-801 with the eps use at L791) and in phase1_c2v003.
   - A written values document passes v003 `check_values`.
   - A members document passes `check_member_eps`.
   - `member_eps` reads a number on valid rows, and MEMBER_EPS_NONE on invalid rows and on a point with no certificate. A144 R3 then flags that pair.

## 3. Builder choices

| # | Choice | Note |
|---|---|---|
| C-1 | **Row radii** are the call's own column-mean `prediction.query_support[].radius_m`, for valid rows. | rotation_rows' `row_columns` must equal that record's `column_indices`, which use the same bisect rule. The DDO producer takes radii from the row contract instead. The NGC equivalent is the target-free query manifest (driver NGC_DATA `a2936517`), which is NGC3198-named and was not opened. |
| C-2 | Rows the call itself marks invalid (`valid: false`, speed null, an N1/A4 reason) get **None**, with that reason. `rotation_rows` runs on valid rows only. | rotation_rows refuses any radius outside [R₀, R₋₁]. The call's valid rows lie inside that range by construction (column-mean `query_partition`). A148's "43 finite" cannot hold where the call has no speed. `band_rows` already reads those rows as NOT_AVAILABLE. |
| C-3 | **tau is an inert 1.0.** `ratio_to_tau` and `pass_tau_over_10` are discarded. | No NGC σ is read. |
| C-4 | The final-rotation stage is found from the driver's own pass record: `passes[-1].rotation`, whose directory must be named `NN_le{final_pass}_rotation`. | Not from a v010 inventory; no NGC inventory exists. |
| C-5 | **Custody** follows A136 G3: the driver sha `577f8c94`, the θ key through the certificate's `point.key`, and the call spec sha that root supplies, which must equal `result.call_spec_sha256`. | The EPS pin must also be equal in three places: the spec, the stage `finish` config and the state record. |
| C-6 | **Any failed check refuses the point**, and no record is written. | Only "no certificate" gives None entries (A148). |
| C-7 | **Query order** = the values document's `query_ids`. It must equal the order of the call's final rows, and nothing is reordered. N_ROWS = 43, the phase1 `n_rows`. | The phase1 tool has no NGC row constants. Its order comes from the values file. |
| C-8 | **The certificate check** requires: schema `UNT_CLAUDE4_S0_POINT_EPS_C4V002` exactly, mode `point`, a role that is not anchor or SMOKE, `key_check`, producer `8972822b`, CERTIFIED (gate, verdict, certificate flag and `rule_verdict`), coverage {NGC: [2,91]}, and contiguous unit shells from 2 to 91. Each shell's `eps` must be at least both recorded `eps_envelope` values. `eps_max` is never read. | A reviewed successor schema or producer needs a writer successor. |
| C-9 | **The gate.** While `ROOT_RULING` is None, `attach_eps` and `main()` refuse. | A successor pins root's ruling. |
| C-10 | `attach_eps` adds `eps_km_s_custody` to each point: the record sha, the certificate pin, the writer pin and the ruling pin. It never overwrites, and it refuses any unused record. | The consumer ignores extra keys (TESTED, T18). |

## 4. Dependencies (UNTESTED; each names its deciding test)

- **D-1. The NGC per-state TailState input.** The record and arrays of `le{final_pass}_rotation` must reproduce `finish.uv_tail.state_digest`. The stage builds this state in memory and saves only its digest (binding `aee7af12` L371-376 and L349-364).
  - This is the same object that NGC per-state LO acceptance needs (A135 item 2; A136 G1-G5). It is not built yet.
  - **Deciding test:** on the first real S0 call, the reconstructed state's digest equals the stage's own digest.
- **D-2. Certificates for every point other than the 4 S0 θ** (u_A, the F points and the Phase-2 members), per A148. **Deciding test:** each one passes C-8.
- **D-3. A driver successor needs a writer successor** (`DRIVER_SHA256`).

## 5. Tests (synthetic only)

- No solver was run, and no real NGC field was computed.
- **Tests:** `test_values_writer_c2v002.py`, run under `python3 -I -B` (codex runtime 3.12.14, numpy 2.3.5). **123/123 passed in each of two record runs** (`test_runs_v002/run1`, `run2`), with identical outcome lists.
- **Coverage of the suite:**
  - the independent oracle matches (relative error 0.0), and the result is bitwise equal to the pinned `srb_rot`;
  - tau independence;
  - the eps_max decoy;
  - shell sensitivity;
  - an empty state;
  - a point with no certificate;
  - 18 synthetic and 22 real certificate refusals or passes;
  - 9 state-binding refusals;
  - 14 call-binding refusals;
  - query order;
  - coverage, which the library also refuses;
  - the row-column cross-check;
  - the attach path against the phase1 consumer;
  - the CLI gate;
  - exclusive create;
  - printing of the inclination factor;
  - 22 byte and line evidence checks for the claims above (T24-T27).
- **Mutation:** `mutation_values_writer_c2v002.py` killed 16 of 16 mutants. They include eps_max broadcast, R_q, a declared N_min, v = speeds, the inclination factor applied, the L434 check skipped, the digest skipped, silent reorder, envelope fed and gate removed.

## 6. Deviations (disclosed)

1. There were no v001 files (section 0).
2. Drafts and development runs were made in the session scratchpad, outside `values_writer_c2/`. The published files were created here by exclusive create, and their shas were verified after each copy. The record runs were written under `test_runs_v002/`.
3. **Real reads, all read-only:**
   - the 4 S0 EPS records and 6 refused records, in the named `out/` folder;
   - source files for code and line evidence: the named files, plus files cited by explicit path inside them. These are the column-mean stage `51ab097c`, the column-mean adapter `6790e28e`, the observation module `8e30897e` and the NGC route-B binding `aee7af12`, a chained citation.
4. **Traversal slip.** One recursive `find | wc -l` ran over this build's own output folder `values_writer_c2/test_runs_v002/`, to size the synthetic fixture trees (5,179 files, 70 MB). It touched only files this build wrote. HASHES_V002 therefore lists the published files and the three results records, not each synthetic fixture file. The fixtures can be regenerated from the test file.
5. **Not opened:**
   - any run tree;
   - any NGC3198-named file other than V006, including the target-free query manifest;
   - `srb_rot_record_cx1v008_cx3v001`, which has no explicit path. Its content is cited only through the row producer's docstring.

## 7. Files

See `HASHES_V002.txt`.
- `values_writer_c2v002.py` `38ac8c93`
- tests `8e66ff31`
- mutation `98818f09`
- results: run1 `f7041245`, run2 `53a99e08`, mutation `a1f44cc6`
