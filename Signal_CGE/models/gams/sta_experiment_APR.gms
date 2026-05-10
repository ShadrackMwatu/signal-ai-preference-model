* ======= DEMETRA Experiment file ===========================================
$ontext
Kenya: r=00_save\KENBase s=00_save\KENExp gdx=10_gdx\KENExpDebug rf=00_save\KENExpRef solvelink=5 cerr=5
Senegal: r=00_save\SENBase s=00_save\SENExp gdx=10_gdx\SENExpDebug rf=00_save\SENExpRef solvelink=5 cerr=5
Ghana: r=00_save\GHABase s=00_save\GHAExp gdx=10_gdx\GHAExpDebug rf=00_save\GHAExpRef solvelink=5 cerr=5
CIV: r=00_save\CIVBase s=00_save\CIVExp gdx=10_gdx\CIVExpDebug rf=00_save\CIVExpRef solvelink=5 cerr=5
Ethiopia: r=00_save\ET_Base s=00_save\ET_Exp gdx=10_gdx\ETExpDebug rf=00_save\ETExpRef solvelink=5 cerr=5

$offtext

* ------- 1. Declare and Assign Simulation Set ---------------------------

*- set experiment file name
*$SETGLOBAL calibDatFile experiment_ET.xlsx
*$SETGLOBAL calibDatFile experiment_TZA.xlsx
*$SETGLOBAL calibDatFile experiment_TZA_HPHC.xlsx
$SETGLOBAL calibDatFile experiment_KENv17.xlsx
*$SETGLOBAL calibDatFile experiment_KENSmall.xlsx
*$SETGLOBAL calibDatFile experiment_GHA.xlsx
*$SETGLOBAL calibDatFile experiment_SEN.xlsx
*$SETGLOBAL calibDatFile experiment_CIV.xlsx
*$SETGLOBAL calibDatFile experiment_NGA.xlsx
*$SETGLOBAL calibDatFile experiment_NER.xlsx

*-this is added to the result file names
$SETGLOBAL Mode sta

$SETGLOBAL exp TEST

*- this is the standard set elements for the results files
$SETGLOBAL resElem clos,sim

*-this is used to write the results in every iteration of loop
$SETGLOBAL resElem1  %resElem%1
$SETGLOBAL resElemBs  clos,"base"

*-this is required for per capita welfare calculations
*popn.fx(h)=popn0(h);

* By including a "base case" in the SIM set a comparator is produced

SETS
* Sets for simulations
 sim          simulations
 sim1(sim)    simulations actually done

* Sets for closures
 closelem     Sets for experiment closures
 clos         Set of sets of closure rules for each experiment

 elst         elasticities    /elst1/

;

$SETGLOBAL samNo 3
$INCLUDE 30_Calibration\samchk_decl.inc

*---- 1a. Load sets from GDX data file
$CALL "GDXXRW i=%dataF%\%calibDatFile% o=%gdxF%\exp_in.gdx INDEX=LAYOUT!A4"
$GDXIN %gdxF%\exp_in.gdx

* Sets to control simulations
$LOAD sim sim1

* Sets to control closure rule selection
$LOAD clos

* Sets for results
*$LOAD adjres scalres

$GDXIN


* ------- 2. Declare and Assign experiment parameters -------------------

*---- 2a. Declare experiment parameters
*---Experiment sets

*load scenario parameters
$GDXIN %gdxF%\exp_in.gdx

Parameter
prl  parallel mode (0=NO & 1=YES) /0/

*---productivity shocks
ADFDSIM(ff,a,sim)       increase in factor efficiency
ADVASIM(a,sim)          increase in total factor efficiency

*--- shocks to overall productivity
adxbSIM(a,sim)          Shift parameter for CES production functions for QX
adxEndo(a)              adx calculated by the model from the fertilizer scenario
dabadxSIM(a,sim)        Change in base shift parameter on functions for QX
adx01SIM(a,sim)         0-1 par for flexing of shift parameter on functions for QX

*--- shocks to productivity of top VA nest
advabSIM(a,sim)         Shift parameter for CES production functions for QVA
dabadvaSIM(a,sim)       Change in base shift parameter on functions for QVA
adva01SIM(a,sim)        0-1 par for flexing of shift parameter on functions for QVA

