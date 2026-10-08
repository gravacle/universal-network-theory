"""Unexecuted exact local-cycle quantum-floor/source certificate; root only."""
import argparse, hashlib, io, json, os, time, traceback
from datetime import datetime, timezone
from pathlib import Path

AUTHOR_DRAFT = True
J = Path(__file__).resolve().parent
STEM = 'LOCAL_RECORD_FEEDBACK_TRANSVERSE_FIELD_FLOOR_AND_BIRTH_CONTACTS_V001'
CP = J / 'local_record_feedback_transverse_field_floor_and_birth_contacts_v001_checkpoints'
PARENT = 'LOCAL_RECORD_FEEDBACK_FINITE_GAUSS_KERNEL_SOURCE_CERTIFICATE_V001'
PCP = J / 'local_record_feedback_finite_gauss_kernel_source_certificate_v001_checkpoints'
DONOR = 'LOCAL_RECORD_FEEDBACK_DONOR_DRESSED_Q4_SOURCE_CHECK_V001'
PINS = {
 'LOCAL_RECORD_FEEDBACK_IDEAL_PLATE_TEM_GAUSS_CONSTRUCTOR_V001.md':'1fbfcea0364eafeabe386da930784099aeab85a00e25b460e32e6b217705cec7',
 'LOCAL_RECORD_FEEDBACK_COUPLED_BIRTH_ENERGY_AND_COUNT_CONTINUATION_V001.md':'58a6f228aec766c9087130d7aa55dd20fb6461327e75553e785ca15e94c81994',
 'local_record_feedback_finite_gauss_kernel_source_certificate_v001.py':'f1ec7a35f3a5719762948a3091f9a1ea8dcd9bd054a4f849031285f3d3b0ea2a',
 'LOCAL_RECORD_FEEDBACK_FINITE_GAUSS_KERNEL_SOURCE_CERTIFICATE_V001.md':'930d5eaf15ef88d7b9a4b19feeb0771e4e9af4a2d08e02175e37d66a2d7b690d',
 'LOCAL_RECORD_FEEDBACK_FINITE_GAUSS_KERNEL_SOURCE_CERTIFICATE_V001_RESULT.json':'21437abbdb243272527f52c0b443019cc6336ea48171aa703239a9e45819f3aa',
 'LOCAL_RECORD_FEEDBACK_FINITE_GAUSS_KERNEL_SOURCE_CERTIFICATE_V001_RECEIPT.json':'b3f0fb9cd493ab56dff085f6af9063de54e7fca9673ab051ad6af8001b277ef3',
 'UNIFIED_RECORD_BIRTH_MAXWELL_DEBIT_AND_SOURCE_CONTACTS_V001.md':'9c65b7a1b7e3b1b32de7d8691e4612312a6a401c15ede9005a4966a0e6e72a1f',
 'UNIFIED_REPEATED_COUNT_VOLUME_DEPENDENT_NORMAL_ACTION_V001.md':'4fb8381caae88420093ab43fdb1abaf31451bbe2ff51e77b7d27ff606efd282a',
 'LOCAL_RECORD_FEEDBACK_TRANSVERSE_FIELD_FLOOR_AND_BIRTH_CONTACTS_V001.md':'032fe34054c705e844e4a71aef720dba40fa1cbcf09d10f7465d95aea4a07a6c',
}
TOL = 1e-11
KAPPA = (0., -.001, .001)
MAP_KEYS = ('vertex_block','cycle_embedding','electric_congruence','inductive_congruence','canonical_transfer')
KERNEL_KEYS = ('Ec_sym','Lc_sym','Ec_chol','Lc_chol','Linv_identity','frequency_sym','eigen_row',
 'eigen_orthogonal','frequency_expected','frequency_positive','canonical_modes','kinetic_normal_form',
 'magnetic_normal_form','mechanical_eigenrow','star_floor','old_floor','new_floor','added_cycles','delta_floor','uniform_spectrum')
CONTACT_KEYS = ('Ec_x','Ec_y','Ec_xy','Lc_x','Lc_y','Lc_xy','Linv_x','Linv_y','Linv_xy',
 'frequency_product_x','frequency_product_y','frequency_product_xy','Nc_value','Nc_x','Nc_y','Nc_xy',
 'mode_canonical_x','mode_canonical_y','mode_canonical_xy','Gauss_chart_contacts')
