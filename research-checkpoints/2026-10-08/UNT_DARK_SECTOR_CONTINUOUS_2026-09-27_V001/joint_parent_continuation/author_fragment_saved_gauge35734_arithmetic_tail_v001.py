"""HELD closed35734 saved-quotient tail and43 unstarted gauge ports.
Definitions only. No old20 ports/80 controls, primal EOS/current or full prefix replay.
Globals np/P/json/bind, exact fy11/fs20/fc/compact123/286 definitions, same repaired
arithmetic SCOPE and containing-owned immutable CACHE hydration/read/checkpoints.
Root proof is mandatory before any survivor array decoding or arithmetic.
"""
GAUGE35734_TAIL_AUTHOR_DRAFT=True
GAUGE35734_TAIL_AUTHORING_IN_PROGRESS=False
GAUGE35734_ROOT_ADMISSION_PROOF=(None,None,None)
GAUGE35734_PARENT_SOURCE=('cross_u_candidate_gauge_registered_current_controls_v002.py','e908868e63f2c2981b01a68bc1fdfd0fe063885ff6e4ed02b7f91d0eb7b5564c')
GAUGE35734_RAW_SOURCE=('author_fragment_candidate_gauge_registered_current_contact_v001.py','ac0502f41c6ad04208f5ef5610d43b3e11064a4b66eb73d076d43c959ffb0cdd')
GAUGE35734_SOURCE_MAP=('OBSERVER_GAUGE35734_ARITHMETIC_STAGE_CONTINUATION_SOURCE_MAP_V002.json','db7caf0e386cfc1276ec555c7157a6eb70bf7386cef5687eb3eb6f05368a5721')
GAUGE35734_SURVIVOR_AUDIT=('OBSERVER_GAUGE35734_SELECTED_SURVIVOR_BYTE_HEADER_AUDIT_V001.json','e27d847dd39e46b0d52171dd2bdae82bedde5924c531e33f0985fcf8dd120be3')


def gauge35734_tail_admission():
 assert not GAUGE35734_TAIL_AUTHOR_DRAFT and not GAUGE35734_TAIL_AUTHORING_IN_PROGRESS
 assert all(x is not None for x in GAUGE35734_ROOT_ADMISSION_PROOF),'Root independent survivor/earned-role admission required'
 for q in (GAUGE35734_PARENT_SOURCE,GAUGE35734_RAW_SOURCE,GAUGE35734_SOURCE_MAP,GAUGE35734_SURVIVOR_AUDIT,GAUGE35734_ROOT_ADMISSION_PROOF):bind(q[0],q[1])
 proof=json.loads(P.path(GAUGE35734_ROOT_ADMISSION_PROOF[0]).read_text());audit=json.loads(P.path(GAUGE35734_SURVIVOR_AUDIT[0]).read_text());mapping=json.loads(P.path(GAUGE35734_SOURCE_MAP[0]).read_text())
 assert proof['status']==GAUGE35734_ROOT_ADMISSION_PROOF[2] and proof['owner']==mapping['parent']['owner'] and proof['owner']['pid']==35734 and proof['owner']['source_sha256']==GAUGE35734_PARENT_SOURCE[1]
 assert proof['naturally_closed'] is True and proof['exit_code']==1 and proof['all30_committed_role_seals_verified'] is True
 assert proof['original80_controls_passed_and_preserved'] is True and proof['root_authorized_selected_survivor_arithmetic_tail_only'] is True
 assert proof['survivor_audit_sha256']==GAUGE35734_SURVIVOR_AUDIT[1] and proof['orphan_sha256']==audit['orphan_sha256']
 assert audit['selected_member_count']==118 and audit['orphan_mode']=='0444' and audit['numeric_arrays_decoded'] is audit['numerical_functions_executed'] is audit['orphan_or_role_admitted'] is False
 assert len(proof['cache_by_column'])==4 and proof['physical_adoption'] is False
 return dict(proof=proof,audit=audit,mapping=mapping,root_proof=GAUGE35734_ROOT_ADMISSION_PROOF)