*---shock to productivity of CES nest ff
adfagbSIM(ff,a,sim)     Shift parameter for ff nest at all levels of production nest
dadfagSIM(ff,a,sim)     Change in base shift parameter for land-water aggr at all levels of production nest
ADFAGfADJSIM(ff,sim)    Scaling Factor for Shift parameter for factors on land-water nest
ADFAGaADJSIM(a,sim)     Scaling Factor for Shift parameter for activities on land-water nest
ADVAADJASIM(a,sim)      Scaling Factor for Shift parameter on CES functions for QVA

*---shocks to intermediate input use efficiency
ioqtdqdSIM(c,a,sim)     Intermediate input output coefficients

*-- shocks productivity of commodity Output
adxcSIM(c,sim)          Shift parameter for commodity output CES aggregation

*-- shocks CET output functions (preference shift)
rhotiSIM(a,sim)         Substitution parameter for Armington CET function (preference shift in Armington)
atiSIM(a,sim)           Shift parameter for Armington CET function
gammaiSIM(a,c,sim)      Share parameter for Armington CET function

gammaSIM(c,sim)         Export suply elasticity for Armington CET

*-factor shocks : requires closure swap
FDSIM(ff,a,sim)         Factor demand in simulations
FSSIM(ff,sim)           Factor supply in simulations
FSISIM(insw,ff,sim)     Factor supplies from institution insw by factor f in sim

*-government spending
QGDADJSIM(SIM)          Government consumption demand scaling factor
HGADJSIM (SIM)          Scaling factor for government transfers to households
EGADJSIM (SIM)          Transfers to enterprises by government Scaling Factor
qgdconstSIM(c,SIM)      Government consumption  level
*-enterprise spending
QEDADJSIM(SIM)          Enterprise demand volume Scaling Factor
HEADJSIM (SIM)          Scaling factor for enterprise transfers to households

*-macro vars: find and add explanations
ERSIM(w,SIM)            Exchange rate
KAPWORSIM(SIM)          Foreign saving
KAPGOVSIM(SIM)          Government saving
GOVWORSIM(w,SIM)        Government transfers from abroad
PWMSIM(c,SIM)           World import price
PWESIMSIM(c,SIM)        World export price

*-saving shifters: both HH and ENT
SADJSIM (SIM)           Savings rate scaling factor
DSSIM(SIM)              Partial household and enterprise savings rate scaling factor

*- HH saving shifters
SHADJSIM(SIM)           Savings rate scaling factor for households
DSHHSIM(SIM)            Partial household savings rate scaling factor
dabshhSIM(h,SIM)        Change in base Household saving rates
shh01SIM(h)             0-1 par for potential flexing of Household saving rates

*-enterprise saving
SEADJSIM(SIM)           Savings rate scaling factor for enterprises
DSENSIM(SIM)            Partial enterprise savings rate scaling factor
dabsenSIM(h,SIM)        Change in base Enterprise saving rates
sen01SIM(h)             0-1 par for potential flexing of Enterprise saving rates

IADJSIM(SIM)            Investment adjustment
INVESTSIM(SIM)          Investment
INVESTSHSIM(SIM)        Investment share

*-other tax related shocks: requires closure swap

*---tax shocks

TEADJSIM(w,sim)         Export taxes on exported commy c
TMADJSIM(w,c,sim)       Tariff rates on imported commy c
TSADJSIM(sim)           Sales tax rate
TEXADJSIM(sim)          Excise tax rate
TVADJSIM(sim)           Value added tax rate
TXADJSIM(sim)           Indirect tax rate
TFADJSIM(sim)           Tax rate on factor use
TYFADJSIM(sim)          Direct tax rate on factor income
TYHADJSIM(sim)          Direct tax rate on households
TYADJSIM(sim)           Direct tax rate on households
TYEADJSIM(sim)          Direct tax rate on enterprises
TSSIM(c,sim)            Sales tax rates
TVSIM(c,sim)            VAT tax rates
DABTVSIM(c,SIM)         VAT on commodity c

DTESIM(w,SIM)           Adjustment for Export taxes on exported commy c
DTMSIM(w,SIM)           Adjustment for Tariff rates on imported commy c
DTSSIM(SIM)             Adjustment for Sales tax rate
DTVSIM(SIM)             Adjustment for Excise tax rate
DTEXSIM(SIM)            Adjustment for Value added tax rate
DTXSIM(SIM)             Adjustment for Indirect tax rate
DTFSIM(SIM)             Adjustment for Tax rate on factor use
DTYFSIM(SIM)            Adjustment for Direct tax rate on factor income
DTYHSIM(SIM)            Adjustment for Direct tax rate on households
DTYSIM(SIM)             Adjustment for Direct tax rate on all incomes
DTYESIM(SIM)            Adjustment for Direct tax rate on enterprises

