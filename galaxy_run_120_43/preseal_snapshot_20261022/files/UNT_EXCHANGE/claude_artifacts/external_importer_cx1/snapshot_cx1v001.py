"""Single-read strict evidence snapshots for the external importer prototype.
Not an admission decision. A fresh Snapshot is required for each locked validation
transaction; do not retain one across transactions or live-result completion.
"""
import hashlib
import json
import math
import os
from pathlib import Path

class Refusal(BaseException):
    """Must not be caught as an ordinary invalid numerical evaluation."""


def strict_json(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise Refusal('JSON_DUPLICATE_KEY:' + key)
            out[key] = value
        return out
    def constant(value):
        raise Refusal('JSON_NONFINITE:' + value)
    try:
        obj = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=constant)
    except (ValueError, UnicodeError) as exc:
        raise Refusal('JSON_MALFORMED:' + str(exc)) from exc
    def finite(value):
        if isinstance(value, float) and not math.isfinite(value):
            raise Refusal('JSON_NONFINITE_NUMBER')
        if isinstance(value, dict):
            for v in value.values(): finite(v)
        elif isinstance(value, list):
            for v in value: finite(v)
    finite(obj)
    return obj


class Snapshot:
    def __init__(self):
        self._bytes = {}
        self.read_counts = {}

    def read(self, path):
        p = Path(path)
        if not p.is_absolute() or str(p.resolve()) != str(p):
            raise Refusal('NONCANONICAL_EVIDENCE_PATH')
        key = str(p)
        if key not in self._bytes:
            try:
                fd = os.open(key, os.O_RDONLY | os.O_NOFOLLOW)
                try:
                    before = os.fstat(fd)
                    import stat
                    if not stat.S_ISREG(before.st_mode):
                        raise Refusal('EVIDENCE_NOT_REGULAR')
                    with os.fdopen(fd, 'rb', closefd=False) as f:
                        raw = f.read()
                    after = os.fstat(fd)
                    now = os.stat(key, follow_symlinks=False)
                    fields = lambda st: (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
                    if fields(before) != fields(after) or fields(after) != fields(now):
                        raise Refusal('EVIDENCE_CHANGED_DURING_READ')
                finally:
                    os.close(fd)
            except OSError as exc:
                raise Refusal('EVIDENCE_UNREADABLE:' + key) from exc
            self._bytes[key] = raw
            self.read_counts[key] = 1
        return self._bytes[key]

    def pin(self, pin):
        if type(pin) is not dict or set(pin) != {'path', 'sha256'}:
            raise Refusal('EXACT_PIN_REQUIRED')
        sha = pin['sha256']
        if type(pin['path']) is not str or type(sha) is not str or len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha):
            raise Refusal('PIN_FORMAT')
        raw = self.read(pin['path'])
        if hashlib.sha256(raw).hexdigest() != sha:
            raise Refusal('PIN_MISMATCH:' + pin['path'])
        return raw

    def document(self, pin):
        return strict_json(self.pin(pin))

    def hash(self, path):
        return hashlib.sha256(self.read(path)).hexdigest()
