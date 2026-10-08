# Coherent writer sectors and the remaining formation inputs

2026-09-30. Exact conditional analysis of the already specified record-paid
writer preparation. A coherent superposition of its two writer contents does
not evade the zero-gap fragment unitality argument. This closes a narrow
mechanism loophole; it neither supplies a passive formation law nor excludes
other UNT mechanisms. No producer was imported or executed and no new
numerical result, bath, metric, time choice or source law was adopted.

## The preparation that actually exists

The record-paid producer uses the full 18-dimensional writer/link/record
tensor space. Its copying term is

    H_copy = g sum_(x=0,1) P_wx tensor I_link tensor X_rx,
    X_rx = |B><x| + |x><B|.

Its graph, storage, feedback and link-flip terms are diagonal in writer
content. Therefore both writer projectors commute with the full generator.
The two accessible sectors have projectors

    P_x = P_wx tensor I_link tensor (|B><B|+|x><x|)_r,
    P = P_0+P_1,                 dim(P_x)=4.

They are invariant, not postselected. The old coherent input is explicitly
`(psi_0+i psi_1)/sqrt(2)`, with each psi_x in its corresponding sector.
Coherence between sectors is retained. The source implements these facts
at `compute.py` lines 64–73, 104–107 and 120–122; its complete baseline and
interactions are not discarded in the restricted H_x.

The old producer contains NO reservoir-fragment coupling. The following is
a theorem about the symbolic extension already isolated in
`NATIVE_RESERVOIR_FORMATION_CHANNEL_V001.md`, not a reinterpretation of that
old run as a reservoir experiment.

## Exact identity preservation in the symbolic extension

Append one fragment b with the BS copy operator

    K_rb = sum_x |x><x|_r tensor X_bx,
    X_bx = |B><x|_b+|x><B|_b.

Assume zero fragment gap, an initially independent blank fragment, and no
additional term that mixes the two writer sectors or leaks from P. Within
sector x the generator is exactly

    H_tot,x(t) = H_x(t) tensor I_b + g_b(t) q_r tensor X_bx.   (1)

The proof permits time-dependent H_x and scalar g_b; it does not choose
their values or a pulse duration. The fragment eigenvectors
`|+_x>=(|B>+|x>)/sqrt(2)` and `|-_x>=(|B>-|x>)/sqrt(2)` are fixed. The third
fragment state has zero initial weight and is not coupled by (1). Hence

    U_x,+/- = T exp[-i integral(H_x(t)+/-g_b(t)q_r)dt/hbar],
    Phi_x(rho_x) = (U_x,+ rho_x U_x,+†
                         +U_x,- rho_x U_x,-†)/2,
    Phi_x(I_x) = I_x.                                      (2)

The full unitary preserves the writer blocks. Since the supported identity
I_P has only diagonal writer blocks,

    Phi(I_P) = sum_x Phi(P_x) = sum_x P_x = I_P.             (3)

Equation (3) is unitality on the declared accessible system space. Its proof
does not assume that the actual initial state is incoherent: input
off-diagonal writer blocks may evolve and become entangled with the
fragment, but they are absent from the identity used to test unitality.
They have not been deleted from the actual preparation. Because the bath
eigenbases differ with x, (2) is a sector statement; no single global
random-unitary decomposition of every off-diagonal block is asserted.

Distinct independent blank fragments obey the same argument if each
fragment has only one fixed target-content operator within each invariant
system sector. Their joint eigenlabels give the corresponding finite
mixture of system unitaries. This is not an assumed inexhaustible supply
of free fresh fragments or a reset prescription.

## Exact limits of the result

The proof requires invariant P and conserved writer-content blocks,
initial system–fragment product state, and fixed mutually commuting
fragment target operators within each block. An exactly pure blank marginal
does imply factorization; a blank label or approximate occupation readout
alone does not authenticate that complete input.

It does not cover a single fragment simultaneously receiving both X_b0 and
X_b1 within ONE conserved system block, a controller that changes writer
content, leakage into mismatched record sectors, or fragment terms such
as a nonzero storage gap that fail to commute with the target shift.
Failure of these proof conditions establishes neither non-unitality nor
cooling; the new complete channel would have to be derived.

Unitality does not prove mixing or an attracting fixed point. A unital
finite channel that uniquely attracts all states within a block can only
select that block's maximally mixed state. Conserved writer populations
already prevent a unique global attractor independent of those populations.
Neither observation prohibits transient passivation of a particular
prepared state, useful coherent record formation, or a different physical
completion. No universal no-go for passive networks or UNT follows.

`critical_path_native` independently checked the sector argument and these
conditions analytically in the same session. That is an analytic check,
not a new numerical reproduction or a physical reservoir validation.

## The next native mechanism needs a completion

The owned coherent writer therefore does not provide an overlooked escape
from the specified fragment control. Together with the previous held-energy
population obstruction and the signed energy-source age spectrum, it gives
no reason to rerun the same finite preparations at selected favorable ages.

The shortest constructive requirement is one explicitly specified or
derived population-changing formation completion, with its input state,
fragment/supply or other exchange mechanism, conserved sectors, switching
or controller energy, and complete work ledger. It must also supply the
physical source derivatives of fragment, interaction and controller
energies. The next test would concern that actual completion's formation,
source response and controlled memory, not merely non-unitality.

These inputs are not determined by the current seed: BS section 2.3 leaves
the mission state open; BS12 is a boundary/port completion slot; BS20a leaves
blocking, source weights, source quotient and contacts to be specified.
The existing absolute-contact and volume-identifiability argument remains
independent of the writer result. Adding more normalized trajectories
cannot choose those absolute physical derivatives.

This is a local input blocker for a uniquely predicted native formation
and physical-source model, not a numerical resource failure, a claim that
new hypotheses are forbidden, or a stop to independent Stage 3 work.
Any new completion must be labeled as new physical content and tested;
it cannot be selected merely because it yields the desired sign. No
physical qualification flag or scientific lane is promoted by this note.

## Inspected source identities

Paths below are relative to the continuous-program directory. Line anchors
identify the specific premises; SHA256 values identify the inspected bytes.

- `record_paid_formation/compute.py:64`, `:104`, `:120` — full generator,
  invariant embeddings and coherent input:
  `75d264a2be74c8e1ddd9324df776e3f1ea7834a649241ac19f1162f1b56a4568`.
- `record_paid_formation/PROTOCOL.md:9` — tensor census and both content
  branches/coherent test:
  `fe43d63e7c920ac6defe321c0ea3c3ae7b8b85623db0bae8843e1e588983d071`.
- `NATIVE_RECORD_PAID_LINK_FORMATION_V001.md:11`, `:64` — invariant writer
  sectors and coherent-copy interpretation:
  `8ba592344007876ce0c6d42aa5ce85f55ad31c106b624f5e6f5a93a39ef40ba1`.
- `joint_parent_continuation/NATIVE_RESERVOIR_FORMATION_CHANNEL_V001.md:89`,
  `:163`, `:176` — fixed-content theorem and unresolved source/supply inputs:
  `6db32da99d6d346736e193b34b34cb270c242821051296de1be3bf7d86031a39`.
- `recovered_sources/BS_MICRO_ACTION.md:113`, `:188`, `:245`, `:420` — state
  family, copy operator, port completion and composite source template:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
- `joint_parent_continuation/NATIVE_SOURCE_BRIDGE_DECISION.md:180`, `:217`
  — distinct calculation/input slots and absolute-contact ambiguity:
  `c82040f7bebbdefcec4e782f8afb86c6c1c3f2367775f5fd2e6dbbe6159c737a`.
