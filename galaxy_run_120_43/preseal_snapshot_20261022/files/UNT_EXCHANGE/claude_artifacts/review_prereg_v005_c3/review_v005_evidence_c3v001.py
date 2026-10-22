"""Claude3 confirmation evidence for dispatch 0479 (prereg V005). Read-only; no result.json of any V005/D7R1 run is opened."""
import json, os, hashlib, datetime, sys
C2="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2"
V5='claude_artifacts/kmax_prereg_v005_c2'; V4='claude_artifacts/kmax_prereg_v004_c2'
def J(p): return json.load(open(p))
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def canon(o): return json.dumps(o,sort_keys=True,separators=(',',':'))
def diff(x,y,path,out):
    if type(x)!=type(y): out.append([path,'TYPE']); return
    if isinstance(x,dict):
        for k in sorted(set(x)|set(y)):
            if k not in x: out.append([path+'/'+k,'ADDED'])
            elif k not in y: out.append([path+'/'+k,'REMOVED'])
            else: diff(x[k],y[k],path+'/'+k,out)
    elif isinstance(x,list):
        if len(x)!=len(y): out.append([path,'LEN'])
        for i,(p,q) in enumerate(zip(x,y)): diff(p,q,f'{path}[{i}]',out)
    elif x!=y: out.append([path,'CHANGED'])
b=J(f'{V5}/KMAX_MATRIX_PREREG_V005.json'); a=J(f'{V4}/KMAX_MATRIX_PREREG_V004.json'); am=b['amendment_v005']; d7=am['d7_recovery']
E={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),'hashes':{p:sha(p) for p in (f'{V5}/KMAX_MATRIX_PREREG_V005.json',f'{V5}/kmax_compare_c2v005.py',f'{V5}/SEAL_RECORD_V005.json',f'{V5}/d7_recovery/KMAX_D7_RECOVERY_R1.json',f'{V5}/check/CHECK_V001.md')}}
out=[]; diff(a,b,'',out); E['v004_to_v005_diff_paths']=out
# unchanged claim: criterion etc byte-identical (canonical)
E['unchanged_canonical']={k: canon(a[k])==canon(b[k]) for k in ('anchor','row_ids','quoted_sigma_km_s','tau_km_s','grids','admission_constraint','fixed_across_all_cases','criterion')}
E['cases_changed_only_drivers_allowed']=all(canon({k:v for k,v in ca.items() if k!='drivers_allowed'})==canon({k:v for k,v in cb.items() if k!='drivers_allowed'}) for ca,cb in zip(a['cases'],b['cases']))
# F1
dt=b['binding_inputs']['v005_deciding_test']; L=J(f'{C2}/runs/DDO154_ROUTE_B_C2V005_DECIDING_ADMIT_PREFIX_RUN_V001.receipt.json.launch.json')
E['F1']={'v005_in_drivers': b['binding_inputs']['drivers']['v005']['sha256']=='2aef51c4a4cf0ee192594ab366e9b37e54881977df2e4d1b2f259a759818a42f','drivers_allowed':{c['id']:c['drivers_allowed'] for c in b['cases']},
 'deciding_required':dt['required'],'deciding_launch_pins':{'driver':L['pins']['driver']['sha256'],'spec':L['pins']['spec']['sha256'],'utc':L['utc']},
 'required_driver_matches_launch': dt['required']['driver_sha256']==L['pins']['driver']['sha256'],'required_spec_matches_launch': dt['required']['call_spec_sha256']==L['pins']['spec']['sha256'],
 'deciding_result_exists': os.path.exists(dt['result_path']), 'deciding_finish_exists': os.path.exists(dt['finish_path'])}
