# s0_launch_kit_c2 C2V003: no memory gating (V006 A166)

**Who and what.** A Claude2 root-workflow lane built this on 2026-10-19 (kit assembled about 19:41Z; record test runs 19:41-19:43Z) for root (Claude2, UNT Galaxy Run 120/43). Spec of record: V006 A166, build item 2 ("S0 kit C2V003"). It is a minimal-delta successor of C2V002 (A161). Nothing was launched. No real root_monitor, NGC driver, filler, dry harness or gate was run. Nothing was written under /Volumes/External1. No running process was touched (step-2 R2 and CP-1 pid 6974 included). Every C2V001 and C2V002 file is unchanged (TESTED: `HASHES.txt` and `HASHES_V002.txt` re-verify, all OK, after the C2V003 build). None of this is adopted until root rules on it and Claude3 reviews the delta (A166).

**Labels.** TESTED: run here, result shown. FORMAL: read from the cited bytes. CHOICE: a decision this build made, which root may overrule.

## 1. Bottom line

- **No memory gating (TESTED, N01, N02).** The kits and scripts no longer call the sched v003 admission, the gate's `--hold-check` or `--twin-start-check`, the A147 L3-03 kind check, or the twin's wave-state attestation. Nothing in the kit reads the machine's memory. Jobs start as their design and order allow; macOS schedules memory.
- **RSS cap = physical RAM, 137,438,953,472 B, for the serial and the twin (TESTED).** `hw.memsize` reads 137438953472 on this Mac. `validate` refuses any other RSS cap constant (`RSS_CAP_NOT_RAM`, N04). `monitor-argv` refuses any other `--rss-cap-bytes` (M09, M09b). The launch-record check refuses a launch whose recorded RSS cap is not RAM (K01, T10).
- **Wall and output caps unchanged (TESTED).** Serial 610,324 s and 136 GiB (146,028,888,064 B); twin 22,752 s and 32 GiB (34,359,738,368 B). `validate` still checks both against `CAPS_S45_C2V003.json` (`35f66b6a`).
- **The twin may start any time after the seed serial's LAUNCH record (TESTED, N03).** It still needs the M-15 record and the seed's registry entry, because its spec comes from the seed's fill.
- **The post-launch check is now the launch record against the plan (CHOICE C1).** It replaces the gate reading. A launch whose `<receipt>.launch.json` differs from the plan is stopped at once, recorded as MISLAUNCH, and relaunched as attempt k+1. The relaunch path is unchanged.
- **Tests: 26/26 MUST_PASS and 73/73 MUST_FAIL in each of two record runs, plus 3 OBSERVED.** The real-pin rows refuse against the live V006: it has the 15 GATE_PIN lines but no HANDOFF_PIN, SPEC_PIN or WATCH_PIN.

## 2. Files (sha256 from bytes; full values in `HASHES_S0_KIT_C2V003.txt`)

| File | sha256 | What |
|---|---|---|
| `s0_kit_c2v003.py` | `e58c8605` | Checks and custody records. It pins the record writer `a10965b7` and `GATE_DOCUMENT_PINS_V002.json` `5e688882` by sha |
| `launch_s0_serial_root_c2v003.sh` | `4ee6b656` | `<seed\|j0\|j1\|j2> [--attempt K]`; DRY by default; `--launch` for root only |
| `launch_twin_root_c2v003.sh` | `51778b17` | The cw8 twin; DRY by default; no `--wave-state` |
| `twin_kill_watch_c2v003.sh` | `88e7c898` | The A141 L4 kill trigger; only the kit name and sha change |
| `s0_prelaunch_record_c2v001.py` | `a10965b7` | **Reused unchanged.** The M-15 record writer |
| `GATE_DOCUMENT_PINS_V002.json` / `.md` | `5e688882` / `5d30ccf9` | **Reused unchanged** (C2V002 data) |
| `tests/test_s0_launch_kit_c2v003.py` | `8001c2a7` | 102 rows; record runs `tests/runs_v003/RUN_20261019T194148Z_6125`, `RUN_20261019T194231Z_11730` |
| `DIFF_S0_KIT_C2V002_TO_C2V003.diff` | see HASHES | Unified diff of the four code files and the test, C2V002 to C2V003 |
| `build/assemble_s0_launch_kit_c2v003.py`, `build/src/*c2v003*` | see HASHES | Assembler and code templates (sha constants filled from bytes) |

