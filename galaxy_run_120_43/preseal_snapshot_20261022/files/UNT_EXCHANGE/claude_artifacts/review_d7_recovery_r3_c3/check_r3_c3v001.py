"""Claude3 check of D7 recovery R3 (dispatch 0483) against the blind W1 derivation. Read-only; opens no result.json."""
import json, hashlib, os, sys, glob, importlib.util, datetime
V5='claude_artifacts/kmax_prereg_v005_c2'; R3D=f'{V5}/d7_recovery_r3'; R2D=f'{V5}/d7_recovery_r2'
C2="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2"
def J(p): return json.load(open(p))
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def canon(o): return json.dumps(o,sort_keys=True,separators=(',',':'))
def mt(p): return datetime.datetime.fromtimestamp(os.stat(p).st_mtime, datetime.timezone.utc).isoformat(timespec='seconds')
def diff(x,y,path,out):
    if type(x)!=type(y): out.append(path); return
    if isinstance(x,dict):
        for k in sorted(set(x)|set(y)):
            if k not in x or k not in y: out.append(path+'/'+k)
            else: diff(x[k],y[k],path+'/'+k,out)
    elif isinstance(x,list):
        if len(x)!=len(y): out.append(path); return
        for i,(p,q) in enumerate(zip(x,y)): diff(p,q,f'{path}[{i}]',out)
    elif x!=y: out.append(path)
B=J(sys.argv[2]); pre=J(f'{V5}/KMAX_MATRIX_PREREG_V005.json'); R2=J(f'{R2D}/KMAX_D7_RECOVERY_R2.json'); R3=J(f'{R3D}/KMAX_D7_RECOVERY_R3.json')
E={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),'R3_sha256':sha(f'{R3D}/KMAX_D7_RECOVERY_R3.json'),'R3_mtime_utc':mt(f'{R3D}/KMAX_D7_RECOVERY_R3.json'),
   'R2_sha256':sha(f'{R2D}/KMAX_D7_RECOVERY_R2.json'),'blind_timestamp':open(os.path.join(os.path.dirname(sys.argv[2]),'BLIND_TIMESTAMP_R3.txt')).read()}
E['R3_keys']=list(R3); E['R3_invocation']=R3.get('invocation'); E['R3_reason']=R3.get('reason')
E['R3_rule_equals_blind']= canon(R3['brackets']['rule'])==canon(B['expected_R3_rule'])
if not E['R3_rule_equals_blind']:
    o=[]; diff(B['expected_R3_rule'],R3['brackets']['rule'],'',o); E['rule_diff_paths']=o
spec=importlib.util.spec_from_file_location('cmp',f'{V5}/kmax_compare_c2v005.py'); cmp=importlib.util.module_from_spec(spec); spec.loader.exec_module(cmp)
E['sealed_validate_recovery_R3']=cmp.validate_recovery(pre,R3['brackets'])
E['R3_contains_R2_every_entry']= all((lambda a,b: b[0]<=a[0] and a[1]<=b[1])(R2['brackets']['rule']['fs_absolute_overrides'][k], R3['brackets']['rule']['fs_absolute_overrides'][k]) for k in R2['brackets']['rule']['fs_absolute_overrides'])
E['R3_vs_R2_changed_fs']=sorted([k for k in R3['brackets']['rule']['fs_absolute_overrides'] if R2['brackets']['rule']['fs_absolute_overrides'].get(k)!=R3['brackets']['rule']['fs_absolute_overrides'][k]],key=int)
E['R3_other_keys_equal_R2']= all(canon(R2['brackets']['rule'][k])==canon(R3['brackets']['rule'][k]) for k in R2['brackets']['rule'] if k!='fs_absolute_overrides')
E['R3_widened_entries_R3']= {k:v for k,v in (R3.get('widened_entries') or {}).items() if v.get('invocation')=='R3'}
# evidence pins
pins=[]
def walk(o):
    if isinstance(o,dict):
        if 'path' in o and 'sha256' in o and isinstance(o['path'],str) and os.path.isfile(o['path']): pins.append(o)
        for v in o.values(): walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(J(f'{R3D}/D7_EVIDENCE_C4R2_S4R2_Y4R2_V001.json')); walk(R3.get('evidence'))
