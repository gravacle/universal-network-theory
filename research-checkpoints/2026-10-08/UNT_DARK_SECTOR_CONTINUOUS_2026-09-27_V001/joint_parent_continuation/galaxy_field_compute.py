"""No-refit observed-density disk experiment, complete-case and iteration resume."""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import tempfile
import time
import numpy as np
import disk_solver as law
import axisymmetric_disk_v002 as disk
import galaxy_density as density

ROOT = law.ROOT
OBSERVED = ROOT.parent/'ngc3198_sparc_excerpt_v001.txt'
FREEZE = ROOT/'GALAXY_FIELD_FROZEN.json'


def observations():
    rows = []
    for line in OBSERVED.read_text().splitlines():
        if line.startswith('NGC3198 '):
            values = line.split()
            rows.append({'R':float(values[2]),'velocity':float(values[3]),'error':float(values[4])})
    assert len(rows) == 43
    return rows


def case_name(hi_tail,h2_tail,n,extent,newtonian):
    return f'galaxy_HI{int(hi_tail)}_H2{int(h2_tail)}_N{n}_L{extent}_Newton{int(newtonian)}'


def checkpoint_writer(path,identity,freeze_hash):
    def write(phi,history):
        history_text = law.encode(history).decode()
        metadata = {'case':identity,'freeze_sha256':freeze_hash,
                    'phi_sha256':hashlib.sha256(phi.tobytes(order='C')).hexdigest(),
                    'history_sha256':hashlib.sha256(history_text.encode()).hexdigest(),
                    'shape':list(phi.shape),'dtype':str(phi.dtype)}
        with tempfile.NamedTemporaryFile(dir=ROOT,prefix=path.name+'.partial.',delete=False) as stream:
            np.savez_compressed(stream,phi=phi,history=history_text,metadata=law.encode(metadata).decode())
            stream.flush()
            os.fsync(stream.fileno())
            temporary = Path(stream.name)
        os.replace(temporary,path)  # Replaces only this calculation's rolling checkpoint.
        print(json.dumps({'checkpoint':identity,'outer':len(history),
                          'nonlinear_error':history[-1].get('nonlinear_error'),
                          'flux_balance_error':history[-1].get('flux_balance_error')}),flush=True)
    return write


def load_checkpoint(path,identity,freeze_hash,n):
    with np.load(path,allow_pickle=False) as saved:
        phi = saved['phi']
        history_text = str(saved['history'].item())
        meta = json.loads(str(saved['metadata'].item()))
    assert meta['case'] == identity and meta['freeze_sha256'] == freeze_hash
    assert meta['shape'] == list(phi.shape) == [n,n] and meta['dtype'] == str(phi.dtype) == 'float64'
    assert meta['phi_sha256'] == hashlib.sha256(phi.tobytes(order='C')).hexdigest()
    assert meta['history_sha256'] == hashlib.sha256(history_text.encode()).hexdigest()
    assert np.all(np.isfinite(phi))
    return phi,json.loads(history_text)


