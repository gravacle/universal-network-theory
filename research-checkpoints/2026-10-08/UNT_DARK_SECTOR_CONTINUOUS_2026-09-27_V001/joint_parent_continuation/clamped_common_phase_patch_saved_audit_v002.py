"""Independent saved-array arithmetic only; no producer/material import."""
import os
for _name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_name]='1'
import sys
sys.dont_write_bytecode=True
import base64, hashlib, json, math, zlib
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
FREEZE=HERE/'CLAMPED_COMMON_PHASE_PATCH_V001_FROZEN.json'

def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def original_sources():
    t=json.loads((HERE/'FINITE_GAP_SHARED_SCREEN_V002_TRANSPORT.json').read_text())
    decoder=zlib.decompressobj()
    raw=decoder.decompress(base64.b64decode(t['data'],validate=True))+decoder.flush()
    assert decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail
    assert len(raw)==t['raw_bytes'] and hashlib.sha256(raw).hexdigest()==t['raw_sha256']
    v=json.loads(raw);p=v['payload']
    assert v['payload_sha256']==hashlib.sha256(encode(p)).hexdigest()
    assert v['freeze_sha256']==sha(HERE/'FINITE_GAP_SHARED_SCREEN_V002_FROZEN.json')
    rows={r['R']:r for r in p['rows'] if r['spectrum_index']==1 and r['reference']==0 and r['R'] in [128,8192]}
    assert set(rows)=={128,8192}
    return rows

def ancestry():
    seen=set();files={};occurrences=0
    def walk(p):
        nonlocal occurrences
        p=p.resolve();p.relative_to(ROOT)
        if p in seen:return
        seen.add(p);files[str(p.relative_to(ROOT))]=sha(p)
        for name,wanted in json.loads(p.read_text())['files'].items():
            occurrences+=1;q=Path(name)
            options=[q] if q.is_absolute() else [ROOT/q,p.parent/q]
            paths={x.resolve() for x in options if x.resolve().is_relative_to(ROOT) and x.is_file()}
            if len(paths)!=1:raise RuntimeError('Missing/ambiguous ancestor '+name)
            q=paths.pop();actual=sha(q)
            if actual!=wanted:raise RuntimeError('Frozen bytes differ '+str(q))
            files[str(q.relative_to(ROOT))]=actual
            if q.name.endswith('_FROZEN.json'):walk(q)
    walk(FREEZE)
    return dict(manifests=len(seen),unique_files=len(files),member_occurrences=occurrences,files=files)