ETAXSIM(SIM)            Revenue from Export taxes on exported commy c
MTAXSIM(SIM)            Revenue from Tariff rates on imported commy c
STAXSIM(SIM)            Revenue from Sales
DTAXSIM(SIM)            Revenue from Direct
EXTAXSIM(SIM)           Revenue from Excise
FYTAXSIM(SIM)           Revenue from Tax on factor use
ITAXSIM(SIM)            Revenue from Indirect tax
FTAXSIM(SIM)            Revenue from Direct tax
VTAXSIM(SIM)            Revenue from VAT
CPISIM(SIM)             CPI
PPISIM(SIM)             PPI

DABTFSIM(ff,a,SIM)      Change in factor tax on activities
DABTMSIM(w,c,SIM)       Change in tariff on comm c imported from region w
DABTESIM(c,w,SIM)       Change in export tax on comm c imported from region w

TMSIM(w,c,sim)          Tariff on comm c imported from region w
QESIM(c,sim)            Exports qunatities
QERSIM(c,w,sim)         Exports by region

*-other sims
HOWORSIM(h,w,sim)       Household remittances
KAPREGSIM(w,sim)        Foreign investment
ioqttqqSIM(m,c,sim)     Trade margins
;



*---set initial values to base level for all parameters
*---tax shocks
TEADJSIM(w,sim)     = TEADJ0(w)     ;
TMADJSIM(w,c,sim)   = TMADJ0(w,c)   ;
TSADJSIM(sim)       = TSADJ0        ;
TVADJSIM(sim)       = TVADJ0        ;
TXADJSIM(sim)       = TXADJ0        ;
TFADJSIM(sim)       = TFADJ0        ;
TYFADJSIM(sim)      = TYFADJ0       ;
TYHADJSIM(sim)      = TYHADJ0       ;
TYADJSIM(sim)       = TYADJ0        ;
TYEADJSIM(sim)      = TYEADJ0       ;
TSSIM(c,sim)        =  tsb(c)       ;
TVSIM(c,sim)        =  tvb(c)       ;
DABTVSIM(c,SIM)     = DABTV(c)      ;

*---productivity shocks

ADFDSIM(ff,a,sim)   = ADFD0(ff,a)   ;
adfagbSIM(ff,a,sim) = adfagb(ff,a)  ;
dadfagSIM(ff,a,sim) = dadfag(ff,a)  ;
ADFAGfADJSIM(ff,sim)= ADFAGfADJ0(ff);
ADFAGaADJSIM(a,sim) = ADFAGaADJ0(a) ;
ioqtdqdSIM(c,a,sim) = ioqtdqd(c,a)  ;
adxcSIM(c,sim)      = adxc(c)       ;
rhotiSIM(a,sim)     = rhoti(a)      ;
atiSIM(a,sim)       = ati(a)        ;
gammaiSIM(a,c,sim)  = gammai(a,c)   ;
ADVAADJASIM(a,sim)  = 1             ;

gammaSIM(c,sim)     = gamma(c)      ;
FDSIM(ff,a,sim)     = FD0(ff,a)     ;
FSSIM(ff,sim)       = FS0(ff)       ;
FSISIM(ins,f,sim)   = FSI0(ins,f)   ;

QGDADJSIM(SIM)      = QGDADJ0       ;
HGADJSIM (SIM)      = HGADJ0        ;
EGADJSIM (SIM)      = EGADJ0        ;
qgdconstSIM(c,SIM)  = qgdconst(c)   ;

QEDADJSIM(SIM)      = QEDADJ0       ;
HEADJSIM (SIM)      = HEADJ0        ;

*-macrovars: might require closure swap
ERSIM(w,SIM)        = ER0(w)        ;
KAPWORSIM(SIM)      = KAPWOR0       ;
KAPGOVSIM(SIM)      = KAPGOV0       ;
GOVWORSIM(W,SIM)    = GOVWOR(w)     ;
PWMSIM(c,SIM)       = PWM0(c)       ;
PWESIMSIM(c,SIM)    = PWE0(c)       ;
KAPREGSIM(w,sim)    = KAPREG0(w)    ;

*-HH and enterprise saving scaling
SADJSIM (SIM)       = SADJ0         ;
DSSIM(SIM)          = DS0           ;

