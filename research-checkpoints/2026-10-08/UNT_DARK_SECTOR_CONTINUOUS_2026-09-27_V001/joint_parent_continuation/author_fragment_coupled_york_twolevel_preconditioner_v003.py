# DEFINITIONS ONLY. No imports, calls, assembly or solver evaluation by author.
# Globals np/P/Q/keep are supplied by a later guarded caller; NumPy triangles below.
# Coarse arithmetic is a numerical preconditioner, never a new physical operator.
YORK_TWOLEVEL_AUTHOR_DRAFT=True
YORK_TWOLEVEL_CURRENT_TERMINAL=None

def york_coarse_mask():
 m=np.ones((3,44,23),bool);m[:,0]=False;m[:,-1]=False;m[:,:,-1]=False;m[1,:,0]=False
 assert np.array_equal(np.sum(m,axis=(1,2)),np.asarray((924,882,924)));return m

def york_coarse_lift(x):
 m=york_coarse_mask();assert x.shape==(2730,);v=np.zeros((3,44,23));v[m]=x;v[:,0]=v[:,1];return v

def york_coarse_restrict(x):
 assert x.shape==(3,44,23);y=x.copy();y[:,1]+=y[:,0];y[:,0]=0;y[:,-1]=0;y[:,:,-1]=0;y[1,:,0]=0;return y[york_coarse_mask()]

def york_coarse_plan(g,label):
 r=g['r'];z=g['z'];assert r.shape==(87,) and z.shape==(45,) and np.all(np.diff(r)>0) and np.all(np.diff(z)>0)
 ci=np.minimum(np.arange(87)//2,42);cj=np.minimum(np.arange(45)//2,21)
 ur=(r-r[2*ci])/(r[2*ci+2]-r[2*ci]);uz=(z-z[2*cj])/(z[2*cj+2]-z[2*cj]);assert np.all((ur>=0)&(ur<=1)) and np.all((uz>=0)&(uz<=1))
 node_weights=np.stack(((1-ur)[:,None]*(1-uz)[None,:],ur[:,None]*(1-uz)[None,:],(1-ur)[:,None]*uz[None,:],ur[:,None]*uz[None,:]))
 for n,v in (('coarse_r',r[::2]),('coarse_z',z[::2]),('fine_to_coarse_i',ci),('fine_to_coarse_j',cj),('physical_node_interpolation_weights',node_weights)):keep(label+'_'+n,v)
 fi=g['cell_i'];fj=g['cell_j'];assert fi.shape==fj.shape==(3784,) and fi.dtype==fj.dtype==np.dtype('int64') and np.all((fi>=0)&(fi<86)) and np.all((fj>=0)&(fj<44))
 ic=fi//2;jc=fj//2;coeff=np.empty((4,4,3784));corners=((0,0),(1,0),(0,1),(1,1))
 for f,(di,dj) in enumerate(corners):
  u=(r[fi+di]-r[2*ic])/(r[2*ic+2]-r[2*ic]);v=(z[fj+dj]-z[2*jc])/(z[2*jc+2]-z[2*jc])
  for c,(dc,ec) in enumerate(corners):coeff[f,c]=(u if dc else 1-u)*(v if ec else 1-v)
 keep(label+'_coarse_hat_values_at_fine_cell_corners',coeff)
 mask=york_coarse_mask();lookup=np.full(mask.shape,-1,dtype=np.int64);lookup[mask]=np.arange(2730);indices=np.empty((3784,12),dtype=np.int64)
 for component in range(3):
  for c,(di,dj) in enumerate(corners):
   ni=ic+di;nj=jc+dj;ni=np.where(ni==0,1,ni);indices[:,4*component+c]=lookup[component,ni,nj]
 keep(label+'_coarse_global_local_indices',indices);keep(label+'_coarse_mask',mask)
 return dict(ci=ci,cj=cj,node_weights=node_weights,corner_coefficients=coeff,indices=indices,mask=mask)

def york_coarse_prolong(x,plan):
 y=york_coarse_lift(x);out=np.zeros((3,87,45));ci=plan['ci'];cj=plan['cj']
 for c,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):out+=plan['node_weights'][c][None]*y[:,ci[:,None]+di,cj[None,:]+dj]
 return out[Q.york_vector_mask()]

