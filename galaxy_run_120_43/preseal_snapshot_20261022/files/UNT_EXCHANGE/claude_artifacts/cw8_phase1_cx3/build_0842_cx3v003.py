"""0842/A281: immutable v003 delta; no scientific execution."""
import ast
import difflib
import hashlib
import json
from pathlib import Path
import subprocess

H = Path(__file__).parent
INPUTS, OUTPUTS = [], []
def pin(p):
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
def read(name, expected):
    p = H/name
    assert pin(p)['sha256'] == expected
    INPUTS.append(pin(p))
    return p.read_text()
def rep(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)
def write(name, text):
    ast.parse(text)
    p = H/name
    with p.open('x') as f:
        f.write(text)
    OUTPUTS.append(pin(p))
    return OUTPUTS[-1]
def functions(text):
    return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(text).body
            if isinstance(n, (ast.FunctionDef, ast.ClassDef))}

pold = read('phase1_ngc_launch_cx3cw8v002.py',
            '6de0d06a16a5ffab7b49bc76bc9219d0bfbd67a91020129677a5f4078846f852')
pnew = rep(pold, 'TOOL_NAME = "P112_LAUNCHER_CX3CW8V002"',
           'TOOL_NAME = "P112_LAUNCHER_CX3CW8V003"')
pnew = rep(pnew, 'import functools\n', 'import functools\nimport fcntl\n')
pnew = rep(pnew, '    need(record.get("spec", call["spec"]) == call["spec"], "CW8_ATTEMPT_RAW_SPEC")',
           '    spec = record.get("spec", call["spec"])\n'
           '    # S0 relaunches fill identical bytes under a fresh work directory.\n'
           '    need(is_pin(spec) and spec["sha256"] == call["spec"]["sha256"],\n'
           '         "CW8_ATTEMPT_RAW_SPEC")')
pnew = rep(pnew, '    record = read_pin(obj["comparator_record"])\n',
           '    record = read_pin(obj["comparator_record"])\n'
           '    need(type(record) is dict, "CW8_COMPARATOR_FORM")\n')
pnew = rep(pnew, '            forecast = read_pin(forecast_pin)\n',
           '            forecast = read_pin(forecast_pin)\n'
           '            need(type(forecast) is dict, "CW8_FORECAST_FORM")\n')
pnew = rep(pnew, '        except (Refusal, OSError, ValueError, KeyError, TypeError) as exc:\n',
           '        except (Refusal, OSError, ValueError, KeyError, TypeError,\n'
           '                AttributeError, OverflowError, RecursionError) as exc:\n')
lock = '''
def cw8_choice_lock(function):
    """Serialize choice discovery and exclusive publication on this launch root.

    The persistent empty lock inode is never replaced, truncated or removed.
    Lock acquisition precedes reading choices; a waiting Context must discard
    its cached call list before reconstructing the now-current durable roles.
    """
    @functools.wraps(function)
    def locked(ctx, *args, **kwargs):
        root = Path(ctx.cfg["p112_launch_root"])
        need(root.is_dir() and os.path.realpath(root) == str(root),
             "CW8_CHOICE_LOCK_ROOT")
        path = root / ".worker_choices.lock"
        path_rules(str(path), "worker choice lock")
        flags = os.O_RDONLY | os.O_NOFOLLOW
        try:
            fd = os.open(path, flags | os.O_CREAT | os.O_EXCL, 0o444)
        except FileExistsError:
            fd = os.open(path, flags)
        try:
            info = os.fstat(fd)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
                 "CW8_CHOICE_LOCK_FILE")
            fcntl.flock(fd, fcntl.LOCK_EX)
            current = os.stat(path, follow_symlinks=False)
            need((current.st_dev, current.st_ino) == (info.st_dev, info.st_ino),
                 "CW8_CHOICE_LOCK_IDENTITY")
            ctx._calls = None
            return function(ctx, *args, **kwargs)
        finally:
            os.close(fd)
    return locked

'''
pnew = rep(pnew, '\n@read_scope\ndef select_workers(', lock + '\n@read_scope\n@cw8_choice_lock\ndef select_workers(')
pf0, pf1 = functions(pold), functions(pnew)
changed = sorted(k for k in pf0 if pf0[k] != pf1[k])
added = sorted(set(pf1) - set(pf0))
assert changed == ['cw8_authenticate', 'cw8_check_attempt', 'select_workers'], changed
assert added == ['cw8_choice_lock']
lp = write('phase1_ngc_launch_cx3cw8v003.py', pnew)

