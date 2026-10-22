"""Write-once A73 lane report and byte manifest."""
import hashlib
import json
from pathlib import Path

H=Path(__file__).resolve().parent;ART=H.parents[1];E=ART.parent
G6=ART/'tail_scheme_impl_c2/gates_v006';G5=ART/'tail_scheme_impl_c2/gates_v005'
DATE_U='Sun Oct 18 16:17:23 UTC 2026'
SRC=G6/'run_identity_compare_c2v006.py'
EXPECTED='097286d762dd171361e7ff5bbb98b3d48029e790de5869b28aa6218098491e48'
RESULT=H/'run_20261018T161641_81032/A73_RESULTS.json'
def pin(p):
    p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(p,o):
    raw=o.encode() if isinstance(o,str) else (json.dumps(o,indent=2,sort_keys=True)+'\n').encode()
    with Path(p).open('xb') as f:f.write(raw)
    return pin(p)
assert pin(SRC)['sha256']==EXPECTED
r=json.loads(RESULT.read_bytes());assert (r['passed'],r['total'])==(20,47) and not r['blocked_attempts']
items=[
 {'id':'SF1','presence':'ABSENT','status':'TESTED','requirement_counts':[4,8],
  'evidence':'check_ro1_armed and check_ro1_unarmed accept a valid six-field record extended with events_suppressed:2 or custom_payload. The inadmissible_record exception remains refused. RESULT delegates the new-only RO1 block to these incomplete checks.',
  'fix':'Require exactly the registered RO1 key set for each permitted form before removing the block from RESULT.'},
 {'id':'SF2','presence':'ABSENT','status':'TESTED','requirement_counts':[6,22],
  'evidence':'Supplied derived baselines pass policy for r4/r5 Z2, Z2_OFF_RO1 and B0P_RERUN. Adding an arbitrary verdict or numeric-string triple also passes tokens_policy and build_tokens. Mutated reference sides/token labels pass Z2 policy. Actual Side normalization equates CONVERGED/NOT_CONVERGED and 101.125/907.875 under those undeclared triples. main reads declared only, ignoring the token document driver metadata.',
  'fix':'Re-derive or pin the allowed complete triples for the selected driver and gate, rejecting extras, substitutions and wrong derivation identity. This is distinct from A71 post-join label injectivity.'},
 {'id':'SF3','presence':'ABSENT','status':'TESTED','requirement_counts':[2,4],
  'evidence':'With r5 selected, static_pin_verifier accepts a fresh arbitrary local binary file and an r4-only table pin when their hashes match. The selected r5 positive passes and a bad raw sha refuses. No selected table membership is checked.',
  'fix':'Check exact raw path/sha membership in the selected driver tables in addition to the byte hash.'},
 {'id':'N3','presence':'ABSENT_IN_INHERITED_FILL_NO_V006_SUCCESSOR','status':'TESTED','requirement_counts':[5,7],
  'evidence':'Fresh scratch /Users paths and their /System/Volumes/Data aliases name the same inode; inherited guarded_resolve permits the alias into the registered scratch directory. NFC and NFD scratch paths likewise name the same inode but NFD bypasses containment. Plain containment and marker controls refuse; a sibling is allowed. No actual forbidden run path is used.',
  'fix':'Provide a fill-tool successor with firmlink-aware filesystem identity and Unicode normalization in containment. Do not confuse existing marker protection with the missing generic containment requirement.'},
 {'id':'N6','presence':'PARTIAL_VERDICT_CHECK_PRESENT_RECEIPT_STATUS_ABSENT','status':'TESTED_SOURCE_ONLY','requirement_counts':[1,4],
  'evidence':'No R5_IDENTITY_COMPARE_COMMANDS.sh successor exists in gates_v006. The inherited gates_v005 script checks receipt existence only and finishes with cat after wait. The v006 identity-record writer checks comparator verdict for each gate, but captures receipt status/exit_code without using either in a predicate. BUILD requests FINISHED in prose; no executable status check was found.',
  'fix':'Supply a v006 r5 command successor that parses and requires the finished receipt status, checks command completion, and reads each resulting verdict. Preserve the existing writer verdict check.'}]
