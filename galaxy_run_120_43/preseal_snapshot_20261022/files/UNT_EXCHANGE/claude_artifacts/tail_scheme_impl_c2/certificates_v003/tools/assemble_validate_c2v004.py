"""SUCCESSOR of assemble_validate_c2v003.py (kept; its GQ_CERT_V004_MS128 / CERT_VALIDATION_V004 / EPS_MS_INDEPENDENCE_V001
outputs are kept unedited).  Error E-C3-1: compare r5 g_GQ requires the roster NAMED DDO_C4T to reach 2P = 256 (FIELDS_R5 GQ
"DDO_C4T>=max(64, 2P)"); V004 named the C4R3 roster's K_big 256 node set DDO_C4T-KHI only, so r5 read
GQ_REQUIRED_ROSTER_ABSENT_OR_SHORT:DDO_C4T.  Change (only): the rosters are named by roster, geometry-wise (the commission's
"C2T/C3T/C4T rosters"): each C2R3 / C3R3 / C4R3 entry on a cube-K / cylinder node set is DDO_C2T / DDO_C3T / DDO_C4T, and the
T-cases whose tail uses that node set are listed in node_set_of (C4T_KB256: C4T-KHI; C4T_KB128: C4T, C4T-A; C4T_KB64: C4T-KLO);
the other T-case geometries keep their T-case names (DDO_C4T-C5c, DDO_S4T, DDO_C6T); part_roster_name keeps the part's name.
The EPS independence record (2) is not recomputed: out/EPS_MS_INDEPENDENCE_V001.json is cited by sha.  Outputs:
gates/GQ_CERT_V005_MS128.json and out/CERT_VALIDATION_V005.json (GQ_CERT_V004_MS128 is also validated, for the record).
Original description (assemble_validate_c2v003):
  (1) gates/GQ_CERT_V004_MS128.json : the compare-format GQ record (FIELDS_R5 GQ) assembled from the ten out/GQ_FULL_*_V001.json
      parts.  rosters[] carries the FIELDS fields from each part's 4096-node contract sample (nodes 4096, M_s 128, M_s_doubled
      256) and, under all_nodes, the every-production-node result of that geometry; the record verdict is PASS only if BOTH the
      sample and the all-node maxima are <= 1e-12 P0 for every geometry.  NGC_T120L (M_s 96, unchanged by A57.1) is copied from
      certificates_v002 GQ_CERT_V002 (cited by sha), as certificates_v002 GQ_CERT_V003_* did.
  (2) out/EPS_MS_INDEPENDENCE_V001.json : whether EPS depends on M_s.  (a) static: the EPS producer chain's AST names/attributes
      contain none of the gas-quadrature tokens; EPS_CERT_V006 has no M_s key anywhere; (b) TESTED: the per-shell eps vector the
      module reads (_eps_per_shell) and the nonzero-shell mask are bitwise equal between M_s 64 and M_s 128 builds at K_big 128
      and 256 (out/MODULE_ACCEPT_V001_V001.json vs out/MODULE_ACCEPT_EPS64_V001.json).
  (3) out/CERT_VALIDATION_V004.json : compare r5 (78ac63b7, FIELDS_R5 736b8d77) evaluate_gate on EPS_CERT_V006, GQ_CERT_V004_MS128,
      LO_CERT_V003_MS128 with a case block whose C4T /numerics is Codex1's C4T MS128 template (P = 128), plus the superseded
      M_s 64 / sampled records for reference; and the r4 compare (fc2d6465) with an empty context.
Usage: python3 -I -B assemble_validate_c2v004.py"""
import ast
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import certs3_common_c2v003 as C3  # noqa: E402

