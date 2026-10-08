# Held hexagon: actual matter addition and complementary memory V001

2026-10-05 UTC. Root derivation following the native review. Prospective
analytical gate; full numerical joint spectrum is uncomputed. This extends
the held cell, not the physical3D phase or a selected cosmic state.

## Same background and actual copying

Let ψ be a normalized eigenstate of the held64 incidence Hamiltonian in
the conserved all-q1 Nc0 block, H_vac ψ=Eψ ψ. The full held Nc0 operator
also owns every other six-record word. ψ has not yet been proved its
globally record-selected ground. Exterior degree2/records/occupied bonds
are fixed; every exterior incidence flip and carrier hop is clamped.
Inside, add one carrier on the six actual vertices, retain all64 internal
record words and the actual copying action. The full joint space is
6×64×64=24576; this note neither constructs nor diagonalizes it.

    H1 = H_vac + EP I + K + g U,
    K = j( I + D_internal(n) ) - t A_internal(n),
    U = sum_v P_v X_record,v,
    EP=1, j=1/4, t=1/10, g=1/10.

The +jI counts the occupied exterior bond at each carrier vertex. Its
hopping is explicitly clamped, not forgotten. D_internal is the diagonal
internal occupied degree and A_internal the occupied C6 adjacency matrix.
All native record-hole Hamiltonian blocks remain in H_vac; they cannot
be replaced by the q1 block after copying.

Define the six-column addition isometry I_add|v>=|v>ψ, its projector P_add,
the excess operator Hrel=H1-Eψ I, and

    A=I_add† Hrel I_add,
    B=(1-P_add)Hrel I_add,
    D=(1-P_add)Hrel(1-P_add) on its actual complement.

These yield the exact moments

    A = EP I + <K>ψ,
    B†B = <K²>ψ - <K>ψ² + g² I >= g² I.             (1)

Proof: H_vac-Eψ annihilates the initial columns. The K fluctuations stay
in record word q1. U sends each column to an orthogonal one-hole record
word, so copy/K cross terms vanish and P_add U P_add=0. In the one-carrier
sector U²=sum_v P_v=I. K is Hermitian, hence its matrix-valued variance is
positive. This does not discard copying or assume that the one-hole
blocks subsequently evolve like q1. Their full dynamics belongs to D.

If ψ is the C6-invariant positive ground of its connected q1 block,
ρ=<n_e>ψ is the same on every edge and

    A = [EP+j+2jρ]I - tρ A_C6,
    a(k)=EP+j+2jρ-2tρ cos(k), k=2πm/6.             (2)

Equation(2) is a spectral first moment. It is not a pole dispersion,
kinetic curvature, particle mass or physical ruler. Even at k0 the
copying part leaves nonzero complementary norm g².

## Exact source/kernel obligation

The complete addition resolvent obeys

    I_add†(z-Hrel)^(-1)I_add
       = [z-A-B†(z-D)^(-1)B]^(-1).                (3)

At real z outside the complementary spectrum,

    K_eff(z)=A+B†(z-D)^(-1)B,
    partial_z K_eff=-B†(z-D)^(-2)B < 0.           (4)

Strict negativity follows from g≠0 and (1): B is injective, and the
complementary resolvent is invertible. Thus the first moment cannot be
the exact frequency-independent joint kernel. A physical pole must earn
its full normalization I-partial_z K_eff and any carrier/record/graph
relaxation. This is constructive native interaction memory, not an extra
mass assigned to records or a demonstrated gravitational enhancement.

Uniform positive L must multiply the FULL background, carrier/current,
copy and owned reference energy. Then A_L=L A,B_L=L B,D_L=L D and
K_eff(z,L)=L K_eff(z/L,1). This uniform control leaves no physical gradient
law. A nonuniform source requires its actual half-edge current vertices,
local g L_v copy vertex, background/exterior contacts and, if ψ or the
addition projector is reselected, their derivatives. Changing the
reference Eψ[L] without its contact would lose background source energy.

## Exact ground moment bound without replay

In the unique positive q1 ground at h>0 let C complement every incidence
bit and ν=sum_e n_e. Then C H_vac C=H_vac+2(ν-3). Variationally <ν>>=3.
Equality would make Cψ the same unique positive ground, then (ν-3)ψ=0,
impossible because every bit word has nonzero positive amplitude. Thus
ρ>1/2 exactly. If the finite certificate gives bare alternating P-weight
at least p, both P words have ν3 and ν<=6 elsewhere, yielding

    1/2 < ρ <= 1-p/2,
    1.5-.1 cos(k) < a(k)
       <= 1.25+(.5-.2 cos(k))(1-p/2).              (5)

Here k in a(k) is Fourier momentum.
These bound first moments, not poles. They require no discarded NumPy
vector, new vacuum eigensolve or global-record ground assertion.

Exact next joint task: obtain authenticated same-reference <K>,<K²>,ρ
or certified intervals after the finite held-q1 reference is available,
and retain the complement in any pole/source calculation. No numeric
worker, phase selection, full joint pole or3D metric is claimed here.
