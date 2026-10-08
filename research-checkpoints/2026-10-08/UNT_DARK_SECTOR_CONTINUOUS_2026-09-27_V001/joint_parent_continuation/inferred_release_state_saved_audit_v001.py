"""Independent saved scalar/geometry arithmetic; no producer or derivative reevaluation."""
import hashlib,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
def enc(o):return json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files={};manifests=set();occurrences=0
def member(p,digest=None):
    p=p.resolve(strict=True);p.relative_to(ROOT);d=sha(p)
    assert digest is None or d==digest
    files[str(p.relative_to(ROOT))]=d;return p
def manifest(p):
    global occurrences
    p=member(p)
    if p in manifests:return
    manifests.add(p)
    for name,d in json.loads(p.read_text())['files'].items():
        raw=Path(name);opts=[raw] if raw.is_absolute() else [ROOT/raw,p.parent/raw]
        found={x.resolve() for x in opts if x.is_file() and x.resolve().is_relative_to(ROOT)}
        assert len(found)==1;q=member(found.pop(),d);occurrences+=1
        if q.name.endswith('_FROZEN.json'):manifest(q)
def packet(stem,digest=None):
    p=member(HERE/(stem+'_RESULTS.json'),digest);o=json.loads(p.read_text());f=member(HERE/(stem+'_FROZEN.json'));manifest(f)
    assert o['freeze_sha256']==sha(f) and o['payload_sha256']==hashlib.sha256(enc(o['payload'])).hexdigest()
    return o['payload']
out=packet('INFERRED_RELEASE_STATE_MAP_V001','46179beab779ff242d1c72a6f694ae2f27c93394264f1bbbc820e47b507f2962')
inv=packet('BBN_SHARED_INVERSE_V001','e05fd83e221897bafb4f8dbe46cc737dc8fef4f5ed11fdf122a7053bac3a02e0')
old=packet('SMOOTH_DISK_RELEASE_CERTIFICATE_V001','773a3b57065e9c4fb6894064b6402e31f761dfe1de8beeb0754701c29ef24a04')
counts={};maxima={};failures=[]
def ck(name,x,y,scale=None):
    den=max(abs(x),abs(y),1e-300) if scale is None else max(abs(scale),1e-300)
    er=abs(x-y)/den;counts[name]=counts.get(name,0)+1;maxima[name]=max(maxima.get(name,0.),er)
    if not math.isfinite(er) or er>2e-11:failures.append(dict(check=name,error=er))
def yes(name,x):ck(name,int(bool(x)),1,1)
cfg=out['configuration'];c=cfg['c_m_s'];G=cfg['G_m3_kg_s2'];a=cfg['a_kpc']*1000*cfg['parsec_m']
yes('result_status',out['status']=='COMPLETE' and not out['failures'])
co={(r['background_id'],r['spectrum_index']):r for r in inv['constants']}
bg={r['background_id']:r for r in inv['backgrounds']};points={r['point_id']:r for r in inv['table_points']}
rows=[dict(zip(out['state_columns'],r)) for r in out['states']]
maps=[dict(zip(out['mapping_columns'],r)) for r in out['mappings']]
geos=out['geometry_bases'];glookup={};signs={}
yes('source_metadata',out['backgrounds']==inv['backgrounds'] and out['constants']==inv['constants'])
yes('counts',len(rows)==1340 and len(maps)==2680 and len(geos)==8)
for gi,g in enumerate(geos):
    si,b=g['spectrum_index'],g['b_over_a'];glookup[(si,b)]=gi
    original=next(x for x in old['geometries'] if x['b_over_a']==b)
    gs=co[(0,si)]['gstar'];eps=gs*a/c**2;U=eps/(2*(1+b));dmax=original['density_max']
    gradient_bound=3*math.pi*eps*dmax*(1/(2*math.pi*dmax))**(1/3)
    for key,val in [('gstar',gs),('epsilon',eps),('compactness',U),('dimensionless_metric_gradient_bound',gradient_bound)]:ck('geometry_'+key,g[key],val)
    yes('contraction',g['contraction_qualified']==(U<1));yes('geometry_witness_census',len(g['points'])==16)
    neg=pos=zero=0
    for p,q in zip(original['points'],g['points']):
        d=p['density'];grad=p['density_gradient'];lap=p['density_laplacian'];u=-eps*p['potential']/2
        eg=4*math.pi*(8*U*math.hypot(*grad)+6*d*gradient_bound)
        el=4*math.pi*(10*U*abs(lap)+10*gradient_bound*math.hypot(*grad)+30*d*gradient_bound**2+12*math.pi*eps*d*d)
        expected=[p['x'],p['z'],2*math.pi*d/(1+u)**6,2*math.pi*d,-2*math.pi*grad[0]/3,-2*math.pi*grad[1]/3,eg/6,
                  math.pi*lap/6,math.pi*lap/6-el/24,math.pi*lap/6+el/24]
        for j,(x,y) in enumerate(zip(q,expected)):ck('geometry_basis_'+str(j),x,y)
        neg+=q[9]<0;pos+=q[8]>0;zero+=q[8]<=0<=q[9]
    signs[str(gi)]=dict(negative=neg,positive=pos,contains_zero=zero)
