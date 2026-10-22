"""Synthetic negative config/cap tests and real-smoke adapter refusal.
No constructed synthetic record is a scientific source-state certificate.
"""
import copy
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time
import numpy as np

HERE=Path(__file__).resolve().parent
def load(path,name):
    sp=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m);return m
LO=load(HERE/'lo_producer_cx2v002.py','cx2_lo_test_v002')
AD=load(HERE/'point_response_admission_adapter_cx2v001.py','cx2_adapter_test')
PR,CU=LO.PR,LO.CU
spec=json.loads((HERE.parent/'corner_preparation_v001/KB064_C000_HEADLINE_FIXED_D.TEMPLATE.json').read_bytes())
ctx=PR.point_context(spec);U,RS,PV=LO.CC.uvt_modules()
checks=[];start=time.monotonic()
def check(name,ok):
    if not ok:raise AssertionError(name)
    checks.append({'name':name,'verdict':'PASS'})
def rejects(name,fn):
    try:fn()
    except (ValueError,KeyError,TypeError):check(name,True)
    else:raise AssertionError('not rejected: '+name)

# These metadata fixtures intentionally have synthetic TEST_ONLY certificate
# slots. They exercise matching and refusal without implying I1-T was run.
uv=copy.deepcopy(spec['numerics']['uv_tail'])
uv['eps_certificate']=uv['lo_certificate']=U.TEST_ONLY_CERT
cfg=U.normalize_config(uv);kept=U.kept_region('route_a',None,4/U.KPC_M)
g=U._grid(kept,cfg['outer'],cfg['quadrature'],cfg['domain']['R_eval_max_kpc'])
arrays={k:g[k]/U.KPC_M for k in ('kp','kz','wkp','wz')}
dm=cfg['domain']
record=dict(stage_kind='route_a',kept=kept,outer=cfg['outer'],
    eps_certificate=U.TEST_ONLY_CERT,lo_certificate=U.TEST_ONLY_CERT,config_sha256=cfg['sha256'],
    domain_m={'R_eval_max_m':dm['R_eval_max_kpc']*U.KPC_M,'z_eval_max_m':dm['z_eval_max_kpc']*U.KPC_M,
              'z_src_max_m':dm['z_src_max_kpc']*U.KPC_M},jet_order=cfg['jet_order'],i1t={'verdict':'PASS'},
    quadrature={'order':cfg['quadrature']['order'],'N_perp':len(g['kp']),'N_z_plus':len(g['kz'])})
ok=LO.validate_current_config(spec,record,arrays,U)
check('exact derived quadrature fixture accepted but slots unbound',ok['exact_production_nodes_verified'] and not ok['certificate_slots_bound'])
for key in ('kp','kz','wkp','wz'):
    bad={k:v.copy() for k,v in arrays.items()};bad[key][0]=np.nextafter(bad[key][0],np.inf)
    rejects('one-ulp '+key+' alteration rejected',lambda b=bad:LO.validate_current_config(spec,record,b,U))
for key,value in [('config_sha256','0'*64),('domain_m',{}),('jet_order',{}),('i1t',{})]:
    bad=copy.deepcopy(record);bad[key]=value
    rejects('incorrect '+key+' rejected',lambda b=bad:LO.validate_current_config(spec,b,arrays,U))
bad=copy.deepcopy(spec);bad['numerics']['uv_tail']['quadrature']['order']=10
rejects('different spec quadrature rejected',lambda:LO.validate_current_config(bad,record,arrays,U))
bad=copy.deepcopy(spec);bad['numerics']['uv_tail']['domain']['R_eval_max_kpc']=15.
rejects('different spec domain rejected',lambda:LO.validate_current_config(bad,record,arrays,U))

# Runtime cap enforcement uses actual per-element total variation, not signed
# cancellation or caller-supplied precomputed mass totals.
geo=ctx['details']['geometry']['profile'];n=4*(len(geo['HI_plus_He']['s_edges_kpc2'])-1)
rc=ctx['details']['row_contract'];nr=len(rc['rows'])
cap=dict(schema=LO.V1.CAP_SCHEMA,identity=ctx['details']['identity'],custody=ctx['details']['custody'],
    component_names=['body','route_a'],component_column_TV_mass_caps_kg=np.ones((2,n)).tolist(),
    mass_convention='ACTUAL_PROPER_SOURCE_TOTAL_VARIATION_PER_COLUMN',fixed_registered_stars_multiplier_abs=1.,
    gas_z_abs_max_m=ctx['L'].KPC,
    readout_caps=dict(row_ids=[r['id'] for r in rc['rows']],R_m=[r['radius_m'] for r in rc['rows']],
        tau_km_s=rc['tau_km_s'],speed_abs_max_km_s=[100.]*nr,
        row_contract_sha256=ctx['details']['custody']['row_contract_sha256']))
