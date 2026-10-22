"""0847 deterministic distribution bytes digest over explicitly owned roots.
Caller must establish complete ownership, including sibling bundled-library roots.
"""
import hashlib,os,stat
from pathlib import Path
class BytesRefusal(ValueError):pass
def need(ok,why):
 if not ok:raise BytesRefusal(why)
def ident(s):return(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode)
def prefix_file(path,prefix):
 prefix=Path(prefix).resolve(strict=True)
 path=Path(os.path.abspath(os.path.normpath(str(path))))
 need(prefix in path.parents,'RECORD_OUTSIDE_PREFIX')
 current=prefix
 for part in path.relative_to(prefix).parts:
  current=current/part
  try:st=current.lstat()
  except FileNotFoundError:need(False,'PREFIX_FILE_MISSING')
  need(not stat.S_ISLNK(st.st_mode),'PREFIX_SYMLINK')
 need(stat.S_ISREG(st.st_mode),'PREFIX_NOT_REGULAR')
 return path

def capture_bytes(*,site_root,owned_roots,record_relative_files,prefix_root=None,explicit_prefix_files=()):
 site=Path(site_root).resolve(strict=True);need(site.is_dir(),'SITE_ROOT')
 extra={}
 if explicit_prefix_files:
  need(prefix_root is not None,'PREFIX_REQUIRED')
  prefix=Path(prefix_root).resolve(strict=True)
  for p in explicit_prefix_files:
   p=prefix_file(p,prefix);name='prefix:'+p.relative_to(prefix).as_posix()
   need(name not in extra,'DUPLICATE_PREFIX_FILE');extra[name]=p
 roots=[Path(p) for p in owned_roots];need(bool(roots),'OWNED_ROOTS_EMPTY')
 def inventory():
  found=set()
  for root in roots:
   need(not root.is_symlink(),'SYMLINK_ROOT')
   real=root.resolve(strict=True);need(site in real.parents,'ROOT_OUTSIDE_SITE')
   candidates=[real] if real.is_file() else real.rglob('*')
   for p in candidates:
    need(not p.is_symlink(),'SYMLINK_ENTRY')
    if p.is_dir():continue
    need(p.is_file(),'NONREGULAR_ENTRY');name=p.relative_to(site).as_posix();need(':' not in name,'SITE_NAMESPACE_COLLISION');found.add(name)
  for name,p in extra.items():prefix_file(p,prefix)
  return sorted(found|set(extra))
 names=inventory();need(bool(names),'EMPTY_DISTRIBUTION')
 expected=set(record_relative_files);all_entries=[];snapshots={};digest=hashlib.sha256(b'CX1_DISTRIBUTION_BYTES_V002\0')
 for name in names:
  path=extra[name] if name in extra else site/name;before=path.stat();cache=name not in extra and '__pycache__' in Path(name).parts
  fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
  try:
   st=os.fstat(fd);need(stat.S_ISREG(st.st_mode) and ident(st)==ident(before),'FILE_CHANGED')
   h=hashlib.sha256();encoded=name.encode('utf-8')
   if not cache:digest.update(len(encoded).to_bytes(8,'big')+encoded+st.st_size.to_bytes(8,'big'))
   while True:
    data=os.read(fd,1048576)
    if not data:break
    h.update(data)
    if not cache:digest.update(data)
   need(ident(st)==ident(os.fstat(fd))==ident(path.stat()),'FILE_CHANGED')
  finally:os.close(fd)
  snapshots[name]=ident(st)
  all_entries.append(dict(path=name,size=st.st_size,sha256=h.hexdigest(),excluded_from_equality=cache,outside_RECORD=name not in expected))
 need(inventory()==names,'INVENTORY_CHANGED')
 for e in all_entries:
  need(ident((extra[e['path']] if e['path'] in extra else site/e['path']).stat())==snapshots[e['path']],'FILE_CHANGED_AFTER_READ')
 return dict(identity_basis='sorted_relative_names_and_file_bytes_v002',sha256=digest.hexdigest(),files=all_entries,missing_RECORD_files=sorted(expected-set(names)))
