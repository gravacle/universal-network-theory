"""HELD exact-Fraction measurement of NEW paired local-factor applications.
Globals np,P,Fraction,mh_pair,ml_rational,ml_decode,ml_matrix_words.
No original action or inverse certificate is invoked. All measurements are
construction contacts for the supplied RHS only, with original2e-11 gates.
"""
MODAL_MEASURE_AUTHOR_DRAFT=True
MODAL_MEASURE_AUTHORING_IN_PROGRESS=False

def ap_vector(x):return [Fraction.from_float(float(a))+Fraction.from_float(float(b)) for a,b in zip(*x)]

def ap_matrix(x):return [ap_vector((a,b)) for a,b in zip(*x)]

def ap_mv(A,x):return [sum((a*b for a,b in zip(row,x)),Fraction(0)) for row in A]

def ap_fraction_contact(actual,target,envelope,keep,describe,check,label):
 assert actual[0].shape==actual[1].shape==(4,105) and len(target)==len(envelope)==4
 mh_pair(label+'_actual',actual,(4,105),keep);expected=(np.zeros((4,105)),np.zeros((4,105)));ratios=np.zeros((4,105));bounds=np.zeros((4,105));entries=[];tol=Fraction.from_float(2e-11)
 for point in range(4):
  assert len(target[point])==len(envelope[point])==105
  for slot,(t,e) in enumerate(zip(target[point],envelope[point])):
   assert e>=0;describe(label+'_current_exact_target',dict(point=point,slot=slot,target=ml_rational(t),envelope=ml_rational(e)))
   hi=float(t);lo=float(t-Fraction.from_float(hi));expected[0][point,slot]=hi;expected[1][point,slot]=lo
   a=Fraction.from_float(float(actual[0][point,slot]))+Fraction.from_float(float(actual[1][point,slot]));gap=a-t;ratio=abs(gap)/e if e else Fraction(0)
   entry=dict(point=point,slot=slot,target=ml_rational(t),target_pair_remainder=ml_rational(t-Fraction.from_float(hi)-Fraction.from_float(lo)),exact_difference=ml_rational(gap),uncancelled_envelope=ml_rational(e),exact_dimensionless_ratio=ml_rational(ratio));entries.append(entry);describe(label+'_completed_exact_contacts_partial',entries.copy())
   x=float(ratio);eb=float(e)
   if Fraction.from_float(x)<ratio:x=float(np.nextafter(x,np.inf))
   if Fraction.from_float(eb)<e:eb=float(np.nextafter(eb,np.inf))
   ratios[point,slot]=x;bounds[point,slot]=eb;keep(label+'_expected_both_words_partial',np.stack(expected).copy());keep(label+'_ratio_upper_partial',ratios.copy());keep(label+'_envelope_upper_partial',bounds.copy())
   assert all(np.isfinite(v) for v in (hi,lo,x,eb))
   if e==0:assert t==0 and gap==0 and actual[0][point,slot]==actual[1][point,slot]==0
 mh_pair(label+'_expected',expected,(4,105),keep);mh_pair(label+'_actual_minus_converted_target',P.a_sub(actual,expected),(4,105),keep)
 check(label+'_full_component_construction',ratios,np.zeros_like(ratios),np.ones_like(ratios));assert all(ml_decode(r['exact_dimensionless_ratio'])<=tol for r in entries)
 return dict(maximum_dimensionless_ratio_upper=float(np.max(ratios)),all420_components_checked=True,exact_target_and_conversion_remainders_retained=True,forward_solution_error_bound_or_physical_gate=False)

