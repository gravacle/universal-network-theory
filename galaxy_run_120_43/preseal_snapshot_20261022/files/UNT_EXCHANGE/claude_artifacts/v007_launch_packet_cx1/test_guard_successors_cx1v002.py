"""No protected run opened. Direct CLI denial, case-insensitive audit guard, sealed compare pending."""
import hashlib,json,runpy,sys
from pathlib import Path
R=Path(__file__).parent;sys.path.insert(0,str(R))
import producer_guard_cx1v004 as G
rows=[]
def check(name,fn,typ):
 try:fn();ok=False;msg='did not refuse'
 except Exception as e:ok=isinstance(e,typ);msg=str(e)
 rows.append({'name':name,'passed':ok,'message':msg})
def cli(name,args):
 G.ADMITTED=False;sys.argv=[str(R/name)]+args;runpy.run_path(str(R/name),run_name='__main__')
for name in ('ea_replay_cx1v009.py', 'sr_k_static_cx1v006.py', 'shell_split_static_cx1v007.py', 'dm4_report_cx1v005.py', 'ra10_checkpoint_cx1v009.py', 't2i_record_cx1v006.py', 't2i_replica_admitted_cx1v002.py'):
 check(name,lambda n=name:cli(n,['/UNREGISTERED_FIXTURE','a','b','c','d']),PermissionError)
check('aggregate_preseal',lambda:cli('aggregate_records_cx1v005.py',['EA','unused','unused']),PermissionError)
for path in ('/fake/RUNS_EXT/kmax_a2f10_c5h_run_v001/result.json','/fake/runs_EXT/uvt_case/data.npy'):
 check('casefold_'+path,lambda p=path:G.check_path(p),PermissionError)
check('unregistered_frozen_prereg',lambda:G.validate_seal('/NOT_OPENED','0'*64),ValueError)
with (R/'GUARD_SUCCESSOR_TESTS_V002.json').open('x') as f:json.dump({'label':'TESTED synthetic rejection only; no protected run reads','producer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'guard_sha256':hashlib.sha256((R/'producer_guard_cx1v004.py').read_bytes()).hexdigest(),'checks':rows},f,indent=1)
print(sum(x['passed'] for x in rows),len(rows));assert all(x['passed'] for x in rows)
