# RUNBOOK_EXEC_C3V002 — consolidated verdict-day executable runbook

Claude3, for Claude2 (root). Root 0850 item 2 (V006 A290); executed by root under A292 ("lean, one block per call"). Generated 2026-10-21T16:15:01Z (`date -u`) by `build_runbook_c3v001.py`, which copies every command line verbatim from the sources below and records each line's source in §X. This runbook authorizes nothing: every scientific launch stays root's (sheet L3, L184).

## 0. How to use it

### 0.1 Sources (sha256 from bytes) — the only sources of commands

- **S** = the verdict-day sheet: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_sheet_cx1/VERDICT_DAY_COMMAND_SHEET_CX1V001.md` `f2a5eec4f00a36a6982833a5611e9fe4d4e008ca3736caef4fa30b2aff80242c`
- **J** = the S0 J0–J2 addendum (A276): `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_sheet_addendum_cx3/S0_J_ADDENDUM_CX3V001.md` `d6bdd5fe8563bfd378ad6cd083d5bfc719f67b5c6c018796f5cee0a2d6251320`
- **M** = Claude3 0276, the DBP C2V004C sheet amendment (adopted A291): `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0276_2026-10-21_0836-built-DBP-C2V004C-HEADLINE11-wall-to-phase2-ceiling-data-only-sheet-amendment-review-request.md` `314ef346d6911725c0cb636cd3a7f6b5077af2ead889cad75d169c16a571f0a1`
- **V** = the verdict-day variable template (A272): `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/VERDICT_DAY_VARS_C2V001.sh` `49607ea4a8660f296516e610718bb26db303ad19c6c517a9f409ba11be56eff5`
- **Rulings applied** (V006, read by heading): A261 (N1–N5), A263 (P1–P4, W1–W3), A268 (the pre-staged §5/§6 gating reviews: Codex3 0683/0684, checker `check_verdict_gates_cx3v003.py` `78358dac`; root 0829 and erratum 0830), A271, A272, A274, A275, A276, A291 (C2V004C adopted).

### 0.2 Execution model

- **Fail-fast (C3V002, Codex2 0580 F-STOP-1).** P0 starts with `set -euo pipefail` (J:L12). The first failing command stops the whole call, and no later command can mask it. Any non-zero exit is a STOP, including the kit's exit 4 flag: review it before continuing.
- **One block per call.** Each call is P0 followed by one block's code, pasted together into one `/bin/bash` invocation (S:L13). Shell variables do not persist between calls. A block re-derives what it needs from files with the same source lines (kind REDERIVED in §X), or takes a PASTE value.
- **PASTE slots.** A line `NAME=   # PASTE: …` is followed by the guard `: "${NAME:?PASTE NAME}"` (the guard form of J:L53). Root types the actual value after `=` before running; an empty slot stops the call. Values come from actual artifacts, never from historical hashes (S:L124).
- **Bash timeouts.** Run every call with `timeout: 600000`, or in the background (`run_in_background`) when it may take longer. B3a, B3c, B4, B8b and the kit DRYs have untested durations, and each B11 launch may wait up to about 300 s for its launch receipt (kit L37, L230). A call killed by the tool's default 120 s timeout leaves partial exclusive-create outputs; those need new paths and a root ruling (S:L32).
- **Paste and invocation hygiene.** Replace a slot's whole right-hand side as `NAME='value'`, deleting the `# PASTE` comment. Quote values with spaces (paths under CTRL; `VERDICT_RULING`). Use absolute paths. Write each call (P0 + block) to a file and run it with `/bin/bash FILE`: the blocks contain heredocs and single quotes.
- **STOP** means: halt the dependent chain, preserve partial outputs, and choose new paths after root's ruling (S:L32). Retries need a new root ruling (S:L169). An exit code alone never authorizes the next step (S:L84, L132, L180).
- **Working directory** persists between calls, but shell state does not. B5a and B5b run `cd "$C4"` (S:L89); every other command uses absolute paths.
- **Branch S blocks** include PJ, the addendum's preamble with `set -euo pipefail` and `set -o noclobber` (J:L12-L13), so the first failing command stops the call.

### 0.3 Rulings that change the sheet

1. **QoS (A274 item 1, the final form of A263/A258).** No `taskpolicy -b` and no `nice -n 10` on any §3–§8 command; the exception list is empty. Lines changed this way are kind QOS_DROPPED in §X. The launcher's own generated environment (B10LH) is not a §3–§8 command and is never bypassed (S:L169).
2. **HEADLINE11 caps (A291; 0276).** First attempts use DBP C2V004C `ce9cbef8` (wall 3,443,340 s). The sheet's L8 "HEADLINE11 first attempts retain DBP wall100800" is superseded. The caps check after bind (B9b) is a STOP gate. The optional exact refill (0276 item 4) is not part of this flow.
3. **Reruns (A275, A282).** No P112 launch on verdict day. Any cap or infrastructure rerun waits for the adopted single launcher (cw8 v003, A282) and its builder. The sheet's "cap reruns use reviewed P112 cx2v004" (L8) and its "subsequent retries need reviewed P112 cx2v004" (L180) do not apply.
4. **Order inside Branch H (A261 N3).** §8 FINAL specs → each HEADLINE11 spec's driver dry plan → §9. S0 dry plans stay with S0.
5. **S0 independence (A274 item 3; A263 W2; J:L5).** S0 needs B1–B4, its own registrations, dry plans and START. It does not wait for B5R/B6R or Branch H.
6. **Folders (A272, A261 N1, A276; V).** Already created and never re-created: `$C4/final`, `$CX2/v006r11_c4`, `$R/chain`, `$PS`, `$E_S0`, `$E_H11`, `$PRELAUNCH_OUT`, `$STEP4_OUTPUT_ROOT`, `$S0_LAUNCH_ROOT`, `$S0_STAGE` with `fills/` and `driver_plans/`. Left absent for their tools: `$R/H11_EVIDENCE`, `$S0_RUN_ROOT`, `$S0_STAGE/handoffs`, `$S0_STAGE/fills/J0-J2`, `$S0_STAGE/driver_plans/J0-J2`. **So the addendum's two `mkdir` lines (J:L28-L29) are not run;** they would fail on the existing folders under `set -e`. PJ checks the folders exist instead (D1).
7. **Model outcomes (A261 N4).** A FINISHED receipt with driver_status COMPLETED_INVALID is a model outcome under A245, never an infrastructure retry. **V005 (A261 N5)** is not edited before §5.
8. **Gating reviews (A263 W1; A268).** §5 and §6 are Codex3 checker runs against its pre-review, with Codex1 as fallback. Root posts the requests (B5R, B6R); Branch H waits for both PASSes.
9. **V006 write freeze (J:L5; kit L23, L34).** The seed's `--launch` (B11.1) writes the M-15 record and refuses if V006 changed since it. From the start of B11.1 until the seed's confirmed launch record, neither branch appends to V006. Schedule Branch H's V006 writes (for example the HEADLINE11 registrations and admission publication) before B11.1 or after that record.

### 0.4 Parallel map (A263 P1–P4)

```text
B1 → B2 → [ B3a (one call per label) ∥ B3b ] → B3c → B4
B4 ─┬─ Branch H: [ B5a → B5b → B5c → B5R ] ∥ [ B6 → (and B5c) → B6R ] → B8a → B8b → B7H (per spec, ∥) → B9a → B9b → B10H → B10LH
    └─ Branch S: B7S1 → B7S2 (∥ with B7S3 → B7X per spec) → B7S4 → B10S → B11.1 seed → B11.2 J0 → B11.3 J1 → B11.4 J2 → B11.5 twin
    V006: no append by either branch from the start of B11.1 until the seed's confirmed launch record (J:L5; kit L34)
```

- **P1:** B3a for every selected label, and B3b, run at once; only B3c waits for the EA components.
- **P2:** B5 and B6 run at once; B8 needs both gating PASSes.
- **P3:** Branch S runs alongside Branch H once B4 is done. S0 launches also wait for step 2's last receipt (S:L180; J:L127).
- **P4:** the per-spec dry plans (B7H; B7X; the J dry plans in B7S2) are independent.

## 0.5 PASTE register — every value root supplies at run time

| Name | Blocks | What | Source |
|---|---|---|---|
| `S4T_R3_RECEIPT` | B1 | receipt path from the registered R3 launch record, not R2; outdir ends KMAX_V007_P128_S4T_MS128_CX1_RUN_V011_CX3V001_R3 | S:L36 |
| `UNT_ROOT_ADMISSION_SHA256` | B3a, B3b, B3c, B4 | B3a: from the independent root publication; producer_guard_cx1v008 has no path override; B3b, B3c: as in B3a; B4: as in B3a (only the §3 producers are known to read it; harmless if the comparator does not) | S:L32 |
| `CASE_RUN` | B3a | the registered run of this case (R3 for S4T) | S:L61 |
| `CASE_LABEL` | B3a | one exact base label from B2 | S:L61 |
| `RESULT_MANIFEST` | B3b | the B2 result manifest path | S:L55 |
| `EA_COMPONENT_MANIFEST` | B3c | label → component-byte-pin manifest (not `runs`), including the registered C5H component; that component is solely root's existing blinded procedure | S:L72 |
| `CASES` | B4 | the B2 cases manifest path | S:L55 |
| `VERDICT_DIR` | B4, B5a, B5b, B6 | B4: a new, unused folder for the comparison report; B5a, B5b, B6: the B4 folder | S:L13 (all new paths must be unused) |
| `VERDICT_RULING` | B6 | root's ruling argument for the fill | S:L114 |
| `H1_PREDECESSOR` | B8a | root's H1 predecessor from the frozen C1 tail_readiness and the adopted r11 bindings | S:L136 |
| `STEP4_SEAL` | B8b | root's registered step-4 seal path | S:L141; S:L27 |
| `STEP4_SEAL_SHA` | B8b | its byte sha256 | S:L141; S:L27 |
| `R11_POLICY_SHA` | B8b | the digest printed by B5b | S:L105, L109 |
| `FINAL_SPECS_DIR` | B8b | a new, unused output folder | S:L141; S:L13 |
| `DRIVER` | B7H | the call's registered driver path (DDO r5 b5cc62af… or NGC r008 577f8c94…, per the annex and the call) | S:L132 |
| `DRIVER_SHA` | B7H | its full sha256 | S:L132 |
| `FILLED_SPEC` | B7H, B7X | B7H: one FINAL spec from B8b; B7X: the seed serial spec, or the seed twin spec | S:L126 |
| `FILLED_SPEC_SHA` | B7H, B7X | its sha256 from bytes | S:L132 |
| `NEW_DRY_REPORT_DIR` | B7H, B7X | B7H: a new path; the driver creates its report folder; B7X: a new path | S:L126; J:L44 |
| `ADMISSION_CANDIDATE` | B9a | the admission candidate path | S:L151 |
| `ADMISSION_CANDIDATE_SHA` | B9a | its sha256 | S:L151 |
| `GUARD011_CANDIDATE` | B9a | the guard011 candidate plan (emission only, A218) | S:L151; S:L11 |
| `GUARD011_CANDIDATE_SHA` | B9a | its sha256 | S:L151 |
| `GUARD014_FINAL_PLAN` | B9b | the root-written final plan | S:L152 |
| `FINAL_ADMISSION_CANDIDATE` | B9b | the root-written final admission candidate | S:L152 |
| `BOUND_PLAN` | B9b | a new path under $PACKET | S:L152; V:L14 |
| `BOUND_ADMISSION` | B9b | a new path under $PACKET | S:L152; V:L14 |
| `BOUND_COMMAND` | B9b | a new path under $PACKET | S:L152; V:L14 |
| `PHASE_SOURCE_ARGS` | B10H | --doc-pin SHA PATH entries for the final run configs, plans, admission records and registered inputs, including the C1 pin with --scope "$C1" /tail_readiness and the registry pin | S:L167 |
| `ROOT_FIELDS` | B7S1 | root's actual §7 root-fields path (schema PHASE1_POINT_HANDOFF_ROOT_FIELDS_C2V001) | J:L50 |
| `ROOT_FIELDS_SHA` | B7S1 | its byte sha256 | J:L50 |
| `STEP2_LAST_RECEIPT` | B7S3, B7S4, B11.1, B11.2, B11.3, B11.4, B11.5 | B7S3: the actual last step-2 receipt (see gap G3); B7S4: as in B7S3; B11.1, B11.2, B11.3, B11.4, B11.5: the actual last step-2 receipt | S:L176; J:L130 |
| `PIN_NAME` | B7X | S0_SEED_SERIAL for the serial spec, or S0_SEED_CW8_TWIN for the twin (kit L357) | S:L124 |
| `SEED_DRY_FILL_DIR` | B7S4 | the seed DRY fill folder from B7S3 | S:L177 |
| `SEED_HANDOFF` | B10S | the seed handoff among the four B7S1 emitted (registered HANDOFF_PIN S0_SEED) | S:L124; J:L50 |
| `SEED_HANDOFF_SHA` | B10S | its registered sha256 | S:L124 |
| `SEED_SPEC` | B10S | the registered seed serial spec (SPEC_PIN S0_SEED_SERIAL) | S:L124 |
| `SEED_SPEC_SHA` | B10S | its registered sha256 | S:L124 |
| `TWIN_SPEC` | B10S | the registered seed twin spec (SPEC_PIN S0_SEED_CW8_TWIN; kit L357) | S:L124 |
| `TWIN_SPEC_SHA` | B10S | its registered sha256 | S:L124 |
| `EXTRA_DOC_PINS` | B10S | --doc-pin SHA PATH entries for the actual verdict binding, final metadata/plans/admissions, referenced inputs and the dry-report/plan pins; add a scoped C1/registry pin only if the S0 config carries tail_readiness | J:L123; S:L167 |
| `UNT_STEP4_ADMISSION_PATH` / `UNT_STEP4_ADMISSION_SHA256` | B10LH | root's independent publication of the bound admission | S:L169 |

## 0.6 Derived lines and gaps (flagged for the narrow check)

