# Independent A99 V6-S2/S3 documentation and plan review

Sun Oct 18 20:40:32 UTC 2026

Decision: PASS_WITH_DOCUMENTATION_NOTE. No blocking or should-fix finding in the assigned static documentation/metadata scope. 136/136 independently constructed assertions pass; zero audit denials; observed RSS 23,429,120 bytes. No producer, binder, launcher, comparator, or scientific module was imported or executed.

TESTED: The selected plan differs from V010 at exactly 51 string leaves and 31 distinct output locations: one launcher log and five references per case (outdir, receipt, monitor log, argv outdir, argv receipt). All changed locations are lexically under the proposed internal root, have fresh V011_CX3V001 names, and no plan field retains External1. Every other parsed plan value is identical, including the r5 driver, scientific input pins, order, timings, wall/RSS/output caps, runtime workers, memory gate, six active route-A cap, 60-second poll and predecessor-iteration ramp. All ten filled-spec byte hashes match. No forecast or parallel/cache saving is introduced.

The case manifest changes exactly ten references, each equal to the corresponding plan outdir. Its legacy C5H reference is an unchanged opaque string. It was never converted to a filesystem path, resolved, statted, opened, or passed to a guard. The only remaining External1 reference in the case template is that preserved legacy string. The command changes only the selected plan basename and remains explicitly PENDING/root-only. No output-root metadata or contents were accessed by this review.

The selected allowlist and producer index contain exactly the same ordered 15 path/SHA pairs. First 13 pairs are unchanged; the two S1 successors replace their predecessors. Every allowlisted source hash was recomputed from bytes. MT/I1T/FLAG_RULINGS map to the selected postseal writer, SRB_ROT maps to the selected SRB writer, and SR_K mapping is unchanged. The producers remain in the shared guard/config directory; the guard bytes/config expression and SRB relative reconstruction path are unchanged. Final BUILD_V007 consistency remains the parent's packaging check; this review creates no BUILD, root config, seal, receipt or admission.

The RUNBOOK and seal format correctly carry A85.2–4: normal-QoS T-run process tree, non-critical lane work under background QoS from step 2, internal outputs before plan binding, and caffeinate tied to the long-lived launcher for all of step 2. The A95 sandbox waiver is distinguished from root's operational launch obligations. A96 r5 selection, single-thread production policy, receipt/config trust and exact 15-source registration remain explicit. The cited root snapshot was byte-verified; no equality to later mutable addendum bytes is assumed.

UNTESTED: physical SSD/hardware identity, available disk space or symlink state at launch; root must perform those stated operational checks. No template was bound and no launch authorization was created. Production behavior is untested. The RUNBOOK's admission21/21, launch-control28/28, output/aggregate56/56, binding7/7 and preseal11/11 counts are inherited evidence, not re-executed in these 136 checks.

Documentation note (non-blocking): inherited introductory wording still attributes earlier no-launch work to Codex1. It does not describe this Codex3 review, which performed only the static checks above. No source or documentation edit is requested for this precision note.

