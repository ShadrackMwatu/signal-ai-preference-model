$ontext
--------------------------------------------------------------------------------
 JRC.DEMETRA  v1.0-alpha
 Dynamic Equilibrium Model for Economic developmenT, Environement & Agriculture

 GAMS file : data_Load.inc
 @purpose  : Load data from excel files
 @author   :
 @date     :
 @since    :
 @refDoc   :
 @seeAlso  :
 @calledBy :
--------------------------------------------------------------------------------
$offtext

*-------------------- DEMETRA data load file --------------------------------
$ontext
 This file:
    a) controls the sets and data that are read into the model
    b) conditions a range of sets etc., that determine certain
       characterisitics of the model.

 To implement the actions controlled by this file the user needs to generate:
    1) An Excel workbook that contains the following worksheets
         'Layout'      - contains information used by GDXXRW
*-~~ Sets
         'Sets'        - all model sets except those defined from data
         'Maps'        - provides links between different but related accounts
*-~~ Model control
         'controls'    - parameters & sets to control model structure & flow
*-~~ Data
         'sam'         - the SAM for the model
         'factuse'     - quantities of factors used by activities
         'popn'        - population (optional)
         'ue_rate'     - unemployment rates
*-~~ Elastcities
         'comelast'    - elasticities defined by reference to commodities
         'actelast'    - elasticities defined by reference to activities
         'hoelast'     - income elasticities of demand for households
         'hoceselast'  - CES elastcities for nested utility functions
         'frischelast' - frisch elasticities for LES
         'hmigelast'   - household migration elasticities
         'fmobelast'   - factor mobility elastcities




         'exp_sets'    - sets used to control experiments
         'res_sets'    - sets used in analyses of results


    2) An optional GDX file that contains data not provided in Excel format
         SAM          - the SAM for the model
         Factuse      - quantities of factors used by activities
         popn         - population (optional)

 If the SAM is large, or the data are readily available in GDX, it can
be easier to read in the SAM directly from GDX.

NOTE: When loading empty sets and parameters (including parameters with only
zeroes), it is important to initialise those variables explicitly.

*-#### 1. DATA  ENTRY SECTION ########
    *---- 1a. Excel workbook sets and data converted to gdx here
          In the statement
          $CALL "GDXXRW i=[filename].xls o=data_in.gdx INDEX=LAYOUT!A4"
          the user replaces [filename] with the Excel filename
    *---- 1b. All data, elasticities and sets from excel are assigned here
          There should be no need to make changes here unless the model
          is being changed.
          * 1bi. Loading a SAM from Excel via GDX
          * 1bii. Loading a SAM and data from GDX (optional)
    *---- 1c. Defining SETS by exclusions from previously defined SETS
          There should be no need to make changes here unless the model
          is being changed.
    *---- 1d. Defining MAPPING SETS by using subset information
          There should be no need to make changes here unless the model
          is being changed.
    *---- 1e. Assign elements of fmig and inswmig based on mapping sets
          These assignments depend on the mapping sets
    *---- 1f. Initial SAM check

*-#### 2. DATA ADJUSTMENTS SECTION ########

    *---- 2a. Data-specific SAM adjustments
          Requires the inclusion of data specific code, and example is
          ($INCLUDE) smod5_adjust.inc
    *---- 2b. Standard SAM adjustments
          Adjusting the SAM to avoid common data problems that do not affect
          model behaviours
    *---- 2c Adjusting satellite accounts to ensure consistency

*-#### 3. DATA SCALING AND INITIAL CHECKS SECTION ########

    *---- 3a. Automatic Scaling of SAM
          This instruction works by successively increasing the samscal
          parameter as multiples of 10 WHILE a given proportion
          - mod_cont("scalprop") - of the SAM entries are below a given
          target - mod_cont("scaltarg").
            mod_cont("scalprop") and mod_cont("scaltarg") are set in the
            Excel worksheet 'controls'.
              The suggested default values for mod_cont("scalprop") and
              mod_cont("scaltarg") are 0.95 and 100.

    *---- 3b. Entering and Scaling of FACTUSE
    *---- 3c. Scaling any Other Transactions
    *---- 3d. Recalculating Account TOTALS, including grand total

*-#### 4. FINAL CHECK ON MODEL DATA ########

      Programme ABORTS if
      "Totals Check failed - Check SAM after adjustments" ;

