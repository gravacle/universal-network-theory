# Existing S0 and not-yet-started Phase-1 calls — CX3V001

date -u: Wed Oct 21 12:46:31 UTC 2026

FORMAL modeled answer: yes, starting a genuinely new Phase-1 member/F at cw8 after the seed-pair proof can shorten the overall path, if the call's PLAN/FDPLAN/AT0A/certificates are already available, the root license is valid, enough cores remain, and S0 does not hide the gain. Existing S0 serials are never restarted, renamed or rebound. If all required calls are reused from S0, there is no new call to accelerate.

TESTED arithmetic only: the cited script evaluates 12 cases using the exact candidate scheduling function. For an illustrative pair time t=6 h, assume the existing S0 critical barrier began at t=0 with the same uniform modeled serial cost: 31.90 h expectation / 84.77 h upper. Its remaining barrier at pair time is then 25.90 / 78.77 h. Eight-core A plus one-core tail costs are 5.84+15.74 h expectation and 17.52+34.33 h upper. These are planning estimates inherited from 0818, not measured full-call times.

| New calls | Free cores | Modeled gain E / U at pair time | Choice |
|---|---:|---:|---|
| 1 | 12–18 | 6.00 / 6.00 h | cw8 |
| 2 | 16–18 | 6.00 / 6.00 h | cw8 |
| 2 | 12–15 | 4.48 / 6.00 h | cw8 |
| 3 | 16–18 | 4.48 / 6.00 h | cw8 |
| 3 | 12–15 | negative / negative | serial |

The apparent per-call saving is not the critical-path saving. At 16–18 free cores a third eight-core A phase waits for the first wave, so its branch is 27.42 / 69.37 h from pair time. S0 masks much of that upper-case gain. If the actual remaining S0 barrier is at least the new serial branch duration, the predicted improvement is zero and the selector uses serial. A fresh root forecast supplies the actual remaining-barrier estimates instead of the illustrative six-hour assumption.

A separate prerequisite can dominate: Phase-1 selection, PLAN, FDPLAN or certificates may not yet be available six hours after seed launch. In that case no new Phase-1 call is admissible at pair time, regardless of CPU capacity. Early dry preparation remains possible without fixing a worker role. When a new call becomes admissible, compute its current cohort and barrier then. Existing preparation with process/commit evidence and existing attempt/registry history remain fixed.

This model supports only 1–3 newly admitted calls with 12–18 free cores. With two existing eight-core DDO jobs, for example, the free-core count is outside its support and it falls back to serial rather than inventing a speedup. Waiting for a future resource window may be better than immediate serial, but that is a root scheduling choice outside the present selector; include the waiting delay and S0 barrier when assessing it. At most 10.32 h expectation-side delay for one/two unconstrained new calls, or 4.48 h for three at 16–18 free cores, can preserve a gain against immediate new serial when no additional barrier masks it. These are strict thresholds, not launch timers.

No S0 process, real state, wall-clock progress or output was inspected for this analysis. Actual timings and production benefit remain UNTESTED.

Evidence (SHA256 from bytes):
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/S0_OPTION_EVIDENCE_CX3V001.json` — `19cb79af9f5ec71ffe23dd2ab94403f3f1347cd1d868b379991478a6d4b8fc26`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/s0_option_analysis_cx3v001.py` — `36c9a491a20063f9ad32a48c752a9d45f00d4149ce0093badcafb6dfbf90cec6`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/phase1_ngc_launch_cx3cw8v001.py` — `04dfc429e335458494fa377f2f46e8d54adbe7e0f0b9a4c3b2121c6b0964f0c2`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/accel_w1disk_cw8_cx3/S9_MAKESPAN_EVIDENCE_CX3V002.json` — `51324dc89b1b2aca08e5952800583d72d95ec9861f8225df574664f4abe44b24`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/accel_w1disk_cw8_cx3/S9_MAKESPAN_CX3V002.md` — `82b906baa500c6b56b3cda077eac79203c09f7ad7d6033c9e7579d4c2a7360d0`.
