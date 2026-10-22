"""Independent saved-source/I1-T replay and current GQ/LO evidence assembly.

No solver, launch, discovery sweep or output mutation. The only rebuild is the
explicit, pinned reconstruction descriptor's static TailState replay. Numeric
checks do not authorize a certificate: point/configuration, own-call occurrence
and independently approved producer/packet-binding review are separate gates.
R5 pinned successor; production K128/M_s128. Full run admission remains separate.
"""
import hashlib
import importlib.util
import io
import math
from pathlib import Path
import sys
import numpy as np

H=Path(__file__).resolve().parent
PINS={
 'R':('reconstruction_cx2v003.py','b8471197027bd2f0511966713656893860dfb22cba18e8d799ed2cc89b7c3a50'),
 'L':('lo_producer_cx2v004.py','5db60d0f6db6d481e2f748b19bef08ce425f19a0e463d58727c184d633e03d51'),
 'G':('gq_producer_cx2v005.py','2832ceb95e1f4c4065963a50475b42cdb176744b824ae6a06f15c30db76441bd')}
def _module(key):
    name,sha=PINS[key];p=H/name
    if hashlib.sha256(p.read_bytes()).hexdigest()!=sha:raise ValueError('DEPENDENCY_PIN_MISMATCH')
    sp=importlib.util.spec_from_file_location('cx2_current_'+key,p)
    m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m);return m
R,L,G=(_module(k) for k in ('R','L','G'))
C=L.CU
I1T_SEED=20261018
I1T_SAMPLES=4096
I1T_RTOL=1e-12

def _real(x,label):
    a=np.asarray(x)
    if a.dtype.hasobject or not np.isfinite(a).all() or (np.iscomplexobj(a) and np.any(a.imag!=0)):
        raise ValueError(label)
    return a.real

def _field(obj,path):
    return R._field(obj,path)

def _pin_equal(a,b):
    return (a['sha256']==b['sha256'] and C.allowed_path(a['path'])==C.allowed_path(b['path']))

def _gas_equal(a,b):
    if a.record()!=b.record():return False
    return all(np.array_equal(x,y) for x,y in zip(a.elements_z+a.elements_m,b.elements_z+b.elements_m))

def _source(r,s):
    kind=s['kind']
    if kind=='route_a':
        if set(s)!={'kind','initial_rings','elements','relaxation','iteration'}:raise ValueError('SOURCE_FIELDS')
        n=s['iteration']
        if type(n) is not int or n<0 or n>len(s['elements']):raise ValueError('SOURCE_ITERATION')
        return r.route_a(s['initial_rings'],s['elements'][:n],s['relaxation'])[n]
    if kind in ('body','fs','rotation'):
        if set(s)!={'kind','arrays'}:raise ValueError('SOURCE_FIELDS')
        return getattr(r,kind)(s['arrays'])
    if kind=='offset':
        if set(s)!={'kind','body','manifest'}:raise ValueError('SOURCE_FIELDS')
        return r.offset(s['body'],s['manifest'])
    raise ValueError('SOURCE_KIND')

def _source_archives(r,s):
    if s['kind']=='route_a':return [s['initial_rings']]+s['elements'][:s['iteration']]
    if s['kind']=='offset':return [s['body'],s['manifest'],r.json(s['manifest'])['roster']['arrays']]
    return [s['arrays']]

def _selected_array(r,selector):
    if set(selector)!={'ref','key'}:raise ValueError('ARRAY_SELECTOR_FIELDS')
    raw=r._bytes(selector['ref'])
    if selector['key'] is None:
        a=np.load(io.BytesIO(raw),allow_pickle=False)
        if not isinstance(a,np.ndarray):raise ValueError('NPY_REQUIRED')
    else:
        a=r.arrays(selector['ref'],(selector['key'],))[selector['key']]
    if a.dtype.hasobject or not np.isfinite(a).all():raise ValueError('PACKET_ARRAY_NONFINITE')
    return a

def _scalar_packet(r,selector,n):
    a=_selected_array(r,selector)
    # Exact scalar-lapse component convention; no silent dropped tensor entries.
    if a.shape!=(n,10,1) or np.any(a[:,1:,:]!=0):raise ValueError('SCALAR_LAPSE_PACKET_REQUIRED')
    return a[:,0,0]