bold = read('roster_builder_c2v007_cx3cw8v002.py',
            'a2d8dc00fd80322a2ba6822648c7399d46e9a4e55bbf309cd2efbc0e33665e7e')
bnew = rep(bold, "BUILDER_NAME = 'roster_builder_c2v007_cx3cw8v002'",
           "BUILDER_NAME = 'roster_builder_c2v007_cx3cw8v003'")
bnew = rep(bnew, "P112_REVIEWED_SHA = '6de0d06a16a5ffab7b49bc76bc9219d0bfbd67a91020129677a5f4078846f852'",
           'P112_REVIEWED_SHA = ' + repr(lp['sha256']))
bnew = rep(bnew,
           "            eligible = [item for item in all_seen if item['time_ns'] <= ceiling_ns]\n",
           "            eligible = [item for item in all_seen if item['time_ns'] <= ceiling_ns]\n"
           "            # A279/A281: a reporting cutoff cannot classify an unresolved\n"
           "            # solo model failure as a schedule ceiling. _receipt has\n"
           "            # already validated any cause_record against this monitor.\n"
           "            for item in eligible:\n"
           "                if (item['class'] == 'FAILED' and\n"
           "                        item['evidence'].get('solo_mode') is True and\n"
           "                        item['evidence'].get('cause_record') is None):\n"
           "                    raise Refused('SNAPSHOT_SOLO_FAILED_CAUSE_REQUIRED', call['name'])\n")
bf0, bf1 = functions(bold), functions(bnew)
assert sorted(k for k in bf0 if bf0[k] != bf1[k]) == ['phase1_snapshot']
bp = write('roster_builder_c2v007_cx3cw8v003.py', bnew)
gold = read('g26_freeze_cx3cw8v002.py',
            '332253d215387fa69822be3e96ec38c5bea5c4e6ffae4fabc53b0298ca312e2b')
gnew = rep(gold, str(H/'roster_builder_c2v007_cx3cw8v002.py'), bp['path'])
gnew = rep(gnew, 'a2d8dc00fd80322a2ba6822648c7399d46e9a4e55bbf309cd2efbc0e33665e7e', bp['sha256'])
assert functions(gold) == functions(gnew)
gp = write('g26_freeze_cx3cw8v003.py', gnew)
diffs = {}
for name, old, new in [('launcher', pold, pnew), ('builder', bold, bnew), ('G26', gold, gnew)]:
    diffs[name] = ''.join(difflib.unified_diff(old.splitlines(keepends=True),
        new.splitlines(keepends=True), fromfile=name+'_v002', tofile=name+'_v003'))
doc = {'date_u': subprocess.check_output(['/bin/date','-u'],text=True).strip(),
       'schema': 'CW8_0842_BUILD_CX3V003', 'inputs': INPUTS, 'outputs': OUTPUTS,
       'launcher_functions_changed': changed, 'launcher_functions_added': added,
       'builder_functions_changed': ['phase1_snapshot'],
       'G26_function_AST_unchanged': True, 'diffs': diffs,
       'tests': 'PENDING', 'scientific_execution': 'NONE'}
out = H/'BUILD_0842_CX3V003.json'
with out.open('x') as f:
    json.dump(doc,f,indent=2,sort_keys=True); f.write('\n')
print(json.dumps({'record': pin(out), 'outputs': OUTPUTS}))
