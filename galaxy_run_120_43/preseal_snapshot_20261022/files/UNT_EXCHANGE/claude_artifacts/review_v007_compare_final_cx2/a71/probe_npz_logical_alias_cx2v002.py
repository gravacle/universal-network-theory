"""Own one-node synthetic packet: ZIP names differ, NumPy logical names alias."""
import os,sys
from pathlib import Path
HERE=Path(__file__).parent
def audit(event,args):
    if event.startswith(('subprocess.','socket.','os.system','os.exec','os.spawn')):raise RuntimeError('NO_LAUNCH')
    if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
        p=os.fsdecode(args[0])
        if '/runs/' in p or '/runs_ext/' in p or 'KMAX_A2F10_C5H_RUN' in p or '/.codex/sessions/' in p:raise RuntimeError('FORBIDDEN')
sys.addaudithook(audit)
import argparse,hashlib,io,json,types,zipfile
import numpy as np
ART=HERE.parent.parent
SRC=ART/'v007_compare_c2/r10/kmax_tail_compare_c2v007_r10.py'
V5=ART/'kmax_prereg_v005_c2/kmax_compare_c2v005.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p,pin,name):
    raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==pin
    m=types.ModuleType(name);m.__file__=str(p);exec(compile(raw,str(p),'exec'),m.__dict__);return m
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--date-u',required=True);a=ap.parse_args()
    out=HERE/'npz_alias_v002';out.mkdir(exist_ok=False)
    m=load(SRC,'e801adc41462bbc9dd8e81ff915b93981c3f2ec4930cb1fb9df26a78cbe18b93','npz_r10')
    c5=load(V5,'49404bc4b0d558c93113ed650802d9009f03be64c364f0d862213783389786f5','npz_v5')
    def npy(a):
        b=io.BytesIO();np.save(b,a,allow_pickle=False);return b.getvalue()
    k=npy(np.zeros((1,3)));good=npy(np.ones((1,1,1)));bad=npy(np.zeros((1,1,1)))
    grid={'breaks_inverse_kpc':[-1.,1.],'panel_orders':[1]};rows=[]
    for name,members in [('positive',[('wavevectors.npy',k),('weighted_responses.npy',good)]),('negative_value',[('wavevectors.npy',k),('weighted_responses.npy',bad)]),('alias_bad_first',[('wavevectors.npy',k),('weighted_responses.npy',bad),('weighted_responses',good)]),('alias_bad_last',[('wavevectors.npy',k),('weighted_responses',good),('weighted_responses.npy',bad)])]:
        p=out/(name+'.npz')
        with p.open('xb') as f:
            with zipfile.ZipFile(f,'w') as z:
                for nm,raw in members:z.writestr(nm,raw)
        pk={'path':str(p),'sha256':sha(p)}
        code=m.npz_duplicate_member_code(pk)
        run={'present':True,'adapted':{'status':'COMPLETED','field_packet':pk}}
        got=m.compute_packets({'C5M':c5,'grids':{m.EXPECTED_GRID['C2T']:grid}},[('C2T',run)])
        with np.load(p,allow_pickle=False) as z:logical=list(z.files);chosen=z['weighted_responses'].tolist()
        rows.append({'name':name,'input':pk,'raw_zip_names':[x[0] for x in members],'numpy_logical_names':logical,'numpy_selected_values':chosen,'duplicate_guard':code,'packet_result':got,'expected_duplicate_refusal':name.startswith('alias')})
    result={'date_u':a.date_u,'status':'TESTED_SYNTHETIC_ONE_NODE_PACKET','source':{'path':str(SRC),'sha256_before_after':sha(SRC)},'adapter':{'path':str(V5),'sha256':sha(V5)},'rows':rows,'limit':'Actual r10 guard and compute_packets with actual pinned V005 packet_checks. Owned tiny supplied grid context; not a registered scientific grid, full decision or sealed adoption.'}
    p=out/'NPZ_LOGICAL_ALIAS_CX2V002.json'
    with p.open('x') as f:json.dump(result,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps({'path':str(p),'sha256':sha(p),'results':[(x['name'],x['duplicate_guard'],x['packet_result']) for x in rows]}))
if __name__=='__main__':main()
