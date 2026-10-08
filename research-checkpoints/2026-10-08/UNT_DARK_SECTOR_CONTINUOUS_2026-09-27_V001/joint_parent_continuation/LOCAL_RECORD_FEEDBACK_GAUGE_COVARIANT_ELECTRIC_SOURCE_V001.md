# Incidence phase as a conserving electric source V001

2026-10-05 UTC. NEW analytical binding of the frozen prepared-current packet
to the disclosed charged-link/Maxwell interface. No Hamiltonian, state or
response is rerun. The physical charge and connector path remain symbolic.

## Complete phase and endpoint source

On one oriented physical path A to B let n be its original incidence bit,
Z=1-2n, q_pi=2qstar and theta=(q_pi/hbar) integral_A^B A.dl. The relative
endpoint charges are Q_A=qstar Z and Q_B=-qstar Z. The complete link source is

    H_ext(t)=H_theta(t)+q_pi[phi_B(t)-phi_A(t)]n
                         +qstar[phi_A(t)-phi_B(t)]I,
    H_theta=exp(i theta n) H exp(-i theta n),
    I_theta=-H_theta,theta,  I_physical=(q_pi/hbar)I_theta.

At theta0 the frozen native vertices are I_theta=hY and
H_theta,theta theta=hX. The scalar identity is the actual centered endpoint
charge reference. It affects no fixed-sector covariance but stays in source
work and the inclusive charge inventory. Other physical charges and their
scalar potentials are retained in the complete action.

Writing psi_theta=exp(i theta n) varphi gives exactly

    i hbar varphi_dot=[H+s(t)n+qstar(phi_A-phi_B)I]varphi,
    s(t)=q_pi(phi_B-phi_A)+hbar theta_dot
        =-q_pi integral_A^B E.dl.                         (1)

Here the path is fixed; moving endpoints/path require the already owned
convective and geometric contacts. Under A->A+grad chi, phi->phi-chi_dot,
theta->theta+(q_pi/hbar)(chi_B-chi_A), s is invariant. The full charge-code
gauge transformation also carries the scalar reference phase; it must not be
removed from an inclusive source/controller experiment. Wilson dressing of
the charged transfer and return readout remains as in the frozen Maxwell note.

## Prepared switch, current contact and work

