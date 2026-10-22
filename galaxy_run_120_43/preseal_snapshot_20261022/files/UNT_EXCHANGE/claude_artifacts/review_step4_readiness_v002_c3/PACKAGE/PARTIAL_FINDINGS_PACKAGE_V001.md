# PARTIAL findings — PACKAGE lens, review of Claude4 step-4 readiness V002 (C4V002)

Helper of the Claude3 lane. Started 2026-10-19T00:27:10Z. STATUS: IN PROGRESS. Final report goes in the hand-back text.

Lens items: (1) HASHES 86 entries + V001 unchanged; (2) DELTA completeness; (3) spec handoff reconciliation 33 template calls; (4) certificate classification (<=3 V007 adoption pins, 27 to R-C1); (5) disk plan R-D17 / caps; (6) closure of Codex2 0491/0497; (7) root-item list completeness.

## Log
- 2026-10-19T00:31:45Z item (1) TESTED: top manifest 86/86 equal (0 unequal/missing/dup/symlink); V001 launch_order 39/39, inventory 19/19, dryplans 3258/3258 + addendum 1/1, refute 453/453; no unlisted file in any V001 folder (all extras are the 42 published V002 copies); work manifests order 47/47, dryplans_inventory 38/38, handoff 91/91, fixlog 153/153, refute_rulings 11/11, refute_numbers 24/24, refute_provenance 37/37, publish 31/31. Record work/VERIFY_MANIFESTS_C3PKG_V001.json 0f85b99d. Fence selftest 11/11 refused (os.path.exists swallowed one PermissionError; the BLOCKED list shows it); BLOCKED [] in the verify run.
- 2026-10-19T00:38:30Z item (3)/(4) TESTED independent reconcile (own tool, not Claude4s): 1106/1110 checks true; the 4 false are v001 templates lacking binding_status (v001 schema differs, disclosed in SPEC_HANDOFF 1.1). 33 calls 11/4/9/9 identical across v001-v004; all spec/prov/source/driver pins re-hash; D bitwise; tail schema; prov differs from dry only at label+2 slots; point keys 29 tail-ON -> 27 distinct, anchor triple TAIL_REANCHOR/WORKERS_8/HEADLINE_TRIAL = 8ad6ca4e = C4T FILLED de6d7d77 point (case block 76309ae3 names it); C4T numerics = dry block + exactly the two A70 slots; DRYPLANS classes 3 V007_ADOPTION_PIN (exactly the anchor triple) / 90 OTHER; 27 non-anchor tail-ON (26 direct + seed) -> R-C1; seed point distinct (28 total). Record work/RECONCILE_C3PKG_V001.json 3617a006. Fence BLOCKED [].
- 2026-10-19T00:38:30Z candidate SHOULD_FIX: R-D17 omits A105.3 (step-2 outputs ~250 GB on internal SSD, 992 GiB caps, 80 GB watchdog) -> internal free 454.1 GiB reading is pre-step-2; disk guard recommended for direct batches is not implemented in launcher008/guard007 (no free-disk check; only memory_free + per-call caps). Runbook CX1V003 step 6 says internal-SSD placement vs R-D17 External1 default (disclosed by Claude4 as root ruling).
- 2026-10-19T00:38:30Z candidate SHOULD_FIX (producer contract): SPEC_HANDOFF 5 step 4 says refusal leaves no output dir, but cmd_final writes specs (L428) before reading PROBE_REC/provisional pins (L429-441) and manifest (L458) -> a later PIN_MISMATCH leaves specs without manifest.
- 2026-10-19T00:45:42Z item (5) TESTED: V011 step-2 output caps (LAUNCH_PLAN_V011_CX3V001 1b406591) sum computed from bytes (see next line); A105.3 (V005 copy c01b3c51 L913-929): step-2 outputs stay internal (~250 GB expected; 80 GB watchdog). V002 R-D17 cites A85.3/A99 V6-S2 only, internal 454.1 GiB pre-step-2; LAUNCH_ORDER L493 says A105 changes no step-4 record beyond R-A3 wording. Launcher008/guard007 have no free-disk check (only memory_free L29-36 and per-call caps).
- 2026-10-19T00:45:42Z item (6) TESTED: Codex2 V001 findings: CX2-S4-GUARD-B1 (fallback) closed (no fallback key at any depth in LAUNCH_ORDER_C4V002.json; R-B6 packet-only); CX2-S4-GUARD-S1 (R-C8 ids) closed (V002 cites probe v002 878d612a/4f0521aa/b370470a = REGISTRY_GROWTH_PROBE_C4V002 bytes); S-1 >=48h closed (sim v003 L56 + late_ge; Codex2 0519); notes 9H/10H, 120-call assumption, 25% pre-admission, 8 h cap, budget 17/24/48 all carried (DELTA rows 12-15, R-D7, R-A5).
- 2026-10-19T00:45:42Z item (7) candidate SHOULD_FIX: DIII tail_off_policy (guard007 L215-218; IMPLEMENTATION_INTERFACE_CX1V003 L20) absent from ROOT_ITEMS_FINAL_C4V004 (0 hits), LAUNCH_ORDER_C4V002, INVENTORY_C4V002 DIII launch_path_steps and DRYPLANS_C4V003 DIII records; only SPEC_HANDOFF 3/7 list it.
- 2026-10-19T00:49:44Z pins re-check TESTED: 1532 pins in the 8 published JSON (= INDEX claim); 1517 equal, 0 unequal, 0 missing; 15 occurrences (8 files: 7 DDO154-named run-config/coordinate JSONs + NGC3198-named V004 addendum) refused by my stricter fence and not hashed. Record work/RECHECK_PINS_C3PKG_V001.json 6a35a769. RECONCILE: 129/129 distinct pins re-hash; 0 protected opens in its opens list.
- 2026-10-19T00:49:44Z item (2) TESTED structure: every changed V001 root item appears in V004 changes table except src-only wording (R-A6, R-B3, R-D7, R-D16); inventory +S4-CERT-PRE/POST (F06), field-set changes map to F01/F03/F04/F10/RR01/RR02/P02; dry plans 34->34, field sets map to F01/F03/F04/0623; record-level change tables omit some field names (NOTE). Record work/DELTA_DIFF_C3PKG_V001.json 6d07a2f5.
- 2026-10-19T00:49:44Z NOTE: Codex2 0494 source review pinned overwritten V001 bytes 056defdf/218b5574 (disclosed F09); findings persisted to manifest bytes and are closed in V002.