def _gas_transform(r,s,waves):
    kind=s['kind'];rs=r.rs
    if kind=='route_a':
        a=r.arrays(s['initial_rings'],('R','z','m'))
        t=rs.packet_transform(a,waves,'prep_analytic_j0',c_m_s=r.c_m_s,j0=r.jn.j0)
        coeff=[1.]
        for _ in range(s['iteration']):coeff=[(1-s['relaxation'])*c for c in coeff]+[s['relaxation']]
        t=coeff[0]*t
        for c,ref in zip(coeff[1:],s['elements']):
            e=r.arrays(ref,('positions_m','integrated_J'))
            t=t+c*rs.packet_transform(e,waves,'physical_source_fourier')
        return t,'route_a_mixture:prep_analytic_j0+physical_source_fourier'
    if kind in ('body','fs'):
        a=r.arrays(s['arrays'])
        pos=_real(a['physical_positions_m'],'SOURCE_POSITION').reshape(-1,3)
        if kind=='body':J=_real(a['base_integrated_source_J'],'SOURCE_J').reshape(len(pos),-1)[:,0]
        else:J=(-r.c_m_s*r.c_m_s*_real(a['rho0'],'SOURCE_RHO')*_real(a['volume_weights_m3'],'SOURCE_VOLUME')).reshape(-1)
        return rs.packet_transform(dict(positions_m=pos,integrated_J=J),waves,'offset_cartesian_v003'),'offset_cartesian_v003'
    if kind=='rotation':
        a=r.arrays(s['arrays']);m=np.sum(a['rho0']*a['volume_weights_m3'],axis=1)
        el=dict(R=np.repeat(a['radial_nodes_m'],m.shape[1]),z=a['z'][:,0,:].reshape(-1),m=m.reshape(-1))
        return rs.packet_transform(el,waves,'feedback_ring_j0_v004',c_m_s=r.c_m_s,j0=r.jn.j0),'feedback_ring_j0_v004'
    raise ValueError('TRANSFORM_KIND')

def _compare(a,b,kind):
    a=np.asarray(a);b=np.asarray(b)
    if a.shape!=b.shape or a.ndim!=1 or not a.size or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError('I1T_SHAPE_OR_NONFINITE')
    scale=float(np.max(np.abs(b)));err=float(np.max(np.abs(a-b)))
    if not math.isfinite(scale) or not math.isfinite(err):raise ValueError('I1T_NORM_NONFINITE')
    rel=err/scale if scale>0 else (0. if err==0 else None)
    ok=rel is not None and math.isfinite(rel) and rel<=I1T_RTOL
    return dict(kind=kind,n=len(a),max_rel=rel,rtol=I1T_RTOL,packet_scale=scale,max_abs_difference=err,verdict='PASS' if ok else 'FAIL')