Delta size (lines removed / added): kit 439 / 172 (1,154 lines now); serial script 46 / 31; twin script 59 / 32; kill watch 4 / 5.

## 3. Every removal

**Kit (`s0_kit_c2v002.py` to `s0_kit_c2v003.py`):**
1. The `admission` subcommand: the sched v003 `ngc_admission` class (`bdb44eeb`), its class and gate consistency checks, the pinned gate's `decide()` on a warmed sample, and the A133 §1.4 103 GB rule (`a133_memory_ok`, `A133_*` constants).
2. The pins `ngc_admission` and `gate` (`736a3438`), from REAL, the plan, the shell assignments (`PLAN_GATE`, `PLAN_GATE_SHA`) and the synthetic-pins schema.
3. The `confirm-kind` subcommand (A147 L3-03): `--hold-check` polling, `kind_reading`, `real_hold_check`, `pid_alive`, `EXPECTED_KIND`, `EXPECTED_PHASE`, the `kind_check/` directory and the `S0_KIND_VERDICT` file.
4. The `gate-cli` synthetic emulation, with `FakeClock`, `substitute`, `synthetic_snapshot`, `load_gate`, `make_gate`, `warm`, the three snapshot templates and the synthetic keys `snapshot` and `snapshot_after_launch`.
5. The `wave-state` subcommand (A143 D2/D3, A140 N2).
6. The ENDED outcome (schema `UNT_S0_ENDED_BEFORE_KIND_READ`, the `ended_record` path). It existed only for "the monitor ended before the gate read its run". With no gate reading it cannot arise. A monitor that ends before writing `.launch.json` still gives the exit-5 alert, unchanged.
7. The LAUNCH flag `HOLD_TRUE_AT_SERIAL_LAUNCH`, which came from the gate's hold reading.
8. The caps-file equality on `rss_cap_bytes`. The file's 32 GiB and 86 GiB are superseded by A166; wall and output are still compared.

**Serial script:** step 8's admission call and `--dry-admission`; `--kind-confirm-timeout-s` and `--kind-poll-s`; the confirm-kind step and its ENDED branch; the D4 "22.4 GB" note in the final message (A143 D4 is a gate-successor rule).

**Twin script:** the required `--wave-state` and its check; `--twin-start-check` (real) and `gate-cli` (synthetic); `--dry-admission`; `--kind-confirm-timeout-s` and `--kind-poll-s`; the confirm-kind step and its ENDED branch.

**Kill watch:** nothing removed.

## 4. Every kept check

