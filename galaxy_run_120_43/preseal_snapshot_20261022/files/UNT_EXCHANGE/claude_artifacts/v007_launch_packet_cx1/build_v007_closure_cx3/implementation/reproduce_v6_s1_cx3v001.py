"""AST-extracted old/new parser and publication-tail reproduction only."""
from pathlib import Path
import ast, hashlib, json, math, os, resource, subprocess, sys, types

HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent;OUT=HERE/'repro_v001';OUT.mkdir()
date_u=subprocess.check_output(['date','-u'],text=True).strip()
checks=[];pins=[]
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def audit(event,args):
    if event in ('subprocess.Popen','os.system','socket.__new__','socket.connect'):raise PermissionError('NO_ACTIONS')
    if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
        p=Path(os.fsdecode(args[0]));s=str(p.absolute()).casefold()
        if 'kmax_a2f10_c5h_run_v001' in s or '/runs_ext/uvt_' in s or '/.codex/' in s or '/.codex-alt/' in s:raise PermissionError('PROTECTED')
        fl=args[2] if len(args)>2 and isinstance(args[2],int) else 0
        if fl&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):
            if not p.resolve().is_relative_to(OUT) or not fl&os.O_EXCL:raise PermissionError('EXCLUSIVE_OWN_ONLY')
sys.addaudithook(audit)
for version,name in [('old','postseal_records_cx1v006.py'),('new','postseal_records_cx1v006_cx3v001.py')]:
    p=BASE/name;pins.append(pin(p));tree=ast.parse(p.read_text())
    nodes=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in ('pairs','loads')]
    for n in nodes:n.decorator_list=[]
    ns={'json':json,'math':math};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),ns)
    for raw in ('1e999','-1e999','{"extra":{"nested":[1e999]}}'):
        try:obj=ns['loads'](raw);raised=False
        except ValueError as e:obj=None;raised=True;assert str(e)=='NONFINITE_JSON'
        expected=version=='new'
        checks.append({'name':version+'_overflow_'+raw,'passed':raised==expected,'required_refusal_observed':raised,'classification':'OLD_DEFECT_REPRODUCED' if version=='old' else 'FIX_REFUSES'})

for role,old,new in [('postseal','postseal_records_cx1v006.py','postseal_records_cx1v006_cx3v001.py'),('srb','srb_rot_record_cx1v008.py','srb_rot_record_cx1v008_cx3v001.py')]:
    for version,name in [('old',old),('new',new)]:
        p=BASE/name;pins.append(pin(p));tree=ast.parse(p.read_text());main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
        # Extract exact final production statements, without rewriting them.
        start=next(i for i,n in enumerate(main.body) if (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='serialized' for t in n.targets)) or (isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='check_run_path' and n.value.args and isinstance(n.value.args[0],ast.Name) and n.value.args[0].id=='out'))
        tail=ast.Module(body=main.body[start:],type_ignores=[])
        for fault in ('stamp','serialize'):
            out=OUT/(role+'_'+version+'_'+fault+'.json')
            def stamp(o,p):
                if fault=='stamp':raise PermissionError('SYNTHETIC_STAMP_FAILURE')
                return dict(o,last_nonfinite=math.inf)
            ns={'json':json,'__file__':str(p),'rec':{'finite':[1,2,3]},'out':str(out),'G':types.SimpleNamespace(stamp=stamp,check_run_path=lambda *a,**k:None)}
            try:exec(compile(tail,str(p),'exec'),ns);raised=False
            except (PermissionError,ValueError):raised=True
            exists=out.exists();size=out.stat().st_size if exists else None
            good=raised and (exists if version=='old' else not exists)
            if version=='old' and fault=='serialize':good=good and size>0
            checks.append({'name':role+'_'+version+'_'+fault,'passed':bool(good),'output_exists':exists,'bytes':size,'classification':'OLD_PARTIAL_OUTPUT_DEFECT_REPRODUCED' if version=='old' else 'FIX_REFUSES_WITH_NO_OUTPUT'})
assert all(x['passed'] for x in checks)
result={'date_u':date_u,'status':'TESTED_PASS','checks_passed':len(checks),'checks_total':len(checks),'checks':checks,'sources':list({x['path']:x for x in pins}.values()),'harness':pin(Path(__file__)),'scope':'AST-extracted exact parser and final publication statements. No producer imports, admission files, science, or runtime reconstruction. Old expected failures are recorded explicitly, not counted as producer readiness.'}
with (OUT/'RESULTS_CX3V001.json').open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':len(checks),'total':len(checks),'rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
