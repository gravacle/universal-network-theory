"""Provisional draft-only logical controls: invented counts and median-class flags, no scientific arrays."""
import hashlib,itertools,json,os,sys
from pathlib import Path
assert os.getpriority(os.PRIO_PROCESS,0)>=10 and sys.flags.isolated and sys.dont_write_bytecode
R=Path(__file__).parent;OUT=R/'LOGICAL_V001';OUT.mkdir();A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts');checks=[]
paths={'draft_text':A/'miss_reading_prereg_c4/r3_work/text_c4/PREREG_MISS_READING_R3.md','draft_root_items':A/'miss_reading_prereg_c4/r3_work/text_c4/ROOT_ITEMS_R3.md','baseline_findings':A/'review_miss_reading_r2_cx2/round2/FINDINGS_CX2V001.json','A98_dispatch':A.parent/'FROM_CODEX/0619_2026-10-18_claude4_codex3_A98.md','author_ack':A.parent/'FROM_CLAUDE4/0096_2026-10-18_ack_0619_miss_reading_r3.md','harness':Path(__file__)}
raw={k:p.read_bytes() for k,p in paths.items()};pins={k:{'path':str(paths[k]),'sha256':hashlib.sha256(b).hexdigest()} for k,b in raw.items()}
def ck(n,b,e=None):checks.append({'name':n,'pass':bool(b),'evidence':e})
def z(h=0,signed=0,unsigned=0,invalid=0,median='UNDEFINED'):
 nv=h+signed+unsigned;m=signed+unsigned;md=nv>0 and 2*m>=nv;hd=nv>0 and 2*h>nv
 sign='UNDEFINED' if median=='UNDEFINED' or md and 2*signed<nv else median
 return {'H':h,'signed_M':signed,'U':unsigned,'I':invalid,'Nv':nv,'M':m,'median_class':median,'miss_dominated':md,'hit_dominated':hd,'S':sign}
def late(a,k):return z(a['H'],a['signed_M'],a['U']+k,a['I']-k,a['median_class'])
def patterns(i,t,o,tsr=False,growing=False,crossing=False):
 p=set();zs=(i,t,o)
 if any(x['I']>0 for x in zs):p.add('P0')
 if o['miss_dominated']:p.add({'DEFICIT':'P1','EXCESS':'P2','CENTERED':'P11','UNDEFINED':'P14'}[o['S']])
 if i['miss_dominated']:p.add({'DEFICIT':'P4','EXCESS':'P3','CENTERED':'P12','UNDEFINED':'P15'}[i['S']])
 if t['miss_dominated']:p.add('P13')
 if i['hit_dominated'] and o['miss_dominated'] and t['Nv']>0 and not t['hit_dominated']:p.add('P5')
 if i['S']==t['S']==o['S'] and i['S'] in ('DEFICIT','EXCESS'):p.add('P6')
 if sum(x['M'] for x in zs)>0 and not any(x['miss_dominated'] for x in zs):p.add('P7')
 if sum(x['Nv'] for x in zs)>0 and sum(x['M'] for x in zs)==0:p.add('P8')
 if o['Nv']==0:p.add('P9')
 if tsr:p.add('P10')
 if growing and 'P1' in p:p.add('P1g')
 if crossing and 'P11' in p:p.add('P11g')
 return p
def verdict(o):return 'TESTED_NEGATIVE' if o['miss_dominated'] else 'NOT_NEGATIVE_AT_OUTER' if o['Nv'] else 'NOT_TESTABLE'
empty=z();hit=z(h=2,median='CENTERED');unsigned=z(unsigned=2);witnesses={}
for role,expected in [('OUTER','P14'),('INNER','P15'),('TRANSITION','P13')]:
 zs={'INNER':hit,'TRANSITION':hit,'OUTER':hit};zs[role]=unsigned;p=patterns(zs['INNER'],zs['TRANSITION'],zs['OUTER']);ck('all_unsigned_'+role,expected in p,sorted(p));witnesses[role+'_unsigned']={'zone':unsigned,'patterns':sorted(p)}