Define the retarded minus-source convention
chi_On(t,t')=(i/hbar)<[O(t),n(t')]>, for any prepared density operator under H.
Equation(1) gives delta<O>=-integral chi_On s. For a step theta0 at t', with
fixed zero endpoint potentials, s=hbar theta0 delta(t-t'). Therefore

    delta<I_theta(t)>/theta0=-hbar chi_In(t,t'),
    delta<n(t)>/theta0=-hbar chi_nn(t,t').                 (2)

These are the saved n-boundary contractions; no new kernel is necessary.
In the packet's hbar1 convention the independent integrated-current result is

    integral_t'^t chi_II(t,s)ds-<hX(t)>
      =-i<[I_theta(t),n(t')]>,
    integral_t'^t chi_nI(t,s)ds=-i<[n(t),n(t')]>.

The first term alone is not the complete current step. A static vector phase
is pure gauge; switching it while holding the preparation fixed is a voltage
impulse. In the transformed frame the impulse produces
varphi(t'+)=exp(-i theta0 n)psi(t'-). This fixes the preparation boundary rather
than silently transforming the initial state into the new equilibrium state.

The actual first-order network switch work is

    delta W/theta0=<H_theta,theta(t')>=-<I_theta(t')>.

Equivalently the saved unperturbed-H integrated response is
<I_theta(t)>-<I_theta(t')>; its inclusive switched-energy readout has the direct
-<I_theta(t)> contact and hence equals -<I_theta(t')>. A time-dependent endpoint
source also owns explicit charge/potential work and its scalar identity.

Every initial release preparation in the packet is supported on occupied n.
Consequently both complete step readouts(2) vanish for those initial source
times in all four matched channels. Later edge-coherent preparations can have
nonzero boundary response. An impulse chi_II or chi_HI can be nonzero even when
the initial complete step is zero. No equilibrium or sign/passivity assumption
is made in these prepared identities.

## The same Maxwell connector receives this port load

For a specified connector path define its distribution
w_b(r)=integral_path dr_b delta(r-r_b). Its divergence is the signed endpoint
distribution, so polarization q_pi<n_b>w_b supplies the same endpoint charge
and physical current q_pi<n_dot_b>w_b. The minus-source voltage is the
gauge-invariant electric line integral in(1). The charge-density response
chi_nn and its time derivative then bind the electric polarization and current:

    delta<n_b>=sum_c q_pi,c integral chi_n_b n_c Eline_c,
    delta I_physical,b=(q_pi,b/hbar)sum_c q_pi,c
                          integral chi_I_b n_c Eline_c.   (3)

For the equivalent vector-potential port, its retarded loading kernel is

    Pi_b c=(q_pi,b q_pi,c/hbar^2)
             [chi_I_b I_c-<H_theta_b theta_c>delta].       (4)

The saved packet owns one incidence port's kernels and direct contact. The
scalar/endpoint vertices and preparation boundary in(1)-(2) are compulsory;
using chi_II alone as an electromagnetic admittance violates their cancellation.
Equation(4) can enter the SAME Maxwell connector's field equation through
w_b Pi_b c w_c^T after its physical paths, charge units, boundary and return
propagation are fixed. Cross-port and transverse spatial data are not supplied
by a one-port ring kernel.

The complete Maxwell Gauss reduction already supplies the charging energy
J_cap once. If that field is reintroduced explicitly, its duplicate capacitor
term cannot remain independently in the matter Hamiltonian. Alternatively use
the matched reduced connector/field action after eliminating that same Gauss
sector. The measured interacting port response is not automatically an
irreducible bare polarization; its field/matter Schur assignment must agree
with that one-count reduction. No new potential or extra capacitor is added.

This is an exact conserving source/readout/work interface, and a concrete use
of the new prepared susceptibility. It supplies no optical characteristic
tensor by itself. A loaded optical signal, a common massive/light/clock cone
and the source-predicted coframe residual still require the frozen common
metric domain and its complete field/material action.

## Frozen resident inputs

| Input | SHA256 |
|---|---|
| LOCAL_RECORD_FEEDBACK_MAXWELL_LIGHT_SOURCE_CONTRACT_V001.md | accff52211c47cbd92d44f1442a2b3754359ac2f1d02be012008fbeb2965d63e |
| LOCAL_RECORD_FEEDBACK_COMMON_COFRAME_OPTICAL_BINDING_V001.md | 585d9a20fb0c2bec5dccd3f8dac726a5b57b8b0c9cdad90744f4ce7d5f22c9c4 |
| LOCAL_RECORD_FEEDBACK_COMMON_METRIC_SOURCE_RESIDUAL_V001.md | 665545ea6e674105e77b5977eecf9fd37287f19d7f1b273be8116867d2fc4bad |
| LOCAL_RECORD_FEEDBACK_PAIRED_LINK_CHARGE_CODE_V001.md | e07704d82098d8dc38b9147cdd3ee98ac7903d7a79f25831899952100b850072 |
| FLOATING_RETURN_C8_RETARDED_INCIDENCE_CURRENT_V001.md | 6a4b32a76b16405871ffba37d86b2012862a4f8336ec5c8f34e258a2312fcd44 |
| floating_return_c8_retarded_incidence_current_v001.py | d828f3aaf6fcb0c452833c6d94813ec4de85b85be228afa4a701315443a13fd2 |
| FLOATING_RETURN_C8_ENDPOINT_RECORD_ISOLATION_V001_AUDIT.json | 61ceede7755790625740620d1ba8d547c7ce63d9ef4d179c509fbd71ac2d50dc |
| FLOATING_RETURN_C8_ENDPOINT_RECORD_ISOLATION_V001_AUDIT.md | 3ed1503e904773cf966c103ef1d0b1738c60e6e941832455808e94b73dcddfb5 |
