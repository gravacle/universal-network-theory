"""Whole fixed hold-window phase test from saved coherences; no evolution.

The disk bound follows from the declared held Hamiltonian, not a finite
difference fit. Floating-point observation allowances are assigned, not
certified. A monotonicity failure is science output, not a numerical failure.
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import tempfile
import time

HERE = Path(__file__).resolve().parent
INPUT = "native_finite_region_formation_v001_results.json"
OUTPUT = HERE / "native_finite_region_phase_window_v001_results.json"
PINS = {
    INPUT: "2a52ba3a029c2aa6d6a421d942837cb78035e935c61a0ae60ababe5237862c91",
    "NATIVE_FINITE_REGION_HELD_STATE_RESULT_V001.md": "cceb278cb9e4ab704ace4c378a1abdf7039092260f205846c90fbdcd5ddabc26",
}
EPS_Z = math.sqrt(2)*1e-10
STEP, LIPSCHITZ = 1/16, .5


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def memory():
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return rss if sys.platform == "darwin" else rss*1024


def run():
    start = time.perf_counter()
    if OUTPUT.exists() or OUTPUT.is_symlink():
        raise FileExistsError("Refusing overwrite: "+str(OUTPUT))
    source_sha = sha(Path(__file__))
    for path, expected in PINS.items():
        if (HERE/path).is_symlink() or sha(HERE/path) != expected:
            raise ValueError("Pinned input differs: "+path)
    payload = json.loads((HERE/INPUT).read_text())
    if payload["status"] != "COMPLETE" or payload["failures"]:
        raise ValueError("Source calculation incomplete or failed")
    results, identities = [], set()
    for history in payload["histories"]:
        if history["id"] in identities or history["status"] != "COMPLETE":
            raise ValueError("Repeated or incomplete history")
        identities.add(history["id"])
        rows = [row for row in history["rows"] if row["stage"] == "hold" and row["time"] >= 2]
        if [r["time"] for r in rows] != [2+j*STEP for j in range(33)]:
            raise ValueError("Not the declared full hold mesh")
        z = [complex(r["record_coherence"]["real"], r["record_coherence"]["imag"]) for r in rows]
        if not all(math.isfinite(v.real) and math.isfinite(v.imag) for v in z):
            raise ValueError("Nonfinite coherence")
        intervals = []
        for j in range(32):
            left, right = z[j], z[j+1]
            product = left.conjugate()*right
            imag_error = EPS_Z*(abs(left)+abs(right))+EPS_Z**2
            lower_amplitude = abs(left)-EPS_Z-LIPSCHITZ*STEP
            continuity_consistent = abs(right-left) <= LIPSCHITZ*STEP+2*EPS_Z
            if not continuity_consistent:
                raise ArithmeticError("Saved values violate analytic speed bound")
            sign = 1 if product.imag > imag_error else (-1 if product.imag < -imag_error else 0)
            qualified = lower_amplitude > 0
            intervals.append(dict(from_x=rows[j]["time"], to_x=rows[j+1]["time"],
                left_coherence=[left.real,left.imag], right_coherence=[right.real,right.imag],
                disk_amplitude_lower_bound=lower_amplitude,
                no_zero_or_hidden_winding_qualified=qualified,
                imaginary_product=product.imag, assigned_imaginary_product_error=imag_error,
                qualified_phase_increment_sign=sign if qualified else None,
                principal_phase_increment=math.atan2(product.imag, product.real),
                principal_increment_is_unwrapped=qualified))
        signs = [entry["qualified_phase_increment_sign"] for entry in intervals]
        complete_disk = all(entry["no_zero_or_hidden_winding_qualified"] for entry in intervals)
        positives, negatives = signs.count(1), signs.count(-1)
        results.append(dict(history_id=history["id"], initial_graph_mask=history["initial_graph_mask"],
            fragment_coupling=history["fragment_coupling"], intervals=intervals,
            whole_hold_amplitude_lower_bound=min(entry["disk_amplitude_lower_bound"] for entry in intervals),
            all_intervals_disk_qualified=complete_disk,
            positive_increments=positives, negative_increments=negatives,
            unresolved_increments=signs.count(0), unqualified_intervals=signs.count(None),
            total_unwrapped_increment=math.fsum(entry["principal_phase_increment"] for entry in intervals) if complete_disk else None,
            monotone_in_either_orientation_rejected=positives>0 and negatives>0,
            instantaneous_monotonicity_certified=False))
    if len(results) != 4:
        raise ValueError("Missing histories")
    for path, expected in PINS.items():
        if sha(HERE/path) != expected:
            raise ValueError("Input changed during analysis")
    if sha(Path(__file__)) != source_sha:
        raise ValueError("Source changed during analysis")
    elapsed, rss = time.perf_counter()-start, memory()
    if elapsed > 120 or rss > 256*1024*1024:
        raise RuntimeError("Resource ceiling exceeded")
    result = dict(status="COMPLETE", source_sha256=source_sha, input_sha256=PINS,
        histories=results, method=dict(coherence_component_allowance=1e-10,
            complex_error_bound=EPS_Z, exact_normalized_state_derivative_bound=LIPSCHITZ,
            all_saved_hold_points_used=True, no_evolution=True, no_state_renormalization=True,
            qualifications_conditional_on_assigned_roundoff_allowance=True,
            certified_floating_point_intervals=False, physical_clock_established=False,
            diagnostic_is_new_Aplus_phase_not_previous_B0_clock=True),
        runtime=dict(wall_seconds=elapsed,peak_rss_bytes=rss))
    data = (json.dumps(result,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=HERE,prefix=OUTPUT.name+".partial.",delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary,OUTPUT)
    finally:
        if temporary is not None:
            temporary.unlink()
    digest = hashlib.sha256(data).hexdigest()
    if sha(OUTPUT) != digest:
        raise RuntimeError("Published hash mismatch")
    print(json.dumps(dict(status="COMPLETE",path=str(OUTPUT),sha256=digest,
        source_sha256=source_sha,runtime=result["runtime"],
        histories=[{k:v for k,v in row.items() if k!="intervals"} for row in results]),allow_nan=False))


if __name__ == "__main__":
    if sys.argv[1:] != ["--run"]:
        raise SystemExit("Explicit --run required; saved coherences only")
    run()
