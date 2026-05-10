*------------------------------------------------------------------------------
*-------------------------------------------------------------------------------
*--   JRC.DEMETRA  v1.0-alpha
*--   Dynamic Equilibrium Model for Economic developmenT, Environement & Agriculture
*--
*--   GAMS file : dynamic.inc
*--
*--   @purpose  : 
*--   @author   :
*--   @date     :
*--   @since    :
*--   @refDoc   :
*--   @seeAlso  :
*--   @calledBy :
*-------------------------------------------------------------------------------
*-------------------------------------------------------------------------------

*-------------------- DEMETRA basic closure ---------------------------------
$ontext
  This is a minimal neo classical closure

                     CONDITION

     FEX        - Exchange rate flexible
                - KAPWOR fixed

     Investment - absorption share fixed

     Government - absorption share fixed
                - Tax rates                            - ALL Fixed
                - CAPGOV fixed

     Factors    - Land sector - mobile & full
                - Capital - mobile & full
                - Unskilled labour - mobile & full
                - Skilled labour - mobile & full

     Numeraire  - CPI

It is assumed that the closures used for experiments will be set in the
experiment files.
$offtext

*-## FOREIGN EXCHANGE MARKET CLOSURE
$ontext
 In this MODEL
 EITHER the exchange rate is fixed and the current account balance is the
 equilibrating variable,
 OR the current account balance is fixed and the excahnge rate is the
 equilibrating variable.

 Import prices are always fixed BUT export prices can be determined via an
 export demand function; control via the set cedn.
$offtext

* ERX.FX            = ERX0 ;

* ER.FX("row")            = ER0("row") ;

*- alternatively the external balance is fixed
*- NB CAPWOR is expressed in WORLD CURRENCY UNITS hence numeraire shock via ER

* KAPWOR.FX         = KAPWOR0 ;
 KAPREG.FX(w)  = KAPREG0(w) ;

*- Fixing of world prices
 PWM.FX(c)        = PWM0(c) ;
 PWE.FX(c)$SUM(w,cedn(c,w))     = PWE0(c) ;

*-## INVESTMENT-SAVINGS CLOSURE
$ontext
 IF Aggregate investment is determined by aggregate savings,
 i.e., the model is savings driven, then fix ALL of SADJ, SHADJ, SEADJ,
 DSHH, DS and DSEN.

 IF the model is investment driven only one of SADJ, SHADJ, SEADJ, DSHH,
 DS or DSEN should be variable.

 MULTIPLICATIVE adjustment
 SADJ variable - h'hold and enterprise savings rates vary equiproportionately
 SHADJ variable - h'hold savings rates vary equiproportionately
 SEADJ variable - enterprise savings rates vary equiproportionately

 ADDITIVE adjustment
 DS variable - selected h'hold and enterprise savings rates vary
 DSHH variable - selected h'hold savings rates vary
 DSEN variable - selected enterprise savings rates vary

 For investment driven closures the 'level' of investment can be defined
 in terms of the volume, value or share of final demand expenditure.
$offtext

*- Savings Rate adjustments

*- SADJ.FX          = SADJ0 ;
 SHADJ.FX         = SHADJ0 ;
 SEADJ.FX         = SEADJ0 ;

 DSHH.FX          = DSHH0 ;
 DS.FX            = DS0 ;
 DSEN.FX          = DSEN0 ;

*- Investment 'level' adjustments

*- IF the model is investment driven fix the investment scaling factor

* IADJ.FX       = IADJ0 ;

 IADjTy.FX(i) = IADJTySIM(i,t1,sim1);

* QINV.FX(i)    = qinvb(i) ;

*- INVSH_I.FX(i) = INVSH_I0(i) ;

*  INVEST.FX       = INVEST0  * mod_cont("numerchk") ;
*- INVESTSH.FX     = INVESTSH0 ;

*- Closure rule for Government savings is part of the Govt Closure Rules

*-## ENTERPRISE CLOSURE RULES
$ontext
 ONE of the volume, value or share of final demand should be fixed
$offtext

 QEDADJ.FX        = QEDADJ0 ;
*- VED.FX(e)        = VED0(e)  * mod_cont("numerchk") ;
*- VEDSH.FX(e)      = VEDSH0(e) ;

*- Enterprise transfers to households

 HEADJ.FX        = HEADJ0 ;

*-## GOVT CLOSURE RULES
$ontext
 IF ALL tax rates are fixed AND Government consumption expenditures
 and transfers are fixed
 the equilibriating variable is Government Savings

 IF a tax rate is variable then an alternative equilibriating variable
 is required.

 Note that the tax rates can be varied multiplicatively or additively
$offtext

*- Tax rate scaling factors

 TEADJ.FX(w)         = TEADJ0(w) ;
 TMADJ.FX(w,c)      = TMADJ0(w,c) ;
 TSADJ.FX         = TSADJ0 ;
 TVADJ.FX         = TVADJ0 ;
 TYFADJ.FX        = TYFADJ0 ;
 TXADJ.FX         = TXADJ0 ;
 TFADJ.FX         = TFADJ0 ;
 TYHADJ.FX        = TYHADJ0 ;
 TYADJ.FX         = TYADJ0 ;
 TYEADJ.FX        = TYEADJ0 ;

 DTE.FX(w)           = DTE0(w) ;
 DTM.FX(w)           = DTM0(w) ;
 DTS.FX           = DTS0 ;
 DTV.FX           = DTV0 ;
 DTX.FX           = DTX0 ;
 DTF.FX           = DTF0 ;
 DTYF.FX          = DTYF0 ;
 DTYH.FX          = DTYH0 ;
 DTY.FX           = DTY0 ;
 DTYE.FX          = DTYE0 ;

