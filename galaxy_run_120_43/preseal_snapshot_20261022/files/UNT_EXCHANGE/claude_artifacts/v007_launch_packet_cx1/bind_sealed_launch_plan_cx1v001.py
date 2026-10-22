"""0576 build-only plan binding. Never starts a process. Root supplies the frozen addendum and chosen driver."""
import argparse,copy,hashlib,json,shlex
from pathlib import Path
HERE=Path(__file__).resolve().parent
PYTHON='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
def pin(p):return {'path':str(Path(p).resolve()),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def bind(template,driver,driver_sha,addendum,addendum_sha,plan_out,command_out):
 plan=json.loads(Path(template).read_bytes());dr=pin(driver);ad=pin(addendum)
 if dr['sha256']!=driver_sha or ad['sha256']!=addendum_sha:raise ValueError('ROOT_SUPPLIED_PIN_MISMATCH')
 if plan.get('driver')!=dr:raise ValueError('CHOSEN_DRIVER_DOES_NOT_MATCH_TEMPLATE')
 for key in ('launcher','guard','monitor'):
  if pin(plan[key]['path'])!=plan[key]:raise ValueError('TEMPLATE_SOURCE_CHANGED')
 for call in plan['calls']:
  if pin(call['spec']['path'])!=call['spec']:raise ValueError('TEMPLATE_SPEC_CHANGED')
 outs=[Path(plan_out),Path(command_out)]
 if outs[0].resolve()==outs[1].resolve():raise ValueError('DISTINCT_OUTPUTS_REQUIRED')
 for p in outs:
  if not p.resolve().is_relative_to(HERE) or p.exists() or p.is_symlink():raise ValueError('NEW_BUILD_OUTPUT_REQUIRED')
 plan['frozen_addendum']=ad;plan['seal_binding_status']='BOUND_BUILD_ONLY_ROOT_SEAL_AND_AUTHORIZATION_STILL_REQUIRED';plan['template_pin']=pin(template)
 cmd=shlex.join([PYTHON,'-I','-B',plan['launcher']['path'],str(outs[0].resolve()),'--execute-root-only'])
 with outs[0].open('x') as f:json.dump(plan,f,indent=1);f.write('\n')
 with outs[1].open('x') as f:f.write('# Claude2 only after root seal/config/receipt publication, independently verified UNT_ROOT_ADMISSION_SHA256 and all root gates. This generator launches nothing.\n'+cmd+'\n')
 return {'label':'TESTED byte binding only; production UNTESTED','plan':pin(outs[0]),'command':pin(outs[1]),'driver':dr,'frozen_addendum':ad}
def main():
 p=argparse.ArgumentParser()
 for name in ('template','driver','driver-sha256','frozen-addendum','frozen-addendum-sha256','plan-out','command-out'):p.add_argument('--'+name,required=True)
 a=p.parse_args();print(json.dumps(bind(a.template,a.driver,a.driver_sha256,a.frozen_addendum,a.frozen_addendum_sha256,a.plan_out,a.command_out),indent=1))
if __name__=='__main__':main()
