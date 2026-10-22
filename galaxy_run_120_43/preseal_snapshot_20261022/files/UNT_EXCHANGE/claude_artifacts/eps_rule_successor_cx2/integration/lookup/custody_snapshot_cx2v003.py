"""D006/D013: exact internal custody dependency seam; public APIs stay strict.

No public whitelist parameter exists. Production authority is extracted from
reviewed custody/driver source bytes, never by importing those modules. Only
legacy file reads within custody_reads() can use the one reviewed runs pin.
Request raw/read/doc/pin/module and output validation remain the frozen policy.
"""
import ast
import builtins
import contextlib
import hashlib
import importlib.machinery
import io
import os
from pathlib import Path, PurePosixPath
import stat
import types

ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
BASE={'path':str(ART/'direct_cert_lookup_cx3/direct_cert_lookup_cx3v001.py'),'sha256':'1cb5039ef380f7472191f40d1293f45b98cbc4e301efb06d9ea9ccc5b59de7e5'}
CUSTODY={'path':str(ART/'calib_tail_readiness_cx2/certificates_per_point/custody_cx2v002.py'),'sha256':'6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377'}
DRIVER={'path':str(ART/'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py'),'sha256':'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'}
AUTHORITY={'path':str(ART/'eps_rule_successor_cx2/integration/custody_replay_fix/AUTHORITY_D006_D013_CX2V001.json'),'sha256':'01bf12fb17fbaa4206dc8a32d0ed1a3753e5704ea60fe3bcf923392827644a3b'}


def need(ok,reason):
    if not ok:raise ValueError('CUSTODY_SNAPSHOT_'+reason)


def _base():
    # Seed the new transaction with exactly the authenticated bootstrap bytes.
    # The secure reader validates inode/stability and never follows a runs alias.
    seed=types.SimpleNamespace(cache={},inodes={},counts={})
    path=_canonical_internal(BASE['path'],_allow_runs=False)
    raw=_ScopedMixin._physical_internal(seed,path,BASE['sha256'])
    m=types.ModuleType('_custody_frozen_snapshot');m.__file__=BASE['path']
    exec(compile(raw,BASE['path'],'exec'),m.__dict__)
    return m,seed


def _literal(node,values):
    """Only Path literals, already known names, and / joins; no eval/import."""
    if isinstance(node,ast.Constant):return node.value
    if isinstance(node,ast.Name):return values[node.id]
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='Path' and len(node.args)==1 and not node.keywords:
        return PurePosixPath(_literal(node.args[0],values))
    if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Div):return PurePosixPath(_literal(node.left,values))/_literal(node.right,values)
    if isinstance(node,(ast.Tuple,ast.List)):return tuple(_literal(n,values) for n in node.elts)
    raise ValueError('CUSTODY_SNAPSHOT_NONLITERAL_PIN_SOURCE')