def gauge35734_restore_tail_selection(admitted,column,read_member,selection_complete,keep,label):
 assert admitted['root_proof']==GAUGE35734_ROOT_ADMISSION_PROOF and callable(read_member) and callable(selection_complete)
 assert column['recovery_closed_cache_ref']==admitted['proof']['cache_by_column'][1]
 data={}
 for row in admitted['audit']['selected_members']:
  a=read_member(admitted['audit']['orphan_file'],row).copy();data[row['member']]=a;keep(label+'_copied_'+row['member'][:-4],a)
  assert a.dtype==np.float64 and list(a.shape)==row['shape'] and np.all(np.isfinite(a)),row['member']
 ref=selection_complete(data,dict(root_proof=GAUGE35734_ROOT_ADMISSION_PROOF,source_audit=GAUGE35734_SURVIVOR_AUDIT,orphan_NOT_promoted_to_old_COMMIT=True))
 assert isinstance(ref,dict) and ref
 members=dict(admitted['mapping']['restore_frame']['dual_variables']);prefix=admitted['mapping']['restore_frame']['member_prefix'];members['z']=[prefix+'z_'+s+'.npy' for s in ('hi','lo','delta_hi','delta_lo')]
 frame={n:((data[refs[0]],data[refs[1]]),(data[refs[2]],data[refs[3]])) for n,refs in members.items()}
 keys=admitted['mapping']['division_boundary']['saved_selectors'];division=dict(x=(data[keys[0]],data[keys[1]]),y=(data[keys[2]],data[keys[3]]),den=data[keys[4]],q1=data[keys[5]])
 assert all(np.array_equal(division['den'].view(np.uint64),division['y'][0].view(np.uint64)) for _ in (0,))
 assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(division['y'],(frame['gamma'][0][0][None,:,None],frame['gamma'][0][1][None,:,None])))
 return dict(frame=frame,division=division,selection_ref=ref,root_proof=admitted['root_proof'])


def gauge35734_resume_a_div64(x,den,q1,keep,label):
 assert not GAUGE35734_TAIL_AUTHOR_DRAFT and not GAUGE35734_TAIL_AUTHORING_IN_PROGRESS
 keep(label+'_saved_denominator',den.copy());keep(label+'_saved_first_quotient',q1.copy());assert np.all(np.isfinite(den)) and np.all(den!=0)
 r=P.a_sub(x,P.a_mul64(den,P.a_dd(q1)));keep(label+'_first_remainder_hi',r[0]);keep(label+'_first_remainder_lo',r[1])
 q2=(r[0]+r[1])/den;keep(label+'_second_quotient',q2);q=P.a_sum(q1,q2)
 r=P.a_sub(x,P.a_mul64(den,q));keep(label+'_second_remainder_hi',r[0]);keep(label+'_second_remainder_lo',r[1])
 q3=(r[0]+r[1])/den;keep(label+'_third_quotient',q3);q=P.a_add(q,P.a_dd(q3))
 residual=P.a_sub(x,P.a_mul64(den,q));keep(label+'_division_defect_hi',residual[0]);keep(label+'_division_defect_lo',residual[1]);keep(label+'_quotient_hi',q[0]);keep(label+'_quotient_lo',q[1])
 return q


