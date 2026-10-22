"""Hand-built target-free classifier records. No producer imports or execution.

Root-contract scaffolding comes from permitted B suite data B340/B342/B343.
Member arrays, score rows, bands and AT1 records below are independently authored
from the pinned producer source forms. They are synthetic classifier inputs,
not claims that any freeze or scientific computation occurred.
"""
import copy
import hashlib
import json
import math
import statistics
import subprocess
from pathlib import Path

ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
ROOT = ART / 'review_classifier_b_cx2'
BASE = ART / 'classifier_b_c2/build_c2v005/suite/run1'
DEST = ROOT / 'own_bundles_cx2v001'
Q = ['NGC3198-Q%02d' % i for i in range(1, 44)]
S0 = 'STAGE0_GRID_OUTER'
EBF = 'EVALUATED_BEFORE_FREEZE'
sources = {}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read(path):
    raw = path.read_bytes()
    sources[str(path)] = sha(raw)
    return raw

def enc(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)).encode()

def put(path, obj=None, raw=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = enc(obj) if raw is None else raw
    with path.open('xb') as f:
        f.write(raw)
    return {'path': path.name, 'sha256': sha(raw)}

def dist(counts):
    return dict(n=len(counts), min=min(counts), median=statistics.median(counts), max=max(counts))

def ladder(member, indexes, observed, sigma):
    rows = []
    for i in indexes:
        pred = member['speeds_km_s'][i]
        residual = None if pred is None else pred-observed[i]
        r = None if residual is None else residual/sigma[i]
        notes = []
        if r is not None and not math.isfinite(r):
            r = None
            notes.append('NON_FINITE_SIGMA_RATIO')
        frac = None if residual is None or observed[i] == 0 else residual/observed[i]
        if frac is not None and not math.isfinite(frac):
            frac = None
            notes.append('NON_FINITE_FRACTIONAL_ERROR')
        valid = member['row_valid'][i] and pred is not None
        hit = valid and r is not None and abs(r) <= 1
        reg = member['row_registration'][i]
        if reg:
            notes.append('INVALID_AS_MISS')
        rows.append(dict(id=Q[i], observed_speed_km_s=observed[i],
                         predicted_speed_km_s=pred, quoted_sigma_km_s=sigma[i],
                         signed_residual_km_s=residual, sigma_ratio=r,
                         fractional_error=frac, valid=valid, within_error=hit,
                         row_notes=notes,
                         status='INVALID' if reg else 'VALID' if valid else 'UNEVALUATED_OR_REFUSED',
                         prediction=None if reg else pred,
                         registered_reason=reg['reason'] if reg else None,
                         score_status='INVALID_AS_MISS' if reg else 'HIT' if hit else 'MISS',
                         tier='WITHIN_ERROR' if hit else 'MISS_WORST_TIER'))
    inv = [r['id'] for r in rows if r['score_status'] == 'INVALID_AS_MISS']
    out = {k:member[k] for k in ('member_id','log_index','role','evaluated','member_valid')}
    out.update(rows=rows, within_error_count=sum(r['within_error'] for r in rows),
               invalid_count=sum(not r['valid'] for r in rows), n_rows=len(rows),
               invalid_as_miss=inv, invalid_as_miss_count=len(inv))
    return out

def agreement(defect):
    # Forms: phase1_c2v003b L1185-1240, L1280-1295. All invented values.
    eqs = [dict(log_index=li, id=q, e_q=0.0, eps_m=0.0, flag=None, flag_reason=None)
           for li in (0,1) for q in Q[2:]]
    ext = [dict(direction=0, extent=[-0.25,0.25], lp_status=['OPTIMAL','OPTIMAL'])]
    rep = dict(rows_not_tested_phase1_not_available=Q[:2], e_q_per_member_row=eqs,
               rows_fd_noise_not_bounded=[], pairs_member_point_noise_not_bounded=[],
               ngc_linearity_residuals=[dict(log_index=e['log_index'],id=e['id'],
                                           ngc_linearity_residual=0.0) for e in eqs],
               envelope_vs_band_width={q:dict(phase2_envelope_width=0.0,phase1_band_width=10.0)
                                       for q in Q[2:]},
               max_ddo_linearity_deviation_over_tau=0.0,
               identified_projection_vs_linear_region=[
                   dict(direction=0,phase2_range=[0.0,0.0],linear_region=[-0.25,0.25],
                        lp_status=['OPTIMAL','OPTIMAL'],resolution_u=0.01,beyond_linear_region=False)],
               band_region_extent=ext,band_region_box_only_extent=copy.deepcopy(ext),
               band_region_single_point=False,band_region_single_point_reason=None)
    return dict(schema='PHASE1_AT1_C2V001',module='phase1_c2v003b',
                outcome='AGREEMENT_DEFECT' if defect else 'COVERED',
                at0=['FAIL' if defect else 'PASS','PASS'],
                e_q_reading='synthetic target-free allowance',
                failing=[],non_discriminating_rows=[],reported=rep,
                record_of_result='Phase 2 in every outcome',
                not_computed_here='target-dependent classifications')

def build(cid, baseid, mode):
    base = BASE/baseid
    bundle = json.loads(read(base/'BUNDLE.json'))
    docs, rawfiles, rawinputs = {}, {}, {}
    for role,pin in bundle['inputs'].items():
        if pin:
            p = base/pin['path']
            assert p.parent == base
            raw = read(p)
            assert sha(raw) == pin['sha256']
            docs[role] = json.loads(raw)
            rawinputs[role] = raw
    for group in ('rosters','sealed'):
        for key,pin in bundle[group].items():
            if isinstance(pin,dict) and set(pin) == {'path','sha256'}:
                p = base/pin['path']
                assert p.parent == base
                raw = read(p)
                assert sha(raw) == pin['sha256']
                rawfiles[pin['path']] = raw
    manifest = docs['freeze_manifest']
    ids = manifest['query_ids']
    assert ids == Q
    phase2 = baseid != 'B340'
    ratios = [0.0]*43
    invalid = {0:'QUERY_INSIDE_INNERMOST_NODE',1:'QUERY_INSIDE_INNERMOST_NODE'}
    observed, sigma = [100.0]*43, [5.0]*43
    if mode == 'boundary':
        ratios[2:6] = [-1.0,1.0,-1.000001,1.000001]
    if mode == 'deficit':
        ratios = [-3.0]*43
    if mode == 'mixed':
        ratios[35:] = [-3.0]*4 + [3.0]*4
    if mode == 'null':
        sigma[35:] = [1e-308]*8
    if mode == 'outercut':
        invalid.update({i:'QUERY_BEYOND_OUTER_GAS_CUT' for i in range(39,43)})
        ratios[35:39] = [-2.0]*4
    if mode in ('s0better','s0worse'):
        ratios[35:] = [-3.0]*8
    for members in [manifest['members']] + [
            a['members'] for a in manifest['alternative_results'].values() if 'members' in a]:
        for mem in members:
            mem['row_registration'] = [
                dict(status='INVALID',reason=invalid[i],registration=None) if i in invalid else None
                for i in range(43)]
            mem['row_valid'] = [i not in invalid for i in range(43)]
            mem['speeds_km_s'] = [
                None if i in invalid else 1e308 if mode == 'null' and i >= 35 else 100+5*ratios[i]
                for i in range(43)]
            mem['member_valid'] = mem['evaluated'] = mem['forward_valid_flag'] = True
            mem['reasons'] = []
            mem['exception'] = None
    if S0 in manifest['alternative_results']:
        for mem in manifest['alternative_results'][S0]['members']:
            for i in range(35,43):
                mem['speeds_km_s'][i] = 100.0 if mode == 's0better' else 80.0 if mode == 's0worse' else 100.0
    if 'stage0_status' in manifest:
        # Last terminal receipt defines step4; equality counts as before.
        manifest['stage0_status']['step4_start_utc'] = manifest['stage0_status']['members'][-1]['written_utc']
    env_label = 'POINTWISE_ENVELOPE_NOT_A_REALIZABLE_CURVE'
    sens_label = 'BOX_LIMITED_SENSITIVITY_BAND_FROM_REFERENCE_MEMBER_NOT_A_REALIZABLE_CURVE_NOT_HEADLINE'
    manifest['pointwise_envelope'] = []
    manifest['sensitivity']['per_query'] = []
    for i,q in enumerate(Q):
        vals = [mem['speeds_km_s'][i] for mem in manifest['members'] if mem['row_valid'][i]]
        lo,hi = (min(vals),max(vals)) if vals else (None,None)
        manifest['pointwise_envelope'].append(dict(id=q,band_low_km_s=lo,band_high_km_s=hi,
            valid=bool(vals),n_members=2,n_valid=len(vals),n_excluded_invalid=2-len(vals),
            n_unevaluated=0,label=env_label))
        manifest['sensitivity']['per_query'].append(dict(id=q,box_limited_band_low_km_s=lo,
            box_limited_band_high_km_s=hi,valid=bool(vals),reference_speed_km_s=lo,
            max_abs_delta_km_s=0.0 if vals else None,n_planned=0,n_valid=0,label=sens_label))
    score = docs['score']
    score['members'] = [ladder(m,range(43),observed,sigma) for m in manifest['members']]
    counts = [m['within_error_count'] for m in score['members']]
    score['headline'].update(counts_by_member={m['member_id']:m['within_error_count'] for m in score['members']},
                            member_within_error_counts=dist(counts),
                            reference_within_error_count=counts[0])
    for role,mrows,lk,hk in [
        ('pointwise_envelope',manifest['pointwise_envelope'],'band_low_km_s','band_high_km_s'),
        ('sensitivity',manifest['sensitivity']['per_query'],'box_limited_band_low_km_s','box_limited_band_high_km_s')]:
        rows=[]
        for i,r in enumerate(mrows):
            lo,hi,valid=r[lk],r[hk],r['valid']
            hit=bool(valid and lo <= observed[i]+sigma[i] and hi >= observed[i]-sigma[i])
            row=dict(id=Q[i],band_low_km_s=lo,band_high_km_s=hi,valid=valid,
                     band_overlaps_error_bar=hit,label=r['label'],
                     score_status='BAND_OVERLAP' if hit else 'BAND_MISS' if valid else 'INVALID_AS_MISS',
                     tier='WITHIN_ERROR' if hit else 'MISS_WORST_TIER')
            if role=='sensitivity':
                row.update(reference_speed_km_s=r['reference_speed_km_s'],max_abs_delta_km_s=r['max_abs_delta_km_s'])
            rows.append(row)
        score[role].update(rows=rows,band_overlap_count=sum(r['band_overlaps_error_bar'] for r in rows),
                           invalid_count=sum(not r['valid'] for r in rows))
    for a in score['alternatives']:
        if a['role']=='NON_PRIMARY' and a['scored']:
            indexes=range(35,43) if a['name']==S0 else range(43)
            a['members']=[ladder(m,indexes,observed,sigma)
                          for m in manifest['alternative_results'][a['name']]['members']]
            a['member_within_error_counts']=dist([m['within_error_count'] for m in a['members']])
    l1 = docs.get('l1_record')
    if l1:
        l1['rows'] = []
        for i,q in enumerate(Q):
            if i in invalid or (mode=='unavailable' and i==9):
                l1['rows'].append(dict(id=q,status='NOT_AVAILABLE',reason='INVALID_AT_u_A' if i in invalid else 'LP_INFEASIBLE_INFEASIBLE'))
                continue
            lo,hi=(95.0,95.0) if mode=='touch' else (95.0,105.0)
            l1['rows'].append(dict(id=q,status='AVAILABLE',lo=lo,hi=hi,width=hi-lo,
                g_A=100.0,K_q=[0.0,0.0],K_q_VI=[0.0],K_q_near_null={'1':0.0},
                lp_status={'band_min':'OPTIMAL','band_max':'OPTIMAL','allowance_min':'OPTIMAL','allowance_max':'OPTIMAL'},
                du_at_lo=[0.0,0.0],du_at_hi=[0.0,0.0],a_q=0.0,eps_q=0.0,
                fd_noise='FD_NOISE_NOT_BOUNDED' if mode=='fdnoise' else {'lo':0.0,'hi':0.0},
                non_discriminating=hi==lo))
        l1['n_available']=sum(r['status']=='AVAILABLE' for r in l1['rows'])
    if phase2:
        docs['agree_record']=agreement(mode=='at1defect')
        bundle['phase1_tool']={'module':'phase1_c2v003b','sha256':'7d891ff7d81b0e9d103707d79c7a057cedc6dc1e893a0f4e9372a51d0b796dd4'}
        bundle['inputs']['phase1_classification']=None
        docs.pop('phase1_classification',None)
        docs['phase_inputs']['phase1_classification_absent_reason']='NO_PHASE_1_SCORE'
    out=DEST/cid
    # Never mutate source or existing case files. Dependencies are sealed in memory
    # before each file's single exclusive creation.
    for name,raw in rawfiles.items():
        put(out/name,raw=raw)
    if l1:
        pin=put(out/bundle['inputs']['l1_record']['path'],l1)
        bundle['inputs']['l1_record']=pin
        if docs['phase_inputs']['phase1_header']:
            docs['phase_inputs']['phase1_header']['l1_sha256']=pin['sha256']
    manifest.pop('manifest_sha256')
    manifest['manifest_sha256']=sha(enc(manifest))
    mpin=put(out/bundle['inputs']['freeze_manifest']['path'],manifest)
    bundle['inputs']['freeze_manifest']=mpin
    for key in ('manifest_file_sha256_actual','manifest_file_sha256_expected','manifest_file_sha256_registered'):
        score[key]=mpin['sha256']
    score['manifest_sha256_self']=manifest['manifest_sha256']
    for role,doc in docs.items():
        if role in ('l1_record','freeze_manifest'): continue
        old=bundle['inputs'][role]
        bundle['inputs'][role]=put(out/old['path'],doc) if role in ('score','phase_inputs','agree_record') else put(out/old['path'],raw=rawinputs[role])
    bp=put(out/'BUNDLE.json',bundle)
    return dict(id=cid,mode=mode,base_scaffold=baseid,bundle=str(out/'BUNDLE.json'),sha256=bp['sha256'])

def main():
    specs=[
        ('H01_boundary','B340','boundary'),('H02_global_deficit','B340','deficit'),
        ('H03_outer_mixed','B340','mixed'),('H04_null_ratio','B340','null'),
        ('H05_outer_cut','B340','outercut'),('H06_unavailable_band','B340','unavailable'),
        ('H07_inclusive_band_touch','B340','touch'),('H08_fd_noise','B340','fdnoise'),
        ('H09_stage0_improves','B342','s0better'),('H10_stage0_worsens','B342','s0worse'),
        ('H11_at1_agreement_defect','B342','at1defect'),('H12_no_successor','B343','no_successor')]
    rows=[build(*s) for s in specs]
    index=dict(date_u=subprocess.check_output(['/bin/date','-u'],text=True).strip(),
               label='TESTED: construction only; classification pending',n=len(rows),cases=rows,
               source_files=[dict(path=k,sha256=v) for k,v in sorted(sources.items())],
               independence='Root scaffolding reused; member/score/band/AT1 fields authored here. No producer imported or executed.',
               scope='Classifier-form synthetic fixtures only; not verified full production freeze custody.')
    put(ROOT/'OWN_BUNDLE_INDEX_CX2V001.json',index)
    print(json.dumps({'n':len(rows),'index':str(ROOT/'OWN_BUNDLE_INDEX_CX2V001.json')}))

if __name__=='__main__':
    main()
