"""Prospective full common-window continuation of protected derived starts.
Root execution only; no prefix replay or boundary state modification.
"""
from pathlib import Path
from decimal import Decimal as D
from datetime import datetime, timezone
from functools import lru_cache
import argparse, ast, hashlib, json, math, os, time, traceback
import numpy as np
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_K10_DERIVED_FULL_COMMON_CONTINUATION_V001'
SHORT='CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001'
PARENT='CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002'
AC=3e-8; AF=1e-6; NSTEP=2048; FRAME_STRIDE=64; CP_STRIDE=128
CURVATURE=1e-5; K=10.; KB=.02; C=1.98; CBAR=.99
CP=299792458.; MPC=3.0856775814913673e22
OMEGAS=(.1,1.,10.,100.); GROUPS=('FINE','START')
PROTOCOL_SHA='eed23fb57ed87d5c245283d01ba6ba34f7837c9ce2b3e3206e1c8e73c9ffcfb3'
ERROR_KEYS=('stage_error','dense_error','metric_momentum_error','curvature_increment_error','baryon_Euler_error','conservative_trace_increment_error','conservative_trace_window_error','los_continuity_error','discarded_source_bound','kernel_tail_bound','collision_kernel_tail_bound')
INCREMENT_KEYS=('metric_momentum_error','curvature_increment_error','baryon_Euler_error','conservative_trace_increment_error','conservative_trace_window_error')
ANCHOR_KEYS={'x','eta','R','qV','cGamma','Gamma','dipole','Pi'}
PINS={
 "CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_DEFAULT_OUTPUT.json": "07e8e4e7fe524fd9d1f1a19422f293f11a49573f6ee6d1bf016b17c80ec70437",
 "CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_HALF_OUTPUT.json": "1df474629eb706d1315f090de228059c59db3ad58c127be2b614c005dc471386",
 "CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002_FINE_CP_002048.json": "da6b2ce2b4576f9914dd88966b866ca5a48ca1e6685122f518a1f90df1bb2077",
 "CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002_FINE_CP_002048_COMMIT.json": "83fa8e2adcdc3f00adc612274112e68750b2b823c8ca09b6e857c764aa037cfc",
 "CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002_MANIFEST.json": "1def78ccec871fc95e9099b17ee4f05079f95804e51769b9cf3d37fb75904d94",
 "CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002_RECEIPT.json": "d026359746d108e69a137bbdb590492f257a27da652682da6b5690d495ec69c8",
 "CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002_RESULT.json": "ba43de8fd479fd3987b4bf5163b9c7fc848d691537962ad7c485d46a92f3be2c",
 "CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002_START_CP_001664.json": "8153f119a00e212f91cdab61a849dc4d390b0265f41167aefe87b9abd1d0b726",
 "CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V002_START_CP_001664_COMMIT.json": "c6f1ac9d7f17bee00165ba988b49c3ab56af3f6ae78656368aada5ff9ea94ac1",
 "CONSTRAINED_U_K10_COMMON_DENSITY_AND_CURRENT_REGULAR_JETS_V001.md": "dcfdf786cd6cdc80ff6182db84d4562a1b0a16150b329fcda8bc5e866fc38282",
 "CONSTRAINED_U_K10_COMMON_START_SCALAR_COEFFICIENTS_V001.md": "8f831f8c0c8e3aef5cdf1fac5d29c52212445cf8d6c30fe34ada5460939c9495",
 "CONSTRAINED_U_K10_COMMON_START_SCALAR_COEFFICIENTS_V001_RECEIPT.json": "f88f042d3332e8ff7de40cb612094d11b74356b416f105b8aa887ebbcecf0209",
 "CONSTRAINED_U_K10_COMMON_START_SCALAR_COEFFICIENTS_V001_REPORT.md": "cab7660aa6b467ccf62d86dd4f25cbc2ea151f7fae77b914e6e7e9e5a59fd088",
 "CONSTRAINED_U_K10_COMMON_START_SCALAR_COEFFICIENTS_V001_RESULT.json": "c8e6b26f229332a3371b46e1a2d8ba80bbaed1ca5fa64689f8c674260ca0dc47",
 "CONSTRAINED_U_K10_DENSITY_CURRENT_AND_ANGULAR_COMPLETION_V001.md": "c0bb7fc0f58c587fb0182383c894116ff1908533cfa6ad1e754dcf5232edfa4f",
 "CONSTRAINED_U_K10_DERIVED_FULL_COMMON_CONTINUATION_V001.md": "eed23fb57ed87d5c245283d01ba6ba34f7837c9ce2b3e3206e1c8e73c9ffcfb3",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001.md": "1788a1d89c5edf0e2c9ba37a1d5984818e050d78117cbffa5125fe8486ea41a0",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_MANIFEST.json": "039595640719d782c3948a2d593bcf8902d119e7cc0ae142e4d73550237afbba",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_N128_CP_000032.json": "3bc4f728c0cabdb11ca2d3b93f1490e52bccefb28516d040b3d267ab558eb5ad",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_N128_CP_000032_COMMIT.json": "ec27989c4d9526e2f494c8f1047fce869def80fad0eb3b368725dd9e7b938e67",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_N128_CP_000064.json": "4b2f43144e445a7d7a08a7c6d533e93436ae81edbbf6e03f20107083bcc815a5",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_N128_CP_000064_COMMIT.json": "3126c0b81857260f89f6c3c1dbcf5524241351390201028df34598ea3d89bc25",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_N128_CP_000096.json": "a7a6a06105d3807da62baf2a6ff3aafa3feedb472a936092e37d3810527c40d0",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_N128_CP_000096_COMMIT.json": "a76f08d62288a2be96237af1cce881dd2a8bf02f7801460eef1a7c43167954d2",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_N128_CP_000128.json": "dbe303c239a2b3b505c3e2930d1c60960f6ccb2135df0b2d85827f93fe741811",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_N128_CP_000128_COMMIT.json": "78215916e5305f52641b89f4d63ce0b062c76294ec8cfa577aa4b830676207c0",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_N64_CP_000032.json": "93d3dcb67559366b0a8fb738bb312b6fbfcb03bc383a3cefbeae575dacc59e84",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_N64_CP_000032_COMMIT.json": "98d1fff4158eaae426b4c29008308fae31974181f9e80eb6aaaeda98e55a0b6c",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_N64_CP_000064.json": "f1447ff468eb5d7ea2a42155559c642b519076030adbac8b9c99ea2681049501",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_N64_CP_000064_COMMIT.json": "d32cd42c218e58fb5b2c3bf8aa40473d3d31f4e34b4080e8838abb6c546c802a",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_PREPARATION_CP.json": "1580d92338dd1ecb95a660afc5eb67cc2ffef8d5d7987026ff182eb64fc63f29",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_PREPARATION_CP_COMMIT.json": "7faeb459ef63e407335df134d61d9737ddea04111cd9461d80e31b7d04a002e9",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_RECEIPT.json": "a8577e68c9388a7f64c2b03c99f377746bd91a35cf4ff32f096811b7fba63cd1",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_REPORT.md": "2e56fe03a54396559469c172ee96e12a0feead6b676fd0582782de1c3e14b851",
 "CONSTRAINED_U_K10_DERIVED_START_OVERLAP_V001_RESULT.json": "9a807da90ce2d735a5469a83eb20c9087969a7c94e820c3de0703ff4f1daa553",
 "CONSTRAINED_U_K10_NATIVE_JETS_AND_NORMAL_CONSTRAINT_PROPAGATION_V001.md": "c6be2c46873770c267420fa8097c6773c830be8029230e61a9f4048b595a87aa",
 "CONSTRAINED_U_K10_REGULAR_METRIC_COMPLETION_V001.md": "e5d638570320830f5edbdc7390af23819a930474733e6441c70f0536a2752d5f",
 "CONSTRAINED_U_K10_SAVED_DENSITY_CURRENT_ANGULAR_COMPLETION_V001.md": "b8353499e58edd0de0c25a774b0cd810585e42d7d336d7bf638e91efb568f924",
 "CONSTRAINED_U_K10_SAVED_DENSITY_CURRENT_ANGULAR_COMPLETION_V001_RECEIPT.json": "bfb914d954c68e6d37a28f7e226868190f165b3b0173c2cd30cbdb0c626f52bd",
 "CONSTRAINED_U_K10_SAVED_DENSITY_CURRENT_ANGULAR_COMPLETION_V001_REPORT.md": "a40cd2676540161fe47809c0974699a6d52eaf818b291b6afe840f4abe86bf00",
 "CONSTRAINED_U_K10_SAVED_DENSITY_CURRENT_ANGULAR_COMPLETION_V001_RESULT.json": "01d1e6a978c045b768f44625bca8a155cda1e25c3f79676e7a0ca7b83dbb9262",
 "CONSTRAINED_U_K10_SAVED_METRIC_COMPLETION_V001.md": "a864cae70c86ee30d08ac24265faf14bbc80a04e80dd1dded7c25c1b458f3503",
 "CONSTRAINED_U_K10_SAVED_METRIC_COMPLETION_V001_RECEIPT.json": "42b7a05641f420dea5dea06d36d03a60b485c3de32e6496b51f151e8997203d3",
 "CONSTRAINED_U_K10_SAVED_METRIC_COMPLETION_V001_REPORT.md": "3a12c5d303ab2201ebc80dc71fffd68465ff3a24e12d27294a2993d5506e043b",
 "CONSTRAINED_U_K10_SAVED_METRIC_COMPLETION_V001_RESULT.json": "04b48d6da753c2cca3b1d95d653a0b34d1c4a8e20a0da3a93bbc1193881bfa81",
 "CONSTRAINED_U_STABLE_ANGULAR_RADIATION_MEMORY_CHART_V001.md": "8471e9d40bb02dca8deed6dfc2bd49e1c4d1f00cd18af456b27df5082e62b04c",
 "actual_opacity_retarded_radiation_kernel_v001.py": "b43b9def6b0eeaafd12f5f947b8dd77cdf02ab60838951f799fb0bc043bc9721",
 "constrained_u_clock_gradient_early_transfer_v004.py": "a4e78b6467b0ba5884c8da2081ff580378b4afb839a90cec548fcf30a389fa07",
 "constrained_u_galaxy_horizon_stable_y_gauss_v002.py": "f70826091d11c38715c00b3a572e08c48a41252018477ac4cf3a20b2ded9f531",
 "constrained_u_k10_common_start_scalar_coefficients_v001.py": "5709f6e12e1c751ea7a253863c60328b1f30208037ccff692c6104966aea4839",
 "constrained_u_k10_derived_start_overlap_v001.py": "27a9dfa54318a58300fa387b380047043c10518e8e2aea7b751b3280ba9d1808",
 "constrained_u_k10_saved_density_current_angular_completion_v001.py": "9b10ac63bcaf32085d0c0a2c5c40b9dc38aaedbde280c8bb3422cc8b21f38c78",
 "constrained_u_k10_saved_metric_completion_v001.py": "a6409e33170e21c1b1423d9f685edff6b7fb0a2d2064f407d00875abf08867c2"
}
DEFINITIONS=('sha','load_declared_helpers','legendre','bessel','si_vector','initial_transport','gauss','equilibrate','to_raw','chart_coefficients','chart_rates','chart_stage_matrix','lagrange_values','cubic_envelope','CubicKernel','stable_anchor','stable_initial_multipoles','compensated_residual','gauss_block_solve','source_vectors','memory_panel','fixed_panel_response','free_history_response','source_envelopes','coupled_gauss','load_optical_namespace','finite_tree')

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def encode(v):
 if isinstance(v,D):assert v.is_finite();return str(v)
 if isinstance(v,np.ndarray):return encode(v.tolist())
 if isinstance(v,np.generic):return encode(v.item())
 if isinstance(v,dict):return {str(k):encode(w) for k,w in v.items()}
 if isinstance(v,(list,tuple)):return [encode(w) for w in v]
 if type(v) is float:assert math.isfinite(v)
 return v

