"""HELD NEW mechanical temporal action on closed candidate section0 support.
Globals np,P,fy_* and NEW160; completed candidate/inputs come only from69 restore.
Two original E/F arguments and their four support cells are fixed before payload.
No missing quadrature sections, old action, configuration or primal replay.
Transpose contacts are gates; raw/formal C*H*L antisymmetry is descriptive.
"""
SECTION_TEMPORAL_AUTHOR_DRAFT=True
SECTION_TEMPORAL_AUTHORING_IN_PROGRESS=False

def ms_keep(label,x,keep):
 assert isinstance(x,tuple) and len(x)==2 and x[0].shape==x[1].shape
 keep(label+'_both_words',np.stack(x).copy())
 for word,a in zip(('hi','lo'),x):keep(label+'_'+word,a)
 return x

def ms_point_selection(values,indices,mode_names=()):
 out={}
 for n,x in values.items():
  select=lambda a:np.take(a,indices,axis=1 if n in mode_names else 0) if (n in mode_names or (a.ndim and a.shape[0]==3784)) else a.copy()
  out[n]=tuple(select(a) for a in x) if isinstance(x,tuple) else select(x)
 return out

def ms_closed_support(bundle,basis,keep,label):
 ii,jj=basis['cell_i'],basis['cell_j'];assert ii.shape==jj.shape==(3784,) and bundle['column']==0
 indices=np.flatnonzero(np.isin(ii,(42,43))&np.isin(jj,(21,22)))
 assert len(indices)==4 and set(zip(ii[indices].tolist(),jj[indices].tolist()))=={(42,21),(42,22),(43,21),(43,22)}
 keep(label+'_fixed_support_indices',indices);keep(label+'_fixed_support_cells',np.column_stack((ii[indices],jj[indices])))
 c0=bundle['candidate'];s=ms_point_selection(c0['s'],indices,('z','z2','f'));c=ms_point_selection(c0['c'],indices,('JzU','zh'))
 jets=ms_point_selection(c0['jets'],indices,('dz',));features=ms_point_selection(c0['features']['paired'],indices,('dz','nz','q','V','D','V_raised','D_raised','Pi'))
 candidate=dict(s=s,c=c,jets=jets,features=dict(constants={n:s[n] for n in ('g','hi','U','z','P','uc','Z','r','z2','f','phi','omega','xi','w')},paired=features),momenta=ms_point_selection(c0['momenta'],indices),KADM=tuple(a[indices] for a in c0['KADM']),coefficient_envelopes=ms_point_selection(c0['coefficient_envelopes'],indices,('z','z2','f','JzU','zh')))
 inputs=bundle['inputs'];geometry=ms_point_selection(inputs[0],indices);gauge=ms_point_selection(inputs[2],indices)
 covectors=ms_point_selection(inputs[3],indices,('z','z_jets'));mechanical=ms_point_selection(inputs[4],indices);reference=ms_point_selection({n:x for n,x in inputs[7].items() if isinstance(x,tuple)},indices,('z','dz'))
 R=basis['R'][0].reshape(3784)[indices];dv=basis['dv'][0].reshape(3784)[indices];hats=basis['hats'][0,:,0].reshape(4,3784)[:,indices]
 assert np.array_equal(R,s['R']) and np.all(R>0) and np.all(dv>0) and np.all(hats>0)
 section=dict(indices=indices,i=ii[indices],j=jj[indices],R=R,dv=dv,hats=hats)
 for n,a in section.items():keep(label+'_section_'+n,a)
 return candidate,geometry,gauge,covectors,mechanical,reference,section

def ms_arguments(keep,label):
 out=[]
 tables=(
  (((0,0,1.),(0,1,.5),(1,0,2.),(17,2,-2.**-10)),(1.,0.,2.**-16,-2.**-8,2.**-12,1.)),
  (((0,0,-.5),(0,2,2.**-11),(1,1,-1.),(7,0,.75)),(-.5,2.**-12,-2.**-17,2.**-9,-2.**-13,2.)))
 for ordinal,(native,metric) in enumerate(tables):
  v=P.a_dd(np.zeros((33,3,87,45)));k=P.a_dd(np.zeros((6,87,45)))
  for mode,component,a in native:v[0][mode,component,43,22]=a;v[1][mode,component,43,22]=(ordinal+1)*a*2.**-60
  for slot,a in enumerate(metric):k[0][slot,43,22]=a;k[1][slot,43,22]=-(ordinal+1)*a*2.**-60
  assert all(np.all(a[~np.broadcast_to(P.native_mask(),a.shape)]==0) for a in v) and all(np.all(a[~P.metric_mask()]==0) for a in k)
  ms_keep(label+'_argument%d_native'%ordinal,v,keep);ms_keep(label+'_argument%d_metric'%ordinal,k,keep);out.append(dict(native=v,metric=k))
 return out

