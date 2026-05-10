$TITLE DEMETRA v1.0-alpha
$OFFUPPER ONEMPTY
*$OFFLISTING OFFSfYMXREF OFFSYMLIST
*------------------------------------------------------------------------------
*------------------------------------------------------------------------------
*-
*-
*-   GAMS file : model.gms
*-
*-   @purpose  : Main Model
*-   @author   :
*-   @date     :
*-   @since    :
*-   @refDoc   :
*-   @seeAlso  :
*-   @calledBy : save file called by experiments
*-   @command  : s=00_save\ET_Base gdx=10_gdx\ETBaseDebug cerr=10 solvelink=5 profile=1 rf=00_save\ETBaseRef
*-   @command  : s=00_save\KEN_Base gdx=10_gdx\KENBaseDebug cerr=10 solvelink=5 profile=1 rf=00_save\KENBaseRef
*------------------------------------------------------------------------------
*------------------------------------------------------------------------------

*-################ GENERAL INFORMATION ####################################
$ontext
DEMETRA (Dynamic Equilibrium Model for Economic Development, Resources and Agriculture)
This programme is developed by the Joint Research Centre JRC.D.4 unit of European Commission.
The technical documentation of the model, use guide and all other documents are available at : https://datam.jrc.ec.europa.eu/datam/model/DEMETRA/index.html

Contact details:
European Commission Joint Research Centre
Directorate For Sustainable Resources
Economics of the Food System
C/ Inca Garcilasso, 3, Edificio Expo, Seville, Spain

Technical Contact:
Emanuele Ferrari  (emanuele.ferrari@ec.europa.eu)

Copyright (c) 2021 European Commission

The DEMETRA model is based on STAGE_DEV:
(Aragie, E. A., McDonald, S., & Thierfelder, K. (2016). A static applied general equilibrium model: Technical documentation: STAGE_DEV Version 2. http://cgemod.org.uk/stg_dev.html).
STAGE DEV has been developed for the European Commission by Aragie, E., McDonald, S., and Thierfleder, K.,
under the supervision of Emanuele Ferrari for the Joint Research Centre (JRC) of the European Commission

DEMETRA is developed by the Joint Research Centre (JRC) of the European Commission

DEMETRA is distributed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) licence (https://creativecommons.org/licenses/by-nc-sa/4.0/)
By accepting the terms of use you are free to:
Share - copy and redistribute the material in any medium or format
Adapt - remix, transform, and build upon the material
Under the following terms:
You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
You may not use the material for commercial purposes.
If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

If you are using or have a copy of this programme without having accepted all the terms of use you are in breach of the copyright.
This programme and all related files should be deleted from your PC, etc., immediately and no copy should be kept.

Do NOT remove this notice even if you are using this programme with agreement.
$offtext
*-------------------------------------------------------------------------------

*################ MODEL DEVELOPMENT NOTES ###########################
$ontext
Developed by the Joint Research Centre of the European Commission, the Dynamic Equilibrium Model for Economic development Resources and Agriculture (DEMETRA) is a single-country computable general equilibrium (CGE) model, developed in GAMS.
The JRC employs DEMETRA within the framework of the Pan African Network on the economic Analysis of Policies (PANAP) - https://datam.jrc.ec.europa.eu/datam/area/PANAP.
DEMETRA investigates the economy-wide and distributional impacts of specific policies and/or structural shocks, sectoral transmission of sector-specific policies for sectors, agents and regions. In particular, DEMETRA can carry out model can be employed to produce ex-ante impact analyses mainly of food security related topics.

The key model features are:
- Flexible CES nesting of production functions - the user can modify the definition and nesting of production technologies for each productive activity, without changing the model code, eliminating thus the risk of errors and mis-specifications of CES production functions
- Flexible CES-LES nesting of household demand systems - in the same spirit as for production functions, the user can define and group consumption goods
- Home production for home consumption whereby non-market (subsistence) production is consumed by the producing household
- International trade modelled through a two-level Armington specification allowing for the consideration of multiple trade partners

The SAMs database and documentation are vailable here: https://datam.jrc.ec.europa.eu/datam/area/PANAP#section-contents
$offtext

*-------------------------------------------------------------------------------
*--  GLOBAL VARIABLES THAT CONTROL FOLDERS AND FILES
*-------------------------------------------------------------------------------
*- These control the names of the folders.
*-------------------------------------------------------------------------------
$SETGLOBAL saveF       00_Save
$SETGLOBAL gdxF        10_gdx
$SETGLOBAL dataF       20_Data
$SETGLOBAL resultF     70_Result

*-------------------------------------------------------------------------------
*--  Data file names
*------------------------------------------------
*- These control the names of the data files. In the code we use %fileName% instead of hardcoding the fileName.
*The SAMs database and documentation are vailable here: https://datam.jrc.ec.europa.eu/datam/area/PANAP#section-contents
*-------------------------------------------------------------------------------

$SETGLOBAL DEMETRA_REG   "KEN"

*$SETGLOBAL data          data_ET_V8.xlsx
$SETGLOBAL data          KEN_SAM_2020.xlsx
*$SETGLOBAL data          data_KEN_V1_small.xlsx
*$SETGLOBAL data          data_GHA_V09.xlsx
*$SETGLOBAL data          data_CIV_V1.xlsx
*$SETGLOBAL data          data_NGA_V2_hphc.xlsx
*$SETGLOBAL data          data_NER_v7_hphc.xlsx
*$SETGLOBAL data          data_TZN_v2_hphc.xlsx
*$SETGLOBAL data          data_TZN_v5_hphc-land-hhreg_fcap_leis_carehrs.xlsx
*$SETGLOBAL data          data_TZN_v7_hphc-land-hhreg_fcap_leis_care.xlsx
*$SETGLOBAL data          data_Senegal_V6.xlsx
*$SETGLOBAL data          data_SouthAfrica_19.xlsx

$SETGLOBAL closureFile   base.inc
*-------------------------------------------------------------------------------
*-SET AND PARAMETERS
*-------------------------------------------------------------------------------
$ontext
 The data are entered in 6 components
  i)     SAM accounts set SAC
  ii)    various subsets of SAC
  iii)   various mapping sets for the model
  iv)    various sets assigned from the data
  v)     sets to control model structure and flow
  vi)    other sets
$offtext

SETS
*-------------------------------------------------------------------------------
*- *- SAM accounts set SAC
*-------------------------------------------------------------------------------
 sac                SAM accounts
*-------------------------------------------------------------------------------
*- *- subsets of SAC
*-------------------------------------------------------------------------------
*-------------------------------------------------------------------------------
*- *- commodities
*-------------------------------------------------------------------------------
 cc(sac)            Commodities and aggregate commodities
 c(cc)              Natural commodity accounts
 cagr(c)            Agricultural Commodities
 cliv(c)            Livestock Commodities
 cnat(c)            Natural Resource Commodities
 cfd(c)             Food Commodities
 cfdh(c)            Commodities consumed by HH as Food
 cfs(c)             Fish Commodities
 cind(c)            Industrial Commodities
 cuti(c)            Utility Commodities
 cener(c)           Energy sectors
 crenw(c)           Renewable Energy sectors (for SDG calculations)
 cfoss(c)           Fossil fuel Energy sectors (for SDG calculations)
 ccon(c)            Construction Commodities
 cinf(c)            Infrastructure Commodities
 cser(c)            Service Commodities
 cpub(c)            Public Service Commodities for migration
 clei(c)            Leisure commodities
 cagg               Aggregate commodity groups for reporting
 ceh(c)             rural education and health commodities (that affect labor productivity)
 cext(c)            extension commodities
 coth(c)            commodities that are not related to current consumption with agricultural budget

***Emissions***
 cener_ghg(c)       Combustion-related commodities
 / /
 NCO                Non-combustion emissions
       / CO2Eq,CO2,CH4, N2O, C2F6, C3F8, C4F10, C5F12, C6F14, CC4F8, CF4, HCFC141b, HCFC142b, HFC125, HFC134, HFC134a, HFC143,
       HFC143a, HFC152a, HFC227ea, HFC23, HFC236fa, HFC245fa, HFC32, HFC365mfc, HFC41, HFC4310mee, NF3, SF6, BC, CO, NH3,
       NMVOC, NOX, OC,PM10, PM2_5, SO2 /
************
 cag(cc)            Aggregate commodities for utility function
 cles(cc)           Commodities and aggregates in the LES utility
 clesn(cc)          Commodities and aggregates NOT in the LES utility
 cces(cc)           Commodities in the CES function
 ccesn(cc)          Commodities NOT in the CES function
 ccesn1(cc)         Commodities NOT Leisure NOT in the CES function

 ccer(c)            Cereals (for SDG calculations)
 cfv(c)             Fruits and vegetables (for SDG calculations)

 m(sac)             Margins
 mw(m)              Export Margins
 md(m)              Domestic Margins
*-------------------------------------------------------------------------------
*- *-activities
*-------------------------------------------------------------------------------
 a(sac)             Activities
 aagr(a)            Agricultural Activities
 aliv(a)            Livestock Activities
 anat(a)            Natural Resource Activities
 afd(a)             Food Activities
 aind(a)            Industrial Activities
 aener(a)           Enercg Activities
 atrn(a)            Transportation Activities
 auti(a)            Utility Activities
 acon(a)            Construction Activities
 aser(a)            Service Activities
 alei(a)            Leisure activities
 apdm(a)            Public service activities
 aagg               Aggregate activity groups

 anch(a)            Anchor activity for fixing 1 WFDIST in various factor closures
 anchN(a)           Anchor activity for fixing 1 WFDIST in land factor closures

 aleon(a)           Activities with Leontief prodn function at Level 1
*-------------------------------------------------------------------------------
*- factors
*-------------------------------------------------------------------------------
 ff(sac)            factors and aggregates
 fc(ff)             natural factors and intermediates under VA nest
 f(ff)              natural factor accounts
 fag(ff)            aggregate factors
 fseed(ff)          seed factors
 ffert(ff)          fertilizer factors
 l(f)               Labour Factors
 ls(l)              Skilled Labour Factors
 lm(l)              Skilled or Unskilled Labour Factors
 lu(l)              Unskilled Labour Factors
 lRuUs(l)           Rural uskilled labor factor
 k(f)              Capital Factors
 n(f)              Land Factors
 nirr(f)           Irrgated land factors
*-------------------------------------------------------------------------------
*- Institutions
*-------------------------------------------------------------------------------
 insw(sac)          Domestic Institutions and Rest of World
 insg(insw)         Domestic Institutions including Government
 ins(insg)          Domestic Non Government Institutions

 h(ins)             Households
 hrur(h)            Rural households
 hurb(h)            Urban households
 hrow(h)            Foreing labor households
 g(sac)             Government
 gt(g)              Government tax accounts
 tff(gt)            Factor tax account used in GDX program
 tln(g)             Factor tax account used in GDX program

 e(ins)             Enterprises

 i(sac)             Investment
 in(i)              Investment categories excluding i_s
 iGov(i)            Investment categories in government budget

 w(insw)            Rest of the world
*-------------------------------------------------------------------------------
*- *- leisure
*-------------------------------------------------------------------------------
 clein(c)           NON leisure commodities
 alein(a)           NON leisure activities
*-------------------------------------------------------------------------------
*- *- Declaring SETS assigned from the data
*-------------------------------------------------------------------------------
 ce(c)              export commodities
 ceR(c,w)           export commodities from region w
 cen(c)             Non-export commodities
 ceRn(c,w)          Non-export commodities from region R

 ced(c,w)           export commodities with export demand functions
 cedn(c,w)          export commodities without export demand functions

 cm(c)              imported commodities
 cmR(w,c)           imported commodities from region w
 cmn(c)             non-imported commodities
 cmRn(w,c)          non-imported commodities from region w

 cx(c)              commodities produced domestically
 cxn(c)             commodities NOT produced domestically AND imported

 cxac(c)            commodities that are differentiated by activity
 cxacn(c)           commodities that are NOT differentiated by activity

 cd(c)              commodities produced and demanded domestically
 cdn(c)             commodities NOT produced and demanded domestically

 aqx(a)             Activities with CES aggregation function at Level 1 of nest
 aqxn(a)            Activities with Leontief aggregation function at Level 1 of nest

 aqx1(ff,ff,a)      Activities with CES aggregation function at Level 1 of nest
 aqx1n(ff,ff,a)     Activities with Leontief aggregation function at Level 1 of nest
 acetmp(a)          Multi-product activities
 acetsp(a)          Single product activities

 acetl(a)           Multi-product activities with commodity shares larger than cutoff
 acets(a)           Multi-product activities with commodity shares smaller than cutoff

 acet(a)            Activities with CET function on output
 acetn(a)           Activities without CET function on output
*-------------------------------------------------------------------------------
*- *- Set used to control model structure and flow
*-------------------------------------------------------------------------------
 fcons              set for parameters controlling program flow
 mcons              set for parameters controlling model content
