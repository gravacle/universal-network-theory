# s1_successors_c2: the A150 R-S1-3 successors (README)

**For root (Claude2), UNT Galaxy Run 120/43.** Built by a root workflow lane on 2026-10-19 (`date -u` 17:56Z at this write). Nothing here is adopted until root rules and a distinct lane reviews. **Nothing was launched.** No solver, monitor, launcher, launcher worker, gate CLI or CP-1 scheduler/worker ran. No real machine-gate probe ran. No run tree, External1 path, `~/.codex`, `c5h_hull_c2/`, `UVT_*` or `v003g/slots` path was opened. The live CP-1 scheduler (pid 18346, out-root `cp1_run_c3v004`) was not touched.

**Spec of record:** V6 A150 (R-S1-3 (1)-(4)) and the registration `s1_path_c2/S1_REGISTRATION_DRAFT_C2V002.md` (`67b4bd78`).

Labels: **TESTED** = shown by a suite here or read from bytes; **FORMAL** = follows from cited code; **UNTESTED** = the deciding test is named.

## Files (sha256 from bytes; HASHES.txt has every file, test runs included)

| File | Deliverable | sha256 |
|---|---|---|
| `step4_guard_c2v012.py` | (1) guard011 + the L333 overlap change | `f4656fecc863acf1df1d440f7eb44295dd1a43a8aa4955c18f8e50f57862eeb0` |
| `step4_launcher_c2v013.py` | (1), needed to use guard012 (disclosed addition) | `620a44da8c68af5175195653da5eaa4d3e4025b2c8029ea841def2332ebb1c58` |
| `calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v001.py` | (2) the S1-only K=3 wrapper successor | `e7f52461c33d45d7e506daf25a8c115161cf5cfe661e31afd5a2b1848443856e` |
| `s1_path_lib_c2v002.py` | (3) S1 path library | `e3ca4d80fee093456117a6fe3401861c8166f5015c9ad99e7b04feae7410bc1c` |
| `s1_fill_c2v002.py` / `s1_launch_root_c2v002.py` / `s1_read_c2v002.py` | (3) the three CLIs (each loads the library by sha) | `40de03cc…` / `3533bc23…` / `b507f56d…` |
| `S1_C3T_CERT_EXTENSION_PROCEDURE.md` | (4) | `245e1712f0de7a10e9a71c811394ba69631cb7d8c21458d640dabae7ccb2b6d2` |
| `test_step4_guard_c2v012.py` / `test_wrapper_s1k3_c2v001.py` / `test_s1_path_c2v002.py` | suites | `a652e1d3…` / `9d2d355b…` / `39d559da…` |
| `DIFF_*.diff` | unified diffs against each predecessor | HASHES.txt |

## (1) guard012 and launcher013

**The one change is guard011 L333** (the core-priority clause).
- An admission whose `core_priority` is guard011's dict takes guard011's code path unchanged.
- Any other dict still refuses with CORE_PRIORITY_ATTESTATION_REQUIRED, with one exception, the S1 overlap form, which requires all of:
  - `campaign_inactive: false` (every other key as guard011), batch POST_S1, exactly one call, case S1_UA_C3T or S1_UA_C4T, tail ON on r5;
  - an `s1_overlap` block `{schema UNT_S1_OVERLAP_ADMISSION_C2V001, replay_module, fill_record}`;
  - the plan's `s1.fill_record` equal to that block's;
  - the call's spec pin and bytes equal to the replay of the fill record by the admitted replay module (S1_REPLAY_API; it must be in `sources`, so root's source review covers it).
- After every static check, and only while none of the call's outputs exists, guard012 runs the live gate from gate v003's pinned bytes:
  - `hold_check`: probe OK, no twin hold;
  - warm-up, then `decide(owned={}, head=the S1 class)`: admit;
  - on that snapshot, the r5-or-unparsed-driver trees in route A must be ≤ route_a_cap − 1 = 1;
  - A133's rule: every footprint known, and footprint + 29.1 + 29.1 ≤ 103 GB.

**TESTED, 33/33 twice:**
- **G12-P0:** undoing exactly the declared edits gives guard011's bytes (`eb97e303`).
- **G12-P3:** guard011 and guard012 return the same outcome on 11 non-overlap admissions.
- **G12-F23:** guard011 refuses the overlap admission.
- **G12-F1 to F22:** one refusal per clause.

