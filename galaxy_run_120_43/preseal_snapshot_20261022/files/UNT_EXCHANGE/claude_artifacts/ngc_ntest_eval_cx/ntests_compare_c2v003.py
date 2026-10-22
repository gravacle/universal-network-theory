"""Path-restricted entry point for 0512 compare. Values/thresholds unchanged from c2v002.
Only records beneath this build and the two named LO/I1-T certificate files can be opened.
"""
import json,sys,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ntests_compare_c2v002 import compare,REQUIRED
ROOT=Path(__file__).resolve().parent
CERT=ROOT.parent/'tail_scheme_impl_c2/certificates_v002/gates'
CERT_NAMES={'LO_NGC':'LO_NGC_CERT_V002.json','I1T_NGC':'I1T_NGC_T120L_V001.json'}

def read_manifest(path):
    path=Path(path)
    if not path.resolve().is_relative_to(ROOT):raise ValueError('MANIFEST_OUTSIDE_BUILD')
    m=json.loads(path.read_text());out={}
    for k,v in m.items():
        if k not in REQUIRED:
            out[k]={};continue # unknown names are pending, never dereferenced
        p=Path(v['path']);resolved=p.resolve()
        allowed=resolved.is_relative_to(ROOT) or (k in CERT_NAMES and resolved==(CERT/CERT_NAMES[k]).resolve())
        if not allowed:raise ValueError('RECORD_PATH_REFUSED '+k)
        raw=p.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=v['sha256']:raise ValueError('HASH_MISMATCH '+k)
        out[k]=json.loads(raw)
    return out

def main():
    try:r=compare(read_manifest(sys.argv[1]))
    except Exception as e:r=dict(outcome='N_NO_RUN',tests_read=False,defects=[str(e)])
    dest=Path(sys.argv[2])
    if not dest.resolve().is_relative_to(ROOT):raise SystemExit('OUTPUT_SCOPE')
    with dest.open('x') as f:json.dump(r,f,indent=1,allow_nan=False)
    print(r['outcome'],flush=True)
if __name__=='__main__':main()
