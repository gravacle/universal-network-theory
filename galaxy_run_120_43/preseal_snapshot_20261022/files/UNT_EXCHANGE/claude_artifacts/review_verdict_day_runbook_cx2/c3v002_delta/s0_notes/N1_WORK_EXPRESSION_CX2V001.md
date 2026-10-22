# N1 static source clarification

date -u observation: Wed Oct 21 16:16:27 UTC 2026.

FORMAL, source text only. In `launch_twin_root_c2v003a.sh` lines 78–83, `STAMP=$(date -u +%Y%m%dT%H%M%SZ)` supplies the UTC component. Line 79 selects `WROOT="$LR/work"` in launch mode and `WROOT="$LR/dry"` otherwise. The exact line 81 is:

> `WORK="$WROOT/S0_SEED_CW8_TWIN_A${PLAN_ATTEMPT}_${STAMP}_$$"`

Line 82 creates that directory. Line 83 names `$WORK/plan.json`; later source names `$WORK/fill_check.json` and `$WORK/dry_verdict.json`. The source-only interpretation for the runbook's DRY attempt 1 is the unique leaf `dry/S0_SEED_CW8_TWIN_A1_<UTC>_<shell-pid>` under the selected launch root. The successful DRY output does not print `WORK`, so root must identify and record the exact invocation-specific leaf before collecting these metadata pins. The author can document that obligation without adding a command. No path was dereferenced, no directory state checked, and no quoted source executed here.

Source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/launch_twin_root_c2v003a.sh`, SHA256 `f199544db9fe40a4fedbe7647d52ad4bd8dacb13a9aa9c1b9ab4ad0198e7769f`.

This supplements the nonblocking N1 residual in `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_verdict_day_runbook_cx2/c3v002_delta/s0_notes/REVIEW_S0_NOTES_C3V002_CX2V001.md`, SHA256 `21efc28a9ee67581b95236311fe28ebfc600f782ab515a42328184168157bad3`. Actual output identification and execution remain UNTESTED.
