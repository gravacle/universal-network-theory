"""Inert, byte-pinned DDO154 point custody. No launch or run-directory discovery.

Aggregate encoding: SHA256 of UTF-8 canonical JSON (sorted keys, compact
separators, finite numbers); arrays: dtype/shape plus C-order bytes digest.
This derives scope, not scientific approval. The speed/uncertainty policy is
explicitly unresolved until separately reviewed in the LO coverage object.
"""
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import numpy as np

ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
HERE = Path(__file__).resolve().parent
DRIVER = ART/'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py'
DRIVER_SHA = 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
COMMON = HERE/'certs_common_r5_cx2v001.py'
COMMON_SHA = 'c75aaa5a197efe7bde1014269d74aa37810ccce6f95b7eec1078352f09ffb3b7'
A2_SHA = '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7'

def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

def allowed_path(path):
    p=Path(path).resolve(strict=True)
    parts=p.parts
    if '.codex' in parts or 'KMAX_A2F10_C5H_RUN_V001' in parts:
        raise ValueError('forbidden input')
    if 'runs_ext' in parts and any(x.startswith('UVT_') for x in parts):
        raise ValueError('forbidden UVT run')
    if not any(p.is_relative_to(Path(r)) for r in ('/Users/bgm/Research','/Volumes/External1')):
        raise ValueError('outside research input roots')
    return p

def sha(path):
    p=allowed_path(path);h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()

def pin(path):
    return {'path':str(Path(path)), 'sha256':sha(path)}

def read_pin(ref, document=True):
    if not isinstance(ref,dict) or set(ref)!= {'path','sha256'}:
        raise ValueError('exact byte reference required')
    p=allowed_path(ref['path'])
    raw=p.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=ref['sha256']:raise ValueError('byte pin mismatch')
    return json.loads(raw) if document else raw

def module(path,name,expected):
    if sha(path)!=expected:raise ValueError('module pin mismatch')
    sp=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(sp);sys.modules[name]=obj
    sp.loader.exec_module(obj);return obj

def libraries():
    return (module(DRIVER,'cx2pc_driver',DRIVER_SHA),
            module(COMMON,'cx2pc_common',COMMON_SHA))

def production_scope(spec):
    uv=spec['numerics']['uv_tail']
    if uv.get('enabled') is not True or uv.get('source_rule')!='continuum_v001':
        raise ValueError('PRODUCTION_CONTINUUM_TAIL_REQUIRED')
    if uv.get('outer')!={'shape':'cylinder','K_big_inverse_kpc':128.0}:
        raise ValueError('PRODUCTION_K128_REQUIRED')
    gas=uv.get('gas',{})
    if gas.get('interp')!='lagrange3_s_gl4' or type(gas.get('M_s')) is not int or gas['M_s']!=128:
        raise ValueError('PRODUCTION_GAS_MS128_REQUIRED')
    return {'driver_sha256':DRIVER_SHA,'K_big_inverse_kpc':128.0,'gas_M_s':128}

def identity(spec):
    production_scope(spec)
    if spec.get('galaxy')!='DDO154':raise ValueError('DDO154 only')
    n=copy.deepcopy(spec['numerics'])
    for k in ('eps_certificate','lo_certificate'):n['uv_tail'].pop(k,None)
    return {'driver_sha256':DRIVER_SHA,'physical':copy.deepcopy(spec['physical']),
            'coefficients':copy.deepcopy(spec['coefficients']),'numerics':n}

def array_record(a):
    a=np.ascontiguousarray(a)
    if a.dtype.hasobject or not np.isfinite(a).all():raise ValueError('invalid coefficient array')
    return {'dtype':a.dtype.str,'shape':list(a.shape),'bytes_sha256':hashlib.sha256(a.tobytes()).hexdigest()}

def point_geometry(spec,driver=None):
    d=driver or libraries()[0]
    p=spec['physical']
    if spec.get('galaxy')!='DDO154' or p['inclination_deg']!=66.0:raise ValueError('unsupported geometry')
    if not all(type(v) in (int,float) and math.isfinite(v) and v>0 for v in p.values()):
        raise ValueError('invalid physical value')
    profile,mono,binding,record=d.derive_geometry('DDO154',float(p['distance_Mpc']),66.0)
    # derive_geometry supplies the same radial data at the registered distance.
    return profile,mono,binding,record

