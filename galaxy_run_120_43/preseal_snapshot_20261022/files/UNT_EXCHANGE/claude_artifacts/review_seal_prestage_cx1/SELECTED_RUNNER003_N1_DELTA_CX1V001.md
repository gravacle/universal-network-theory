# Selected runner003 N1-only delta CX1V001

date -u: `Sun Oct 18 22:34:00 UTC 2026`

**PASS — SA-CX1-N1 closed in this scoped delta. Zero blocking findings in the requested runner003 change.** Selected runner source SHA256 is `2b040e94a2b74eae981485288471376b86be0784a0a50b59093312c4fd87bf73`. This does not approve a real seal or close pending0642/v003 integration.

## TESTED source delta

The runner was read once into an immutable snapshot after its digest matched SELECTED_SEAL_PRESTAGE_C3SA_c3v002.json. The only executable AST change from runner002 is UnpinnedSiblingGuard.find_spec; comments also change. Removing that method from each module leaves identical ASTs. No main/parse/read_pinned/exec_buffer behavior changed.

Runner002 checked dirname(spec.origin) for equality with a guarded directory. Runner003 lines82–88 checks both origin and all submodule_search_locations for equality with or descent under a guarded directory, with a slash boundary. A regular sibling package's __init__.py and a namespace package's search location are now covered. A string-prefix sibling directory is outside the guard, as intended.

## Own TESTED controls: 8/8 PASS

1. The prior inert sibling-package payload (would return41 if executed) now raises UNPINNED_SIBLING_IMPORT_REFUSED.
2. An inert sibling namespace package with no __init__.py is refused before its leaf payload can return43.
3. A pinned sibling module executes the verified source despite a deliberately different timestamp-valid pyc.
4. An unpinned flat sibling module still refuses.
5. An inert external module in guarded_sibling/ is allowed while guarded/ is the guarded directory, confirming slash-boundary behavior.
6. A previously unloaded standard-library calendar import is allowed and executes successfully.
7. Actual process nice priority is at least10.
8. Exact AST comparison confirms only find_spec changed.

Only the copied runner and small new inert programs were executed. No original root script, helper semantic suite, comparator or scientific program ran. The 21 helper-semantic cases, B1 and B3 were not repeated.

## Scope and remaining work

This closes the reported regular-package gap and its namespace-package counterpart for the requested import paths. It is not a universal proof for every Python import mechanism, arbitrary concurrent filesystem replacement or preloaded module state. No production bypass or production mutation is asserted.

Root owns selected-manifest and script-diff checks. Dispatch0642 still requires the output-root creation and exact15-row producer allowlist integration, plus the separately requested convenience watchdog. V003 publication/wiring and the previously documented revision/old_section object-pointer alignment remain pending. The selected runner improvement does not change any of those requirements or remove the script's pending-tool refusal.

No real protected metadata, targets/observed velocities, session logs, network or git writes. All review writes were exclusive new files under the assigned directory; Python used the prescribed isolated interpreter, nice10 and single-thread BLAS.

## Byte pins

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/selected_runner003_snapshot_v001/SNAPSHOT.json` — `cdcd2a62331aca9a1d5d36c3397d40589c51cd24a0f48abc3d582216ee01362a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/selected_runner003_snapshot_v001/SELECTED_SEAL_PRESTAGE_C3SA_c3v002.json` — `32502ffc93ef82dae2ce869c24505da1a72060390033b1b674c067d31fd0e4ca`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/selected_runner003_snapshot_v001/runner.py` — `2b040e94a2b74eae981485288471376b86be0784a0a50b59093312c4fd87bf73`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/selected_runner003_snapshot_v001/0642_2026-10-18_claude3_script_add_RP_S1_W7_S1.md` — `b96f14fb3116cb277ff4b14ebf7e51f0c73ad8de1333464aa783cd799ad9ea74`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v002/run_pinned_c3sa_c3v002.py` — `b57e4859c498bf57e05706dcd83d89db0f14102c33aec7359580c155d924861c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/runner002_controls_v001/RESULTS.json` — `5b954e5a2bfe848861fca260d39ebcfffb4e5a0ab8e573b061a2fd6189ab7300`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/runner003_controls_v001/RESULTS.json` — `72edd819b3f23868c732ef1d8934be7b2a1c8d8c40e83ddd76df5b461700503d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/review_runner003_cx1v001.py` — `6f657e23daec258713ed3c22aa0a20a4853d2a3c740eaf2a819f057a8dce2c81`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/SELECTED_HELPER_SEMANTICS_CX1V001.md` — `19ab7247a075085d160d6085d4f13ec7510a7aa70f58f33fd941fdba7bb4ca5a`