*-------------------------------------------------------------------------------
*- *- Declaring other sets
*-------------------------------------------------------------------------------
 sacn(sac)          SAM accounts excluding TOTAL

 ss                 ASAM categories
 ssn(ss)            ASAM excluding totals

 NT                 production nest type
 prodNest(NT,ff,ff) production nest structure
 map_NT_a(NT,a)     mapping between nest type and activity
*-------------------------------------------------------------------------------
*- *- Sets for structural tables & results
*-------------------------------------------------------------------------------
 structElem1        real and nominal macroeconomic summary totals
 structElem2        imports or exports
 structElem3        commodity account structure
 structElem4        activity account structure
 structElem5        factor use structure


 qles(cc,h)         commodities in LES nest
 qcag(cc,h)         aggregate commodities
 road(i)            road investments
 ceduc(c)           education commodities
 cheal(c)           health commodities
*-------------------------------------------------------------------------------
*- *-sets for agricultural budget
*-------------------------------------------------------------------------------
 cGovAgr(c)         commodities in agri budget
 iGovAgr(i)         investment types in agri budget
 fGovAgr(ff)        subsidized factors with agri budget
 aGovAgr(a)         activities receiving factor subsidies from agri budget
 fRev(ff)           subsidized factors with agri budget via revolving fund
 aRev(a)            activities receiving factor subsidies from agri budget via revolving fund
*-------------------------------------------------------------------------------
*- *- Nutrition elements
*-------------------------------------------------------------------------------
 nutElem(sac)       Nutrition Elements
*-------------------------------------------------------------------------------
*- *- Mapping sets for the model
*-------------------------------------------------------------------------------
 map_f_tff(ff,tff)   Factor taxes to factors
 map_tff_f(tff,ff)   Factor taxes to factors reverse
 map_aagg_a(aagg,a)  Mapping from activies to aggregate activities
 map_cagg_c(cagg,c)  Mapping from commodities to aggregate commodities

 map_f_c(ff,c,NT)    Mapping from natural factors f to commodities
 map_fag_a_leo(ff,a) Activities with Leontieff nest at ff

 map_fag_NT_leo(fag,NT)      Activity groups with Leontieff

 map_cag_c(cc,cc)    Mapping from natural commodities to aggergate commodities

 map_hh_alei(insw,a) Mapping from leisure activities to paired households

 map_f_i(f,i)       Mapping to factors from investments

 map_mtax_w(gt,w)    Mapping between import tax and regions
 map_etax_w(gt,w)    Mapping between export tax and regions
 map_hrow_w(h,w)     Mapping of foreing households to trading regions
 map_ff_qgd(ff,cc)   map between factors and gov't spendings effecting their productivity

 map_c_ceh(c,c)      mapping between commodities for ceh
 map_c_coth(c,c)     mapping between commodities and coth
 map_c_cext(c,c)     mapping betwe3en commodities and cext
;

*- Setting up ALIASES

 ALIAS(sac,sacp,sacpp,sacppp), (sacn,sacnp),
      (cc,ccp), (c,cp,cpp),
      (cag,cagp), (cles,clesp), (clesn,clesnp), (cces,ccesp), (ccesn,ccesnp),
      (cagr,cagrp), (cnat,cnatp), (cfd,cfdp), (cind,cindp),
      (cuti,cutip), (ccon,cconp), (cser,cserp),(cpub,cpubp), (clei,cleip),
      (m,mp),
      (a,ap,app), (aagr,aagrp), (anat,anatp), (afd,afdp), (aind,aindp),
      (auti,autip), (acon,aconp), (aser,aserp), (alei,aleip),
      (fc,fcp), (fag,fagp,fagpp),
      (f,fp,fpp), (ff,ffp,ffpp),
      (ins, insp), (insg,insgp), (insw, inswp),
      (l,lp), (ls,lsp), (lm,lmp), (lu,lup), (k,kp), (n,np)
      (h,hp,hpp), (e,ep), (g,gp), (gt,gtp),
      (tff,tffp), (tln,tlnp), (i,ip), (w,wp),
      (ce,cep), (ced,cedp), (cm,cmp), (cx,cxp), (cxac,cxacp), (cd,cdp),
      (ss,ssp), (ssn,ssnp),
      (NT,NTP),
      (NCO,GHG)

;


*-#### DECLARING PARAMETERS FOR ALL MODEL DATA

*- ------- Declare parameters for data loading ----------------------------

PARAMETER
*-~~~~ DATA parameters

*- Transactions
 SAM(sac,sacp)    the SAM for this model
*- Factors
 FACTUSE(ff,a)    Factor use by activity
 factins(ins,f)   Factor supplies by institution
 unempRate0(ff)   Unemployment rate
*-Nutrition Table
 nutTable(c,nutElem)  nutrition values per unit of commodity
*-~~~~ ELASTICITIES
*- Commodities and Activities
 ELASTC(c,*)       Trade Elasticities indexed on commodities
 ELASTX(a,*)       Production Elasticities indexed on activities
 ELASTEXDEM(c,w)   Export demand elasticities per region
*- Household Demand
 ELASTY(cc,h)      Income Demand Elasticities for households LES function
 ELASTCES(cc,h)    Income Demand Elasticities for households CES function
 ELASTMU(h,*)      Elasticity of the MU of income
*- Production
 ELASTFD(ff,a)     Elasticities for CES Production function level 3
*- Data scaling parameters
 samscal           algorithm performance scaling parameter for SAM
 factscal          algorithm performance scaling parameter for FACTUSE
*- Parameters used to control model flow
 flow_cont(fcons)   values for parameters controlling program flow
 mod_cont(mcons)    values for parameters controlling model content
;

*-############### 5. DATA ENTRY ###########################################

*- ------- Data load include file -----------------------------------------
$ontext
All data and sets are read in using an include file
The output filename - data_in.gdx - should NOT be changed since it is used
in several places.
Adjustments to the data are also made in this file.
$offtext

$INCLUDE 30_Calibration\data_load.inc

singleton set
govert (sac) /govert /
facttax(sac) /facttax/
saltax (sac) /saltax /
vattax (sac) /vattax /
ectax  (sac) /ectax  /
indtax (sac) /indtax /
dirtax (sac) /dirtax /
total  (sac) /total  /
is     (sac) /i-s    /
flivst (f)   / /
;

*-################ 6. ADDITIONAL SET ASSIGNMENT ###########################

*- Define sets on the basis of read in data

 ce(c)$(SUM(w,SAM(c,w)))  = YES ;
 ceR(c,w)$(SAM(c,w))      = YES ;
 cen(c)                   = NOT ce(c) ;
 ceRn(c,w)                = NOT ceR(c,w) ;

 ELASTC(c,"exdem")$(NOT ELASTC(c,"exdem"))     = 0.0 ;

 ced(c,w)$(ELASTEXDEM(c,w) AND SAM(c,w))       = YES ;
 cedn(c,w)                = NOT ced(c,w) ;

 cm(c)$(SUM(w,SAM(w,c)))  = YES ;
 cmR(w,c)$SAM(w,c)        = YES ;
 cmn(c)                   = NOT cm(c);
 cmRn(w,c)                = NOT cmR(w,c);

 cx(c)$(SUM(a,SAM(a,c)))  = YES ;
 cxn(c)                   = NOT cx(c) ;

 ELASTC(c,"sigmaxc")$(NOT ELASTC(c,"sigmaxc")) = 0.0 ;

 cxac(c)$ELASTC(c,"sigmaxc")  = YES ;
 cxacn(c)                     = NOT cxac(c) ;

 cd(c)$( SUM(a,SAM(a,c))
            GT SUM(w,SAM(c,w)
               - SUM(mw,SAM(mw,c))
               - SUM(gt$map_etax_w(gt,w),SAM(gt,c))))
         = YES ;
 cdn(c)  = NOT cd(c) ;

*- Define set for utility functions based on read in sets

 ccesn(c) = NOT cces(c) ;
 ccesn1(c)= NOT cces(c) AND NOT clei(c);


*- Define Commodities consumed by household as food
 cfdh(c)$(SUM(h,SAM(c,h)) AND (cfd(c) OR cagr(c))) = YES;

*- Define rural unskilled labor
 lRuUs(l)$(lu(l) AND SUM(h$hrur(h),SAM(h,l))) = YES;

*- Define urban households
 hurb(h) $(not hrur(h)) = YES;

*- Define foreign labor households
 hrow(h)$(SUM(f,SAM(h,f)) AND (SUM(sac,SAM(h,sac)) LT 1E-8)) = YES;
 map_hrow_w(hrow,w)= NO;
 map_hrow_w(hrow,w)$SAM(hrow,w)= YES;

 qles(c,h)$ccesn(c)      = YES ;

 qcag(cc,h)$cag(cc)      = YES ;

*- Single vs. multiproduct activities
 acetsp(a)$actprods(a)  = YES ;
 acetmp(a)              = NOT acetsp(a) ;

*- Large vs. small commodity shares in multprod activities
 acetl(a)$bigc(a)       = YES ;
 acets(a)$acetmp(a)     = NOT acetl(a) ;


*- CET vs. non-CET activities
$ontext
 CET if elasticity for CET is non-zero and if multi-product firm AND large shares
 Fixed proportions if single product firm or if CET is zero or small shares
$offtext

 ELASTX(a,"omegaout")$(NOT ELASTX(a,"omegaout")) =   0.0 ;
 acet(a)$(ELASTX(a,"omegaout")AND acetmp(a) AND acetl(a))  = YES ;
 acetn(a)   = NOT acet(a) ;

*- Non Leisure commodities and activities
 clein(c)   = NOT clei(c) ;
 alein(a)   = NOT alei(a) ;

*-domestic margins
 md(m)=YES;
 md(m)$mw(m)=NO;

*- govt spending type that effects factor productivities
 map_ff_qgd(fseed,cext) =   YES;
 map_ff_qgd(ffert,cext) =   YES;
 map_ff_qgd(flivst,cext)=   YES;
 map_ff_qgd(l,cext)     =   YES;

 coth(c)                =   YES;
 coth(c)$(ceh(c) OR cext(c) ) = NO;
 cfoss(c)$(cener(c) AND NOT crenw(c)) = YES;

 map_c_ceh(ceh,c)$(SAMEAS(c,ceh)) = YES;
 map_c_coth(coth,c)$(SAMEAS(c,coth) AND NOT (ceh(c) OR cext(c) ) ) = YES;
 map_c_cext(cext,c)$(SAMEAS(c,cext)) = YES;

*-######################## END OF DATA ENTRY ##############################

*-################ 7. DATA DIAGNOSTICS ####################################

$INCLUDE 30_Calibration\diagnost.inc

*-################ 8. MODEL CALIBRATION ###################################
*- Calibration proceeds by the blocks of equations
*- each block contains all the related parameter declarations and assignments

*-################ 8. MODEL CALIBRATION ###################################
*- Calibration proceeds by the blocks of equations
*- each block contains all the related parameter declarations and assignments

$INCLUDE 30_Calibration\parmcalib_decl.inc

$INCLUDE 30_Calibration\parmcalib_assign.inc

* recalibrating emissions coeffiecients and initial emissions levels
$IF EXIST 10_gdx\emissions_Coeff_DEMETRA_%DEMETRA_REG%.gdx $BATINCLUDE 30_Calibration/calibEmissions.inc  "init"

*--#### Various Checks on Calibration: NOW MERGED TO CALIBRATION FILE

*-################ 9. VARIABLE DECLARATION ################################
$ontext
NOTE 1: the default specification of variables in an MCP programme is FREE
NOTE 2: the model uses various POSITIVE variables
         - this ensures that some variables are always positive BUT
             requires the variables are paired with specific equations
         - Use positive variables and MCP constraint
$offtext

Positive Variables

 FSIL(ins,f)            Factor supply for leisure
 FSIM(f,ins,fp,insp)    Number of factors to f from ins by ins
 WFA(ff,a)              Sectoral factor prices (WFxWFDIST)

 Free Variables
*-------------------------------------------------------------------------------
*- TRADE BLOCK
*-------------------------------------------------------------------------------

*-------------------------------------------------------------------------------
*- Exchange Rate Block
*-------------------------------------------------------------------------------
 ERX                Trade weighted overall exchange rate (domestic per partner unit)
 ER(w)              Exchange rate for each trade partner (domestic per partner unit)
*-------------------------------------------------------------------------------
*- Exports Block
*-------------------------------------------------------------------------------
 PWE(c)             World price of exports in dollars
 PER(c,w)           Domestic price of exports from region w
 PE(c)              Domestic price of exports of commodity c
 PD(c)              Consumer price for domestic supply of commodity c

 QE(c)              Exports of commodity c
 QER(c,w)           Domestic output exported to region r
 QD(c)              Domestic demand for commodity c

 ZETAER(c,w)        Preference shifter for exports
 ZETAE(c)           Preference shifter for exports
