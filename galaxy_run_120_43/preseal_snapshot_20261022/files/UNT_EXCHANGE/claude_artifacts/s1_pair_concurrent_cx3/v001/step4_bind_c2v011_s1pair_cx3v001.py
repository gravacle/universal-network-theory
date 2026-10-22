"""CX3V001 S1 pair binder. assemble-pair preserves each child admission and call bytes; bind retains original exclusive publication contract."""
"""Prepare immutable step-4 plan/admission/command. Never publish authority or spawn.
Input admission is a ROOT-authorized candidate. Output needs independent root
publication of its byte hash; merely running this binder grants no authority.

c2v011 (s1_successors_c2; V006 A177 item (1), A182) = step4_bind_c2v010 (4d07dca3) with two changes:
  * it loads guard014 (6efdca01, V006 A172) by path and sha256 in place of guard011, so it validates guard014 /
    launcher015 plans (c2v010 refused them: LAUNCHER_GUARD_IDENTITY);
  * its command runs no nice (V006 A166 / A172): env with single-thread BLAS (kept, a determinism guard), then
    python -I -B <launcher> <plan> --execute-root-only. check_command refuses an argv carrying nice or renice
    (NICE_IN_COMMAND_REFUSED) before any output is written.
It lives in s1_successors_c2, so the packet folder its outputs must lie in is named (PACKET = c2v010's HERE.parent,
step4_launch_packet_cx1). Every other check is c2v010's.
"""
import argparse,copy,hashlib,json,os,shlex,types,sys
from pathlib import Path
PACKET=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1')
GUARD_PATH=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001/step4_guard_c2v014_s1pair_cx3v001.py')
GUARD_SHA256='1274a39a19a7d8540858b8f45be0b683e776fa4fc1386bec10871bb0342ac6cc'
GUARD_BYTES=GUARD_PATH.read_bytes()
if hashlib.sha256(GUARD_BYTES).hexdigest()!=GUARD_SHA256:
    raise PermissionError('GUARD_BOOTSTRAP_HASH_MISMATCH')
G=types.ModuleType('_step4_guard');G.__file__=str(GUARD_PATH)
exec(compile(GUARD_BYTES,str(GUARD_PATH),'exec'),G.__dict__)
PYTHON='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
NICE_PROGRAMS=frozenset({'nice','renice'})
def check_command(argv):
    # c2v011: the launcher command carries no nice (A166); single-thread BLAS stays.
    G.require(isinstance(argv,list) and bool(argv) and all(isinstance(x,str) for x in argv),'COMMAND_ARGV_REQUIRED')
    G.require(not any(os.path.basename(x) in NICE_PROGRAMS for x in argv),'NICE_IN_COMMAND_REFUSED')
    return argv
def bind(final_plan,admission_candidate,plan_out,admission_out,command_out):
    # Snapshot each input once; validation and publication consume these buffers.
    plan_path=G.safe_path(str(final_plan));plan_bytes=G.raw(plan_path)
    inp={'path':str(plan_path),'sha256':hashlib.sha256(plan_bytes).hexdigest()}
    plan=G.decode(plan_bytes);cfg=G.decode(G.raw(admission_candidate))
    G.require(cfg.get('plan') is None,'BINDER_REQUIRES_UNBOUND_ADMISSION_CANDIDATE')
    probe=copy.deepcopy(cfg);probe['plan']=inp
    G.validate(inp,plan['launcher']['path'],_candidate_config=probe,_plan_bytes=plan_bytes)
    outs=[G.safe_path(str(x)) for x in (plan_out,admission_out,command_out)]
    G.require(len(set(outs))==3,'DISTINCT_NEW_OUTPUTS_REQUIRED')
    for p in outs:
        G.require(p.is_relative_to(PACKET) and not os.path.lexists(p),'EXCLUSIVE_PACKET_OUTPUT_REQUIRED')
        for q in outs:G.require(p==q or not p.is_relative_to(q),'NESTED_OUTPUT_REFUSED')
    plan_ref={'path':str(outs[0]),'sha256':hashlib.sha256(plan_bytes).hexdigest()}
    cfg['plan']=plan_ref;cfg_bytes=json.dumps(cfg,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n'
    cfg_ref={'path':str(outs[1]),'sha256':hashlib.sha256(cfg_bytes).hexdigest()}
    argv=check_command(['env','OPENBLAS_NUM_THREADS=1','OMP_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1',PYTHON,'-I','-B',plan['launcher']['path'],str(outs[0]),'--execute-root-only'])
    command=('# Claude2 only, after independent review and published exact admission digest.\n'
             '# Set UNT_STEP4_ADMISSION_PATH and UNT_STEP4_ADMISSION_SHA256 from the independent publication.\n'
             '# This file does not export or self-authenticate those variables.\n'+shlex.join(argv)+'\n').encode()
    # All serialization and gates finish before the first exclusive write. Failures
    # preserve any prefix of the three outputs; no retry, cleanup or overwrite.
    for p,b in zip(outs,(plan_bytes,cfg_bytes,command)):
        with p.open('xb') as f:f.write(b)
    return {'label':'TESTED binding; production UNTESTED; root publication still required','plan':plan_ref,'admission':cfg_ref,'command':G.pin(outs[2])}
def main():
    if len(sys.argv)>1 and sys.argv[1]=='assemble-pair':return pair_main(sys.argv[2:])
    a=argparse.ArgumentParser()
    for name in ('final-plan','admission-candidate','plan-out','admission-out','command-out'):a.add_argument('--'+name,required=True)
    x=a.parse_args();print(json.dumps(bind(x.final_plan,x.admission_candidate,x.plan_out,x.admission_out,x.command_out),indent=2))

PAIR_LAUNCHER_PATH=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_pair_concurrent_cx3/v001/step4_launcher_c2v015_s1pair_cx3v001.py')
PAIR_LAUNCHER_SHA256='2e41da3746053f073d3c775de29c5c8df156deaa861e2b774ee88d7ab96808aa'
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

if __name__=='__main__':main()
