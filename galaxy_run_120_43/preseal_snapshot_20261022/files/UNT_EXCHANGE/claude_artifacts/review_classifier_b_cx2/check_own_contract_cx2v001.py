"""Independent clause expectations for B outputs. Never opens A-side output."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2')
checks=[]
files={}

def read(path):
    raw=path.read_bytes()
    files[str(path)]=hashlib.sha256(raw).hexdigest()
    return json.loads(raw)

def check(case,clause,name,actual,expected):
    checks.append(dict(case=case,clause=clause,check=name,
                       actual=actual,expected=expected,pass_=actual==expected))

allcases=[]
for v in (1,2):
    idx=read(ROOT/('OWN_BUNDLE_INDEX_CX2V%03d.json'%v))
    for case in idx['cases']:
        cid=case['id']
        d=read(ROOT/'B_shared_outputs'/('OWN_CX2V%03d'%v)/cid/'B.json')
        allcases.append((case,d))
        check(cid,'C-1.1','honest classifier form has no stop',d['stops'],[])
        check(cid,'C-1.1','classification available',d['status'],'CLASSIFIED')
        check(cid,'C-4','two built-in inner INVALID rows',
              [r['tier'] for r in d['rows'][:2]],['INVALID_AS_MISS']*2)
        check(cid,'C-3','closed reading list length',len(d['readings']),13)
        for r in d['rows']:
            if r['tier']=='INVALID_AS_MISS':
                check(cid,'C-4','invalid row excluded from reading citations '+r['id'],
                      any(r['id'] in rr['cited_miss_rows'] for rr in d['readings']),False)
        if d['phase']=='PHASE_1':
            check(cid,'C-6.3','STAGE0 excluded in Phase1',d['stage0']['reasons'],['NOT_IN_PHASE_1'])
        else:
            check(cid,'C-8 item11','Phase2 remains score of record',d['agreement']['phase2_is_score_of_record'],True)
            check(cid,'C-8 item11','explicit absent Phase1 classification is not a defect',
                  d['agreement']['cross_phase'],{'NOT_AVAILABLE':['NO_PHASE_1_CLASSIFICATION']})
            check(cid,'C-8','Phase2 has no L1 band column',any('phase1_band' in r for r in d['rows']),False)
        if cid.startswith('H01'):
            check(cid,'C-1.1','inclusive unit thresholds and strict outside misses',
                  [r['tier'] for r in d['rows'][2:6]],['HIT','HIT','MISS','MISS'])
            check(cid,'C-2 P7','two scattered misses',d['patterns']['P7'],True)
        elif cid.startswith('H02'):
            for z in ('INNER','TRANSITION','OUTER'):
                check(cid,'C-2','global deficit '+z,d['zones'][z]['S'],'DEFICIT')
            check(cid,'C-2 P6','global offset',d['patterns']['P6'],True)
            check(cid,'C-1.4','flagged signed miss triggers P10',d['patterns']['P10'],True)
        elif cid.startswith('H03'):
            check(cid,'C-2','balanced outer signs median',d['zones']['OUTER']['m'],0.0)
            check(cid,'C-2 P11','outer mixed',d['patterns']['P11'],True)
            check(cid,'C-2','all eight outer misses',d['zones']['OUTER']['M'],8)
        elif cid.startswith('H04'):
            check(cid,'C-1.1/C-1.2','finite prediction with null ratio remains unsigned miss',
                  [(r['tier'],r['r_q'],r['sign']) for r in d['rows'][35:]],
                  [('MISS',None,'UNDEFINED')]*8)
            check(cid,'C-2 P14','unsigned outer count',d['zones']['OUTER']['U'],8)
            check(cid,'C-2 P14','outer unsigned pattern',d['patterns']['P14'],True)
        elif cid.startswith('H05'):
            check(cid,'C-4','outer cut invalid count',d['zones']['OUTER']['I'],4)
            check(cid,'C-4','remaining outer rows count',d['zones']['OUTER']['N_v'],4)
            check(cid,'C-2','remaining signed misses',d['zones']['OUTER']['M'],4)
        elif cid.startswith('H06'):
            check(cid,'C-1.1 L1 column','honest unavailable band row',
                  d['rows'][9]['phase1_band']['overlaps'],{'NOT_AVAILABLE':['L1_ROW_NOT_AVAILABLE']})
            check(cid,'C-1.1 L1 column','unavailable band does not retier',d['rows'][9]['tier'],'HIT')
        elif cid.startswith('H07'):
            check(cid,'C-1.1 L1 column','point band touching lower error edge overlaps',
                  [r['phase1_band']['overlaps'] for r in d['rows'][2:]],['yes']*41)
        elif cid.startswith('H08'):
            check(cid,'C-1.1 L1 column','unbounded FD noise remains a flag',
                  [r['phase1_band']['fd_noise_not_bounded'] for r in d['rows'][2:]],[True]*41)
            check(cid,'C-1.1','FD flag does not change hits',[r['tier'] for r in d['rows'][2:]],['HIT']*41)
        elif cid.startswith(('H09','H10','H13')):
            cmp=d['stage0']['comparison']
            better=not cid.startswith('H10')
            check(cid,'C-6.3','STAGE0 exact outer denominator',d['stage0']['denominator'],8)
            check(cid,'C-6.3','qualifying eight rows',len(cmp['qualifying_rows']),8)
            check(cid,'C-6.3','strict improvement or against comparison',
                  cmp['result'],'CONSISTENT' if better else 'AGAINST')
            drift=next(x for x in d['readings'] if x['reading']=='R-DRIFT')
            check(cid,'C-3/C-6.3','drift score relation',
                  drift['part1']['relation'],'CONSISTENT' if better else 'INCONSISTENT')
            check(cid,'C-6.1','alternative never gets primary TSR pattern',
                  d['stage0']['twin_classification']['patterns']['P10'],'NOT_EVALUATED_FOR_ALTERNATIVE')
        elif cid.startswith('H11'):
            check(cid,'C-8 item11','honest AT1 failure outcome',
                  d['agreement']['outcome'],'AGREEMENT_DEFECT')
            check(cid,'C-8 item11','Phase2 stands after AT1 failure',
                  d['agreement']['phase1_consequence'],'PHASE_2_STANDS_ROOT_INVESTIGATES')
            drift=next(x for x in d['readings'] if x['reading']=='R-DRIFT')
            check(cid,'C-3/C-6.3','absent pattern takes priority over against test',
                  drift['part1'],{'relation':'NOT_ADDRESSED','code':'PATTERN_NOT_HELD'})
            check(cid,'C-3/C-6.3','against test remains visible',drift['part2']['status'],'AGAINST')
        elif cid.startswith('H12'):
            check(cid,'C-6.3/A173','no successor cannot evaluate STAGE0',
                  d['stage0']['status'],'NOT_EVALUATED_BEFORE_FREEZE')
            check(cid,'C-6.3/A173','vacuous no-member record reason',d['stage0']['reasons'],['NO_SEALED_SUCCESSOR'])
        elif cid.startswith('H14'):
            check(cid,'C-6.1','invalid STAGE0 twin',d['stage0']['twin'],'TWIN_INVALID')
            drift=next(x for x in d['readings'] if x['reading']=='R-DRIFT')
            check(cid,'C-6.3','invalid twin leaves drift test open',drift['part2']['status'],'OPEN')
reporting=[]
for case,d in allcases:
    if case['id'].startswith(('H13','H14')):
        reporting.append(dict(case=case['id'],input_distribution=case['input_member_counts'],
            printed_field=d['stage0'].get('stage0_within_error_distribution'),
            alternative_entry=d['alternatives'][-1],
            classification='CONTRACT_AMBIGUITY_CA1_NONBLOCKING',
            clauses='C-6.1 invalid twin distribution; C-6.3 final sentence versus adopted output-schema shape',
            note='No classification, row reading, gate or blinding effect demonstrated.'))
result=dict(date_u=subprocess.check_output(['/bin/date','-u'],text=True).strip(),label='TESTED',
            n_cases=len(allcases),checks=len(checks),passed=sum(c['pass_'] for c in checks),
            failed=[c for c in checks if not c['pass_']],rows=checks,
            reporting_contract_probes=reporting,contract_ambiguity_count=1,
            files=[dict(path=k,sha256=v) for k,v in sorted(files.items())])
with (ROOT/'OWN_CONTRACT_CHECKS_CX2V001.json').open('x') as f:
    json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:result[k] for k in ('n_cases','checks','passed','failed','contract_ambiguity_count')}))
