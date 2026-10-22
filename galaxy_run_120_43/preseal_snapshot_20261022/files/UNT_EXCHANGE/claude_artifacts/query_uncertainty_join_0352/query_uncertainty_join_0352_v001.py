#!/usr/bin/env python3
"""0352 query x uncertainty/missingness join (CLAUDE2 helper 0352-join).

Read-only documentary join. It reads the root-run coverage output (saved), the
source-only bundle (labels, edges, mask fractions, open issues only), the 0341
ledger/crosswalk and the 0346 correction, and writes ONE JSON file with an
exclusive create. It does not rerun any adapter, never reads value_literal,
error_literal, mass, effective-density, area or scatter fields, performs no
interpolation, resampling, unit or distance conversion, and makes no source,
threshold or physical choice.

usage: python3 -I query_uncertainty_join_0352_v001.py <output_json_path>
"""
import hashlib
import json
import os
import sys
from decimal import Decimal
from fractions import Fraction

CODEX1 = ("/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/"
          "FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/")
XCH = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/"
PINS = {
    "coverage": (CODEX1 + "NGC3198_QUERY_SOURCE_COVERAGE_CANDIDATE_V001.json",
                 "d22ea85089de3fbe3017482fffeaf47a0a1a8bb63d49bcbc44124b62f9787f82"),
    "coverage_root_review": (CODEX1 + "NGC3198_QUERY_COVERAGE_ROOT_SAVED_OUTPUT_REVIEW_V001.json",
                             "f008725d84a2775be5b6dc34d3251ed9a96edf38be654a842937197957af05e4"),
    "bundle": (CODEX1 + "NGC3198_SOURCE_ONLY_BUNDLE_CANDIDATE_V001.json",
               "62abc88f12cb9da99ea1f1ba27c7eab2454553391984a65e2aa87a155fcc1fc1"),
    "crosswalk_0341": (XCH + "source_crosswalk_0341/SOURCE_CROSSWALK_V001.json",
                       "691483835e9d5201957a2b7183deaa1e8d994efeaa2644c3374d8e59f2450c72"),
    "ledger_0341": (XCH + "source_crosswalk_0341/UNCERTAINTY_MISSING_INPUT_LEDGER_V001.json",
                    "07dd4aa300b8b818a2b962646dffd3711f461cccfa87052f7f9d760e4fdb29e0"),
    "correction_0346": (XCH + "source_crosswalk_0341/SOURCE_CROSSWALK_CORRECTION_0346_V001.json",
                        "988e871acc0e6f3c1e3b91abec7143cb5b69241d6894b140f15369a6f29fca24"),
    "context_query_coverage_contract_V002": (XCH + "query_coverage_0350/QUERY_COVERAGE_FIELD_CONTRACT_V002.json", None),
    "context_source_bundle_contract_V006": (XCH + "source_adapter_write_0348/SOURCE_BUNDLE_FIELD_CONTRACT_V006.json", None),
}

BUNDLE_FORBIDDEN_SUBSTRINGS = ("value_literal", "error_literal", "mass", "effective_HI",
                               "nominal_disk_area", "plane_pc2", "cosi_times")


class JoinError(Exception):
    pass


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def no_dup(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise JoinError("E_JSON_DUPLICATE_KEY " + k)
        out[k] = v
    return out


def bad_const(tok):
    raise JoinError("E_JSON_NONFINITE_TOKEN " + tok)


def load_pinned(name):
    path, pin = PINS[name]
    with open(path, "rb") as fh:
        raw = fh.read()
    h = sha256_bytes(raw)
    if pin is not None and h != pin:
        raise JoinError("E_PIN " + name + " " + h)
    obj = json.loads(raw.decode("utf-8"), object_pairs_hook=no_dup,
                     parse_float=lambda s: s, parse_constant=bad_const)
    return obj, {"role": name, "file": path, "sha256": h, "bytes": len(raw),
                 "pin_verified": pin is not None}


def hash_only(name):
    path, _ = PINS[name]
    with open(path, "rb") as fh:
        raw = fh.read()
    return {"role": name, "file": path, "sha256": sha256_bytes(raw), "bytes": len(raw),
            "pin_verified": False, "use": "context only; hashed, not parsed by this script"}


def bundle_get(bundle, pointer):
    """Resolve a bundle-relative pointer; refuses forbidden value fields."""
    for s in BUNDLE_FORBIDDEN_SUBSTRINGS:
        if s in pointer:
            raise JoinError("E_FORBIDDEN_POINTER " + pointer)
    cur = bundle
    for seg in pointer.split("/")[1:]:
        seg = seg.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, list):
            cur = cur[int(seg)]
        else:
            cur = cur[seg]
    return cur


def frac(text):
    return Fraction(Decimal(text))


def round_text(text, places):
    q = Decimal(1).scaleb(-places)
    return str(Decimal(text).quantize(q))


def corr_class(state):
    for tok in ("PRIMARY-STATED", "PROGRAM-DECLARED", "SECONDARY", "PRIMARY", "CITED"):
        if state.startswith(tok):
            return tok
    return "UNCLASSIFIED"


