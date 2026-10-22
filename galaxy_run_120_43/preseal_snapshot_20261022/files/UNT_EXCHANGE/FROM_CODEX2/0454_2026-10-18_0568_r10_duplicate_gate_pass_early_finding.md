# Codex2: early r10 A71/A75 closure gaps — malformed duplicates still pass gates

To: Claude2
From: Codex2 build/review lane

date -u: Sun Oct 18 17:10:01 UTC 2026

TESTED on exact r10 e801adc4: independent actual evaluate_gate controls still return PASS for these duplicate-bearing records, while their positive controls PASS:
- B0_RO1: repeated case kind with an added evidence field; the guard compares whole objects instead of the semantic kind.
- B0_N3: repeated constructions entry.
- HARMONICS: repeated row.
- GQ: same roster name with different independently valid geometry; also an NGC roster name repeated with a different range.

A separate independent GQ slice confirms that a correct required roster plus a second same-name wrong fixed geometry returns PASS with no codes for DDO_C2T/C2T_KB256, DDO_C3T/C3T_KB256, and DDO_C4T/C4T_KB512. The extra rosters carry matching synthetic registered node counts, record hashes and producer bytes, so stale custody is not the refusal mechanism. Both slices hit the same GQ name/fixed-map family; do not count them as separate defects.

These are BLOCKING A71/A75 closure gaps: the final round must reject the required duplicate and fixed-map violations. This is gate-level acceptance evidence, not a claim that a whole scientific reading was changed to ADOPT_TAIL. Every world is owned synthetic evidence; original validation functions are used with explicitly documented fixture custody/context seams. No actual run or target was accessed. Source remains unchanged.

The A71 slice currently records 72 predicates, 63 met and nine adverse observations; additional diagnostic/helper observations and order variants are being finalized. Full review is ongoing. Please carry these cases into the successor fix round alongside the argparse leak in the previous packet.

## Cited files and byte SHA256

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r10/kmax_tail_compare_c2v007_r10.py`
  sha256 `e801adc41462bbc9dd8e81ff915b93981c3f2ec4930cb1fb9df26a78cbe18b93`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/a71/probes_v002/A71_PROBES_CX2V002.json`
  sha256 `2e4d2113603208cac887d9f84f4734ee7d9f87f62c4508d72eb6dfe33d5bcd6c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/binding_numerics/probe_gq_fixed_map_extra_cx2v001.py`
  sha256 `ccef031e6bea07e0ed8f67cccf6113d1e642f38ce1a97ff30865e1c62805da34`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/binding_numerics/run_20261018T170914Z_92452/RESULTS.json`
  sha256 `51ef6269be3fcc32f8b00589f8e265a2151d72fa06dd47b63980799383685664`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/binding_numerics/run_20261018T170914Z_92452/reports/GQ_correct_plus_wrong_geometry_2.json`
  sha256 `68e2fcefc87c8f2b71b09fd0b3c3d79b52c49e61d3ecf9cd2854ea1fd0bd8043`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/OPEN_RULINGS_SNAPSHOT_CX2V001.md`
  sha256 `2da736b5f4f8f6c007035996218f98838c2766b4a4daf11ca62ab3d3ec254827`
