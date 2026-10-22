"""0525 parametric successor specs; no scientific stages executed. Exclusive writes."""
import copy, hashlib, json, runpy, sys
from pathlib import Path
ROOT=Path(__file__).parent
ART=ROOT.parent
BASE=ART/'tail_scheme_impl_c2'
REG=BASE/'driver_r4/specs/SPECS_V007_C2V002_R1.json'
FILL=BASE/'driver/tools/fill_certificates_v007_c2v001.py'
EPS=BASE/'certificates_v002/gates/EPS_CERT_V006.json'
LO=BASE/'certificates_v002/gates/LO_CERT_V002.json'
DRIVER=BASE/'driver_r4/galaxy_m0_forward_c2v010.py'
def pin(p):
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f: json.dump(obj,f,indent=1,sort_keys=True); f.write('\n')
def diff(a,b,path=''):
    if isinstance(a,dict) and isinstance(b,dict):
        return sum((diff(a.get(k),b.get(k),path+'/'+k) for k in sorted(set(a)|set(b))),[])
    return [] if a==b else [{'field':path,'before':a,'after':b}]
def main():
    registry=json.loads(REG.read_bytes()); records=[]
    for P in (64,128):
        for ent in registry['specs']:
            if not ent['role'].startswith('T-case ') or not ent['role'].endswith(' N8'): continue
            src=Path(ent['file']); assert pin(src)['sha256']==ent['sha256']
            old=json.loads(src.read_bytes()); spec=copy.deepcopy(old)
            case=ent['role'].split()[1]; case={'C4T-K16':'C4T-KLO','C4T-K64':'C4T-KHI'}.get(case,case)
            K=5. if case=='C4T-C5c' else P/2 if case=='C4T-KLO' else 2*P if case=='C4T-KHI' else P
            spec['label']=f'0525 PARAMETRIC SUCCESSOR V007 {case}; production P={P}; outer scale={K:g}; pending root registration and seal; route A N8 M32; RA4 hull inherited; RO1 armed by tail-ON driver'
            if case!='C4T-C5c': spec['numerics']['uv_tail']['outer']['K_big_inverse_kpc']=float(K)
            assert spec['numerics']['route_a']=={'column_workers':8,'max_iterations':32}
            assert spec['numerics']['brackets']==old['numerics']['brackets']
            delta=diff(old,spec)
            assert {x['field'] for x in delta}<={'/label','/numerics/uv_tail/outer/K_big_inverse_kpc'}
            tpl=ROOT/f'P{P}/specs/{case}_P{P}_CX1V002.TEMPLATE.json'; write(tpl,spec)
            oldargv=sys.argv[:]
            try:
                sys.argv=[str(FILL),str(tpl),pin(tpl)['sha256'],str(EPS),str(LO),str(tpl.parent)]
                runpy.run_path(str(FILL),run_name='__main__')
            finally: sys.argv=oldargv
            filled=tpl.with_name(tpl.name.replace('.TEMPLATE.json','.FILLED.json'))
            records.append({'P':P,'case':case,'K_big_inverse_kpc':K,'parent':pin(src),'template':pin(tpl),'filled':pin(filled),'declared_parent_changes':delta,'RO1':'implicit tail-ON v010r4 armed path; no ro1_workers key'})
    write(ROOT/'SPEC_REGISTRY_CX1V002.json',{'label':'TESTED construction; UNTESTED launch; pending seal/root adoption','registry':pin(REG),'fill_tool':pin(FILL),'EPS':pin(EPS),'LO':pin(LO),'driver':pin(DRIVER),'specs':records})
if __name__=='__main__':main()
