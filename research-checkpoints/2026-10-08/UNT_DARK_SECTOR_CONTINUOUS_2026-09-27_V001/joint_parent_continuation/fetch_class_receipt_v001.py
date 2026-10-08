"""Pinned, bounded public CLASS text retrieval; stdout only, never execute source.

Root invocation, after source review:
  python3 stdout_paged_capture_v001.py fetch_class_receipt_v001.py --all
or replace --all with distinct exact paths from the pinned inventory.

One serial GET per selected path; no redirect, fallback, hidden retry or file
write. Every attempted response has a byte-preserving receipt, including failed
verification/partial reads. A subset is never labeled a complete source receipt.
The existing pager captures this JSON and emits acknowledged stdout pages.
"""
import sys

sys.dont_write_bytecode = True

import base64
from datetime import datetime, timezone
import hashlib
import http.client
import json
from pathlib import Path
import re
import time
import urllib.error
import urllib.request


ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT / 'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
INVENTORY = J / 'CLASS_SOURCE_INVENTORY_PLAN_V001.json'
INVENTORY_SHA256 = '8bd251bba28d681afac2913863fccd69f5901d76ee5cde7b041f0b02adcff042'
PAGER = J / 'stdout_paged_capture_v001.py'
PAGER_SHA256 = '4cc9408d97b5cfa6def942d9220065ebf304f07de37b81396609b69b753be6d1'
COMMIT = '64bbab707faf4de4779a9e04edd180fef18d98fa'
PREFIX = 'https://raw.githubusercontent.com/lesgourg/class_public/' + COMMIT + '/'
EXPECTED_COUNT = 89
EXPECTED_TOTAL_BYTES = 3294365
MAX_FILE_BYTES = 1024 * 1024
ERROR_BODY_LIMIT = 8192
SOCKET_TIMEOUT_SECONDS = 30
PUBLICATION_ROOT = J / 'class_inputs_v001/upstream'
PATH_PATTERN = re.compile(r'[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\Z')
SHA1_PATTERN = re.compile(r'[0-9a-f]{40}\Z')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def validate_path(name):
    if not isinstance(name, str) or not PATH_PATTERN.fullmatch(name):
        raise ValueError('Inventory path has forbidden characters')
    parts = name.split('/')
    if any(part in ('.', '..', '') for part in parts):
        raise ValueError('Inventory path has traversal or an empty component')
    return parts


def no_existing_symlink(path, anchor):
    """Read-only publication-path guard, not creation or a future-write lock."""
    relative = path.relative_to(anchor)
    current = anchor
    if current.is_symlink():
        raise ValueError('Project anchor is a symlink')
    for i, part in enumerate(relative.parts):
        current = current / part
        if current.is_symlink():
            raise ValueError('Existing path component is a symlink: ' + str(current))
        if i + 1 < len(relative.parts) and current.exists() and not current.is_dir():
            raise ValueError('Existing parent component is not a directory')
    if path.exists() and not path.is_file():
        raise ValueError('Existing publication target is not a regular file')


