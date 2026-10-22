# Adapter V001 → V002: response to the distinct helper review (0345-A)

The review of V001 (adapter f2df4d49…, contract 886cb3cc…) was by CLAUDE2 helper 0345-A-review. Verdict: HOLD, with 1 BLOCKING item, 8 SHOULD-FIX items and 9 NOTEs. V001 and its contract, harness and receipt are preserved unchanged. V002 makes no science change.

| Item | Finding | V002 change | Test |
|---|---|---|---|
| B1 | S1 table-level fields passed through verbatim, without pointers | `need()` for each key; identity checks (`whole_covariance is None`, `raw_to_native_map is None`, `source_selected is False`, `physical_prediction_released is False`); table sha checked as 64 hex; each emitted as {value, pointer} | s1_table_level_nested_payload, …_covariance_payload, …_key_absent, s1_table_sha_format |
| S1 | Hard-coded "x1.36" in a kind label | Label now refers to `/settings/helium_factor` (PROGRAM-DECLARED, correction C5); no numeric factor in the label | T1 helium label |
| S2 | Unbounded verbatim copies of crosswalk/correction text | Type bound: only strings, string-keyed objects and lists (correction `now` also allows booleans); numbers rejected. Claim narrowed: these are pinned Claude-authored METADATA, labelled so; the sentinel guarantee covers the observational inputs | crosswalk_numeric_payload, correction_now_numeric, T1b metadata verbatim |
| S3 | Duplicate JSON keys; NaN/Infinity tokens | `object_pairs_hook` rejects duplicates (E_JSON_DUPLICATE_KEY); `parse_constant` rejects NaN/Infinity (E_JSON_NONFINITE_TOKEN) | duplicate_json_key, nan_token, infinity_token |
| S4 | `0 == False` accepted for conversion flags | `is False` identity checks | s1_flag_int_zero_not_false, s1_flag_float_zero_not_false |
| S5 | `re.match` + `$`; non-ASCII digits | ASCII `fullmatch` everywhere | query_radius_trailing_newline, …_fullwidth_digits, query_id_trailing_newline, s1_radius_trailing_newline, s1_note3_err_trailing_newline |
| S6 | `error_kind` not cross-checked; "measurement error" overclaim | Fail-closed rule: (error literal "1" on HI/stars) iff P53 interpretation UPPER_LIMIT_NOTE3; unknown interpretations rejected; neutral label PUBLISHED_PER_RING_RMS_FIELD; OPEN-8 states the measurement-vs-scatter meaning is open | s1_err1_without_note3_interp, s1_note3_interp_without_err1, s1_unknown_interp |
| S7 | No failure-code table; provenance overclaim | Contract V002 lists every static code and prefix family. Every observational value now carries a pointer (S1 row conventions, original_line_number, table level, width_arcsec and subpixels_per_axis read from source). Adapter-added values are labelled adapter_label / derived_count. File and sha are stated once per block | T1 exhaustive round-trip (every value) |
| S8 | Test gaps | Exact code equality; all six pins tested; exhaustive provenance round-trip; existing output byte-identical; previously untested codes now covered | 79/79 |
| N1 | H2 rows 0–9 check fitted to the data | Removed; OPEN-4 now carries the computed present/missing row indices | T1 missing H2 / OPEN-4 |
| N2 | Ledger refs unbound; OPEN-10 text incomplete | Ledger pinned as an input; refs are item indices checked in range; OPEN-10 text names C1–C6 | ledger_ref_out_of_range, R ledger refs |
| N3 | Lenient pointer parsing; source-level pointer misfiled | Pointers must start with "/", with no empty segment and no "~"; source-level corrections are filed separately; `corrects.file` name and `unchanged` checked | correction_pointer_syntax, T2 source-level, correction_binding_file, correction_not_unchanged |
| N4 | width_arcsec was an adapter constant | Read from the source, checked as finite and equal, emitted with pointer | s2_width_value |
| N5 | Non-atomic write | Exclusive temp file, fsync, hard-link to the output name (fails if it exists), temp removed | T1 no temp file; every failure case checks no leftover temp |
| N6 | missing_footprint_fraction_raw excluded without a reason | Included, labelled raw unclipped quadrature, not a noise model; negative values preserved | T1 negative values |
| N7 | Usage line | `python3 -I -B` | — |
| N8 | S1 H2 allowlist broader than the crosswalk | Recorded in contract `addition_vs_0341` | — |
| N9 | Harness deleted a `work/` dir beside itself | Harness writes to a fresh temp dir or argv[1]; no rmtree | — |

Real-data compatibility (types and literals only; no adapter run on real inputs):
- In the P53 table, the only error literal "1" is stars row 2, with interpretation UPPER_LIMIT_NOTE3. No HI row has "1". The S6 rule therefore matches the pinned table.
- The table-level values are None/False/None/False, as V002 requires.
- In PLANAR_SOURCE_RESULTS.json, missing_footprint_fraction_raw is all floats with some negative values, so it is never-null and passes through signed.
