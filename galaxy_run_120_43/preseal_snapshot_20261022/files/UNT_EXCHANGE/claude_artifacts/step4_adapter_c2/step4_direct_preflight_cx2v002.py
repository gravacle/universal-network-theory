"""Process-free direct-run Context adapter, not a campaign Context constructor.
Reuses the reviewed native prelaunch/certificate/sensitivity methods unchanged.
Explicit state is precisely the four attributes those prelaunch branches consume:
cfg, numerics, D, norm_base. Campaign observations, engine/cache/work-volume and
future deciding/capability records are not inputs to a direct-run preflight.
"""
import copy
DIRECT_CONTEXT_API='UNT_STEP4_DIRECT_PREFLIGHT_CX1V001'
def build(C,config,*,guard,admission):
    G=guard;O=C.O;M=C.M
    G.require(config.get('schema')==O.SCHEMA_CONFIG and not (set(config)-O.CONFIG_KEYS),'DIRECT_C1_SCHEMA_REQUIRED')
    G.require(config.get('synthetic_test') is False,'DIRECT_C1_NON_SYNTHETIC_REQUIRED')
    G.require(config.get('driver',{}).get('sha256')==G.R5_SHA,'DIRECT_C1_R5_REQUIRED')
    G.admitted_source(config['driver'],admission)
    # Exact target-free anchor registration; completed step-4 result slots are not
    # required by registered_anchor and must not be fabricated before those runs.
    M.registered_anchor(config.get('anchor'))
    coord=G.doc(config['coordinate_spec'])
    G.require(coord.get('schema')==O.SCHEMA_SPEC and coord.get('call_spec_mapping',{}).get('mapping_id')==O.SPEC_MAPPING_ID,'DIRECT_COORDINATE_TEMPLATE_BINDING')
    # cx2v002 (root A131, Claude3 0169 R1G-A1): the registered coordinate spec pins its template as {path, schema, sha256};
    # G.doc/verify accept only {path, sha256}. Require the exact 3-key form and schema, verify path+sha, then match the loaded schema.
    tp=coord['call_spec_mapping']['template']
    G.require(isinstance(tp,dict) and set(tp)=={'path','schema','sha256'} and tp.get('schema')=='UNT_GALAXY_M0_FORWARD_CALL_C2V001','DIRECT_TEMPLATE_PIN_FORM')
    template=G.doc({'path':tp['path'],'sha256':tp['sha256']})
    G.require(template.get('schema')==tp['schema'],'DIRECT_TEMPLATE_SCHEMA_MISMATCH')
    G.require(template.get('galaxy')=='DDO154','DIRECT_TEMPLATE_DDO154_REQUIRED')
    inclination=coord['ddo154_forward_constants']['inclination_deg']['value']
    G.require(float(template['physical']['inclination_deg'])==float(inclination),'DIRECT_REGISTERED_INCLINATION_REQUIRED')
    numerics=copy.deepcopy(config['numerics']['block']);C.validate_block(numerics)
    base=copy.deepcopy(template);base['numerics']=copy.deepcopy(numerics)
    # Same template/base construction and A7 checks as O.Context lines1758–1770.
    G.require(not [p for p in O.diff_paths(template,base) if not (p=='numerics' or p.startswith('numerics.'))],'DIRECT_BASE_TEMPLATE_DIFF')
    G.require(not (O.lint_override_keys(base)+O.relative_paths(base)),'DIRECT_BASE_A7_REFUSED')
    D=G.load(config['driver'],admission,'_step4_direct_driver')
    norm_base=D.normalize_spec(copy.deepcopy(base))
    class DirectPreflightContext(C.Context):
        def __init__(self):
            self.cfg=copy.deepcopy(config)
            self.numerics=copy.deepcopy(numerics)
            self.D=D
            self.norm_base=norm_base
    return DirectPreflightContext()
