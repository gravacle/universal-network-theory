#!/usr/bin/env python3
"""Inert source transformer: stdout receipt only; never compile, run, or write."""
import base64
import difflib
import hashlib
import json
from pathlib import Path

J = Path(__file__).resolve().parent
ROOT = Path("/Users/bgm/Documents/ChatGPT/Universal Network Theory")
B = J / "bbn_inputs_v001/primat_c_reference_v001"
PINS = {
    "plasma.c": "ecf991cb5aeee8c9744c34a4c0924fb3509eeadf08e23120bb939665fddb539c",
    "weak_rates.c": "c535a4ba63ed76f1ea878e21757758e8602cadf81db997bcee212b3078a5f49e",
}
MANIFEST_SHA = "5ec0ccea45d547b639ebcdaf86f059b1518256ea6e709829ec0e47980e4cc38e"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def once(text, old, new):
    if text.count(old) != 1:
        raise ValueError("nonunique/missing exact source anchor: " + old[:100])
    return text.replace(old, new, 1)


TABLE_HELPER = r'''
/* UNT derived read-only input guard. No change to valid table arithmetic. */
static int unt_ro_table_valid(const CPRTable *t, size_t nc, size_t nr)
{
    if (t->n_cols != nc || t->n_rows < nr) return 0;
    for (size_t i = 0; i < t->n_rows; i++) {
        if (!(t->cols[0][i] > 0.0) ||
            (i && !(t->cols[0][i] > t->cols[0][i-1]))) return 0;
        for (size_t k = 0; k < nc; k++)
            if (!isfinite(t->cols[k][i])) return 0;
    }
    return 1;
}
'''


def transform_plasma(s):
    s = once(s, "/* Below Tg = me / _ELEC_THERMO_LOWT_RATIO", TABLE_HELPER + "\n/* Below Tg = me / _ELEC_THERMO_LOWT_RATIO")
    s = once(s, "    free(qed_fp_hash);\n\n    if (recompute || !files_present) {", r'''    free(qed_fp_hash);
    /* UNT: reject legacy/missing/stale/recompute paths before generation. */
    if (recompute || !split_valid) {
        *errmsg = strdup("UNT readonly: matching current QED pair required; generation/legacy fallback disabled");
        return 1;
    }

    if (recompute || !files_present) {''')
    s = once(s, "        CPRInterp1D *targets[3] = { &pl->P_QED, &pl->dP_QED, &pl->d2P_QED };\n        for (int k = 0; k < 3; k++) {\n            targets[k]->is_spline = 0;\n            targets[k]->n = tab_e2.n_rows;", r'''        int valid = unt_ro_table_valid(&tab_e2, 4, 4)
                 && unt_ro_table_valid(&tab_e3, 4, 4)
                 && tab_e2.n_rows == tab_e3.n_rows;
        if (valid) for (size_t i = 0; i < tab_e2.n_rows; i++)
            if (tab_e2.cols[0][i] != tab_e3.cols[0][i]) valid = 0;
        if (!valid) {
            cpr_table_free(&tab_e2); cpr_table_free(&tab_e3);
            *errmsg = strdup("UNT readonly: invalid or mismatched QED table grids");
            return 1;
        }
        CPRInterp1D *targets[3] = { &pl->P_QED, &pl->dP_QED, &pl->d2P_QED };
        for (int k = 0; k < 3; k++) {
            targets[k]->is_spline = 0;
            targets[k]->n = tab_e2.n_rows;''')
    s = once(s, "            if (cpr_table_read(cache_read, 5, &tab, &read_err) == 0) {\n                int rc =", r'''            if (cpr_table_read(cache_read, 5, &tab, &read_err) == 0) {
                if (!unt_ro_table_valid(&tab, 5, 4)) {
                    cpr_table_free(&tab); free(fp_hash);
                    *errmsg = strdup("UNT readonly: invalid electron-thermo table");
                    return 1;
                }
                int rc =''')
    start = "            /* Fall through to recompute if the cache file turned out to"
    end = "            free(read_err);\n"
    a = s.index(start); b = s.index(end, a) + len(end)
    s = s[:a] + r'''            /* Preserve the original read error; never regenerate. */
            free(fp_hash);
            *errmsg = read_err ? read_err : strdup("UNT readonly: unreadable electron cache");
            return 1;
''' + s[b:]
    s = once(s, "    double *grid = CPR_XMALLOC(npts * sizeof(double));", r'''    /* UNT: every valid cache path above returns; no quadrature/write fallback. */
    free(fp_hash);
    *errmsg = strdup("UNT readonly: electron cache miss/mismatch or recompute requested");
    return 1;

    double *grid = CPR_XMALLOC(npts * sizeof(double));''')
    return s


