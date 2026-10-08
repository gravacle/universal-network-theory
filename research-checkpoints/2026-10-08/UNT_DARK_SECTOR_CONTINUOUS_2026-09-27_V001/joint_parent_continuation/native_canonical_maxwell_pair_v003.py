"""Prospective exact canonical native/Maxwell fixture. Root execution only."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,time
BASE=Path(__file__).resolve().parent
STEM='NATIVE_CANONICAL_MAXWELL_PAIR_V003'
PROTOCOL_SHA='f57e996ffa158b434f82dacb02b8863f9655a2677f9b38a605f91d941d0ce048'
PINS={
 'native_canonical_maxwell_pair_v002.py':'cb134002c02cecaea26e59a8abd3f8af423c70f58fc41aaae1e916d7876e355b',
 'NATIVE_CANONICAL_MAXWELL_PAIR_V002.md':'f6ba23540f314fa781a9a731dcc842f2f1cbcfd8b3a48c7859cdc1a861dd2c45',
 'native_canonical_maxwell_pair_v001.py':'fea75ea26891c8b7b23f664fe5268d45dd9f3bfd312bfaf57b28968ad7b61335',
 'NATIVE_CANONICAL_MAXWELL_PAIR_V001.md':'d1425f03cc1f4fc1ca5c606c7d5695f8b8030933408b015824e34adacad85a8e',
 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_RESULT.json':'90ab446321a185f0ffae97d6ac6a7d9bbfc50fbc9540460ec491ce1f7c586feb',
 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_RECEIPT.json':'81611398329f56feb0d1b14fc8eb7cae3b7514791c27ccc617f65c370dc72d2f',
 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_MANIFEST.json':'eed0247905d543b6cc658824a0711f74b1a2fab011a680b6b9648ffc4cfba98f',
 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_JOURNAL.jsonl':'e80c8cee5df3edd137256b6174641859c22223eaf68e6f8103c877118050464a',
 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_CP0000.json':'16bc8403151a00565d61c63fda4bbefa45c98cf8bbf89e66ebef1f27173405d1',
 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_CP0000_COMMIT.json':'539059898279512e031d2328a007239de28d4993cf4b3a8c9291792c934f157f',
 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_CP0072.json':'b93a26c777a8ab8321db518f4e75ea4337853b2274f46f138ec3df6f25d36c35',
 'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_CP0072_COMMIT.json':'505f316ef7bde685ead62b90371fab5a503fb95e4f61407ccd7e439beab5898c',
 'NATIVE_THERMAL_PACKET_V001_RESULTS.json':'8531cd6f2cf7d60e4b981428c9f80b55ee76b23f17bd4ab91c0e435894010538',
 'NATIVE_THERMAL_PACKET_V001_FROZEN.json':'4a6ed3c387bc87961264806ef630f988199bfdde0b3f9d81fb53b11a2c40f0b3',
 'NATIVE_INCIDENCE_MAXWELL_PAIR_SOURCE_V002.md':'7e5cf9d3651de4471b52c9a3769f23cdd5457726c8354ff42ecee3c2a4034c7b',
 'NATIVE_ENERGY_RELEASE_THERMAL_ORIGIN_AND_EXPANSION_BRIDGE_V003.md':'2547e8533877d3f630fd2e283f6d63bebc920d4c1bb768f067a556b649bb5742'}
CONFIG=dict(record_occupations=[0,1],incidences=[0,3],omegas=[.5,1.,2.],kappas=[0.,-.001,.001],cutoffs=[8,12,16],steps=[128,256],durations=[.25,1.,2.],native_preparations=['cycle','tree'],ages=[0.,.5,2.],norm_tolerance=2e-11,operator_tolerance=2e-10,energy_tolerance=2e-8,state_tolerance=2e-8,cutoff_probability_tolerance=2e-8)
SCOPE='NEW homogeneous positive canonical Maxwell coupling; finite vacuum irrep, no thermalization, ordinary-rate, photon-origin, cosmology or continuum-cutoff qualification'
SEALS={};CREATED={};SOURCE_SHA=None;MANIFEST_SHA=None;EPOCH=None;ENTERED=False

def require(ok,msg):
    if not ok:raise AssertionError(msg)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def seal(p,h):
    p=Path(p).resolve();require(p.is_relative_to(BASE.parent.parent),'Owned input path')
    require(sha(p)==h,'Input seal '+str(p));require(str(p) not in SEALS or SEALS[str(p)]==h,'Conflicting seal');SEALS[str(p)]=h
def now():return datetime.now(timezone.utc).isoformat()
def write(name,obj):
    data=canonical(obj);p=BASE/name
    with p.open('xb') as f:f.write(data)
    p.chmod(0o444);CREATED[str(p)]=sha(p);return sha(p)
def event(kind,**kw):
    row=dict(time=now(),event=kind,owner='root',pid=os.getpid(),epoch=EPOCH,source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,**kw)
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(json.dumps(row,sort_keys=True,allow_nan=False)+'\n')
def recheck():
    require(sha(__file__)==SOURCE_SHA,'Source changed')
    for p,h in SEALS.items():require(sha(p)==h,'Input changed '+p)
    for p,h in CREATED.items():require(sha(p)==h,'Created artifact changed '+p)
def finite_tree(x):
    if x is None or type(x) in (bool,int,str):return
    if type(x) is float:require(math.isfinite(x),'Finite serialized number');return
    if isinstance(x,list):
        for v in x:finite_tree(v)
        return
    if isinstance(x,dict):
        require(all(type(k) is str for k in x),'String keys')
        for v in x.values():finite_tree(v)
        return
    raise AssertionError('Unexpected serialized type')

def authenticate():
    for n,h in PINS.items():seal(BASE/n,h)
    seal(BASE/(STEM+'.md'),PROTOCOL_SHA)
    r=read(BASE/'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_RECEIPT.json')
    parent=read(BASE/'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_RESULT.json')
    require(r['status']==parent['status']=='SELECTIVE_PORT_ARITHMETIC_PASS','Accepted native parent')
    require(r['result_sha256']==PINS['NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_RESULT.json'] and r['checkpoint_count']==144,'Parent result/census')
    require(r['manifest_sha256']==PINS['NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_MANIFEST.json'] and r['journal_sha256']==PINS['NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_JOURNAL.jsonl'],'Parent custody map')
    require(read(BASE/'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_MANIFEST.json')==r['manifest']==parent['manifest'],'Identical parent manifests')
    seal(BASE/'native_energy_selective_calorimeter_ports_v001.py',r['source_sha256'])
    for p,h in r['manifest']['input_sha256'].items():seal(p,h)
    for p,h in r['output_sha256'].items():seal(p,h)
    j=[json.loads(x) for x in (BASE/'NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_JOURNAL.jsonl').read_text().splitlines()]
    require(len(j)==146 and j[0]['event']=='OWNER_START' and j[-1]['event']=='OWNER_COMPLETE' and j[-1]['checkpoint_count']==144,'Parent complete lifecycle')
    require(j[-1]['result_sha256']==r['result_sha256'] and j[-1]['status']==r['status'],'Parent terminal result/status')
    for i,e in enumerate(j):
        require(e['owner']=='root' and e['pid']==j[0]['pid'] and e['epoch']==0 and e['source_sha256']==r['source_sha256'] and e['manifest_sha256']==r['manifest_sha256'],'Parent owner/source')
        if 0<i<145:
            require(e['event']=='CHECKPOINT' and e['index']==i-1,'Parent ordered checkpoint')
            c=read(BASE/e['commit']);seal(BASE/e['commit'],e['commit_sha256']);seal(BASE/e['payload'],e['payload_sha256'])
            require(c=={k:e[k] for k in ('epoch','index','manifest_sha256','owner','payload','payload_sha256','pid','source_sha256','stage')},'Parent commit exact identity')
    packet=read(BASE/'NATIVE_THERMAL_PACKET_V001_RESULTS.json');frozen=read(BASE/'NATIVE_THERMAL_PACKET_V001_FROZEN.json')
    require(packet['status']=='COMPLETE' and packet['freeze_sha256']==PINS['NATIVE_THERMAL_PACKET_V001_FROZEN.json'],'Complete prepared-state packet')
    require(hashlib.sha256(json.dumps(packet['payload'],sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()==packet['payload_sha256'],'Thermal payload canonical seal')
    require(packet['payload']['parameters']==r['manifest']['parameters']==frozen['parameters'] and packet['payload']['record_parameters']==r['manifest']['record_parameters']==frozen['record_parameters'],'Same absolute native law')
    return r,packet

def complex_array(np,x,shape):
    require(set(x)=={'real','imag'},'Complex array schema')
    a=np.asarray(x['real'],dtype=float)+1j*np.asarray(x['imag'],dtype=float)
    require(a.shape==shape and bool(np.isfinite(a).all()),'Complex shape/finite');return a
def expectation(np,state,op,axis):
    if axis==0:acted=(op@state.reshape(64,-1)).reshape(state.shape)
    else:acted=np.einsum('ab,ibk->iak',op,state,optimize=True)
    value=np.einsum('ipk,ipk->k',state.conj(),acted)
    return value
def native_data(np,q,packet,check):
    cp=read(BASE/('NATIVE_ENERGY_SELECTIVE_CALORIMETER_PORTS_V001_CP'+('0000' if q==0 else '0072')+'.json'))
    w=cp['witness'];require(w['q']==q and cp['stage']=='SPECTRAL_'+str(q),'Exact native witness')
    H=complex_array(np,w['native_H'],(64,64));V=complex_array(np,w['eigenvectors'],(64,64));E=np.asarray(w['eigenvalues'],dtype=float)
    require(E.shape==(64,) and bool(np.isfinite(E).all()) and bool(np.all(E[1:]>=E[:-1])),'Saved spectral order')
    scale=max(1.,float(np.max(np.sum(abs(H),axis=1))))
    check('native_H_hermitian',float(np.max(abs(H-H.conj().T)))/scale,CONFIG['operator_tolerance'],q=q)
    check('native_saved_orthogonality',float(np.max(abs(V.conj().T@V-np.eye(64)))),CONFIG['operator_tolerance'],q=q)
    check('native_saved_residual',float(np.max(abs(H@V-V*E)))/scale,CONFIG['operator_tolerance'],q=q)
    sectors=[s for s in packet['payload']['sectors'] if s['record_occupation']==q];require(len(sectors)==1,'Unique q sector')
    cols=[];labels=[]
    for prep in CONFIG['native_preparations']:
        for age in CONFIG['ages']:
            matches=[h for h in sectors[0]['holds'] if h['preparation']==prep and h['age']==age];require(len(matches)==1,'Unique owned preparation')
            cols.append(complex_array(np,matches[0]['state_vector'],(64,)));labels.append(dict(preparation=prep,age=age))
    ground=w['groups'][0];require(ground['qualified'] and ground['indices']==[0],'Complete supplied rank-one ground eigenspace')
    cols.append(V[:,0].copy());labels.append(dict(preparation='complete_native_ground',age=None))
    states=np.column_stack(cols)
    for k,label in enumerate(labels):check('native_incoming_norm',abs(float(np.vdot(states[:,k],states[:,k]).real)-1),CONFIG['norm_tolerance'],q=q,**label)
    return H,V,E,states,labels,w

def field_data(np,omega,M,kappa,check):
    require(kappa>-1,'Positive operator Z')
    K0=np.diag(np.arange(1,M+2,dtype=float));off=np.sqrt(np.arange(1,M+1)*np.arange(2,M+2))/2
    X=np.diag(off,1)+np.diag(off,-1)
    HD=omega*(K0-X);HB=omega*(K0+X);H0=2*omega*K0;H1=HD/(1+kappa)+(1+kappa)*HB
    W=H1-H0;dH=HB-HD/(1+kappa)**2;ddH=2*HD/(1+kappa)**3
    for name,op in (('HD',HD),('HB',HB),('H1',H1)):
        check('field_positive_'+name,max(0.,-float(np.linalg.eigvalsh(op)[0]))/max(1.,float(np.max(abs(op)))),CONFIG['operator_tolerance'],omega=omega,M=M,kappa=kappa)
    check('projector_inverse_W',float(np.max(abs(W-omega*(kappa*kappa*K0/(1+kappa)+kappa*(2+kappa)*X/(1+kappa))))),CONFIG['operator_tolerance'],omega=omega,M=M,kappa=kappa)
    e,u=np.linalg.eigh(H1)
    return dict(H0=H0,H1=H1,W=W,dH=dH,ddH=ddH,e=e,u=u,N=np.diag(2*np.arange(M+1,dtype=float)))

def propagate(np,H,V,E,incoming,mask,field,steps,kappa):
    M=field['H0'].shape[0]-1;state=np.zeros((64,M+1,7),dtype=complex);state[:,0,:]=incoming
    snapshots=[];dt=2./steps;p=1/(2-2**(1/3));composition=(p,1-2*p,p)
    def ukick(s):return (V*np.exp(-1j*E*s))@V.conj().T
    kicks=[ukick(c*dt/2) for c in composition]
    field0=[np.exp(-1j*np.diag(field['H0'])*c*dt) for c in composition]
    field1=[(field['u']*np.exp(-1j*field['e']*c*dt))@field['u'].conj().T for c in composition]
    for n in range(1,steps+1):
        if kappa!=0:
            for U,d0,U1 in zip(kicks,field0,field1):
                state=(U@state.reshape(64,-1)).reshape(state.shape)
                state[~mask]*=d0[None,:,None]
                state[mask]=np.einsum('ab,ibk->iak',U1,state[mask],optimize=True)
                state=(U@state.reshape(64,-1)).reshape(state.shape)
        if n in (steps//8,steps//2,steps):
            if kappa==0:state[:,0,:]=(V*np.exp(-1j*E*n*dt))@(V.conj().T@incoming)*np.exp(-1j*2*float(field['H0'][0,0]/2)*n*dt)
            snapshots.append(state.copy())
    return np.stack(snapshots)

def readout(np,state,H,mask,field,initial_energy,initial_norm,n0,omega,kappa,labels,q,edge,M,steps,tau,check):
    EN=expectation(np,state,H,0);EG=expectation(np,state,field['H0'],1);PH=expectation(np,state,field['N'],1)
    occupied=state*mask[:,None,None];EI=expectation(np,occupied,field['W'],1)
    source1=expectation(np,occupied,field['dH'],1);source2=expectation(np,occupied,field['ddH'],1)
    norms=np.sum(abs(state)**2,axis=(0,1));cut=np.sum(abs(state[:,-1,:])**2,axis=0)
    rows=[]
    for k,label in enumerate(labels):
        ids=dict(q=q,edge=edge,omega=omega,kappa=kappa,M=M,steps=steps,tau=tau,**label)
        photon_initial=2*omega*float(initial_norm[k]);energy_scale=max(1.,abs(float(initial_energy[k]))+photon_initial)
        imaginary=max(abs(v[k].imag) for v in (EN,EG,PH,EI,source1,source2))
        check('real_Hermitian_observables',float(imaginary)/energy_scale,CONFIG['norm_tolerance'],**ids)
        en,eg,ei,phot,s1,s2=(float(v[k].real) for v in (EN,EG,EI,PH,source1,source2))
        on=omega*kappa*kappa*float(n0[k])/(1+kappa);off=-ei;total=en+eg+ei
        native_change=en-float(initial_energy[k]);photon_change=eg-photon_initial
        ledger=native_change+photon_change+ei-on
        check('norm',abs(float(norms[k])-1),CONFIG['norm_tolerance'],**ids)
        check('inclusive_energy',abs(total-(float(initial_energy[k])+photon_initial+on))/energy_scale,CONFIG['energy_tolerance'],**ids)
        check('switch_ledger',abs(ledger)/energy_scale,CONFIG['energy_tolerance'],**ids)
        check('field_cutoff_probability',float(cut[k]),CONFIG['cutoff_probability_tolerance'],**ids)
        check('photon_nonnegative',max(0.,-phot),CONFIG['norm_tolerance'],**ids)
        if label['preparation']=='complete_native_ground':check('ground_has_no_native_energy_release',max(0.,-native_change)/energy_scale,CONFIG['energy_tolerance'],**ids)
        if kappa==0:
            check('zero_coupling_vacuum',abs(phot)+abs(photon_change)/energy_scale+abs(ei)/energy_scale,CONFIG['norm_tolerance'],**ids)
        rows.append(dict(**ids,initial_norm=float(initial_norm[k]),native_energy_initial=float(initial_energy[k]),photon_energy_initial=photon_initial,norm=float(norms[k]),native_energy=en,photon_free_energy=eg,interaction_energy=ei,total_on_energy=total,native_change=native_change,photon_change=photon_change,native_release=-native_change,photon_number=phot,pair_number=phot/2,each_polarization_mean_photon_number=phot/2,switch_on_work=on,switch_off_work=off,net_switch_work=on+off,ledger_residual=ledger,cutoff_probability=float(cut[k]),kappa_first_contact=s1,kappa_second_contact=s2,field_lapse_contact=eg+ei,native_lapse_contact=en,total_lapse_contact=total,field_spatial_first_contact=eg+ei,field_mixed_N_psi_contact=eg+ei,field_metric_second_contact=3*(eg+ei),ground_control=label['preparation']=='complete_native_ground'))
    return rows

def trials():return [(q,e,o,k,M,n) for q in CONFIG['record_occupations'] for e in CONFIG['incidences'] for o in CONFIG['omegas'] for k in CONFIG['kappas'] for M in CONFIG['cutoffs'] for n in CONFIG['steps']]
def cp_name(i):return STEM+'_CP'+str(i).zfill(4)
def check_row(kind,value,tolerance,**ids):return dict(kind=kind,value=float(value),tolerance=float(tolerance),passed=bool(math.isfinite(value) and value<=tolerance),**ids)
def validate_payload(np,d,i,t):
    keys={'index','trial','owner','pid','epoch','source_sha256','manifest_sha256','npz','npz_sha256','rows','checks'}
    require(set(d)==keys and d['index']==i and d['trial']==list(t),'Exact checkpoint schema/census')
    require(d['owner']=='root' and type(d['pid']) is int and d['pid']>0 and type(d['epoch']) is int and d['source_sha256']==SOURCE_SHA and d['manifest_sha256']==MANIFEST_SHA,'Checkpoint owner/source')
    finite_tree(d);require(len(d['rows'])==21 and [(r['tau'],r['preparation'],r['age']) for r in d['rows']]==[(tau,p,a) for tau in CONFIG['durations'] for p,a in [('cycle',0.),('cycle',.5),('cycle',2.),('tree',0.),('tree',.5),('tree',2.),('complete_native_ground',None)]],'Complete row order')
    q,e,o,k,M,n=t
    require(all((r['q'],r['edge'],r['omega'],r['kappa'],r['M'],r['steps'])==(q,e,o,k,M,n) for r in d['rows']),'Complete physical trial labels')
    rowkeys={'q','edge','omega','kappa','M','steps','tau','preparation','age','initial_norm','native_energy_initial','photon_energy_initial','norm','native_energy','photon_free_energy','interaction_energy','total_on_energy','native_change','photon_change','native_release','photon_number','pair_number','each_polarization_mean_photon_number','switch_on_work','switch_off_work','net_switch_work','ledger_residual','cutoff_probability','kappa_first_contact','kappa_second_contact','field_lapse_contact','native_lapse_contact','total_lapse_contact','field_spatial_first_contact','field_mixed_N_psi_contact','field_metric_second_contact','ground_control'}
    require(all(set(r)==rowkeys and type(r['ground_control']) is bool and r['ground_control']==(r['preparation']=='complete_native_ground') for r in d['rows']),'Exact complete readout schema')
    expected=[('owned_incidence_projector',CONFIG['operator_tolerance'])]+[('field_positive_'+name,CONFIG['operator_tolerance']) for name in ('HD','HB','H1')]+[('projector_inverse_W',CONFIG['operator_tolerance'])]
    for row in d['rows']:
        expected.extend((kind,CONFIG[tol]) for kind,tol in (('real_Hermitian_observables','norm_tolerance'),('norm','norm_tolerance'),('inclusive_energy','energy_tolerance'),('switch_ledger','energy_tolerance'),('field_cutoff_probability','cutoff_probability_tolerance'),('photon_nonnegative','norm_tolerance')))
        if row['ground_control']:expected.append(('ground_has_no_native_energy_release',CONFIG['energy_tolerance']))
        if k==0:expected.append(('zero_coupling_vacuum',CONFIG['norm_tolerance']))
    require([(c['kind'],c['tolerance']) for c in d['checks']]==expected and all(type(c['passed']) is bool and c['passed']==(c['value']<=c['tolerance']) and c['value']>=0 for c in d['checks']),'Exact check census/criteria/dispositions')
    require(d['npz']==cp_name(i)+'.npz' and sha(BASE/d['npz'])==d['npz_sha256'],'Joint state bytes')
    with np.load(BASE/d['npz'],allow_pickle=False) as z:
        require(set(z.files)=={'states'} and z['states'].shape==(3,64,M+1,7) and bool(np.isfinite(z['states']).all()),'Full joint state array')
    return d
def recover(np,resume):
    jp=BASE/(STEM+'_JOURNAL.jsonl');runtime=list(BASE.glob(STEM+'_CP*'));rows=[];epoch=-1;pid=None
    require(resume or not runtime,'Existing checkpoints require --resume')
    if jp.exists():
        for e in [json.loads(x) for x in jp.read_text().splitlines()]:
            require(e['owner']=='root' and type(e['pid']) is int and e['pid']>0 and e['source_sha256']==SOURCE_SHA and e['manifest_sha256']==MANIFEST_SHA,'Journal owner/source')
            if e['event'] in ('OWNER_START','OWNER_RESUME'):
                require(e['epoch']==epoch+1 and e['event']==('OWNER_START' if epoch<0 else 'OWNER_RESUME'),'Owner epoch sequence');epoch=e['epoch'];pid=e['pid']
            else:require(e['epoch']==epoch and e['pid']==pid,'Current owner epoch')
            if e['event']=='CHECKPOINT':
                i=len(rows);require(e['index']==i and e['payload']==cp_name(i)+'.json' and e['commit']==cp_name(i)+'_COMMIT.json','Ordered global prefix')
                p=BASE/e['payload'];c=BASE/e['commit'];require(sha(p)==e['payload_sha256'] and sha(c)==e['commit_sha256'],'Committed bytes')
                commit=read(c);require(commit=={k:e[k] for k in ('index','payload','payload_sha256','owner','pid','epoch','source_sha256','manifest_sha256')},'Exact checkpoint commit')
                d=validate_payload(np,read(p),i,trials()[i]);require(d['epoch']==epoch and d['pid']==pid,'Payload current epoch');require(p.read_bytes()==canonical(d) and c.read_bytes()==canonical(commit),'Canonical checkpoint bytes')
                rows.append(d)
                for f in (p,c,BASE/d['npz']):CREATED[str(f)]=sha(f)
            require(e['event'] in ('OWNER_START','OWNER_RESUME','CHECKPOINT','FAILED'),'No unexpected/terminal journal')
    expected={name for i in range(len(rows)) for name in (cp_name(i)+'.json',cp_name(i)+'_COMMIT.json',cp_name(i)+'.npz')}
    require({p.name for p in runtime}==expected,'No orphan/uncommitted checkpoint files')
    return rows,epoch

def main():
    global SOURCE_SHA,MANIFEST_SHA,EPOCH,ENTERED
    ap=argparse.ArgumentParser();ap.add_argument('--resume',action='store_true');args=ap.parse_args();start=time.monotonic()
    import numpy as np
    SOURCE_SHA=sha(__file__);r,packet=authenticate();fixed=dict(configuration=CONFIG,source_sha256=SOURCE_SHA,input_sha256=SEALS.copy(),numpy_version=np.__version__,scope=SCOPE,units='Eunit global and tau=Eunit*tproper/hbar symbolic; omega here hbar*omega_physical/Eunit; no cosmic temperature')
    mp=BASE/(STEM+'_MANIFEST.json');jp=BASE/(STEM+'_JOURNAL.jsonl')
    require(not any((BASE/(STEM+s)).exists() for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json')),'No completed output overwrite')
    require(args.resume or not (BASE/(STEM+'_ERROR.json')).exists(),'Existing failure needs --resume')
    require(mp.exists() or not (jp.exists() or list(BASE.glob(STEM+'_CP*'))),'Orphan runtime before manifest')
    if mp.exists():
        require(args.resume and read(mp)==fixed and mp.read_bytes()==canonical(fixed),'Exact resumed manifest')
        require(jp.exists() and bool(jp.read_text().strip()),'Existing manifest requires original owner journal')
    else:write(mp.name,fixed)
    MANIFEST_SHA=sha(mp);CREATED[str(mp)]=MANIFEST_SHA;saved,epoch=recover(np,args.resume);EPOCH=epoch+1;ENTERED=True
    previous_error=BASE/(STEM+'_ERROR.json')
    if previous_error.exists():CREATED[str(previous_error)]=sha(previous_error)
    event('OWNER_RESUME' if args.resume else 'OWNER_START',completed_prefix=len(saved),previous_error_sha256=sha(previous_error) if previous_error.exists() else None)
    allchecks=[];data={}
    def precheck(kind,value,tol,**ids):allchecks.append(check_row(kind,value,tol,**ids))
    for q in CONFIG['record_occupations']:data[q]=native_data(np,q,packet,precheck)
    outputs=saved.copy()
    for i,t in enumerate(trials()):
        if i<len(saved):continue
        q,edge,omega,kappa,M,steps=t;H,V,E,incoming,labels,w=data[q];mask=np.array([bool((word>>edge)&1) for word in range(16) for carrier in range(4)])
        observed=V.conj().T@np.diag(mask.astype(float))@V;reference=complex_array(np,w['incidence_spectral'][CONFIG['incidences'].index(edge)],(64,64))
        local=[]
        def check(kind,value,tol,**ids):local.append(check_row(kind,value,tol,**ids))
        check('owned_incidence_projector',float(np.max(abs(observed-reference))),CONFIG['operator_tolerance'],q=q,edge=edge)
        field=field_data(np,omega,M,kappa,check);states=propagate(np,H,V,E,incoming,mask,field,steps,kappa)
        EN=expectation(np,incoming[:,None,:],H,0).real;norm0=np.sum(abs(incoming)**2,axis=0);n0=np.sum(abs(incoming[mask])**2,axis=0);rows=[]
        for j,tau in enumerate(CONFIG['durations']):rows.extend(readout(np,states[j],H,mask,field,EN,norm0,n0,omega,kappa,labels,q,edge,M,steps,tau,check))
        recheck();name=cp_name(i)+'.npz'
        with (BASE/name).open('xb') as f:np.savez_compressed(f,states=states)
        (BASE/name).chmod(0o444);CREATED[str(BASE/name)]=sha(BASE/name)
        payload=dict(index=i,trial=list(t),owner='root',pid=os.getpid(),epoch=EPOCH,source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,npz=name,npz_sha256=sha(BASE/name),rows=rows,checks=local)
        h=write(cp_name(i)+'.json',payload);commit=dict(index=i,payload=cp_name(i)+'.json',payload_sha256=h,owner='root',pid=os.getpid(),epoch=EPOCH,source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA)
        ch=write(cp_name(i)+'_COMMIT.json',commit);event('CHECKPOINT',index=i,payload=commit['payload'],payload_sha256=h,commit=cp_name(i)+'_COMMIT.json',commit_sha256=ch)
        outputs.append(payload)
    comparisons=[];index={tuple(d['trial']):d for d in outputs}
    def compare(kind,left,right):
        ld,rd=index[left],index[right]
        with np.load(BASE/ld['npz'],allow_pickle=False) as f, np.load(BASE/rd['npz'],allow_pickle=False) as g:
            a=f['states'];b=g['states']
            # Photon axis is 2; retain full absolute phase and every native column.
            padded=np.zeros_like(b);padded[:,:,:a.shape[2],:]=a;err=np.sqrt(np.sum(abs(padded-b)**2,axis=(1,2)))
        for j,(lrow,rrow) in enumerate(zip(ld['rows'],rd['rows'])):
            value=float(err[j//7,j%7]);ids={k:rrow[k] for k in ('q','edge','omega','kappa','tau','preparation','age')}
            precheck(kind+'_joint_state',value,CONFIG['state_tolerance'],left_M=left[4],right_M=right[4],left_steps=left[5],right_steps=right[5],**ids)
            signed={key:rrow[key]-lrow[key] for key in ('native_change','photon_change','interaction_energy','photon_number','net_switch_work','kappa_first_contact','kappa_second_contact')}
            comparisons.append(dict(kind=kind,**ids,left_M=left[4],right_M=right[4],left_steps=left[5],right_steps=right[5],joint_state_error=value,signed_changes=signed))
    for t in trials():
        q,e,o,k,M,n=t
        if n==128:compare('time',t,(q,e,o,k,M,256))
        if n==256 and M in (8,12):compare('cutoff',t,(q,e,o,k,12 if M==8 else 16,256))
    for d in outputs:allchecks.extend(d['checks'])
    require(len(outputs)==216 and sum(len(d['rows']) for d in outputs)==4536 and len(comparisons)==3780 and len(allchecks)==34256,'Full locked census/check count')
    completed,closing_epoch=recover(np,True)
    owner_events=[json.loads(x) for x in jp.read_text().splitlines()]
    require(len(completed)==216 and closing_epoch==EPOCH and owner_events[-1]['pid']==os.getpid(),'Complete current-root checkpoint prefix before publication')
    recheck();failed=[c for c in allchecks if not c['passed']];status='CANONICAL_MAXWELL_FIXTURE_PASS' if not failed else 'CANONICAL_MAXWELL_FIXTURE_NUMERICAL_FAIL'
    result=dict(status=status,scope=SCOPE,manifest=fixed,configuration=CONFIG,checkpoint_count=216,rows=[v for d in outputs for v in d['rows']],comparisons=comparisons,checks=allchecks,elapsed_seconds=time.monotonic()-start,physical_rates_or_thermalization_qualified=False)
    result_sha=write(STEM+'_RESULT.json',result)
    report=('# Canonical native Maxwell pair fixture\n\n'+status+'\n\nAll 4536 rows and 3780 signed comparisons retained. This is a homogeneous two-polarization finite-mode fixture; actual ordinary alpha matching/rate histories, localized recoil, continuum limit and thermal origin are not qualified.\n\nNumerical checks: '+str(len(allchecks))+'; failures: '+str(len(failed))+'. Absolute vacuum, interaction and switch work are retained.\n')
    rp=BASE/(STEM+'_REPORT.md')
    with rp.open('x') as f:f.write(report)
    rp.chmod(0o444);CREATED[str(rp)]=sha(rp);event('OWNER_COMPLETE',checkpoint_count=216,status=status,result_sha256=result_sha)
    terminal=json.loads(jp.read_text().splitlines()[-1])
    require(set(terminal)=={'time','event','owner','pid','epoch','source_sha256','manifest_sha256','checkpoint_count','status','result_sha256'} and terminal['event']=='OWNER_COMPLETE' and terminal['owner']=='root' and terminal['pid']==os.getpid() and terminal['epoch']==EPOCH and terminal['source_sha256']==SOURCE_SHA and terminal['manifest_sha256']==MANIFEST_SHA and terminal['checkpoint_count']==216 and terminal['status']==status and terminal['result_sha256']==result_sha,'Exact terminal owner/census/result identity')
    jp.chmod(0o444);CREATED[str(jp)]=sha(jp);recheck()
    receipt=dict(status=status,source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,input_sha256=SEALS,output_sha256=CREATED.copy(),journal_sha256=sha(jp),result_sha256=result_sha,report_sha256=sha(rp),checkpoint_count=216)
    write(STEM+'_RECEIPT.json',receipt);recheck();print(json.dumps(dict(status=status,checks=len(allchecks),failures=len(failed),rows=4536,elapsed_seconds=result['elapsed_seconds'])));return 0 if not failed else 3

if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as e:
        if ENTERED:
            p=BASE/(STEM+'_ERROR.json')
            if not p.exists():write(p.name,dict(time=now(),owner='root',pid=os.getpid(),epoch=EPOCH,source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,error=repr(e)))
            event('FAILED',error=repr(e))
        raise