*- HH saving shifters
SHADJSIM(SIM)       = SHADJ0        ;
DSHHSIM(SIM)        = DSHH0         ;
dabshhSIM(h,SIM)    =dabshh(h)      ;
shh01SIM(h)         =shh01(h)       ;

*-enterprise saving shifters
SEADJSIM(SIM)       = SEADJ0        ;
DSENSIM(SIM)        = DSEN0         ;
dabsenSIM(h,SIM)    =dabshh(h)      ;
sen01SIM(h)         =shh01(h)       ;

IADJSIM(SIM)        = IADJ0         ;
INVESTSIM(SIM)      = INVEST0       ;
INVESTSHSIM(SIM)    = INVESTSH0     ;

DTESIM(w,SIM)       = DTE0(w)       ;
DTMSIM(w,SIM)       = DTM0(w)       ;
DTSSIM(SIM)         = DTS0          ;
DTVSIM(SIM)         = DTV0          ;
DTXSIM(SIM)         = DTX0          ;
DTFSIM(SIM)         = DTF0          ;
DTYFSIM(SIM)        = DTYF0         ;
DTYHSIM(SIM)        = DTYH0         ;
DTYSIM(SIM)         = DTY0          ;
DTYESIM(SIM)        = DTYE0         ;

ETAXSIM(SIM)        = ETAX0         ;
MTAXSIM(SIM)        = MTAX0         ;
STAXSIM(SIM)        = STAX0         ;
DTAXSIM(SIM)        = DTAX0         ;
FYTAXSIM(SIM)       = FYTAX0        ;
ITAXSIM(SIM)        = ITAX0         ;
FTAXSIM(SIM)        = FTAX0         ;
VTAXSIM(SIM)        = VTAX0         ;

DABTFSIM(ff,a,SIM)  = DABTF(ff,a)   ;
DABTMSIM(w,c,SIM)   = DABTM(w,c)    ;
DABTESIM(c,w,SIM)   = DABTE(c,w)    ;

CPISIM(SIM)         = CPI0          ;
PPISIM(SIM)         = PPI0          ;

TMSIM(w,c,sim)      = tmb(w,c)      ;

QESIM(c,sim)        = QE0(c)        ;

ioqttqqSIM(m,c,sim) = ioqttqq.L(m,c)  ;


*-- --- 2b. Assign experiment parameters
*Domestic financing (domestic resource mobilization)
*-- tmsim(c,"base") = 0.00 * tm0(c) ;
*TMSIM(w,cagr,"test")   = 1.10*tmb(w,cagr)       ;

*TSSIM("c_petr","test")        =  1.16*tsb("c_petr")     ;
*TSSIM("c_mach","test")        =  -tsb("c_mach")*0.1075  ;

*TVSIM("c_petr", "vat")         =  0.08*tvb("c_petr")     ;
*TVADJSIM("vat")       = TVADJ0*0.16        ;
*TMSIM(w,"c_fert","test")   = 0.00*tmb(w,"c_fert")       ;

*TMSIM(w,"c_mach","test")   = 0.00*tmb(w,"c_mach")       ;
*TMSIM(w,"c_whea","test")   = 0.00*tmb(w,"c_whea")       ;
*TMSIM(w,"c_rice","test")   = 0.00*tmb(w,"c_rice")       ;

*DABTVSIM("c_petr","vat")   = 0.16;

*Simulation for international support through reduction in world inport prices for machinery; petr is likely to increase with global mitigation measures
PWMSIM("c_petr","test") = PWM0("c_petr") * 1.10        ;
*PWMSIM("c_mach","test")  = PWM0("c_mach") * 0.922613       ;
*dadfagSIM("fcap",a,"test")=adfagb("fcap",a)*0.05;
*dadfagSIM("fcap","a_food","invest")=adfagb("fcap","a_food")*0.06;

*Below assignment is for investments

*KAPREGSIM(w,"KAPWOR")=KAPREG0(w)*1.06;

*Below codes target ech of the 13 sectors
*ADVAADJASIM("a_food","invest")     = 1.06;
*ADVAADJASIM("a_ocrp","invest")     = 1.06;
*ADVAADJASIM("a_livs","invest")     = 1.06;
*ADVAADJASIM("a_text","invest")     = 1.06;
*ADVAADJASIM("a_oman","invest")     = 1.06;
*ADVAADJASIM("a_elec","invest")     = 1.06;
*ADVAADJASIM("a_cons","invest")     = 1.06;
*ADVAADJASIM("a_hotl","invest")     = 1.06;
*ADVAADJASIM("a_tran","invest")     = 1.06;
*ADVAADJASIM("a_comm","invest")     = 1.06;
*ADVAADJASIM("a_fsrv","invest")     = 1.06;
*ADVAADJASIM("a_educ","invest")     = 1.06;
*ADVAADJASIM("a_osrv","invest")     = 1.06;

