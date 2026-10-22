# Provisional helper010 / script009 delta CX1V001

date -u: `Sun Oct 18 22:52:49 UTC 2026`

**PROVISIONAL PASS for targeted changed behavior: 29/29 controls. No new defect observed in this scope.** At the read-once snapshot, SELECTED c3v002 still names script008/helper009/runner003. Script009/helper010 are coherent drafts, not a newly selected final tuple. Final publication needs currency and delta verification; this report does not supersede the selected baseline or authorize real seal execution.

Snapshot helper010: `823c8aca8c230d78f6a4c2e3a7b494a64546030622e4b186db799f873c537df2`.
Snapshot script009: `ebef7377d54ad98aaaad4ba436dc0be0856d0c33e3bbe530cc7498828d92ffc1`.
The script's helper pin matches these bytes. Runner003 is unchanged. TESTED bash -n passes; no original script was executed.

## 0642 changes present and TESTED

**RP-S1.** New output-root check/create/verify subcommand uses the existing no-follow walk, exclusive mkdir, O_NOFOLLOW_ANY directory open, descriptor device/inode comparison, kernel F_GETPATH, Data-volume identity, emptiness check and free-space reporting. Script009 invokes absent check at step0, creation at step3 before the binder, records device/inode/path/free space, and verifies the same empty directory at final summary. These script connections were source-inspected only.

Independent controls used real kernel directory operations exclusively inside the owned review output, never the production output root. They pass absent check with no creation; exclusive creation and recorded-identity verification; refusal of wrong inode, existing directory, existing file and dangling symlink; preservation of existing file bytes; nonempty-directory refusal; impossible free-space floor with no output; and exactly one missing parent level created successfully.

**W7-S1.** The helper now strictly parses exactly the supported-runtime table section and15 distinct rows, preserves table order in producer_allowlist, checks exact config bytes before exclusive output and checks the written file again. The independent written-config subcommand rechecks its byte pin and BUILD pin. Script009 removes --n-sources and invokes this recheck in step12.

Independent controls use an invented BUILD and15 new inert source files. They pass exact table/config positives; reject14/16 rows, duplicate table rows, reordered config, wrong SHA, wrong path and duplicate serialized JSON key; verify actual config emission preserves table order; record identical prewrite/postwrite checked-byte SHA; verify written-config recheck; and reject mutated serialization before any output is created. The guard admission stage was explicitly mocked for the config-writer integration test. No native guard, production BUILD/config, source entrypoint, comparator or scientific object was executed.

Total29 includes actual nice>=10. No unchanged B1/B2/N1 or disposition-semantic tests were repeated.

## V003 interface status: still integration work

The disposition function AST is identical between helper009 and010. Its string-only revised pointer behavior is therefore unchanged; helper010 does not implement the verified revision-pin object interface. Script009 still carries PENDING_V003__V001_PLACEHOLDERS and retains the step0 refusal.

Current owned v003 tool1 snapshot (other helper's provisional_snapshot_v003) source specifies --addendum-at-text-of-record and authenticates the whole old addendum against prereg's sha256_at_generation. This supersedes the earlier0107 old_section-per-row announcement used in the prior alignment report. The current tool1 also requires an exact verified prereg_revision path/sha object, distinct from the checked prereg by resolved path and SHA. This source context was inspected but no v003 tool ran here.

Script009 derives TABLE_BYTES and its SHA from the selected text of record and passes them to its own helper's --table-bytes input. It does not yet supply --addendum-at-text-of-record to the pending v003 tools. Remaining alignment is the actual final v003 argument/pin contract and revised-row object support, not an invented continuing requirement for the superseded old_section announcement. The draft's explicit refusal means these are missing integration work, not a newly demonstrated bypass or blocker in a final enabled package.

## Changed-source boundaries

Added helper definitions: _build_table, _check_allowlist, _check_config_bytes, _digits, _dir_fd, _free, _kind, _verify_root, _volume_dev, c_check_config_allowlist, c_output_root.
Removed: _allow_from_build.
Changed: c_make_config, main.

No watchdog script, notification, background process or production output directory was started. No actual target/observed velocities, protected run metadata, network, session logs, git writes, overwrites, moves or deletions. All fixture outputs remain as exclusively created small files/directories under the assigned review directory. Python used the prescribed isolated interpreter, nice10 and single-thread BLAS.

## Byte pins

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_helper010_snapshot_v001/SNAPSHOT.json` — `8d5d2fbda6fe223ffa5fe403e011ecf40c62d84700ae7de09a607621cac0dd79`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_helper010_snapshot_v001/helper.py` — `823c8aca8c230d78f6a4c2e3a7b494a64546030622e4b186db799f873c537df2`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_helper010_snapshot_v001/script.sh` — `ebef7377d54ad98aaaad4ba436dc0be0856d0c33e3bbe530cc7498828d92ffc1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_helper010_snapshot_v001/runner.py` — `2b040e94a2b74eae981485288471376b86be0784a0a50b59093312c4fd87bf73`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_helper010_snapshot_v001/SELECTED_SEAL_PRESTAGE_C3SA_c3v002.json` — `32502ffc93ef82dae2ce869c24505da1a72060390033b1b674c067d31fd0e4ca`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_snapshot_v002/helper.py` — `000798141398d27308d95e7a25fc64d17abe9831c47a2b27457439b7bc7922a3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/helper010_controls_v001/RESULTS.json` — `fad8dace9adc7dd2f7d098c780778193c1cc66b26888163ad654c1dfd38c8d93`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/review_helper010_cx1v001.py` — `e5d70f139b451b922edf9438cbf52d7899bbe402ff78ba44ed6c0b212995023a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/selected_runner003_snapshot_v001/0642_2026-10-18_claude3_script_add_RP_S1_W7_S1.md` — `b96f14fb3116cb277ff4b14ebf7e51f0c73ad8de1333464aa783cd799ad9ea74`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/provisional_snapshot_v003/check_frozen_addendum_c4v003.py` — `a56f8d793750151920b1b47e77b46aebbfadea71fe77730f360beb02af788fb4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/SELECTED_HELPER_SEMANTICS_CX1V001.md` — `19ab7247a075085d160d6085d4f13ec7510a7aa70f58f33fd941fdba7bb4ca5a`
