# AUDIT_C3V001: the S3 → S11 critical-path wall-clock audit (root 0822; 0826 item 3)

**From:** Claude3 lane. This is the helper's draft; the lead files it. **Research window:** 2026-10-21 12:26–12:56Z (`date -u`).

**Read-only.** No launch, and nothing opened from run trees, receipts, step-2 outputs, NGC3198 data, V007_POSTSEAL_RECORDS or the network. Every command ran under `taskpolicy -b`.

**Labels:**
- TESTED: from bytes (sha, grep, sysctl).
- FORMAL: from reading code or records.
- Every saving is UNTESTED.

**Rule (A258 L4446–4449):** minimize wall clock to S10, then to S11. Physics, custody and blinding stay unchanged. A lever that changes a value or the engine's path is FAIL.

## 0. Bottom line
1. **The A263 exception list (due before Thu 03:00 CDT) is empty.**
   - No §3–§8 tool on sheet `f2a5eec4` checks its own QoS, and neither does any module they visibly load by path (TESTED for those files).
   - Root can drop `taskpolicy -b` and `nice -n 10` from every §3–§8 command.
2. **After u_A, the binding S10 term at E is probably S8, not S9.**
   - The S1 pair runs serially. Three things force that: CHOICE C14, guard014's one-call S1 overlap rule, and the machine lock.
   - So S8 ≈ 4–6 h of row-32 chain plus 32–36 h, against S9 ≈ 34–38 h at cw1 or 24–28 h at cw8.
   - **When N_new ≥ 1, cw8 (A259) alone saves at most about 2 h on S10, and so does S1 concurrency alone. Together they save about 11 h (E).** When N_new = 0, S1 concurrency alone saves about 14 h.
   - C14's own stated basis was that each S1 head must meet the machine gate. A166 removed that gate. **Top recommendation.**
3. **The sheet launches only the S0 seed and the twin.**
   - J0–J2 have no pin lines and no commands on it (TESTED). They are three of the four S0 serials that A161 calls Phase 1's critical path.
   - Add them to root's A263 W3 template.
4. **Candidate 1 is PARTIAL.**
   - Background QoS is enforced and recorded inside the pinned c3v004 `run_point`, not only in the list runner's argv. A one-flag successor would therefore refuse.
   - march0+ CP-1 is S11 work: Phase 1 ends before march0.
   - It is worth a Claude3 build for S11 (E ≈ 10–20 h), but only after the S10 levers.
5. **Two night-lane waits remain on the S10 path.** Both can be pre-staged:
   - Codex3's campaign policy review at drive mount (S5);
   - the row-32 EPS review and the S1 C1 prerequisites at u_A (S8).
6. **The seal is not critical at E.** It becomes near-critical if L2, S1 concurrency and cw8 all land. The concrete hazard is the V006 write-freeze window colliding with the row-32 pin entry near u_A.

## 1. A263: which verdict-day tools check their own QoS

**Method.** On each file:
- `grep -c -i` for `getpriority|PRIO_DARWIN|background_qos|taskpolicy|nice|setpriority|qos`;
- then a second pass for `psutil|PRIO_|os\.nice|sched_|cpu_count|perflevel`.

Every sheet tool's sha equals the sheet annex (L203–236); the loaded modules were hashed from bytes. TESTED.

