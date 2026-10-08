"""Root-owned SAVED scalar attribution; no producer imports or propagation."""
from pathlib import Path
from decimal import Decimal, getcontext
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
import os

BASE = Path(__file__).resolve().parent
STEM = 'CONSTRAINED_U_SAVED_CLOCK_CONSTRAINT_ATTRIBUTION_V001'
PARENT = 'CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002'
PINS = {
    'constrained_u_galaxy_horizon_stable_y_gauss_v002.py': 'f70826091d11c38715c00b3a572e08c48a41252018477ac4cf3a20b2ded9f531',
    PARENT+'_MANIFEST.json': '1def78ccec871fc95e9099b17ee4f05079f95804e51769b9cf3d37fb75904d94',
    PARENT+'_FINE_CP_002048.json': 'da6b2ce2b4576f9914dd88966b866ca5a48ca1e6685122f518a1f90df1bb2077',
    PARENT+'_FINE_CP_002048_COMMIT.json': '83fa8e2adcdc3f00adc612274112e68750b2b823c8ca09b6e857c764aa037cfc',
    PARENT+'_START_CP_001664.json': '8153f119a00e212f91cdab61a849dc4d390b0265f41167aefe87b9abd1d0b726',
    PARENT+'_START_CP_001664_COMMIT.json': 'c6f1ac9d7f17bee00165ba988b49c3ab56af3f6ae78656368aada5ff9ea94ac1',
    'CONSTRAINED_U_FINITE_START_FORCED_ENTROPY_DIAGNOSIS_V001.md': '37a552337ca647afb06d0315271badf5c3295828aaa1b5e6675844bd479b0b39',
    'CONSTRAINED_U_FINITE_START_FORCED_ENTROPY_PERCENTAGE_ADDENDUM_V001.md': '43c117506a131004bf372f5fae68eb7b500258283e5a406352582ded936e1e9d',
    STEM+'.md': 'cdda7ff38c1b64707b868f6928dd62f57679c6d6984c50c33bf4ce9907ba1d43',
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def number(value):
    assert type(value) in (int, float) and math.isfinite(value)
    return Decimal.from_float(float(value))

def encode(value):
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, list):
        return [encode(v) for v in value]
    return value

