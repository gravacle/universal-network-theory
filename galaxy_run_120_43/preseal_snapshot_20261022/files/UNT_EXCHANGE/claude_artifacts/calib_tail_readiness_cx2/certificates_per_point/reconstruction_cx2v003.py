"""Explicit-input saved-source reconstruction; pinned v010 r5; production K128/M_s128 or explicit synthetic fixture.

No run discovery, solver, launch, subprocess, network or output write. Inputs
are byte references. This module does not certify occurrence completeness or
point/custody joins. Static TailState rebuilds are explicit method calls only.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import zipfile
import numpy as np

H = Path(__file__).resolve().parent
ART = H.parent.parent
INV = H/'consumed_states_cx2v005.py'
INV_SHA = '7b7400f331970a5f5fb7f7104f5e1850a765fcd04fc993100b5d1f0f37f4d653'
MODULE = ART/'tail_scheme_impl_c2/driver_r5/module'
PINS = {
    'roster': (MODULE/'uv_tail_source_roster_c2v001.py','4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2'),
    'lib': (MODULE/'owned_uv_tail_lapse_v002.py','2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54'),
    'provider': (MODULE/'posix_libm_bessel_jn_provider_c2v001.py','d6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171'),
    'binding': (ART/'tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001_r5.py','1e27430c12cc84195b7642fe925bc6f9916a55158ecc02c9fbff9b8564506329'),
    'forward': (Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/galaxy_baryonic_source_forward_v002.py'),'e9be043b46790e3493f4e427fb483a98a5665f004dfac287d5758afce0ac96ad'),
}

class ReconstructionError(ValueError):
    pass

def _module(path, sha, name):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=sha:raise ReconstructionError('SOURCE_PIN_MISMATCH')
    sp=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m)
    if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=sha:raise ReconstructionError('SOURCE_CHANGED')
    return m

I=_module(INV,INV_SHA,'cx2_reconstruction_inventory')

def _positive(x, label):
    if type(x) not in (int,float) or not math.isfinite(x) or x<=0:raise ReconstructionError(label)
    return float(x)

def _real(a, label):
    a=np.asarray(a)
    if a.dtype.hasobject or not np.isfinite(a).all() or (np.iscomplexobj(a) and np.any(a.imag!=0)):
        raise ReconstructionError(label)
    return a.real

class SourceProduct:
    """Reconstructed source, not a production completeness assertion."""
    def __init__(self, roster, files, components, role):
        self.roster=roster
        self.source_sha256=roster.digest()
        self.source_record=roster.record()
        self.source_files=list(files)
        self.components=components
        self.role=role
        self.source_digest_verified=False
        self.source_assertion_pin=None
        self.nonnegative_masses=None
        self.positive_total_zero_mode=None
        self.total_zero_mode_mass=None
        self.dependency_pins=[]

    def record(self):
        return dict(role=self.role,source_sha256=self.source_sha256,source_record=self.source_record,
                    source_digest_verified=self.source_digest_verified,source_assertion_pin=self.source_assertion_pin,
                    source_files=self.source_files,dependency_pins=self.dependency_pins,components=self.components,
                    nonnegative_masses=self.nonnegative_masses,positive_total_zero_mode=self.positive_total_zero_mode,
                    total_zero_mode_mass=self.total_zero_mode_mass,complete=False,
                    certificate_status='UNAVAILABLE',point_status='INCOMPLETE')

class StateProduct:
    def __init__(self,state,source,pins,*,digest_verified,factors_reconstructed):
        self.state=state;self.source=source;self.state_sha256=state.digest
        self.state_digest_verified=bool(digest_verified)
        self.source_digest_verified=source.source_digest_verified
        self.factors_reconstructed=bool(factors_reconstructed)
        self.input_pins=list(pins)
        self.context_ref=None;self.descriptor_ref=None
        aa=state.to_arrays()
        self.factor_arrays_sha256=I.digest({k:{'dtype':aa[k].dtype.str,'shape':list(aa[k].shape),'bytes_sha256':hashlib.sha256(np.ascontiguousarray(aa[k]).tobytes()).hexdigest()} for k in ('P','F')})

    def record(self):
        return dict(state_sha256=self.state_sha256,state_digest_verified=self.state_digest_verified,
                    source_digest_verified=self.source_digest_verified,factors_reconstructed=self.factors_reconstructed,
                    source=self.source.record(),input_pins=self.input_pins,context_ref=self.context_ref,descriptor_ref=self.descriptor_ref,
                    factor_arrays_sha256=self.factor_arrays_sha256,complete=False,driver_sha256=I.DRIVER_SHA,production_admissible=False,
                    i1t_status='SAVED_OR_REBUILT_RECORD; INDEPENDENT_PACKET_CHECK_REQUIRED',
                    certificate_status='UNAVAILABLE',point_status='INCOMPLETE')

class SavedSourceReconstructor:
    def __init__(self,context_ref,*,max_archive_bytes=512*1024*1024,allow_synthetic_fixture=False):
        self.pins={};self.source_pins={};self.dependency_pins={};self._loading_dependencies=True
        self.context_ref=dict(context_ref);self.max_archive_bytes=max_archive_bytes
        if type(max_archive_bytes) is not int or not 0<max_archive_bytes<=2*1024**3:
            raise ReconstructionError('ARCHIVE_LIMIT_INVALID')
        self.context=self.json(context_ref)
        if self.context.get('schema')!='DDO154_SAVED_SOURCE_CONTEXT_CX2V001' or self.context.get('galaxy')!='DDO154':
            raise ReconstructionError('DDO154_CONTEXT_REQUIRED')
        if self.context.get('driver_sha256')!=I.DRIVER_SHA:raise ReconstructionError('R5_DRIVER_REQUIRED')
        self.modules={}
        for key,(path,sha) in PINS.items():
            I.safe_path(path)
            self.modules[key]=_module(path,sha,'cx2_saved_'+key)
            self.pins[str(path)]={'path':str(path),'sha256':sha}
            self.dependency_pins[str(path)]={'path':str(path),'sha256':sha}
        self.rs=self.modules['roster'];self.lib=self.modules['lib'];self.rb=self.modules['binding']
        self.jn=self.modules['provider'].create_provider()
        self.profile=self.json(self.context['profile'])
        self.kpc_m=_positive(self.context['kpc_m'],'KPC_INVALID')
        self.solar_mass_kg=_positive(self.context['solar_mass_kg'],'SOLAR_MASS_INVALID')
        self.c_m_s=_positive(self.context['c_m_s'],'C_INVALID')
        if self.kpc_m!=self.lib.KPC_M:raise ReconstructionError('KPC_UNIT_MISMATCH')
        self.config=self.lib.normalize_config(self.json(self.context['config']))
        if self.config['source_rule']!='continuum_v001' or self.config['enabled'] is not True:
            raise ReconstructionError('CONTINUUM_TAIL_ON_REQUIRED')
        self.replay_scope=self.context.get('replay_scope','PRODUCTION_P128_MS128')
        if self.replay_scope=='SYNTHETIC_FIXTURE':
            if allow_synthetic_fixture is not True:raise ReconstructionError('SYNTHETIC_FIXTURE_REQUIRES_EXPLICIT_OPT_IN')
        elif self.replay_scope=='PRODUCTION_P128_MS128':
            if self.config['outer']!={'shape':'cylinder','K_big_inverse_kpc':128.0} or type(self.config['gas']['M_s']) is not int or self.config['gas']['M_s']!=128:
                raise ReconstructionError('PRODUCTION_K128_GAS_MS128_REQUIRED')
        else:raise ReconstructionError('REPLAY_SCOPE_UNSUPPORTED')
        self.M_s=self.config['gas']['M_s']
        self.edges=np.asarray(self.profile['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2'],float)
        if self.edges.ndim!=1 or len(self.edges)<2 or not np.isfinite(self.edges).all() or self.edges[0]<0 or np.any(np.diff(self.edges)<=0):
            raise ReconstructionError('ANNULUS_EDGES_INVALID')
        self.stars=self._stars()
        self._loading_dependencies=False

    def _bytes(self,ref):
        if not isinstance(ref,dict) or set(ref)!={'path','sha256'} or not I._hex(ref['sha256']):
            raise ReconstructionError('EXACT_BYTE_REFERENCE_REQUIRED')
        p=I.safe_path(ref['path'])
        if p.stat().st_size>self.max_archive_bytes:raise ReconstructionError('INPUT_TOO_LARGE')
        raw=p.read_bytes();sha=hashlib.sha256(raw).hexdigest()
        if sha!=ref['sha256']:raise ReconstructionError('BYTE_PIN_MISMATCH')
        prior=self.pins.get(str(p))
        if prior and prior['sha256']!=sha:raise ReconstructionError('BYTES_CHANGED')
        self.pins[str(p)]={'path':str(p),'sha256':sha}
        target=self.dependency_pins if self._loading_dependencies else self.source_pins
        target[str(p)]={'path':str(p),'sha256':sha}
        return raw

    def json(self,ref):
        raw=self._bytes(ref)
        if len(raw)>I.MAX_JSON_BYTES:raise ReconstructionError('JSON_TOO_LARGE')
        return I._strict_json(raw)

    def arrays(self,ref,keys=None):
        # Hash the exact bytes used by np.load; no hash/open race or pickle.
        import io
        raw=self._bytes(ref)
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            if sum(x.file_size for x in z.infolist())>self.max_archive_bytes:raise ReconstructionError('ARCHIVE_EXPANSION_TOO_LARGE')
        with np.load(io.BytesIO(raw),allow_pickle=False) as f:
            if len(f.files)!=len(set(f.files)):raise ReconstructionError('DUPLICATE_ARCHIVE_MEMBER')
            names=f.files if keys is None else keys
            a={k:np.array(f[k],copy=True) for k in names}
        for v in a.values():
            if v.dtype.hasobject or not np.isfinite(v).all():raise ReconstructionError('ARRAY_NONFINITE_OR_OBJECT')
        return a

    def _stars(self):
        return self.rs.stars_registered(self.profile,'DDO154',units={'kpc_m':self.kpc_m,'solar_mass_kg':self.solar_mass_kg},
                    radial_surface=self.modules['forward'].radial_surface)

    def _kwargs(self):
        return dict(s_edges_kpc2=self.edges,kpc_m=self.kpc_m,M_s=self.M_s)

    def _product(self,roster,role,components=None):
        if components is None:
            gas=roster.gas
            masses=np.concatenate(gas.elements_m) if gas is not None else np.zeros(0)
            if not np.isfinite(masses).all():raise ReconstructionError('NONFINITE_RECONSTRUCTED_MASS')
            components=[dict(role='gas',sign=1,mass=float(np.sum(masses)),nonnegative=bool(np.all(masses>=0)))]
        product=SourceProduct(roster,list(self.source_pins.values()),components,role)
        product.dependency_pins=list(self.dependency_pins.values())
        if hasattr(roster,'a'):
            product.nonnegative_masses=False
            product.positive_total_zero_mode=None
            return product
        gas_positive=all(c['nonnegative'] for c in components)
        star_positive=True;star_mass=0.
        if roster.stars is not None:
            _positive(roster.stars.height_kpc,'STELLAR_HEIGHT_INVALID')
            for c in roster.stars.components:
                _positive(c['outer_scale_kpc'],'STELLAR_OUTER_SCALE_INVALID')
                r=np.asarray(c['radii_kpc']);v=np.asarray(c['sigma_Msun_pc2'])
                if len(r)<2 or len(r)!=len(v) or not np.isfinite(r).all() or not np.isfinite(v).all() or np.any(np.diff(r)<=0) or r[0]<0:
                    raise ReconstructionError('STELLAR_PROFILE_INVALID')
                star_positive=star_positive and bool(np.all(v>=0))
            # Fresh clone avoids mutating the build object's certificate cache.
            star_mass=float(self._stars().radial_transform(np.array([0.]),self.jn.j0)[0])
            components.append(dict(role='registered_stars',sign=1,mass=star_mass,nonnegative=star_positive))
        total=star_mass+sum(c['mass'] for c in components if c['role']!='registered_stars')
        if not math.isfinite(total):raise ReconstructionError('TOTAL_ZERO_MODE_NONFINITE')
        product.nonnegative_masses=bool(gas_positive and star_positive)
        product.total_zero_mode_mass=total
        product.positive_total_zero_mode=bool(product.nonnegative_masses and total>0)
        return product

    def route_a(self,initial_rings_ref,element_refs,relaxation):
        if type(relaxation) not in (int,float) or not math.isfinite(relaxation) or not 0<relaxation<=1:
            raise ReconstructionError('RELAXATION_OUTSIDE_CONVEX_INTERVAL')
        init=self.arrays(initial_rings_ref,('R','z','m'))
        if any(x.ndim!=1 for x in init.values()) or len({len(x) for x in init.values()})!=1:
            raise ReconstructionError('INITIAL_RING_SHAPE')
        for x in init.values():_real(x,'INITIAL_RINGS_NONREAL')
        elements=[]
        for ref in element_refs:
            e=self.arrays(ref,('positions_m','integrated_J'))
            pos=_real(e['positions_m'],'ELEMENT_POSITION_NONREAL');J=_real(e['integrated_J'],'ELEMENT_SOURCE_NONREAL')
            if pos.ndim!=2 or pos.shape[1]!=3 or J.ndim!=1 or len(pos)!=len(J):raise ReconstructionError('ELEMENT_SHAPE')
            elements.append(dict(positions_m=pos,integrated_J=J))
        result=[]
        for n in range(len(elements)+1):
            roster=self.rs.roster_route_a(self.stars,init,elements[:n],relaxation,c_m_s=self.c_m_s,**self._kwargs())
            result.append(self._product(roster,'route_a_iteration_%d'%n))
        return result

    def body(self,body_ref,*,stars=True):
        a=self.arrays(body_ref,('physical_positions_m','base_integrated_source_J'))
        for x in a.values():_real(x,'BODY_SOURCE_NONREAL')
        roster=self.rs.roster_body(a,self.stars if stars else None,c_m_s=self.c_m_s,**self._kwargs())
        return self._product(roster,'body_gas' if not stars else 'stars_plus_body_gas')

    def fs(self,updated_base_ref):
        a=self.arrays(updated_base_ref,('physical_positions_m','rho0','volume_weights_m3'))
        pos=_real(a['physical_positions_m'],'FS_POSITION_NONREAL').reshape(-1,3)
        rho=_real(a['rho0'],'FS_RHO_NONREAL');vol=_real(a['volume_weights_m3'],'FS_VOLUME_NONREAL')
        if rho.shape!=vol.shape or rho.size!=len(pos) or np.any(vol<0):raise ReconstructionError('FS_ARRAY_SHAPE_OR_VOLUME')
        J=(-self.c_m_s*self.c_m_s*rho*vol).reshape(-1)
        roster=self.rs.roster_body(dict(physical_positions_m=pos,base_integrated_source_J=J),self.stars,c_m_s=self.c_m_s,**self._kwargs())
        return self._product(roster,'fs_stars_plus_body_gas')

    def rotation(self,rotation_ref):
        a=self.arrays(rotation_ref,('rho0','volume_weights_m3','radial_nodes_m','z'))
        for x in a.values():_real(x,'ROTATION_SOURCE_NONREAL')
        shape=a['rho0'].shape
        if len(shape)!=3 or shape!=a['volume_weights_m3'].shape or shape!=a['z'].shape or a['radial_nodes_m'].shape!=(shape[0],) or np.any(a['volume_weights_m3']<0):
            raise ReconstructionError('ROTATION_SHAPE_OR_VOLUME')
        roster=self.rs.roster_rotation(a,self.stars,**self._kwargs())
        return self._product(roster,'feedback_v004_rotation_rings')

    def _manifest_gas(self,man):
        r=man['roster']
        if r.get('kind')!='registered_gas_columns':raise ReconstructionError('REGISTERED_GAS_MANIFEST_REQUIRED')
        a=self.arrays(r['arrays']);rec=r['record'];n=rec['n_columns']
        required={'gas_column_R_m','gas_column_rdr_m2','gas_present'}|{'gas_%s_%03d'%(t,i) for t in ('z','m') for i in range(n)}
        if set(a)!=required or n!=4*(len(self.edges)-1) or rec['M_s']!=self.M_s or rec['s_edges_kpc2']!=self.edges.tolist():
            raise ReconstructionError('MANIFEST_GAS_FIELDS_OR_CONFIG')
        R,w=self.rs.annulus_columns(self.edges,self.kpc_m)
        if not np.array_equal(a['gas_column_R_m'],R) or not np.array_equal(a['gas_column_rdr_m2'],w):raise ReconstructionError('MANIFEST_GL4_COLUMNS_DIFFER')
        present=a['gas_present']
        if present.shape!=(n,) or not np.isin(present,[0,1]).all():raise ReconstructionError('MANIFEST_PRESENT_INVALID')
        zs=[];ms=[]
        for i in range(n):
            z=_real(a['gas_z_%03d'%i],'GAS_Z_NONREAL');m=_real(a['gas_m_%03d'%i],'GAS_M_NONREAL')
            if z.ndim!=1 or m.shape!=z.shape or (not present[i] and len(z)):raise ReconstructionError('MANIFEST_GAS_ELEMENT_SHAPE')
            zs.append(z);ms.append(m)
        gas=self.rs.GasColumns(column_R_m=R,column_rdr_m2=w,present=present.astype(bool),elements_z=zs,elements_m=ms,**self._kwargs())
        if gas.record()!=rec:raise ReconstructionError('MANIFEST_GAS_RECORD_MISMATCH')
        return gas

    def offset(self,body_ref,accepted_manifest_ref):
        positive=self.body(body_ref,stars=False)
        man=self.json(accepted_manifest_ref);gas=self._manifest_gas(man)
        negative=self.rs.Roster(stars=None,gas=gas,provenance=dict(rule='route_a_manifest_gas_IT'))
        pm=positive.components[0]
        nm=np.concatenate(gas.elements_m)
        components=[dict(pm,role='body_gas',sign=1),dict(role='route_a_gas_IT',sign=-1,mass=float(np.sum(nm)),nonnegative=bool(np.all(nm>=0)))]
        return self._product(self.rb._DifferenceRoster(positive.roster,negative,False),'signed_offset',components)

    def expect_source(self,product,assertion_ref,field_path=('uv_tail','roster_digest')):
        rec=self.json(assertion_ref)
        for field in field_path:rec=rec[field]
        if rec!=product.source_sha256:raise ReconstructionError('RECONSTRUCTED_SOURCE_DIGEST_MISMATCH')
        product.source_digest_verified=True;product.source_assertion_pin=dict(assertion_ref)
        product.source_files=list(self.source_pins.values())
        return product

    def _check_factors(self,state,source):
        if state.empty:raise ReconstructionError('EMPTY_STATE_SOURCE_RULE_NOT_IMPLEMENTED')
        a=state.to_arrays()
        P=source.roster.radial_factors(a['kp'],self.jn.j0)
        F=source.roster.vertical_factors(a['kz'],self.c_m_s)
        if not np.array_equal(P,a['P']) or not np.array_equal(F,a['F']):raise ReconstructionError('RECONSTRUCTED_STATE_FACTORS_DIFFER')
        return True

    def accepted_manifest(self,manifest_ref):
        man=self.json(manifest_ref)
        if man.get('schema')!=self.rb.MANIFEST_SCHEMA or man.get('config_sha256')!=self.config['sha256']:
            raise ReconstructionError('ACCEPTED_MANIFEST_SCHEMA_OR_CONFIG')
        entry=man['state'];record=entry['record']
        if record.get('config_sha256')!=self.config['sha256'] or record.get('stage_kind')!='route_a' or record.get('i1t')!=man.get('i1t'):
            raise ReconstructionError('ACCEPTED_STATE_IDENTITY_MISMATCH')
        rr=record.get('roster_record')
        if not isinstance(rr,dict) or rr.get('stars')!=self.stars.record():raise ReconstructionError('ACCEPTED_REGISTERED_STARS_MISMATCH')
        gas=self._manifest_gas(man)
        roster=self.rs.Roster(stars=self.stars,gas=gas,provenance=rr['provenance'])
        if roster.record()!=rr:raise ReconstructionError('ACCEPTED_FULL_ROSTER_RECORD_MISMATCH')
        source=self._product(roster,'accepted_route_a')
        if source.source_sha256!=record.get('roster_digest'):raise ReconstructionError('ACCEPTED_FULL_SOURCE_DIGEST_MISMATCH')
        source.source_digest_verified=True;source.source_assertion_pin=dict(manifest_ref)
        state=self.lib.TailState.from_arrays(self.arrays(entry['arrays']),record,jn_provider=self.jn,expected_digest=entry['digest'])
        factors=self._check_factors(state,source)
        source.source_files=list(self.source_pins.values())
        return StateProduct(state,source,list(self.pins.values()),digest_verified=True,factors_reconstructed=factors)

    def rebuild_state(self,source,recipe_ref,expected_state_sha256=None,*,state_assertion_ref,state_field_path):
        """Static replay, never a solve; caller must budget the explicit grid."""
        recipe=self.json(recipe_ref)
        expected=_field(self.json(state_assertion_ref),state_field_path)
        if not I._hex(expected) or (expected_state_sha256 is not None and expected_state_sha256!=expected):
            raise ReconstructionError('STATE_ASSERTION_DIGEST_INVALID_OR_CONFLICTING')
        expected_state_sha256=expected
        if recipe.get('config_sha256')!=self.config['sha256']:raise ReconstructionError('REPLAY_RECIPE_CONFIG_MISMATCH')
        allowed={'signed_offset':{'offset'},'feedback_v004_rotation_rings':{'rfs_columns','le_columns','le_rotation'},
                 'fs_stars_plus_body_gas':{'fs_columns','fs_rotation'},'stars_plus_body_gas':{'fs_columns','fs_rotation'}}
        kinds={'route_a'} if source.role.startswith('route_a_iteration_') else allowed.get(source.role,set())
        if recipe.get('stage_kind') not in kinds:raise ReconstructionError('SOURCE_ROLE_STAGE_MISMATCH')
        for key in ('eps_certificate','lo_certificate'):
            if self.config[key]!=self.lib.TEST_ONLY_CERT:self._bytes(self.config[key])
        radii=self.arrays(recipe['eval_radii'],('eval_radii_m',))['eval_radii_m']
        state=self.lib.build(config=self.config,kept=recipe['kept'],roster=source.roster,
                gamma_eff=_positive(recipe['gamma_eff'],'GAMMA_INVALID'),c_m_s=self.c_m_s,eval_radii_m=radii,
                jn_provider=self.jn,i1t=recipe['i1t'],stage_kind=recipe['stage_kind'])
        if not I._hex(expected_state_sha256) or state.digest!=expected_state_sha256:raise ReconstructionError('REBUILT_STATE_DIGEST_MISMATCH')
        if state.record.get('roster_digest')!=source.source_sha256:raise ReconstructionError('REBUILT_SOURCE_DIGEST_MISMATCH')
        source.source_digest_verified=True;source.source_assertion_pin=dict(state_assertion_ref)
        factors=self._check_factors(state,source)
        source.source_files=list(self.source_pins.values())
        return StateProduct(state,source,list(self.pins.values()),digest_verified=True,factors_reconstructed=factors)


def _field(obj,path):
    if not isinstance(path,list) or not path or any(type(k) not in (str,int) for k in path):
        raise ReconstructionError('EXPLICIT_STATE_FIELD_PATH_REQUIRED')
    for k in path:obj=obj[k]
    return obj


def replay_state(descriptor_ref,*,allow_synthetic_fixture=False):
    """Re-execute byte-pinned descriptor; do not trust product boolean claims.

    Returns (reconstructor, StateProduct). This proves only the selected state;
    independent I1-T, own-call occurrence closure and point/custody joins remain.
    """
    if not isinstance(descriptor_ref,dict) or set(descriptor_ref)!={'path','sha256'} or not I._hex(descriptor_ref['sha256']):
        raise ReconstructionError('EXACT_DESCRIPTOR_PIN_REQUIRED')
    p=I.safe_path(descriptor_ref['path'])
    if p.stat().st_size>I.MAX_JSON_BYTES:raise ReconstructionError('DESCRIPTOR_TOO_LARGE')
    raw=p.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=descriptor_ref['sha256']:raise ReconstructionError('DESCRIPTOR_PIN_MISMATCH')
    d=I._strict_json(raw)
    if d.get('schema')!='DDO154_STATE_REPLAY_DESCRIPTOR_CX2V001':raise ReconstructionError('DESCRIPTOR_SCHEMA')
    r=SavedSourceReconstructor(d['context'],allow_synthetic_fixture=allow_synthetic_fixture)
    if d.get('operation')=='accepted_manifest':
        if set(d)!={'schema','context','operation','manifest'}:raise ReconstructionError('DESCRIPTOR_FIELDS')
        state=r.accepted_manifest(d['manifest'])
    elif d.get('operation')=='rebuild':
        if set(d)!={'schema','context','operation','source','recipe','state_assertion','state_field_path'}:raise ReconstructionError('DESCRIPTOR_FIELDS')
        s=d['source'];kind=s.get('kind')
        if kind=='route_a':
            if set(s)!={'kind','initial_rings','elements','relaxation','iteration'}:raise ReconstructionError('SOURCE_DESCRIPTOR_FIELDS')
            n=s['iteration']
            if type(n) is not int or n<0 or n>len(s['elements']):raise ReconstructionError('ROUTE_A_SOURCE_INDEX')
            source=r.route_a(s['initial_rings'],s['elements'],s['relaxation'])[n]
        elif kind in ('body','fs','rotation'):
            if set(s)!={'kind','arrays'}:raise ReconstructionError('SOURCE_DESCRIPTOR_FIELDS')
            source=getattr(r,kind)(s['arrays'])
        elif kind=='offset':
            if set(s)!={'kind','body','manifest'}:raise ReconstructionError('SOURCE_DESCRIPTOR_FIELDS')
            source=r.offset(s['body'],s['manifest'])
        else:raise ReconstructionError('SOURCE_DESCRIPTOR_KIND')
        state=r.rebuild_state(source,d['recipe'],state_assertion_ref=d['state_assertion'],state_field_path=d['state_field_path'])
    else:raise ReconstructionError('DESCRIPTOR_OPERATION')
    state.context_ref=dict(d['context']);state.descriptor_ref=dict(descriptor_ref)
    state.input_pins=list(r.pins.values())+[dict(descriptor_ref)]
    return r,state
