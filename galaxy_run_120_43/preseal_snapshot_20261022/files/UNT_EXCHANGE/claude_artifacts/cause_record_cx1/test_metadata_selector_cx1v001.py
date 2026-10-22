import sys,json,hashlib,os,tempfile,importlib.util
from pathlib import Path
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('metadata_selector_cx1v001.py')
s=importlib.util.spec_from_file_location('reader',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
rows=[]
def test(name,fn):
 try:fn();rows.append({'name':name,'pass':True})
 except Exception as e:rows.append({'name':name,'pass':False,'error_type':type(e).__name__})
def eq(a,b):assert a==b
def refuses(fn):
 try:fn()
 except m.Refused:return
 raise AssertionError('accepted')
sel=lambda raw,paths,kind='finish':m.Selector(raw,kind).select(paths)
test('status_only_ignores_predictions',lambda:eq(sel(b'{"status":"FAILED","predictions":[{"value":12345}]}',[('status',)]),{('status',):'FAILED'}))
test('forbidden_prediction_access',lambda:refuses(lambda:sel(b'{"predictions":2}',[('predictions',)])))
test('forbidden_nested_access',lambda:refuses(lambda:sel(b'{"status":"FAILED"}',[('reasons',)])))
test('selected_array_refused',lambda:refuses(lambda:sel(b'{"status":[1]}',[('status',)])))
test('selected_object_refused',lambda:refuses(lambda:sel(b'{"status":{}}',[('status',)])))
test('duplicate_refused',lambda:refuses(lambda:sel(b'{"status":"FAILED","status":"COMPLETED"}',[('status',)])))
test('escaped_duplicate_refused',lambda:refuses(lambda:sel(b'{"status":"FAILED","statu\\u0073":"COMPLETED"}',[('status',)])))
test('unselected_array_does_not_alias',lambda:eq(sel(b'{"unused":[{"status":"secret"}]}',[('status',)]),{}))
test('trailing_refused',lambda:refuses(lambda:sel(b'{"status":"FAILED"} null',[('status',)])))
test('missing_is_missing',lambda:eq(sel(b'{}',[('status',)]),{}))
test('receipt_signal',lambda:eq(sel(b'{"exit_code":-9}',[('exit_code',)],'receipt'),{('exit_code',):-9}))
test('nonfinite_refused',lambda:refuses(lambda:sel(b'{"exit_code":NaN}',[('exit_code',)],'receipt')))
test('malformed_skipped_refused',lambda:refuses(lambda:sel(b'{"status":"FAILED","rows":[1,]}',[('status',)])))
# json decoder spy: selected strings/key names only, never skipped scalar/array content.
def spy():
 old=m.json.loads;seen=[]
 def load(x,*a,**kw):seen.append(x);return old(x,*a,**kw)
 m.json.loads=load
 try:eq(sel(b'{"status":"FAILED","rows":["SECRET_VALUE",456]}',[('status',)]),{('status',):'FAILED'})
 finally:m.json.loads=old
 assert not any(b'SECRET_VALUE' in x or b'456' in x for x in seen)
test('unselected_values_never_decoded',spy)
# No cleanup/deletion: retained inert artifacts.
d=Path(tempfile.mkdtemp(prefix='cx1_cause_reader_inert_'));a=d/'metadata.json';a.write_bytes(b'{"status":"FAILED"}');alias=d/'alias.json';os.link(a,alias)
opens=[]
def audit(event,args):
 if event=='open' and args and str(args[0]) in (str(a),str(alias)):opens.append(str(args[0]))
sys.addaudithook(audit)
r=m.OneRead();expected=hashlib.sha256(b'{"status":"FAILED"}').hexdigest()
def one():
 x,_=r.read(a,expected);y,_=r.read(alias,expected);z,_=r.read(a,expected)
 assert x is y and y is z;assert len(opens)==1
 eq(sel(x,[('status',)]),{('status',):'FAILED'})
test('audit_hook_single_read_inode_alias',one)
test('tampered_pin_refused',lambda:refuses(lambda:r.read(a,'0'*64)))
result={'tests':rows,'passed':sum(x['pass'] for x in rows),'total':len(rows),'audit_opens':opens,'inert_folder':str(d),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
print(json.dumps(result,indent=2));sys.exit(0 if all(x['pass'] for x in rows) else 1)
