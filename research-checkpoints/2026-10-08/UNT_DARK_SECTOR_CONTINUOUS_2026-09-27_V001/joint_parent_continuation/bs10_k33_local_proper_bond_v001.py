#!/usr/bin/env python3
"""Root-approved, new standalone local-family saved-scalar benchmark only.

No old module, NPZ, H, propagation or solver is accessed. Fraction arithmetic
uses authoritative serialized Decimal scalars; parent numerical qualifications
are inherited, not upgraded to physical or directed-rounding evidence.
"""
import argparse
from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import resource
import socket
import sys
import time
import traceback

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT / 'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
SOURCE = J / 'bs10_k33_local_proper_bond_v001.py'
PROTOCOL = J / 'BS10_K33_LOCAL_PROPER_BOND_V001.md'
OUT = J / 'BS10_K33_LOCAL_PROPER_BOND_V001_RESULT.json'
REPORT = J / 'BS10_K33_LOCAL_PROPER_BOND_V001_RESULT.md'
RECEIPT = J / 'BS10_K33_LOCAL_PROPER_BOND_V001_RECEIPT.json'
CP = J / 'bs10_k33_local_proper_bond_v001_checkpoints'
CNAME = 'BS10_K33_CENSUS_CREATION_SAVED_V001_RESULT.json'
GNAME = 'BS10_K33_GROWN_CONNECTION_V001_RESULT.json'
CCP = 'bs10_k33_census_creation_saved_v001_checkpoints'
GCP = 'bs10_k33_grown_connection_v001_checkpoints'
CANON_C = '39a82f837492861365d0986bde5c9fb3578bdfeac0586ea12c14e7d47ea1719c'
CANON_G = 'b573b645dace83b518da98e27a528c3076b0e4b74d81c7e6bd1a357dd0356823'
ATOL = F(5, 10**11)
DELAYS = (F(0), F(1, 10), F(1, 2), F(1), F(2), F(5))
KEYS = tuple(f'g{g}_n{n}_age{age}' for g in (0, 1) for n in (0, 413)
             for age in (0, 5, 20, 50))
TERMS = ('new_degree_baseline', 'removed_direct_hopping',
         'old_nonanchor_flip_normalization', 'lost_old_anchor_flip')
REMOVED = 'old_nonanchor_flip_normalization'
KEEP = tuple(k for k in TERMS if k != REMOVED)
ANC = {
    CNAME: 'be5bce8c92163cdb10000e1e706a1b6ad8b1a01c15299ad5a7d6f6a8e9b40ccf',
    'BS10_K33_CENSUS_CREATION_SAVED_V001_RESULT.md': '07601461760486c70c77dff88637e3fe11a3243d37ab3994bfd18fc4b580158c',
    'bs10_k33_census_creation_saved_v001.py': 'ca5429b498a274c26765667a2f4f5ab333d998e9d9cb07894c0243b2f77d9948',
    'NATIVE_UNCLAMPED_CENSUS_CREATION_V001.md': '92d6e1b2b2ce862832a6032cd6c4e891e7bbd1a7e9bb8079e62c3a66251112fb',
    CCP+'/manifest.json': 'f895883b03c435757a9bc91df235659d431f4240407732afe3f36cbc48f5b85b',
    CCP+'/events.jsonl': 'e68dd6bcc21c36825655ba5a64b2bb8b6e34902d7ac5bbcae1f6a3b96354c478',
    GNAME: '0ee08b31c2f9455e2d27b9fe14da349a8c3eff2dd0843b629905049a0d390a31',
    'BS10_K33_GROWN_CONNECTION_V001_RESULT.md': '6087a23486a494d9934547cf394df0f62c3246fedec05737b2a30c0bad5cd541',
    'bs10_k33_grown_connection_v001.py': 'cf265e9aa25a18d6c345e5214b483a9bd17e32da62e933c5f52f1c91da8106cd',
    'BS10_K33_GROWN_CONNECTION_V001.md': '486de85570196172a7813cc254f40cd405dae1a821075a75aee1dbfe9f192a1f',
    GCP+'/manifest.json': 'dd8e3942d254327a78ca763df3851c5654569c0f0ed752714f686403407cfcc4',
    GCP+'/events.jsonl': '8d025ddfbeef58a419722b872a133d38c297bbee3ad438a418433b5bbb73f1c1',
    GCP+'/error.json': '1da6e20cec2c34ae4cf404eb5cf634b1cc86340c6e820dcb9f93f0f7f3a69e0d',
    'LOCAL_PROPER_BOND_NORMALIZATION_V001.md': '9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b',
}
SCOPE = (
    'NEW local-size family h3=h4=.2, reference matched once to unchanged N3; '
    'same F,16 frozen old states,96 old whole-h0 kernels. Saved JSON scalar '
    'linear combinations only; no NPZ, old code, H, propagation, solver, '
    'target trajectory or delayed local mean reconstruction. P1 only scales '
    '4/3; no P2/endpoints. No physical clock/metric/volume/pressure/phase/'
    'growth or superiority claim. Parent floating/state qualifications retained.'
)


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    path = Path(path).resolve()
    if not path.is_relative_to(ROOT) or path.suffix == '.npz':
        raise RuntimeError('Outside sole root or prohibited NPZ access: '+str(path))
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def canon(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':'),
                                    allow_nan=False).encode()).hexdigest()


