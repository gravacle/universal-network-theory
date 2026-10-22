# Unselected script007/helper009/runner002 delta CX1V001

date -u: `Sun Oct 18 22:24:46 UTC 2026`

**PROVISIONAL only. No SELECTED tuple found at snapshot creation. No final seal approval.** Snapshot inputs were read once into exclusive new files before execution or extraction. Script007 still declares PENDING_V003__V001_PLACEHOLDERS and step0 refuses; the final tool interface/publication is pending.

## TESTED targeted correction results

- B1/B2: 5/5 PASS on helper009. The inert alias into an owned protected-name dummy directory is refused without any target stat/lstat/readlink/listdir/scandir call. Fence source bytes execute despite a deliberately different timestamp-valid inert pyc; wrong source hash refuses. Actual nice>=10.
- B3 envelope: 11/11 PASS with helper009's new pinned table-bytes input supplied from invented fixture text. The exact object succeeds; legacy bare-list/dispositions/rows, wrong or absent schema/frozen pin, extra top key, non-list entries and wrong file hash refuse.
- Same-file arguments: 2/2 PASS. Exact copied step2, renamed step4a and step10 bodies call only inert replacements; tool1/3/4 and per-step checks receive the same disposition path+sha. A deliberate path rebind between steps2 and4a is detected. This establishes copied-function argument transport, not actual tool IO.
- Runner002: 5/6 PASS. Correct pinned sibling source overrides stale pyc, wrong module/main pins refuse, and unpinned flat sibling import refuses. One conditional guard gap is below.
- TESTED source syntax: bash -n passes script007; no script execution. Script helper, runner and fence pins all match the copied bytes.

Prior B1/B2/B3 defects are corrected within these targeted snapshot controls. This does not certify the unfinished tool integration or whole seal procedure.

## New conditional finding SA-CX1-N1: package-form sibling bypass

Runner002 UnpinnedSiblingGuard.find_spec checks only whether dirname(spec.origin) equals one of the pinned program/module directories. An unpinned flat sibling origin shares that directory and is refused. An unpinned sibling package origin is package/__init__.py; its dirname is a subdirectory, so the guard returns None and Python executes it.

TESTED inert main importing a newly created sibling package returned its payload marker41 instead of refusal. Nothing came from author or scientific data. This falsifies the runner's blanket 'an import of an UNPINNED module that lives beside a pinned file is refused' claim. The current observed seal-tool sibling imports are flat; no actual production bypass, mutation or unpinned package import is claimed. Treat as a conditional loader-hardening finding pending the selected import graph. A correction should check origins/search locations under guarded directories, account for approved pinned modules explicitly, and include a sibling-package negative. Do not block standard library/third-party imports outside guarded directories merely by expanding the check indiscriminately.

## TESTED source connection audit; limits

Script007 pins helper009 and runner002 and uses the runner for tool main programs plus explicitly ordered sibling modules. Runner002 reads all pinned buffers before execution and compiles those buffers; helper009 load_pinned likewise compiles the buffer returned by its no-follow reader. The script supplies a fresh empty pycache prefix and checks it remains empty. These changes address the earlier flat-module/fence bytecode concern at those inspected boundaries.

H still invokes helper by pathname, and runner itself is invoked by pathname after separate shell hash checks. Therefore this review does not assert an atomic source-buffer handoff across the outer shell entry boundary or immunity to arbitrary concurrent path mutation. No live path mutation was attempted.

path_resolution_c3sa.py is a standalone old read-only probe, with no reference from the copied script, helper or runner (verified by source search). It was snapshotted for the requested connection audit but never executed. Its legacy resolve/importlib behavior is not in this copied executable graph.

Script tool order is now tool1 after freeze, tool3 at step4a directly after sealed prereg, then tool2 at step5a after sealed compare. Disposition file propagation remains exact in the inert capture. Semantic changed-entry D05 evaluation is owned by the other local helper; this report does not duplicate or certify it.

Source AST delta (helper007→009):
- Added definitions: _cited, _lexical_veto, load_pinned, nofollow_walk, read_nofollow
- Removed definitions: none
- Changed definitions: _dispositions, _exec_module, _fence, c_check_tool4, c_gates_only, c_rehash, c_row_scan, c_same, main, path_policy, pin, write_x

Harness provenance: regress_disposition_contract_cx1v004 stopped before shell extraction because the author renamed step6_tool3 to step4a_tool3. The complete v005 run uses the inspected new name; both artifacts remain unchanged. This was reviewer adaptation, not an author defect.

No real root script or comparator execution; no protected run, observed-target, session-log or network access; no scientific process. All Python isolated, nice10 and single-thread BLAS.

## Byte pins

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v002/SNAPSHOT.json` — `8b25608fd5310a17db99f7bece16c4b76532b7379f359a0bb08b59a73f110306`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v002/script.sh` — `e7409d93d17cdcde0e113ba971233fb59ade77157e2fe0b4a0c91f6b20b985cb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v002/helper.py` — `000798141398d27308d95e7a25fc64d17abe9831c47a2b27457439b7bc7922a3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v002/run_pinned_c3sa_c3v002.py` — `b57e4859c498bf57e05706dcd83d89db0f14102c33aec7359580c155d924861c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v002/path_resolution_c3sa.py` — `69a74b9418deb9c3268b437a9c13fba38e28700472ccf3904ce250f0f84532fe`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v002/fence.py` — `9c62ad4902c895f0aeeba3a78976b5944146ee0de153989dbc79470528dd2863`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/fix009_controls_v001/RESULTS.json` — `3f90474bd6e1e56bb00cd898cb256c6b11a77f53cb2dae558958d4be91a6daad`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/contract009_controls_v002/RESULTS.json` — `2bfdfb51dbbc6922901b19fe7cf852b63aa8dfa23bf29b78cbeec0a314f1f170`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/runner002_controls_v001/RESULTS.json` — `5b954e5a2bfe848861fca260d39ebcfffb4e5a0ab8e573b061a2fd6189ab7300`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/regress_fix_delta_cx1v002.py` — `b74e1ff43116b0ec1e2fc97243838f924f26848d3347b30fd08bac369c21a22a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/regress_disposition_contract_cx1v004.py` — `b0fbd530845c1389c9cf0ba109234ef193b8857c37b77a54a7956e8148d6349d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/regress_disposition_contract_cx1v005.py` — `30fe79a4dbb2c11737fe10258015538d5de4db15f3e7a6f14638de9eb43f094a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/review_runner002_cx1v001.py` — `35bb627787846813734052e68afe20e98e410e533faf7c805b0e883738c67f4e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v001/helper.py` — `2f08fb88c17dbe340fe5f03da10ed510aff384cdb404d8e3d9544664d2d79172`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v001/script.sh` — `cb3aeb324067910acdd9be5730e70305c819df4327ba00465aeae89249d3ed34`
