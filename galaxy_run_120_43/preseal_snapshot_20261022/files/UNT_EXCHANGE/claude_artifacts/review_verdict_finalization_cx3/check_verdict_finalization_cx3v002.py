"""A205/0770 byte-and-tuple check. Never imports or runs production modules.
CLI: --self-test OUTPUT.json, or --manifest ROOT_NAMED_INPUTS.json --output OUTPUT.json.
Live manifest entries are {path,sha256}; chain/published are ordered policy/core/wrapper[/entry].
Run only after root names every live input. Outputs are exclusive and in this lane.
"""
import argparse, ast, copy, hashlib, json, subprocess
from pathlib import Path
H=Path(__file__).parent
A=H.parent
CX=A/'calib_tail_readiness_cx2'
PH=A/'h3_campaign_path_c2/placeholder_chain_c2v004/v006r12_c4'
CTRL=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
CMP=CTRL/'V007_SEAL_ASSEMBLY/kmax_tail_compare_c2v007_r14_cx1v001_SEALED_V007.py'
PRE=CTRL/'V007_SEAL_ASSEMBLY/KMAX_TAIL_PREREG_V007_SEALED.json'
T4=('a99105a19b582c68d961e0ee12be3a2efa79dbd1e65d63682c3d2d8daa55f0ab','b2989012c92161a7da3dd10d0148e1607422416d369fc4ebe164217758b5c695','c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1','UNT_KMAX_TAIL_COMPARISON_C2V007_R11')
KEYS=('compare_sha256','prereg_sha256','addendum_sha256','report_schema','verdict_sha256')
NAMES=('adoption_policy_cx2v006r12_c4.py','calibration_core_cx2v006r12_c4.py','calibration_orchestrator_cx2v006r12_c4_q5b1.py','h3_campaign_entry_cx2v006r12_c4.py')
PINS=('93d9c0acdb3e9fd40ec63ed0db7c1356b6d2b025eeb5bcde57a2ffebdbd04ba3','192d086348fed9307da99732c0ef146bb336a3d605afc1e9e56b6ce959ad1a73','381fa2957edabf18032afba9a8ff026744f6cc1d933efb5f3d30f289ea9decb9','dd9c951bbe2a374ff56059a392b49e65d3ca369d849b307e7365d28226c0b116')
DISCLOSURE='Codex3 holds generator/output-diff review, campaign-set review, certificate-policy signing and per-wave EPS signing. Codex3 revised postseal_records/srb_rot and LAUNCH_PLAN/CASES_MANIFEST pieces feeding V. This checks byte equality and tuple identity only, not independent verdict content.'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def require(ok,msg):
 if not ok:raise ValueError(msg)
def pin(p):return {'path':str(p),'sha256':sha(p.read_bytes())}
def baseline():
 out=[]
 for n,s in zip(NAMES,PINS):
  b=(PH/n).read_bytes();require(sha(b)==s,'placeholder pin '+n);out.append(b)
 r10=(CX/'v006r10_c4/adoption_policy_cx2v006r10_c4.py').read_bytes()
 require(sha(r10)==PINS[0] and r10==out[0],'r10 policy pin')
 return out

def changed(a,b):
 x=a.splitlines(keepends=True);y=b.splitlines(keepends=True)
 require(len(x)==len(y),'line count')
 return [i for i,(p,q) in enumerate(zip(x,y),1) if p!=q]
def replace1(raw,old,new):
 require(raw.count(old)==1,'replacement occurrence')
 return raw.replace(old,new)
def report_projection(raw):
 # 0770 authorizes only these seven field paths and sha256 of complete bytes.
 d=json.loads(raw)
 out={'schema':d.get('schema'),'script_sha256':d.get('script_sha256'),
      'prereg.sha256':(d.get('prereg') or {}).get('sha256'),
      'pins_verified.V005_addendum':(d.get('pins_verified') or {}).get('V005_addendum'),
      'decision.outcome':(d.get('decision') or {}).get('outcome'),
      'decision.tests_read':(d.get('decision') or {}).get('tests_read'),'test_mode':d.get('test_mode')}
 require(out['decision.outcome']=='ADOPT_TAIL' and out['decision.tests_read'] is True and out['test_mode'] is False,'STOP: report not sealed ADOPT_TAIL')
 require((out['script_sha256'],out['prereg.sha256'],out['pins_verified.V005_addendum'],out['schema'])==T4,'report tuple fields')
 return out

def expected_chain(base,t):
 p=replace1(base[0],b'# No final V007 seal has been supplied. A root-reviewed immutable successor',b'# The V007 seal tuple below was registered at the A126 finalization, after the V007 verdict. A root-reviewed immutable successor')
 p=replace1(p,b'APPROVED_V007_SEALS = frozenset()',('APPROVED_V007_SEALS = frozenset({'+repr(t)+'})').encode())
 c=replace1(base[1],PINS[0].encode(),sha(p).encode())
 w=replace1(base[2],PINS[1].encode(),sha(c).encode())
 e=replace1(base[3],PINS[2].encode(),sha(w).encode())
 return [p,c,w,e]

