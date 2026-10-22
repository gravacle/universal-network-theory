import tempfile,json,hashlib
from pathlib import Path
from runtime_distribution_bytes_cx1v003 import capture_bytes,BytesRefusal
b=Path(__file__).resolve().parent;c=Path(tempfile.mkdtemp(prefix='prefix_bytes_',dir=b/'inert_fixtures'))
prefix=c/'prefix';site=prefix/'lib'/'site-packages';package=site/'numpy';package.mkdir(parents=True);(prefix/'bin').mkdir()
for p,raw in [(package/'x.py',b'INERT'),(prefix/'bin'/'f2py',b'INERT SCRIPT'),(prefix/'bin'/'UNLISTED',b'NOT TO BE READ')]:
 with p.open('xb') as f:f.write(raw)
args=dict(site_root=site,owned_roots=[package],record_relative_files=['numpy/x.py','prefix:bin/f2py'],prefix_root=prefix)
r=capture_bytes(**args,explicit_prefix_files=[site/'../../bin/f2py']);assert [x['path'] for x in r['files']]==['numpy/x.py','prefix:bin/f2py'];passed=['normpath resolves explicit prefix script; unlisted prefix file omitted']
without=capture_bytes(**{**args,'record_relative_files':['numpy/x.py']});assert without['sha256']!=r['sha256'];passed.append('prefix script participates in equality digest')
symlink=prefix/'bin'/'alias';symlink.symlink_to(prefix/'bin'/'f2py')
ancestor=prefix/'link';ancestor.symlink_to(prefix/'bin',target_is_directory=True)
for name,path in [('outside_prefix',c/'outside'),('missing',prefix/'missing'),('symlink_file',symlink),('symlink_ancestor',ancestor/'f2py'),('directory',prefix/'bin')]:
 try:capture_bytes(**args,explicit_prefix_files=[path])
 except (BytesRefusal,OSError):passed.append(name+' refuses')
 else:raise AssertionError(name)
report=dict(status='PASS',blocking_count=0,scope='D001 prefix boundaries with inert files only',tested=passed,untested=['RECORD ownership integration','Production installed package layout','Runtime record schema/CLI updated for bytes v002'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [b/'runtime_distribution_bytes_cx1v003.py',Path(__file__)]])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(c/'TEST_REPORT.json')
