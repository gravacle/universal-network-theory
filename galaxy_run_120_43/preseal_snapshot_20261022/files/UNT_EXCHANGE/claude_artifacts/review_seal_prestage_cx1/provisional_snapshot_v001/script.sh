#!/bin/bash
# ROOT_SEAL_STEPS_c3v006.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY. Built by Claude3 (dispatch 0626).
# c3v006 supersedes ROOT_SEAL_STEPS_c3v005.sh (f43bab61): citation corrections only (README_SEAL_TOOLS v001 1e04bd2a rows L11-L14,
# recipe L16-L22, forms L26-L33; V005 line numbers are those of snapshot 27b62183, which A103 shifted by +12 in 643ef6ef).
# c3v005 superseded ROOT_SEAL_STEPS_c3v004.sh (d4659d4d): the v003 dispositions flags announced by Claude4 0105 (--dispositions
# D.json --dispositions-sha H) and helper c3v007 (accepts the 0105 row format). Tools stay v001 PLACEHOLDERS (P1).
# c3v004 superseded ROOT_SEAL_STEPS_c3v003.sh (8faa9e55; dry run 2): the STOPPED message goes to the original stderr (fd 3), not into a
# step log; helper c3v006 (manifest scans read path values only).
# c3v003 superseded ROOT_SEAL_STEPS_c3v002.sh (b0d0b8f2; dry-run pass A only): set -E so the STOPPED message also fires inside the
# step functions; the v003 dispositions flag must be published before use; the E-SEAL1 captures are pinned when created.
# c3v002 superseded ROOT_SEAL_STEPS.sh (f7590383, never run): covered-later comes ONLY from the root-supplied dispositions JSON
# (0633, seal tools v003 interface); r13 is the frozen compare candidate (0632); helper c3v005.
# Order of record: 0561 item 1 + A81 RI-19 (V005 27b62183 L1263) + A82 (L1241-1257) + prereg r5 seal_record_requirements[4]
# + SEAL_CHECKLIST_R5 (7ff81720) B1-B9 (L23-L32). It stops at the FIRST failure (set -e; every helper/tool exits 2 on REFUSE).
# Every input is verified from bytes before its step uses it; every file is created exclusively (open(...,'x') / noclobber / mkdir);
# nothing is overwritten, edited or deleted. Isolated pinned Python (-I -B); single-thread BLAS; no network. NOTHING TOUCHES THE
# REGISTERED C5H RUN EXCEPT STEP 9. This file writes nothing until root runs it.
#
# =================================================================================================================== PENDING TABLE
# Status at build (2026-10-18 ~21:40Z). The script REFUSES in step 0 while any item below is unresolved.
# | # | item                         | expected / candidates                                                          | resolved by            |
# |---|------------------------------|--------------------------------------------------------------------------------|------------------------|
# | P1| seal tools v003 (Claude4;    | NOT LANDED: T1..T4 below are v001 PLACEHOLDERS (v001 tools 3/4 are pinned to   | successor script pins  |
# |   | 0633/0634: v002 + D-05 + B8) | prereg r4 e3b6b5b2 and miss ddo_gas_M_s, D-01: they REFUSE r5); the v003 flag  | v003 paths, shas and   |
# |   |                              | for the dispositions JSON is a PLACEHOLDER (T_DISPOSITIONS_FLAG)               | the dispositions flag  |
# | P2| compare reviewed source      | r13 FROZEN 21:22Z: kmax_tail_compare_c2v007_r13_cx3v001.py f5adfd11, SELECTED_R13| env (root, invocation) |
# |   |                              | 10acd098 (A102); the slot waits for the Claude3 + Codex2 deltas, 0 blocking   |                        |
# | P3| driver check record (RI-36)  | CHECK.md 89a6de88 | Codex3 0602 R5_REVIEW_FINAL_V001.md 6758bd24               | env (root ruling)      |
# | P4| EPS_NGC, I1T_NGC (GAP-12)    | EPS_CERT_NGC91_V001 1d5eef1b; I1T_NGC_T120L_V001 3ae7981a (single candidates) | env (root ruling)      |
# | P5| dispositions JSON (0633;     | root writes it at assembly: $CTRL/V007_SEAL_ASSEMBLY_INPUTS/                   | env path + sha (root)  |
# |   | RI-34; A81 RI-26)            | COVERED_LATER_DISPOSITIONS_V007.json: {entry, disposition revised|no_change,   |                        |
# |   |                              | reason non-empty} for every entry after A101 (now A102) + any changed row      |                        |
# | P6| B7 inputs (GAP-17)           | key-equivalence map (RI-30), NEW-item disposition list (A81 RI-20), raw        | env (root/owners)      |
# |   |                              | successor-custody record (A59; root UVT read)                                  |                        |
# | P7| CASCADE_MAP_R5_ADDENDUM      | required before the seal on r5 (r5 seal_record_requirements[9]; RI-32)         | env (owner TBD)        |
# | P8| C5H run dir spelling         | one of the sealed compare's C5H_REGISTERED_RUN_DIRS (string compare only)      | env (root)             |
# | P9| open rulings acknowledged    | RI-28..RI-37 and GAP-12 (ROOT_ITEMS_R5 2387dc23), incl. RI-29 BUILD_V007       | env UNT_SEAL_ROOT_ACK  |
# |   |                              | adoption, RI-31 B0 record, RI-33 B0_N3/B0_RO1/I4, RI-37 SR_K registry reading  |                        |
# |P10| free-space floor (RUNBOOK_V008 L37) | root's GiB floor for the internal output root                          | env UNT_SEAL_MIN_FREE_GIB |
# Outputs created by this script (expected paths; FIXED = a text of record fixes the path, PROPOSED = this builder's proposal):
#   FROZEN addendum ........ $CTRL/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md     FIXED (r5 path_to_be; FORMAT_V005 L14)
#   seal folder ............ $CTRL/V007_SEAL_ASSEMBLY[_ATTEMPT_n]/                                           PROPOSED
#   driver BUILD record .... <seal folder>/DRIVER_BUILD_RECORD_R5_V007_SEAL.json                             PROPOSED (SEAL_CHECKLIST_R5 B2a)
#   bound plan / command ... $PKT/P128/LAUNCH_{PLAN,COMMAND}_V011_CX3V001_BOUND_R5_V007_SEAL[_ATTEMPT_n].{json,txt}  PROPOSED names; under the
#                            binder folder FIXED (binder L18)
#   slots, sealed prereg, sealed compare, E-SEAL1 outputs, SEAL_RECORD, receipt: <seal folder>/...                  PROPOSED
#   ROOT_SEAL_ADMISSION config $PKT/ROOT_SEAL_ADMISSION_V001.json                                              FIXED (guard v008 L8; FORMAT_V005 L7)
#
# Root-supplied inputs (environment, all REQUIRED):
#   UNT_SEAL_FREEZE_V005_SHA256           the open V005 sha root has read and freezes (step 1 refuses any other bytes)
#   UNT_SEAL_DISPOSITIONS_PATH / _SHA256  the dispositions JSON (under $CTRL/V007_SEAL_ASSEMBLY_INPUTS/), verified before tools 1, 3, 4;
#                                         format: Claude4 0105 / the v003 README (frozen_addendum_sha256; rows entry, disposition,
#                                         reason, section_sha256 [, change]) for every entry after A101 plus any changed table row
#   UNT_SEAL_COMPARE_REVIEWED_PATH / _SHA256      the reviewed compare source (r13), seal-time pins unset
#   UNT_SEAL_COMPARE_SELECTION_PATH / _SHA256     its SELECTED record (must name that path and sha)
#   UNT_SEAL_DRIVER_CHECK_RECORD_PATH / _SHA256   RI-36 ruling (one of the two candidates)
#   UNT_SEAL_RULING_EPS_NGC, UNT_SEAL_RULING_I1T_NGC   full sha of the ruled record (must equal the draft's single candidate)
#   UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH / _SHA256, UNT_SEAL_NEW_ITEM_LIST_PATH / _SHA256, UNT_SEAL_SUCCESSOR_CUSTODY_PATH / _SHA256
#   UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_PATH / _SHA256
#   UNT_SEAL_C5H_RUN_DIR                  the C5H run directory spelling for step 9 (string only until step 9)
#   UNT_SEAL_MIN_FREE_GIB                 integer
#   UNT_SEAL_ROOT_ACK                     exactly: RI-28,RI-29,RI-30,RI-31,RI-32,RI-33,RI-34,RI-35,RI-36,RI-37,GAP-12
#   UNT_SEAL_ATTEMPT                      optional, default 1 (n > 1: fresh seal folder and bound names; the FROZEN copy is reused
#                                         only if it exists with exactly the stated bytes)
# =================================================================================================================================
set -Eeuo pipefail
set -o noclobber
umask 022
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
cd /
STEP=preflight
exec 3>&2
trap 'echo "ROOT_SEAL_STEPS: STOPPED at step ${STEP} (exit $?). Nothing after this step ran." >&3' ERR