ROW_KEYS = ('eligibility','signed_cost','first_cost_source','mixed_cost_source','uniform_Z')
PHYSICAL = {k:False for k in ('physical_unit_selected','physical_geometry_selected','physical_profile_selected',
 'auxiliary_preparation_selected','full_quantum_transfer_certified','physical_source_Hilbert_certified',
 'dynamic_photon_state_solved','thermal_inflation_cosmic_result','late_phase_galaxy_match')}
RAW, CONTEXT, PARTIAL = {}, {}, []


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def utc(): return datetime.now(timezone.utc).isoformat()
def canon(v): return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def verify(pins):
    for n,h in pins.items(): assert sha(J/n)==h, ('protected_input',n)

def exclusive(p,b):
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    p.chmod(0o444); assert p.read_bytes()==b, 'expected_byte_reread'
    return sha(p)

def closed():
    receipt=json.loads((J/(PARENT+'_RECEIPT.json')).read_text())
    result=json.loads((J/(PARENT+'_RESULT.json')).read_text())
    assert receipt['status']=='CLOSED' and result['status']=='ARITHMETIC_PASS'
    assert result['pins']==receipt['pins'] and result['owner']==receipt['owner']
    assert type(receipt['owner']['pid']) is int and receipt['owner']['pid']>0
    assert result['census']=={'AR_members':3,'kappa_members':3,'charge_rows':864,'checkpoint_pairs':12,'predicates':22539}
    assert result['implementation_fixture']=={'qstar':1,'qR':1,'ed':.5,'em':.5,'gc':.25,'U':1,
      'lambdaR':.5,'self_per_star':1,'cp':1,'branch_lengths':1,'AR':[.125,.175,.25],'kappa':list(KAPPA)}
    assert all(v is False for v in result['qualification'].values())
    maps={**receipt['pins'],**receipt['outputs'],**receipt['checkpoint_outputs']};verify(maps)
    assert len(receipt['checkpoint_outputs'])==25 and len(result['checkpoints'])==12
    assert json.loads((PCP/'OWNER_START.json').read_text())=={'owner':receipt['owner'],'pins':receipt['pins']}
    for cp in result['checkpoints']:
        assert sha(PCP/cp['checkpoint'])==cp['sha256']
        assert json.loads((PCP/cp['commit']).read_text())=={'checkpoint':cp['checkpoint'],
          'sha256':cp['sha256'],'pins':receipt['pins'],'owner':receipt['owner'],'status':'ARITHMETIC_PASS'}
    donor=json.loads((J/(DONOR+'_RECEIPT.json')).read_text())
    assert donor['status']=='CLOSED' and donor['owner']['pid']>0
    for key in ('pins','outputs','checkpoint_outputs'): verify(donor[key])
    assert result['inherited_census']['total_predicates']==93210
    assert all(v is False for v in result['inherited_qualification'].values())
    return result,receipt,maps

def check(flags,name,a,b):
    CONTEXT['control']=name; a,b=np.asarray(a,dtype=float),np.asarray(b,dtype=float)
    RAW['control_'+name+'_actual']=a;RAW['control_'+name+'_expected']=b
    assert np.all(np.isfinite(a)) and np.all(np.isfinite(b)), ('nonfinite_control',name)
    err=float(np.max(abs(a-b),initial=0));scale=float(max(1.,np.max(abs(a),initial=0),np.max(abs(b),initial=0)))
    flags[name]={'pass':err<=TOL*scale,'absolute_error':err,'scale':scale}
    assert flags[name]['pass'],(name,err,scale)

def load_kernel(cp,parent,receipt):
    with np.load(PCP/cp['checkpoint'],allow_pickle=False) as f:
        assert set(f.files)==set(cp['array_shapes'])
        assert json.loads(f['_metadata'].tobytes())=={'name':Path(cp['checkpoint']).stem,
          'records':cp['records'],'pins':parent['pins'],'owner':receipt['owner'],'status':'ARITHMETIC_PASS'}
        arrays={k:f[k].copy() for k in f.files if k!='_metadata'}
    for k,v in arrays.items():
        assert list(v.shape)==cp['array_shapes'][k] and v.dtype.kind in 'fiu' and np.all(np.isfinite(v)),k
    r=6 if cp['records']['AR']==.125 else 10;ne=len(cp['records']['positive_branches'])
    assert arrays['Ec'].shape==arrays['Lc'].shape==(r,r) and arrays['R'].shape==(ne,r)
    assert arrays['D_old'].shape==(271,54*ne) and arrays['D_new'].shape==(281,56*ne)
    assert len(cp['records']['old_ports'])==54 and len(cp['records']['new_ports'])==56
    return arrays

