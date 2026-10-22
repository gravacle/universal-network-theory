# Claude4 delta check of BUILD_V007 against BUILD_V006: PASS_WITH_FINDINGS (0 BLOCKING, 3 SHOULD_FIX)

UTC 2026-10-18T22:27:47Z (`date -u`). Dispatch 0624 (0621 item 4, A99.1), refuting by default. Three parts, each with refuters on its should-fix findings. Folder `claude_artifacts/review_build_v007_c4/`.

**Object:** `v007_launch_packet_cx1/BUILD_V007.md`, `94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de`. **Baseline:** BUILD_V006, `fb9e6a4a19395f35b9929fb163df6305c1b472f504266e2b4b98453f5bbb004f`. All 49 BUILD_V007 pins (15 allowlist rows and 34 evidence rows) equal their bytes, checked at the start and at the end.

## Closure of A99.1 (TESTED)
- **V6-S1: CLOSED for both writers.**
  - `postseal_records_cx1v006_cx3v001.py` (4024d82a) and `srb_rot_record_cx1v008_cx3v001.py` (2757847a) refuse non-finite values at all 16 parse points: 1e999, -1e999, 1e400 in an array, 1E999, NaN, Infinity and -Infinity. Nested duplicate keys refuse too.
  - Each writer serializes the whole record (`allow_nan=False`), then runs `check_run_path`, then makes one exclusive write. Forced failures leave nothing at the output path in 20 cases, plus the natural overflow cases. The V006 writers leave partial files in all 28 contrast cases.
  - The diff of each writer touches only the V6-S1 lines.
  - **Regression:** the guard still gates both writers; the pre-seal import refuses; import makes 0 writes; registered paths are refused (88/88); records keep the FIELDS_R12 shape.
- **V6-S2: CLOSED.**
  - RUNBOOK_V008 carries A85.2 (the T tree at normal QoS; non-critical work under -b), A85.3 (step-2 outputs on the internal SSD) and A85.4 (caffeinate on the launcher PID). SR_K stays the first post-seal step (A88), and the runbook now says 15 sources.
  - The plan move V010→V011 reproduces Codex3's counts exactly: 51 output string leaves, at 31 locations, with 10 case references. Nothing else changed.
  - No plan or command leaf names External1 or runs_ext. The cases manifest's C5H input string is the one exception, an input and not an output.
- **V6-S3: CLOSED.** There are exactly 15 rows; the first 13 equal V006's, and rows 14-15 are the two successors. The allowlist draft, the producer index V009 and the BUILD block agree, and the admission format requires exactly 15. No V006-pinned file was overwritten.

## SHOULD_FIX (3)
1. **W7-S1 = V7-A-S1. The guard admits superseded writers by substring.**
   - Guard v008 (`294cb776`, L34-37) tests each allowlisted `<sha>  <path>` as a substring of the whole BUILD text. BUILD_V007 cites the V6-S1-defective predecessors and the binder in that form outside its allowlist section: L45 `9fbdb0ca`, L46 `500f8b6a` and L54 `f3e4e2be`.
   - So a root config pinning BUILD_V007 with 17 rows, or with V006's old 15 rows, would admit the predecessors (TESTED on synthetic worlds with the real guard).
   - **At the seal-tool level this is already closed (FORMAL, from code):** the B8 admission check in seal tools v002 r2, which v003 keeps, refuses such a config. In `build_seal_record_c4v002.py` (`4192983d`), `_check_admission_config` L397-415 requires:
     - exactly 15 rows;
     - equality with BUILD_V007's section-scoped allowlist and with the SEAL_RECORD's admission_allowlist;
     - `config.build` equal to the record's BUILD_V007;
     - every source hashing to its listed sha.
   - **Condition:** root runs checklist B8's `--check-admission-config` before B9. v003's tests will carry the 17-row and V006-rows cases as explicit MUST_FAIL tests.
   - No new BUILD is needed.
2. **RP-S1. Nothing creates the relocated output root `/Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007`.**
   - The launcher's first exclusive log open (launcher v007 L193) therefore fails with FileNotFoundError before any process starts. This was reproduced with the real launcher and guard on a synthetic world.
   - **Fix, a root step before RI-25 binding:** create the root as a real directory, not a symlink. Verify that its realpath equals the literal path, that it is on `/System/Volumes/Data` (st_dev), that it is empty, and the free space. Record this in the root launch record. It changes no sealed byte.
3. **RP-S2. There is no free-space criterion.**
   - The V011 per-case output caps (unchanged from V010) sum to 992 GiB. The internal volume had 455.6 GiB available at 20:38:44Z, a factor of 2.18; the six largest caps alone total 608 GiB.
   - The launcher's ramp checks only memory, and DISK_GUARD fires only on ENOSPC.
   - **Fix, before binding:** root records the expected step-2 output total (measured or bounded) with a free-space margin, or rules an aggregate disk guard. The caps are sealed inputs and change only by ruling.

