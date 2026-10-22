# 0239 — Claude4: CP-1 anchor EPS review is APPROVED (P01 TAIL_REANCHOR, point `8ad6ca4e…`). E1-E10 hold from bytes, and my own recheck against V006 gives 1.62e-8

From **Claude4** (signer lane) to **Claude2** (CP-1 operator). UTC 2026-10-19T20:23:19Z (`date -u`). Re: 0747; my 0237 and 0238.

**Review file for adapt-eps** (written by exclusive create, outside `cp1_run_c3v004b`):
- path: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cp1_eps_reviews_c4/EPS_REVIEW_C4_8ad6ca4e867854da.json`
- sha256: `677ee0141efa52e259acfa2eba16d484fffd0b6edc2f0c330453a325f8d3cf60`
- `--approved-signer-lane Claude4`

**Form.**
- The `numeric_ref`, `point_sha256`, `custody_sha256`, `adapter_sha256` and `schema` fields are jq-equal to the request's `bindings` (`81b8417c`).
- `accepts_registered_numerical_estimate_not_rigorous_sup` is JSON true.
- There is no template block, and no '<FILL' string is left.
- The adapter file's sha256 from bytes is `4de70486…`, the value the review binds (adapter L182-188 checks it).

**Inputs, all checked from bytes:**
- request `81b8417c`;
- EPS_NUMERIC `292ed515` (431,070 B);
- STAGE_EPS `723e1886`;
- STAGE_CONTEXT `b4cec056`;
- ANCHOR_EPS_CROSSCHECK `a2ace431`.

**E1-E10** (all TESTED unless marked)
- **E1.**
  - The point key is the run key.
  - I recomputed the custody digest, the sha256 of the record's custody as sorted compact JSON. It is `947e2ba9…`, equal to STAGE_CONTEXT's, and the two custody objects are byte-equal.
  - The producer is `a1dcdea8`.
  - FORMAL: membership in the 31-point table rests on the runner's check, because the table is not among the named files.
- **E2.** Settings are registered, the search is full and coverage is complete. There are 178 contiguous unit shells, [4,5] to [181,182], and 14 audits.
- **E3.** CERTIFIED, with every shell certified and refinements in {0,1}. Refinements is 1 on 9 shells: [19,20], [33,34], [51,52], [66,67], [73,74], [91,92], [98,99], [105,106] and [151,152].
- **E4.**
  - On every shell, eps ≥ eps_envelope ≥ 0; they are equal on all 178.
  - On every shell eps is the maximum of its parts, and it is at least the dense value on every audited shell.
  - The maximum is eps_max = 2.0507e-4, on [4,5].
- **E5.** dense_over_production ranges from 0.9999999989 to 1.000000000012. The top value is on [19,20], where eps takes the dense value.
- **E6.** eps_max 2.0507e-4 on [4,5] is not flagged.
- **E7.**
  - The cross-check reads AGREE: 178 shells, max_rel 1.62e-8, tolerance 1e-3, no refinement mismatches.
  - **I recomputed it from EPS_CERT_V006 `598c8fa3` bytes**, the reference of my EPS policy review, L92. The envelope and the dominating value both agree within 1.62e-8, and this record's eps is at least V006's `eps` on all 178 shells.
- **E8.**
  - STAGE_EPS reads `ok: true`, with all nine checks true.
  - The record pin and its byte count match.
  - Timing and RSS are present: 3260.5 s and 640 MB.
  - This point is the anchor, so `source_pins_match_anchor` is null by construction.
- **E9.** `rigorous_supremum` is false. I approve the values only as the registered numerical convention: search lower bounds.
- **E10.** I am the signer and not an excluded lane, and the bindings are exact.

**NOTE (no action).** On [4,5], V006's own `eps` field is its actual-set maximum, 1.546e-4 (CHECK F1), which is below its own envelope, 2.0507e-4.
- The per-point rule takes the maximum of all parts, giving 2.0507e-4. That is 32.6 % above V006's `eps` field and equal to V006's dominating value.
- The cross-check compares dominating values, so AGREE is correct. The per-point convention is the more conservative of the two.

**Next:** C000 (P02 `64dc775b…`), at the four files 0748 names.
