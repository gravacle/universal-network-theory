"""Guarded saved-word closure of actual80429; no density/CMC/FE replay."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMBINED_INITIAL_WEAK_CMC_DERIVATIVE_V002'
OUT='READONLY_COMBINED_INITIAL_CMC_CLOSURE_V002_RESULT.json'
AUTHOR_DRAFT=True
SOURCE='cross_u_combined_initial_weak_CMC_derivative_v002.py'
SOURCE_SHA='95061a24538ba691f612f27e67c95efe75385b74db29f388830cff84c0aa1c33'
PROTOCOL_SHA='10f345d40f1f7d56d4e03fc4ed88aeea4b98a6ffcf755d3c86e73e39054062ff'
TERMINAL=dict(pid=80429,result_sha256='2a18a4311b38f7956c8bf5b758dc1ba855790834847cdca82d33cbcad9ed53b5',receipt_sha256='0abe61a43ee25e8d9efb8d0add02fe51ed33332ac9249d88b7cda97d1417b9d6',error_sha256=None)
COMBINED='CROSS_U_COMBINED_CONFIGURATION_NORMAL_DERIVATIVE_V001'
RECOVERY='READONLY_COMBINED_NORMAL_DERIVATIVE_RECOVERY_V001_RESULT.json'
RECOVERY_SHA='899f6d8697a234b25c7f6bddd68215ed649cdaa6b6663263950c963b2cd5a371'
COMBINED_TERMINAL=dict(pid=65324,result_sha256=None,receipt_sha256='e4ce7828602f9ec078638919f13e09c705080a0b178ecd66a5365b620044ed26',error_sha256='d3dfa80d9948a258295d622721a3d3daf754fb61e064626885b705b750881eb2')
TOL=2e-11
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def saved_json(n,h):
 assert h is not None and sha(n)==h,n
 return json.loads(path(n).read_text())
def main():
 assert AUTHOR_DRAFT is False and not path(OUT).exists() and all(TERMINAL[n] is not None for n in ('pid','result_sha256','receipt_sha256'))
 assert sha(SOURCE)==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 r=saved_json(STEM+'_RESULT.json',TERMINAL['result_sha256']);rc=saved_json(STEM+'_RECEIPT.json',TERMINAL['receipt_sha256'])
 assert rc['status']=='CLOSED' and rc['result_sha256']==TERMINAL['result_sha256'] and rc.get('error_sha256') is None and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA
 assert r['status']=='COMBINED_DIRECTION_INITIAL_WEAK_CMC_DERIVATIVE_MEASURED' and r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 assert all(r[n] is False for n in ('finite_configuration_prepared','initial_CMC_qualified','primitive_bridge_resolved','physical_adoption'))
 records=r['checkpoints'];controls=r['controls'];assert len(records)==6 and len(controls)==1 and r['input']==records[0] and r['columns']==records[1:5] and r['loads']==records[5]
 assert len({q['file'] for q in records})==6 and {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 for q in records:
  for n,k in ((q['file'],'sha256'),(q['commit_file'],'commit_sha256')):assert rc['output_sha256'][n]==q[k] and sha(n)==q[k]
  assert saved_json(q['commit_file'],q['commit_sha256'])=={n:q[n] for n in ('file','sha256','metadata')} and q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification'] and q['metadata']['failed'] is False
  assert all(s['finite'] is True for s in q['metadata']['schema'].values())
 def inherited(n,h):
  key=n if n in rc['input_sha256'] else str(path(n).resolve());assert rc['input_sha256'][key]==h
  return saved_json(n,h)
 proof=inherited(RECOVERY,RECOVERY_SHA);old=inherited(COMBINED+'_ERROR.json',COMBINED_TERMINAL['error_sha256']);oldrc=inherited(COMBINED+'_RECEIPT.json',COMBINED_TERMINAL['receipt_sha256'])
 assert proof['status']=='RECOVERED_COMPLETE_COMBINED_NORMAL_DERIVATIVE_SAVED_WORDS_PASS' and proof['parent']==COMBINED_TERMINAL and proof['controls']==4 and proof['committed_pairs']==7 and proof['original_closed_error_preserved'] is True and proof['complete_calculation_evidence'] is True
 assert all(proof[n] is False for n in ('formal_LOADS_committed','formal_RESULT_published','original_primitive_bridge_resolved','normal_constraints_qualified','reachable_rank_or_five_field_admission_claimed','physical_adoption'))
 assert old['status']=='FAILED' and oldrc['status']=='CLOSED_ERROR' and oldrc['owner']==old['owner'] and old['owner']['pid']==65324 and oldrc['error_sha256']==COMBINED_TERMINAL['error_sha256'] and oldrc.get('result_sha256') is None and old['qualification']==oldrc['qualification'] and all(v is False for v in old['qualification'].values()) and not path(COMBINED+'_RESULT.json').exists() and not list(BASE.glob(COMBINED+'_*_LOADS.npz'))
 import numpy as np
 selected=[];identities=[]
 def read(q,names):
  out={};schema=q['metadata']['schema']
  with np.load(path(q['file']),allow_pickle=False) as z:
   assert set(z.files)==set(schema)|{'metadata_json'} and json.loads(str(z['metadata_json']))==q['metadata']
   for n in names:
    x=z[n].copy();assert list(x.shape)==schema[n]['shape'] and str(x.dtype)==schema[n]['dtype'] and schema[n]['finite'] is True and np.all(np.isfinite(x)),n;out[n]=x
  selected.append(dict(file=q['file'],fields=len(names)));return out
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def total(x):return x[0]+x[1]
 def identity(name,terms):
  words=[sign*w for sign,x in terms for w in x];gap=np.add.reduce(words);bound=np.add.reduce([abs(w) for w in words]);error=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0));assert error<=TOL,(name,error);identities.append(dict(name=name,error=error))
 def norm(x):return dict(L2=float(np.linalg.norm(x)),Linf=float(np.max(abs(x),initial=0)),nonzero=int(np.count_nonzero(x)))
 inp,columns,loads=records[0],records[1:5],records[5];md=inp['metadata']
 assert md['kind']=='same_combined_direction_initial_CMC_derivative_inputs' and md['phase_direct_metric_CMC_contact_zero'] is True and math.isfinite(md['Hbar']) and md['Hbar']>0 and md['combined_input']==proof['recovered_records']['input'] and md['columns']==proof['recovered_records']['columns']
 assert md['signed_bridge_refs']['prior_signed_primitive_readout']['metadata']['canonical_primitive_readout_admitted'] is False and md['signed_bridge_refs']['warm_readout']['metadata']['original_finite_stationarity_gap_retained'] is True
 assert len(inp['metadata']['schema'])==3 and len(loads['metadata']['schema'])==33 and loads['metadata']['kind']=='same_combined_direction_initial_weak_CMC_contact' and loads['metadata']['scalar_free_coordinates']==3870 and loads['metadata']['Hbar_fixed'] is True and loads['metadata']['initial_CMC_only'] is True and loads['metadata']['full_CMC_preservation_computed'] is False and loads['metadata']['controls']==controls
 assert loads['metadata']['columns']==[{k:q[k] for k in ('file','sha256','commit_file','commit_sha256')} for q in columns]
 names=tuple(n+'_'+w for n in ('compact_density_contact','rate_density_contact','total_density_contact','compact_weak_initial_CMC_contact','rate_weak_initial_CMC_contact','total_weak_initial_CMC_contact')+tuple(part+'_functional_'+kind for part in ('compact','rate','total') for kind in ('nodal','direct','gap')) for w in ('hi','lo'))
 c=controls[0];assert c['ordinal']==0 and c['name']=='new_initial_CMC_scalar_nodal_direct_functionals' and c['tolerance']==TOL and c['passed'] is True
 prefix='control_000_'+c['name']+'_';triplet=tuple(prefix+n for n in ('actual','expected','envelope'));a=read(loads,names+triplet)
 actual,expected,envelope=(a[n] for n in triplet);assert actual.shape==expected.shape==envelope.shape==(3,) and np.all(expected==0) and np.all(envelope>=0)
 error=float(np.max(abs(actual-expected)/np.maximum(envelope,1e-30),initial=0));assert error==c['error'] and error<=TOL;identities.append(dict(name=c['name'],error=error))
 density=[];point_norms=[]
 for iq,q in enumerate(columns):
  qm=q['metadata'];assert len(qm['schema'])==59 and qm['kind']=='new_same_direction_initial_weak_CMC_density_contact' and qm['column']==iq and qm['phase_direct_metric_contact_zero'] is True and qm['Gamma_and_ADM_serialized_trace_gaps_retained'] is True and qm['physical_ports'] is None
  for key,group in (('combined_rate_ref','columns'),('current_moment_ref','pilots'),('compact_ref','compact')):assert qm[key]==md[group][iq]
  base=('initial_CMC_compact_trace_contact_density','initial_CMC_compact_measure_contact_density','initial_CMC_compact_initial_CMC_density_contact','initial_CMC_global_induced_rate_initial_CMC_density_contact','initial_CMC_embedded_compact_initial_CMC_density_contact','initial_CMC_combined_initial_CMC_density_contact','initial_CMC_current_pointwise_initial_CMC_gap','initial_CMC_compact_sqrt_h_minus_4D_density_chain_contact','copied_compact_Gamma_minus_ADM_density_contact','copied_compact_Gamma_minus_ADM_pointwise_CMC_gap','new_compact_density_minus_saved_Gamma_density_contact','current_sqrt_h_minus_native_density_reference','current_native_density_reference_quotient')
  owned=tuple('owned_compact_trace_'+kind+'_'+field for kind in ('Gamma','ADM') for field in ('delta_density','pointwise_CMC_gap'))
  b=read(q,tuple(n+'_'+w for n in base+owned for w in ('hi','lo'))+('compact_point_indices','owned_compact_indices','owned_current_chart_sqrt_h'))
  take=b['compact_point_indices'];assert take.dtype==np.int64 and take.shape==(4,) and np.array_equal(take,b['owned_compact_indices']) and len(np.unique(take))==4 and np.all((0<=take)&(take<3784))
  identity('column%d_compact_trace_plus_measure'%iq,[(1,pair(b,base[0])),(1,pair(b,base[1])),(-1,pair(b,base[2]))])
  embedded=pair(b,base[4]);compact=pair(b,base[2]);rate=pair(b,base[3]);combined=pair(b,base[5]);assert all(x.shape==(3784,) for x in embedded+rate+combined) and all(x.shape==(4,) for x in compact)
  for word in (0,1):assert np.array_equal(embedded[word][take],compact[word]) and np.all(np.delete(embedded[word],take)==0)
  identity('column%d_embedded_compact_plus_rate'%iq,[(1,embedded),(1,rate),(-1,combined)])
  for field,name in (('delta_density','copied_compact_Gamma_minus_ADM_density_contact'),('pointwise_CMC_gap','copied_compact_Gamma_minus_ADM_pointwise_CMC_gap')):identity('column%d_saved_Gamma_ADM_%s'%(iq,field),[(1,pair(b,'owned_compact_trace_Gamma_'+field)),(-1,pair(b,'owned_compact_trace_ADM_'+field)),(-1,pair(b,name))])
  identity('column%d_saved_compact_Gamma_difference'%iq,[(1,compact),(-1,pair(b,'owned_compact_trace_Gamma_delta_density')),(-1,pair(b,'new_compact_density_minus_saved_Gamma_density_contact'))])
  identity('column%d_saved_density_reference_difference'%iq,[(1,(b['owned_current_chart_sqrt_h'],np.zeros_like(b['owned_current_chart_sqrt_h']))),(-1,pair(b,'current_native_density_reference_quotient')),(-1,pair(b,'current_sqrt_h_minus_native_density_reference'))])
  density.append(dict(compact=embedded,rate=rate,total=combined));point_norms.append(dict(column=iq,norms={n:norm(total(pair(b,n))) for n in base[:-1]}))
 for part in ('compact','rate','total'):
  x=pair(a,part+'_density_contact');assert x[0].shape==x[1].shape==(15136,)
  for word in (0,1):assert np.array_equal(x[word],np.concatenate([d[part][word] for d in density]))
  w=pair(a,part+'_weak_initial_CMC_contact');assert w[0].shape==w[1].shape==(87,45)
  identity(part+'_saved_nodal_direct_gap',[(1,pair(a,part+'_functional_nodal')),(-1,pair(a,part+'_functional_direct')),(-1,pair(a,part+'_functional_gap'))])
 assert np.array_equal(np.asarray([float(total(pair(a,n+'_functional_gap'))) for n in ('compact','rate','total')]),actual)
 identity('saved_compact_rate_density_sum',[(1,pair(a,'compact_density_contact')),(1,pair(a,'rate_density_contact')),(-1,pair(a,'total_density_contact'))])
 identity('saved_compact_rate_weak_sum',[(1,pair(a,'compact_weak_initial_CMC_contact')),(1,pair(a,'rate_weak_initial_CMC_contact')),(-1,pair(a,'total_weak_initial_CMC_contact'))])
 report=dict(status='SAVED_COMBINED_INITIAL_CMC_CLOSURE_PASS',owner_pid=os.getpid(),parent=TERMINAL,recovered_combined_parent=COMBINED_TERMINAL,recovered_combined_proof=dict(file=RECOVERY,sha256=RECOVERY_SHA),original_combined_CLOSED_ERROR_preserved=True,controls=1,committed_pairs=6,identities=identities,selected=selected,point_diagnostic_norms=point_norms,density_norms={n:norm(total(pair(a,n+'_density_contact'))) for n in ('compact','rate','total')},weak_norms={n:norm(total(pair(a,n+'_weak_initial_CMC_contact'))) for n in ('compact','rate','total')},arithmetic_tolerance=TOL,phase_direct_metric_CMC_contact_zero=True,Hbar_fixed=True,initial_CMC_only=True,initial_CMC_constraint_qualified=False,primitive_bridge_resolved=False,full_CMC_preservation_computed=False,reachable_rank_or_finite_preparation_claimed=False,physical_adoption=False,old_input_maps_rehashed=False,density_CMC_FE_scatter_functional_feature_or_fixture_replayed=False,scope_limit='Selected saved words, trace+measure/compact+rate sums, embedding and COLUMN-to-LOADS copies, saved gaps/triplet and descriptive norms only. Density equation, scalar scatter, functional and any original producer are never called.')
 for q in records:assert sha(q['file'])==q['sha256'] and sha(q['commit_file'])==q['commit_sha256']
 assert sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256'] and sha(SOURCE)==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA and sha(RECOVERY)==RECOVERY_SHA
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
