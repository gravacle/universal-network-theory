"""Read-only CP1 list record validation; exclusive registration/staging only. No proof or solver execution."""
import argparse, copy, hashlib, json, os, shlex, types
from pathlib import Path
ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
OUTPUT=ART/'cp1_list_rho_slot_cx1'
CHECKS=(ART/'s4rc1_c3/rho_registration_c2v001/cp1_registry_checks_c2v001.py','6e46698eb0f8500d62d1c39d6bcf449acd0ac1c876c20fafb9ba6bafe93774ad')
COMMON=(ART/'h3_campaign_path_c2/cp1_points_common_c2v001.py','302abdad6b076190f7bc8e79cc71cf4de91402a1a216eb94c254acf2be22c27e')
PYTHON='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
class Refusal(ValueError):pass
def need(x,msg):
 if not x:raise Refusal(msg)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def decode(raw):
 def pairs(items):
  out={}
  for k,v in items:
   need(k not in out,'DUPLICATE_JSON_KEY');out[k]=v
  return out
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(Refusal('NONFINITE_JSON')))
def path(p):
 p=str(p);need(os.path.isabs(p) and os.path.realpath(p)==p,'NONCANONICAL_PATH')
 q=Path(p);need(q.is_relative_to(ART),'OUTSIDE_ARTIFACTS')
 need(not any(x in ('runs','runs_ext') or x.startswith(('UVT_','C5H')) for x in q.parts),'FORBIDDEN_PATH')
 return q
class Snapshot:
 def __init__(self):self.cache={};self.counts={}
 def raw(self,p,sha=None,label='input'):
  p=path(p);s=str(p)
  if s not in self.cache:
   need(p.is_file(),'MISSING_INPUT '+s)
   with p.open('rb') as f:b=f.read()
   self.cache[s]=(b,hashlib.sha256(b).hexdigest());self.counts[s]=1
  b,h=self.cache[s];need(sha is None or h==sha,'SHA_MISMATCH '+label);return b,h
 def pin(self,p):return {'path':str(path(p)),'sha256':self.raw(p)[1]}
 def doc(self,p,sha=None):return decode(self.raw(p,sha)[0])
 def ref(self,p):
  need(isinstance(p,dict) and set(p)=={'path','sha256'} and isinstance(p['sha256'],str) and len(p['sha256'])==64,'EXACT_PIN_REQUIRED')
  return self.doc(p['path'],p['sha256'])
 def module(self,pin,name):
  b,_=self.raw(str(pin[0]),pin[1],name);m=types.ModuleType(name);m.__file__=str(pin[0]);exec(compile(b,str(pin[0]),'exec'),m.__dict__);return m

def setup(s):
 H=s.module(CHECKS,'pinned_registration_checks');H.read_raw=s.raw
 P=s.module(COMMON,'pinned_list_common')
 table,C=H.table();S=H.slot_consts()
 shim=types.SimpleNamespace(Refusal=Refusal,ART=str(ART),is_pin=H.is_pin,point_rows=lambda:table,
  require_policy=lambda p,*a:str(path(p)),require_canonical=lambda p:str(path(p)),
  read_bytes_pinned=lambda ref,*a,**k:canonical(s.ref(ref)),point_key=lambda spec:digest(H.point_identity(spec,C['DRIVER_SHA'])))
 # Preserve original bytes: loader hashes via Snapshot and parses those exact bytes.
 def read(ref,*a,**k):s.ref(ref);return s.raw(ref['path'],ref['sha256'])[0]
 shim.read_bytes_pinned=read
 return H,P,C,S,shim