def maps(local):
    R,E,L=local['R'],local['Ec'],local['Lc'];ne=R.shape[0];r=R.shape[1]
    records=[];transfers=[];errors=[];inductive_errors=[]
    for v in range(54):
        CONTEXT.update(stage='retained_cycle_map',vertex=v);idx=local['retained_edge_map'][v*ne:(v+1)*ne]
        sign=local['retained_edge_sign'][v*ne:(v+1)*ne];F=np.zeros((ne,ne))
        RAW['retained_map_'+str(v)]=F
        flags={};check(flags,'vertex_block',((idx>=v*ne)&(idx<(v+1)*ne)).astype(float),np.ones(ne))
        F[idx-v*ne,np.arange(ne)]=sign
        # Saved R has identity at its chord rows; coordinates need no arbitrary fit.
        # Actual chord list is supplied independently by the sealed kernel metadata.
        chords=local['chords'];S=(F@R)[chords];RAW['cycle_transfer_'+str(v)]=S
        check(flags,'cycle_embedding',R@S,F@R)
        check(flags,'electric_congruence',S.T@E@S,E)
        check(flags,'inductive_congruence',S.T@L@S,L)
        A=np.linalg.solve(S.T,np.eye(r));RAW['cycle_coordinate_'+str(v)]=A
        check(flags,'canonical_transfer',S.T@A,np.eye(r))
        assert set(flags)==set(MAP_KEYS)
        transfers.append(S);errors.append(S.T@E@S-E);inductive_errors.append(S.T@L@S-L);records.append({'vertex':v,'controls':flags})
    return records,{'retained_cycle_maps':np.asarray(transfers),'retained_Ec_errors':np.asarray(errors),
      'retained_Lc_errors':np.asarray(inductive_errors)}

def kernel(local,Z,prefix):
    E,L=local['Ec']/Z,local['Lc']/Z;r=E.shape[0];I=np.eye(r);arrays={'Ec':E,'Lc':L}
    RAW.update({prefix+k:v for k,v in arrays.items()});flags={}
    LE=np.linalg.cholesky(E);RAW[prefix+'chol_Ec']=LE
    LL=np.linalg.cholesky(L);RAW[prefix+'chol_Lc']=LL
    Li=np.linalg.solve(L,I);RAW[prefix+'Linv']=Li;S=LE.T@Li@LE;RAW[prefix+'frequency_matrix']=S
    lam,U=np.linalg.eigh(S);RAW[prefix+'omega_squared']=lam;RAW[prefix+'frequency_vectors']=U
    check(flags,'frequency_positive',(lam>0).astype(float),np.ones(r))
    om=np.sqrt(lam);qa=LE@U;pp=np.linalg.solve(LE.T,U)
    arrays.update(chol_Ec=LE,chol_Lc=LL,Linv=Li,frequency_matrix=S,omega_squared=lam,omega=om,
      frequency_vectors=U,eigen_residual=S@U-U*lam,eigen_orthogonal_residual=U.T@U-I,
      a_normal_map=qa,p_normal_map=pp,old_tiled_omega=np.tile(om,54),new_tiled_omega=np.tile(om,56))
    RAW.update({prefix+k:v for k,v in arrays.items()})
    check(flags,'Ec_sym',E,E.T);check(flags,'Lc_sym',L,L.T)
    check(flags,'Ec_chol',LE@LE.T,E);check(flags,'Lc_chol',LL@LL.T,L)
    check(flags,'Linv_identity',L@Li,I);check(flags,'frequency_sym',S,S.T)
    check(flags,'eigen_row',S@U,U*lam);check(flags,'eigen_orthogonal',U.T@U,I)
    check(flags,'frequency_expected',lam,np.ones(r));check(flags,'canonical_modes',pp.T@qa,I)
    check(flags,'kinetic_normal_form',pp.T@E@pp,I)
    check(flags,'magnetic_normal_form',qa.T@Li@qa,np.diag(lam))
    check(flags,'mechanical_eigenrow',E@Li@qa,qa*lam)
    floor=float(om.sum()/2);old=float(np.tile(om,54).sum()/2);new=float(np.tile(om,56).sum()/2)
    check(flags,'star_floor',floor,r/2);check(flags,'old_floor',old,54*r/2)
    check(flags,'new_floor',new,56*r/2);check(flags,'added_cycles',len(arrays['new_tiled_omega'])-len(arrays['old_tiled_omega']),2*r)
    check(flags,'delta_floor',new-old,r);check(flags,'uniform_spectrum',om,np.ones(r))
    assert set(flags)==set(KERNEL_KEYS)
    rec={'Z':Z,'cycles_per_star':r,'old_cycles':54*r,'new_cycles':56*r,'added_cycles':2*r,
      'star_vacuum_floor':floor,'old_vacuum_floor':old,'new_vacuum_floor':new,'delta_vacuum_floor':new-old,
      'units':'hbar*cp/ell; arithmetic hbar=cp=ell=1 only','controls':flags,
      'whole_Ec_Lc_representation':{'type':'exact_direct_sum','old_blocks':54,'new_blocks':56,'complete_block_prefix':prefix}}
    return arrays,rec

