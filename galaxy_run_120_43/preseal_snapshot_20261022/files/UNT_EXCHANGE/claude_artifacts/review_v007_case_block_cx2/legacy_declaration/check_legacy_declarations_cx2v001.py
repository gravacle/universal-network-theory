"""Independent static A50/A99 declaration check; no project import, no pointer following."""
from pathlib import Path
import os,stat,json,hashlib,copy

A='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
O=Path(A)/'review_v007_case_block_cx2/legacy_declaration'
P={
 'review':(A+'/kmax_prereg_v005_c2/extension_c5c6/check/REVIEW_V009_PREP_V009_V001_ORIG_3bce7c02.json','3bce7c02926526edf2a594418097ff379604ee1c9760dc1145bcd37ed2882d9f'),
 'dry':(A+'/c5h_hull_c2/dryrun/C5H/DRYRUN_REPORT.json','cbd2885dd6a41ded3ec34f6daa07069108fec68d644d22f0819f972747d9bf7a'),
 'reviewed_spec':(A+'/kmax_prereg_v005_c2/extension_c5c6/v006_r1/specs/CALL_KMAX_C5R3_A2F10_EXT_N8_M32_C2V009.json','09ff5a96c02b0428f121138f5ebc23072333c743506a93774af9f496d7fc51e8'),
 'hull_spec':(A+'/c5h_hull_c2/CALL_KMAX_C5H_A2F10_HULL_N8_M32_C2V009.json','60b4613080055aedd92dbb649cdfa45675f64a4d133c7ba3e4fbb15b59c7704e'),
 'candidate':(A+'/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json','76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'),
 'r12_source':(A+'/v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py','4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28'),
 'builder_source':(A+'/v007_final_prereg_c4/r5/tools/build_case_block_c4v001.py','11823fe0e9c0dab0b3f47360e73f8a572e7259f534647eca3a3b257d96beaaae'),
 'loader_source':(A+'/v007_final_prereg_c4/r5/tools/load_r12_c4r5.py','caf3ea9c795083133c351f7813f1d35f7fd8242f5dfacc324295896ff614e79e'),
}
chains={};raw={}
def sha(b):return hashlib.sha256(b).hexdigest()
def deny(p):
 s=os.fspath(p).lower();parts=s.split('/')
 if any(x in ('runs','runs_ext') for x in parts) or 'c5h_run_v001' in s or any(x.startswith('uvt_') for x in parts) or s.startswith('/.vol'):
  raise PermissionError('forbidden path before traversal')
 if any(x in s for x in ('target_velocity','target_velocities','observed_velocity','observed_velocities')) or ('ngc3198' in s and any(x in s for x in ('target','observed','rotation_curve'))):
  raise PermissionError('target velocity path before traversal')
def safe_path(path):
 """Check every lexical candidate and symlink target BEFORE lstat/traversal."""
 deny(path);assert os.path.isabs(path)
 pending=path.split('/')[1:];done=[];events=[];links=0
 while pending:
  part=pending.pop(0)
  if not part or part=='.':continue
  if part=='..':
   if done:done.pop()
   continue
  candidate='/'+'/'.join(done+[part]);deny(candidate)
  st=os.lstat(candidate)
  if stat.S_ISLNK(st.st_mode):
   links+=1
   if links>40:raise ValueError('too many symlinks')
   target=os.readlink(candidate);deny(target)
   expanded=target if os.path.isabs(target) else '/'+'/'.join(done+[target])
   deny(expanded);events.append({'link':candidate,'target':target})
   pending=expanded.split('/')[1:]+pending;done=[]
  else:
   if pending and not stat.S_ISDIR(st.st_mode):raise ValueError('non-directory component')
   if not pending and not stat.S_ISREG(st.st_mode):raise ValueError('not a regular static declaration')
   done.append(part)
 q='/'+'/'.join(done);deny(q);return q,events
def read(path):
 q,events=safe_path(path);chains[path]={'resolved':q,'symlinks':events}
 fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  if not stat.S_ISREG(os.fstat(fd).st_mode):raise ValueError('not regular')
  with os.fdopen(fd,'rb',closefd=False) as f:return f.read()
 finally:os.close(fd)
def pairs(xs):
 d={}
 for k,v in xs:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=v
 return d
