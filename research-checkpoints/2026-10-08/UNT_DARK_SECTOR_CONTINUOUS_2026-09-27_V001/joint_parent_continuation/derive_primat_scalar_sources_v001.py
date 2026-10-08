"""Inert exact-anchor source derivation; stdout only, no import/build/run/write.

ROOT publishes the returned sources and command manifest after full review.
All original PRIMAT and qualified ordinary bytes remain untouched.
"""
import base64
import difflib
import hashlib
import json
from pathlib import Path

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
B=J/'bbn_inputs_v001/primat_c_reference_v001'
D=B/'derived_scalar_v001'
BUILD=B/'build_scalar_v001'
PINS={
 'upstream/primat-c/include/background.h':'5ced6cd5d02393f4f1b2b9a250a6709f64f1ac823394098d3419504b89ee5eae',
 'upstream/primat-c/src/background.c':'d692a9c810d65b2711ebe7aa246c317c0284428305463c0534bf742b8f675064',
 'derived_ordinary_v001/unt_primat_ordinary_v001.c':'3021c54cf72e990875f763f7f44d597d05c202674ad13c9e2b152c343fdafc7a',
 'PRIMAT_ORDINARY_BUILD_MANIFEST_V001.json':'7df47e6d272a326d56b1067f75d59f18e5a9f8b0f0104e1856275c8737e27f90'}

def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(rel):
 p=B/rel
 if p.resolve()!=p or not p.is_file():raise RuntimeError('Nonregular/symlink input')
 raw=p.read_bytes()
 if sha(raw)!=PINS[rel]:raise RuntimeError('Changed source '+rel)
 return raw.decode('utf-8')
def once(s,a,b):
 if s.count(a)!=1:raise RuntimeError('Exact anchor not unique: '+a[:100])
 return s.replace(a,b,1)

HEADER=r'''
/* UNT owned scalar branch. Units MeV^4, MeV and seconds. Context borrowed. */
typedef struct {
    double rho_em, rho_nu, rho_b, rho_h, p_h, rho_lambda, H;
    int provider_used;
    unt_hard_state material;
} CPRScalarComponents;
int cpr_bg_owned_components(const CPRBackground *, double, double, double,
                            double, double, CPRScalarComponents *, char *, size_t);
int cpr_bg_Hubble_checked(const CPRBackground *, double, double, double,
                          double, double, double *, char *, size_t);
int cpr_bg_init_owned(CPRBackground *, const CPRConfig *, const CPRPlasma *,
                      const unt_hard_context *, int, char **);
'''

COMPONENTS=r'''
/* The same selected ordinary thermal functions; no temperature-proxy scalar. */
int cpr_bg_owned_components(const CPRBackground *bg, double T, double Te,
                            double Tmu, double Ttau, double a,
                            CPRScalarComponents *out, char *error, size_t nerror)
{
    memset(out,0,sizeof(*out));
    if (!(isfinite(T)&&T>0&&isfinite(Te)&&Te>0&&isfinite(Tmu)&&Tmu>0
          &&isfinite(Ttau)&&Ttau>0&&isfinite(a)&&a>=1e-16&&a<=1.)) {
        snprintf(error,nerror,"owned H: finite positive T/a in fixed[1e-16,1] required"); return 1;
    }
    const CPRConfig *cfg=bg->cfg;
    out->rho_em=cpr_rho_g(T)+cpr_plasma_rho_e(bg->plasma,T)
                    -bg_PQEDofT(bg->plasma,T)+T*bg_dPQEDdT(bg->plasma,T);
    out->rho_nu=cpr_rho_nu(Te)+cpr_rho_nu(Tmu)+cpr_rho_nu(Ttau);
    out->rho_lambda=bg->rholambda;
    out->rho_b=bg->owned_baryon_rest ? cpr_config_get_Omegabh2(cfg)*cpr_config_rhocOverh2(cfg)/(a*a*a):0.;
    if(bg->owned_hard) {
        if(unt_hard_eval(bg->owned_hard,a,&out->material,error,nerror))return 1;
        out->provider_used=1;out->rho_h=out->material.rho;out->p_h=out->material.pressure;
    } else out->rho_h=bg->rhocdm_a3/(a*a*a);
    double total=out->rho_em+out->rho_nu+out->rho_b+out->rho_h+out->rho_lambda;
    if(!(isfinite(out->rho_em)&&out->rho_em>0&&isfinite(out->rho_nu)&&out->rho_nu>0
         &&isfinite(out->rho_b)&&out->rho_b>=0&&isfinite(out->rho_h)&&out->rho_h>0
         &&isfinite(out->p_h)&&out->p_h>=0&&isfinite(out->rho_lambda)&&out->rho_lambda>=0
         &&isfinite(total)&&total>0)) {
        snprintf(error,nerror,"owned H: invalid component/total density");return 1;
    }
    out->H=cpr_MeV_to_secm1()*sqrt(total*8.*M_PI/(3.*cpr_config_Mpl(cfg)*cpr_config_Mpl(cfg)));
    if(!(isfinite(out->H)&&out->H>0)) {snprintf(error,nerror,"owned H: invalid H");return 1;}
    return 0;
}
'''

