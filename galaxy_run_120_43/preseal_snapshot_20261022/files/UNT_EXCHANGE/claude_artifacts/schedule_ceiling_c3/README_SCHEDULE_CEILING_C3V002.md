# Phase-2 schedule-ceiling writer: README C3V002 (backlog #8; V006 A272 open item; A253 interface)

**Author:** Claude3. **Reviewer:** Claude4 (0871). c3v001 (`d8db59ce`) was reviewed PASS with 0 blocking (Claude4 0258). c3v002 applies that review's NOTEs S2–S4 (deputy D035) and needs a delta review. It is not adopted until root rules.

- `schedule_ceiling_writer_c3v002.py` — `6b773463c7fbfa98bcbc1c1aa399ce08936ee36bcaf8731144d265e4d3139994`
- `test_schedule_ceiling_writer_c3v002.py` — `da315a5dc42b0e5aee7f8564792e3deac2ea7713b46713e62d182842b2601833`
- `TEST_RECORD_SCHEDULE_CEILING_C3V002.json` — `d39f5b4bc1d702a0c4988a47f3638936738a0be244ef31a6b5ef150240d1d941` (33/33, 5 of 5 mutants killed, `$PY` 3.12.14)
- c3v001 stays as reviewed; use c3v002 once its delta review passes.

## What changed from c3v001 (the whole delta)

| NOTE | Change |
|---|---|
| C4-S2: one closure per call | `close` refuses `CLOSURE_ALREADY_IN_FOLDER:<name>` when the records folder (the folder of `--out`, read flat, `*.json` only) already holds a closure of the phase whose call has the same consumer `_call_key`. A `.json` entry there that is a symlink, or is not regular, unreadable or a malformed closure, also refuses: `FOLDER_JSON_NOT_REGULAR`, `FOLDER_JSON_UNREADABLE`, `FOLDER_CLOSURE_MALFORMED`. Other JSON files, such as call bindings, and non-JSON files are ignored. |
| C4-S3: temporary folders | The validation copies go in a new private (0700) `tempfile.mkdtemp` folder, never beside root's records. If that folder would fall inside the records folder (for example, TMPDIR pointing there), the writer refuses `VALIDATION_DIR_IN_RECORDS_FOLDER`. A crash can no longer leave a hidden folder among root's records. |
| C4-S4: phase scope | Only `PHASE_2` is in scope (`PHASES_IN_SCOPE`). `PHASE_1` refuses `PHASE_OUT_OF_SCOPE` for both commands. If root wants Phase-1 closures, the successor changes that one constant plus tests S4a and S4b. |
| Refactor | `read_pin` = `read_regular` (O_NOFOLLOW, S_ISREG, cap, fstat stability, unchanged) + the sha check, so folder entries are read the same way. |

Nothing else changed. The consumer pin, the record shapes and the date checks are byte-identical to c3v001.

## Root procedure (C4-S1)

`interruption_policy` checks shapes, dates, the registration binding and duplicates within one policy. Three checks run only when the roster is built (`_ceiling_or_hold`, roster builder L4778–4782): the call against the registry, the last receipt against the call's real last attempt, and the closure dated after that attempt ended. Root therefore:
1. closes only calls that are **stopped**, with no live attempt;
2. takes `--call` from the call's launch-registry binding `{alternative, kind, key, theta_sha256, spec_sha256}`, copied exactly;
3. takes `--last-receipt` from the call's last `<run>.attempt_receipt.json`; uses `--no-last-receipt` only for a call that has no attempts;
4. writes all closures into the one records folder, so the S2 check sees them all;
5. runs the roster builder right after writing the closures, so any roster-time refusal shows at once.

## Commands (root)

```bash
W=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/schedule_ceiling_c3/schedule_ceiling_writer_c3v002.py
# before the ceiling, once (date_u must be no later than the ceiling):
"$PY" -I -B "$W" register --phase PHASE_2 --out <FOLDER>/SCHEDULE_CEILING_REGISTRATION_PHASE_2.json
# at or after 2026-12-01T05:59:00Z, once for each stopped registered call that is not terminal:
"$PY" -I -B "$W" close --phase PHASE_2 --registration <REG> --registration-sha256 <H> --call <CALL_BINDING.json> --call-sha256 <H> \
      (--last-receipt <RECEIPT> --last-receipt-sha256 <H> | --no-last-receipt) --out <FOLDER>/SCHEDULE_CEILING_CLOSURE_<key>.json
```

## Folder (A272 asks root to rule it)

**Proposal, unchanged:** `<p112_launch_root>/SCHEDULE_CEILING_PHASE_2/`, on the internal disk beside the P112 launch records. Root creates it empty. The registration goes in early; the closures go in at 2026-12-01T05:59Z or later. Root then names the registration and the closures in the PHASE_2 `INTERRUPTION_POLICY_C2V002`. Claude4 0258 found this proposal sound, subject to S3, which c3v002 now meets.

## Tests (33)

- **T1–T4** and **F1–F11**: as in c3v001. The F cases now use a third call, CALL_C, which has no closure, so the S2 scan cannot mask them.
- **S4a/S4b:** PHASE_1 refused for `register` and `close`.
- **S2a:** a second closure for CALL_A in the same folder is refused. **S2b:** the same call in another folder is written, and other JSON and non-JSON files are ignored there. **S2c:** the consumer still refuses a policy naming both (SCHEDULE_CEILING_DUPLICATE), as a backstop. **S2d/S2e/S2f:** an unreadable, a symlinked and a malformed-closure `.json` in the folder each refuse.
- **S3a–S3e:** the validation folders are created outside the records folder and removed; the records folder is unchanged while the consumer runs; a simulated crash inside the consumer run leaves it clean; a TMPDIR inside the records folder is refused.
- **Mutants:** M1 no consumer run (F6 passes); M2 no S2 scan (S2a passes); M3 no phase scope (S4a passes); M4 validation folder back inside the records folder (S3b sees it); M5 no S3 guard (S3e passes). All 5 are killed.