def derive_details(*,spec,driver_sha256=DRIVER_SHA):
    if driver_sha256!=DRIVER_SHA:raise ValueError('unsupported driver')
    ident=identity(spec);d,cc=libraries()
    uv=spec['numerics']['uv_tail']
    if uv.get('source_rule')!='continuum_v001' or uv.get('enabled') is not True:
        raise ValueError('production continuum point required')
    if uv['outer'] != {'shape':'cylinder','K_big_inverse_kpc':128.0}:
        raise ValueError('unsupported outer domain')
    grid=spec['numerics']['composite_grid_spec']
    if spec['numerics']['truncation']!={'shape':'cube'} or max(grid['breaks_inverse_kpc'])!=4 or min(grid['breaks_inverse_kpc'])!=-4:
        raise ValueError('K4 cube required')
    ref=spec['coefficients']
    if ref['sha256']!=A2_SHA or sha(ref['path'])!=A2_SHA:raise ValueError('coefficient custody')
    with np.load(allowed_path(ref['path']),allow_pickle=False) as f:
        arrays={k:array_record(f[k]) for k in ('source_hessian_grid','background_C','background_mu')}
    profile,mono,binding,record=point_geometry(spec,d)
    prereg=read_pin(cc.pin('prereg_v005'))
    rows=binding['query_rows'];ids=[x['id'] for x in rows]
    if ids!=prereg['row_ids'] or len(set(ids))!=len(ids):raise ValueError('ordered row contract mismatch')
    tau=prereg['tau_km_s']
    if len(tau)!=len(ids) or any(not math.isfinite(x) or x<=0 for x in tau):raise ValueError('invalid tau')
    row={'schema':'DDO154_POINT_ROWS_CX2V001','rows':rows,'tau_km_s':tau,
         'distance_Mpc':spec['physical']['distance_Mpc'],
         'speed_reference_policy':'PENDING_REVIEWED_LO_COVERAGE_OBJECT',
         'uncertainty_carrier_policy':'PREREG_V005_TAU; CALIBRATION_CARRIER_PENDING_ROOT',
         'prereg':cc.pin('prereg_v005')}
    modules=d.uvt_static_pins(False)
    for name,(path,want) in d.GEOMETRY_PINS.items():
        if sha(path)!=want:raise ValueError('geometry input pin mismatch '+name)
        modules[str(path)]=want
    modules.update({str(DRIVER):DRIVER_SHA,str(COMMON):COMMON_SHA,str(Path(__file__)):sha(__file__)})
    geo={'schema':'DDO154_DERIVED_GEOMETRY_CX2V001','profile':profile['galaxies']['DDO154'],
         'monotone':mono,'binding':binding,'derivation':record}
    custody={
      'grid_sha256':digest({'encoding':'ARRAY_C_ORDER_V1','coefficient_file':ref,'grid':arrays['source_hessian_grid'],'composite_grid':grid}),
      'background_sha256':digest({'C':arrays['background_C'],'mu':arrays['background_mu'],'physical':spec['physical']}),
      'geometry_sha256':digest(geo),'modules_sha256':digest(modules),'row_contract_sha256':digest(row)}
    return {'schema':'DDO154_POINT_CUSTODY_CX2V001','identity':ident,'point_sha256':digest(ident),
            'custody':custody,'custody_sha256':digest(custody),'arrays':arrays,'geometry':geo,'row_contract':row,'modules':modules}

def derive_custody(*,spec,driver_sha256):
    return derive_details(spec=spec,driver_sha256=driver_sha256)['custody']

def write_new(path,obj):
    p=Path(path)
    if not p.parent.resolve().is_relative_to(HERE):raise ValueError('output outside certificate directory')
    raw=json.dumps(obj,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n'
    with p.open('xb') as f:f.write(raw)
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()}

if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser();a.add_argument('--spec',required=True);a.add_argument('--out',required=True)
    ns=a.parse_args();s=json.loads(allowed_path(ns.spec).read_bytes())
    print(json.dumps(write_new(ns.out,derive_details(spec=s))))
