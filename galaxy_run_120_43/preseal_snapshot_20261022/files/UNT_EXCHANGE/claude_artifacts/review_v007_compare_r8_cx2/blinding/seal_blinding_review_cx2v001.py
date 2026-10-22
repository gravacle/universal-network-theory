"""Seal the independent 0558 blinding/priority lane, exclusive outputs only."""
import hashlib
import json
from pathlib import Path

H=Path(__file__).resolve().parent
E=H.parents[2]
DATE_U='Sun Oct 18 15:34:31 UTC 2026'
SOURCE=H.parents[1]/'v007_compare_c2/r8/kmax_tail_compare_c2v007_r8.py'
EXPECTED='bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3'
def pin(p):
    p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(p,o):
    raw=o.encode() if isinstance(o,str) else (json.dumps(o,indent=2,sort_keys=True)+'\n').encode()
    with Path(p).open('xb') as f:f.write(raw)
    return pin(p)
assert pin(SOURCE)['sha256']==EXPECTED
blinding=H/'run_20261018T153234_27448/BLINDING_RESULTS.json'
priority=H/'run_20261018T153337_32888/PRIORITY_RESULTS.json'
b=json.loads(blinding.read_bytes());p=json.loads(priority.read_bytes())
assert (b['passed'],b['total'],p['passed'],p['total'])==(37,43,43,43)
failed=[r for r in b['rows'] if not r['pass']]
assert len(failed)==6 and all('refusal suppresses numeric' in r['name'] for r in failed)
paths=[SOURCE,H/'probe_blinding_cx2v001.py',H/'probe_blinding_cx2v002.py',H/'probe_priority_cx2v001.py',
       H/'priority_support_cx2v001.py',blinding,priority,
       E/'FROM_CODEX/0558_2026-10-18_codex2_crosslineage_review_compare_r8.md',
       E/'claude_artifacts/v007_final_prereg_c4/r2/KMAX_TAIL_PREREG_V007_FINAL_DRAFT.json',
       E/'claude_artifacts/v007_final_prereg_c4/r2/CLAUSE_SOURCE_MAP.md',
       Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md'),
       Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'),
       SOURCE.parent/'FIELDS_R8.md',SOURCE.parent/'COMPARE_V007_IMPL_R8.md']
evidence=[pin(x) for x in paths]
finding={'id':'CX2-R8-BLIND-S1','severity':'SHOULD_FIX','status':'TESTED',
 'title':'Blinded-mode early refusal diagnostics emit arbitrary numeric input labels',
 'binding':'A54 S6 record-controlled label blinding; A47 I3 no row values printed/written',
 'trigger':'Unknown key v_73.246813579 in a fresh case block, manifest, or producer registry; both --validity-only and --gates-only.',
 'observed':'Each invocation returns2 and prints the canary verbatim to stderr. No report is produced and no decision/adoption is made.',
 'example':"REFUSED: unknown manifest keys ['v_73.246813579']",
 'cause':'validate_case_block, load_manifest and producer_registry_from_obj interpolate unknown-key lists; _main catches Refused and prints str(exc) before the success-path blinding formatter.',
 'recommendation':'In either blinded mode, emit fixed refusal codes or allowlisted/redacted diagnostic fields at the common CLI error boundary. Apply the same rule to every preflight refusal; keep detailed raw input labels out of stderr.',
 'impact_limit':'Synthetic input-label disclosure, not an observed scientific velocity disclosure and not an ADOPT_TAIL bypass. Successful report bodies passed the canaries.',
 'reproductions':[x['detail'] for x in failed]}
finding_pin=write(H/'FINDINGS_CX2V001.json',{'date_u':DATE_U,'verdict':'PASS_WITH_FINDINGS','findings':[finding],
    'source_before':b['source_before'],'source_after':pin(SOURCE)})