def collect(s,list_ref,out_root,keys,anchor_ref,approved_ref):
 H,P,C,S,shim=setup(s);doc,rows=P.load_points_list(shim,list_ref)
 need(keys and len(keys)==len(set(keys)),'UNIQUE_FULL_KEYS_REQUIRED')
 by={r['key']:r for r in rows};need(all(k in by for k in keys),'KEY_NOT_IN_LIST')
 rows=[r for r in rows if r['key'] in keys]
 root=path(out_root);need(root.is_dir() and root.parent==ART/'s4rc1_c3' and root.name.startswith('cp1_run_'),'CP1_OUT_ROOT_REQUIRED')
 approved=s.ref(approved_ref).get('approved_certificate_producers')
 expected=[{'path':C['PINS'][n][0],'sha256':C['PINS'][n][1]} for n in C['CANONICAL_APPROVED_PRODUCERS']]
 need(approved==expected,'APPROVED_PRODUCERS_NOT_CANONICAL')
 for p in approved:s.raw(p['path'],p['sha256'])
 anchor=s.ref(anchor_ref);pair=anchor.get('anchor_rho_pair');registered=anchor.get('registered_rho_records')
 need(isinstance(pair,list) and len(pair)==2 and all(H.is_pin(p) for p in pair),'MISSING_ANCHOR_PAIR')
 need(isinstance(registered,list) and all(p in registered for p in pair),'ANCHOR_UNREGISTERED')
 need(pair[0]['path']!=pair[1]['path'] and pair[0]['sha256']!=pair[1]['sha256'],'ANCHOR_NOT_TWO_RUNS')
 ar=[s.ref(p) for p in pair]
 for a in ar:H.check_rho_record(a,S,'anchor');need(a.get('point_sha256')==S['ANCHOR_KEY'],'WRONG_ANCHOR_KEY')
 need(ar[0]['identity']==ar[1]['identity'] and ar[0].get('custody')==ar[1].get('custody'),'ANCHOR_IDENTITY_CUSTODY')
 need(H.rho_bitwise_canonical(ar[0],S)==H.rho_bitwise_canonical(ar[1],S),'ANCHOR_NOT_BITWISE_EQUAL')
 for p in S['ROOT_RULINGS']:s.raw(p['path'],p['sha256'])
 points=[];deps=set()
 for row in rows:
  key=row['key'];k=key[:16];folder=root/('P%02d_%s_%s_a1'%(row['row'],k,row['label']))
  matches=sorted(root.glob('P%02d_%s_*'%(row['row'],k)))
  need(matches==[folder] and folder.is_dir() and not folder.is_symlink(),'POINT_DIR_NOT_UNIQUE')
  need(sorted(folder.glob('RHO_NUMERIC_*'))==[folder/('RHO_NUMERIC_'+k+'_a.json')],'RHO_RECORD_SET_UNEXPECTED')
  rho=s.pin(folder/('RHO_NUMERIC_'+k+'_a.json'));rr=s.ref(rho);H.check_rho_record(rr,S,'point rho')
  spec=s.doc(row['spec_path'],row['spec_sha256']);ident=H.point_identity(spec,C['DRIVER_SHA'])
  need(rr['identity']==ident and rr['point_sha256']==key,'WRONG_RHO_KEY')
  ep=s.pin(folder/('EPS_PROOF_'+k+'.json'));gp=s.pin(folder/('GQ_PROOF_'+k+'.json'))
  ed=s.ref(ep);gd=s.ref(gp);en=s.pin(folder/('EPS_NUMERIC_'+k+'.json'));er=s.ref(en)
  need(ed.get('driver_certificate')==en,'EPS_SLOT_NOT_THIS_POINT')
  need(er.get('schema')==H.EPS_NUMERIC_SCHEMA and er.get('identity')==ident,'EPS_IDENTITY')
  need(er.get('settings')=='registered' and er.get('full_registered_search_executed') is True,'PARTIAL_EPS')
  custody=er.get('custody');need(isinstance(custody,dict) and set(custody)==H.CUSTODY_KEYS and rr.get('custody')==custody,'CUSTODY_MISMATCH')
  for gate,p in [('EPS',ed),('GQ',gd)]:
   need(p.get('schema')==C['PROOF_SCHEMA'] and p.get('gate')==gate and p.get('status')=='TESTED' and p.get('verdict')=='PASS','PROOF_NOT_PASS')
   need(p.get('point_sha256')==key and p.get('custody_sha256')==digest(custody) and p.get('producer') in approved,'PROOF_IDENTITY_CUSTODY_PRODUCER')
  need(gd.get('all_production_kperp_nodes') is True and gd.get('nodes_tested')==gd.get('production_nodes'),'PARTIAL_GQ')
  deps.add(digest({'dependencies':er.get('dependencies'),'producer':er.get('producer')}))
  points.append({'row':row,'spec':spec,'rho_ref':rho,'eps_ref':en,'eps_proof':ep,'gq_proof':gp})
 need(len(deps)==1,'EPS_SOURCE_PINS_DIFFER')
 reg={'schema':'CP1_LIST_RHO_REGISTRATION_CX1V001','points_list':list_ref,'cp1_out_root':str(root),'keys':[p['row']['key'] for p in points],
  'anchor_registration':anchor_ref,'anchor_rho_pair':pair,'approved_producers':approved_ref,
  'registered_rho_records':[p['rho_ref'] for p in points]+pair,
  'slot_rho_by_row':[{'row':p['row']['row'],'key':p['row']['key'],'label':p['row']['label'],'rho_ref':p['rho_ref']} for p in points],
  'eps_source_pins_digest':next(iter(deps)),'scope':'Registration candidate for root pinning; no LO certification or launch authority.'}
 return reg,points,approved,S

def filled_check(spec,filled,rho,eps,registered):
 need(rho in registered,'RHO_UNREGISTERED')
 want=copy.deepcopy(spec);want['numerics']['uv_tail'].update(lo_certificate=rho,eps_certificate=eps)
 need(filled==want,'FILLED_SLOT_OR_NON_SLOT_MISMATCH')