## Lead summary at 2026-10-19T00:52:13Z (STATUS: COMPLETE; the full structured result is in the hand-back)

Verdict: PASS_WITH_FINDINGS. 0 BLOCKING, 4 SHOULD_FIX, 5 NOTE.

SHOULD_FIX
- PKG-S1 R-D17 / disk plan: A105.3 (RP-S2) is not folded in. Step-2 outputs stay on the internal SSD (about 250 GB expected; the V011 caps sum to 992.0 GiB, TESTED from LAUNCH_PLAN_V011_CX3V001 1b406591; an 80 GB watchdog). The internal-SSD analysis uses the pre-step-2 reading of 454.1 GiB, and LAUNCH_ORDER L493 and DELTA section 4 say A105 changes no step-4 record. The fail-closed disk guard recommended for the direct batches has no implementer: guard007 and launcher008 have no free-disk check (only memory_free, L29-36, and per-call caps).
- PKG-S2 The DIII tail_off_policy is missing. guard007 L216-218 and IMPLEMENTATION_INTERFACE_CX1V003 L20 require it, yet it is absent from ROOT_ITEMS_FINAL_C4V004 (md and json, 0 hits), from the INVENTORY_C4V002 S4-DIII-* launch_path_steps and from the DRYPLANS_C4V003 DIII prerequisites. Only SPEC_HANDOFF L86 and L203 name it.
- PKG-S3 The route-A cap ruling has no root item. The guard requires max_active (L243-244). R-D14 L382 points to "the route-A cap (R-D8)", but R-D8 (L329-336) covers only the wall, RSS and output caps. The N1 1.80 GiB condition and N5 sit in no root item.
- PKG-S4 SPEC_HANDOFF md L148 says a refusal leaves no output directory. In the producer, write_specs (L428) runs before the read_pinned calls on PROBE_REC and on each provisional spec (L429-441) and before the manifest is written (L458). A refusal there leaves the specs without a manifest (fail-safe).

NOTE
- PKG-N1 For SENS, the binder-check wording "manifest inputs.config == admission C1 pin" conflicts with the sibling config of R-D16. The JSON adds the SENS check.
- PKG-N2 The record-level change tables omit some field names. The item-level DELTA coverage holds.
- PKG-N3 Codex2's 0494 review pinned V001 bytes that were later overwritten (056defdf, 218b5574). This is disclosed under F09, and the findings are closed in V002.
- PKG-N4 The 0115 phrasing "the other 27 go to R-C1" is a simplification. All 30 tail-ON specs need R-C1, and the records say so.
- PKG-N5 My fence refused 8 protected-named files (15 pin occurrences) in the pin re-check. Claude4's 1530+2 claim is consistent with that. W4 opened DDO154 config and coordinate files, which is disclosed.

Conduct disclosures
- Short read-only stdlib one-liners in the pinned Python ran without c3run, and some ran without the BLAS variables or taskpolicy. They were JSON inspections of named package, packet and registry files; none named a protected path.
- Bounded recursive greps ran inside the object subfolders only.
- One zsh echo of a '=' string failed ("not found") with no effect.
- Four small helper scripts were written to the session scratchpad. They are byte-copied to tools/scratch_copies/.
- I read the V005 addendum byte copy (rulings text) in the package.
- Listing calib_tail_readiness_cx2/v006r7 showed DDO154-named config file names.
