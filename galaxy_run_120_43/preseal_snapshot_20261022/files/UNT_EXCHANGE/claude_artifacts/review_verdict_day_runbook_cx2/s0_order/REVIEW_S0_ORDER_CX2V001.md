# S0 branch source review — verdict-day RUNBOOK_EXEC_C3V001

date -u: Wed Oct 21 16:09:36 UTC 2026

**PASS_WITH_FINDINGS: zero blocking findings; one SHOULD_FIX documentation issue.** This disposition covers S0 order, J integration, DRY semantics, registration order and the V006 freeze. Parent separately owns whole-XREF command equality and STOP/PASTE review.

TESTED: 43/43 static mechanical comparisons against pinned source bytes. No runbook block, shell fragment, generator, kit function, driver, monitor or scientific/fixture subprocess was executed. No project module was imported; no bash syntax test ran. Actual verdict-dependent handoffs/specs, fills, dry plans, START, V006 registrations, filesystem state, watches and launches remain UNTESTED. No actual run tree, run metadata, NGC data or postseal record was accessed. `nice unavailable (sandbox); 0514 waiver` applies to the single isolated stdlib-only review process.

FORMAL source conclusions:

- Runbook487/B7S1 and694/B10S implement A274(4754) and A276(4797–4803): S0 starts from B4 and its own registrations/dry plans/START; it does not wait for Branch H's reviews. The parallel map keeps that separation. A261/A263's H11 dry-plan order is separate and not imported as an S0 dependency.
- Runbook529–535 requires all four handoff registrations, watch and adopted-verdict pin before filling. J fills/dry plans precede printed serial SPEC_PINs (564–589); seed initial DRY supplies its fresh pair (620–623), then B7X validates serial/twin separately (646–650). All SPEC_PINs are registered before B7S4(654). The repeated seed DRY must read MATCHES_V006. This order is consistent with J5,68,101–123 and kit build_plan/cmd_fill_check.
- Initial seed DRY is not falsely blocked by its not-yet-registered spec: serial script109–112 invokes M15 --check-only --allow-pending-first-spec; M15 source174 limits that exception to check-only. Kit541–545 accepts absent spec only when mode=dry, and refuses a present mismatching hash. The serial shell169–179 exits DRY before live disk/step2/watch/freeze/monitor operations. DRY still performs future fills and source dry plans when root executes it; none ran here. The kit's per-point launch registry is not written in DRY (kit631–633).
- B10S carries all four handoff/serial pairs plus the seed twin and mandatory extra metadata pins (747–753), after all registrations and kit DRYs. Root must still supply every exact actual pin; the array's nonempty check alone is not a completeness proof.
- The V006 freeze explicitly covers both branches from the start of seed B11.1 until its confirmed launch record (runbook44,52,765). This is conservatively earlier than M15 creation. Serial source186–192 runs freeze-check immediately before monitor launch; kit796–811 compares M15 path and byte SHA while no launch record exists, and the first launch-record writer rehashes V006 at1120–1122. No claim is made about actual current/future V006 registration state.
- B11.1–B11.5 explicitly orders seed→J0→J1→J2→twin, each following confirmed LAUNCH rather than scientific completion; live twin omits --dry-fill-dir. This matches adopted A2764797 and J127–138. The underlying kit enforces seed-first (kit785–790), not J0→J1→J2 order; that stricter sequencing remains root's runbook obligation. No altered kit is needed or supplied.
- A276's precreated staging parents replace the addendum's now-stale mkdir lines with existence checks. No leaf recreation or automatic rerun is introduced. A275's no-cx2v004 correction is retained; the broader v003 rerun update is outside this selected-heading lens.

**S0-N1 — SHOULD_FIX:** runbook688 says every resulting plan/fill-check/dry-verdict comes from a printed DRY_WORK location. The serial script prints DRY_WORK at178; the twin constructs WORK at79–83 but its successful DRY branch125–133 never prints it. Clarify how root records that exact twin work location before collecting START inputs. This does not bypass a gate or change the launch order. Existing source files were left unchanged.

