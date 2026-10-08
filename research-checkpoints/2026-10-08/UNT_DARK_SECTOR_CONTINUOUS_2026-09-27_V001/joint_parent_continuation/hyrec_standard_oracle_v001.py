"""Authenticated standard-only C invocation; stdout unchanged, no file writes."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ATOMIC = HERE / 'hyrec_inputs_v001'
RECEIPT_SHA = 'b92abea8bc12c963f531976fadecb751402c26625d49b9b8da7bc81d8ebcd63d'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bounded(path):
    result = path.resolve(strict=True)
    result.relative_to(ROOT)
    return result


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ('default', 'half') or sys.argv[2] not in ('standard-internal', 'standard-external'):
        raise RuntimeError('Use default|half standard-internal|standard-external')
    receipt_path = bounded(ATOMIC / 'HYREC_LOCAL_BUILD_V001.json')
    if sha(receipt_path) != RECEIPT_SHA:
        raise RuntimeError('Build receipt changed')
    receipt = json.loads(receipt_path.read_text())
    frozen_path = bounded(ATOMIC / receipt['freeze']['path'])
    if sha(frozen_path) != receipt['freeze']['sha256']:
        raise RuntimeError('Build freeze changed')
    frozen = json.loads(frozen_path.read_text())
    for name, expected in frozen['files'].items():
        if sha(bounded(ROOT / name)) != expected:
            raise RuntimeError('Frozen source changed: ' + name)
    upstream = json.loads((ATOMIC / 'HYREC_SOURCE_RECEIPT_V001.json').read_text())
    for item in upstream['files']:
        path = bounded(ATOMIC / 'upstream' / item['name'])
        if path.stat().st_size != item['bytes'] or sha(path) != item['sha256']:
            raise RuntimeError('Upstream bytes changed: ' + item['name'])
    selected = receipt['binaries'][sys.argv[1]]
    binary = bounded(ATOMIC / selected['path'])
    if sha(binary) != selected['sha256']:
        raise RuntimeError('Binary changed')
    command = [str(binary), str(bounded(ATOMIC / 'upstream')) + '/', sys.argv[2]]
    result = subprocess.run(command, cwd=str(ROOT), stdin=subprocess.DEVNULL,
                            capture_output=True, text=True, check=False)
    if result.returncode or result.stderr:
        print(json.dumps(dict(status='FAILED_OR_DIAGNOSTIC_ATOMIC_INVOCATION',
              returncode=result.returncode, command=command, stdout=result.stdout,
              stderr=result.stderr, binary_sha256=selected['sha256'])))
        return 2
    parsed = json.loads(result.stdout)
    if parsed.get('status') != 'COMPLETE_ATOMIC_HISTORY_ONLY' or parsed.get('mode') != sys.argv[2]:
        raise RuntimeError('Unexpected atomic result identity')
    sys.stdout.write(result.stdout)
    return 0


if __name__ == '__main__':
    sys.exit(main())
