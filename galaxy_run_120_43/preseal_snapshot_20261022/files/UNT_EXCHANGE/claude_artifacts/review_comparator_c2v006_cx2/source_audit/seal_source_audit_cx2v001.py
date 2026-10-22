"""Independent AST conversion-site inventory and immutable review finalizer."""
import argparse,ast,hashlib,json
from pathlib import Path
HERE=Path(__file__).parent
ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
TARGET=ART/'tail_scheme_impl_c2/gates_v006/run_identity_compare_c2v006.py'
PIN='097286d762dd171361e7ff5bbb98b3d48029e790de5869b28aa6218098491e48'
ADD=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o):
    with p.open('x') as f:json.dump(o,f,indent=2,sort_keys=True);f.write('\n')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--date-u',required=True);a=ap.parse_args()
    raw=TARGET.read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN
    tree=ast.parse(raw);parents={c:n for n in ast.walk(tree) for c in ast.iter_child_nodes(n)}
    def scope(n):
        names=[]
        while n in parents:
            n=parents[n]
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):names.append(n.name)
        return '.'.join(reversed(names)) or '<module>'
    def disposition(line,sc,kind):
        if sc=='_npy_header':return 'FAIL_B1_NPY_HEADER_DUPLICATES','ast.literal_eval collapses duplicate raw header keys before the parsed mapping and NumPy decoder; actual full-gate counterexamples.'
        if sc=='build_tokens':return 'PARTIAL_FAIL_B2_AND_S1','Raw relation conflicts are guarded, but identical input triples are set-deduplicated and joined label serialization is not injective.'
        if line==1425:return 'FAIL_B3_LEDGER_GROUP_COLLISION','Unguarded (directory, token, kind) grouping; final-newline regex alias overwrites and removes both raw paths from inventory.'
        if sc in ('_pairs','npz_identity_bytes','_ev'):return 'GUARDED','Explicit membership guard before key insertion; NPZ raw names/logical keys retained until duplicate validation.'
        if sc.startswith('Store.'):return 'CACHE_OR_HASH_ACCOUNTING','Path cache keys; first hash retained by setdefault and changed hash recorded unstable. Repeated reads do not silently replace the first content digest.'
        if sc=='cm_read':return 'STRICT_PARSED_DICTIONARY_UPDATE','Strict object_pairs_hook first; payload_sha256 temporarily removed/restored for canonical integrity.'
        if sc=='driver_tables':return 'PINNED_CODE_ENV_OR_KEY_PRESERVING_PROJECTION','Sequential top-level assignments model the pinned source environment, not duplicate records. Table projection preserves keys from _ev guarded dictionaries.'
        if sc.startswith('StrictArgv.'):return 'MULTIMAP_NO_VALUE_DISCARD','All values retained in lists per flag; consulted repeated flags return Dup and record LAST_WINS. No list-to-scalar last-wins.'
        if sc.startswith('Tree.'):return 'GUARDED_OR_COPY','Stage names/numbers collected as multimaps then duplicates excluded and flagged; canonical inventory checks duplicate key before insertion; inventory() copies that mapping.'
        if sc=='Side.__init__':return 'MULTIMAP_AND_KEY_PRESERVING_PROJECTIONS','SHA-to-token and inverse collections retain all values; hash-map many-to-one flagged except declared NPZ equivalence. Sorted token join is derived metadata, not a raw-record overwrite.'
        if sc=='Side.s':return 'COUNTER','Token fired counts aggregate occurrences; not a record selection.'
        if sc=='Side.norm':return 'GUARDED_NORMALIZED_KEYS','Each dict key is normalized and collision checked before insertion; Collided sentinel and NORM_INJECTIVE flag retained.'
        if sc in ('caller_norm','check_requests','apply_declared','check_declared_off'):return 'COPY_OR_FIXED_SCHEMA_PROJECTION','Copies strictly parsed input maps or fixed named fields; declared masking/updates are explicit comparison rules, not duplicate-record conversion.'
        if sc in ('tokens_policy','check_custody'):return 'SET_OR_MULTIMAP_POLICY_VIEW','Membership/projection or multimap over token relations; token duplicate/join defects owned by build_tokens. A73 derivation-admission issue is a separate lane.'
        if sc=='ra_new_pins':return 'GUARDED_NORMALIZED_KEYS','Normalized route-A pin keys checked before insertion; collisions append LAST_WINS and Collided.'
        if sc=='static_pin_verifier':return 'EMPTY_REVERSE_MAP_FACTORY','Caller populates reverse map with explicit normalized-key guard. A73 allowed-producer policy is separate.'
        if line in (1616,1618):return 'GUARDED_NORMALIZED_KEYS','static_pins normalized key collision guard preceding insertion; a third collision can raise, which main turns into FAIL.'
        if line in (1569,1582,1585,1589):return 'GUARDED_STAGE_RECORDS','Ordered names must equal unique stage/request names; repeated known name explicitly rejected; strict object fields projected without key change.'
        if sc.startswith('_compare'):
            if line in (1511,1512):return 'INJECTIVE_KEY_PROJECTION','Fixed prefix removed from already unique inventory keys; suffix operation is injective.'
            return 'FIXED_SCHEMA_OR_UNIQUE_INDEX','Remaining maps key by fixed unique check/stage/group names or preserve existing map keys; inspected against guarded Tree inventory and fixed internal labels. Ledger exception is separately listed.'
        if sc in ('auto_custody','expected_tail_blocks','check_manifest_stage','ro1_expectations'):return 'FIXED_FIELDS_OR_UNIQUE_STAGES','Fixed schema fields and per-stage maps from guarded Tree.stages; no raw record list key discarded.'
        if sc=='main.put':return 'INTERNAL_CHECK_REGISTRY','Fixed internal check names; inspected call sites use unique names except exception recovery only fills missing strictness checks.'
        if sc.startswith('main') or sc=='_strict_puts':return 'FIXED_REPORT_OR_STATE_FIELDS','Report and configuration updates use fixed internal fields; not arbitrary record list conversion.'
        if sc=='<module>':return 'FIXED_SOURCE_CONSTANTS','Constant tables checked independently for repeated literal keys; none found.'
        return 'NO_INGESTION_OVERWRITE_FOUND','Inspected source operation is copy/projection or fixed state/report update; retained in inventory for review.'
    sites=[];literal_dups=[];literal_count=0
    for n in ast.walk(tree):
        kinds=[]
        if isinstance(n,ast.DictComp):kinds.append('DictComp')
        if isinstance(n,ast.SetComp):kinds.append('SetComp_membership_or_dedup')
        if isinstance(n,ast.Dict):
            literal_count+=1;seen={}
            for k in n.keys:
                if k is None:continue
                try:value=ast.literal_eval(k);hash(value)
                except Exception:continue
                if value in seen:literal_dups.append({'line':n.lineno,'key':repr(value),'first_key_line':seen[value],'second_key_line':k.lineno})
                seen[value]=k.lineno
            if any(k is None or not isinstance(k,ast.Constant) for k in n.keys):kinds.append('dynamic_or_unpack_dict_literal')
        if isinstance(n,ast.Call):
            if isinstance(n.func,ast.Name) and n.func.id=='dict':kinds.append('dict_constructor')
            if isinstance(n.func,ast.Attribute) and n.func.attr in ('setdefault','update','literal_eval'):kinds.append(n.func.attr)
        if isinstance(n,(ast.Assign,ast.AnnAssign,ast.AugAssign)):
            tg=n.targets if isinstance(n,ast.Assign) else [n.target]
            if any(isinstance(x,ast.Subscript) for t in tg for x in ast.walk(t)):kinds.append('subscript_assignment')
        for kind in kinds:
            sc=scope(n);status,why=disposition(n.lineno,sc,kind)
            sites.append({'line':n.lineno,'end_line':getattr(n,'end_lineno',n.lineno),'scope':sc,'kind':kind,'source':ast.get_source_segment(raw.decode(),n)[:350],'assessment':status,'reason':why})
    sites.sort(key=lambda x:(x['line'],x['kind']))
    assert not literal_dups
    records=json.loads((HERE/'probes_v001/RESULTS_CX2V001.json').read_text());ledger=json.loads((HERE/'ledger_v001/RESULTS_LEDGER_CX2V001.json').read_text())
    refs=[TARGET,ART/'tail_scheme_impl_c2/gates_v006/BUILD.md',ART/'tail_scheme_impl_c2/gates_v006/DIFF_c2v005_c2v006.diff',ADD,
      Path('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0564_2026-10-18_codex2_crosslineage_review_comparator_c2v006.md'),
      ART/'resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py',ART/'review_comparator_c2v005_cx2/invocation/invocation_canaries_cx2v003.py',
      HERE/'probe_a71_store_cx2v001.py',HERE/'probe_ledger_alias_cx2v001.py',HERE/'probes_v001/RESULTS_CX2V001.json',HERE/'ledger_v001/RESULTS_LEDGER_CX2V001.json',Path(__file__)]
    refs += [Path(x['report']['path']) for x in records['rows']+ledger['rows']]
    pins=[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in refs]
    inv={'date_u':a.date_u,'status':'STATIC_SOURCE_REVIEW','target_sha256':PIN,'method':'Independent AST sweep of every DictComp, dict constructor, dynamic/unpack dict, set comprehension, setdefault/update/literal_eval call and subscript assignment; manual source review grouped by function and line. No BUILD site list used to generate inventory.','site_count':len(sites),'all_dict_literal_count':literal_count,'duplicate_constant_dict_keys':literal_dups,'sites':sites,'external_decode_review':'Pinned checkpoint module _decode list-of-pairs rejects duplicate string keys before assignment and refuses structured/object dtypes.','limits':'This is a finite source audit with explicit site coverage, not a formal proof. Fixed report assignments and list-index mutations are overincluded for completeness.'}
    ip=HERE/'CONVERSION_INVENTORY_CX2V001.json';write(ip,inv)
    findings=[
      {'id':'CX2-V6-B1','severity':'BLOCKING','title':'Duplicate NPY header keys are last-wins','location':'_npy_header:212','evidence':['F01_npy_duplicate_descr','F02_npz_member_duplicate_shape','F03_npy_duplicate_equal_fortran'],'owner_should_fail':'STRICT_PARSE (and optionally NO_LAST_WINS)','fix':'Parse the header AST without evaluating mappings first; recursively reject duplicate dict keys and malformed schema/types before ast.literal_eval/NumPy read_array. Retain both entry positions/values in diagnostics.','limit':'Malformed header acceptance is TESTED; occurrence in production files UNTESTED.'},
      {'id':'CX2-V6-B2','severity':'BLOCKING','title':'Joined token labels are not injective','location':'build_tokens:708-709','evidence':['F06_joined_label_alias_changes_result'],'owner_should_fail':'NORM_INJECTIVE','fix':'Use an injective structured representation for label sets or a fresh opaque identifier; reject duplicate final normalized tokens across distinct raw pairs after joining. A73 derived-triple admission remains separately necessary.','limit':'Actual changed result value hidden under supplied synthetic tokens; no claim that registered production token files contain this pattern.'},
      {'id':'CX2-V6-B3','severity':'BLOCKING','title':'Attempt-ledger newline aliases overwrite and disappear from inventory','location':'ATTEMPT_RE:83 and _compare:1425','evidence':['F02_ledger_newline_alias_hides_change','F03_equal_duplicate_ledger_alias'],'owner_should_fail':'NO_LAST_WINS/ATTEMPT_LEDGER/INVENTORY','fix':'Use fullmatch or absolute end anchor; independently reject a repeated (directory,token,kind) before assigning or removing inventory entries, naming both raw paths. Preserve all raw paths for inventory/coverage accounting.','limit':'Synthetic ledger under a compared reference-stage tree; same grouping code handles route-A ledgers. No production incidence tested.'},
      {'id':'CX2-V6-S1','severity':'SHOULD_FIX','title':'Identical declared token triples silently deduplicate','location':'build_tokens:695-698','evidence':['F05_duplicate_exact_declared_token'],'owner_should_fail':'NO_LAST_WINS or token parse/policy','fix':'Reject repeated raw declared entries before set aggregation, including equal-valued repeats; distinguish declared-source duplicates from intentional provenance merging of auto/declared relation entries.','limit':'A71 duplicate acceptance; the reproduced unused duplicate alone does not change a scientific value.'},
    ]
    fp=HERE/'FINDINGS_SOURCE_CX2V001.json';write(fp,{'date_u':a.date_u,'verdict':'FAIL','target_sha256':PIN,'findings':findings,'source_pins':pins,'inventory':{'path':str(ip),'sha256':sha(ip)}})
    lines=['# c2v006 independent A71 and Store audit — FAIL','', '`date -u`: '+a.date_u,'',
      '**FAIL: three TESTED blocking classes remain, plus one A71 should-fix.** All 13 whole-gate executions used fresh synthetic B0P/r5 trees and the unchanged target bytes. Seven negative executions unexpectedly returned PASS_BITWISE_EQUAL with every check passing. Three positive baselines passed; ordinary array, result and ledger changes failed solely on STAGES, RESULT and ATTEMPT_LEDGER respectively. The 18 unit observations confirm mechanisms and cache/hash behavior; finding observations are not correctness passes.','',
      '1. **Duplicate NPY header keys (B1).** `_npy_header` calls ast.literal_eval before checking the header. Duplicate descr, shape or fortran_order keys collapse to the final entry. Standalone NPY and NPY-inside-NPZ whole-gate controls pass, including unequal and equal duplicates; STRICT_PARSE and NO_LAST_WINS remain true. Guard the header AST before any mapping is built.','',
      '2. **Joined token-label alias (B2).** Distinct pairs receive the same final token: one literal label `<X>|<Y>` versus two labels `<X>` and `<Y>` joined with `|`. The original label-to-pair check misses the collision after joining. REF scientific_probe=cx2_left0 and NEW scientific_probe=cx2_right1 compare equal under these distinct pairs; all checks pass. Without tokens, the same value change fails RESULT. Validate injectivity after construction or use structured/opaque identifiers. This is separate from the A73 requirement to admit only driver-derived triples.','',
      '3. **Attempt-ledger alias (B3).** ATTEMPT_RE ends in `$`, which matches before a terminal newline. `cx2token.start.json` and `cx2token.start.json\\n` map to the same captured directory/token/kind. The latter silently overwrites the former, and both raw paths have already been popped from inventory. A tampered value 900 in the ordinary NEW file is hidden by value 1 in the newline file; REF contains only ordinary value 1. ATTEMPT_LEDGER, INVENTORY, NO_LAST_WINS and COVERAGE all pass. Use fullmatch/absolute end and an explicit grouping-key duplicate guard before removing any raw file.','',
      '4. **Repeated equal token triples (S1).** Identical declared triples silently collapse in set accumulators. The whole gate passes with NO_LAST_WINS true. A71 requires duplicate rejection even when values agree. This unused-duplicate control is a strictness violation, not by itself a changed scientific-value demonstration.','',
      'Independent conversion inventory: **%d candidate sites**, plus all **%d dict literals** checked for duplicate constant keys (none found). The inventory was generated from the complete AST, not the BUILD list. It includes dict comprehensions/constructors, dynamic/unpack literals, set comprehensions, setdefault/update/literal_eval and all subscript assignments; fixed report/state/list-index operations are deliberately overincluded. Every site has its source location, enclosing scope and assessment.'%(len(sites),literal_count),'',
      'Guarded paths reviewed: strict JSON object pairs; NPZ central-directory/member names and logical keys; driver AST dict keys; stage directory names/numbers and canonical inventory keys; normalized object and pin keys; stage_records; argv multimaps. Injective fixed-prefix inventory projections and dictionary copies preserve keys. Pinned checkpoint decode rejects repeated list-of-pairs keys. The missing header guard, token aggregation/final join and attempt-ledger grouping are identified separately. This is a finite source audit, not a formal completeness proof.','',
      'Store checks: JSON duplicates are rejected, NPY/NPZ array objects are cached, their recorded SHA is from the parsed bytes, stable rehashes pass, synthetic changed end hashes fail verification, and intermediate hash changes are retained in unstable. End-hash fault injection changed an in-memory function temporarily and restored it; no file was overwritten. Source review confirms module/driver exec uses the verified byte buffer. JSONL/raw/scan paths can read again: their digests are recorded against the first digest; the literal blanket claim “every file read once” should be understood with that implementation qualification. No new consistency bypass was found in this bounded Store slice.','',
      'Hygiene: audit guards installed before target/helper imports; isolated prescribed Python -I -B, NumPy/stdlib, one-thread environment, default priority under 0514 waiver. Source and synthetic fixtures only. No production runs, UVT/C5H reports/receipts, NGC targets, network, solver, scientific launch, logs, deletion, move, rename or overwrite. The existing own fixture writer was imported from pinned bytes; no supplied c2v006 checker was imported or run. Scientific identity and production incidence are UNTESTED. A73 SF1/SF2/SF3/N3/N6 are owned by the parallel review lane.','',
      'Whole-gate owner checks:','', '| Case | Expected owner | Actual verdict | Actual failing checks |','|---|---|---|---|']
    for x in records['rows']:
        lines.append('| '+x['name']+' | '+str(x['owner'] or 'positive control')+' | '+x['actual']+' | '+(', '.join(x['failing']) or 'none')+' |')
    for x in ledger['rows']:
        own='positive control' if x['case'].startswith('P') else ('ATTEMPT_LEDGER' if x['case'].startswith('C') else 'NO_LAST_WINS / ATTEMPT_LEDGER / INVENTORY')
        lines.append('| '+x['case']+' | '+own+' | '+x['verdict']+' | '+(', '.join(x['failing']) or 'none')+' |')
    lines += ['', 'Every cited source and evidence file, SHA256 from bytes:','', '| File | SHA256 |','|---|---|']
    pins+= [{'path':str(ip),'sha256':sha(ip)},{'path':str(fp),'sha256':sha(fp)}]
    lines += ['| `'+p['path']+'` | `'+p['sha256']+'` |' for p in pins]
    lines += ['','The manifest additionally hashes all small synthetic fixture files. Open V005 addendum hashes are observations of mutable bytes, not seal pins.','']
    md=HERE/'REVIEW_SOURCE_CX2V001.md'
    with md.open('x') as f:f.write('\n'.join(lines))
    manifest={p['path']:p['sha256'] for p in pins};manifest.update({str(p):sha(p) for p in HERE.rglob('*') if p.is_file()})
    mp=HERE/'HASHES_SOURCE_CX2V001.txt'
    with mp.open('x') as f:
        f.write('# date -u: '+a.date_u+'\n')
        for p,h in sorted(manifest.items()):f.write(h+'  '+p+'\n')
    assert sha(TARGET)==PIN
    assert all(sha(p)==h for p,h in manifest.items())
    print(json.dumps({'verdict':'FAIL','candidate_sites':len(sites),'dict_literals':literal_count,'report_sha256':sha(md),'findings_sha256':sha(fp),'inventory_sha256':sha(ip),'manifest_sha256':sha(mp),'entries':len(manifest),'date_u':a.date_u}))
if __name__=='__main__':main()