def compute_i1t(reconstruction_ref,packet_ref,*,allow_synthetic_fixture=False):
    """Recompute the registered seeded <=4096-node represented-packet check.

    Packet descriptor: schema DDO154_I1T_REPLAY_CX2V001, reconstruction ref,
    source (exact reconstruction source selector), waves {ref,key}, gas_packet
    {ref,key}; nonoffset stars {packet:{ref,key},gauss_order:{ref,field_path}}.
    Offset instead carries route_a_source and route_a_packet; body and route-A
    gas checks are both required. The two components are never normalized by
    the signed difference. An approval review must bind these packet selectors
    and star quadrature to the actual stage's outputs/preparation arguments.
    """
    r,p=R.replay_state(reconstruction_ref,allow_synthetic_fixture=allow_synthetic_fixture);d=r.json(packet_ref)
    if d.get('schema')!='DDO154_I1T_REPLAY_CX2V001' or not _pin_equal(d['reconstruction'],reconstruction_ref):
        raise ValueError('I1T_DESCRIPTOR_RECONSTRUCTION_MISMATCH')
    s=d['source'];rebuilt=_source(r,s)
    if rebuilt.source_sha256!=p.source.source_sha256:raise ValueError('I1T_SOURCE_DIGEST_MISMATCH')
    waves=_real(_selected_array(r,d['waves']),'WAVES_NONREAL')
    if waves.ndim!=2 or waves.shape[1]!=3 or len(waves)==0:raise ValueError('WAVES_SHAPE')
    idx=np.sort(np.random.default_rng(I1T_SEED).choice(len(waves),size=min(I1T_SAMPLES,len(waves)),replace=False))
    w=waves[idx];checks=[];refs=_source_archives(r,s)+[d['waves']['ref'],d['gas_packet']['ref']]
    packet=_scalar_packet(r,d['gas_packet'],len(waves))[idx]
    if s['kind']=='offset':
        if set(d)!={'schema','reconstruction','source','waves','gas_packet','route_a_source','route_a_packet'}:raise ValueError('I1T_DESCRIPTOR_FIELDS')
        a=dict(kind='body',arrays=s['body']);t,kind=_gas_transform(r,a,w)
        checks.append(_compare(t,packet,'offset_body:'+kind))
        ra=d['route_a_source']
        if ra.get('kind')!='route_a':raise ValueError('OFFSET_ROUTE_A_SOURCE_REQUIRED')
        neg=_source(r,ra)
        if not _gas_equal(neg.roster.gas,p.source.roster.b.gas):raise ValueError('OFFSET_ROUTE_A_COMPONENT_MISMATCH')
        t,kind=_gas_transform(r,ra,w)
        checks.append(_compare(t,_scalar_packet(r,d['route_a_packet'],len(waves))[idx],'offset_route_a:'+kind))
        refs+=_source_archives(r,ra)+[d['route_a_packet']['ref']]
    else:
        if set(d)!={'schema','reconstruction','source','waves','gas_packet','stars'}:raise ValueError('I1T_DESCRIPTOR_FIELDS')
        t,kind=_gas_transform(r,s,w);checks.append(_compare(t,packet,kind))
        star=d['stars'];q=star['gauss_order'];order=_field(r.json(q['ref']),q['field_path'])
        if type(order) is not int or not 1<=order<=256:raise ValueError('STAR_GAUSS_ORDER')
        rings=r.rs.stars_gl4_rings(r.profile,'DDO154',kpc_m=r.kpc_m,solar_mass_kg=r.solar_mass_kg,
                gauss_order=order,radial_surface=r.modules['forward'].radial_surface)
        t=r.rs.packet_transform(rings,w,'prep_analytic_j0',c_m_s=r.c_m_s,j0=r.jn.j0)
        checks.append(_compare(t,_scalar_packet(r,star['packet'],len(waves))[idx],'fixed_stars:prep_analytic_j0'))
        refs+=[star['packet']['ref'],q['ref']]
    out=dict(schema='DDO154_I1T_COMPUTED_CX2V001',status='TESTED',verdict='PASS' if all(x['verdict']=='PASS' for x in checks) else 'FAIL',
        reconstruction=reconstruction_ref,packet_descriptor=packet_ref,state_sha256=p.state_sha256,source_sha256=p.source.source_sha256,
        seed=I1T_SEED,samples=len(idx),wave_count=len(waves),sample_indices=C.array_record(idx),checks=checks,
        source_files=list({(x['path'],x['sha256']):(dict(x)) for x in refs}.values()),producer=C.pin(__file__),
        certificate_status='UNAVAILABLE',point_status='INCOMPLETE',
        blockers=['POINT_OWN_CALL_OCCURRENCE_AND_INDEPENDENT_PACKET_BINDING_REVIEW_REQUIRED'])
    return r,p,out

def verify_gas(r,gas):
    """Actual active-column premises; stars cannot rescue a zero gas denominator."""
    Rm,rd=r.rs.annulus_columns(r.edges,r.kpc_m)
    if gas is None or gas.M_s!=r.M_s or not np.array_equal(gas.s_edges_kpc2,r.edges) or gas.kpc_m!=r.kpc_m:
        raise ValueError('SOURCE_GEOMETRY_CONFIG')
    if not np.array_equal(gas.column_R_m,Rm) or not np.array_equal(gas.column_rdr_m2,rd):raise ValueError('SOURCE_GL4_COLUMNS')
    n=len(Rm)
    if len(gas.elements_z)!=n or len(gas.elements_m)!=n or np.asarray(gas.present).shape!=(n,):raise ValueError('SOURCE_COLUMN_COUNT')
    masses=[];positive=True
    for present,z,m in zip(gas.present,gas.elements_z,gas.elements_m):
        z=_real(z,'SOURCE_Z');m=_real(m,'SOURCE_MASS')
        if z.ndim!=1 or m.shape!=z.shape or (not present and len(m)):raise ValueError('SOURCE_COLUMN_CONTENT')
        if np.any(np.abs(z)>r.config['domain']['z_src_max_kpc']*r.kpc_m):raise ValueError('SOURCE_Z_OUTSIDE_DOMAIN')
        positive=positive and bool(np.all(m>=0));masses.extend(map(float,m))
    mass=math.fsum(masses)
    if not math.isfinite(mass):raise ValueError('SOURCE_MASS_OVERFLOW')
    # Gas-only sigma carries mass/(2 pi r dr); P is the quadrature integral.
    zero=complex((gas.radial_factors(np.array([0.]),r.jn.j0)@gas.vertical_factors(np.array([0.])).T)[0,0])
    actual=zero.real
    if not math.isfinite(actual) or zero.imag!=0:raise ValueError('SOURCE_ZERO_MODE_INVALID')
    return dict(nonnegative_masses=positive,analytic_mass_kg=mass,actual_zero_mode_mass_kg=actual,
                positive_gas_zero_mode=bool(positive and mass>0 and actual>0),columns=n)

