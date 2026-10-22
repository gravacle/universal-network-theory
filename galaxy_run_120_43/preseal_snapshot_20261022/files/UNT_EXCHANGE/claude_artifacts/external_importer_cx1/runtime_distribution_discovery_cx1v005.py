"""Resolve top-level package distributions without importing package code.
Production caller supplies isolated sys.path, importlib.metadata and PathFinder.find_spec.
"""
from pathlib import Path
import re
from runtime_distribution_owned_bytes_cx1v003 import capture_distribution
from runtime_distribution_cx1v001 import need
from runtime_fingerprints_cx1v002 import FileFingerprints

def discover(*,import_roots,stdlib_names,search_path,metadata,find_spec,prefix_root):
 need(type(import_roots) is list and all(type(n) is str and n.isidentifier() for n in import_roots),'IMPORT_ROOTS')
 required=(set(import_roots)-set(stdlib_names))|{'numpy'}
 names=sorted(required|{'scipy'})
 scipy_presence=None
 mapping=metadata.packages_distributions();records={};bindings=[];files=FileFingerprints()
 for name in names:
  spec=find_spec(name,search_path)
  if name=='scipy':
   scipy_presence={'state':'NOT_INSTALLED' if spec is None else 'INSTALLED','find_spec_none':spec is None,'search_path':list(search_path)}
   if spec is None:
    need(name not in required,'REQUIRED_IMPORT_ABSENT:scipy')
    continue
  candidates=mapping.get(name,[])
  need(len(candidates)==1,'DISTRIBUTION_MAPPING_AMBIGUOUS:'+name)
  need(spec is not None and type(spec.origin) is str and spec.origin not in ('built-in','frozen'),'PACKAGE_ORIGIN_REQUIRED:'+name)
  origin=Path(spec.origin).resolve(strict=True)
  roots=[Path(p).resolve(strict=True) for p in search_path if p and Path(p).is_dir() and Path(p).resolve(strict=True) in origin.parents]
  need(bool(roots),'PACKAGE_OUTSIDE_SEARCH_PATH:'+name)
  root=max(roots,key=lambda p:len(p.parts))
  distribution=metadata.distribution(candidates[0])
  entries=distribution.files;need(entries is not None,'DISTRIBUTION_FILES_MISSING')
  need(any(Path(distribution.locate_file(x)).resolve()==origin for x in entries),'DISTRIBUTION_DOES_NOT_OWN_IMPORT:'+name)
  record=capture_distribution(distribution,site_root=root,prefix_root=prefix_root,files=files)
  canonical=re.sub(r'[-_.]+','-',candidates[0]).lower()
  need(canonical==record['name'],'DISTRIBUTION_NAME_MISMATCH')
  if canonical in records:need(records[canonical]==record,'DISTRIBUTION_IDENTITY_CONFLICT')
  records[canonical]=record
  bindings.append({'import':name,'distribution':canonical,'origin':str(origin)})
 return {'distributions':[records[k] for k in sorted(records)],'import_bindings':bindings,'scipy_presence':scipy_presence,'required_imports':sorted(required)}
