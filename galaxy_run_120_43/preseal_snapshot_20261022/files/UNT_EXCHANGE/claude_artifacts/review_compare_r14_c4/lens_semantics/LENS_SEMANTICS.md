# LENS 2: I4 after-seal token semantics (compare r14 delta review of record)

Claude4 helper, under dispatch 0651 and root entry A114 (V006). Written 2026-10-19T03:36:53Z (date -u).
Labels: **TESTED** means a synthetic check run under the review fence. **FORMAL** means read from bytes, not executed. **UNTESTED** means neither.

## Verdict

**There are no BLOCKING findings in lens 2.** r14's I4 token behaves as A114.1 rules.

- The token is accepted for I4.
- It is still refused at load for every gate the ruling names, and for every other gate outside the ten-gate set.
- Before a real I4 record exists, I4 never reads PASS and parallel8 route A is never licensed.
- No other gate's behaviour changes.

There are 2 SHOULD_FIX items (S1, S2). Neither needs an r14 change. Under A114 ("nothing else changes") and A115 they do not block. There are also several NOTEs.

**A115 was appended to V006 while this review was running.** At 03:20Z the V006 bytes were ca5d7ae3…; at 03:28:35Z they became 63e7802f…. A115 sets the blocking criterion for the r14 review: a finding blocks only if an honest pinned producer reaches it on real records, or if it could change a physics reading. The A114 text was re-read after the change and is unchanged (FORMAL). The severities below apply A115.

## Object, verified from bytes

Every pin matched its bytes.

| File | Verified sha256 |
|---|---|
| SELECTED_R14_CX1V001.json | dc74949d1d4f19336661f8ce85e9a85de0176837adad61c7a9585a147f933533 |
| r14 source | f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7 |
| FIELDS V002 | 2ce9f1c710bb16ad1224ab49ec0713dd4f3fd48a04d730c78cfc3ed0ffdb7fe4 |
| FIELDS V001 | a33b153b40e3a709cbbf095908007c737e90c3383e6a113d30c786732e800c83 |
| IMPL | 854cad0d269161bff1fc314cdb2801df000eeb0d94ea004ef659d62edfb44680 |
| VALIDATION | 930ca7bc78e74134aeac46851a6bbf9481e78f9ce3862b77d370b716dd8380ec |
| Author harness | 998e0c2eb7309fd2a2135bc27974b95899f2f3583116312ccb7476120a1555c6 |
| SOURCE_DELTA | 56a95b7ef983608b89b5f4c30799fa9ea578eb69c7e01ccb31de96b8bf92ec51 |
| HASHES V001 | 8b92153a0200953df2e4df8e1993cfcade58ddc4b6b5536439359a9119be5a8f |
| r13 source (the parent) | f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157 |

The r14 folder also holds `SELECTED_R14_CX1V002.json` (6b650ece…). It supersedes V001 for the IMPL binding only (COMPARE_V007_IMPL_R14_CX1V002.md, 2ba6d12e…) and pins the same source, fields, validation and harness. The lens-2 results apply to both selections.

## Method

The review read the named r14 paths:

- the constants, L332-342;
- the loader, L1102-1149;
- `gate_record_sha_codes`, L1176-1188;
- `required_gates`, L1309-1311;
- `g_I4`, L3741-3759;
- `evaluate_gate`, L3790-3878;
- the reading, L4528-4581;
- `read_gates`, L5528-5531;
- the FIELDS generator.

One script ran on synthetic inputs only: `tools/lens_semantics_tests_c4v001.py` (ca9c935c…).

- It ran through the byte-identical fence copies `tools/fence_c4v002.py` (c993d34c…) and `tools/run_fenced_c4st2.py` (fe904509…).
- Result: **60/60 checks**, in `out_v003/LENS_SEMANTICS_TESTS.json` (c1d70117…).
- Fence summary: selftest 8/8, exception probes 15/15, and `blocked_after_selftest: []`.
- Importing r14 and r13 tripped nothing.
- Runs v001 and v002 stopped on my own test-helper bugs (a function signature and a keyword clash). They are preserved, with no source change in between.

The script never called any of these: `main`, `build_context`, `read_run`, `read_all`, `read_gates`, `c5h_interlock`, `registered_identity_code`. Nothing touched a run tree or the C5H directory, not even a stat.