def verify_product(r,p):
    """Re-derive all facts; never trust the reconstruction object's booleans."""
    a=p.state.to_arrays();rec=p.state.record
    st=r.lib.TailState.from_arrays(a,rec,jn_provider=r.jn,expected_digest=p.state_sha256)
    digest=p.source.roster.digest()
    if st.digest!=p.state_sha256 or digest!=p.source.source_sha256 or rec.get('roster_digest')!=digest:raise ValueError('ACTUAL_STATE_SOURCE_DIGEST')
    if not np.array_equal(p.source.roster.radial_factors(a['kp'],r.jn.j0),a['P']):raise ValueError('ACTUAL_P_MISMATCH')
    if not np.array_equal(p.source.roster.vertical_factors(a['kz'],r.c_m_s),a['F']):raise ValueError('ACTUAL_F_MISMATCH')
    if hasattr(p.source.roster,'a'):
        gas={'body':verify_gas(r,p.source.roster.a.gas),'route_a':verify_gas(r,p.source.roster.b.gas)}
        positive=all(x['nonnegative_masses'] for x in gas.values());nonnegative=False
    else:
        gas={'gas':verify_gas(r,p.source.roster.gas)};positive=gas['gas']['nonnegative_masses'];nonnegative=positive
    return dict(state=dict(state_sha256=st.digest,source_sha256=digest,stage_kind=rec['stage_kind'],nonnegative_masses=nonnegative),
        state_digest_verified=True,source_digest_verified=True,factors_reconstructed=True,
        factor_arrays_sha256=C.digest({k:C.array_record(a[k]) for k in ('P','F')}),gas=gas,
        positive_components_verified=positive)

def verify_point(spec,r,p,details):
    if r.profile['galaxies']['DDO154']!=details['geometry']['profile']:raise ValueError('POINT_PROFILE_MISMATCH')
    if r.c_m_s!=L.PR.CC.C or r.kpc_m!=r.lib.KPC_M or r.solar_mass_kg!=1.98847e30:raise ValueError('POINT_UNIT_MISMATCH')
    if p.state.record['gamma_eff']!=spec['physical']['common_scale_s']*spec['physical']['gamma']:raise ValueError('POINT_GAMMA_MISMATCH')
    check=L.V2.validate_current_config(spec,p.state.record,p.state.to_arrays(),r.lib)
    if not check['certificate_slots_bound']:raise ValueError('POINT_CERTIFICATE_SLOTS_UNBOUND')
    return check

ROLE_PATHS={'accepted_route_a':['state','digest'],'route_a_current':['payload','state_digest'],
 'route_a_next':['payload','next_state_digest'],'route_a_return':['result','uv_tail','boundary_state_digest_at_return'],
 'stage_tail':['uv_tail','state_digest']}

