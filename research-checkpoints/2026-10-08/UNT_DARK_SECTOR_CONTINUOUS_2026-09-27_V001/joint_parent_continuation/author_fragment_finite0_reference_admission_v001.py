# Definitions only. Caller supplies path,bind,json,INPUTS; author never calls.
# Finite0 consumes saved fields/labels, then REBUILDS all candidate coefficients/action.
# Force seed time slots are obsolete: use ONLY spatial slots; current47969 supplies time.
FINITE0_PARENTS={
 'current':('CROSS_U_CANONICAL_NODAL_METRIC_RATE_DD_COORDINATES_V001', 47969, 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py', '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', '1f3c5afbb26dd9f43fcea053f92bfad073fdeb75221265d6212772125445e23e', '6979db89e7612ddda54e9b4cadaa565263b99d02c2eca24324a695e0fc92a2bc', 'a11e491baa8950d8dbedf5a0470aea1604cc0366e008fed8fc6154fd649f123d', 4, 9),
 'pilot':('CROSS_U_PAIRED_CURRENT_PRIMITIVE_MOMENTUM_READOUT_V002', 50104, 'cross_u_paired_current_primitive_momentum_readout_v002.py', 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', '0ccd71e96ff40c8105256fd9cce17b68ff06ad0292a726bd1ecac458d8bff30a', '7289a181e37a8f3277dfc7a587f09bf9078e1d20381eb0c0c371aac2511203be', '293295534b3c32ea152641ee4bd54b4cf224a171e3de9e14f2833759787eadaa', 18, 7),
 'force':('CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003', 36387, 'cross_u_weak_canonical_spatial_euler_loads_v003.py', '4f239074b5345709f493b3633f7dd376fa7ac97dbb23bf20825eabde2ed56b79', 'de6ae873e7cf783c4bdfbc20eeb0d5de82c27ea7dc709ba8832ed4c4ec7aba2b', '981a314d7ca598c101db34d4da6f36679c752da81d8cc1325c521f4ce0c7b770', '822c82d59631ebef6f87c0847829370792338a1dcb741c325843d1c8f07e3af2', 36, 8),
 'phase':('CROSS_U_PHASE_FIXED_WEAK_CHARGE_PREPARATION_V003', 59190, 'cross_u_phase_fixed_weak_charge_preparation_v003.py', 'ed18caa749cbbfef40956ee4764390d688aaf6a1567912317d6cc81c9851d079', 'a1f9b46ddb29879633eb38b099671ad762f0a8d4bcb8a4d12297035d586c111f', 'fefe9a83c871577653a3965d0c61ff869f6786ff0b1c9a943d9abf4fd6ee79d7', '9d2fb6e0a649976167144b0d428bc730800844d78670587ad8891b11ddfcca90', 6, 7),
 'mean':('CROSS_U_ONCE_COUNTED_ORDINARY_MEAN_WEAK_LOADS_V001', 56727, 'cross_u_once_counted_ordinary_mean_weak_loads_v001.py', '6c6f31a382f884e84d303aa617788eb90f46c78c44ebcfb789499a1771ff2cc9', '7a405ed8fa42c79073cce5adce0dd4081469d21615b8147190c49baf5b5286ec', '2b8d9e27d7fdafad1ce6369e5c9c01ad87bd1cff2880f57e053c6ca4e6eb5f8e', '9238701c16c637216c4d775bc74f8e2d66e578d5cc03fe3c9e6062ca97ca1120', 12, 6),
}
FINITE0_PROOFS={
 'current':('READONLY_DD_NODE_COORDINATE_WORDS_V001_RESULT.json', 'ce19e353075341a82b475f019cd3fb6ca6f630868001b479b5aee1760c9bb8fc', 'SAVED_DD_NODE_COORDINATE_WORDS_PASS'),
 'pilot':('READONLY_PAIRED_PRIMITIVE_CLOSURE_V002_RESULT.json', '5c3eba7c11f65c6c9449325f24683c8f3fde04a55dd684729d759431c7e771cf', 'SAVED_PAIRED_PRIMITIVE_CLOSURE_PASS'),
 'phase':('READONLY_LITERAL_PHASE_PREPARATION_CLOSURE_V001_RESULT.json', '0a07d01a07a5632b57fa3c7e58e73403ceb6fbfb32670d6fa546472b479c804b', 'SAVED_LITERAL_PHASE_PREPARATION_CLOSURE_PASS'),
 'mean':('READONLY_ONCE_COUNTED_MEAN_CLOSURE_V001_RESULT.json', '8e3b75822d70e58b56a0873f40463fc1a105376484c2192bc98fece02833ba1c', 'SAVED_ONCE_COUNTED_MEAN_CLOSURE_PASS'),
}
def finite0_reference_admission():
 assert all(all(x is not None for x in q) for q in FINITE0_PARENTS.values()) and all(all(x is not None for x in q) for q in FINITE0_PROOFS.values()),'Earned CLOSED parents and saved proofs required before I/O'
 def mapped(m,n):return m[n] if n in m else m[str(path(n).resolve())]
 def selected(q,m):
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert mapped(m,n)==h;bind(n,h)
  c=json.loads(path(q['commit_file']).read_text());assert c['file']==q['file'] and c['sha256']==q['sha256']
  if 'metadata' in q:assert c['metadata']==q['metadata']
  return dict(c,commit_file=q['commit_file'],commit_sha256=q['commit_sha256'])
 def schema(q,n,sh,dtype='float64'):assert q['metadata']['schema'][n]==dict(shape=sh,dtype=dtype,finite=True),(q['file'],n)
 def same(q,z):return all(q[n]==z[n] for n in ('file','sha256','commit_file','commit_sha256'))
 parents={};proofs={};terminals={}
 for key,(stem,pid,source,sh,ph,rh,ch,nc,nr) in FINITE0_PARENTS.items():
  for n,h in ((source,sh),(stem+'.md',ph),(stem+'_RESULT.json',rh),(stem+'_RECEIPT.json',ch)):bind(n,h)
  r=json.loads(path(stem+'_RESULT.json').read_text());rc=json.loads(path(stem+'_RECEIPT.json').read_text())
  assert rc['status']=='CLOSED' and rc.get('error_sha256') is None and rc['result_sha256']==rh and rc['owner']==r['owner'] and r['owner']['pid']==pid and r['owner']['source_sha256']==sh
  assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values()) and len(r['controls'])==nc and len(r['checkpoints'])==nr and all(c['passed'] for c in r['controls'])
  terminals[key]=dict(pid=pid,source_sha256=sh,protocol_sha256=ph,result_sha256=rh,receipt_sha256=ch);parents[key]=(r,rc)
  if key in FINITE0_PROOFS:
   name,h,status=FINITE0_PROOFS[key];bind(name,h);a=json.loads(path(name).read_text());assert a['status']==status and a['controls']==nc and a['committed_pairs']==nr
   expected=terminals[key] if 'parent_terminal' in a else dict(pid=pid,result_sha256=rh,receipt_sha256=ch,error_sha256=None);assert a.get('parent_terminal',a.get('parent'))==expected;proofs[key]=a
 cr,cc=parents['current'];pr,pc=parents['pilot'];fr,fc=parents['force'];hr,hc=parents['phase'];mr,mc=parents['mean']
 assert proofs['current']['canonical_and_weak_trace_admitted'] is True and proofs['current']['physical_state_or_history_adopted'] is False
 assert pr['case']['canonical_primitive_readout_admitted'] is proofs['pilot']['canonical_primitive_readout_admitted'] is False and pr['case']['frozen_canonical_admission_preserved'] is True and pr['case']['physical_adoption'] is False
 assert hr['literal_Hessian_positive'] and hr['phase_mass_positive'] and hr['physical_adoption'] is False and proofs['phase']['physical_adoption'] is False
 assert mr['physical_adoption'] is proofs['mean']['physical_adoption'] is False and mr['mean_inventory_overlap_proven'] is False
 ci=selected(cr['checkpoints'][0],cc['output_sha256']);cj=selected(cr['case']['rate_jets'],cc['output_sha256']);pi=selected(pr['checkpoints'][0],pc['output_sha256']);pilots=[selected(q,pc['output_sha256']) for q in pr['case']['columns']];prior=selected(pr['case']['readout'],pc['output_sha256'])
 assert same(pi['metadata']['selected_rate_jets'],cj) and prior['metadata']['offsets_targets_or_state_refitted'] is False
 system=ci['metadata']['system_records'];basis=selected(system['basis'],cc['input_sha256']);assert same(basis,pi['metadata']['selected_basis']) and same(basis,cj['metadata']['basis_ref']) and basis['metadata']['owner']['pid']==39611
 canonical=[selected(system[str(i)],cc['input_sha256']) for i in range(4)];forces=[]
 for i,(q,z) in enumerate(zip(pilots,canonical)):
  assert q['metadata']['column']==z['metadata']['column']==i and q['metadata']['source_configuration_changed'] is False
  f=selected(q['metadata']['old_force_ref'],pc['input_sha256']);assert f in fr['checkpoints'] and same(f,z['metadata']['force_parent']);forces.append(f)
  for n,sh in (('chart_h',[3784,3,3]),('chart_ih',[3784,3,3]),('chart_sqrt_h',[3784]),('chart_N',[3784]),('chart_beta',[3784,3]),('chart_u',[3784,3]),('config_z',[32,3784,4]),('config_phi',[3784,4]),('config_R',[3784]),('config_Z_coordinate',[3784]),('config_g',[3784,4,4]),('seed_owned_coordinate_Ndot',[3784]),('seed_owned_coordinate_betadot',[3784,3])):schema(q,n,sh)
  for n,sh in (('dg',[3784,4,4,4]),('Ga',[3784,4,4,4])):
   for w in ('hi','lo'):schema(q,'first_jet_'+n+'_'+w,sh)
  for n,sh in (('seed_chart_derivative_dN',[3784,4]),('seed_chart_derivative_dbeta',[3784,4,3]),('seed_chart_derivative_dh',[3784,4,3,3]),('seed_chart_derivative_du_cov',[3784,4,3]),('seed_dz',[32,3784,4,4])):schema(f,n,sh)
  schema(z,'pstar',[3784,99]);schema(z,'pistar',[3784,6])
 for n,sh in (('R',[4,3784]),('dv',[4,3784]),('hats',[4,4,3,86,44]),('r',[87]),('z',[45])):schema(basis,n,sh)
 for n in ('cell_i','cell_j'):schema(basis,n,[3784],'int64')
 for family,sh in (('native',[33,15136,3]),('metric',[15136,6])):
  for axis in ('value','R','Z'):
   for w in ('hi','lo'):schema(cj,family+'_jet_'+axis+'_'+w,sh)
 for family,sh in (('native',[33,3,87,45]),('metric',[6,87,45])):
  schema(prior,family+'_original_target',sh)
  for n in ('frozen_rhs_defect','primitive_minus_earned_bridge','actual_target_residual'):
   for w in ('hi','lo'):schema(prior,family+'_'+n+'_'+w,sh)
 hi=selected(hr['checkpoints'][0],hc['output_sha256']);hl=selected(hr['loads'],hc['output_sha256']);mi=selected(mr['checkpoints'][0],mc['output_sha256']);means=[selected(q,mc['output_sha256']) for q in mr['checkpoints'][1:5]]
 fixed=pi['metadata']['fixed'];bg=pi['metadata']['owned_background'];old=hi['metadata']['phase_refs']
 assert old['fixed']==mi['metadata']['fixed']==fixed and old['owned_background']==mi['metadata']['owned_background']==bg and same(old['basis'],basis) and same(old['prior_primitive_readout'],prior)
 assert all(same(q,z) for q,z in zip(old['pilot_columns'],pilots)) and hl['metadata']['target_prior']=='prior_current_literal_action_weak_phase_density_unchanged'
 for n in ('fixed_literal_weak_phase_charge','registered_weak_phase_charge','owned_registered_weak_phase_charge','literal_minus_registered_weak_gap','registered_minus_owned_weak_gap'):
  for w in ('hi','lo'):schema(hl,n+'_'+w,[87,45])
 ordinary=selected(mi['metadata']['full_source_ref'],fc['output_sha256']);assert same(ordinary,fr['cases'][0]['loads']) and fr['cases'][0]['sigma']==1.
 for n,sh in (('source_R',[4832]),('source_Z',[4832]),('source_mass_weights',[4832]),('fine_reference_directions',[64,3]),('fine_reference_weights',[64])):schema(mi,n,sh)
 for i,(q,z) in enumerate(zip(means,pilots)):
  assert q['metadata']['column']==i and same(q['metadata']['configuration_parent'],z) and q['metadata']['production_rule']=='fine' and q['metadata']['angular_rules'][1]['antipodal_directions']==128
  for n in ('reference_coordinate_dust_density','reference_radiation_energy_measure'):schema(q,n,[3784])
 for n,sh in (('ordinary_input_source_R',[4832]),('ordinary_input_source_Z',[4832]),('ordinary_input_source_mass_weight',[4832]),('ordinary_input_source_right_weight',[4832]),('ordinary_input_source_specific_covariant_p',[4832,3])):schema(ordinary,n,sh)
 schema(ordinary,'ordinary_input_source_indices',[4832],'int64')
 registration=mi['metadata']['registration_file'];bind(registration,mi['metadata']['registration_sha256']);reg=json.loads(path(registration).read_text());assert reg['branch_adopted'] is False and reg['ordinary_source_appended'] is False
 refs=dict(pilots=pilots,forces=forces,current_input=ci,current_jets=cj,canonical_columns=canonical,prior_readout=prior,basis=basis,phase_input=hi,phase_loads=hl,mean_input=mi,mean_columns=means,ordinary_loads=ordinary,fixed=fixed,owned_background=bg,proofs=proofs,terminals=terminals,ordinary_registration=reg,primitive_bridge_admitted=False,weak_phase_target='fixed_literal_weak_phase_charge_hi/lo',radiation_rule='64 normalized hemisphere weights; expand antipodes with half weight each; covector=(nR,nZ,R_ref*nphi), D_R fixed',galaxy_same_position_new_geometry_sampler_required=True,new_candidate_coefficients_and_EOS_must_be_rebuilt=True,physical_adoption=False)
 return dict(INPUTS),refs
