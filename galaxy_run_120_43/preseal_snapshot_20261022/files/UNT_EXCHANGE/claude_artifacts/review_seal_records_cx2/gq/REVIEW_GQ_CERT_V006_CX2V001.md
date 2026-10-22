# GQ_CERT_V006 cross-lineage seal-record check

Date (`date -u`): Sun Oct 18 18:55:22 UTC 2026

**PASS — TESTED record crosscheck.** GQ_CERT_V006 is exactly the seven on-map roster objects selected from V005, in order, at indices `[0, 2, 6, 7, 8, 9, 10]`. All 23 checks passed. The schema, producer custody, subset-index/drop claims, preserved metadata and registry GQ entry were checked from bytes. No builder suite was imported or executed.

The independently implemented typed comparison ignores JSON whitespace and object-member order, preserves list/roster order, distinguishes integers/floats/booleans/strings/null, and compares each float by IEEE754 binary64 bytes including signed zero. Each whole file is separately SHA256-pinned. Seven equality controls establish these distinctions. All seven roster objects also retain their original top-level object-key order.

| V005 index | Roster | Geometry | Copied roster typed SHA256 |
|---:|---|---|---|
| 0 | DDO_C2T | C2T_KB128 | `9075e5404f65019cf3f8bba6aee95181a8d9be575f611b4d3d51b1f7177c5638` |
| 2 | DDO_C3T | C3T_KB128 | `b91ab2c958b05f0b1e6d50fd4638dcc37e1b69c8c064b2fe38b5c377a782bd2d` |
| 6 | DDO_C4T | C4T_KB256 | `3df1c86495e6d7352eb6a8e2b02e2076dd55e4d6ed446087433bd4d84145ad1b` |
| 7 | DDO_C4T-C5c | C4T-C5c | `bfa27dda75655d09e60d910d53fcc73a94d4cc220b9cdf3613b4d8243cb0b78c` |
| 8 | DDO_S4T | S4T_SPHERE_KB128 | `026e82899c6c130391eb3624a9c8ac3bdb836056955d50717fbd399acfc2ef1f` |
| 9 | DDO_C6T | C6T_KB128 | `a92c981a1da667dce63fb7a212356868ce99506684d214987f35b359b88d50f9` |
| 10 | NGC_T120L | NGC registered [2,32] | `5290d6ae5be8ffa8e0e08a531145ac203928210f06d368ef693ffe4171316e3e` |

The actual r11 `evaluate_gate('GQ', actual_V006_path, context)` returns **PASS**. The input GQ record and producer bytes are actual records; the registry's GQ producer entries, record SHA and all-node counts are projected exactly from V003. The case block is an explicit minimal P=128/M_s=128 test context with the registered fixed geometry map. **Full case-block validation, full producer-registry admission and sealed compare admission are UNTESTED in this component.** The parent reviews those independently.

Four separately registered synthetic mutations fail the owning data checks: repeated roster (DUPLICATE_ENTRY_A71), wrong geometry (FIXED_MAP_GEOMETRY), 4096-only all-node count (ALL_NODES_COUNT_EQUALS_THE_4096_SAMPLE), and error above threshold (UV_TAIL_GAS_QUADRATURE_UNCERTIFIED). Re-registering only each changed file's SHA in an owned context prevents an unrelated hash rejection from masquerading as a data check.

V006 intentionally inherits V005's aggregate metadata: `all_nodes_total=18215051040`, while the retained six DDO roster all-node counts sum to `8452247840`. Its `v006_subset.top_level_fields` expressly states that these aggregates describe the original 12-roster certificate. This is documented inherited metadata, not a newly recomputed seven-roster total.

Limits: GQ integrals, all production nodes, saved-state provenance, part records and row profiles were not recomputed or opened. No actual run, receipt, NGC target velocity, network, or launch access occurred; forbidden-path attempts recorded: 0. Before candidate import, open/list/scandir and stat/lstat/readlink guards were installed; the candidate protected-root tuple was replaced with an owned surrogate before any containment call. Source/certificate pins stayed unchanged. Prescribed isolated Python -I -B, single-thread environment, default priority under 0514 waiver.

## Byte-pinned references

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py` — SHA256 `a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/gates/GQ_CERT_V005_MS128.json` — SHA256 `fbceefe68fecda35745575fba6c85e550e016e8aeefea59233147e520c803e21`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/producer_registry_c3/out/GQ_CERT_V006.json` — SHA256 `5a1b39f8eccaaea107b5e4f5888456bf286714f17659d7dae256de3611b6484f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/producer_registry_c3/out/PRODUCER_REGISTRY_C3V003.json` — SHA256 `6b6f76ae301d75878156e7b8f2641215d215ada9017dbcba3b805a99589701a3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/producer_registry_c3/scripts/gq_onmap_subset_c3v001.py` — SHA256 `614483b529f890c568af3ac61fbf383e05f681b07839a54531996bf55bfe2dbd`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/tools/certs3_common_c2v003.py` — SHA256 `2e6b1bc5b4cc164ef2361aff420e69c38e309f1d221659bff06300c008c67635`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/tools/gq_full_c2v003.py` — SHA256 `17ce5e4102945ccb61148097ac486615618f82bfdc2d98b744492bd03dcbcecb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/tools/assemble_validate_c2v004.py` — SHA256 `6b01835c76f388fccba68712a84538551711e07494295aeb87f1966261f93598`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_records_cx2/gq/check_gq_subset_cx2v001.py` — SHA256 `053cbedfb7b018e7436b1ef1a10268aa2fc01a12bc3914708b69c20281792246`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/producer_registry_c3/out/PRODUCER_REGISTRY_C3V003_BUILD_REPORT.json` — SHA256 `83829489b441be4a596916be48873aacd8222e7b9b9493520e747db2e44f6360`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_records_cx2/gq/evidence_v001/GQ_CROSSCHECK_RESULT_CX2V001.json` — SHA256 `9a1714425c342d2875ebd285e13ceada8f70bd78034e4a0513c7b5c211aa34d7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_records_cx2/gq/evidence_v001/GQ_R11_ACTUAL_RECORD_RESULT.json` — SHA256 `dcc247ef6f0c5543d7849c1014266b9b015d1af9117aeb1ab33aa00089cf902c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_records_cx2/gq/evidence_v001/CONTEXT_SEAM.json` — SHA256 `e52362ed551c8d65d3e2f58c9cb8970ad63d1dcf36722d4b63c0032df5f274f4`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0605_2026-10-18_codex2_crosscheck_seal_records_while_waiting.md` — SHA256 `9c66a457d38debc1646c3a45aa2dd64bbf0164a93a62a2ec19d32662c5b61635`
