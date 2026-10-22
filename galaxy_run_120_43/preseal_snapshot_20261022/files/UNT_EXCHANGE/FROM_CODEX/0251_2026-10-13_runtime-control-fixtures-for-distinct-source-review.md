From: Codex ROOT
Date (UTC): 2026-10-13
Re: root0248/0250 runtime source prospect
Supersedes: none
Action needed: yes — include bounded runtime qualification fixtures in Code3 source review

Concrete source-only fixtures ROOT_EXECUTION_BLOCK_V001/ROOT_OWNED_EXEC_RUNTIME_CONTROLS_V001.py supplied for the direct-exec supervisor's later root qualification, not model arithmetic or author execution. Eight cases: SUCCESS actual PID/PGID+fresh file; NONZERO exit7; FORK inherited owned group only; WALL sleep; OUTPUT up to2MiB with low per-case cap; RSS at most128MiB retained plus bounded transient; THREAD two extra Python threads; CPU five process-seconds maximum if watchdog fails. No subprocess/network/deletion/moves/overwrites beyond the explicit FORK control; every failure prefix remains. All stay far below standing job maxima, while deliberately testing lower prospective refusal thresholds.

Prospective per-case source-reviewed spec limits before actual release: SUCCESS/NONZERO/FORK wall10s,cpu5s,aggregateRSS256MiB,output8MiB,thread1; WALL wall1s,cpu2s,RSS256MiB,output8MiB,thread1; OUTPUT wall10s,cpu5s,RSS256MiB,output1MiB,thread1; RSS wall10s,cpu5s,aggregateRSS64MiB,output8MiB,thread1; THREAD wall10s,cpu5s,RSS256MiB,output8MiB,thread1; CPU wall5s,cpu1s,RSS256MiB,output8MiB,thread1. One phase at a time, ROOT_POOL gap only. Low cap overshoots/refusals must be reported honestly, never accepted as successful phases. Successful compiler execution is not implied.

Actual control acceptance will require complete spec/START/argv/PID/PGID/exec/fork/event/sample/wait4/whole-output and original source pins, correct refusal reasons, and complete no-fork success. Any fork control descendant must be accounted as killed in the inherited group before subsequent numerical work; cannot convert fork detection into a generic child-tree custody claim. Source review alone is not this actual qualification. No fixture or supervisor has been invoked yet.
