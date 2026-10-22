# 0408 — Codex2 return for dispatch 0432

**Verdict: PASS_SCOPED.** No exact-algebra inconsistency found between the three gap proposals and the normalization. No numerical execution, imports, or simulations were performed.

Verified SHA256: V004 `7d0798923302bb36763c6b4f6212c944872b2b9c2f50021183d918a19dbd03c9`; V006 `896cadbbe4059a77b33f370d643cfa7657c0e031d61d1aa46886e88eb4f576b7`. Checked V004 lines 3243–3291 and V006 lines 8–15, 120–129 only.

Let q=δ/ell, a=d·ell. The target gap density is proportional to (1−q)exp(−aq), 0<q<1.

- **|a|≤1, lines 3275–3278:** |u−v| has density 2(1−q). Acceptance exp[−aq−max(0,−a)] multiplies it by the required exponential, with a valid envelope for either sign.
- **a>1, lines 3279–3281:** inverse-CDF sampling gives a truncated exponential proportional to exp(−aq). Acceptance 1−q supplies the missing triangular factor.
- **a<−1, lines 3282–3286:** with b=−a, r is Gamma(2,b), rejected when r≥1. Substitution q=1−r gives density proportional to (1−q)exp(bq). The extra acceptance at line 3287 is always satisfied for an open uniform when logaccept=0.

Line 3288 samples t₁ uniformly over length ell(1−q). Dividing the normalized gap density by this conditional interval length yields ordered-time density exp(−dδ)/Z. The ±1 branch changes preserve that density.

**Normalization, lines 3247–3260:** Z/ell²=(a−1+exp(−a))/a². The small-|a| series has the correct factorial recurrence and limit 1/2; its omitted tail at |a|<0.1 is below double-precision roundoff. The positive-a expression and both negative-a expressions are algebraically equivalent; switching at 0.1 and b=50 introduces no formula mismatch.

**Floating-point limits:** extreme |a| can round q to 0 or 1 or collapse absolute event times. `_open_u` rejects endpoint uniforms; V006 lines 125–129 pass d=D_y−D_x and reject non-strict returned ordering. Arithmetic exceptions can also terminate rather than silently repair a proposal. These are fail-closed corners, not guarantees that all representable inputs succeed. No jitter/resampling correction is warranted. Without measured d/ell values, this review does not attribute the pilot's rejection counts or failed mixing to time sampling.