*-#### 5. OTHER SET ASSIGNMENTS ########

    *---- 5a. Assign set members for unskilled labour by exclusion
    *---- 5b. Defining sets to control production nesting structure
          This includes a control over the minimium share of inputs costs
          due to intermediate inputs for a top level CES function
    *---- 5c. Defining sets to control aggregation commodities
    *---- 5d. Defining sets to control CET on output based
              on multi-vs. single prod
    *---- 5e. Parameters for defining sets based on commodity share size

*-#### 6. OTHER ELASTICITY ASSIGNMENTS ########

    This section is used to override specific elasticities set in Excel
    *---- 6a. Defining elasticities for export demand
    *---- 6b. Elasticities for commodity output

$offtext

*- ------- 1. Converting XLSX File to GDX File -----------------------------
$ontext
  1) Convert the data to gdx format.
        The resultant GDX file should contain
        a) all sets for the model;
        b) all transactions data, i.e., SAM,
        c) all factor quantity data, i.e., FACTUSE
        d) all elasticity data
        e) parameters to control model structure and flow
        e) parameters to control experiment and closure options
        f) sets used in the experiment files
        h) sets used to analyse and report results.

 The output filename - data_in.gdx - MUST NOT be changed since it is used
 in several places.

$offtext

*-#### 1. DATA  ENTRY SECTION ########

*----- 1a. Excel workbook sets and data converted to gdx here

$CALL "GDXXRW i=%dataf%\%data% o=%gdxF%\data_in.gdx index=Layout!A4"

*----- 1b. All data, elasticities and sets from excel are assigned here

$GDXIN %gdxF%\data_in.gdx

$LOADdc sac

$LOADdc cc c cagr cliv cnat cfd cfs cind cuti cener crenw ccon cinf cser cpub clei cagg ccer cfv ceh cext
$LOADdc cag cles cces
$LOADdc m mw
$LOADdc a aagr aliv anat afd aind aener atrn auti acon aser apdm alei aagg anch anchN aleon
$LOADdc ff fc f fag l k n nirr ls lm lu fseed ffert unempRate0
$LOADdc g gt
$LOADdc tff
$LOADdc insw insg ins
* -$LOAD inswmig
$LOADdc h hrur
$LOADdc e
$LOADdc i w

$LOADdc ss

$LOADdc road ceduc cheal

$LOADdc mcons fcons

$LOADdc map_f_tff map_tff_f map_cag_c map_hh_alei

$LOADdc NT prodNest map_NT_a
$Loaddc cGovAgr iGovAgr fGovAgr aGovAgr iGov fRev aRev


*-$LOADdc fmig
$LOADdc map_f_i  map_f_c map_fag_a_leo  map_fag_NT_leo map_mtax_w map_etax_w

*-result and strcut sets
$GDXIN

*- 1bi. Loading other data from Excel via GDX

$GDXIN %gdxF%\data_in.gdx

*- Transactions
$LOADdc sam


*- Factors
$LOADdc factuse 

*- Elasticities data
$LOADdc elastc elastx elasty elastfd elastces elastmu elastExdem

*- Nutrition elements and values
$LOADdc nutelem nutTable

*- Control data
$LOADdc flow_cont mod_cont


$GDXIN


*- Initialise empty parameters

*- (currently none)

*- 1bii. Loading a SAM and data from GDX
*- If the SAM is a gdx file it can be read in here - NOT a preferred option

*-$ontext
*-$GDXIN ????.gdx

*-$LOADdc ????

*-$GDXIN
*-$offtext


*----- 1c. Defining SETS by exclusions from previously defined SETS

*- SAM Accounts excluding totals
 sacn(sac)      = YES ;
 sacn("total")  = NO ;

*- ASAM Accounts excluding totals

 ssn(ss)        = YES ;
 ssn("totals")  = NO ;

 in(i)          = YES ;
 in("i-s")      = NO ;

*----- 1d. Defining MAPPING SETS by using subset information

*- Mapping from commodities to aggregate commodities

 map_cagg_c("cagr",c)$(cagr(c))     = YES ;
 map_cagg_c("cnat",c)$(cnat(c))     = YES ;
 map_cagg_c("cfd",c)$(cfd(c))       = YES ;
 map_cagg_c("cind",c)$(cind(c))     = YES ;
 map_cagg_c("cuti",c)$(cuti(c))     = YES ;
 map_cagg_c("ccon",c)$(ccon(c))     = YES ;
 map_cagg_c("cser",c)$(cser(c))     = YES ;
 map_cagg_c("clei",c)$(clei(c))     = YES ;

