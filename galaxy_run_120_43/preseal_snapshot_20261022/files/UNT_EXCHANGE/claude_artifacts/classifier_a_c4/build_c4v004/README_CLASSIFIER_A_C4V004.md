# Classifier A (lane Claude4), build c4v004: the narrow V-N1 successor of c4v003

**What it is.** `classifier_a_c4v004.py` is classifier A (ROOT_ITEMS M-12, Implementation A) for the r3a text of record. It is `classifier_a_c4v003.py` (`394a8b61…`, verified 0 BLOCKING, Claude4 0225) with one behaviour change: root ruling **A168 V-N1** (root dispatch 0742).

The ruling: a frozen `stage0_status` block from the STAGE0 successor's exception path (`STAGE0_RECEIPT_RULE_EXCEPTION`) is taken at the module's own reading, NOT_EVALUATED_BEFORE_FREEZE [STAGE0_RECEIPT_NOT_FINISHED, NO_SEALED_SUCCESSOR]. The classifier reports the producer of record and does not reinterpret it.

Everything else is c4v003 as built and verified: the text of record, the phase1 pins (d64351ec, 7d891ff7), the successor binding (d260ee30), every input contract (C1–C9 as re-adopted in A168), the output schema and every other rule. Classifier B (Codex1) is built separately; nothing of B was opened.

**Status.** Built and suite-tested on synthetic, target-free inputs only. Record run `SUITE_RESULTS_C4V004.json` (classifier `e92aa30e…`): **476 cases, 476 pass**. That is 449 regression cases carried from c4v003 plus 41 new cases (X01–X41). Exactly one regression output changes: the c4v003 verifier's probe VS14, which is the exception-path block V-N1 is about.

**Files** (sha256 in `HASHES_C4V004.txt`):