CHECKED=r'''
int cpr_bg_Hubble_checked(const CPRBackground *bg,double T,double Te,double Tmu,
                          double Ttau,double a,double *out,char *error,size_t nerror)
{
    if(bg->owned_hard) {
        CPRScalarComponents c;
        if(cpr_bg_owned_components(bg,T,Te,Tmu,Ttau,a,&c,error,nerror))return 1;
        *out=c.H;
    } else *out=cpr_bg_Hubble(bg,T,Te,Tmu,Ttau,a);
    if(!(isfinite(*out)&&*out>0)) {snprintf(error,nerror,"nonpositive/nonfinite H");return 1;}
    return 0;
}
'''

WRAPPERS=r'''
int cpr_bg_init_standard(CPRBackground *bg,const CPRConfig *cfg,const CPRPlasma *plasma,char **errmsg)
{ return cpr_bg_init_standard_impl(bg,cfg,plasma,NULL,0,errmsg); }
int cpr_bg_init_owned(CPRBackground *bg,const CPRConfig *cfg,const CPRPlasma *plasma,
                      const unt_hard_context *material,int baryon,char **errmsg)
{
    if(!material||!material->initialized||(baryon!=0&&baryon!=1)
       ||material->a_min!=1e-16||material->a_max!=1.
       ||cfg->custom_background||cfg->external_scale_factor||cfg->extra_rho_n
       ||cfg->DeltaNeff!=0||cfg->fEDE!=0||cpr_config_xi_nu_e(cfg)!=0
       ||cpr_config_xi_nu_mu(cfg)!=0||cpr_config_xi_nu_tau(cfg)!=0
       ||!cfg->incomplete_decoupling||!cfg->spectral_distortions) {
        *errmsg=strdup("owned branch: fixed finite domain and NEVO/no-extra-source configuration required");return 1;
    }
    double expected=cfg->Omegach2*cpr_config_rhocOverh2(cfg);
    if(!(expected>0&&isfinite(expected))||fabs(material->rho_1/expected-1)>2e-12) {
        *errmsg=strdup("owned branch: hard density normalization mismatch");return 1;
    }
    return cpr_bg_init_standard_impl(bg,cfg,plasma,material,baryon,errmsg);
}
'''

def header(s):
 s=once(s,'#include "config.h"','#include "unt_hard_barotrope_v001.h"\n#include "config.h"')
 s=once(s,'    CPRBackgroundKind kind;', '    const unt_hard_context *owned_hard; /* borrowed immutable; NULL legacy */\n    int owned_baryon_rest;\n    CPRBackgroundKind kind;')
 return once(s,'} CPRBackground;','} CPRBackground;\n'+HEADER)

