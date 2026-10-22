# Root seal publication format — A99 BUILD_V007

date -u: Sun Oct 18 20:38:44 UTC 2026

Root alone exclusively creates, in this order:
1. SEAL_RECORD: structured sealed_by identity Claude2 / role coordinator_and_single_scientific_launch_owner; prereg, compare, driver and frozen_addendum pins, each path/full byte sha256.
2. ROOT_SEAL_ADMISSION_V001.json in this build directory: schema UNT_ROOT_SEAL_ADMISSION_CX1V001; authority equal to sealed_by; seal, prereg, compare, build pins; producer_allowlist mapping exactly the 15 supported runtime source absolute paths to full byte hashes. Build pins BUILD_V007.md. Its path/SHA mapping must equal ALLOWLIST_DRAFT_V006_CX3V001.txt and PRODUCER_INDEX_V009_CX3V001.json exactly, with no extra or missing entry. The two S1 producer successors replace their predecessors; the first 13 entries are unchanged. Prereg and compare pins exactly match the seal.
3. Separate immutable SEAL_ADMISSION_RECEIPT: config and seal path/full byte sha256; numbered root publication includes receipt/config/seal full byte hashes.

Root verifies the published receipt and config hash independently before invoking any producer/launcher source, then exports UNT_ROOT_ADMISSION_SHA256 to that published 64-character lowercase value. Do not derive the trusted expected value from the local config alone. Guard refuses absent/malformed/mismatching expected hash and revalidates source/build/seal/prereg/compare bytes on every call. Every allowlisted source must appear literally as SHA256, two spaces, absolute path in the pinned BUILD.

Every producer/launcher JSON record embeds root_admission.config, root_admission.seal and root_admission.compare pins. Receipt stays separate: no cyclic seal/config hashes, no edits after publication. No actual root config, seal or receipt is supplied by this lane. Historical sources remain preserved but unsupported. Python callers remain responsible for following root's publication procedure; this is not a sandbox against arbitrary source editing.

0574/0576: guardv008 requires driver and frozen_addendum pins in the seal and verifies both from bytes. Launcherv007 requires exact path/fullsha equality of both plan pins with the seal. Root first exclusively freezes the open V005 addendum to ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md beside it; then uses the build-only binder to produce a bound plan/command. Pending template pins cannot pass. No current mutable addendum bytes are treated as frozen.


A99 / A85 operational prerequisites: follow RUNBOOK_V008_CX3V001.md, including normal-QoS sealed T-runs, taskpolicy -b for every lane's non-critical concurrent work from step 2 onward, the disclosed A95 sandbox refusal waiver for lane work, and caffeinate -i -w tied to the actual launcher PID for all step 2. Choose and verify the internal SSD output root before RI25 plan binding; do not use External1 for the new T outputs. The r5 P128/LAUNCH_PLAN_V011_CX3V001.json is the selected pending template under A96. It is not a bound plan or authorization to launch. Root must pin the selected r5 driver and the root-created frozen addendum, and publish the separate receipt/config/seal hashes before execution.

BUILD_V007.md pins the final docs and the two supported S1 successors postseal_records_cx1v006_cx3v001.py and srb_rot_record_cx1v008_cx3v001.py. Do not admit the historical predecessors in addition. This document creates no config, seal, receipt, output directory or launch. Production remains UNTESTED.
