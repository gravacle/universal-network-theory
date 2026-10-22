"""Phase 2/3 launcher (PREREG_KGRID_FIDELITY_V001 4c2eefeb). Runs one compute/tools *_v001.py tool UNCHANGED.

- Every compute/tools file used is verified from bytes against the sha recorded in compute/HASHES.txt before import.
- kg_lib_v001 output roots are redirected to phase23/ (L.OPS = phase23/ops, L.OUT = phase23/out); nothing is written
  under compute/. L.LANE is unchanged (the prep_v001 H-OVR guard still requires the review file under LANE/check).
- L.write_json is replaced by an exclusive-create writer with the identical serialization
  (json.dumps(obj, indent=1, allow_nan=False, default=str)); v001 wrote tmp + os.replace (a rename), not allowed here.
- --z95 (ringeval only): ZK extended to (0,10,-10,20,-20,30,-30,95,-95) for the A14.C5 reported addition; the 7 sealed
  heights are evaluated by the same ctx.lnN calls on the same cached line (checker replay_c1 Ctx caches the line per
  (R, phi)); 95 kpc values are reported only and never a criterion.
usage: run_p23_v001.py TOOL.py [--z95] args...
"""
import hashlib, importlib.util, json, sys
from pathlib import Path

LANE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_kgrid_fidelity_c2')
CT = LANE/'compute'/'tools'
P23 = LANE/'phase23'
ALLOWED = ('prep_v001.py', 'respond_v001.py', 'assemble_v001.py', 'ringeval_v001.py', 'known_field_v001.py', 'replay_v001.py')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def recorded():
    m = {}
    for line in (LANE/'compute'/'HASHES.txt').read_text().splitlines():
        if line.strip():
            d, n = line.split(None, 1)
            m[n.strip()] = d
    return m


def write_exclusive(path, obj):
    path = Path(path)
    with open(path, 'x') as f:
        f.write(json.dumps(obj, indent=1, allow_nan=False, default=str))


def main():
    tool = sys.argv[1]
    args = sys.argv[2:]
    z95 = False
    if args and args[0] == '--z95':
        z95 = True; args = args[1:]
    if tool not in ALLOWED:
        raise SystemExit('tool not allowed: '+tool)
    rec = recorded()
    for f in ('kg_lib_v001.py', tool):
        got = sha(CT/f)
        if rec.get('./tools/'+f) != got:
            raise SystemExit('TOOL SHA MISMATCH %s %s %s' % (f, got, rec.get('./tools/'+f)))
    sys.path.insert(0, str(CT))
    import kg_lib_v001 as L
    if Path(L.__file__).resolve() != (CT/'kg_lib_v001.py').resolve():
        raise SystemExit('kg_lib imported from unexpected path')
    L.OPS = P23/'ops'
    L.OUT = P23/'out'
    L.write_json = write_exclusive
    spec = importlib.util.spec_from_file_location(tool[:-3], str(CT/tool))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if z95:
        if tool != 'ringeval_v001.py':
            raise SystemExit('--z95 only for ringeval')
        if tuple(mod.ZK) != (0.0, 10.0, -10.0, 20.0, -20.0, 30.0, -30.0):
            raise SystemExit('unexpected ZK')
        mod.ZK = tuple(mod.ZK) + (95.0, -95.0)
    sys.argv = [str(CT/tool)] + args
    if tool == 'known_field_v001.py':
        if args[0] == 'V4':
            raise SystemExit('V4 not run in phase23')
        mod.run_grid(args[0])
    else:
        mod.main()


if __name__ == '__main__':
    main()
