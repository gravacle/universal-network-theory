"""NE1/NE2. Saved T120L only; no solver or forward entry point. Exclusive outputs."""
import hashlib, importlib.util, json, math, os, sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
ART=HERE.parent
KG=ART/'ngc_kgrid_fidelity_c2'
OP=KG/'phase23/ops/T120L_hovr'
MOD=ART/'tail_scheme_impl_c2/module'
CERT=ART/'tail_scheme_impl_c2/certificates_v002/gates'
PINS=json.loads((HERE/'INPUT_PINS_V001.json').read_text())
THETA=3.3657664138980042e-09
OP_SHA='e6453d520f902e77da77e49b8f8d1cdbed84639f11ed6cc661943553741b2af4'
KPC=3.085677581491367e19
ZK=(0.,10.,-10.,20.,-20.,30.,-30.,95.,-95.)

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def verify(p):
    p=Path(p)
    if sha(p)!=PINS[str(p)]:raise ValueError('PIN_MISMATCH '+str(p))
    return p

def load(p,name):
    p=verify(p); spec=importlib.util.spec_from_file_location(name,p)
    m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m

def write(name,obj):
    p=HERE/name
    if not p.resolve().is_relative_to(HERE.resolve()):raise ValueError('OUTPUT_SCOPE')
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(obj,f,indent=1,allow_nan=False)
    return {'path':str(p),'sha256':sha(p)}

def env():
    for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
        if os.environ.get(k)!='1':raise ValueError('SINGLE_THREAD_REQUIRED '+k)

def modules():
    return tuple(load(MOD/n,name) for n,name in (
        ('owned_uv_tail_lapse_v001.py','ngc_uvt'),('uv_tail_source_roster_c2v001.py','ngc_rs'),
        ('posix_libm_bessel_jn_provider_c2v001.py','ngc_jn')))

def certificates():
    rec={n:json.loads(verify(CERT/f).read_text()) for n,f in (
        ('EPS','EPS_CERT_V006.json'),('LO_NGC','LO_NGC_CERT_V002.json'),
        ('I1T_NGC','I1T_NGC_T120L_V001.json'),('GQ','GQ_CERT_V003_KB128.json'))}
    if rec['LO_NGC']['operator_sha256']!=OP_SHA or rec['LO_NGC']['verdict']!='PASS':raise ValueError('LO_NGC_REQUIRED')
    if rec['I1T_NGC']['verdict']!='PASS':raise ValueError('I1T_REQUIRED')
    if rec['I1T_NGC']['pins']['ngc_T120L_operator']['sha256']!=OP_SHA:raise ValueError('I1T_WRONG_STATE')
    return rec

def config(U,kbig=16.,doubled=False):
    ref=lambda n:dict(path=str(CERT/n),sha256=PINS[str(CERT/n)])
    return U.normalize_config(dict(enabled=True,outer=dict(shape='cylinder',K_big_inverse_kpc=kbig),
        source_rule='continuum_v001',gas=dict(interp='lagrange3_s_gl4',M_s=96),
        stars=dict(segment_rule='max16_ceil_kdr_plus8',tail_rule='t_panels_40a_phase1p5_gl12'),
        quadrature=dict(order=12 if doubled else 8,w_perp_max_inverse_kpc=.0025 if doubled else .005,
                        w_z_max_inverse_kpc=.0035 if doubled else .007),
        domain=dict(R_eval_max_kpc=136.5,z_eval_max_kpc=105.,z_src_max_kpc=95.),
        asymptote='EH_exact_minus_quarter',lapse_only=True,jet_order=dict(route_a=1,route_b=2,ngc_eval=1),
        lambda_scale=1.,eps_certificate=ref('EPS_CERT_V006.json'),lo_certificate=ref('LO_NGC_CERT_V002.json')))

