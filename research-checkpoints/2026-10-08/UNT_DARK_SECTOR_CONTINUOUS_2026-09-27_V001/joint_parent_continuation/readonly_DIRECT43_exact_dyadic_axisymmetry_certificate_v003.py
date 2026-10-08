"""HELD exact represented-operand DIRECT43 compatibility/gauge certificate.
Root alone binds and runs after closed87 custody. No producer/action/rounding
kernel replay, zero projection, stationarity or circle/velocity admission.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import ast,hashlib,itertools,json,math,os,struct,sys,traceback,zipfile
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
EXPECTED_SOURCE=('direct43_original_baseline_preparation_v003.py','68fff180edacd39e1d88c828201f6ea6c5018eaec78bbdd2e4bb90f4528ae336')
SOURCE=(None,None)
RESULT=(None,None,'DIRECT43_ORIGINAL_BASELINE_FIELDS_PREPARED_UNQUALIFIED')
RECEIPT=(None,None,'CLOSED')
CUSTODY=(None,None,'READONLY_NATURAL_CLOSED_DIRECT43_BASELINE_SUCCESS_SEALS_VERIFIED')
CONTRACT=('OBSERVER_DIRECT43_AXISYMMETRY_DEFECT_SOURCE_CONTRACT_V001.json','f1188bac9e9bdbba57aacc4007be8b20ee79ed72f2d319524fe6de25302c0aba')
PROTOCOL='DIRECT43_EXACT_DYADIC_AXISYMMETRY_CERTIFICATE_V003.md'
PROTOCOL_SHA=None
OUTPUT_FILE=None
STEM='DIRECT43_ORIGINAL_BASELINE_PREPARATION_V003'
np=None
VERIFIED={};STATS={}
RAW_FIELDS={'source_g':(4,4),'source_hi':(4,4),'seed_dg_operand':(4,4,4),'seed_Gamma_operand':(4,4,4),'owned_increment_dg':(4,4,4),'owned_Gamma_increment':(4,4,4),'owned_Gamma':(4,4,4),'chart_dg':(4,4,4),'chart_dhi':(4,4,4),'source_N':(),'source_beta':(3,),'genuine_N_jets':(4,),'genuine_beta_jets':(4,3)}
PAIR_FIELDS={'g':(4,4),'dg':(4,4,4),'N':(),'beta':(3,),'N_jets':(4,),'beta_jets':(4,3)}
PINS={'author_fragment_direct43_owned_baseline_field_law_v004.py':'99ea2904f4b699764f0e186b9cb7d05db691bb5dc91a5019ee7199bb850ce7b1','cross_u_whole_slice_cauchy_data_v002.py':'6d5a994584d1967965c72e9b0568e67c14610078832c9b40f4cbd04336b19df7','cross_u_whole_slice_q1_adm_residual_v001.py':'c66c86c06d16c22209b95bde8e18a9bba4d336674da5389c777408534d205e8a'}

def verified(name,digest):
 p=BASE/name;st=p.stat();key=str(p.resolve());identity=(st.st_ino,st.st_size,st.st_mtime_ns,st.st_mode)
 assert not st.st_mode&0o222 and st.st_size>0 and isinstance(digest,str) and len(digest)==64
 if key not in VERIFIED:
  h=hashlib.sha256()
  with p.open('rb') as f:
   for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
  assert h.hexdigest()==digest,name;VERIFIED[key]=digest;STATS[key]=identity
 assert VERIFIED[key]==digest and STATS[key]==identity
 end=p.stat();assert identity==(end.st_ino,end.st_size,end.st_mtime_ns,end.st_mode);return p

def metadata(name,digest):
 p=verified(name,digest);assert p.stat().st_size<=16*1024*1024;return json.loads(p.read_text())

def thin(ref):return {n:ref[n] for n in ('file','sha256','commit_file','commit_sha256')}

def member(z,name,schema):
 info=z.getinfo(name+'.npy')
 with z.open(info) as f:
  version=np.lib.format.read_magic(f);assert version in ((1,0),(2,0))
  shape,order,dtype=(np.lib.format.read_array_header_1_0(f) if version==(1,0) else np.lib.format.read_array_header_2_0(f));position=f.tell()
  assert list(shape)==schema['shape'] and str(dtype)==schema['dtype'] and not dtype.hasobject and schema['finite'] is True
  payload=f.read();assert len(payload)==math.prod(shape)*dtype.itemsize and position+len(payload)==info.file_size
 if dtype.kind=='b':assert shape==() and dtype.itemsize==1 and payload in (b'\x00',b'\x01');return bool(payload[0])
 assert dtype.kind=='f' and dtype.itemsize==8
 big=dtype.byteorder=='>' or dtype.byteorder=='=' and sys.byteorder=='big';values=struct.unpack(('>' if big else '<')+'d'*math.prod(shape),payload)
 assert all(math.isfinite(v) for v in values)
 strides=[];stride=1
 for axis in (range(len(shape)) if order else reversed(range(len(shape)))):
  strides.append((axis,stride));stride*=shape[axis]
 strides=dict(strides);indices=itertools.product(*(range(n) for n in shape));logical=[values[sum(i*strides[a] for a,i in enumerate(index))] for index in indices]
 return dict(shape=tuple(shape),values=[F.from_float(v) for v in logical],hex_words=[v.hex() for v in logical],member_sha256=hashlib.sha256(payload).hexdigest())

def at(a,*index):
 shape=a['shape'];assert len(index)==len(shape);offset=0
 for n,i in zip(shape,index):assert 0<=i<n;offset=offset*n+i
 return a['values'][offset]

def read_event(ref,index,owner,receipt):
 q=metadata(ref['commit_file'],ref['commit_sha256']);assert set(q)=={'file','sha256','metadata'} and q['file']==ref['file'] and q['sha256']==ref['sha256']
 for f,h in (('file','sha256'),('commit_file','commit_sha256')):assert receipt['output_sha256'][ref[f]]==ref[h]
 md=q['metadata'];assert md['owner']==owner and md['index']==index and md['failed'] is False and md['physical_adoption'] is False and all(v is False for v in md['qualification'].values())
 assert type(md['axisymmetric_gauge_phi_exact_zero']) is bool and md['stationary_seed_adopted_as_current'] is False
 p=verified(ref['file'],ref['sha256']);prefix='DIRECT_reference_%02d_'%index;fields={}
 with zipfile.ZipFile(p) as z:
  names=z.namelist();assert len(names)==len(set(names)) and set(names)=={n+'.npy' for n in md['schema']}|{'metadata_json.npy'}
  for n,shape in RAW_FIELDS.items():
   key=prefix+n;assert md['schema'][key]==dict(shape=[1]+list(shape),dtype='float64',finite=True)
   a=member(z,key,md['schema'][key]);a['shape']=shape;fields[n]=a
  for n,shape in PAIR_FIELDS.items():
   for w in ('hi','lo'):
    key=n+'_'+w;assert md['schema'][key]==dict(shape=list(shape),dtype='float64',finite=True);fields[key]=member(z,key,md['schema'][key])
  flag=member(z,'axisymmetric_gauge_phi_exact_zero',md['schema']['axisymmetric_gauge_phi_exact_zero']);assert flag==md['axisymmetric_gauge_phi_exact_zero']
  with z.open('metadata_json.npy') as f:
   v=np.lib.format.read_magic(f);assert v in ((1,0),(2,0));shape,order,dtype=(np.lib.format.read_array_header_1_0(f) if v==(1,0) else np.lib.format.read_array_header_2_0(f))
   assert shape==() and not order and dtype.kind=='U' and dtype.itemsize<=16*1024*1024;raw=f.read();assert len(raw)==dtype.itemsize
   big=dtype.byteorder=='>' or dtype.byteorder=='=' and sys.byteorder=='big';assert json.loads(raw.decode('utf-32-be' if big else 'utf-32-le').rstrip('\x00'))==md
 for alias,source in {'g':'source_g','dg':'chart_dg','N':'source_N','beta':'source_beta','N_jets':'genuine_N_jets','beta_jets':'genuine_beta_jets'}.items():
  assert fields[alias+'_hi']['hex_words']==fields[source]['hex_words'] and all(v==0 for v in fields[alias+'_lo']['values'])
 assert flag==all(at(fields['N_jets_'+w],3)==0 and all(at(fields['beta_jets_'+w],3,i)==0 for i in range(3)) for w in ('hi','lo'))
 return fields,md

def exact_certificate(a,md,ref):
 g,I,Cs,Co,Gs,Go,G,D,Dhi=(a[n] for n in ('source_g','source_hi','seed_dg_operand','owned_increment_dg','seed_Gamma_operand','owned_Gamma_increment','owned_Gamma','chart_dg','chart_dhi'))
 for A in (g,I):assert all(at(A,i,j)==at(A,j,i) for i in range(4) for j in range(4))
 for C in (Cs,Co,D):assert all(at(C,k,i,j)==at(C,k,j,i) for k in range(4) for i in range(4) for j in range(4))
 assert all(at(C,3,i,j)==0 for C in (Cs,Co) for i in range(4) for j in range(4))
 T=lambda C,l,m:at(C,3,m,l)+at(C,m,3,l)-at(C,l,3,m)
 U=lambda C,l,m:abs(at(C,3,m,l))+abs(at(C,m,3,l))+abs(at(C,l,3,m))
 M=[[sum(at(g,k,n)*at(I,k,l) for k in range(4)) for l in range(4)] for n in range(4)]
 half=F(1,2);es=[[at(Gs,k,3,m)-half*sum(at(I,k,l)*T(Cs,l,m) for l in range(4)) for m in range(4)] for k in range(4)]
 eo=[[at(Go,k,3,m)-half*sum(at(I,k,l)*T(Co,l,m) for l in range(4)) for m in range(4)] for k in range(4)]
 ez=[[at(G,k,3,m)-at(Gs,k,3,m)-at(Go,k,3,m) for m in range(4)] for k in range(4)]
 eg=[[es[k][m]+eo[k][m]+ez[k][m] for m in range(4)] for k in range(4)]
 compatibility=[];recover=[];bd=[];actual=[]
 for m in range(4):
  c_row=[];r_row=[];b_row=[];d_row=[]
  for n in range(4):
   c=half*sum((M[n][l]-int(n==l))*(T(Cs,l,m)+T(Co,l,m))+(M[m][l]-int(m==l))*(T(Cs,l,n)+T(Co,l,n)) for l in range(4))
   e=sum(eg[l][m]*at(g,l,n)+eg[l][n]*at(g,l,m) for l in range(4));r=at(D,3,m,n)-sum(at(G,l,3,m)*at(g,l,n)+at(G,l,3,n)*at(g,l,m) for l in range(4))
   assert at(D,3,m,n)==c+e+r
   b=half*sum(abs(M[n][l]-int(n==l))*(U(Cs,l,m)+U(Co,l,m))+abs(M[m][l]-int(m==l))*(U(Cs,l,n)+U(Co,l,n)) for l in range(4))+sum((abs(es[l][m])+abs(eo[l][m])+abs(ez[l][m]))*abs(at(g,l,n))+(abs(es[l][n])+abs(eo[l][n])+abs(ez[l][n]))*abs(at(g,l,m)) for l in range(4))+abs(r)
   assert abs(at(D,3,m,n))<=b;c_row.append(c);r_row.append(r);b_row.append(b);d_row.append(at(D,3,m,n))
  compatibility.append(c_row);recover.append(r_row);bd.append(b_row);actual.append(d_row)
 ei=[[at(Dhi,3,i,j)+sum(at(I,i,k)*at(D,3,k,l)*at(I,l,j) for k in range(4) for l in range(4)) for j in range(4)] for i in range(4)]
 bi=[[sum(abs(at(I,i,k))*bd[k][l]*abs(at(I,l,j)) for k in range(4) for l in range(4))+abs(ei[i][j]) for j in range(4)] for i in range(4)]
 N=at(a['source_N']);assert N>0;na=at(a['genuine_N_jets'],3);en=na-half*N**3*at(Dhi,3,0,0);bn=half*abs(N)**3*bi[0][0]+abs(en)
 eb=[at(a['genuine_beta_jets'],3,i)-(2*N*na*at(I,0,i+1)+N**2*at(Dhi,3,0,i+1)) for i in range(3)]
 bb=[2*abs(N)*bn*abs(at(I,0,i+1))+N**2*bi[0][i+1]+abs(eb[i]) for i in range(3)]
 assert abs(na)<=bn and all(abs(at(a['genuine_beta_jets'],3,i))<=bb[i] for i in range(3))
 return dict(index=md['index'],R=md['R'],reference_event=thin(ref),raw_exact_zero_flag=md['axisymmetric_gauge_phi_exact_zero'],input_phi_exact_zero=True,paired_alias_word_ties=True,source_member_payload_sha256={n:q['member_sha256'] for n,q in a.items()},raw_inverse_compatibility=[[M[n][l]-int(n==l) for l in range(4)] for n in range(4)],seed_connection_defect=es,owned_connection_defect=eo,connection_sum_defect=ez,recovery_defect_phi=recover,compatibility_term_phi=compatibility,actual_chart_dg_phi=actual,chart_dg_phi_uncancelled_enclosure=bd,inverse_jet_defect_phi=ei,inverse_jet_phi_enclosure=bi,lapse_jet_defect_phi=en,lapse_jet_phi_enclosure=bn,shift_jet_defect_phi=eb,shift_jet_phi_enclosure=bb,actual_lapse_phi=na,actual_shift_phi=[at(a['genuine_beta_jets'],3,i) for i in range(3)],raw_gauge_phi_words_hex=dict(N=[a['N_jets_'+w]['hex_words'][3] for w in ('hi','lo')],beta=[a['beta_jets_'+w]['hex_words'][9:12] for w in ('hi','lo')]),raw_chart_phi_words_hex=[a['dg_'+w]['hex_words'][48:64] for w in ('hi','lo')],genuine_time_words_hex=dict(N=a['genuine_N_jets']['hex_words'][0],beta=a['genuine_beta_jets']['hex_words'][:3]),exact_dyadic_identity_verified=True,observed_arithmetic_defects_included_not_apriori_roundoff_theorem=True,axisymmetry_precision_admitted=False)

def serial(q):
 if isinstance(q,F):return dict(numerator=str(q.numerator),denominator=str(q.denominator))
 if isinstance(q,dict):return {n:serial(v) for n,v in q.items()}
 if isinstance(q,(list,tuple)):return [serial(v) for v in q]
 return q

def publish(name,value):
 blob=(json.dumps(serial(value),indent=2,sort_keys=True)+'\n').encode();path=BASE/name
 with path.open('xb') as f:f.write(blob);f.flush();os.fsync(f.fileno())
 path.chmod(0o444);return dict(file=path.name,sha256=hashlib.sha256(blob).hexdigest(),bytes=len(blob))

def main():
 global np
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and SOURCE==EXPECTED_SOURCE and all(v is not None for q in (SOURCE,RESULT,RECEIPT,CUSTODY) for v in q) and PROTOCOL_SHA is not None
 assert isinstance(OUTPUT_FILE,str) and OUTPUT_FILE.endswith('.json') and '/' not in OUTPUT_FILE and not (BASE/OUTPUT_FILE).exists()
 assert not list(BASE.glob(OUTPUT_FILE[:-5]+'_*.json')),'Existing exact-dyadic event/error namespace must be preserved'
 verified(Path(__file__).name,hashlib.sha256(Path(__file__).read_bytes()).hexdigest());verified(PROTOCOL,PROTOCOL_SHA);contract=metadata(*CONTRACT)
 for n,h in PINS.items():verified(n,h);assert contract['source_pins'][n]==h
 verified(*SOURCE);result=metadata(*RESULT[:2]);rc=metadata(*RECEIPT[:2]);proof=metadata(*CUSTODY[:2]);owner=rc['owner']
 assert owner==result['owner']==proof['owner'] and owner['pid']==1071 and owner['source_sha256']==SOURCE[1]
 assert result['status']==RESULT[2] and rc['status']==RECEIPT[2] and rc['result_sha256']==RESULT[1] and rc['error_sha256'] is None
 assert proof['status']==CUSTODY[2] and proof['source_sha256']==SOURCE[1] and proof['result_sha256']==RESULT[1] and proof['receipt_sha256']==RECEIPT[1]
 assert proof['naturally_closed'] is True and proof['exit_code']==0 and all(proof[n] is True for n in ('all_input_seals_verified','all_output_seals_verified','all_success_role_seals_verified','full87_preparation_completed'))
 assert proof['science_role_count']==proof['total_records']==87 and proof['input_count']==len(rc['input_sha256'])==41 and proof['output_count']==len(rc['output_sha256'])==177
 assert result['qualification']==rc['qualification']==proof['qualification'] and all(v is False for v in rc['qualification'].values()) and result['controls']==proof['controls']==[]
 events=result['case']['events'];assert events==proof['events'] and len(events)==43 and len(result['checkpoints'])==len(proof['records'])==87
 import numpy as numpy
 np=numpy;rows=[];completed=[];context={};analysis_owner=dict(owner='root',pid=os.getpid(),started=datetime.now(timezone.utc).isoformat(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 try:
  for i,event in enumerate(events):
   ref=event['reference_event'];context=dict(index=i,reference_event=ref,R=event['R'])
   assert event['index']==i and ref==thin(result['checkpoints'][2*i+1])==thin(proof['records'][2*i+1]) and ref['file']==STEM+'_%05d_REFERENCE_EVENT.npz'%(2*i+1)
   a,md=read_event(ref,i,owner,rc);assert md['R']==event['R'];row=exact_certificate(a,md,ref)
   completed.append(publish(OUTPUT_FILE[:-5]+'_%02d_EVENT.json'%i,dict(analysis_owner=analysis_owner,baseline_owner=owner,source_contract=CONTRACT,certificate=row,physical_or_velocity_adoption=False)));rows.append(row)
  assert [q['raw_exact_zero_flag'] for q in rows]==proof['axisymmetric_gauge_phi_exact_zero_metadata']
 except BaseException:
  publish(OUTPUT_FILE[:-5]+'_ERROR.json',dict(status='FAILED_EXACT_DYADIC_CERTIFICATE_PREFIX_PRESERVED',analysis_owner=analysis_owner,baseline_owner=owner,context=context,completed_event_certificates=completed,selected_input_sha256=VERIFIED,traceback=traceback.format_exc(),source_contract=CONTRACT,physical_or_velocity_adoption=False));raise
 for name,identity in STATS.items():
  st=Path(name).stat();assert identity==(st.st_ino,st.st_size,st.st_mtime_ns,st.st_mode)
 out=dict(status='CLOSED_DIRECT43_EXACT_DYADIC_COMPATIBILITY_AND_GAUGE_DEFECTS_MEASURED',measured_at=datetime.now(timezone.utc).isoformat(),analysis_owner=analysis_owner,completed_event_certificates=completed,baseline_owner=owner,baseline_terminal=(SOURCE,RESULT,RECEIPT,CUSTODY),source_contract=CONTRACT,source_pins=PINS,event_count=43,rows=rows,input_sha256=VERIFIED,stable_stats=STATS,all_selected_byte_seals_verified=True,all_exact_dyadic_defect_identities_verified=True,raw_flags_and_words_preserved=True,source_phi_input_exact_zero=True,apriori_roundoff_model_or_inverse_conditioning_qualified=False,geodesic_accuracy_budget_supplied=False,axisymmetry_precision_admitted=False,exact132_axisymmetry_guard_promoted=False,physical_or_velocity_adoption=False,original_bodies_or_controls_replayed=False,selected_numeric_members_decoded=True,numeric_scope='Exact rational reference contractions of saved finite binary64 operands only; explicit observed stage defects remain in all bounds. No floating source kernel or physical geodesic is evaluated.',qualification=rc['qualification'])
 answer=publish(OUTPUT_FILE,out);print(json.dumps(dict(answer,events=43,axisymmetry_precision_admitted=False)))
if __name__=='__main__':main()
