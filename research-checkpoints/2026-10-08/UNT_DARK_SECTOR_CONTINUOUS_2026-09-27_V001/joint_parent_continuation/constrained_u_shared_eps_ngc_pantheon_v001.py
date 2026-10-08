"""Root-owned fixed global epsilon shared observed-data comparison. No fit."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,base64,hashlib,json,math,os,time,zlib
import numpy as np
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001'
EPS=(1e-6,1e-5,1e-4,1e-3)
PINS={'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001.md': '9125291f442dfd3aebb63199de2c707e3f86ec3d02c236f87d606772f9a879ec', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002_RESULT.json': '8ccfba9bbded7faf0c2c3eb6250fb49f7d7f2951dbd71fc305f42cb81a3cd67b', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002_RECEIPT.json': '4ea9d4615ee248ffd0143cf862348bbc3648d080ac5e6d8cde3ba1dabdca2e3b', 'NGC3198_STATIONARY_LAPSE_SPAN_V001_RESULT.json': '7852e3eda3fd53c0619f7de506623fea3402949d9a97bfa433e82093e2123b37', 'NGC3198_STATIONARY_LAPSE_SPAN_V001_RECEIPT.json': 'b2f215e6ae66bb3f7343d7dde0d24d253b070899fec4bde7f18358068c726c42', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CONSTRAINED_U_SAVED_GALAXY_PHASE_LOADING_SCALE_V001_RESULT.json': '246a2c61a2467b19a23f20c3427368a7b293a857e842a3e2f298ae94af677a35', 'pantheon_inputs_v001/PANTHEON_COVARIANCE_V001_TRANSPORT.json': '58317db1be2c6591309a206f6ac6b54d564218f596f639457389eaaa5945a573', 'pantheon_inputs_v001/COVARIANCE_V001.part000.b64': '96e41bebcfe6217606c01656011d6e75d43076932706547fc27093071aa38898', 'pantheon_inputs_v001/COVARIANCE_V001.part001.b64': '341b243ea87a15275b570fa34c58d8296df7d78b5c9dd91e3db2c2775a0bd81e', 'pantheon_inputs_v001/COVARIANCE_V001.part002.b64': '8c73a43d20fe428423e4e84bbbe649d3037fcf8f53d00524dddd4955431b9236', 'pantheon_inputs_v001/COVARIANCE_V001.part003.b64': 'ab6f98037a4c3fe64c8448622efe42525e0d7abd6afd733e3a349dcfdb8850d9', 'pantheon_inputs_v001/COVARIANCE_V001.part004.b64': '63aadd0d4eac0e47138f9eec9602d75c63c3e425e34b4e830257367fdfab1e21', 'pantheon_inputs_v001/COVARIANCE_V001.part005.b64': '1342a15074048c948e3b7684024e1c8ae9153874b227be564f2dc42632e7119b', 'pantheon_inputs_v001/COVARIANCE_V001.part006.b64': '4ac5e9000ca304e96cc6745624997f6b8cb5ecc03f49c0a6c41ff656d0a9146f', 'pantheon_inputs_v001/COVARIANCE_V001.part007.b64': 'd224830e719c84927724ac3f938200d8f90112b4ab0d22dd8cadb753129692d9', 'pantheon_inputs_v001/COVARIANCE_V001.part008.b64': '938771ea6c8b4f6fb27bafdb7c17cfdc6099c6ee3e3617588aa52b63822e17b6', 'pantheon_inputs_v001/COVARIANCE_V001.part009.b64': '8392b21df6c52f72f95ea6eac31afb9d594c33ab5e7bd737b2f7167422474eb0', 'pantheon_inputs_v001/COVARIANCE_V001.part010.b64': 'dd0f98d0864dd0a6b3d824c883d5c988024b77e832ae44de09ee7fffafb93d88', 'pantheon_inputs_v001/COVARIANCE_V001.part011.b64': '18625dd0a97c0e326cd29d3340f1262777f55d89761631538072ec6fd3dd82db', 'pantheon_inputs_v001/COVARIANCE_V001.part012.b64': 'a0ce31a52f8b0f3357b8462534973785c082b0a17820826ee292f6d52e75fe4a', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EXECUTION_NOTE.md': 'ab41b98a6f4f8682c7a4a8d49054a3f9a39cf56d19e811da9148a7a505965edf'}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def write(name,v):
 p=BASE/name;raw=(json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 with p.open('xb') as f:f.write(raw)
 p.chmod(0o444);return sha(p)
def authenticate():
 for n,h in PINS.items():assert sha(BASE/n)==h,('changed input',n)
def background(a,f):
 a=np.asarray(a,float);ep=f['eps'];norm=1/ep-math.log1p(1/ep);d=f['d0']/a**3;target=.5*ep*norm*d;s=target.copy()
 for _ in range(12):
  q=np.sqrt(1+ep*s/(1+s));dq=ep/(2*q*(1+s)**2);s-=(s*q-target)/(q+s*dq)
 q=np.sqrt(1+ep*s/(1+s));pex=(np.log1p(s)-s/(1+s))/norm
 cs=ep*s/(2+(4+3*ep)*s+2*(1+ep)*s*s);A=1.5*f['OA']/f['rG'];w=A*q*d;rho=A*(1+q*d-pex)
 h=np.sqrt((2/3)*(1.5*f['OB']/f['rG']/a**3+1.5*f['OR']/f['rG']/a**4+rho))
 return dict(s=s,q=q,cs=cs,w=w,rho=rho,h=h,d=d,A=A,charge_error=np.abs(2*q*s/(ep*norm)/d-1))
def scalar_bg(f):
 return {k:float(v) for k,v in background(np.asarray(1.),f).items()}
def forward(L,b):
 b=np.asarray(b,float);out=np.empty_like(b)
 for i in range(len(L)):out[i]=(b[i]-L[i,:i]@out[:i])/L[i,i]
 return out
def dist(z,f,order):
 x,w=np.polynomial.legendre.leggauss(order);lo=np.r_[0.,z[:-1]];hi=z
 xx=lo[:,None]+(hi-lo)[:,None]*(x+1)/2
 return np.cumsum((hi-lo)*((1/background(1/(1+xx),f)['h'])@w)/2)
def covariance(parent):
 p=BASE/'pantheon_inputs_v001/PANTHEON_COVARIANCE_V001_TRANSPORT.json';pkt=json.loads(p.read_text());parts=[]
 assert pkt['bytes']==33284960 and pkt['key']=='covariance' and pkt['commit']=='c447f0fea703fcd0fff57de5000947b5ca81286b'
 for part in pkt['data_parts']:
  q=p.parent/part['file'];assert str(q.relative_to(BASE)) in PINS;raw=q.read_bytes();assert len(raw)==part['characters']+1 and raw.endswith(b'\n');parts.append(raw[:-1])
 raw=zlib.decompress(base64.b64decode(b''.join(parts),validate=True));assert len(raw)==pkt['bytes'] and hashlib.sha256(raw).hexdigest()==pkt['sha256']
 head,body=raw.decode().split('\n',1);assert int(head)==1701
 full=np.fromstring(body,sep=' ');assert full.size==1701**2
 ix=np.asarray(parent['data']['original_row_indices']);assert ix.shape==(1590,) and np.issubdtype(ix.dtype,np.integer) and np.all(np.diff(ix)>0) and ix[0]>=0 and ix[-1]<1701
 cov=full.reshape(1701,1701)[np.ix_(ix,ix)].copy()
 assert hashlib.sha256(np.asarray(cov,dtype='<f8').tobytes()).hexdigest()==parent['data']['covariance_selected_f64_sha256']
 assert cov.shape==(1590,1590) and np.all(np.isfinite(cov))
 return cov

def main():
 tick=time.monotonic();source=sha(__file__);authenticate()
 assert not [p for p in BASE.glob(STEM+'_*') if p.name!=STEM+'_EXECUTION_NOTE.md'],'Existing runtime prefix preserved'
 parent=json.loads((BASE/'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002_RESULT.json').read_text())
 receipt=json.loads((BASE/'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002_RECEIPT.json').read_text())
 assert receipt['result_sha256']==PINS['CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002_RESULT.json']
 assert parent['all_numerical_gates_passed'] and len(parent['numerical_gates'])==52 and all(t['passed'] for t in parent['numerical_gates'])
 ngc=json.loads((BASE/'NGC3198_STATIONARY_LAPSE_SPAN_V001_RESULT.json').read_text())
 nr=json.loads((BASE/'NGC3198_STATIONARY_LAPSE_SPAN_V001_RECEIPT.json').read_text());assert nr['result_sha256']==PINS['NGC3198_STATIONARY_LAPSE_SPAN_V001_RESULT.json']
 assert ngc['arithmetic_qualified'] and not ngc['readout']['galaxy_solution_qualified']
 fixed=parent['manifest']['fixed'];assert fixed['eps']==EPS[0] and fixed['rG']==.98/.99
 spans=[dict(inclination=a['inclination_deg'],speed_arm=a['speed_arm'],scheme=t['name'],span=t['span']) for a in ngc['readout']['arms'] for t in a['schemes']];assert len(spans)==18
 assert all(not t['conditional_stationary_band_compatible'] for a in ngc['readout']['arms'] for t in a['schemes'])
 controls=[]
 def check(name,error,tol):
  er=float(error);controls.append(dict(name=name,error=er,tolerance=tol,passed=math.isfinite(er) and er<=tol))
 manifest=dict(source_sha256=source,input_sha256=PINS,fixed_parent=fixed,eps_values=list(EPS),owner='root',pid=os.getpid(),started=now(),profiled_parameters=['common magnitude offset'],new_physical_fit_count=0,reference='Existing same-inventory eps->0 dust ablation',exposure=parent['manifest']['exposure'],galaxy_scope='Conditional charged stationary outer-band necessity only')
 mh=write(STEM+'_MANIFEST.json',manifest);outputs={STEM+'_MANIFEST.json':mh}
 cov=covariance(parent);check('covariance_symmetry',np.max(abs(cov-cov.T)),2e-12);L=np.linalg.cholesky(cov);check('Cholesky_reconstruction',np.max(abs(L@L.T-cov)),2e-12)
 data=parent['data'];zh=np.asarray(data['zHD']);zhel=np.asarray(data['zHEL']);Y=np.asarray(data['m_b_corr'])
 assert all(v.shape==(1590,) and np.all(np.isfinite(v)) for v in (zh,zhel,Y)) and np.all(zh>.01) and np.all(1+zhel>0)
 ones=forward(L,np.ones(len(Y)));den=ones@ones
 for row in parent['rows']:
  r=row['profile_rows'][0];w=np.asarray(r['whitened_residual']);res=np.asarray(r['residual'])
  check('baseline_'+row['shape']+'_whitened_reconstruction',np.max(abs(L@w-res)),2e-10);check('baseline_'+row['shape']+'_score',abs(w@w-r['score']),2e-8)
 z,inv=np.unique(zh,return_inverse=True);reference=parent['rows'][1];assert reference['shape']=='DUST_LIMIT';rows=[]
 for ep in EPS:
  f=dict(fixed,eps=ep);bg=scalar_bg(f);width=.5*math.log1p(ep/(1+(1+ep)*bg['s']))
  armrows=[dict(a,charged_width=width,span_over_width=a['span']/width,signed_width_minus_span=width-a['span'],compatible=bool(a['span']<width)) for a in spans]
  aa=1/(1+np.r_[0.,z]);bgs=background(aa,f)
  check('charge_'+str(ep),np.max(bgs['charge_error']),2e-12)
  check('energy_lower_'+str(ep),max(0.,float(np.max((bgs['A']*(1+bgs['d'])-bgs['rho'])/np.maximum(1,bgs['rho'])))),2e-12)
  check('energy_upper_'+str(ep),max(0.,float(np.max((bgs['rho']-bgs['A']*(1+math.sqrt(1+ep)*bgs['d']))/np.maximum(1,bgs['rho'])))),2e-12)
  assert np.all(np.isfinite(bgs['h'])) and np.all(bgs['cs']>0) and np.all(bgs['s']>0) and np.all(bgs['q']>=1) and np.all(bgs['q']<math.sqrt(1+ep))
  if ep==EPS[0]:
   payload=dict(parent['rows'][0]);assert payload['shape']=='CURRENT';payload['baseline_copied_exactly']=True
  else:
   ds=np.column_stack([dist(z,f,n) for n in (16,32)]);check('distance_'+str(ep),np.max(abs(ds[:,0]-ds[:,1])/ds[:,1]),2e-10)
   q=5*np.log10((1+zhel[:,None])*ds[inv]);white=forward(L,Y[:,None]-q);offset=(ones@white)/den
   residual=q+offset[None,:]-Y[:,None];wr=forward(L,residual);score=np.sum(wr*wr,axis=0)
   check('score_refinement_'+str(ep),abs(score[0]-score[1]),2e-6);check('offset_refinement_'+str(ep),abs(offset[0]-offset[1]),2e-9)
   check('profile_stationarity_'+str(ep),np.max(abs(ones@wr))/max(1.,float(np.sum(abs(ones[:,None]*wr)))),2e-11)
   payload=dict(unique_zHD=z.tolist(),dimensionless_distance_arms=ds.tolist(),profile_rows=[dict(arm='GAUSS'+str(n),score=float(score[i]),magnitude_offset=float(offset[i]),magnitude_shape=q[:,i].tolist(),residual=residual[:,i].tolist(),whitened_residual=wr[:,i].tolist()) for i,n in enumerate((16,32))],baseline_copied_exactly=False)
  ell=2.2514615723180782e-8;C=1.98;kJ2=2*bg['w']/(C*bg['cs']);qc2=(kJ2+math.sqrt(kJ2*kJ2+4*kJ2/ell**2))/2
  rows.append(dict(eps=ep,background=bg,H_today=f['Hunit']*bg['h'],sound_km_s=299792.458*math.sqrt(bg['cs']),Dphi_over_2M2Hstar2=bg['w']/bg['cs'],charged_width=width,all18=armrows,compatible_count=sum(a['compatible'] for a in armrows),qcrit_inverse_kpc=299792.458/f['Hunit']/math.sqrt(qc2)*1000,pantheon=payload,score_minus_reference=payload['profile_rows'][0]['score']-reference['profile_rows'][0]['score']))
  authenticate();assert sha(__file__)==source
  n=STEM+'_EPS_'+format(ep,'.0e').replace('-','m')+'_CP.json';h=write(n,rows[-1]);outputs[n]=h;print('SHARED_EPS',ep,'COMPLETE',flush=True)
 check('charged_width_increases',max(0.,max(rows[i]['charged_width']-rows[i+1]['charged_width'] for i in range(3))),0.)
 assert len(controls)==31,'Full prospective numerical-control census'
 status='NUMERICAL_PASS' if all(t['passed'] for t in controls) else 'NUMERICAL_FAILED'
 result=dict(status=status,manifest=manifest,rows=rows,reference_copied_exactly=reference,ngc_ancestral_flags=ngc['readout'],prior_numerical_gates_copied=parent['numerical_gates'],controls=controls,physical_flags=dict(nonlinear_disk_predicted=False,mature_state_qualified=False,new_eps_adopted=False,joint_superiority_qualified=False,native_origin_qualified=False),elapsed_seconds=time.monotonic()-tick)
 authenticate();assert sha(__file__)==source;rh=write(STEM+'_RESULT.json',result);outputs[STEM+'_RESULT.json']=rh
 report=['# Shared global epsilon measured-data comparison V001','',status,'','All other physical calibration fixed; one magnitude offset per fixed supernova curve. Charged NGC stationary condition is necessary only. Existing reference is an ablation, not fitted LCDM.','', '| eps | NGC compatible/18 | charged width | Htoday | sound km/s | SNe score | score minus dust |','|---|---:|---:|---:|---:|---:|---:|']
 for r in rows:report.append(f"| {r['eps']:.0e} | {r['compatible_count']} | {r['charged_width']:.10g} | {r['H_today']:.10g} | {r['sound_km_s']:.10g} | {r['pantheon']['profile_rows'][0]['score']:.12g} | {r['score_minus_reference']:.10g} |")
 report+=['','No parameter value adopted. No disk force prediction, native-origin or superiority qualification. All outcomes, saved ancestor failures and per-measurement residuals retained.']
 rp=BASE/(STEM+'_REPORT.md')
 with rp.open('x') as f:f.write('\n'.join(report)+'\n')
 rp.chmod(0o444);outputs[rp.name]=sha(rp);authenticate()
 receipt=dict(status=status,owner='root',pid=os.getpid(),started=manifest['started'],closed=now(),source_sha256=source,manifest_sha256=mh,result_sha256=rh,output_sha256=outputs)
 write(STEM+'_RECEIPT.json',receipt);print(status,rh,flush=True);return 0 if status=='NUMERICAL_PASS' else 3

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');assert ap.parse_args().root_owned
 raise SystemExit(main())