def gauge35734_resume_first_fs_div(restored,column,keep,label):
 assert restored['root_proof']==GAUGE35734_ROOT_ADMISSION_PROOF and not GAUGE35734_TAIL_AUTHOR_DRAFT
 f=restored['frame'];d=restored['division'];x,y=d['x'],d['y'];assert np.all(abs(y[0])>abs(y[1]))
 q=gauge35734_resume_a_div64(x,d['den'],d['q1'],keep,label+'_value_initial_high_denominator')
 for step in range(2):
  r=fy_keep(label+'_value_current_remainder',P.a_sub(x,P.a_mul(y,q)),keep)
  dq=P.a_div64(r,y[0],keep,label+'_value_correction_'+str(step));q=fy_keep(label+'_value_current_quotient',P.a_add(q,dq),keep)
 fy_keep(label+'_value_final_division_residual',P.a_sub(x,P.a_mul(y,q)),keep);q=fy_keep(label+'_value_quotient',q,keep)
 # Only the previously unrecorded fs_mv(I,zi) DIRECTION temporary is rebuilt.
 zi=fs_dual(P.a_dd(column['candidate']['s']['z'][:,:,1:]));expanded=fs_expand(zi,(Ellipsis,None,slice(None)))
 delta_product=P.a_add(P.a_mul(f['ih'][1],expanded[0]),P.a_mul(f['ih'][0],expanded[1]));fy_keep(label+'_reconstructed_missing_direction_product',delta_product,keep)
 delta_numerator=fy_sum(delta_product,-1);fy_keep(label+'_reconstructed_missing_numerator_direction',delta_numerator,keep)
 denominator_direction=f['gamma'][1][0][None,:,None],f['gamma'][1][1][None,:,None]
 numerator=P.a_sub(delta_numerator,P.a_mul(q,denominator_direction));fy_keep(label+'_direction_numerator',numerator,keep)
 dq=fy_div(numerator,y,keep,label+'_direction')
 fy_keep(label+'_direction_division_residual',P.a_sub(P.a_add(P.a_mul(y,dq),P.a_mul(denominator_direction,q)),delta_numerator),keep)
 return q,dq


def gauge35734_raw_contact_tail(column,full,restored,first_completed,keep,label):
 assert not GAUGE35734_TAIL_AUTHOR_DRAFT and not GAUGE35734_TAIL_AUTHORING_IN_PROGRESS and restored['root_proof']==GAUGE35734_ROOT_ADMISSION_PROOF
 candidate=column['candidate'];geometry=column['geometry'];gauge=column['gauge'];covectors=column['covectors'];mechanical=column['mechanical'];reference=column['reference'];direction=full
 s,c=candidate['s'],candidate['c'];jets=candidate['jets'];p=len(c['N']);frame=restored['frame']
 put=lambda n,x:fs_keep(label+'_'+n,x,keep);anchor=lambda n,x,v:fc_anchor(label+'_'+n,x,v,keep);quotient=lambda n,a,b,v:fc_quotient(label+'_'+n,a,b,v,keep)
 h,I,mu,N,beta=(frame[n] for n in ('h','ih','sqrt_h','N','beta'));up,gamma,U,A,z=(frame[n] for n in ('up','gamma','U','A','z'))
 g,hi,dens,uc,projector,phi,Z,z2=(frame[n] for n in ('g','hi','dens','uc','P','phi','Z','z2'));N2,g2,g3,hb,JU,Jzz=(frame[n] for n in ('N2','g2','g3','hb','JU','Jzz'))
 ha,Na,ba=(frame[n] for n in ('h_first','N_first','beta_first'));u=fs_dual(P.a_dd(c['u']));zi=fs_dual(P.a_dd(s['z'][:,:,1:]));ua=fs_dual(covectors['u_jets']);za=fs_dual(covectors['z_jets']);ht=fs_dual(mechanical['h_dot'],direction['h_dot']);U0=fs_slice(U,(slice(None),0))
 e=np.zeros((6,3,3))
 for a,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):e[a,i,j]=e[a,j,i]=1.
 E=fs_dual(P.a_dd(e[None]))
 term=fs_sub(first_completed,fs_div(fs_mul(fs_expand(A,(Ellipsis,None)),fs_expand(up,(None,Ellipsis))),fs_expand(g3,(None,Ellipsis,None)),keep,label+'_JzU_second'))
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


