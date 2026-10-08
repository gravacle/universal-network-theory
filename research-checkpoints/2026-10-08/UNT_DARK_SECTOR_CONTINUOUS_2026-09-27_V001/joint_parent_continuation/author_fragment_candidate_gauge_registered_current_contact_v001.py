"""HELD NEW gauge-current block; definitions only, no numerical invocation.
Globals np/P, reviewed160 fc_* anchor helpers, fy11/fs20, compact123 and195
cached derivative utilities. The containing owner authenticates SAME225 primals,
closed147 mechanical provenance and UPDATED13764 staged116 phase cache.
N/beta and all owned t/R/Z/phi firstjets vary; h, covariant spatial fields and
current genuine mechanical/phase rates remain fixed. Nothing constructs a new
primal feature/momentum/EOS/log/current. Anchored algebra comparisons retain
raw/formal inverse/chart/quotient/projector/Gamma/ADM defects.
C=D_gauge registered current; this is not -R_v^* or a literal-gradient bridge.
"""
GAUGE_CURRENT_AUTHOR_DRAFT=True
GAUGE_CURRENT_AUTHORING_IN_PROGRESS=False
GAUGE_CURRENT_PARENT_SOURCE=('author_fragment_finite_candidate_configuration_contact_v001.py','7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41')
GAUGE_PHASE_PARENT_SOURCE=('author_fragment_cached_updated_phase_compact_chi_contact_v001.py','ba1f599b85c367320d601fee9d58ea885c17f08452a7935666472fccc2eafa10')
GAUGE_NORMAL_SOURCE=('author_fragment_finite_candidate_native_EH_normal_v003.py','5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499')
GAUGE_CURRENT_CLOSED_SOURCE=(None,None)
GAUGE_CURRENT_CLOSED_RESULT=(None,None,None)
GAUGE_CURRENT_CLOSED_RECEIPT=(None,None,'CLOSED')
GAUGE_CURRENT_CLOSED_PROOF=(None,None,None)


def fgc_connection(hi,dg,E0,keep,label):
 shifted=fs_sub(dg,fs_dual(E0));rows=[]
 for a in range(4):
  columns=[]
  for b in range(4):
   terms=fs_sub(fs_add(fs_slice(shifted,(slice(None),a,b,slice(None))),fs_slice(shifted,(slice(None),b,a,slice(None)))),fs_slice(shifted,(slice(None),slice(None),a,b)))
   columns.append(fs_keep(label+'_connection_slot_%d_%d'%(a,b),fs_scale(.5,fs_mv(hi,terms)),keep))
   fs_keep(label+'_completed_connection_row_%d_columns'%a,fs_stack(columns,-1),keep)
  rows.append(fs_stack(columns,-1));fs_keep(label+'_completed_connection_rows',fs_stack(rows,-2),keep)
 return fs_keep(label+'_Gamma',fs_stack(rows,-2),keep)


