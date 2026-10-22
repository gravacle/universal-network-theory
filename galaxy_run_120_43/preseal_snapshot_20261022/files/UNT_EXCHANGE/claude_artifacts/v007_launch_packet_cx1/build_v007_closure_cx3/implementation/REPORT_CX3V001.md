# V6-S1 immutable producer closure

Sun Oct 18 20:38:17 UTC 2026

Decision: TESTED_PASS within the bounded parser/publication scope. The two selected source successors are listed with byte hashes below. No existing source, shared guard, root admission/seal, BUILD, index, or allowlist was modified. Parent owns the remaining V007 packaging and adoption.

The postseal JSON reader now applies a finite float parser in addition to existing constant/duplicate-key rejection. Positive and negative exponent overflow refuses even in unknown nested metadata. Normal integers, floats, signed zero, underflow, strings and container values retain existing decoding.

Both actual main functions now finish root stamping and full JSON serialization before the final output-path guard and a single exclusive open/write. Existing indent=1, Unicode/default encoding behavior, and no-final-newline semantics are preserved. SRB imports the selected postseal successor; relative guard/config/reconstruction paths are unchanged. Exact reverse-patch byte checks and all untouched function AST checks passed. Numerical arithmetic, gate logic and admission code are unchanged.

TESTED: focused suite 92/92; exact old/new parser and publication-statement reproductions 14/14. The latter explicitly reproduces the old parser accepting overflow and both old writers creating empty or partial output on stamp/serialization exceptions; selected successors refuse before output creation. These are expected old defects, not passing readiness claims for the old producers.

The focused suite executes actual selected MT, I1T, FLAG_RULINGS and SRB main functions on exclusive synthetic fixtures. Comparator admission/gates, SRB reconstruction and library arithmetic are explicitly stubbed; source record validation, parser, archive/row/envelope checks and publication statements execute. Fixture structure adapts the two earlier CLI harnesses cited below. Clean I1T fixture exports all 30 expected synthetic build records. Every mode covers positive/negative nested overflow, clean exact serialization bytes, one write, stamp failure, serialization Inf/NaN/object/cycle failure, and exclusive refusal preserving existing bytes. Source imports without any root config yield actual shared-guard ROOT_SEAL_ADMISSION_PENDING. In-memory synthetic admission is then used, with shared guard REGISTERED=() to prevent any protected registered-run metadata probe. Admission withdrawal still refuses. No root config or seal file is created.

Focused audit: zero denials, single-thread environment, observed peak RSS 40,796,160 bytes. Reproduction observed RSS 25,362,432 bytes. No scientific launches, production numerical reconstruction, protected run or NGC target reads, network, or existing-file writes occurred. All synthetic outputs and original failure evidence remain immutable.

UNTESTED: real production export, actual sealed admission, eventual compare gate acceptance, and scientific reconstruction. Serializing before opening prevents stamp/serialization failures from creating a file; it does not provide atomic complete-or-absent publication against an OS write failure. No claim of launch readiness or final V007 closure is made.

Byte-derived cited inputs, sources and evidence:

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0621_2026-10-18_claude4_codex1_codex3_claude3_A99.md` — SHA256 `7ab78e6a0aa4c3d11d6c4dd9887ea2fc8b65e40a84bc75de387a319534b99504`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_launch_packet_v006_c4/REVIEW_LAUNCH_PACKET_V006_C4V001.md` — SHA256 `d0d1c6e7d4ea73829ff5deeccab2873b41c633dc952c351dd28121b62efe15d8`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/postseal_records_cx1v006.py` — SHA256 `9fbdb0ca24153436b7c807778f140b7998fc0c0b5d18f4372d65a20a0e11cc59`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/srb_rot_record_cx1v008.py` — SHA256 `500f8b6a27cff6157246cdaca1373ad7340003263578331d30cbdf7cebc0e4f4`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/producer_guard_cx1v008.py` — SHA256 `294cb7760679b883a62fb3117dc75e91231b2f173bcec65983e6762371ea0731`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/test_postseal_cli_0599_cx1v003.py` — SHA256 `1a7949825947e1fd709a8a7324c5afe6cb98c39c6aed92d698e3e4a7c727c9aa`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/test_srb_cli_0599_cx1v003.py` — SHA256 `eefa83e39a12d0c7ab9b2bd4c6030e7ec6f3b80f58882a967d2449e21c9d063f`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/postseal_records_cx1v006_cx3v001.py` — SHA256 `4024d82a8ec59ba339f00214066798ea905d1234466d29db2e8bb5e5869de366`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/srb_rot_record_cx1v008_cx3v001.py` — SHA256 `2757847a0a2c6da7ab83dc5b203cbfd8c2291da57e430d4ce0cff99ceb4628cc`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/build_v007_closure_cx3/implementation/test_v6_s1_cx3v001.py` — SHA256 `21d2c5ad5779056a05a991a89d96175c92f5297530dac38e7363b590c8746816`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/build_v007_closure_cx3/implementation/reproduce_v6_s1_cx3v001.py` — SHA256 `47eac15d39d1fecd250b63a2485bdb67d835f639f5d13e64b9fc707399e76b2c`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/build_v007_closure_cx3/implementation/run_v001/RESULTS_CX3V001.json` — SHA256 `fff389a389522868512b8eb6f1a29582857dcecc0e0c49d98339fb171eae2330`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/build_v007_closure_cx3/implementation/repro_v001/RESULTS_CX3V001.json` — SHA256 `4eaec5aa66809d066daf50cd02d217db7827d5a0387a434d08c1b3d2fbe15b37`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/build_v007_closure_cx3/implementation/SELECTION_CX3V001.json` — SHA256 `d75c15f787b62f4807de41e12de8f7bdbf54df0b96926cc7b0571ac40ad1a903`.