def check_bytes(base,report_raw,r11,chain,published,seal,regen,report_pin):
 projected=report_projection(report_raw);t=T4+(sha(report_raw),);td=dict(zip(KEYS,t))
 require(report_pin['sha256']==t[4],'report supplied sha')
 require(seal.get('schema')=='H3_V007_SEAL_TUPLE_RECORD_C2V001' and seal.get('status')=='ROOT_FILLED','seal status/schema')
 require(seal.get('tuple')==td,'seal tuple')
 require(seal.get('report')==report_pin,'seal report binding')
 require(seal.get('compare')=={'path':str(CMP),'sha256':t[0]},'seal compare binding')
 expect=expected_chain(base,t)
 require(r11==expect[0],'r11 extra/missing change or wrong tuple')
 require(len(chain)==4 and chain==expect,'r12 extra/missing change or wrong hash pin')
 diffs=[changed(a,b) for a,b in zip(base,chain)]
 require(diffs==[[13,16],[202],[29],[61]],'r12 diff shape')
 require(regen.get('schema')=='H3_REGENERATE_RECORD_C2V004' and regen.get('dry_run') is False,'regenerate schema/dry_run')
 require(regen.get('tuple')==td and regen.get('report')==report_pin and regen.get('compare')==seal['compare'],'regenerate tuple/binding')
 require(regen.get('outputs')=={n:sha(b) for n,b in zip(NAMES,chain)},'regenerate outputs')
 require(len(published)==3 and published==chain[:3],'publication differs')
 return {'tuple':td,'permitted_report_fields':projected,'r11_diff_lines':changed(base[0],r11),'r12_diff_lines':diffs,'publication_equal':True,'status':'PASS'}

def self_test():
 b=baseline()
 report={'schema':T4[3],'script_sha256':T4[0],'prereg':{'sha256':T4[1]},'pins_verified':{'V005_addendum':T4[2]},'decision':{'outcome':'ADOPT_TAIL','tests_read':True},'test_mode':False}
 raw=json.dumps(report,sort_keys=True).encode();t=T4+(sha(raw),);ch=expected_chain(b,t);rp={'path':str(H/'SYNTHETIC_REPORT_NOT_WRITTEN.json'),'sha256':sha(raw)}
 seal={'schema':'H3_V007_SEAL_TUPLE_RECORD_C2V001','status':'ROOT_FILLED','tuple':dict(zip(KEYS,t)),'report':rp,'compare':{'path':str(CMP),'sha256':T4[0]}}
 regen={'schema':'H3_REGENERATE_RECORD_C2V004','dry_run':False,'tuple':seal['tuple'],'report':rp,'compare':seal['compare'],'outputs':{n:sha(v) for n,v in zip(NAMES,ch)}}
 args=[b,raw,ch[0],ch,ch[:3],seal,regen,rp]
 rows=[{'case':'positive synthetic sealed ADOPT_TAIL byte chain','passed':check_bytes(*args)['status']=='PASS'}]
 cases=[]
 for path,val in [(('decision','outcome'),'DO_NOT_ADOPT'),(('decision','tests_read'),False),(('test_mode',),True),(('schema',),'WRONG_SCHEMA')]:
  r=copy.deepcopy(report)
  if len(path)==2:r[path[0]][path[1]]=val
  else:r[path[0]]=val
  a=copy.deepcopy(args);a[1]=json.dumps(r).encode();cases.append(('.'.join(path),a))
 a=copy.deepcopy(args);a[2]+=b'# extra\n';cases.append(('r11 extra line',a))
 for i in range(4):
  a=copy.deepcopy(args);a[3][i]+=b'# extra\n';cases.append(('r12 extra line '+str(i),a))
 a=copy.deepcopy(args);a[5]['tuple']['verdict_sha256']='0'*64;cases.append(('seal wrong V',a))
 a=copy.deepcopy(args);a[6]['outputs'][NAMES[1]]='0'*64;cases.append(('regenerate wrong output',a))
 a=copy.deepcopy(args);a[4][2]+=b'# extra\n';cases.append(('published wrapper mismatch',a))
 for name,a in cases:
  try:check_bytes(*a)
  except (ValueError,TypeError,KeyError) as e:rows.append({'case':name,'passed':True,'refusal':str(e)})
  else:rows.append({'case':name,'passed':False})
 require(all(r['passed'] for r in rows),'self-test failed')
 return {'status':'TESTED','scope':'synthetic checker controls only; no live input','checks':rows,'count':len(rows),'actual_verdict_review':'UNTESTED'}

def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--self-test');g.add_argument('--manifest');ap.add_argument('--output');args=ap.parse_args()
 if args.self_test:out=Path(args.self_test);result=self_test()
 else:
  require(args.output is not None,'output required');out=Path(args.output);m=json.loads(Path(args.manifest).read_bytes());opened=[]
  def read(p):
   require(set(p)=={'path','sha256'} and Path(p['path']).is_absolute(),'input pin shape');raw=Path(p['path']).read_bytes();require(sha(raw)==p['sha256'],'input bytes pin '+p['path']);opened.append(p);return raw
  require(sha(CMP.read_bytes())==T4[0] and sha(PRE.read_bytes())==T4[1],'sealed byte pins')
  report=read(m['report']);report_projection(report)  # stop before other live files if verdict fails
  r11=read(m['r11']);seal=json.loads(read(m['seal_record']));regen=json.loads(read(m['regenerate_record']))
  require(regen.get('seal_record')==m['seal_record'],'regenerate seal record binding')
  ch=[read(p) for p in m['chain']];pub=[read(p) for p in m['published']]
  result=check_bytes(baseline(),report,r11,ch,pub,seal,regen,m['report']);result['inputs']=opened;result['manifest']=pin(Path(args.manifest))
 require(out.absolute().is_relative_to(H),'output outside own lane')
 result.update(date_u=subprocess.check_output(['/bin/date','-u'],text=True).strip(),checker=pin(Path(__file__)),disclosure=DISCLOSURE)
 with out.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps({'result':pin(out),'status':result['status'],'checks':result.get('count')}))
if __name__=='__main__':main()
