"""N2 exact durable refusal controls and isolated in-memory mutant; no launches."""
from pathlib import Path
import hashlib, sys
FIXTURE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/test_selector_cx3v003.py')
assert hashlib.sha256(FIXTURE.read_bytes()).hexdigest() == '39fa111c3e5e29f8fcd33f3d6e749da565fb51d2f542efb12e3f9994695af14b'
source = FIXTURE.read_text().split('\ncase("missing_license_automatic_serial"')[0]
# Preserve the fixture's source-relative paths while retaining its audit fence.
exec(compile(source, str(FIXTURE), 'exec'), dict()) if False else None
__file__ = str(FIXTURE)
exec(compile(source, str(FIXTURE), 'exec'), globals())
original = M.cw8_authenticate
segment = ast.get_source_segment(raw.decode(), next(n for n in ast.parse(raw).body if isinstance(n, ast.FunctionDef) and n.name == 'cw8_authenticate'))
needle = '    need(type(record) is dict, "CW8_COMPARATOR_FORM")'
assert segment.count(needle) == 1
mutant = segment.replace(needle, '    pass # isolated guard deletion')

def replace_license(f, value):
    rp = put(f.root / 'MALFORMED_COMPARATOR.json', value)
    lic = M.read_pin(f.license); lic['comparator_record'] = rp
    lp = put(f.root / 'LICENSE_SUCCESSOR.json', lic)
    text = f.ctx.v006_text.replace('CW8_LICENSE_PIN path=%s sha256=%s' % (f.license['path'], f.license['sha256']), 'CW8_LICENSE_PIN path=%s sha256=%s' % (lp['path'], lp['sha256']))
    vp = put(f.root / 'ROOT_SUCCESSOR.md', text.encode(), raw=True)
    cp = put(f.root / 'CONFIG_SUCCESSOR.json', dict(f.ctx.cfg, v006=vp['path']))
    f.config, f.ctx, f.license = cp, f.context(cp), lp
    return f

records = []
for label, value in [('null', None), ('empty_list', []), ('list', [1]), ('string', 'bad'), ('integer', 1), ('boolean', False)]:
    for mutated in (False, True):
        M.cw8_authenticate = original
        if mutated:
            exec(compile(mutant, '<isolated comparator guard mutant>', 'exec'), M.__dict__)
        f = replace_license(make_context(), value)
        result, record = choose(f)
        expected = 'AttributeError' if mutated else 'CW8_COMPARATOR_FORM'
        assert result['reason'] == record['prediction']['reason'] == expected, (label, result)
        assert result['column_workers'] == record['prediction']['column_workers'] == 1
        assert len(list(M.cw8_choice_directory(f.ctx).glob('CHOICE_*.json'))) == 1
        restored = f.context(f.config)
        assert all(M.cw8_workers(c) == 1 for c in restored.calls() if c['origin'] == 'P112')
        records.append(dict(case=label, mutant=mutated, reason=expected, exact_guard_detected=(expected != 'CW8_COMPARATOR_FORM') if mutated else None, status='PASS'))
M.cw8_authenticate = original
report = dict(schema='CW8_N2_EXACT_COMPARATOR_PROBE_CX1V001', tool=dict(path=str(TOOL), sha256=TOOL_SHA), checks=records, controls=6, mutants_detected=6, scientific_launches=0)
put(WORK / 'REPORT.json', report)
print(json.dumps(report, sort_keys=True))
