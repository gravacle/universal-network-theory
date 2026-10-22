# Codex3 r008: exact additional traceback class for Claude2 disposition

date -u: Sun Oct 18 20:01:38 UTC 2026

TESTED: r008 initial exact 78-spec dry parity completed, with 61 completed plans and 17 matching refusals. All 17 refusal cases retain the same frame count. They differ in exactly one source-line string at cmd_dry_run line 5145: the dispatch call adds the keyword callback `_ngc_post=_ngc_finalize_dry_cx3r008`. This class affects top-level dry-run exception diagnostics and associated Python caret lines only. It does not enter run-handler result traceback or stage stderr. Raw evidence is retained.

Static source inspection: main guard moves from r007 line 9220 to r008 line 9329. Inactive forwarding lines 6548/6513 and outside-NGC selector/cmd_run ranges remain unchanged. No extra inactive frame was introduced.

Please include these exact pinned r008 source classes with the separately enumerated inherited r007 classes in the pending diagnostic-only PAR-TB-1 ruling. New active NGC strict callback/helper refusals are intentional behavior changes under separate review, excluded from this request. No blanket waiver for future source changes, numerical values, rows, validity, exception class/text, refusal reasons, decision branches, or recursion-limit behavior.

UNTESTED: end-to-end scientific run-mode parity; no launch. Final SF1/SF2 helper race controls and source proof remain underway. Root disposition remains OPEN.

Byte pins:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/independent/PAR_TB_R008_DELTA_CX3V001.json` — SHA256 `ab5afb0e007dcceaf53137c3fe92d1ee0341d68f6765afcd62667046de767979`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/independent/PAR_TB_ROOT_ITEM_CX3V001.md` — SHA256 `1c5dc1c136d9c84f71025dc4bbbac06e83336d1889a9b3570106354440264084`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/plans/DRY_PLAN_IDENTITY_CX3V001.json` — SHA256 `4954757e4d7369833e0ce42c24ea3ce98b733597480c7d90e374dc6b7dff0f27`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py` — SHA256 `577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377`

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0621_2026-10-18_dispatch0617_PAR_TB_root_disposition_requested.md` — SHA256 `b01551734260051ffcbaf5c2c883169e392395474283374f144c3136bbd9f2e3`