def parse(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
def leaves(x,path=()):
 if isinstance(x,dict):
  if not x:return {path:canon({})}
  return {k:v for name,value in x.items() for k,v in leaves(value,path+(name,)).items()}
 return {path:canon(x)}
def diffs(a,b):
 a,b=leaves(a),leaves(b)
 return sorted(k for k in set(a)|set(b) if a.get(k)!=b.get(k))
for k,(p,h) in P.items():
 raw[k]=read(p);assert sha(raw[k])==h,k
J={k:parse(raw[k]) for k in ('review','dry','reviewed_spec','hull_spec','candidate')}
rv,dry,rs,hs,cb=[J[k] for k in ('review','dry','reviewed_spec','hull_spec','candidate')]
checks=[]
def ck(n,b):checks.append({'name':n,'pass':bool(b)})
sr=rv.get('shas_reviewed') or {};reviewed={v.get('sha256') for v in sr.values() if isinstance(v,dict)}
driver='999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6'
ck('preserved review PASS zero blocking',rv['verdict']=='PASS' and rv['blocking_findings']==0)
ck('review binds driver',sr['driver_v009_EXT']['sha256']==driver)
ck('review binds reviewed C5 spec',P['reviewed_spec'][1] in reviewed)
diff=diffs(hs,rs)
off=[p for p in diff if p!=('label',) and p[:5]!=('numerics','brackets','rule','fs_absolute_overrides')[:5]]
# Explicit prefix is four path components; indices are below it.
off=[p for p in diff if p!=('label',) and not (len(p)>4 and p[:4]==('numerics','brackets','rule','fs_absolute_overrides'))]
ck('spec differences nonempty and within declaration allowances',bool(diff) and not off)
ck('dry binds exact hull spec',dry['call_spec_sha256']==P['hull_spec'][1])
ck('dry binds driver',dry['driver_sha256']==driver)
ck('dry binding blockers empty',dry['binding_blockers']==[])
rr=dry['remaining_refusals'];ck('dry unexplained/beyond-pending empty',rr.get('unexplained')==[] and rr.get('beyond_pending_inputs')==[])
dn=dry['normalized_spec']['numerics'];sn=hs['numerics'];sleaf,dleaf=leaves(sn),leaves(dn)
changed=[p for p in sleaf if dleaf.get(p)!=sleaf[p]];added=[p for p in dleaf if p not in sleaf]
ck('normalization preserves every source numeric leaf',not changed)
ck('normalization adds only cube null default',added==[('truncation','kmax_inverse_kpc')] and dn['truncation']['kmax_inverse_kpc'] is None)
ck('dry recorded no execution',dry.get('executed_stages')==0)
ck('dry physical coefficient metadata consistent',canon(dry['normalized_spec']['physical'])==canon(hs['physical']) and canon(dry['normalized_spec']['coefficients'])==canon(hs['coefficients']))
ck('candidate parallel8 empty key map',cb['route_a_mode']=='parallel8' and cb['key_equivalence_map']==[])
d5=cb['cases']['C4T-D5']['normalized_spec_equal']['/numerics'];a,b=copy.deepcopy(d5),copy.deepcopy(dn)
for name in ('composite_grid_spec','uv_tail'):a.pop(name,None);b.pop(name,None)
ck('D5 exact normalized equality outside two allowed blocks',canon(a)==canon(b))
ck('D5/reference worker count8 retained',a['route_a']['column_workers']==b['route_a']['column_workers']==8)
ck('D5/reference iteration budget32 retained',a['route_a']['max_iterations']==b['route_a']['max_iterations']==32)
ck('D5/reference Picard6 retained',a['picard']['passes']==b['picard']['passes']==6)
ck('D5/reference brackets retained',canon(a['brackets'])==canon(b['brackets']))
ck('literal A48 reviewed-both claim reported false',P['hull_spec'][1] not in reviewed)
# Own comparison controls do not create or admit a case block.
bad=copy.deepcopy(a);bad['route_a']['column_workers']=1
ck('worker mutation is not exempt',canon(bad)!=canon(b))
bad=copy.deepcopy(a);bad['picard']['passes']=7
ck('Picard mutation is not exempt',canon(bad)!=canon(b))
bad=copy.deepcopy(d5);bad['uv_tail']={'own_synthetic':True};bad['composite_grid_spec']={'own_synthetic':True}
for name in ('composite_grid_spec','uv_tail'):bad.pop(name,None)
ck('only declared blocks exempt',canon(bad)==canon(b))
end={k:sha(read(p)) for k,(p,h) in P.items()};changedpins=[k for k,(p,h) in P.items() if end[k]!=h]
ck('all bytes stable',not changedpins)
out={'schema':'CX2_A99_LEGACY_DECLARATION_V001','date_u':'Sun Oct 18 20:42:44 UTC 2026','policy':'nice unavailable (sandbox); 0514 waiver','verdict':'PASS','passed':sum(x['pass'] for x in checks),'total':len(checks),'checks':checks,'findings':[],
 'declaration_difference_paths':['/'+'/'.join(p) for p in diff],'outside_allowed_difference_paths':['/'+'/'.join(p) for p in off],
 'normalization_added_paths':['/'+'/'.join(p) for p in added],'normalization_changed_paths':['/'+'/'.join(p) for p in changed],
 'D5_unexcluded_difference_paths':['/'+'/'.join(p) for p in diffs(d5,dn)],'D5_after_exclusions_difference_paths':['/'+'/'.join(p) for p in diffs(a,b)],
 'A48_literal_both_spec_hashes_claim':False,'admission_declaration_grounds':'Preserved review of driver+C5 spec, hull-spec differences limited to label/fs_absolute_overrides, clean saved dry report; exact normalization adds only truncation default.',
 'TESTED':'Static declarations and source-defined metadata predicates, no project code execution. D5 normalized numerics equal saved dry-reference numerics except composite_grid_spec and uv_tail. Symlink checks precede metadata traversal and reject run/target paths.',
 'UNTESTED':'Actual C5H/other run custody, actual scientific execution/results, saved dry-run process provenance beyond the static report, underlying coefficient or state arrays, full comparator runtime and sealed production admission.',
 'pins_start':{k:{'path':p,'sha256':h} for k,(p,h) in P.items()},'pins_end':end,'changed':changedpins,'path_chains':chains,'embedded_pointers_followed':False}
assert all(x['pass'] for x in checks)
p=O/'LEGACY_DECLARATION_RESULTS_CX2V001.json'
with p.open('x') as f:json.dump(out,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps({'verdict':out['verdict'],'passed':out['passed'],'total':out['total'],'difference_count':len(diff),'added':out['normalization_added_paths'],'sources':len(P),'sha256':sha(p.read_bytes())}))