def contacts(local,a,Z,x,y,prefix):
    E,L,Li=a['Ec'],a['Lc'],a['Linv'];R,c=local['R'],local['c'];I=np.eye(len(E));flags={}
    Ex,Ey,Exy=-x*local['Ec']/Z**2,-y*local['Ec']/Z**2,2*x*y*local['Ec']/Z**3
    Lx,Ly,Lxy=-x*local['Lc']/Z**2,-y*local['Lc']/Z**2,2*x*y*local['Lc']/Z**3
    Lix,Liy=-Li@Lx@Li,-Li@Ly@Li
    Lixy=Li@Ly@Li@Lx@Li+Li@Lx@Li@Ly@Li-Li@Lxy@Li
    Fi=np.linalg.solve(E,I);Fix,Fiy=-Fi@Ex@Fi,-Fi@Ey@Fi
    Fixy=Fi@Ey@Fi@Ex@Fi+Fi@Ex@Fi@Ey@Fi-Fi@Exy@Fi
    B=R/(Z*c[:,None]);Bx,By,Bxy=-x*R/(Z**2*c[:,None]),-y*R/(Z**2*c[:,None]),2*x*y*R/(Z**3*c[:,None])
    Nc=B@Fi;Nx=Bx@Fi+B@Fix;Ny=By@Fi+B@Fiy;Nxy=Bxy@Fi+Bx@Fiy+By@Fix+B@Fixy
    Fx=Ex@Li+E@Lix;Fy=Ey@Li+E@Liy;Fxy=Exy@Li+Ex@Liy+Ey@Lix+E@Lixy
    qa,pp=a['a_normal_map'],a['p_normal_map'];qx,qy=-x*qa/(2*Z),-y*qa/(2*Z)
    px,py=x*pp/(2*Z),y*pp/(2*Z);qxy=3*x*y*qa/(4*Z**2);pxy=-x*y*pp/(4*Z**2)
    out=dict(Ec_x=Ex,Ec_y=Ey,Ec_xy=Exy,Lc_x=Lx,Lc_y=Ly,Lc_xy=Lxy,Linv_x=Lix,Linv_y=Liy,Linv_xy=Lixy,
      frequency_product_x=Fx,frequency_product_y=Fy,frequency_product_xy=Fxy,Nc=Nc,Nc_x=Nx,Nc_y=Ny,Nc_xy=Nxy,
      a_map_x=qx,a_map_y=qy,a_map_xy=qxy,p_map_x=px,p_map_y=py,p_map_xy=pxy)
    RAW.update({prefix+k:v for k,v in out.items()})
    for key,value,target in [('Ec_x',Ex,-x*E/Z),('Ec_y',Ey,-y*E/Z),('Ec_xy',Exy,2*x*y*E/Z**2),
      ('Lc_x',Lx,-x*L/Z),('Lc_y',Ly,-y*L/Z),('Lc_xy',Lxy,2*x*y*L/Z**2),
      ('Linv_x',Lix,x*Li/Z),('Linv_y',Liy,y*Li/Z),('Linv_xy',Lixy,np.zeros_like(Li)),
      ('frequency_product_x',Fx,np.zeros_like(E)),('frequency_product_y',Fy,np.zeros_like(E)),('frequency_product_xy',Fxy,np.zeros_like(E)),
      ('Nc_value',Nc,local['Nc']),('Nc_x',Nx,np.zeros_like(Nc)),('Nc_y',Ny,np.zeros_like(Nc)),('Nc_xy',Nxy,np.zeros_like(Nc))]:check(flags,key,value,target)
    check(flags,'mode_canonical_x',px.T@qa+pp.T@qx,np.zeros_like(E))
    check(flags,'mode_canonical_y',py.T@qa+pp.T@qy,np.zeros_like(E))
    check(flags,'mode_canonical_xy',pxy.T@qa+px.T@qy+py.T@qx+pp.T@qxy,np.zeros_like(E))
    check(flags,'Gauss_chart_contacts',np.stack([local['D']@(c[:,None]*v) for v in (Nx,Ny,Nxy)]),np.zeros((3,6,len(E))))
    assert set(flags)==set(CONTACT_KEYS)
    return out,{'source_x':x,'source_y':y,'static_vacuum_floor_first_x':0,'static_vacuum_floor_first_y':0,
      'static_vacuum_floor_mixed':0,'source_expectation':None,
      'reason':'frequency operator source identities prove floor invariance; no state expectation calculated',
      'oscillator_chart_contact':'p_normal^T d(a_normal) gives -dlnZ*pi^Tq/2; retain symmetric quantum ordering',
      'frame_policy':'hold this central eigenframe for source contacts; additional moving-frame rotations require their connection','controls':flags}

