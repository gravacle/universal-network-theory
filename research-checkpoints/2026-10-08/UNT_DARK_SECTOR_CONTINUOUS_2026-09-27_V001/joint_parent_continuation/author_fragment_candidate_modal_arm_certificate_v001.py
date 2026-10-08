"""HELD independent exact-rational modal arm certificate on raw coefficients.
Globals np,P,Fraction,itertools,ft_keep and describe(name,JSON), keep(name,array).
No candidate producer, specialization, inverse solver or numerical invocation
occurs on import. Positive coefficients do not imply invertibility: all eta
and the actual nonsymmetric common G must pass separate resolved checks.
"""
MODAL_ARM_AUTHOR_DRAFT=True
MODAL_ARM_AUTHORING_IN_PROGRESS=False

def arm_rational(x):return dict(numerator=str(x.numerator),denominator=str(x.denominator))
def arm_matrix_words(A):return [[arm_rational(x) for x in row] for row in A]
def arm_fraction_mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def arm_fraction_transpose(A):return [list(row) for row in zip(*A)]
def arm_fraction_pair(x):
 hi=float(x);assert np.isfinite(hi);lo=float(x-Fraction.from_float(hi));assert np.isfinite(lo)
 return hi,lo,arm_rational(x-Fraction.from_float(hi)-Fraction.from_float(lo))
def arm_fraction_upper(x):
 value=float(x);assert np.isfinite(value) and x>=0
 if Fraction.from_float(value)<x:value=float(np.nextafter(value,np.inf))
 assert np.isfinite(value);return value