E['evidence_pins']={'n':len(pins),'mismatch':[p['path'] for p in pins if sha(p['path'])!=p['sha256']],'result_json_pinned':[p['path'] for p in pins if p['path'].endswith('result.json')]}
mine={f"{e['case']}:{e['index']}":[x['mass_relative_residual'] for x in e['evaluations']] for e in B['evidence']}
theirs={}
def collect(o,case=None):
    if isinstance(o,dict):
        if 'index' in o and isinstance(o.get('evidence'),list) and case: theirs[f"{case}:{o['index']}"]=[x.get('mass_relative_residual') for x in o['evidence']]
        for k,v in o.items(): collect(v, k if k in ('C4R2','S4R2','Y4R2') else case)
    elif isinstance(o,list):
        for v in o: collect(v,case)
collect(J(f'{R3D}/D7_EVIDENCE_C4R2_S4R2_Y4R2_V001.json')); collect(R3.get('evidence'))
E['evidence_values']={'mine':len(mine),'theirs':len(theirs),'all_equal':all(mine.get(k)==theirs.get(k) for k in set(mine)|set(theirs)),'unequal':[k for k in set(mine)|set(theirs) if mine.get(k)!=theirs.get(k)]}
# builder reads
src=open(f'{R3D}/make_d7r3_c2.py').read().splitlines()
E['builder_result_json_mentions']=[(i,l.strip()[:140]) for i,l in enumerate(src,1) if 'result.json' in l]
# specs (step 4)
rec=J(f'{R3D}/BUILD_R3_RECORD.json'); sp={}
for cid,s in (rec.get('specs') or {}).items():
    x=J(s['path']); d={'sha_match':sha(s['path'])==s['sha256'],'driver':s.get('driver'),'kind':s.get('kind'),'cube':os.path.basename(s.get('cube_outdir') or ''),
       'brackets_equal_R3': canon((x.get('numerics') or {}).get('brackets'))==canon(R3['brackets'])}
    c=s.get('r2_counterpart') or s.get('r1_counterpart')
    if c and os.path.isfile(c['path']):
        o=[]; diff(J(c['path']),x,'',o); d['counterpart']=os.path.basename(c['path']); d['counterpart_sha_match']=sha(c['path'])==c['sha256']
        d['changed_vs_counterpart']=sorted(set(p if '/numerics/brackets' not in p else p.split('[')[0] for p in o))
    sp[cid]=d
E['specs']=sp; E['cases']=sorted(sp)
E['stopped_r2_runs']=J(f'{R3D}/STOPPED_R2_RUNS_V001.json')
E['r3_runs']=sorted(os.path.basename(p) for p in glob.glob(f'{C2}/runs/*D7R3*')+glob.glob(f'{C2}/runs_ext/*D7R3*'))
ok=0; bad=[]
for line in open(f'{R3D}/HASHES.txt'):
    p=line.split()
    if len(p)>=2 and len(p[0])==64:
        f=p[-1] if os.path.isabs(p[-1]) else os.path.join(R3D,p[-1])
        if os.path.isfile(f) and sha(f)==p[0]: ok+=1
        else: bad.append(p[-1])
E['hashes_txt']={'ok':ok,'bad':bad}
json.dump(E,open(sys.argv[1],'w'),indent=1,default=str)
print(json.dumps({k:v for k,v in E.items() if k not in ('specs','stopped_r2_runs','R3_widened_entries_R3')},indent=1,default=str)[:3500])
print('R3 widened (R3):', {k:(v.get('from_R2') or v.get('from'), v.get('to'), v.get('W1_step'), v.get('evidenced_by')) for k,v in E['R3_widened_entries_R3'].items()})
for k,v in sp.items(): print(' ',k,v)
print('stopped R2 runs:', json.dumps(E['stopped_r2_runs'])[:900])
