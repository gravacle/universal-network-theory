"""Saved matrices/source custody only: no cosmological distance calculation."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import base64,hashlib,io,json,math,zlib
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files={};manifests=set();occurrences=0
def member(p,digest=None):
    p=p.resolve(strict=True);p.relative_to(ROOT);got=sha(p)
    if digest is not None and digest!=got:raise AssertionError(('hash',str(p)))
    files[str(p.relative_to(ROOT))]=got;return p
def manifest(p):
    global occurrences
    p=member(p)
    if p in manifests:return
    manifests.add(p)
    for name,digest in json.loads(p.read_text())['files'].items():
        raw=Path(name);options=[raw] if raw.is_absolute() else [ROOT/raw,p.parent/raw]
        candidates={q.resolve() for q in options if q.is_file() and q.resolve().is_relative_to(ROOT)}
        if len(candidates)!=1:raise AssertionError(('path',name))
        q=member(candidates.pop(),digest);occurrences+=1
        if q.name.endswith('_FROZEN.json'):manifest(q)
def packet(name,fr):
    p=member(HERE/name);o=json.loads(p.read_text());f=member(HERE/fr);manifest(f)
    assert o['freeze_sha256']==sha(f)
    assert o['payload_sha256']==hashlib.sha256(enc(o['payload'])).hexdigest()
    return o['payload']
counts={};maxima={};failures=[]
def check(name,a,b,scale=1.,tol=3e-10):
    er=np.abs(np.asarray(a)-np.asarray(b))/np.maximum(np.abs(scale),1e-300);mx=float(np.max(er))
    counts[name]=counts.get(name,0)+int(er.size);maxima[name]=max(mx,maxima.get(name,0.))
    if not np.all(np.isfinite(er)) or mx>tol:failures.append(dict(check=name,error=mx,tolerance=tol))
def yes(name,x):check(name,int(bool(x)),1,tol=0.)
pl=packet('PANTHEON_FINITE_PRESSURE_V001_RESULTS.json','PANTHEON_FINITE_PRESSURE_V001_FROZEN.json')
inv=packet('BBN_SHARED_INVERSE_V001_RESULTS.json','BBN_SHARED_INVERSE_V001_FROZEN.json')
yes('status',pl['status']=='COMPLETE_ALL_335_SN_PROFILES' and not pl['failures'] and not pl['benchmark_only'])
def decode_raw(key):
    p=member(HERE/f'pantheon_inputs_v001/PANTHEON_{key.upper()}_V001_TRANSPORT.json');t=json.loads(p.read_text())
    assert t['commit']=='c447f0fea703fcd0fff57de5000947b5ca81286b'
    assert t['repository']=='PantheonPlusSH0ES/DataRelease' and t['key']==key
    if 'data_parts' in t:
        parts=[]
        for part in t['data_parts']:
            b=member(p.parent/part['file']).read_bytes()
            assert len(b)==part['characters']+1 and b.endswith(b'\n');parts.append(b[:-1])
        comp=base64.b64decode(b''.join(parts),validate=True)
    else:comp=base64.b64decode(t['data'],validate=True)
    dec=zlib.decompressobj();raw=dec.decompress(comp,t['bytes']+1)
    assert dec.eof and not dec.unused_data and not dec.unconsumed_tail and len(raw)==t['bytes']
    assert hashlib.sha256(raw).hexdigest()==t['sha256']
    yes('raw_metadata',all(pl['raw_source_metadata'][key][k]==t[k] for k in pl['raw_source_metadata'][key]))
    return raw
raw={k:decode_raw(k) for k in ('vector','covariance','readme','likelihood')}
table=np.genfromtxt(io.StringIO(raw['vector'].decode()),names=True,dtype=None,encoding='utf-8',autostrip=True)
mask=table['zHD']>.01;ix=np.flatnonzero(mask);data=pl['data'];n=len(ix)
yes('complete_mask',len(table)==1701 and n==1590 and data['total_rows']==1701 and data['selected_rows']==1590)
yes('mask_hash',hashlib.sha256(mask.astype('u1').tobytes()).hexdigest()==data['mask_sha256'])
yes('original_indices',ix.tolist()==data['original_row_indices'])
yes('identifiers',[str(x) for x in table['CID'][mask]]==data['CID'] and table['IDSURVEY'][mask].tolist()==data['IDSURVEY'])
for name in ('zHD','zHEL','m_b_corr'):check('data_'+name,data[name],table[name][mask],tol=0.)
y=np.asarray(data['m_b_corr']);head,body=raw['covariance'].decode().split('\n',1)
values=np.fromstring(body,sep=' ');assert int(head)==1701 and len(values)==1701**2
cov=values.reshape(1701,1701)[np.ix_(ix,ix)]
yes('covariance_submatrix_hash',hashlib.sha256(np.asarray(cov,dtype='<f8').tobytes()).hexdigest()==data['covariance_selected_f64_sha256'])
check('covariance_diagonal',np.diag(cov),data['covariance_diagonal'],tol=0.)
check('covariance_symmetry',cov,cov.T,tol=2e-12)
L=np.linalg.cholesky(cov);check('Cholesky_reconstruction',L@L.T,cov,tol=2e-12)
white_one=np.linalg.solve(L,np.ones(n));precision_one=np.linalg.solve(L.T,white_one)
den=float(white_one@white_one)
check('precision_one',cov@precision_one,np.ones(n),np.maximum(1,np.abs(cov)@np.abs(precision_one)))
packed_hashes={}
def unpack(key,shape):
    p=pl['arrays'][key];assert p['dtype']=='<f8' and p['order']=='C' and p['shape']==list(shape)
    dec=zlib.decompressobj();raw=dec.decompress(base64.b64decode(p['data'],validate=True),p['bytes']+1)
    assert dec.eof and not dec.unused_data and not dec.unconsumed_tail
    assert len(raw)==p['bytes']==8*math.prod(shape) and hashlib.sha256(raw).hexdigest()==p['sha256']
    packed_hashes[key]=dict(sha256=p['sha256'],bytes=len(raw),shape=list(shape))
    return np.frombuffer(raw,dtype='<f8').reshape(shape)
res=unpack('residual',(n,335));white=unpack('whitened_residual',(n,335))
dres=unpack('dust_residual',(n,5));dwhite=unpack('dust_whitened_residual',(n,5))
check('full_whitening',L@white,res,np.maximum(1,np.abs(L)@np.abs(white)))
check('dust_whitening',L@dwhite,dres,np.maximum(1,np.abs(L)@np.abs(dwhite)))
scores=np.sum(white**2,axis=0);dscores=np.sum(dwhite**2,axis=0)
derivatives=2*white_one@white;dderivatives=2*white_one@dwhite
points={p['point_id']:p for p in inv['table_points']};states={(s['point_id'],s['background_id'],s['spectrum_index']):s for s in inv['state_rows']}
backgrounds={b['background_id']:b for b in inv['backgrounds']};seen=set();columns=set();dustcols={}
yes('label_census',pl['source_label_mapping']==[{k:s[k] for k in ('point_id','background_id','spectrum_index','status')} for s in inv['state_rows']])
for d in pl['dust_controls']:
    j=d['array_column'];bi=d['background_id'];dustcols[bi]=j
    check('dust_score',d['score'],dscores[j],max(1,dscores[j]))
    check('dust_derivative',d['derivative'],dderivatives[j],max(1,2*np.sum(np.abs(white_one*dwhite[:,j]))))
    check('dust_curvature',d['curvature'],2*den,2*den)
for row in pl['records']:
    pi,bi,j=row['point_id'],row['background_id'],row['array_column'];point=points[pi];src=states[(pi,bi,0)]
    yes('unique_association',(pi,bi) not in seen and j not in columns);seen.add((pi,bi));columns.add(j)
    yes('row_status',row['status']=='COMPLETE_CONDITIONAL_SN_PROFILE')
    yes('roles',row['point_roles']==point['roles'] and row['inherited_local_BBN_rectangle']==point['prediction']['local_numerical_rectangle'])
    check('table_parameters',[row['omega_b'],row['Delta']],[point['omega_b'],point['Delta']],tol=0.)
    yes('state_status',row['source_statuses']==[states[(pi,bi,si)]['status'] for si in range(4)] and row['finite_gap']==(src['status']=='FINITE_HARD_STATE'))
    check('profile_score',row['score'],scores[j],max(1,scores[j]))
    scale=max(1,2*np.sum(np.abs(white_one*white[:,j])))
    check('profile_derivative',row['derivative'],derivatives[j],scale)
    check('stationarity',derivatives[j],0,scale,tol=2e-11)
    check('curvature',row['curvature'],2*den,2*den)
    # Reconstruct the saved shape; this is not independent distance verification.
    q=res[:,j]+y-row['magnitude_offset']
    offset=float(precision_one@(y-q)/np.sum(precision_one))
    check('reconstructed_offset',row['magnitude_offset'],offset,max(1,abs(offset)))
    check('absolute_magnitude_convention',row['implied_absolute_M_at_fixed_Hcal'],row['magnitude_offset']-25-5*math.log10(299792.458/row['Hcal_km_s_Mpc']))
    check('Hcal',row['Hcal_km_s_Mpc'],backgrounds[bi]['H0_km_s_Mpc'],tol=0.)
    dj=dustcols[bi]
    check('score_minus_dust',row['score_minus_same_background_dust'],row['score']-pl['dust_controls'][dj]['score'])
    if not row['finite_gap']:check('dust_limit_residual',res[:,j],dres[:,dj],np.maximum(1,np.abs(dres[:,dj])))
    ctrl=row['distance_controls'];yes('distance_census',ctrl['unique_redshifts']==len(np.unique(data['zHD'])))
    yes('distance_witnesses',[x['z'] for x in ctrl['witnesses']]==[float(x) for x in np.unique(data['zHD'])[[0,len(np.unique(data['zHD']))//2,-1]]])
    yes('refinement_census',[x['method'] for x in row['profile_refinement']]==['interval8','angle64'])
    for p in row['profile_refinement']:
        yes('saved_refinement_gates',abs(p['offset_minus_primary'])<=2e-9 and abs(p['score_minus_primary'])<=2e-6)
yes('complete_census',len(pl['records'])==335 and seen=={(p,b) for p in points for b in range(5)} and columns==set(range(335)))
def summary(rows):
    def span(key):return [min(r[key] for r in rows),max(r[key] for r in rows)]
    return dict(count=len(rows),finite=sum(r['finite_gap'] for r in rows),local_BBN_rectangle=sum(r['inherited_local_BBN_rectangle'] for r in rows),
                score=span('score'),score_minus_dust=span('score_minus_same_background_dust'),offset=span('magnitude_offset'),
                implied_M=span('implied_absolute_M_at_fixed_Hcal'),max_abs_residual_change_vs_dust=max(float(np.max(np.abs(res[:,r['array_column']]-dres[:,dustcols[r['background_id']]]))) for r in rows))
rows=pl['records'];groups={'all':summary(rows),'all_finite':summary([r for r in rows if r['finite_gap']])}
for tag,prefix in [('joint_any','joint:'),('central','central:')]+[(f'joint_{k}',f'joint:{k}:') for k in (1,2,3)]:
    for finite in (False,True):
        rr=[r for r in rows if any(x.startswith(prefix) for x in r['point_roles']) and (not finite or r['finite_gap'])]
        groups[tag+('_finite' if finite else '_including_limits')]=summary(rr)
bybg={str(bi):dict(dust_score=pl['dust_controls'][dustcols[bi]]['score'],joint_finite=summary([r for r in rows if r['background_id']==bi and r['finite_gap'] and any(x.startswith('joint:') for x in r['point_roles'])])) for bi in range(5)}
out=dict(status='PASS_SAVED_ARITHMETIC' if not failures else 'FAILED',scope='Custody, original data/covariance selection and saved residual linear algebra. No cosmological distance/root/quadrature/producer run; reconstructed q is not independent distance evidence.',
    checks=counts,maxima=maxima,failures=failures,total_checks=sum(counts.values()),files=files,
    unique_files=len(files),recursive_manifests=len(manifests),manifest_member_occurrences=occurrences,packed_arrays=packed_hashes,
    producer_checks=sum(pl['counts'].values()),producer_seconds=pl['seconds'],producer_peak_self_rss_bytes=pl['peak_self_rss_bytes'],
    total_original_rows=1701,selected_rows=1590,excluded_by_published_mask=111,histories=335,represented_labels=1340,summary_groups=groups,by_background=bybg)
print(json.dumps(out,indent=2,sort_keys=True,allow_nan=False))
