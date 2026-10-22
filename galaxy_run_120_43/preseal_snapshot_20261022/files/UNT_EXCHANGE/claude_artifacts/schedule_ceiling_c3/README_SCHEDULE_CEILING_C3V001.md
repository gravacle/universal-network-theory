# Phase-2 schedule-ceiling writer: README C3V001 (backlog #8; V006 A272 open item; A253 interface)

**Author:** Claude3. **Reviewer:** Claude4 (0871). It is not adopted until root rules.

- `schedule_ceiling_writer_c3v001.py` — `d8db59ce5bd70ea50d990ee06a968069e667f879a6aaeff50e175010c46b07c4`
- `test_schedule_ceiling_writer_c3v001.py` — `4431a18f29ec32b2e73df21ad60b5a0f611a6c4570027ff7b5396cdf5cf4891b`
- `TEST_RECORD_SCHEDULE_CEILING_C3V001.json` — `b02a81684ece349d7a89796e9c6d927e996fbdbfaa72150771f9b676f87d4cdb` (20/20, `$PY` 3.12.14)

## The consumer contract (FORMAL)

The consumer is `cw8_phase1_cx3/roster_builder_c2v007_cx3cw8v003.py` (f710334b), pinned by full sha in the writer:
- `interruption_policy` checks the registration and the closures (L4590–4646).
- `_ceiling_or_hold` binds each closure to its call and its last receipt (L4762–4782).
- The PHASE_2 ceiling is 2026-12-01T05:59:00Z (L4598).

## Commands (root)

```bash
W=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/schedule_ceiling_c3/schedule_ceiling_writer_c3v001.py
# before the ceiling, once (date_u must be no later than the ceiling):
"$PY" -I -B "$W" register --phase PHASE_2 --out <FOLDER>/SCHEDULE_CEILING_REGISTRATION_PHASE_2.json
# at or after 2026-12-01T05:59:00Z, once for each registered call that is not terminal:
"$PY" -I -B "$W" close --phase PHASE_2 --registration <REG> --registration-sha256 <H> --call <CALL_BINDING.json> --call-sha256 <H> \
      (--last-receipt <RECEIPT> --last-receipt-sha256 <H> | --no-last-receipt) --out <FOLDER>/SCHEDULE_CEILING_CLOSURE_<key>.json
```

- `--call` is the call's launch-registry binding `{alternative, kind, key, theta_sha256, spec_sha256}`, exactly as the roster builder compares it.
- `--last-receipt` is the call's latest receipt. It is hashed and never parsed.
- Each record is validated by the unchanged `interruption_policy` on a private copy, which is then removed, before the exclusive write.

## Folder (A272 asks root to rule it)

**Proposal:** `<p112_launch_root>/SCHEDULE_CEILING_PHASE_2/`, on the internal disk beside the P112 launch records. The cw8 launcher requires `p112_launch_root` to be internal (L835).
- Root creates the folder empty.
- The registration goes in early, for example at the Phase-1 ceiling (2026-11-06T05:59Z) or when Phase 2 starts.
- The closures are written at 2026-12-01T05:59Z or later.
- Root then names the registration and the closures in the PHASE_2 `INTERRUPTION_POLICY_C2V002` that the roster builder reads.

## Tests

- **T1–T4:** register; close with and without a receipt; the consumer accepts both real closures.
- **F1–F11** (no output on any of them):
  - F1: a close before the ceiling;
  - F2: a registration after it;
  - F3: an extra call key;
  - F4: a registration sha mismatch;
  - F5: a wrong-phase registration;
  - F6: a registration dated late, caught only by the consumer;
  - F7: an existing out; F8: a relative out;
  - F9: a half pin pair; F10: no `-I -B`;
  - F11: a real-clock close before the ceiling.
- **M1:** removing the consumer run makes F6 pass, so M1 is killed.
