"""Exclusive successor builder. Source bytes only; no production modules executed."""
import ast,hashlib,json,sys
from pathlib import Path
BASE=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2')
PINS={'step4_guard_c2v014.py':'6efdca016416a919b25a1e23d46a415b75fe2b5e60145ba098f864730975165d','step4_launcher_c2v015.py':'cd987edd097323999847208d7b5fdfd93dadecb8a10beb6feaf91a0c53b68e0b','step4_bind_c2v011.py':'d3d9702eb8096d11b98461f1c62c67931b9ecf74957cee95fbc3a60f60deaea0'}
def raw(name):
 b=(BASE/name).read_bytes();assert hashlib.sha256(b).hexdigest()==PINS[name];return b.decode()
def replace_fn(src,name,text):
 n=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name==name)
 lines=src.splitlines(True);return ''.join(lines[:n.lineno-1])+text+'\n'+''.join(lines[n.end_lineno:])
def write(d,name,s):
 ast.parse(s);p=d/name
 with p.open('x') as f:f.write(s)
 return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
HELPERS=r"""
# CX3V001 / A274: exactly two immutable legacy single-call admissions feed one batch.
# Each retains its own C1/context. Parent source review covers the union and these successors.
S1_PAIR_PARENT_GUARD={'path':'/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_guard_c2v014.py','sha256':'6efdca016416a919b25a1e23d46a415b75fe2b5e60145ba098f864730975165d'}
S1_PAIR_PARENT_LAUNCHER={'path':'/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_launcher_c2v015.py','sha256':'cd987edd097323999847208d7b5fdfd93dadecb8a10beb6feaf91a0c53b68e0b'}
def pair_case_admission(cfg,call):
    refs=cfg.get('s1_pair_admissions')
    require(isinstance(refs,dict) and set(refs)==set(S1_OVERLAP_CASES),'S1_PAIR_ADMISSIONS_REQUIRED')
    case=call.get('case');require(case in S1_OVERLAP_CASES,'S1_PAIR_CASE_REQUIRED')
    child=doc(refs[case])
    require(child.get('schema')=='UNT_STEP4_ADMISSION_CX1V001' and child.get('authority')==AUTHORITY and child.get('status')=='ROOT_AUTHORIZED','S1_PAIR_CHILD_ROOT_AUTHORITY')
    require('s1_pair_admissions' not in child,'S1_PAIR_NESTED_ADMISSION_REFUSED')
    source_map(child);check_review(child)
    require(all(cfg['sources'].get(p)==h for p,h in child['sources'].items()),'S1_PAIR_SOURCE_UNION_REQUIRED')
    require(child.get('v007')==cfg.get('v007'),'S1_PAIR_VERDICT_MISMATCH')
    require(child.get('core_priority')==cfg.get('core_priority'),'S1_PAIR_CORE_PRIORITY_MISMATCH')
    require(child.get('case_order')==[case],'S1_PAIR_CHILD_ORDER')
    require(child.get('calls')=={case:{'spec':call['spec'],'driver':call['driver'],'prelaunch':call.get('prelaunch')}},'S1_PAIR_CHILD_CALL_BINDING')
    require(child.get('caps')=={case:{k:call.get(k) for k in ('wall_cap_s','rss_cap_bytes','output_cap_bytes')}},'S1_PAIR_CHILD_CAP_BINDING')
    original=doc(child.get('plan'))
    require(original.get('schema')=='UNT_STEP4_LAUNCH_PLAN_CX1V001' and original.get('binding_status')=='ROOT_BOUND' and original.get('batch')=='POST_S1','S1_PAIR_CHILD_PLAN_REQUIRED')
    require(original.get('guard')==S1_PAIR_PARENT_GUARD and original.get('launcher')==S1_PAIR_PARENT_LAUNCHER,'S1_PAIR_CHILD_LINEAGE')
    require(original.get('calls')==[call],'S1_PAIR_CHILD_CALL_BYTES')
    require(original.get('s1',{}).get('fill_record')==cfg.get('s1_overlap',{}).get('fill_record'),'S1_PAIR_CHILD_FILL_BINDING')
    rule=dict(cfg['route_a_admission'],max_active=1)
    require(original.get('route_a_admission')==rule and child.get('route_a_admission')==rule,'S1_PAIR_CHILD_RAMP_BINDING')
    if child.get('core_priority')==CORE_PRIORITY_S1_OVERLAP:
        require(child.get('s1_overlap')==cfg.get('s1_overlap'),'S1_PAIR_CHILD_OVERLAP_BINDING')
    for k in ('config','context_module','adoption_policy','direct_context'):verify(child.get(k))
    return child
"""
CORE=r"""def core_priority_admission(plan,cfg):
    # S1-specific successor: never admits a HEADLINE/DIII/sensitivity batch.
    require(plan.get('batch')=='POST_S1','S1_PAIR_POST_S1_REQUIRED')
    cp=cfg.get('core_priority')
    require(cp in (CORE_PRIORITY_INACTIVE,CORE_PRIORITY_S1_OVERLAP),'CORE_PRIORITY_ATTESTATION_REQUIRED')
    calls=plan.get('calls')
    require(isinstance(calls,list) and len(calls)==2 and all(isinstance(c,dict) for c in calls),'S1_PAIR_TWO_CALLS_REQUIRED')
    require([c.get('case') for c in calls]==list(S1_OVERLAP_CASES),'S1_PAIR_EXACT_ORDER_REQUIRED')
    require(type(plan.get('route_a_admission',{}).get('max_active')) is int and plan['route_a_admission']['max_active']==2,'S1_PAIR_MAX_ACTIVE_TWO_REQUIRED')
    require(plan.get('s1_pair_admissions')==cfg.get('s1_pair_admissions'),'S1_PAIR_PLAN_ADMISSION_BINDING')
    ov=cfg.get('s1_overlap')
    require(isinstance(ov,dict),'S1_OVERLAP_ADMISSION_REQUIRED')
    require(set(ov)=={'schema','replay_module','fill_record'} and ov.get('schema')==S1_OVERLAP_SCHEMA,'S1_OVERLAP_ADMISSION_SCHEMA')
    require(isinstance(plan.get('s1'),dict) and plan['s1'].get('fill_record')==ov['fill_record'],'S1_OVERLAP_FILL_RECORD_BINDING')
    verify(ov['fill_record'])
    m=load(ov['replay_module'],cfg,'_step4_s1_replay')
    require(getattr(m,'S1_REPLAY_API',None)==S1_REPLAY_API,'S1_OVERLAP_REPLAY_API')
    try:rep=m.guard_replay(ov['fill_record'])
    except Exception as e:raise Refusal('S1_OVERLAP_REPLAY_REFUSED',str(getattr(e,'code',None) or type(e).__name__)) from e
    configs=[]
    for call in calls:
        require(call.get('tail_on') is True and isinstance(call.get('driver'),dict) and call['driver'].get('sha256')==R5_SHA,'S1_OVERLAP_TAIL_ON_R5_REQUIRED')
        got=(rep.get('cases') or {}).get(call['case']) if isinstance(rep,dict) else None
        require(isinstance(got,dict) and got.get('spec')==call.get('spec'),'S1_OVERLAP_SPEC_NOT_FILLED_SPEC')
        require(got.get('bytes')==verify(call['spec']),'S1_OVERLAP_REPLAY_MISMATCH')
        configs.append(pair_case_admission(cfg,call)['config'])
    require(configs[0]!=configs[1],'S1_PAIR_DISTINCT_C1_REQUIRED')
    return calls
"""
ASSEMBLE=r"""
PAIR_LAUNCHER_PATH=Path(__PAIR_PATH__)
PAIR_LAUNCHER_SHA256=__PAIR_SHA__
REPLAY_PIN={'path':'/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/s1_path_lib_c2v002c.py','sha256':'99e2be175e546992c70984435bc480e1eddb90b052fda65ddcbfe8780bdbd27e'}
def assemble_pair(admissions,source_review,launcher_log,plan_out,candidate_out):
    # Reads only immutable inputs. No child admission/spec/plan is changed.
    G.require(isinstance(admissions,dict) and set(admissions)==set(G.S1_OVERLAP_CASES),'S1_PAIR_ADMISSIONS_REQUIRED')
    children=[G.doc(admissions[c]) for c in G.S1_OVERLAP_CASES]
    originals=[G.doc(c['plan']) for c in children]
    G.require(all(len(p.get('calls',[]))==1 for p in originals),'S1_PAIR_SINGLE_PARENTS_REQUIRED')
    calls=[copy.deepcopy(p['calls'][0]) for p in originals]
    for p in originals:G.require(p.get('monitor')==originals[0].get('monitor'),'S1_PAIR_MONITOR_MISMATCH')
    for k in ('fill_record','theta_key','branch','attempt'):
        G.require(originals[0].get('s1',{}).get(k)==originals[1].get('s1',{}).get(k),'S1_PAIR_COMMON_'+k.upper())
    review=G.doc(source_review)
    cfg=copy.deepcopy(children[0]);cfg['plan']=None
    for k in ('config','context_module','adoption_policy','direct_context'):cfg.pop(k,None)
    cfg['sources']=review.get('approved_sources');cfg['source_review']=source_review
    cfg['s1_pair_admissions']=copy.deepcopy(admissions)
    cfg['case_order']=list(G.S1_OVERLAP_CASES)
    cfg['calls']={c['case']:{'spec':c['spec'],'driver':c['driver'],'prelaunch':c.get('prelaunch')} for c in calls}
    cfg['caps']={c['case']:{k:c[k] for k in ('wall_cap_s','rss_cap_bytes','output_cap_bytes')} for c in calls}
    cfg['route_a_admission']=dict(originals[0]['route_a_admission'],max_active=2)
    cfg['s1_overlap']={'schema':G.S1_OVERLAP_SCHEMA,'fill_record':originals[0]['s1']['fill_record'],'replay_module':REPLAY_PIN}
    plan=copy.deepcopy(originals[0]);plan['calls']=calls;plan['launcher_log']=str(launcher_log)
    plan['guard']={'path':str(GUARD_PATH),'sha256':GUARD_SHA256}
    plan['launcher']={'path':str(PAIR_LAUNCHER_PATH),'sha256':PAIR_LAUNCHER_SHA256}
    plan['route_a_admission']=copy.deepcopy(cfg['route_a_admission'])
    plan['s1_pair_admissions']=copy.deepcopy(admissions)
    plan['s1'].pop('k',None)
    plan['s1']['case_k']={c:p['s1'].get('k') for c,p in zip(G.S1_OVERLAP_CASES,originals)}
    raw=G.canonical(plan)+b'\n';outs=[G.safe_path(str(p)) for p in (plan_out,candidate_out)]
    G.require(len(set(outs))==2,'DISTINCT_NEW_OUTPUTS_REQUIRED')
    for p in outs:
        G.require(p.parent.is_dir() and p.is_relative_to(PACKET) and not os.path.lexists(p),'EXCLUSIVE_PACKET_OUTPUT_REQUIRED')
        for q in outs:G.require(p==q or not p.is_relative_to(q),'NESTED_OUTPUT_REFUSED')
    pref={'path':str(outs[0]),'sha256':hashlib.sha256(raw).hexdigest()}
    probe=copy.deepcopy(cfg);probe['plan']=pref
    G.validate(pref,str(PAIR_LAUNCHER_PATH),_candidate_config=probe,_plan_bytes=raw)
    cbytes=G.canonical(cfg)+b'\n'
    for p,b in zip(outs,(raw,cbytes)):
        with p.open('xb') as f:f.write(b)
    return {'schema':'UNT_S1_PAIR_ASSEMBLY_CX3V001','launch_authorized':False,'plan':pref,'admission_candidate':G.pin(outs[1]),'child_admissions':admissions}
def pair_pin(text):
    path,sep,sha=text.rpartition('@');G.require(bool(sep),'PIN_AT_SHA_REQUIRED')
    ref={'path':path,'sha256':sha};G.verify(ref);return ref
def pair_main(argv):
    a=argparse.ArgumentParser(description='Assemble the two approved S1 single-call inputs into one pair, no launch.')
    for n in ('c3t-admission','c4t-admission','source-review','launcher-log','plan-out','candidate-out'):a.add_argument('--'+n,required=True)
    x=a.parse_args(argv)
    refs=dict(zip(G.S1_OVERLAP_CASES,(pair_pin(x.c3t_admission),pair_pin(x.c4t_admission))))
    print(json.dumps(assemble_pair(refs,pair_pin(x.source_review),x.launcher_log,x.plan_out,x.candidate_out),indent=2))
"""
def build(d):
 d=Path(d);d.mkdir()
 g=raw('step4_guard_c2v014.py')
 g='"""CX3V001 S1 pair successor, A274/0838. Two calls, separate pinned C1s, one batch lock. HEADLINE11 uses unchanged guard014."""\n'+g
 g=g.replace('def native_preflight(cfg,call):\n','def native_preflight(cfg,call):\n    cfg=pair_case_admission(cfg,call)\n',1)
 g=replace_fn(g,'core_priority_admission',CORE)
 pos=g.index('\ndef validate(');g=g[:pos]+HELPERS+g[pos:]
 gp=write(d,'step4_guard_c2v014_s1pair_cx3v001.py',g)
 l=raw('step4_launcher_c2v015.py').replace("HERE/'step4_guard_c2v014.py'","HERE/'step4_guard_c2v014_s1pair_cx3v001.py'").replace(PINS['step4_guard_c2v014.py'],gp['sha256'])
 l='"""CX3V001 S1 pair launcher: one worker holds the unchanged machine lock for both calls. Runtime functions byte-for-byte AST-equal to launcher015."""\n'+l
 lp=write(d,'step4_launcher_c2v015_s1pair_cx3v001.py',l)
 b=raw('step4_bind_c2v011.py').replace('import argparse,copy,hashlib,json,os,shlex,types','import argparse,copy,hashlib,json,os,shlex,types,sys')
 b=b.replace(str(BASE/'step4_guard_c2v014.py'),gp['path']).replace(PINS['step4_guard_c2v014.py'],gp['sha256'])
 b=b.replace('def main():\n','def main():\n    if len(sys.argv)>1 and sys.argv[1]==\'assemble-pair\':return pair_main(sys.argv[2:])\n',1)
 extra=ASSEMBLE.replace('__PAIR_PATH__',repr(lp['path'])).replace('__PAIR_SHA__',repr(lp['sha256']))
 b=b.replace("if __name__=='__main__':main()",extra+"\nif __name__=='__main__':main()")
 b='"""CX3V001 S1 pair binder. assemble-pair preserves each child admission and call bytes; bind retains original exclusive publication contract."""\n'+b
 bp=write(d,'step4_bind_c2v011_s1pair_cx3v001.py',b)
 rec={'files':[gp,lp,bp],'parents':{str(BASE/k):v for k,v in PINS.items()}}
 with (d/'BUILD_RECORD_CX3V001.json').open('x') as f:json.dump(rec,f,indent=2);f.write('\n')
 print(json.dumps(rec))
if __name__=='__main__':build(sys.argv[1])