def background(s):
 anchor='double cpr_bg_Hubble(const CPRBackground *bg, double Tg, double Tnue, double Tnumu,\n                      double Tnutau, double a)\n{'
 s=once(s,anchor,COMPONENTS+'\n'+anchor+r'''
    if(bg->owned_hard) {
        CPRScalarComponents components;char error[256];
        return cpr_bg_owned_components(bg,Tg,Tnue,Tnumu,Tnutau,a,&components,error,sizeof error) ? NAN : components.H;
    }
''')
 s=once(s,'static double dlnadlnT_value(',CHECKED+'\nstatic double dlnadlnT_value(')
 s=once(s,'typedef struct { CPRBackground *bg; } CombinedBgCtx;','typedef struct { CPRBackground *bg; char error[256]; } CombinedBgCtx;')
 s=once(s,'    double H = cpr_bg_Hubble(bg, T, Tnue, Tnumu, Tnutau, a);\n\n    /* trel:',r'''    double H;
    if(cpr_bg_Hubble_checked(bg,T,Tnue,Tnumu,Tnutau,a,&H,c->error,sizeof c->error)) return 1;
    if(!(isfinite(dlna_dlnT)&&dlna_dlnT<0)) {
        snprintf(c->error,sizeof c->error,"invalid fixed-NEVO entropy derivative");return 1;
    }

    /* trel:''')
 s=once(s,'            *errmsg = err;\n            return 1;\n        }\n        have_combined_path = 1;',r'''            if(ctx.error[0]) { free(err); *errmsg=strdup(ctx.error); }
            else *errmsg=err;
            return 1;
        }
        have_combined_path = 1;''')
 a='        double t_ini = 1.0 / (2.0 * cpr_bg_Hubble(bg, Tstartcosmo, Tnue_s, Tnumu_s, Tnutau_s, a_ini));'
 if s.count(a)!=2:raise RuntimeError('Endpoint anchor census')
 left,tail=s.rsplit(a,1)
 s=left+r'''        double H_ini; char H_error[256];
        if(cpr_bg_Hubble_checked(bg,Tstartcosmo,Tnue_s,Tnumu_s,Tnutau_s,a_ini,&H_ini,H_error,sizeof H_error)) {
            dense_path_free(&combined_path);free(T_sol);*errmsg=strdup(H_error);return 1;
        }
        double t_ini=1.0/(2.0*H_ini);'''+tail
 a='int cpr_bg_init_standard(CPRBackground *bg, const CPRConfig *cfg, const CPRPlasma *plasma,\n                          char **errmsg)'
 s=once(s,a,'static int cpr_bg_init_standard_impl(CPRBackground *bg, const CPRConfig *cfg, const CPRPlasma *plasma,\n                          const unt_hard_context *owned,int baryon,char **errmsg)')
 s=once(s,'    bg->kind = CPR_BG_STANDARD;','    bg->owned_hard=owned; bg->owned_baryon_rest=baryon;\n    bg->kind = CPR_BG_STANDARD;')
 a='/* ---------------------------------------------------------------------\n * CustomBackground.'
 return once(s,a,WRAPPERS+'\n'+a)

ADAPTER_HELPERS=r'''
static int numeric(const char *s,double *out) {
 char *end=NULL;*out=strtod(s,&end);return end!=s&&!*end&&isfinite(*out);
}
static int close_rel(double a,double b,double tol) {
 return isfinite(a)&&isfinite(b)&&fabs(a-b)<=tol*fmax(fabs(a),fabs(b));
}
static void component_row(const CPRBackground *bg,double T,double Te,double Tmu,double Ttau,double a) {
 CPRScalarComponents c;char error[256];
 int status=cpr_bg_owned_components(bg,T,Te,Tmu,Ttau,a,&c,error,sizeof error);
 test(status==0);
 if(status) { printf("null");return; }
 double nB=cpr_n0CMB(&bg->cfg->consts)*bg->cfg->eta0b/(a*a*a);
 double rhoBref=cpr_mB(&bg->cfg->consts)*nB;
 double rhoBcosmic=cpr_config_get_Omegabh2(bg->cfg)*cpr_config_rhocOverh2(bg->cfg)/(a*a*a);
 test(close_rel(rhoBref,rhoBcosmic,2e-12));
 double legacyH=cpr_bg_Hubble(bg,T,Te,Tmu,Ttau,a);
 test(close_rel(legacyH,c.H,2e-12));
 putchar('[');num(c.rho_em);putchar(',');num(c.rho_nu);putchar(',');num(c.rho_b);
 putchar(',');num(c.rho_h);putchar(',');num(c.p_h);putchar(',');num(c.rho_lambda);
 putchar(',');num(c.H);putchar(',');num(rhoBref);putchar(',');num(bg->cfg->consts.ma*nB);
 putchar(',');num(c.provider_used?c.material.w:0.);putchar(',');num(c.provider_used?c.material.ca2:0.);
 putchar(',');num(c.provider_used?c.material.drho_dln_a:-3*c.rho_h);
 putchar(',');num(c.provider_used?c.material.log_action_residual:0.);
 putchar(',');num(c.provider_used?c.material.virial_relative_residual:0.);putchar(']');
 if(c.provider_used) {
  test(close_rel(c.material.drho_dln_a,-3*(c.rho_h+c.p_h),2e-11));
  test(fabs(c.material.log_action_residual)<=2e-11);
  test(fabs(c.material.virial_relative_residual)<=2e-11);
  test(c.material.w>=0&&c.material.w<=1./3.+2e-12);
 }
}
'''

