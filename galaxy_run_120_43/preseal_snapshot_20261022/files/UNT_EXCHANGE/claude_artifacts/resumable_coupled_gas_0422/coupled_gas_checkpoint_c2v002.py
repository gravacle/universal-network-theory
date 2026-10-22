"""INERT exact restart records for coupled_hi_fourier_source_iteration_v005_resume_c2v001.
Claude2 0422 c2v002. Restart only at a COMPLETED HI-column boundary of the current
source iteration. No physics, defaults, tolerances, repair, retry or fallback here.
c2v002 changes only resume memory: column records of every iteration except the
resume iteration are validated and dropped (count kept); the resume iteration's
records are decoded one at a time as validated. Record format is unchanged.

Layout below one checkpoint directory (append-only; nothing replaced or deleted):
  IDENTITY.json                     exact code/input/control/environment identity
  checkpoint.lock                   advisory flock held by the single live writer
  blobs/<sha256>.npy                content-addressed arrays, allow_pickle=False
  attempts/<token>.start.json       one per solve call; .end.json on a returned outcome
  iteration_NNNN/START.json         commit marker written BEFORE any column: actual
                                    iteration, gas iterate (stored, never derived),
                                    fixed/current source, prepared waves, digest of
                                    the full prepared response, prior history
  iteration_NNNN/column_NNNNN.json  one COMPLETE HI column solution (incl. source
                                    quadrature) per completed column, roster order
  iteration_NNNN/COMPLETED.json     updated gas, residual, bound, history entry
  iteration_NNNN/FAILURE.<token>.json  actual returned column failure
Each JSON record carries payload_sha256 of its canonical payload and is published
as fsynced temp + hard link (never replaces), after which only the temp ALIAS of
that same inode is unlinked. Values are encoded exactly: float.hex, list/tuple
and dict order kept, numpy dtype+shape+bytes. Object aliasing is not retained.
Interrupted temps, attempts without an end record, failure records and uncommitted
iteration directories are reported and preserved. Any doubt raises CheckpointError,
a RuntimeError, so it can never be caught as a physical HI-column ValueError.
"""
import fcntl
import hashlib
import io
import json
import os
import platform
import re
import struct
import sys
import time
import types
import numpy as np

FORMAT='UNT_0422_COUPLED_GAS_CHECKPOINT_C2V001'
_HEX64=re.compile('[0-9a-f]{64}')
_TOKEN=r'\d{20}-\d+-[0-9a-f]{8}'


class CheckpointError(RuntimeError):
    """Checkpoint/identity/integrity failure; deliberately not a ValueError."""


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _file_pin(path):
    path=os.path.abspath(path)
    try:
        with open(path,'rb') as f: data=f.read()
    except OSError:
        raise CheckpointError('CODE_PIN_UNREADABLE '+path) from None
    return {'path':path,'sha256':_sha(data)}


def _module_pin(m,name):
    path=getattr(m,'__file__',None)
    if not isinstance(path,str) or not os.path.isfile(path):
        raise CheckpointError('MODULE_CODE_PIN_UNAVAILABLE '+name)
    return _file_pin(path)


def _feed(h,v):
    t=type(v)
    if v is None: h.update(b'N')
    elif t is bool: h.update(b'T' if v else b'F')
    elif t is int:
        s=str(v).encode(); h.update(b'I'+struct.pack('<Q',len(s))+s)
    elif t is float: h.update(b'D'+struct.pack('<d',v))
    elif t is complex: h.update(b'C'+struct.pack('<dd',v.real,v.imag))
    elif t is str:
        s=v.encode('utf-8'); h.update(b'S'+struct.pack('<Q',len(s))+s)
    elif t is np.ndarray or isinstance(v,np.generic):
        a=np.asarray(v)
        if a.dtype.kind not in 'biufc': raise CheckpointError('UNSUPPORTED_ARRAY_DTYPE '+a.dtype.str)
        d=a.dtype.str.encode()
        h.update((b'A' if t is np.ndarray else b'G')+struct.pack('<Q',len(d))+d
                 +struct.pack('<Q',a.ndim)+struct.pack('<%dQ'%a.ndim,*a.shape))
        h.update(np.ascontiguousarray(a).tobytes())
    elif t is list or t is tuple:
        h.update((b'L' if t is list else b'U')+struct.pack('<Q',len(v)))
        for x in v: _feed(h,x)
    elif t is dict:
        if any(type(k) is not str for k in v): raise CheckpointError('NON_STRING_KEY')
        h.update(b'M'+struct.pack('<Q',len(v)))
        for k in sorted(v):
            _feed(h,k); _feed(h,v[k])
    elif isinstance(v,types.ModuleType):
        pin=_module_pin(v,str(getattr(v,'__name__','module')))
        h.update(b'P'); _feed(h,pin['path']); _feed(h,pin['sha256'])
    else: raise CheckpointError('UNSUPPORTED_IDENTITY_TYPE '+t.__name__)


