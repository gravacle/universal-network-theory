import json, os, hashlib, glob, datetime
C2="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2"
V2='claude_artifacts/kmax_prereg_v002_c2'; V3='claude_artifacts/kmax_prereg_v003_c2'
def J(p): return json.load(open(p))
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def mt(p): return datetime.datetime.fromtimestamp(os.stat(p).st_mtime, datetime.timezone.utc).isoformat()
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
def show(out):
    for p,k,x,y in out:
        sx=json.dumps(x)[:110] if x is not None else None; sy=json.dumps(y)[:110] if y is not None else None
        print(f'   {k:8s} {p}: {sx} -> {sy}')
print('=== 1. spec diffs V002 (F3) -> V003 (F10) ===')
pairs=[]
for c in ('C3','C4','R'): pairs.append((f'{V2}/specs_anchor/v002/wave1/CALL_KMAX_{c}_A2F3_C2V002.json', f'{V3}/specs_anchor_f10/wave1/CALL_KMAX_{c}_A2F10_C2V003.json'))
for c in ('S2','S3','S4','Y2','Y3','Y4'): pairs.append((f'{V2}/specs_anchor/v002/templates/CALL_KMAX_{c}_A2F3_C2V002.TEMPLATE.json', f'{V3}/specs_anchor_f10/templates/CALL_KMAX_{c}_A2F10_C2V003.TEMPLATE.json'))
for c in ('S2','Y2'): pairs.append((f'{C2}/specs/CALL_KMAX_{c}_A2F3_FILLED_C2V002.json', f'{V3}/specs_anchor_f10/filled/CALL_KMAX_{c}_A2F10_FILLED_C2V003.json'))
summary={}
for a,b in pairs:
    out=[]; diff(J(a),J(b),'',out)
    print(f'-- {os.path.basename(a)} -> {os.path.basename(b)}: {len(out)} diffs')
    show(out)
print('=== 2. anchor spec F10 vs seed-scan NEXT (F3) spec ===')
out=[]; diff(J(f'{C2}/runs/A2_SEED_SCAN_G2_RUN_V001/route_b_specs/CALL_A2_SEEDSCAN_NEXT_C2V001.json'), J(f'{C2}/specs/CALL_A2_ANCHOR_F10_C2V001.json'),'',out); print(len(out),'diffs'); show(out)
print('F10 spec sha', sha(f'{C2}/specs/CALL_A2_ANCHOR_F10_C2V001.json'), 'inputs/call_spec sha', sha(f'{C2}/runs/A2_ANCHOR_F10_RUN_V001/inputs/call_spec.json'))
print('=== 3. F10 launch.json / F3 timing ===')
L=J(f'{C2}/runs/A2_ANCHOR_F10_RUN_V001.receipt.json.launch.json'); print('F10 launch keys', list(L)[:20]); print('F10 launch pins', json.dumps(L.get('pins'))[:600]); print('F10 launch utc', {k:L[k] for k in L if 'utc' in k.lower() or 'time' in k.lower()})
print('F10 start.json mtime', mt(f'{C2}/runs/A2_ANCHOR_F10_RUN_V001/start.json'), '| F3 start.json mtime', mt(f'{C2}/runs/A2_ANCHOR_F3_RUN_V001/start.json'))
L3=J(f'{C2}/runs/A2_ANCHOR_F3_RUN_V001.receipt.json.launch.json'); print('F3 launch utc', {k:L3[k] for k in L3 if 'utc' in k.lower() or 'time' in k.lower()}); print('F3 launch pins.spec', json.dumps(L3.get('pins',{}).get('spec'))[:200])
print('V002 SEAL_RECORD mtime', mt(f'{V2}/SEAL_RECORD.json'), json.dumps(J(f'{V2}/SEAL_RECORD.json'))[:700])
print('=== 4. F10 progress.jsonl raw ===')
for l in open(f'{C2}/runs/A2_ANCHOR_F10_RUN_V001/progress.jsonl'): print('  ', l.strip()[:200])
print('F3 finish.json:', json.dumps(J(f'{C2}/runs/A2_ANCHOR_F3_RUN_V001/finish.json'))[:400])
print('=== 5. filled S2/Y2 admission blocks and F10 stage outputs ===')
for c in ('S2','Y2'):
    d=J(f'{V3}/specs_anchor_f10/filled/CALL_KMAX_{c}_A2F10_FILLED_C2V003.json'); print(c,'top keys',list(d)[:30])
    for k in d:
        if 'admi' in k.lower() or 'bind' in k.lower() or 'prefix' in k.lower(): print('  ',k, json.dumps(d[k])[:900])
for st in ('01_route_a','02_reference','03_body'):
    p=f'{C2}/runs/A2_ANCHOR_F10_RUN_V001/stages/{st}'; print(st, sorted(os.listdir(p))[:15])
