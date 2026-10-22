"""Machine-generated evidence for the Claude3 review of KMAX pre-registration V003 (dispatch 0474). Read-only."""
import json, os, hashlib, glob, datetime, sys
C2="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2"
V2='claude_artifacts/kmax_prereg_v002_c2'; V3='claude_artifacts/kmax_prereg_v003_c2'
def J(p): return json.load(open(p))
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def canon(o): return json.dumps(o,sort_keys=True,separators=(',',':')).encode()
def mt(p): return datetime.datetime.fromtimestamp(os.stat(p).st_mtime, datetime.timezone.utc).isoformat()
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
E={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':{}}
for p in [f'{V3}/KMAX_MATRIX_PREREG_V003.json',f'{V3}/kmax_compare_c2v003.py',f'{V3}/SEAL_RECORD_V003.json',f'{V2}/KMAX_MATRIX_PREREG_V002.json',f'{V2}/kmax_compare_c2v002.py',f'{V2}/SEAL_RECORD.json',f'{C2}/specs/CALL_A2_ANCHOR_F10_C2V001.json',f'{C2}/runs/A2_SEED_SCAN_G2_RUN_V001/route_b_specs/CALL_A2_SEEDSCAN_NEXT_C2V001.json',f'{C2}/runs/A2_SEED_SCAN_G2_RUN_V001/result.json',f'{C2}/runs/A2_ANCHOR_F10_RUN_V001.receipt.json.launch.json',f'{C2}/runs/A2_ANCHOR_F3_RUN_V001/finish.json']:
    E['inputs'][p]={'sha256':sha(p),'mtime_utc':mt(p)}
a=J(f'{V2}/KMAX_MATRIX_PREREG_V002.json'); b=J(f'{V3}/KMAX_MATRIX_PREREG_V003.json')
out=[]; diff(a,b,'',out); E['prereg_v002_to_v003_diff_paths']=out
E['prereg_v003_supersedes_sha_matches_v002_bytes']= b['supersedes']['sha256']==sha(f'{V2}/KMAX_MATRIX_PREREG_V002.json')
E['prereg_v003_stale_fe1ad000_mentions']=[k for k,v in (('anchor.source',b['anchor']['source']),('cases[6].bound_call.verified',b['cases'][6]['bound_call']['verified'])) if 'fe1ad000' in v]
r=J(f'{C2}/runs/A2_SEED_SCAN_G2_RUN_V001/result.json'); c2=r['candidates'][2]
E['anchor_f10_values']={'prereg_gamma':b['anchor']['physical']['gamma'],'seed_scan_candidates2_gamma_eval':c2['candidate_seed']['gamma_eval'],'prereg_common_scale_s':b['anchor']['physical']['common_scale_s'],'seed_scan_candidates2_scale_s':c2['scale_s'],'factor':c2['factor'],'bitwise_equal': b['anchor']['physical']['gamma']==c2['candidate_seed']['gamma_eval'] and b['anchor']['physical']['common_scale_s']==c2['scale_s']}
pairs=[]
for c in ('C3','C4','R'): pairs.append((f'{V2}/specs_anchor/v002/wave1/CALL_KMAX_{c}_A2F3_C2V002.json', f'{V3}/specs_anchor_f10/wave1/CALL_KMAX_{c}_A2F10_C2V003.json'))
for c in ('S2','S3','S4','Y2','Y3','Y4'): pairs.append((f'{V2}/specs_anchor/v002/templates/CALL_KMAX_{c}_A2F3_C2V002.TEMPLATE.json', f'{V3}/specs_anchor_f10/templates/CALL_KMAX_{c}_A2F10_C2V003.TEMPLATE.json'))
for c in ('S2','Y2'): pairs.append((f'{C2}/specs/CALL_KMAX_{c}_A2F3_FILLED_C2V002.json', f'{V3}/specs_anchor_f10/filled/CALL_KMAX_{c}_A2F10_FILLED_C2V003.json'))
E['spec_diffs']={}
for p,q in pairs:
    o=[]; diff(J(p),J(q),'',o); x=J(q)
    E['spec_diffs'][os.path.basename(q)]={'v002_sha256':sha(p),'v003_sha256':sha(q),'changed_paths':[t[0] for t in o],'physical_gamma':x['physical']['gamma'],'physical_common_scale_s':x['physical']['common_scale_s']}
o=[]; diff(J(f'{C2}/runs/A2_SEED_SCAN_G2_RUN_V001/route_b_specs/CALL_A2_SEEDSCAN_NEXT_C2V001.json'),J(f'{C2}/specs/CALL_A2_ANCHOR_F10_C2V001.json'),'',o)
L=J(f'{C2}/runs/A2_ANCHOR_F10_RUN_V001.receipt.json.launch.json')
E['anchor_spec']={'f3_next_to_f10_changed_paths':[t[0] for t in o],'f10_spec_sha256':sha(f'{C2}/specs/CALL_A2_ANCHOR_F10_C2V001.json'),'f10_inputs_call_spec_sha256':sha(f'{C2}/runs/A2_ANCHOR_F10_RUN_V001/inputs/call_spec.json'),'f10_launch_pins_spec_sha256':L['pins']['spec']['sha256'],'f10_launch_utc':L['utc'],'f3_launch_utc':J(f'{C2}/runs/A2_ANCHOR_F3_RUN_V001.receipt.json.launch.json')['utc'],'retries_allowed':L.get('retries_allowed'),'caps':L.get('caps')}
adm=J(f'{V3}/specs_anchor_f10/filled/CALL_KMAX_S2_A2F10_FILLED_C2V003.json')['admit']
RA=f'{C2}/runs/A2_ANCHOR_F10_RUN_V001/stages'
ident=J(f'{RA}/01_route_a/checkpoint/IDENTITY.json')
E['admission']={'y2_admit_equals_s2_admit': adm==J(f'{V3}/specs_anchor_f10/filled/CALL_KMAX_Y2_A2F10_FILLED_C2V003.json')['admit'],
 'route_a_result_sha256_matches': adm['route_a']['result_sha256']==sha(f'{RA}/01_route_a/attempt_000/result.json'),
 'route_a_identity_sha256_matches_canonical_IDENTITY_json_identity': adm['route_a']['identity_sha256']==hashlib.sha256(canon(ident['identity'])).hexdigest(),
 'reference_start_sha256_matches': adm['reference']['start_sha256']==sha(f'{RA}/02_reference/reference/start.json'),
 'reference_finish_sha256_matches': adm['reference']['finish_sha256']==sha(f'{RA}/02_reference/reference/finish.json'),
 'body_finish_sha256_matches': adm['body']['finish_sha256']==sha(f'{RA}/03_body/body/finish.json'),
 'directories_exist': {k:os.path.isdir(v) for sec in adm.values() for k,v in sec.items() if 'directory' in k}}
t0=datetime.datetime(2026,10,17,14,35,58,tzinfo=datetime.timezone.utc)
stages=[]
for l in open(f'{C2}/runs/A2_ANCHOR_F10_RUN_V001/progress.jsonl'):
    d=json.loads(l)
    if 'stage' not in d or 'elapsed_seconds' not in d: stages.append({'raw':l.strip()[:200]}); continue
    stages.append({'stage':d['stage'],'event':d['event'],'utc':(t0+datetime.timedelta(seconds=d['elapsed_seconds'])).isoformat(timespec='seconds')})
seal=J(f'{V3}/SEAL_RECORD_V003.json')['utc']
E['seal_timing']={'seal_utc':seal,'v003_files_mtime_utc':{os.path.basename(p):mt(p) for p in (f'{V3}/KMAX_MATRIX_PREREG_V003.json',f'{V3}/kmax_compare_c2v003.py',f'{V3}/SEAL_RECORD_V003.json')},'f10_result_json_exists':os.path.exists(f'{C2}/runs/A2_ANCHOR_F10_RUN_V001/result.json'),'f10_finish_json_exists':os.path.exists(f'{C2}/runs/A2_ANCHOR_F10_RUN_V001/finish.json'),'f10_stage_timeline_from_launch_plus_elapsed':stages,'f3_failed_utc':(t0+datetime.timedelta(seconds=J(f'{C2}/runs/A2_ANCHOR_F3_RUN_V001/finish.json')['elapsed_seconds'])).isoformat(timespec='seconds'),'v002_seal_utc':J(f'{V2}/SEAL_RECORD.json')['utc'],'stages_finished_before_v003_seal':[s['stage'] for s in stages if s.get('event')=='finished' and s['utc']<seal]}
src=open(f'{V3}/kmax_compare_c2v003.py').read().splitlines()
E['compare_script']={'pinned_sha_line':[l for l in src if l.startswith('PREREG_SHA256')],'refusal_lines':[(i,l.strip()) for i,l in enumerate(src,1) if 'not the pinned' in l or 'test_allow_unpinned_prereg' in l][:4]}
json.dump(E,open(sys.argv[1],'w'),indent=1); print('evidence written')
