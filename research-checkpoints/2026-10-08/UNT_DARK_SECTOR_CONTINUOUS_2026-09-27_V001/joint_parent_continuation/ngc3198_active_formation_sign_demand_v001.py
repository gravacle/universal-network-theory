#!/usr/bin/env python3
"""Bounded root-only arithmetic on frozen observed/model velocities; no force law or fit."""
from pathlib import Path
import argparse,hashlib,json,math,os,sys
from datetime import datetime,timezone
AUTHOR_DRAFT=False
J=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
STEM='NGC3198_ACTIVE_FORMATION_SIGN_DEMAND_V001'
PINS={
 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_RESULT.json':'963de6b73e19820fc424bbb994d7e07fbed4ecea4401b25730fbe38499f1524d',
 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_RECEIPT.json':'b7834e205c379e8f9444e3ac17243744fc2266f92ccd186bcd780a7cebaac926',
 'NGC3198_ACTIVE_SOURCE_OBSERVATION_AUDIT_V001.json':'76675a2ffa36acd3c58e73d5f268a5ce2b6e63cf72d37bd9b1489ee7da593063'}
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def verify():
 for p,h in PINS.items():
  if sha(J/p)!=h:raise RuntimeError('Frozen input changed: '+p)
def put(p,obj):
 with p.open('x') as f:json.dump(obj,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 p.chmod(0o444)
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root-execute',action='store_true');a=parser.parse_args()
 if not a.root_execute or AUTHOR_DRAFT:raise RuntimeError('Held author draft or missing root execution flag')
 if sys.platform!='darwin' or Path(__file__).resolve()!=J/'ngc3198_active_formation_sign_demand_v001.py':raise RuntimeError('Root Mac/source context')
 if any(p.name!=STEM+'.md' for p in J.glob(STEM+'*')):raise FileExistsError('Prior output namespace is preserved')
 verify();r=json.loads((J/'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_RESULT.json').read_text());c=json.loads((J/'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_RECEIPT.json').read_text());s=json.loads((J/'NGC3198_ACTIVE_SOURCE_OBSERVATION_AUDIT_V001.json').read_text())
 if c['status']!='CLOSED' or c['owner']['pid']!=78729 or c['result_sha256']!=PINS['CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_RESULT.json']:raise RuntimeError('Parent closure/owner')
 case=next(x for x in r['cases'] if x['arm']=='FINE_Q3')
 if case['status']!='CONVERGED' or len(case['rows'])!=43 or len(s['rows'])!=23 or s['adopted_in_galaxy_solver'] is not False:raise RuntimeError('Exact original case/source census')
 final=case['final_checkpoint']
 if sha(J/final['file'])!=final['sha256'] or sha(J/final['commit_file'])!=final['commit_sha256']:raise RuntimeError('Frozen fine-state pair changed')
 lo=min(x['R_kpc'] for x in s['rows']);hi=max(x['R_kpc'] for x in s['rows'])
 if any(x['SFR_surface_Msun_yr_kpc2']<=0 for x in s['rows']):raise RuntimeError('Declared proxy positivity fails')
 owner=dict(pid=os.getpid(),utc=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),inputs=PINS,parent_pid=78729,operation='required velocity-squared correction intervals; no fit/source/force adoption')
 put(J/(STEM+'_OWNER_START.json'),owner);rows=[]
 try:
  for x in case['rows']:
   R=x['R_kpc'];v=x['observed_velocity_kms'];e=x['observed_error_kms'];model=[x['Q1_left_v2'],x['Q1_right_v2']]
   if not all(math.isfinite(y) for y in (R,v,e,*model)) or R<=0 or v<0 or e<0:raise ArithmeticError('Original speed/error schema')
   lower=max(0.,v-e);upper=v+e
   bands=[[lower**2-u,upper**2-u] for u in model]
   intersection=[max(z[0] for z in bands),min(z[1] for z in bands)]
   kind='requires_positive' if min(z[0] for z in bands)>0 else 'requires_negative' if max(z[1] for z in bands)<0 else 'not_common_sign'
   rows.append(dict(original_row=x,R_kpc=R,observed_speed_band_kms=[lower,upper],lower_band_clipped_at_zero=v-e<0,signed_model_v2_left_right_kms2=model,required_delta_v2_left_right_kms2=bands,joint_reading_intersection_kms2=intersection,empty_joint_reading_intersection=intersection[0]>intersection[1],common_quoted_error_sign=kind,within_activity_proxy_radial_coverage=lo<=R<=hi))
  verify();put(J/(STEM+'_RESULT.json'),dict(status='ARITHMETIC_CLOSED',owner=owner,rows=rows,counts={k:sum(x['common_quoted_error_sign']==k for x in rows) for k in ('requires_positive','requires_negative','not_common_sign')},covered_counts={k:sum(x['common_quoted_error_sign']==k and x['within_activity_proxy_radial_coverage'] for x in rows) for k in ('requires_positive','requires_negative','not_common_sign')},original_activity_rows=s['rows'],proxy_coverage_kpc=[lo,hi],interpretation='A nonnegative local added delta-v-squared term cannot repair requires_negative rows. This does not test the full signed retarded UNT stress or prove an active formation correction.',physical_source_or_history_selected=False,new_force_or_fit=False,units='velocity-squared correction (km/s)^2',parent_final=dict(file=final['file'],sha256=final['sha256'],commit_file=final['commit_file'],commit_sha256=final['commit_sha256'])))
  result=J/(STEM+'_RESULT.json');verify();put(J/(STEM+'_RECEIPT.json'),dict(status='CLOSED',pid=os.getpid(),source_sha256=owner['source_sha256'],inputs=PINS,result_sha256=sha(result),owner_sha256=sha(J/(STEM+'_OWNER_START.json'))))
  out=json.loads(result.read_text());print(json.dumps(dict(status='CLOSED',pid=os.getpid(),counts=out['counts'],covered_counts=out['covered_counts'],result_sha256=sha(result))))
 except BaseException as exc:
  put(J/(STEM+'_ERROR.json'),dict(status='CLOSED_ERROR',owner=owner,partial_rows=rows,error=repr(exc)));raise
if __name__=='__main__':main()