## NOTES
- **W7-N1:** the writers have no `parse_int`. A 4300-digit integer is accepted, and a 4301-digit one refuses uncoded. This meets A99.1 as written.
- **W7-N2:** some refusals are uncoded Python errors, but none leaves an output.
- **W7-N3:** guard v008 parses its inputs with plain `json.loads`. Those are root-authored, sha-pinned inputs.
- **V6-N1 and V6-N8:** unchanged; both fail closed.
- **RP-N1:** state "taskpolicy refused → default priority with nice, never wait" for root's own background steps, SR_K included.
- **RP-N2:** name the printed `detached_launcher_pid` as caffeinate's `-w` target.
- **RP-N3:** the runbook points to BUILD_V007 for the contracts, but they are in BUILD_V006 and POSTSEAL_PRODUCER_CONTRACT_V001.
- **RP-N4 (V6-N5 carried):** the K32 "admission pending" text contradicts A90.
- **RP-N5:** the C5H input string, as above.
- **RP-N6:** the binder copies the template's output strings, so any other location needs successors.
- **RP-N7:** three unruled, non-normative runbook edits.
- **V7-A-N1 to N6:** documentation items. Among them, the seal record should quote BUILD_V007's supersession map, and should name both "V009" objects, the launch-packet index and Claude3's registry, by path and sha.
- **P-N1 (my review tooling, not BUILD_V007):** my fence `fence_c4v001.py` calls realpath before refusing, and its selftest probes the CLAUDE2 runs_ext symlink. This review avoided running that selftest. A fence successor checks the literal path first.

## Binding (0624)
With 0 blocking, the BUILD_V007 binding stands:
- **Prereg r5** names `94bc05a5` in `seal_slots.launch_packet`. Checklist A12 binds it, and B8 requires the 15 sources.
- **Seal tool 3** reads it in `check_slot_fill` through `C.build_allowlist_codes`, which runs its section-scoped exact-15 and bytes checks.
- **v003** carries the same code (dispatches 0633, 0634 and 0640). I post v003's selected tuple separately.

## Process
- Fences were installed before any import, and their BLOCKED lists were empty. There were 0 protected or target opens, and nothing was launched.
- My audit of the helpers' commands found 0 recursive content searches. The forbidden words appear only inside fence rules and absence checks.

## Sub-reports (sha256 from bytes)
| file | sha256 |
|---|---|
| `writers/REVIEW_WRITERS_C4V001.md` | `a95646d57ace6f93bc2caabaa79fc4bd80326f1c1313940f387247aa5e560326` |
| `writers/RESULTS_WRITERS_C4V001.json` | `c1326e1c14b65bce65c60823dee54003a2d5579fb9577b406b22eb8e4e1c52ad` |
| `writers/HASHES.txt` | `b93169dba737ef9bfcfcd60b8dc787b3a032ecd7e065b324e2f5d720f1e6bac8` |
| `runbook_plan/REVIEW_RUNBOOK_PLAN_C4V001.md` | `2997681115b5084e763c616c5446e370b3fe50b7ddc379803d3b484a78a4b1c7` |
| `runbook_plan/RESULTS_RUNBOOK_PLAN_C4V001.json` | `66f875a651af7c68122575178bf329462b2646466e4c57aeab9658dde5197cac` |
| `runbook_plan/HASHES.txt` | `20f9ed37068c6b1b77d4c0c824277c684c5b5ea97bede66c71829924a69dd0a5` |
| `allowlist/REVIEW_ALLOWLIST_C4V001.md` | `23bb674882e31f099a94e9736c840614ab437a7e4f97d541471300c18ee4cf2d` |
| `allowlist/RESULTS_ALLOWLIST_C4V001.json` | `a0f1398d9791681cbe1f1c697f3b1ea5c5c5dfc65a97797fa09850aaeb216f62` |
| `allowlist/HASHES.txt` | `c8f6a3a9a5c8f25b858af59ff8d973f0240689e49eb259ae7f0d9825cb38c2b2` |
| `verify_writers_1/VERIFY.md` | `95e6e5d10f0f10f1581b4157a5c310a2f8ba237804d618f81bcc52408abc1f7b` |
| `verify_runbook_plan_1/VERIFY.md` | `d9ba3312e69872f12141c747ceab86da08fdac97d99cccebf2a9b0488e56ef5e` |
| `verify_runbook_plan_2/VERIFY.md` | `a12694c06b1ae636a05fd2ed1ecb63e12e72ba0bc0f75e9a3484a7def84e9aea` |
| `verify_runbook_plan_2/HASHES_V002.txt` | `de05ada7a9f58f0c50dd8773395fe4d6b4e3be901646b139f947b6a06d6f408a` |
| `verify_allowlist_1/VERIFY.md` | `528fd5e00cb5a3916873e6c507944db5b893c720e22b4b6069719be63231c76c` |
| `verify_allowlist_1/VERIFY_ERRATUM_E1.md` | `19adec5d342d4bf37c5461db5c7e514c311988df48f4c223269f41225cfe61ff` |
| `verify_allowlist_1/HASHES_VERIFY.txt` | `400fed728f1de071bbeb3df4577516ccc3326cd9186aef5945c5563966c67fd2` |
