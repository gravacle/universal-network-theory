"""0588 preparation: A79.4 NPZ logical-name fixtures, direct parser only. No run tree or scientific process."""
import hashlib,importlib.util,io,json,sys,warnings,zipfile
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
SRC=HERE.parent.parent/'run_identity_compare_c2v007.py'
OUT=HERE/'NPZ_LOGICAL_PREP_V001';OUT.mkdir()
def audit(event,args):
 if event in ('subprocess.Popen','os.system','socket.connect'):raise PermissionError('NO_PROCESS_OR_NETWORK')
 if event=='open' and isinstance(args[0],(str,bytes)):
  p=str(args[0]).lower()
  if '/runs_ext/' in p or 'kmax_a2f10_c5h_run' in p:raise PermissionError('NO_PROTECTED_RUN_READ')
sys.addaudithook(audit)
spec=importlib.util.spec_from_file_location('cmp_npz_prep',SRC);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
M.C5H_REGISTERED=str(OUT/'synthetic_registered_not_used')
def payload(value):
 b=io.BytesIO();np.save(b,np.array([value],dtype='<f8'),allow_pickle=False);return b.getvalue()
zero,one=payload(0),payload(1)
cases=[('clean',[('weighted_responses.npy',one)],False),('alias_bad_first',[('weighted_responses.npy',zero),('weighted_responses',one)],True),('alias_bad_last',[('weighted_responses',one),('weighted_responses.npy',zero)],True),('extensionless_only',[('weighted_responses',one)],True),('duplicate_raw_same',[('weighted_responses.npy',one),('weighted_responses.npy',one)],True),('duplicate_raw_changed',[('weighted_responses.npy',zero),('weighted_responses.npy',one)],True),('nested_alias',[('group/weighted_responses.npy',zero),('group/weighted_responses',one)],True)]
rows=[]
for name,members,must_fail in cases:
 b=io.BytesIO()
 with warnings.catch_warnings():
  warnings.simplefilter('ignore',UserWarning)
  with zipfile.ZipFile(b,'w') as z:
   for n,payload_bytes in members:
    info=zipfile.ZipInfo(n,date_time=(2026,10,18,0,0,0));z.writestr(info,payload_bytes)
 raw=b.getvalue();p=OUT/(name+'.npz')
 with p.open('xb') as f:f.write(raw)
 error=None
 try:got=M.npz_identity_bytes(raw);refused=False
 except ValueError as e:error=str(e);refused=True
 expected_code='DUPLICATE_NPZ_MEMBER' if name.startswith('duplicate') else 'NPZ_MEMBER_NOT_NPY'
 passed=(refused and expected_code in error) if must_fail else (not refused and set(got)=={'weighted_responses'})
 rows.append({'case':name,'expect':'MUST_FAIL' if must_fail else 'MUST_PASS','passed':passed,'refused':refused,'error':error,'fixture':{'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()}})
record={'label':'TESTED direct NPZ parser only; full comparator selftest UNTESTED here','candidate':{'path':str(SRC),'sha256':hashlib.sha256(SRC.read_bytes()).hexdigest()},'rows':rows,'passed':sum(x['passed'] for x in rows),'total':len(rows)}
with (OUT/'NPZ_LOGICAL_PREP_RESULTS_V001.json').open('x') as f:json.dump(record,f,indent=1)
print(record['passed'],record['total']);assert all(x['passed'] for x in rows)