def candidate_gauge_raw_action_contact(candidate,geometry,gauge,covectors,mechanical,direction,reference,keep,label):
 assert not GAUGE_CURRENT_AUTHOR_DRAFT and not GAUGE_CURRENT_AUTHORING_IN_PROGRESS
 s,c=candidate['s'],candidate['c'];jets=candidate['jets'];p=len(c['N'])
 put=lambda n,x:fs_keep(label+'_'+n,x,keep)
 anchor=lambda n,x,v:fc_anchor(label+'_'+n,x,v,keep)
 quotient=lambda n,a,b,v:fc_quotient(label+'_'+n,a,b,v,keep)
 for name,shape in (('h',(p,3,3)),('h_spatial_jets',(p,2,3,3)),('h_dot',(p,3,3)),('u_jets',(p,4,3)),('z_jets',(32,p,4,3))):
  assert all(isinstance(w,np.ndarray) and w.dtype==np.float64 and w.shape==shape and np.all(np.isfinite(w)) for w in direction[name])
  fy_keep(label+'_input_direction_'+name,direction[name],keep)
 assert all(np.all(w==0) for name in ('h','h_spatial_jets','h_dot','u_jets','z_jets') for w in direction[name]),'Gauge contact holds h, all mechanical rates and covector jets fixed'
 for name,shape in (('N',(p,)),('beta',(p,3)),('N_jets',(p,4)),('beta_jets',(p,4,3))):
  fy_keep(label+'_input_gauge_direction_'+name,direction[name],keep);assert all(w.shape==shape and w.dtype==np.float64 and np.all(np.isfinite(w)) for w in direction[name])
 assert all(np.all(w[:,1:]==0) for w in direction['u_jets']) and all(np.all(w[:,:,1:]==0) for w in direction['z_jets'])
 h=put('h',fs_dual(P.a_dd(c['h']),direction['h']));I0=P.a_dd(c['ih'])
 dI=fc_symmetric_contact(label+'_inverse_direction',P.a_mul64(-1.,fy_mm(fy_mm(I0,direction['h']),I0)),keep);I=put('ih',fs_dual(I0,dI))
 fractional=P.a_mul64(.5,fy_contract(I0,direction['h']));mu=put('sqrt_h',fs_dual(P.a_dd(c['sqrt_h']),P.a_mul64(c['sqrt_h'],fractional)))
 N=put('N',fs_dual(P.a_dd(c['N']),direction['N']));beta=put('beta',fs_dual(P.a_dd(c['beta']),direction['beta']));u=fs_dual(P.a_dd(c['u']));zi=fs_dual(P.a_dd(s['z'][:,:,1:]))
 Na=put('N_first',fs_dual(gauge['N_jets'],direction['N_jets']));ba=put('beta_first',fs_dual(gauge['beta_jets'],direction['beta_jets']));ua=fs_dual(covectors['u_jets']);za=fs_dual(covectors['z_jets'])
 ht=fs_dual(mechanical['h_dot'],direction['h_dot']);zero=fs_dual(P.a_dd(np.zeros((p,3,3))))
 ha=put('h_first',fs_stack([ht,fs_dual(P.a_slice(geometry['h_spatial_jets'],(slice(None),0)),P.a_slice(direction['h_spatial_jets'],(slice(None),0))),fs_dual(P.a_slice(geometry['h_spatial_jets'],(slice(None),1)),P.a_slice(direction['h_spatial_jets'],(slice(None),1))),zero],1))
 put('inverse_residual',fs_sub(fs_mm(h,I),fs_dual(P.a_dd(np.broadcast_to(np.eye(3),(p,3,3))))))
 put('volume_square_contact',fs_mul(mu,mu))
 if 'ih' in direction:fy_keep(label+'_supplied_geometry_minus_raw_formal_inverse_contact',P.a_sub(direction['ih'],dI),keep)
 if 'mu' in direction:fy_keep(label+'_supplied_geometry_minus_raw_volume_contact',P.a_sub(direction['mu'],mu[1]),keep)
 up=put('up',anchor('up',fs_mv(I,u),c['up']))
 gamma=put('gamma',fc_square_root(label+'_gamma',fs_add(fs_dual(P.a_dd(np.ones(p))),fs_dot(u,up)),c['gamma'],keep))
 U0=quotient('U0',gamma,N,s['U'][:,0]);Ui=anchor('Ui',fs_sub(up,fs_mul(beta,fs_expand(U0,(Ellipsis,None)))),s['U'][:,1:])
 U=put('U',fs_stack([U0]+[fs_slice(Ui,(slice(None),i)) for i in range(3)],1))
 A=anchor('up_dot_zi',fs_dot(fs_expand(up,(None,Ellipsis)),zi),np.einsum('pi,jpi->jp',c['up'],s['z'][:,:,1:]))
 zquot=quotient('z0_quotient',fs_mul(fs_expand(N,(None,Ellipsis)),A),fs_expand(gamma,(None,Ellipsis)),c['N'][None]*A[0][0]/c['gamma'][None])
 z0=anchor('z0',fs_sub(fs_dot(fs_expand(beta,(None,Ellipsis)),zi),zquot),s['z'][:,:,0]);z=put('z',fs_stack([z0]+[fs_slice(zi,(slice(None),slice(None),i)) for i in range(3)],2))
 N2=anchor('N_squared',fs_mul(N,N),c['N']**2);g2=anchor('gamma_squared',fs_mul(gamma,gamma),c['gamma']**2);g3=anchor('gamma_cubed',fs_mul(g2,gamma),c['gamma']**3)
 hb=anchor('h_beta',fs_mv(h,beta),np.einsum('pij,pj->pi',c['h'],c['beta']))
 g=put('g',anchor('g',fs_block(fs_sub(fs_dot(beta,hb),N2),hb,h),s['g']))
 bb=fs_mul(fs_expand(beta,(Ellipsis,slice(None),None)),fs_expand(beta,(Ellipsis,None,slice(None))))
 hi00=put('hi00',quotient('hi00',fs_dual(P.a_dd(-np.ones(p))),N2,s['hi'][:,0,0]));hi0i=put('hi0i',quotient('hi0i',beta,fs_expand(N2,(Ellipsis,None)),s['hi'][:,0,1:]))
 hij=anchor('hi_spatial',fs_sub(I,fs_div(bb,fs_expand(N2,(Ellipsis,None,None)),keep,label+'_shift_inverse')),s['hi'][:,1:,1:])
 hi=put('hi',fs_block(hi00,hi0i,hij));dens=put('dens',anchor('dens',fs_mul(N,mu),c['dens']))
 uc=put('uc',anchor('uc',fs_mv(g,U),s['uc']))
 projector=put('P',anchor('P',fs_add(fs_dual(P.a_dd(np.broadcast_to(np.eye(4),(p,4,4)))),fs_mul(fs_expand(uc,(Ellipsis,slice(None),None)),fs_expand(U,(Ellipsis,None,slice(None))))),s['P']))
 Z=fs_dual(P.a_dd(np.zeros((p,4))))
 for j in range(32):Z=fs_add(Z,fs_scale(s['w'][j],fs_slice(z,j)));put('current_Z',Z)
 Z=put('Z',anchor('Z',Z,s['Z']))
 assert 'phi' not in direction,'Gauge contact fixes the actual phase covector'
 phi=fs_dual(P.a_dd(s['phi']));put('phi',phi)
 put('r',anchor('r',fs_mv(projector,phi),s['r']))
 z2=put('z2',anchor('z2',fs_dot(z,fs_mv(hi,z)),s['z2']))
 kj=(P.B*P.GC)**2*s['xi'][:,None]**4;put('f',anchor('f',fs_add(fs_dual(P.a_dd(np.ones_like(s['f']))),fs_scale(1/kj,z2)),s['f']))
 e=np.zeros((6,3,3))
 for a,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):e[a,i,j]=e[a,j,i]=1.
 E=fs_dual(P.a_dd(e[None]));Ng=anchor('N_gamma',fs_mul(N,gamma),c['N']*c['gamma'])
 JU0=quotient('JU0',up,fs_expand(Ng,(Ellipsis,None)),c['JU'][:,0])
 JUsp=anchor('JUsp',fs_sub(I,fs_mul(fs_expand(beta,(Ellipsis,slice(None),None)),fs_expand(JU0,(Ellipsis,None,slice(None))))),c['JU'][:,1:])
 JU=put('JU',fs_stack([JU0]+[fs_slice(JUsp,(slice(None),i)) for i in range(3)],1))
 Jzz=put('Jzz',anchor('Jzz',fs_sub(beta,fs_div(fs_mul(fs_expand(N,(Ellipsis,None)),up),fs_expand(gamma,(Ellipsis,None)),keep,label+'_Jzz_quotient')),c['Jzz']))
 term=fs_sub(fs_div(fs_mv(I,zi),fs_expand(gamma,(None,Ellipsis,None)),keep,label+'_JzU_first'),fs_div(fs_mul(fs_expand(A,(Ellipsis,None)),fs_expand(up,(None,Ellipsis))),fs_expand(g3,(None,Ellipsis,None)),keep,label+'_JzU_second'))
 JzU=put('JzU',anchor('JzU',fs_mul(fs_expand(fs_neg(N),(None,Ellipsis,None)),term),c['JzU']))
 Eu=fs_mv(E,fs_expand(up,(Ellipsis,None,slice(None))));wh=anchor('wh',fs_neg(fs_mv(fs_expand(I,(Ellipsis,None,slice(None),slice(None))),Eu)),-np.einsum('pij,ajk,pk->pai',c['ih'],e,c['up']))
 gh=quotient('gh',fs_neg(fs_dot(fs_expand(up,(Ellipsis,None,slice(None))),Eu)),fs_expand(fs_scale(2.,gamma),(Ellipsis,None)),-np.einsum('pi,aij,pj->pa',c['up'],e,c['up'])/(2*c['gamma'][:,None]))
 Uh0=quotient('Uh0',gh,fs_expand(N,(Ellipsis,None)),c['Uh'][:,:,0]);Uhi=fs_sub(wh,fs_mul(fs_expand(beta,(Ellipsis,None,slice(None))),fs_expand(Uh0,(Ellipsis,None))))
 Uh=put('Uh',anchor('Uh',fs_stack([Uh0]+[fs_slice(Uhi,(slice(None),slice(None),i)) for i in range(3)],2),c['Uh']))
 whz=fs_dot(fs_expand(zi,(Ellipsis,None,slice(None))),fs_expand(wh,(None,Ellipsis)))
 zh=put('zh',anchor('zh',fs_mul(fs_expand(fs_neg(N),(None,Ellipsis,None)),fs_sub(fs_div(whz,fs_expand(gamma,(None,Ellipsis,None)),keep,label+'_zh_first'),fs_div(fs_mul(fs_expand(A,(Ellipsis,None)),fs_expand(gh,(None,Ellipsis))),fs_expand(g2,(None,Ellipsis,None)),keep,label+'_zh_second'))),c['zh']))
 eb=fs_mv(E,fs_expand(beta,(Ellipsis,None,slice(None))))
 embed=put('embed',anchor('embed',fs_stack([fs_block(fs_dot(beta,fs_slice(eb,(slice(None),a))),fs_slice(eb,(slice(None),a)),fs_dual(P.a_dd(np.broadcast_to(e[a],(p,3,3))))) for a in range(6)],1),c['embed']))
 dgrows=[];durows=[];dzrows=[];Iarows=[];warows=[];garows=[]
 for a in range(4):
  H=fs_slice(ha,(slice(None),a));n=fs_slice(Na,(slice(None),a));b=fs_slice(ba,(slice(None),a));v=fs_slice(ua,(slice(None),a));zz=fs_slice(za,(slice(None),slice(None),a))
  ia=fs_neg(fs_mm(fs_mm(I,H),I));Iarows.append(ia)
  wa=fs_add(fs_mv(ia,u),fs_mv(I,v));warows.append(wa)
  ga=fs_div(fs_add(fs_dot(v,up),fs_dot(u,wa)),fs_scale(2.,gamma),keep,label+'_gamma_first_'+str(a));garows.append(ga)
  U0a=fs_sub(fs_div(ga,N,keep,label+'_U0_first_'+str(a)),fs_div(fs_mul(gamma,n),N2,keep,label+'_U0_second_'+str(a)))
  Uia=fs_sub(fs_sub(wa,fs_mul(fs_expand(U0,(Ellipsis,None)),b)),fs_mul(beta,fs_expand(U0a,(Ellipsis,None))))
  durows.append(fs_stack([U0a]+[fs_slice(Uia,(slice(None),i)) for i in range(3)],1))
  Aa=fs_add(fs_dot(fs_expand(wa,(None,Ellipsis)),zi),fs_dot(fs_expand(up,(None,Ellipsis)),zz))
  numerator=fs_add(fs_mul(fs_expand(n,(None,Ellipsis)),A),fs_mul(fs_expand(N,(None,Ellipsis)),Aa))
  second=fs_div(fs_mul(fs_mul(fs_expand(N,(None,Ellipsis)),A),fs_expand(ga,(None,Ellipsis))),fs_expand(g2,(None,Ellipsis)),keep,label+'_z0_second_'+str(a))
  shift=fs_add(fs_dot(fs_expand(b,(None,Ellipsis)),zi),fs_dot(fs_expand(beta,(None,Ellipsis)),zz))
  z0a=fs_add(shift,fs_sub(second,fs_div(numerator,fs_expand(gamma,(None,Ellipsis)),keep,label+'_z0_first_'+str(a))))
  dzrows.append(fs_stack([z0a]+[fs_slice(zz,(slice(None),slice(None),i)) for i in range(3)],2))
  hba=fs_add(fs_mv(H,beta),fs_mv(h,b));g00a=fs_sub(fs_add(fs_dot(b,hb),fs_dot(beta,hba)),fs_scale(2.,fs_mul(N,n)))
  dgrows.append(fs_block(g00a,hba,H));put('current_dg',fs_stack(dgrows,1));put('current_du',fs_stack(durows,1));put('current_dz',fs_stack(dzrows,2))
 dg=put('dg',anchor('dg',fs_stack(dgrows,1),jets['dg']));du=put('du',anchor('du',fs_stack(durows,1),jets['du']));dz=put('dz',anchor('dz',fs_stack(dzrows,2),jets['dz']))
 Ia=put('inverse_first',fs_stack(Iarows,1));wa=put('up_first',fs_stack(warows,1));ga=put('gamma_first',fs_stack(garows,1))
 Ga=put('Ga',anchor('Ga',fgc_connection(hi,dg,reference['E0'],keep,label+'_fixed_E0'),jets['Ga']))
 put('spacetime_inverse_residual',fs_sub(fs_mm(g,hi),fs_dual(P.a_dd(np.broadcast_to(np.eye(4),(p,4,4))))))
 formal_inverse=fy_keep(label+'_formal_inverse_gauge_contact',P.a_mul64(-1.,fy_mm(fy_mm(P.a_dd(s['hi']),g[1]),P.a_dd(s['hi']))),keep)
 fy_keep(label+'_direct_ADM_minus_formal_inverse_gauge_contact',P.a_sub(hi[1],formal_inverse),keep)
 put('unit_constraint',fs_add(fs_dot(U,uc),fs_dual(P.a_dd(np.ones(p)))));put('transverse_constraint',fs_dot(fs_expand(U,(None,Ellipsis)),z))
 compatibility=[]
 for a in range(4):
  G=fs_slice(Ga,(slice(None),slice(None),a,slice(None)))
  compatibility.append(fs_sub(fs_slice(dg,(slice(None),a)),fs_add(fs_mm(fs_transpose(G,(0,2,1)),g),fs_mm(g,G))))
 put('compatibility_minus_fixed_E0',fs_sub(fs_stack(compatibility,1),fs_dual(reference['E0'])))
 put('connection_torsion',fs_sub(Ga,fs_transpose(Ga,(0,1,3,2))))
 d={n:x[1] for n,x in dict(g=g,hi=hi,U=U,z=z,uc=uc,P=projector,phi=phi,dg=dg,du=du,dz=dz,Ga=Ga).items()}
 dc={n:x[1] for n,x in dict(h=h,ih=I,N=N,beta=beta,u=u,up=up,gamma=gamma,JU=JU,Jzz=Jzz,JzU=JzU,Uh=Uh,zh=zh,embed=embed,dens=dens,sqrt_h=mu,mu=mu).items()}
 dc['log_dens']=fy_div(dc['dens'],P.a_dd(c['dens']),keep,label+'_fractional_density_contact')
 df,dm=compact_contact_momenta(s,c,jets,candidate['features'],candidate['momenta'],d,dc,keep,label+'_NEW_action_contact')
 # 123's K direction fixes N. The NEW gauge contact needs both factors.
 oldK,oldtrace=dm['K'],dm['Ktrace'];fy_keep(label+'_123_fixed_N_K_contact',oldK,keep);fy_keep(label+'_123_fixed_N_Ktrace_contact',oldtrace,keep)
 KG=put('K_Gamma',anchor('K_Gamma',fs_mul(fs_expand(N,(Ellipsis,None,None)),fs_slice(Ga,(slice(None),0,slice(1,None),slice(1,None)))),candidate['momenta']['K']))
 trace=put('Ktrace_Gamma',anchor('Ktrace_Gamma',fs_sum(fs_sum(fs_mul(I,KG),2),1),candidate['momenta']['Ktrace']))
 dm['K'],dm['Ktrace']=KG[1],trace[1]
 fy_keep(label+'_full_gauge_minus_123_fixed_N_K_contact',P.a_sub(dm['K'],oldK),keep);fy_keep(label+'_full_gauge_minus_123_fixed_N_Ktrace_contact',P.a_sub(dm['Ktrace'],oldtrace),keep)
 df['fixed_rates_gauge_spectrum_and_phase_jets']=False;df['gauge_contact_with_fixed_mechanical_rates']=True
 fy_keep(label+'_full_N_product_minus_fixed_N_increment',P.a_sub(P.a_sub(dm['K'],oldK),P.a_mul((direction['N'][0][:,None,None],direction['N'][1][:,None,None]),P.a_slice(jets['Ga'],(slice(None),0,slice(1,None),slice(1,None))))),keep)
 spatial_fraction=fy_div(dc['sqrt_h'],P.a_dd(c['sqrt_h']),keep,label+'_fractional_spatial_volume_contact')
 fy_keep(label+'_spatial_minus_4D_density_fraction_gap',P.a_sub(spatial_fraction,dc['log_dens']),keep)
 # NEW EH contact uses its own sqrt_h product/division, not the 4D fraction.
 Kdual=fs_dual(candidate['momenta']['K'],dm['K']);taudual=fs_dual(candidate['momenta']['Ktrace'],dm['Ktrace'])
 pinum=fs_mul(fs_expand(mu,(Ellipsis,None,None)),fs_sub(fs_mm(fs_mm(I,Kdual),I),fs_mul(fs_expand(taudual,(Ellipsis,None,None)),I)))
 pi=anchor('metric_EH_tensor',(P.a_div64(pinum[0],2*P.C,keep,label+'_EH_value_division'),P.a_div64(pinum[1],2*P.C,keep,label+'_EH_contact_division')),candidate['momenta']['metric_EH_tensor'])
 fy_keep(label+'_new_EH_minus_123_density_measure_contact',P.a_sub(pi[1],dm['metric_EH_tensor']),keep);dm['metric_EH_tensor']=pi[1]
 dm['metric_EH_density']=P.a_stack([P.a_mul64(1. if i==j else 2.,P.a_slice(pi[1],(slice(None),i,j))) for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],-1)
 two_sided=P.a_stack([P.a_slice(pi[1],(slice(None),i,j)) if i==j else P.a_add(P.a_slice(pi[1],(slice(None),i,j)),P.a_slice(pi[1],(slice(None),j,i))) for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],-1)
 fy_keep(label+'_EH_genuine_two_entry_physical_pullback',two_sided,keep);fy_keep(label+'_EH_registered_twice_upper_minus_two_entry_contact',P.a_sub(dm['metric_EH_density'],two_sided),keep)
 dm['metric_total_density']=P.a_add(dm['metric_native_density'],dm['metric_EH_density'])
 for family,values in (('configuration',d),('chart',dc),('feature',df['paired']),('momentum',dm)):
  for n,x in values.items():fy_keep(label+'_completed_'+family+'_'+n,x,keep)
 Lie=fs_dual(P.a_dd(np.zeros((p,3,3))))
 for k in range(3):Lie=fs_add(Lie,fs_mul(fs_expand(fs_slice(beta,(slice(None),k)),(Ellipsis,None,None)),fs_slice(ha,(slice(None),k+1))))
 columns=[]
 for i in range(3):
  rows=[]
  for j in range(3):
   rows.append(fs_add(fs_slice(Lie,(slice(None),i,j)),fs_add(fs_dot(fs_slice(h,(slice(None),j)),fs_slice(ba,(slice(None),i+1))),fs_dot(fs_slice(h,(slice(None),i)),fs_slice(ba,(slice(None),j+1))))))
  columns.append(fs_stack(rows,-1))
 Lie=put('Lie_beta_h',fs_stack(columns,-2));KADM=put('KADM',fs_div(fs_sub(ht,Lie),fs_expand(fs_scale(2.,N),(Ellipsis,None,None)),keep,label+'_KADM'))
 KG=fs_dual(candidate['momenta']['K'],dm['K']);put('KGamma_minus_KADM',fs_sub(KG,KADM))
 put('Ktrace_Gamma_minus_ADM',fs_sub(fs_dual(candidate['momenta']['Ktrace'],dm['Ktrace']),fs_sum(fs_sum(fs_mul(I,KADM),2),1)))
 # The raw mechanical r contact uses the archived phase representative only;
 # mechanical momenta are phi independent. Literal phase uses updated cache.
 fy_keep(label+'_phase_direction_omitted_from_native_r_contact',fy_mv(P.a_dd(s['P']),phi[1]),keep)
 state=dict(h=h,ih=I,mu=mu,N=N,beta=beta,up=up,gamma=gamma,A=A,U=U,z=z,g=g,hi=hi,uc=uc,P=projector,phi=phi,Z=Z,z2=z2,dens=dens,h_first=ha,inverse_first=Ia,up_first=wa,gamma_first=ga,N_first=Na,beta_first=ba,z_spatial_first=za,du=du,dz=dz,dg=dg,Ga=Ga,KADM=KADM)
 return dict(d=d,dc=dc,delta_features=df,delta_momenta=dm,state=state,h_first=ha[0],delta_h_first=ha[1],inverse_first=Ia[0],delta_inverse_first=Ia[1],geometry_rounding_map_differentiated=False,phase_relative_owned_by_separate_literal_core=True,gauge_value_and_all_firstjets_varied=True,mechanical_and_phase_rates_fixed=True,old_coefficients_transported=False,physical_adoption=False)