| Sheet section (lines) | Tools (sha8), with the modules they load by path | Self-check |
|---|---|---|
| §3 (L64–69) | ea_replay_cx1v012 `380e2d81` (driver r5 `b5cc62af`); ra10_checkpoint_cx1v012 `b66dd9c0` with route_a_tail_replay_cx1v005 `9e49aad9`, common_tests_v001 `52906fde`, kbig_build_timing_c2v002 `83b9735e` and owned_uv_tail_nodes_v001 `c8a04fb5`; aggregate_records_cx1v008 `9794123d` with compare r5 `78ac63b7`; postseal_records_cx1v006_cx3v001 `4024d82a`; producer_guard_cx1v008 `294cb776` | none |
| §4 (L79) | compare r14 `a99105a1` | none |
| §5 (L90–92) | run_fenced_c4st2 `fe904509` with fence_c4v002 `c993d34c`; make_b1_cascade_c4v002 `a7a5fe58` (stdlib only) | none |
| §6, §8, §9–10 | regenerate_h3_c2v004 `ad5cee08`; make_campaign_cascade_c2v004 `5014b04f`; apply_h3_fields_c2v006 `0ed72837`; produce_final_step4_specs_c4v004 `fcbf1c3e`; fence_c4v003 `5851f42f`; step4_prelaunch_c2v005 `117b3520`; envelope c2v003 `9d531381` | none |
| §7 dry plans (L129) | drivers `577f8c94` and `b5cc62af` | none |
| §11 | s0_kit_c2v003a `fdc0ee6c`; launchers `621263a2` and `f199544d` | none |
| §9–10, generated launch | launcher015 `cd987edd` L43–46 runs `taskpolicy -B -p <self>`, which forces normal QoS. binder c2v011 `d3d9702e` L25–29 refuses nice and renice. guard014 `6efdca01` L319 holds an attestation dict. | QoS-aware, and already at normal QoS |

**Must keep `-b`.** These tools are off the sheet but on the wave path, and they do check their own QoS:
- CP-1 runner c3v004, L231–233, called at L466;
- list assembler cx2v002 `verify`, L192–193;
- list assembler c2v001, L191–192;
- registry assembler c3v004, L510–511.

guard014 L319 `background_noncritical_lanes: True` is root's attestation when HEADLINE11 is admitted. Keep the hedge CP-1 runs at `-b` for as long as root attests it.

## 2. The critical path at E (UNTESTED; each row cites its basis)

| Segment | E | Basis | Binding at E? |
|---|---|---|---|
| S4T R3 last receipt | Thu 22, 09:30–10:30Z | A260 L4505 | yes |
| Receipt → HEADLINE11 launch: root's serial §1–§10; the §5/§6 gating reviews now take minutes | 2–4 h | sheet; A268 L4631. No gate runtime has been measured anywhere. | no: about 6–12 h of slack before the drive |
| HEADLINE11, then acceptance and evidence | about 24 h, plus 1–3 h | A247 L4234–4238; A192 L2347 | no at E; yes at U, or if the drive arrives early |
| Drive mount → W1: storage check, volume fields, Codex3 policy review | Fri night CDT | A256 L4401; A247 L4252; V006 L2669 | **yes** |
| W1 plus the W2/W3 direct calls (L2) → u_A | about 20–24 h | A262 L4532 | **yes** |
| S8: the row-32 chain, then the S1 pair in series | 4–6 h, plus 2 × 16–18 h | A160 L1566, L1754; A201 L2572; S1 registration L214, L264 | **yes** |
| S9: 0–3 new calls (N_new). A call takes 31.90 h at cw1 and 21.58 h at cw8. The join includes R, the remaining time of the S0 serials. | — | S9_MAKESPAN L21–26, L48–49, L70–74 | only once S8 is shortened |
| Seal: Claude4 renders after Fri 19:00Z | — | STEPS L11; V006 L1907 | no: 1–2 d of slack |
| S10 freeze chain | serial by registration; duration UNTESTED | RUNBOOK L68–106 | yes, as the tail |

**Host (TESTED, `sysctl`):** Apple M5 Max with 18 cores and 128 GiB:
- 6 "Super" cores (perflevel0);
- 12 "Performance" cores (perflevel1).

Background QoS confines a process to the 12-core tier (FORMAL).

## 3. Ranked levers: S10 levers first, then S11

Physics, custody and blinding are NONE for every lever unless the entry says otherwise.

**L1. S8 · (a) not inherent, plus (c) · Run the S1 pair concurrently.**
- **Today.** guard014 L338–339 requires `len(calls)==1` (S1_OVERLAP_ONE_CALL_REQUIRED). The launcher lock refuses a second batch (launcher015 L3–4). So the pair runs in series (A150 L1006; S1 registration L214).
- **Change.** Admit one POST_S1 overlap batch of exactly {S1_UA_C3T, S1_UA_C4T}.
- **Root ruling.** Root amends C14 before any S1 number exists:
  - C14 (S1 registration L264) is "timing only, so A48 does not apply".
  - Its machine-gate basis was removed by A166 (L1464–1468).
  - C16 (L266): "order changes no value".
