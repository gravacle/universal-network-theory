# Retain the archive: an exact finite-prefix memory and energy candidate

2026-09-30. Source-only derivation. This is a separately declared conditional
extension of the finite-fragment apparatus, not a change to the frozen A/B
parent or a numerical result. It removes neither old fragments nor their
energy. No Markov approximation, measurement, reset, transport, bath limit or
favorable-time selection is used.

## 1. The smaller alternative to a decoupling adapter

The preceding ordered-channel note correctly identifies that an occupied A
fragment remains coupled through nu*s^-1(Q)*q_b after its copy port is turned
off. Reusing a memoryless native-only channel would erase that interaction.
There is another exact option: retain its conserved occupation as a memory
label and retain its Hamiltonian and physical-source contribution.

Take a prescribed FINITE inventory of N initially independent blank fragment
pairs. Couple each pair once, for an independently specified finite interval,
then turn off only its copy port. Keep every old gap term. Keep the full 96D
native cell, its original blank preparation, dynamic incidence, Q and C.
This is not literal BS14a old-bulk tracing; it is a finite retained-cell
construction with a declared ordered boundary schedule.

The conditional assumptions are important:

- All pairs have the same nu and the same A/B volume assignment; all old left
  and right fragments remain assigned to their respective fixed endpoints.
- After use, no future Hamiltonian, source, boundary operation or readout
  contains X_b, Y_b or any other term changing an old occupation q_b.
- The supplied pair for each pulse is a product blank, not a reset or a reused
  correlated pair. The finite inventory, preparation, schedule and port work
  are declared inputs, not derived from BS12 or given for free.
- We retain only the future algebra that is diagonal in every old q_b. This
  includes the presently adopted energy, lapse and volume source family.

These premises do not describe fragments leaving the endpoints. A later
spatially outgoing model must replace the fixed endpoint assignment with its
actual geometry and source transport.

## 2. Exact block reduction, without a measurement

Let h=(b_L1,b_R1,...,b_Lj,b_Rj) label the used fragment occupations and let
sigma_h=<h|rho|h> be an UNNORMALIZED native operator. Every future propagator
and allowed observable is block diagonal in h. Therefore their expectation
values depend on sigma_h but not on <h|rho|h'> with h!=h'. Discarding those
off-diagonal blocks for this restricted calculation is an exact algebraic
reduction, not a physical collapse or a claim that the full state decohered.

If all future operators depend on h only through

    m_L=sum_k b_Lk,  m_R=sum_k b_Rk,
    M=m_L+m_R,       D=m_R-m_L,

then sigma_m=sum_(h with counts m) sigma_h is sufficient. Native correlations
with the counts, including carrier-sector coherences inside sigma_m, remain.
At prefix j, 0<=m_L,m_R<=j, so there are at most (j+1)^2 native blocks rather
than 4^j occupation strings. This is not a resource claim for an unlimited
prefix or an instruction to compute it.

Count aggregation fails if gaps, endpoint weights, volume/source laws or
future operations distinguish fragment identities. Then retain the full h
labels, or justified equivalence classes for which ALL future operators
agree. An equality of total zero-source energy alone is not sufficient.

## 3. The exact conditional instrument

Use a_A=s^-1(Q), a_B=1 and z_A=1, z_B=s(Q). Between copy pulses, the native
Hamiltonian conditioned on the old archive is

    H_X,m=H_X+a_X*nu*M.                                      (1)

For the next pair and a real prescribed pulse envelope f(t), the zero-source
Hamiltonian is

    H_X,m,pulse=H_X+a_X*[nu*(M+q_bL+q_bR)
                         +lambda*f(t)*(q_L X_bL+q_R X_bR)].  (2)

Let U_m be its time-ordered unitary, including the ordinary native dynamics,
and K_b(m)=<b_L b_R|U_m|00>. The exact step is

    sigma'_(m+b) += K_b(m) sigma_m K_b(m)^dagger,
    sum_b K_b(m)^dagger K_b(m)=I_96.                          (3)

