# Revised native branch: recovered stability and finite-energy degree control

2026-10-05 UTC. Analytical application to the declared revised BS tuple; no new term, parameter fit, numerical execution or canonical integration. Original action: `program-worktree/LANE_GRA_BS_F3_QIRN_MICRO_ACTION_V001/MICRO_ACTION.md`, BS06–BS14. Root derivation independently checked against that action.

## Prior result recovered, not restarted

`NATIVE_RECORD_CONNECTIVITY_PATHWAY_V001.md`, “Degree stabilization outside BS13,” already proves an extensive lower bound at fixed coefficients when the positive degree penalty is retained. `NATIVE_RECORD_CONNECTIVITY_REVIEW_V001.md` accepts that proof. `NATIVE_FORMED_STATE_SOURCE_MATCHING_V001.md` subsequently uses it for the unrestricted full-quantum dense-eligibility, fixed-finite-temperature Gibbs obstruction.

The current supported Delta=0 branch does not satisfy the seed's sufficient BS13 inequality. That is not absence of an extensive lower bound in the full family. The following is a sharper application to its revised coefficients, including dynamic copying. Preserve all earlier phase, connectivity, entropy and physical-matching limitations.

## Exact operator inequality for the revised tuple

Take one complete bipartite slab with N vertices on each side, all N^2 eligible incidence qubits, h_N=Omega/N and fixed Omega. Retain U_d=1, d_star=2, Delta=0, epsilon_r=epsilon_psi=1, lambda_R=1/2, lambda_J=1/4, |t|=1/10, nonnegative other storage and the original bounded BS10 copies. This is a full-slab mathematical parameter branch; the supported hexagon's clamps are a separate preparation whose physical implementation remains owed.

BS07 gives T_e^2=J_e^2=P_e, where P_e projects on a pair with exactly one blank and one occupied carrier register. It does not project on different contents of two occupied registers. Since incidence commutes with carrier operators,

    n_e (lambda_J J_e^2 - t T_e)
      >= (lambda_J-|t|) n_e P_e >= 0.

Regroup each record-storage term and each endpoint feedback exactly once. For integer d_v>=0 and record-occupation projection q_v in {0,1}, put k_v=d_v-2:

    (d_v-2)^2 + q_v - (1/2)d_v q_v
      = k_v(k_v-q_v/2) >= (1/2)k_v^2 >= 0.

The first inequality uses integer degree: k(k-q)>=0 for every integer k and q=0,1. It is not a continuous-degree minimum. The bare record gap cancels against feedback at d=2, so a positive bare epsilon_r supplies no effective positive record gap there.

BS08 copies have operator norm one on their orthogonal content blocks. Define

    c_copy = |g_psi_r| + |g_wr| + sum_k |g_rbk|,
    c_port = c_partial + c_p g_max,
    C0 = Omega + 2 c_copy + c_port.

Here BS13a supplies ||H_partial||<=c_partial N and at most c_p N norm-bounded port attachments. There are 2N active copy sites and N^2 flip terms. Without requiring terms to commute, their separate lower bounds add:

    H_N,ell >= (1/2) sum_v (d_v-2)^2 - C0 N I.

Consequently H_N,ell>=-C0 N I. For the disclosed example Omega=.6, g_psi_r=.1 and all other copy/port couplings zero, C0=.8. Omega is a declared full-family coefficient, not a physical calibration inferred from the supported cell.

## Conserved finite-energy preparations can stay sparse in mean

Let M=sum_e n_e. Since sum_v(d_v-2)=2M-4N, the commuting incidence operators satisfy Cauchy–Schwarz:

    sum_v(d_v-2)^2 >= 2(M-2N)^2/N.

For a normalized state with <H><=C_E N, where C_E is bounded independently of N,

    sum_v <(d_v-2)^2> <= 2(C_E+C0)N,
    <(M-2N)^2> <= (C_E+C0)N^2,
    <M> <= [2+sqrt(C_E+C0)]N.

A fixed-slab autonomous evolution conserves this energy premise if it is satisfied by its initial preparation, even with all original record-copy sites active. This supplies a controlled mean-degree bound for such histories. It proves neither concentration at degree two nor a connected, local, retained or geometrically dimensional phase. Scheduled changes between slabs require inclusive controller/switching work; conservation within one slab does not settle that work.

For N>=2, a degree-two graph formed from two distinct cyclic perfect matchings, with all local registers blank, is a zero-expectation-energy trial when ports vanish. Copy, transfer and flip expectations vanish in that number basis trial. Thus -C0 N<=E_ground<=0. This variational comparison does not describe the nonzero-carrier prepared histories or generate a lattice.

There is no contradiction with the prior fixed-finite-temperature Gibbs obstruction: that ensemble's <H>/N is not bounded uniformly in N under the assumptions of this finite-energy corollary. The obstruction is retained. Likewise, counting finite support states in the new six-record calculation does not test the full dense-eligibility thermodynamic limit.

## Nonzero carriers require an owned matter preparation

For exactly g_psi_r=.1 and other copying/ports zero, let H_common be the incidence/record part with carriers absent. On a conserved Nc sector, ||sum_v K_psi_v->r_v||<=Nc, because each local copy is bounded by its carrier-occupation projection. Nonnegative transfer/current energy then gives

    H|Nc >= E_common,min + (epsilon_psi-|g_psi_r|)Nc
          = E_common,min + .9 Nc.

Nc=0 realizes E_common,min. Hence the unrestricted zero-chemical-potential ground lies in the carrier-blank sector. The supported Nc=1,3,6 calculations are explicitly retained matter preparations; they do not show spontaneous formation of matter in the absolute ground state. A physical conserved carrier census or preparation must be owned independently.

## Scientific implication

The revised native action can have bounded energy density and bounded mean raw degree in specified finite-energy histories, with record formation allowed. This is useful constructive control of that branch. It earns no physical source/ruler/clock, metric or spin-two sector, volume deformation, negative pressure, observed galaxy law, CMB spectrum or superiority. The pending full-six-record and shared-strain gates test separate, explicitly frozen parts of the physical join. All eleven Stage3 lanes remain open.
