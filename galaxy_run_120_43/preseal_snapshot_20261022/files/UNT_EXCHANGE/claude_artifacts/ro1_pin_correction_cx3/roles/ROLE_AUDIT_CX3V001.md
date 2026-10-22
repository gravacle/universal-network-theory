# Dispatch 0563: r5 RO1 role verification and Codex3 metadata audit

`date -u`: Sun Oct 18 16:15:19 UTC 2026

**TESTED PASS: 33/33 checks. No wrong NGC/nodes_v001 worker-pair use was found in the scanned Codex3 review and readiness metadata.** The corrected role assignments follow the actual r5 AST and full worker bytes; no scientific source was imported or executed.

The scan covered 584 files: 49 r5/certificate review artifacts, 48 readiness BUILD/REPORT/HASH or Markdown files, and 487 Codex3 packets. Nine files contain the relevant hashes, on 130 lines. All 110 explicit path/hash pairs match the corresponding worker or binding filename. The two prose hits were manually checked: the current start packet states the corrected roles, and the earlier readiness report cites the NGC binding correctly. Hash-only token-change records carry lineage values without assigning a conflicting role.

## Role manifest from actual r5 bytes

- **NGC_RO1_SERIAL**: `RO1_ROUTE_A['ngc_worker']`, driver line 296.
  File `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/ro1_readout_c2/ngc43_composite_coupled_root_worker_v002_uvtail_ro1_c2v002_r5.py`; SHA-256 `b6c4586d2236a4cb14cc3d334adb0c8bb0aa729a3c23b33af8f71f807777370d`.
  Its `LOCAL.binding` at worker line 26 is `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_readout_c2/ngc_composite_full_coupled_binding_v002_uvtail_ro1_c2v002.py`, SHA-256 `52dc4065da6b0307d1a37bb63bf22921edd08709a763b0ed5a114e8c2b0f2226`.
- **NGC_RO1_PARALLEL**: `RO1_ROUTE_A['ngc_worker_parallel']`, driver line 297.
  File `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/ro1_readout_c2/ngc43_composite_coupled_root_worker_v002_parallel_uvtail_ro1_c2v002_r5.py`; SHA-256 `ee0510dface33bf97b55d51e31941c635b365f386054bf96b9dd218a490e3a3e`.
  Its `LOCAL.binding` at worker line 28 is `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_readout_c2/ngc_composite_full_coupled_binding_v002_uvtail_ro1_c2v002.py`, SHA-256 `52dc4065da6b0307d1a37bb63bf22921edd08709a763b0ed5a114e8c2b0f2226`.
- **DDO_RO1_SERIAL**: `RO1_ROUTE_A['worker']`, driver line 294.
  File `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/ro1_readout_c2/ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_c2v002_r5.py`; SHA-256 `fbe9ae79ac113aab76109ece785d8030729ce62890dc76ff58144a75af6c17b3`.
  Its `LOCAL.binding` at worker line 28 is `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_readout_c2/ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py`, SHA-256 `86af6198045ee6995daa7b57e78570643ddbd9edcc0eba42e2fdc816897ca885`.
- **DDO_RO1_PARALLEL**: `RO1_ROUTE_A['worker_parallel']`, driver line 295.
  File `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/ro1_readout_c2/ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_c2v002_r5.py`; SHA-256 `869ce3870a13fdc94a014cdb0b34eab867c05e59ab7d8abfb15f7db382fd52da`.
  Its `LOCAL.binding` at worker line 30 is `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_readout_c2/ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py`, SHA-256 `86af6198045ee6995daa7b57e78570643ddbd9edcc0eba42e2fdc816897ca885`.
- **NODES_V001_RO1_SERIAL**: `NODES_ROUTE_A['worker']`, driver line 379.
  File `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_a/ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_nodes_c2v001_r5.py`; SHA-256 `0ae245d86ef4f28c9a348094cedca14e5b2f4e704a9c90905a167084ac88af15`.
  Its `LOCAL.binding` at worker line 31 is `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_readout_c2/ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py`, SHA-256 `86af6198045ee6995daa7b57e78570643ddbd9edcc0eba42e2fdc816897ca885`.
- **NODES_V001_RO1_PARALLEL**: `NODES_ROUTE_A['worker_parallel']`, driver line 380.
  File `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_a/ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_nodes_c2v001_r5.py`; SHA-256 `a527717283f8234df6a562eae6a4f28d5c9d34abfbc08cd7cf3f18d7d5f903f2`.
  Its `LOCAL.binding` at worker line 33 is `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_readout_c2/ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py`, SHA-256 `86af6198045ee6995daa7b57e78570643ddbd9edcc0eba42e2fdc816897ca885`.
- **DDO_AND_NODES_V001_BINDING**: `RO1_ROUTE_A['binding']`, driver line 298.
  File `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_readout_c2/ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py`; SHA-256 `86af6198045ee6995daa7b57e78570643ddbd9edcc0eba42e2fdc816897ca885`.
