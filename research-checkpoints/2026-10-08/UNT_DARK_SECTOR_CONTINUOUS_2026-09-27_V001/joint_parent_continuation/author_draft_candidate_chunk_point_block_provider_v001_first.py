"""HELD CLOSED-cache point provider; definitions only, root numerical owner.
Globals np,P,json and reviewed147 + generic96 definitions. No prepare, primal,
old action, inverse, factor or weak operator is evaluated. The caller supplies
read_closed(ref,names), seal_completed(role,metadata), clear_completed(),
describe and original2e-11 check; seal commits all current kept words before
clear. NEW point basis is exact(1,0); later fullweak probes use both words.
"""
POINT_PROVIDER_AUTHOR_DRAFT=True
POINT_PROVIDER_AUTHORING_IN_PROGRESS=False
MECHANICAL_SOURCE=(None,None)
MECHANICAL_RESULT=(None,None,'COMPLETED_CANDIDATE_MECHANICAL_TEMPORAL_CACHES_PREPARED_UNQUALIFIED')
MECHANICAL_RECEIPT=(None,None,'CLOSED')
MECHANICAL_CLOSURE_PROOF=(None,None,None)
POINT_CHUNK_CAP=128
POINT_CACHE_PREFIX='NEW_candidate_temporal_cache_'
POINT_S=('g','hi','U','z','P','w','omega')
POINT_C=('h','ih','N','beta','u','up','gamma','dens','sqrt_h','JU','JzU','Jzz','Uh','zh','embed')

def candidate_point_provider_admission(bind):
 assert not POINT_PROVIDER_AUTHOR_DRAFT and not POINT_PROVIDER_AUTHORING_IN_PROGRESS
 assert all(x is not None for ref in (MECHANICAL_SOURCE,MECHANICAL_RESULT,MECHANICAL_RECEIPT,MECHANICAL_CLOSURE_PROOF) for x in ref),'Naturally CLOSED mechanical cache and proof required'
 for ref in (MECHANICAL_SOURCE,MECHANICAL_RESULT,MECHANICAL_RECEIPT,MECHANICAL_CLOSURE_PROOF):bind(ref[0],ref[1])
 r=json.loads(P.path(MECHANICAL_RESULT[0]).read_text());rc=json.loads(P.path(MECHANICAL_RECEIPT[0]).read_text());proof=json.loads(P.path(MECHANICAL_CLOSURE_PROOF[0]).read_text());stem=MECHANICAL_RESULT[0].removesuffix('_RESULT.json')
 assert r['status']==MECHANICAL_RESULT[2] and rc['status']==MECHANICAL_RECEIPT[2] and rc['result_sha256']==MECHANICAL_RESULT[1] and rc['error_sha256'] is None
 assert r['owner']==rc['owner']==proof['owner'] and r['owner']['source_sha256']==MECHANICAL_SOURCE[1]
 assert proof['status']==MECHANICAL_CLOSURE_PROOF[2] and proof['source_sha256']==MECHANICAL_SOURCE[1] and proof['result_sha256']==MECHANICAL_RESULT[1] and proof['receipt_sha256']==MECHANICAL_RECEIPT[1]
 assert proof['naturally_closed'] is True and proof['exit_code']==0 and proof['all_input_seals_verified'] is True and proof['all_success_role_seals_verified'] is True
 assert r['qualification']==rc['qualification'] and all(x is False for x in r['qualification'].values()) and r['controls']==[] and not P.path(stem+'_ERROR.json').exists() and not P.path(stem+'_ERROR_RECEIPT.json').exists()
 case=r['case'];records=r['checkpoints'];assert case['roles']==len(records)==6 and case['new_controls']==0 and case['inherited_controls']==12 and case['physics_action_evaluated'] is False and case['global_inverse_or_physical_adoption'] is False
 caches=records[1:5];assert [thin(x) for x in caches]==case['caches']==case['preparation']['metadata']['caches'] and records[0]==case['input'] and records[-1]==case['preparation']
 for ref in records:
  bind(ref['file'],ref['sha256']);bind(ref['commit_file'],ref['commit_sha256']);assert json.loads(P.path(ref['commit_file']).read_text())=={n:ref[n] for n in ('file','sha256','metadata')}
  assert ref['metadata']['owner']==r['owner'] and ref['metadata']['failed'] is False and ref['metadata']['qualification']==r['qualification']
  assert rc['output_sha256'][ref['file']]==ref['sha256'] and rc['output_sha256'][ref['commit_file']]==ref['commit_sha256']
 for iq,ref in enumerate(caches):
  md=ref['metadata'];assert md['column']==iq and md['points']==3784 and md['kind']=='NEW_full_column_fixed_configuration_temporal147_cache_from_completed_STATE' and md['cache_prefix']==POINT_CACHE_PREFIX.removesuffix('_')
  assert md['configuration_held'] is True and md['old_coefficients_features_momenta_EOS_current_or_action_replayed'] is False and md['global_inverse_or_action_qualified'] is False and md['physical_adoption'] is False
  assert md['input']==thin(case['input']) and md['constants']==case['preparation']['metadata'].get('constants',md['constants']) and md['candidate_provenance']['closed_candidate_proof']==case['closed_candidate_proof']
 return dict(caches=caches,input=case['input'],preparation=case['preparation'],closed_provenance=dict(owner=r['owner'],source=MECHANICAL_SOURCE,result=MECHANICAL_RESULT,receipt=MECHANICAL_RECEIPT,proof=MECHANICAL_CLOSURE_PROOF),physical_adoption=False)

