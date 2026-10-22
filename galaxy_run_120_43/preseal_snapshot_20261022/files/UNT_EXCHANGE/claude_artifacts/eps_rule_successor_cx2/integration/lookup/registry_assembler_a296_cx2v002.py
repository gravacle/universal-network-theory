"""Narrow C1/guard bridge around frozen c3v005 registry functions.

All bundle/slot/custody/point-verification behavior is the frozen implementation.
Only an explicit bound A296 policy selects the new guard and seventh producer.
Unbound and ordinary entry points retain the exact old implementation.
"""
import hashlib
from pathlib import Path
import types

ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
OLD={'path':str(ART/'s4rc1_c3/build_c3v005_c2/registry_assembler_c3v005.py'),'sha256':'7df1c4813865b9e1245f5a91d827591a6d87963b6413ab53c50d2a542d211310'}
LINEAGE={'path':str(ART/'eps_rule_successor_cx2/integration/lookup/eps_lineage_cx2v001.py'),'sha256':'da5329e1f9530dc296b9592361cc86b7b480096f9514a9f4aba8cbfdd29c7abb'}
BINDING={'path':str(ART/'eps_rule_successor_cx2/integration/lookup/a296_binding_cx2v002.py'),'sha256':'141c1cd291ece1899ebaa0308882e6b44a91bd8896738e233a94a28cc31bfe43'}


def _load(ref,name):
    raw=Path(ref['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=ref['sha256']:raise ValueError('A296_BRIDGE_SOURCE_PIN')
    m=types.ModuleType(name);m.__file__=ref['path']
    exec(compile(raw,ref['path'],'exec'),m.__dict__)
    return m


O=_load(OLD,'_a296_registry_original')
L=_load(LINEAGE,'_a296_registry_lineage')
H=_load(BINDING,'_a296_registry_binding')
C=O.C
Refusal=C.Refusal
SLOT_GATE=O.SLOT_GATE
load_point_spec=O.load_point_spec
validate_block=O.validate_block
load_approved=O.load_approved
assemble_bundle=O.assemble_bundle
verify_point=O.verify_point
real_custody_fn=O.real_custody_fn
_out_root=O._out_root
main=O.main


def c1_policy_gate(c1_ref,registry_ref,*,roots=(C.ART,),canonical_producers=None,binding_ref=None,snapshot=None):
    if binding_ref is None:
        return O.c1_policy_gate(c1_ref,registry_ref,roots=roots,canonical_producers=canonical_producers)
    try:
        s=snapshot if snapshot is not None else L.snapshot()
        bound=H.validate_binding(s,binding_ref)
        if c1_ref!=bound['c1'] or registry_ref!=H.GENESIS:
            raise ValueError('A296_C1_OR_GENESIS_BINDING_MISMATCH')
        if canonical_producers is not None and canonical_producers!=bound['tail_readiness']['approved_certificate_producers']:
            raise ValueError('A296_CANONICAL_PRODUCERS_OVERRIDE_REFUSED')
        return bound['tail_readiness'],[]
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as exc:
        return None,[type(exc).__name__+': '+str(exc)]


def real_guard(binding_ref=None,snapshot=None):
    if binding_ref is None:return O.real_guard()
    s=snapshot if snapshot is not None else L.snapshot()
    H.validate_binding(s,binding_ref)
    return s.module(H.GUARD,'_a296_bound_b1_guard')
