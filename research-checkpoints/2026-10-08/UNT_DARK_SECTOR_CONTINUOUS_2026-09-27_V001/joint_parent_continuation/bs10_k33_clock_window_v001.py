#!/usr/bin/env python3
"""Conditional local baseline phase windows from sealed clock JSON; no dynamics."""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import hashlib,json,math,os,resource,socket,sys,time,traceback
from pathlib import Path

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
PROTOCOL=J/'BS10_K33_CLOCK_WINDOW_V001.md';SOURCE=J/'bs10_k33_clock_window_v001.py'
RESULT=J/'BS10_K33_CLOCK_WINDOW_V001_RESULT.json';REPORT=J/'BS10_K33_CLOCK_WINDOW_V001_RESULT.md'
CP=J/'bs10_k33_clock_window_v001_checkpoints'
PRESULT=J/'BS10_K33_INTERNAL_CLOCK_V001_RESULT.json';PCP=J/'bs10_k33_internal_clock_v001_checkpoints'
ANCHORS={
 'BS10_K33_INTERNAL_CLOCK_V001_RESULT.json':'4d728596bfad33eb5006dab3c1c62d3f66a34ed909c9bcd8f94231e34f150ff4',
 'BS10_K33_INTERNAL_CLOCK_V001_RESULT.md':'3e2ed3b359bd0a3249b8d82be9b831d5cbab1498ec1926835a8ae25e54de17a4',
 'BS10_K33_INTERNAL_CLOCK_V001.md':'4700b457f5f5886e2291ee27131ef6dae71c25e4c352b017591494f9606ee23d',
 'bs10_k33_internal_clock_v001.py':'78191f1f80bde1792cc915e32a71bf466d3891046f79c081a8f43ec95373b540'}
GS=(0.,.1);STARTS=(0,413);AGES=(0.,5.,20.,50.);DELAYS=(0.,.1,.5,1.,2.,5.)
C1=1.4;C2=1.65;TOL=1e-14

