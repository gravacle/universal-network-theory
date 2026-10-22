"""Dry, in-memory: phase1 freeze_spec (placeholder slots) vs Claude4 B2 fix (slots V003). Prints geometry leaves only."""
import copy
import hashlib
import importlib.util
import json
import sys

G_PATH = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py'
G_SHA = '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405'
SPEC = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/DDO154_COORDINATES_CX2V006.json',
        '50e7288e4697c8c8bca0544a4b81b5b15462c10efaed2d437530b95d8a80951f')
SPEC_V002 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_engine_freeze_v003b_v003d/orchestrator_v005a/DDO154_CALIBRATION_COORDINATE_SPEC_V002.json',
             '89e7d33e0376552e8b243e28abea5ed34e87134d18e3dba5bc92c1c60607855d')
ADD = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/COORDINATE_ADDENDUM_CX2V006.json',
       '9962b2aa673572a712d07fd74d12e61fe2418acbeb03b0ef3437118a6ca1e2b9')
SLOTS = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json',
         'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969')


def pinned(pin):
    b = open(pin[0], 'rb').read()
    assert hashlib.sha256(b).hexdigest() == pin[1], 'PIN MISMATCH ' + pin[0]
    return b


def canon_sha(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


gb = pinned((G_PATH, G_SHA))
spec_mod = importlib.util.spec_from_file_location('v003g_dry', G_PATH)
G = importlib.util.module_from_spec(spec_mod)
spec_mod.loader.exec_module(G)
cs = json.loads(pinned(SPEC))
cs2 = json.loads(pinned(SPEC_V002))
add = json.loads(pinned(ADD))
slots = json.loads(pinned(SLOTS))
ngc_real = slots['ngc3198_slots']                 # allowed key
nbm = slots['notes_block_for_manifest']           # allowed key
mode = add['coordinate_mode']


def build(coords_doc, ngc):
    coords = list(coords_doc['coordinates']) + list(ngc)
    am = G.apply_coordinate_mode(coordinates=coords, coordinate_mode=mode)
    assert am.get('ok'), am.get('reasons')
    fs = G.make_freeze_coordinate_spec(coordinates=am['coordinates'])
    assert fs.get('ok'), fs.get('reasons')
    r = []
    S = G._spec_from(fs['spec'], r)
    assert S is not None, r
    return fs, S


def geo(S):
    return {nm: {k: S['by_name'][nm][k] for k in ('lower', 'upper', 'trial_value', 'reference_value')}
            for nm in S['ngc_nuisance_names']}


out = {}
cases = {
    'PHASE1_FREEZE_SPEC_AS_CODED_CX2V006_PLACEHOLDER': (cs, cs['ngc3198_nuisance_slots']['placeholder_for_engine_coordinate_derivation']),
    'PHASE1_FREEZE_SPEC_AS_CODED_V002_PLACEHOLDER': (cs2, cs2['ngc3198_nuisance_slots']['placeholder_for_engine_coordinate_derivation']),
    'B2_FIX_CX2V006_PLUS_SLOTS_V003': (cs, ngc_real),
}
eng = {}
for name, (doc, ngc) in cases.items():
    fs, S = build(doc, ngc)
    eng[name] = canon_sha(fs['engine_coordinates'])
    u = [0.5] * len(S['varying_engine'])                      # synthetic member u
    th_eng = G._theta_engine_from_u(S, u)
    th_ngc = G._theta_ngc_from_engine(S, th_eng)
    rec = {'coordinate_mode': S['coordinate_mode'], 'ngc_slots': geo(S),
           'member_theta_ngc_geometry_leaves': {nm: th_ngc[nm] for nm in S['ngc_nuisance_names']},
           'engine_coordinates_canon_sha256': eng[name]}
    sens = {'evaluations': [], 'per_query': []}
    for nlabel, notes in (('notes=slots_V003.notes_block_for_manifest', copy.deepcopy(nbm)),
                          ('notes=list_C2V003_keys_A13_A16.1_only', {'A13': 'x', 'A16.1': 'x'})):
        reasons = []
        a16 = G._check_slot_geometry(S, sens, notes, reasons)
        rec['_check_slot_geometry[%s]' % nlabel] = {'passes': a16 is not None and not reasons, 'n_reasons': len(reasons),
                                                     'reasons_head': [r[:150] for r in reasons[:3]]}
    out[name] = rec
out['engine_coordinates_equal_placeholder_vs_fix'] = (eng['PHASE1_FREEZE_SPEC_AS_CODED_CX2V006_PLACEHOLDER'] ==
                                                      eng['B2_FIX_CX2V006_PLUS_SLOTS_V003'] ==
                                                      eng['PHASE1_FREEZE_SPEC_AS_CODED_V002_PLACEHOLDER'])
out['engine_coordinates_equal_cx2v006_file_field'] = None
out['notes_block_for_manifest_top_keys'] = sorted(nbm)
print(json.dumps(out, indent=1, sort_keys=True))
