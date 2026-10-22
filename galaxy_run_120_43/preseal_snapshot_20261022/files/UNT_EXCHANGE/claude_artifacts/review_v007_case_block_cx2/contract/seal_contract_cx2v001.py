import hashlib,json,subprocess
from pathlib import Path

date=subprocess.check_output(['/bin/date','-u'],text=True).strip()
h=Path(__file__).absolute().parent
b=(h/'CONTRACT_RESULTS_CX2V001.json').read_bytes()
assert hashlib.sha256(b).hexdigest()=='8095e3dcf10b721c4ad31edd6f0555aba18be0fdd518737e96c699bdc2d68f71'
r=json.loads(b)
mutations=sum(x['owner'].startswith('r12 structural slice: ') for x in r['checks'])
assert mutations==48
report='''# A99 case-block contract review

`date -u`: DATE.

**PASS — limited structural scope; 106/106 independent checks. No finding in this slice.** The published case block passes the retained r12 structural/content rules. This is not a full-validator, sealed-prereg, scientific-admission or launch-readiness verdict.

The candidate is `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json`, SHA256 `76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71`. The frozen comparison source is `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py`, SHA256 `4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28`. Both and all five explicit input files were byte-checked at start and end and remained unchanged.

## Tested contract

The candidate contains exactly ten T entries plus the legacy C5H declaration. T entries register whole `/numerics`, use the expected G2/G3/G4/G6 grids and S4T spherical exception, declare tail and RO1 true, and permit exactly the pinned r5 driver. Production P=128 and integer gas M_s=128 are present. KLO/KHI are 64/256; C5c has cube outer 5; C4T-A has lambda_scale 1.05. D5 uses nodes_v001 on G5, other T cases continuum_v001. Other tail settings agree across cases. Full RA4 brackets, pairwise numerics distinctness, and the five required tail-content/hash distinctions pass. Mode is parallel8 and key_equivalence_map is empty.

Independent static checks also confirm every T declaration has route-A workers 8, max_iterations 32, and the six-pass Picard block (0.01 km/s, observe every pass). These checks do not validate actual run behavior. The C5H entry is compared only against literal declarations in the permitted source: tail/RO1 false, G5, the registered spec hash and v009-EXT driver. Its protected source artifact or run is not opened.

The 106 checks comprise 45 candidate/custody/content observations, 48 owned structural mutation cases, four actual strict-JSON duplicate-key canaries, three explicit omitted-premise controls, three actual key-map application checks, and three final byte/guard/import checks. Mutations identify the owning rejection rather than merely observing a generic failure. Cases cover missing/extra labels, unknown keys, T raw-spec hash prohibition, missing whole numerics, grids/truncation, tail/RO1, drivers, legacy declarations, hash shape/required distinctions, P/M_s/type drift, KLO/KHI/outer/lambda/source rules, RA4, seed factor, mode and key-map shape/forbidden/duplicate pointers. Actual r12 duplicate-key parsing rejects equal and unequal repeated case names, nested `/numerics`, and repeated schema members.

## Exact execution boundary

The harness parses the pinned source AST and selects only named pure functions/constants. It retains `validate_case_block` through route-mode validation, removes the final C5H-reference comparison block, renames the resulting slice, and always passes `check_uv_link=False`. The excluded normalizer loader is a raising sentinel. Registered grids come directly from two pinned permitted prereg declarations. The active driver and legacy-spec hashes are source literals; no build activation or legacy loader executes. The original retained code is otherwise unchanged. The result records all selected functions, source line boundaries and a hash of the executed AST.

No full comparator or project module is imported, and no supplied builder/checker is executed. There are zero protected-path attempts. No run tree, target velocity, checkpoint, NPZ table or scientific producer is read or executed. Protected open/stat/lstat/readlink/listdir/scandir paths are guarded before source execution.

Three deliberate controls document this slice's limits: a syntactically valid but incorrect tail hash is admitted without normalization; a non-D5 worker drift is not owned by this block-level slice; an argument/block mode mismatch is owned by the CLI seal check, not this retained validator. Their expected admissions are not candidate acceptance claims. Likewise, key-map unit checks prove exact absent-equivalent dropping, wrong-value retention and no mutation of caller inputs, but the actual empty map requires no such equivalence.

**UNTESTED here:** actual uv_tail normalization and config hashes; ten filled-spec/dry-report/physical joins; D5 versus permitted legacy-reference equivalence; actual C5H run custody; full CLI/seal/registry/physical gates and runtime outputs. Other review lanes own the safe normalization and spec/reference joins. Those results must be combined explicitly, never inferred from this structural PASS.

## Evidence

- `CONTRACT_RESULTS_CX2V001.json`, SHA256 `8095e3dcf10b721c4ad31edd6f0555aba18be0fdd518737e96c699bdc2d68f71`.
- Builder report (claims only; not execution authority): `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/out/CASE_BLOCK_BUILD_C4V001.json`, SHA256 `bcf560de77cd42f67fedb62744df0723a052c1f2ffc4f4b2a7bed874eb5b59ad`.
- Grid declaration V005: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json`, SHA256 `dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174`.
- Grid declaration V006R1: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/v006_r1/prereg/KMAX_MATRIX_PREREG_V006_R1.json`, SHA256 `807fc5bfcb24ee779137746db3536f41dd97c16bd5f367f79ad5a1b8c3ec067c`.

The accompanying JSONL manifest lists all input and own-artifact paths with byte SHA256, and is verified by parsing its written bytes. Embedded prereg/report pointers are not followed.
'''.replace('DATE',date)
rp=h/'REVIEW_CONTRACT_CX2V001.md'
with rp.open('x') as f:f.write(report)
entries=list(r['input_pins'])
for name in ('check_contract_cx2v001.py','CONTRACT_RESULTS_CX2V001.json','REVIEW_CONTRACT_CX2V001.md','seal_contract_cx2v001.py'):
 p=h/name;entries.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'kind':'own_artifact'})
mp=h/'HASHES_CONTRACT_CX2V001.jsonl'
with mp.open('x') as f:
 for e in entries:
  e['date_u']=date;f.write(json.dumps(e,sort_keys=True)+'\n')
parsed=[json.loads(line) for line in mp.read_text().splitlines()]
assert len({e['path'] for e in parsed})==len(parsed)
for e in parsed:
 p=Path(e['path'])
 assert not any(v in p.parts for v in ('runs','runs_ext','.codex'))
 assert 'KMAX_A2F10_C5H_RUN_V001' not in str(p) and 'NGC3198' not in str(p) and '/c5h_hull_c2/' not in str(p)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256']
print(json.dumps({'date_u':date,'entries':len(parsed),'report_sha256':hashlib.sha256(rp.read_bytes()).hexdigest(),
                  'manifest_sha256':hashlib.sha256(mp.read_bytes()).hexdigest(),
                  'harness_sha256':hashlib.sha256((h/'check_contract_cx2v001.py').read_bytes()).hexdigest()}))
