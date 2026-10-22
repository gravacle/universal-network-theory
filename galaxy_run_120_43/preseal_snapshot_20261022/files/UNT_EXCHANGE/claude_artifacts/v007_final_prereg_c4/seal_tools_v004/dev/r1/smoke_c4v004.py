# Claude4 seal tools v004 dev smoke check (work copy, not of record): the new manual-disclosures functions of the dev tool 4 on root's
# real file (read only) and on in-memory variants. Writes nothing. Run inside tools/run_fenced_c4st2.py.
import hashlib, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import seal_common_c4v003 as C
import build_seal_record_c4v004 as T4

ROOT_MD = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/root_inputs/SEAL_MANUAL_DISCLOSURES_V001.json')
ROOT_MD_SHA = 'b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6'
SEL = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json')
raw = ROOT_MD.read_bytes()
assert hashlib.sha256(raw).hexdigest() == ROOT_MD_SHA
sel = C.strict_json_bytes(SEL.read_bytes())
print('E_R6_1 equals SELECTED:', T4.E_R6_1 == sel['basis']['erratum_E_R6_1'])
chk = C.Checker('smoke')
md = T4.manual_disclosures_codes(chk, (str(ROOT_MD), ROOT_MD_SHA))
print('root file:', chk.result()['verdict'], [f['code'] for f in chk.failures], [n['code'] for n in chk.notes])
rec = T4.manual_disclosures_record(chk, md)
print('record value: raw_text == file text', rec['raw_text'] == raw.decode('utf-8'), 'content keys', sorted(rec['content']), 'pin', rec['pin'])
obj = json.loads(raw)


def form(mut):
    d = json.loads(raw)
    mut(d)
    c = C.Checker('smoke')
    T4.manual_disclosures_form_codes(c, d)
    return [f['code'] for f in c.failures]
print('extra key', form(lambda d: d.update(x=1)))
print('one char', form(lambda d: d.update(e_r6_1_text=d['e_r6_1_text'][:-1] + '!')))
print('empty e', form(lambda d: d.update(e_r6_1_text='')))
print('line 0', form(lambda d: d['c08_table'][0].update(line=0)))
print('line bool', form(lambda d: d['c08_table'][0].update(line=True)))
print('no declared', form(lambda d: [r.pop('declared_in_r13') for r in d['c08_table']]))
print('dup c08', form(lambda d: d['c08_table'].append(dict(d['c08_table'][0]))))
print('dup root id', form(lambda d: d['root_disclosures'].append(dict(d['root_disclosures'][0]))))
print('surrogate', form(lambda d: d.update(c08_confirmation='x \ud800 y')))
print('rd empty', form(lambda d: d.update(root_disclosures=[])))
