
$TITLE STAGE DEV Recursive Dynamic CGE Model Capital Updating V13
*------------------------------------------------------------------------------
*-------------------------------------------------------------------------------
*--   DEMETRA v1.0-alpha
*--
*--   GAMS file : cap_update.inc
*--
*--   @purpose  : capital stock update
*--   @author   : 
*--   @date     :
*--   @since    :
*--   @refDoc   :
*--   @seeAlso  :
*--   @calledBy : dynamic simulations
*-------------------------------------------------------------------------------
*-------------------------------------------------------------------------------

$ontext

  7. Physical Capital for the NEXT period

     Steps:
      7a.  Define gfcf(k) on the basis of investment decisions in investments
           of type i in the previous period
           Define the price of capital of type k (pk(k))

      7b.  Define allocations of new physical capital to activities on
           the basis of
           (i)   distribution of capital type k to activity a in the previous
                 period
           (ii)  changes in the rates of return to capital type k in
                 the previous period
           (iii) investment of capital type k to activity a in the next
                 period given responiveness to changes in rates of return

      7c.  Define quantities of NEW capital type k by activity for the next
           period on the basis of
           (i)   investnment shares
           (ii)  quantities of each new type of capital

      7d. Define Quantities of Capital for the NEXT period
           (i)   the depreciation of capital by capital type k and activity
                 a at the end of the period
           (ii)  the quantity of new capital k allocated to activity a
           (iii) check supply and demand equilibrium

  8. Defining Shares of Investment funds used to generate new capital in the NEXT period

       8a. Savings and Shares by each Institution based on
           (i)   after tax incomes by institution
           (ii)  savings rates by institution

       8b. Define shares of investible funds to each investment type i
           in the next period on the basis
           (i)   distribution of investment type i in the previous
                 period
           (ii)  changes in the rates of return to capital type k in
                 the previous period

       8c. New capital by institution

       8d. Capital ownership by each institution for next period based on
           (i)   quantity from previous period
           (ii)  depreciation rates by type of capital
           (iii) NEW capital by institution


       9. Updating Shares of Investment funds for next period based on
           (i)   capital value shares
           (ii)  investment shares
           (iii) responsiveness of investment shares to rates of return

$offtext

*-------- 7. Updating capital stocks ------------------------------------

*----- 7a. Defining Generation of New Capital

 cap_sup_sh(k,i)$map_f_i(k,i) = (cap_sup_ad(k,i,sim1,t1)*FS.L(k))/SUM(kp$map_f_i(kp,i),FS.L(kp)*cap_sup_ad(kp,i,sim1,t1));

 Trk_cap_sup_sh(k,i,t1,sim1) =  cap_sup_sh(k,i);

* invest_f(k)  = SUM{i$map_k_i(k,i), SUM[c,PQD.L(c)*QINVD.L(c,i)]} ;;
 invest_f(k)  = transrate(k,t1)*SUM{i$map_f_i(k,i), SUM[c,PQD.L(c)*QINVD.L(c,i)*cap_sup_sh(k,i)]} ;;

 Trk_invest_f(k,t1,sim1) = invest_f(k) ;

 pk(k)        = SUM(i$(map_f_i(k,i) AND SUM(cp,QINVD.L(cp,i))),SUM{c,PQD.L(c)
                       * [QINVD.L(c,i)/SUM(cp,QINVD.L(cp,i))]}) ;

 Trk_pk(k,t1,sim1) = pk(k);

 gfcf(k)$pk(k)   = invest_f(k)/pk(k) ;

 Trk_gfcf(k,t1,sim1)      =  gfcf(k);

 fs_k(k)         = SUM(ins,fsia(ins,k)) ;

*----- 7b. Defining Allocation of New Capital
*- Define captital shares in current period by ref to type of capital & activity

 cap_sh_ka(k,a)$ (SUM(ap,FD.L(k,ap)))  = FD.L(k,a)/SUM(ap,FD.L(k,ap)) ;



 cap_sh_kaCHK(k) = SUM(a, cap_sh_ka(k,a)) ;

