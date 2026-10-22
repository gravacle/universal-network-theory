"""Successor: verify case config, source identity and paired radii before deriving any record."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import assemble_ntests_c2v001 as A
import ngc_ring_tail_ctx_c2v001 as L

EXPECTED={'N0':(2.,'cube',False),'CUBE16':(16.,'cube',False),'NQ_FINE':(16.,'cube',True),
          'SPHERE16':(16.,'sphere',False),'CUBE8':(8.,'cube',False),'CUBE32':(32.,'cube',False)}

def validate(manifest):
    if set(manifest)-set(EXPECTED)-{'C1PRIME'}:raise ValueError('UNKNOWN_REPLAY_CASE')
    U,_,_=L.modules();radii={};digests=[]
    for name,ref in manifest.items():
        if name=='C1PRIME':continue
        r=A.raw(ref);big,shape,fine=EXPECTED[name]
        if (r.get('kbig'),r.get('shape'),r.get('doubled'))!=(big,shape,fine):raise ValueError('CASE_CONFIG '+name)
        cfg=L.config(U,big,fine);tr=r['tail_record']
        if tr.get('config_sha256')!=cfg['sha256'] or tr.get('kept')!={'shape':shape,'K_inverse_kpc':2.}:raise ValueError('TAIL_CONFIG '+name)
        if tr.get('outer')!=cfg['outer'] or tr.get('production_admissible') is not True:raise ValueError('TAIL_ADMISSION '+name)
        if name=='N0':
            if tr.get('empty') is not True:raise ValueError('N0_NOT_EMPTY')
        else:
            if tr.get('empty') is not False or not tr.get('roster_digest'):raise ValueError('MISSING_SOURCE '+name)
            digests.append(tr['roster_digest'])
        A.rows(r);radii[name]=[x['R_kpc'] for x in r['rows']]
    if len(set(digests))>1:raise ValueError('SOURCE_MISMATCH')
    if 'CUBE16' in radii:
        a=radii['CUBE16']
        for n,b in radii.items():
            if n=='N0':continue
            if a[:min(len(a),len(b))]!=b[:min(len(a),len(b))]:raise ValueError('RADIUS_MISMATCH '+n)
            if n!='NQ_FINE' and len(a)!=len(b):raise ValueError('RING_COUNT_MISMATCH '+n)
    return True

if __name__=='__main__':
    validate(json.loads(Path(sys.argv[1]).read_text()));A.main()