def digest(value):
    """Exact type-tagged sha256: float bits, dtype/shape/bytes, list vs tuple."""
    h=hashlib.sha256(); _feed(h,value)
    return h.hexdigest()


def encode(v):
    t=type(v)
    if v is None: return ['n']
    if t is bool: return ['b',v]
    if t is int: return ['i',str(v)]
    if t is float: return ['f',v.hex()]
    if t is complex: return ['c',v.real.hex(),v.imag.hex()]
    if t is str: return ['s',v]
    if t is list: return ['l',[encode(x) for x in v]]
    if t is tuple: return ['t',[encode(x) for x in v]]
    if t is dict:
        if any(type(k) is not str for k in v): raise CheckpointError('RECORD_NON_STRING_KEY')
        return ['d',[[k,encode(x)] for k,x in v.items()]]
    if t is np.ndarray or isinstance(v,np.generic):
        a=np.asarray(v)
        if a.dtype.kind not in 'biufc': raise CheckpointError('UNSUPPORTED_RECORD_DTYPE '+a.dtype.str)
        return ['a' if t is np.ndarray else 'g',a.dtype.str,list(a.shape),
                np.ascontiguousarray(a).tobytes().hex()]
    raise CheckpointError('UNSUPPORTED_RECORD_TYPE '+t.__name__)


def _decode(e):
    tag=e[0]
    if tag=='n' and len(e)==1: return None
    if len(e)==2:
        x=e[1]
        if tag=='b' and type(x) is bool: return x
        if tag=='i' and type(x) is str and re.fullmatch('-?[0-9]+',x): return int(x)
        if tag=='f' and type(x) is str: return float.fromhex(x)
        if tag=='s' and type(x) is str: return x
        if tag=='l' and type(x) is list: return [_decode(y) for y in x]
        if tag=='t' and type(x) is list: return tuple(_decode(y) for y in x)
        if tag=='d' and type(x) is list:
            out={}
            for k,y in x:
                if type(k) is not str or k in out: raise CheckpointError('MALFORMED_RECORD_DICT')
                out[k]=_decode(y)
            return out
    if tag=='c' and len(e)==3: return complex(float.fromhex(e[1]),float.fromhex(e[2]))
    if tag in ('a','g') and len(e)==4 and type(e[2]) is list:
        dtype=np.dtype(e[1])
        if dtype.kind not in 'biufc': raise CheckpointError('UNSUPPORTED_RECORD_DTYPE')
        a=np.frombuffer(bytes.fromhex(e[3]),dtype=dtype).reshape(tuple(e[2])).copy()
        return a if tag=='a' else a[()]
    raise CheckpointError('MALFORMED_RECORD_ENCODING')


def decode(e):
    try: return _decode(e)
    except CheckpointError: raise
    except (TypeError,ValueError,IndexError,KeyError,OverflowError) as exc:
        raise CheckpointError('MALFORMED_RECORD_ENCODING '+type(exc).__name__) from None


def _canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=True,
                      allow_nan=False).encode('ascii')


def _exact(value,what):
    """Encode, then prove the JSON text decodes to an identical typed digest."""
    e=encode(value)
    if digest(decode(json.loads(_canonical(e))))!=digest(value):
        raise CheckpointError('RECORD_ROUNDTRIP_NOT_EXACT '+what)
    return e


def _fsync_dir(path):
    fd=os.open(path,os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)