*- Mapping from activies to aggregate activities
 map_aagg_a("aagr",a)$(aagr(a))     = YES ;
 map_aagg_a("aliv",a)$(aliv(a))     = YES ;
 map_aagg_a("anat",a)$(anat(a))     = YES ;
 map_aagg_a("afd",a)$(afd(a))       = YES ;
 map_aagg_a("aind",a)$(aind(a))     = YES ;
 map_aagg_a("auti",a)$(auti(a))     = YES ;
 map_aagg_a("acon",a)$(acon(a))     = YES ;
 map_aagg_a("aser",a)$(aser(a))     = YES ;
 map_aagg_a("atrn",a)$(atrn(a))     = YES ;
 map_aagg_a("apdm",a)$(apdm(a))     = YES ;
 map_aagg_a("alei",a)$(alei(a))     = YES ;

*----- 1f. Initial SAM check

*- Perform an initial SAM totals check

PARAMETER
 SAM0CHK           Check that row and column totals are equal
 SAM0CNT           Count the unblanaced accounts
;

 SAM0CHK(SACN)    = SUM(sacnp , SAM(sacn, sacnp))
                    - SUM(sacnp , SAM(sacnp, sacn)) ;

 SAM0CHK(sacn)$(ABS(SAM0CHK(sacn) lt mod_cont("toldiffsam")))
                    = 0 ;

 SAM0CNT  = SUM(sacn$ SAM0CHK(sacn), 1) ;


 ABORT $(SAM0CNT GT 0)
                  "Totals Check failed - Check Base SAM" ;

*-#### 2. DATA ADJUSTMENTS SECTION ########

*----- 2a. Data-specific SAM adjustments

*----- 2b. Standard SAM adjustments
*- Adjusting the SAM to avoid common problems that do not affect model

*- Eliminating transactions between accounts and themselves

 SAM(sac,sac)        = 0 ;

*- Net transactions between domestic institutions and ROW

 SAM(h,w)            = SAM(h,w) - SAM(w,h) ;
 SAM(w,h)            = 0 ;
 SAM(e,w)            = SAM(e,w) - SAM(w,e) ;
 SAM(w,e)            = 0 ;
 SAM(g,w)            = SAM(g,w) - SAM(w,g) ;
 SAM(w,g)            = 0 ;
 SAM(i,w)            = SAM(i,w) - SAM(w,i) ;
 SAM(w,i)            = 0 ;

*- Net transfers between domestic non-govt institutions and govt

 SAM(h,"govert")       = SAM(h,"govert") - SAM("govert",h) ;
 SAM("govert",h)       = 0 ;
 SAM(e,"govert")       = SAM(e,"govert") - SAM("govert",e) ;
 SAM("govert",e)       = 0 ;

*----- 2c Adjusting satellite accounts to ensure consistency

*- Forcing FSI0 and FD0 to be consistent


*-#### 3. DATA SCALING AND INITIAL CHECKS SECTION ########

*----- 3a. Automatic Scaling of SAM

$ontext
AUTOMATIC CALCULATING OF A SCALING FACTOR - samscal

This instruction works by successively increasing the samscal parameter as
multiples of 10 WHILE a given proportion - mod_cont("scalprop") - of the
SAM entries are below a given target - mod_cont("scaltarg").

The conditional statement is computed as follows
Denominator - the total number of non zero cells in the SAM(sacn,sacnp)
Numerator - the total number of cells in SAM(sacn,sacnp) that are
            i)  non zero cells; AND
            ii) whose absolute values when divided by the current value of
                samscal are less that the target.

The ABORT statement protects against illegal values of scaltarg
$offtext

*- Assigning values to initialise scaling parameter

 samscal            = mod_cont("samscal") ;

 ABORT $(mod_cont("scaltarg") LE 0.0)
 "samautoscaltarg is less than or equal to ZERO - set to positive value" ;