def candidate_modal_arm_certificate(cache,keep,describe,label):
 s,c,p=cache['s'],cache['c'],cache['p'];assert p==4 and np.array_equal(s['hi'],s['hi'].swapaxes(-1,-2))
 assert np.all(s['w']>0) and np.all(c['dens']>0);F=lambda x:Fraction.from_float(float(x));tol=F(2e-11)
 omega_squared=s['omega']**2;ell_squared=float(P.ELL**2);assert np.all(np.isfinite(omega_squared)) and np.all(omega_squared>0)
 keep(label+'_raw_omega_squared_denominator',omega_squared.copy());keep(label+'_raw_ELL_squared_coefficient',np.asarray(ell_squared))
 describe(label+'_squared_constant_rounding',dict(omega=[arm_rational(F(x)*F(x)-F(y)) for x,y in zip(s['omega'],omega_squared)],ELL=arm_rational(F(P.ELL)**2-F(ell_squared))))
 records=[];exact=[]
 for point in range(p):
  H=[[F(x) for x in row] for row in s['hi'][point]];proj=[[F(x) for x in row] for row in s['P'][point]]
  C=[[F(x) for x in c['Jzz'][point]]]+[[Fraction(int(i==j)) for j in range(3)] for i in range(3)]
  L=[[F(c['beta'][point,j])-F(c['N'][point])*F(c['up'][point,j])/F(c['gamma'][point]) for j in range(3)]]+[[Fraction(int(i==j)) for j in range(3)] for i in range(3)]
  G=arm_fraction_mm(arm_fraction_mm(arm_fraction_mm(arm_fraction_transpose(C),H),proj),L)
  eG=arm_fraction_mm(arm_fraction_mm(arm_fraction_mm(arm_fraction_transpose([[abs(x) for x in row] for row in C]),[[abs(x) for x in row] for row in H]),[[abs(x) for x in row] for row in proj]),[[abs(x) for x in row] for row in L])
  r0=sum(H[0][k]*proj[k][0] for k in range(4));er0=sum(abs(H[0][k]*proj[k][0]) for k in range(4));signed=[];unsigned=[]
  for perm in itertools.permutations(range(3)):
   value=G[0][perm[0]]*G[1][perm[1]]*G[2][perm[2]];parity=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
   signed.append(-value if parity%2 else value);unsigned.append(abs(value))
  determinant=sum(signed);edeterminant=sum(unsigned)
  record=dict(point=point,C=arm_matrix_words(C),L=arm_matrix_words(L),C_minus_L=arm_matrix_words([[x-y for x,y in zip(a,b)] for a,b in zip(C,L)]),G=arm_matrix_words(G),G_skew=arm_matrix_words([[G[i][j]-G[j][i] for j in range(3)] for i in range(3)]),r0=arm_rational(r0),determinant=arm_rational(determinant),determinant_envelope=arm_rational(edeterminant),determinant_resolved=edeterminant>0 and abs(determinant)>tol*edeterminant,modes=[])
  et=[]
  for mode in range(32):
   kinetic=F(s['U'][point,0])**2/F(omega_squared[mode]);gradient=F(ell_squared)*r0;eta=kinetic-gradient;eeta=abs(kinetic)+F(ell_squared)*er0
   scale=F(c['dens'][point])*F(s['w'][mode]);record['modes'].append(dict(mode=mode,eta=arm_rational(eta),eta_envelope=arm_rational(eeta),eta_resolved=eeta>0 and abs(eta)>tol*eeta,density_weight_scale=arm_rational(scale)));et.append((eta,eeta,scale))
  records.append(record);exact.append((G,eG,determinant,edeterminant,et));describe(label+'_completed_rational_points',records)
 assert len(records)==4 and all(r['determinant_resolved'] and all(m['eta_resolved'] for m in r['modes']) for r in records),'Actual G/eta unresolved; all four G and 128 eta retained, no jitter or identity replacement'
 D=P.a_dd(np.zeros((32,p,3,3)));eD=np.zeros_like(D[0]);Gwords=P.a_dd(np.zeros((p,3,3)));Ginverse=P.a_dd(np.zeros((p,3,3)));etas=P.a_dd(np.zeros((32,p)));eta_bounds=np.zeros((32,p));eta_margin=np.zeros((32,p));det=P.a_dd(np.zeros(p));det_bounds=np.zeros(p);det_margin=np.zeros(p);inverse_identity=np.zeros((p,3,3))
 for point,(G,eG,determinant,edeterminant,et) in enumerate(exact):
  record=records[point];inverse=[]
  for i in range(3):
   row=[]
   for j in range(3):
    rows=[k for k in range(3) if k!=j];cols=[k for k in range(3) if k!=i]
    cofactor=G[rows[0]][cols[0]]*G[rows[1]][cols[1]]-G[rows[0]][cols[1]]*G[rows[1]][cols[0]];row.append(((-1)**(i+j))*cofactor/determinant)
   inverse.append(row)
  product=arm_fraction_mm(G,inverse);record['exact_G_inverse']=arm_matrix_words(inverse);record['exact_G_inverse_product']=arm_matrix_words(product);describe(label+'_completed_rational_points',records)
  assert all(product[i][j]==int(i==j) for i in range(3) for j in range(3))
  inverse_norm=max(sum(abs(x) for x in row) for row in inverse);record['inverse_inf_norm']=arm_rational(inverse_norm);record['real_sigma_min_lower']=arm_rational(1/(3*inverse_norm));record['G_pair_remainders']=[];record['G_inverse_pair_remainders']=[]
  for i in range(3):
   grems=[];irems=[]
   for j in range(3):
    Gwords[0][point,i,j],Gwords[1][point,i,j],gr=arm_fraction_pair(G[i][j]);Ginverse[0][point,i,j],Ginverse[1][point,i,j],ir=arm_fraction_pair(inverse[i][j]);grems.append(gr);irems.append(ir);inverse_identity[point,i,j]=float(product[i][j])
   record['G_pair_remainders'].append(grems);record['G_inverse_pair_remainders'].append(irems)
  det[0][point],det[1][point],record['determinant_pair_remainder']=arm_fraction_pair(determinant);det_bounds[point]=arm_fraction_upper(edeterminant);det_margin[point]=float(abs(determinant)/edeterminant-tol)
  for mode,(eta,eeta,scale) in enumerate(et):
   scalar=record['modes'][mode];etas[0][mode,point],etas[1][mode,point],scalar['pair_remainder']=arm_fraction_pair(eta);eta_bounds[mode,point]=arm_fraction_upper(eeta);eta_margin[mode,point]=float(abs(eta)/eeta-tol);converted=[]
   for i in range(3):
    row=[]
    for j in range(3):
     value=scale*eta*G[i][j];D[0][mode,point,i,j],D[1][mode,point,i,j],remainder=arm_fraction_pair(value);eD[mode,point,i,j]=arm_fraction_upper(scale*eeta*eG[i][j]);row.append(dict(exact=arm_rational(value),pair_remainder=remainder))
    converted.append(row)
   scalar['arm_columns']=converted
  for n,x in (('G',Gwords),('G_inverse',Ginverse),('eta',etas),('G_determinant',det),('independent_arm_matrix',D)):ft_keep(label+'_'+n,x,keep)
  for n,x in (('eta_uncancelled_envelope',eta_bounds),('eta_resolution_margin',eta_margin),('determinant_uncancelled_envelope',det_bounds),('determinant_resolution_margin',det_margin),('arm_uncancelled_envelope',eD),('exact_inverse_product',inverse_identity)):keep(label+'_'+n,x)
  describe(label+'_completed_rational_points',records)
 return dict(expected=D,envelope=eD,inverse_identity=inverse_identity,rational_points=records,real_raw_coefficient_point_arm_invertibility_qualified=True,rounded_DD_arm_implementation_invertibility_qualified=False,point_or_global_Schur_inverse_earned=False,physical_adoption=False)

