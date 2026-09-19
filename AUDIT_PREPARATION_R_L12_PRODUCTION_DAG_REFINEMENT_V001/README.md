# L12 production-DAG refinement and final-sink packet V001

## Outcome

The current Stage 1 candidate passes its bounded nonphysical implementation
suite. This packet maps the abstract authorization/launch models to the target,
hostile, launcher, evidence-publisher, and final-auditor interfaces. It also
implements the strict A23--A27 sinks and the complete Stage-1 artifact census.

This is a pre-freeze candidate, not the Stage 1 certification and not an L12
accumulation result. It launched no worker and created no gate, cache,
workspace, history, telemetry, spectral result, continuum claim, or gravity
claim.

## Implemented evidence

- The production graph contains 30 nodes, 39 direct edges, and 389 transitive
  edges, and preserves all 22 edges of the 18-node abstract model.
- The launch model has nine exact methods and 14 proved refinement edges,
  including both terminal-live worker completions before telemetry.
- Static inspection authenticates 38 production interfaces, 14 ordered stage
  calls, 37 predecessor argument bindings, ten launcher runtime interfaces,
  and two evidence-custody interfaces.
- All five A23--A27 sinks are production-wired. The final auditor reconstructs
  42 transitive authority records and compares all 12 L12 terminal shards after
  the exact lineage and carrier basis permutations.
- Authority and terminal inputs use retained parent/file descriptors, exact
  canonical bytes, full file identity and link-count checks, and pre/post hash
  revalidation. Evidence publication is no-clobber and owner-once.
- The target/hostile representations remain distinct: target
  Krylov/coarse-fine/NPY and hostile Chebyshev/rough-sharp/raw-`c128`.
- The obligation matrix SHA-256 is
  `49a1a5901249c0476ebd775d60b9342436e4391a2a97b9c08f1082247b719e77`.
  It contains 26 artifacts, 33 positives, 36 mutation classes, 477 assignments,
  and 375 rule statements.

## Verification

The active suite passes 46/46 tests. The Stage-1 census test follows the
governing handoff verifier's exact five-manifest target census and keeps the
hostile cache paths classified as Stage-2 outputs. The active suite includes
all five final-sink positive
fixtures, 113 A23--A27 native mutations, the complete 477-case/33-positive A27
ledger, exact native refusal phrases for all 73 artifact/class pairs whose
messages are more specific than their mutation categories, explicit test-only
fixture-provider injection that cannot affect live validators, the exact 42-record authority
census, basis-permutation reconstruction,
parent/path/hardlink/noncanonical/metadata-race attacks, 24 predecessor orders
for A26 publication, and the production-interface refinement checks.

See `VERIFICATION.txt` and `ADJUDICATION_RECORD_V001.json` for the exact
candidate record. Promotion still requires source quiescence, two independent
same-hash reviews, immutable freeze, and two frozen-byte audits.

## Reproduction

From this directory, without creating canonical outputs:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/wacf-pycache python3 -c 'import unittest, test_production_dag_refinement as t; s=unittest.defaultTestLoader.loadTestsFromModule(t); r=unittest.TextTestRunner(verbosity=2).run(s); raise SystemExit(0 if r.wasSuccessful() and s.countTestCases()==46 else 2)'
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/wacf-pycache python3 -c 'import json, production_dag_refinement as p; print(json.dumps(p.run_all_refinement_checks(), indent=2, sort_keys=True))'
```
