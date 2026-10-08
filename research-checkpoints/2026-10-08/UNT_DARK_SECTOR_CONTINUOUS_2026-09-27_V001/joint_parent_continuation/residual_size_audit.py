"""Post-existing-data arithmetic audit. No field solve, new fit or acceptance gate."""
import hashlib
import json
import math
from pathlib import Path
from statistics import median

BASE = Path(__file__).resolve().parent
A0 = 1.2e-10
KPC_M = 3.085677581491367e19


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unwrap(name):
    obj = json.loads((BASE / name).read_text())
    raw = json.dumps(obj['payload'], sort_keys=True, separators=(',', ':'),
                     allow_nan=False).encode()
    assert hashlib.sha256(raw).hexdigest() == obj['payload_sha256'], name
    assert obj['freeze_sha256'] == digest(BASE / 'HALOGAS_FIELD_FROZEN.json'), name
    return obj['payload']


def summarize(rows):
    n = len(rows)
    residual = [r['prediction'] - r['velocity'] for r in rows]
    assert all(math.isclose(a, r['residual'], abs_tol=1e-10)
               for a, r in zip(residual, rows))
    rms = math.sqrt(sum(x*x for x in residual) / n)
    vtyp = median(r['velocity'] for r in rows)
    return dict(n=n, rms_kms=rms, mean_signed_residual_kms=sum(residual)/n,
                median_observed_speed_kms=vtyp,
                rms_over_median_observed_speed_descriptive=rms/vtyp,
                max_abs_residual_kms=max(map(abs, residual)))


def last_row(r):
    dv = r['prediction'] - r['velocity']
    dv2 = r['prediction']**2 - r['velocity']**2
    dg = dv2 / r['R']
    return dict(R_kpc=r['R'], observed_kms=r['velocity'],
                predicted_kms=r['prediction'], signed_delta_v_kms=dv,
                signed_delta_v_fraction=dv/r['velocity'],
                signed_delta_v_squared_kms2=dv2,
                signed_delta_g_kms2_per_kpc=dg,
                signed_delta_g_m_s2=dg*1e6/KPC_M,
                signed_delta_g_over_a0=dg*1e6/KPC_M/A0,
                signed_delta_g_over_observed_g=dv2/r['velocity']**2)


def differences(left, right):
    assert [(r['R'], r['velocity'], r['error']) for r in left] == [
        (r['R'], r['velocity'], r['error']) for r in right]
    delta = [a['prediction']-b['prediction'] for a,b in zip(left,right)]
    k = max(range(len(delta)), key=lambda i: abs(delta[i]))
    return dict(max_abs_delta_v_kms=abs(delta[k]), radius_of_max_kpc=left[k]['R'],
                signed_delta_at_max_kms=delta[k],
                rms_delta_v_kms=math.sqrt(sum(d*d for d in delta)/len(delta)))


def main():
    receipt = unwrap('HALOGAS_FIELD_RESULTS.json')
    assert receipt['status'] == 'COMPLETE'
    source_hashes = {}
    cases = {}
    for name, expected in receipt['case_files_sha256'].items():
        assert digest(BASE/name) == expected, name
        source_hashes[name] = expected
        cases[name] = unwrap(name)
        assert all(cases[name]['checks'].values()), name
    assert len(cases) == 8
    out = {}
    cuts = {'all_43':0, 'R_ge_2_kpc':2, 'R_ge_8_kpc':8, 'R_ge_35_kpc':35}
    fine = {}
    for width in (40,120):
        stem = f'HALOGAS{width}_ML36_RETAINED_V001'
        net = cases[f'{stem}_N512_L255_Newton0.json']['comparison']
        newton = cases[f'{stem}_N512_L255_Newton1.json']['comparison']
        coarse = cases[f'{stem}_N256_L255_Newton0.json']['comparison']
        remote = cases[f'{stem}_N320_L1023_Newton0.json']['comparison']
        fine[width] = net
        assert len(net)==43
        summaries = {}
        for label,cut in cuts.items():
            nr = [r for r in net if r['R']>=cut]
            br = [r for r in newton if r['R']>=cut]
            summaries[label] = {'network':summarize(nr), 'same_source_newtonian':summarize(br)}
            summaries[label]['rms_ratio_network_over_newtonian'] = (
                summaries[label]['network']['rms_kms']/summaries[label]['same_source_newtonian']['rms_kms'])
        out[str(width)] = dict(summaries=summaries,
                              last_row_network=last_row(net[-1]),
                              last_row_newtonian=last_row(newton[-1]),
                              fine_minus_coarse=differences(net,coarse),
                              remote_minus_coarse=differences(remote,coarse))
    result = dict(role='Descriptive audit of existing predictions; no significance, fit, new field, or new physics acceptance.',
                  source_hashes=source_hashes,
                  receipt_sha256=digest(BASE/'HALOGAS_FIELD_RESULTS.json'),
                  source_script_sha256=digest(Path(__file__)),
                  cases=out,
                  source_representation_40_minus_120=differences(fine[40],fine[120]))
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == '__main__':
    main()
