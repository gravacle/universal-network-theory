"""Claude3 BLIND derivation of D7 recovery R3 by the sealed W1 rule (prereg V005 amendment_v005.d7_recovery.W1_widening_rule),
starting from R2 (ff7cf806), from the failed D7R2 calls' column *_failure.json and *_iterations.jsonl files only.
Written before KMAX_D7_RECOVERY_R3.json exists. Opens no result.json / finish.json."""
import json, glob, hashlib, sys
C2="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2"
V5='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
R2P=f'{V5}/d7_recovery_r2/KMAX_D7_RECOVERY_R2.json'; assert sha(R2P)=='ff7cf806cc3e297201cc151d05ce46b1c43e911d3a9dda15f1a07734532e93fd', 'R2 pin'
pre=json.load(open(f'{V5}/KMAX_MATRIX_PREREG_V005.json')); d7=pre['amendment_v005']['d7_recovery']
R2=json.load(open(R2P))
R2rule=R2['brackets']['rule']; R2wid=R2.get('widened_entries',{})
T=d7['fs_template_bracket']; T_lo,T_hi=T; HULL_HI=1.05*T_hi
runs={'C4R2':'KMAX_A2F10_C4R2_D7R2_RUN_V001','S4R2':'KMAX_A2F10_S4R2_D7R2_RUN_V001','Y4R2':'KMAX_A2F10_Y4R2_D7R2_RUN_V001'}
ev=[]
for case,name in runs.items():
    base=f'{C2}/runs/{name}/stages'
    for ff in sorted(glob.glob(base+'/*fs_columns*/columns/column_*_failure.json')):
        f=json.load(open(ff)); itp=ff.replace('_failure.json','_iterations.jsonl')
        its=[json.loads(l) for l in open(itp) if l.strip()]
        ev.append({'case':case,'index':f['index'],'stage':ff.split('/stages/')[1].split('/')[0],'type':f['type'],'message':f['message'],
                   'failure_file':{'path':ff,'sha256':sha(ff)},'iterations_file':{'path':itp,'sha256':sha(itp)},
                   'evaluations':[{'Hc_m2_s2':x['Hc_m2_s2'],'mass_relative_residual':x['mass_relative_residual']} for x in its]})
def used(idx):
    o=R2rule['fs_absolute_overrides'].get(str(idx))
    return (list(o),'R2 override') if o else (list(T),'fs template (no override in R2)')
rows={}; conflicts=[]; notes=[]
for e in ev:
    idx=e['index']; br,src=used(idx); lo,hi=br
    H=[x['Hc_m2_s2'] for x in e['evaluations']]; r=[x['mass_relative_residual'] for x in e['evaluations']]
    e['bracket_used_by_rule']=br; e['bracket_source']=src
    e['evaluated_ends_match_bracket']=(len(H)==2 and H[0]==lo and H[1]==hi)
    if not e['evaluated_ends_match_bracket']: notes.append(f"{e['case']} col {idx}: evaluations at {H}, rule bracket {br}")
    if e['type']!='ValueError' or 'MASS_ENTHALPY_NOT_BRACKETED' not in e['message']:
        e['w1']='OUTSIDE_W1'; notes.append(f"{e['case']} col {idx}: {e['type']} {e['message']}"); continue
    if all(x>0 for x in r): d='root_below_lo'
    elif all(x<0 for x in r): d='root_above_hi'
    else: d='SIGN_CHANGE'
    e['direction']=d
    prior_r2=R2wid.get(str(idx))
    if d=='root_below_lo':
        new=[T_lo if lo>T_lo else lo/2, hi]; step='A' if lo>T_lo else 'B'
    elif d=='root_above_hi':
        new=[lo, HULL_HI if hi<HULL_HI else 2*hi]; step='A' if hi<HULL_HI else 'B'
    else: new=None; step=None
    e['w1_new']=new; e['w1_step']=step
    e['entry_previously_widened']= (prior_r2 is not None)
    k=str(idx)
    if k in rows and rows[k]['new']!=new:
        conflicts.append({'index':idx,'first':{'cases':rows[k]['cases'],'new':rows[k]['new'],'direction':rows[k]['direction']},'second':{'case':e['case'],'new':new,'direction':d}})
    rows.setdefault(k,{'new':new,'direction':d,'step':step,'from':br,'from_source':src,'previously_widened_by':(prior_r2 or {}).get('invocation'),'cases':[]})['cases'].append(e['case'])
R3=json.loads(json.dumps(R2rule))
for k,v in rows.items():
    if v['new'] is not None: R3['fs_absolute_overrides'][k]=v['new']
out={'R2_sha256':sha(R2P),'W1_text':d7['W1_widening_rule'],'fs_template':T,'hull_hi_float':HULL_HI,
     'evidence':ev,'per_column':rows,'cross_case_conflicts':conflicts,'notes':notes,
     'step_B_entries':[k for k,v in rows.items() if v['step']=='B'],
     'misses_on_entries_already_widened_in_R1_or_R2':[k for k,v in rows.items() if v['previously_widened_by']],
     'expected_R3_rule':R3}
json.dump(out,open(sys.argv[1],'w'),indent=1)
for e in ev: print(e['case'],e['index'],e['stage'],e.get('direction'),e['bracket_source'],e['evaluated_ends_match_bracket'],[(x['Hc_m2_s2'],round(x['mass_relative_residual'],5)) for x in e['evaluations']],e['message'][:60])
print('per column:'); [print('  ',k,v) for k,v in sorted(rows.items(),key=lambda kv:int(kv[0]))]
print('conflicts:',conflicts); print('notes:',notes); print('step B:',out['step_B_entries']); print('previously widened hit:',out['misses_on_entries_already_widened_in_R1_or_R2'])
print('expected R3 fs overrides:',{k:R3['fs_absolute_overrides'][k] for k in sorted(R3['fs_absolute_overrides'],key=int)})
