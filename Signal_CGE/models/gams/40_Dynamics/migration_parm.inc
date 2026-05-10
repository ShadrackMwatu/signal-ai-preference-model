*#######MIGRATION###########################


*######### select functional form for migration ########
* Select among three functional forms
* Variant 1 employs a constant elasticity functional form
* that governs migration
* - select V1 and elasthh = 0 for no migration
* the other two variants are employing transition matrices
* that are based on probability functions:
* Version 2 is a basic version and
* version 3 a more sophisticated setup employing a nested
* functional form


*#######################################################

Set map_insw_inswp(insw,insw)
 /#ins:#ins/
 ins_mig(ins) institutions that can migrate
 fmig_group   factor groups for migration
 f_mig(f)     factors that can migrate
 map_f_fmig(f,fmig_group) mapping between factors and factor groups in which they migrate
 ;
 SINGLETON Set
t01(t1);
t01(t1)$(not  t2(t1)) =yes;

Alias (ins,insp,inspp);

*sets that govern migration coefficients
set
*wider regions different households may be part of and mapping
    region
    map_region_h(*,insw)
    mig_coeff 
;


Parameter

 fsi_beforeMig(insw,fmig_group,t) Factor supplies of ins and f in periode t before migration
 fs_beforeMig(insw,t)             Factor supplies of ins in periode t before migration
 fsi_afterMig(insw,fmig_group,t)  Factor supplies of ins and f in periode t after migration
 fsim_i(fmig_group,insw,insw)     Migration matrix by origin factor f origin ins and destination ins
*Parameters for V1
 ymigr_t(insw,inswp,t)            relative income-expenditure driver used in V1
 etahh(fmig_group,insw,insw)      migration  elasticity for variant 1
*Parameters for V2 und V3
 Y_migr(insw,t)                   income-expenditure driver used in V2 and V3
 beta_mig0(mig_coeff,*)           migration coefficients (destination) employed in V2 and V3
 beta_mig(mig_coeff)              applied migration coefficients (destination) 
 dist_insa(insw,insw)             distance between regions (from-to) --> from excel
 own_01(insw,inswp)               dummy for own household
 urban_01(ins)                    urban dummy 1 if urban
 region_01(insw,inswp, region)    regional dummy - 0 if same region

 Vod(fmig_group,insw,inswp,t)     intermediate step Pod - Vod
 exp_Vod_1(fmig_group,ins,insp,t) intermediate step Pod - exp Vod origin factors
 exp_Vod(fmig_group,ins,insp,t)   intermediate step Pod - exp Vod 
 exp_Voo(fmig_group,insw,inswp,t) intermediate step Pod - exp Voo 
 sum_exp_Vod(fmig_group,ins,t)    intermediate step Pod - sum of exp Vod
 Pod(fmig_group,ins,insp,t)       probability matrix
 Pod_0(fmig_group,ins,insp)       control parameter - Pod in t01 before calibration

*Result/control Parameters
 resfsim_i(fmig_group,insw,insw,sim,t) Migration matrix by origin factor f origin ins and destination ins 
 resPod(fmig_group,ins,insp,sim,t)     probability to migrate
 resymigr_t(h,hp,sim,t)                relative income-expenditure driver used in V1
 resy_migr(h,sim,t)                    income-expenditure driver used in V2 and V3
 reshohosh_mig(f,hp,h,sim,t1)          share of factor income remitted by destination household

*Parameters used for remittances 
 mig_net(fmig_group,h,hp)           net migration flow of factor f from region h in region hp
 mig_stock(fmig_group,h,hp,t)       stock of migrants of factor f from region h in region hp
* mig_stock_pos(fmig_group,h,hp,t)   
 deprec_mig                         rate migrants become member of destination region
 sh_remit                           share of factor income remitted by migrants
 urbn_growth                        growth rate of urbanisation

 Trk_urbanratep(sim,t)
 urbanratep          Uranisation rate
 ;
 

*$CALL "GDXXRW i=%dataF%\%experiment% o=%gdxF%\exp_in.gdx INDEX=LAYOUT!A4"
$GDXIN %gdxF%\exp_in.gdx

$LOADdc ins_mig fmig_group f_mig map_f_fmig
$LOADdc deprec_mig sh_remit
$LOADdc etahh
$LOADdc region map_region_h mig_coeff beta_mig0 dist_insa
$LOADdc urbn_growth
    
$GDXIN
 
