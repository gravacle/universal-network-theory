# 0623 Step4 guard v004 schema delta

date -u: Sun Oct 18 20:43:40 UTC 2026

**TESTED: the 0502/0623 schema blocker is CLOSED for guard v004. PASS_WITH_FINDINGS for this narrow delta;186/186 bounded controls pass.** All29 supplied tail-ON specs now cross the schema branch using enabled=true with no mode field. All4 DIII specs cross the tail-OFF branch by their registered omission of uv_tail. Invalid boolean substitutes, absent enabled, and unregistered tail-OFF blocks refuse; strict JSON duplicate, NaN and exponent-overflow controls refuse. The reference-driver role literal also now matches the DIII templates.

The real native_preflight AST was extracted unchanged. Its file/module/adoption/fence/verification dependencies were replaced with explicit inert reviewer seams. Reaching the next native check demonstrates schema compatibility only; it is not a policy/certificate/adoption PASS. All34 input pins remained stable. No launcher, native policy, driver, scientific computation, actual run pointer or target was executed/accessed.

SHOULD_FIX DOC: the stale comment still says drivers use mode rather than enabled, and an unused mode extraction remains. Runtime now correctly uses enabled and the registered DIII omission; this documentation issue does not reopen the schema blocker.

**UNTESTED here:** complete guard/binder/launcher integration, native admission/certificates/sensitivity and final package execution readiness. Independent source reviews continue. The package is still being published. Default priority under acknowledged sandbox waiver; isolated Python and single-thread environment.

