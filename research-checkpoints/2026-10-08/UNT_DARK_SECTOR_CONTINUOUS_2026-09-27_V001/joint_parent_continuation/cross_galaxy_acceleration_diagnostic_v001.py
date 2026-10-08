"""Exploratory arithmetic on all saved rows; no field solve, fit or new law."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DDO = ROOT/'external_ddo154_v001'
OUTPUT = ROOT/'CROSS_GALAXY_ACCELERATION_DIAGNOSTIC_V001.json'
A0 = 1.2e-10
KPC_M = 3.085677581491367e19
A0_UNITS = A0*KPC_M/1e6


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def load(path, freeze):
    wrapped = json.loads(path.read_text())
    assert wrapped['freeze_sha256'] == sha(freeze)
    assert wrapped['payload_sha256'] == hashlib.sha256(encode(wrapped['payload'])).hexdigest()
    return wrapped['payload']


def row(radius, observed, predicted, error):
    assert radius > 0 and all(math.isfinite(v) for v in (radius, observed, predicted, error))
    go, gp = observed**2/(radius*A0_UNITS), predicted**2/(radius*A0_UNITS)
    return {'R_kpc': radius, 'observed_kms': observed, 'predicted_kms': predicted,
            'quoted_error_kms': error, 'delta_v_kms': predicted-observed,
            'g_observed_over_a0': go, 'g_predicted_over_a0': gp,
            'delta_g_over_a0': gp-go,
            'fractional_acceleration_excess': gp/go-1 if go else None}


def describe(rows):
    assert all(rows[i]['R_kpc'] < rows[i+1]['R_kpc'] for i in range(len(rows)-1))
    def sign(value):
        return (value > 0)-(value < 0)
    crossings = [[a, b] for a,b in zip(rows, rows[1:])
                 if sign(a['delta_v_kms']) != sign(b['delta_v_kms'])]
    start = len(rows)
    while start and rows[start-1]['delta_v_kms'] > 0:
        start -= 1
    terminal = rows[start:]
    bracket = rows[max(0, start-1):start+1] if terminal else []
    return {'all_row_count': len(rows), 'all_rows': rows,
        'every_sign_change_bracket': crossings,
        'terminal_positive_count': len(terminal),
        'terminal_positive_start_bracket': bracket,
        'terminal_positive_g_observed_range': [min(r['g_observed_over_a0'] for r in terminal),
            max(r['g_observed_over_a0'] for r in terminal)] if terminal else None,
        'terminal_positive_delta_g_range': [min(r['delta_g_over_a0'] for r in terminal),
            max(r['delta_g_over_a0'] for r in terminal)] if terminal else None,
        'outermost': rows[-1],
        'scope': 'Exact residual signs in saved samples, not a statistically certified transition or a new radial cut.'}


def main():
    assert not OUTPUT.exists(), 'Retain earlier diagnostic; do not overwrite.'
    inputs, models = {}, {}
    receipt_path = ROOT/'HALOGAS_FIELD_RESULTS.json'
    assert sha(receipt_path) == '24729fb613fb3da2a07c41155cabd17898954f15cca3ae21d83f5fa00f54466d'
    receipt = load(receipt_path, ROOT/'HALOGAS_FIELD_FROZEN.json')
    assert receipt['status'] == 'COMPLETE'
    inputs[receipt_path.name] = sha(receipt_path)
    inputs['HALOGAS_FIELD_FROZEN.json'] = sha(ROOT/'HALOGAS_FIELD_FROZEN.json')
    for width in (40, 120):
        name = f'HALOGAS{width}_ML36_RETAINED_V001_N512_L255_Newton0.json'
        path = ROOT/name
        assert sha(path) == receipt['case_files_sha256'][name]
        p = load(path, ROOT/'HALOGAS_FIELD_FROZEN.json')
        assert all(p['checks'].values()) and len(p['comparison']) == 43
        inputs[name] = sha(path)
        models[f'NGC3198_{width}'] = describe([row(r['R'], r['velocity'], r['prediction'], r['error'])
                                             for r in p['comparison']])
    ddo_path = DDO/'ROTATION_COMPARISON.json'
    assert sha(ddo_path) == '36d11667ee7ca1cd534db91bef3a18cb735a07a74d69bbc0d29ca53f2299ed65'
    scored = load(ddo_path, DDO/'SCORING_FROZEN.json')
    assert scored['status'] == 'COMPLETE_DESCRIPTIVE_COMPARISON' and all(scored['checks'].values())
    inputs[str(ddo_path.relative_to(ROOT))] = sha(ddo_path)
    inputs['external_ddo154_v001/SCORING_FROZEN.json'] = sha(DDO/'SCORING_FROZEN.json')
    for label in ('NA', 'RO'):
        data = scored['models'][label]['comparison']
        assert len(data) == 12
        models[f'DDO154_{label}'] = describe([row(r['R_kpc'], r['observed_velocity_kms'],
            r['candidate']['prediction_kms'], r['quoted_error_kms']) for r in data])
    result = {'role': 'Exploratory diagnostic after both curves were scored. No new field, fitted scale or physical acceptance.',
        'inputs_sha256': inputs, 'source_sha256': sha(Path(__file__)),
        'acceleration_normalization_m_s2': A0, 'models': models,
        'interpretation_rules': [
            'All 43 NGC3198 and all 12 DDO154 rows, with both correlated source representations, remain.',
            'A terminal positive run is a descriptive sign census; no points are excluded from scientific scores.',
            'No common threshold is fitted or inferred as an intrinsic network constant.',
            'Disk geometry makes a local baryonic-force ratio an invalid substitute for solving the nonlinear field equation.',
            'Different observational products, source geometry, omitted matter and covariance limits remain unchanged.']}
    result['payload_sha256'] = hashlib.sha256(encode(result)).hexdigest()
    with OUTPUT.open('x') as stream:
        json.dump(result, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({name: {k: v for k,v in model.items() if k in
        ('all_row_count', 'terminal_positive_count', 'terminal_positive_start_bracket',
         'terminal_positive_g_observed_range', 'terminal_positive_delta_g_range', 'outermost')}
        for name,model in models.items()}, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