def york_coarse_adjoint(x,plan):
 assert x.shape==(11135,);v=np.zeros((3,87,45));v[Q.york_vector_mask()]=x;out=np.zeros((3,44,23));ci=plan['ci'];cj=plan['cj']
 for c,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
  for component in range(3):np.add.at(out[component],(ci[:,None]+di,cj[None,:]+dj),plan['node_weights'][c]*v[component])
 return york_coarse_restrict(out)

def york_coarse_upper_add(upper,indices,a,b,gram):
 ia=indices[:,a];ib=indices[:,b];active=(ia>=0)&(ib>=0);left=ia[active];right=ib[active];term=gram[active]
 if a!=b:term=term*np.where(left==right,2.,1.)
 np.add.at(upper,(np.minimum(left,right),np.maximum(left,right)),term)

def york_new_coarse_gram(d,plan,label):
 # New local12 coarse columns compose frozen fine hats with physical nodal I.
 # All map words, including measured offblock contacts, enter the new features.
 maps=tuple(x.reshape(4,3784,3,3,3,3) for x in d['maps']);g=d['geometry'];upper=np.zeros((2730,2730));corners=((0,0),(1,0),(0,1),(1,1))
 ihdiag=np.diagonal(d['ih'],axis1=1,axis2=2).reshape(4,3784,3);mu=d['sqrt_h'].reshape(4,3784)
 assert np.all(ihdiag>0) and np.all(mu>0)
 for iq in range(4):
  features=P.a_dd(np.zeros((3784,12,3,3)));R=g['R'][iq].reshape(3784)
  for component in range(3):
   for coarsecorner in range(4):
    value=P.a_dd(np.zeros((3784,3,3)))
    for finecorner in range(4):
     N,NR,NZ=g['hats'][iq,finecorner].reshape(3,3784)
     factor=(R*N,R*NR+N,R*NZ) if component==0 else (N,NR,NZ)
     for jet in range(3):
      scalar=P.a_prod(factor[jet],plan['corner_coefficients'][finecorner,coarsecorner]);term=P.a_mul((maps[0][iq,:,component,jet],maps[1][iq,:,component,jet]),(scalar[0][:,None,None],scalar[1][:,None,None]));value=P.a_add(value,term)
      Q.york_pair_keep(label+'_current_coarse_column',value,keep)
    slot=4*component+coarsecorner;features[0][:,slot]=value[0];features[1][:,slot]=value[1];Q.york_pair_keep(label+'_current_coarse_features',features,keep)
  f=features[0]+features[1];keep(label+'_coarse_features_binary64_readout',f);Q.york_pair_keep(label+'_coarse_features_readout_defect',P.a_sub(features,P.a_dd(f)),keep)
  # The approximate Gram remains symmetric; no dropped crossblock or jitter.
  weight=(g['dv'][iq]/g['R'][iq]).reshape(3784)[:,None,None]*mu[iq,:,None,None]*ihdiag[iq,:,:,None]*ihdiag[iq,:,None,:]
  keep(label+'_positive_point_tensor_weights',weight);assert np.all(np.isfinite(weight)) and np.all(weight>0)
  for a in range(12):
   for b in range(a,12):
    gram=np.sum(weight*f[:,a]*f[:,b],axis=(1,2));keep(label+'_current_local_gram_term',gram)
    york_coarse_upper_add(upper,plan['indices'],a,b,gram)
   keep(label+'_coarse_gram_canonical_upper_partial',upper)
 # Sum once in canonical global order, then copy. Aliased local columns retain2.
 A=upper.copy();lower=np.tril_indices(2730,-1);A[lower]=upper.T[lower]
 keep(label+'_coarse_gram_canonical_upper',upper);keep(label+'_coarse_gram',A);assert np.all(np.isfinite(A)) and np.array_equal(A,A.T)
 diagonal=np.diag(A);keep(label+'_coarse_gram_diagonal',diagonal);assert np.all(diagonal>0)
 scale=np.sqrt(diagonal);normalized=A/(scale[:,None]*scale[None,:]);keep(label+'_coarse_positive_scale',scale);keep(label+'_normalized_coarse_gram',normalized)
 # Strict positivity is earned or refused; no diagonal gain or eigenvalue fit.
 factor=np.linalg.cholesky(normalized);keep(label+'_normalized_coarse_Cholesky',factor)
 defect=normalized-factor@factor.T;keep(label+'_coarse_factorization_defect',defect);assert np.all(np.isfinite(factor)) and np.all(np.diag(factor)>0)
 return dict(plan=plan,coarse_scale=scale,coarse_factor=factor,fine_scale=d['scale'],prolong=lambda x:york_coarse_prolong(x,plan),adjoint=lambda x:york_coarse_adjoint(x,plan),coarse_Gram_is_new_approximate_preconditioner=True,full_coupled_features_retained=True,global_coercivity_claimed=False,jitter_added=False)