*-------------------------------------------------------------------------------
*-     Imports Block
*-------------------------------------------------------------------------------
 PWM(c)             World price of imports in dollars
 PM(c)              Domestic price of competitive imports of commodity c
 PMR(w,c)           Domestic price of imports of commodity c from region w

 QM(c)              Imports of commodity c
 QMR(w,c)           Imports of commodity c from region w
 QQ(c)              Supply of composite commodity c

 ZETAM(w,c)         Preference shifter for imports
*-------------------------------------------------------------------------------
*-     TRADE AND TRANSPORT MARGINS BLOCK -
*-------------------------------------------------------------------------------
 PTT(m)             Price of trade and transport margin m
 QTT(m)             Quantity of trade and transport margin m
 QTTD(c)            Intermediate input use for trade and transport margin m
 IOQTTQQ(m,c)       Trade margins

*-------------------------------------------------------------------------------
*-      COMMODITY PRICE BLOCK
*-------------------------------------------------------------------------------
 PQS(c)             Supply price of composite commodity c
 PQD(cc)            Purchaser price of composite commodity c
 PQCD(cc,h)         Purchaser price of aggregate commodity cag by h
 PQC(cc,h)          price paid by consumers for consumed commodities
*-------------------------------------------------------------------------------
*-     NUMERAIRE PRICE BLOCK
*-------------------------------------------------------------------------------
 CPI                Consumer price index
 PPI                Producer (domestic) price index
 VQCD               Value of HH consumption
 COMTOTSH           Share of commodity c in total commodity demand
 VDDTOTSH           Value of domestic output for the domestic market
*-------------------------------------------------------------------------------
*-     PRODUCTION BLOCK ----
*-------------------------------------------------------------------------------
 PX(a)              Composite price of output by activity a
 PVA(a)             Value added price for activity a
 PINT(a)            Price of aggregate intermediate input

 AD(ff,a)           Shift parameter for total efficiency [ADFD*(1+ADFH)]
 ADFD(ff,a)         Shift parameter for factor and activity specific efficiency
 ADFH(ff,h)         Shift parameter for factor and household specific efficiency

 ADFAG(ff,a)        Shift parameter for land-water aggr at all levels of production nest
 ADFAGfADJ(ff)      Scaling Factor for Shift parameter for aggregate factors
 ADFAGaADJ(a)       Scaling Factor for Shift parameter for activities
 ADFAGADJ           Scaling Factor for Shift parameter

 QX(a)              Domestic production by activity a
 QVA(a)             Quantity of aggregate value added for level 1 production
 VVA(a)             Corrected value for Value added (sum of natural factors)
 QINT(a)            Aggregate quantity of intermediates used by activity a
 QINTD(c,a)         Intermediate input demand by activity a for commodity c

 WF(ff)             Price of factor f
 WFDIST(ff,a)       Sectoral proportion for factor prices
 PQDDIST(c,a)       Price distribution parameter for factors coming from int inps
 FD(ff,a)           Demand for factor f by activity a
 FSI(ins,ff)        Factor supplies from institution ins by factor f
 FS(ff)             Supply of factor f
 UNEMP(ff)          Unemployment
 UNEMPRATE(ff)      Unemployment

 PXC(c)             Producer price of composite domestic output
 QXC(c)             Domestic production by commodity c
 PXAC(a,c)          Activity commodity prices
 QXAC(a,c)          Domestic commodity output by each activity
 IOQXACQXV(a,c)     Share of commodity c in output by activity a
*-------------------------------------------------------------------------------
*-     FACTOR BLOCK
*-------------------------------------------------------------------------------
 YF(f)              Income to factor f
 YFDISP(f)          Factor income for distribution after depreciation
 YFINS(f)           Factor income for distribution to domestic non govt institutions

 FSISH(ins,f)       Shares of factor f supplied by institution ins
 INSVA(ins,f)       Factor income after deprecn distribution to institn ins
*-------------------------------------------------------------------------------
*-     HOUSEHOLD BLOCK
*-------------------------------------------------------------------------------
*-------------------------------------------------------------------------------
*-     Household Income
*-------------------------------------------------------------------------------
 YH(h)              Income to household h
*-------------------------------------------------------------------------------
*-    Household Expenditure
*-------------------------------------------------------------------------------
 HOHO(h,hp)         Inter household transfer
 HOWOR(h,w)         Trasnfer of foreign labor households to row
 HEXP(h)            Household consumption expenditure

 QCD(cc,h)          Household consumption by commodity c
 QCD2(cc,cc,h)      Household consumption by com'dy cces used in com'dy cag
*-------------------------------------------------------------------------------
*-     ENTERPRISE BLOCK
*-------------------------------------------------------------------------------
*-------------------------------------------------------------------------------
*-     Enterprise Income
*-------------------------------------------------------------------------------
 YE(e)              Enterprise incomes
*-------------------------------------------------------------------------------
*-     Enterprise Expenditure
*-------------------------------------------------------------------------------
 QEDADJ             Enterprise demand volume Scaling Factor
 HEADJ              Scaling factor for enterprise transfers to households

 HOENT(h,e)         Household Income from enterprise e
 GOVENT(e)          Government income from enterprise e
 QED(c,e)           Enterprise consumption by commodity c
 VED(e)             Value of enterprise e consumption expenditure
*-------------------------------------------------------------------------------
*-     GOVERNMENT BLOCK
*-------------------------------------------------------------------------------
*-------------------------------------------------------------------------------
*-     Government Income Block
*-------------------------------------------------------------------------------
 TE(c,w)            Export taxes on exported commy c
 TM(w,c)            Tariff rates on imported commy c
 TS(c)              Sales tax rate
*-*-*-*-CAUTION*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-
*-THC is a dummy tax type for introducing food aid in the siulations.
*-It cannot exist in the baseline as there is no way to put it in the SAM
*-If you use satelite accounts to introduce it you have to modify model calibration
*-(still I cannot see how this would work). In short THC=0 in the base year.
 THC(h,cc)          HH specific sales tax(for food aid)
*-*-*-*-CAUTION*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-
 TV(cc)             Value added tax rate
 TX(a)              Indirect tax rate
 TF(ff,a)           Tax rate on factor use
 TYF(ff)            Direct tax rate on factor income
 TYH(h)             Direct tax rate on households
 TYE(e)             Direct tax rate on enterprises
*-------------------------------------------------------------------------------
*-     Government Tax Revenues
*-------------------------------------------------------------------------------
 MTAX               Tariff revenue
 ETAX               Export tax revenue
 DTAX               Direct Income tax revenue
 FYTAX              Factor Income tax revenue
 ITAX               Indirect tax revenue
 STAX               Sales tax revenue
 FTAX               Factor use tax revenue
 VTAX               Value added tax revenue
 HCTAX              Household specific comm tax (for food aid)
 DVTAX              Value added tax revenue releaser


 TEADJ(w)           Export subsidy Scaling Factor
 TMADJ(w,cc)        Tarrif rate Scaling Factor
 TSADJ              Sales tax rate scaling factor
 THCADJ             Household specific sales tax scaling factor
 TVADJ              Value added tax rate scaling factor
 TXADJ              Indirect Tax Scaling Factor
 TFADJ              Factor Use Tax Scaling Factor
 TYFADJ             Factor Tax Scaling Factor
 TYHADJ             Household Income Tax Scaling Factor
 TYADJ              Household and Enterprise Income Tax Scaling Factor
 TYEADJ             Enterprise income tax Scaling Factor

 DTE(w)             Partial Export tax rate scaling factor
 DTM(w)             Partial Tariff rate scaling factor
 DTS                Partial Sales tax rate scaling factor
 DTHC               Partial Household specific sales tax
 DTV                Partial value added tax rate scaling factor
 DTX                Partial Indirect tax rate scaling factor
 DTF                Uniform adjustment to factor use tax by activity
 DTYF               Partial direct tax on factor rate scaling factor
 DTYH               Partial direct tax on household rate scaling factor
 DTY                Partial direct tax on hold and enterprise rate scaling factor
 DTYE               Partial direct tax on enterprise rate scaling factor
*-------------------------------------------------------------------------------
*-     Government Income
*-------------------------------------------------------------------------------
 YG                 Government income
 YGADJ              Government income adjuster
*-------------------------------------------------------------------------------
*-     Government Expenditure Block
*-------------------------------------------------------------------------------
 QGDADJ             Government consumption demand scaling factor
 QGDADJc(c)         Commodity level government spending adjuster
 QGDADJceh          Government spending adjuster for education and health commodities in agricultural budg
 QGDADJoth          Government spending adjuster for other commodities in general budget
 QGDADJext          Government spending adjuster for extension commodities in agricultural budget

 HGADJ              Scaling factor for government transfers to households
 HOGOV(h)           Government transfers to HHs
 DHOGOV             Partial governmet transfer scaling factor
 EGADJ              Transfers to enterprises by government Scaling Factor

 QGD(c)             Government consumption demand by commodity c
 VGD                Value of Government consumption expenditure
 EG                 Expenditure by government
 GBUDG              Government budget for current spendings and investments

 AgBuRecurr(c)      Recurrent budget
 AgBuInvest(i)      Investment budget
 AgBuInpSub(ff,a)   Input subsidy budget
 AgBuRevFund(ff,a)  Revolving Fund budget
 AgBuOutSub(a)      Output subsidy budget
 AgBuComSub(cc,h)   Commodity subsidies (i.e. food aid)
 AgBuIncSub(h)      Income subsidies & transfers

 AgBuTotRecurr      Total Recurrent budget
 AgBuTotInvest      Total Investment budget
 AgBuTotInpSub      Total Input subsidy budget
 AgBuTotOutSub      Total Output subsidy budget
 AgBuTotComSub      Commodity subsidies (i.e. food aid)
 AgBuTotIncSub      Income subsidies & transfers
 AgBuTOTALx         Total agricultural budget
 AgBuTOTShr         Share of agricultural budget in total gov't income
*-------------------------------------------------------------------------------
*-     KAPITAL BLOCK
*-------------------------------------------------------------------------------
*-------------------------------------------------------------------------------
*-     Savings Block
*-------------------------------------------------------------------------------
 SHH(h)             Household savings rates
 SEN(e)             Enterprise savings rates

 SADJ               Savings rate scaling factor for BOTH households and enterprises
 SHADJ              Savings rate scaling factor for households
 SEADJ              Savings rate scaling factor for enterprises

 DSHH               Partial household savings rate scaling factor
 DS                 Partial household and enterprise savings rate scaling factor
 DSEN               Partial enterprise savings rate scaling factor

 TOTSAV             Total savings
*-------------------------------------------------------------------------------
*-     Investment Block
*-------------------------------------------------------------------------------
 IADJ               Investment scaling factor
 IADJTy(i)          Investment scaling factor for investment of type i

 QINVD(c,i)         Investment demand by commodity c for investment of type i
 QINV(i)            Investment volume by investment type i

 INVSH_I(i)         Shares of savings to investment of type i

 INVEST             Total investment expenditure
*-------------------------------------------------------------------------------
*-    FOREIGN INSTITUTIONS BLOCK -
*-------------------------------------------------------------------------------
 YFWOR(w,f)         Foreign factor income
*-------------------------------------------------------------------------------
*-    MARKET CLEARING BLOCK
*-------------------------------------------------------------------------------
*-------------------------------------------------------------------------------
*-     Account Closure
*-------------------------------------------------------------------------------
 KAPGOV             Government Savings
 KAPREG(w)          Current account balance with each trade partner
 KAPWOR             Current account balance total
*-------------------------------------------------------------------------------
*-     Absorption Closure
*-------------------------------------------------------------------------------
 VFDOMD             Value of final domestic demand
 INVESTSH           Value share of investment in total final domestic demand
 VGDSH              Value share of Govt consumption in total final domestic demand
 VEDSH(e)           Value share of Ent consumption in total final domestic demand
*-------------------------------------------------------------------------------
*-    Dynamic Variables
*-------------------------------------------------------------------------------
 EXTENS(ff,a)       Extension services consumption
 EXTENSSHR(ff,a)    Share of extension services benefiting to to each factor
 ADFExt(ff,a)       Change in factor productivity due to extension services
*-------------------------------------------------------------------------------
*-    Nutrition
*-------------------------------------------------------------------------------
 NutVal(nutElem,h)  Nutrition indicator values
*-------------------------------------------------------------------------------
*-    GDP
*-------------------------------------------------------------------------------
 GDP                GDP from Expenditure
 RGDP               Real GDP from Expenditure
 RGDPFC             Real GDP at Factor Cost

