"""HELD signed directed local-real Schur certificate; definitions only.
Globals np,Fraction,mh_pair; callbacks keep/describe/check are supplied.
The containing driver must bind naturally CLOSED successful arm recovery and
its measured-matrix proof. No old producer, Pi/action, arm certificate or
eigensystem is replayed. Hex rational witnesses avoid decimal digit limits.
"""
MODAL_LOCAL_AUTHOR_DRAFT=True
MODAL_LOCAL_AUTHORING_IN_PROGRESS=True
MODAL_LOCAL_ARM_SOURCE=(None,None)
MODAL_LOCAL_ARM_RESULT=(None,None,None)
MODAL_LOCAL_ARM_RECEIPT=(None,None,None)
MODAL_LOCAL_ARM_PROOF=(None,None,None)

def ml_rational(x):return dict(numerator_hex=hex(x.numerator),denominator_hex=hex(x.denominator))

def ml_decode(x):
 n=int(x['numerator_hex'],16) if 'numerator_hex' in x else int(x['numerator']);d=int(x['denominator_hex'],16) if 'denominator_hex' in x else int(x['denominator'])
 assert d>0;return Fraction(n,d)

def ml_matrix_words(A):return [[ml_rational(x) for x in row] for row in A]

def ml_mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),Fraction(0)) for j in range(len(B[0]))] for i in range(len(A))]

def ml_abs(A):return [[abs(x) for x in row] for row in A]

def ml_inf(A):return max(sum((abs(x) for x in row),Fraction(0)) for row in A)

def ml_record_entries(record,shape,describe,label):
 describe(label+'_supplied_exact_coefficients',record);assert record['shape']==list(shape) and ml_decode(record['amplitude'])==Fraction(1)+Fraction(1,2**60)
 values={}
 for entry in record['entries']:
  index=tuple(entry['index']);assert len(index)==len(shape) and all(isinstance(i,int) and 0<=i<n for i,n in zip(index,shape)) and index not in values
  values[index]=ml_decode(entry['exact']);ml_decode(entry['pair_remainder'])
 assert len(values)==int(np.prod(shape));return values

def ml_exact_inverse(A,describe,label):
 n=len(A);assert n in (3,9) and all(len(row)==n for row in A)
 rows=[list(row)+[Fraction(int(i==j)) for j in range(n)] for i,row in enumerate(A)];pivots=[]
 describe(label+'_initial_augmented_matrix',ml_matrix_words(rows))
 for column in range(n):
  pivot=max(range(column,n),key=lambda i:abs(rows[i][column]));value=rows[pivot][column]
  pivots.append(dict(column=column,row=pivot,pivot=ml_rational(value)));describe(label+'_completed_pivots',pivots.copy());assert value!=0,'Singular measured local coefficient matrix; no jitter or identity replacement'
  rows[column],rows[pivot]=rows[pivot],rows[column];rows[column]=[x/value for x in rows[column]]
  describe(label+'_pivot%d_normalized_augmented_matrix'%column,ml_matrix_words(rows))
  for i in range(n):
   if i!=column:
    factor=rows[i][column];rows[i]=[x-factor*y for x,y in zip(rows[i],rows[column])]
    describe(label+'_pivot%d_row%d_completed_augmented_matrix'%(column,i),ml_matrix_words(rows))
 I=[row[n:] for row in rows];left=ml_mm(A,I);right=ml_mm(I,A)
 describe(label+'_exact_left_inverse_product',ml_matrix_words(left));describe(label+'_exact_right_inverse_product',ml_matrix_words(right))
 assert all(left[i][j]==right[i][j]==int(i==j) for i in range(n) for j in range(n));return I

def ml_convert_matrix(A,keep,describe,label):
 shape=(len(A),len(A[0]));words=(np.zeros(shape),np.zeros(shape));entries=[];actual=[[Fraction(0) for x in row] for row in A]
 for i,row in enumerate(A):
  for j,x in enumerate(row):
   describe(label+'_current_exact_conversion',dict(index=[i,j],exact=ml_rational(x)))
   hi=float(x);lo=float(x-Fraction.from_float(hi));words[0][i,j]=hi;words[1][i,j]=lo
   actual[i][j]=Fraction.from_float(hi)+Fraction.from_float(lo);remainder=x-actual[i][j]
   entries.append(dict(index=[i,j],exact=ml_rational(x),pair_remainder=ml_rational(remainder)));describe(label+'_completed_exact_conversions_partial',entries.copy())
   keep(label+'_converted_both_words_partial',np.stack(words).copy());assert np.isfinite(hi) and np.isfinite(lo)
 mh_pair(label+'_converted_pair',words,shape,keep);return words,actual,entries