def ms_section_lift(argument,section,keep,label):
 v=tuple(P.lift_velocity(a) for a in argument['native']);k=tuple(P.lift_metric(a) for a in argument['metric']);q=len(section['R'])
 native=P.a_dd(np.zeros((q,33,3)));metric=P.a_dd(np.zeros((q,6)));F=P.dd_metric_F(section['R'])
 for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
  hat=section['hats'][corner];factor=np.column_stack((hat,hat,section['R']**2*hat))
  vp=tuple(np.moveaxis(a[:,:,section['i']+di,section['j']+dj],-1,0) for a in v);kp=tuple(a[:,section['i']+di,section['j']+dj].T for a in k)
  native=P.a_add(native,P.a_mul64(factor[:,None],vp));metric=P.a_add(metric,P.a_matvec(hat[:,None,None]*F,kp))
  ms_keep(label+'_native_corner%d_partial'%corner,native,keep);ms_keep(label+'_metric_corner%d_partial'%corner,metric,keep)
 native=tuple(a.reshape(q,99) for a in native);ms_keep(label+'_physical_native99',native,keep);ms_keep(label+'_physical_metric6',metric,keep)
 return dict(native=native,metric=metric)

def ms_direct_polynomial(argument,section,keep,label):
 # Separate F and hat products, independently explicit physical-six formulas.
 v=tuple(P.lift_velocity(a) for a in argument['native']);k=tuple(P.lift_metric(a) for a in argument['metric']);q=len(section['R'])
 native=P.a_dd(np.zeros((q,33,3)));coeff=P.a_dd(np.zeros((q,6)))
 for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
  h=section['hats'][corner];vp=tuple(np.moveaxis(a[:,:,section['i']+di,section['j']+dj],-1,0) for a in v);kp=tuple(a[:,section['i']+di,section['j']+dj].T for a in k)
  term=P.a_mul64(h[:,None,None],vp)
  # Apply the original native azimuthal polynomial as a distinct DD product.
  az=P.a_mul64(section['R'][:,None]**2,P.a_slice(term,(slice(None),slice(None),2)))
  for word in (0,1):term[word][:,:,2]=az[word]
  native=P.a_add(native,term);coeff=P.a_add(coeff,P.a_mul64(h[:,None],kp))
 R=section['R'];a,b,c,d,e,f=[P.a_slice(coeff,(slice(None),i)) for i in range(6)]
 metric=P.a_stack((P.a_add(a,P.a_mul64(R**2,b)),f,P.a_mul64(R**2,a),P.a_mul64(R,d),P.a_mul64(R**3,c),P.a_mul64(R**2,e)),-1)
 native=tuple(a.reshape(q,99) for a in native)
 return dict(native=ms_keep(label+'_independent_native_polynomial',native,keep),metric=ms_keep(label+'_independent_metric_polynomial',metric,keep))

