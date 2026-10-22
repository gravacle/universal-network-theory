import tempfile,types,os,hashlib,json
from pathlib import Path
from runtime_fingerprints_cx1v002 import FileFingerprints,module_fingerprint,FingerprintRefusal
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
pkgdir=case/'inert_package';pkgdir.mkdir();init=pkgdir/'__init__.py';init.write_bytes(b'INERT PACKAGE');child=pkgdir/'child.py';child.write_bytes(b'INERT CHILD')
pkg=types.ModuleType('inert_package');pkg.__path__=[str(pkgdir)];pkg.__file__=str(init);pkg.__version__='2.0'
sub=types.ModuleType('inert_package.child');sub.__file__=str(child)
a=module_fingerprint(sub,files=f,interpreter=interpreter,sys_version='inert-python',stdlib_names=set(),package_roots={'inert_package':pkg})
assert a['version']=='2.0' and a['version_provider']['sha256']==hashlib.sha256(b'INERT PACKAGE').hexdigest();passed.append('submodule version bound to captured package file')
sub.__file__=str(q)
try:module_fingerprint(sub,files=f,interpreter=interpreter,sys_version='inert-python',stdlib_names=set(),package_roots={'inert_package':pkg})
except FingerprintRefusal:passed.append('foreign submodule cannot borrow package version')
else:raise AssertionError('foreign submodule')
r=dict(status='PASS',blocking_count=0,scope='Runtime fingerprint primitives; inert files/modules only',tested=passed,untested=['Actual import resolution/version coverage','macOS runtime capture','Launch-time authentication','Capture producer entry'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),root/'runtime_fingerprints_cx1v002.py']])
p=case/'PACKAGE_TEST_REPORT.json'
with p.open('x') as out:json.dump(r,out,indent=2);out.write('\n')
print(p)