def exclusive_json(path, obj):
    with path.open('x', encoding='utf-8') as f:
        json.dump(obj, f, sort_keys=True, indent=2, allow_nan=False)
        f.write('\n'); f.flush(); os.fsync(f.fileno())
    return sha(path)


def event(name, **kw):
    with (CP/'events.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps({'event': name, 'pid': os.getpid(), 'utc': utc(), **kw},
                           sort_keys=True, allow_nan=False)+'\n')
        f.flush(); os.fsync(f.fileno())


def q(x):
    return x if isinstance(x, F) else F(x)


def dec20(x, rounding):
    x = q(x)
    with localcontext() as ctx:
        ctx.prec = 20; ctx.rounding = rounding
        return str(Decimal(x.numerator)/Decimal(x.denominator))


def rat(x):
    x = q(x)
    return {'numerator': str(x.numerator), 'denominator': str(x.denominator),
            'decimal20_floor': dec20(x, ROUND_FLOOR),
            'decimal20_ceiling': dec20(x, ROUND_CEILING)}


def band(xs):
    return {'lower': rat(xs[0]), 'upper': rat(xs[1])}


def check(checks, name, passed, **evidence):
    checks.append({'name': name, 'passed': bool(passed), 'evidence': evidence})


def equal(checks, name, actual, expected):
    actual, expected = q(actual), q(expected)
    allowance = ATOL*max(F(1), abs(actual), abs(expected))
    check(checks, name, abs(actual-expected) <= allowance,
          actual=rat(actual), expected=rat(expected), residual=rat(actual-expected),
          conditional_consistency_allowance=rat(allowance))


def loaded(name):
    text = (J/name).read_text()
    return json.loads(text), json.loads(text, parse_float=Decimal)


def committed(events, name, **fields):
    return any(e.get('event') == name and all(e.get(k) == v for k,v in fields.items())
               for e in events)


