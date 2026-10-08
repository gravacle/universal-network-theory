# Coherent source/volume discriminator — prospective protocol V001

2026-09-29. Construct ID `NATIVE-CONTROLLER-INTERFEROMETER-V001`.
This is a small operational diagnostic of a proposed controller extension,
not a derivation of physical volume, a selected vacuum energy or a galaxy fit.
The original 16-state Hamiltonian, source and saved states remain unchanged.

## Question and exact target

The prior source argument shows that a prescribed classical-source experiment
cannot see a source-dependent identity energy in normalized native states.
Test a minimal coherent controller that CAN distinguish that energy without
replacing the actual prepared native state or its record-clock coherences.

Declare two source labels g=0,0.4 and two calibrated volume-displacement labels
v=0,0.3 in operational demonstration units, with hbar=1. Four controller arms
give a 64-dimensional total Hilbert space. The time-independent hold generator is

    Htot = sum_(i,j) |ij><ij| tensor [Hhold - g_i*n + e_ij I],
    e_ij = c*g_i^2/2 + alpha*v_j.

This completion adopts coherent controller preparation/readout and a volume
label calibration. The native BS seed does not itself derive them. There is
no controller hopping, count creation, spatial field or expanding universe
in this test. The original native diagnostic contact remains exactly zero;
the c term belongs only to this separately named controller completion.

Start the controller in the equal coherent superposition of four arms. For a
native pure state psi, define C_ab=<psi_b|psi_a> and controller rho_ab=C_ab/4.
Then, relative to the zero-contact reference with the same source amplitudes,

    C_ab(c,alpha) = exp[-i(e_a-e_b)t] C_ab(0,0).

For a=(g,0), b=(0,0), the ratio gives c=-2 arg(C/Cref)/(g^2*t).
For a=(g_i,v), b=(g_i,0), alpha=-arg(C_ab)/(v*t). The preselected values
below keep both phases strictly within (-pi,pi); source-only reference
contrast is at least 1-|g|t >= 0.7 by the unitary Duhamel bound.

The reduced native density matrix and every normalized conditional native
state are independent of c and alpha. Full controller dephasing removes
these phase signals. A common identity shift of the ENTIRE 64-state generator
is still unobservable. Thus the diagnostic distinguishes branch-relative
energies, not an absolute universal energy origin. Unknown controller self
energies would be confounded with these phases and must be calibrated or
derived before extracting physical coefficients from a real experiment.

## Frozen census and implementation checks

- Use all three saved preparations from `RECORD_ADDITION_RESULTS.json`:
  native, feedback_off and copying_off. Keep the saved vectors, not eigenstates.
- Ages 0, 0.5, 2 under their unchanged held Hamiltonians.
- Hold durations 0.25, 0.75.
- Completion pairs (c,alpha)=(0,0),(0.8,0),(0,0.6),(-0.8,-0.6).
- Total: 72 cases. Fixed g=0.4, v=0.3; no optimization or astronomical inputs.
- Compare a full 64-state scaled-Taylor propagator with independent 16-state
  eigensystem propagation in each controller arm. Taylor scaled norm <=0.5,
  exact-arithmetic local remainder target 1e-18; at most 200 Taylor terms.
- Absolute numerical allowance 1e-10 for state/operator identities, unitary
  evolution, total energy conservation, reduced states, and phase readout;
  decoded c/alpha allowance 1e-8. These are numerical identity checks, not
  observational acceptance tolerances or proofs of rounded-arithmetic bounds.
- Preserve all cases. Test each c/alpha sign, zero controls, the fully dephased
  controller and a global +0.31 I shift. Check visibility and phase aliasing.
- Authenticate the saved parent result, its source freeze and every parent
  source before import/use. Freeze this protocol and worker before running.

## Resource and result handling

One local single-thread numerical worker, matrices no larger than 64x64.
The arithmetic is rerunnable if interrupted; no long-job checkpoint machinery
is needed. The worker emits JSON without modifying source or old evidence;
the calling agent saves its fresh freeze/result additively using file tools.
No package installation, remote calculation, L8 or account action is needed.

Passing establishes an implemented, state-preserving discriminator for the
otherwise invisible contact/volume family. It does NOT choose c/alpha in
nature, provide a native ruler or close Stage 1. The next physical task is
an owned controller/geometry mechanism that predicts those couplings rather
than supplying them as test constants. An independent check must address
the phase sign, gauge invariance and what information the controller adds.