def ml_normwise_identity(A,I,keep,describe,check,label):
 n=len(A);left=ml_mm(A,I);right=ml_mm(I,A);identity=[[Fraction(int(i==j)) for j in range(n)] for i in range(n)]
 le=[[x-y for x,y in zip(a,b)] for a,b in zip(left,identity)];re=[[x-y for x,y in zip(a,b)] for a,b in zip(right,identity)]
 el=ml_mm(ml_abs(A),ml_abs(I));er=ml_mm(ml_abs(I),ml_abs(A));el=[[x+y for x,y in zip(a,b)] for a,b in zip(el,identity)];er=[[x+y for x,y in zip(a,b)] for a,b in zip(er,identity)]
 nl,nr,dl,dr=ml_inf(le),ml_inf(re),ml_inf(el),ml_inf(er);assert dl>0 and dr>0
 ratios=(nl/dl,nr/dr);q=max(nl,nr);tol=Fraction.from_float(2e-11)
 record=dict(left_residual=ml_matrix_words(le),right_residual=ml_matrix_words(re),left_operation_envelope=ml_matrix_words(el),right_operation_envelope=ml_matrix_words(er),left_norm_ratio=ml_rational(ratios[0]),right_norm_ratio=ml_rational(ratios[1]),two_sided_inverse_Neumann_residual_inf=ml_rational(q),tol=ml_rational(tol))
 describe(label+'_exact_normwise_inverse_witness',record);upper=[]
 for ratio in ratios:
  x=float(ratio)
  if Fraction.from_float(x)<ratio:x=float(np.nextafter(x,np.inf))
  upper.append(x)
 actual=np.asarray(upper);keep(label+'_dimensionless_normwise_ratio_upper',actual.copy());assert all(r<=tol for r in ratios) and q<1
 check(label+'_two_sided_normwise_inverse',actual,np.zeros(2),np.ones(2));return record

