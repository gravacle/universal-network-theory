# Provisional seal pre-stage continuation — CX1V001

date -u: `Sun Oct 18 22:07:33 UTC 2026`

Status: **PROVISIONAL FAIL / 3 blocking findings on copied script006 + helper007**. B1 and B2 were already reported and adopted by Claude2 dispatch0639. B3 is a new TESTED integration finding. This is a review snapshot, not a final selected publication; current script preflight deliberately refuses pending v003 integration. Final delta remains pending the selected successor tuple.

## New TESTED blocker SA-CX1-B3: dispositions container disagrees with v003

Copied helper.py lines233–241 takes a bare list, object.dispositions or object.rows. It never reads object.entries. Copied script.sh lines242–250 invokes this helper precheck before tool1. Current v003 tool1 requires exactly schema, frozen_addendum_sha256, entries (line43; lines146–163).

The synthetic inert object has the exact v003 schema and one later A102 row with a matching section hash. The exact extracted pure v003 disposition_codes function accepts it with zero failures. The exact copied helper rejects the identical bytes with DISPOSITIONS_NOT_A_LIST before it accesses any frozen/prereg argument. Three of three controls passed, including actual nice>=10. No real scientific documents or data were passed to either validator. Evidence: dispositions_controls_v001/RESULTS.json.

Required successor correction: consume the exact v003 entries contract in the helper and preserve that same pinned file through tools1,3,4. A valid v003 disposition object must pass precheck; malformed/duplicate entries and wrong section/change pins must refuse.

## TESTED boundary regression results

18/18 inert controls PASS in boundary_controls_v001/RESULTS.json: exclusive new writes; existing-output refusal and preservation; no implicit parent creation; wrong-pin refusal without output; exact byte copy; prereg changes confined to slot values; exactly five compare pin lines changed; global pin rebind refused without output; isolated run_h shell wrapper stops on a failing inert helper and on noclobber; existing log preserved; error trap visible; nice>=10. These controls execute a copied helper and an extracted inert wrapper only, never the real root seal script or comparator. They do not close B1/B2.

## TESTED source inspection; runtime limits stated

- Copied helper pin returns the bytes it hashes (lines99–110); _exec_module compiles that exact returned buffer (lines293–300). Those paths preserve source-buffer custody.
- Copied script H executes HELPER by pathname (line148). HELPER_SHA is checked once during step0 (line167), rather than every H call. Tool inputs are re-pinned before steps6/7 (lines338–351), then invoked separately by pathname. v003 tool1 imports seal_common through ordinary Python import (lines32–35). Thus the present source does not establish one verified source buffer through every executable boundary/import. This is a source-only residual observation; this continuation did not inject a replacement helper or v003 module, did not inspect a live pycache and does not claim those live bytes changed. Existing B2 already demonstrates the distinct fence-loader cache issue; broader import custody remains UNTESTED at runtime.
- Dispatch0639 explicitly resolves tool2/tool3 order to the v003 README order. The old order discrepancy is closed as an authority question, not counted as a blocker here.
- The published README already lists pending v003 pins, extended slot schema, text-of-record sha flags, native JSON output handoffs, driver-build selection and admission crosscheck. These known construction tasks are not recounted as newly found defects. B3 is additional to that list.
- The known metadata-alias B1 prevents certifying that all pre-step9 paths avoid protected target metadata. Direct real C5H/UVT/target access was never attempted. Root-only operations and complete script behavior remain UNTESTED here.

## Ready successor controls

regress_fix_delta_cx1v002.py is **TESTED syntax-valid, runtime UNTESTED pending corrected successor**. It preserves v001 and adds explicit typed refusal checks plus stat/lstat/readlink/listdir/scandir spies on a new inert protected-name target. It tests no target metadata before alias refusal, exact pinned-source execution despite a deliberately different inert pyc, wrong source-pin refusal and nice priority. Run it only with a newly copied, byte-pinned snapshot and a fresh output directory under this review directory. It never opens a real protected path. Existing interface and boundary harnesses are available for targeted successor adaptation.

No new review of final selected publication is claimed. Parent owns inbox watch and final outbox packets. This helper's deliverable is the new actionable B3 plus tested boundary coverage and a prepared corrected-successor harness.

## Byte pins (each computed from the cited file's bytes)

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v001/SNAPSHOT.json` — `6ed2188160d79acf0b11a9f5c39fe897dc8e457e425f661e19635b8d6d8eef27`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v001/script.sh` — `cb3aeb324067910acdd9be5730e70305c819df4327ba00465aeae89249d3ed34`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v001/helper.py` — `2f08fb88c17dbe340fe5f03da10ed510aff384cdb404d8e3d9544664d2d79172`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v001/README.md` — `2391590b453f5c029f94e9f5cc52086865ac94ebb1071de799475acbaa242fc0`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v001/dispatch0639.md` — `251196b23610a371152d5cac1f1af0d37541e64679d0ed42508d7cde6dec6b6b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/boundary_controls_v001/RESULTS.json` — `10eb412bb2771fe8ee110d89782f7fc2c521b169502f058f479f3112c619a925`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/regress_boundary_cx1v001.py` — `6451f4e524ff2b153162b26893440875525200544cb5822a6686d255d8cfb4ea`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/dispositions_controls_v001/RESULTS.json` — `dd604682ae683eb17f67b76da203b9d3dfef9f77ee862b3aaa2f421419d98f27`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/regress_dispositions_cx1v001.py` — `f3c897c8d6e60f78c079652fa55944b73ee2234225130bf91d2f781e668ab281`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/dispositions_controls_v001/inert_dispositions.json` — `453deaa39073989e9c8b0057e743adebc4c54430df6137c7d0cc6846a67b9ca9`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/regress_fix_delta_cx1v002.py` — `b74e1ff43116b0ec1e2fc97243838f924f26848d3347b30fd08bac369c21a22a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/PRELIMINARY_FINDINGS_CX1V001.md` — `3c8959aef3884280dfd351a03754907c38d654cacb5eb5b52a4c9f0b1424b19f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/provisional_snapshot_v001/check_frozen_addendum_c4v003.py` — `72d9191d064e61e0a3f6d40d04848971d1babd852236ddae4da36b8ca910a612`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/provisional_snapshot_v001/seal_common_c4v003.py` — `101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21`