def audit(path,sources):
    t=json.loads(path.read_text());decoder=zlib.decompressobj()
    raw=decoder.decompress(base64.b64decode(t['data'],validate=True))+decoder.flush()
    assert decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail
    assert t['encoding']=='zlib_base64_canonical_json'
    assert len(raw)==t['raw_bytes'] and hashlib.sha256(raw).hexdigest()==t['raw_sha256']
    wrapper=json.loads(raw);p=wrapper['payload']
    assert wrapper['freeze_sha256']==sha(FREEZE)
    assert wrapper['payload_sha256']==hashlib.sha256(encode(p)).hexdigest()
    assert p['configuration']==json.loads(FREEZE.read_text())['configuration']
    assert (p['R'],p['L'],p['n'])==[(r,l,n) for r in [128,8192] for l in [1.,2.] for n in [16,32]][p['case_index']]
    assert p['source_row']==sources[p['R']]
    checks={};fail=[];count=0
    def check(name,left,right,scale=1.,tol=2e-11):
        nonlocal count
        a,b,s=np.broadcast_arrays(np.asarray(left,dtype=float),np.asarray(right,dtype=float),np.asarray(scale,dtype=float))
        err=np.abs(a-b)/np.maximum(np.abs(s),1e-300);count+=err.size
        if not err.size:
            checks[name]=dict(comparison_count=0,maximum_scaled_error=None,tolerance=tol,passed=True,status='EMPTY_MASK_NO_COMPARISON')
            return
        maximum=float(np.max(err));ok=bool(np.all(np.isfinite(err)) and maximum<=tol)
        checks[name]=dict(maximum_scaled_error=maximum,tolerance=tol,passed=ok)
        if not ok:fail.append(name)
    reported=[]
    for name,c in p['checks'].items():
        passed=math.isfinite(c['error']) and c['error']<=c['tolerance']
        assert passed==c['passed']
        if not passed:reported.append(name)
    assert sorted(reported)==sorted(p['failures'])
    edges=np.asarray(p['edges']);width=np.diff(edges);area=np.diff(edges**2)/2
    volume=area[:,None]*width[None,:];sheet=1/np.sqrt(1+edges[:-1]**2)-1/np.sqrt(1+edges[1:]**2)
    check('total_volume',np.sum(volume),p['L']**3/2,p['L']**3/2)
    check('sheet_total',np.sum(sheet),1-1/math.sqrt(1+p['L']**2))
    eps=p['epsilon_scale'];kb=p['Kb'];base=p['cosmic_baseline'];summaries=[]
    if p['status']=='FAILED_PREREQUISITES':
        assert p['outcomes']==[] and p['unstarted_seeds']==[1.,2.]
    else:assert [o['seed_multiplier'] for o in p['outcomes']]==[1.,2.]
    for o in p['outcomes']:
        prefix='seed'+str(o['seed_multiplier'])+'_';u=np.asarray(o['u']);assert u.shape==volume.shape
        summary=dict(seed=o['seed_multiplier'],status=o['status'],history_records=len(o['history']),
            actual_accepted_updates=sum('accepted_residual' in x for x in o['history']),
            u_range=[float(u.min()),float(u.max())],Phi_range=[float(eps*u.min()),float(eps*u.max())])
        if 'material' not in o:summaries.append(summary);continue
        m={k:np.asarray(v) for k,v in o['material'].items()}
        assert all(v.shape==u.shape for v in m.values())
        scale=np.maximum.reduce([np.abs(m['E']),np.abs(m['hard_min'])+m['hard_excitation'],np.full_like(u,abs(base['Tb']))])
        check(prefix+'E_split',m['E'],m['hard_E']+m['soft_E'],scale)
        check(prefix+'Pi_split',m['Pi'],m['hard_Pi']-m['soft_E'],scale)
        check(prefix+'hard_split',m['hard_E'],m['hard_min']+m['hard_excitation'],scale)
        check(prefix+'deltaE',m['deltaE'],m['E']-base['Eb'],scale)
        check(prefix+'deltaPi',m['deltaPi'],m['Pi']-base['Pib'],scale)
        check(prefix+'deltaT',m['deltaT'],m['deltaE']+3*m['deltaPi'],scale)
        check(prefix+'deltaT_parts',m['deltaT'],m['deltaT_soft']+m['deltaT_hard'],scale)
        check(prefix+'soft_reaction',m['deltaT_soft'],-2*m['soft_E'],scale)
        check(prefix+'hard_reaction',m['deltaT_hard'],m['hard_E']+3*m['hard_Pi']-base['hard_Eb']-3*base['hard_Pib'],scale)
        check(prefix+'I_ratio',m['I_over_Ib'],m['I']/base['Ib'],np.maximum(1,np.abs(m['I_over_Ib'])))
        omega=p['R']*base['unit']['omega']*np.exp(-eps*u)
        check(prefix+'phase_energy',m['hard_E']+m['hard_Pi'],.005*m['I']*omega,scale)
        occupied=m['branch']==1
        predicted_J=np.zeros_like(u)
        predicted_J[occupied]=.005*(omega[occupied]**2/m['eII'][occupied]+3*m['I'][occupied]*omega[occupied])
        check(prefix+'J_phase',m['J'],predicted_J,np.maximum(1,np.abs(m['J'])))
        gr=np.asarray(o['gradients']['radial']);gz=np.asarray(o['gradients']['vertical']);g=np.hypot(gr,gz)
        check(prefix+'contact_identity',m['KT']*g,kb*g-m['F'],np.maximum(1,kb*g))
        om=o['omitted_estimates'];gf=g*m['F'];er=np.divide(gr,g,out=np.zeros_like(g),where=g>0);ez=np.divide(gz,g,out=np.zeros_like(g),where=g>0)
        for name,wanted in [('gF',gf),('Kb_g_squared',kb*g*g),('pressure_trace',3*m['deltaPi']),('anisotropic_RR',-gf*er*er),('anisotropic_Rz',-gf*er*ez),('anisotropic_zz',-gf*ez*ez)]:
            check(prefix+'omitted_'+name,om[name],wanted,np.maximum(1,np.abs(wanted)))
        check(prefix+'max_Phi',om['max_abs_Phi'],np.max(np.abs(eps*u)))
        for part in ['','_soft','_hard']:
            check(prefix+'volume_source'+part,o['volume_source'+part],eps/kb*np.sum(volume*m['deltaT'+part]),max(abs(o['sheet_flux']),abs(o['volume_source'])))
        check(prefix+'sheet_flux',o['sheet_flux'],np.sum(sheet))
        check(prefix+'ledger',o['flux_balance'],o['outer_flux']-o['sheet_flux']-o['volume_source'],max(abs(o['sheet_flux']),abs(o['volume_source'])))
        check(prefix+'action_inventory',o['dimensionless_per_copy_action_inventory'],np.sum(volume*m['I']),max(1,abs(o['dimensionless_per_copy_action_inventory'])))
        for axis,key in [('transverse','KT'),('longitudinal','KL')]:
            valid=(m[key]>0)&(m['J']>0);saved=np.asarray(o['local_lengths'][axis+'_valid']);assert np.array_equal(valid,saved)
            ell=np.sqrt(m[key][valid]/m['J'][valid])/eps
            stored=np.asarray(o['local_lengths'][axis+'_length_over_a'],dtype=float)
            ratio=np.asarray(o['local_lengths'][axis+'_width_over_length'],dtype=float)
            check(prefix+axis+'_length',stored[valid],ell,np.maximum(ell,1e-300))
            check(prefix+axis+'_resolution',ratio[valid],np.maximum(width[:,None],width[None,:])[valid]/ell,np.maximum(np.abs(ratio[valid]),1e-300))
            summary[axis+'_width_over_length_range']=[float(np.min(ratio[valid])),float(np.max(ratio[valid]))] if np.any(valid) else None
        directions=[x for x in o['directional_checks'] if x['status']=='CHECKED']
        assert o['jacobian_checked_comparisons']==len(directions)
        assert o['jacobian_qualified']==(len(directions)==4 and all(x['error']<=p['configuration']['directional_tolerance'] for x in directions))
        if o['sheet_normal']['status']=='BRACKETED_LOCAL_INVERSION':
            s=o['sheet_normal'];target=sheet/area
            check(prefix+'sheet_bin_targets',s['target_bin_average'],target,target)
            check(prefix+'sheet_recovered',s['recovered'],target,target,tol=p['configuration']['quadrature_tolerance'])
        summary.update(residual=o['residual'],jacobian_qualified=o['jacobian_qualified'],
            I_ratio_range=[float(m['I_over_Ib'].min()),float(m['I_over_Ib'].max())],
            J_range=[float(m['J'].min()),float(m['J'].max())],
            KT_range=[float(m['KT'].min()),float(m['KT'].max())],KL_range=[float(m['KL'].min()),float(m['KL'].max())],
            volume_source=o['volume_source'],volume_source_soft=o['volume_source_soft'],volume_source_hard=o['volume_source_hard'],
            outer_flux=o['outer_flux'],sheet_flux=o['sheet_flux'],flux_balance=o['flux_balance'])
        summaries.append(summary)
    if len(p['outcomes'])==2:
        difference=float(np.max(np.abs(np.asarray(p['outcomes'][0]['u'])-np.asarray(p['outcomes'][1]['u']))))
        check('seed_difference',p['two_seed_max_u_difference'],difference)
    return dict(case_index=p['case_index'],R=p['R'],L=p['L'],N=p['n'],
        transport_sha256=sha(path),raw_sha256=t['raw_sha256'],payload_sha256=wrapper['payload_sha256'],
        raw_bytes=len(raw),producer_status=p['status'],producer_checks=len(p['checks']),producer_failures=p['failures'],
        audit_status='PASS' if not fail else 'FAIL',arithmetic_checks=count,failures=fail,checks=checks,
        summaries=summaries,seconds=p['seconds'],peak_self_rss_bytes=p['peak_self_rss_bytes'])

if __name__=='__main__':
    if len(sys.argv)<2:raise RuntimeError('Supply explicit saved case paths; no producer is invoked.')
    paths=[Path(p).resolve() for p in sys.argv[1:]]
    for p in paths:p.relative_to(ROOT)
    ancestors=ancestry();sources=original_sources()
    results=[audit(p,sources) for p in paths]
    p=dict(status='PASS' if all(r['audit_status']=='PASS' for r in results) else 'FAIL',
        source_sha256=sha(Path(__file__)),producer_freeze_sha256=sha(FREEZE),ancestry=ancestors,cases=results,
        scope='Saved-array/custody arithmetic, not independent orbit quadrature, Jacobian evaluation, PDE solution, boundary formation, grid resolution, uniqueness or observed-galaxy validation.')
    print(encode(dict(payload_sha256=hashlib.sha256(encode(p)).hexdigest(),payload=p)).decode())