- **Saving on S10:**

  | Case | E | U |
  |---|---|---|
  | With cw8 | ≈ 11 h | ≈ 18 h |
  | N_new = 0 | ≈ 14 h | ≈ 18 h |
  | N_new ≥ 1, at cw1 | 1–2 h | ≈ 18 h |

  Basis: about 16–18 h per S1 call (A201 L2572), and the S9 terms in §2.
- **Cost.** No extra calls. There are about 1.4–6 h of overlapping route-A load (16 workers), which the existing ramp staggers.
- **Build: Y, small.** New guard, launcher and binder successors, as new files. Fold them into the A265 item-2 overlap unit. The HEADLINE11 pins stay byte-identical.
- **Risk.** A defective successor makes one S1 call unacceptable and costs a rerun of about 16–18 h. The fallback is one call per batch, as now.
- **Effects:**
  - physics NONE: the same spec bytes, driver r5 and single-thread BLAS;
  - custody: new reviewed pins only, with the admission closure (A240 item 4);
  - blinding NONE: DDO only, and the reading still comes before any NGC read (S1 registration L224).
- FORMAL.

**L2. S4 · (b) · Put S0 J0–J2 on the verdict-day sheet.**
- **TESTED:**
  - §7 (L124) pins only S0_SEED.
  - §11 (L171–180) launches only the seed and the twin.
  - A grep of `f2a5eec4` for `j0|j1|j2|S0_J` finds nothing.
- **FORMAL:**
  - The kit needs HANDOFF_PIN S0_J{n} and SPEC_PIN S0_J{n}_SERIAL for each role (kit L390–392, L432–434; launcher L12, L20–26).
  - The J serials launch right after the seed's confirmed LAUNCH (A161 L1362–1364).
  - They are reused as F points (S9_MAKESPAN L26).
- **Saving.** E 0–9 h on S10, measured against discovering the gap as late as u_A. In that case the J calls end about 32 h after u_A, which is longer than S8 once L1 lands. U up to about 2 days.
- **Cost.** Three fill, dry-plan and launch cycles. **Build: N.**

**L3. S8 · (b) · Pre-stage the u_A front chain.**
- **(i)** Arrange a Codex3 window and a scripted EPS check for row 32 (A202 item 2: E1–E10).
- **(ii)** Root writes templates now for the row-32 row file and its V006 pin entry (A160 L1754).
- **(iii)** Re-date the S1 C1 prerequisites from "about Oct 30" (A240 L4104; A238 L4054) to before W3 acceptance, which is about Sun 25 under L2:
  - Codex3's S1 C1 policy review;
  - the freeze binding A268's ordered six producers (L4623);
  - the source-closure delta (A240 item 4);
  - root's dry launch on the real admission (V006 L2179).
- **Saving.** E 2–5 h. U 1–2 d, if an early u_A finds these prerequisites still open.
- **Cost.** Lane time only. **Build: N.**
- **Risk.** None new.

**L4. S5 · (b) · Codex3's campaign policy review at drive mount.**
- **Today.** The review binds `certificate_ledger` once the W1 work dir is fixed on the new volume (V006 L2669; A247 L4252).
- **FORMAL.** The signed review carries the `{schema, path: <work_dir>/CERTIFICATE_LEDGER.jsonl}` object (README_CAMPAIGN_CERT C2V001 L53–55).
- **Change.** If root fixes the mount point and the work-dir path now, Codex3 can sign before the drive arrives. Only a path-equality check is then left for mount time.
- **Fallback.** If the review schema binds a UUID or inode field (UNTESTED), Codex3 pre-reviews a parameterized recipe and arranges a night window, as in 0829/A268. The same applies to A265 item 2's root-bound overlap admission, which binds the W1 work dir.
- **Saving.** E 1–4 h; U 6–10 h, if the review would otherwise wait until morning.
- **Build: N.**
- **Risk.** The volume is named differently from the plan, and the fallback applies.

