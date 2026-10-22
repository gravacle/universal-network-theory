import tempfile,types,os,hashlib,json
from pathlib import Path
from runtime_fingerprints_cx1v001 import FileFingerprints,module_fingerprint,FingerprintRefusal
root=Path(__file__).resolve().parent;case=Path(tempfile.mkdtemp(prefix='fingerprints_',dir=root/'inert_fixtures'))
p=case/'binary';p.write_bytes(b'INERT INTERPRETER');q=case/'module';q.write_bytes(b'INERT MODULE');alias=case/'module_alias';os.link(q,alias)
f=FileFingerprints();interpreter=f.capture(p);assert interpreter['sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
passed=['interpreter fixture bytes hashed']
m=types.ModuleType('inert');m.__file__=str(q);m.__version__='1.0'
a=module_fingerprint(m,files=f,interpreter=interpreter,sys_version='inert-python',stdlib_names=set())
assert a['sha256']==hashlib.sha256(b'INERT MODULE').hexdigest();passed.append('module version and source bytes recorded')
m.__file__=str(alias);z=module_fingerprint(m,files=f,interpreter=interpreter,sys_version='inert-python',stdlib_names=set())
assert z['sha256']==a['sha256'] and f.content_reads==2;passed.append('hard-link aliases share one content read')
for origin in ('built-in','frozen'):
 mod=types.ModuleType('inert_stdlib');mod.__spec__=types.SimpleNamespace(origin=origin)
 r=module_fingerprint(mod,files=f,interpreter=interpreter,sys_version='inert-python',stdlib_names={'inert_stdlib'})
 assert r['sha256']==interpreter['sha256'] and r['identity_basis']=='interpreter_binary';passed.append(origin+' explicitly binds interpreter bytes')
for label,mod in [('missing version',types.ModuleType('unknown')),('missing file',types.ModuleType('no_file'))]:
 if label=='missing file':mod.__version__='1'
 try:module_fingerprint(mod,files=f,interpreter=interpreter,sys_version='inert-python',stdlib_names=set())
 except FingerprintRefusal:passed.append(label+' refuses')
 else:raise AssertionError(label)
r=dict(status='PASS',blocking_count=0,scope='Runtime fingerprint primitives; inert files/modules only',tested=passed,untested=['Actual import resolution/version coverage','macOS runtime capture','Launch-time authentication','Capture producer entry'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),root/'runtime_fingerprints_cx1v001.py']])
p=case/'TEST_REPORT.json'
with p.open('x') as out:json.dump(r,out,indent=2);out.write('\n')
print(p)
