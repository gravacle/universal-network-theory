"""Fill a V007 TEMPLATE call spec with the EPS and LO certificates (Claude2 tail_scheme_impl_c2/driver).  Nothing is launched.
The FILLED spec is the TEMPLATE with EXACTLY numerics.uv_tail.eps_certificate and numerics.uv_tail.lo_certificate replaced by
{path, sha256} (sha256 from the certificate bytes); every other byte-level JSON value is kept; the result is checked by
re-parsing (canonical comparison with the two entries removed) and written with exclusive create next to OUTDIR as
<template name with .TEMPLATE.json -> .FILLED.json>.  The FILLED spec sha is what root registers before the launch.
Usage: python3 -I -B fill_certificates_v007_c2v001.py TEMPLATE_JSON TEMPLATE_SHA256 EPS_CERT LO_CERT OUTDIR"""
import copy
import hashlib
import json
import sys
from pathlib import Path


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    tpl, tsha, eps, lo, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5])
    if sha(tpl) != tsha or not tpl.name.endswith('.TEMPLATE.json'):
        raise SystemExit('template pin or name')
    spec = json.loads(tpl.read_text())
    u = spec['numerics']['uv_tail']
    if u['eps_certificate'] != 'PENDING_UV_TAIL_CERTIFICATE' or u['lo_certificate'] != 'PENDING_UV_TAIL_CERTIFICATE':
        raise SystemExit('template certificates are not the pending sentinel')
    for c in (eps, lo):
        if not c.is_file() or not c.is_absolute():
            raise SystemExit('certificate must be an existing absolute path: %s' % c)
    filled = copy.deepcopy(spec)
    filled['numerics']['uv_tail']['eps_certificate'] = {'path': str(eps), 'sha256': sha(eps)}
    filled['numerics']['uv_tail']['lo_certificate'] = {'path': str(lo), 'sha256': sha(lo)}
    a, b = copy.deepcopy(spec), copy.deepcopy(filled)
    for x in (a, b):
        for k in ('eps_certificate', 'lo_certificate'):
            del x['numerics']['uv_tail'][k]
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    out.mkdir(parents=True, exist_ok=True)
    p = out / tpl.name.replace('.TEMPLATE.json', '.FILLED.json')
    raw = (json.dumps(filled, indent=1, sort_keys=True) + '\n').encode()
    with open(p, 'xb') as f:
        f.write(raw)
    print(json.dumps({'filled': str(p), 'sha256': hashlib.sha256(raw).hexdigest(), 'template_sha256': tsha,
                      'eps_certificate': filled['numerics']['uv_tail']['eps_certificate'],
                      'lo_certificate': filled['numerics']['uv_tail']['lo_certificate']}, indent=1))


if __name__ == '__main__':
    main()
