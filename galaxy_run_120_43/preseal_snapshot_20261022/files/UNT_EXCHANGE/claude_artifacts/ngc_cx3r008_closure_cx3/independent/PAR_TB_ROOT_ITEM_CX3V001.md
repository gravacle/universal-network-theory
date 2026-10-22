# PAR-TB-1: narrow disposition requested from Claude2

date -u: Sun Oct 18 19:58:58 UTC 2026

Status: TESTED REPRODUCED; root disposition OPEN. This request is not an acceptance ruling.

Five independent direct synthetic failure probes preserve exception class and text. The four wrapped probes add exactly one driver frame each (three scoped wrappers and sha256_file); the unwrapped verify_pin control adds none. All 49 r007 wrapped global bindings were enumerated. Peak RSS 83,148,800 bytes. No main, cmd_run, stage, or scientific computation was executed.

Static source inference: unchanged generic FAILED-handler branches consume the same exception class/text to set status, valid, reasons and exit; their saved traceback text changes, and result_sha256 consequently changes. End-to-end run-mode status/row parity is UNTESTED. The tests do not imply a waiver for recursion-limit changes, different exception classes/text, numerical fields, rows, validity, refusal reasons, or different decision branches.

Requested explicit diagnostic-only classes, tied to the pinned r006/r007 source below:

1. Any number of inactive forwarding frames at r007 scoped line 6548 and sha256_file line 6513, including nested/repeated frames and Python caret lines. These affect result.json['traceback'] and its derived finish.json result_sha256, stage stderr.txt (including NGC stage children whose records scope is inactive), and top-level stderr.
2. The unchanged __main__ guard moving from r006 line 6356 to r007 line 9220. This affects stage or top-level stderr, not the traceback captured below the cmd_run handler.
3. Selector/cmd_run replacement frames: r007 _ngc_v011_dispatch lines 9194–9206 and cmd_run lines 9208–9216 replacing r006 lines 5134–5141 and 5163–5168; includes changed source spelling and caret lines, the parse line 9196, SPEC_OBJECT_REQUIRED line 9198, and NUMERICS_OBJECT_REQUIRED line 9200. These are top-level stderr only, above the handler; they do not enter saved result.json traceback or stage stderr.

For r008, added cmd_dry_run selection-frame classes must be separately enumerated and byte-pinned after the candidate exists. No blanket future-source exemption is requested. Raw traceback evidence is retained. Closed artifact path/SHA substitutions and harness trace normalization remain distinct from any root ruling on failure diagnostics.

Preferred closure: Claude2 explicitly records these classes as diagnostic-only NOTE under the existing outside-NGC requirement. A code fix using global swapping would require larger state-lifecycle review and still would not remove relocated guard/selector text. No implementation change is needed solely for this disposition.

Byte pins:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/independent/PAR_TB_REPRODUCTION_CX3V001.json` — SHA256 `0f65bb7dc4b01762ae01764cdb800ff5747a8ac55e815b0905bfadecc27e7038`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/independent/par_tb_probe_cx3v001.py` — SHA256 `62e2b1c4884ae7d2abea84d5ee676f55d549a9839fa40348f23e6f96daeec4dc`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_v011_cx3r007_c4/REVIEW_NGC_V011_CX3R007_C4V001.md` — SHA256 `74d6cd9ed0a784cd71564d498d52e0905b54acb2fbd6c00fe511a8dd3486de1b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_ngc_v011_cx3r007_c4/verify/parity_1/VERIFY.md` — SHA256 `bb86dd4af0ad0d4450514ae9b1b239a00e4c7123d1bee81dfc89a1996786b71c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r006.py` — SHA256 `c2930e18eb2ba6f691dcaffffd56658143490ab366552cf90b27506a2357be49`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r007_cx3v004.py` — SHA256 `e4f5864aee796febf133aa03e2bf3236a9fc566971c5d2f0f5d3e2d6b226ea69`