- **D1** (PJ): three `[ -d … ]` checks replace J:L28-L29 `mkdir`, because A276 pre-created those folders (one check per line, so `set -e` stops on any).
- **D2** (B4): a `printf` of the verdict path and sha, so root can publish them (S:L84); printf form of J:L63.
- **D3** (B8b): `H1_CONFIG_SHA` from the written bytes, as S:L144 instructs; form of S:L81.
- **D4** (B7H, B7X): the spec hash check before each dry plan, as S:L132 instructs; form of J:L91.
- **D5** (B10H, B10S): a non-empty check on `PHASE_SOURCE_ARGS` (S:L167).
- **D6** (B10S): the J `--doc-pin` pairs in J:L123's exact form, the same form for the seed and twin, and the root-supplied extra pins.
- **D7** (B7X): a `printf` of the SPEC_PIN line, in J:L106's form, with the kit's pin names (kit L357).
- **G1:** the seed's fill comes from the kit's seed DRY (B7S3, S:L176); the sources give no separate filler command for the seed.
- **G2:** the §6 README publication `cp -n` steps (S:L120) are outside 0850's source list and are not reproduced. Publication may be checked after the gating review (Codex3 0684).
- **G3:** S:L176's seed DRY passes `--step2-receipt`, while the J DRY lines (J:L116-L118) do not. This is likely moot: B4 consumes every step-2 result, so step 2's last receipt exists before Branch S starts.
- **G5:** HANDOFF_PIN S0_SEED: the seed handoff is one of the four files B7S1 emits, but the sources name only the J files. Root identifies the seed's file and composes the line in J:L63's form.
- **G6:** WATCH_PIN MEMORY_WATCH and the V007 adoption pin: their syntax is the kit's parsed V006 contract (S:L124), not reproduced here.
- **G7:** the twin's SPEC_PIN name is S0_SEED_CW8_TWIN (kit L357). B7X prints both seed lines.
- **G4:** the gating checker's command line is not in the sources; Codex3 runs it, and root posts the requests (B5R, B6R).

## 0.7 Changes from C3V001 (`553a0e2c`)

- **F-STOP-1 (Codex2 0580, blocking): fixed.** P0 now starts with `set -euo pipefail` (J:L12). In C3V001, B9b's caps check could return 0 after a binder refusal, and B4 could hide a comparator failure.
- **SHOULD_FIX:** B7S4's DRY_WORK sentence now covers the J DRYs only, and the PASTE register gives each block's own description for `FILLED_SPEC` and the other shared names.
- Nothing else changes: every command line, source and kind is as in C3V001, plus the one P0 line.

## P0. Common preamble — the start of every call

```bash
set -euo pipefail
source "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/VERDICT_DAY_VARS_C2V001.sh"
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
CTRL='/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
PKT="$ART/v007_launch_packet_cx1"
H3="$ART/h3_campaign_path_c2"
C4="$ART/b1_policy_successor_c4"
C1="$ART/c1_h1_c2/C1_H1_C2V001.json"
REG="$ART/s4rc1_c3/registry_c2v001/REGISTRY_31pts_20261020T140004Z.json"
COMPARE="$CTRL/V007_SEAL_ASSEMBLY/kmax_tail_compare_c2v007_r14_cx1v001_SEALED_V007.py"
PREREG="$CTRL/V007_SEAL_ASSEMBLY/KMAX_TAIL_PREREG_V007_SEALED.json"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
```

## PJ. Addendum preamble — Branch S blocks include it (shown inside each block)

PJ is J:L12-L27, then D1 (instead of J:L28-L29), then J:L30. It appears in full inside every Branch S block below.

## B1 — S4T R3 receipt check (sheet §1)

**Root only** (S:L34). **Wait for:** root's watch reporting the S4T R3 monitor exit (A292). **Call:** P0 + this block.

```bash
S4T_R3_RECEIPT=   # PASTE: receipt path from the registered R3 launch record, not R2; outdir ends KMAX_V007_P128_S4T_MS128_CX1_RUN_V011_CX3V001_R3
: "${S4T_R3_RECEIPT:?PASTE S4T_R3_RECEIPT}"
"$PY" -I -B - "$S4T_R3_RECEIPT" <<'CHECK'
from pathlib import Path
import json,hashlib,sys
p=Path(sys.argv[1]); raw=p.read_bytes(); r=json.loads(raw)
print('receipt_sha256',hashlib.sha256(raw).hexdigest())
for k in ('schema','utc_start','utc_end','status','driver_status','exit_code','stop_reason','command','pins','caps','result'):
    print(k,json.dumps(r.get(k),sort_keys=True))
assert r.get('status')=='FINISHED' and type(r.get('exit_code')) is int and r['exit_code']==0
assert r.get('stop_reason') is None and r.get('driver_status')=='COMPLETED'
CHECK
```

**Expected:** exit 0; prints `receipt_sha256` and the eleven fields. Root compares command, pins, caps and the result reference with the R3 launch publication: driver b5cc62af…, spec 8e71be9b…, wall 792000, RSS 137438953472, output 103079215104. Do not dereference the result in this step (S:L51).

**STOP:** any non-success pauses the verdict path for root classification; no retry and no scientific invalidation is inferred (S:L51). A FINISHED receipt whose driver_status is COMPLETED_INVALID fails the assert: it is a model outcome that root classifies under A245, never an infrastructure retry (A261 N4).

## B2 — Cases manifest and result manifest (sheet §2) — ROOT ACTION, no command in the sources

**Root writes, by exclusive create** (S:L55, L57):
- `CASES` from the registered cases-manifest schema. `cases.S4T` names R3; all other case paths and bindings stay registered. The comparator resolves the sealed case block itself.
- `RESULT_MANIFEST`: an object whose `runs` maps each exact T label to `{path, sha256}` of its `result.json`. Never use a cases directory map as the pinned-result manifest.
- Exact base labels: C2T, C3T, C4T, C6T, S4T, C4T-D5, C4T-C5c, C4T-KLO, C4T-KHI, C4T-A.
- FLAG_RULINGS also needs a byte pin `root_rulings` to root's explicit request (FLAG_RULINGS_REQUEST_SCHEMA_V001.json).
- Root hashes actual result bytes only when authorized to produce the gates. Publish both manifest hashes.

**Expected:** complete exact labels, unique run paths, S4T R3. **STOP:** an absent, aliased, stale-R2 or mismatched input (S:L57).

**Order note:** if the cases manifest must bind the §3 gate records (S:L72), write `CASES` after B3c, before B4.

## B3a — Per-label EA replay and HARMONICS (sheet §3; parallel P1)

**Root only** (S:L59). **Call once per case selected by the gate contract** (S:L61). The calls run at the same time, together with B3b (A263 P1).

```bash
export UNT_ROOT_ADMISSION_SHA256=   # PASTE: from the independent root publication; producer_guard_cx1v008 has no path override
: "${UNT_ROOT_ADMISSION_SHA256:?PASTE UNT_ROOT_ADMISSION_SHA256}"
CASE_RUN=   # PASTE: the registered run of this case (R3 for S4T)
: "${CASE_RUN:?PASTE CASE_RUN}"
CASE_LABEL=   # PASTE: one exact base label from B2
: "${CASE_LABEL:?PASTE CASE_LABEL}"
"$PY" -I -B "$PKT/ea_replay_cx1v012.py" "$CASE_RUN" "$CASE_LABEL" "$PS/EA_${CASE_LABEL}.json"
"$PY" -I -B "$PKT/ra10_checkpoint_cx1v012.py" "$CASE_RUN" "$CASE_LABEL" "$PS/HARMONICS_${CASE_LABEL}.json"
```

**Expected:** exit 0 and new stamped records `$PS/EA_<label>.json` and `$PS/HARMONICS_<label>.json` (S:L72). HARMONICS uses the ra10 checkpoint readout with route_a_tail_replay v005 for tail-ON. It reports saved-state harmonics, not a convergence acceptance. Bind each returned HARMONICS record as the sealed manifest contract requires; do not fabricate a combined record (S:L72).

**STOP:** any missing gate, partial record, producer refusal or unresolved root flag stops comparison (S:L74).

## B3b — MT, I1T and FLAG_RULINGS (sheet §3; parallel with B3a)

```bash
export UNT_ROOT_ADMISSION_SHA256=   # PASTE: as in B3a
: "${UNT_ROOT_ADMISSION_SHA256:?PASTE UNT_ROOT_ADMISSION_SHA256}"
RESULT_MANIFEST=   # PASTE: the B2 result manifest path
: "${RESULT_MANIFEST:?PASTE RESULT_MANIFEST}"
"$PY" -I -B "$PKT/postseal_records_cx1v006_cx3v001.py" MT "$RESULT_MANIFEST" "$PS/MT.json"
"$PY" -I -B "$PKT/postseal_records_cx1v006_cx3v001.py" I1T "$RESULT_MANIFEST" "$PS/I1T.json"
"$PY" -I -B "$PKT/postseal_records_cx1v006_cx3v001.py" FLAG_RULINGS "$RESULT_MANIFEST" "$PS/FLAG_RULINGS.json"
```

**Expected:** exit 0; new `$PS/MT.json`, `$PS/I1T.json`, `$PS/FLAG_RULINGS.json`. I1T exports actual runtime checks, not a new replay. FLAG_RULINGS exports root decisions and creates none (S:L72).

**STOP:** as B3a (S:L74).

## B3c — EA aggregate (sheet §3; after every B3a EA record)

```bash
export UNT_ROOT_ADMISSION_SHA256=   # PASTE: as in B3a
: "${UNT_ROOT_ADMISSION_SHA256:?PASTE UNT_ROOT_ADMISSION_SHA256}"
EA_COMPONENT_MANIFEST=   # PASTE: label → component-byte-pin manifest (not `runs`), including the registered C5H component; that component is solely root's existing blinded procedure
: "${EA_COMPONENT_MANIFEST:?PASTE EA_COMPONENT_MANIFEST}"
"$PY" -I -B "$PKT/aggregate_records_cx1v008.py" EA "$EA_COMPONENT_MANIFEST" "$PS/EA.json"
```

**Expected:** exit 0; new `$PS/EA.json` (S:L72).

**STOP:** as B3a. The five gate families do not replace the sealed manifest's full registry: preserve every other required identity/SR/T2I/shell record. A88's SR_K timing is a prior obligation; never redo it after T outputs are read (S:L74).

## B4 — Sealed compare r14 (sheet §4)

**Wait for:** B3a, B3b and B3c complete with no STOP.

```bash
export UNT_ROOT_ADMISSION_SHA256=   # PASTE: as in B3a (only the §3 producers are known to read it; harmless if the comparator does not)
: "${UNT_ROOT_ADMISSION_SHA256:?PASTE UNT_ROOT_ADMISSION_SHA256}"
CASES=   # PASTE: the B2 cases manifest path
: "${CASES:?PASTE CASES}"
VERDICT_DIR=   # PASTE: a new, unused folder for the comparison report
: "${VERDICT_DIR:?PASTE VERDICT_DIR}"
"$PY" -I -B "$COMPARE" --prereg "$PREREG" --manifest "$CASES" --outdir "$VERDICT_DIR"
VERDICT="$VERDICT_DIR/KMAX_TAIL_COMPARISON.json"
VERDICT_SHA=$(shasum -a 256 "$VERDICT" | cut -c1-64)
printf 'VERDICT %s %s\n' "$VERDICT_SHA" "$VERDICT"
```

**Expected:** a new report; exit code alone never authorizes adoption. Use the full decision: no test, validity-only, gates-only or no-packets override (S:L84). Root checks: schema UNT_KMAX_TAIL_COMPARISON_C2V007_R11, script_sha256 a99105a1…, prereg.sha256 b2989012…, pins_verified.V005_addendum c01b3c51…, decision.outcome ADOPT_TAIL, decision.tests_read true, test_mode false (S:L84).

**STOP:** if any of these differs (S:L84).

**Then:** publish the verdict path and byte SHA (S:L84). Branch H (B5, B6) and Branch S (B7S1) start now (A263 P2, P3; A274 item 3).

## B5a — r11 policy, dry run (sheet §5; parallel P2 with B6)

**Pre-conditions:** `$C4/final` exists (A261 N1; V:L4). V005 (`c01b3c51`) is not edited before §5 (A261 N5).

```bash
VERDICT_DIR=   # PASTE: the B4 folder
: "${VERDICT_DIR:?PASTE VERDICT_DIR}"
VERDICT="$VERDICT_DIR/KMAX_TAIL_COMPARISON.json"
VERDICT_SHA=$(shasum -a 256 "$VERDICT" | cut -c1-64)
cd "$C4"
"$PY" -I -B tools/run_fenced_c4st2.py tools/make_b1_cascade_c4v002.py "$C4/final" v006r11_c4 --dry-run --policy-only --seal-tuple a99105a19b582c68d961e0ee12be3a2efa79dbd1e65d63682c3d2d8daa55f0ab b2989012c92161a7da3dd10d0148e1607422416d369fc4ebe164217758b5c695 c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1 UNT_KMAX_TAIL_COMPARISON_C2V007_R11 "$VERDICT_SHA"
```

**Expected:** dry exit 0 (S:L95). **STOP:** any refusal; a changed method, changed base pins or a tuple mismatch (S:L109).

## B5b — r11 policy, write (sheet §5; only after B5a succeeded)

"Only after dry success" (S:L91).

```bash
VERDICT_DIR=   # PASTE: the B4 folder
: "${VERDICT_DIR:?PASTE VERDICT_DIR}"
VERDICT="$VERDICT_DIR/KMAX_TAIL_COMPARISON.json"
VERDICT_SHA=$(shasum -a 256 "$VERDICT" | cut -c1-64)
cd "$C4"
"$PY" -I -B tools/run_fenced_c4st2.py tools/make_b1_cascade_c4v002.py "$C4/final" v006r11_c4 --write --policy-only --seal-tuple a99105a19b582c68d961e0ee12be3a2efa79dbd1e65d63682c3d2d8daa55f0ab b2989012c92161a7da3dd10d0148e1607422416d369fc4ebe164217758b5c695 c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1 UNT_KMAX_TAIL_COMPARISON_C2V007_R11 "$VERDICT_SHA"
```

**Expected:** an exclusive policy write, not the test `build_f1` output (S:L95). **STOP:** any refusal; then do not run B5c (S:L109).

## B5c — r11 policy, copy and byte check (sheet §5; only after B5b succeeded)

**Pre-conditions:** the destination parent `$CX2/v006r11_c4` exists (A272 hard stop 1; V:L5) and the destination file is absent; `cp -n` may silently skip (S:L109).

