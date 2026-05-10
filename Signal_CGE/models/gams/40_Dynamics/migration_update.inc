*------------------ internal migration --------------
 display "before" FSI.l;

 fsi_beforeMig(ins,fmig_group,t1) = sum(f$map_f_fmig(f,fmig_group), FSI.L(ins,f)) ;
 fs_beforeMig(ins,t1)=sum(fmig_group,fsi_beforeMig(ins,fmig_group,t1));
 
$ifthen.driver %mig_Ydriver%=="INSVA"
 ymigr_t(h,hp,t1)=
    [SUM(f,INSVA.L(hp,f))/POPNp(hp)]/[SUM(f,INSVA.L(h,f))/POPNp(h)] ;
 y_migr(h,t1) = SUM(f,INSVA.l(h,f)/POPNp(h));
$elseif.driver %mig_Ydriver%=="HEXP"
 ymigr_t(h,hp,t1)= HEXP.l(hp)/HEXP.l(h)*POPNp(h)/POPNp(hp) ;
 y_migr(h,t1) = HEXP.l(h)/POPNp(h);
$endif.driver 



*########## Variant 1: constant elasticity functional form ############################
$ifthen %mig_Variant%=="V1_constElast"
 
if(NOT t2(t1),

 fsim_i(fmig_group,ins,ins_mig(insp))$ (fsi_beforeMig(ins,fmig_group,t1) )
        = fsi_beforeMig(ins,fmig_group,t1)*(ymigr_t(ins,insp,t01)/
                  ymigr_t(ins,insp,t01))**etahh(fmig_group,ins,insp)
                                       - fsi_beforeMig(ins,fmig_group,t1) ;

else                   

 fsim_i(fmig_group,ins,ins_mig(insp))$ (fsi_beforeMig(ins,fmig_group,t1) )
        = fsi_beforeMig(ins,fmig_group,t1)*(ymigr_t(ins,insp,t1)/
                  ymigr_t(ins,insp,t1-1))**etahh(fmig_group,ins,insp)
                                       - fsi_beforeMig(ins,fmig_group,t1) ;
display "what goes on?";                                      
);                                       
display fsim_i,ymigr_t;
 fsim_i(fmig_group,ins,insp)$(fsim_i(fmig_group,ins,insp)<0)=0.0;                                      
* this calculates the supply to itself accounting for any migration outflows

 fsim_i(fmig_group,ins,ins)$(ins_mig(ins) AND fsi_beforeMig(ins,fmig_group,t1))
                = fsi_beforeMig(ins,fmig_group,t1) - SUM(insp$(NOT sameas(insp,ins)),
                             fsim_i(fmig_group,ins,insp)) ;

*#####################################################################################
*########## Variant 2: simple probability function ############################

$elseif %mig_Variant%=="V2_simple-prob"
display "V2 - not nested!!";

 Vod(fmig_group,ins,insp,t1)$(ins_mig(ins) and ins_mig(insp) and fsi_beforeMig(insp,fmig_group,t01) )
                =
                     beta_mig("B_JOBSD") * log[fs_beforeMig(insp,t1)]
                  +  beta_mig("B_DIST")  * log[dist_insa(ins,insp)]
                  +  beta_mig("B_PAYD")  * log[ y_migr(insp,t1)]
                  +  beta_mig("B_URBD")  * urban_01(insp)
                  +  beta_mig("B_OTHER") *  [1-sum(region,region_01(ins,insp,region) )]
                  +  beta_mig("B_OWN")   * own_01(ins,insp)
                  +  MigCorrectionFactor.l(fmig_group,ins,insp)
 ;

 exp_Vod(fmig_group,ins,insp,t1(t))$Vod(fmig_group,ins,insp,t)= exp(Vod(fmig_group,ins,insp,t));
 sum_exp_Vod(fmig_group,ins,t1(t))=sum((insp),exp_Vod(fmig_group,ins,insp,t)) ; 
 Pod(fmig_group,ins,insp,t1(t))$sum_exp_Vod(fmig_group,ins,t)=[exp_Vod(fmig_group,ins,insp,t)/sum_exp_Vod(fmig_group,ins,t)]
 ;
 
* Mh,hp,t = POPhp,t * Ph,hp,t 
 fsim_i(fmig_group,ins,ins_mig(insp))$ (fsi_beforeMig(ins,fmig_group,t1) )
        = fsi_beforeMig(ins,fmig_group,t1)*Pod(fmig_group,ins,insp,t1) ;
                                   
  resPod(fmig_group,ins,insp,sim1,t1) =  Pod(fmig_group,ins,insp,t1) ;
  
*#####################################################################################
*########## Variant 3: nested probability functional form ############################

