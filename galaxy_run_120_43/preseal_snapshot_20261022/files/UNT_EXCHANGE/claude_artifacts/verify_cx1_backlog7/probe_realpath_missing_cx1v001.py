"""Distinct c3v003 review: preserve fixture-only writes and probe missing target components."""
from pathlib import Path
import hashlib
AUTHOR=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/roster_parent_check_c3/test_roster_parent_check_c3v007.py')
raw=AUTHOR.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='8b0e15c34bbdf40f9ef03621f20a2c8f28b55afd75f35d8966aaf293b65d9df5'
source=raw.decode()
# The author's K1 root case attempts mkdir through a symlink to /. Replace it
# with an explicitly inert read-only parent before executing; no writes outside WORK.
old="'dang_abs_readonly_root': lambda d: os.symlink('/nonexistent_c3p7_target', d + '/L'),"
new="'dang_abs_readonly_root': lambda d: (os.mkdir(d + '/local_readonly'), os.symlink(d + '/local_readonly/target', d + '/L'), os.chmod(d + '/local_readonly', 0o500), RO.append(Path(d + '/local_readonly'))),"
assert source.count(old)==1
source=source.replace(old,new)
exec(compile(source,str(AUTHOR)+':fixture-only-root-probe','exec'),globals())
probes=[]
for kind in ('missing','not_directory'):
    out,d,argv=step7_setup('review_target_component_'+kind)
    if kind=='not_directory': t.wbytes(str(d/'component'),b'inert')
    os.symlink('component/../made',d/'dangling')
    destination=str(d/'dangling')+'/'
    preflight=W.preflight(destination)
    answer=run(W.main,argv+[destination]);entries=ledger(out)[1]
    assert preflight is None
    assert answer[0]==1 and entries==['STEP7_0001.json'],answer
    assert not (d/'made').exists()
    probes.append({'case':kind,'preflight':preflight,'rc':answer[0],'stderr':answer[2],'ledger':entries})
record={'schema':'BACKLOG7_REALPATH_MISSING_COMPONENT_CX1V001','author_suite_passed':sum(x['pass'] for x in RESULTS),'author_suite_count':len(RESULTS),'reviewer_suite_adaptation':'K1 root write attempt replaced with inert read-only parent; same expected outcome','probes':probes,'scientific_launches':0}
jwrite(WORK/'REVIEW_PROBE.json',record)
print(json.dumps(record,sort_keys=True))