CC = C3.CC
PARTS = ('C2T_KB128', 'C2T_KB256', 'C3T_KB128', 'C3T_KB256', 'C4T_KB64', 'C4T_KB128', 'C4T_KB256', 'C4T-C5c', 'S4T_SPHERE_KB128', 'C6T_KB128')
CMP = {'r5': (CC.ART / 'v007_compare_c2/r5/kmax_tail_compare_c2v007_r5.py', '78ac63b7a52a8746e96f390d0d5b46de4aa7ce5eaa27def6e54ef27330ce9755',
              CC.ART / 'v007_compare_c2/r5/FIELDS_R5.md', '736b8d7759484b7bbf90c0a430315ae23678d420020c9e2497c7ba6d3332dcfe'),
       'r4': (CC.ART / 'v007_compare_c2/r4/kmax_tail_compare_c2v007_r4.py', 'fc2d646508cdae832503ac072aef0a421b2cd4b7c8b770c3645d4fe63dbbcfc0',
              CC.ART / 'v007_compare_c2/r4/FIELDS_R4_V2.md', None)}
C4T_TEMPLATE = (CC.ART / 'v007_launch_packet_cx1/P128/specs/C4T_P128_MS128_CX1V003.TEMPLATE.json',
                '088902fb6498f06528f87eb460294095abcae2471b0932a935e9b43564b4e785')
EPS_CHAIN = [C3.V002_TOOLS / 'eps_cert_c2v005.py', C3.V002_TOOLS / 'eps_cert_assemble_c2v006.py',
             C3.C2.V001_TOOLS / 'eps_cert_c2v002.py', C3.C2.V001_TOOLS / 'eps_cert_c2v004.py']
GAS_TOKENS = ('M_s', 'GasColumns', 'radial_factors', 'vertical_factors', 'roster_rotation', 'gas_columns', 'gas_columns_from_rings',
              'uvt_modules', 'uvt_config', 'build', 'source_rotation_arrays', 'gas_packet')


def ast_tokens(path):
    t = ast.parse(Path(path).read_text())
    names = set()
    for n in ast.walk(t):
        if isinstance(n, ast.Name):
            names.add(n.id)
        elif isinstance(n, ast.Attribute):
            names.add(n.attr)
        elif isinstance(n, ast.keyword) and n.arg:
            names.add(n.arg)
    return names


