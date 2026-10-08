"""Preserve V001 failure; reevaluate only cancellation-prone references."""
from decimal import Decimal, localcontext
from pathlib import Path
import hashlib
import json
import time


def main():
    start = time.perf_counter()
    base = Path(__file__).resolve().parent
    prior_path = base / "COMPACT_DWARF_ISOLATED_BOUND_V001_RESULT.json"
    output = base / "COMPACT_DWARF_ISOLATED_BOUND_V002_REPAIR_RESULT.json"
    if output.exists():
        raise SystemExit("Refusing overwrite or duplicate repair")
    prior_hash = hashlib.sha256(prior_path.read_bytes()).hexdigest()
    if prior_hash != "6fe41c1fdb3f971a449ad34ec58adcd9c4fdb062659e174d306f9e55e4e26bd9":
        raise SystemExit("Prior result hash mismatch")
    prior = json.loads(prior_path.read_text())
    references = []
    replacements = {}
    with localcontext() as context:
        context.prec = 80
        for row in prior["kernel_rows"]:
            x = Decimal.from_float(row["x"])
            exact = Decimal(1)+Decimal(2)*((Decimal(1)+x)*(-x).exp()-1)/(x*x)
            value = float(exact)
            name = "kernel_closed_"+str(row["x"])
            old = next(c for c in prior["controls"] if c["name"] == name)
            error = abs(row["normalized_extra_force"]-value)/max(abs(value),1e-20)
            new = dict(name=name,error=error,tolerance=old["tolerance"],
                       passed=error <= old["tolerance"])
            replacements[name] = new
            references.append(dict(x=row["x"],decimal_reference=str(exact),
                                   prior_control=old,repaired_control=new))
    combined = [replacements.get(c["name"], c) for c in prior["controls"]]
    result = dict(status="TECHNICAL_CONTROL_RECOVERED" if all(c["passed"] for c in combined) else "FAILED",
                  source_result_sha256=prior_hash,
                  original_status=prior["status"],
                  original_failed_controls=[c for c in prior["controls"] if not c["passed"]],
                  precision=80,criteria_changed=False,science_rows_recomputed=False,
                  references=references,combined_controls=combined,
                  combined_control_count=len(combined),
                  unchanged_rows=prior["rows"],
                  custody={name:hashlib.sha256((base/name).read_bytes()).hexdigest()
                           for name in (Path(__file__).name,
                                        "COMPACT_DWARF_ISOLATED_BOUND_V002_REPAIR.md")},
                  elapsed_seconds=time.perf_counter()-start)
    with output.open("x") as handle:
        json.dump(result,handle,indent=2,allow_nan=False)
        handle.write("\n")
    print(json.dumps({k:result[k] for k in ("status","original_failed_controls","combined_control_count","elapsed_seconds")},indent=2))
    print("max repaired relative error", max(r["repaired_control"]["error"] for r in references))
    if result["status"] != "TECHNICAL_CONTROL_RECOVERED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