**L5. S9–S10 · (b) · Do the value-free work per call, as each call finishes.**
- NGC ρ registration for each new Phase-1 point at its launch. It is point-derived, and it is required before acceptance (V006 L2857).
- Custody close at each receipt. The snapshot refuses until every close is done (RUNBOOK L70).
- The value-free 1a/1b PLAN at u_A (RUNBOOK L62).
- The G16 3(b) Phase-2 ruling now (V006 L3582).
- **Saving.** E 0.5–2 h. **Build: N.**
- **Blinding NONE.** No NGC value is read, and acceptance stays after the seal.

**L6. S7/S8 · (b) · Schedule the seal against L2.**
- **Change.** Fix the V006 write-freeze window now, outside u_A ± 1 d, because row 32 needs a V006 entry before its CP-1 run (A160 L1754; A201 L2569).
- Reserve Claude4's render at Fri 19:00Z (V006 L1907), with Claude3's r3a delta review right after it.
- **Saving.** E 0. U up to about 1 d of S8 stall avoided. **Build: N.**

**L7. S3 · (c) · Drop QoS on verdict night (the §1 list).**
- **Saving.** E ≈ 0 on S10, because HEADLINE11 has slack against the drive. U 0.5–2 h, rising to 1:1 if the drive arrives before HEADLINE11's evidence.
- **Basis.** The gate runtimes and this host's background-to-default speed ratio are both UNTESTED.
- **Build: N.**

**L8. S4 · (a) not inherent · Run S0's branch ahead of HEADLINE11's chain.**
- **TESTED (grep):**
  - the kit binds only the verdict report, as `v007_adoption_pin` (kit L509);
  - there is no r11, r12 or seal-tuple token in the kit or its launchers.
- **So** S0 needs §1–§4, its own §7 pins, its dry plan and its START. It does not need §5, §6, §8 or §9.
- This answers A263 W2 (L4553): S0 does not wait on the gating reviews.
- **Saving.** E 0; U 1–3 h. **Build: N.**

**L9. S4/S5 · (d) · Run the HEADLINE11 reuse deciding test early.**
- **Change.** Right after §8, before HEADLINE11 launches, compare the candidate config's probe spec shas (design map L199–202) against table D (sheet L186–198).
- If any sha differs, root rules at that point, instead of hitting reuse exit 5 at W1, which costs +2.25 d (A201 L2547).
- **Saving.** E ≈ 0; U up to 2.25 d × P(differ).
- **Build.** N, if `status` runs on a volume-free provisional config (UNTESTED).

**L10. S9, rerun branch only · (c) · Allow non-solo reruns after non-physics ends.**
- **Today.** P112 `enforce_solo` (L1347–1370) and A245 item 4 (L4197) register solo reruns.
- **Basis.** Solo protects no value:
  - A166 L1461: contention changes speed only.
  - A245 2(b): an identical reproduction is the physics evidence.
- **Saving.** U about 1–1.5 d per non-physics rerun; E 0.
- **Build: Y.** A P112 successor, plus a disclosed pre-result registration of the A244–A246 kind.

**S11 levers.**

**L11. S11 · (c)/(d) · CP-1 QoS successor (candidate 1).**
- **Saving.** On S11: E 10–20 h, U about 25 h. On S10: at most 1 h, through row 32, and only with a matching row-32 runner delta.
- **Scope.** See §5.

**L12. S11 · (b) · Pipeline each Phase-2 wave.**
- Codex3 reviews EPS per point as each point finishes, in a standing window, not once per round.
- Root uses one pre-reviewed command template per wave. There are 6 steps × 14 cycles, none measured (design map L116–123, L138).
- **Saving.** E 5–15 h.
- **Build.** N for the template; Y (small) for a script.

## 4. Verdicts on 0822's six candidates