def candidate_point_cache_names(metadata):
 schema=metadata['schema'];prefix=POINT_CACHE_PREFIX
 names=[prefix+'raw_configuration_'+n for n in POINT_S]+[prefix+'raw_chart_'+n for n in POINT_C]
 for suffix in ('anchored_raw_up_dot_zi','paired_N_times_anchored_A','fixed_lowered_E0','gamma_squared_denominator','formal_I_times_u','formal_Iu_minus_raw_up'):
  names.extend(prefix+suffix+'_'+word for word in ('hi','lo'))
 names.extend(n for n in schema if n.startswith(prefix+'copied_positive_coefficient_'))
 diagnostics=('copied_STATE_candidate_raw_direct_minus_quotient_','copied_STATE_candidate_raw_model_minus_new_raw_chart_first_','copied_STATE_candidate_raw_new_candidate_minus_owned_reference_','copied_STATE_candidate_raw_geometry_')
 extra=tuple('copied_STATE_candidate_raw_'+n+'_'+w for n in ('KGamma_minus_KADM','Ktrace_Gamma_minus_ADM','new_first_compatibility_minus_E0') for w in ('hi','lo'))
 names.extend(n for n in schema if n.startswith(diagnostics) or n in extra)
 assert len(names)==len(set(names))==117 and sum(n.startswith(prefix+'copied_positive_coefficient_') for n in names)==29
 assert all(schema[n]['dtype']=='float64' and schema[n]['finite'] is True for n in names)
 return tuple(names)

def candidate_point_slice(data,name,selection,keep,label):
 a=data[name];assert a.dtype==np.float64 and np.all(np.isfinite(a));axes=[i for i,n in enumerate(a.shape) if n==3784];assert len(axes)<=1
 if axes:
  assert axes[0] in (0,1);index=[slice(None)]*a.ndim;index[axes[0]]=selection;a=a[tuple(index)]
 return keep(label+'_'+name,np.asarray(a).copy())

def candidate_point_hydrate(data,metadata,selection,keep,label):
 assert isinstance(selection,slice) and selection.step in (None,1) and isinstance(selection.start,int) and isinstance(selection.stop,int)
 lo,hi=selection.start,selection.stop;p=hi-lo;assert 0<=lo<hi<=3784 and 1<=p<=POINT_CHUNK_CAP and POINT_CHUNK_CAP==128
 local={n:candidate_point_slice(data,n,selection,keep,label+'_copied') for n in candidate_point_cache_names(metadata)};prefix=POINT_CACHE_PREFIX
 s={n:local[prefix+'raw_configuration_'+n] for n in POINT_S};c={n:local[prefix+'raw_chart_'+n] for n in POINT_C};pair=lambda n:(local[prefix+n+'_hi'],local[prefix+n+'_lo'])
 ep=prefix+'copied_positive_coefficient_';envelopes={n[len(ep):]:a for n,a in local.items() if n.startswith(ep)}
 cache=dict(s=s,c=c,p=p,A=pair('anchored_raw_up_dot_zi'),NA=pair('paired_N_times_anchored_A'),gamma_squared=pair('gamma_squared_denominator'),fixed_E0=pair('fixed_lowered_E0'),envelopes=envelopes,constants={n:metadata['constants'][n] for n in ('ALPHA','ELL','C')},candidate_provenance=metadata['candidate_provenance'],configuration_held=True,old_coefficients_or_primal_features_replayed=False)
 assert c['N'].shape==(p,) and s['z'].shape==(32,p,4) and s['w'].shape==s['omega'].shape==(32,) and c['JzU'].shape==(32,p,3) and c['zh'].shape==(32,p,6) and all(a.shape==(p,) for a in cache['gamma_squared'])
 assert np.all(c['N']>0) and np.all(c['gamma']>0) and np.all(c['dens']>0) and np.all(s['omega']>0) and np.all(s['w']>=0) and all(cache['constants'][n]==getattr(P,n) for n in cache['constants'])
 keep(label+'_exact_full_column_point_indices',np.arange(lo,hi,dtype=np.int64));return cache