def york_coarse_triangular_solve(A,b,lower=False,check_finite=True):
 # One earned dense factor; O(n^2) substitution, never repeated factorization.
 A=np.asarray(A,dtype=np.float64);b=np.asarray(b,dtype=np.float64);n=len(b);assert b.shape==(n,) and A.shape==(n,n)
 if check_finite:assert np.all(np.isfinite(A)) and np.all(np.isfinite(b))
 pivots=np.diag(A);assert np.all(np.isfinite(pivots)) and np.all(pivots>0)
 out=np.zeros(n);P.AVAILABLE['coarse_triangular_current_rhs']=b;P.AVAILABLE['coarse_triangular_current_partial_solution']=out
 for i in (range(n) if lower else range(n-1,-1,-1)):
  product=np.dot(A[i,:i],out[:i]) if lower else np.dot(A[i,i+1:],out[i+1:])
  value=(b[i]-product)/pivots[i];assert np.isfinite(product) and np.isfinite(value);out[i]=value
 return out

def york_twolevel_forward(y,pre,label):
 # T=(D^-1/2, I S^-1 L^-T), Ac=S L L^T S; TT^T is the SPD inverse preconditioner.
 n=len(pre['fine_scale']);m=len(pre['coarse_scale']);assert y.shape==(n+m,);fine=y[:n]/pre['fine_scale']
 coarse=york_coarse_triangular_solve(pre['coarse_factor'].T,y[n:],lower=False,check_finite=True)/pre['coarse_scale'];keep(label+'_coarse_potential',coarse)
 out=fine+pre['prolong'](coarse);keep(label+'_fine_correction',out);assert np.all(np.isfinite(out));return out

def york_twolevel_adjoint(x,pre,label):
 assert x.shape==pre['fine_scale'].shape;restricted=pre['adjoint'](x);keep(label+'_coarse_restricted_vector',restricted)
 coarse=york_coarse_triangular_solve(pre['coarse_factor'],restricted/pre['coarse_scale'],lower=True,check_finite=True)
 out=np.concatenate((x/pre['fine_scale'],coarse));keep(label+'_extended_vector',out);assert np.all(np.isfinite(out));return out

