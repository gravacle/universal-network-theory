from pathlib import Path
import hashlib,ast
base=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl');out=Path(__file__).parent/'disk_v001';out.mkdir()
g=(base/'step4_guard_cx1v007.py').read_text()
extra='''
# A124: one fixed, non-symlinked output volume/root. statvfs supplies the same
# filesystem available-block measure as df without creating a helper process.
OUTPUT_VOLUME=Path('/Volumes/External1')
OUTPUT_ROOT=OUTPUT_VOLUME/'Research/UNT_STEP4_RUNS/V007_STEP4_DIRECT_V001'
DISK_RESERVE_BYTES=20*1024**3

def disk_free_bytes(path):
    try:
        v=os.statvfs(path)
        n=v.f_bavail*v.f_frsize
    except OSError as e:raise Refusal('DISK_READING_UNAVAILABLE') from e
    require(type(n) is int and n>=0,'DISK_READING_UNAVAILABLE')
    return n

def disk_output_volume(plan):
    # Reject aliases before resolution; root creates this directory at T0.
    require(OUTPUT_ROOT.is_dir(),'OUTPUT_ROOT_MISSING')
    for p in (OUTPUT_ROOT,*OUTPUT_ROOT.parents):
        require(not p.is_symlink(),'OUTPUT_SYMLINK_REFUSED')
    require(os.path.ismount(OUTPUT_VOLUME),'DECLARED_OUTPUT_VOLUME_UNMOUNTED')
    device=OUTPUT_VOLUME.stat().st_dev
    require(OUTPUT_ROOT.stat().st_dev==device,'WRONG_OUTPUT_VOLUME')
    paths=[plan['launcher_log']]
    for c in plan['calls']:paths.extend([c['outdir'],c['receipt'],c['monitor_log'],c['receipt']+'.launch.json'])
    for raw_path in paths:
        p=Path(raw_path)
        require(p.is_absolute() and '..' not in p.parts and p!=OUTPUT_ROOT and p.is_relative_to(OUTPUT_ROOT),'OUTPUT_OUTSIDE_DECLARED_ROOT')
        current=p
        while current!=OUTPUT_ROOT:
            require(not current.is_symlink(),'OUTPUT_SYMLINK_REFUSED')
            if current.exists():require(current.stat().st_dev==device,'WRONG_OUTPUT_VOLUME')
            current=current.parent
    return OUTPUT_VOLUME

def disk_admission(plan,call=None):
    volume=disk_output_volume(plan)
    chosen=plan['calls'] if call is None else [call]
    caps=[c.get('output_cap_bytes') for c in chosen]
    require(bool(caps) and all(type(n) is int and n>0 for n in caps),'POSITIVE_OUTPUT_CAP_REQUIRED')
    # Sum permits heterogeneous approved caps and equals calls*cap otherwise.
    required=sum(caps)+DISK_RESERVE_BYTES
    free=disk_free_bytes(volume)
    require(free>=required,'DISK_BATCH_BOUND' if call is None else 'DISK_START_BOUND')
    return {'free_bytes':free,'required_bytes':required,'volume':str(volume)}

'''
pos=g.index('def validate(');g=g[:pos]+extra+g[pos:]
old=g[g.index('def validate('):g.index('\n',g.index('def validate('))]
assert old.endswith('):'),old
g=g.replace(old,old[:-2]+',disk_batch=True):',1)
g=g.replace('    return plan,cfg\n','    if disk_batch:disk_admission(plan)\n    return plan,cfg\n')
with (out/'step4_guard_cx1v008.py').open('x') as f:f.write(g)
h=hashlib.sha256(g.encode()).hexdigest()
for oldn,newn in [('step4_launcher_cx1v008.py','step4_launcher_cx1v009.py'),('step4_bind_cx1v006.py','step4_bind_cx1v007.py')]:
 s=(base/oldn).read_text().replace('step4_guard_cx1v007.py','step4_guard_cx1v008.py').replace('42bf0ce9dcd48f734299ace4f07cb92a15563e57a39f5ae40be451e481d1c3de',h)
 if 'launcher' in oldn:
  s=s.replace('check_outputs=False)','check_outputs=False,disk_batch=False)')
  s=s.replace('                    free=memory_free()','                    disk=G.disk_admission(plan,pending[0])\n                    free=memory_free()')
  s=s.replace("                        for q in (c['outdir']", "                        G.disk_admission(plan,c)\n                        for q in (c['outdir']")
 with (out/newn).open('x') as f:f.write(s)
for p in out.iterdir():ast.parse(p.read_bytes())
# Native scientific gate and its fence remain byte-identical.
for name in ['native_preflight','fence']:
 def segment(s):
  t=ast.parse(s);n=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name==name);return ast.get_source_segment(s,n)
 assert segment(g)==segment((base/'step4_guard_cx1v007.py').read_text())
print('draft successors parsed; native_preflight and fence identical; guard',h)
