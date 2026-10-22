"""Seal independent LO review; exclusively creates new reports."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

OUT = Path(__file__).parent
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p): return {'path': str(p), 'sha256': sha(p)}
def read(name): return json.loads((OUT/name).read_text())
def write(name, obj):
    with (OUT/name).open('x') as f:
        json.dump(obj, f, indent=2, sort_keys=True, allow_nan=False); f.write('\n')

date_u = sys.argv[1]
utc = datetime.now(timezone.utc).isoformat()
names = ['LO_STATIC_REVIEW_V001.json', 'LO_RHO_REVIEW_V001.json',
         'LO_INTEGRAL_COARSE_V001.json', 'LO_INTEGRAL_REFINED_V001.json',
         'LO_CONSUMER_GATE_REVIEW_V002.json']
static, rho, coarse, refined, gate = [read(n) for n in names]
convergence = abs(coarse['B1']/refined['B1']-1)
independent_ratio = refined['max_over_tau_using_certificate_rho'] * rho['own_search']['maximum']/rho['certificate_rho']
assert static['passed'] == 39 and static['total'] == 40
assert gate['passed'] == gate['total'] == 5
assert coarse['numeric_pass'] and refined['numeric_pass']
assert convergence < 1e-4 and refined['B1_relative_difference'] < 1e-4
assert independent_ratio < .005
record = static['record']
assert sha(record['path']) == record['sha256']
cert = json.loads(Path(record['path']).read_text())
assert 'source_gas_M_s' not in cert
findings = [{
    'id': 'CX3-0552-LO-1', 'severity': 'BLOCKER',
    'type': 'CERTIFICATE_REQUIRED_FIELD_MISSING', 'status': 'TESTED',
    'owner': 'Claude2 certificate producer and scientific launch owner',
    'condition': 'Original LO_CERT_V003_MS128 has gas_M_s=128 but lacks the required source_gas_M_s integer. Actual pinned r8 LO gate raises FIELD_MISSING:LO:source_gas_M_s.',
    'deciding_step': 'Produce an immutable LO certificate successor declaring source_gas_M_s=128, preserving and pinning the measured source and numerical evidence; revalidate actual consumer admission and repin downstream certificate inputs. An in-memory diagnostic field addition is not that successor.'}]
decision = {
    'date_u': date_u, 'utc': utc, 'verdict': 'FAIL',
    'reason': 'Required LO consumer field absent from reviewed original certificate.',
    'numerical_subreview': 'PASS_WITH_LIMITATIONS',
    'original_certificate_admission': 'TESTED_FAIL_REQUIRED_FIELD',
    'record': record, 'consumer_snapshot_version': gate['consumer'],
    'static_checks': {'passed': static['passed'], 'total': static['total'], 'sole_failed_check': 'required_source_gas_M_s_field'},
    'gate_expectation_checks': {'passed': gate['passed'], 'total': gate['total']},
    'source_gas_M_s_measured': 128, 'source_roster_digest': static['source_roster_digest'],
    'independent_shell': [128.0, 256.0], 'coarse_B1': coarse['B1'], 'refined_B1': refined['B1'],
    'certificate_B1': refined['certificate_B1'], 'coarse_refined_relative_change': convergence,
    'refined_certificate_B1_relative_difference': refined['B1_relative_difference'],
    'own_rho': rho['own_search']['maximum'], 'certificate_rho': rho['certificate_rho'],
    'independent_max_over_tau': independent_ratio, 'shell_tolerance': .005,
    'all10_record_shell_max': static['numeric_shell_max'], 'all10_record_sum': static['summed_max_over_tau'],
    'all10_sum_tolerance': .05, 'coverage_endpoint_inverse_kpc': 363.0,
    'required_P128_endpoint_inverse_kpc': 362.03867196751236,
    'limitations': [
        'Only the (128,256] shell integral is independently recomputed; all ten declared shell arithmetic and tolerances are rechecked.',
        'Shared continuum source implementation and production symbol definitions; independent radial factor representation, quadrature, endpoint handling, binding/search, and gate harness.',
        'Rho remains a sampled/local numerical maximum and B1 a quadrature estimate. No interval or global supremum proof.',
        'This LO review does not independently rerun the recorded I1-T or audit the full comparison engine, GQ, r5, or NGC.',
        'Consumer source changed externally during review. The executed fragment is preserved with its exact byte hash and time; no claim is made about a later consumer version.',
        'In-memory synthetic source_gas_M_s=128 gate acceptance is a diagnostic only, not an adopted production record.'
    ], 'findings': findings, 'evidence': [pin(OUT/n) for n in names],
    'peak_rss_bytes': max(x.get('peak_rss_bytes', 0) for x in (static,rho,coarse,refined)),
    'scientific_launches': 0, 'real_NGC_targets_opened': False, 'forbidden_runs_opened': False}
write('REVIEW_DECISION_CX3V001.json', decision)
write('TYPED_BLOCKERS_CX3V001.json', {'date_u': date_u, 'findings': findings, 'decision': pin(OUT/'REVIEW_DECISION_CX3V001.json')})

citations = [record, gate['consumer'], cert['producer'], cert['common'],
             *[pin(OUT/n) for n in names], pin(OUT/'LO_CONSUMER_FRAGMENT_SNAPSHOT_V002.json'),
             pin(OUT/'REVIEW_DECISION_CX3V001.json'), pin(OUT/'TYPED_BLOCKERS_CX3V001.json'),
             pin(OUT/'review_lo_ms128_cx3v001.py'), pin(OUT/'review_lo_consumer_fragment_cx3v002.py'), pin(__file__)]
report = f'''# Codex3 LO certificates_v003 cross-lineage review

{date_u}

Verdict: **FAIL** for the original LO record's required admission metadata. Numerical subreview: **PASS_WITH_LIMITATIONS**. No launch authority is conveyed.

The reviewed original record has `gas_M_s: 128` but lacks the distinct required integer `source_gas_M_s`. The actual r8 `g_LO` fragment raises `FIELD_MISSING:LO:source_gas_M_s`. Its producer writes only `gas_M_s`; this is a producer/record defect, not a demonstrated source-resolution defect. The static review passes 39/40 checks, with this sole failure. Five isolated gate expectation tests pass, including original refusal, wrong-M_s and Boolean refusal, and 362 endpoint refusal. Adding 128 only to a synthetic in-memory copy makes this isolated gate accept; no certificate was changed or adopted.

TESTED source custody: independently reconstructed permitted saved C4R3 source at M_s=128 has roster digest `{static['source_roster_digest']}`, exactly the record's build digest and gas record. Production M_s=128 radial factors agree with an independent normalized-Lagrange reconstruction. Actual producer, common helper and certificate source pins were checked from bytes. This establishes use of the M_s=128 source; the earlier M_s=64 bound is not assumed to transfer.

TESTED numerical recomputation: independent complete spherical-shell (128,256] cylindrical quadrature uses endpoint maps, two refinements, and validated barycentric vertical interpolation. Coarse B1 = {coarse['B1']:.17g}; refined B1 = {refined['B1']:.17g}; certificate B1 = {refined['certificate_B1']:.17g}. Coarse/refined relative change = {convergence:.9g}; refined/certificate relative difference = {refined['B1_relative_difference']:.9g}. Coarse/refined node counts are {coarse['tensor_nodes_evaluated']:,}/{refined['tensor_nodes_evaluated']:,}. Shared source definitions remain an explicit dependency; neither producer nor producer checker was imported.

Independent direction × cardinal-torus × radius search gives rho = {rho['own_search']['maximum']:.17g}, compared with certificate {rho['certificate_rho']:.17g}. The independently evaluated certificate witness agrees within relative {rho['witness_relative_difference']:.9g}. Own rho and refined B1 give max/tau = {independent_ratio:.17g}, below the registered shell tolerance 0.005. This is a numerical search and quadrature estimate, not a rigorous global supremum proof; the record honestly labels that limitation.

TESTED full reach and algebra: ten contiguous declared shells cover [4,363]; 363 exceeds sqrt(2) × 256 = 362.03867196751236 for production P=128 and also covers P=64. All ten row-bound calculations reproduce exactly, maximum declared shell/tau = {static['numeric_shell_max']:.17g} <= 0.005, and sum of all ten shell maxima = {static['summed_max_over_tau']:.17g} <= 0.05. Only one shell's source integral was independently recomputed; other shells received arithmetic/custody/tolerance checks.

Consumer custody: the supplied historical a3384de6be21baa755d6003000863ec084c7d45d5a3bd37f36938a5ab44fe576 byte pin and then b00dd854e79b36718fc67d9e82311e567a3e1ce08fbc1ed93cab5e60d9e6af01 changed externally before execution. The failed first harness stopped at its exact-pin assertion and executed no gate. The successful harness captured one byte buffer at {gate['utc']} and executed only its selected LO fragment, preserved in the snapshot. Its consumer byte hash is {gate['consumer']['sha256']}. No broad comparator conclusion or claim about future consumer bytes follows.

UNTETSTED/limitations: no independent rerun of the certificate's I1-T in this LO subreview; no GQ, full r5, NGC, full comparison-engine, or rigorous envelope audit. No scientific launch, forbidden-run read, real NGC target read, network operation, or existing-file overwrite. Peak review-process RSS was {decision['peak_rss_bytes']:,} bytes, below 8 GB. Only standard library and NumPy were used, with isolated Python and single-thread BLAS.

Blocker owner: Claude2 certificate producer/launch owner. Deciding step: immutable LO successor with the exact required `source_gas_M_s: 128`, measured source custody retained, actual consumer admission revalidated and downstream pins updated. Existing reviewed bytes stay unchanged.

Every cited file below is pinned from bytes. The consumer is the historical tested snapshot version, not a claim that the live pathname remains unchanged. All transitive actually read source dependencies are also recorded in the individual evidence and final hash manifest.

| File | SHA256 |
|---|---|
'''
report = report.replace('UNTETSTED', 'UNTESTED')
report += ''.join('| `'+p['path']+'` | `'+p['sha256']+'` |\n' for p in citations)
with (OUT/'REVIEW_CX3V001.md').open('x') as f:f.write(report)
dependencies = {}
for obj in (static,rho,coarse,refined):
    for p in obj['read_dependencies']:
        assert sha(p['path']) == p['sha256'], 'Source changed: '+p['path']
        dependencies[p['path']] = p['sha256']
files = [p for p in OUT.iterdir() if p.is_file()]
write('HASH_MANIFEST_CX3V001.json', {
    'date_u': date_u, 'outputs': [pin(p) for p in sorted(files)],
    'verified_read_dependencies': [{'path': p, 'sha256': h} for p,h in sorted(dependencies.items())],
    'historical_consumer_fragment_version': gate['consumer'],
    'note': 'No self hash. Historical consumer bytes preserved by fragment snapshot. Unexecuted/failed harness successors remain retained and are not passing evidence.'})
write('BUILD_REVIEW_CX3V001.json', {
    'date_u': date_u, 'verdict': 'FAIL', 'numerical_subreview': 'PASS_WITH_LIMITATIONS',
    'report': pin(OUT/'REVIEW_CX3V001.md'), 'decision': pin(OUT/'REVIEW_DECISION_CX3V001.json'),
    'manifest': pin(OUT/'HASH_MANIFEST_CX3V001.json'), 'blockers': pin(OUT/'TYPED_BLOCKERS_CX3V001.json')})
print(json.dumps({'build': pin(OUT/'BUILD_REVIEW_CX3V001.json'), 'report': pin(OUT/'REVIEW_CX3V001.md'), 'decision': pin(OUT/'REVIEW_DECISION_CX3V001.json'), 'manifest': pin(OUT/'HASH_MANIFEST_CX3V001.json'), 'convergence': convergence, 'independent_max_over_tau': independent_ratio}))