`evaluate_v007` was exercised through group 1 of the reading only:

- every case and identity run was stubbed VALID;
- `flag_rulings` was replaced by a sentinel. It is the first call after `dec['tests_read'] = True`, so the sentinel firing proves the T-tests would be read next.

## (a) Before the real I4 record exists (gate_records['I4'] = token, parallel8)

**The gate.** `evaluate_gate('I4', path)` with no path, a path that does not exist yet, or a directory gives `MISSING` with code `GATE_RECORD_MISSING:I4`. It never gives PASS (TESTED A1).

- SR_K under the token behaves identically (TESTED A1).
- The token in the registry only waives the record-sha check. It does not stand in for a record (FORMAL, L1183-1185 and L3794-3796).
- An empty or placeholder file gives RECORD_DEFECT, for example `GATE_RECORD_UNREADABLE:I4:JSONDecodeError` or `GATE_RECORD_FIELD_MISSING:I4:bitwise_equal` (TESTED A1).
- The `--gates-only` blinded view of a missing I4 reads MISSING (TESTED A1, `blinded_gate`).

**The reading.** These outcomes are TESTED (A3, A4, D6) and identical in r13 and r14.

| I4 state | parallel8 | serial_with_exemption |
|---|---|---|
| MISSING | INCOMPLETE, `CASES_OR_RECORDS`; the only reason is `gate record I4 missing`; next step "produce the I4 record before the T-tests are read"; T-tests not read | not required; the reading proceeds |
| FAIL | INCOMPLETE, "I4 FAIL […]: parallel8 route A not licensed"; next step `I4_NEXT` (switch to serial_with_exemption); T-tests not read | reported in `gates_failing_reported`; the reading proceeds |
| RECORD_DEFECT | NO_RUN | NO_RUN (`defective` loops over ALL_GATES) |
| PASS | the reading proceeds | the reading proceeds |

**Compared with SR_K and the other token gates** (TESTED A3, A4):

- **MISSING.** SR_K, I1T, T2I, SRB_ROT, RB_FP and EA (OTHER_REQUIRED_GATES) read INCOMPLETE in both modes. I4 reads INCOMPLETE in parallel8 only. MT, HARMONICS and FLAG_RULINGS are optional, so MISSING does not block.
- **FAIL.** SR_K FAIL does not block group 1; it is read in the T-tests by `sr_k()`. **I4 FAIL is stricter: it blocks parallel8.**
- **RECORD_DEFECT.** Every gate reads NO_RUN.

## (b) How a post-seal I4 record is bound

**Through the producer pin only (TESTED B1, B8).**

- The record must carry `schema` = GATE_SCHEMA and `gate` = 'I4'.
- `producer/{path, sha256}` must be a registered `producers['I4']` entry, matched by both realpath and sha. Its bytes must still hash to that sha at read time.
- Each failure is a RECORD_DEFECT:
  - another gate's producer, or an unregistered one: `PRODUCER_NOT_ROOT_REGISTERED_A62_2:I4`;
  - the same sha at another path: `PRODUCER_PATH_NOT_ROOT_REGISTERED_A69_1:I4`;
  - producer bytes changed after the registry loaded: `PRODUCER_BYTES_NOT_THE_REGISTERED_SHA_A69_1:I4`;
  - no registry at all: `PRODUCER_REGISTRY_ABSENT_A62_2:I4`;
  - no I4 producer registered: `PRODUCER_NOT_ROOT_REGISTERED_A62_2:I4`.

**The record's own sha is not checked.** The token waives it.

- The same record bytes read PASS under the token.
- Under a sha list naming another sha they read `GATE_RECORD_SHA_NOT_ROOT_REGISTERED_A67_N2:I4`.
- Under a sha list naming their own sha they read PASS (TESTED B1).
- The record's sha is *reported*, in the gate output `record.sha256` and in the blinded `record_sha256` (TESTED B1).

**There is no registry update.** The only registry is the pinned `PIN_PRODUCER_REGISTRY` in sealed mode, or `--test-producer-registry` in test mode. No code path adds a record sha after the seal (FORMAL, L336 and L5686-5735).

**The content clauses of g_I4 are enforced** (TESTED B14):

