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
import argparse,copy,hashlib,json,os,shlex,types
from pathlib import Path
PACKET=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1')
GUARD_PATH=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_guard_c2v014.py')
GUARD_SHA256='6efdca016416a919b25a1e23d46a415b75fe2b5e60145ba098f864730975165d'
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
    a=argparse.ArgumentParser()
    for name in ('final-plan','admission-candidate','plan-out','admission-out','command-out'):a.add_argument('--'+name,required=True)
    x=a.parse_args();print(json.dumps(bind(x.final_plan,x.admission_candidate,x.plan_out,x.admission_out,x.command_out),indent=2))
if __name__=='__main__':main()
