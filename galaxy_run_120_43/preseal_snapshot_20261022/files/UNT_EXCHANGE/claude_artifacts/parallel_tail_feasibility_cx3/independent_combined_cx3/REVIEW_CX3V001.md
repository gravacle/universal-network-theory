# Independent combined benchmark review

date -u: Sun Oct 18 20:05:49 UTC 2026

Verdict: **PASS_WITH_REPORTING_LIMITS** for `benchmark_tail_cx3v007.py` at `fa1ee0531243773a7dc4bfaa35d9ac5cdf1f127ce7929a82a45afaf1a2e46629`. No blocking source defect was observed in the assigned timing/comparison/thread-cap scope. No source change is requested by this review.

TESTED: 58/58 source-AST and observed-record consistency/accounting checks. The review did not import the scientific modules or rerun a numerical benchmark. Every prior v004 function other than `main` remains AST-identical, including input preparation and CPU/wall accounting. The new child function matches the separately prepared threading v003 function. The process prototype remains pinned and unchanged.

The measured serial interval includes fresh roster/provider creation and native `U.build`. The process interval additionally includes the prototype's star preparation, duplicate grid construction, and pool startup/teardown. Both exclude the later jet comparisons. The fresh thread-child interval likewise includes roster/provider creation and native build, while excluding interpreter startup, source import/input preparation, jet evaluation and IPC. Whole-study elapsed time is reported separately. The CPU formula adds parent self CPU and reaped child CPU; the compact record's arithmetic and speedup/CPU ratios recompute consistently. These intervals must not be presented as equal end-to-end startup costs.

The process comparator tests key sets, dtype, shape and direct bytes for every state table and every field returned by order-1/order-2 jets. The thread comparator uses the same-invocation serial state, checks the union of all table/jet keys, dtype, shape and direct bytes, then independently checks record and state-digest equality. Hashes are evidence alongside direct byte checks, not substitutes for them.

A fresh `spawn` child receives the private measurement variable set to six before the module's NumPy import. Only VECLIB changes to six; the other BLAS controls remain one. The parent restores the private variable in a `finally` block around child start, leaves its own VECLIB cap at one, and rechecks the prototype's BLAS1 requirement before/after the child. A cap is configuration evidence, not measured active thread concurrency.

Observed validation, not independently rerun: the compact synthetic K32 invocation contains an N2 process case and one configured-VECLIB6 child. All 18 table/jet arrays report direct equality, their serial baseline hashes match across process/thread records, record/digest equality passes, and the 218-probe shapes agree. The child reports Accelerate and the intended cap6/other-caps1 environment. The summary reports TESTED_PASS and `production_admissible=false`. The N2 process's global four-PID union comes from two sequential component/doubling passes, each with two task PIDs; it does not show four simultaneous workers. There is no claim about simultaneous occupancy from these PIDs.

The serial, N2 and configured-VECLIB6 component wall measurements in this one synthetic invocation are approximately 0.474, 0.515 and 0.473 seconds. This small single observation supports neither a general threading speedup nor universal determinism. Source comparison and compact-record review do not independently establish numerical equality on saved K128/K256 states or N6/N12 under v007.

Failure handling and limits:

- Process comparison failure writes TESTED_FAIL and raises. Child exception/nonzero exit raises in the parent. A thread byte mismatch is saved as TESTED_FAIL and propagates into SUMMARY TESTED_FAIL, but need not make the command exit nonzero. Report aggregation must inspect every process/thread comparison and summary status; shell exit zero alone is insufficient.
- Child and parent RSS checks include post-jet, post-receive and post-comparison points. They are observed post-allocation limits, not hard address-space guarantees. Peaks are process lifetime maxima. The observed synthetic peaks are below 8 GiB; the review process itself peaked at 27459584 bytes.
- The runner does not install a timeout for an indefinitely unresponsive child. Pipe/child exceptions prevent a successful summary; bounded wall termination is not established by this source review.
- Actual simultaneous process/thread counts, universal determinism, production admission, persistent-cache behavior and end-to-end saved-state performance remain UNTESTED here. No scientific solve, worker main, target/protected-run read, network call or existing-file modification was performed by this review. Guard denials were zero.

Byte-pinned source and observed evidence:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/benchmark_tail_cx3v007.py` — SHA256 `fa1ee0531243773a7dc4bfaa35d9ac5cdf1f127ce7929a82a45afaf1a2e46629`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/benchmark_tail_cx3v004.py` — SHA256 `56e08972a4edd329975e7adca96ae8924aa548354cb7db9d3b63af3f03a2e645`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/parallel_stars_prototype_cx3v002.py` — SHA256 `f1daa12e71418cd565188b1760345b7c0b8c78c5705589e0918e5edf6d20e8c7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/threading_tail_cx3v003.py` — SHA256 `78d54f9bfd6b60b2b9f8405ecdb0e0d3372263a4a2de0ebf06d6eb65ee7134cc`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_COMBINED_V001/INPUTS_V001.json` — SHA256 `7361063958a23d704de3263575ce70a634da52265710e31d35e3f6372f15a98e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_COMBINED_V001/N02_V001.json` — SHA256 `cdbdd845149b998b8772dccaa7ae5f266d3509dc0b8d6b553c31eec3cc40b856`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_COMBINED_V001/THREADS6_REPEAT0_V001.json` — SHA256 `aa2ca5279b1769da4331310b5144962eaad8057f746467c3160d2247f200b1ce`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K032_COMBINED_V001/SUMMARY_V001.json` — SHA256 `dbebb4b7552c7f54befd5403f0e0b53dc783d0381776e5d84d4b332f4ea6eee2`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_combined_cx3/RESULTS_CX3V001.json` — SHA256 `7939574a39ff27c88f7b360ce188869c3e9b2d70783f521d559bc0f5f62c7a1c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_combined_cx3/review_combined_cx3v001.py` — SHA256 `c7294502d1299431aadce14ee1fc414f11f8e7ce9aa5ba14f25c820d4cf540c4`
