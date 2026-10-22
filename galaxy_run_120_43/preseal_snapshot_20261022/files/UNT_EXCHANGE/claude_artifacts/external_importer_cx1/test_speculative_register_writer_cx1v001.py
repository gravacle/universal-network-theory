"""Inert stage-a writer tests; no referenced evidence or call roots exist."""
import sys, json, hashlib, tempfile, copy, subprocess
from pathlib import Path
base=Path(__file__).resolve().parent
sys.path.insert(0,str(base))
import speculative_register_writer_cx1v001 as writer
from snapshot_cx1v001 import Snapshot
from register_two_stage_cx1v003 import select_two_stage
root=Path(tempfile.mkdtemp(prefix='stage_a_writer_',dir=base/'inert_fixtures'))
def write(path,obj):
    raw=(json.dumps(obj,sort_keys=True)+'\n').encode()
    with path.open('xb') as f:f.write(raw)
    return {'path':str(path),'sha256':hashlib.sha256(raw).hexdigest()}
def filepin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
entries=[]
for row in sorted(writer.ROWS):
    key=hashlib.sha256(str(row).encode()).hexdigest()
    e={'row':row,'key':key,'call_root':str(root/('DDO154_JACOBIAN_R%d_%s_A1'%(row,key[:16]))),'attempt':1}
    for f in writer.PIN_FIELDS:e[f]={'path':str(root/('ABSENT_'+str(row)+'_'+f)),'sha256':hashlib.sha256((str(row)+f).encode()).hexdigest()}
    entries.append(e)
doc={'schema':'SPECULATIVE_REGISTER_L2_V001','entries':entries}
inp=write(root/'root_input.json',doc);out=root/'register.json'
r=subprocess.run([sys.executable,'-I','-B',str(base/'speculative_register_writer_cx1v001.py'),'--input',inp['path'],'--input-sha256',inp['sha256'],'--output',str(out)],capture_output=True,text=True)
assert r.returncode==0,(r.stdout,r.stderr)
registered=json.loads(r.stdout);assert registered==filepin(out)
assert json.loads(out.read_bytes())==doc
tested=['Actual isolated CLI publishes exactly seven rows and reports byte SHA']
context={k:hashlib.sha256(k.encode()).hexdigest() for k in ('config_sha256','cache_id','gate_digest')}
binding=write(root/'binding.json',{'schema':'SPECULATIVE_REGISTER_BINDING_L2_V001','register':registered,'context':context,'campaign_capture':entries[0]['runtime_capture'],'utc':'INERT','interpreter':{},'freeze':{}})
snap=Snapshot()
selected=select_two_stage(snap,register_pin=registered,binding_pin=binding,context=context,key=entries[0]['key'],spec_pin=entries[0]['spec'])
assert selected['entry']==entries[0] and len(snap.read_counts)==2
tested.append('Published document accepted by unchanged register_two_stage_cx1v003')
before=out.read_bytes()
try:writer.publish(inp['path'],inp['sha256'],str(out))
except FileExistsError:pass
else:raise AssertionError('overwrite accepted')
assert out.read_bytes()==before;tested.append('Existing output preserved')
dangling=root/'dangling';dangling.symlink_to(root/'never_created')
try:writer.publish(inp['path'],inp['sha256'],str(dangling))
except FileExistsError:pass
else:raise AssertionError('dangling symlink overwritten')
assert dangling.is_symlink() and not (root/'never_created').exists();tested.append('Dangling output symlink refused')
for name,mutate in [
 ('missing_row',lambda x:x['entries'].pop()),
 ('duplicate_row',lambda x:x['entries'][1].update(row=28)),
 ('boolean_row',lambda x:x['entries'][0].update(row=True)),
 ('duplicate_key',lambda x:x['entries'][1].update(key=x['entries'][0]['key'])),
 ('foreign_root',lambda x:x['entries'][0].update(call_root='/inert/wrong')),
 ('status_not_authority',lambda x:x['entries'][0].update(status='COMPLETED_VALID')),
 ('bad_pin',lambda x:x['entries'][0]['spec'].update(sha256='z'*64)),
 ('relative_pin',lambda x:x['entries'][0]['spec'].update(path='relative')),
 ('conflicting_pin',lambda x:x['entries'][1]['spec'].update(path=x['entries'][0]['spec']['path'])),
 ('zero_attempt',lambda x:x['entries'][0].update(attempt=0))]:
    obj=copy.deepcopy(doc);mutate(obj);p=write(root/(name+'.json'),obj);dest=root/(name+'_out.json')
    try:writer.publish(p['path'],p['sha256'],str(dest))
    except writer.Refusal:pass
    else:raise AssertionError(name)
    assert not dest.exists();tested.append(name+' refuses before output')
for name,path,sha in [('wrong_input_sha',inp['path'],'0'*64)]:
    dest=root/(name+'_out.json')
    try:writer.publish(path,sha,str(dest))
    except writer.Refusal:pass
    else:raise AssertionError(name)
    assert not dest.exists();tested.append(name+' refuses')
dup=root/'duplicate_keys.json';raw=b'{"schema":"X","schema":"Y","entries":[]}'
with dup.open('xb') as f:f.write(raw)
try:writer.publish(str(dup),hashlib.sha256(raw).hexdigest(),str(root/'duplicate_out.json'))
except writer.Refusal:pass
else:raise AssertionError('duplicate keys accepted')
tested.append('Duplicate JSON keys refuse')
alias=root/'input_symlink';alias.symlink_to(Path(inp['path']))
try:writer.publish(str(alias),inp['sha256'],str(root/'alias_out.json'))
except OSError:pass
else:raise AssertionError('input symlink accepted')
tested.append('Input final symlink refuses')
assert all(not Path(e[f]['path']).exists() for e in entries for f in writer.PIN_FIELDS)
assert all(not Path(e['call_root']).exists() for e in entries)
tested.append('Referenced pins and call roots never opened or created')
report={'status':'PASS','blocking_count':0,'tested':tested,'scope':__doc__,'pins':[filepin(base/'speculative_register_writer_cx1v001.py'),filepin(Path(__file__)),filepin(base/'register_two_stage_cx1v003.py'),registered],'untested':['Real root input authentication','Runtime capture content and chronology','Referenced pin bytes; native L2_DIRECT START snapshot must authenticate them before launch','No operational register or launch created']}
rp=write(root/'TEST_REPORT.json',report);print(json.dumps(rp))
