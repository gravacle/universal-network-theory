"""Root-only exposed-data arithmetic; no field/state/fit/producer execution."""
from pathlib import Path
import datetime
import hashlib
import json
import math
import os
import sys
import traceback

BASE = Path(__file__).resolve().parent
STEM = 'NGC3198_STATIONARY_LAPSE_SPAN_V001'
PROTOCOL_SHA = '242c5f8f5f38b476bb3d348f2721a7f71dcc27c231b5164b3b5e1f49ef26de65'
EPS, CP_KMS, TOL = 1e-6, 299792.458, 5e-13
INCLINATIONS = (70, 73, 76)
SPEED_ARMS = ('nominal', 'lower', 'upper')
STAGES = ('AUTH', 'READOUT')
PINS = {
 '../ngc3198_sparc_excerpt_v001.txt': '58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900',
 '../NGC3198_OBSERVATION_INFERENCE_AUDIT_V001.md': '7c0ee068178438cc3c970fef21c96f5165ed00719efe12fd909556cf8f97dd2b',
 'GALAXY_INPUT_READINESS.md': '6e23d981e7bf0450a1e51169d29a9d54b6f2d1e4fd014432255988e018e0ec6c',
 'CONSTRAINED_U_CLOCK_GRADIENT_COMOVING_CLUSTERING_BUDGET_V001.md': '04574291aa7fa464456ec5bbae1ff590a6addaa21cf18889503298b89a506f96',
 'CONSTRAINED_U_GALAXY_WORLDTUBE_AND_STATIC_BOUNDARY_DISCRIMINATOR_V002.md': 'a7598cc79c7e3bdaa83ad31f32826e7cf439b0f28c6f79fda9a09ea98c5ab90b'}
SEALS, CREATED = {}, {}
SOURCE_SHA = MANIFEST_SHA = None

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def finite(value):
    if type(value) is dict:
        require(all(type(k) is str for k in value), 'Native string keys')
        for v in value.values():
            finite(v)
    elif type(value) is list:
        for v in value:
            finite(v)
    else:
        require(type(value) in (str, int, float, bool), 'Native JSON scalar')
        require(type(value) is not float or math.isfinite(value), 'Finite JSON scalar')

def canonical(value):
    finite(value)
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()

def read(path):
    value = json.loads(Path(path).read_text())
    require(Path(path).read_bytes() == canonical(value), 'Canonical immutable JSON '+str(path))
    return value

def write(name, value):
    data = canonical(value)
    path = BASE/name
    with path.open('xb') as stream:
        stream.write(data)
    path.chmod(0o444)
    CREATED[str(path)] = sha(path)
    return CREATED[str(path)]

def authenticate():
    for name, digest in dict(PINS, **{STEM+'.md': PROTOCOL_SHA}).items():
        path = (BASE/name).resolve()
        require(path.is_relative_to(BASE.parent) and not (BASE/name).is_symlink(), 'Owned regular input')
        require(sha(path) == digest, 'Input bytes '+name)
        SEALS[str(path)] = digest

def recheck():
    require(sha(__file__) == SOURCE_SHA, 'Frozen own source')
    for name, digest in dict(SEALS, **CREATED).items():
        require(sha(name) == digest, 'Unchanged input/output '+name)

def source_rows():
    rows = []
    raw = (BASE/'../ngc3198_sparc_excerpt_v001.txt').read_text()
    for line in raw.splitlines():
        if line.startswith('#') or not line.strip():
            continue
        tokens = line.split()
        require(len(tokens) == 10 and tokens[0] == 'NGC3198', 'Full observed column schema')
        values = [float(x) for x in tokens[1:]]
        require(all(math.isfinite(x) for x in values), 'Finite original values')
        require(values[0] == 13.8 and values[1] > 0 and values[2] >= 0 and values[3] >= 0, 'Observed source convention')
        rows.append(dict(index=len(rows)+1, tokens=tokens, values=values))
    require(len(rows) == 43 and rows[0]['values'][1] == .32 and rows[-1]['values'][1] == 44.08, 'All43 exposed rows')
    require(all(a['values'][1] < b['values'][1] for a,b in zip(rows,rows[1:])), 'Ordered radii')
    return rows

def relative(error, terms):
    return abs(error)/(math.fsum(abs(x) for x in terms)+1e-300)