Parameter
closSwap(sim) parameter for sim specific closure swaps

;

 closSwap(sim)           = 0 ;



$INCLUDE 60_Report\resparm.inc

* ------- 4. Expclos loop  -----------------------------------------

* ------- 4a. Declaring Parameters for Closure ----------------------------

* Load closures from xls
$ontext
$GDXIN %gdxF\data_in.gdx
$LOAD closelem expclos closure
$GDXIN
$offtext


* ------- 5. Implementing Closure Changes --------------------------------
$include 40_Dynamics\reset.inc
*$INCLUDE 50_Closure\bclose_sta.inc
$INCLUDE 50_Closure\base.inc

$Setglobal simcount 0

* ------- 6. sim loop begins ---------------------------------------------


LOOP(sim1,
$INCLUDE 30_Calibration\varinit.inc
* ------- 7. Shocks implemented ------------------------------------------
* ... SHOCKS HERE ...

tmb(w,c) = TMSIM(w,c,sim1)  ;
tsb(c)  = TSSIM(c,sim1);
tvb(c) =  TVSIM(c,sim1);
PWM.FX(c) = PWMSIM(c,sim1) ;


*dadfag(ff,a)=dadfagSIM(ff,a,sim1);
*TVADJ.FX=TVADJSIM(sim1);
*dabtv(c) = DABTVSIM(c,sim1)   ;
*dadfag(ff,a)=dadfagSIM(ff,a,sim1);

*Closure rules for investments
*KAPREG.FX(w)=KAPREGSIM(w,sim1);

*Fixing labour mobility and allowing wage distortions for agricultural activities
*FD.FX(l,aagr)=FD0(l,aagr);
*The below command frees variable WFDIST
*WFDIST.LO(l,aagr)=-INF;
*WFDIST.UP(l,aagr)=+INF;
*WFDIST.L(l,aagr)=WFDIST0(l,aagr);


*Fixing labour mobility and allowing wage distortions for natural resource activities
*FD.FX(l,anat)=FD0(l,anat);
*The below command frees variable WFDIST
*WFDIST.LO(l,anat)=-INF;
*WFDIST.UP(l,anat)=+INF;
*WFDIST.L(l,anat)=WFDIST0(l,anat);

*Fixing labour mobility and allowing wage distortions for industrial activities
*FD.FX(l,aind)=FD0(l,aind);
*The below command frees variable WFDIST
*WFDIST.LO(l,aind)=-INF;
*WFDIST.UP(l,aind)=+INF;
*WFDIST.L(l,aind)=WFDIST0(l,aind);

*Fixing labour mobility and allowing wage distortions for industrial activities
*FD.FX(l,aliv)=FD0(l,aliv);
*The below command frees variable WFDIST
*WFDIST.LO(l,aliv)=-INF;
*WFDIST.UP(l,aliv)=+INF;
*WFDIST.L(l,aliv)=WFDIST0(l,aliv);

*Fixing labour mobility and allowing wage distortions for industrial activities
*FD.FX(l,aser)=FD0(l,aser);
*The below command frees variable WFDIST
*WFDIST.LO(l,aser)=-INF;
*WFDIST.UP(l,aser)=+INF;
*WFDIST.L(l,aser)=WFDIST0(l,aser);

*Below is the closure rule for total factor productivity
*ADVAADJA.FX(a)=ADVAADJASIM(a,sim1)  ;


if(closswap(sim1)=1,
* simulation-specific closure

) ;


* ------- 8. Solve statement ---------------------------------------------

 OPTION DECIMALS = 6 ;
 option MCP      = PATH ;
 option NLP      = CONOPT3;
 option ITERLIM  = 1000 ;

 demetra.optfile=4;
 demetra.HOLDFIXED   = 1 ;
 demetra.TOLINFREP   = 1E-8 ;

 Solve demetra Using MCP ;


* ------- 9. Storing results ---------------------------------------------

$INCLUDE 60_Report\resassign.inc

* ------- 10. Terminating sim and expclos loops ---------------------------

 ) ;


$INCLUDE 60_Report\report.inc

* ============================================ END OF EXPERIMENT CODE FILE


