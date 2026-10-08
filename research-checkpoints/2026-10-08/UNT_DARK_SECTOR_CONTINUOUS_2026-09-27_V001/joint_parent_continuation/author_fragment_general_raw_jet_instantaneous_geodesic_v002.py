"""HELD model313 general raw-jet event readout; definitions only.
Globals np, math, Fraction. Root owns binding, selected-word loading and execution.
Exact rational reference contractions preserve both input words and all four jets.
This is instantaneous radial balance, not an exact-axisymmetry or orbit admission.
"""
GENERAL_RAW_GEODESIC_AUTHOR_DRAFT=True
GENERAL_RAW_GEODESIC_AUTHORING_IN_PROGRESS=False
GENERAL_RAW_GEODESIC_EVENT_SOURCE=(None,None)
GENERAL_RAW_GEODESIC_EVENT_RESULT=(None,None,None)
GENERAL_RAW_GEODESIC_EVENT_RECEIPT=(None,None,None)
GENERAL_RAW_GEODESIC_EVENT_PROOF=(None,None,None)
GENERAL_RAW_GEODESIC_INTERVAL_SOURCE=(None,None)
GENERAL_RAW_GEODESIC_INTERVAL_PROOF=(None,None,None)
GENERAL_RAW_GEODESIC_SOURCE_PINS={
 'cross_u_full_metric_geodesic_and_rotating_material_v001.py':'53bc39888adeff33fffb13e04182fc9ee23d93233b15e0c533d02e24345137aa',
 'author_fragment_full_dynamic_metric_circle_v002.py':'3be37b2181ff154067ccd0d01587266ce64a58a118bd6dbd331fca1f49001c6b',
 'author_fragment_model_metric_si_circle_readout_v002.py':'245685583f389bb7b8379fc27b8ea31301b3c26f4aa63032f3d8959822fecdd8',
 'author_fragment_direct_TOTAL43_finite_event_v001.py':'9458f530b2d15beb9138d806749a42ef1192df9215292a3b39280b63d7f50e59',
 'author_fragment_conformal_DIRECT43_uncertainty_primitives_v002.py':'138c24243842734bddcfb0c83c3f2ca79202a4dafbab57ed3a9a976b57cc03e6'}
GENERAL_RAW_GEODESIC_ROOT_BITS=128

def grg_pair(x,shape,word_leaves,keep,label):
 assert isinstance(x,tuple) and len(x)==2
 for w,a in zip(('hi','lo'),x):
  keep(label+'_'+w,a.copy());assert a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a))
 keep(label+'_both_words',np.stack(x).copy())
 assert all(np.array_equal(a,a.swapaxes(-1,-2)) for a in x),'Supplied symmetry; no repair'
 words=[(Fraction.from_float(float(a)),Fraction.from_float(float(b))) for a,b in zip(x[0].flat,x[1].flat)]
 def build(dims,offset,leaves):
  if not dims:
   assert isinstance(leaves,(tuple,list)) and len(leaves)==2 and all(isinstance(v,Fraction) for v in leaves) and tuple(leaves)==words[offset]
   return sum(words[offset],Fraction(0)),offset+1
  assert isinstance(leaves,(tuple,list)) and len(leaves)==dims[0]
  rows=[]
  for source in leaves:row,offset=build(dims[1:],offset,source);rows.append(row)
  return rows,offset
 result,end=build(shape,0,word_leaves);assert end==len(words);return result