def candidate_point_physical_basis(p,kind,coordinate,keep,label):
 n=P.a_dd(np.zeros((p,99)));m=P.a_dd(np.zeros((p,6)))
 if kind=='head':
  assert 0<=coordinate<9;target=n if coordinate<3 else m;slot=coordinate if coordinate<3 else coordinate-3;target[0][:,slot]=1.
 else:
  assert kind=='modal' and 0<=coordinate<3
  for mode in range(32):n[0][:,3+3*mode+coordinate]=1.
 mh_pair(label+'_NEW_unit_physical_native',n,(p,99),keep);mh_pair(label+'_NEW_unit_physical_metric',m,(p,6),keep);return dict(native=n,metric=m)

def candidate_point_canonical_envelopes(cache,physical,keep,label):
 s,c,p=cache['s'],cache['c'],cache['p'];e=candidate_temporal_jet_envelopes(cache,physical,keep,label+'_NEW_jet');U,z,hi,proj=abs(s['U']),abs(s['z']),abs(s['hi']),abs(s['P']);g=abs(s['g'])
 nu=e['du'].copy();nz=e['dz'].copy()
 for l in range(4):nu+=U[:,l,None,None]*e['Ga'][:,:,:,l].transpose(0,2,1);nz+=z[:,:,l,None,None]*e['Ga'][:,l][None]
 q=np.einsum('pa,jpab->jpb',U,nz);V=np.einsum('pab,jpb->jpa',proj,q);DD=np.einsum('pac,jpcd,pbd->jpab',proj,nz,proj)
 lower=np.einsum('pab,pbc->pac',nu,g);F=lower+lower.swapaxes(-1,-2);Fu=np.einsum('pac,pcd,pdb->pab',hi,F,hi);Vu=np.einsum('pab,jpb->jpa',hi,V);Du=np.einsum('pac,jpcd,pdb->jpab',hi,DD,hi)
 Pi=abs(s['w'])[:,None,None,None]*(U[None,:,:,None]*Vu[:,:,None,:]/s['omega'][:,None,None,None]**2+P.ELL**2*Du);PiU=abs(P.ALPHA)*np.einsum('pab,pbc->pac',hi,F);sym=.5*(Pi+Pi.swapaxes(-1,-2))
 Klo=np.einsum('jpl,jpab->plab',z,sym);Kup=np.einsum('plm,pmab->plab',hi,Klo);CC=.5*(Kup.transpose(0,2,1,3)+Kup.transpose(0,2,3,1)+Kup)
 MX=U[:,None,None,:]*Fu[:,:,:,None]+U[:,None,:,None]*Fu[:,:,None,:];CC+=abs(P.ALPHA)/2*MX;PU=PiU[:,0];P00=Pi[:,:,0,0]
 pu=np.einsum('pab,pa->pb',abs(c['JU']),PU)+np.einsum('jpa,jp->pa',abs(c['JzU']),P00);pz=Pi[:,:,0,1:]+abs(c['Jzz'])[None]*P00[:,:,None]
 native=abs(c['dens'])[:,None]*np.concatenate((pu,pz.transpose(1,0,2).reshape(p,96)),axis=1)
 pm=np.einsum('pqa,pa->pq',abs(c['Uh']),PU)+np.einsum('pqab,pab->pq',abs(c['embed']),CC[:,0])+np.einsum('jpq,jp->pq',abs(c['zh']),P00);metric_native=abs(c['dens'])[:,None]*pm
 K=abs(c['N'])[:,None,None]*e['Ga'][:,0,1:,1:];I=abs(c['ih']);trace=np.einsum('pij,pij->p',I,K);EH=abs(c['sqrt_h'])[:,None,None]*(np.einsum('pij,pjk,pkl->pil',I,K,I)+I*trace[:,None,None])/(2*abs(P.C))
 metric_EH=np.stack([EH[:,i,j]*(1. if i==j else 2.) for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],axis=1);metric=metric_native+metric_EH
 out=dict(native=native,metric_total=metric,Pi=Pi,PiU=PiU,metric_EH=metric_EH)
 for n,a in out.items():keep(label+'_NEW_positive_'+n,a.copy());assert np.all(np.isfinite(a)) and np.all(a>=0)
 return out

