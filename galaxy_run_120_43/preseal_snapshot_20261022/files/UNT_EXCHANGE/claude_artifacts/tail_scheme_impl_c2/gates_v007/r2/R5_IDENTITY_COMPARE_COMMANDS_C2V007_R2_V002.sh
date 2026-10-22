#!/bin/zsh
# r5 identity comparisons with comparator c2v007 (root V005 A74; A73 N6; A67 N1; A59 tokens, re-derived and checked by the comparator).
# NOT RUN by the build lane: the *_R5_RUN_V001 runs were still running when it was written.
# N6: (1) every receipt is checked first, strictly (status FINISHED, driver_status COMPLETED, exit_code 0, stop_reason null, retries 0,
#     driver pin = r5, result sha from the result.json bytes); no comparison starts unless all three pass.
#     (2) each comparison's exit code is collected from its own PID; (3) each report's verdict is read and checked (schema, gate, driver,
#     PASS_BITWISE_EQUAL, failing == [], comparator sha); (4) the records are written only after all three verdicts pass.
# Any failure exits 1 and says which item failed.  Read-only on the runs; writes only out/IDENTITY_C2V007_R5_V001 and records/R5_V001.
set -u
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
G7=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2
REF="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs"
EXT="/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext"
O=$G7/out/IDENTITY_C2V007_R5_V001
R5=b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6
CMP_SHA=052da0fe378b7927f35be28f9eda6f03313aef32bae7d5c9a301d276de21b12e
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
pin() { [ "$(shasum -a 256 "$1" | cut -d' ' -f1)" = "$2" ] || { echo "PIN MISMATCH: $1"; exit 1; } }
pin $G7/run_identity_compare_c2v007.py $CMP_SHA
pin $G7/tokens/TOKENS_Z2_R5_C2V007.json 0773782b6ce323a6e5bec3241791e6daf9188050f7296483ccaed6d98b9dcbb0
pin $G7/tokens/TOKENS_Z2_OFF_RO1_R5_C2V007.json 29eab731d0aa2f524c3745b6664d27c8b2795a73cb4477ede0453b85d5333d93
pin $G7/tokens/TOKENS_B0P_RERUN_R5_C2V007.json bbe2eb498e3bb087b305c3865ba1e926628d12a86699987e778189c58a4554f3
pin $G7/tools/r5_gate_check_c2v007.py 5dcd51422409f3354b480e67bd59c28f1b3412b756ea3228d834d133a673d745
pin $G7/tools/write_identity_records_c2v007_r2.py 67bb3d098e8a98e10ee542310fbcae026088bb666657244c835dbe36f881d2da
# N6 (1): the receipts (FINISHED etc.) before anything else
$PY -I -B $G7/tools/r5_gate_check_c2v007.py receipts --ext "$EXT" --driver-sha $R5 \
  UVT_Z2_A2F10_R5_RUN_V001 UVT_Z2_OFF_RO1_A2F10_R5_RUN_V001 UVT_B0P_RERUN_ADMIT_PREFIX_R5_RUN_V001 \
  || { echo 'RECEIPT CHECK FAILED: no comparison was started'; exit 1; }
mkdir -p "$(dirname "$O")" || { echo "CANNOT CREATE OUTPUT PARENT: $O (see mkdir error above)" >&2; exit 1; }
mkdir "$O" || { echo "CANNOT EXCLUSIVELY CREATE OUTPUT DIRECTORY: $O (see mkdir error above)" >&2; exit 1; }
$PY -I -B $G7/run_identity_compare_c2v007.py --gate Z2 --driver r5 \
  --reference "$REF/DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001" --new "$EXT/UVT_Z2_A2F10_R5_RUN_V001" \
  --tokens $G7/tokens/TOKENS_Z2_R5_C2V007.json --out $O/Z2.json > $O/z2.log 2>&1 &
P1=$!
$PY -I -B $G7/run_identity_compare_c2v007.py --gate Z2_OFF_RO1 --driver r5 \
  --reference "$REF/DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001" --new "$EXT/UVT_Z2_OFF_RO1_A2F10_R5_RUN_V001" \
  --tokens $G7/tokens/TOKENS_Z2_OFF_RO1_R5_C2V007.json --out $O/Z2_OFF_RO1.json > $O/z2offro1.log 2>&1 &
P2=$!
$PY -I -B $G7/run_identity_compare_c2v007.py --gate B0P_RERUN --driver r5 \
  --reference "$REF/DDO154_ROUTE_B_C2V009_DECIDING_ADMIT_PREFIX_RUN_V001" --new "$EXT/UVT_B0P_RERUN_ADMIT_PREFIX_R5_RUN_V001" \
  --tokens $G7/tokens/TOKENS_B0P_RERUN_R5_C2V007.json --out $O/B0P_RERUN.json > $O/b0p.log 2>&1 &
P3=$!
wait $P1; C1=$?
wait $P2; C2=$?
wait $P3; C3=$?
echo "comparator exit codes: Z2 $C1, Z2_OFF_RO1 $C2, B0P_RERUN $C3"
# N6 (2)-(3): each exit code and each verdict
$PY -I -B $G7/tools/r5_gate_check_c2v007.py verdicts --comparator-sha $CMP_SHA --driver r5 \
  Z2=$O/Z2.json=$C1 Z2_OFF_RO1=$O/Z2_OFF_RO1.json=$C2 B0P_RERUN=$O/B0P_RERUN.json=$C3 \
  || { echo 'VERDICT CHECK FAILED: no record was written'; exit 1; }
# N6 (4): the seal records (driver r5, A67 N1), only after all three verdicts pass
$PY -I -B $G7/tools/write_identity_records_c2v007_r2.py --driver r5 --reports $O --outdir $G7/records/R5_V001 \
  || { echo 'RECORD WRITER FAILED'; exit 1; }
echo 'R5 identity comparisons: all three PASS_BITWISE_EQUAL; records written to records/R5_V001'
exit 0