def candidate_cached_phase_gauge_contact(prepared,direction,keep,label):
 assert not GAUGE_CURRENT_AUTHOR_DRAFT and not GAUGE_CURRENT_AUTHORING_IN_PROGRESS and prepared['physical_adoption'] is False
 v=prepared['values'];s=prepared['s'];c=prepared['c'];p=s['phi'][0].shape[0];put=lambda n,x:fy_keep(label+'_NEW_'+n,x,keep)
 z=lambda shape:P.a_dd(np.zeros(shape));add=P.a_add;mul=P.a_mul;scale=P.a_mul64;sl=P.a_slice;sub=lambda a,b:add(a,scale(-1.,b))
 expand=lambda x,key:(x[0][key],x[1][key]);neg=lambda x:scale(-1.,x);prod=cached_phase_product_direction;dot=cached_phase_dot_direction;mv=cached_phase_mv_direction
 zero=z((p,))
 for values,shapes in ((s,dict(hi=(p,4,4),P=(p,4,4),phi=(p,4),U=(p,4),uc=(p,4))), (c,dict(N=(p,),mu=(p,),ih=(p,3,3),u=(p,3)))):
  for n,shape in shapes.items():
   fy_keep(label+'_configuration_direction_'+n,direction[n],keep);assert all(a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a)) for a in direction[n])
 assert all(np.all(a==0) for n in ('mu','ih','u','phi') for a in direction[n]),'Gauge contact holds spatial geometry, covectors and phase rate fixed'
 assert all(np.array_equal(a,a.swapaxes(-1,-2)) for n in ('hi','ih') for a in direction[n])
 div=lambda key,den,dnum,dden:put(key+'_direction',cached_phase_division_direction(v[key],den,dnum,dden,keep,label+'_'+key))
 draised=put('raised_phi',mv(s['hi'],s['phi'],direction['hi'],direction['phi']))
 dX2=put('X2',neg(dot(s['phi'],v['raised'],direction['phi'],draised)))
 dX=put('X',fy_div(dX2,scale(2.,v['X']),keep,label+'_clock_root_NEW_direction'))
 fy_keep(label+'_NEW_clock_direction_square_residual',sub(scale(2.,mul(v['X'],dX)),dX2),keep)
 dq=div('q',v['X0'],dX,zero);du=put('u',sub(prod(v['q'],v['q'],dq,dq),zero));dd=put('distance_to_EOS_boundary',sub(zero,du))
 ds=div('s',v['d'],du,dd);dlog=put('logarithm',fy_div(ds,v['one_plus_s'],keep,label+'_log_NEW_analytic_direction'))
 dfraction=div('fraction',v['one_plus_s'],ds,add(zero,ds));dpressureq=div('pressure_quotient',v['norm'],sub(dlog,dfraction),zero)
 A0=prepared['constants']['A0'];dpressure=put('pressure',scale(A0,sub(dpressureq,zero)))
 dPXdimensionless=div('PX_dimensionless',v['epnorm'],prod(v['q'],v['s'],dq,ds),zero)
 dPX=div('PX',v['X0'],scale(2*A0,dPXdimensionless),zero)
 dfirst=div('PXX_first',v['epnorm'],scale(2.,ds),zero);dq2=prod(v['q'],v['q'],dq,dq);dd2=prod(v['d'],v['d'],dd,dd)
 # The constant normalization direction is exactly zero; retain source addition.
 dPXXden=add(zero,mul(v['norm'],dd2));dsecond=div('PXX_second',v['PXX_second_denominator'],scale(4.,dq2),dPXXden)
 dPXX=div('PXX',v['X0_squared'],scale(A0,add(dfirst,dsecond)),zero)
 chain={}
 for n,actual,expected in (('P',dpressure,mul(v['PX'],dX)),('PX',dPX,mul(v['PXX'],dX)),('PXX',dPXX,mul(v['PXXX'],dX))):
  fy_keep(label+'_NEW_'+n+'_analytic_chain_actual',actual,keep);fy_keep(label+'_NEW_'+n+'_analytic_chain_expected',expected,keep);chain[n]=put(n+'_analytic_chain_gap',sub(actual,expected))
 dclock=put('clock_velocity',cached_phase_division_direction(v['clock'],expand(v['X'],(Ellipsis,None)),draised,expand(dX,(Ellipsis,None)),keep,label+'_clock_normalization'))
 dpressureJ=put('pressure_current',neg(prod(expand(v['PX'],(Ellipsis,None)),v['clock'],expand(dPX,(Ellipsis,None)),dclock)))
 dr=put('relative_phase',mv(s['P'],s['phi'],direction['P'],direction['phi']));dhir=put('raised_relative_phase',mv(s['hi'],v['r'],direction['hi'],dr))
 drelative=put('literal_relative_current_negative',mv((s['P'][0].transpose(0,2,1),s['P'][1].transpose(0,2,1)),v['hi_r'],(direction['P'][0].transpose(0,2,1),direction['P'][1].transpose(0,2,1)),dhir))
 dJ=put('literal_current',sub(dpressureJ,drelative));dregisteredJ=put('registered_current',sub(dpressureJ,dhir));ddensity=put('density',prod(c['N'],c['mu'],direction['N'],direction['mu']))
 dp=put('literal_canonical_density',prod(v['density'],sl(v['J'],(slice(None),0)),ddensity,sl(dJ,(slice(None),0))))
 dregisteredp=put('registered_canonical_density',prod(v['density'],sl(v['registered_J'],(slice(None),0)),ddensity,sl(dregisteredJ,(slice(None),0))))
 n0=sl(v['clock'],(slice(None),0));dn0=sl(dclock,(slice(None),0));dn02=put('clock_time_square',prod(n0,n0,dn0,dn0));dPXoverX=div('PX_over_X',v['X'],dPX,dX)
 h00=sl(s['hi'],(slice(None),0,0));dh00=sl(direction['hi'],(slice(None),0,0))
 dpressureH=put('pressure_temporal_H',sub(prod(v['PXX'],v['n02'],dPXX,dn02),prod(v['PX_over_X'],add(h00,v['n02']),dPXoverX,add(dh00,dn02))))
 p0=sl(s['P'],(slice(None),slice(None),0));dp0=sl(direction['P'],(slice(None),slice(None),0));dhp0=put('inverse_projector_time_column',mv(s['hi'],p0,direction['hi'],dp0));dA00=put('literal_relative_temporal_coefficient',dot(p0,v['hp0'],dp0,dhp0))
 dH=put('literal_temporal_H',prod(v['density'],sub(v['pressureH'],v['A00']),ddensity,sub(dpressureH,dA00)))
 dregisteredH=put('registered_temporal_H',prod(v['density'],sub(v['pressureH'],sl(v['hp0'],(slice(None),0))),ddensity,sub(dpressureH,sl(dhp0,(slice(None),0)))))
 dIu=mv(c['ih'],c['u'],direction['ih'],direction['u']);db=put('spatial_native_norm_b',fy_sum(add(z((p,3)),mul(c['u'],dIu)),-1))
 dreducednum=prod(c['mu'],sub(v['PXX'],v['b']),direction['mu'],sub(dPXX,db));dreduced=div('reduced_H',c['N'],dreducednum,direction['N'])
 delta=dict(X2=dX2,X=dX,q=dq,u=du,s=ds,pressure=dpressure,PX=dPX,PXX=dPXX,J=dJ,registered_J=dregisteredJ,p=dp,registered_p=dregisteredp,H=dH,registered_H=dregisteredH,reduced_H=dreduced,density=ddensity,current_gap=sub(dJ,dregisteredJ),density_gap=sub(dp,dregisteredp),hessian_gap=sub(dH,dregisteredH),reduced_gap=sub(dH,dreduced))
 for n,a in delta.items():fy_keep(label+'_completed_NEW_delta_'+n,a,keep)
 fy_keep(label+'_NEW_clock_square_construction_contact',add(prod(v['X'],v['X'],dX,dX),dot(s['phi'],v['raised'],direction['phi'],draised)),keep)
 dconstructed=add(z((p,4,4)),prod(expand(s['uc'],(Ellipsis,slice(None),None)),expand(s['U'],(Ellipsis,None,slice(None))),expand(direction['uc'],(Ellipsis,slice(None),None)),expand(direction['U'],(Ellipsis,None,slice(None)))))
 fy_keep(label+'_NEW_supplied_minus_constructed_projector_contact',sub(direction['P'],dconstructed),keep)
 values={n:v[n] for n in delta};values.update(current_gap=v['current_gap'],density_gap=v['density_gap'],hessian_gap=v['hessian_gap'],reduced_gap=v['reduced_gap'])
 return dict(value=values,delta=delta,PXXX=v['PXXX'],cached_intermediates=v,constants=prepared['constants'],chain_gaps=chain,candidate_pressure_recomputed_from_invariant=True,candidate_provenance=prepared['candidate_provenance'],new_direction_scope='gauge N/beta at fixed spatial geometry and current mechanical/phase rates',EOS_primal_log_or_current_recomputed=False,old_temporal_direction_reused=False,physical_adoption=False)