- **NGC_BINDING**: `RO1_ROUTE_A['ngc_binding']`, driver line 299.
  File `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_readout_c2/ngc_composite_full_coupled_binding_v002_uvtail_ro1_c2v002.py`; SHA-256 `52dc4065da6b0307d1a37bb63bf22921edd08709a763b0ed5a114e8c2b0f2226`.

**Binding clarification:** `86af6198…` belongs to the DDO and nodes_v001 binding. The NGC workers use the distinct `RO1_ROUTE_A.ngc_binding` / `LOCAL.binding` pin `52dc4065…`. Both binding byte hashes verify. The nodes_v001 workers, unlike the NGC and ordinary DDO RO1 workers, explicitly include the `uvt_nodes` dependency. The NGC workers select NGC preparation; the other four select DDO preparation.

## Affected-location audit

**No corrections required in this lane's scanned files.** Existing immutable artifacts remain unchanged. Relevant existing locations are listed below with their current byte hashes; the JSON audit enumerates every matched line and all 110 verified structured pairs.

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0604_2026-10-18_dispatch0563_corrected_RO1_pin_audit_start.md`: SHA-256 `0323f8cd297ad6b00b212b7638e8e66f13c11ea8f94245395becf435cabda184`; 1 matching lines, first at line 5.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/FILE_HASHES_V001.json`: SHA-256 `1c03fc601517091717d5a1a92b6e5329ddb5c6e72cf041bb98717aed43e4d05a`; 1 matching lines, first at line 43.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/LANE_A_READINESS_REPORT_V001.md`: SHA-256 `3dd07d7301348476671749e6473ae7bb0628d75c8d8446fc263a525e91daec6e`; 1 matching lines, first at line 63.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/r5/BUILD_REBASE_CX3V001.json`: SHA-256 `728efb032043e050f3e1e2d17d7bbc1313e3a50cf6e5a6b957b12a4f0c5a1aeb`; 12 matching lines, first at line 93.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/route_a/BUILD_ROUTE_A_CX3V001.json`: SHA-256 `597584e3935368cb15f5573fa23992434cb861787da3982744e14dd6c31bd720`; 1 matching lines, first at line 25.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/r5_source/DECISION_V001.json`: SHA-256 `53c4afecef05d4418c95bffdeca3cf1a805ab2d3dee11b4bc412efa90273c528`; 8 matching lines, first at line 144.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/r5_source/PIN_GRAPH_V001.json`: SHA-256 `d63f8dd004a6ac04a1db2a9227843611ba084e2a2087f44c2499d5d4277fa7e9`; 36 matching lines, first at line 260.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/r5_source/R4_PIN_GRAPH_V001.json`: SHA-256 `257427254780c66303b1ac3401c7319264b5dddb82d48e3e48528934d4d12948`; 30 matching lines, first at line 288.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/r5_source/TOKEN_AST_BYTE_PROOFS_V001.json`: SHA-256 `ed145a716e72136b7b6eb965521f88e99ae728998bb00cdb207ee46e759e7c9c`; 40 matching lines, first at line 1450.

The prior r5 source decision, graph and token proofs already pair the NGC worker filenames with b6c4586d/ee0510df and the nodes_v001 filenames with 0ae245d8/a5277172. The earlier r5 rebase BUILD likewise records both pairs under their correct paths. The reviewed r5 byte and closure conclusions therefore need no successor for this role correction.

## Scope and limits

**TESTED:** the eight r5 role pins, six workers' local binding and preparation families, nodes_v001 dependency distinction, and the listed metadata/packet scan.

**UNTESTED by this lane:** active v011/freeze source selection, raw dry-run plan documents, other accounts' artifacts, and worker runtime execution. Active NGC and freeze audits are owned by the parent/sibling lanes. Raw `DRYRUN_REPORT.json` files are explicitly excluded from this metadata census. This report makes no statement about future launch packets and does not authorize a launch.

No scientific run, prohibited UVT/C5H read, observed/target NGC velocity read, network, overwrite, deletion or rename occurred. The only writes are new successors in this directory. Python used the prescribed isolated runtime, no bytecode writes and single-thread environment.

## Evidence byte pins

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/roles/audit_roles_cx3v001.py`: `b16f12e6fc735a11ff8e24f8fa7813aeb433c1a5c61f008d7c3ec54e895d6f41`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/roles/R5_RO1_ROLE_MANIFEST_CX3V001.json`: `3c528684c636e4a650ec07c154e10ec4970028b7f16c3b86eacb7c098976527e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/roles/AFFECTED_LOCATION_AUDIT_CX3V001.json`: `f3bbe250ff354d5c5df099b5dfe3e2cb3103b17af64866a177a32f1a3bd309aa`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/roles/INPUT_HASHES_CX3V001.json`: `d91eaf8a81d50d29a48b20db8eb63dea709f64dd441ec76b3619affbca8cb6d9`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py`: `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0563_2026-10-18_codex_any_A62_pin_correction.md`: `10eb9cb361ff59f2c510e065450c7257b5bf3114e0e4024d95ada143bf239f7f`