def york_twolevel_warm_correction(nodes,current,d,pre,label,cap):
 # One explicit caller budget; no zero reset, automatic cycles, or changed targets.
 assert 1<=cap<=160 and not current['admitted'];start=nodes;before=current
 Q.york_pair_keep(label+'_before_nodes',start,keep);Q.york_pair_keep(label+'_before_original_residual',before['residual'],keep);keep(label+'_before_original_ratios',before['ratios'])
 rhs0=before['residual'][0]+before['residual'][1];keep(label+'_fine_rhs_binary64',rhs0);Q.york_pair_keep(label+'_fine_rhs_readout_defect',P.a_sub(before['residual'],P.a_dd(rhs0)),keep)
 rhs=york_twolevel_adjoint(rhs0,pre,label+'_rhs');wn=float(np.linalg.norm(rhs));assert wn>0
 sufficient=float(np.min(d['sufficient_component_targets']));tolerance=min(.1,max(np.finfo(float).tiny,sufficient/wn));keep(label+'_sufficient_original_white_target',np.asarray(sufficient));keep(label+'_extended_relative_target',np.asarray(tolerance))
 def action(y):
  delta=york_twolevel_forward(y,pre,label+'_iterative_forward');value=Q.york_packed_action(P.a_dd(delta),d,label+'_iterative_fine_action')[0]
  return york_twolevel_adjoint(value[0]+value[1],pre,label+'_iterative_adjoint')
 def certificate(y):
  delta=york_twolevel_forward(y,pre,label+'_callback_forward');trial,q=P.dd_node_update(start,delta,keep,label+'_callback_update');answer=Q.york_original_certificate(trial,d,label+'_callback')
  return york_twolevel_adjoint(answer['residual'][0]+answer['residual'][1],pre,label+'_callback_residual'),answer['ratios']
 y,ratios,admitted,reason=P.minres_core(action,rhs,np.ones(13865),tolerance,certificate,label,cap=cap)
 keep(label+'_completed_extended_correction',y);keep(label+'_solver_return_ratios',ratios)
 delta=york_twolevel_forward(y,pre,label+'_completed_forward');updated,q=P.dd_node_update(start,delta,keep,label+'_final_update');after=Q.york_original_certificate(updated,d,label+'_final_original')
 adelta=Q.york_packed_action(P.a_dd(delta),d,label+'_completed_correction_action')[0];aq=Q.york_packed_action(P.a_dd(q),d,label+'_compression_action')[0]
 gap=P.a_sub(P.a_add(P.a_sub(after['residual'],before['residual']),adelta),aq);Q.york_pair_keep(label+'_original_residual_update_identity',gap,keep)
 envelope=2*d['rhs_envelope']
 for suffix,value in (('before',start),('after',updated),('delta',P.a_dd(delta)),('compression',P.a_dd(q))):envelope+=Q.york_packed_envelope(value,d,label+'_'+suffix)
 keep(label+'_residual_update_operation_envelope',envelope);P.check(label+'_paired_original_residual_update_identity',gap[0]+gap[1],np.zeros(11135),envelope)
 return updated,after,dict(cap=cap,reason=reason,solver_return_admitted=admitted,solver_return_ratios=ratios.tolist(),original_component_ratios=after['ratios'].tolist(),all_original_rows_admitted=after['admitted'],extended_dimension=13865,physical_TT_prepared=False)

