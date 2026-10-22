import json, os, hashlib, glob, datetime
C2="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2"
V2='claude_artifacts/kmax_prereg_v002_c2'; V3='claude_artifacts/kmax_prereg_v003_c2'
def J(p): return json.load(open(p))
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def diff(x,y,path,out):
    if type(x)!=type(y): out.append((path,'TYPE',x,y)); return
    if isinstance(x,dict):
        for k in sorted(set(x)|set(y)):
            if k not in x: out.append((path+'/'+k,'ADDED',None,y[k]))
            elif k not in y: out.append((path+'/'+k,'REMOVED',x[k],None))
            else: diff(x[k],y[k],path+'/'+k,out)
    elif isinstance(x,list):
        if len(x)!=len(y): out.append((path,'LEN',len(x),len(y)))
        for i,(p,q) in enumerate(zip(x,y)): diff(p,q,f'{path}[{i}]',out)
    elif x!=y: out.append((path,'CHANGED',x,y))
a=J(f'{V2}/KMAX_MATRIX_PREREG_V002.json'); b=J(f'{V3}/KMAX_MATRIX_PREREG_V003.json')
print('=== A. full text of changed criterion/status/anchor fields ===')
print('V002 deciding_test:', a['criterion']['bracket_precondition_P6']['deciding_test']); print('V003 deciding_test:', b['criterion']['bracket_precondition_P6']['deciding_test'])
print('V002 status:', a['status']); print('V003 status:', b['status'])
print('V003 change_log_v003:', b['change_log_v003'])
print('V002 anchor:', json.dumps(a['anchor'],indent=1)); print('V003 anchor:', json.dumps(b['anchor'],indent=1))
print('V003 supersedes:', json.dumps(b['supersedes'],indent=1))
print('cases[6] V002:', json.dumps(a['cases'][6],indent=1)[:1500]); print('cases[6] V003:', json.dumps(b['cases'][6],indent=1)[:1500])
print('V002 self sha', sha(f'{V2}/KMAX_MATRIX_PREREG_V002.json'))
print('=== B. seed scan candidates[2] and spec hashes ===')
r=J(f'{C2}/runs/A2_SEED_SCAN_G2_RUN_V001/result.json'); c=r['candidates']
for i,cc in enumerate(c): print(i, cc['factor'], cc['scale_s'], json.dumps(cc['candidate_seed'])[:300])
print('route_b_specs:', json.dumps(r['route_b_specs'],indent=1)[:2000])
print('selection:', r['selection'])
want={'fe1ad000a4ff35d84f16e7aceeb1e1d597d2b7885218f2c5d8e968ffce995560':'F3 anchor spec (V002)','a93c95b95c1f112b7293ffd598371335227cb93d7334981be33e368c6cd9f52b':'F10 anchor spec (V003)'}
for p in glob.glob(f'{C2}/**/*.json',recursive=True):
    h=sha(p)
    if h in want: print('FOUND',want[h],p)
print('=== D. compare script hash check logic ===')
src=open(f'{V3}/kmax_compare_c2v003.py').read().splitlines()
for i,l in enumerate(src,1):
    if 'PREREG_SHA256' in l or 'sha256' in l.lower() and ('prereg' in l.lower()): print(i,l)
print('=== E. seal timing ===')
def mt(p): return datetime.datetime.fromtimestamp(os.stat(p).st_mtime, datetime.timezone.utc).isoformat()
for p in [f'{V3}/SEAL_RECORD_V003.json',f'{V3}/KMAX_MATRIX_PREREG_V003.json',f'{V3}/kmax_compare_c2v003.py',f'{C2}/runs/A2_ANCHOR_F10_RUN_V001/start.json',f'{C2}/runs/A2_ANCHOR_F10_RUN_V001/progress.jsonl']:
    print(mt(p), p)
for p in sorted(glob.glob(f'{C2}/runs/A2_ANCHOR_F10_RUN_V001/stages/*')): print(mt(p), os.path.basename(p), 'dir' if os.path.isdir(p) else os.path.getsize(p))
for n in ('result.json','finish.json'): print(n,'exists', os.path.exists(f'{C2}/runs/A2_ANCHOR_F10_RUN_V001/{n}'))
print('--- progress.jsonl (all lines, utc + stage) ---')
for l in open(f'{C2}/runs/A2_ANCHOR_F10_RUN_V001/progress.jsonl'):
    try: d=json.loads(l); print({k:d[k] for k in d if k in ('utc','time','stage','event','status','elapsed_s','column','message')})
    except Exception as e: print('raw', l[:160])