| file | role |
|---|---|
| `classifier_a_c4v004.py` | the classifier (stdlib only, Python 3.12); byte copy of `work/cls_c4v004_d01.py` |
| `run_suite_c4v004.py` | runs the six case sets (R1, R2, N2, N3, V3, N4), writes the results file |
| `SUITE_RESULTS_C4V004.json` | the record run |
| `suite/case_defs_c4v004.py`, `suite/build_suite_c4v004.py` | the 41 new cases (hand expectations with d260ee30 line citations and derivations) and their generator |
| `suite/SUITE_INDEX_C4V004.json`, `suite/cases/X01…X41/` | the new cases: `BUNDLE.json` (pins relative, to the base case's own files), the mutated documents, `EXPECT_SPEC.json`, `EXPECTED_OUTPUT.json` |
| `regression_c4v001/`, `regression_c4v002/`, `regression_verify/`, `regression_conv_r2/` | `cp -R -n` byte copies of the same-named build_c4v003 folders |
| `regression_c4v003/suite/`, `regression_c4v003/basis/` | `cp -R -n` of build_c4v003 `suite/` (the c4v003 cases, N3); `cp -n` of its three basis files, which the N3 bundles seal at `../../../basis` |
| `regression_verify_c4v003/cases/`, `…/cases_r2/` | `cp -R -n` of the c4v003 verifier's case folders (V3) |
| `regression_conv_c4v004/` | the R1, R2, N2 and V3 bundles re-pointed from build_c4v003 to these copies (`tools/convert_regression_c4v004.py`), with `CONVERSION_INDEX_C4V004.json` |
| `tools/run_fenced_c4ep1.py`, `tools/fence_c4v003.py` | the fenced runner and its fence `175b995b…` (byte copy). The runner's EXPECTED_BUILD and refusal message name build_c4v004; nothing else differs |
| `tools/make_cls_c4v004_d01.py` | writes the classifier draft from the c4v003 bytes by 11 exact replacements (refuses unless each occurs once) |
| `tools/convert_regression_c4v004.py`, `tools/compare_n4_c4v003.py` | the bundle re-pointing; a review aid that runs c4v003 and c4v004 on every N4 case |
| `work/` | `cls_c4v003_ref.py` (`cp -n` of c4v003, `cmp`-equal), `cls_c4v004_d01.py`, the dev runs, `n4_c4v003_vs_d01.json`, `copy_check_c4v004.txt`, fenced run logs |
| `PARTIAL.md` | the append-only progress log |

## How to run

```
<codex python3> -I -B B/tools/run_fenced_c4ep1.py B/classifier_a_c4v004.py BUNDLE.json OUT.json
```

No taskpolicy, nice or thread variables (A166, dispatch 0740). `OUT.json` is created exclusively. The entry point is `classify_bundle(bundle_path) -> bytes`.

The suite runs as `run_suite_c4v004.py RESULTS.json [--classifier PATH] [--freeze] [--sets R1,R2,N2,N3,V3,N4]`.

## CHANGES against c4v003

**Behaviour (one change, V-N1).**

1. **Exception-path block.** In successor mode (a Phase 2 whose seal pins d260ee30), `_stage0_block_facts` keeps every c4v003 check, in c4v003's order:
   - the sealed sha;
   - the manifest schema;
   - `BLOCK_KEYS` and `BLOCK_MODULE`;
   - `BLOCK_SUCCESSOR_SHA`;
   - `BLOCK_STATUS_RECORD`;
   - `BLOCK_DIAGNOSTICS`.

   It then calls the new `_stage0_exception_path`:
   - **Not a claim.** A block with no diagnostic starting with `STAGE0_RECEIPT_RULE_EXCEPTION` is read exactly as by c4v003.
   - **Claim in the module's form.** The claim is the only such diagnostic and the last one; it reads `STAGE0_RECEIPT_RULE_EXCEPTION: ` followed by a class name (`str.isidentifier()`); and `rule_a_receipts_finished` and `rule_b_successor_sealed` are both the JSON value false. Such a block is an **exception-path block**.
   - **Claim not in the module's form.** Any other claim is a block defect with the word `BLOCK_EXCEPTION_PATH`. It reads TWIN_INPUT_DEFECT, stop FIELD_DEFECT_ALTERNATIVE, as every block defect does.

   On an exception-path block, `_stage0_facts(…, exception_path=True)` keeps every row and type check with one exception: a finished row may carry `before_step4` null, but a `before_step4` that is set must still equal (receipt time ≤ step-4 start).

   It drops the three receipt-rule recomputations a partial apply can violate:
   - rule (a) is taken as False, not `bool(members) and all(finished)`;
   - rule (b) is taken as False, not "sealed sha = the module's sha";
   - `receipts_before_step4` is taken as True, not "no finished row after the start". A block saying false is not the module's form and reads `RECEIPTS_BEFORE_STEP4`.

   It then requires the printed reading to be `_stage0_block`'s derivation from those flags:
   - reasons `[STAGE0_RECEIPT_NOT_FINISHED, NO_SEALED_SUCCESSOR]`;
   - reading NOT_EVALUATED_BEFORE_FREEZE;
   - no evaluation refusals;
   - `post_score_exploratory` false.

   Receipt refusals are allowed and do not change the reading.

   After the facts, the c4v003 checks still apply: `BLOCK_MEMBER`, members = the frozen PRIMARY members in order, and root's optional separate record = the block's exact projection.

   The printed STAGE0 status is the block's own reading and reasons, in c4v003's output form. The source is `FREEZE_MANIFEST_STAGE0_STATUS_BLOCK`, and the step-4 start and receipt times are as the block holds them (null where the partial apply never wrote them).

**Where the definition comes from (d260ee30, read by line range, never executed).**

The verdict and the exception path:
- **L3830–3836, the initial verdict.** `phase`, `sealed_successor` and `step4_start_utc` are null, and custody is false. Every PRIMARY member row starts as `{receipt null, custody_ok false, terminal_status null, written_utc null, finished false, before_step4 null, defects []}`. The flags start as rule (a) false, rule (b) false and `receipts_before_step4` **true** (L3835). Refusals and diagnostics start empty.
- **L3838–3843.** `_stage0_apply_record` runs inside `try`. `except Exception` sets both rule flags False and appends `'STAGE0_RECEIPT_RULE_EXCEPTION: %s' % type(exc).__name__`. That is the last write before `return v`.

The write order of `_stage0_apply_record` (L3713–3817):
- custody and phase (L3737–3738); a PHASE_1 record returns at once (L3739–3740), before any raise point;
- `step4_start_utc` (L3748);
- `sealed_successor`, rule (b), and the diagnostic `STAGE0_SEALED_SUCCESSOR_NOT_NAMED` or `…_IS_NOT_THIS_MODULE` (L3749–3755);
- `_stage0_registered()` (L3756, the slots read);
- the receipt refusals (L3761–3769);
- then, per member in order: MISSING/DUPLICATE or the receipt (L3771–3777); a read defect, or custody_ok, terminal_status and written_utc (L3787–3799); then IDENTITY_MISMATCH or NOT_FINISHED, or `finished` (L3812), `before_step4` (L3813) and WRITTEN_AFTER_STEP4 (L3815);
- **rule (a) (L3816) and `receipts_before_step4` (L3817) last.**

A raise leaves some prefix of this order. L3817 is the last statement, so it never completes on the path: `receipts_before_step4` keeps its initial True, and **RECEIPTS_AFTER_STEP4 is not producible on the exception path** (no RA4 case is reachable; X11 shows a block claiming it is refused).

The reading:
- **`_stage0_freeze_decision` (L3955–3963).** Evaluation refusals are computed only when `_stage0_eligible`, which needs rule (a), so they are `[]` on the path.
- **`_stage0_block` (L3853–3875).** The phase is not PHASE_1, so the reasons are RNF and NSS, the reading is NOT_EVALUATED (refusals are judged only when there are no reasons), and `post_score_exploratory` is false.

**Member-row states a partial apply can leave**, all accepted on the path:

| state | case |
|---|---|
| untouched (initial) | X01, X02, X03, X10 |
| STAGE0_RECEIPT_MISSING, no receipt | X06 |
| receipt pinned, a read defect (e.g. MALFORMED), custody false | X08 |
| receipt pinned, not yet read | X08 |
| custody_ok true, terminal_status and written_utc null | X05 |
| custody_ok true, terminal_status set, written_utc null | X06 |
| custody_ok true, FINISHED with a time, no defect, not finished (raise in the identity check) | X04 |
| completed not FINISHED (FAILED / INVALID) | X05, base S02 |
| finished true, before_step4 null (raise between L3812 and L3813) | X07 |
| completed FINISHED on time | X03, X09, VS14 |
| completed FINISHED after the start (before_step4 false), with `receipts_before_step4` still true | X04 |

**Contracts.** No input contract changes. The bundle, the roles, the root-written records and `STAGE0_STATUS_RECORD_C4V003` are as in c4v003 (C1–C9).

**Output.** No field is added or removed, and the schema strings are unchanged. Two things do change:
- one new value of the existing `defect` word in a block defect: `BLOCK_EXCEPTION_PATH`;
- on claim-bearing blocks, which reading prints:
  - an exception-path block now prints the module's reading (c4v003 printed a block defect: RULE_A, RULE_B or MEMBER_FINISHED);
  - a claim not in the module's form now prints a block defect (c4v003 printed whatever its facts gave, EVALUATED included: X12, X13, X39).

**Names.** `NAME = 'classifier_a_c4v004'`; usage text; docstring. The runner's refusal message names build_c4v004.

## Rule-to-function map (delta)

| rule | function(s) |
|---|---|
| A168 V-N1: when a block is an exception-path block; claims not in the module's form | `Run._stage0_exception_path` (constants `S0_EXCEPTION_PREFIX`, `S0_EXCEPTION_FORM`) |
| A168 V-N1: the module's reading on the path; the checks kept and dropped | `Run._stage0_facts` (`exception_path`), `Run._stage0_block_facts` |

Everything else is as in the c4v003 README.

## Open choices (raised, not decided; the value used and the pinning case)

These are carried from c4v003: OC-01–OC-49, with A168's rulings F1 (OC-41, vacuous), F2 (OC-36), F4 (OC-49) and contract re-adoption (C1–C9). New in c4v004:

| id | question the module bytes leave open | classifier A uses | cases |
|---|---|---|---|
| OC-50 | what "claims" the exception path | any diagnostic that **starts with** `STAGE0_RECEIPT_RULE_EXCEPTION`. A lower-cased or otherwise different string is not a claim, and c4v003's checks apply | X14–X20, X12, X13 |
| OC-51 | the class-name form after `STAGE0_RECEIPT_RULE_EXCEPTION: ` | `str.isidentifier()`: non-empty, no dot or space, non-ASCII identifiers accepted (a `__name__` written by a `class` statement) | X15–X17, X41 |
| OC-52 | "both rule flags false" | the JSON value false (`is False`), checked in `_stage0_exception_path`, so an integer 0 reads `BLOCK_EXCEPTION_PATH`, not `RULE_FLAGS` | X40 |
| OC-53 | which partial states the path can leave | **any prefix of the write order**: the clause catches every Exception, so any statement may raise. This is needed for VS14 (every row FINISHED on time, flags false: reachable only by a raise at L3816). It admits a finished row with `before_step4` null (X07). No ordering check across rows is added (processed prefix, then untouched rows); c4v003 has none | X03–X09, VS14 |
| OC-54 | diagnostics before the exception entry | not checked (c4v003 OC-43 extended). The module writes `STAGE0_SEALED_SUCCESSOR_NOT_NAMED` or `…_IS_NOT_THIS_MODULE` there when root's record named no successor or another sha | X09, X10 |
| OC-55 | `receipts_before_step4` false on the path | not the module's form: defect `RECEIPTS_BEFORE_STEP4`. RECEIPTS_AFTER_STEP4 is not derived from the flag | X11 |
| OC-56 | the order of the defect words | `BLOCK_EXCEPTION_PATH` after `BLOCK_DIAGNOSTICS` and before the facts. `BLOCK_KEYS`, `BLOCK_MODULE`, `BLOCK_SUCCESSOR_SHA` and `BLOCK_STATUS_RECORD` win over it; the facts' words, `BLOCK_MEMBER`, the PRIMARY members and the projection follow it | X21, X24, X25 |
| OC-57 | phase PHASE_1 on the path | a defect (`PHASE`), as c4v003 OC-40. The module returns on PHASE_1 before any raise point | X26 |
| OC-58 | the record path (no successor) | it has no exception path: `STAGE0_STATUS_RECORD_C4V003` carries no diagnostics, so a record projected from an exception-path block is checked by c4v003's recomputation | X36 (RECORD_DEFECT), X37 |
| OC-59 | a late FINISHED receipt in a partial block | read as the module does: no RECEIPTS_AFTER_STEP4, and `post_score_exploratory` false, though the row's `before_step4` is false | X04 |

Classifier B should share OC-50–OC-59, or root should rule on them.

## Findings (from the bytes; severity by the A115 rule)

- **SHOULD_FIX (OC-54).** The ruling and the brief say "the diagnostic string form MOD writes". That can be read as `diagnostics == ['STAGE0_RECEIPT_RULE_EXCEPTION: <name>']`. But the module can write `STAGE0_SEALED_SUCCESSOR_NOT_NAMED` or `…_IS_NOT_THIS_MODULE` before a raise at or after L3756, and L3756 (the slots read, `ValueError` on a pin mismatch) is the one raise point that needs no resource failure. A classifier with the exact-list reading would read X10's block TWIN_INPUT_DEFECT where classifier A reads NOT_EVALUATED [RNF, NSS]. Root should fix the form for both classifiers.
- **NOTE (OC-53).** The model of partial states is not fixed by the bytes, because any statement may raise under `except Exception`. A classifier that admits only "ordinary" raise points would refuse X07, X09 and even VS14. Those states need a raise inside an unguarded expression (in practice MemoryError or RecursionError), so they are not reachable from honest inputs. Root's V-N1 names VS14's state, which already needs the write-order model.
- **NOTE (reachability).** A block reaches a frozen manifest only if the writer's own structural check passes. That check is `_validate_manifest_structure`, L3111–3120, "writer and verifier share it" → `_stage0_manifest_check`, L3966. It recomputes the block from the pinned bytes with `frozen` and `pinned` set, and requires byte equality. So the same exception must recur at the same write point in the recompute. With V-N1's observation that every root-byte read is guarded, the path needs a repeatable environmental failure. No N4 state is reachable from honest inputs in normal operation. The change is a reporting rule, and it changes no physics reading: the block reads NOT_EVALUATED either way, and STAGE0 is never scored on it.
- **NOTE (tightening).** c4v003 did not read diagnostics (OC-43). A block that claims the path in a form the module cannot write was read by its facts: X12 read EVALUATED, X13 read NOT_EVALUATED [RNF], and X39 passed prescore. c4v004 reads such a block TWIN_INPUT_DEFECT (`BLOCK_EXCEPTION_PATH`), as the brief requires. None of these is producible by the module (the except clause forces both flags False).
- **NOTE (OC-55, OC-59).** On the path, a FINISHED receipt written after the step-4 start does not produce RECEIPTS_AFTER_STEP4, and `post_score_exploratory` prints false (X04). This is the module's reading, as ruled. A classifier deriving RA4 from the rows would disagree, but only on a block that is not reachable (see above).
- **No output change was needed.** The ruling is met within c4v003's output schema.

## The suite

The sets are synthetic and target-free. `SUITE_RESULTS_C4V004.json` (classifier `e92aa30e…`): 476 cases, 476 pass.

| set | folder | cases | pass | failing | oracle |
|---|---|---|---|---|---|
| R1 | `regression_c4v001/suite/cases` | 206 | 206 | none | c4v003's carried oracle (X1–X3, four overrides, Z1–Z4, its declared T087 change), then W1. Bytes equal on 205; T087 is compared by its declared spec and key equality, as in c4v003 |
| R2 | `regression_verify/cases_r3` | 92 | 92 | none | the c4v001 verifier's checks. Informational: bytes equal the carried c4v001 output except V71 and V85 (c4v002 fixes, unchanged) |
| N2 | `regression_c4v002/suite/cases` | 64 | 64 | none | hand spec and the c4v002 bytes carried by Z1–Z4, then W1. Bytes equal on all |
| N3 | `regression_c4v003/suite/cases` | 47 | 47 | none | hand spec and the frozen c4v003 bytes carried by W1. Bytes equal on all |
| V3 | `regression_verify_c4v003/{cases,cases_r2}` | 26 | 26 | none | the verifier's recorded c4v003 output (`OUTPUT.json`, 394a8b61) carried by W1. Bytes equal on all; VS14 against its declared, derived oracle |
| N4 | `suite/cases` (new) | 41 | 41 | none | hand spec written before any run, then the frozen bytes |

**Every changed expected output, with its reason.** Declared in `run_suite_c4v004.py` before the first c4v004 run on any regression case.

- **W1, every output.** `classifier` reads `classifier_a_c4v004` (brief item 3).
- **V3 VS14 (A168 V-N1), the only regression input that claims the exception path.** It has diagnostics `['STAGE0_RECEIPT_RULE_EXCEPTION: TypeError']`, both flags false, both rows FINISHED on time, and `sealed_successor` naming the module's sha.
  - c4v003 read it NOT_READ, with TWIN_INPUT_DEFECT and the block defect `RULE_A` (stop FIELD_DEFECT_ALTERNATIVE).
  - c4v004 reads it CLASSIFIED, with STAGE0 NOT_EVALUATED_BEFORE_FREEZE [RNF, NSS] from the block.
  - Its expected output is derived independently of the output under test: the c4v003 verifier's VS15 output (same base S02, an honest [RNF, NSS] block c4v003 already read), carried by W1, with VS14's manifest sha and its block's step-4 start (`2026-11-05T00:00:00Z`) and receipt times (`[2026-11-04T10:00:00Z, 2026-11-04T11:00:00Z]`). The output is byte-equal to that, and its 14-path spec passes.
- **Nothing else.** No other R1, R2, N2, N3 or V3 output changed: each is byte-equal to its oracle as carried.

**New cases (N4).** They were written from d260ee30's bytes in `suite/case_defs_c4v004.py` before any run. All 41 passed their spec on the first run; then `--freeze` wrote the bytes.

| group | cases | expected output |
|---|---|---|
| honest exception-path blocks (all rows untouched; before custody; each partial member state; all rows finished with a refusal and IS_NOT_THIS_MODULE; NOT_NAMED) | X01–X10 | NOT_EVALUATED [RNF, NSS] |
| a block claiming RECEIPTS_AFTER_STEP4 on the path (not producible) | X11 | `RECEIPTS_BEFORE_STEP4` |
| the exception diagnostic present with a rule flag true | X12 (EVALUATED block), X13 (rule (b) true) | `BLOCK_EXCEPTION_PATH` |
| a malformed exception diagnostic: no space, empty name, a space, a dotted name, not last, twice | X14–X19 | `BLOCK_EXCEPTION_PATH` |
| a non-claim: a lower-cased diagnostic on the VS14 state | X20 | `RULE_A`, unchanged from c4v003 |
| identity and structure checks kept on the path | X21–X28 | `BLOCK_SUCCESSOR_SHA`; `BLOCK_MEMBERS_NOT_THE_PRIMARY_MEMBERS` (order; one member); `BLOCK_MODULE`; `BLOCK_KEYS`; `PHASE`; `MEMBER_FINISHED`; `BLOCK_MEMBER` |
| a printed reading that is not the module's derivation | X29–X33 | `REASONS` (two cases); `READING`; `POST_SCORE_EXPLORATORY`; `EVALUATION_REFUSALS` |
| root's separate record in successor mode | X34 (exact projection: accepted), X35 (record with c4v003's recomputed flags) | X35: `STAGE0_STATUS_RECORD_NOT_THE_BLOCK_PROJECTION` |
| the record path (no successor), unchanged | X36, X37 | X36: STAGE0_STATUS_RECORD_DEFECT; X37: [RNF, NSS] from the record |
| prescore under the successor | X38 (VS14 state), X39 (claim with rule (b) true) | X38: PASS; X39: CLASSIFICATION_INPUT_DEFECT |
| an integer 0 rule flag on a claim | X40 | `BLOCK_EXCEPTION_PATH` |
| a non-ASCII identifier class name | X41 | accepted |

