$TITLE DEMETRA Capital Accumulation parameter declarations
*------------------------------------------------------------------------------
*-------------------------------------------------------------------------------
*--   DEMETRA v1.0-alpha
*--
*--   GAMS file : calibchk_declare.inc
*--
*--   @purpose  : Declares the parameters for capital update
*--   @author   :
*--   @date     :
*--   @since    :
*--   @refDoc   :
*--   @seeAlso  :
*--   @calledBy : dynamic simulations
*-------------------------------------------------------------------------------
*-------------------------------------------------------------------------------

$ontext
Notes and description



$offtext

*------- 1. Declare and Assign Parameters  ------------------------

*---- 1a. Declare Parameters for Capital Accumulation

Parameter
*----- 2a. Parameters for updating Capital stock

*-~~~~ 2a1. Investment - generation of new capital goods

 invest_f(f)          Investment expenditure by factor type f
 Trk_invest_f(k,t,sim) Tracker for invest_f
 gfcf(f)              Gross fixed capital formation by capital type k

 Trk_gfcf(k,t,sim)     Tracker for gfcf

 fda(k,a)              updated FD value carrier between periods

 pk(f)                Price of gfcf by capital type k
 Trk_pk(k,t,sim)
*-~~ depreciation

 deprec_a(f,a)    Depreciation rates in by capital type and activity

 fs_k(k)          Total capital by capital type

*-~~~~ 2a2. Allocation of new capital goods
*-~~ Rental returns on capital

 wf_rel(k)         Relative returns on capital by type k

 wfa_av(k)         Average return on capital by type across activities
 wfa_rel(k,a)      Relative returns on capital by type and activity

*-~~ Shares of existing capital stock
 cap_sup_sh(ff,i)       capital supply shares in each investment type
 Trk_cap_sup_sh(k,i,t,sim)      tracker for capital supply shares in each investment type
 cap_sh_k(ff)     Capital shares by type of capital for investment type i
 cap_sh_ki(ff,i)     Capital shares by type of capital for investment type i
 Trk_cap_sh_ki(k,i,sim,t) Tracker for Capital shares by type of capital for investment type i

 cap_sh_ka(ff,a)    Capital shares by type of capital and activity

 cap_sh_kCHK     Check on Capital shares by type of capital
 cap_sh_kaCHK(k)    Check on Capital shares by type of capital and activity

*-~~ Shares of new capital goods

 inv_sh_k(k,i)       Investment shares by type of capital
 inv_sh_kCHK(k)      Check on Investment shares by type of capital
 Trk_inv_sh_k(k,i,sim,t)  Tracker for Investment shares by type of capital
 inv_sh_ka(k,a)    Investment shares by capital type and activity
 inv_sh_kaCHK(k)   Check on investment shares by capital type and activity

*-~~ Changes in capital stocks

 d_kap_k(k)        Changes in capital stock by type of capital
 Trk_d_kap_k(k)    tracker for d_kap_k(k)
 d_kap_ka(k,a)     Changes in capital stock by type of capital and activity
 Trk_d_kap_ka(k,a,t,sim)   tracker for d_kap_ka
 d_kap_kaCHK(k)    Check on Changes in capital stock by type of capital and activity

 Diff_FD(k,a)

*-~~~~ 2a3. Savings - funding of New Capital goods

*-~~ Savings by institutions
 ins_sav(ins)      Savings by each institution
 tot_ins_sav       Total Savings by institution

 ins_sav_sh(ins)   Shares of Savings by each institution
 ins_sav_sh_CHK    Check on Shares of Savings by each institution

*-~~ Shares of existing capital stock owned by institutions

 cap_sh_insw(insw,f)  Shares of capital by each insitution at end of period

 cap_sh_insw_CHK(f)  CHK on Shares of capital by each insitution

*-~~ Investment shares by Institution in current period

 inv_sh_ins(ins,k) Investment shares by institution and capital

 inv_sh_insCHK(ins) Check on Investment shares by institution

*-~~ Changes in ownership of capital stocks

 d_kap_ins(ins,k)   New Capital by institution

 d_kap_insCHK(k)    CHECK on new capital

 diff_FSI(ins,k)   Changes in capital ownership matrix

*-~~ Parameters ensuring reconciliation between FD and FSI

 fmkt(k)
 fsi_ent(k)       allocation of new capital to ent based on shares
 fsi_resid_chk(k) Difference between assigned FSI and residual assignment

*-~~ Changes in investment share relative to capital shares

 diff_cap_inv_sh_k(k,i)     Differences in capital and investment share by k
 diff_cap_inv_sh_ka(k,a)  Differences in capital and investment share by k anad a


*-~~~~ 2a4. Shares of Investment funds for next period

 qinvb0(i)         Investment volumes for comparison of changes

 diff_qinvb(i)     Changes in investment volumes


*- Changes in capital services
*- FSCHK(k)          Check that FS = sumFD gives same result as FS+inv-dep


 ;


*----- Loading data and sets from Excel

*- GDX data file generated in main (static/dynamic) experiment files

*----- 1a. Load data from GDX data file

$GDXIN %gdxF%\exp_in.GDX

*- Sets
$LOADdc

*- Data
$LOADdc   mu_fact mu_activ  


$GDXIN

 fda(k,a) =  fd0(k,a);


 mu_k(k,t)   = mu_fact(k,"wf_k") ;

 mu_a(a,t)   = mu_activ(a,"wf_a") ;

 deprec_a(k,a) = 0.05;
* deprec_a("capital_Livst_Rural",a) = 0.10;