for i,(src,r) in enumerate(zip(inv['state_rows'],rows)):
    yes('state_association',r['source_index']==i and all(r[k]==src[k] for k in ('point_id','background_id','spectrum_index','R')))
    bi,si=r['background_id'],r['spectrum_index'];const=co[(bi,si)];bgg=bg[bi];gs=const['gstar'];kb=const['Kb'];eps=gs*a/c**2;td=math.sqrt(a/gs)
    finite=src['status']=='FINITE_HARD_STATE';ci,w,p=(src['cI2'],src['w'],src['pressure']) if finite else (0.,0.,0.)
    du=src['DeltaU'] if finite else src['DeltaU_target'];stress=gs**2/(4*math.pi*G*kb)
    rho=stress*src['E']/c**2;vac=stress*du/c**2
    for key,value in [('cI2',ci),('w',w),('Xi',ci/eps),('t_dyn_seconds',td),('rho_H_kg_m3',rho),('p_H_Pa',stress*p),('rho_vac_kg_m3',vac)]:ck('state_'+key,r[key],value)
    ck('cosmic_density',rho,3*bgg['H0_s_inverse']**2*src['Omega_exc']/(8*math.pi*G))
    ck('cosmic_vacuum',vac,3*bgg['H0_s_inverse']**2*bgg['Omega_Lambda']/(8*math.pi*G))
    ck('enthalpy_pressure',r['p_H_Pa'],rho*c**2*w)
    if finite:
        yes('finite_status',r['status']=='FINITE')
        ck('sound_time',r['t_sound_over_t_dyn_or_null_infinite'],math.sqrt(eps/ci))
        ck('intrinsic_response',ci,src['I']*src['eII']/src['omega'])
        ck('action_enthalpy',cfg['beta']*src['I']*src['omega'],src['E']+p)
        ck('frequency_H_coefficient',r['omega_phys_over_H_times_tau_seconds_or_null'],src['omega']/bgg['H0_s_inverse'])
        ck('frequency_dyn_coefficient',r['omega_phys_t_dyn_times_tau_seconds_or_null'],src['omega']*td)
    else:
        yes('dust_limit_semantics',r['status']=='EXACT_MACRO_DUST_LIMIT' and rho>0 and r['R'] is None and
            r['t_sound_over_t_dyn_or_null_infinite'] is None and r['omega_phys_over_H_times_tau_seconds_or_null'] is None and r['omega_phys_t_dyn_times_tau_seconds_or_null'] is None)