def encode(x):return json.dumps(x,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n'
def write_set(dest,outputs):
 dest=path(dest);need(dest.is_relative_to(OUTPUT) and dest!=OUTPUT and not os.path.lexists(dest),'NEW_OUTPUT_DIRECTORY_REQUIRED')
 need(dest.parent.is_dir(),'OUTPUT_PARENT_REQUIRED')
 dest.mkdir()
 for name,b in outputs.items():
  with (dest/name).open('xb') as f:f.write(b)
 return {n:{'path':str(dest/n),'sha256':hashlib.sha256(b).hexdigest()} for n,b in outputs.items()}
def main():
 a=argparse.ArgumentParser();a.add_argument('command',choices=['register','stage'])
 for k in ['points-list','points-list-sha256','out-root','anchor-registration','anchor-registration-sha256','approved-producers','approved-producers-sha256','output-dir']:a.add_argument('--'+k,required=True)
 a.add_argument('--key',action='append',required=True);a.add_argument('--registration');a.add_argument('--registration-sha256')
 a.add_argument('--slot-out-root');a.add_argument('--bundle-out-root');v=a.parse_args();s=Snapshot()
 def ref(n):return {'path':getattr(v,n),'sha256':getattr(v,n+'_sha256')}
 try:
  reg,pts,approved,S=collect(s,ref('points_list'),v.out_root,v.key,ref('anchor_registration'),ref('approved_producers'))
  outputs={};dest=path(v.output_dir)
  if v.command=='register':outputs['RHO_REGISTRATION.json']=encode(reg)
  else:
   need(v.registration and v.registration_sha256,'ROOT_PINNED_REGISTRATION_REQUIRED')
   actual=s.ref(ref('registration'));need(actual==reg,'REGISTRATION_DIFFERS_OR_UNREGISTERED_RHO')
   slot=path(v.slot_out_root or '');bundle=path(v.bundle_out_root or '')
   need(slot.parent==ART/'s4rc1_c3' and slot.name.startswith('lo_slot_'),'SLOT_OUT_ROOT_POLICY')
   need(bundle.parent==ART/'s4rc1_c3' and bundle.name.startswith('registry_'),'BUNDLE_OUT_ROOT_POLICY')
   commands=[]
   for p in pts:
    row=p['row'];k=row['key'][:16];tag='P%02d_%s'%(row['row'],k)
    filled=copy.deepcopy(p['spec']);filled['numerics']['uv_tail'].update(lo_certificate=p['rho_ref'],eps_certificate=p['eps_ref'])
    filled_check(p['spec'],filled,p['rho_ref'],p['eps_ref'],actual['registered_rho_records'])
    name='FILLED_SPEC_'+tag+'.json';b=encode(filled);outputs[name]=b
    args={'spec_ref':{'path':str(dest/name),'sha256':hashlib.sha256(b).hexdigest()},'rho_ref':p['rho_ref'],'registered_rho_records':actual['registered_rho_records'],'anchor_rho_pair':actual['anchor_rho_pair'],'root_ruling_refs':S['ROOT_RULINGS'],'approved_producer_sha256':[q['sha256'] for q in approved]}
    an='SLOT_ARGS_'+tag+'.json';ab=encode(args);outputs[an]=ab
    commands.append(shlex.join(['/usr/sbin/taskpolicy','-b',PYTHON,'-I','-B',str(ART/'s4rc1_c3/proof_side_c3v003/lo_slot_proof_c3v003.py'),'--args',str(dest/an),'--args-sha256',hashlib.sha256(ab).hexdigest(),'--out-root',str(slot)]))
    commands.append(shlex.join([PYTHON,'-I','-B',str(ART/'h3_campaign_path_c2/cp1_points_assembler_c2v001.py'),'bundle','--points-list',v.points_list,'--points-list-sha256',v.points_list_sha256,'--out-root',str(bundle),'--point',row['key'],'--eps-proof',p['eps_proof']['path'],'--gq-proof',p['gq_proof']['path'],'--lo-proof',str(slot/('LO_RHO_SLOT_PROOF_'+k+'.json')),'--approved-producers',v.approved_producers]))
   outputs['COMMANDS.txt']=('# Root only after review; tools not executed here. Create output roots first. Run slot proofs at least one second apart.\n'+'\n'.join(commands)+'\n').encode()
  outputs['INPUT_SNAPSHOT.json']=encode({'inputs':[{'path':p,'sha256':h} for p,(b,h) in s.cache.items()],'read_counts':s.counts,'opened_record_types':['RHO_NUMERIC','EPS_NUMERIC','EPS_PROOF','GQ_PROOF'],'launches_performed':0})
  pins=write_set(dest,outputs);print(json.dumps({'status':'PASS','outputs':pins,'launches_performed':0}))
 except (ValueError,OSError,KeyError,TypeError,AttributeError) as e:print(json.dumps({'status':'REFUSED','reason':str(e),'launches_performed':0}));return 2
 return 0
if __name__=='__main__':raise SystemExit(main())
