#!/bin/bash
# Dry-run runner, pass A (Claude3 0626; final dry run on ROOT_SEAL_STEPS_c3v026.sh b43cc38b). Root-supplied inputs are DRY-RUN
# STAND-INS (labelled); nothing here is a root ruling.
export UNT_SEAL_DISPOSITIONS_PATH="/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/dry_run_20261019T060249Z/passA/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json"
export UNT_SEAL_DISPOSITIONS_SHA256=6a3fa5353e575fbfe617aa497abd4752e8a2c8676d19f6c4c16a69dfeac0c9fe      # FIXTURE (v003 object on r6: entries [], no later or changed entry; labelled)
export UNT_SEAL_COMPARE_REVIEWED_PATH="/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py"     # r14, the compare of record (A114/A116)
export UNT_SEAL_COMPARE_REVIEWED_SHA256=f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7
export UNT_SEAL_COMPARE_SELECTION_PATH="/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14/SELECTED_R14_CX1V002.json"
export UNT_SEAL_COMPARE_SELECTION_SHA256=6b650ececefee673ec3e04849574f9a4b75b977288afd3c9949a4b8d2d3cd49a
export UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH="/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_b7_inputs_c4/KEY_EQUIVALENCE_MAP_V007.json"
export UNT_SEAL_KEY_EQUIVALENCE_MAP_SHA256=72a21888eda617638df38ddd64a0e7981bfb6842a9f7f17b8c1a7d4b93e50ec4
export UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_PATH="/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cascade_map_r5_addendum_cx3/CASCADE_MAP_R5_ADDENDUM_CX3V001.json"
export UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_SHA256=86c897304ec5a0971c3ad1552a60cfad90fc3ac809d68fdacee2be1b942caf9e
export UNT_SEAL_C5H_RUN_DIR="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext/KMAX_A2F10_C5H_RUN_V001"  # STRING ONLY (step 9 stubbed)
export UNT_SEAL_MIN_FREE_GIB=300                                                                             # STAND-IN floor
export UNT_SEAL_ROOT_ACK=RI-28,RI-29,RI-30,RI-31,RI-32,RI-33,RI-34,RI-35,RI-36,RI-37,GAP-12                  # STAND-IN ack (dry run only)
exec /bin/bash "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/dry_run_20261019T060249Z/passA/ROOT_SEAL_STEPS_DRYRUN_A.sh"