def row_ledger(row,krec,parent_ref,index):
    flags={};CONTEXT.update(stage='row_ledger',parent_group=parent_ref,parent_row=index)
    yes=row['T_state'] is not None;Z=row['Z'];x,y=row['source_x'],row['source_y']
    check(flags,'eligibility',[yes,row['blank_T_reason']=='ineligible_donor'],[bool(row['state'][2]),not bool(row['state'][2])])
    if yes:
        cost=-row['released_storage'];cx=-row['source_release_x'];cxy=-row['source_release_xy']
        check(flags,'signed_cost',cost,row['energy_after']-row['energy_before'])
        check(flags,'first_cost_source',cx,-x*cost/Z);check(flags,'mixed_cost_source',cxy,2*x*y*cost/Z**2)
    else:
        assert all(row[k] is None for k in ('energy_after','released_storage','source_release_x','source_release_xy'))
        cost=cx=cxy=None
        for key in ('signed_cost','first_cost_source','mixed_cost_source'):check(flags,key,0.,0.)
    check(flags,'uniform_Z',Z,1+row['kappa']*row['O']);assert set(flags)==set(ROW_KEYS)
    return {'parent_checkpoint':parent_ref,'parent_row':index,'inherited_row_exact':row,'eligible':yes,
      'cost_native_units':cost,'cost_first_source':cx,'cost_mixed_source':cxy,
      'delta_vacuum_quantum_units':None if not yes else krec['delta_vacuum_floor'],
      'old_vacuum_floor_quantum_units':krec['old_vacuum_floor'],'new_vacuum_floor_quantum_units':krec['new_vacuum_floor'],
      'old_transverse_excitation':None,'native_support_interaction_debit':None,'theta_hbar_cp_over_ell_Eunit':None,
      'necessary_ledger':'deltaE_diag >= <Dlong>+deltaEvac-Eexc_old+deltaE_native_noncap+deltaE_support/reference; full port/reaction work separate',
      'controls':flags}

def checkpoint(name,records,arrays,pins,owner):
    assert all(isinstance(v,np.ndarray) and v.dtype.kind in 'fiu' and np.all(np.isfinite(v)) for v in arrays.values())
    meta={'name':name,'records':records,'pins':pins,'owner':owner,'status':'ARITHMETIC_PASS'}
    text=canon(meta);meta=json.loads(text);arrays=dict(arrays);arrays['_metadata']=np.frombuffer(text,dtype=np.uint8)
    b=io.BytesIO();np.savez_compressed(b,**arrays);path=CP/(name+'.npz');h=exclusive(path,b.getvalue())
    cm={'checkpoint':path.name,'sha256':h,'pins':pins,'owner':owner,'status':'ARITHMETIC_PASS'}
    exclusive(path.with_name(path.name+'.COMMIT.json'),canon(cm))
    with np.load(path,allow_pickle=False) as z:
        assert set(z.files)==set(arrays) and all(np.array_equal(z[k],v) for k,v in arrays.items())
        assert json.loads(z['_metadata'].tobytes())==meta
    assert json.loads(path.with_name(path.name+'.COMMIT.json').read_text())==cm
    return {'checkpoint':path.name,'sha256':h,'commit':path.name+'.COMMIT.json','records':meta['records'],
      'array_shapes':{k:list(v.shape) for k,v in arrays.items()}}