components={name:{'elements_m_kg':[[.2,-.2] for _ in range(n)],'elements_z_m':[[0.,0.] for _ in range(n)]}
            for name in cap['component_names']}
kw=dict(ctx=ctx,components=components,row_speeds_km_s=[20.]*nr,stars_multiplier_abs=1.,
    geometry_sha256=ctx['details']['custody']['geometry_sha256'],complete_source_roster=True)
res=LO.enforce_caps(cap,**kw)
check('runtime cap computes TV despite signed zero total',res['component_TV_masses_kg'][0][0]==.4)
for name,change in [('mass overflow',{'components':copy.deepcopy(components)}),('speed overflow',{'row_speeds_km_s':[101.]*nr}),
                    ('geometry mismatch',{'geometry_sha256':'0'*64}),('roster incomplete',{'complete_source_roster':False}),
                    ('star overflow',{'stars_multiplier_abs':2.})]:
    if name=='mass overflow':change['components']['body']['elements_m_kg'][0]=[2.,-2.]
    rejects('runtime '+name+' rejected',lambda c=change:LO.enforce_caps(cap,**dict(kw,**c)))
bad=copy.deepcopy(components);bad['unaccounted']=bad['body']
rejects('runtime extra source component rejected',lambda:LO.enforce_caps(cap,**dict(kw,components=bad)))
bad=copy.deepcopy(components);bad['body']['elements_z_m'][0]=[0.,2*ctx['L'].KPC]
rejects('runtime out-of-domain z rejected',lambda:LO.enforce_caps(cap,**dict(kw,components=bad)))
bad=copy.deepcopy(cap);bad['readout_caps']['tau_km_s'][0]*=2
rejects('runtime altered tau rejected',lambda:LO.enforce_caps(bad,**kw))
bad=copy.deepcopy(cap);bad['component_column_TV_mass_caps_kg'][0][0]=float('nan')
rejects('runtime NaN cap rejected',lambda:LO.enforce_caps(bad,**kw))
epsref=CU.pin(HERE/'point_response_producer_cx2v001_TEST_EPS_C000.json')
refused=AD.adapt_eps(spec,epsref)
check('real-smoke adapter blocked before approval',refused['verdict']=='BLOCKED' and refused['proof'] is None
      and 'FULL_REGISTERED_POINT_EPS_UNTESTED' in refused['blockers'])
outref=CU.write_new(HERE/'point_response_producer_cx2v001_TEST_ADAPTER_REFUSAL.json',refused)
import ast
for name in ('point_response_producer_cx2v001.py','lo_producer_cx2v001.py','lo_producer_cx2v002.py',
             'point_response_admission_adapter_cx2v001.py'):
    ast.parse((HERE/name).read_bytes());check('syntax '+name,True)
result=dict(schema='CX2_LO_CONFIG_CAP_ADAPTER_TEST_V002',status='TESTED',verdict='PASS',utc=PR.utc(),
    fixture_scope='Synthetic metadata/caps only; no scientific I1-T or cap-review claim',checks=checks,n_checks=len(checks),
    adapter_refusal=outref,producers={n:CU.pin(HERE/n) for n in ('point_response_producer_cx2v001.py',
        'lo_producer_cx2v001.py','lo_producer_cx2v002.py','point_response_admission_adapter_cx2v001.py')},
    test=CU.pin(__file__),seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    untested=['positive full-EPS admission','full registered point EPS/rho','current real TailState source reconstruction',
              'approved conditional prelaunch envelope','all calibration points'])
print(json.dumps(CU.write_new(HERE/'lo_producer_cx2v002_TEST_RESULT.json',result)))
print(json.dumps({'checks':len(checks),'seconds':result['seconds'],'rss':result['peak_rss_bytes']}))
