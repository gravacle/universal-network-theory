# Independent operational review of v006r6 v002

`date -u`: Sun Oct 18 13:15:19 UTC 2026

**TESTED PASS within bounded operational scope: 51/51 checks.** Runtime 0.060443292022682726 seconds, peak RSS 47,497,216 bytes. One process, prescribed Python `-I -B`, stdlib only, single-thread environment. No scientific launch, solver call, network access, candidate edit, deletion, rename or overwrite. Candidate bytes were checked before and after the test.

**UNTESTED:** full live campaign/cache/engine integration, real post-state scientific acceptance, final V007 seal, production current-state certificates, full source enumeration. The production seal allowlist is empty, as it should be until a separately reviewed immutable successor registers actual evidence. A passing operational review does not authorize a launch.

## Reviewed bytes

Short paths below are relative to this report's directory.

| File | SHA256 from bytes |
|---|---|
| `calibration_orchestrator_cx2v006r6_v002.py` | `09a8f28aa36ba2ac396d7957e1dbee28cf52d7f18f5a1887bfa14915ab35eb88` |
| `calibration_core_cx2v006r6_v002.py` | `921abceaa7d8fc6be98619a2bb4eb1f7ddf5de5cb7d7d7a443c6f0dfc611ffbf` |
| `adoption_policy_cx2v006r6_v002.py` | `c7776f70ebe6cf9f3cc78836b1833861ef92c610db4ae57c84c3c36a9993c448` |
| `independent_operational_tests_cx2v002.py` | `39655c924a1654d321d794a2df1148a3343e49464ae3e92598d480e82246f637` |
| `independent_ops_review_cx2v002/RESULT.json` | `5e5d337029849c16fb049f502afdeb7cb1a97a4945531efa3f5ebd7fb980a276` |

Requirements read: dispatch `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0533_2026-10-18_codex2_orchestrator_v006r6_fixes.md`, SHA256 `9f1ee52a148618a0ce41c6320667edede0427918c804da83d47c703a324e80e2`; Claude3 review `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_calib_cx2_c3/REVIEW_CALIB_CX2_V006R5_C3V001.md`, SHA256 `8016cad0e816807088b062df850a1727f9a02b799b9b7b77aaece4b3c0d8e777`.

## Results

| Requirement | Test and result |
|---|---|
| A01 | Both actual deciding and capability callers accept the positive synthetic receipt and reject non-receipt and STOPPED_WALL_CAP cases by consuming `_receipt_ok` return reasons. |
| A03 seal | The unmodified v002 policy rejects a fully self-consistent invented comparator/prereg/report because its seal tuple is absent from the independently trusted allowlist. Source files are never imported or executed as comparators. A separate policy instance receives an explicitly synthetic tuple in memory only to exercise downstream positive and refusal branches. The on-disk allowlist stays empty. |
| A03 report | Rejects wrong reading, test mode, foreign compare SHA, invalid C4T, and explicit unsealed input. The positive fixture checks exact registered block/driver/case and byte relationships. |
| A03 C4-6 | The actual inherited adoption function passes a complete synthetic fixture and rejects mismatched seed, capability, timing, missing receipt, cap/disk declarations, reading and prereg. Additional checks set matching declared/config caps equal to measured usage and verify refusal for wall, RSS and output separately. Disk allocation below measured output and a stopped source receipt also refuse. |
| A02 | Actual `Cache.forward` emits `CertificateRefusal(BaseException)` through an ordinary `except Exception` handler. Actual CLI `main` catches an injected refusal and returns exit 3 with REFUSED output. No engine solve occurs. |
| A04 | Actual patched resolve is invoked first with a forced put failure, then with actual wrapper `Cache.put` refusing an uncertified root-invalid entry. Both refuse before creating a resolution journal. This proves failure ordering, not two-file transaction atomicity. No root-invalid evidence exemption is introduced. |
| A06 | Actual `Context.certificate_check`, `write_acceptance` and actual guard verify a synthetic prelaunch/current-state bundle. The only result is `out/result.json`; no top-level result exists. Missing handoff refuses. Writer verifies before exclusive creation, then rereads successfully. Repeating the same write leaves bytes unchanged; changed bundle and foreign driver refuse. |
| A06 reingest | Saved-call reingest control flow performs one bounded cache put and reports zero launches. Lock, executor, mapper and cache are explicit stand-ins in this narrow unit. The handoff/guard path above is tested without replacing either function. Full live campaign/cache integration is not claimed. |
| B4 | Headline D=4.04 is exempt. Alternate D without evidence refuses. A headline run cannot masquerade as the required alternate-D deciding evidence. A scoped alternate-D synthetic fixture passes; changing its receipt to STOPPED_WALL_CAP refuses. No real deciding run is claimed. |
| Production settings | K64 and M_s64 are independently refused by the actual production block validator. |

## Finding closed during this review

The initial candidate's numerics policy accepted a newly invented four-constant comparator, arbitrary newly written prereg and mutually consistent synthetic ADOPT_TAIL report with `synthetic=False`. A truthy `PIN_ADDENDUM_V005=True` sufficed. This was a TESTED seal-authentication hole, reported before any candidate edit. Parent wrote an immutable successor with a trusted `(compare SHA, prereg SHA, addendum SHA, report schema)` allowlist, exact byte-pinned addendum, and report/addendum binding. The successor refuses the reproduction.

Original wrapper `calibration_orchestrator_cx2v006r6.py`, SHA256 `8d5d06af84f7a24229129d50d381089cf0ffcac1bfe14b33b823de3b97c41374`, and original policy `adoption_policy_cx2v006r6.py`, SHA256 `7ab6ab39566ddceb060dac6465cacec4c5d876136e66bc36151133392df64082`, remain unchanged. The first test result `independent_ops_review_cx2v001/RESULT.json`, SHA256 `148ecc090cdaab2945360a5911006cb25f18cad6979de729c4e93eb286461d5e`, records the seal finding and an A04 harness error: the initial synthetic HALT item omitted `call_index`. That fixture error was corrected in the new test source; it was not a candidate defect.

## Fixture trust boundary

Synthetic receipt verification, custody derivation, complete-state enumeration and certificate producers are labeled as fixtures. The actual certificate guard and certificate-check/writer functions are not monkeypatched. This tests plumbing and refusal behavior, not scientific truth of fixture claims. The independent review does not supply a trusted production seal or approve any scientific certificate producer. The parent's full inventory and distinct scientific reviews remain mandatory.