**1. CP-1 between waves: PARTIAL.**
- **TESTED: the background requirement is deeper than the list runner.**
  - The list runner hard-codes `-b` (L60).
  - The pinned c3v004 `run_point` also refuses unless the process runs at background QoS (L466 → L231–233).
  - It writes `qos {darwin_bg, taskpolicy:'-b'}` into POINT_START (L486).
  - It caps `max_concurrent` at 8 (L736).
  - The list common loads c3v004 by sha and never changes a byte of it (common L4, L27).
  - So a one-flag list-runner successor refuses with BACKGROUND_QOS_REQUIRED.
- **"2.25 h at background" is measured.** Phase B ran 29 points at k = 8 from 20:20:04Z to 04:39:42Z, alongside step 2 (A199 L2512; A166 L1486).
- **"About 1.1 h at normal QoS" is UNTESTED.** Run sheet L203 is an estimate for GQ+EPS only. The one TESTED normal-QoS figure is GQ at 37.13 s (L200).
- **"Every march0+ wave pays it on the critical path" holds for S11 only:**
  - Phase 1 ends before march0 (A133 L467; A137 L600; design map L26, L137).
  - W1–W3 and the 24 conditional points are pre-certified (A257/A258).
  - The only CP-1 on S10's path is row 32 (S8).
- **Worth building:** for S11, after L1–L4. The scope is in §5.

**2. EPS review latency: VERIFIED.** It can be overlapped and pre-requested; it should not be removed.
- In Phase 1, every expected-path and branch point is already signed proactively (A257 L4434; A258 L4455). Only row 32 remains (L3).
- In Phase 2, review each point as it finishes (L12).

**3. Verdict-day sequence: VERIFIED, with additions.**
- **Confirmed:**
  - P1–P4 are adopted (A263 L4542–4547).
  - The night reviews are now byte checks (A268 L4625–4631).
  - S0 can launch before HEADLINE11's PRELAUNCH/binder chain (L8).
- **Additions:**
  - J0–J2 are missing (L2).
  - The QoS exception list is empty (§1).
  - Root's own steps stay serial for custody.
  - Root works on its last ~10 % of weekly credit until the Thu 18:00Z reset (A236 L3996). A credit stall would hold the chain until 18:00Z. At E, HEADLINE11's slack absorbs that.

**4. S10 replay passes per call: REFUTED (FORMAL).**
- **Why per-call replay is not possible:**
  - An incomplete snapshot is refused before the ceiling (RUNBOOK L72).
  - PASS_ONE needs the FULL build, which in turn needs the snapshot patch (L76–86).
  - PASS_K uses the same admitted plan (L92).
  - The final PASS_K must be byte-equal to the ledger head, after the seal and reading gates (L90, L96).
  - The replays compute NGC predictions, so they cannot run before the seal (A133 L471–473).
- **Duration: UNTESTED.** These are budget-zero replays of saved states, run in process. They have been tested on synthetic inputs only (L128). The deciding measurement is the first real PASS_ONE.
- **What can move earlier:** L5.

**5. Phase 2 during Phase 1: PARTIAL.**
- **Already overlapping:** the Phase-2 campaign continues past B_P1, during S8 and S9 (A133 L467–469).
- **Inherent:** step-5 NGC needs the end of the campaign.
- **Can move earlier:**
  - L11 and L12;
  - the committed Phase-2 rule set (RUNBOOK L110) and G16 3(b);
  - the S1-B successor (A160 N7, L1567), commissioned as soon as u_A reads AT_ANCHOR.

**6. The seal: PARTIAL.**
- Not critical at E: 1–2 d of slack.
- With L2, L1 and cw8 all in place, the S10 join is about u_A + 24–28 h (about Mon 26), which leaves about 1 d.
- When N_new = 0, S0's acceptance waits only on the seal.
- The concrete hazard is the write-freeze collision with the row-32 pin entry (L6).

## 5. Candidate-1 build scope: a Claude3 build with a Codex1 review, after L1–L4

**Files.** New files only, in `claude_artifacts/cp1_qos_successor_c3/`:

1. **`cp1_runner_c3q001.py`**, from c3v004 `3f5e5c18`:
   - Add `--qos {background,default}` to run, worker, rho-repeat and adapt-eps. If the flag is omitted, the mode is background and behaviour is identical.
   - `require_compute_environment(mode)` checks getpriority(PRIO_DARWIN_PROCESS) == 1 in background mode and == 0 in default mode (L231–233).
   - `_spawn` (L766) and `spawn_rho_repeat` (L419) prefix `taskpolicy -b` only in background mode, and pass `--qos` on.
   - POINT_START `qos` (L486) records {darwin_bg, mode, taskpolicy: '-b' or null}, truthfully. SCHEDULER_START records the mode.
   - **Optional, separate flag:** raise the bound from 8 to 16 (L736; design map L140–141).
   - Everything else stays AST-identical.
2. **`cp1_points_common_c3q001.py`**, from the adopted cx2v002 `65859327` (A269):
   - Only RUNNER (L28) changes.
   - ASSEMBLER stays c3v005 `7df1c481`.
3. **`cp1_points_runner_c3q001.py`**, from c2v001 `3c6a5ba3`:
   - L60 depends on the mode.
   - `--qos` passes through to workers.
4. **Optional:** the same delta for the row-32 KS3 runner `54595c2d`. It is worth at most 1 h on S10.

**Unchanged:**
- The assemblers. `verify` keeps background QoS for custody derivation, which takes minutes (cx2v002 L192–193).
- The producers, the ledger, the entry, and every bundle field.
- TESTED: no assembler reads `runner`, `RUNNER`, `POINT_START` or `list_runner`.

**Tests:**
- (a) With the mode omitted, behaviour is byte- and AST-identical, including the BACKGROUND_QOS_REQUIRED refusal.
- (b) A mismatch between mode and actual QoS refuses, in both directions.
- (c) A default-mode record is truthful.
- (d) The spawn argv matches the mode.
- (e) On a synthetic point, stage payloads are byte-identical across modes. Excluded fields: utc, pid, run_id, timing and qos.
- (f) A default-mode bundle passes `records`, `verify` and guard `verify_bundle`.
- (g) Restoring mutants are killed. They ignore the mode in spawn, ignore it in the check, or record '-b' in default mode.
- (h) A226 single read.
- (i) A243 scan for rename and remove calls.

**Decide before building.** This costs root one minute and reads only value-free fields. Compare the Phase-B GQ stage wall seconds, run at background QoS, with the 37.13 s measured at normal QoS (run sheet L200). Build only if the ratio is at least 1.3.

**Use rule:**
- Use default mode only between waves, and only when no S10-critical run would lose cores.
- Never use it while root attests `background_noncritical_lanes` at a direct-batch admission (guard014 L319).
- Hedge runs stay at `-b` (A258 L4448).

**Risks:**
- **The value claim is FORMAL only.** CP-1 already shows a 1.62e-08 difference in the cross-run anchor check, at tolerance 1e-3 (A257 L4429).
  - So the deciding test reruns one certified point, in a fresh out-root, once at the same QoS and once at the other.
  - The cost is about 2–4 point-hours.
- **Disclosure changes.** The list runner's disclosure that "every gate is c3v004's" (L3–9) no longer holds.
- **Review load** on Codex1.

**No-build alternative: not recommended.** Running `taskpolicy -B -p <worker>` after POINT_START is possible (`man taskpolicy`; launcher015 L45 does it to itself), and it changes no value. But POINT_START would then record `-b` while the stages ran at default QoS. That is a custody effect, so not without a root disclosure ruling.

## 6. FAIL: not recommended
- **Bulk preloading direct results into the cache.** It changes the probe misses and the wave numbering (A262 L4528).
- **Multi-threaded BLAS, or dropping the single-thread environment.** It changes the summation order, and the single-thread setting is the determinism guard (sheet L28–29; V006 L1563).
- **Per-call PASS_ONE/PASS_K before the snapshot or before the seal.** See candidate 4.
- **Resume for registered calls** (A242 L4126–4133).
- **Ending S9 sooner with a member subset or a forced incomplete disposition** (S9_MAKESPAN L30).
- **Migrating the volume, or starting W1 before the drive** (A256 L4395–4399).
- **Removing or shortening a review.** Pre-staging is the only allowed lever.
- **Not FAIL, but not recommended now: a speculative S1 at a guessed u_A, such as the seed.**
  - The S1 fill binds u_A from the snapshot (A150 L1017), so this would need a fill-and-import successor.
  - P(u_A = seed) is unknown.