*- ETAX.FX        = ETAX0     ;
*- MTAX.FX        = MTAX0     ;
*- STAX.FX        = STAX0     ;
*- DTAX.FX        = DTAX0     ;
*- FYTAX.FX       = FYTAX0    ;
*- ITAX.FX        = ITAX0     ;
*- FTAX.FX        = FTAX0     ;
*- VTAX.FX        = VTAX0     ;

*- Government expenditure scaling factor
*- EITHER the volume, value or share of final demand should be fixed

* QGDADJ.FX= QGDADJ0 ;
*- VGD.FX   = VGD0  * mod_cont("numerchk") ;
*- VGDSH.FX = VGDSH0 ;
 YGADJ.FX = YGADJ0;

*- Government transfers scaling factors are fixed

 HGADJ.FX         = HGADJ0 ;
 DHOGOV.FX        = DHOGOV0 ;
 EGADJ.FX         = EGADJ0 ;

*- alternatively the internal balance / Govt savings can be fixed

 KAPGOV.FX       = KAPGOV0 * mod_cont("numerchk") ;

*-## FACTOR MARKET CLOSURE

*-# Basic Factor Market Closure
$ontext
 ALL factors are fully employed and mobile
$offtext

*- Factor supplies by institution (FSI) are fixed
*  FSIA(ins,f)=FSI0(ins,f);
* to de-activate all migration-related equations, FSI is fixed over all factors, replacing the statement above
 FSI.FX(ins,f) = FSI.L(ins,f) ;
* FSI.FX(ins,f) = FSIA(ins,f) ;
* FSI.FX(ins,f)$(NOT fsia(ins,f))        = 0.0 ;
* POPN.FX(h) = POPN0(h) ;


*-- EF_CES unfreeze WFDIST for intermediate consumption moved into CES
*-- and fix WF:

 WFDIST.FX(f,a)$(not k(f))          = WFDIST0(f,a) ;
 WF.FX(fc)               = WF0(fc) ;
 WF.LO(f)                = -inf ;
 WF.UP(f)                = +inf ;

$ontext
This section fixes capital by activity
Uses:
  1.  When running the comparative static mode in short-run scenarios

  2.  When implementing the putty-clay option in the recursive dynamic mode
$offtext

*-- Capital of all types (k) fixed by activity (a)

*- Allow adjustment via WFDIST; therefore free up WFDIST(k,a)

 WFDIST.LO(k,a)  = -inf ;
 WFDIST.UP(k,a)  = +inf ;


*- Fix quantities of capital by activity
*- done in the cap update file

* FD.FX(k,a)      = FDA(k,a) ;

*- Fix average wage rate for capital

 WF.FX(k)        = WF0(k) ;


*-land cannot move between regions

* WFDIST.LO(n,a)  = -inf ;
* WFDIST.UP(n,a)  = +inf ;

*- Fix quantities of land by activity
* FD.FX(n,a)      = FD0(n,a) ;

*- Fix average wage rate for land
* WF.FX(n)        = WF0(n) ;

*-this is required for unemployment specification to work
 WF.LO(ff)$UNEMP0(ff)         = WF0(ff) * mod_cont("numerchk") ;
 WF.UP(ff)$UNEMP0(ff)         = + INF ;


*- # Technology Closures for Factor Market
$ontext

$offtext
*- Technology for CES production functions for Level 1 of production nest

* ADXADJ.FX(a)        = ADXADJ0(a) ;
* DADX.FX          = DADX0 ;

*- Technology for CES aggregation functions for Level 2 of production nest

* ADVAADJ.FX       = ADVAADJ0 ;
* DADVA.FX         = DADVA0 ;

*- Technology for factor activity and region specific factor efficiency

 ADFD.FX(ff,a)     = ADFD.L(ff,a) ;
 ADFH.FX(ff,h)  = ADFH0(ff,h) ;
* ADFH.LO(l,h)$FSI0(h,l)   = -inf ;
* ADFH.UP(l,h)$FSI0(h,l)   = +inf ;

*--efficiency varaiable for aggregate factors
 ADFAGfADJ.FX(ff) = ADFAGfADJ0(ff)  ;
 ADFAGaADJ.FX(a)  = ADFAGaADJ0(a)  ;
 ADFAGADJ.FX      = ADFAGADJ0    ;

 ADFAGfADJ.lo("fva") = -inf ;
 ADFAGfADJ.up("fva") = +inf ;
 ADFAGfADJ.l("fva") = ADFAGfADJ0("fva")  ;
 ADFExt.FX(ff,a)$(NOT mu_extSIM(ff,a,t1,sim1))=ADFExt0(ff,a);

*-## GDP

 GDP.FX            = GDP0 * mod_cont("numerchk")  ;
*- GDP.FX            = GDP_bl  ;

*-## MISCELLANEOUS FIXED VARIABLES
$ontext

$offtext
*- To use CPI as the numeraire fix CPI

* CPI.FX            = CPI0 * mod_cont("numerchk") ;

*- To fix the real exchange rate fix ER and PPI

 PPI.FX           = PPI0 * mod_cont("numerchk") ;


 PQDDIST.fx(c,a)= pqddist0(c,a);
 QINTD.FX(c,a) $(not SAM(c,a)) = 0.00;
 FD.FX(ff,a)$(NOT FD0(ff,a))  = 0       ;
 WF.FX(ff)  $(NOT FC(FF))     = WF0(ff) ;
 TF.FX(ff,a) $(NOT FC(FF))    = TF0(ff,a) ;
 ADFD.FX(ff,a)$(NOT FC(FF))    = 1.0 ;

*---------------END of DEMETRA basic closure ---------------------------------
