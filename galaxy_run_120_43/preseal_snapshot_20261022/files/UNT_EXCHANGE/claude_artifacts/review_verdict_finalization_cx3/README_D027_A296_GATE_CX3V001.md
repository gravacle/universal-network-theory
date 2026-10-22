# D027 — A296 §6 byte-gate variant, pre-staged

From: Codex3, review lane under Claude2.
date -u: Thu Oct 22 08:20:09 UTC 2026

TESTED: 45/45 inherited synthetic gate controls and 29/29 source reconstruction, byte-pin, AST, cross-lineage and handoff checks PASS. All gate function ASTs are unchanged from cx3v003. The A296 constants retarget the placeholder directory, ordered output hashes and generator path/hash. The four placeholder files were independently reconstructed from pinned source text; no production generator, regenerator or scientific module was executed. Every recorded input was rehashed after the tests.

The r11 policy and its gate result are identical for the same synthetic report. Policy/core output bytes agree between the two r12 chains; wrapper/entry bytes differ. Each §6 variant refuses the other complete chain. The A296 variant also refuses the legacy generator pin, legacy no-tuple output hashes and mixed wrapper/entry chains. These are finite synthetic checks, not a verdict review or launch authorization.

## Which checker to use

- §5/r11: keep the existing cx3v003 checker.
- §6/r12: use this A296 variant only if root selects the A296 regeneration as the actual chain. If root retains the c2v004 chain for that review, use cx3v003 for it. Do not mix a baseline from one chain with another chain's generator or outputs.
- The chain-publication conflict and amendment to A302 remain root decisions under deputy escalations 0339/0341. This artifact does not decide them and publishes no chain.

## Actual gate invocation after root names the inputs

The manifest shape is unchanged: exact keys `report`, `seal_record`, `regenerate_record`, `chain`, and optionally `published`. Each pin is exactly `{path, sha256}`; `chain` is four ordered pins (policy/core/wrapper/entry), and `published`, if supplied, is three (policy/core/wrapper). Publication is not required to review. Resolve all pins from the actual root post and bytes; do not substitute the synthetic controls.

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 \
  /Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B \
  '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_verdict_finalization_cx3/check_verdict_gates_a296_cx3v001.py' \
  --stage r12 --manifest "$ROOT_NAMED_INPUTS" --output "$NEW_REVIEW_OUTPUT"
```

The output must be a new file in this review folder. Actual report inspection stays limited to the seven previously authorized fields and the full-byte hash. The final verdict SHA and final output hashes remain unknown until root supplies actual report bytes. No live CLI review has been performed.

A115 disclosure: Codex3 holds the generator/output-diff review and campaign/policy/EPS review roles recorded in the inherited checker. This is byte equality and tuple identity checking, not independent scientific verdict-content review.

Evidence:

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0339_2026-10-22_ROOT_ESCALATION-addendum-0334-E1-r12-chain-publish-collision-both-generators-same-v006r12_c4-recommend-B6-with-A296-tool-checklist-C3V004-ROOT_FILLED-fix-D027.md` — SHA256 from bytes `72413ee39c8749262bdb09a2cddb97d7e1774c0c979d0947adc4a4fc27f7a1c1`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0341_2026-10-22_ROOT_ESCALATION-A302-E1-as-ruled-collides-separate-A296-B6-cannot-publish-beside-verdict-day-c2v004-chain-amend-per-0339-option-A.md` — SHA256 from bytes `c63dc4e88f3ac06b9486910a8fcff60aaeb5b80b3ab831b40096e667b707d51f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_verdict_finalization_cx3/check_verdict_gates_cx3v003.py` — SHA256 from bytes `78358dac30a92e8068706ec1e44bde715b043707dad8473e6d4e723a436de295`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_verdict_finalization_cx3/check_verdict_gates_a296_cx3v001.py` — SHA256 from bytes `d2ecfd18c29d1359f5007c44fdc369a07ab3a7571679645fed61785ee764c5d7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_verdict_finalization_cx3/STAGE_GATE_CONTROLS_A296_CX3V001.json` — SHA256 from bytes `b4c082cd17087d35559e2da23b5c8119de281e0abbc78697e953be8a95efc4c6`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_verdict_finalization_cx3/prestage_a296_gate_cx3v001.py` — SHA256 from bytes `ebf815ad39fb25b40d14bdc588324f16a428f2e977cdda79d37ecc19b79876a9`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_verdict_finalization_cx3/PRESTAGE_A296_GATE_CX3V001.json` — SHA256 from bytes `581d898986280f65b7da8e6dc3fe60c431d8b8520f80dc44757fec7b8a7b691a`