def candidate_modal_basis_argument(coordinate,p,keep,label):
 assert coordinate in (0,1,2) and p==4;native=P.a_dd(np.zeros((p,99)));metric=P.a_dd(np.zeros((p,6)))
 for mode in range(32):native[0][:,3+3*mode+coordinate]=1.;native[1][:,3+3*mode+coordinate]=2.**-60
 ft_keep(label+'_native',native,keep);ft_keep(label+'_metric',metric,keep)
 return dict(native=native,metric=metric)

def candidate_modal_arm_compare(certificate,result,coordinate,keep,describe,label,check):
 actual=tuple(a[:,3:].reshape(4,32,3).transpose(1,0,2) for a in result['point']['native']);target=P.a_dd(np.zeros_like(actual[0]));bound=np.zeros_like(actual[0]);F=lambda x:Fraction.from_float(float(x));factor=Fraction(1)+Fraction(1,2**60);words=[]
 for point,record in enumerate(certificate['rational_points']):
  for mode,item in enumerate(record['modes']):
   row=[]
   for component in range(3):
    entry=item['arm_columns'][component][coordinate]['exact'];value=Fraction(int(entry['numerator']),int(entry['denominator']))*factor
    target[0][mode,point,component],target[1][mode,point,component],remainder=arm_fraction_pair(value);row.append(dict(exact=arm_rational(value),pair_remainder=remainder))
    bound[mode,point,component]=arm_fraction_upper(2*F(certificate['envelope'][mode,point,component,coordinate])*factor)
   words.append(dict(point=point,mode=mode,target_entries=row))
 describe(label+'_exact_scaled_targets',words);ft_keep(label+'_actual_modal_outputs',actual,keep);ft_keep(label+'_independent_expected',target,keep);gap=ft_keep(label+'_difference',P.a_sub(actual,target),keep);keep(label+'_uncancelled_envelope',bound)
 check(label+'_independent_modal_column',gap[0]+gap[1],np.zeros_like(gap[0]),bound)
 return dict(all32_simultaneous_modal_axes_separated_by_proven_source_structure=True,coordinate=coordinate,shared_native_and_metric_head_outputs_retained=True,head_or_global_inverse_qualified=False,physical_adoption=False)

def candidate_modal_measured_matrix_bound(certificate,results,keep,describe,label):
 decode=lambda x:Fraction(int(x['numerator']),int(x['denominator']));factor=Fraction(1)+Fraction(1,2**60);F=lambda x:Fraction.from_float(float(x));records=[];qvalues=np.zeros((32,4));lowers=np.zeros((32,4))
 for point,record in enumerate(certificate['rational_points']):
  inverse_norm=decode(record['inverse_inf_norm'])
  for mode,item in enumerate(record['modes']):
   expected=[[decode(item['arm_columns'][i][j]['exact']) for j in range(3)] for i in range(3)]
   measured=[[sum(F(results[j]['point']['native'][word][point,3+3*mode+i]) for word in (0,1))/factor for j in range(3)] for i in range(3)]
   difference=[[x-y for x,y in zip(a,b)] for a,b in zip(measured,expected)];delta=max(sum(abs(x) for x in row) for row in difference)
   b=inverse_norm/abs(decode(item['density_weight_scale'])*decode(item['eta']));q=b*delta
   entry=dict(point=point,mode=mode,measured_matrix=arm_matrix_words(measured),measured_minus_exact_raw_polynomial=arm_matrix_words(difference),perturbation_inf_norm=arm_rational(delta),reference_inverse_inf_norm=arm_rational(b),Neumann_q=arm_rational(q))
   records.append(entry);describe(label+'_completed_measured_matrix_bounds',records)
   assert q<1,'Observed modal basis coefficient matrix did not earn perturbation invertibility'
   lower=(1-q)/(3*b);entry['conditional_measured_real_sigma_min_lower']=arm_rational(lower);qvalues[mode,point]=arm_fraction_upper(q)
   value=float(lower)
   if Fraction.from_float(value)>lower:value=float(np.nextafter(value,-np.inf))
   assert np.isfinite(value) and value>0;lowers[mode,point]=value
 keep(label+'_Neumann_q_upper',qvalues);keep(label+'_measured_real_sigma_min_lower',lowers);describe(label+'_completed_measured_matrix_bounds',records)
 return dict(measured_three_basis_real_coefficient_matrices_invertible=True,same_three_input_amplitudes_only=True,uniform_all_input_DD_error_or_global_inverse_earned=False,physical_adoption=False)
