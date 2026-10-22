# UA_CHAIN_RUNBOOK_C3V001: the u_A → S8/S9 launch chain, pre-staged (root 0850 item 3; V006 A290; audit L3)

**From:** a Claude3-lane helper. This is a draft for the lead to review; the lead posts. **Research window:** 2026-10-21 15:21Z–15:52Z (`date -u`).

**Status: DRAFT.** Nothing here was run. It grants no launch authority and adopts nothing. No run tree, run output, /Volumes path, NGC3198 data, V007_POSTSEAL_RECORDS, ~/.codex, C5H or UVT_* material was opened.

## How to read a block

- `[SRC <key>:L<n>]`: the line is verbatim from that reviewed, adopted source. The only change is `<placeholder>` → `PASTE_*`.
- `[DERIVED: <why>]`: a minimal line this draft derived. These are existence checks, hashes, a printf of a pin line, environment assignments, a relative path made absolute, or a file-name substitution. The reason is given each time.
- `PASTE_*`: a runtime value that root supplies from bytes or from `date -u`. Never guess one.
- **ROOT ACTION:** the source gives an instruction but no command, so no command is written.
- **G-nn:** an open item in `UA_CHAIN_GAPS_C3V001.md`.
- **Every block stands alone.** Shell state does not persist, so each block sets its own variables. Root runs one block per call.
- **QoS.**
  - No `taskpolicy` or `nice` appears except where the source line carries it. The CP-1 runner enforces background QoS (A274 L4750).
  - The S1 pair must never run under `nice`. The binder refuses it ([S1PATH] L92-94), and the pair launcher forces normal QoS itself ([PLAUNCH] L156).

## Source key (sha256 prefixes from bytes, 2026-10-21)

