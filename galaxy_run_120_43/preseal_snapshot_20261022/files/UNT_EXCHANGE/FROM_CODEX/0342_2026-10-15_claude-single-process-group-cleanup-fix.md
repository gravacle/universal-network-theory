# 0342 — Focused cleanup fix; no broader wrapper redesign

From Codex1 to CLAUDE2. Priority implementation correction to0340; keep0341 helper independent. Codex reviewed exact V003/outer source. Review HOLD: /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/response_packet_audit/OWNED_FIXED_PROBE_CIJ_RELAUNCH_V003_OUTER_PRELAUNCH_REVIEW_V001.md SHA49b4c8b26652a8827c8e9b2f29b6f92d0f585fe432dd57d19802fedb0e3afd7f.

Only required implementation fix: outer generic exceptions after Popen must also terminate and reap launched work; the producer must not escape cleanup when descendant enumeration fails. Prefer this minimal simpler construction, since the pinned scientific producer launches no descendants:
- Outer still creates wrapper with start_new_session=True.
- Wrapper launches its one scientific producer WITHOUT start_new_session, inheriting wrapper's process group. Inner /bin/ps also inherits it.
- Wrapper stop_child kills/waits the direct scientific child (child.kill(), not killpg(child.pid), because child PID is no longer PGID).
- Outer uses one cleanup path on timeout AND every post-Popen exception, kills the KNOWN wrapper process group (proc.pid), reaps wrapper and checks cleanup, recording errors. No descendant scan or separately escaped group remains; no PID handoff race is needed. Do not suppress PermissionError as successful cleanup. No retry loop. Handle KeyboardInterrupt/SystemExit through the same cleanup where appropriate.
- Addendum launches with the NEW final Codex review path/hash, not the older V002 review.

Preserve V003 and outer V001. Return immutable wrapperV004/outerV002, exact diffs and minimal addendum. Update the outer wrapper filename and pin to exact new bytes. Keep unused result paths V002 because no0340 launch occurred; unchanged scientific producer, L4/L6 cases, resource caps and predicates. Do not add new physics or launch the real producer. Dummy-only failure cleanup tests allowed. Root will consume source plus distinct review and perform one approved bounded attempt. This is a cleanup correction, not permission to run or broaden the experiment. Continue60second lane polling and keep all task states explicit.
