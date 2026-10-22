"""NGC-only anisotropic quadrature and immutable roster-cut custody. Inert."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import numpy as np

CHECKPOINT = (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py'),
              '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114')


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()


def checkpoint_module():
    p,s=CHECKPOINT
    if sha(p)!=s:raise ValueError('CHECKPOINT_PIN_MISMATCH')
    spec=importlib.util.spec_from_file_location('ngc_cut_checkpoint',p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m


def validate_anisotropic(spec, kmax=2.):
    if not isinstance(spec,dict) or set(spec)-{'version','axes','scope'} or not isinstance(spec.get('version'),str):
        raise ValueError('NGC_ANISOTROPIC_SCHEMA')
    axes=spec.get('axes')
    if not isinstance(axes,dict) or set(axes)!=set('xyz'):raise ValueError('NGC_ANISOTROPIC_AXES')
    for key,n in zip('xyz',(120,120,80)):
        a=axes[key]
        if not isinstance(a,dict) or set(a)!={'breaks_inverse_kpc','panel_orders','total_axis_nodes'}:
            raise ValueError('NGC_ANISOTROPIC_AXIS_SCHEMA')
        br,po=a['breaks_inverse_kpc'],a['panel_orders']
        if not isinstance(br,list) or not isinstance(po,list) or len(br)!=len(po)+1:
            raise ValueError('NGC_ANISOTROPIC_PARTITION')
        if any(type(x) not in (int,float) or not math.isfinite(x) for x in br):raise ValueError('NGC_ANISOTROPIC_BREAKS')
        if any(type(x)is not int or x<2 for x in po) or sum(po)!=n or a['total_axis_nodes']!=n:
            raise ValueError('NGC_ANISOTROPIC_BUDGET')
        if br[0]!=-kmax or br[-1]!=kmax or any(y<=x for x,y in zip(br,br[1:])):
            raise ValueError('NGC_ANISOTROPIC_CUBE')
        if br!=[-x for x in br[::-1]] or po!=po[::-1]:raise ValueError('NGC_ANISOTROPIC_REFLECTION')
    if axes['x']!=axes['y']:raise ValueError('NGC_TRANSVERSE_AXES_DIFFER')
    # Dispatch 0517 specifies the registered T120L, not an arbitrary 120x120x80.
    if axes['x']['panel_orders'] != [22,16,8,5,6,3,3,6,5,8,16,22] or axes['z']['panel_orders'] != [14,10,5,3,6,2,2,6,3,5,10,14]:
        raise ValueError('NGC_NOT_REGISTERED_T120L')
    if axes['x']['breaks_inverse_kpc'] != [-2,-1,-.3,-.1,-.03,-.01,0,.01,.03,.1,.3,1,2] or axes['z']['breaks_inverse_kpc']!=axes['x']['breaks_inverse_kpc']:
        raise ValueError('NGC_NOT_REGISTERED_T120L_BREAKS')
    return spec


def tensor_grid(spec,kpc_m,kmax=2.):
    validate_anisotropic(spec,kmax)
    av=[];aw=[]
    for name in 'xyz':
        a=spec['axes'][name];parts=[];weights=[]
        breaks=np.asarray(a['breaks_inverse_kpc'],dtype=float)
        for lo,hi,n in zip(breaks[:-1],breaks[1:],a['panel_orders']):
            gx,gw=np.polynomial.legendre.leggauss(n)
            parts.append(((lo+hi)/2+(hi-lo)*gx/2)/kpc_m)
            weights.append((hi-lo)*gw/(2*kpc_m))
        av.append(np.concatenate(parts));aw.append(np.concatenate(weights))
    # Same operation/order as the reviewed H-OVR reference, including wx*wy*wz.
    waves=np.array([(x,y,z) for x in av[0] for y in av[1] for z in av[2]])
    dk=np.array([x*y*z for x in aw[0] for y in aw[1] for z in aw[2]])
    if not np.isfinite(waves).all() or not np.isfinite(dk).all() or np.any(dk<=0) or any(np.any(x==0) for x in av):
        raise ValueError('NGC_INVALID_GRID')
    return waves,dk


def controls_digest(controls):
    # Optional absent arguments and explicit None have one identity.
    clean={k:v for k,v in controls.items() if k not in ('progress_directory','ngc_outer_gas_cut') and v is not None}
    return checkpoint_module().digest(clean)


def apply_cut(columns,pin,kpc_m,controls=None):
    if pin is None:return columns,None
    if not isinstance(pin,dict) or set(pin)!={'path','sha256'} or not Path(pin['path']).is_absolute():
        raise ValueError('NGC_CUT_PIN_SCHEMA')
    if sha(pin['path'])!=pin['sha256']:raise ValueError('NGC_CUT_PIN_MISMATCH')
    r=json.loads(Path(pin['path']).read_text())
    if r.get('schema')!='NGC_CANDIDATE_ROSTER_CUT_CX3V001':raise ValueError('NGC_CUT_RECORD_SCHEMA')
    cm=checkpoint_module()
    if r.get('full_roster_digest')!=cm.digest(columns):raise ValueError('NGC_CUT_FULL_ROSTER_MISMATCH')
    if controls is not None and r.get('controls_sha256')!=controls_digest(controls):
        raise ValueError('NGC_CUT_DIFFERENT_PHYSICAL_OR_NUMERICAL_POINT')
    cut=r.get('first_unconfined_R_kpc')
    if type(cut) not in (int,float) or not math.isfinite(cut) or cut<=0:raise ValueError('NGC_CUT_RADIUS')
    radii=[c['R_m']/kpc_m for c in columns]
    if cut not in radii:raise ValueError('NGC_CUT_NOT_A_ROSTER_RADIUS')
    kept=[c for c,radius in zip(columns,radii) if radius<cut]
    if not kept:raise ValueError('NGC_CUT_EMPTY_ROSTER')
    if r.get('kept_roster_digest')!=cm.digest(kept):raise ValueError('NGC_CUT_KEPT_ROSTER_MISMATCH')
    mass=lambda c:c['Sigma_kg_m2']*c['R_m']*c['radial_weight_m']*c['azimuth_weight_rad']
    total=math.fsum(mass(c) for c in columns)
    frac=math.fsum(mass(c) for c,rad in zip(columns,radii) if rad>=cut)/total
    if not math.isfinite(frac) or abs(frac-r.get('dropped_HI_mass_fraction',-1))>1e-14:
        raise ValueError('NGC_CUT_MASS_MISMATCH')
    # A pin and mass do not turn a numerical bracket failure into a proof.
    if r.get('confinement_status')!='CERTIFIED_UNCONFINED' or not isinstance(r.get('classification_evidence'),dict) or not r['classification_evidence']:
        raise ValueError('NGC_CUT_CONFINEMENT_EVIDENCE_REQUIRED')
    rec=dict(r,record_pin=dict(pin),computed_dropped_HI_mass_fraction=frac,columns_kept=len(kept),columns_dropped=len(columns)-len(kept))
    return kept,rec


# Added to the immutable grid/cut helper; no source read until explicitly called.
REGISTERED_GL_NODES = (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json'), 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d')
OUTER_CUT_REASON = 'QUERY_BEYOND_OUTER_GAS_CUT'
SUPPORT_GAP_REASON = 'QUERY_OUTSIDE_RETAINED_SUPPORT'


def read_cut_record(pin):
    if not isinstance(pin,dict) or set(pin)!={'path','sha256'} or not isinstance(pin['path'],str) or not Path(pin['path']).is_absolute():
        raise ValueError('NGC_CUT_PIN_SCHEMA')
    if sha(pin['path'])!=pin['sha256']:raise ValueError('NGC_CUT_PIN_MISMATCH')
    record=json.loads(Path(pin['path']).read_bytes())
    if not isinstance(record,dict) or record.get('schema')!='NGC_CANDIDATE_ROSTER_CUT_CX3V001':raise ValueError('NGC_CUT_RECORD_SCHEMA')
    radius=record.get('first_unconfined_R_kpc')
    if type(radius) not in (int,float) or not math.isfinite(radius) or radius<=0:raise ValueError('NGC_CUT_RADIUS')
    if record.get('confinement_status')!='CERTIFIED_UNCONFINED' or not isinstance(record.get('classification_evidence'),dict) or not record['classification_evidence']:
        raise ValueError('NGC_CUT_CONFINEMENT_EVIDENCE_REQUIRED')
    return record


def registered_route_b_nodes(order,kpc_m):
    p,s=REGISTERED_GL_NODES
    if sha(p)!=s:raise ValueError('NGC_REGISTERED_GL_NODE_PIN')
    doc=json.loads(p.read_bytes())
    if type(order) is not int or order not in (4,10) or doc['kpc_m']!=kpc_m:raise ValueError('NGC_REGISTERED_GL_NODE_ORDER_OR_UNITS')
    for pin in doc['sources'].values():
        if sha(pin['path'])!=pin['sha256']:raise ValueError('NGC_REGISTERED_GL_SOURCE_PIN')
    return list(doc['orders'][str(order)]['radii_m'])


def registered_cut_rows(pin,query_rows,order,kpc_m):
    """Derive outer and support-gap rows from pinned cut and original registered GL prefix."""
    if pin is None:return {}
    record=read_cut_record(pin);cut=record['first_unconfined_R_kpc']*kpc_m
    kept=[r for r in registered_route_b_nodes(order,kpc_m) if r<cut]
    if not kept:raise ValueError('NGC_CUT_EMPTY_REGISTERED_SUPPORT')
    answer={}
    for q in query_rows:
        radius=q['radius_m']
        if type(radius) not in (int,float) or not math.isfinite(radius):raise ValueError('NGC_QUERY_RADIUS')
        if radius>=cut:answer[q['id']]=OUTER_CUT_REASON
        elif radius>kept[-1]:answer[q['id']]=SUPPORT_GAP_REASON
    return answer
