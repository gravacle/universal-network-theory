# DEFINITIONS ONLY. No imports, calls, assembly or solver evaluation by author.
# Globals np/P/Q/keep and solve_triangular are supplied by a later guarded caller.
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

def york_new_coarse_gram(d,plan,label):
 # New local12 coarse columns compose frozen fine hats with physical nodal I.
 # All map words, including measured offblock contacts, enter the new features.
 maps=tuple(x.reshape(4,3784,3,3,3,3) for x in d['maps']);g=d['geometry'];A=np.zeros((2730,2730));corners=((0,0),(1,0),(0,1),(1,1))
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
    ia=plan['indices'][:,a];ib=plan['indices'][:,b];active=(ia>=0)&(ib>=0)
    np.add.at(A,(ia[active],ib[active]),gram[active])
    if a!=b:np.add.at(A,(ib[active],ia[active]),gram[active])
   keep(label+'_coarse_gram_partial',A)
 keep(label+'_coarse_gram',A);assert np.all(np.isfinite(A)) and np.array_equal(A,A.T)
 diagonal=np.diag(A);keep(label+'_coarse_gram_diagonal',diagonal);assert np.all(diagonal>0)
 scale=np.sqrt(diagonal);normalized=A/(scale[:,None]*scale[None,:]);keep(label+'_coarse_positive_scale',scale);keep(label+'_normalized_coarse_gram',normalized)
 # Strict positivity is earned or refused; no diagonal gain or eigenvalue fit.
 factor=np.linalg.cholesky(normalized);keep(label+'_normalized_coarse_Cholesky',factor)
 defect=normalized-factor@factor.T;keep(label+'_coarse_factorization_defect',defect);assert np.all(np.isfinite(factor)) and np.all(np.diag(factor)>0)
 return dict(plan=plan,coarse_scale=scale,coarse_factor=factor,fine_scale=d['scale'],coarse_Gram_is_new_approximate_preconditioner=True,full_coupled_features_retained=True,global_coercivity_claimed=False,jitter_added=False)

def york_twolevel_forward(y,pre,label):
 # T=(D^-1/2, I S^-1 L^-T), Ac=S L L^T S; TT^T is the SPD inverse preconditioner.
 assert y.shape==(13865,);fine=y[:11135]/pre['fine_scale']
 coarse=solve_triangular(pre['coarse_factor'].T,y[11135:],lower=False,check_finite=True)/pre['coarse_scale'];keep(label+'_coarse_potential',coarse)
 out=fine+york_coarse_prolong(coarse,pre['plan']);keep(label+'_fine_correction',out);assert np.all(np.isfinite(out));return out

def york_twolevel_adjoint(x,pre,label):
 assert x.shape==(11135,);restricted=york_coarse_adjoint(x,pre['plan']);keep(label+'_coarse_restricted_vector',restricted)
 coarse=solve_triangular(pre['coarse_factor'],restricted/pre['coarse_scale'],lower=True,check_finite=True)
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