WHILE(
 ((SUM((sacn,sacnp)$(SAM(sacn,sacnp)
            AND (ABS(SAM(sacn,sacnp)/samscal)
              < mod_cont("scaltarg"))),1))
        /SUM((sacn,sacnp)$SAM(sacn,sacnp), 1)) < mod_cont("scalprop") ,

*-     samscal is increased in multiples of 10 until the condition is satisfied
      samscal = samscal * 10;
  ) ;


*- Scale the SAM data for algorithm performance
 SAM(sac,sacp)$samscal  = SAM(sac,sacp)/samscal ;

*- eliminate infinitesimal numbers from the SAM
SAM(sac,sacp)$(ABS(SAM(sac,sacp)) LT 1E-8)=0;



*----- 3b. Entering and Scaling of FACTUSE

*- Remove factuse where there is no corresponding SAM payment
 factuse(f,a)$(not SAM(f,a)) = 0 ;
* factuse(f,a) = SAM(f,a) ;

*- By default set factor use scaling factor equal to SAM scaling factor

 factscal       = samscal ;
* factscal       = 1 ;

*- scale the factor supply  & demand

 factuse(f,a)$factscal   = factuse(f,a)/factscal ;

*- Declare factuse from SAM if neccessary

 factuse(f,a)$((NOT factuse(f,a)) AND SAM(f,a)) = SAM(f,a) ;


*----- 3e. Recalculating Account TOTALS, including grand total

 SAM("total",sac)    = SUM(sacn, SAM(sacn,sac));
 SAM(sac,"total")    = SUM(sacn, SAM(sac,sacn));

*-#### 4. FINAL CHECK ON MODEL DATA ########

*- Recompute SAM account totals

 SAM(sacn,"total")      = 0.0 ;
 SAM("total",sacn)      = 0.0 ;

 SAM(sacn,"total")      = SUM(sacnp, SAM(sacn,sacnp)) ;
 SAM("total",sacnp)     = SUM(sacn, SAM(sacn,sacnp)) ;

*- Perform a SAM totals check after adjustments

 SAM0CHK(SACN)    = SUM(sacnp , SAM(sacn, sacnp))
                    - SUM(sacnp , SAM(sacnp, sacn)) ;

 SAM0CHK(sacn)$(ABS(SAM0CHK(sacn) lt mod_cont("toldiffsam")))
                    = 0 ;

 SAM0CNT  = SUM(sacn$ SAM0CHK(sacn), 1) ;

 ABORT $(SAM0CNT GT 0)
                  "Totals Check failed - Check SAM after adjustments" ;


*-#### 5. OTHER SET ASSIGNMENTS ########

*----- 5a. Assign set members for unskilled labour by exclusion

*- lu(l)          = (NOT ls(l)) AND (NOT lm(l));

*----- 5b. Defining sets to control production nesting structure
$ontext
  The set aqxn(a) - activities with Leontief at the top level is set as
     the complement to aqx(a,r)

Selecting aqx
 a) All activities WITH intermediate inputs where intermediates account
    for more than the value share set in Excel worksheet 'controls'
    are assigned to aqx.
 b) Selected members of a in aqx are cancelled - use the set aleon.
 c) Other members of a in aqx are cancelled manually.

Setting aqxn
    Defined as the complement to aqx.

$offtext

*- Top level CES chosen by reference to intermediate input shares

*- aqx(a)$((SUM(c,SAM(c,a))/SAM("total",a)) GT mod_cont("minaqxsh") )
*-                  = YES ;

 aqx(a)           = YES ;

*- Top level CES canceled for selected activities

 aqx(aleon)       = NO ;

*- Top level CES canceled for selected activities manually

*- aqx("amines")   = NO ;

*- Top level Leontief set for all activities without top level CES

 aqxn(a)         = not aqx(a) ;

*----- 5c. Defining sets to control aggregation commodities

*- Linear aggregation of homogenous commodities

*- cxac(c)         = YES ;
*- cxac(cagr)      = NO ;

*- cxacn(c)        = not cxac(c) ;


*----- 5d. Defining sets to control CET on output based on multi-vs. single prod
$Ontext
 The main issue that makes the CET controls problematic is that the shares
 are defined over a and c, but sets are defined over a. All of the below is
 just ways to get the dimensions consistent and should probably be revised and
 tidied up. This works for now.
$offtext

*-* Need this share parameter for set control - the same as ioqxacqx
Parameter
comsh(a,c)       share of commodity in activity output      ;

 comsh(a,c)$SUM(cp,SAM(a,cp))
               = SAM(a,c)/SUM(cp,SAM(a,cp)) ;