def candidate_gauge_registered_current_column(column,direction,keep,label):
 assert not GAUGE_CURRENT_AUTHOR_DRAFT and not GAUGE_CURRENT_AUTHORING_IN_PROGRESS
 assert column['same_candidate_provenance'] and column['gauge_target_derivative_zero'] is True and column['physical_adoption'] is False
 assert set(direction)=={'N','beta','N_jets','beta_jets'}
 candidate=column['candidate'];p=len(candidate['c']['N']);zero=lambda shape:P.a_dd(np.zeros(shape))
 full=dict(h=zero((p,3,3)),h_spatial_jets=zero((p,2,3,3)),h_dot=zero((p,3,3)),u_jets=zero((p,4,3)),z_jets=zero((32,p,4,3)),**direction)
 contact=candidate_gauge_raw_action_contact(candidate,column['geometry'],column['gauge'],column['covectors'],column['mechanical'],full,column['reference'],keep,label+'_NEW_gauge_mechanical')
 prepared=column['phase'];assert prepared['physical_adoption'] is False
 for n in ('hi','U','uc','P'):
  fy_keep(label+'_same_phase_'+n,prepared['s'][n],keep);assert all(np.array_equal(a,b) for a,b in zip(prepared['s'][n],P.a_dd(candidate['s'][n])))
 for n,raw in (('N','N'),('mu','sqrt_h'),('ih','ih'),('u','u')):
  fy_keep(label+'_same_phase_'+n,prepared['c'][n],keep);assert all(np.array_equal(a,b) for a,b in zip(prepared['c'][n],P.a_dd(candidate['c'][raw])))
 phase_direction={n:contact['d'][n] for n in ('hi','U','uc','P')};phase_direction['phi']=zero((p,4))
 phase_direction.update({n:contact['dc'][n] for n in ('N','mu','ih','u')})
 phase=candidate_cached_phase_gauge_contact(prepared,phase_direction,keep,label+'_NEW_literal_phase')
 current={'native':candidate['momenta']['native_density'],'metric':candidate['momenta']['metric_total_density'],'phase':phase['value']['p']}
 delta={'native':contact['delta_momenta']['native_density'],'metric':contact['delta_momenta']['metric_total_density'],'phase':phase['delta']['p']}
 for family,values in (('copied_current_point',current),('NEW_gauge_point_contact',delta)):
  for n,x in values.items():fy_keep(label+'_'+family+'_'+n,x,keep)
 for n,x in (('q',contact['d']['g']),('eta',contact['d']['U']),('zeta',contact['d']['z']),('q_first',contact['d']['dg']),('eta_first',contact['d']['du']),('zeta_first',contact['d']['dz'])):fy_keep(label+'_direct239_gauge_'+n,x,keep)
 return dict(current_point=current,canonical_point_contact=delta,mechanical=contact,phase=phase,same_candidate_provenance=column['same_candidate_provenance'],gauge_target_derivative_zero=True,
             gauge_coordinate_order=('value','R','Z','t'),phase_charge_target_unchanged=True,registered_mechanical_and_literal_phase_current_only=True,
             fullweak_transpose_assembled=False,Schwarz_or_literal_action_gradient_bridge_earned=False,canonical_or_normal_or_physical_admission=False,physical_adoption=False)


