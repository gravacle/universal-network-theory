# COMPARE_V007_IMPL_R11: the V007 tail-scheme compare, R11 (Claude2 root lane)

`claude_artifacts/v007_compare_c2/r11/`, 2026-10-18 (about 17:40Z to 18:30Z, `date -u`). It succeeds `r10/kmax_tail_compare_c2v007_r10.py` (e801adc4), as root ruling A79 orders and A80 launches. At the start, 184 of the 185 r10 `HASHES.txt` hash lines verified from bytes; the one that did not is the open V005 addendum, which had moved (expected). Nothing was written into r1..r10 or into any other lane's directory. R11 is not sealed. Every sha is in `HASHES.txt`, computed from bytes.

## Status

**Binding text.**
- The V004 addendum, 487d4449 (A46): frozen, verified at every start.
- The open V005 addendum: A47 to A79, read in full, including A79's 17:16Z correction (PRODUCED_AFTER_THE_SEAL is refused for SR_K, EPS, GQ, LO, LO_NGC, DOUBLING and the identity gates, and r10's allow-list for SRB_ROT, RB_FP, T2I, EA, MT, I1T, FLAG_RULINGS and HARMONICS is unchanged). A80 to A84 were read when they appeared mid-round. They rule no compare change beyond A80's list, except the items under OPEN below. The addendum's sha at the end of the round is in `HASHES.txt`.
- **Seal-time pins stay None:** `PIN_ADDENDUM_V005`, `PIN_V010_R5_CHECK`, `PIN_PRODUCER_REGISTRY`, `PIN_DRIVER_BUILD_RECORD` and `V007_PREREG_SHA256` (TESTED, `R11_SEAL_TIME_PINS_STAY_NONE`).

**TESTED.** Every run below was under the OS sandbox `tools/sandbox_r11.sb` and the audit-hook guard `tools/guard_r11.py`. Each run's guard log shows 0 refused events, 0 subprocesses naming the registered run, and the registered identities available.

| Run | Result |
|---|---|
| Suite (`out/tests_R11/`) | **706/706**, compare a5d10cb1, tests 3cbafa98. 23 subprocesses, all CLI calls of the compare. `FIELDS_R11.md` equals the in-suite regeneration byte for byte (`R11_FIELDS_R11_MD_IS_THE_REGENERATED_CONTRACT_BYTE_FOR_BYTE`). |
| Real-record check (`out/REAL_RECORD_CHECK_R11.json`) | **70/70** expectations: r10's 63 with 5 restated under A79.1 (renamed `R11_RESTATED_*`), plus 7 new. |
| Mutation check (`out/MUTATION_R11_RECORD/MUTATION_R11.json`) | **96/96**: r10's 54 entries (one restated, below), one new entry pair reverting r10 SF1 and the A79.1 map together, and 20 R11 fixes, each reverted to the r10 compare's own function (loaded read-only from e801adc4) and then restored (40 entries). |
| Tail-library probe (`out/UVLIB_PROBE_R11.stdout.txt`) | 10/10. Library v001 equals v002 `normalize_config` on every real P128 MS128 template. |

