"""Independent A71 attempt-ledger newline alias probe; no existing bytes changed."""
import os,sys
from pathlib import Path
def guard(event,args):
    if event.startswith(('subprocess.','socket.','os.system','os.exec','os.spawn')):raise RuntimeError('NO_LAUNCH')
    if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
        p=os.path.realpath(os.fsdecode(args[0]))
        if '/runs_ext/' in p or '/runs/' in p or 'KMAX_A2F10_C5H_RUN' in p or '/.codex/sessions/' in p or '/gates_v006/out/IDENTITY' in p or '/gates_v006/records/R4' in p:raise RuntimeError('FORBIDDEN_READ')
sys.addaudithook(guard)
import argparse,contextlib,hashlib,io,json,types
ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts');HERE=Path(__file__).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p,h,name):
    raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==h
    m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m;exec(compile(raw,str(p),'exec'),m.__dict__);return m
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--date-u',required=True);a=ap.parse_args();out=HERE/'ledger_v001';out.mkdir(exist_ok=False)
    target=ART/'tail_scheme_impl_c2/gates_v006/run_identity_compare_c2v006.py';pin='097286d762dd171361e7ff5bbb98b3d48029e790de5869b28aa6218098491e48'
    fp=ART/'review_comparator_c2v005_cx2/invocation/invocation_canaries_cx2v003.py';fh='711580269ba37be0fc6c4e7206c27ca5427d56b7a558e1247cff8e44172ce72e'
    M=load(target,pin,'ledger_v6');F=load(fp,fh,'ledger_own_fixture');M.DRIVER[:]=M.DRIVERS['r5'];drv=M.load_driver();cm=M.load_cm();rows=[]
    for name,tamper,alias in [('P00_ledger_equal',False,False),('C01_ledger_ordinary_change',True,False),('F02_ledger_newline_alias_hides_change',True,True),('F03_equal_duplicate_ledger_alias',False,True)]:
        d=out/name;d.mkdir();r=F.Tree(d/'REF','REF','B0P_RERUN',M,drv,cm);n=F.Tree(d/'NEW','NEW','B0P_RERUN',M,drv,cm)
        rel='stages/11_reference/checkpoint/attempts/cx2token.start.json'
        r.add(rel,{'synthetic_ledger_value':1});n.add(rel,{'synthetic_ledger_value':900 if tamper else 1})
        if alias:n.add(rel+'\n',{'synthetic_ledger_value':1})
        r.publish();n.publish();tp=d/'TOKENS.json';F.jfile(tp,{'declared':[]});op=d/'REPORT.json'
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):M.main(['--driver','r5','--gate','B0P_RERUN','--reference',str(r.root),'--new',str(n.root),'--tokens',str(tp),'--out',str(op)])
        report=json.loads(op.read_bytes());row={'case':name,'verdict':report['verdict'],'failing':report['failing'],'expected':'PASS_BITWISE_EQUAL' if name.startswith('P') else 'FAIL','report':{'path':str(op),'sha256':sha(op)},'attempt_ledger':report['checks'].get('ATTEMPT_LEDGER'),'no_last_wins':report['checks'].get('NO_LAST_WINS'),'coverage':report['checks'].get('COVERAGE')};rows.append(row);print(json.dumps(row))
    assert sha(target)==pin
    data={'date_u':a.date_u,'status':'TESTED_SYNTHETIC_ONLY','target':{'path':str(target),'sha256':pin},'fixture_factory':{'path':str(fp),'sha256':fh},'harness':{'path':str(Path(__file__)),'sha256':sha(__file__)},'rows':rows,'source_before_after_equal':True,'production_incidence':'UNTESTED','mechanism':'ATTEMPT_RE uses $ (accepts before final newline); grouping by captured dir/token/kind overwrites without a duplicate check, and removes both raw files from the later inventory.'}
    p=out/'RESULTS_LEDGER_CX2V001.json'
    with p.open('x') as f:json.dump(data,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({'result_sha256':sha(p),'unexpected':[x['case'] for x in rows if x['verdict']!=x['expected']]}))
if __name__=='__main__':main()