# ============================================================================================================ PINS (substitutable)
PY="/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
PY_REAL_SHA="8506f337a83611246ffcff62d6e96c6d2269e5db48508ca3ac2553d56c962aee"
A="/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts"
CTRL="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2"
PKT="$A/v007_launch_packet_cx1"
C3="$A/seal_assembly_c3"
HELPER="$C3/tools/seal_steps_c3sa_c3v007.py";          HELPER_SHA="2f08fb88c17dbe340fe5f03da10ed510aff384cdb404d8e3d9544664d2d79172"
FENCE="$C3/tools/fence_c3sa_c3v003.py";                 FENCE_SHA="9c62ad4902c895f0aeeba3a78976b5944146ee0de153989dbc79470528dd2863"
DRAFT="$C3/SLOT_VALUES_DRAFT.json";                     DRAFT_SHA="c93691f5d1931beef8abb656ced3446c99d0adf286d4b5de0c709ecb570284ba"
MANIFEST_GATES="$C3/MANIFEST_GATES_ONLY_DRAFT_C3SA.json"; MANIFEST_GATES_SHA="e5967bb9901fda39703553c5c02b4d11a580ef8456f6c0b7d315ee4c750f09da"
PREREG_TOR="$A/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json"; PREREG_TOR_SHA="3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393"
OPEN_V005="$CTRL/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md"
DRIVER="$A/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py"; DRIVER_SHA="b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6"
BINDER="$PKT/bind_sealed_launch_plan_cx1v001.py";      BINDER_SHA="f3e4e2beeb8f1cb151892fd903b889c471cea58fea1b67c72552137d037575ca"
TEMPLATE="$PKT/P128/LAUNCH_PLAN_V011_CX3V001.json";    TEMPLATE_SHA="1b406591784ab4647e4aaf2686d9b3d18a259fadb435391439d2ff75df22ad3c"
BUILD="$PKT/BUILD_V007.md";                             BUILD_SHA="94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de"
ALLOWLIST="$PKT/ALLOWLIST_DRAFT_V006_CX3V001.txt";      ALLOWLIST_SHA="18300b52fdef500defacae06e4b98564534cd37661874ae7e2aa92d5c9f5fc47"
PRODUCER_INDEX="$PKT/PRODUCER_INDEX_V009_CX3V001.json"; PRODUCER_INDEX_SHA="7a61747efeee8ff27e8e5b3c2213a0aa2f3e8ed888e871ac1df193a6a64b6a97"
GUARD="$PKT/producer_guard_cx1v008.py";                 GUARD_SHA="294cb7760679b883a62fb3117dc75e91231b2f173bcec65983e6762371ea0731"
LAUNCHER="$PKT/route_a_token_launcher_cx1v007.py";      LAUNCHER_SHA="861bba68dd7d207beb30ed828c1557955f31979cf2e15369acccc52ea595953d"
REGISTRY="$A/producer_registry_c3/out/PRODUCER_REGISTRY_C3V009.json"; REGISTRY_SHA="32ddadcb7567213f42288004f19def122da1d8c4db1a426f0f888bc3242484e8"
IDREC_Z2="$A/tail_scheme_impl_c2/gates_v007/r2/records/R5_V001/B1_R5_C2V007.json";              IDREC_Z2_SHA="83e7b0673159156832995a1d7caae401a430918cbd110975bac8e18335aedc72"
IDREC_Z2OFF="$A/tail_scheme_impl_c2/gates_v007/r2/records/R5_V001/B1_OFF_R5_C2V007.json";       IDREC_Z2OFF_SHA="3b9ad4029a8673eabfa87b2fe77ea66241589412291c44af5d0b220a6fad3df2"
IDREC_B0P="$A/tail_scheme_impl_c2/gates_v007/r2/records/R5_V001/B0prime_RERUN_R5_C2V007.json"; IDREC_B0P_SHA="e33af53d1df36d858ed887bc4ed24fae77fe606d88ab26e2a77d9e5481d09258"
B0_RECORD="$A/seal_records_c4/build/records/B0_R5_RECORD_C4V001.json"; B0_RECORD_SHA="c2cec35b1821a9868816405c8442ad20c831c0b4cbb599016593959f5b450c1b"
# seal tools: v001 PLACEHOLDERS (P1). A successor script pins v003 here and its exact dispositions flag.
SEAL_TOOLS_STATUS="PENDING_V003__V001_PLACEHOLDERS"
SEAL_TOOLS_COVERED_LATER_MODE="v003_dispositions"      # v003 interface (0633): tools 1, 3, 4 take the dispositions JSON
T_DISPOSITIONS_FLAG="--dispositions"; T_DISPOSITIONS_SHA_FLAG="--dispositions-sha"   # v003 flags as announced (Claude4 0105)
T_DISPOSITIONS_FLAG_STATUS="ANNOUNCED_0105_UNPUBLISHED"  # the successor sets PUBLISHED when the v003 files and README land
SEAL_INPUTS_DIR="$CTRL/V007_SEAL_ASSEMBLY_INPUTS"        # root writes the dispositions JSON here at assembly
TD="$A/v007_final_prereg_c4/seal_tools"
T_COMMON="$TD/seal_common_c4v001.py";          T_COMMON_SHA="43d8f8eb610106c61be197defba59cff7f357bb31c70ca9c9136a44b5d267c25"
T1="$TD/check_frozen_addendum_c4v001.py";      T1_SHA="c4ebbb5bf69bb8b9c2ea82046c3553897a246cefc417f2d8bc556b10c62381e2"
T2="$TD/check_sealed_compare_c4v001.py";       T2_SHA="b339a8f6051ffe7a596179216ec3ba6e103a14356ed13befa51cf3529110b3ed"
T3="$TD/check_slot_fill_c4v001.py";            T3_SHA="7f3cf07da0d92fef0a1cc592cb644eafca2737e90b917e83ea9ffa5fc367187b"
T4="$TD/build_seal_record_c4v001.py";          T4_SHA="3091fc2afa2e16f74d8c634d8605205c792788924f078b5aae806351a1d18c70"
T1_RUN=("$PY" -I -B "$T1"); T2_RUN=("$PY" -I -B "$T2"); T3_RUN=("$PY" -I -B "$T3"); T4_RUN=("$PY" -I -B "$T4")
TOOL_PINS=("$T_COMMON=$T_COMMON_SHA" "$T1=$T1_SHA" "$T2=$T2_SHA" "$T3=$T3_SHA" "$T4=$T4_SHA")
# compare: superseded candidates are refused as the reviewed source (A102: r13 supersedes r12; A90/A91: r11; A79: r10)
COMPARE_SUPERSEDED_SHAS="4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28 a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a e801adc41462bbc9dd8e81ff915b93981c3f2ec4930cb1fb9df26a78cbe18b93"
# RI-36 admissible candidates (path|sha)
DRIVER_CHECK_CANDIDATES="$A/tail_scheme_impl_c2/driver_r5/check/CHECK.md|89a6de88739e1c4b76c39dc11d7417d7e243b7235511d8ea0951e1493865b632
$A/review_r5_certs_cx3/R5_REVIEW_FINAL_V001.md|6758bd24784ec514d73054a30a8fdd673c3d0c571521a62514ba4260f3ad7ba9"
REQUIRED_ACK="RI-28,RI-29,RI-30,RI-31,RI-32,RI-33,RI-34,RI-35,RI-36,RI-37,GAP-12"
INTERNAL_OUTPUT_ROOT="/Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007"     # RUNBOOK_V008 L37 / template outputs
# ---------------------------------------------------------------------------------------------------- OUTPUTS (substitutable)
ATTEMPT="${UNT_SEAL_ATTEMPT:-1}"
case "$ATTEMPT" in 1) SFX="";; [2-9]) SFX="_ATTEMPT_$ATTEMPT";; *) echo "UNT_SEAL_ATTEMPT must be 1-9" >&2; false;; esac
FROZEN="$CTRL/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md"
SEAL_DIR="$CTRL/V007_SEAL_ASSEMBLY$SFX"
BOUND_PLAN="$PKT/P128/LAUNCH_PLAN_V011_CX3V001_BOUND_R5_V007_SEAL$SFX.json"
BOUND_COMMAND="$PKT/P128/LAUNCH_COMMAND_V011_CX3V001_BOUND_R5_V007_SEAL$SFX.txt"
CONFIG="$PKT/ROOT_SEAL_ADMISSION_V001.json"
DRAFT_PATHS_MUST_MATCH=1              # attempt 1: the output paths above equal the draft's documented paths
EXPECT_CONFIG_IS_GUARD_CONFIG=True    # the config is the guard's own CONFIG path
STEP8_MODE=root                       # step 8 reads the three identity-run trees (root only), fenced against the C5H run
STEP8_STANDIN=""
# =================================================================================================================================
LOGS="$SEAL_DIR/logs"
DRIVER_BUILD_RECORD="$SEAL_DIR/DRIVER_BUILD_RECORD_R5_V007_SEAL.json"
SLOTS_FINAL="$SEAL_DIR/SLOT_VALUES_FINAL_V007.json"
SEALED_PREREG="$SEAL_DIR/KMAX_TAIL_PREREG_V007_SEALED.json"
GATES_OUTDIR="$SEAL_DIR/E_SEAL1_GATES_ONLY_OUT";        GATES_STDOUT="$SEAL_DIR/E_SEAL1_GATES_ONLY.stdout.txt"
C5H_MANIFEST="$SEAL_DIR/MANIFEST_VALIDITY_C5H_V007.json"
VALIDITY_OUTDIR="$SEAL_DIR/E_SEAL1_VALIDITY_ONLY_C5H_OUT"; VALIDITY_STDOUT="$SEAL_DIR/E_SEAL1_VALIDITY_ONLY_C5H.stdout.txt"
T4_STDOUT="$SEAL_DIR/SEAL_RECORD_CANDIDATE_TOOL4.stdout.json"; T4_STDERR="$SEAL_DIR/SEAL_RECORD_TOOL4.stderr.json"
SEAL_RECORD="$SEAL_DIR/SEAL_RECORD_V007.json"
RECEIPT="$SEAL_DIR/SEAL_ADMISSION_RECEIPT_V001.json"
SUMMARY="$SEAL_DIR/SEAL_ASSEMBLY_SUMMARY_V007.json"

