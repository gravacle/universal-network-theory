"""Claude3 distinct check of D7 recovery R2 (dispatch 0482). Read-only; opens no result.json/finish.json of any run
(run status is taken from receipts/listings only)."""
import json, hashlib, os, sys, glob, importlib.util, datetime
V5='claude_artifacts/kmax_prereg_v005_c2'; R2D=f'{V5}/d7_recovery_r2'
C2="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2"
def J(p): return json.load(open(p))
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def canon(o): return json.dumps(o,sort_keys=True,separators=(',',':'))
def mt(p): return datetime.datetime.fromtimestamp(os.stat(p).st_mtime, datetime.timezone.utc).isoformat(timespec='seconds')
def diff(x,y,path,out):
    if type(x)!=type(y): out.append([path,'TYPE']); return
    if isinstance(x,dict):
        for k in sorted(set(x)|set(y)):
            if k not in x: out.append([path+'/'+k,'ADDED'])
            elif k not in y: out.append([path+'/'+k,'REMOVED'])
            else: diff(x[k],y[k],path+'/'+k,out)
    elif isinstance(x,list):
        if len(x)!=len(y): out.append([path,'LEN']); return
        for i,(p,q) in enumerate(zip(x,y)): diff(p,q,f'{path}[{i}]',out)
    elif x!=y: out.append([path,'CHANGED'])
E={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}
pre=J(f'{V5}/KMAX_MATRIX_PREREG_V005.json'); R1=J(f'{V5}/d7_recovery/KMAX_D7_RECOVERY_R1.json'); R2=J(f'{R2D}/KMAX_D7_RECOVERY_R2.json')
B=J(sys.argv[2])  # blind expectation
E['hashes']={'prereg_V005':sha(f'{V5}/KMAX_MATRIX_PREREG_V005.json'),'compare_v005':sha(f'{V5}/kmax_compare_c2v005.py'),'R1':sha(f'{V5}/d7_recovery/KMAX_D7_RECOVERY_R1.json'),'R2':sha(f'{R2D}/KMAX_D7_RECOVERY_R2.json'),'evidence_R2':sha(f'{R2D}/D7_EVIDENCE_C3R_S3_Y3_V001.json'),'make_d7r2':sha(f'{R2D}/make_d7r2_c2.py')}
E['R2_mtime_utc']=mt(f'{R2D}/KMAX_D7_RECOVERY_R2.json'); E['blind_derivation']=open(os.path.join(os.path.dirname(sys.argv[2]),'BLIND_TIMESTAMP.txt')).read()
E['R2_rule_equals_blind_W1']= canon(R2['brackets']['rule'])==canon(B['expected_R2_rule'])
# sealed validator, executed
spec=importlib.util.spec_from_file_location('cmp',f'{V5}/kmax_compare_c2v005.py'); cmp=importlib.util.module_from_spec(spec); spec.loader.exec_module(cmp)
E['sealed_validate_recovery_reasons']=cmp.validate_recovery(pre,R2['brackets'])
E['sealed_validate_recovery_R1_still_valid']=cmp.validate_recovery(pre,R1['brackets'])
# evidence pins and values
ev=J(f'{R2D}/D7_EVIDENCE_C3R_S3_Y3_V001.json'); pins=[]
def walk(o):
    if isinstance(o,dict):
        if set(o)>={'path','sha256'} and isinstance(o.get('path'),str) and os.path.isfile(o['path']): pins.append(o)
        for v in o.values(): walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(ev); walk(R2.get('evidence'))
bad=[p['path'] for p in pins if sha(p['path'])!=p['sha256']]
E['evidence_pins']={'n':len(pins),'mismatch':bad,'kinds':sorted(set(os.path.basename(p['path']).split('_')[-1] for p in pins))}
E['evidence_reads_result_json']=[p['path'] for p in pins if p['path'].endswith('result.json')]
# blind evidence vs R2 evidence values (residuals)
mine={(e['case'],e['index']):[x['mass_relative_residual'] for x in e['evaluations']] for e in B['evidence']}
theirs={}
def collect(o,case=None):
    if isinstance(o,dict):
        if 'index' in o and 'evidence' in o and isinstance(o['evidence'],list) and case:
            theirs[(case,o['index'])]=[x.get('mass_relative_residual') for x in o['evidence']]
        for k,v in o.items(): collect(v, k if k in ('C3R','S3','Y3') else case)
    elif isinstance(o,list):
        for v in o: collect(v,case)
collect(ev); collect(R2.get('evidence'))
E['evidence_values']={'mine_n':len(mine),'theirs_n':len(theirs),'equal':{f'{k[0]}:{k[1]}':(mine.get(k)==theirs.get(k)) for k in sorted(set(mine)|set(theirs))}}
# specs vs R1 counterparts
rec=J(f'{R2D}/BUILD_R2_RECORD.json'); sp={}
for cid,s in rec['specs'].items():
    x=J(s['path']); sp[cid]={'sha_match':sha(s['path'])==s['sha256'],'kind':s.get('kind'),'driver':s.get('driver'),'cube_outdir':os.path.basename(s.get('cube_outdir') or '')}
    br=(x.get('numerics') or {}).get('brackets'); sp[cid]['brackets_equal_R2']= canon(br)==canon(R2['brackets'])
    r1c=s.get('r1_counterpart')
    if r1c and os.path.isfile(r1c['path']):
        o=[]; diff(J(r1c['path']),x,'',o); sp[cid]['r1_counterpart']=os.path.basename(r1c['path']); sp[cid]['r1_sha_match']=sha(r1c['path'])==r1c['sha256']
        sp[cid]['changed_paths_vs_R1']=sorted(set(p[0].split('[')[0] if '/numerics/brackets' in p[0] else p[0] for p in o))
E['specs']=sp
E['registered_cases_covered']=sorted(rec['specs'])
# R2 runs state (listing only)
E['r2_runs']=sorted(os.path.basename(p) for p in glob.glob(f'{C2}/runs/*D7R2*')+glob.glob(f'{C2}/runs_ext/*D7R2*'))
# HASHES.txt
ok=0; badh=[]
for line in open(f'{R2D}/HASHES.txt'):
    parts=line.split()
    if len(parts)>=2 and len(parts[0])==64:
        p=parts[-1] if os.path.isabs(parts[-1]) else os.path.join(R2D,parts[-1])
        if os.path.isfile(p) and sha(p)==parts[0]: ok+=1
        else: badh.append(parts[-1])
E['hashes_txt']={'ok':ok,'bad':badh}
json.dump(E,open(sys.argv[1],'w'),indent=1,default=str)
print(json.dumps({k:v for k,v in E.items() if k not in ('specs','evidence_values')},indent=1,default=str)[:4000])
print('evidence values equal:', all(E['evidence_values']['equal'].values()), E['evidence_values']['mine_n'], E['evidence_values']['theirs_n'])
for k,v in sp.items(): print(' ',k,v)
