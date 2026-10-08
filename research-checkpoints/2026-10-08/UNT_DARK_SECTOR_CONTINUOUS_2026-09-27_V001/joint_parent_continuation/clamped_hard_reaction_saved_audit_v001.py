"""Independent saved-array audit only: no producer/material imports or solves."""
import base64
import hashlib
import json
import math
from pathlib import Path
import zlib

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
COUNTER=HERE/'CLAMPED_HARD_REACTION_ATTRIBUTION_V001_FROZEN.json'
PHYSICAL=HERE/'CLAMPED_COMMON_PHASE_PATCH_V001_FROZEN.json'
counts={};maxima={};failures=[];members={};manifests=set()
def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(name,a,b=0.,scale=1.,tol=2e-11):
    err=abs(a-b)/max(abs(scale),1e-300)
    counts[name]=counts.get(name,0)+1;maxima[name]=max(maxima.get(name,0.),err)
    if not math.isfinite(err) or err>tol:failures.append(dict(check=name,error=err,tolerance=tol))
def yes(name,b):check(name,int(bool(b)),1)
def manifest(p):
    p=p.resolve();p.relative_to(ROOT)
    if p in manifests:return
    manifests.add(p);members[str(p.relative_to(ROOT))]=sha(p)
    for name,h in json.loads(p.read_text())['files'].items():
        q=Path(name);choices=set()
        for x in ([q] if q.is_absolute() else [ROOT/q,p.parent/q]):
            try:x=x.resolve(strict=True);x.relative_to(ROOT)
            except (ValueError,FileNotFoundError):continue
            if x.is_file():choices.add(x)
        yes('manifest_unique_member',len(choices)==1)
        if len(choices)!=1:raise RuntimeError(name)
        x=choices.pop();yes('manifest_hash',sha(x)==h)
        members[str(x.relative_to(ROOT))]=h
        if x.name.endswith('_FROZEN.json'):manifest(x)
def packet(p,freeze):
    t=json.loads(p.read_text());yes('transport_encoding',t['encoding']=='zlib_base64_canonical_json')
    decoder=zlib.decompressobj();raw=decoder.decompress(base64.b64decode(t['data'],validate=True))+decoder.flush()
    yes('compression_integrity',decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail)
    yes('raw_hash',hashlib.sha256(raw).hexdigest()==t['raw_sha256'])
    check('raw_bytes',len(raw),t['raw_bytes'])
    w=json.loads(raw);d=w['payload']
    yes('wrapper_freeze',w['freeze_sha256']==sha(freeze))
    yes('wrapper_payload',w['payload_sha256']==hashlib.sha256(encode(d)).hexdigest())
    return d,dict(path=str(p.relative_to(ROOT)),transport_sha256=sha(p),
                  raw_sha256=t['raw_sha256'],payload_sha256=w['payload_sha256'])
def flat(a):return [v for row in a for v in row]
def integrate(w,a):return math.fsum(x*y for x,y in zip(w,a))
def metric(a,b,w):
    dif=[y-x for x,y in zip(a,b)];tot=math.fsum(w)
    rms=lambda x:math.sqrt(integrate(w,[v*v for v in x])/tot)
    first,second,d=rms(a),rms(b),rms(dif)
    return dict(weighted_RMS_difference=d,symmetric_relative_RMS=2*d/(first+second) if first+second else 0.,
        max_absolute_difference=max(map(abs,dif)),signed_difference_range=[min(dif),max(dif)],
        first_RMS=first,second_RMS=second)
