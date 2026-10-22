# 0409 — Codex2 return for dispatch 0434

**Verdict: PASS_SCOPED.** No sign or conditional-distribution defect found. No numerical execution/imports or live-code changes.

Verified V004 SHA256: `7d0798923302bb36763c6b4f6212c944872b2b9c2f50021183d918a19dbd03c9`. Inspected only lines 3263–3267 and 3293–3314.

At fixed states, marks, and neighbouring times, the time-dependent path weight is exp[−D_L(t−lo)−D_R(hi−t)]. Thus the conditional density is proportional to exp[−d(t−lo)], with d=D_L−D_R exactly as line 3300 uses. Mark weights are constant under this update.

Writing q=(t−lo)/ell and a=d·ell:

- Line 3303 correctly gives a uniform draw when a=0.
- Line 3304 inverts F(q)=(1−exp(−aq))/(1−exp(−a)) for a>0.
- For a<0, put b=−a>0. Line 3305 is q=1−r, where r=−log[1−u(1−exp(−b))]/b is a truncated positive-rate exponential. Reflection therefore gives density proportional to exp(bq), exactly the required negative-a law. It is a reflected inverse-CDF draw, not a sign error.

Uniform event selection at line 3298 has probability 1/k in both directions because k is unchanged. Each chosen-coordinate update samples its full conditional, so the target-density ratio cancels the proposal ratio: no Metropolis rejection is needed. The k=0 and unchanged-time cases are self-loops (3297, 3308–3310).

**Finite arithmetic:** nonfinite a fails at 3301; endpoint uniform draws fail at 3265–3266; rounded times outside the strict neighbour interval fail at 3307. Interior rounding to the old time is an identity, not a retry. These guards do not promise representability for extreme parameters or constitute exact real-arithmetic sampling. No jitter is introduced. The finding establishes the conditional-update algebra, not improved mixing or the cause of residence-time persistence.
