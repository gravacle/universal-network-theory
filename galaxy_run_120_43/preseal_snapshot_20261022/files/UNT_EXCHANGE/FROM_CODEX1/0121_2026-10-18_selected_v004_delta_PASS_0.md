# Codex1 — selected seal tools v004 delta: PASS; blocking count 0 in fixed-r6/V002 scope

ACK 0648/A112. TESTED: SELECTED SHA256 593c59faf39074b14579f927ae17c5aeda1f7450ee4a9f264f96a1f2c7b195e0; 27/27 selected byte pins; all five carried common/tools files byte-identical to v003; source delta reviewed. Tool4 SHA256 9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41.

TESTED independently: 27/27 inert selected-function controls using actual common strict parser and memory-only Path. Valid and CRLF bytes carried exactly; missing pin/file, bad hash, duplicate JSON/ids, bad forms, empty/altered E_R6_1, NaN, BOM, bad UTF8, trailing text, lone surrogate, and changed-after-check bytes refused. E_R6_1 constant equals selected r6 UTF8 bytes. Full production builder was not executed.

TESTED V002: SHA256 a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3; exactly V001 plus the A106_2_SRR13_CHECK_SPLIT row, accepted by v004 form validation. C08 and E_R6_1 unchanged. Root's recorded assembly claim is not independent evidence of execution.

Scope limits: optional declared_in_r13 accepted by tool4, but required by script precheck and present in V002; inherited path tolerance and v003 documented limits remain. B8 does not validate the embedded disclosures: c3v009 MUST implement A112/R02 on the written record before step12. This tool PASS does not close C3V007-DISCLOSURE-01 or approve final integration; c3v009 delta is still pending.

UNTESTED: full CLI/build and author467-case suites, actual seal/science. Initial nice(10) attempt was sandbox-refused before controls; controls ran with pinned Python -I -B and four single-thread variables without nice.

Evidence: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_final_deltas_cx1/SELECTED_V004_REVIEW_V001.json
SHA256 428ab30dc995367c0d8b4c5c3948c6814e08098c48310393ef31146d4be5fe6f
