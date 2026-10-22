"""R3 checker C1: independent re-derivation of the miss set and W1 results.
Reads only permitted run files: finish.json status/reasons, stage listings,
column *_failure.json, *_iterations.jsonl, stderr.txt, launch.json, monitor log.
Never opens result.json, inputs/, column_XXXX.json, *_source.npz, rotation/.
"""
import json, hashlib, os, re, sys

RUNS = "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs"
BASE = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2"
R3D = BASE + "/d7_recovery_r3"
OUT = R3D + "/check/C1_W1_REDERIVE_V001.json"
TPL = (1.5125e8, 3.025e8)
CASES = {"C4R2": BASE + "/d7_recovery_r2/specs_d7r2/filled/CALL_KMAX_C4R2_A2F10_D7R2_C2V005.json",
         "S4R2": BASE + "/d7_recovery_r2/specs_d7r2/filled/CALL_KMAX_S4R2_A2F10_D7R2_C2V005.json",
         "Y4R2": BASE + "/d7_recovery_r2/specs_d7r2/filled/CALL_KMAX_Y4R2_A2F10_D7R2_C2V005.json"}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def jl(p):
    return json.load(open(p))


def w1(entry, rlo, rhi, tlo, thi):
    """Declared W1 text, implemented independently."""
    lo, hi = entry
    if rlo > 0 and rhi > 0:
        if lo > tlo:
            return [tlo, hi], "A", "root_below_lo"
        return [lo / 2.0, hi], "B", "root_below_lo"
    if rlo < 0 and rhi < 0:
        if hi < 1.05 * thi:
            return [lo, 1.05 * thi], "A", "root_above_hi"
        return [lo, 2.0 * hi], "B", "root_above_hi"
    return None, None, "SIGN_CHANGE_OR_ZERO_NOT_W1"