H() { "$PY" -I -B "$HELPER" "$@"; }
# jf FILE KEY.PATH  -> prints the value (strict JSON read)
jf() { "$PY" -I -B -c 'import json,sys
d=json.loads(open(sys.argv[1],"rb").read())
for k in sys.argv[2].split("."):
    d=d[int(k)] if isinstance(d,list) else d[k]
print(d if not isinstance(d,(dict,list)) else json.dumps(d))' "$1" "$2"; }
# run_h LOGNAME helper-args...   (helper verdict -> $LOGS/LOGNAME.json, exclusive)
run_h() { local log="$LOGS/$1.json"; shift; H "$@" 2> "$log"; echo "  PASS  $(basename "$log")"; }
sha_of() { /usr/bin/shasum -a 256 "$1" | /usr/bin/cut -d' ' -f1; }
v005_still_frozen() { H same-bytes --open "$OPEN_V005" --frozen "$FROZEN" --frozen-sha "$FROZEN_SHA" 2> "$LOGS/V005_STILL_FROZEN_BEFORE_$1.json"; }
need() { local v; for v in "$@"; do if [ -z "${!v+x}" ]; then echo "REFUSE: root input $v is not set" >&2; false; fi; done; }

# ======================================================================================================== STEP 0: preflight
step0_preflight() {
  STEP=0; echo "STEP 0 preflight (writes nothing)"
  # interpreter: the pinned isolated Python, its real bytes, UTF-8 stdout
  [ "$(sha_of "$("$PY" -I -B -c 'import os,sys; print(os.path.realpath(sys.executable))')")" = "$PY_REAL_SHA" ]
  [ "$("$PY" -I -B -c 'import sys; print(sys.stdout.encoding.lower().replace("-",""), sys.version_info[:2])')" = "utf8 (3, 12)" ]
  [ "$(sha_of "$HELPER")" = "$HELPER_SHA" ]                       # the helper verifies everything else from bytes
  case "$SEAL_TOOLS_STATUS $PY $A $CTRL $PKT $HELPER $DRAFT $FROZEN $SEAL_DIR $BOUND_PLAN $BOUND_COMMAND $CONFIG" in
    *PENDING*) echo "REFUSE: a PINS value is still PENDING (P1: seal tools v002 not pinned)" >&2; false;; esac
  need UNT_SEAL_FREEZE_V005_SHA256 UNT_SEAL_DISPOSITIONS_PATH UNT_SEAL_DISPOSITIONS_SHA256 UNT_SEAL_COMPARE_REVIEWED_PATH UNT_SEAL_COMPARE_REVIEWED_SHA256 \
       UNT_SEAL_COMPARE_SELECTION_PATH UNT_SEAL_COMPARE_SELECTION_SHA256 UNT_SEAL_DRIVER_CHECK_RECORD_PATH \
       UNT_SEAL_DRIVER_CHECK_RECORD_SHA256 UNT_SEAL_RULING_EPS_NGC UNT_SEAL_RULING_I1T_NGC UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH \
       UNT_SEAL_KEY_EQUIVALENCE_MAP_SHA256 UNT_SEAL_NEW_ITEM_LIST_PATH UNT_SEAL_NEW_ITEM_LIST_SHA256 UNT_SEAL_SUCCESSOR_CUSTODY_PATH \
       UNT_SEAL_SUCCESSOR_CUSTODY_SHA256 UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_PATH UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_SHA256 \
       UNT_SEAL_C5H_RUN_DIR UNT_SEAL_MIN_FREE_GIB UNT_SEAL_ROOT_ACK
  [ "$UNT_SEAL_ROOT_ACK" = "$REQUIRED_ACK" ] || { echo "REFUSE: UNT_SEAL_ROOT_ACK must be exactly $REQUIRED_ACK (P9)" >&2; false; }
  case "$UNT_SEAL_MIN_FREE_GIB" in ''|*[!0-9]*) echo "REFUSE: UNT_SEAL_MIN_FREE_GIB must be an integer" >&2; false;; esac
  case " $COMPARE_SUPERSEDED_SHAS " in *" $UNT_SEAL_COMPARE_REVIEWED_SHA256 "*) echo "REFUSE: the compare source is a superseded round (A102)" >&2; false;; esac
  printf '%s\n' "$DRIVER_CHECK_CANDIDATES" | /usr/bin/grep -qxF "$UNT_SEAL_DRIVER_CHECK_RECORD_PATH|$UNT_SEAL_DRIVER_CHECK_RECORD_SHA256" \
    || { echo "REFUSE: the driver check record is not an RI-36 candidate (a different record needs a successor draft)" >&2; false; }
  case "$UNT_SEAL_C5H_RUN_DIR" in *KMAX_A2F10_C5H_RUN_V001) ;; *) echo "REFUSE: UNT_SEAL_C5H_RUN_DIR" >&2; false;; esac
  case "$UNT_SEAL_DISPOSITIONS_PATH" in "$SEAL_INPUTS_DIR"/*.json) ;; *) echo "REFUSE: the dispositions JSON must lie in $SEAL_INPUTS_DIR (P5)" >&2; false;; esac
  case "$SEAL_TOOLS_COVERED_LATER_MODE" in v003_dispositions|v001_names) ;; *) echo "REFUSE: SEAL_TOOLS_COVERED_LATER_MODE" >&2; false;; esac
  if [ "$SEAL_TOOLS_COVERED_LATER_MODE" = v003_dispositions ] && [ "$T_DISPOSITIONS_FLAG_STATUS" != PUBLISHED ]; then
    echo "REFUSE: the v003 dispositions flag is a placeholder (P1)" >&2; false; fi
  # every input from bytes (the helper also refuses non-canonical, firmlink, /private, /.vol and protected spellings)
  H pin --pin "$FENCE=$FENCE_SHA" --pin "$DRAFT=$DRAFT_SHA" --pin "$MANIFEST_GATES=$MANIFEST_GATES_SHA" --pin "$PREREG_TOR=$PREREG_TOR_SHA" \
        --pin "$OPEN_V005=$UNT_SEAL_FREEZE_V005_SHA256" --pin "$DRIVER=$DRIVER_SHA" --pin "$BINDER=$BINDER_SHA" --pin "$TEMPLATE=$TEMPLATE_SHA" \
        --pin "$BUILD=$BUILD_SHA" --pin "$ALLOWLIST=$ALLOWLIST_SHA" --pin "$PRODUCER_INDEX=$PRODUCER_INDEX_SHA" --pin "$GUARD=$GUARD_SHA" \
        --pin "$LAUNCHER=$LAUNCHER_SHA" --pin "$REGISTRY=$REGISTRY_SHA" --pin "$IDREC_Z2=$IDREC_Z2_SHA" --pin "$IDREC_Z2OFF=$IDREC_Z2OFF_SHA" \
        --pin "$IDREC_B0P=$IDREC_B0P_SHA" --pin "$B0_RECORD=$B0_RECORD_SHA" \
        --pin "$UNT_SEAL_COMPARE_REVIEWED_PATH=$UNT_SEAL_COMPARE_REVIEWED_SHA256" --pin "$UNT_SEAL_COMPARE_SELECTION_PATH=$UNT_SEAL_COMPARE_SELECTION_SHA256" \
        --pin "$UNT_SEAL_DRIVER_CHECK_RECORD_PATH=$UNT_SEAL_DRIVER_CHECK_RECORD_SHA256" \
        --pin "$UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH=$UNT_SEAL_KEY_EQUIVALENCE_MAP_SHA256" --pin "$UNT_SEAL_NEW_ITEM_LIST_PATH=$UNT_SEAL_NEW_ITEM_LIST_SHA256" \
        --pin "$UNT_SEAL_SUCCESSOR_CUSTODY_PATH=$UNT_SEAL_SUCCESSOR_CUSTODY_SHA256" \
        --pin "$UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_PATH=$UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_SHA256" \
        --pin "$UNT_SEAL_DISPOSITIONS_PATH=$UNT_SEAL_DISPOSITIONS_SHA256" $(printf -- '--pin %s ' "${TOOL_PINS[@]}")
  # the SELECTED record names exactly the supplied compare (format-agnostic: both strings in its bytes; a selected_source dict must equal)
  "$PY" -I -B -c 'import json,sys
b=open(sys.argv[1],"rb").read(); t=b.decode("utf-8")
assert sys.argv[2] in t and sys.argv[3] in t, "SELECTION_DOES_NOT_NAME_THE_COMPARE"
try: d=json.loads(b)
except ValueError: d=None
if isinstance(d,dict) and isinstance(d.get("selected_source"),dict):
    s=d["selected_source"]; assert s.get("path")==sys.argv[2] and s.get("sha256")==sys.argv[3], "SELECTED_SOURCE_DIFFERS"
' "$UNT_SEAL_COMPARE_SELECTION_PATH" "$UNT_SEAL_COMPARE_REVIEWED_PATH" "$UNT_SEAL_COMPARE_REVIEWED_SHA256"
  # the draft's FILLED pins are the PINS this script binds with
  [ "$(jf "$DRAFT" driver.path)" = "$DRIVER" ] && [ "$(jf "$DRAFT" driver.sha256)" = "$DRIVER_SHA" ]
  [ "$(jf "$DRAFT" producer_registry.path)" = "$REGISTRY" ] && [ "$(jf "$DRAFT" producer_registry.sha256)" = "$REGISTRY_SHA" ]
  [ "$(jf "$DRAFT" launch_packet.build.path)" = "$BUILD" ] && [ "$(jf "$DRAFT" launch_packet.build.sha256)" = "$BUILD_SHA" ]
  [ "$(jf "$DRAFT" identity_gate_records.Z2.sha256)" = "$IDREC_Z2_SHA" ] && [ "$(jf "$DRAFT" identity_gate_records.Z2_OFF_RO1.sha256)" = "$IDREC_Z2OFF_SHA" ] \
    && [ "$(jf "$DRAFT" identity_gate_records.B0prime_RERUN.sha256)" = "$IDREC_B0P_SHA" ]
  if [ "$DRAFT_PATHS_MUST_MATCH" = 1 ] && [ "$ATTEMPT" = 1 ]; then
    [ "$(jf "$DRAFT" frozen_addendum.path)" = "$FROZEN" ] && [ "$(jf "$DRAFT" driver_build_record.path)" = "$DRIVER_BUILD_RECORD" ] \
      && [ "$(jf "$DRAFT" launch_packet.bound_plan.path)" = "$BOUND_PLAN" ] && [ "$(jf "$DRAFT" launch_packet.bound_command.path)" = "$BOUND_COMMAND" ]
  fi
  # outputs are fresh (the FROZEN copy may pre-exist only on attempt > 1, and then only with the stated bytes: step 1)
  H absent --path "$SEAL_DIR" --path "$BOUND_PLAN" --path "$BOUND_COMMAND" --path "$CONFIG"
  if [ "$ATTEMPT" = 1 ]; then H absent --path "$FROZEN"; fi
  echo "  PASS  preflight"
}

# ======================================================================================= STEP 1 (B1): exclusive FROZEN addendum
step1_freeze() {
  STEP=1; echo "STEP 1 freeze the V005 addendum (SEAL_CHECKLIST_R5 L23 B1; r5 srr[4](1); A81 RI-26 V005@27b62183 L1270; A82 V005@27b62183 L1255; FORMAT_V005 L14)"
  /bin/mkdir "$SEAL_DIR"; /bin/mkdir "$LOGS"
  if [ "$ATTEMPT" != 1 ] && [ -e "$FROZEN" ]; then
    H pin --pin "$FROZEN=$UNT_SEAL_FREEZE_V005_SHA256" 2> "$LOGS/STEP_01_FROZEN_REUSED.json"; FROZEN_SHA="$UNT_SEAL_FREEZE_V005_SHA256"
    echo "  PASS  FROZEN copy reused (attempt $ATTEMPT): exactly the stated bytes"
  else
    run_h STEP_01_FREEZE freeze --open "$OPEN_V005" --open-sha "$UNT_SEAL_FREEZE_V005_SHA256" --out "$FROZEN"
    FROZEN_SHA="$(jf "$LOGS/STEP_01_FREEZE.json" frozen.sha256)"
  fi
  echo "  >>> From now on root writes NOTHING to $OPEN_V005; later entries go to a V006 addendum (A82; A99.6)."
}

# ===================================================================== STEP 2: tool 1 (check_frozen_addendum) + entry-table re-hash
step2_tool1() {
  STEP=2; echo "STEP 2 tool 1 check_frozen_addendum + r5 entry-table re-hash (README_SEAL_TOOLS L11; SEAL_CHECKLIST_R5 L23; r5 srr[11]; 0633; Claude4 0105)"
  v005_still_frozen 2
  # the dispositions JSON first (0633): no bare name, no empty reason, exactly the entries after the table plus any changed row
  run_h STEP_02_DISPOSITIONS dispositions --prereg "$PREREG_TOR" --prereg-sha "$PREREG_TOR_SHA" --frozen "$FROZEN" --frozen-sha "$FROZEN_SHA" \
        --dispositions "$UNT_SEAL_DISPOSITIONS_PATH" --dispositions-sha "$UNT_SEAL_DISPOSITIONS_SHA256"
  COVERED_NAMES="$(jf "$LOGS/STEP_02_DISPOSITIONS.json" covered_later_names_for_v001)"
  if [ "$SEAL_TOOLS_COVERED_LATER_MODE" = v003_dispositions ]; then
    COV_ARGS=("$T_DISPOSITIONS_FLAG" "$UNT_SEAL_DISPOSITIONS_PATH" "$T_DISPOSITIONS_SHA_FLAG" "$UNT_SEAL_DISPOSITIONS_SHA256")
  else COV_ARGS=(--covered-later "$COVERED_NAMES"); fi      # v001 placeholders take bare names only (the D-05 defect v003 closes)
  H pin --pin "$PREREG_TOR=$PREREG_TOR_SHA" --pin "$FROZEN=$FROZEN_SHA" --pin "$T1=$T1_SHA" --pin "$T_COMMON=$T_COMMON_SHA" \
        --pin "$UNT_SEAL_DISPOSITIONS_PATH=$UNT_SEAL_DISPOSITIONS_SHA256" 2> "$LOGS/STEP_02_INPUTS.json"
  "${T1_RUN[@]}" --prereg "$PREREG_TOR" --frozen "$FROZEN" --expect-frozen-sha "$FROZEN_SHA" "${COV_ARGS[@]}" > "$LOGS/STEP_02_TOOL1.json"
  echo "  PASS  STEP_02_TOOL1.json"
  run_h STEP_02_REHASH rehash-entries --prereg "$PREREG_TOR" --prereg-sha "$PREREG_TOR_SHA" --frozen "$FROZEN" --frozen-sha "$FROZEN_SHA" \
        --dispositions "$UNT_SEAL_DISPOSITIONS_PATH" --dispositions-sha "$UNT_SEAL_DISPOSITIONS_SHA256"
}

# ================================================================================ STEP 2a (B2/B2a): driver r5 and its BUILD record
step2a_driver_build() {
  STEP=2a; echo "STEP 2a driver r5 + exclusive driver BUILD record (SEAL_CHECKLIST_R5 L24-L25 B2/B2a; r5 srr[8]; A72; A96)"
  v005_still_frozen 2a
  run_h STEP_02A_DRIVER_BUILD driver-build-record --compare "$UNT_SEAL_COMPARE_REVIEWED_PATH" --compare-sha "$UNT_SEAL_COMPARE_REVIEWED_SHA256" \
        --check-record "$UNT_SEAL_DRIVER_CHECK_RECORD_PATH" --check-sha "$UNT_SEAL_DRIVER_CHECK_RECORD_SHA256" --fence "$FENCE" --fence-sha "$FENCE_SHA" \
        --out "$DRIVER_BUILD_RECORD"
  DBR_SHA="$(jf "$LOGS/STEP_02A_DRIVER_BUILD.json" driver_build_record.sha256)"
  [ "$(jf "$LOGS/STEP_02A_DRIVER_BUILD.json" driver.sha256)" = "$DRIVER_SHA" ]
}

# ============================================================================ STEP 3 (B3): pre-binding output-root check + binder
step3_bind() {
  STEP=3; echo "STEP 3 build-only binder: bound plan and command (SEAL_CHECKLIST_R5 L26 B3; A81 RI-25 V005@27b62183 L1269; RUNBOOK_V008 L19, L37)"
  v005_still_frozen 3
  H pin --pin "$BINDER=$BINDER_SHA" --pin "$TEMPLATE=$TEMPLATE_SHA" --pin "$DRIVER=$DRIVER_SHA" --pin "$FROZEN=$FROZEN_SHA" 2> "$LOGS/STEP_03_INPUTS.json"
  # RUNBOOK_V008 L37 (before binding): internal startup Data volume, no symlink redirection, fresh outputs, free space
  "$PY" -I -B -c 'import json,os,sys,shutil
t=json.loads(open(sys.argv[1],"rb").read()); root=sys.argv[2]; floor=int(sys.argv[3])
outs=[t["launcher_log"]]+[p for c in t["calls"] for p in (c["outdir"],c["receipt"],c["receipt"]+".launch.json",c["monitor_log"])]
assert len(outs)==41==len(set(outs)) and all(o.startswith(root+"/") for o in outs), "TEMPLATE_OUTPUTS"
assert not any(os.path.lexists(o) for o in outs), "TEMPLATE_OUTPUT_EXISTS"
a=root
while not os.path.lexists(a): a=os.path.dirname(a)
cur=a
while cur!="/":
    assert not os.path.islink(cur), "SYMLINK_ON_OUTPUT_ROOT "+cur
    cur=os.path.dirname(cur)
assert os.stat(a).st_dev==os.stat("/Users/bgm/Research").st_dev, "OUTPUT_ROOT_NOT_ON_THE_RESEARCH_DATA_VOLUME"
free=shutil.disk_usage(a).free/2**30
assert free>=floor, "FREE_GIB %.0f < %d" % (free, floor)
print(json.dumps({"existing_ancestor":a,"free_gib":int(free),"outputs_fresh":41,"no_symlink":True}))' "$TEMPLATE" "$INTERNAL_OUTPUT_ROOT" "$UNT_SEAL_MIN_FREE_GIB" > "$LOGS/STEP_03_PREBIND_OUTPUT_ROOT.json"
  "$PY" -I -B "$BINDER" --template "$TEMPLATE" --driver "$DRIVER" --driver-sha256 "$DRIVER_SHA" --frozen-addendum "$FROZEN" \
        --frozen-addendum-sha256 "$FROZEN_SHA" --plan-out "$BOUND_PLAN" --command-out "$BOUND_COMMAND" > "$LOGS/STEP_03_BINDER.json"
  BP_SHA="$(jf "$LOGS/STEP_03_BINDER.json" plan.sha256)"; BC_SHA="$(jf "$LOGS/STEP_03_BINDER.json" command.sha256)"
  # the binder's resolved pin strings must be byte-identical to the strings this seal uses (r4 N7; README "Path strings")
  [ "$(jf "$LOGS/STEP_03_BINDER.json" plan.path)" = "$BOUND_PLAN" ] && [ "$(jf "$LOGS/STEP_03_BINDER.json" command.path)" = "$BOUND_COMMAND" ]
  [ "$(jf "$LOGS/STEP_03_BINDER.json" driver.path)" = "$DRIVER" ] && [ "$(jf "$LOGS/STEP_03_BINDER.json" frozen_addendum.path)" = "$FROZEN" ]
  [ "$(jf "$LOGS/STEP_03_BINDER.json" frozen_addendum.sha256)" = "$FROZEN_SHA" ]
  H pin --pin "$BOUND_PLAN=$BP_SHA" --pin "$BOUND_COMMAND=$BC_SHA" 2> "$LOGS/STEP_03_OUTPUTS.json"
  echo "  PASS  STEP_03_BINDER.json"
}

# ======================================================================================= STEP 3a: the final slot values (from bytes)
step3a_fill() {
  STEP=3a; echo "STEP 3a fill SLOT_VALUES_FINAL from the draft + run-time pins + root rulings (README_SEAL_TOOLS L27 mapping, L33 'Slot JSON')"
  v005_still_frozen 3a
  run_h STEP_03A_FILL_SLOTS fill-slots --draft "$DRAFT" --draft-sha "$DRAFT_SHA" --out "$SLOTS_FINAL" \
        --runtime "FROZEN_ADDENDUM=$FROZEN=$FROZEN_SHA" --runtime "DRIVER_BUILD_RECORD=$DRIVER_BUILD_RECORD=$DBR_SHA" \
        --runtime "BOUND_PLAN=$BOUND_PLAN=$BP_SHA" --runtime "BOUND_COMMAND=$BOUND_COMMAND=$BC_SHA" \
        --runtime "COMPARE_REVIEWED_SOURCE=$UNT_SEAL_COMPARE_REVIEWED_PATH=$UNT_SEAL_COMPARE_REVIEWED_SHA256" \
        --runtime "DRIVER_CHECK_RECORD=$UNT_SEAL_DRIVER_CHECK_RECORD_PATH=$UNT_SEAL_DRIVER_CHECK_RECORD_SHA256" \
        --expect "FROZEN_ADDENDUM=$FROZEN" --expect "DRIVER_BUILD_RECORD=$DRIVER_BUILD_RECORD" --expect "BOUND_PLAN=$BOUND_PLAN" \
        --expect "BOUND_COMMAND=$BOUND_COMMAND" --expect "COMPARE_REVIEWED_SOURCE=$UNT_SEAL_COMPARE_REVIEWED_PATH" \
        --ruling "EPS_NGC=$UNT_SEAL_RULING_EPS_NGC" --ruling "I1T_NGC=$UNT_SEAL_RULING_I1T_NGC"
  SLOTS_SHA="$(jf "$LOGS/STEP_03A_FILL_SLOTS.json" slots_final.sha256)"
}

# ================================================================================================= STEP 4 (B4): the sealed prereg
step4_sealed_prereg() {
  STEP=4; echo "STEP 4 sealed prereg = r5 with every seal_slots.<k>.value filled (SEAL_CHECKLIST_R5 L27 B4; README_SEAL_TOOLS L26; r5 srr[4](3))"
  v005_still_frozen 4
  run_h STEP_04_SEALED_PREREG sealed-prereg --text-of-record "$PREREG_TOR" --tor-sha "$PREREG_TOR_SHA" --slots "$SLOTS_FINAL" --slots-sha "$SLOTS_SHA" \
        --out "$SEALED_PREREG"
  SP_SHA="$(jf "$LOGS/STEP_04_SEALED_PREREG.json" sealed_prereg.sha256)"
}

# =============================================================================================== STEP 5 (B5): the sealed compare
step5_sealed_compare() {
  STEP=5; echo "STEP 5 sealed compare: exactly the five seal-time pins set (SEAL_CHECKLIST_R5 L28 B5; A82 V005@27b62183 L1245; README_SEAL_TOOLS L28; r5 srr[4](4), srr[8])"
  v005_still_frozen 5
  local base; base="$(basename "$UNT_SEAL_COMPARE_REVIEWED_PATH" .py)"
  SEALED_COMPARE="$SEAL_DIR/${base}_SEALED_V007.py"
  run_h STEP_05_SEALED_COMPARE sealed-compare --reviewed "$UNT_SEAL_COMPARE_REVIEWED_PATH" --reviewed-sha "$UNT_SEAL_COMPARE_REVIEWED_SHA256" \
        --slots "$SLOTS_FINAL" --slots-sha "$SLOTS_SHA" --sealed-prereg "$SEALED_PREREG" --sealed-prereg-sha "$SP_SHA" --out "$SEALED_COMPARE"
  SC_SHA="$(jf "$LOGS/STEP_05_SEALED_COMPARE.json" sealed_compare.sha256)"
}

# =================================================================================================== STEP 6: tool 3 check_slot_fill
step6_tool3() {
  STEP=6; echo "STEP 6 check_slot_fill (README_SEAL_TOOLS L12, 'after B4')"
  v005_still_frozen 6
  H pin --pin "$SLOTS_FINAL=$SLOTS_SHA" --pin "$SEALED_PREREG=$SP_SHA" --pin "$PREREG_TOR=$PREREG_TOR_SHA" --pin "$FROZEN=$FROZEN_SHA" \
        --pin "$UNT_SEAL_DISPOSITIONS_PATH=$UNT_SEAL_DISPOSITIONS_SHA256" $(printf -- '--pin %s ' "${TOOL_PINS[@]}") 2> "$LOGS/STEP_06_INPUTS.json"
  "${T3_RUN[@]}" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" --text-of-record "$PREREG_TOR" --frozen "$FROZEN" \
        "${COV_ARGS[@]}" > "$LOGS/STEP_06_TOOL3.json"
  echo "  PASS  STEP_06_TOOL3.json"
}

# ============================================================================================== STEP 7: tool 2 check_sealed_compare
step7_tool2() {
  STEP=7; echo "STEP 7 check_sealed_compare (README_SEAL_TOOLS L13, 'after B5')"
  v005_still_frozen 7
  H pin --pin "$UNT_SEAL_COMPARE_REVIEWED_PATH=$UNT_SEAL_COMPARE_REVIEWED_SHA256" --pin "$SEALED_COMPARE=$SC_SHA" --pin "$SLOTS_FINAL=$SLOTS_SHA" \
        --pin "$SEALED_PREREG=$SP_SHA" $(printf -- '--pin %s ' "${TOOL_PINS[@]}") 2> "$LOGS/STEP_07_INPUTS.json"
  "${T2_RUN[@]}" --reviewed "$UNT_SEAL_COMPARE_REVIEWED_PATH" --sealed "$SEALED_COMPARE" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" > "$LOGS/STEP_07_TOOL2.json"
  echo "  PASS  STEP_07_TOOL2.json"
}

# ==================================================================================== STEP 8 (B6a): --gates-only (never the C5H run)
step8_gates_only() {
  STEP=8; echo "STEP 8 sealed compare --gates-only, fenced (SEAL_CHECKLIST_R5 L29 B6; r5 srr[0], srr[1]; A46 RA13; A47 I3)"
  v005_still_frozen 8
  run_h STEP_08_MANIFEST_CHECK check-manifest --sealed-compare "$SEALED_COMPARE" --sealed-compare-sha "$SC_SHA" --manifest "$MANIFEST_GATES" \
        --manifest-sha "$MANIFEST_GATES_SHA" --mode "gates-$STEP8_MODE" --identity-record "Z2=$IDREC_Z2=$IDREC_Z2_SHA" \
        --identity-record "Z2-OFF=$IDREC_Z2OFF=$IDREC_Z2OFF_SHA" --identity-record "B0prime_RERUN=$IDREC_B0P=$IDREC_B0P_SHA"
  H gates-only --fence "$FENCE" --fence-sha "$FENCE_SHA" --sealed-compare "$SEALED_COMPARE" --sealed-compare-sha "$SC_SHA" \
        --sealed-prereg "$SEALED_PREREG" --sealed-prereg-sha "$SP_SHA" --manifest "$MANIFEST_GATES" --manifest-sha "$MANIFEST_GATES_SHA" \
        --outdir "$GATES_OUTDIR" --mode "$STEP8_MODE" --standin "$STEP8_STANDIN" > "$GATES_STDOUT" 2> "$LOGS/STEP_08_GATES_ONLY.json"
  echo "  PASS  STEP_08_GATES_ONLY.json (fence refused 0)"
  run_h STEP_08_ROW_SCAN row-value-scan --path "$GATES_STDOUT"
  GS_SHA="$(jf "$LOGS/STEP_08_ROW_SCAN.json" e_seal1.sha256)"
}

# ============================================================== STEP 9 (B6b): --validity-only --case C5H (THE ONLY STEP THAT READS C5H)
step9_validity_c5h() {
  STEP=9; echo "STEP 9 sealed compare --validity-only --case C5H, booleans only, stdout to file (SEAL_CHECKLIST_R5 L29 B6; r5 srr[1]; A47 I3)"
  v005_still_frozen 9
  run_h STEP_09_MANIFEST make-c5h-manifest --sealed-compare "$SEALED_COMPARE" --sealed-compare-sha "$SC_SHA" --c5h-dir "$UNT_SEAL_C5H_RUN_DIR" \
        --b0-record "$B0_RECORD=$B0_RECORD_SHA" --out "$C5H_MANIFEST"
  local msha; msha="$(jf "$LOGS/STEP_09_MANIFEST.json" manifest_c5h.sha256)"
  run_h STEP_09_MANIFEST_CHECK check-manifest --sealed-compare "$SEALED_COMPARE" --sealed-compare-sha "$SC_SHA" --manifest "$C5H_MANIFEST" \
        --manifest-sha "$msha" --mode c5h
  H pin --pin "$SEALED_COMPARE=$SC_SHA" --pin "$SEALED_PREREG=$SP_SHA" --pin "$C5H_MANIFEST=$msha" 2> "$LOGS/STEP_09_INPUTS.json"
  "$PY" -I -B "$SEALED_COMPARE" --prereg "$SEALED_PREREG" --manifest "$C5H_MANIFEST" --outdir "$VALIDITY_OUTDIR" --validity-only --case C5H \
        > "$VALIDITY_STDOUT" 2> "$LOGS/STEP_09_VALIDITY_ONLY.stderr.txt"
  echo "  PASS  E_SEAL1_VALIDITY_ONLY_C5H.stdout.txt captured (not echoed)"
  run_h STEP_09_ROW_SCAN row-value-scan --path "$VALIDITY_STDOUT"
  VS_SHA="$(jf "$LOGS/STEP_09_ROW_SCAN.json" e_seal1.sha256)"
}

# =========================================================================== STEP 10 (B7a): tool 4 build_seal_record (prints the record)
step10_tool4() {
  STEP=10; echo "STEP 10 build_seal_record: record bytes to stdout, sha to stderr (README_SEAL_TOOLS L14, L16-L22; SEAL_CHECKLIST_R5 L30 B7)"
  v005_still_frozen 10
  H pin --pin "$SLOTS_FINAL=$SLOTS_SHA" --pin "$SEALED_PREREG=$SP_SHA" --pin "$PREREG_TOR=$PREREG_TOR_SHA" --pin "$FROZEN=$FROZEN_SHA" \
        --pin "$UNT_SEAL_COMPARE_REVIEWED_PATH=$UNT_SEAL_COMPARE_REVIEWED_SHA256" --pin "$SEALED_COMPARE=$SC_SHA" \
        --pin "$GATES_STDOUT=$GS_SHA" --pin "$VALIDITY_STDOUT=$VS_SHA" \
        --pin "$UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH=$UNT_SEAL_KEY_EQUIVALENCE_MAP_SHA256" --pin "$UNT_SEAL_NEW_ITEM_LIST_PATH=$UNT_SEAL_NEW_ITEM_LIST_SHA256" \
        --pin "$UNT_SEAL_SUCCESSOR_CUSTODY_PATH=$UNT_SEAL_SUCCESSOR_CUSTODY_SHA256" --pin "$UNT_SEAL_DISPOSITIONS_PATH=$UNT_SEAL_DISPOSITIONS_SHA256" \
        $(printf -- '--pin %s ' "${TOOL_PINS[@]}") 2> "$LOGS/STEP_10_INPUTS.json"
  "${T4_RUN[@]}" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" --text-of-record "$PREREG_TOR" --frozen "$FROZEN" \
        "${COV_ARGS[@]}" --reviewed "$UNT_SEAL_COMPARE_REVIEWED_PATH" --sealed-compare "$SEALED_COMPARE" \
        --gates-only-output "$GATES_STDOUT" --validity-only-output "$VALIDITY_STDOUT" --key-equivalence-map "$UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH" \
        --new-item-list "$UNT_SEAL_NEW_ITEM_LIST_PATH" --successor-custody "$UNT_SEAL_SUCCESSOR_CUSTODY_PATH" > "$T4_STDOUT" 2> "$T4_STDERR"
  run_h STEP_10_TOOL4_CHECK check-tool4 --stdout "$T4_STDOUT" --stderr "$T4_STDERR"
  CAND_SHA="$(jf "$LOGS/STEP_10_TOOL4_CHECK.json" candidate.sha256)"
}

# ======================================================== STEP 11 (B7b): exclusive SEAL_RECORD; its sha equals tool 4's stderr sha
step11_seal_record() {
  STEP=11; echo "STEP 11 exclusive-create the SEAL_RECORD (0561 1.1; A81 RI-19 V005@27b62183 L1263; README_SEAL_TOOLS L16-L22)"
  v005_still_frozen 11
  run_h STEP_11_SEAL_RECORD copy-exclusive --src "$T4_STDOUT" --src-sha "$CAND_SHA" --dst "$SEAL_RECORD"
  SR_SHA="$(sha_of "$SEAL_RECORD")"
  [ "$SR_SHA" = "$(jf "$T4_STDERR" seal_record_sha256)" ] || { echo "REFUSE: SEAL_RECORD sha differs from tool 4 stderr" >&2; false; }
  echo "  PASS  SEAL_RECORD $SR_SHA (= tool 4 stderr)"
}

# ===================================================== STEP 12 (B8): exclusive ROOT_SEAL_ADMISSION config pinning the SEAL_RECORD
step12_config() {
  STEP=12; echo "STEP 12 exclusive-create the ROOT_SEAL_ADMISSION config (0561 1.2; A81 RI-19; FORMAT_V005 L7; SEAL_CHECKLIST_R5 L31 B8; r5 srr[10])"
  v005_still_frozen 12
  run_h STEP_12_CONFIG make-config --seal "$SEAL_RECORD" --seal-sha "$SR_SHA" --build "$BUILD" --build-sha "$BUILD_SHA" --allowlist "$ALLOWLIST" \
        --allowlist-sha "$ALLOWLIST_SHA" --producer-index "$PRODUCER_INDEX" --producer-index-sha "$PRODUCER_INDEX_SHA" --guard "$GUARD" \
        --guard-sha "$GUARD_SHA" --launcher "$LAUNCHER" --launcher-sha "$LAUNCHER_SHA" --out "$CONFIG" --n-sources 15
  CFG_SHA="$(jf "$LOGS/STEP_12_CONFIG.json" config.sha256)"
  [ "$(jf "$LOGS/STEP_12_CONFIG.json" config_is_guard_CONFIG)" = "$EXPECT_CONFIG_IS_GUARD_CONFIG" ]
}

# ============================================================== STEP 13 (B9): the separate SEAL_ADMISSION_RECEIPT naming both
step13_receipt() {
  STEP=13; echo "STEP 13 exclusive-create the SEAL_ADMISSION_RECEIPT (0561 1.3; A81 RI-19; FORMAT_V005 L8; SEAL_CHECKLIST_R5 L32 B9)"
  v005_still_frozen 13
  run_h STEP_13_RECEIPT make-receipt --config "$CONFIG" --config-sha "$CFG_SHA" --seal "$SEAL_RECORD" --seal-sha "$SR_SHA" --out "$RECEIPT"
  RC_SHA="$(jf "$LOGS/STEP_13_RECEIPT.json" receipt.sha256)"
}

summary() {
  STEP=summary
  "$PY" -I -B -c 'import json,sys
k=sys.argv[2::2]; v=sys.argv[3::2]
d={"schema":"C3SA_ROOT_SEAL_ASSEMBLY_SUMMARY_V001","pins":dict(zip(k,v)),
   "root_next":["publish receipt, config and SEAL_RECORD full shas in a numbered root packet (FORMAT_V005 L8)",
                "export UNT_ROOT_ADMISSION_SHA256 from the PUBLISHED config sha, never from the local file (FORMAT_V005 L10)",
                "verify the bound plan and command shas from bytes immediately before running the command (A81 RI-25; SEAL_CHECKLIST_R5 C2)",
                "write nothing more to the open V005 file; later entries go to a V006 addendum (A82; A99.6)"]}
open(sys.argv[1],"x").write(json.dumps(d,indent=1)+"\n"); print(json.dumps(d,indent=1))' "$SUMMARY" \
    frozen_addendum "$FROZEN $FROZEN_SHA" driver_build_record "$DRIVER_BUILD_RECORD $DBR_SHA" bound_plan "$BOUND_PLAN $BP_SHA" \
    bound_command "$BOUND_COMMAND $BC_SHA" slots_final "$SLOTS_FINAL $SLOTS_SHA" sealed_prereg "$SEALED_PREREG $SP_SHA" \
    sealed_compare "$SEALED_COMPARE $SC_SHA" e_seal1_gates_only "$GATES_STDOUT $GS_SHA" \
    e_seal1_validity_only_C5H "$VALIDITY_STDOUT $VS_SHA" seal_record "$SEAL_RECORD $SR_SHA" \
    config "$CONFIG $CFG_SHA" receipt "$RECEIPT $RC_SHA"
}

step0_preflight
step1_freeze
step2_tool1
step2a_driver_build
step3_bind
step3a_fill
step4_sealed_prereg
step5_sealed_compare
step6_tool3
step7_tool2
step8_gates_only
step9_validity_c5h
step10_tool4
step11_seal_record
step12_config
step13_receipt
summary
echo "ROOT_SEAL_STEPS: ALL STEPS PASS"