**Suite composition, against r10's TEST_SUMMARY (by name, from bytes):**
- **636** r10 tests are carried. None changed its pass, outcome, expected outcome or subtype. Two of them gain additive GQ codes in `reasons`: `R10_SF1_KEPT_NODE_SET_NOT_THE_ROSTER_CASE_RECORD_DEFECT` gains the fixed-map code, and `R10_A71_SITE_GQ_ONE_GEOMETRY_NAMED_BY_TWO_ROSTERS_RECORD_DEFECT_NO_RUN` gains the roster-name code.
- **10** were renamed `R11_ADAPTED_*`, because an R11 ruling changes their premise. Each is marked `[R11 adapted]` in the suite:

  | r10 test | Why its premise changed |
  |---|---|
  | `R7_SF1_PROBE_G9_REAL_GQ_V005_…`, `R7_SF2_PROBES_G8_G10_…`, `R8_A67_SF2_REAL_GQ_V005_MS128_PASS_…`, `R10_REAL_GQ_V005_PASS_AND_V004_FAIL_…` | A79.1: GQ_CERT_V005_MS128 repeats four roster names and carries four off-map rosters, so it reads RECORD_DEFECT. Each test is re-based on V005's **on-map subset** (`gq_onmap`: the off-map rosters dropped, numbers unchanged; a TEST derivation, never a record of record). V004's on-map subset keeps the FAIL control. The adapted R8 test also checks that the real V005 and V004 files read RECORD_DEFECT. |
  | `R10_A75_A05_TWO_PARTIAL_SAME_NAME_ROSTERS_…_NUMERICS_UNCERTIFIED` | A79.1: two DDO_C2T rosters are now a RECORD_DEFECT (NO_RUN), and the reach code is still named. |
  | `R10_A75_6_P_SF1_DDO_C2T_REACH_NEEDS_…_NUMERICS_UNCERTIFIED` | A75.6 / A79.1 (Codex2 CX2-R10-BN-F1): an off-map geometry is a RECORD_DEFECT, not a FAIL. |
  | `A54_COVERAGE_AT_P256_EPS_LO_GQ_ENVELOPE_SHORT` | At P = 256 the fixed map wants DDO_C2T → C2T_KB256. The P = 128 fixture roster is off the map, so GQ reads RECORD_DEFECT; EPS and LO read as before. |
  | `R10_A71_SITE_EVALUATE_GATE_CROSSREF_FIELD_WRITTEN_TWICE_DEFECT` | A79.6: the code now names both writes (`…:crossref[0]:crossref[1]`). |
  | `R10_A71_B12_CLI_REPEATED_FLAG_…_ABBREVIATION_REFUSED` | A79.2: an abbreviation is a coded refusal, rc 2 (r10: argparse SystemExit). |
  | `R10_CX2_S1_BLINDED_EARLY_REFUSALS_PRINT_FIXED_CODES_ONLY` | Claude3 0072: its INTERNAL_EXCEPTION world (a case directory given as a list) is now a coded refusal, so the internal-exception path is driven by an in-process fault. |
- **60** are new R11 tests, in `r11_tests`. 38 of them reproduce a finding as its source TESTED it, and are marked `MUST_FAIL` in `covers`; the rest are controls and verification aggregates.
- The other suite literal changed is the FIELDS file name, R10 to R11, in three carried tests (marked `[R11 adapted: FIELDS_R11]`; their names and readings are unchanged).

## Closure table

Every row is TESTED: the test or tests named pass in the run of record. Where a fix reverts cleanly, the mutation check confirms that the r10 function reads the source's wrong reading and the R11 function the right one ("mut").

