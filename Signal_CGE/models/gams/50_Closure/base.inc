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
 One of the below 3 is free and the other two must be fixed:
 ERX: Exchange rate index
 ER("reg"): Exchange rate with region reg
 CAPREG("reg"): Current account deficit with region reg
 KAPREG: Total Current account deficit

Notes:
 - To free all exchange rates fix  KAPREG and CAPREG("reg")
 - if ER("reg") is fixed model is still homogenous of deg 0 but large numerchk values might (almost certainly) create
   numerical problems for solution. So check homogenity with small numerchecks. This happens since ERW affect in many income equations etc..
 - If KAPREG and ERX are fixed, trade liberalization can be done only with 1 region
 - If KAPWOR and KAPREG are fixed (trade deficit with both regions are kept fixed) trade liberalization has to be done with all regions
 - Import prices are always fixed BUT export prices can be determined via an
   export demand function; control via the set cedn.
 - If there is only one trade partner in the SAM Then either ERX or one of KAPWOR or KAPREG("reg") can be fixed!
   In this case fixing ERX and fixing ERW("reg") are equilvalent. However fixing ERX will not create numerical problems while fixing ER(w) might.
$offtext

*-exchange rate index = always fixed?
*  ERX.FX = ERX0 * mod_cont("numerchk");
*  ER.FX("row") = ER0("row")* mod_cont("numerchk");
*- alternatively the external balance is fixed
*- NB KAPREG is expressed in WORLD CURRENCY UNITS hence numeraire shock via ER

*  KAPWOR.FX = KAPWOR0;

 KAPREG.FX(w) = KAPREG0(w);

*- Fixing of world prices
 PWM.FX(c)        = PWM0(c) ;
 PWE.FX(c)        = PWE0(c) ;
* PWSE.FX(c)       = PWSE0(c) ;
* PWE.lo(c)=-inf; PWE.up(c)=+inf;
* PWE.FX(c)$sum(w,cedn(c,w))     = PWE0(c) ;

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

 SADJ.FX          = SADJ0 ;
 SHADJ.FX         = SHADJ0 ;
 SEADJ.FX         = SEADJ0 ;

 DSHH.FX          = DSHH0 ;
 DS.FX            = DS0 ;
 DSEN.FX          = DSEN0 ;

*- Investment 'level' adjustments

*- IF the model is investment driven fix the investment scaling factor

* IADJ.FX       = IADJ0 ;
 IADJTy.FX(i)=IADJTy0(i);



*- QINV.FX(i)    = QINV0(i) ;

* INVSH_I.FX(i) = INVSH_I0(i) ;

*-  WALRAS.FX=WALRAS0;

*  INVEST.FX       = INVEST0  * mod_cont("numerchk") ;
*- INVESTSH.FX     = INVESTSH0 ;

*- Closure rule for Government savings is part of the Govt Closure Rules

*-## ENTERPRISE CLOSURE RULES
* ONE of the volume, value or share of final demand should be fixed

 QEDADJ.FX        = QEDADJ0 ;
*- VED.FX(e)        = VED0(e)  * mod_cont("numerchk") ;
*- VEDSH.FX(e)      = VEDSH0(e) ;

*-one of gov income adjuster or governmet income is fixed
   YGADJ.FX = YGADJ0;


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

 TEADJ.FX(w)      = TEADJ0(w) ;
 TMADJ.FX(w,c)    = TMADJ0(w,c) ;
 TSADJ.FX         = TSADJ0 ;
 TVADJ.FX         = TVADJ0 ;
 TYFADJ.FX        = TYFADJ0 ;
 TXADJ.FX         = TXADJ0 ;
 TFADJ.FX         = TFADJ0 ;
 TYHADJ.FX        = TYHADJ0 ;
 TYADJ.FX         = TYADJ0 ;
 TYEADJ.FX        = TYEADJ0 ;


*- DTE.FX(w)        = DTE0(w) ;
*- DTM.FX(w)        = DTM0(w) ;
*- DTS.FX           = DTS0 ;
*- DTV.FX(c)        = DTV0(c) ;
*- DTX.FX           = DTX0 ;
*- DTF.FX           = DTF0 ;
*- DTYF.FX          = DTYF0 ;
*- DTYH.FX          = DTYH0 ;
*- DTY.FX           = DTY0 ;
*- DTYE.FX          = DTYE0 ;

*- ETAX.FX        = ETAX0     ;
*- MTAX.FX        = MTAX0     ;
*- STAX.FX        = STAX0     ;
*- DTAX.FX        = DTAX0     ;
*- EXTAX.FX       = EXTAX0    ;
*- FYTAX.FX       = FYTAX0    ;
*- ITAX.FX        = ITAX0     ;
*- FTAX.FX        = FTAX0     ;
*- VTAX.FX        = VTAX0     ;

   DVTAX.FX = DVTAX0;

*- Government expenditure scaling factor
*- EITHER the volume, value or share of final demand should be fixed

 QGDADJ.FX       = QGDADJ0 ;
*- VGD.FX          = VGD0  * mod_cont("numerchk") ;
*- VGDSH.FX        = VGDSH0 ;