def source(RS):
    # Read-only, target-free helper. No SavedCase is instantiated and no DDO result is read.
    verify(MOD/'tests/common_tests_v001.py')
    sys.path.insert(0,str(MOD/'tests'))
    SS=load(MOD/'tests/saved_states_v001.py','ngc_saved_inputs')
    ng=SS.ngc_inputs()
    stars=RS.stars_registered(ng['profile_all'],'NGC3198',units=dict(kpc_m=ng['kpc_m'],solar_mass_kg=ng['msun']),extra_components=(ng['h2'],))
    gas=RS.gas_columns_from_rings(ring_R_m=ng['ring_R'],ring_z_m=np.zeros_like(ng['ring_R']),
        ring_m_kg=ng['ring_m'],s_edges_kpc2=ng['edges'],M_s=96,kpc_m=ng['kpc_m'])
    return RS.Roster(stars=stars,gas=gas,provenance={'state':OP_SHA,'scope':'registered continuum; discrete representation certified separately'})

def ctx_with_tail(kbig=2.,shape='cube',doubled=False):
    env()
    if kbig not in (2.,8.,16.,32.,64.) or shape not in ('cube','sphere'):raise ValueError('UNREGISTERED_CASE')
    L=load(KG/'compute/tools/kg_lib_v001.py','ngc_kg')
    verify(ART/'ngc_route_a_freeboundary_c2/check/tools/replay_c1.py')
    verify(ART/'ngc_route_a_freeboundary_c2/check/tools/sweep_c1.py')
    C,S=L.checker()
    class TailCtx(C.Ctx):
        def metric_point(self,R,phi,z):
            if self.tail.empty:return super().metric_point(R,phi,z)
            pos=np.array([[R*math.cos(phi),R*math.sin(phi),z]])
            if (R,phi)!=self._k:
                self._line=self.line.prepare_line(prepared=self.prepared,x_m=float(pos[0,0]),y_m=float(pos[0,1]))
                self._k=(R,phi)
            pk=self.line.evaluate_line(line=self._line,z_m=z,**self.tail.jet(pos,1))
            d=pk['fields'][0,:,0];g=pk['gradient'][0,:,0,:]
            for a in (d,g):
                sc=float(np.linalg.norm(a.real));im=float(np.linalg.norm(a.imag))
                if not all(math.isfinite(v) for v in (im,sc)) or im>self.ratol+self.rrtol*sc:raise ValueError('NONREAL_PHYSICAL_METRIC')
            return self.metric.evaluate_point(delta_fields=d.real,delta_gradient_physical=g.real,
                Cbar=self.Cbar,mubar=self.mubar,R=R,phi=phi,z=z)
        def solve(self,*a,**k):raise RuntimeError('REPLAY_ONLY_NO_SOLVER')
    ctx=TailCtx()
    verify(OP/'OPERATOR.json');verify(OP/'PREP.json')
    L.OPS=KG/'phase23/ops';ctx.prepared,man=L.load_operator('T120L','hovr');ctx._k=None;ctx._line=None
    if shape=='sphere':
        k=ctx.prepared['wavevectors'];keep=np.linalg.norm(k,axis=1)*C.KPC<=2.
        ctx.prepared={key:a[keep] for key,a in ctx.prepared.items()}
    cols=S.roster(ctx)
    U,RS,PV=modules();U.TAIL_MEMORY_CAP_BYTES=4*2**30;cert=certificates();cfg=config(U,kbig,doubled)
    kept=dict(shape=shape,K_inverse_kpc=2.)
    ros=None if U.domain_is_empty(kept,cfg['outer']) else source(RS)
    gamma=float.fromhex(json.loads((OP/'PREP.json').read_text())['fa_scalars']['gamma'])
    ctx.tail=U.build(config=cfg,kept=kept,roster=ros,gamma_eff=gamma,c_m_s=ctx.c,
        eval_radii_m=[c['R_m'] for c in cols[::32]],jn_provider=PV.create_provider(),i1t=cert['I1T_NGC'],stage_kind='ngc_ring_eval')
    if not ctx.tail.record['production_admissible']:raise ValueError('NONADMISSIBLE_STATE')
    ctx.memory_cap_override=dict(bytes=4*2**30,reason="replay-only resource guard, 0513",module_sha256="c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22")
    ctx.radius_table_policy="module build precomputes the 156 declared roster radii; unchanged quadrature"
    return ctx,cols
