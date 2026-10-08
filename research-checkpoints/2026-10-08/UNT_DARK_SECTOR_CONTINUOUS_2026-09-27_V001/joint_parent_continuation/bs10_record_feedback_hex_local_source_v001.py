#!/usr/bin/env python3
"""NEW combined small-source vacuum and full-copy certificate; no old imports."""
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING, localcontext
from fractions import Fraction
from itertools import permutations
from pathlib import Path
import hashlib
import json
import math
import os
import resource
import sys
import time
import traceback
import numpy as np

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME='BS10_RECORD_FEEDBACK_HEX_LOCAL_SOURCE_V001'
SOURCE=Path(__file__).resolve()
PROTOCOL=J/(NAME+'.md')
RESULT=J/(NAME+'_RESULT.json')
REPORT=J/(NAME+'_RESULT.md')
RECEIPT=J/(NAME+'_RECEIPT.json')
CP=J/'bs10_record_feedback_hex_local_source_v001_checkpoints'
JS='BS10_RECORD_FEEDBACK_HEX_JOINT_SOURCE_V001'
VS='BS10_RECORD_FEEDBACK_HEX_SOURCE_VACUUM_V001'
JOINT='BS10_RECORD_FEEDBACK_HEX_JOINT_V001'
Q63='BS10_RECORD_FEEDBACK_HEX_SOURCE_V001'
VAC='BS10_RECORD_FEEDBACK_HEX_VACUUM_V001'
BASE='BS10_RECORD_FEEDBACK_HEX_FINITE_V001'
D=2000
SCALE=40*D
ALPHA=Fraction(1,1000)
A_PLUS=(2002,2001,1999,1998,1999,2001)
A_MINUS=tuple(2*D-a for a in A_PLUS)
W=(Fraction(1),Fraction(1,2),Fraction(-1,2),Fraction(-1),Fraction(-1,2),Fraction(1,2))
DIM=6*64*64
SEED_DENOMINATOR=10**12
EXPANSION_ATTEMPTS=24
REFINEMENT_STEPS=32
OFFSETS=(0,1,-1,2,-2)
FRACTIONS=(Fraction(1,2),Fraction(1,3),Fraction(2,3),Fraction(2,5),Fraction(3,5))
VACUUM_TARGET=Fraction(1,10**11)
CERTIFICATE_STAGES=(16,64,256,1024,4096)
MAX_ITERATIONS=4096
ROUND_SCALE=10**60
TARGET=Fraction(1,10**8)
DROP_NORM=1e-14
POSITIVE_FLOOR=1e-100
ATTEMPT_CREATED=False
STAGES={}
FLOAT_ACTION_CALLS=0
INERTIA_SERIAL=0
INPUTS={
 'HELD_HEX_COMPLETE_NONUNIFORM_ADDITION_SOURCE_GATE_V001.md':'c99ceb680037c35f87d6b280c0fd11bb456f1bc798fc429175e3d9a8cc55cbdc',
 'HELD_HEX_SOURCE_SECTOR_SELECTION_RADIUS_V001.md':'b4bd089ba910c78e8eec2500316e9a2dfc4df6128c2dd5d5189b75df6542262a',
 'bs10_record_feedback_hex_joint_v001.py':'d27bc48797b49f9c8a27eee43667dafdfc71f404217153cf0e9f0afb17a97cc6',
 'BS10_RECORD_FEEDBACK_HEX_JOINT_V001.md':'1c4bf052ee95773b73d5d823fdb04a316effba469f458eca382ad52389b7cd81',
 'BS10_RECORD_FEEDBACK_HEX_JOINT_V001_RESULT.json':'ec4b754ae9ec867068f68210ad67d17546ad5b5265e1c92baee4b63b765344fd',
 'BS10_RECORD_FEEDBACK_HEX_JOINT_V001_RECEIPT.json':'92719713b13fcc12e7c4bd6c8e1a2352d9cfee3abac0564c9a0624f491a0a868',
 'bs10_record_feedback_hex_joint_source_v001.py':'1ef4287d6f654aede296d8f1681e917f6d21830307d596baf80b800a90163678',
 'BS10_RECORD_FEEDBACK_HEX_JOINT_SOURCE_V001.md':'8d8d2f4695e3834786e48bd462eb0c9690ea57190febff2ad53bca3e281593a9',
 'BS10_RECORD_FEEDBACK_HEX_JOINT_SOURCE_V001_RESULT.json':'2fb189f2685f5367fc535fad054c38692cbfa3e871627a34a2b18673a6d953ed',
 'BS10_RECORD_FEEDBACK_HEX_JOINT_SOURCE_V001_RECEIPT.json':'e3cfadec3a4f7b06e835ac48e26932da2722a99188b4e38e0e1600cd2dfc18d8',
 'bs10_record_feedback_hex_source_vacuum_v001.py':'3df379b5dbc0c0a4b27cc7f0ad265cdc6e673b174c83f3db0b4e597219495c5b',
 'BS10_RECORD_FEEDBACK_HEX_SOURCE_VACUUM_V001.md':'eba3c816494a4c3be13091e15803688cf604388d1fb76011e0b30c5ddb70394f',
 'BS10_RECORD_FEEDBACK_HEX_SOURCE_VACUUM_V001_RESULT.json':'48c649d26ab8a2718c0119f40976950e941d90babc4a18a6e4b36558bc29fb4c',
 'BS10_RECORD_FEEDBACK_HEX_SOURCE_VACUUM_V001_RECEIPT.json':'711f3291d0626864926ebae6fa79dcd7724b833e2c7189600f1bd9da461e9da2',
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def exact(value):
    value = Fraction(value)
    displays = []
    for mode in (ROUND_FLOOR,ROUND_CEILING):
        with localcontext() as context:
            context.prec,context.rounding = 20,mode
            displays.append(str(Decimal(value.numerator)/Decimal(value.denominator)))
    return {'numerator':value.numerator,'denominator':value.denominator,
            'decimal20_lower':displays[0],'decimal20_upper':displays[1]}

def frac(value):
    return Fraction(value['numerator'],value['denominator'])

def interval(lo,hi):
    return {'lower':exact(lo),'upper':exact(hi),'width':exact(hi-lo)}

def exclusive(path,obj):
    with path.open('xb') as stream:
        stream.write(canonical(obj)+b'\n')
        stream.flush()
        os.fsync(stream.fileno())
    return sha(path)

def event(kind,**fields):
    entry = {'event':kind,'pid':os.getpid(),'elapsed_seconds':time.perf_counter()-T0,**fields}
    with (CP/'journal.jsonl').open('ab') as stream:
        stream.write(canonical(entry)+b'\n')
        stream.flush()
        os.fsync(stream.fileno())

def save(name,obj,**fields):
    digest = exclusive(CP/name,obj)
    STAGES[name] = digest
    event('stage_complete',filename=name,sha256=digest,**fields)
    return digest

def add(checks,label,condition):
    checks.append({'label':label,'passed':bool(condition)})

def bounds(value):
    return frac(value['lower']),frac(value['upper'])

def same(first,second):
    return bounds(first)==bounds(second)

def subtract(first,second):
    a,b = bounds(first)
    c,d = bounds(second)
    return interval(a-d,b-c)

def scale(value,factor):
    a,b = bounds(value)
    return interval(factor*a,factor*b) if factor>=0 else interval(factor*b,factor*a)

def sign(value):
    lo,hi = bounds(value)
    return 'POSITIVE' if lo>0 else ('NEGATIVE' if hi<0 else 'ZERO_CONTAINING_OR_UNRESOLVED')

def verify_map(mapping,directory,label):
    out = {}
    for name,wanted in mapping.items():
        got = sha(directory/name)
        if got != wanted:
            raise RuntimeError(label+' changed: '+name)
        out[name] = got
    return out

def packet(tag,source_name,expected):
    directory = J/(source_name[:-3]+'_checkpoints')
    result = json.loads((J/(tag+'_RESULT.json')).read_text())
    receipt = json.loads((J/(tag+'_RECEIPT.json')).read_text())
    raw_hash,receipt_hash = sha(J/(tag+'_RESULT.json')),sha(J/(tag+'_RECEIPT.json'))
    if raw_hash != expected[tag+'_RESULT.json'] or receipt_hash != expected[tag+'_RECEIPT.json']:
        raise RuntimeError('Parent anchor mismatch: '+tag)
    if receipt['result_raw_sha256'] != raw_hash or receipt['result_canonical_sha256'] != hashlib.sha256(canonical(result)).hexdigest():
        raise RuntimeError('Parent raw/canonical mismatch: '+tag)
    report_hash = sha(J/(tag+'_RESULT.md'))
    if report_hash != receipt['report_sha256']:
        raise RuntimeError('Parent current report mismatch: '+tag)
    for key,name in (('source_sha256',source_name),('protocol_sha256',tag+'.md')):
        if not(result[key]==receipt[key]==expected[name]==sha(J/name)):
            raise RuntimeError('Parent code pin mismatch: '+tag)
    key = 'authenticated_inputs' if 'authenticated_inputs' in receipt else 'input_sha256'
    if result[key] != receipt[key] or result['checkpoint_sha256'] != receipt['checkpoint_sha256']:
        raise RuntimeError('Parent input/checkpoint equality mismatch: '+tag)
    checkpoints = verify_map(receipt['checkpoint_sha256'],directory,'Parent checkpoint '+tag)
    manifest_hash = checkpoints['input_manifest.json']
    if not(result['manifest_sha256']==receipt['manifest_sha256']==manifest_hash):
        raise RuntimeError('Parent manifest equality mismatch: '+tag)
    manifest = json.loads((directory/'input_manifest.json').read_text())
    if manifest['source_sha256'] != receipt['source_sha256'] or manifest['protocol_sha256'] != receipt['protocol_sha256'] or (key in manifest and manifest[key] != receipt[key]):
        raise RuntimeError('Parent manifest payload mismatch: '+tag)
    lines = (directory/'journal.jsonl').read_bytes().splitlines(keepends=True)
    events = [json.loads(line) for line in lines]
    if not events or events[-1]['event'] != 'receipt_complete' or events[-1]['receipt_sha256'] != receipt_hash:
        raise RuntimeError('Parent final receipt commit mismatch: '+tag)
    prefix = hashlib.sha256(b''.join(lines[:-1])).hexdigest()
    if prefix != receipt['journal_prefix_sha256']:
        raise RuntimeError('Parent prefix mismatch: '+tag)
    starts = [row for row in events if row['event']=='started']
    if len(starts)!=1 or starts[0]['manifest_sha256']!=manifest_hash:
        raise RuntimeError('Parent start seal mismatch: '+tag)
    for filename,wanted in checkpoints.items():
        if sum(row.get('filename')==filename and row.get('sha256')==wanted for row in events)!=1:
            raise RuntimeError('Parent checkpoint commit mismatch: '+tag+'/'+filename)
    if result['checks_failed']!=0 or receipt['checks_failed']!=0:
        raise RuntimeError('Parent arithmetic unqualified: '+tag)
    proof = {'result_raw_sha256':raw_hash,'receipt_sha256':receipt_hash,'report_sha256':report_hash,
             'checkpoint_sha256':checkpoints,'journal_prefix_sha256':prefix,'authenticated_inputs':receipt[key]}
    return proof,result

def authenticate():
    direct = verify_map(INPUTS,J,'Frozen direct input')
    jsp,js = packet(JS,'bs10_record_feedback_hex_joint_source_v001.py',direct)
    vsp,vs = packet(VS,'bs10_record_feedback_hex_source_vacuum_v001.py',direct)
    ji,vi = jsp['authenticated_inputs'],vsp['authenticated_inputs']
    jp,joint = packet(JOINT,'bs10_record_feedback_hex_joint_v001.py',ji['direct_input_sha256'])
    qp,q63 = packet(Q63,'bs10_record_feedback_hex_source_v001.py',vi['direct_input_sha256'])
    if jp!=ji['joint_parent'] or qp!=ji['q63_source_parent'] or qp['authenticated_inputs']!=vi['source_parent_authenticated_inputs']:
        raise RuntimeError('Shared parent receipt/input proof mismatch')
    v0p,vacuum = packet(VAC,'bs10_record_feedback_hex_vacuum_v001.py',jp['authenticated_inputs']['direct_input_sha256'])
    bp,finite = packet(BASE,'bs10_record_feedback_hex_finite_v001.py',qp['authenticated_inputs']['direct_input_sha256'])
    if v0p!=ji['vacuum_parent'] or bp!=ji['finite_parent']:
        raise RuntimeError('Shared baseline proof mismatch')
    inherited = {}
    for label,mapping,directory in (
        ('joint0_direct',jp['authenticated_inputs']['direct_input_sha256'],J),
        ('joint0_inherited_direct',jp['authenticated_inputs']['inherited_direct_input_sha256'],J),
        ('joint0_root',jp['authenticated_inputs']['inherited_root_input_sha256'],ROOT),
        ('q63_direct',qp['authenticated_inputs']['direct_input_sha256'],J),
        ('q63_root',qp['authenticated_inputs']['inherited_input_sha256'],ROOT)):
        inherited[label]=verify_map(mapping,directory,'Inherited '+label)
    if bp['authenticated_inputs']!=inherited['q63_root'] or bp['authenticated_inputs']!=inherited['joint0_root']:
        raise RuntimeError('Original finite root-input proof mismatch')
    original = json.loads((J/'bs10_record_feedback_hex_finite_v001_checkpoints/structure.json').read_text())
    prefix,alias = original['checks'],finite['structural_checks']['checks']
    if prefix != alias[:len(prefix)] or ji['preserved_finite_stage_alias']!={'prefix_count':len(prefix),'nested_count':len(alias),'prefix_equal':True}:
        raise RuntimeError('Preserved original stage-check alias mismatch')
    if js['ground_certificate_status']!='FULL_HELD_SOURCE_GROUND_INTERVAL_CERTIFIED' or not vacuum['q63_strict_selected']:
        raise RuntimeError('Certified matched premises missing')
    a = js['finite_source_assembly']
    if not(same(a['E10_authenticated'],joint['final_ground_interval_raw']) and same(a['Ebg0_authenticated'],vacuum['global_vacuum_interval'])
           and same(a['Ebg63alpha_authenticated'],q63['new_Ealpha_interval']) and same(vs['retained_q63_source_vacuum_interval'],q63['new_Ealpha_interval'])):
        raise RuntimeError('Shared source/background reference mismatch')
    proofs = {'direct_input_sha256':direct,'joint_source_parent':jsp,'source_vacuum_parent':vsp,
              'baseline_joint_parent':jp,'retained_q63_parent':qp,'zero_source_vacuum_parent':v0p,
              'original_finite_parent':bp,'inherited_current_input_bytes':inherited,
              'preserved_original_stage_alias':ji['preserved_finite_stage_alias']}
    references={'E10':joint['final_ground_interval_raw'],'Ebg0':vacuum['global_vacuum_interval'],
                'Delta0':joint['final_matched_addition_interval_raw'],
                'old20H_diagonal':joint['complete_action_controls']['diagonal20'],
                'large1600_diagonal':js['complete_nonuniform_action_controls']['diagonal1600'],
                'zero_vacuum_diagonals':vacuum['dihedral_and_physical_controls']['all64_physical_diagonals'],
                'large_vacuum_controls':vs['complete_source_and_R3_controls'],
                'large_E1':js['final_ground_interval_raw'],
                'large_Ebg_global':vs['global_source_vacuum_interval'],
                'large_Ebg63':vs['retained_q63_source_vacuum_interval'],
                'zero_record_gap':vacuum['other_sector_minus_q63_interval'],
                'large_joint_stages':js['certificate_stages']}
    return proofs,references

def index(q,n,v):
    return 6*(64*q+n)+v


def rotate3(word):
    return sum(((word>>u)&1)<<((u+3)%6) for u in range(6))


def background_integer(q,n,a,exterior=D):
    total=0
    for u in range(6):
        left,right=(n>>((u-1)%6))&1,(n>>u)&1
        delta=left+right-1
        c=-4*a[u]+left*(a[(u-1)%6]+a[u])+right*(a[u]+a[(u+1)%6])+(a[u]+exterior)
        total+=40*a[u]*delta*delta-20*a[u]*delta+10*(1-((q>>u)&1))*c
    return total


def physical_background_integer(q,n,a,exterior=D):
    total=120*exterior
    for u in range(6):
        delta=((n>>((u-1)%6))&1)+((n>>u)&1)-1
        bit=(q>>u)&1
        total+=40*a[u]*(delta*delta+bit)-10*(a[u]+exterior)*(bit+1)
    for e in range(6):
        total-=10*(a[e]+a[(e+1)%6])*((n>>e)&1)*(((q>>e)&1)+((q>>((e+1)%6))&1))
    return total


def source_diagonal(q,n,v,a,exterior=D):
    left,right=(n>>((v-1)%6))&1,(n>>v)&1
    return background_integer(q,n,a,exterior)+40*a[v]+5*(left*(a[(v-1)%6]+a[v])+right*(a[v]+a[(v+1)%6])+(a[v]+exterior))


def action_ports(q,n,v,a):
    row=[(index(q,n^(1<<e),v),-4*(a[e]+a[(e+1)%6]),'incidence') for e in range(6)]
    for e,dest in (((v-1)%6,(v-1)%6),(v,(v+1)%6)):
        if n&(1<<e):
            row.append((index(q,n,dest),-2*(a[e]+a[(e+1)%6]),'carrier'))
    row.append((index(q^(1<<v),n,v),-4*a[v],'copy'))
    return row


def selection_proof(references):
    large=references['large_vacuum_controls']['all64_record_source_controls']
    zero=references['zero_vacuum_diagonals']
    maximum_all,maximum63=Fraction(0),Fraction(0)
    witness=None
    for row in large:
        q=row['qword']
        for n,large_diagonal in enumerate(row['diagonal1600']):
            slope=(Fraction(large_diagonal,1600)-frac(zero[str(q)][n]))/Fraction(1,20)
            if abs(slope)>maximum_all:
                maximum_all=abs(slope)
                witness={'qword':q,'nword':n,'signed_diagonal_slope':exact(slope)}
            if q==63:
                maximum63=max(maximum63,abs(slope))
    off=Fraction(1,10)*sum(abs(W[e]+W[(e+1)%6]) for e in range(6))
    delta=frac(references['zero_record_gap']['lower'])
    norm_all=maximum_all+off
    radius=delta/norm_all
    margin=delta-norm_all*ALPHA
    checks=[]
    add(checks,'all4096_saved_source_diagonal_slope_norm3',maximum_all==3)
    add(checks,'saved_q63_source_diagonal_slope_norm5over2',maximum63==Fraction(5,2))
    add(checks,'midpoint_flip_slope_row_norm3over5',off==Fraction(3,5))
    add(checks,'allq_source_norm_bound18over5',norm_all==Fraction(18,5))
    add(checks,'saved_record_gap5139916237over500000000000',delta==Fraction(5139916237,500000000000))
    add(checks,'selection_radius_exact',radius==Fraction(5139916237,1800000000000))
    add(checks,'small_alpha_strictly_inside_radius',0<ALPHA<radius)
    add(checks,'selection_margin_exact_positive',margin==Fraction(3339916237,500000000000)>0)
    return {'alpha':exact(ALPHA),'saved_uniform_other_sector_gap_lower':exact(delta),
            'saved_diagonal_source_norm_allq':exact(maximum_all),'saved_diagonal_source_norm_q63':exact(maximum63),
            'diagonal_norm_witness':witness,'offdiagonal_source_row_norm':exact(off),
            'allq_source_norm_bound':exact(norm_all),'guaranteed_radius':exact(radius),
            'other_record_sector_ground_gap_lower_at_small_alpha':exact(margin),
            'q63_even_concavity_trial_used':True,'other63_sector_new_solves':0,
            'selection_is_ground_preparation_or_relaxation_claim':False,'checks':list(checks)},checks


def build_action(references):
    checks=[]
    physical=True
    affine_background=True
    uniform_background=True
    r3_background=True
    whole_collar_ward=True
    large_rows={row['qword']:row['diagonal1600'] for row in references['large_vacuum_controls']['all64_record_source_controls']}
    small_background=[]
    for q in range(64):
        row=[]
        for n in range(64):
            value=background_integer(q,n,A_PLUS)
            row.append(value)
            physical=physical and value==physical_background_integer(q,n,A_PLUS)
            zero20=20*frac(references['zero_vacuum_diagonals'][str(q)][n])
            affine_background=affine_background and value==3920*zero20+large_rows[q][n]
            uniform_background=uniform_background and background_integer(q,n,(D,)*6)==4000*zero20
            r3_background=r3_background and value==background_integer(rotate3(q),rotate3(n),A_MINUS)
            for factor in (Fraction(1,2),Fraction(2)):
                whole_collar_ward=whole_collar_ward and background_integer(q,n,(factor*D,)*6,factor*D)==factor*background_integer(q,n,(D,)*6)
        small_background.append(row)
    diagonal,ports=[],[]
    reciprocal,unique_negative,r3_diag,r3_ports,affine_joint,uniform_joint,ward_joint=True,True,True,True,True,True,True
    for q in range(64):
        for n in range(64):
            for v in range(6):
                i=index(q,n,v)
                value=source_diagonal(q,n,v,A_PLUS)
                row=action_ports(q,n,v,A_PLUS)
                diagonal.append(value)
                ports.append(row)
                affine_joint=affine_joint and value==3920*references['old20H_diagonal'][i]+references['large1600_diagonal'][i]
                uniform_joint=uniform_joint and source_diagonal(q,n,v,(D,)*6)==4000*references['old20H_diagonal'][i]
                unique_negative=unique_negative and len({dest for dest,weight,kind in row})==len(row) and all(weight<0 for dest,weight,kind in row)
                qr,nr,vr=rotate3(q),rotate3(n),(v+3)%6
                r3_diag=r3_diag and value==source_diagonal(qr,nr,vr,A_MINUS)
                mapped=[]
                for dest,weight,kind in row:
                    dq,tail=divmod(dest,64*6)
                    dn,dv=divmod(tail,6)
                    mapped.append((index(rotate3(dq),rotate3(dn),(dv+3)%6),weight,kind))
                r3_ports=r3_ports and sorted(mapped)==sorted(action_ports(qr,nr,vr,A_MINUS))
                for factor in (Fraction(1,2),Fraction(2)):
                    ward_joint=ward_joint and source_diagonal(q,n,v,(factor*D,)*6,factor*D)==factor*source_diagonal(q,n,v,(D,)*6)
    for i,row in enumerate(ports):
        reciprocal=reciprocal and all((i,w,kind) in ports[dest] for dest,w,kind in row)
    reached={0}
    frontier=[0]
    while frontier:
        i=frontier.pop()
        for dest,weight,kind in ports[i]:
            if dest not in reached:
                reached.add(dest)
                frontier.append(dest)
    old_large=(42,41,39,38,39,41)
    affine_ports=True
    uniform_ports=True
    whole_port_ward=True
    for e in range(6):
        for base_weight,multiplier in ((-4,-4),(-2,-2)):
            small=multiplier*(A_PLUS[e]+A_PLUS[(e+1)%6])
            affine_ports=affine_ports and small==3920*base_weight+multiplier*(old_large[e]+old_large[(e+1)%6])
            uniform_ports=uniform_ports and multiplier*(2*D)==4000*base_weight
            whole_port_ward=whole_port_ward and all(multiplier*(2*factor*D)==factor*multiplier*(2*D) for factor in (Fraction(1,2),Fraction(2)))
        affine_ports=affine_ports and -4*A_PLUS[e]==3920*(-2)-4*old_large[e]
        uniform_ports=uniform_ports and -4*D==4000*(-2)
        whole_port_ward=whole_port_ward and all(-4*factor*D==factor*(-4*D) for factor in (Fraction(1,2),Fraction(2)))
    add(checks,'all4096_owned_physical_backgrounds_equal',physical)
    add(checks,'all4096_background_affinity3920M20plusM1600',affine_background)
    add(checks,'all4096_uniform_background4000M20',uniform_background)
    add(checks,'all4096_R3_backgrounds',r3_background)
    add(checks,'full_dimension24576',len(diagonal)==len(ports)==DIM)
    add(checks,'all24576_joint_affinity3920M20plusM1600',affine_joint)
    add(checks,'all24576_uniform_joint4000M20',uniform_joint)
    add(checks,'distinct_negative_offdiagonal_ports',unique_negative)
    add(checks,'all_joint_ports_reciprocal',reciprocal)
    add(checks,'joint_graph_connected',len(reached)==DIM)
    add(checks,'all24576_R3_joint_diagonals',r3_diag)
    add(checks,'all_R3_joint_ports',r3_ports)
    add(checks,'all_source_ports_affine',affine_ports)
    add(checks,'all_uniform_ports4000M20',uniform_ports)
    add(checks,'whole_collar_Lhalf_Ltwo_background_Ward',whole_collar_ward)
    add(checks,'whole_collar_Lhalf_Ltwo_joint_diagonal_Ward',ward_joint)
    add(checks,'whole_collar_port_Ward',whole_port_ward)
    add(checks,'source_nodes_positive',min(A_PLUS)>0)
    add(checks,'clamped_exterior_identity_derived_zero',sum(a-D for a in A_PLUS)==0)
    vacuum_diagonal=small_background[63]
    edges=[(n,n^(1<<e),-4*(A_PLUS[e]+A_PLUS[(e+1)%6])) for n in range(64) for e in range(6) if not n&(1<<e)]
    add(checks,'q63_vacuum_joint_background_agrees',all(diagonal[index(63,n,v)]-40*A_PLUS[v]-5*(((n>>((v-1)%6))&1)*(A_PLUS[(v-1)%6]+A_PLUS[v])+((n>>v)&1)*(A_PLUS[v]+A_PLUS[(v+1)%6])+(A_PLUS[v]+D))==vacuum_diagonal[n] for n in range(64) for v in range(6)))
    stage={'basis_order':'i=6(64q+n)+v','dimension':DIM,'integer_scale':SCALE,
           'source_denominator':D,'a_plus':list(A_PLUS),'a_minus':list(A_MINUS),
           'background80000_all64q':small_background,'diagonal80000':diagonal,
           'offdiagonal_port_count':sum(len(row) for row in ports),'connected_count':len(reached),
           'fixed_exterior_reference80000':120*D,'derived_clamped_exterior_identity':-10*sum(a-D for a in A_PLUS),
           'vacuum_q63_diagonal80000':vacuum_diagonal,'vacuum_q63_edges80000':edges,
           'direct_second_alpha_contact':0,'record_parity_copy_unitary':True,'checks':list(checks)}
    return diagonal,ports,{'diagonal':vacuum_diagonal,'edges':edges},stage,checks


class ZeroMinor(Exception):
    def __init__(self,index,minors):
        self.index,self.minors=index,list(minors)
        super().__init__('Zero leading minor at order '+str(index))

def bareiss(matrix):
    a = [row[:] for row in matrix]
    size,previous,minors,divisions = len(a),1,[],0
    for k in range(size-1):
        pivot = a[k][k]
        minors.append(pivot)
        if pivot == 0:
            raise ZeroMinor(k+1,minors)
        for i in range(k+1,size):
            for j in range(i,size):
                numerator = pivot*a[i][j]-a[i][k]*a[k][j]
                value,remainder = divmod(numerator,previous)
                if remainder:
                    raise ArithmeticError('Nonexact Bareiss division')
                a[i][j] = a[j][i] = value
                divisions += 1
        for i in range(k+1,size):
            a[i][k] = a[k][i] = 0
        previous = pivot
    minors.append(a[-1][-1])
    if minors[-1] == 0:
        raise ZeroMinor(size,minors)
    signs = [1]+[1 if x>0 else -1 for x in minors]
    return minors,sum(a!=b for a,b in zip(signs,signs[1:])),divisions

def direct_det(matrix):
    out = 0
    for order in permutations(range(len(matrix))):
        inversions = sum(order[i]>order[j] for i in range(len(order)) for j in range(i+1,len(order)))
        term = (-1)**inversions
        for i,j in enumerate(order):
            term *= matrix[i][j]
        out += term
    return out

def algorithm_controls():
    checks,rows = [],[]
    for i,matrix in enumerate(([[2,1],[1,-1]],[[0,1],[1,2]],[[2,1,0],[1,3,1],[0,1,-1]])):
        direct = [direct_det([row[:n] for row in matrix[:n]]) for n in range(1,len(matrix)+1)]
        try:
            minors,count,divisions = bareiss(matrix)
            add(checks,f'algorithm_control{i}_minors',minors == direct)
            add(checks,f'algorithm_control{i}_inertia',count == 1)
            rows.append({'matrix':matrix,'direct_minors':direct,'bareiss_minors':minors,'negative_inertia':count})
        except ZeroMinor as error:
            add(checks,f'algorithm_control{i}_zero',i == 1 and error.index == 1 and direct[0] == 0)
            rows.append({'matrix':matrix,'direct_minors':direct,'rejected_zero_order':error.index})
    return {'rows':rows,'checks':list(checks)},checks

def inertia_candidate(model,shift,purpose):
    global INERTIA_SERIAL
    matrix=[[0]*64 for _ in range(64)]
    for i,value in enumerate(model['diagonal']):
        matrix[i][i]=shift.denominator*value-SCALE*shift.numerator
    for i,j,value in model['edges']:
        matrix[i][j]=matrix[j][i]=shift.denominator*value
    serial=INERTIA_SERIAL
    INERTIA_SERIAL+=1
    row={'serial':serial,'matrix':'NEW_SMALL_Q63_VACUUM_ONLY','dimension':64,
         'shift':exact(shift),'positive_integer_scale':SCALE*shift.denominator,'purpose':purpose}
    try:
        minors,count,divisions=bareiss(matrix)
        row.update({'valid_nonzero_leading_minors':True,'leading_minors_scaled_integer':minors,
                    'negative_inertia':count,'exact_divisions':divisions})
    except ZeroMinor as error:
        row.update({'valid_nonzero_leading_minors':False,'rejected_zero_minor_order':error.index,
                    'leading_minors_scaled_integer':error.minors,'negative_inertia':None})
    name=f'vacuum_inertia_{serial:04d}.json'
    save(name,row,valid=row['valid_nonzero_leading_minors'])
    row['checkpoint_filename']=name
    return row

def ground_bracket(model,seed):
    center = Fraction(math.floor(seed*SEED_DENOMINATOR),SEED_DENOMINATOR)
    attempts,lo,hi = [],None,None
    for j in range(EXPANSION_ATTEMPTS):
        radius = Fraction(2**j,SEED_DENOMINATOR)
        endpoints = []
        for side,base in (('lower',center-radius),('upper',center+radius)):
            candidate = None
            for offset in OFFSETS:
                shift = base+Fraction(offset,17*SEED_DENOMINATOR)
                row = inertia_candidate(model,shift,f'expand{j}_{side}_offset{offset}')
                if row['valid_nonzero_leading_minors']:
                    candidate = (shift,row)
                    break
            endpoints.append(candidate)
        attempts.append({'attempt':j,'radius':exact(radius),
                         'lower_checkpoint':None if endpoints[0] is None else endpoints[0][1]['checkpoint_filename'],
                         'upper_checkpoint':None if endpoints[1] is None else endpoints[1][1]['checkpoint_filename']})
        if all(x is not None for x in endpoints):
            if endpoints[0][1]['negative_inertia'] == 0 and endpoints[1][1]['negative_inertia'] == 1:
                lo,hi = endpoints
                break
    if lo is None:
        save('UNRESOLVED_bracket.json',{'attempts':attempts,'center':exact(center)})
        raise ArithmeticError('Frozen expansion attempts exhausted')
    refinements = []
    for step in range(REFINEMENT_STEPS):
        if hi[0]-lo[0] <= VACUUM_TARGET:
            break
        choice = None
        for position in FRACTIONS:
            value = lo[0]+position*(hi[0]-lo[0])
            row = inertia_candidate(model,value,f'refine{step}_fraction{position}')
            if row['valid_nonzero_leading_minors']:
                choice = (value,row)
                break
        if choice is None:
            raise ArithmeticError('All frozen refinement candidates had zero minors')
        if choice[1]['negative_inertia'] == 0:
            lo = choice
        else:
            hi = choice
        refinements.append(choice[1]['checkpoint_filename'])
    if hi[0]-lo[0] > VACUUM_TARGET:
        save('UNRESOLVED_bracket.json',{'attempts':attempts,'refinements':refinements,'interval':interval(lo[0],hi[0])})
        raise ArithmeticError('Frozen refinements exhausted')
    checks = []
    add(checks,'ground_lower_count_zero',lo[1]['negative_inertia'] == 0)
    add(checks,'ground_upper_count_one',hi[1]['negative_inertia'] == 1)
    add(checks,'ground_bracket_target',0<hi[0]-lo[0]<=VACUUM_TARGET)
    row = {'matrix':'NEW_SMALL_Q63_VACUUM_ONLY','seed_not_certificate':seed,'center':exact(center),
           'interval':interval(lo[0],hi[0]),'lower_endpoint_evidence':lo[1],'upper_endpoint_evidence':hi[1],
           'expansion_attempts':attempts,'refinements':refinements,'checks':list(checks)}
    save('new_small_vacuum_ground_bracket.json',row)
    return row,lo[0],hi[0],checks

def vacuum_seed(model):
    matrix=np.zeros((64,64),dtype=float)
    for i,value in enumerate(model['diagonal']):
        matrix[i,i]=value/SCALE
    for i,j,value in model['edges']:
        matrix[i,j]=matrix[j,i]=value/SCALE
    values=np.linalg.eigh(matrix)[0]
    if not np.all(np.isfinite(values)):
        raise ArithmeticError('Nonfinite NEW vacuum seeds')
    row={'matrix':'NEW_SMALL_Q63_VACUUM_ONLY','seed_eigenvalues_not_certificates':[float(value) for value in values],
         'dimension':64,'new_vacuum_eigh_count':1,'vectors_saved_or_claimed':False}
    save('new_small_vacuum_seed.json',row)
    return float(values[0])

def float_h(x,diagonal):
    global FLOAT_ACTION_CALLS
    FLOAT_ACTION_CALLS += 1
    state = np.asarray(x,dtype=float).reshape(64,64,6)
    out = np.asarray(diagonal,dtype=float).reshape(64,64,6)*state
    words = np.arange(64)
    for e in range(6):
        bond = A_PLUS[e]+A_PLUS[(e+1)%6]
        out -= 4*bond*state[:,words^(1<<e),:]
        occupied = ((words>>e)&1).astype(float)
        out[:,:,e] -= 2*bond*occupied[None,:]*state[:,:,(e+1)%6]
        out[:,:,(e+1)%6] -= 2*bond*occupied[None,:]*state[:,:,e]
    for v in range(6):
        out[:,:,v] -= 4*A_PLUS[v]*state[words^(1<<v),:,v]
    return out.reshape(DIM)/SCALE

def round_ratio_even(a,b):
    quotient,remainder = divmod(a,b)
    if 2*remainder>b or (2*remainder==b and quotient%2):
        quotient += 1
    return quotient

def rounding_controls():
    checks = []
    for a,b,wanted in ((1,2,0),(3,2,2),(5,2,2),(7,2,4),(9,4,2),(11,4,3)):
        add(checks,f'nearest_even_{a}_{b}',round_ratio_even(a,b)==wanted)
    for value,wanted in ((0.5,ROUND_SCALE//2),(0.25,ROUND_SCALE//4),(1.0,ROUND_SCALE)):
        a,b = value.as_integer_ratio()
        add(checks,'exact_binary_float_round_'+value.hex(),round_ratio_even(a*ROUND_SCALE,b)==wanted)
    return {'round_scale':ROUND_SCALE,'tie_rule':'nearest_even_by_exact_as_integer_ratio_divmod','checks':list(checks)},checks

def save_float_state(iteration,x,p_previous,diagnostics):
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(p_previous)) or np.min(x)<=0:
        raise ArithmeticError('Nonfinite/nonpositive floating proposal at iteration '+str(iteration))
    obj = {'iteration':iteration,'basis_order':'i=6(64q+n)+v',
           'x_hex':[float(value).hex() for value in x],
           'p_previous_hex':[float(value).hex() for value in p_previous],
           'x_squared_norm':float(np.dot(x,x)),'x_min':float(np.min(x)),
           'diagnostics_trial_only':diagnostics,'elapsed_seconds':time.perf_counter()-T0}
    return save(f'iteration_{iteration:04d}_float_state.json',obj,iteration=iteration)

def optimizer_step(x,p_previous,diagonal):
    hx = float_h(x,diagonal)
    rq = float(np.dot(x,hx))
    residual = hx-rq*x
    basis,kept,dropped = [],[],[]
    for label,column in (('x',x),('residual',residual),('p_previous',p_previous)):
        candidate = column.copy()
        for existing in basis:
            candidate -= float(np.dot(existing,candidate))*existing
        norm = float(np.linalg.norm(candidate))
        if not math.isfinite(norm):
            raise ArithmeticError('Nonfinite MGS column norm')
        if norm <= DROP_NORM:
            dropped.append(label)
        else:
            basis.append(candidate/norm)
            kept.append(label)
    if not basis:
        raise ArithmeticError('Empty frozen projected subspace')
    projected = np.empty((len(basis),len(basis)),dtype=float)
    for j in range(len(basis)):
        action = float_h(basis[j],diagonal)
        for i in range(j+1):
            value = float(np.dot(basis[i],action))
            projected[i,j] = projected[j,i] = value
    if not np.all(np.isfinite(projected)):
        raise ArithmeticError('Nonfinite projected trial matrix')
    values,vectors = np.linalg.eigh(projected)
    trial = sum((vectors[j,0]*basis[j] for j in range(len(basis))),np.zeros(DIM,dtype=float))
    trial = np.maximum(np.abs(trial),POSITIVE_FLOOR)
    norm = float(np.linalg.norm(trial))
    if not math.isfinite(norm) or norm<=0:
        raise ArithmeticError('Nonfinite/zero absolute proposal norm')
    newx = trial/norm
    newp = newx-float(np.dot(x,newx))*x
    if not np.all(np.isfinite(newx)) or not np.all(np.isfinite(newp)) or np.min(newx)<=0:
        raise ArithmeticError('Nonfinite/nonpositive normalized proposal')
    gram = np.array([[float(np.dot(a,b)) for b in basis] for a in basis])
    diagnostics = {'rayleigh_before_trial':rq,'residual_norm_before_trial':float(np.linalg.norm(residual)),
                   'retained_columns':kept,'dropped_columns':dropped,'projected_dimension':len(basis),
                   'projected_eigenvalues_trial_only':[float(value) for value in values],
                   'max_MGS_Gram_error':float(np.max(np.abs(gram-np.eye(len(basis))))),
                   'numpy_eigensolve_dimension_at_most3':True}
    return newx,newp,diagnostics

def integer_apply(z,diagonal,ports):
    return [diagonal[i]*z[i]+sum(w*z[j] for j,w,kind in ports[i]) for i in range(DIM)]

def independent_quadratic(z,diagonal):
    total = sum(diagonal[i]*z[i]*z[i] for i in range(DIM))
    for q in range(64):
        for n in range(64):
            for e in range(6):
                bond = A_PLUS[e]+A_PLUS[(e+1)%6]
                if not n&(1<<e):
                    for v in range(6):
                        total -= 8*bond*z[index(q,n,v)]*z[index(q,n^(1<<e),v)]
                else:
                    total -= 4*bond*z[index(q,n,e)]*z[index(q,n,(e+1)%6)]
            for v in range(6):
                if not q&(1<<v):
                    total -= 8*A_PLUS[v]*z[index(q,n,v)]*z[index(q^(1<<v),n,v)]
    return total

def certificate(iteration,x,diagonal,ports,references):
    rounded = []
    floor_count = 0
    for value in x:
        a,b = float(value).as_integer_ratio()
        candidate = round_ratio_even(a*ROUND_SCALE,b)
        if candidate == 0:
            candidate = 1
            floor_count += 1
        rounded.append(candidate)
    mz = integer_apply(rounded,diagonal,ports)
    min_index,max_index = 0,0
    for i in range(1,DIM):
        if mz[i]*rounded[min_index] < mz[min_index]*rounded[i]:
            min_index = i
        if mz[i]*rounded[max_index] > mz[max_index]*rounded[i]:
            max_index = i
    lower = Fraction(mz[min_index],SCALE*rounded[min_index])
    cw_upper = Fraction(mz[max_index],SCALE*rounded[max_index])
    quadratic = sum(a*b for a,b in zip(rounded,mz))
    norm = sum(a*a for a in rounded)
    upper = Fraction(quadratic,SCALE*norm)
    checks = []
    add(checks,f'iter{iteration}_positive_full_integer_vector',len(rounded)==DIM and min(rounded)>0)
    add(checks,f'iter{iteration}_integer_action_dimension',len(mz)==DIM and all(isinstance(a,int) for a in mz))
    add(checks,f'iter{iteration}_independent_undirected_quadratic',quadratic==independent_quadratic(rounded,diagonal))
    add(checks,f'iter{iteration}_CW_Rayleigh_order',lower<=upper<=cw_upper)
    vector = {'iteration':iteration,'basis_order':'i=6(64q+n)+v','round_scale':ROUND_SCALE,
              'z':rounded,'Mz':mz,'rounded_zero_floor_count':floor_count,
              'exact_quadratic_z_Mz':quadratic,'exact_squared_norm_z':norm}
    vector_hash = save(f'iteration_{iteration:04d}_integer_vector.json',vector,iteration=iteration)
    row = {'iteration':iteration,'integer_vector_filename':f'iteration_{iteration:04d}_integer_vector.json',
           'integer_vector_sha256':vector_hash,'ground_interval_raw':interval(lower,upper),
           'CW_ratio_interval_raw':interval(lower,cw_upper),'rayleigh_upper':exact(upper),
           'minimum_ratio_witness':{'index':min_index,'Mz_i':mz[min_index],'z_i':rounded[min_index],'ratio':exact(lower)},
           'maximum_ratio_witness':{'index':max_index,'Mz_i':mz[max_index],'z_i':rounded[max_index],'ratio':exact(cw_upper)},
           'matched_small_addition_interval_raw':interval(lower-frac(references['Ebgsmall']['upper']),upper-frac(references['Ebgsmall']['lower'])),
           'target_energy_width':exact(TARGET),'raw_target_width_candidate':upper-lower<=TARGET,
           'rounded_zero_floor_count':floor_count,'checks':list(checks),
           'elapsed_seconds':time.perf_counter()-T0,'ru_maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    return row,lower,upper,checks

def finite_quantities(joint_source,bg,references,alpha):
    delta=subtract(joint_source,bg)
    f1=scale(subtract(references['E10'],joint_source),2/(alpha*alpha))
    fbg=scale(subtract(references['Ebg0'],bg),2/(alpha*alpha))
    fadd=scale(subtract(references['Delta0'],delta),2/(alpha*alpha))
    change=scale(subtract(delta,references['Delta0']),2/(alpha*alpha))
    return {'E1':joint_source,'Ebg':bg,'Delta':delta,'F1':f1,'Fbg':fbg,'Fadd':fadd,'D':change}


def finite_assembly(joint_source,bg,references):
    small=finite_quantities(joint_source,bg,references,ALPHA)
    large={label:finite_quantities(references['large_E1'],references[key],references,Fraction(1,20))
           for label,key in (('global','large_Ebg_global'),('retained63','large_Ebg63'))}
    checks=[]
    for label,quantities in [('small_global',small),('small_retained63',small)]+[('large_'+k,v) for k,v in large.items()]:
        add(checks,'Fadd_equals_F1_minus_Fbg_'+label,same(quantities['Fadd'],subtract(quantities['F1'],quantities['Fbg'])))
        add(checks,'D_equals_negative_Fadd_'+label,same(quantities['D'],scale(quantities['Fadd'],-1)))
        add(checks,'Delta_interval_order_'+label,frac(quantities['Delta']['lower'])<=frac(quantities['Delta']['upper']))
    small_by_label={'global':small,'retained63':small}
    comparisons={label:{key:subtract(small[key],quantities[key]) for key in ('Delta','F1','Fbg','Fadd','D')}
                 for label,quantities in large.items()}
    separate_drops={'joint':subtract(references['E10'],joint_source),'vacuum':subtract(references['Ebg0'],bg)}
    candidates={label:('STRICT_FINITE_DROP' if frac(bounds['lower'])>0 else ('CONCAVITY_CONTRADICTION_PRESERVED' if frac(bounds['upper'])<0 else 'DROP_ZERO_OR_UNRESOLVED_PRESERVED'))
                for label,bounds in separate_drops.items()}
    signs={label:{key:sign(values[key]) for key in ('Delta','F1','Fbg','Fadd','D')} for label,values in [('small_global',small),('small_retained63',small)]+[('large_'+k,v) for k,v in large.items()]}
    add(checks,'same_small_global_retained63_intervals',same(small_by_label['global']['Ebg'],small_by_label['retained63']['Ebg']))
    return {'E10_authenticated':references['E10'],'Ebg0_authenticated':references['Ebg0'],'Delta0_authenticated':references['Delta0'],
            'small_alpha':exact(ALPHA),'small_quantities_by_reference':small_by_label,
            'large_alpha':exact(Fraction(1,20)),'large_quantities_by_reference':large,
            'small_minus_large_independent_intervals':comparisons,
            'raw_sign_descriptors':signs,'separate_ground_drops':separate_drops,'raw_drop_candidates':candidates,
            'large_joint_stage_intervals_inherited':[row['ground_interval_raw'] for row in references['large_joint_stages']],
            'derivative_stiffness_fit_gravity_mass_metric_claim':False,'checks':list(checks)},checks


def format_report(result):
    def rat(value):
        return str(value['numerator'])+'/'+str(value['denominator'])
    lines=['# Held hexagon: small complete native source V001','',
           f"Controls: {result['checks_passed']}/{result['checks_total']}; failed {result['checks_failed']}.",
           'Vacuum certificate: '+result['vacuum_certificate_status']+'.',
           'Joint certificate: '+result['ground_certificate_status']+'.',
           'Requested joint precision: '+result['requested_precision_status']+'.',
           'Earned vacuum selection: '+str(result['q63_global_selected_earned'])+'.',
           'Selection margin lower: '+rat(result['source_selection_proof']['other_record_sector_ground_gap_lower_at_small_alpha'])+'.','',
           '| NEW vacuum | exact lower | exact upper | width |','|---|---:|---:|---:|']
    bounds=result['new_vacuum_interval_raw']
    lines.append('| q63, also global by the selection proof | '+rat(bounds['lower'])+' | '+rat(bounds['upper'])+' | '+rat(bounds['width'])+' |')
    lines+=['','| completed joint stage | exact lower | exact upper | width | matched addition lower | matched addition upper |','|---:|---:|---:|---:|---:|---:|']
    for row in result['joint_certificate_stages']:
        energy,addition=row['ground_interval_raw'],row['matched_small_addition_interval_raw']
        lines.append('| '+str(row['iteration'])+' | '+rat(energy['lower'])+' | '+rat(energy['upper'])+' | '+rat(energy['width'])+' | '+rat(addition['lower'])+' | '+rat(addition['upper'])+' |')
    assembly=result['finite_source_assembly']
    lines+=['','| source point / reference | signed quantity | exact lower | exact upper | raw sign |','|---|---|---:|---:|---|']
    count=0
    for point,key in (('small','small_quantities_by_reference'),('large','large_quantities_by_reference')):
        for label,values in assembly[key].items():
            for name in ('Delta','F1','Fbg','Fadd','D'):
                bounds=values[name]
                lines.append('| '+point+'/'+label+' | '+name+' | '+rat(bounds['lower'])+' | '+rat(bounds['upper'])+' | '+sign(bounds)+' |')
                count+=1
    if count!=20:
        raise RuntimeError('Frozen source/reference report census mismatch')
    lines+=['','| small minus large / reference | quantity | exact lower | exact upper |','|---|---|---:|---:|']
    compare_count=0
    for label,values in assembly['small_minus_large_independent_intervals'].items():
        for name,bounds in values.items():
            lines.append('| '+label+' | '+name+' | '+rat(bounds['lower'])+' | '+rat(bounds['upper'])+' |')
            compare_count+=1
    if compare_count!=10 or len(result['joint_certificate_stages'])<1:
        raise RuntimeError('Frozen comparison/stage report census mismatch')
    lines+=['',
           'The NEW small source lies in the proven q63 selection neighborhood. Global-static and retained63 labels coincide here, while the inherited alpha1/20 sector switch and its two reference branches remain unchanged.',
           'F values are finite-field drops; D is the opposite finite-field increase. Every raw sign and interval is retained. Two source points do not measure a zero-field derivative or select a stiffness function.',
           'Only the NEW q63 vacuum eigensolve/inertia and NEW matrix-free full-copy proposal/certificates are calculated. Other63 vacuum blocks, alpha-minus, old operators/eigensolves/inertia/evolution and old producers are not replayed.',
           'Full exterior/current/feedback/storage/hop/flip/copy energy is sourced once. Whole-collar uniform scaling is the Ward control; fixed-exterior inside scaling is a different experiment.',
           'Perron visibility concerns definite-q carrier injection in this held finite B/x action. No numerical residue, rank-three pole, bulk phase, physical ruler/clock, common normalized gravity/expansion law or Stage3 completion is earned.',
           'Vacuum and joint strict-drop qualitative flags require all arithmetic controls passing. Ground-sector conservation alone does not form a state or an adiabatic preparation.',
           'The positive optimizer is trial-only. Exact integer CW/Rayleigh and rational inertia endpoints remain the certificates. Every stage, partial failure and original input byte is preserved.',
           '',f"Elapsed seconds: {result['elapsed_seconds']}; native peak RSS: {result['ru_maxrss_native']}.",'']
    return '\n'.join(lines)


def main():
    global ATTEMPT_CREATED
    if sys.argv[1:]!=['--execute']:
        raise RuntimeError('Explicit --execute required; no calculation launched')
    for path in (RESULT,REPORT,RECEIPT,CP):
        if path.exists():
            raise FileExistsError('Exclusive reserved output exists: '+str(path))
    inputs,references=authenticate()
    source_hash,protocol_hash=sha(SOURCE),sha(PROTOCOL)
    CP.mkdir()
    ATTEMPT_CREATED=True
    manifest={'schema':NAME+'_INPUT_MANIFEST','pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
              'authenticated_inputs':inputs,'alpha':exact(ALPHA),'source_denominator':D,'a_plus':list(A_PLUS),
              'a_minus':list(A_MINUS),'exterior_source':1,'integer_scale':SCALE,'joint_dimension':DIM,
              'vacuum_bracket_policy':{'seed_denominator':SEED_DENOMINATOR,'expansion_attempts':EXPANSION_ATTEMPTS,
                 'offsets_over17seed':list(OFFSETS),'refinement_max':REFINEMENT_STEPS,'fractions':[exact(x) for x in FRACTIONS],
                 'target_width':exact(VACUUM_TARGET)},
              'joint_optimizer_frozen':{'initial':'uniform_positive_norm1','maximum_iterations':MAX_ITERATIONS,
                 'certificate_stages':list(CERTIFICATE_STAGES),'drop_norm':DROP_NORM,'positive_float_floor':POSITIVE_FLOOR,
                 'round_scale':ROUND_SCALE,'round_rule':'nearest_even_exact_as_integer_ratio','target_energy_width':exact(TARGET),
                 'MGS_passes':1,'column_order':['x','residual','p_previous'],'fallback':False},
              'numpy_version':np.__version__,'environment':{key:os.environ.get(key) for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','PYTHONDONTWRITEBYTECODE')}}
    manifest_hash=save('input_manifest.json',manifest)
    event('started',manifest_sha256=manifest_hash,source_sha256=source_hash,protocol_sha256=protocol_hash)
    selection,checks=selection_proof(references)
    save('source_selection_proof.json',selection)
    diagonal,ports,vacuum_model,structure,extra=build_action(references)
    checks.extend(extra)
    ones_integer=integer_apply([1]*DIM,diagonal,ports)
    ones_float=float_h(np.ones(DIM,dtype=float),diagonal)
    difference=float(np.max(np.abs(ones_float-np.array(ones_integer,dtype=float)/SCALE)))
    add(checks,'uniform_NEW_float_action_matches_exact_integer_row_sum',difference<=1e-12)
    structure['uniform_NEW_float_action_max_error']=difference
    structure['checks']=list(extra)+[dict(checks[-1])]
    save('new_complete_source_action_controls.json',structure)
    algorithm,extra=algorithm_controls()
    save('inertia_algorithm_controls.json',algorithm)
    checks.extend(extra)
    rounding,extra=rounding_controls()
    save('nearest_even_rounding_controls.json',rounding)
    checks.extend(extra)
    if any(not row['passed'] for row in checks):
        raise ArithmeticError('Prospective structural/source/inertia control failed')
    seed=vacuum_seed(vacuum_model)
    vacuum_row,vacuum_lower,vacuum_upper,extra=ground_bracket(vacuum_model,seed)
    checks.extend(extra)
    references_with_vacuum=dict(references)
    references_with_vacuum['Ebgsmall']=vacuum_row['interval']
    save('completed_new_vacuum_and_selection.json',{'vacuum_interval_raw':vacuum_row['interval'],
         'vacuum_bracket':vacuum_row,'selection_proof':selection,'global_and_retained63_reference_same':True,
         'checks_failed_through_stage':sum(not check['passed'] for check in checks)})
    x=np.full(DIM,1/math.sqrt(DIM),dtype=float)
    p_previous=np.zeros(DIM,dtype=float)
    initial_hash=save_float_state(0,x,p_previous,{'initial_uniform_positive':True})
    rows,precision_earned,last_diagnostics=[],False,{}
    for iteration in range(1,MAX_ITERATIONS+1):
        x,p_previous,last_diagnostics=optimizer_step(x,p_previous,diagonal)
        if iteration not in CERTIFICATE_STAGES:
            continue
        float_hash=save_float_state(iteration,x,p_previous,last_diagnostics)
        row,lower,upper,extra=certificate(iteration,x,diagonal,ports,references_with_vacuum)
        row['float_state_filename']=f'iteration_{iteration:04d}_float_state.json'
        row['float_state_sha256']=float_hash
        checks.extend(extra)
        row['controls_failed_through_stage']=sum(not check['passed'] for check in checks)
        row['target_width_earned_through_stage']=row['raw_target_width_candidate'] and row['controls_failed_through_stage']==0
        save(f'iteration_{iteration:04d}_energy_certificate.json',row,iteration=iteration)
        rows.append(row)
        print(json.dumps({'pid':os.getpid(),'phase':'joint','iteration':iteration,
              'raw_width_decimal20_upper':row['ground_interval_raw']['width']['decimal20_upper'],
              'stage_controls_failed':row['controls_failed_through_stage'],'elapsed_seconds':time.perf_counter()-T0}),flush=True)
        if row['target_width_earned_through_stage']:
            precision_earned=True
            break
    if not rows:
        raise ArithmeticError('Frozen optimizer produced no exact joint certificate')
    final=rows[-1]
    assembly,extra=finite_assembly(final['ground_interval_raw'],vacuum_row['interval'],references)
    checks.extend(extra)
    add(checks,'declared_completed_joint_stage_census',[row['iteration'] for row in rows]==list(CERTIFICATE_STAGES[:len(rows)]))
    add(checks,'no_iteration_beyond4096',iteration<=MAX_ITERATIONS)
    final_inputs,final_references=authenticate()
    add(checks,'all_frozen_parent_input_checkpoint_report_bytes_unchanged',final_inputs==inputs and final_references==references)
    add(checks,'new_source_protocol_bytes_unchanged',sha(SOURCE)==source_hash and sha(PROTOCOL)==protocol_hash)
    add(checks,'private_source_check_list_unchanged',selection['checks']==checks[:len(selection['checks'])])
    failed=sum(not check['passed'] for check in checks)
    qualified=failed==0
    drops=assembly['raw_drop_candidates']
    result={'schema':NAME+'_RESULT','status':'EXACT_ARITHMETIC_PASS' if qualified else 'ARITHMETIC_FAILED_PRESERVED',
            'vacuum_certificate_status':'NEW_Q63_VACUUM_INTERVAL_CERTIFIED' if qualified else 'RAW_VACUUM_ARITHMETIC_UNQUALIFIED',
            'q63_global_selected_earned':qualified and frac(selection['other_record_sector_ground_gap_lower_at_small_alpha'])>0,
            'ground_certificate_status':'NEW_FULL_COPY_GROUND_INTERVAL_CERTIFIED' if qualified else 'RAW_JOINT_ARITHMETIC_UNQUALIFIED',
            'requested_precision_status':('TARGET_WIDTH_EARNED' if precision_earned else 'TARGET_WIDTH_UNEARNED_VALID_INTERVAL_PRESERVED') if qualified else 'PRECISION_ARITHMETIC_UNQUALIFIED',
            'vacuum_finite_source_status':drops['vacuum'] if qualified else 'FINITE_SOURCE_ARITHMETIC_UNQUALIFIED',
            'joint_finite_source_status':drops['joint'] if qualified else 'FINITE_SOURCE_ARITHMETIC_UNQUALIFIED',
            'chi0_strictly_positive_qualitative_only':qualified and drops['vacuum']=='STRICT_FINITE_DROP',
            'chi1_strictly_positive_qualitative_only':qualified and drops['joint']=='STRICT_FINITE_DROP',
            'raw_target_precision_candidate':final['raw_target_width_candidate'],
            'pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
            'authenticated_inputs':inputs,'manifest_sha256':manifest_hash,'checkpoint_sha256':dict(STAGES),
            'alpha':exact(ALPHA),'source_denominator':D,'integer_scale':SCALE,'dimension':DIM,
            'source_selection_proof':selection,'new_complete_source_controls':structure,'inertia_algorithm_controls':algorithm,
            'new_vacuum_bracket':vacuum_row,'new_vacuum_interval_raw':vacuum_row['interval'],
            'small_global_vacuum_interval_raw':vacuum_row['interval'],'small_retained63_vacuum_interval_raw':vacuum_row['interval'],
            'rounding_controls':rounding,'initial_float_state_sha256':initial_hash,'joint_certificate_stages':rows,
            'final_joint_interval_raw':final['ground_interval_raw'],'finite_source_assembly':assembly,
            'iterations_completed':iteration,'NEW_float_H_action_calls':FLOAT_ACTION_CALLS,'NEW_vacuum_eigh_count':1,
            'NEW_other_vacuum_eigh_count':0,'maximum_joint_projected_eigensolve_dimension':3,
            'alpha_minus_from_exact_R3_only':True,'alpha_minus_run':False,'direct_second_alpha_contact':0,
            'old_producer_operator_eigensolve_inertia_evolution_replay':False,
            'numerical_derivative_gravity_mass_metric_bulk_phase_completion_claim':False,
            'checks':checks,'checks_total':len(checks),'checks_passed':len(checks)-failed,'checks_failed':failed,
            'elapsed_seconds':time.perf_counter()-T0,'ru_maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    result_hash=exclusive(RESULT,result)
    canonical_hash=hashlib.sha256(canonical(result)).hexdigest()
    event('result_complete',filename=RESULT.name,sha256=result_hash,canonical_sha256=canonical_hash)
    text=format_report(result)
    with REPORT.open('x') as stream:
        stream.write(text)
        stream.flush()
        os.fsync(stream.fileno())
    report_hash=sha(REPORT)
    event('report_complete',filename=REPORT.name,sha256=report_hash)
    prefix_hash=sha(CP/'journal.jsonl')
    receipt={'schema':NAME+'_RECEIPT','pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
             'authenticated_inputs':inputs,'manifest_sha256':manifest_hash,'checkpoint_sha256':dict(STAGES),
             'result_raw_sha256':result_hash,'result_canonical_sha256':canonical_hash,'report_sha256':report_hash,
             'journal_prefix_sha256':prefix_hash,'checks_failed':failed,'checks_total':len(checks),'checks_passed':len(checks)-failed,
             'status':result['status'],'elapsed_seconds':result['elapsed_seconds'],'ru_maxrss_native':result['ru_maxrss_native']}
    receipt_hash=exclusive(RECEIPT,receipt)
    event('receipt_complete',filename=RECEIPT.name,receipt_sha256=receipt_hash)
    print(json.dumps({'pid':os.getpid(),'status':result['status'],'checks_passed':len(checks)-failed,'checks_total':len(checks),
          'result_raw_sha256':result_hash,'receipt_sha256':receipt_hash,'elapsed_seconds':result['elapsed_seconds']}),flush=True)
    return 0 if qualified else 2


if __name__=='__main__':
    T0=time.perf_counter()
    try:
        sys.exit(main())
    except Exception as error:
        if ATTEMPT_CREATED:
            evidence={'error_type':type(error).__name__,'error_message':str(error),'traceback':traceback.format_exc(),
                      'pid':os.getpid(),'elapsed_seconds':time.perf_counter()-T0,'checkpoint_sha256':dict(STAGES),
                      'rerun_or_resume_authorized':False}
            try:
                digest=exclusive(CP/'ERROR.json',evidence)
                event('error',filename='ERROR.json',sha256=digest,error_type=type(error).__name__)
            except Exception:
                pass
        print(json.dumps({'error_type':type(error).__name__,'error_message':str(error),'pid':os.getpid()}),flush=True)
        sys.exit(3)
