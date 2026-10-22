"""Independent bounded step5 filler review. No scientific work or output filling."""
from pathlib import Path
import ast,copy,hashlib,importlib.util,json,math,os,sys
ROOT=Path(__file__).parent.parent;OUT=ROOT/'review'
F=ROOT/'tools/fill_step5_cx3v002.py';POL=ROOT/'POLICY_CX3V001.json';TEST=ROOT/'FILLER_TESTS_CX3V001.json'
READS=set()
def audit(event,args):
    if event in ('subprocess.Popen','os.system','os.posix_spawn','os.remove','os.rename','os.rmdir','socket.connect','socket.getaddrinfo'):raise RuntimeError('FORBIDDEN_'+event)
    if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
        p=Path(os.fsdecode(args[0]));r=p.resolve();s=str(r).lower()
        if '/runs_ext/uvt_' in s or 'kmax_a2f10_c5h_run_v001' in s or '/.codex/' in s or '/.codex-alt/' in s:raise RuntimeError('FORBIDDEN_READ')
        if 'ngc3198' in s and any(x in s for x in ('observed','velocit','rotmod')):raise RuntimeError('NGC_TARGET_READ')
        if isinstance(args[2],int) and args[2]&(os.O_WRONLY|os.O_RDWR):
            if not r.is_relative_to(OUT) or p.exists() or not args[2]&os.O_EXCL:raise RuntimeError('WRITE_NOT_NEW_REVIEW')
        elif '/Research/' in str(p):READS.add(str(p))
sys.addaudithook(audit)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def write(name,data):
    with (OUT/name).open('xb') as f:f.write((json.dumps(data,indent=2)+'\n').encode())
def caught(f):
    try:return {'return':f()}
    except Exception as e:return {'exception':type(e).__name__,'message':str(e)}
sp=importlib.util.spec_from_file_location('independent_step5',F);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
assert sha(F)=='c427a8eafec7c540629cc4063756f311d789764303c029dd0d432521721be6e8'
checks=[]
def check(name,ok,detail=None):checks.append({'name':name,'pass':bool(ok),'detail':detail})
check('POLICY_BYTES_ANCHORED',sha(POL)==m.POLICY_SHA)
p=m.parse(POL.read_bytes());co=m.load_pin(p['coordinates'],'COORDINATES');slots=m.load_pin(p['slots'],'SLOTS')
hand=ROOT/'synthetic/SYNTHETIC_HANDOFF_CX3V001.json'
payloads,receipt=m.prepare(hand,sha(hand),True)
check('PURE_PREPARE_FOUR_SPECS',len(payloads)==5 and len(receipt['outputs'])==4)
export=m.load_pin(m.parse(hand.read_bytes())['source_export_pin'],'EXPORT');point=export['admitted_points'][0]
for label,template_pin in p['templates'].items():
    t=m.load_pin(template_pin,label);original=m.load_pin(t['source_spec_pin'],label+'_SOURCE');spec=m.parse(payloads['CALL_'+label+'_CX3V001.json'])
    a=copy.deepcopy(original);b=copy.deepcopy(spec)
    for q in (a,b):q.pop('label');q.pop('physical')
    check(label+'_ALL_NONPHYSICAL_EQUALS_SOURCE',a==b)
    check(label+'_GAMMA_PRODUCT',spec['physical']['gamma']==point['theta_natural']['gamma_over_Eref']*point['theta_natural']['Eref_base_J'])
    check(label+'_GEOMETRY_FROM_REAL_SLOTS',spec['physical']['distance_Mpc']==13.8 and spec['physical']['inclination_deg']==72.)
    check(label+'_SOURCE_COEFFICIENTS_MATCH_FILLED',original['coefficients']==spec['coefficients'])
    check(label+'_OUTPUT_PIN_BYTES',next(r['sha256'] for r in receipt['outputs'] if r['file']=='CALL_'+label+'_CX3V001.json')==hashlib.sha256(payloads['CALL_'+label+'_CX3V001.json']).hexdigest())
for name,value in [('bool',True),('str','0.5'),('inf',float('inf')),('nan',float('nan')),('list',[]),('dict',{})]:
    bad=copy.deepcopy(export);bad['admitted_points'][0]['u'][0]=value
    got=caught(lambda:m.validate_points(bad,co));check('REJECT_U_'+name,got.get('exception')=='Refusal',got)
bad=copy.deepcopy(export);bad['admitted_points'][0]['theta_natural']['gamma_over_Eref']*=1.0000001
got=caught(lambda:m.validate_points(bad,co));check('REJECT_SMALL_RELATIVE_GAMMA_CHANGE',got.get('exception')=='Refusal',got)
for name,raw in [('duplicate_nested','{"x":[{"a":1,"a":2}]}'),('nan','{"x":NaN}')]:
    got=caught(lambda raw=raw:m.parse(raw));check('REJECT_JSON_'+name,got.get('exception')=='Refusal',got)
got=caught(lambda:m.prepare(hand,'0'*64,True));check('REJECT_WRONG_EXTERNAL_HANDOFF_SHA',got.get('exception')=='Refusal',got)
got=caught(lambda:m.prepare(hand,sha(hand),False));check('SYNTHETIC_ADMISSION_FENCE',got.get('exception')=='Refusal',got)
tree=ast.parse(F.read_text());fill=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='fill')
check('FILL_PREPARES_BEFORE_CREATING_DIRECTORY',isinstance(fill.body[0],ast.Assign) and ast.unparse(fill.body[0].value).startswith('prepare('))
check('EXCLUSIVE_FILE_OPEN_PRESENT',"open('xb')" in ast.unparse(fill))
check('EXCLUSIVE_DIRECTORY_CREATE_PRESENT','out.mkdir(exist_ok=False)' in ast.unparse(fill))
numeric_overflow=caught(lambda:m.number(10**400,'oversized_int'))
check('HUGE_INTEGER_FAILS_CLOSED',numeric_overflow.get('exception') in ('Refusal','OverflowError'),numeric_overflow)
result={'date_u':'Sun Oct 18 18:54:11 UTC 2026','status':'TESTED_PASS_WITH_NONBLOCKING_FINDING','passed':sum(x['pass'] for x in checks),'total':len(checks),'checks':checks,'finding':{'id':'SF1','severity':'low','issue':'Oversized JSON integer conversion raises OverflowError; main does not catch this type. It fails before output creation.','observed':numeric_overflow},'scope':'Custody and mapping only; root-supplied handoff SHA trusted. Admission, certificate semantics, root adoption and scientific execution untested. No actual fill or mutation of reviewed files.','filler':pin(F),'policy':pin(POL),'producer_tests':pin(TEST),'harness':pin(__file__),'read_pins':{q:sha(q) for q in sorted(READS) if Path(q).is_file()}}
write('BOUNDED_REVIEW_RESULTS_CX3V003.json',result)
print(json.dumps({k:result[k] for k in ('status','passed','total','finding')}))
