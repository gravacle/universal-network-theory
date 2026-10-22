# UA_CHAIN_XREF_C3V001: every runbook line mapped to its source line

This file goes with `UA_CHAIN_RUNBOOK_C3V001.md` (RB). "RB L<n>" is a line of that file. Source keys are as in RB's source-key table.

**Tags:**
- **SRC:** verbatim. The only changes are the substitutions listed.
- **DERIVED:** a minimal line this draft derived, with the reason stated.
- **TEMPLATE:** a fill-in object or entry, not a command.

**Mechanical check (TESTED, 2026-10-21):** a read-only script compared all 22 SRC command groups below with their source lines after the stated substitutions. **Result: 22/22 equal.** The script is `/private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/71ea3fb2-2be2-4b38-b919-d6ca63cf052f/scratchpad/ua_chain/verify_src_lines.py`. It compared these groups:
- PAIR L27–31, L34–38, L39–44 and L52–54;
- PROCA L54–55, L56, L57–58, L62, L64, L68–69, L71–74 and L84;
- SCAN L550, L562, L574, L580, L622 and L844;
- CW8C L11, L12 and L40;
- DBPD L37.

## P0: pin check

| RB line | Command | Tag | Source |
|---|---|---|---|
| L83–102 | `shasum -a 256` over 19 adopted files | DERIVED: hashes from bytes | the expected pins come from A284 L4957–4959; A291 L5058; A282 L4904–4906; CW8C L65; S1PATH L17–21; PAIR L83–85 |

## P2: the S1 C1 prerequisites

| RB line | Command | Tag | Source |
|---|---|---|---|
| L146 | `shasum -a 256 …/S1_C1_PRODUCER_LIST_DRAFT_CX1V001.json` | DERIVED: hash | A240 L4083 (`ccb8f7d1`) and L4097 |

## P3: folders (A272 checklist of record, A272 L4725–4726)

| RB line | Command | Tag | Source and substitution |
|---|---|---|---|
| L164 | `mkdir -p PASTE_P112_LAUNCH_ROOT/{registry,…,assembly}` | SRC | SCAN L562. `<p112_launch_root>` → PASTE. Same text at SCAN L440 |
| L165 | `ls -la PASTE_P112_LAUNCH_ROOT` | DERIVED: an existence view | CW8L L2065–2070 (the six subdirs) |
| L179 | `mkdir -p PASTE_V006_COPY_DIR` | SRC | SCAN L550 (also L424). `<v006_copy_dir>` → PASTE |
| L187 | `mkdir -p PASTE_CUSTODY_DIR` | SRC | SCAN L574 (also L456). `<custody dir>` → PASTE |
| L194 | `mkdir -p PASTE_CAUSE_RECORD_DIR` | SRC | SCAN L622 (also L520). `<folder>` → PASTE |
| L202 | `mkdir /Users/bgm/Research/UNT_S0_LAUNCH_C2V003A/monitor_refused` | SRC | SCAN L580 (also L464). `<S0 launch root>` → the A272 L4719 value |
| L209 | `mkdir …/s4rc1_c3/s1_c3t_specs` | SRC | PROCA L56 |
| L210 | `mkdir PASTE_S1_FILL_DIR` | DERIVED | the verb from SCAN L856 (also L762), "mkdir a new fill folder" |
| L211 | `mkdir PASTE_S1_PLAN_DIR PASTE_S1_PRELAUNCH_DIR` | DERIVED | SCAN L862 (also L770) |
| L212 | `mkdir PASTE_S1_RECORD_DIR PASTE_S1_READING_DIR` | DERIVED | SCAN L868 (also L778) |

## Lane S8