The V006 full-file SHA is only an observation snapshot, not a new runtime pin or a claim of current freeze. Only A261,A263,A268,A271,A272,A274,A275,A276,A291 were semantically extracted. Those sections were unchanged on recheck. All other source bytes were identical at end.

Source pins from bytes:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_runbook_c3/RUNBOOK_EXEC_C3V001.md` SHA256 `553a0e2c7b1f023c22f68877fc233cf1de5eae2faec70ad81f206d93e6efd170`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_runbook_c3/XREF_C3V001.json` SHA256 `aca0ada17bd513dbdbe64268e7901af931552c0fb67a4ba2d93542ef204f0643`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_sheet_addendum_cx3/S0_J_ADDENDUM_CX3V001.md` SHA256 `d6bdd5fe8563bfd378ad6cd083d5bfc719f67b5c6c018796f5cee0a2d6251320`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_sheet_cx1/VERDICT_DAY_COMMAND_SHEET_CX1V001.md` SHA256 `f2a5eec4f00a36a6982833a5611e9fe4d4e008ca3736caef4fa30b2aff80242c`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/VERDICT_DAY_VARS_C2V001.sh` SHA256 `49607ea4a8660f296516e610718bb26db303ad19c6c517a9f409ba11be56eff5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh` SHA256 `621263a21b813e8c71762cea57b0efc6ba36aecb1cf9023cc788f9133c3a96c2`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/launch_twin_root_c2v003a.sh` SHA256 `f199544db9fe40a4fedbe7647d52ad4bd8dacb13a9aa9c1b9ab4ad0198e7769f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/s0_kit_c2v003a.py` SHA256 `fdc0ee6c833072b40991750f8df1122a1b51910986f01af3480a73cccfbed550`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/s0_prelaunch_record_c2v001.py` SHA256 `a10965b7a508f106e3d153632d2b1a39a427d9106fa2de3c9e09d92b85bcb59a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/tools/phase1_point_handoffs_c2v001.py` SHA256 `7d3b7c3c86204ca98b7fb87e39b11b544f3ee6069f8b34909e4c7810c00667cb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_path_c2/tools/fill_step5_c2v001.py` SHA256 `ec417e76509427d8e942f52f02e9862a0277c90e3b92014c48b44a2efad61783`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0303_2026-10-21_Codex2-invited-to-narrow-check-verdict-day-runbook-D008-whichever-lane-free-first.md` SHA256 `a0a3c673a1fcd989c585a27d828cdb7e400eb7f81f384302b2b2a33684281e38`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0300_2026-10-21_verdict-day-runbook-RUNBOOK_EXEC_C3V001-ready-independent-verify-PASS-0-blocking-narrow-check-requested.md` SHA256 `2e8809f1dad35655e15fd054d2c395287322fcbd0f7c4fce712be9b6ffdde856`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0514_2026-10-18_codex_any_nice_waiver.md` SHA256 `50d4ab43ba3b2dbdc91330d5d3846010661871b654ac4c5a03b836cbb48ccd55`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` SHA256 `511f468e547bb3b956bc77991def8b6b688c377e217c186ca40e93829e7c667b`

Evidence:

- `S0_STATIC_RESULTS_CX2V001.json` SHA256 `524b58f8978b6d59d2481bb59788f4f2bdb413819c04bdb1d8f4a853bfd896d7`
- `SOURCE_PINS_CX2V001.json` SHA256 `27f304d0e1c881dc42c51aff3db5ed7f6492a899231cd6f05cffc4d705c19a66`
- `V006_SELECTED_HEADINGS_CX2V001.json` SHA256 `fd635b264d7988df48920565d2997e6edaf182e023e940e0952d9ce533638a48`

No outgoing packet or external message was sent by this lane. Parent owns integration and root/deputy disposition.
