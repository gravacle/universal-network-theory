"""Read-only saved arithmetic audit; no producer import or orbit calculation."""
import base64
import hashlib
import json
import math
from pathlib import Path
import zlib

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
NAME='FINITE_GAP_PHOTON_BUDGET_V001'

def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    result=HERE/(NAME+'_RESULTS.json'); frozen=HERE/(NAME+'_FROZEN.json')
    assert sha(result)=='23feee802337320fde647fe87ff3ff24b1006c935cc3f31d9cf6a4a9574dba10'
    v=json.loads(result.read_text());p=v['payload']
    assert sha(frozen)==v['freeze_sha256']
    assert hashlib.sha256(encode(p)).hexdigest()==v['payload_sha256']
    assert p['status']=='COMPLETE' and p['failures']==[]
    files={};seen=set();occurrences=0
    def manifest(path):
        nonlocal occurrences
        path=path.resolve();path.relative_to(ROOT)
        if path in seen:return
        seen.add(path)
        for name,h in json.loads(path.read_text())['files'].items():
            q=Path(name);options=[q] if q.is_absolute() else [ROOT/q,path.parent/q]
            owned={c.resolve() for c in options if c.resolve().is_relative_to(ROOT) and c.is_file()}
            assert len(owned)==1
            f=owned.pop();assert sha(f)==h
            files[str(f.relative_to(ROOT))]=h;occurrences+=1
            if f.name.endswith('_FROZEN.json'):manifest(f)
    manifest(frozen)
    t=json.loads((HERE/'FINITE_GAP_SHARED_SCREEN_V002_TRANSPORT.json').read_text())
    z=zlib.decompressobj();raw=z.decompress(base64.b64decode(t['data'],validate=True))+z.flush()
    assert z.eof and not z.unused_data and not z.unconsumed_tail
    assert len(raw)==t['raw_bytes'] and hashlib.sha256(raw).hexdigest()==t['raw_sha256']
    ov=json.loads(raw);old=ov['payload']
    assert hashlib.sha256(encode(old)).hexdigest()==ov['payload_sha256']
    photons=json.loads((HERE/'RADIATION_PHOTON_REFERENCE_V001_RESULTS.json').read_text())
    calibration=json.loads((HERE/'GLOBAL_GAP_LIMIT_CALIBRATION_V001_RESULTS.json').read_text())['payload']
    refs={r['reference']:r for r in photons['references']}
    assert len(refs)==len(calibration['references'])==18
    assert all(refs[i]['inherited_reference']==r for i,r in enumerate(calibration['references']))
    expected={(s,r,R) for s in range(4) for r in range(18) for R in [32,128,512,2048,8192]}
    assert len(p['rows'])==360 and {(r['spectrum_index'],r['reference'],r['R']) for r in p['rows']}==expected
    assert sum(p['counts'].values())==2182
    checks=0;maximum=0.;failures=[]
    def ck(name,a,b,scale=None):
        nonlocal checks,maximum
        den=max(abs(a),abs(b),1e-300) if scale is None else max(abs(scale),1e-300)
        err=abs(a-b)/den;checks+=1;maximum=max(maximum,err)
        if not math.isfinite(err) or err>2e-11:failures.append(dict(check=name,error=err))
    # Log-Beta expression rather than the producer's direct Gamma ratio.
    C=math.exp(4/3*(math.log(math.pi)-math.lgamma(.25)-math.lgamma(1.5)+math.lgamma(1.75)))
    ck('quartic_normalization',C,p['C'])
    A=1101;beta=.005
    for r in p['rows']:
        src=old['rows'][r['source_row_index']];ref=calibration['references'][r['reference']]
        assert (src['spectrum_index'],src['reference'],src['R'])==(r['spectrum_index'],r['reference'],r['R'])
        ck('same_present_action',r['I'],src['I']);ck('same_present_energy',r['E_present'],src['E'])
        ck('same_reference_density',r['Omega_exc'],ref['Omega_exc'])
        og=refs[r['reference']]['Omega_gamma'];ck('same_photon_reference',r['Omega_gamma'],og)
        q=beta*C*math.exp(4/3*math.log(src['I']))
        d=r['R']**2*math.sqrt(beta*q)
        ck('Q',r['Q'],q);ck('D',r['D'],d)
        ck('Q_over_E',r['Q_over_E'],q/src['E'])
        asym=ref['Omega_exc']/og*q/src['E']
        finite=ref['Omega_exc']/og/A*src['early_dust_ratio']
        upper=ref['Omega_exc']/og*d/(src['E']*A*A)
        ck('asymptote_photon_ratio',r['asymptote_over_photons'],asym)
        ck('finite_photon_ratio_from_dust_factor',r['at_A1101_over_photons'],finite)
        ck('finite_photon_ratio_direct',r['at_A1101_over_photons'],ref['Omega_exc']*src['early_E']/(og*src['E']*A**4))
        ck('finite_upper_difference',r['upper_difference_bound_A1101'],upper)
        ck('finite_lower_bound',min(finite-asym,0),0,max(finite,asym))
        ck('finite_upper_bound',max(finite-asym-upper,0),0,max(finite,asym+upper))
        ck('same_early_w',r['w_at_A1101'],beta*src['early_p']/src['early_E'])
        ck('same_early_action',src['early_I'],A**3*src['I'])
        for eps,value in r['A_sufficient_for_fractional_quartic_error'].items():
            ck('asymptotic_accuracy_epoch',float(eps)*q*value*value,d)
    groups=[]
    for saved in p['summaries']:
        rows=[r for r in p['rows'] if r['R']==saved['R']];assert len(rows)==saved['rows']==72
        ranges={k:[min(r[k] for r in rows),max(r[k] for r in rows)] for k in saved['ranges']}
        for key,extrema in ranges.items():
            for a,b in zip(extrema,saved['ranges'][key]):ck('range_'+key,a,b)
        groups.append(dict(R=saved['R'],rows=72,ranges=ranges,
            sufficient_A_1percent=[min(r['A_sufficient_for_fractional_quartic_error']['0.01'] for r in rows),max(r['A_sufficient_for_fractional_quartic_error']['0.01'] for r in rows)]))
    out=dict(status='PASS' if not failures else 'FAIL',checks=checks,max_relative_error=maximum,failures=failures,
        custody=dict(result_sha256=sha(result),freeze_sha256=sha(frozen),payload_sha256=v['payload_sha256'],
            source_sha256=sha(HERE/'finite_gap_photon_budget_v001.py'),protocol_sha256=sha(HERE/'FINITE_GAP_PHOTON_BUDGET_PROTOCOL_V001.md'),
            unique_files=len(files),manifests=len(seen),member_occurrences=occurrences),
        producer=dict(rows=360,checks=2182,max_reported_error=max(p['maxima'].values()),seconds=p['seconds'],peak_self_rss_bytes=p['peak_self_rss_bytes']),
        summaries=groups,
        scope='Saved scalar arithmetic only, no orbit or producer execution. Finite-A ratio is total excitation relative to ordinary photons, not extra radiation when w is matter-like. Formal asymptote and finite epoch must not be conflated. No BBN/CMB acceptance or network-photon identification.')
    print(json.dumps(out,sort_keys=True,indent=2,allow_nan=False))

if __name__=='__main__':main()