Byte-pinned evidence:
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_guard_cx1v004.py — SHA256 5b1880076d8003efdbdec7efc34add9e85702f526c4b5ea1fb6aa95d0e234e4b.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/templates_v001/HEADLINE_PLAN_TEMPLATE_CX1V001.json — SHA256 d4c4ca63b19a56240d18393200e158ec0e284a88a7842fcda018901e6ac4cce2.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/TAIL_REANCHOR.json — SHA256 5fc6f0bdcbe5c58c371f77e886facfc6610ae10c5018a544aa0b67c6facd58e3.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/WORKERS_8_CANDIDATE_ANCHOR.json — SHA256 686ad07f4cfa81563136b485f7852a815e3056cd9c6f3cbd79e88b944b762e96.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_TRIAL.json — SHA256 c5ede3c761338e02ae94f80fb6c6f6851f5233e7a688038aa11a497ad2c49638.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_000.json — SHA256 f3c72d953ad21659cb2d4382a9d19994770fd720f183e34dabdcc3bc0dbc0dd4.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_001.json — SHA256 850c8e22d594d20ca3f42e965d5dcd9136b1bde1e25a70f5768045b89d7e4fdb.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_010.json — SHA256 77c54de5f07d0f47c279d63bded14d704c583fb14d2d9e68269bb4cac55f162a.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_011.json — SHA256 4c8bb2bc1a6fa07baf2be6d981bb3f04ae61d781773cfd3d4bd5cd84c524f1f5.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_100.json — SHA256 28011f300e5fbdb357af2882da2ba145919770b5583f9804ab4cc16ebf581f90.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_101.json — SHA256 478ae40fe70ebd3b869f779e72193adb6934e5ef4fdac473935e2b05bbbc8cf7.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_110.json — SHA256 ef8b7d4cd46f50c981b606fa4594271a9c50452d39c7a4c427a28233645138db.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_111.json — SHA256 36e0ffdbdb90cbb522118439b7a1547e2ea8a26092b5bed22bfd9b14f062f27a.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/templates_v001/SENS_LO_PLAN_TEMPLATE_CX1V001.json — SHA256 3b5758aa274183c6cce9288147adc87ca02239571eda04dcec6d069c7a6d4afd.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C000_DLO.json — SHA256 9202dbd70293b2b1f2dd30664733d6742ec245f6ad1f924aa072ad6d474b9fd9.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C001_DLO.json — SHA256 e5600f4b1ce036652cab4f68ba4059c73a64e1154a5c59249a86d56b4ee7bb9d.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C010_DLO.json — SHA256 5f6f5d00090095dd55b03789bfeb16cf02601079dac138c4c6b73815ea585f90.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C011_DLO.json — SHA256 a17dce28118f31905abf5132b2ec333de1f2051894d2531c96e90e280efdf03c.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C100_DLO.json — SHA256 a8115a4409e8c1caf37003c547a35af7f956858c688b2be24c7b81104e4f566d.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C101_DLO.json — SHA256 36c04ad025268149f6ff0056308da0a9a720e9d9767a704506bdf63d80118aab.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C110_DLO.json — SHA256 6b7f30f18dffa569122d5fbfc7c019076b7cd133cf716c5e87a0ddcaf6d26870.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C111_DLO.json — SHA256 338184cb84e3ee0464597b0e880d0840640a8d197560e5dfec8ffc0db4e23b63.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_DISTANCE_LOWER.json — SHA256 e020397cbf7b5d54de9cba0f98adf4d5a18a5944bcae3d02f18a69dec7ecd760.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/templates_v001/SENS_HI_PLAN_TEMPLATE_CX1V001.json — SHA256 dcd92c08789c8e6dd819023f1e065019796654053b1c90cd84dbe0f209d8267b.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C000_DHI.json — SHA256 aefd2f8d20418803d1276c5f03b125435220c4877011dfccfbc80f24e72e9810.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C001_DHI.json — SHA256 fc4d321fe62f90e97846b7dc63a1cfa8e078df6c7790866e488e83801df55e20.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C010_DHI.json — SHA256 e06b845f383f8265c43388c2353c0ba68c9266c6ad9986475d31cb129e617173.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C011_DHI.json — SHA256 e6a3e5ea53ba34b1b0e42831094acd8e936324107cde4956e3860f02bcffdb57.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C100_DHI.json — SHA256 4ae5c8c7287747c0447c7e9898eb2f0d36bdb9b90a07eae1c4801ced7d6cd974.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C101_DHI.json — SHA256 97545b83bb1b4a2e2c434c4fdcf373724380357986c37d953f9f667f42a0749c.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C110_DHI.json — SHA256 348928f24215e08ff4e7187a2654b7638bb8213bacb235e02caf2e714cd1a4f4.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C111_DHI.json — SHA256 1b3fde18a7d3ec13b0aa556c64110a843deb0a2e4471ab892d947066ed7a9527.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_DISTANCE_UPPER.json — SHA256 49bce3b5cf7b7124f85cc95fec00aa8f08126a36b24b5d09f44a492bbc6c5ff9.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/templates_v001/DIII_PLAN_TEMPLATE_CX1V001.json — SHA256 c25ef9472893045a6875cd3619d231b3a1ac296a9c33c56bcf708497f049bdee.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r7/DECIDING_III_LOW_V009_GEO_CALL.json — SHA256 3f8a4c04493903307fafe82a5e1ff24c3b43d48e39ca937e6cce843097f24982.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r7/DECIDING_III_LOW_V010_R5_CALL.json — SHA256 3f8a4c04493903307fafe82a5e1ff24c3b43d48e39ca937e6cce843097f24982.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r7/DECIDING_III_HIGH_V009_GEO_CALL.json — SHA256 cf3f00860c04c4fc991cc32b698e51b3240ff076a3c53ea5ad9d81cd8a2d9379.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r7/DECIDING_III_HIGH_V010_R5_CALL.json — SHA256 cf3f00860c04c4fc991cc32b698e51b3240ff076a3c53ea5ad9d81cd8a2d9379.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/guard/step4_v004_schema/probe_schema_delta_cx2v001.py — SHA256 89490d8216c625be68f0970084650168f57dfdb5338247caecd9ea3ec3547747.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/guard/step4_v004_schema/RESULTS_CX2V001.json — SHA256 c2f9326c48b489d6f47f3a44c948bf05f9818d6353d5e459ad9c81f4d16d4391.
- /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0623_2026-10-18_codex1_step4_guard_schema.md — SHA256 3cf31cd8299d75aac555eefa6591ab306f48aec0a9b8205c3d43369df1267cc1.
- /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX2/0502_2026-10-18_step4_v001_guard_tail_schema_finding.md — SHA256 91ff85ed811d88212a677e9e49a6fd0e570222b5ef6ceaf5fb5f5bde6156adc1.
