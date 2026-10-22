"""Claude3 independent evidence for the NGC3198 parallel route-A launch packet (pre-announced in 0481). Read-only.
No result.json/finish.json/column/FAILURE record of any run is opened; the serial run's receipt is read for status fields only."""
import json, os, hashlib, sys, datetime
P='claude_artifacts/ngc_f10_c2/route_a_f10_parallel'; S='claude_artifacts/ngc_f10_c2/route_a_f10'; B='claude_artifacts/ngc_f10_c2/route_b_v006'
C2="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2"
def J(p): return json.load(open(p))
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def mt(p): return datetime.datetime.fromtimestamp(os.stat(p).st_mtime, datetime.timezone.utc).isoformat(timespec='seconds')
def diff(x,y,path,out):
    if type(x)!=type(y): out.append([path,'TYPE',str(x)[:80],str(y)[:80]]); return
    if isinstance(x,dict):
        for k in sorted(set(x)|set(y)):
            if k not in x: out.append([path+'/'+k,'ADDED',None,str(y[k])[:120]])
            elif k not in y: out.append([path+'/'+k,'REMOVED',str(x[k])[:120],None])
            else: diff(x[k],y[k],path+'/'+k,out)
    elif isinstance(x,list):
        if len(x)!=len(y): out.append([path,'LEN',len(x),len(y)])
        for i,(p,q) in enumerate(zip(x,y)): diff(p,q,f'{path}[{i}]',out)
    elif x!=y: out.append([path,'CHANGED',str(x)[:120],str(y)[:120]])
def leaves(o):
    if isinstance(o,dict): return sum(leaves(v) for v in o.values())
    if isinstance(o,list): return sum(leaves(v) for v in o)
    return 1
E={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}
ser=f'{S}/launcher/NGC3198_ROUTE_A_A2F10_REQUEST_C2V001.json'; n8=f'{P}/launcher/NGC3198_ROUTE_A_A2F10_PAR_N8_REQUEST_C2V002.json'; n3=f'{P}/launcher/NGC3198_ROUTE_A_A2F10_PAR_N3_REQUEST_C2V002.json'; tpl=f'{P}/route_b_spec/CALL_NGC3198_ROUTE_B_A2F10_PAR_TEMPLATE_C2V006.json'; tpl0=f'{B}/specs/CALL_NGC3198_ROUTE_B_A2F10_TEMPLATE_C2V006.json'
E['hashes']={'serial_request':sha(ser),'par_n8':sha(n8),'par_n3':sha(n3),'par_template':sha(tpl),'serial_template':sha(tpl0),'launcher_v002':sha(f'{P}/launcher/ngc_route_a_launch_c2v002.py'),'parallel_worker':sha('claude_artifacts/parallel_route_a_c2/ngc43_composite_coupled_root_worker_v002_parallel_c2v001.py'),'parallel_solver':sha('claude_artifacts/parallel_route_a_c2/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_c2v001.py'),'v006_driver':sha(f'{B}/galaxy_m0_forward_c2v006.py')}
a=J(ser); b8=J(n8); b3=J(n3)
o=[]; diff(a,b8,'',o); E['serial_to_n8']={'leaves_serial':leaves(a),'leaves_n8':leaves(b8),'diffs':o}
o=[]; diff(b3,b8,'',o); E['n3_to_n8']=o
# argv-level: which argv entries changed
E['argv_serial']=a['argv']; E['argv_n8']=b8['argv']
# pins equal apart from worker/solver
pk=set(a['launch_pins'])|set(b8['launch_pins']); E['launch_pins_changed']=[k for k in pk if a['launch_pins'].get(k)!=b8['launch_pins'].get(k)]
# template diff
o=[]; diff(J(tpl0),J(tpl),'',o); E['template_diff']=o
# B1: seed pins from bytes
seed=J('claude_artifacts/ngc_f10_c2/route_a_f10/seed/NGC3198_ROUTE_A_A2F10_SEED_C2V001.json'); E['seed_sha']=sha('claude_artifacts/ngc_f10_c2/route_a_f10/seed/NGC3198_ROUTE_A_A2F10_SEED_C2V001.json')
pins=seed.get('pins',{}); bad=[]
for p,h in pins.items():
    try: act=sha(p)
    except Exception as e: act='ERR '+str(e)
    if act!=h: bad.append({'path':p,'pinned':h[:8],'actual':act[:8],'mtime_utc':mt(p) if os.path.exists(p) else None})
E['seed_pin_mismatches']=bad; E['seed_pin_count']=len(pins)
# HASHES.txt from bytes
ok=0; badh=[]
for line in open(f'{P}/HASHES.txt'):
    parts=line.split()
    if len(parts)>=2 and len(parts[0])==64:
        h,rel=parts[0],parts[-1]; p=os.path.join(P,rel) if not os.path.isabs(rel) else rel
        if os.path.exists(p) and sha(p)==h: ok+=1
        else: badh.append(rel)
E['hashes_txt']={'ok':ok,'bad':badh[:10]}
# serial run receipt status only; PAR run absent?
rc=f'{C2}/runs/NGC3198_ROUTE_A_A2F10_RUN_V001.receipt.json'
if os.path.exists(rc):
    r=J(rc); E['serial_run_receipt']={k:r.get(k) for k in ('status','driver_status','exit_code','stop_reason','elapsed_seconds','peak_rss_bytes')}
E['serial_checkpoint_iteration0_names']=sorted(set(n.split('.')[0] for n in os.listdir(f'{C2}/runs/NGC3198_ROUTE_A_A2F10_RUN_V001/checkpoint/iteration_0000')))[:6] if os.path.isdir(f'{C2}/runs/NGC3198_ROUTE_A_A2F10_RUN_V001/checkpoint/iteration_0000') else None
E['par_run_absent']= not os.path.exists(f'{C2}/runs/NGC3198_ROUTE_A_A2F10_PAR_RUN_V001') and not os.path.exists(f'{C2}/runs/NGC3198_ROUTE_A_A2F10_PAR_RUN_V001.receipt.json')
# v006: any read of solver/worker sha against route-A results?
src=open(f'{B}/galaxy_m0_forward_c2v006.py').read().splitlines()
E['v006_solver_worker_refs']=[(i,l.strip()[:150]) for i,l in enumerate(src,1) if ("AUX['solver']" in l or 'code.solver' in l or "['solver']" in l or 'worker' in l.lower() and 'sha' in l.lower())][:30]
json.dump(E,open(sys.argv[1],'w'),indent=1)
print('serial->N8 leaves', E['serial_to_n8']['leaves_serial'], E['serial_to_n8']['leaves_n8'], 'ndiffs', len(E['serial_to_n8']['diffs']))
for d in E['serial_to_n8']['diffs']: print('  ', d[0], d[1], str(d[2])[-60:], '->', str(d[3])[-70:])
print('n3->n8', E['n3_to_n8']); print('launch_pins changed', E['launch_pins_changed'])
print('template diff', [(d[0],d[1]) for d in E['template_diff']])
print('seed pins', E['seed_pin_count'], 'mismatches', E['seed_pin_mismatches'])
print('HASHES.txt', E['hashes_txt']); print('serial receipt', E.get('serial_run_receipt')); print('iter0 names', E['serial_checkpoint_iteration0_names']); print('PAR run absent', E['par_run_absent'])
print('hashes', {k:v[:8] for k,v in E['hashes'].items()})
print('v006 refs:'); [print('  ',r) for r in E['v006_solver_worker_refs']]