*-------------------------------------------------------------------------------
*-EMISSION variables
*-------------------------------------------------------------------------------

 CO2EM_Q(c,a)          CO2 emissions by activities from use of fossil energy inputs
 CO2EM_H(c,h)          CO2 emissions by households from consumption of fossil energy goods
 CO2EMIS_Q(a)          Total CO2 emissions from energy use by activities
 CO2EMIS_H(h)          Total CO2 emissions from energy use by households
 CO2EMIS               Total CO2 emissions from combustion

 NCO2EM_Q(NCO,a)        Non-combustive emissions  by activities
 NCO2EM_FS(NCO,c,a)     Non-combustive emission based on fossil fuel combustion in production
 NCO2EM_IO(NCO,c,a)     Process non-combustive emissions based on intermediate demand
 NCO2EM_EN(NCO,f,a)     Non-combustive emissions based on factor use
 NCO2EM_H(NCO,c,h)      Non-combustive emissions  by households

 NCO2EM_FS_SUM(NCO,a)      Non-combustive emission based on fossil fuel combustion in production - total by activity
 NCO2EM_IO_SUM(NCO,a)      Process non-combustive emissions based on intermediate demand - total by activity
 NCO2EM_EN_SUM(NCO,a)      Non-combustive emissions based on factor use - total by activity
 NCO2EM_H_SUM(NCO,h)       Non-combustive emissions  by households - total by household
 NCO2EM_A_SUM(NCO,a)       Non-combustive emissions from all sources by activity - total by activity
 NCO2EM_SUM(NCO)           Non-combustive emissions from differnt sources - total by GHG

 GHGEM                 Total GHG emissions - combustive and non-combustive

*-------------------------------------------------------------------------------
*-    Slack
*-------------------------------------------------------------------------------
 WALRAS             Slack variable for Walrass Law
 OBJ                Dummy var for NLP objective
;


*-################ 10. VARIABLE INITIALISATION ############################
*   This file initialises the variables to their base values.
$INCLUDE 30_Calibration\varinit.inc
$INCLUDE 30_Calibration\calibCheck_decl.inc
$INCLUDE 30_Calibration\calibCheck_assign.inc


