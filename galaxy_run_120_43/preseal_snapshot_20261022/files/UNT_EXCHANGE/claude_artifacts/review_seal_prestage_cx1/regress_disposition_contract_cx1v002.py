"""0640 strict envelope and inert same-path/sha regression. Never run a real root script."""
import argparse,copy,hashlib,json,os,re,shlex,subprocess,types
from pathlib import Path
sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--snapshot',required=True);ap.add_argument('--snapshot-sha',required=True);ap.add_argument('--outdir',required=True);a=ap.parse_args()
 mb=Path(a.snapshot).read_bytes();assert sha(mb)==a.snapshot_sha;m=json.loads(mb);sources={}
 for r in m['inputs']:
  p=Path(r['snapshot']);b=p.read_bytes();assert sha(b)==r['sha256'];sources[p.name]=b
 out=Path(a.outdir);assert str(out).startswith('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/');out.mkdir()
 def put(p,b):
  b=b.encode() if isinstance(b,str) else b
  with p.open('xb') as f:f.write(b)
  return str(p),sha(b)
 ns={'__name__':'inert_contract_review','__file__':str(out/'helper_identity.py')};exec(compile(sources['helper.py'],'owned_helper_snapshot','exec'),ns)
 # Exact one table row, unchanged, followed by one later entry. No actual scientific content.
 s82=b'## A82: Inert table entry\nUnchanged fixture text.\n';s83=b'## A83: Inert later entry\nAdditional fixture text.\n'
 fp,fh=put(out/'inert_frozen.md',s82+s83)
 doc={'entries_after_A81':{'rows':[{'entry':'A82','section_sha256':sha(s82),'section_bytes':len(s82),'decision':'NO_CHANGE','reason':'Inert unchanged row.'}]}}
 pp,ph=put(out/'inert_prereg.json',json.dumps(doc))
 row={'entry':'A83','disposition':'no_change','reason':'Inert later-entry disposition.','section_sha256':sha(s83)}
 valid={'schema':'UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001','frozen_addendum_sha256':fh,'entries':[row]}
 cases=[('valid_exact_object',valid,True),('legacy_bare_list',[row],False),('legacy_dispositions',{'dispositions':[row]},False),('legacy_rows',{'rows':[row]},False),('extra_top_key',dict(valid,extra='unused'),False),('wrong_schema',dict(valid,schema='WRONG'),False),('missing_schema',{k:v for k,v in valid.items() if k!='schema'},False),('missing_frozen_pin',{k:v for k,v in valid.items() if k!='frozen_addendum_sha256'},False),('wrong_frozen_pin',dict(valid,frozen_addendum_sha256='0'*64),False),('entries_not_list',dict(valid,entries={}),False)]
 shape=[]
 for name,obj,want in cases:
  dp,dh=put(out/(name+'.json'),json.dumps(obj))
  args=types.SimpleNamespace(dispositions=dp,dispositions_sha=dh,prereg=pp,prereg_sha=ph,frozen=fp,frozen_sha=fh)
  try:ns['_dispositions'](args);accepted=True;detail='ACCEPT'
  except ns['Refuse'] as e:accepted=False;detail=str(e).split(':')[0]
  except Exception as e:accepted=None;detail='UNEXPECTED '+type(e).__name__+': '+str(e)
  shape.append({'id':name,'expected_accept':want,'actual_accept':accepted,'passed':accepted==want,'detail':detail})
 validpath=str(out/'valid_exact_object.json');validsha=sha(Path(validpath).read_bytes())
 try:ns['_dispositions'](types.SimpleNamespace(dispositions=validpath,dispositions_sha='0'*64,prereg=pp,prereg_sha=ph,frozen=fp,frozen_sha=fh));detail='ACCEPT'
 except ns['Refuse'] as e:detail=str(e).split(':')[0]
 except Exception as e:detail='UNEXPECTED '+type(e).__name__
 shape.append({'id':'wrong_file_sha','passed':detail.startswith('PIN_BYTES_MISMATCH'),'detail':detail})
 # Copy only three inspected function bodies; all original executable/tool/helper entries are replaced with inert shell functions.
 # This validates argv transport, not the real tools' IO or cryptographic checks.
 script=sources['script.sh'].decode();functions=[]
 for name in ('step2_tool1','step6_tool3','step10_tool4'):
  start=script.index(name+'() {');end=script.index('\n}',start)+2;functions.append(script[start:end])
 selected='\n'.join(functions)
 assert all(x not in selected for x in ('step9_validity','"$PY"')) and not re.search(r'--validity-only(?:\s|$)',selected)
 transport=[]
 for case,mutate in [('same_pair',False),('negative_pin_rebind',True)]:
  caseout=out/case;caseout.mkdir();logs=caseout/'logs';logs.mkdir();capture=caseout/'capture';capture.mkdir()
  names=set(re.findall(r'\$(?:\{)?([A-Z][A-Z0-9_]*)',selected))
  setup='set -Eeuo pipefail\nset -o noclobber\n'
  for name in sorted(names-{'T1_RUN','T3_RUN','T4_RUN','TOOL_PINS','COV_ARGS'}):setup+=name+'='+shlex.quote(str(caseout/('dummy_'+name)))+'\n'
  mapping={'LOGS':str(logs),'CAP':str(capture),'UNT_SEAL_DISPOSITIONS_PATH':validpath,'UNT_SEAL_DISPOSITIONS_SHA256':validsha,'SEAL_TOOLS_COVERED_LATER_MODE':'v003_dispositions','T_DISPOSITIONS_FLAG':'--dispositions','T_DISPOSITIONS_SHA_FLAG':'--dispositions-sha','T4_STDOUT':str(caseout/'tool4_stdout.json'),'T4_STDERR':str(caseout/'tool4_stderr.json')}
  for k,v in mapping.items():setup+=k+'='+shlex.quote(v)+'\n'
  setup+='''T1_RUN=(capture_tool T1); T3_RUN=(capture_tool T3); T4_RUN=(capture_tool T4); TOOL_PINS=(inert=inert)
PIN_COUNT=0
capture_tool() { local name="$1"; shift; printf '%s\0' "$@" > "$CAP/$name.argv"; printf '{}\n'; }
H() { PIN_COUNT=$((PIN_COUNT+1)); printf '%s\0' "$@" > "$CAP/pin$PIN_COUNT.argv"; printf '{}\n' >&2; }
run_h() { :; }
v005_still_frozen() { :; }
jf() { printf 'inert\n'; }
'''
  call='\nstep2_tool1\n'
  if mutate:call+='UNT_SEAL_DISPOSITIONS_PATH='+shlex.quote(str(caseout/'rebound_dispositions.json'))+'\n'
  call+='step6_tool3\nstep10_tool4\n'
  sp,_=put(caseout/'inert_transport.sh',setup+selected+call)
  proc=subprocess.run(['/bin/bash',sp],capture_output=True,text=True)
  def args(n):return [x.decode() for x in (capture/n).read_bytes().split(b'\0') if x]
  expected=(validpath,validsha);observed={};pins={};errors=[]
  if proc.returncode==0:
   for tool in ('T1','T3','T4'):
    av=args(tool+'.argv');observed[tool]=[av[av.index('--dispositions')+1],av[av.index('--dispositions-sha')+1]]
   for i in range(1,4):
    av=args('pin%d.argv'%i);pin=next(x for x in av if x.endswith('='+validsha));pins[str(i)]=pin
   allsame=all(tuple(v)==expected for v in observed.values()) and all(v==validpath+'='+validsha for v in pins.values())
  else:allsame=None;errors=[proc.stderr[:500]]
  transport.append({'id':case,'passed':allsame==(not mutate),'all_tools_and_checks_same_pair':allsame,'expected_pair':expected,'tool_args':observed,'pin_args':pins,'returncode':proc.returncode,'errors':errors})
 result={'date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'label':'TESTED_0640_INERT_CONTRACT_AND_TRANSPORT','snapshot':{'path':a.snapshot,'sha256':a.snapshot_sha},'harness':{'path':__file__,'sha256':sha(Path(__file__).read_bytes())},'shape_controls':shape,'shape_passed':sum(x['passed'] for x in shape),'shape_total':len(shape),'positive_shape_passed':shape[0]['passed'],'negative_shape_limits':'Negative controls alone do not establish strict acceptance while the positive control fails.','transport_controls':transport,'transport_passed':sum(x['passed'] for x in transport),'transport_total':len(transport),'nice':os.getpriority(os.PRIO_PROCESS,0),'scope':'Owned snapshot helper; three extracted functions with inert tools. No original root script, comparator, protected data or target data. Same-file test proves argv transport only; semantic D05 and tool IO are separate.'}
 rp=out/'RESULTS.json';put(rp,json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'path':str(rp),'sha256':sha(rp.read_bytes()),'shape':str(result['shape_passed'])+'/'+str(result['shape_total']),'transport':str(result['transport_passed'])+'/'+str(result['transport_total'])}))
if __name__=='__main__':main()