All cited metadata, source inputs and review evidence, byte-derived SHA256:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/LAUNCH_PLAN_V010.json` — `26f1ebf90d95d2674d4bcba7ac3416049cdba171c5754c32440b4c66480c8021`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/LAUNCH_PLAN_V011_CX3V001.json` — `1b406591784ab4647e4aaf2686d9b3d18a259fadb435391439d2ff75df22ad3c`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T-KHI_P128_MS128_R5_CX1V004.FILLED.json` — `ce3bee66a3721293e2f70b8403aa02edba1d311bf06aec050e61637854ff7a04`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C6T_P128_MS128_R5_CX1V004.FILLED.json` — `e4016037423b6302cbe4cd3993dc484ee430c770e6711c48caf867f532c9ade9`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T-D5_P128_MS128_R5_CX1V004.FILLED.json` — `51551ee7cac54600663c3ea291e99552ac8f1417ad903460c6ce2b0c57b60eef`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T_P128_MS128_R5_CX1V004.FILLED.json` — `de6d7d77d053d9c983f15eca11468fe8520d025ff2ad1f643b2a517a915b1738`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/S4T_P128_MS128_R5_CX1V004.FILLED.json` — `8e71be9bee2887f9454b0efeb83fbc50e4c6e6bec1ed5513786be29bd2fa41ee`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T-A_P128_MS128_R5_CX1V004.FILLED.json` — `96c73b1e478ee7d56f4a91d91fa2e0db6ec955f1edc4bb9a843571638855fc97`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C3T_P128_MS128_R5_CX1V004.FILLED.json` — `212f4b3673903ef28f0cca23474a3f08970b0309e347b473bae8a96d85264854`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C2T_P128_MS128_R5_CX1V004.FILLED.json` — `84933cad8fa19bd9d8e95893e19ce744f8d19d3b44c937eb9ddf599c5c333bf2`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T-KLO_P128_MS128_R5_CX1V004.FILLED.json` — `3001aa3a5e34fe42c63c9ad05ffd845096a891bed70e486cac88eba96e80b206`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T-C5c_P128_MS128_R5_CX1V004.FILLED.json` — `0d60cd7b6a2fa8ec5f386cf4addb412a0772fdd1a33fb045dd6c71fb0ed45fcf`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/CASES_MANIFEST_TEMPLATE_V010.json` — `ec884ff7d9797044422ce2752ef3d94d7062b63e3f1c02502a80d56686e5e1ce`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/CASES_MANIFEST_TEMPLATE_V011_CX3V001.json` — `df4cad82f947edf85741ce97d5902c9b926daa1401448c5daac4ad461a2b1726`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/LAUNCH_COMMAND_V010.txt` — `7d649ac5e0fe6a17625e7c773e1ed500101367ea8b99d578c2da8f716e1809c4`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/LAUNCH_COMMAND_V011_CX3V001.txt` — `956b933b2b54f031dfc07253240f15b8c9a7a9d63b8bfc8aeb6a86fab31d8503`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/ALLOWLIST_DRAFT_V005.txt` — `23af0a4000374627fdaab622cd82bd49fef49fc66edd097cfebe29ef2961ab39`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/ALLOWLIST_DRAFT_V006_CX3V001.txt` — `18300b52fdef500defacae06e4b98564534cd37661874ae7e2aa92d5c9f5fc47`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/PRODUCER_INDEX_V008.json` — `88289906978ce6513a85bfc8b838d8a5f05e81aebe100b10689335aa425921d4`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/PRODUCER_INDEX_V009_CX3V001.json` — `7a61747efeee8ff27e8e5b3c2213a0aa2f3e8ed888e871ac1df193a6a64b6a97`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/ea_replay_cx1v012.py` — `380e2d81027eba4c86843b904ccb79f5f27e6c917b5f3f5a71f286c01be32156`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/sr_k_static_cx1v009.py` — `cc2eb3bb41059679f67ed550583c035ae17a8ccd2dfc8a36a3f6cb131fe1524e`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/shell_split_static_cx1v010.py` — `cafcb128627cb465dc38437ba4a764497437c8f4436977da1e30cc4d426d63a7`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/dm4_report_cx1v008.py` — `e969c8908894175c4f6ed1549e5aaaeb6f9aa95cef10052833a0f2941ebe3e77`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/ra10_checkpoint_cx1v012.py` — `b66dd9c083dda5bd4218baf12583c842ce8548ecbeb11df5ada4d953cbfa8b98`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/t2i_record_cx1v009.py` — `562cbf78f246bd5dccd8cc0b0f78e28253b468b3ef0cde4398d991df2bc11564`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/t2i_replica_admitted_cx1v005.py` — `cb03359168cfe397dda75a54f121520c02cc76ba5c9b34c606899d8a61658b4f`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/aggregate_records_cx1v008.py` — `9794123d20d6617428a7e6445af5a831885946f0178e9a58edee5801ba01b28f`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/route_a_tail_replay_cx1v005.py` — `9e49aad93ed85f1ade6f620836fa2ab14d38010633b4a6bf0ed9a03de7691465`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/producer_runtime_cx1v004.py` — `b64098691d22fb1d3c7a296c500c126e362dc0ffb2d5f0cb29dd39836c63234f`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/shell_filter_cx1v004.py` — `4fcbd495fe41e881637aa64eef342c8adf1193b54e9b7e80b7261f9217b5dabb`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/producer_guard_cx1v008.py` — `294cb7760679b883a62fb3117dc75e91231b2f173bcec65983e6762371ea0731`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/route_a_token_launcher_cx1v007.py` — `861bba68dd7d207beb30ed828c1557955f31979cf2e15369acccc52ea595953d`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/postseal_records_cx1v006_cx3v001.py` — `4024d82a8ec59ba339f00214066798ea905d1234466d29db2e8bb5e5869de366`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/srb_rot_record_cx1v008_cx3v001.py` — `2757847a0a2c6da7ab83dc5b203cbfd8c2291da57e430d4ce0cff99ceb4628cc`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/RUNBOOK_V008_CX3V001.md` — `0c9368bdb3f2a03c7ff345787154fef84568aa25700d6583f4287aada8957b79`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/ROOT_SEAL_ADMISSION_FORMAT_V005_CX3V001.md` — `75f814e0c338d1636ad0af0c3dd7c3247ff682eef2545bf9e070cad6fe4849cd`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/RUNBOOK_V007.md` — `648cfd748eb65bf08e9e79e9a27b5fb30c575128fdfd6556b71ae9e2c9e390cf`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/ROOT_SEAL_ADMISSION_FORMAT_V004.md` — `6908ee88e903443487280bfde6d4e91d6d4a53b621aee543eba8948cfcda1fb1`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/build_v007_closure_cx3/docs_plans/ROOT_DECISIONS_V005_READ_SNAPSHOT_CX3V001.md` — `7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/build_v007_closure_cx3/docs_plans/ROOT_DECISIONS_SNAPSHOT_CUSTODY_CX3V001.json` — `663a1b87fdc666c837b0dabb24a04244b057ddaadcdda8e12bfea2788813274f`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/build_v007_closure_cx3/docs_plans/FILESYSTEM_EVIDENCE_CX3V001.json` — `d066c08476154164662e38bd0fa39cc669139c623b83c179084aa64e5b952a42`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0613_2026-10-18_all_lanes_taskpolicy_preferred_not_required.md` — `82c214dfe8729603ccea43f803cc091f5b484f4b2fa09147ea57955a1a0f1377`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0621_2026-10-18_claude4_codex1_codex3_claude3_A99.md` — `7ab78e6a0aa4c3d11d6c4dd9887ea2fc8b65e40a84bc75de387a319534b99504`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/build_v007_closure_cx3/independent_docs/review_docs_cx3v001.py` — `f25c471f7a347e955582b8e3830dd38f9a76e0befe6c499e7390fc32743981c2`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/build_v007_closure_cx3/independent_docs/RESULTS_CX3V001.json` — `ac15eaf5b4bb9a8a424906cab592b3cab487a806af7cbd0251f61ec4b22f80e6`.
