"""Unexecuted root-only broken-Q1 volume and faithful cylindrical SIPG controls."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, importlib, json, math, os

BASE=Path(__file__).resolve().parent
STEM='CROSS_U_BROKEN_NATIVE_PROJECTION_CONTROLS_V001'
SPLIT='CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001'
V3='CROSS_U_NGC3198_MINRES_RECOVERY_V003'
AUTHOR_DRAFT=False
TOL=1e-11
ELL=.1
CASES=['E1em05_HI0_H20','E1em04_HI0_H20','E1em03_HI0_H20']
PINS={'CROSS_U_BROKEN_NATIVE_PROJECTION_CONTROLS_V001.md': '6325c4809386070b3a449a810408c9c87d7a4b84360cfee2f37f9930fa3cdf1f',
 'cross_u_nonzero_native_curvature_split_v001.py': 'a60415dd3983e91161b45428ce5c030ff27ec3b8dd03032aa9e42c9a30a2f028',
 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001.md': '3eb392f83607b7c6373c6d5cdae012fe7fba9984fd4ff37f74935bb1b2cebc0a',
 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RESULT.json': 'd20f71731fe822a5af9e7d78408a346b5414752d9378a2a062a1e4ae5f16b871',
 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RECEIPT.json': '1f1f1aa4c06cf74f54875aefed42dc347932debc4a321211a96a5b3623f7331a',
 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_MANIFEST.json': '3654b4e41dc9658447ce2f2bcbec5572eda5b61a7adfe4e34ec2b497fe22c44d',
 'cross_u_ngc3198_nonlinear_disk_v001.py': 'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1',
 'cross_u_ngc3198_minres_recovery_v003.py': '5f807a858ac7b00e29b724a39e4d1de4d96e102442530b067bbc2ee7953a5683',
 'CROSS_U_NGC3198_MINRES_RECOVERY_V003.md': '91f8df979025c53ee96601839e1adad7eacb6436b7444ab2e488c53fc9a01dc8',
 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RESULT.json': '9da87a64f0e37c17530d34aae0f2ffb0efdf16d610763adcddff875c0a87ec8c',
 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json': 'eee323ea063832eac8f9d731823cf9fd3e5135930e74d9a477646d60b5300eb5'}
np=None

def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def native(obj):
    if obj is None or type(obj) in (str,bool,int):return
    if type(obj) is float:assert math.isfinite(obj);return
    if type(obj) is list:
        for v in obj:native(v)
        return
    assert type(obj) is dict and all(type(k) is str for k in obj)
    for v in obj.values():native(v)
def encoded(obj):
    native(obj);return (json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def publish(name,obj):
    raw=encoded(obj);p=BASE/name
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);assert p.read_bytes()==raw;return sha(p)
def read(name):
    obj=json.loads((BASE/name).read_text());native(obj);return obj
def pin_merge(dst,src):
    for n,h in src.items():
        assert type(n) is str and type(h) is str and len(h)==64
        if n in dst:assert dst[n]==h
        dst[n]=h
def input_map():
    pins=dict(PINS);m=read(SPLIT+'_MANIFEST.json');r=read(SPLIT+'_RECEIPT.json')
    pin_merge(pins,m['input_sha256']);pin_merge(pins,r['output_sha256'])
    return pins
def authenticate(pins):
    for n,h in pins.items():assert not h.startswith('AUTHOR') and sha(BASE/n)==h,('changed input',n)
def closed(name):
    d=read(name)
    assert d['owner']=='root' and type(d['pid']) is int and d['pid']>0
    assert datetime.fromisoformat(d['started'])<datetime.fromisoformat(d['closed'])
    assert d['output_sha256']
    authenticate(d['output_sha256']);return d
def pair(name,commit,expected,commit_hash):
    assert sha(BASE/name)==expected and sha(BASE/commit)==commit_hash
    c=read(commit);assert c['file']==name and c['sha256']==expected
    return c
def save_arrays(label,arrays,metadata):
    raw=encoded(metadata);name=f'{STEM}_{label}.npz';p=BASE/name
    assert all(type(k) is str and np.all(np.isfinite(v)) for k,v in arrays.items())
    with p.open('xb') as f:
        np.savez_compressed(f,**arrays,metadata=raw.decode());f.flush();os.fsync(f.fileno())
    p.chmod(0o444);h=sha(p);cn=name+'.commit.json'
    ch=publish(cn,dict(file=name,sha256=h,owner='root',pid=os.getpid(),payload=metadata))
    with np.load(p,allow_pickle=False) as d:
        assert set(d.files)==set(arrays)|{'metadata'} and json.loads(str(d['metadata']))==metadata
        for k,v in arrays.items():assert np.array_equal(d[k],v)
    assert read(cn)['payload']==metadata
    return dict(file=name,sha256=h,commit=cn,commit_sha256=ch)
def check(label,error,envelope=1.):
    assert math.isfinite(error) and math.isfinite(envelope) and envelope>0
    return dict(name=label,error=float(error),envelope=float(envelope),tolerance=TOL,
                passed=abs(error)<=TOL*envelope)
def volume(r,z):
    dr=np.diff(r)[:,None];dz=np.diff(z)[None,:];out=[];a=1/math.sqrt(3)
    for u,v in ((-a,-a),(-a,a),(a,-a),(a,a)):
        rr=(r[:-1,None]+r[1:,None])/2+u*dr/2
        shapes=[((1+si*u)*(1+sj*v)/4,si*(1+sj*v)/(2*dr),sj*(1+si*u)/(2*dz))
                for si,sj in ((-1,-1),(1,-1),(-1,1),(1,1))]
        out.append((rr,rr*dr*dz/4,shapes))
    return out
def cells(a):
    return np.stack([a[...,i:a.shape[-2]-1+i,j:a.shape[-1]-1+j]
                     for i,j in ((0,0),(1,0),(0,1),(1,1))],axis=-1)
def evaluate(a,s):
    return tuple(sum(a[...,k]*x[t] for k,x in enumerate(s)) for t in range(3))
def inverse_four(values):
    roots=((-1,-1),(-1,1),(1,-1),(1,1));a=math.sqrt(3)
    return np.stack([sum(values[...,q]*(1+si*ui*a)*(1+sj*vj*a)/4
                         for q,(ui,vj) in enumerate(roots))
                     for si,sj in ((-1,-1),(1,-1),(-1,1),(1,1))],axis=-1)
def h_action(v,y,alpha):
    norm=np.sum(v*v,axis=1);t=1+alpha*norm;dot=np.sum(v*y,axis=1)
    return t[:,None]*y+2*alpha[:,None]*v*dot[:,None]
def local_forms(v,y,g,quadrules,alpha,sw):
    load=np.zeros_like(y);action=np.zeros_like(y);K=L=Q=mass=0.
    for rr,vol,s in quadrules:
        vv,_,_=evaluate(v,s);yy,_,_=evaluate(y,s);_,gr,gz=evaluate(g,s)
        bg=sw[:,None,None,None]*np.stack((gr,gz))[None]
        hy=h_action(vv,yy,alpha);norm=np.sum(vv*vv,axis=1);t=1+alpha*norm;h=1+3*alpha*norm
        gg=gr*gr+gz*gz;dot=vv[:,0]*gr+vv[:,1]*gz;cross=vv[:,0]*gz-vv[:,1]*gr
        K+=float(np.sum(vol*gg))
        L+=float(np.sum(vol*sw[:,None,None]**2*(gg/h+2*alpha*cross*cross/(t*h))))
        Q+=float(np.sum(vol*sw[:,None,None]**2*(alpha*norm*gg/t+2*alpha*dot*dot/(t*h))))
        mass+=float(np.sum(vol*np.sum(yy*hy,axis=1)))
        for k,(N,_,_) in enumerate(s):load[...,k]+=vol*N*bg;action[...,k]+=vol*N*hy
    return load,action,K,L,Q,mass
def axis_projection(v,free,g,q,alpha,sw):
    # Only first radial-cell v_R trace is strongly zero; all other faces remain unrestricted.
    dofs=((0,1),(0,3),(1,0),(1,1),(1,2),(1,3));nmode,_,_,nz,_=v.shape
    A=np.zeros((nmode,nz,6,6));b=np.zeros((nmode,nz,6));ans=free.copy()
    for rr,vol,s in q:
        vv,_,_=evaluate(v,s);_,gr,gz=evaluate(g,s);vv=vv[:,:,0]
        norm=np.sum(vv*vv,axis=1);t=1+alpha[:,0]*norm
        H=np.zeros((nmode,nz,2,2))
        for a in range(2):
            for c in range(2):H[...,a,c]=(t if a==c else 0)+2*alpha[:,0]*vv[:,a]*vv[:,c]
        bg=sw[:,None,None]*np.stack((gr[0],gz[0]))[None];vv0=vol[0]
        for i,(a,k) in enumerate(dofs):
            Nk=s[k][0];b[...,i]+=vv0*Nk*bg[:,a]
            for j,(c,l) in enumerate(dofs):A[...,i,j]+=vv0*Nk*s[l][0]*H[...,a,c]
    assert np.all(np.isfinite(A)) and np.all(np.diagonal(A,axis1=-2,axis2=-1)>0)
    y=np.linalg.solve(A,b);assert np.all(np.isfinite(y))
    ans[:,:,0]=0
    for i,(a,k) in enumerate(dofs):ans[:,a,0,:,k]=y[...,i]
    return ans
def projection(x,p,r,z,xi,w):
    q=volume(r,z);v=cells(np.stack((x[1::2],x[2::2]),axis=1));g=cells(p)
    sw=np.sqrt(w);alpha=(1/(w*(3*math.pi/8)**2*xi**4))[:,None,None]
    values=[];point_errors=[];point_envelopes=[]
    for rr,vol,s in q:
        vv,_,_=evaluate(v,s);_,gr,gz=evaluate(g,s);bg=sw[:,None,None,None]*np.stack((gr,gz))[None]
        norm=np.sum(vv*vv,axis=1);t=1+alpha*norm;h=1+3*alpha*norm
        cross=vv[:,0]*bg[:,1]-vv[:,1]*bg[:,0]
        yy=bg/h[:,None]+2*alpha[:,None]*np.stack((-vv[:,1],vv[:,0]),axis=1)*cross[:,None]/(t*h)[:,None]
        assert np.all(np.isfinite(yy));values.append(yy)
        hy=h_action(vv,yy,alpha);point_errors.append(float(np.max(abs(hy-bg))))
        dot=np.sum(vv*yy,axis=1)
        point_envelopes.append(max(1.,float(np.max(abs(bg))),float(np.max(abs(t[:,None]*yy)))+
                                   float(np.max(abs(2*alpha[:,None]*vv*dot[:,None])))))
    free=inverse_four(np.stack(values,axis=-1));axis=axis_projection(v,free,g,q,alpha,sw)
    b,A,K,L,Q,mass=local_forms(v,free,g,q,alpha,sw)
    ba,Aa,Ka,La,Qa,ma=local_forms(v,axis,g,q,alpha,sw);E=float(np.sum(b*free));Ea=float(np.sum(ba*axis))
    free_scale=max(1.,float(np.max(abs(b))),float(np.max(abs(A))))
    mask=np.ones(axis.shape,bool);mask[:,0,0,:,(0,2)]=False
    reeval=max(float(np.max(abs(evaluate(free,s)[0]-values[i]))) for i,(_,_,s) in enumerate(q))
    envelope=max(1.,abs(K),abs(L),abs(Q),abs(E),abs(mass),abs(Ea),abs(ma))
    controls=[check('pointwise_positive_H_inverse',max(point_errors),max(point_envelopes)),
              check('four_point_reconstruction',reeval,max(1.,float(np.max(abs(free))))),
              check('free_modal_residual',float(np.max(abs(b-A))),free_scale),
              check('free_coupling_equals_local_inverse',E-L,envelope),
              check('free_mass_equals_coupling',mass-E,envelope),
              check('free_direct_energy',K+mass-2*E-(K-E),envelope),
              check('quartic_partition',L+Q-float(np.sum(w))*K,envelope),
              check('strong_axis_radial_trace',float(np.max(abs(axis[:,0,0,:,(0,2)]))),1.),
              check('axis_free_residual',float(np.max(abs((ba-Aa)[mask]))),free_scale),
              check('axis_direct_energy',Ka+ma-2*Ea-(Ka-Ea),envelope),
              check('axis_projection_loss_nonnegative',min(0.,L-Ea),envelope)]
    return free,axis,dict(K=K,weighted_local_inverse=L,Q_quartic=Q,weight_sum=float(np.sum(w)),
             free_coupling=E,free_mass_energy=mass,Q_space_DG=L-E,free_direct_energy=K+mass-2*E,
             axis_coupling=Ea,axis_mass_energy=ma,Q_axis=L-Ea,axis_direct_energy=Ka+ma-2*Ea,
             axis_only_essential_restriction=True,controls=controls)
def face_shapes(hR,hZ,u,v):
    return [((1+si*u)*(1+sj*v)/4,si*(1+sj*v)/(2*hR),sj*(1+si*u)/(2*hZ))
            for si,sj in ((-1,-1),(1,-1),(-1,1),(1,1))]
def face_trace(a,idx,s,direction):
    vals=tuple(sum(a[:,idx[0],idx[1],k]*x[t] for k,x in enumerate(s)) for t in range(3))
    return vals[0],vals[direction+1]
def faces(r,z):
    a=1/math.sqrt(3);nr=len(r)-1;nz=len(z)-1
    for i in range(1,nr):
        for j in range(nz):
            for t in (-a,a):
                yield ((i-1,j),(i,j),face_shapes(r[i]-r[i-1],z[j+1]-z[j],1,t),
                       face_shapes(r[i+1]-r[i],z[j+1]-z[j],-1,t),0,
                       r[i]*(z[j+1]-z[j])/2,8*max(2/(r[i]-r[i-1]),2/(r[i+1]-r[i])),1,(0,1))
    for i in range(nr):
        for j in range(1,nz):
            for t in (-a,a):
                R=(r[i]+r[i+1])/2+t*(r[i+1]-r[i])/2
                yield ((i,j-1),(i,j),face_shapes(r[i+1]-r[i],z[j]-z[j-1],t,1),
                       face_shapes(r[i+1]-r[i],z[j+1]-z[j],t,-1),1,
                       R*(r[i+1]-r[i])/2,8*max(1/(z[j]-z[j-1]),1/(z[j+1]-z[j])),1,(0,1))
    for j in range(nz):
        for t in (-a,a):
            yield ((nr-1,j),None,face_shapes(r[-1]-r[-2],z[j+1]-z[j],1,t),None,0,
                   r[-1]*(z[j+1]-z[j])/2,16/(r[-1]-r[-2]),1,(0,1))
    for i in range(nr):
        for t in (-a,a):
            R=(r[i]+r[i+1])/2+t*(r[i+1]-r[i])/2
            for j,v,sgn,components in ((nz-1,1,1,(0,1)),(0,-1,-1,(1,))):
                yield ((i,j),None,face_shapes(r[i+1]-r[i],z[j+1]-z[j],t,v),None,1,
                       R*(r[i+1]-r[i])/2,8/(z[j+1]-z[j]),sgn,components)
def sip(u,v,r,z):
    grad=connection=penalty=flux=0.
    for R,vol,s in volume(r,z):
        uv,ur,uz=evaluate(u,s);vv,vr,vz=evaluate(v,s)
        grad+=float(np.sum(vol*np.sum(ur*vr+uz*vz,axis=0)))
        connection+=float(np.sum(vol*uv[0]*vv[0]/R**2))
    for left,right,s,t,d,weight,eta,sgn,components in faces(r,z):
        ul,du=face_trace(u,left,s,d);vl,dv=face_trace(v,left,s,d)
        if right is not None:
            uu,duu=face_trace(u,right,t,d);vv,dvv=face_trace(v,right,t,d)
            ju=ul-uu;jv=vl-vv;fu=(du+duu)/2;fv=(dv+dvv)/2
        else:ju=ul;jv=vl;fu=sgn*du;fv=sgn*dv
        c=list(components)
        penalty+=float(weight*eta*np.dot(ju[c],jv[c]))
        flux-=float(weight*(np.dot(fu[c],jv[c])+np.dot(fv[c],ju[c])))
    total=grad+connection+penalty+flux
    assert all(math.isfinite(x) for x in (grad,connection,penalty,flux,total))
    return dict(value=total,gradient=grad,connection=connection,penalty=penalty,flux=flux)
def boundary_load(test,patch,r,z):
    ans=0.
    for left,right,s,t,d,weight,eta,sgn,components in faces(r,z):
        if right is not None:continue
        value,derivative=face_trace(test,left,s,d);g,_=face_trace(patch,left,s,d);c=list(components)
        ans+=float(weight*(-sgn*np.dot(derivative[c],g[c])+eta*np.dot(g[c],value[c])))
    return ans
def sip_controls(r,z,label):
    R=cells(np.broadcast_to(r[:,None],(len(r),len(z))))
    Z=cells(np.broadcast_to(z[None,:],(len(r),len(z))))
    ii=np.arange(len(r)-1)[:,None,None];jj=np.arange(len(z)-1)[None,:,None]
    u=np.stack((R*(1+ii+jj), (1+R)*(1+ii+2*jj+Z)))
    v=np.stack((R*(2+ii-jj)*(1+Z), (1+Z)*(2+2*ii+jj+R)))
    patch=np.stack((R,Z));uv=sip(u,v,r,z);vu=sip(v,u,r,z);uu=sip(u,u,r,z);vv=sip(v,v,r,z)
    pu=sip(patch,u,r,z);pv=sip(patch,v,r,z);lu=boundary_load(u,patch,r,z);lv=boundary_load(v,patch,r,z)
    controls=[check('SIP_symmetry',uv['value']-vu['value'],max(1.,abs(uv['value']),abs(vu['value'])))]
    for key,row in (('u',uu),('v',vv)):
        gap=row['value']-row['connection']-.5*(row['gradient']+row['penalty'])
        controls.append(check('SIP_coercivity_'+key,min(0.,gap),max(1.,abs(row['value']),row['gradient']+row['penalty'])))
    controls.extend([check('regular_cylindrical_patch_u',pu['value']-lu,max(1.,abs(pu['value']),abs(lu))),
                     check('regular_cylindrical_patch_v',pv['value']-lv,max(1.,abs(pv['value']),abs(lv))),
                     check('strong_axis_regular_test_space',max(float(np.max(abs(u[0,0,:,(0,2)]))),float(np.max(abs(v[0,0,:,(0,2)])))),1.)])
    return dict(label=label,r_kpc=r.tolist(),z_kpc=z.tolist(),bilinear_uv=uv,bilinear_vu=vu,
                quadratic_u=uu,quadratic_v=vv,patch_values=[pu,pv],matching_patch_loads=[lu,lv],
                ell_squared=ELL**2,controls=controls),dict(u=u,v=v,regular_patch=patch)
def main():
    global np
    assert not AUTHOR_DRAFT,'Unexecuted draft: root and independent static acceptance required'
    authenticate(PINS);pins=input_map();authenticate(pins);source=sha(__file__)
    assert not list(BASE.glob(STEM+'_*.json')) and not list(BASE.glob(STEM+'_*.npz')),'Existing outputs preserved'
    receipts={SPLIT+'_RECEIPT.json':closed(SPLIT+'_RECEIPT.json'),V3+'_RECEIPT.json':closed(V3+'_RECEIPT.json'),
              'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RECEIPT.json':closed('CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RECEIPT.json')}
    parent=read(SPLIT+'_RESULT.json');m=read(SPLIT+'_MANIFEST.json')
    assert receipts[SPLIT+'_RECEIPT.json']['source_sha256']==PINS['cross_u_nonzero_native_curvature_split_v001.py']
    assert receipts[SPLIT+'_RECEIPT.json']['result_sha256']==PINS[SPLIT+'_RESULT.json']
    assert receipts[SPLIT+'_RECEIPT.json']['manifest_sha256']==PINS[SPLIT+'_MANIFEST.json']
    assert receipts[V3+'_RECEIPT.json']['source_sha256']==PINS['cross_u_ngc3198_minres_recovery_v003.py']
    assert receipts[V3+'_RECEIPT.json']['result_sha256']==PINS[V3+'_RESULT.json']
    assert m['cases']==CASES and len(parent['cases'])==3 and len(parent['controls'])==48
    assert all(c['passed'] for c in parent['controls']) and len(parent['all_parent_cases'])==16
    np=importlib.import_module('numpy');nodes,weights=np.polynomial.legendre.leggauss(32)
    xi=(nodes+1)/2;w=weights*xi;assert np.all(w>0)
    manifest=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=source,input_sha256=pins,
          cases=CASES,directions_per_case=2,physics_changes=[],no_resume=True,no_newton=True,
          volume_quadrature='same_positive_2x2',penalty='8 max directional trace constant')
    mh=publish(STEM+'_MANIFEST.json',manifest);rows=[];sip_rows=[];sip_arrays={};actual_mesh=None
    for case in parent['cases']:
        name=case['case'];assert name in CASES and len(case['directions'])==2
        binding=m['state_bindings'][name]['terminal'];recname=binding['receipt_file']
        if recname not in receipts:receipts[recname]=closed(recname)
        receipt=receipts[recname]
        assert receipt['output_sha256'][binding['file']]==binding['sha256']
        assert receipt['output_sha256'][binding['commit_file']]==binding['commit_sha256']
        commit=pair(binding['file'],binding['commit_file'],binding['sha256'],binding['commit_sha256'])
        with np.load(BASE/binding['file'],allow_pickle=False) as a:
            x=a['state'].copy();identity=json.loads(str(a['identity']))
        assert commit['identity']==identity==case['parent_case']['identity']
        r=np.array(identity['r_kpc']);z=np.array(identity['z_kpc']);assert list(x.shape)==identity['grid_shape']==[65,len(r),len(z)]
        assert np.all(np.isfinite(x)) and np.all(np.diff(r)>0) and np.all(np.diff(z)>0) and r[0]==z[0]==0
        assert np.all(x[:,-1,:]==0) and np.all(x[:,:,-1]==0) and np.all(x[1::2,0,:]==0) and np.all(x[2::2,:,0]==0)
        if actual_mesh is None:actual_mesh=(r,z)
        else:assert np.array_equal(actual_mesh[0],r) and np.array_equal(actual_mesh[1],z)
        for index,row in enumerate(case['directions'],1):
            assert row['direction']==index and row['passed'] and row['status']=='DIAGNOSTIC_ONLY'
            seal=row['output'];cp=pair(seal['file'],seal['commit'],seal['sha256'],seal['commit_sha256'])
            assert cp['payload']=={k:v for k,v in row.items() if k!='output'}
            with np.load(BASE/seal['file'],allow_pickle=False) as a:
                p=a['scalar_direction'].copy();assert json.loads(str(a['metadata']))==cp['payload']
            assert p.shape==x.shape[1:] and np.all(np.isfinite(p)) and np.max(abs(p))>0
            assert np.all(p[-1,:]==0) and np.all(p[:,-1]==0)
            assert row['identity']['parent_identity']==identity and row['identity']['state_bindings']==m['state_bindings'][name]
            free,axis,answer=projection(x,p,r,z,xi,w)
            for key in ('K','weighted_local_inverse','Q_quartic'):
                answer['controls'].append(check('parent_'+key,answer[key]-row[key],max(1.,abs(row[key]),abs(answer[key]))))
            answer.update(case=name,direction=index,inherited_direction=row,state_binding=binding,
                          no_physical_boundary_solution=True,continuum_qualified=False,force_bias_qualified=False)
            out=save_arrays(name+f'_D{index}',dict(scalar_direction=p,broken_free=free,broken_axis_only=axis),answer)
            rows.append(dict(answer,output=out))
    for refine in (1,2):
        rr=np.linspace(0,2,4*refine+1);zz=np.linspace(0,1,4*refine+1)
        row,arrays=sip_controls(rr,zz,'manufactured_'+str(refine));sip_rows.append(row)
        sip_arrays.update({row['label']+'_'+k:v for k,v in arrays.items()})
    row,arrays=sip_controls(*actual_mesh,'actual_mesh');sip_rows.append(row)
    sip_arrays.update({row['label']+'_'+k:v for k,v in arrays.items()})
    ss=save_arrays('SIPG',sip_arrays,dict(cases=sip_rows,homogeneous_increment_coercivity=True,
                   matching_patch_wall_data_only=True,ell_terms_scaled=True,no_disk_boundary_solution=True))
    controls=[c for row in rows for c in row['controls']]+[c for row in sip_rows for c in row['controls']]
    assert len(rows)==6 and len(sip_rows)==3 and len(controls)==102
    authenticate(pins);assert sha(__file__)==source
    for rec in receipts.values():authenticate(rec['output_sha256'])
    for out in [r['output'] for r in rows]+[ss]:
        assert sha(BASE/out['file'])==out['sha256'] and sha(BASE/out['commit'])==out['commit_sha256']
    result=dict(status='CONTROL_PASS' if all(c['passed'] for c in controls) else 'CONTROL_FAILURES_RETAINED',
          manifest=manifest,rows=rows,sipg_controls=sip_rows,sipg_output=ss,controls=controls,
          inherited_nonzero_controls=parent['controls'],all_parent_cases=parent['all_parent_cases'],
          all_parent_flags_unchanged=True,observational_prediction=False,continuum_qualified=False,
          physical_state_qualified=False,force_bias_qualified=False,new_galaxy_solution=False)
    rh=publish(STEM+'_RESULT.json',result)
    report=encoded(dict(status=result['status'],control_count=len(controls),direction_count=len(rows),
                        SIPG_case_count=len(sip_rows),physical_flags=False,result_sha256=rh))
    rp=BASE/(STEM+'_REPORT.json')
    with rp.open('xb') as f:f.write(report);f.flush();os.fsync(f.fileno())
    rp.chmod(0o444);assert rp.read_bytes()==report
    outputs={p.name:sha(p) for p in BASE.glob(STEM+'_*') if p.is_file()}
    publish(STEM+'_RECEIPT.json',dict(owner='root',pid=os.getpid(),started=manifest['started'],closed=now(),
                  source_sha256=source,input_sha256=pins,manifest_sha256=mh,result_sha256=rh,output_sha256=outputs))
    print(STEM,result['status'],flush=True);return 0 if result['status']=='CONTROL_PASS' else 3
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true')
    assert ap.parse_args().root_owned;raise SystemExit(main())
