# NGC-only RO1 worker/binding role guard successor

Sun Oct 18 16:17:55 UTC 2026

**TESTED: 117/117 focused synthetic checks pass.** Driver successor r005 is ready for the parent lane's DDO B0 and NGC plan integration checks. This report does not claim those broader checks have completed.

The parent probe demonstrated that the inherited shared RO1 outcome accepted a nodes_v001 worker hash paired with the current NGC binding, in both headline and Stage0 contexts. Dispatch0563's role correction exposed this admission defect. The earlier freeze-lane census remains scoped to the freeze boundary; it did not test this upstream shared driver predicate.

The successor adds exactly 1308 bytes before the main guard. Removing that insertion reproduces every parent r004 byte. The insertion retains the original `ro1_outcome` reference. Outside `_NGC_V011_ACTIVE`, it delegates directly to that reference. Inside NGC it first obtains the original block, then requires an armed block's worker to equal the selected `V011_PINS` serial or parallel worker and its binding to equal the selected binding. `V011_PINS` already follows the existing headline/Stage0 context; no role hash is guessed or hardcoded. Existing context-entry byte checks, binding-path custody, convergence and event checks remain in force.

A rejected pair produces the normal block shape with `armed=false`, `fired=false`, empty events, and null worker/binding hashes. A supplied refusal is retained as `inadmissible_record`; absent refusal stays absent. No original driver statement, DDO mapping, absolute dependency path, scientific arithmetic, source construction or stage implementation changes.

The focused harness imports definitions only and calls RO1/context functions on synthetic start records. It verifies both selected serial/parallel workers for both coefficient contexts; both nodes-worker defect reproductions and rejection; DDO, old r5 NGC, other coefficient-grid and unknown roles; incorrect binding bytes/path and independently exercised binding-table drift; absent, null, malformed and invalid event records; convergence/status/row conditions; malformed/missing starts; normal and exceptional context restoration; exact DDO delegation before/after NGC contexts; and preservation of all parent bytes outside the insertion. Peak RSS was 62,324,736 bytes. Audit denials: zero.

UNTESTED here: full DDO B0, NGC dry-plan integration and scientific runtime. Those integration checks are owned by the parent lane; no full freeze/score rerun was needed. The inherited TypeError for an unhashable malformed worker_pin remains unchanged; it yields no armed/fired result, and exception context restoration is tested. This narrow role guard does not claim broader producer authentication.

Timestamp correction: the first focused result artifact had an erroneous manually supplied date-u argument. It is preserved unchanged and excluded from final evidence. The V002 harness reran the same 117 expectations under new fixture/output names with the actual captured `date -u` value above; candidate source bytes were unchanged.

No scientific launch, real target read, prohibited-run read, network operation, deletion or existing-file overwrite occurred. Python isolation and single-thread BLAS were used. All cited hashes are from file bytes.

| File | SHA256 |
|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/successor/galaxy_m0_forward_c2v011_cx3v005_cx3r005.py` | `f85746f0bdfd3c108771225eff7c8a55a81e5d6634ee0e5403cf68aa9fa3dd6b` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/galaxy_m0_forward_c2v011_cx3v005_cx3r004.py` | `39c505175905576ff1029ede4be20be765ba47967b5a6eedf1298bd7c4305895` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/successor/BUILD_SOURCE_CX3V001.json` | `08d3037ad9c47a99e3aa35c5449b0a21e77f06363d97a15a285b5b1a8f699bd1` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/successor/FOCUSED_TEST_RESULTS_CX3V002.json` | `f8f0faccfd9691e70cd115d8629b82de64a02cb0229eb36d72bb87eb7a74518e` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/successor/test_ngc_ro1_scope_cx3v002.py` | `11de06511debf6685082d5d8177dc08ac39dc59b215f10a98a8e08b0177473eb` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/successor/build_ngc_ro1_scope_cx3v001.py` | `cdc6301e14dc9bda795c0c6b127a9a5991b57326c1fa6152712f5fde13a7609d` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/guard_probe/RESULTS_V001.json` | `506a63a3b740a872f9e25678869f6def869082fcecd0e4a71ed7736ddee1c5c6` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0563_2026-10-18_codex_any_A62_pin_correction.md` | `10eb9cb361ff59f2c510e065450c7257b5bf3114e0e4024d95ada143bf239f7f` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/successor/seal_ngc_ro1_scope_cx3v001.py` | `acbd36a6dec799c6e943fd00ca236f428f21d7b45a0ea3d99a285e87b3e1210e` |
