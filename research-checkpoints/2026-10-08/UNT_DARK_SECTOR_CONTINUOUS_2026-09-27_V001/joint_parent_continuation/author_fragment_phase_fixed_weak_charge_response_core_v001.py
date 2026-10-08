# Definitions only. Globals np, P (exact DD-node provider), K (repaired72 phase core).
# Caller admits positive literal H, its diagonal, geometry and unchanged -Qphi first.
# Numerical cap/cycles are explicit caller inputs; no budget or physical step chosen here.
def phase_response_pack(x):
 assert x[0].shape==x[1].shape==(87,45)
 mask=P.scalar_mask();assert np.count_nonzero(mask)==3870
 return x[0][mask],x[1][mask]

def phase_response_unpack(x):
 assert x[0].shape==x[1].shape==(3870,)
 mask=P.scalar_mask();out=P.a_dd(np.zeros((87,45)))
 for w in (0,1):out[w][mask]=x[w]
 return out

def phase_response_keep(name,x,keep):
 keep(name+'_hi',x[0]);keep(name+'_lo',x[1]);return x

def phase_response_scalar_jets(x,g,keep,label):
 assert x[0].shape==x[1].shape==(87,45)
 y=tuple(P.scalar_lift(a) for a in x);out={}
 for jet,name in enumerate(('value','R','Z')):
  value=P.a_dd(np.zeros((4,86,44)))
  for iq in range(4):
   for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
    term=P.a_mul64(g['hats'][iq,corner,jet],P.a_slice(y,(slice(di,86+di),slice(dj,44+dj))))
    v=P.a_add(P.a_slice(value,iq),term);value[0][iq]=v[0];value[1][iq]=v[1]
    phase_response_keep(label+'_'+name+'_partial',value,keep)
  out[name]=P.a_reshape(value,(15136,));phase_response_keep(label+'_'+name,out[name],keep)
 return out

def phase_response_certificate(nodes,rhs,H,g,scale,keep,label):
 field=phase_response_unpack(nodes);phase_response_keep(label+'_nodal_velocity',field,keep)
 full=K.phase_mass_action(field,H,g,keep,label+'_original_phase_mass')
 action=phase_response_pack(full);phase_response_keep(label+'_action',action,keep)
 res=P.a_sub(rhs,action);phase_response_keep(label+'_residual',res,keep)
 f=rhs[0]+rhs[1];r=res[0]+res[1]
 assert f.shape==r.shape==scale.shape==(3870,) and np.all(scale>0)
 fn=float(np.linalg.norm(f));fs=float(np.linalg.norm(f/scale));rn=float(np.linalg.norm(r));rs=float(np.linalg.norm(r/scale))
 assert np.all(np.isfinite((fn,fs,rn,rs)))
 if fn==0:
  assert fs==0 and np.all(rhs[0]==0)&np.all(rhs[1]==0)
  ratios=np.array((0. if rn==0 else np.inf,0. if rs==0 else np.inf))
 else:
  assert fs>0;ratios=np.array((rn/fn,rs/fs))
 keep(label+'_original_raw_and_scaled_ratios',ratios)
 return res,ratios,action

def phase_response_solve(H,diagonal,rhs_full,g,keep,label,cap,max_cycles):
 assert isinstance(cap,int) and cap>0 and isinstance(max_cycles,int) and max_cycles>0 and P.LINEAR_TOL==1e-10
 assert H[0].shape==H[1].shape==(15136,) and np.all(H[0]>abs(H[1]))
 diag=phase_response_pack(diagonal);assert np.all(diag[0]>abs(diag[1]))
 scale=np.sqrt(diag[0]+diag[1]);keep(label+'_new_phase_positive_scale',scale)
 rhs=phase_response_pack(rhs_full);phase_response_keep(label+'_original_phase_rhs',rhs,keep)
 nodes=P.a_dd(np.zeros(3870));res=rhs;ratios=np.array((0.,0.)) if np.all(rhs[0]==0)&np.all(rhs[1]==0) else np.array((np.inf,np.inf));history=[]
 for cycle in range(1,max_cycles+1):
  if np.all(ratios<=P.LINEAR_TOL):break
  prefix=label+'_cycle_%03d'%cycle;start=(nodes[0].copy(),nodes[1].copy());last={}
  def action(delta):
   full=K.phase_mass_action(phase_response_unpack(P.a_dd(delta)),H,g,keep,prefix+'_correction_mass')
   packed=phase_response_pack(full);return packed[0]+packed[1]
  def certificate(delta):
   updated,q3=P.dd_node_update(start,delta,keep,prefix+'_trial_update')
   rr,rat,aa=phase_response_certificate(updated,rhs,H,g,scale,keep,prefix+'_trial')
   last.clear();last.update(delta=delta.copy(),nodes=updated,compression=q3,residual=rr,ratios=rat,action=aa)
   return rr[0]+rr[1],rat
  floating_rhs=res[0]+res[1];keep(prefix+'_rounded_recurrence_rhs',floating_rhs)
  delta,rat,admitted,reason=P.minres_core(action,floating_rhs,scale,1e-10,certificate,prefix,cap=cap)
  assert np.array_equal(last['delta'],delta) and np.array_equal(rat,last['ratios'])
  nodes=last['nodes'];res=last['residual'];ratios=last['ratios'];phase_response_keep(prefix+'_final_nodes',nodes,keep)
  phase_response_keep(prefix+'_final_original_residual',res,keep);phase_response_keep(prefix+'_final_original_action',last['action'],keep)
  keep(prefix+'_third_word_update_defect',last['compression']);history.append(dict(cycle=cycle,cap=cap,reason=reason,admitted=bool(admitted),original_ratios=ratios.tolist()))
 field=phase_response_unpack(nodes);jets=phase_response_scalar_jets(field,g,keep,label+'_phase_velocity_increment')
 return dict(nodal_pair=field,jet_pairs=jets,original_residual=res,original_ratios=ratios,linearized_weak_charge_response_admitted=bool(np.all(ratios<=P.LINEAR_TOL)),history=history,finite_phase_charge_restored=False,configuration_adopted=False,baseline_mixed_jets_replaced=False)
