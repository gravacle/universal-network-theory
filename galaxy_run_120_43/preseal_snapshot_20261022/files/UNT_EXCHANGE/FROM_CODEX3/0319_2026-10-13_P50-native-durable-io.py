"""SOURCE ONLY. Exact pinned input and immutable compact240MiB scientific I/O.
Root external supervisor owns whole3GiB/900s/256MiB process/runtime limits.
"""
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import time
from types import SimpleNamespace

RESERVE = 240*2**20


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def plain(path, cap):
    p = Path(path)
    need(p.is_absolute() and p.resolve() == p and not p.is_symlink()
         and p.is_file() and p.stat().st_size <= cap, 'plain bounded file '+str(p))
    with p.open('rb') as stream:
        data = stream.read(cap+1)
    need(len(data) <= cap, 'actual read cap')
    return data


def decode(raw):
    def unique(items):
        result = {}
        for k, v in items:
            need(k not in result, 'duplicate JSON key')
            result[k] = v
        return result
    def bad(v):
        raise ValueError('nonfinite JSON '+v)
    return json.loads(raw, object_pairs_hook=unique, parse_constant=bad)


class Sink:
    def __init__(self, output):
        self.start = time.monotonic()
        self.root = Path(output)
        need(self.root.is_absolute() and self.root.resolve() == self.root, 'fresh literal absolute output')
        self.root.mkdir(exist_ok=False)
        self.inputs = {}
        self.files = {}
        self.bytes = 0

    def guard(self):
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            rss *= 1024
        need(time.monotonic()-self.start <= 900 and rss <= 3*2**30, 'whole native900s3GiB cap')
        need(self.bytes <= RESERVE, '240MiB scientific reserve')

    def pinned(self, pin, cap=256*2**20):
        need(set(pin) in ({'path', 'sha256'}, {'path', 'sha256', 'bytes'}), 'closed exact pin')
        raw = plain(pin['path'], cap)
        need(sha(raw) == pin['sha256'], 'input hash '+pin['path'])
        if 'bytes' in pin:
            need(type(pin['bytes']) is int and len(raw) == pin['bytes'], 'input bytecount')
        actual = {'path': pin['path'], 'sha256': pin['sha256'], 'bytes': len(raw)}
        if pin['path'] in self.inputs:
            need(self.inputs[pin['path']] == actual, 'unchanged duplicate input binding')
        self.inputs[pin['path']] = actual
        self.guard()
        return raw

    def module(self, pin):
        raw = self.pinned(pin, 65536)
        ns = {'__name__': 'root_p50_fixed_source', '__file__': pin['path']}
        exec(compile(raw, pin['path'], 'exec'), ns)
        return SimpleNamespace(**ns), raw

    def save(self, name, value):
        need(Path(name).name == name and name not in self.files, 'unique scientific filename')
        raw = (json.dumps(value, separators=(',', ':'), sort_keys=True, allow_nan=False)+'\n').encode()
        self.guard()
        need(self.bytes+len(raw) <= RESERVE, 'full scientific output cap before write')
        with (self.root/name).open('xb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        self.files[name] = {'bytes': len(raw), 'sha256': sha(raw)}
        self.bytes += len(raw)
        self.guard()

    def close_inputs(self):
        for pin in list(self.inputs.values()):
            self.pinned(pin, max(pin['bytes'], 1))

    def failure(self, error):
        try:
            self.save('FAILURE.json', {'exception': type(error).__name__, 'message': str(error),
                                     'partial_scientific_acceptance': False})
        except BaseException:
            pass
