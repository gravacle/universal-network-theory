# Independent hostile audit

## Disposition

`PASS_AFTER_REPAIR`.

The active-seam physics survives independent reconstruction.  The repaired
packet no longer calls a signed Hamiltonian integral a CTP action: it supplies
branch Hamiltonians and propagators and defines the exact finite operator CTP
generator.  The prior material defect is closed.

## Independently confirmed

From BS07 and BS09, on the ordered basis
`A=|x,B>`, `B=|B,x>`, the target conventions give

\[
 T=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
 J=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad H=-tT.
\]

The Heisenberg equations are exactly
`dot(q_a)=-(t/hbar)J` and `dot(q_b)=+(t/hbar)J`.  Evolution of `A` is
`cos(theta)A+i sin(theta)B`; hence the current is positive in the declared
`a -> b` orientation and its integral is one.  Multiplication by the
post-write branch weight `1/2` yields transported seam current `1/2`.
The two cell residuals and their telescoped sum are all exactly zero.

The two-stage unitary is also coherent: the positive write Hamiltonian sends
the blank target to `cos(Phi)|B>-i sin(Phi)|x>`, while the negative BS09
Hamiltonian sends `A` to `iB` at `theta=pi/2`.  Their phases do not change the
occupation ledger.

The coefficient identity
`32128/27 + 7212448/6075 = 14441248/6075` is exact.  Bare F3 explicitly calls
itself a parametric action family with an initial/port completion contract,
and `H_port` does not fix the raw-source normalization.  Distinct real port
coefficients preserve Hermiticity and the stated content covariance, so the
packet's non-identifiability conclusion is defensible.  `alpha=r0` remains an
adopted conditional F3-MDC choice, not a derivation from bare F3.

## Re-audit of the repaired CTP generator

Repaired A09 defines `H_+`, `H_-` and their time-ordered propagators.  A09a
defines `Z_y=Tr(E_y U_+ rho_0 U_-^dagger)` with a complete effect family.
Independently summing two orthogonal terminal effects at equal branches gives
`Z=Tr(U rho_0 U^dagger)=Tr(rho_0)=1`.  The connected logarithm is explicitly
restricted to a nonzero source neighborhood.  This is a complete
finite-dimensional operator generator; it does not require a separately
written continuum Berry term, and the packet now expressly avoids claiming a
continuum variational action.

The mission owner-once conclusion remains bounded to the declared generator
and protocol.  It does not establish stationary global owner completeness.

The global sixteen-category JSON is appropriately fail-closed: it retains
undefined owners and marks the stationary action `OWNER_INCOMPLETE`, with
physical descent and Ward residuals `UNDEFINED`.  Its “exactly_once” field
means only that category IDs are unique; it must not be read as proof that
their physical formulas exist or are complete.

## Global and scope disposition

The sixteen-category JSON remains appropriately fail-closed: it retains
undefined owners, marks the stationary action `OWNER_INCOMPLETE`, and now says
the census fails before a physical global action can be formed.  Category-ID
uniqueness is not mistaken for supplied physical formulas.

Plan-level Gate A remains open.  Gate B is unauthorized.  No Ward identity,
graviton, grid, or gravity claim is licensed.
