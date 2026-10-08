"""Saved-state audit of the assembly linear transfer; no new evolution.

Check every PREFIX of the retained history with the inherited1e-4 relative
component gate/floor1e-30, so a huge endpoint cannot mask early error.
Also report adjacent-epoch segment errors (same gate, no zero crossing
division), gauge-invariant charge/current identity and baryon rest-slice
contrasts, and the COMPLETE metric-source decomposition. Tests at seeds
1e-5,1e-9,1e-12 and domain fractions .1/1 are ILLUSTRATIVE breakdown
diagnostics, not observations or selected primordial amplitudes. Include
C*j/mu because the J constitutive correction may matter before p/bs=1.
Frozen-time eigenvalues are descriptive, not a time-dependent stability
proof. No fit, branch clipping, new physical assumption, or lane closure.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np
import invariant_clock_compression_assembly_v001 as assembly

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'INVARIANT_CLOCK_COMPRESSION_ASSEMBLY_V001_RESULT.json'
OUT=ROOT/'INVARIANT_CLOCK_ASSEMBLY_AUDIT_V001_RESULT.json'
EXPECTED='b2043bf559fb5aed6b22386183a389062e7b2698bc9e9575083ead6825121f10'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if OUT.exists():raise FileExistsError(OUT)
    if sha(SOURCE)!=EXPECTED:raise ValueError('changed assembly evidence')
    src=json.loads(SOURCE.read_text())
    if sha(Path(assembly.__file__))!=src['producer_sha256']:raise ValueError('changed producer')
    for path,digest in src['dependencies'].items():
        if sha(Path(path))!=digest:raise ValueError('changed dependency')
    saved=json.loads(assembly.linear.old.base.SOURCE.read_text())
    saved['inherited']=src['fixed'];model=assembly.linear.old.base.Model(saved,1)
    run=assembly.Assembly(model);hist=src['histories'];fine=hist[-1]['snapshots']
    controls=[];prefixes={};segments={}
    def check(name,error,gate):
        controls.append(dict(name=name,error=float(error),gate=gate,passed=bool(error<=gate)))
    for key in ('state','observables'):
        aa=np.array([s[key] for s in hist[-2]['snapshots']])
        bb=np.array([s[key] for s in fine]);pref=[];seg=[]
        for i in range(1,len(fine)):
            num=np.max(abs(aa[:i+1]-bb[:i+1]),axis=0)
            den=np.maximum(np.max(abs(bb[:i+1]),axis=0),1e-30)
            errors=num/den
            pref.append(dict(a=fine[i]['a'],maximum=float(errors.max()),by_component=errors.tolist()))
            errors=np.max(abs(aa[i-1:i+1]-bb[i-1:i+1]),axis=0)/np.maximum(np.max(abs(bb[i-1:i+1]),axis=0),1e-30)
            seg.append(dict(a=fine[i]['a'],maximum=float(errors.max()),by_component=errors.tolist()))
        prefixes[key]=pref;segments[key]=seg
        check('all_prefix_'+key,max(r['maximum'] for r in pref),1e-4)
        check('all_adjacent_segment_'+key,max(r['maximum'] for r in seg),1e-4)
    rows=[];current_error=0.;decomposition_error=0.
    for s in fine:
        x=math.log(s['a']);a,Q,m,d,H,Hd,Hdx,rb,k2=run.bg(x)
        dm,phi,alpha,Z,db,theta=np.array(s['state']);rel=phi+Q*alpha
        y=np.vstack((dm,rel,alpha,Z,db,theta))/run.scale[:,None]
        rhs=run.rhs(x,np.vstack((y,np.zeros(2))))[:6]*run.scale[:,None]*H
        E=(Z-model.C*rel)/model.KB;D=model.C*(E-rel)
        Jrel=D-m/Q*(phi-Q*theta)
        Sdot=rhs[0]/m+3*H*dm/m-rhs[4];target=k2/m*Jrel
        current_error=max(current_error,float(np.max(abs(Sdot-target)/np.maximum(abs(rhs[0]/m)+abs(3*H*dm/m)+abs(rhs[4])+abs(target),1e-100))))
        pieces=np.array([Z/2,-Q*dm/(2*k2),-rb*db/(2*k2),-3*H*(m*phi+rb*theta)/(2*k2)])
        Phi=np.array(s['observables'][0]);decomposition_error=max(decomposition_error,float(np.max(abs(pieces.sum(axis=0)-Phi)/np.maximum(np.sum(abs(pieces),axis=0),1e-100))))
        row=dict(a=a,relative_charge=(dm/m-db).tolist(),relative_current=Jrel.tolist(),
            baryon_rest_clock_contrast=(dm/m+3*H*theta).tolist(),
            baryon_rest_ordinary_contrast=(db+3*H*theta).tolist(),
            potential_pieces=pieces.tolist(),potential_piece_fractions=(pieces/Phi).tolist(),
            effective_Phi_over_baryon_Phi=(Phi/pieces[2]).tolist(),
            clock_energy_over_ordinary_energy=(Q*dm/(rb*db)).tolist())
        # Matrix eigenvalues per e-fold, only a frozen-time diagnostic.
        matrix=run.matrix(x);vals,vec=np.linalg.eig(matrix)
        residual=np.linalg.norm(matrix@vec-vec*vals,axis=0)/(np.linalg.norm(matrix,2)*np.linalg.norm(vec,axis=0)+abs(vals)*np.linalg.norm(vec,axis=0))
        row['frozen_eigenvalues_per_log_a']=[[float(v.real),float(v.imag)] for v in vals]
        row['frozen_eigen_residual']=float(max(residual))
        row['unit_seed_linear_domain']=s['linear_unit_seed_domain']
        row['amplitude_domains']={}
        for amplitude in (1e-5,1e-9,1e-12):
            domain={k:(amplitude*np.array(v)).tolist() for k,v in s['linear_unit_seed_domain'].items()}
            p=amplitude*np.sqrt(k2)*abs(rel)
            domain['Cj_over_mu']=(model.C*model.lam*p/np.sqrt(p*p+model.bs**2)/(m/Q)).tolist()
            row['amplitude_domains'][str(amplitude)]=domain
        rows.append(row)
    check('gauge_invariant_relative_current',current_error,1e-12)
    check('complete_metric_source_sum',decomposition_error,1e-12)
    check('frozen_eigen_backward_residual',max(r['frozen_eigen_residual'] for r in rows),1e-12)
    crossings=[]
    for amplitude in (1e-5,1e-9,1e-12):
        for seed in (0,1):
            for threshold in (.1,1.):
                found=None
                for i,row in enumerate(rows):
                    dom=row['amplitude_domains'][str(amplitude)]
                    values={k:v[seed] for k,v in dom.items()}
                    if max(values.values())>=threshold:
                        found=dict(last_below_a=rows[i-1]['a'] if i else None,
                            first_saved_exceedance_a=row['a'],trigger=max(values,key=values.get),values=values)
                        break
                crossings.append(dict(illustrative_amplitude=amplitude,seed=seed,threshold=threshold,crossing=found))
    result=dict(protocol=__doc__,producer_sha256=sha(Path(__file__)),source_sha256=EXPECTED,
        dependencies={str(p):sha(p) for p in (Path(assembly.__file__),Path(assembly.linear.__file__))},
        controls=controls,all_controls_passed=all(c['passed'] for c in controls),prefixes=prefixes,segments=segments,
        potential_piece_order=['Z_over_2','clock_density','ordinary_density','momentum'],rows=rows,
        illustrative_domain_crossings=crossings,physical_linear_domain_required=True,
        nonlinear_formation=False,observational_superiority=False)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(controls=controls,crossings=crossings,selected_rows=[rows[i] for i in (0,1,8,16,32,48,64)],sha256=sha(OUT)),indent=2),flush=True)
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
