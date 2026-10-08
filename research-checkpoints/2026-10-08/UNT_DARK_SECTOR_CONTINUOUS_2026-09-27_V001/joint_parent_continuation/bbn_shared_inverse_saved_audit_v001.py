"""Saved inverse-state and contour arithmetic; no interpolator/producer import."""
import hashlib,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    files={};seen=set();occurrences=0
    def manifest(p):
        nonlocal occurrences
        p=p.resolve();p.relative_to(ROOT)
        if p in seen:return
        seen.add(p);files[str(p.relative_to(ROOT))]=sha(p)
        for n,h in json.loads(p.read_text())['files'].items():
            occurrences+=1;q=Path(n)
            opts={x.resolve() for x in ([q] if q.is_absolute() else [ROOT/q,p.parent/q]) if x.is_file() and x.resolve().is_relative_to(ROOT)}
            assert len(opts)==1
            x=opts.pop();assert sha(x)==h;files[str(x.relative_to(ROOT))]=h
            if x.name.endswith('_FROZEN.json'):manifest(x)
    def load(stem):
        path=HERE/(stem+'_RESULTS.json');w=json.loads(path.read_text());f=HERE/(stem+'_FROZEN.json');manifest(f)
        assert w['freeze_sha256']==sha(f)
        canonical=w['payload']
        if stem=='BBN_TABLE_PROXY_V001':
            assert set(canonical['matched_Delta0'])=={str(i) for i in range(18)}
            canonical=dict(canonical,matched_Delta0={int(k):v for k,v in canonical['matched_Delta0'].items()})
        assert w['payload_sha256']==hashlib.sha256(enc(canonical)).hexdigest()
        return w['payload'],w
    p,wrapper=load('BBN_SHARED_INVERSE_V001');old,_=load('BBN_TABLE_PROXY_V001');cal,_=load('GLOBAL_GAP_LIMIT_CALIBRATION_V001')
    budget,_=load('FINITE_GAP_PHOTON_BUDGET_V001')
    assert p['configuration']==json.loads((HERE/'BBN_SHARED_INVERSE_V001_FROZEN.json').read_text())['configuration']
    assert not p['failures'] and not p['inherited_table_controls']['failures'] and p['parameter_count']==2
    assert p['observations']==old['observations'] and p['conserved_scalar_abundance_status']=='NOT_YET_QUALIFIED'
    checks=0;maxerr=0.;fails=[]
    def check(name,x,y,scale=None,tolerance=2e-11):
        nonlocal checks,maxerr
        checks+=1;den=max(abs(x),abs(y),1e-300) if scale is None else max(abs(scale),1e-300)
        err=abs(x-y)/den;maxerr=max(maxerr,err)
        if not math.isfinite(err) or err>tolerance:fails.append(dict(name=name,error=err,tolerance=tolerance))
    pts={v['point_id']:v for v in p['table_points']};bgs={b['background_id']:b for b in p['backgrounds']}
    cc={(v['background_id'],v['spectrum_index']):v for v in p['constants']}
    assert len(pts)==67 and set(pts)==set(range(67)) and len(bgs)==5 and len(cc)==20
    assert len(p['reference_mapping'])==18 and {r['reference'] for r in p['reference_mapping']}==set(range(18))
    for m in p['reference_mapping']:
        ref=cal['references'][m['reference']];bg=bgs[m['background_id']]
        assert m['old_bbn_marker']==ref['bbn'] and m['old_metadata']==ref['inherited_reference_input']
        check('background_H',bg['H0_s_inverse'],ref['H0_s_inverse']);check('background_vacuum',bg['Omega_Lambda'],ref['Omega_Lambda'])
        assert m['reference'] in bg['old_labels']
    assert len(p['coarse_Delta'])==17 and len(p['fine_Delta'])==33
    assert p['fine_Delta']==sorted(set(p['coarse_Delta']+[(a+b)/2 for a,b in zip(p['coarse_Delta'],p['coarse_Delta'][1:])]))
    geom={g['Delta']:g for g in p['contour_geometry']};assert set(geom)==set(p['fine_Delta'])
    for point in pts.values():
        x=point['omega_b'];D=point['Delta'];v=point['prediction'];g=geom[D]
        assert point['coarse_node']==(D in p['coarse_Delta']) and v['local_numerical_rectangle']==(.020<=x<=.024 and 0<=D<=3)
        for key,q in v['observables'].items():
            ob=p['observations'][key];res=q['prediction']-ob['value']
            check('signed_residual',q['signed_residual'],res,max(abs(q['prediction']),abs(ob['value'])))
            check('observed_sigma',q['observational_sigma'],ob['sigma']);assert q['theory_sigma']>0
            check('marginal_z',q['descriptive_marginal_z'],res/math.hypot(q['theory_sigma'],ob['sigma']),max(1.,abs(q['descriptive_marginal_z'])))
            check('matched_zero',q['minus_matched_Delta0'],q['prediction']-q['matched_Delta0'],q['prediction'])
        Y=v['observables']['helium']['prediction'];dh=v['observables']['deuterium']['prediction']
        check('Y_D_convention',v['helium_D_only_denominator_correction'],2*Y*dh*(1-Y)/(1+2*Y*dh),Y)
        check('He3_coefficient',v['helium_unprovided_He3_linear_coefficient'],3*Y*(1-Y)/(1+2*Y*dh)**2)
        for role in point['roles']:
            if role.startswith('central:'):
                key=role.split(':')[1];assert any(abs(x-y)<2e-13 for y in g['central'][key])
                check('central_residual',v['observables'][key]['signed_residual'],0.,p['observations'][key]['sigma'],tolerance=2e-8)
            else:
                _,k,n,end=role.split(':');check('joint_endpoint',x,g['joint_bands'][k][int(n)][0 if end=='lower' else 1],1.)
                for key,q in v['observables'].items():
                    excess=abs(q['signed_residual'])-int(k)*math.hypot(q['observational_sigma'],q['theory_sigma'])-q['interpolation_allowance']
                    check('joint_membership',max(excess,0.),0.,q['observational_sigma'],tolerance=2e-8)
    for g in geom.values():
        for k in ['1','2','3']:
            aa=g['marginal_bands']['helium'][k]['intervals'];bb=g['marginal_bands']['deuterium'][k]['intervals']
            raw=sorted([max(a,c),min(b,d)] for a,b in aa for c,d in bb if max(a,c)<=min(b,d))
            merged=[]
            for lo,hi in raw:
                if merged and lo<=merged[-1][1]+2e-13:merged[-1][1]=max(merged[-1][1],hi)
                else:merged.append([lo,hi])
            assert len(merged)==len(g['joint_bands'][k])
            for a,b in zip(merged,g['joint_bands'][k]):
                for x,y in zip(a,b):check('interval_intersection',x,y,1.)
    C4=(math.pi/(math.gamma(.25)*math.gamma(1.5)/math.gamma(1.75)))**(4/3);fnu=(7/8)*(4/11)**(4/3)
    check('C4',p['C4'],C4);check('fnu',p['fnu'],fnu)
    photons={r['reference']:r['Omega_gamma'] for r in budget['rows']};beta=p['configuration']['beta'];c=p['configuration']['c_m_s']
    for (bi,si),co in cc.items():
        bg=bgs[bi];sp=cal['spectra'][si]['spectrum'];kb=math.fsum(sp['weights'])+beta
        gs=p['configuration']['exposed_a0_m_s2']*3*math.pi/(16*kb);norm=1.5*kb*(c*bg['H0_s_inverse']/gs)**2
        for key,wanted in [('Kb',kb),('gstar',gs),('L',norm),('Omega_gamma',photons[bg['representative_reference']]),('target_DeltaU',norm*bg['Omega_Lambda'])]:check('constant_'+key,co[key],wanted)
    lookup={(r['point_id'],r['background_id'],r['spectrum_index']):r for r in p['state_rows']}
    assert len(lookup)==len(p['state_rows'])==len(pts)*5*4
    labels={};A=old['thermal_history_lower_bound_A_at_10keV'];th=old['thermal_interface'];lo,hi=th['log_ratio_all_T_intersection'];fine=th['per_resolution'][-1]
    hf=(7*math.pi**2/120)*(fine['sigma_bounds'][1]/(11*math.pi**2/45))**(4/3)/fine['plasma_rho_over_T4_bounds'][0]
    for r in p['state_rows']:
        point=pts[r['point_id']];bg=bgs[r['background_id']];co=cc[(r['background_id'],r['spectrum_index'])]
        x=point['omega_b'];Dlt=point['Delta'];ob=x/(bg['H0_km_s_Mpc']/100)**2;oe=bg['Omega_m']-ob;E=co['L']*oe;e=E/beta
        for key,val in [('omega_b',x),('Delta',Dlt),('Omega_b',ob),('Omega_exc',oe),('E',E),('DeltaU_target',co['target_DeltaU'])]:check('state_'+key,r[key],val)
        labels[r['status']]=labels.get(r['status'],0)+1
        if r['status']=='INFINITE_GAP_STANDARD_LIMIT':assert Dlt==0 and r['I'] is None and r['R'] is None and r['Q']==0;continue
        assert r['status']=='FINITE_HARD_STATE' and Dlt>0 and oe>0 and r['R']>1
        I=(Dlt*co['L']*co['Omega_gamma']*fnu/(beta*C4))**.75;R=r['R'];s=r['s'];b2=2*math.sqrt(e)*s
        check('I_target',r['I'],I);check('hard_energy',r['hard_energy'],e)
        check('s_gap',R*R,math.sqrt(e)*(1-s*s)/s);check('turning_energy',R*R*b2/2+b2*b2/4,e)
        pressure=r['pressure']/beta;om=r['omega'];eii=r['eII'];Q=beta*C4*I**(4/3);D=beta*R*R*math.sqrt(Q/beta)
        for key,val in [('w',pressure/e),('cI2',I*eii/om),('Q',Q),('D',D),('Q_over_E',Q/E),('DeltaU',co['target_DeltaU']),
            ('K0',3*beta*(e+pressure)/(R**4+4*e)),('J_static',beta*(om*om/eii+3*I*om)),('cold_parameter',e/R**4),
            ('J_cold',(4/3)*beta*R**4),('J_cold_from_proxy',(4/3)*beta*(e/I)**4),('source_hardening_ratio',r['S']/R**2),
            ('fractional_gap_energy_bound_at_10keV',D/(Q*A*A))]:check(key,r[key],val)
        check('action_virial',I*om,e+pressure)
        check('static_ratio',r['K0']/r['J_static'],3*r['cI2']/((R**4+4*e)*(1+3*r['cI2'])))
        assert r['source_hardening_sufficient']==(r['S']**2/R**4<1/12)
        q=Dlt*hf;expected=[min(0.,math.sqrt((1+q)/(1+q*math.exp(-lo)))-1),max(0.,math.sqrt((1+q)/(1+q*math.exp(-hi)))-1)]
        for v,w in zip(r['fixed_heating_fractional_H_envelope'],expected):check('H_envelope',v,w)
    for profile in p['sampled_profiles']:
        for mesh in ['coarse','fine']:
            eligible=[q for q in pts.values() if q['Delta'] in p[mesh+'_Delta'] and any(role.startswith('joint:'+str(profile['band_label'])+':') for role in q['roles'])]
            rr=[lookup[(q['point_id'],profile['background_id'],profile['spectrum_index'])] for q in eligible];ff=[r for r in rr if r['status']=='FINITE_HARD_STATE'];saved=profile[mesh]
            assert saved['sampled_boundary_points']==len(rr) and saved['finite_states']==len(ff)
            assert saved['includes_infinite_gap_limit']==any(r['status']=='INFINITE_GAP_STANDARD_LIMIT' for r in rr)
            assert saved['outside_local_interpolation_qualification_points']==sum(not q['prediction']['local_numerical_rectangle'] for q in eligible)
            for key,limits in saved['finite_ranges'].items():
                if not ff:assert limits is None
                else:
                    for i,f in enumerate([min,max]):check('profile_'+key,limits[i],f(r[key] for r in ff))
    for v in p['soft_resolution_contrasts']:
        aa,bb=v['spectrum_pair'];bi=v['background_id'];differences=[];mismatch=[]
        for q in pts.values():
            a=lookup[(q['point_id'],bi,aa)];b=lookup[(q['point_id'],bi,bb)]
            if a['status']!=b['status']:mismatch.append(q['point_id'])
            if a['status']==b['status']=='FINITE_HARD_STATE':differences.append({k:(a[k]-b[k])/abs(b[k]) for k in ['R','S','E','I','J_static','K0']})
        assert v['status_mismatches']==mismatch and v['matched_finite_states']==len(differences)
        for k,val in v['max_relative_differences'].items():check('resolution_'+k,val,max([abs(d[k]) for d in differences],default=0.),1.)
    return dict(status='PASS' if not fails else 'FAIL',source_sha256=sha(Path(__file__)),result_sha256=sha(HERE/'BBN_SHARED_INVERSE_V001_RESULTS.json'),
        freeze_sha256=wrapper['freeze_sha256'],payload_sha256=wrapper['payload_sha256'],
        ancestry=dict(unique_files=len(files),manifests=len(seen),member_occurrences=occurrences),checks=checks,max_scaled_error=maxerr,failures=fails,
        producer_checks=sum(p['counts'].values()),inherited_table_checks=sum(p['inherited_table_controls']['counts'].values()),
        table_points=len(pts),state_rows=len(lookup),state_statuses=labels,sampled_profiles=p['sampled_profiles'],
        producer_seconds=p['seconds'],producer_peak_self_rss_bytes=p['peak_self_rss_bytes'],
        scope='Saved evidence/arithmetic only. Does not re-evaluate table interpolation, marginal root isolation, inverse action quadrature or finite-R vacuum roots. Those remain preflighted source/producer controls, not a second numerical implementation.')
if __name__=='__main__':
    p=run();print(enc(dict(payload_sha256=hashlib.sha256(enc(p)).hexdigest(),payload=p)).decode())