def candidate_gauge_registered_current_coefficients(column,keep,label,test_complete=None):
 assert not GAUGE_CURRENT_AUTHOR_DRAFT and not GAUGE_CURRENT_AUTHORING_IN_PROGRESS
 p=len(column['candidate']['c']['N']);zero=lambda shape:P.a_dd(np.zeros(shape))
 out={'native':zero((p,99,4,4)),'metric':zero((p,6,4,4)),'phase':zero((p,4,4))};refs=[]
 for row in range(4):
  for jet,coordinate in enumerate((None,1,2,0)):
   direction={'N':zero((p,)),'beta':zero((p,3)),'N_jets':zero((p,4)),'beta_jets':zero((p,4,3))}
   target=direction['N' if row==0 else 'beta'] if coordinate is None else direction['N_jets' if row==0 else 'beta_jets']
   index=(slice(None),) if row==0 and coordinate is None else (slice(None),row-1) if coordinate is None else (slice(None),coordinate) if row==0 else (slice(None),coordinate,row-1)
   target[0][index]=1.
   for n,x in direction.items():fy_keep(label+'_row%d_jet%d_supplied_gauge_'%(row,jet)+n,x,keep)
   part=candidate_gauge_registered_current_column(column,direction,keep,label+'_row%d_jet%d'%(row,jet))
   for n,x in part['canonical_point_contact'].items():
    index=(slice(None),row,jet) if n=='phase' else (slice(None),slice(None),row,jet)
    for w in (0,1):out[n][w][index]=x[w]
    fy_keep(label+'_completed_'+n+'_gauge_coefficient_inventory',out[n],keep)
   if test_complete is not None:refs.append(test_complete(row,jet,part))
 return dict(coefficients=out,completed_test_refs=refs,same_candidate_provenance=column['same_candidate_provenance'],gauge_target_derivative_zero=True,
             gauge_row_order=('N','beta_R','beta_Z','beta_phi'),gauge_coordinate_order=('value','R','Z','t'),all16_gauge_ports_retained=True,
             original_native_E_metric_F_and_phase_scalar_scatter_external=True,time_primary_coefficients_external=True,
             C_equals_minus_Rv_transpose_assumed=False,uniform_DD_or_global_inverse_or_physical_admission=False,physical_adoption=False)



