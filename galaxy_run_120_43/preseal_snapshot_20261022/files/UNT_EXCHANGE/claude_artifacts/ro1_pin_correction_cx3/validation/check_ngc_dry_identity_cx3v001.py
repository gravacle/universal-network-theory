"""Eight existing NGC source-readiness plans, comparing the A73 guard successor to r004."""
from pathlib import Path
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import resource
import subprocess
import sys
import time

BASE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
OLDROOT = BASE / 'ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative'
OLD = OLDROOT / 'galaxy_m0_forward_c2v011_cx3v005_cx3r004.py'
NEW = Path(sys.argv[1])
ROOT = Path(__file__).parent / 'NGC_DRY_V001'
ROOT.mkdir(exist_ok=False)
UTC = subprocess.check_output(['date', '-u'], text=True).strip()
START = time.monotonic()

def audit(event, args):
    if event in ('subprocess.Popen', 'os.system', 'os.posix_spawn', 'os.remove', 'os.rename', 'os.rmdir', 'socket.connect', 'socket.getaddrinfo'):
        raise RuntimeError('FORBIDDEN_' + event)
    if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
        p = Path(os.fsdecode(args[0])); resolved = str(p.resolve()).lower()
        if '/runs_ext/uvt_' in resolved or 'kmax_a2f10_c5h_run_v001' in resolved or '/.codex/' in resolved:
            raise RuntimeError('FORBIDDEN_PATH')
        if isinstance(args[2], int) and args[2] & (os.O_WRONLY | os.O_RDWR):
            if not p.resolve().is_relative_to(ROOT) or p.exists():
                raise RuntimeError('NONEXCLUSIVE_WRITE')

sys.addaudithook(audit)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def pin(p):
    return dict(path=str(p), sha256=sha(p))

def load(p, name):
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

assert sha(OLD) == '39c505175905576ff1029ede4be20be765ba47967b5a6eedf1298bd7c4305895'
old, new = load(OLD, 'ngc_old'), load(NEW, 'ngc_new')
registry = OLDROOT / 'SPEC_REGISTRY_V001.json'
reg = json.loads(registry.read_bytes())
assert len(reg['cases']) == 8

def dry(mod, sp, output):
    names = ('V011_PINS', 'GALAXIES', 'SCRIPTS_UVT', 'SCRIPTS', 'AUX_UVT', 'RO1_ROUTE_A', 'NODES_ROUTE_A', '_NGC_V011_ACTIVE')
    before = {k: getattr(mod, k) for k in names}
    cap = io.StringIO()
    with contextlib.redirect_stdout(cap), contextlib.redirect_stderr(cap):
        code = mod.cmd_dry_run(str(sp), str(output))
    ready = json.loads((output / 'NGC_SOURCE_BUILD_READINESS.json').read_bytes())
    assert code == 0 and ready['executed_stages'] == 0
    assert not ready['binding_blockers'] and len(ready['source_build_blockers']) == 2
    assert ready['readiness'] == 'PENDING_CERTIFICATES'
    assert all(getattr(mod, k) is v for k, v in before.items())
    return ready

def files(d):
    return {str(p.relative_to(d)): p.read_bytes() for p in d.rglob('*') if p.is_file()}

def replace(data, pairs):
    for a, b in pairs:
        data = data.replace(a.encode(), b.encode())
    return data

def compare(a, b):
    aa, bb = files(a), files(b)
    pairs = [(str(OLD), str(NEW)), (sha(OLD), sha(NEW)), (str(a), str(b))]
    assert aa.keys() == bb.keys() and aa
    for _ in range(12):
        added = []
        known = {x for x, _ in pairs}
        for k in aa:
            x, y = hashlib.sha256(aa[k]).hexdigest(), hashlib.sha256(bb[k]).hexdigest()
            if x != y and x not in known and replace(aa[k], pairs) == bb[k]:
                added.append((x, y)); known.add(x)
        pairs += added
        if not added:
            break
    short = pairs + [(x[:n], y[:n]) for x, y in pairs if len(x) == 64 and all(c in '0123456789abcdef' for c in x) for n in (16, 12)]
    differing = [k for k in aa if replace(aa[k], short if k.endswith('DRYRUN_PLAN.txt') else pairs) != bb[k]]
    return dict(files=len(aa), differing=differing, derived_hash_pairs=len(pairs)-3, identical=not differing)

cases = []
for i, case in enumerate(reg['cases']):
    sp = Path(case['spec']['path']); assert sha(sp) == case['spec']['sha256']
    a, b = ROOT / ('%02d_old' % i), ROOT / ('%02d_new' % i)
    dry(old, sp, a); dry(new, sp, b)
    cmp = compare(a, b)
    assert cmp['identical'], (case['case'], cmp)
    cases.append(dict(case=case['case'], status='TESTED_PASS', spec=pin(sp), comparison=cmp,
                      new_report=pin(b / 'DRYRUN_REPORT.json'), new_readiness=pin(b / 'NGC_SOURCE_BUILD_READINESS.json')))
    print(case['case'] + ' PASS_IDENTITY_0_STAGES', flush=True)
result = dict(date_u=UTC, status='TESTED_PASS', passed=len(cases), total=8,
              driver=pin(NEW), baseline=pin(OLD), registry=pin(registry), harness=pin(__file__), cases=cases,
              max_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              seconds=time.monotonic()-START,
              scope='Existing readiness fixtures only; no admitted-calibration or production prediction claim. Only self path/hash, output-root and derived hash substitutions are ignored.')
p = ROOT / 'RESULTS_V001.json'
with p.open('x') as f:
    json.dump(result, f, indent=2); f.write('\n')
print(json.dumps(dict(result=pin(p), passed=8, max_rss_bytes=result['max_rss_bytes'])), flush=True)
