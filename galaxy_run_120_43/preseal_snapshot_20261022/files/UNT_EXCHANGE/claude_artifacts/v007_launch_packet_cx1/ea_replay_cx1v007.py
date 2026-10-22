"""EA accepted route-A residual at registered radii, saved operators only.
RUN_DIR LABEL OUTPUT; --fixture permits C4R3/C5R3/C6R3 (explicit fixture labels).
No nonlinear solve. Formula = controller _rows_K/_normalize, no relaxation factor.
"""
import argparse,hashlib,importlib.util,json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).parent; ART=ROOT.parent
DRIVER=ART/'tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py'
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(2**22),b''):h.update(b)
    return h.hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def load(p):
    s=importlib.util.spec_from_file_location('ea_driver',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def recorded_entry(tail,radii,result_sha):
    if 'probe_R_m' not in tail:return None
    got=tail['probe_R_m'];rows=tail.get('E_A_rows_km_s_accepted');it=tail.get('accepted_iteration')
    if not isinstance(got,list) or len(got)!=12 or any(not math.isfinite(x) or abs(x-y)>1e-12*abs(y) for x,y in zip(got,radii)):raise ValueError('EA_RECORDED_RADII_MISMATCH')
    if not isinstance(rows,list) or len(rows)!=12 or any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or x<0 for x in rows):raise ValueError('EA_RECORDED_ROWS_INVALID')
    if isinstance(it,bool) or not isinstance(it,int) or it<0:raise ValueError('EA_RECORDED_ITERATION_INVALID')
    return {'result_sha256':result_sha,'E_A_rows_km_s':rows,'accepted_iteration':it,'row_radii_m':got}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('run');ap.add_argument('label');ap.add_argument('out');ap.add_argument('--fixture',action='store_true');a=ap.parse_args()
    run=Path(a.run); result=run/'result.json'; obj=json.loads(result.read_bytes())
    if a.fixture and (a.label not in ('C4R3','C5R3','C6R3') or a.label not in run.name):raise ValueError('fixture run mismatch')
    mod=load(DRIVER);mon=mod.uvt_route_a_monitor(json.loads((run/'inputs/seed_c2v001.json').read_bytes())['numerical_inputs'])
    if mon is None:raise ValueError('driver monitor API name must be verified before use')
    R=mon['probe_R_m'];v=np.asarray(mon['v_ref_km_s'],float)
    ro=obj.get('route_a_outcome') or {}
    if ro.get('result_path'):
        trp=Path(ro['result_path'])
        if sha(trp)!=ro['result_sha256']:raise ValueError('ROUTE_A_RESULT_PIN_MISMATCH')
        tr=json.loads(trp.read_bytes());entry=recorded_entry(tr.get('uv_tail') or {},R,sha(result))
        if entry is not None:
            rec={'schema':'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002','gate':'EA','verdict':'REPLAYED','producer':pin(Path(__file__)),'per_case':{a.label:entry},'evidence':[pin(result),pin(trp)],'label':'TESTED extraction of radius-bound accepted tail record','method':'recorded E_A with verified probe_R_m'}
            with open(a.out,'x') as f:json.dump(rec,f,indent=1)
            print('EA radius-bound recorded values used');return
    it=ro.get('converged_iteration'); dirs=sorted((run/'stages').glob('*_route_a/checkpoint'))
    if not dirs:
        admitted=(obj.get('identity') or {}).get('route_a') or {}
        if admitted.get('checkpoint'): dirs=[Path(admitted['checkpoint'])]; it=admitted['custody']['iteration']
        else: raise ValueError('NO_COMPUTED_OR_ADMITTED_ROUTE_A_CHECKPOINT')
    ck=dirs[0]
    if it is None:
        done=[(int(p.parent.name.split('_')[-1]),json.loads(p.read_bytes())) for p in ck.glob('iteration_*/COMPLETED.json')]
        accepted=[i for i,d in done if d.get('converged') is True]
        if not accepted:raise ValueError('NO_ACCEPTED_ROUTE_A_ITERATION')
        it=max(accepted)
    startp=ck/f'iteration_{it:04d}/START.json';donep=ck/f'iteration_{it:04d}/COMPLETED.json'
    start=json.loads(startp.read_bytes());done=json.loads(donep.read_bytes());assert done['converged'] is True
    sources=[pin(result),pin(startp),pin(donep),pin(DRIVER)]
    def blob(ref):
        p=ck/ref['blob']; pp=pin(p);assert pp['sha256']==ref['file_sha256'];sources.append(pp)
        return np.load(p,mmap_mode='r',allow_pickle=False)
    cur=blob(start['current_source_fourier_J'])[:,0,0]; gas=blob(start['gas_fourier_J'])[:,0,0]
    updated=blob(done['updated_gas_fourier_J'])[:,0,0];w=blob(start['prepared_weighted_responses'])[:,0,0];k=blob(start['prepared_wavevectors'])
    if np.any(cur==0) or not np.all(np.isfinite(cur)):raise ValueError('ZERO_OR_NONFINITE_CURRENT_LAPSE_SOURCE')
    amp=w*((updated-gas)/cur)
    if not np.all(np.isfinite(amp)):raise ValueError('NONFINITE_RESPONSE_RATIO')
    rows=[]
    for Ri,vi in zip(R,v):
        vals=[]
        for phi in mon['probe_phi_rad']:
            kr=k[:,0]*math.cos(phi)+k[:,1]*math.sin(phi)
            vals.append(abs(float(np.sum(amp*np.exp(1j*kr*Ri)*(1j*kr)).real)))
        rows.append(max(vals)*Ri*299792458.0**2/(2*vi*1e6))
    entry={'result_sha256':sha(result),'E_A_rows_km_s':rows,'accepted_iteration':it,'row_radii_m':R}
    rec={'schema':'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002','gate':'EA','verdict':'REPLAYED','producer':pin(Path(__file__)),'per_case':{a.label:entry},'evidence':sources,'label':'TESTED saved-operator replay; fixture only' if a.fixture else 'TESTED saved-operator replay','monitor_provenance':mon['provenance']}
    with open(a.out,'x') as f:json.dump(rec,f,indent=1)
    print(json.dumps({'case':a.label,'iteration':it,'max_E_A_km_s':max(rows)}))
if __name__=='__main__':
    sys.path.insert(0,str(Path(__file__).parent))
    import producer_guard_cx1v003 as guard
    guard.authorize(sys.argv,'run')
    main()
