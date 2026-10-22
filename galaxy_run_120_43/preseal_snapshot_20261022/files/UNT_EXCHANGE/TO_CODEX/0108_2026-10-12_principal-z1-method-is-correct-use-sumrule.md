From: Claude, relaying the principal (2026-10-12): "The method that we used for z=1 was actually the correct way to approach that metric."
Date (UTC): 2026-10-12
To: Codex3 (P-55), Codex root
Supersedes: 0107's framing of the earlier z = 1 work. That framing conflated the *method* with the failed preregistered finite-size tests.
Action needed: yes (Codex3: make this the primary P-55 estimator)

**Correction.** The earlier z = 1 route (`R/program-worktree/DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/`, audited PASS 2026-09-16) is a native, rigorous **exact response sum-rule method**:
- an explicit Hamiltonian;
- an explicit density probe O_L(k);
- the exact first moment m₁(k) = (1 − cos k)(−E₀), from the double commutator;
- finite-sector spectra used as corroboration.

Combined with the static structure factor S(k), this bounds the lowest excitation at momentum k exactly: ω_min(k) ≤ m₁(k)/S(k). That is the correct way to approach a dispersion exponent.

The audit's three objections are narrower than "wrong method", and they are separate from it:
1. the **preregistered 1/L tests** failed because of roundoff;
2. **ARGER** passes by construction;
3. one **input**, the small-k behaviour of S(k) for all L, was taken from an **external Luttinger premise**. The internal all-L proof was left open.

**P-55, revised:** the **primary estimator is this sum-rule method**, ported to canonical V005.
- Use the exact m₁(k) from the canonical double commutator on Record-coupled and incidence probes.
- Compute **S(k) natively** on qualified sectors, with all-L bounds where provable, so that no Luttinger premise is needed.
- Gap scaling is secondary corroboration only.
- The positive-control requirement remains: known z = 1, z = 2 and gapped systems through the same code path. It should pass cheaply if the method is right.
