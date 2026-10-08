"""Guarded scalar ordinary-mean size diagnostic; no galaxy/source/volume replay."""
from pathlib import Path
import hashlib,json,math,os,sys,traceback
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_MEAN_BARYON_ORBITAL_SCALE_V001'
AUTHOR_DRAFT=True
PROTOCOL_SHA='5a084eef270b3476e3979f062964cb371b78f5751593a61f7b3715342f1ebfcf'
PINS={'CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002_RESULT.json':'ca1056f8798864eb7ae86c61812379ad8be46c4586560bf832f308fb79242158','CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002_RECEIPT.json':'00a630bd20e5ac06ce3dcc63dd4187c6d82b8ea73989274b0d105157cfee25b2','CROSS_U_OWNED_FLRW_ORDINARY_REFERENCE_BENCHMARK_V001_RESULT.json':'d279da68cbf50ebbeae62021cb39333cc986abda54f467df71eecc5791358502','CROSS_U_OWNED_FLRW_ORDINARY_REFERENCE_BENCHMARK_V001_RECEIPT.json':'5c21282863bbbfb129ce59fa0cf861d18c6f0fe77af16a62a2a3c3fd3fe1f243','CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_00000_REUSED_SOURCE_FOOTPRINTS.npz.COMMIT.json':'b8061d69f72302d923a45a4a8875cb687188eb3a4a9ebf13801c92eebbcd4dc7','cross_u_saved_full_metric_native_source_residual_v001.py':'23ff7ab909e60f4cd5ab96e12ea7cc1bc64e07821ebb11dd5cec28a9a02f5d68','CROSS_U_ONCE_COUNTED_ORDINARY_EXCESS_LABEL_REGISTRATION_V001.json':'6bf78e13e4099d7a13988237658a81ad90ea975ab0b3f18c0e4446206d411f05'}
TOL=2e-11;INPUTS={};OUTPUTS={};AVAILABLE={};CONTROLS=[]
FLAGS={k:False for k in ('source_added','configuration_updated','physical_embedding_admitted','normal_constraint_zero','orbital_or_observational_prediction','mean_overlap_explanation_adopted')}
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(n,x):
 p=BASE/n;b=(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);OUTPUTS[n]=sha(p);return OUTPUTS[n]
def recheck():
 for n,h in INPUTS.items():assert sha(BASE/n)==h,n
 for n,h in OUTPUTS.items():assert sha(BASE/n)==h,n
 assert all(v is False for v in FLAGS.values())
def capture(n,v):
 assert isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v),n
 AVAILABLE[n]=v;return v
def check(n,a,e,v):
 for key,x in (('actual',a),('expected',e),('envelope',v)):capture(n+'_'+key,x)
 assert v>=0;error=abs(a-e)/max(v,1e-30);row=dict(name=n,actual=a,expected=e,envelope=v,error=error,tolerance=TOL,passed=error<=TOL);CONTROLS.append(row);assert row['passed'],row