ck('r2_outer_coverage_counterexample_has_teeth',unsigned['miss_dominated'] and not {'P1','P2','P11','P7'}&patterns(hit,hit,unsigned))
ck('r2_inner_coverage_counterexample_has_teeth',unsigned['miss_dominated'] and not {'P3','P4','P12','P7'}&patterns(unsigned,hit,hit))
before=z(signed=1,invalid=2,median='DEFICIT');after=late(before,2);pb=patterns(hit,hit,before);pa=patterns(hit,hit,after)
ck('LATE_removes_P1_replaces_P14_while_signed_row_remains','P1' in pb and 'P1' not in pa and 'P14' in pa and after['signed_M']==1,{'before':before,'after':after})
witnesses['late_signed_to_unsigned']={'before':before,'after':after,'patterns_before':sorted(pb),'patterns_after':sorted(pa)}
allgate=z(invalid=2);alllate=late(allgate,2)
ck('all_LATE_outer_negative_explicit_policy',verdict(allgate)=='NOT_TESTABLE' and verdict(alllate)=='TESTED_NEGATIVE' and 'P14' in patterns(hit,hit,alllate))
# Exhaust an overapproximation of possible median-class flags at bounded counts.
# This avoids creating any residual/prediction/target arrays. Extra abstract states
# can only strengthen universal checks; no witness of physical attainability is claimed.
states=[]
for h,s,u,i in itertools.product(range(5),range(5),range(5),range(3)):
 if h+s+u>6:continue
 medians=['UNDEFINED'] if h+s==0 else ['CENTERED'] if h>s else ['DEFICIT','EXCESS','CENTERED']
 for median in medians:states.append(z(h,s,u,i,median))
def feature(a):return (a['Nv']>0,a['M']>0,a['I']>0,a['hit_dominated'],a['miss_dominated'],a['S'])
representatives={feature(a):a for a in states};domain=list(representatives.values());coverage=equivalence=partition=True;global_count=0
for i,t,o in itertools.product(domain,repeat=3):
 ps=patterns(i,t,o);global_count+=1;coverage &= not any(x['M'] for x in (i,t,o)) or bool(ps&{'P1','P2','P11','P14','P3','P4','P12','P15','P13','P7'})
 equivalence &= (len(ps&{'P1','P2','P11','P14'})==1)==o['miss_dominated']
 partition &= all(not a['Nv'] or a['miss_dominated'] != a['hit_dominated'] for a in (i,t,o))
ck('bounded_global_MISS_coverage',coverage,global_count);ck('bounded_OUTER_FAILURE_exact_one_pattern',equivalence,global_count);ck('hit_miss_partition',partition,global_count)
pairs={}
for a in states:
 for k in range(a['I']+1):
  b=late(a,k);pairs[(feature(a),feature(b))]=(a,b,k)
monotone=class_weakening=True
for a,b,k in pairs.values():
 monotone &= b['Nv']==a['Nv']+k and b['M']==a['M']+k and b['U']==a['U']+k and b['H']==a['H'] and b['median_class']==a['median_class'] and (not a['miss_dominated'] or b['miss_dominated'])
 class_weakening &= b['S'] in (a['S'],'UNDEFINED') and (a['S']!='UNDEFINED' or b['S']=='UNDEFINED')
ck('LATE_count_and_domination_monotonicity',monotone,len(pairs));ck('LATE_sign_only_same_or_undefined',class_weakening,len(pairs))
never_add={'P0','P1','P1g','P2','P3','P4','P6','P8','P9','P11','P11g','P12'};never_remove={'P13','P14','P15'}
changes_ok=True;replacement=True;status_ok=True;transition_count=0;seen_add=set();seen_remove=set()
for ip,tp,op in itertools.product(pairs.values(),repeat=3):
 i,t,o=ip[0],tp[0],op[0];j,u,q=ip[1],tp[1],op[1]
 x=patterns(i,t,o,True,True,True);y=patterns(j,u,q,True,True,True);add=y-x;remove=x-y;seen_add|=add;seen_remove|=remove;transition_count+=1
 changes_ok &= not add&never_add and not remove&never_remove and (('P10' in x)==('P10' in y))
 replacement &= not remove&{'P1','P2','P11'} or 'P14' in y
 replacement &= not remove&{'P3','P4','P12'} or 'P15' in y
 status_ok &= not o['miss_dominated'] or q['miss_dominated']