- `tail` must be ON;
- `driver_sha256` must be in every T-case's `drivers_allowed`. `validate_case_block` requires that list to be exactly the sealed driver (FORMAL, around L1519);
- `v8c_f1_fix_confirmed` and `bitwise_equal` must be true booleans, so a string "true" is a defect;
- `differences_outside_custody` must be [];
- the verdict must agree with the data;
- an unregistered verdict such as PENDING is a defect;
- so are a missing field, a wrong gate name, a wrong schema, a duplicate JSON key, and a wrong `numbers_producer` sha.

**Can a record that is not the I4 producer's output pass? Yes, if it names the registered producer** (TESTED B6, B7, B27).

- A hand-written record that copies the registered producer path and sha reads PASS when:
  - its `parallel_result_sha256` differs from the manifest's C2T result sha (`crossref` is {});
  - `serial_result_sha256 == parallel_result_sha256`;
  - it carries unread extra fields such as `n1_spec_sha256`.
- `g_I4` calls `xr()` zero times (TESTED P3).
- SR_K under A88 has the same producer-pin property: a hand-written SR_K record naming the registered producer also reads PASS (TESTED P1). But SR_K's states are pinned to the PIN_R3 shas, and a wrong state gives `SR_K_STATE_C4R3` (TESTED P1).
- SRB_ROT cross-references its run: a record not on C4T gives `CROSSREF_MISMATCH:SRB_ROT:c4t_result_sha256` (TESTED P2).
- Of the ten token gates, three bind no run result: I1T, HARMONICS and I4. SR_K binds pinned states instead (FORMAL, P3 counts).

**Under A115 this is a NOTE** (forged-input class) **with one cheap root check, S1.** The I4 verdict on genuine N1/N8 records is the honest producer's, and the missing cross-reference cannot change it.

## (c) The token is refused at load (TESTED C1, C2)

`producer_registry_from_obj` with `gate_records = {g: 'PRODUCED_AFTER_THE_SEAL'}` refuses with code `PRODUCER_REGISTRY_GATE_RECORDS` for each of:

B0, B0_FA, B0_N3, B0_RO1, B0prime_RERUN, B1, B1_OFF, B2, B3, EPS, GQ, LO, LO_NGC, DOUBLING. B0prime_DRY is refused as well.

- The file route `load_producer_registry` gives the same results.
- The accepted set is exactly the ten gates in r14 and exactly the nine in r13 (r14 minus I4).
- I4's token together with any refused gate's token refuses the whole registry.
- These variants are refused: lowercase, list-wrapped, a trailing space, `PRODUCED_AFTER_SEAL`, null, a dict, `true`, and the keys `i4`, `I4 `, `I4_`.
- I4 given both as the token and as a sha list (a duplicate JSON key) refuses with `PRODUCER_REGISTRY_DUPLICATE_JSON_KEY_A71`.
- **Hand-built registries that bypass the loader still fail closed.** `gate_record_sha_codes` returns `GATE_RECORD_TOKEN_NOT_ALLOWED_FOR_THIS_GATE_NEW52:<g>` for every gate outside the ten. r13 differs from r14 on I4 only.
- **A114's finding is confirmed in r13** (TESTED D9). r13 refuses the token on I4, and a post-seal I4 record under a sha list reads RECORD_DEFECT, so the parallel8 reading is NO_RUN.

## (d) Does adding I4 change any other gate? No (TESTED D1-D7)

- **The source diff r13 → r14 is exactly one line, L341.**
- **Every use of the set is a membership test or a joined string** (D7):
  - L1122: the loader's membership test;
  - L1184: `gate_record_sha_codes`, membership;
  - L1126: the refusal text, `'/'.join`;
  - L5172: the FIELDS text, `', '.join`;
  - L332 and L1106: a comment and a docstring.
- There is no loop over the set and no dependence on its order.
- **Loader and `gate_record_sha_codes` results are identical in r13 and r14 for every other gate**, under both token and sha-list registries.
- **The refusal code is unchanged.** The non-blinded text gains only `/I4`.
- **The generated field contract differs from r13's in that one joined line only.** It regenerates byte-identical to the published FIELDS_R14_CX1V001.md (a33b153b).
- **The reading is identical in r13 and r14** for every gate × {MISSING, FAIL, RECORD_DEFECT} × both modes: 0 differences.

## Findings