def reread(cp,pins,owner):
    p=CP/cp['checkpoint'];assert sha(p)==cp['sha256']
    with np.load(p,allow_pickle=False) as z:
        assert set(z.files)==set(cp['array_shapes'])
        for n in z.files:assert list(z[n].shape)==cp['array_shapes'][n] and np.all(np.isfinite(z[n]))
        assert json.loads(z['_metadata'].tobytes())=={'name':p.stem,'records':cp['records'],'pins':pins,'owner':owner,'status':'ARITHMETIC_PASS'}
    assert json.loads((CP/cp['commit']).read_text())=={'checkpoint':p.name,'sha256':sha(p),'pins':pins,'owner':owner,'status':'ARITHMETIC_PASS'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');ap.add_argument('--execute',action='store_true');args=ap.parse_args()
    assert args.root_owned and args.execute and not AUTHOR_DRAFT,'root_only_guard'
    verify(PINS);parent,receipt,inherited=closed();pins=dict(PINS)
    for n,h in inherited.items():assert n not in pins or pins[n]==h;pins[n]=h
    pins[Path(__file__).name]=sha(__file__);verify(pins)
    paths=[J/(STEM+v) for v in ('_RESULT.json','_REPORT.md','_RECEIPT.json','_ERROR.json')]
    assert not CP.exists() and not any(J.glob(STEM+'_*')),'unused_runtime_namespace'
    global np
    import numpy as np
    owner={'pid':os.getpid(),'started_utc':utc(),'source_sha256':sha(__file__)};start=time.monotonic()
    CP.mkdir();owner_data={'owner':owner,'pins':pins};owner_sha=exclusive(CP/'OWNER_START.json',canon(owner_data));made=[]
    try:
        for ia in range(3):
            CONTEXT.clear();CONTEXT.update(AR_index=ia);RAW.clear();PARTIAL.clear()
            cp=next(c for c in parent['checkpoints'] if c['checkpoint']=='KERNEL_AR'+str(ia)+'.npz')
            local=load_kernel(cp,parent,receipt);local['chords']=np.asarray(cp['records']['chords'],dtype=np.int64)
            RAW.update({'parent_'+k:v for k,v in local.items()});mr,ma=maps(local);arrays={**RAW,**ma};kernel_records=[];ledgers=[]
            for ik,kappa in enumerate(KAPPA):
                keys={}
                for O in (0,1):
                    CONTEXT.update(stage='frequency',kappa=kappa,O=O);Z=1+kappa*O;assert Z>0
                    prefix=f'k{ik}_O{O}_';a,rec=kernel(local,Z,prefix);arrays.update({prefix+k:v for k,v in a.items()})
                    source_records=[]
                    for y in (0,1):
                        CONTEXT.update(stage='source_contacts',source_y=y)
                        sa,srec=contacts(local,a,Z,O,y,prefix+'y'+str(y)+'_');arrays.update({prefix+'y'+str(y)+'_'+k:v for k,v in sa.items()});source_records.append(srec)
                    rec.update(kappa=kappa,O=O,source_contacts=source_records);kernel_records.append(rec);keys[O]=rec;PARTIAL.append(rec)
                group=next(c for c in parent['checkpoints'] if c['checkpoint']==f'CHARGE_AR{ia}_K{ik}.npz')
                assert len(group['records'])==96
                for ir,row in enumerate(group['records']):
                    ledger=row_ledger(row,keys[int(row['O'])],group['checkpoint'],ir);ledgers.append(ledger);PARTIAL.append(ledger)
            assert len(mr)==54 and len(kernel_records)==6 and len(ledgers)==288
            # Every saved raw actual/expected check tensor is retained with scientific results.
            arrays.update(RAW)
            records={'AR_index':ia,'AR':cp['records']['AR'],'parent_kernel_exact':cp['records'],
              'retained_maps':mr,'kernels':kernel_records,'birth_ledgers':ledgers,'qualification':PHYSICAL}
            made.append(checkpoint('FLOOR_AR'+str(ia),records,arrays,pins,owner))
        predicates=sum(len(m['controls']) for cp in made for m in cp['records']['retained_maps'])
        predicates+=sum(len(k['controls'])+sum(len(s['controls']) for s in k['source_contacts']) for cp in made for k in cp['records']['kernels'])
        predicates+=sum(len(r['controls']) for cp in made for r in cp['records']['birth_ledgers'])
        assert len(made)==3 and predicates==6210
        assert json.loads((CP/'OWNER_START.json').read_text())==owner_data and sha(CP/'OWNER_START.json')==owner_sha
        for c in made:reread(c,pins,owner)
        cpmap={p.relative_to(J).as_posix():sha(p) for p in sorted(CP.iterdir())};assert len(cpmap)==7
        verify(pins);closed()
        result={'status':'ARITHMETIC_PASS','pins':pins,'owner':owner,'checkpoints':made,
          'census':{'AR_members':3,'kernel_arms':18,'source_classes':36,'retained_stars':162,'birth_rows':864,'pairs':3,'predicates':6210},
          'parent_census_exact':parent['census'],'parent_qualification_exact':parent['qualification'],
          'native_census_exact':parent['inherited_census'],'native_qualification_exact':parent['inherited_qualification'],
          'qualification':PHYSICAL,'physical_scale_names':['hbar','cp','ell','capacitance_scale','Eunit'],
          'arithmetic_frequency_fixture':{'hbar':1,'cp':1,'ell':1},'theta_physical':None,
          'scope':'absolute static full-cycle lower edge/source identities; no selected vacuum, source expectation or trajectory'}
        report=('# Exact transverse field floor and birth contacts V001\n\n6210 arithmetic controls; all three inherited passive kernels, '
          'full old/new cycle counts, all864 donor rows and every blank refusal retained. Physical energy scales and old excitation remain '
          'named inputs; static floor/source invariance is not a prepared-state or dynamic photon result.\n').encode()
        rh=exclusive(paths[0],canon(result));th=exclusive(paths[1],report)
        assert json.loads(paths[0].read_text())==result
        receipt_new={'status':'CLOSED','owner':owner,'finished_utc':utc(),'elapsed_seconds':time.monotonic()-start,
          'pins':pins,'outputs':{paths[0].name:rh,paths[1].name:th},'checkpoint_outputs':cpmap,'qualification':PHYSICAL}
        exclusive(paths[2],canon(receipt_new));assert json.loads(paths[2].read_text())==receipt_new
        verify(pins);verify(receipt_new['outputs']);closed()
        for c in made:reread(c,pins,owner)
        assert cpmap=={p.relative_to(J).as_posix():sha(p) for p in sorted(CP.iterdir())}
        assert sha(CP/'OWNER_START.json')==owner_sha
        print(json.dumps({'status':'ARITHMETIC_PASS','predicates':predicates,'result_sha256':rh,'receipt_sha256':sha(paths[2])}))
    except Exception:
        path=CP/'FAILED_RAW.npz';b=io.BytesIO();np.savez_compressed(b,**{k:np.asarray(v) for k,v in RAW.items()})
        fh=exclusive(path,b.getvalue());exclusive(path.with_name(path.name+'.COMMIT.json'),canon({'checkpoint':path.name,'sha256':fh,
          'pins':pins,'owner':owner,'status':'FAILED_RAW_UNACCEPTED'}))
        with np.load(path,allow_pickle=False) as z:
            assert set(z.files)==set(RAW) and all(np.array_equal(z[k],v,equal_nan=True) for k,v in RAW.items())
        cpmap={p.relative_to(J).as_posix():sha(p) for p in CP.iterdir()}
        failure={'status':'ERROR','owner':owner,'failed_utc':utc(),'pins':pins,'context':CONTEXT,
          'raw_failure':path.relative_to(J).as_posix(),'completed_current_records':PARTIAL,'completed_groups':made,
          'traceback':traceback.format_exc(),'checkpoint_outputs':cpmap,'qualification':PHYSICAL}
        failure['protected_terminal_files']={p.name:sha(p) for p in paths[:3] if p.exists()}
        eh=exclusive(paths[3],canon(failure))
        if not paths[2].exists():
            exclusive(paths[2],canon({'status':'ERROR','owner':owner,'closed_utc':utc(),
              'pins':pins,'outputs':{paths[3].name:eh},'checkpoint_outputs':cpmap,'qualification':PHYSICAL}))
        verify(pins);closed();verify(cpmap);raise

if __name__=='__main__': main()