ck('C4_exact_forbidden_pattern_changes',changes_ok,{'transition_count':transition_count,'observed_add':sorted(seen_add),'observed_remove':sorted(seen_remove)});ck('signed_patterns_replaced_by_unsigned',replacement,transition_count);ck('E3_never_improves_under_LATE',status_ok,transition_count)
# Precise prose counterexample: all-HIT is CENTERED under C2, while C9's
# unqualified 'unless signed misses reach half' wording says UNDEFINED.
allhit=z(h=1,median='CENTERED');c9='UNDEFINED' if 2*allhit['signed_M']<allhit['Nv'] else allhit['S']
ck('C9_vs_C2_all_HIT_counterexample',allhit['S']=='CENTERED' and c9=='UNDEFINED',{'C2':allhit['S'],'C9_unqualified':c9})
# Pure fictional publication times, no actual history or output access.
pubs=[{'kind':'text','version':'R2','time':1},{'kind':'root_items','version':'R2','time':1},{'kind':'classifier','version':'R2','time':1},{'kind':'text','version':'R3','time':2},{'kind':'root_items','version':'R3','time':2},{'kind':'classifier','version':'R3','time':4}];first_read=3
selected={kind:max((p for p in pubs if p['kind']==kind and p['time']<first_read),key=lambda p:p['time']) for kind in ('text','root_items','classifier')}
ck('fallback_postread_candidate_excluded',selected['classifier']['version']=='R2');ck('fallback_mixed_version_countermodel',selected['text']['version']=='R3' and selected['root_items']['version']=='R3' and selected['classifier']['version']=='R2',selected)
ck('draft_bytes_unchanged_at_end',all(hashlib.sha256(p.read_bytes()).hexdigest()==pins[k]['sha256'] for k,p in paths.items()))
result={'schema':'UNT_MISS_READING_R3_PROVISIONAL_LOGIC_CX1V001','date_u':sys.argv[1],'status':'TESTED_LOGICAL_CONTROLS_DRAFT_ONLY','final_review_verdict':'PENDING_PUBLISHED_REVIEW_TUPLE','passed':sum(x['pass'] for x in checks),'total':len(checks),'checks':checks,'bounded_zone_states':len(states),'logical_feature_states':len(domain),'global_combinations':global_count,'logical_late_pairs':len(pairs),'late_global_combinations':transition_count,'witnesses':witnesses,'provisional_findings':[{'id':'CX1-MR3-P1','severity':'SHOULD_FIX_PROSE','claim':'C9 unqualified sign-class summary disagrees with C2 for all-HIT zones. Qualify by miss-dominated or explicitly refer to governing C2.','counterexample':{'H':1,'signed_M':0,'U':0,'median_class':'CENTERED','C2_S':'CENTERED','C9_unqualified_S':'UNDEFINED'}},{'id':'CX1-MR3-P2','severity':'SHOULD_FIX_VERSION_CONTRACT','claim':'Independent last-pre-read selection can mix R3 text/root-items with an R2 classifier. Explicitly bind a compatible tuple or treat an older incompatible classifier as unavailable, require deterministic agreement to exact text and preserve post-prediction labeling. M12 may block execution but fallback does not resolve this case.','counterexample':selected}], 'root_choices_preserved':['M3 recommended signed-miss threshold Nv/2 is stronger than ACK0096 all-unsigned wording; root must adopt exact selected text.','M15 all-LATE OUTER leads TESTED-NEGATIVE with no prediction and is expressly disclosed as an open root choice.'], 'source_pins':pins,'limits':['No actual classifier or author check code executed; no final published tuple exists in this review.','Counts and logical median-class flags are invented. No residual/prediction/target array was created or read.','Bounded state enumeration is not a proof for all row counts or all scientific outcomes. The direct partition argument is source-level.','Production M12 agreement, actual exposure history, final source currency and scientific adoption remain UNTESTED.','All writes are exclusive under assigned review prefix; no actual runs, targets, network or launches.']}
p=OUT/'RESULTS_CX1V001.json'
with p.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'passed':result['passed'],'total':result['total'],'final_review_verdict':result['final_review_verdict'],'global_combinations':global_count,'late_combinations':transition_count,'result_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'failures':[x for x in checks if not x['pass']]}))