def screen(rows):
    widths = [math.log(b['values'][1]/a['values'][1]) for a,b in zip(rows,rows[1:])]
    band = .5*math.log1p(EPS)
    arms, maxima = [], [0., 0., 0., 0.]
    for inclination in INCLINATIONS:
        factor = math.sin(math.radians(73))/math.sin(math.radians(inclination))
        for speed_arm in SPEED_ARMS:
            speeds, signed_lower = [], []
            for row in rows:
                v, e = row['values'][2:4]
                signed_lower.append((v-e)*factor)
                base_speed = v if speed_arm == 'nominal' else max(0.,v-e) if speed_arm == 'lower' else v+e
                speeds.append(base_speed*factor)
            panels = []
            for index,(dx,u,v) in enumerate(zip(widths,speeds,speeds[1:])):
                linear = dx*(u*u+u*v+v*v)/(3*CP_KMS**2)
                trapezoid = dx*(u*u+v*v)/(2*CP_KMS**2)
                nodes = (.5-.5/math.sqrt(3), .5+.5/math.sqrt(3))
                gauss = dx*.5*math.fsum(((1-t)*u+t*v)**2 for t in nodes)/CP_KMS**2
                difference = dx*(u-v)**2/(6*CP_KMS**2)
                maxima[0] = max(maxima[0],relative(linear-gauss,[linear,gauss]))
                maxima[1] = max(maxima[1],relative(trapezoid-linear-difference,[trapezoid,linear,difference]))
                panels.append(dict(left_row=index+1,right_row=index+2,delta_log_radius=dx,
                    speed_left_kms=u,speed_right_kms=v,linear_v_span=linear,linear_v2_span=trapezoid,
                    independent_gauss_span=gauss,interpolation_difference=difference))
            spans = [math.fsum(p[k] for p in panels) for k in ('linear_v_span','linear_v2_span')]
            arms.append(dict(inclination_deg=inclination,speed_arm=speed_arm,deprojection_factor=factor,
                speeds_kms=speeds,raw_signed_lower_kms=signed_lower,panels=panels,
                schemes=[dict(name=name,span=s,span_over_width=s/band,
                    conditional_stationary_band_compatible=bool(s < band),eps_required=math.expm1(2*s))
                    for name,s in zip(('linear_v_logr','linear_v2_logr'),spans)]))
    for arm in arms:
        reference = next(x for x in arms if x['inclination_deg'] == 73 and x['speed_arm'] == arm['speed_arm'])
        for a,b in zip(arm['schemes'],reference['schemes']):
            scaled = b['span']*arm['deprojection_factor']**2
            maxima[2] = max(maxima[2],relative(a['span']-scaled,[a['span'],scaled]))
    constant = 100.**2*math.fsum(widths)/CP_KMS**2
    direct = 100.**2*math.log(rows[-1]['values'][1]/rows[0]['values'][1])/CP_KMS**2
    maxima[3] = relative(constant-direct,[constant,direct])
    controls = [dict(name=name,error=e,tolerance=TOL,passed=bool(math.isfinite(e) and e <= TOL))
        for name,e in zip(('exact_linear_v_vs_gauss2','interpolation_difference_identity',
                          'shared_inclination_square_scaling','constant_speed_log_span'),maxima)]
    return dict(rows=rows,arms=arms,controls=controls,width=band,eps=EPS,cp_kms=CP_KMS,
        observational_confidence_qualified=False,galaxy_solution_qualified=False,
        model_wide_exclusion_qualified=False,physical_parameter_changed=False)

def journal(event, epoch, **extra):
    row = dict(event=event,owner='root',pid=os.getpid(),epoch=epoch,source_sha256=SOURCE_SHA,
               manifest_sha256=MANIFEST_SHA,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**extra)
    path = BASE/(STEM+'_JOURNAL.jsonl')
    with path.open('ab') as stream:
        stream.write(canonical(row))

def checkpoint(stage, data, epoch):
    name = STEM+'_'+stage+'_CP.json'
    payload = dict(stage=stage,owner='root',pid=os.getpid(),epoch=epoch,source_sha256=SOURCE_SHA,
                   manifest_sha256=MANIFEST_SHA,data=data)
    digest = write(name,payload)
    commit_name = STEM+'_'+stage+'_COMMIT.json'
    commit_sha = write(commit_name,dict(stage=stage,owner='root',pid=os.getpid(),epoch=epoch,
        source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,payload=name,payload_sha256=digest))
    journal('CHECKPOINT',epoch,stage=stage,payload=name,payload_sha256=digest,
            commit=commit_name,commit_sha256=commit_sha)

