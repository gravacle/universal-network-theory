"""HELD literal current temporal-gradient bridge; definitions only.
Globals np,P,fy_* use the reviewed paired arithmetic and exact-exponent product
scope. Inputs are completed SAME225 features/momenta and hydrated147 constants.
No geometry, current feature, canonical momentum, action, fixture or solver is
replayed. The literal six-term action is differentiated as a declared coefficient
polynomial, not as bitwise AD of the finite EFT program. Both words and both
tensor sides remain. Pure temporal mechanical contacts hold configuration fixed;
relative phase/ordinary rate derivatives are zero only in this declared scope.
The original weighted E* versus registered S bridge is a containing obligation.
"""
LITERAL_TEMPORAL_GRADIENT_AUTHOR_DRAFT=True
LITERAL_TEMPORAL_GRADIENT_AUTHORING_IN_PROGRESS=False

def lg_keep(label,x,keep):
 keep(label+'_both_words',np.stack(x).copy())
 assert len(x)==2 and x[0].shape==x[1].shape and all(a.dtype==np.float64 and np.all(np.isfinite(a)) for a in x)
 return fy_keep(label,x,keep)

def lg_transpose(x):return tuple(a.swapaxes(-1,-2) for a in x)

def lg_outer(x,y):return P.a_mul(tuple(a[..., :,None] for a in x),tuple(a[...,None,:] for a in y))

def lg_expand(x,*axes):
 for axis in axes:x=tuple(np.expand_dims(a,axis) for a in x)
 return x

def lg_div(x,y,keep,label):
 # Formal reciprocal coefficients; the finite quotient construction defect stays.
 out=fy_div(x,y,keep,label)
 lg_keep(label+'_reconstructed_product_defect',P.a_sub(P.a_mul(y,out),x),keep);return out

def lg_six(x):
 # A physical symmetric input has both cross entries equal to its single slot.
 return P.a_stack([P.a_slice(x,(slice(None),i,j)) if i==j else P.a_add(P.a_slice(x,(slice(None),i,j)),P.a_slice(x,(slice(None),j,i))) for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],-1)

def lg_native(u,z):
 return P.a_stack([P.a_slice(u,(slice(None),i)) for i in range(3)]+[P.a_slice(z,(j,slice(None),i)) for j in range(32) for i in range(3)],-1)

