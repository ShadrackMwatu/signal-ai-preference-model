$TITLE DEMETRA v1.0-alphaMacro Baseline

*------- 2. Declare and Assign Parameters  ------------------------

*----- Parameters for capital updating

*---- 1e. Declare Parameters for Dynamic Updating

Parameter

 macro_BL(t,mbas)     Baseline GDP data for sims with updates to SAM base data

 numt(t)              year number
 numtotal             total number of years
 gr_macro(mbas)       growth rates for macro variables
 gr_lab(ins,ff)       growth rates for labor types by institution

 ;

*----- Loading data and sets from Excel

*- Convert Excel workbook data to GDX here

*----- 1a. Load sets from GDX data file

$GDXIN %gdxF%\BaU_in.GDX

*- Sets for macro baseline
$LOADdc mbas

*- Data for macro baseline
$LOADdc gr_macro


$GDXIN


*------- 2. Declare and Assign Parameters  ------------------------

*------ Parameters for Baseline

$ontext

 Assign baseline values for updates using growth rate defined in baseline
 data need to define the baseline over sim because later will use the
 assignments for each of the simulations (i.e. included in addition to the
 policy shocks

$offtext

*----- Macro growth

 numt(t)              = ORD(t) ;
 numtotal             = CARD(t) ;

$ontext
 macro_BL(t,"bgdp")   = GDP0 * (1 + gr_macro("bgdp"))**(numt(t) - 1) ;

 macro_BL(t,"binv")   = INVEST0 * (1 + gr_macro("binv"))**(numt(t) - 1) ;

 macro_BL(t,"bsav")   = TOTSAV0 * (1 + gr_macro("bsav"))**(numt(t) - 1) ;

$offtext
 macro_BL(t,"bgdp")   = GDP0 (1+gr_macro("bgdp",t)) ; 

 macro_BL(t,"binv")   = INVEST0 * (1+gr_macro("binv",t)) ;
                        
 macro_BL(t,"bsav")   = TOTSAV0 * (1+gr_macro("bsav",t)) ;

*----- Factor Market Growth (non-capital)

Parameters
 macro_l(mbas)        Solution values for the macro total ;

 macro_l("bgdp")     = GDP.L ;

 macro_l("binv")     = INVEST.L ;

 macro_l("bsav")     = TOTSAV.L ;


Execute_Unload  '%gdxF%\baseline_shocks.gdx',

        macro_BL, mbas, gr_macro

   ;