*-################ 11. SOCIAL ACCOUNTING MATRICES #########################
$ontext
This section checks that the model is calibrated with a balanced SAM,
by using a Macro and a Micro SAM`.

The MICRO SAM element can be switched off by setting "micsam1" = 0 in the
parameter 'flow_cont' in the worksheet 'controls'

 1) Macro SAM
  The programme aborts IF
           - ROW AND COLUMN SUMS FOR ASAM1 NOT EQUAL
           - ALL ASAM1 CELL ENTRIES DO NOT EQUAL ASAM0 ENTRIES

 2) Micro SAM
  The programme aborts IF
           - ALL SAM1 CELL ENTRIES DO NOT EQUAL SAM0 ENTRIES
$offtext

*-This is used in namimg of SAM check parameters 1= initial check 2=post-solve check

$SETGLOBAL samNo 1
$INCLUDE 30_Calibration\samchk_decl.inc

*-################ 12. STRUCTURAL DESCRIPTION #############################
$ontext
   This section produces various summary macroeconoic statistics and a
series of summary descriptive statistics.
$offtext

$INCLUDE 30_Calibration\struct.inc
*-################ END OF CALIBRATION ######################################

EQUATIONS

*-################ 13. EQUATION DECLARATIONS ###############################
*- ------- TRADE BLOCK ----------------------------------------------------
*- #### Exports Block
 ERXDEF                  Trade weighted overall exchange rate definition
 PERDEF(c,w)             Domestic price of exports to region w by commodity c
 PEDEF(c)                Domestic price of exports by commodity c

 CET(c)                  CET function for domestic production
 ESUPPLY1(c,w)           Export supply function (FOC)
 ESUPPLY2(c)             Export supply function (FOC)
 EDEMAND(c,w)            Export demand function
 CETALT(c)               CET fn for dom prodn with no exports OR only exported
*- #### Imports Block
 PMRDEF(w,c)             Domestic price of competitive imports to region w of commodity c
 ARMINGTON1(c)           First level Armington nest (aggregates composite imports)
 ARMINGTON2(c)           Second level Armington nest (aggregates composite com. supply)
 COSTMIN1(w,c)           FOC for 1st level Armington
 COSTMIN2(c)             FOC for 2nd level Armington
 ARMALT(c)               Comp commody aggn fn with no imports OR no dom prodn
*- ------- TRADE AND TRANSPORT MARGINS BLOCK ------------------------------
 IOQTTQQEVAL(m,c)        Evolution of trade margins based on road investments

 PTTDEF(m)               Price of trade and transport margin m
 QTTDEF(m)               Quantity of trade and transport margin m
 QTTDEQ(c)               Intermediate input use for trade and transport margin m
*- ------- COMMODITY PRICE BLOCK ------------------------------------------
 PQSDEF(c)               Supply price of composite commodity c
 PQDDEF(c)               Purchaser price of composite commodity c
 PQCDDEF(cag,h)          Purchaser price of aggregate commodity cag by h
 PXCDEF(c)               Producer price for composite domestic output
 PQCDEF(cc,h)            definition of price paid by consumers for consumed commodities
 PQCDEF2(cc,h)           definition of price paid by consumers for consumed commodities
*- ------- NUMERAIRE PRICE BLOCK ------------------------------------------
 CPIDEF                  Consumer price index
 PPIDEF                  Producer (domestic) price index
 VQCDDEF(c)              Value of HH consumption
 COMTOTSHDEF(c)          Share of commodity c in total commodity demand
 VDDTOTSHDEF(c)          Share of value of domestic output for the domestic market
*- ------- PRODUCTION BLOCK -----------------------------------------------
 PXDEF(a)                Composite price of output by activity a
*- CES aggregation functions
 QXEQUIL(a)            Production function for QX in activity a level 1 of nest - leontieff
 PVADEF(a)               Value added price for activity a level 1 of nest
 PINTDEF(a)              Aggregate intermed input price for activity a level 1 of nest
 QINTDEF(a)              Leontief intermediate aggregation for Level 1 of nest
 QVADEF(a)               Leontief value added aggregation for Level 1 of nest
 VVADEF(a)               Value of value added (sum of factor values)
 QXDEF(a)               FOC Production function for QVA level 2 of nest
*- CES aggregation functions for generalised production nest
 FDPRODFN(ff,a)          Production function for nested CES function
 FDPRODFN2(ff,a)         Production function for nested CES function
 FDFOC   (ff,ff,a)       FOC for nested CES function
 FDFOC2  (ff,ff,a)       FOC for nested CES function
 WFAGDEF(c,a)            Returns equal to PQD
 ADDEF(ff,a)             Total Efficiency shift parameter
 ADFAGEQ(ff,a)           Shift parameter for aggregate factors
 WFADEF                  Sectoral factor prices
*- Intermediate Input Demand
 QINTDEQ(c,a)            Intermediate input demand by activity a for commodity c
*- Commodity Output
 COMOUT(c)               Domestic differentiated commodity production
 COMOUTFOC(a,c)          FOC for Domestic differentiated commodity production

 COMOUT2(c)              Domestic homogenous commodity production
 COMOUTFOC2(a,c)         FOC for Domestic homogenous commodity production
*- Activity Output
 ACTOUT(a,c)             Domestic activity output
 ACTOUTFOC(a,c)          FOC for domestic activity output
*- ------- FACTOR BLOCK ---------------------------------------------------
 YFEQ(f)                 Factor incomes
 YFDISPEQ(f)             Factor income for distribution after depreciation
 YFINSEQ(f)              Factor income for distribution to domestic non govt institutions

 FSISHEQ(insw,f)         Shares of factor f supplied by institution insw

 INSVAEQ(insw,f)         Factor income after deprecn distribution to institn insw
*- ------- HOUSEHOLD BLOCK ------------------------------------------------
*- ## Household Income
 YHEQ(h)                 Household incomes
 HOGOVEQ(h)              Government transfers
*- Household Expenditure
 HOHOEQ(h,hp)            Inter household transfer
 HOWOREQ(h,w)            trasnfer of foreign labor HHs to row
 HEXPEQ(h)               Household consumption expenditure

 QCDLES1EQ(cc,h)         LES Household utility function natural commodities
 QCDLES2EQ(cag,h)        LES Household utility function aggregate commodities
 QCDCESFOC(cag,cces,h)   FOC for household consumption at the lower nest
*- ------- ENTERPRISE BLOCK -----------------------------------------------
*- ## Enterprise Income
 YEEQ(e)                 Enterprise incomes
*- ## Enterprise Expenditure
 QEDEQ(c,e)              Enterprise commodity consumption
 HOENTEQ(h,e)            Household Income from enterprise e
 VEDEQ(e)                Value of enterprise consumption expenditure
 GOVENTEQ(e)             Government income from enterprise e
*- ------- GOVERNMENT BLOCK -----------------------------------------------
*- #### Government Income Block
*- ## Government Tax Rates
 TEDEF(c,w)              Export tax rates on exports of commy c
 TMDEF(w,c)              Tariff rates
 TSDEF(c)                Sales tax rates
 TVDEF(c)                Value added tax rates
 THCDEF(h,c)             HH specific comm tax (for food aid)
 TXDEF(a)                Indirect tax rates
 TFDEF(ff,a)             Factor use tax rates paid by activities
 TYFDEF(f)               Factor income tax rates
 TYHDEF(h)               Household income tax rates
 TYEDEF(e)               Enterprise income tax rates
*- ## Government Tax Revenues
 MTAXEQ                  Import tariff taxes revenue definition
 ETAXEQ                  Export taxes revenue definition
 STAXEQ                  Sales taxes revenue definition
 VTAXEQ                  Value added taxes revenue definition
 ITAXEQ                  Indirect taxes on activities revenue definition
 FTAXEQ                  Factor use tax revenue revenue definition
 FYTAXEQ                 Factor income taxes revenue definition
 DTAXEQ                  Direct taxes on households and enterprises
 HCTAXEQ                 HH specific comm tax (dor food aid)
*- #### Government Expenditure Block
 YGEQ
 QGDEQ(c)                Government commodity consumption
 EGEQ                    Government expenditure
 VGDEQ                   Value of Government consumption expenditure
 GBUDGEQ                 Government budget for current spendings and investments
*- ------- KAPITAL BLOCK --------------------------------------------------
*- ## Savings Block
 SHHDEF(h)               Household savings rates
 SENDEF(e)               Enterprise savings rates
 TOTSAVEQ                Total Savings
*- ## Investment Block
 QINVDEQ(c,i)            Investment demand in quantities for investment of type i
 QINVEQ(i)               Investment volume by investment type i

 INVSH_IEQ(i)            Shares of savings to investment of type i

 INVESTEQ                Total Investment expenditure
*- ------- FOREIGN INSTITUTIONS BLOCK -------------------------------------
 YFWOREQ(w,f)            Foreign factor income
*- ------- MARKET CLEARING BLOCK ------------------------------------------
*- ##### Account Closure
*- ## Factor Market Equilibria
 FMEQUIL(f)              Factor market equilibrium
 FSDEF_F(ff)             Factor supply definition  for natural factors
 FSDEF_FAG(ff)           Factor supply definition  for aggregate factors
 FSDEF_FC(ff)            Factor supply definition  for non-natural factors
 UNEMPEQUIL(ff)          Unemployment equation (U>0)
 UNEMPRATEDEF(ff)        Unemployment equation (U>0)
 FSILEQUIL(ins,f)        Factor supply for leisure
*- ## Commodity Market Equilibria
 PRODEQUIL(a,c)          Production equilibrium
 QEQUIL(c)               Commodity market equilibrium
*- ## Other Equlibria
 GOVEQUIL                Government equilibrium
 KAPREGDEF               Current account balance (foreign trade equilibrium)
 KAPWORDEF               Total Current account balance (foreign trade equilibrium)
*- #### Absorption Closure
 VFDOMDEQ                Value of final domestic demand
 INVESTSHEQ              Value share of investment in total final domestic demand
 VGDSHEQ                 Value share of Govt consumption in total final domestic demand
 VEDSHEQ(e)              Value share of Ent consumption in total final domestic demand
*- dynamic variables
 EXTENSDEF(ff,a)          Definition of the extension spendings
 EXTENSSHRDEF(ff,a)       Definition  of share of each factor in extension spending
 EXTENSEVAL(ff,a)         Evolution of extension (i.e. dynamic equation)
*- ##### GDP
 GDPEQ                   GDP from Expenditure
 RGDPEQ                  Real GDP from Expenditure
 RGDPFCEQ                Real GDP at Factor Cost
*- Agricutlural budget
 AgBuRecurrDEF(c)        Recurrent budget definition
 AgBuInvestDEF(i)        Investment budget definition
 AgBuInpSubDEF(ff,a)     Input subsidy budget definition
 AgBuRevFundDEF(ff,a)    Revolving Fund budget definition
 AgBuOutSubDEF(a)        Output subsidy budget definition
 AgBuComSubDEF(cc,h)     Commodity subsidies (i.e. food aid)
 AgBuIncSubDEF(h)        Income subsidies & transfers
 AgBuTotRecurrDEF        Total Recurrent budget definition
 AgBuTotInvestDEF        Total Investment budget definition
 AgBuTotInpSubDEF        Total Input subsidy budget definition
 AgBuTotOutSubDEF        Total Output subsidy budget definition
 AgBuTOTALxDEF           Total agricultural budget
 AgBuTOTShrDEF           Share of agri budget in total govt budget
 AgBuTotComSubDEF        Commodity subsidies (i.e. food aid)
 AgBuTotIncSubDEF        Income subsidies & transfers
*- Nutrition
 NutEqu(nutElem,h)       Nutrition indicator equations

*-------------------------------------------------------------------------------
*-EMISSIONS Equations
*-------------------------------------------------------------------------------

 CO2EM_Q_EQ(cener_ghg,a)      CO2 emissions by activities from use of fossil energy inputs
 CO2EM_H_EQ(cener_ghg,h)      CO2 emissions by households from consumption of fossil energy goods
 CO2EMIS_Q_EQ(a)              Total CO2 emissions by activities
 CO2EMIS_H_EQ(h)              Total CO2 emissions by households

 CO2EMIS_EQ                    Total CO2 emissions from combustion

 NCO2EM_Q_EQ(NCO,a)     Non-combustive emissions by activities
 NCO2EM_FS_EQ(NCO,c,a)    Non-combustive emission based on fossil fuel combustion in production
 NCO2EM_IO_EQ(NCO,c,a)    Process non-combustive NCO2 emissions based on intermediate demand
 NCO2EM_EN_EQ(NCO,f,a)    Non-combustive emissions based on factor use
 NCO2EM_H_EQ(NCO,c,h)     Non-combustive emissions by households

 NCO2EM_FS_SUM_EQ(NCO,a)    Non-combustive emission based on fossil fuel combustion in production
 NCO2EM_IO_SUM_EQ(NCO,a)    Process non-combustive NCO2 emissions based on intermediate demand
 NCO2EM_EN_SUM_EQ(NCO,a)    Non-combustive emissions based on factor use
 NCO2EM_H_SUM_EQ(NCO,h)     Non-combustive emissions by households

 NCO2EM_SUM_EQ(NCO)         Non-combustive emissions from all sources
 NC2OEM_A_SUM_EQ(NCO,a)     Non-combustive emissions from all sources by activity
 GHG_EQ                 Total GHG emissions

*- ##### Slack
 WALRASEQ                Savings and Investment equilibrium
 OBJNLP                  NLP dummy objective
 ;

*-################ 14. EQUATIONS ASSIGNMENTS ##############################
*------------------------------------------------------------------------------
*-  TRADE BLOCK
*------------------------------------------------------------------------------
*- Export price
 PERDEF(c,w)$ceR(c,w)..  PER(c,w) =E=
                             PWE(c) * ER(w) * (1 - TE(c,w))
                                    - SUM(m,ioqttqe(m,c,w) * PTT(m)) ;

*-export price through the index: works better
 PEDEF(c)$ce(c)..  atR(c)*PE(c) =E= SUM(w$gammaR(c,w),gammaR(c,w)**(1/(1+rhotR(c)))*PER(c,w)**(rhotR(c)/(1+rhotR(c))))**((1+rhotR(c))/rhotR(c))  ;

*- fix PE if a commodity is not exported
 PE.FX(c)$(NOT ce(c))         = 0.0 ;
 PER.FX(c,w)$(NOT ceR(c,w))         = 0.0 ;

*- CET function between exports and domestic demand = Commodity production
 CET(c)$(cd(c) AND ce(c))..
                  QXC(c) =E= at(c)*(gamma(c)*ZETAE(c)*QE(c)**rhot(c) +
                                 (1-(gamma(c)*ZETAE(c)))*QD(c)**rhot(c))**(1/rhot(c)) ;

*-fix production if not domestically produced
 QXC.FX(c)$(NOT cx(c))        = 0.0 ;

*- FOC for CET function Level 1 for comms w/o export demand
 ESUPPLY1(c,w)$(cedn(c,w) AND ceR(c,w))..
                   PER(c,w)*QER(c,w) =E= [QE(c)*PE(c)]*[SUM(wp$gammaR(c,wp), gammaR(c,wp)*(ZETAER(c,w)*QER(c,wp))**(-rhotR(c)))]**(-1)
                                         * gammaR(c,w) * (ZETAER(c,w)*QER(c,w))**(-rhotR(c));

 ZETAER.FX(c,w)     = ZETAER0(c,w);
 ZETAE.FX(c)        = ZETAE0(c)   ;


*- FOC for CET function Level 2
 ESUPPLY2(c)$(cd(c) AND ce(c))..
                   QE(c) =E= QD(c)*((PE(c)/PD(c))*((1-gamma(c))
                                 /gamma(c)))**(1/(rhot(c)-1)) ;

*-fix QE and QD if zero at the base
 QE.FX(c)$(NOT ce(c))         = 0.0 ;
 QD.FX(c)$(NOT cd(c))         = 0.0 ;
 QER.FX(c,w)$(NOT ceR(c,w))   = 0.0 ;

*-Export demand function. Active only if commodity is in ced(c,w).
 EDEMAND(c,w)$ced(c,w)..
                   QER(c,w) =E= econ(c,w)*((PWE(c)/pwse(c,w))**(-eta(c,w))) ;

*- For c with no exports OR for c with no domestic production domestic supply is by CETALT

 CETALT(c)$((cd(c) AND cen(c)) OR (cdn(c) AND ce(c)))..
                  QXC(c) =E= QD(c) + QE(c) ;

*- #### Imports Block

*- Import price

 PMRDEF(w,c)$cmR(w,c)..  PMR(w,c) =E= (PWM(c) * (1 + TM(w,c))) * ER(w) ;

*- fix PM of a commodity if not imported
 PM.FX(c)$(NOT cm(c))         = 0.0 ;
 PMR.FX(w,c)$(NOT cmR(w,c))   = 0.0 ;

*---  ## Parameters for Armington/CES functions

 ARMINGTON1(c)$(cm(c)).. QM(c) =E= acR(c)*(SUM(w$deltaR(w,c), deltaR(w,c)*(ZETAM(w,c)*QMR(w,c))**(-rhocR(c))))**(-1/rhocR(c));

 ZETAM.FX(w,c)=ZETAM0(w,c);

 ARMINGTON2(c)$(cx(c) AND cm(c))..
*- If imports AND dom. production is non-zero agg. supply is a CES
   QQ(c)  =E= ac(c)*(delta(c)*QM(c)**(-rhoc(c)) +
                                 (1-delta(c))*QD(c)**(-rhoc(c)))**(-1/rhoc(c));

*-                        if imports OR domestic production is zero agg. supply is the non-zero one
 ARMALT(c)$((cx(c) AND cmn(c)) OR (cxn(c) AND cm(c))) ..     QQ(c)  =E= QD(c) + QM(c)   ;

 COSTMIN1(w,c)$(cmR(w,c))..
                   PMR(w,c)*QMR(w,c) =E= [QM(c)*PM(c)]*[SUM(wp$deltaR(wp,c), deltaR(wp,c)*(ZETAM(w,c)*QMR(wp,c))**(-rhocR(c)))]**(-1)
                                 * deltaR(w,c) * (ZETAM(w,c)*QMR(w,c))**(-rhocR(c)) ;

 COSTMIN2(c)$(cx(c) AND cm(c))..
                   QM(c) =E= QD(c)*((PD(c)/PM(c))*(delta(c)/
                                 (1-delta(c))))**(1/(1+rhoc(c))) ;

*- fix QM and PD if there is no imports or dom. production
 QM.FX(c)$(NOT cm(c))         = 0.0 ;
 QMR.FX(w,c)$(NOT cmR(w,c))   = 0.0 ;
 PD.FX(c)$(NOT cd(c))         = 0.0 ;

*- ------- TRADE AND TRANSPORT MARGINS BLOCK ------------------------------
 IOQTTQQEVAL(m,c)$(sum(road, qinv0(road)))..
                  IOQTTQQ(m,c) =E=  ioqttqq0(m,c)*(sum(road, qinv0(road)) / SUM(road,QINV(road)))**etatr;

 IOQTTQQ.FX(m,c)$(NOT sum(road, qinv0(road))) =  ioqttqq0(m,c);

*- Price of margin commodities is a weighted sum of all comm. used for trade & transport
 PTTDEF(m)..      PTT(m) =E= SUM(c,ioqtdqtt(c,m) * PQD(c)) ;

*- supply of margin commodity
 QTTDEF(m)..      QTT(m) =E= SUM(c,IOQTTQQ(m,c) * QQ(c))
                               + SUM((w,c),ioqttqe(m,c,w) * QER(c,w)) ;
*- demand of commodity demand
 QTTDEQ(c)..     QTTD(c) =E= SUM(m,ioqtdqtt(c,m) * QTT(m)) ;

*- ------- COMMODITY PRICE BLOCK ------------------------------------------
 PQDDEF(c)$(cd(c) OR cm(c))..
                 PQD(c) =E= PQS(c) * (1 + TS(c))
                              + SUM(m,IOQTTQQ(m,c) * PTT(m)) ;

 PQD.FX(cc)$(NOT PQD0(cc))      = 0.0 ;

 PQCDDEF(cag,h)..
  PQCD(cag,h)*QCD(cag,h) =E= SUM(cces$map_cag_c(cag,cces),
                            PQD(cces)*(1+TV(cces))*(1+THC(h,cces))
                                     *QCD2(cag,cces,h)) ;

 PQCDEF(cc,h)$(ccesn(cc) AND HEXP0(h))..
                  PQC(cc,h) =E= (PQD(cc)*(1+TV(cc))*(1+THC(h,cc))) ;

 PQCDEF2(cc,h)$(cag(cc) AND HEXP0(h))..
                  PQC(cc,h) =E= PQCD(cc,h);

 PQC.fx(cc,h) $(not PQC0(cc,h)) = 0.0;
 PQCD.FX(cc,h)$(NOT qcag(cc,h)) = 0.0 ;

 PQSDEF(c)$(cd(c) OR cm(c))..
            PQS(c)*QQ(c) =E= (PD(c)*QD(c))+(PM(c)*QM(c)) ;
 PQS.FX(c)$(NOT PQS0(c))=0;

 PXCDEF(c)$cx(c)..
           PXC(c)*QXC(c) =E= (PD(c)*QD(c)) + (PE(c)*QE(c))$ce(c) ;

 PXC.FX(c)$(NOT cx(c))        = 0.0 ;

*- ------- NUMERAIRE PRICE BLOCK ------------------------------------------
 CPIDEF..            CPI =E= SUM(c,COMTOTSH(c)* (PQD(c) * (1 + TV(c))) ) ;

 PPIDEF..            PPI =E= SUM(c,VDDTOTSH(c)*PD(c)) ;

 VDDTOTSHDEF(c)$SUM(cp,PXC0(cp)*QXC0(cp)) ..
                     VDDTOTSH(c) =E= PXC(c)*QXC(c)/SUM(cp,PXC(cp)*QXC(cp)) ;

 VQCDDEF(c)..        VQCD(c) =E= SUM(h,(PQD(c)*(1+TV(c))*(1+THC(h,c))*QCD(c,h)$ccesn(c))
                           + SUM(cag,PQD(c)*(1+TV(c))*QCD2(cag,c,h)$cces(c)));

 COMTOTSHDEF(c)$SUM(cp,VQCD0(cp))..
                COMTOTSH(c)  =E= VQCD(c)/SUM(cp,VQCD(cp));


*- ------- PRODUCTION BLOCK -----------------------------------------------
 PXDEF(a)..   PX(a)=E= SUM(c,IOQXACQXV(a,c)*PXAC(a,c)) ;
 PX.FX(a)$(NOT PX0(a))=0;

 QXDEF(a)..   QX(a) =E= FD("ftop",a);
 QX.FX(a)$(NOT QX0(a))=0;

 QXEQUIL(a).. PX(a)*QX(a)*(1-TX(a)) =E= FD("ftop",a)*WFA("ftop",a);

 QVADEF(a)..  QVA(a) =E= SUM(fc$(map_fag_ffall_a("ftop",fc,a) AND f(fc)), FD(fc,a));
 QVA.FX(a)$(NOT QVA0(a))=0;

 QINTDEF(a)$qint0(a).. QINT(a) =E= SUM(fc$(map_fag_ffall_a("ftop",fc,a) and (not f(fc))), FD(fc,a));
 QINT.FX(a)$(NOT QINT0(a))=0;

 QINTDEQ(c,a)$ SAM(c,a)..   QINTD(c,a) =E=  SUM((fc)$map_c_f_a(c,fc,a),FD(fc,a)) ;
 QINTD.FX(c,a) $(not SAM(c,a)) = 0.00;

 VVADEF(a)..     VVA(a) =E= SUM(fc$(map_fag_ffall_a("ftop",fc,a) AND f(fc)), WFA(fc,a)*FD(fc,a));
 VVA.FX(a)$(NOT VVA0(a))=0;

 WFADEF(ff,a)$FD0(ff,a)..   WFA(ff,a) =E= WF(ff)*WFDIST(ff,a);
 WF.FX(fc)$(NOT f(fc))        = WF0(fc) ;


 PVADEF(a)$(SUM(fc$(map_fag_ffall_a("ftop",fc,a) AND f(fc)), FD0(fc,a)) )..
                    PVA(a) =E= SUM(fc$(map_fag_ffall_a("ftop",fc,a) AND f(fc)), WFA(fc,a)*FD(fc,a))
                            / SUM(fc$(map_fag_ffall_a("ftop",fc,a) AND f(fc)), FD(fc,a)) ;
 PVA.FX(a)$(NOT PVA0(a))=0;

 PINTDEF(a)$pint0(a).. PINT(a) =E=  SUM(fc$(map_fag_ffall_a("ftop",fc,a) and (not f(fc))), WFA(fc,a)*FD(fc,a))
                                        / SUM(fc$(map_fag_ffall_a("ftop",fc,a) and (not f(fc))), FD(fc,a));
 PINT.FX(a)$(NOT PINT0(a))=0;

*Flexible nested production function
 FDPRODFN(fag,a)$ (FD0(fag,a)and sum(ff,aqx1(fag,ff,a)))..
             FD(fag,a)
                    =E= ADFAG(fag,a)*(SUM(ff$deltafd(fag,ff,a),
                                deltafd(fag,ff,a)
                                *(AD(ff,a)*FD(ff,a))**(-rhofd(fag,a))))
                                   **(-1/rhofd(fag,a)) ;

 FDFOC(fag,ff,a)$  (deltafd(fag,ff,a) and aqx1(fag,ff,a) )..
             WFA(ff,a)*(1 + TF(ff,a))
                      =E= WFA(fag,a)*(1 + TF(fag,a))*FD(fag,a)
                         *(SUM(ffp$deltafd(fag,ffp,a),deltafd(fag,ffp,a)
                          *(AD(ff,a)*FD(ffp,a))**(-rhofd(fag,a))))**(-1)
                           *deltafd(fag,ff,a)*AD(ff,a)**(-rhofd(fag,a))
                            *FD(ff,a)**(-rhofd(fag,a)-1)  ;

*-Flexible Leontief possibility in any production function nest
 FDPRODFN2(fag,a)$ (FD0(fag,a)and sum(ff,aqx1n(fag,ff,a)))..
             WFA(fag,a)*(1+TF(fag,a))*FD(fag,a)  =E=
         SUM(ff$map_fag_ff_a(fag,ff,a), FD(ff,a)*WFA(ff,a)*(1+TF(ff,a)));

 FDFOC2(fag,ff,a)$  (deltafd(fag,ff,a) and aqx1n(fag,ff,a))..
          FD(ff,a) =E=  iofdfag (fag,ff,a)*FD(fag,a) ;

 WFAGDEF(c,a)$ sum((ff)$(map_c_f_a(c,ff,a)),SAM(c,a))..
         SUM(ff$map_c_f_a(c,ff,a), WFA(ff,a)) =E=  PQD(c)*PQDDIST(c,a)     ;
 WFA.FX(ff,a)$(NOT FD0(ff,a)) = 0;

* Proudctivy increae due to extension services
 EXTENSDEF(ff,a)$ mu_ext(ff,a)..
                 EXTENS(ff,a) =E= SUM(c$map_ff_qgd(ff,c),QGD(c)*EXTENSSHR(ff,a))  ;
 EXTENS.FX(ff,a)$ (not mu_ext(ff,a)) = EXTENS0(ff,a) ;

 EXTENSSHRDEF(ff,a)$ mu_ext(ff,a)..
                 EXTENSSHR(ff,a)*SUM(ffp$SUM(c,map_ff_qgd(ffp,c)),FD(ffp,a)*WFA(ffp,a))=E= FD(ff,a)*WFA(ff,a);
 EXTENSSHR.FX(ff,a)$ (not mu_ext(ff,a)) = EXTENSSHR0(ff,a) ;

 EXTENSEVAL(ff,a)$mu_ext(ff,a)..
                 ADFExt(ff,a) =E= ADFExt0(ff,a)*(EXTENS(ff,a)/EXTENS0(ff,a))**mu_ext(ff,a)  ;
 ADFExt.FX(ff,a)$ (not mu_ext(ff,a)) = ADFExt0(ff,a) ;

* Productivity shifter
 ADDEF(ff,a)..    AD(ff,a) =E= (1+SUM(h$FSI0(h,ff),ADFH(ff,h))/numHH(ff))*ADFD(ff,a)*ADFExt(ff,a) ;

 ADFAGEQ(ff,a)..  ADFAG(ff,a) =E= (adfagb(ff,a) + dadfag(ff,a))
                              *ADFAGADJ * (ADFAGfADJ(ff) * ADFAGaADJ(a)) ;
*- Commodity Output

*- CES aggregation of differentiated commodities

 COMOUT(c)$(cx(c) AND cxac(c))..
                  QXC(c) =E= adxc(c)*(SUM(a$deltaxc(a,c),deltaxc(a,c)
                             *(QXAC(a,c))**(-rhocxc(c))))**(-1/rhocxc(c)) ;

 COMOUTFOC(a,c)$(deltaxc(a,c) AND cxac(c))..
               PXAC(a,c) =E= PXC(c)*QXC(c)
                             *(SUM(ap$deltaxc(ap,c),deltaxc(ap,c)
                             *(QXAC(ap,c))**(-rhocxc(c))))**(-1)
                             *deltaxc(a,c)*(QXAC(a,c))**(-rhocxc(c)-1) ;

 PXAC.FX(a,c)$(NOT SAM(a,c)) = 0.0 ;

*- Aggregation of homogenous commodities

 COMOUT2(c)$(cx(c) AND cxacn(c))..              QXC(c) =E= SUM(a,QXAC(a,c)) ;

 COMOUTFOC2(a,c)$(deltaxc(a,c) AND cxacn(c))..  PXAC(a,c) =E= PXC(c) ;

*- Activity Output
*- Selection of CET - specify elast of transformation in Excel as non-zero
 ACTOUT(a,c)$(ioqxacqx(a,c) AND acetn(a))..
               QXAC(a,c) =E= IOQXACQX(a,c) * QX(a)*cti(a,c) ;

*- CET FOC for multiproduct firms with transformation possibility NO PRIMAL
 ACTOUTFOC(a,c)$(ioqxacqx(a,c) AND acet(a))..
              QXAC(a,c) =E= QX(a)*cti(a,c)
                *(PXAC(a,c)/(PX(a)*gammai(a,c)*ati(a)**(rhoti(a))))
                      **(1/(rhoti(a)-1)) ;

 QXAC.FX(a,c)$(NOT SAM(a,c))  = 0.0 ;

*- ######## FACTOR BLOCK`
 YFEQ(f)..         YF(f) =E= SUM(a,WFA(f,a)*FD(f,a))
                             + SUM(w,factwor(f,w)*ER(w)) ;

 YFDISPEQ(f).. YFDISP(f) =E= (YF(f) * (1- deprec(f)))*(1 - TYF(f)) ;

 YFINSEQ(f)..   YFINS(f) =E= YFDISP(f) - [(govvash(f)*YFDISP(f))
                                          + (SUM(w,worvash(w,f)*YFDISP(f)))] ;

 FSISHEQ(ins,f)$SUM(insp,fsi0(insp,f)) ..
                       FSISH(ins,f) =E= FSI(ins,f)/SUM(insp,FSI(insp,f)) ;

 FSISH.FX(ins,f)$(NOT FSISH0(ins,f))  = 0.0 ;

 INSVAEQ(ins,f)..   INSVA(ins,f) =E= FSISH(ins,f) * YFINS(f) ;

 INSVA.FX(ins,f)$(NOT INSVA0(ins,f)) = 0.0 ;