def prepare_candidate_point_block_provider(admitted,read_closed,seal_completed,clear_completed,describe,check):
 assert not POINT_PROVIDER_AUTHOR_DRAFT and admitted['physical_adoption'] is False and len(admitted['caches'])==4
 loaded={}
 def provider(column,selection,keep,label):
  assert 0<=column<4;ref=admitted['caches'][column];md=ref['metadata'];assert md['column']==column
  if column not in loaded:
   loaded.clear();loaded[column]=read_closed(ref,candidate_point_cache_names(md))
  cache=candidate_point_hydrate(loaded[column],md,selection,keep,label+'_cache');p=cache['p'];chunk_source=dict(cache=thin(ref),closed_mechanical=admitted['closed_provenance'],selection=[selection.start,selection.stop],exact_basis_amplitude=[1.,0.])
  cache_record=seal_completed('POINT_CACHE',dict(kind='closed_cached147_chunk_hydration_only',source=chunk_source,closed_candidate_provenance=cache['candidate_provenance'],old_prepare_or_primal_replayed=False));clear_completed();heads=[];modes=[];eH=np.zeros((p,9,9));eE=np.zeros((32,p,3,9));eD=np.zeros((32,p,3,3));D=P.a_dd(np.zeros((32,p,3,3)));action_refs=[]
  for kind,count in (('head',9),('modal',3)):
   for coordinate in range(count):
    name=label+'_NEW_'+kind+str(coordinate);physical=candidate_point_physical_basis(p,kind,coordinate,keep,name);result=candidate_specialized_temporal_action(cache,physical,keep,name+'_147');bounds=candidate_point_canonical_envelopes(cache,physical,keep,name+'_bounds')
    record=seal_completed('POINT_DIRECTION',dict(kind='NEW_unit_basis_147_point_action_and_uncancelled_bounds',basis_kind=kind,coordinate=coordinate,source=chunk_source,cache=thin(cache_record),phase_or_configuration_action_replayed=False,physical_adoption=False));action_refs.append(thin(record))
    item=dict(physical_native=physical['native'],physical_metric=physical['metric'],native=result['point']['native'],metric_total=result['point']['metric_total'],amplitude_words=(1.,0.))
    if kind=='head':
     item.update(head_coordinate=coordinate,new_provenance=dict(source=chunk_source,completed_action=thin(record)));heads.append(item);eH[:,:,coordinate]=np.concatenate((bounds['native'][:,:3],bounds['metric_total']),axis=1);eE[:,:,:,coordinate]=bounds['native'][:,3:].reshape(p,32,3).transpose(1,0,2)
    else:
     item.update(Pi=P.a_slice(result['point']['native'],slice(None)) if False else pair_from_POINT_Pi(result,record),completed_provenance=dict(source=chunk_source,completed_action=thin(record)));modes.append(item)
     for word in (0,1):D[word][:,:,:,coordinate]=result['point']['native'][word][:,3:].reshape(p,32,3).transpose(1,0,2)
     eD[:,:,:,coordinate]=bounds['native'][:,3:].reshape(p,32,3).transpose(1,0,2)
    clear_completed()
  contacts=[]
  def construction_check(name,actual,expected,envelope):
   check(name,actual,expected,envelope);contacts.append(dict(name=name,tolerance=2e-11,passed=True,scope='original109_post_Pi_distribution_association_only'))
  b=reconstruct_modal_head_blocks(cache,modes,keep,describe,construction_check,label+'_NEW_B');h=collect_directed_head_blocks(cache,heads,keep,describe,label+'_NEW_HE');d=mh_real_readout(D,keep,label+'_NEW_D');eB=b['post_Pi_envelope']
  for n,a in (('eH',eH),('eB',eB),('eE',eE),('eD',eD)):keep(label+'_'+n,a.copy());assert np.all(np.isfinite(a)) and np.all(a>=0)
  assert len(action_refs)==12 and len(contacts)==3
  final=seal_completed('POINT_BLOCK_CHUNK',dict(kind='NEW_directed_real_numerical_H_B_E_D_chunk_with_paired_readout_gaps',source=chunk_source,cache=thin(cache_record),actions=action_refs,construction_contacts=contacts,closed_candidate_provenance=cache['candidate_provenance'],C_equals_L_or_E_equals_B_transpose_assumed=False,exact_normalization_or_point_inverse_earned=False,original_paired_full_weak_action_authoritative=True,global_or_uniform_DD_inverse_qualified=False,physical_adoption=False));clear_completed()
  return dict(H=h['H_real'],B=b['B_real'],E=h['E_real'],D=d['real'],eH=eH,eB=eB,eE=eE,eD=eD,paired_raw=dict(H=h['H'],B=b['B'],E=h['E'],D=D),readout_gaps=dict(H=h['H_readout_gap'],B=b['B_readout_gap'],E=h['E_readout_gap'],D=d['readout_gap']),closed_candidate_provenance=cache['candidate_provenance'],construction_contacts=contacts,committed_chunk=thin(final),source=chunk_source,global_or_uniform_DD_inverse_qualified=False,physical_adoption=False)
 return provider