def adapter(s):
 s=s.replace('PRIMAT_ORDINARY_BASELINE_V001','PRIMAT_MATCHED_SCALAR_V001')
 s=s.replace('COMPLETE_ORDINARY_ONLY','COMPLETE_FIXED_NEVO_CONDITIONAL')
 s=once(s,'int main(int argc,char **argv) {',ADAPTER_HELPERS+'\nint main(int argc,char **argv) {')
 s=once(s,' if (argc!=2||(strcmp(argv[1],"default")&&strcmp(argv[1],"refined")))\n  return fail("arguments","exactly one fixed profile: default or refined");',r''' if(argc!=12) return fail("arguments","profile branch case kind h omega_b Omega_m T0 R I1 e1 required");
 int profile=!strcmp(argv[1],"default")?0:!strcmp(argv[1],"refined")?1:!strcmp(argv[1],"material")?2:!strcmp(argv[1],"background")?3:-1;
 int branch=!strcmp(argv[2],"L")?0:!strcmp(argv[2],"D0")?1:!strcmp(argv[2],"D")?2:!strcmp(argv[2],"S")?3:-1;
 double values[9];for(int i=0;i<9;i++)if(!numeric(argv[3+i],values+i))return fail("arguments","finite strict numbers required");
 if(values[0]<0||values[0]>=335||(values[1]!=1&&values[1]!=2))return fail("arguments","case/kind range");
 int caseid=(int)values[0],kind=(int)values[1];
 double h=values[2],ob=values[3],om=values[4],T0=values[5],R=values[6],I1=values[7],e1=values[8];
 if(profile<0||branch<0||caseid<0||caseid>=335||caseid!=values[0]||(kind!=1&&kind!=2)||kind!=values[1]
    ||!(h>0&&ob>0&&om>ob/(h*h)&&om<1&&T0==2.72548)
    ||(kind==1&&!(R>1&&I1>0&&e1>0))||(kind==2&&(R!=0||I1!=0||e1!=0)))
  return fail("arguments","outside fixed case/state/configuration domain");
 int order=profile<2?64:128;''')
 s=once(s,' char *err=NULL; const char *stage="config";',' unt_hard_context material={0};\n char *err=NULL; const char *stage="config";')
 s=once(s,' cfg.numerical_precision=!strcmp(argv[1],"default")?1e-7:1e-8;',r''' cfg.numerical_precision=profile==0?1e-7:1e-8;
 cfg.sampling_temperature_per_decade=profile==3?1200:600;
 cfg.h=h;cfg.Omegach2=h*h*om-ob;
 CPRParam T0value={.type=CPR_DOUBLE,.v.d=T0};
 if(cpr_config_set_by_name(&cfg,"T0CMB",T0value,&err))goto failed;
 cpr_config_set_Omegabh2(&cfg,ob);''')
 s=once(s,'||cfg.sampling_temperature_per_decade!=600||!cfg.weak_rate_cache)', '||cfg.sampling_temperature_per_decade!=(profile==3?1200:600)||!cfg.weak_rate_cache)')
 a=' stage="standard_background"; if(cpr_bg_init_standard(&bg,&cfg,&pl,&err)) goto failed; have_bg=1;'
 s=once(s,a,r''' stage="material_initialization";
 char material_error[256];double rho1=cfg.Omegach2*cpr_config_rhocOverh2(&cfg);
 int mrc=(branch==3&&kind==1)?unt_hard_init(&material,order,R,I1,e1,rho1,1e-16,1.,material_error,sizeof material_error)
                             :unt_hard_init_dust(&material,rho1,1e-16,1.,material_error,sizeof material_error);
 if(mrc) {err=strdup(material_error);goto failed;}
 stage="matched_background";
 if(branch==0) {if(cpr_bg_init_standard(&bg,&cfg,&pl,&err))goto failed;}
 else if(cpr_bg_init_owned(&bg,&cfg,&pl,&material,branch>=2,&err))goto failed;
 have_bg=1;''')
 s=s.replace('ordinary fixed-NEVO standard background; no candidate H modification, abundance likelihood or uncertainty propagation','same-state scalar/dust matched fixed-NEVO conditional abundances; no self-consistent reheating, abundance likelihood or native-origin qualification')
 s=once(s,' printf(",\\\"physical\\\":{\\\"h\\\":");num(cfg.h);',r''' printf(",\"state\":{\"case_id\":%d,\"kind\":%d,\"branch\":",caseid,kind);js(argv[2]);
 printf(",\"provider_order\":%d,\"R\":",order);num(R);printf(",\"I1\":");num(I1);printf(",\"e1\":");num(e1);
 printf(",\"reference_energy_relative_error\":");num(material.reference_energy_relative_error);
 printf(",\"domain_a\":[1e-16,1]},\"physical\":{\"h\":");num(cfg.h);''')
 s=once(s,' printf(",\\\"LT_rtol_multiplier\\\":10,\\\"rate_grid_npts\\\":1000,\\\"temperature_samples_per_decade\\\":600,\\\"new_tables_generated\\\":false},");',r''' printf(",\"LT_rtol_multiplier\":10,\"rate_grid_npts\":1000,\"temperature_samples_per_decade\":%d,\"new_tables_generated\":false},",cfg.sampling_temperature_per_decade);''')
 # Keep every original nuclear/background/rate row, plus same-node components.
 a=' /* No new ODE: quadrature of the actual fixed HT generator, in log time. */'
 s=once(s,a,r''' printf("],\"component_columns\":[\"rho_EM\",\"rho_nu\",\"rho_b_in_H\",\"rho_H\",\"p_H\",\"rho_Lambda\",\"H\",\"mB_ref_nB\",\"ma_nB_reaction\",\"w_H\",\"ca2_H\",\"drho_H_dln_a\",\"log_action_residual\",\"virial_residual\"],\"components\":[");
 for(size_t i=0;i<bg.n_bg;i++) {
  if(i)putchar(',');component_row(&bg,bg.Tg_vec[i],bg.Tnue_vec[i],bg.Tnumu_vec[i],bg.Tnutau_vec[i],bg.a_vec[i]);
 }
 /* No new ODE: quadrature of the actual fixed HT generator, in log time. */''')
 return s.replace('/* Project-local ordinary PRIMAT baseline. No scalar H hook or file output.','/* Project-local matched scalar PRIMAT. Four explicit branches; no file output.')