def write(name,v):
 p=BASE/name;data=(json.dumps(encode(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 with p.open('xb') as f:f.write(data)
 p.chmod(0o444);return sha(p)

def load_definitions():
 p=BASE/'constrained_u_galaxy_horizon_stable_y_gauss_v002.py';tree=ast.parse(p.read_text())
 nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in DEFINITIONS]
 assert {n.name for n in nodes}==set(DEFINITIONS)
 env=dict(BASE=BASE,Path=Path,ast=ast,hashlib=hashlib,np=np,math=math,json=json,lru_cache=lru_cache,K=K,CP=CP,MPC=MPC,KB=KB,C=C,CBAR=CBAR,CURVATURE=CURVATURE,
  EARLY_SOURCE_SHA=PINS['constrained_u_clock_gradient_early_transfer_v004.py'],OPTICAL_KERNEL_SHA=PINS['actual_opacity_retarded_radiation_kernel_v001.py'],CHECKED_HELPERS=('background','Thermal','Layout','coefficients','rates','stage_matrix','snapshot'))
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p)+'<unchanged-short-overlap-definitions>','exec'),env)
 return env

def base_snapshot(x,y,fixed,lay,therm,snodes,weights,omega,helpers,env):
 dy,f=env['chart_rates'](x,y,fixed,lay,therm,snodes,weights,omega,helpers)
 q,h,b,rg,rn,w=(f[k] for k in ('q','h','b','rg','rn','w'));P=KB*q*f['ncalc']/2+CBAR*f['Z']
 nt=[q*q*f['psi'],3*h*f['S'],b*y[1],rg*y[3],rn*y[5],w*y[7],-q*P]
 contrast=y[1]+3*h*f['wb'];Eb=b*contrast;Eg=rg*(y[3]+4*h*f['wg']);En=rn*(y[5]+4*h*y[6]);Ec=w*y[7];Ep=-q*P
 raw=env['to_raw'](y,f['bg'],fixed);Pi=y[lay.fg[2]]+y[lay.pol[0]]+y[lay.pol[2]]
 reads=[raw[3]/4+f['phi'],q*raw[4],q*raw[2],f['psi']+f['phi'],y[lay.fg[2]],Pi,y[lay.fn[2]],contrast,Eb,Eg+En,Ec,Ep,-KB*q*q*f['ncalc']/2,-CBAR*q*f['Z'],q*f['ncalc']]
 normal=math.fsum(map(float,nt));raw_nt=[q*q*f['psi'],3*h*f['mom'],b*raw[1],rg*raw[3],rn*raw[5],w*raw[7],-q*P]
 normal_error=abs(normal)/max(sum(abs(float(t)) for t in raw_nt),q*q*CURVATURE*1e-10)
 stable_error=abs(normal)/max(sum(abs(float(t)) for t in nt),q*q*CURVATURE*1e-10)
 vdd=(float(weights@dy[lay.zd])-2*f['Ld']*f['vd']-f['Ldd']*f['v'])/f['L']
 nd=vdd-f['bg']['cs_dt']*y[7]-f['c']*dy[7]
 et=[KB*q*nd/2,-KB*h*q*f['ncalc']/2,CBAR*f['Zd'],2*h*P,CBAR*f['Q']*f['sigma']]
 ef=KB*q*CURVATURE*max(h,f['Q'],omega)*1e-10/2
 wbd=f['g']*y[4]/f['rb']-f['c']*y[7]
 wgd=h*f['wg']+y[3]/4-y[lay.fg[2]]/2-f['g']*y[4]-f['c']*y[7]
 Sdot=b*(wbd-3*h*f['wb'])+4*rg*(wgd-4*h*f['wg'])/3+4*rn*(dy[6]-4*h*y[6])/3
 total=b+4*(rg+rn)/3+w;totaldot=-3*h*b-16*h*(rg+rn)/3-3*h*(1+f['c'])*w
 momdot=Sdot+totaldot*y[8]+total*dy[8]
 phid=f['psid']-2*(rg*(dy[lay.fg[2]]-2*h*y[lay.fg[2]])+rn*(dy[lay.fn[2]]-2*h*y[lay.fn[2]]))/q**2
 psidd=momdot-f['bg']['h_dt']*f['phi']-h*phid
 tt=[psidd,h*phid,3*h*f['psid'],(2*f['bg']['h_dt']+3*h*h)*f['phi'],q*q*(f['psi']-f['phi'])/3,-f['c']*w*raw[7],-(rg*raw[3]+rn*raw[5])/3]
 tf=CURVATURE*max(h*h,q*q)*1e-12
 return dict(a=f['bg']['a'],stable_state=y,raw_state=raw,readouts=reads,normal_terms=nt,normal_error=normal_error,
  Phi=f['phi'],Psi=f['psi'],w=w,Gamma_phase=y[7],sigma=f['sigma'],n=f['ncalc'],physical_seed_qualified=False,
  native_Euler_terms=et,native_Euler_error=abs(math.fsum(map(float,et)))/max(sum(abs(float(t)) for t in et),ef),
  proper_trace_terms=tt,proper_trace_error=abs(math.fsum(map(float,tt)))/max(sum(abs(float(t)) for t in tt),tf),
  positive_baryon_drag_used=True,old_failure_flags_changed=False,raw_normal_terms=raw_nt,raw_normal_residual=math.fsum(map(float,raw_nt)),stable_normal_error=stable_error,
  shear_error=abs(f['psi']-f['phi']-2*(rg*y[lay.fg[2]]+rn*y[lay.fn[2]])/q**2)/CURVATURE)

