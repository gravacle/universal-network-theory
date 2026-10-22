"""Emit reviewed-lane v006 r2 candidate config successors from byte-pinned R1 snapshots.
No launches. Output directory must already exist; files are exclusive-create.
"""
from pathlib import Path
import argparse,hashlib,json
PINS = {64: {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/RUN_CONFIG_DDO154_CX2V006_KB064_R1.json', 'sha256': '4a645dbf28d64bfd7a55e87958bded9a3c1c0741c80d154823813287c88f03b3'}, 128: {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/RUN_CONFIG_DDO154_CX2V006_KB128_R1.json', 'sha256': 'e73cfa08b95d15a3478754bea984a4c42ce1d9a1c37a55efd206d3c1b9f8a021'}}
def main():
 p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True);a=p.parse_args()
 out=Path(a.output_dir)
 for kb,pin in PINS.items():
  raw=Path(pin['path']).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=pin['sha256']:raise ValueError('R1 config pin mismatch')
  c=json.loads(raw);r=c['tail_readiness']
  r.update(custody_deriver=None,state_enumerator=None,certificate_policy_review=None,
           approved_certificate_producers=[],post_state_verifier='ENFORCED_FAIL_CLOSED_REVIEWED_ADAPTERS_AND_PROOFS_PENDING')
  c['per_call']['rss_cap_bytes']=64*1024**3
  c['notes']+=' v006r3 adapter: certificate preflight/ingest/cache gates enforced; missing reviewed proof producers and state enumerator halt. Proposed RSS ceiling64GiB requires Claude2 ratification; no full-call measurement.'
  target=out/('RUN_CONFIG_DDO154_CX2V006_KB%03d_R2.json'%kb)
  with target.open('x') as f:json.dump(c,f,sort_keys=True,indent=1);f.write('\n')
 print('Created two R2 candidate configs; no launches')
if __name__=='__main__':main()