def ms_rate_envelopes(candidate,physical,keep,label):
 e=candidate['coefficient_envelopes'];s,c=candidate['s'],candidate['c'];q=len(c['N'])
 assert np.all(c['N']>0) and np.all(c['gamma']>0) and all(np.all(a>=0) for a in e.values())
 v=(abs(physical['native'][0])+abs(physical['native'][1])).reshape(q,33,3);ut=v[:,0];zt=v[:,1:].transpose(1,0,2)
 k=abs(physical['metric'][0])+abs(physical['metric'][1]);ht=np.zeros((q,3,3))
 for slot,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):ht[:,i,j]=ht[:,j,i]=k[:,slot]
 dI=np.einsum('pij,pjk,pkl->pil',e['ih'],ht,e['ih']);up=np.einsum('pij,pj->pi',dI,e['u'])+np.einsum('pij,pj->pi',e['ih'],ut)
 gamma=(np.einsum('pi,pi->p',ut,e['up'])+np.einsum('pi,pi->p',e['u'],up))/(2*c['gamma']);U0=gamma/c['N']
 du=np.column_stack((U0,up+e['beta']*U0[:,None]));A=np.einsum('pi,jpi->jp',e['up'],e['z'][:,:,1:])
 dA=np.einsum('pi,jpi->jp',up,e['z'][:,:,1:])+np.einsum('pi,jpi->jp',e['up'],zt)
 z0=np.einsum('pi,jpi->jp',e['beta'],zt)+c['N'][None]*dA/c['gamma'][None]+c['N'][None]*A*gamma[None]/c['gamma'][None]**2
 dz=np.concatenate((z0[:,:,None],zt),2);dg=np.zeros((q,4,4,4));dg[:,0,1:,1:]=ht
 dg[:,0,0,1:]=dg[:,0,1:,0]=np.einsum('pij,pj->pi',ht,e['beta']);dg[:,0,0,0]=np.einsum('pi,pij,pj->p',e['beta'],ht,e['beta'])
 Ga=np.zeros((q,4,4,4))
 for a in range(4):
  for b in range(4):Ga[:,:,a,b]=.5*np.einsum('plm,pm->pl',e['hi'],dg[:,a,b]+dg[:,b,a]+dg[:,:,a,b])
 nu=np.einsum('pl,pbal->pab',e['U'],Ga);nu[:,0]+=du
 nz=np.einsum('jpl,plab->jpab',e['z'],Ga);nz[:,:,0]+=dz
 qq=np.einsum('pa,jpab->jpb',e['U'],nz);V=np.einsum('pab,jpb->jpa',e['P'],qq);D=np.einsum('pab,jpbc,pdc->jpad',e['P'],nz,e['P'])
 lower=np.einsum('pak,pkb->pab',nu,e['g']);FF=lower+lower.swapaxes(-1,-2)
 Vu=np.einsum('pab,jpb->jpa',e['hi'],V);Du=np.einsum('pab,jpbc,pcd->jpad',e['hi'],D,e['hi'])
 Pi=e['w'][:,None,None,None]*(e['U'][None,:,:,None]*Vu[:,:,None,:]/s['omega'][:,None,None,None]**2+P.ELL**2*Du)
 PiU=abs(P.ALPHA)*np.einsum('pab,pbc->pac',e['hi'],FF);sym=.5*(Pi+Pi.swapaxes(-1,-2));Klo=np.einsum('jpl,jpab->plab',e['z'],sym)
 Kup=np.einsum('plm,pmab->plab',e['hi'],Klo);CC=.5*(Kup.transpose(0,2,1,3)+Kup.transpose(0,2,3,1)+Kup)
 Fu=np.einsum('pab,pbc,pcd->pad',e['hi'],FF,e['hi']);CC+=abs(P.ALPHA)/2*(Fu[:,:,:,None]*e['U'][:,None,None,:]+Fu[:,:,None,:]*e['U'][:,None,:,None])
 pu=np.einsum('pab,pa->pb',e['JU'],PiU[:,0])+np.einsum('jpb,jp->pb',e['JzU'],Pi[:,:,0,0]);pz=Pi[:,:,0,1:]+e['Jzz'][None]*Pi[:,:,0,0,None]
 native=e['dens'][:,None]*np.concatenate((pu[:,None],pz.transpose(1,0,2)),1).reshape(q,99)
 metric_native=e['dens'][:,None]*(np.einsum('pqa,pa->pq',e['Uh'],PiU[:,0])+np.einsum('pqab,pab->pq',e['embed'],CC[:,0])+np.einsum('jpq,jp->pq',e['zh'],Pi[:,:,0,0]))
 dK=e['N'][:,None,None]*Ga[:,0,1:,1:];trace=np.einsum('pij,pij->p',e['ih'],dK)
 EH=e['sqrt_h'][:,None,None]/(2*P.C)*(np.einsum('pij,pjk,pkl->pil',e['ih'],dK,e['ih'])+trace[:,None,None]*e['ih'])
 metric_EH=np.stack([EH[:,i,j] if i==j else EH[:,i,j]+EH[:,j,i] for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],-1)
 out=dict(native=native,metric_native=metric_native,metric_EH=metric_EH,metric=metric_native+metric_EH)
 for n,a in out.items():keep(label+'_uncancelled_'+n,a)
 return out