- **Script self-checks:** kit sha and record-writer or kill-watch sha before anything runs; with real pins, driver `577f8c94` and monitor `ba031c23`.
- **Synthetic fences:** synthetic pins may not name the real monitor or driver, or a `root_monitor_c2v*.py` name; a synthetic `--launch` may not use `/Volumes/`.
- **Paths (validate):** the launch root is absolute, normal, a real directory and not on `/Volumes/`. The run root is absolute, normal and exactly one level under `/Volumes/External1`, named `NGC_*`. Neither may be spelled through `runs_ext` or contain a `uvt_` component, `UNT_INTERNAL_RUNS`, the C5H marker, or `ngc3198` in the run-root name.
- **Pins from bytes:** driver, monitor, filler, dry harness, S0 record (with the role's θ key), policy, acceptance, LO, GQ gate, gate-document pins, and the role's EPS and GQ binding; caps file wall and output.
- **V006:** pin lines parsed with the record writer's parser. For `--launch`, HANDOFF_PIN, SPEC_PIN and WATCH_PIN are required.
- **M-15 first (A142 item 6):** only the seed serial's attempt 1 writes the record, by exclusive create, as the first action. It refuses if launch records exist without it. J serials, the twin and relaunches refuse without it.
- **Order (`order-check`):** seed serial first; one LAUNCH per name; attempt k unrecorded and no later attempt recorded; attempt k > 1 only after attempt k-1's MISLAUNCH record, under the same M-15 record sha, with its monitor receipt present; the twin needs the seed's LAUNCH record and registry entry.
- **Spec:** fill from the V006 HANDOFF_PIN; `fill-check` (handoff schema, mode, θ key, source, certificates, branch, admission label, policy, acceptance, V007 pin form; fill receipt; leaf 1 and 8; per-point EPS and LO; label; the pair differs only in the leaf; spec sha equals the V006 SPEC_PIN).
- **Dry plan (RI45-13):** a fresh dry plan with the pinned harness; `dry-verdict` reads the blocker lists, not the label.
- **Registry:** exclusive create; reused only for the same spec and V006 pins; no registration after a LAUNCH.
- **Launch form (D3):** driver and monitor sha from bytes twice. `monitor-argv` requires exactly `PY -I -B <monitor>` plus the 8 flags in order, no `=` forms, a 64-hex driver sha equal to the pin, an absolute `--spec`, an absolute `--outdir` under External1 equal to the planned string, `receipt = outdir + .receipt.json`, and caps equal to the plan's (RSS = RAM).
- **Preconditions:** `ext1-check` (mounted, not symlinked, outputs absent, free space at least output cap + 20 GiB, the disk guard A166 keeps); `step2-check` (A135.5; see note N1); `watch-check` (the WATCH_PIN watch runs; the watch is passive, A166); the V006 write freeze until the first receipt; the UTC second advances past the record's; the spec sha equals the SPEC_PIN just before launch; `caffeinate -i -w`.
- **After launch:** wait for `.launch.json` (alert exit 5 if absent). The launch-record checks, unchanged from C2V002 plus `launch_json_parseable`: schema, planned command, driver pin, spec pin, monitor sha, caps (RSS = RAM), retries 0, integer child pid, launch utc after the M-15 record. On a mismatch, the stop runs with every `kill-target` check (child alive, group leader, exact command, parent = monitor pid, spec sha and leaf), TERM then KILL after 15 s, then waits for the monitor receipt and writes the MISLAUNCH record naming the relaunch.
- **LAUNCH record:** requires a CONFIRMED launch verdict for this monitor pid, this plan's sha and these launch-record bytes. A change in V006 between the record and the first launch is flagged (exit 4).
- **Twin kill (A141 L4, kept by A166 to save compute):** the kill watch starts after a confirmed twin launch, with `--mon-pid`; it stops the twin when `iteration_0001/COMPLETED.json` and `uv_tail_sidecar/iteration_0001.json` both exist, after the kill-target checks, and writes the kill record.
- **All writes** are exclusive creates with fsync.

## 5. CHOICES (root may overrule each)

- **C1. The launch-record check decides LAUNCH or MISLAUNCH** (new subcommand `launch-check`, verdict `S0_LAUNCH_VERDICT_C2V003`). In C2V002 these same checks only annotated a LAUNCH record, and a failure gave exit 5 with the run left going. The commission keeps the relaunch path, and without the gate reading nothing else would trigger it. A launch whose record differs from the plan is not the call of record, so it is stopped (fail closed). The alternative is C2V002's behaviour, which leaves the relaunch path with no trigger.
- **C2. A launch-check error or an unreadable launch record reads MISLAUNCH** (fail closed).
- **C3. ENDED is removed** (section 3, item 6).
- **C4. The caps file stays pinned** for wall and output only. RSS comes from A166 as the constant `RAM_BYTES`.

## 6. Notes for root (unchanged in this build)

- **N1. The step-2 precondition is kept.** A135 item 5 reads "**Memory.** The identity pair runs only after step 2's last receipt". Neither A166's removal list nor this commission names it, so the kit still requires `--step2-receipt` (minimal delta). If root rules it memory-only, dropping it needs a C2V004. The S0 handoff's V007 pin (RI45-05, the sealed compare's verdict) follows step 2 in any case.
- **N2.** The reused record writer still lists "A143 D2" among its rule labels. This is text in the M-15 record only, and the writer is unchanged by design (`a10965b7`).
- **N3.** The dry-plan harness still runs with single-thread BLAS environment variables, as in C2V002. That is the simulate-only dry plan, not the run.
- **N4.** A161 N1 ("the four serials first; the twin when the gate admits it") is superseded for the kit by A166. The kit enforces only "seed first".
- **N5. One kit version per launch root (A161 N9).** C2V003 counts only C2V003-named records, so a C2V002 seed launch does not satisfy C2V003's seed-first check (fail closed).
- **N6. V006 moved during the work:** `db163b3f` → `13fc80c2` → `b2b3ad7f`. It now carries the 15 GATE_PIN lines and `ROOT_LISTED_ROW_GATES NONE`, but no HANDOFF_PIN, SPEC_PIN or WATCH_PIN. The real-pin DRY refuses at "no HANDOFF_PIN S0_SEED", and `--launch` refuses at validate.

## 7. Tests (TESTED; two record runs, 26/26 + 73/73 each, 3 OBSERVED)

**Row accounting (TESTED, by comparing the two RESULTS files).**
- 89 of C2V002's 117 ids are present in both: 84 unchanged in substance and 5 re-purposed (below). The unchanged rows carry C2V003 names, RSS = RAM, and launch-check fields where they read the kind check.
- 28 ids are removed. With the old T02, that makes 29 removed rows.
- 13 ids are new: 89 + 13 = 102 rows.

**Re-purposed under the same id:**
- **K01:** was "GENERIC kind is stopped"; now "the launch record carries a 32 GiB RSS cap, not RAM: stopped, MISLAUNCH".
- **T10:** the same change for the twin.
- **L14:** was "the gate MEMORY_HARD refusal after the M-15 record"; now the disk-guard refusal after the M-15 record.
- **L16:** was "j0 beside a holding twin, exit 4 with the gate flag"; now j0 after the seed, exit 0, no flag.
- **T02:** was "the twin refuses mid-wave"; now "the removed `--wave-state` option is refused".

**Removed (gate-related; 29 C2V002 rows):**
- U01 (the A133 103 GB rule) and U02-U14 (`kind_reading`);
- GC01-GC03 (the gate CLI emulation against the real `main()`);
- K07-K10 (NGC_UNIDENTIFIED, not seen, probe failed, phase after);
- E01 and E02 (ENDED);
- T02 (old), T03 and T04 (wave state: mid-wave, direct batch pending, stale);
- T05 (`--twin-start-check` refusal);
- T09 and T11 (twin not seen, twin NGC_UNIDENTIFIED).

**New:**
- **MUST_PASS, launch without a gate:**
  - N01: static checks (16 subcommands; no gate or ngc_admission pin; no gate, kind or memory token in the kit code or the scripts; CAPS = RAM);
  - N02: the seed launch ran no admission, gate call or kind check, and its RSS cap is RAM in the plan, the argv and the launch record;
  - N03: the twin launches straight after the seed's LAUNCH record, with no J serial and no wave state.
- **MUST_FAIL, RSS cap not RAM:** N04 (validate with the C2V002 32 GiB and 86 GiB constants: `RSS_CAP_NOT_RAM`), M09 and M09b (argv 32 GiB, and RAM - 1), K01 and T10 (launch record).
- **MUST_FAIL, relative paths:** M10 (relative `--outdir`) and L14d (relative `--step2-receipt`), with the ported L02 (run root), L06b (launch root) and M02 (spec).
- **MUST_FAIL, missing M-15:** N06 (a twin with no record: `M15_RECORD_MISSING`), with the ported L13 and L13c.
- **MUST_FAIL, also new:** N05 (synthetic pins with the C2V002 gate keys), K11 (a launch record with retries 1), L18 and L18b (the removed `--dry-admission` and `--kind-confirm-timeout-s` options).

**Test-side changes:**
- Stub-monitor variants `rss32` and `retries1` produce the mis-launches.
- Z01 and Z01b now run only while the live V006 has no HANDOFF, SPEC or WATCH pin line, so the tests can never drive the real filler or dry harness.
- `kit_files` in RESULTS hashes an explicit file list instead of every file in the folder, so `NGC3198_GEOMETRY_TRACE_C2V004.json` is not opened.

## 8. Conduct and disclosures

**Opened (named paths only):**
- V006 (A130-A166 read; a pin-line grep);
- the C2V002 kit files, README, HASHES and test;
- the C2V002 builder header;
- the path list of `FREEZE_EXPECTED_INPUTS_C2V002.json`;
- a key grep of `CAPS_S45_C2V003.json`.

**Hashed without reading:** the gate documents and the FREEZE-listed files (tests G01 and F03), the real driver and monitor (tests L10 and Z01).

**Not opened:** run trees, External1, `~/.codex`, `c5h_hull_c2/`, `UVT_*`, and every NGC3198-named file other than V006.

**Not run:** the real filler, dry harness, gate, root_monitor and driver. No process was signalled except the test's own stub children.

**Writes.**
- Development and one full test run were in the session scratchpad first.
- In this folder every C2V003 file was written once, by exclusive create: templates, assembler, the assembled code, the test, two runs under `tests/runs_v003/`, the diff, this README and `HASHES_S0_KIT_C2V003.txt`.
- No C2V001 or C2V002 file was touched.
