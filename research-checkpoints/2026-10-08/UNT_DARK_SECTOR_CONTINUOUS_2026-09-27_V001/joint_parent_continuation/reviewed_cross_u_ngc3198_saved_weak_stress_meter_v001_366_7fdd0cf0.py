"""Guarded CLOSED V006 weak-source meter; no producer imports or metric solves."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, ast, hashlib, json, math, os, time
AUTHOR_DRAFT = True
BASE = Path(__file__).resolve().parent
STEM = 'CROSS_U_NGC3198_SAVED_WEAK_STRESS_METER_V001'
PARENT = 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006'
PINS = {'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006.md': 'acaca99c1c9c6fef56b50f1daf1b24c7d154f41f8fe53482797aa7f76e354e32', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_00148_FINAL.npz': 'ce35318b55b6f6afc7f225154aec7deb1587887a912b38962a751d9db97fa6fc', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_00148_FINAL.npz.COMMIT.json': 'e14fc7e7268207cb6abb3de025c2a79abf2112bda88da8d10e4e92ddeb6a6ede', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_E1em05_HI0_H20_CASE.json': 'a15aac98b954c86af73b85be7c8498ecec3b70da60553837353c4bfd21cab599', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_MANIFEST.json': '08252627c9809538690cac22f51fdf2a83606c016e7f731c87f1dfa2c979533b', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_RECEIPT.json': '581605c923df95b6008ccf0fabe7ce1fc7ce7533e5d7cd2b2b51e36d90899b3f', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_REPORT.md': '71e44896cafeb813f3d4676c285c29e7f6d63ccabf66634a2567ea98a4bc0d5a', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_RESULT.json': 'd470f406ec2279c9631f8e3e3c46a9e0d862f2a1691e1af6851b80aa871f3ff8', 'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76', 'CROSS_U_NGC3198_NONLINEAR_DISK_V001_MANIFEST.json': '65cb05b3aba084bde5fe75015e0a546c0c116a5a7906e7f647a5f2232c206683', 'CROSS_U_STATIC_HILBERT_STRESS_AND_LEADING_LENSING_INTERFACE_V001.md': '6844c982d0c017350d85731f3f58bf8b4167c860ee52f8bdd238ceef1fdcd68b', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'cross_u_ngc3198_nonlinear_disk_v001.py': 'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1'}
PROTOCOL_SHA = 'f7bcf098c776eca248f4c80ebcdbca526e221db0bfefeee537ccf81cd647bc87'
TOL = 1e-11
ORDERS = (2, 3)
A0, KPC, LIGHT = 1.0059833281731022e-10, 3.085677581491367e19, 299792458.
KB, C, ELL, GC = .02, 1.98, .1, 3*math.pi/8
B0 = A0*KPC/LIGHT**2
PHYSICAL = {k: False for k in ('full_metric', 'lensing', 'force_correction', 'refinement', 'stability', 'exterior_match', 'physical_stress_bound', 'parameter_adoption')}
np = None
MERGED, CREATED, RAW, RECORDS, FLAGS, CONTEXT = {}, {}, {}, [], [], {}
OWNER = None
ORDINAL = 0

def now(): return datetime.now(timezone.utc).isoformat()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def encode(x): return (json.dumps(x, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
def load(n): return json.loads((BASE/n).read_text())
def bind(n, h):
    p = (BASE/n).resolve()
    assert isinstance(h, str) and len(h) == 64 and sha(p) == h, str(p)
    assert str(p) not in MERGED or MERGED[str(p)] == h
    MERGED[str(p)] = h

def parent():
    for n, h in PINS.items(): bind(n, h)
    bind(STEM+'.md', PROTOCOL_SHA)
    rc, m, result = (load(PARENT+s) for s in ('_RECEIPT.json', '_MANIFEST.json', '_RESULT.json'))
    assert rc['status'] == 'CLOSED' and rc['owner'] == m['owner'] and result['manifest'] == m
    owner = rc['owner']
    assert owner['owner'] == 'root' and type(owner['pid']) is int and owner['pid'] > 0 and rc['closed'] > owner['started']
    assert owner['source_sha256'] == PINS['cross_u_ngc3198_native_elimination_recovery_v006.py']
    assert rc['input_sha256'] == m['input_sha256'] and rc['result_sha256'] == PINS[PARENT+'_RESULT.json']
    for k in ('input_sha256', 'output_sha256'):
        for n, h in rc[k].items(): bind(n, h)
    assert len(result['cases']) == 1 and not any(result['qualification'].values())
    case = load(PARENT+'_E1em05_HI0_H20_CASE.json')
    assert case == result['cases'][0] and case['identity']['case'] == 'E1em05_HI0_H20'
    assert case['status'] == 'CONVERGED' and not case['readout_qualified'] and not any(case['physical_flags'].values())
    identity = case['identity']
    assert identity['eps'] == 1e-5 and identity['grid_shape'] == [65, 87, 45]
    assert identity['source_sha256'] == PINS['cross_u_ngc3198_nonlinear_disk_v001.py']
    final = [r for r in case['own_checkpoints'] if r['metadata'].get('kind') == 'final_state']
    assert len(final) == 1
    rec = final[0]
    assert rec['file'] == PARENT+'_00148_FINAL.npz'
    assert load(rec['commit_file']) == {k: v for k, v in rec.items() if k not in ('commit_file', 'commit_sha256')}
    assert rc['output_sha256'][rec['file']] == rec['sha256'] and rc['output_sha256'][rec['commit_file']] == rec['commit_sha256']
    md = rec['metadata']
    assert md['identity'] == identity and md['history'] == case['history'] and md['status'] == case['status'] and md['owner'] == owner
    assert md['schema'] == {k: dict(shape=identity['grid_shape'], dtype='float64', finite=True) for k in ('state', 'residual', 'pre')}
    fixed = load('CROSS_U_NGC3198_NONLINEAR_DISK_V001_MANIFEST.json')['fixed']
    assert fixed['Hunit'] == identity['Hunit'] and len(case['rows']) == 43
    return case, rec, fixed

def publish(n, x):
    raw = encode(x); p = BASE/n
    with p.open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
    p.chmod(0o444); assert p.read_bytes() == raw; CREATED[n] = sha(p)
    return CREATED[n]

def checkpoint(tag, arrays, meta, failed=False):
    schema = {n: dict(shape=list(a.shape), dtype=str(a.dtype), finite=bool(np.isfinite(a).all())) for n, a in arrays.items()}
    assert failed or all(d['finite'] for d in schema.values())
    text = encode(dict(meta, schema=schema, owner=OWNER, failed=failed, physical_flags=PHYSICAL)).decode()
    md = json.loads(text); p = BASE/f'{STEM}_{len(RECORDS):03d}_{tag}.npz'
    with p.open('xb') as f: np.savez_compressed(f, metadata=text, **arrays); f.flush(); os.fsync(f.fileno())
    p.chmod(0o444); CREATED[p.name] = sha(p)
    rec = dict(file=p.name, sha256=CREATED[p.name], metadata=md)
    cn = p.name+'.COMMIT.json'; ch = publish(cn, rec)
    rec = dict(rec, commit_file=cn, commit_sha256=ch); RECORDS.append(rec)
    with np.load(p, allow_pickle=False) as z:
        assert str(z['metadata']) == text and set(z.files) == set(arrays)|{'metadata'}
        for n, a in arrays.items(): assert np.array_equal(z[n], a, equal_nan=True)
    return rec

def check(name, actual, expected):
    global ORDINAL
    ORDINAL += 1; CONTEXT.update(control=name, ordinal=ORDINAL)
    a, b = np.asarray(actual), np.asarray(expected)
    RAW[f'control_{ORDINAL:03d}_{name}_actual'] = a.copy(); RAW[f'control_{ORDINAL:03d}_{name}_expected'] = b.copy()
    assert np.isfinite(a).all() and np.isfinite(b).all()
    error = float(np.max(abs(a-b))/max(1., float(np.max(abs(a))), float(np.max(abs(b)))))
    FLAGS.append(dict(name=name, ordinal=ORDINAL, error=error, tolerance=TOL, passed=error <= TOL))

def recheck(ownerbytes):
    parent()
    assert (BASE/(STEM+'_OWNER_START.json')).read_bytes() == ownerbytes and sha(__file__) == OWNER['source_sha256']
    for n, h in CREATED.items(): assert sha(BASE/n) == h
    for rec in RECORDS:
        assert load(rec['commit_file']) == {k: v for k, v in rec.items() if k not in ('commit_file', 'commit_sha256')}
        with np.load(BASE/rec['file'], allow_pickle=False) as z:
            md = rec['metadata']; assert json.loads(str(z['metadata'])) == md and set(z.files) == set(md['schema'])|{'metadata'}
            for n, d in md['schema'].items():
                a = z[n]; assert d == dict(shape=list(a.shape), dtype=str(a.dtype), finite=bool(np.isfinite(a).all()))
    assert {p.name for p in BASE.glob(STEM+'_*')} == set(CREATED)

def clock(psi, ep, fixed):
    norm = 1/ep-math.log1p(1/ep); A = 1.5*fixed['OA']/fixed['rG']
    target = .5*ep*norm*fixed['d0']; s0 = target
    for _ in range(12):
        q = math.sqrt(1+ep*s0/(1+s0)); dq = ep/(2*q*(1+s0)**2); s0 -= (s0*q-target)/(q+s0*dq)
    u0 = ep*s0/(1+s0); delta = (1+u0)*np.expm1(-2*B0*psi); u = u0+delta
    RAW['current_clock_u'] = u.copy()
    assert np.isfinite(u).all() and np.all(u > 0) and np.all(u < ep)
    s = u/(ep-u); q = np.sqrt(1+u); pe = (np.log1p(s)-s/(1+s))/norm
    d = 2*q*s/(ep*norm); rho = A*(1+q*d-pe); pressure = A*(pe-1)
    ds = ep*delta/((ep-u)*(ep-u0))
    dpe = (np.log1p(ds/(1+s0))-ds/((1+s)*(1+s0)))/norm
    dqd = 2*((1+u)*ds+s0*delta)/(ep*norm)
    kappa = 2*(fixed['Hunit']/KPC)**2*KPC/(C*A0)
    return dict(u=u, rho_norm=rho, P_norm=pressure, delta_rho_norm=A*(dqd-dpe), delta_P_norm=A*dpe,
                pressure_scaled=kappa/B0*pressure, rho_scaled=kappa/B0*rho, kappa=kappa)

def shapes(r, z, u, v):
    dr, dz = np.diff(r)[:, None], np.diff(z)[None, :]
    rr = (r[:-1, None]+r[1:, None])/2+u*dr/2
    zz = (z[None, :-1]+z[None, 1:])/2+v*dz/2
    basis = []
    for i, j in ((0, 0), (1, 0), (0, 1), (1, 1)):
        si, sj = 2*i-1, 2*j-1
        basis.append(((1+si*u)*(1+sj*v)/4, si*(1+sj*v)/(2*dr), sj*(1+si*u)/(2*dz), i, j))
    return rr, zz, dr, dz, basis

def interpolate(x, basis):
    val = np.zeros((65, x.shape[-2]-1, x.shape[-1]-1)); gr = np.zeros_like(val); gz = np.zeros_like(val)
    for n, nr, nz, i, j in basis:
        a = x[:, i:x.shape[-2]-1+i, j:x.shape[-1]-1+j]
        val += n*a; gr += nr*a; gz += nz*a
    return val, gr, gz

def point(x, r, z, u, v, xi, weight, fixed, ep):
    for name in list(RAW):
        if name.startswith('current_point_'): del RAW[name]
    rr, zz, dr, dz, basis = shapes(r, z, u, v); val, gr, gz = interpolate(x, basis)
    RAW.update(current_point_value=val.copy(), current_point_gr=gr.copy(), current_point_gz=gz.copy())
    sw = np.sqrt(weight)[:, None, None]; uv = np.stack((val[1::2]/sw, np.zeros_like(val[1::2]), val[2::2]/sw), axis=-1)
    ur, uz = uv[..., 0], uv[..., 2]; a = np.stack((gr[0], np.zeros_like(gr[0]), gz[0]), axis=-1)
    G = np.zeros(uv.shape[:-1]+(3, 3)); G[..., 0, 0] = gr[1::2]/sw; G[..., 0, 2] = gr[2::2]/sw
    G[..., 2, 0] = gz[1::2]/sw; G[..., 2, 2] = gz[2::2]/sw
    G[..., 1, 1] = np.divide(ur, rr, out=G[..., 0, 0].copy(), where=rr > 0)
    RAW.update(current_point_u=uv.copy(), current_point_G=G.copy())
    sym = (G+np.swapaxes(G, -1, -2))/2; norm = np.sum(uv*uv, axis=-1)
    inv = 1/(GC**2*xi[:, None, None]**4); potential = norm/2+norm*norm*inv/4; f = 1+norm*inv
    gradnorm = np.sum(G*G, axis=(-2, -1)); coupling = np.sum(uv*a, axis=-1)
    w = weight[:, None, None]; aa = np.sum(a*a, axis=-1)
    lag = KB/(2*C)*aa+np.sum(w*(-potential-ELL**2*gradnorm/2+coupling), axis=0)
    bulk = lag[..., None, None]*np.eye(3)-KB/C*a[..., :, None]*a[..., None, :]
    dyad = f[..., None, None]*uv[..., :, None]*uv[..., None, :]-a[None, ..., :, None]*uv[..., None, :]-uv[..., :, None]*a[None, ..., None, :]
    gradstress = G@np.swapaxes(G, -1, -2)+np.swapaxes(G, -1, -2)@G
    bulk += np.sum(w[..., None, None]*(dyad+ELL**2*gradstress), axis=0)
    flux = np.zeros((3,)+rr.shape+(3, 3))
    for k in range(3):
        one = uv[..., k, None, None]*sym-uv[..., :, None]*sym[..., None, :, k]-uv[..., None, :]*sym[..., :, None, k]
        flux[k] = np.sum(w[..., None, None]*one, axis=0)
    traceflux = np.trace(flux, axis1=-2, axis2=-1)
    RAW.update(current_point_bulk=bulk.copy(), current_point_flux=flux.copy(), current_point_traceflux=traceflux.copy())
    rhoq = KB/(2*C)*aa+np.sum(w*(potential+ELL**2*gradnorm/2), axis=0)
    active = KB/C*aa+np.sum(w*(norm*norm*inv/2+ELL**2*gradnorm+coupling), axis=0)
    active_envelope = KB/C*aa+np.sum(w*(norm*norm*inv/2+ELL**2*gradnorm+abs(coupling)), axis=0)
    cl = clock(val[0], ep, fixed); N = np.exp(B0*val[0]); totalbulk = bulk+cl['pressure_scaled'][..., None, None]*np.eye(3)
    return dict(rr=rr, zz=zz, dr=dr, dz=dz, basis=basis, value=val, gr=gr, gz=gz, u=uv, G=G, sym=sym,
                gradnorm=gradnorm, Gnorm_expected=(gr[1::2]**2+gr[2::2]**2+gz[1::2]**2+gz[2::2]**2)/sw**2+G[..., 1, 1]**2,
                bulk=bulk, totalbulk=totalbulk, flux=flux, traceflux=traceflux, rhoq=rhoq, active=active, active_envelope=active_envelope, lag=lag, aa=aa, a=a, N=N, clock=cl)

def add_scalar(out, value, radial, vertical, volume, basis, absolute=False):
    for n, nr, nz, i, j in basis:
        term = n*value+nr*radial+nz*vertical
        if absolute: term = abs(n*value)+abs(nr*radial)+abs(nz*vertical)
        out[i:out.shape[0]-1+i, j:out.shape[1]-1+j] += volume*term

def add_tensor(out, bulk, flux, a, rr, volume, basis, absolute=False):
    # Components RR, phiphi, ZZ, RZ; RZ tests have BOTH symmetric entries.
    for component, (i0, j0, factor) in enumerate(((0, 0, 1), (1, 1, 1), (2, 2, 1), (0, 2, 2))):
        val = factor*(bulk[..., i0, j0]+B0*ELL**2*(a[..., 0]*flux[0, ..., i0, j0]+a[..., 2]*flux[2, ..., i0, j0]))
        angular = np.zeros_like(rr)
        if component in (0, 1): angular = (-1 if component == 0 else 1)*2*ELL**2*flux[1, ..., 0, 1]/rr
        if component == 3: angular = -2*ELL**2*flux[1, ..., 1, 2]/rr
        if absolute:
            val = factor*(abs(bulk[..., i0, j0])+B0*ELL**2*(abs(a[..., 0]*flux[0, ..., i0, j0])+abs(a[..., 2]*flux[2, ..., i0, j0])))+abs(angular)
        else: val += angular
        add_scalar(out[component], val, -factor*ELL**2*flux[0, ..., i0, j0], -factor*ELL**2*flux[2, ..., i0, j0], volume, basis, absolute)

def regular_tensor_load(a):
    b = a.copy(); b[0, 0] += b[1, 0]; b[1, 0] = 0; b[3, 0] = 0; b[3, :, 0] = 0
    return b

def volume_order(order, x, r, z, xi, weight, fixed, ep):
    nodes, qw = np.polynomial.legendre.leggauss(order)
    shape = (len(r), len(z)); tensor = np.zeros((4,)+shape); total = np.zeros_like(tensor); env = np.zeros_like(tensor)
    active = np.zeros(shape); active_independent = np.zeros(shape); aenv = np.zeros(shape); rhoqload = np.zeros(shape)
    leading = np.zeros(shape); leadingenv = np.zeros(shape); geom = np.zeros(shape); phase = np.zeros(shape)
    rholinear = np.zeros(shape); pabsolute = np.zeros(shape); rhoabsolute = np.zeros(shape)
    all_arrays = {}; errors = dict(Gnorm=0., active=0., TF=0., fluxtrace=0.); area = zfirst = 0.
    for iu, u in enumerate(nodes):
        for iv, v in enumerate(nodes):
            tag = f'Q{order}_U{iu}_V{iv}'; CONTEXT.update(stage='volume', order=order, iu=iu, iv=iv)
            p = point(x, r, z, u, v, xi, weight, fixed, ep); volume = p['rr']*p['dr']*p['dz']*qw[iu]*qw[iv]/4
            for key in ('rr', 'zz', 'value', 'gr', 'gz', 'u', 'G', 'bulk', 'totalbulk', 'flux', 'traceflux', 'rhoq', 'active', 'active_envelope', 'N'):
                all_arrays[tag+'_'+key] = p[key].copy(); RAW[tag+'_'+key] = all_arrays[tag+'_'+key]
            for key in ('u', 'rho_norm', 'P_norm', 'delta_rho_norm', 'delta_P_norm', 'pressure_scaled', 'rho_scaled'):
                all_arrays[tag+'_clock_'+key] = p['clock'][key].copy(); RAW[tag+'_clock_'+key] = all_arrays[tag+'_clock_'+key]
            all_arrays[tag+'_measure'] = volume.copy(); RAW[tag+'_measure'] = volume.copy()
            eye = np.eye(3); tf = p['bulk']-np.trace(p['bulk'], axis1=-2, axis2=-1)[..., None, None]/3*eye
            uvec, sym, w = p['u'], p['sym'], weight[:, None, None]
            jt = np.stack([np.sum(w*(uvec[..., k]*np.trace(sym, axis1=-2, axis2=-1)-2*np.sum(uvec*sym[..., :, k], axis=-1)), axis=0) for k in range(3)])
            for name, aa, bb in (('Gnorm', p['gradnorm'], p['Gnorm_expected']), ('active', p['active'], p['rhoq']+np.trace(p['bulk'], axis1=-2, axis2=-1)), ('TF', np.trace(tf, axis1=-2, axis2=-1), np.zeros_like(p['rr'])), ('fluxtrace', p['traceflux'], jt)):
                all_arrays[tag+'_identity_'+name+'_actual'] = aa.copy(); all_arrays[tag+'_identity_'+name+'_expected'] = bb.copy()
                RAW[tag+'_identity_'+name+'_actual'] = aa.copy(); RAW[tag+'_identity_'+name+'_expected'] = bb.copy()
                assert np.isfinite(aa).all() and np.isfinite(bb).all()
                errors[name] = max(errors[name], float(np.max(abs(aa-bb))/max(1., float(np.max(abs(aa))), float(np.max(abs(bb))))))
            add_tensor(tensor, p['bulk'], p['flux'], p['a'], p['rr'], volume, p['basis'])
            add_tensor(total, p['totalbulk'], p['flux'], p['a'], p['rr'], volume, p['basis'])
            add_tensor(env, p['bulk'], p['flux'], p['a'], p['rr'], volume, p['basis'], True)
            J = p['traceflux']; correction = B0*ELL**2*(p['a'][..., 0]*J[0]+p['a'][..., 2]*J[2])
            add_scalar(active, p['active']+correction, -ELL**2*J[0], -ELL**2*J[2], volume, p['basis'])
            add_scalar(active_independent, p['rhoq'], 0., 0., volume, p['basis'])
            add_scalar(rhoqload, p['rhoq'], 0., 0., volume, p['basis'])
            add_scalar(aenv, p['active_envelope']+B0*ELL**2*(abs(p['a'][..., 0]*J[0])+abs(p['a'][..., 2]*J[2])), -ELL**2*J[0], -ELL**2*J[2], volume, p['basis'], True)
            Z = np.sum(weight[:, None, None, None]*p['u'], axis=0)
            add_scalar(leading, 0., p['a'][..., 0]-Z[..., 0], p['a'][..., 2]-Z[..., 2], volume, p['basis'])
            add_scalar(leadingenv, 0., p['a'][..., 0], p['a'][..., 2], volume, p['basis'], True)
            add_scalar(leadingenv, 0., -Z[..., 0], -Z[..., 2], volume, p['basis'], True)
            add_scalar(geom, -2/C*p['aa'], 0., 0., volume, p['basis'])
            add_scalar(phase, p['clock']['kappa']*(p['clock']['delta_rho_norm']+3*p['clock']['delta_P_norm']), 0., 0., volume, p['basis'])
            add_scalar(rholinear, 0., -(KB/C*p['a'][..., 0]+Z[..., 0])/B0, -(KB/C*p['a'][..., 2]+Z[..., 2])/B0, volume, p['basis'])
            add_scalar(pabsolute, p['clock']['pressure_scaled'], 0., 0., volume, p['basis'])
            add_scalar(rhoabsolute, p['clock']['rho_scaled'], 0., 0., volume, p['basis'])
            area += float(np.sum(volume)); zfirst += float(np.sum(volume*p['zz']))
    active_independent += tensor[0]+tensor[1]+tensor[2]
    check(f'Q{order}_Gnorm', errors['Gnorm'], 0.); check(f'Q{order}_bulk_active', errors['active'], 0.)
    check(f'Q{order}_TF_trace', errors['TF'], 0.); check(f'Q{order}_flux_trace', errors['fluxtrace'], 0.)
    check(f'Q{order}_weak_active', active, active_independent)
    tfloads = tensor.copy(); trace = tensor[0]+tensor[1]+tensor[2]
    for k in range(3): tfloads[k] -= trace/3
    check(f'Q{order}_weak_TF_trace', tfloads[0]+tfloads[1]+tfloads[2], np.zeros(shape))
    check(f'Q{order}_volume_measure', area, r[-1]**2*z[-1]/2)
    check(f'Q{order}_volume_first_Z', zfirst, r[-1]**2*z[-1]**2/4)
    loads = dict(native_tensor_raw=tensor, native_tensor_regular_axis=regular_tensor_load(tensor), total_tensor_raw=total,
                 native_tensor_absolute_envelope=env, native_TF_raw=tfloads, native_active=active,
                 native_active_independent=active_independent, native_active_envelope=aenv, native_rho_quadratic=rhoqload,
                 leading_native=leading, leading_native_termwise_envelope=leadingenv, flat_lapse_geometric=geom,
                 inherited_clock_active=phase, omitted_native_lapse_load=B0*active,
                 native_plus_flat_geometry_load=B0*(active+geom), native_rho_linear_volume_weak=rholinear,
                 phase_P_absolute_load=pabsolute, phase_rho_absolute_load=rhoabsolute)
    all_arrays.update(loads); RAW.update({f'Q{order}_'+n: a for n, a in loads.items()})
    return all_arrays, loads

def faces_order(order, x, r, z, xi, weight, fixed, ep):
    nodes, qw = np.polynomial.legendre.leggauss(order); arrays = {}; er = ez = 0.
    outerrho = np.zeros((len(r), len(z)))
    P = np.diag([1., 1., -1.])
    for k, t in enumerate(nodes):
        CONTEXT.update(stage='faces', order=order, node=k)
        saved = []
        for label, uu, vv in (('left', 1., t), ('right', -1., t), ('bottom', t, -1.), ('top', t, 1.)):
            p = point(x, r, z, uu, vv, xi, weight, fixed, ep); saved.append(p)
            for n in ('value', 'a', 'u', 'G', 'flux'):
                RAW[f'Q{order}_F{k}_{label}_{n}'] = p[n].copy()
        left, right, bottom, top = saved
        er = max(er, float(np.max(abs(left['value'][:, :-1]-right['value'][:, 1:]))))
        ez = max(ez, float(np.max(abs(top['value'][:, :, :-1]-bottom['value'][:, :, 1:]))))
        fr = right['flux'][0, 1:]-left['flux'][0, :-1]
        fz = bottom['flux'][2, :, 1:]-top['flux'][2, :, :-1]
        sheet = bottom['flux'][2, :, 0]; sheet_jump = sheet+P@sheet@P
        fields = dict(radial_internal_jump=fr, vertical_internal_jump=fz, sheet_upper_flux=sheet,
                      sheet_mirrored_jump=sheet_jump, sheet_half_domain_contact=sheet_jump/2,
                      axis_flux=right['flux'][0, 0], radial_outer_flux=left['flux'][0, -1], vertical_outer_flux=top['flux'][2, :, -1],
                      radial_measure=r[1:-1, None]*np.diff(z)[None, :]*qw[k]/2,
                      vertical_measure=bottom['rr'][:, :1]*np.diff(r)[:, None]*qw[k]/2,
                      sheet_measure=bottom['rr'][:, 0]*np.diff(r)*qw[k]/2,
                      axis_a=right['a'][0], axis_u=right['u'][:, 0], sheet_a=bottom['a'][:, 0],
                      radial_a_jump=right['a'][1:]-left['a'][:-1], vertical_a_jump=bottom['a'][:, 1:]-top['a'][:, :-1],
                      sheet_a_mirrored_jump=2*bottom['a'][:, 0, 2], radial_outer_a=left['a'][-1], vertical_outer_a=top['a'][:, -1])
        for name, a in fields.items(): arrays[f'F{k}_'+name] = a.copy(); RAW[f'Q{order}_F{k}_'+name] = arrays[f'F{k}_'+name]
        zr = np.sum(weight[:, None, None, None]*left['u'], axis=0)[-1, :, 0]
        zt = np.sum(weight[:, None, None, None]*top['u'], axis=0)[:, -1, 2]
        radial = (KB/C*left['a'][-1, :, 0]+zr)/B0*r[-1]*np.diff(z)*qw[k]/2
        vertical = (KB/C*top['a'][:, -1, 2]+zt)/B0*top['rr'][:, -1]*np.diff(r)*qw[k]/2
        outerrho[-1, :-1] += radial*(1-t)/2; outerrho[-1, 1:] += radial*(1+t)/2
        outerrho[:-1, -1] += vertical*(1-t)/2; outerrho[1:, -1] += vertical*(1+t)/2
    check(f'Q{order}_radial_C0_trace', er, 0.); check(f'Q{order}_vertical_C0_trace', ez, 0.)
    # Outer mode Dirichlet values are already required by the inherited field mask.
    # Hence their improvement flux vanishes; no sheet/internal delta is added again
    # to the distributional volume weak loads, which already include those contacts.
    arrays['outer_native_rho_linear_load'] = outerrho; RAW[f'Q{order}_outer_rho_load'] = outerrho.copy()
    return arrays, outerrho

def main():
    global np, OWNER
    assert not AUTHOR_DRAFT and PINS and PROTOCOL_SHA
    assert not list(BASE.glob(STEM+'_*'))
    case, rec, fixed = parent(); OWNER = dict(owner='root', pid=os.getpid(), started=now(), source_sha256=sha(__file__))
    tick = time.monotonic(); ownerbytes = encode(OWNER)
    try:
        publish(STEM+'_OWNER_START.json', OWNER)
        publish(STEM+'_MANIFEST.json', dict(owner=OWNER, inputs=MERGED, parent=rec, fixed=fixed, orders=list(ORDERS), prospective_controls=24, physical_flags=PHYSICAL))
        for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'): os.environ[name] = '1'
        import numpy as np
        with np.load(BASE/rec['file'], allow_pickle=False) as z:
            for n in z.files:
                if n != 'metadata': RAW['parent_'+n] = z[n].copy()
            assert json.loads(str(z['metadata'])) == rec['metadata'] and set(z.files) == {'metadata', 'state', 'residual', 'pre'}
            x = z['state'].copy()
        identity = case['identity']; r = np.asarray(identity['r_kpc']); z = np.asarray(identity['z_kpc'])
        assert x.shape == (65, 87, 45) and np.isfinite(x).all() and r[0] == z[0] == 0 and np.all(np.diff(r) > 0) and np.all(np.diff(z) > 0)
        mask = np.ones(x.shape, bool); mask[:, -1] = False; mask[:, :, -1] = False; mask[1::2, 0] = False; mask[2::2, :, 0] = False
        check('exact_inherited_field_mask', x[~mask], np.zeros_like(x[~mask]))
        sn, sw = np.polynomial.legendre.leggauss(32); xi = (sn+1)/2; weight = sw*xi
        check('weight_sum', float(np.sum(weight)), 1.)
        check('positive_weights', 0. if np.min(weight) > 0 else 1., 0.)
        c = clock(x[0], identity['eps'], fixed); check('finite_admitted_clock', 0. if all(np.isfinite(a).all() for a in c.values()) else 1., 0.)
        checkpoint('INPUT', dict(RAW, r=r, z=z, xi=xi, weight=weight, mask=mask), dict(identity=identity, parent=rec, original_case=case))
        results = {}
        for order in ORDERS:
            arrays, loads = volume_order(order, x, r, z, xi, weight, fixed, identity['eps'])
            checkpoint(f'VOLUME_Q{order}', arrays, dict(order=order, units='g*(a0/cp^2)^2; source load conversion B0', B0=B0, controls=list(FLAGS)))
            facearrays, outerrho = faces_order(order, x, r, z, xi, weight, fixed, identity['eps'])
            loads['native_rho_linear_full_weak'] = loads['native_rho_linear_volume_weak']+outerrho
            loads['native_rho_full_weak'] = loads['native_rho_linear_full_weak']+loads['native_rho_quadratic']
            facearrays['native_rho_linear_full_weak'] = loads['native_rho_linear_full_weak']
            facearrays['native_rho_full_weak'] = loads['native_rho_full_weak']
            checkpoint(f'FACES_Q{order}', facearrays, dict(order=order, all_contacts_retained=True, sheet_deltas_not_added_twice=True, controls=list(FLAGS)))
            results[order] = loads
        differences = {n: results[3][n]-results[2][n] for n in results[2]}
        RAW.update({'difference_'+n: a for n, a in differences.items()}); summaries = {}
        for order, loads in results.items():
            leading = float(np.max(abs(loads['leading_native']))); envelope = float(np.max(loads['leading_native_termwise_envelope']))
            summaries[str(order)] = dict(native_load_max=float(np.max(abs(B0*loads['native_active']))), native_load_envelope_max=float(np.max(B0*loads['native_active_envelope'])),
                leading_native_signed_max=leading, leading_native_envelope_max=envelope,
                signed_load_ratio=float(np.max(abs(B0*loads['native_active']))/max(leading, 1e-30)),
                envelope_load_ratio=float(np.max(B0*loads['native_active_envelope'])/max(envelope, 1e-30)), relative_floor=1e-30,
                metric_inverse_bound=None, force_correction=None, ordinary_spatial_stress=None, background_Einstein_remainder=None)
        checkpoint('COMPARISONS', differences, dict(signed_Q3_minus_Q2=True, descriptive_only=True, summaries=summaries))
        assert len(FLAGS) == 24 and len(RECORDS) == 6
        status = 'ARITHMETIC_PASS' if all(f['passed'] for f in FLAGS) else 'ARITHMETIC_FAILED'
        publish(STEM+'_RESULT.json', dict(status=status, owner=OWNER, inputs=MERGED, records=RECORDS, controls=FLAGS, summaries=summaries,
            parent_case_copied_exactly=case, physical_flags=PHYSICAL, units=dict(native_stress='g*(a0/cp^2)^2', linear_native_source='g*a0/(cp^2*L0)', B0=B0), elapsed_seconds=time.monotonic()-tick))
        report = ('# Saved weak Hilbert stress meter V001\n\n'+status+': 24 arithmetic controls; one closed coarse field, two postprocessing orders.\n\n'
                  'Full native tensor, isotropic clock pressure and distributional face/sheet contacts are retained. Load ratios are descriptive; no metric inverse, force correction, lensing or exterior qualification.\n').encode()
        p = BASE/(STEM+'_REPORT.md')
        with p.open('xb') as f: f.write(report); f.flush(); os.fsync(f.fileno())
        p.chmod(0o444); assert p.read_bytes() == report; CREATED[p.name] = sha(p)
        recheck(ownerbytes)
        publish(STEM+'_RECEIPT.json', dict(status='CLOSED', owner=OWNER, closed=now(), source_sha256=OWNER['source_sha256'], result_sha256=CREATED[STEM+'_RESULT.json'], input_sha256=MERGED, output_sha256=dict(CREATED), records=RECORDS, predicate_count=24, physical_flags=PHYSICAL))
        recheck(ownerbytes); return 0 if status == 'ARITHMETIC_PASS' else 3
    except Exception as exc:
        existing = BASE/(STEM+'_RECEIPT.json'); protected = sha(existing) if existing.exists() else None
        if protected is not None: CREATED[existing.name] = protected
        if np is not None and RAW: checkpoint('ERROR_RAW', RAW, dict(context=dict(CONTEXT), error=str(exc), exception=type(exc).__name__, unaccepted=True), True)
        publish(STEM+'_ERROR.json', dict(owner=OWNER, context=dict(CONTEXT), error=str(exc), exception=type(exc).__name__, records=RECORDS, inputs=MERGED, outputs=dict(CREATED), protected_existing_receipt_sha256=protected, physical_flags=PHYSICAL))
        if protected is None: publish(STEM+'_RECEIPT.json', dict(status='ERROR', owner=OWNER, closed=now(), input_sha256=MERGED, output_sha256=dict(CREATED), records=RECORDS, physical_flags=PHYSICAL))
        else: assert sha(existing) == protected
        raise

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--root-owned', action='store_true'); args = ap.parse_args()
    if not args.root_owned: raise RuntimeError('Root-owned execution only')
    raise SystemExit(main())
