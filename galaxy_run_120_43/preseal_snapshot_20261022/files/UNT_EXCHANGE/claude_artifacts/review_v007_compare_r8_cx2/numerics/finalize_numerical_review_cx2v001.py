"""Create immutable scoped review and SHA256 manifest from existing test evidence."""
import argparse, hashlib, json
from pathlib import Path

BASE=Path(__file__).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--date-u',required=True);a=ap.parse_args()
    evidence=BASE/'synthetic_v001/NUMERICAL_CANARIES_CX2V001.json';r=json.loads(evidence.read_text())
    assert r['pass'] and r['passed']==r['total']==85
    src=r['pins_before']; end=[]
    for s in src:
        p=Path(s['path']);end.append({'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size})
    assert end[0]['sha256']==src[0]['sha256']
    artifacts=sorted(p for p in BASE.rglob('*') if p.is_file())
    hashes={str(p):sha(p) for p in artifacts}
    summary={'schema':'UNT_CX2_R8_NUMERICAL_REVIEW_V001','date_u':a.date_u,'verdict':'PASS','scope':'Noise and R-PAIR numerical/protocol slice only','tested':'85/85 independent synthetic canaries','scientific_or_sealed_adoption':'UNTESTED','source_pins_at_test':src,'source_pins_at_review':end,'test_result':{'path':str(evidence),'sha256':sha(evidence)},'no_actionable_finding_in_scope':True,'limits':r['limits'],'not_executed':['supplied test module','build_context','main/full CLI','real record read','scientific solver','sealed/scientific adoption'],'open_V005_addendum_changed_since_test':src[7]['sha256']!=end[7]['sha256'],'latest_binding_reading':'A58 RI-18 supersedes capped wording retained in draft r2; A53 and R3-4 govern admitted PICARD route A.'}
    sp=BASE/'NUMERICAL_REVIEW_CX2V001.json'
    with sp.open('x') as f:json.dump(summary,f,indent=2,sort_keys=True);f.write('\n')
    hashes[str(sp)]=sha(sp)
    paragraphs=[
        '# Compare r8: independent noise and R-PAIR review',
        '',
        'date -u: `'+a.date_u+'`',
        '',
        '**PASS in the assigned numerical/R-PAIR slice. TESTED: 85/85 independent synthetic canaries.** No actionable false-pass finding was found in this slice. This is not the overall compare verdict and does not establish scientific or sealed adoption.',
        '',
        'The target is imported from its unchanged bytes. The suite never imports the supplied tests or invokes build_context; the supplied tests have real-record reads at module scope. All histories, run dictionaries and manifests are independently constructed. A Fraction oracle computes bounds from the represented synthetic row values, independently of the target implementation. There are no target monkeypatches.',
        '',
        'The applicable noise rule is the latest A58 RI-18 reading, overriding the cap still transcribed in draft r2: q/(1-q) without the 0.9 cap at norm level and for same-sign rows, q/(1+q) for alternating rows. Either of the last two norm ratios >= 1, or any last per-row ratio >= 1, makes E unavailable. Exactly one increment uses the norm directly. The geometric/contraction interpretation remains DECLARED; these finite histories verify code behavior, not a theorem about future iterates.',
        '',
        '| Area | Independent evidence |',
        '|---|---|',
        '| Uncapped arithmetic | q=31/32 norm case and a slow same-sign row hidden by a faster norm; both retain the larger bound. The latter forces R-PAIR. |',
        '| Alternating rows | A slow alternating row whose own bound dominates the norm; exact-rational oracle and sign-kind checked. |',
        '| Unavailable E | Both NEW-7 ratio positions, same-sign and alternating q_i=1, zero previous/nonzero last, no increment. |',
        '| Record problems | Pass gap, S9 sentinel, missing/nonfinite row and final-pass mismatch. Record defects do not become decidable. |',
        '| Pair selection | Inclusive tau/8 equality; next float above it; worst normalized row; EA-dominant ROUTE_A; exact tie PICARD; unavailable E forces PICARD. |',
        '| R-PAIR result | Missing pair pending; wrong branch or invalid member incomplete; still noisy member at iteration floor; member gap incomplete; member rows used after resolution. |',
        '| A53 inheritance | Base flags retained for PICARD, member-only flags not substituted; PICARD EA entry substitution rejected and base EA retained. |',
        '| RB_FP | Independent noise/kappa arithmetic; unavailable base triggers PICARD path; resolved members used; unresolved member or zero shell sum incomplete; ROUTE_A RB_FP manifest refused. |',
        '| R3-4/V6 | Actual case_validity accepts planning column_workers=1 with admitted parallel base record; rejects serial-record substitution, changed base result/identity, changed tail record and unregistered numerics; ROUTE_A cannot reuse base identity. |',
        '',
        'The R3-4 positive control explicitly asserts synthetic V4/V5 and I1T seams. It tests the actual case_validity R3-4/V6 code, but does not reconstruct a packet or certify I1T. Result/receipt dictionaries are synthetic adapter-layer fixtures; this suite does not prove real reader custody. The own manifests test manifest structure and RB_FP branch refusal; full CLI and complete global ADOPT_TAIL evaluation are UNTESTED by this slice.',
        '',
        'Source review additionally checked the evaluate_v007 caller: it derives member validity, compares registered R-PAIR leaves between members, invalidates contradictory PICARD EA entries and detects aliased result hashes. Untriggered members are refused before T-tests are evaluated. The RB_FP leaf relies on load_manifest to enforce its PICARD-only branch; the independent own-manifest negative verifies that boundary. These caller observations are STATIC REVIEW, not a full scientific execution.',
        '',
        'The run took %.6f s, peak RSS %d bytes, isolated Python -I -B, single-thread BLAS environment, default priority under the 0514 waiver. No scientific launches, external run/receipt reads, observed targets, network, or session logs. The late-pass floating-point floor on the first real 12-pass member remains UNTESTED; the observed-ratio contraction assumption remains DECLARED.'%(r['runtime_seconds'],r['peak_rss_bytes']),
        '',
        'The open V005 addendum is recorded by bytes at the test and final review; an append changes its hash and requires checking for newer relevant rulings. It is not represented as a frozen file. Its hash changed during this slice: **%s**.'%str(summary['open_V005_addendum_changed_since_test']),
        '',
        'Source byte pins (all cited source files):',
        '',
        '| File | SHA256 at final review |',
        '|---|---|',
    ]
    paragraphs += ['| `'+s['path']+'` | `'+s['sha256']+'` |' for s in end]
    paragraphs += ['', 'Artifact byte pins:', '', '| File | SHA256 |','|---|---|']
    paragraphs += ['| `'+p+'` | `'+h+'` |' for p,h in sorted(hashes.items())]
    paragraphs += ['', 'The companion HASHES_NUMERICAL_CX2V001.txt manifest includes this report and every local artifact. Its own hash is provided to the parent separately to avoid a self-reference.', '']
    md=BASE/'NUMERICAL_REVIEW_CX2V001.md'
    with md.open('x') as f:f.write('\n'.join(paragraphs))
    manifest=BASE/'HASHES_NUMERICAL_CX2V001.txt'
    allpins={s['path']:s['sha256'] for s in end}
    allpins.update({str(p):sha(p) for p in BASE.rglob('*') if p.is_file()})
    with manifest.open('x') as f:
        f.write('# date -u: '+a.date_u+'\n')
        for p,h in sorted(allpins.items()):f.write(h+'  '+p+'\n')
    assert all(sha(p)==h for p,h in allpins.items())
    print(json.dumps({'report':str(md),'report_sha256':sha(md),'summary_sha256':sha(sp),'manifest_sha256':sha(manifest),'manifest_entries':len(allpins),'target_sha256':end[0]['sha256'],'V005_sha256':end[7]['sha256'],'date_u':a.date_u}))
if __name__=='__main__':main()