def main():
    findings = []
    r1 = jl(BASE + "/d7_recovery/KMAX_D7_RECOVERY_R1.json")["brackets"]["rule"]["fs_absolute_overrides"]
    r2 = jl(BASE + "/d7_recovery_r2/KMAX_D7_RECOVERY_R2.json")["brackets"]["rule"]["fs_absolute_overrides"]
    anchor = jl(BASE + "/KMAX_MATRIX_PREREG_V005.json")["anchor"]["brackets"]["rule"]["fs_absolute_overrides"]
    r3 = jl(R3D + "/KMAX_D7_RECOVERY_R3.json")["brackets"]["rule"]["fs_absolute_overrides"]
    ev = jl(R3D + "/D7_EVIDENCE_C4R2_S4R2_Y4R2_V001.json")
    # which columns were widened by R1 or R2 (vs anchor / template): step-B candidates
    widened_before = sorted({int(k) for k, v in r1.items() if anchor.get(k) != v} |
                            {int(k) for k, v in r2.items() if r1.get(k) != v})
    out = {"cases": {}, "widened_by_R1_or_R2": widened_before}
    per_col = {}
    for case, spec in CASES.items():
        run = f"{RUNS}/KMAX_A2F10_{case}_D7R2_RUN_V001"
        fin = jl(run + "/finish.json")
        rec = {"finish_status": fin["status"], "finish_reasons": fin["reasons"],
               "finish_sha256": sha(run + "/finish.json"), "spec_sha256": sha(spec)}
        lj = jl(run + ".receipt.json.launch.json")
        rec["launch_sha256"] = sha(run + ".receipt.json.launch.json")
        argv = json.dumps(lj)
        rec["launch_mentions_spec"] = os.path.basename(spec) in argv
        spec_over = jl(spec)["numerics"]["brackets"]["rule"]["fs_absolute_overrides"]
        stages = sorted(os.listdir(run + "/stages"))
        rec["stages"] = stages
        present, failed = {}, {}
        for st in stages:
            cdir = f"{run}/stages/{st}/columns"
            if not os.path.isdir(cdir):
                continue
            for fn in os.listdir(cdir):
                m = re.fullmatch(r"column_(\d{4})(_failure\.json|\.json|_iterations\.jsonl|_source\.npz)", fn)
                if fn in ("start.json", "finish.json"):
                    continue
                if not m:
                    findings.append(f"{case}: unexpected file {st}/{fn}")
                    continue
                i = int(m.group(1))
                if m.group(2) == ".json":
                    present.setdefault(i, []).append(st)
                elif m.group(2) == "_failure.json":
                    failed.setdefault(i, []).append(st)
        all_idx = set(present) | set(failed)
        rec["n_success"] = len(present)
        rec["n_failed"] = len(failed)
        rec["missing_any"] = sorted(set(range(72)) - all_idx)
        rec["both_success_and_failure"] = sorted(set(present) & set(failed))
        misses = []
        for i in sorted(failed):
            st = failed[i][0]
            cdir = f"{run}/stages/{st}/columns"
            fj = jl(f"{cdir}/column_{i:04d}_failure.json")
            its = [json.loads(l) for l in open(f"{cdir}/column_{i:04d}_iterations.jsonl") if l.strip()]
            pts = sorted({(r["Hc_m2_s2"], r["mass_relative_residual"]) for r in its})
            entry = spec_over.get(str(i), list(TPL))
            src = "override" if str(i) in spec_over else "template"
            lo_pt = [p for p in pts if p[0] == entry[0]]
            hi_pt = [p for p in pts if p[0] == entry[1]]
            m = {"index": i, "stage": st, "type": fj.get("type"), "message": fj.get("message"),
                 "failure_sha256": sha(f"{cdir}/column_{i:04d}_failure.json"),
                 "iterations_sha256": sha(f"{cdir}/column_{i:04d}_iterations.jsonl"),
                 "entry_in_spec": entry, "entry_source": src,
                 "distinct_points": pts,
                 "endpoints_match_entry": len(lo_pt) == 1 and len(hi_pt) == 1 and len(pts) == 2}
            if not ("NOT_BRACKETED" in str(fj.get("message"))):
                findings.append(f"{case} col {i}: failure not a bracket miss: {fj}")
            if m["endpoints_match_entry"]:
                new, step, side = w1(entry, lo_pt[0][1], hi_pt[0][1], *TPL)
                if i in widened_before and step == "A":
                    # declared: a miss on an entry already widened by R1/R2 is step B
                    lo, hi = entry
                    new = [lo / 2.0, hi] if side == "root_below_lo" else [lo, 2.0 * hi]
                    step = "B(forced:previously widened)"
                m.update(r_lo=lo_pt[0][1], r_hi=hi_pt[0][1], side=side, step=step, new_entry=new)
            else:
                findings.append(f"{case} col {i}: iteration endpoints do not match spec entry {entry}: {pts}")
            misses.append(m)
            per_col.setdefault(i, []).append((case, tuple(entry), tuple(m.get("new_entry") or ()), m.get("step")))
        rec["misses"] = misses
        # stderr of fs_rotation
        se = run + "/stages/06_fs_rotation/stderr.txt"
        if os.path.exists(se):
            lines = [l for l in open(se).read().splitlines() if l.strip()]
            rec["fs_rotation_last_stderr_line"] = lines[-1] if lines else None
        # compare to builder evidence
        bev = ev.get(case, {})
        bm = {m["index"]: m for m in bev.get("missed_columns", [])}
        for m in misses:
            b = bm.get(m["index"])
            if b is None:
                findings.append(f"{case} col {m['index']}: missing from builder evidence")
                continue
            if b["entry_in_failed_call"] != m["entry_in_spec"]:
                findings.append(f"{case} col {m['index']}: builder entry {b['entry_in_failed_call']} != {m['entry_in_spec']}")
            if b["W1"]["new_entry"] != m.get("new_entry"):
                findings.append(f"{case} col {m['index']}: builder new entry {b['W1']['new_entry']} != {m.get('new_entry')}")
            if b["W1"].get("declared_step") != m.get("step"):
                findings.append(f"{case} col {m['index']}: builder step {b['W1'].get('declared_step')} != {m.get('step')}")
            bres = [(e["Hc_m2_s2"], e["mass_relative_residual"]) for e in b["evidence"]]
            if sorted(bres) != sorted(m["distinct_points"]):
                findings.append(f"{case} col {m['index']}: builder residuals differ")
            if b["failure_file"]["sha256"] != m["failure_sha256"] or b["iterations_file"]["sha256"] != m["iterations_sha256"]:
                findings.append(f"{case} col {m['index']}: builder file hashes differ")
        extra = set(bm) - {m["index"] for m in misses}
        if extra:
            findings.append(f"{case}: builder evidence lists extra columns {sorted(extra)}")
        if bev.get("finish", {}).get("sha256") != rec["finish_sha256"]:
            findings.append(f"{case}: builder finish sha differs")
        if bev.get("call_spec", {}).get("sha256") != rec["spec_sha256"]:
            findings.append(f"{case}: builder spec sha differs")
        if bev.get("launch_file", {}).get("sha256") != rec["launch_sha256"]:
            findings.append(f"{case}: builder launch sha differs")
        out["cases"][case] = rec
    # cross-case consistency + expected R3
    cons = {}
    expected = dict(r2)
    for i, rows in sorted(per_col.items()):
        news = {r[2] for r in rows}
        froms = {r[1] for r in rows}
        cons[i] = {"cases": [r[0] for r in rows], "from": sorted(froms), "new": sorted(news),
                   "consistent": len(news) == 1 and len(froms) == 1}
        if not cons[i]["consistent"]:
            findings.append(f"col {i}: cross-case inconsistency {rows}")
        else:
            expected[str(i)] = list(next(iter(news)))
        if any(str(r[3]).startswith("B") for r in rows):
            cons[i]["note"] = "step B"
    out["cross_case"] = {str(k): v for k, v in cons.items()}
    out["miss_set"] = {c: [m["index"] for m in out["cases"][c]["misses"]] for c in out["cases"]}
    out["expected_R3_fs"] = expected
    out["R3_fs_equals_expected"] = (r3 == expected)
    if r3 != expected:
        findings.append(f"R3 fs overrides != expected: diff keys {sorted(set(r3) ^ set(expected)) + [k for k in r3 if k in expected and r3[k] != expected[k]]}")
    out["findings"] = findings
    json.dump(out, open(OUT, "w"), indent=1, sort_keys=True)
    print(json.dumps({"miss_set": out["miss_set"], "R3_fs_equals_expected": out["R3_fs_equals_expected"],
                      "cross_case": out["cross_case"], "widened_by_R1_or_R2": widened_before,
                      "statuses": {c: (v["finish_status"], v["finish_reasons"], v["n_success"], v["n_failed"], v["missing_any"], v["both_success_and_failure"], v.get("fs_rotation_last_stderr_line"), v["launch_mentions_spec"]) for c, v in out["cases"].items()},
                      "steps": {c: [(m["index"], m.get("r_lo"), m.get("r_hi"), m.get("step"), m.get("entry_source")) for m in v["misses"]] for c, v in out["cases"].items()},
                      "findings": findings}, indent=1))


main()