def candidate_whole_gauge_registered_current_coefficients(columns,basis,keep,label,test_complete,column_complete):
 assert not GAUGE_CURRENT_AUTHOR_DRAFT and not GAUGE_CURRENT_AUTHORING_IN_PROGRESS
 assert len(columns)==4 and basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44)
 assert callable(test_complete) and callable(column_complete),'Every NEW full-column/test transaction must seal before the next'
 parts=[];refs=[]
 for iq,column in enumerate(columns):
  assert np.array_equal(column['candidate']['s']['R'],basis['R'][iq])
  part=candidate_gauge_registered_current_coefficients(column,keep,label+'_column%d'%iq,lambda row,jet,result:test_complete(iq,row,jet,result))
  parts.append(part);refs.append(column_complete(iq,part))
 return dict(columns=parts,completed_column_refs=refs,gauge_row_order=('N','beta_R','beta_Z','beta_phi'),gauge_coordinate_order=('value','R','Z','t'),
             all_four_quadrature_sections_and16_gauge_ports_retained=True,canonical_targets_and_current_values_unchanged=True,
             native_E_metric_F_scalar_left_scatter_and_normal_right_test_polynomial_external=True,
             represented_forward_block_only=True,C_equals_minus_Rv_transpose_assumed=False,global_inverse_or_physical_adoption=False,physical_adoption=False)