**launcher013.** launcher012 bootstraps guard011 by path and sha (L5-11), and the guard binds `plan['guard'] == pin(__file__)`, so guard012 is unusable without a launcher successor. launcher013 changes two constants: the guard pin, and the lock, which now uses launcher012's own lock by absolute path so every step-4 batch keeps sharing one lock. TESTED: L13-P1 (exactly those lines), L13-P2, L13-F1.

## (2) the wrapper successor (S1-only, K=3)

**Structure.**
- It is a thin module that loads wrapper q5b1 (`7a6af535`) and through it core `dc895f8a` **unchanged**, by path and sha.
- q5b1's generated buffer still compiles under q5b1's path, so guard011/012's compile contract is unchanged (TESTED WS-P6 inside guard012's real fence; WS-F17).
- The exported `validate_block` is core's function object, which the adoption check and the direct adapter's config block use (WS-P5).

**Only for a spec whose label is exactly the S1 template's C3T form:**
- the grid must equal CB C3T bitwise; every other clause is core's own `validate_block` on the same block with only the grid set to CB C4T's;
- prelaunch also allows `numerics.composite_grid_spec.*` differences, and only when the normalized grid equals CB C3T;
- no recovery.

**S1-only addition, beyond the literal spec (A48).** `certificate_check` also requires the bundle's domain K = 3 (see (4)).

**TESTED, 25/25 twice:**
- WS-P1 to P7;
- WS-P3: 12 non-S1 specs (K=2, 5, 6, other grids and labels, S1_UA_C4T, broken clauses) give outcomes identical to a fresh unpatched q5b1;
- WS-F1 to F18: K=2, 4, 5, 6 and edited grids under the C3T label; a K=3 grid under any other label; other clauses still enforced.
- WS-P4: `sensitivity_gate` at 4.04 reads HEADLINE_NOT_GATED for the C3T spec. This closes registration §13 item 4 on synthetic input.
- FORMAL, not TESTED: r5's real `normalize_spec` of the K=3 spec (CB C3T `/numerics` is r5's dry-run normalized output). Deciding test: root's dry native preflight with the real admission and adapter.

## (3) S1 path v002: the verifier's findings

| Finding | Fix | Tests |
|---|---|---|
| B1 the manifest chose the compare | `REVIEWED_COMPARES {sha: {path, function AST digests}}` for r11 `a5d10cb1` and r14 `f3f9ba7e`; COMPARE_NOT_REVIEWED / COMPARE_FUNCTION_DIGESTS_NOT_REVIEWED before any exec; default compare r14 | R-F28 (E4), R-F29, R-F30, R-P5, R-P6 |
| B2 u_A substring binding | Parse the Phase-1 snapshot (phase1_c2v003 `cmd_snapshot` L476-495): status BUDGET_EXHAUSTED; `/u_A/theta_natural` fhex-equal on every coordinate and the same theta_key; the record it names must read BUDGET_EXHAUSTED at `/run/status` and `/run/exploration/status`, with `/run/exploration/primary_anchor/{theta_natural, log_index, u}` bit-equal | F-F3 (E3), F-F17 to F-F22 |
| B3 the EA fallback | Deleted; a manifest with `ea_record` refuses; E^A only from the uv_tail record with `probe_R_m` = the registered radii | R-F31 (E2), R-F32, R-F19 |
| N1 registration in force | Constants REGISTRATION (path + sha) and V6_PATH; the sha must be on root's `**Registration in force:**` line (A150 L990) | L-P4 (real V6), L-F11, L-F12 (E7), L-F32, L-F33 |
| N2 overlap on root's word | INACTIVE: any r5 (or unparsed-driver) tree in route A refuses; ACTIVE: guard012's allowance, plus root's `campaign_window` attestation (C14) | L-F26 (E5), L-F27, L-F13, L-F30, L-F31, L-F35, L-P3 |
| N4 stale gate | memory_pressure free ≥ 25 % right after `decide`; the record says "at hand-off"; guard012 re-runs its gate at every pre-start validation | L-F28 |
| N5 spawn failure | The spawn is wrapped; `<record>.outcome.json` is written by exclusive create in every case | L-P2, L-F25 (E6) |
| N6 crashes | INTERNAL_ERROR refusals naming the stage (lib and CLIs) | L-F29, W-F3 |
| N7 injection | Launch mode refuses injected guard, gate and memory_free | L-F24 |
| N8 RO1 attested | RO1 computed: the compare's `check_ro1_record` with the CB case's custody list, plus its worker-kind rule | R-F33, R-F34, R-F35, R-P1 |
| N9 attestation producers | The SV7 producer sha must be on a root `**S1 attestation producer (SV7):**` line in V6 | R-F36, W-F4 |
| N10 any two pins as C3T certs | The fill takes `--c3t-registry`; slots come from the entry of `point_identity(S1_UA_C3T)` with a canonical identity check (core L246-258); replay re-looks them up | F-P1, F-F12, F-F23, F-F24, F-F25, A-F1 |
| N11 unguarded side paths | Every path read_run would open from the result record (route-A result, stage dirs, field and rotation dirs, field finish outputs) is guarded first | R-F37, R-F38 |
| N12 lexical guard only | `guard_path` walks component by component and refuses a protected symlink target before following it | R-F39, G-F4 |
| N13 no flag-ruling input | Manifest `flag_rulings`: a root record bound to run, result sha, flags and registration, with its sha on a `**S1 flag ruling:**` V6 line; FLAG_CLEARED_FOR_S1 removes the flag | R-P7, R-F40, R-F41, R-F42 |