*- ######## HOUSEHOLD BLOCK
*- ## Household Income
 YHEQ(h)$YH0(h)..         YH(h) =E= SUM(f,INSVA(h,f))
                             + SUM(hp,HOHO(h,hp))
                             + SUM(e,HOENT(h,e))
                             + HOGOV(h)
                             + SUM(w,HOWOR(h,w)*ER(w))    ;

 YH.FX(h)$(NOT YH0(h))=YH0(h);
*- ## government transfers

 HOGOVEQ(h)..    HOGOV(h) =E= ((hogovb(h)+dabhogov(h))*HGADJ
                                 +DHOGOV * hogov01(h))*CPI    ;


*- ## inter household transfers
 HOHOEQ(h,hp)..  HOHO(h,hp) =E= sum(f, hohosh_mig(f,h,hp) *YF(f));

*- ## HH transfer to row for foreign labor HHs
 HOWOREQ(hrow,w)$map_hrow_w(hrow,w)..  HOWOR(hrow,w)*ER(w) + SUM(f,INSVA(hrow,f)) =e= 0;
 HOWOR.FX(h,w)$(NOT map_hrow_w(h,w)) = HOWOR0(h,w);

*- ##  Household Expenditure
 HEXPEQ(h)$HEXP0(h)..     HEXP(h) =E= YH(h) * (1 - TYH(h)) * (1 - SHH(h))
                             - SUM(hp,HOHO(h,hp)) ;

*- ## Utility maximization FOC
 QCDLES1EQ(ccesn,h)..
     QCD(ccesn,h)*PQD(ccesn)*(1+TV(ccesn))*(1+THC(h,ccesn))
       =E= (qcdconst(ccesn,h)*PQD(ccesn)*(1+TV(ccesn))*(1+THC(h,ccesn)))
            + beta(ccesn,h)
            *(HEXP(h)
              - (SUM(ccesnp,qcdconst(ccesnp,h)*PQD(ccesnp)*(1+TV(ccesnp))*(1+THC(h,ccesnp))))
              - (SUM(cagp,qcdconst(cagp,h)*PQCD(cagp,h))) ) ;
 QCD.FX(cc,h)$(NOT beta(cc,h))    = 0.0 ;

 QCDLES2EQ(cag,h)..
     QCD(cag,h)*PQCD(cag,h)
       =E= (qcdconst(cag,h)*PQCD(cag,h))
            + beta(cag,h)
            *(HEXP(h)
              - (SUM(cagp,qcdconst(cagp,h)*PQCD(cagp,h)))
              - (SUM(ccesnp,qcdconst(ccesnp,h)*PQD(ccesnp)*(1+THC(h,ccesnp))*(1+TV(ccesnp)))) ) ;

 QCDCESFOC(cag,cces,h)$(deltacd(cag,cces,h))..
     QCD2(cag,cces,h) =E= QCD(cag,h)
                          * ((((PQD(cces)*(1+THC(h,cces))*(1+TV(cces))) )
                                    *accd(cag,h)**rhocd(cag,h))
                             /(PQCD(cag,h)*deltacd(cag,cces,h)))
                                **(-1/(rhocd(cag,h)+1)) ;
 QCD2.FX(cc,ccp,h)$(NOT deltacd(cc,ccp,h)) = 0.0 ;

*- ------- ENTERPRISE BLOCK -----------------------------------------------
*- ## Enterprise Income
 YEEQ(e)..         YE(e) =E= SUM(f,INSVA(e,f))
                             + (EGADJ * entgovconst(e) * CPI)
                             + SUM(w,entwor(e,w)*ER(w));

*- ## Enterprise Expenditure
 QEDEQ(c,e)..      QED(c,e) =E= QEDADJ*qedconst(c,e) ;

 HOENTEQ(h,e)..    HOENT(h,e) =E= hoentsh(h,e)
                   * (((YE(e) * (1 - TYE(e))) * (1 - SEN(e)))
                   - SUM(c,QED(c,e)*PQD(c))) ;

 GOVENTEQ(e).. GOVENT(e) =E= goventsh(e)
                             * (((YE(e) * (1 - TYE(e))) * (1 - SEN(e)))
                              - SUM(c,QED(c,e)*PQD(c))) ;

 VEDEQ(e)..       VED(e) =E= SUM(c,QED(c,e)*PQD(c)) ;