def ap_represented_factor_reference(factors,rhs,describe,label):
 targets=[];envelopes=[];records=[]
 for point in range(4):
  native=ap_vector(tuple(a[point] for a in rhs['native']));metric=ap_vector(tuple(a[point] for a in rhs['metric']));head_rhs=native[:3]+metric;arm_rhs=[native[3+3*j:6+3*j] for j in range(32)]
  reduced=head_rhs.copy();e_reduced=[abs(x) for x in head_rhs];record=dict(point=point,free_arms=[],solved_arms=[]);records.append(record);describe(label+'_completed_rational_points',records)
  for mode in range(32):
   DI=ap_matrix(tuple(a[mode,point] for a in factors['D_inverse']));B=ap_matrix(tuple(a[mode,point] for a in factors['B']));free=ap_mv(DI,arm_rhs[mode]);e_free=ap_mv([[abs(x) for x in row] for row in DI],[abs(x) for x in arm_rhs[mode]])
   reaction=ap_mv(B,free);e_reaction=ap_mv([[abs(x) for x in row] for row in B],e_free);reduced=[a-b for a,b in zip(reduced,reaction)];e_reduced=[a+b for a,b in zip(e_reduced,e_reaction)]
   record['free_arms'].append(dict(mode=mode,free=[ml_rational(x) for x in free],free_envelope=[ml_rational(x) for x in e_free],head_reaction=[ml_rational(x) for x in reaction],reduced_head_partial=[ml_rational(x) for x in reduced],reduced_head_envelope_partial=[ml_rational(x) for x in e_reduced]));describe(label+'_completed_rational_points',records)
  J=ap_matrix(tuple(a[point] for a in factors['S9_inverse']));head=ap_mv(J,reduced);e_head=ap_mv([[abs(x) for x in row] for row in J],e_reduced);record['head']=[ml_rational(x) for x in head];record['head_envelope']=[ml_rational(x) for x in e_head];describe(label+'_completed_rational_points',records);arms=[];e_arms=[]
  for mode in range(32):
   DI=ap_matrix(tuple(a[mode,point] for a in factors['D_inverse']));E=ap_matrix(tuple(a[mode,point] for a in factors['E']));reaction=ap_mv(E,head);corrected=[a-b for a,b in zip(arm_rhs[mode],reaction)];arm=ap_mv(DI,corrected)
   e_reaction=ap_mv([[abs(x) for x in row] for row in E],e_head);e_corrected=[abs(a)+b for a,b in zip(arm_rhs[mode],e_reaction)];e_arm=ap_mv([[abs(x) for x in row] for row in DI],e_corrected);arms.append(arm);e_arms.append(e_arm)
   record['solved_arms'].append(dict(mode=mode,corrected_rhs=[ml_rational(x) for x in corrected],solution=[ml_rational(x) for x in arm],envelope=[ml_rational(x) for x in e_arm]));describe(label+'_completed_rational_points',records)
  targets.append(head[:3]+[x for arm in arms for x in arm]+head[3:]);envelopes.append(e_head[:3]+[x for arm in e_arms for x in arm]+e_head[3:])
 return targets,envelopes

