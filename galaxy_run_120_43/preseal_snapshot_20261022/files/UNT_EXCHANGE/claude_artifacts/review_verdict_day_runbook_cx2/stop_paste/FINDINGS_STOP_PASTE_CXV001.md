# Codex2 internal review — STOP, PASTE, and per-call shell state

`date -u`: Wed Oct 21 16:10:51 UTC 2026

**Disposition: FAIL — one blocking finding, F-STOP-1.** This is an internal narrow review for the parent Codex2 lane, not a program ruling, launch authorization, or outbox dispatch. Source-byte mechanics are TESTED. Bash semantics and code-flow deductions are FORMAL. All runbook execution and production behavior are UNTESTED.

## F-STOP-1 — P0 omits fail-fast options, so dependent commands run after a refusal

**FORMAL, blocking.** The execution model is a fresh `/bin/bash FILE` containing P0 and one block (runbook lines 17–22). P0 (lines 116–130) and its sourced variable file V (lines 1–19) set no `errexit` or `pipefail` options. Therefore a normal fresh bash invocation is allowed to continue after a failed simple command, and a pipeline normally returns only its final command's status. The explicit options in later blocks cannot supply state to a separate call.

Concrete counterexample directly supported by the reviewed sources:

1. B9b executes the binder at runbook line 447, then unconditionally executes the caps checker at line 448. There is no intervening status check or short-circuit.
2. Binder source lines 51–54 explicitly preserve a partial prefix of three exclusive writes, in the order plan, admission, command. If opening the command output fails after successful plan and admission writes, the binder raises and exits nonzero. Such a refusal is expressly within the binder's documented partial-output behavior.
3. The following caps checker reads only DBP, bound plan, and bound admission (checker lines 2–10). It has no command-file argument or binder-completion check. The just-written valid plan and admission can satisfy every check, so it prints its success line and exits zero.
4. Thus B9b can return zero with the binder having refused and the command output missing. The runbook's line 453 STOP condition is not enforced inside the call. This is not a claim that an actual failure occurred; it is a source-derived reachable failure path.

A second concrete manifestation is B4 (runbook lines 233–236): a comparator refusal with no report is followed by a failing `shasum` piped into successful `cut`, then a successful `printf` of an empty digest. The call's final status can be zero. The prose requiring inspection of the full verdict remains a separate necessary human gate; it does not stop the shell continuation. B3a/B3b also continue to later producers after an earlier producer returns nonzero, and B6 continues from fill to build.

**Smallest correction:** create an immutable successor adding `set -euo pipefail` as the first P0 command, before `source`. Identify it as an approved derived guard in the successor's XREF/source policy. Alternatively add explicit fail-fast guards to every affected dependency and hash pipeline; a universal preamble is smaller. Retain the manual semantic STOP checks: `set -e` cannot establish a scientifically acceptable verdict or a blocker-free dry report. No reviewed file was edited and no suggested successor was created in this helper lane.

## Checks that passed within this narrow scope

- **TESTED:** XREF's bound runbook digest equals the actual runbook bytes. All 56 PASTE rows equal their actual source lines. The 54 scalar slots each have an immediately following `${NAME:?...}` presence guard. The two array slots have nonempty-length checks within their blocks (B10H lines 463–465; B10S lines 743–753). The latter runs under `set -euo pipefail`.
- **TESTED:** 26 executable bash blocks were inventoried. A lexical uppercase shell-variable-reference scan found zero unassigned references after accounting for P0, V, and preceding block assignments. This covers executable blocks, not the manual root-action prose; it is not a general Bash parser or a proof for arbitrary substitutions.
- **FORMAL:** B7H, B7X, B10H and every full PJ-bearing Branch S block include their own `set -euo pipefail`. Explicit equality and directory checks in these blocks therefore stop on false status in ordinary standalone execution. PASTE presence checks do not prove semantic validity of a nonempty value; the root selections, hash checks, downstream validators and prose review gates still apply.
- **FORMAL:** the map and wait prose preserve B4 before both branches, both Branch H gating PASSes before B8a, and FINAL specs before H11 per-spec dry plans before PRELAUNCH. Branch S's B7S1/B10S prose does not depend on B5R/B6R. The V006 write freeze is explicitly cross-branch from the start of B11.1 until the seed's confirmed launch record; it is an operator sequencing requirement, not an automatic interprocess lock in this runbook.
- **FORMAL:** the envelope source explicitly excludes V006 itself as a growing file (source lines 37–40, 705–720, 751–757). Consequently this review does not infer a longer whole-V006-byte freeze from the envelope after the runbook's named freeze ends. The already collected pinset must remain the END pinset, as the runbook requires.

## Limits and evidence

No runbook block, shell fragment, scientific command, monitor, generator, source module or fixture child was executed. Only source reads and a newly authored static text-inspection script ran. No run-tree paths were statted, listed or opened; no actual NGC data, forbidden run paths, postseal records, session logs or network were accessed. All inspected source files remain unchanged. The Python command used the required isolated no-bytecode interpreter, all six single-thread variables and `nice -n 10`; the environment printed the known `setpriority: Operation not permitted` warning.

The all-PASTE inventory tests presence, not correctness of arbitrary root values. No production, shell-failure injection, launch, registration, output-path availability or scientific execution claim is TESTED here.

### Cited files — SHA256 from bytes

- **binder**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_bind_c2v011.py`
  SHA256 `d3d9702eb8096d11b98461f1c62c67931b9ecf74957cee95fbc3a60f60deaea0`
- **caps_checker**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h11_wall_ceiling_c3/check_headline_caps_c3v001.py`
  SHA256 `4efb810bdfb03c4c0458fc75a3910dda27c1dd62f9b80b19a34ba0fddbedd9ba`
- **envelope**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py`
  SHA256 `9d531381615f7b68f2f33bfc19f0aa2bcfe97a4e6f5c0e93187ea8eb35ce8d9a`
- **invitation**: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0303_2026-10-21_Codex2-invited-to-narrow-check-verdict-day-runbook-D008-whichever-lane-free-first.md`
  SHA256 `a0a3c673a1fcd989c585a27d828cdb7e400eb7f81f384302b2b2a33684281e38`
- **runbook**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_runbook_c3/RUNBOOK_EXEC_C3V001.md`
  SHA256 `553a0e2c7b1f023c22f68877fc233cf1de5eae2faec70ad81f206d93e6efd170`
- **vars**: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/VERDICT_DAY_VARS_C2V001.sh`
  SHA256 `49607ea4a8660f296516e610718bb26db303ad19c6c517a9f409ba11be56eff5`
- **xref**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/verdict_day_runbook_c3/XREF_C3V001.json`
  SHA256 `aca0ada17bd513dbdbe64268e7901af931552c0fb67a4ba2d93542ef204f0643`
- **Static inspection script**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_verdict_day_runbook_cx2/stop_paste/inspect_stop_paste_cxv001.py`
  SHA256 `b696897d94822823bea2790e3ea5a9d53dd43910d73d147cd70503a4bf76814b`
- **Static inventory and mechanical evidence**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_verdict_day_runbook_cx2/stop_paste/STATIC_INVENTORY_CXV001.json`
  SHA256 `09f1fcb1a4a6ca797381edff6eea359d57770c5081d0a7ae3b354a81533eeeed`
