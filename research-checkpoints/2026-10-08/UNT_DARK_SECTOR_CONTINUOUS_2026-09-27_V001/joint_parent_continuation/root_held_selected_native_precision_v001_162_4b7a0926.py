"""Guarded NEW two-row Decimal precision experiment; no global action or solve."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal,localcontext
import argparse,hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SELECTED_NATIVE_FE_PRECISION_WITNESS_V001'
AUTHOR_DRAFT=True
PROTOCOL_SHA='2a4ce3dc9ceefb87bd239b64c4549a1855adc0cfaee38dda1986524144a58af3'
REVIEWED_ANCESTORS=(('authoring_cross_u_selected_native_fe_precision_witness_v001_159_938065b3.py', '938065b3a4eaba0ac93229848801456eccd1f0ac3ec95de45093680d50a70c29'), ('authoring_CROSS_U_SELECTED_NATIVE_FE_PRECISION_WITNESS_V001_12_ec483693.md', 'ec483693be877195f6fd13e3c60c4d3df475f0fef81a51a4438f0e7be158b3ea'))
TOL=Decimal('2e-11');FLOOR=Decimal('1e-30')
ROWS=((10,0,82,39),(14,0,84,37));CORNERS=((0,0),(1,0),(0,1),(1,1))
np=None;OWNER=None;INPUTS={};OUTPUTS={};CHECKS=[]
FLAGS=dict(original_canonical_admission=False,physical_rate_adoption=False,normal_constraint_seed=False,metric_adoption=False,galaxy_prediction=False)
PARENTS=(('CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V002',41181,'6759a9c44574bfd75865d1867c4467df18deca79a162979b89f1546ba9e417b7','2b6603b36ef3596c419d76e2ce82ac9c50dae31d150fb850f2d4179a56e3ff70'),('CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001',39611,'efffd53fc12abd68daf723a418de8c58b05374e5ad117c260ad2cbde73fbae82','8f306769022830cb0762e735308f493b072b58320fbdffabf46898c5a180f473'),('CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001',28469,'e5a8f065a865245a430a2b23fe1c69a20ae2dd542071e5804a216f2f604f8fe5','00478e51c5ae07c31707ca8ec548bef193d33b2f76dc4b09361efd6e281727ae'))

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(p):
 h=hashlib.sha256()
 with path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def bind(n,h):
 key=str(path(n).resolve());assert key not in INPUTS or INPUTS[key]==h
 assert sha(n)==h,n;INPUTS[key]=h
def publish(tag,obj):
 n=STEM+'_'+tag+'.json';raw=(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 with path(n).open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 path(n).chmod(0o444);assert path(n).read_bytes()==raw;OUTPUTS[n]=sha(n);return dict(file=n,sha256=OUTPUTS[n])
def recheck():
 for n,h in INPUTS.items():assert sha(n)==h,n
 assert sha(__file__)==OWNER['source_sha256']
 for n,h in OUTPUTS.items():assert sha(n)==h,n
def admitted():
 for n,h in REVIEWED_ANCESTORS:bind(n,h)
 docs=[];maps={}
 for st,pid,rh,ch in PARENTS:
  bind(st+'_RESULT.json',rh);bind(st+'_RECEIPT.json',ch)
  r=json.loads(path(st+'_RESULT.json').read_text());rc=json.loads(path(st+'_RECEIPT.json').read_text())
  assert rc['status']=='CLOSED' and rc['owner']==r['owner'] and r['owner']['pid']==pid and r['owner']['owner']=='root'
  assert rc['result_sha256']==rh and rc.get('error_sha256') is None and rc['closed']>rc['owner']['started']
  assert all(c['passed'] for c in r['controls']) and all(v is False for v in r['qualification'].values())
  for mapping in (rc['input_sha256'],rc['output_sha256']):
   for n,h in mapping.items():
    key=str(path(n).resolve());assert key not in maps or maps[key]==h;maps[key]=h
  docs.append(r)
 current,old,weak=docs
 assert current['status']==old['status']=='ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED'
 assert len(current['controls'])==21 and len(current['checkpoints'])==19 and len(old['controls'])==17 and len(old['checkpoints'])==25
 assert current['case']['trace_preparation'] is None and current['case']['parent_nonadmission_preserved'] is True
 assert current['owner']['source_sha256']=='f662ade49c204ba116049fa7de6b303575ef219dc8dd6313df5c3fbd453b6ea0'
 bind('cross_u_canonical_nodal_metric_rate_solve_v002.py',current['owner']['source_sha256'])
 bind(PARENTS[0][0]+'.md','0128d1613b8f43f8dce40ed5cb2c5a72b974104da3e838deff6cfec4345b0465')
 def unique(r,kind):
  q=[x for x in r['checkpoints'] if x['metadata']['kind']==kind];assert len(q)==1;return q[0]
 records=dict(solution=current['case']['compatibility'],basis=unique(old,'unchanged_E_F_S_bases_and_positive_solver_congruences'),coefficient=unique(weak,'complete_fixed_metric_native99_mass_coefficients'))
 cols=[q for q in old['checkpoints'] if q['metadata']['kind']=='copied_signed_blocks_and_current_actual_affine_reference']
 assert len(cols)==4 and [q['metadata']['column'] for q in cols]==list(range(4));records.update({str(i):q for i,q in enumerate(cols)})
 for rec in records.values():
  for key in ('file','commit_file'):assert maps[str(path(rec[key]).resolve())]==rec['sha256' if key=='file' else 'commit_sha256'];bind(rec[key],rec['sha256' if key=='file' else 'commit_sha256'])
  assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 return records,dict(parent_nonadmission_preserved=True,parent_map_authority='hashed CLOSED receipts; only selected immutable files rehashed',old_controls=current['controls'],old_qualification=current['qualification'])
def read_pair(rec,names):
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert set(f.files)==set(rec['metadata']['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==rec['metadata']
  out={}
  for n in names:
   a=f[n];s=rec['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and a.dtype.kind in 'fi' and np.all(np.isfinite(a)),n
   out[n]=a.copy()
 return out
def D(x):
 return Decimal.from_float(float(x))
def dots(a,b):return sum((x*y for x,y in zip(a,b)),Decimal(0))
def check(n,a,b,e):
 ratio=abs(a-b)/max(e,FLOOR);row=dict(name=n,actual=str(a),expected=str(b),envelope=str(e),error=str(ratio),tolerance=str(TOL),passed=ratio<=TOL)
 CHECKS.append(row);assert row['passed'],row
def factors(R,hat):
 # Freeze the original binary64 geometric intermediates; no Decimal redefinition of FE coefficients.
 rr=np.asarray(R,dtype=np.float64);r2=float(rr**2);r3=float(rr**3)
 F=np.zeros((6,6));F[0,0]=1.;F[0,1]=r2;F[1,5]=1.;F[2,0]=r2;F[3,3]=R;F[4,2]=r3;F[5,4]=r2
 nf=[];mf=[]
 for h in hat:
  nf.append([float(h),float(h),float(np.float64(r2)*np.float64(h))]);mf.append((np.float64(h)*F).tolist())
 return nf,mf,r2,r3
def extract(rec):
 s=read_pair(rec['solution'],('native_nodal_rate','metric_nodal_rate','compatibility_native_original_rhs','compatibility_native_original_residual','compatibility_original_action','current_Pn'))
 g=read_pair(rec['basis'],('R','dv','hats','cell_i','cell_j','native_scale','r','z'))
 b=read_pair(rec['coefficient'],('mixing_L','modal_D'))
 assert s['native_nodal_rate'].shape==(33,3,87,45) and s['metric_nodal_rate'].shape==(6,87,45) and b['mixing_L'].shape==b['modal_D'].shape==(32,15136,3,3)
 rows=[]
 for group,component,ni,nj in ROWS:
  assert component==0 and 1<ni<85 and 1<nj<43;mode=group-1;packed_index=group*11524+(ni-1)*45+nj
  row=dict(group=group,mode_index=mode,component=component,node=[ni,nj],packed_native_index=packed_index,original_rhs=float(s['compatibility_native_original_rhs'][group,component,ni,nj]),original_float_residual=float(s['compatibility_native_original_residual'][group,component,ni,nj]),original_float_action=float(s['compatibility_original_action'][packed_index]),actual_Pn_target=float(s['current_Pn'][group,component,ni,nj]),scale=float(g['native_scale'][group,component,ni,nj]),rate=float(s['native_nodal_rate'][group,component,ni,nj]),contacts=[])
  for iq in range(4):
   col=read_pair(rec[str(iq)],('B','cn','pstar','vstar','kstar'))
   for ci,cj in ((ni-1,nj-1),(ni-1,nj),(ni,nj-1),(ni,nj)):
    local=ci*44+cj;p=iq*3784+local
    assert int(g['cell_i'][local])==ci and int(g['cell_j'][local])==cj
    a=CORNERS.index((ni-ci,nj-cj));R=float(g['R'][iq,local]);dv=float(g['dv'][iq,local]);hat=[float(g['hats'][iq,j,0,ci,cj]) for j in range(4)]
    nf,mf,r2,r3=factors(R,hat);weight=float(np.float64(dv)/np.float64(R));scatter=float(np.float64(hat[a]));assert R>0 and weight>0 and all(h>0 for h in hat)
    vn=[[float(s['native_nodal_rate'][q,c,ci+di,cj+dj]) for di,dj in CORNERS] for q in (0,group) for c in range(3)]
    kn=[[float(s['metric_nodal_rate'][c,ci+di,cj+dj]) for di,dj in CORNERS] for c in range(6)]
    row['contacts'].append(dict(iq=iq,cell=[ci,cj],local=local,point=p,row_corner=a,R=R,dv=dv,weight64=weight,R2_64=r2,R3_64=r3,hats=hat,native_factors=nf,metric_factors=mf,scatter_factor64=scatter,native_corner_values=vn,metric_corner_values=kn,L=b['mixing_L'][mode,p].tolist(),modal_D=b['modal_D'][mode,p].tolist(),Bz=col['B'][local,group*3:(group+1)*3].tolist(),cn=col['cn'][local,group*3:(group+1)*3].tolist(),pstar=col['pstar'][local,group*3:(group+1)*3].tolist(),vstar_U=col['vstar'][local,:3].tolist(),vstar_Z=col['vstar'][local,group*3:(group+1)*3].tolist(),kstar=col['kstar'][local].tolist()))
  assert len(row['contacts'])==16 and len({p['point'] for p in row['contacts']})==16;rows.append(row)
 return rows
def polynomial(row,precision):
 with localcontext() as ctx:
  ctx.prec=precision;direct=centered=env=cs=ps=ds=Decimal(0);points=[]
  for p in row['contacts']:
   L=[[D(x) for x in r] for r in p['L']];dm=[[D(x) for x in r] for r in p['modal_D']];bz=[[D(x) for x in r] for r in p['Bz']]
   v=[dots([D(x) for x in p['native_corner_values'][c]],[D(p['native_factors'][j][c%3]) for j in range(4)]) for c in range(6)]
   k=[sum((D(p['metric_corner_values'][a][j])*D(p['metric_factors'][j][t][a]) for j in range(4) for a in range(6)),Decimal(0)) for t in range(6)]
   def modal(u,z,h):return [dots(dm[a],[z[t]+dots(L[t],u) for t in range(3)])+dots(bz[a],h) for a in range(3)]
   val=modal(v[:3],v[3:],k);ru=[D(x) for x in p['vstar_U']];rz=[D(x) for x in p['vstar_Z']];rh=[D(x) for x in p['kstar']]
   ref=modal(ru,rz,rh);delta=modal([v[t]-ru[t] for t in range(3)],[v[t+3]-rz[t] for t in range(3)],[k[t]-rh[t] for t in range(6)])
   cn=[D(x) for x in p['cn']];star=[D(x) for x in p['pstar']];defect=[cn[t]+ref[t]-star[t] for t in range(3)]
   momentum=[star[t]+defect[t]+delta[t] for t in range(3)];q=D(p['weight64'])*D(p['scatter_factor64']);direct+=q*val[0];centered+=q*(momentum[0]-cn[0]);cs+=q*cn[0];ps+=q*star[0];ds+=q*(defect[0]+delta[0])
   positive=dots([abs(x) for x in dm[0]],[abs(v[t+3])+dots([abs(x) for x in L[t]],[abs(x) for x in v[:3]]) for t in range(3)])+dots([abs(x) for x in bz[0]],[abs(x) for x in k]);env+=abs(q)*(positive+abs(momentum[0])+abs(cn[0])+sum(abs(x) for x in defect)+sum(abs(x) for x in delta))
   points.append(dict(point=p['point'],U_rate=list(map(str,v[:3])),Z_rate=list(map(str,v[3:])),metric_rate=list(map(str,k)),mode_terms=dict(D_vz=str(dots(dm[0],v[3:])),D_Lvu=str(dots(dm[0],[dots(L[t],v[:3]) for t in range(3)])),Bz_k=str(dots(bz[0],k))),point_reference_defect=list(map(str,defect)),point_centered_momentum=list(map(str,momentum))))
  rhs=D(row['original_rhs']);target=D(row['actual_Pn_target']);res=rhs-direct;epsilon=D(row['original_float_residual'])-res;rhs_defect=rhs-(target-cs);target_defect=target-ps
  centered_res=rhs_defect+target_defect-ds
  check('row%d_precision%d_centered_action'%(row['group'],precision),centered,direct,env)
  check('row%d_precision%d_original_centered_residual'%(row['group'],precision),centered_res,res,env+abs(rhs)+abs(target))
  return dict(precision=precision,action=str(direct),centered_action=str(centered),original_rhs_residual=str(res),scaled_original_residual=str(res/D(row['scale'])),saved_residual_minus_high_precision=str(epsilon),actual_Pn_residual=str(target-cs-direct),frozen_rhs_defect=str(rhs_defect),target_scatter_defect=str(target_defect),operation_envelope=str(env),points=points)
def fixtures():
 operands=(float(2**60),1.,-float(2**60));out=[];product=(float(2**53+2),1.-2.**-52,-float(2**53),1.)
 for precision in (70,100):
  with localcontext() as ctx:
   ctx.prec=precision;value=sum(map(D,operands),Decimal(0));check('fresh_three_term_cancellation_%d'%precision,value,Decimal(1),Decimal(1));out.append(dict(precision=precision,result=str(value)))
   value=D(product[0])*D(product[1])+D(product[2])*D(product[3]);expected=-Decimal(2)**-51;check('fresh_product_low_part_%d'%precision,value,expected,abs(expected));out[-1]['product_low_part']=str(value)
 nf,mf,_,_=factors(2.,(1/4,)*4);phi=sum(D(j+1)*D(nf[j][2]) for j in range(4));check('fresh_covector_phi_R_squared',phi,Decimal(10),Decimal(20))
 answer=(9,6,4,8,24,20);metric=[sum(D(j+1)*D(mf[a][t][j]) for a in range(4) for j in range(6)) for t in range(6)]
 check('fresh_metric_F_order_without_extra_offdiag_two',max(abs(x-Decimal(y)) for x,y in zip(metric,answer)),Decimal(0),Decimal(1))
 return dict(operands=operands,binary64_left_associated=(operands[0]+operands[1])+operands[2],exact_expected='1',product_operands=product,product_binary64=product[0]*product[1]+product[2]*product[3],product_exact_expected='-2^-51',decimal=out,phi_R2=str(phi),metric_F=list(map(str,metric)))
def main():
 global np,OWNER
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 assert args.root_run and not AUTHOR_DRAFT and PROTOCOL_SHA,'Guarded NEW two-row precision experiment; ROOT only'
 assert not list(BASE.glob(STEM+'_*'));bind(STEM+'.md',PROTOCOL_SHA)
 records,ancestry=admitted();OWNER=dict(owner='root',pid=os.getpid(),started=datetime.now(timezone.utc).isoformat(),source_sha256=sha(__file__),scope='two selected FE mode rows only')
 publish('OWNER_START',OWNER)
 try:
  import numpy as np_local
  np=np_local;raw=extract(records);rawref=publish('POINT_OPERANDS',dict(owner=OWNER,rows=raw,qualification=FLAGS,selected_records=[{k:v[k] for k in ('file','sha256','commit_file','commit_sha256')} for v in records.values()],contract='Freeze original binary64 dv/R,R powers and hat-times-F/native factors; Decimal.from_float ingestion; no full A replay'))
  fix=fixtures();publish('FIXTURE',dict(owner=OWNER,fixture=fix,controls=CHECKS.copy()))
  results=[]
  for row in raw:
   a=polynomial(row,70);publish('ROW_%d_PRECISION70'%row['group'],dict(owner=OWNER,selection=[row['group'],row['component'],row['node']],result=a,controls=CHECKS.copy(),qualification=FLAGS))
   b=polynomial(row,100);publish('ROW_%d_PRECISION100'%row['group'],dict(owner=OWNER,selection=[row['group'],row['component'],row['node']],result=b,controls=CHECKS.copy(),qualification=FLAGS))
   with localcontext() as ctx:
    ctx.prec=100;check('row%d_precision70_vs100'%row['group'],Decimal(a['action']),Decimal(b['action']),Decimal(b['operation_envelope']))
   results.append(dict(selection={k:row[k] for k in row if k!='contacts'},decimal70=a,decimal100=b));publish('ROW_%d'%row['group'],dict(owner=OWNER,row=results[-1],controls=CHECKS.copy(),qualification=FLAGS))
  recheck();publish('MANIFEST',dict(owner=OWNER,input_sha256=INPUTS,output_sha256=OUTPUTS.copy(),qualification=FLAGS))
  result=publish('RESULT',dict(status='BOUNDED_PRECISION_WITNESS_COMPLETE',owner=OWNER,rows=results,controls=CHECKS,point_operands=rawref,ancestry=ancestry,qualification=FLAGS,full_row_admission=False,new_operator_solve=False,coefficient_rounding='D/L/B entries exact saved binary64; elementary geometry intermediates frozen to original binary64 before Decimal; no longdouble used'))
  recheck();publish('RECEIPT',dict(status='CLOSED',owner=OWNER,closed=datetime.now(timezone.utc).isoformat(),result_sha256=result['sha256'],error_sha256=None,input_sha256=INPUTS,output_sha256=OUTPUTS.copy(),qualification=FLAGS));recheck();print(json.dumps(dict(status='BOUNDED_PRECISION_WITNESS_COMPLETE',pid=OWNER['pid'],controls=len(CHECKS),result_sha256=result['sha256'])))
 except BaseException:
  actual={p.name:sha(p) for p in BASE.glob(STEM+'_*') if p.is_file()}
  for n in actual:path(n).chmod(0o444)
  error=publish('ERROR',dict(status='FAILED',owner=OWNER,traceback=traceback.format_exc(),controls=CHECKS,actual_prior_files=actual,qualification=FLAGS));prior=path(STEM+'_RECEIPT.json')
  publish('ERROR_RECEIPT' if prior.exists() else 'RECEIPT',dict(status='CLOSED_ERROR',owner=OWNER,closed=datetime.now(timezone.utc).isoformat(),error_sha256=error['sha256'],result_sha256=None,prior_receipt_sha256=sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=OUTPUTS.copy(),qualification=FLAGS));raise
if __name__=='__main__':main()
