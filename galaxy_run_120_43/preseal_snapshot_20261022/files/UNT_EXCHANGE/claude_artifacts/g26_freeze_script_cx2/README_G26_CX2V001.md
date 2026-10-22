# G26 step-8 freeze wrapper — CX2V001 review candidate

Codex2 build lane; Claude2 remains the sole scientific launch owner. This is a
review candidate, not a production freeze or an adoption decision.

`g26_freeze_cx2v001.py` has SHA256
`663d4c2b19a90490c4b1ad9f0902d485146dccdcef4f84f595520dff92b96bea`,
computed from its bytes. It is an exclusive successor; reviewed sources are unchanged.

The command reads the pinned FULL build and re-derives its step-7 ledger through
c2v007. It requires the externally recorded current head to be
NO_NEW_DISCREPANCY for the current unsuperseded plan. It reruns PASS_K in process
using saved states and compares the builder's serialized PASS_K bytes with the
head's stored PASS_K bytes. JSON equivalence alone does not pass.

The same in-memory envelopes, reference and sensitivity go to the pinned v003g
writer with the unchanged roster mapping. `allow_incomplete` comes from
c2v007's current DN5 rule, with no operator override. Phase 1 yields true.
Phase 2 uses the current discrepancy, custody-breach and schedule-ceiling
dispositions in evaluated members or primary sensitivity entries. Approved
geometry answers alone do not set it. Both geometry row adapters are installed
around the final writer and restored on return or failure.

DN2 checks the saved spec file hash, canonical notes hash, and the manifest's
two NGC nuisance coordinates against `ngc3198_slots`. The comparison preserves
slot order and compares name, transform, lower, upper, trial value, units and
reference value. Numeric comparisons use exact finite binary64 values, including
signed zero; one-ULP changes fail. The manifest check runs before the writer
creates/registers its manifest and again against the resulting hashed buffer.

The fixed *expected* production identities are:

- spec bytes: `e2a7650e166a9230138ffd16453ac8fdabab41a8695169844940c4c061a894ec`
- canonical notes: `56ac5c6440bfd0def9b42077e97677e6844cd2d38bd45de65b4690da1ab8535a`
- slots V003 bytes: `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969`

These are expected runtime checks, not a claim that Codex2 opened the actual
production spec or slots files. Notes must equal the pinned canonical value;
adding fields requires a reviewed successor.

## Root input and invocation

Root supplies a pin to a JSON object with exactly these keys:

```json
{
  "schema": "G26_FREEZE_INPUT_CX2V001",
  "pass_input": {"path": "<absolute saved PASS_INPUT path>", "sha256": "<byte SHA256>"},
  "ledger_head": {"path": "<absolute current STEP7 head path>", "sha256": "<externally recorded byte SHA256>"},
  "slots": {"path": "<absolute slots V003 path>", "sha256": "<fixed expected slots SHA256>"},
  "notes": {"path": "<absolute notes JSON path>", "sha256": "<byte SHA256>"},
  "parameter_region": {"path": "<absolute parameter-region JSON path>", "sha256": "<byte SHA256>"},
  "observation_rule": {"path": "<absolute observation-rule JSON path>", "sha256": "<byte SHA256>"},
  "code_files": [],
  "input_files": []
}
```

Every pin is exactly `{path, sha256}` with an absolute path and lowercase
64-hex SHA256. `pass_input` is the existing `PASS_INPUT_C2V003` document with
`pass_label=PASS_K`, the current build and plan, saved spec and selection, roster
mapping, freeze-module pin and null-direction rule. The command derives
alternatives from the pinned slots and the query manifest from the primary
roster. Production requires the program query-manifest identity.

`input_files` must contain the pinned calibration record and observation-region
file required by v003g, together with the root's other required freeze evidence.
`code_files` contains additional code pins required by the root's inventory.
The wrapper automatically includes itself, the builder and freeze module as
code files, and its command inputs, head, head PASS_K, build, plan, spec, notes,
slots, selection, roster mapping, query manifest and metadata as input files.
v003g also adds registered roster dependencies. Duplicate conflicting pins and
code/input overlaps refuse.

The external head pin is mandatory because a hash chain alone cannot detect
removal of its newest entry. Root must supply its independently recorded latest
head, not infer that authority from the directory being checked.

Only after the separately adopted seal/reading gates and ledger-root decision,
root can invoke the wrapper with:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 \
  nice -n 10 \
  /Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/g26_freeze_script_cx2/g26_freeze_cx2v001.py \
  --input "$FREEZE_INPUT_PATH" --input-sha256 "$FREEZE_INPUT_SHA256" \
  --out-dir "$NEW_FREEZE_DIRECTORY"
