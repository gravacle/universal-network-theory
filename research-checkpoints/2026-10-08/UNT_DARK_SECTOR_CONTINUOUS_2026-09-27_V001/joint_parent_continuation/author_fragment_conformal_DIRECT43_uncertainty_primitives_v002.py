"""HELD exact-rational finite-input conformal event enclosure; no arrays/libm/IO.
Source law is DIRECT103 -> finite132 ADM, with every gauge time/phi jet kept.
Globals Fraction,isqrt,json are installed from stdlib by a reviewed caller.
All nested tensor leaves are rational endpoint pairs or high/low dyadic words.
"""
CONFORMAL_UNCERTAINTY_AUTHOR_DRAFT=True
CONFORMAL_UNCERTAINTY_AUTHORING_IN_PROGRESS=False
CONFORMAL_UNCERTAINTY_TERMINALS={n:(None,None,None,None) for n in ('direct_baseline','finite_trial','coupled_correction','selected_inputs')}
CONFORMAL_UNCERTAINTY_SOURCE_PINS={
 'author_fragment_direct_TOTAL43_finite_event_v001.py':'9458f530b2d15beb9138d806749a42ef1192df9215292a3b39280b63d7f50e59',
 'author_fragment_finite_conformal_circle_event_v001.py':'b607fcf3346d83e012771e75d9b658cef9ad51aeac4de09ad0a69bb3d75489b1',
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_model_metric_si_circle_readout_v002.py':'245685583f389bb7b8379fc27b8ea31301b3c26f4aa63032f3d8959822fecdd8'}


def cui_interval(x):
 assert isinstance(x,(tuple,list)) and len(x)==2 and all(type(q) is Fraction for q in x) and x[0]<=x[1]
 return tuple(x)


def cui_point(q):
 assert type(q) is Fraction
 return q,q


def cui_dyadic(q):
 assert type(q) is Fraction and q.denominator&(q.denominator-1)==0
 return q


def cui_word(words):
 assert isinstance(words,(tuple,list)) and len(words)==2
 return cui_dyadic(words[0])+cui_dyadic(words[1])


def cui_add(x,y):
 x,y=cui_interval(x),cui_interval(y);return x[0]+y[0],x[1]+y[1]


def cui_neg(x):
 x=cui_interval(x);return -x[1],-x[0]


def cui_sub(x,y):return cui_add(x,cui_neg(y))


def cui_mul(x,y):
 x,y=cui_interval(x),cui_interval(y);p=[a*b for a in x for b in y];return min(p),max(p)


def cui_div(x,y):
 y=cui_interval(y);assert not y[0]<=0<=y[1],'Unresolved actual denominator interval'
 return cui_mul(x,(1/y[1],1/y[0]))


def cui_sum(xs):
 out=cui_point(Fraction(0))
 for x in xs:out=cui_add(out,x)
 return out


def cui_quantize(x,bits):
 x=cui_interval(x);D=1<<bits
 lo=x[0]*D;hi=x[1]*D
 return Fraction(lo.numerator//lo.denominator,D),Fraction(-((-hi.numerator)//hi.denominator),D)


def cui_exp_point(q,limits):
 assert type(q) is Fraction
 if q<0:return cui_div(cui_point(Fraction(1)),cui_exp_point(-q,limits))
 if q==0:return cui_point(Fraction(1))
 bits,cap,squares=limits['bits'],limits['max_terms'],limits['max_squarings']
 z=q;k=0
 while z>Fraction(1,2):
  assert k<squares,'Resource cap, not a physical-domain bound';z/=2;k+=1
 term=Fraction(1);total=term;eps=Fraction(1,1<<bits)
 for n in range(cap):
  nxt=term*z/(n+1);tail=nxt/(1-z/Fraction(n+2))
  if tail<=eps:out=(total,total+tail);break
  term=nxt;total+=term
 else:raise ArithmeticError('Taylor resource cap; no enclosure published')
 out=cui_quantize(out,bits)
 for unused in range(k):out=cui_quantize(cui_mul(out,out),bits)
 return out


def cui_exp(x,limits):
 x=cui_interval(x);return cui_exp_point(x[0],limits)[0],cui_exp_point(x[1],limits)[1]


def cui_sqrt(x,bits):
 x=cui_interval(x);assert x[0]>=0,'Actual square-root domain unresolved';D=1<<bits
 def endpoint(q,upper):
  a=q*D*D;k=isqrt(a.numerator//a.denominator);exact=Fraction(k*k,D*D)==q
  return Fraction(k+(1 if upper and not exact else 0),D)
 out=endpoint(x[0],False),endpoint(x[1],True)
 assert out[0]>=0 and out[0]*out[0]<=x[0] and out[1]*out[1]>=x[1]
 return out


def cui_rsqrt(x,bits):
 assert cui_interval(x)[0]>0
 return cui_div(cui_point(Fraction(1)),cui_sqrt(x,bits))


def cui_tree(words,shape,boxes=None):
 if not shape:
  q=cui_word(words);x=cui_point(q) if boxes is None else cui_interval(boxes)
  assert x[0]<=q<=x[1];return x
 assert isinstance(words,(list,tuple)) and len(words)==shape[0]
 assert boxes is None or isinstance(boxes,(list,tuple)) and len(boxes)==shape[0]
 return [cui_tree(w,shape[1:],None if boxes is None else boxes[i]) for i,w in enumerate(words)]


def cui_complete(role,payload,complete,records):
 ref=complete(role,payload);assert isinstance(ref,dict) and all(ref.get(n) for n in ('file','sha256','commit_file','commit_sha256'))
 records.append(ref);return ref


def cui_direct_sampling(s,complete,records,label):
 assert len(s['chi_corners'])==len(s['metric_corners'])==len(s['Fhat'])==4 and len(s['weights'])==len(s['rho_words'])==3
 rho=[];rho_gaps=[];delta=[];delta_gaps=[]
 for jet in range(3):
  assert len(s['weights'][jet])==4
  terms=[cui_dyadic(s['weights'][jet][corner])*cui_word(s['chi_corners'][corner]) for corner in range(4)]
  ideal=sum(terms,Fraction(0));actual=cui_word(s['rho_words'][jet]);rho.append((min(ideal,actual),max(ideal,actual)));rho_gaps.append(actual-ideal)
 cui_complete(label+'_SAMPLING_CHI',dict(rho=rho,actual_minus_exact_fixed_weight_law=rho_gaps,corner_order=[0,1,2,3]),complete,records)
 assert len(s['delta_six_words'])==6
 for slot in range(6):
  terms=[]
  for corner in range(4):
   assert len(s['Fhat'][corner])==len(s['metric_corners'][corner])==6 and len(s['Fhat'][corner][slot])==6
   terms.append(sum((cui_dyadic(s['Fhat'][corner][slot][j])*cui_word(s['metric_corners'][corner][j]) for j in range(6)),Fraction(0)))
  ideal=sum(terms,Fraction(0));actual=cui_word(s['delta_six_words'][slot]);delta.append((min(ideal,actual),max(ideal,actual)));delta_gaps.append(actual-ideal)
 cui_complete(label+'_SAMPLING_CORRECTION',dict(delta_six=delta,actual_minus_exact_fixed_Fhat_law=delta_gaps,corner_order=[0,1,2,3],matvec_coordinate_order=list(range(6))),complete,records)
 total=cui_tree(s['total_hdot_words'],(3,3));base=cui_tree(s['baseline_hdot_words'],(3,3));gaps=[]
 for slot,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
  assert s['baseline_hdot_words'][i][j]==s['baseline_hdot_words'][j][i] and s['total_hdot_words'][i][j]==s['total_hdot_words'][j][i]
  target=cui_add(base[i][j],delta[slot]);actual=total[i][j][0];gaps.append(cui_sub(cui_point(actual),target))
  total[i][j]=total[j][i]=(min(target[0],actual),max(target[1],actual))
 cui_complete(label+'_SAMPLING_TOTAL',dict(h_dot=total,total_words_minus_baseline_plus_fixed_Fhat_law=gaps,point_TOTAL_addition_after_lift=True),complete,records)
 return rho,total


def cui_det_inverse3(h):
 assert all(h[i][j]==h[j][i] for i in range(3) for j in range(3))
 cof=[]
 for i in range(3):
  row=[]
  for j in range(3):
   a=[k for k in range(3) if k!=i];b=[k for k in range(3) if k!=j]
   c=cui_sub(cui_mul(h[a[0]][b[0]],h[a[1]][b[1]]),cui_mul(h[a[0]][b[1]],h[a[1]][b[0]]));row.append(cui_neg(c) if (i+j)%2 else c)
  cof.append(row)
 det=cui_sum(cui_mul(h[0][j],cof[0][j]) for j in range(3));minor=cui_sub(cui_mul(h[0][0],h[1][1]),cui_mul(h[0][1],h[1][0]))
 assert h[0][0][0]>0 and minor[0]>0 and det[0]>0,'Actual reference SPD domain not proved'
 return det,[[cui_div(cof[j][i],det) for j in range(3)] for i in range(3)]


def cui_mv(A,x):return [cui_sum(cui_mul(A[i][j],x[j]) for j in range(3)) for i in range(3)]


def cui_block(g00,g0i,h):return [[g00]+g0i]+[[g0i[i]]+h[i] for i in range(3)]


def conformal_DIRECT43_primitive_enclosure(reference,sampling,admission,limits,complete,label):
 assert not CONFORMAL_UNCERTAINTY_AUTHOR_DRAFT and not CONFORMAL_UNCERTAINTY_AUTHORING_IN_PROGRESS
 assert all(x is not None for ref in CONFORMAL_UNCERTAINTY_TERMINALS.values() for x in ref)
 assert json.loads(json.dumps(admission['terminals']))==json.loads(json.dumps(CONFORMAL_UNCERTAINTY_TERMINALS)) and admission['source_pins']==CONFORMAL_UNCERTAINTY_SOURCE_PINS
 for n in ('all_selected_dyadic_inputs_authenticated','original_masks_lifts_Fhat_corner_order_verified','point_TOTAL_addition_after_lift_verified','same_event_reference_and_radial_side_verified','all_original_word_hex_and_gauge_time_phi_retained'):assert admission[n] is True
 assert admission['physical_metric_admitted'] is False and type(admission['finite_constraint_solution_admitted']) is bool and callable(complete)
 assert type(limits['bits']) is type(limits['max_terms']) is type(limits['max_squarings']) is int and 64<=limits['bits']<=1024 and 1<=limits['max_terms']<=4096 and 0<=limits['max_squarings']<=16
 records=[];fields={}
 for n,shape in (('h',(3,3)),('h_spatial_jets',(2,3,3)),('N',()),('beta',(3,)),('N_jets',(4,)),('beta_jets',(4,3))):fields[n]=cui_tree(reference['words'][n],shape,reference.get('source_boxes',{}).get(n))
 assert not reference.get('source_boxes') or admission['reference_source_box_proof_authenticated'] is True
 assert all(fields['h_spatial_jets'][a][i][j]==fields['h_spatial_jets'][a][j][i] for a in range(2) for i in range(3) for j in range(3)),'Original symmetric spatial-jet interval source required'
 cui_complete(label+'_INPUT',dict(reference=fields,sampling_refs=admission['sampling_refs'],provenance=admission,limits=limits),complete,records)
 rho,ht=cui_direct_sampling(sampling,complete,records,label);h0=fields['h'];N=fields['N'];b=fields['beta'];Na=fields['N_jets'];ba=fields['beta_jets'];assert N[0]>0
 det,I0=cui_det_inverse3(h0);lam=cui_exp(cui_mul(cui_point(Fraction(4)),rho[0]),limits);assert lam[0]>0
 rootlam=cui_sqrt(lam,limits['bits']);mu0=cui_sqrt(det,limits['bits']);ilam=cui_div(cui_point(Fraction(1)),lam)
 h=[[cui_mul(lam,x) for x in row] for row in h0];I=[[cui_mul(ilam,x) for x in row] for row in I0];mu=cui_mul(mu0,cui_mul(lam,rootlam))
 cui_complete(label+'_CONFORMAL',dict(rho=rho,lambda_interval=lam,lambda_inverse=ilam,lambda_root=rootlam,reference_det=det,reference_inverse=I0,h=h,ih=I,mu=mu),complete,records)
 spatial=[[[cui_mul(lam,cui_add(fields['h_spatial_jets'][a][i][j],cui_mul(cui_mul(cui_point(Fraction(4)),rho[a+1]),h0[i][j]))) for j in range(3)] for i in range(3)] for a in range(2)]
 zero=cui_point(Fraction(0));ha=[ht]+spatial+[[[zero for j in range(3)] for i in range(3)]]
 hb=cui_mv(h,b);g=cui_block(cui_sub(cui_sum(cui_mul(b[i],hb[i]) for i in range(3)),cui_mul(N,N)),hb,h)
 cui_complete(label+'_METRIC',dict(g=g,h_first=ha,all_four_gauge_jets=fields),complete,records);dg=[]
 for a in range(4):
  hba=[cui_add(x,y) for x,y in zip(cui_mv(ha[a],b),cui_mv(h,ba[a]))]
  first=cui_sum(cui_mul(ba[a][i],hb[i]) for i in range(3));second=cui_sum(cui_mul(b[i],hba[i]) for i in range(3));lapse=cui_mul(cui_point(Fraction(2)),cui_mul(N,Na[a]))
  dg.append(cui_block(cui_sub(cui_add(first,second),lapse),hba,ha[a]));cui_complete(label+'_FIRST_JET%d'%a,dict(derivative_index=a,dg=dg[-1]),complete,records)
 result=dict(g=g,dg=dg,h=h,ih=I,mu=mu,h_first=ha,derivative_index_first=True,coordinate_system='native313_cp_model_equals_one',provenance=admission,completed=records,finite_input_exact_law_enclosure=True,source_uncertainty_admitted=bool(reference.get('source_boxes')),installed_exp_pow_sqrt_accuracy_assumed=False,installed_DD_rounding_order_identity_claimed=False,Fhat_accuracy_beyond_authenticated_saved_words_admitted=False,axisymmetry_exact_zero_admitted=False,paired_word_collapse_admitted=False,binary64_readout_admitted=False,finite_constraint_solution_admitted=admission['finite_constraint_solution_admitted'],physical_metric_admitted=False,circle_or_velocity_adopted=False)
 cui_complete(label+'_PRIMITIVE_BOX',result,complete,records);return result


def attach_completed_DIRECT43_words(packet,words,complete,label):
 assert packet['finite_input_exact_law_enclosure'] is True and words['all_output_dyadic_words_authenticated'] is words['all_original_word_hex_preserved'] is True
 records=[];hulls={};gaps={}
 def attach(box,pair,shape):
  if not shape:
   q=cui_word(pair);box=cui_interval(box);return (min(box[0],q),max(box[1],q)),cui_sub(cui_point(q),box)
  assert len(pair)==len(box)==shape[0];rows=[attach(b,p,shape[1:]) for b,p in zip(box,pair)];return [r[0] for r in rows],[r[1] for r in rows]
 for n,shape in (('g',(4,4)),('dg',(4,4,4))):
  hulls[n],gaps[n]=attach(packet[n],words[n],shape);cui_complete(label+'_OUTPUT_'+n,dict(source_box=packet[n],exact_output_words=words[n],finite_input_output_hull=hulls[n],output_minus_source_box=gaps[n]),complete,records)
 return dict(g=hulls['g'],dg=hulls['dg'],source_box=packet,authentic_output_words=words,source_output_gaps=gaps,completed=records,finite_input_output_enclosure=True,observed_gap_used_as_a_priori_budget=False,rounding_origin_or_external_accuracy_budget_admitted=False,axisymmetry_exact_zero_admitted=False,paired_word_collapse_admitted=False,binary64_readout_admitted=False,physical_metric_admitted=False,circle_or_velocity_adopted=False)
