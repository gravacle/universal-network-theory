"""0847 distribution ownership from RECORD plus conventional bundled-library siblings.
Outside-site RECORD paths refuse; shared namespace ownership is not supported.
"""
from pathlib import Path
import re
from runtime_distribution_cx1v001 import need
from runtime_distribution_bytes_cx1v002 import capture_bytes

def capture_distribution(distribution,*,site_root,files=None):
 site=Path(site_root).resolve(strict=True)
 name=distribution.metadata.get('Name');version=distribution.version
 need(type(name) is str and bool(name) and type(version) is str and bool(version),'DISTRIBUTION_METADATA')
 canonical=re.sub(r'[-_.]+','-',name).lower()
 entries=distribution.files;need(entries is not None and bool(entries),'DISTRIBUTION_FILES_MISSING')
 relative=[];roots=set()
 for entry in entries:
  declared=Path(str(entry));need(not declared.is_absolute() and '..' not in declared.parts,'RECORD_OUTSIDE_SITE')
  path=Path(distribution.locate_file(entry));need(not path.is_symlink(),'RECORD_SYMLINK')
  real=path.resolve(strict=True);need(site in real.parents,'RECORD_OUTSIDE_SITE')
  rel=real.relative_to(site);relative.append(rel.as_posix());roots.add(site/rel.parts[0])
 # Native wheels can carry bundled libraries omitted from RECORD. Include
 # conventional siblings explicitly; inner .dylibs are covered recursively.
 for stem in {canonical,canonical.replace('-','_')}:
  for suffix in ('.libs','.dylibs'):
   sibling=site/(stem+suffix)
   if sibling.exists():roots.add(sibling)
 evidence=capture_bytes(site_root=site,owned_roots=sorted(roots),record_relative_files=relative)
 need(not evidence['missing_RECORD_files'],'MISSING_RECORD_FILES')
 return dict(name=canonical,version=version,identity_basis=evidence['identity_basis'],sha256=evidence['sha256'],files=evidence['files'],owned_roots=[str(p.relative_to(site)) for p in sorted(roots)])