*- Average rental to capital

 wfa_av(k)              = SUM(a, WF.L(k) * WFDIST.L(k,a) * cap_sh_ka(k,a)) ;

 wfa_rel(k,a)$wfa_av(k) = (WF.L(k) * WFDIST.L(k,a))/wfa_av(k) ;

*- Deriving investment shares for NEXT period
*- modified by a response function to a relative price

 inv_sh_ka(k,a)$(SUM(ap,cap_sh_ka(k,ap) * (1 + mu_a(ap,t1) * (wfa_rel(k,ap) - 1)))) =
                 cap_sh_ka(k,a) * (1 + mu_a(a,t1) * (wfa_rel(k,a) - 1))
                 / SUM(ap,cap_sh_ka(k,ap) * (1 + mu_a(ap,t1) * (wfa_rel(k,ap) - 1))) ;
* inv_sh_ka(k,a) = cap_sh_ka(k,a) * (1 + mu_a(a,t1) * (wfa_rel(k,a) - 1)) ;

 inv_sh_kaCHK(k) = SUM(a, inv_sh_ka(k,a)) ;

*- Differences in Capital and Investment shares for information

 diff_cap_inv_sh_ka(k,a) = cap_sh_ka(k,a) - inv_sh_ka(k,a) ;

*----- 7c. Defining Quantities of NEW Capital for the NEXT period

 d_kap_ka(k,a) $pk(k)  = inv_sh_ka(k,a) * gfcf(k) ;

 Trk_d_kap_ka(k,a,t1,sim1)  = d_kap_ka(k,a);
 d_kap_kaCHK(k)$pk(k)  = SUM(a,d_kap_ka(k,a)) - gfcf(k) ;

*-calculate average depreciation rate
 deprec(k)$(SUM(a,FD.L(k,a))) = SUM(a,FD.L(k,a)*deprec_a(k,a))/SUM(a,FD.L(k,a));

*----- 7d. Defining Quantities of Capital for the NEXT period
 FD.fx(k,a)      = ((FD.L(k,a) * (1-deprec_a(k,a))) + d_kap_ka(k,a)) ;

 Diff_FD(k,a)    = ((FD.L(k,a) * (1-deprec_a(k,a))) + d_kap_ka(k,a)) - FD.L(k,a) ;

*----- 8. Defining Capital ownership by Institution for the NEXT period

*-~~~ 8a. Savings and Shares by each Institution

 ins_sav(h)      = (YH.L(h) * (1 - TYH.L(h))) * SHH.L(h) ;
 ins_sav(e)      = (YE.L(e) * (1 - TYE.L(e))) * SEN.L(e) ;
*- ins_sav("row")  = (CAPWOR.L * ER.L) ;

 tot_ins_sav       = SUM(h, ins_sav(h)) + SUM(e, ins_sav(e)) ;
*- + ins_sav("row") ;

 ins_sav_sh(h)     = ins_sav(h)/tot_ins_sav ;
 ins_sav_sh(e)     = ins_sav(e)/tot_ins_sav ;
*- ins_sav_sh("row") = ins_sav("row")/tot_ins_sav ;

 ins_sav_sh_CHK    = SUM(h,ins_sav_sh(h)) + SUM(e,ins_sav_sh(e)) ;
*-                     + ins_sav_sh("row") ;

*-~~~ 8b. Capital shares by Institution in current period

 fsia(ins,k)    = FSI.L(ins,k) ;

 cap_sh_insw(ins,k)$fsia(ins,k)  = fsia(ins,k)/SUM(insp,fsia(insp,k)) ;

 cap_sh_insw_CHK(k)  = SUM(ins,cap_sh_insw(ins,k)) ;

*- New capital by institution

 d_kap_ins(ins,k) = cap_sh_insw(ins,k) * gfcf(k) ;

 d_kap_insCHK(k)  = SUM(ins,d_kap_ins(ins,k)) - gfcf(k) ;

