"""Rehearsal implementation of UNSEALED prereg r2. Never a production classifier."""
import copy,hashlib,json,statistics,time,types,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parent
RUN=ROOT/'run_20261018T185402142937Z'
OUT=ROOT/'reading_v001';OUT.mkdir()
def write(p,d):
 with open(p,'x') as f:json.dump(d,f,sort_keys=True,indent=1,allow_nan=False)
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def load(p,n):
 m=types.ModuleType(n);m.__file__=str(p);sys.modules[n]=m;exec(compile(Path(p).read_bytes(),str(p),'exec'),m.__dict__);return m
ART=ROOT.parent;FD=ART/'freeze_score_readiness_cx3/v003g';PR=ART/'miss_reading_prereg_c4/r2/round1/PREREG_MISS_READING_R2.md'
R=load(FD/'review_v003g_cx3v001.py','reading_helpers');R.RUN=ROOT
R.ALLOWED.update(str(p.resolve()) for p in (Path(__file__),PR));sys.addaudithook(R.audit)
F=load(FD/'prediction_freeze_c2v003g_cx3v001.py','reading_freeze')
slots=json.loads((FD/'slots/NGC3198_FREEZE_SLOTS_CX3V003.json').read_bytes());Q=slots['query_block']['rows'];IDS=[r['query_id'] for r in Q]
trace=json.loads((RUN/'TRACE.json').read_bytes());base=json.loads((RUN/'LADDER_SYNTHETIC.json').read_bytes());doc=json.loads(Path(trace['freeze']['path']).read_bytes())
ZONES=['INNER','TRANSITION','OUTER'];GRID_NOTE='Counted coefficient-grid uncertainty (A63/A65); no sigma widening or tier change.'
READINGS={'P1':['R-MF','R-UT1','R-HIST','R-REACH','R-DRIFT'],'P2':['R-MF','R-S1','R-GRID','R-DRIFT'],'P3':['R-GEFF','R-ML','R-SPEC','R-GEO','R-NAX'],'P4':['R-GEFF','R-ML','R-SPEC','R-GEO','R-NAX'],'P5':['R-UT1','R-HIST','R-REACH','R-DRIFT','R-NAX'],'P6':['R-S1','R-GEO','R-MF'],'P7':['R-NAX','R-MF'],'P10':['R-TSR']}
DT={'R-MF':['SCORE_SCOPE_ONLY'],'R-UT1':['DT-UT1'],'R-HIST':['DT-BHD'],'R-REACH':['DT-U12'],'R-DRIFT':['DT-S0G'],'R-S1':['DT-S1'],'R-GRID':['DT-ALT','A17_C3'],'R-GEFF':['DT-T1a'],'R-ML':['DT-T1a','DT-ALT'],'R-SPEC':['DT-T1a'],'R-GEO':['DT-GEO'],'R-NAX':['DT-NAX'],'R-TSR':['DT-TSR']}
def classify(score,flags=None,rows_override=None):
 flags=flags or {};ref=next(m for m in score['members'] if m['member_id']==score['headline']['reference_member_id']);lr=rows_override or ref['rows'];er=score['pointwise_envelope']['rows']
 if [r['id'] for r in lr]!=IDS or [r['id'] for r in er]!=IDS:raise ValueError('CLASSIFICATION_INPUT_DEFECT')
 rows=[]
 for i,(l,e,q) in enumerate(zip(lr,er,Q)):
  required=('status','score_status','within_error','sigma_ratio','registered_reason')
  if any(k not in l for k in required) or 'band_overlaps_error_bar' not in e or l['status']=='UNEVALUATED_OR_REFUSED':raise ValueError('CLASSIFICATION_INPUT_DEFECT')
  radius=float(q['Rad_text']);zone='INNER' if radius<10 else 'TRANSITION' if radius<30 else 'OUTER'
  if zone!=('INNER' if i<24 else 'TRANSITION' if i<35 else 'OUTER'):raise ValueError('ZONE_TABLE_MISMATCH')
  tier='INVALID_AS_MISS' if l['score_status']=='INVALID_AS_MISS' else 'HIT' if l['within_error'] else 'NEAR' if e['band_overlaps_error_bar'] else 'MISS'
  r=None if tier=='INVALID_AS_MISS' else l['sigma_ratio']
  if tier!='INVALID_AS_MISS' and (not isinstance(r,(int,float)) or isinstance(r,bool)):raise ValueError('CLASSIFICATION_INPUT_DEFECT')
  rows.append(dict(query_id=l['id'],zone=zone,R_q=radius,tier=tier,r_q=r,sign=None if r is None else (r>0)-(r<0),NEAR=tier=='NEAR',TRUNCATION_SHAPE_RESIDUAL=l['id'] in flags,S_over_theta=flags.get(l['id']),invalid_reason=l['registered_reason'] if tier=='INVALID_AS_MISS' else None,notes=[GRID_NOTE]))
 zones={}
 for z in ZONES:
  rr=[r for r in rows if r['zone']==z];valid=[r for r in rr if r['tier']!='INVALID_AS_MISS'];nv=len(valid);med=statistics.median([r['r_q'] for r in valid]) if nv else None
  counts={t:sum(r['tier']==t for r in rr) for t in ('HIT','NEAR','MISS','INVALID_AS_MISS')}
  zones[z]=dict(counts=counts,N_v=nv,median_r=med,sign_class='UNDEFINED' if med is None else 'DEFICIT' if med<-1 else 'EXCESS' if med>1 else 'CENTERED',miss_dominated=nv>0 and counts['MISS']>=nv/2,hit_dominated=nv>0 and counts['HIT']>=nv/2,near_rows=[r['query_id'] for r in rr if r['NEAR']])
 I,T,O=[zones[z] for z in ZONES];outer=[r['r_q'] for r in rows if r['zone']=='OUTER' and r['r_q'] is not None];n=len(outer)//2
 delta=statistics.median(outer[n:])-statistics.median(outer[:n]) if len(outer)>=2 else None
 growing=O['sign_class']=='DEFICIT' and delta is not None and delta<0 and T['median_r'] is not None and T['median_r']>O['median_r']
 patterns={'P0':any(r['tier']=='INVALID_AS_MISS' for r in rows),'P1':O['miss_dominated'] and O['sign_class']=='DEFICIT','P2':O['miss_dominated'] and O['sign_class']=='EXCESS','P3':I['miss_dominated'] and I['sign_class']=='EXCESS','P4':I['miss_dominated'] and I['sign_class']=='DEFICIT','P5':I['hit_dominated'] and O['miss_dominated'] and T['N_v']>=1 and not T['hit_dominated'],'P6':all(z['N_v'] for z in zones.values()) and I['sign_class']==T['sign_class']==O['sign_class'] and I['sign_class']!='CENTERED','P7':any(r['tier']=='MISS' for r in rows) and not any(z['miss_dominated'] for z in zones.values()),'P8':not any(r['tier']=='MISS' for r in rows),'P9':O['N_v']==0,'P10':any(r['tier']=='MISS' and r['TRUNCATION_SHAPE_RESIDUAL'] for r in rows)}
 patterns['P1g']=patterns['P1'] and growing
 readings=[]
 for p,ids in READINGS.items():
  if not patterns[p]:continue
  for rid in ids:
   scope=[r['query_id'] for r in rows if r['tier']!='INVALID_AS_MISS' and (rid!='R-DRIFT' or r['zone']=='OUTER') and (rid!='R-TSR' or r['TRUNCATION_SHAPE_RESIDUAL'] and r['tier']=='MISS')]
   readings.append(dict(pattern=p,reading=rid,status='TESTED-NEGATIVE' if rid=='R-MF' and p in ('P1','P2') else 'OPEN',score_consistency='consistent',deciding_tests=[dict(id=d,status='SYNTHETIC_SCORE_ONLY' if d=='SCORE_SCOPE_ONLY' else 'NOT_RUN_IN_REHEARSAL') for d in DT[rid]],row_scope=scope,scope_note='Present-mass-only L=4 A2 calibrated response only; synthetic rehearsal, no scientific inference.'))
 invalid={}
 for r in rows:
  if r['tier']=='INVALID_AS_MISS':invalid.setdefault(r['invalid_reason'],[]).append({'query_id':r['query_id'],'zone':r['zone']})
 alts=[]
 for a in score['alternatives']:
  item={k:copy.deepcopy(v) for k,v in a.items() if k!='members'}
  if a.get('members'):
   twin=next((m for m in a['members'] if m['log_index']==ref['log_index']),None);item['twin_status']='AVAILABLE' if twin and twin['member_valid'] else 'NO_TWIN';item['twin_rows']=[] if twin is None else [{'query_id':r['id'],'tier':'INVALID_AS_MISS' if r['score_status']=='INVALID_AS_MISS' else 'HIT' if r['within_error'] else 'MISS','r_q':r['sigma_ratio']} for r in twin['rows']]
  alts.append(item)
 stage=[a for a in alts if a['name']=='STAGE0_GRID_OUTER'];alts=[a for a in alts if a['name']!='STAGE0_GRID_OUTER']+stage
 return dict(scope='SYNTHETIC_REHEARSAL_UNSEALED_PREREG_NOT_PRODUCTION',header=dict(prereg=pin(PR),prereg_status='UNSEALED_DRAFT_R2',manifest_sha=score['manifest_file_sha256_actual'],registration_sha=score['registration_file_sha256'],expected_manifest_sha=score['manifest_file_sha256_expected'],slots=pin(FD/'slots/NGC3198_FREEZE_SLOTS_CX3V003.json'),module=pin(Path(F.__file__)),rosters=trace['root_pins'],flag_record={'status':'SYNTHETIC_INPUT_ONLY_NOT_ROOT_REGISTERED'},I6={'status':'NOT_APPLICABLE_SYNTHETIC_NO_NUMERICAL_RUN','K_big':None,'M_s':None,'certificates':[]},freeze_status=score['freeze_status'],disclosures={'D1':'S0-FAIL-RHAT sealed negative; k=0 lapse drift SUPPORTED as quoted; causal gloss UNTESTED','D2':GRID_NOTE,'D3':'N1 kept-cube TRUNCATION_SHAPE residual; no scientific inference here','D4':'NOT_APPLICABLE_SYNTHETIC'}),headline=copy.deepcopy(score['headline']),rows=rows,zones=zones,outer_trend=dict(delta=delta,growing=growing),patterns=patterns,readings=readings,invalid_by_reason=invalid,A15=dict(E1a={k:I['counts'][k] for k in ('HIT','NEAR','MISS')},E1a_Q03_Q15=[r for r in rows[2:15]],E1b='NOT_AVAILABLE_NO_PRE_FREEZE_CARRIER',E2='NOT_TESTABLE' if patterns['P9'] else {'P1':patterns['P1'],'P1g':patterns['P1g'],'P2':patterns['P2'],'P8':patterns['P8'],'P9':patterns['P9']},E3='APPLIED'),alternatives=alts,P8_original_grid_consistency='REQUIRED_NOT_RUN_NO_SYNTHETIC_A17_C3_CARRIER' if patterns['P8'] else 'NOT_TRIGGERED',exploratory=[])