def candidate_modal_head_local_real_certificate(reconstructed,head,arm,keep,describe,check,label):
 assert reconstructed['physical_adoption'] is False and head['physical_adoption'] is False and reconstructed['uniform_DD_operator_or_global_inverse_qualified'] is False and head['uniform_DD_operator_or_global_inverse_qualified'] is False
 describe(label+'_admitted_arm_ancestry',arm);assert isinstance(arm['closed_provenance'],dict) and arm['closed_provenance']
 admission=arm['measured_admission'];assert admission['measured_three_basis_real_coefficient_matrices_invertible'] is True and admission['same_three_input_amplitudes_only'] is True and admission['uniform_all_input_DD_error_or_global_inverse_earned'] is False and admission['physical_adoption'] is False
 B=ml_record_entries(reconstructed['B_rational'],(32,4,9,3),describe,label+'_B');H=ml_record_entries(head['H_rational'],(4,9,9),describe,label+'_H');E=ml_record_entries(head['E_rational'],(32,4,3,9),describe,label+'_E')
 coefficients=arm['coefficient_points'];measured=arm['measured_matrix_records'];assert len(coefficients)==4 and len(measured)==128
 index={}
 for r in measured:
  key=(r['point'],r['mode']);assert key not in index and key[0] in range(4) and key[1] in range(32);index[key]=r
  assert ml_decode(r['Neumann_q'])<1 and ml_decode(r['conditional_measured_real_sigma_min_lower'])>0
 Swords=(np.zeros((4,9,9)),np.zeros((4,9,9)));Iwords=(np.zeros((4,9,9)),np.zeros((4,9,9)));Dwords=(np.zeros((32,4,3,3)),np.zeros((32,4,3,3)));records=[];tol=Fraction.from_float(2e-11)
 for point,ancestry in enumerate(coefficients):
  assert ancestry['point']==point and ancestry['determinant_resolved'] is True and len(ancestry['modes'])==32 and all(r['mode']==j and r['eta_resolved'] is True for j,r in enumerate(ancestry['modes']))
  h=[[H[point,i,j] for j in range(9)] for i in range(9)];S=[row.copy() for row in h];eS=ml_abs(h);local=dict(point=point,raw_G_eta_reference_D_ancestry=ancestry,measured_arm_ancestry=[index[point,j] for j in range(32)],directed_B_E_transpose_not_assumed=True,arms=[])
  records.append(local);describe(label+'_completed_local_points',records)
  for mode in range(32):
   tag=label+'_point%d_mode%02d'%(point,mode);D=[[ml_decode(x) for x in row] for row in index[point,mode]['measured_matrix']];assert len(D)==3 and all(len(row)==3 for row in D)
   DI=ml_exact_inverse(D,describe,tag+'_D_inverse');dp,dpa,drem=ml_convert_matrix(DI,keep,describe,tag+'_D_inverse');dw=ml_normwise_identity(D,dpa,keep,describe,check,tag+'_D_pair_inverse')
   for word in (0,1):Dwords[word][mode,point]=dp[word]
   b=[[B[mode,point,i,j] for j in range(3)] for i in range(9)];e=[[E[mode,point,i,j] for j in range(9)] for i in range(3)];bd=ml_mm(b,DI);term=ml_mm(bd,e);bound=ml_mm(ml_mm(ml_abs(b),ml_abs(DI)),ml_abs(e))
   S=[[x-y for x,y in zip(a,z)] for a,z in zip(S,term)];eS=[[x+y for x,y in zip(a,z)] for a,z in zip(eS,bound)]
   local['arms'].append(dict(mode=mode,measured_D=ml_matrix_words(D),exact_D_inverse=ml_matrix_words(DI),D_inverse_pair_remainders=drem,D_pair_inverse_witness=dw,directed_B=ml_matrix_words(b),directed_E=ml_matrix_words(e),B_Dinv_E=ml_matrix_words(term),uncancelled_B_Dinv_E=ml_matrix_words(bound)))
   describe(tag+'_completed_S9_partial',ml_matrix_words(S));describe(tag+'_completed_S9_envelope_partial',ml_matrix_words(eS));describe(label+'_completed_local_points',records)
   keep(tag+'_D_inverse_all_points_partial',np.stack(Dwords).copy())
  local['S9']=ml_matrix_words(S);local['S9_uncancelled_assembly_envelope']=ml_matrix_words(eS);describe(label+'_completed_local_points',records)
  SI=ml_exact_inverse(S,describe,label+'_point%d_S9_inverse'%point);sensitivity=ml_mm(ml_abs(SI),eS);q=tol*ml_inf(sensitivity);local['assembly_tolerance_cone_q']=ml_rational(q);local['exact_S9_inverse_inf_norm']=ml_rational(ml_inf(SI));local['assembly_cone_resolved']=q<1
  describe(label+'_completed_local_points',records);assert q<1,'Local measured-real Schur is unresolved at original2e-11 assembly cone; no jitter'
  sp,spa,srem=ml_convert_matrix(S,keep,describe,label+'_point%d_S9'%point);ip,ipa,irem=ml_convert_matrix(SI,keep,describe,label+'_point%d_S9_inverse'%point)
  witness=ml_normwise_identity(S,ipa,keep,describe,check,label+'_point%d_S9_pair_inverse'%point)
  for word in (0,1):Swords[word][point]=sp[word];Iwords[word][point]=ip[word]
  local.update(exact_S9_inverse=ml_matrix_words(SI),S9_pair_remainders=srem,S9_inverse_pair_remainders=irem,S9_pair_inverse_witness=witness,local_real_coefficient_Schur_inverse_certified=True)
  describe(label+'_completed_local_points',records);mh_pair(label+'_S9_all_points_partial',Swords,(4,9,9),keep);mh_pair(label+'_S9_inverse_all_points_partial',Iwords,(4,9,9),keep)
 mh_pair(label+'_measured_D_inverse',Dwords,(32,4,3,3),keep)
 return dict(S9=Swords,S9_inverse=Iwords,D_inverse=Dwords,rational_local_points=records,all_four_local_measured_real_coefficient_Schur_inverses_certified=True,source_raw_G_eta_reference_D_retained=True,directed_crossblocks_transpose_not_assumed=True,uniform_all_input_DD_inverse_qualified=False,full_weak_or_global_inverse_qualified=False,physical_rank_or_adoption=False)
