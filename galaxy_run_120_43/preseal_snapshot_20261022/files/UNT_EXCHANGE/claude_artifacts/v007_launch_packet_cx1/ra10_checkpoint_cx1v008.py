"""RA10 checkpoint-only readout; no column solve. RUN LABEL OUTPUT.
Replay last completed prepared metric at query 03, R=1.48kpc,z=0, 32/64 uniform azimuths.
Tail-ON requires a successor that reconstructs the accepted tail boundary; refused here.
Reports explicit Fourier convention and four diagonal values; no acceptance threshold.
"""
import hashlib,json,math,sys
from pathlib import Path
import numpy as np
def pin(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(2**22),b''):h.update(b)
    return {'path':str(p),'sha256':h.hexdigest()}
if __name__=='__main__':
    sys.path.insert(0,str(Path(__file__).parent))
    import producer_guard_cx1v003 as guard
    guard.authorize(sys.argv,'run')
    run,label,out=sys.argv[1:4];run=Path(run);rp=run/'result.json';r=json.loads(rp.read_bytes())
    tail_raw=(r.get('normalized_spec') or {}).get('numerics',{}).get('uv_tail')
    if len(sys.argv)>4:
        if label not in ('C4R3','C5R3','C6R3'):raise ValueError('TAIL_OVERRIDE_RESTRICTED_TO_FIXTURE_LABELS')
        if sys.argv[4]!='--fixture-tail-spec':raise ValueError('UNKNOWN_ARGUMENT')
        tail_raw=json.loads(Path(sys.argv[5]).read_bytes())['numerics']['uv_tail']
    ds=sorted((run/'stages').glob('*_route_a/checkpoint'))
    if not ds:
        admitted=(r.get('identity') or {}).get('route_a') or {}
        if admitted.get('checkpoint'): ds=[Path(admitted['checkpoint'])]
        else: raise ValueError('NO_COMPUTED_OR_ADMITTED_CHECKPOINT')
    ck=ds[0];done=sorted(ck.glob('iteration_*/COMPLETED.json'))
    if not done:raise ValueError('NO_COMPLETED_ITERATION')
    dp=done[-1];sp=dp.parent/'START.json';s=json.loads(sp.read_bytes());d=json.loads(dp.read_bytes())
    refs=[pin(rp),pin(sp),pin(dp)]
    def blob(ref):
        p=ck/ref['blob'];q=pin(p);assert q['sha256']==ref['file_sha256'];refs.append(q)
        return np.load(p,mmap_mode='r',allow_pickle=False)
    k=blob(s['prepared_wavevectors']);w=blob(s['prepared_weighted_responses'])[:,0,0]
    ni=json.loads((run/'inputs/seed_c2v001.json').read_bytes())['numerical_inputs'];R=1.48*ni['kpc_m']
    tail=None
    if tail_raw:
        sys.path.insert(0,str(Path(__file__).parent))
        import route_a_tail_replay_cx1v002 as TR
        tail=TR.build(run,ck,s['iteration'],TR.T.UVT.normalize_config(tail_raw),R)
    values={}
    for n in (32,64):
        y=[]
        for j in range(n):
            ph=2*math.pi*j/n;kr=k[:,0]*math.cos(ph)+k[:,1]*math.sin(ph);phase=np.exp(1j*kr*R)
            delta=float(np.sum(w*phase).real);der=float(np.sum(w*phase*(1j*kr)).real)
            if tail is not None:
                tj=tail.cyl_jets(R,np.array([ph]),np.array([0.]),1)
                delta+=float(tj['f'][0,0]);der+=float(tj['fR'][0,0])
            if 1+delta<=0:raise ValueError('NONPOSITIVE_LAPSE')
            y.append(der/(1+delta))
        f=np.fft.rfft(y)/n
        values[n]={'a0':float(f[0].real),'a4':float(2*abs(f[4])),'a8':float(2*abs(f[8])),
        'diagonals':[{'phi_rad':2*math.pi*j/n,'dlnN_dR':y[j]} for j in (n//8,3*n//8,5*n//8,7*n//8)]}
    row={'case':label,'source':'route-A saved prepared checkpoint (last completed START)','query':3,'R_kpc':1.48,'units':'m^-1',**{k:values[64][k] for k in ('a0','a4','a8')}}
    rec={'schema':'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002','gate':'HARMONICS','verdict':'REPORTED','producer':pin(Path(__file__)),
    'rows':[row],'label':'TESTED finite saved-operator readout; not a convergence or accepted-state claim',
    'iteration':s['iteration'],'accepted':d['converged'],'input_pins':refs,'samples':values,
    'convention':'a0 = signed mean; a_m = 2 abs(DFT_m)/N for m>0; z=0; derivatives of ln(1+delta_n)',
    'azimuth_doubling_absolute_deltas':{k:abs(values[64][k]-values[32][k]) for k in ('a0','a4','a8')}}
    rec['tail_record']=None if tail is None else tail.record
    rec['fixture_tail_spec']=pin(Path(sys.argv[5])) if len(sys.argv)>4 else None
    with open(out,'x') as f:json.dump(rec,f,indent=1)
    print(label,rec['iteration'],rec['accepted'])