def main():
 if Path.cwd().resolve()!=ROOT or Path(__file__).resolve()!=J/'derive_primat_scalar_sources_v001.py':raise RuntimeError('Wrong root/script')
 specs=[('upstream/primat-c/include/background.h','background.h',header),
        ('upstream/primat-c/src/background.c','background.c',background),
        ('derived_ordinary_v001/unt_primat_ordinary_v001.c','unt_primat_scalar_v001.c',adapter)]
 files=[]
 for source,name,fn in specs:
  old=read(source);new=fn(old);raw=new.encode()
  files.append(dict(path='derived_scalar_v001/'+name,source_path=source,source_sha256=PINS[source],bytes=len(raw),sha256=sha(raw),data_base64=base64.b64encode(raw).decode(),diff=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=source,tofile='derived_scalar_v001/'+name))))
 old=json.loads(read('PRIMAT_ORDINARY_BUILD_MANIFEST_V001.json'));commands=[];objects=[]
 for c in old['commands']:
  if c['kind']!='compile':continue
  source=Path(c['source'])
  if source.name=='background.c':source=D/'background.c'
  if source.name=='unt_primat_ordinary_v001.c':source=D/'unt_primat_scalar_v001.c'
  out=BUILD/(source.stem+'.o');objects.append(str(out))
  argv=['/usr/bin/clang','-std=gnu11','-O2','-Wall','-Wextra','-fno-fast-math','-pthread','-I'+str(B/'upstream/primat-c/include'),'-I'+str(J),'-include',str(D/'background.h'),'-c',str(source),'-o',str(out)]
  commands.append(dict(id=len(commands),kind='compile',source=str(source),output=str(out),argv=argv))
 source=J/'unt_hard_barotrope_v001.c';out=BUILD/'unt_hard_barotrope_v001.o';objects.append(str(out))
 commands.append(dict(id=len(commands),kind='compile',source=str(source),output=str(out),argv=['/usr/bin/clang','-std=gnu11','-O2','-Wall','-Wextra','-fno-fast-math','-pthread','-I'+str(B/'upstream/primat-c/include'),'-I'+str(J),'-include',str(D/'background.h'),'-c',str(source),'-o',str(out)]))
 binary=BUILD/'unt_primat_scalar_v001'
 commands.append(dict(id=len(commands),kind='link',output=str(binary),argv=['/usr/bin/clang','-pthread',*objects,'-lm','-o',str(binary)]))
 manifest=dict(schema='PRIMAT_MATCHED_SCALAR_BUILD_V001',cwd=str(ROOT),commands=commands,binary=str(binary),environment=old['environment'],unset_environment=old['unset_environment'],compiler_version_argv=['/usr/bin/clang','--version'],forced_header=str(D/'background.h'),ordinary_manifest_sha256=PINS['PRIMAT_ORDINARY_BUILD_MANIFEST_V001.json'])
 print(json.dumps(dict(schema='PRIMAT_SCALAR_DERIVATION_V001',status='DERIVED_NOT_COMPILED_OR_RUN',transformer_sha256=sha(Path(__file__).read_bytes()),files=files,build_manifest=manifest),sort_keys=True,separators=(',',':'),allow_nan=False))
if __name__=='__main__':main()
