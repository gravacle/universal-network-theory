"""Uninstalled natural-wave executor hook prototype. Not a campaign entry.
The installer must bind _external_orch, _external_lock, _external_modules and
_external_candidates on each executor. Parent locking/planning remain upstream.
Cache verification/write integration and F6 remain incomplete.
"""
import copy
import types
from pathlib import Path
from snapshot_cx1v001 import Refusal
from valid_admission_cx1v002 import validate_valid, check_held_lock
from request_guard_cx1v002 import require


def make_executor_type(parent, scheduler):
    class ExternalExecutor(parent):
        def _validate(self, candidate):
            return validate_valid(self._external_orch,lock=self._external_lock(),
                chain_modules=self._external_modules,wave_dir=self._external_wave_dir,
                plan=self._external_plan,candidate=candidate)

        def execute(self,wave_dir,plan,resume,log):
            check_held_lock(self._external_lock(),self.ctx.work_dir)
            self._external_wave_dir=wave_dir
            self._external_plan=copy.deepcopy(plan)
            self._external_selected={}
            admitted={}
            # Candidate metadata is searched only after the actual natural plan.
            # Files for unrequested candidates are never opened here.
            for c in plan['calls']:
                matches=[x for x in self._external_candidates if x.get('key')==c['key']
                         and (x.get('spec') or {}).get('sha256')==c['spec_sha256']]
                require(len(matches)<=1,'AMBIGUOUS_EXTERNAL_CANDIDATE')
                if not matches:continue
                candidate=copy.deepcopy(matches[0])
                candidate['call_index']=c['call_index']
                # Never substitute a direct call after local execution exists.
                local=Path(wave_dir)/'campaign'/('call_%04d'%c['call_index'])
                if local.exists():continue
                verified=self._validate(candidate)
                self._external_selected[c['call_index']]=candidate
                admitted[c['call_index']]={'index':c['call_index'],'status':'OK',
                    'call_dir':candidate['call_dir'],'execution_origin':'DIRECT_EXTERNAL',
                    'receipt_sha256':verified['receipt'].get('receipt_sha256')}
            if not admitted:
                return super().execute(wave_dir,plan,resume,log)
            original=self.ctx.C
            proxy=types.ModuleType('_cx1_private_scheduler_proxy')
            proxy.__dict__.update(original.__dict__)
            def run_campaign(**kw):
                return scheduler.run_campaign(_admitted_external=admitted,**kw)
            proxy.run_campaign=run_campaign
            self.ctx.C=proxy
            try:
                records,meta=super().execute(wave_dir,plan,resume,log)
            finally:
                self.ctx.C=original
            if records is not None:
                require(len(records)==len(plan['calls']),'EXTERNAL_RECORD_COUNT')
                meta=dict(meta,external_import_count=len(admitted),
                    external_call_indices=sorted(admitted),external_custody='ORIGINAL_DIRECT_CALL_DIR')
            return records,meta

        def classify(self,call,record):
            if record.get('execution_origin')!='DIRECT_EXTERNAL':
                return super().classify(call,record)
            candidate=self._external_selected.get(call['call_index'])
            require(candidate is not None and candidate['call_dir']==record.get('call_dir'),'EXTERNAL_RECORD_NOT_SELECTED')
            # Fallback execution may take hours: revalidate evidence at ingest,
            # using a fresh snapshot, rather than retaining the selection snapshot.
            verified=self._validate(candidate)
            return (verified['classification'],verified['failure_class'],
                    verified['forward'],verified['provenance'])
    return ExternalExecutor