manifest(COUNTER);manifest(PHYSICAL)
cf=json.loads(COUNTER.read_text());pf=json.loads(PHYSICAL.read_text())
yes('control_configuration',cf['configuration']['hard_reaction_multiplier']==0.)
records=[];producer_checks=0;qualified_pairs=0
for i,old_index in enumerate([0,2,4,6]):
    d,custody=packet(HERE/f'CLAMPED_HARD_REACTION_ATTRIBUTION_V001_CASE_{i:03d}.json',COUNTER)
    old,oldcustody=packet(HERE/f'CLAMPED_COMMON_PHASE_PATCH_V001_CASE_{old_index:03d}.json',PHYSICAL)
    yes('case_identity',d['attribution_case_index']==i and d['case_index']==old_index and d['n']==16
        and (d['R'],d['L'])==[(128,1.),(128,2.),(8192,1.),(8192,2.)][i])
    yes('same_source_and_geometry',all(d[k]==old[k] for k in ['R','L','n','source_row','edges','centres','DeltaU','Kb','cosmic_baseline','epsilon_scale']))
    yes('physical_receipt',d['physical_result_custody']=={k:oldcustody[k] for k in ['path','transport_sha256','raw_sha256','payload_sha256']})
    yes('configuration',d['attribution_configuration']==cf['configuration'] and d['configuration']==pf['configuration'])
    yes('census',[o['seed_multiplier'] for o in d['outcomes']]==[1.,2.] and len(d['paired_comparisons'])==2)
    for name,c in d['checks'].items():
        producer_checks+=1
        yes('producer_check_reclassification',c['passed']==(math.isfinite(c['error']) and c['error']<=c['tolerance']))
    yes('producer_failed_list',d['failures']==[k for k,v in d['checks'].items() if not v['passed']])
    n=d['n'];ed=d['edges'];width=[b-a for a,b in zip(ed,ed[1:])]
    areas=[(b*b-a*a)/2 for a,b in zip(ed,ed[1:])]
    weight=[ar*dz for ar in areas for dz in width]
    check('volume_geometry',math.fsum(weight),d['L']**3/2)
    eps,Kb=d['epsilon_scale'],d['Kb'];outcomes=[]
    check('epsilon_units',eps,d['source_row']['gstar']*d['a_m']/d['configuration']['c_m_s']**2,eps)
    for oi,o in enumerate(d['outcomes']):
        oo=old['outcomes'][oi];pair=d['paired_comparisons'][oi];m=o['material'];bm=d['cosmic_baseline']
        yes('converged_control',o['status']=='CONVERGED')
        yes('all_four_directional',o['jacobian_checked_comparisons']==4 and len(o['directional_checks'])==4
            and all(c['status']=='CHECKED' and c['error']<=d['configuration']['directional_tolerance'] for c in o['directional_checks']))
        for arr in [o['u'],*o['gradients'].values(),*m.values()]:
            yes('array_shape_finite',len(arr)==n and all(len(row)==n for row in arr)
                and all(math.isfinite(v) for v in flat(arr)))
        wscale=max(o['sheet_flux'],abs(o['volume_source']),abs(o['full_model_volume_source_on_counterfactual']))
        src=[eps/Kb*v for v in flat(m['deltaT_hard'])]
        soft=[eps/Kb*v for v in flat(m['deltaT_soft'])]
        for a,b in zip(src,flat(o['removed_hard_source_density'])):check('removed_source_density',a,b,max(abs(a),1e-300))
        hard_int=integrate(weight,src);soft_int=integrate(weight,soft)
        check('recorded_hard_source',hard_int,o['recorded_but_removed_hard_volume_source'],wscale)
        check('soft_source',soft_int,o['volume_source_soft'],wscale)
        check('applied_soft_only',soft_int,o['volume_source'],wscale)
        check('zero_hard_applied',o['volume_source_hard_applied'])
        check('physical_volume_source',hard_int+soft_int,o['full_model_volume_source_on_counterfactual'],wscale)
        physical_res=flat(o['full_model_residual_on_counterfactual'])
        control_res=[a+b for a,b in zip(physical_res,src)]
        cnorm=integrate(weight,list(map(abs,control_res)))/o['sheet_flux']
        pnorm=integrate(weight,list(map(abs,physical_res)))/o['sheet_flux']
        check('counter_residual_norm',cnorm,o['residual'],1.)
        check('physical_residual_norm',pnorm,o['full_model_residual_norm_on_counterfactual'],max(pnorm,1.))
        check('counter_global_residual',integrate(weight,control_res),o['flux_balance'],wscale)
        check('physical_global_residual',integrate(weight,physical_res),o['full_model_flux_balance_on_counterfactual'],wscale)
        check('counter_flux_ledger',o['outer_flux']-o['sheet_flux']-soft_int,o['flux_balance'],wscale)
        check('physical_flux_ledger',o['outer_flux']-o['sheet_flux']-hard_int-soft_int,o['full_model_flux_balance_on_counterfactual'],wscale)
        check('flux_defect_sign',o['full_model_flux_balance_on_counterfactual']-o['flux_balance'],-hard_int,wscale)
        check('action_inventory',integrate(weight,flat(m['I'])),o['dimensionless_per_copy_action_inventory'],o['dimensionless_per_copy_action_inventory'])
        for j in range(n*n):
            E,Pi,hardE,softE,hardPi=[flat(m[k])[j] for k in ['E','Pi','hard_E','soft_E','hard_Pi']]
            scale=max(abs(E),abs(Pi),abs(hardE),abs(softE),abs(bm['Tb']),1e-300)
            check('energy_split',E,hardE+softE,scale)
            check('hard_min_plus_excitation',hardE,flat(m['hard_min'])[j]+flat(m['hard_excitation'])[j],scale)
            check('delta_energy',flat(m['deltaE'])[j],E-bm['Eb'],scale)
            check('delta_pressure',flat(m['deltaPi'])[j],Pi-bm['Pib'],scale)
            check('reaction_split',flat(m['deltaT'])[j],flat(m['deltaT_hard'])[j]+flat(m['deltaT_soft'])[j],scale)
            check('reaction_energy_pressure',flat(m['deltaT'])[j],flat(m['deltaE'])[j]+3*flat(m['deltaPi'])[j],scale)
            check('hard_reaction',flat(m['deltaT_hard'])[j],hardE+3*hardPi-bm['hard_Eb']-3*bm['hard_Pib'],scale)
            check('action_ratio',flat(m['I_over_Ib'])[j],flat(m['I'])[j]/bm['Ib'],max(flat(m['I_over_Ib'])[j],1))
            for axis,key in [('transverse','KT'),('longitudinal','KL')]:
                kval,J=flat(m[key])[j],flat(m['J'])[j]
                valid=kval>0 and J>0
                yes('length_validity',flat(o['local_lengths'][axis+'_valid'])[j]==valid)
                if valid:
                    ell=math.sqrt(kval/J)/eps
                    check('length_full_material_J',ell,flat(o['local_lengths'][axis+'_length_over_a'])[j],ell)
                    check('width_full_material_length',max(width[j//n],width[j%n])/ell,
                          flat(o['local_lengths'][axis+'_width_over_length'])[j],max(1,max(width)/ell))
        fields={'u':(flat(oo['u']),flat(o['u']))}
        for ax in ['radial','vertical']:
            a,b=flat(oo['gradients'][ax]),flat(o['gradients'][ax])
            fields[ax+'_G']=(a,b)
            fields[ax+'_m_s2']=([v*d['source_row']['gstar'] for v in a],[v*d['source_row']['gstar'] for v in b])
        for name in ['I','I_over_Ib','deltaT_hard','deltaT_soft','deltaT','hard_E','hard_Pi']:
            fields[name]=(flat(oo['material'][name]),flat(m[name]))
        for name,(a,b) in fields.items():
            mm=metric(a,b,weight);reported=pair['metrics_physical_to_counterfactual'][name]
            scale=max(mm['first_RMS'],mm['second_RMS'],1e-300)
            for key in mm:
                av=mm[key] if isinstance(mm[key],list) else [mm[key]]
                bv=reported[key] if isinstance(reported[key],list) else [reported[key]]
                for x,y in zip(av,bv):
                    check('paired_'+key,x,y,1. if key=='symmetric_relative_RMS' else scale)
        qualified=(oo['status']=='CONVERGED' and o['status']=='CONVERGED'
                   and oo['jacobian_qualified'] and o['jacobian_qualified']
                   and not d['failures'] and not old['failures'])
        yes('qualified_pair_flag',pair['equilibrium_comparison_qualified']==qualified)
        qualified_pairs+=qualified
        outcomes.append(dict(seed=o['seed_multiplier'],status=o['status'],physical_status=oo['status'],
            qualified_pair=qualified,iterations=len(o['history']),residual=o['residual'],
            hard_omitted_over_sheet=hard_int/o['sheet_flux'],
            physical_residual_on_control=pnorm,
            radial_relative_RMS=pair['metrics_physical_to_counterfactual']['radial_G']['symmetric_relative_RMS'],
            vertical_relative_RMS=pair['metrics_physical_to_counterfactual']['vertical_G']['symmetric_relative_RMS'],
            I_over_Ib_range=[min(flat(m['I_over_Ib'])),max(flat(m['I_over_Ib']))]))
    records.append(dict(case=i,physical_case=old_index,R=d['R'],L=d['L'],custody=custody,
        physical_custody=oldcustody,checks=len(d['checks']),outcomes=outcomes,
        seconds=d['seconds_including_attribution_checks'],rss=d['peak_self_rss_bytes']))
print(json.dumps(dict(status='PASS' if not failures else 'FAIL',audit_code_sha256=sha(Path(__file__)),
    counts=counts,maxima=maxima,failures=failures,independent_checks=sum(counts.values()),
    producer_checks=producer_checks,qualified_pairs=qualified_pairs,
    manifests=len(manifests),distinct_ancestor_files=len(members),ancestor_hashes=members,
    attribution_freeze_sha256=sha(COUNTER),physical_freeze_sha256=sha(PHYSICAL),cases=records,
    limitations=['No physical producer/material/PDE/orbit re-evaluation.',
                 'Saved full Jacobians/face quadrature tensors absent: their producer checks are authenticated, not independently recomputed.',
                 'Inherited local_lengths use the full material J, not the reaction-deleted control operator.',
                 'Counterfactual convergence is not an original-action equilibrium or nonexistence proof.']),
    sort_keys=True,separators=(',',':'),allow_nan=False))