def main():
 t=time.monotonic();checks=[];reports={};flags={IDS[24]:1.0148}
 def chk(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
 reports['end_to_end']=classify(base)
 ref=next(m for m in doc['members'] if m['member_id']==doc['reference_member']['member_id'])
 scenarios={'all_hit':[0.]*43,'global_deficit':[-40.]*43,'global_excess':[40.]*43,'transition_onset':[0.]*24+[-40.]*11+[-50.-i for i in range(8)],'scattered':[0.]*43}
 scenarios['scattered'][24]=-40.
 for name,residuals in scenarios.items():
  target=[{'id':q,'velocity':(ref['speeds_km_s'][j] or 100.)-residuals[j],'sigma':1.} for j,q in enumerate(IDS)]
  sc=F.score_after_freeze(freeze_manifest_path=trace['freeze']['path'],registration_path=trace['freeze']['registration_path'],expected_manifest_file_sha256=base['manifest_file_sha256_expected'],target_rows=target,row_registration_rosters=trace['root_pins'])
  chk(name+'_public_score',sc['ok']);reports[name]=classify(sc,flags);write(OUT/(name+'_LADDER.json'),sc)
 # P9 is a classification unit fixture, explicitly not a new freeze/roster.
 synthetic=copy.deepcopy(base);r=next(m for m in synthetic['members'] if m['member_id']==synthetic['headline']['reference_member_id'])
 for row in r['rows'][35:]:row.update(score_status='INVALID_AS_MISS',status='INVALID',sigma_ratio=None,within_error=False,registered_reason='SYNTHETIC_OUTER_GATE')
 reports['outer_invalid_UNIT_ONLY']=classify(synthetic);reports['outer_invalid_UNIT_ONLY']['scope']='CLASSIFIER_UNIT_FIXTURE_NOT_PUBLIC_FREEZE'
 reached={p for rep in reports.values() for p,yes in rep['patterns'].items() if yes};chk('all_patterns_reachable',reached==set('P'+str(i) for i in range(11))|{'P1g'},sorted(reached))
 reachedr={r['reading'] for rep in reports.values() for r in rep['readings']};chk('all_readings_reachable',reachedr==set(DT),sorted(reachedr))
 for label,mut in [('missing_field',lambda d:d['members'][2]['rows'][3].pop('within_error')),('wrong_order',lambda d:d['members'][2]['rows'].reverse())]:
  bad=copy.deepcopy(base);mut(bad)
  try:classify(bad);ok=False
  except ValueError as e:ok=str(e)=='CLASSIFICATION_INPUT_DEFECT'
  chk(label+'_refused',ok)
 stage=next(a for a in slots['alternatives']['declared'] if a['name']=='STAGE0_GRID_OUTER');roster=F._load_row_roster(trace['root_pins']['STAGE0_GRID_OUTER'],IDS);scope=F._alternative_score_scope(stage,IDS,roster)
 chk('stage0_exact_8_rows',scope['query_ids']==IDS[35:] and scope['n_rows']==8)
 changed=copy.deepcopy(slots['alternatives']);changed['declared'][-1]['status']='EVALUATED_BEFORE_FREEZE';reasons=[];chk('stage0_public_flip_refused',F._bind_alternatives(changed,reasons) is None,reasons)
 m=copy.deepcopy(ref);m.update(row_valid=[True]*43,speeds_km_s=[100.]*43,row_registration=[None]*43)
 scored=F._score_members_on_rows([m],IDS,[(100.,1.)]*43,scope['query_ids'])[0];chk('stage0_private_subset_arithmetic',scored['n_rows']==8 and scored['within_error_count']==8)
 # Fixed registered DT-S0G comparison branches, synthetic counts/medians only.
 def grid(hp,hs,sp,ss,n):return 'NOT_DECIDED' if n==0 else 'CONSISTENT' if hs>hp else 'AGAINST' if ss==sp else 'NOT_DECIDED'
 chk('stage0_comparison_three_branches',[grid(1,2,'DEFICIT','CENTERED',8),grid(1,1,'DEFICIT','DEFICIT',8),grid(1,1,'DEFICIT','EXCESS',8),grid(0,0,'UNDEFINED','UNDEFINED',0)]==['CONSISTENT','AGAINST','NOT_DECIDED','NOT_DECIDED'])
 for name,report in reports.items():write(OUT/(name+'_READING.json'),report)
 rough=[{'id':'STAGE0','owner':'Claude2/Codex3','finding':'Adopted public slots prohibit evaluated STAGE0. Raw alternative saved; public refusal and private eight-row arithmetic TESTED. Evaluated public freeze requires adopted successor.'},{'id':'M7','owner':'Claude2/Claude4','finding':'No sealed TSR flag carrier/radial support rule. P10 only synthetic classification fixture; do not infer physical flagged rows.'},{'id':'M11','owner':'Claude2/Claude4','finding':'No pre-freeze baryonic Newtonian carrier. E1b NOT_AVAILABLE.'},{'id':'M12','owner':'Claude2/Claude4','finding':'Prereg r2 remains unsealed; this classifier is rehearsal only, requires independent review/adoption for production.'},{'id':'P8','owner':'Claude2','finding':'Mandatory ORIGINAL_K/A17 C3 consistency needs pinned C3 carrier; no synthetic carrier fabricated.'},{'id':'I6','owner':'Claude4','finding':'I6 mentions A66 shape-only allowance but later says only N_PASS under0512. Clarify precedence before score.'},{'id':'GEOMETRY','owner':'Claude2','finding':'Sensitivity geometry box attempted/refused as registered; all box sensitivity bands invalid, not zero width.'},{'id':'P9','owner':'Codex1','finding':'P9 covered as classifier unit only; separate all-outer-invalid public freeze not yet tested.'}]
 write(OUT/'RESULTS.json',dict(status='TESTED' if all(c['passed'] for c in checks) else 'TEST_FAILED',checks=checks,wall_seconds=time.monotonic()-t,rough_edges=rough,inputs=[pin(PR),pin(Path(__file__)),pin(RUN/'TRACE.json'),pin(RUN/'LADDER_SYNTHETIC.json')],output_pins=[pin(p) for p in sorted(OUT.glob('*_READING.json'))]))
 print(json.dumps({'checks':len(checks),'passed':sum(c['passed'] for c in checks),'dir':str(OUT)}))
if __name__=='__main__':main()
