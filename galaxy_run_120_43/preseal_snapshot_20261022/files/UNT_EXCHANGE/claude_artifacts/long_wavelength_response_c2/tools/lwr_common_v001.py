"""long_wavelength_response_c2: shared loaders + lapse transfer T(k) (READ-ONLY diagnostic, not a run).

T(k) = xtilde_n / f_n for a unit lapse source, exactly the per-node statements of Fourier v005:100-113
as replayed by the audit tool lapse_integration_audit_c2/route_a_lapse/tools/transfer_scan_v001.py:
  kr = ell_F * Cbar^(1/2) k ; kp = A^T kr ; F = sum_abc w_a w_b w_c grid[a,b,c] (pinned cardinal module)
  bound = complex binding v002 bind_symbol(F, jbar=0, mubar, Cbar, kr, Eref, ell_F, gamma, static EH v002)
  x = solve(K_density, -e_n)  ->  T = x_n.
Two evaluators:
  T_module(...)  : calls the run's IDENTITY-pinned modules node by node (reference path),
  T_vec(...)     : own batched numpy transcription of the same algebra, validated against T_module.
Physical inputs: the failed NGC run's seed numerical_inputs (= s * unscaled anchor values).
numpy only. No velocities, no targets, no result.json.
"""
import hashlib, importlib.util, json, math
from pathlib import Path
import numpy as np

UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
RUN = UPC/'CLAUDE2/runs/NGC3198_ROUTE_A_A2F10_RUN_V001'
CK = RUN/'checkpoint'
CKMOD = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py')
CKMOD_SHA = '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114'
C = 299792458.0
G = 6.67430e-11
A_BRAVAIS = np.array([[0., .5, .5], [.5, 0., .5], [.5, .5, 0.]])
# task-stated unscaled anchor values (CALL_A2_ANCHOR_F10_C2V001 'physical'); the driver applies s (driver c2v001:556-557)
ANCHOR_UNSCALED = dict(common_scale_s=0.10154172268068731, gamma=2.941048894067774e42, Eref_J=1.4642919592009638e58,
                       ell_F_m=9.905025036587288e19)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def load_pinned(path, want, name):
    if sha(path) != want:
        raise ValueError('pin mismatch '+str(path))
    s = importlib.util.spec_from_file_location('lwr_'+name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


IDENT = json.loads((CK/'IDENTITY.json').read_text())['identity']
MODS = IDENT['code']['modules']


def mod(name):
    m = MODS[name]
    return load_pinned(m['path'], m['sha256'], name.replace('.', '_'))


card = mod('fourier_arguments.cardinal_module')
cplx = mod('fourier_arguments.complex_binding_module')
stat = mod('fourier_arguments.static_binding_module')
ckm = load_pinned(CKMOD, CKMOD_SHA, 'checkpoint')
SEED = json.loads((RUN/'start.json').read_text())['seed']['numerical_inputs']
EREF = SEED['Eref_J']; ELL = SEED['ell_F_m']; GAM = SEED['gamma']; KPC = SEED['kpc_m']
_s = ANCHOR_UNSCALED['common_scale_s']
ANCHOR_CHECK = dict(Eref_seed_equals_s_times_unscaled=bool(EREF == _s*ANCHOR_UNSCALED['Eref_J']),
                    gamma_seed_equals_s_times_unscaled=bool(GAM == _s*ANCHOR_UNSCALED['gamma']),
                    ell_equal=bool(ELL == ANCHOR_UNSCALED['ell_F_m']),
                    Eref_J=EREF, gamma=GAM, ell_F_m=ELL)


def root_C(Cbar):
    eig, vec = np.linalg.eigh(Cbar)
    return np.einsum('ia,a,ja->ij', vec, np.sqrt(eig), vec, optimize=False)


def T_module(kv, grid, Cbar, mubar, Eref=EREF, ell=ELL, gam=GAM):
    """Reference path: the pinned modules, one node. kv in 1/m. Returns (T complex, cond_inv, nn_native)."""
    root = root_C(Cbar)
    kr = ell*np.einsum('ij,j->i', root, kv, optimize=False)
    kp = np.einsum('ji,j->i', A_BRAVAIS, kr, optimize=False)
    wp = card.cardinal_weights(L=grid.shape[0], k_primitive=kp)
    F = np.einsum('abc,abcij->ij', wp['weights'], grid, optimize=False)
    b = cplx.bind_symbol(F_source_symbol=F, jbar=np.zeros(9), mubar=mubar, Cbar=Cbar, k_registered=kr, Eref=Eref, ell_F=ell,
                         gamma=gam, static_binding_module=stat, relative_singular_floor=SEED['relative_singular_floor'],
                         hermitian_tolerance=SEED['hermitian_tolerance'])
    f = np.zeros((10, 1), complex); f[0, 0] = 1.0
    s = cplx.solve_symbol(bound=b, source_density_columns=f, relative_singular_floor=SEED['relative_singular_floor'],
                          full_residual_relative_tolerance=SEED['solve_rtol'], full_residual_absolute_tolerance=SEED['solve_atol'])
    sv = s['singular_values']
    return complex(s['fields'][0, 0]), float(sv[-1]/sv[0]), float(b['native_kernel_cell'][0, 0].real)


class Binder:
    """Batched transcription of bind_symbol + solve_symbol for a fixed (grid, Cbar, mubar)."""

    def __init__(self, grid, Cbar, mubar, Eref=EREF, ell=ELL, gam=GAM):
        self.grid = np.asarray(grid, complex); self.L = self.grid.shape[0]
        self.Cbar = np.asarray(Cbar, float); self.mubar = np.asarray(mubar, float)
        self.Eref = Eref; self.ell = ell; self.gam = gam
        self.root = root_C(self.Cbar)
        ev, vec = np.linalg.eigh(self.Cbar)
        self.invsqrt = np.einsum('ik,k,jk->ij', vec, 1/np.sqrt(ev), vec, optimize=False)
        self.volume = ell**3*0.25*float(np.prod(np.sqrt(ev)))*1.0
        J = np.zeros((10, 10)); J[0, 0] = 1; J[1:4, 7:10] = np.eye(3); J[4:10, 1:7] = np.eye(6)
        for a in range(3):
            e = np.eye(3)[a]
            J[4:10, 7+a] = stat.mandel_vector(np.outer(e, self.mubar)+np.outer(self.mubar, e))
        self.J = J
        self.tensors = [np.zeros((3, 3))]+[self.invsqrt@stat.mandel_matrix(np.eye(6)[a])@self.invsqrt for a in range(6)]

    def F_of(self, kv):
        kr = self.ell*(kv@self.root.T)
        kp = kr@A_BRAVAIS
        q = np.remainder(kp, 2*np.pi)
        a = np.arange(self.L, dtype=float); gv = 2*np.pi*a/self.L
        ph = np.exp(1j*a[None, None, :, None]*(q[:, :, None, None]-gv[None, None, None, :]))  # n,axis,a,m
        sums = ph.sum(axis=2)
        one = (sums.real**2+sums.imag**2)/(self.L*self.L)
        F = np.einsum('na,nb,nc,abcij->nij', one[:, 0], one[:, 1], one[:, 2], self.grid, optimize=True)
        return F, kr

    def eh(self, kr):
        k = (kr@self.invsqrt.T)/self.ell
        k2 = np.einsum('ni,ni->n', k, k)
        out = np.zeros((k.shape[0], 10, 10))
        T = self.tensors
        for a in range(7):
            s = T[a]; sk = k@s.T; ts = np.trace(s); ks = np.einsum('ni,ni->n', k, sk); n = float(a == 0)
            for b in range(a, 7):
                t = T[b]; tk = k@t.T; tt = np.trace(t); kt = np.einsum('ni,ni->n', k, tk); m = float(b == 0)
                v = (-k2*float(np.einsum('ij,ji->', s, t))/2+k2*ts*tt/2+np.einsum('ni,ni->n', sk, tk)-(ks*tt+kt*ts)/2
                     + n*(k2*tt-kt)+m*(k2*ts-ks))
                out[:, a, b] = out[:, b, a] = self.gam*self.volume*v
        return out

    def native_from_F(self, F):
        D = F[:, 1:, 1:]
        Di = np.linalg.inv(D)
        Dc = np.linalg.solve(D, F[:, 1:, :1])
        Gm = np.zeros(F.shape, complex)
        Gm[:, :1, :1] = -F[:, :1, :1]+F[:, :1, 1:]@Dc
        Gm[:, :1, 1:] = F[:, :1, 1:]@Di; Gm[:, 1:, :1] = Dc; Gm[:, 1:, 1:] = Di
        return self.Eref*np.einsum('ji,njk,kl->nil', self.J, Gm, self.J)

    def T_vec(self, kv, chunk=20000, want_cond=False):
        kv = np.atleast_2d(np.asarray(kv, float))
        out = np.empty(kv.shape[0], complex); cond = np.empty(kv.shape[0]) if want_cond else None
        herm = 0.0
        for lo in range(0, kv.shape[0], chunk):
            hi = min(lo+chunk, kv.shape[0])
            F, kr = self.F_of(kv[lo:hi])
            herm = max(herm, float(np.max(np.linalg.norm(F-np.conj(np.swapaxes(F, 1, 2)), axis=(1, 2)) /
                                          np.maximum(1., np.linalg.norm(F, axis=(1, 2))))))
            tot = self.native_from_F(F)+self.eh(kr)
            e0 = np.zeros((hi-lo, 10, 1), complex); e0[:, 0, 0] = 1.0
            x = np.linalg.solve(tot/self.volume, -e0)
            out[lo:hi] = x[:, 0, 0]
            if want_cond:
                sv = np.linalg.svd(tot/self.volume, compute_uv=False)
                cond[lo:hi] = sv[:, -1]/sv[:, 0]
        self.last_F_hermitian_rel_residual = herm
        return (out, cond) if want_cond else out

    def T0_analytic(self):
        """k->0: EH block is O(k^2) and vanishes; jbar=0 so contact=0; cardinal weights -> delta at grid[0,0,0].
        native = Eref J^T Gamma J with J=diag(1,J'), [Gamma^-1]_nn = -1/F_nn  =>  T(0) = -v [K_cell^-1]_nn = v/(Eref h_NN(0))."""
        return self.volume/(self.Eref*float(self.grid[0, 0, 0, 0, 0].real))


def T_N(k_inv_m):
    return 4*np.pi*G/(C**4*np.asarray(k_inv_m)**2)


def axis_nodes():
    g = SEED['composite_grid_spec']; br = np.asarray(g['breaks_inverse_kpc'], float); ords = g['panel_orders']
    ax = []; aw = []
    for lo, hi, n in zip(br[:-1], br[1:], ords):
        gx, gw = np.polynomial.legendre.leggauss(n)
        ax.append(((lo+hi)/2+(hi-lo)*gx/2)/KPC); aw.append((hi-lo)*gw/(2*KPC))
    return np.concatenate(ax), np.concatenate(aw)


def load_iteration0():
    start = json.loads((CK/'iteration_0000'/'START.json').read_text())
    arr = {}
    for key in ('current_source_fourier_J', 'prepared_wavevectors', 'prepared_weighted_responses'):
        ref = start[key]; p = CK/ref['blob']
        assert sha(p) == ref['file_sha256'], key
        a = np.load(p, allow_pickle=False)
        assert ckm.digest(a) == ref['array_sha256'], key
        arr[key] = a
    return arr, {k: start[k] for k in arr}


DIRS = {'z': [0, 0, 1], 'x': [1, 0, 0], 'y': [0, 1, 0], '110': [1, 1, 0], '101': [1, 0, 1], '011': [0, 1, 1], '111': [1, 1, 1],
        '1-10': [1, -1, 0], '10-1': [1, 0, -1], '01-1': [0, 1, -1], '11-1': [1, 1, -1], '1-11': [1, -1, 1], '-111': [-1, 1, 1]}