def authenticate():
    custody = {name: sha(J/name) for name in ANC}
    if custody != ANC:
        raise RuntimeError('Frozen ancestor changed: '+repr({k:v for k,v in custody.items() if v!=ANC[k]}))
    c, cd = loaded(CNAME); g, gd = loaded(GNAME)
    for parent, expected, label, count, status in (
            (c,CANON_C,'census',3157,'QUALIFIED_SAVED_ARRAY_ARITHMETIC'),
            (g,CANON_G,'grown',7215,'QUALIFIED_ARITHMETIC')):
        payload = dict(parent); digest = payload.pop('canonical_payload_sha256')
        if digest!=expected or canon(payload)!=expected or parent['status']!=status or parent['passed_count']!=count or parent['failed_count']:
            raise RuntimeError('Parent scientific/canonical receipt mismatch: '+label)
        if len(parent['rows'])!=16 or {r['key'] for r in parent['rows']} != set(KEYS):
            raise RuntimeError('Parent16-state census mismatch: '+label)
    if c['error'] is not None:
        raise RuntimeError('Original census science error')
    cm = json.loads((J/CCP/'manifest.json').read_text())
    gm = json.loads((J/GCP/'manifest.json').read_text())
    if cm['host']!=socket.gethostname() or gm['host']!=socket.gethostname():
        raise RuntimeError('Not same Mac host as both parent calculations')
    if cm['input_sha256']!=c['input_sha256'] or gm!=g['manifest']:
        raise RuntimeError('Original manifest/receipt mismatch')
    for manifest, src, prot in (
        (cm,'bs10_k33_census_creation_saved_v001.py','NATIVE_UNCLAMPED_CENSUS_CREATION_V001.md'),
        (gm,'bs10_k33_grown_connection_v001.py','BS10_K33_GROWN_CONNECTION_V001.md')):
        if manifest['source_sha256']!=ANC[src] or manifest['protocol_sha256']!=ANC[prot]:
            raise RuntimeError('Original source/protocol manifest mismatch')
    for parent, cpname, resultname, reportname, canonical in (
        (c,CCP,CNAME,'BS10_K33_CENSUS_CREATION_SAVED_V001_RESULT.md',CANON_C),
        (g,GCP,GNAME,'BS10_K33_GROWN_CONNECTION_V001_RESULT.md',CANON_G)):
        events=[json.loads(s) for s in (J/cpname/'events.jsonl').read_text().splitlines() if s]
        if not committed(events,'result_saved',sha256=ANC[resultname],canonical_payload_sha256=canonical):
            raise RuntimeError('Parent result commit missing')
        if not committed(events,'report_saved',sha256=ANC[reportname]):
            raise RuntimeError('Parent report commit missing')
        mh=ANC[cpname+'/manifest.json']
        if cpname==CCP and not committed(events,'manifest_saved',sha256=mh):
            raise RuntimeError('Census manifest commit missing')
        if cpname==GCP:
            if not committed(events,'started',manifest_sha256=mh):
                raise RuntimeError('Grown started commit missing')
            if not committed(events,'error',sha256=ANC[GCP+'/error.json']):
                raise RuntimeError('Preserved original formatter error commit missing')
            if not committed(events,'report_saved',sha256=ANC[reportname],recovered=True):
                raise RuntimeError('Grown report-only recovery commit missing')
        for row in parent['rows']:
            rel=cpname+'/'+row['key']+'.json'; rh=sha(J/rel)
            if json.loads((J/rel).read_text())!=row or row['failed_count']:
                raise RuntimeError('Original row mismatch: '+rel)
            if not committed(events,'row_complete',key=row['key'],sha256=rh,failed=0):
                raise RuntimeError('Original row journal seal missing: '+rel)
            custody[rel]=rh
    return cd,gd,custody


def value_display(x):
    return x['decimal20_floor']


