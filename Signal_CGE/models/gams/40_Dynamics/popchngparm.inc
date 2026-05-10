$TITLE DEMETRA Population change parameter declarations
*------------------------------------------------------------------------------
*-------------------------------------------------------------------------------
*--   DEMETRA v1.0-alpha
*--
*--   GAMS file : popchange.inc
*--
*--   @purpose  : Declares the parameters for population change including migration and demographic evolution
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

*------- 1. Declare Parameters  ------------------------

*---- 1a. Declare Parameters for Population Change

Parameter
*----- 1a1. Parameters for updating demography-driven change
 demog0(h,*)         Initial Demographic structure by age only

 EDUC0(h)         Spending on education
 EDUCR0(h)        Rural Spending on education
 EDUCU0(h)        Urban Spending on education
 mu_ed_l(h)       Elasticity of labor productivity to spending on education
 HEAL0(h)         Health spendings
 mu_he_l(h)       Elasticity of labor productivity to spending on health
 BRATE0(h)        Birth rate
 mu_ed_br(h)      Elasticity of birth rate to spending on education
 DRATE0(h)        Death rate
 mu_he_dr(h)      Elasticity of birth rate to spending on health
 POPN0(h)         Population

 bratep(h)        Education spending-driven changes in birth rates
 dratep(h)        Health spending-driven changes in death rates
 deathp(h)        Overall deaths
 birthp(h)        Overall births

 popchngp(h)      Net population changes due to demographics
 popnp(h)         Population by HH in labour due to demographics (net of migration)
 popp              Total population in labour due to demographics (net of migration)
 popchngrate(h)   Rate changes due to demographics
 poppchngrate     Rate changes due to demographics

 EDUCR(h)         Rural Education spending per HH
 EDUCU(h)         Urban Education spending per HH
 EDUC (h)         Education spending per HH      
 HEAL(h)          Health spending per HH         
 EDUCR0(h)        Initial Rural Education spending per HH
 EDUCU0(h)        Initial Urban Education spending per HH
 EDUC0 (h)        Initial Education spending per HH      
 HEAL0(h)         Initial Health spending per HH

 Trk_educ(h,sim,t1)     Track Education spending per HH
 Trk_heal(h,sim,t1)     Track Health spending per HH
 Trk_deathp(h,sim,t)    Track death rate
 Trk_birthp(h,sim,t)    Track birth rate
 Trk_popchngp(h,sim,t)  Track Net population changes due to demographics
 Trk_popnp(h,sim,t)     Track population by HH in labour due to demographics (net of migration)
 Trk_popp(sim,t)        Track Total population in labour due to demographics (net of migration)
 trk_bratep(h,sim,t)    Track Education spending-driven changes in birth rates
 trk_dratep(h,sim,t)    Track Health spending-driven changes in death rates
 trk_popchngrate(h,sim,t)     Track Rate changes due to demographics
 trk_poppchngrate(sim,t)     Track Rate changes due to demographics
 
 tlagedu                Lag of education effect on birth rate /3/
 tlagheal               Lag of health effect on death rate    /3/

; 
*------- 2. Assign Initial Values to Parameters  ------------------------
POPN0(h) = SUM(l,FSI0(h,l)) ;
popnp(h) = popn0(h) ;
mu_ed_l(h)  = demog0(h,"mu_ed_l");
mu_he_l(h)  = demog0(h,"mu_he_l")  ;
mu_ed_br(h) = demog0(h,"mu_ed_br") ;
mu_he_dr(h) = demog0(h,"mu_he_dr") ;
DRATE0(h)   = demog0(h,"drate")    ;
BRATE0(h)   = demog0(h,"brate")    ;

EDUCR0(hrur) =
*-                      per capita private spending on education
                             SUM(ceduc,QCD0(ceduc,hrur))/popn0(hrur)
*-                      plus per capita government spending
                           + SUM(ceduc,QGD0(ceduc))/popn0(hrur) ;

EDUCU0(hurb) =
*-                      per capita private spending on education
                             SUM(ceduc,QCD0(ceduc,hurb))/popn0(hurb)
*-                      plus per capita government spending
                           + SUM(ceduc,QGD0(ceduc))/popn0(hurb) ;

EDUC0(h) = EDUCR0(h) + EDUCU0(h) ;



HEAL0(h) =
*-                       per capita private spending on education
                             SUM(cheal,QCD0(cheal,h))/popn0(h)
*-                       plus per capita government spending
                           + SUM(cheal,QGD0(cheal))/popn0(h);


 Trk_educ(h,sim1,t1)$(NOT t2(t1)) = EDUC0(h);
 Trk_heal(h,sim1,t1)$(NOT t2(t1)) = HEAL0(h);
 Trk_popnp(h,sim1,t1)$(NOT t2(t1)) = popn0(h);
 Trk_popp (sim1,t1)$(NOT t2(t1)) = sum(h,popn0(h));


*--------- End of Population Change Parameters declaration and init -------

