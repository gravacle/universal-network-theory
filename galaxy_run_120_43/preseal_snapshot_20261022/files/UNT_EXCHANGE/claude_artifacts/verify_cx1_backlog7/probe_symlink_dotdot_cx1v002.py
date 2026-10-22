"""Distinct reviewer probe: symlink-plus-dotdot parent resolution through real CLI and ledger."""
from pathlib import Path
import hashlib
AUTHOR = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/roster_parent_check_c3/test_roster_parent_check_c3v003.py')
raw_author = AUTHOR.read_bytes()
assert hashlib.sha256(raw_author).hexdigest() == '0ea8ebafac3699685e641f8ba62984d292a6a69748e6e597f630bc6dab1ee599'
exec(compile(raw_author, str(AUTHOR), 'exec'), globals())
out, d, argv = step7_setup('review_symlink_dotdot')
(d / 'lexical').mkdir()
(d / 'actual').mkdir()
(d / 'actual' / 'deep').mkdir()
(d / 'actual' / 'only_actual').mkdir()
os.symlink(d / 'actual' / 'deep', d / 'lexical' / 'link')
destination = str(d / 'lexical' / 'link') + '/../only_actual/out'
wrapped = run(W.main, argv + [destination])
entries_before = ledger(out)[1]
base_answer = run(RB.main, argv + [destination])
entries_after = ledger(out)[1]
assert wrapped[0] == 2 and json.loads(wrapped[2])['refused'] == 'OUT_DIR_PARENT_MISSING'
assert entries_before == []
assert base_answer[0] == 0 and entries_after == ['STEP7_0001.json'], base_answer
assert (d / 'actual' / 'only_actual' / 'out' / 'STEP7_RESULT.json').is_file()
record = {'schema':'BACKLOG7_REVIEW_SYMLINK_DOTDOT_CX1V001','finding':'preflight refuses a valid base operation because abspath removes dotdot before resolving symlink', 'wrapper': {'rc':wrapped[0], 'stderr':wrapped[2]}, 'base':{'rc':base_answer[0],'stdout':base_answer[1]}, 'ledger_before_base':entries_before,'ledger_after_base':entries_after,'scientific_launches':0}
out2, d2, argv2 = step7_setup('review_symlink_dotdot_false_negative')
(d2 / 'lexical').mkdir()
(d2 / 'lexical' / 'only_lexical').mkdir()
(d2 / 'actual').mkdir()
(d2 / 'actual' / 'deep').mkdir()
os.symlink(d2 / 'actual' / 'deep', d2 / 'lexical' / 'link')
destination2 = str(d2 / 'lexical' / 'link') + '/../only_lexical/out'
answer2 = run(W.main, argv2 + [destination2])
entries2 = ledger(out2)[1]
assert answer2[0] == 1 and entries2 == ['STEP7_0001.json'], (answer2, entries2)
assert not (d2 / 'actual' / 'only_lexical').exists()
record['reverse_case'] = {'finding':'preflight admits nonexistent actual parent and permits ledger commit before mkdir fails','rc':answer2[0],'stderr':answer2[2],'ledger_entries':entries2}
jwrite(WORK / 'REVIEW_PROBE.json', record)
print(json.dumps(record,sort_keys=True))