*- ------- GOVERNMENT BLOCK -----------------------------------------------
*- #### Government Income Block
*- ## Government Tax Rates
 TMDEF(w,c)$cmR(w,c)..  TM(w,c) =E= ((tmb(w,c) + dabtm(w,c)) * TMADJ(w,c))
                                      + (DTM(w) * tm01(w,c)) ;


 TEDEF(c,w)$ceR(c,w)..    TE(c,w) =E= ((teb(c,w) + dabte(c,w)) * TEADJ(w))
                                      + (DTE(w) * te01(c,w)) ;

 TSDEF(c)$(cd(c) OR cm(c)).. TS(c) =E= ((tsb(c) + dabts(c)) * TSADJ)
                                      + (DTS * ts01(c)) ;
 TS.FX(c)$(NOT TS0(c))=0;

 THCDEF(h,c)..      THC(h,c) =E= ((thcb(h,c) + dabthc(h,c)) * THCADJ)
                                      + (DTHC * thc01(h,c)) ;

 TVDEF(c)$(cd(c) OR cm(c)).. TV(c) =E= ((tvb(c) + dabtv(c)) * TVADJ)
                                      + (DTV * tv01(c)) ;
 TV.FX(cc)$(NOT c(cc))        = 0.0 ;

 TXDEF(a)..        TX(a) =E= ((txb(a) + dabtx(a)) * TXADJ)
                                      + (DTX * tx01(a));

 TFDEF(ff,a)..    TF(ff,a) =E= ((tfb(ff,a) + dabtf(ff,a))* TFADJ )
                                     + (DTF*tf01(ff,a)) ;

 TYFDEF(f)..      TYF(f) =E= ((tyfb(f) + dabtyf(f)) * TYFADJ)
                                     + (DTYF * tyf01(f)) ;

 TYHDEF(h)..      TYH(h) =E= ((tyhb(h) + dabtyh(h)) * TYHADJ * TYADJ)
                                     + (DTYH * DTY * tyh01(h)) ;

 TYEDEF(e)..      TYE(e) =E= ((tyeb(e) + dabtye(e)) * TYEADJ * TYADJ)
                                     + (DTYE * DTY * tye01(e)) ;

*- ## Government Tax Revenues
 MTAXEQ..         MTAX    =E= SUM((w,c),(TM(w,c)*PWM(c)*ER(w)*QMR(w,c)));

 ETAXEQ..         ETAX    =E= SUM((w,c),TE(c,w)*PWE(c)*ER(w)*QER(c,w)) ;

 STAXEQ..         STAX    =E= SUM(c,TS(c)*PQS(c)*QQ(c)) ;

 VTAXEQ..         VTAX*(1-vtax01)+DVTAX*vtax01    =E= SUM((c,h),TV(c)*PQD(c)*QCD(c,h))
                              + SUM((cag,c,h),TV(c)*PQD(c)*QCD2(cag,c,h)) ;

 ITAXEQ..         ITAX    =E= SUM(a,TX(a)*PX(a)*QX(a)) ;

 FTAXEQ..         FTAX    =E= SUM((ff,a),TF(ff,a)*WFA(ff,a)*FD(ff,a)) ;

 FYTAXEQ..        FYTAX   =E= SUM(f,TYF(f)*(YF(f) * (1- deprec(f)))) ;

 DTAXEQ..         DTAX    =E= SUM(h,TYH(h)*YH(h)) + SUM(e,TYE(e)*YE(e)) ;

 HCTAXEQ..        HCTAX   =E= SUM((c,h),THC(h,c)*PQD(c)*QCD(c,h))
                              + SUM((cag,c,h),THC(h,c)*PQD(c)*QCD2(cag,c,h));

*- ## Government Income
 YGEQ..               YG =E= (MTAX + STAX + VTAX
                             + FTAX  + ITAX + FYTAX + DTAX  + ETAX + HCTAX
                             + SUM(f,govvash(f)*YFDISP(f))
                             + SUM(e,GOVENT(e)) + SUM(w,govwor(w)*ER(w)))*YGADJ    ;
*- #### Government Expenditure Block

*- government expenditure with agricultural budget
 QGDEQ(c)..       QGD(c) =E= (SUM(ceh$map_c_ceh(c,ceh),QGDADJceh*qgdconst(ceh))
                                 +SUM(coth$map_c_coth(c,coth),QGDADJoth*qgdconst(coth))
                                 +SUM(cext$map_c_cext(c,cext),QGDADJext*qgdconst(cext)))*QGDADJ
                                 +QGDADJc(c) ;

 EGEQ..               EG =E= SUM(c,QGD(c)*PQD(c))
                             + SUM(h,HOGOV(h))
                             + SUM(e,EGADJ*entgovconst(e)*CPI) ;

 VGDEQ..             VGD =E= SUM(c,QGD(c)*PQD(c)) ;

 GBUDGEQ..           GBUDG =E= VGD + SUM((iGov,c),PQD(c)*QINVD(c,iGov)) ;

*- ### Agricultural Budget
 AgBuRecurrDEF(cGovAgr)..           AgBuRecurr(cGovAgr)           =E= PQD(cGovAgr)*QGD(cGovAgr);

 AgBuInvestDEF(iGovAgr)..           AgBuInvest(iGovAgr)           =E= INVEST * INVSH_I(iGovAgr);

 AgBuInpSubDEF(fGovAgr,aGovAgr)..   AgBuInpSub(fGovAgr,aGovAgr)   =E= -TF(fGovAgr,aGovAgr)*WF(fGovAgr)*WFDIST(fGovAgr,aGovAgr)*FD(fGovAgr,aGovAgr);

 AgBuRevFundDEF(fRev,aRev)..        AgBuRevFund(fRev,aRev)        =E= -TF(fRev,aRev)*WF(fRev)*WFDIST(fRev,aRev)*FD(fRev,aRev);

 AgBuOutSubDEF(aGovAgr)..           AgBuOutSub(aGovAgr)           =E= -TX(aGovAgr)*PX(aGovAgr)*QX(aGovAgr) ;

 AgBuComSubDEF(c,h)..               AgBuComSub(c,h)               =E= -THC(h,c)*PQD(c)*QCD(c,h) - SUM(cag,THC(h,c)*PQD(c)*QCD2(cag,c,h)); ;

 AgBuIncSubDEF(h)$hrur(h)..         AgBuIncSub(h)                 =E= HOGOV(h);
 AgBuIncSub.FX(h)$(NOT hrur(h)) = 0;

 AgBuTotRecurrDEF..  AgBuTotRecurr =E= SUM((cGovAgr),AgBuRecurr(cGovAgr));

 AgBuTotInvestDEF..  AgBuTotInvest =E= SUM((iGovAgr),AgBuInvest(iGovAgr));

 AgBuTotInpSubDEF..  AgBuTotInpSub =E= SUM((fGovAgr,aGovAgr),AgBuInpSub(fGovAgr,aGovAgr) ) + sum((fRev,aRev), AgBuRevFund(fRev,aRev));

 AgBuTotOutSubDEF..  AgBuTotOutSub =E= SUM((aGovAgr),AgBuOutSub(aGovAgr));

 AgBuTotComSubDEF..  AgBuTotComSub =E= SUM((c,h),AgBuComSub(c,h));

 AgBuTotIncSubDEF..  AgBuTotIncSub =E= SUM((h),AgBuIncSub(h));

 AgBuTOTALxDEF..     AgBuTOTALx     =E=(  AgBuTotRecurr
                                          + AgBuTotInvest
                                          + AgBuTotInpSub
                                          + AgBuTotOutSub
                                          + AgBuTotComSub
                                          + AgBuTotIncSub );

 AgBuTOTShrDEF..  AgBuTOTALx =E= AgBuTOTShr*GBUDG ;

*- ------- KAPITAL BLOCK --------------------------------------------------
*- ## Savings Block
 SHHDEF(h)..     SHH(h) =E= ((shhb(h) + dabshh(h)) * SHADJ * SADJ)
                              + (DSHH * DS * shh01(h)) ;

 SENDEF(e)..     SEN(e) =E= ((senb(e) + dabsen(e)) * SEADJ * SADJ)
                              + (DSEN * DS * sen01(e)) ;

 TOTSAVEQ..       TOTSAV =E= SUM(f,(deprec(f)*YF(f)))
                             + SUM(h,(YH(h) * (1 - TYH(h))) * SHH(h))
                             + SUM(e,(YE(e) * (1 - TYE(e))) * SEN(e))
                             + KAPGOV
                             + SUM(w,KAPREG(w)*ER(w)) ;

*- ## Investment Block
 QINVDEQ(c,i)..  QINVD(c,i) =E= (QINV(i)*ioqinvd(c,i)) ;
 QINVD.FX(c,i)$(NOT ioqinvd(c,i))  = 0.0 ;

 QINVEQ(i)..     QINV(i) =E= qinvb(i) * IADJ *IADJTy(i) ;

 INVSH_IEQ(i)..  INVEST * INVSH_I(i) =E= SUM(c,PQD(c)*QINVD(c,i)) ;

 INVESTEQ..       INVEST =E= SUM((c,i),PQD(c)*QINVD(c,i))  ;

*- ------- FOREIGN INSTITUTIONS BLOCK -------------------------------------
 YFWOREQ(w,f)..   YFWOR(w,f) =E= (worvash(w,f)*YFDISP(f)) ;

*- ------- MARKET CLEARING BLOCK ------------------------------------------
*- ##### Account Closure
*- ## Factor Market Equilibria
* Unemployment
 UNEMPEQUIL(f)$UNEMP0(f)..   UNEMP(f) =G= 0 ;

 UNEMPRATEDEF(f)$UNEMP0(f)..   UNEMPRATE(f) =E= UNEMP(f)/FS(f) ;

 UNEMPRATE.FX(f)$(NOT UNEMP0(f)) = 0;

 FMEQUIL(f)..      SUM(ins,FSI(ins,f)) =E= SUM(a, FD(f,a)) + UNEMP(f) ;

 FSDEF_F(f)..       FS(f) =E= SUM(ins,FSI(ins,f)) ;

 FSDEF_FAG(fag)..   FS(fag) =E= SUM((a,fc)$map_fag_ffall_a(fag,fc,a),FD(fc,a)* (1 + (WFA(fc,a)-1)$sameas(fag,'ftop'))) ;

 FSDEF_FC(fc)$(NOT f(fc))..       FS(fc) =E= SUM(a,FD(fc,a)) ;

 FSILEQUIL(ins,f).. FSIL(ins,f) =E= SUM(alei$map_hh_alei(ins,alei),FD(f,alei)) ;

*- ## Commodity Market Equilibria
 PRODEQUIL(a,c)$QXAC0(a,c)..  QXAC(a,c) =E= IOQXACQXV(a,c)*QX(a) ;

 QEQUIL(c)..      QQ(c)  =E= QTTD(c) + SUM(a,QINTD(c,a))
                             + SUM(h,QCD(c,h))$ccesn(c)
                             + SUM((cag,h),QCD2(cag,c,h)$cces(c))
                             + SUM(e,QED(c,e)) + QGD(c)
                             + SUM(i,QINVD(c,i)) ;

*- ## Other Equlibria
 GOVEQUIL..       KAPGOV =E= YG - EG ;

 KAPREGDEF(w)..        KAPREG(w) =E= SUM(cm,PWM(cm)*QMR(w,cm))
                             + SUM(f,YFWOR(w,f))/ER(w)
                             - SUM(ce,PWE(ce)*QER(ce,w))
                             - SUM(h,howor(h,w))
                             - SUM(e,entwor(e,w))
                             - govwor(w)
                             - SUM(f,factwor(f,w)) ;

 KAPWORDEF..        KAPWOR =E= SUM(w,KAPREG(w)) ;

 ERXDEF..              ERX =E= SUM(w,SUM(c,PER(c,w)*QER(c,w))/SUM((cp,wp),PER(cp,wp)*QER(cp,wp))*ER(w));


*- #### Absorption Closure
 VFDOMDEQ..       VFDOMD =E= SUM((ccesn1,h),PQD(ccesn1) * (1+THC(h,ccesn1))*(1+TV(ccesn1)) * QCD(ccesn1,h))
                             + SUM((cag,cces,h),PQD(cces)* (1+THC(h,cces)) * (1+TV(cces)) * QCD2(cag,cces,h))
                             + SUM(c,PQD(c)*QGD(c))
                             + SUM((c,e),PQD(c)*QED(c,e))
                             + SUM((c,i),PQD(c)*QINVD(c,i)) ;

 INVESTSHEQ..       INVESTSH * VFDOMD =E= INVEST ;

 VGDSHEQ..          VGDSH * VFDOMD =E= VGD ;

 VEDSHEQ(e)..       VEDSH(e) * VFDOMD =E= VED(e) ;

*- ##### GDP
 GDPEQ..             GDP =E= SUM((clein,h),PQD(clein)* (1+THC(h,clein)) * (1+TV(clein)) * QCD(clein,h))
                             + SUM((cag,cces,h),PQD(cces)* (1+TV(cces))* QCD2(cag,cces,h))
                             + SUM(c,PQD(c)*QGD(c))
                             + SUM((c,i), PQD(c)*QINVD(c,i))
