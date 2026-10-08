"""Saved-state scalar charge audit: no evolution, fit or acceptance change.

Compare the implemented split divergence with the equivalent combined
flux divergence and the point-value quadrature's integral budget. Report
defects, not an automatic failure of continuum charge conservation. The
quadrature/derivative pair is not assumed to telescope. Ordinary FV mass
budgets cannot substitute for this independent scalar current audit.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import invariant_clock_polar_source_v005 as source
from invariant_clock_polar_compare_v002 import interpolation

BASE=Path(__file__).resolve().parent


def main():
    rows=[];identities={}
    for tag in ('MIXED02','MIXED03','MIXED04'):
        path=BASE/('INVARIANT_CLOCK_POLAR_SOURCE_'+tag+'_RESULT.json')
        receipt=json.loads(path.read_text());cp_path=BASE/receipt['checkpoint']
        cp=json.loads(cp_path.read_text());z=np.array(cp['state'])
        model=source.Polar(json.loads(source.prev.inherited.SOURCE.read_text()),
                           receipt['args']['nodes'],receipt['args']['extent'])
        model.initial();t=cp['step']*cp['dt'];dz,g=model.rhs(t,z,True)
        r=model.r;mask=model.mask;flux=g['N']*g['cur']
        combined=-model.divergence(flux)
        regular=-(3*flux/r+r*model.derivative(flux/r))
        split=dz[3]
        budget_split=2*(model.massint@split+r*r*flux)
        budget_combined=2*(model.massint@combined+r*r*flux)
        budget_regular=2*(model.massint@regular+r*r*flux)
        rate_scale=max(float(np.max(abs(split[mask]))),1e-30)
        flux_scale=max(float(np.max(abs(2*r[mask]**2*flux[mask]))),1e-30)
        drift=split-combined;imax=np.argmax(abs(drift[mask]))
        # A polynomial calibration distinguishes pair/quadrature accuracy
        # from an exact finite-volume telescoping identity that is absent.
        poly=r+(.1/model.L**2)*r**3
        dpoly=3+(.5/model.L**2)*r**2
        polynomial_budget=2*(model.massint@dpoly-r*r*poly)
        rows.append(dict(tag=tag,nodes=model.n,
            split_combined_inner_relative=float(np.max(abs(drift[mask])))/rate_scale,
            split_regular_inner_relative=float(np.max(abs((split-regular)[mask])))/rate_scale,
            split_combined_peak_radius_over_L=float(r[mask][imax]/model.L),
            split_integral_budget_inner_relative=float(np.max(abs(budget_split[mask])))/flux_scale,
            combined_integral_budget_inner_relative=float(np.max(abs(budget_combined[mask])))/flux_scale,
            regular_integral_budget_inner_relative=float(np.max(abs(budget_regular[mask])))/flux_scale,
            global_split_budget=float(budget_split[-1]),global_combined_budget=float(budget_combined[-1]),
            polynomial_integral_pair_inner_relative=float(np.max(abs(polynomial_budget[mask])))/float(np.max(abs(2*r[mask]**2*poly[mask]))),
            r=r[mask].tolist(),charge_change=(np.array(receipt['snapshots'][-1]['state'])[3]-np.array(receipt['snapshots'][0]['state'])[3]).tolist()))
        for p in (path,cp_path):identities[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    pairs=[]
    for a,b in zip(rows[:-1],rows[1:]):
        ra=np.array(a['r']);rb=np.array(b['r']);mask=(rb>=ra[2])&(rb<=ra[-3]);rr=rb[mask]
        left=interpolation(ra,np.array(a['charge_change'])[None,:],rr)[0]
        right=np.array(b['charge_change'])[mask];diff=right-left;ind=np.argmax(abs(diff))
        pairs.append(dict(left=a['tag'],right=b['tag'],maximum_radius_over_L=float(rr[ind]/model.L),
            absolute_difference=float(diff[ind]),right_charge_change=float(right[ind]),
            relative_change_error=float(np.max(abs(diff))/np.max(abs(right))),
            sign_changes=int(np.count_nonzero(np.diff(np.sign(diff))))) )
    for row in rows:
        del row['r'];del row['charge_change']
    for p in (Path(__file__),Path(source.__file__),Path(source.prev.__file__)):
        identities[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    result=dict(protocol=__doc__,rows=rows,pairs=pairs,identities=identities)
    out=BASE/'INVARIANT_CLOCK_POLAR_CHARGE_AUDIT_V001_RESULT.json'
    with out.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(result,allow_nan=False))


if __name__=='__main__':main()