def grg_interval_event(g,dg,bounds,orientation,complete,label):
 # All interval operations below are exact rational endpoint operations.
 F=Fraction;bits=GENERAL_RAW_GEODESIC_ROOT_BITS;unit=1<<bits
 def point(x):return (x,x)
 def add(a,b):return (a[0]+b[0],a[1]+b[1])
 def neg(a):return (-a[1],-a[0])
 def sub(a,b):return add(a,neg(b))
 def mul(a,b):
  q=[x*y for x in a for y in b];return (min(q),max(q))
 def div(a,b):
  assert b[1]<0 or b[0]>0,'Unresolved interval denominator';return mul(a,(1/b[1],1/b[0]))
 def square(a):return (F(0) if a[0]<=0<=a[1] else min(x*x for x in a),max(x*x for x in a))
 def root(a):
  assert a[0]>=0
  def endpoint(x,upper):
   k=math.isqrt((x.numerator<<(2*bits))//x.denominator)
   exact=k*k*x.denominator==x.numerator*unit*unit
   return F(k+int(upper and not exact),unit)
  return (endpoint(a[0],False),endpoint(a[1],True))
 def total(q):
  out=point(F(0))
  for x in q:out=add(out,x)
  return out
 def determinant(a):
  if len(a)==1:return a[0][0]
  terms=[]
  for j in range(len(a)):
   minor=[[row[k] for k in range(len(a)) if k!=j] for row in a[1:]]
   term=mul(a[0][j],determinant(minor));terms.append(term if j%2==0 else neg(term))
  return total(terms)
 def inverse(a,d):
  rows=[]
  for i in range(4):
   row=[]
   for j in range(4):
    minor=[[a[r][c] for c in range(4) if c!=i] for r in range(4) if r!=j]
    co=determinant(minor);row.append(div(co if (i+j)%2==0 else neg(co),d))
   rows.append(row)
  return rows
 def checked(a,c,shape):
  if not shape:
   assert isinstance(a,tuple) and len(a)==2 and all(isinstance(v,F) for v in a) and a[0]<=c<=a[1]
   return a
  assert isinstance(a,(list,tuple)) and len(a)==shape[0] and len(c)==shape[0]
  return [checked(x,y,shape[1:]) for x,y in zip(a,c)]
 G=checked(bounds['g'],g,(4,4));D=checked(bounds['dg'],dg,(4,4,4))
 assert all(G[i][j]==G[j][i] for i in range(4) for j in range(4))
 assert all(D[a][i][j]==D[a][j][i] for a in range(4) for i in range(4) for j in range(4))
 G0=[[point(v) for v in row] for row in g];det=determinant(G);det0=determinant(G0)
 leading=[determinant([row[1:1+k] for row in G[1:1+k]]) for k in (1,2,3)]
 domains=dict(spatial_leading_minors=leading,spacetime_determinant=det,spatial_SPD_enclosed=all(v[0]>0 for v in leading),Lorentz_signature_enclosed=all(v[0]>0 for v in leading) and det[1]<0)
 complete(label+'_INPUT_INTERVAL_DOMAINS',dict(g=g,dg=dg,bounds=bounds,domains=domains))
 if not domains['Lorentz_signature_enclosed'] or det0[0]==0:
  return dict(status='UNRESOLVED_METRIC_DOMAIN',domains=domains,candidates=[],selected_index=None)
 I=inverse(G,det);I0=inverse(G0,det0)
 assert all(sum(g[i][k]*I0[k][j][0] for k in range(4))==int(i==j) for i in range(4) for j in range(4))
 domains['timelike_time_gradient_enclosed']=I[0][0][1]<0
 if not domains['timelike_time_gradient_enclosed']:
  complete(label+'_INVERSE_REFUSAL',dict(inverse=I,represented_inverse=I0,domains=domains))
  return dict(status='UNRESOLVED_TIME_GRADIENT',domains=domains,candidates=[],selected_index=None)
 def connection(M,J):
  return [[[mul(point(F(1,2)),total([mul(M[a][l],sub(add(J[m][l][n],J[n][l][m]),J[l][m][n])) for l in range(4)])) for n in range(4)] for m in range(4)] for a in range(4)]
 Gamma=connection(I,D);Gamma0=connection(I0,[[[point(v) for v in row] for row in slab] for slab in dg])
 coeff=[Gamma[1][0][0],add(Gamma[1][0][3],Gamma[1][3][0]),Gamma[1][3][3]]
 coeff0=[Gamma0[1][0][0],add(Gamma0[1][0][3],Gamma0[1][3][0]),Gamma0[1][3][3]]
 complete(label+'_INVERSE_AND_CONNECTION',dict(inverse=I,represented_inverse=I0,Gamma=Gamma,represented_Gamma=Gamma0,radial_coefficients=coeff,represented_radial_coefficients=coeff0,domains=domains))
 def roots(q):
  c,b,a=q
  if a==(F(0),F(0)):
   if b[0]>0 or b[1]<0:return dict(kind='LINEAR_ENCLOSED',roots=[div(neg(c),b)],discriminant=None)
   if b==(F(0),F(0)) and c==(F(0),F(0)):return dict(kind='IDENTICALLY_ZERO_NO_UNIQUE_ROOT',roots=[],discriminant=None)
   if b==(F(0),F(0)) and (c[0]>0 or c[1]<0):return dict(kind='CONSTANT_NONZERO_NO_ROOT',roots=[],discriminant=None)
   return dict(kind='UNRESOLVED_LINEAR_BRANCH',roots=[],discriminant=None)
  if a[0]<=0<=a[1]:return dict(kind='UNRESOLVED_POLYNOMIAL_DEGREE',roots=[],discriminant=None)
  disc=sub(square(b),mul(point(F(4)),mul(a,c)))
  if disc[1]<0:return dict(kind='NEGATIVE_DISCRIMINANT_NO_ROOT',roots=[],discriminant=disc)
  if disc[0]<=0:return dict(kind='UNRESOLVED_DISCRIMINANT_OR_MULTIPLE_ROOT',roots=[],discriminant=disc)
  sr=root(disc);den=mul(point(F(2)),a)
  return dict(kind='TWO_REAL_ROOTS_ENCLOSED',roots=sorted([div(sub(neg(b),sr),den),div(add(neg(b),sr),den)],key=lambda v:v[0]),discriminant=disc)
 radial=roots(coeff);nominal=roots(coeff0)
 complete(label+'_RADIAL_ROOT_INTERVALS',dict(radial=radial,represented_radial=nominal))
 N=root(neg(div(point(F(1)),I[0][0])));beta=[neg(div(I[0][i],I[0][0])) for i in (1,2,3)]
 axial_length=root(G[3][3]);cpSI=F(299792458);L0=F.from_float(3.085677581491367e19);rateSI=cpSI/L0
 if N[0]<=0 or axial_length[0]<=0:
  complete(label+'_NORMAL_FRAME_REFUSAL',dict(lapse=N,axial_length=axial_length,domains=domains,radial_root_diagnostics=radial))
  return dict(status='UNRESOLVED_NORMAL_FRAME_ENDPOINTS',domains=domains,candidates=[],selected_index=None)
 rows=[]
 for index,omega in enumerate(radial['roots']):
  omega2=square(omega)
  contracted=[total([Gamma[a][0][0],mul(add(Gamma[a][0][3],Gamma[a][3][0]),omega),mul(Gamma[a][3][3],omega2)]) for a in range(4)]
  norm=total([G[0][0],mul(point(F(2)),mul(G[0][3],omega)),mul(G[3][3],omega2)])
  w=[point(F(0)),point(F(0)),omega];v=[div(add(x,b),N) for x,b in zip(w,beta)]
  v2=total([mul(G[i+1][j+1],mul(v[i],v[j])) for i in range(3) for j in range(3)])
  speed=div(total([mul(G[3][i+1],v[i]) for i in range(3)]),axial_length);speedkms=mul(speed,point(cpSI/F(1000)))
  oriented=mul(speedkms,point(F(orientation)));timelike=norm[1]<0 and v2[1]<1
  omega_dot=add(neg(contracted[3]),mul(omega,contracted[0]));clock=neg(contracted[0])
  row=dict(index=index,Omega_model=omega,Omega_SI=mul(omega,point(rateSI)),radial_acceleration=neg(contracted[1]),vertical_acceleration=neg(contracted[2]),Omega_dot_model=omega_dot,Omega_dot_SI=mul(omega_dot,point(rateSI**2)),clock_nonaffinity_model=clock,clock_nonaffinity_SI=mul(clock,point(rateSI)),Gamma_WW=contracted,gWW=norm,normal_velocity=v,normal_speed_squared=v2,normal_axial_speed_kms=speedkms,declared_orientation_speed_kms=oriented,timelike_enclosed=timelike,orientation_kind='DECLARED_ORIENTATION' if oriented[0]>0 else ('OPPOSITE_ORIENTATION' if oriented[1]<0 else 'UNRESOLVED_ORIENTATION'),source_coefficient_root_interval=True,persistent_orbit_or_stability_claimed=False,physical_or_velocity_adoption=False)
  complete(label+'_ROOT_%d_DIAGNOSTICS'%index,row);rows.append(row)
 chosen=[i for i,v in enumerate(rows) if v['timelike_enclosed'] and v['orientation_kind']=='DECLARED_ORIENTATION']
 resolved=len(chosen)==1 and all(i==chosen[0] or v['orientation_kind']=='OPPOSITE_ORIENTATION' or not v['timelike_enclosed'] and v['gWW'][0]>=0 for i,v in enumerate(rows))
 return dict(status='GENERAL_INSTANTANEOUS_RADIAL_BALANCE_INTERVALS',domains=domains,radial_root_diagnostics=radial,represented_radial_root_diagnostics=nominal,candidates=rows,selected_index=chosen[0] if resolved else None,root_branch_or_domain_refusal_retained=not radial['roots'],represented_phi_derivative_exact_zero=all(dg[3][i][j]==0 for i in range(4) for j in range(4)),model_coordinates=('t313','R_kpc','Z_kpc','phi_rad'),SI_clock_rate_factor=rateSI,SI_speed_factor_kms=cpSI/F(1000),metric_length_unit_m=L0,exact_represented_input_reference_arithmetic=True,installed_floating_kernel_accuracy_used=False,exact_axisymmetry_guard_promoted=False,instantaneous_vertical_balance_or_full_circle_admitted=False,persistent_orbit_or_stability_claimed=False,physical_or_velocity_adoption=False)

def general_raw_jet_instantaneous_geodesic(g_pair,dg_pair,*,bounds,orientation,admission,keep,label,stage_complete):
 assert not GENERAL_RAW_GEODESIC_AUTHOR_DRAFT and not GENERAL_RAW_GEODESIC_AUTHORING_IN_PROGRESS
 assert admission['source_pins']==GENERAL_RAW_GEODESIC_SOURCE_PINS and type(orientation) is int and orientation in (-1,1)
 for n,pin in (('source',GENERAL_RAW_GEODESIC_EVENT_SOURCE),('result',GENERAL_RAW_GEODESIC_EVENT_RESULT),('receipt',GENERAL_RAW_GEODESIC_EVENT_RECEIPT),('proof',GENERAL_RAW_GEODESIC_EVENT_PROOF),('interval_source',GENERAL_RAW_GEODESIC_INTERVAL_SOURCE),('interval_proof',GENERAL_RAW_GEODESIC_INTERVAL_PROOF)):
  assert all(v is not None for v in pin) and tuple(admission[n])==pin
 assert admission['naturally_closed'] is True and admission['exit_code']==0 and admission['all_selected_byte_owner_and_header_seals_verified'] is True
 assert admission['physical_metric_admitted'] is False
 assert admission['interval_event_provenance']==bounds['source_box']['provenance'] and admission['event_provenance'] and admission['input_scope'] in ('closed_direct_baseline_evidence','accepted_conditional_finite_metric','closed_measured_unqualified_changed_trial')
 assert len(admission['coordinate_event'])==4 and admission['coordinate_event'][0]==admission['coordinate_event'][2]==admission['coordinate_event'][3]==0 and math.isfinite(float(admission['coordinate_event'][1])) and admission['coordinate_event'][1]>0
 assert admission['radial_side'] in ('left','right') and admission['vertical_side'] in ('upper','lower','registered_junction')
 assert bounds['finite_input_output_enclosure'] is True and bounds['source_box']['finite_input_exact_law_enclosure'] is True and bounds['source_box']['derivative_index_first'] is True
 assert bounds['source_box']['coordinate_system']=='native313_cp_model_equals_one' and bounds['authentic_output_words']['all_output_dyadic_words_authenticated'] is bounds['authentic_output_words']['all_original_word_hex_preserved'] is True
 assert callable(keep) and callable(stage_complete)
 if admission['input_scope']=='accepted_conditional_finite_metric':
  assert admission['finite_constraint_solution_admitted'] is admission['finite_domains_admitted'] is bounds['source_box']['finite_constraint_solution_admitted'] is True and admission['finite_physical_metric_admitted'] is False
 elif admission['input_scope']=='closed_measured_unqualified_changed_trial':
  assert admission['closed_measured_trial_word_lineage_verified'] is admission['measurement_only'] is True
  assert admission['finite_constraint_solution_admitted'] is admission['finite_domains_admitted'] is bounds['source_box']['finite_constraint_solution_admitted'] is False
  assert admission['finite_physical_metric_admitted'] is admission['scientific_acceptance_used'] is False
 g=grg_pair(g_pair,(4,4),bounds['authentic_output_words']['g'],keep,label+'_raw_g');dg=grg_pair(dg_pair,(4,4,4),bounds['authentic_output_words']['dg'],keep,label+'_raw_dg');refs=[]
 def complete(stage,data):
  ref=stage_complete(stage,data);assert isinstance(ref,dict) and all(ref.get(n) for n in ('file','sha256','commit_file','commit_sha256'));refs.append(ref)
 result=grg_interval_event(g,dg,bounds,orientation,complete,label)
 result.update(completed_stage_refs=list(refs),supplied_admission=admission,supplied_interval_provenance=bounds['source_box']['provenance'],source_uncertainty_admitted=bounds['source_box']['source_uncertainty_admitted'],finite_input_source_output_hull_only=True,source_output_gaps=bounds['source_output_gaps'],raw_phi_both_words_exact_zero=all(np.all(a[3]==0) for a in dg_pair),represented_phi_derivative_exact_zero=all(dg[3][i][j]==0 for i in range(4) for j in range(4)),input_phi_or_time_words_changed=False,paired_words_collapsed_to_binary64=False,declared_orientation=orientation,orientation_selected_using_observations=False,old_circle_or_metric_producers_replayed=False,exact_axisymmetry_guard_promoted=False,instantaneous_vertical_balance_or_full_circle_admitted=False,persistent_orbit_or_stability_claimed=False,physical_or_velocity_adoption=False)
 complete(label+'_READOUT',result);result['completed_stage_refs']=list(refs);return result
