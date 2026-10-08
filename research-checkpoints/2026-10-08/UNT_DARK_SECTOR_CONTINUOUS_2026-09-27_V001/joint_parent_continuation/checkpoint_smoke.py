"""Tiny prospective interrupted/resumed-field check for the actual galaxy writer."""
import json
import hashlib
import sys
import numpy as np
import disk_solver as law
import axisymmetric_disk_v002 as disk
import galaxy_field_compute as runner

ROOT = law.ROOT


def main():
    path = ROOT/'CHECKPOINT_SMOKE_FROZEN.json'
    identity = {'files':{name:law.sha(ROOT/name) for name in ('checkpoint_smoke.py',
                'galaxy_field_compute.py','axisymmetric_disk_v002.py','axisymmetric_disk.py',
                'disk_solver.py','galaxy_density.py','NGC3198_BARYON_INPUT.json',
                '../joint_parent_dynamics/SHAPE_REFERENCE_RESULTS.json')},
                'definition':'N16 L8 eta1 Kuzmin; interrupt after5 completed updates; unchanged tolerances; compare resumed/full phi to1e-11 absolute.'}
    if sys.argv[1:] == ['freeze']:
        law.save_new(path,identity)
        return
    assert not sys.argv[1:]
    assert json.loads(path.read_text()) == identity
    freeze_hash = law.sha(path)
    n,extent,eta = 16,8.,1.
    geometry = e,c,w = disk.mesh(n,extent)
    sr = np.sqrt(extent**2+(c+1)**2)
    sz = np.sqrt(c*c+(extent+1)**2)
    pr = disk.spherical_potential(sr,eta)
    pz = disk.spherical_potential(sz,eta)
    tr = law.inverse(eta/sr**2)*(c+1)/sr
    tz = law.inverse(eta/sz**2)*c/sz
    bottom = eta*(1/np.sqrt(e[:-1]**2+1)-1/np.sqrt(e[1:]**2+1))
    boundary = pr,pz,tr,tz,bottom
    rr,zz = np.meshgrid(c,c,indexing='ij')
    initial = float(law.inverse(eta/4))/(eta/4)*eta*(1-1/np.sqrt(rr*rr+(zz+1)**2))
    full,force,history,ok = disk.solve(geometry,boundary,initial)
    checkpoint = ROOT/'CHECKPOINT_SMOKE_STATE.npz'
    writer = runner.checkpoint_writer(checkpoint,'smoke',freeze_hash)

    class SimulatedInterruption(Exception):
        pass

    def interrupt(phi,rows):
        if len(rows) == 5:
            writer(phi,rows)
            raise SimulatedInterruption()
    interrupted = False
    try:
        disk.solve(geometry,boundary,initial,checkpoint=interrupt)
    except SimulatedInterruption:
        interrupted = True
    saved,previous = runner.load_checkpoint(checkpoint,'smoke',freeze_hash,n)
    resumed,rforce,rhistory,rok = disk.solve(geometry,boundary,saved,history_start=previous)
    wrong_identity_rejected = wrong_freeze_rejected = False
    try:
        runner.load_checkpoint(checkpoint,'not-smoke',freeze_hash,n)
    except AssertionError:
        wrong_identity_rejected = True
    try:
        runner.load_checkpoint(checkpoint,'smoke','invalid-freeze',n)
    except AssertionError:
        wrong_freeze_rejected = True
    error = float(np.max(abs(full-resumed)))
    checks = {'uninterrupted_converged':ok,'interrupted_after_five':interrupted and len(previous)==5,
              'resumed_converged':rok,'field_agreement':error<=1e-11,
              'same_total_iterations':len(history)==len(rhistory),
              'wrong_case_rejected':wrong_identity_rejected,'wrong_freeze_rejected':wrong_freeze_rejected}
    payload = {'checks':checks,'maximum_phi_difference':error,
               'uninterrupted_updates':len(history),'resumed_total_updates':len(rhistory),
               'scope':'One exact benchmark exercising real rolling checkpoint path; not filesystem power-loss certification.'}
    law.save_new(ROOT/'CHECKPOINT_SMOKE_RESULTS.json',{'freeze_sha256':freeze_hash,
        'payload_sha256':hashlib.sha256(law.encode(payload)).hexdigest(),'payload':payload})
    print(json.dumps(payload),flush=True)
    assert all(checks.values())


if __name__ == '__main__':
    main()
