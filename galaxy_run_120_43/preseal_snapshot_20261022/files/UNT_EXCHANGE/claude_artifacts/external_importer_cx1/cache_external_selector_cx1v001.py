"""Select external validation from directory location as well as declared origin."""
from pathlib import Path

def needs_external_validation(ctx,entry):
 p=entry.get('provenance') or {}
 if p.get('execution_origin')=='DIRECT_EXTERNAL' or 'external_admission' in p:return True
 if entry.get('source')!='WAVE':return False
 directory=p.get('call_dir')
 if not isinstance(directory,str) or not directory:return False # original verifier rejects missing custody
 work=Path(ctx.work_dir).resolve();call=Path(directory).resolve()
 return call!=work and work not in call.parents
