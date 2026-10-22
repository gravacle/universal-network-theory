"""Bounded real-point smoke plus independent/adversarial producer checks."""
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import sys
import time
import numpy as np

HERE = Path(__file__).resolve().parent
def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sys.modules[name] = m; sp.loader.exec_module(m)
    return m

P = load(HERE/'point_response_producer_cx2v001.py', 'pr_test')
LO = load(HERE/'lo_producer_cx2v001.py', 'lo_test')
CU = P.CU
SPEC = HERE.parent/'corner_preparation_v001/KB064_C000_HEADLINE_FIXED_D.TEMPLATE.json'
LEGACY = P.ART/'tail_scheme_impl_c2/certificates_v002/gates/LO_CERT_V002.json'
checks = []
def check(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(dict(name=name, verdict='PASS'))
def rejects(name, fn):
    try:
        fn()
    except (ValueError, KeyError, TypeError, np.linalg.LinAlgError):
        check(name, True)
    else:
        raise AssertionError('did not reject: '+name)

start = time.monotonic()
spec = json.loads(SPEC.read_bytes())
ctx = P.point_context(spec)
check('actual point independent module cross-check', ctx['checks']['max_relative_q_reference'] < 2e-8)
check('envelope t(k) reproduces actual bitwise', ctx['checks']['envelope_actual_bitwise'])
eps = P.produce_eps(spec, settings='smoke', shell_ranges=[[4,5],[8,9]], context=ctx,
                    progress=lambda x: print(json.dumps(x), flush=True))
eps_ref = CU.write_new(HERE/'point_response_producer_cx2v001_TEST_EPS_C000.json', eps)
check('subset smoke cannot claim full coverage', not eps['coverage_complete'] and not eps['full_registered_search_executed'])
check('subset smoke cannot claim production approval', not eps['production_admissible'] and eps['verdict'] != 'PASS')
check('torus audit retained in every applicable smoke shell', len(eps['envelope_audit']) == 2)
check('shell values dominate each recorded numerical candidate', all(
    r['eps'] >= max(r['eps_base'], r['eps_refined'], r['eps_envelope'], r['actual']['estimate']) for r in eps['shells']))
E2_PATH = P.ART/'tail_scheme_impl_c2/certificates_v001/tools/eps_cert_c2v002.py'
check('registered discrete reference pin', CU.sha(E2_PATH) == 'e41548099df88f3622892e0342597482d8e3df5b4230a0b87e600286071ef62a')
E2 = load(E2_PATH, 'cx2_test_reference_eps')
old = E2.certify(ctx['B'], ctx['L'], ctx['D'], 4., 5.)
check('new independent discrete rule reproduces pinned rule', all(eps['shells'][0][k] == old[k]
    for k in ('eps_base','eps_refined','refinements')))
check('full KB64 plan includes cylindrical corner magnitude', P.shell_plan(spec)[0][-1] == [90.,91.] and P.shell_plan(spec)[1])
s128 = copy.deepcopy(spec); s128['numerics']['uv_tail']['outer']['K_big_inverse_kpc'] = 128.0
check('full KB128 plan includes cylindrical corner magnitude', P.shell_plan(s128)[0][-1] == [181.,182.])
rejects('duplicate shells rejected', lambda: P.shell_plan(spec, [[4,5],[4,5]]))
rejects('outside shell rejected', lambda: P.shell_plan(spec, [[3,4]]))
rejects('nonunit EPS shell rejected', lambda: P.shell_plan(spec, [[4,6]]))
check('gap classified incomplete', not P.shell_plan(spec, [[4,5],[6,7]])[1])
rejects('NaN rejected', lambda: P.finite([float('nan')], 'bad'))
rejects('infinity rejected', lambda: P.finite([float('inf')], 'bad'))
altered = copy.deepcopy(spec); altered['physical']['gamma'] *= 2
rejects('other-point context cannot be reused', lambda: P.produce_eps(altered, context=ctx, settings='smoke', shell_ranges=[[4,5]]))
probe = ctx['D'][1] * 4.5 / ctx['L'].KPC
B = ctx['B']; L = ctx['L']; baseq = P.CC.q_of(B, probe)
scaled = L.Binder(B.grid, B.Cbar, B.mubar, Eref=2*B.Eref, ell=B.ell, gam=2*B.gam)
check('common Eref/gamma scale invariance sampled bitwise', np.array_equal(baseq, P.CC.q_of(scaled, probe)))
changed = L.Binder(B.grid, B.Cbar, B.mubar, Eref=B.Eref, ell=B.ell, gam=2*B.gam)
check('gamma/Eref point dependence actually changes q', np.max(np.abs(baseq-P.CC.q_of(changed, probe))) > 1e-7)
changed_ell = L.Binder(B.grid, B.Cbar, B.mubar, Eref=B.Eref, ell=2*B.ell, gam=B.gam)
check('ell point dependence actually changes q', np.max(np.abs(baseq-P.CC.q_of(changed_ell, probe))) > 1e-7)
lo = LO.saved_b1_diagnostic(spec, CU.pin(LEGACY), context=ctx)
lo_ref = CU.write_new(HERE/'lo_producer_cx2v001_TEST_SAVED_B1_C000.json', lo)
check('real saved B1 has finite point rho/LO calculation', lo['shells'][0]['rho_used'] > 0 and lo['shells'][0]['max_over_tau'] > 0)
check('saved B1 replay never becomes solved current-state proof', lo['verdict']=='BLOCKED' and not lo['cover_all_consumed_states'])
conditional = LO.produce_conditional_lo(spec, context=ctx)
cond_ref = CU.write_new(HERE/'lo_producer_cx2v001_TEST_CONDITIONAL_BLOCKED.json', conditional)
check('prelaunch without reviewed caps blocked before numerical envelope', conditional['verdict']=='BLOCKED'
    and not conditional['numerical_envelope_executed'] and not conditional['cover_all_consumed_states'])

# Independently check the source majorant against explicit complex sums at
# several actual DDO radial factors with positive and signed masses/z phases.
U, RS, PV = P.CC.uvt_modules(); jn = PV.create_provider()
edges = ctx['details']['geometry']['profile']['HI_plus_He']['s_edges_kpc2']
R, rdr = RS.annulus_columns(edges, U.KPC_M)
gas = RS.GasColumns(s_edges_kpc2=edges, kpc_m=U.KPC_M, M_s=64, column_R_m=R,
    column_rdr_m2=rdr, present=np.ones(len(R),bool), elements_z=[np.zeros(0) for _ in R],
    elements_m=[np.zeros(0) for _ in R])
kp = np.array([0.,4.1,13.2,64.])/U.KPC_M
radial = gas.radial_factors(kp, jn.j0)
rng = np.random.default_rng(20261018)
mass = rng.uniform(.1,2.,(2,len(R),3)) * 1e30
z = rng.uniform(-1,1,mass.shape)*U.KPC_M
caps = mass.sum(axis=2)
bound = LO.source_bound_J(radial,rdr,caps)
worst = 0.
for kz in (0.,.1,4.,32.):
    sigma = (np.exp(-1j*kz*z/U.KPC_M)*mass).sum(axis=2)/(2*math.pi*rdr[None,:])
    for signs in ((1.,1.),(1.,-1.),(-1.,1.)):
        source = P.CC.C**2 * (radial @ (np.array(signs)[:,None]*sigma).sum(axis=0))
        ratio = float(np.max(np.abs(source)/bound)); worst=max(worst,ratio)
        check('source TV majorant kz=%g signs=%s'%(kz,signs), ratio <= 1+1e-14)
toy = LO.source_bound_J(np.array([[3.]]),np.array([1/(2*math.pi)]),np.array([[1.]]),c_m_s=1)
check('radial amplification retained (naive total mass insufficient)', toy[0]==3.)
rejects('negative mass cap rejected', lambda: LO.source_bound_J(radial,rdr,-caps))
rejects('wrong radial cap shape rejected', lambda: LO.source_bound_J(radial,rdr,caps[:,:-1]))
rejects('nonfinite radial source rejected', lambda: LO.source_bound_J(np.array([[np.nan]]),[1],[[1]]))
rejects('star multiplier without star factor rejected', lambda: LO.source_bound_J(radial,rdr,caps,stars_multiplier_abs=1))

# Tiny synthetic arrays exercise the real TailState checksum and B1 algebra.
kp = np.array([4.25,5.5])/U.KPC_M; kz=np.array([.1,1.25])/U.KPC_M
a=dict(kp=kp,kz=kz,wkp=np.ones(2)/U.KPC_M,wz=np.ones(2)/U.KPC_M,
       P=np.array([[2.,3.],[-4.,5.]]),F=np.array([[1.+2j,3.+1j],[2.-1j,-1.+2j]]),
       shell_edges_inverse_kpc=np.array([4.,5.,6.]),shell_integrals=np.zeros((2,3)))
record=dict(empty=False,kept={'shape':'cube','K_inverse_kpc':4.0},
    outer={'shape':'cylinder','K_big_inverse_kpc':64.0},lambda_scale=1.,gamma_eff=B.gam,c_m_s=P.CC.C)
record['pref']=1/(4*B.gam*(2*math.pi)**3)
for i,k in enumerate(kp):
    for j,l in enumerate(kz):
        kn=math.sqrt(k*k+l*l)
        angular=float(U._c0_D(record['kept'],record['outer'],np.array([k*U.KPC_M]),np.array([l*U.KPC_M]))[0,0])
        S=abs(sum(a['P'][i,t]*a['F'][j,t] for t in range(2)))
        idx=int(np.searchsorted(a['shell_edges_inverse_kpc'],kn*U.KPC_M,side='right')-1)
        a['shell_integrals'][idx,1]+=2*record['pref']*a['wkp'][i]*k*a['wz'][j]*S*angular/kn
b1,bcheck=LO.recompute_b1(a,record,U)
check('saved B1 reconstructed against independent scalar sum', bcheck['max_relative_difference']<1e-14)
st=U.TailState(empty=False,record=record,arrays=a)
check('TailState expected digest accepted', U.TailState.from_arrays(a,record,expected_digest=st.digest).digest==st.digest)
tamper={k:v.copy() for k,v in a.items()};tamper['P'][0,0]+=1
try:
    U.TailState.from_arrays(tamper,record,expected_digest=st.digest)
except Exception as e:
    check('TailState altered P fails digest', 'DIGEST_MISMATCH' in str(e))
else:raise AssertionError('tampered digest accepted')
tamper={k:v.copy() for k,v in a.items()};tamper['shell_integrals'][0,1]*=2
rejects('mismatched B1 rejected', lambda: LO.recompute_b1(tamper,record,U))
rejects('zero tau rejected', lambda: LO.aggregate_shares({'shells':[{'range_inverse_kpc':[4.,5.],'rho_used':1.}]},
    np.array([4.,5.]),np.array([1.]),np.array([1.]),np.array([0.]),np.array([1.])))
rejects('uncovered B1 shell boundary rejected', lambda: LO.aggregate_shares({'shells':[{'range_inverse_kpc':[4.,6.],'rho_used':1.}]},
    np.array([4.,5.]),np.array([1.]),np.array([1.]),np.array([1.]),np.array([1.])))

out=dict(schema='CX2_POINT_PRODUCERS_TEST_V001',utc=P.utc(),status='TESTED',verdict='PASS',checks=checks,
    n_checks=len(checks),source_bound_max_sample_ratio=worst,
    artifacts={'eps':eps_ref,'saved_b1_diagnostic':lo_ref,'conditional_blocked':cond_ref},
    inputs={'spec':CU.pin(SPEC),'legacy_B1':CU.pin(LEGACY),'discrete_reference':CU.pin(E2_PATH)},
    producers={'EPS':CU.pin(HERE/'point_response_producer_cx2v001.py'),'LO':CU.pin(HERE/'lo_producer_cx2v001.py'),
               'test':CU.pin(__file__)},seconds=time.monotonic()-start,
    peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    untested=['full registered EPS/rho search','all calibration points','actual perpoint TailState/source custody',
              'trusted reviewed conditional cap positive path','driver admission adapter'])
print(json.dumps(CU.write_new(HERE/'point_response_producer_cx2v001_TEST_RESULT.json',out)))
print(json.dumps({'checks':len(checks),'seconds':out['seconds'],'rss':out['peak_rss_bytes']}))