```bash
SRC="$C4/final/v006r11_c4/adoption_policy_cx2v006r11_c4.py"
DST="$ART/calib_tail_readiness_cx2/v006r11_c4/adoption_policy_cx2v006r11_c4.py"
cp -n "$SRC" "$DST"
"$PY" -I -B - "$SRC" "$DST" <<'CHECK'
from pathlib import Path
import hashlib,sys
a,b=(Path(x).read_bytes() for x in sys.argv[1:]); assert a==b
print(hashlib.sha256(b).hexdigest())
CHECK
```

**Expected:** the CHECK asserts the bytes of SRC and DST are equal and prints the policy digest (S:L105). **Publish it as `R11_POLICY_SHA`** (S:L109).

**STOP:** a byte mismatch, a changed method, base pins or tuple (S:L109).

## B5R — §5 gating review — ROOT ACTION (A263 W1, A268; 0829 as corrected by 0830)

Root posts a numbered FROM_CODEX review request carrying the actual `--write` output shas (0829 §5, with 0830's restored flag). Codex3 checks them against its pre-review: the r10 baseline with only line 13 (the registration comment) and line 16 (the tuple) changed, which reconstructs r10 exactly (`93d9c0ac`). It uses `check_verdict_gates_cx3v003.py` `78358dac` (45 control checks); the checker hashes the root-named report, reads only the seven authorized fields, refuses any reading other than sealed ADOPT_TAIL and requires exact bytes (A268; Codex3 0683). Codex1 is the fallback gating reviewer (0829); Codex1's second look is nongating (S:L109; A208). Target answer about 15 minutes (0829). Root checks FROM_CODEX3 (and FROM_CODEX1) for the PASS: root's lane-outbox watch is stopped (A292).

**STOP:** Branch H waits for this PASS (A263 W1). Branch S does not (A274 item 3).

## B6 — H3 r12 fill and build (sheet §6; parallel P2 with B5)

**Pre-condition:** `$R/chain` exists (A272 hard stop 2; V:L7). Do not run `mkdir "$R/chain"`.

```bash
VERDICT_DIR=   # PASTE: the B4 folder
: "${VERDICT_DIR:?PASTE VERDICT_DIR}"
VERDICT="$VERDICT_DIR/KMAX_TAIL_COMPARISON.json"
VERDICT_RULING=   # PASTE: root's ruling argument for the fill
: "${VERDICT_RULING:?PASTE VERDICT_RULING}"
"$PY" -I -B "$H3/regenerate_h3_c2v004.py" fill --report "$VERDICT" --filled-by 'root (Claude2)' --ruling "$VERDICT_RULING" --out "$R/SEAL_TUPLE_RECORD_H3_FILLED.json"
SEAL_RECORD="$R/SEAL_TUPLE_RECORD_H3_FILLED.json"
SEAL_SHA=$(shasum -a 256 "$SEAL_RECORD" | cut -c1-64)
"$PY" -I -B "$H3/regenerate_h3_c2v004.py" build --seal-record "$SEAL_RECORD" --seal-record-sha256 "$SEAL_SHA" --out-dir "$R/chain"
```

**Expected:** exit 0, `chain/v006r12_c4` and `REGENERATE_RECORD_v006r12_c4.json`; exit 2 refuses (S:L120). Diff against `h3_campaign_path_c2/placeholder_chain_c2v004/v006r12_c4`, not an older placeholder or wrapper (S:L120). Root follows the README publication `cp -n` and byte-equality checks for policy, core and wrapper; the entry stays at its generated path as registered (S:L120). Those README commands are outside 0850's source list and are not reproduced here (gap G2); publication may be checked after the gating review (Codex3 0684).

**STOP:** exit 2 or any other refusal.

## B6R — §6 gating review — ROOT ACTION (A263 W1, A268)

**Wait for:** B6 and B5c (the request carries the r11 policy, S:L120). Root posts a fresh numbered FROM_CODEX review request with: the verdict path and hash, the seven allowed verdict fields (0770), the r11 policy, the seal tuple record, the four r12 files, the regenerate record and the byte hashes (S:L120). Codex3 (gating) checks only the permitted bytes: policy L13 and L16, core L202 (the policy sha), wrapper L29 (the core sha) and entry L61 (the wrapper sha); everything else must be byte-identical, compared on complete expected bytes (A268; Codex3 0684). Codex1's second lens is nongating (S:L120); Codex1 is the gating fallback if Codex3 is unavailable (0829). Root checks FROM_CODEX3 (and FROM_CODEX1) for the PASS (A292).

**STOP:** Branch H waits for this PASS (A263 W1).

## B8a — H1 config (sheet §8; after both B5R and B6R PASS)

**Wait for:** B5R and B6R PASS (A263 P2: §8 needs both). **Root action first:** write `$H1_DELTA` (S:L136). Use only C1.tail_readiness, not C1's other top-level keys (S:L136).

```bash
H1_PREDECESSOR=   # PASTE: root's H1 predecessor from the frozen C1 tail_readiness and the adopted r11 bindings
: "${H1_PREDECESSOR:?PASTE H1_PREDECESSOR}"
# H1_DELTA and H1_CONFIG are set by VARS (V:L12-13); root writes the delta file before this call (S:L136)
SEAL_RECORD="$R/SEAL_TUPLE_RECORD_H3_FILLED.json"
SEAL_SHA=$(shasum -a 256 "$SEAL_RECORD" | cut -c1-64)
BLOCK_SOURCE="$PKT/P128/specs/C4T_P128_MS128_R5_CX1V004.FILLED.json"
"$PY" -I -B "$H3/apply_fields_c2v006/apply_h3_fields_c2v006.py" "$H1_PREDECESSOR" "$H1_DELTA" "$H1_CONFIG" "$R/H1_APPLY_REPORT.json" --seal-record "$SEAL_RECORD" --seal-record-sha256 "$SEAL_SHA" --block-source "$BLOCK_SOURCE" --block-source-sha256 de6d7d77d053d9c983f15eca11468fe8520d025ff2ad1f643b2a517a915b1738
```

**Expected:** apply exit 0 and a verified verdict/prereg association (S:L144). **STOP:** exit 3 (undecided or refused) or 5 (write failure) stops binding, including any partial folder (S:L144).

## B8b — FINAL specs (sheet §8; after B8a succeeded)

```bash
STEP4_SEAL=   # PASTE: root's registered step-4 seal path
: "${STEP4_SEAL:?PASTE STEP4_SEAL}"
STEP4_SEAL_SHA=   # PASTE: its byte sha256
: "${STEP4_SEAL_SHA:?PASTE STEP4_SEAL_SHA}"
R11_POLICY_SHA=   # PASTE: the digest printed by B5b
: "${R11_POLICY_SHA:?PASTE R11_POLICY_SHA}"
FINAL_SPECS_DIR=   # PASTE: a new, unused output folder
: "${FINAL_SPECS_DIR:?PASTE FINAL_SPECS_DIR}"
HEADLINE_CASES='TAIL_REANCHOR,WORKERS_8_CANDIDATE_ANCHOR,HEADLINE_TRIAL,HEADLINE_CORNER_000,HEADLINE_CORNER_001,HEADLINE_CORNER_010,HEADLINE_CORNER_011,HEADLINE_CORNER_100,HEADLINE_CORNER_101,HEADLINE_CORNER_110,HEADLINE_CORNER_111'
DST="$ART/calib_tail_readiness_cx2/v006r11_c4/adoption_policy_cx2v006r11_c4.py"
H1_CONFIG_SHA=$(shasum -a 256 "$H1_CONFIG" | cut -c1-64)
"$PY" -I -B "$ART/step4_launch_readiness_c4/handoff_v004/tools/produce_final_step4_specs_c4v004.py" final --config "$H1_CONFIG" --config-sha "$H1_CONFIG_SHA" --seal "$STEP4_SEAL" --seal-sha "$STEP4_SEAL_SHA" --adoption-policy "$DST" --adoption-policy-sha "$R11_POLICY_SHA" --cases "$HEADLINE_CASES" --outdir "$FINAL_SPECS_DIR" --utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

**Expected:** producer exit 0 and complete FINAL output and manifest (S:L144). FINAL mode reads the registry only from C1 tail_readiness; passing `--registry` would refuse (S:L144).

**STOP:** exit 3 or 5 stops binding, including any partial folder. Compare the final `binder_pins` with all nine table-D values below; never bind provisional or test specs. The frozen registry and C1 pins stay unchanged (S:L144).

**0778 table D — expected FINAL binder pins (copied from S:L188-L198):**

| # | Case | Registry row | Predicted spec sha256 |
|---|---|---|---|
| 2 | TRIAL | P01 | `f4ae15461f669979e8648e6686f093c6a909988f9cfb122de71b42c073327aff` |
| 3 | CORNER_000 | P02 | `14e943baa68acceec5dfd600efa8b7b536d7c76adb5239d900a597d4e0c24cec` |
| 4 | CORNER_001 | P03 | `eed3be9b19b6941ba30ab4ac09e8787f6aaf331ba2e6d81317dea51cc597bf40` |
| 5 | CORNER_010 | P04 | `e6c0e3cda12276c3fb830906c0ee30c9a20912015225418755145182e3a81031` |
| 6 | CORNER_011 | P05 | `bb7014113d66c38b634d07e4ff59a730c3762812c10e9bace78c0280bd12505b` |
| 7 | CORNER_100 | P06 | `fac5b8a11754ecc5b4665c2f640f8bce56d5c614c52e42b39ceb3a9ea469ed7c` |
| 8 | CORNER_101 | P07 | `d6a63c4bcb47f0b05b5d08c740d1ea67bf5a4ad2240313ce087410e9f804a290` |
| 9 | CORNER_110 | P08 | `44fee9a4e247d810d508b440c9dc07e67aa5abf7dac312704bc2e2df92b9112e` |
| 10 | CORNER_111 | P09 | `ca46f232cd9d18601c218f895ec490679df85fae710057f2edea9cf71265a510` |

## B7H — Driver dry plan for each HEADLINE11 FINAL spec (sheet §7; after B8b, before B9 — A261 N3; parallel P4)

**Call once per FINAL spec**; the calls can run at the same time (A263 P4). Order: §8 → these dry plans → §9 (A261 N3).

```bash
set -euo pipefail
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
DRIVER=   # PASTE: the call's registered driver path (DDO r5 b5cc62af… or NGC r008 577f8c94…, per the annex and the call)
: "${DRIVER:?PASTE DRIVER}"
DRIVER_SHA=   # PASTE: its full sha256
: "${DRIVER_SHA:?PASTE DRIVER_SHA}"
FILLED_SPEC=   # PASTE: one FINAL spec from B8b
: "${FILLED_SPEC:?PASTE FILLED_SPEC}"
FILLED_SPEC_SHA=   # PASTE: its sha256 from bytes
: "${FILLED_SPEC_SHA:?PASTE FILLED_SPEC_SHA}"
NEW_DRY_REPORT_DIR=   # PASTE: a new path; the driver creates its report folder
: "${NEW_DRY_REPORT_DIR:?PASTE NEW_DRY_REPORT_DIR}"
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
[ "$(sha "$FILLED_SPEC")" = "$FILLED_SPEC_SHA" ]
"$PY" -I -B "$DRIVER" dry-run --spec "$FILLED_SPEC" --report-dir "$NEW_DRY_REPORT_DIR"
```

**Expected:** root reads the blocker lists, requires RI45-13 success, and pins the spec and the dry report. No scientific stage may execute (S:L132).

**STOP:** any blocker or stale spec; no success is inferred from the exit code alone (S:L132).

## B9a — PRELAUNCH emission (sheet §9–10)

**Wait for:** every B7H dry plan accepted.

```bash
DBP_C="$ART/h11_wall_ceiling_c3/C2V004C_FILL_20261022T093000Z/DIRECT_BATCH_PARAMS_S45_C2V004C.json"
DBP_C_SHA=ce9cbef8caaef8120377f302647c71d80387353d192d25d7d0b7e13e5872e809
ADMISSION_CANDIDATE=   # PASTE: the admission candidate path
: "${ADMISSION_CANDIDATE:?PASTE ADMISSION_CANDIDATE}"
ADMISSION_CANDIDATE_SHA=   # PASTE: its sha256
: "${ADMISSION_CANDIDATE_SHA:?PASTE ADMISSION_CANDIDATE_SHA}"
GUARD011_CANDIDATE=   # PASTE: the guard011 candidate plan (emission only, A218)
: "${GUARD011_CANDIDATE:?PASTE GUARD011_CANDIDATE}"
GUARD011_CANDIDATE_SHA=   # PASTE: its sha256
: "${GUARD011_CANDIDATE_SHA:?PASTE GUARD011_CANDIDATE_SHA}"
# PRELAUNCH_OUT is set by VARS (V:L11): new and empty; use a fresh folder for any re-emission
"$PY" -I -B "$ART/step4_prelaunch_cx1/v005/step4_prelaunch_c2v005.py" --admission "$ADMISSION_CANDIDATE" --admission-sha256 "$ADMISSION_CANDIDATE_SHA" --plan "$GUARD011_CANDIDATE" --plan-sha256 "$GUARD011_CANDIDATE_SHA" --output-dir "$PRELAUNCH_OUT"
```

**Expected:** PRELAUNCH records. The candidate names guard011 with a null prelaunch (S:L155).

**Root action before B9b (S:L155; 0276 item 2; A291):**
- Write `GUARD014_FINAL_PLAN`: it names guard014 and launcher015, with the actual PRELAUNCH pins.
- Write `FINAL_ADMISSION_CANDIDATE`: its `sources` equal the source review's `approved_sources` exactly. Retain guard011 and add guard014/launcher015, the native imports, the C1 producers and the adopted r11 policy (C1_ROOT_STEPS §5 + A218). No missing transitive dependency may be waived.
- **Caps (A291):** copy `batches.HEADLINE.caps_per_case[case]` from DBP C2V004C (`$DBP_C` in B9b), **not** from C2V004B, into each GUARD014_FINAL_PLAN call's `wall_cap_s`, `rss_cap_bytes` and `output_cap_bytes`, and into FINAL_ADMISSION_CANDIDATE's `caps[case]`. `route_a_admission` and `case_order` are byte-identical between C2V004B and C2V004C (0276 item 2).

**STOP:** any PRELAUNCH refusal.

## B9b — Bind, then the caps check (sheet §9–10; 0276 items 2–3; A291)

```bash
DBP_C="$ART/h11_wall_ceiling_c3/C2V004C_FILL_20261022T093000Z/DIRECT_BATCH_PARAMS_S45_C2V004C.json"
DBP_C_SHA=ce9cbef8caaef8120377f302647c71d80387353d192d25d7d0b7e13e5872e809
GUARD014_FINAL_PLAN=   # PASTE: the root-written final plan
: "${GUARD014_FINAL_PLAN:?PASTE GUARD014_FINAL_PLAN}"
FINAL_ADMISSION_CANDIDATE=   # PASTE: the root-written final admission candidate
: "${FINAL_ADMISSION_CANDIDATE:?PASTE FINAL_ADMISSION_CANDIDATE}"
BOUND_PLAN=   # PASTE: a new path under $PACKET
: "${BOUND_PLAN:?PASTE BOUND_PLAN}"
BOUND_ADMISSION=   # PASTE: a new path under $PACKET
: "${BOUND_ADMISSION:?PASTE BOUND_ADMISSION}"
BOUND_COMMAND=   # PASTE: a new path under $PACKET
: "${BOUND_COMMAND:?PASTE BOUND_COMMAND}"
"$PY" -I -B "$ART/s1_successors_c2/step4_bind_c2v011.py" --final-plan "$GUARD014_FINAL_PLAN" --admission-candidate "$FINAL_ADMISSION_CANDIDATE" --plan-out "$BOUND_PLAN" --admission-out "$BOUND_ADMISSION" --command-out "$BOUND_COMMAND"
"$PY" -I -B "$ART/h11_wall_ceiling_c3/check_headline_caps_c3v001.py" "$DBP_C" "$DBP_C_SHA" "$BOUND_PLAN" "$BOUND_ADMISSION"
```

**Expected:** successful binder validation (S:L155). The check (`check_headline_caps_c3v001.py` sha256 `4efb810b`, 0276 L47) prints `HEADLINE caps == DBP C2V004C for 11 calls; wall_cap_s 3443340` (0276 item 3).

**STOP:** any binder refusal; any check failure (0276 item 3; A291).

## B10H — Integrity envelope START, phase HEADLINE11 (sheet §9–10)

**Wait for:** B9b passed. V006 must already hold every registration the phase needs, because collect reads it (S:L162).

```bash
set -euo pipefail
PHASE=HEADLINE11
E="$E_H11"
PHASE_SOURCE_ARGS=(   # PASTE: --doc-pin SHA PATH entries for the final run configs, plans, admission records and registered inputs, including the C1 pin with --scope "$C1" /tail_readiness and the registry pin
)
[ "${#PHASE_SOURCE_ARGS[@]}" -gt 0 ]
T="$ART/pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py"
V006="$CTRL/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md"
"$PY" -I -B "$T" collect --phase "$PHASE" --max-depth 0 "${PHASE_SOURCE_ARGS[@]}" --v006 "$V006" --out "$E/PINSET.json"
PINSET_SHA=$(shasum -a 256 "$E/PINSET.json" | cut -c1-64)
"$PY" -I -B "$T" snapshot --pins "$E/PINSET.json" --pins-sha256 "$PINSET_SHA" --label start --out "$E/START.json"
```

**Expected:** both commands exit 0 (S:L167). **STOP:** exit 3 INVALIDATE stops the phase. Preserve this same pinset for END; never re-collect. No chmod, hard link or GUI mutation of any input during the phase (S:L167).

## B10LH — HEADLINE11 launch — ROOT ACTION (sheet §9–10)

**Pre-conditions:** B10H passed; root's alert-only CPU/stage-mtime stall watch is running (S:L9).

Root independently publishes `UNT_STEP4_ADMISSION_PATH`/`SHA256`, verifies the generated command (`$BOUND_COMMAND`) and launches **that** command after START. Its executor is launcher015 `PLAN --execute-root-only`. Do not bypass the generated single-thread/nice/taskpolicy/lock environment; it is the launcher's own, not a §3–§8 command, so the A274 QoS drop does not touch it (S:L169).

**Expected:** the launcher detaches, so return 0 is not completion. Monitor the child receipts and root's non-content stall watch. HEADLINE11 max_active counts route-A only (A247) (S:L169).

**STOP:** any refusal. Every retry needs a new root ruling (S:L169); cap or infrastructure reruns wait for the adopted single launcher (A275, A282). No P112 launch on verdict day.

## B7S1 — S0 handoffs, all four (addendum §2; sheet §7)

**Wait for:** B4 (S0 needs §1–§4; A274 item 3). **Call:** P0 + this block (it includes the addendum preamble PJ). Branch S runs alongside Branch H (A263 P3).

```bash
set -euo pipefail
set -o noclobber
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
S0_LAUNCH_ROOT=/Users/bgm/Research/UNT_S0_LAUNCH_C2V003A
S0_RUN_ROOT=/Volumes/External1/NGC_S0_PHASE1_V001
S0_STAGE="$S0_LAUNCH_ROOT/prestage_J_CX3V001"
FILLER="$ART/step5_path_c2/tools/fill_step5_c2v001.py"
HANDOFF_TOOL="$ART/step5_path_c2/tools/phase1_point_handoffs_c2v001.py"
SERIAL_KIT="$ART/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh"
DRIVER="$ART/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py"
DRIVER_SHA=577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
[ -d "$S0_LAUNCH_ROOT" ]
[ -d "$S0_STAGE" ]
[ -d "$S0_STAGE/fills" ]
[ -d "$S0_STAGE/driver_plans" ]
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
ROOT_FIELDS=   # PASTE: root's actual §7 root-fields path (schema PHASE1_POINT_HANDOFF_ROOT_FIELDS_C2V001)
: "${ROOT_FIELDS:?root must supply actual root-fields path}"
ROOT_FIELDS_SHA=   # PASTE: its byte sha256
: "${ROOT_FIELDS_SHA:?root must supply actual root-fields byte SHA}"
[ "$(sha "$ROOT_FIELDS")" = "$ROOT_FIELDS_SHA" ]
"$PY" -I -B "$HANDOFF_TOOL"   --source "$ART/phase1_c2/S0_RECORD_ROOT_V001/S0_C2V001.json"   --source-sha256 1be5ed709cdb49106652beb76baaafc1c257e760d8cda2c62c18ea6fb2e88143   --root-fields "$ROOT_FIELDS" --root-fields-sha256 "$ROOT_FIELDS_SHA"   --out-dir "$S0_STAGE/handoffs"
J0_HANDOFF="$S0_STAGE/handoffs/HANDOFF_jacobian_first_attempt_0_3d7785669b549d6f_C2V001.json"
J1_HANDOFF="$S0_STAGE/handoffs/HANDOFF_jacobian_first_attempt_1_ab7bf95317b37652_C2V001.json"
J2_HANDOFF="$S0_STAGE/handoffs/HANDOFF_jacobian_first_attempt_2_4b9b4ec88eb2d94c_C2V001.json"
J0_HANDOFF_SHA=$(sha "$J0_HANDOFF")
J1_HANDOFF_SHA=$(sha "$J1_HANDOFF")
J2_HANDOFF_SHA=$(sha "$J2_HANDOFF")
printf 'HANDOFF_PIN S0_J0 %s %s\n' "$J0_HANDOFF_SHA" "$J0_HANDOFF"
printf 'HANDOFF_PIN S0_J1 %s %s\n' "$J1_HANDOFF_SHA" "$J1_HANDOFF"
printf 'HANDOFF_PIN S0_J2 %s %s\n' "$J2_HANDOFF_SHA" "$J2_HANDOFF"
```

**Expected:** the tool emits all four handoffs (seed and J0–J2) once into `$S0_STAGE/handoffs`, and the three printf lines print the exact HANDOFF_PIN lines (J:L50, L63-L65). If the seed branch already produced the four registered handoffs, reuse those exact paths; never recreate them or duplicate V006 pin lines (J:L50).

**Root action:** register the three expanded HANDOFF_PIN lines, plus HANDOFF_PIN S0_SEED (the seed handoff emitted by the same tool), WATCH_PIN MEMORY_WATCH and the V007 adoption pin to the verdict report (S:L124), under a real `## A<number>` V006 entry, **before filling** (RI45-09; J:L68). Use the exact whole-line grammar: no backticks, indentation, `sha256=`, `path=`, trailing spaces or shell variables (J:L68-L74). Check the point_key mapping J0 `3d778566…`, J1 `ab7bf953…`, J2 `4b9b4ec8…` against the S0 source (J:L76). Paths are canonical and avoid ngc3198, runs_ext and /tmp spellings (J:L76; S:L124).

**STOP:** any refusal; no invented verdict digest or pending certificate is acceptable (J:L50).

## B7S2 — J fills and J driver dry plans (addendum §3)

**Wait for:** B7S1 registrations recorded.

```bash
set -euo pipefail
set -o noclobber
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
S0_LAUNCH_ROOT=/Users/bgm/Research/UNT_S0_LAUNCH_C2V003A
S0_RUN_ROOT=/Volumes/External1/NGC_S0_PHASE1_V001
S0_STAGE="$S0_LAUNCH_ROOT/prestage_J_CX3V001"
FILLER="$ART/step5_path_c2/tools/fill_step5_c2v001.py"
HANDOFF_TOOL="$ART/step5_path_c2/tools/phase1_point_handoffs_c2v001.py"
SERIAL_KIT="$ART/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh"
DRIVER="$ART/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py"
DRIVER_SHA=577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
[ -d "$S0_LAUNCH_ROOT" ]
[ -d "$S0_STAGE" ]
[ -d "$S0_STAGE/fills" ]
[ -d "$S0_STAGE/driver_plans" ]
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
J0_HANDOFF="$S0_STAGE/handoffs/HANDOFF_jacobian_first_attempt_0_3d7785669b549d6f_C2V001.json"
J1_HANDOFF="$S0_STAGE/handoffs/HANDOFF_jacobian_first_attempt_1_ab7bf95317b37652_C2V001.json"
J2_HANDOFF="$S0_STAGE/handoffs/HANDOFF_jacobian_first_attempt_2_4b9b4ec88eb2d94c_C2V001.json"
J0_HANDOFF_SHA=$(sha "$J0_HANDOFF")
J1_HANDOFF_SHA=$(sha "$J1_HANDOFF")
J2_HANDOFF_SHA=$(sha "$J2_HANDOFF")
"$PY" -I -B "$FILLER" --handoff "$J0_HANDOFF" --expected-sha256 "$J0_HANDOFF_SHA" --output-dir "$S0_STAGE/fills/J0"
"$PY" -I -B "$FILLER" --handoff "$J1_HANDOFF" --expected-sha256 "$J1_HANDOFF_SHA" --output-dir "$S0_STAGE/fills/J1"
"$PY" -I -B "$FILLER" --handoff "$J2_HANDOFF" --expected-sha256 "$J2_HANDOFF_SHA" --output-dir "$S0_STAGE/fills/J2"
J0_SPEC="$S0_STAGE/fills/J0/CALL_A_K32_A2_HEADLINE_C2V001.json"
J1_SPEC="$S0_STAGE/fills/J1/CALL_A_K32_A2_HEADLINE_C2V001.json"
J2_SPEC="$S0_STAGE/fills/J2/CALL_A_K32_A2_HEADLINE_C2V001.json"
J0_SPEC_SHA=$(sha "$J0_SPEC")
J1_SPEC_SHA=$(sha "$J1_SPEC")
J2_SPEC_SHA=$(sha "$J2_SPEC")
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
[ "$(sha "$J0_SPEC")" = "$J0_SPEC_SHA" ]
"$PY" -I -B "$DRIVER" dry-run --spec "$J0_SPEC" --report-dir "$S0_STAGE/driver_plans/J0"
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
[ "$(sha "$J1_SPEC")" = "$J1_SPEC_SHA" ]
"$PY" -I -B "$DRIVER" dry-run --spec "$J1_SPEC" --report-dir "$S0_STAGE/driver_plans/J1"
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
[ "$(sha "$J2_SPEC")" = "$J2_SPEC_SHA" ]
"$PY" -I -B "$DRIVER" dry-run --spec "$J2_SPEC" --report-dir "$S0_STAGE/driver_plans/J2"
printf 'SPEC_PIN S0_J0_SERIAL %s %s\n' "$J0_SPEC_SHA" "$J0_SPEC"
printf 'SPEC_PIN S0_J1_SERIAL %s %s\n' "$J1_SPEC_SHA" "$J1_SPEC"
printf 'SPEC_PIN S0_J2_SERIAL %s %s\n' "$J2_SPEC_SHA" "$J2_SPEC"
```

**Expected:** three fills and three dry reports. These are sheet §7's driver dry-run interface with the A263/A274 QoS waiver (J:L101). Root checks the dry-plan blockers and the actual reports, not the exit code: zero executed scientific stages, no binding or source-build blocker, and only the allowed future `PENDING_ROUTE_A_OUTPUTS` dependency. Pin the reports from their bytes (J:L101). The fills include a twin per point; only J serial specs launch (J:L101).

**Root action:** after successful dry plans, register the three printed SPEC_PIN lines in the same final registration pass, before START and M-15 (J:L103, L111). Later kit fills must reproduce each registered serial SHA exactly (J:L111).

**STOP:** any blocker; with `set -e` the block stops at the first failing command.

## B7S3 — Seed kit DRY (sheet §11, dry form)

**Wait for:** B7S1 registrations. Default is DRY, no launch (S:L180).

```bash
set -euo pipefail
set -o noclobber
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
S0_LAUNCH_ROOT=/Users/bgm/Research/UNT_S0_LAUNCH_C2V003A
S0_RUN_ROOT=/Volumes/External1/NGC_S0_PHASE1_V001
S0_STAGE="$S0_LAUNCH_ROOT/prestage_J_CX3V001"
FILLER="$ART/step5_path_c2/tools/fill_step5_c2v001.py"
HANDOFF_TOOL="$ART/step5_path_c2/tools/phase1_point_handoffs_c2v001.py"
SERIAL_KIT="$ART/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh"
DRIVER="$ART/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py"
DRIVER_SHA=577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
[ -d "$S0_LAUNCH_ROOT" ]
[ -d "$S0_STAGE" ]
[ -d "$S0_STAGE/fills" ]
[ -d "$S0_STAGE/driver_plans" ]
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
STEP2_LAST_RECEIPT=   # PASTE: the actual last step-2 receipt (see gap G3)
: "${STEP2_LAST_RECEIPT:?PASTE STEP2_LAST_RECEIPT}"
/bin/bash "$ART/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh" seed --launch-root "$S0_LAUNCH_ROOT" --run-root /Volumes/External1/NGC_S0_PHASE1_V001 --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT"
```

**Expected:** a dry plan and fill under a unique `dry/S0_SEED_SERIAL_A1_<UTC>_<pid>` (J:L46 pattern). Root pins the seed's fresh filled serial spec and the seed twin spec, runs **B7X** for each, then registers SPEC_PIN S0_SEED_SERIAL and the twin spec in the same final registration pass as J's SPEC_PINs (S:L124; J:L103). The seed's fill comes from this kit DRY (gap G1). With no seed SPEC_PIN registered yet, the kit's fill-check reports `spec_pin_status` PENDING_V006_SPEC_PIN and still passes in DRY (kit L486-541: `spec_pin_present` is true in dry), so no flag is expected here.

**STOP:** any refusal or flag; exit 5 or a parse timeout means reconcile under the kit's rules (S:L180).

## B7X — Driver dry plan for the seed serial and seed twin specs (sheet §7)

**Call once per spec** (seed serial, seed twin); the calls can run at the same time (A263 P4).

```bash
set -euo pipefail
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
DRIVER="$ART/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py"
DRIVER_SHA=577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377
PIN_NAME=   # PASTE: S0_SEED_SERIAL for the serial spec, or S0_SEED_CW8_TWIN for the twin (kit L357)
: "${PIN_NAME:?PASTE PIN_NAME}"
FILLED_SPEC=   # PASTE: the seed serial spec, or the seed twin spec
: "${FILLED_SPEC:?PASTE FILLED_SPEC}"
FILLED_SPEC_SHA=   # PASTE: its sha256 from bytes
: "${FILLED_SPEC_SHA:?PASTE FILLED_SPEC_SHA}"
NEW_DRY_REPORT_DIR=   # PASTE: a new path
: "${NEW_DRY_REPORT_DIR:?PASTE NEW_DRY_REPORT_DIR}"
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
[ "$(sha "$FILLED_SPEC")" = "$FILLED_SPEC_SHA" ]
"$PY" -I -B "$DRIVER" dry-run --spec "$FILLED_SPEC" --report-dir "$NEW_DRY_REPORT_DIR"
printf 'SPEC_PIN %s %s %s\n' "$PIN_NAME" "$FILLED_SPEC_SHA" "$FILLED_SPEC"
```

**Expected and STOP:** as B7H (S:L132). The last line prints the exact SPEC_PIN line; root registers it in the same final pass as J's SPEC_PINs (S:L124; J:L103).

## B7S4 — J kit DRY and twin DRY (addendum §4; sheet §11 dry form)

**Wait for:** every SPEC_PIN registered (B7S2, B7S3 and B7X). The first line re-runs the seed DRY (S:L176) after the final registration pass, so the registered seed spec is checked before START: its fill-check must now read MATCHES_V006 (kit L543). `SEED_DRY_FILL_DIR` must be canonical and ngc3198-free, with no /tmp or runs_ext symlink spelling (S:L124).

```bash
set -euo pipefail
set -o noclobber
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
S0_LAUNCH_ROOT=/Users/bgm/Research/UNT_S0_LAUNCH_C2V003A
S0_RUN_ROOT=/Volumes/External1/NGC_S0_PHASE1_V001
S0_STAGE="$S0_LAUNCH_ROOT/prestage_J_CX3V001"
FILLER="$ART/step5_path_c2/tools/fill_step5_c2v001.py"
HANDOFF_TOOL="$ART/step5_path_c2/tools/phase1_point_handoffs_c2v001.py"
SERIAL_KIT="$ART/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh"
DRIVER="$ART/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py"
DRIVER_SHA=577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
[ -d "$S0_LAUNCH_ROOT" ]
[ -d "$S0_STAGE" ]
[ -d "$S0_STAGE/fills" ]
[ -d "$S0_STAGE/driver_plans" ]
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
STEP2_LAST_RECEIPT=   # PASTE: as in B7S3
: "${STEP2_LAST_RECEIPT:?PASTE STEP2_LAST_RECEIPT}"
SEED_DRY_FILL_DIR=   # PASTE: the seed DRY fill folder from B7S3
: "${SEED_DRY_FILL_DIR:?PASTE SEED_DRY_FILL_DIR}"
/bin/bash "$ART/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh" seed --launch-root "$S0_LAUNCH_ROOT" --run-root /Volumes/External1/NGC_S0_PHASE1_V001 --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT"
/bin/bash "$SERIAL_KIT" j0 --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1
/bin/bash "$SERIAL_KIT" j1 --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1
/bin/bash "$SERIAL_KIT" j2 --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1
/bin/bash "$ART/s0_launch_kit_c2/launch_twin_root_c2v003a.sh" --launch-root "$S0_LAUNCH_ROOT" --run-root /Volumes/External1/NGC_S0_PHASE1_V001 --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT" --dry-fill-dir "$SEED_DRY_FILL_DIR" --watch-poll-s 30
```

**Expected:** no `--launch` means DRY. A J DRY before seed M-15 reports the record pending, which is allowed only in DRY. Each must pass the handoff, fill and dry-verdict checks, show the same registered SPEC SHA, zero science stages and the planned caps and paths. Save and hash each resulting plan, fill-check and dry-verdict file from each J DRY's printed DRY_WORK location (J:L121). The seed and twin DRY outputs are whatever their own commands report.

**STOP:** any refusal or flag.

## B10S — Integrity envelope START, phase S0_SEED (sheet §9–10; addendum §4)

**Wait for:** B7S2, B7S3, B7X and B7S4 complete; all S0 registrations recorded. S0 does not wait for B5R/B6R or Branch H (A274 item 3).

```bash
set -euo pipefail
set -o noclobber
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
S0_LAUNCH_ROOT=/Users/bgm/Research/UNT_S0_LAUNCH_C2V003A
S0_RUN_ROOT=/Volumes/External1/NGC_S0_PHASE1_V001
S0_STAGE="$S0_LAUNCH_ROOT/prestage_J_CX3V001"
FILLER="$ART/step5_path_c2/tools/fill_step5_c2v001.py"
HANDOFF_TOOL="$ART/step5_path_c2/tools/phase1_point_handoffs_c2v001.py"
SERIAL_KIT="$ART/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh"
DRIVER="$ART/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py"
DRIVER_SHA=577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
[ -d "$S0_LAUNCH_ROOT" ]
[ -d "$S0_STAGE" ]
[ -d "$S0_STAGE/fills" ]
[ -d "$S0_STAGE/driver_plans" ]
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
J0_HANDOFF="$S0_STAGE/handoffs/HANDOFF_jacobian_first_attempt_0_3d7785669b549d6f_C2V001.json"
J1_HANDOFF="$S0_STAGE/handoffs/HANDOFF_jacobian_first_attempt_1_ab7bf95317b37652_C2V001.json"
J2_HANDOFF="$S0_STAGE/handoffs/HANDOFF_jacobian_first_attempt_2_4b9b4ec88eb2d94c_C2V001.json"
J0_HANDOFF_SHA=$(sha "$J0_HANDOFF")
J1_HANDOFF_SHA=$(sha "$J1_HANDOFF")
J2_HANDOFF_SHA=$(sha "$J2_HANDOFF")
J0_SPEC="$S0_STAGE/fills/J0/CALL_A_K32_A2_HEADLINE_C2V001.json"
J1_SPEC="$S0_STAGE/fills/J1/CALL_A_K32_A2_HEADLINE_C2V001.json"
J2_SPEC="$S0_STAGE/fills/J2/CALL_A_K32_A2_HEADLINE_C2V001.json"
J0_SPEC_SHA=$(sha "$J0_SPEC")
J1_SPEC_SHA=$(sha "$J1_SPEC")
J2_SPEC_SHA=$(sha "$J2_SPEC")
PHASE=S0_SEED
E="$E_S0"
SEED_HANDOFF=   # PASTE: the seed handoff among the four B7S1 emitted (registered HANDOFF_PIN S0_SEED)
: "${SEED_HANDOFF:?PASTE SEED_HANDOFF}"
SEED_HANDOFF_SHA=   # PASTE: its registered sha256
: "${SEED_HANDOFF_SHA:?PASTE SEED_HANDOFF_SHA}"
SEED_SPEC=   # PASTE: the registered seed serial spec (SPEC_PIN S0_SEED_SERIAL)
: "${SEED_SPEC:?PASTE SEED_SPEC}"
SEED_SPEC_SHA=   # PASTE: its registered sha256
: "${SEED_SPEC_SHA:?PASTE SEED_SPEC_SHA}"
TWIN_SPEC=   # PASTE: the registered seed twin spec (SPEC_PIN S0_SEED_CW8_TWIN; kit L357)
: "${TWIN_SPEC:?PASTE TWIN_SPEC}"
TWIN_SPEC_SHA=   # PASTE: its registered sha256
: "${TWIN_SPEC_SHA:?PASTE TWIN_SPEC_SHA}"
EXTRA_DOC_PINS=(   # PASTE: --doc-pin SHA PATH entries for the actual verdict binding, final metadata/plans/admissions, referenced inputs and the dry-report/plan pins; add a scoped C1/registry pin only if the S0 config carries tail_readiness
)
PHASE_SOURCE_ARGS=(
  --doc-pin 5e688882451824931f964e610cf17597d82ee0eb246fb0dce528ec0c6e148042 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/GATE_DOCUMENT_PINS_V002.json
  --doc-pin "$J0_HANDOFF_SHA" "$J0_HANDOFF" --doc-pin "$J0_SPEC_SHA" "$J0_SPEC"
  --doc-pin "$J1_HANDOFF_SHA" "$J1_HANDOFF" --doc-pin "$J1_SPEC_SHA" "$J1_SPEC"
  --doc-pin "$J2_HANDOFF_SHA" "$J2_HANDOFF" --doc-pin "$J2_SPEC_SHA" "$J2_SPEC"
  --doc-pin "$SEED_HANDOFF_SHA" "$SEED_HANDOFF" --doc-pin "$SEED_SPEC_SHA" "$SEED_SPEC" --doc-pin "$TWIN_SPEC_SHA" "$TWIN_SPEC"
  "${EXTRA_DOC_PINS[@]}"
)
[ "${#EXTRA_DOC_PINS[@]}" -gt 0 ]
T="$ART/pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py"
V006="$CTRL/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md"
"$PY" -I -B "$T" collect --phase "$PHASE" --max-depth 0 "${PHASE_SOURCE_ARGS[@]}" --v006 "$V006" --out "$E/PINSET.json"
PINSET_SHA=$(shasum -a 256 "$E/PINSET.json" | cut -c1-64)
"$PY" -I -B "$T" snapshot --pins "$E/PINSET.json" --pins-sha256 "$PINSET_SHA" --label start --out "$E/START.json"
```

**Expected and STOP:** as B10H (S:L167). Root keeps V006 byte-frozen from M-15 through the first launch receipt (J:L5).

## B11.1 — S0 first-attempt launch: seed (addendum §5) — ROOT ONLY

**Pre-conditions (J:L127):** step 2's last receipt exists; every gate and START passed; the registered passive watch is installed; current disk checks pass; root's alert-only stall watch is running (S:L9). Run this line only if the seed has not already launched through sheet §11; otherwise resume after its confirmed LAUNCH (J:L138). This call writes the M-15 record itself (kit `s0_prelaunch_record_c2v001.py` `a10965b7`; kit L23, L96-112) and then waits up to about 300 s for the launch receipt to parse (kit L37), so run it with timeout 600000 or in the background. **V006 freeze:** no V006 append by either branch from the start of this call until its confirmed launch record (J:L5; kit L34). **One call per invocation;** the next waits for this one's confirmed LAUNCH record.

```bash
set -euo pipefail
set -o noclobber
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
S0_LAUNCH_ROOT=/Users/bgm/Research/UNT_S0_LAUNCH_C2V003A
S0_RUN_ROOT=/Volumes/External1/NGC_S0_PHASE1_V001
S0_STAGE="$S0_LAUNCH_ROOT/prestage_J_CX3V001"
FILLER="$ART/step5_path_c2/tools/fill_step5_c2v001.py"
HANDOFF_TOOL="$ART/step5_path_c2/tools/phase1_point_handoffs_c2v001.py"
SERIAL_KIT="$ART/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh"
DRIVER="$ART/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py"
DRIVER_SHA=577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
[ -d "$S0_LAUNCH_ROOT" ]
[ -d "$S0_STAGE" ]
[ -d "$S0_STAGE/fills" ]
[ -d "$S0_STAGE/driver_plans" ]
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
STEP2_LAST_RECEIPT=   # PASTE: the actual last step-2 receipt
: "${STEP2_LAST_RECEIPT:?PASTE STEP2_LAST_RECEIPT}"
: "${STEP2_LAST_RECEIPT:?root must supply the actual last step-2 receipt}"
/bin/bash "$SERIAL_KIT" seed --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT" --launch
```

**Expected:** exit 0 with a confirmed LAUNCH record (run directory, receipt and launch-record paths as J:L140 lists). Exit 3 is a refusal; exit 4 is a flag for root review; exit 5 or a timeout requires reconciliation under the kit's stop rules (J:L127). A launch return is not completion; do not wait for scientific completion before the next confirmed launch (J:L127).

**Caps:** J first attempts keep wall 610324 s, RSS 137438953472 B and output 146028888064 B; the External1 free-space guard stays at 156 GiB per start (J:L138). S0 first attempts keep serial 610324 and twin 22752 (S:L8); A291 superseded only HEADLINE11's A248 exception.

**STOP:** any exit other than 0, or no confirmed LAUNCH record. Exit 5 or a parse timeout means reconcile or stop the qualified child under root's rule; never assume it died. Any cap, signal or root stop is nonphysics; never record a completed twin without explicit bound planned-stop evidence (S:L180). No automatic rerun; reruns wait for the adopted single launcher (A275, A282; J:L142). If the S0 twin is cut before iteration 1, root reruns it after H11, planned and uncounted (A271 item 2).

## B11.2 — S0 first-attempt launch: J0 (addendum §5) — ROOT ONLY

**Pre-conditions (J:L127):** step 2's last receipt exists; every gate and START passed; the registered passive watch is installed; current disk checks pass; root's alert-only stall watch is running (S:L9). **One call per invocation;** the next waits for this one's confirmed LAUNCH record.

```bash
set -euo pipefail
set -o noclobber
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
S0_LAUNCH_ROOT=/Users/bgm/Research/UNT_S0_LAUNCH_C2V003A
S0_RUN_ROOT=/Volumes/External1/NGC_S0_PHASE1_V001
S0_STAGE="$S0_LAUNCH_ROOT/prestage_J_CX3V001"
FILLER="$ART/step5_path_c2/tools/fill_step5_c2v001.py"
HANDOFF_TOOL="$ART/step5_path_c2/tools/phase1_point_handoffs_c2v001.py"
SERIAL_KIT="$ART/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh"
DRIVER="$ART/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py"
DRIVER_SHA=577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
[ -d "$S0_LAUNCH_ROOT" ]
[ -d "$S0_STAGE" ]
[ -d "$S0_STAGE/fills" ]
[ -d "$S0_STAGE/driver_plans" ]
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
STEP2_LAST_RECEIPT=   # PASTE: the actual last step-2 receipt
: "${STEP2_LAST_RECEIPT:?PASTE STEP2_LAST_RECEIPT}"
: "${STEP2_LAST_RECEIPT:?root must supply the actual last step-2 receipt}"
/bin/bash "$SERIAL_KIT" j0 --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT" --launch
```

**Expected:** exit 0 with a confirmed LAUNCH record (run directory, receipt and launch-record paths as J:L140 lists). Exit 3 is a refusal; exit 4 is a flag for root review; exit 5 or a timeout requires reconciliation under the kit's stop rules (J:L127). A launch return is not completion; do not wait for scientific completion before the next confirmed launch (J:L127).

**Caps:** J first attempts keep wall 610324 s, RSS 137438953472 B and output 146028888064 B; the External1 free-space guard stays at 156 GiB per start (J:L138). S0 first attempts keep serial 610324 and twin 22752 (S:L8); A291 superseded only HEADLINE11's A248 exception.

**STOP:** any exit other than 0, or no confirmed LAUNCH record. Exit 5 or a parse timeout means reconcile or stop the qualified child under root's rule; never assume it died. Any cap, signal or root stop is nonphysics; never record a completed twin without explicit bound planned-stop evidence (S:L180). No automatic rerun; reruns wait for the adopted single launcher (A275, A282; J:L142). If the S0 twin is cut before iteration 1, root reruns it after H11, planned and uncounted (A271 item 2).

## B11.3 — S0 first-attempt launch: J1 (addendum §5) — ROOT ONLY

**Pre-conditions (J:L127):** step 2's last receipt exists; every gate and START passed; the registered passive watch is installed; current disk checks pass; root's alert-only stall watch is running (S:L9). **One call per invocation;** the next waits for this one's confirmed LAUNCH record.

```bash
set -euo pipefail
set -o noclobber
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
S0_LAUNCH_ROOT=/Users/bgm/Research/UNT_S0_LAUNCH_C2V003A
S0_RUN_ROOT=/Volumes/External1/NGC_S0_PHASE1_V001
S0_STAGE="$S0_LAUNCH_ROOT/prestage_J_CX3V001"
FILLER="$ART/step5_path_c2/tools/fill_step5_c2v001.py"
HANDOFF_TOOL="$ART/step5_path_c2/tools/phase1_point_handoffs_c2v001.py"
SERIAL_KIT="$ART/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh"
DRIVER="$ART/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py"
DRIVER_SHA=577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
[ -d "$S0_LAUNCH_ROOT" ]
[ -d "$S0_STAGE" ]
[ -d "$S0_STAGE/fills" ]
[ -d "$S0_STAGE/driver_plans" ]
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
STEP2_LAST_RECEIPT=   # PASTE: the actual last step-2 receipt
: "${STEP2_LAST_RECEIPT:?PASTE STEP2_LAST_RECEIPT}"
: "${STEP2_LAST_RECEIPT:?root must supply the actual last step-2 receipt}"
/bin/bash "$SERIAL_KIT" j1 --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT" --launch
```

**Expected:** exit 0 with a confirmed LAUNCH record (run directory, receipt and launch-record paths as J:L140 lists). Exit 3 is a refusal; exit 4 is a flag for root review; exit 5 or a timeout requires reconciliation under the kit's stop rules (J:L127). A launch return is not completion; do not wait for scientific completion before the next confirmed launch (J:L127).

**Caps:** J first attempts keep wall 610324 s, RSS 137438953472 B and output 146028888064 B; the External1 free-space guard stays at 156 GiB per start (J:L138). S0 first attempts keep serial 610324 and twin 22752 (S:L8); A291 superseded only HEADLINE11's A248 exception.

**STOP:** any exit other than 0, or no confirmed LAUNCH record. Exit 5 or a parse timeout means reconcile or stop the qualified child under root's rule; never assume it died. Any cap, signal or root stop is nonphysics; never record a completed twin without explicit bound planned-stop evidence (S:L180). No automatic rerun; reruns wait for the adopted single launcher (A275, A282; J:L142). If the S0 twin is cut before iteration 1, root reruns it after H11, planned and uncounted (A271 item 2).

## B11.4 — S0 first-attempt launch: J2 (addendum §5) — ROOT ONLY

**Pre-conditions (J:L127):** step 2's last receipt exists; every gate and START passed; the registered passive watch is installed; current disk checks pass; root's alert-only stall watch is running (S:L9). **One call per invocation;** the next waits for this one's confirmed LAUNCH record.

```bash
set -euo pipefail
set -o noclobber
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
S0_LAUNCH_ROOT=/Users/bgm/Research/UNT_S0_LAUNCH_C2V003A
S0_RUN_ROOT=/Volumes/External1/NGC_S0_PHASE1_V001
S0_STAGE="$S0_LAUNCH_ROOT/prestage_J_CX3V001"
FILLER="$ART/step5_path_c2/tools/fill_step5_c2v001.py"
HANDOFF_TOOL="$ART/step5_path_c2/tools/phase1_point_handoffs_c2v001.py"
SERIAL_KIT="$ART/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh"
DRIVER="$ART/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py"
DRIVER_SHA=577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
[ -d "$S0_LAUNCH_ROOT" ]
[ -d "$S0_STAGE" ]
[ -d "$S0_STAGE/fills" ]
[ -d "$S0_STAGE/driver_plans" ]
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
STEP2_LAST_RECEIPT=   # PASTE: the actual last step-2 receipt
: "${STEP2_LAST_RECEIPT:?PASTE STEP2_LAST_RECEIPT}"
: "${STEP2_LAST_RECEIPT:?root must supply the actual last step-2 receipt}"
/bin/bash "$SERIAL_KIT" j2 --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT" --launch
```

**Expected:** exit 0 with a confirmed LAUNCH record (run directory, receipt and launch-record paths as J:L140 lists). Exit 3 is a refusal; exit 4 is a flag for root review; exit 5 or a timeout requires reconciliation under the kit's stop rules (J:L127). A launch return is not completion; do not wait for scientific completion before the next confirmed launch (J:L127).

**Caps:** J first attempts keep wall 610324 s, RSS 137438953472 B and output 146028888064 B; the External1 free-space guard stays at 156 GiB per start (J:L138). S0 first attempts keep serial 610324 and twin 22752 (S:L8); A291 superseded only HEADLINE11's A248 exception.

**STOP:** any exit other than 0, or no confirmed LAUNCH record. Exit 5 or a parse timeout means reconcile or stop the qualified child under root's rule; never assume it died. Any cap, signal or root stop is nonphysics; never record a completed twin without explicit bound planned-stop evidence (S:L180). No automatic rerun; reruns wait for the adopted single launcher (A275, A282; J:L142). If the S0 twin is cut before iteration 1, root reruns it after H11, planned and uncounted (A271 item 2).

## B11.5 — S0 first-attempt launch: twin (addendum §5) — ROOT ONLY

**Pre-conditions (J:L127):** step 2's last receipt exists; every gate and START passed; the registered passive watch is installed; current disk checks pass; root's alert-only stall watch is running (S:L9). The twin runs only after the seed's confirmed LAUNCH (A166; S:L180) and, per 0838, after J0–J2. It uses the seed's registered live fill, so no `--dry-fill-dir` (J:L138). Keep its iteration-1 planned-stop watch (J:L138). **One call per invocation;** the next waits for this one's confirmed LAUNCH record.

```bash
set -euo pipefail
set -o noclobber
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
S0_LAUNCH_ROOT=/Users/bgm/Research/UNT_S0_LAUNCH_C2V003A
S0_RUN_ROOT=/Volumes/External1/NGC_S0_PHASE1_V001
S0_STAGE="$S0_LAUNCH_ROOT/prestage_J_CX3V001"
FILLER="$ART/step5_path_c2/tools/fill_step5_c2v001.py"
HANDOFF_TOOL="$ART/step5_path_c2/tools/phase1_point_handoffs_c2v001.py"
SERIAL_KIT="$ART/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh"
DRIVER="$ART/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py"
DRIVER_SHA=577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
[ -d "$S0_LAUNCH_ROOT" ]
[ -d "$S0_STAGE" ]
[ -d "$S0_STAGE/fills" ]
[ -d "$S0_STAGE/driver_plans" ]
[ "$(sha "$DRIVER")" = "$DRIVER_SHA" ]
STEP2_LAST_RECEIPT=   # PASTE: the actual last step-2 receipt
: "${STEP2_LAST_RECEIPT:?PASTE STEP2_LAST_RECEIPT}"
: "${STEP2_LAST_RECEIPT:?root must supply the actual last step-2 receipt}"
/bin/bash "$ART/s0_launch_kit_c2/launch_twin_root_c2v003a.sh" --launch-root "$S0_LAUNCH_ROOT" --run-root "$S0_RUN_ROOT" --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT" --watch-poll-s 30 --launch
```

**Expected:** exit 0 with a confirmed LAUNCH record (run directory, receipt and launch-record paths as J:L140 lists). Exit 3 is a refusal; exit 4 is a flag for root review; exit 5 or a timeout requires reconciliation under the kit's stop rules (J:L127). A launch return is not completion; do not wait for scientific completion before the next confirmed launch (J:L127).

**Caps:** J first attempts keep wall 610324 s, RSS 137438953472 B and output 146028888064 B; the External1 free-space guard stays at 156 GiB per start (J:L138). S0 first attempts keep serial 610324 and twin 22752 (S:L8); A291 superseded only HEADLINE11's A248 exception.

**STOP:** any exit other than 0, or no confirmed LAUNCH record. Exit 5 or a parse timeout means reconcile or stop the qualified child under root's rule; never assume it died. Any cap, signal or root stop is nonphysics; never record a completed twin without explicit bound planned-stop evidence (S:L180). No automatic rerun; reruns wait for the adopted single launcher (A275, A282; J:L142). If the S0 twin is cut before iteration 1, root reruns it after H11, planned and uncounted (A271 item 2).

## X. Cross-reference — every code line and its source

Kinds:
- **VERBATIM:** the source line, unchanged.
- **QOS_DROPPED:** the source line without its `taskpolicy`/`nice` prefix (A274 item 1).
- **REDERIVED:** a source line repeated in a later call.
- **PASTE / PASTE_GUARD:** a runtime slot and its guard.
- **FIXED:** a value stated in a source.
- **DERIVED:** flagged in 0.6.
- **COMMENT:** a note only.

| RB line | Block | Kind | Source |
|---|---|---|---|
| 125 | P0 | REDERIVED | J:L12 |
| 126 | P0 | FIXED | V:L1 ("Source this at the S4T R3 receipt: `source <this file>`") |
| 127 | P0 | VERBATIM | S:L16 |
| 128 | P0 | VERBATIM | S:L17 |
| 129 | P0 | VERBATIM | S:L18 |
| 130 | P0 | VERBATIM | S:L19 |
| 131 | P0 | VERBATIM | S:L20 |
| 132 | P0 | VERBATIM | S:L21 |
| 133 | P0 | VERBATIM | S:L22 |
| 134 | P0 | VERBATIM | S:L23 |
| 135 | P0 | VERBATIM | S:L24 |
| 136 | P0 | VERBATIM | S:L25 |
| 137 | P0 | VERBATIM | S:L28 |
| 138 | P0 | VERBATIM | S:L29 |
| 150 | B1 | PASTE | S:L36 |
| 151 | B1 | PASTE_GUARD | J:L53 guard form |
| 152 | B1 | VERBATIM | S:L39 |
| 153 | B1 | VERBATIM | S:L40 |
| 154 | B1 | VERBATIM | S:L41 |
| 155 | B1 | VERBATIM | S:L42 |
| 156 | B1 | VERBATIM | S:L43 |
| 157 | B1 | VERBATIM | S:L44 |
| 158 | B1 | VERBATIM | S:L45 |
| 159 | B1 | VERBATIM | S:L46 |
| 160 | B1 | VERBATIM | S:L47 |
| 161 | B1 | VERBATIM | S:L48 |
| 186 | B3a | PASTE | S:L32 |
| 187 | B3a | PASTE_GUARD | J:L53 guard form |
| 188 | B3a | PASTE | S:L61 |
| 189 | B3a | PASTE_GUARD | J:L53 guard form |
| 190 | B3a | PASTE | S:L61 |
| 191 | B3a | PASTE_GUARD | J:L53 guard form |
| 192 | B3a | QOS_DROPPED | S:L64 minus its taskpolicy/nice prefix (A274 item 1) |
| 193 | B3a | QOS_DROPPED | S:L65 minus its taskpolicy/nice prefix (A274 item 1) |
| 203 | B3b | PASTE | S:L32 |
| 204 | B3b | PASTE_GUARD | J:L53 guard form |
| 205 | B3b | PASTE | S:L55 |
| 206 | B3b | PASTE_GUARD | J:L53 guard form |
| 207 | B3b | QOS_DROPPED | S:L67 minus its taskpolicy/nice prefix (A274 item 1) |
| 208 | B3b | QOS_DROPPED | S:L68 minus its taskpolicy/nice prefix (A274 item 1) |
| 209 | B3b | QOS_DROPPED | S:L69 minus its taskpolicy/nice prefix (A274 item 1) |
| 219 | B3c | PASTE | S:L32 |
| 220 | B3c | PASTE_GUARD | J:L53 guard form |
| 221 | B3c | PASTE | S:L72 |
| 222 | B3c | PASTE_GUARD | J:L53 guard form |
| 223 | B3c | QOS_DROPPED | S:L66 minus its taskpolicy/nice prefix (A274 item 1) |
| 235 | B4 | PASTE | S:L32 |
| 236 | B4 | PASTE_GUARD | J:L53 guard form |
| 237 | B4 | PASTE | S:L55 |
| 238 | B4 | PASTE_GUARD | J:L53 guard form |
| 239 | B4 | PASTE | S:L13 (all new paths must be unused) |
| 240 | B4 | PASTE_GUARD | J:L53 guard form |
| 241 | B4 | QOS_DROPPED | S:L79 minus its taskpolicy/nice prefix (A274 item 1) |
| 242 | B4 | VERBATIM | S:L80 |
| 243 | B4 | VERBATIM | S:L81 |
| 244 | B4 | DERIVED | D2: display for publication (S:L84 "publish verdict path and byte SHA"); printf form of J:L63 |
| 258 | B5a | PASTE | S:L79 |
| 259 | B5a | PASTE_GUARD | J:L53 guard form |
| 260 | B5a | REDERIVED | S:L80 |
| 261 | B5a | REDERIVED | S:L81 |
| 262 | B5a | VERBATIM | S:L89 |
| 263 | B5a | QOS_DROPPED | S:L90 minus its taskpolicy/nice prefix (A274 item 1) |
| 273 | B5b | PASTE | S:L79 |
| 274 | B5b | PASTE_GUARD | J:L53 guard form |
| 275 | B5b | REDERIVED | S:L80 |
| 276 | B5b | REDERIVED | S:L81 |
| 277 | B5b | REDERIVED | S:L89 |
| 278 | B5b | QOS_DROPPED | S:L92 minus its taskpolicy/nice prefix (A274 item 1) |
| 288 | B5c | VERBATIM | S:L98 |
| 289 | B5c | VERBATIM | S:L99 |
| 290 | B5c | VERBATIM | S:L100 |
| 291 | B5c | VERBATIM | S:L101 |
| 292 | B5c | VERBATIM | S:L102 |
| 293 | B5c | VERBATIM | S:L103 |
| 294 | B5c | VERBATIM | S:L104 |
| 295 | B5c | VERBATIM | S:L105 |
| 296 | B5c | VERBATIM | S:L106 |
| 314 | B6 | PASTE | S:L79 |
| 315 | B6 | PASTE_GUARD | J:L53 guard form |
| 316 | B6 | REDERIVED | S:L80 |
| 317 | B6 | PASTE | S:L114 |
| 318 | B6 | PASTE_GUARD | J:L53 guard form |
| 319 | B6 | VERBATIM | S:L114 |
| 320 | B6 | VERBATIM | S:L115 |
| 321 | B6 | VERBATIM | S:L116 |
| 322 | B6 | VERBATIM | S:L117 |
| 340 | B8a | PASTE | S:L136 |
| 341 | B8a | PASTE_GUARD | J:L53 guard form |
| 342 | B8a | COMMENT |  |
| 343 | B8a | REDERIVED | S:L115 |
| 344 | B8a | REDERIVED | S:L116 |
| 345 | B8a | VERBATIM | S:L139 |
| 346 | B8a | VERBATIM | S:L140 |
| 354 | B8b | PASTE | S:L141; S:L27 |
| 355 | B8b | PASTE_GUARD | J:L53 guard form |
| 356 | B8b | PASTE | S:L141; S:L27 |
| 357 | B8b | PASTE_GUARD | J:L53 guard form |
| 358 | B8b | PASTE | S:L105, L109 |
| 359 | B8b | PASTE_GUARD | J:L53 guard form |
| 360 | B8b | PASTE | S:L141; S:L13 |
| 361 | B8b | PASTE_GUARD | J:L53 guard form |
| 362 | B8b | FIXED | S:L144 (the comma-separated string given there) |
| 363 | B8b | REDERIVED | S:L99 |
| 364 | B8b | DERIVED | D3: S:L144 "Compute H1_CONFIG_SHA from the newly written bytes before the producer call"; form of S:L81 |
| 365 | B8b | VERBATIM | S:L141 |
| 391 | B7H | REDERIVED | J:L12 |
| 392 | B7H | REDERIVED | J:L24 |
| 393 | B7H | PASTE | S:L132 |
| 394 | B7H | PASTE_GUARD | J:L53 guard form |
| 395 | B7H | PASTE | S:L132 |
| 396 | B7H | PASTE_GUARD | J:L53 guard form |
| 397 | B7H | PASTE | S:L126 |
| 398 | B7H | PASTE_GUARD | J:L53 guard form |
| 399 | B7H | PASTE | S:L132 |
| 400 | B7H | PASTE_GUARD | J:L53 guard form |
| 401 | B7H | PASTE | S:L126; J:L44 |
| 402 | B7H | PASTE_GUARD | J:L53 guard form |
| 403 | B7H | REDERIVED | J:L90 |
| 404 | B7H | DERIVED | D4: S:L132 "Hash driver and filled spec before it"; form of J:L91 |
| 405 | B7H | QOS_DROPPED | S:L129 minus its taskpolicy/nice prefix (A274 item 1) |
| 417 | B9a | VERBATIM | M:L34 |
| 418 | B9a | VERBATIM | M:L35 |
| 419 | B9a | PASTE | S:L151 |
| 420 | B9a | PASTE_GUARD | J:L53 guard form |
| 421 | B9a | PASTE | S:L151 |
| 422 | B9a | PASTE_GUARD | J:L53 guard form |
| 423 | B9a | PASTE | S:L151; S:L11 |
| 424 | B9a | PASTE_GUARD | J:L53 guard form |
| 425 | B9a | PASTE | S:L151 |
| 426 | B9a | PASTE_GUARD | J:L53 guard form |
| 427 | B9a | COMMENT |  |
| 428 | B9a | VERBATIM | S:L151 |
| 443 | B9b | REDERIVED | M:L34 |
| 444 | B9b | REDERIVED | M:L35 |
| 445 | B9b | PASTE | S:L152 |
| 446 | B9b | PASTE_GUARD | J:L53 guard form |
| 447 | B9b | PASTE | S:L152 |
| 448 | B9b | PASTE_GUARD | J:L53 guard form |
| 449 | B9b | PASTE | S:L152; V:L14 |
| 450 | B9b | PASTE_GUARD | J:L53 guard form |
| 451 | B9b | PASTE | S:L152; V:L14 |
| 452 | B9b | PASTE_GUARD | J:L53 guard form |
| 453 | B9b | PASTE | S:L152; V:L14 |
| 454 | B9b | PASTE_GUARD | J:L53 guard form |
| 455 | B9b | VERBATIM | S:L152 |
| 456 | B9b | VERBATIM | M:L45 |
| 468 | B10H | REDERIVED | J:L12 |
| 469 | B10H | FIXED | S:L157 (each phase separately) |
| 470 | B10H | FIXED | V:L10 |
| 471 | B10H | PASTE | S:L167 |
| 472 | B10H | FIXED | S:L167 |
| 473 | B10H | DERIVED | D5: S:L167 "an empty array is not a phase envelope" |
| 474 | B10H | VERBATIM | S:L160 |
| 475 | B10H | VERBATIM | S:L161 |
| 476 | B10H | VERBATIM | S:L162 |
| 477 | B10H | VERBATIM | S:L163 |
| 478 | B10H | VERBATIM | S:L164 |
| 498 | B7S1 | VERBATIM | J:L12 |
| 499 | B7S1 | VERBATIM | J:L13 |
| 500 | B7S1 | VERBATIM | J:L14 |
| 501 | B7S1 | VERBATIM | J:L15 |
| 502 | B7S1 | VERBATIM | J:L16 |
| 503 | B7S1 | VERBATIM | J:L17 |
| 504 | B7S1 | VERBATIM | J:L18 |
| 505 | B7S1 | VERBATIM | J:L19 |
| 506 | B7S1 | VERBATIM | J:L20 |
| 507 | B7S1 | VERBATIM | J:L21 |
| 508 | B7S1 | VERBATIM | J:L22 |
| 509 | B7S1 | VERBATIM | J:L23 |
| 510 | B7S1 | VERBATIM | J:L24 |
| 511 | B7S1 | VERBATIM | J:L25 |
| 512 | B7S1 | VERBATIM | J:L26 |
| 513 | B7S1 | VERBATIM | J:L27 |
| 514 | B7S1 | DERIVED | D1: replaces J:L28 mkdir (A276 pre-created it; J:L27 check form) |
| 515 | B7S1 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 516 | B7S1 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 517 | B7S1 | VERBATIM | J:L30 |
| 518 | B7S1 | PASTE | J:L50 |
| 519 | B7S1 | VERBATIM | J:L53 |
| 520 | B7S1 | PASTE | J:L50 |
| 521 | B7S1 | VERBATIM | J:L54 |
| 522 | B7S1 | VERBATIM | J:L55 |
| 523 | B7S1 | VERBATIM | J:L56 |
| 524 | B7S1 | VERBATIM | J:L57 |
| 525 | B7S1 | VERBATIM | J:L58 |
| 526 | B7S1 | VERBATIM | J:L59 |
| 527 | B7S1 | VERBATIM | J:L60 |
| 528 | B7S1 | VERBATIM | J:L61 |
| 529 | B7S1 | VERBATIM | J:L62 |
| 530 | B7S1 | VERBATIM | J:L63 |
| 531 | B7S1 | VERBATIM | J:L64 |
| 532 | B7S1 | VERBATIM | J:L65 |
| 546 | B7S2 | VERBATIM | J:L12 |
| 547 | B7S2 | VERBATIM | J:L13 |
| 548 | B7S2 | VERBATIM | J:L14 |
| 549 | B7S2 | VERBATIM | J:L15 |
| 550 | B7S2 | VERBATIM | J:L16 |
| 551 | B7S2 | VERBATIM | J:L17 |
| 552 | B7S2 | VERBATIM | J:L18 |
| 553 | B7S2 | VERBATIM | J:L19 |
| 554 | B7S2 | VERBATIM | J:L20 |
| 555 | B7S2 | VERBATIM | J:L21 |
| 556 | B7S2 | VERBATIM | J:L22 |
| 557 | B7S2 | VERBATIM | J:L23 |
| 558 | B7S2 | VERBATIM | J:L24 |
| 559 | B7S2 | VERBATIM | J:L25 |
| 560 | B7S2 | VERBATIM | J:L26 |
| 561 | B7S2 | VERBATIM | J:L27 |
| 562 | B7S2 | DERIVED | D1: replaces J:L28 mkdir (A276 pre-created it; J:L27 check form) |
| 563 | B7S2 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 564 | B7S2 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 565 | B7S2 | VERBATIM | J:L30 |
| 566 | B7S2 | REDERIVED | J:L57 |
| 567 | B7S2 | REDERIVED | J:L58 |
| 568 | B7S2 | REDERIVED | J:L59 |
| 569 | B7S2 | REDERIVED | J:L60 |
| 570 | B7S2 | REDERIVED | J:L61 |
| 571 | B7S2 | REDERIVED | J:L62 |
| 572 | B7S2 | VERBATIM | J:L81 |
| 573 | B7S2 | VERBATIM | J:L82 |
| 574 | B7S2 | VERBATIM | J:L83 |
| 575 | B7S2 | VERBATIM | J:L84 |
| 576 | B7S2 | VERBATIM | J:L85 |
| 577 | B7S2 | VERBATIM | J:L86 |
| 578 | B7S2 | VERBATIM | J:L87 |
| 579 | B7S2 | VERBATIM | J:L88 |
| 580 | B7S2 | VERBATIM | J:L89 |
| 581 | B7S2 | VERBATIM | J:L90 |
| 582 | B7S2 | VERBATIM | J:L91 |
| 583 | B7S2 | VERBATIM | J:L92 |
| 584 | B7S2 | VERBATIM | J:L93 |
| 585 | B7S2 | VERBATIM | J:L94 |
| 586 | B7S2 | VERBATIM | J:L95 |
| 587 | B7S2 | VERBATIM | J:L96 |
| 588 | B7S2 | VERBATIM | J:L97 |
| 589 | B7S2 | VERBATIM | J:L98 |
| 590 | B7S2 | VERBATIM | J:L106 |
| 591 | B7S2 | VERBATIM | J:L107 |
| 592 | B7S2 | VERBATIM | J:L108 |
| 606 | B7S3 | VERBATIM | J:L12 |
| 607 | B7S3 | VERBATIM | J:L13 |
| 608 | B7S3 | VERBATIM | J:L14 |
| 609 | B7S3 | VERBATIM | J:L15 |
| 610 | B7S3 | VERBATIM | J:L16 |
| 611 | B7S3 | VERBATIM | J:L17 |
| 612 | B7S3 | VERBATIM | J:L18 |
| 613 | B7S3 | VERBATIM | J:L19 |
| 614 | B7S3 | VERBATIM | J:L20 |
| 615 | B7S3 | VERBATIM | J:L21 |
| 616 | B7S3 | VERBATIM | J:L22 |
| 617 | B7S3 | VERBATIM | J:L23 |
| 618 | B7S3 | VERBATIM | J:L24 |
| 619 | B7S3 | VERBATIM | J:L25 |
| 620 | B7S3 | VERBATIM | J:L26 |
| 621 | B7S3 | VERBATIM | J:L27 |
| 622 | B7S3 | DERIVED | D1: replaces J:L28 mkdir (A276 pre-created it; J:L27 check form) |
| 623 | B7S3 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 624 | B7S3 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 625 | B7S3 | VERBATIM | J:L30 |
| 626 | B7S3 | PASTE | S:L176; J:L130 |
| 627 | B7S3 | PASTE_GUARD | J:L53 guard form |
| 628 | B7S3 | VERBATIM | S:L176 |
| 640 | B7X | REDERIVED | J:L12 |
| 641 | B7X | REDERIVED | J:L24 |
| 642 | B7X | REDERIVED | J:L22 |
| 643 | B7X | REDERIVED | J:L23 |
| 644 | B7X | PASTE | S:L124 |
| 645 | B7X | PASTE_GUARD | J:L53 guard form |
| 646 | B7X | PASTE | S:L126 |
| 647 | B7X | PASTE_GUARD | J:L53 guard form |
| 648 | B7X | PASTE | S:L132 |
| 649 | B7X | PASTE_GUARD | J:L53 guard form |
| 650 | B7X | PASTE | S:L126 |
| 651 | B7X | PASTE_GUARD | J:L53 guard form |
| 652 | B7X | REDERIVED | J:L90 |
| 653 | B7X | DERIVED | D4 (as in B7H) |
| 654 | B7X | QOS_DROPPED | S:L129 minus its taskpolicy/nice prefix (A274 item 1) |
| 655 | B7X | DERIVED | D7: J:L106 printf form; pin names from kit L357 (S0_%s_SERIAL, S0_SEED_CW8_TWIN) |
| 665 | B7S4 | VERBATIM | J:L12 |
| 666 | B7S4 | VERBATIM | J:L13 |
| 667 | B7S4 | VERBATIM | J:L14 |
| 668 | B7S4 | VERBATIM | J:L15 |
| 669 | B7S4 | VERBATIM | J:L16 |
| 670 | B7S4 | VERBATIM | J:L17 |
| 671 | B7S4 | VERBATIM | J:L18 |
| 672 | B7S4 | VERBATIM | J:L19 |
| 673 | B7S4 | VERBATIM | J:L20 |
| 674 | B7S4 | VERBATIM | J:L21 |
| 675 | B7S4 | VERBATIM | J:L22 |
| 676 | B7S4 | VERBATIM | J:L23 |
| 677 | B7S4 | VERBATIM | J:L24 |
| 678 | B7S4 | VERBATIM | J:L25 |
| 679 | B7S4 | VERBATIM | J:L26 |
| 680 | B7S4 | VERBATIM | J:L27 |
| 681 | B7S4 | DERIVED | D1: replaces J:L28 mkdir (A276 pre-created it; J:L27 check form) |
| 682 | B7S4 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 683 | B7S4 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 684 | B7S4 | VERBATIM | J:L30 |
| 685 | B7S4 | PASTE | S:L177 |
| 686 | B7S4 | PASTE_GUARD | J:L53 guard form |
| 687 | B7S4 | PASTE | S:L177 |
| 688 | B7S4 | PASTE_GUARD | J:L53 guard form |
| 689 | B7S4 | REDERIVED | S:L176 |
| 690 | B7S4 | VERBATIM | J:L116 |
| 691 | B7S4 | VERBATIM | J:L117 |
| 692 | B7S4 | VERBATIM | J:L118 |
| 693 | B7S4 | VERBATIM | S:L177 |
| 705 | B10S | VERBATIM | J:L12 |
| 706 | B10S | VERBATIM | J:L13 |
| 707 | B10S | VERBATIM | J:L14 |
| 708 | B10S | VERBATIM | J:L15 |
| 709 | B10S | VERBATIM | J:L16 |
| 710 | B10S | VERBATIM | J:L17 |
| 711 | B10S | VERBATIM | J:L18 |
| 712 | B10S | VERBATIM | J:L19 |
| 713 | B10S | VERBATIM | J:L20 |
| 714 | B10S | VERBATIM | J:L21 |
| 715 | B10S | VERBATIM | J:L22 |
| 716 | B10S | VERBATIM | J:L23 |
| 717 | B10S | VERBATIM | J:L24 |
| 718 | B10S | VERBATIM | J:L25 |
| 719 | B10S | VERBATIM | J:L26 |
| 720 | B10S | VERBATIM | J:L27 |
| 721 | B10S | DERIVED | D1: replaces J:L28 mkdir (A276 pre-created it; J:L27 check form) |
| 722 | B10S | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 723 | B10S | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 724 | B10S | VERBATIM | J:L30 |
| 725 | B10S | REDERIVED | J:L57 |
| 726 | B10S | REDERIVED | J:L58 |
| 727 | B10S | REDERIVED | J:L59 |
| 728 | B10S | REDERIVED | J:L60 |
| 729 | B10S | REDERIVED | J:L61 |
| 730 | B10S | REDERIVED | J:L62 |
| 731 | B10S | REDERIVED | J:L84 |
| 732 | B10S | REDERIVED | J:L85 |
| 733 | B10S | REDERIVED | J:L86 |
| 734 | B10S | REDERIVED | J:L87 |
| 735 | B10S | REDERIVED | J:L88 |
| 736 | B10S | REDERIVED | J:L89 |
| 737 | B10S | FIXED | S:L157; J:L123 |
| 738 | B10S | FIXED | V:L9; J:L123 |
| 739 | B10S | PASTE | S:L124; J:L50 |
| 740 | B10S | PASTE_GUARD | J:L53 guard form |
| 741 | B10S | PASTE | S:L124 |
| 742 | B10S | PASTE_GUARD | J:L53 guard form |
| 743 | B10S | PASTE | S:L124 |
| 744 | B10S | PASTE_GUARD | J:L53 guard form |
| 745 | B10S | PASTE | S:L124 |
| 746 | B10S | PASTE_GUARD | J:L53 guard form |
| 747 | B10S | PASTE | S:L124 |
| 748 | B10S | PASTE_GUARD | J:L53 guard form |
| 749 | B10S | PASTE | S:L124 |
| 750 | B10S | PASTE_GUARD | J:L53 guard form |
| 751 | B10S | PASTE | J:L123; S:L167 |
| 752 | B10S | FIXED | J:L123 |
| 753 | B10S | FIXED | S:L167 |
| 754 | B10S | FIXED | S:L167 (gate document and its sha); path from the envelope README L91 (that README is pinned in S's annex) |
| 755 | B10S | DERIVED | D6: J:L123 form with n=0 |
| 756 | B10S | DERIVED | D6: J:L123 form with n=1 |
| 757 | B10S | DERIVED | D6: J:L123 form with n=2 |
| 758 | B10S | DERIVED | D6: the same form for the seed and the seed twin (S:L124; J:L123 "all four final handoffs/serial specs, seed-twin spec") |
| 759 | B10S | DERIVED | D6 |
| 760 | B10S | FIXED | S:L167 |
| 761 | B10S | DERIVED | D5: S:L167 "an empty array is not a phase envelope"; under PJ set -e |
| 762 | B10S | VERBATIM | S:L160 |
| 763 | B10S | VERBATIM | S:L161 |
| 764 | B10S | VERBATIM | S:L162 |
| 765 | B10S | VERBATIM | S:L163 |
| 766 | B10S | VERBATIM | S:L164 |
| 776 | B11.1 | VERBATIM | J:L12 |
| 777 | B11.1 | VERBATIM | J:L13 |
| 778 | B11.1 | VERBATIM | J:L14 |
| 779 | B11.1 | VERBATIM | J:L15 |
| 780 | B11.1 | VERBATIM | J:L16 |
| 781 | B11.1 | VERBATIM | J:L17 |
| 782 | B11.1 | VERBATIM | J:L18 |
| 783 | B11.1 | VERBATIM | J:L19 |
| 784 | B11.1 | VERBATIM | J:L20 |
| 785 | B11.1 | VERBATIM | J:L21 |
| 786 | B11.1 | VERBATIM | J:L22 |
| 787 | B11.1 | VERBATIM | J:L23 |
| 788 | B11.1 | VERBATIM | J:L24 |
| 789 | B11.1 | VERBATIM | J:L25 |
| 790 | B11.1 | VERBATIM | J:L26 |
| 791 | B11.1 | VERBATIM | J:L27 |
| 792 | B11.1 | DERIVED | D1: replaces J:L28 mkdir (A276 pre-created it; J:L27 check form) |
| 793 | B11.1 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 794 | B11.1 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 795 | B11.1 | VERBATIM | J:L30 |
| 796 | B11.1 | PASTE | J:L130 |
| 797 | B11.1 | PASTE_GUARD | J:L53 guard form |
| 798 | B11.1 | VERBATIM | J:L130 |
| 799 | B11.1 | VERBATIM | J:L131 |
| 813 | B11.2 | VERBATIM | J:L12 |
| 814 | B11.2 | VERBATIM | J:L13 |
| 815 | B11.2 | VERBATIM | J:L14 |
| 816 | B11.2 | VERBATIM | J:L15 |
| 817 | B11.2 | VERBATIM | J:L16 |
| 818 | B11.2 | VERBATIM | J:L17 |
| 819 | B11.2 | VERBATIM | J:L18 |
| 820 | B11.2 | VERBATIM | J:L19 |
| 821 | B11.2 | VERBATIM | J:L20 |
| 822 | B11.2 | VERBATIM | J:L21 |
| 823 | B11.2 | VERBATIM | J:L22 |
| 824 | B11.2 | VERBATIM | J:L23 |
| 825 | B11.2 | VERBATIM | J:L24 |
| 826 | B11.2 | VERBATIM | J:L25 |
| 827 | B11.2 | VERBATIM | J:L26 |
| 828 | B11.2 | VERBATIM | J:L27 |
| 829 | B11.2 | DERIVED | D1: replaces J:L28 mkdir (A276 pre-created it; J:L27 check form) |
| 830 | B11.2 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 831 | B11.2 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 832 | B11.2 | VERBATIM | J:L30 |
| 833 | B11.2 | PASTE | J:L130 |
| 834 | B11.2 | PASTE_GUARD | J:L53 guard form |
| 835 | B11.2 | VERBATIM | J:L130 |
| 836 | B11.2 | VERBATIM | J:L132 |
| 850 | B11.3 | VERBATIM | J:L12 |
| 851 | B11.3 | VERBATIM | J:L13 |
| 852 | B11.3 | VERBATIM | J:L14 |
| 853 | B11.3 | VERBATIM | J:L15 |
| 854 | B11.3 | VERBATIM | J:L16 |
| 855 | B11.3 | VERBATIM | J:L17 |
| 856 | B11.3 | VERBATIM | J:L18 |
| 857 | B11.3 | VERBATIM | J:L19 |
| 858 | B11.3 | VERBATIM | J:L20 |
| 859 | B11.3 | VERBATIM | J:L21 |
| 860 | B11.3 | VERBATIM | J:L22 |
| 861 | B11.3 | VERBATIM | J:L23 |
| 862 | B11.3 | VERBATIM | J:L24 |
| 863 | B11.3 | VERBATIM | J:L25 |
| 864 | B11.3 | VERBATIM | J:L26 |
| 865 | B11.3 | VERBATIM | J:L27 |
| 866 | B11.3 | DERIVED | D1: replaces J:L28 mkdir (A276 pre-created it; J:L27 check form) |
| 867 | B11.3 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 868 | B11.3 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 869 | B11.3 | VERBATIM | J:L30 |
| 870 | B11.3 | PASTE | J:L130 |
| 871 | B11.3 | PASTE_GUARD | J:L53 guard form |
| 872 | B11.3 | VERBATIM | J:L130 |
| 873 | B11.3 | VERBATIM | J:L133 |
| 887 | B11.4 | VERBATIM | J:L12 |
| 888 | B11.4 | VERBATIM | J:L13 |
| 889 | B11.4 | VERBATIM | J:L14 |
| 890 | B11.4 | VERBATIM | J:L15 |
| 891 | B11.4 | VERBATIM | J:L16 |
| 892 | B11.4 | VERBATIM | J:L17 |
| 893 | B11.4 | VERBATIM | J:L18 |
| 894 | B11.4 | VERBATIM | J:L19 |
| 895 | B11.4 | VERBATIM | J:L20 |
| 896 | B11.4 | VERBATIM | J:L21 |
| 897 | B11.4 | VERBATIM | J:L22 |
| 898 | B11.4 | VERBATIM | J:L23 |
| 899 | B11.4 | VERBATIM | J:L24 |
| 900 | B11.4 | VERBATIM | J:L25 |
| 901 | B11.4 | VERBATIM | J:L26 |
| 902 | B11.4 | VERBATIM | J:L27 |
| 903 | B11.4 | DERIVED | D1: replaces J:L28 mkdir (A276 pre-created it; J:L27 check form) |
| 904 | B11.4 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 905 | B11.4 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 906 | B11.4 | VERBATIM | J:L30 |
| 907 | B11.4 | PASTE | J:L130 |
| 908 | B11.4 | PASTE_GUARD | J:L53 guard form |
| 909 | B11.4 | VERBATIM | J:L130 |
| 910 | B11.4 | VERBATIM | J:L134 |
| 924 | B11.5 | VERBATIM | J:L12 |
| 925 | B11.5 | VERBATIM | J:L13 |
| 926 | B11.5 | VERBATIM | J:L14 |
| 927 | B11.5 | VERBATIM | J:L15 |
| 928 | B11.5 | VERBATIM | J:L16 |
| 929 | B11.5 | VERBATIM | J:L17 |
| 930 | B11.5 | VERBATIM | J:L18 |
| 931 | B11.5 | VERBATIM | J:L19 |
| 932 | B11.5 | VERBATIM | J:L20 |
| 933 | B11.5 | VERBATIM | J:L21 |
| 934 | B11.5 | VERBATIM | J:L22 |
| 935 | B11.5 | VERBATIM | J:L23 |
| 936 | B11.5 | VERBATIM | J:L24 |
| 937 | B11.5 | VERBATIM | J:L25 |
| 938 | B11.5 | VERBATIM | J:L26 |
| 939 | B11.5 | VERBATIM | J:L27 |
| 940 | B11.5 | DERIVED | D1: replaces J:L28 mkdir (A276 pre-created it; J:L27 check form) |
| 941 | B11.5 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 942 | B11.5 | DERIVED | D1: replaces J:L29 mkdir (A276) |
| 943 | B11.5 | VERBATIM | J:L30 |
| 944 | B11.5 | PASTE | J:L130 |
| 945 | B11.5 | PASTE_GUARD | J:L53 guard form |
| 946 | B11.5 | VERBATIM | J:L130 |
| 947 | B11.5 | VERBATIM | J:L135 |

