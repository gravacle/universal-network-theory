"""REGISTRY RESULT_STEM: verified r5 dry-runs only, no scientific launch."""
import contextlib,hashlib,json,runpy,sys
from pathlib import Path
R=Path(__file__).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def audit(e,a):
    if e=='open' and isinstance(a[0],(str,bytes)):
        p=str(Path(a[0]).resolve())
        if '/runs_ext/UVT_' in p or '/runs_ext/KMAX_A2F10_C5H_RUN_V001/' in p:raise PermissionError('PROTECTED_RUN_READ')
sys.addaudithook(audit)
def main():
    regpath,stem=sys.argv[1:];reg=json.loads(Path(regpath).read_bytes());d=reg['driver'];assert sha(d['path'])==d['sha256'];rows=[]
    if '/' in stem:raise ValueError('STEM_ONLY')
    for ent in reg['specs']:
        sp=ent['filled'];assert sha(sp['path'])==sp['sha256'];out=R/'P128/dry'/f'{ent["case"]}_{stem}'
        sys.argv=[d['path'],'dry-run','--spec',sp['path'],'--report-dir',str(out)]
        with (R/f'P128/{ent["case"]}_{stem}.log').open('x') as f,contextlib.redirect_stdout(f):
            try:runpy.run_path(d['path'],run_name='__main__');code=0
            except SystemExit as e:code=e.code
        p=out/'DRYRUN_REPORT.json';q=json.loads(p.read_bytes());s=q['summary']
        passed=code==0 and q['executed_stages']==0 and not any(s[k] for k in ('binding_blockers','refusals_beyond_pending_inputs','pin_problems')) and not s['uv_tail']['pending_certificates']
        rows.append({'case':ent['case'],'passed':passed,'exit':code,'executed_stages':q['executed_stages'],'report':{'path':str(p),'sha256':sha(p)}})
        print(ent['case'],passed,flush=True)
    with (R/(stem+'.json')).open('x') as f:json.dump({'label':'TESTED dry-run only','registry':{'path':regpath,'sha256':sha(regpath)},'driver':d,'checks':rows,'passed':sum(x['passed'] for x in rows)},f,indent=1)
    assert all(x['passed'] for x in rows)
if __name__=='__main__':main()
