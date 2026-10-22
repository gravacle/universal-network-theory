# A124 disk guard and A122 PRELAUNCH successor

Candidate supported packet successors: guard008, launcher009, binder007; PRELAUNCH002. Earlier objects remain unchanged. Claude3 distinct review is pending.

TESTED: disk helper8 behavioral controls plus2 source-wiring assertions, all PASS; PRELAUNCH0028 inert controls with guard008 plan pins, all PASS. Native_preflight and fence source segments in guard008 are byte-identical to guard007. UNTESTED: production stack, live External1 behavior, full launcher process lifecycle with disk changes, and all scientific execution. Prior broader packet tests have not been claimed as carried forward.

A124 requires External1/Research/UNT_STEP4_RUNS/V007_STEP4_DIRECT_V001; root creates it at T0. All call outputs, receipts, monitor logs and launcher log must be distinct descendants. Symlinks, absent mount and differing filesystem device ids refuse. statvfs available blocks supply df-equivalent bytes without spawning a process. Batch admission requires sum of approved call output caps plus20GiB (identical to calls times cap for equal caps). Launcher repeats the one-call bound beside the memory gate and immediately before start. Unreadable/low space refuses and invokes existing drain behavior; it cannot start a monitor. Repeated active-worker validation skips the full-batch free-space check, avoiding counting already-allocated output twice; per-start checks remain.

PRELAUNCH002 still bootstraps guard007 and calls its native_preflight under its fence. It accepts byte-pinned guard007 or guard008 plans and verifies their source membership. The launcher/binder successors bootstrap guard008 by hash. Both guards therefore belong in the final source inventory. PRELAUNCH manifests do not grant root authority.

G7-SCOPE-1 remains incomplete: selected adoption-policy and certificate tooling, sensitivity dynamic dependencies, DIII reference closure and final root C1 source review remain pending. The prior draft inventory is not admissible. No production output root was created or read by these tests.

Reproduction: copy this directory to a fresh scratch directory, run test_prelaunch_v002.py and test_disk_v001.py with python -I -B. They create exclusive fixture/result paths. build_disk_v001.py is provenance only; its output directory already exists in this publication. Do not re-run it here.