def full_snapshot(x,y,fixed,lay,therm,snodes,weights,omega,helpers,env):
 case=base_snapshot(x,y,fixed,lay,therm,snodes,weights,omega,helpers,env)
 _,f=env['chart_rates'](x,y,fixed,lay,therm,snodes,weights,omega,helpers)
 q,h,rg,rn,b,w=(f[k] for k in ('q','h','rg','rn','b','w'));raw=case['raw_state'];normal=math.fsum(case['normal_terms'])
 Eb=case['readouts'][8];Eg=rg*(y[3]+4*h*f['wg']);En=rn*(y[5]+4*h*y[6]);Ec=w*y[7];Ep=-q*(KB*q*f['ncalc']/2+CBAR*f['Z']);shear=rg*y[lay.fg[2]]+rn*y[lay.fn[2]]
 other=math.fsum((Eg,En,Ec,Ep));force_terms=[-q*q*f['phi'],-Eb,-other,-2*shear];lens_terms=[-q*q*(f['phi']+f['psi'])/2,-Eb,-other,-shear]
 identities={}
 for name,terms in (('force',force_terms),('lens',lens_terms)):
  numerator=math.fsum(map(float,terms));residual=math.fsum((numerator,normal));scale=math.fsum(abs(float(v)) for v in terms)+abs(normal)
  identities[name]=dict(terms=terms,numerator=numerator,plus_normal=residual,absolute_term_sum=scale,error=abs(residual)/max(scale,q*q*CURVATURE*1e-10))
 ratios=dict(denominator=Eb,normal_over_denominator=normal/Eb if Eb else None)
 if Eb:
  ref=-Eb/q**2;ratios.update(force_metric=.99*f['phi']/ref,lens_metric=.99*(f['phi']+f['psi'])/(2*ref),force_source=.99*(1+(other+2*shear)/Eb),lens_source=.99*(1+(other+shear)/Eb),refusal=None)
 else:ratios.update(force_metric=None,lens_metric=None,force_source=None,lens_source=None,refusal='ZERO_SIGNED_BARYON_DENOMINATOR')
 bg=f['bg'];ss=bg['s'];qb=bg['qbar'];eps=fixed['eps'];lower=eps*ss/((1+ss)*(qb+1)*qb);upper=eps/((1+ss)*(math.sqrt(1+eps)+qb)*qb);gap=min(lower,upper)
 phase_fraction=abs(f['c']*raw[7])/gap;pi=y[8]-f['v']
 amplitude=max(abs(f['psi']),abs(f['phi']),abs(raw[1]),abs(raw[3]),abs(raw[5]),abs(raw[7]),abs(q*raw[2]),abs(q*raw[4]),abs(q*raw[6]),abs(q*y[8]),abs(q*pi))
 heads=dict(lower_gap=lower,upper_gap=upper,phase_rate=f['c']*raw[7],phase_rate_fraction=phase_fraction,phase_velocity=q*y[8],U_tilt=q*pi,relative_velocity=q*f['v'],phase_square_over_gap=(q*y[8])**2/(2*gap),relative_square_over_gap=(q*f['v'])**2/(2*gap),maximum_linear_amplitude=amplitude,sampled_absolute_curvature_ceiling=min(.01*CURVATURE/amplitude if amplitude else 1.,CURVATURE/phase_fraction if phase_fraction else 1.),inside_sampled_linear_domain=bool(amplitude<.01 and phase_fraction<1))
 case.update(x=x,background=bg,thermal=f['thermal'],Q=f['Q'],reaction_denominator=f['Delta'],P=KB*q*f['ncalc']/2+CBAR*f['Z'],Z=f['Z'],Zd=f['Zd'],pi_U=pi,signed_sources=dict(baryon=Eb,photon=Eg,neutrino=En,phase=Ec,polarization=Ep,shear=shear),source_ratios=ratios,source_numerator_identities=identities,domain_heads=heads)
 return case

