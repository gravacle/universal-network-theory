"""Sequential driver dry-runs in this process; refuses every scientific run command."""
import hashlib,json,runpy,sys
from pathlib import Path
ROOT=Path(__file__).parent
REG=ROOT/'SPEC_REGISTRY_CX1V001.json'
def guard(event,args):
    if event=='open' and isinstance(args[0],(str,bytes)):
        p=str(args[0])
        if '/runs_ext/UVT_' in p or '/runs_ext/KMAX_A2F10_C5H_RUN_V001' in p:
            raise PermissionError('Forbidden run read: '+p)
sys.addaudithook(guard)
def main():
    r=json.loads(REG.read_bytes()); d=r['driver']; assert hashlib.sha256(Path(d['path']).read_bytes()).hexdigest()==d['sha256']
    results=[]
    for ent in r['specs']:
        out=ROOT/f"P{ent['P']}/dry/{ent['case']}_V001"
        sp=ent['filled']; assert hashlib.sha256(Path(sp['path']).read_bytes()).hexdigest()==sp['sha256']
        sys.argv=[d['path'],'dry-run','--spec',sp['path'],'--report-dir',str(out)]
        try: runpy.run_path(d['path'],run_name='__main__'); code=0
        except SystemExit as e: code=e.code
        results.append({'P':ent['P'],'case':ent['case'],'exit':code,'report_dir':str(out)})
        print('DRY_RESULT',results[-1],flush=True)
    with (ROOT/'DRY_RESULTS_CX1V001.json').open('x') as f:json.dump(results,f,indent=1)
if __name__=='__main__':main()