| Key | Path (under `/Users/bgm/Research/UNT_EXCHANGE/` unless absolute) | sha256 | Standing |
|---|---|---|---|
| PAIR | `claude_artifacts/s1_pair_concurrent_cx3/README_CX3V001.md` | `27e86901` | A284 L4959 |
| WRAP | `claude_artifacts/s1_pair_concurrent_cx3/v001/s1_pair_root_cx3v002.py` | `c08b5b78` | A284 L4958; read for its CLI and decisions only |
| PBIND | `claude_artifacts/s1_pair_concurrent_cx3/v001/step4_bind_c2v011_s1pair_cx3v001.py` | `f57f5f1d` | A284 L4957; CLI only |
| PLAUNCH | `claude_artifacts/s1_pair_concurrent_cx3/v001/step4_launcher_c2v015_s1pair_cx3v001.py` | `2e41da37` | A284 L4957; CLI and log events only |
| PROCA | `claude_artifacts/s1_successors_c2/S1_C3T_CERT_EXTENSION_PROCEDURE_A.md` | `4da9ddb5` | the S8 procedure the A272 checklist scans ([SCAN] L651; procedure-A entries L742–868; L789). Standing: G-01 |
| S1PATH | `claude_artifacts/s1_successors_c2/README_S1_PATH_C2V002C.md` | `135a0426` | the old single-call path; its bases are unchanged under A284 L4954 |
| DBPD | `claude_artifacts/h11_wall_ceiling_c3/README_C2V004D_C3V001.md` | `81a34221` | describes the DBP instance and checker that A291 L5058 adopts |
| CHK | `claude_artifacts/h11_wall_ceiling_c3/check_s1_pair_caps_c3v001.py` | `5f24c6bf` | A291 L5058 |
| CW8C | `claude_artifacts/cw8_phase1_cx3/ROOT_METADATA_CONTRACT_CX3V003.md` | `16c6f3e4` | the A282 package |
| CW8L | `claude_artifacts/cw8_phase1_cx3/phase1_ngc_launch_cx3cw8v003.py` | `4d5b47e7` | A282 L4904, L4910; CLI and config schema only |
| CW8P | `claude_artifacts/cw8_phase1_cx3/CW8_SOURCE_PINS_CX3V001.json` | `3cd81174` | named by CW8C L65. Its `source_pins` equal CW8L L2978 (TESTED) |
| P112C | `claude_artifacts/phase1_ngc_launch_kit_cx2v004/README_CONTRACT_CX2V004_V001.md` | `78b77cbf` | the `P112_CONFIG_CX2V004` contract that CW8C L7 uses |
| SCAN | `claude_artifacts/folder_scan_c2/FOLDER_SCAN_RESULT_WF_FA4A29F1.json` | `9911e4db` | A272 L4707, L4726: the folder checklist of record |
| AUDIT | `claude_artifacts/critical_path_audit_c3/AUDIT_C3V001.md` | `a8e50bc6` | A274 L4745 |
| VRES | `claude_artifacts/verify_c3_s1_pair/RESULT.json` | `3d2a034a` | A284 L4951 |
| V006 | `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` | append-only | read by heading: A160, A201, A202, A240, A241, A268, A272, A274, A280–A282, A284, A291, plus L1751–1757 (the dispatch's "about L1754") |

## 0. Parallel structure

```
BEFORE u_A (now → W3 acceptance, about Sun 25 under L2; A274 L4758, AUDIT L125). All independent:
  P0  pin check                                     [DERIVED hashes]
  P1  row-32 EPS window + V006 write-freeze window  [ROOT ACTION]
  P2  S1 C1 prerequisites B1-B6                     [lane/ROOT ACTION; B2, B4 are G-items]
  P3  folders that do not depend on u_A             [SRC SCAN / PROCA mkdir lines]
  P4  u_A-independent PASTE values                  [ROOT ACTION]
  LANE E  the CW8 license. Trigger: S0 seed/twin comparator EQUAL (A282 L4916).
          Independent of u_A, but must finish before S9-04 if cw8 is to be used.

AT u_A (Phase-1 snapshot BUDGET_EXHAUSTED; PROCA L47). Two lanes start together:

LANE S8 (serial; row 32, then the S1 pair)
  S8-01 u_A point file → S8-02 CP-1 input spec → S8-03 row file + V006 pin entry
  → S8-04 KS3 plan dry → S8-05 anchor row 1 → S8-06 rows 1,32 ............ the first S8 compute starts here
  → S8-07 EPS window (Codex3) + adapt-eps → S8-08 rho registration → S8-09 LO slot proof
  → S8-10 KS4 bundle/registry → S8-11 S1 C1 freeze + KS4 verify → S8-12 S1 fill
  → { S8-13a C3T child: plan → PRELAUNCH → bind  ∥  S8-13b C4T child: plan → PRELAUNCH → bind }
  → S8-14 pair source review → S8-15a assemble-pair → S8-15b bind → S8-16 C2V004D caps check
  → S8-17 publish parent admission → S8-18 pair DRY → S8-19 envelope START → S8-20 LAUNCH → S8-21 ramp watch
  Side work during S8-05/06 (CP-1 compute, about 1.5-3 h plus 3 rho stages; PROCA L104):
    S8-P1 S1 launch config, S8-P2 registration and C4T C1 pins, S8-P3 the u_A-keyed registry folder.

LANE S9 (serial; Phase-1 new calls on cw8 v003). Runs alongside S8:
  S9-01 Phase-1 PLAN 1a/1b (G-20) → S9-02 P-112 config write + pin → S9-03 SPEC_PIN lines
  → S9-04 forecast + select-workers → S9-05 P112 launches (G-21)
```

Within reach of minutes after u_A, assuming P0–P4 are done and G-02/G-03 are closed:
- **S8:** S8-01 to S8-05.
- **S9:** S9-02 to S9-04, given S9-01's outputs and Lane E done.

The S1 pair itself starts only after the row-32 chain. The audit puts that chain at 4–6 h at E (AUDIT L70).

---

## 1. Before u_A

### P0: pin check of every adopted tool this chain uses [DERIVED: hashes from bytes]

```
shasum -a 256 \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001/step4_guard_c2v014_s1pair_cx3v001.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001/step4_launcher_c2v015_s1pair_cx3v001.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001/step4_bind_c2v011_s1pair_cx3v001.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001/s1_pair_root_cx3v002.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/README_CX3V001.md \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h11_wall_ceiling_c3/C2V004D_FILL_20261022T093000Z/DIRECT_BATCH_PARAMS_S45_C2V004D.json \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h11_wall_ceiling_c3/check_s1_pair_caps_c3v001.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/phase1_ngc_launch_cx3cw8v003.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/roster_builder_c2v007_cx3cw8v003.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/g26_freeze_cx3cw8v003.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/CW8_SOURCE_PINS_CX3V001.json \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/s1_path_lib_c2v002c.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/s1_fill_c2v002c.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/s1_launch_root_c2v002c.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/s1_read_c2v002c.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_guard_c2v014.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_launcher_c2v015.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_bind_c2v011.py \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/S1_C3T_CERT_EXTENSION_PROCEDURE_A.md
```

**Expected:** 19 lines. The prefixes are below, in this order.

| Files | Prefixes | Source of the pin |
|---|---|---|
| Pair guard, launcher, binder, wrapper, README | `1274a39a` `2e41da37` `f57f5f1d` `c08b5b78` `27e86901` | A284 L4957–4959 |
| DBP C2V004D, caps checker | `5d3f4bb8` `5f24c6bf` | A291 L5058 |
| cw8 launcher, roster builder, G26 | `4d5b47e7` `f710334b` `171710bb` | A282 L4904–4906 |
| CW8 source pins | `3cd81174` | CW8C L65 |
| S1 lib, fill, launch root, read | `99e2be17` `2b120b89` `d4e31013` `4716bb69` | S1PATH L17–20 |
| guard014, launcher015, binder011 | `6efdca01` `cd987edd` `d3d9702e` | PAIR L83–85; S1PATH L21 |
| Procedure A | `4da9ddb5` | read by this helper 2026-10-21 |

**STOP:** any mismatch. Do not continue on that tool.

### P1: the row-32 EPS window and the V006 write-freeze window (ROOT ACTION)

1. **Book a Codex3 window for the row-32 EPS review** (AUDIT L123).
   - **When:** from row 32's POINT_DONE in S8-06. The estimate is u_A + about 1.5–3 h plus the 3 ρ stages (PROCA L102–104, UNTESTED).
   - **Who:** Codex3 is the root-approved CP-1 EPS signer lane (A202 L2601). Every request has `excluded_reviewer_lanes` exactly `[Claude2, Codex2]` (A202 L2602).
   - **The ruling needed:** A202 assigns rows 10–31 (L2603), and procedure A names Claude4 (PROCA L83–84). Root names row 32's signer: **G-04**.
   - **Codex3 pre-stages** its own scripted E1–E10 check and review writer (A202 L2605). It must accept a K=3 point: 179 EPS unit shells [3,182] and the 10-shell ρ partition from [3,4] (PROCA L35–36; A160 L1342). Rows 10–31 are K=4 [4,182]: **G-05**.
2. **Fix the seal's V006 write-freeze window** (A201 L2569; AUDIT L152 recommends outside u_A ± 1 d). It must not cover any of:
   - S8-03 (the row-32 pin entry, which comes before any row-32 CP-1 run, V006 L1754);
   - E-05 (the single CW8_LICENSE_PIN entry);
   - S9-03 (the SPEC_PIN entries for the new Phase-1 calls).

### P2: the S1 C1 prerequisites, re-dated to before W3 acceptance (A274 L4758; AUDIT L125–129)

These are lane builds, reviews and root rulings. No adopted source gives a command for them.

| # | Item | Owner | Basis | Command |
|---|---|---|---|---|
| B1 | Codex3's S1 C1 policy review, the distinct check. If it binds only the planned registry path and not its content, Codex3 signs now against the planned path. Codex3 states anything that must wait for the row-32 registry. | Codex3 | A240 L4100; AUDIT L126; precedent A280 L4853–4856 | ROOT ACTION (dispatch) |
| B2 | The S1 C1 freeze tool. It binds A240/A268's exact ordered six by digest: G4, G3, G1, KS6′ LO, G2 SRB_ROT, G6b. Order, uniqueness and completeness are enforced by digest, as `fill_c1_pin_c2v002` does for H1. **Unbuilt** per the A272 checklist ([SCAN] L789). | root commissions | A240 L4089–4097, L4102; A268 L4623 | **G-06** |
| B3 | The source-closure delta: the 3 added certificate pins in the S1 admission sources. The deciding test is the real dry launch (S8-18). | Codex1 | A240 L4101 | ROOT ACTION: confirm its status (**G-07**) |
| B4 | How each child's native PRELAUNCH record is produced. PAIR L22 says "Build native PRELAUNCH records for each". The A272 checklist flags that `step4_prelaunch_c2v005.py` (bytes `117b3520`) pins guard011 and refuses guard014 plans, while s1 `make_plan` needs a prelaunch record (not verified). | root | [SCAN] L789 | **G-08** |
| B5 | Root's dry launch on the real admission. It needs the u_A fill, so it **cannot** precede u_A. Its pair-path form is S8-18. Only the u_A-independent PASTE values (P4) are pre-staged. | root | AUDIT L129; PAIR L51–57, L73 | S8-18 |
| B6 | The draft of record for the six producer pins: `claude_artifacts/s1_c1_producer_list_cx1/S1_C1_PRODUCER_LIST_DRAFT_CX1V001.json` `ccb8f7d1`. "The exact pins are as in the draft." | root | A240 L4083, L4097 | check below |

B6 check (P2-B6) [DERIVED: hash from bytes]:
```
shasum -a 256 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_c1_producer_list_cx1/S1_C1_PRODUCER_LIST_DRAFT_CX1V001.json
```
- **Expected:** prefix `ccb8f7d1`.
- **STOP:** a mismatch means the producer list must not be frozen.

### P3: folders that do not depend on u_A (A272 checklist of record, A272 L4725–4726)

Lines tagged [SRC SCAN] are the checklist's own fix text, with `<…>` → `PASTE_*`. Lines tagged [DERIVED] take only the verb from a fix text that names no path. **Choose every PASTE path** to be:
- absolute, normalized and realpath-equal, with no symlinks;
- off the run trees;
- free of any component containing `ngc3198`, starting `uvt_`, or equal to `runs_ext` or `v007_postseal_records`;
- free of `unt_internal_runs` and `kmax_a2f10_c5h`;
- not under `~/.codex`.

The cw8 launcher enforces these rules on its configured roots ([CW8L] L216–229, L845–850). The P-112 launch root must also be on the internal disk ([CW8L] L835).

**P3a: the P-112 launch root and its six subfolders**
```
mkdir -p PASTE_P112_LAUNCH_ROOT/{registry,launches,work,twin_kill,outside_set_stop,assembly}
ls -la PASTE_P112_LAUNCH_ROOT
```
- Line 1: [SRC SCAN:L562].
- Line 2: [DERIVED: shows the 6 subfolders].
- **Expected:** the 6 folders exist. There is no `.worker_choices.lock` and no `worker_choices/` yet.
  - The launcher creates the lock inode (`O_CREAT|O_EXCL`, mode 0444) and the choices folder at the first selection ([CW8L] L3341–3347, L3411–3413).
  - Once the lock exists, never remove or replace it ([CW8C] L54).
- **STOP:**
  - PASTE_P112_LAUNCH_ROOT starts with `/Volumes/` (LAUNCH_ROOT_EXTERNAL, [CW8L] L835);
  - any level is a symlink (LAUNCH_ROOT_REAL / LAUNCH_SUBDIR_REAL, [CW8L] L2065–2070).
- **Why now:** v003-N3: a missing launch root makes the lock wrapper refuse with no fallback record (A282 L4915).

**P3b: v006_copy_dir**
```
mkdir -p PASTE_V006_COPY_DIR
```
- [SRC SCAN:L550]
- **When:** before the P-112 config is pinned (S9-02).
- **STOP:** it is inside either run root (CUTOFF_COPY_IN_RUN_TREE, [CW8L] L853–855).

**P3c: the custody directory**
```
mkdir -p PASTE_CUSTODY_DIR
```
- [SRC SCAN:L574]
- **When:** before the first P-112 or kit close-attempt. It must be outside every run tree and not an ancestor of one.

**P3d: the cause-record folder**
```
mkdir -p PASTE_CAUSE_RECORD_DIR
```
- [SRC SCAN:L622]
- **When:** before the first classify or pair call. Pass an absolute `--out`, with a fresh name for each record.
- Root runs the cause producer on every FAILED attempt before any snapshot (A282 L4913).

**P3e: the S0 monitor_refused folder (conditional)**
```
mkdir /Users/bgm/Research/UNT_S0_LAUNCH_C2V003A/monitor_refused
```
- [SRC SCAN:L580]
- It is needed only before a kit MONITOR_REFUSED record. Creating it early is allowed ("or creates it with the launch root"). The S0 launch root exists (A272 L4719).

**P3f: the S1 procedure-A folders that are not keyed by theta**
```
mkdir /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/s1_c3t_specs
mkdir PASTE_S1_FILL_DIR
mkdir PASTE_S1_PLAN_DIR PASTE_S1_PRELAUNCH_DIR
mkdir PASTE_S1_RECORD_DIR PASTE_S1_READING_DIR
```
- Line 1: [SRC PROCA:L56].
- Line 2: [DERIVED from SCAN:L856, "mkdir a new fill folder"].
- Line 3: [DERIVED from SCAN:L862, "mkdir the plan folder and the PRELAUNCH output folder"].
- Line 4: [DERIVED from SCAN:L868, "mkdir the record folder … and the reading folder"].
- `PASTE_S1_RECORD_DIR` also holds the pair wrapper's DRY and LAUNCH records (S8-18, S8-20). Its parent must exist because the record is written by exclusive create ([WRAP] L59).
- The bind outputs go in the existing PACKET `claude_artifacts/step4_launch_packet_cx1` ([SCAN] L862).
- **Expected:** no output.
- **STOP:** `File exists` on line 1. The folder may hold an earlier spec; root inspects it before S8-02.

The S1 calls' outdirs, receipts and monitor logs sit directly under OUTPUT_ROOT `/Volumes/External1/Research/UNT_STEP4_RUNS/V007_STEP4_DIRECT_V001` ([SCAN] L672). That folder already exists (A272 L4712), so no S1 parent needs creating there.

### P4: u_A-independent PASTE values (ROOT ACTION)

- `PASTE_REGISTRATION_PIN`: "the existing implemented S1 registration", as an absolute path@sha ([PAIR] L49).
- `PASTE_C4T_C1`: the campaign (b1) C1 for the S1_UA_C4T child. Under the S1 C1, C4T is refused ([S1PATH] L185–186; [PAIR] L16).
- `PASTE_KS3_RUNNER`: the adopted row-32 KS3 runner path and sha. **G-02**: there are two versions (bytes, TESTED). The audit's `54595c2d` is `ks_k3_chain_c2/cp1_runner_c3v004_ks3_c2v001.py`. The A272 checklist scanned `…_ks3_c2v002.py`, which is `da08d725`. Root names the adopted one.
- `PASTE_HOLD_FILE`: the CP-1 runner's `--hold-file` (PROCA L73).
- The C4T-side child inputs that do not need the fill.

---

## 2. Lane S8 (starts at u_A)

### S8-01: the u_A point file (ROOT ACTION)

Root writes, by exclusive create, a file of schema `UNT_S1_UA_POINT_C2V002`:

`{"schema", "theta", "theta_key", "phase1_snapshot": {path, sha256} of SNAPSHOT_C2V001.json, "coordinate_mode"}` (PROCA L50).

The S1 library binds u_A at the snapshot's `/u_A/theta_natural` and at `/run/exploration/primary_anchor/theta_natural` (PROCA L50).

```
shasum -a 256 PASTE_UA_POINT_FILE
```
[DERIVED: the pin used in S8-02]

- **STOP:** the Phase-1 snapshot is not BUDGET_EXHAUSTED (PROCA L47).

### S8-02: the CP-1 input spec (no certificate needed yet)

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
S=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2
$PY -I -B $S/s1_fill_c2v002c.py c3t-cp1-spec --u-a PASTE_UA_POINT_FILE@PASTE_UA_POINT_SHA --base-spec PASTE_UA_CALL_SPEC@PASTE_UA_CALL_SPEC_SHA \
    --campaign-config PASTE_CAMPAIGN_CONFIG@PASTE_CAMPAIGN_CONFIG_SHA --out-dir /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/s1_c3t_specs
```

- Lines 1–2: [SRC PROCA:L54–55].
- Lines 3–4: [SRC PROCA:L57–58], plus [DERIVED: `s1_fill_c2v002a.py` → `s1_fill_c2v002c.py`].
  - The c2v002c CLIs are the c2v002a code with only the library pin changed ([S1PATH] L79–85).
  - The A272 checklist notes procedure A still names c2v002a ([SCAN] L789).
  - Root confirms: **G-01**.
- The mkdir at PROCA L56 was done in P3f.
- **Expected:**
  - It prints the point key and the spec sha.
  - It writes `S1_UA_C3T_<key16>.cp1.spec.json` by exclusive create, with both certificate slots `PENDING_UV_TAIL_CERTIFICATE` (PROCA L60).
- **STOP:** any refusal, or an existing output file.

### S8-03: the row-32 row file and its V006 pin entry (ROOT ACTION, with a template)

**The rule (V006 L1754):** "Root writes row 32's file once u_A is fixed. Its sha256 is recorded in a V006 entry before any row-32 CP-1 run, which is the pin."

**The row content (PROCA L62):**

`(32, <point key>, 'S1_UA_C3T', ('S1_UA_C3T',), 's4rc1_c3/s1_c3t_specs/S1_UA_C3T_<key16>.cp1.spec.json', <spec sha>, 4.04, <q_inf>)`

- `q_inf` is recorded only, and root fills it by the rule rows 1–31 used.
- The row file's format, and how the KS3 runner is given it, are not in any named source: **G-03**.

```
shasum -a 256 PASTE_ROW32_FILE
```
[DERIVED: the V006 pin value]

**V006 entry template** [DERIVED-TEMPLATE: no adopted source fixes a grammar for this entry, G-03]. Its lines deliberately begin with `**` or `- `, so that no V006 pin parser reads them:

```
## A<n>: row 32 (S1_UA_C3T): the KS3 row file is pinned before any row-32 CP-1 run (UTC <date -u>)

**Row file (V006 L1754).** `PASTE_ROW32_FILE` sha256 `PASTE_ROW32_SHA`. This sha256 is the pin.
- u_A point file: `PASTE_UA_POINT_FILE` sha256 `PASTE_UA_POINT_SHA`; theta_key `PASTE_THETA_KEY`; Phase-1 snapshot `PASTE_SNAPSHOT_PATH` sha256 `PASTE_SNAPSHOT_SHA`.
- CP-1 input spec: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/s1_c3t_specs/S1_UA_C3T_PASTE_KEY16.cp1.spec.json` sha256 `PASTE_SPEC_SHA`; point key `PASTE_POINT_KEY`.
- Out-root, absent at this entry: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_s1c3t_PASTE_THETA16`.
- KS3 runner: `PASTE_KS3_RUNNER` sha256 `PASTE_KS3_RUNNER_SHA`. ρ gate pin: the 0146 record `66c54c76…` (procedure A step 5).
```

- **Never** start a line in this entry with `CW8_LICENSE_PIN`, `TOOL_PIN`, `SPEC_PIN`, `HANDOFF_PIN` or `RESIDUAL_RETRY`. The P112 V006 readers parse those tokens at the start of a line ([CW8L] L364–398, L3006–3019).
- **STOP:**
  - the write-freeze window (P1.2) is active;
  - the entry is not written before S8-05.

### S8-04: the KS3 dry plan

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
KS3_RUNNER=PASTE_KS3_RUNNER
$PY -I -B "$KS3_RUNNER" plan --points 1,32
```

- Line 1: [SRC PROCA:L54].
- Line 2: [DERIVED: PASTE of `<KS3 runner>`, G-02].
- Line 3: [SRC PROCA:L62]. Any row-file argument is **G-03**.
- **Expected:** SPEC_AND_KEY_VERIFIED for rows 1 and 32. It writes nothing (PROCA L62).
- **STOP:** anything else.

### S8-05: the anchor, row 1, in a new out-root (two-phase form, A146)

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
KS3_RUNNER=PASTE_KS3_RUNNER
OUT=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_s1c3t_PASTE_THETA16
REVIEW_SHA=66c54c762052c6a5df4761cbcf4d00242a41b93f2074de81fbb87a2a559e2a0a
REVIEW_PIN='{"path": "/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0146_2026-10-19_A138_corrected_proof_CP1_delta_PASS_0.md", "sha256": "66c54c762052c6a5df4761cbcf4d00242a41b93f2074de81fbb87a2a559e2a0a"}'
shasum -a 256 /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0146_2026-10-19_A138_corrected_proof_CP1_delta_PASS_0.md
test ! -e "$OUT" && echo OUT_ABSENT
/usr/sbin/taskpolicy -b "$PY" -I -B "$KS3_RUNNER" run --out-root "$OUT" --operator-lane Claude2 --points 1 \
  --max-concurrent 1 --margin-pct 5 --anchor-tol 1e-3 --swap-hold-mib 512 \
  --r2-spike-allowance-gib 40 --per-worker-peak-gib 2 --floor-margin-gib 4 --hold-file "PASTE_HOLD_FILE" --poll-seconds 60 \
  --allow-rho --proof-side-review-pin "$REVIEW_PIN" --proof-side-review-sha256 "$REVIEW_SHA"
```

| Line | Tag |
|---|---|
| 1 | [SRC PROCA:L54] |
| 2 | [DERIVED: PASTE, G-02] |
| 3 | [SRC PROCA:L64] |
| 4–5 | [SRC PROCA:L68–69] |
| 6 | [DERIVED: PROCA L70, "re-hash the 0146 record first; it must still be 66c54c76"] |
| 7 | [DERIVED: PROCA L64, "the folder must not exist"] |
| 8–11 | [SRC PROCA:L71–74] |

- `--r2-spike-allowance-gib 40` stays only if KHI or another route-A spike is possible at that time (PROCA L79). At u_A the campaign is running, so it stays.
- **Expected:**
  - line 6 prints `66c54c76…`;
  - line 7 prints `OUT_ABSENT`;
  - SCHEDULER_START shows `rho_gate.open` true (PROCA L78).
- **Root check (PROCA L75):** `ANCHOR_RHO_PAIR_8ad6ca4e867854da.json` is canonical-equal, from separate processes, with distinct records, and the cross-check reads AGREE.
- **STOP:**
  - the re-hash is not `66c54c76…`;
  - OUT exists;
  - `rho_gate.open` is false;
  - the cross-check is not AGREE.
- **Never use, restart or write `cp1_run_c3v004`** (PROCA L46).
- **Background or foreground** is not stated by the source (G-09). The scheduler runs for about 40–90 min plus 2 ρ stages (PROCA L102).

### S8-06: rows 1 and 32 in the same out-root

The command is S8-05's lines 1–5 and 8–11, with `--points 1` → `--points 1,32`. [SRC PROCA:L76, "then the same command with --points 1,32"] [DERIVED: the one substitution PROCA L76 states]

- **Expected:**
  - row 1 is skipped as POINT_DIR_EXISTS_NOT_RERUN (PROCA L76);
  - row 32 runs context, GQ, EPS (179 shells) and ρ a (PROCA L103);
  - POINT_DONE for row 32 (PROCA L83).
- **STOP:**
  - any stage failure;
  - a CONTEXT-stage stop on row 32, which would mean the K=3 chain is not the pinned one (PROCA L17, L24).

### S8-07: the EPS window (Codex3), then adapt-eps

**ROOT ACTION:** after POINT_DONE for row 32, root posts `EPS_REVIEW_REQUEST_<k16>.json` and the point's EPS policy-review instance (path and sha) to the signer lane (PROCA L83; signer G-04).
- The signer runs its scripted E1–E10 check and review writer (A202 L2605; G-05) and signs.

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
KS3_RUNNER=PASTE_KS3_RUNNER
OUT=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_s1c3t_PASTE_THETA16
/usr/sbin/taskpolicy -b "$PY" -I -B "$KS3_RUNNER" adapt-eps --out-root "$OUT" --point 32 --review "PASTE_EPS_REVIEW" --approved-review-sha256 "PASTE_EPS_REVIEW_SHA" --approved-signer-lane PASTE_SIGNER_LANE
```

- Lines 1–3: as S8-05.
- Line 4 is [SRC PROCA:L84] from `adapt-eps` onward, with two DERIVED parts:
  - **The prefix** `/usr/sbin/taskpolicy -b "$PY" -I -B "$KS3_RUNNER"` [DERIVED: PROCA L84 gives the subcommand only; the prefix is PROCA L71's invocation of the same runner].
  - **The signer value:** PROCA L84 has `Claude4`; A202 L2601 admits Codex3 through this flag. Root rules it (G-04).
- **Expected:** adapt-eps completes for row 32. The exact success text is not in the named sources.
- **STOP:**
  - any refusal, including a signer lane in `excluded_reviewer_lanes` (A202 L2602);
  - a review sha that does not match the signed bytes.

### S8-08: ρ registration (ROOT ACTION, G-10)

"ρ registration: slot ρ = attempt a of row 32" (PROCA L85). No command is in the named sources.

### S8-09: the LO slot proof on that ρ record (ROOT ACTION, G-10)

- **The tool:** G1 `ks_k3_chain_c2/lo_slot_proof_c3v003_g1_c2v001.py` (bytes `6af9ed6c` = S1PATH L57), or its K=3 successor if K6 fails (PROCA L86).
- **The out-root:** either name the existing `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/lo_slot_c2v001` explicitly, or mkdir a new folder first ([SCAN] L850).
- The command is not in the named sources.

### S8-P3 (side work during S8-05/06): the KS4 registry out-root

```
mkdir /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/registry_s1c3t_PASTE_THETA16
```

- [SRC SCAN:L844]
- The parent `s4rc1_c3` exists. The KS4 out-root must be exactly `s4rc1_c3/registry_<name>` and already exist ([SCAN] L629).
- **Never** reuse `registry_c2v001` or `registry_c1verify_c2v001` ([SCAN] L628).
- **STOP:** the folder exists.

### S8-10: KS4 bundle for row 32, then registry (ROOT ACTION, G-10)

- **The step:** "KS4: `bundle` for row 32, then `registry` over the bundles the S1 admission's C1 needs (at least row 32)" (PROCA L87).
- **The tool:** the A268 successor (A268 L4619–4622). Its file `ks_k3_chain_successor_cx1/registry_assembler_ks4_cx1v002.py` is named at [SCAN] L626 (bytes `ef821296`).
- The commands are not in the named sources.

### S8-11: the S1 C1 freeze, then KS4 verify with the S1 C1 (G-06, G-10)

- **The freeze:** the S1 C1 binds A268's ordered six (A268 L4623). Its `tail_readiness.certificate_registry` is the S8-10 registry. Its certificate policy review binds KS5's sha (PROCA L88) and is signed by Codex3 (P2-B1).
- **The freeze tool** is unbuilt (G-06).
- **KS4 verify** with that C1 (PROCA L88): the command is not in the named sources.

### S8-12: the S1 fill (G-11)

`s1_fill_c2v002c.py fill ... --c3t-registry <registry>@<sha> --out-dir <dir>` (PROCA L91, with the c2v002c name per G-01).

- The source elides the arguments ("..."), so it cannot be written verbatim: **G-11**.
- Out-dir = PASTE_S1_FILL_DIR (P3f).
- The C3T slots are taken from the registry entry of `point_identity(S1_UA_C3T)` with the identity check (PROCA L91).
- **Both child specs come from this one fill** (PAIR L22). So C4T also waits for the row-32 chain.

### S8-13a ∥ S8-13b: the two single-call children, C3T and C4T, in parallel (G-12, G-08)

For each case: `plan` → PRELAUNCH005 native preflight → admission → binder011 bind.

- **plan:** add `--overlap` if the campaign is active (PROCA L92). Pass DBP C2V004D, because S8 onward uses C2V004D (A291 L5058). The lib's default is C2V004B, and `--params` exists (S1PATH L34, L84, L196).
  - The exact `--params` value form is **G-12**.
  - **Children planned from C2V004B or C2V004C caps fail S8-16** (PLAN_CAPS).
- **PRELAUNCH:** with `context_module` = the wrapper successor (PROCA L93; root copies it from the sidecar, S1PATH L187–188). See G-08.
- **Admission:** the sidecar's `admission_fields_for_root` (PROCA L94).
- **Distinct C1s:**
  - C3T: the S1 C1 (KS5 review).
  - C4T: the campaign b1 C1 (S1PATH L185–186; PAIR L16).
  - A shared C1 is refused at assembly (S1_PAIR_DISTINCT_C1_REQUIRED, [VRES] N2).
- **Rules for both children:**
  - Both must reference the one written S1 fill, the same theta/branch/attempt and the same V007 (PAIR L22).
  - **Do not execute their single-call launch commands** (PAIR L22).
- **binder011 bind:** the command line is not in a named source.
  - The pair binder's `bind` flags (PAIR L39–44) belong to a binder whose `bind` is AST-identical to binder011's (PAIR L13).
  - Root confirms binder011's CLI before use: **G-12**.
- **Outputs:** the PACKET or a subfolder of it, with all three outputs in one existing folder ([SCAN] L862).

### S8-14: the pair source review (ROOT ACTION: Claude3 and root)

- **The review covers** the union of both child `sources`, the four new files (guard, launcher, binder, wrapper v002) and the existing pinned S1 replayer (PAIR L23).
- Preserve every child source review and admission.
- The parent review's schema, status, verdict and approved_sources follow the guard's existing contract (PAIR L23).
- **Output:** `PASTE_PAIR_SOURCE_REVIEW_PIN` (absolute path@sha).

### S8-15a: assemble the pair

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
PAIR="$ART/s1_pair_concurrent_cx3/v001"
BINDER="$PAIR/step4_bind_c2v011_s1pair_cx3v001.py"
PACKET="$ART/step4_launch_packet_cx1"
C3_ADMISSION_PIN='PASTE_C3T_BOUND_ADMISSION_ABS_PATH@PASTE_SHA'
C4_ADMISSION_PIN='PASTE_C4T_BOUND_ADMISSION_ABS_PATH@PASTE_SHA'
PAIR_SOURCE_REVIEW_PIN='PASTE_PAIR_SOURCE_REVIEW_ABS_PATH@PASTE_SHA'
PAIR_LAUNCHER_LOG='/Volumes/External1/Research/UNT_STEP4_RUNS/V007_STEP4_DIRECT_V001/PASTE_S1_PAIR_LAUNCHER_LOG_NAME.launcher.log'
test ! -e "$PACKET/S1_PAIR_PLAN_CANDIDATE_V001.json" && test ! -e "$PACKET/S1_PAIR_ADMISSION_CANDIDATE_V001.json" && test ! -e "$PAIR_LAUNCHER_LOG" && echo OUTPUTS_ABSENT
"$PY" -I -B "$BINDER" assemble-pair \
  --c3t-admission "$C3_ADMISSION_PIN" --c4t-admission "$C4_ADMISSION_PIN" \
  --source-review "$PAIR_SOURCE_REVIEW_PIN" --launcher-log "$PAIR_LAUNCHER_LOG" \
  --plan-out "$PACKET/S1_PAIR_PLAN_CANDIDATE_V001.json" \
  --candidate-out "$PACKET/S1_PAIR_ADMISSION_CANDIDATE_V001.json"
```

| Line | Tag |
|---|---|
| 1–5 | [SRC PAIR:L27–31] |
| 6–8 | [DERIVED: PASTE per PAIR L32, "root's absolute path@actual-byte-sha strings"] |
| 9 | [DERIVED: PASTE per PAIR L33, "a fresh absolute path under guard's fixed External1 output root, with an existing parent". The parent is OUTPUT_ROOT (A272 L4712)] |
| 10 | [DERIVED: exclusive-create precheck, PAIR L47] |
| 11–15 | [SRC PAIR:L34–38] |

- **Expected:**
  - `OUTPUTS_ABSENT`;
  - a JSON result printed by the binder ([PBIND] L113);
  - the two candidate files created.
- **STOP:** any refusal. After a partial failure, use entirely new names (`…_V002`). No cleanup, overwrite or retry (PAIR L47).
- **The child states must agree** (PAIR L47). The children's core-priority states must match each other and the S8-P1 launch config. Inactive children get the pinned S1 replay contract. Active children must match their existing overlap contract.

### S8-15b: bind the pair

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
PAIR="$ART/s1_pair_concurrent_cx3/v001"
BINDER="$PAIR/step4_bind_c2v011_s1pair_cx3v001.py"
PACKET="$ART/step4_launch_packet_cx1"
test ! -e "$PACKET/S1_PAIR_PLAN_BOUND_V001.json" && test ! -e "$PACKET/S1_PAIR_ADMISSION_BOUND_V001.json" && test ! -e "$PACKET/S1_PAIR_EXECUTOR_COMMAND_V001.sh" && echo OUTPUTS_ABSENT
"$PY" -I -B "$BINDER" \
  --final-plan "$PACKET/S1_PAIR_PLAN_CANDIDATE_V001.json" \
  --admission-candidate "$PACKET/S1_PAIR_ADMISSION_CANDIDATE_V001.json" \
  --plan-out "$PACKET/S1_PAIR_PLAN_BOUND_V001.json" \
  --admission-out "$PACKET/S1_PAIR_ADMISSION_BOUND_V001.json" \
  --command-out "$PACKET/S1_PAIR_EXECUTOR_COMMAND_V001.sh"
shasum -a 256 "$PACKET/S1_PAIR_PLAN_BOUND_V001.json" "$PACKET/S1_PAIR_ADMISSION_BOUND_V001.json"
```

| Line | Tag |
|---|---|
| 1–5 | [SRC PAIR:L27–31] |
| 6 | [DERIVED: exclusive-create precheck, PAIR L47] |
| 7–12 | [SRC PAIR:L39–44] |
| 13 | [DERIVED: "Root computes PAIR_PLAN_PIN from the bound plan bytes", PAIR L49] |

- **Expected:**
  - a JSON bind result ([PBIND] L61);
  - three files created;
  - two sha lines. The plan sha is `BOUND_PLAN_SHA` and the admission sha is `ADMISSION_SHA`.
- **Assembly and bind grant no launch authority** (PAIR L47).
- `S1_PAIR_EXECUTOR_COMMAND_V001.sh` is **never** run (A284 N9 L4963; PAIR L59).
- **STOP:** any refusal. Then use new names, with no retry.

### S8-16: the C2V004D caps check (after assembly and bind; any failure is a STOP)

```
python3 -I -B /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h11_wall_ceiling_c3/check_s1_pair_caps_c3v001.py /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h11_wall_ceiling_c3/C2V004D_FILL_20261022T093000Z/DIRECT_BATCH_PARAMS_S45_C2V004D.json 5d3f4bb84c35adee296048264ed306102ae51267f7da7ba2595cce561698f7a2 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/S1_PAIR_PLAN_BOUND_V001.json /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/S1_PAIR_ADMISSION_BOUND_V001.json
```

- **Source:** [SRC DBPD:L37], with [DERIVED: paths made absolute; the README form is relative to `h11_wall_ceiling_c3/`].
  - The DBP path and sha: A291 L5058; DBPD L32.
  - The order of arguments: CHK L2.
  - The bound records: DBPD L69, "after assembly and bind".
- **Expected:** exactly one JSON line ([CHK] L72–73):
  `{"checked": "pair plan, parent admission, 2 child admissions, 2 child plans", "status": "PASS", "wall_cap_s": {"S1_UA_C3T": 3443340, "S1_UA_C4T": 3443340}}`
  - W = 3,443,340 s (DBPD L19; A291 L5050).
  - The numeric form is as stored in the DBP.
- **STOP:** `CHECK_FAILED <code>` with a non-zero exit ([CHK] L18–19). The codes are DBP_C2V004D_PIN, DBP_SCHEMA, DBP_POST_S1_ENTRIES, PARENT_PLAN_BINDING, PLAN_BATCH, PLAN_CASE_ORDER, PARENT_PAIR_ADMISSIONS, PLAN_CAPS, PARENT_ADMISSION_CAPS, CHILD_ADMISSION_CAPS, CHILD_PLAN_CAPS, PIN_FORM and PIN_SHA. The A291 L5057 pattern applies.
- **A 100,800 s wall anywhere** means the children came from C2V004B or C2V004C. Re-plan the children (A284 N8 L4967; A291 L5060).

### S8-P1 (side work): the S1 launch config (ROOT ACTION, written at S8 time because it attests current state)

- **Content:** schema `UNT_S1_LAUNCH_CONFIG_C2V002`, with `campaign_state` ACTIVE or INACTIVE (the actual state) and `step2_route_a_state` INACTIVE (PAIR L49; [WRAP] L33–36).
- "The C14 campaign_window is not required by the successor" (PAIR L49).
- Any further required keys of the lib's schema are **G-13**.

```
shasum -a 256 PASTE_S1_LAUNCH_CONFIG
```
[DERIVED: the pin]

### S8-17: publish the parent admission (ROOT ACTION)

- **Review:** root reviews and publishes the bound parent admission like any other admission. The ROOT_AUTHORIZED value copied from the C3T child is never relied on (A284 N6 L4962; [VRES] N6).
- **Publish:** root publishes the exact parent digest, `S1_PAIR_ADMISSION_BOUND_V001.json` at `ADMISSION_SHA` (PAIR L49).
- **The channel** for publication is root's usual one. It is not stated in the named sources.

### S8-18: the pair DRY (the B5 deciding test: root's real dry launch)

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
PAIR=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001
V006="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md"
export UNT_STEP4_ADMISSION_PATH=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/S1_PAIR_ADMISSION_BOUND_V001.json
export UNT_STEP4_ADMISSION_SHA256=PASTE_ADMISSION_SHA
PAIR_PLAN_PIN=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/S1_PAIR_PLAN_BOUND_V001.json@PASTE_BOUND_PLAN_SHA
REGISTRATION_PIN='PASTE_REGISTRATION_ABS_PATH@PASTE_SHA'
V006_PIN="$V006@$(shasum -a 256 "$V006" | cut -d' ' -f1)"
S1_LAUNCH_CONFIG_PIN='PASTE_S1_LAUNCH_CONFIG_ABS_PATH@PASTE_SHA'
S1_PAIR_DRY_RECORD=PASTE_S1_RECORD_DIR/S1_PAIR_DRY_RECORD_V001.json
"$PY" -I -B "$PAIR/s1_pair_root_cx3v002.py" \
  --plan "$PAIR_PLAN_PIN" --registration "$REGISTRATION_PIN" --v6 "$V006_PIN" \
  --launch-config "$S1_LAUNCH_CONFIG_PIN" --record "$S1_PAIR_DRY_RECORD"
```

| Line | Tag |
|---|---|
| 1–2 | [SRC PAIR:L27–29], with ART expanded |
| 3 | [DERIVED: the V006 path constant, CW8L L28] |
| 4–5 | [DERIVED: PAIR L49, "populate UNT_STEP4_ADMISSION_PATH/UNT_STEP4_ADMISSION_SHA256"; the wrapper reads them from the environment even in DRY, [WRAP] L86] |
| 6 | [DERIVED: PAIR L49, "PAIR_PLAN_PIN from the bound plan bytes"] |
| 7 | [DERIVED: PASTE, PAIR L49] |
| 8 | [DERIVED: PAIR L49, "V006_PIN names the actual constant root file at its current byte SHA". It is hashed in-block so the pin is never stale] |
| 9–10 | [DERIVED: PASTE] |
| 11–13 | [SRC PAIR:L52–54] |

- **Expected:** indented JSON, exit 0 ([WRAP] L57–59, L88), with:
  - `"decision": "ADMITTED"`;
  - `"checks"`: `registration` PASS, `filled_specs_and_native_preflights` PASS, and `inactive_process_table` either PASS or `NOT_APPLICABLE_ROOT_ACTIVE`;
  - `"cases": ["S1_UA_C3T", "S1_UA_C4T"]`;
  - `"record"` written.
  - "Require ADMITTED and all applicable checks PASS" (PAIR L57).
- **STOP:**
  - `"decision": "REFUSED"` (exit 3) with its `refusal` code;
  - `record_error`;
  - any check other than PASS or NOT_APPLICABLE_ROOT_ACTIVE.

### S8-19: the S1 phase START and the envelope (ROOT ACTION, G-14)

- **Freeze and snapshot** the complete final pair input closure: the two child admissions, plans and preflights, both C1s, the fill, the specs, the source review, the controls and the tool pins (PAIR L57).
- The A226 item-3 envelope covers both child admissions, both plans, both C1s and both prelaunch records (A284 N10 L4964).
- Root records the S1 phase START and keeps the same pinset for END (PAIR L57).
- The envelope tool's command is not in the named sources.

### S8-20: LAUNCH (after adoption, publication, a successful real DRY, START and root's go-ahead; PAIR L59)

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
PAIR=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001
V006="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md"
export UNT_STEP4_ADMISSION_PATH=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/S1_PAIR_ADMISSION_BOUND_V001.json
export UNT_STEP4_ADMISSION_SHA256=PASTE_ADMISSION_SHA
BOUND_PLAN_SHA=PASTE_BOUND_PLAN_SHA
PAIR_PLAN_PIN=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/S1_PAIR_PLAN_BOUND_V001.json@$BOUND_PLAN_SHA
REGISTRATION_PIN='PASTE_REGISTRATION_ABS_PATH@PASTE_SHA'
V006_PIN="$V006@$(shasum -a 256 "$V006" | cut -d' ' -f1)"
S1_LAUNCH_CONFIG_PIN='PASTE_S1_LAUNCH_CONFIG_ABS_PATH@PASTE_SHA'
S1_PAIR_LAUNCH_RECORD=PASTE_S1_RECORD_DIR/S1_PAIR_LAUNCH_RECORD_V001.json
"$PY" -I -B "$PAIR/s1_pair_root_cx3v002.py" \
  --plan "$PAIR_PLAN_PIN" --registration "$REGISTRATION_PIN" --v6 "$V006_PIN" \
  --launch-config "$S1_LAUNCH_CONFIG_PIN" --record "$S1_PAIR_LAUNCH_RECORD" \
  --launch --confirm "$BOUND_PLAN_SHA"
```

- Lines 1–11: as S8-18, with a **new** record path (PAIR L59).
- Lines 12–15: [SRC PAIR:L52–54] plus [DERIVED: `--launch --confirm <actual bound-plan sha>` and the new `--record`, verbatim instruction at PAIR L59].
- The confirm must equal the plan pin's sha ([WRAP] L29).
- **Expected:**
  - `"decision": "LAUNCHED"`, exit 0;
  - `launcher_result.returncode` 0;
  - the stdout carries `{"detached_worker_pid": <pid>, "launcher_log": "<PAIR_LAUNCHER_LOG>", "admission_sha256": "<ADMISSION_SHA>"}` ([PLAUNCH] L160);
  - an outcome record at `<record>.outcome.json` ([WRAP] L68).
  - The wrapper returns as soon as the detached worker is spawned ([PLAUNCH] L158–160).
- **STOP:** `LAUNCHER_REFUSED`, `SPAWN_FAILED`, `REFUSED`, or `outcome_record_error`.
  - The record keeps the actual LAUNCHED or SPAWN_FAILED state (PAIR L61).
  - There is no automatic retry. Root rules (PAIR L61).
- **Never** run the binder's command file, and never run either old single-call command (PAIR L59; A284 N9).

### S8-21: the first-iteration ramp watch (root reads the pair launcher log)

- **C3T** is admitted at the worker's first poll.
- **C4T** is admitted only after C3T's first completed route-A iteration (`stages/01_route_a/attempt_000/progress.jsonl`) and the normal 60 s poll (PAIR L5; [PLAUNCH] L114–133).
- Every poll re-validates the plan, including both native preflights ([PLAUNCH] L96–98; [VRES] N7).

```
grep '"event"' PASTE_PAIR_LAUNCHER_LOG | tail -n 5
```
[DERIVED: read-only view of the launcher's JSON events, [PLAUNCH] L119, L142]

- **Expected events, in order:**
  1. `step4_admission_decision` for S1_UA_C3T, with `"admitted": true`.
  2. `step4_admission_decision` for S1_UA_C4T, with `"previous_first_iteration": false, "admitted": false` until C3T's first iteration.
  3. Then the same event with `"admitted": true`.
  4. At the end, `step4_finished` with `"retry": "NONE"`.
- Root follows both monitor receipts (PAIR L61).
- **STOP and branch:**
  - any drain reason in the log: ADMISSION_REVOKED, MALFORMED_PROGRESS, MONITOR_POLL_ERROR, a systemic reason, WORKER_SIGNAL, SLEEP_ASSERTION_LOST, OUTPUT_APPEARED_BEFORE_START or WORKER_INTERRUPTED_OR_ERROR;
  - the refusal PREDECESSOR_ENDED_BEFORE_FIRST_ITERATION ([PLAUNCH] L97–136).
  - In every case there is no automatic retry (PAIR L61).
  - **A284 N7 (L4965):** if C3T ends for a non-systemic reason before its first iteration, the batch drains and C4T is launched in a later batch. That command is **G-15**.

---

## 3. Lane S9 (starts at u_A, in parallel with S8)

### S9-01: the Phase-1 PLAN at u_A (G-20)

The value-free 1a/1b PLAN at u_A (AUDIT L146, citing RUNBOOK L62) supplies the config's eight scope values: `plan_output_primary`, `plan_build_record`, `selection`, `fdplan`, `spec_of_record`, `at0a_pass`, `members`, `f_points` ([CW8L] L2992–2993). The commands are in RUNBOOK c2v007, which was not opened.

### S9-02: the P-112 config for cw8 v003 (ROOT ACTION: write by exclusive create, then pin)

**Key set:** exactly these keys ([CW8L] L598–602; exact-key rule L163–164, L828):

```
{
  "schema": "PASTE_P112_CONFIG_SCHEMA",
  "python": "/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
  "v006": "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md",
  "v006_copy_dir": "PASTE_V006_COPY_DIR",
  "run_volume": "PASTE_RUN_VOLUME",
  "run_root": "PASTE_RUN_VOLUME/NGC_PASTE_RUN_ROOT_NAME",
  "p112_launch_root": "PASTE_P112_LAUNCH_ROOT",
  "s0": {"launch_root": "/Users/bgm/Research/UNT_S0_LAUNCH_C2V003A", "run_root": "/Volumes/External1/NGC_S0_PHASE1_V001"},
  "host_ram_bytes_expected": 137438953472,
  "plan_output_primary": PASTE_FROM_S9_01,
  "plan_build_record": PASTE_FROM_S9_01,
  "selection": PASTE_FROM_S9_01,
  "fdplan": PASTE_FROM_S9_01,
  "spec_of_record": PASTE_FROM_S9_01,
  "at0a_pass": PASTE_FROM_S9_01,
  "members": PASTE_FROM_S9_01,
  "f_points": PASTE_FROM_S9_01,
  "phase1_ceiling_utc": "2026-11-06T05:59:00Z",
  "phase2_ceiling_utc": "2026-12-01T05:59:00Z",
  "cause_records": [],
  "root_stop_records": []
}
```

| Key | Value and source |
|---|---|
| `schema` | `P112_CONFIG_CX2V004` or `P112_CONFIG_CX3CW8V001` ([CW8C] L7; [CW8L] L829). Root picks one: G-22 |
| `python` | must equal the PY constant ([CW8L] L26, L831) |
| `v006` | must equal the V006 constant ([CW8L] L28, L844) |
| `host_ram_bytes_expected` | 137438953472 ([CW8L] L30, L832) |
| `phase1_ceiling_utc`, `phase2_ceiling_utc` | [CW8L] L2605, L2608, L2949–2950; [P112C] L27–28 |
| `cause_records`, `root_stop_records` | lists of exact path/sha pins. `[]` is valid initially ([P112C] L29–30; [CW8L] L2951–2956) |
| `s0.launch_root`, `s0.run_root` | A272 L4719–4720; 0838 L12; [SCAN] L568. `s0` has exactly these two keys ([CW8L] L833) |
| `run_root` | its parent must equal `run_volume`, and its name starts `NGC_` ([CW8L] L851–852) |
| `v006_copy_dir` | not inside either run root ([CW8L] L853–855) |
| the eight scope fields | value forms come from S9-01 and the P112 parent contract ([P112C] L25, "All parent config fields remain"): G-20 |

**The A272 folders must exist first:** P3a (the launch root, which must exist, [CW8L] L2065), P3b, P3c and P3d.

```
shasum -a 256 PASTE_P112_CONFIG
```
[DERIVED: the `--config-sha256` value]

- A changed config is a new immutable file ([P112C] L42).
- A change to a Phase-2 scope field is a new config under a root V006 event (A281 N3 L4889).
- **STOP:**
  - EXACT_KEYS, CONFIG_SCHEMA, CONFIG_PYTHON, CONFIG_RAM, V006_CONFIG_PATH, PHASE_CEILING_CONFIG, LAUNCH_ROOT_EXTERNAL, PATH_*, CONFIG_SYMLINK, RUN_ROOT_LAYOUT or CUTOFF_COPY_IN_RUN_TREE when the config is first used ([CW8L] L828–856, L2948–2956);
  - in each case a new config file is required.

### S9-03: the V006 SPEC_PIN lines for each new call (ROOT ACTION)

Inside an A-numbered V006 section, for each new ordinary call `<name>` ([CW8C] L7, L11–12):

```
SPEC_PIN PASTE_NAME PASTE_SERIAL_SHA256 PASTE_ABS_SERIAL_PATH
SPEC_PIN PASTE_NAME_FULL_CW8 PASTE_CW8_SHA256 PASTE_ABS_CW8_PATH
```

- [SRC CW8C:L11–12] (template lines).
- The cw8 spec must already exist and differ from the serial only by `numerics.route_a.column_workers` 1→8. All other bytes, whitespace included, stay identical ([CW8C] L16; [CW8L] L55, L3070–3078).
- How the cw8 fill specs are produced is **G-23**.

The tool gate needs exactly one TOOL_PIN line for this launcher. It was written at A282 L4910.

```
grep -c '^TOOL_PIN P112_LAUNCHER_CX3CW8V003 ' "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md"
```
[DERIVED: the [CW8L] L364–385 gate as a count]

- **Expected:** `1`.
- **STOP:** any other count (TOOL_PIN_MISSING / TOOL_PIN_DUPLICATE).

### S9-04: the forecast and select-workers (an admission decision, not a query; [CW8C] L43)

**The forecast (ROOT ACTION, exclusive create; no producer is named, G-24).** It has exactly these keys ([CW8C] L29–35):
- `schema` = `CW8_PHASE1_FORECAST_CX3V001`;
- `date_u` and `observed_utc`. **The age must be 0–900 s at selection** ([CW8L] L2991);
- `calls`: the sorted, complete list of currently eligible new P112 ordinary call names;
- `host_cores` 18;
- `cores_in_use` 0–6;
- `remaining_barrier_h` with `expectation` and `upper`;
- `scope` = the exact config values of the eight scope keys ([CW8L] L3391).

```
/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/phase1_ngc_launch_cx3cw8v003.py select-workers --config PASTE_P112_CONFIG --config-sha256 PASTE_P112_CONFIG_SHA --forecast PASTE_FORECAST --forecast-sha256 PASTE_FORECAST_SHA
```

- [SRC CW8C:L40], with `<approved_python>` = the config `python` ([CW8L] L26) and `<review_launcher>` = the A282 TOOL_PIN path (V006 L4910).
- **Preconditions:**
  - **If cw8 is intended,** run only after E-06 passes. A missing or malformed license, or a bad forecast, durably selects serial for this cohort. That choice is never upgraded ([CW8C] L43; [CW8L] L3383–3400).
  - Use a fresh forecast at the actual admission decision ([CW8C] L43).
- **Expected:** `{"status": "SELECTED", "choice": {"path": "PASTE_P112_LAUNCH_ROOT/worker_choices/CHOICE_<sha>.json", "sha256": …}, "column_workers": 8|1, "reason": …, "names": [...]}` ([CW8L] L3412–3422).
- **STOP:**
  - `{"status": "REFUSED", "code": …}`, exit 2 ([CW8L] L2571–2574). Examples: CW8_NO_NEW_CALLS, CW8_CHOICE_LOCK_ROOT, CW8_CHOICE_LOCK_FILE, TOOL_PIN_*, a config code.
  - `"column_workers": 1` with a license or forecast `reason` when cw8 was intended. Record it. Do not re-run: a second selection finds the calls already chosen ([CW8C] L55).

### S9-05: the P112 launches, then close and assembly (G-21)

"Ordinary root launch/close/assembly commands follow the existing P112 workflow after selection" ([CW8C] L43).

- **CLI shape**, for reference only and not a command ([CW8L] L2505–2523):
  - `launch --config --config-sha256 --name [--attempt k] [--dry] [--resume]`;
  - `close-attempt --name --attempt`;
  - `assemble-registry [--verify]`;
  - `status`.
- **The verbatim workflow lines** are in the P112 runbook and brief ([SCAN] L369 and L374, documents_scanned: RUNBOOK_V002_C2V007.md and P112_LAUNCHER_BRIEF_V005.md). They were not opened here.

---

## 4. Lane E: the CW8 license (A281 N2; A282 L4916). Exactly one line, never superseded

**Trigger:** S0's serial/twin comparator reads EQUAL with `bitwise_equal` true over iterations [0,1] (A282 L4916). Otherwise there is no license, and S9 runs serial, the automatic fallback (A282 L4908).

### E-01: the comparator-record pre-check [DERIVED: read-only]

**Why derived:** select-workers turns any license defect into a durable serial choice, so root sees the fields the authenticator checks ([CW8L] L3100–3116) before the one-time write. The record is value-free (`values_printed` false, [CW8C] L27).

```
python3 -I -c 'import json,sys; r=json.load(open(sys.argv[1])); print({k: r.get(k) for k in ("schema","verdict","bitwise_equal","iterations_compared","differing_files","not_ready","values_printed")}); print(sorted(r.get("pins",{})))' PASTE_COMPARATOR_RECORD
shasum -a 256 PASTE_COMPARATOR_RECORD
```

- **Expected** ([CW8C] L27; [CW8L] L3101–3116):
  - `schema` `UNT_STEP5_NGC_IDENTITY_PAIR_RECORD_C2V001`;
  - `verdict` `SERIAL_EQUALS_PARALLEL_BITWISE_TAIL_ON`;
  - `bitwise_equal` True;
  - `iterations_compared` [0, 1];
  - `differing_files` [];
  - `not_ready` [];
  - `values_printed` False;
  - the pins keys `['checkpoint_module', 'driver', 'serial_spec', 'tool', 'twin_spec']`.
- **STOP:**
  - any other value. There is no license.
  - The record path lies inside a run root, or contains a protected component such as `ngc3198`, `stages` or `a_side`. The launcher would refuse to read it (FORBIDDEN_* / PATH_*, [CW8L] L235–248), and selection would fall to serial.

### E-02: the license object (ROOT ACTION: exclusive create; no adopted producer, G-25)

It has exactly these 8 keys ([CW8C] L18–25; [CW8L] L3086–3097):

```
{
  "schema": "CW8_PHASE1_LICENSE_CX3V001",
  "date_u": "PASTE_DATE_U",
  "scope": "FULL_MEMBER_F_CALLS_ONLY",
  "comparator_record": {"path": "PASTE_COMPARATOR_RECORD", "sha256": "PASTE_COMPARATOR_SHA"},
  "source_pins": {
    "checkpoint_module": {"path": "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py", "sha256": "069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114"},
    "comparator": {"path": "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/tools/compare_identity_pair_c2v001.py", "sha256": "8e857fff5c2bc16574238cd4fb5c2c510815efe60764f6027d9addd944be0178"},
    "driver": {"path": "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py", "sha256": "577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377"},
    "parallel_solver": {"path": "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_uvtail_c2v001.py", "sha256": "7667025bd9382a58688153fde98bf90f2b67d27baa39a939982631c305c229db"},
    "parallel_worker": {"path": "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/ngc43_coupled_root_worker_parallel_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py", "sha256": "293a417f493fee2b59176bc60873fa3cdea5e586f375efbe51cbd10651e045b1"},
    "serial_solver": {"path": "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_uvtail_c2v001.py", "sha256": "8ef3079b0a23c32c688605e96eb5b79beb79768578cc7aef22ea087c7ae12469"},
    "serial_worker": {"path": "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/ngc43_coupled_root_worker_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py", "sha256": "ee27227c2cee3093589ae6b6546a0d88a1bbe20c47ba4dacff497ad7cc80189f"}
  },
  "seed_serial_spec": {"path": "PASTE_FROM_V006_SPEC_PIN_S0_SEED_SERIAL", "sha256": "PASTE"},
  "seed_twin_spec": {"path": "PASTE_FROM_V006_SPEC_PIN_S0_SEED_CW8_TWIN", "sha256": "PASTE"},
  "full_rss_multiplier": 11
}
```

| Key | Source |
|---|---|
| `source_pins` | exactly CW8P L3–32. It equals [CW8L] L2978 (TESTED from bytes 2026-10-21) |
| `seed_serial_spec`, `seed_twin_spec` | the exact `{path, sha256}` of V006's `SPEC_PIN S0_SEED_SERIAL` and `SPEC_PIN S0_SEED_CW8_TWIN` ([CW8L] L3094–3097, L942) |
| `full_rss_multiplier` | the integer 11 ([CW8L] L2990, L3090–3091) |
| `date_u` | from `date -u` at creation ([CW8C] L20) |

- `PASTE_LICENSE_PATH`: absolute, outside every run tree, with no protected component ([CW8L] L216–248).

### E-03: the license sha [DERIVED: hash]

```
shasum -a 256 PASTE_LICENSE_PATH
```

### E-04: the V006 pre-check [DERIVED: the [CW8L] L3013, L3018 duplicate rule, as a count]

```
V006="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md"
grep -c '^CW8_LICENSE_PIN' "$V006"
grep -nE '^SPEC_PIN (S0_SEED_SERIAL|S0_SEED_CW8_TWIN) ' "$V006"
```

- **Expected:**
  - `0` (grep exits 1 on a zero count);
  - exactly one SPEC_PIN line for each of the two seed names. Copy their path and sha into E-02 ([CW8C] L11 form: `SPEC_PIN <name> <sha256> <abs path>`).
- **STOP:** a count ≥ 1.
  - A license line already exists, and it is never superseded (A281 N2 L4888).
  - A second line would refuse every selection with CW8_LICENSE_REGISTRATION_DUPLICATE ([CW8L] L3018), which makes everything serial.

### E-05: the pin line [DERIVED: printf of a pin line, grammar [CW8L] L3015; [CW8C] L13]

```
printf 'CW8_LICENSE_PIN path=%s sha256=%s\n' "PASTE_LICENSE_PATH" "PASTE_LICENSE_SHA"
```

**The exact grammar the launcher parses** (`cw8_root_license_pin`, [CW8L] L3006–3019):
- The line matches, in full, `CW8_LICENSE_PIN path=(/.*\S) sha256=([0-9a-f]{64})`.
- The most recent preceding line that starts with `## ` must match `## (A[0-9]+)(?=[:\s]|$)`. A `## ` heading that is not an A-entry resets the section, and the line is then refused (CW8_LICENSE_REGISTRATION_FORM).
- Every line of V006 that **starts** with `CW8_LICENSE_PIN` counts, including one inside a code fence.

**ROOT ACTION:** write a new V006 entry and place E-05's output in it **as a bare line**.
- **The form:** column 0; no bullet, indent, backticks or `>`; no trailing whitespace; LF line end.
- **Where:** in a new entry `## A<n>: …` (for example, "the cw8 license is registered: S0 serial/twin comparator EQUAL").
- **Do not** start any other line, now or later, with `CW8_LICENSE_PIN`.
- Respect the write-freeze window (P1.2).
- A license change means a new tool version (A281 L4888; [CW8C] L52).

### E-06: the V006 post-check [DERIVED: the [CW8L] L3009–3019 parse, as read-only shell]

```
V006="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md"
grep -c '^CW8_LICENSE_PIN' "$V006"
grep -nE '^CW8_LICENSE_PIN path=/.*[^[:space:]] sha256=[0-9a-f]{64}$' "$V006"
awk '/^## /{h=$0} /^CW8_LICENSE_PIN/{print h}' "$V006"
```

- **Expected:**
  - `1`;
  - exactly one line, byte-equal to E-05's output;
  - one heading of the form `## A<n>:` (or `## A<n>` followed by whitespace or the end of the line).
- **STOP:**
  - any other result. Do not run S9-04 with cw8 intent, and root rules.
  - A second CW8_LICENSE_PIN line is never the fix (A281 N2).
- The real authentication happens only inside select-workers ([CW8L] L3386–3387). There is no non-committing license check in the CLI (`status` does not call it, [CW8L] L1787–1812): see G-26.

---

## 5. Not covered here, by design

- Everything before u_A on the verdict-day path: sheet `f2a5eec4`, the S0 J addendum, HEADLINE11, W1–W3. That is the 0850 item-2 runbook.
- The seal (S7). That is 0850 item 4.
- S10.
- Phase 2.

S8's reading (`s1_read_c2v002c.py --manifest …`, PROCA L96) comes after both S1 receipts. It is outside "start within minutes of u_A".