def run_case(hi_tail,h2_tail,n,extent,newtonian,freeze_hash):
    start = time.perf_counter()
    identity = case_name(hi_tail,h2_tail,n,extent,newtonian)
    components = density.profiles(hi_tail,h2_tail)
    masses = density.masses(components)
    mass = sum(masses.values())
    q = density.G_KPC_KMS2_MSUN*mass/density.A0_KMS2_KPC
    geometry = edges,c,width = disk.mesh(n,extent)
    sr = np.sqrt(extent**2+c*c)
    pr = disk.spherical_potential(sr,q,newtonian=newtonian)
    pz = pr.copy()
    inv = (lambda d:d) if newtonian else law.inverse
    tangent = inv(q/sr**2)*c/sr
    bottom = density.bottom_flux(edges,components)
    boundary = (pr,pz,tangent,tangent,bottom)
    checkpoint_path = ROOT/(identity+'.checkpoint.npz')
    history = None
    if checkpoint_path.exists():
        initial,history = load_checkpoint(checkpoint_path,identity,freeze_hash,n)
        print(json.dumps({'resume_checkpoint':identity,'completed_outer':len(history)}),flush=True)
    else:
        rr,zz = np.meshgrid(c,c,indexing='ij')
        # Smooth monopole initial field, not a solved disk or an observed velocity.
        s = np.sqrt(rr*rr+(zz+5.)**2)
        # Analytic asymptotic starting potential; the boundary is imposed by the solve.
        initial = q*(1-1/s) if newtonian else math.sqrt(q)*np.log(s)
    phi,radial,history,ok = disk.solve(geometry,boundary,initial,newtonian,
                                      checkpoint=checkpoint_writer(checkpoint_path,identity,freeze_hash),
                                      history_start=history)
    obs = observations()
    observed_radii = np.array([row['R'] for row in obs])
    sampled = np.interp(observed_radii,c,radial)
    comparisons = []
    for row,force in zip(obs,sampled):
        v2 = row['R']*density.A0_KMS2_KPC*float(force)
        velocity = math.sqrt(v2) if v2>=0 else None
        comparisons.append(dict(**row,radial_force_a0=float(force),velocity_squared=v2,
                                prediction=velocity,residual=None if velocity is None else velocity-row['velocity']))
    summaries = {}
    for lower in (0.,2.,8.):
        selected = [row for row in comparisons if row['R']>=lower and row['residual'] is not None]
        residuals = np.array([row['residual'] for row in selected])
        errors = np.array([row['error'] for row in selected])
        summaries[f'R_ge_{lower:g}_kpc'] = {
            'count':len(selected),'omitted_negative_force_count':sum(row['R']>=lower and row['residual'] is None for row in comparisons),
            'rms_kms':float(np.sqrt(np.mean(residuals**2))) if selected else None,
            'mean_residual_kms':float(np.mean(residuals)) if selected else None,
            'max_abs_residual_kms':float(np.max(abs(residuals))) if selected else None,
            'nominal_sum_squared_error_units':float(np.sum((residuals/errors)**2)) if selected else None}
    flux_mass = float(np.sum(bottom))*density.A0_KMS2_KPC/density.G_KPC_KMS2_MSUN
    expected_in_domain = sum(float(2*math.pi*1e6*p.integral(0.,extent)) for p in components.values())
    mass_error = abs(flux_mass-expected_in_domain)/expected_in_domain
    checks = {'converged':bool(ok),'source_mass':mass_error<=1e-13,
              'flux_balance':history[-1].get('flux_balance_error',math.inf)<=2e-6,
              'unclipped':history[-1].get('clipped_faces',-1)==0,
              'nonlinear_residual':history[-1].get('nonlinear_error',math.inf)<=1e-9}
    numerical_comparison = {}
    if not newtonian and (extent == 1023 or n == 512):
        prior_name = case_name(hi_tail,h2_tail,256,255,False)
        prior_record = json.loads((ROOT/(prior_name+'.json')).read_text())
        prior = prior_record['payload']
        assert prior_record['freeze_sha256'] == freeze_hash
        assert prior_record['payload_sha256'] == hashlib.sha256(law.encode(prior)).hexdigest()
        assert prior['case'] == prior_name and all(prior['checks'].values())
        prior_force = np.array([row['radial_force_a0'] for row in prior['comparison']])
        selected = observed_radii>=2.
        difference = float(np.max(abs(sampled[selected]-prior_force[selected])/
                                  np.maximum(abs(sampled[selected]),1e-12)))
        label = 'remote_domain' if extent == 1023 else 'mesh_refinement'
        numerical_comparison[label+'_max_force_change'] = difference
        checks[label] = difference < .02
    ring_comparison = []
    if newtonian:
        oracle = json.loads((ROOT/'RING_ORACLE_RESULTS.json').read_text())['payload']
        for item in oracle['cases']:
            if item['hi_tail'] != hi_tail or item['h2_tail'] != h2_tail:
                continue
            radius = item['R_kpc']
            reference = item['extrapolated_gR_kms2_per_kpc'][-1]
            grid_force = float(np.interp(radius,c,radial))*density.A0_KMS2_KPC
            extrapolation_difference = abs(reference-item['extrapolated_gR_kms2_per_kpc'][0])
            last_height = item['heights'][-1]['orders']
            quadrature_difference = abs(last_height['96']['gR_kms2_per_kpc']-last_height['48']['gR_kms2_per_kpc'])
            allowance = .02*max(1.,abs(reference))+extrapolation_difference+quadrature_difference
            discrepancy = abs(grid_force-reference)
            ring_comparison.append({'R_kpc':radius,'grid_gR_kms2_per_kpc':grid_force,
                'oracle_extrapolated_gR_kms2_per_kpc':reference,
                'oracle_extrapolation_difference':extrapolation_difference,
                'oracle_quadrature_difference':quadrature_difference,
                'absolute_discrepancy':discrepancy,'numerical_allowance':allowance,
                'passed':discrepancy<=allowance})
        assert len(ring_comparison) == 5
        checks['independent_newtonian_force'] = all(row['passed'] for row in ring_comparison)
    payload = {'case':identity,'hi_tail':hi_tail,'h2_tail':h2_tail,'N':n,'extent':extent,
               'newtonian':newtonian,'component_masses_Msun':masses,
               'omitted_mass_beyond_boundary_Msun':mass-expected_in_domain,
               'source_mass_relative_error':mass_error,'checks':checks,'history':history,
               'numerical_comparison':numerical_comparison,
               'independent_newtonian_force_comparison':ring_comparison,
               'radii':c.tolist(),'radial_force_a0':radial.tolist(),'phi':phi.tolist(),
               'comparison':comparisons,'summaries_descriptive_only':summaries,
               'seconds_this_invocation':time.perf_counter()-start,
               'peak_self_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    law.save_new(ROOT/(identity+'.json'),{'freeze_sha256':freeze_hash,
                 'payload_sha256':hashlib.sha256(law.encode(payload)).hexdigest(),'payload':payload})
    print(json.dumps({'completed':identity,'checks':checks,'seconds':payload['seconds_this_invocation'],
                      'descriptive_velocity_residuals':summaries}),flush=True)
    return payload


