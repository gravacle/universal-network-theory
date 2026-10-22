"""SOURCE ONLY. Bounded immutable payload I/O; external root monitor required."""
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import time


def require(ok, why):
    if not ok:
        raise ValueError(why)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def plain(path, limit=32*2**20):
    p = Path(path)
    require(p.is_absolute() and p.resolve() == p and not p.is_symlink(), 'plain absolute input')
    require(p.is_file() and p.stat().st_size <= limit, 'bounded regular input')
    with p.open('rb') as stream:
        raw = stream.read(limit + 1)
    require(len(raw) <= limit, 'bounded actual input')
    return raw


def decode(raw):
    def pairs(items):
        value = {}
        for k, v in items:
            require(k not in value, 'duplicate JSON field')
            value[k] = v
        return value
    def bad(value):
        raise ValueError('nonfinite JSON ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)


class Sink:
    def __init__(self, output, seconds, rss):
        self.started = time.monotonic()
        self.seconds = seconds
        self.rss = rss
        self.bytes = 0
        self.files = {}
        self.inputs = {}
        self.root = Path(output)
        require(self.root.is_absolute() and self.root.resolve() == self.root, 'literal fresh output')
        self.root.mkdir(exist_ok=False)

    def guard(self):
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            rss *= 1024
        require(time.monotonic() - self.started <= self.seconds, 'whole caller time cap')
        require(rss <= self.rss, 'whole caller RSS cap')
        require(self.bytes <= 8*2**20, 'eight MiB scientific reserve')

    def pinned(self, pin, limit=32*2**20):
        require(set(pin) in ({'path', 'sha256'}, {'path', 'sha256', 'bytes'}), 'literal pin fields')
        raw = plain(pin['path'], limit)
        require(digest(raw) == pin['sha256'], 'input hash ' + pin['path'])
        if 'bytes' in pin:
            require(type(pin['bytes']) is int and len(raw) == pin['bytes'], 'input exact bytes')
        self.inputs[pin['path']] = {'path': pin['path'], 'sha256': pin['sha256'], 'bytes': len(raw)}
        self.guard()
        return raw

    def save(self, name, value):
        require(Path(name).name == name and name not in self.files, 'unique payload filename')
        raw = (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
        require(self.bytes + len(raw) <= 8*2**20, 'prospective whole scientific bytes')
        self.guard()
        with (self.root/name).open('xb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        self.bytes += len(raw)
        self.files[name] = {'bytes': len(raw), 'sha256': digest(raw)}
        self.guard()

    def module(self, pin):
        raw = self.pinned(pin, 65536)
        module = {'__name__': 'root_p64_fixed_injected', '__file__': pin['path']}
        exec(compile(raw, pin['path'], 'exec'), module)
        # Existing source API takes attribute access for the injected module.
        from types import SimpleNamespace
        return SimpleNamespace(**module), raw

    def close_inputs(self):
        for pin in list(self.inputs.values()):
            self.pinned(pin)

    def failure(self, error):
        # Best effort after a cap failure; never hides the original exception.
        try:
            self.save('FAILURE.json', {'exception': type(error).__name__,
                                      'message': str(error), 'qualified': False})
        except BaseException:
            pass
