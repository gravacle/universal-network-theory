"""Saved arithmetic/custody audit only. No producer import, roots or quadrature."""
import base64
import hashlib
import json
import math
from pathlib import Path
import zlib

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
NAME = 'FINITE_FIELD_PHASE_RESPONSE_V001'
EXPECTED_TRANSPORT = '18788e16f5575da64a7e6ed527179bd7142b9cd42ce3d814f98642c81e76a3a2'


def encode(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transport(path):
    t=json.loads(path.read_text()); d=zlib.decompressobj()
    raw=d.decompress(base64.b64decode(t['data'],validate=True))+d.flush()
    assert d.eof and not d.unused_data and not d.unconsumed_tail
    assert t['encoding']=='zlib_base64_canonical_json'
    assert len(raw)==t['raw_bytes'] and hashlib.sha256(raw).hexdigest()==t['raw_sha256']
    v=json.loads(raw)
    assert hashlib.sha256(encode(v['payload'])).hexdigest()==v['payload_sha256']
    return t,v


def main():
    tp=HERE/(NAME+'_TRANSPORT.json'); assert sha(tp)==EXPECTED_TRANSPORT
    t,v=transport(tp); p=v['payload']; frozen=HERE/(NAME+'_FROZEN.json')
    assert sha(frozen)==v['freeze_sha256']
    files={}; manifests=set(); occurrences=0
    def manifest(path):
        nonlocal occurrences
        path=path.resolve(); path.relative_to(ROOT)
        if path in manifests:return
        manifests.add(path)
        for name,digest in json.loads(path.read_text())['files'].items():
            raw=Path(name)
            options=[raw] if raw.is_absolute() else [ROOT/raw,path.parent/raw]
            candidates={x.resolve() for x in options if x.resolve().is_relative_to(ROOT) and x.is_file()}
            assert len(candidates)==1,(path,name)
            member=candidates.pop(); assert sha(member)==digest,member
            files[str(member.relative_to(ROOT))]=digest; occurrences+=1
            if member.name.endswith('_FROZEN.json'):manifest(member)
    manifest(frozen)
    assert p['status']=='COMPLETE' and p['failures']==[]
    assert len(p['rows'])==1296 and len(p['baselines'])==144
    assert p['branch_counts']=={'OCCUPIED':1296}
    assert sum(p['counts'].values())==109232==t['summary']['checks']
    assert t['summary']['rows']==1296 and t['summary']['failures']==0
    oldt,oldv=transport(HERE/'FINITE_GAP_SHARED_SCREEN_V002_TRANSPORT.json')
    old=oldv['payload']; globalv=json.loads((HERE/'GLOBAL_GAP_LIMIT_CALIBRATION_V001_RESULTS.json').read_text())
    globalp=globalv['payload']
    assert oldv['freeze_sha256']==sha(HERE/'FINITE_GAP_SHARED_SCREEN_V002_FROZEN.json')
    assert globalv['payload_sha256']==hashlib.sha256(encode(globalp)).hexdigest()
    expected={(s,r,R,g,Phi) for s in range(4) for r in range(18) for R in [128,8192]
              for g in [1e-12,1e-10,1e-8] for Phi in [0.,-1e-8,-1e-7]}
    assert {(r['spectrum_index'],r['reference'],r['R'],r['physical_g_m_s2'],r['Phi']) for r in p['rows']}==expected
    bases={r['source_row_index']:r for r in p['baselines']}
    assert len(bases)==144
    counts={}; maxima={}; failures=[]; stable_differences=[]; ulp_ratios=[]
    def ck(name,a,b,scale=None,tol=2e-11):
        scale=max(abs(a),abs(b),1e-300) if scale is None else max(abs(scale),1e-300)
        error=abs(a-b)/scale
        counts[name]=counts.get(name,0)+1; maxima[name]=max(maxima.get(name,0),error)
        if not math.isfinite(error) or error>tol:failures.append(dict(check=name,error=error,tolerance=tol))
    beta=.005; lightspeed=299792458.; parsec=3.085677581491367e16
    for row in p['rows']:
        src=old['rows'][row['source_row_index']]; R=row['R']; G=row['G']; S=row['S']; kb=row['Kb']
        assert (src['spectrum_index'],src['reference'],src['R'])==(row['spectrum_index'],row['reference'],R)
        for key,oldkey in [('DeltaU','DeltaU'),('S','S'),('cosmic_I','I'),('cosmic_E','E'),('cosmic_static_length_pc','static_length_pc'),('gstar_m_s2','gstar')]:
            ck('inherited_'+key,row[key],src[oldkey])
        spec=globalp['spectra'][row['spectrum_index']]['spectrum']; ws=math.fsum(spec['weights'])
        ck('owned_contact',kb,ws+beta)
        ck('physical_acceleration_units',G*src['gstar'],row['physical_g_m_s2'])
        h=G/math.sqrt(1+(G/S)**2); hp=(h/G)**3; hpp=-3*h**5/(G**4*S*S)
        ck('bounded_eta',row['eta'],h/R**2)
        ck('certificate',row['all_field_certificate_margin'],1-12*(S/R**2)**2)
        assert row['all_field_certificate_margin']>0
        base=bases[row['source_row_index']]
        target=base['stable_omega_excess']*math.exp(-row['Phi'])+math.expm1(-row['Phi'])
        ck('stable_target',row['target_omega_excess'],target)
        for label,obj,phase in [('phase',row,True),('fixed',row['same_g_fixed_cosmic_I'],False)]:
            o=obj['hard']; a=obj['response']; soft=a['soft']; scale=o['epsilon_exc']+abs(o['epsilon_min'])
            ck(label+'_center',o['c']*(1+o['r']**2+o['c']**2),o['eta'])
            ck(label+'_absolute_minimum',a['hard_absolute_minimum'],beta*R**4*o['epsilon_min'])
            ck(label+'_energy_ledger',o['epsilon'],o['epsilon_min']+o['epsilon_exc'],scale)
            ck(label+'_Iomega',o['i']*o['omega'],o['epsilon']+o['pressure'],scale)
            ck(label+'_virial',2*o['kinetic'],o['mean2']+o['mean4']-o['eta']*o['b'],scale)
            ck(label+'_pressure_moments',o['pressure'],o['mean4']/4+o['eta']*o['b']/2)
            ck(label+'_mean_equation',o['b']+o['mean3'],o['eta'])
            ck(label+'_eII',o['eii'],o['omega_r']/o['i_r'])
            ck(label+'_bI',o['b_i'],-o['mean3_r']/o['i_r'])
            deficit=o['mean3_eta']-o['mean3_r']*o['i_eta']/o['i_r']
            ck(label+'_fixed_deficit',o['susceptibility_deficit_fixed_i'],deficit)
            square=o['b_i']**2/o['eii']; ck(label+'_square',o['square_correction'],square)
            ck(label+'_Maxwell',o['b_i'],-o['omega_eta']+o['omega_r']*o['i_eta']/o['i_r'],max(abs(o['b_i']),abs(o['eta'])))
            ck(label+'_soft_contact',soft['deficit']+soft['B'],ws*h)
            ck(label+'_soft_energy',soft['Pi'],-soft['E'])
            B=soft['B']+beta*R**2*o['b']; F=hp*B
            chi=ws-soft['susceptibility_deficit']+beta*(1-deficit)
            kl_local=kb-hpp*B-hp*hp*chi
            kl=kl_local-(hp*hp*beta*square if phase else 0.)
            kt=kb-F/G
            ck(label+'_F',a['F'],F)
            ck(label+'_KT_direct',a['K_transverse'],kt,kb)
            ck(label+'_KL_direct',a['K_longitudinal'],kl,kb)
            ck(label+'_same_local_KL',a['K_longitudinal_same_local_fixed_I'],kl_local,kb)
            ck(label+'_normalized_D',a['D_normalized'],G-F/kb,G)
            ck(label+'_D_over_G',a['D_over_G'],a['D_normalized']/G)
            ck(label+'_hard_E',a['hard_E'],beta*R**4*o['epsilon'])
            ck(label+'_hard_Pi',a['hard_Pi'],beta*R**4*o['pressure'])
            ck(label+'_hard_excitation',a['hard_excitation_above_local_min'],beta*R**4*o['epsilon_exc'])
            ck(label+'_E',a['E'],soft['E']+a['hard_E'],abs(soft['E'])+abs(a['hard_E']))
            ck(label+'_Pi',a['Pi'],soft['Pi']+a['hard_Pi'])
            ck(label+'_active_source',a['E_plus_3Pi'],a['E']+3*a['Pi'],abs(a['E'])+3*abs(a['Pi']))
            ck(label+'_h',a['h'],h); ck(label+'_hp',a['h_prime'],hp); ck(label+'_hpp',a['h_second'],hpp)
            if phase:
                J=beta*R**4*(o['omega']**2/o['eii']+3*o['i']*o['omega'])
                fp=-hp*beta*R**2*o['omega']*o['b_i']/o['eii']
                ck('J_physical',a['J_static'],J); ck('F_Phi_physical',a['F_Phi'],fp)
                ck('phase_frequency',o['omega_excess'],target)
                ck('action_ratio',row['hard_I_over_cosmic_I'],R**3*o['i']/src['I'])
                ck('action_units',row['hard_I'],R**3*o['i'])
                for axis,key in [('transverse','K_transverse'),('longitudinal','K_longitudinal')]:
                    length=lightspeed**2/src['gstar']*math.sqrt(a[key]/J)/parsec
                    ck('length_'+axis,row['local_lengths'][axis+'_pc'],length)
                assert row['elliptic_local']==(a['K_transverse']>0 and a['K_longitudinal']>0)
            else:
                ck('fixed_cosmic_action',R**3*o['i'],src['I'])
                ck('fixed_no_phase_J',a['J_static'],0.,1.)
        a=row['response']; b=row['same_g_fixed_cosmic_I']['response']
        reported=row['signed_D_over_G_difference_from_fixed_Ib']
        ck('published_signed_difference',reported,a['D_over_G']-b['D_over_G'],1.)
        stable=hp*beta*R**2/(kb*G)*(row['hard']['mean3']-row['same_g_fixed_cosmic_I']['hard']['mean3'])
        budget=math.ulp(a['D_over_G'])+math.ulp(b['D_over_G'])
        ratio=abs(stable-reported)/budget; ulp_ratios.append(ratio)
        ck('stable_signed_difference_vs_rounded',stable,reported,budget,tol=2.)
        stable_differences.append(stable)
    def bounds(seq): return [min(seq),max(seq)]
    def signs(seq): return dict(negative=sum(x<0 for x in seq),zero=sum(x==0 for x in seq),positive=sum(x>0 for x in seq))
    groups=[]
    for R in [128,8192]:
        for g in [1e-12,1e-10,1e-8]:
            for Phi in [0.,-1e-8,-1e-7]:
                indexes=[n for n,r in enumerate(p['rows']) if (r['R'],r['physical_g_m_s2'],r['Phi'])==(R,g,Phi)]
                rs=[p['rows'][n] for n in indexes]; assert len(rs)==72
                diffs=[r['signed_D_over_G_difference_from_fixed_Ib'] for r in rs]
                stable=[stable_differences[n] for n in indexes]
                groups.append(dict(R=R,physical_g_m_s2=g,Phi=Phi,rows=len(rs),
                    action_ratio=bounds([r['hard_I_over_cosmic_I'] for r in rs]),
                    hard_energy_over_cosmic_E=bounds([r['response']['hard_E']/r['cosmic_E'] for r in rs]),
                    hard_excitation_over_cosmic_E=bounds([r['response']['hard_excitation_above_local_min']/r['cosmic_E'] for r in rs]),
                    D_over_G=bounds([r['response']['D_over_G'] for r in rs]),
                    longitudinal_pc=bounds([r['local_lengths']['longitudinal_pc'] for r in rs]),
                    transverse_pc=bounds([r['local_lengths']['transverse_pc'] for r in rs]),
                    signed_fixed_Ib_difference=bounds(diffs),published_signs=signs(diffs),
                    stable_same_saved_moment_difference=bounds(stable),stable_signs=signs(stable)))
    assert len(p['summaries'])==len(groups)==18
    for summary,group in zip(p['summaries'],groups):
        assert (summary['R'],summary['physical_g_m_s2'],summary['Phi'])==(group['R'],group['physical_g_m_s2'],group['Phi'])
        ck('summary_action_min',summary['hard_I_over_cosmic_I'][0],group['action_ratio'][0])
        ck('summary_action_max',summary['hard_I_over_cosmic_I'][1],group['action_ratio'][1])
        ck('summary_force_min',summary['ranges']['D_over_G'][0],group['D_over_G'][0])
        ck('summary_force_max',summary['ranges']['D_over_G'][1],group['D_over_G'][1])
    receipt=dict(status='PASS' if not failures else 'FAIL',scope='Independent saved scalar algebra and custody only; no source import, quadrature, action/frequency root, propagation or empirical fit.',
        custody=dict(transport_sha256=sha(tp),raw_sha256=t['raw_sha256'],raw_bytes=t['raw_bytes'],
            payload_sha256=v['payload_sha256'],freeze_sha256=sha(frozen),new_freeze_members=len(json.loads(frozen.read_text())['files']),
            unique_authenticated_files=len(files),recursive_manifests=len(manifests),member_occurrences=occurrences,
            source_sha256=sha(HERE/'finite_field_phase_response_v001.py'),
            protocol_sha256=sha(HERE/'FINITE_FIELD_PHASE_RESPONSE_PROTOCOL_V001.md'),
            output_recovery_note_sha256=sha(HERE/(NAME+'_OUTPUT_RECOVERY.md'))),
        producer=dict(rows=1296,checks=sum(p['counts'].values()),max_reported_error=max(p['maxima'].values()),
            seconds=p['seconds'],peak_self_rss_bytes=p['peak_self_rss_bytes'],branch_counts=p['branch_counts'],
            elliptic_rows=sum(r['elliptic_local'] for r in p['rows']),
            normalized_action_range=bounds([r['hard']['i'] for r in p['rows']]),
            normalized_source_range=bounds([r['eta'] for r in p['rows']]),
            phase_square_range=bounds([r['response']['longitudinal_phase_square'] for r in p['rows']])),
        audit=dict(checks=sum(counts.values()),counts=counts,maxima=maxima,failures=failures,
            maximum_signed_difference_ULP_budget= max(ulp_ratios)),
        groups=groups,global_signed_differences=signs([r['signed_D_over_G_difference_from_fixed_Ib'] for r in p['rows']]),
        stable_moment_signed_differences=signs(stable_differences),
        limits='Moment integrals and alternate quadrature arrays are not independently regenerated. Hard action/energy ratios are not full gravitating-density contrasts: absolute baseline, soft energy, acceleration-polarization and its spatial divergence remain in the full equations. Local lengths are not galaxy radii or solution/stability certificates.')
    print(json.dumps(receipt,sort_keys=True,indent=2,allow_nan=False))


if __name__=='__main__':main()