All blocks are unnormalized; the total trace is one. No outcome b is measured
or selected. Equation (3) sums the full inclusive instrument. At zero source
the old carrier X_c symmetry survives, but the physical dipole still crosses
its sectors, so no carrier-sector source projection is allowed.

For A, nu*s^-1(Q)*M does not commute with H_Q. The archive changes later Q
dynamics and K_b(m) genuinely depends on its retained memory. For B at ZERO
source, nu*M is a scalar on the native cell, so

    K_b(m)=exp[-i*nu*M*delta_tau/hbar] K_b(0)                  (4)

for a pulse of duration delta_tau with the same schedule. The summed native
marginal can then obey the same one-pair channel, even though the count/native
correlations and absolute energy must still be retained. Equation (4) is not
a license to discard the archive under subsequent physical-source probes.

The used counts never decrease at copy-off boundaries because m is replaced
by m+b with b=0 or 1. Within a pulse the new occupation is reversible. This
prefix monotonicity follows from the explicitly one-use schedule and unused
blank inventory; it is not a derived fundamental arrow of time, nor does it
make the native record occupation R permanent.

## 4. Source and contact preservation, including the archive

Use precisely the earlier adopted weak-lapse chart and common controller
clock, not a newly derived metric. Let eta be the external logarithmic length
strain, alpha the signed acceleration source and L0 the positive uniform
lapse. Thus a_A(eta)=exp(-eta)*s^-1, a_B(eta)=1,
z_A(eta)=1 and z_B(eta)=exp(eta)*s. At fixed m, the complete active-pair family
is

    H(L0,alpha,eta)=L0*{H_X(eta)
       +a_X(eta)*[nu*(M+q_bL+q_bR)+lambda*f*sum_v q_v X_bv]
       +alpha*[Z_X(eta)+gamma0*z_X(eta)*
          (nu*(D+q_bR-q_bL)+lambda*f*(q_R X_bR-q_L X_bL))]}.
                                                               (5)

Here gamma0=ell0/(2*c_phys^2) remains symbolic, and source identities retain
the prior source/energy units. Positive weak lapse is imposed on the fixed
endpoint chart. Equation (5) inherits only its explicit affine-alpha family;
it does not determine omitted physical metric second-order contacts.

Between pulses the added archive insertions at L0=1, alpha=eta=0 are

    E_arch=a_X*nu*M,             Z_arch=gamma0*z_X*nu*D,
    B_eta,arch=-partial_eta E_arch,
    C_etaeta,arch=partial_eta^2 E_arch,
    C_alphaeta,arch=partial_eta Z_arch.

Consequently A adds B_eta=C_etaeta=s^-1*nu*M and C_alphaeta=0;
B adds B_eta=C_etaeta=0 and C_alphaeta=gamma0*s*nu*D. Uniform
lapse couples E_arch as well as the complete native/controller energy, and
its mixed derivative with alpha contains Z_arch. A blockwise scalar energy
is therefore not an irrelevant universal offset to this source family.

For A, Z_arch is a scalar within each fixed-m native block; for B it depends
on Q. Neither statement permits erasing the archive from all multi-pulse
responses. The source-dependent instrument and count/native correlations
must be differentiated too. In particular, sources applied DURING a copy
pulse see its X_b terms in (5). Their effects are retained by differentiating
K_b(m;source), not by substituting a native-only stationary Kubo formula.

For source histories after a cut, the same block reduction is exact because
the entire family (5) commutes with every OLD q_b. Source dependence of the
preparation or boundary schedule, if proposed later, must also be specified
and differentiated. No derivative of that unspecified data is set to zero
as a claimed physical law.

