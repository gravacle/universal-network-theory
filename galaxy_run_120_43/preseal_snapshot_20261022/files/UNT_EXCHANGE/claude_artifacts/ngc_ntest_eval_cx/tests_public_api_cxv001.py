"""Design interface checks and empty-tail bit identity against reviewed Ctx. No tail build or forward solve."""
import json,sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ngc_ring_tail_ctx_c2v001 as L
import ngc_ring_tail_ctx_c2v003 as P

def main():
    L.env();old,cols=L.ctx_with_tail(2.,'cube',False)
    C,S,new=P.ctx_with_tail('T120L','hovr',old.tail,'cube')
    tests=[]
    for o,j in ((1,0),(7,5),(15,13)):
        c=cols[32*o+j]
        for z in L.ZK[:7]:
            a=old.lnN(c['R_m'],c['phi'],z*L.KPC);b=new.lnN(c['R_m'],c['phi'],z*L.KPC)
            tests.append(dict(name=f'empty_identity_{o}_{j}_{z}',passed=a.hex()==b.hex()))
            k=new.kept_delta_n(c['R_m'],c['phi'],z*L.KPC)
            tests.append(dict(name=f'exact_kept_{o}_{j}_{z}',passed=math.log(1.+k).hex()==a.hex()))
    for cid,label,mask in [('G160L','hovr','cube'),('T120L','other','cube'),('T120L','hovr','sphere')]:
        try:P.ctx_with_tail(cid,label,old.tail,mask);ok=False
        except ValueError:ok=True
        tests.append(dict(name=f'refuse_{cid}_{label}_{mask}',passed=ok))
    try:new.solve({});ok=False
    except RuntimeError:ok=True
    tests.append(dict(name='solver_refused',passed=ok))
    for path in sorted(L.HERE.glob('*.py')):
        compile(path.read_text(),str(path),'exec')
    tests.append(dict(name='all_source_syntax_no_bytecode',passed=True))
    rep=dict(label='TESTED',passed=sum(x['passed'] for x in tests),total=len(tests),tests=tests)
    L.write('out/PUBLIC_API_TESTS_V001.json',rep);print(rep['passed'],rep['total'],flush=True)
    assert rep['passed']==rep['total']
if __name__=='__main__':main()