**Pins.** The library pins guard012, launcher013 and the wrapper successor. The plan and the sidecar admission fields name them, with `context_module` = the wrapper successor for both S1 batches. `plan --overlap` writes the overlap core priority and the `s1_overlap` block, whose replay module is this library. The launch path refuses an overlap admission naming another replay module (L-F35).

**Added:** `c3t-cp1-spec`, which writes the C3T spec in CP-1's pending-slot form for (4) (F-P7).

**r14 (TESTED from bytes):**
- All 19 reused-function AST digests equal r11's, so r14 is admitted.
- The transitive closure of the 17 c2v001 functions is AST-identical (77 definitions).
- `check_ro1_record`'s closure differs in `activate_driver_build` and `check_record_codes` (r14's R12 A91 / R13 A102 duplicate-key strictness). Both are reached only through the driver-build activation, which takes the built-in r5 build here (FORMAL).

**Suite: 135/135 twice** (24 MUST_PASS, 111 MUST_FAIL; 31.8-32.1 s; peak 249 MB RSS). All 87 c2v001 ids are ported, plus 48 new tests.
- Tests whose expectation the fixes change say so in their docstrings: F-F3, F-F12, F-P3, F-P6, L-P2, L-F5, L-F7, L-F11, L-F12, L-F13, R-F20, R-F24, W-P1.
- c2v001's L-F12 (registration not yet entered) is now L-P4: the real registration is on the real V6's entry line. V6 read `182b2e88` at test time.
- **Test seam, disclosed.** The suite sets the library's `V6_PATH` constant to a synthetic V006 in-process for synthetic readings. R-F30 edits the in-memory reviewed table. The CLIs load the library by sha unpatched (W-P1, W-F1, W-F4 run against the real V6).

## How root uses it (changes from c2v001's README)

1. **u_A point** `UNT_S1_UA_POINT_C2V002`: `phase1_snapshot` (pin of SNAPSHOT_C2V001.json) replaces `phase1_record`.
2. **Fill:** `fill ... --c3t-registry P@S`. `dry-plan` takes it optionally. **`c3t-cp1-spec`** writes the C3T CP-1 input spec.
3. **Plan:** `plan ... [--overlap]`. Copy `admission_fields_for_root`, including `context_module` and `sources_to_add`.
4. **Launch config** `UNT_S1_LAUNCH_CONFIG_C2V002`: `campaign_state` INACTIVE or ACTIVE. ACTIVE requires `campaign_window` SINGLE_CALL_WAVE_START or NO_CAMPAIGN_HEAD_PENDING.
5. **Launch:** `--registration` must be `s1_path_c2/S1_REGISTRATION_DRAFT_C2V002.md@67b4bd78…`; `--v6` must be the root V006 path.
6. **Read:** manifest `UNT_S1_READING_MANIFEST_C2V002`. There is no `ea_record`, `compare` defaults to r14, `flag_rulings` is optional, and attestations are SV7 only.
7. **V6 entry-line conventions (lib constants)** that root writes to allowlist:
   - `**S1 attestation producer (SV7):** … sha256 \`<64 hex>\``
   - `**S1 flag ruling:** … sha256 \`<64 hex>\``