def transform_weak(s):
    s = once(s, "static const double EXP_CUTOFF", TABLE_HELPER + "\nstatic const double EXP_CUTOFF")
    s = once(s, "    if (have_cache) {\n        cpr_log(cfg, \"weak\", \"background n<->p weak rates: loaded from cache.\");", r'''    char *unt_cached_hash = have_cache ? cpr_cache_read_fingerprint_hash(path) : NULL;
    int unt_match = unt_cached_hash && strcmp(unt_cached_hash, fp_hash) == 0;
    free(unt_cached_hash);
    if (!have_cache || !unt_match) {
        free(fp_hash); free(Tg_K); free(ratio);
        *errmsg = strdup("UNT readonly: matching nonthermal weak cache required; generation disabled");
        return 1;
    }
    if (have_cache) {
        cpr_log(cfg, "weak", "background n<->p weak rates: loaded from cache.");''')
    s = once(s, "        wr->n = tab.n_rows;", r'''        if (!unt_ro_table_valid(&tab, 3, 4)) {
            cpr_table_free(&tab); free(fp_hash); free(Tg_K); free(ratio);
            *errmsg = strdup("UNT readonly: invalid nonthermal weak table");
            return 1;
        }
        wr->n = tab.n_rows;''')
    s = once(s, "        FILE *f = fopen(th_path, \"r\");", r'''        char *unt_expected = cpr_fingerprint_hash(th_fields, n_th_fp);
        char *unt_actual = cpr_cache_read_fingerprint_hash(th_path);
        int unt_match_th = unt_actual && strcmp(unt_actual, unt_expected) == 0;
        free(unt_expected); free(unt_actual);
        if (!unt_match_th) {
            free(Tg_K); free(ratio); cpr_weak_rates_free(wr);
            *errmsg = strdup("UNT readonly: matching thermal weak cache required; VEGAS disabled");
            return 1;
        }
        FILE *f = fopen(th_path, "r");''')
    s = once(s, "            wr->n_th = tab.n_rows;", r'''            if (!unt_ro_table_valid(&tab, 3, 4)) {
                cpr_table_free(&tab); free(Tg_K); free(ratio); cpr_weak_rates_free(wr);
                *errmsg = strdup("UNT readonly: invalid thermal weak table");
                return 1;
            }
            wr->n_th = tab.n_rows;''')
    s = once(s, "        } else {\n            /* No matching cache file: compute CCRTh from scratch", r'''        } else {
            free(Tg_K); free(ratio); cpr_weak_rates_free(wr);
            *errmsg = strdup("UNT readonly: thermal cache became unreadable; VEGAS disabled");
            return 1;
            /* No matching cache file: compute CCRTh from scratch''')
    return s


def main():
    expected = ROOT / "UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation"
    if J != expected or Path.cwd().resolve() != ROOT:
        raise ValueError("wrong project/transformer context")
    mraw = (B / "PRIMAT_C_READONLY_DEPENDENCY_MANIFEST_V001.json").read_bytes()
    if sha(mraw) != MANIFEST_SHA:
        raise ValueError("dependency manifest changed")
    out = []
    for name, transform in [("plasma.c", transform_plasma), ("weak_rates.c", transform_weak)]:
        source = B / ("primat-c__src__" + name + ".txt")
        raw = source.read_bytes()
        if sha(raw) != PINS[name]:
            raise ValueError("upstream source changed: " + name)
        text = raw.decode("utf-8", errors="strict")
        modified = transform(text)
        encoded = modified.encode("utf-8")
        diff = "".join(difflib.unified_diff(text.splitlines(True), modified.splitlines(True),
                      fromfile="upstream/primat-c/src/" + name,
                      tofile="derived_ordinary_v001/" + name))
        out.append(dict(path="derived_ordinary_v001/" + name, source_path=str(source.relative_to(J)),
                        source_sha256=sha(raw), bytes=len(encoded), sha256=sha(encoded),
                        data_base64=base64.b64encode(encoded).decode("ascii"), unified_diff=diff))
    print(json.dumps(dict(schema="PRIMAT_READONLY_DERIVATION_V001", status="DERIVED_NOT_COMPILED_OR_RUN",
                          transformer_sha256=sha(Path(__file__).read_bytes()),
                          dependency_manifest_sha256=MANIFEST_SHA, files=out), sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"schema": "PRIMAT_READONLY_DERIVATION_V001", "status": "FAILED_DERIVATION",
                          "error_type": type(exc).__name__, "error": str(exc)}))
        raise SystemExit(1)
