"""Shared helpers for certificates_v003 (tail_scheme_impl_c2/certificates_v003; root A57.1, production gas M_s = 128 for the
DDO tail-corrected cases).  READ-ONLY on every input; writes only under certificates_v003/ (exclusive create).  numpy only.

Reuses, read-only and pinned by sha:
  certificates_v002 tools/certs2_common_c2v002.py (8a42fbf3; itself pins certificates_v001 certs_common_c2v001.py 1946a394:
  saved R3 states, I1-T on DDO states, tail-module loading, symbol route);
  certificates_v001 tools/gq_cert_c2v001.py (806eb23c; clone_gas only).
Tail modules: the r4 module owned_uv_tail_lapse_v001.py (c28d4209, pinned by certs_common) for every GQ / LO computation;
the r5 successor owned_uv_tail_lapse_v002.py (2026f2b6; A55.2 cap-only successor, being built in driver_r5/) is loaded only by
the module-acceptance tool."""
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CERT3 = HERE.parent
V002_TOOLS = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/tools')
V002_COMMON_SHA = '8a42fbf34339392d60164bfd108a38b02d093b5bc5066522655b9e3705ff863b'
sys.path.insert(0, str(V002_TOOLS))
import certs2_common_c2v002 as C2  # noqa: E402

if C2.CC.sha(V002_TOOLS / 'certs2_common_c2v002.py') != V002_COMMON_SHA:
    raise SystemExit('certs2_common_c2v002 pin mismatch')
CC = C2.CC
sys.path.insert(0, str(C2.V001_TOOLS))
import gq_cert_c2v001 as G1  # noqa: E402  (clone_gas only)

PIN_G1 = '806eb23c5daec645ac77e57925ad3f6e34fb001f2c9b18bd197c7a07df285f22'
if CC.sha(C2.V001_TOOLS / 'gq_cert_c2v001.py') != PIN_G1:
    raise SystemExit('gq_cert_c2v001 pin')

V002 = C2.CERT2
V002_RECORDS = {
    'EPS_CERT_V006': (V002 / 'gates/EPS_CERT_V006.json', '598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192'),
    'LO_CERT_V002': (V002 / 'gates/LO_CERT_V002.json', 'fd4fa52b76e10ee987461e77c23b1e5dd7f7df800d453a8409a86bd0868e67b4'),
    'GQ_CERT_V002': (V002 / 'gates/GQ_CERT_V002.json', 'fac4aca74244dc46c3699ce6502fc365a4bfe2535c4ded3a8de396186ab4d44c'),
    'GQ_CERT_V003_KB256_MS128': (V002 / 'gates/GQ_CERT_V003_KB256_MS128.json', 'b3a5390f83f9cdd23667290ed942138a56396afcf27bdec05ca3fab5ae99e5c5'),
    'LO_B1_MS128_V001': (V002 / 'out/LO_B1_MS128_V001.json', '573e51f55866037d08c84cf71b7bb76945791704bc88d72fde5803bc53924b9e'),
}
ADDENDUM_V005 = CC.UPC / 'CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
MS_PROD = 128            # A57.1
QUAD_DDO = {'order': 8, 'w_perp_max_inverse_kpc': 0.05, 'w_z_max_inverse_kpc': 0.02}
R_EVAL_DDO = 14.2
ROSTERS = {'C2R3': 2.0, 'C3R3': 3.0, 'C4R3': 4.0}


def v002_record(name):
    p, want = V002_RECORDS[name]
    got = CC.sha(p)
    if got != want:
        raise SystemExit('v002 record pin ' + name)
    return json.loads(p.read_text()), {'path': str(p), 'sha256': got}


def write_new(path, obj):
    path = Path(path)
    if CERT3 not in path.resolve().parents:
        raise SystemExit('refusing to write outside certificates_v003: %s' % path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(obj, indent=1, allow_nan=False, sort_keys=False) + '\n').encode()
    with open(path, 'xb') as f:
        f.write(raw)
    return hashlib.sha256(raw).hexdigest()


def decisions():
    return {'frozen_pinned': CC.pin('addendum_v004_frozen'),
            'open_cited_by_name': str(ADDENDUM_V005) + ' (A53-A57; A57.1 production gas M_s 128)',
            'open_sha256_at_read': CC.sha(ADDENDUM_V005)}


def ddo_roster(U, RS, PV, jn, cid, M_s):
    """Saved R3 le3 rotation roster (as certificates_v001/v002) at gas M_s; returns (case, roster, i1t, units, prof, s_edges)."""
    prof = json.loads(Path(CC.pin('profile')['path']).read_text())
    s_edges = prof['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2']
    case = CC.SavedR3(cid)
    units = dict(kpc_m=case.ni['kpc_m'], solar_mass_kg=case.ni['solar_mass_kg'])
    i1t = CC.i1t_on_state(RS, PV, case, prof, s_edges, units, jn)
    ros = RS.roster_rotation(case.source_rotation_arrays(), RS.stars_registered(prof, 'DDO154', units=units), s_edges_kpc2=s_edges,
                             kpc_m=units['kpc_m'], M_s=M_s)
    return case, ros, i1t, units, prof, s_edges


def clone_gas(RS, gas, M_s):
    return G1.clone_gas(RS, gas, M_s)