*- Government transfers scaling factors are fixed

 HGADJ.FX      = HGADJ0 ;
 DHOGOV.FX      = DHOGOV0 ;
 EGADJ.FX         = EGADJ0 ;

*- alternatively the internal balance / Govt savings can be fixed

* KAPGOV.FX       = KAPGOV0 * mod_cont("numerchk") ;

*-## FACTOR MARKET CLOSURE

*-# Basic Factor Market Closure
$ontext
 ALL factors are fully employed and mobile
$offtext


*- Factor supplies by institution (FSI) are fixed if ins is not migrating, f is not segemented

* FSI.FX(ins,f)$((NOT fmigin(f) OR NOT inswmigin(ins)) AND (NOT fmigout(f) OR NOT inswmigout(ins)))= FSIA(ins,f) ;
* FSI.FX(ins,f)$((NOT fmigin(f) OR NOT inswmigin(ins)) AND (NOT fmigout(f) OR NOT inswmigout(ins)))= FSI0(ins,f) ;
* FSI.FX(ins,f)$(NOT FSI_PGR0(ins,f))= FSI0(ins,f) ;
* to de-activate all migration-related equations, FSI is fixed over all factors, replacing the statement above
 FSI.FX(ins,f) = FSI0(ins,f) ;

 FSI.FX(ins,f)$(FSI0(ins,f) eq 0.0)        = 0.0 ;

* POPN.FX(h) = POPN0(h) ;


*-- EF_CES unfreeze WFDIST for intermediate consumption moved into CES
*-- and fix WF:

 WFDIST.FX(f,a)          = WFDIST0(f,a) ;
 WF.FX(fc)                = WF0(fc) ;
 WF.LO(f)                = -inf ;
 WF.UP(f)                = +inf ;


*-unemployment & wage are fixed if it is zero
 UNEMP.FX(ff)$(NOT UNEMP0(ff)) =  UNEMP0(ff);

 WF.LO(ff)$UNEMP0(ff)         = WF0(ff) * mod_cont("numerchk") ;
 WF.UP(ff)$UNEMP0(ff)         = + INF ;


$ontext
This section fixes capital by activity
Uses:
  1.  When running the comparative static mode in short-run scenarios

  2.  When implementing the putty-clay option in the recursive dynamic mode
$offtext

*-ontext
*- Capital of all types (k) fixed by activity (a)

*- Allow adjustment via WFDIST; therefore free up WFDIST(k,a)

* WFDIST.LO("capital_land_nirri",a)  = -inf ;
* WFDIST.UP("capital_land_nirri",a)  = +inf ;

*- Fix quantities of capital by activity
* FD.FX("capital_land_nirri",a)      = FD0("capital_land_nirri",a) ;
* FSI.FX(ins,"capital_land_nirri")   = FSI0(ins,"capital_land_nirri") ;
* FS.FX("capital_land_nirri")      = FS0("capital_land_nirri") ;

*- Fix average wage rate for capital
* WF.FX(k)        = WF0(k) ;
*-$offtext

*-land cannot move between regions

* WFDIST.LO(n,a)  = -inf ;
* WFDIST.UP(n,a)  = +inf ;

*- Fix quantities of land by activity
* FD.FX(n,a)      = FD0(n,a) ;

*- Fix average wage rate for capital
* WF.FX(n)        = WF0(n) ;
*-$offtext


*- Technology for factor activity and region specific factor efficiency

 ADFD.FX(ff,a)     = ADFD0(ff,a) ;
 ADFH.FX(ff,h)     = ADFH0(ff,h) ;
* ADFH.LO(l,h)$FSI0(h,l)   = -inf ;
* ADFH.UP(l,h)$FSI0(h,l)   = +inf ;

*--
 ADFAGfADJ.FX(ff)  = ADFAGfADJ0(ff)  ;
 ADFAGaADJ.FX(a)  = ADFAGaADJ0(a)  ;
 ADFAGADJ.FX      = ADFAGADJ0    ;


ADFExt.FX(ff,a)$(NOT mu_ext(ff,a))=ADFExt0(ff,a);


*-## GDP

*- GDP.FX            = GDP0 * mod_cont("numerchk")  ;

*-## MISCELLANEOUS FIXED VARIABLES
$ontext

$offtext
*- To use CPI as the numeraire fix CPI

* CPI.FX            = CPI0 * mod_cont("numerchk") ;

*- To fix the real exchange rate fix ER and PPI

 PPI.FX           = PPI0 * mod_cont("numerchk") ;

 PQDDIST.fx(c,a) = pqddist0(c,a);
 QINTD.FX(c,a) $(not SAM(c,a)) = 0.00;
 FD.FX(ff,a)$(NOT FD0(ff,a))   = 0       ;
 WF.FX(ff)  $(NOT FC(FF))      = WF0(ff) ;
 TF.FX(ff,a) $(NOT FC(FF))     = TF0(ff,a) ;
 ADFD.FX(ff,a)$(NOT FC(FF))    = 1.0 ;


*- agricultural budget adjusters (currently not in the model)
*- gov't consumption adjusters
 QGDADJceh.FX=1;
 QGDADJoth.FX=1;
 QGDADJext.FX=1;
 QGDADJc.FX(c)=0;
*---------------END of DEMETRA basic closure ---------------------------------
