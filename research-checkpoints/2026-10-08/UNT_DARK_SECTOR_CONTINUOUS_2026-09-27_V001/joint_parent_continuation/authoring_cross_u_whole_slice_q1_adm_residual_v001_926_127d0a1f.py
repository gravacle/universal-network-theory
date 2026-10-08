"""Guarded genuine Q1 whole-slice ADM residual and conservative EH incidence."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,hashlib,json,math,os,traceback
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001'
WHOLE='CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V001'
COMPACT='CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V002'
METRIC='CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001'
ORDINARY='CROSS_U_SAVED_ROTATING_SHEET_FRECHET_V001'
BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
PROTOCOL_SHA=None
LIGHT=299792458.;KPC=3.085677581491367e19;A0=1.0059833281731022e-10
B=A0*KPC/LIGHT**2;C=1.98;KB=.02;ALPHA=KB/C;GC=3*math.pi/8;ELL=.1
SIGMAS=(.1,1.,10.,100.);TOL=2e-11;POINTS_PER_COLUMN=3784;POINTS_PER_ARM=15136
CONTROL_COUNT=77;PAIR_COUNT=23
np=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};ARM_AVAILABLE={};CONTEXT={}
FLAGS={k:False for k in ('whole_constraint_solution_qualified','CMC_solution_qualified','physical_Cauchy_data_qualified','physical_history_qualified','physical_junction_qualified','physical_native_inertia_qualified','full_temporal_improvement_qualified','ordinary_cosmic_state_qualified','metric_correction_applied','orbital_force_qualified','observational_qualified','joint_model_adopted')}
PINS={'cross_u_saved_full_native_adm_constraint_sources_v002.py': '1236e6b6837dd0356f7aae55bcf3d8ee4ed0ce3b4530907580990430e021d880', 'CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V002.md': '609ad771c8d7e3487d7db4545a76343452c91d773e8c6138de71ebcb92518b6c', 'CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V002_RESULT.json': '82dc17bc2d3d5ab730110887ea24c67d5b5b99fdff843397d98b455a8b5f29d2', 'CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V002_RECEIPT.json': 'bdbe52eaf088bf2139d1bc7c385dcee755cd1fffcbbfef8467d86c85edfc46a7', 'CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001_RESULT.json': 'ef7f81025c000fd9281bbb9a5afdbb3503a204b56ed0f8b6a291fc2152225798', 'CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001_RECEIPT.json': 'eb450284a7c28b65df0eb5d9ecb08d0f6156c98d7ca6ae52ce2af37b6353dfde', 'CROSS_U_SAVED_ROTATING_SHEET_FRECHET_V001_RESULT.json': 'e62722bbff40d0f063d3a80e2467b06d7d4d305dd304140efced5add000fe929', 'CROSS_U_SAVED_ROTATING_SHEET_FRECHET_V001_RECEIPT.json': 'f24459d3dfffbfd773323ba69c375ac8f08bda5e121d2f530dc156c1955fb6d7', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json': '3f4cbdf1c8255ae06668dc63fa6cdfc7ca4c5b70c78a2b5cbe64a303fb17973c', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CROSS_U_CONSTRAINED_CANONICAL_CHART_AND_CMC_ADMISSION_V001.md': '872ca230d040bfca08ac127c117e741e81549a4316e62dd5de8df8e8732f7e98', 'cross_u_whole_slice_cauchy_data_v001.py': None, 'CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V001.md': None, 'CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V001_RESULT.json': None, 'CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V001_RECEIPT.json': None}
HELPER_SPANS=[{'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'lower', 'first': 234, 'last': 234, 'sha256': '065bc9c41f65ef90b29f76e49d31bbe082ab7995a2f31dcfee81e74d72847a28'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'lower_last', 'first': 237, 'last': 237, 'sha256': 'a5499ee24271aa5e88cc7a6bbc63e5c554179f3f1b572dd891ed65ccce86554a'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'raise_cov', 'first': 240, 'last': 240, 'sha256': 'f361d67c7314df41c3c6ac01d96d9362912269eb45ffb4a6568bbb1398b4263b'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'covdot', 'first': 243, 'last': 243, 'sha256': '7746ebccfd341cc85e0168705cc0c0627b26e9157cfd2c3a7813a960e59f8551'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'features', 'first': 246, 'last': 270, 'sha256': '4f458b4c8277a90abc2cffcea3d268b1be54a828a2cfc66b281bd50b5e4554e0'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'variation', 'first': 273, 'last': 302, 'sha256': '06b0cf4a6611f694ebfab5d7fa89ae820c3a1a47569c553524838bce111f1f9d'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'metric_partial', 'first': 305, 'last': 308, 'sha256': '35322f99ef24ed0ca3167bda05714d8499b4c99cd91f32f2c30f46570ca05d07'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'connection_delta', 'first': 311, 'last': 316, 'sha256': '25e5fd7429e4fbbe00d8637bc1b3259fa75a1e68a277904c74f0cd17576d495e'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'metric_native', 'first': 319, 'last': 360, 'sha256': '8c3a2432b3b7daa45f878828f4bbb060f6fdb4502357bb2dc97146d1bc204e0f'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'metric_basis', 'first': 363, 'last': 366, 'sha256': '82d2cfa2ad99dd38b4a4288768515717bfc43bcd761411b1b144c51ede631b6f'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'symmetric_tensor_from_coordinates', 'first': 369, 'last': 372, 'sha256': '06f37c65cdcf715a84ede125cb915071a27cea474c5a186435a354da3b127aee'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'adm_chart', 'first': 375, 'last': 401, 'sha256': 'dcf8e74239d8b577aff9b945b795a614f8cc1bd7258f04f99a186ab32e6ceb18'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'connection_momentum', 'first': 404, 'last': 412, 'sha256': '535db3aa5173a0be102fc7d54342aea7175c4518a029280212df48464ddfc80e'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'reduced_momenta', 'first': 415, 'last': 422, 'sha256': '9fbfc9ba16c8585383461623765b6f1f16e30dcec05d5608d7e2ead915e66bb9'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'connection_from_jet', 'first': 425, 'last': 429, 'sha256': '1a91701d7a350da6c651255c128f8a345a2d3d7f60d890da461178137af44f18'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'native_velocity_jet', 'first': 432, 'last': 440, 'sha256': 'c291268ef5986fb9bbd39929e5621ec6e86c5e0f68a6b26755ed4c84a6b2f2c3'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'kinetic_tangent', 'first': 443, 'last': 453, 'sha256': '2a73b477ef65385c5bd6bab8d5970584b82ba5e7a00367c8eecfa1361a67145c'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'ordinary_velocity', 'first': 465, 'last': 470, 'sha256': 'f5f98a365e86f1cce7c19f293e416783ec86e894f7b0504f09ed7fcecfafc987'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'arrowhead_blocks', 'first': 483, 'last': 498, 'sha256': '533c1ea643fcda93e284b5d33c0672f228683e2f870778aae706bafa74cc15d1'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'arrowhead_action', 'first': 501, 'last': 506, 'sha256': 'bfef80ee288426b0e4cef778804e64e3a2bd2e3298e7d58f632c72f6f72acb56'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'arrowhead_solve', 'first': 509, 'last': 523, 'sha256': 'b896134b70ccf02334aa6a42289e9c358dcd928fca5bdb2449a1fb9e55228927'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'adm_first_jets', 'first': 526, 'last': 530, 'sha256': 'afe980a18505337ed145a7a0ce3c5bbde1835edd72877db94812b644d6d3350f'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'lapse_shift_lift', 'first': 533, 'last': 549, 'sha256': '1e99cec78a1f68df0698bf4bbb2906d2007bcf06e026a5f7e7cd825b725cb1e0'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'absolute_phase_metric_row', 'first': 552, 'last': 558, 'sha256': '92db83e67e54ca978abb49a21d081ba346afb04eb467462bf6ae05296b508608'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'native_phase_constraint_direction', 'first': 561, 'last': 570, 'sha256': '05cc05d9dc1b4768c461cde7652866f806a22586b19a68039f3808a220ffbdd3'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'spatial_generator_density', 'first': 573, 'last': 584, 'sha256': '9e5b954472b14d5b0118b140251cec4ee6215e5648debe2ac6d6c99a01ca5b3c'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'spatial_curvature_weak_density', 'first': 587, 'last': 619, 'sha256': 'a94909811439b4bb6130aac41850992a865a594bd407c78ebd451d2fad94a16f'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'EH_ADM_constraint_direction', 'first': 622, 'last': 635, 'sha256': 'fc0117917054b02a2d95de07fd16bb4a2a71b55b3a0dff0af9451eac519d460f'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'ordinary_canonical_constraint_rows', 'first': 638, 'last': 642, 'sha256': '50d806bb625cab3ae665f32cf086f2668674018bbfdd3ad6329921b2cc00114e'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'chart_operation_envelopes', 'first': 140, 'last': 163, 'sha256': 'd36b54047e7cff6638f1ce035a1ab6926e4ae13ba5e20aa43b9ffaf905a2f2d9'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'momentum_envelope', 'first': 166, 'last': 181, 'sha256': '4bbd4b53c6de9d0f70dee6e88fafdc12d93469b06ffe397bbdbf34d659af3e31'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'arrowhead_operation_envelopes', 'first': 670, 'last': 708, 'sha256': '8b5b6e6c8ad01d2236dbf1a454c52c67a6b0e3e674dd5d36db2ac7639b00f69a'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'arrowhead_original_envelope', 'first': 662, 'last': 667, 'sha256': '6dd3ba42fd39b740a9a19476973eded2e771e4c9906656ae393101f8570dd153'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'arrowhead_original_operation_envelope', 'first': 780, 'last': 786, 'sha256': '22ec892b0beca41d602002ab5012c1f65b651c6535895325a12867ef8686629c'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'arrowhead_saved_action_operation_envelope', 'first': 764, 'last': 778, 'sha256': '75f6f2c759ab817bd04aff396ee907b8020899676afb8a58e22048b98c0578a1'}, {'file': 'cross_u_saved_full_native_adm_constraint_sources_v002.py', 'name': 'reconstruct_owned_K', 'first': 815, 'last': 837, 'sha256': '8eba1724bb2641df2c0062136b67c8ded225605791ac3f4556122951c7e41d4b'}, {'file': 'cross_u_whole_slice_cauchy_data_v001.py', 'name': 'now', 'first': 238, 'last': 238, 'sha256': 'cfeba74fb44c1d3d845b6e24206d7c7deb6ccaff77dfa195290154fed20ce565'}, {'file': 'cross_u_whole_slice_cauchy_data_v001.py', 'name': 'path', 'first': 239, 'last': 240, 'sha256': '5e5c0bc42761e84c4993ff97a061409b6a91c2295d2bab504fc73c3bfbedd7d7'}, {'file': 'cross_u_whole_slice_cauchy_data_v001.py', 'name': 'sha', 'first': 242, 'last': 246, 'sha256': '9d1ebcd1dfd3edcb6d587b9c575b602c23bab4bd1c09b106ab5461951e333342'}, {'file': 'cross_u_whole_slice_cauchy_data_v001.py', 'name': 'canonical', 'first': 248, 'last': 254, 'sha256': 'b02c884a9689660e30278aa4bce010a0e728c616b0c5865ee950e9e0620b54be'}, {'file': 'cross_u_whole_slice_cauchy_data_v001.py', 'name': 'encode', 'first': 256, 'last': 256, 'sha256': 'fb3b9923e84a279b4bfeaaa9c31fe4261c7da1e43d6e9ef9b328848c80b7aeb8'}, {'file': 'cross_u_whole_slice_cauchy_data_v001.py', 'name': 'publish', 'first': 258, 'last': 261, 'sha256': 'eaddf4faf7cae6c7454e8689d14f5164569fe1ed507e61dd18919e196d6ccdc9'}, {'file': 'cross_u_whole_slice_cauchy_data_v001.py', 'name': 'json_file', 'first': 263, 'last': 263, 'sha256': '0bcbc7c3054ae70302c0758a9ecc77401c1b98efa9503f936eb275e0b6e31b79'}, {'file': 'cross_u_whole_slice_cauchy_data_v001.py', 'name': 'check', 'first': 265, 'last': 271, 'sha256': 'a49fcde61938565bc14a896d5f97a3a06f49df629e05612aeacae8707e656fca'}, {'file': 'cross_u_whole_slice_cauchy_data_v001.py', 'name': 'checkpoint', 'first': 273, 'last': 287, 'sha256': '0fea2da5ccacc583774859760a85a3a85b47926ff76c9fe332a3220e35094be7'}, {'file': 'cross_u_whole_slice_cauchy_data_v001.py', 'name': 'recheck', 'first': 289, 'last': 301, 'sha256': '3bd12d218161fb20d375bbd236013aa4d77f29add25a716bdfd7907bd0b3dd2c'}, {'file': 'cross_u_whole_slice_cauchy_data_v001.py', 'name': 'seal_actual', 'first': 303, 'last': 305, 'sha256': '64de99eedfae465cd0ebe7ad87a209eead6a2eb56345ea7891f0f26fd86792e8'}, {'file': 'cross_u_whole_slice_cauchy_data_v001.py', 'name': 'read_pair', 'first': 307, 'last': 318, 'sha256': '54c1c37dc7f183901c22497d2bd50b815193b69e25d8b2d7532ef5a5d4f6d06b'}, {'file': 'cross_u_whole_slice_cauchy_data_v001.py', 'name': 'authenticate_helpers', 'first': 320, 'last': 330, 'sha256': 'e26bf285224797ede7fbfd56ff8e58d12b04dfe3817b32c16e0bcae054d55a74'}, {'file': 'cross_u_whole_slice_cauchy_data_v001.py', 'name': 'scatter_q1', 'first': 395, 'last': 398, 'sha256': '5a0b655c4c23bd603c3e2d0661b571431769c1ab8d9d9e42d4e82fdb603d9890'}]

def lower(g,v):return np.einsum('pab,...pb->...pa',g,v)


def lower_last(g,v):return np.einsum('pab,pcb->pca',g,v)


def raise_cov(hi,v):return np.einsum('pab,...pb->...pa',hi,v)


def covdot(hi,a,b):return np.einsum('...pa,...pa->...p',raise_cov(hi,a),b)


def features(g,hi,Ga,U,du,z,dz,phi,omega,xi,w):
 # du/dz have derivative index first; z and dz are COVECTORS.
 nu=du+np.einsum('pbal,pl->pab',Ga,U)
 nz=dz-np.einsum('plab,jpl->jpab',Ga,z)
 uc=lower(g,U);P=np.eye(4)[None,:,:]+np.einsum('pa,pb->pab',uc,U)
 q=np.einsum('pa,jpab->jpb',U,nz);V=np.einsum('pab,jpb->jpa',P,q)
 D=np.einsum('pac,jpcd,pbd->jpab',P,nz,P)
 F=lower_last(g,nu)-np.swapaxes(lower_last(g,nu),1,2)
 # lower_last(g,nu) lowers nu's last (vector) index, leaving derivative index first.
 a=np.einsum('pa,pab->pb',U,nu);r=np.einsum('pab,pb->pa',P,phi)
 z2=covdot(hi,z,z);f=1+z2/((B*GC)**2*xi[:,None]**4)
 Vu=raise_cov(hi,V);Du=np.einsum('pac,jpcd,pdb->jpab',hi,D,hi)
 Pi=w[:,None,None,None]*(np.einsum('pa,jpb->jpab',U,Vu)/omega[:,None,None,None]**2-ELL**2*Du)
 nuc=lower_last(g,nu);mu=np.einsum('jpab,pab->jp',Pi,nuc)
 Z=np.einsum('j,jpa->pa',w,z);Fup=np.einsum('pac,pcd,pdb->pab',hi,F,hi)
 PiU=-ALPHA*np.einsum('pac,pcb->pab',hi,F)+np.einsum('pa,pb->pab',U,Z)
 Aj=(np.einsum('jpn,jprn->jpr',Vu,nz)+np.einsum('jpa,pa->jp',q,U)[:,:,None]*V)/omega[:,None,None]**2
 Aj-=ELL**2*(np.einsum('jprn,jpn->jpr',D,Vu)
        +np.einsum('jpmr,jpmn,pn->jpr',np.einsum('pmc,jpcr->jpmr',hi,D),nz,U))
 # In the second projector term raise D's FIRST index; rho stays lower.
 Q=np.einsum('pa,pa->p',U,phi);Ur=np.einsum('pa,pa->p',U,r)
 A=-(Q[:,None]*r+Ur[:,None]*phi)+np.einsum('pn,prn->pr',Z,nu)+np.einsum('j,jpr->pr',w,Aj)
 out=dict(g=g,hi=hi,Ga=Ga,U=U,du=du,z=z,dz=dz,phi=phi,omega=omega,xi=xi,w=w,nu=nu,nz=nz,uc=uc,P=P,q=q,V=V,D=D,a=a,r=r,f=f,z2=z2,Pi=Pi,mu=mu,Z=Z,F=F,Fup=Fup,PiU=PiU,A=A)
 RAW.update({f'current_{k}':v for k,v in out.items() if isinstance(v,np.ndarray)})
 return out


def variation(s,eta,deta,zeta,dzeta):
 g,hi,Ga=s['g'],s['hi'],s['Ga'];U=s['U'];z=s['z'];w=s['w'];om=s['omega'];P=s['P']
 ne=deta+np.einsum('pbal,pl->pab',Ga,eta)
 nzeta=dzeta-np.einsum('plab,jpl->jpab',Ga,zeta)
 ec=lower(g,eta);dP=np.einsum('pa,pb->pab',ec,U)+np.einsum('pa,pb->pab',s['uc'],eta)
 dq=np.einsum('pa,jpab->jpb',eta,s['nz'])+np.einsum('pa,jpab->jpb',U,nzeta)
 dV=np.einsum('pab,jpb->jpa',dP,s['q'])+np.einsum('pab,jpb->jpa',P,dq)
 dD=np.einsum('pac,jpcd,pbd->jpab',dP,s['nz'],P)+np.einsum('pac,jpcd,pbd->jpab',P,s['nz'],dP)+np.einsum('pac,jpcd,pbd->jpab',P,nzeta,P)
 dF=lower_last(g,ne)-np.swapaxes(lower_last(g,ne),1,2)
 da=np.einsum('pa,pab->pb',eta,s['nu'])+np.einsum('pa,pab->pb',U,ne)
 dr=np.einsum('pab,pb->pa',dP,s['phi'])
 # Raw terms and TERMwise absolute contraction sums, before any integration/cancellation.
 mterms=[raise_cov(hi,s['V'])*dV/om[:,None,None]**2,
  -raise_cov(hi,z)*zeta,-(s['z2']/((B*GC)**2*s['xi'][:,None]**4))[:,:,None]*raise_cov(hi,z)*zeta,
  -ELL**2*np.einsum('pac,jpcd,pdb->jpab',hi,s['D'],hi)*dD,
  da[None,:,:]*z+s['a'][None,:,:]*zeta]
 md=np.stack([np.sum(t,axis=tuple(range(2,t.ndim))) for t in mterms],axis=-1)
 me=np.stack([np.sum(abs(t),axis=tuple(range(2,t.ndim))) for t in mterms],axis=-1)
 mx=-ALPHA*s['Fup']*dF/2;ph=-raise_cov(hi,s['r'])*dr
 terms=np.column_stack((mx.sum(axis=(1,2)),ph.sum(axis=1),np.einsum('j,jpk->pk',w,md)))
 env=np.column_stack((abs(mx).sum(axis=(1,2)),abs(ph).sum(axis=1),np.einsum('j,jpk->pk',w,me)))
 weakU=np.sum(s['A']*eta,axis=1)+np.sum(s['PiU']*ne,axis=(1,2))
 potential=w[:,None]*np.sum((s['a'][None,:,:]-s['f'][:,:,None]*raise_cov(hi,z))*zeta,axis=-1)
 weakmode=potential+np.einsum('jpab,jpab->jp',s['Pi'],nzeta)
 unitjet=2*(np.einsum('pab,pb->pa',lower_last(g,s['nu']),eta)+np.einsum('pb,pab->pa',s['uc'],ne))
 constraint=np.column_stack((2*np.einsum('pa,pa->p',s['uc'],eta),unitjet))
 dc=np.einsum('pa,jpa->jp',eta,z)+np.einsum('pa,jpa->jp',U,zeta)
 ddc=np.einsum('pab,jpb->jpa',ne,z)+np.einsum('pb,jpab->jpa',eta,s['nz'])+np.einsum('pab,jpb->jpa',s['nu'],zeta)+np.einsum('pb,jpab->jpa',U,nzeta)
 RAW.update(current_eta=eta,current_eta_partial=deta,current_zeta=zeta,current_zeta_partial=dzeta,current_direct_terms=terms,current_envelope=env,current_weakU=weakU,current_weakmode=weakmode,current_mode_envelope=me,current_constraint=constraint,current_delta_transverse=dc,current_delta_transverse_jet=ddc)
 return terms,env,md,weakU,weakmode,constraint,dc,ddc


def metric_partial(s):
 # Metric compatibility recovers the same exact first metric jet, no second derivatives.
 a=np.einsum('plam,pln->pamn',s['Ga'],s['g'])
 return a+np.swapaxes(a,2,3)


def connection_delta(s,q,dq):
 nq=dq-np.einsum('plam,pln->pamn',s['Ga'],q)-np.einsum('plan,pml->pamn',s['Ga'],q)
 dG=np.zeros_like(s['Ga'])
 for a in range(4):
  for b in range(4):dG[:,:,a,b]=np.einsum('plm,pm->pl',s['hi'],nq[:,a,b,:]+nq[:,b,a,:]-nq[:,:,a,b])/2
 return dG


def metric_native(s,q,dq,eta,deta):
 hi,g,U,z,P=s['hi'],s['g'],s['U'],s['z'],s['P'];w=s['w'];om=s['omega'];kj=(B*GC)**2*s['xi'][:,None]**4
 dG=connection_delta(s,q,dq);dhi=-np.einsum('pac,pcd,pdb->pab',hi,q,hi)
 dnu=deta+np.einsum('pbal,pl->pab',dG,U)+np.einsum('pbal,pl->pab',s['Ga'],eta)
 dnz=-np.einsum('plab,jpl->jpab',dG,z)
 duc=lower(q,U)+lower(g,eta);dP=np.einsum('pa,pb->pab',duc,U)+np.einsum('pa,pb->pab',s['uc'],eta)
 dqq=np.einsum('pa,jpab->jpb',eta,s['nz'])+np.einsum('pa,jpab->jpb',U,dnz)
 dV=np.einsum('pab,jpb->jpa',dP,s['q'])+np.einsum('pab,jpb->jpa',P,dqq)
 dD=np.einsum('pac,jpcd,pbd->jpab',dP,s['nz'],P)+np.einsum('pac,jpcd,pbd->jpab',P,dnz,P)+np.einsum('pac,jpcd,pbd->jpab',P,s['nz'],dP)
 lower_nu=lower_last(q,s['nu'])+lower_last(g,dnu);dF=lower_nu-np.swapaxes(lower_nu,1,2)
 da=np.einsum('pa,pab->pb',eta,s['nu'])+np.einsum('pa,pab->pb',U,dnu);dr=np.einsum('pab,pb->pa',dP,s['phi'])
 z2=s['z2'];V2=covdot(hi,s['V'],s['V']);F2=np.sum(s['Fup']*s['F'],axis=(1,2));r2=covdot(hi,s['r'],s['r'])
 Du=np.einsum('pac,jpcd,pdb->jpab',hi,s['D'],hi);D2=np.sum(Du*s['D'],axis=(2,3));az=np.einsum('pa,jpa->jp',s['a'],z)
 dz2=covdot(dhi,z,z);dV2=covdot(dhi,s['V'],s['V'])+2*covdot(hi,s['V'],dV)
 dD2=2*np.sum(Du*dD,axis=(2,3))+np.einsum('pac,jpab,pbd,jpcd->jp',dhi,s['D'],hi,s['D'])+np.einsum('pac,jpab,pbd,jpcd->jp',hi,s['D'],dhi,s['D'])
 dF2=2*np.sum(s['Fup']*dF,axis=(1,2))+np.einsum('pac,pab,pbd,pcd->p',dhi,s['F'],hi,s['F'])+np.einsum('pac,pab,pbd,pcd->p',hi,s['F'],dhi,s['F'])
 dr2=covdot(dhi,s['r'],s['r'])+2*covdot(hi,s['r'],dr);daz=np.einsum('pa,jpa->jp',da,z)
 modal=np.stack((V2/(2*om[:,None]**2),-z2/2,-z2*z2/(4*kj),-ELL**2*D2/2,az),axis=-1)
 dm=np.stack((dV2/(2*om[:,None]**2),-dz2/2,-z2*dz2/(2*kj),-ELL**2*dD2/2,daz),axis=-1)
 primal=np.column_stack((-ALPHA*F2/4,-r2/2,np.einsum('j,jpk->pk',w,modal)))
 derivative=np.column_stack((-ALPHA*dF2/4,-dr2/2,np.einsum('j,jpk->pk',w,dm)))
 lm=np.einsum('pab,pba->p',hi,q)/2
 total=derivative+lm[:,None]*primal
 # Sum absolute tensor products BEFORE contractions or inter-term cancellation.
 def quad_env(hh,v):return np.einsum('pab,jpa,jpb->jp',abs(hh),abs(v),abs(v))
 ez=quad_env(hi,z);ev=quad_env(hi,s['V']);ed=np.einsum('pac,jpab,pbd,jpcd->jp',abs(hi),abs(s['D']),abs(hi),abs(s['D']))
 edz=quad_env(dhi,z);edv=quad_env(dhi,s['V'])+2*np.sum(abs(raise_cov(hi,s['V'])*dV),axis=-1)
 edd=2*np.sum(abs(Du*dD),axis=(2,3))+np.einsum('pac,jpab,pbd,jpcd->jp',abs(dhi),abs(s['D']),abs(hi),abs(s['D']))+np.einsum('pac,jpab,pbd,jpcd->jp',abs(hi),abs(s['D']),abs(dhi),abs(s['D']))
 ef=np.einsum('pac,pab,pbd,pcd->p',abs(hi),abs(s['F']),abs(hi),abs(s['F']))
 edf=2*np.sum(abs(s['Fup']*dF),axis=(1,2))+np.einsum('pac,pab,pbd,pcd->p',abs(dhi),abs(s['F']),abs(hi),abs(s['F']))+np.einsum('pac,pab,pbd,pcd->p',abs(hi),abs(s['F']),abs(dhi),abs(s['F']))
 er=np.einsum('pab,pa,pb->p',abs(hi),abs(s['r']),abs(s['r']));edr=np.einsum('pab,pa,pb->p',abs(dhi),abs(s['r']),abs(s['r']))+2*np.sum(abs(raise_cov(hi,s['r'])*dr),axis=-1)
 mp=np.stack((ev/(2*om[:,None]**2),ez/2,ez*ez/(4*kj),ELL**2*ed/2,np.sum(abs(s['a'][None,:,:]*z),axis=-1)),axis=-1)
 em=np.stack((edv/(2*om[:,None]**2),edz/2,ez*edz/(2*kj),ELL**2*edd/2,np.sum(abs(da[None,:,:]*z),axis=-1)),axis=-1)
 el=np.einsum('pab,pba->p',abs(hi),abs(q))/2
 penv=np.column_stack((ALPHA*ef/4,er/2,np.einsum('j,jpk->pk',w,mp)))
 denv=np.column_stack((ALPHA*edf/4,edr/2,np.einsum('j,jpk->pk',w,em)))
 env=denv+el[:,None]*penv
 per_mode=w[:,None,None]*(dm+lm[None,:,None]*modal)
 menv=w[:,None,None]*(em+el[None,:,None]*mp)
 operands=dict(delta_connection=dG,delta_inverse=dhi,delta_U=eta,delta_U_partial=deta,log_measure_tangent=lm,raw_native_primal=primal,raw_native_no_measure=derivative,per_mode_metric_terms=per_mode,per_mode_metric_envelope=menv)
 RAW.update({'current_metric_'+k:v for k,v in operands.items()})
 return total,env,operands


def metric_basis():
 e=np.zeros((6,3,3))
 for k,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):e[k,i,j]=e[k,j,i]=1
 return e


def symmetric_tensor_from_coordinates(p):
 t=np.zeros((len(p),3,3));t[:,0,0]=p[:,0];t[:,1,1]=p[:,1];t[:,2,2]=p[:,2]
 for k,(i,j) in enumerate(((0,1),(0,2),(1,2)),start=3):t[:,i,j]=t[:,j,i]=p[:,k]/2
 return t


def adm_chart(s):
 # Independent configuration is U_i and every z_ji, all spatial covectors.
 g,hi,U,z=s['g'],s['hi'],s['U'],s['z'];p=len(U)
 h=g[:,1:,1:];ih=np.linalg.inv(h);N=1/np.sqrt(-hi[:,0,0]);beta=N[:,None]**2*hi[:,0,1:]
 assert np.all(N>0) and np.all(np.linalg.eigvalsh(h)>0)
 uc=lower(g,U);u=uc[:,1:];up=np.einsum('pij,pj->pi',ih,u);gamma=np.sqrt(1+np.sum(u*up,axis=1))
 rebuilt=np.column_stack((gamma/N,up-beta*gamma[:,None]/N[:,None]))
 zt=-np.einsum('pi,jpi->jp',rebuilt[:,1:],z[:,:,1:])/rebuilt[None,:,0]
 JU=np.empty((p,4,3));JU[:,0]=up/(N*gamma)[:,None];JU[:,1:]=ih-beta[:,:,None]*JU[:,None,0,:]
 JzU=-np.einsum('jpa,pai->jpi',z,JU)/U[None,:,0,None]
 Jzz=-U[:,1:]/U[:,0,None]
 e=metric_basis();embed=np.zeros((p,6,4,4));embed[:,:,1:,1:]=e[None,:,:,:]
 embed[:,:,0,1:]=np.einsum('kij,pj->pki',e,beta);embed[:,:,1:,0]=embed[:,:,0,1:]
 embed[:,:,0,0]=np.einsum('pi,kij,pj->pk',beta,e,beta)
 dgamma=-np.einsum('pi,kij,pj->pk',up,e,up)/(2*gamma[:,None])
 Uh=np.empty((p,6,4));Uh[:,:,0]=dgamma/N[:,None]
 Uh[:,:,1:]=-np.einsum('pij,kjl,pl->pki',ih,e,up)-beta[:,None,:]*Uh[:,:,0,None]
 zh=-np.einsum('jpa,pka->jpk',z,Uh)/U[None,:,0,None]
 dens=np.sqrt(-np.linalg.det(g));sqrt_h=np.sqrt(np.linalg.det(h))
 dg=metric_partial(s);udot=np.einsum('pia,pa->pi',dg[:,0,1:,:],U)+lower_last(g,s['du'])[:,0,1:]
 zdot=s['dz'][:,:,0,1:]
 old_velocity=np.concatenate((udot,zdot.transpose(1,0,2).reshape(p,96)),axis=1)
 # Kplus = projected nabla n = N Gamma^0_ij; this is the declared stationary trial K.
 K=N[:,None,None]*s['Ga'][:,0,1:,1:];Kup=np.einsum('pik,pkl,plj->pij',ih,K,ih);Kt=np.einsum('pij,pij->p',ih,K)
 pEH=sqrt_h[:,None,None]*(Kup-Kt[:,None,None]*ih)/(2*C)
 GEH=sqrt_h[:,None,None]/(4*N[:,None,None]*C)*(np.einsum('aij,pjk,bkl,pli->pab',e,ih,e,ih)-np.einsum('pij,kij->pk',ih,e)[:,:,None]*np.einsum('pij,kij->pk',ih,e)[:,None,:])
 return dict(h=h,ih=ih,N=N,beta=beta,u=u,up=up,gamma=gamma,rebuilt_U=rebuilt,rebuilt_zt=zt,JU=JU,JzU=JzU,Jzz=Jzz,embed=embed,Uh=Uh,zh=zh,dens=dens,sqrt_h=sqrt_h,old_velocity=old_velocity,K=K,Ktrace=Kt,pi_EH=pEH,EH_Hessian=GEH)


def connection_momentum(s,Pi=None,Fup=None):
 Pi=s['Pi'] if Pi is None else Pi;Fup=s['Fup'] if Fup is None else Fup
 Z=s['Z'];U=s['U'];z=s['z'];hi=s['hi']
 sym=(Pi+np.swapaxes(Pi,2,3))/2
 Klo=np.einsum('pl,pa,pb->plab',Z,U,U)-np.einsum('jpab,jpl->plab',sym,z)
 Kup=np.einsum('plm,pmab->plab',hi,Klo)
 D=(Kup.transpose(0,2,1,3)+Kup.transpose(0,2,3,1)-Kup)/2
 mx=-ALPHA*(Fup[:,:,:,None]*U[:,None,None,:]+Fup[:,:,None,:]*U[:,None,:,None])/2
 return D+mx,D,mx


def reduced_momenta(s,c,PiU=None,Pi=None,Ctime=None):
 PiU=s['PiU'] if PiU is None else PiU;Pi=s['Pi'] if Pi is None else Pi
 if Ctime is None:Ctime=connection_momentum(s)[0][:,0]
 pu=np.einsum('pa,pai->pi',PiU[:,0],c['JU'])+np.einsum('jp,jpi->pi',Pi[:,:,0,0],c['JzU'])
 pz=Pi[:,:,0,1:]+Pi[:,:,0,0,None]*c['Jzz'][None,:,:]
 py=c['dens'][:,None]*np.concatenate((pu,pz.transpose(1,0,2).reshape(len(pu),96)),axis=1)
 pmetric=c['dens'][:,None]*(np.einsum('pmn,pkmn->pk',Ctime,c['embed'])+np.einsum('pa,pka->pk',PiU[:,0],c['Uh'])+np.einsum('jp,jpk->pk',Pi[:,:,0,0],c['zh']))
 return py,pmetric


def connection_from_jet(hi,dg):
 p=len(hi);out=np.zeros((p,4,4,4))
 for a in range(4):
  for b in range(4):out[:,:,a,b]=np.einsum('plm,pm->pl',hi,dg[:,a,b,:]+dg[:,b,a,:]-dg[:,:,a,b])/2
 return out


def native_velocity_jet(s,c,y,k):
 # y has 99 reduced field velocities; k has six symmetric hdot coefficients.
 p=len(s['U']);y=np.broadcast_to(y,(p,99));k=np.broadcast_to(k,(p,6))
 du=np.zeros((p,4,4));dz=np.zeros((32,p,4,4));dg=np.zeros((p,4,4,4))
 du[:,0]=np.einsum('pai,pi->pa',c['JU'],y[:,:3])+np.einsum('pka,pk->pa',c['Uh'],k)
 dz[:,:,0,1:]=y[:,3:].reshape(p,32,3).transpose(1,0,2)
 dz[:,:,0,0]=np.einsum('jpi,pi->jp',c['JzU'],y[:,:3])+np.einsum('pi,jpi->jp',c['Jzz'],dz[:,:,0,1:])+np.einsum('jpk,pk->jp',c['zh'],k)
 dg[:,0]=np.einsum('pk,pkab->pab',k,c['embed'])
 return du,dz,dg,connection_from_jet(s['hi'],dg)


def kinetic_tangent(s,du,dz,dGa,ell=ELL):
 dn=du+np.einsum('pbal,pl->pab',dGa,s['U']);dnz=dz-np.einsum('plab,jpl->jpab',dGa,s['z'])
 dV=np.einsum('pab,jpb->jpa',s['P'],np.einsum('pa,jpab->jpb',s['U'],dnz))
 dD=np.einsum('pac,jpcd,pbd->jpab',s['P'],dnz,s['P'])
 dF=lower_last(s['g'],dn)-np.swapaxes(lower_last(s['g'],dn),1,2)
 dFu=np.einsum('pac,pcd,pdb->pab',s['hi'],dF,s['hi'])
 dPiU=-ALPHA*np.einsum('pac,pcb->pab',s['hi'],dF)
 dPi=s['w'][:,None,None,None]*(np.einsum('pa,jpb->jpab',s['U'],raise_cov(s['hi'],dV))/s['omega'][:,None,None,None]**2-ell**2*np.einsum('pac,jpcd,pdb->jpab',s['hi'],dD,s['hi']))
 # Acceleration.Z is linear in all velocities; subtract the constant connection vertex.
 zero=dict(s,Z=np.zeros_like(s['Z']));dC=connection_momentum(zero,dPi,dFu)[0]
 return dict(du=du,dz=dz,dg_connection=dGa,delta_nu=dn,delta_nz=dnz,delta_V=dV,delta_D=dD,delta_F=dF,delta_PiU=dPiU,delta_Pi=dPi,delta_Ctime=dC[:,0])


def ordinary_velocity(g,p):
 hi=np.linalg.inv(g);h=g[:,1:,1:];ih=np.linalg.inv(h);N=1/np.sqrt(-hi[:,0,0]);beta=N[:,None]**2*hi[:,0,1:]
 p=np.asarray(p);pu=np.einsum('pij,pj->pi',ih,p);gamma=np.sqrt(1+np.sum(p*pu,axis=1))
 u=np.column_stack((gamma/N,pu-beta*gamma[:,None]/N[:,None]));coordinate=N[:,None]*pu/gamma[:,None]-beta
 H=N*gamma-np.sum(beta*p,axis=1)
 return dict(u_M=u,coordinate_velocity=coordinate,gamma=gamma,specific_covariant_momentum=p,coordinate_time_Hamiltonian=H)


def arrowhead_blocks(s,c):
 # Full fixed-metric99 kinetic map, including every transverse azimuthal mode.
 U,P,hi=s['U'],s['P'],s['hi'];w,om=s['w'],s['omega']
 S=P[:,:,1:]+P[:,:,0,None]*c['Jzz'][:,None,:]
 T=P[None,:,:,0,None]*c['JzU'][:,:,None,:]
 cone=U[None,:,0]**2/om[:,None]**2-ELL**2*(hi[None,:,0,0]+U[None,:,0]**2)
 assert np.all(w>0) and np.all(cone>0) and np.all(c['N']>0)
 factor=c['dens'][None,:]*w[:,None]*cone
 gram=np.einsum('pai,pab,pbj->pij',S,hi,S)
 DD=factor[:,:,None,None]*gram[None]
 BB=factor[:,:,None,None]*np.einsum('jpai,pab,pbk->jpik',T,hi,S)
 AA_modes=factor[:,:,None,None]*np.einsum('jpai,pab,jpbk->jpik',T,hi,T)
 Maxwell=c['dens'][:,None,None]*ALPHA*c['ih']/c['N'][:,None,None]**2
 AA=Maxwell+AA_modes.sum(axis=0)
 RAW.update(arrowhead_S=S,arrowhead_T=T,arrowhead_native_cone=cone,arrowhead_factor=factor,arrowhead_transverse_Gram=gram,arrowhead_D=DD,arrowhead_B=BB,arrowhead_A_modes=AA_modes,arrowhead_A=AA,arrowhead_Maxwell_Schur=Maxwell)
 return dict(S=S,T=T,cone=cone,factor=factor,D=DD,B=BB,A_modes=AA_modes,A=AA,Maxwell=Maxwell)


def arrowhead_action(block,y):
 assert y.ndim==2 and y.shape[1]==99
 p=y.shape[0];uy=y[:,:3];zy=y[:,3:].reshape(p,32,3).transpose(1,0,2)
 au=np.einsum('pik,pk->pi',block['A'],uy)+np.einsum('jpik,jpk->pi',block['B'],zy)
 az=np.einsum('jpki,pk->jpi',block['B'],uy)+np.einsum('jpik,jpk->jpi',block['D'],zy)
 return np.concatenate((au,az.transpose(1,0,2).reshape(p,96)),axis=1)


def arrowhead_solve(block,rhs):
 assert rhs.ndim==3 and rhs.shape[1]==99
 # No subtraction of enormous modal Grams to recover the Maxwell Schur.
 # The exact transverse-span identity must first be certified against saved M.
 p=rhs.shape[0];rr=rhs[:,3:].reshape(p,32,3,-1).transpose(1,0,2,3)
 dsolve=np.linalg.solve(block['D'],rr);RAW['arrowhead_modal_elimination']=dsolve.copy()
 reduced=rhs[:,:3]-np.einsum('jpik,jpkl->pil',block['B'],dsolve)
 RAW['arrowhead_reduced_U_rhs']=reduced.copy()
 yu=np.linalg.solve(block['Maxwell'],reduced);RAW['arrowhead_U_solution']=yu.copy()
 modal_rhs=rr-np.einsum('jpki,pkl->jpil',block['B'],yu)
 RAW['arrowhead_modal_rhs']=modal_rhs.copy()
 yz=np.linalg.solve(block['D'],modal_rhs);RAW['arrowhead_mode_solution']=yz.copy()
 y=np.concatenate((yu,yz.transpose(1,0,2,3).reshape(p,96,-1)),axis=1)
 RAW.update(arrowhead_rhs=rhs,arrowhead_modal_elimination=dsolve,arrowhead_reduced_U_rhs=reduced,arrowhead_U_solution=yu,arrowhead_mode_solution=yz,arrowhead_solution=y)
 return y


def adm_first_jets(s,c):
 dg=metric_partial(s);dhi=-np.einsum('pbc,pacd,pde->pabe',s['hi'],dg,s['hi'])
 dN=.5*c['N'][:,None]**3*dhi[:,:,0,0]
 dbeta=2*c['N'][:,None,None]*dN[:,:,None]*s['hi'][:,None,0,1:]+c['N'][:,None,None]**2*dhi[:,:,0,1:]
 return dict(dg=dg,dhi=dhi,dN=dN,dbeta=dbeta,dh=dg[:,:,1:,1:])


def lapse_shift_lift(s,c,f,df,b,db):
 # Fixed h_ij,U_i,z_ji, phi and their independent jets. b^i=delta beta^i.
 jets=adm_first_jets(s,c);N,h,beta,U,z=c['N'],c['h'],c['beta'],s['U'],s['z']
 dN,dh,dbe=jets['dN'],jets['dh'],jets['dbeta'];p=len(U)
 q=np.zeros((p,4,4));dq=np.zeros((p,4,4,4));eta=np.zeros((p,4));deta=np.zeros((p,4,4))
 q[:,0,0]=-2*N*f+2*np.einsum('pi,pij,pj->p',beta,h,b)
 q[:,0,1:]=np.einsum('pij,pj->pi',h,b);q[:,1:,0]=q[:,0,1:]
 dq[:,:,0,0]=-2*dN*f[:,None]-2*N[:,None]*df+2*np.einsum('pai,pij,pj->pa',dbe,h,b)+2*np.einsum('pi,paij,pj->pa',beta,dh,b)+2*np.einsum('pi,pij,paj->pa',beta,h,db)
 dq[:,:,0,1:]=np.einsum('paij,pj->pai',dh,b)+np.einsum('pij,paj->pai',h,db);dq[:,:,1:,0]=dq[:,:,0,1:]
 eta[:,0]=-U[:,0]*f/N;eta[:,1:]=-U[:,0,None]*b-beta*eta[:,0,None]
 deta[:,:,0]=-s['du'][:,:,0]*f[:,None]/N[:,None]-U[:,0,None]*df/N[:,None]+U[:,0,None]*f[:,None]*dN/N[:,None]**2
 deta[:,:,1:]=-s['du'][:,:,0,None]*b[:,None,:]-U[:,0,None,None]*db-dbe*eta[:,None,0,None]-beta[:,None,:]*deta[:,:,0,None]
 zeta=np.zeros_like(z);dzeta=np.zeros_like(s['dz']);ez=np.einsum('pa,jpa->jp',eta,z)
 zeta[:,:,0]=-ez/U[None,:,0]
 dzeta[:,:,:,0]=-(np.einsum('pab,jpb->jpa',deta,z)+np.einsum('pb,jpab->jpa',eta,s['dz']))/U[None,:,0,None]+ez[:,:,None]*s['du'][None,:,:,0]/U[None,:,0,None]**2
 RAW.update(constraint_test_lapse=f,constraint_test_lapse_partial=df,constraint_test_shift=b,constraint_test_shift_partial=db,constraint_metric_test=q,constraint_metric_test_partial=dq,constraint_U_chain=eta,constraint_U_chain_partial=deta,constraint_z_chain=zeta,constraint_z_chain_partial=dzeta)
 return dict(q=q,dq=dq,eta=eta,deta=deta,zeta=zeta,dzeta=dzeta,ADM_jets=jets)


def absolute_phase_metric_row(s,q,Pstar,Wstar):
 raised=raise_cov(s['hi'],s['phi']);X2=-covdot(s['hi'],s['phi'],s['phi'])
 dl=np.einsum('pa,pab,pb->p',raised,q,raised)/(2*X2)
 measure=np.einsum('pab,pba->p',s['hi'],q)/2
 value=Wstar*dl+Pstar*measure
 envelope=abs(Wstar)*np.einsum('pa,pab,pb->p',abs(raised),abs(q),abs(raised))/(2*X2)+abs(Pstar)*np.einsum('pab,pba->p',abs(s['hi']),abs(q))/2
 return value,envelope


def native_phase_constraint_direction(s,c,f,df,b,db,Pstar,Wstar,R):
 lift=lapse_shift_lift(s,c,f,df,b,db)
 native,en,*_=metric_native(s,lift['q'],lift['dq'],lift['eta'],lift['deta'])
 modal,me,*_=variation(s,np.zeros_like(s['U']),np.zeros_like(s['du']),lift['zeta'],lift['dzeta'])
 phase,pe=absolute_phase_metric_row(s,lift['q'],Pstar,Wstar)
 ratio=c['dens']/R
 action_components=ratio[:,None]*np.column_stack((native.sum(axis=1),modal.sum(axis=1),phase))
 envelope=ratio[:,None]*np.column_stack((en.sum(axis=1),me.sum(axis=1),pe))
 # Hamiltonian source derivative at fixed canonical state is minus action derivative.
 return dict(Hamiltonian_components=-action_components,action_components=action_components,envelope=envelope,lift=lift)


def spatial_generator_density(s,c,py,pmetric,p_phi,b,db,R):
 # Total metric momentum is native chart+connection PLUS EH in the same representative.
 jets=adm_first_jets(s,c);u=c['u'];zi=s['z'][:,:,1:]
 dUcov=np.einsum('pajm,pm->paj',jets['dg'][:,:,1:,:],s['U'])+np.einsum('pjm,pam->paj',s['g'][:,1:,:],s['du'])
 Lie_h=np.einsum('pk,pkij->pij',b,jets['dh'][:,1:])+np.einsum('pik,pjk->pij',c['h'],db[:,1:])+np.einsum('pkj,pik->pij',c['h'],db[:,1:])
 Lie_u=np.einsum('pk,pkj->pj',b,dUcov[:,1:])+np.einsum('pk,pjk->pj',u,db[:,1:])
 Lie_z=np.einsum('pk,jpkm->jpm',b,s['dz'][:,:,1:,1:])+np.einsum('jpk,pmk->jpm',zi,db[:,1:])
 metric=np.einsum('pij,pij->p',pmetric,Lie_h)
 preferred=np.einsum('pi,pi->p',py[:,:3],Lie_u)
 mode=np.einsum('jpi,jpi->p',py[:,3:].reshape(len(py),32,3).transpose(1,0,2),Lie_z)
 phase=p_phi*np.einsum('pi,pi->p',b,s['phi'][:,1:])
 return np.column_stack((metric,preferred,mode,phase))/R[:,None]


def spatial_curvature_weak_density(s,c,f,df,R):
 # Complete first-derivative R3 weak representative in flat cylindrical reference.
 # Output is divided by reference R. Integrate with the authentic R dR dZ weight.
 # Reflected internal sheet distributions belong to this global weak form once.
 jets=adm_first_jets(s,c);dh=jets['dh'][:,1:];ih=c['ih'];p=len(R)
 Ga=np.zeros((p,3,3,3))
 for i in range(3):
  for j in range(3):Ga[:,:,i,j]=np.einsum('plm,pm->pl',ih,dh[:,i,j,:]+dh[:,j,i,:]-dh[:,:,i,j])/2
 bar=np.zeros_like(Ga);bar[:,0,2,2]=-R;bar[:,2,0,2]=bar[:,2,2,0]=1/R
 cc=Ga-bar;tr=np.einsum('plil->pi',cc)
 ratio=c['sqrt_h']/R;dratio=ratio[:,None]*np.einsum('pij,paij->pa',ih,dh)/2;dratio[:,0]-=ratio/R
 dih=-np.einsum('pij,pajk,pkl->pail',ih,dh,ih)
 V=f[:,None,None]*ratio[:,None,None]*ih
 DV=(df[:,1:]*ratio[:,None]+f[:,None]*dratio)[:,:,None,None]*ih[:,None]+f[:,None,None,None]*ratio[:,None,None,None]*dih
 DV+=np.einsum('pial,plj->paij',bar,V)+np.einsum('pjal,pil->paij',bar,V)
 aa=np.einsum('pkij,pk->pij',cc,tr)-np.einsum('plik,pkjl->pij',cc,cc)
 one=-np.einsum('plij,plij->p',DV,cc)
 two=np.einsum('pjij,pi->p',DV,tr)
 three=np.einsum('pij,pij->p',V,aa)
 eGa=np.zeros_like(Ga)
 for i in range(3):
  for j in range(3):eGa[:,:,i,j]=np.einsum('plm,pm->pl',abs(ih),abs(dh[:,i,j,:])+abs(dh[:,j,i,:])+abs(dh[:,:,i,j]))/2
 ecc=eGa+abs(bar);etr=np.einsum('plil->pi',ecc)
 edratio=ratio[:,None]*(np.einsum('pij,paij->pa',abs(ih),abs(dh))/2);edratio[:,0]+=ratio/R
 edih=np.einsum('pij,pajk,pkl->pail',abs(ih),abs(dh),abs(ih))
 eV=abs(f)[:,None,None]*ratio[:,None,None]*abs(ih)
 eDV=(abs(df[:,1:])*ratio[:,None]+abs(f[:,None])*edratio)[:,:,None,None]*abs(ih[:,None])+abs(f[:,None,None,None])*ratio[:,None,None,None]*edih
 eDV+=np.einsum('pial,plj->paij',abs(bar),eV)+np.einsum('pjal,pil->paij',abs(bar),eV)
 eaa=np.einsum('pkij,pk->pij',ecc,etr)+np.einsum('plik,pkjl->pij',ecc,ecc)
 envelope=np.einsum('plij,plij->p',eDV,ecc)+np.einsum('pjij,pi->p',eDV,etr)+np.einsum('pij,pij->p',eV,eaa)
 RAW.update(ADM_curvature_connection_envelope=ecc,ADM_curvature_V_envelope=eV,ADM_curvature_DV_envelope=eDV)
 RAW.update(ADM_spatial_connection=Ga,ADM_spatial_reference_connection=bar,ADM_spatial_connection_difference=cc,ADM_curvature_V=V,ADM_curvature_reference_DV=DV,ADM_curvature_terms=np.column_stack((one,two,three)),ADM_curvature_uncancelled_envelope=envelope)
 return dict(value=one+two+three,envelope=envelope,terms=np.column_stack((one,two,three)),unknown_outer_port=None,internal_sheet='reflected global weak distribution once; no added synthetic jump')


def EH_ADM_constraint_direction(s,c,f,df,b,db,R):
 curv=spatial_curvature_weak_density(s,c,f,df,R)
 ratio=c['sqrt_h']/R;K=c['K'];ih=c['ih'];Kt=c['Ktrace']
 K2=np.einsum('pij,pik,pjl,pkl->p',K,ih,ih,K)
 kinetic=ratio*f*(K2-Kt**2)/(2*C)
 # Positive Hamiltonian shift row from the full metric Lie derivative.
 jets=adm_first_jets(s,c)
 Lie_h=np.einsum('pk,pkij->pij',b,jets['dh'][:,1:])+np.einsum('pik,pjk->pij',c['h'],db[:,1:])+np.einsum('pkj,pik->pij',c['h'],db[:,1:])
 shift=np.einsum('pij,pij->p',c['pi_EH'],Lie_h)/R
 normal=kinetic-curv['value']/(2*C)
 ek=ratio*abs(f)*(np.einsum('pij,pik,pjl,pkl->p',abs(K),abs(ih),abs(ih),abs(K))+np.einsum('pij,pij->p',abs(ih),abs(K))**2)/(2*C)
 eLie=np.einsum('pk,pkij->pij',abs(b),abs(jets['dh'][:,1:]))+np.einsum('pik,pjk->pij',abs(c['h']),abs(db[:,1:]))+np.einsum('pkj,pik->pij',abs(c['h']),abs(db[:,1:]))
 es=np.einsum('pij,pij->p',abs(c['pi_EH']),eLie)/R
 return dict(normal=normal,shift=shift,normal_envelope=ek+curv['envelope']/(2*C),shift_envelope=es,curvature=curv,paired_GHY_time_port=None,outer_geometry_port=None)


def ordinary_canonical_constraint_rows(g,p_specific,mass_weight,f,b):
 o=ordinary_velocity(g,p_specific)
 normal=mass_weight*o['gamma']*f
 shift=-mass_weight*np.einsum('pi,pi->p',p_specific,b)
 return dict(normal=normal,shift=shift,gamma=o['gamma'],source_support='fixed owned razor-thin rest-mass annuli; no3D density or unknown activity extension')


def chart_operation_envelopes(s,c):
 # u_i=g_i,nu U^nu; propagate its CANCELING contraction before h^-1 and JU.
 N,ga,be,ih=c['N'],c['gamma'],c['beta'],c['ih'];U,z=s['U'],s['z']
 eu=np.einsum('pia,pa->pi',abs(s['g'][:,1:,:]),abs(U))
 RAW['operation_chart_u_cov_envelope']=eu.copy()
 eup=np.einsum('pij,pj->pi',abs(ih),eu)
 RAW['operation_chart_up_envelope']=eup.copy()
 eU=np.column_stack((ga/N,eup+abs(be)*ga[:,None]/N[:,None]))
 RAW['operation_chart_rebuilt_U_envelope']=eU.copy()
 ezt=np.einsum('jpi,pi->jp',abs(z[:,:,1:]),eU[:,1:])/abs(c['rebuilt_U'][None,:,0])
 RAW['operation_chart_rebuilt_zt_envelope']=ezt.copy()
 eJU=np.zeros_like(c['JU']);eJU[:,0]=eup/(N*ga)[:,None]
 eJU[:,1:]=abs(ih)+abs(be)[:,:,None]*eJU[:,None,0,:]
 RAW['operation_chart_JU_envelope']=eJU.copy()
 eJzU=np.einsum('jpa,pai->jpi',abs(z),eJU)/abs(U[None,:,0,None])
 RAW['operation_chart_JzU_envelope']=eJzU.copy()
 eJzz=np.maximum(eU[:,1:],abs(U[:,1:]))/abs(U[:,0,None])
 RAW['operation_chart_Jzz_envelope']=eJzz.copy()
 # EXACT order of the preexisting rational-chart actual/expected vectors.
 ordered=np.r_[eU.ravel(),ezt.ravel(),eJU.ravel(),eJzz.ravel(),eJzU.ravel(),
               abs(N),abs(ga),abs(c['dens'])]
 RAW['operation_chart_certificate_envelope']=ordered.copy()
 return dict(u_cov=eu,up=eup,rebuilt_U=eU,rebuilt_zt=ezt,JU=eJU,JzU=eJzU,Jzz=eJzz,
             certificate_envelope=ordered)


def momentum_envelope(s,c):
 # Propagate original covariant jets/projectors and additive momenta before cancellation.
 ce=chart_operation_envelopes(s,c);g,hi,U,z=s['g'],s['hi'],s['U'],s['z']
 euc=np.einsum('pab,pb->pa',abs(g),abs(U));eP=np.eye(4)[None]+np.einsum('pa,pb->pab',euc,abs(U))
 enu=s.get('operation_nu_envelope',abs(s['du'])+np.einsum('pbal,pl->pab',abs(s['Ga']),abs(U)))
 enz=s.get('operation_nz_envelope',abs(s['dz'])+np.einsum('plab,jpl->jpab',abs(s['Ga']),abs(z)))
 eV=np.einsum('pab,jpb->jpa',eP,np.einsum('pa,jpab->jpb',abs(U),enz))
 eD=np.einsum('pac,jpcd,pbd->jpab',eP,enz,eP)
 eg=lower_last(abs(g),enu);eF=eg+np.swapaxes(eg,1,2)
 eZ=np.einsum('j,jpa->pa',s['w'],abs(z))
 ePiU=ALPHA*np.einsum('pac,pcb->pab',abs(hi),eF)+np.einsum('pa,pb->pab',abs(U),eZ)
 ePi=s['w'][:,None,None,None]*(np.einsum('pa,jpb->jpab',abs(U),raise_cov(abs(hi),eV))/s['omega'][:,None,None,None]**2+ELL**2*np.einsum('pac,jpcd,pdb->jpab',abs(hi),eD,abs(hi)))
 RAW.update(operation_momentum_covariant_U_envelope=enu,operation_momentum_covariant_z_envelope=enz,operation_momentum_projector_envelope=eP,operation_momentum_PiU_envelope=ePiU,operation_momentum_Pi_envelope=ePi)
 pu=np.einsum('pa,pai->pi',ePiU[:,0],ce['JU'])+np.einsum('jp,jpi->pi',ePi[:,:,0,0],ce['JzU'])
 pz=ePi[:,:,0,1:]+ePi[:,:,0,0,None]*ce['Jzz'][None,:,:]
 return c['dens'][:,None]*np.concatenate((pu,pz.transpose(1,0,2).reshape(len(pu),96)),axis=1)


def arrowhead_operation_envelopes(s,c,chartenv=None,label='current'):
 # If the producer already stored the admitted chart operation envelopes, pass
 # them here. Otherwise its owner may run that same positive helper once; this
 # neither reconstructs a signed kinetic Gram nor solves a modal block.
 if chartenv is None:chartenv=chart_operation_envelopes(s,c)
 U,g,hi=s['U'],s['g'],s['hi'];w,om=s['w'],s['omega']
 p=len(U);assert U.shape==(p,4) and g.shape==hi.shape==(p,4,4)
 assert w.shape==om.shape==(32,) and np.all(om>0) and np.all(w>0)
 assert chartenv['Jzz'].shape==(p,3) and chartenv['JzU'].shape==(32,p,3)
 out={}
 def keep(name,value):
  RAW['operation_arrowhead_'+label+'_'+name]=value.copy()
  out[name]=value
  assert np.issubdtype(value.dtype,np.number) and np.all(np.isfinite(value))
  assert np.all(value>=0)
  return value
 # P_a^b=delta_a^b+(g_ac U^c)U^b. Its magnitude must precede cancellation
 # in P_0^0 and in the compensated spatial-covector columns S and T.
 euc=keep('U_cov',np.einsum('pab,pb->pa',abs(g),abs(U)))
 eP=keep('P',np.eye(4)[None]+euc[:,:,None]*abs(U)[:,None,:])
 eS=keep('S',eP[:,:,1:]+eP[:,:,0,None]*chartenv['Jzz'][:,None,:])
 eT=keep('T',eP[None,:,:,0,None]*chartenv['JzU'][:,:,None,:])
 # The actual cone is U0^2/omega^2-ell^2(hi00+U0^2). Keep all three
 # terms positive here, including the inner hi00+U0^2 cancellation.
 eU02=abs(U[None,:,0])**2
 econe=keep('cone',eU02/abs(om[:,None])**2
             +ELL**2*(abs(hi[None,:,0,0])+eU02))
 efactor=keep('factor',abs(c['dens'])[None,:]*abs(w)[:,None]*econe)
 ehi=abs(hi)
 egram=keep('transverse_Gram',np.einsum('pai,pab,pbj->pij',eS,ehi,eS))
 eD=keep('D',efactor[:,:,None,None]*egram[None])
 eB=keep('B',efactor[:,:,None,None]
         *np.einsum('jpai,pab,pbk->jpik',eT,ehi,eS))
 eAm=keep('A_modes',efactor[:,:,None,None]
          *np.einsum('jpai,pab,jpbk->jpik',eT,ehi,eT))
 eMaxwell=keep('Maxwell',abs(c['dens'])[:,None,None]*abs(ALPHA)
               *abs(c['ih'])/abs(c['N'])[:,None,None]**2)
 keep('A',eMaxwell+eAm.sum(axis=0))
 return out


def arrowhead_original_envelope(block,y,rhs):
 if 'operation_A' in block:return arrowhead_original_operation_envelope(block,y,rhs)
 uy=abs(y[:,:3]);zy=abs(y[:,3:].reshape(len(y),32,3).transpose(1,0,2))
 eu=np.einsum('pik,pk->pi',abs(block['Maxwell'])+abs(block['A_modes']).sum(axis=0),uy)+np.einsum('jpik,jpk->pi',abs(block['B']),zy)
 ez=np.einsum('jpki,pk->jpi',abs(block['B']),uy)+np.einsum('jpik,jpk->jpi',abs(block['D']),zy)
 return np.concatenate((eu,ez.transpose(1,0,2).reshape(len(y),96)),axis=1)+abs(rhs)


def arrowhead_original_operation_envelope(block,y,rhs):
 # Positive block fields are installed by span_operation_envelopes at q0.
 # Install the same fields after arrowhead_operation_envelopes for q1..q3.
 # Old synthetic fixtures need not be replayed or re-registered.
 names=('A','B','D');assert all('operation_'+name in block for name in names)
 envelope={name:block['operation_'+name] for name in names}
 return arrowhead_saved_action_operation_envelope(envelope,y,rhs)


def arrowhead_saved_action_operation_envelope(envelope,y,rhs):
 # Same 99 coordinates and original residual as arrowhead_original_envelope.
 # Use for each of seven saved Y columns and for every full-q owned-K residual.
 # Every signed A/B/D action remains the producer's original stored/action row.
 assert y.ndim==2 and y.shape[1]==99 and rhs.shape==y.shape
 p=len(y);uy=abs(y[:,:3]);zy=abs(y[:,3:].reshape(p,32,3).transpose(1,0,2))
 assert envelope['A'].shape==(p,3,3)
 assert envelope['B'].shape==envelope['D'].shape==(32,p,3,3)
 eu=np.einsum('pik,pk->pi',envelope['A'],uy)
 eu+=np.einsum('jpik,jpk->pi',envelope['B'],zy)
 ez=np.einsum('jpki,pk->jpi',envelope['B'],uy)
 ez+=np.einsum('jpik,jpk->jpi',envelope['D'],zy)
 result=np.concatenate((eu,ez.transpose(1,0,2).reshape(p,96)),axis=1)+abs(rhs)
 assert np.all(np.isfinite(result)) and np.all(result>=0)
 return result


def reconstruct_owned_K(s,c,block,Hbar,label):
 # Prescribed initial K increment only: all metric positions and all native p stay
 # fixed. This does not hold the old total metric p fixed or earn a history.
 kten=2*c['N'][:,None,None]*Hbar*c['h']
 k=np.column_stack((kten[:,0,0],kten[:,1,1],kten[:,2,2],kten[:,0,1],kten[:,0,2],kten[:,1,2]))
 py,ph=reduced_momenta(s,c);du,dz,dg,dGa=native_velocity_jet(s,c,np.zeros((len(py),99)),k)
 kt=kinetic_tangent(s,du,dz,dGa);delta,_=reduced_momenta(s,c,kt['delta_PiU'],kt['delta_Pi'],kt['delta_Ctime'])
 ARM_AVAILABLE.update({label+'owned_hdot_tensor':kten,label+'owned_hdot_coordinates':k,label+'old_native_canonical_momentum':py,label+'metric_only_native_momentum_delta':delta})
 y=arrowhead_solve(block,-delta[:,:,None])[:,:,0]
 ARM_AVAILABLE[label+'reconstructed_native_velocity_delta']=y.copy()
 action=arrowhead_action(block,y);env=arrowhead_original_envelope(block,y,-delta)
 ARM_AVAILABLE.update({label+'original_native_block_action':action,label+'original_native_rhs':-delta,label+'original_native_residual':action+delta,label+'original_native_residual_envelope':env})
 du,dz,dg,dGa=native_velocity_jet(s,c,y,k)
 new=features(s['g'],s['hi'],s['Ga']+dGa,s['U'],s['du']+du,s['z'],s['dz']+dz,s['phi'],s['omega'],s['xi'],s['w']);nc=adm_chart(new)
 nmp,nph=reduced_momenta(new,nc);m_env=momentum_envelope(new,nc)+momentum_envelope(s,c)
 constraints=np.concatenate((np.einsum('pa,pa->p',new['uc'],new['U'])+1,np.einsum('pa,jpa->jp',new['U'],new['z']).ravel(),2*np.einsum('pab,pb->pa',lower_last(new['g'],new['nu']),new['U']).ravel(),(np.einsum('pab,jpb->jpa',new['nu'],new['z'])+np.einsum('pb,jpab->jpa',new['U'],new['nz'])).ravel()))
 # Operation bounds, not normalization by exact-zero cancellation remainders.
 unenv=abs(new['du'])+np.einsum('pbal,pl->pab',abs(new['Ga']),abs(new['U']))
 znenv=abs(new['dz'])+np.einsum('plab,jpl->jpab',abs(new['Ga']),abs(new['z']))
 cenv=np.concatenate((np.einsum('pa,pa->p',abs(new['uc']),abs(new['U']))+1,np.einsum('pa,jpa->jp',abs(new['U']),abs(new['z'])).ravel(),(2*np.einsum('pab,pb->pa',lower_last(abs(new['g']),unenv),abs(new['U']))).ravel(),(np.einsum('pab,jpb->jpa',unenv,abs(new['z']))+np.einsum('pb,jpab->jpa',abs(new['U']),znenv)).ravel()))
 Kgap=nc['K']-c['K'];Kexpected=Hbar*c['h'];Kenv=abs(nc['K'])+abs(c['K'])+abs(Kexpected)
 for key,value in dict(native_p=nmp,metric_native_p=nph,metric_EH_p=nc['pi_EH'],metric_total_p=symmetric_tensor_from_coordinates(nph)+nc['pi_EH'],du_increment=du,dz_increment=dz,dg_increment=dg,connection_increment=dGa,new_K=nc['K'],old_K=c['K'],K_increment=Kgap,K_expected=Kexpected,native_p_reconstruction_envelope=m_env,constraints=constraints,constraint_envelope=cenv).items():ARM_AVAILABLE[label+key]=value.copy()
 return new,nc,dict(action=action,rhs=-delta,action_envelope=env,native_p=nmp,old_native_p=py,momentum_envelope=m_env,constraints=constraints,constraint_envelope=cenv,Kgap=Kgap,Kexpected=Kexpected,Kenv=Kenv)


def now():return datetime.now(timezone.utc).isoformat()


def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p


def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()


def canonical(v):
 if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
 if np is not None and isinstance(v,np.generic):return canonical(v.item())
 if v is None or type(v) in (str,bool,int):return v
 if type(v) is float and math.isfinite(v):return v
 raise TypeError('Unsupported/nonfinite metadata '+type(v).__name__)


def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def publish(n,raw):
 p=path(n)
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==raw;OUTPUTS[n]=sha(p);return OUTPUTS[n]


def json_file(n,v):return publish(n,encode(v))


def check(label,actual,expected,envelope):
 a=np.asarray(actual);b=np.asarray(expected);e=np.asarray(envelope);k=len(CHECKS)
 CONTEXT.update(control=label,ordinal=k)
 for n,v in (('actual',a),('expected',b),('envelope',e)):RAW[f'control_{k:03d}_{label}_{n}']=v.copy()
 assert a.shape==b.shape==e.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(np.isfinite(e)) and np.all(e>=0)
 error=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0));row=dict(ordinal=k,name=label,error=error,tolerance=TOL,passed=error<=TOL);CHECKS.append(row)
 assert row['passed'],(label,error)


def checkpoint(tag,arrays,meta,failed=False):
 schema={}
 for k,a in arrays.items():
  assert isinstance(a,np.ndarray) and a.dtype.kind in 'fiub'
  finite=bool(np.all(np.isfinite(a)));assert failed or finite,k
  schema[k]=dict(shape=list(a.shape),dtype=str(a.dtype),finite=finite)
 md=json.loads(encode(dict(meta,owner=OWNER,qualification=FLAGS,schema=schema,failed=failed)).decode())
 text=encode(md).decode();name=f'{STEM}_{len(RECORDS):05d}_{tag}.npz';p=path(name)
 with p.open('xb') as f:np.savez_compressed(f,metadata_json=np.array(text),**arrays);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);OUTPUTS[name]=sha(p);rec=dict(file=name,sha256=OUTPUTS[name],metadata=md);cf=name+'.COMMIT.json';ch=json_file(cf,rec)
 rec=dict(rec,commit_file=cf,commit_sha256=ch);RECORDS.append(rec)
 with np.load(p,allow_pickle=False) as f:
  assert str(f['metadata_json'])==text and set(f.files)==set(arrays)|{'metadata_json'}
  for k,a in arrays.items():assert f[k].shape==a.shape and f[k].dtype==a.dtype and np.array_equal(f[k],a,equal_nan=True),k
 return rec


def recheck(strict=True):
 for n,h in INPUTS.items():assert sha(path(n))==h,('input changed',n)
 assert sha(__file__)==OWNER['source_sha256']
 for n,h in OUTPUTS.items():assert sha(path(n))==h,('output changed',n)
 for r in RECORDS:
  assert json.loads(path(r['commit_file']).read_text())=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
  with np.load(path(r['file']),allow_pickle=False) as f:
   assert json.loads(str(f['metadata_json']))==r['metadata'] and set(f.files)==set(r['metadata']['schema'])|{'metadata_json'}
   for n,s in r['metadata']['schema'].items():assert list(f[n].shape)==s['shape'] and str(f[n].dtype)==s['dtype'] and bool(np.all(np.isfinite(f[n])))==s['finite']
 if strict:
  assert path(STEM+'_OWNER_START.json').read_bytes()==encode(OWNER)
  assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={r['file'] for r in RECORDS}
  assert {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in RECORDS}


def seal_actual():
 for p in sorted(BASE.glob(STEM+'_*')):
  if p.is_file():p.chmod(0o444);OUTPUTS[p.name]=sha(p)


def read_pair(rec,names):
 assert sha(path(rec['file']))==rec['sha256'] and sha(path(rec['commit_file']))==rec['commit_sha256']
 assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 out={};metadata_key='metadata' if rec['file'].startswith(BAND+'_') else 'metadata_json'
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert set(f.files)==set(rec['metadata']['schema'])|{metadata_key}
  assert json.loads(str(f[metadata_key]))==rec['metadata']
  for n in names:
   a=f[n].copy();RAW['loaded_'+n]=a
   s=rec['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and np.all(np.isfinite(a)),n
   out[n]=a
 return out


def authenticate_helpers():
 # Compile/AST source comparison only; the copied definitions are not imported.
 trees={}
 own=ast.parse(Path(__file__).read_text());own_defs={n.name:n for n in own.body if isinstance(n,ast.FunctionDef)}
 for row in HELPER_SPANS:
  if row['file'] not in trees:
   text=path(row['file']).read_text();tree=ast.parse(text);trees[row['file']]=(text,{n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)})
  text,defs=trees[row['file']];node=defs[row['name']]
  assert node.lineno==row['first'] and node.end_lineno==row['last']
  raw=ast.get_source_segment(text,node)+'\n';assert hashlib.sha256(raw.encode()).hexdigest()==row['sha256']
  assert ast.dump(node,include_attributes=False)==ast.dump(own_defs[row['name']],include_attributes=False)


def scatter_q1(values,weight,shapes,nr,nz):
 loads=np.zeros((values.shape[1],nr,nz));cell=(nr-1,nz-1)
 for N,NR,NZ,i,j in shapes:loads[:,i:nr-1+i,j:nz-1+j]+=np.moveaxis((values*weight[:,None]*N).reshape(cell+(values.shape[1],)),-1,0)
 return loads


def resolve_record(ref):
 assert sha(path(ref['file']))==ref['sha256'] and sha(path(ref['commit_file']))==ref['commit_sha256']
 out=json.loads(path(ref['commit_file']).read_text())
 assert out['file']==ref['file'] and out['sha256']==ref['sha256']
 return dict(out,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'])

def admission():
 ins={}
 def add(n,h):
  n=str(path(n).resolve());assert isinstance(h,str) and len(h)==64 and (n not in ins or ins[n]==h);ins[n]=h
 for n,h in PINS.items():add(n,h)
 add(STEM+'.md',PROTOCOL_SHA);add(__file__,sha(__file__));parents={}
 for st in (WHOLE,COMPACT,METRIC,ORDINARY):
  r=json.loads(path(st+'_RESULT.json').read_text());rc=json.loads(path(st+'_RECEIPT.json').read_text())
  assert rc['status']=='CLOSED' and rc['owner']==r['owner'] and rc['result_sha256']==PINS[st+'_RESULT.json']
  assert all(v is False for v in r['qualification'].values())
  for key in ('input_sha256','output_sha256'):
   for n,h in rc[key].items():add(n,h)
  parents[st]=(r,rc)
 for n,h in ins.items():assert sha(path(n))==h,n
 authenticate_helpers();whole=parents[WHOLE][0];compact=parents[COMPACT][0];metric=parents[METRIC][0];ordinary=parents[ORDINARY][0]
 assert whole['status']=='CONDITIONAL_WHOLE_SLICE_CAUCHY_INVENTORY_PASS' and len(whole['controls'])==92 and all(c['passed'] for c in whole['controls'])
 assert compact['status']=='CONDITIONAL_CANONICAL_CONSTRAINT_SOURCE_ARITHMETIC_PASS' and parents[COMPACT][1]['owner']['pid']==23177
 assert len(compact['controls'])==42 and all(c['passed'] for c in compact['controls'])
 for r in (whole,compact,metric,ordinary):assert [c['sigma'] for c in r['cases']]==list(SIGMAS)
 fixed=whole['checkpoints'][0]['metadata']['fixed'];cp=json.loads(path('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json').read_text())
 assert fixed['eps']==1e-5 and fixed['Q0_over_Hstar']==100 and cp['eps']==1e-5
 assert fixed==metric['checkpoints'][0]['metadata']['owned_fixed'] and whole['checkpoints'][0]['metadata']['owned_EPS5_background']==cp['background']
 for wc,cc in zip(whole['cases'],compact['cases']):
  assert len(wc['columns'])==4
  for iq,ref in enumerate(wc['columns']):
   rec=resolve_record(ref);md=rec['metadata'];assert md['sigma']==wc['sigma'] and md['column']==iq and md['points']==POINTS_PER_COLUMN
   for n,shape in dict(R=[3784],Z=[3784],reference_volume=[3784],native_canonical_density=[3784,99],canonical_density_106=[3784,106],Q1_weak_loads=[106,87,45],phase_Pstar=[3784],phase_Wstar=[3784],phase_P_X=[3784],phase_P_XX=[3784],phase_canonical_density=[3784]).items():assert md['schema'][n]==dict(shape=shape,dtype='float64',finite=True)
   assert md['compact_parent_file']==cc['checkpoint']['file'] and md['compact_parent_sha256']==cc['checkpoint']['sha256']
 return ins,whole,compact,metric,ordinary,fixed,cp

def restrict_rows(rows):
 # Adjoint of regular axis nodal extension: even scalar/Z/phi tie node0=node1;
 # odd radial vector vanishes at R0. Z shift is odd at the reflected sheet.
 out=rows.copy();out[0,1]+=out[0,0];out[2,1]+=out[2,0];out[3,1]+=out[3,0]
 out[[0,2,3],0]=0;out[1,0]=0;out[2,:,0]=0
 out[:,-1]=0;out[:,:,-1]=0
 return out

def extend_tests(values):
 out=values.copy();out[0,0]=out[0,1];out[2,0]=out[2,1];out[3,0]=out[3,1]
 out[1,0]=0;out[2,:,0]=0;out[:,-1]=0;out[:,:,-1]=0
 return out

def column_shapes(rec):
 vals=read_pair(rec,['cell_i','cell_j']+[f'corner{a}_'+k for a in range(4) for k in ('shape','shape_R','shape_Z')])
 ij=((0,0),(1,0),(0,1),(1,1));return [(vals[f'corner{a}_shape'],vals[f'corner{a}_shape_R'],vals[f'corner{a}_shape_Z'],i,j) for a,(i,j) in enumerate(ij)],vals['cell_i'],vals['cell_j']

def scatter_coefficients(coeff,dv,shapes):
 # coeff[p,ADMdirection,component,jet] with jet=(value,dR,dZ).
 loads=np.zeros((4,coeff.shape[2],87,45));env=np.zeros_like(loads)
 for N,NR,NZ,i,j in shapes:
  terms=coeff*np.stack((N,NR,NZ),axis=-1)[:,None,None,:]
  value=dv[:,None,None]*terms.sum(axis=-1);bound=abs(dv)[:,None,None]*abs(terms).sum(axis=-1)
  loads[:,:,i:86+i,j:44+j]+=value.reshape(86,44,4,coeff.shape[2]).transpose(2,3,0,1)
  env[:,:,i:86+i,j:44+j]+=bound.reshape(86,44,4,coeff.shape[2]).transpose(2,3,0,1)
 return loads,env

def scatter_coefficients_independent(coeff,dv,shapes,ci,cj):
 out=np.zeros((4,coeff.shape[2],87,45))
 for N,NR,NZ,i,j in shapes:
  value=(dv[:,None,None]*(coeff[:,:,:,0]*N[:,None,None]+coeff[:,:,:,1]*NR[:,None,None]+coeff[:,:,:,2]*NZ[:,None,None]))
  for d in range(4):
   for k in range(coeff.shape[2]):np.add.at(out[d,k],(ci+i,cj+j),value[:,d,k])
 return out

def source_projection(r,ordinary,metric):
 # Exact old immutable rest-mass/momentum samples. No density reconstruction.
 vals=read_pair(ordinary['checkpoint'],('source_g','p_phi','mass_weight'))
 coords=read_pair(metric['checkpoint'],('source_R','source_Z'));R=coords['source_R'];Z=coords['source_Z'];assert np.all(Z==0)
 indices=np.searchsorted(r,R,side='right')-1;assert np.all((indices>=0)&(indices<86))
 t=(R-r[indices])/(r[indices+1]-r[indices]);assert np.all((t>0)&(t<1))
 p=np.zeros((len(R),3));p[:,2]=vals['p_phi'];o=ordinary_velocity(vals['source_g'],p)
 normal=vals['mass_weight']*o['gamma'];shift=-vals['mass_weight'][:,None]*p
 rows=np.zeros((4,87,45));envelope=np.zeros_like(rows)
 for offset,wgt in ((0,1-t),(1,t)):
  a=np.column_stack((normal,shift))*wgt[:,None]
  for d in range(4):np.add.at(rows[d,:,0],indices+offset,a[:,d]);np.add.at(envelope[d,:,0],indices+offset,abs(a[:,d]))
 return rows,envelope,dict(source_R=R,source_Z=Z,source_g=vals['source_g'],source_mass_weight=vals['mass_weight'],source_specific_covariant_p=p,source_gamma=o['gamma'],source_indices=indices.astype(np.int64),source_right_weight=t,source_Q1_normal=normal,source_Q1_shift=shift)

def conservative_H_faces(r,z,Phi,Hbar):
 # Shared face quadrature is a representation of the exact divergence identity.
 # Its flux cancels by incidence independently of its integration accuracy.
 t=(1+np.array([-1.,1.])/math.sqrt(3))/2
 dz=np.diff(z);dr=np.diff(r)
 phiR=(1-t)[None,None,:]*Phi[:,:-1,None]+t[None,None,:]*Phi[:,1:,None]
 wR=r[:,None,None]*np.exp(-3*phiR)*dz[None,:,None]/2
 rface=r[:-1,None]+dr[:,None]*t[None]
 phiZ=(1-t)[None,:,None]*Phi[:-1,None,:]+t[None,:,None]*Phi[1:,None,:]
 wZ=rface[:,:,None]*np.exp(-3*phiZ)*dr[:,None,None]/2
 nodal=np.zeros((4,87,45));envelope=np.zeros_like(nodal);cell_terms=[]
 factor=-2*Hbar/C
 for i in range(86):
  for j in range(44):
   for face,sign,coords,weight in ((0,-1,((i,j),(i,j+1)),wR[i,j]),(1,1,((i+1,j),(i+1,j+1)),wR[i+1,j])):
    for a,(ni,nj) in enumerate(coords):
     term=factor*sign*weight*(1-t if a==0 else t);value=term.sum();nodal[1,ni,nj]+=value;envelope[1,ni,nj]+=abs(term).sum();cell_terms.append(value)
   for face,sign,coords,weight in ((2,-1,((i,j),(i+1,j)),wZ[i,:,j]),(3,1,((i,j+1),(i+1,j+1)),wZ[i,:,j+1])):
    for a,(ni,nj) in enumerate(coords):
     term=factor*sign*weight*(1-t if a==0 else t);value=term.sum();nodal[2,ni,nj]+=value;envelope[2,ni,nj]+=abs(term).sum();cell_terms.append(value)
 raw=dict(face_GL_fraction=t,face_R_weight=wR,face_Z_weight=wZ,face_cell_outward_contributions=np.array(cell_terms),EH_H_face_loads=nodal,EH_H_face_envelope=envelope)
 return nodal,envelope,raw

def global_geometry(r,z,whole,ordinary,metric,Hbar):
 global RAW,AVAILABLE
 RAW={};AVAILABLE={};start=len(CHECKS)
 sample=np.arange(4*87*45,dtype=float).reshape(4,87,45)/10000
 test=np.cos(np.arange(sample.size,dtype=float)).reshape(sample.shape)
 a=np.array([np.sum(restrict_rows(sample)*test)]);e=np.array([np.sum(sample*extend_tests(test))]);env=np.array([np.sum(abs(sample*extend_tests(test)))+np.sum(abs(restrict_rows(sample)*test))])
 check('Q1_axis_parity_restriction_adjoint',a,e,env)
 first=resolve_record(whole['columns'][0]);shapes,ci,cj=column_shapes(first);allRZ=[];total=np.zeros((4,1,87,45));envelope=np.zeros_like(total)
 for ref in whole['columns']:
  rec=resolve_record(ref);v=read_pair(rec,('R','Z','reference_volume'));sh,ii,jj=column_shapes(rec);coeff=np.zeros((len(v['R']),4,1,3));coeff[:,1,0,1]=1/v['R'];coeff[:,2,0,2]=1/v['R']
  load,le=scatter_coefficients(coeff,v['reference_volume'],sh);total+=load;envelope+=le;allRZ.append(v)
 dualR=np.r_[np.diff(r)[0]/2,(np.diff(r)[:-1]+np.diff(r)[1:])/2,np.diff(r)[-1]/2];dualZ=np.r_[np.diff(z)[0]/2,(np.diff(z)[:-1]+np.diff(z)[1:])/2,np.diff(z)[-1]/2]
 expected=np.zeros_like(total);expected[1,0,0]=-dualZ;expected[1,0,-1]=dualZ;expected[2,0,:,0]=-dualR;expected[2,0,:,-1]=dualR
 check('Q1_constant_coordinate_flux_scatter',total,expected,envelope+abs(expected))
 source,se,sv=source_projection(r,ordinary,metric);R=sv['source_R'];i=sv['source_indices'];t=sv['source_right_weight'];actual=np.r_[1-t+t,(1-t)*r[i]+t*r[i+1]];expected=np.r_[np.ones(len(t)),R]
 check('immutable_annular_Q1_partition_and_location',actual,expected,np.r_[np.ones(len(t))*2,abs((1-t)*r[i])+abs(t*r[i+1])+abs(R)])
 RAW.update({k:v.copy() for k,v in sv.items()});RAW['ordinary_Q1_loads']=source;RAW['ordinary_Q1_envelope']=se
 geo=checkpoint('GEOMETRY',RAW,dict(kind='new_axis_parity_and_derivative_hat_assembly',controls=CHECKS[start:],physical_boundary_scope='algebraic compact interior test restriction; not a physical exterior condition'))
 return source,se,geo

def state_from_whole(rec,omega,xi,w):
 names=('g','hi','Ga','U','du','z','dz','phi','Pi','PiU','native_canonical_density','phase_Pstar','phase_Wstar','phase_P_X','phase_P_XX','phase_canonical_density','R','Z','reference_volume','compact_reused_whole_indices','new_whole_indices')
 vals=read_pair(rec,names);s=features(*(vals[k] for k in ('g','hi','Ga','U','du','z','dz','phi')),omega,xi,w)
 s['Pi']=vals['Pi'];s['PiU']=vals['PiU'];s['R']=vals['R'];s['Phi']=read_pair(rec,('Phi',))['Phi'];return s,vals

def state_subset(s,index):
 modal=('z','dz','nz','q','V','D','f','z2','Pi','mu');static=('omega','xi','w');out={}
 for k,v in s.items():
  if k in static:out[k]=v
  elif k in modal:out[k]=v[:,index]
  else:out[k]=v[index]
 return out

def owned_response(s,v,old,iq,Hbar):
 global ARM_AVAILABLE
 label=f'q{iq}_';ix=v['compact_reused_whole_indices'].astype(np.int64);ox=v['new_whole_indices'].astype(np.int64);c=adm_chart(s)
 fields=('du_increment','dz_increment','connection_increment','owned_hdot_tensor','native_p','metric_native_p','metric_EH_p','old_native_canonical_momentum')
 prior=read_pair(old,[label+k for k in fields])
 AR=AVAILABLE
 for k,a in prior.items():AR['copied_'+k]=a.copy()
 sn=state_subset(s,ox);cn=adm_chart(sn);block=arrowhead_blocks(sn,cn);op=arrowhead_operation_envelopes(sn,cn,label='whole_complement')
 for k in ('A','B','D','A_modes','Maxwell'):block['operation_'+k]=op[k]
 ARM_AVAILABLE=AVAILABLE
 new,nc,cert=reconstruct_owned_K(sn,cn,block,Hbar,'new_')
 check(label+'complement_original_99_action',cert['action'],cert['rhs'],cert['action_envelope'])
 check(label+'complement_fixed_native_p',cert['native_p'],v['native_canonical_density'][ox],cert['momentum_envelope']+abs(v['native_canonical_density'][ox]))
 target=np.r_[np.zeros_like(cert['constraints']),cert['Kexpected'].ravel()]
 check(label+'complement_unit_transverse_and_owned_K',np.r_[cert['constraints'],cert['Kgap'].ravel()],target,np.r_[cert['constraint_envelope'],cert['Kenv'].ravel()])
 du=np.empty_like(s['du']);dz=np.empty_like(s['dz']);dGa=np.empty_like(s['Ga']);du[ix]=prior[label+'du_increment'];du[ox]=AR['new_du_increment'];dz[:,ix]=prior[label+'dz_increment'];dz[:,ox]=AR['new_dz_increment'];dGa[ix]=prior[label+'connection_increment'];dGa[ox]=AR['new_connection_increment']
 # Only unsaved firstjet/features needed by new Q1 tests are reconstructed;
 # the completed selected response, p and Pi/PiU are authoritative copies.
 n=features(s['g'],s['hi'],s['Ga']+dGa,s['U'],s['du']+du,s['z'],s['dz']+dz,s['phi'],s['omega'],s['xi'],s['w']);n['R']=s['R'];n['Phi']=s['Phi'];cc=adm_chart(n)
 selected=read_pair(old,[label+'new_native_Pi',label+'new_native_PiU']);n['Pi'][:,ix]=selected[label+'new_native_Pi'];n['PiU'][ix]=selected[label+'new_native_PiU']
 py=v['native_canonical_density'].copy();pm=np.empty((len(py),6));pm[ix]=prior[label+'metric_native_p'];pm[ox]=AR['new_metric_native_p']
 pmetric=symmetric_tensor_from_coordinates(pm)+cc['pi_EH']
 iso=-cc['sqrt_h'][:,None,None]*Hbar*cc['ih']/C;split=cc['pi_EH']-c['pi_EH']
 AR.update(owned_du_increment=du,owned_dz_increment=dz,owned_connection_increment=dGa,owned_native_canonical_density=py,owned_metric_native_p=pm,owned_metric_total_p=pmetric,old_EH_p=c['pi_EH'],owned_EH_p=cc['pi_EH'],EH_isotropic_increment=iso,EH_isotropic_split_actual=split)
 return n,cc,py,pmetric,split,iso

def unit_test(p,d,j):
 f=np.zeros(p);df=np.zeros((p,4));b=np.zeros((p,3));db=np.zeros((p,4,3))
 if d==0:
  if j==0:f[:]=1
  else:df[:,j]=1
 else:
  if j==0:b[:,d-1]=1
  else:db[:,j,d-1]=1
 return f,df,b,db

def coefficient_fields(n,c,py,pmetric,v,Hbar):
 p=len(n['U']);coeff=np.zeros((p,4,4,3));bounds=np.zeros_like(coeff);generator=np.zeros((p,4,4,3));iso=np.zeros((p,4,1,3));R=v['R']
 for d in range(4):
  for j in range(3):
   f,df,b,db=unit_test(p,d,j);src=native_phase_constraint_direction(n,c,f,df,b,db,v['phase_Pstar'],v['phase_Wstar'],R);eh=EH_ADM_constraint_direction(n,c,f,df,b,db,R)
   coeff[:,d,:3,j]=src['Hamiltonian_components'];coeff[:,d,3,j]=eh['normal']+eh['shift'];bounds[:,d,:3,j]=src['envelope'];bounds[:,d,3,j]=eh['normal_envelope']+eh['shift_envelope']
   generator[:,d,:,j]=spatial_generator_density(n,c,py,pmetric,v['phase_canonical_density'],b,db,R)
   if d:
    jets=adm_first_jets(n,c);Lie=np.einsum('pk,pkij->pij',b,jets['dh'][:,1:])+np.einsum('pik,pjk->pij',c['h'],db[:,1:])+np.einsum('pkj,pik->pij',c['h'],db[:,1:])
    piso=-c['sqrt_h'][:,None,None]*Hbar*c['ih']/C;iso[:,d,0,j]=np.einsum('pij,pij->p',piso,Lie)/R
   AVAILABLE.update(Q1_coefficient_partial=coeff.copy(),Q1_coefficient_envelope_partial=bounds.copy(),Q1_generator_coefficient_partial=generator.copy(),Q1_EH_isotropic_coefficient_partial=iso.copy())
 return coeff,bounds,generator,iso

def column(case,iq,ref,old,xi,w,fixed,cp):
 global RAW,AVAILABLE,ARM_AVAILABLE
 RAW={};AVAILABLE={};ARM_AVAILABLE={};start=len(CHECKS);CONTEXT.update(sigma=case['sigma'],column=iq,stage='Q1_column')
 rec=resolve_record(ref);omega=case['sigma']*xi*fixed['Hunit']/LIGHT;s,v=state_from_whole(rec,omega,xi,w);Hbar=fixed['Hunit']/LIGHT*cp['background']['h']
 n,c,py,pm,split,iso_p=owned_response(s,v,old,iq,Hbar)
 coeff,bounds,generator,iso=coefficient_fields(n,c,py,pm,v,Hbar);shapes,ci,cj=column_shapes(rec);loads,en=scatter_coefficients(coeff,v['reference_volume'],shapes);again=scatter_coefficients_independent(coeff,v['reference_volume'],shapes,ci,cj)
 check(f'q{iq}_independent_Q1_coefficient_scatter',loads,again,en+abs(again))
 gl,ge=scatter_coefficients(generator,v['reference_volume'],shapes);il,ie=scatter_coefficients(iso,v['reference_volume'],shapes)
 AVAILABLE.update(R=v['R'],Z=v['Z'],reference_volume=v['reference_volume'],Q1_coefficients=coeff,Q1_coefficient_envelope=bounds,Q1_canonical_generator_coefficients=generator,Q1_EH_H_coefficients=iso,Q1_component_loads=loads,Q1_component_envelope=en,Q1_canonical_generator_loads=gl,Q1_EH_H_quadrature_loads=il,Q1_EH_H_quadrature_envelope=ie,EH_isotropic_split_actual=split,EH_isotropic_increment=iso_p)
 AVAILABLE.update({k:a.copy() for k,a in RAW.items() if k.startswith('control_')})
 cpout=checkpoint('COLUMN',AVAILABLE,dict(kind='all_real_Q1_hat_normal_and_three_shift_coefficients',sigma=case['sigma'],column=iq,points=3784,controls=CHECKS[start:],whole_parent_file=rec['file'],whole_parent_sha256=rec['sha256'],compact_parent_file=old['file'],compact_parent_sha256=old['sha256'],reused_points=len(v['compact_reused_whole_indices']),new_response_points=len(v['new_whole_indices']),velocity_scope='pointwise/mixed canonical Cauchy jets; no nodal Q1 velocity compatibility claimed',initial_time_scope='same conditional fixed-native-p ownedH increment; no evolved history or independently imposed total metric p',physical_changes=[]))
 return cpout,loads,en,gl,il,ie,split,iso_p

def arm(case,compact,metric,ordinary,even,face,face_envelope,fixed,cp):
 global RAW,AVAILABLE,ARM_AVAILABLE
 RAW={};AVAILABLE={};ARM_AVAILABLE={};start=len(CHECKS);rows=[];total=np.zeros((4,4,87,45));env=np.zeros_like(total);gen=np.zeros_like(total);iqH=np.zeros((4,1,87,45));iqE=np.zeros_like(iqH);splits=[];targets=[]
 for iq,ref in enumerate(case['columns']):
  rec,a,e,g,h,he,split,target=column(case,iq,ref,compact['checkpoint'],even['xi'],even['weights'],fixed,cp);rows.append(rec);total+=a;env+=e;gen+=g;iqH+=h;iqE+=he;splits.append(split.ravel());targets.append(target.ravel())
 check(f's{case["sigma"]}_EH_exact_constant_H_momentum_split',np.concatenate(splits),np.concatenate(targets),abs(np.concatenate(splits))+abs(np.concatenate(targets))+1e-30)
 source,se,sv=source_projection(even['r_kpc'],ordinary,metric)
 conservative=total.copy();conservative[:,3]-=iqH[:,0];conservative[:,3]+=face
 total_with_source=np.concatenate((total,source[:,None]),axis=1);conservative_with_source=np.concatenate((conservative,source[:,None]),axis=1)
 restricted=np.stack([restrict_rows(conservative_with_source[:,k]) for k in range(5)],axis=1);raw_restricted=np.stack([restrict_rows(total_with_source[:,k]) for k in range(5)],axis=1)
 rebuilt=np.zeros_like(total)
 for row in rows:rebuilt+=read_pair(row,('Q1_component_loads',))['Q1_component_loads']
 check(f's{case["sigma"]}_whole_Q1_component_recontraction',total,rebuilt,env+abs(rebuilt))
 RAW.update(Q1_original_quadrature_components=total_with_source,Q1_conservative_components=conservative_with_source,Q1_restricted_components=restricted,Q1_original_restricted_components=raw_restricted,Q1_original_residual=raw_restricted.sum(axis=1),Q1_conservative_residual=restricted.sum(axis=1),Q1_component_envelope=np.concatenate((env,se[:,None]),axis=1),Q1_canonical_generator_components=gen,Q1_EH_H_original_quadrature=iqH[:,0],Q1_EH_H_conservative_face=face,Q1_EH_H_conservative_face_envelope=face_envelope,Q1_EH_H_quadrature_alias=iqH[:,0]-face,ordinary_Q1_loads=source,ordinary_Q1_envelope=se)
 RAW.update({k:a.copy() for k,a in sv.items()});summary=checkpoint('ARM',RAW,dict(kind='whole87x45_true_Q1_interior_canonical_residual_inventory',sigma=case['sigma'],controls=CHECKS[start:],column_files=[r['file'] for r in rows],column_sha256=[r['sha256'] for r in rows],component_names=['native_metric','mode_constraint_compensation','absolute_phase','EH_ADM','ordinary_annuli'],row_names=['lapse','shift_R','shift_Z','shift_phi'],axis_scope='regular even scalar/Z/phi axis adjoint; radial odd axis zero; vertical odd sheet zero',boundary_scope='compact interior hats used diagnostically; no physical wall/junction adopted',EH_scope='only known constant-H momentum divergence replaced by shared-face weak representative; original Q2 row and alias retained',unknowns=dict(CMC_time_prescription=None,full_temporal_improvement=None,exterior_ports=None,local_cosmic_ordinary_state=None,formation_history=None,nodal_velocity_compatibility=None,activity_outside_0p3_15p1=None),residual_smallness_gate=None,physical_changes=[]))
 return dict(sigma=case['sigma'],status='CONDITIONAL_Q1_CANONICAL_RESIDUAL_MEASURES',checkpoint=summary,columns=[dict(file=r['file'],sha256=r['sha256'],commit_file=r['commit_file'],commit_sha256=r['commit_sha256']) for r in rows],qualification=FLAGS)

def main():
 global np,OWNER,INPUTS,RAW,AVAILABLE,ARM_AVAILABLE
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.root_run:raise SystemExit('Guarded whole-Q1 source: actual CLOSED whole bindings and FULL root/distinct review required.')
 assert not list(BASE.glob(STEM+'_*'))
 INPUTS,whole,compact,metric,ordinary,fixed,cp=admission();OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_file=Path(__file__).name,source_sha256=sha(__file__));cases=[]
 try:
  json_file(STEM+'_OWNER_START.json',OWNER);json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,configuration=dict(points_per_arm=15136,columns=4,modes=32,controls=CONTROL_COUNT,pairs=PAIR_COUNT,coefficient_tests=12,grid=[87,45],sigma=SIGMAS,tolerance=TOL),qualification=FLAGS))
  import numpy as _np
  np=_np;even=read_pair(whole['checkpoints'][0],('r_kpc','z_kpc','final_state','xi','weights'));checkpoint('INPUT',even,dict(kind='exact_whole_Cauchy_configuration_and_compact_response_references',fixed=fixed,owned_EPS5_background=cp['background'],copied_whole_controls=whole['controls'],copied_constraint_controls=compact['controls'],qualification=FLAGS))
  Hbar=fixed['Hunit']/LIGHT*cp['background']['h'];source,se,geometry=global_geometry(even['r_kpc'],even['z_kpc'],whole['cases'][0],ordinary['cases'][0],metric['cases'][0],Hbar)
  RAW={};start=len(CHECKS);Phi=B*even['final_state'][0];face,fe,fr=conservative_H_faces(even['r_kpc'],even['z_kpc'],Phi,Hbar);RAW.update(fr)
  check('constant_H_shared_face_interior_telescope',restrict_rows(face),np.zeros_like(face),restrict_rows(fe)+fe+1e-30)
  boundary=np.zeros(4);boundary[1]=(-2*Hbar/C)*fr['face_R_weight'][-1].sum();boundary[2]=(-2*Hbar/C)*(fr['face_Z_weight'][:,:,-1].sum()-fr['face_Z_weight'][:,:,0].sum())
  check('constant_H_shared_face_boundary_flux',face.sum(axis=(1,2)),boundary,fe.sum(axis=(1,2))+abs(boundary));checkpoint('FACES',RAW,dict(kind='conservative_constant_isotropic_EH_momentum_incidence',controls=CHECKS[start:],quadrature_scope='fixed shared2point face rule; cancellation is incidence identity rather than accuracy claim'))
  for a,c,m,o in zip(whole['cases'],compact['cases'],metric['cases'],ordinary['cases']):cases.append(arm(a,c,m,o,even,face,fe,fixed,cp))
  assert len(CHECKS)==CONTROL_COUNT and len(RECORDS)==PAIR_COUNT and all(c['passed'] for c in CHECKS)
  recheck();rh=json_file(STEM+'_RESULT.json',dict(owner=OWNER,status='CONDITIONAL_WHOLE_Q1_ADM_RESIDUAL_ARITHMETIC_PASS',cases=cases,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS))
  publish(STEM+'_REPORT.md',(f'# {STEM}\n\nGenuine Q1 normal/three-shift rows for four same-law stationary-seed canonical slices; no residual-smallness or physical-velocity gate.\n\nOriginal Q2 EH rows and the constant-H conservative face/incidence representation are saved separately. Pointwise velocities remain mixed Cauchy operands, with nodal compatibility, full temporal/exterior ports and local cosmic-ordinary allocation unresolved.\n').encode());recheck();rc=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,qualification=FLAGS);json_file(STEM+'_RECEIPT.json',rc);assert json.loads(path(STEM+'_RECEIPT.json').read_text())==canonical(rc);recheck();print('CONDITIONAL_WHOLE_Q1_ADM_RESIDUAL_ARITHMETIC_PASS',len(CHECKS),len(RECORDS))
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None;available=dict(AVAILABLE);available.update(ARM_AVAILABLE);available.update(RAW)
  if np is not None and available:
   try:checkpoint('ERROR_RAW',available,dict(kind='unaccepted_available_Q1_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:seal_actual();recheck(False)
  except BaseException:close_error=traceback.format_exc()
  prior=sha(path(STEM+'_RECEIPT.json')) if path(STEM+'_RECEIPT.json').exists() else None
  if prior:OUTPUTS[STEM+'_RECEIPT.json']=prior
  eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,cases=cases,checkpoints=RECORDS,input_sha256=INPUTS,preserved_outputs=dict(OUTPUTS),prior_receipt_sha256=prior,unqualified_npz=[p.name for p in BASE.glob(STEM+'_*.npz') if p.name not in {r['file'] for r in RECORDS}],qualification=FLAGS))
  if prior is None:json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),error_sha256=eh,qualification=FLAGS))
  seal_actual();recheck(False);raise

if __name__=='__main__':raise SystemExit(main())
