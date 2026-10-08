"""AUTHORING ONLY: actual NEW139 coupled correction; no execution release.
Existing Ahat/Rv/three-chi/M/Rw coefficient consumers own the declared proxy.
Original147/87/290 contacts, original canonical gates and a naturally CLOSED
94->138->158 finite trial remain external authorities. All future pins None.
This source begins with exact saved phase-cache hydration and original packing.
No numerical body has been invoked during authoring.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
STEM='CROSS_U_NEW139_COUPLED425955_CORRECTION_V001'
CAP=40
PROTOCOL=None
PROTOCOL_SHA=None
COUPLED_DIMENSION=425955
COUPLED_NEW_CLOSURES={n:(None,None,None,None) for n in ('finite139','literal220','mechanical_gauge64','literal_rate_normal120','configuration_three_chi','mechanical_adjoint','phase_adjoint')}
COUPLED_INVARIANT_CLOSURES={n:(None,None,None,None) for n in ('updated_phase_mass','phase_rate_cache','nodal_factors','nodal_apply','paired_coefficients','original_targets','phase_gauge')}
np=P=N=None
SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)


def coupled_pair(label,x,shape):
 assert isinstance(x,tuple) and len(x)==2
 keep(label+'_both_words',np.stack(x).copy())
 for word,a in zip(('hi','lo'),x):
  keep(label+'_'+word,a.copy());assert a.dtype==np.float64 and a.shape==shape and np.all(np.isfinite(a))
 return tuple(a.copy() for a in x)


def coupled_saved_phase_names(iq):
 assert type(iq) is int and 0<=iq<4
 e='column%d_cached_EOS_'%iq;n=[]
 for key in {**EOS_SCALARS,**EOS_VECTORS,**EOS_MATRICES}:n.extend(e+'copied_'+key+'_'+w for w in ('hi','lo'))
 for name in ('hi','P','phi','U','uc','N','mu','ih','u'):n.extend(e+'same_candidate_'+name+'_'+w for w in ('hi','lo'))
 n.extend(e+'inherited_'+name for name in ('elementary_low_over_high','elementary_log_high','elementary_log1p_low'))
 for name in ('P','PX','PXX'):
  for kind in ('actual','expected','gap'):n.extend(e+'inherited_temporal_chain_'+name+'_'+kind+'_'+w for w in ('hi','lo'))
 for name in EOS_DIVISION_GAPS:n.extend(e+'inherited_primal_division_gap_'+name+'_'+w for w in ('hi','lo'))
 n.extend(e+'inherited_primal_'+name for name in ('current_operation_envelope','H_operation_envelope'))
 for row in range(4):
  p='cache_column%d_row%d_'%(iq,row)
  for name in NORMAL_FIELDS:n.extend(p+'copied_normal_'+name+'_'+w for w in ('hi','lo'))
  for name in ('g','hi','U','uc','P','phi','N','mu','h','beta'):n.extend(p+'same_cached_normal_'+name+'_'+w for w in ('hi','lo'))
  for name in ('It_phi','It_r','hi_rt'):n.extend(p+'NEW_fixed_contact_coefficient_'+name+'_'+w for w in ('hi','lo'))
  n.extend(p+'same_'+name for name in ('fixed_test_lapse','fixed_test_shift'))
  for name in ('X','pressure','PX'):n.extend(p+'same_cached_EOS_'+name+'_'+w for w in ('hi','lo'))
  for name in ('EOS_clock_square_contact','measure_test_trace_contact','unit_constraint','projector_construction_contact'):n.extend(p+'inherited_'+name+'_'+w for w in ('hi','lo'))
 assert len(n)==len(set(n));return tuple(n)


def coupled_hydrate_phase_rate_column(ref,data,constants,normal_s,normal_c,current_H,expected,keep,label):
 # Data are selected immutable28110 cache operands, not a new EOS/row action.
 md=ref['metadata'];iq=md['column'];p=3784;e='column%d_cached_EOS_'%iq
 assert md['role']=='TEMPORAL_CACHE_COLUMN' and md['kind']=='copied_updated_EOS_normal_primal_and_NEW_fixed_rate_derivative_coefficients'
 assert md['failed'] is md['physical_adoption'] is False and md['owner']['pid']==28110
 assert md['owner']['source_sha256']=='5c595057f4311bce62f4b76345d38b578cc6295492b488a954028a04179a5c38'
 assert expected['naturally_closed'] is True and expected['all_selected_seals_verified'] is True and expected['source_rate_independent_operands_verified'] is True
 assert md['state']==expected['state'] and md['finite_phase_column']==expected['finite_phase_column'] and md['normal_rows']==expected['normal_rows']
 assert md['input']==expected['input'] and md['new_fixed_coefficients']==['It_phi','It_r','hi_rt'] and md['old_chi_and_temporal_step_not_used_as_rate_direction'] is True
 assert expected['closure']==COUPLED_INVARIANT_CLOSURES['phase_rate_cache'] and all(x is not None for q in expected['closure'] for x in q)
 assert set(data)==set(coupled_saved_phase_names(iq))
 pair=lambda name,shape:coupled_pair(label+'_copied_'+name,tuple(data[name+'_'+w].copy() for w in ('hi','lo')),shape)
 values={key:pair(e+'copied_'+key,(p,4,4) if key in EOS_MATRICES else (p,4) if key in EOS_VECTORS else (p,)) for key in {**EOS_SCALARS,**EOS_VECTORS,**EOS_MATRICES}}
 s={n:normal_s[n] for n in ('g','hi','P','phi','U','uc')};c={n:normal_c[n] for n in ('N','mu','ih','u','h','beta')}
 for family,shapes in ((s,dict(hi=(p,4,4),P=(p,4,4),phi=(p,4),U=(p,4),uc=(p,4))),(c,dict(N=(p,),mu=(p,),ih=(p,3,3),u=(p,3)))):
  for name,shape in shapes.items():
   saved=pair(e+'same_candidate_'+name,shape);assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(saved,family[name]))
 assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(values['H'],current_H))
 assert constants['eps']==1e-5 and constants['C']==1.98 and constants['relative_phase_coefficient']==1. and constants['synthetic_control'] is False
 for n in ('X0','norm'):assert all(np.array_equal(a,b) for a,b in zip(values[n],P.a_dd(np.full(p,constants[n]))))
 assert np.all(values['X'][0]-abs(values['X'][1])>0) and np.all(values['u'][0]-abs(values['u'][1])>0) and np.all(constants['eps']-values['u'][0]-abs(values['u'][1])>0)
 inherited={}
 for n in ('elementary_low_over_high','elementary_log_high','elementary_log1p_low'):
  x=keep(label+'_inherited_'+n,data[e+'inherited_'+n].copy());assert x.dtype==np.float64 and x.shape==(p,) and np.all(np.isfinite(x));inherited[n]=x
 for n in ('P','PX','PXX'):
  for kind in ('actual','expected','gap'):inherited[n+'_'+kind]=pair(e+'inherited_temporal_chain_'+n+'_'+kind,(p,))
 for n in EOS_DIVISION_GAPS:inherited['division_'+n]=pair(e+'inherited_primal_division_gap_'+n,(p,4) if n=='clock_normalization' else (p,))
 for n,shape in (('current_operation_envelope',(p,4)),('H_operation_envelope',(p,))):
  x=keep(label+'_inherited_'+n,data[e+'inherited_primal_'+n].copy());assert x.dtype==np.float64 and x.shape==shape and np.all(np.isfinite(x)) and np.all(x>=0);inherited[n]=x
 eos=dict(values=values,s=s,c=c,constants=dict(constants),candidate_provenance=expected['phase_provenance'],EOS_values_recomputed=False,old_temporal_direction_reused=False,physical_adoption=False,inherited_stage_contacts=inherited)
 rows=[]
 for row in range(4):
  rp='cache_column%d_row%d_'%(iq,row);test={n:pair(rp+'copied_normal_'+n,(p,)+shape) for n,shape in NORMAL_FIELDS.items()}
  for family,shapes in ((normal_s,dict(g=(p,4,4),hi=(p,4,4),U=(p,4),uc=(p,4),P=(p,4,4),phi=(p,4))),(normal_c,dict(N=(p,),mu=(p,),h=(p,3,3),beta=(p,3)))):
   for n,shape in shapes.items():
    saved=pair(rp+'same_cached_normal_'+n,shape);assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(saved,family[n]))
  f=keep(label+'_row%d_fixed_lapse'%row,data[rp+'same_fixed_test_lapse'].copy());b=keep(label+'_row%d_fixed_shift'%row,data[rp+'same_fixed_test_shift'].copy());ef=np.ones(p) if row==0 else np.zeros(p);eb=np.zeros((p,3))
  if row:eb[:,row-1]=1.
  assert f.dtype==b.dtype==np.float64 and np.array_equal(f,ef) and np.array_equal(b,eb)
  for n in ('X','pressure','PX'):
   saved=pair(rp+'same_cached_EOS_'+n,(p,));assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(saved,values[n]))
  for n,shape in (('EOS_clock_square_contact',(p,)),('measure_test_trace_contact',(p,)),('unit_constraint',(p,)),('projector_construction_contact',(p,4,4))):pair(rp+'inherited_'+n,shape)
  for n in ('r','density'):assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(test[n],values[n]))
  coeff={n:pair(rp+'NEW_fixed_contact_coefficient_'+n,(p,4)) for n in ('It_phi','It_r','hi_rt')}
  rows.append(dict(test=test,s=normal_s,c={n:normal_c[n] for n in ('N','mu','h','beta')},f=f,b=b,contact_coefficients=coeff,cached_value_provenance=dict(record=thin(ref),row=row,original_row=md['normal_rows'][row]),phase_normal_value_recomputed=False,physical_adoption=False))
 return dict(eos=eos,normal_rows=rows,source=thin(ref),literal_phase_mass_and_gauge_rate_independence_verified=True,EOS_primal_or_fixed_coefficient_or_normal_VALUE_replayed=False,physical_adoption=False)


def coupled_unpack_unknown(x,keep,label):
 x=coupled_pair(label+'_packed_unknown',x,(425955,));mask=N.normal_test_mask();sm=P.scalar_mask();counts=[int(np.count_nonzero(a)) for a in mask]
 assert counts==[3740,3740,3655,3740] and int(np.count_nonzero(sm))==3870
 v=P.a_slice(x,slice(0,403340));wp=P.a_slice(x,slice(403340,407210));qp=P.a_slice(x,slice(407210,None));normal=P.a_dd(np.zeros((4,87,45)));t=P.a_dd(np.zeros((87,45)));w=P.a_dd(np.zeros((87,45)));offset=0
 for word in (0,1):w[word][sm]=wp[word]
 for row,count in enumerate(counts):
  for word in (0,1):normal[word][row][mask[row]]=qp[word][offset:offset+count]
  offset+=count
 for word in (0,1):t[word][sm]=qp[word][offset:]
 assert offset==14875 and len(qp[0])==18745
 q=dict(chi=P.a_slice(normal,0),W=P.a_slice(normal,slice(1,None)),t=t)
 for name,a in (('mechanical',v),('phase',w),('normal_configuration',normal),('trace_configuration',t)):coupled_pair(label+'_'+name,a,a[0].shape)
 return v,w,q


def coupled_pack_rows(mechanical,phase,normal,CMC,keep,label):
 shapes=dict(mechanical=(403340,),phase=(87,45),normal=(4,87,45),CMC=(87,45));values=dict(mechanical=mechanical,phase=phase,normal=normal,CMC=CMC);mask=N.normal_test_mask();sm=P.scalar_mask()
 for n,a in values.items():coupled_pair(label+'_'+n,a,shapes[n])
 assert all(np.all(a[~sm]==0) for pair in (phase,CMC) for a in pair) and all(np.all(a[~mask]==0) for a in normal)
 return coupled_pair(label+'_original_packed_rows',tuple(np.concatenate((mechanical[word],phase[word][sm],normal[word][mask],CMC[word][sm])) for word in (0,1)),(425955,))