def raw_derivatives_corrected(y,dy,f,lay):
 out=np.array(dy,copy=True);h=f['h'];V=y[8];hd=f['bg']['h_dt'];c=f['c'];Gamma=y[7]
 out[0]=dy[0]-hd*V-h*dy[8];out[1]=dy[1]-3*(hd*V+h*dy[8]);out[2]=dy[8]+f['g']*y[4]/f['rb']-c*Gamma
 out[3]=dy[3]-4*(hd*V+h*dy[8]);out[4]=dy[8]+h*f['wg']+y[3]/4-y[lay.fg[2]]/2-f['g']*y[4]-c*Gamma
 out[5]=dy[5]-4*(hd*V+h*dy[8]);out[6]=dy[8]+dy[6];out[7]=dy[7]-3*(hd*V+h*dy[8])
 return out

def trace_source(y,f):
 # M=Psi_dot+h*Phi. M_dot+3hM=F_tau; J=a^3 M obeys J_x=a^3 F_tau/h.
 phase_pressure=f['c']*f['w']*(y[7]-3*f['h']*y[8])
 radiation_pressure=(f['rg']*(y[3]-4*f['h']*y[8])+f['rn']*(y[5]-4*f['h']*y[8]))/3
 terms=[-f['bg']['h_dt']*f['phi'],-f['q']**2*(f['psi']-f['phi'])/3,phase_pressure,radiation_pressure]
 return math.fsum(map(float,terms))/f['h'],terms

def incoming_packets(prepared,prefix,fixed,lay,therm,snodes,weights,helpers,env):
 fine=[np.array(v['stable_state'],float) for v in prepared['fine_preparation']]
 start=[np.array(v,float) for v in prefix['states']]
 assert [v['stable_state'] for v in prepared['fine_preparation']]==[v.tolist() for v in fine]
 bg=helpers['background'](math.log(AC),fixed)
 fine_moments=[env['stable_initial_multipoles'](y,lay,K*CP/(1000*fixed['Hunit']*AC),bg,fixed) for y in fine]
 fine_anchors=[[env['stable_anchor'](math.log(AC),0.,y,fixed,lay,therm,snodes,weights,om,helpers)] for y,om in zip(fine,OMEGAS)]
 return dict(FINE=dict(states=fine,anchors=fine_anchors,moments=fine_moments,eta_origin=0.,eta_common=0.,prefix_steps=0),START=dict(states=start,anchors=prefix['anchors'],moments=prefix['moments'],eta_origin=prefix['eta'][0],eta_common=prefix['eta'][-1],prefix_steps=128))

def validate_payload(cp,commit,lineage,label,step,xs,eta,initial,created):
 keys={'lineage','owner','pid','group','nstep','xs','eta','incoming_binding','states','anchors','moments','snapshots','errors','trajectory_diagnostics','los_diagnostics','trace_integrals','trace_absolute_integrals','trace_initial_current','last_stages','optical_controls','initial_angular_errors','conformal_grid_error'}
 assert set(cp)==keys and cp['lineage']==lineage and cp['group']==label and cp['nstep']==step
 assert cp['owner']=='root' and type(cp['pid']) is int and cp['pid']>0
 name=STEM+'_'+label+'_CP_'+str(step).zfill(6)+'.json'
 assert commit==dict(lineage=lineage,owner='root',pid=cp['pid'],group=label,nstep=step,payload=name,sha256=sha(BASE/name))
 assert cp['xs']==xs.tolist() and cp['eta']==eta.tolist() and cp['incoming_binding']==initial['binding'] and cp['moments']==encode(initial['moments'])
 assert len(cp['states'])==len(cp['anchors'])==len(cp['errors'])==len(cp['trajectory_diagnostics'])==len(cp['los_diagnostics'])==len(cp['last_stages'])==4
 assert all(len(v)==84 for v in cp['states'])
 assert all(set(v)==set(ERROR_KEYS) and all(e>=0 for e in v.values()) for v in cp['errors'])
 assert len(cp['trace_integrals'])==len(cp['trace_absolute_integrals'])==len(cp['trace_initial_current'])==4 and all(v>=0 for v in cp['trace_absolute_integrals'])
 assert set(cp['optical_controls'])==set(initial['optical_names']) and all(v>=0 for v in cp['optical_controls'].values())
 assert [v['nstep'] for v in cp['snapshots']]==list(range(0,step+1,FRAME_STRIDE))
 for frame in cp['snapshots']:
  assert set(frame)=={'nstep','cases'} and len(frame['cases'])==4
  assert all(v['x']==xs[frame['nstep']] and len(v['stable_state'])==84 and len(v['readouts'])==15 for v in frame['cases'])
 for arm,history in enumerate(cp['anchors']):
  prefix=initial['anchors'][arm];assert len(history)==len(prefix)+step and history[:len(prefix)]==encode(prefix)
  for j,row in enumerate(history[len(prefix):],1):
   assert set(row)==ANCHOR_KEYS|{'panel_nodes','panel_envelopes'} and row['x']==xs[j] and row['eta']==eta[j]
   pp=row['panel_nodes'];assert len(pp)==4 and len(row['panel_envelopes'])==3 and all(v>=0 for v in row['panel_envelopes'])
   assert all(set(p)==ANCHOR_KEYS for p in pp) and all(pp[k]['x']<pp[k+1]['x'] and pp[k]['eta']<pp[k+1]['eta'] for k in range(3))
   prior=history[len(prefix)+j-2];assert pp[0]=={k:v for k,v in prior.items() if k in ANCHOR_KEYS} and pp[-1]=={k:v for k,v in row.items() if k in ANCHOR_KEYS}
  assert set(cp['trajectory_diagnostics'][arm])==set(INCREMENT_KEYS)
  for key,row in cp['trajectory_diagnostics'][arm].items():assert set(row)=={'maximum','location'} and row['maximum']==cp['errors'][arm][key]
  assert set(cp['los_diagnostics'][arm])==set(initial['los_names'])
  for row in cp['los_diagnostics'][arm].values():assert set(row)=={'maximum','location'} and row['maximum']>=0
  st=cp['last_stages'][arm]
  if step:
   assert set(st)=={'x','dx','coordinates','conformal','previous','states','algebraic_states','stage_error','dense_error'}
   assert len(st['states'])==len(st['coordinates'])==len(st['conformal'])==len(st['algebraic_states'])==3
   assert all(len(v)==84 for v in st['states']) and all(len(v)==2 for v in st['algebraic_states']) and len(st['previous'])==84
   assert st['states'][-1]==cp['states'][arm] and st['coordinates'][-1]==xs[step] and st['conformal'][-1]==eta[step]
  else:assert st is None and cp['states'][arm]==encode(initial['states'][arm])
 assert [v['stable_state'] for v in cp['snapshots'][-1]['cases']]==cp['states']
 for n in (name,name[:-5]+'_COMMIT.json'):created[n]=sha(BASE/n)

