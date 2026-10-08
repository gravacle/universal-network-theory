"""HELD unsigned NEW configuration-current/CMC contraction preparation.
Globals np,P and exact reviewed124 mp_add/mul/div/sum/mm/mv. No signed action,
feature, momentum, geometry, current or EOS body is invoked. Inputs are already
completed NEW160 d/dc, cached current primitive pairs and NEW195 stage contacts.
The envelope keeps uncancelled product-rule sides through123 left pullbacks and
160 own-spatial-measure EH. It is conditional on these actual stage operands,
not a bound for upstream chart/EFT errors or arbitrary DD linearity.
"""
CONFIGURATION_CURRENT_UNSIGNED_AUTHOR_DRAFT=True
CONFIGURATION_CURRENT_UNSIGNED_AUTHORING_IN_PROGRESS=False
CONFIGURATION_CURRENT_UNSIGNED_PINS={
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_finite_candidate_configuration_contact_v001.py':'7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41',
 'author_fragment_cached_updated_phase_compact_chi_contact_v001.py':'ba1f599b85c367320d601fee9d58ea885c17f08452a7935666472fccc2eafa10',
 'author_fragment_candidate_weak_mechanical_positive_v001.py':'8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94'}


def candidate_configuration_current_CMC_unsigned(candidate,contact,phase,eos,Hbar,keep,label):
 assert not CONFIGURATION_CURRENT_UNSIGNED_AUTHOR_DRAFT and not CONFIGURATION_CURRENT_UNSIGNED_AUTHORING_IN_PROGRESS
 s,c=candidate['s'],candidate['c'];F=candidate['features']['paired'];M=candidate['momenta'];d,dc=contact['d'],contact['dc'];p=len(c['N']);counter=0
 assert np.isfinite(Hbar) and Hbar>0 and p>=1
 def tag(name):
  nonlocal counter
  counter+=1;return label+'_%05d_'%counter+name
 def mag(x,name):
  assert isinstance(x,tuple) and len(x)==2 and x[0].shape==x[1].shape
  keep(tag(name+'_both_words'),np.stack(x).copy())
  assert all(a.dtype==np.float64 and np.all(np.isfinite(a)) for a in x)
  return mp_add(abs(x[0]),abs(x[1]),keep,tag(name+'_magnitude'))
 add=lambda a,b:mp_add(a,b,keep,tag('add'))
 mul=lambda a,b:mp_mul(a,b,keep,tag('mul'))
 div=lambda a,b:mp_div(a,b,keep,tag('div'))
 sum_=lambda a,axis:mp_sum(a,axis,keep,tag('sum'))
 mm=lambda a,b:mp_mm(a,b,keep,tag('mm'))
 mv=lambda a,b:mp_mv(a,b,keep,tag('mv'))
 outer=lambda a,b:mul(a[..., :,None],b[...,None,:])
 E={n:mag(d[n],'NEW_d_'+n) for n in ('g','hi','U','z','du','dz','Ga')}
 EC={n:mag(dc[n],'NEW_dc_'+n) for n in ('ih','JU','JzU','Jzz','Uh','zh','embed','dens','sqrt_h','log_dens')}
 for n in ('N','beta','u'):assert all(np.all(w==0) for w in dc[n]),'Fixed gauge and covariant spatial u required'
 assert all(np.all(w==0) for w in d['phi']) and eos['old_temporal_direction_reused'] is False
 EF={n:mag(F[n],'cached_feature_'+n) for n in ('nu','nz','q','V','D','F','Fup','V_raised','D_raised','Pi','PiU')}
 U,z,G,I,proj,uc,Z=(abs(s[n]) for n in ('U','z','g','hi','P','uc','Z'))
 duc=add(mv(E['g'],U),mv(G,E['U']));dproj=add(outer(duc,U),outer(uc,E['U']))
 dZ=np.zeros((p,4))
 for j in range(32):dZ=add(dZ,mul(abs(s['w'][j]),E['z'][j]))
 enu=E['du'].copy();enz=E['dz'].copy();Ga=mag(candidate['jets']['Ga'],'cached_Gamma')
 for l in range(4):
  enu=add(enu,add(mul(U[:,l,None,None],E['Ga'][:,:,:,l].transpose(0,2,1)),mul(E['U'][:,l,None,None],Ga[:,:,:,l].transpose(0,2,1))))
  enz=add(enz,add(mul(z[:,:,l,None,None],E['Ga'][:,l][None]),mul(E['z'][:,:,l,None,None],Ga[:,l][None])))
 eq=np.zeros((32,p,4))
 for a in range(4):eq=add(eq,add(mul(E['U'][None,:,a,None],EF['nz'][:,:,a]),mul(U[None,:,a,None],enz[:,:,a])))
 eV=add(mv(dproj,EF['q']),mv(proj,eq));eD=add(add(mm(mm(dproj,EF['nz']),proj.swapaxes(-1,-2)),mm(mm(proj,enz),proj.swapaxes(-1,-2))),mm(mm(proj,EF['nz']),dproj.swapaxes(-1,-2)))
 lower=add(mm(enu,G),mm(EF['nu'],E['g']));eF=add(lower,lower.swapaxes(-1,-2))
 eFu=add(add(mm(mm(E['hi'],EF['F']),I),mm(mm(I,eF),I)),mm(mm(I,EF['F']),E['hi']))
 eVu=add(mv(E['hi'],EF['V']),mv(I,eV));eDu=add(add(mm(mm(E['hi'],EF['D']),I),mm(mm(I,eD),I)),mm(mm(I,EF['D']),E['hi']))
 omega2=s['omega'][:,None,None,None]**2;keep(tag('source_rounded_omega_squared'),omega2.copy());assert np.all(omega2>0)
 ePi=mul(abs(s['w'])[:,None,None,None],add(div(add(outer(E['U'][None],EF['V_raised']),outer(U[None],eVu)),omega2),mul(abs(P.ELL**2),eDu)))
 ePiU=add(mul(abs(P.ALPHA),add(mm(E['hi'],EF['F']),mm(I,eF))),add(outer(E['U'],Z),outer(U,dZ)))
 sym=mul(.5,add(EF['Pi'],EF['Pi'].swapaxes(-1,-2)));dsym=mul(.5,add(ePi,ePi.swapaxes(-1,-2)));UU=outer(U,U);dUU=add(outer(E['U'],U),outer(U,E['U']));rows=[]
 for l in range(4):
  row=add(mul(dZ[:,l,None,None],UU),mul(Z[:,l,None,None],dUU))
  for j in range(32):row=add(row,add(mul(z[j,:,l,None,None],dsym[j]),mul(E['z'][j,:,l,None,None],sym[j])))
  rows.append(row)
 eKlo=np.stack(rows,axis=1);Klo=mag(M['connection_Klo'],'cached_connection_Klo');eKup=np.zeros((p,4,4,4))
 for m in range(4):eKup=add(eKup,add(mul(E['hi'][:,:,m,None,None],Klo[:,None,m]),mul(I[:,:,m,None,None],eKlo[:,None,m])))
 eCCn=mul(.5,add(add(eKup.transpose(0,2,1,3),eKup.transpose(0,2,3,1)),eKup))
 mx=lambda f,u:add(mul(f[:,:,:,None],u[:,None,None,:]),mul(f[:,:,None,:],u[:,None,:,None]))
 eMX=mul(abs(P.ALPHA/2),add(mx(eFu,U),mx(EF['Fup'],E['U'])));eCC=add(eCCn,eMX)
 PU,P00=EF['PiU'][:,0],EF['Pi'][:,:,0,0];dPU,dP00=ePiU[:,0],ePi[:,:,0,0];epu=np.zeros((p,3))
 for a in range(4):epu=add(epu,add(mul(abs(c['JU'][:,a]),dPU[:,a,None]),mul(EC['JU'][:,a],PU[:,a,None])))
 for j in range(32):epu=add(epu,add(mul(abs(c['JzU'][j]),dP00[j,:,None]),mul(EC['JzU'][j],P00[j,:,None])))
 epz=add(ePi[:,:,0,1:],add(mul(abs(c['Jzz'])[None],dP00[:,:,None]),mul(EC['Jzz'][None],P00[:,:,None])))
 e99=np.concatenate((epu,epz.transpose(1,0,2).reshape(p,96)),axis=1)
 enative=add(mul(abs(c['dens'])[:,None],e99),mul(EC['log_dens'][:,None],mag(M['native_density'],'cached_native_density')))
 epm=np.zeros((p,6));C0=mag(M['connection_momentum'],'cached_connection_momentum')[:,0]
 for a in range(4):
  epm=add(epm,add(mul(abs(c['Uh'][:,:,a]),dPU[:,a,None]),mul(EC['Uh'][:,:,a],PU[:,a,None])))
  for b in range(4):epm=add(epm,add(mul(abs(c['embed'][:,:,a,b]),eCC[:,0,a,b,None]),mul(EC['embed'][:,:,a,b],C0[:,a,b,None])))
 for j in range(32):epm=add(epm,add(mul(abs(c['zh'][j]),dP00[j,:,None]),mul(EC['zh'][j],P00[j,:,None])))
 emetric_native=add(mul(abs(c['dens'])[:,None],epm),mul(EC['log_dens'][:,None],mag(M['metric_native_density'],'cached_metric_native_density')))
 II=abs(c['ih']);K=mag(M['K'],'cached_KGamma');tau=mag(M['Ktrace'],'cached_KGamma_trace');eK=mul(abs(c['N'])[:,None,None],E['Ga'][:,0,1:,1:])
 etau=add(sum_(sum_(mul(EC['ih'],K),2),1),sum_(sum_(mul(II,eK),2),1))
 primal=add(mm(mm(II,K),II),mul(tau[:,None,None],II))
 derivative=add(add(add(mm(mm(EC['ih'],K),II),mm(mm(II,eK),II)),mm(mm(II,K),EC['ih'])),add(mul(etau[:,None,None],II),mul(tau[:,None,None],EC['ih'])))
 eEH=div(add(mul(EC['sqrt_h'][:,None,None],primal),mul(abs(c['sqrt_h'])[:,None,None],derivative)),abs(2*P.C))
 eEHsix=np.stack([mul(1. if i==k else 2.,eEH[:,i,k]) for i,k in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],axis=-1)
 emetric=add(emetric_native,eEHsix);eCMC=add(mul(EC['sqrt_h'],add(tau,abs(3*Hbar))),mul(abs(c['sqrt_h']),etau))
 v,ps,pc=phase['values'],phase['s'],phase['c'];D={**contact['d'],**contact['dc']};D['mu']=contact['dc']['sqrt_h']
 phi=mag(ps['phi'],'updated_phi');hi=mag(ps['hi'],'updated_phase_inverse');Pp=mag(ps['P'],'updated_phase_projector');dhi=mag(D['hi'],'NEW_phase_dhi');dP=mag(D['P'],'NEW_phase_dP')
 eX=mag(eos['delta']['X'],'NEW_cached_stage_delta_X');ePX=mag(eos['delta']['PX'],'NEW_cached_stage_delta_PX');clock=mag(v['clock'],'cached_literal_clock')
 X=v['X'];keep(tag('cached_clock_denominator_both'),np.stack(X).copy());lower=np.nextafter(X[0]-abs(X[1]),-np.inf);keep(tag('cached_clock_denominator_lower'),lower.copy());assert np.all(np.isfinite(lower)) and np.all(lower>0)
 eraised=mv(dhi,phi);eclock=div(add(eraised,mul(clock,eX[:,None])),lower[:,None]);epressure=add(mul(ePX[:,None],clock),mul(mag(v['PX'],'cached_PX')[:,None],eclock))
 er=mv(dP,phi);ehir=add(mv(dhi,mag(v['r'],'cached_literal_relative_phase')),mv(hi,er));erelative=add(mv(dP.swapaxes(-1,-2),mag(v['hi_r'],'cached_raised_relative_phase')),mv(Pp.swapaxes(-1,-2),ehir))
 eJ=add(epressure,erelative);e_density=mul(mag(pc['N'],'fixed_N'),mag(D['mu'],'NEW_formal_mu_contact'))
 ephase=add(mul(mag(v['density'],'cached_literal_density'),eJ[:,0]),mul(e_density,mag(v['J'],'cached_literal_current')[:,0]))
 mechanical=np.concatenate((enative,emetric),axis=1)
 out=dict(mechanical=mechanical,phase=ephase,CMC=eCMC)
 for n,a in out.items():keep(label+'_completed_source_unsigned_'+n,a.copy());assert np.all(np.isfinite(a)) and np.all(a>=0)
 return dict(fields=out,source_terms_before_output_cancellation=True,signed_response_magnitude_used_as_bound=False,actual_NEW_chart_and_EOS_stage_inputs_retained=True,normal_envelope_prepared=False,upstream_EFT_error_bound_qualified=False,source_input_association_or_uniform_Jacobian_qualified=False,physical_adoption=False)