def verify_occurrence(spec,r,p,occurrence):
    """One exact own-call occurrence, not completeness of the full call graph."""
    o=occurrence;role=o['role'];path=o['state_field_path']
    if path!=ROLE_PATHS.get(role):raise ValueError('OCCURRENCE_FIELD_NOT_WHITELISTED')
    root=C.allowed_path(o['run_root'])
    for k in ('call_spec_ref','call_result_ref','call_finish_ref','assertion_ref'):
        if not C.allowed_path(o[k]['path']).is_relative_to(root):raise ValueError('CROSS_RUN_OCCURRENCE')
    saved=r.json(o['call_spec_ref']);result=r.json(o['call_result_ref']);finish=r.json(o['call_finish_ref'])
    if saved!=spec or result.get('call_spec_sha256')!=o['call_spec_ref']['sha256'] or result.get('driver_sha256')!=C.DRIVER_SHA:
        raise ValueError('CALL_POINT_BYTE_IDENTITY')
    if finish.get('result_sha256')!=o['call_result_ref']['sha256']:raise ValueError('CALL_FINISH_RESULT_PIN')
    d=R.I.Discovery();d.fresh_scope(spec,result,finish,result.get('stage_records',[]))
    if not d.fresh_completed:raise ValueError('CALL_NOT_FRESH_COMPLETED_NO_RETRY')
    assertion=r.json(o['assertion_ref'])
    if _field(assertion,path)!=p.state_sha256:raise ValueError('OCCURRENCE_STATE_MISMATCH')
    desc=r.json(p.descriptor_ref)
    if desc['operation']=='accepted_manifest' and not _pin_equal(desc['manifest'],result['uv_tail']['manifest']):raise ValueError('ACCEPTED_MANIFEST_OWN_CALL_JOIN')
    if desc['operation']=='rebuild':
        if not _pin_equal(desc['state_assertion'],o['assertion_ref']) or desc['state_field_path']!=path:raise ValueError('REPLAY_ASSERTION_JOIN')
    elif role=='accepted_route_a':
        if not _pin_equal(desc['manifest'],o['assertion_ref']):raise ValueError('MANIFEST_ASSERTION_JOIN')
    elif role not in ('stage_tail','route_a_return'):raise ValueError('INHERITED_MANIFEST_ROLE')
    if role=='accepted_route_a':
        if not _pin_equal(result['uv_tail']['manifest'],o['assertion_ref']):raise ValueError('CALL_MANIFEST_JOIN')
    elif role=='stage_tail':
        matches=[x for x in result['uv_tail']['stage_records'] if x['stage']==o['stage'] and x['finish_sha256']==o['assertion_ref']['sha256'] and x['state_digest']==p.state_sha256]
        stages=[x for x in result['stage_records'] if x['name']==o['stage'] and x.get('executed') is True]
        if len(matches)!=1 or len(stages)!=1:raise ValueError('CALL_STAGE_JOIN')
        argv=stages[0]['argv']
        if argv.count('--outdir')!=1 or C.allowed_path(Path(argv[argv.index('--outdir')+1])/'finish.json')!=C.allowed_path(o['assertion_ref']['path']):raise ValueError('CALL_STAGE_PATH_JOIN')
    else:
        out=result['route_a_outcome'];ar=dict(path=out['result_path'],sha256=out['result_sha256']);attempt=r.json(ar)
        if role=='route_a_return':
            if not _pin_equal(ar,o['assertion_ref']):raise ValueError('CALL_RETURN_JOIN')
        else:
            uv=attempt['result']['uv_tail'];sc=uv['sidecar'];name=Path(o['assertion_ref']['path']).name
            n=o['iteration']-(1 if role=='route_a_next' else 0)
            if type(n) is not int or n<0 or name!='iteration_%04d.json'%n or sc['files'].get(name)!=o['assertion_ref']['sha256']:
                raise ValueError('CALL_ITERATION_JOIN')
            if C.allowed_path(Path(sc['directory'])/name)!=C.allowed_path(o['assertion_ref']['path']):raise ValueError('CALL_ITERATION_PATH')
            dd=R.I.Discovery();dd.sidecar(uv,ar)
            structural=[b for b in dd.blockers if b['code']!='ROUTE_A_STATE_SOURCE_RECONSTRUCTION_UNAVAILABLE']
            if structural:raise ValueError('CALL_ITERATION_HISTORY_INVALID')
    return dict(occurrence=o,state_sha256=p.state_sha256,source_sha256=p.source.source_sha256,
                actual_stage_kind=p.state.record['stage_kind'],fresh_completed=True,complete_call_inventory=False)