$ifthen.driver %mig_Ydriver%=="INSVA"
 ymigr_t(h,hp,t01)=[SUM(f,INSVA0(hp,f))/POPN0(hp)]/[SUM(f,INSVA0(h,f))/POPN0(h)] ;
 y_migr(h,t01)=SUM(f,INSVA0(h,f))/POPN0(h);
$elseif.driver %mig_Ydriver%=="HEXP"
 ymigr_t(h,hp,t01)= (HEXP0(hp)/POPN0(hp))/(HEXP0(h)/POPN0(h)) ;
 y_migr(h,t01) = HEXP0(h)/POPN0(h);
$endif.driver

 fsim_i(fmig_group,insw,insw) = 0.0;
 fsi_beforeMig(ins_mig(ins),fmig_group,t01) =sum(f$map_f_fmig(f,fmig_group), FSI0(ins,f)) ;
 fs_beforeMig(ins,t01)=sum(fmig_group,fsi_beforeMig(ins,fmig_group,t01));
 
 urban_01(ins) = 0.0 ; 
 urban_01(h)$(NOT hrur(h)) = 1.0 ;
 own_01(h,hp) = 0.0 ;
 own_01(h,h)  = 1.0 ;
 region_01(h,hp,region) = 0.0 ;
 region_01(h,hp,region)$(map_region_h(region,h) and  map_region_h(region,hp)) = 1.0 ;

 mig_stock(fmig_group,h,hp,t01) = 0.0;
 
*####################### CALIBRATE MIGRATION TO 0 IN t0 ##########################################

* define migration target based on change in Urbanisation rate
Parameter
 urbnrate_targ   urbanisation rate reached in next period (target)
 urbnrate_pop    urbanisation rate reached after pop growth
 net_migration_BaU(fmig_group,ins)  net migration in BaU triggered by urbanisation rate
;

 urbanratep = SUM(h$(NOT hrur(h)),popn0(h)) / SUM(h,popn0(h)) ;
 trk_urbanratep(sim1,t1) = urbanratep ;
 urbnrate_targ = urbanratep * (1+urbn_growth) ;
 urbnrate_pop = SUM(h$(NOT hrur(h)),POPNp(h)) / SUM(h,POPNp(h)) ;
 net_migration_BaU(fmig_group,h)$(NOT hrur(h))
        = (urbnrate_targ/urbnrate_pop  -1) * fsi_beforeMig(h,fmig_group,t01)
;
 net_migration_BaU(fmig_group,h)$( hrur(h))
    = - sum(hp$(NOT hrur(hp)),net_migration_BaU(fmig_group,hp))/
                SUM(hrur(hpp),fsi_beforeMig(hpp,fmig_group,t01))* fsi_beforeMig(h,fmig_group,t01);
;

$ifthen.calib  %mig_Variant%=="V2_simple-prob"

 beta_mig(mig_coeff) = beta_mig0(mig_coeff,"V2") ;

 Vod(fmig_group,ins,insp,t01)$(ins_mig(ins) and ins_mig(insp) )
                =
                     beta_mig("B_JOBSD") * log[fs_beforeMig(insp,t01)]
                  +  beta_mig("B_DIST")  * log[dist_insa(ins,insp)]
                  +  beta_mig("B_PAYD")  * log[ y_migr(insp,t01)]
                  +  beta_mig("B_URBD")  * urban_01(insp)
                  +  beta_mig("B_OTHER") * [1-sum(region,region_01(ins,insp,region) )]
                  +  beta_mig("B_OWN")   * own_01(ins,insp)
 ;
 
* intermediate steps 
 exp_Vod(fmig_group,ins,insp,t01)$(Vod(fmig_group,ins,insp,t01) )= exp(Vod(fmig_group,ins,insp,t01));
 sum_exp_Vod(fmig_group,ins,t01)=sum((insp),exp_Vod(fmig_group,ins,insp,t01)) ;
 
* uncalibrated probability matrix
 Pod_0(fmig_group,ins,insp)$(sum_exp_Vod(fmig_group,ins,t01))=[exp_Vod(fmig_group,ins,insp,t01)/sum_exp_Vod(fmig_group,ins,t01)]
 ;
 fsim_i(fmig_group,ins,ins_mig(insp))$fsi_beforeMig(ins,fmig_group,t01) 
        = fsi_beforeMig(ins,fmig_group,t01)*Pod_0(fmig_group,ins,insp) ;
              
                        
