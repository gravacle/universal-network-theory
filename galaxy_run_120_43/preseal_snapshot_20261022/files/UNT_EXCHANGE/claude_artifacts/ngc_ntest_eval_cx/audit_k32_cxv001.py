"""0512 data-auditing entry point. Real N records must cite byte-pinned raw replay evidence.
Synthetic branch tests exercise compare() directly. CLI verifies all derivable metrics before compare().
Missing file -> N_INCOMPLETE; bad pin/config/statistic -> N_NO_RUN. No unrelated path is dereferenced.
"""
import json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ntests_compare_c2v003 as P
from ntests_compare_c2v002 import compare
import assemble_k32_cxv001 as A
import validate_k32_cxv001 as V
import ngc_ring_tail_ctx_c2v001 as L
ROOT=P.ROOT

def local(ref):
    p=Path(ref['path'])
    if not p.resolve().is_relative_to(ROOT):raise ValueError('RAW_PATH_REFUSED')
    return A.raw(ref)

def audit(records):
    cache={};metrics={}
    for n,r in records.items():
        if n not in ('N0','NQ','N1','N2','N3','N4'):continue
        if r.get('schema')!='NGC_NTEST_RECORD_C2V001' or r.get('label')!='TESTED':continue
        refs=r.get('input_pins')
        if refs is None:raise FileNotFoundError(n+': raw replay evidence absent')
        key=json.dumps(refs,sort_keys=True)
        if key not in cache:
            raw={k:local(v) for k,v in refs.items()}
            V.validate(refs);cache[key]=(raw,{k:A.rows(v) for k,v in raw.items() if k!='C1PRIME'})
        raw,ar=cache[key]
        expected={}
        if n=='N0':
            old=[]
            expected_refs=sorted((L.KG/'phase23/out/rings/T120L_hovr').glob('rings_*.json'))
            pins=r.get('reference_pins')
            if pins is None:raise FileNotFoundError('N0 reference pins')
            if [Path(q['path']) for q in pins]!=expected_refs:raise ValueError('N0_REFERENCE_ROSTER')
            for q in pins:
                if L.sha(q['path'])!=q['sha256']:raise ValueError('N0_REFERENCE_HASH')
                old.extend(json.loads(Path(q['path']).read_text())['rows'])
            old.sort(key=lambda x:x['ordinal'])
            old=np.array([x['lnN'] for x in old],float)[:,:,:7];new=ar['N0'][:,:,:7]
            if old.shape!=new.shape:raise ValueError('N0_SHAPE')
            mm=int(np.count_nonzero(old.view(np.uint64)!=new.view(np.uint64)))
            expected=dict(mismatches=mm,bitwise_equal=mm==0,ring_count=len(new),heights=7,azimuths=32)
        elif n=='NQ':
            a=ar['CUBE32'];b=ar['NQ_FINE'];count=min(len(a),len(b));expected=A.pair(a[:count],b[:count])
            expected['memory_cap_override']=raw['NQ_FINE'].get('memory_cap_override')
        elif n=='N1':
            expected['spread']=np.ptp(ar['CUBE32'][:100,:,0],axis=1).tolist()
            if 'C1PRIME' in raw:
                for k in ('c1prime_spread','reference_check_spread','c1prime_reference','reference_checked_against'):expected[k]=raw['C1PRIME'][k]
            elif any(k in r for k in ('c1prime_spread','reference_check_spread')):raise ValueError('N1_UNCITED_REFERENCE')
        elif n=='N2':expected=A.pair(ar['CUBE32'],ar['SPHERE32'])
        elif n=='N3':
            a=ar['CUBE32'];pairs={}
            for k in ('CUBE16','CUBE64'):
                b=ar[k];d=A.pair(a,b)
                pairs[k[4:]+'_vs_32']=dict(ring_count=len(a),azimuths=32,max_delta_S=float(np.max(np.abs(np.ptp(a[:,:,0],axis=1)-np.ptp(b[:,:,0],axis=1)))),max_delta_dL=d['max_delta_dL'],same_kept_packet=True,arithmetic='1.+(n_kept+t)')
            expected['pairs']=pairs
        else:
            a=ar['CUBE32'];b=ar['SPHERE32']
            d=a[:,:,7:9]-a[:,:,0,None];e=b[:,:,7:9]-b[:,:,0,None]
            expected=dict(ring_count=len(a),azimuths=32,e4_z95=float(np.max(np.abs(d-e))))
        for k,v in expected.items():
            if r.get(k)!=v:raise ValueError(n+': statistic contradicts raw data: '+k)
    return True

def main():
    try:
        records=P.read_manifest(sys.argv[1]);audit(records);r=compare(records)
    except FileNotFoundError as e:r=dict(outcome='N_INCOMPLETE',tests_read=False,pending=[str(e)])
    except Exception as e:r=dict(outcome='N_NO_RUN',tests_read=False,defects=[str(e)])
    dest=Path(sys.argv[2])
    if not dest.resolve().is_relative_to(ROOT):raise SystemExit('OUTPUT_SCOPE')
    with dest.open('x') as f:json.dump(r,f,indent=1,allow_nan=False)
    print(r['outcome'],flush=True)
if __name__=='__main__':main()
