"""Own arithmetic-only schedule reconstruction. No reviewed source is executed.
Models declared 30-second processor sharing and 60-second admissions; it does
not launch, observe processes, inspect saved runs, or validate empirical inputs.
"""
from pathlib import Path
import json, hashlib, math, time
from datetime import datetime, timezone

A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
D=A/'step4_launch_readiness_c4/launch_order'
O=A/'review_step4_readiness_cx2/schedule'
P={
 'order':D/'LAUNCH_ORDER_C4V001.json',
 'launch_doc':D/'LAUNCH_ORDER_C4V001.md',
 'roots':D/'ROOT_ITEMS_FINAL_C4V001.md',
 'manifest':D/'HASHES.txt',
 'sim_source':D/'tools/schedule_sim_c4v002.py',
 'sim_record':D/'work/SCHEDULE_SIM_C4V002.json',
 'timing':A/'tail_scheme_impl_c2/kbig_timing_v003/TIMING_V003.json',
 'projection':A/'parallel_route_a_c2/results/projection_c2v001.json',
 'campaign_source':A/'calibration_orchestrator_c2/v005/campaign_c2v005.py',
 'config':A/'calib_tail_readiness_cx2/v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json',
 'no_fallback_ruling':A.parent/'FROM_CODEX/0620_2026-10-18_claude4_codex1_step4_no_unguarded_fallback.md',
}
expected={
 'order':'2b4dd6a0bdb0f541793a43f6b2091b586ffbed45532999b99103ae66b01bd6ab',
 'launch_doc':'c276c4d9e3c5552d26ae600eac01d97489aaf766daf2abf5e6fe69185a795938',
 'roots':'5d83f0672f9b45fdae31772b2c29c5f786159aa960f0855cc1e258291353ee36',
 'manifest':'be7f811dc5381bbf3c4ba217c1d6f2ff0a111426454a00589dc07ad4b0b2186c',
 'sim_source':'94a0aa32797a3be359905e9b12f1a941342859356687538008c602ea8ef4c6a6',
 'sim_record':'2723042e704a04ae7dd90c7aeec848e210f2895bbeb6985823b11a864f22029b',
 'timing':'3e3fb60081acf19c6247bda056ebcb92a4cfb4439dbe912b8b6213da4f9ec925',
 'projection':'cffa3150a2aac120bad1fdb045a93f645b938f76f22c3e8ff0bce56f387eaad2',
 'campaign_source':'d35d5d4a62e6e5b632eb10c59bf4c82c2b1d744f6ceba609399c02baa5ecfeb2',
 'config':'721c7230f3f3efde6f8406f13a52995ae321248829ab1ee64a2f522ad5582b8e',
}
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(v):
 d={}
 for k,x in v:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=x
 return d
