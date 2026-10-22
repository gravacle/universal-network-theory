"""Inert tests of the exact A226 comparator; never snapshots real inputs."""
import copy, contextlib, hashlib, io, json, tempfile, types
from pathlib import Path
source=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/pinned_input_envelope_c2v002/pinned_input_envelope_c2v002.py')
raw=source.read_bytes(); sha=hashlib.sha256(raw).hexdigest()
assert sha=='0fac239ad7e5573084bfa494e55a344f40ab4deaa3469d5d54671ca5b457598c'
m=types.ModuleType('inert_envelope');m.__file__=str(source);exec(compile(raw,str(source),'exec'),m.__dict__)
b=Path(tempfile.mkdtemp(prefix='envelope_',dir=Path(__file__).parent/'inert_fixtures')).resolve()
f=str(b/'unopened_input');h='a'*64
start={'schema':m.SCHEMA_MANIFEST,'label':'start','phase':'INERT_ONLY','created_epoch_ns':1,
 'pin_set':{'body_sha256':'b'*64,'file_sha256':'c'*64},'excluded':[],'unresolved_pins':[],
 'pins':[{'path':f,'sha256':h,'realpath':f,'status':'match','match':True}],
 'files':[{'file_key':f,'status':'ok','sha256_from_bytes':h,'size':1,'mtime_ns':1,'ctime_ns':1,'ino':1,'xattr_names':[]}]}
end=copy.deepcopy(start);end.update(label='end',created_epoch_ns=2)
def write(name,o):
 o=copy.deepcopy(o);o['body_sha256']=m.sha_b(m.canon(o).encode('ascii'))
 raw=json.dumps(o).encode();p=b/(name+'.json');p.write_bytes(raw)
 return str(p),hashlib.sha256(raw).hexdigest()
sp,sh=write('start',start);cases=[]
def check(name,e,rc=None,reason=None):
 ep,eh=write(name,e)
 try:
  with contextlib.redirect_stdout(io.StringIO()):got=m.compare(sp,ep,sh,eh,None)
  assert reason is None and got==rc,(name,got)
 except m.Refusal as exc:
  assert reason and reason in str(exc),(name,str(exc))
 cases.append(name)
check('unchanged',end,0)
for field,value in [('sha256_from_bytes','d'*64),('mtime_ns',3),('ctime_ns',3),('ino',2),('size',2)]:
 e=copy.deepcopy(end);e['files'][0][field]=value;check('changed_'+field,e,3)
e=copy.deepcopy(end);e['pins'][0]['status']='missing';e['pins'][0]['match']=False;check('missing',e,3)
e=copy.deepcopy(end);e['phase']='FOREIGN';check('foreign_phase',e,reason='PHASE_DIFFERS')
e=copy.deepcopy(end);e['label']='start';check('wrong_label',e,reason='END_NOT_LABELLED_END')
e=copy.deepcopy(end);e['pin_set']['file_sha256']='d'*64;check('foreign_pinset',e,reason='PIN_SET_DIFFERS')
assert not Path(f).exists()
report={'status':'PASS','blocking_count':0,'scope':'Pinned envelope comparator on fabricated inert manifests only',
 'tested':cases,'untested':['Real collection/snapshots','Importer single-read integration','Required coverage and root approval of pin set'],
 'source':{'path':str(source),'sha256':sha}}
p=b/'TEST_REPORT.json';p.write_text(json.dumps(report,indent=2)+'\n');print(p)