def utc():return datetime.now(timezone.utc).isoformat()
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def canonical(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def exclusive(p,o):
    with p.open('x',encoding='utf-8') as f:json.dump(o,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def event(kind,**kw):
    with (CP/'events.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(dict(event=kind,pid=os.getpid(),utc=utc(),**kw),sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
def rss():return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
def check(c,name,ok,e=None):c.append(dict(name=name,passed=bool(ok),**({} if e is None else {'evidence':e})))
def le(c,name,x,y):
    allowance=TOL*max(1.,abs(x),abs(y));check(c,name,x<=y+allowance,dict(left=x,right=y,residual=x-y,floating_allowance=allowance))

def authenticate():
    hashes={str(PROTOCOL):sha(PROTOCOL),str(SOURCE):sha(SOURCE)}
    for name,h in ANCHORS.items():
        p=J/name
        if sha(p)!=h:raise RuntimeError('Frozen clock anchor changed: '+name)
        hashes[str(p)]=h
    parent=json.loads(PRESULT.read_text());unsealed=dict(parent);claim=unsealed.pop('canonical_payload_sha256')
    if canonical(unsealed)!=claim or claim!='d22dd535d35a504878308c3bc5ea9b8a84c19cd998f5b17429bc0a8e60d774c0':raise RuntimeError('Clock canonical seal mismatch')
    if parent['status']!='QUALIFIED_ARITHMETIC' or parent['failed_count'] or len(parent['rows'])!=16:raise RuntimeError('Clock parent incomplete/unqualified')
    manifest=json.loads((PCP/'manifest.json').read_text());events=[json.loads(s) for s in (PCP/'events.jsonl').read_text().splitlines() if s]
    if manifest!=parent['manifest'] or manifest['host']!=socket.gethostname():raise RuntimeError('Clock manifest/host mismatch')
    if not any(x.get('event')=='started' and x.get('manifest_sha256')==sha(PCP/'manifest.json') for x in events):raise RuntimeError('Clock started seal mismatch')
    for p,h in manifest['input_sha256'].items():
        if sha(Path(p))!=h:raise RuntimeError('Original clock input changed: '+p)
        hashes[p]=h
    native=str(J/'bs10_k33_unclamped_formation_v001.py')
    if hashes.get(native)!='2a6d6326592dee5fb04ba47776ea495df68c0acdf7dce22f26f4be0eae0a1b6c':raise RuntimeError('Native C1/C2 action custody mismatch')
    for p in (PCP/'manifest.json',PCP/'events.jsonl'):hashes[str(p)]=sha(p)
    census=[]
    for row in parent['rows']:
        key=f'g{GS.index(row["g"])}_n{row["start"]}_age{int(row["age"])}';p=PCP/(key+'.json')
        if json.loads(p.read_text())!=row or row['input_sha256']!=manifest['input_sha256'] or row['failed_count']:raise RuntimeError('Clock row metadata mismatch')
        if not any(x.get('event')=='row_complete' and x.get('key')==key and x.get('sha256')==sha(p) and x.get('failed')==0 for x in events):raise RuntimeError('Clock row journal mismatch')
        if tuple(x['delay'] for x in row['points'])!=DELAYS:raise RuntimeError('Clock point census mismatch')
        hashes[str(p)]=sha(p);census.append((row['g'],row['start'],row['age']))
    if sorted(census)!=sorted((g,n,t) for g in GS for n in STARTS for t in AGES):raise RuntimeError('Whole preparation census mismatch')
    if parent['clock_status_counts']!={'EXACT_ZERO_RATE_G0':48,'QUALIFIED_LOCAL_ABSOLUTE_PHASE':48}:raise RuntimeError('Clock status census mismatch')
    if not any(x.get('event')=='result_saved' and x.get('sha256')==ANCHORS[PRESULT.name] and x.get('canonical_payload_sha256')==claim for x in events):raise RuntimeError('Clock result journal seal mismatch')
    if not any(x.get('event')=='report_saved' and x.get('sha256')==ANCHORS['BS10_K33_INTERNAL_CLOCK_V001_RESULT.md'] for x in events):raise RuntimeError('Clock report journal seal mismatch')
    return hashes,parent

def point(row,p,checks):
    prefix=f't{p["delay"]}_';err=p['error_budgets'];rawnorm=p['raw_norm'];epsi=err['psi_vector']
    Nplus=max(1.,(math.sqrt(rawnorm)+epsi)**2)
    out=dict(delay=p['delay'],comparison_scope=p['comparison_scope'],parent_clock_status=p['clock_status'],raw_norm=rawnorm,conditional_exact_norm_upper=Nplus,start_error_budgets=err,raw_beta=p['beta'],raw_beta_dot=p['beta_dot'],raw_nu=p['nu'],clock_window_status=None,orientation=None,bminus=None,dplus=None,numinus=None,r1=None,r2=None,unrounded_radius=None,certified_radius=None,post_source_radius=None,delay_interval=None,absolute_native_age_interval=None,guaranteed_minimum_amplitude=None,guaranteed_minimum_absolute_rate=None,amplitude_change_bound=None,rate_change_bound=None)
    check(checks,prefix+'norm_budget_finite',math.isfinite(Nplus) and rawnorm>0 and epsi>=0)
    le(checks,prefix+'normalized_exact_seed_covered',1.,Nplus);le(checks,prefix+'raw_state_norm_covered',rawnorm,Nplus)
    if p['clock_status']=='EXACT_ZERO_RATE_G0':
        check(checks,prefix+'exact_g0_undefined_clock',row['g']==0. and p['nu']==0. and p['source_time_shift'] is None)
        out['clock_window_status']='UNDEFINED_ZERO_RATE_G0';return out
    check(checks,prefix+'prospective_qualified_input',row['g']==.1 and p['clock_status']=='QUALIFIED_LOCAL_ABSOLUTE_PHASE')
    b=math.hypot(*p['beta']);d=math.hypot(*p['beta_dot']);nu=p['nu'];bm=b-err['beta'];dp=d+err['beta_dot'];nm=abs(nu)-err['nu']
    check(checks,prefix+'positive_conditional_margins',all(math.isfinite(z) and z>0 for z in (bm,dp,nm)))
    if bm<=0 or nm<=0:raise ArithmeticError('Frozen qualified-clock error margins not positive')
    r1=bm/(4*C1*Nplus);den=C2/bm+C1*dp/bm**2;r2=nm/(4*Nplus*den);raw=min(r1,r2);r=math.nextafter(raw,0.)
    ampchange=C1*Nplus*r;ratechange=(4/3)*Nplus*r*den
    check(checks,prefix+'positive_finite_window',all(math.isfinite(z) and z>0 for z in (r1,r2,raw,r)))
    le(checks,prefix+'radius1_covered',r,r1);le(checks,prefix+'radius2_covered',r,r2);le(checks,prefix+'rounded_radius_conservative',r,raw)
    le(checks,prefix+'amplitude_change_limit',ampchange,bm/4);le(checks,prefix+'rate_change_limit',ratechange,nm/3)
    if p['delay']==0:
        post=r;interval=[0.,r];scope='ONE_SIDED_SOURCE_OFF_BASELINE'
        check(checks,prefix+'source_boundary_scope',p['comparison_scope']=='SOURCE_BOUNDARY_TANGENT_ONLY')
    else:
        post=min(r,p['delay']/2);interval=[p['delay']-post,p['delay']+post];scope='INTERIOR_SOURCE_OFF_BASELINE'
        le(checks,prefix+'interior_post_source_radius',post,p['delay']/2);le(checks,prefix+'interior_within_certified_radius',post,r)
        check(checks,prefix+'interior_nonnegative_delay',interval[0]>=0. and p['comparison_scope']=='INTERIOR_LOCAL_PHASE_CHART')
    out.update(clock_window_status='CONDITIONAL_LOCAL_BASELINE_WINDOW',window_scope=scope,orientation='POSITIVE' if nu>0 else 'NEGATIVE',bminus=bm,dplus=dp,numinus=nm,r1=r1,r2=r2,unrounded_radius=raw,certified_radius=r,post_source_radius=post,delay_interval=interval,absolute_native_age_interval=[row['age']+x for x in interval],guaranteed_minimum_amplitude=3*bm/4,guaranteed_minimum_absolute_rate=2*nm/3,amplitude_change_bound=ampchange,rate_change_bound=ratechange)
    return out

def execute():
    if sys.platform!='darwin' or Path(__file__).resolve()!=SOURCE.resolve():raise RuntimeError('Same Mac/source path only')
    if any(p.exists() for p in (CP,RESULT,REPORT)):raise RuntimeError('Exclusive outputs exist; no replay/resume authorized')
    hashes,parent=authenticate();CP.mkdir();t0=time.monotonic()
    manifest=dict(pid=os.getpid(),ppid=os.getppid(),host=socket.gethostname(),utc=utc(),input_sha256=hashes,inputs=dict(g=GS,starts=STARTS,ages=AGES,delays=DELAYS,C1=C1,C2=C2,floating_check_tolerance=TOL,rounding='nextafter_toward_zero',norm_upper='max(1,(sqrt(raw_norm)+e_psi)^2)',native_bound_tuple=dict(gmax=.1,h_N=.2,t=.1,lambdaR=.5),source_off_baseline_only=True,no_propagation_or_H_apply=True))
    exclusive(CP/'manifest.json',manifest);event('started',manifest_sha256=sha(CP/'manifest.json'));print(json.dumps(dict(pid=os.getpid(),ppid=os.getppid(),status='started')),flush=True)
    rows=[];checks=[]
    try:
        check(checks,'native_common_C1_bound',1+4*.1<=C1)
        check(checks,'native_common_C2_bound',1+2*.1+8*.1**2+3*.2*.5+4*.1*.1*math.sqrt(3)<C2)
        for old in parent['rows']:
            local=[];points=[point(old,p,local) for p in old['points']]
            row=dict(g=old['g'],start=old['start'],age=old['age'],input_sha256=hashes,points=points,checks=local,failed_count=sum(not x['passed'] for x in local),elapsed_seconds=time.monotonic()-t0,peak_RSS_bytes=rss());key=f'g{GS.index(old["g"])}_n{old["start"]}_age{int(old["age"])}';p=CP/(key+'.json');exclusive(p,row);event('row_complete',key=key,path=str(p),sha256=sha(p),failed=row['failed_count']);rows.append(row)
            print(json.dumps(dict(checkpoint=key,failed=row['failed_count'],local_windows=sum(x['clock_window_status']=='CONDITIONAL_LOCAL_BASELINE_WINDOW' for x in points))),flush=True)
        after,_=authenticate();check(checks,'input_bytes_unchanged',hashes==after)
        points=[p for r in rows for p in r['points']];counts={status:sum(p['clock_window_status']==status for p in points) for status in sorted({p['clock_window_status'] for p in points})}
        check(checks,'whole96_point_48defined_48undefined_census',len(rows)==16 and len(points)==96 and counts=={'CONDITIONAL_LOCAL_BASELINE_WINDOW':48,'UNDEFINED_ZERO_RATE_G0':48})
        combined=checks+[x for r in rows for x in r['checks']];failed=[x for x in combined if not x['passed']]
        payload=dict(status='QUALIFIED_ARITHMETIC' if not failed else 'FAILED_ARITHMETIC',qualification='Conditional local source-off baseline ensemble-clock windows under native commutator bounds and frozen start-error budgets only; no global monotone clock, finite kicked match, physical time/lapse, ruler, metric, gravity or cosmology',manifest=manifest,rows=rows,checks=checks,window_status_counts=counts,passed_count=len(combined)-len(failed),failed_count=len(failed),failed_checks=failed,runtime_seconds=time.monotonic()-t0,peak_RSS_bytes=rss(),pid=os.getpid());payload['canonical_payload_sha256']=canonical(payload);exclusive(RESULT,payload);event('result_saved',sha256=sha(RESULT),canonical_payload_sha256=payload['canonical_payload_sha256'])
        lines=['# K3,3 conditional local clock windows V001: sealed result','',f"{payload['status']}; {payload['passed_count']}/{len(combined)} controls,16 preparations/96 points.",'',payload['qualification'],'',f'Window census: {json.dumps(counts,sort_keys=True)}','', '| g | seed | age | native local radius range | post-source radius range |','|---|---:|---:|---|---|']
        for r in rows:
            rr=[p['certified_radius'] for p in r['points'] if p['certified_radius'] is not None];rp=[p['post_source_radius'] for p in r['points'] if p['post_source_radius'] is not None];lines.append(f"|{r['g']}|{r['start']}|{r['age']}|{None if not rr else [min(rr),max(rr)]}|{None if not rp else [min(rp),max(rp)]}|")
        lines+=['','Zero-rate g0 clocks remain undefined. Delay0 certificates are one-sided baseline windows and do not make an instantaneous pulse phase match physically accessible. Interior windows remain source-off baseline neighborhoods; no finite kicked trajectory is certified.',f"Runtime {payload['runtime_seconds']:.6f}s; peak RSS {payload['peak_RSS_bytes']}bytes; PID {os.getpid()}.",f'Raw result SHA256: {sha(RESULT)}',f"Canonical payload SHA256: {payload['canonical_payload_sha256']}",f'Protocol SHA256: {hashes[str(PROTOCOL)]}',f'Source SHA256: {hashes[str(SOURCE)]}','Every completed preparation has exclusive JSON/journal custody; all parent vectors/results remain unchanged. This process ends here with no replay or automatic continuation. Root integrates existing continuation log/ledger.']
        with REPORT.open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n');f.flush();os.fsync(f.fileno())
        event('report_saved',sha256=sha(REPORT));print(json.dumps(dict(status=payload['status'],passed=payload['passed_count'],failed=payload['failed_count'],window_status_counts=counts,result_sha256=sha(RESULT),report_sha256=sha(REPORT),runtime_seconds=payload['runtime_seconds'],peak_RSS_bytes=payload['peak_RSS_bytes'])),flush=True);return 0 if not failed else 2
    except BaseException as e:
        error=dict(status='INTERRUPTED_OR_FAILED',error=repr(e),traceback=traceback.format_exc(),pid=os.getpid(),runtime_seconds=time.monotonic()-t0,peak_RSS_bytes=rss());exclusive(CP/'error.json',error);event('error',sha256=sha(CP/'error.json'));print(json.dumps(error),flush=True);return 3

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--execute',action='store_true');args=p.parse_args()
    if args.execute:return execute()
    print('Prospective saved-data source only; final preflight/ownership approval precede one worker.');return 0
if __name__=='__main__':sys.exit(main())