def ms_temporal_point_action(candidate,inputs,physical,keep,label):
 q=len(candidate['c']['N']);v=tuple(a.reshape(q,33,3) for a in physical['native']);u=P.a_dd(np.zeros((q,4,3)));z=P.a_dd(np.zeros((32,q,4,3)));ht=P.a_dd(np.zeros((q,3,3)))
 for word in (0,1):u[word][:,0]=v[word][:,0];z[word][:,:,0]=v[word][:,1:].transpose(1,0,2)
 for slot,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
  for word in (0,1):ht[word][:,i,j]=ht[word][:,j,i]=physical['metric'][word][:,slot]
 direction=dict(h=P.a_dd(np.zeros((q,3,3))),h_spatial_jets=P.a_dd(np.zeros((q,2,3,3))),h_dot=ht,u_jets=u,z_jets=z)
 for n,x in direction.items():ms_keep(label+'_NEW_direction_'+n,x,keep)
 contact=finite_candidate_configuration_contact(candidate,*inputs[:4],direction,inputs[4],keep,label+'_NEW160_temporal')
 for n in ('g','hi','U','z','P','phi'):assert all(np.all(a==0) for a in contact['d'][n]),n
 moments=contact['delta_momenta'];out={n:ms_keep(label+'_NEW_point_'+n,moments[n+'_density'],keep) for n in ('native','metric_native','metric_EH','metric_total')}
 formal=ms_keep(label+'_formal_U_time',P.a_slice(contact['d']['du'],(slice(None),0)),keep)
 chart=P.a_add(P.a_matvec(candidate['c']['JU'],tuple(a[:,0] for a in v)),P.a_matvec(candidate['c']['Uh'].transpose(0,2,1),physical['metric']))
 ms_keep(label+'_formal_minus_canonical_primary_U_time',P.a_sub(formal,chart),keep)
 zz=P.a_dd(np.zeros((32,q)))
 for n,coef,arg in (('JzU',candidate['c']['JzU'],tuple(a[:,0][None] for a in v)),('Jzz',candidate['c']['Jzz'][None],tuple(a[:,1:].transpose(1,0,2) for a in v)),('zh',candidate['c']['zh'],tuple(a[None] for a in physical['metric']))):
  zz=P.a_add(zz,fy_sum(P.a_mul64(coef,arg),2));ms_keep(label+'_canonical_z_time_'+n+'_partial',zz,keep)
 chartz=P.a_stack([zz]+[tuple(a[:,1:,i].T for a in v) for i in range(3)],2)
 ms_keep(label+'_formal_minus_canonical_primary_z_time',P.a_sub(P.a_slice(contact['d']['dz'],(slice(None),slice(None),0)),chartz),keep)
 return dict(point=out,contact=contact,direction=direction)

def ms_section_scatter(point,envelope,section,keep,label):
 q=len(section['R']);n=P.a_dd(np.zeros((33,3,87,45)));m=P.a_dd(np.zeros((6,87,45)));en=np.zeros_like(n[0]);em=np.zeros_like(m[0]);R=section['R'];F=P.dd_metric_F(R);weight=section['dv']/R
 modes=tuple(a.reshape(q,33,3) for a in point['native']);emodes=envelope['native'].reshape(q,33,3)
 nw=P.a_mul64(weight[:,None,None],modes);mw=P.a_mul64(weight[:,None],P.a_matvec(F.swapaxes(-1,-2),point['metric_total']))
 enw=weight[:,None,None]*emodes;emw=weight[:,None]*np.einsum('pab,pa->pb',abs(F),envelope['metric'])
 for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
  hat=section['hats'][corner];factor=np.column_stack((hat,hat,R**2*hat));nv=P.a_mul64(factor[:,None],nw);mv=P.a_mul64(hat[:,None],mw)
  for p in range(q):
   key=(slice(None),slice(None),int(section['i'][p]+di),int(section['j'][p]+dj));updated=P.a_add(P.a_slice(n,key),P.a_slice(nv,p));n[0][key]=updated[0];n[1][key]=updated[1];en[key]+=enw[p]*abs(factor[p])[None]
   key=(slice(None),int(section['i'][p]+di),int(section['j'][p]+dj));updated=P.a_add(P.a_slice(m,key),P.a_slice(mv,p));m[0][key]=updated[0];m[1][key]=updated[1];em[key]+=emw[p]*abs(hat[p])
  ms_keep(label+'_native_corner%d_partial'%corner,n,keep);ms_keep(label+'_metric_corner%d_partial'%corner,m,keep)
 for component in (1,2):
  value=P.a_add(P.a_slice(n,(slice(None),component,1,slice(None))),P.a_slice(n,(slice(None),component,0,slice(None))));n[0][:,component,1]=value[0];n[1][:,component,1]=value[1];en[:,component,1]+=en[:,component,0]
 value=P.a_add(P.a_slice(m,(slice(None),1,slice(None))),P.a_slice(m,(slice(None),0,slice(None))));m[0][:,1]=value[0];m[1][:,1]=value[1];em[:,1]+=em[:,0]
 for a in (*n,en):a[:,:,0]=0.;a[:,1,:,0]=0.
 for a in (*m,em):a[:,0]=0.;a[3:5,:,0]=0.
 ms_keep(label+'_native_section_weak',n,keep);ms_keep(label+'_metric_section_weak',m,keep);keep(label+'_native_positive_scatter',en);keep(label+'_metric_positive_scatter',em)
 return dict(native=n,metric=m),dict(native=en,metric=em)

