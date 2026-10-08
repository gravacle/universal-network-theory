# Native mechanism and calorimeter-port analytical review

Accepted after complete read of `NATIVE_THERMAL_PACKET_MECHANISM_AND_PORT_TEST_V001.md`, SHA `6fd5a4def12ec22d0ec66035b0ed75368437a870a53a238baca60836e5de2d72`. No scientific producer, matrix evolution or new eigenproblem was run. The prospective 256-dimensional implementation still requires its own source/protocol preflight.

For the common cycle basis state, D=4−M and D_v=1−d_v/2 annihilate the state. Consequently H1 psi=H0 psi and every h_v,1 psi=h_v,0 psi: identical energy means/variances and local second cross moments are exact. The third energy moment differs by four flip contributions hN², hence +1. Equal first moments are not an equal full spectrum. The tree is not an equal-energy comparison.

For Q=h_L0−h_L1 and the real initial basis vector, opposite exp(±i eta Q/hbar) kicks are complex conjugates. Every real spectral projector and local energy therefore has the same expectation; purely imaginary Hermitian energy-current expectations reverse. Expanding the transformed current gives the stated positive sign, ±eta〈[Q,[H,Q]]〉/hbar². The common leading work is +eta²〈[Q,[H,Q]]〉/(2hbar²). Symmetry makes the current odd and work even in eta.

The nonzero coefficients have an independent sparse-basis derivation. Write A_j=H_ji, B_j=Q_ji. The common flip/hop graph has no triangle of three off-diagonal moves, so

    [Q,[H,Q]]_ii
      = 2 sum_j { B_j²(E_j−E_i) − A_j B_j(Q_jj−Q_ii) }.

For cycle15/carrierL0 the flip subtotal is 1/32 and carrier-hop subtotal 3/8, giving **13/16=.8125**. For tree11/carrierL0 they are 1/32 and 23/64, giving **25/32=.78125**. The occupied-record diagonal changes cancel within each flip contribution; the values are the same for q=0 and q=1. Thus equal local energies can coexist with opposite nonzero immediate energy transfer. No first-order temperature-only closure follows without an additional memory-loss or state-selection argument.

The prospective two-calorimeter census is correctly 4 native preparations × 3 ages × 3 frequencies × 3 durations × 3 probe-number preparations × 2 couplings =648. The twelve q/frequency/coupling Hamiltonians suffice. Initially 〈V〉=0, so switch-on work is zero; conserved H_on during the window then gives ΔE_native+ΔE_probe=−g〈V〉_T at switch-off. This is a switched, work-accounted port, not free radiation.

With equal probe gaps and vacuum initial probes, 〈sigma+_0 sigma−_3〉/g² tends to K_03, not K_30; subtracting the two probe means gives the connected K_03. Probe populations and this cross coherence are even under simultaneous g→−g, so their normalized finite-g corrections start at O(g²). Initially occupied probe loss instead uses the absorption diagonal. Full finite-g and Dyson remainder checks must retain their exact operator/probe conventions; none is a bosonic-photon or thermalization claim.

No algebraic or interpretive defect was found in this note. Its pure-gauge actuator energy ambiguity, actual nonstationarity, recurrence, fixed-graph connected-incidence null and distinction between total/coherent and connected probe signals are all important scope boundaries, not reasons to discard the demonstrated record-controlled transport.
