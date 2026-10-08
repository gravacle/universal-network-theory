"""Fetch one pinned public input to stdout; no file writes or source execution."""
import base64
import hashlib
import json
from pathlib import Path
import sys
import urllib.parse
import urllib.request
import zlib

sys.dont_write_bytecode = True
COMMIT = 'c447f0fea703fcd0fff57de5000947b5ca81286b'
FILES = {
    'vector': 'Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat',
    'covariance': 'Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES_STAT+SYS.cov',
    'readme': 'Pantheon+_Data/4_DISTANCES_AND_COVAR/README',
    'likelihood': 'Pantheon+_Data/5_COSMOLOGY/cosmosis_likelihoods/Pantheon+_only_cosmosis_likelihood.py',
}

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in FILES:
        raise SystemExit('Choose vector, covariance, readme, or likelihood')
    key = sys.argv[1]
    path = FILES[key]
    url = ('https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/'
           + COMMIT + '/' + urllib.parse.quote(path, safe='/'))
    request = urllib.request.Request(url, headers={'User-Agent': 'UNT-public-source-custody/1'})
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200 or response.url != url:
            raise RuntimeError('Unexpected HTTP response or redirect')
        raw = response.read(64*1024*1024+1)
    if not raw or len(raw) > 64*1024*1024:
        raise RuntimeError('Unexpected input size')
    raw.decode('utf-8')  # All four declared products are text.
    packet = dict(kind='public_source_verbatim_zlib_base64', repository='PantheonPlusSH0ES/DataRelease',
        commit=COMMIT, path=path, url=url, key=key,
        bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
        transport_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        encoding='zlib_base64', data=base64.b64encode(zlib.compress(raw,9)).decode(),
        scope='Public input custody only; no likelihood scoring, parameter fit, local file write, or downloaded source execution.')
    print(json.dumps(packet, sort_keys=True, separators=(',', ':'), allow_nan=False))

if __name__ == '__main__':
    main()