def york_fresh_twolevel_control():
 # A new alias witness uses two physical scalar feature entries, not York data.
 indices=np.asarray(((0,0,1),),dtype=np.int64);columns=np.asarray(((1.,0.),(0.,2.),(1.,1.)));upper=np.zeros((2,2))
 keep('fresh_twolevel_alias_indices',indices);keep('fresh_twolevel_local_features',columns)
 for a in range(3):
  for b in range(a,3):york_coarse_upper_add(upper,indices,a,b,np.asarray((np.dot(columns[a],columns[b]),)))
 alias=upper.copy();alias[1,0]=upper[0,1];expected_alias=np.asarray(((5.,3.),(3.,2.)));keep('fresh_twolevel_alias_Gram',alias);keep('fresh_twolevel_expected_alias_Gram',expected_alias)
 # Exercise actual NumPy forward/back substitution with exact dyadic answers.
 L=np.asarray(((2.,0.),(1.,1.)));expected_tri=np.asarray((2.,3.));lo=york_coarse_triangular_solve(L,np.asarray((4.,5.)),lower=True);hi=york_coarse_triangular_solve(L.T,np.asarray((7.,3.)),lower=False)
 keep('fresh_twolevel_triangular_factor',L);keep('fresh_twolevel_triangular_expected',expected_tri);keep('fresh_twolevel_lower_solution',lo);keep('fresh_twolevel_upper_solution',hi)
 A=np.asarray(((3.,1.),(1.,2.)));target=np.asarray((1.,-2.));rhs=np.asarray((1.,-3.));fine_scale=np.asarray((2.,3.));I=np.asarray(((1.,0.),(1.,1.)))
 pre=dict(fine_scale=fine_scale,coarse_scale=np.ones(2),coarse_factor=L,prolong=lambda x:I@x,adjoint=lambda x:I.T@x)
 start=(np.asarray((.25,.5)),np.asarray((2.**-55,-2.**-54)));Q.york_pair_keep('fresh_twolevel_warm_nodes',start,keep)
 for name,value in (('fine_matrix',A),('exact_fine_target',target),('original_rhs',rhs),('fine_positive_scale',fine_scale),('coarse_prolongation',I)):keep('fresh_twolevel_'+name,value)
 def original(y):
  delta=york_twolevel_forward(y,pre,'fresh_twolevel_callback_forward');nodes,q=P.dd_node_update(start,delta,keep,'fresh_twolevel_callback_update');action=P.a_matvec(A,nodes);res=P.a_sub(P.a_dd(rhs),action)
  ratios=np.stack([P.original_ratios((res[0]+res[1])[i:i+1],rhs[i:i+1],fine_scale[i:i+1]) for i in range(2)]);Q.york_pair_keep('fresh_twolevel_current_original_residual',res,keep);keep('fresh_twolevel_current_original_ratios',ratios)
  return york_twolevel_adjoint(res[0]+res[1],pre,'fresh_twolevel_callback_adjoint'),ratios
 initial=P.a_sub(P.a_dd(rhs),P.a_matvec(A,start));Q.york_pair_keep('fresh_twolevel_initial_original_residual',initial,keep)
 rr=york_twolevel_adjoint(initial[0]+initial[1],pre,'fresh_twolevel_rhs');sufficient=1e-10*min(abs(rhs)/fine_scale);tolerance=sufficient/np.linalg.norm(rr)
 def transformed(y):
  delta=york_twolevel_forward(y,pre,'fresh_twolevel_trial_forward');a=P.a_matvec(A,P.a_dd(delta));return york_twolevel_adjoint(a[0]+a[1],pre,'fresh_twolevel_trial_adjoint')
 y,ratios,admitted,reason=P.minres_core(transformed,rr,np.ones(4),tolerance,original,'fresh_twolevel_rectangular_MINRES',cap=8)
 keep('fresh_twolevel_completed_extended_correction',y);keep('fresh_twolevel_final_original_ratios',ratios)
 delta=york_twolevel_forward(y,pre,'fresh_twolevel_completed_forward');nodes,q=P.dd_node_update(start,delta,keep,'fresh_twolevel_final_update');res=P.a_sub(P.a_dd(rhs),P.a_matvec(A,nodes));Q.york_pair_keep('fresh_twolevel_final_nodes',nodes,keep);Q.york_pair_keep('fresh_twolevel_final_residual',res,keep)
 error=float(np.linalg.norm(nodes[0]+nodes[1]-target));resnorm=float(np.linalg.norm(res[0]+res[1]));rounding=64*np.finfo(float).eps*(np.linalg.norm(target)+np.linalg.norm(nodes[0])+np.linalg.norm(nodes[1])+np.linalg.norm(rhs));bound=resnorm+rounding
 keep('fresh_twolevel_solution_error_and_bound',np.asarray((error,resnorm,rounding,bound)))
 actual=np.concatenate(((alias-expected_alias).ravel(),lo-expected_tri,hi-expected_tri,np.asarray((float(admitted),max(0.,error-bound)))))
 expected=np.zeros(10);expected[-2]=1.;P.check('fresh_twolevel_alias_triangular_and_rectangular_original_rows',actual,expected,np.ones(10))
 return dict(kind='fresh_alias_triangular_and_redundant_rectangular_congruence_control',fine_dimension=2,extended_dimension=4,cap=8,solver_reason=reason,original_ratios=ratios.tolist(),original_rows_admitted=admitted,fine_coercive_eigenvalue_lower_bound=1.,independent_error_bound=bound,coarse_matrix_is_artificial_preconditioner=True,old_York_or_coupled_fixture_replayed=False)