text='''# V007 compare r8: blinding and decision-priority review

`date -u`: DATE_VALUE

**PASS_WITH_FINDINGS — one should-fix blinding finding; no decision-order defect found in this lane.** Final controls: actual CLI blinding 37/43, isolated priority 43/43, total 80/86. The six failed expectations are one defect class across three malformed input types and two modes. The source matched the supplied byte pin before and after both suites. These are TESTED software checks; scientific acceptance and production inputs remain UNTESTED.

**CX2-R8-BLIND-S1 (SHOULD_FIX, TESTED): blinded refusal diagnostics disclose input labels.** A fresh synthetic key `v_73.246813579` placed in a case block, manifest or producer registry appears verbatim on stderr under both `--validity-only` and `--gates-only`. For example: `REFUSED: unknown manifest keys ['v_73.246813579']`. All six calls return 2 with no report. The loader/validator constructs the raw diagnostic and `_main` prints `str(exc)` before success-path redaction. This fails the A54 S6 record-label blinding requirement at the CLI error boundary. It demonstrates disclosure of an invented numeric label, not disclosure of a real scientific row and not an adoption bypass. Use fixed refusal codes or an allowlisted/redacted error formatter for every blinded-mode preflight refusal.

The actual CLI success paths passed six numeric-canary forms in invented failed records: decimal, trailing decimal point, long digit run, leading-dot decimal, exponent and signed decimal. No canary appeared in stdout/stderr. Six independently written RB_FP records were registered by exact record SHA and synthetic producer SHA; the actual gate reader returned PASS while suppressing their shell labels and numeric arrays. `--gates-only` successfully hashed invalid-JSON case bytes without parsing them or opening the case's start/finish files. Empty manifests produced blinded fail-closed reports with no numeric JSON values. The unsealed source refused operation without explicit test-mode permission. No source or preflight method was patched for these CLI probes; the tests called the actual `main(argv)` with captured stdout/stderr in the approved interpreter.

The synthetic case block was independently assembled from the specified static grids, RA4 block and permitted C5H prep normalization. It passed the complete actual case-block validator. No existing author's fixture or production run record was imported. C5H CALL spec, dry-run report and preserved REVIEW_V009 prep were read only as permitted by the parent; the actual C5H run tree and every runs/runs_ext tree were forbidden by the audit hook. Writes were exclusive and confined to this lane, with process/network operations blocked. No forbidden operation was attempted.

The priority suite first exercised an actual empty-manifest read/validation/decision path, which returned INCOMPLETE without reading tests. Its other decision worlds explicitly substituted synthetic upstream validity and test-producer outputs, while exercising the actual `evaluate_v007`, first-applicable ordering, alias checks, flags, pending/provisional bookkeeping and carried uncertainty aggregation. It covered invalid cases/identities, aliases, fired identity RO1, record defects, missing required gates, I4 failure, certificate classes, competing decided failures, both undecidable classes, unresolved R-PAIR/record gaps, uncomputed flags, MT flags, RERUN_ORDERED versus CLEARED, and adoption only after all supplied predicates were resolved. Earlier pending conditions correctly mark later decided failures PROVISIONAL. This is an isolated decision-machine test, not a full record-validator positive world. Full end-to-end ADOPT_TAIL admission, real certificates, sealed mode and scientific runs remain UNTESTED here.

The initial blinding harness used the generic PASS verdict for RB_FP; the actual parser correctly refused that unregistered verdict. Its immutable v002 successor uses the registered RB_FP verdict. The initial source and outputs are preserved and are not included in final pass counts. Candidate source bytes never changed. The open V005 addendum is hashed as observed at report time, not claimed frozen. The parent's other lanes own noise/R-PAIR, registry/admission and binding findings; this verdict covers only this lane.

Files and SHA256 from bytes:

'''.replace('DATE_VALUE',DATE_U)
text+=''.join('- `'+x['path']+'` — `'+x['sha256']+'`\n' for x in evidence+[finding_pin])
review_pin=write(H/'REVIEW_CX2V001.md',text)
summary_pin=write(H/'SUMMARY_CX2V001.json',{'date_u':DATE_U,'verdict':'PASS_WITH_FINDINGS',
 'final_counts':{'passed':80,'total':86,'blinding_passed':37,'blinding_total':43,'priority_passed':43,'priority_total':43},
 'findings':[finding_pin],'review':review_pin,'evidence':evidence,'source_before':b['source_before'],'source_after':pin(SOURCE),
 'actual_scientific_runs':0,'scientific_status':'UNTESTED','execution_note':'nice unavailable (sandbox);0514 waiver'})
files=sorted(set([x for x in H.rglob('*') if x.is_file()]+[x for x in paths if not x.is_relative_to(H)]),key=str)
manifest_pin=write(H/'HASHES_CX2V001.txt',''.join(pin(x)['sha256']+'  '+str(x)+'\n' for x in files))
for line in Path(manifest_pin['path']).read_text().splitlines():
    sh,path=line.split('  ',1);assert pin(path)['sha256']==sh
print(json.dumps({'review':review_pin,'summary':summary_pin,'findings':finding_pin,'manifest':manifest_pin,'entries_verified':len(files)}))