```

The variables above are root-supplied placeholders. This command was not run
against production inputs by Codex2. There is no synthetic-mode flag or pin
override in the deliverable.

The output directory must be absent and have an existing parent. Success writes
four new files: a freeze manifest, its registration, a value-free G26 result,
and the single-read audit. Standard output contains only verdict and output
pins. Refusal reports a code, not prediction values or arbitrary exception text.
No file is overwritten, renamed, moved or deleted. A partial writer failure
preserves all new partial files; a retry requires a new directory.

## Tested scope and limitations

**TESTED:** 47/47 functional checks and 13/13 restoring mutants on the release
source bytes. Full synthetic integration includes actual c2v007 PASS_K and
step-7 comparison, the actual v003g writer, registered manifest verification,
and an audit hook confirming one byte read per input, including bootstrap.
Tests use a previously saved synthetic calibration state; no calibration or
NGC forward is run. The audit fence rejects subprocesses, outside reads,
existing-file writes, moves and deletions.

The inherited fixture uses an explicit synthetic registry-verifier seam.
Test-only module constants select synthetic spec/slots pins, node files and
the SYNTHETIC_FIXTURE query role. Individual negative tests use labeled
in-memory counterfactual contexts. Mutation witnesses require the prohibited
condition to reach acceptance or its guarded writer boundary; an unrelated
refusal is not counted as a killed negative mutant.

**UNTESTED:** a production freeze, actual production spec/slots reads, target
access, and independent production registry verification within this fixture.
G28 ledger-root adoption, seal/reading gates, G16 Phase-2 sensitivity custody
form and subsequent scoring remain with root. This command neither supplies
those decisions nor launches or scores anything.

The single-read buffer semantics are inherited from c2v007: regular-file and
descriptor identity/stability checks, cached bytes by realpath and file
identity, and reuse across builder and v003g. Bootstrap verifies and executes
the builder from one guarded buffer and seeds that same cache. Existing inputs
are assumed immutable under the program's custody rules; the wrapper does not
claim to lock external writers.

**FORBIDDEN-set lineage:** pinned v003g identifies its set as inherited from the
P46 prediction harness, with four additional interface target-row names.
Reuse is disclosed under A205 item 10; it is not independent blinding evidence.
No P46 source or NGC3198-named data file was opened for this G26 build.

## Byte-hash evidence

The inventory is `REVIEW_EVIDENCE_G26_CX2V001.json`, SHA256
`e4b2cf5ce16dc9ffadadc94e86ae4acbb0dc6fa75331040f8d7dcf0fed3ff197`.
It records full paths, byte sizes and SHA256 for the test sources, source
dependencies, result records, and selected synthetic manifest/registration/audit
outputs. Every named test below is relative to this directory.

| File | SHA256 from bytes |
|---|---|
| `test_g26_cx2v001.py` | `2ec6d227e56e129d511490407e5433a72e95f3bec6af476cedc1eb6a3acc1f4d` |
| `g26_cases_draft001.py` | `fbb0245dd4e8abf39cf90b6b78aaea64bd9bdf669184b2d299e48402e2d9da1d` |
| `test_g26_mutants_cx2v001.py` | `c9d66056da56c8abbb94596c3426348cec237c421d66b41a6961a09dd98e8934` |
| `g26_mutations_draft001.py` | `99e5740ceb2ea898185ea77c3f93fbd587e9e3c2c9c066347c56ce57e85e21f1` |
| `RELEASE_CX2V001_TESTS/TEST_RECORD.json` | `e721bd17ea864b9a1c481f476604d7de2b1984abc2973eaeaa62dcc63262fde2` |
| `RELEASE_CX2V001_MUTANTS/MUTATION_RECORD.json` | `6081505c22c4bf3513d76db1df5f762ccaca735be6b48096775d0efe6c3560d2` |

Fixed source dependencies, byte-verified during this build:

| File | SHA256 from bytes |
|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2v007_cx2/roster_builder_c2v007_a253_v001.py` | `799fb2d002ba39885326f161e1efbe3ad35dd2b66d3c84f961ddce910e9cd15b` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py` | `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/FREEZE_EXPECTED_INPUTS_C2V004.json` | `54997f946b85150ea76cf14485c26ccd5d67227d80ddb7c2aaa05011c887a3ce` |

The c2v007 source is itself under the assigned review; a changed adopted
dependency requires a separately named G26 successor and new validation.
