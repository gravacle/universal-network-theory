"""Compute N records from byte-pinned replay arrays. Does not infer absent scientific tests.
Usage: assemble_k32_cxv001.py MANIFEST_JSON OUTPUT_PREFIX
Manifest keys: N0, CUBE32, NQ_FINE, SPHERE32, CUBE16, CUBE64, C1PRIME (each path,sha256).
Only available pairs are summarized. C1PRIME, when supplied, contains the explicit G160L/G120L evidence.
"""
import json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ngc_ring_tail_ctx_c2v001 as L

def raw(ref):
    p=Path(ref['path'])
    if L.sha(p)!=ref['sha256']:raise ValueError('INPUT_HASH_MISMATCH')
    return json.loads(p.read_text())

def rows(r):
    if r.get('operator_sha256')!=L.OP_SHA or r.get('azimuths')!=32 or r.get('label')!='TESTED':raise ValueError('REPLAY_CUSTODY')
    v=r['rows'];ords=[x['ordinal'] for x in v]
    if ords!=list(range(len(v))) or len(v)<100:raise ValueError('RING_COVERAGE')
    a=np.array([x['lnN'] for x in v],float)
    if a.shape!=(len(v),32,9) or not np.all(np.isfinite(a)) or r['z_kpc']!=list(L.ZK):raise ValueError('HEIGHT_COVERAGE')
    return a

def base(n):return dict(production_K_big=32,scope_ruling='0546',schema='NGC_NTEST_RECORD_C2V001',test=n,label='TESTED',operator_sha256=L.OP_SHA,theta=L.THETA)

def pair(a,b):
    if a.shape!=b.shape:raise ValueError('PAIR_SHAPE')
    d=a[:,:,1:7]-a[:,:,0,None];e=b[:,:,1:7]-b[:,:,0,None]
    return dict(ring_count=len(a),azimuths=32,heights=7,max_delta_lnN0=float(np.max(np.abs(a[:,:,0]-b[:,:,0]))),max_delta_dL=float(np.max(np.abs(d-e))))

def main():
    manifest=json.loads(Path(sys.argv[1]).read_text());prefix=sys.argv[2];r={n:raw(v) for n,v in manifest.items()}
    arrays={n:rows(v) for n,v in r.items() if n!='C1PRIME'};records={}
    if 'N0' in r:
        ref=[];pins=[]
        for p in sorted((L.KG/'phase23/out/rings/T120L_hovr').glob('rings_*.json')):
            q=json.loads(p.read_text());ref.extend(q['rows']);pins.append(dict(path=str(p),sha256=L.sha(p)))
        ref.sort(key=lambda x:x['ordinal']);old=np.array([x['lnN'] for x in ref],float)[:,:,:7]
        new=arrays['N0'][:,:,:7]
        if old.shape!=new.shape or len(new)!=156:raise ValueError('N0_REFERENCE_SHAPE')
        mismatch=int(np.count_nonzero(old.view(np.uint64)!=new.view(np.uint64)))
        records['N0']=dict(base('N0'),bitwise_equal=mismatch==0,mismatches=mismatch,ring_count=len(new),azimuths=32,heights=7,reference_pins=pins)
    if 'CUBE32' in r:
        a=arrays['CUBE32'];S=np.ptp(a[:100,:,0],axis=1)
        records['N1']=dict(base('N1'),spread=S.tolist())
        if 'C1PRIME' in r:
            for k in ('c1prime_spread','reference_check_spread','c1prime_reference','reference_checked_against'):records['N1'][k]=r['C1PRIME'][k]
        if 'NQ_FINE' in r:
            b=arrays['NQ_FINE'];n=min(len(a),len(b))
            records['NQ']=dict(base('NQ'),**pair(a[:n],b[:n]),base_quadrature=[.005,.007,8],fine_quadrature=[.0025,.0035,12],memory_cap_override=r['NQ_FINE'].get('memory_cap_override'))
        if 'SPHERE32' in r:
            b=arrays['SPHERE32'];records['N2']=dict(base('N2'),**pair(a,b))
            d=a[:,:,7:9]-a[:,:,0,None];e=b[:,:,7:9]-b[:,:,0,None]
            records['N4']=dict(base('N4'),ring_count=len(a),azimuths=32,e4_z95=float(np.max(np.abs(d-e))))
        if all(k in r for k in ('CUBE16','CUBE64')):
            pp={}
            for k in ('CUBE16','CUBE64'):
                b=arrays[k];p=pair(a,b)
                pp[k[4:]+'_vs_32']=dict(ring_count=len(a),azimuths=32,max_delta_S=float(np.max(np.abs(np.ptp(a[:,:,0],axis=1)-np.ptp(b[:,:,0],axis=1)))),max_delta_dL=p['max_delta_dL'],same_kept_packet=True,arithmetic='1.+(n_kept+t)')
            records['N3']=dict(base('N3'),pairs=pp)
    out={}
    for n,v in records.items():
        v['input_pins']=manifest;out[n]=L.write(prefix+'_'+n+'.json',v)
    out['LO_NGC']=dict(path=str(L.CERT/'LO_NGC_CERT_V002.json'),sha256=L.sha(L.CERT/'LO_NGC_CERT_V002.json'))
    out['I1T_NGC']=dict(path=str(L.CERT/'I1T_NGC_T120L_V001.json'),sha256=L.sha(L.CERT/'I1T_NGC_T120L_V001.json'))
    print(L.write(prefix+'_MANIFEST.json',out),flush=True)
if __name__=='__main__':main()