*---------------------------------------------------------------
** calculate fixed effects to ensure 0 migration in base-year **
*---------------------------------------------------------------
Variable
 migobj
 outMIG_V(fmig_group,insw)
 inMIG_V(fmig_group,insw)
 numerMIG_V(fmig_group,insw,insw)
 denomMIG_V(fmig_group,insw)
 MigCorrectionFactor(fmig_group,insw,insw)
 shareMIG_V(fmig_group,insw,insw)
;
 Equation
 migobj_eq
 numerMIG_eq(fmig_group,insw,insw)
 denomMIG_eq(fmig_group,insw)
 shareMIG_eq(fmig_group,insw,insw)
 outMIG_eq(fmig_group,insw)
 inMIG_eq(fmig_group,insw)
 ;

** we will look for the values of variable a(L,Reg1) which ensure that there is no
** net migration (out-migration = in-migration) for the base-year values of regional wages/unemployment/...
** here the equation with the objective variable (sum of squared net-migration)
** below we define more auxiliary equations (based on equation (1) in JEI
** article http://www.e-jei.org/journal/view.php?doi=10.11130/jei.2014.29.2.372 )

migobj_eq.. migobj =E= sum(fmig_group,sum(ins_mig(ins), power((outMIG_V(fmig_group,ins)-inMIG_V(fmig_group,ins)+net_migration_BaU(fmig_group,ins)),2)));


numerMIG_eq(fmig_group,ins,insp)$(ins_mig(ins) and ins_mig(insp) )..
        numerMIG_V(fmig_group,ins,insp) =E=exp( Vod(fmig_group,ins,insp,t01)
        + MigCorrectionFactor(fmig_group,ins,insp) )
        ;
        
denomMIG_eq(fmig_group,ins_mig(ins)).. denomMIG_V(fmig_group,ins) =E= sum(insp$ins_mig(insp),numerMIG_V(fmig_group,ins,insp));

shareMIG_eq(fmig_group,ins,insp)$(ins_mig(insp) and ins_mig(ins) and fsi_beforeMig(ins,fmig_group,t01))..
        shareMIG_V(fmig_group,ins,insp) =E= numerMIG_V(fmig_group,ins,insp)/denomMIG_V(fmig_group,ins);

outMIG_eq(fmig_group,ins_mig(ins))..
        outMIG_V(fmig_group,ins) =E= sum(insp$(ins_mig(insp) and(not map_insw_inswp(ins,insp))),fsi_beforeMig(ins,fmig_group,t01)*shareMIG_V(fmig_group,ins,insp));

inMIG_eq(fmig_group,ins_mig(ins))..
        inMIG_V(fmig_group,ins) =E=   sum(insp$(ins_mig(insp) and(not map_insw_inswp(ins,insp))),fsi_beforeMig(insp,fmig_group,t01)*shareMIG_V(fmig_group,insp,ins));

model mig /numerMIG_eq, denomMIG_eq, shareMIG_eq, outMIG_eq, inMIG_eq, migobj_eq/;


** set initial values 
 MigCorrectionFactor.l(fmig_group,ins,insp)$Vod(fmig_group,ins,insp,t01)=0.1;
 numerMIG_V.l(fmig_group,ins,insp)$Vod(fmig_group,ins,insp,t01)=exp(Vod(fmig_group,ins,insp,t01));
 denomMIG_V.L(fmig_group,ins_mig(ins)) = sum(insp,numerMIG_V.L(fmig_group,ins,insp));
 shareMIG_V.L(fmig_group,ins,insp)$(denomMIG_V.L(fmig_group,ins) and ins_mig(insp)) = numerMIG_V.L(fmig_group,ins,insp)/denomMIG_V.L(fmig_group,ins);
 outMIG_V.L(fmig_group,ins) = sum(insp$(ins_mig(insp) and(not map_insw_inswp(ins,insp))),fsi_beforeMig(ins,fmig_group,t01)*shareMIG_V.L(fmig_group,ins,insp));
 inMIG_V.L(fmig_group,ins)  =    sum(insp$(not map_insw_inswp(ins,insp)),fsi_beforeMig(insp,fmig_group,t01)*shareMIG_V.L(fmig_group,insp,ins));

option iterlim= 2500;
OPTION RESLIM = 3600;
SOLVE mig using nlp minimizing migobj;


*------------------ end fixed effects ----------------------------------------

*recalculate Pod in t01
 Vod(fmig_group,ins,insp,t01)$(ins_mig(ins) and ins_mig(insp) and fsi_beforeMig(insp,fmig_group,t01) )
                =
                     beta_mig("B_JOBSD") * log[fs_beforeMig(insp,t01)]                  
                  +  beta_mig("B_DIST")  * log[dist_insa(ins,insp)]
                  +  beta_mig("B_PAYD")  * log[ y_migr(insp,t01)]
                  +  beta_mig("B_URBD")  * urban_01(insp)
                  +  beta_mig("B_OTHER") *  [1-sum(region,region_01(ins,insp,region) )]
                  +  beta_mig("B_OWN")   * own_01(ins,insp)
                  +  MigCorrectionFactor.l(fmig_group,ins,insp)
 ;

 exp_Vod(fmig_group,ins,insp,t01)$Vod(fmig_group,ins,insp,t01)= exp(Vod(fmig_group,ins,insp,t01));
 sum_exp_Vod(fmig_group,ins,t01)=sum((insp),exp_Vod(fmig_group,ins,insp,t01)) ; 
 Pod(fmig_group,ins,insp,t01)$sum_exp_Vod(fmig_group,ins,t01)=[exp_Vod(fmig_group,ins,insp,t01)/sum_exp_Vod(fmig_group,ins,t01)]
 ;
 
 fsim_i(fmig_group,ins,ins_mig(insp))$ (fsi_beforeMig(ins,fmig_group,t01) )
        = fsi_beforeMig(ins,fmig_group,t01)*Pod(fmig_group,ins,insp,t01) ;
        
 fsi_afterMig(ins,fmig_group,t01)$(ins_mig(ins)  )
              =  SUM(insp, fsim_i(fmig_group,insp,ins)) ;
                          
 

$elseif.calib %mig_Variant%=="V3_nested-prob"

 beta_mig(mig_coeff) = beta_mig0(mig_coeff,"V3") ;

 Vod(fmig_group,ins,insp,t01)$(ins_mig(ins) and ins_mig(insp) )
                =
                     beta_mig("B_JOBSD") * log[fs_beforeMig(insp,t01)]
                  +  beta_mig("B_DIST")  * log[dist_insa(ins,insp)]
                  +  beta_mig("B_PAYD")  * log[ y_migr(insp,t01)]
                  +  beta_mig("B_URBD")  * urban_01(insp)
                  +  beta_mig("B_OTHER") * [1-sum(region,region_01(ins,insp,region) )]
                  +  beta_mig("B_OWN")   * own_01(ins,insp)
 ;

* intermediate steps
 exp_Voo(fmig_group,ins,ins,t01)$Vod(fmig_group,ins,ins,t01)= exp(Vod(fmig_group,ins,ins,t01));
 exp_Vod(fmig_group,ins,insp,t01)$(Vod(fmig_group,ins,insp,t01)and (not map_insw_inswp(ins,insp)))
                        = exp(Vod(fmig_group,ins,insp,t01)/ beta_mig("kappa") );

 sum_exp_Vod(fmig_group,ins,t01) $(ins_mig(ins) )   = sum(insp,exp_Vod(fmig_group,ins,insp,t01))**beta_mig("kappa") ;


* uncalibrated probability matrix 
 Pod_0(fmig_group,ins,ins) $exp_Voo(fmig_group,ins,ins,t01)  = exp_Voo(fmig_group,ins,ins,t01)/[exp_Voo(fmig_group,ins,ins,t01)+ sum_exp_Vod(fmig_group,ins,t01)];
 Pod_0(fmig_group,ins,insp)$exp_Vod(fmig_group,ins,insp,t01) =
                    sum_exp_Vod(fmig_group,ins,t01)/[sum(inspp,exp_Voo(fmig_group,ins,inspp,t01))+sum_exp_Vod(fmig_group,ins,t01)]
                  * exp_Vod(fmig_group,ins,insp,t01)/sum(inspp, exp_Vod(fmig_group,ins,inspp,t01))
 ;


 fsim_i(fmig_group,ins,ins_mig(insp))$fsi_beforeMig(ins,fmig_group,t01)
        = fsi_beforeMig(ins,fmig_group,t01)* Pod_0(fmig_group,ins,insp)
        ;

*---------------------------------------------------------------
** calculate fixed effects to ensure 0 migration in base-year **
*---------------------------------------------------------------
free variable
 migobj;
positive Variable 
 outMIG_V(fmig_group,insw)
 inMIG_V(fmig_group,insw)
 MigCorrectionFactor(fmig_group,insw,insw)
 shareMIG_V(fmig_group,insw,insw)
 V_exp_Voo(fmig_group,insw,insw)
 V_exp_Vod(fmig_group,insw,insw)
 V_sum_exp_Vod(fmig_group,insw) 
;
 Equation
 migobj_eq 
 shareMIG_eq(fmig_group,insw,insw)
 shareMIG_eq1(fmig_group,insw,insw)
 outMIG_eq(fmig_group,insw)
 inMIG_eq(fmig_group,insw)
 Eq_exp_Voo(fmig_group,insw,insw)
 Eq_exp_Vod(fmig_group,insw,insw)
 Eq_sum_exp_Vod(fmig_group,insw) 
 ;

** we will look for the values of variable a(L,Reg1) which ensure that there is no
** net migration (out-migration = in-migration) for the base-year values of regional wages/unemployment/...
** here the equation with the objective variable (sum of squared net-migration)
** below we define more auxiliary equations (based on equation (1) in JEI
** article http://www.e-jei.org/journal/view.php?doi=10.11130/jei.2014.29.2.372 )

 migobj_eq.. migobj =E= sum(fmig_group,sum(ins_mig(ins), power((outMIG_V(fmig_group,ins)-inMIG_V(fmig_group,ins) + net_migration_BaU(fmig_group,ins)),2)));


 Eq_exp_Voo(fmig_group,ins,ins)$Vod(fmig_group,ins,ins,t01)..
                        V_exp_Voo(fmig_group,ins,ins)=E= exp(Vod(fmig_group,ins,ins,t01)
                        + MigCorrectionFactor(fmig_group,ins,ins)
                        );
 Eq_exp_Vod(fmig_group,ins,insp)$(Vod(fmig_group,ins,insp,t01)and (not map_insw_inswp(ins,insp)))..
                        V_exp_Vod(fmig_group,ins,insp) =E=
                            exp((Vod(fmig_group,ins,insp,t01)+ MigCorrectionFactor(fmig_group,ins,insp)
                            )/ beta_mig("kappa") );

 Eq_sum_exp_Vod(fmig_group,ins_mig(ins))..
                        V_sum_exp_Vod(fmig_group,ins) =E= sum(insp$((  not map_insw_inswp(ins,insp)) and ins_mig(insp)),
                                V_exp_Vod(fmig_group,ins,insp))**beta_mig("kappa") ;
                                
 shareMIG_eq(fmig_group,ins,insp)$(Vod(fmig_group,ins,insp,t01)and (not map_insw_inswp(ins,insp)))..
        shareMIG_V(fmig_group,ins,insp) =E=
                            V_sum_exp_Vod(fmig_group,ins)/[sum(inspp$(ins_mig(inspp) and map_insw_inswp(ins,inspp)) ,
                        V_exp_Voo(fmig_group,ins,inspp))+V_sum_exp_Vod(fmig_group,ins)]
                  * V_exp_Vod(fmig_group,ins,insp)/
                        sum(inspp$(ins_mig(inspp) and (not map_insw_inswp(ins,inspp))), V_exp_Vod(fmig_group,ins,inspp)) ;

 shareMIG_eq1(fmig_group,ins,ins_mig(ins))$(Vod(fmig_group,ins,ins,t01) and map_insw_inswp(ins,ins))..
            shareMIG_V(fmig_group,ins,ins)=E=V_exp_Voo(fmig_group,ins,ins)
                    /[V_exp_Voo(fmig_group,ins,ins)+ V_sum_exp_Vod(fmig_group,ins)];


 outMIG_eq(fmig_group,ins_mig(ins))..
        outMIG_V(fmig_group,ins) =E= sum(insp$(ins_mig(insp) and(not map_insw_inswp(ins,insp))),
                    fsi_beforeMig(ins,fmig_group,t01)*shareMIG_V(fmig_group,ins,insp));

 inMIG_eq(fmig_group,ins_mig(ins))..
        inMIG_V(fmig_group,ins) =E=   sum(insp$(ins_mig(insp) and(not map_insw_inswp(ins,insp))),
                    fsi_beforeMig(insp,fmig_group,t01)*shareMIG_V(fmig_group,insp,ins));

   
model mig
/Eq_exp_Voo.V_exp_Voo, Eq_exp_Vod.MigCorrectionFactor, Eq_sum_exp_Vod.V_sum_exp_Vod
 shareMIG_eq.shareMIG_V, shareMIG_eq1.V_exp_Vod, outMIG_eq.outMIG_V, inMIG_eq.inMIG_V, migobj_eq/;


** set initial values 
 MigCorrectionFactor.l(fmig_group,ins,insp)$Vod(fmig_group,ins,insp,t01) = 1;
 MigCorrectionFactor.up(fmig_group,ins,insp) = 1;
 MigCorrectionFactor.lo(fmig_group,ins,insp) = -1; 
 V_exp_Voo.l(fmig_group,ins,ins)  = exp_Voo(fmig_group,ins,ins,t01);
 V_exp_Vod.l(fmig_group,ins,insp)$(Vod(fmig_group,ins,insp,t01)and (not map_insw_inswp(ins,insp)))=exp_Vod(fmig_group,ins,insp,t01);
 V_sum_exp_Vod.l(fmig_group,ins)  = sum_exp_Vod(fmig_group,ins,t01) ;

 shareMIG_V.L(fmig_group,ins,insp)$(not map_insw_inswp(ins,insp))= Pod_0(fmig_group,ins,insp);
 outMIG_V.L(fmig_group,ins) = sum(insp$(ins_mig(insp) and(not map_insw_inswp(ins,insp))),fsi_beforeMig(ins,fmig_group,t01)*shareMIG_V.L(fmig_group,ins,insp));
 inMIG_V.L(fmig_group,ins)  =    sum(insp$(not map_insw_inswp(ins,insp)),fsi_beforeMig(insp,fmig_group,t01)*shareMIG_V.L(fmig_group,insp,ins));

option iterlim= 2500;
OPTION RESLIM = 3600;
SOLVE mig using nlp minimizing migobj ;

*------------------ end fixed effects ----------------------------------------

*recalculate Pod in t01
 Vod(fmig_group,ins,insp,t01)$(ins_mig(ins) and ins_mig(insp) and fsi_beforeMig(insp,fmig_group,t01) )
                =
                     beta_mig("B_JOBSD") * log[fs_beforeMig(insp,t01)]
                  +  beta_mig("B_DIST")  * log[dist_insa(ins,insp)]
                  +  beta_mig("B_PAYD")  * log[ y_migr(insp,t01)]
                  +  beta_mig("B_URBD")  * urban_01(insp)
                  +  beta_mig("B_OTHER") *  [1-sum(region,region_01(ins,insp,region) )]
                  +  beta_mig("B_OWN")   * own_01(ins,insp)
                  +  MigCorrectionFactor.l(fmig_group,ins,insp)
 ;
 



 exp_Voo(fmig_group,ins,ins,t01)$Vod(fmig_group,ins,ins,t01)= exp(Vod(fmig_group,ins,ins,t01));
 exp_Vod(fmig_group,ins,insp,t01)$(Vod(fmig_group,ins,insp,t01)and (not map_insw_inswp(ins,insp)))
                        = exp(Vod(fmig_group,ins,insp,t01)/ beta_mig("kappa") );

 sum_exp_Vod(fmig_group,ins,t01)  $(ins_mig(ins) )   = sum(insp,exp_Vod(fmig_group,ins,insp,t01))**beta_mig("kappa") ;
 
 Pod(fmig_group,ins,ins,t01) $exp_Voo(fmig_group,ins,ins,t01)  = exp_Voo(fmig_group,ins,ins,t01)/[exp_Voo(fmig_group,ins,ins,t01)+ sum_exp_Vod(fmig_group,ins,t01)];
 Pod(fmig_group,ins,insp,t01)$exp_Vod(fmig_group,ins,insp,t01) =
                    sum_exp_Vod(fmig_group,ins,t01)/[sum(inspp,exp_Voo(fmig_group,ins,inspp,t01))+sum_exp_Vod(fmig_group,ins,t01)]
                  * exp_Vod(fmig_group,ins,insp,t01)/sum(inspp, exp_Vod(fmig_group,ins,inspp,t01))
 ;

* Mh,hp,t = POPhp,t * Ph,hp,t


*migration in t01
 fsim_i(fmig_group,ins,ins_mig(insp))$fsi_beforeMig(ins,fmig_group,t01)
        = fsi_beforeMig(ins,fmig_group,t01)* Pod(fmig_group,ins,insp,t01);
$endif.calib

 fsi_afterMig(ins,fmig_group,t01)$(ins_mig(ins)  )
              =  SUM(insp, fsim_i(fmig_group,insp,ins)) ;