*-                            + SUM(c,PQD(c)*dstocconst(c))
                             + SUM(c, PE(c)*QE(c))
                             - SUM(c, PM(c)*QM(c)) ;

 RGDPFCEQ..          RGDPFC =E= SUM((alein,f),WFA0(f,alein)*(1 + TF(f,alein))*FD(f,alein))
                                + SUM(clein,TS(clein)*PQS0(clein)*QQ(clein))
                                + SUM(alein,TX(alein)*PX0(alein)*QX(alein))
                                + SUM((clein,h),TV(clein)*PQD0(clein)*QCD(clein,h))   ;

 RGDPEQ..            RGDP =E= SUM((clein,h),PQD0(clein)* (1+THC(h,clein)) * (1+TV(clein)) * QCD(clein,h))
                             + SUM((cag,cces,h),PQD0(cces) * (1+TV(cces)) * QCD2(cag,cces,h))
                             + SUM(c,PQD0(c)*QGD(c))
                             + SUM((c,i), PQD0(c)*QINVD(c,i))
                             + SUM(c, PE0(c)*QE(c))
                             - SUM(c, PM0(c)*QM(c)) ;
*-Nutrition
 NutEqu(nutElem,h)..       NutVal(nutElem,h) =E= SUM(c,nutTable(c,nutElem)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))));

*-##### Introduction of CO2 Combustion and Non-combustion GHG (NCO2) EMISSIONS

 CO2EM_Q_EQ(cener_ghg,a)..      CO2EM_Q(cener_ghg,a) =E= coefco2Q(cener_ghg,a)*QINTD(cener_ghg,a);
 CO2EM_H_EQ(cener_ghg,h)..      CO2EM_H(cener_ghg,h) =E= coefco2H(cener_ghg,h)*QCD(cener_ghg,h);
 CO2EMIS_Q_EQ(a)..              CO2EMIS_Q(a)         =E= SUM(cener_ghg,CO2EM_Q(cener_ghg,a));
 CO2EMIS_H_EQ(h)..              CO2EMIS_H(h)         =E= SUM(cener_ghg,CO2EM_H(cener_ghg,h));
 CO2EMIS_EQ..                   CO2EMIS              =E= sum(a,CO2EMIS_Q(a)) + sum(h,CO2EMIS_H(h)) ;

*Non-combustive emission coeeficients per unit of production by activities

 NCO2EM_Q_EQ(NCO,a)..           NCO2EM_Q(NCO,a)    =E= coefnco2Q(NCO,a)*QX(a);

*Process non-combustive emissions based on fossil fuel combustion in production

 NCO2EM_FS_EQ(NCO,c,a)..         NCO2EM_FS(NCO,c,a)     =E= coefnco2FS(NCO,c,a)*QINTD(c,a) ;

 NCO2EM_FS_SUM_EQ(NCO,a)..       NCO2EM_FS_SUM(NCO,a)   =E= sum(c,coefnco2FS(NCO,c,a)*QINTD(c,a)) ;

*Process non-combustive emissions based on intermediate demand
 NCO2EM_IO_EQ(NCO,c,a)..         NCO2EM_IO(NCO,c,a)     =E= coefnco2IO(NCO,c,a)*QINTD(c,a);

 NCO2EM_IO_SUM_EQ(NCO,a)..       NCO2EM_IO_SUM(NCO,a)   =E= sum(c,coefnco2IO(NCO,c,a)*QINTD(c,a));

*Endowment based non-combustive emissions
 NCO2EM_EN_EQ(NCO,f,a)..         NCO2EM_EN(NCO,f,a)     =E= coefnco2EN(NCO,f,a)*FD(f,a);

 NCO2EM_EN_SUM_EQ(NCO,a)..       NCO2EM_EN_SUM(NCO,a)   =E= sum(f,coefnco2EN(NCO,f,a)*FD(f,a));

*Non-combustive emissions linked to activities from all processes

 NC2OEM_A_SUM_EQ(NCO,a)..       NCO2EM_A_SUM(NCO,a)   =E= NCO2EM_FS_SUM(NCO,a) + NCO2EM_Q(NCO,a) + sum(f,coefnco2EN(NCO,f,a)*FD(f,a)) ;

*Household-based non-combustive emissions
 NCO2EM_H_EQ(NCO,c,h)..          NCO2EM_H(NCO,c,h)      =E= coefnco2H(NCO,c,h)*QCD(c,h);

 NCO2EM_H_SUM_EQ(NCO,h)..        NCO2EM_H_SUM(NCO,h)    =E= sum(c,coefnco2H(NCO,c,h)*QCD(c,h));


* Total non-combustive emissions from all sources
 NCO2EM_SUM_EQ(NCO)..            NCO2EM_SUM(NCO)       =E= sum(a,NCO2EM_Q(NCO,a) + NCO2EM_FS_SUM(NCO,a) + NCO2EM_IO_SUM(NCO,a)+ NCO2EM_EN_SUM(NCO,a))
                                                           + sum(h,NCO2EM_H_SUM(NCO,h));

 GHG_EQ..                       GHGEM                  =E= CO2EMIS + SUM(NCO,NCO2EM_SUM(NCO)) ;


*- ##### Slack
 WALRASEQ..       TOTSAV =E= INVEST + WALRAS ;

 OBJNLP..         WALRAS*WALRAS =E= OBJ;


*-################ 15. MODEL CLOSURE ######################################
$ontext
The standard or default closure is a minimal closure.

It is assumed that the closures used for experiments will be set in the experiment files.
$offtext

$INCLUDE 50_Closure\%closureFile%


*-################ 16. MODEL & SOLVE STATEMENTS ###########################

$ontext
limrow - number of rows for each equation block in the *.lst file (default 3)
limcol - number of columns for each equation block in the *.lst file (default 3)
iterlim - limit on iterations (default 1000)
nlp - non-linear programming
MINOS5 - MINOS5 solver
CONOPT - CONOPT Solver
CONOPT2 - CONOPT2 Solver
mcp - mixed complementarity problem
PATH - PATH Solver
$offtext


 Model demetra /

$ontext
When matching equations and variables do NOT match variables that may be
fixed in any model closure.
$offtext
*- ------- TRADE BLOCK ----------------------------------------------------
*- #### Exports Block
 ERXDEF
 PEDEF.PE
 PERDEF.PER
 CET
 ESUPPLY1
 ESUPPLY2
 EDEMAND
 CETALT
*- #### Imports Block
 PMRDEF.PMR
 ARMINGTON1
 ARMINGTON2
 COSTMIN1
 COSTMIN2
 ARMALT
*- ------- TRADE AND TRANSPORT MARGINS BLOCK ------------------------------
 PTTDEF.PTT
 QTTDEF.QTT
 QTTDEQ.QTTD
 ioqttqqEVAL.IOQTTQQ
*- ------- COMMODITY PRICE BLOCK ------------------------------------------
 PQSDEF.PQS
 PQDDEF
 PQCDDEF
 PQCDEF
 PQCDEF2
 PXCDEF.PXC
*- ------- NUMERAIRE PRICE BLOCK ------------------------------------------
 CPIDEF
 PPIDEF
 VQCDDEF
 COMTOTSHDEF
 VDDTOTSHDEF
*- ------- PRODUCTION BLOCK -----------------------------------------------
 PXDEF.PX
 PVADEF.PVA
 PINTDEF.PINT
 QXEQUIL
 QINTDEF.QINT
 QVADEF.QVA
 QXDEF.QX
 VVADEF.VVA
 WFADEF.WFA
 ADFAGEQ.ADFAG
 ADDEF.AD
 FDPRODFN
 FDPRODFN2
 FDFOC
 FDFOC2
 WFAGDEF
 QINTDEQ.QINTD
 COMOUT
 COMOUTFOC
 COMOUT2
 COMOUTFOC2
 ACTOUT.QXAC
 ACTOUTFOC
*- ------- FACTOR BLOCK ---------------------------------------------------
 YFEQ.YF
 YFDISPEQ.YFDISP
 YFINSEQ.YFINS
 FSISHEQ.FSISH
 INSVAEQ
*- ------- HOUSEHOLD BLOCK ------------------------------------------------
 YHEQ.YH
 HOGOVEQ.HOGOV
 HOHOEQ.HOHO
 HOWOREQ
 HEXPEQ.HEXP
 QCDLES1EQ
 QCDLES2EQ
 QCDCESFOC.QCD2
*- ------- ENTERPRISE BLOCK -----------------------------------------------
 YEEQ.YE
 QEDEQ.QED
 HOENTEQ.HOENT
 VEDEQ
 GOVENTEQ.GOVENT
*- ------- GOVERNMENT BLOCK -----------------------------------------------
 TEDEF.TE
 TMDEF.TM
 TSDEF.TS
 TVDEF.TV
 TXDEF.TX
 TFDEF.TF
 TYFDEF.TYF
 TYHDEF.TYH
 TYEDEF.TYE
 THCDEF.THC
 MTAXEQ.MTAX
 ETAXEQ.ETAX
 STAXEQ.STAX
 VTAXEQ
 ITAXEQ
 FTAXEQ
 FYTAXEQ.FYTAX
 DTAXEQ.DTAX
 HCTAXEQ.HCTAX
 YGEQ
 QGDEQ.QGD
 EGEQ
 VGDEQ.VGD
 GBUDGEQ.GBUDG
*- ------- KAPITAL BLOCK --------------------------------------------------
 SHHDEF.SHH
 SENDEF.SEN
 TOTSAVEQ.TOTSAV
 QINVDEQ.QINVD
 QINVEQ
 INVSH_IEQ
 INVESTEQ
*- ------- FOREIGN INSTITUTIONS BLOCK -------------------------------------
 YFWOREQ.YFWOR
*- ------- MARKET CLEARING BLOCK ------------------------------------------
 FMEQUIL
 UNEMPEQUIL.WF
 UNEMPRATEDEF
 FSDEF_F
 FSDEF_FAG
 FSDEF_FC
 FSILEQUIL.FSIL
 PRODEQUIL.IOQXACQXV
 QEQUIL.QQ
 GOVEQUIL
 KAPREGDEF
 KAPWORDEF
 VFDOMDEQ
 INVESTSHEQ
 VGDSHEQ
 VEDSHEQ
 GDPEQ
 RGDPEQ
 RGDPFCEQ
*-Dynamic links
 EXTENSDEF
 EXTENSSHRDEF
 EXTENSEVAL
 AgBuRecurrDEF.AgBuRecurr
 AgBuInvestDEF.AgBuInvest
 AgBuInpSubDEF.AgBuInpSub
 AgBuRevFundDEF.AgBuRevFund
 AgBuOutSubDEF.AgBuOutSub
 AgBuTOTALxDEF.AgBuTOTALx
 AgBuTOTShrDEF
 AgBuComSubDEF.AgBuComSub
 AgBuIncSubDEF.AgBuIncSub
 AgBuTotRecurrDEF.AgBuTotRecurr
 AgBuTotInvestDEF.AgBuTotInvest
 AgBuTotInpSubDEF.AgBuTotInpSub
 AgBuTotOutSubDEF.AgBuTotOutSub
 AgBuTotComSubDEF.AgBuTotComSub
 AgBuTotIncSubDEF.AgBuTotIncSub
*-Slack
 NutEqu
 CO2EM_Q_EQ
 CO2EM_H_EQ
 CO2EMIS_Q_EQ
 CO2EMIS_H_EQ
 CO2EMIS_EQ
 NCO2EM_Q_EQ
 NCO2EM_FS_EQ
 NCO2EM_IO_EQ
 NCO2EM_EN_EQ
 NCO2EM_H_EQ
 NCO2EM_FS_SUM_EQ
 NCO2EM_IO_SUM_EQ
 NCO2EM_EN_SUM_EQ
 NCO2EM_H_SUM_EQ
 NC2OEM_A_SUM_EQ
 NCO2EM_SUM_EQ
 GHG_EQ
 WALRASEQ
/ ;

model demetra_nlp
/
demetra
OBJNLP
/ ;

 demetra.HOLDFIXED   = 1 ;
 demetra.TOLINFREP   = 0.00000001 ;
 demetra.TOLINFEAS   = 1.0e-8 ;
 demetra.optfile     = 3;

 Options limrow=0,limcol=0;

* option iterlim = 25000 ;
 option iterlim = 0 ;
* option solprint = off
 option MCP           = PATH ;
 option NLP = CONOPT3;
 Solve demetra Using MCP ;

 demetra_nlp.HOLDFIXED   = 1 ;
 demetra_nlp.TOLINFREP   = 0.00000001 ;
 demetra_nlp.TOLINFEAS   = 1.0e-8 ;
* demetra.optfile = 6;

*-################ 17. SOCIAL ACCOUNTING MATRICES #########################
$ontext
the Global variable samNO determines the name of the SAM to be calculated, e.g. if it is 2, SAM2 will be created etc...
The .inc files calculates the SAM from the solution
$offtext

$SETGLOBAL samNo 2

*-################ 18. SUSTAINABLE DEVELOPMENT GOALS #########################

$include 30_Calibration\sdg.inc

*-################ 19. SAM and CALIBRATIO CHECK #########################

$INCLUDE 30_Calibration\samchk_decl.inc
$INCLUDE 30_Calibration\samchk_assign.inc
$include 30_Calibration\calibcheck_assign.inc

