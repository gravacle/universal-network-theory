import json
import math
import resource
import sys
import time
import numpy as np
import disk_solver as law
import axisymmetric_disk as disk

ROOT = law.ROOT


def case(n,extent,eta,newtonian=False):
    start = time.perf_counter()
    geometry = edges,c,width = disk.mesh(n,extent)
    sr = np.sqrt(extent**2+(c+1)**2)
    sz = np.sqrt(c*c+(extent+1)**2)
    inverse = (lambda d:d) if newtonian else law.inverse
    pr = disk.spherical_potential(sr,eta,newtonian=newtonian)
    pz = disk.spherical_potential(sz,eta,newtonian=newtonian)
    error = max(float(np.max(abs(pr-disk.spherical_potential(sr,eta,128,newtonian)))),
                float(np.max(abs(pz-disk.spherical_potential(sz,eta,128,newtonian)))))
    error /= max(1.,float(np.max(abs(pr))),float(np.max(abs(pz))))
    tr = inverse(eta/sr**2)*(c+1)/sr
    tz = inverse(eta/sz**2)*c/sz
    bottom = eta*(1/np.sqrt(edges[:-1]**2+1)-1/np.sqrt(edges[1:]**2+1))
    rr,zz = np.meshgrid(c,c,indexing='ij')
    scale = float(inverse(eta/4))/(eta/4)
    initial = scale*eta*(1-1/np.sqrt(rr*rr+(zz+1)**2))
    phi,radial,history,ok = disk.solve(geometry,(pr,pz,tr,tz,bottom),initial,newtonian)
    s0 = np.sqrt(c*c+1)
    exact = c/s0*inverse(eta/s0**2)
    selected = (c>=.5)&(c<=4)
    max_error = float(np.max(abs(radial[selected]/exact[selected]-1)))
    mass_error = abs(float(np.sum(bottom))-eta*(1-1/math.sqrt(1+extent**2)))/float(np.sum(bottom))
    checks = {'converged':bool(ok),'boundary_quadrature':error<=1e-9,
              'annular_mass':mass_error<=1e-13,'positive_force':bool(np.all(radial[selected]>0)),
              'flux_balance':history[-1].get('flux_balance_error',math.inf)<=2e-6,
              'unclipped':history[-1].get('clipped_faces',-1)==0}
    if n == 256 or newtonian:
        checks['force_accuracy'] = max_error < .02
    return {'N':n,'extent':extent,'eta':eta,'newtonian':newtonian,'checks':checks,
            'max_curve_relative_error':max_error,'boundary_error':error,'mass_error':mass_error,
            'history':history,'phi':phi.tolist(),'radii':c.tolist(),
            'radial_force':radial.tolist(),'exact_force':exact.tolist(),
            'seconds':time.perf_counter()-start,
            'peak_self_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def main():
    frozen = ROOT/'STRETCHED_DISK_FROZEN.json'
    sources = {name:law.sha(ROOT/name) for name in ('STRETCHED_DISK_PROTOCOL.md',
               'test_stretched_disk.py','axisymmetric_disk.py','disk_solver.py','DISK_SOLVER_FROZEN.json',
               '../joint_parent_dynamics/SHAPE_REFERENCE_RESULTS.json')}
    for name,digest in json.loads((ROOT/'DISK_SOLVER_FROZEN.json').read_text())['files'].items():
        assert law.sha(ROOT/name) == digest
    if sys.argv[1:] == ['freeze']:
        law.save_new(frozen,{'files':sources})
        return
    assert not sys.argv[1:]
    assert json.loads(frozen.read_text())['files'] == sources
    plan = [(n,8,eta,False) for n in (64,128,256) for eta in (.01,1.,100.)]
    plan += [(256,128,eta,False) for eta in (.01,1.,100.)]+[(128,8,1.,True)]
    previous = {}
    for n,extent,eta,newtonian in plan:
        path = ROOT/f'stretched_N{n}_L{extent}_eta{eta:g}_Newton{int(newtonian)}.json'
        if path.exists():
            record = json.loads(path.read_text())
            assert record['freeze_sha256'] == law.sha(frozen)
            assert record['payload_sha256'] == law.hashlib.sha256(law.encode(record['payload'])).hexdigest()
            payload = record['payload']
            assert (payload['N'],payload['extent'],payload['eta'],payload['newtonian']) == (n,extent,eta,newtonian)
            print(json.dumps({'verified_resume':path.name}),flush=True)
        else:
            payload = case(n,extent,eta,newtonian)
            if extent == 8 and not newtonian and eta in previous:
                payload['checks']['refinement_improves'] = payload['max_curve_relative_error'] < previous[eta]
            law.save_new(path,{'freeze_sha256':law.sha(frozen),
                'payload_sha256':law.hashlib.sha256(law.encode(payload)).hexdigest(),'payload':payload})
            print(json.dumps({key:payload[key] for key in ('N','extent','eta','newtonian','checks','max_curve_relative_error','seconds')}),flush=True)
        assert all(payload['checks'].values()), 'Failed case preserved for diagnosis.'
        if extent == 8 and not newtonian:
            if eta in previous:
                assert payload['max_curve_relative_error'] < previous[eta]
            previous[eta] = payload['max_curve_relative_error']


if __name__ == '__main__':
    main()
