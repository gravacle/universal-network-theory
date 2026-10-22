# A79 addition to c2v007 identity-comparator review preparation

date -u: Sun Oct 18 17:14:00 UTC 2026

UNTESTED for c2v007; candidate BUILD.md is still absent. A79 item4 extends the independently TESTED compare-r10 NPZ logical-name finding to the identity comparator wherever it reads NPZ members.

Required controls after publication:
- Guard both raw ZIP names and the exact NumPy logical-name mapping before constructing a mapping or loading arrays.
- Reject any extensionless NPY member outright, even when it carries equal data.
- Preserve the concrete weighted_responses.npy / weighted_responses collision in both archive orders, with clean positive and ordinary unequal-value controls.
- Add equal-payload duplicates and byte-identical malformed archives on both sides when exercising a declared parsed NPZ path, to prevent raw-equality short-circuit from substituting for required strict parsing.
- Use owning-check evidence and a source-backed check mapping. An unrelated token/pin failure does not close the case.
- Keep the scope precise: A79 concerns paths that read NPZ members; opaque raw-only handling must be reported separately rather than asserted to exercise the parser.

The r10 fixture proves a hidden V5 failure only in its tiny owned packet context, not a production scientific reading. Port under new names and outputs; do not run the existing fixed-output script unchanged. No scientific launches, prohibited runs/receipts/targets, or reviewed-file edits.

## Cited byte pins

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/OPEN_RULINGS_SNAPSHOT_CX2V002.md`
  sha256 `4c68b462a419c2e4524fc6cb65e5c08040980bd070dd607db300c0783a7430f5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/a71/probe_npz_logical_alias_cx2v002.py`
  sha256 `cfb7756999b3d2927d7dabdf91a83b3ec3530ed8553211f624d32cbe0870208c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/a71/npz_alias_v002/NPZ_LOGICAL_ALIAS_CX2V002.json`
  sha256 `190c899030412bbe493fa6892cb39f83fd964119252998eb46609d59835b7e52`
