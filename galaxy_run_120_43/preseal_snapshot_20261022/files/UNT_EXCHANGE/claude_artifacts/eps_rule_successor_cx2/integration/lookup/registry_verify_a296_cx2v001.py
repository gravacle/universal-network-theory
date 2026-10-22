"""Explicit root-bound, read-only verifier for the frozen 31-point registry.

The existing registry bridge CLI deliberately remains legacy-only. This separate
entry supplies the authenticated A296 policy and current guard to the unchanged
original verify_registry checking function. It constructs no registry, numeric
record or proof, and exposes no launch action. Runtime custody remains required.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import sys
import types

ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
HERE=Path(__file__).absolute().parent
REGISTRY_BRIDGE={'path':str(HERE/'registry_assembler_a296_cx2v002.py'),'sha256':'0f9283b86f47a1382c9c00173d70d8a4fd34fa20664400ca55ed3bbf3c9cf548'}
ORIGINAL_VERIFIER={'path':str(ART/'s4rc1_c3/build_c3v005_c2/registry_assembler_c3v005.py'),'sha256':'7df1c4813865b9e1245f5a91d827591a6d87963b6413ab53c50d2a542d211310'}
LINEAGE={'path':str(HERE/'eps_lineage_cx2v001.py'),'sha256':'da5329e1f9530dc296b9592361cc86b7b480096f9514a9f4aba8cbfdd29c7abb'}


def need(ok,reason):
    if not ok:raise ValueError('A296_REGISTRY_VERIFY_'+reason)


def snapshot():
    raw=Path(LINEAGE['path']).read_bytes()
    need(hashlib.sha256(raw).hexdigest()==LINEAGE['sha256'],'LINEAGE_SOURCE_PIN')
    ns={'__file__':LINEAGE['path'],'__name__':'_a296_registry_snapshot'}
    exec(compile(raw,LINEAGE['path'],'exec'),ns)
    return ns['snapshot']()


def _transplanted_verifier(A,bound,binding_ref,s):
    """Unchanged original checking AST, with explicitly bound dependency globals."""
    tree=ast.parse(s.read(ORIGINAL_VERIFIER),filename=ORIGINAL_VERIFIER['path'])
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='verify_registry']
    need(len(nodes)==1,'ORIGINAL_FUNCTION_SET')
    def policy(c1_ref,registry_ref,*,roots=(A.C.ART,),canonical_producers=None):
        return A.c1_policy_gate(c1_ref,registry_ref,roots=roots,canonical_producers=canonical_producers,
                                binding_ref=binding_ref,snapshot=s)
    ns=dict(A.O.__dict__)
    ns.update(__file__=str(Path(__file__).absolute()),__name__='_a296_registry_bound_check',
        c1_policy_gate=policy,generator_pin=lambda:s.pin(__file__),
        wrapper_l30_guard_pin=lambda:dict(A.H.GUARD))
    exec(compile(ast.Module(body=nodes,type_ignores=[]),ORIGINAL_VERIFIER['path'],'exec'),ns)
    return ns['verify_registry'],hashlib.sha256(ast.dump(nodes[0],include_attributes=False).encode()).hexdigest()


def verify_bound(binding_ref,*,saved_snapshot=None):
    """Verify all frozen31 points under root-bound C1; no subset/vacuous pass."""
    s=saved_snapshot if saved_snapshot is not None else snapshot()
    with s.reads():
        A=s.module(REGISTRY_BRIDGE,'_a296_registry_verified_bridge')
        try:
            bound=A.H.validate_binding(s,binding_ref)
            need(A.C.background_qos(),'BACKGROUND_QOS_REQUIRED for custody derivation: run under taskpolicy -b')
            rows=A.C.point_rows()
            genesis=s.doc(A.H.GENESIS)
            keys=[r['key'] for r in rows]
            need(len(rows)==31 and len(set(keys))==31 and set(keys)==set(genesis.get('points',{})),'EXACT_FULL_FROZEN31_REQUIRED')
            guard=A.real_guard(binding_ref,snapshot=s)
            need(s.pin(guard.__file__)==A.H.GUARD,'ACTIVE_GUARD_PIN')
            verify,ast_sha=_transplanted_verifier(A,bound,binding_ref,s)
            report=verify(A.H.GENESIS,rows,c1_ref=bound['c1'],custody_loader=A.real_custody_fn,
                          guard=guard,canonical_producers=bound['tail_readiness']['approved_certificate_producers'])
            need(type(report.get('n')) is int and report['n']==31 and len(report.get('points',[]))==31,'FULL_REPORT_REQUIRED')
            need(report.get('generator')==s.pin(__file__) and report.get('guard')==A.H.GUARD,'REPORT_SOURCE_BINDING')
            wrapper=report.pop('wrapper')
            source=s.read(wrapper).decode('utf-8')
            lo,hi=A.O.WRAPPER_BLOCK_LINES
            block='\n'.join(source.split('\n')[lo-1:hi])+'\n'
            report.update(a296_binding=dict(binding_ref),
                executed_slot_block_source={'wrapper':wrapper,'lines':[lo,hi],
                    'block_sha256':hashlib.sha256(block.encode()).hexdigest(),
                    'role':'Unchanged original slot-check AST; not the active runtime guard or a constructed native context.'},
                original_verifier=dict(ORIGINAL_VERIFIER),registry_bridge=dict(REGISTRY_BRIDGE),
                original_verify_registry_ast_sha256=ast_sha,
                scope='All frozen31 registry points, unchanged original verify_registry and verify_point checks with authenticated root-bound C1 and current B1 guard. Actual custody is required. No native context, sensitivity/other prelaunch gates or Step4 fence are constructed; no launch authorization.')
            return report
        except A.Refusal as exc:
            raise ValueError('A296_REGISTRY_VERIFY_'+str(exc)) from exc


def write_report(path,report):
    """Optional exclusive report only, under this integration tree."""
    p=Path(path)
    need(p.is_absolute() and '..' not in p.parts,'OUTPUT_ABSOLUTE_NONTRAVERSING_PATH')
    need(p.parent.resolve()==p.parent and p.parent.is_dir() and p.is_relative_to(HERE.parent),'OUTPUT_CANONICAL_INTEGRATION_PARENT')
    need(not os.path.lexists(p),'OUTPUT_EXISTS')
    raw=(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    with p.open('xb') as f:f.write(raw)
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()}


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    ap.add_argument('--a296-binding',required=True)
    ap.add_argument('--a296-binding-sha256',required=True)
    ap.add_argument('--output',help='Optional new report file under integration; defaults to stdout only.')
    ns=ap.parse_args(argv)
    try:
        report=verify_bound({'path':ns.a296_binding,'sha256':ns.a296_binding_sha256})
        if ns.output:
            written=write_report(ns.output,report)
            print(json.dumps({'ok':report['ok'],'n':report['n'],'n_ok':report['n_ok'],'written':written},sort_keys=True))
        else:print(json.dumps(report,sort_keys=True))
        return 0 if report.get('ok') is True else 3
    except (ValueError,KeyError,TypeError,OSError,AttributeError) as exc:
        print(json.dumps({'status':'REFUSED','reason':str(exc)},sort_keys=True));return 2


if __name__=='__main__':sys.exit(main())
