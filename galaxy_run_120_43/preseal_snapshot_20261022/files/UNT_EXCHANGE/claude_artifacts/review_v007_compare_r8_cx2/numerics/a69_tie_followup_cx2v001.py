"""Bounded A69 exact-tie control; preserves sealed prior evidence."""
import argparse, hashlib, importlib.util, json, os, sys
from pathlib import Path

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--date-u',required=True);a=ap.parse_args()
    base=Path(__file__).parent
    target=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/kmax_tail_compare_c2v007_r8.py')
    add=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md')
    expected='bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3';assert sha(target)==expected
    s=importlib.util.spec_from_file_location('tie_review_r8',target);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    hp=base/'synthetic_v001/synthetic_histories.json';hist=json.loads(hp.read_text())['uncapped_same_sign_hidden_by_fast_norm']
    ids=list(hist['adapted']['rows']);tau={i:1.0 for i in ids};ctx={'ids':ids,'tau':tau}
    e,c=m.picard_noise(hist,ids,tau);assert c is None
    # Equal total pair noise at first two ordered rows, but opposite preferred branches.
    A=[(.375-2*e[i])/2 if j<2 else 0.0 for j,i in enumerate(ids)]
    V={k:{'_uvt_info':{'E_A_rows_km_s':A}} for k in ('C4T','C6T')}
    n=m.pair_noise('C4T','C6T',{'C4T':hist,'C6T':hist},V,None,ctx)
    checks={'exact_tie':n['noise_over_tau'][ids[0]]==n['noise_over_tau'][ids[1]]==.375,
      'opposite_branch_preferences':n['EA_pair'][ids[0]]>n['E_pair'][ids[0]] and n['EA_pair'][ids[1]]<n['E_pair'][ids[1]],
      'lowest_ordered_row_selected':n['rpair_branch_row']==ids[0],
      'selected_route_a':n['rpair_branch']=='ROUTE_A','target_unchanged':sha(target)==expected}
    assert all(checks.values())
    refs=[target,add,hp,base/'NUMERICAL_REVIEW_CX2V001.md',base/'synthetic_v001/NUMERICAL_CANARIES_CX2V001.json',Path(__file__)]
    data={'date_u':a.date_u,'label':'TESTED_SYNTHETIC_ONLY','checks':checks,'passed':len(checks),'total':len(checks),'pair':n,'byte_pins':[{'path':str(p),'sha256':sha(p)} for p in refs],'scope_note':'Prior 85/85 scoped PASS remains numerical/R-PAIR only. Current open addendum A71 records the separate LO duplicate-shell finding and mandates a systematic duplicate audit in the next compare round. Overall compare verdict belongs to parent; no whole-program PASS or scientific adoption is asserted. A69 exact tie uses the lowest row in the registered ordered ids; this test uses synthetic ascending row indices.'}
    out=base/'A69_TIE_FOLLOWUP_CX2V001.json'
    with out.open('x') as f:json.dump(data,f,indent=2,sort_keys=True);f.write('\n')
    manifest=base/'HASHES_NUMERICAL_CX2V002.txt'
    files={str(p):sha(p) for p in base.rglob('*') if p.is_file()};files.update({str(p):sha(p) for p in refs})
    with manifest.open('x') as f:
        f.write('# date -u: '+a.date_u+'\n')
        for p,h in sorted(files.items()):f.write(h+'  '+p+'\n')
    assert all(sha(p)==h for p,h in files.items())
    print(json.dumps({'passed':len(checks),'total':len(checks),'followup_sha256':sha(out),'manifest_sha256':sha(manifest),'date_u':a.date_u,'addendum_sha256':sha(add)}))
if __name__=='__main__':main()
