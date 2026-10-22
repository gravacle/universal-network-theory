"""Prototype: snapshot IO for explicitly private chain modules during validation.
Not a production integration. The caller supplies only privately loaded modules;
never use on shared application or stdlib modules. Only explicitly audited private producer modules. This is an IO adapter, not a sandbox; direct os/io/numpy path access still needs a separate call-site audit.
"""
import io
import json
import threading
import types
from pathlib import Path
from snapshot_cx1v001 import Refusal, strict_json

class ExclusiveOutputScope:
    def __init__(self, snapshot, modules, output_roots):
        self.snapshot=snapshot
        self.output_roots=tuple(Path(p) for p in output_roots)
        if not self.output_roots or any(not p.is_absolute() or str(p.resolve())!=str(p) for p in self.output_roots):
            raise Refusal('OUTPUT_ROOT_CANONICAL')
        self.handles=[]
        self.modules=list(modules)
        self.saved=[]
        self.seen=set()

    def check_output(self,p):
        p=Path(p)
        if not p.is_absolute() or str(p.resolve())!=str(p) or not any(p==r or r in p.parents for r in self.output_roots):
            raise Refusal('OUTPUT_OUTSIDE_DECLARED_ROOTS')

    def enter_module(self,m):
        if id(m) in self.seen:return m
        if not isinstance(m,types.ModuleType) or not getattr(m,'__file__',None):
            raise Refusal('PRIVATE_MODULE_REQUIRED')
        # Explicit caller responsibility for isolation; never adapt stdlib.
        if '/claude_artifacts/' not in str(Path(m.__file__).resolve()):
            raise Refusal('NON_ARTIFACT_MODULE')
        self.seen.add(id(m))
        snap=self.snapshot
        def read_open(file,mode='r',buffering=-1,encoding=None,errors=None,newline=None,closefd=True,opener=None):
            if opener is not None or not closefd or isinstance(file,int):
                raise Refusal('PRODUCER_IO_OPTIONS')
            if mode in ('x','xt','xb'):
                p=Path(file)
                self.check_output(p)
                handle=p.open(mode,buffering=buffering,encoding=encoding,errors=errors,newline=newline)
                self.handles.append((str(p),handle))
                return handle
            if any(name==str(file) and not handle.closed for name,handle in self.handles):
                raise Refusal('READ_BEFORE_OUTPUT_CLOSED')
            if mode not in ('r','rt','rb') or opener is not None or not closefd or isinstance(file,int):
                raise Refusal('VALIDATION_IO_NOT_READ_ONLY')
            raw=snap.read(file)
            if 'b' in mode:return io.BytesIO(raw)
            return io.StringIO(raw.decode(encoding or 'utf-8',errors or 'strict'),newline=newline)
        scope=self
        class SnapshotPath(type(Path())):
            def mkdir(self,mode=0o777,parents=False,exist_ok=False):
                scope.check_output(self)
                # Do not create ancestors outside declared roots.
                p=Path(str(self))
                missing=p
                while not missing.parent.exists():
                    missing=missing.parent;scope.check_output(missing)
                return p.mkdir(mode=mode,parents=parents,exist_ok=exist_ok)

            def read_bytes(self):return read_open(str(self),'rb').read()
            def read_text(self,encoding=None,errors=None):
                return read_open(str(self),'r',encoding=encoding,errors=errors).read()
            def open(self,mode='r',buffering=-1,encoding=None,errors=None,newline=None):
                return read_open(str(self),mode,buffering,encoding,errors,newline)
        def loads(value,*a,**kw):
            if a or kw:raise Refusal('JSON_CUSTOM_PARSE_UNSUPPORTED')
            return strict_json(value.encode('utf-8') if isinstance(value,str) else value)
        shim=types.SimpleNamespace(**{k:getattr(json,k) for k in dir(json) if not k.startswith('__')})
        shim.loads=loads
        shim.load=lambda f,*a,**kw:loads(f.read(),*a,**kw)
        replacements={'open':read_open}
        if 'Path' in m.__dict__:replacements['Path']=SnapshotPath
        if m.__dict__.get('json') is json:replacements['json']=shim
        loader=m.__dict__.get('load_pinned_module')
        if loader is not None:
            def load_and_adapt(*a,**kw):return self.enter_module(loader(*a,**kw))
            replacements['load_pinned_module']=load_and_adapt
        for key,value in replacements.items():
            self.saved.append((m,key,key in m.__dict__,m.__dict__.get(key)))
            m.__dict__[key]=value
        return m

    def __enter__(self):
        if threading.active_count()!=1:raise Refusal('VALIDATION_REQUIRES_ISOLATED_SINGLE_THREAD')
        try:
            for m in self.modules:self.enter_module(m)
        except BaseException:
            self.__exit__(None,None,None)
            raise
        return self

    def __exit__(self,*exc):
        for m,key,present,value in reversed(self.saved):
            if present:m.__dict__[key]=value
            else:m.__dict__.pop(key,None)
        self.saved.clear()
        self.seen.clear()