def validate(manifest, auth, complete=False):
    path = BASE/(STEM+'_JOURNAL.jsonl')
    require(path.exists(), 'Manifest requires owner journal')
    events = [json.loads(line) for line in path.read_text().splitlines()]
    require(path.read_bytes() == b''.join(canonical(e) for e in events), 'Entire canonical journal')
    require(events and events[0]['event'] == 'OWNER_START', 'Original root epoch')
    prefix, epoch, pid, data = [], 0, 0, []
    for position,e in enumerate(events):
        finite(e)
        require(e['owner'] == 'root' and e['source_sha256'] == SOURCE_SHA and
                e['manifest_sha256'] == MANIFEST_SHA, 'Entire owner/source binding')
        require(type(e['pid']) is int and e['pid'] > 0 and type(e['epoch']) is int, 'Root PID and epoch')
        if e['event'] in ('OWNER_START','OWNER_RESUME'):
            require(e['epoch'] == epoch+1, 'Consecutive ownership epochs')
            epoch,pid = e['epoch'],e['pid']
            continue
        require(e['epoch'] == epoch and e['pid'] == pid, 'Latest owner PID epoch')
        if e['event'] == 'OWNER_COMPLETE':
            require(complete and position == len(events)-1 and prefix == list(STAGES), 'Exact terminal closure')
            require(e['result_sha256'] == sha(BASE/(STEM+'_RESULT.json')), 'Terminal result bytes')
            continue
        require(e['event'] == 'CHECKPOINT' and len(prefix) < 2 and e['stage'] == STAGES[len(prefix)], 'Exact2-stage prefix; refuse failure')
        pn,cn = STEM+'_'+e['stage']+'_CP.json',STEM+'_'+e['stage']+'_COMMIT.json'
        require(e['payload'] == pn and e['commit'] == cn and sha(BASE/pn) == e['payload_sha256']
                and sha(BASE/cn) == e['commit_sha256'], 'Full pair byte binding')
        p,c = read(BASE/pn),read(BASE/cn)
        expected = dict(stage=e['stage'],owner='root',pid=pid,epoch=epoch,
                        source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA)
        require(set(p) == set(expected)|{'data'} and all(p[k] == v for k,v in expected.items()), 'Entire finite payload identity')
        require(c == dict(expected,payload=pn,payload_sha256=e['payload_sha256']), 'Entire commit identity')
        if e['stage'] == 'AUTH':
            require(p['data'] == auth, 'All original rows and fixed controls')
        else:
            v = p['data']
            require(set(v) == {'rows','arms','controls','width','eps','cp_kms','observational_confidence_qualified',
                    'galaxy_solution_qualified','model_wide_exclusion_qualified','physical_parameter_changed'}, 'Complete readout schema')
            require(v['rows'] == auth['rows'] and len(v['arms']) == 9 and len(v['controls']) == 4,
                    'Full original rows/arm/control census')
            for arm,(i,s) in zip(v['arms'],[(i,s) for i in INCLINATIONS for s in SPEED_ARMS]):
                require(arm['inclination_deg'] == i and arm['speed_arm'] == s and len(arm['panels']) == 42
                        and len(arm['speeds_kms']) == len(arm['raw_signed_lower_kms']) == 43
                        and len(arm['schemes']) == 2, 'Full ordered panels and both schemes')
            require(v['eps'] == EPS and v['cp_kms'] == CP_KMS and all(x['tolerance'] == TOL for x in v['controls']), 'Unchanged fixed controls')
            require([x['name'] for x in v['controls']] == ['exact_linear_v_vs_gauss2','interpolation_difference_identity',
                    'shared_inclination_square_scaling','constant_speed_log_span'] and
                    all(type(x['passed']) is bool for x in v['controls']), 'Exact ordered four dispositions')
            require(all(v[k] is False for k in ('observational_confidence_qualified','galaxy_solution_qualified',
                    'model_wide_exclusion_qualified','physical_parameter_changed')), 'Retain physical scope refusals')
        CREATED[str(BASE/pn)],CREATED[str(BASE/cn)] = e['payload_sha256'],e['commit_sha256']
        prefix.append(e['stage']);data.append(p['data'])
    actual = {p.name for p in BASE.glob(STEM+'_*') if p.name.endswith(('_CP.json','_COMMIT.json'))}
    require(actual == {STEM+'_'+s+t for s in prefix for t in ('_CP.json','_COMMIT.json')}, 'No orphan pair')
    require(not complete or events[-1]['event'] == 'OWNER_COMPLETE', 'Closed root journal')
    return prefix,data,epoch