def _publish(final,data,token):
    """fsynced temp + hard link: atomic, and never replaces an existing file."""
    folder,name=os.path.split(final)
    tmp=os.path.join(folder,'.'+name+'.'+token+'.tmp')
    with open(tmp,'xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    try: os.link(tmp,final)
    except FileExistsError:
        raise CheckpointError('RECORD_EXISTS; nothing replaced; temp kept: '+tmp) from None
    if not os.path.samefile(tmp,final): raise CheckpointError('PUBLICATION_LINK_MISMATCH '+final)
    os.unlink(tmp)  # only the temporary alias of the file just published
    _fsync_dir(folder)


def _write(final,payload,token):
    body=dict(payload,format=FORMAT)
    body['payload_sha256']=_sha(_canonical(body))
    _publish(final,_canonical(body)+b'\n',token)
    return body['payload_sha256']


def _read(path,kind):
    try:
        with open(path,'rb') as f: raw=f.read()
        body=json.loads(raw.decode('ascii'))
    except (OSError,UnicodeDecodeError,ValueError) as exc:
        raise CheckpointError('UNREADABLE_RECORD '+type(exc).__name__+' '+path) from None
    if type(body) is not dict or body.get('format')!=FORMAT or body.get('kind')!=kind:
        raise CheckpointError('WRONG_RECORD_KIND '+path)
    claimed=body.pop('payload_sha256',None)
    if claimed!=_sha(_canonical(body)): raise CheckpointError('RECORD_INTEGRITY_FAILURE '+path)
    body['payload_sha256']=claimed
    if raw!=_canonical(body)+b'\n': raise CheckpointError('NONCANONICAL_RECORD '+path)
    return body


def _put(ck,array):
    a=np.asarray(array)
    if a.dtype.kind not in 'biufc': raise CheckpointError('UNSUPPORTED_BLOB_DTYPE '+a.dtype.str)
    buf=io.BytesIO(); np.save(buf,a,allow_pickle=False); data=buf.getvalue()
    name=_sha(data)+'.npy'; final=os.path.join(ck['directory'],'blobs',name)
    if os.path.exists(final):
        with open(final,'rb') as f:
            if f.read()!=data: raise CheckpointError('BLOB_CONTENT_MISMATCH '+final)
    else: _publish(final,data,ck['token'])
    return {'blob':'blobs/'+name,'file_sha256':name[:-4],'array_sha256':digest(a),
            'dtype':a.dtype.str,'shape':list(a.shape)}


def _get(directory,ref):
    try:
        blob=ref['blob']; fsha=ref['file_sha256']; dtype=ref['dtype']; shape=ref['shape']; asha=ref['array_sha256']
    except (KeyError,TypeError):
        raise CheckpointError('MALFORMED_BLOB_REFERENCE') from None
    if type(blob) is not str or type(fsha) is not str or blob!='blobs/'+fsha+'.npy' or not _HEX64.fullmatch(fsha):
        raise CheckpointError('MALFORMED_BLOB_REFERENCE')
    path=os.path.join(directory,blob)
    try:
        with open(path,'rb') as f: data=f.read()
    except OSError:
        raise CheckpointError('BLOB_MISSING '+path) from None
    if _sha(data)!=fsha: raise CheckpointError('BLOB_INTEGRITY_FAILURE '+path)
    a=np.load(io.BytesIO(data),allow_pickle=False)
    if a.dtype.str!=dtype or list(a.shape)!=shape or digest(a)!=asha:
        raise CheckpointError('BLOB_ARRAY_MISMATCH '+path)
    return a


def _lock(directory,create):
    path=os.path.join(directory,'checkpoint.lock')
    try: f=open(path,'xb' if create else 'rb')
    except OSError:
        raise CheckpointError('CHECKPOINT_LOCK_FILE_UNAVAILABLE '+path) from None
    try: fcntl.flock(f.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
    except OSError:
        f.close(); raise CheckpointError('CHECKPOINT_IN_USE by another live writer '+directory) from None
    return f


def _identity(*,solver_file,inputs,caller,fixed):
    if type(caller) is not dict: raise CheckpointError('CALLER_IDENTITY_DICT_REQUIRED')
    for key in ('code_pins','boundary_prescription','physical_parameters','numerical_controls'):
        if key not in caller: raise CheckpointError('CALLER_IDENTITY_FIELD_REQUIRED '+key)
    if not isinstance(caller['boundary_prescription'],str) or not caller['boundary_prescription'].strip():
        raise CheckpointError('EXPLICIT_BOUNDARY_PRESCRIPTION_REQUIRED')
    pins=caller['code_pins']
    if type(pins) is not dict or not pins or any(type(k) is not str or type(v) is not str
            or not _HEX64.fullmatch(v) for k,v in pins.items()):
        raise CheckpointError('CALLER_CODE_PINS_REQUIRED path->64-hex sha256')
    modules={name:_module_pin(inputs[name],name) for name in ('source_module','fourier_module',
             'metric_module','hi_module','quadrature_module')}
    vm=inputs['vertical_fourier_module']
    modules['vertical_fourier_module']=None if vm is None else _module_pin(vm,'vertical_fourier_module')
    fa=inputs['fourier_arguments']
    if type(fa) is not dict: raise CheckpointError('FOURIER_ARGUMENTS_DICT_REQUIRED')
    for name,value in fa.items():
        if isinstance(value,types.ModuleType): modules['fourier_arguments.'+name]=_module_pin(value,name)
    code={'solver':_file_pin(solver_file),'checkpoint':_file_pin(__file__),'modules':modules}
    for pin in [code['solver'],code['checkpoint']]+[p for p in modules.values() if p is not None]:
        if pin['path'] in pins and pins[pin['path']]!=pin['sha256']:
            raise CheckpointError('CODE_CHANGED_SINCE_CALLER_PIN '+pin['path'])
    gas=inputs['initial_gas_fourier_J']; roster=inputs['gas_columns']
    identity={'format':FORMAT,'code':code,
        'environment':{'python':sys.version,'numpy':np.__version__,'platform':sys.platform,
                       'machine':platform.machine(),'byteorder':sys.byteorder},
        'inputs_sha256':{'fixed_positions_m':digest(inputs['fixed_positions_m']),
            'fixed_integrated_columns_J':digest(inputs['fixed_integrated_columns_J']),
            'initial_gas_fourier_J':digest(gas),'fixed_source_fourier_J':digest(fixed),
            'gas_columns':digest(roster),
            'fourier_arguments':{k:digest(v) for k,v in sorted(fa.items())}},
        'shapes':{'gas_column_count':len(roster),'source_fourier':list(np.shape(gas))},
        'controls':{k:encode(v) for k,v in sorted(inputs['controls'].items())},
        'caller':{'sha256':digest(caller),'record':encode(caller)}}
    return json.loads(_canonical(identity))


def _differences(a,b,path='identity'):
    if type(a) is dict and type(b) is dict:
        out=[]
        for k in sorted(set(a)|set(b)):
            out+=([path+'.'+k] if k not in a or k not in b else _differences(a[k],b[k],path+'.'+k))
        return out
    return [] if a==b else [path]


def _scan(directory,ck):
    """Read-only structure/integrity scan. Returns committed records and a report.
    Every column record is read and validated. Only the resume iteration (highest
    START.json present) keeps its column results, each decoded as it is validated;
    any other iteration keeps only its count. Resume memory is one iteration."""
    report={'interrupted_temporary_files':[],'attempts_without_end':[],'failure_records':[],
            'uncommitted_iteration_directories':[],'ignored_system_files':[]}
    problems=[]
    def read(path,kind):
        try: return _read(path,kind)
        except CheckpointError as exc:
            problems.append(str(exc)); return None
    def skip(name,path):
        if name=='.DS_Store': report['ignored_system_files'].append(path); return True
        if name.startswith('.') and name.endswith('.tmp'):
            report['interrupted_temporary_files'].append(path); return True
        return False
    def listing(path):
        if not os.path.isdir(path): problems.append('MISSING_DIRECTORY '+path); return []
        return sorted(os.listdir(path))
    def field(rec,key):
        return rec.get(key) if type(rec) is dict else None
    sid=ck['identity_sha256']; n=ck['column_count']
    iterations={}
    for name in listing(directory):
        path=os.path.join(directory,name)
        m=re.fullmatch(r'iteration_(\d{4})',name)
        if name in ('IDENTITY.json','checkpoint.lock','blobs','attempts') or skip(name,path): continue
        if m and os.path.isdir(path): iterations[int(m.group(1))]=path
        else: problems.append('UNEXPECTED_ENTRY '+path)
    for name in listing(os.path.join(directory,'blobs')):
        path=os.path.join(directory,'blobs',name)
        if not skip(name,path) and not re.fullmatch('[0-9a-f]{64}[.]npy',name):
            problems.append('UNEXPECTED_ENTRY '+path)
    starts=set(); ends=set()
    for name in listing(os.path.join(directory,'attempts')):
        path=os.path.join(directory,'attempts',name)
        m=re.fullmatch('('+_TOKEN+r')[.](start|end)[.]json',name)
        if skip(name,path): continue
        if not m: problems.append('UNEXPECTED_ENTRY '+path); continue
        if read(path,'attempt_'+m.group(2)) is not None:
            (starts if m.group(2)=='start' else ends).add(m.group(1))
    report['attempts_without_end']=sorted(starts-ends)
    # Resume iteration: highest directory holding START.json. If that START is not
    # valid, or any iteration below it is not committed, the scan rejects below.
    top=max([i for i,p in iterations.items() if os.path.exists(os.path.join(p,'START.json'))],default=None)
    chain=[]
    for i in sorted(iterations):
        path=iterations[i]; start=None; completed=None; cols={}
        for name in listing(path):
            p=os.path.join(path,name); m=re.fullmatch(r'column_(\d{5})[.]json',name)
            if skip(name,p): continue
            if name=='START.json': start=read(p,'iteration_start')
            elif name=='COMPLETED.json': completed=read(p,'iteration_completed')
            elif m: cols[int(m.group(1))]=p
            elif re.fullmatch('FAILURE[.]'+_TOKEN+'[.]json',name):
                if read(p,'failure') is not None: report['failure_records'].append(p)
            else: problems.append('UNEXPECTED_ENTRY '+p)
        if start is None:
            if cols or os.path.exists(os.path.join(path,'START.json')) or os.path.exists(os.path.join(path,'COMPLETED.json')):
                problems.append('RECORDS_WITHOUT_VALID_START '+path)
            else: report['uncommitted_iteration_directories'].append(path)
            continue
        if field(start,'iteration')!=i or field(start,'identity_sha256')!=sid or field(start,'column_count')!=n:
            problems.append('START_MISMATCH '+path)
        if sorted(cols)!=list(range(len(cols))) or len(cols)>n:
            problems.append('NONCONTIGUOUS_COLUMN_RECORDS '+path)
        records=0; restored=[] if i==top else None
        for k in sorted(cols):
            rec=read(cols[k],'column')
            if rec is None: continue
            records+=1
            if (field(rec,'iteration')!=i or field(rec,'column_index')!=k or field(rec,'column_count')!=n
                    or field(rec,'identity_sha256')!=sid or k>=n
                    or field(rec,'iteration_start_sha256')!=start['payload_sha256']
                    or field(rec,'column_input_sha256')!=digest(ck['gas_columns'][k])):
                problems.append('COLUMN_RECORD_MISMATCH '+cols[k])
            elif restored is not None:
                # Decode now; the parsed record is released before the next is read.
                try: restored.append(decode(rec['result']))
                except (CheckpointError,KeyError) as exc:
                    problems.append('COLUMN_RESULT_UNDECODABLE '+type(exc).__name__+' '+cols[k])
            rec=None
        if completed is not None and (field(completed,'iteration')!=i or field(completed,'identity_sha256')!=sid
                or field(completed,'iteration_start_sha256')!=start['payload_sha256'] or len(cols)!=n
                or type(field(completed,'converged')) is not bool):
            problems.append('COMPLETED_RECORD_MISMATCH '+path)
        chain.append(dict(iteration=i,start=start,completed=completed,records=records,restored=restored))
    committed=[c['iteration'] for c in chain]
    if committed!=list(range(len(committed))): problems.append('NONCONTIGUOUS_ITERATION_STARTS')
    loose=[int(os.path.basename(p)[10:]) for p in report['uncommitted_iteration_directories']]
    if any(i!=len(committed) for i in loose): problems.append('UNCOMMITTED_DIRECTORY_NOT_AT_RESUME_POINT')
    if loose and chain and (chain[-1]['completed'] is None or chain[-1]['completed'].get('converged') is not False):
        problems.append('UNCOMMITTED_DIRECTORY_AFTER_UNFINISHED_OR_CONVERGED_ITERATION')
    if chain and chain[-1]['restored'] is None: problems.append('RESUME_ITERATION_NOT_HIGHEST_START')
    for c in chain[:-1]:
        if c['records']!=n or c['completed'] is None or c['completed'].get('converged') is not False:
            problems.append('EARLIER_ITERATION_INCOMPLETE_OR_TERMINAL iteration=%d'%c['iteration'])
    if problems:
        raise CheckpointError('CHECKPOINT_REJECTED; every file preserved unchanged; problems: '
                              +' | '.join(problems)+'; report: '+json.dumps(report))
    return chain,report


def _resume_point(directory,ck,chain,fixed,controls):
    """Exact-arithmetic chain: START(0) gas is the input, every later gas is ONE
    relaxation of the previous gas with its recorded updated gas, current=fixed+gas."""
    if not chain: return None
    ident=ck['identity']['inputs_sha256']; relax=ck['relax']
    if len(chain)>controls['max_iterations']: raise CheckpointError('ITERATION_BEYOND_BUDGET')
    previous=None
    for c in chain:
        start=c['start']; i=c['iteration']
        if start['fixed_source_fourier_J']['array_sha256']!=ident['fixed_source_fourier_J']:
            raise CheckpointError('FIXED_SOURCE_MISMATCH iteration=%d'%i)
        gas=_get(directory,start['gas_fourier_J'])
        current=_get(directory,start['current_source_fourier_J'])
        for name in ('fixed_source_fourier_J','prepared_wavevectors','prepared_weighted_responses'):
            _get(directory,start[name])
        if digest(fixed+gas)!=digest(current):
            raise CheckpointError('CURRENT_SOURCE_NOT_FIXED_PLUS_GAS iteration=%d'%i)
        updated=None if c['completed'] is None else _get(directory,c['completed']['updated_gas_fourier_J'])
        if previous is None:
            if start['gas_fourier_J']['array_sha256']!=ident['initial_gas_fourier_J'] or start['history']!=['l',[]]:
                raise CheckpointError('ITERATION0_NOT_INITIAL_STATE')
        else:
            p_gas,p_updated,p=previous
            if digest(relax(p_gas,p_updated))!=start['gas_fourier_J']['array_sha256']:
                raise CheckpointError('RELAXATION_CHAIN_BROKEN; gas iterate is not exactly one relaxation, iteration=%d'%i)
            if start['history']!=['l',p['start']['history'][1]+[p['completed']['history_entry']]]:
                raise CheckpointError('HISTORY_CHAIN_BROKEN iteration=%d'%i)
        previous=(gas,updated,c)
    top=chain[-1]; gas=previous[0]
    restored=top['restored']  # decoded one record at a time in _scan
    if type(restored) is not list or len(restored)!=top['records']:
        raise CheckpointError('RESUME_ITERATION_RECORDS_INCOMPLETE iteration=%d'%top['iteration'])
    return dict(iteration=top['iteration'],gas=gas,history=decode(top['start']['history']),
        restored=restored,next_column_index=len(restored),start=top['start'],
        completed=top['completed'],consumed=False)


def open_run(*,checkpoint,solver_file,inputs,fixed,relax):
    """Create (mode='new') or verify and resume (mode='resume'). Writes nothing in
    resume mode until identity, integrity and the exact relaxation chain pass."""
    if type(checkpoint) is not dict or set(checkpoint)!={'module','directory','mode','caller_identity'}:
        raise CheckpointError('CHECKPOINT_FIELDS module,directory,mode,caller_identity required')
    mode=checkpoint['mode']
    if mode not in ('new','resume'): raise CheckpointError('EXPLICIT_MODE new|resume REQUIRED')
    directory=os.path.abspath(os.fspath(checkpoint['directory']))
    if not 0<inputs['controls']['max_iterations']<=10000 or not 0<len(inputs['gas_columns'])<=100000:
        raise CheckpointError('CHECKPOINT_NAMING_LIMIT iterations<=10000, columns<=100000')
    identity=_identity(solver_file=solver_file,inputs=inputs,caller=checkpoint['caller_identity'],fixed=fixed)
    sid=_sha(_canonical(identity))
    token='%020d-%d-%s'%(time.time_ns(),os.getpid(),os.urandom(4).hex())
    ck=dict(directory=directory,mode=mode,identity=identity,identity_sha256=sid,token=token,
        column_count=len(inputs['gas_columns']),gas_columns=inputs['gas_columns'],relax=relax,
        resume=None,report=None,start_sha={},next_column={},lock=None,
        written={'iteration_starts':0,'columns':0,'completed':0,'failures':0})
    if mode=='new':
        try: os.mkdir(directory)
        except FileExistsError:
            raise CheckpointError('CHECKPOINT_DIRECTORY_EXISTS; never reused as new: '+directory) from None
        ck['lock']=_lock(directory,True)
        os.mkdir(os.path.join(directory,'blobs')); os.mkdir(os.path.join(directory,'attempts'))
        _write(os.path.join(directory,'IDENTITY.json'),
               {'kind':'identity','identity':identity,'identity_sha256':sid},token)
        ck['report']={'interrupted_temporary_files':[],'attempts_without_end':[],'failure_records':[],
                      'uncommitted_iteration_directories':[],'ignored_system_files':[]}
    else:
        if not os.path.isdir(directory): raise CheckpointError('CHECKPOINT_DIRECTORY_MISSING '+directory)
        ck['lock']=_lock(directory,False)
        try:
            stored=_read(os.path.join(directory,'IDENTITY.json'),'identity')
            if _sha(_canonical(stored['identity']))!=stored['identity_sha256']:
                raise CheckpointError('IDENTITY_RECORD_INCONSISTENT')
            if stored['identity_sha256']!=sid:
                raise CheckpointError('IDENTITY_MISMATCH; checkpoint rejected, saved columns not used; differing: '
                                      +', '.join(_differences(stored['identity'],identity)))
            chain,ck['report']=_scan(directory,ck)
            ck['resume']=_resume_point(directory,ck,chain,fixed,inputs['controls'])
        except (KeyError,TypeError,IndexError,ValueError) as exc:
            ck['lock'].close()
            raise CheckpointError('MALFORMED_CHECKPOINT_CONTENT '+type(exc).__name__+': '+str(exc)) from None
        except BaseException:
            ck['lock'].close(); raise
    r=ck['resume']
    _write(os.path.join(directory,'attempts',token+'.start.json'),
           {'kind':'attempt_start','identity_sha256':sid,'attempt':token,'mode':mode,'pid':os.getpid(),
            'started_unix_ns':time.time_ns(),'preserved_report':ck['report'],
            'resume_point':None if r is None else {'iteration':r['iteration'],
                                                  'next_column_index':r['next_column_index']}},token)
    return ck


def begin_iteration(ck,*,iteration,gas,current,fixed,prepared,history):
    """Returns (restored_results, resumed). New iteration: commit START first."""
    r=ck['resume']
    if r is not None and not r['consumed']:
        if iteration!=r['iteration']: raise CheckpointError('RESUME_SEQUENCE_ERROR')
        r['consumed']=True; start=r['start']
        bad=[name for name,value in (('gas_fourier_J',gas),('current_source_fourier_J',current),
                ('fixed_source_fourier_J',fixed),('prepared_wavevectors',prepared['wavevectors']),
                ('prepared_weighted_responses',prepared['weighted_responses']))
             if digest(value)!=start[name]['array_sha256']]
        if digest(prepared)!=start['prepared_metric_response_sha256']: bad.append('prepared_metric_response')
        if encode(history)!=start['history']: bad.append('history')
        if bad: raise CheckpointError('RESUMED_ITERATION_NOT_REPRODUCED '+','.join(bad))
        ck['start_sha'][iteration]=start['payload_sha256']
        restored=r.pop('restored'); ck['next_column'][iteration]=len(restored)
        return restored,True
    folder=os.path.join(ck['directory'],'iteration_%04d'%iteration)
    if os.path.exists(os.path.join(folder,'START.json')): raise CheckpointError('START_EXISTS '+folder)
    payload={'kind':'iteration_start','identity_sha256':ck['identity_sha256'],'iteration':iteration,
        'column_count':ck['column_count'],'gas_fourier_J':_put(ck,gas),
        'current_source_fourier_J':_put(ck,current),'fixed_source_fourier_J':_put(ck,fixed),
        'prepared_wavevectors':_put(ck,prepared['wavevectors']),
        'prepared_weighted_responses':_put(ck,prepared['weighted_responses']),
        'prepared_metric_response_sha256':digest(prepared),'history':_exact(history,'history'),
        'attempt':ck['token']}
    try: os.mkdir(folder)
    except FileExistsError: pass  # uncommitted container left by an interrupted attempt
    ck['start_sha'][iteration]=_write(os.path.join(folder,'START.json'),payload,ck['token'])
    ck['next_column'][iteration]=0; ck['written']['iteration_starts']+=1
    return [],False


def write_column(ck,*,iteration,column_index,column,result):
    if ck['next_column'].get(iteration)!=column_index or column is not ck['gas_columns'][column_index]:
        raise CheckpointError('COLUMN_ORDER_ERROR iteration=%d column=%d'%(iteration,column_index))
    payload={'kind':'column','identity_sha256':ck['identity_sha256'],'iteration':iteration,
        'iteration_start_sha256':ck['start_sha'][iteration],'column_index':column_index,
        'column_count':ck['column_count'],'column_input_sha256':digest(column),
        'result':_exact(result,'column %d'%column_index),'attempt':ck['token']}
    _write(os.path.join(ck['directory'],'iteration_%04d'%iteration,'column_%05d.json'%column_index),
           payload,ck['token'])
    ck['next_column'][iteration]=column_index+1; ck['written']['columns']+=1


def complete_iteration(ck,*,iteration,updated,residual,bound,history_entry,converged):
    """After ALL columns. A COMPLETED record found on resume must be reproduced bitwise."""
    if ck['next_column'].get(iteration)!=ck['column_count']: raise CheckpointError('ITERATION_NOT_COMPLETE')
    fields={'iteration':iteration,'iteration_start_sha256':ck['start_sha'][iteration],
        'gas_fourier_residual_J':encode(residual),'bound_J':encode(bound),
        'history_entry':_exact(history_entry,'history entry'),'converged':converged is True}
    r=ck['resume']
    existing=r['completed'] if r is not None and r['iteration']==iteration else None
    if existing is not None:
        bad=[k for k,v in fields.items() if existing[k]!=v]
        if digest(updated)!=existing['updated_gas_fourier_J']['array_sha256']: bad.append('updated_gas_fourier_J')
        if bad: raise CheckpointError('COMPLETED_RECORD_NOT_REPRODUCED '+','.join(bad))
        return
    payload=dict(fields,kind='iteration_completed',identity_sha256=ck['identity_sha256'],
        column_count=ck['column_count'],updated_gas_fourier_J=_put(ck,updated),attempt=ck['token'])
    _write(os.path.join(ck['directory'],'iteration_%04d'%iteration,'COMPLETED.json'),payload,ck['token'])
    ck['written']['completed']+=1


def finish(ck,*,outcome,result):
    """Terminal records. Errors here are REPORTED in the returned summary so the
    actual scientific result/failure is never discarded by a checkpoint write."""
    errors=[]
    try:
        if outcome=='FAILED_SOURCE_PREPARATION':
            f=result['failure']; it=f['iteration']
            _write(os.path.join(ck['directory'],'iteration_%04d'%it,'FAILURE.%s.json'%ck['token']),
                {'kind':'failure','identity_sha256':ck['identity_sha256'],'iteration':it,
                 'column_index':f['column_index'],'iteration_start_sha256':ck['start_sha'][it],
                 'failure':_exact(f,'failure'),'attempt':ck['token']},ck['token'])
            ck['written']['failures']+=1
        _write(os.path.join(ck['directory'],'attempts',ck['token']+'.end.json'),
            {'kind':'attempt_end','identity_sha256':ck['identity_sha256'],'attempt':ck['token'],
             'outcome':outcome,'records_written':dict(ck['written']),'ended_unix_ns':time.time_ns()},ck['token'])
    except (OSError,CheckpointError,KeyError,TypeError) as exc:
        errors.append(type(exc).__name__+': '+str(exc))
    if ck['lock'] is not None:
        ck['lock'].close(); ck['lock']=None
    r=ck['resume']
    return {'format':FORMAT,'directory':ck['directory'],'identity_sha256':ck['identity_sha256'],
        'attempt':ck['token'],'mode':ck['mode'],'outcome':outcome,
        'resumed_from':None if r is None else {'iteration':r['iteration'],'next_column_index':r['next_column_index']},
        'records_written':dict(ck['written']),'preserved_report':ck['report'],'finish_errors':errors,
        'scope':'restart evidence only; no physics, acceptance or convergence claim'}