def ms_pairing(x,y,keep,label):
 assert x[0].shape==x[1].shape==y[0].shape==y[1].shape
 mask=(x[0]!=0)|(x[1]!=0);xs=tuple(a[mask] for a in x);ys=tuple(a[mask] for a in y)
 ms_keep(label+'_selected_left',xs,keep);ms_keep(label+'_selected_right',ys,keep)
 return ms_keep(label+'_sum',fy_sum(P.a_mul(xs,ys),0),keep)

def ms_transpose_contacts(argument,polynomial,result,section,keep,label,check):
 out={}
 for n,field in (('native','native'),('metric','metric_total')):
  nodal=ms_pairing(argument[n],result['weak'][n],keep,label+'_'+n+'_nodal')
  weighted=P.a_mul64((section['dv']/section['R'])[:,None],result['point'][field]);direct=ms_pairing(polynomial[n],weighted,keep,label+'_'+n+'_direct')
  gap=ms_keep(label+'_'+n+'_nodal_minus_direct',P.a_sub(nodal,direct),keep)
  bound=float(np.sum((abs(argument[n][0])+abs(argument[n][1]))*result['weak_envelope'][n])+np.sum((abs(polynomial[n][0])+abs(polynomial[n][1]))*result['point_envelope'][n]*(section['dv']/section['R'])[:,None]))
  keep(label+'_'+n+'_uncancelled_functional_envelope',np.asarray(bound));check(label+'_'+n+'_partial_section_polynomial_transpose',np.asarray(gap[0]+gap[1]),np.asarray(0.),np.asarray(bound));out[n]=direct
 return out

def ms_cross_bilinear_readout(arguments,polynomials,results,section,keep,label):
 matrix={};envelopes={};weight=(section['dv']/section['R'])[:,None]
 for family,test in (('native','native'),('metric_native','metric'),('metric_EH','metric')):
  rows=[];eb=np.zeros((2,2))
  for a in range(2):
   row=[]
   for b in range(2):
    point=results[b]['point'][family];row.append(ms_pairing(polynomials[a][test],P.a_mul64(weight,point),keep,label+'_%s_%d%d'%(family,a,b)))
    eb[a,b]=np.sum((abs(polynomials[a][test][0])+abs(polynomials[a][test][1]))*results[b]['point_envelope'][family]*weight)
   rows.append(P.a_stack(row,0))
  M=P.a_stack(rows,0);matrix[family]=ms_keep(label+'_'+family+'_cross_matrix',M,keep);envelopes[family]=eb
 total=P.a_add(matrix['native'],P.a_add(matrix['metric_native'],matrix['metric_EH']));matrix['total']=ms_keep(label+'_total_cross_matrix',total,keep);envelopes['total']=envelopes['native']+envelopes['metric_native']+envelopes['metric_EH']
 nodal=[];ne=np.zeros((2,2))
 for a in range(2):
  row=[]
  for b in range(2):
   terms=[ms_pairing(arguments[a][n],results[b]['weak'][n],keep,label+'_nodal_%s_%d%d'%(n,a,b)) for n in ('native','metric')]
   row.append(P.a_add(*terms));ne[a,b]=sum(float(np.sum((abs(arguments[a][n][0])+abs(arguments[a][n][1]))*results[b]['weak_envelope'][n])) for n in ('native','metric'))
  nodal.append(P.a_stack(row,0))
 matrix['nodal_total']=ms_keep(label+'_actual_nodal_total_cross_matrix',P.a_stack(nodal,0),keep);envelopes['nodal_total']=ne
 ms_keep(label+'_actual_nodal_minus_independent_polynomial_cross_matrix',P.a_sub(matrix['nodal_total'],total),keep);descriptors={}
 for family,M in matrix.items():
  anti=ms_keep(label+'_'+family+'_signed_antisymmetry',P.a_sub(P.a_slice(M,(0,1)),P.a_slice(M,(1,0))),keep);e=float(envelopes[family][0,1]+envelopes[family][1,0]);keep(label+'_'+family+'_uncancelled_cross_envelope',np.asarray(e))
  value=float(anti[0]+anti[1]);descriptors[family]=dict(signed_gap=value,uncancelled_envelope=e,normalized_gap=abs(value)/e if e>0 else None,zero_envelope_exact_gap_zero=value==0 if e==0 else None,symmetry_gate_applied=False)
 return dict(descriptors=descriptors,canonical_formal_map='C* H L; C=L not presumed',exact_Hessian_symmetry_or_coercivity_earned=False,missing_three_sections_fabricated=False,physical_adoption=False)