def main(argv):
    if len(argv) != 2:
        raise JoinError("E_USAGE")
    out_path = os.path.abspath(argv[1])
    if os.path.lexists(out_path):
        raise JoinError("E_OUTPUT_EXISTS " + out_path)
    with open(os.path.abspath(__file__), "rb") as fh:
        script_sha = sha256_bytes(fh.read())

    cov, pin_cov = load_pinned("coverage")
    rev, pin_rev = load_pinned("coverage_root_review")
    bun, pin_bun = load_pinned("bundle")
    cw, pin_cw = load_pinned("crosswalk_0341")
    led, pin_led = load_pinned("ledger_0341")
    cor, pin_cor = load_pinned("correction_0346")
    ctx = [hash_only("context_query_coverage_contract_V002"),
           hash_only("context_source_bundle_contract_V006")]

    # ---- binding checks (identity only) ----
    checks = []
    def chk(name, ok, detail):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})
        if not ok:
            raise JoinError("E_CHECK " + name)
    chk("root_review_names_coverage_sha", rev["output"]["sha256"] == pin_cov["sha256"], rev["output"]["sha256"])
    chk("root_review_names_bundle_sha", rev["input"]["sha256"] == pin_bun["sha256"], rev["input"]["sha256"])
    chk("root_review_status", rev["status"] == "PASS_METADATA_CORRESPONDENCE_ONLY" and rev["mismatches"] == [], rev["status"])
    chk("coverage_names_bundle_sha", cov["inputs"]["bundle"]["sha256"] == pin_bun["sha256"], cov["inputs"]["bundle"]["sha256"])
    chk("correction_binds_crosswalk", cor["corrects"]["sha256"] == pin_cw["sha256"] and cor["corrects"]["unchanged"] is True, cor["corrects"]["sha256"])
    chk("bundle_open_issues_pin_ledger", bun["open_issues"]["ref_files"]["ledger"]["sha256"] == pin_led["sha256"], "ledger sha in bundle /open_issues/ref_files/ledger")
    chk("bundle_open_issues_pin_correction", bun["open_issues"]["ref_files"]["crosswalk_correction"]["sha256"] == pin_cor["sha256"], "correction sha in bundle /open_issues/ref_files/crosswalk_correction")
    queries = cov["queries"]
    chk("coverage_43_queries", len(queries) == 43, len(queries))

    # ---- 0346 correction classes ----
    corrections = {}
    for c in cor["corrections"]:
        parts = {}
        for k, v in c["now"].items():
            if isinstance(v, dict) and "state" in v:
                parts[k] = {"state": v["state"], "class": corr_class(v["state"])}
            elif isinstance(v, dict):
                for k2, v2 in v.items():
                    if isinstance(v2, dict) and "state" in v2:
                        parts[k + "/" + k2] = {"state": v2["state"], "class": corr_class(v2["state"])}
        corrections[c["id"]] = {"crosswalk_pointer": c["crosswalk_pointer"],
                                "correction_pointer": "correction_0346:/corrections/%d" % cor["corrections"].index(c),
                                "parts": parts,
                                "classes": sorted(set(p["class"] for p in parts.values()))}

    def corr_refs(ids):
        return [{"id": i, "classes": corrections[i]["classes"],
                 "crosswalk_pointer": corrections[i]["crosswalk_pointer"]} for i in ids]

    # ---- ledger items ----
    L = {it["id"]: it for it in led["items"]}
    chk("ledger_U1_U19", sorted(L, key=lambda s: int(s[1:])) == ["U%d" % i for i in range(1, 20)], len(L))
    ledger_index = {it["id"]: i for i, it in enumerate(led["items"])}

    # ---- bundle OPEN items and their ledger/correction refs ----
    open_items = []
    for i, it in enumerate(bun["open_issues"]["items"]):
        led_refs, cor_refs, other = [], [], []
        for r in it["refs"]:
            if r.startswith("ledger:/items/"):
                led_refs.append(led["items"][int(r.split("/")[-1])]["id"])
            elif r.startswith("crosswalk_correction:/corrections/"):
                cor_refs.append(cor["corrections"][int(r.split("/")[-1])]["id"])
            elif r == "crosswalk_correction:/corrections":
                cor_refs.extend(sorted(corrections))
            else:
                other.append(r)
        open_items.append({"id": it["id"], "bundle_pointer": "/open_issues/items/%d" % i,
                           "topic": it["topic"], "state": it["state"],
                           "ledger_ids": led_refs, "correction_ids": cor_refs, "other_refs": other})
    OPEN = {o["id"]: o for o in open_items}
    cov_open_ids = [o["id"] for o in cov["context"]["open_issue_refs"]]

    # ---- S1 labels over all 23 bundle rows ----
    s1rows = bun["sources"]["S1_LEROY_T7"]["rows"]
    row_labels = {}
    for r in s1rows:
        ri = r["row_index"]
        row_labels[ri] = {}
        for c in ("HI", "H2", "stars"):
            base = "/sources/S1_LEROY_T7/rows/%d/components/%s" % (ri, c)
            row_labels[ri][c] = {
                "p53_interpretation": bundle_get(bun, base + "/p53_interpretation/value"),
                "error_kind": bundle_get(bun, base + "/error_kind/adapter_label"),
                "bundle_pointer": base}
        row_labels[ri]["_radius_literal"] = r["radius_kpc_literal"]["value"]
        row_labels[ri]["_line"] = r["original_line_number"]["value"]
    U9_rows = [(ri, c) for ri in row_labels for c in ("HI", "H2", "stars")
               if row_labels[ri][c]["p53_interpretation"] == "UPPER_LIMIT_NOTE3"]
    U10_rows = [(ri, c) for ri in row_labels for c in ("HI", "H2", "stars")
                if row_labels[ri][c]["error_kind"] == "LITERAL_ZERO_MEANING_UNRESOLVED"]
    U11_rows = [(ri, c) for ri in row_labels for c in ("HI", "H2", "stars")
                if row_labels[ri][c]["p53_interpretation"] == "MISSING"]
    chk("U11_rows_equal_OPEN4_computed",
        [ri for ri, c in U11_rows if c == "H2"] == bun["open_issues"]["items"][3]["computed"]["missing_rows"]
        and all(c == "H2" for _, c in U11_rows), "H2 MISSING rows vs OPEN-4 computed")

    # ---- S2 stored edges / mask fractions (metadata only) ----
    s2 = bun["sources"]["S2_HALOGAS_PLANAR"]
    prof = {}
    for o in s2["orders"]:
        oi = o["order_index"]
        for pn in ("profile_40arcsec", "profile_120arcsec"):
            base = "/sources/S2_HALOGAS_PLANAR/orders/%d/profiles/%s" % (oi, pn)
            pr = o["profiles"][pn]
            prof[(oi, pn)] = {
                "base": base,
                "r_lo": pr["r_lo_kpc"]["values"], "r_hi": pr["r_hi_kpc"]["values"],
                "complete": pr["complete_by_conservative_chord_bound"]["values"],
                "n_bins": pr["n_bins"]["derived_count"],
                "width": pr["width_arcsec"]["value"],
                "zero": {g: pr["groups"][g]["zero_fraction_of_footprint"]["values"] for g in ("full", "X_negative", "X_nonnegative")},
                "finite": {g: pr["groups"][g]["finite_fraction_of_footprint"]["values"] for g in ("full", "X_negative", "X_nonnegative")},
                "subpix": o["subpixels_per_axis"]["value"]}

    # identify ledger-named 120-arcsec annuli BY STORED EDGES (prose text used only to find the match)
    def find_annulus(oi, lo_txt, hi_txt, places):
        p = prof[(oi, "profile_120arcsec")]
        hits = [j for j in range(len(p["r_lo"]))
                if round_text(p["r_lo"][j], places) == lo_txt and round_text(p["r_hi"][j], places) == hi_txt]
        return hits
    U1_idx, U2_idx, U3_idx = {}, {}, {}
    for oi in (0, 1):
        h1 = find_annulus(oi, "40.1426", "48.1711", 4)
        h2 = find_annulus(oi, "32.11", "40.14", 2)
        chk("U1_unique_annulus_order%d" % oi, len(h1) == 1, h1)
        chk("U2_unique_annulus_order%d" % oi, len(h2) == 1, h2)
        U1_idx[oi], U2_idx[oi] = h1[0], h2[0]
        p = prof[(oi, "profile_120arcsec")]
        U3_idx[oi] = [j for j in range(len(p["r_lo"])) if frac(p["r_hi"][j]) <= frac(p["r_lo"][U2_idx[oi]])]

    # exact-text containment / overlap of 40-arcsec annuli with the U1 and U2 annuli
    def nested40(oi, j120):
        p120, p40 = prof[(oi, "profile_120arcsec")], prof[(oi, "profile_40arcsec")]
        lo, hi = frac(p120["r_lo"][j120]), frac(p120["r_hi"][j120])
        contained, overlap = [], []
        for j in range(len(p40["r_lo"])):
            a, b = frac(p40["r_lo"][j]), frac(p40["r_hi"][j])
            if a < hi and b > lo:
                overlap.append(j)
                if a >= lo and b <= hi:
                    contained.append(j)
        return contained, overlap

    # ---- per-query join ----
    SW_S1 = ["U12", "U13", "U16", "U17", "U18", "OPEN-1", "OPEN-2", "OPEN-5", "OPEN-6", "OPEN-8", "OPEN-9", "OPEN-10"]
    SW_S2 = ["U4", "U5", "U6", "U8", "U16", "U17", "OPEN-1", "OPEN-5", "OPEN-7", "OPEN-9", "OPEN-10"]
    per_query = []
    attach = {k: set() for k in ("U1", "U2", "U3", "U9", "U10", "U11", "U15", "U11_ABSENCE")}
    attach_entries = {k: [] for k in ("U1", "U2", "U3")}
    ur_hits = {k: set() for k in ("UR-1", "UR-2", "UR-3", "UR-4", "UR-5")}
    s1_status_count, s2_status_count = {}, {}
    label_check_count = 0
    pointer_check_count = 0
    U1_nested = {oi: nested40(oi, U1_idx[oi]) for oi in (0, 1)}

    for qi, q in enumerate(queries):
        qid = q["query_id"]
        rad = q["Rad_text"]
        S1 = q["S1"]
        s1_status_count[S1["status"]] = s1_status_count.get(S1["status"], 0) + 1
        s1_out = {"status": S1["status"], "coverage_pointer": "/queries/%d/S1" % qi, "rows": [],
                  "row_level_items": []}
        roles = [k for k in ("row", "lower_row", "upper_row") if k in S1]
        orient = [k for k in ("first_sampled_row", "last_sampled_row") if k in S1]
        for role in roles + orient:
            r = S1[role]
            comps = {}
            for c, v in r["components"].items():
                # cross-check stored labels against bundle labels at the stored pointer
                bl = row_labels[r["row_index"]][c]
                if not (bl["p53_interpretation"] == v["p53_interpretation"] and bl["error_kind"] == v["error_kind"]
                        and bl["bundle_pointer"] == v["bundle_pointer"]):
                    raise JoinError("E_S1_LABEL_MISMATCH %s %s" % (qid, c))
                label_check_count += 1
                comps[c] = {k: v[k] for k in ("p53_interpretation", "error_kind", "value_missing", "upper_limit_marker")}
            s1_out["rows"].append({"role": role if role in roles else role + " (orientation only; not attached)",
                                   "row_index": r["row_index"], "original_line_number": r["original_line_number"],
                                   "radius_literal": r["radius_literal"], "bundle_pointer": r["bundle_pointer"],
                                   "components": comps})
            if role not in roles:
                continue
            rel = "applies to a bracketing row (%s); not an interpolation claim" % role if S1["status"] == "BRACKETED" else "applies to the exact-sample row"
            for c, v in r["components"].items():
                if v["p53_interpretation"] == "UPPER_LIMIT_NOTE3" or v["upper_limit_marker"]:
                    s1_out["row_level_items"].append({"id": "U9", "open_id": "OPEN-8", "relation": rel, "pointer": v["bundle_pointer"],
                                                      "basis": "p53_interpretation %s; error_kind %s; upper_limit_marker %s (as stored)" % (v["p53_interpretation"], v["error_kind"], v["upper_limit_marker"])})
                    attach["U9"].add(qid)
                if v["error_kind"] == "LITERAL_ZERO_MEANING_UNRESOLVED":
                    s1_out["row_level_items"].append({"id": "U10", "open_id": "OPEN-8", "relation": rel, "pointer": v["bundle_pointer"],
                                                      "basis": "error_kind LITERAL_ZERO_MEANING_UNRESOLVED (as stored)"})
                    attach["U10"].add(qid)
                if v["p53_interpretation"] == "MISSING" or v["value_missing"]:
                    s1_out["row_level_items"].append({"id": "U11", "open_id": "OPEN-4", "relation": rel, "pointer": v["bundle_pointer"],
                                                      "basis": "p53_interpretation MISSING; value_missing %s (null, never zero)" % v["value_missing"]})
                    attach["U11"].add(qid)
        if S1["status"] in ("ABOVE_SAMPLED_RANGE", "BELOW_SAMPLED_RANGE"):
            s1_out["note"] = ("no S1 row stands in for this query; S1 row-level and S1 source-wide items are not attached; "
                              "the orientation row's flags are carried as stored only")
        else:
            s1_out["note"] = S1.get("note")
            if s1_out["row_level_items"]:
                ur_hits["UR-4"].add(qid)

        s2_out = []
        for k, e in enumerate(q["S2"]):
            oi, pn = e["order_index"], e["profile"]
            setting = "order%d_sub%d_%s" % (oi, e["subpixels_per_axis"], pn.replace("profile_", "w"))
            s2_status_count[e["status"]] = s2_status_count.get(e["status"], 0) + 1
            ent = {"setting": setting, "coverage_pointer": "/queries/%d/S2/%d" % (qi, k),
                   "order_index": oi, "subpixels_per_axis": e["subpixels_per_axis"], "profile": pn,
                   "status": e["status"], "annulus_items": [], "unresolved_refs": []}
            if e["status"] == "IN_ANNULUS":
                j = e["annulus_index"]
                p = prof[(oi, pn)]
                # pointer resolution check (edges, completeness, mask fractions) against the bundle
                ok = (bundle_get(bun, e["edge_pointers"]["r_lo"]) == e["inner_edge_as_stored"]["decimal_as_stored"]
                      and bundle_get(bun, e["edge_pointers"]["r_hi"]) == e["outer_edge_as_stored"]["decimal_as_stored"]
                      and bundle_get(bun, e["complete_pointer"]) == e["complete_by_conservative_chord_bound"])
                for g in ("full", "X_negative", "X_nonnegative"):
                    for f in ("zero_fraction_of_footprint", "finite_fraction_of_footprint", "missing_footprint_fraction_raw"):
                        ok = ok and bundle_get(bun, e["groups"][g]["pointers"][f]) == e["groups"][g][f]["decimal_as_stored"]
                if not ok:
                    raise JoinError("E_S2_POINTER_TEXT %s %d" % (qid, k))
                pointer_check_count += 1
                ent.update({"annulus_index": j,
                            "inner_edge_as_stored": e["inner_edge_as_stored"]["decimal_as_stored"],
                            "outer_edge_as_stored": e["outer_edge_as_stored"]["decimal_as_stored"],
                            "edge_pointers": e["edge_pointers"],
                            "query_equals_inner_edge": e["query_equals_inner_edge"],
                            "complete_by_conservative_chord_bound": e["complete_by_conservative_chord_bound"],
                            "groups_as_stored": {g: {"zero_fraction_of_footprint": e["groups"][g]["zero_fraction_of_footprint"]["decimal_as_stored"],
                                                     "finite_fraction_of_footprint": e["groups"][g]["finite_fraction_of_footprint"]["decimal_as_stored"],
                                                     "missing_footprint_fraction_raw": e["groups"][g]["missing_footprint_fraction_raw"]["decimal_as_stored"],
                                                     "effective_density_present": e["groups"][g]["effective_density_present"]}
                                                 for g in ("full", "X_negative", "X_nonnegative")}})
                zp = lambda g: e["groups"][g]["pointers"]["zero_fraction_of_footprint"]
                if pn == "profile_120arcsec":
                    if j == U1_idx[oi]:
                        ent["annulus_items"].append({"id": "U1", "open_id": "OPEN-7", "literal_scope": "annulus %d, group full" % j,
                                                     "pointer": zp("full"),
                                                     "basis": "stored annulus_index %d edges round (4 dp) to the ledger text 40.1426-48.1711; ledger state REVIEW-FLAGGED; no threshold" % j})
                        ent["unresolved_refs"].append("UR-1")
                        attach["U1"].add(qid); attach_entries["U1"].append(ent["coverage_pointer"]); ur_hits["UR-1"].add(qid)
                    elif j == U2_idx[oi]:
                        ent["annulus_items"].append({"id": "U2", "literal_scope": "annulus %d" % j, "pointer": zp("full"),
                                                     "basis": "stored annulus_index %d edges round (2 dp) to the ledger text 32.11-40.14; state REPORTED, NOT FLAGGED; no reliability class" % j})
                        attach["U2"].add(qid); attach_entries["U2"].append(ent["coverage_pointer"])
                    elif j in U3_idx[oi]:
                        ent["annulus_items"].append({"id": "U3", "literal_scope": "annulus %d" % j, "pointer": zp("full"),
                                                     "basis": "stored annulus_index %d lies below the U2 annulus inner edge; state REPORTED; zero mask fraction is not a detection-completeness statement" % j})
                        attach["U3"].add(qid); attach_entries["U3"].append(ent["coverage_pointer"])
                else:
                    cont, ovl = U1_nested[oi]
                    if j in ovl:
                        ent["unresolved_refs"].append("UR-2"); ur_hits["UR-2"].add(qid)
                    nonzero = [g for g in ("full", "X_negative", "X_nonnegative")
                               if frac(e["groups"][g]["zero_fraction_of_footprint"]["decimal_as_stored"]) != 0]
                    if nonzero:
                        ent["unresolved_refs"].append("UR-3"); ur_hits["UR-3"].add(qid)
            else:
                ent["final_outer_edge_as_stored"] = e.get("final_outer_edge_as_stored")
            s2_out.append(ent)

        ql = []
        radf = Fraction(Decimal(rad))
        if radf > Fraction(Decimal("21.42")):
            ql.append({"id": "U15", "open_id": "OPEN-3", "basis": "LEDGER-STATED by prose band (\"Queries 21.42-44.08 kpc (12)\"); S3/S4 grids are not in the bundle or coverage output, so no stored pointer exists",
                       "pointer": "ledger_0341:/items/%d" % ledger_index["U15"]})
            attach["U15"].add(qid); ur_hits["UR-5"].add(qid)
            if radf > Fraction(Decimal("42.8435")):
                ql[-1]["sub_statement"] = "ledger: lies beyond the last .dens row (prose 42.8435 / 42.84 kpc)"
        if S1["status"] == "ABOVE_SAMPLED_RANGE":
            ql.append({"id": "U11", "open_id": "OPEN-4", "basis": "absence statement: no S1 row (ABOVE_SAMPLED_RANGE) and ledger U11 'Outer H2: no source found within searched paths'; H2 is null, never zero",
                       "pointer": "ledger_0341:/items/%d" % ledger_index["U11"]})
            attach["U11_ABSENCE"].add(qid)
        has_s1 = S1["status"] in ("BRACKETED", "EXACT_SAMPLE_RADIUS")
        per_query.append({
            "query_id": qid, "Rad_text": rad, "Rad_unit": q["Rad_unit"],
            "coverage_pointer": "/queries/%d" % qi, "bundle_query_pointer": q["bundle_pointer"],
            "S1": s1_out, "S2": s2_out, "query_level_ledger_stated": ql,
            "source_wide_refs": {"via_S1_rows": SW_S1 if has_s1 else [], "via_S2_entries": SW_S2},
            "unresolved_refs": sorted(set([u for ent in s2_out for u in ent["unresolved_refs"]]
                                          + (["UR-4"] if has_s1 and s1_out["row_level_items"] else [])
                                          + (["UR-5"] if qid in ur_hits["UR-5"] else []))),
        })

    qorder = [q["query_id"] for q in queries]
    def ordered(s):
        return [x for x in qorder if x in s]
    s1_ids = [p["query_id"] for p in per_query if p["S1"]["status"] in ("BRACKETED", "EXACT_SAMPLE_RADIUS")]
    above_ids = [p["query_id"] for p in per_query if p["S1"]["status"] == "ABOVE_SAMPLED_RANGE"]
    all_ids = list(qorder)

    # ---- item classification ----
    def li(uid):
        it = L[uid]
        return {"source": it["source"], "item": it["item"], "ledger_state": it["state"],
                "ledger_pointer": "ledger_0341:/items/%d" % ledger_index[uid]}
    U1_rows_txt = {oi: [prof[(oi, "profile_120arcsec")]["r_lo"][U1_idx[oi]], prof[(oi, "profile_120arcsec")]["r_hi"][U1_idx[oi]]] for oi in (0, 1)}
    classification = {}
    def cls(uid, scope, **kw):
        d = li(uid); d["scope_class"] = scope
        d["open_ids"] = [o["id"] for o in open_items if uid in o["ledger_ids"]]
        d.update(kw); classification[uid] = d
    cls("U1", "ANNULUS_LEVEL", targets=[{"order_index": oi, "profile": "profile_120arcsec", "annulus_index": U1_idx[oi],
                                          "r_lo_as_stored": U1_rows_txt[oi][0], "r_hi_as_stored": U1_rows_txt[oi][1],
                                          "zero_fraction_pointer_full": prof[(oi, "profile_120arcsec")]["base"] + "/groups/full/zero_fraction_of_footprint/values/%d" % U1_idx[oi]}
                                         for oi in (0, 1)],
        identification="by stored annulus_index/edges; the prose band only located the match", literal_group="full", unresolved=["UR-1", "UR-2"])
    cls("U2", "ANNULUS_LEVEL", targets=[{"order_index": oi, "profile": "profile_120arcsec", "annulus_index": U2_idx[oi]} for oi in (0, 1)], note="reported, not flagged; no reliability class")
    cls("U3", "ANNULUS_LEVEL", targets=[{"order_index": oi, "profile": "profile_120arcsec", "annulus_indices": U3_idx[oi]} for oi in (0, 1)], note="reported zero fraction; not a completeness statement")
    cls("U4", "SOURCE_WIDE", applies_to="S2: every complete_by_conservative_chord_bound flag (geometric image coverage only, not support)")
    cls("U5", "SOURCE_WIDE", applies_to="S2: all entries; bundle /sources/S2_HALOGAS_PLANAR/measurement_uncertainty state UNKNOWN (never zero)")
    cls("U6", "SOURCE_WIDE", applies_to="S2: all entries (reduction dependency on a kinematic window)")
    cls("U7", "SOURCE_WIDE", applies_to="S2: no query entry (ledger: outside the complete aperture and outside the query domain; every one of the 172 stored S2 entries is IN_ANNULUS in a complete annulus)")
    cls("U8", "SOURCE_WIDE", unresolved_dependency="GEOMETRY", corrections=corr_refs(["C6", "C4"]), applies_to="S2 working plane (all entries)")
    cls("U9", "ROW_LEVEL", targets=[{"row_index": ri, "component": c, "bundle_pointer": row_labels[ri][c]["bundle_pointer"]} for ri, c in U9_rows],
        note="only stored occurrence is listed; see disagreements D1")
    cls("U10", "ROW_LEVEL", targets=[{"row_index": ri, "component": c, "bundle_pointer": row_labels[ri][c]["bundle_pointer"]} for ri, c in U10_rows])
    cls("U11", "ROW_LEVEL", targets=[{"row_index": ri, "component": c, "bundle_pointer": row_labels[ri][c]["bundle_pointer"]} for ri, c in U11_rows],
        also="absence statement applies at query level to ABOVE_SAMPLED_RANGE queries (no row)")
    cls("U12", "SOURCE_WIDE", applies_to="S1: every row; /sources/S1_LEROY_T7/table_level/whole_covariance is null; each bracketing pair is two adjacent, beam-correlated rings")
    cls("U13", "SOURCE_WIDE", unresolved_dependency="CONVERSION", corrections=corr_refs(["C2", "C3"]), applies_to="S1: H2 rows where present (X_CO, line ratio) and stars rows (M/L); bundle /sources/S1_LEROY_T7/unknown_uncertainty")
    cls("U14", "SOURCE_WIDE", applies_to="S3 (not in bundle or coverage output): no stored setting, no per-query join")
    cls("U15", "QUERY_LEVEL_LEDGER_STATED", applies_to="queries named by the ledger prose band; S3/S4 grids not stored in the allowed inputs", unresolved=["UR-5"],
        note="not one of the four scope classes: the ledger names queries directly, and no stored S3/S4 pointer exists")
    cls("U16", "SOURCE_WIDE", unresolved_dependency="GEOMETRY_AND_DISTANCE", corrections=corr_refs(["C4", "C6"]), applies_to="all sources")
    cls("U17", "SOURCE_WIDE", unresolved_dependency="OVERLAPPING_HI", corrections=corr_refs(["C1", "C5", "C8"]), applies_to="S1 HI, S2, S5 (S5 not in bundle)")
    cls("U18", "SOURCE_WIDE", unresolved_dependency="STELLAR_CONVENTION", corrections=corr_refs(["C3", "C7", "C4"]), applies_to="S1 stars rows and S3 (not in bundle)")
    cls("U19", "SOURCE_WIDE", unresolved_dependency="CONVERSION", corrections=corr_refs(["C7"]), applies_to="S3/S4 (not in bundle or coverage output): no per-query join")

    # ---- source-wide list (once, by reference) ----
    source_wide = []
    for uid in ("U4", "U5", "U6", "U7", "U8", "U12", "U13", "U14", "U16", "U17", "U18", "U19"):
        c = classification[uid]
        source_wide.append({"id": uid, "ledger_state": c["ledger_state"], "applies_to": c["applies_to"],
                            "unresolved_dependency": c.get("unresolved_dependency"),
                            "corrections": c.get("corrections", []), "open_ids": c["open_ids"]})
    for oid, txt in (("OPEN-6", "S1 table_level raw_to_native_map is null; no observation-to-native map exists"),
                     ("OPEN-8", "S1 per-ring rms fields: measurement-vs-descriptive meaning not established (every PUBLISHED_PER_RING_RMS_FIELD component); U9/U10 are its row-level parts"),
                     ("OPEN-9", "no mapping, interpolation or extrapolation from source grids to query radii"),
                     ("OPEN-10", "primary conversion verification pending for C1-C8")):
        source_wide.append({"id": oid, "applies_to": txt,
                            "unresolved_dependency": "CONVERSION" if oid == "OPEN-10" else None,
                            "corrections": corr_refs(sorted(corrections)) if oid == "OPEN-10" else [],
                            "ledger_ids": OPEN[oid]["ledger_ids"]})

    # ---- unresolved list ----
    c1, o1 = U1_nested[0]
    unresolved = [
        {"id": "UR-1", "type": "APPLICABILITY", "item": "U1",
         "what": "whether the whole-annulus review caution transfers to the half-footprint group records X_negative and X_nonnegative of the same annulus",
         "named_choice": "group-transfer rule for an annulus-level review flag (the ledger figure matches the stored full-group zero fraction; the half groups carry their own stored zero fractions)",
         "candidate_query_ids": ordered(ur_hits["UR-1"]),
         "entries": "120-arcsec annulus %d, orders 0 and 1" % U1_idx[0]},
        {"id": "UR-2", "type": "APPLICABILITY", "item": "U1",
         "what": "whether the 120-arcsec review flag applies to 40-arcsec annuli in the same radial range",
         "named_choice": "a 120-to-40-arcsec transfer rule plus a containment-or-overlap rule at the 600-arcsec edge, whose stored text differs between the two profiles (see D3)",
         "exact_text_containment_40arcsec_indices": c1, "exact_text_overlap_40arcsec_indices": o1,
         "candidate_query_ids": ordered(ur_hits["UR-2"])},
        {"id": "UR-3", "type": "APPLICABILITY", "item": "none (no ledger statement for 40-arcsec rows)",
         "what": "40-arcsec annuli with a nonzero stored zero fraction in at least one group have no ledger classification",
         "named_choice": "a mask-fraction threshold or reliability rule for 40-arcsec annuli (the ledger sets none: U1 'No threshold is set here')",
         "candidate_query_ids": ordered(ur_hits["UR-3"])},
        {"id": "UR-4", "type": "APPLICABILITY", "item": "U9, U10, U11 on bracketing rows",
         "what": "the query-level consequence of an item on a bracketing row",
         "named_choice": "an S1 query-mapping/representation rule (OPEN-9), plus the primary Appendix E meaning of the e=1 marker (U9) and the meaning of the literal e=0 (U10); not made",
         "candidate_query_ids": ordered(ur_hits["UR-4"])},
        {"id": "UR-5", "type": "APPLICABILITY", "item": "U15",
         "what": "the ledger assignment rests on prose (last uncommented .sfb radius 320.16 arcsec, 21.42 kpc at 13.8 Mpc); the crosswalk records two commented .sfb rows at 352.17 and 387.39 arcsec and U14 says comment/kill semantics are undocumented",
         "named_choice": "whether commented .sfb rows count as observed stellar support; which queries this affects would need an arcsec-to-kpc conversion at the 13.8 Mpc convention (C4, SECONDARY), not performed here",
         "candidate_query_ids": ordered(ur_hits["UR-5"])},
        {"id": "UR-SW-GEOMETRY", "type": "SOURCE_WIDE_DEPENDENCY", "items": ["U8", "U16", "OPEN-5"],
         "named_choice": "geometry/distance model (fixed working plane vs tilted-ring/warp/thick disk; distance uncertainty); inputs missing per U16",
         "corrections": corr_refs(["C4", "C6"]), "candidate_query_ids": all_ids},
        {"id": "UR-SW-CONVERSION", "type": "SOURCE_WIDE_DEPENDENCY", "items": ["U13", "U19", "OPEN-10"],
         "named_choice": "none to make here: primary verification and uncertainties of conversion factors are missing inputs (deciding input: primary papers)",
         "corrections": corr_refs(sorted(corrections)), "candidate_query_ids_via_S1": s1_ids,
         "S2_conversion_note": "S2 conversion (1.25e20 per Msun/pc^2, helium factor) is PROGRAM-DECLARED per C5; no ledger U item covers it; carried via OPEN-10"},
        {"id": "UR-SW-HI-OVERLAP", "type": "SOURCE_WIDE_DEPENDENCY", "items": ["U17", "OPEN-1"],
         "named_choice": "crosswalk rule for which HI product is used where (counting the same HI once); ledger: a declared choice for root/principal",
         "corrections": corr_refs(["C1", "C5", "C8"]),
         "stored_co_presence": {"S1_BRACKETED_and_S2_IN_ANNULUS": s1_ids, "S2_only_among_bundle_sources": above_ids},
         "note": "co-presence is a stored-coverage fact, not an assignment; S5 is not in the bundle"},
        {"id": "UR-SW-STELLAR", "type": "SOURCE_WIDE_DEPENDENCY", "items": ["U18", "OPEN-2"],
         "named_choice": "stellar source/convention (Leroy vs SPARC conversion; inclination 72 vs 73)",
         "corrections": corr_refs(["C3", "C4", "C7"]), "candidate_query_ids_via_S1": s1_ids},
    ]

    # ---- issue -> query summary ----
    def ranges(ids):
        nums = sorted(int(x.rsplit("Q", 1)[1]) for x in ids)
        out, start, prev = [], None, None
        for n in nums:
            if start is None:
                start = prev = n
            elif n == prev + 1:
                prev = n
            else:
                out.append((start, prev)); start = prev = n
        if start is not None:
            out.append((start, prev))
        return ", ".join("Q%02d" % a if a == b else "Q%02d-Q%02d" % (a, b) for a, b in out)

    def rng(ids):
        return {"count": len(ids), "query_ranges": ranges(ids), "query_ids": ids}
    used_rows = set(r["row_index"] for p in per_query for r in p["S1"]["rows"] if "orientation" not in r["role"])
    def unreached(rows):
        return sorted(set(ri for ri, _ in rows if ri not in used_rows))
    summary = {
        "U1": dict(rng(ordered(attach["U1"])), via="120-arcsec annulus_index %d, orders 0 and 1, group full (literal)" % U1_idx[0], entries=attach_entries["U1"]),
        "U2": dict(rng(ordered(attach["U2"])), via="120-arcsec annulus_index %d, orders 0 and 1" % U2_idx[0]),
        "U3": dict(rng(ordered(attach["U3"])), via="120-arcsec annulus_indices %s, orders 0 and 1" % U3_idx[0]),
        "U9": dict(rng(ordered(attach["U9"])), via="bracketing row(s) %s" % sorted(set("%d/%s" % rc for rc in U9_rows)), rows_reaching_no_query=unreached(U9_rows)),
        "U10": dict(rng(ordered(attach["U10"])), via="stars rows %s on a bracketing row" % [ri for ri, _ in U10_rows], rows_reaching_no_query=unreached(U10_rows)),
        "U11": dict(rng(ordered(attach["U11"])), via="H2 MISSING on a bracketing row", rows_reaching_no_query_as_bracketing_row=unreached(U11_rows),
                    absence_statement_ABOVE=rng(ordered(attach["U11_ABSENCE"]))),
        "U15": dict(rng(ordered(attach["U15"])), via="ledger prose band (no stored pointer)", beyond_last_dens_row=[p["query_id"] for p in per_query if p["query_level_ledger_stated"] and any("sub_statement" in x for x in p["query_level_ledger_stated"])]),
        "U4": dict(rng(all_ids), via="S2 source-wide"), "U5": dict(rng(all_ids), via="S2 source-wide"),
        "U6": dict(rng(all_ids), via="S2 source-wide"), "U7": {"via": "no query entry", "count": 0},
        "U8": dict(rng(all_ids), via="S2 source-wide (geometry, unresolved)"),
        "U12": dict(rng(s1_ids), via="S1 source-wide (rows exist only for BRACKETED queries)"),
        "U13": dict(rng(s1_ids), via="S1 source-wide (conversion, unresolved)"),
        "U14": {"via": "S3 not in coverage; no per-query join", "count": None},
        "U16": dict(rng(all_ids), via="all sources (geometry/distance, unresolved)"),
        "U17": dict(rng(all_ids), via="S2 for all; S1 HI co-present for BRACKETED queries", S1_co_present=ranges(s1_ids)),
        "U18": dict(rng(s1_ids), via="S1 stars rows (S3 not stored)"),
        "U19": {"via": "S3/S4 not in coverage; no per-query join", "count": None},
        "UR-1": rng(ordered(ur_hits["UR-1"])), "UR-2": rng(ordered(ur_hits["UR-2"])),
        "UR-3": rng(ordered(ur_hits["UR-3"])), "UR-4": rng(ordered(ur_hits["UR-4"])),
        "UR-5": rng(ordered(ur_hits["UR-5"])),
    }

    # ---- prose vs exact saved coverage ----
    p0, p1 = prof[(0, "profile_120arcsec")], prof[(1, "profile_120arcsec")]
    z_full = {oi: prof[(oi, "profile_120arcsec")]["zero"]["full"][U1_idx[oi]] for oi in (0, 1)}
    fin_full = {oi: prof[(oi, "profile_120arcsec")]["finite"]["full"][U1_idx[oi]] for oi in (0, 1)}
    pct = {oi: round_text(str(Decimal(z_full[oi]) * 100), 2) for oi in (0, 1)}
    z2 = {oi: prof[(oi, "profile_120arcsec")]["zero"]["full"][U2_idx[oi]] for oi in (0, 1)}
    u3_all_zero = all(frac(prof[(oi, "profile_120arcsec")]["zero"][g][j]) == 0 for oi in (0, 1) for g in ("full", "X_negative", "X_nonnegative") for j in U3_idx[oi])
    hi_marker_rows = [ri for ri, c in U9_rows if c == "HI"]
    edge_mismatch_in_domain = []
    qmax = max(Fraction(Decimal(q["Rad_text"])) for q in queries)
    for oi in (0, 1):
        p40, p120 = prof[(oi, "profile_40arcsec")], prof[(oi, "profile_120arcsec")]
        for kk in range(len(p120["r_lo"])):
            a, b = p120["r_lo"][kk], p40["r_lo"][3 * kk]
            if a != b and frac(min(a, b, key=frac)) <= qmax:
                between = [q["query_id"] for q in queries if min(frac(a), frac(b)) <= Fraction(Decimal(q["Rad_text"])) < max(frac(a), frac(b))]
                edge_mismatch_in_domain.append({"order_index": oi, "edge_120_pointer": p120["base"] + "/r_lo_kpc/values/%d" % kk, "text_120": a,
                                                "edge_40_pointer": p40["base"] + "/r_lo_kpc/values/%d" % (3 * kk), "text_40": b,
                                                "queries_between": between})
    U2_nested = {oi: nested40(oi, U2_idx[oi]) for oi in (0, 1)}
    n_mismatch_total = sum(1 for oi in (0, 1) for kk in range(79) if prof[(oi, "profile_120arcsec")]["r_lo"][kk] != prof[(oi, "profile_40arcsec")]["r_lo"][3 * kk])

    band_counts = cw["query_domain"]["query_counts_by_source_support_band_kpc"]
    band_check = []
    for band, n in band_counts.items():
        lo, hi = band.split("-")
        cnt = sum(1 for q in queries if Fraction(Decimal(lo)) < Fraction(Decimal(q["Rad_text"])) <= Fraction(Decimal(hi))) if lo != "0" else \
              sum(1 for q in queries if Fraction(Decimal(q["Rad_text"])) <= Fraction(Decimal(hi)))
        band_check.append({"band_prose": band, "prose_count": n, "count_from_query_Rad_text": cnt, "agree": cnt == n})
    stored_band_check = {
        "S1_BRACKETED_vs_band_0-15.1": {"stored": len(s1_ids), "prose": band_counts["0-15.1"], "agree": len(s1_ids) == band_counts["0-15.1"]},
        "U2_annulus_members_vs_band_32.11-40.14": {"stored": len(attach["U2"]), "prose": band_counts["32.11-40.14"], "agree": len(attach["U2"]) == band_counts["32.11-40.14"]},
        "U1_annulus_members_vs_bands_40.14-48.17": {"stored": len(attach["U1"]), "prose": band_counts["40.14-42.8435"] + band_counts["42.8435-48.17"],
                                                    "agree": len(attach["U1"]) == band_counts["40.14-42.8435"] + band_counts["42.8435-48.17"]},
    }

    disagreements = [
        {"id": "D1", "kind": "PROSE_SCOPE (column-level note read as row occurrence)",
         "prose": ["ledger U9 item 'e=1.0 entries (HI rms; stars row 2)'", "bundle OPEN-8 'e=1 on HI/stars carries ReadMe Note 3'",
                   "crosswalk /sources/S1_LEROY_T7/error_fields/e_SigmaHI '1.0 carries Note 3'"],
         "saved": {"UPPER_LIMIT_NOTE3_occurrences": ["%d/%s" % rc for rc in U9_rows], "HI_rows_with_marker": hi_marker_rows},
         "finding": "In the saved bundle and coverage output the Note-3 marker occurs only at /sources/S1_LEROY_T7/rows/2/components/stars. No HI component of any of the 23 rows is labelled UPPER_LIMIT_NOTE3. Under the bundle adapter's validated rule (contract V006: error literal '1' on HI/stars iff UPPER_LIMIT_NOTE3; literals not read here), no NGC3198 HI row carries e=1. U9's 'HI rms' is column-level (Note 3 attached to e_SigmaHI), not a row occurrence.",
         "effect": "U9 attaches to Q04-Q07 through stars row 2 only; no query gets an HI upper-limit attachment."} if not hi_marker_rows else None,
        {"id": "D2", "kind": "PROSE_FIGURE_ORDER_UNSPECIFIED",
         "prose": ["ledger U1 '43.66% of finite sky area'", "crosswalk support_by_query_band '0.4366'", "bundle OPEN-7 '43.66%'"],
         "saved": {"order0_sub4_full_zero_fraction": z_full[0], "order1_sub8_full_zero_fraction": z_full[1],
                   "as_percent_2dp": {"order0": pct[0], "order1": pct[1]},
                   "finite_fraction_full": {"order0": fin_full[0], "order1": fin_full[1]},
                   "pointers": [prof[(oi, "profile_120arcsec")]["base"] + "/groups/full/zero_fraction_of_footprint/values/%d" % U1_idx[oi] for oi in (0, 1)]},
         "finding": "The single prose figure matches order index 1 (8 subpixels) after rounding; order index 0 (4 subpixels) rounds to %s%% and matches 43.66 only by truncation. The prose does not name an order. finite_fraction_of_footprint is 1.0 in both orders, so 'of finite sky area' and the stored 'of footprint' coincide here." % pct[0],
         "effect": "None on applicability: annulus_index %d holds Q42 and Q43 in both orders." % U1_idx[0]} if pct[0] != pct[1] else None,
        {"id": "D3", "kind": "STORED_EDGE_TEXT_NON_IDENTITY (between saved profiles, not ledger)",
         "saved": edge_mismatch_in_domain, "nested_edge_text_mismatches_all_annuli_per_order": n_mismatch_total // 2,
         "exact_text_nesting": {"U2_annulus_%d" % U2_idx[0]: {"contained_40arcsec": U2_nested[0][0], "overlapping_40arcsec": U2_nested[0][1]},
                                "U1_annulus_%d" % U1_idx[0]: {"contained_40arcsec": U1_nested[0][0], "overlapping_40arcsec": U1_nested[0][1]},
                                "same_in_order_1": U2_nested[0] == U2_nested[1] and U1_nested[0] == U1_nested[1]},
         "finding": "At the 600-arcsec edge the 120-arcsec profile stores 40.142572795869576 and the 40-arcsec profile stores 40.14257279586958; by exact Fraction comparison these differ, so 40-arcsec annulus 14 is contained in neither the U2 nor the U1 120-arcsec annulus and overlaps the U1 annulus by a sliver. Both texts are consistent with the prose '40.14'/'40.1426'. No query lies between the two values. Within the query domain this is the only nested edge whose text differs.",
         "effect": "None on stored assignments; it matters only for any 120-to-40 transfer rule (UR-2)."},
    ]
    disagreements = [d for d in disagreements if d is not None]

    consistent = [
        {"claim": "U1 identifies the outer 120-arcsec annulus 40.1426-48.1711 kpc",
         "saved": "annulus_index %d in both orders; stored r_lo %s, r_hi %s (identical text across orders)" % (U1_idx[0], U1_rows_txt[0][0], U1_rows_txt[0][1]), "agree": U1_rows_txt[0] == U1_rows_txt[1]},
        {"claim": "U1 'Applies to queries at 40.14-44.08 kpc (2 queries)'",
         "saved": "stored members (both orders): %s; Q41 (Rad_text 40.10) is in annulus %d" % (ordered(attach["U1"]), U2_idx[0]), "agree": len(attach["U1"]) == 2},
        {"claim": "'outer' in U1",
         "saved": "annulus %d of %d stored 120-arcsec annuli (complete prefix %d); 'outer' means the outermost annulus holding a query, not the last stored annulus" % (U1_idx[0], p0["n_bins"], sum(1 for x in p0["complete"] if x is True)),
         "agree": True},
        {"claim": "U2 annulus 32.11-40.14 kpc, zero/replaced 0.0402",
         "saved": "annulus_index %d; full zero fraction order0 %s, order1 %s; both round to 0.0402; members %s" % (U2_idx[0], z2[0], z2[1], ordered(attach["U2"])),
         "agree": round_text(z2[0], 4) == "0.0402" and round_text(z2[1], 4) == "0.0402"},
        {"claim": "U3 zero/replaced fraction 0 in all 120-arcsec rows 0-32.11 kpc",
         "saved": "annuli %s, all three groups, both orders: zero fraction 0" % U3_idx[0], "agree": u3_all_zero},
        {"claim": "U10 stars rows 16,18,19,20 e=0.0", "saved": "LITERAL_ZERO_MEANING_UNRESOLVED on %s; row 19 is a bracketing row for no query" % ["%d/%s" % rc for rc in U10_rows],
         "agree": [ri for ri, _ in U10_rows] == [16, 18, 19, 20]},
        {"claim": "U11 H2 rows 10-22 missing", "saved": "H2 MISSING rows %s (equals bundle OPEN-4 computed)" % [ri for ri, _ in U11_rows],
         "agree": [ri for ri, _ in U11_rows] == list(range(10, 23))},
        {"claim": "U15 '12 queries 21.42-44.08 kpc'", "saved": "%d queries with Rad_text > 21.42 (%s); no stored S3/S4 grid to check pointers against" % (len(attach["U15"]), ordered(attach["U15"])),
         "agree": len(attach["U15"]) == 12},
        {"claim": "crosswalk S2 grid: 40 arcsec x237, 120 arcsec x79; complete 51/17 bins to 136.4847 kpc",
         "saved": "n_bins %s/%s; complete prefix %d/%d; last complete r_hi %s" % (prof[(0, "profile_40arcsec")]["n_bins"], p0["n_bins"],
                  sum(1 for x in prof[(0, "profile_40arcsec")]["complete"] if x is True), sum(1 for x in p0["complete"] if x is True), p0["r_hi"][16]),
         "agree": prof[(0, "profile_40arcsec")]["n_bins"] == 237 and p0["n_bins"] == 79},
        {"claim": "crosswalk query band counts", "saved": band_check, "agree": all(b["agree"] for b in band_check)},
        {"claim": "crosswalk band counts vs stored coverage where a band edge is a stored edge", "saved": stored_band_check,
         "agree": all(v["agree"] for v in stored_band_check.values())},
    ]

    observations = [
        {"id": "N1", "text": "coverage /context/open_issue_refs lists %s; bundle OPEN items not listed there: %s. This join carries them from the bundle directly." % (
            cov_open_ids, [o["id"] for o in open_items if o["id"] not in cov_open_ids])},
        {"id": "N2", "text": "S1 status counts %s; S2 status counts %s (equal to the root review counts)" % (s1_status_count, s2_status_count)},
        {"id": "N3", "text": "S2 conversion conventions (1.25e20 per Msun/pc^2; helium factor) have no ledger U item; they are carried by correction C5 (PROGRAM-DECLARED) and OPEN-10"},
    ]
    chk("root_review_counts", s1_status_count.get("BRACKETED") == rev["counts"]["S1_BRACKETED"]
        and s1_status_count.get("ABOVE_SAMPLED_RANGE") == rev["counts"]["S1_ABOVE_SAMPLED_RANGE"]
        and s2_status_count.get("IN_ANNULUS") == rev["counts"]["S2_IN_ANNULUS"], [s1_status_count, s2_status_count])

    out = {
        "schema": "CLAUDE2_QUERY_UNCERTAINTY_JOIN_0352_V001",
        "task": "0352 (Codex1)",
        "status": "DOCUMENTARY JOIN; metadata only; no source, threshold, transfer rule or physical choice made",
        "generated_by": {"script": "query_uncertainty_join_0352_v001.py", "sha256": script_sha},
        "inputs": [pin_cov, pin_rev, pin_bun, pin_cw, pin_led, pin_cor] + ctx,
        "never_emitted": "density values, error literals, masses, areas, effective densities, descriptive scatter, velocities; no interpolation, resampling, unit or distance conversion, fitting or adapter rerun",
        "bundle_fields_read": ["/sources/S1_LEROY_T7/rows/{i}/{row_index,original_line_number/value,radius_kpc_literal/value}",
                               "/sources/S1_LEROY_T7/rows/{i}/components/{HI,H2,stars}/{p53_interpretation/value,error_kind/adapter_label}",
                               "/sources/S2_HALOGAS_PLANAR/orders/{0,1}/{order_index,subpixels_per_axis/value}",
                               "/sources/S2_HALOGAS_PLANAR/orders/{0,1}/profiles/{profile_40arcsec,profile_120arcsec}/{n_bins/derived_count,width_arcsec/value,r_lo_kpc/values,r_hi_kpc/values,complete_by_conservative_chord_bound/values}",
                               "/sources/S2_HALOGAS_PLANAR/orders/{0,1}/profiles/*/groups/{full,X_negative,X_nonnegative}/{zero_fraction_of_footprint,finite_fraction_of_footprint,missing_footprint_fraction_raw}/values (via pointers stored in the coverage output, text equality only)",
                               "/open_issues (items and ref_files)"],
        "bundle_fields_never_resolved": "value_literal, error_literal, mass_*, effective_HI_*, nominal_disk_area_pc2, plane_pc2, cosi_times_* (refused by bundle_get); effective_density_present is carried from the coverage output, not re-resolved",
        "notes": {"S2_40arcsec": "no ledger item is stated for 40-arcsec annuli; their mask fractions are carried as stored (bundle value_kinds mask_fraction_*: S2 mask bookkeeping); see UR-2 and UR-3",
                  "S1_bracketing": "an item on either bracketing row is recorded as 'applies to a bracketing row'; this is not an interpolation claim (coverage label note)",
                  "S1_above": "ABOVE_SAMPLED_RANGE queries have no S1 row; the last sampled row is carried for orientation only and receives no attachment",
                  "flags": "value_missing, upper_limit_marker and effective_density_present are copied exactly as stored in the coverage output",
                  "S1_component_pointer_rule": "component flags sit at bundle /sources/S1_LEROY_T7/rows/{row_index}/components/{HI,H2,stars} (as stored in the coverage output at the query's coverage_pointer); item attachments give the exact pointer"},
        "pointer_conventions": {"bundle": "pointers without prefix are bundle-relative (as stored in the coverage output)",
                                "coverage": "coverage_pointer values are relative to the coverage output",
                                "ledger_0341:": "UNCERTAINTY_MISSING_INPUT_LEDGER_V001.json", "correction_0346:": "SOURCE_CROSSWALK_CORRECTION_0346_V001.json"},
        "scope_classes": {"ROW_LEVEL": "literal S1 row component", "ANNULUS_LEVEL": "literal S2 stored annulus index",
                          "SOURCE_WIDE": "whole source or whole table; listed once, referenced by id",
                          "QUERY_LEVEL_LEDGER_STATED": "ledger names queries by a prose band; no stored pointer (U15 only)",
                          "UNRESOLVED_APPLICABILITY": "attachment needs a choice not made here (UR-1..UR-5)"},
        "corrections_0346": corrections,
        "item_classification": classification,
        "open_issue_crossref": open_items,
        "source_wide": source_wide,
        "unresolved": unresolved,
        "per_query": per_query,
        "issue_to_query_summary": summary,
        "disagreements": disagreements,
        "consistent_with_saved_coverage": consistent,
        "observations": observations,
        "checks": checks,
        "check_counts": {"S1_component_label_matches": label_check_count, "S2_entries_pointer_text_verified": pointer_check_count},
    }
    parts = []
    keys = list(out)
    for n, key in enumerate(keys):
        if key == "per_query":
            body = "[\n" + ",\n".join(json.dumps(x, separators=(",", ":"), ensure_ascii=True) for x in out[key]) + "\n]"
        else:
            body = json.dumps(out[key], indent=1, ensure_ascii=True)
        parts.append(json.dumps(key) + ": " + body + ("," if n < len(keys) - 1 else ""))
    text = "{\n" + "\n".join(parts) + "\n}\n"
    if json.loads(text) != out:
        raise JoinError("E_SERIALIZE")
    data = text.encode("ascii")
    fd = os.open(out_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    with os.fdopen(fd, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    with open(out_path, "rb") as fh:
        if fh.read() != data:
            raise JoinError("E_VERIFY")
    print(json.dumps({"status": "WRITTEN", "output": out_path, "sha256": sha256_bytes(data), "bytes": len(data)}))


if __name__ == "__main__":
    try:
        main(sys.argv)
    except JoinError as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}))
        sys.exit(2)