## 7. Per-step inventory

Key: (a) serial dependency (I = inherent, N = not inherent); (b) latency; (c) throttle; (d) trade.

**S3**
- (a) receipt → manifests → gates → compare → (r11 ∥ r12): I, by custody.
- (b) the gating reviews, now minutes; root's credit (A236).
- (c) `-b`/`nice` on §3–§7: drop them (L7).
- (d) none.

**S4**
- (a) HEADLINE11 after the verdict: I. S0 waiting behind HEADLINE11: N (L8).
- (b) J0–J2 missing from the sheet (L2).
- (c) max_active 3, counting route A only, with a 60 s ramp. About inherent at 18 cores: 3 × 8 workers.
- (d) L9.

**S5**
- (a) the drive: I.
- (b) the policy review at mount (L4).
- (c) none.
- (d) L3 is ruled out.

**S6**
- (a) W1→W2→W3: N, now handled by L2. Each wave after that needs the previous wave's results: I.
- (b) per-wave acceptance, ledger work and the root cycle.
- (c) CP-1 background QoS (L231–233, L466); k ≤ 8 (L736); one start per poll (L727–728); the process budget of 17 (A262 L4530), which is about inherent.
- (d) the hedges, in flight.

**S7**
- (a) seal before any NGC read: I.
- (b) Claude4's render, then Claude3's delta review.
- (c) the write freeze (L6).
- (d) none.

**S8**
- (a) u_A → row 32 → S1: I. C3T before C4T: N (L1).
- (b) L3.
- (c) guard014's one-call rule and the lock.
- (d) none.

**S9**
- (a) u_A → members and F points: I. Also R, the S0 tail.
- (b) L5.
- (c) solo reruns (L10).
- (d) cw8, in flight.

**S10**
- (a) all terminal → snapshot → FULL → PASS_ONE → PASS_K → final → score: I, by registration.
- (b) L5.
- (c) none.
- (d) none.

**S11**
- (a) campaign end → step 5: I.
- (b) L12.
- (c) L11.
- (d) S1-B prepared ahead, for the AT_ANCHOR case.

## 8. Sources (sha256 prefixes, from bytes)

**Dispatches and posts**
- 0822 `30cb5211`
- 0826 `4c8460b2`
- STEPS `0398b1b6`
- 0262 `b27d5aa1`
- 0265 `93722720`

**V006.** Read by entry ranges, A133–A269. The file is append-only and grew during the audit. Its last sha was `7bacd5bd`, at 4653 lines.

**Verdict-day sheet**
- sheet `f2a5eec4`

**Campaign certification**
- design map `29071333`
- README_CAMPAIGN_CERT C2V001 `bc0ea884`
- README_CAMPAIGN_CERT C2V004 `638d6543`

**CP-1**
- list runner `3c6a5ba3`
- common c2v001 `302abdad`
- assembler c2v001 `951e7203`
- c3v004 runner `3f5e5c18`
- c3v004 common `53f10e6e`
- c3v004 assembler `cb5c61ee`
- cx2v002 common `65859327`
- cx2v002 assembler `1b701591`
- CP-1 run sheet `75481f2b`

**S1 and the launch path**
- S1 registration `67b4bd78`
- guard014 `6efdca01`
- launcher015 `cd987edd`
- binder `d3d9702e`

**S0 kit**
- kit `fdc0ee6c`
- serial launcher `621263a2`

**Phase 1 and S10**
- RUNBOOK c2v007 `12917ba9`
- P112 cx2v004 `8cec1b56`
- S9_MAKESPAN `82b906ba`