def report(result):
    lines=['# Local proper-bond matched-reference scalar benchmark V001','',
           f"{result['status']}: {result['passed_count']}/{result['check_count']} arithmetic controls.",
           'New local-size family h3=h4=.2, matched once; original global-size results unchanged.',
           'All signed values refer to the same old N3 preparations and whole h0 response.',
           'No new target trajectory, physical pressure/volume/clock or superiority is inferred.','',
           '| State | raw norm | global work | local work | work difference | global leakage | local leakage | local P1 |',
           '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in result['rows']:
        cols=[r['key']]+[value_display(r[k]) for k in ('raw_state_norm_squared',
              'raw_global_work','raw_local_work','raw_work_difference','raw_global_leakage',
              'raw_local_leakage','raw_local_P1')]
        lines.append('| '+' | '.join(cols)+' |')
    lines += ['', 'All96 actual signed complete-h0 kernels, using the ORIGINAL initial normalization:', '',
              '| State | delay | global kernel | removed rest component | local kernel | difference |',
              '|---|---:|---:|---:|---:|---:|']
    for r in result['rows']:
        for p in r['kernels']:
            cols=[r['key'],p['delay']]+[value_display(p[k]) for k in
                  ('normalized_global_kernel','normalized_removed_rest_kernel',
                   'normalized_local_kernel','normalized_kernel_difference')]
            lines.append('| '+' | '.join(cols)+' |')
    lines += ['', 'Exact Fraction arithmetic applies to serialized parent numbers; their original',
              'floating/state qualifications remain conditional. No physically qualified sign',
              'effects are created from missing error budgets. Raw norms are kept; no state',
              'is renormalized. Local leakage increases; removing a signed kernel component',
              'can increase or decrease the response. Exact-zero occupied weights stay undefined.',
              'Only P1 and its existing error intervals scale4/3; no P2 or endpoint certificate',
              'is transferred. Separate delayed local mean-work terms are absent and uncomputed.', '',
              f"Runtime seconds: {result['runtime_seconds']:.9f}; PID: {result['pid']}.",
              f"Source SHA256: {result['source_sha256']}",
              f"Protocol SHA256: {result['protocol_sha256']}",
              f"Canonical payload SHA256: {result['canonical_payload_sha256']}", '',
              'Failed checks:']
    bad=[c['name'] for c in result['checks'] if not c['passed']]
    lines += ['- '+x for x in bad] if bad else ['None.']
    return '\n'.join(lines)+'\n'


def derive_row(c,g,checks):
    key=c['key']; first=len(checks)
    if (c['g'],c['start'],c['age']) != (g['g'],g['start'],g['age']):
        raise RuntimeError('Joined state metadata mismatch: '+key)
    ni=q(c['raw_norm']); ns=ni; ng=q(g['raw_norm_squared'])
    check(checks,key+'_positive_saved_norm',ni>0 and ng>0)
    equal(checks,key+'_two_parent_norms',ns,ng)
    equal(checks,key+'_same_original_complete_energy',c['original_complete_energy'],g['original_complete_energy'])
    equal(checks,key+'_same_encoded_initial_connection',c['raw_target_connected_probability'],g['raw_target_initial_connected_probability'])
    ts=c['work_terms']
    if set(ts)!=set(TERMS): raise RuntimeError('Missing mean-work scalar term: '+key)
    ts={k:q(v) for k,v in ts.items()}; wg=q(c['raw_unconditional_work']); removed=ts[REMOVED]
    equal(checks,key+'_global_mean_four_terms',wg,sum(ts.values(),F(0)))
    equal(checks,key+'_nonanchor_mean_coefficient',removed,F(1,20)*q(c['raw_Xrest']))
    equal(checks,key+'_rest_mean_Xsum',c['raw_Xrest'],sum((q(x) for x in c['X_values'][1:]),F(0)))
    equal(checks,key+'_anchor_mean_coefficient',ts['lost_old_anchor_flip'],F(1,5)*q(c['X_values'][0]))
    equal(checks,key+'_hopping_mean_coefficient',ts['removed_direct_hopping'],F(1,10)*q(c['raw_nT03']))
    equal(checks,key+'_baseline_mean_coefficient',ts['new_degree_baseline'],8*(ns-q(c['success_weight'])))
    wl=wg-removed; wl_route=sum((ts[k] for k in KEEP),F(0))
    equal(checks,key+'_local_mean_two_routes',wl,wl_route)
    equal(checks,key+'_local_mean_difference',wl-wg,-removed)
    kg=q(c['raw_target_leakage_squared']); cp=q(c['raw_n0_carrier_end_occupation'])
    equal(checks,key+'_old_leakage_operator',kg,F(9,50)*ns+F(1,100)*cp)
    kl=kg+F(7,50)*ns; kl_route=F(8,25)*ns+F(1,100)*cp
    equal(checks,key+'_local_leakage_two_routes',kl,kl_route)
    tol=ATOL*max(F(1),abs(kl),ns)
    check(checks,key+'_local_leakage_bounds',F(8,25)*ns-tol<=kl<=F(33,100)*ns+tol,
          raw_lower=rat(F(8,25)*ns),raw_upper=rat(F(33,100)*ns),allowance=rat(tol))
    check(checks,key+'_local_work_norm_bound',abs(wl)<=F(83,10)*ns+ATOL*max(F(1),abs(wl)))
    w=q(c['success_weight'])
    if w>0:
        eligible=F(1,10)*q(c['raw_nT03'])/w
        equal(checks,key+'_eligible_work_two_routes',eligible,
              q(c['eligible_conditional_work'])-F(1,20)*q(c['raw_PXrest'])/w)
        eligible_status='DEFINED_EXACT_POSITIVE_SAVED_WEIGHT'
    elif w==0:
        eligible=None;eligible_status='UNDEFINED_EXACT_ZERO_SAVED_WEIGHT'
        check(checks,key+'_old_zero_weight_null',c['eligible_conditional_work'] is None)
    else: raise RuntimeError('Negative saved weight')
    p1g=q(g['P1']); p1l=F(4,3)*p1g
    equal(checks,key+'_old_P1_normalization',g['normalized_stored_P1'],p1g/ng)
    b=g['bands']; rawband=[F(4,3)*q(x) for x in b['raw_stored_P1_band']]
    histband=[F(4,3)*q(x) for x in b['conditional_original_P1_band']]
    check(checks,key+'_P1_scaled_raw_interval',rawband[0]<=p1l<=rawband[1])
    check(checks,key+'_P1_scaled_history_interval_order',histband[0]<=histband[1])
    if q(c['age'])==0:
        blank=int(c['start'])==0
        equal(checks,key+'_basis_local_work',wl,8*ns if blank else 0)
        equal(checks,key+'_basis_local_leakage',kl,F(8,25)*ns if blank else F(33,100)*ns)
        equal(checks,key+'_basis_P1_null',p1l,0)
    cells=c['creation_work_source_response']
    if len(cells)!=6 or tuple(q(p['delay']) for p in cells)!=DELAYS:
        raise RuntimeError('Frozen six-delay source census mismatch: '+key)
    kernels=[]
    for p in cells:
        delay=q(p['delay']); label=key+'_delay'+str(delay)
        st=p['signed_source_kernel_terms']
        if set(st)!=set(TERMS): raise RuntimeError('Missing signed source scalar component')
        st={k:q(v) for k,v in st.items()}; rg=q(p['complete_h0_plus_source_kernel']); rr=st[REMOVED]
        rl=rg-rr; route=sum((st[k] for k in KEEP),F(0))
        equal(checks,label+'_old_kernel_sum',rg,sum(st.values(),F(0)))
        equal(checks,label+'_local_kernel_two_routes',rl,route)
        equal(checks,label+'_local_kernel_difference',rl-rg,-rr)
        scalar_allow=ATOL*(max(F(1),abs(rg))+max(F(1),abs(rr)))
        old_vector=q(p['induced_exact_arithmetic_kernel_error_ceiling'])
        check(checks,label+'_retained_old_conservative_Dnorm',q(p['D_norm_bound'])>=F(83,10))
        if delay==0:
            equal(checks,label+'_same_baseline_work',p['raw_creation_work'],wg)
        kernels.append({'delay':str(p['delay']), 'initial_norm_squared':rat(ni),
            'raw_delay_state_norm_squared':rat(q(p['raw_psi_norm_squared'])),
            'normalized_global_kernel':rat(rg),'normalized_removed_rest_kernel':rat(rr),
            'normalized_local_kernel':rat(rl),'normalized_kernel_difference':rat(rl-rg),
            'raw_global_numerator_kernel':rat(ni*rg),
            'raw_local_numerator_kernel':rat(ni*rl),
            'raw_numerator_kernel_difference':rat(ni*(rl-rg)),
            'route_residual':rat(rl-route), 'retained_old_exact_vector_kernel_ceiling':rat(old_vector),
            'additional_conditional_parent_scalar_allowance':rat(scalar_allow),
            'new_fraction_subtraction_roundoff':rat(0),
            'conditional_combined_bookkeeping_allowance':rat(old_vector+scalar_allow),
            'parent_floating_roundoff_certified':p['floating_roundoff_certified'],
            'physically_qualified_sign':False,'clock_corrected':False})
    result={'key':key,'g':str(c['g']),'start':int(c['start']),'age':str(c['age']),
        'initial_norm_squared':rat(ni),'raw_state_norm_squared':rat(ns),'grown_raw_state_norm_squared':rat(ng),
        'original_complete_energy':rat(q(c['original_complete_energy'])),
        'raw_global_work':rat(wg),'raw_removed_nonanchor_work':rat(removed),
        'raw_local_work':rat(wl),'raw_work_difference':rat(wl-wg),'mean_route_residual':rat(wl-wl_route),
        'normalized_global_work':rat(wg/ni),'normalized_local_work':rat(wl/ni),
        'normalized_work_difference':rat((wl-wg)/ni),'raw_global_leakage':rat(kg),
        'raw_local_leakage':rat(kl),'raw_leakage_difference':rat(kl-kg),
        'normalized_global_leakage':rat(kg/ni),'normalized_local_leakage':rat(kl/ni),
        'normalized_leakage_difference':rat((kl-kg)/ni),
        'raw_leakage_increment_formula':rat(F(7,50)*ns),
        'normalized_leakage_increment_formula':rat(F(7,50)*ns/ni),
        'unchanged_raw_encoded_connection':rat(q(c['raw_target_connected_probability'])),
        'unchanged_success_weight':rat(w),'eligible_work_status':eligible_status,
        'eligible_local_work':rat(eligible) if eligible is not None else None,
        'raw_global_P1':rat(p1g),'raw_local_P1':rat(p1l),
        'normalized_local_P1':rat(p1l/ng),'local_raw_stored_P1_band':band(rawband),
        'local_conditional_original_history_P1_band':band(histband),
        'scaled_P1_coefficient_arithmetic_allowance':rat(F(4,3)*q(b['coefficient_arithmetic_allowances'][1])),
        'P1_floating_budgets_conditional':b['floating_budgets_conditional'],
        'P1_directed_roundoff_certified':b['directed_roundoff_certified'],
        'no_P2_or_endpoint_transfer':True,'kernels':kernels,
        'physically_qualified_mean_sign':False,'checks':checks[first:],
        'failed_count':sum(not x['passed'] for x in checks[first:])}
    return result


def run():
    if Path(__file__).resolve()!=SOURCE or sys.platform!='darwin':
        raise RuntimeError('Sole source path on this Mac only')
    if any(p.exists() for p in (OUT,REPORT,RECEIPT,CP)):
        raise FileExistsError('Existing exclusive output; preserve without resume/rerun')
    started=utc();start=time.perf_counter();CP.mkdir();(CP/'events.jsonl').open('x').close()
    checks=[]; rows=[]
    try:
        c,g,custody=authenticate();source_hash=sha(SOURCE);protocol_hash=sha(PROTOCOL)
        manifest={'started_utc':started,'pid':os.getpid(),'host':socket.gethostname(),
            'source_sha256':source_hash,'protocol_sha256':protocol_hash,'input_sha256':custody,
            'old_array_references_inherited_only_no_NPZ_access':True,'scope':SCOPE,
            'parameters':{'h3':rat(F(1,5)),'old_h4':rat(F(3,20)),'local_h4':rat(F(1,5)),
                          'scalar_consistency_allowance':rat(ATOL)}}
        mh=exclusive_json(CP/'manifest.json',manifest);event('started',manifest_sha256=mh)
        check(checks,'exact16_parent_census',len(c['rows'])==len(g['rows'])==16)
        gm={r['key']:r for r in g['rows']}; cm={r['key']:r for r in c['rows']}
        row_sha={}
        for key in KEYS:
            row=derive_row(cm[key],gm[key],checks)
            row['elapsed_seconds']=time.perf_counter()-start
            rh=exclusive_json(CP/(key+'.json'),row);row_sha[key]=rh
            event('row_completed',key=key,sha256=rh,failed_count=row['failed_count'])
            rows.append(row)
        check(checks,'all96_source_kernel_cells',sum(len(r['kernels']) for r in rows)==96)
        for name,h in custody.items():
            if sha(J/name)!=h: raise RuntimeError('Input changed during new scalar benchmark: '+name)
        check(checks,'source_protocol_unchanged',sha(SOURCE)==source_hash and sha(PROTOCOL)==protocol_hash)
        failed=sum(not x['passed'] for x in checks)
        result={'status':'QUALIFIED_SAVED_SCALAR_ARITHMETIC' if not failed else 'FAILED_SAVED_SCALAR_ARITHMETIC',
            'scope':SCOPE,'started_utc':started,'finished_utc':utc(),'pid':os.getpid(),
            'runtime_seconds':time.perf_counter()-start,'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'source_sha256':source_hash,'protocol_sha256':protocol_hash,'input_sha256':custody,
            'manifest_sha256':mh,'row_sha256':row_sha,'rows':rows,'check_count':len(checks),
            'passed_count':len(checks)-failed,'failed_count':failed,'checks':checks,
            'old_global_results_unchanged':True,'delayed_local_mean_work':'MISSING_SEPARATE_SAVED_TERMS_NOT_COMPUTED',
            'P2_and_endpoint':'NOT_TRANSFERRED_NOT_COMPUTED','rerun_resume':False}
        result['canonical_payload_sha256']=canon(result)
        oh=exclusive_json(OUT,result);event('result_completed',sha256=oh,canonical_payload_sha256=result['canonical_payload_sha256'])
        with REPORT.open('x',encoding='utf-8') as f:
            f.write(report(result));f.flush();os.fsync(f.fileno())
        report_hash=sha(REPORT);event('report_completed',sha256=report_hash)
        receipt={'status':result['status'],'pid':os.getpid(),'passed_count':result['passed_count'],
            'check_count':len(checks),'failed_count':failed,'runtime_seconds':result['runtime_seconds'],
            'source_sha256':source_hash,'protocol_sha256':protocol_hash,'input_sha256':custody,
            'manifest_sha256':mh,'row_sha256':row_sha,'result_sha256':oh,'report_sha256':report_hash,
            'journal_sha256':sha(CP/'events.jsonl'),'canonical_payload_sha256':result['canonical_payload_sha256'],
            'scope':SCOPE,'rerun_resume':False}
        receipt_hash=exclusive_json(RECEIPT,receipt)
        print(json.dumps({'status':result['status'],'pid':os.getpid(),'checks':len(checks),'failed':failed,
                          'runtime_seconds':result['runtime_seconds'],'result_sha256':oh,'receipt_sha256':receipt_hash}))
        return 0 if not failed else 3
    except Exception as exc:
        error={'status':'ERROR_PRESERVED','utc':utc(),'pid':os.getpid(),'exception':repr(exc),
               'traceback':traceback.format_exc(),'completed_rows':[r['key'] for r in rows],
               'checks':checks,'partial_output_sha256':{p.name:sha(p) for p in (OUT,REPORT,CP/'manifest.json') if p.is_file()},
               'elapsed_seconds':time.perf_counter()-start,'rerun_resume':False}
        eh=exclusive_json(CP/'error.json',error);event('error_preserved',sha256=eh,exception=repr(exc))
        print(json.dumps({'status':'ERROR_PRESERVED','pid':os.getpid(),'exception':repr(exc),'error_sha256':eh}))
        return 2


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true',help='one root-reviewed new scalar launch')
    args=parser.parse_args()
    if not args.execute: parser.error('Explicit --execute requires root approval and fresh ownership check')
    sys.exit(run())
