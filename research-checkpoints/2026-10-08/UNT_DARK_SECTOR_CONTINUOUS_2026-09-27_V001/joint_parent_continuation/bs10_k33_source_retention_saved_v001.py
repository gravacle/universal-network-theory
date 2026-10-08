#!/usr/bin/env python3
"""One saved-array projection application; no Hamiltonian or propagation."""
from pathlib import Path
import argparse, hashlib, json, math, os, sys

J=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
PARENT=J/'BS10_K33_NODAL_SIGNAL_V001_RESULT.json'
CP=J/'bs10_k33_nodal_signal_v001_checkpoints'
PROTOCOL=J/'NATIVE_UNCLAMPED_SOURCE_RETENTION_APPLICATION_V001.md'
OUT=J/'BS10_K33_SOURCE_RETENTION_SAVED_V001_RESULT.json'
REPORT=J/'BS10_K33_SOURCE_RETENTION_SAVED_V001_RESULT.md'
SOURCE=Path(__file__).resolve()

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()

def canonical(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def exclusive(p,x):
    with p.open('x',encoding='utf8') as f:
        json.dump(x,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parent-sha256',required=True)
    args=parser.parse_args()
    if sys.platform!='darwin':raise RuntimeError('Same Mac only')
    if OUT.exists() or REPORT.exists():raise RuntimeError('Exclusive outputs exist; preserve them')
    if sha(PARENT)!=args.parent_sha256:raise RuntimeError('Parent receipt digest mismatch')
    parent=json.loads(PARENT.read_text());copy=dict(parent);digest=copy.pop('canonical_payload_sha256')
    if canonical(copy)!=digest or parent['status']!='QUALIFIED_ARITHMETIC' or parent['failed_count']:
        raise RuntimeError('Parent canonical/qualification gate failed')
    custody=dict(parent['manifest']['input_sha256'])
    for p,h in custody.items():
        if sha(Path(p))!=h:raise RuntimeError('Original input digest mismatch: '+p)
    if json.loads((CP/'manifest.json').read_text())!=parent['manifest']:raise RuntimeError('Parent manifest mismatch')
    events=[json.loads(s) for s in (CP/'events.jsonl').read_text().splitlines() if s]
    if not any(e['event']=='result_saved' and e['sha256']==args.parent_sha256 for e in events):raise RuntimeError('Parent result journal mismatch')
    custody.update({str(PARENT):args.parent_sha256,str(CP/'manifest.json'):sha(CP/'manifest.json'),str(CP/'events.jsonl'):sha(CP/'events.jsonl'),str(PROTOCOL):sha(PROTOCOL),str(SOURCE):sha(SOURCE)})
    import numpy as np
    rows=[];checks=[]
    def check(name,ok,evidence):checks.append(dict(name=name,passed=bool(ok),evidence=evidence))
    expected={(g,n,a) for g in (0.,.1) for n in (0,413) for a in (0.,5.,20.,50.)}
    actual={(r['g'],r['start'],r['age']) for r in parent['rows']}
    if actual!=expected or len(parent['rows'])!=16:raise RuntimeError('Frozen16-row census mismatch')
    for row in parent['rows']:
        key=f'g{int(row["g"]>0)}_n{row["start"]}_age{int(row["age"])}'
        rp=CP/(key+'.json');bp=Path(row['bundle_path'])
        rh=sha(rp);bh=sha(bp)
        if json.loads(rp.read_text())!=row or bh!=row['bundle_sha256']:raise RuntimeError('Parent row/bundle mismatch')
        if not any(e['event']=='row_complete' and e['key']==key and e['sha256']==rh and e['failed']==0 for e in events):raise RuntimeError('Parent row journal mismatch')
        if not any(e['event']=='bundle_saved' and e['key']==key and e['sha256']==bh for e in events):raise RuntimeError('Parent bundle journal mismatch')
        custody[str(rp)]=rh;custody[str(bp)]=bh
        with np.load(bp,allow_pickle=False) as z:
            cols=z['input_columns'];metadata=json.loads(str(z['metadata_json']))
            if metadata['input_sha256']!=parent['manifest']['input_sha256'] or (metadata['g'],metadata['start'],metadata['age'])!=(row['g'],row['start'],row['age']):raise RuntimeError('Parent array metadata mismatch')
        if cols.shape!=(3,196608) or not np.all(np.isfinite(cols)):raise RuntimeError('Input array shape/finite gate failed')
        psi=cols[0].reshape(512,6,64).transpose(1,0,2).reshape(6,-1)
        xi=cols[1].reshape(512,6,64).transpose(1,0,2).reshape(6,-1)
        prob=np.sum(np.abs(psi)**2,axis=1)
        overlaps=np.array([np.vdot(p,x) for p,x in zip(psi,xi)])
        xi2=float(np.vdot(xi,xi).real);positive=prob>0
        retained=float(np.sum(np.abs(overlaps[positive])**2/prob[positive]))
        raw=xi2-retained;residual=xi.copy()
        for v in range(6):
            if prob[v]>0:residual[v]-=psi[v]*(overlaps[v]/prob[v])
        explicit=float(np.vdot(residual,residual).real)
        orth=max(abs(np.vdot(psi[v],residual[v])) for v in range(6))
        tolerance=5e-11*max(1.,xi2)
        check(key+'_two_projection_forms',abs(raw-explicit)<=tolerance,dict(raw=raw,explicit=explicit,tolerance=tolerance))
        check(key+'_raw_nonnegative_with_roundoff',raw>=-tolerance,dict(raw=raw,tolerance=tolerance))
        check(key+'_residual_orthogonal',orth<=tolerance,dict(residual=orth,tolerance=tolerance))
        ref=np.array([row['response'][0]['means'][f'carrier{v}'] for v in range(6)])
        err=float(np.max(np.abs(prob-ref)));check(key+'_same_carrier_probabilities',err<=tolerance,dict(error=err,tolerance=tolerance))
        if row['age']==0:
            target=.03+(0.005 if row['start']==413 else 0)+row['g']**2
            check(key+'_analytic_initial_coefficient',abs(explicit-target)<=tolerance,dict(actual=explicit,expected=target,tolerance=tolerance))
        rows.append(dict(g=row['g'],start=row['start'],age=row['age'],carrier_probabilities=prob.tolist(),retained_rank=int(np.sum(positive)),minimum_positive_probability=float(prob[positive].min()),source_vector_norm_squared=xi2,retained_source_norm_squared=retained,raw_subtraction_leakage_squared=raw,explicit_residual_leakage_squared=explicit,subtraction_residual=raw-explicit,orthogonality_residual=orth,tolerance=tolerance,source_bundle_sha256=bh))
    for p,h in custody.items():
        if sha(Path(p))!=h:raise RuntimeError('Custody changed during extraction: '+p)
    failed=[c for c in checks if not c['passed']]
    output=dict(status='QUALIFIED_SAVED_ARRAY_ARITHMETIC' if not failed else 'FAILED_SAVED_ARRAY_ARITHMETIC',qualification='Frozen actual-state carrier-space source tangent only; no full-subspace invariance, irreversible loss, gravity or continuum claim',input_sha256=custody,parent_sha256=args.parent_sha256,pid=os.getpid(),rows=rows,checks=checks,passed_count=len(checks)-len(failed),failed_count=len(failed))
    output['canonical_payload_sha256']=canonical(output);exclusive(OUT,output)
    lines=['# Unclamped complete-source retention: saved-array result','',f"{output['status']}: {output['passed_count']}/{len(checks)} numerical controls.",'',output['qualification'],'','| g | start | age | conditional rank | actual source leakage squared |','|---:|---:|---:|---:|---:|']
    lines += [f"|{r['g']}|{r['start']}|{r['age']}|{r['retained_rank']}|{r['explicit_residual_leakage_squared']:.12g}|" for r in rows]
    lines += ['',f'Parent result SHA256: {args.parent_sha256}',f'Saved-array result SHA256: {sha(OUT)}','', 'All exact zero-probability sectors and raw subtraction residuals are retained. No probability threshold, clipping, Hamiltonian call, helper import, eigensolver or propagation.']
    with REPORT.open('x',encoding='utf8') as f:f.write('\n'.join(lines)+'\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status=output['status'],passed=output['passed_count'],failed=output['failed_count'],result_sha256=sha(OUT))))
    return int(bool(failed))

if __name__=='__main__':sys.exit(main())