def candidate_literal_temporal_gradient_bridge(candidate,cache,keep,label):
 s,c,F,M=candidate['s'],candidate['c'],candidate['features']['paired'],candidate['momenta'];p=len(c['N']);put=lambda n,x:lg_keep(label+'_'+n,x,keep)
 assert cache['configuration_held'] is True and cache['p']==p and all(cache['constants'][n]==getattr(P,n) for n in ('ALPHA','ELL','C'))
 for family in ('s','c'):
  for n,a in cache[family].items():
   keep(label+'_same_candidate_'+family+'_'+n,np.asarray(a).copy())
   assert np.array_equal(a,candidate[family][n]),(family,n)
 for n,shape in (('F',(p,4,4)),('Fup',(p,4,4)),('V',(32,p,4)),('V_raised',(32,p,4)),('D',(32,p,4,4)),('D_raised',(32,p,4,4)),('Pi',(32,p,4,4)),('PiU',(p,4,4))):
  put('copied_current_feature_'+n,F[n]);assert F[n][0].shape==shape,n
 for n,shape in (('K',(p,3,3)),('Ktrace',(p,)),('native_density',(p,99)),('metric_native_density',(p,6)),('metric_EH_tensor',(p,3,3)),('metric_EH_density',(p,6)),('metric_total_density',(p,6))):
  put('copied_current_momentum_'+n,M[n]);assert M[n][0].shape==shape,n
 for n,x,shape in (('NA',cache['NA'],(32,p)),('gamma_squared',cache['gamma_squared'],(p,)),('formal_Iu',cache['formal_Iu'],(p,3))):
  put('copied_temporal_cache_'+n,x);assert x[0].shape==shape,n
 assert np.all(c['N']>0) and np.all(c['gamma']>0) and np.all(s['omega']>0) and np.all(s['w']>=0)
 H,G,Proj,I,U,z,beta,N,gamma=(P.a_dd(x) for x in (s['hi'],s['g'],s['P'],c['ih'],s['U'],s['z'],c['beta'],c['N'],c['gamma']))
 HT,PT,IT=lg_transpose(H),lg_transpose(Proj),lg_transpose(I);zi=P.a_slice(z,(slice(None),slice(None),slice(1,None)))
 up,uc=P.a_dd(c['up']),P.a_dd(c['u']);dens=P.a_dd(c['dens'])
 keep(label+'_copied_raw_current_Z',s['Z'].copy());assert s['Z'].shape==(p,4) and s['Z'].dtype==np.float64 and np.all(np.isfinite(s['Z']))
 put('formal_Iu_minus_raw_up',P.a_sub(cache['formal_Iu'],up));put('fixed_lowered_E0',cache['fixed_E0'])
 # Reverse both terms in each quadratic, with the actual saved raised operand.
 bF=put('literal_F_adjoint',P.a_mul64(-P.ALPHA/4,P.a_add(fy_mm(fy_mm(HT,F['F']),HT),F['Fup'])))
 bnu_Max=put('literal_nu_Maxwell_adjoint',fy_mm(P.a_sub(bF,lg_transpose(bF)),lg_transpose(G)))
 omega2=s['omega']**2;keep(label+'_literal_rounded_frequency_squared',omega2.copy())
 bV=lg_div(P.a_add(fy_mv(HT,F['V']),F['V_raised']),P.a_dd(2*omega2[:,None,None]),keep,label+'_literal_V_frequency')
 bV=put('literal_V_adjoint',P.a_mul64(s['w'][:,None,None],bV))
 bnz_V=put('literal_nz_V_adjoint',lg_outer(lg_expand(U,0),fy_mv(PT,bV)))
 bD=put('literal_D_adjoint',P.a_mul64(s['w'][:,None,None,None],P.a_mul64(-P.ELL**2/2,P.a_add(fy_mm(fy_mm(HT,F['D']),HT),F['D_raised']))))
 bnz_D=put('literal_nz_D_adjoint',fy_mm(fy_mm(PT,bD),Proj));bnz=put('literal_nz_adjoint',P.a_add(bnz_V,bnz_D))
 put('literal_nz_adjoint_minus_registered_Pi',P.a_sub(bnz,F['Pi']))
 Z=P.a_dd(np.zeros((p,4)))
 for j in range(32):Z=put('literal_acceleration_Z_partial',P.a_add(Z,P.a_mul64(s['w'][j],P.a_slice(z,j))))
 put('literal_acceleration_Z_minus_raw_Z',P.a_sub(Z,P.a_dd(s['Z'])))
 bnu_acc=put('literal_nu_acceleration_adjoint',lg_outer(U,Z));bnu=put('literal_nu_adjoint',P.a_add(bnu_Max,bnu_acc))
 put('literal_current_U_outer_Z_action',bnu_acc);put('registered_current_PiU_minus_literal_nu_adjoint',P.a_sub(F['PiU'],bnu))
 for n,terms in (('nu',(bnu_Max,bnu_acc)),('nz',(bnz_V,bnz_D))):
  keep(label+'_uncancelled_'+n+'_feature_adjoint_terms',np.stack([abs(t[0])+abs(t[1]) for t in terms]))
 # nu[a,l]=du[a,l]+Gamma[l,a,b]U[b]; nz_j[a,b]=dz_j[a,b]-Gamma[l,a,b]z_j[l].
 gamma_rows=[]
 for l in range(4):
  row=lg_outer(P.a_slice(bnu,(slice(None),slice(None),l)),U)
  for j in range(32):row=P.a_sub(row,P.a_mul64(s['z'][j,:,l,None,None],P.a_slice(bnz,j)))
  gamma_rows.append(row);put('literal_Gamma_adjoint_partial',P.a_stack(gamma_rows,1))
 bGa=put('literal_Gamma_adjoint',P.a_stack(gamma_rows,1));DGrows=[]
 for b in range(4):
  DGcols=[]
  for k in range(4):
   v=P.a_dd(np.zeros(p))
   for l in range(4):
    sym=P.a_add(P.a_slice(bGa,(slice(None),l,0,b)),P.a_slice(bGa,(slice(None),l,b,0)))
    v=P.a_add(v,P.a_sub(P.a_mul64(s['hi'][:,l,k],sym),P.a_mul64(s['hi'][:,l,0],P.a_slice(bGa,(slice(None),l,b,k)))))
   DGcols.append(P.a_mul64(.5,v))
  DGrows.append(P.a_stack(DGcols,-1));put('literal_temporal_DG_adjoint_partial',P.a_stack(DGrows,-2))
 bDG=put('literal_temporal_DG_adjoint',P.a_stack(DGrows,-2))
 # Reverse the declared147 temporal chart, retaining each quotient grouping.
 bUt=P.a_slice(bnu,(slice(None),0,slice(None)));bZt=P.a_slice(bnz,(slice(None),slice(None),0,slice(None)));gz0=P.a_slice(bZt,(slice(None),slice(None),0))
 gwt=put('formal_up_time_adjoint_initial',P.a_slice(bUt,(slice(None),slice(1,None))))
 ggt=lg_div(P.a_sub(P.a_slice(bUt,(slice(None),0)),fy_sum(P.a_mul(beta,gwt),-1)),N,keep,label+'_U0_reverse')
 gt_second=lg_div(P.a_mul(cache['NA'],gz0),lg_expand(cache['gamma_squared'],0),keep,label+'_z0_second_reverse')
 ggt=put('gamma_time_adjoint',P.a_add(ggt,fy_sum(gt_second,0)))
 gAt=put('anchored_A_time_adjoint',P.a_mul64(-1.,lg_div(P.a_mul(lg_expand(N,0),gz0),lg_expand(gamma,0),keep,label+'_z0_first_reverse')))
 gwt=put('formal_up_time_adjoint_after_modes',P.a_add(gwt,fy_sum(P.a_mul(zi,lg_expand(gAt,-1)),0)))
 gzt=put('modal_spatial_time_adjoint',P.a_add(P.a_add(P.a_slice(bZt,(slice(None),slice(None),slice(1,None))),P.a_mul(lg_expand(beta,0),lg_expand(gz0,-1))),P.a_mul(lg_expand(up,0),lg_expand(gAt,-1))))
 gnum=put('gamma_time_numerator_adjoint',lg_div(ggt,P.a_dd(2*c['gamma']),keep,label+'_gamma_numerator_reverse'))
 gwt=put('formal_up_time_adjoint_complete',P.a_add(gwt,P.a_mul(uc,lg_expand(gnum,-1))))
 gv=put('native_covector_time_adjoint',P.a_add(P.a_mul(up,lg_expand(gnum,-1)),fy_mv(IT,gwt)))
 gIt=put('formal_inverse_time_adjoint',lg_outer(gwt,uc))
 gQtime=put('formal_metric_time_adjoint',P.a_mul64(-1.,fy_mm(fy_mm(IT,gIt),IT)))
 factored=P.a_mul64(-1.,lg_outer(fy_mv(IT,gwt),cache['formal_Iu']))
 put('matrix_chain_minus_factored_formal_metric_adjoint',P.a_sub(gQtime,factored))
 cross=P.a_add(P.a_slice(bDG,(slice(None),0,slice(1,None))),P.a_slice(bDG,(slice(None),slice(1,None),0)))
 gQDG=put('temporal_DG_metric_adjoint',P.a_add(P.a_add(P.a_slice(bDG,(slice(None),slice(1,None),slice(1,None))),lg_outer(cross,beta)),P.a_mul(lg_expand(P.a_slice(bDG,(slice(None),0,0)),-1,-1),lg_outer(beta,beta))))
 native_L=put('literal_native_density',P.a_mul(lg_expand(dens,-1),lg_native(gv,gzt)))
 metric_L=put('literal_metric_native_density',P.a_mul(lg_expand(dens,-1),lg_six(P.a_add(gQtime,gQDG))))
 # Pull the SAME literal primitive adjoints through the registered raw left chart.
 cu=fy_mv(P.a_dd(c['JU'].transpose(0,2,1)),bUt)
 for j in range(32):cu=put('literal_C_native_U_partial',P.a_add(cu,P.a_mul64(c['JzU'][j],lg_expand(P.a_slice(gz0,j),-1))))
 cz=P.a_add(P.a_slice(bZt,(slice(None),slice(None),slice(1,None))),P.a_mul64(c['Jzz'][None],lg_expand(gz0,-1)))
 native_C=put('literal_C_native_density',P.a_mul(lg_expand(dens,-1),lg_native(cu,cz)))
 cm=fy_mv(P.a_dd(c['Uh']),bUt)
 for a in range(4):
  for b in range(4):cm=P.a_add(cm,P.a_mul64(c['embed'][:,:,a,b],lg_expand(P.a_slice(bDG,(slice(None),a,b)),-1)))
  put('literal_C_metric_embed_partial',cm)
 for j in range(32):cm=put('literal_C_metric_mode_partial',P.a_add(cm,P.a_mul64(c['zh'][j],lg_expand(P.a_slice(gz0,j),-1))))
 metric_C=put('literal_C_metric_native_density',P.a_mul(lg_expand(dens,-1),cm))
 # EH adjoint retains both occurrences of K, all current trace and raw hi00.
 K,tau=M['K'],M['Ktrace'];Kup=put('literal_EH_Kup_adjoint_coefficient',fy_mm(fy_mm(I,K),I))
 Kboth=put('literal_EH_two_sided_K_adjoint',P.a_add(Kup,fy_mm(fy_mm(IT,K),IT)))
 Ktrace=put('literal_EH_trace_adjoint',P.a_mul64(2.,P.a_mul(lg_expand(tau,-1,-1),I)))
 bK=lg_div(P.a_mul(lg_expand(dens,-1,-1),P.a_sub(Kboth,Ktrace)),P.a_dd(np.full((p,1,1),2*P.C)),keep,label+'_EH_K_reverse')
 kappa=put('literal_EH_Gamma_to_hdot_coefficient',P.a_mul64(-s['hi'][:,0,0]/2,N))
 EHtensor=put('literal_metric_EH_tensor',P.a_mul(lg_expand(kappa,-1,-1),bK));EH=put('literal_metric_EH_density',lg_six(EHtensor))
 registered_symmetric=put('registered_EH_two_sided_serialization',lg_six(M['metric_EH_tensor']))
 put('registered_EH_two_sided_minus_twice_upper',P.a_sub(registered_symmetric,M['metric_EH_density']))
 ratio=put('raw_EH_ideal_multiplier_comparison',P.a_mul64(-s['hi'][:,0,0],P.a_prod(c['N'],c['N'])))
 put('literal_EH_minus_ideal_multiplier_registered',P.a_sub(EH,P.a_mul(lg_expand(ratio,-1),registered_symmetric)))
 metric_total=put('literal_metric_total_density',P.a_add(metric_L,EH))
 bridges={}
 for name,right,left,registered in (('native',native_L,native_C,M['native_density']),('metric_native',metric_L,metric_C,M['metric_native_density'])):
  bridges[name+'_L_minus_C']=put(name+'_formal_right_minus_raw_left_gradient',P.a_sub(right,left))
  bridges[name+'_C_minus_registered']=put(name+'_literal_left_minus_registered_gradient',P.a_sub(left,registered))
  bridges[name+'_literal_minus_registered']=put(name+'_literal_minus_registered_gradient',P.a_sub(right,registered))
 bridges['metric_EH_literal_minus_registered']=put('metric_EH_literal_minus_registered_gradient',P.a_sub(EH,M['metric_EH_density']))
 bridges['metric_total_literal_minus_registered']=put('metric_total_literal_minus_registered_gradient',P.a_sub(metric_total,M['metric_total_density']))
 return dict(literal=dict(native=native_L,metric_native=metric_L,metric_EH=EH,metric_total=metric_total),literal_C=dict(native=native_C,metric_native=metric_C),registered={n:M[n+'_density'] for n in ('native','metric_native','metric_EH','metric_total')},bridges=bridges,primitive_adjoints=dict(nu=bnu,nz=bnz,Gamma=bGa,temporal_DG=bDG),candidate_provenance=candidate.get('candidate_provenance'),temporal_cache_provenance=cache.get('candidate_provenance'),scope='current fixed-configuration coefficient-polynomial temporal gradient; physical99+6 point covectors',relative_phase_or_ordinary_mechanical_rate_contact=False,original_weighted_Estar_vs_registered_S_measured=False,bitwise_EFT_program_AD=False,true_global_stationarity_or_Schwarz_qualified=False,physical_adoption=False)
