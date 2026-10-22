"""Claude3 BLIND derivation of D7 recovery R2 by the sealed W1 rule (prereg V005 amendment_v005.d7_recovery.W1_widening_rule),
from the failed calls' column failure + iteration files only. Written before reading Claude2's R2. Opens no result.json/finish.json."""
import json, glob, os, hashlib, sys
C2="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2"
V5='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
pre=json.load(open(f'{V5}/KMAX_MATRIX_PREREG_V005.json')); d7=pre['amendment_v005']['d7_recovery']
R1=json.load(open(f'{V5}/d7_recovery/KMAX_D7_RECOVERY_R1.json'))['brackets']['rule']
T=d7['fs_template_bracket']; T_lo,T_hi=T
W1=d7['W1_widening_rule']
runs={'C3R':'KMAX_A2F10_C3R_D7R1_V005_RUN_V001','S3':'KMAX_A2F10_S3_D7R1_V005_RUN_V001','Y3':'KMAX_A2F10_Y3_D7R1_V005_RUN_V001'}
ev=[]; 
for case,name in runs.items():
    base=f'{C2}/runs/{name}/stages'
    for ff in sorted(glob.glob(base+'/*fs_columns*/columns/column_*_failure.json')):
        f=json.load(open(ff)); idx=f['index']; itp=ff.replace('_failure.json','_iterations.jsonl')
        its=[json.loads(l) for l in open(itp) if l.strip()]
        Hs=[x['Hc_m2_s2'] for x in its]; rs=[x['mass_relative_residual'] for x in its]
        ev.append({'case':case,'index':idx,'stage':ff.split('/stages/')[1].split('/')[0],'type':f['type'],'message':f['message'],
                   'failure_file':{'path':ff,'sha256':sha(ff)},'iterations_file':{'path':itp,'sha256':sha(itp)},
                   'evaluations':[{'Hc_m2_s2':h,'mass_relative_residual':r} for h,r in zip(Hs,rs)]})
# bracket used per column: R1 override if present else template
def used(idx):
    o=R1['fs_absolute_overrides'].get(str(idx)); return (list(o) if o else list(T)), ('R1 override' if o else 'fs template (no override)')
rows={}; conflicts=[]; notes=[]
for e in ev:
    idx=e['index']; br,src=used(idx); lo,hi=br
    H=[x['Hc_m2_s2'] for x in e['evaluations']]; r=[x['mass_relative_residual'] for x in e['evaluations']]
    e['bracket_used_by_rule']=br; e['bracket_source']=src
    e['evaluated_ends_match_bracket']= (len(H)==2 and H[0]==lo and H[1]==hi)
    if not e['evaluated_ends_match_bracket']: notes.append(f"{e['case']} col {idx}: evaluations {H} differ from expected bracket {br}")
    if e['type']!='ValueError' or 'MASS_ENTHALPY_NOT_BRACKETED' not in e['message']:
        e['w1']='OUTSIDE_W1 (not a MASS_ENTHALPY_NOT_BRACKETED miss)'; continue
    if all(x>0 for x in r): direction='root_below_lo'
    elif all(x<0 for x in r): direction='root_above_hi'
    else: direction='SIGN_CHANGE (should have bracketed?)'
    e['direction']=direction
    if direction=='root_below_lo':
        new=[T_lo if lo>T_lo else lo/2, hi]; step='A (to template lo)' if lo>T_lo else 'B (lo/2)'
    elif direction=='root_above_hi':
        new=[lo, 1.05*T_hi if hi<1.05*T_hi else 2*hi]; step='A (to 1.05*template hi)' if hi<1.05*T_hi else 'B (2*hi)'
    else: new=None; step=None
    e['w1_new']=new; e['w1_step']=step
    k=str(idx)
    if k in rows and rows[k]['new']!=new: conflicts.append({'index':idx,'a':rows[k],'b':{'case':e['case'],'new':new,'direction':direction}})
    rows.setdefault(k,{'new':new,'direction':direction,'step':step,'from':br,'cases':[]})['cases'].append(e['case'])
R2=json.loads(json.dumps(R1)); 
for k,v in rows.items():
    if v['new'] is not None: R2['fs_absolute_overrides'][k]=v['new']
out={'W1_text':W1,'fs_template':T,'one_point_oh_five_times_T_hi_float':1.05*T_hi,'equals_317625000.0':1.05*T_hi==317625000.0,
     'evidence':ev,'per_column':rows,'cross_case_conflicts':conflicts,'notes':notes,'expected_R2_rule':R2,
     'R1_entries_preserved_or_widened': all((lambda a,b: b[0]<=a[0] and a[1]<=b[1])(R1['fs_absolute_overrides'][k], R2['fs_absolute_overrides'][k]) for k in R1['fs_absolute_overrides']),
     'non_override_keys_unchanged': all(R1[k]==R2[k] for k in R1 if k!='fs_absolute_overrides')}
json.dump(out,open(sys.argv[1],'w'),indent=1)
print('failures:', [(e['case'],e['index'],e['stage'],e.get('direction'),e['bracket_source'],e['evaluated_ends_match_bracket'],[round(x['mass_relative_residual'],5) for x in e['evaluations']]) for e in ev])
print('per column expected:'); [print('  ',k,v) for k,v in sorted(rows.items(),key=lambda kv:int(kv[0]))]
print('conflicts:', conflicts); print('notes:', notes); print('1.05*T_hi =', repr(1.05*T_hi))
print('expected R2 fs overrides:', {k:R2['fs_absolute_overrides'][k] for k in sorted(R2['fs_absolute_overrides'],key=int)})
