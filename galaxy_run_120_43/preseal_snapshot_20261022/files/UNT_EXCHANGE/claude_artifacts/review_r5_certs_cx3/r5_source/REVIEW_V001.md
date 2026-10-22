# Dispatch0552 r5 source and cascade review

date -u: Sun Oct 18 15:04:55 UTC 2026

**VERDICT: PASS_WITH_FINDINGS.** Parts (a) and (c) pass. Part (b)'s reachable pin closure and pin-only source requirement pass; its literal cascade-directory inventory is incomplete. This review covers source only. Part (d), numerical replay, is owned by the parent lane and is UNTESTED here.

**TESTED — module cap and all declared source deltas.** The 36 declared entries verify from bytes. Independent tokenize/AST/byte reconstruction passes 41/41 checks: the module successor differs in exactly one numeric token, 0.6 → 8, in TAIL_MEMORY_CAP_BYTES (644,245,094 → 8,589,934,592 bytes). The other changed tokens are declared complete SHA strings or paths that independently resolve to matching predecessor/successor path/hash pairs. The two sibling copies are byte-identical. Outside those exact token spans, bytes are identical; AST structure and all docstrings are unchanged. The r4 b9ae92d5 driver → r5 b5cc62af change is consequently pin-only. The producer generator, checker, recorded edit list and supplied diff files were not used as proof.

**TESTED — runtime source graph.** The own static expression interpreter resolves absolute and relative Path expressions, explicit Python path/hash pairs, existing local imports and sibling literals, and the library's provider fallback. It finds 130 r5 Python sources, 576 directed source edges, and 446 pin occurrences, all matching file bytes. There is no reachable changed predecessor path or hash. A separate census checks all 35,041 runtime string constants, including embedded substrings: zero stale changed hashes or paths. Seven comments and three docstrings retain lineage hashes and are excluded from runtime pins.

The r4 graph contains 129 sources. All 30 r4 sources that transitively reach the old tail library are represented by successors in the map. The canonical source-node and 576-edge sets match exactly after inverse mapping. The extra r5 node is the byte-identical provider fallback copy. Original provider and roster paths remain in binding PINS, but those bytes did not change. An absolute replacement path on the right of MODULE / path correctly overrides the old MODULE directory. The copied roster is not selected by the driver; four additional declared non-RO1 worker successors are also not selected. All are still covered by the 36-entry byte proof. The only unresolved Python path is the inherited literal /synthetic.py inside a caller-identity probe; it is not loaded.

**Finding F1 — missing orphan inventory entry. TESTED, nonblocking to the selected source closure.** The cascade directory also contains ddo_homotopy_reference_root_worker_v001_gal_c2v005_uvt_c2v002_r5.py (ec1a2108), omitted from CASCADE_MAP_R5_C2V001.json. Its predecessor is 6775599e. Independent verification shows exactly two pin string changes (binding path and SHA), exact byte reconstruction and unchanged AST otherwise. The orphan is unreachable from the selected r5 driver, which uses the c2v003 reference successor. Thus source reachability passes, while the requested literal manifest-completeness assertion fails. The closure/inventory test records 8/9 passing checks, with that single inventory failure.

Recommended resolution: write a new immutable inventory successor or addendum recording both orphan hashes and marking it NOT_SELECTED_UNREACHABLE. Do not overwrite the reviewed map or delete the orphan. This finding is retained even though it cannot change the selected driver’s current arithmetic.

**UNTESTED / limits.** No numerical tail evaluation, actual worker execution, launch, target velocity access, prohibited UVT/C5H run reads, or network access occurred. The graph is a conservative static graph of pinned source paths and literal loader dependencies; it does not authorize arbitrary caller-supplied future paths. No claim is made that an 8 GiB guard causes an allocation to remain below the principal's process-memory limit. This result is not launch authorization.

The independent closure harness initially had a tokenizer callback typo and stopped before writing a result. Its immutable v002 successor produced the cited successful closure result; the failed script is retained in the hash inventory.

Every cited file has a SHA256 computed from bytes:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/CASCADE_MAP_R5_C2V001.json` — `a7281e10a15c7f51eae8b5d5336648c1d0a7d04a8cf932b3860c9eba3636a880`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/module/owned_uv_tail_lapse_v001.py` — `c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py` — `2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py` — `b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py` — `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_b/stages/ddo_homotopy_reference_root_worker_v001_gal_c2v005_uvt_c2v002.py` — `6775599ed3c3ee4e32517246a323f692cbd47257629eb5425c1e15742057f9cd`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_homotopy_reference_root_worker_v001_gal_c2v005_uvt_c2v002_r5.py` — `ec1a2108ed79eccaffbbc0e1775edf66d327705b6a944a24866f2706abfb8a05`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/r5_source/TOKEN_AST_BYTE_PROOFS_V001.json` — `ed145a716e72136b7b6eb965521f88e99ae728998bb00cdb207ee46e759e7c9c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/r5_source/PIN_GRAPH_V001.json` — `d63f8dd004a6ac04a1db2a9227843611ba084e2a2087f44c2499d5d4277fa7e9`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/r5_source/R4_PIN_GRAPH_V001.json` — `257427254780c66303b1ac3401c7319264b5dddb82d48e3e48528934d4d12948`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/r5_source/CLOSURE_INVENTORY_V001.json` — `c92c35c992cf83bfd059254cccc555aa23c53ed325705d8e18144e11576882eb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/r5_source/RUNTIME_LITERAL_CENSUS_V001.json` — `91fd67e001d505c71463ecf9d196b3a8a6254d9a9a8195cc386539c78b2250d8`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/r5_source/source_audit_cx3v001.py` — `7c5045a9977a71e850edbffdec245ec99765f5049f3f310944260495523452c5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/r5_source/pin_graph_cx3v001.py` — `172d45083bcb4ce0de804d60ff90a5e910b515519e870171d2502bc8cca789b8`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/r5_source/pin_graph_r4_cx3v001.py` — `e3782308c78d72649e3c8b2655c7351f694e224ab8bbabe5fbfc3223c0ffca86`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/r5_source/closure_inventory_cx3v002.py` — `c876f93186375c9a0c4427069b783c5703b39cdc3e88df6281ecc4f3871d53d3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/r5_source/runtime_literals_cx3v001.py` — `2ebf583763dbedf6d9305d06517cf2464242389f3b11352438c33e9204131842`
