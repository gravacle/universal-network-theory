"""Exclusive successor of reviewed v001 guard; finite signed-P0 TV bound only."""
import hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
src=(HERE/'certificate_guard_cx2v001.py').read_bytes()
assert hashlib.sha256(src).hexdigest()=='f69678f92c6e18d07c765952c104b1d2fe0fbb90d72746cf9f5d41f2ae2d58b3'
text=src.decode()
old="""                if not isinstance(state['stage_kind'], str) or not state['stage_kind'] or state['nonnegative_masses'] is not True:
                    raise ValueError('state violates GQ positivity premise')
                row = keyed[digest(state)]
"""
new="""                if not isinstance(state['stage_kind'], str) or not state['stage_kind'] or type(state['nonnegative_masses']) is not bool:
                    raise ValueError('invalid state mass-sign declaration')
                row = keyed[digest(state)]
                if state['nonnegative_masses'] is False:
                    signed = proof(row['GQ_SIGNED'], 'GQ_SIGNED')
                    if signed.get('state') != state:
                        raise ValueError('signed GQ state/source mismatch')
                    if signed.get('method') != 'TV_BOUND_WITH_SIGNED_P0' or signed.get('normalization') != 'ABS_SIGNED_ZERO_MODE':
                        raise ValueError('signed GQ requires explicit unchanged signed-P0 normalization')
                    if signed.get('positive_components_verified') is not True:
                        raise ValueError('signed GQ component positivity unverified')
                    if signed.get('GQ_uniform_proof_sha256') != doc['prelaunch']['GQ']['sha256']:
                        raise ValueError('signed GQ uniform-proof mismatch')
                    p0, tv = signed.get('P0_abs_signed_mass_kg'), signed.get('component_mass_sum_kg')
                    if not _number(p0) or p0 <= 0 or not _number(tv) or tv < p0:
                        raise ValueError('signed GQ zero/invalid normalization; root ruling required')
                    bound = (b / (1 - z)) * (tv / p0)
                    recorded = signed.get('max_difference_over_signed_P0_bound')
                    if not _number(recorded) or not math.isfinite(bound) or not math.isclose(recorded, bound, rel_tol=1e-12, abs_tol=1e-18):
                        raise ValueError('signed GQ contradictory TV/P0 bound')
                    if bound > 1e-12:
                        raise ValueError('signed GQ TV/P0 bound insufficient; exact replay or root ruling required')
"""
assert text.count(old)==1
text=text.replace(old,new)
text=text.replace('Fail-closed certificate metadata/gate verifier; no solver or launch imports.',
                  'Fail-closed v002 guard: positive-source GQ plus conservative signed-P0 TV branch.')
with (HERE/'certificate_guard_cx2v002.py').open('xb') as f:f.write(text.encode())
print(hashlib.sha256(text.encode()).hexdigest())