def main():
    plan = [(n,8,eta,False) for n in (64,128,256) for eta in (.01,1.,100.)]
    plan += [(256,128,eta,False) for eta in (.01,1.,100.)]+[(128,8,1.,True)]
    qualification = [(ROOT/f'stretched_V002_N{n}_L{extent}_eta{eta:g}_Newton{int(newtonian)}.json',
                       (n,extent,eta,newtonian)) for n,extent,eta,newtonian in plan]
    paths = ['NGC3198_FIXED_DENSITY_PROTOCOL.md','galaxy_field_compute.py','galaxy_density.py',
             'NGC3198_BARYON_INPUT.json','leroy2008_table7.dat','leroy2008_table4.dat',
             'leroy2008_ReadMe.html','begeman1989_original.pdf','disk_solver.py',
             'axisymmetric_disk.py','axisymmetric_disk_v002.py','STRETCHED_DISK_V002_FROZEN.json',
             '../joint_parent_dynamics/SHAPE_REFERENCE_RESULTS.json','../ngc3198_sparc_excerpt_v001.txt',
             'RING_ORACLE_FROZEN.json','RING_ORACLE_RESULTS.json']
    paths += [path.name for path,_ in qualification]
    files = {name:law.sha(ROOT/name) for name in paths}
    for name,digest in json.loads((ROOT/'STRETCHED_DISK_V002_FROZEN.json').read_text())['files'].items():
        assert law.sha(ROOT/name) == digest
    for name,digest in json.loads((ROOT/'RING_ORACLE_FROZEN.json').read_text())['files'].items():
        assert law.sha(ROOT/name) == digest
    if sys.argv[1:] == ['freeze']:
        law.save_new(FREEZE,{'files':files,'r':law.RATIO,'a0_kms2_kpc':density.A0_KMS2_KPC})
        return
    assert not sys.argv[1:]
    assert json.loads(FREEZE.read_text())['files'] == files
    # Stretched solver must have completed its independent exact-field qualification.
    previous_error = {}
    for path,expected in qualification:
        record = json.loads(path.read_text())
        assert record['freeze_sha256'] == law.sha(ROOT/'STRETCHED_DISK_V002_FROZEN.json')
        assert record['payload_sha256'] == hashlib.sha256(law.encode(record['payload'])).hexdigest()
        payload = record['payload']
        assert tuple(payload[key] for key in ('N','extent','eta','newtonian')) == expected
        assert all(payload['checks'].values())
        c = np.array(payload['radii'])
        selected = (c>=.5)&(c<=4.)
        relative_error = float(np.max(abs(np.array(payload['radial_force'])[selected]/
                                          np.array(payload['exact_force'])[selected]-1)))
        assert abs(relative_error-payload['max_curve_relative_error']) < 1e-14
        n,extent,eta,newtonian = expected
        if n == 256 or newtonian:
            assert relative_error < .02
        if extent == 8 and not newtonian:
            if eta in previous_error:
                assert relative_error < previous_error[eta]
            previous_error[eta] = relative_error
    oracle = json.loads((ROOT/'RING_ORACLE_RESULTS.json').read_text())
    assert oracle['freeze_sha256'] == law.sha(ROOT/'RING_ORACLE_FROZEN.json')
    assert oracle['payload_sha256'] == hashlib.sha256(law.encode(oracle['payload'])).hexdigest()
    assert oracle['payload']['status'] == 'COMPLETE' and all(row['passed'] for row in oracle['payload']['checks'])
    freeze_hash = law.sha(FREEZE)
    for hi_tail,h2_tail in ((True,True),(False,True),(True,False),(False,False)):
        for n,extent,newtonian in ((256,255,False),(320,1023,False),(512,255,False),(512,255,True)):
            identity = case_name(hi_tail,h2_tail,n,extent,newtonian)
            path = ROOT/(identity+'.json')
            if path.exists():
                record = json.loads(path.read_text())
                assert record['freeze_sha256'] == freeze_hash
                assert record['payload_sha256'] == hashlib.sha256(law.encode(record['payload'])).hexdigest()
                result = record['payload']
                assert result['case'] == identity
                print(json.dumps({'verified_completed_case':identity}),flush=True)
            else:
                result = run_case(hi_tail,h2_tail,n,extent,newtonian,freeze_hash)
            assert all(result['checks'].values()), 'Failed calculation preserved; diagnose before continuing.'


if __name__ == '__main__':
    main()