def keys_with(obj, sub, path=''):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if sub in k:
                out.append(path + '/' + k)
            out += keys_with(v, sub, path + '/' + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += keys_with(v, sub, '%s[%d]' % (path, i))
    return out


NAMING = {'C2T_KB128': ('DDO_C2T', ['C2T']), 'C2T_KB256': ('DDO_C2T', []), 'C3T_KB128': ('DDO_C3T', ['C3T']), 'C3T_KB256': ('DDO_C3T', []),
          'C4T_KB64': ('DDO_C4T', ['C4T-KLO']), 'C4T_KB128': ('DDO_C4T', ['C4T', 'C4T-A']), 'C4T_KB256': ('DDO_C4T', ['C4T-KHI']),
          'C4T-C5c': ('DDO_C4T-C5c', ['C4T-C5c']), 'S4T_SPHERE_KB128': ('DDO_S4T', ['S4T (mask stages)']), 'C6T_KB128': ('DDO_C6T', ['C6T'])}


def main():
    CC.require_env(); t0 = time.time()
    # ---------------------------------------------------------------- (1) GQ
    parts = {}
    for lab in PARTS:
        p = C3.CERT3 / ('out/GQ_FULL_%s_V001.json' % lab)
        parts[lab] = (json.loads(p.read_text()), {'path': str(p), 'sha256': CC.sha(p)})
    v2, v2pin = C3.v002_record('GQ_CERT_V002')
    ngc = [dict(r, copied_from=v2pin) for r in v2['rosters'] if r['roster'] == 'NGC_T120L']
    rosters = []
    for lab in PARTS:
        d, pin = parts[lab]
        c = dict(d['contract_sample'])
        f = dict(d['full_domain']); f.pop('histogram', None)
        c.update(geometry=lab, role=d['role'], kept=d['kept'], outer=d['outer'], state=d['roster_state'], state_result_sha256=d['state_result_sha256'],
                 P0=d['P0'], gas_mass_kg=d['gas_mass_kg'], grid=dict(N_perp=d['grid']['N_perp'], N_z_plus=d['grid']['N_z_plus']),
                 k_abs_max_inverse_kpc=f['k_abs_max_inverse_kpc'], i1t=d['i1t'], all_nodes=f, part_record=pin,
                 k_range_convention='[kept K, outer K_big (cylinder) or K_out (cube)]; node |k| reaches k_abs_max_inverse_kpc')
        c['part_roster_name'] = c['roster']
        c['roster'], c['node_set_of'] = NAMING[lab]
        rosters.append(c)
    ddo = rosters
    smax = max(r['max_abs_diff_over_P0'] for r in ddo); fmax = max(r['all_nodes']['max_abs_diff_over_P0'] for r in ddo)
    ok = all(r['max_abs_diff_over_P0'] <= 1e-12 and r['all_nodes']['max_abs_diff_over_P0'] <= 1e-12 and r['nodes'] == 4096
             and r['M_s_doubled'] == 2 * r['M_s'] and r['M_s'] == C3.MS_PROD for r in ddo) and all(r['max_abs_diff_over_P0'] <= 1e-12 for r in ngc)
    gq = dict(schema=CC.GATE_SCHEMA, gate='GQ', verdict='PASS' if ok else 'UV_TAIL_GAS_QUADRATURE_UNCERTIFIED',
              producer=CC.producer(__file__), common=CC.producer(C3.HERE / 'certs3_common_c2v003.py'),
              part_producer=parts[PARTS[0]][0]['producer'],
              rosters=ddo + ngc, gas_M_s_DDO=C3.MS_PROD, gas_M_s_NGC=96,
              coverage_inverse_kpc={'DDO': [2.0, 256.0], 'NGC': [2.0, 46.0]},
              coverage_note=('DDO k ranges are [kept K, cylinder K_big] of the production node sets (64, 128, 256; cube K_out 5 for C4T-C5c); '
                             'the K_big 256 node sets reach |k| = sqrt2 x 256 = 362.04 /kpc, the full DDO reach [2, 362] of A57.1 '
                             '(C2T, C3T and C4T rosters each at K_big 256); every production tail node of each geometry is evaluated (all_nodes)'),
              threshold_over_P0=1e-12, max_abs_diff_over_P0=float(max(smax, max(r['max_abs_diff_over_P0'] for r in ngc))),
              max_abs_diff_over_P0_DDO_sample=float(smax), max_abs_diff_over_P0_DDO_all_nodes=float(fmax),
              all_nodes_total=int(sum(r['all_nodes']['nodes'] for r in ddo)),
              max_rel_change_DDO_all_nodes=float(max(r['all_nodes']['max_rel_change'] for r in ddo)),
              max_rel_change_DDO_all_nodes_S_over_P0_ge_1em6=float(max(r['all_nodes']['max_rel_change_S_over_P0_ge_1em6'] for r in ddo)),
              max_rel_change=float(max(r['max_rel_change'] for r in rosters)),
              max_rel_change_S_over_P0_ge_1em6=float(max(r['max_rel_change_S_over_P0_ge_1em6'] for r in rosters)),
              note=('the gate value is the P0-normalized change (RA7); max_rel_change is reported and not gated (it is large only where '
                    '|S| is tiny; see all_nodes.at.rel); A57.1: production gas M_s 128 for every DDO tail-corrected case'),
              supersedes_for_ms128={'GQ_CERT_V003_KB256_MS128': C3.v002_record('GQ_CERT_V003_KB256_MS128')[1],
                                    'GQ_CERT_V004_MS128': CC.producer(C3.CERT3 / 'gates/GQ_CERT_V004_MS128.json') | {'error': 'E-C3-1 roster naming'}},
              roster_naming='geometry-wise by roster (DDO_C2T / DDO_C3T / DDO_C4T on cube-K cylinder node sets); node_set_of lists the T-cases using that node set',
              not_covered=('C4T-D5 (source_rule nodes_v001): its tail is the explicit packet over G5 minus G4 (module nodes_v001_packet; the '
                           'nodes_v001 lib has no M_s / GasColumns / radial_factors token), so no gas M_s quadrature enters; GQ does not apply'),
              decisions=C3.decisions(), seconds=round(time.time() - t0, 1))
    hgq = C3.write_new(C3.CERT3 / 'gates/GQ_CERT_V005_MS128.json', gq)
    print('GQ_CERT_V005_MS128', gq['verdict'], smax, fmax, hgq, flush=True)
    # ---------------------------------------------------------------- (2) EPS M_s independence: cited (not recomputed)
    eip = C3.CERT3 / 'out/EPS_MS_INDEPENDENCE_V001.json'
    epsind = json.loads(eip.read_text())
    print('EPS_MS_INDEPENDENCE_V001 (cited)', epsind['verdict'], CC.sha(eip), flush=True)
    # ---------------------------------------------------------------- (3) compare validation
    if CC.sha(C4T_TEMPLATE[0]) != C4T_TEMPLATE[1]:
        raise SystemExit('C4T template pin')
    num = json.loads(C4T_TEMPLATE[0].read_text())['numerics']
    ctx = {'case_block': {'cases': {'C4T': {'normalized_spec_equal': {'/numerics': num}}}}}
    lo3 = C3.CERT3 / 'gates/LO_CERT_V003_MS128.json'
    gates = {'EPS': C3.V002_RECORDS['EPS_CERT_V006'][0], 'GQ': C3.CERT3 / 'gates/GQ_CERT_V005_MS128.json', 'LO': lo3,
             'GQ@v003_GQ_CERT_V004_MS128_E-C3-1': C3.CERT3 / 'gates/GQ_CERT_V004_MS128.json',
             'GQ@v002_KB256_MS128_sampled': C3.V002_RECORDS['GQ_CERT_V003_KB256_MS128'][0], 'LO@v002_MS64': C3.V002_RECORDS['LO_CERT_V002'][0]}
    val = dict(schema='UVT_CERT_VALIDATION_C2V005', eps_ms_independence={'path': str(eip), 'sha256': CC.sha(eip), 'verdict': epsind['verdict']}, producer=CC.producer(__file__), compare={},
               context=dict(case_block_C4T_numerics_from=dict(path=str(C4T_TEMPLATE[0]), sha256=C4T_TEMPLATE[1]),
                            P=num['uv_tail']['outer']['K_big_inverse_kpc'], gas_M_s=num['uv_tail']['gas']['M_s']))
    for tag, (p, want, fields, fwant) in CMP.items():
        if CC.sha(p) != want or (fwant is not None and CC.sha(fields) != fwant):
            raise SystemExit('compare pin ' + tag)
        m = CC.load_module(p, 'cmp_' + tag)
        res = {}
        for name, path in gates.items():
            for cname, c in (('P128', ctx), ('empty', {})):
                if tag == 'r4' and cname == 'P128':
                    continue
                r = m.evaluate_gate(name.split('@')[0], str(Path(path).resolve()), c)
                res[name + '|' + cname] = dict(path=str(Path(path).resolve()), sha256=CC.sha(path), status=r['status'], codes=r['codes'],
                                               derived=r.get('derived', {}))
                print(tag, name, cname, r['status'], r['codes'], flush=True)
        val['compare'][tag] = dict(path=str(p), sha256=want, fields_file=str(fields), fields_sha256=CC.sha(fields), gates=res)
    val['seconds'] = round(time.time() - t0, 1)
    hv = C3.write_new(C3.CERT3 / 'out/CERT_VALIDATION_V005.json', val)
    print('CERT_VALIDATION_V005', hv)


if __name__ == '__main__':
    main()
