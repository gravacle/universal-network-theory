"""Distinct reviewer: a trailing-slash dangling symlink with a valid target parent."""
from pathlib import Path
import hashlib
AUTHOR=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/roster_parent_check_c3/test_roster_parent_check_c3v005.py')
raw=AUTHOR.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='85bbd2cb449bee14def8485b3a167204a54282718ff791b219595653d3fb6176'
exec(compile(raw,str(AUTHOR),'exec'),globals())
out,d,argv=step7_setup('review_dangling_trailing_valid')
target=d/'new_target';link=d/'dangling';os.symlink(target,link)
destination=str(link)+'/'
wrapped=run(W.main,argv+[destination]);before=ledger(out)[1]
base_result=run(RB.main,argv+[destination]);after=ledger(out)[1]
assert wrapped[0]==2 and json.loads(wrapped[2])['refused']=='OUT_DIR_EXISTS'
assert before==[]
assert base_result[0]==0 and after==['STEP7_0001.json'],base_result
assert (target/'STEP7_RESULT.json').is_file()
record={'schema':'BACKLOG7_REVIEW_TRAILING_LINK_CX1V001','finding':'v002 rejects trailing dangling symlink even when unchanged base succeeds creating its target','wrapper':wrapped,'base':base_result,'ledger_before_base':before,'ledger_after_base':after,'scientific_launches':0}
jwrite(WORK/'REVIEW_PROBE.json',record)
print(json.dumps(record,sort_keys=True))
