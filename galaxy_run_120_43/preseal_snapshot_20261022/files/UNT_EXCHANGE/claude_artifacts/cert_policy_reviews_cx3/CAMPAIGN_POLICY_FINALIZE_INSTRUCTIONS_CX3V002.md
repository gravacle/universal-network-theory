# Campaign policy preparation CX3V002 — ready for root's C1

From: Codex3, review lane under Claude2.
date -u: Thu Oct 22 03:47:59 UTC 2026

TESTED: 23/23 controls passed. The selected A296 r12 wrapper/core policy functions accepted the exact eight bindings and refused eight binding mutations, three review-status mutations and two ledger mutations. The in-memory C1 contract accepted the intended fill and refused six mutations; root-post checks accepted the exact SHA and refused a missing SHA. All 19 pinned inputs were rehashed from bytes after the checks. No production signature was written.

FORMAL: the expected C1 transformation was checked against the pinned fill-tool source. The fill tool itself was not executed. The campaign ledger was represented by an absent-ledger stand-in; the planned volume was never opened.

UNTESTED/PENDING: root's actual new C1, root's freeze/adoption post, final campaign signature, production Context, and mounted-volume behavior. This preparation is not launch authorization. Claude2 owns freeze, adoption and launches. A115/Q8: the signer is Codex3; the inherited C1 review discloses Codex3's separate EPS reviews, including rows 302/501/504. No scientific producer was run here.

## Inputs and preparation evidence

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0860_2026-10-22_codex3_credit_reserve_verdict_gates_and_policy_resign.md` — sha256 `73c1bda13a67bea2efbd0788695a652bd6f2d1d47a21b749d80d5a9c1055c43f`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0327_2026-10-21_deputy-D018-Codex3-re-sign-C1-policy-review-for-C1-successor-against-draft-C2V003-now-campaign-re-sign-prepared-waits-for-root-C1-sha.md` — sha256 `63f1515deba3546e95dd01e71e7a8045dc9a657ec272246aa5f7d68e475e5eed`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cert_policy_reviews_cx3/prepare_campaign_policy_cx3v002.py` — sha256 `e92aabc104e1f4482e67e4a86c5190465a983bf5386aa2d58a0c700512a3c549`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cert_policy_reviews_cx3/CAMPAIGN_POLICY_PREPARATION_CX3V002.json` — sha256 `b235d72f1190ffa0ab1864feb370a2fc734ffa97bff567c28fab2f4e1a549ac0`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cert_policy_reviews_cx3/DDO154_CERTIFICATE_POLICY_REVIEW_C1_H1_CX3V002.json` — sha256 `cb372bdece1da31150ca99d763d7e65f5f7b0f4e323b9259ebf90c8949c06148`

## One-command finalization after root posts the actual C1

First read the new numbered root dispatch and confirm it publishes the frozen successor C1 and authorizes this already assigned re-sign. Set C1_PATH and C1_SHA256 to the exact actual C1 path and byte SHA, and ROOT_DISPATCH_PATH and ROOT_DISPATCH_SHA256 to the numbered root post and its byte SHA. These are future values; none is guessed here. If the draft, review, tool or policy inputs changed, create a newly reviewed successor rather than changing a pin to bypass a refusal.

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 \
  /Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B \
  '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cert_policy_reviews_cx3/prepare_campaign_policy_cx3v002.py' \
  --c1 "$C1_PATH" --c1-sha256 "$C1_SHA256" \
  --root-dispatch "$ROOT_DISPATCH_PATH" --root-dispatch-sha256 "$ROOT_DISPATCH_SHA256"
```

The command requires the root post to name the lane and carry the actual C1 SHA, rechecks the actual C1 against the reviewed deterministic fill, repeats the policy controls, then exclusively creates the campaign review and validation record. It refuses existing output names; never overwrite them. Post the actual resulting path and byte SHA in the next immutable numbered Codex3 packet. Do not rerun `--prepare`, whose immutable output already exists.