def packet():
 nr=json.loads((BASE/'CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002_RESULT.json').read_text());rc=json.loads((BASE/'CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002_RECEIPT.json').read_text());br=json.loads((BASE/'CROSS_U_OWNED_FLRW_ORDINARY_REFERENCE_BENCHMARK_V001_RESULT.json').read_text());bc=json.loads((BASE/'CROSS_U_OWNED_FLRW_ORDINARY_REFERENCE_BENCHMARK_V001_RECEIPT.json').read_text())
 for result,receipt,pid,name in ((nr,rc,51682,'CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002_RESULT.json'),(br,bc,54328,'CROSS_U_OWNED_FLRW_ORDINARY_REFERENCE_BENCHMARK_V001_RESULT.json')):
  assert receipt['status']=='CLOSED' and receipt['error_sha256'] is None and receipt['result_sha256']==PINS[name] and result['owner']==receipt['owner'] and result['owner']['pid']==pid and result['qualification']==receipt['qualification'] and all(v is False for v in result['qualification'].values())
 fixed=nr['checkpoints'][0]['metadata']['fixed'];assert fixed['Hunit']==67.49711988577813 and fixed['OB']==.04659233656879551 and fixed['rG']==.98989898989899 and fixed['eps']==1e-5
 register=json.loads((BASE/'CROSS_U_ONCE_COUNTED_ORDINARY_EXCESS_LABEL_REGISTRATION_V001.json').read_text());assert register['branch_adopted'] is False and register['ordinary_source_appended'] is False
 summary=json.loads((BASE/'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_00000_REUSED_SOURCE_FOOTPRINTS.npz.COMMIT.json').read_text())['metadata']['summaries']['EXP24'];Mgal=capture('copied_EXP24_total_rest_mass_Msun',summary['total_mass_Msun']);assert Mgal==34488290104.60389
 H=capture('Hstar_km_s_kpc',fixed['Hunit']/1000);OB=capture('OB',fixed['OB']);rg=capture('registered_rG',fixed['rG']);GN=capture('GN_kpc_km2_s2_Msun',4.30091e-6);gb=capture('Gbare_kpc_km2_s2_Msun',.99*GN);R=capture('R_kpc',44.08);v=capture('comparison_base_km_s',149.);KPC=capture('KPC_m',3.085677581491367e19)
 rho=capture('mean_baryon_Msun_kpc3',3*H*H*OB/(8*math.pi*gb*rg));mass=capture('mean_baryon_mass_inside_R_Msun',4*math.pi*rho*R**3/3);v2=capture('mean_baryon_localGN_speed_squared_km2_s2',H*H*OB*R*R/(2*.99*rg));bare_v2=capture('mean_baryon_bare_speed_squared_km2_s2',H*H*OB*R*R/(2*rg))
 check('physical_mass_localGN_normalization',mass,v2*R/GN,abs(mass)+abs(v2*R/GN));check('bare_vs_localGN_acceleration',bare_v2,.99*v2,abs(bare_v2)+abs(.99*v2))
 accel=capture('localGN_acceleration_m_s2',v2*1e6/(R*KPC));bare_accel=capture('bare_acceleration_m_s2',bare_v2*1e6/(R*KPC));speed=capture('quadrature_background_speed_km_s',math.sqrt(v2));shift=capture('positive_static_mass_shift_on_149_km_s',v2/(math.sqrt(v*v+v2)+v));check('stable_quadrature_shift',shift*(2*v+shift),v2,abs(shift*(2*v+shift))+abs(v2))
 capture('subtracting_same_positive_mass_speed_shift_on_149_km_s',-v2/(math.sqrt(v*v-v2)+v));capture('mean_label_radius_RL_kpc',(3*Mgal/(4*math.pi*rho))**(1/3));required=capture('speed_squared_needed_for_plus_16_5_km_s',16.5*(2*v+16.5));capture('required_uniform_density_over_frozen_mean_size_diagnostic',required/v2)
 return dict(status='SCALAR_MEAN_BARYON_ORBITAL_SIZE_DIAGNOSTIC',operands=AVAILABLE,controls=CONTROLS,qualification=FLAGS,interpretation='A positive static uniform-sphere size diagnostic only; background speed combines in quadrature. No mean is appended or subtracted from the original state, no halo/amplitude is fitted, and a FLRW metric/geodesic calculation is not replaced.',current_constraints='Known ordinary homogeneous inventory omission, not proven background overlap',old_43_curve='Scalar Q1 curve, not the current evolved full metric',label_radius_status='Conditional excess-label registrar length only; no finite pure FLRW junction or source continuation selected')
def main():
 assert AUTHOR_DRAFT is False and '--root-run' in sys.argv,'Root review/release required';assert not list(BASE.glob(STEM+'_*')),'Preserve existing output namespace';own=sha(__file__)
 INPUTS.update(PINS);INPUTS[Path(__file__).name]=own;INPUTS[STEM+'.md']=PROTOCOL_SHA;recheck();owner=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=own)
 try:
  result=packet();assert len(CONTROLS)==3 and all(c['passed'] for c in CONTROLS);result['owner']=owner;recheck();rh=write(STEM+'_RESULT.json',result);recheck();write(STEM+'_RECEIPT.json',dict(owner=owner,status='CLOSED',closed=now(),result_sha256=rh,error_sha256=None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));recheck();print(json.dumps(dict(status=result['status'],pid=os.getpid(),result_sha256=rh)),flush=True)
 except BaseException:
  eh=write(STEM+'_ERROR.json',dict(owner=owner,status='FAILED',operands=AVAILABLE,controls=CONTROLS,traceback=traceback.format_exc(),qualification=FLAGS));prior=BASE/(STEM+'_RECEIPT.json');write(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=owner,status='CLOSED_ERROR',closed=now(),error_sha256=eh,prior_receipt_sha256=sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));raise
if __name__=='__main__':main()