def run_group(label,initial,fixed,lay,therm,snodes,weights,helpers,env,lineage,authenticate,created):
 xs=np.linspace(math.log(AC),math.log(AF),NSTEP+1);optical=env['CubicKernel'](fixed,therm)
 eta=[initial['eta_common']];check_eta=[initial['eta_common']]
 for lo,hi in zip(xs[:-1],xs[1:]):
  eta.append(eta[-1]+float(optical.integral(float(lo),float(hi),16)[1]));check_eta.append(check_eta[-1]+float(optical.integral(float(lo),float(hi),32)[1]))
 eta=np.array(eta);conformal_error=float(np.max(abs(eta-np.array(check_eta)))/max(float(eta[-1]-eta[0]),1e-30))
 initial['binding']=dict(parent_preparation_sha256=PINS[SHORT+'_PREPARATION_CP.json'],parent_prefix_sha256=PINS[SHORT+'_N128_CP_000128.json'],group=label,eta_origin=initial['eta_origin'],eta_common=initial['eta_common'],prefix_steps=initial['prefix_steps'])
 initial['optical_names']=list(optical.maximum);initial['los_names']=['delta_gamma','Hstar_u_gamma','delta_nu','Hstar_u_nu','F_gamma_2','F_nu_2','G_gamma_0','G_gamma_2']
 c1=.5-math.sqrt(3)/6;c2=.5+math.sqrt(3)/6;targets=[]
 for i in range(1,NSTEP+1):
  lo=float(xs[i-1]);dx=float(xs[i]-xs[i-1]);xx=(lo+c1*dx,lo+c2*dx,float(xs[i]))
  targets.append([eta[i-1]+float(optical.integral(lo,xj,16)[1]) if j<2 else float(eta[i]) for j,xj in enumerate(xx)])
 phases=K*(np.array(targets)-initial['eta_origin']);transported=[];angular_errors=[]
 for moments in initial['moments']:
  transported.append({kind:np.array([env['initial_transport'](coeff,phases,l).real for l in range(5)]) for kind,coeff in moments.items()})
  angular_errors.append({kind:float(np.max(abs(transported[-1][kind]-np.array([env['initial_transport'](coeff,phases,l,256).real for l in range(5)]))))/CURVATURE for kind,coeff in moments.items()})
 states=[y.copy() for y in initial['states']];anchors=json.loads(json.dumps(encode(initial['anchors'])))
 errors=[{k:0. for k in ERROR_KEYS} for _ in OMEGAS];trajectory=[{k:dict(maximum=0.,location=None) for k in INCREMENT_KEYS} for _ in OMEGAS]
 los=[{k:dict(maximum=0.,location=None) for k in initial['los_names']} for _ in OMEGAS];last_stages=[None]*4
 snapshots=[dict(nstep=0,cases=[full_snapshot(float(xs[0]),y,fixed,lay,therm,snodes,weights,om,helpers,env) for y,om in zip(states,OMEGAS)])]
 trace_initial=[math.exp(3*float(xs[0]))*env['chart_coefficients'](float(xs[0]),y,fixed,lay,therm,snodes,weights,om,helpers)['mom'] for y,om in zip(states,OMEGAS)]
 trace_integrals=[0.]*4;trace_absolute=[0.]*4
 commits=sorted(BASE.glob(STEM+'_'+label+'_CP_*_COMMIT.json'));payloads=[p for p in BASE.glob(STEM+'_'+label+'_CP_*.json') if not p.name.endswith('_COMMIT.json')]
 assert len(commits)==len(payloads),'Preserved orphan checkpoint requires explicit recovery'
 expected=list(range(0,NSTEP+1,CP_STRIDE));seen=[];prior=None
 for path in commits:
  commit=json.loads(path.read_text());cp=json.loads((BASE/commit['payload']).read_text());env['finite_tree'](cp);env['finite_tree'](commit)
  step=cp['nstep'];validate_payload(cp,commit,lineage,label,step,xs,eta,initial,created);seen.append(step)
  assert cp['initial_angular_errors']==encode(angular_errors) and cp['conformal_grid_error']==conformal_error and cp['trace_initial_current']==trace_initial
  if prior:
   assert cp['snapshots'][:len(prior['snapshots'])]==prior['snapshots'] and all(cp['anchors'][a][:len(prior['anchors'][a])]==prior['anchors'][a] for a in range(4))
   assert all(cp['errors'][a][k]>=prior['errors'][a][k] for a in range(4) for k in ERROR_KEYS)
   assert all(cp['trace_absolute_integrals'][a]>=prior['trace_absolute_integrals'][a] for a in range(4)) and all(cp['optical_controls'][k]>=prior['optical_controls'][k] for k in prior['optical_controls'])
  prior=cp
 assert seen==expected[:len(seen)]
 start=0
 if commits:
  start=cp['nstep'];states=[np.array(v,float) for v in cp['states']];anchors=cp['anchors'];snapshots=cp['snapshots'];errors=cp['errors'];trajectory=cp['trajectory_diagnostics'];los=cp['los_diagnostics'];last_stages=cp['last_stages'];trace_integrals=cp['trace_integrals'];trace_absolute=cp['trace_absolute_integrals'];optical.maximum=cp['optical_controls']
 def checkpoint(i):
  authenticate();name=STEM+'_'+label+'_CP_'+str(i).zfill(6)+'.json'
  payload=dict(lineage=lineage,owner='root',pid=os.getpid(),group=label,nstep=i,xs=xs,eta=eta,incoming_binding=initial['binding'],states=states,anchors=anchors,moments=initial['moments'],snapshots=snapshots,errors=errors,trajectory_diagnostics=trajectory,los_diagnostics=los,trace_integrals=trace_integrals,trace_absolute_integrals=trace_absolute,trace_initial_current=trace_initial,last_stages=last_stages,optical_controls=optical.maximum,initial_angular_errors=angular_errors,conformal_grid_error=conformal_error)
  ch=write(name,payload);cn=name[:-5]+'_COMMIT.json';write(cn,dict(lineage=lineage,owner='root',pid=os.getpid(),group=label,nstep=i,payload=name,sha256=ch));created[name]=ch;created[cn]=sha(BASE/cn)
  sealed=json.loads((BASE/name).read_text());sealed_commit=json.loads((BASE/cn).read_text());env['finite_tree'](sealed);env['finite_tree'](sealed_commit);validate_payload(sealed,sealed_commit,lineage,label,i,xs,eta,initial,created)
  authenticate();print('FULL_COMMON',label,i,'/',NSTEP,flush=True)
 if not commits:checkpoint(0)
 for i in range(start+1,NSTEP+1):
  lo=float(xs[i-1]);dx=float(xs[i]-xs[i-1]);xx=(lo+c1*dx,lo+c2*dx,float(xs[i]));optical.weight_cache.clear();next_states=[]
  for arm,om in enumerate(OMEGAS):
   iv=[{kind:arr[:,i-1,j] for kind,arr in transported[arm].items()} for j in range(3)]
   stage,err,final,record=env['coupled_gauss'](states[arm],lo,dx,targets[i-1],anchors[arm],fixed,lay,therm,snodes,weights,om,helpers,iv,optical,dense=i%CP_STRIDE==0)
   previous=states[arm];before=env['chart_coefficients'](lo,previous,fixed,lay,therm,snodes,weights,om,helpers)
   stage_dy=[];fs=[];raw_rates=[];raws=[]
   for xj,yj in zip(xx,stage):
    dy,f=env['chart_rates'](xj,yj,fixed,lay,therm,snodes,weights,om,helpers);stage_dy.append(dy);fs.append(f);raw_rates.append(raw_derivatives_corrected(yj,dy,f,lay)/f['h']);raws.append(env['to_raw'](yj,f['bg'],fixed))
   after=fs[-1];end=stage[-1];raw_before=env['to_raw'](previous,before['bg'],fixed)
   tests={
    'metric_momentum_error':(after['psi']-before['psi'],[f['mom']/f['h']-f['phi'] for f in fs[:2]],abs(after['psi'])+abs(before['psi'])),
    'curvature_increment_error':(end[0]-previous[0],[f['Rd']/f['h'] for f in fs[:2]],abs(end[0])+abs(previous[0])),
    'baryon_Euler_error':((end[8]+after['wb'])-(previous[8]+before['wb']),[(f['phi']+f['g']*stage[j][4]/f['rb'])/f['h'] for j,f in enumerate(fs[:2])],abs(end[8]+after['wb'])+abs(previous[8]+before['wb']))}
   trace_forces=[];trace_terms=[]
   for xj,yj,f in zip(xx[:2],stage[:2],fs[:2]):
    source,terms=trace_source(yj,f);trace_forces.append(math.exp(3*xj)*source);trace_terms.append(terms)
   current0=math.exp(3*lo)*before['mom'];current1=math.exp(3*xx[-1])*after['mom']
   tests['conservative_trace_increment_error']=(current1-current0,trace_forces,abs(current1)+abs(current0))
   contribution=dx*math.fsum(trace_forces)/2;trace_integrals[arm]=math.fsum((trace_integrals[arm],contribution));trace_absolute[arm]+=abs(dx)*math.fsum(abs(v) for v in trace_forces)/2
   for key,(delta,forces,scale0) in tests.items():
    integral=dx*math.fsum(map(float,forces))/2;residual=delta-integral;scale=scale0+abs(dx)*math.fsum(abs(float(v)) for v in forces)/2
    floor=CURVATURE*AC**3*1e-18 if key=='conservative_trace_increment_error' else CURVATURE*1e-18
    err[key]=abs(residual)/max(scale,floor)
    if err[key]>trajectory[arm][key]['maximum']:trajectory[arm][key]=dict(maximum=err[key],location=dict(nstep=i,a=math.exp(xx[-1]),delta=delta,gauss_integral=integral,residual=residual,scale=scale,forces=forces,log_step=dx,proper_trace_source_terms=trace_terms if key=='conservative_trace_increment_error' else None))
   wr=math.fsum((current1,-trace_initial[arm],-trace_integrals[arm]));ws=abs(current1)+abs(trace_initial[arm])+trace_absolute[arm]
   err['conservative_trace_window_error']=abs(wr)/max(ws,CURVATURE*AC**3*1e-18)
   if err['conservative_trace_window_error']>trajectory[arm]['conservative_trace_window_error']['maximum']:trajectory[arm]['conservative_trace_window_error']=dict(maximum=err['conservative_trace_window_error'],location=dict(nstep=i,a=math.exp(xx[-1]),current=current1,initial_current=trace_initial[arm],gauss_integral=trace_integrals[arm],residual=wr,scale=ws))
   indices=[3,4,5,6,lay.fg[2],lay.fn[2],lay.pol[0],lay.pol[2]];delta=raws[-1][indices]-raw_before[indices];forces=(raw_rates[0][indices]+raw_rates[1][indices])/2;residual=delta-dx*forces
   scale=abs(raws[-1][indices])+abs(raw_before[indices])+abs(dx)*(abs(raw_rates[0][indices])+abs(raw_rates[1][indices]))/2;row_errors=abs(residual)/np.maximum(scale,CURVATURE*1e-12);err['los_continuity_error']=float(np.max(row_errors))
   for j,name in enumerate(initial['los_names']):
    if row_errors[j]>los[arm][name]['maximum']:los[arm][name]=dict(maximum=float(row_errors[j]),location=dict(nstep=i,a=math.exp(xx[-1]),residual=float(residual[j]),scale=float(scale[j]),old_state=float(raw_before[indices[j]]),new_state=float(raws[-1][indices[j]]),gauss_stage_rates=[float(raw_rates[t][indices[j]]) for t in range(2)],log_step=dx))
   for key in ERROR_KEYS:errors[arm][key]=max(errors[arm][key],float(err[key]))
   next_states.append(end);anchors[arm].append(final);last_stages[arm]=record
  states=next_states
  if i%FRAME_STRIDE==0:snapshots.append(dict(nstep=i,cases=[full_snapshot(float(xs[i]),y,fixed,lay,therm,snodes,weights,om,helpers,env) for y,om in zip(states,OMEGAS)]))
  if i%CP_STRIDE==0:checkpoint(i)
 return dict(group=label,common_grid=xs,snapshots=snapshots,errors=errors,trajectory_diagnostics=trajectory,los_diagnostics=los,optical_controls=optical.maximum,initial_angular_errors=angular_errors,conformal_grid_error=conformal_error,endpoint_phase=K*float(eta[-1]-initial['eta_origin']),incoming_binding=initial['binding'],trace_initial_current=trace_initial,trace_final_current=[math.exp(3*xs[-1])*env['chart_coefficients'](float(xs[-1]),y,fixed,lay,therm,snodes,weights,om,helpers)['mom'] for y,om in zip(states,OMEGAS)],trace_integrals=trace_integrals,trace_absolute_integrals=trace_absolute)
