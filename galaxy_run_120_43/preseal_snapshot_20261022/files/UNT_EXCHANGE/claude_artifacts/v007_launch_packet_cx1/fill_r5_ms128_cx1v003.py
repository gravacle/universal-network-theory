"""0555: fill final r5/MS128 P128 successors from retained EPSv2 and explicit-MS128 LOv4. EPS LO arguments; exclusive writes."""
import contextlib,hashlib,json,runpy,sys
from pathlib import Path
R=Path(__file__).parent;A=R.parent
FILL=A/'tail_scheme_impl_c2/driver/tools/fill_certificates_v007_c2v001.py'
CERT=A/'tail_scheme_impl_c2/certificates_v003'
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def main():
    ep,lp=map(Path,sys.argv[1:]);rp=json.loads((R/'R5_RUNTIME_PINS_V001.json').read_bytes())['pins']
    assert ep.resolve()==(A/'tail_scheme_impl_c2/certificates_v002/gates/EPS_CERT_V006.json').resolve() and lp.resolve()==(A/'tail_scheme_impl_c2/certificates_v004/gates/LO_CERT_V004_MS128.json').resolve(),'0555_AUTHORIZED_CERTIFICATE_PATHS_REQUIRED'
    assert pin(ep)['sha256']=='598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192','RETAINED_EPS_BYTES_CHANGED'
    assert json.loads(ep.read_bytes())['verdict']=='CERTIFIED'
    lo=json.loads(lp.read_bytes());assert lo['verdict']=='PASS'
    assert type(lo.get('source_gas_M_s')) is int and lo['source_gas_M_s']==128,'LO_SOURCE_GAS_MS128_REQUIRED'
    assert pin(Path(rp['driver']['path']))==rp['driver'],'R5_DRIVER_CHANGED'
    registry=json.loads((R/'SPEC_TEMPLATES_MS128_CX1V003.json').read_bytes());rows=[]
    for ent in registry['specs']:
        parent=Path(ent['template']['path']);assert pin(parent)==ent['template'];sp=json.loads(parent.read_bytes())
        sp['label']=f'V007 A55/A57 P128 {ent["case"]}; gas M_s128; r5; N8 M32 RA4 hull; prepared, unlaunched'
        p=R/f'P128/specs/{ent["case"]}_P128_MS128_R5_CX1V004.TEMPLATE.json'
        with p.open('x') as f:json.dump(sp,f,indent=1,sort_keys=True);f.write('\n')
        sys.argv=[str(FILL),str(p),pin(p)['sha256'],str(ep),str(lp),str(p.parent)]
        with (R/f'P128/{ent["case"]}_FILL_R5_V004.log').open('x') as log,contextlib.redirect_stdout(log):runpy.run_path(str(FILL),run_name='__main__')
        filled=p.with_name(p.name.replace('.TEMPLATE.json','.FILLED.json'))
        rows.append({'P':128,'case':ent['case'],'parent':ent['template'],'template':pin(p),'filled':pin(filled),'changes_from_parent_template':['/label','certificate slots only in FILLED']})
    out={'label':'TESTED file construction; UNTESTED launch; pending seal','driver':rp['driver'],'module':rp['module'],'EPS':pin(ep),'LO':pin(lp),'fill_tool':pin(FILL),'specs':rows}
    with (R/'SPEC_REGISTRY_R5_MS128_CX1V004.json').open('x') as f:json.dump(out,f,indent=1)
    print('10 r5/MS128 specs filled')
if __name__=='__main__':main()