seen=set()
for m in maps:
    i,gi=m['source_index'],m['basis_index'];r=rows[i];g=geos[gi];gs=g['gstar'];td=r['t_dyn_seconds'];ci=r['cI2'];rho=r['rho_H_kg_m3']
    yes('map_association',(i,gi) not in seen and g['spectrum_index']==r['spectrum_index']);seen.add((i,gi))
    d=rho*(1+r['w'])*gs/a
    expect={'density_tau2_scale_kg_m3_s2':d,'pressure_tau2_scale_Pa_s2':c**2*ci*d,
            'velocity_tau3_scale_m_s4':c**2*ci*gs/a**2,'current_tau4_scale_s4':c**2*ci*gs/a**3}
    for key,val in expect.items():ck('map_'+key,m[key],val)
expected={(i,glookup[(r['spectrum_index'],b)]) for i,r in enumerate(rows) for b in (.125,.0625)}
yes('full_mapping',seen==expected)
for case in old['cases']:
    g=geos[glookup[(old['configuration']['spectrum_index'],case['b_m']/case['a_m'])]]
    gs=case['source_state']['gstar'];td=math.sqrt(a/gs);ci=case['source_state']['cI2'];vscale=c*c*ci*gs/a**2;pscale=vscale/a
    for q,p in zip(g['points'],case['points']):
        for j in range(2):
            ck('original64_focusing',q[2+j]/td**2,p['fractional_density_tau2_interval'][j])
            ck('original64_velocity',q[4+j]*vscale,p['orthonormal_velocity_tau3_m_s4_leading'][j])
            ck('original64_current_interval',q[8+j]*pscale,p['canonical_current_tau4_s4_interval'][j])
        ck('original64_velocity_bound',q[6]*vscale,p['orthonormal_velocity_tau3_norm_error_m_s4'])
        ck('original64_current',q[7]*pscale,p['canonical_current_tau4_s4_leading'])
yes('ranking',out['summary']['complete_increasing_Xi_source_indices']==sorted(range(len(rows)),key=lambda i:(rows[i]['Xi'],i)))
yes('finite_dust_counts',sum(r['status']=='FINITE' for r in rows)==1180 and sum(r['status']=='EXACT_MACRO_DUST_LIMIT' for r in rows)==160)
def summary(rr):
    def span(k):return [min(r[k] for r in rr),max(r[k] for r in rr)]
    finite=[r for r in rr if r['status']=='FINITE']
    return dict(count=len(rr),finite=len(finite),Xi=span('Xi'),cI2=span('cI2'),density_kg_m3=span('rho_H_kg_m3'),
        finite_sound_over_dyn=[min(r['t_sound_over_t_dyn_or_null_infinite'] for r in finite),max(r['t_sound_over_t_dyn_or_null_infinite'] for r in finite)],
        dynamical_seconds=span('t_dyn_seconds'))
groups={'all':summary(rows)}
for tag,prefix in [('joint_any','joint:'),('central','central:')]+[(f'joint_{k}',f'joint:{k}:') for k in (1,2,3)]:
    for finite in (False,True):
        rr=[r for r in rows if any(x.startswith(prefix) for x in points[r['point_id']]['roles']) and (not finite or r['status']=='FINITE')]
        groups[tag+('_finite' if finite else '_including_limits')]=summary(rr)
receipt=dict(status='PASS_SAVED_ARITHMETIC' if not failures else 'FAILED',scope='Saved derivatives/scalars only; no source differentiation, quadrature, mode inversion or propagation.',
    files=files,unique_files=len(files),recursive_manifests=len(manifests),manifest_member_occurrences=occurrences,
    checks=counts,maxima=maxima,failures=failures,total_checks=sum(counts.values()),summary_groups=groups,
    geometry_current_interval_signs=signs,producer_checks=sum(out['checks'].values()),producer_seconds=out['elapsed_seconds'],producer_peak_self_rss_bytes=out['peak_bytes'])
print(json.dumps(receipt,sort_keys=True,indent=2,allow_nan=False))