| RB line | Command | Tag | Source and substitution |
|---|---|---|---|
| L246 | `shasum -a 256 PASTE_UA_POINT_FILE` | DERIVED: hash | PROCA L50 (the file's schema) |
| L255 | `PY=…/python3` | SRC | PROCA L54 |
| L256 | `S=…/s1_successors_c2` | SRC | PROCA L55 |
| L257–258 | `$PY -I -B $S/s1_fill_c2v002c.py c3t-cp1-spec --u-a … --base-spec … --campaign-config … --out-dir …/s1_c3t_specs` | SRC + DERIVED | PROCA L57–58. `s1_fill_c2v002a.py` → `s1_fill_c2v002c.py` (S1PATH L79–85; SCAN L789; G-01). `<UA>@<sha>`, `<u_A call spec>@<sha>` and `<campaign config>@<sha>` → PASTE |
| L284 | `shasum -a 256 PASTE_ROW32_FILE` | DERIVED: hash | V006 L1754 ("its sha256 is recorded in a V006 entry") |
| L291–297 | the row-32 V006 entry | TEMPLATE (DERIVED) | V006 L1754; PROCA L50, L60, L62, L64, L68–69. No grammar exists in a named source (G-03) |
| L308 | `PY=…/python3` | SRC | PROCA L54 |
| L309 | `KS3_RUNNER=PASTE_KS3_RUNNER` | DERIVED: PASTE of `<KS3 runner>` | PROCA L62, L71 (G-02) |
| L310 | `$PY -I -B "$KS3_RUNNER" plan --points 1,32` | SRC | PROCA L62. `<KS3 runner>` → `"$KS3_RUNNER"` |
| L322 | `PY=…` | SRC | PROCA L54 |
| L323 | `KS3_RUNNER=PASTE_KS3_RUNNER` | DERIVED | as L309 |
| L324 | `OUT=…/s4rc1_c3/cp1_s1c3t_PASTE_THETA16` | SRC | PROCA L64. `<theta16>` → PASTE |
| L325 | `REVIEW_SHA=66c54c76…` | SRC | PROCA L68 |
| L326 | `REVIEW_PIN='{…0146…}'` | SRC | PROCA L69 |
| L327 | `shasum -a 256 …/FROM_CODEX1/0146_…_PASS_0.md` | DERIVED | PROCA L70 ("re-hash the 0146 record first; it must still be 66c54c76") |
| L328 | `test ! -e "$OUT" && echo OUT_ABSENT` | DERIVED | PROCA L64 ("the folder must not exist") |
| L329–332 | `/usr/sbin/taskpolicy -b "$PY" -I -B "$KS3_RUNNER" run --out-root "$OUT" --operator-lane Claude2 --points 1 …` | SRC | PROCA L71–74. `<KS3 runner>` → `"$KS3_RUNNER"`, and `"<HOLD>"` → `"PASTE_HOLD_FILE"` |
| (S8-06, no new lines) | the same as L322–326 and L329–332, with `--points 1,32` | SRC + DERIVED | PROCA L76 ("then the same command with --points 1,32") |
| L377–379 | `PY=` / `KS3_RUNNER=` / `OUT=` | SRC / DERIVED / SRC | as L322–324 |
| L380 | `/usr/sbin/taskpolicy -b "$PY" -I -B "$KS3_RUNNER" adapt-eps --out-root "$OUT" --point 32 --review … --approved-review-sha256 … --approved-signer-lane PASTE_SIGNER_LANE` | SRC + DERIVED | From `adapt-eps` on: PROCA L84, with `<review>` and `<sha>` → PASTE and `Claude4` → PASTE_SIGNER_LANE (A202 L2601; G-04). The prefix: PROCA L71, the invocation of the same runner (DERIVED, because L84 gives only the subcommand) |
| L405 | `mkdir …/s4rc1_c3/registry_s1c3t_PASTE_THETA16` | SRC | SCAN L844 (also L746). `<theta16>` → PASTE |
| L465–469 | `PY=` `ART=` `PAIR=` `BINDER=` `PACKET=` | SRC | PAIR L27–31 |
| L470–472 | `C3_ADMISSION_PIN=` `C4_ADMISSION_PIN=` `PAIR_SOURCE_REVIEW_PIN=` | DERIVED: PASTE | PAIR L32 ("root's absolute path@actual-byte-sha strings") |
| L473 | `PAIR_LAUNCHER_LOG='/Volumes/External1/…/V007_STEP4_DIRECT_V001/PASTE_….launcher.log'` | DERIVED: PASTE | PAIR L33; the parent is OUTPUT_ROOT (A272 L4712; SCAN L672) |
| L474 | `test ! -e … && echo OUTPUTS_ABSENT` | DERIVED | PAIR L47 ("All output files are exclusive-create") |
| L475–479 | `"$PY" -I -B "$BINDER" assemble-pair …` | SRC | PAIR L34–38 |
| L500–504 | `PY=` … `PACKET=` | SRC | PAIR L27–31 |
| L505 | `test ! -e … && echo OUTPUTS_ABSENT` | DERIVED | PAIR L47 |
| L506–511 | `"$PY" -I -B "$BINDER" --final-plan … --command-out …` | SRC | PAIR L39–44 |
| L512 | `shasum -a 256 …PLAN_BOUND… …ADMISSION_BOUND…` | DERIVED: hash | PAIR L49 ("Root computes PAIR_PLAN_PIN from the bound plan bytes") |
| L533 | `python3 -I -B …/check_s1_pair_caps_c3v001.py <DBP> 5d3f4bb8… <bound plan> <bound parent admission>` | SRC + DERIVED | DBPD L37. Paths made absolute; the DBP path and sha come from A291 L5058 and DBPD L32. The argument order is CHK L2. The "after assembly and bind" timing is DBPD L69 |
| L554 | `shasum -a 256 PASTE_S1_LAUNCH_CONFIG` | DERIVED: hash | PAIR L49 (`S1_LAUNCH_CONFIG_PIN`) |
| L567–568 | `PY=` `PAIR=` | SRC | PAIR L27–29 (ART expanded into PAIR) |
| L569 | `V006="…"` | DERIVED | CW8L L28 (the V006 path constant) |
| L570–571 | `export UNT_STEP4_ADMISSION_PATH=…` / `…_SHA256=PASTE` | DERIVED | PAIR L49 ("populate UNT_STEP4_ADMISSION_PATH/UNT_STEP4_ADMISSION_SHA256"). The wrapper reads them in DRY too (WRAP L86) |
| L572 | `PAIR_PLAN_PIN=…PLAN_BOUND…@PASTE` | DERIVED | PAIR L49 |
| L573 | `REGISTRATION_PIN=` | DERIVED: PASTE | PAIR L49 ("the existing implemented S1 registration") |
| L574 | `V006_PIN="$V006@$(shasum …)"` | DERIVED: hash in-block | PAIR L49 ("V006_PIN names the actual constant root file at its current byte SHA") |
| L575–576 | `S1_LAUNCH_CONFIG_PIN=`, `S1_PAIR_DRY_RECORD=` | DERIVED: PASTE | PAIR L49, L54 |
| L577–579 | `"$PY" -I -B "$PAIR/s1_pair_root_cx3v002.py" --plan … --record "$S1_PAIR_DRY_RECORD"` | SRC | PAIR L52–54 |
| L614–618 | as L567–571 | SRC / DERIVED | as above |
| L619–620 | `BOUND_PLAN_SHA=PASTE`; `PAIR_PLAN_PIN=…@$BOUND_PLAN_SHA` | DERIVED | PAIR L49, L59 |
| L621–623 | as L573–575 | DERIVED | as above |
| L624 | `S1_PAIR_LAUNCH_RECORD=…` | DERIVED: PASTE | PAIR L59 ("with a **new** record path") |
| L625–628 | `"$PY" -I -B "$PAIR/s1_pair_root_cx3v002.py" … --record "$S1_PAIR_LAUNCH_RECORD" --launch --confirm "$BOUND_PLAN_SHA"` | SRC + DERIVED | PAIR L52–54, plus PAIR L59 (`--launch --confirm <actual bound-plan sha>`) and the new `--record`. WRAP L84–87 for the flags |
| L652 | `grep '"event"' PASTE_PAIR_LAUNCHER_LOG \| tail -n 5` | DERIVED: read-only view | PLAUNCH L119, L142 (the JSON events) |

## Lane S9

| RB line | Command | Tag | Source and substitution |
|---|---|---|---|
| L681–703 | the P-112 config object | TEMPLATE | See the key sources below |
| L722 | `shasum -a 256 PASTE_P112_CONFIG` | DERIVED: hash | CW8L L2508–2509 (`--config-sha256` is required) |
| L737 | `SPEC_PIN PASTE_NAME PASTE_SERIAL_SHA256 PASTE_ABS_SERIAL_PATH` | SRC (template line) | CW8C L11 |
| L738 | `SPEC_PIN PASTE_NAME_FULL_CW8 PASTE_CW8_SHA256 PASTE_ABS_CW8_PATH` | SRC (template line) | CW8C L12 |
| L748 | `grep -c '^TOOL_PIN P112_LAUNCHER_CX3CW8V003 ' "<V006>"` | DERIVED | CW8L L364–385 (the gate: exactly one line in an A-entry); V006 L4910 (the line) |
| L767 | `<python3> -I -B <cw8 launcher> select-workers --config … --config-sha256 … --forecast … --forecast-sha256 …` | SRC | CW8C L40. `<approved_python>` → the CW8L L26 value; `<review_launcher>` → the A282 L4910 path; the four file and sha placeholders → PASTE |

**Config keys at RB L681–703:**

| Key | Source |
|---|---|
| the key set | CW8L L598–602, exact (L163–164, L828) |
| `schema` | CW8C L7; CW8L L829 |
| `python` | CW8L L26, L831 |
| `v006` | CW8L L28, L844 |
| `host_ram_bytes_expected` | CW8L L30, L832 |
| `s0` | CW8L L833; A272 L4719–4720; 0838 L12 |
| the ceilings | CW8L L2605, L2608, L2949–2950; P112C L27–28 |
| `cause_records`, `root_stop_records` | P112C L29–30; CW8L L2951–2956 |
| path rules | CW8L L216–229, L834–835, L845–855 |
| the 8 scope keys | CW8L L2992–2993 |

## Lane E: the CW8 license

| RB line | Command | Tag | Source |
|---|---|---|---|
| L801 | `python3 -I -c '…print the 7 fields and the pins keys…' PASTE_COMPARATOR_RECORD` | DERIVED: read-only | the fields CW8L L3101–3116 checks; CW8C L27. Why: a defect becomes a durable serial choice (CW8L L3383–3400; CW8C L43) |
| L802 | `shasum -a 256 PASTE_COMPARATOR_RECORD` | DERIVED: hash | CW8C L22 (the comparator record's path and byte SHA256) |
| L823–840 | the license object | TEMPLATE | See the key sources below |
| L855 | `shasum -a 256 PASTE_LICENSE_PATH` | DERIVED: hash | CW8C L13 (`sha256=<license_sha256>`) |
| L861 | `V006="…"` | DERIVED | CW8L L28 |
| L862 | `grep -c '^CW8_LICENSE_PIN' "$V006"` | DERIVED | CW8L L3013, L3018 (every line starting with the token counts; >1 refuses); A281 L4888 |
| L863 | `grep -nE '^SPEC_PIN (S0_SEED_SERIAL\|S0_SEED_CW8_TWIN) ' "$V006"` | DERIVED | CW8L L3094–3095; CW8C L11 (the line form) |
| L876 | `printf 'CW8_LICENSE_PIN path=%s sha256=%s\n' …` | DERIVED: printf of a pin line | CW8L L3015 (the regex); CW8C L13 (the form); A281 L4888 and CW8C L52 (one line, never superseded) |
| L894 | `V006="…"` | DERIVED | CW8L L28 |
| L895 | `grep -c '^CW8_LICENSE_PIN' "$V006"` | DERIVED | CW8L L3013, L3018 |
| L896 | `grep -nE '^CW8_LICENSE_PIN path=/.*[^[:space:]] sha256=[0-9a-f]{64}$' "$V006"` | DERIVED | CW8L L3015 in POSIX ERE (`\S` → `[^[:space:]]`) |
| L897 | `awk '/^## /{h=$0} /^CW8_LICENSE_PIN/{print h}' "$V006"` | DERIVED | CW8L L3009–3012, L3016 (the section is the last `## ` line, which must be `## A<n>`) |

**License keys at RB L823–840:**

| Key | Source |
|---|---|
| the key set | CW8C L18–25; CW8L L3086–3087, exact |
| `schema`, `scope` | CW8L L2986, L3088 |
| `source_pins` | CW8P L3–32, equal to CW8L L2978 (TESTED) |
| the seed pins | CW8L L3094–3097, L942 |
| `full_rss_multiplier` | CW8L L2990, L3090–3091 |

## Non-command source lines the blocks rely on for expected output and STOP conditions

- **PAIR:** L5 (the ramp), L13, L16, L22–24, L47, L49, L57, L59, L61, L73.
- **WRAP:** L29 (the confirm), L33–36 (the launch config), L57–59 (ADMITTED and the record), L68 (the outcome record), L86 (the environment), L88 (the exit codes).
- **PLAUNCH:**
  - L96–98: re-validate each poll;
  - L114–133: the admission ramp;
  - L119: the decision event;
  - L120: PREDECESSOR_ENDED_BEFORE_FIRST_ITERATION;
  - L136: drain;
  - L142: finished;
  - L156: normal QoS;
  - L158–160: the detached worker and its stdout.
- **PBIND:** L61 and L113 (printed JSON).
- **CHK:** L18–19 (CHECK_FAILED), L72–73 (PASS).
- **DBPD:** L19 (W = 3,443,340 s), L26 (the optional exact refill: not used, because A291 adopted `5d3f4bb8`), L69.
- **CW8L:**
  - L2505–2523: CLI;
  - L2571–2574: REFUSED and exit 2;
  - L2991: the forecast age;
  - L3341–3347: the lock;
  - L3391: the forecast scope;
  - L3411–3422: the choice and SELECTED;
  - L1787–1812: `status`, which does not authenticate the license.
- **CW8C:** L16, L29–35, L43, L45, L52–58.
- **V006:**
  - A160 L1342;
  - A201 L2569;
  - L1754;
  - A202 L2601–2605;
  - A240 L4083–4104;
  - A268 L4619–4623;
  - A272 L4707–4726;
  - A274 L4745–4759;
  - A280 L4853–4856;
  - A281 L4878–4891;
  - A282 L4904–4916;
  - A284 L4951–4969;
  - A291 L5047–5066.
- **AUDIT:** L70, L122–131, L146, L151–154.
- **SCAN:** L369, L374, L626–629, L672, L789, L850, L856, L862, L868.
- **PROCA:** L17, L24, L35–36, L46–47, L50, L60, L75–79, L83, L85–88, L91–96, L102–104.
- **S1PATH:** L34, L57, L79–85, L92–94, L185–188, L196.
- **P112C:** L25, L27–30, L42.
