"""0599 SRB_ROT C4T static-bound producer. MANIFEST OUTPUT; root post-seal only.
Manifest pins: result, reconstruction, EPS. Reconstructs the final rotation's
actual saved tail state with the existing pinned Codex2 replay; no solve.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import producer_guard_cx1v008 as G
G.admission(__file__)
import hashlib,importlib.util,io,json,math,bisect,zipfile,ast,struct
import numpy as np
import postseal_records_cx1v004 as C
RECON=Path(__file__).parent.parent/'calib_tail_readiness_cx2/certificates_per_point/reconstruction_cx2v003.py'
RECON_SHA='b8471197027bd2f0511966713656893860dfb22cba18e8d799ed2cc89b7c3a50'

@C.entry
def reconstruct(ref):
 if C.pin(RECON)['sha256']!=RECON_SHA:raise ValueError('RECONSTRUCTION_SOURCE_PIN')
 s=importlib.util.spec_from_file_location('cx1_srb_recon',RECON);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
 return m.replay_state(ref)

@C.entry
def rotation_arrays(ref):
 G.check_run_path(ref['path'],allow_registered=False)
 raw=Path(ref['path']).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=ref['sha256']:raise ValueError('ROTATION_ARRAY_PIN')
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  names=z.namelist()
  if len(set(names))!=len(names) or any(not n.endswith('.npy') for n in names):raise ValueError('NPZ_DUPLICATE_OR_EXTENSIONLESS')
  for info in z.infolist():
   data=z.read(info)
   if data[:6]!=b'\x93NUMPY' or data[6:8] not in (b'\x01\x00',b'\x02\x00',b'\x03\x00'):raise ValueError('NPY_MAGIC_VERSION')
   size=2 if data[6]==1 else 4;start=8+size;n=int.from_bytes(data[8:start],'little')
   header=ast.parse(data[start:start+n].decode('utf8' if data[6]==3 else 'latin1').strip(),mode='eval').body
   if not isinstance(header,ast.Dict):raise ValueError('NPY_HEADER_DICT')
   keys=[ast.literal_eval(k) for k in header.keys]
   if len(keys)!=3 or set(keys)!={'descr','fortran_order','shape'}:raise ValueError('NPY_HEADER_KEYS')
 with np.load(io.BytesIO(raw),allow_pickle=False) as z:
  return {k:z[k].copy() for k in ('radial_nodes_m','rotation_Omega_squared','full_fields_complex')}

@C.entry
def row_contract(arr,binding,ids,tau):
 R=np.asarray(arr['radial_nodes_m']);omega=np.asarray(arr['rotation_Omega_squared']);fields=np.asarray(arr['full_fields_complex'])
 if R.ndim!=1 or len(R)<2 or not np.all(np.isfinite(R)) or np.any(R<=0) or np.any(np.diff(R)<=0):raise ValueError('RADIAL_GRID')
 if omega.ndim!=2 or omega.shape[0]!=len(R) or not np.all(np.isfinite(omega)) or np.any(omega<=0):raise ValueError('POSITIVE_ROTATION_SQUARE')
 if fields.ndim!=4 or fields.shape[0]!=len(R) or fields.shape[2]!=omega.shape[1] or fields.shape[3]!=10 or not np.all(np.isfinite(fields)):raise ValueError('FULL_FIELDS_SHAPE')
 # Exactly the real lapse convention used by the saved rotation stage.
 if np.max(np.abs(fields[...,0].imag))>1e-12:raise ValueError('LAPSE_REALITY')
 Nmin=float(np.min(1+fields[...,0].real))
 if Nmin<=0:raise ValueError('POSITIVE_LAPSE')
 v=R*np.sqrt(np.min(omega,axis=1))
 rows=binding['query_rows']
 if [x['id'] for x in rows]!=ids or len(ids)!=12 or len(tau)!=12 or any(C.number(t)<=0 for t in tau):raise ValueError('REGISTERED_ROWS')
 indices=[]
 for row in rows:
  q=C.number(row['radius_m']);j=bisect.bisect_left(R,q)
  if q<R[0] or q>R[-1]:raise ValueError('ROW_OUTSIDE_RADIAL_SUPPORT')
  indices.append([j] if j<len(R) and R[j]==q else [j-1,j])
 physical=C.number(binding['physical_inclination_rad']);released=C.number(binding['released_inclination_rad'])
 factor=math.sin(physical)/math.sin(released)
 if not math.isfinite(factor) or factor<=0:raise ValueError('INCLINATION_FACTOR')
 return {'column_R_m':R.tolist(),'v_c_m_s':v.tolist(),'row_columns':indices,'N_min':Nmin,'tau_km_s':tau},factor

@C.entry
def envelope_certificate(eps,lo,hi):
 if eps.get('gate')!='EPS' or eps.get('verdict')!='CERTIFIED':raise ValueError('CERTIFIED_EPS_REQUIRED')
 env=eps['envelope_bound']
 if env.get('rule')!='A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS' or env.get('dominates_actual_every_shell') is not True or C.number(env['coverage_max_inverse_kpc'])<hi:raise ValueError('EPS_ENVELOPE_COVERAGE')
 shells=[];last=None
 for x in eps['shells']:
  a=C.number(x['lo_inverse_kpc']);b=C.number(x['hi_inverse_kpc']);v=C.number(x['eps_envelope'])
  if a>=b or v<0 or (last is not None and a!=last):raise ValueError('EPS_SHELL_GAP_OVERLAP')
  if v<C.number(x.get('eps_actual_set',x.get('eps',v))):raise ValueError('ENVELOPE_BELOW_ACTUAL')
  shells.append({'lo_inverse_kpc':a,'hi_inverse_kpc':b,'eps':v});last=b
 if not shells or shells[0]['lo_inverse_kpc']>lo or shells[-1]['hi_inverse_kpc']<hi:raise ValueError('EPS_SHELL_COVERAGE')
 return {'shells':shells}

@C.entry
def main():
 mp,out=sys.argv[1:];man=C.loads(Path(mp).read_bytes())
 if set(man)!={'result','reconstruction','EPS'}:raise ValueError('MANIFEST_FIELDS')
 m=C.comparator();result=C.read(man['result']);root=Path(man['result']['path']).resolve().parent
 if result.get('status')!='COMPLETED' or result['normalized_spec']['galaxy']!='DDO154':raise ValueError('COMPLETED_DDO154_REQUIRED')
 if result['driver_sha256']!=G.admission(__file__)['_verified_seal']['driver']['sha256']:raise ValueError('SEALED_DRIVER_REQUIRED')
 if C.read(C.pin(root/'finish.json'))['result_sha256']!=man['result']['sha256']:raise ValueError('RESULT_FINISH_PIN')
 last=result['passes'][-1];rot=Path(last['rotation']).resolve()
 if not rot.is_relative_to(root):raise ValueError('FINAL_ROTATION_OUTSIDE_RUN')
 finish_ref=C.pin(rot/'finish.json');finish=C.read(finish_ref)
 desc=C.read(man['reconstruction'])
 if desc.get('operation')!='rebuild' or desc.get('state_assertion')!=finish_ref or desc.get('state_field_path')!=['uv_tail','state_digest']:raise ValueError('FINAL_ROTATION_STATE_ASSERTION_REQUIRED')
 r,p=reconstruct(man['reconstruction'])
 cfg=r.config;actual=result['normalized_spec']['numerics']['uv_tail']
 if r.replay_scope!='PRODUCTION_P128_MS128' or r.lib.normalize_config(actual)['sha256']!=cfg['sha256']:raise ValueError('OWN_RUN_PRODUCTION_CONFIG')
 if cfg['lambda_scale']!=1 or cfg['source_rule']!='continuum_v001' or cfg['outer']['K_big_inverse_kpc']!=128 or result['normalized_spec']['numerics']['truncation'].get('shape')!='cube' or result['normalized_spec']['numerics']['composite_grid_spec']['breaks_inverse_kpc'][::len(result['normalized_spec']['numerics']['composite_grid_spec']['breaks_inverse_kpc'])-1]!=[-4,4]:raise ValueError('C4T_ONLY')
 if p.state.digest!=finish['uv_tail']['state_digest'] or finish['uv_tail']['production_admissible'] is not True:raise ValueError('STATE_DIGEST_OR_ADMISSION')
 if cfg['eps_certificate']!=man['EPS']:raise ValueError('ACTUAL_STATE_EPS_PIN')
 eps=C.read(man['EPS']);top=math.sqrt(2)*128;envelope=envelope_certificate(eps,4,top)
 ar={'path':finish['arrays_path'],'sha256':finish['arrays_sha256']}
 if Path(ar['path']).resolve()!=rot/'rotation_base_arrays.npz':raise ValueError('ROTATION_ARRAY_PATH')
 arr=rotation_arrays(ar)
 bp=m.PIN_ROW_RADII_BINDING
 binding=C.read({'path':bp[0],'sha256':bp[1]});pre=C.read({'path':m.PIN_PREREG_V005[0],'sha256':m.PIN_PREREG_V005[1]})
 ids,tm,_=m.registered_row_maps(pre);tau=[tm[x] for x in ids]
 rows,factor=row_contract(arr,binding,ids,tau);bound=r.lib.srb_rot(p.state,envelope,rows)
 values=[C.number(x)*factor for x in bound['bound_km_s']]
 rec={'schema':C.SCHEMA,'gate':'SRB_ROT','verdict':'PASS' if all(v<=t/10 for v,t in zip(values,tau)) else 'FAIL','producer':C.pin(__file__),'case':'C4T','c4t_result_sha256':man['result']['sha256'],'srb_rot_km_s':values,'inputs':man,'rotation_finish':finish_ref,'rotation_arrays':ar,'state_digest':p.state.digest,'state_replay_inputs':p.input_pins,'row_contract':rows,'inclination_factor':factor,'scope':'static channel only; envelope epsilon; per-column minimum positive speed across vertical nodes and global sampled N_min; necessary, not sufficient'}
 codes=m.g_SRB_ROT(rec,{'ids':ids,'tau':tm},lambda *a:None,[]);rec['gate_codes']=codes
 for ref in p.input_pins+[man['result'],man['EPS'],finish_ref,ar]:
  if C.pin(ref['path'])['sha256']!=ref['sha256']:raise ValueError('INPUT_CHANGED')
 G.check_run_path(out,allow_registered=False)
 with open(out,'x') as f:json.dump(G.stamp(rec,__file__),f,indent=1,allow_nan=False)
if __name__=='__main__':main()
