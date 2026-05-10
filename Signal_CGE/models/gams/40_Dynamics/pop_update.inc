$TITLE DEMETRA Population updates
*------------------------------------------------------------------------------
*-------------------------------------------------------------------------------
*--   DEMETRA v1.0-alpha
*--
*--   GAMS file : popchange.inc
*--
*--   @purpose  : Updates population related parameters resulting from migration and demographic evolution
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

*---- 1a. Update Parameters for Population Change

 EDUCR(hrur) =
*-                      per capita private spending on education
                             SUM(ceduc,QCD.L(ceduc,hrur))/popnp(hrur)
*-                      plus per capita government spending
                           + SUM(ceduc,QGD.L(ceduc))/popnp(hrur) ;

 EDUCU(hurb) =
*-                      per capita private spending on education
                             SUM(ceduc,QCD.L(ceduc,hurb))/popnp(hurb)
*-                      plus per capita government spending
                           + SUM(ceduc,QGD.L(ceduc))/popnp(hurb) ;

 EDUC(h) = EDUCR(h) + EDUCU(h) ;
 Trk_educ(h,sim1,t1-1) = EDUC(h);


 HEAL(h) =
*-                       per capita private spending on education
                             SUM(cheal,QCD.L(cheal,h))/popnp(h)
*-                       plus per capita government spending
                           + SUM(cheal,QGD.L(cheal))/popnp(h);

 Trk_heal(h,sim1,t1-1) = HEAL(h);

 
 bratep(h) = brate0(h) ;
 bratep(h)$(ord(t1)>tlagedu) = brate0(h) * (Trk_educ(h,sim1,t1-tlagedu)/EDUC0(h))**mu_ed_br(h) ;
 trk_bratep(h,sim1,t1) = bratep(h);


 dratep(h) = drate0(h) ;
 dratep(h)$(ord(t1)>tlagheal) = drate0(h) * (Trk_heal(h,sim1,t1-tlagheal)/HEAL0(h))**mu_he_dr(h) ;
 trk_dratep(h,sim1,t1) = dratep(h);

 deathp(h) = popnp(h)*dratep(h) ;
 Trk_deathp(h,sim1,t1) = deathp(h);

 birthp(h) =  popnp(h)*bratep(h) ;
 Trk_birthp(h,sim1,t1) = birthp(h);
 
 FSI.FX(h,l)    = FSI.L(h,l)*(1+bratep(h)-dratep(h));

 popchngp(h) = birthp(h) - deathp(h);
 Trk_popchngp(h,sim1,t1) = popchngp(h);

 Trk_popnp(h,sim1,t1)= popnp(h);

 popp = Sum(h, popnp(h));
 Trk_popp(sim1,t1)= popp;
 
 popchngrate(h)      = (1+popchngp(h)/Trk_popnp(h,sim1,t1)-1)*100; 
 trk_popchngrate(h,sim1,t1)  = popchngrate(h);  
 
 poppchngrate               = (1+sum(h,popchngp(h))/Trk_popp(sim1,t1)-1)*100; 
 trk_poppchngrate(sim1,t1)  = poppchngrate;  

 ADFH.FX(l,h)   = ADFH0(l,h)+  ((EDUC(h)/EDUC0(h))**mu_ed_l(h) - 1) + ((HEAL(h)/HEAL0(h))**mu_he_l(h) - 1) ;
* FSI.FX(h,l)    = FSI.L(h,l)*(1+popchngp(h)/Trk_popnp(h,sim1,t1));

 popnp(h) = popnp(h) + popchngp(h);

*-------------------- End of Population Change and Migration Parameter update --