paths=[SRC,G6/'BUILD.md',G6/'DIFF_c2v005_c2v006.diff',G6/'tools/make_tokens_c2v006.py',
       G6/'tools/write_identity_records_c2v006.py',G5/'tools/fill_picard_member_c2v002.py',
       G5/'R5_IDENTITY_COMPARE_COMMANDS.sh',G5/'check/CHECK.md',H/'probe_a73_cx2v001.py',RESULT,
       E/'FROM_CODEX/0564_2026-10-18_codex2_crosslineage_review_comparator_c2v006.md',
       Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md')]
evidence=[pin(p) for p in paths]
summary_pin=write(H/'A73_PRESENCE_CX2V001.json',{'date_u':DATE_U,'verdict':'PASS_WITH_FINDINGS',
 'scope':'A73 should-fix presence/absence lane only, not whole comparator verdict. A73 permits a c2v007 successor if c2v006 lands without these items.',
 'requirement_predicates':{'passed':20,'total':47,'failed':27},'items':items,'evidence':evidence,
 'source_before':r['source_before'],'source_after':pin(SRC),'scientific_status':'UNTESTED','scientific_launches':0,
 'execution_note':'nice unavailable (sandbox);0514 waiver'})
doc='''# Comparator c2v006 — A73 presence/absence review

`date -u`: DATE_VALUE

**PASS_WITH_FINDINGS for this A73 lane.** SF1, SF2 and SF3 are absent. N3 remains absent from the inherited fill tool, with no v006 replacement. N6 is partial: comparator-verdict checking is present in the record writer, while executable receipt-status checking is absent. A73 expressly allows these should-fix changes in c2v007 if c2v006 lands without them. This is not an overall PASS for the comparator; the parent integrates the independent A71 findings.

**TESTED: 20/47 requirement predicates pass, 27 fail.** The failed predicates demonstrate the specified missing restrictions; they are not unexplained harness failures. Positive and negative controls are included. The candidate source matched the supplied sha before and after execution. No real run or production identity report was read. Scientific comparisons remain UNTESTED in this lane.

| A73 item | Presence | Evidence |
|---|---|---|
| SF1, full RO1 key set | Absent | Both armed and unarmed records accept extra events_suppressed/custom_payload keys. Exact valid records pass and inadmissible_record still refuses. |
| SF2, only driver-derived triples | Absent | r4/r5 policy accepts arbitrary verdict/numeric-string pairs for Z2, Z2_OFF_RO1 and B0P. Z2 reference/label substitutions also pass. Actual normalization erases those string differences. |
| SF3, selected driver static pins | Absent | With r5 selected, an arbitrary own file and an r4-only pin are admitted by matching bytes alone. |
| N3, firmlink/NFD containment | Absent in inherited fill | Both aliases name the registered scratch inode but pass the lexical containment guard. Plain and marker controls still refuse. |
| N6, receipt status and each verdict | Partial | No v006 command successor. Old command tests existence; v006 writer checks each comparator verdict but not receipt status/exit_code. |

SF1 is at check_ro1_armed/check_ro1_unarmed (source lines 1206–1217). Their named-value checks do not constrain the key set. The RESULT rules remove the new-only RO1 object as checked by RO1. Require the exact registered key set before that declaration can excuse the block.

SF2 is at tokens_policy (918–945), token loading (1331–1333) and the normalization chain. Policy verifies successor presence and excludes some inappropriate successor/base values, but does not establish that every complete [ref,new,label] triple belongs to the A59 derivation. The metadata in the token file is ignored by main. A fresh non-derived CONVERGED→NOT_CONVERGED pair and a numeric-string pair each pass policy and become equal under actual Side.norm. These are policy/normalizer unit probes; this lane does not claim a whole-gate false PASS. The separate A71 lane found post-join label non-injectivity; that is a distinct mechanism and is not counted again here. A selected-driver derivation allowlist must constrain all three columns and reject extras.

SF3 is at static_pin_verifier (1268–1276). The predicate only hashes the raw path stored in its reverse map. It never consults DRIVER or a table. The own arbitrary file and cross-driver pin probes confirm this directly. Hash validity is necessary but does not establish declared membership.

N3 belongs to the fill tool's generic containment layer, not the comparison Tree inventory. The bundle provides no fill successor; the inherited c2v002 guarded_resolve uses casefolded lexical containment. Scratch firmlink and NFC/NFD pairs were confirmed with os.path.samefile before probing. No actual C5H path was passed. Existing marker protection remains effective for a marker-bearing scratch path, so this is not evidence of a bypass of the real C5H marker restriction. A filesystem-identity/normalization-aware containment successor remains required.

N6 is a source-only inspection; neither the command script nor identity-record writer was executed. The old script checks -f on receipt files and ends with wait/cat. The v006 writer records status and exit_code but never predicates on them; it does explicitly reject comparator verdicts other than PASS_BITWISE_EQUAL. BUILD's request to wait for FINISHED is prose, not an executable status guard. The dispatch/A73 calls this N6; the original c2v005 CHECK labels the same command-script note N5 (its N6 is a port caveat). This numbering difference does not alter the requested fix.

All probes use fresh scratch fixtures or source-derived configuration tables. Imports were inspected and guarded. All production runs/runs_ext, C5H, NGC targets, session logs, production gates_v006 identity reports and R4 records were prohibited; no prohibited operation was attempted. No network, subprocess, solver, launch, deletion, rename or overwrite occurred. Python used the approved isolated interpreter with single-thread environment settings and the 0514 nice waiver. The open A73 addendum is cited at its observed bytes, not claimed frozen.

Files and SHA256 from bytes:

'''.replace('DATE_VALUE',DATE_U)
doc+=''.join('- `'+x['path']+'` — `'+x['sha256']+'`\n' for x in evidence+[summary_pin])
review_pin=write(H/'REVIEW_CX2V001.md',doc)
allpaths=sorted(set([x for x in H.rglob('*') if x.is_file()]+paths+[Path(x) for x in r['reads'] if Path(x).is_file()]),key=str)
manifest=write(H/'HASHES_CX2V001.txt',''.join(pin(x)['sha256']+'  '+str(x)+'\n' for x in allpaths))
for line in Path(manifest['path']).read_text().splitlines():
    sh,path=line.split('  ',1);assert pin(path)['sha256']==sh
assert pin(SRC)['sha256']==EXPECTED
print(json.dumps({'review':review_pin,'presence':summary_pin,'manifest':manifest,'entries_verified':len(allpaths)}))
