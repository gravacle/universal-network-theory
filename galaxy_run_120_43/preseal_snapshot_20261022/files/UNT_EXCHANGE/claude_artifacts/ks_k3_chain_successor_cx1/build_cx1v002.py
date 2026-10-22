from pathlib import Path
import hashlib
D=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_successor_cx1')
c=(D/'s4rc1_common_ks3_cx1v001.py').read_bytes()
s=(D/'registry_assembler_ks4_cx1v001.py').read_text()
s=s.replace("COMMON_PATH = HERE + '/s4rc1_common_ks3_cx1v001.py'","COMMON_PATH = HERE + '/s4rc1_common_ks3_cx1v002.py'")
old="        for k in C1_REQUIRED_PINS:                                                                # L68\n            C.read_bytes_pinned(r[k], roots, 'C1 ' + k)"
new="        for k in C1_REQUIRED_PINS:                                                                # L68\n            if k != 'certificate_policy_review':  # A241: review read once below; parse its validated buffer\n                C.read_bytes_pinned(r[k], roots, 'C1 ' + k)"
assert s.count(old)==1;s=s.replace(old,new)
old="rv = C.read_json_pinned(r['certificate_policy_review'], roots, 'certificate policy review')"
new="rv = json.loads(C.read_bytes_pinned(r['certificate_policy_review'], roots, 'certificate policy review'))"
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace('# A240 / 0794: KS3 successor pin only; inherited policy logic unchanged.','# A241 / 0795: policy review parsed from its single hash-validated read; remaining logic unchanged.')
for name,b in [('s4rc1_common_ks3_cx1v002.py',c),('registry_assembler_ks4_cx1v002.py',s.encode()),('build_cx1v002.py',Path(__file__).read_bytes())]:
 with (D/name).open('xb') as f:f.write(b)
print(hashlib.sha256(s.encode()).hexdigest())