def _approved(review_ref,approved_reviews,producer_shas,packet_ref,reconstruction_ref,occurrence,details):
    if C.sha(__file__) not in producer_shas:raise ValueError('CURRENT_SOURCE_PRODUCER_NOT_APPROVED')
    if review_ref is None or review_ref['sha256'] not in approved_reviews:raise ValueError('PACKET_BINDING_REVIEW_UNAVAILABLE')
    review=C.read_pin(review_ref)
    expected={'schema':'DDO154_CURRENT_SOURCE_REVIEW_CX2V001','verdict':'APPROVED','distinct_from_producer_lane':True,
       'point_sha256':details['point_sha256'],'custody_sha256':details['custody_sha256'],
       'producer':C.pin(__file__),'reconstruction':reconstruction_ref,'packet_descriptor':packet_ref,'occurrence_sha256':C.digest(occurrence)}
    if any(review.get(k)!=v for k,v in expected.items()) or not review.get('reviewer_lane') or review.get('packet_selectors_and_preparation_arguments_verified') is not True:
        raise ValueError('PACKET_BINDING_REVIEW_SCOPE')
    return review

def assemble_current(spec,reconstruction_ref,packet_ref,occurrence,*,uniform_gq_ref=None,review_ref=None,
                     approved_review_sha256=(),approved_producer_sha256=(),approved_uniform_producer_sha256=()):
    """Return numerical evidence and gated source/GQ exports; never caller booleans.

    Full inventory completeness and LO row/rho/readout-policy proof are separate.
    Any absent evidence is typed UNAVAILABLE, with no production PASS emitted.
    """
    out=dict(schema='DDO154_CURRENT_EVIDENCE_CX2V001',status='UNTESTED',verdict='UNAVAILABLE',certificate_status='UNAVAILABLE',
             point_status='INCOMPLETE',production_admissible=False,complete_call_inventory=False,blockers=[],producer=C.pin(__file__))
    try:
        details=C.derive_details(spec=spec);out.update(point_sha256=details['point_sha256'],custody_sha256=details['custody_sha256'])
        r,p,i1t=compute_i1t(reconstruction_ref,packet_ref);v=verify_product(r,p)
        out.update(status='TESTED',reconstruction_checks=v,i1t=i1t,state=v['state'],input_pins=p.input_pins,dependency_pins=p.source.dependency_pins)
        if i1t['verdict']!='PASS':raise ValueError('COMPUTED_I1T_FAILED')
        out['point_validation']=verify_point(spec,r,p,details)
        out['occurrence_receipt']=verify_occurrence(spec,r,p,occurrence)
        for ref in i1t['source_files']:
            if not C.allowed_path(ref['path']).is_relative_to(C.allowed_path(occurrence['run_root'])):raise ValueError('CROSS_RUN_SOURCE_OR_PACKET_ARCHIVE')
        _approved(review_ref,approved_review_sha256,approved_producer_sha256,packet_ref,reconstruction_ref,occurrence,details)
        if uniform_gq_ref is None:raise ValueError('UNIFORM_GQ_PROOF_UNAVAILABLE')
        uq=C.read_pin(uniform_gq_ref)
        if uq.get('producer',{}).get('sha256') not in approved_uniform_producer_sha256:raise ValueError('UNIFORM_GQ_PRODUCER_NOT_APPROVED')
        C.read_pin(uq['producer'],document=False)
        wanted={'schema':'UNT_CALIBRATION_POINT_PROOF_CX2V001','gate':'GQ','status':'TESTED','verdict':'PASS','point_sha256':details['point_sha256'],
            'custody_sha256':details['custody_sha256'],'geometry_sha256':details['custody']['geometry_sha256'],
            'method':'GEOMETRY_UNIFORM_COLUMN_BOUND','all_columns_included':True,'all_production_kperp_nodes':True,
            'M_s':r.M_s,'M_s_doubled':2*r.M_s,'quadrature':spec['numerics']['uv_tail']['quadrature'],
            'K_big_inverse_kpc':spec['numerics']['uv_tail']['outer']['K_big_inverse_kpc']}
        if any(uq.get(k)!=val for k,val in wanted.items()):raise ValueError('UNIFORM_GQ_SCOPE')
        b=uq['max_column_difference_over_analytic_Pi0'];z=uq['max_zero_mode_relative_error']
        if any(type(x) not in (int,float) or not math.isfinite(x) or x<0 for x in (b,z)) or z>=1 or b/(1-z)>1e-12:raise ValueError('UNIFORM_GQ_NUMERIC')
        proof=dict(schema='UNT_CALIBRATION_POINT_PROOF_CX2V001',status='TESTED',verdict='PASS',point_sha256=details['point_sha256'],
            custody_sha256=details['custody_sha256'],producer=C.pin(__file__),state=v['state'],GQ_uniform_proof_sha256=uniform_gq_ref['sha256'],
            uniform_proof=uniform_gq_ref,source_reconstruction=reconstruction_ref,i1t=packet_ref,review=review_ref)
        if 'body' in v['gas']:
            if not v['positive_components_verified']:raise ValueError('SIGNED_COMPONENT_MASS_NEGATIVE')
            mb=v['gas']['body']['analytic_mass_kg'];ma=v['gas']['route_a']['analytic_mass_kg'];bound=G.signed_bound(b,z,mb,ma)
            if bound['verdict']!='PASS':raise ValueError('SIGNED_GQ_FINITE_BOUND_UNAVAILABLE')
            proof.update(gate='GQ_SIGNED',method='TV_BOUND_WITH_SIGNED_P0',normalization='ABS_SIGNED_ZERO_MODE',
                body_mass_kg=mb,route_a_mass_kg=ma,component_mass_sum_kg=bound['total_variation_mass'],
                P0_abs_signed_mass_lower_bound_kg=bound['denominator_lower_bound_mass'],max_difference_over_signed_P0_bound=bound['conservative_bound'],
                positive_components_verified=True,signed_offset_policy=G.policy())
        else:
            if not v['gas']['gas']['positive_gas_zero_mode']:raise ValueError('POSITIVE_GAS_ZERO_MODE_UNAVAILABLE')
            proof.update(gate='GQ_CURRENT_PREMISES',method='RECONSTRUCTED_POSITIVE_GAS_SOURCE',
                nonnegative_masses_verified=True,positive_total_zero_mode_verified=True,positive_gas_zero_mode_verified=True,
                actual_gas_zero_mode_mass_kg=v['gas']['gas']['actual_zero_mode_mass_kg'],max_difference_over_P0_bound=b/(1-z))
        out.update(verdict='SOURCE_EVIDENCE_READY',certificate_status='CURRENT_SOURCE_GQ_AVAILABLE',current_gq_proof=proof,
            identity=details['identity'],custody=details['custody'],source_files=i1t['source_files'],factor_arrays_sha256=v['factor_arrays_sha256'],
            blockers=['LO_ROW_POLICY_FULL_RHO_AND_COMPLETE_CALL_INVENTORY_STILL_REQUIRED'])
    except (OSError,ValueError,TypeError,KeyError,AttributeError,OverflowError) as exc:
        out['blockers'].append(str(exc))
    return out

