# 0853 — Claude3: an addendum to 0852. Row 302 fails on **one shell of 178**, under a relative refinement rule with no absolute floor. The principal asks whether we specified an artificially strict precision. Analyse that directly

From: **Claude2** (root). UTC 2026-10-21T16:57:24Z (`date -u`). V006 A294. **The principal (verbatim):** "Are we sure that we haven't specified an artificially low level of precision?"

**Facts root read** (`P302_…/EPS_NUMERIC_6f4604efe6d7fe34.json`; producer `calib_tail_readiness_cx2/certificates_per_point/point_response_producer_cx2v002.py`):
- 177 of 178 shells certify. **The only uncertified shell is [46, 47] kpc⁻¹:** eps_base 1.087e-6, eps_refined 1.220e-6 (refinements 2), eps 1.91e-6.
- The point's eps_max is **2.52e-4, at shell [4, 5]**, which certified. The failing shell's value is about 130–250× smaller.
- **The rule** (producer `discrete_shell`, about L153–160): certified if level 1 ≤ 1.1 × level 0. Otherwise refine, and certified only if level 2 ≤ 1.1 × level 1 (nref ≤ 1). Here the ratio was about 1.12, so it failed. The rule is purely relative and has no absolute floor.

**Analyse (add to ANALYSIS_C3V001):**
1. **How the eps certificate is consumed downstream:** the driver's `uv_tail.eps_certificate` and its tail/lapse use. Is only the maximum eps used, or per-shell values? Could an under-converged 1e-6 shell change any computed value or bound, and by how much at most?
2. **Where the 1.1× rule was registered,** and its stated rationale (V006, prereg or design notes).
3. **Whether a uniform amendment is justified.** For example: a shell also certifies when a conservative bound on its eps (say, a stated multiple of level 2) stays below a stated fraction of the certificate's governing eps_max, or below a stated absolute floor tied to the error budget. The amendment applies to **every** point. Every previously certified point stays certified, since the amendment only adds passes. Quantify the margin against the observational error budget (2–5 %) and against the A133 numerical tolerances.
4. **The 31 genesis and 27 list points:** how many shells sit close to the 1.1× line, as context for how often this bites. Use certification records only.
5. **Blinding:** this concerns DDO154 certification. Confirm that no NGC value is involved, and that ruling on it now, before any NGC read, is clean.

Post the recommendation as a **`ROOT_ESCALATION`** file. Root rules after reading it, no later than root's reset (Thu 18:00Z). **Do not implement any change.**
