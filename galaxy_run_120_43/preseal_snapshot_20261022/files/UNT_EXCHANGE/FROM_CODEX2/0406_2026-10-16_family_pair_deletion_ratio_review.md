# 0406 — Codex2 return for dispatch 0429

**Verdict: PASS_SCOPED.** The inspected V006 insertion/deletion ratios are reciprocal for the stated marked-path measure. No live code was modified and no numerical sampling was launched.

Both requested SHA256 pins match:

- V006: `896cadbbe4059a77b33f370d643cfa7657c0e031d61d1aa46886e88eb4f576b7`
- V004: `7d0798923302bb36763c6b4f6212c944872b2b9c2f50021183d918a19dbd03c9`

## Independent proposal derivation

1. Let X contain K events and X' contain k=K+2 events; let n=N_elig(X'), d=D_y−D_x, and δ=t₂−t₁.
2. The insertion density is Q_I(X→X')=p_I q_a q_b exp(−dδ)/[(K+1)Z], with q_a=α_f W_a/r_f(x) and q_b=1.
3. Reverse deletion has Q_D(X'→X)=p_D/n, while π(X')/π(X)=W_aW_b exp(−dδ).
4. Consequently R_I=(p_D/p_I)(K+1)W_aW_bZ/(n q_aq_b).
5. At deletion, the resulting path has k−2 events and therefore k−1 reverse-insertion dwells: R_D=(p_I/p_D)[n/(k−1)]q_aq_b/(W_aW_bZ)=1/R_I.
6. With the unique reverse, R_D=(p_I/p_D)[n/(k−1)]α_f/[r_f(x)W_bZ]. No additional deletion-family draw or α factor belongs in this expression.

## Code confirmation

- V006 lines 20–23 define five disjoint families with α=0.2. Lines 85–95 draw a family uniformly, choose within its weighted roster, and set `r_x=r_f/_ALPHA`. V004 lines 3325–3334 therefore evaluate the correct q_a and energy-cancelled log Z expression.
- V006 lines 89–93 return the original path when the selected family is empty; there is no resampling.
- V006 lines 138–144 use the proposed path's eligible count and the pre-insertion `k+1` dwell count.
- Deletion lines 175–187 choose uniformly from the current eligible roster and infer the family from the stored forward mark, without another random family selection. Lines 190–203 verify the returning canonical state. Lines 210–216 evaluate r_f at x, the merged dwell's state; lines 252–254 use its entire merged duration.
- Lines 256–259 negate the complete insertion-form sum, including `log(k-1)-log(neligible)`. Thus both count factors and the family factor are reciprocated correctly. V004 lines 3369–3372 use full-channel proposals and the fixed insertion/deletion split.

**Documentation only:** V004 lines 3319–3322 still describe uniform times; executed lines 3329–3334 use energy-weighted times. Its palette prose at 3362–3365 also predates the full-channel assignment at 3369. Neither is an executed ratio defect. No hot patch is needed for this finding.

Scope excludes time-sampling stability, other kernels, ergodicity, performance, and empirical mixing. The reviewed log-Z evaluation and stated unique-reverse/path-admission properties are premises, as requested.

## Availability

The principal subsequently directed Codex2 to keep taking new work while usage remains. This task is complete; please post the next small, independent assignment with exact files and scope. No additional work on the running V006 pilot is implied by this request.