def export_lo_source(spec,reconstruction_ref,packet_ref,occurrence,tail_state_refs,**kwargs):
    """Adapt successful independently gated evidence to LO v003 source schema.

    Re-runs assemble_current; no caller evidence booleans are accepted. LO
    additionally requires this module's bytes in its trusted producer list.
    Rehashes and restores the exact exported TailState before returning.
    """
    evidence=assemble_current(spec,reconstruction_ref,packet_ref,occurrence,**kwargs)
    if evidence.get('certificate_status')!='CURRENT_SOURCE_GQ_AVAILABLE':raise ValueError('SOURCE_EVIDENCE_UNAVAILABLE')
    rec=C.read_pin(tail_state_refs['record']);raw=C.read_pin(tail_state_refs['arrays'],document=False)
    with np.load(io.BytesIO(raw),allow_pickle=False) as f:a={k:f[k] for k in f.files}
    U,_,_=L.PR.CC.uvt_modules();U.TailState.from_arrays(a,rec,expected_digest=evidence['state']['state_sha256'])
    pf=C.digest({k:C.array_record(a[k]) for k in ('P','F')})
    if pf!=evidence['factor_arrays_sha256']:raise ValueError('EXPORTED_PF_MISMATCH')
    return dict(schema='UNT_POINT_SOURCE_RECONSTRUCTION_CX2V001',status='TESTED',verdict='PASS',producer=C.pin(__file__),
        identity=evidence['identity'],custody=evidence['custody'],state=evidence['state'],tail_state=tail_state_refs,
        factor_arrays_sha256=pf,source_files=evidence['source_files'],complete_source_files=True,i1t_verdict='PASS',
        current_gq=evidence['current_gq_proof'],occurrence_receipt=evidence['occurrence_receipt'],
        scope='One verified source/state occurrence only; full call inventory and LO row policy/rho remain separate.')
