# Step4 guard v006 native-loader delta

Date (`date -u`): Sun Oct 18 20:53:02 UTC 2026

**FAIL — one blocking native-context compatibility finding, NI-3.** The earlier NI-1 bytecode-cache failure is closed by the new standard source loader. This is a bounded guard/loader delta verdict, not a full package or scientific admission verdict.

TESTED: 39/39 independent assertions, using the actual byte-pinned v006 guard with owned inert modules under the prescribed Python `-I -B`, single-thread environment. Four source pins matched before, after, and at report sealing. `nice unavailable (sandbox); 0514 waiver`. No full native context/driver/custody/certificate/adoption/sensitivity module was imported or executed. No runtime config, production report, receipt, run directory, target or scientific stage was accessed.

NI-1 closure: a correctly pinned standard SourceFileLoader load and a genuine transitive Python import now succeed with zero `.pyc` probes. Wrong source hash, nonallowlisted direct/transitive source, transitive wrong hash, and changed bytes after the initial source-map check all refuse on the owning hash/allowlist check. The changed-byte case uses a labeled read-return fault injection; no file was overwritten. Exact compile buffers pass; mismatched buffers and nonallowlisted absolute source filenames refuse. Serial nested fences restore the outer allowlist and loader; normal and exceptional exits restore the original global loader and fence state.

NI-3 — BLOCKING. The new compile audit hashes the compiled source buffer against the full file pin whenever the filename is an absolute Research `.py` path. The exact registered native context wrapper has `exec(compile(_resolve_source, __file__, 'exec'), O.__dict__)` at line 285. Its embedded function text hashes to `79e8936d96103b1540987a980b289b6d25e5e25941b02db647f7a833818da0e1`, while the full wrapper hashes to `24abe3bc4f6ee0e3c5d7c89502062cf99464573b35bc5b53c33c14ef2ae888af`. Therefore the native context module cannot finish loading under the new audit: the generated-function compile raises `PREFLIGHT_COMPILE_HASH_MISMATCH`. This executes before the direct preflight adapter can be constructed. The identical owned toy pattern succeeds without the fence and refuses with the actual v006 fence on exactly that code. The native module itself was not executed. A successor needs an explicitly bound generated-code mechanism while retaining exact source-byte checks; the check must not be broadly disabled.

The direct adapter bytes are unchanged from the previous reviewed version; its four-attribute prelaunch contract is not reopened by this delta. Empty adoption registration and closed sensitivity review/comparator flags remain prior pending policy premises, not resolved by a loader fix. Current pending policy may refuse earlier; the NI-3 claim concerns the compatibility path after those prior requirements are legitimately satisfied.

Harness correction: v001 stopped in test setup because it attempted to read the inner toy source to compute its pin while an outer fence intentionally did not admit that source. This was a harness error, not a guard finding. It and its fixture bytes were preserved. v002 precomputes those immutable fixture pins before nested use and completes all 39 assertions. No failed case was silently reclassified or deleted.

Limitations: production/native end-to-end execution, registered final config/source closure, already-loaded module-cache reuse, nonstandard loader classes, outside-Research library boundaries, and cross-thread interleavings of process-global patches are UNTESTED. No global readiness claim or authorization follows from this review.

Byte pins:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_direct_preflight_cx1v001.py` — SHA256 `eee61ac61ff93a11c97b9fdd3d6340661f17a92394653e524ac1cd8648d20fd1`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_guard_cx1v005.py` — SHA256 `11a31edd2cbbb0adb6738360bacecc6363b5cada4f91c0cd976276fd72c7e2d8`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_guard_cx1v006.py` — SHA256 `af66d0d8861f3d414c3a52e12e8b1f8d5f205c96b0abaf932949575a3ffe5832`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/calibration_orchestrator_cx2v006r9.py` — SHA256 `24abe3bc4f6ee0e3c5d7c89502062cf99464573b35bc5b53c33c14ef2ae888af`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/delta_v006/loader/run_v002/own_dep_cx2v006.py` — SHA256 `4e50eef146fd0ee9147a749220b38cd82745872a5b3ea7af5cabe79de4a094cf`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/delta_v006/loader/run_v002/own_dynamic_cx2v006.py` — SHA256 `f9e8e6041e66886457e2842245fbf01b9725ec3eac2a24e6f3463975146a6fbe`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/delta_v006/loader/run_v002/own_inner_cx2v006.py` — SHA256 `382ff38e2f7ae4f5b1ff2773d1d9e3481ca62264bc60061c60142e9ef20a3026`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/delta_v006/loader/run_v002/own_missing_cx2v006.py` — SHA256 `3e29430f1f5190ce5b49d92306ff0a807804a34c425ce0eca201f29817ad5015`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/delta_v006/loader/run_v002/own_outer_cx2v006.py` — SHA256 `68080d7ce916d73586d69035ccc362d882a112d2439c056d6a4519620e11ecbe`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/delta_v006/loader/run_v002/own_simple_cx2v006.py` — SHA256 `76b26c40fd1de8995c9a5457c2bd4cf363c42d1f88a66f4d583bc10295f2062a`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/delta_v006/loader/probe_loader_delta_cx2v001.py` — SHA256 `e18b4277d9e5151b7873e41870e38fd6afb04ca762307ab9e69f31227665f7f2`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/delta_v006/loader/probe_loader_delta_cx2v002.py` — SHA256 `234b23c4c0f44d9189b84f6583e310828262a458d09d025e2c4bab824666e0f8`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/delta_v006/loader/run_v002/LOADER_DELTA_RESULTS_CX2V002.json` — SHA256 `3a6fa4793b8d333fc5ce93d6073281a06be5c85c59d0f003142b9c888c2421c7`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/native_interfaces_v005/NATIVE_INTERFACE_REVIEW_CX2V001.md` — SHA256 `1131f3d1ae99dc2254e653c0578cdfd333ca22c5e57c1091d336fdce47d87bbb`.
