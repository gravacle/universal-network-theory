# Native canonical Maxwell pair fixture V003

Prospectively authored 2026-10-06 UTC. The author does not import or execute this source, native Hamiltonians, propagators, eigensolvers or numerical readouts. Root alone launches after full independent preflight and fresh worker ownership. All grids and numerical criteria below are fixed before new outcomes.

The new source is `native_canonical_maxwell_pair_v003.py`. It imports no old producer. It consumes the accepted selective-port parent only for its literal absolute native 64-by-64 Hamiltonians, complete saved eigensystems, incidence projectors and previously prepared vectors. The previous spectral energy-selective interaction is replaced by the disclosed canonical Maxwell interaction; its free-energy-commutation and zero-switch-work result are not transferred.

## Exact finite field and action

Take a homogeneous, constant registered support, one opposite-momentum pair at the same frequency for each of the two transverse polarizations. This is a finite physical-source fixture, not a localized-emission or recoil construction. In dimensionless native units put Omega=hbar*omega_physical/Eunit and tau=Eunit*t_proper/hbar. Eunit is an unspecified single global physical scale. For this box fixture L_box=2*pi*hbar*c_p/(Eunit*Omega); no microscopic scale is inferred from the galaxy gradient length or macroscopic Q0/Hstar.

For two pair species, K_+=a1^dagger b1^dagger+a2^dagger b2^dagger, K_0=(N_photon+2)/2. From the four-mode vacuum the exact invariant k=1 SU(1,1) basis is |n>=sum_{j=0}^n |j,n-j>/sqrt(n+1), where each entry counts one polarization's opposite-momentum pairs. Thus K_0|n>=(n+1)|n>, K_+|n>=sqrt((n+1)(n+2))|n+1>, and N_photon=2n. Both polarizations are retained coherently; each polarization's total mean photon number is half the total.

H_D=Omega[K_0-(K_++K_-)/2], H_B=Omega[K_0+(K_++K_-)/2]. Their full positive forms are Galerkin projected onto n=0..M. They are not rebuilt from truncated a*a^dagger and their zero point is not removed. H_gamma,0=H_D+H_B=2*Omega*K_0, so the absolute four-mode vacuum energy is 2*Omega.

For a literal native incidence projector O=n_e, Z=I+kappa*n_e with kappa>-1. Its exact inverse is I-kappa*n_e/(1+kappa). The full canonical Hamiltonian, at fixed canonical electric momentum, is

H=H_native tensor I + I tensor H_gamma,0 + n_e tensor W_kappa,

W_kappa=Omega[kappa^2*K_0/(1+kappa)+kappa*(2+kappa)*(K_++K_-)/(2*(1+kappa))].

This retains counter-rotating creation/annihilation, diagonal storage, elastic native matrix elements and all coherences. There is no rotating-wave approximation, gap filter, secularization, fitted temperature or per-line coupling. No global 64(M+1)-dimensional eigensolver is used.

The exact held-source contacts are H_kappa=n_e tensor [H_B-H_D/(1+kappa)^2], H_kappa,kappa=2*n_e tensor H_D/(1+kappa)^3. On the declared homogeneous fixed-canonical-mode chart, H_gamma[N,a]=N*H_gamma[1,1]/a with a=sqrt(1-2psi), N=1+eta. At reference its first lapse/spatial and mixed N-psi contacts equal H_gamma, spatial second contact is 3H_gamma and N-N contact is zero. The native lapse contact is H_native. These particular spatial field contacts hold the registered support, native projector and native proper couplings fixed; they are not a mechanically derived all-sector coframe law.

## Input preparation and complete work ledger

Both held record sectors q=0,1, incidences e=0,3, and the same cycle/tree preparations at actual saved ages 0,.5,2 are retained. A seventh control uses the complete saved, qualified rank-one native ground eigenspace. Every incoming native column is tensored with the bare Maxwell vacuum. This ground control is not the dressed interacting ground state. No old state is propagated again to prepare an age, and no incoming vector is dephased or reset.

For each column the switch-on work is exactly W_on=Omega*kappa^2*<n_e>_initial/(1+kappa)>=0. With the constant coupled Hamiltonian, E_native+E_gamma,0+E_interaction is conserved. At an ideal switch-off at the readout time, W_off=-E_interaction. The complete identity is Delta E_native+Delta E_gamma,0+E_interaction=W_on, or after switch-off Delta E_native+Delta E_gamma,0=W_on+W_off. The original raw column norm is retained and checked, with initial photon energy 2*Omega times that raw norm; no normalization correction is silently applied. Preparation of the native column, bare vacuum and support is separately disclosed, not free work.

A ground native column cannot supply positive net native free-energy release; transient bare photons can be dressing or switching funded. Signs of native release, photons and interaction/switch storage are all saved, including negative outcomes. Positive photon count or a positive vacuum outcome is not a scientific success criterion or evidence of thermal origin.

## Fixed grid and controls

Omega={.5,1,2}; kappa={0,-.001,+.001}; M={8,12,16}; steps={128,256} on tau=0..2; saved times tau={.25,1,2}. The two q sectors, two projectors, three frequencies, three couplings, three cutoffs and two step arms give 216 trials, each with seven coherent incoming columns and three snapshots: 4,536 rows. Compare 128 versus 256 at every cutoff, and M8 versus M12 plus M12 versus M16 at 256: 3,780 complete signed row comparisons. No arm or preparation is selected after outcomes.

