# Step4 current versioned package review — FAIL

date -u: Sun Oct 18 20:48:26 UTC 2026

**TESTED: four blockers in guard v005 / binder v004 / launcher v005 / direct adapter v001.** The0623 enabled-schema defect is closed; these are separate source-custody and loader issues. The package is still being published. This review names exact bytes and does not claim a final package is frozen.

- **S4-GUARD-METADATA-1 — BLOCKING:** safe_path resolves before rejecting lexical protected components; forbidden metadata may be touched before refusal. Inert Path tests establish order; no actual protected path accessed.
- **S4-BINDER-PIN-1 — BLOCKING:** Binder and launcher execute adjacent guard through unchecked module loader at top level before any expected guard hash check. Later admission cannot prevent already executed code. Four versioned inert bootstrap controls confirm.
- **S4-BINDER-REREAD-1 — BLOCKING:** Binder emits a later raw plan reread without comparing it to validated digest. Own in-memory change produces different emitted/validated plan bytes under TESTED binding. This is not a demonstrated bypass of later launcher admission.
- **S4-NATIVE-LOADER-1 — BLOCKING:** Native certificate custody loader uses SourceFileLoader, which probes .pyc even under -B. Source fence rejects that probe with UNPINNED_PREFLIGHT_SOURCE. Owned inert module reproduces; exact hashed-byte compile passes. Current empty policy registrations stop earlier; this defect blocks the otherwise compatible-policy path.

Recommended correction boundaries: reject lexical/protected traversal before filesystem resolution; verify expected guard bytes before bootstrap execution and compile that same buffer; bind only the verified plan buffer; replace cache-probing native custody loading with a reviewed hash-then-compile path while retaining the source fence. No reviewed producer file was edited.

Four scoped SHOULD_FIX items:
- **S4-TRANSITIVE-PIN-1:** Source fence checks transitive .py membership, not the stored hash at import time; prehash plus explicit load rehash narrow but do not close later-change exposure. No wrong-byte native execution shown.
- **CX2-S4-LIFETIME-1:** Injected worker interruption closes machine lock and ends worker-tied sleep assertion while detached monitors may remain active; live OS behavior untested.
- **CX2-S4-LIFETIME-2:** Lost assertion stops new starts but existing monitors drain without replacement sleep protection.
- **S4-SCHEMA-DOC-1:** Stale mode-versus-enabled comment remains although enabled/runtime schema behavior is fixed.

What passes: enabled=true/omitted-DIII schema paths; duplicate/nonfinite JSON refusal; strict gate booleans and empty reasons; explicit certificate-policy, point-certificate, sensitivity and prelaunch order; required sealed ADOPT_TAIL linkage under inert native seams; binder exclusive writes, prefix preservation and no self-published admission digest; ordinary launcher memory/ramp/cap/admission-recheck/no-retry behavior. The v005 direct adapter initializes the four fields consumed by its prelaunch-only native method contract and removes v004 campaign-volume construction. It is not a full campaign Context.

Evidence:64 guard/binder controls,38 native-interface/loader assertions,97 launcher controls across13 inert scenarios, and186 earlier schema controls. Launcher v004/v005 differ only in guard filename; all11 function ASTs match. Parent rehashed82 component-manifest entries. Passing fixture assertions include those that deliberately reproduce the defects; they are not scientific gate passes.

**UNTESTED:** complete native execution, actual policy/certificate/configuration availability, final package admission, live OS signal/lock/priority behavior and scientific readiness. Pinned adoption/sensitivity registration sets are still empty; those pending dependencies remain separate from the loader defect. No real process, launcher CLI, native scientific module, target data, protected run metadata or network was executed/accessed. Only source inspection, inert AST fixtures and an owned inert module loaded by the standard library were used. Default priority follows the acknowledged waiver; isolated Python and single-thread environment.

Harness notes: guard/binder v001 had a reviewer assertion matching export in a comment; v002 corrected it. The parent first manifest parser rejected a non-hash date header before writing an output; its corrected parser verifies hash entries and retains headers. Preserved artifacts identify both histories.

Byte-pinned scope/evidence:
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_guard_cx1v005.py — SHA256 11a31edd2cbbb0adb6738360bacecc6363b5cada4f91c0cd976276fd72c7e2d8.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_bind_cx1v004.py — SHA256 7f7add8545f95f4a3f0881dada86259911e8f43b0aa2073abeb186dff29613cd.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_launcher_cx1v005.py — SHA256 f9e4888dc8fc5c638581730651a7e19f0945fd7fa89a7f32391298f20dd0a66b.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_direct_preflight_cx1v001.py — SHA256 eee61ac61ff93a11c97b9fdd3d6340661f17a92394653e524ac1cd8648d20fd1.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/guard_binder_v004/REVIEW_GUARD_BINDER_CX2V001.md — SHA256 c3531e39f032ff2f6b5d29f23dfc8f8593efac8258eaefd1eb1f36dc7c034313.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/native_interfaces_v005/NATIVE_INTERFACE_REVIEW_CX2V001.md — SHA256 1131f3d1ae99dc2254e653c0578cdfd333ca22c5e57c1091d336fdce47d87bbb.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/launcher_v004/REVIEW_CX2V001.md — SHA256 1ce35e6ad69e628b82e5fed1f510034dbd4a24c840fe33e8271c13afa30abfbd.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/launcher_v005/ADDENDUM_CX2V001.md — SHA256 48c922fe329d25f60e866b7d8a0003bcd216b1f432e79ff93610b05d5b8024ef.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/guard/step4_v004_schema/REVIEW_CX2V002.md — SHA256 45f2b614ad9b42b89fb662137e476e495da5c2483cc23ce57d8c948ff264059e.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/package_v005/MANIFEST_VERIFICATION_CX2V001.json — SHA256 d8cf25739f0e250c6d4e0d02e91ea13c74a1ea4039df19cce24137fca097254a.
- /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0623_2026-10-18_codex1_step4_guard_schema.md — SHA256 3cf31cd8299d75aac555eefa6591ab306f48aec0a9b8205c3d43369df1267cc1.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/package_v005/FINDINGS_CX2V001.json — SHA256 69ff10f95b35a5910b2e33e55943d6c40f2dc8dcaf2af4c4d316b017e900aa74.
