"""Physical original-spec resolver for private checker contexts (0841).
Registration/root authorization and natural planning must be checked by caller.
No aliases, copying, status inference, acceptance production or cache writes.
"""
import copy,re
from pathlib import Path
from snapshot_cx1v001 import Refusal
from direct_layout_cx1v001 import bind_layout

def need(ok,why):
    if not ok:raise Refusal(why)

class OriginalSpecResolver:
    def __init__(self, snapshot, *, work_dir, bindings):
        self.snapshot=snapshot;self.work=Path(work_dir)
        need(self.work.is_absolute() and str(self.work.resolve())==str(self.work),'RESOLVER_WORK_PATH')
        self.sources={}
        for supplied in bindings:
            b=copy.deepcopy(supplied)
            layout=bind_layout(snapshot,plan_pin=b['direct_plan'],case=b['case'],expected_spec=b['spec'],expected_driver=b['driver'])
            out=Path(layout['outdir']);root=out.parent
            need(out.name=='out' and layout['receipt_path']==str(root/'RECEIPT.json')
                 and layout['monitor_log']==str(root/'monitor.log'),'RESOLVER_LAYOUT_NOT_0841')
            need(root!=self.work and self.work not in root.parents,'RESOLVER_EXTERNAL_IS_LOCAL')
            need(str(root) not in self.sources,'RESOLVER_DUPLICATE_ROOT')
            snapshot.pin(b['spec'])
            self.sources[str(root)]=b['spec']
    def __call__(self,directory):
        p=Path(directory)
        need(p.is_absolute() and str(p.resolve())==str(p),'RESOLVER_CALL_PATH')
        if str(p) in self.sources:
            pin=self.sources[str(p)];self.snapshot.pin(pin)
            return Path(pin['path'])
        try:rel=p.relative_to(self.work).parts
        except ValueError:raise Refusal('RESOLVER_UNREGISTERED_EXTERNAL')
        need(len(rel)==4 and rel[0]=='waves' and re.fullmatch(r'wave_[0-9]{4,}',rel[1])
             and rel[2]=='campaign' and re.fullmatch(r'call_[0-9]{4,}',rel[3]),'RESOLVER_UNKNOWN_LOCAL_LAYOUT')
        return p/'spec.json'