$elseif %mig_Variant%=="V3_nested-prob"
display "NESTED!!" ;


 Vod(fmig_group,ins,insp,t1)$(ins_mig(ins) and ins_mig(insp) and fsi_beforeMig(insp,fmig_group,t1) )
                =
                     beta_mig("B_JOBSD") * log[fs_beforeMig(insp,t1)]
                  +  beta_mig("B_DIST")  * log[dist_insa(ins,insp)]
                  +  beta_mig("B_PAYD")  * log[ y_migr(insp,t1)]
                  +  beta_mig("B_URBD")  * urban_01(insp)
                  +  beta_mig("B_OTHER") *  [1-sum(region,region_01(ins,insp,region) )]
                  +  beta_mig("B_OWN")   * own_01(ins,insp)
                  +  MigCorrectionFactor.l(fmig_group,ins,insp)
 ;

 exp_Voo(fmig_group,ins,ins,t1)$Vod(fmig_group,ins,ins,t1)= exp(Vod(fmig_group,ins,ins,t1));
 exp_Vod(fmig_group,ins,insp,t1)$(Vod(fmig_group,ins,insp,t1)and (not map_insw_inswp(ins,insp)))
                        = exp(Vod(fmig_group,ins,insp,t1)/ beta_mig("kappa") );

 sum_exp_Vod(fmig_group,ins,t1) $(ins_mig(ins) )    = sum(insp,exp_Vod(fmig_group,ins,insp,t1))**beta_mig("kappa") ;
 
 Pod(fmig_group,ins,ins,t1) $exp_Voo(fmig_group,ins,ins,t1)  = exp_Voo(fmig_group,ins,ins,t1)/[exp_Voo(fmig_group,ins,ins,t1)+ sum_exp_Vod(fmig_group,ins,t1)];
 Pod(fmig_group,ins,insp,t1)$exp_Vod(fmig_group,ins,insp,t1) =
                    sum_exp_Vod(fmig_group,ins,t1)/[sum(inspp,exp_Voo(fmig_group,ins,inspp,t1))+sum_exp_Vod(fmig_group,ins,t1)]
                  * exp_Vod(fmig_group,ins,insp,t1)/sum(inspp, exp_Vod(fmig_group,ins,inspp,t1))
 ;                 
 
* Mh,hp,t = POPhp,t * Ph,hp,t 
 fsim_i(fmig_group,ins,ins_mig(insp))$ (fsi_beforeMig(ins,fmig_group,t1) )
        = fsi_beforeMig(ins,fmig_group,t1)*Pod(fmig_group,ins,insp,t1) ;

  resPod(fmig_group,ins,insp,sim1,t1) =  Pod(fmig_group,ins,insp,t1) ;                             
$endif
                            
$ontext
 the supply of factor f in household type ins, accounting for migration
 flows, is the sum of migration of factor type f, from household insp to
 household ins
$offtext
        
 fsi_afterMig(ins,fmig_group,t1)$(ins_mig(ins)  )
              =  SUM(insp, fsim_i(fmig_group,insp,ins)) ;
                          
 FSI.fx(ins_mig(ins),f_mig(f))$FSI0(ins,f) =sum(fmig_group$map_f_fmig(f,fmig_group),fsi_afterMig(ins,fmig_group,t1)) ;
 POPNp(h)      =  SUM(l,FSI.L(h,l))  ;
 
 resfsim_i(fmig_group,ins,insp,sim1,t1) = fsim_i(fmig_group,ins,insp);
 resymigr_t(h,hp,sim1,t1)= ymigr_t(h,hp,t1) ;
 resy_migr(h,sim1,t1) = y_migr(h,t1);

*----------------------------------
* remittances: based on bilateral net migration  - manipulate hohosh(h,hp)

*Stock of migrants
 mig_net(fmig_group,h,hp) =  fsim_i(fmig_group,h,hp) - fsim_i(fmig_group,hp,h);
 mig_stock(fmig_group,h,hp,t1)= mig_stock(fmig_group,h,hp,t1-1)*(1-deprec_mig)+ mig_net(fmig_group,h,hp) ;
 
*net migration:
  mig_stock(fmig_group,h,hp,t1)$(  mig_stock(fmig_group,h,hp,t1) lt 0) = 0.0;
 
 hohosh_mig(f,hp,h)$(FSI0(hp,f) AND sum(fmig_group$map_f_fmig(f,fmig_group), fsi_afterMig(hp,fmig_group,t1))) =
                                                    sum(fmig_group$map_f_fmig(f,fmig_group),mig_stock(fmig_group,h,hp,t1)
                                                        /fsi_afterMig(hp,fmig_group,t1) )*sh_remit;
                                
 reshohosh_mig(f,hp,h,sim1,t1)=  hohosh_mig(f,hp,h) ;
 
*also adjustment in model.gms HOHOEQ
display "after mig" FSI.l;
*-------------------------------
 
 




