Within this adopted strain law, the instantaneous added archive contribution
to pressure at fixed state is B_eta,arch/(3V) PER CALIBRATED BRANCH VOLUME:
nonnegative for A when nu>=0, and zero for B. For quantum Q this statement
must not silently replace a branch-wise volume/readout convention with a
ratio of separately averaged quantities. This archive gap term is not a derived
negative-pressure component. The full pressure includes the original native
terms and the consistently evolved joint state; the physical volume and
absolute offset law remain conditional as before.

## 5. Complete finite-prefix energy identity, not free blank supply

At a copy-off boundary the inclusive assigned energy is

    E_j=sum_m Tr[sigma_m (H_X+a_X*nu*M)].                     (6)

Unused blanks have q_b=0 and add zero expectation under this declared gap
convention. This says nothing about the preparation cost of a pure blank,
its supporting apparatus or an independently required absolute offset.

For a square pulse with constant external sources zero, turning on the copy
term has zero mean work because the fresh independent blank has <X_b>=0.
Energy is conserved during the constant-H pulse. Turning the copy port off
requires the signed controller work

    W_off=-lambda*<a_X*(q_L X_bL+q_R X_bR)>_exit.

It follows EXACTLY, without a discarded energy term, that

    E_(j+1)-E_j=W_off,                                      (7)

where the exit expectation includes all incoming m blocks. For a smooth
pulse starting and ending at f=0, replace the right-hand side by

    W_port=integral dt lambda*dot(f)*
                      <a_X*(q_L X_bL+q_R X_bR)>.

More generally d<H>/dt=<partial_t H> gives all lapse, strain, pulse and other
declared external work through (5). Native H_Q and H_C remain included;
their internal energy changes are not counted again as external port work.
Summing (7) closes the stated finite-prefix pulse ledger. It does NOT close
the separately unsupplied preparation, fixed-endpoint support, clock,
absolute-volume or physical source-construction ledger. If those operations
are made autonomous, their Hamiltonians and initial energy must be added.

## 6. What decision this actually changes

No outgoing/decoupling adapter is needed merely to ACCOUNT for old A gaps:
retained conserved archive labels give an exact alternative. This removes
the specific mistaken memoryless discard, not the need to specify a finite
supply and port schedule. It also makes a definite A/B distinction: A has
zero-source archive feedback on Q; B retains archive-sensitive physical
probes even when its unforced marginal channel is memoryless.

The smallest next conditional specification is therefore a finite prefix
with fixed symbolic nu, lambda, pulse duration/envelope and explicitly owned
blank/support preparation, using (1)--(7) and the original native initial
state. Any future computation must first freeze that finite schedule and
its source derivatives. No new numerical packet or parameter choice follows
from this note. It would test cumulative source/energy memory, not a claimed
steady state, continuous soft spectrum, galaxy-density law or acceleration
scale. After the final prescribed external pulse, a finite complete apparatus
with a fixed finite Hamiltonian has the earlier finite-unitary recurrence and
no-global-attractor limitations. The earlier nonconstant-R proof for the
original unforced blank does not automatically apply to a deliberately
controlled final state, which could be stationary. All physical promotion
flags remain false.

## Source anchors

- `NATIVE_ORDERED_FRAGMENT_SECTORS_AND_COLLISION_LIMIT_V001.md`:
  `db905c9315a4918d18c55703b8c3ca31f16807df61944db05ba14e1cf978a7db`.
- `NATIVE_FINITE_FRAGMENT_SOURCE_CURRENT_V001.md`:
  `1116b37f9cbd35a10abc55632f4d21230cdee5a27c5122e0d70d138881b4324b`.
- `NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md`:
  `81b3c455d761667e2645117699e8986c7030290de8b54bc45879112237d2db96`.
- `NATIVE_FINITE_FRAGMENT_FORMATION_LIMIT_V001.md`:
  `f7d79015b6ed6773bf2c02e611db2b8454bca1ecd5e0ef189633ab6f1cd2cc07`.
