"""Exact-path scalar metadata reader. No application module imports or value logging.
Unselected values are syntax-checked and skipped, never decoded or materialized.
This is a component, not an adopted cause authenticator.
"""
import hashlib
import json
import math
import os
import re
import stat
from pathlib import Path

class Refused(ValueError):
    pass

ALLOWED = {
 'receipt': frozenset({('status',),('driver_status',),('exit_code',),('stop_reason',),
    ('result','path'),('result','sha256'),('pins','spec','sha256'),('pins','driver','path'),('pins','driver','sha256')}),
 'finish': frozenset({('status',),('result_path',),('result_sha256',)}),
}
NUMBER = re.compile(rb'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?')
HEX = frozenset(b'0123456789abcdefABCDEF')

class Selector:
    def __init__(self, raw, kind):
        if kind not in ALLOWED: raise Refused('UNKNOWN_METADATA_KIND')
        if type(raw) is not bytes: raise Refused('BYTES_REQUIRED')
        self.raw=raw; self.i=0; self.kind=kind; self.values={}; self.selected=set()
    def ws(self):
        while self.i<len(self.raw) and self.raw[self.i] in b' \r\n\t':self.i+=1
    def string(self, decode=False):
        start=self.i; self.i+=1
        while self.i<len(self.raw):
            c=self.raw[self.i];self.i+=1
            if c==34:
                if not decode:return None
                try: v=json.loads(self.raw[start:self.i])
                except (ValueError,UnicodeError):raise Refused('INVALID_STRING') from None
                if any(0xd800<=ord(x)<=0xdfff for x in v):raise Refused('UNPAIRED_SURROGATE')
                return v
            if c<32:raise Refused('INVALID_STRING')
            if c==92:
                if self.i>=len(self.raw):raise Refused('INVALID_ESCAPE')
                e=self.raw[self.i];self.i+=1
                if e==117:
                    h=self.raw[self.i:self.i+4]
                    if len(h)!=4 or any(x not in HEX for x in h):raise Refused('INVALID_ESCAPE')
                    self.i+=4
                elif e not in b'"\\/bfnrt':raise Refused('INVALID_ESCAPE')
        raise Refused('UNTERMINATED_STRING')
    def value(self,path,depth):
        if depth>64:raise Refused('JSON_DEPTH_LIMIT')
        self.ws()
        if self.i>=len(self.raw):raise Refused('TRUNCATED_JSON')
        wanted=path in self.selected
        c=self.raw[self.i]
        if c in (123,91):
            if wanted:raise Refused('METADATA_CONTAINER_FORBIDDEN')
            obj=c==123;self.i+=1;self.ws();close=125 if obj else 93
            if self.i<len(self.raw) and self.raw[self.i]==close:self.i+=1;return
            seen=set()
            while True:
                self.ws()
                if obj:
                    if self.i>=len(self.raw) or self.raw[self.i]!=34:raise Refused('OBJECT_KEY_REQUIRED')
                    key=self.string(True)
                    if key in seen:raise Refused('DUPLICATE_KEY')
                    seen.add(key);self.ws()
                    if self.i>=len(self.raw) or self.raw[self.i]!=58:raise Refused('COLON_REQUIRED')
                    self.i+=1;child=path+(key,) if path is not None else None
                else:child=None # array contents can never satisfy a metadata path
                self.value(child,depth+1);self.ws()
                if self.i>=len(self.raw):raise Refused('TRUNCATED_JSON')
                t=self.raw[self.i];self.i+=1
                if t==close:return
                if t!=44:raise Refused('DELIMITER_REQUIRED')
        elif c==34:v=self.string(wanted)
        elif self.raw.startswith(b'true',self.i):self.i+=4;v=True
        elif self.raw.startswith(b'false',self.i):self.i+=5;v=False
        elif self.raw.startswith(b'null',self.i):self.i+=4;v=None
        else:
            m=NUMBER.match(self.raw,self.i)
            if not m:raise Refused('INVALID_SCALAR')
            self.i=m.end();v=None
            if wanted:
                token=m.group()
                try:v=float(token) if any(x in token for x in b'.eE') else int(token)
                except ValueError:raise Refused('INVALID_NUMBER') from None
                if isinstance(v,float) and not math.isfinite(v):raise Refused('NONFINITE_METADATA')
        if wanted:self.values[path]=v
    def select(self,paths):
        requested=set(paths)
        if not requested<=ALLOWED[self.kind]:raise Refused('FORBIDDEN_KEY_ACCESS')
        self.selected=requested
        if self.i!=0:raise Refused('SELECTOR_SINGLE_USE')
        self.ws()
        if self.i>=len(self.raw) or self.raw[self.i]!=123:raise Refused('OBJECT_REQUIRED')
        self.value((),0);self.ws()
        if self.i!=len(self.raw):raise Refused('TRAILING_JSON')
        return dict(self.values)

def identity(st):
    return (st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns,st.st_mode,st.st_nlink)

class OneRead:
    """Cache by inode; hash and parse the same buffer. All path aliases revalidate metadata."""
    def __init__(self):self.cache={}
    def read(self,path,want_sha=None):
        p=Path(path)
        if not p.is_absolute():raise Refused('ABSOLUTE_PATH_REQUIRED')
        before=os.lstat(p)
        if not stat.S_ISREG(before.st_mode):raise Refused('REGULAR_FILE_REQUIRED')
        if before.st_size>16*1024*1024:raise Refused('METADATA_SIZE_LIMIT')
        key=(before.st_dev,before.st_ino)
        if key in self.cache:
            prior,raw=self.cache[key]
            if prior!=identity(before):raise Refused('INPUT_CHANGED')
        else:
            fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
            try:
                st=os.fstat(fd)
                if identity(st)!=identity(before):raise Refused('INPUT_CHANGED')
                chunks=[]
                while True:
                    part=os.read(fd,65536)
                    if not part:break
                    chunks.append(part)
                raw=b''.join(chunks)
                if identity(os.fstat(fd))!=identity(st) or len(raw)!=st.st_size:raise Refused('INPUT_CHANGED')
            finally:os.close(fd)
            self.cache[key]=(identity(st),raw)
        if identity(os.lstat(p))!=identity(before):raise Refused('INPUT_CHANGED')
        digest=hashlib.sha256(raw).hexdigest()
        if want_sha is not None and (type(want_sha) is not str or digest!=want_sha):raise Refused('PIN_MISMATCH')
        return raw,digest