def parse(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def save(n,b):
 with (O/n).open('xb') as f:f.write(b)
 return sha(b)
raw={}
for k,p in P.items():
 assert not any(x in ('runs','runs_ext') for x in p.parts)
 raw[k]=p.read_bytes()
 if k in expected:assert sha(raw[k])==expected[k],k+' changed before audit'
pins={k:{'path':str(P[k]),'sha256':sha(b)} for k,b in raw.items()}
# Preserve the exact reviewed final-named documents because previous versions changed in place.
for k in ('order','launch_doc','roots','manifest'):
 save('SNAPSHOT_200805_'+P[k].name,raw[k])
T=parse(raw['timing']);J=parse(raw['projection']);S=parse(raw['sim_record']);L=parse(raw['order'])
n8=next(x for x in J['DDO154_KMAX_A2F10_C4_measured']['rows'] if x['N']==8)
iteration=(n8['seconds_low']+n8['seconds_high'])/2
prep=T['baseline_tail_off']['route_a_8_workers_s_PROJECTION_UNTESTED'][0]-7*n8['seconds_low']
cold=T['measured']['128']['route_a']['solo_estimate']['cold_s']
warm=T['measured']['128']['route_a']['solo_estimate']['warm_s']
def segments(on,upper):
 n=32 if upper else 7
 b=T['baseline_tail_off']
 rb=b['C4R3_receipt_offset_to_le3_s']+b['C4_V005_reference_s']+b['C4_V005_body_s']+(3*T['baseline_extra_pass_s'] if upper else 0)
 phases=[('prep',prep,1)]
 if on:phases.append(('cold',cold,1))
 for _ in range(n):
  phases.append(('iteration',iteration,8))
  if on:phases.append(('warm',warm,1))
 if on:
  phases.append(('manifest',cold,1))
  key='C4T_upper_I32_P6' if upper else 'C4T_expected_I7_P3'
  rb+=T['scenarios'][key]['tail_solo_estimate']['route_b_side_s']
 phases.append(('B',rb,1.5))
 return phases

def project(wave_sizes,on,upper,*,campaign=False,limit=6,budget=17,ra_limit=3,cores=18):
 phases=segments(on,upper);clock=0.;spans=[];starts=[];ends=[];headline_end=None
 peak_ra=peak_demand=peak_account=0;minimum_free=100.;late=0
 for nw in wave_sizes:
  w0=clock;next_admit=clock;active=[];previous=None;queue=nw
  while queue or active:
   if clock>=next_admit and queue:
    while queue:
     ra=sum(c['ra'] for c in active)
     account=sum(8 if c['ra'] else 2 for c in active)
     memory=17+sum((13.7 if on else 10.5) if c['ra'] else (4.3 if on else 3.01) for c in active)
     allowed=(len(active)<limit and account+8<=budget) if campaign else (
       previous is None or (previous['first'] and ra<ra_limit and 100*(128-memory)/128>=25))
     if not allowed:break
     c={'pos':0,'left':phases[0][1],'ra':True,'first':False,'start':clock,'id':len(starts)}
     starts.append(clock);active.append(c);previous=c;queue-=1
     if clock-w0>172800:late+=1
     if not campaign:break
    next_admit=clock+60
   demand=sum(phases[c['pos']][2] for c in active)
   pace=1 if demand<=cores else cores/demand
   peak_demand=max(peak_demand,demand);peak_ra=max(peak_ra,sum(c['ra'] for c in active))
   peak_account=max(peak_account,sum(8 if c['ra'] else 2 for c in active))
   memory=17+sum((13.7 if on else 10.5) if c['ra'] else (4.3 if on else 3.01) for c in active)
   minimum_free=min(minimum_free,100*(128-memory)/128)
   clock+=30
   for c in active[:]:
    advance=30*pace
    while advance>1e-12:
     chunk=min(c['left'],advance);c['left']-=chunk;advance-=chunk
     if c['left']>1e-9:break
     if phases[c['pos']][0]=='iteration':c['first']=True
     c['pos']+=1
     if c['pos']==len(phases):
      ends.append((c['id'],clock,clock-c['start']));active.remove(c);break
     if phases[c['pos']][0] in ('manifest','B'):c['ra']=False
     c['left']=phases[c['pos']][1]
   assert clock<1e7
  spans.append((clock-w0)/3600)
 return {'makespan_h':round(clock/3600,2),'max_route_a':peak_ra,'max_demand':peak_demand,
  'max_accounted':peak_account,'min_free_percent':minimum_free,
  'max_wave_span_h':round(max(spans),2),'calls_starting_after_48h_wave_cap':late,
  'per_call_wall_h_min_max':[round(min(x[2] for x in ends)/3600,2),round(max(x[2] for x in ends)/3600,2)],
  'headline9_done_h':round(max(x[1] for x in ends if x[0]<9)/3600,2) if len(ends)>=9 else None,
  'headline10_done_h':round(max(x[1] for x in ends if x[0]<10)/3600,2) if len(ends)>=10 else None}

checks=[];computed={}
def ck(n,ok,detail=None):checks.append({'name':n,'pass':bool(ok),'detail':detail})
for on in (False,True):
 for upper in (False,True):
  key=('TAIL_ON' if on else 'TAIL_OFF')+('_U_ADJ' if upper else '_E')
  sec=sum(x[1] for x in segments(on,upper))
  ck(key+' solo hours',round(sec/3600,2)==S['per_call'][key]['solo_h'],{'computed_seconds':sec})
for n,lab,on in [(4,'DIII_4',False),(10,'HEADLINE_10',True),(18,'SENS_18_BOTH_D',True),(2,'POST_S1_2',True)]:
 for up in (False,True):
  key=lab+'|'+('U_ADJ' if up else 'E')+'|RAMP_RA3|cores18'
  v=project([n],on,up);computed[key]=v
  for fld in ('makespan_h','max_route_a','max_demand','max_accounted','per_call_wall_h_min_max'):
   ck(key+' '+fld,v[fld]==S['batches'][key][fld],{'computed':v[fld],'published':S['batches'][key][fld]})
  ck(key+' memory',abs(v['min_free_percent']-S['batches'][key]['min_free_percent'])<1e-12)
sizes=[1]+[6]*19+[5]
ck('wave count21 and call budget120',len(sizes)==21 and sum(sizes)==120)
for m in (1,6):
 for up in (False,True):
  key=('U_ADJ' if up else 'E')+f'|max_concurrent{m}|budget17|cores18'
  v=project(sizes,True,up,campaign=True,limit=m);computed[key]=v
  for fld in ('makespan_h','max_route_a','max_accounted','max_wave_span_h','calls_starting_after_48h_wave_cap'):
   ck(key+' '+fld,v[fld]==S['campaign'][key][fld],{'computed':v[fld],'published':S['campaign'][key][fld]})
  ck(key+' budget enforced',v['max_accounted']<=17 and v['max_route_a']<=2)
for up in (False,True):
 sc='U_ADJ' if up else 'E';key='MIXED_9H_18S|'+sc+'|RAMP_RA3|cores18'
 v=project([27],True,up);computed[key]=v
 ck(key+' total',v['makespan_h']==S['mixed_queue'][key]['makespan_h'])
 ck(key+' headline9',v['headline9_done_h']==S['mixed_queue'][key]['headline_subset_done_h'])
 computed['OWN_MIXED_10H_18S|'+sc]=project([28],True,up)
for sc,up in [('E',False),('U',True)]:
 tag='U_ADJ' if up else 'E'
 h=computed['HEADLINE_10|'+tag+'|RAMP_RA3|cores18']['makespan_h'];c=computed[tag+'|max_concurrent6|budget17|cores18']['makespan_h'];p=computed['POST_S1_2|'+tag+'|RAMP_RA3|cores18']['makespan_h'];s=computed['SENS_18_BOTH_D|'+tag+'|RAMP_RA3|cores18']['makespan_h']
 ck(sc+' critical sum',round(h+c+p,1)==L['wall_times']['critical_path'][sc+'_h'])
 ck(sc+' total sum',round(h+c+p+s,1)==L['wall_times']['critical_path']['total_step4_from_T0_sequential'][sc+'_h'])
 ph=lambda on:sum(sec*workers for _,sec,workers in segments(on,up))/3600
 ck(sc+' process hours',round(150*ph(True)+4*ph(False),0)==L['wall_times']['compute_volume_process_hours'][sc])
# Exact-boundary witness for the published metric, not a launched or measured call.
cap_probe={'hypothetical_start_offsets_s':[0,57600,115200,172800],
 'published_metric_gt_cap':sum(x>172800 for x in [0,57600,115200,172800]),
 'actual_campaign_inadmissible_ge_cap':sum(x>=172800 for x in [0,57600,115200,172800])}
ck('cap endpoint distinction',cap_probe['published_metric_gt_cap']==0 and cap_probe['actual_campaign_inadmissible_ge_cap']==1)
ck('source metric uses strict greater','c.start - w0 > 172800.0' in raw['sim_source'].decode())
ck('real admission is strictly before cap','time.monotonic() - t0 < cap' in raw['campaign_source'].decode())
end={k:sha(p.read_bytes()) for k,p in P.items()}
changed=[k for k in pins if pins[k]['sha256']!=end[k]]
result={'schema':'CX2_STEP4_OWN_SCHEDULE_ARITHMETIC_V001','date_u':'Sun Oct 18 20:08:05 UTC 2026',
 'utc':datetime.now(timezone.utc).isoformat(),'policy':'nice unavailable (sandbox); 0514 waiver',
 'passed':sum(x['pass'] for x in checks),'total':len(checks),'failures':[x for x in checks if not x['pass']],
 'checks':checks,'computed':computed,'cap_boundary_witness':cap_probe,'pins_start':pins,'pins_end':end,'changed_during_audit':changed,
 'TESTED':'Independent arithmetic under the declared fixed-step fluid model, source pin checks, record sums; no scheduler module executed.',
 'UNTESTED':'Empirical timings, actual stage iteration counts, performance under real load, RAM usage, failure handling, adaptive campaign wave sizes, launcher admission and root work latency.',
 'scope':'Historical exact versioned input bytes preserved in owned snapshots; 0620 removes the unguarded fallback regardless of stale document text.'}
b=(json.dumps(result,indent=2,allow_nan=False)+'\n').encode();h=save('ARITHMETIC_RESULTS_CX2V001.json',b)
print(json.dumps({'passed':result['passed'],'total':result['total'],'failures':result['failures'],'changed':changed,'result_sha256':h,'mixed10':{k:v for k,v in computed.items() if k.startswith('OWN_MIXED')}}))