def ap_measured_real_residual(blocks,rhs,actual,describe,label):
 values=[];envelopes=[];records=[]
 for point in range(4):
  x=ap_vector(tuple(a[point] for a in actual));xh=x[:3]+x[99:];xa=[x[3+3*j:6+3*j] for j in range(32)];native=ap_vector(tuple(a[point] for a in rhs['native']));metric=ap_vector(tuple(a[point] for a in rhs['metric']));rh=native[:3]+metric;ra=[native[3+3*j:6+3*j] for j in range(32)]
  H=blocks[point]['H'];head=ap_mv(H,xh);eh=ap_mv([[abs(x) for x in row] for row in H],[abs(x) for x in xh]);arm_values=[];arm_envelopes=[];record=dict(point=point,arms=[]);records.append(record)
  for mode,arm in enumerate(blocks[point]['arms']):
   B,E,D=arm['B'],arm['E'],arm['D'];bh=ap_mv(B,xa[mode]);ebh=ap_mv([[abs(x) for x in row] for row in B],[abs(x) for x in xa[mode]]);head=[a+b for a,b in zip(head,bh)];eh=[a+b for a,b in zip(eh,ebh)]
   ex=ap_mv(E,xh);dx=ap_mv(D,xa[mode]);r=[a+b-c for a,b,c in zip(ex,dx,ra[mode])];er=[a+b+abs(c) for a,b,c in zip(ap_mv([[abs(x) for x in row] for row in E],[abs(x) for x in xh]),ap_mv([[abs(x) for x in row] for row in D],[abs(x) for x in xa[mode]]),ra[mode])]
   arm_values.append(r);arm_envelopes.append(er);record['arms'].append(dict(mode=mode,residual=[ml_rational(x) for x in r],envelope=[ml_rational(x) for x in er],head_partial=[ml_rational(x) for x in head],head_envelope_partial=[ml_rational(x) for x in eh]));describe(label+'_completed_measured_real_residual_points',records)
  hr=[a-b for a,b in zip(head,rh)];he=[a+abs(b) for a,b in zip(eh,rh)];values.append(hr[:3]+[x for arm in arm_values for x in arm]+hr[3:]);envelopes.append(he[:3]+[x for arm in arm_envelopes for x in arm]+he[3:])
 return values,envelopes

def measure_modal_head_application(factors,blocks,rhs,actual,expected_direction,keep,describe,check,label):
 physical=P.a_stack([P.a_slice(actual['native'],(slice(None),i)) for i in range(99)]+[P.a_slice(actual['metric'],(slice(None),i)) for i in range(6)],-1);mh_pair(label+'_physical_rate_all105',physical,(4,105),keep)
 expected=P.a_stack([P.a_slice(expected_direction['native'],(slice(None),i)) for i in range(99)]+[P.a_slice(expected_direction['metric'],(slice(None),i)) for i in range(6)],-1);mh_pair(label+'_known_direction_all105',expected,(4,105),keep)
 target,e_apply=ap_represented_factor_reference(factors,rhs,describe,label+'_independent_represented_factor');arithmetic=ap_fraction_contact(physical,target,e_apply,keep,describe,check,label+'_represented_factor_arithmetic')
 residual,e_residual=ap_measured_real_residual(blocks,rhs,physical,describe,label+'_authoritative_measured_real');residual_words=(np.zeros((4,105)),np.zeros((4,105)));rems=[]
 for point,row in enumerate(residual):
  for slot,value in enumerate(row):
   describe(label+'_current_exact_measured_real_residual',dict(point=point,slot=slot,value=ml_rational(value)));hi=float(value);lo=float(value-Fraction.from_float(hi));residual_words[0][point,slot]=hi;residual_words[1][point,slot]=lo
   rems.append(dict(point=point,slot=slot,remainder=ml_rational(value-Fraction.from_float(hi)-Fraction.from_float(lo))));describe(label+'_completed_residual_pair_remainders',rems.copy());keep(label+'_measured_real_residual_both_words_partial',np.stack(residual_words).copy());assert np.isfinite(hi) and np.isfinite(lo)
 # The gate owns the exact residual, rather than its converted pair: use the
 # difference from zero as an exact target against an exactly zero actual pair.
 zero=(np.zeros((4,105)),np.zeros((4,105)));real_residual=ap_fraction_contact(zero,residual,e_residual,keep,describe,check,label+'_measured_real_full_block_residual')
 direction=[ap_vector(tuple(a[point] for a in expected)) for point in range(4)];e_direction=[[abs(x)+e for x,e in zip(row,bound)] for row,bound in zip(direction,e_apply)]
 direction_contact=ap_fraction_contact(physical,direction,e_direction,keep,describe,check,label+'_known_direction_construction')
 return dict(arithmetic=arithmetic,measured_real_residual=real_residual,known_direction_construction=direction_contact,original_forward_action_at_recovered_direction_evaluated=False,these_RHS_only=True,uniform_all_input_DD_or_global_inverse_qualified=False,physical_adoption=False)