def _custody_pins(s):
    """Production-only source authority. Tests may replace this private function in RAM."""
    s.read(AUTHORITY)
    custody=ast.parse(s.read(CUSTODY));driver=ast.parse(s.read(DRIVER))
    def assignments(tree):
        return {t.id:n.value for n in tree.body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
    ca,da=assignments(custody),assignments(driver)
    cv={'ART':PurePosixPath(str(ART))}
    need(str(_literal(ca['DRIVER'],cv))==DRIVER['path'] and _literal(ca['DRIVER_SHA'],cv)==DRIVER['sha256'],'CUSTODY_DRIVER_BINDING')
    root=_literal(da['ROOT'],{})
    table=da['UVT_MONITOR_PINS']
    need(isinstance(table,ast.Dict),'DRIVER_MONITOR_TABLE')
    nodes=[v for k,v in zip(table.keys,table.values) if isinstance(k,ast.Constant) and k.value=='a2f10_result']
    need(len(nodes)==1,'EXACT_INTERNAL_ROLE')
    path,sha=_literal(nodes[0],{'ROOT':root})
    need(isinstance(sha,str) and len(sha)==64 and all(c in '0123456789abcdef' for c in sha),'SOURCE_SHA')
    need(PurePosixPath(path).parts[-4:]==('CLAUDE2','runs','A2_ANCHOR_F10_RUN_V001','result.json'),'SOURCE_ROLE_PATH')
    return {str(path):sha}


def _hard_path(value):
    need(isinstance(value,str) and os.path.isabs(value) and os.path.normpath(value)==value,'ABSOLUTE_NORMALIZED_PATH')
    p=Path(value)
    bad={'.codex','runs_ext','unt_internal_runs','v007_postseal_records','kmax_a2f10_c5h_run_v001'}
    need(not any(x.casefold() in bad or 'ngc3198' in x.casefold() or x.casefold().startswith('uvt_') for x in p.parts),'HARD_PROTECTED_PATH')
    return p


def _canonical_internal(value,*,_allow_runs=True):
    """Validate each symlink target before any traversal into that target."""
    def policy(path):
        p=_hard_path(path)
        need(_allow_runs or not any(x.casefold()=='runs' for x in p.parts),'BOOTSTRAP_RUNS_ALIAS')
        return p
    p=policy(value);todo=list(p.parts[1:]);current=Path('/');links=0
    while todo:
        part=todo.pop(0)
        candidate=policy(str(current/part))
        mode=os.lstat(candidate).st_mode
        if stat.S_ISLNK(mode):
            links+=1;need(links<=40,'SYMLINK_LOOP')
            target=os.readlink(candidate)
            target=target if os.path.isabs(target) else str(current/target)
            target=os.path.normpath(target);policy(target)
            current=Path('/');todo=list(Path(target).parts[1:])+todo
        else:current=candidate
    return policy(str(current))


class _ScopedMixin:
    def _physical_internal(self,path,expected):
        name=str(path)
        if name not in self.cache:
            st=path.stat();need(stat.S_ISREG(st.st_mode) and st.st_size<=64*1024*1024,'REGULAR_BOUNDED_INPUT')
            inode=(st.st_dev,st.st_ino)
            if inode in self.inodes:self.cache[name]=self.inodes[inode]
            else:
                fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
                try:
                    first=os.fstat(fd);need((first.st_dev,first.st_ino)==inode,'INPUT_IDENTITY_CHANGED')
                    chunks=[];size=0
                    while True:
                        b=os.read(fd,1024*1024)
                        if not b:break
                        size+=len(b);need(size<=64*1024*1024,'INPUT_SIZE_LIMIT');chunks.append(b)
                    raw=b''.join(chunks);end=os.fstat(fd)
                    need((first.st_size,first.st_mtime_ns,first.st_ctime_ns)==(end.st_size,end.st_mtime_ns,end.st_ctime_ns) and len(raw)==end.st_size,'INPUT_CHANGED_DURING_READ')
                finally:os.close(fd)
                self.cache[name]=self.inodes[inode]=raw;self.counts[name]=1
        raw=self.cache[name]
        need(hashlib.sha256(raw).hexdigest()==expected,'EXACT_INTERNAL_SHA_MISMATCH')
        return raw

    def _legacy_raw(self,path,pins):
        path=os.fsdecode(path)
        if pins is None:return self.raw(path)
        # Fixed R1 source is governed by the frozen public exception, not D006.
        if path==self._frozen.R1:return self.raw(path)
        _hard_path(path)
        if path in pins:return self._physical_internal(_canonical_internal(path),pins[path])
        # Only a canonical spelling derived from an exact registered path can
        # inherit that pin. Arbitrary symlink aliases and same-inode names cannot.
        if any(x.casefold()=='runs' for x in Path(path).parts):
            for registered,sha in pins.items():
                canonical=_canonical_internal(registered)
                if path==str(canonical):return self._physical_internal(canonical,sha)
        return self.raw(path)

    @contextlib.contextmanager
    def _intercept(self,pins):
        oldopen,oldio=builtins.open,io.open
        olddata=importlib.machinery.SourceFileLoader.get_data
        def selected(path):
            if not isinstance(path,(str,bytes,os.PathLike)):return False
            value=os.fsdecode(path)
            parts=Path(value).parts
            protected=any(x.casefold() in {'runs','runs_ext','unt_internal_runs','.codex','v007_postseal_records','kmax_a2f10_c5h_run_v001'} or 'ngc3198' in x.casefold() or x.casefold().startswith('uvt_') for x in parts)
            return value.startswith(('/Users/bgm/Research/','/Volumes/External1/')) or value in (pins or {}) or protected
        def fallback_path_check(path):
            # Outside the snapshotted project roots, preserve normal I/O only
            # after the strict symlink walk. A clean alias outside Research
            # must not become a back door to a protected target.
            if isinstance(path,(str,bytes,os.PathLike)):
                self._frozen.safe_path(os.path.abspath(os.fsdecode(path)))
        def opening(file,mode='r',buffering=-1,encoding=None,errors=None,newline=None,closefd=True,opener=None):
            if not selected(file):
                fallback_path_check(file)
                return oldopen(file,mode,buffering,encoding,errors,newline,closefd,opener)
            need(mode in ('r','rt','rb') and opener is None,'REPLAY_READ_ONLY')
            raw=self._legacy_raw(file,pins)
            if 'b' in mode:return io.BytesIO(raw)
            return io.TextIOWrapper(io.BytesIO(raw),encoding=encoding or 'utf-8',errors=errors,newline=newline)
        def source_data(loader,path):
            if selected(path):
                if str(path).endswith('.pyc'):raise FileNotFoundError(path)
                return self._legacy_raw(path,pins)
            fallback_path_check(path)
            return olddata(loader,path)
        self.depth+=1;builtins.open=io.open=opening
        importlib.machinery.SourceFileLoader.get_data=source_data
        try:yield
        finally:
            builtins.open,io.open=oldopen,oldio
            importlib.machinery.SourceFileLoader.get_data=olddata;self.depth-=1

    @contextlib.contextmanager
    def reads(self):
        # Even nested inside custody_reads, an explicit strict context suspends
        # the exception. A second Snapshot never inherits the first's authority.
        with self._intercept(None):yield

    @contextlib.contextmanager
    def custody_reads(self):
        pins=_custody_pins(self)
        need(isinstance(pins,dict) and bool(pins),'INTERNAL_PIN_MAP')
        for path,sha in pins.items():
            _hard_path(path)
            need(isinstance(sha,str) and len(sha)==64 and all(c in '0123456789abcdef' for c in sha),'INTERNAL_PIN_SHA')
        with self._intercept(dict(pins)):yield


def snapshot():
    base,seed=_base()
    cls=type('ScopedCustodySnapshot',(_ScopedMixin,base.Snapshot),{})
    result=cls();result._frozen=base
    result.cache.update(seed.cache);result.inodes.update(seed.inodes);result.counts.update(seed.counts)
    return result