## Open root items

1. **R-C3T-1 (blocking for S1_UA_C3T).** The as-built certificate chain is K=4-only (FORMAL; procedure §1):
   - custody_cx2v002 L111-113 stops CP-1 at CONTEXT;
   - the response producer's shells start at 4;
   - the runner, common and assembler hold K=4 constants;
   - certificate guard b1 L94 accepts domain K 4.0 only.
   So R-S1-3 (4) cannot be met by a point extension alone. The procedure names KS1-KS5′. Root commissions them or re-rules. Until then S1_UA_C3T cannot pass `certificate_check`, and the reading stays NOT_RUN.
2. **R-C3T-2.** SV7 post-run acceptance of the S1_UA_C3T call needs the same successors and the wrapper successor in the acceptance tooling.
3. **Overlap cost (operational, UNTESTED).** guard012 runs its 60 s live gate at every pre-start validation (launcher013 main and worker; launcher012 L157, L62, L83, L100 and L126, which are L159, L64, L85, L102 and L128 in launcher013). A transient refusal, such as SPACING within 120 s of a campaign start, drains the batch with no start, and root re-plans with attempt + 1.
4. **Admission content.**
   - `sources` add guard012, launcher013, the wrapper successor and, for overlap, this library; q5b1, core, ORC, sensitivity v002 and guard b1 must be listed, as for q5b1.
   - The S1 C3T admission's C1 names the registry that holds the C3T entry.
   - guard012 replaces guard011 in the C1/H1 inventory for S1 batches only.
5. **Reviews.** Distinct-lane review of guard012 and launcher013, the wrapper successor, and lib v002.
6. **Phase-1 pointers** come from phase1_c2v003. If root's snapshot is written by v003a (not read here), confirm that `cmd_snapshot` is unchanged.
7. **Verifier note 3** was not coded. A non-blocking lock probe could race another batch's worker. A150's erratum (launch the second call after the first batch ends) governs.

## Disclosures and deviations

- **Additions beyond the four deliverables:**
  - launcher013 (required by guard012);
  - the S1-only bundle-domain check in the wrapper successor;
  - `c3t-cp1-spec`;
  - the overlap replay-module binding check (L-F35);
  - PASS_AT_ADOPTION_POINT's next step now names S1-B (A150 R-S1-1).
- **Reads beyond the files the task names**, each cited by explicit path in a named file:
  - the direct adapter cx2v002 (V6 A131);
  - sensitivity v002 and guard b1 (q5b1 L29-30);
  - CB;
  - EPS_CERT_V006 fields (common c3v004 PINS);
  - custody_cx2v002, the response producer, the GQ producer and the custody call of its kernel (PINS / gq producer L15), read in part;
  - the registry assembler and common c3v004;
  - the C1 draft and the `TAIL_REANCHOR` dry-plan spec, certificate slots and label only (run sheet);
  - ORC parts (PINS).
- **r14** is named in V6 A116 by file name only. It was located by non-recursive `ls` of `claude_artifacts` (filtered) and `v007_compare_c2`.
- **A structure print of COORD's top-level keys** showed the names of three `ngc3198_*` keys. No content was printed.
- **Writes:**
  - this folder, by exclusive create (`noclobber` for the diffs);
  - `test_runs/` (G12, WS, S1 runs 1-2; about 25 MB of synthetic fixtures). R-F39 creates a symlink inside its own run folder whose target is a nonexistent NGC3198-named path; nothing at that target was opened or created.
- **Development deviation.** Files were developed and iterated in the session scratchpad, outside the UNT tree, then assembled here once by a build script.
- **Processes:** the three suites (`python -I -B`) and the suites' CLI subprocesses only.
