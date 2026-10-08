"""Read-only originating-machine ZIP and table audit; never execute contents.

The pinned hash below was measured locally, not independently sent by sender.
No physics replay or statistical acceptance gate is performed. Table tolerance
is only float serialization/summation consistency, not a new physics threshold.
"""
import csv
import hashlib
import io
import itertools
import json
import math
from pathlib import Path, PurePosixPath
import resource
import stat
import sys
import zipfile

resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
ROOT = "UNT_L6_PI_TRANSPORT_COMPLETION_RESULT_V002/"
LOCAL_PIN = "8d61b5e934896ec290cab03b6206ab1b2343577f9a402afea3032c7160be6523"
TOL = 2e-14

def require(condition, label):
    if not condition:
        raise ValueError(label)

def unique_object(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, "duplicate JSON key")
        value[key] = item
    return value

def parse_json(raw):
    return json.loads(raw, object_pairs_hook=unique_object)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

path = Path(sys.argv[1])
require(not path.is_symlink() and path.stat().st_size < 32 * 1024**2, "ZIP route/size")
require(digest(path.read_bytes()) == LOCAL_PIN, "ZIP changed since inspection")
out = {"zip_sha256": LOCAL_PIN, "independent_sender_digest_supplied": False}
with zipfile.ZipFile(path) as archive:
    members = archive.infolist()
    require(len(members) <= 5000, "member count cap")
    require(sum(i.file_size for i in members) <= 128 * 1024**2, "expanded size cap")
    names, folded = set(), set()
    for info in members:
        name = info.filename
        require(name.startswith(ROOT) and not info.is_dir(), "wrong root or directory")
        require(all(p not in ("", ".", "..") for p in name.split("/")), "unsafe path")
        require(not any(c in name for c in ("\\", ":", "\0")), "unsafe path character")
        require(name == str(PurePosixPath(name)), "noncanonical path")
        require(name not in names and name.casefold() not in folded, "duplicate/case collision")
        require(stat.S_IFMT(info.external_attr >> 16) in (0, stat.S_IFREG), "special object")
        require(not info.flag_bits & 1 and info.file_size <= 16 * 1024**2, "encrypted/large member")
        names.add(name)
        folded.add(name.casefold())
    for name in names:
        require(not any(str(p).casefold() in folded for p in PurePosixPath(name).parents),
                "file-parent collision")
    manifest_raw = archive.read(ROOT + "MANIFEST.json")
    manifest = parse_json(manifest_raw)
    require(manifest["schema"] == "UNT_CODEX_RESULT_MANIFEST_V001", "manifest schema")
    files = manifest["files"]
    relative = [r["path"] for r in files]
    require(relative == sorted(set(relative)), "manifest order/duplicates")
    require({ROOT + r for r in relative} == names - {ROOT + "MANIFEST.json"}, "manifest census")
    byte_count = 0
    for row in files:
        payload = archive.read(ROOT + row["path"])
        require(len(payload) == row["bytes"] and digest(payload) == row["sha256"],
                "size/hash mismatch: " + row["path"])
        byte_count += len(payload)
    require(byte_count == manifest["total_bytes"], "total size")
    out.update(manifest_files=len(files), manifest_bytes=byte_count,
               manifest_sha256=digest(manifest_raw))
    if len(sys.argv) > 2:
        report = Path(sys.argv[2])
        require(not report.is_symlink() and report.stat().st_size < 100000, "report route/size")
        require(archive.read(ROOT + "SCIENTIFIC_REPORT.md") == report.read_bytes(), "separate report mismatch")
        out["separate_report_byte_match"] = True

    def table(name):
        return list(csv.DictReader(io.StringIO(archive.read(ROOT + "TABLES/" + name).decode())))

    rows = table("ALL_SECTORS_AND_AGGREGATES.csv")
    require(len(rows) == 9984, "table row count")
    dimensions = ("dwell", "lane", "profile", "stage", "sector", "kind", "site_i", "site_j")
    values = ("actual", "conditional_product", "signed_actual_minus_product")
    indexed = {}
    signed_error = 0.0
    for row in rows:
        key = tuple(row[k] for k in dimensions)
        require(key not in indexed, "duplicate scientific key")
        item = tuple(float(row[k]) for k in values)
        require(all(math.isfinite(x) for x in item), "nonfinite scientific entry")
        signed_error = max(signed_error, abs(item[0] - item[1] - item[2]))
        indexed[key] = item
    observables = [("occupation", str(i), "") for i in range(12)]
    observables += [("pair", str(i), str(j)) for i, j in itertools.combinations(range(12), 2)]
    dwells = ("pi_over_4", "pi")
    lanes = ("audit", "target")
    profiles = ("fine", "tight")
    stages = ("before_transport", "after_transport")
    # Inspect actual aggregate spelling, but require exactly one extra sector label.
    sectors = {r["sector"] for r in rows}
    agg_names = sectors - {str(i) for i in range(7)}
    require(len(agg_names) == 1 and len(sectors) == 8, "sector census")
    agg = next(iter(agg_names))
    expected = {a + b for a in itertools.product(dwells, lanes, profiles, stages, sectors)
                for b in observables}
    require(set(indexed) == expected, "complete axes/observables")
    aggregation_error = 0.0
    start_error = 0.0
    maxima = {"pi_cross_per_sector": 0.0, "pi_cross_aggregate": 0.0,
              "pi_fine_tight_per_sector": 0.0, "pi_fine_tight_aggregate": 0.0}
    for dwell, lane, profile, stage in itertools.product(dwells, lanes, profiles, stages):
        for obs in observables:
            individual = [indexed[(dwell, lane, profile, stage, str(q)) + obs] for q in range(7)]
            total = indexed[(dwell, lane, profile, stage, agg) + obs]
            for k in range(3):
                aggregation_error = max(aggregation_error, abs(math.fsum(v[k] for v in individual) - total[k]))
    for lane, profile, sector in itertools.product(lanes, profiles, sectors):
        for obs in observables:
            a = indexed[("pi_over_4", lane, profile, "before_transport", sector) + obs]
            b = indexed[("pi", lane, profile, "before_transport", sector) + obs]
            start_error = max(start_error, *(abs(x-y) for x,y in zip(a,b)))
    for stage, sector in itertools.product(stages, sectors):
        suffix = "aggregate" if sector == agg else "per_sector"
        for obs in observables:
            for profile in profiles:
                a = indexed[("pi", "audit", profile, stage, sector) + obs]
                b = indexed[("pi", "target", profile, stage, sector) + obs]
                key = "pi_cross_" + suffix
                maxima[key] = max(maxima[key], *(abs(x-y) for x,y in zip(a,b)))
            for lane in lanes:
                a = indexed[("pi", lane, "fine", stage, sector) + obs]
                b = indexed[("pi", lane, "tight", stage, sector) + obs]
                key = "pi_fine_tight_" + suffix
                maxima[key] = max(maxima[key], *(abs(x-y) for x,y in zip(a,b)))
    signed = table("ALL_SIGNED_OCCUPATIONS_AND_PAIRS.csv")
    require(len(signed) == 78, "signed rows")
    require({tuple(r[k] for k in ("kind", "site_i", "site_j")) for r in signed} == set(observables), "signed coverage")
    signed_table_error = 0.0
    for row in signed:
        obs = tuple(row[k] for k in ("kind", "site_i", "site_j"))
        for dwell, lane, profile in itertools.product(dwells, lanes, profiles):
            signed_table_error = max(signed_table_error, abs(float(row[f"{dwell}_{lane}_{profile}"])
                - indexed[(dwell, lane, profile, "after_transport", agg) + obs][2]))
    predictions = table("ALL_SIX_EVENTS_PREDICTION_VERSUS_RESULT.csv")
    require(len(predictions) == 132, "prediction count")
    unique_predictions = {(r["event"], r["partner_site"], r["profile"]) for r in predictions}
    require(len(unique_predictions) == 132, "duplicate prediction")
    require({r["profile"] for r in predictions} == set(profiles), "prediction profiles")
    require(len({(r["event"], r["partner_site"]) for r in predictions}) == 66, "distinct predictions")
    for profile in profiles:
        selected = [r for r in predictions if r["profile"] == profile]
        require(len(selected) == 66, "per-profile count")
        events = {r["event"] for r in selected}
        require(len(events) == 6 and all(sum(r["event"] == e for r in selected) == 11 for e in events), "event census")
    covariance_formula_error = max(abs(float(r["signed_prediction"]) - math.sin(math.pi/8)**2
                                  * float(r["weighted_loaded_genesis_covariance"])) for r in predictions)
    prediction_error = max(abs(float(r[f"{lane}_signed_delta"]) - float(r["signed_prediction"]))
                           for r in predictions for lane in lanes)
    prediction_cross = max(abs(float(r["target_signed_delta"]) - float(r["audit_signed_delta"])) for r in predictions)
    require(max(signed_error, aggregation_error, start_error, signed_table_error, covariance_formula_error) <= TOL,
            "table consistency")
    out.update(table_rows=len(rows), scientific_coverage="2 dwells x 2 lanes x 2 settings x 2 stages x 8 sector/aggregate labels x 78 observables",
               signed_arithmetic_max_error=signed_error, sector_sum_max_error=aggregation_error,
               fresh_start_readout_max_error=start_error, signed_table_max_error=signed_table_error,
               covariance_formula_max_error=covariance_formula_error,
               covariance_prediction_max_error=prediction_error,
               covariance_cross_lane_max_error=prediction_cross, table_only_comparisons=maxima)
    out["prediction_signs_fine"] = {label:sum(test(float(r["signed_prediction"])) for r in predictions if r["profile"] == "fine")
        for label,test in (("positive",lambda x:x>0),("negative",lambda x:x<0),("zero",lambda x:x==0))}
    selected = [r for r in signed if r["kind"] == "occupation"]
    largest_occ = max(selected, key=lambda r:abs(float(r["pi_target_tight"])))
    largest_pair = max((r for r in signed if r["kind"] == "pair"), key=lambda r:abs(float(r["pi_target_tight"])))
    out["largest_pi_target_tight"] = {"occupation": [largest_occ["site_i"],float(largest_occ["pi_target_tight"])],
        "pair":[largest_pair["site_i"],largest_pair["site_j"],float(largest_pair["pi_target_tight"])]}
    out["phase_facade_sha256"] = digest(archive.read(ROOT + "sources/DEVELOPMENT_R_L6_PI_TRANSPORT_COMPLETION_V002/phase_facade.py"))
    out["scope"] = "Internal consistency and returned table arithmetic only; no physics re-execution, source-lineage replay, full error proof, remote live status, or DM/DE validation."
print(json.dumps(out, sort_keys=True, indent=2))
