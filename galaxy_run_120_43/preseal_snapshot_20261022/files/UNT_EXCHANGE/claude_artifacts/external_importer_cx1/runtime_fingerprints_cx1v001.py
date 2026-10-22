"""Runtime fingerprint primitives. No module import or driver execution; caller supplies resolved modules."""
import hashlib,os,stat
from pathlib import Path
class FingerprintRefusal(ValueError):pass

def need(ok,why):
 if not ok:raise FingerprintRefusal(why)

def identity(st):return (st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns,st.st_mode,st.st_nlink)

class FileFingerprints:
 def __init__(self):self.by_inode={};self.content_reads=0
 def capture(self,path):
  real=str(Path(path).resolve(strict=True));before=os.stat(real,follow_symlinks=False)
  need(stat.S_ISREG(before.st_mode),'RUNTIME_NOT_REGULAR')
  key=(before.st_dev,before.st_ino)
  if key in self.by_inode:
   old,digest=self.by_inode[key];need(old==identity(before),'RUNTIME_CHANGED_AFTER_READ')
   return {'realpath':real,'sha256':digest}
  fd=os.open(real,os.O_RDONLY|os.O_NOFOLLOW)
  try:
   st=os.fstat(fd);need(identity(st)==identity(before),'RUNTIME_CHANGED_BEFORE_READ')
   h=hashlib.sha256()
   while True:
    chunk=os.read(fd,1024*1024)
    if not chunk:break
    h.update(chunk)
   after=os.fstat(fd);now=os.stat(real,follow_symlinks=False)
   need(identity(st)==identity(after)==identity(now),'RUNTIME_CHANGED_DURING_READ')
   self.content_reads+=1;self.by_inode[key]=(identity(after),h.hexdigest())
   return {'realpath':real,'sha256':h.hexdigest()}
  finally:os.close(fd)

def module_fingerprint(module, *, files, interpreter, sys_version, stdlib_names):
 name=getattr(module,'__name__',None);need(type(name) is str and bool(name),'RUNTIME_MODULE_NAME')
 spec=getattr(module,'__spec__',None);origin=getattr(spec,'origin',None)
 version=getattr(module,'__version__',None)
 if version is None and name.split('.')[0] in stdlib_names:version=sys_version;version_source='interpreter_version'
 else:version_source='module___version__'
 need(type(version) is str and bool(version),'RUNTIME_MODULE_VERSION_UNRESOLVED:'+name)
 if origin in ('built-in','frozen'):
  return {'name':name,'version':version,'version_source':version_source,'kind':origin,
          'realpath':interpreter['realpath'],'sha256':interpreter['sha256'],'identity_basis':'interpreter_binary'}
 path=getattr(module,'__file__',None);need(type(path) is str and bool(path),'RUNTIME_MODULE_FILE_UNRESOLVED:'+name)
 pin=files.capture(path)
 return dict(name=name,version=version,version_source=version_source,kind='file',identity_basis='module_file',**pin)
