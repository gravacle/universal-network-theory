"""Lane generator for RUNBOOK_EXEC_C3V002.md (successor of C3V001 after Codex2 0580 F-STOP-1) (Claude3; root 0850 item 2, V006 A290/A292).
It copies command lines verbatim from the pinned sources, applies only the documented transformations
(A274 item 1 QoS drop; re-derivation of a source line in a later block; PASTE slots), and emits the
cross-reference table and XREF_C3V001.json. It writes by exclusive create. It runs nothing else."""
import hashlib, json, subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
SRC = {
 'S': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_sheet_cx1/VERDICT_DAY_COMMAND_SHEET_CX1V001.md',
       'f2a5eec4f00a36a6982833a5611e9fe4d4e008ca3736caef4fa30b2aff80242c'),
 'J': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_sheet_addendum_cx3/S0_J_ADDENDUM_CX3V001.md',
       'd6bdd5fe8563bfd378ad6cd083d5bfc719f67b5c6c018796f5cee0a2d6251320'),
 'M': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0276_2026-10-21_0836-built-DBP-C2V004C-HEADLINE11-wall-to-phase2-ceiling-data-only-sheet-amendment-review-request.md',
       '314ef346d6911725c0cb636cd3a7f6b5077af2ead889cad75d169c16a571f0a1'),
 'V': ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/VERDICT_DAY_VARS_C2V001.sh',
       '49607ea4a8660f296516e610718bb26db303ad19c6c517a9f409ba11be56eff5'),
}
LINES = {}
for k, (p, h) in SRC.items():
    raw = open(p, 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == h, k
    LINES[k] = raw.decode('utf-8').split('\n')

def L(k, n):
    return LINES[k][n - 1]

QOS = ('/usr/sbin/taskpolicy -b /usr/bin/nice -n 10 ', '/usr/sbin/taskpolicy -b ')
def qos_drop(line):
    for p in QOS:
        if line.startswith(p):
            rest = line[len(p):]
            assert rest.startswith('"$PY"'), line
            return rest
    raise AssertionError('no QoS prefix: ' + line)

# code items: (text, kind, ref)
def V(k, a, b=None):
    return [(L(k, n), 'VERBATIM', '%s:L%d' % (k, n)) for n in range(a, (b or a) + 1)]
def R(k, a, b=None):
    return [(L(k, n), 'REDERIVED', '%s:L%d' % (k, n)) for n in range(a, (b or a) + 1)]
def Q(k, n):
    return [(qos_drop(L(k, n)), 'QOS_DROPPED', '%s:L%d minus its taskpolicy/nice prefix (A274 item 1)' % (k, n))]
def P(name, what, ref, export=False):
    pre = 'export ' if export else ''
    return [('%s%s=   # PASTE: %s' % (pre, name, what), 'PASTE', ref),
            (': "${%s:?PASTE %s}"' % (name, name), 'PASTE_GUARD', 'J:L53 guard form')]
def F(text, ref):
    return [(text, 'FIXED', ref)]
def D(text, ref):
    return [(text, 'DERIVED', ref)]
def C(text):
    return [(text, 'COMMENT', '')]

P0 = (R('J', 12)
      + F('source "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/VERDICT_DAY_VARS_C2V001.sh"',
        'V:L1 ("Source this at the S4T R3 receipt: `source <this file>`")')
      + V('S', 16, 25) + V('S', 28, 29))
PJ = (V('J', 12, 27)
      + D('[ -d "$S0_STAGE" ]', 'D1: replaces J:L28 mkdir (A276 pre-created it; J:L27 check form)')
      + D('[ -d "$S0_STAGE/fills" ]', 'D1: replaces J:L29 mkdir (A276)')
      + D('[ -d "$S0_STAGE/driver_plans" ]', 'D1: replaces J:L29 mkdir (A276)')
      + V('J', 30))
SHA_FN = R('J', 24)
STRICT = R('J', 12)

BLOCKS = []
def block(bid, title, code, prose_before='', prose_after=''):
    BLOCKS.append({'id': bid, 'title': title, 'code': code, 'before': prose_before.strip(), 'after': prose_after.strip()})

# ---------------- Gates chain ----------------
block('B1', 'S4T R3 receipt check (sheet §1)',
      P('S4T_R3_RECEIPT', 'receipt path from the registered R3 launch record, not R2; outdir ends KMAX_V007_P128_S4T_MS128_CX1_RUN_V011_CX3V001_R3', 'S:L36')
      + V('S', 39, 48),
      '**Root only** (S:L34). **Wait for:** root\'s watch reporting the S4T R3 monitor exit (A292). **Call:** P0 + this block.',
      '**Expected:** exit 0; prints `receipt_sha256` and the eleven fields. Root compares command, pins, caps and the result reference with the R3 launch publication: driver b5cc62af…, spec 8e71be9b…, wall 792000, RSS 137438953472, output 103079215104. Do not dereference the result in this step (S:L51).\n\n'
      '**STOP:** any non-success pauses the verdict path for root classification; no retry and no scientific invalidation is inferred (S:L51). A FINISHED receipt whose driver_status is COMPLETED_INVALID fails the assert: it is a model outcome that root classifies under A245, never an infrastructure retry (A261 N4).')

block('B2', 'Cases manifest and result manifest (sheet §2) — ROOT ACTION, no command in the sources', [],
      '**Root writes, by exclusive create** (S:L55, L57):\n'
      '- `CASES` from the registered cases-manifest schema. `cases.S4T` names R3; all other case paths and bindings stay registered. The comparator resolves the sealed case block itself.\n'
      '- `RESULT_MANIFEST`: an object whose `runs` maps each exact T label to `{path, sha256}` of its `result.json`. Never use a cases directory map as the pinned-result manifest.\n'
      '- Exact base labels: C2T, C3T, C4T, C6T, S4T, C4T-D5, C4T-C5c, C4T-KLO, C4T-KHI, C4T-A.\n'
      '- FLAG_RULINGS also needs a byte pin `root_rulings` to root\'s explicit request (FLAG_RULINGS_REQUEST_SCHEMA_V001.json).\n'
      '- Root hashes actual result bytes only when authorized to produce the gates. Publish both manifest hashes.\n\n'
      '**Expected:** complete exact labels, unique run paths, S4T R3. **STOP:** an absent, aliased, stale-R2 or mismatched input (S:L57).\n\n'
      '**Order note:** if the cases manifest must bind the §3 gate records (S:L72), write `CASES` after B3c, before B4.')

block('B3a', 'Per-label EA replay and HARMONICS (sheet §3; parallel P1)',
      P('UNT_ROOT_ADMISSION_SHA256', 'from the independent root publication; producer_guard_cx1v008 has no path override', 'S:L32', export=True)
      + P('CASE_RUN', 'the registered run of this case (R3 for S4T)', 'S:L61')
      + P('CASE_LABEL', 'one exact base label from B2', 'S:L61')
      + Q('S', 64) + Q('S', 65),
      '**Root only** (S:L59). **Call once per case selected by the gate contract** (S:L61). The calls run at the same time, together with B3b (A263 P1).',
      '**Expected:** exit 0 and new stamped records `$PS/EA_<label>.json` and `$PS/HARMONICS_<label>.json` (S:L72). HARMONICS uses the ra10 checkpoint readout with route_a_tail_replay v005 for tail-ON. It reports saved-state harmonics, not a convergence acceptance. Bind each returned HARMONICS record as the sealed manifest contract requires; do not fabricate a combined record (S:L72).\n\n'
      '**STOP:** any missing gate, partial record, producer refusal or unresolved root flag stops comparison (S:L74).')

block('B3b', 'MT, I1T and FLAG_RULINGS (sheet §3; parallel with B3a)',
      P('UNT_ROOT_ADMISSION_SHA256', 'as in B3a', 'S:L32', export=True)
      + P('RESULT_MANIFEST', 'the B2 result manifest path', 'S:L55')
      + Q('S', 67) + Q('S', 68) + Q('S', 69),
      '',
      '**Expected:** exit 0; new `$PS/MT.json`, `$PS/I1T.json`, `$PS/FLAG_RULINGS.json`. I1T exports actual runtime checks, not a new replay. FLAG_RULINGS exports root decisions and creates none (S:L72).\n\n'
      '**STOP:** as B3a (S:L74).')

block('B3c', 'EA aggregate (sheet §3; after every B3a EA record)',
      P('UNT_ROOT_ADMISSION_SHA256', 'as in B3a', 'S:L32', export=True)
      + P('EA_COMPONENT_MANIFEST', 'label → component-byte-pin manifest (not `runs`), including the registered C5H component; that component is solely root\'s existing blinded procedure', 'S:L72')
      + Q('S', 66),
      '',
      '**Expected:** exit 0; new `$PS/EA.json` (S:L72).\n\n'
      '**STOP:** as B3a. The five gate families do not replace the sealed manifest\'s full registry: preserve every other required identity/SR/T2I/shell record. A88\'s SR_K timing is a prior obligation; never redo it after T outputs are read (S:L74).')

block('B4', 'Sealed compare r14 (sheet §4)',
      P('UNT_ROOT_ADMISSION_SHA256', 'as in B3a (only the §3 producers are known to read it; harmless if the comparator does not)', 'S:L32', export=True)
      + P('CASES', 'the B2 cases manifest path', 'S:L55')
      + P('VERDICT_DIR', 'a new, unused folder for the comparison report', 'S:L13 (all new paths must be unused)')
      + Q('S', 79) + V('S', 80, 81)
      + D('printf \'VERDICT %s %s\\n\' "$VERDICT_SHA" "$VERDICT"', 'D2: display for publication (S:L84 "publish verdict path and byte SHA"); printf form of J:L63'),
      '**Wait for:** B3a, B3b and B3c complete with no STOP.',
      '**Expected:** a new report; exit code alone never authorizes adoption. Use the full decision: no test, validity-only, gates-only or no-packets override (S:L84). Root checks: schema UNT_KMAX_TAIL_COMPARISON_C2V007_R11, script_sha256 a99105a1…, prereg.sha256 b2989012…, pins_verified.V005_addendum c01b3c51…, decision.outcome ADOPT_TAIL, decision.tests_read true, test_mode false (S:L84).\n\n'
      '**STOP:** if any of these differs (S:L84).\n\n'
      '**Then:** publish the verdict path and byte SHA (S:L84). Branch H (B5, B6) and Branch S (B7S1) start now (A263 P2, P3; A274 item 3).')

# ---------------- Branch H ----------------
block('B5a', 'r11 policy, dry run (sheet §5; parallel P2 with B6)',
      P('VERDICT_DIR', 'the B4 folder', 'S:L79') + R('S', 80, 81) + V('S', 89) + Q('S', 90),
      '**Pre-conditions:** `$C4/final` exists (A261 N1; V:L4). V005 (`c01b3c51`) is not edited before §5 (A261 N5).',
      '**Expected:** dry exit 0 (S:L95). **STOP:** any refusal; a changed method, changed base pins or a tuple mismatch (S:L109).')

block('B5b', 'r11 policy, write (sheet §5; only after B5a succeeded)',
      P('VERDICT_DIR', 'the B4 folder', 'S:L79') + R('S', 80, 81) + R('S', 89) + Q('S', 92),
      '"Only after dry success" (S:L91).',
      '**Expected:** an exclusive policy write, not the test `build_f1` output (S:L95). **STOP:** any refusal; then do not run B5c (S:L109).')

block('B5c', 'r11 policy, copy and byte check (sheet §5; only after B5b succeeded)',
      V('S', 98, 106),
      '**Pre-conditions:** the destination parent `$CX2/v006r11_c4` exists (A272 hard stop 1; V:L5) and the destination file is absent; `cp -n` may silently skip (S:L109).',
      '**Expected:** the CHECK asserts the bytes of SRC and DST are equal and prints the policy digest (S:L105). **Publish it as `R11_POLICY_SHA`** (S:L109).\n\n'
      '**STOP:** a byte mismatch, a changed method, base pins or tuple (S:L109).')

block('B5R', '§5 gating review — ROOT ACTION (A263 W1, A268; 0829 as corrected by 0830)', [],
      'Root posts a numbered FROM_CODEX review request carrying the actual `--write` output shas (0829 §5, with 0830\'s restored flag). Codex3 checks them against its pre-review: the r10 baseline with only line 13 (the registration comment) and line 16 (the tuple) changed, which reconstructs r10 exactly (`93d9c0ac`). It uses `check_verdict_gates_cx3v003.py` `78358dac` (45 control checks); the checker hashes the root-named report, reads only the seven authorized fields, refuses any reading other than sealed ADOPT_TAIL and requires exact bytes (A268; Codex3 0683). Codex1 is the fallback gating reviewer (0829); Codex1\'s second look is nongating (S:L109; A208). Target answer about 15 minutes (0829). Root checks FROM_CODEX3 (and FROM_CODEX1) for the PASS: root\'s lane-outbox watch is stopped (A292).\n\n'
      '**STOP:** Branch H waits for this PASS (A263 W1). Branch S does not (A274 item 3).')

block('B6', 'H3 r12 fill and build (sheet §6; parallel P2 with B5)',
      P('VERDICT_DIR', 'the B4 folder', 'S:L79') + R('S', 80)
      + P('VERDICT_RULING', 'root\'s ruling argument for the fill', 'S:L114')
      + V('S', 114, 117),
      '**Pre-condition:** `$R/chain` exists (A272 hard stop 2; V:L7). Do not run `mkdir "$R/chain"`.',
      '**Expected:** exit 0, `chain/v006r12_c4` and `REGENERATE_RECORD_v006r12_c4.json`; exit 2 refuses (S:L120). Diff against `h3_campaign_path_c2/placeholder_chain_c2v004/v006r12_c4`, not an older placeholder or wrapper (S:L120). Root follows the README publication `cp -n` and byte-equality checks for policy, core and wrapper; the entry stays at its generated path as registered (S:L120). Those README commands are outside 0850\'s source list and are not reproduced here (gap G2); publication may be checked after the gating review (Codex3 0684).\n\n'
      '**STOP:** exit 2 or any other refusal.')

block('B6R', '§6 gating review — ROOT ACTION (A263 W1, A268)', [],
      '**Wait for:** B6 and B5c (the request carries the r11 policy, S:L120). Root posts a fresh numbered FROM_CODEX review request with: the verdict path and hash, the seven allowed verdict fields (0770), the r11 policy, the seal tuple record, the four r12 files, the regenerate record and the byte hashes (S:L120). Codex3 (gating) checks only the permitted bytes: policy L13 and L16, core L202 (the policy sha), wrapper L29 (the core sha) and entry L61 (the wrapper sha); everything else must be byte-identical, compared on complete expected bytes (A268; Codex3 0684). Codex1\'s second lens is nongating (S:L120); Codex1 is the gating fallback if Codex3 is unavailable (0829). Root checks FROM_CODEX3 (and FROM_CODEX1) for the PASS (A292).\n\n'
      '**STOP:** Branch H waits for this PASS (A263 W1).')

block('B8a', 'H1 config (sheet §8; after both B5R and B6R PASS)',
      P('H1_PREDECESSOR', 'root\'s H1 predecessor from the frozen C1 tail_readiness and the adopted r11 bindings', 'S:L136')
      + C('# H1_DELTA and H1_CONFIG are set by VARS (V:L12-13); root writes the delta file before this call (S:L136)')
      + R('S', 115, 116) + V('S', 139, 140),
      '**Wait for:** B5R and B6R PASS (A263 P2: §8 needs both). **Root action first:** write `$H1_DELTA` (S:L136). Use only C1.tail_readiness, not C1\'s other top-level keys (S:L136).',
      '**Expected:** apply exit 0 and a verified verdict/prereg association (S:L144). **STOP:** exit 3 (undecided or refused) or 5 (write failure) stops binding, including any partial folder (S:L144).')

block('B8b', 'FINAL specs (sheet §8; after B8a succeeded)',
      P('STEP4_SEAL', 'root\'s registered step-4 seal path', 'S:L141; S:L27')
      + P('STEP4_SEAL_SHA', 'its byte sha256', 'S:L141; S:L27')
      + P('R11_POLICY_SHA', 'the digest printed by B5b', 'S:L105, L109')
      + P('FINAL_SPECS_DIR', 'a new, unused output folder', 'S:L141; S:L13')
      + F("HEADLINE_CASES='TAIL_REANCHOR,WORKERS_8_CANDIDATE_ANCHOR,HEADLINE_TRIAL,HEADLINE_CORNER_000,HEADLINE_CORNER_001,HEADLINE_CORNER_010,HEADLINE_CORNER_011,HEADLINE_CORNER_100,HEADLINE_CORNER_101,HEADLINE_CORNER_110,HEADLINE_CORNER_111'",
          'S:L144 (the comma-separated string given there)')
      + R('S', 99)
      + D('H1_CONFIG_SHA=$(shasum -a 256 "$H1_CONFIG" | cut -c1-64)', 'D3: S:L144 "Compute H1_CONFIG_SHA from the newly written bytes before the producer call"; form of S:L81')
      + V('S', 141),
      '',
      '**Expected:** producer exit 0 and complete FINAL output and manifest (S:L144). FINAL mode reads the registry only from C1 tail_readiness; passing `--registry` would refuse (S:L144).\n\n'
      '**STOP:** exit 3 or 5 stops binding, including any partial folder. Compare the final `binder_pins` with all nine table-D values below; never bind provisional or test specs. The frozen registry and C1 pins stay unchanged (S:L144).\n\n'
      '**0778 table D — expected FINAL binder pins (copied from S:L188-L198):**\n\n'
      + '\n'.join(L('S', n) for n in range(188, 199)))

block('B7H', 'Driver dry plan for each HEADLINE11 FINAL spec (sheet §7; after B8b, before B9 — A261 N3; parallel P4)',
      STRICT + SHA_FN
      + P('DRIVER', 'the call\'s registered driver path (DDO r5 b5cc62af… or NGC r008 577f8c94…, per the annex and the call)', 'S:L132')
      + P('DRIVER_SHA', 'its full sha256', 'S:L132')
      + P('FILLED_SPEC', 'one FINAL spec from B8b', 'S:L126')
      + P('FILLED_SPEC_SHA', 'its sha256 from bytes', 'S:L132')
      + P('NEW_DRY_REPORT_DIR', 'a new path; the driver creates its report folder', 'S:L126; J:L44')
      + R('J', 90)
      + D('[ "$(sha "$FILLED_SPEC")" = "$FILLED_SPEC_SHA" ]', 'D4: S:L132 "Hash driver and filled spec before it"; form of J:L91')
      + Q('S', 129),
      '**Call once per FINAL spec**; the calls can run at the same time (A263 P4). Order: §8 → these dry plans → §9 (A261 N3).',
      '**Expected:** root reads the blocker lists, requires RI45-13 success, and pins the spec and the dry report. No scientific stage may execute (S:L132).\n\n'
      '**STOP:** any blocker or stale spec; no success is inferred from the exit code alone (S:L132).')

block('B9a', 'PRELAUNCH emission (sheet §9–10)',
      V('M', 34, 35)
      + P('ADMISSION_CANDIDATE', 'the admission candidate path', 'S:L151')
      + P('ADMISSION_CANDIDATE_SHA', 'its sha256', 'S:L151')
      + P('GUARD011_CANDIDATE', 'the guard011 candidate plan (emission only, A218)', 'S:L151; S:L11')
      + P('GUARD011_CANDIDATE_SHA', 'its sha256', 'S:L151')
      + C('# PRELAUNCH_OUT is set by VARS (V:L11): new and empty; use a fresh folder for any re-emission')
      + V('S', 151),
      '**Wait for:** every B7H dry plan accepted.',
      '**Expected:** PRELAUNCH records. The candidate names guard011 with a null prelaunch (S:L155).\n\n'
      '**Root action before B9b (S:L155; 0276 item 2; A291):**\n'
      '- Write `GUARD014_FINAL_PLAN`: it names guard014 and launcher015, with the actual PRELAUNCH pins.\n'
      '- Write `FINAL_ADMISSION_CANDIDATE`: its `sources` equal the source review\'s `approved_sources` exactly. Retain guard011 and add guard014/launcher015, the native imports, the C1 producers and the adopted r11 policy (C1_ROOT_STEPS §5 + A218). No missing transitive dependency may be waived.\n'
      '- **Caps (A291):** copy `batches.HEADLINE.caps_per_case[case]` from DBP C2V004C (`$DBP_C` in B9b), **not** from C2V004B, into each GUARD014_FINAL_PLAN call\'s `wall_cap_s`, `rss_cap_bytes` and `output_cap_bytes`, and into FINAL_ADMISSION_CANDIDATE\'s `caps[case]`. `route_a_admission` and `case_order` are byte-identical between C2V004B and C2V004C (0276 item 2).\n\n'
      '**STOP:** any PRELAUNCH refusal.')

block('B9b', 'Bind, then the caps check (sheet §9–10; 0276 items 2–3; A291)',
      R('M', 34, 35)
      + P('GUARD014_FINAL_PLAN', 'the root-written final plan', 'S:L152')
      + P('FINAL_ADMISSION_CANDIDATE', 'the root-written final admission candidate', 'S:L152')
      + P('BOUND_PLAN', 'a new path under $PACKET', 'S:L152; V:L14')
      + P('BOUND_ADMISSION', 'a new path under $PACKET', 'S:L152; V:L14')
      + P('BOUND_COMMAND', 'a new path under $PACKET', 'S:L152; V:L14')
      + V('S', 152) + V('M', 45),
      '',
      '**Expected:** successful binder validation (S:L155). The check (`check_headline_caps_c3v001.py` sha256 `4efb810b`, 0276 L47) prints `HEADLINE caps == DBP C2V004C for 11 calls; wall_cap_s 3443340` (0276 item 3).\n\n'
      '**STOP:** any binder refusal; any check failure (0276 item 3; A291).')

block('B10H', 'Integrity envelope START, phase HEADLINE11 (sheet §9–10)',
      STRICT
      + F('PHASE=HEADLINE11', 'S:L157 (each phase separately)') + F('E="$E_H11"', 'V:L10')
      + [('PHASE_SOURCE_ARGS=(   # PASTE: --doc-pin SHA PATH entries for the final run configs, plans, admission records and registered inputs, including the C1 pin with --scope "$C1" /tail_readiness and the registry pin', 'PASTE', 'S:L167'),
         (')', 'FIXED', 'S:L167')]
      + D('[ "${#PHASE_SOURCE_ARGS[@]}" -gt 0 ]', 'D5: S:L167 "an empty array is not a phase envelope"')
      + V('S', 160, 164),
      '**Wait for:** B9b passed. V006 must already hold every registration the phase needs, because collect reads it (S:L162).',
      '**Expected:** both commands exit 0 (S:L167). **STOP:** exit 3 INVALIDATE stops the phase. Preserve this same pinset for END; never re-collect. No chmod, hard link or GUI mutation of any input during the phase (S:L167).')

block('B10LH', 'HEADLINE11 launch — ROOT ACTION (sheet §9–10)', [],
      '**Pre-conditions:** B10H passed; root\'s alert-only CPU/stage-mtime stall watch is running (S:L9).\n\n'
      'Root independently publishes `UNT_STEP4_ADMISSION_PATH`/`SHA256`, verifies the generated command (`$BOUND_COMMAND`) and launches **that** command after START. Its executor is launcher015 `PLAN --execute-root-only`. Do not bypass the generated single-thread/nice/taskpolicy/lock environment; it is the launcher\'s own, not a §3–§8 command, so the A274 QoS drop does not touch it (S:L169).\n\n'
      '**Expected:** the launcher detaches, so return 0 is not completion. Monitor the child receipts and root\'s non-content stall watch. HEADLINE11 max_active counts route-A only (A247) (S:L169).\n\n'
      '**STOP:** any refusal. Every retry needs a new root ruling (S:L169); cap or infrastructure reruns wait for the adopted single launcher (A275, A282). No P112 launch on verdict day.')

# ---------------- Branch S ----------------
block('B7S1', 'S0 handoffs, all four (addendum §2; sheet §7)',
      PJ
      + [('ROOT_FIELDS=   # PASTE: root\'s actual §7 root-fields path (schema PHASE1_POINT_HANDOFF_ROOT_FIELDS_C2V001)', 'PASTE', 'J:L50')]
      + V('J', 53)
      + [('ROOT_FIELDS_SHA=   # PASTE: its byte sha256', 'PASTE', 'J:L50')]
      + V('J', 54) + V('J', 55, 65),
      '**Wait for:** B4 (S0 needs §1–§4; A274 item 3). **Call:** P0 + this block (it includes the addendum preamble PJ). Branch S runs alongside Branch H (A263 P3).',
      '**Expected:** the tool emits all four handoffs (seed and J0–J2) once into `$S0_STAGE/handoffs`, and the three printf lines print the exact HANDOFF_PIN lines (J:L50, L63-L65). If the seed branch already produced the four registered handoffs, reuse those exact paths; never recreate them or duplicate V006 pin lines (J:L50).\n\n'
      '**Root action:** register the three expanded HANDOFF_PIN lines, plus HANDOFF_PIN S0_SEED (the seed handoff emitted by the same tool), WATCH_PIN MEMORY_WATCH and the V007 adoption pin to the verdict report (S:L124), under a real `## A<number>` V006 entry, **before filling** (RI45-09; J:L68). Use the exact whole-line grammar: no backticks, indentation, `sha256=`, `path=`, trailing spaces or shell variables (J:L68-L74). Check the point_key mapping J0 `3d778566…`, J1 `ab7bf953…`, J2 `4b9b4ec8…` against the S0 source (J:L76). Paths are canonical and avoid ngc3198, runs_ext and /tmp spellings (J:L76; S:L124).\n\n'
      '**STOP:** any refusal; no invented verdict digest or pending certificate is acceptable (J:L50).')

block('B7S2', 'J fills and J driver dry plans (addendum §3)',
      PJ + R('J', 57, 62) + V('J', 81, 98) + V('J', 106, 108),
      '**Wait for:** B7S1 registrations recorded.',
      '**Expected:** three fills and three dry reports. These are sheet §7\'s driver dry-run interface with the A263/A274 QoS waiver (J:L101). Root checks the dry-plan blockers and the actual reports, not the exit code: zero executed scientific stages, no binding or source-build blocker, and only the allowed future `PENDING_ROUTE_A_OUTPUTS` dependency. Pin the reports from their bytes (J:L101). The fills include a twin per point; only J serial specs launch (J:L101).\n\n'
      '**Root action:** after successful dry plans, register the three printed SPEC_PIN lines in the same final registration pass, before START and M-15 (J:L103, L111). Later kit fills must reproduce each registered serial SHA exactly (J:L111).\n\n'
      '**STOP:** any blocker; with `set -e` the block stops at the first failing command.')

block('B7S3', 'Seed kit DRY (sheet §11, dry form)',
      PJ + P('STEP2_LAST_RECEIPT', 'the actual last step-2 receipt (see gap G3)', 'S:L176; J:L130')
      + V('S', 176),
      '**Wait for:** B7S1 registrations. Default is DRY, no launch (S:L180).',
      '**Expected:** a dry plan and fill under a unique `dry/S0_SEED_SERIAL_A1_<UTC>_<pid>` (J:L46 pattern). Root pins the seed\'s fresh filled serial spec and the seed twin spec, runs **B7X** for each, then registers SPEC_PIN S0_SEED_SERIAL and the twin spec in the same final registration pass as J\'s SPEC_PINs (S:L124; J:L103). The seed\'s fill comes from this kit DRY (gap G1). With no seed SPEC_PIN registered yet, the kit\'s fill-check reports `spec_pin_status` PENDING_V006_SPEC_PIN and still passes in DRY (kit L486-541: `spec_pin_present` is true in dry), so no flag is expected here.\n\n'
      '**STOP:** any refusal or flag; exit 5 or a parse timeout means reconcile under the kit\'s rules (S:L180).')

block('B7X', 'Driver dry plan for the seed serial and seed twin specs (sheet §7)',
      STRICT + SHA_FN
      + R('J', 22, 23)
      + P('PIN_NAME', 'S0_SEED_SERIAL for the serial spec, or S0_SEED_CW8_TWIN for the twin (kit L357)', 'S:L124')
      + P('FILLED_SPEC', 'the seed serial spec, or the seed twin spec', 'S:L126')
      + P('FILLED_SPEC_SHA', 'its sha256 from bytes', 'S:L132')
      + P('NEW_DRY_REPORT_DIR', 'a new path', 'S:L126')
      + R('J', 90)
      + D('[ "$(sha "$FILLED_SPEC")" = "$FILLED_SPEC_SHA" ]', 'D4 (as in B7H)')
      + Q('S', 129)
      + D("printf 'SPEC_PIN %s %s %s\\n' \"$PIN_NAME\" \"$FILLED_SPEC_SHA\" \"$FILLED_SPEC\"", 'D7: J:L106 printf form; pin names from kit L357 (S0_%s_SERIAL, S0_SEED_CW8_TWIN)'),
      '**Call once per spec** (seed serial, seed twin); the calls can run at the same time (A263 P4).',
      '**Expected and STOP:** as B7H (S:L132). The last line prints the exact SPEC_PIN line; root registers it in the same final pass as J\'s SPEC_PINs (S:L124; J:L103).')

block('B7S4', 'J kit DRY and twin DRY (addendum §4; sheet §11 dry form)',
      PJ + P('STEP2_LAST_RECEIPT', 'as in B7S3', 'S:L177')
      + P('SEED_DRY_FILL_DIR', 'the seed DRY fill folder from B7S3', 'S:L177')
      + R('S', 176) + V('J', 116, 118) + V('S', 177),
      '**Wait for:** every SPEC_PIN registered (B7S2, B7S3 and B7X). The first line re-runs the seed DRY (S:L176) after the final registration pass, so the registered seed spec is checked before START: its fill-check must now read MATCHES_V006 (kit L543). `SEED_DRY_FILL_DIR` must be canonical and ngc3198-free, with no /tmp or runs_ext symlink spelling (S:L124).',
      '**Expected:** no `--launch` means DRY. A J DRY before seed M-15 reports the record pending, which is allowed only in DRY. Each must pass the handoff, fill and dry-verdict checks, show the same registered SPEC SHA, zero science stages and the planned caps and paths. Save and hash each resulting plan, fill-check and dry-verdict file from each J DRY\'s printed DRY_WORK location (J:L121). The seed and twin DRY outputs are whatever their own commands report.\n\n'
      '**STOP:** any refusal or flag.')

block('B10S', 'Integrity envelope START, phase S0_SEED (sheet §9–10; addendum §4)',
      PJ + R('J', 57, 62) + R('J', 84, 89)
      + F('PHASE=S0_SEED', 'S:L157; J:L123') + F('E="$E_S0"', 'V:L9; J:L123')
      + P('SEED_HANDOFF', 'the seed handoff among the four B7S1 emitted (registered HANDOFF_PIN S0_SEED)', 'S:L124; J:L50')
      + P('SEED_HANDOFF_SHA', 'its registered sha256', 'S:L124')
      + P('SEED_SPEC', 'the registered seed serial spec (SPEC_PIN S0_SEED_SERIAL)', 'S:L124')
      + P('SEED_SPEC_SHA', 'its registered sha256', 'S:L124')
      + P('TWIN_SPEC', 'the registered seed twin spec (SPEC_PIN S0_SEED_CW8_TWIN; kit L357)', 'S:L124')
      + P('TWIN_SPEC_SHA', 'its registered sha256', 'S:L124')
      + [('EXTRA_DOC_PINS=(   # PASTE: --doc-pin SHA PATH entries for the actual verdict binding, final metadata/plans/admissions, referenced inputs and the dry-report/plan pins; add a scoped C1/registry pin only if the S0 config carries tail_readiness', 'PASTE', 'J:L123; S:L167'),
         (')', 'FIXED', 'J:L123'),
         ('PHASE_SOURCE_ARGS=(', 'FIXED', 'S:L167'),
         ('  --doc-pin 5e688882451824931f964e610cf17597d82ee0eb246fb0dce528ec0c6e148042 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/GATE_DOCUMENT_PINS_V002.json', 'FIXED', 'S:L167 (gate document and its sha); path from the envelope README L91 (that README is pinned in S\'s annex)'),
         ('  --doc-pin "$J0_HANDOFF_SHA" "$J0_HANDOFF" --doc-pin "$J0_SPEC_SHA" "$J0_SPEC"', 'DERIVED', 'D6: J:L123 form with n=0'),
         ('  --doc-pin "$J1_HANDOFF_SHA" "$J1_HANDOFF" --doc-pin "$J1_SPEC_SHA" "$J1_SPEC"', 'DERIVED', 'D6: J:L123 form with n=1'),
         ('  --doc-pin "$J2_HANDOFF_SHA" "$J2_HANDOFF" --doc-pin "$J2_SPEC_SHA" "$J2_SPEC"', 'DERIVED', 'D6: J:L123 form with n=2'),
         ('  --doc-pin "$SEED_HANDOFF_SHA" "$SEED_HANDOFF" --doc-pin "$SEED_SPEC_SHA" "$SEED_SPEC" --doc-pin "$TWIN_SPEC_SHA" "$TWIN_SPEC"', 'DERIVED', 'D6: the same form for the seed and the seed twin (S:L124; J:L123 "all four final handoffs/serial specs, seed-twin spec")'),
         ('  "${EXTRA_DOC_PINS[@]}"', 'DERIVED', 'D6'),
         (')', 'FIXED', 'S:L167')]
      + D('[ "${#EXTRA_DOC_PINS[@]}" -gt 0 ]', 'D5: S:L167 "an empty array is not a phase envelope"; under PJ set -e')
      + V('S', 160, 164),
      '**Wait for:** B7S2, B7S3, B7X and B7S4 complete; all S0 registrations recorded. S0 does not wait for B5R/B6R or Branch H (A274 item 3).',
      '**Expected and STOP:** as B10H (S:L167). Root keeps V006 byte-frozen from M-15 through the first launch receipt (J:L5).')

for i, (who, line_no) in enumerate([('seed', 131), ('J0', 132), ('J1', 133), ('J2', 134), ('twin', 135)], 1):
    block('B11.%d' % i, 'S0 first-attempt launch: %s (addendum §5) — ROOT ONLY' % who,
          PJ + P('STEP2_LAST_RECEIPT', 'the actual last step-2 receipt', 'J:L130') + V('J', 130) + V('J', line_no),
          ('**Pre-conditions (J:L127):** step 2\'s last receipt exists; every gate and START passed; the registered passive watch is installed; current disk checks pass; root\'s alert-only stall watch is running (S:L9). '
           + ('Run this line only if the seed has not already launched through sheet §11; otherwise resume after its confirmed LAUNCH (J:L138). This call writes the M-15 record itself (kit `s0_prelaunch_record_c2v001.py` `a10965b7`; kit L23, L96-112) and then waits up to about 300 s for the launch receipt to parse (kit L37), so run it with timeout 600000 or in the background. **V006 freeze:** no V006 append by either branch from the start of this call until its confirmed launch record (J:L5; kit L34). ' if who == 'seed' else '')
           + ('The twin runs only after the seed\'s confirmed LAUNCH (A166; S:L180) and, per 0838, after J0–J2. It uses the seed\'s registered live fill, so no `--dry-fill-dir` (J:L138). Keep its iteration-1 planned-stop watch (J:L138). ' if who == 'twin' else '')
           + '**One call per invocation;** the next waits for this one\'s confirmed LAUNCH record.'),
          '**Expected:** exit 0 with a confirmed LAUNCH record (run directory, receipt and launch-record paths as J:L140 lists). Exit 3 is a refusal; exit 4 is a flag for root review; exit 5 or a timeout requires reconciliation under the kit\'s stop rules (J:L127). A launch return is not completion; do not wait for scientific completion before the next confirmed launch (J:L127).\n\n'
          '**Caps:** J first attempts keep wall 610324 s, RSS 137438953472 B and output 146028888064 B; the External1 free-space guard stays at 156 GiB per start (J:L138). S0 first attempts keep serial 610324 and twin 22752 (S:L8); A291 superseded only HEADLINE11\'s A248 exception.\n\n'
          '**STOP:** any exit other than 0, or no confirmed LAUNCH record. Exit 5 or a parse timeout means reconcile or stop the qualified child under root\'s rule; never assume it died. Any cap, signal or root stop is nonphysics; never record a completed twin without explicit bound planned-stop evidence (S:L180). No automatic rerun; reruns wait for the adopted single launcher (A275, A282; J:L142). If the S0 twin is cut before iteration 1, root reruns it after H11, planned and uncounted (A271 item 2).')

# ---------------- render ----------------
utc = subprocess.check_output(['/bin/date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], text=True).strip()
md, xref = [], []
pastes = {}
for b in BLOCKS:
    for t, kind, ref in b['code']:
        if kind == 'PASTE' and '=' in t.split('#')[0]:
            name = t.split('=')[0].replace('export ', '').strip()
            what = t.split('# PASTE: ', 1)[1]
            e = pastes.setdefault(name, {'blocks': [], 'whats': {}, 'ref': ref})
            if b['id'] not in e['blocks']:
                e['blocks'].append(b['id'])
            e['whats'].setdefault(what, []).append(b['id'])

def emit(s=''):
    md.extend(s.split('\n'))

emit('# RUNBOOK_EXEC_C3V002 — consolidated verdict-day executable runbook')
emit('')
emit('Claude3, for Claude2 (root). Root 0850 item 2 (V006 A290); executed by root under A292 ("lean, one block per call"). Generated %s (`date -u`) by `build_runbook_c3v001.py`, which copies every command line verbatim from the sources below and records each line\'s source in §X. This runbook authorizes nothing: every scientific launch stays root\'s (sheet L3, L184).' % utc)
emit('')
emit('## 0. How to use it')
emit('')
emit('### 0.1 Sources (sha256 from bytes) — the only sources of commands')
emit('')
for k, label in (('S', 'the verdict-day sheet'), ('J', 'the S0 J0–J2 addendum (A276)'), ('M', 'Claude3 0276, the DBP C2V004C sheet amendment (adopted A291)'), ('V', 'the verdict-day variable template (A272)')):
    emit('- **%s** = %s: `%s` `%s`' % (k, label, SRC[k][0], SRC[k][1]))
emit('- **Rulings applied** (V006, read by heading): A261 (N1–N5), A263 (P1–P4, W1–W3), A268 (the pre-staged §5/§6 gating reviews: Codex3 0683/0684, checker `check_verdict_gates_cx3v003.py` `78358dac`; root 0829 and erratum 0830), A271, A272, A274, A275, A276, A291 (C2V004C adopted).')
emit('')
emit('### 0.2 Execution model')
emit('')
emit('- **Fail-fast (C3V002, Codex2 0580 F-STOP-1).** P0 starts with `set -euo pipefail` (J:L12). The first failing command stops the whole call, and no later command can mask it. Any non-zero exit is a STOP, including the kit\'s exit 4 flag: review it before continuing.')
emit('- **One block per call.** Each call is P0 followed by one block\'s code, pasted together into one `/bin/bash` invocation (S:L13). Shell variables do not persist between calls. A block re-derives what it needs from files with the same source lines (kind REDERIVED in §X), or takes a PASTE value.')
emit('- **PASTE slots.** A line `NAME=   # PASTE: …` is followed by the guard `: "${NAME:?PASTE NAME}"` (the guard form of J:L53). Root types the actual value after `=` before running; an empty slot stops the call. Values come from actual artifacts, never from historical hashes (S:L124).')
emit('- **Bash timeouts.** Run every call with `timeout: 600000`, or in the background (`run_in_background`) when it may take longer. B3a, B3c, B4, B8b and the kit DRYs have untested durations, and each B11 launch may wait up to about 300 s for its launch receipt (kit L37, L230). A call killed by the tool\'s default 120 s timeout leaves partial exclusive-create outputs; those need new paths and a root ruling (S:L32).')
emit('- **Paste and invocation hygiene.** Replace a slot\'s whole right-hand side as `NAME=\'value\'`, deleting the `# PASTE` comment. Quote values with spaces (paths under CTRL; `VERDICT_RULING`). Use absolute paths. Write each call (P0 + block) to a file and run it with `/bin/bash FILE`: the blocks contain heredocs and single quotes.')
emit('- **STOP** means: halt the dependent chain, preserve partial outputs, and choose new paths after root\'s ruling (S:L32). Retries need a new root ruling (S:L169). An exit code alone never authorizes the next step (S:L84, L132, L180).')
emit('- **Working directory** persists between calls, but shell state does not. B5a and B5b run `cd "$C4"` (S:L89); every other command uses absolute paths.')
emit('- **Branch S blocks** include PJ, the addendum\'s preamble with `set -euo pipefail` and `set -o noclobber` (J:L12-L13), so the first failing command stops the call.')
emit('')
emit('### 0.3 Rulings that change the sheet')
emit('')
emit('1. **QoS (A274 item 1, the final form of A263/A258).** No `taskpolicy -b` and no `nice -n 10` on any §3–§8 command; the exception list is empty. Lines changed this way are kind QOS_DROPPED in §X. The launcher\'s own generated environment (B10LH) is not a §3–§8 command and is never bypassed (S:L169).')
emit('2. **HEADLINE11 caps (A291; 0276).** First attempts use DBP C2V004C `ce9cbef8` (wall 3,443,340 s). The sheet\'s L8 "HEADLINE11 first attempts retain DBP wall100800" is superseded. The caps check after bind (B9b) is a STOP gate. The optional exact refill (0276 item 4) is not part of this flow.')
emit('3. **Reruns (A275, A282).** No P112 launch on verdict day. Any cap or infrastructure rerun waits for the adopted single launcher (cw8 v003, A282) and its builder. The sheet\'s "cap reruns use reviewed P112 cx2v004" (L8) and its "subsequent retries need reviewed P112 cx2v004" (L180) do not apply.')
emit('4. **Order inside Branch H (A261 N3).** §8 FINAL specs → each HEADLINE11 spec\'s driver dry plan → §9. S0 dry plans stay with S0.')
emit('5. **S0 independence (A274 item 3; A263 W2; J:L5).** S0 needs B1–B4, its own registrations, dry plans and START. It does not wait for B5R/B6R or Branch H.')
emit('6. **Folders (A272, A261 N1, A276; V).** Already created and never re-created: `$C4/final`, `$CX2/v006r11_c4`, `$R/chain`, `$PS`, `$E_S0`, `$E_H11`, `$PRELAUNCH_OUT`, `$STEP4_OUTPUT_ROOT`, `$S0_LAUNCH_ROOT`, `$S0_STAGE` with `fills/` and `driver_plans/`. Left absent for their tools: `$R/H11_EVIDENCE`, `$S0_RUN_ROOT`, `$S0_STAGE/handoffs`, `$S0_STAGE/fills/J0-J2`, `$S0_STAGE/driver_plans/J0-J2`. **So the addendum\'s two `mkdir` lines (J:L28-L29) are not run;** they would fail on the existing folders under `set -e`. PJ checks the folders exist instead (D1).')
emit('7. **Model outcomes (A261 N4).** A FINISHED receipt with driver_status COMPLETED_INVALID is a model outcome under A245, never an infrastructure retry. **V005 (A261 N5)** is not edited before §5.')
emit('8. **Gating reviews (A263 W1; A268).** §5 and §6 are Codex3 checker runs against its pre-review, with Codex1 as fallback. Root posts the requests (B5R, B6R); Branch H waits for both PASSes.')
emit('9. **V006 write freeze (J:L5; kit L23, L34).** The seed\'s `--launch` (B11.1) writes the M-15 record and refuses if V006 changed since it. From the start of B11.1 until the seed\'s confirmed launch record, neither branch appends to V006. Schedule Branch H\'s V006 writes (for example the HEADLINE11 registrations and admission publication) before B11.1 or after that record.')
emit('')
emit('### 0.4 Parallel map (A263 P1–P4)')
emit('')
emit('```text')
emit('B1 → B2 → [ B3a (one call per label) ∥ B3b ] → B3c → B4')
emit('B4 ─┬─ Branch H: [ B5a → B5b → B5c → B5R ] ∥ [ B6 → (and B5c) → B6R ] → B8a → B8b → B7H (per spec, ∥) → B9a → B9b → B10H → B10LH')
emit('    └─ Branch S: B7S1 → B7S2 (∥ with B7S3 → B7X per spec) → B7S4 → B10S → B11.1 seed → B11.2 J0 → B11.3 J1 → B11.4 J2 → B11.5 twin')
emit('    V006: no append by either branch from the start of B11.1 until the seed\'s confirmed launch record (J:L5; kit L34)')
emit('```')
emit('')
emit('- **P1:** B3a for every selected label, and B3b, run at once; only B3c waits for the EA components.')
emit('- **P2:** B5 and B6 run at once; B8 needs both gating PASSes.')
emit('- **P3:** Branch S runs alongside Branch H once B4 is done. S0 launches also wait for step 2\'s last receipt (S:L180; J:L127).')
emit('- **P4:** the per-spec dry plans (B7H; B7X; the J dry plans in B7S2) are independent.')
emit('')

emit('## 0.5 PASTE register — every value root supplies at run time')
emit('')
emit('| Name | Blocks | What | Source |')
emit('|---|---|---|---|')
for name, v in pastes.items():
    whats = v['whats']
    text = list(whats)[0] if len(whats) == 1 else '; '.join('%s: %s' % (', '.join(bs), w) for w, bs in whats.items())
    emit('| `%s` | %s | %s | %s |' % (name, ', '.join(v['blocks']), text.replace('|', '/'), v['ref']))
emit('| `UNT_STEP4_ADMISSION_PATH` / `UNT_STEP4_ADMISSION_SHA256` | B10LH | root\'s independent publication of the bound admission | S:L169 |')
emit('')
emit('## 0.6 Derived lines and gaps (flagged for the narrow check)')
emit('')
emit('- **D1** (PJ): three `[ -d … ]` checks replace J:L28-L29 `mkdir`, because A276 pre-created those folders (one check per line, so `set -e` stops on any).')
emit('- **D2** (B4): a `printf` of the verdict path and sha, so root can publish them (S:L84); printf form of J:L63.')
emit('- **D3** (B8b): `H1_CONFIG_SHA` from the written bytes, as S:L144 instructs; form of S:L81.')
emit('- **D4** (B7H, B7X): the spec hash check before each dry plan, as S:L132 instructs; form of J:L91.')
emit('- **D5** (B10H, B10S): a non-empty check on `PHASE_SOURCE_ARGS` (S:L167).')
emit('- **D6** (B10S): the J `--doc-pin` pairs in J:L123\'s exact form, the same form for the seed and twin, and the root-supplied extra pins.')
emit('- **D7** (B7X): a `printf` of the SPEC_PIN line, in J:L106\'s form, with the kit\'s pin names (kit L357).')
emit('- **G1:** the seed\'s fill comes from the kit\'s seed DRY (B7S3, S:L176); the sources give no separate filler command for the seed.')
emit('- **G2:** the §6 README publication `cp -n` steps (S:L120) are outside 0850\'s source list and are not reproduced. Publication may be checked after the gating review (Codex3 0684).')
emit('- **G3:** S:L176\'s seed DRY passes `--step2-receipt`, while the J DRY lines (J:L116-L118) do not. This is likely moot: B4 consumes every step-2 result, so step 2\'s last receipt exists before Branch S starts.')
emit('- **G5:** HANDOFF_PIN S0_SEED: the seed handoff is one of the four files B7S1 emits, but the sources name only the J files. Root identifies the seed\'s file and composes the line in J:L63\'s form.')
emit('- **G6:** WATCH_PIN MEMORY_WATCH and the V007 adoption pin: their syntax is the kit\'s parsed V006 contract (S:L124), not reproduced here.')
emit('- **G7:** the twin\'s SPEC_PIN name is S0_SEED_CW8_TWIN (kit L357). B7X prints both seed lines.')
emit('- **G4:** the gating checker\'s command line is not in the sources; Codex3 runs it, and root posts the requests (B5R, B6R).')
emit('')
# P0
emit('## 0.7 Changes from C3V001 (`553a0e2c`)')
emit('')
emit('- **F-STOP-1 (Codex2 0580, blocking): fixed.** P0 now starts with `set -euo pipefail` (J:L12). In C3V001, B9b\'s caps check could return 0 after a binder refusal, and B4 could hide a comparator failure.')
emit('- **SHOULD_FIX:** B7S4\'s DRY_WORK sentence now covers the J DRYs only, and the PASTE register gives each block\'s own description for `FILLED_SPEC` and the other shared names.')
emit('- Nothing else changes: every command line, source and kind is as in C3V001, plus the one P0 line.')
emit('')
emit('## P0. Common preamble — the start of every call')
emit('')
emit('```bash')
for t, kind, ref in P0:
    emit(t); xref.append({'line': len(md), 'block': 'P0', 'kind': kind, 'ref': ref, 'text': t})
emit('```')
emit('')
emit('## PJ. Addendum preamble — Branch S blocks include it (shown inside each block)')
emit('')
emit('PJ is J:L12-L27, then D1 (instead of J:L28-L29), then J:L30. It appears in full inside every Branch S block below.')
emit('')

for b in BLOCKS:
    emit('## %s — %s' % (b['id'], b['title']))
    emit('')
    if b['before']:
        emit(b['before']); emit('')
    if b['code']:
        emit('```bash')
        for t, kind, ref in b['code']:
            emit(t); xref.append({'line': len(md), 'block': b['id'], 'kind': kind, 'ref': ref, 'text': t})
        emit('```')
        emit('')
    if b['after']:
        emit(b['after']); emit('')

emit('## X. Cross-reference — every code line and its source')
emit('')
emit('Kinds:')
emit('- **VERBATIM:** the source line, unchanged.')
emit('- **QOS_DROPPED:** the source line without its `taskpolicy`/`nice` prefix (A274 item 1).')
emit('- **REDERIVED:** a source line repeated in a later call.')
emit('- **PASTE / PASTE_GUARD:** a runtime slot and its guard.')
emit('- **FIXED:** a value stated in a source.')
emit('- **DERIVED:** flagged in 0.6.')
emit('- **COMMENT:** a note only.')
emit('')
emit('| RB line | Block | Kind | Source |')
emit('|---|---|---|---|')
xref_start = len(md)
for x in xref:
    emit('| %d | %s | %s | %s |' % (x['line'], x['block'], x['kind'], x['ref'].replace('|', '/')))
emit('')
raw = ('\n'.join(md) + '\n').encode()
with open(OUT / 'RUNBOOK_EXEC_C3V002.md', 'xb') as f:
    f.write(raw)
xj = {'schema': 'RUNBOOK_XREF_C3V002', 'utc': utc, 'runbook_sha256': hashlib.sha256(raw).hexdigest(),
      'sources': {k: {'path': p, 'sha256': h} for k, (p, h) in SRC.items()}, 'lines': xref}
with open(OUT / 'XREF_C3V002.json', 'x') as f:
    f.write(json.dumps(xj, indent=1, sort_keys=True) + '\n')
print(json.dumps({'runbook_sha256': xj['runbook_sha256'], 'lines': len(md), 'code_lines': len(xref), 'pastes': len(pastes),
                  'kinds': {k: sum(1 for x in xref if x['kind'] == k) for k in sorted({x['kind'] for x in xref})}}))
