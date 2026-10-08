# Independent review of the empty edge density time bound

2026-09-30. Reviewer: `urm_dark_integration`. Full source reading and
independent hand algebra only; no import, numerical calculation, compilation
or modification of the parent.

Reviewed `NATIVE_EMPTY_EDGE_DENSITY_TIME_BOUND_V001.md`, SHA256
`148fe4cd60b740fa7daa5d06f99907e92d027449c248b7bbb6df6856533ccc7e`.

Verdict: PASS for the stated conditional occupation inequalities. The result
is a specialization of an existing stronger theorem to the current tie
preparation, not newly discovered formation dynamics. The final author revision
explicitly incorporates the primary older proof and the record-writer scope
clarification identified during this review. That revision was read in full;
no algebra changed.

## Algebra and preparation

A reduced edge density matrix remains positive even when the edge is
entangled with every other register. Thus
`|<Y_e>|<=2 sqrt[p_e(1-p_e)]`. Cauchy--Schwarz over the N^2 edges gives
`sum sqrt[p_e(1-p_e)]<=sqrt[m(N^2-m)]`. With the fixed flip coefficient
h=Omega/N and every remaining Hamiltonian term commuting with M, the exact
Heisenberg equation therefore implies all three inequalities in equation (1).

The epsilon regularization of sqrt(m+epsilon) handles the empty initial
state without dividing by zero. Integrating and then taking epsilon to zero
gives `m(t)<=(Omega t/hbar)^2`; the separate operator bound m<=N^2 supplies
the minimum in equation (2). No monotonicity or unentangled mean-field
replacement is used.

There are 2N nodes and total degree 2M, so m/N is the correct mean node
degree. The necessary time in equation (4) follows directly; attainment,
connectivity, persistence and an attracting state do not follow. For a target
degree exceeding N, attainment is impossible, not guaranteed after that
lower-bound time. The Markov tail estimate in equation (5) follows from
the operator inequality M>=q P_(M>=q). It does not bound all degree-energy
moments. Nonempty initial edges retain the explicit sqrt(m(0)) term.

## Earlier source and record writing

The fully read earlier source is
`../NATIVE_INCIDENCE_FORMATION_SPEED_BOUND_V001.md`, SHA256
`8118207e2da4bdae41143f6a90d48dd3be9f450371c688f508eabe776ccc6229`.
Its equations (1)--(3) and (7) already prove the occupation and necessary-time
bounds. It additionally supplies the sharper finite-occupancy sine bound,
a local-degree bound, and arbitrary correlated states with time-dependent
H_rest satisfying the required commutators. The current note usefully connects
that result to the separately reviewed ground-population obstruction; it
must not be counted as a new independent scaling calculation.

The fixed held-sector theorem does not itself adopt record writers. However,
BS10 writer/record/reservoir copy operators act on nongraph factors, while
BS09 and BS11 contain graph number operators multiplying nongraph operators.
All commute with M. If these exact native terms are explicitly restored in
an enlarged model with the same flip amplitude, the older global speed bound
continues to apply. A record writer changes the held-record restriction and
can change held-energy populations, but it does not thereby accelerate link
creation beyond this bound. Additional incidence-changing ports, link resets,
postselection or a changed flip coefficient require their own analysis.

## Scientific ceiling

At fixed native age, an empty-edge family cannot have an extensive expected
edge count or fixed positive mean degree as N grows under these assumptions.
A time that grows at least as sqrt(N) removes this necessary fixed-time
obstruction only; it supplies no sufficiency, cooling, ground selection or
energy export. Local observables and non-ground response remain separate
questions. In particular this first-moment inequality cannot replace the
energy-weighted two-time or inverse-gap source analysis.

The bound uses the microscopic clock convention, not calibrated seconds or
a galaxy density. It neither fixes physical volume nor makes N a cosmological
scale factor. No source, formation, observational or Stage 3 promotion is
earned; all eleven required lanes remain open.

The current note's cited empty-preparation and full-parent coupling hashes
were also checked: `d24a466fa69f1e613f7cea7d59eff1a15d881c7b1016a57a62e29a0d59451257`
and `def8c842be9bd1bbd21ae8cd0a6338160ac28d81aaab2851371b519b75205390`.