*-~~~ 8e. Capital ownership by each institution for next period

 FSI.FX(ins,k)  = fsia(ins,k) * (1-deprec(k)) + d_kap_ins(ins,k) ;

 fsia(ins,k)    = FSI.L(ins,k) ;

*- Set one capital source residually to avoid problems with constraints

 fsi_ent(k)     = FSI.L('ent',k) ;

 FSI.FX('ent',k) = SUM(a, FD.L(k,a)) - SUM(h, FSI.L(h,k)) ;


 fsi_resid_chk(k)   = fsi_ent(k) - FSI.L('ent',k) ;

*-------- 9. Updating Shares of Investment funds -------------------------
*- This section defines qinvb(i) for the next solution

*- Capital value shares

 cap_sh_k(k)  = [SUM(a,WF.L(k)*WFDIST.L(k,a)*FD.L(k,a))]
                   /[SUM((kp,a),WF.L(kp)*WFDIST.L(kp,a)*FD.L(kp,a))] ;

 cap_sh_ki(k,i)$map_f_i(k,i)  = cap_sh_k(k);

 cap_sh_ki(f,i)$(SUM(fp,cap_sh_ki(fp,i))) = (cap_sup_ad(f,i,sim1,t1)*cap_sh_ki(f,i))/(SUM(fp,cap_sup_ad(fp,i,sim1,t1)*cap_sh_ki(fp,i)));

 Trk_cap_sh_ki(k,i,sim1,t1) = cap_sh_ki(k,i);

 cap_sh_kCHK     = SUM(k, cap_sh_k(k)) ;

*- Deriving investment shares

 qinvb0(i)     =  qinvb(i) ;

 wf_rel(k)     = wfa_av(k)/[SUM(kp, wfa_av(kp) * cap_sh_k(kp))] ;

 inv_sh_k(k,i)$map_f_i(k,i)   = cap_sh_ki(k,i) * (1 + mu_k(k,t1) * (wf_rel(k) - 1));

 Trk_inv_sh_k(k,i,sim1,t1) =  inv_sh_k(k,i);

 inv_sh_kCHK(k)   = SUM(i, inv_sh_k(k,i)) ;

 diff_cap_inv_sh_k(k,i)    = cap_sh_ki(k,i) - inv_sh_k(k,i) ;

 qinvb(i)      = SUM(k,inv_sh_k(k,i)* qinvb0(i)) ;

 fmkt(k)  = SUM(a, FD.L(k,a)) - SUM(ins,FSI.L(ins,k)) ;

*-Ethiopia
 FSI.FX(ins,"flnd-rf")  =    FSI0(ins,"flnd-rf")  +  FSI0(ins,"flnd-ir")-  fsia(ins,"flnd-ir");

*- Senegal
* FSI.FX(ins,"fland_nir")  =    FSI0(ins,"fland_nir")  +  FSI0(ins,"fland_irr_sml")-  fsia(ins,"fland_irr_sml")
*                                                +  FSI0(ins,"fland_irr_com")-  fsia(ins,"fland_irr_com");

* FSI.FX(ins,"fland_nir")  =    FSI0(ins,"fland_nir");

* FSI.FX(ins,"fland_nir")  =    FSI0(ins,"fland_nir")  +  FSI0(ins,"fland_irr_sml")-  fsia(ins,"fland_irr_sml")
*                                                +  FSI0(ins,"fland_irr_com")-  fsia(ins,"fland_irr_com");

* FSI.FX(ins,"fland_nir")  =    FSI0(ins,"fl_nir")  +  FSI0(ins,"fl_irr")-  fsia(ins,"fl_irr");


*-update land use for irrigated activities according to base shares
* FD.FX("fl_nir",a)    =      FD.L("fl_nir",a) /SUM(ap,  FD.L("fl_nir",ap) )* SUM(ins,FSI.L(ins,"fl_nir"))  ;
* FD.FX("fland_nir",a)$(FD0("fland_irr_sml",a)+FD0("fland_irr_com",a))
*                    =      FD.L("fland_nir",a)  ;

*-############# END OF PHYSICAL CAPITAL UPDATES ###########################
