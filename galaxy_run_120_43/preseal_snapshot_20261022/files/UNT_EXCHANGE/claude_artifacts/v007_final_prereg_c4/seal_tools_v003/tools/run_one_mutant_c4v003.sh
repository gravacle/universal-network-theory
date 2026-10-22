#!/bin/sh
# Claude4 seal tools v003 (BUILD helper): run the suite of ONE mutant folder (argument: its id under mutants/final/) under the pinned fence
# runner; the log goes to mutants/final/<id>/run.log (created new; noclobber). Single-thread BLAS, low priority.
set -C
M="/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v003/mutants/final/$1"
cd "$M/tests" || exit 3
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 taskpolicy -b \
  /Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v003/tools/run_fenced_c4st2.py test_seal_tools_c4v003.py > ../run.log 2>&1
echo "$1 rc=$?"
