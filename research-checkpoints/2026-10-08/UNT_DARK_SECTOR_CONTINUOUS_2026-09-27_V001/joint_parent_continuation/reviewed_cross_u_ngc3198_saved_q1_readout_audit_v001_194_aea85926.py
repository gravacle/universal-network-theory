#!/usr/bin/env python3
"""Guarded saved-state Q1 readout audit; no scientific producer/helper imports."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,time,importlib
AUTHOR_DRAFT=True
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_SAVED_Q1_READOUT_AUDIT_V001'
PROTOCOL_SHA='f26e03efc1e075cb93a99b3c9cd98c9f2d4ddc913d6ee26920086f7f3dc9c2f1'
PINS = {'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006.md': 'acaca99c1c9c6fef56b50f1daf1b24c7d154f41f8fe53482797aa7f76e354e32', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_MANIFEST.json': '08252627c9809538690cac22f51fdf2a83606c016e7f731c87f1dfa2c979533b', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_RESULT.json': 'd470f406ec2279c9631f8e3e3c46a9e0d862f2a1691e1af6851b80aa871f3ff8', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_REPORT.md': '71e44896cafeb813f3d4676c285c29e7f6d63ccabf66634a2567ea98a4bc0d5a', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_RECEIPT.json': '581605c923df95b6008ccf0fabe7ce1fc7ce7533e5d7cd2b2b51e36d90899b3f', 'cross_u_ngc3198_native_elimination_recovery_v006.py': '3d707e5d078980202cca884b18175673cfcfa649e7a01e7e0805cd6c6f7c8170', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_E1em05_HI0_H20_CASE.json': 'a15aac98b954c86af73b85be7c8498ecec3b70da60553837353c4bfd21cab599', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_00148_FINAL.npz': 'ce35318b55b6f6afc7f225154aec7deb1587887a912b38962a751d9db97fa6fc', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_00148_FINAL.npz.COMMIT.json': 'e14fc7e7268207cb6abb3de025c2a79abf2112bda88da8d10e4e92ddeb6a6ede', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V007.md': '4a8d5ec49a2104479e7664c1512fb8c6bc61fff839b6db424f10e9463cbdb359', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V007_MANIFEST.json': 'b3b0138afd4b4a211c1c81a63857184830a9868a27a946ff272831915a2d2a02', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V007_RESULT.json': 'f28072d52afcdb7835307be5625dff7decdcf20fe8b2e78151f3f7106e21e82d', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V007_REPORT.md': '3640fbe1cc8c141c7dacc77da69f884e41ff6293357541849bdea96430602068', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V007_RECEIPT.json': '5e10f5418cb697b521b53c2d938ad05e16db0caa11150511dcd69e29e741af5b', 'cross_u_ngc3198_native_elimination_recovery_v007.py': '0ba1deef983516b903a7a6ce0e5434add6a6718e73c584f78ec0c0b33c242ffe', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V007_E1em05_HI0_H21_CASE.json': '20312ff336e4433c872838253c2e581f4cb5f6d92fdfb65f574008cd320551f7', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V007_00144_FINAL.npz': 'b8ac11bb0847374ce45aece5a0a9b60717406fae51c3341f9f7bde03b50256fa', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V007_00144_FINAL.npz.COMMIT.json': 'ed975a4c419554b7ec4326faba0de66573b632c343f0f94715d99f73138f0778', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V007_E1em05_HI1_H20_CASE.json': '2825b1aea06b4ce469d352b77ea410d4cd6783cee326000a3d9fe73246b1813b', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V007_00289_FINAL.npz': '6148586719b2f926ec85c9ae3c6a2bb7fd04f3d112753a91a4b830de01907a6c', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V007_00289_FINAL.npz.COMMIT.json': '6645c34faec01acae2a390dec05c883146c2c84466c3eb265d1a00f19876be1b', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008.md': 'a9b0780d632c351aab9820a8118ea249e06f8cfac6329db0eea9ab34bf294d80', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008_MANIFEST.json': 'ff8226e41aabc3b6b9da006cc5a9811346f99709c85471f72a31a903e7599d46', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008_COARSE_Q3_CASE.json': '7f599bacaff6fcfd86aaf1015c8210347f166bf2052e3b4d459d3f608af7d18c', 'cross_u_ngc3198_space_quadrature_recovery_v008.py': '8ebcc132c3933aae2e4868092f13187680aeacd0d94fa74e88790fb14b4c0627', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008_00021_FINAL.npz': '1b6d5410070632fa362813cc63b5b1cef772f0e0b36ff64993e055388c393da1', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008_00021_FINAL.npz.COMMIT.json': 'fe72aa126a0530f27d7fc848cc26c0d6c63ae6afb2ca8e78e89b78c33d719e76', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008_RESULT.json': 'b7c1694a99aed6fbde84324ae9454b30cc50c008d49c535b9cb3603875089b7d', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008_REPORT.md': 'f32ce9d0e268f23aae592848392048da741e037834c6875f76dea9225bf80e02', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008_RECEIPT.json': 'fb417f6d3125db4c8d50c9157ae9a80e6fc689954c9d912338ba40e2effaedb1', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008_FINE_Q2_CASE.json': '3135ac369d68536c6d0ae68e625cc3c75935e7565a0c858785ad6d6ffb92b1c2', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008_FINE_Q3_CASE.json': 'f925f0103d4cc7ae6fdc1f517ab118ed929903d910bc4cc184afd093327befa1', 'cross_u_ngc3198_nonlinear_disk_v001.py': 'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1', 'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76', '../ngc3198_sparc_excerpt_v001.txt': '58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900', 'NGC3198_BARYON_INPUT.json': '8895693861ee0db1b42136c6aac7f0fb9fa9e0e84c72c69e8c8e3c89ba0e78d1', 'author_workdraft_cross_u_ngc3198_saved_q1_readout_audit_v001_187_436cd9b1.py': '436cd9b11656f41d135a3b0cc01e7aa67ce14f54d4e5c6a2289a0ac226d7551f', 'author_workdraft_cross_u_ngc3198_saved_q1_readout_audit_v001_21_2b8b461d.md': '2b8b461dbb34be1eacdeb7d2d77573418f9db6d6248cac0955eb59e06acbfaa3', 'reviewed_cross_u_ngc3198_saved_q1_readout_audit_v001_194_661b934d.py': '661b934dbbefeafb291ead075d1e913e73909692179dba4a3c64477221824d4b', 'reviewed_cross_u_ngc3198_saved_q1_readout_audit_v001_21_6a1573a5.md': '6a1573a57ee390b878a2d3c89d204c2adc8c90bdb85ccf705836b630573c6655'}
PARENTS=('CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006', 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V007', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008')
SOURCES=('cross_u_ngc3198_native_elimination_recovery_v006.py','cross_u_ngc3198_native_elimination_recovery_v007.py','cross_u_ngc3198_space_quadrature_recovery_v008.py')
CASES=(('V006_COARSE_Q2',0,'E1em05_HI0_H20','E1em05_HI0_H20'),('V007_HI0_H21',1,'E1em05_HI0_H21','E1em05_HI0_H21'),('V007_HI1_H20',1,'E1em05_HI1_H20','E1em05_HI1_H20'),('V008_COARSE_Q3',2,'COARSE_Q3','E1em05_HI0_H20_COARSE_Q3'),('V008_FINE_Q2',2,'FINE_Q2','E1em05_HI0_H20_FINE_Q2'),('V008_FINE_Q3',2,'FINE_Q3','E1em05_HI0_H20_FINE_Q3'))
CROSS=((0,3),(0,4),(0,5),(3,5),(4,5))
A0=1.0059833281731022e-10
KPC=3.085677581491367e19
A0_V=A0*KPC/1e6
TOL=1e-11
PHYSICAL={k:False for k in ('readout_qualified','full_metric_qualified','lensing_qualified','refinement_qualified','stability_qualified','FLRW_junction_qualified','formation_qualified','fit_qualified','joint_superiority_qualified','parameter_adopted')}
np=None;OWNER=None;CREATED={};RECORDS=[];RAW={};CONTEXT={};FLAGS=[];CONTROL_ORDINAL=0;MERGED={}

def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def tree(x):
    if isinstance(x,float):assert math.isfinite(x)
    elif isinstance(x,dict):
        assert all(isinstance(k,str) for k in x)
        for v in x.values():tree(v)
    elif isinstance(x,list):
        for v in x:tree(v)
    else:assert x is None or isinstance(x,(str,int,bool))
def encode(x):tree(x);return (json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def load(name):x=json.loads((BASE/name).read_text());tree(x);return x
def inputs():return dict(PINS,**{STEM+'.md':PROTOCOL_SHA})
def auth():
    assert not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64
    for n,h in inputs().items():assert isinstance(h,str) and len(h)==64 and sha(BASE/n)==h,('unbound or changed input',n)
def merge(a):
    for n,h in a.items():
        assert isinstance(n,str) and isinstance(h,str) and len(h)==64 and sha(BASE/n)==h
        assert n not in MERGED or MERGED[n]==h;MERGED[n]=h

def parents():
    merge(inputs());out=[]
    for st,source in zip(PARENTS,SOURCES):
        rc=load(st+'_RECEIPT.json');m=load(st+'_MANIFEST.json');r=load(st+'_RESULT.json')
        assert rc['status']=='CLOSED' and rc['owner']==m['owner'] and r['manifest']==m
        owner=rc['owner'];assert owner['owner']=='root' and isinstance(owner['pid'],int) and owner['pid']>0 and rc['closed']>owner['started'] and owner['source_sha256']==PINS[source]
        assert rc['input_sha256']==m['input_sha256'] and rc['result_sha256']==rc['output_sha256'][st+'_RESULT.json']==PINS[st+'_RESULT.json']
        assert rc['output_sha256'][st+'_REPORT.md']==PINS[st+'_REPORT.md']
        assert rc['qualification']==r['qualification']==m['qualification'] and all(v is False for v in rc['qualification'].values())
        merge(rc['input_sha256']);merge(rc['output_sha256']);assert len(r['cases'])==(1 if st==PARENTS[0] else 2 if st==PARENTS[1] else 3)
        out.append((rc,m,r))
    return out

def select(allparents):
    selected=[];measure=None
    for label,pindex,suffix,caseid in CASES:
        rc,m,r=allparents[pindex];name=PARENTS[pindex]+'_'+suffix+'_CASE.json';c=load(name)
        assert rc['output_sha256'][name]==PINS[name] and c in r['cases'] and c['identity']['case']==caseid
        assert c['readout_qualified'] is False and all(v is False for v in c['physical_flags'].values()) and len(c['rows'])==43
        i=c['identity'];assert i['eps']==1e-5 and i['source_sha256']==PINS['cross_u_ngc3198_nonlinear_disk_v001.py'] and i['grid_shape'][0]==65
        assert i['h2_tail']==(label=='V007_HI0_H21') and i['hi_tail']==(label=='V007_HI1_H20')
        key='space_quadrature' if pindex==2 else 'native_elimination'
        assert i[key+'_source_sha256']==PINS[SOURCES[pindex]] and i[key+'_manifest_sha256']==sha(BASE/(PARENTS[pindex]+'_MANIFEST.json'))
        f=[p for p in c['own_checkpoints'] if p['metadata'].get('kind')=='final_state'];assert len(f)==1;rec=f[0]
        assert all(rec[k]==rc['output_sha256'][rec[n]]==sha(BASE/rec[n]) for k,n in (('sha256','file'),('commit_sha256','commit_file')))
        assert load(rec['commit_file'])=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
        md=rec['metadata'];assert md['identity']==i and md['history']==c['history'] and md['status']==c['status'] and md['owner']==rc['owner'] and set(md['schema'])=={'state','residual','pre'}
        assert all(s==dict(dtype='float64',finite=True,shape=i['grid_shape']) for s in md['schema'].values())
        obs=[{k:a[k] for k in ('R','velocity','error')} for a in c['rows']]
        assert all(a['R']>0 and a['velocity']>=0 and a['error']>0 for a in obs) and len({a['R'] for a in obs})==43
        if measure is None:measure=obs
        else:assert obs==measure
        selected.append(dict(label=label,parent=pindex,case=c,final=rec,observations=obs))
    return selected

def publish(name,obj):
    b=encode(obj);p=BASE/name
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);assert p.read_bytes()==b;CREATED[name]=sha(p);return CREATED[name]
def cp(tag,arrays,metadata):
    schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in arrays.items()}
    text=encode(dict(metadata,owner=OWNER,schema=schema)).decode();md=json.loads(text);p=BASE/f'{STEM}_{len(RECORDS):03d}_{tag}.npz'
    with p.open('xb') as f:np.savez_compressed(f,metadata=text,**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[p.name]=sha(p);rec=dict(file=p.name,sha256=CREATED[p.name],metadata=md)
    ch=publish(p.name+'.COMMIT.json',rec);rec=dict(rec,commit_file=p.name+'.COMMIT.json',commit_sha256=ch);RECORDS.append(rec)
    with np.load(p,allow_pickle=False) as x:
        assert str(x['metadata'])==text and set(x.files)==set(arrays)|{'metadata'}
        for k,v in arrays.items():assert np.array_equal(x[k],v,equal_nan=True)
    return rec

def recheck(ownerbytes):
    auth();select(parents());assert (BASE/(STEM+'_OWNER_START.json')).read_bytes()==ownerbytes and sha(__file__)==OWNER['source_sha256']
    for n,h in CREATED.items():assert sha(BASE/n)==h
    for rec in RECORDS:
        assert load(rec['commit_file'])=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
        with np.load(BASE/rec['file'],allow_pickle=False) as x:
            assert json.loads(str(x['metadata']))==rec['metadata'] and set(x.files)==set(rec['metadata']['schema'])|{'metadata'}
            for k,s in rec['metadata']['schema'].items():
                a=x[k];assert s==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))
    assert set(p.name for p in BASE.glob(STEM+'_*'))==set(CREATED)

def check(name,actual,expected):
    global CONTROL_ORDINAL
    CONTROL_ORDINAL+=1;prefix=f'control_{CONTROL_ORDINAL:03d}_{name}'
    a=np.asarray(actual);b=np.asarray(expected);RAW[prefix+'_actual']=a.copy();RAW[prefix+'_expected']=b.copy();CONTEXT.update(control=name,ordinal=CONTROL_ORDINAL)
    assert a.shape==b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b))
    err=float(np.max(np.abs(a-b),initial=0.));scale=max(1.,float(np.max(np.abs(b),initial=0.)))
    q=dict(name=name,ordinal=CONTROL_ORDINAL,error=err,scale=scale,tolerance=TOL,passed=err<=TOL*scale);FLAGS.append(q);assert q['passed'],q
    return q

def samples(r,y,R):
    left=[];right=[];indices=[];nodes=[];psi=[]
    for value in R:
        assert r[0]<value<r[-1];i=int(np.searchsorted(r,value,side='left'));node=bool(r[i]==value)
        lo=i-1;hi=i if node else lo;assert 0<=lo<len(r)-1 and 0<=hi<len(r)-1
        left.append((y[lo+1]-y[lo])/(r[lo+1]-r[lo]));right.append((y[hi+1]-y[hi])/(r[hi+1]-r[hi]));indices.append((lo,hi));nodes.append(node)
        t=(value-r[lo])/(r[lo+1]-r[lo]);psi.append((1-t)*y[lo]+t*y[lo+1])
    return np.array(left),np.array(right),np.array(indices,dtype=np.int64),np.array(nodes,dtype=np.bool_),np.array(psi)

def datum(slope,R,observed):
    v2=float(R*A0_V*slope);speed=math.sqrt(v2) if v2>=0 else None
    return dict(radial_force_a0=float(slope),velocity_squared=v2,negative_force=bool(slope<0),model_velocity=speed,velocity_residual=None if speed is None else speed-observed,undefined_speed_reason=None if speed is not None else 'negative_velocity_squared')

def readout(item):
    RAW.clear();CONTEXT.clear();CONTEXT.update(stage='readout',label=item['label']);start=len(FLAGS);c=item['case'];md=item['final']['metadata'];i=c['identity']
    r=np.array(i['r_kpc'],dtype=float);z=np.array(i['z_kpc'],dtype=float);RAW.update(r_kpc=r,z_kpc=z)
    assert r.ndim==z.ndim==1 and r[0]==z[0]==0 and np.all(np.diff(r)>0) and np.all(np.diff(z)>0) and i['grid_shape']==[65,len(r),len(z)]
    with np.load(BASE/item['final']['file'],allow_pickle=False) as x:
        for k in x.files:
            if k!='metadata':RAW['current_parent_'+k]=x[k].copy()
        assert json.loads(str(x['metadata']))==md and set(x.files)==set(md['schema'])|{'metadata'}
        for k,s in md['schema'].items():
            a=x[k];assert dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))==s
        psi=x['state'][0,:,0].copy();RAW['psi_midplane']=psi
    for k in md['schema']:RAW.pop('current_parent_'+k)
    R=np.array([a['R'] for a in item['observations']]);RAW['observed_R']=R
    oldgradient=np.gradient(psi,r,edge_order=2);RAW['old_nodal_gradient']=oldgradient
    old=np.interp(R,r,oldgradient);RAW['old_force']=old
    slopes=np.diff(psi)/np.diff(r);RAW['cell_slopes']=slopes
    left,right,indices,nodes,potential=samples(r,psi,R);RAW.update(Q1_left=left,Q1_right=right,Q1_cells=indices,Q1_exact_node=nodes,Q1_observed_potential=potential)
    check('old_force',old,np.array([a['radial_force_a0'] for a in c['rows']]))
    check('old_v2',R*A0_V*old,np.array([a['velocity_squared'] for a in c['rows']]))
    check('Q1_cell_increment',slopes*np.diff(r),np.diff(psi));check('Q1_observed_potential',potential,np.interp(R,r,psi));rows=[]
    for k,obs in enumerate(item['observations']):
        legacy=datum(old[k],R[k],obs['velocity']);l=datum(left[k],R[k],obs['velocity']);rr=datum(right[k],R[k],obs['velocity'])
        rows.append(dict(obs,old=legacy,prior_row=c['rows'][k],Q1_left=l,Q1_right=rr,exact_mesh_node=bool(nodes[k]),left_cell=int(indices[k,0]),right_cell=int(indices[k,1]),Q1_interpretation='two_one_sided_node_limits' if nodes[k] else 'unique_open_cell',left_minus_old_force=float(left[k]-old[k]),right_minus_old_force=float(right[k]-old[k]),left_minus_old_v2=float(l['velocity_squared']-legacy['velocity_squared']),right_minus_old_v2=float(rr['velocity_squared']-legacy['velocity_squared'])))
    retained=dict(label=item['label'],identity=i,parent_status=c['status'],parent_numerical_residual=c['numerical_residual'],parent_controls=c['controls'],parent_history=c['history'],parent_readout_qualified=c['readout_qualified'],parent_physical_flags=c['physical_flags'],parent_final_state=item['final'],rows=rows,controls=FLAGS[start:],qualification=PHYSICAL)
    rec=cp(item['label'],dict(RAW),retained);retained['checkpoint']=rec
    return dict(r=r,psi=psi,retained=retained)

def cross(a,b):
    RAW.clear();CONTEXT.clear();CONTEXT.update(stage='crossmesh',left=a['retained']['label'],right=b['retained']['label']);start=len(FLAGS)
    ra,rb=a['r'],b['r'];assert ra[0]==rb[0] and ra[-1]==rb[-1]
    r=np.union1d(ra,rb);RAW['common_R']=r
    mid=r[:-1]+np.diff(r)/2;RAW['open_interval_midpoints']=mid
    pa=np.interp(r,ra,a['psi']);RAW['left_potential']=pa
    pb=np.interp(r,rb,b['psi']);RAW['right_potential']=pb
    sa=samples(ra,a['psi'],mid)[0];RAW['left_cell_slope']=sa
    sb=samples(rb,b['psi'],mid)[0];RAW['right_cell_slope']=sb
    RAW.update(right_minus_left_potential=pb-pa,right_minus_left_slope=sb-sa,right_minus_left_v2=mid*A0_V*(sb-sa))
    check('left_common_increment',sa*np.diff(r),np.diff(pa));check('right_common_increment',sb*np.diff(r),np.diff(pb));rows=[]
    for x,y in zip(a['retained']['rows'],b['retained']['rows']):
        assert all(x[k]==y[k] for k in ('R','velocity','error'))
        rows.append(dict(R=x['R'],left_exact_mesh_node=x['exact_mesh_node'],right_exact_mesh_node=y['exact_mesh_node'],old_force_difference=y['old']['radial_force_a0']-x['old']['radial_force_a0'],Q1_left_force_difference=y['Q1_left']['radial_force_a0']-x['Q1_left']['radial_force_a0'],Q1_right_force_difference=y['Q1_right']['radial_force_a0']-x['Q1_right']['radial_force_a0'],Q1_left_v2_difference=y['Q1_left']['velocity_squared']-x['Q1_left']['velocity_squared'],Q1_right_v2_difference=y['Q1_right']['velocity_squared']-x['Q1_right']['velocity_squared']))
    m=dict(left=a['retained']['label'],right=b['retained']['label'],left_parent_final_state=a['retained']['parent_final_state'],right_parent_final_state=b['retained']['parent_final_state'],rows=rows,controls=FLAGS[start:],qualification=PHYSICAL)
    rec=cp('CROSS',dict(RAW),m);m['checkpoint']=rec;return m

def main():
    global np,OWNER
    auth();assert not list(BASE.glob(STEM+'_*')),'Existing runtime namespace preserved';allparents=parents();items=select(allparents)
    OWNER=dict(owner='root',pid=os.getpid(),source_sha256=sha(__file__),started=now());assert OWNER['pid']>0;tick=time.monotonic();ownerbytes=encode(OWNER)
    try:
        publish(STEM+'_OWNER_START.json',OWNER);manifest=dict(owner=OWNER,input_sha256=dict(MERGED),parents=[p[1] for p in allparents],fixed_cases=[a[0] for a in CASES],cross_pairs=[list(a) for a in CROSS],A0_SI=A0,kpc_SI=KPC,A0_V=A0_V,arithmetic_tolerance=TOL,predetermined_control_count=34,physics_changes=[],qualification=PHYSICAL)
        publish(STEM+'_MANIFEST.json',manifest);np=importlib.import_module('numpy')
        data=[readout(i) for i in items];comparisons=[cross(data[a],data[b]) for a,b in CROSS]
        assert len(FLAGS)==CONTROL_ORDINAL==34 and len(RECORDS)==11 and all(a['passed'] for a in FLAGS)
        result=dict(status='ARITHMETIC_PASS',manifest=manifest,cases=[a['retained'] for a in data],comparisons=comparisons,controls=FLAGS,checkpoint_pairs=RECORDS,elapsed_seconds=time.monotonic()-tick,qualification=PHYSICAL)
        rh=publish(STEM+'_RESULT.json',result)
        report='# Saved Q1 galaxy readout audit V001\n\nAll six frozen fields and five fixed mesh comparisons retained. Literal smoothed forces and exact Q1 one-sided cell slopes are reported without selection or fitting. The 34 predicates are arithmetic checks; all physical and observational qualifications remain false.\n'
        p=BASE/(STEM+'_REPORT.md');raw=report.encode()
        with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        p.chmod(0o444);assert p.read_bytes()==raw;CREATED[p.name]=sha(p);recheck(ownerbytes)
        publish(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=OWNER,closed=now(),input_sha256=dict(MERGED),output_sha256=dict(CREATED),result_sha256=rh,qualification=PHYSICAL));recheck(ownerbytes)
        print('ARITHMETIC_PASS',len(FLAGS),'CASES',len(data),'CROSS',len(comparisons),flush=True);return 0
    except Exception as e:
        existing=sha(BASE/(STEM+'_RECEIPT.json')) if (BASE/(STEM+'_RECEIPT.json')).exists() else None
        if RAW:cp('ERROR_RAW',dict(RAW),dict(kind='unaccepted_failure_arrays',context=dict(CONTEXT),error_type=type(e).__name__,error=str(e),qualification=PHYSICAL))
        publish(STEM+'_ERROR.json',dict(owner=OWNER,context=dict(CONTEXT),error_type=type(e).__name__,error=str(e),controls=FLAGS,checkpoint_pairs=RECORDS,existing_receipt_sha256=existing,qualification=PHYSICAL))
        if existing is None:publish(STEM+'_RECEIPT.json',dict(status='ERROR',owner=OWNER,closed=now(),input_sha256=dict(MERGED),output_sha256=dict(CREATED),qualification=PHYSICAL))
        raise
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',action='store_true');a=p.parse_args();assert a.run,'Root --run required';raise SystemExit(main())