def main(resume):
 assert PROTOCOL_SHA!='PENDING' and PINS[STEM+'.md']==PROTOCOL_SHA
 source_sha=sha(__file__);started=datetime.now(timezone.utc).isoformat();tick=time.monotonic();created={}
 assert not any((BASE/(STEM+s)).exists() for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json'))
 assert not list(BASE.glob(STEM+'_FAILED*')),'A preserved failed attempt requires a new namespace'
 mp=BASE/(STEM+'_MANIFEST.json');cp_paths=list(BASE.glob(STEM+'_*_CP_*.json'))
 if not resume:assert not mp.exists() and not cp_paths,'Explicit --resume required for same-lineage recovery'
 if not mp.exists():assert not cp_paths,'Preserved pre-manifest checkpoint orphan'
 def authenticate():
  assert sha(__file__)==source_sha and not Path(__file__).stat().st_mode&0o222
  for p,h in PINS.items():assert sha(BASE/p)==h and not (BASE/p).stat().st_mode&0o222,p
  for p,h in created.items():assert sha(BASE/p)==h and not (BASE/p).stat().st_mode&0o222,p
 authenticate()
 short=json.loads((BASE/(SHORT+'_RESULT.json')).read_text());receipt=json.loads((BASE/(SHORT+'_RECEIPT.json')).read_text());parent_manifest=json.loads((BASE/(SHORT+'_MANIFEST.json')).read_text())
 assert short['status']=='SHORT_DERIVED_START_DIAGNOSTIC_PASS' and short['all_short_diagnostic_gates_passed'] is True
 assert len(short['diagnostic_gates'])==216 and all(v['passed'] for v in short['diagnostic_gates'])
 assert short['owner']==receipt['owner']=='root' and short['pid']==receipt['pid']
 assert short['source_sha256']==receipt['source_sha256']==parent_manifest['source_sha256']==PINS['constrained_u_k10_derived_start_overlap_v001.py']
 assert short['input_sha256']==receipt['input_sha256']==parent_manifest['input_sha256'] and all(PINS[k]==v for k,v in short['input_sha256'].items())
 assert receipt['result_sha256']==PINS[SHORT+'_RESULT.json'] and receipt['report_sha256']==PINS[SHORT+'_REPORT.md']
 assert len(receipt['output_sha256'])==15 and all(PINS[k]==v for k,v in receipt['output_sha256'].items())
 assert short['original_failure_flags_changed'] is short['physical_seed_qualified'] is short['full_33_frame_start_criterion_qualified'] is False
 prepared=json.loads((BASE/(SHORT+'_PREPARATION_CP.json')).read_text());prep_commit=json.loads((BASE/(SHORT+'_PREPARATION_CP_COMMIT.json')).read_text())
 prefix=json.loads((BASE/(SHORT+'_N128_CP_000128.json')).read_text());prefix_commit=json.loads((BASE/(SHORT+'_N128_CP_000128_COMMIT.json')).read_text())
 assert prepared['lineage']==prefix['lineage']==parent_manifest and prepared['fine_preparation']==short['fine_preparation'] and prepared['start_preparation']==short['start_preparation'] and prepared['seeds']==prefix['seeds']==short['seeds']
 assert prepared['owner']==prefix['owner']=='root' and prepared['pid']==prefix['pid']==short['pid'] and prefix['n']==prefix['nstep']==128
 assert prep_commit==dict(lineage=parent_manifest,owner='root',pid=prepared['pid'],payload=SHORT+'_PREPARATION_CP.json',sha256=PINS[SHORT+'_PREPARATION_CP.json'])
 assert prefix_commit==dict(lineage=parent_manifest,owner='root',pid=prefix['pid'],n=128,nstep=128,payload=SHORT+'_N128_CP_000128.json',sha256=PINS[SHORT+'_N128_CP_000128.json'])
 assert prefix['states']==[v['stable_state'] for v in short['propagations'][1]['endpoint']] and prefix['xs'][-1]==math.log(AC)
 assert all(len(v)==129 and v[-1]['x']==prefix['xs'][-1] and v[-1]['eta']==prefix['eta'][-1] for v in prefix['anchors'])
 original=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());old_start=next(v for v in original['comparisons'] if v['label']=='start')
 assert original['status']=='COUPLED_HORIZON_ARITHMETIC_FAILED' and original['all_numerical_gates_passed'] is False
 assert len(original['numerical_gates'])==670 and sum(v['passed'] for v in original['numerical_gates'])==618 and len(original['optical_map_controls'])==36 and all(v['passed'] for v in original['optical_map_controls'])
 fixed=parent_manifest['fixed'];assert fixed==json.loads((BASE/(PARENT+'_MANIFEST.json')).read_text())['fixed']
 lineage=encode(dict(source_sha256=source_sha,input_sha256=PINS,fixed=fixed,groups=GROUPS,common_ai=AC,af=AF,nstep=NSTEP,frame_stride=FRAME_STRIDE,checkpoint_stride=CP_STRIDE,omega=OMEGAS,ns=32,numpy_version=np.__version__,method='Same simultaneous stable-Y cubic Gauss memory, complete saved prefix; corrected baryon diagnostic and integrating-factor proper trace',gate_count=252))
 if mp.exists():assert json.loads(mp.read_text())==lineage
 else:write(mp.name,lineage)
 created[mp.name]=sha(mp)
 expected=[STEM+'_'+label+'_CP_'+str(i).zfill(6)+'.json' for label in GROUPS for i in range(0,NSTEP+1,CP_STRIDE)]
 actual=[p.name for p in sorted(BASE.glob(STEM+'_*_CP_*.json')) if not p.name.endswith('_COMMIT.json')]
 own_order=[n for n in expected if n in actual];assert actual==sorted(own_order) and own_order==expected[:len(own_order)],'Global exact group/step prefix'
 env=load_definitions();helpers=env['load_declared_helpers']();lay=helpers['Layout'](32,4,4);therm=helpers['Thermal']('HALF',1,fixed)
 for v in (short,prepared,prefix,lineage):env['finite_tree'](v)
 nodes,weight=env['gauss'](32);snodes=(nodes+1)/2;weights=weight*snodes;weights/=sum(weights)
 incoming=incoming_packets(prepared,prefix,fixed,lay,therm,snodes,weights,helpers,env)
 rows=[run_group(label,incoming[label],fixed,lay,therm,snodes,weights,helpers,env,lineage,authenticate,created) for label in GROUPS]
 fine,start=rows;assert len(fine['snapshots'])==len(start['snapshots'])==33 and fine['common_grid'].tolist()==start['common_grid'].tolist()
 original_fine=next(v for v in original['rows'] if v['label']=='FINE')
 assert [s['nstep'] for s in fine['snapshots']]==[s['nstep'] for s in original_fine['snapshots']]
 assert all([v['a'] for v in f['cases']]==[v['a'] for v in old['cases']] for f,old in zip(fine['snapshots'],original_fine['snapshots']))
 values_f=np.array([[c['readouts'] for c in s['cases']] for s in fine['snapshots']]);values_s=np.array([[c['readouts'] for c in s['cases']] for s in start['snapshots']])
 den=np.maximum(np.max(abs(values_f),axis=0),CURVATURE*1e-8);difference=values_s-values_f;maximum=np.max(abs(difference),axis=0);error=maximum/den
 oldden=np.array(old_start['normalization']);names=original['readout_names'];assert len(names)==15 and oldden.shape==den.shape==(4,15)
 comparison=dict(label='start',tolerance=2e-4,signed_frame_differences=difference,first_original_peak_frame=np.argmax(abs(difference),axis=0),signed_endpoint_difference=difference[-1],maximum_absolute_difference=maximum,normalization=den,normalized_error=error,old_normalization_auxiliary=oldden,error_using_old_normalization_auxiliary=maximum/oldden,normalization_scope='Unchanged functional maximum over the new FINE full33 common frames, same curvature-times1e-8 floor; old denominator auxiliary only')
 gates=[]
 def check(label,error,tol,**fields):
  error=float(error);gates.append(dict(label=label,error=error,tolerance=tol,passed=bool(math.isfinite(error) and error<=tol),**fields))
 for row in rows:
  label=row['group'];check('conformal_grid',row['conformal_grid_error'],2e-11,group=label);check('bounded_horizon_kernel_range',max(0.,row['endpoint_phase']-8),0.,group=label)
  for arm in range(4):
   first=row['snapshots'][0]['cases'][arm]
   for key,tol in (('normal_error',1e-10),('shear_error',2e-13),('native_Euler_error',1e-9),('proper_trace_error',1e-9)):check('initial_'+key,first[key],tol,group=label,arm=arm)
   for kind in ('nu','photon','polarization'):check('initial_angular_'+kind,row['initial_angular_errors'][arm][kind],2e-11,group=label,arm=arm)
   for key in ('stage_error','dense_error'):check(key,row['errors'][arm][key],2e-11,group=label,arm=arm)
   for key in INCREMENT_KEYS:check(key,row['errors'][arm][key],1e-5,group=label,arm=arm)
   check('los_continuity_error',row['errors'][arm]['los_continuity_error'],1e-3,group=label,arm=arm)
   check('discarded_radiation_source_absolute',row['errors'][arm]['discarded_source_bound']/CURVATURE,1e-12,group=label,arm=arm)
   for key,tol in (('normal_error',1e-10),('shear_error',2e-13),('native_Euler_error',1e-9),('proper_trace_error',1e-9)):check('sampled_'+key,max(s['cases'][arm][key] for s in row['snapshots']),tol,group=label,arm=arm)
   for name in ('force','lens'):check('source_'+name+'_numerator_identity',max(s['cases'][arm]['source_numerator_identities'][name]['error'] for s in row['snapshots']),2e-11,group=label,arm=arm)
  for name,e in row['optical_controls'].items():check(name,e,2e-11,group=label)
 for arm in range(4):
  for variable,name in enumerate(names):check('start_refinement',error[arm,variable],2e-4,arm=arm,variable=name)
 assert len(gates)==252 and len(created)==69
 qualified=all(v['passed'] for v in gates)
 result=dict(status='DERIVED_FULL_COMMON_DIAGNOSTIC_PASS' if qualified else 'DERIVED_FULL_COMMON_DIAGNOSTIC_FAILED',all_new_diagnostic_gates_passed=qualified,new_diagnostic_gates=gates,new_gate_count=252,owner='root',pid=os.getpid(),started=started,ended=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick,source_sha256=source_sha,input_sha256=PINS,lineage=lineage,rows=rows,readout_names=names,start_comparison=comparison,full33_start_diagnostic_passed=bool(np.all(error<=2e-4)),preserved_short_gates=short['diagnostic_gates'],preserved_parent_gates=original['numerical_gates'],preserved_parent_optical_controls=original['optical_map_controls'],parent52_failed_flags_changed=False,no_prefix_rerun=True,no_boundary_projection=True,physical_seed_qualified=False,physical_fluid_or_origin_qualified=False,full_new_suite_scope='Two fixed preparations on original common grid; no new time/mode/source refinement suite, finite Cauchy remainder or microscopic preparation dictionary')
 authenticate();rh=write(STEM+'_RESULT.json',result);created[STEM+'_RESULT.json']=rh
 report=BASE/(STEM+'_REPORT.md')
 text='# Derived full common continuation V001\n\n'+result['status']+'\n\n'+str(sum(v['passed'] for v in gates))+'/252 new diagnostic checks. Two unchanged preparations, four inertias, original2048-step common log grid and33frames. Complete saved START prefix/history carried without re-evaluation or boundary modification. Corrected positive baryon drag and conservative J=a³M proper trace are separate new diagnostics. Original618/670 plus36/36 and all52 failures remain copied unchanged; all physical preparation/origin flags remain false.\n'
 with report.open('x') as f:f.write(text)
 report.chmod(0o444);created[report.name]=sha(report);authenticate()
 cp_outputs={k:v for k,v in created.items() if k not in (STEM+'_RESULT.json',report.name)}
 write(STEM+'_RECEIPT.json',dict(owner='root',pid=os.getpid(),closed=datetime.now(timezone.utc).isoformat(),source_sha256=source_sha,input_sha256=PINS,output_sha256=cp_outputs,checkpoint_count=34,result_sha256=rh,report_sha256=sha(report),status=result['status']))
 authenticate();print(json.dumps(dict(status=result['status'],result_sha256=rh,receipt_sha256=sha(BASE/(STEM+'_RECEIPT.json')))),flush=True)
 return 0 if qualified else 3
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root-owned',action='store_true',required=True);p.add_argument('--resume',action='store_true');args=p.parse_args()
 if 'AUTHOR_DRAFT' in Path(__file__).name:raise SystemExit('Protected author draft; not a numerical entry point')
 try:raise SystemExit(main(args.resume))
 except Exception:
  write(STEM+'_FAILED_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'.json',dict(owner='root',pid=os.getpid(),traceback=traceback.format_exc()))
  raise