def write(name, value):
    p = BASE/name
    data = (json.dumps(encode(value), sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()
    with p.open('xb') as stream:
        stream.write(data)
    p.chmod(0o444)
    return digest(p)

def run():
    started = datetime.now(timezone.utc).isoformat()
    getcontext().prec = 80
    outputs = [STEM+s for s in ('_RESULT.json', '_REPORT.md', '_RECEIPT.json')]
    assert all(not (BASE/name).exists() for name in outputs), 'Preserve existing outputs'
    source_sha = digest(Path(__file__))
    for name, expected in PINS.items():
        assert digest(BASE/name) == expected and not (BASE/name).stat().st_mode & 0o222, name
    fine = json.loads((BASE/(PARENT+'_FINE_CP_002048.json')).read_text())
    start = json.loads((BASE/(PARENT+'_START_CP_001664.json')).read_text())
    for payload, label, step in ((fine, 'FINE', 2048), (start, 'START', 1664)):
        commit = json.loads((BASE/(PARENT+'_'+label+'_CP_'+str(step).zfill(6)+'_COMMIT.json')).read_text())
        assert commit['sha256'] == PINS[commit['payload']]
        assert commit['trial'] == payload['trial'] == label and commit['nstep'] == payload['nstep'] == step
        assert commit['lineage'] == payload['lineage']
    assert fine['lineage'] == start['lineage']
    initial = fine['snapshots'][0]
    common = next(s for s in start['snapshots'] if s['nstep'] == 128)
    assert initial['nstep'] == 0 and len(initial['cases']) == len(common['cases']) == 4
    fixed = fine['lineage']['fixed']; fg = number(fixed['fgamma'])
    kb, cbar = number(.02), number(.99)
    rows = []
    for arm, (old, new) in enumerate(zip(initial['cases'], common['cases'])):
        assert old['background'] == new['background'] and old['a'] == new['a']
        bg = old['background']; h, b, r, w, cs = [number(bg[k]) for k in ('h', 'b', 'r', 'w', 'cs')]
        rg, rn = r*fg, r*(1-fg)
        q = number(fixed['k_Mpc_inverse']*299792458./(1000*fixed['Hunit']*bg['a']))
        q2 = q*q
        denominator = b+4*r/3+w+kb*q2*cs/2
        assert denominator > 0
        records = []
        for case in (old, new):
            c = {k: number(v) for k, v in case['stable_coordinates'].items()}
            s = b*c['wb']+4*rg*c['wg']/3+4*rn*c['w_nu']/3
            records.append(dict(phase=c['Gamma_phase'], sbp=c['Gamma_b']-c['Gamma_phase'],
                sbg=c['Gamma_b']-3*c['Gamma_gamma']/4, sgn=c['Gamma_gamma']-c['Gamma_nu'],
                psi=number(case['Psi']), relative_momentum=s, vd=number(case['n_U'])+cs*c['Gamma_phase'],
                z=number(case['Z']), normal=number(case['normal_stable_residual'])))
            assert case['readouts'][10] == bg['w']*case['stable_coordinates']['Gamma_phase']
        delta = {key: records[1][key]-records[0][key] for key in records[0]}
        contributions = dict(normal=delta['normal']/denominator,
            metric=-q2*delta['psi']/denominator,
            relative_momentum=-3*h*delta['relative_momentum']/denominator,
            baryon_phase_entropy=-(b+4*r/3)*delta['sbp']/denominator,
            baryon_photon_entropy=4*r*delta['sbg']/(3*denominator),
            photon_neutrino_entropy=rn*delta['sgn']/denominator,
            native_velocity=kb*q2*delta['vd']/(2*denominator),
            native_storage=cbar*q*delta['z']/denominator)
        total = sum(contributions.values(), Decimal(0))
        rows.append(dict(arm=arm, omega=fine['lineage']['omegas'][arm], a=old['a'], q=q,
            denominator=denominator, input_records=records, signed_delta=delta,
            phase_contributions=contributions, contribution_sum=total,
            saved_phase_delta=delta['phase'], scalar_reconstruction_gap=delta['phase']-total,
            absolute_contribution_sum=sum(map(abs, contributions.values()), Decimal(0)),
            clock_density_delta=number(new['readouts'][10])-number(old['readouts'][10])))
    for name, expected in PINS.items():
        assert digest(BASE/name) == expected
    assert digest(Path(__file__)) == source_sha
    result = dict(status='COMPLETED_SAVED_SCALAR_DIAGNOSTIC', owner='root', pid=os.getpid(),
        started=started, ended=datetime.now(timezone.utc).isoformat(), source_sha256=source_sha,
        input_sha256=PINS, case_count=4, rows=rows,
        physical_seed_qualified=False, microscopic_macroscopic_causal_identity_qualified=False,
        original_failure_flags_changed=False, new_physical_threshold_applied=False)
    result_sha = write(outputs[0], result)
    report = ['# Saved clock constraint attribution V001', '',
        'Four unchanged first common frames; START minus FINE. Exact normal-constraint scalar attribution, not an independently identified cause or corrected seed.', '',
        '| Contribution to delta Gamma phase | omega0.1 |', '|---|---:|']
    report += ['| '+k+' | '+str(v)+' |' for k, v in rows[0]['phase_contributions'].items()]
    report += ['', 'Saved phase delta: '+str(rows[0]['saved_phase_delta']),
        'Scalar reconstruction gap: '+str(rows[0]['scalar_reconstruction_gap']),
        'All four arms and exact binary-decimal inputs remain in RESULT. No producer action, new propagation, state reset, thermal law or success threshold. Original failures remain.']
    report_path = BASE/outputs[1]
    with report_path.open('x') as stream:
        stream.write('\n'.join(report)+'\n')
    report_path.chmod(0o444)
    report_sha = digest(report_path)
    receipt_sha = write(outputs[2], dict(status=result['status'], owner='root', pid=os.getpid(),
        source_sha256=source_sha, input_sha256=PINS, result_sha256=result_sha, report_sha256=report_sha,
        closed=datetime.now(timezone.utc).isoformat()))
    print(json.dumps(dict(status=result['status'], pid=os.getpid(), rows=4,
        result_sha256=result_sha, report_sha256=report_sha, receipt_sha256=receipt_sha)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root-owned', action='store_true', required=True)
    parser.parse_args()
    run()