def load_inventory():
    source = Path(__file__).absolute()
    if source.parent != J or source.name != 'fetch_class_receipt_v001.py':
        raise ValueError('Fetcher must reside in the exact owned packet')
    for local in (source, INVENTORY, PAGER):
        no_existing_symlink(local, ROOT)
    raw = INVENTORY.read_bytes()
    if digest(raw) != INVENTORY_SHA256:
        raise ValueError('Inventory SHA256 differs')
    if digest(PAGER.read_bytes()) != PAGER_SHA256:
        raise ValueError('Existing stdout pager SHA256 differs')
    data = json.loads(raw.decode('utf-8', errors='strict'))
    if (data['commit'] != COMMIT or data['raw_url_prefix'] != PREFIX
            or data['api_tree_truncated'] is not False
            or data['count'] != EXPECTED_COUNT
            or data['planned_source_bytes'] != EXPECTED_TOTAL_BYTES):
        raise ValueError('Pinned inventory identity/census differs')
    rows = data['files']
    if not isinstance(rows, list) or len(rows) != EXPECTED_COUNT:
        raise ValueError('Inventory file array differs')
    names = set()
    folded_names = set()
    total = 0
    for row in rows:
        if not isinstance(row, dict) or set(row) != {'path', 'bytes', 'git_blob_sha1'}:
            raise ValueError('Unexpected inventory entry schema')
        name = row['path']
        validate_path(name)
        if name in names or name.casefold() in folded_names:
            raise ValueError('Duplicate or case-colliding inventory path')
        names.add(name)
        folded_names.add(name.casefold())
        count = row['bytes']
        if type(count) is not int or not 0 < count <= MAX_FILE_BYTES:
            raise ValueError('Expected file size outside fixed bound')
        if not isinstance(row['git_blob_sha1'], str) or not SHA1_PATTERN.fullmatch(row['git_blob_sha1']):
            raise ValueError('Invalid Git blob digest')
        total += count
        target = PUBLICATION_ROOT.joinpath(*name.split('/'))
        # Pure lexical containment plus every existing ancestor checked before GETs.
        target.relative_to(PUBLICATION_ROOT)
        no_existing_symlink(target, ROOT)
    if total != EXPECTED_TOTAL_BYTES:
        raise ValueError('Inventory byte-total mismatch')
    for name in names:
        parts = name.split('/')
        if any('/'.join(parts[:n]).casefold() in folded_names for n in range(1, len(parts))):
            raise ValueError('Inventory file/directory prefix collision')
    return rows, digest(source.read_bytes())


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, new_url):
        return None


def selected_headers(response):
    return {key: response.headers.get(key) for key in
            ('Content-Length', 'Content-Type', 'Content-Encoding', 'ETag', 'Last-Modified')
            if response.headers.get(key) is not None}


def read_bounded(response, limit, buffer):
    """Buffer survives exceptions; at most limit response bytes are retained."""
    while len(buffer) < limit:
        try:
            part = response.read(min(65536, limit - len(buffer)))
        except http.client.IncompleteRead as exc:
            # HTTPResponse may attach bytes to the exception before returning
            # them. Retain the received prefix within the same hard read limit,
            # then propagate the failure; a partial body is never a success.
            buffer.extend(exc.partial[:limit - len(buffer)])
            raise
        if not part:
            return True
        buffer.extend(part)
    return False


def attempt(opener, row, index):
    name = row['path']
    url = PREFIX + name  # All path characters already strictly allowlisted.
    started = time.perf_counter()
    raw = bytearray()
    metadata = dict(attempt_index=index, path=name, url=url,
                    expected_bytes=row['bytes'], expected_git_blob_sha1=row['git_blob_sha1'],
                    requested_read_limit=row['bytes'] + 1, started_utc=datetime.now(timezone.utc).isoformat())
    error = None
    http_ok = False
    try:
        request = urllib.request.Request(url, method='GET', headers={
            'User-Agent': 'UNT-pinned-public-source-custody/1',
            'Accept-Encoding': 'identity'})
        with opener.open(request, timeout=SOCKET_TIMEOUT_SECONDS) as response:
            metadata.update(http_status=response.status, response_url=response.geturl(),
                            response_headers=selected_headers(response))
            if response.status != 200 or response.geturl() != url:
                raise ValueError('Unexpected HTTP status or URL; no destination accepted')
            encoding = response.headers.get('Content-Encoding', 'identity').strip().lower()
            if encoding not in ('', 'identity'):
                raise ValueError('Encoded HTTP response is not the requested raw representation')
            metadata['read_reached_eof'] = read_bounded(response, row['bytes'] + 1, raw)
            http_ok = True
    except urllib.error.HTTPError as exc:
        metadata.update(http_status=exc.code, response_url=exc.geturl(),
                        response_headers=selected_headers(exc))
        # Redirects arrive here without following Location; errors have bounded bodies.
        try:
            metadata['error_body_reached_eof'] = read_bounded(exc, ERROR_BODY_LIMIT, raw)
        except (Exception, KeyboardInterrupt) as body_error:
            metadata['error_body_read_error'] = type(body_error).__name__ + ': ' + str(body_error)
            if isinstance(body_error, KeyboardInterrupt):
                metadata['interrupted'] = True
        finally:
            exc.close()
        error = type(exc).__name__ + ': ' + str(exc)
    except (Exception, KeyboardInterrupt) as exc:
        error = type(exc).__name__ + ': ' + str(exc)
        if isinstance(exc, KeyboardInterrupt):
            metadata['interrupted'] = True
    content = bytes(raw)
    actual_blob = hashlib.sha1(b'blob ' + str(len(content)).encode('ascii') + b'\0' + content).hexdigest()
    utf8_ok = True
    try:
        decoded = content.decode('utf-8', errors='strict')
        metadata['text_properties'] = dict(ends_with_lf=decoded.endswith('\n'),
                                          contains_cr='\r' in decoded, contains_nul='\0' in decoded)
    except UnicodeDecodeError as exc:
        utf8_ok = False
        metadata['utf8_error'] = str(exc)
    checks = dict(http_200_exact_url_raw=http_ok, exact_byte_count=len(content) == row['bytes'],
                  exact_git_blob=actual_blob == row['git_blob_sha1'], strict_utf8=utf8_ok)
    passed = error is None and all(checks.values())
    metadata.update(status='VERIFIED' if passed else 'FAILED_ATTEMPT', checks=checks,
                    bytes=len(content), sha256=digest(content), git_blob_sha1=actual_blob,
                    encoding='base64_raw', data=base64.b64encode(content).decode('ascii'),
                    elapsed_seconds=time.perf_counter() - started)
    if error is not None:
        metadata['error'] = error
    return metadata


