# Exact F3 physical-parent support-selection screen

## 1. Question and inherited parent

The audited autonomous record packet evolves a supplied cycle support with
literal BS09. The remaining question is whether the unchanged F3/FPSS parent
selects that support rather than merely accepting it as mission data.

For even `L`, split the `L^3` inherited enumeration labels by parity of the
first label. The two F3 layers each have

\[
 M={L^3\over2}
\]

sites. At every fixed pair of the other labels, activate the edges joining an
even first label to its two odd neighbors modulo `L`. The result `n_*` is a
union of `L^2` cycles of length `L`, has `2M=L^3` occupied links, and has
degree two at every vertex. These labels are a finite enumeration only; they
are not a physical grid or distance.

The incidence part of the unchanged parent is

\[
 H_{inc}=-h_M\sum_{e\in K_{M,M}}X_e
 +\Delta\sum_e n_e
 +U_d\sum_v(d_v-2)^2,
 \qquad h_M={\Omega\over M}.                       \tag{S01}
\]

It is invariant under independent permutations of the two layers.

## 2. What the classical degree energy can select

At `h_M=0`, split the link cost equally between its endpoints. The cost of a
vertex of degree `d` is

\[
 f(d)=U_d(d-2)^2+{\Delta\over2}d.                  \tag{S02}
\]

For `U_d>0` and `0<Delta<2U_d`, `d=2` is the unique integer minimizer of
(S02). Whenever a two-regular bipartite support exists, every classical
ground word is therefore two-regular.

This is degree-class selection, not support-word selection. Exchange two
right-layer labels belonging to different cycles of `n_*`. The resulting
word `n_*'` is distinct, remains two-regular, and has exactly the same (S01)
diagonal energy. The L4 and L8 constructions have respectively 16 and 64
cycles, so this competitor exists in both cases. More generally, the full
`S_M x S_M` orbit is degenerate. No coefficient choice in the diagonal BS06
terms distinguishes one labeled member of that orbit.

## 3. The transverse flip does not select an exact word

For `h_M>0`, the computational incidence words are the vertices of a connected
Boolean hypercube. Every one-link matrix element of (S01) is `-h_M`. The
finite matrix is irreducible and stoquastic. Perron--Frobenius therefore gives
a unique ground state with strictly positive amplitude on every incidence
word. Because the Hamiltonian commutes with `S_M x S_M`, uniqueness makes
that ground state permutation invariant.

Consequently it is neither `|n_*>` nor any other exact sparse support word.
A finite-temperature Gibbs state is full rank and likewise cannot be an exact
support word. A measurement could return a word, but no unchanged-parent rule
privileges the labeled cycle-cover outcome. The verifier's exact `K_(3,3)`
example has six classical degree-two ground words; after the flip is restored,
the finite ground state is unique, positive on all 512 words, and equal on the
six symmetry-related classical words.

## 4. The other inherited terms do not close selection

Literal BS09 and BS11 contain incidence occupations only as diagonal controls,
and BS10 acts trivially on the incidence factors, so

\[
 [H_{car},n_e]=[H_{form},n_e]=[H_{fb},n_e]=0      \tag{S03}
\]

for every link. They can evolve or form carriers on, or assign energies to, a
supplied incidence background; they do not prepare that background. The
reduced source-derived carrier input is identical on every right-layer site
and blank on every left-layer site. It is invariant under the explicit
right-label exchange used above, so it does not distinguish `n_*` from
`n_*'`. Any attached port or lineage anchoring that does distinguish those
labels is conditional selector data, not a bulk consequence.

FPSS can prepare `n_*` exactly only after its address map, edge list, source
tokens, controller schedule, and ports are supplied as an orthogonal program.
Its qualified hold conserves every correct or incorrect `K` support word. That
is conditional compilation and passive retention, not autonomous selection.

A concrete label-anchored `H_port` could break the symmetry, but BS12 is only
a completion slot. Specifying such matrices would make that port/program the
new selector and would require its complete source, work, recoil, clock,
boundary, failure, reset, and reference ownership. No such selector is added
or adopted here.

## 5. Result and claim classes

**Proved:** the L4/L8 support census; exact degree two; an explicit distinct
symmetry-related equal-energy competitor; the `0<Delta<2U_d` classical
degree-two window; the active-flip finite non-word ground-state theorem; and
the BS09/BS10/BS11 incidence commutators.

**Adopted:** none.

**Conditional:** FPSS may compile and hold the selected cycle word when its
complete orthogonal program and ports are supplied.

**Empirical/numerical:** a `K_(3,3)` exact diagonalization checks the finite
Perron--Frobenius consequences and orbit equality; it is corroboration, not
the general proof.

**Open:** an autonomous, label-anchored support selector; coefficient
selection; clock/duration selection; generic preparation or phase selection;
and all macroscopic/continuum response questions.

Thus the unchanged physical parent does not autonomously choose the L4/L8
cycle program. The existing autonomous carrier records remain valid
conditional-on-support microscopic accumulation records. This screen neither
calls their residuals defects nor assumes mature macroscopic behavior. It
inserts no grid, graph reward, second support field, graviton, Ward axiom, or
gravity claim.