- **S1 (SHOULD_FIX, root procedure; no r14 change; NOTE-class under A115).** The I4 record's link to its evidence is not checked by the compare. A114.3 makes N8 the C2T T-run itself, but `g_I4` checks neither `parallel_result_sha256` against the manifest's C2T result nor serial ≠ parallel (TESTED B6, B7).
  - **Suggested cheap root check after the reading**, recorded with the seal disclosures:
    - `gates.I4.record` gives `parallel_result_sha256` = `inputs.C2T.result_sha256`, read from the comparison report;
    - `serial_result_sha256` is the result of the N1 companion run under the pinned N1 spec;
    - the two differ.
  - **The alternative** is a successor compare that adds `xr('parallel_result_sha256', …, 'C2T')`. That is outside A114's scope.
- **S2 (SHOULD_FIX, for V010 drafting and the seal record; r14 needs no change).** A114.3 says "the N1 spec sha is pinned in V010's I4 entry". r14's registry schema C2V003 has no field that can hold it.
  - A producer pin must be exactly {path, sha256}. An extra key refuses the registry with `PRODUCER_REGISTRY_PRODUCERS` (TESTED B28).
  - `gate_records['I4']` must stay exactly the token string. A sha list holding the N1 spec sha would make the genuine I4 record `GATE_RECORD_SHA_NOT_ROOT_REGISTERED`, a RECORD_DEFECT, and the reading NO_RUN (TESTED B2). That could change a physics reading.
  - Only `note` accepts it (TESTED), and the compare never reads `note`. Nor does `g_I4` read any N1 field (TESTED B27).
  - So: put the N1 spec sha inside the I4 producer's own bytes, which the registry pins, or in `note` plus a seal-record check.
- **N1 (NOTE).** The comment at L332-334 still says "every other gate (… the B-gates, I4) is registered by record sha", which is now false for I4 (TESTED D8). It has no behavioural effect. SOURCE_DELTA says the line was left alone deliberately under "nothing else changes"; correct it in a later round. L49 is an R8 history entry, not a statement of current behaviour.
- **N2 (NOTE, inherited, identical in r13).** A gates dict that has no 'I4' key at all lets the parallel8 reading pass group 1, because absent is not MISSING (TESTED A3 probe). The CLI never builds such a dict, since `read_gates` evaluates ALL_GATES (FORMAL, L5530 and L5830). Only tools that call `evaluate_v007` directly must pass every gate.
- **N3 (NOTE).** A partial or placeholder I4 file reads NO_RUN, not INCOMPLETE (TESTED A1). This fails closed. Name the I4 record in the manifest only after the producer has finished writing it.
- **N4 (NOTE).** The author's 12 A114 MUST checks test the loader only.
  - B0_FA, B0_N3, B0_RO1 and B0prime_DRY are covered only by the generic test `R12_ADAPTED_A88_TOKEN_ACCEPTED_ONLY_ON_THE_NINE_POST_SEAL_GATES`. That test checks the loader against the constant, and its name still says NINE.
  - No author test runs the token on I4 through `evaluate_gate` or the reading. This lens covers that ground (TESTED).
- **N5 (NOTE, provenance).** The A114 header stamps "2026-10-19 03:35Z", but its bytes already existed at 03:20Z (my first read) and r14 was built at 03:15-03:19Z. Likewise A115 says "~03:30Z" and was written by 03:28:35Z. These are not clock times.

## Not tested

- The real V010 registry and the real I4 producer.
- The N1/N8 runs.
- The full CLI and sealed mode. These would need run trees and the C5H interlock, which are outside the rules.
- The T-test phase of the reading. I4 is not referenced there; it appears only at L4450 and L4539-4545 (FORMAL).
- Seal tools that may import these constants.

## Files

All paths are under `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_compare_r14_c4/lens_semantics/`:

- `LENS_SEMANTICS.md` (this file)
- `PARTIAL.md`
- `tools/lens_semantics_tests_c4v001.py`
- `tools/fence_c4v002.py`
- `tools/run_fenced_c4st2.py`
- `out_v003/LENS_SEMANTICS_TESTS.json`
- `out_v003.stdout.txt`
- `out_v003.stderr.txt`
- `sandbox/v003/`: the synthetic producers, records, registries and regenerated FIELDS files
- `out_v001*` and `out_v002*`, with `sandbox/v001` and `sandbox/v002`: the failed attempts, preserved