def main():
    global SOURCE_SHA,MANIFEST_SHA
    require(sys.argv[1:] == ['--root-owned'], 'Explicit root-owned launch only')
    SOURCE_SHA = sha(__file__)
    authenticate();rows = source_rows()
    auth = dict(rows=rows,eps=EPS,cp_kms=CP_KMS,inclinations=list(INCLINATIONS),speed_arms=list(SPEED_ARMS),tolerance=TOL)
    manifest = dict(source_sha256=SOURCE_SHA,input_sha256=SEALS.copy(),owner='root',stages=list(STAGES),fixed=auth)
    mp = BASE/(STEM+'_MANIFEST.json')
    require(not (BASE/(STEM+'_ERROR.json')).exists(), 'Preserved failed attempt requires disjoint version')
    if mp.exists():
        require(read(mp) == manifest, 'Identical recovery manifest')
        MANIFEST_SHA=sha(mp);CREATED[str(mp)]=MANIFEST_SHA
        if (BASE/(STEM+'_RECEIPT.json')).exists():
            receipt=read(BASE/(STEM+'_RECEIPT.json'))
            require(receipt['source_sha256'] == SOURCE_SHA and receipt['input_sha256'] == SEALS, 'Complete receipt lineage')
            require(receipt['manifest_sha256'] == MANIFEST_SHA and receipt['journal_sha256'] == sha(BASE/(STEM+'_JOURNAL.jsonl'))
                    and receipt['result_sha256'] == sha(BASE/(STEM+'_RESULT.json')), 'Complete publication hashes')
            expected_outputs={str(BASE/(STEM+t)) for t in ('_MANIFEST.json','_JOURNAL.jsonl','_RESULT.json','_REPORT.md')}
            expected_outputs|={str(BASE/(STEM+'_'+s+t)) for s in STAGES for t in ('_CP.json','_COMMIT.json')}
            require(set(receipt['output_sha256']) == expected_outputs, 'Exact8 sealed outputs plus receipt')
            for name,digest in receipt['output_sha256'].items():
                require(sha(name) == digest, 'Complete saved output bytes')
            validate(manifest,auth,complete=True)
            require(read(BASE/(STEM+'_RESULT.json'))['readout'] == read(BASE/(STEM+'_READOUT_CP.json'))['data'], 'Full result closure')
            recheck();print(receipt['status']);return
        require(not (BASE/(STEM+'_RESULT.json')).exists() and not (BASE/(STEM+'_REPORT.md')).exists(), 'No partial publication')
        prefix,data,epoch=validate(manifest,auth);epoch+=1;journal('OWNER_RESUME',epoch)
    else:
        require(not list(BASE.glob(STEM+'_*')), 'Refuse every pre-manifest orphan')
        MANIFEST_SHA=write(STEM+'_MANIFEST.json',manifest);prefix,data,epoch=[],[],1
        journal('OWNER_START',epoch)
    if not prefix:
        checkpoint('AUTH',auth,epoch);prefix.append('AUTH')
    readout=data[-1] if len(prefix) == 2 else screen(rows)
    if len(prefix) == 1:
        checkpoint('READOUT',readout,epoch)
    validate(manifest,auth)
    status='PASS' if all(x['passed'] for x in readout['controls']) else 'NUMERICAL_FAIL'
    recheck()
    result=dict(status=status,manifest=manifest,readout=readout,
                arithmetic_qualified=bool(status == 'PASS'),observational_confidence_qualified=False)
    digest=write(STEM+'_RESULT.json',result)
    report=['# NGC3198 conditional stationary lapse screen V001', '',
            'Arithmetic '+status+'. Exposed development data; no observational confidence or whole-model verdict.',
            'All43 rows retained; static geodesic/central-minimum/smooth symmetric phase and interpolation premises apply.',
            'eps remains '+str(EPS)+'; required eps is a necessary diagnostic and is never adopted.', '',
            '| inclination | speed arm | interpolation | span/width | conditional compatible | required eps |',
            '|---|---|---|---|---|---|']
    for arm in readout['arms']:
        for s in arm['schemes']:
            report.append('|'+str(arm['inclination_deg'])+'|'+arm['speed_arm']+'|'+s['name']+'|'+
                format(s['span_over_width'],'.12g')+'|'+str(s['conditional_stationary_band_compatible'])+'|'+format(s['eps_required'],'.12g')+'|')
    path=BASE/(STEM+'_REPORT.md')
    with path.open('xb') as stream:stream.write(('\n'.join(report)+'\n').encode())
    path.chmod(0o444);CREATED[str(path)]=sha(path)
    journal('OWNER_COMPLETE',epoch,result_sha256=digest,status=status)
    validate(manifest,auth,complete=True)
    jp=BASE/(STEM+'_JOURNAL.jsonl');jp.chmod(0o444);CREATED[str(jp)]=sha(jp)
    recheck()
    write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=SOURCE_SHA,input_sha256=SEALS,
          output_sha256=CREATED.copy(),manifest_sha256=MANIFEST_SHA,journal_sha256=sha(jp),result_sha256=digest))
    recheck();print(status)
    if status != 'PASS':raise SystemExit(3)

if __name__ == '__main__':
    try:
        main()
    except Exception:
        if SOURCE_SHA is not None and not (BASE/(STEM+'_ERROR.json')).exists():
            write(STEM+'_ERROR.json',dict(source_sha256=SOURCE_SHA,input_sha256=SEALS,
                  created=CREATED.copy(),owner='root',pid=os.getpid(),traceback=traceback.format_exc()))
        raise