The propagator is the fourth-order symmetric composition S2(p*dt) S2((1-2p)*dt) S2(p*dt), p=1/(2-2^(1/3)), where S2 is exact native half-step, exact projector-conditioned canonical field full-step, exact native half-step. Negative composition substeps are a numerical unitary construction, not negative physical duration or a modified interaction. Native unitaries use the authenticated saved eigenvectors/eigenvalues after new orthogonality/residual controls; only new field matrices of dimension at most 17 are diagonalized. Kappa=0 uses the exact full-phase native/free-vacuum control.

All numerical failures remain data. Norm and imaginary-Hermitian-observable errors <=2e-11; operator/eigenvector and field positivity/identity errors <=2e-10; inclusive-energy and switch-ledger errors normalized by max(1,|E_native,initial|+2Omega) <=2e-8. Whole joint-state norm differences with absolute phase retained <=2e-8 for both time and cutoff pairs; final top-n population <=2e-8 is an independent boundary check, not an infinite-cutoff theorem. Photon negativity and zero-coupling vacuum deviations <=2e-11; ground native-negative-energy error uses the same 2e-8 energy scale. There are exactly 34,256 structured checks: 20 incoming-native controls, 1,080 per-trial operator/field controls, 29,376 row controls, and 3,780 joint-state refinement controls. Physical positive release, thermalization, irreversibility, stationarity, ordinary photon spectra/rates and cosmological effects have no pass gate.

Rows retain norm, native/free photon/interaction/total energy, native change/release, photon and pair count, coherent equal-polarization mean, switch work, top-n probability and first/second kappa contacts plus owned field metric contacts. Full complex joint states at all snapshots are saved in an NPZ per trial with shape (3,64,M+1,7). Signed refinement differences are saved for all energy/number/work/kappa contacts; effects smaller than numerical convergence and ledger errors are not earned positive-release measurements by virtue of the overall pass label.

## Custody and recovery

The twelve original scientific input seals in the source include the accepted selective RESULT/RECEIPT/MANIFEST/JOURNAL, both selected spectral payloads and commits, thermal packet/freeze, and both prospective physical notes. The source authenticates every inherited parent input/output seal and all 144 parent checkpoint commits/ordered journal owner records, completed result and prepared-state canonical payload. This is byte/schema custody, not a replay of 243,648 old measurement rows, old Hamiltonian construction or spectral-port propagation.

New runtime prefix is exclusively NATIVE_CANONICAL_MAXWELL_PAIR_V003. Manifest, journal, result, report, receipt, error and CP0000..CP0215 JSON/COMMIT/NPZ are absent before launch. JSON is fully serialized with finite-number checks before exclusive creation, files are protected 0444, and no existing artifact is overwritten. Each completed trial commits all 21 rows, all exact criterion dispositions and all three complete joint states; a resume reuses only the authenticated exact global prefix with source/input/manifest, root PID and owner epoch, canonical payload/commit bytes, NPZ shape/finiteness/hash and exact row/check census. Orphan files, a journal before manifest, a missing commit or conflicting input require refusal. Partial/uncommitted work is not silently adopted. Resume may preserve a prior own error artifact by its hash; final artifacts prohibit execution again.

Entry and prepublication rehash all consumed inputs and newly committed outputs. Final result includes every row/check/comparison; report states exact fixture scope. Root-owned journal closes with complete trial count and result hash, receipt contains source/manifest/input/output/journal seals. Failures preserve their artifacts and numerical statuses. No process timeout, kill, automatic second worker, installation or calibration is introduced.

## Physical scope retained

The positive homogeneous canonical Z changes impedance, not the common principal Maxwell cone. Once ordinary charged matter is coupled minimally, canonical photon normalization gives e_eff=e/sqrt(Z) and alpha_eff=alpha/Z at fixed bare e. A future physical history must match measured electromagnetic normalization once and include the actual native Z state/source in atomic, Compton, bremsstrahlung, double-Compton and applicable other rates. Earlier bare-Maxwell BBN/HYREC tables are not automatically new evidence for this candidate. This future rate/history obligation is not a new tolerance or cutoff gate for the finite closed fixture.

Homogeneous momentum conservation makes pairs back-to-back with equal photon energies. Individual energy-sharing continua, recoil and localized support belong to a different physical source family. A finite projected vacuum irrep with a sudden switch can establish the exact canonical mechanism and its energy debit/dressing controls only. It does not establish an outgoing detector definition, large-bath equilibrium, thermal spectrum, physical Eunit, ordinary radiation abundance, BBN compatibility or accelerated expansion.

V001 source fea75ea26891c8b7b23f664fe5268d45dd9f3bfd312bfaf57b28968ad7b61335 and protocol d1425f03cc1f4fc1ca5c606c7d5695f8b8030933408b015824e34adacad85a8e remain protected and unexecuted. V002 changes only the exclusive namespace/ancestry and protects/registers the completed own journal before the receipt; no scientific function, grid, criterion or observable changes.

V002 source cb134002c02cecaea26e59a8abd3f8af423c70f58fc41aaae1e916d7876e355b and protocol f6ba23540f314fa781a9a731dcc842f2f1cbcfd8b3a48c7859cdc1a861dd2c45 also remain protected and unexecuted. V003 additionally refuses resume from a missing or empty owner journal, validates the complete 216-checkpoint source/root/epoch/census before publication, and verifies the exact terminal owner record before journal protection. These changes, version ancestry and the clarification that twelve means the original scientific pins are custody/text only.