`work/n4_c4v003_vs_d01.json` (review aid) runs c4v003 on the same 41 inputs:
- V-N1 changes 31 readings.
- X02, X10, X20, X21, X24–X27, X36 and X37 read the same under both classifiers. X02 and X10 are honest exception-path blocks whose facts already satisfied c4v003's recomputation.

## Rule notes (self-reported; also in PARTIAL.md)

- **Python.** All Python ran through the fenced runner, with no taskpolicy, nice or thread variables. Every fence summary shows nothing opened or listed outside build_c4v004. No `python -c`, heredoc Python, system python or unfenced run.
- **Recursive commands.** The only ones used were `cp -R -n` of the named folders and `diff -rq` of each B3 folder against its copy (plus `cmp` of named files). No `find`, `grep -r`, `rg`, `ls -R` or `du`, and no walking loop. HASHES are computed from explicit paths (named folders listed one level deep; per-case files named by the suite and conversion indexes).
- **Edits before a first run.** Some files of mine were edited in place before their first run:
  - `tools/make_cls_c4v004_d01.py` (two line citations);
  - `suite/case_defs_c4v004.py` (X28's receipt literal; X38/X39 rebased from S24 to S02 with a prescore bundle; one docstring line);
  - `tools/compare_n4_c4v003.py` (shebang typo).

  The runner copy was edited as the brief requires. No file was edited after its first run. The classifier deliverable is a `cp -n` of the generated draft.
- **Files opened outside this build.**
  - the four briefs;
  - B3's README, PARTIAL, VERIFY_C4V003, run_suite, runner, fence and verifier r2 generator;
  - B3's classifier, by line range (read in full only via its byte copy);
  - B3 case files by jq: S01, S02, S14, S15, S17, S19, S20, S24, VS14, a T051 conversion bundle and the verify EXPECT files;
  - the module d260ee30, by line range: L3515–4010, L288–312, L1619–1660, L4185–4210 and L3110–3122, the last to settle the writer-check question above;
  - the V006 addendum, sections A154 and A168 only, through an awk section filter.

  Nothing of classifier B, and nothing under C/schema_c4v003/.
