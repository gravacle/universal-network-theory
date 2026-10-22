"""0541 immutable successors: admission before module initialization and every function call. No producer execution."""
import ast,hashlib,json
from pathlib import Path
R=Path(__file__).parent
pairs={'ea_replay_cx1v009.py':'ea_replay_cx1v010.py','sr_k_static_cx1v006.py':'sr_k_static_cx1v007.py','shell_split_static_cx1v007.py':'shell_split_static_cx1v008.py','dm4_report_cx1v005.py':'dm4_report_cx1v006.py','ra10_checkpoint_cx1v009.py':'ra10_checkpoint_cx1v010.py','t2i_record_cx1v006.py':'t2i_record_cx1v007.py','t2i_replica_admitted_cx1v002.py':'t2i_replica_admitted_cx1v003.py','aggregate_records_cx1v005.py':'aggregate_records_cx1v006.py','route_a_tail_replay_cx1v002.py':'route_a_tail_replay_cx1v003.py','producer_runtime_cx1v001.py':'producer_runtime_cx1v002.py','shell_filter_cx1v001.py':'shell_filter_cx1v002.py'}
class GuardFunctions(ast.NodeTransformer):
 def visit_FunctionDef(self,n):
  self.generic_visit(n);n.decorator_list.insert(0,ast.parse('@_root_guard.guarded\ndef f():pass').body[0].decorator_list[0]);return n
prefix=ast.parse("import sys as _guard_sys\nfrom pathlib import Path as _GuardPath\n_guard_sys.path.insert(0,str(_GuardPath(__file__).parent))\nimport producer_guard_cx1v005 as _root_guard\n_root_guard.admission(__file__)\n").body
rows=[]
for old,new in pairs.items():
 s=(R/old).read_text().replace('producer_guard_cx1v004','producer_guard_cx1v005').replace('if not guard.ADMITTED:guard.authorize','guard.authorize')
 for a,b in pairs.items():s=s.replace(a,b).replace(a[:-3],b[:-3])
 tree=ast.parse(s);tree=GuardFunctions().visit(tree)
 i=1 if tree.body and isinstance(tree.body[0],ast.Expr) and isinstance(tree.body[0].value,ast.Constant) and isinstance(tree.body[0].value.value,str) else 0
 while i<len(tree.body) and isinstance(tree.body[i],ast.ImportFrom) and tree.body[i].module=='__future__':i+=1
 tree.body[i:i]=prefix;ast.fix_missing_locations(tree);out=ast.unparse(tree)+'\n';ast.parse(out)
 with (R/new).open('x') as f:f.write(out)
 rows.append({'path':str(R/new),'sha256':hashlib.sha256((R/new).read_bytes()).hexdigest(),'parent':{'path':str(R/old),'sha256':hashlib.sha256((R/old).read_bytes()).hexdigest()}})
with (R/'GUARDED_SUCCESSORS_0541_V001.json').open('x') as f:json.dump({'label':'TESTED source construction only; admission and execution tests pending','files':rows},f,indent=1)
print('guarded successors',len(rows))
