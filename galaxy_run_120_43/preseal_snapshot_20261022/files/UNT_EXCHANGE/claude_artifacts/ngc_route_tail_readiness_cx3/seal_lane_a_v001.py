"""Write readiness report and resource projections, never launches anything."""
import hashlib
import importlib.util
import json
import math
import subprocess
from pathlib import Path

O = Path(__file__).parent
B = O.parent
R = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for x in iter(lambda: f.read(1048576), b''): h.update(x)
    return h.hexdigest()


def write(p, obj):
    with p.open('x') as f:
        f.write(obj if isinstance(obj,str) else json.dumps(obj, indent=2, sort_keys=True, allow_nan=False)+'\n')


def main():
    sources = json.loads((O/'INPUT_HASHES_V001.json').read_text())['sha256_from_bytes']
    def load(p):
        sources[str(p)] = sha(p)
        return json.loads(p.read_text())
    receipt_path = R/'runs/NGC3198_ROUTE_A_A2F10_RUN_V001.receipt.json'
    progress_path = R/'runs/NGC3198_ROUTE_A_A2F10_RUN_V001/progress.jsonl'
    receipt = load(receipt_path)
    sources[str(progress_path)] = sha(progress_path)
    lines = [json.loads(s) for s in progress_path.read_text().splitlines() if s.strip()]
    prep = next(x for x in lines if x.get('stage') == 'iteration_prepared')
    prereg = load(B/'ngc_kgrid_fidelity_c2/PREREG_KGRID_FIDELITY_V001.json')
    measured = prereg['measured_baseline_facts_G80C_run_v001']
    assert receipt['elapsed_seconds'] == measured['run_elapsed_s']
    assert receipt['peak_rss_bytes'] == measured['peak_rss_bytes']
    assert prep['elapsed_seconds'] == measured['prep_elapsed_s']
    op = load(B/'ngc_kgrid_fidelity_c2/phase23/ops/T120L_hovr/OPERATOR.json')
    oprep = load(B/'ngc_kgrid_fidelity_c2/phase23/ops/T120L_hovr/PREP.json')
    # Validate every K16 expected pin from the actual bytes; never follow run
    # paths embedded in these records, and never inspect forbidden runs.
    driver_path=B/'tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py'
    sp=importlib.util.spec_from_file_location('cx3_seal_driver',driver_path)
    d=importlib.util.module_from_spec(sp);sp.loader.exec_module(d)
    pin_check=[]
    for k,(p,expected) in d.NGC_CODE_UVT.items():
        actual=sha(p);sources[str(p)]=actual
        pin_check.append({'role':k,'path':str(p),'expected':expected,'sha256_from_bytes':actual,'matches':actual==expected})
    assert all(x['matches'] for x in pin_check)
    write(O/'K16_PIN_CHECK_V001.json',{'label':'TESTED','pins':pin_check})
    # No numerical model fitting: explicit extrapolation of the saved partial
    # G80C column work, plus the design's untested NGC tail cost per iteration.
    prep_s=measured['prep_elapsed_s']*2.25
    col_s=measured['column_phase_s']/measured['completed_columns']*2.25
    tail_s=96.+205.*.5
    rows=[]
    for ncol in (2496,4992):
        for nw in (1,2,8):
            per=prep_s+col_s*ncol/nw+tail_s
            rows.append({'illustrative_kept_columns':ncol,'column_workers':nw,
                         'seconds_per_iteration_UNTESTED':per,
                         'hours_16_iterations_UNTESTED':per*16/3600,
                         'assumptions':'serial prep; linear W scaling; ideal column parallelism; design tail estimate; no failed-column search cost'})
    cap5=5*1024**3
    plan={
        'status':'UNTESTED_LAUNCH_PLAN_ONLY_CLAUDE2_OWNS_LAUNCHES',
        'measured_saved_G80C': {k:measured[k] for k in ('run_elapsed_s','prep_elapsed_s','completed_columns','column_phase_s','s_per_metric_call','peak_rss_bytes')},
        'measured_T120L_replay_prep':{'peak_rss_bytes':oprep['timing']['peak_rss_bytes'],
            'prep_wall_s':oprep['timing']['total_wall_s'],'response_cpu_s_sum':op['response_cpu_s_sum'],
            'scope':'Saved iteration-0 replay construction; not fixed-point route-A or route-B timing.'},
        'K15_tail_memory': {'ring_tables_GB':.18,'LRU16_corner_tables_GB':.19,'corner_source_GB':.049,
                            'cap_GiB_per_process':.6,'status':'DESIGN_ESTIMATE_UNTESTED_ON_NGC_FIXED_POINT'},
        'serial_peak_estimate_bytes_UNTESTED':measured['peak_rss_bytes']*2.25+.6*1024**3,
        'route_A_forecasts_UNTESTED':rows,
        'full_route_B_wall_time':'UNTESTED: no completed matching NGC route-B saved run. Measure first valid point; do not present DDO time as NGC measurement.',
        'proposed_caps_require_Claude2_registration': {
            'serial_process_tree_RSS_bytes':cap5,
            'parallel8_process_tree_RSS_bytes':9*cap5,
            'individual_RSS_bytes':cap5,
            'wall_seconds':43200,
            'total_output_bytes':32*1024**3,
            'max_route_A_iterations':16,
            'picard_passes':4,
            'retry':'No automatic retry; preserve failures and checkpoints; deliberate root continuation only.',
            'note':'Serial v009 cap 4 GiB + design 1 GiB = 5 GiB; do not confuse a process-tree cap with a per-worker cap. Parallel cap is conservative, unmeasured, not a new authority.'},
        '18_core_envelope': {
            'parallel8_points_max':2,'accounting':'2*(8 column workers + 1 active parent) = 18; monitor overhead and other lanes may lower this.',
            'conservative_two_tree_RSS_GiB':90,
            'serial_points_cpu_only_upper_bound':18,
            'current_Codex3_authorization':'No scientific points; at most two dry/synthetic/replay processes total, each <8 GB.',
            'other_requirements':'Root must reserve shared RAM/disk/cores for other lanes; two N8 points permitted only by the future root allocation.'},
        'admitted_point_sequence':[
            'Require byte-pinned V007 adoption and DDO154 admitted region; the A2F10 example is not an admitted region.',
            'Require N_PASS, EPS/GQ/I1T/NQ and LO_NGC records for the current NGC domain; no N-tests launched by this lane.',
            'Integrate reviewed anisotropic prep, decided coefficients, tail route-B stages, and truncation custody; nonempty zero-blocker dry-run.',
            'At each member classify current tail-ON confinement, compute whole-radius cut, mass fraction, rebuild source/checkpoint, and recheck confinement. Never reuse G80C cut as the production cut.',
            'Run first admitted point under root monitor; measure RSS/wall/disk. Same-state v009/v010 assembly comparator decides L3. Nonempty-tail physical differences are not identity failures.',
            'Only then schedule within caps and shared machine budget; retain all failed/INVALID rows for the frozen scoring contract.']}
    write(O/'ADMITTED_POINT_RESOURCE_PLAN_V001.json',plan)
    blockers=[
        ('A-GRID','IMPLEMENTATION','Claude2 / assigned NGC prep owner','T120L is 120×120×80; r4 single-axis prep capped at 80.','Reviewed anisotropic prep+worker+binding, saved-state identity and nonempty dry-run.'),
        ('A-COEFF','IMPLEMENTATION','Claude2 / assigned NGC driver owner','NGC route-A driver normalizer fixes fe5a2f06, not the requested decided A2 grid.','Bind per-call decided coefficient grid through the v002-lineage worker and prove custody.'),
        ('A-TAIL-B','IMPLEMENTATION','Claude2 / assigned NGC route-B owner','Route-B numerics rejects uv_tail; route-B tail successors are DDO-only.','Reviewed NGC continuum tail binding at every read site and clean dry-run.'),
        ('A-CUT','IMPLEMENTATION_AND_CURRENT_POINT_DATA','Claude2 / assigned NGC prep owner','Standalone cut calculator is not integrated into gas prep/source/checkpoint identity. Actual tail-ON cut and dropped fraction are unknown.','Pinned confinement classification at each point, whole-radius cut, rebuild source and recheck fixed-point confinement.'),
        ('A-ROW','SCHEMA','Claude2 / NGC driver and freeze owners','r4 final_rows_check accepts only the existing inner-node INVALID reason; rejects outer-truncation reason.','Reviewed row-schema successor plus INVALID freeze/scoring tests.'),
        ('A-CERT','CERTIFICATE_DEPENDENCY','Claude2 certificate owner; Codex1 N-test evaluator lane','Current validated certificates and N_PASS were not supplied to these contracts.','Pin actual applicable EPS, GQ, I1T, NQ, LO_NGC and N_PASS records; no fabricated certificates.'),
        ('A-ADOPT','SCIENTIFIC_DEPENDENCY','Claude2','V007 adoption and independent DDO154 admitted region not supplied.','Root adoption and calibration admitted-region freeze.'),
        ('A-L3','RUNTIME_EVIDENCE','Claude2','Actual first NGC v010 route-B result assembly remains UNTESTED.','Same admitted state/stage outputs against v009 parent; strict results, stage array bytes and complete custody comparison.'),
        ('A-COST','RESOURCE_EVIDENCE','Claude2','Full NGC tail fixed-point and route-B costs, process-tree memory and disk are UNTESTED.','Monitor first valid root-owned point, preserve measurements, then register concurrency/caps.')]
    write(O/'BLOCKERS_V001.json',{'schema':'TYPED_BLOCKERS_CX3V001','blockers':[dict(zip(('id','type','owner','finding','deciding_step'),x)) for x in blockers]})
    date=subprocess.check_output(['date','-u'],text=True).strip()
    report=f'''# Lane A — NGC route/tail readiness, dispatch 0516

date -u: {date}

**NOT READY: zero-blocker v010 r4 dry-run is not achieved.** Three actual driver dry-run attempts refused before any stage. This is a build/readiness finding, not a physical failure. Claude2 remains the sole scientific launch owner.

TESTED: 22/22 initial checks, plus 3/3 row-reason compatibility checks. Peak RSS for the initial suite was 71,516,160 bytes. The expected early refusals passed their test expectations; they are not successful dry-runs. No complete DRYRUN_REPORT was emitted. No forward, route-A or route-B run was invoked.

The contract fixes the requested kept cube K=2, cylinder K_big=16, continuum_v001, R1 quadrature (order 8, transverse width .005, vertical width .007, M_s=96), RO1 v002 workers/binding and certificate slots. T120L means 120×120×80, 1,152,000 waves. It must not be replaced by an isotropic 120³ grid. The K16 worker/binding/lineage pins were verified from bytes. A2F10 is an illustrative physical input, not a calibrated admitted point.

The actual refusals are: route-B unknown numerics key uv_tail; route-A only default fe5a2f06 coefficients; and the route-A >80-axis-node guard. K16 changes a plan's worker lineage but does not provide an executable NGC tail fixed-point chain. No reviewed file was edited to remove these guards.

Truncation helper v002 applies A14 C3/A12.5 to complete classified columns: drop the entire first unconfined radius and all exterior columns, compute total dropped HI mass fraction with original weights, and set query rows strictly beyond the cut INVALID with null speeds. It refuses undecided/numerically failed confinement. Synthetic tests distinguish the dropped mass from the smaller unconfined-column mass. The current tail-ON cut, its mass fraction and its fixed-point validity are UNTESTED. A27 forbids borrowing a G80C cut to bypass failed grid fidelity. The old failing fraction 2.55e-4 is not the whole-radius cut fraction. Source rebuild and current-point confinement recheck remain required. The v002 successor changes only invalid_reason to the driver-aligned reason key; r4 still rejects this new outer-truncation reason, as tested.

The comparator was tested using the exact final-result assembly AST extracted from the byte-pinned v009-GEO parent and v010 r4, fed synthetic final-stage rows. It checks all 43 rows, speed map, validity and pass data, and has a separate NPZ dtype/shape/byte comparison. Adversarial changes to speed, row count/order, INVALID metadata, tail-OFF metadata, RO1 firing and stage arrays fail. This tests assembly logic without calling execute_chain. It does not test NGC tail physics or full run custody. The deciding L3 test remains the first real v010 NGC result against a v009 parent on identical admitted state/stage outputs. First test tail OFF (or a separately declared empty-tail identity); do not demand speed equality between a nonempty-tail physical run and a tail-OFF parent. The full deciding test must additionally validate all stage records, artifacts, declared custody maps, source/checkpoint identity and driver hashes.

Resource projections are explicitly UNTESTED extrapolations from saved NGC receipt/progress bytes, never DDO measurements relabelled NGC. Saved G80C: 418.47 s prep, 1,003.07 s over 2,503 completed columns, 1.123 GB peak process-tree RSS. The run stopped on a column failure; it is not a full-iteration benchmark. T120L replay prep measured 1.172 GB peak RSS. K15's tail tables sum to about .419 GB before overhead, under the design's .6 GiB tail cap, but the fixed-point implementation is unmeasured. The explicit resource plan gives serial/N2/N8 forecasts for 2,496 or 4,992 columns, not a selected production cut. Full route-B wall time is unavailable. On 18 cores, two N8 points consume 2×(8 workers+1 parent); the conservative two-tree RSS envelope is 90 GiB at 5 GiB per process. Shared machine occupancy can lower that allocation. Current Codex3 authorization remains zero scientific points and at most two small test processes.

Typed blockers, owner and deciding step are in BLOCKERS_V001.json. These are implementation, evidence and existing scientific dependencies, not new approval gates. No target velocities, prohibited KMAX/UVT runs, session logs or network were read. No file was deleted, moved, renamed or overwritten.

Errors retained: build_readiness_v001 stopped before outputs because macOS refused RLIMIT_AS. build_readiness_v002 removed that unsupported limit for these tiny checks and records actual RSS. All v001 bytes are retained. The standalone helper's v001 reason-key mismatch is corrected only in v002. Readiness remains blocked as reported.

File custody follows. Hashes are SHA256 of file bytes. V005 is an observed open-file snapshot, not an execution pin. Generated manifests exclude themselves to avoid a self-hash claim.
'''
    # All references in reports/contracts: verified inputs and every existing own
    # output. Directory names and future absent paths are not claimed artifacts.
    for p in O.rglob('*'):
        if p.is_file(): sources[str(p)] = sha(p)
    report += '\n'.join(f'- `{p}` — `{s}`' for p,s in sorted(sources.items()))+'\n'
    write(O/'LANE_A_READINESS_REPORT_V001.md',report)
    files={str(p):sha(p) for p in O.rglob('*') if p.is_file()}
    write(O/'FILE_HASHES_V001.json',{'sha256_from_bytes':files,'inputs':sources,'date_u':date})
    print(json.dumps({'report':str(O/'LANE_A_READINESS_REPORT_V001.md'),'files':len(files), 'resource_rows':rows}))


if __name__=='__main__':main()