def gauge35734_finish_lost_port(column,direction,restored,keep,label,tail_complete):
 assert restored['root_proof']==GAUGE35734_ROOT_ADMISSION_PROOF and callable(tail_complete)
 candidate=column['candidate'];p=len(candidate['c']['N']);zero=lambda shape:P.a_dd(np.zeros(shape))
 full=dict(h=zero((p,3,3)),h_spatial_jets=zero((p,2,3,3)),h_dot=zero((p,3,3)),u_jets=zero((p,4,3)),z_jets=zero((32,p,4,3)),**direction)
 first=gauge35734_resume_first_fs_div(restored,column,keep,label+'_NEW_gauge_mechanical_JzU_first');tail_complete('resumed_first_division',dict(value=first,selection_ref=restored['selection_ref']))
 contact=gauge35734_raw_contact_tail(column,full,restored,first,keep,label+'_NEW_gauge_mechanical');tail_complete('resumed_mechanical_tail',contact)
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


def gauge35734_unit_direction(p,row,jet):
 zero=lambda shape:P.a_dd(np.zeros(shape));direction=dict(N=zero((p,)),beta=zero((p,3)),N_jets=zero((p,4)),beta_jets=zero((p,4,3)));coordinate=(None,1,2,0)[jet]
 target=direction['N' if row==0 else 'beta'] if coordinate is None else direction['N_jets' if row==0 else 'beta_jets']
 index=(slice(None),) if row==0 and coordinate is None else (slice(None),row-1) if coordinate is None else (slice(None),coordinate) if row==0 else (slice(None),coordinate,row-1)
 target[0][index]=1.;return direction


def gauge35734_continue_remaining_ports(admitted,columns,restored,inventories,test_refs,column0_ref,keep,label,test_complete,column_complete,tail_complete):
 assert not GAUGE35734_TAIL_AUTHOR_DRAFT and not GAUGE35734_TAIL_AUTHORING_IN_PROGRESS and admitted['root_proof']==GAUGE35734_ROOT_ADMISSION_PROOF
 assert len(columns)==len(inventories)==len(test_refs)==4 and [len(r) for r in test_refs]==[16,4,0,0]
 assert all(columns[i]['recovery_closed_cache_ref']==admitted['proof']['cache_by_column'][i] for i in range(4))
 assert all(callable(x) for x in (test_complete,column_complete,tail_complete));column_refs=[column0_ref];new_ports=[]
 for iq in (1,2,3):
  column=columns[iq];p=len(column['candidate']['c']['N']);out=inventories[iq]
  for row in range(4):
   for jet in range(4):
    if iq==1 and row==0:continue
    direction=gauge35734_unit_direction(p,row,jet);tag=label+'_column%d_row%d_jet%d'%(iq,row,jet)
    for n,a in direction.items():fy_keep(tag+'_supplied_gauge_'+n,a,keep)
    part=gauge35734_finish_lost_port(column,direction,restored,keep,tag,tail_complete) if (iq,row,jet)==(1,1,0) else candidate_gauge_registered_current_column(column,direction,keep,tag)
    for n,x in part['canonical_point_contact'].items():
     index=(slice(None),row,jet) if n=='phase' else (slice(None),slice(None),row,jet)
     for w in (0,1):out[n][w][index]=x[w]
     fy_keep(tag+'_completed_'+n+'_gauge_coefficient_inventory',out[n],keep)
    ref=test_complete(iq,row,jet,part,out);assert isinstance(ref,dict) and ref;test_refs[iq].append(ref);new_ports.append((iq,row,jet))
  assert len(test_refs[iq])==16
  q=column_complete(iq,dict(coefficients=out,completed_test_refs=test_refs[iq],same_candidate_provenance=column['same_candidate_provenance'],gauge_target_derivative_zero=True,physical_adoption=False));assert isinstance(q,dict) and q;column_refs.append(q)
 assert len(new_ports)==44 and sum(len(r) for r in test_refs)==64
 return dict(completed_column_refs=column_refs,completed_test_refs=test_refs,lost_serialization_tail_reconstructed=True,earned20_port_bodies_and80_controls_replayed=False,genuinely_unstarted_ports_evaluated=43,original_missing_COMMIT_and_failed_ERROR_RAW_preserved=True,C_equals_minus_Rv_transpose_assumed=False,global_or_physical_adoption=False,physical_adoption=False)
