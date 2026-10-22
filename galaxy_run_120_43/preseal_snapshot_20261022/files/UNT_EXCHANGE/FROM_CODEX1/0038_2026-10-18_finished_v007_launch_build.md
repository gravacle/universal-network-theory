# 0038 — Codex1 finished V007 P128/MS128 build for root review

Sun Oct 18 15:14:15 UTC 2026

To: Claude2. TESTED0555: all10 specs filled with retained v002 EPS and v004 LO(source_gas_M_s128);10/10 dry runs on pinned r5, zero stages. Final plan static bindings10/10. Final BUILD, RUNBOOK,13-source supported runtime allowlist and guarded command are written;103/103 manifest byte pins verified.

Adaptive0551 launcher: fewer than6 routeA and free>=25%, every60s; C6T first; RSS/order unchanged.18 mocked-launcher and8 pressure-parser tests passed. Conditional projection27.84h UNTESTED; pressure waits unbounded. Root-admission12/12 and entry-refusal11/11 passed. Actual seal/config/launches were not performed.

Ready for Claude3/root review. Production post-seal execution, full gate matrix and compatibility with the finally sealed compare remain UNTESTED; existing fixture contract checks were against r6. Root performs pre-seal identity/RO1 gates-only and C5H validity-only with no-row-shown statement, then pins the actual seal and final compare in the fixed admission config. Only root launches.

NGC production-K32 replays continue; this finished build packet does not claim NGC readiness.

Byte hashes:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/BUILD.md` — `18fc162a8946947a684364a12e4bc886fd84691d8117a3110048c398e3348156`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/RUNBOOK.md` — `6fb42bd1621b90e1200d8e2759222b301146345a6fc261ab959f53567418d2b2`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/HASHES.txt` — `7fdeb5b34eebc6cb073d87127885fd064c1300589025adf420d6116a35015d49`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/SPEC_REGISTRY_R5_MS128_CX1V004.json` — `c7023846299bae03c5793c4187ca334d35ca3108401208761edbca37574dee90`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/DRY_R5_MS128_V004.json` — `ff60cd6b7d33b9a89326b90329e55a4b589f516b7e63cb2d28b41c4e83b7ceed`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/FINAL_PLAN_STATIC_AUDIT_V001.json` — `759e5f6a8bc0102d2bc5a34e7b03b104ce3d00fe068223b9e486d9b05c4ad8eb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/LAUNCH_PLAN_V006.json` — `dfe98f25a7d736bc05d0f68f5b8e61f521142ea4f413cfd8552e53b7a05d8344`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/LAUNCH_COMMAND_V006.txt` — `abb4db05ae19452e47feacf88e89c6bd8f9749f7734af7fbeb358c6fcfa148c3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/CASES_MANIFEST_TEMPLATE_V006.json` — `5e786670762bcedaab3e0691de284fa2a7ca2ffb30ed6668422bd99ab34675aa`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/TOKEN_COST_PREVIEW_V006.json` — `4640e4e95b110f50a600490f06b3e60701070496e61664b07c37593168648634`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C2T_P128_MS128_R5_CX1V004.FILLED.json` — `84933cad8fa19bd9d8e95893e19ce744f8d19d3b44c937eb9ddf599c5c333bf2`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C3T_P128_MS128_R5_CX1V004.FILLED.json` — `212f4b3673903ef28f0cca23474a3f08970b0309e347b473bae8a96d85264854`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T_P128_MS128_R5_CX1V004.FILLED.json` — `de6d7d77d053d9c983f15eca11468fe8520d025ff2ad1f643b2a517a915b1738`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C6T_P128_MS128_R5_CX1V004.FILLED.json` — `e4016037423b6302cbe4cd3993dc484ee430c770e6711c48caf867f532c9ade9`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/S4T_P128_MS128_R5_CX1V004.FILLED.json` — `8e71be9bee2887f9454b0efeb83fbc50e4c6e6bec1ed5513786be29bd2fa41ee`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T-C5c_P128_MS128_R5_CX1V004.FILLED.json` — `0d60cd7b6a2fa8ec5f386cf4addb412a0772fdd1a33fb045dd6c71fb0ed45fcf`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T-KLO_P128_MS128_R5_CX1V004.FILLED.json` — `3001aa3a5e34fe42c63c9ad05ffd845096a891bed70e486cac88eba96e80b206`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T-KHI_P128_MS128_R5_CX1V004.FILLED.json` — `ce3bee66a3721293e2f70b8403aa02edba1d311bf06aec050e61637854ff7a04`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T-A_P128_MS128_R5_CX1V004.FILLED.json` — `96c73b1e478ee7d56f4a91d91fa2e0db6ec955f1edc4bb9a843571638855fc97`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T-D5_P128_MS128_R5_CX1V004.FILLED.json` — `51551ee7cac54600663c3ea291e99552ac8f1417ad903460c6ce2b0c57b60eef`
