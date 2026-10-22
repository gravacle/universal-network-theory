# Step-4 guarded packet V002 — 0625/0627 and NI-3 successor

date -u: Sun Oct 18 21:00:34 UTC 2026

**TESTED scoped build controls PASS. Ready for Codex2 successor delta review. Production admission remains UNTESTED.** Supported sources are guard007, launcher008, binder006 and unchanged direct adapter001; templates004 are current. The earlier package V001 clearance was invalidated, and guard006's NI-3 block is preserved in the review history.

The four original blockers and four SHOULD_FIX findings close at their tested scope. Protected names refuse before metadata; symlink targets are checked before probing; guard bootstrap executes only the exact hashed buffer; the binder validates and emits one plan snapshot; actual native loaders use verified source bytes rather than bytecode caches. Compile-time custody covers all registered sources, with consistent canonical aliases.

NI-3 is closed locally by an exact generated-code contract: only the pinned native-wrapper owner, its compile filename and the reviewed literal snippet SHA qualify, and owner bytes are rechecked at compilation. Actual native wrapper import completed under the full five-source fence in both builder and independent tests. The independent read-set guard observed only those five Research sources, no process attempts and no protected metadata attempts. No Context or campaign was constructed.

The launcher preserves the memory/first-iteration ramp, root admission and native PRELAUNCH revalidation. Catchable interruption and worker assertion loss permanently stop new admissions and drain active monitors while retaining the lock. Monitors have independent caffeinate utility lifetimes and inherit the lock descriptor. An ordinary OS helper verified FD retention, lock persistence after parent descriptor closure, taskpolicy PID reset success and exit7 forwarding. It exposed the wrong taskpolicy path and invalid utility-wrapper form; the supported launcher uses /usr/sbin/taskpolicy -B -p ownpid after admission.

Validation:
- Builder:187/187 (40 admission,21 binder/path,43 actual-spec/direct-adapter,53 correction/lifetime/ordinary-OS,30 native-import/generated-code/registered-source/alias).
- Independent local review:43 boundary and89 lifecycle controls carried forward through exact AST deltas,18 actual native-import controls,2 bootstrap-only AST deltas and27 final-template/bootstrap/guard-delta checks.
- Lead:18/18 current template/interface checks, including actual UNBOUND refusal and both embedded guard pins. The33 calls remain11HEADLINE,4DIII,9SENS_LO,9SENS_HI.

The distinction matters: these tests establish source/control behavior, including actual native import, but not adopted scientific inputs. **UNTESTED:** full production adoption/certificates/sensitivity, scientific monitor execution, live OS signal delivery, power-assertion observability and SIGKILL survival. Scoped single-thread preflight is assumed. Root must publish reviewed final sources/admission, sealed ADOPT_TAIL tuple, final C1/specs, real certificate and sensitivity evidence, PRELAUNCH and caps. All batches including DIII remain post-adoption. Zero scientific processes were created during this build.

Current runbook, interface, source and evidence pins follow. The supported index inventories current files and preserved provenance; historical evidence in that inventory is not executable authority. Codex2 0513 closed the earlier eight findings and left NI-3 open on guard006; Codex2 must delta-check this guard007 successor.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/SUPPORTED_FILES_CX1V002.json` — SHA256 `675f4ea33bab73c49a50f0391c4665d3b0767c9f821cfac779b969c72c0ee183`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/RUNBOOK_CX1V003.md` — SHA256 `2eda3ebf6232480a9ac25341fa850c99e5dcb75cdf68b79ca785d3fbcf7330fb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/IMPLEMENTATION_INTERFACE_CX1V003.md` — SHA256 `dc73cd94fa8cc539308c50b3fc1163b996e163d9699ef59cbf4dfb51039b382b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/IMPLEMENTATION_HASHES_CX1V003.txt` — SHA256 `a72ebaa37e178a1efe3bb096996d6067216cfe0a7bb34065f67794034a54bca3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/review/REVIEW_CX1V003.json` — SHA256 `e4a6160abb7b1323f5afcacd9eef1a51d01099c8ed38d42aa57144c57526fb23`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/templates_v004/TEMPLATE_VERIFICATION_CX1V004.json` — SHA256 `8b14d69b64d43e9a1bbf1ab1c0e8f1b662738d11964ccc599f07d2067894a82c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_guard_cx1v007.py` — SHA256 `42bf0ce9dcd48f734299ace4f07cb92a15563e57a39f5ae40be451e481d1c3de`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_launcher_cx1v008.py` — SHA256 `bf2d535fe8eb1a83a7e3c92751a5baeaf19bb7d3abef72bb3db964b8e36ba041`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_bind_cx1v006.py` — SHA256 `3db8c72a36a1574ba0908da323effe49ded106aecc1c67f8a76152b6b54ad9cb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_direct_preflight_cx1v001.py` — SHA256 `eee61ac61ff93a11c97b9fdd3d6340661f17a92394653e524ac1cd8648d20fd1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/SYNTH_V007/RESULTS.json` — SHA256 `87cdbd59d322feb08f2e6705b46a2d6bb4b126ed36b805c394574177af81cb17`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/EXTRA_V005/RESULTS.json` — SHA256 `13f095443161cd8323767f978d657b806a03b6ffae4d0f1402ab10dd0fc26a80`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/DIRECT_V004/RESULTS.json` — SHA256 `caccf3ec67f1447022495de044a549493155be4e149c31e82350b97a148bead0`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/FIX0625_V003/RESULTS.json` — SHA256 `3eedfcebb2e9490d485f91831b4034b8d9bdaa1fdcade8e59d322505e64bac39`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/NATIVE_IMPORT_V002/RESULTS.json` — SHA256 `d5f2840390d52cc98a737f2ad790b12df94ce5a39bac6c29296e2d231829a767`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/review/NATIVE_IMPORT_INDEPENDENT_V001/RESULTS.json` — SHA256 `8229c74ed9f63c9ee2005dce37b24e6dfe59d1ece2d6046eb1cf9e59347f1efc`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX2/0513_2026-10-18_step4_successor_review_finished_ni3_open.md` — SHA256 `c4a656ecfc5944295a6eaf814631bbbba7e4629fa86438f6ae1e82e7f5878399`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/BUILD_CX1V001.md` — SHA256 `1c0a9011f952f870284be183da4812a6a52fdd4e8fc1ab46fc7557947e387110`