def main(argv):
    packet = dict(kind='unt_class_public_source_receipt_v001', commit=COMMIT,
                  inventory_path=str(INVENTORY.relative_to(ROOT)), inventory_sha256=INVENTORY_SHA256,
                  pager_sha256=PAGER_SHA256, expected_inventory_files=EXPECTED_COUNT,
                  expected_inventory_bytes=EXPECTED_TOTAL_BYTES, records=[], failed_attempts=[],
                  scope='Pinned public UTF-8 source bytes only; no local writes, build, install, source execution, or science.',
                  retrieval_policy=dict(serial=True, attempts_per_selected_path=1, redirects=False,
                                        retries=False, proxy_environment_used=False,
                                        socket_timeout_seconds=SOCKET_TIMEOUT_SECONDS),
                  publication_policy='No filesystem publication by this program. Existing path symlinks are rejected; publisher must recheck all ancestors before writing. Git file modes are not in this inventory and are never materialized.')
    selected = []
    try:
        rows, source_sha = load_inventory()
        packet['fetcher_source_sha256'] = source_sha
        by_name = {row['path']: row for row in rows}
        if argv == ['--all']:
            selected = [row['path'] for row in rows]
        elif argv and len(argv) == len(set(argv)) and all(name in by_name for name in argv):
            selected = list(argv)
        else:
            raise ValueError('Choose --all alone, or distinct exact allowlisted paths')
        packet.update(selected_paths=selected, selected_bytes=sum(by_name[n]['bytes'] for n in selected),
                      not_selected_paths=[row['path'] for row in rows if row['path'] not in selected])
        # No environment proxy, credentials, redirect following or filesystem handler.
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
        for index, name in enumerate(selected):
            record = attempt(opener, by_name[name], index)
            packet['records' if record['status'] == 'VERIFIED' else 'failed_attempts'].append(record)
            if record.get('interrupted'):
                packet['status'] = 'FAILED_OR_INTERRUPTED'
                break
        else:
            packet['status'] = ('FAILED_RETRIEVAL' if packet['failed_attempts'] else
                                'COMPLETE' if len(selected) == EXPECTED_COUNT else 'COMPLETE_SELECTED_SUBSET')
    except (Exception, KeyboardInterrupt) as exc:
        packet['status'] = 'FAILED_OR_INTERRUPTED'
        packet['fatal_error'] = type(exc).__name__ + ': ' + str(exc)
    attempted = {r['path'] for key in ('records', 'failed_attempts') for r in packet[key]}
    packet['unstarted_paths'] = [name for name in selected if name not in attempted]
    packet['counts'] = dict(verified=len(packet['records']), failed=len(packet['failed_attempts']),
                          unstarted=len(packet['unstarted_paths']), selected=len(selected),
                          verified_bytes=sum(row['bytes'] for row in packet['records']))
    print(json.dumps(packet, sort_keys=True, separators=(',', ':'), allow_nan=False), flush=True)
    return 0 if packet['status'] in ('COMPLETE', 'COMPLETE_SELECTED_SUBSET') else 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
