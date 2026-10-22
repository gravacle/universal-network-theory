"""0847 distribution ownership from RECORD plus conventional bundled-library siblings.
D001 permits explicit regular files inside the interpreter prefix; no prefix traversal.
"""
from pathlib import Path
import re,csv,io,hashlib,os
from email.parser import BytesParser
from runtime_distribution_cx1v001 import need
from runtime_distribution_bytes_cx1v003 import capture_bytes,prefix_file

def capture_distribution(distribution,*,site_root,prefix_root,files=None):
 site=Path(site_root).resolve(strict=True);prefix=Path(prefix_root).resolve(strict=True)
 need(prefix in site.parents or prefix==site,'SITE_OUTSIDE_PREFIX')
 name=distribution.metadata.get('Name');version=distribution.version
 need(type(name) is str and bool(name) and type(version) is str and bool(version),'DISTRIBUTION_METADATA')
 canonical=re.sub(r'[-_.]+','-',name).lower()
 entries=distribution.files;need(entries is not None and bool(entries),'DISTRIBUTION_FILES_MISSING')
 records=[x for x in entries if Path(str(x)).name=='RECORD' and Path(str(x)).parent.name.endswith('.dist-info')]
 need(len(records)==1,'RECORD_UNIQUE')
 record_path=Path(distribution.locate_file(records[0]))
 metadata_path=record_path.parent/'METADATA'
 for p in (record_path,metadata_path):
  prefix_file(p,site)
 record_raw=record_path.read_bytes();metadata_raw=metadata_path.read_bytes()
 parsed=list(csv.reader(io.StringIO(record_raw.decode('utf-8'))))
 need(all(len(row)==3 for row in parsed),'RECORD_CSV')
 record_names=[row[0] for row in parsed]
 need(len(record_names)==len(set(record_names)) and sorted(record_names)==sorted(str(x) for x in entries),'RECORD_METADATA_LIST_CHANGED')
 message=BytesParser().parsebytes(metadata_raw)
 need(message.get_all('Name')==[name] and message.get_all('Version')==[version],'METADATA_VERSION_CHANGED')
 metadata_pins={p.resolve().relative_to(site).as_posix():hashlib.sha256(raw).hexdigest() for p,raw in [(record_path,record_raw),(metadata_path,metadata_raw)]}
 relative=[];roots=set();external=[]
 for entry in entries:
  declared=Path(str(entry));need(not declared.is_absolute(),'RECORD_ABSOLUTE_PATH')
  path=Path(os.path.abspath(os.path.normpath(str(site/declared))))
  if site in path.parents:
   path=prefix_file(path,site);rel=path.relative_to(site)
   relative.append(rel.as_posix());roots.add(site/rel.parts[0])
  else:
   path=prefix_file(path,prefix);external.append(path)
   relative.append('prefix:'+path.relative_to(prefix).as_posix())
 # Native wheels can carry bundled libraries omitted from RECORD. Include
 # conventional siblings explicitly; inner .dylibs are covered recursively.
 for stem in {canonical,canonical.replace('-','_')}:
  for suffix in ('.libs','.dylibs'):
   sibling=site/(stem+suffix)
   if sibling.exists():roots.add(sibling)
 evidence=capture_bytes(site_root=site,owned_roots=sorted(roots),record_relative_files=relative,prefix_root=prefix,explicit_prefix_files=external)
 need(not evidence['missing_RECORD_files'],'MISSING_RECORD_FILES')
 hashed={item['path']:item['sha256'] for item in evidence['files']}
 need(all(hashed.get(path)==sha for path,sha in metadata_pins.items()),'METADATA_CHANGED_DURING_CAPTURE')
 return dict(name=canonical,version=version,identity_basis=evidence['identity_basis'],sha256=evidence['sha256'],files=evidence['files'],owned_roots=[str(p.relative_to(site)) for p in sorted(roots)])
