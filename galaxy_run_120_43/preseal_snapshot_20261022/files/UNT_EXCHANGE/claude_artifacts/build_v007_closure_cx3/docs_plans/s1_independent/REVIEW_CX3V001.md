# Independent bounded V6-S1 review

Date -u: Sun Oct 18 20:41:47 UTC 2026

TESTED_PASS: 37/37 independently executed parser/publication-slice checks and 6/6 exact AST delta checks. No observed finding in this bounded scope. This review did not reuse the author's assertions or execute full producer main functions, numerical reconstruction, comparator gates or real admission. Shared guard bytes remain unchanged. Scientific production remains UNTESTED.

The exact candidate parser AST was executed with only entry decorators omitted. It refuses positive/negative and nested 1e309 overflow, NaN, Infinity, -Infinity and duplicate keys; finite examples, underflow and null-containing structures preserve ordinary json.loads values. The exact last three statements of each candidate main were separately executed against an explicit traceable synthetic guard. Nonfinite and nonserializable payloads refuse before path guard or file creation; finite records produce the specified no-newline indented bytes. Existing-output exclusivity and final synthetic guard refusal preserve the output filesystem.

Static AST equality proves the postseal module changes only the loads function and final publication statements; SRB changes only the producer import and publication statements. The original main bodies and path guard are otherwise identical. The parser keeps existing duplicate and parse_constant checks and adds only a finite parse_float hook. Publication changes json.dump(..., f, indent=1, allow_nan=False) into a complete json.dumps using identical payload/options, followed by the unchanged guard and one exclusive open/write. Semantics outside executed slices are source inference, not independently exercised full production behavior.

The first inline AST audit contained an incorrect harness assumption that the old writer used f.write(json.dumps(...)); it stopped at an assertion before audit artifact writes. The actual old writer uses json.dump(...,f). The immutable successor audit checks that exact transition and passes; no producer code changed. This harness-only failure is preserved as metadata in SOURCE_DELTA_CX3V002.json.

The serialization-first guarantee applies to JSON/finite serialization failures. A later filesystem I/O failure after exclusive creation can still leave a partial file; no atomic-publication or cleanup guarantee is claimed. No actual seal/config, protected run, observed target or scientific stage was read or created. Test files are synthetic and new. Process 24870912 was 24870912 bytes; this is observed usage, not a hard address-space cap.

## Byte pins

- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/postseal_records_cx1v006_cx3v001.py — SHA256 `4024d82a8ec59ba339f00214066798ea905d1234466d29db2e8bb5e5869de366`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/srb_rot_record_cx1v008_cx3v001.py — SHA256 `2757847a0a2c6da7ab83dc5b203cbfd8c2291da57e430d4ce0cff99ceb4628cc`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/build_v007_closure_cx3/docs_plans/s1_independent/RESULTS_CX3V001.json — SHA256 `3d2ad95af856946c1ef30771b005cbc4a27fc8f888bf2ac99828630a39b9c7f3`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/build_v007_closure_cx3/docs_plans/s1_independent/SOURCE_DELTA_CX3V002.json — SHA256 `746d24e2b0b39441c228a4c898233cbe8804fe1180cc4ee13b028477673663c8`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/build_v007_closure_cx3/docs_plans/s1_independent/postseal_records_cx1v006_cx3v001.py.diff.txt — SHA256 `288fefd3e753d4db269a5bc9fe63bbf59ee4df2b675aae721bf6dc6b418435fd`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/build_v007_closure_cx3/docs_plans/s1_independent/postseal_records_cx1v006_cx3v001_positive.json — SHA256 `5d30aeb4867b27c81c0eabaf656eb7c899cfee81cf19f90fa57bd3fc27ef0801`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/build_v007_closure_cx3/docs_plans/s1_independent/srb_rot_record_cx1v008_cx3v001.py.diff.txt — SHA256 `2b88ffce0a1006edde0fee2b3b46d6691eeb141c01b1e636c25ebe6cb480029f`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/build_v007_closure_cx3/docs_plans/s1_independent/srb_rot_record_cx1v008_cx3v001_positive.json — SHA256 `5d30aeb4867b27c81c0eabaf656eb7c899cfee81cf19f90fa57bd3fc27ef0801`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/build_v007_closure_cx3/docs_plans/s1_independent_slice_cx3v001.py — SHA256 `20df45ad60a9d7d52b912dfce6f3ae76d233227d4376ce4ebee2dbef1a2c176f`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/build_v007_closure_cx3/docs_plans/s1_source_delta_cx3v002.py — SHA256 `deeac611d57d0d2713556210bab1969b404994371a4c9958ed99b3f03ef2cafc`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/producer_guard_cx1v008.py — SHA256 `294cb7760679b883a62fb3117dc75e91231b2f173bcec65983e6762371ea0731`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/postseal_records_cx1v006.py — SHA256 `9fbdb0ca24153436b7c807778f140b7998fc0c0b5d18f4372d65a20a0e11cc59`
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/srb_rot_record_cx1v008.py — SHA256 `500f8b6a27cff6157246cdaca1373ad7340003263578331d30cbdf7cebc0e4f4`