*-Parameters for defining sets based on multi- vs. single product
Parameter
 actprod(a,c)     output by commodity of single product activities
 actprods(a)      output of single product activities ;


 actprod(a,c)$(comsh(a,c)=1) =  comsh(a,c)*SUM(cp,SAM(a,cp)) ;

 actprods(a)                 =  SUM(c,actprod(a,c)) ;


*----- 5e. Parameters for defining sets based on commodity share size
Parameter
 CETcutoff     CET cutoff value for commodity shares
 bigcsh(a,c)   commodity shares larger than cutoff for multiprod activities
 bigc(a)       multiprod activities with commdy shares larger than cutoff ;

 CETcutoff  =  mod_cont("mincetsh") ;

 bigcsh(a,c)$(comsh(a,c)<>1)                               = comsh(a,c) ;
 bigcsh(a,c)$(bigcsh(a,c) LT CETcutoff)                    = 0  ;
 bigcsh(a,c)$(sum(cp,bigcsh(a,cp)) LT sum(cp,comsh(a,cp))) = 0 ;

 bigc(a)                      = SUM(c,bigcsh(a,c)) ;


*-#### 6. OTHER ELASTICITY ASSIGNMENTS ########

$ontext
NB: If the values for elasticities of substitution and/or transformation
    are set here they OVERRIDE the values set in the Excel database.
$offtext

*----- 6a. Defining elasticities for export demand

*-Syntax example
*- elastc("cmines","exdem")    = 0.5 ;



*----- 6b. Elasticities for commodity output

*-Syntax example
*- elastc("cmines","sigmaxc")    = 0.5 ;

*----- 7. Production Nest Structure

Set
map_fag_ff_a(ff,ff,a) Production nest structure for each activity
map_fag_ffall_a(ff,ff,a) Production nest structure for each activity (full depth with all children)
map_a_ftop(a,ff)       Top nest in each activity
;

*-find the top nest
map_a_ftop(a,fag)

*---        this sum maps NT to activity
         $SUM(NT$map_NT_a(NT,a),

*---        this sum checks if fag exists on columns of prodnest
                 (SUM(ff$prodNest(NT,ff,fag),1)

*---        this sum checks of fag does not exists on the rows of prodnest
                  AND (NOT SUM(ff$prodNest(NT,fag,ff),1))))=YES;


map_fag_ff_a(fag,ff,a)$SUM(NT$map_NT_a(NT,a),prodNest(NT,ff,fag))=YES;

*-initialize the set
map_fag_ffall_a(fag,ff,a)=map_fag_ff_a(fag,ff,a);

*-complete recursively
WHILE((SUM((ffp,a)$((SUM(ff$map_fag_ffall_a(ff,ffp,a),1) GT 0)
                                  AND
                    (SUM(ff$(map_a_ftop(a,ff) AND map_fag_ffall_a(ff,ffp,a)),1) EQ 0)),1)),

        map_fag_ffall_a(ff,ffp,a)$SUM(ffpp$(map_fag_ffall_a(ff,ffpp,a) AND map_fag_ffall_a(ffpp,ffp,a)),1)=YES;
      );


SET map_c_f_a(cc,ff,a) mapping between commodities and factor accounts for int inp under VA nest ;
map_c_f_a(c,fc,a)$(SUM(NT$map_NT_a(NT,a),map_f_c(fc,c,NT)))=YES;
*map_c_f_a(ch,fc,a)$(not map_a_c(a,ch))=NO;

SET map_c_fag(ff,c,a);
map_c_fag(fag,c,a)=SUM(fc$map_c_f_a(c,fc,a),map_fag_ff_a(fag,fc,a));

map_fag_a_leo(fag,a)$SUM(NT$map_NT_a(NT,a),map_fag_NT_leo(fag,NT)) = YES;

* Introduce CES possibility to any NEST
aqx1(fag,ff,a)$map_fag_ff_a(fag,ff,a)  = yes;
aqx1(fag,ff,a)$(map_fag_ff_a(fag,ff,a) AND map_fag_a_leo(fag,a)) = NO;

aqx1n(fag,ff,a) $map_fag_ff_a(fag,ff,a)=  not aqx1(fag,ff,a);

*--------------------- end of DEMETRA data load file -------------------------