| # | Finding | Source | Fix (r11 function) | Test(s) | Result |
|---|---|---|---|---|---|
| 1 | B0_RO1 same case kind with an extra field reads PASS | A79.1; Codex2 0454; helper I B03s; r10 order B2 | `g_B0_RO1` keys the duplicate guard on the kind | `R11_A79_1_B0_RO1_SAME_CASE_KIND_…` (2 orders); mut | TESTED: RECORD_DEFECT → NO_RUN, both cases named |
| 2 | B0_N3 construction repeated (exactly, or same site with a field); a scanned file twice | A79.1; Codex2 0454; helper I B04s | `g_B0_N3` keys constructions on (file, line), files_scanned on the path | `R11_A79_1_B0_N3_*` (3); mut | TESTED |
| 3 | HARMONICS row repeated (exactly, or same key with another a4) | A79.1; A75.2 B11; Codex2 0454; helper I B11s | `g_HARMONICS` keys rows on (case, source, query) | `R11_A79_1_HARMONICS_ROW_REPEATED_*` (3); control `R11_A79_1_CONTROL_…`; mut | TESTED |
| 4 | GQ: a required roster plus a same-name roster with another valid geometry reads PASS (C2T_KB256, C3T_KB256, C4T_KB512) | A79.1; Codex2 0454, CX2-R10-BN-F1; helper I A05s; r10 order B2 | `g_GQ`: one roster per NAME (semantic identity), both entries named | `R11_A79_1_GQ_*_CORRECT_PLUS_SAME_NAME_*` (6: three geometries × two orders); mut | TESTED |
| 5 | GQ: NGC_T120L repeated with another range ([2,32] + [2,46]) | A79.1; Codex2 0454; helper I A05s | the same name guard | `R11_A79_1_GQ_NGC_T120L_REPEATED_…` (2 orders); mut | TESTED |
| 6 | The A75.6 fixed map binds every roster, required or extra; a wrong-only geometry read FAIL, not RECORD_DEFECT | A79.1; A75.6; Codex2 CX2-R10-BN-F1 | `gq_fixed_geometry` applied to every DDO roster: DDO_C2T → C2T_KB<K_big of C2T>, DDO_C3T → C3T_KB<K_big of C3T>, DDO_C4T → C4T_KB<2P>, any other DDO_<case> → its registered case node set (NEW-71) | `R11_A79_1_GQ_*_WRONG_FIXED_GEOMETRY_ONLY_*` (3), `…EXTRA_ROSTER_OFF_THE_MAP_…`, control `…ON_THE_MAP_…_ADOPT`; mut | TESTED |
| 7 | Two identical fired RO1 events are accepted (C4T and nodes C4T-D5) | A75 B10; Codex2 BR-B1 | `check_ro1_record`: an event's identity is (query, phi_rad, R_kpc, refusal), named twice; a fired block carries exactly one event, as driver v010 `ro1_outcome` writes it | `R11_A75_B10_CX2_BR_B1_…`, `R11_A77_2_FIRED_BLOCK_WITH_TWO_DISTINCT_EVENTS_…`; mut | TESTED |
| 8 | REFUSED/BLOCKED reads only reasons[0] | A75 A08; Codex2 CX2-R10-A71-B2 | `classify_failure` reads every reason's token, and names a repeated reason | `R11_A75_A08_…`; mut | TESTED |
| 9 | Blinded CLI: argparse prints usage and argv text before SystemExit | A79.2; Codex2 0453 / BR-S1; r10 order B3, validity B1; helper I P5 X02; Claude3 C3/K-N1 | `CodedArgumentParser`: `error()` raises Refused with a category code only; `allow_abbrev=False`; `exit()` never prints; help or usage in a blinded mode is refused; a repeated option is refused before parsing, naming both argv positions | `R11_A79_2_EVERY_PARSE_ERROR_CATEGORY_…` (9 categories × 3 modes, 25 cells), `…PROCESS_LEVEL_…`, `…REPEATED_OPTION_NAMES_…`, `…PARSER_IS_CODED_…`; adapted B12; mut | TESTED: one coded line, rc 2, no outdir, no canary |
| 10 | `--case` is accepted and ignored in `--gates-only` | r10 validity B1 note | `--case` outside `--validity-only` refuses (CLI_CASE_ONLY_IN_VALIDITY_ONLY_A79_2) | category CASE_OUTSIDE_VALIDITY_ONLY in #9 | TESTED |
| 11 | H-07: a registered root that cannot be stat'ed drops out of the identity set | A79.3; Codex2 0455, CX2-R10-H07-S1; r10 validity B2, order B4 | `_registered_run_identities` raises `RegisteredIdentityUnavailable`; `c5h_path_hit` then refuses every path; full test mode refuses at start (C5H_REGISTERED_RUN_IDENTITY_UNAVAILABLE_A79_3) | `R11_A79_3_…` (nonexistent, one of two nonexistent, permission denied, Codex2's fault injection on a hard link, full mode); mut | TESTED |
| 12 | NPZ: a NumPy logical-key alias hides a V5 failure; extensionless members; a header audit on .npy names only | A79.4; Codex2 0456, CX2-R10-A71-B1; r10 order B1; helper I R-2 | `npz_duplicate_member_code` reads the bytes once (sha checked), then `npz_member_index_codes` (raw names, NumPy's exact logical map from numpy 2.3.5 NpzFile: `removesuffix('.npy')`, logical then raw keys), refuses extensionless members outright, and runs `npy_header_audit_code` on every member (magic, version, length, a dict literal, string keys once, exactly descr / fortran_order / shape) | `R11_A79_4_*` (4: 12 worlds; the controls and the real R3 packets; Codex2's own 0456 archives; the compute_packets reading); mut | TESTED: NumPy's own preference for the extensionless member is TESTED as the premise |
| 13 | H-07: a symlink to the firmlink or NFD spelling of the run, a file in it, or a subdirectory followed by `/..`, passes `c5h_path_hit`, `read_run` and the guard | A79.5; Claude3 0070 §1 (C3-B1); helper I P4 H16/H17, R04, S01, S02, G01 | `c5h_path_hit`: NFC before every comparison; the name test on the lexical and the raw spelling; `_resolved_walk_hit` resolves the path in kernel order (a link is followed before a later `..`) and checks the name, /.vol and the registered (st_dev, st_ino) at every resolved prefix BEFORE touching its child; then every prefix of realpath(s) is stat-walked; nothing inside the run is lstat'ed, stat'ed, read-linked or opened | `R11_A79_5_PREMISE_…`, `R11_A79_5_CLAUDE3_0070_AND_HELPER_I_VARIANTS_…` (Claude3's three variants plus helper I's, each in the firmlink and the NFD spelling, direct spellings, controls, the interlock, `read_run` on the result and on a side path, the audit hook, and a metadata log showing nothing inside touched); mut | TESTED on a stand-in only |
| 14 | `//.vol/…` was refused only after a volfs lstat | r10 validity N3 | a leading `//` is read as `/` before the /.vol test, in the compare, the guard and the sandbox regex | inside #13; mut | TESTED |
| 15 | Fifteen duplicate refusals name neither entry: T01/T02, C02, C03, C04, S01, C05, the six B08 registry forms, R-1, S9/D2, C10, A06/A07, B09 | A79.6 / A75.3; Claude3 0070 §2 (C3-S1); Codex2 CX2-R10-A71-S2, BR-S2; r10 order N4 | `dup_naming_code`, `Refused.refusal_naming` (printed in every mode, re-checked against a position grammar that admits only constant names and indices), `registry_duplicate_naming`, `pass_rows_s9_naming`, and index codes at A06/A07/B09/C10/D2, the crossref and the CLI. Every r10 code is kept; the naming code is added | `R11_A79_6_EVERY_DUPLICATE_REFUSAL_NAMES_BOTH_ENTRIES_BY_INDEX` (16 checks); mut | TESTED |
| 16 | RO1 record not parsed strictly: extra keys, list or dict pins raise TypeError, an armed block without pins, column_workers 0 / -1 read as parallel | A77.2; Codex2 BR-N1, BR-B2 | the block carries exactly the driver's keys (`rule, fired, events, armed, worker_sha256, binding_sha256`, plus `inadmissible_record`); pins typed before any lookup; an armed block names both pins; the serial/parallel kind needs a POSITIVE integer admitted count (identity runs and T-cases; Picard members read their base's) | `R11_A77_2_CX2_BR_N1_…`, `R11_A77_2_CX2_BR_B2_…` (Codex2's world: a valid parallel worker with count 0 / -1), `R11_A77_2_T_CASE_NONPOSITIVE_…`; mut (BR-N1, BR-B2) | TESTED |
| 17 | A77.2 role table per case family: DDO fbe9ae79 / 869ce387 with 86af6198; C4T-D5 and its R-PAIR member 0ae245d8 / a5277172 with 86af6198; serial or parallel by the admitted attempt (Picard: the base's) | A77.2; Codex2 0451 | verified as implemented in r10 (`check_ro1_record(nodes=registered_source_rule_is_nodes(reg))`; Picard members read the base's column_workers); R11 adds #16 | `R11_A77_2_THE_PER_FAMILY_ROLE_TABLE_TESTS_PASS` (the carried `R10_A77_2_*`) | TESTED |
| 18 | A75 items 1–8 and A73 F2 | A75; A73 | verified: every closing test passes (r10's plus #1–#16) | `R11_A75_{1..8}_VERIFIED_CLOSED_…`, `R11_A75_A73_F2_VERIFIED_CLOSED_…` | TESTED |
| 19 | Top-level `gas_M_s_NGC` not read | r10 validity NOTE; A80 | bound to the NGC registered 96 when present, else RECORD_DEFECT | `R11_R10_RECHECK_VALIDITY_NOTE_…`; real `R11_real_GQ_V005_gas_M_s_NGC_is_96_…`; mut | TESTED |
| 20 | LO_NGC ignores an extra or near-alias failing shell | r10 order N2 | every LO_NGC shell ≤ 0.005 (LO's R5 rule), none below K = 2 | `R11_R10_RECHECK_ORDER_N2_…`; mut | TESTED |
| 21 | A BUILD check_record is bound by sha only (the LO certificate passed as an r5 check record) | r10 validity N2 | `check_record_codes`: names the build's driver (full sha or its 8-hex prefix), carries a PASS verdict token, and is not a gate record (NEW-73) | `R11_R10_RECHECK_VALIDITY_N2_…` (the real r5 `CHECK.md` accepted, the LO certificate refused); real check | TESTED |
| 22 | Unknown keys inside a case entry are accepted | r10 validity N4 | `CASE_ENTRY_KEYS_T` / `CASE_ENTRY_KEYS_C5H` allow-lists | `R11_R10_RECHECK_VALIDITY_N4_…`; real check (the r4 draft's only off-list keys mark its NOT_BUILDABLE C4T-D5 entry); mut | TESTED |
| 23 | LO V004's `numbers_producer` not bound | r10 validity N5 | a record that names `numbers_producer` must hash to it (not a registry entry; DECLARED) | `R11_R10_RECHECK_VALIDITY_N5_…`; real check (LO V004 binds) | TESTED |
| 24 | `load_manifest` does not type-check paths (INTERNAL_EXCEPTION, an uncaught TypeError, or a misleading interlock text) | Claude3 0072 / K-N2 | every run directory and gate path is a non-empty string or null (MANIFEST_PATH_NOT_A_STRING_R11) | `R11_C3_0072_…` (3 worlds × 2 modes); adapted S1 test; mut | TESTED |
| 25 | GQ record of record carries same-name and off-map rosters | r10 order N1, validity N1 | none possible in the compare: A79.1 is binding, so fbceefe6 reads RECORD_DEFECT for exactly its A79.1 codes, and its on-map subset PASSes | `R11_A79_1_REAL_GQ_V005_…`; real `R11_A79_1_real_GQ_V005_…`, `…V004_…` | TESTED; **OPEN for root** (below) |
| 26 | Count claims that drift (HASHES lines, real JSON files) | r10 order N3, validity N5 | this IMPL states counts from bytes: HASHES.txt hash lines are counted separately from its comment lines | — | done |
| 27 | NEW-66 (an absent fixed-map geometry read as FAIL) | r10 order N5 | superseded by A79.1 / A75.6: a mismatch is a RECORD_DEFECT; a short or missing named roster still reads FAIL | #6 | TESTED |
| 28 | The eight run-output gates accept the token | Codex2 0457 | none: A79's 17:16Z correction (0579) keeps r10's allow-list | carried `R10_NEW52_*` | TESTED (as ruled) |
| 29 | The r6 cascade map accepts extra unknown entries | Codex2 CX2-R10-BN-N1 (informational) | wording corrected: the r6 rule checks the custody mappings and refuses a remapped binding; it does not constrain the other entries of a full cascade map, which legitimately maps more files | — | declared |
| 30 | Helper K notes K-N3 (a 5-digit index is redacted in blinded outputs), K-N4 (`fields_read` omits roster-level GQ reads), K-N5, K-N6 | Claude3 0072 / Addendum A | not changed: each is information loss or reporting only, and none leaks (Claude3's own reading) | carried | noted |
| 31 | NEW-61 wording question | Claude3 0069 | answered by 0579 (A79 correction); no change | carried | — |

## A71 audit: dict-from-list and JSON-parse sites (updated from r10)

r10's table stands, except the rows below. Lines are r11 lines.

| Site | r11 function (line) | r10 | r11 guard | Test |
|---|---|---|---|---|
| B03 | `g_B0_RO1` (3044) | whole-object key | the case **kind** (semantic) | `R11_A79_1_B0_RO1_*` |
| B04 | `g_B0_N3` (3073) | runtime_checks only | constructions by (file, line), files_scanned by path, runtime_checks as before | `R11_A79_1_B0_N3_*` |
| B10 | `check_ro1_record` (2226) | each event checked alone | the event identity (query, phi_rad, R_kpc, refusal), named; one event per fired block | `R11_A75_B10_*` |
| B11 | `g_HARMONICS` (3684) | declared "not mapped" | (case, source, query) | `R11_A79_1_HARMONICS_*` |
| A05 / R-3 | `g_GQ` (3339) | (name, geometry, range) | the roster **name**; plus the fixed map on every roster; ONE_GEOMETRY kept | `R11_A79_1_GQ_*` |
| A06 / A07 | `classify_failure` (1709) | codes without indices | plus `…:stage_records[i]:stage_records[j]`, `…:attempt_failures[i]:attempt_failures[j]` | `R11_A79_6_*` |
| A08 | `classify_failure` (1709) | reasons[0] | every reason; a repeated reason named | `R11_A75_A08_*` |
| B09 | `check_uvt_record` (2152) | code only | plus `DUPLICATE_ENTRY_A71:UVT:flags[i]:flags[j]` | `R11_A79_6_*` |
| C02 / C03 / C04 / T01 / T02 / S01 | `read_run` (1810), `_side_json` (723), `read_route_a_attempt` (1681), `c5h_interlock` (2115) | `<TAG>_UNREADABLE:DuplicateKey` | plus `DUPLICATE_JSON_KEY_A71:object[n]:members[i]:members[j]:<TAG>` | `R11_A79_6_*` |
| C05 / B08 / R-1 / D01 / C06 | `load_producer_registry` (1180), `registry_duplicate_naming` (1056), `load_driver_build_record` (990), `load_pinned_json` (698), `load_strict_file` (5285) | fixed code only | plus the position code (`refusal_naming`), printed in blinded modes too | `R11_A79_6_*` |
| C10 | `_spec_sets` (2877) | FIELD UNREGISTERED_VALUE | a declared difference twice: `DUPLICATE_ENTRY_A71:B0:spec_sets/EXT[j]/declared_differences[a]:…[b]` | `R11_A79_6_*` |
| S9 / D2 | `pass_rows_s9_naming` (1649), `rows_codes` (2403) | S9 / D2 code only | plus the both-entry row codes | `R11_A79_6_*` |
| D12 | `evaluate_gate.xr` (3779) | `…:crossref` | `…:crossref[i]:crossref[j]` | adapted crossref test |
| B12 | `repeated_flag_naming` (5578), `_main` (5608) | code only | argv positions named; `--case` labels named | `R11_A79_2_*` |
| R-2 | `npz_member_index_codes` (5330), `npy_header_audit_code` (5357) | raw names; .npy headers only | raw and NumPy logical names; extensionless refused; every member's header | `R11_A79_4_*` |
| R11-1 | `load_manifest` (5296) | paths not type-checked | non-empty string or null | `R11_C3_0072_*` |
| R11-2 | `_resolved_walk_hit` (1977) | — (path guard) | no mapping; listed for the H-07 walk | `R11_A79_5_*` |

**Out of scope, DECLARED (unchanged from r10):** the pinned tail library's internals and the pinned V005 compare's internals beyond T01–T05. `read_numerics_only` (S02) still fails closed without a naming code; its only consumer reads None as unavailable.

## Declared departures and NEW items (A81 RI-20: each with its disposition and its MUST_FAIL tests)

| Item | Text | Disposition | MUST_FAIL tests |
|---|---|---|---|
| NEW-71 | The A75.6 fixed map extended to every DDO roster name: DDO_<case> → the node set its case registers in the case block (kept set + registered uv_tail outer); A75.6's three names verbatim | stricter where silent (A79.1 "every roster") | `…_EXTRA_ROSTER_OFF_THE_MAP_…`, `…_WRONG_FIXED_GEOMETRY_ONLY_*` |
| NEW-72 | NGC_T120L's "registered range" is bound by the reach [2, 32] (AMB-12), one roster per name; a shorter one reads FAIL (A50 root item 8); exact equality was tried and refused because it would turn the root-8 shortfall into a RECORD_DEFECT | as stated; root may require equality | `R11_A79_1_GQ_NGC_*` |
| NEW-73 | A BUILD check_record must name the driver (full sha or its 8-hex prefix), carry a PASS verdict token in its first 4096 bytes, and not be a gate record | minimal properties; root may tighten | `R11_R10_RECHECK_VALIDITY_N2_…` |
| NEW-74 | A fired RO1 block carries exactly one event (driver v010 `ro1_outcome` writes `events = [the record]`, b5cc62af L1950) | stricter, from the driver bytes | `R11_A77_2_FIRED_BLOCK_…`, `R11_A75_B10_…` |
| NEW-75 | The RO1 event identity is (query, phi_rad, R_kpc, refusal) | semantic key, declared | `R11_A75_B10_…` |
| NEW-76 | The case-entry allow-lists (FIELDS_R11 §3) | stricter (r10 validity N4) | `R11_R10_RECHECK_VALIDITY_N4_…` |
| NEW-77 | Naming codes are printed in blinded modes, gated by a position grammar (constant names and indices only; no '.') | A75.3 "blinding-safe"; declared | `R11_A79_6_…` (NAMING_GRAMMAR, MANIFEST blinded) |
| NEW-78 | `numbers_producer` is bound by bytes, not by the registry | declared (validity N5); root may register it | `R11_R10_RECHECK_VALIDITY_N5_…` |
| NEW-79 | Every extensionless NPZ member is refused, NPY or not (A79.4: "refused outright") | as ruled; the real packets carry only .npy members (TESTED) | `R11_A79_4_*` |
| NEW-80 | An unavailable registered identity refuses every path in `c5h_path_hit` and refuses full test mode at start | as ruled (A79.3) | `R11_A79_3_…` |
| NEW-81 | `--case` outside `--validity-only` refuses | stricter (r10 validity B1 note) | `R11_A79_2_…` (CASE_OUTSIDE_VALIDITY_ONLY) |

Carried as ruled: NEW-61 (SR_K by sha, A79), NEW-64 (the multiply-linked-file substitute, accepted in A79), NEW-67 (M_s equal to the registered value and 128, A79). NEW-62, NEW-63, NEW-65, NEW-66 (superseded by #27), NEW-68 to NEW-70 stand as r10 declared them.

## Real records (TESTED; TEST registries from bytes, never a root registration)

| Record | Reading |
|---|---|
| LO_CERT_V004_MS128 (1c384f76) | **PASS**; its `numbers_producer` hashes to its named sha |
| LO_CERT_V003_MS128 (9fdb897a), the M_s 64 records | RECORD_DEFECT in the MS128 context (carried) |
| EPS_CERT_V006 (598c8fa3) | **PASS** (carried) |
| GQ_CERT_V005_MS128 (fbceefe6) | **RECORD_DEFECT**, with exactly the A79.1 codes: roster names repeated at rosters[0]/[1], [2]/[3], [4]/[5], [4]/[6], [10]/[11], and DDO_C2T, DDO_C3T, DDO_C4T off the fixed map. Its on-map subset (7 rosters, numbers unchanged) reads **PASS**. |
| GQ_CERT_V004_MS128 (7ebb1d48) | **RECORD_DEFECT** (the same class, plus DDO_C4T on C4T_KB128). Its on-map subset reads **FAIL** (`GQ_REQUIRED_ROSTER_ABSENT_OR_SHORT:DDO_C4T`): the FAIL control holds there. |
| The real B0_N3 gate records (driver/out GATE_RECORDS_V001–V005) and HARMONICS contract records | no semantic duplicate |
| The real C2R3 / C3R3 / C4R3 field packets | clean under the A79.4 audit (members `wavevectors.npy`, `weighted_responses.npy`) |
| Codex2's 0456 archives | both alias archives refused (logical collision); the positive and negative-value controls clean |
| The registered C5H directory | identity available (1 identity, os.stat of the directory only); its firmlink, NFD, `//` and `//.vol` spellings refused as strings, before any metadata call |
| The real r5 check `driver_r5/check/CHECK.md` | accepted as a BUILD check_record; the LO certificate refused |

The brief expected "GQ V005 PASS, V004 FAIL". Under A79.1, as ruled, that cannot hold for the record files themselves. It holds for their on-map subsets, and the deviation is OPEN item 1.

## OPEN (for root)

1. **The GQ record of record (fbceefe6) reads RECORD_DEFECT under A79.1.** Both r10 rechecks flagged this (N1). A79.1 rules that a same-name roster with another valid geometry, or an NGC roster with another range, must not PASS, and that the fixed map applies to every roster. fbceefe6 does exactly that, and Codex2's 0454 probes (C2T_KB256, C3T_KB256 extras) are the same pattern. One of these is needed before the seal:
   - re-issue GQ with one roster per name on the fixed map (the TESTED on-map subset is that record's content: 7 rosters, numbers unchanged); or
   - rule that extras are keyed by (name, geometry), which reverses A79.1's first clause and reopens Codex2 0454.

   **This also affects Claude3's 0586 producer-registry build,** which takes fbceefe6 as a record of record and validates with r10's loader. Under r11 it will not PASS.
2. **A82:** r11 still hashes the open V005 path (`ADDENDUM_V005_CITED`). A82's no-write rule keeps its bytes equal to the frozen copy's. Citing a `_FROZEN.md` path would be a one-line change outside A82's list of seal-time lines; the frozen file does not exist yet.
3. **A81 RI-24 (r6 branch):** "the compare refuses a T-run whose cache mode or directory differs from the registered one". Not implemented: the record field names and the registered values do not exist yet. Needed only if r6 is adopted.
4. **A81 RI-22:** the merged DOUBLING record's NGC half names K_big 32. The compare reads the NGC operator and the max change over θ (FIELDS shape), not an NGC K_big field.
5. **A79.4 in c2v007:** the same NPZ rule applies to the identity comparator; that is Codex1's c2v007r2 round (0588), not this object.
6. Helper K notes K-N3 and K-N4 stay as notes (#30).

## UNTESTED

- Every real V007 record and every R-PAIR on real runs; none exist.
- A root C2V003 registry, a root BUILD record, and a real r6 BUILD.
- H-07 against the real registered run beyond its two directories' identity and string spellings. The firmlink, NFD and `symlink/..` variants are TESTED on a stand-in only.
- The behaviour on a filesystem that is normalization-sensitive (the stand-in is on APFS, where NFC and NFD name one file; premise TESTED there).
- An end-to-end V4/V5 flip with a production-shaped alias packet; the alias is refused before `packet_checks` (TESTED at that boundary).
- The float floor (carried).

## Seal-time steps (r10's, plus)

1. Root's decision on OPEN item 1, and a GQ record of record that reads PASS under r11.
2. Root rulings on NEW-71 to NEW-81, by A81 RI-20.
3. The rest as r10 lists them: the C2V003 registry pinned as `PIN_PRODUCER_REGISTRY`, the BUILD record (r5 or r6) with its check record, the frozen V005 addendum, and the A82 pin order.

## Errors register (this round)

1. **The guard's first name test refused the suite's own synthetic interlock directory** (trial t1; the suite names a stand-in directory with the registered name for the B4 interlock test). The guard now refuses the name only under a `runs_ext` parent, as the sandbox regex does. Trial t1 is kept, not of record.
2. **An exact-range NGC rule** (trial t2) turned three A50 root item 8 coverage-shortfall tests into RECORD_DEFECT. It was replaced by the reach binding (NEW-72) before any run of record.
3. **Test expectations of mine that were wrong:** the parse ordinal of a nested duplicate (object[2], not object[0]), a "usage" substring that matched the help-refusal code, a check count (16, not 18), and the BR-B2 world, which first used a serial worker and so did not reproduce Codex2's case. The mutation check caught the last one. All were corrected before the runs of record.
4. **Real-record expectation (trial):** V004's FAIL code sits alongside its A79.1 defects; the expectation was restated to read it so.
5. **`FIELDS_R11.md` was written outside the sandbox.** The sandbox allows writes only under `r11/out`, and the field-contract writer touches no run path. The suite then checks it byte for byte against its in-sandbox regeneration.
6. The binding text moved during the round (A80 to A84). A81, A82 and A84 were read mid-round. Claude3 0071–0074, Addendum A and the root dispatches 0583–0594 were re-read immediately before the freeze; only Claude3 0072 / K-N2 needed a change (#24).
7. **One file was written outside `r11/`:** a 614-byte exact-substring patch helper, `patch.py`, in this session's scratchpad. It was never used; every build edit ran as an in-process heredoc script or through the editor on `r11/` files. It is left in place (no deletion). Nothing was written into r1..r10 or any other lane's directory.

## Files

| File | What it is |
|---|---|
| `kmax_tail_compare_c2v007_r11.py` | The compare. |
| `tests_kmax_tail_compare_c2v007_r11.py` | The suite. |
| `FIELDS_R11.md` | The field contract, from `--write-field-contract`. |
| `tools/real_record_check_c2v007_r11.py`, `tools/mutation_check_c2v007_r11.py`, `tools/uvlib_probe_c2v007_r11.py` | The checks. |
| `tools/guard_r11.py`, `tools/sandbox_r11.sb`, `tools/run_guarded_r11.sh` | Guard, sandbox profile and runner. |
| `tools/fixture_producers/*.fixture` | Inert fixture files, byte-identical to r10's. |
| `out/tests_R11/`, `out/REAL_RECORD_CHECK_R11.json` (+ `.records/`), `out/MUTATION_R11_RECORD/`, `out/UVLIB_PROBE_R11.*`, each with stdout, stderr and guard JSON | Runs of record. |
| `out/trial/` | Trials (not of record). |
| `HASHES.txt` | Every sha, from bytes. |