# F5
ic=b['binding_inputs']['v005_independent_check']; E['F5']={'pinned_sha':ic['sha256'],'actual_sha':sha(ic['path']),'match':ic['sha256']==sha(ic['path']),'verdict':ic['verdict']}
# F3
sr=am['stopped_runs']; E['F3']={'record_sha_match': sha(sr['record']['path'])==sr['record']['sha256'],'summary_keys':list(sr['summary'])}
# D7 R1: widened entries vs evidence from the actual failure files
r1=J(f'{V5}/d7_recovery/KMAX_D7_RECOVERY_R1.json'); ev=[]
for case,items in r1['evidence'].items():
    for it in items:
        ff=it['failure_file']; itf=it.get('iterations_file')
        rec={'case':case,'index':it['index'],'failure_file_sha_match': sha(ff['path'])==ff['sha256']}
        if itf: rec['iterations_file_sha_match']= sha(itf['path'])==itf['sha256']
        # independent residual signs from the iterations file
        signs=[]
        if itf and os.path.exists(itf['path']):
            for l in open(itf['path']):
                try: d=json.loads(l)
                except Exception: continue
                h=d.get('Hc_m2_s2') or d.get('Hc') ; r=d.get('mass_relative_residual')
                if h is not None and r is not None: signs.append((h, r))
        rec['iterations_H_residual_pairs']=signs[:6]; rec['both_ends_positive']= all(r>0 for h,r in signs if abs(h-3.025e8)<1 or abs(h-3.17625e8)<1) and any(abs(h-3.025e8)<1 for h,r in signs) and any(abs(h-3.17625e8)<1 for h,r in signs)
        rec['r1_evidence']=it['evidence']; ev.append(rec)
E['D7_R1_evidence']=ev
anc=b['anchor']['brackets']['rule']; rr=r1['brackets']['rule']
changed={k:(anc['fs_absolute_overrides'][k],rr['fs_absolute_overrides'][k]) for k in anc['fs_absolute_overrides'] if anc['fs_absolute_overrides'][k]!=rr['fs_absolute_overrides'][k]}
E['R1_vs_anchor']={'fs_entries_changed':changed,'only_lo_moved_to_template_lo': all(v[1]==[151250000.0, v[0][1]] for v in changed.values()),'other_keys_identical': all(canon(anc[k])==canon(rr[k]) for k in anc if k!='fs_absolute_overrides'),'changed_set_equals_evidenced_columns': sorted(changed)==sorted({str(it['index']) for items in r1['evidence'].values() for it in items})}
# specs: S2R/Y2R/C2R vs derived_from
sp={}
for cid,c in d7['calls'].items():
    o=[]; diff(J(c['derived_from']['path']),J(c['path']),'',o); x=J(c['path'])
    sp[cid]={'spec_sha_match':sha(c['path'])==c['sha256'],'derived_from_sha_match':sha(c['derived_from']['path'])==c['derived_from']['sha256'],'derived_from':os.path.basename(c['derived_from']['path']),'changed_paths':[t[0] for t in o],'brackets_equal_R1': canon(x.get('brackets'))==canon(r1['brackets']),'driver':c['driver']}
E['d7r1_specs']=sp
# seal timing
seal=J(f'{V5}/SEAL_RECORD_V005.json'); E['seal']={'utc':seal['utc'],'statement':seal['statement']}
runs={}
for n in ('KMAX_A2F10_S2R_D7R1_RUN_V001','KMAX_A2F10_Y2R_D7R1_RUN_V001','KMAX_A2F10_C2R_D7R1_RUN_V001','KMAX_A2F10_C3_V005_RUN_V001','KMAX_A2F10_C4_V005_RUN_V001','KMAX_A2F10_R_V005_RUN_V001','DDO154_ROUTE_B_C2V005_DECIDING_ADMIT_PREFIX_RUN_V001'):
    d=f'{C2}/runs/{n}'; Lp=d+'.receipt.json.launch.json'
    runs[n]={'launch_utc':J(Lp)['utc'] if os.path.exists(Lp) else None,'result_exists':os.path.exists(d+'/result.json'),'finish_exists':os.path.exists(d+'/finish.json'),'launch_after_seal': (J(Lp)['utc']>seal['utc'][:19]) if os.path.exists(Lp) else None}
E['runs']=runs
E['W1_rule']=d7['W1_widening_rule']; E['step4_text']=d7['step4_every_case']; E['later_invocations']=d7['later_invocations']
json.dump(E,open(sys.argv[1],'w'),indent=1)
print('unchanged', E['unchanged_canonical'], 'cases only drivers_allowed', E['cases_changed_only_drivers_allowed'])
print('F1', {k:v for k,v in E['F1'].items() if k not in ('drivers_allowed','deciding_required','deciding_launch_pins')})
print('F5', E['F5']['match'], '| F3', E['F3'])
print('R1 vs anchor', E['R1_vs_anchor'])
for r in ev: print(' ', r['case'], r['index'], 'ff', r['failure_file_sha_match'], 'it', r.get('iterations_file_sha_match'), 'both_pos', r['both_ends_positive'], r['iterations_H_residual_pairs'][:2])
for k,v in sp.items(): print(' ', k, v)
print('runs', {k:(v['launch_utc'],v['result_exists'],v['launch_after_seal']) for k,v in runs.items()})
