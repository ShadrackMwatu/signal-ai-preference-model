*------------------------------------------------------------------------------
*------------------------------------------------------------------------------
*-
*-
*-   GAMS file : resparm.inc
*-
*-   @purpose  : Declares parameters used for reporting
*-   @author   :
*-   @date     :
*-   @since    :
*-   @refDoc   :
*-   @seeAlso  :
*-   @calledBy : report.inc
*------------------------------------------------------------------------------
*------------------------------------------------------------------------------

*-------- DEMETRA declare result parameters ---------------------------------
$ontext
 This section declares the result parameter that are used to store model
 results between experiments and sims.
 It is used by the result analysis code found in include files such as
 reslevel.gms, macrocal.gms, welfcal.gms, etc.
$offtext

*- The definitions depend on expclos and sim sets.
$include 60_Report\resultsets.inc


SET
sacAg                                    Aggregate SAM accounts
map_sac_sacAg(sac,sacAg)                 mapping between disaggregated and aggregated SAM accounts
sdgGoal                                  SDGs
sdgVar                                   SDG indicators
sdgRvs(sdgVar)                           SDG indicators that are inversely related to the goals
map_sdgGoal_sdgVar(sdgGoal,sdgVar)       mapping between SDGs and indicators
sdgEl                                    Elements of SDG result container

;



*-individual result parameters

$gdxin %gdxF%\exp_in.gdx
$loaddc sacAg map_sac_sacAg sdgGoal sdgVar map_sdgGoal_sdgVar sdgEl sdgRvs
$gdxin

ALIAS (sacAG,sacAGp,sacAGpp,sacAGppp), (sdgEl,sdgElp) ;

PARAMETERS

*- These parameter are used to report the results from the simulations
 resultSAM(restype,sac,sac,%resElem%)


*- A MicroSAM for each Experiment
 result(resType,resVar,*,sac,sac,sac,%resElem%)  holder for all results

 resultAg(resType,resVar,sacag,sacag,sacag,sacag,%resElem%)  holder for aggregated results

 resultMacro(resType,varType,stab1,%resElem%)     holder for all macro results

*-SDG results
 sdgResult(restype,sdgGoal,sdgVar,sac,sacp,%resElem%)   container for SDG indicators
* sdgSummary(restype,sdgGoal,sac,sacp,%resElem%)

*- Macroeconomic tables - indexed on stab1
 nMACROTOT(stab1,%resElem%)     Nominal Macro totals
 nMACROSH1(stab1,%resElem%)     Nominal Macro shares in GDP Expenditure
 nMACROSH2(stab1,%resElem%)     Nominal Macro shares in Domestic Absorption

 rMACROTOT(stab1,%resElem%)     Real Macro totals

*- Macroeconomic totals - percentage change
 rperMACROTOT(stab1,%resElem%)  Percentage changes in Real Macro totals
 nperMACROTOT(stab1,%resElem%)  Percentage changes in Nominal Macro totals
 nBasMACROTOT(stab1,%resElem%)  nominal macro results as per diff from base
 rBasMACROTOT(stab1,%resElem%)  real macro results as per diff from base

*---- 5a. Define Welfare Tables

Parameter

 YH_capres(h,%resElem%)    Income per capita to household h
 HEXP_capres(h,%resElem%)  Hhold consumption expend per capita
 ComTOTSHres(cc,%resElem%)
 VQCDres(cc,%resElem%)

 EV0(h,%resElem%)         EV by household on consumption

 EV1(resType,welfDim,h,sac,%resElem%)  EV Container
 EV1Base(resType,welfDim,h,sac,%resElem%) EV Container for diff from base

 EVBase(h,%resElem%)         EV by household on consumption
 EVBasePerc(h,%resElem%)         EV by household on consumption
 EVPriceBase(c,h,%resElem%)         EV by household on consumption
 EV_cap(h,%resElem%)     EV per capita by household on consumption
 EVBase_cap(h,%resElem%)     EV per capita by household on consumption

 IC(h,%resElem%)         LES Indirect compensation by hhold on consumption
 IC_cap(h,%resElem%)     LES IC per capita by hhold on consumption
 ICBase(h,%resElem%)         LES Indirect compensation by hhold on consumption
 ICBase_cap(h,%resElem%)     LES IC per capita by hhold on consumption

 EV_alt(h,%resElem%)     LES Alternative EV by hhold on consumption
 EV_alt_cap(h,%resElem%) LES Alt EV per capita by hhold on consumption
 EVBase_alt(h,%resElem%)     LES Alternative EV by hhold on consumption
 EVBase_alt_cap(h,%resElem%) LES Alt EV per capita by hhold on consumption

 YH_cap(h,%resElem%)    Income per capita to household h
 HEXP_cap(h,%resElem%)  Hhold consumption expend per capita

*popRes(h)                    Population by household and region

 EV_H_slut(h,%resElem%)  Slutsky approx EV by household on consumption
 EV_R_slut(%resElem%)    Slutsky approx EV by region on consumption

 EVBase_H_slut(h,%resElem%)  Slutsky approx EV by household on consumption
 EVBase_R_slut(%resElem%)    Slutsky approx EV by region on consumption


*- Check Base
  baseCheck(resVar,sac,sac,sac,sacppp,%reselem%) check if Base scenario can replicate BaU scenario

*-Psot sim SAM
 SAMres(sac,sacp,%resElem%)   Result SAMs

 TOTALSCHECKP         sum of abs value of differences as fraction of SAM total

*- Table of scalar results

 SCALres(scalresElem,%resElem%)   table of scalar results
 
*- GHG Emissions results
 
 GHGres(ghgElem1,*,*,ghgElem2,ghgElem3,GHG,%resElem%) table of GHG emissions results 

 CO2EM_Qres(c,a,%resElem%)          CO2 emissions by activities from use of fossil energy inputs
 CO2EM_Hres(c,h,%resElem%)          CO2 emissions by households from consumption of fossil energy goods
 CO2EMIS_Qres(a,%resElem%)          Total CO2 emissions from energy use by activities
 CO2EMIS_Hres(h,%resElem%)          Total CO2 emissions from energy use by households
 CO2EMISres(%resElem%)              Total CO2 emissions from combustion
 NCO2EM_Qres(ghg,a,%resElem%)       Non-combustive emissions  by activities
 NCO2EM_FSres(ghg,c,a,%resElem%)    Non-combustive emission based on fossil fuel combustion in production
 NCO2EM_IOres(ghg,c,a,%resElem%)    Process non-combustive emissions based on intermediate demand
 NCO2EM_ENres(ghg,f,a,%resElem%)    Non-combustive emissions based on factor use
 NCO2EM_Hres(ghg,c,h,%resElem%)     Non-combustive emissions  by households
 NCO2EM_A_SUMres(ghg,a,%resElem%)   Non-combustive emissions from all sources by activity - total by activity
 NCO2EM_SUMres(ghg,%resElem%)       Non-combustive emissions from differnt sources - total by GH
 GHGEMres(%resElem%)                Total GHG emissions - combustive and non-combustive

 NCO2EM_FS_SUMres(NCO,a,%resElem%)     Non-combustive emission based on fossil fuel combustion in production - total by activity
 NCO2EM_IO_SUMres(NCO,a,%resElem%)     Process non-combustive emissions based on intermediate demand - total by activity
 NCO2EM_EN_SUMres(NCO,a,%resElem%)     Non-combustive emissions based on factor use - total by activity
 NCO2EM_H_SUMres(NCO,h,%resElem%)      Non-combustive emissions  by households - total by household 
 NCO2EM_SUMres(NCO,%resElem%)          Non-combustive emissions - total
  
*- Table of adjuster results

 ADJres(adjresElem,%resElem%)     table of adjuster results


*- ------- TRADE BLOCK ----------------------------------------------------
*- #### Exports Block
 ERres(w,%resElem%)     Current account balance with each trade partner
 KAPREGres(w,%resElem%)     Current account balance with each trade partner
 PWEres(cc,%resElem%)       World price of exports in dollars
 PWSEres(cc,%resElem%)      World price of exports in dollars
 PEres(cc,%resElem%)        Domestic price of exports by activity a
 PERres(cc,w,%resElem%)        Domestic price of exports by activity a
 PDres(cc,%resElem%)        Consumer price for domestic supply of commodity c
 QEres(cc,%resElem%)        Domestic output exported by commodity c
 QERres(cc,w,%resElem%)     Domestic output exported by commodity c
 QDres(cc,%resElem%)        Domestic demand for commodity c

*- #### Imports Block

 PWMres(cc,%resElem%)       World price of imports in dollars
 PMres(cc,%resElem%)        Domestic price of competitive imports of commodity c
 PMRres(w,cc,%resElem%)        Domestic price of competitive imports of commodity c
 QMres(cc,%resElem%)        Imports of commodity c
 QMRres(w,cc,%resElem%)        Imports of commodity c
 QQres(cc,%resElem%)        Supply of composite commodity c

*- ------- TRADE AND TRANSPORT MARGINS BLOCK ------------------------------

 PTTres(m,%resElem%)          Price of trade and transport margin m
 QTTres(m,%resElem%)          Quantity of trade and transport margin m
 QTTDres(cc,%resElem%)        Intermediate input use for trade and transport margin m
 IOQTTQQres(m,cc,%resElem%)
*- ------- COMMODITY PRICE BLOCK ------------------------------------------

 PQSres(cc,%resElem%)       Supply price of composite commodity c
 PQDres(cc,%resElem%)      Purchaser price of composite commodity c
 PQCDres(cc,h,%resElem%)   Purchaser price of aggregate commodity cag by h
 PQCres(cc,h,%resElem%)    price paid by consumers for consumed commodities

*- ------- PRODUCTION BLOCK -----------------------------------------------

 PXres(a,%resElem%)        Composite price of output by activity a
 PVAres(a,%resElem%)       Value added price for activity a
 PINTres(a,%resElem%)      Price of aggregate intermediate input

 ADXres(a,%resElem%)       Shift parameter for CES production functions for QX
 ADres(ff,a,%resElem%)     Total Shift parameter res(ADFD*(1+ADFH))
 ADFDres(ff,a,%resElem%)    Shift parameter for factor and activity specific efficiency
 ADFHres(ff,h,%resElem%)    Shift parameter for factor and activity specific efficiency
 QXres(a,%resElem%)        Domestic production by activity a

 QVAres(a,%resElem%)       Quantity of aggregate value added for level 1 production
 VVAres(a,%resElem%)       Value of aggregate value added calculated from value of natural factors
 QINTres(a,%resElem%)      Aggregate quantity of intermediates used by activity a
 ADVAres(a,%resElem%)      Shift parameter for CES production functions for QVA

 WFres(ff,%resElem%)        Price of factor f
 WFDISTres(ff,a,%resElem%)  Sectoral proportion for factor prices
 WFAres(ff,a,%resElem%)     Sectoral proportion for factor prices
 PQDDISTres(cc,a,%resElem%) Price distribution parameter for factors coming from int inps
 FDres(ff,a,%resElem%)      Demand for factor f by activity a
 FSres(ff,%resElem%)        Supply of factor f
 UNEMPres(ff,%resElem%)        Unemployment of factor f
 UNEMPRATEres(ff,%resElem%)        Unemployment rate of factor f
 FSIres(insw,ff,%resElem%)         Factor supplies from institution ins by factor f
 FSILres(insw,ff,%resElem%)        Factor supply for leisure
 FSIMres(ff,insw,ff,insw,%resElem%)   Number of factors to f from f by ins
 MIGCONSres(ff,insw,ff,insw,%resElem%)   Constant part of the share of population migration
 SHMIGres(ff,insw,ff,insw,%resElem%)   Share of population migration
 URBNRATEres(%resElem%)             Share of population living in urban areas
 FMIGDRVres(f,fp,%resElem%)      Migration driver from fp to f
 HMIGDRVres(ins,insp,%resElem%)     Migration driver from insp to ins
 PMIGDRVres(ins,insp,%resElem%)     Migration driver from insp to ins due to public spending

 UNEMPres(ff,%resElem%)     Unemployed factors

 QINTDres(cc,a,%resElem%)   Demand for intermediate inputs by commodity

 PXCres(cc,%resElem%)       Producer price of composite domestic output
 QXCres(cc,%resElem%)       Domestic production by commodity c

 IOQXACQXVres(a,cc,%resElem%) Share of commodity c in output by activity a
 PXACres(a,cc,%resElem%)    Activity commodity prices
 QXACres(a,cc,%resElem%)    Domestic commodity output by each activity

*- ------- FACTOR BLOCK ---------------------------------------------------

 YFres(ff,%resElem%)        Income to factor f
 YFDISPres(ff,%resElem%)    Factor income for distribution after depreciation
 YFINSres(ff,%resElem%)     Factor income for distribution to domestic non govt institutions

 FSISHres(insw,ff,%resElem%) Shares of factor f supplied by institution ins
 INSVAres(insw,ff,%resElem%) Factor income after deprecn distribution to institn ins

*- ------- HOUSEHOLD BLOCK ------------------------------------------------
*- ## Household Income

 YHres(h,%resElem%)        Income to household h
 HOGOVres(h,%resElem%)     Government Transfers

*- Household Expenditure

 HOHOres(h,hp,%resElem%)   Inter household transfer
 HOWORres(h,w,%resElem%)     Transfer to HH from ROW
 HEXPres(h,%resElem%)      Household consumption expenditure

 QCDres(cc,h,%resElem%)     Household consumption by commodity c
 QCDTotalres(cc,h,%resElem%)     Household consumption by commodity c
 QCD2res(cc,cc,h,%resElem%) Household consumption by com'dy cces used in com'dy cag

*- Institution and Household Migration

 YMIGRres(insw,insw,%resElem%) household migration trigger is institution income

*- ~~ FACTOR MOBILITY BLOCK

 WMIGRres(ff,ff,insw,%resElem%) Wage ratio for factor mobility

*- ------- ENTERPRISE BLOCK -----------------------------------------------
*- ## Enterprise Income

 YEres(e,%resElem%)        Enterprise incomes

*- ## Enterprise Expenditure

 HOENTres(h,e,%resElem%)   Household Income from enterprise e
 GOVENTres(e,%resElem%)    Government income from enterprise e
 QEDres(cc,e,%resElem%)     Enterprise consumption by commodity c
 VEDres(e,%resElem%)       Value of enterprise e consumption expenditure

*- ------- GOVERNMENT BLOCK -----------------------------------------------

*- #### Government Income Block

 TEres(cc,w,%resElem%)        Export taxes on exported commy c
 TMres(w,cc,%resElem%)        Tariff rates on imported commy c
 TSres(cc,%resElem%)        Sales tax rate
 TQSres(cc,%resElem%)       Quantity Sales tax rate
 TVres(cc,%resElem%)        Value added tax rate
 TEXres(cc,%resElem%)       Excise tax rate

 TXres(a,%resElem%)        Indirect tax rate
 TXAres(a,%resElem%)        Indirect tax rate

 TFres(ff,a,%resElem%)      Tax rate on factor use
 TYFres(ff,%resElem%)       Direct tax rate on factor income

 TYHres(h,%resElem%)       Direct tax rate on households
 TYEres(e,%resElem%)       Direct tax rate on enterprises
 TINres(a,%resElem%)       Int inp tax on activity a
 THCres(h,c,%resElem%)     Household specific commodity tax

*- #### Government Expenditure Block

 QGDres(cc,%resElem%)       Government consumption demand by commodity c

 AgBuRecurrres(c,%resElem%)     Recurrent budget
 AgBuInvestres(i,%resElem%)     Investment budget
 AgBuInpSubres(ff,a,%resElem%)  Input subsidy budget
 AgBuRevFundres(ff,a,%resElem%)    Revolving Fund budget
 AgBuOutSubres(a,%resElem%)     Output subsidy budget
 AgBuComSubres(c,h,%resElem%)     Output subsidy budget
 AgBuIncSubres(h,%resElem%)     Output subsidy budget
 AgBuTotres(agBudgEl,%resElem%)    Total Recurrent budget
 QGDADJcres(cc,%resElem%)      Commodity level government spending adjuster

*- ------- KAPITAL BLOCK --------------------------------------------------

*- ## Savings Block

 SHHres(h,%resElem%)       Household savings rates
 SENres(e,%resElem%)       Enterprise savings rates

*- ## Investment Block

 QINVDres(cc,i,%resElem%)   Investment demand by commodity c
 QINVres(i,%resElem%)      Investment volume by investment type i
 INVSH_Ires(i,%resElem%)   Shares of savings to investment of type i

*- ------- FOREIGN INSTITUTIONS BLOCK -------------------------------------

 YFWORres(ff,%resElem%)     Foreign factor income

*- ------- MARKET CLEARING BLOCK ------------------------------------------
*- #### Absorption Closure

 VEDSHres(e,%resElem%)            Value share of Ent consumption in total final domestic demand
 EXTENSres(ff,a,%resElem%)        Extension services consumption
 ADFExtres(ff,a,%resElem%)        Change in factor productivity due to extension services
 EDUCres(h,%resElem%)             Education spending per HH
 HEALres(h,%resElem%)             Health spending per HH
 BRATEres(h,%resElem%)            Birth rate
 DRATEres(h,%resElem%)            Death rate
 DEATHres(h,%resElem%)            Number of deaths
 BIRTHres(h,%resElem%)            Number of births
 POPNres(h,%resElem%)             Demographic structure by age only
 POPCHNGres(h,%resElem%)          change in population due to deaths and births

* SolRep(resvar,%resElem%)      Solution Status

*- nutrition values
 NutValRes(nutElem,h,%resElem%)   Nutrition values

*- parameters for tables created by resstruct.inc

 EXP_CAGG_TOT(cagg,%resElem%)
 IMP_CAGG_TOT(cagg,%resElem%)
 EXPORT_DIF(%resElem%)
* EXPORT_DIF_AGG(wagg,ragg,%resElem%)
 EXPORT_TOT(%resElem%)
* EXPORT_TOT_SH(wgn,%resElem%)
 FACTADJ(f,%resElem%)
 IMPORT_TOT(%resElem%)
* IMPORT_TOT_SH(wgn,%resElem%)
 nACTIVSH(stab4,a,%resElem%)
 nCOMMODSH(stab3,c,%resElem%)
 nFACTUSESH(stab5,f,a,%resElem%)
 EXP_OUTshr(cagg,%resElem%)      Share of exports over output
 IMP_DEMshr(cagg,%resElem%)      Share of imports over demand


*-SDG results
g01UtilPCRes(h,%resElem%)                Per capita utility from private expenditure
g01UtilPCAgRes(%resElem%)                Per capita utility from private expenditure
g01WageCerRtRes(%resElem%)               Rural wage rate
g02TFPRes(%resElem%)                     Total factor productivity: endowment enhancing technical change
g02TMAvRes(%resElem%)                    Average import tariffs on agricultural food products (ad valorem rate)
g02FdProdIndRes(%resElem%)               Index of Food production
g02FdFsProdIndRes(%resElem%)             Index of Food production
g02FdimpRes(%resElem%)                   food import value
g02FdexpRes(%resElem%)                   Food export value
g02NutPCRes(nutElem,h,%resElem%)         nutrition values per capita
g02NutPCAgRes(nutElem,%resElem%)         nutrition values per capita
g02CalCerShRes(h,%resElem%)              share of calories per capita in total calories pc
g02CalCerShAgRes(%resElem%)              share of calories per capita in total calories pc
g02ProLvsFsRes(h,%resElem%)              Protein from livestock and fish and livestock  products
g02ProLvsFsAgRes(%resElem%)              Protein from livestock and fish and livestock  products
g02ProLvsRes(h,%resElem%)                Protein from livestock and livestock  products (no fish)
g02ProLvsAgRes(%resElem%)                Protein from livestock and livestock  products (no fish)
g02YDAvRes(h,%resElem%)                  Average household disposable income
g02YDAvAgRes(%resElem%)                  Average household disposable income
g02FdPriIndRes(h,%resElem%)              food price index
g02FdPriIndAgRes(%resElem%)              food price index
g02FdYDShRes(h,%resElem%)                Share of food expenditure in total disposable income
g02FdYDShAgRes(%resElem%)                Share of food expenditure in total disposable income
g02FdConsRes(h,%resElem%)                food consumption
g02FdConsAgRes(%resElem%)                food consumption
g02FdConsPCRes(h,%resElem%)              food consumption per capita
g02FdConsPCAgRes(%resElem%)              food consumption per capita
g02CalFrVShRes(h,%resElem%)              Share of calories from fruit and vegetables
g02CalFrVShAgRes(%resElem%)              Share of calories from fruit and vegetables
g02TMIndRes(%resElem%)                   index of import tariffs on agricultural goods products
g02ExpSubIndRes(%resElem%)               index of export subsidies on agricultural goods products
g02TFPRes(%resElem%)                     Total factor productivity: endowment enhancing technical change (AD)
g06WatUseRes(%resElem%)                  index of total abstracted irrigation water volumes
g07EnerPrimRes(%resElem%)                Primary Energy
g07EnerClnShRes(%resElem%)               Share of clean energy in total energy
g07EnerProdRes(%resElem%)                Energy production (Final Energy)
g07EnerSfSuRes(%resElem%)                Energy Self sufficiency
g07EnerPriIndRes(c,%resElem%)            Energy price
g07EnerPriIndAgRes(%resElem%)            Energy price
g07FosCompRes(%resElem%)                 Relative competitiveness of  fossil    (PD over PWM)
g07RenCompRes(%resElem%)                 Relative competitiveness of  fossil    (PD over PWM)
g07FosRenRtRes(%resElem%)                Relative competitiveness of  fossil
g07EnerSecRes(%resElem%)                 Energy security: value-added contribution
g07EnerVaRtRes(a,%resElem%)              Ratio of value added to net domestic energy use by industry
g07EnerVaRtAgRes(%resElem%)              Ratio of value added to net domestic energy use by industry
g07EnerPrimStkRes(enEl1,%resElem%)       Primary energy stock: mining
g07EnerRefnRes(%resElem%)                Refining transformation and power station usage (perto-chem & electricity)
g07EnerUseRes(enEl2,%resElem%)           Energy use by transportation industry other export of refined
g07PrimGdpRtRes(enEl1,%resElem%)         PrimaryEnergy intensity measured in terms of GDP
g07RefnGdpRtRes(%resElem%)               Refining Energy intensity measured in terms of GDP
g07UseGdpRtRes(enEl2,%resElem%)          Energy use intensity measured in terms of GDP
g07RefnPrimRtRes(%resElem%)              Refining Energy intensity measured in terms of Primary energy
g07UsePrimRtRes(enEl2,%resElem%)         Energy use intensity measured in terms of Primary energy
g08GDPPCGrRes(%resElem%)                 GDP per capita growth
g08NetTradeRes(%resElem%)                net trade position
g08RevCompRes(c,%resElem%)               Revealed Comparative Advantage (if >1 country has RCA in that comm. export more compared to other sectors)
g08RevCompAgRes(%resElem%)               Revealed Comparative Advantage (if >1 country has RCA in that comm. export more compared to other sectors)
g08FosGDPShRes(%resElem%)                Diversification index (IRRELEVANT)
g09ManVaShRes(%resElem%)                 Share of fossil fuels in GDP
g09ManVaPCRes(%resElem%)                 Manufacturing value added as a share of total value
g08ManEmpShRes(%resElem%)                Manufacturing value added per capita
g08ExpRes(%resElem%)                     Manufacturing employment as a percentage of total employment
g08ImpRes(%resElem%)                     Total Exports
g08OpenRes(%resElem%)                    Total Imports
g10LabShRes(%resElem%)                   Trade Opennes
g10AgrEmpRes(%resElem%)                  Labour share of GDP comprising wages
g10AgrEmpShRes(%resElem%)                Agricultural employment as a percentage of total employment
g10SkilRes(%resElem%)                    Skills composition
g10WageDifSklRes(%resElem%)              Wage differential skilled:unskilled
g10WageDifAgrRes(%resElem%)              Wage differential agriculture:non-agriculture
g10IncDiffHHRes(h,hp,%resElem%)          Income differential households (ratio of inc per capita)
g10IncDiffHHAgRes(%resElem%)          Income differential households (ratio of inc per capita)
g12RenShRes(%resElem%)                   Share of renewables in total energy production
g13RenShRes(%resElem%)                   Share of renewables in total energy production
g14FsShRes(%resElem%)                    Fisheries as a value share of GDP
g15NonAgriRes(%resElem%)                 Share of non-agricultural land (1 - change in agri land) (or forest area ???)
g17GDPPcRes(%resElem%)                   GDP per capita
g17EGShRes(egEl,%resElem%)               Total government revenue (by source) as a percentage of GDP
g17EGShAgRes(%resElem%)               Total government revenue (by source) as a percentage of GDP
;

*-parameters for aggregate results
Parameter
SCALagRes
ADJagRes
ERagRes
KAPREGagRes
PWEagRes
PEagRes
PERagRes
PDagRes
QEagRes
QERagRes
QDagRes
PWMagRes
PMagRes
PMRagRes
QMagRes
QMRagRes
QQagRes
PTTagRes
QTTagRes
QTTDagRes
PQSagRes
PQDagRes
PQCDagRes
PQCagRes
PXagRes
PVAagRes
PINTagRes
ADXagRes
ADagRes
ADFDagRes
ADFHagRes
QXagRes
QVAagRes
VVAagRes
QINTagRes
ADVAagRes
WFagRes
WFAagRes
PQDDISTagRes
FDagRes
FSagRes
UNEMPagRes
FSIagRes
FSILagRes
MIGCONSagRes
SHMIGagRes
FSIMagRes
FMIGDRVagRes
HMIGDRVagRes
PMIGDRVagRes
QINTDagRes
PXCagRes
QXCagRes
IOQXACQXVagRes
PXACagRes
QXACagRes
YFagRes
YFDISPagRes
YFINSagRes
FSISHagRes
INSVAagRes
YHagRes
HOGOVagRes
HOHOagRes
HOWORagRes
HEXPagRes
QCDagRes
QCD2agRes
YMIGRagRes
WMIGRagRes
YEagRes
HOENTagRes
GOVENTagRes
QEDagRes
VEDagRes
TEagRes
TMagRes
TSagRes
TVagRes
TEXagRes
TXagRes
TXAagRes
TFagRes
TYFagRes
TYHagRes
TYEagRes
THCagRes
TINagRes
QGDagRes
SHHagRes
SENagRes
QINVDagRes
QINVagRes
INVSH_IagRes
YFWORagRes
VEDSHagRes
*SolRepagRes
AgBuRecurragRes
AgBuInvestagRes
AgBuInpSubagRes
AgBuRevFundagRes
AgBuOutSubagRes
AgBuComSubagRes
AgBuIncSubagRes
AgBuTotagRes
EXTENSagRes
ADFExtagRes
EDUCagRes
HEALagRes
BRATEagRes
DRATEagRes
DEATHagRes
BIRTHagRes
POPNagRes
POPCHNGagRes
;

*--------- end of declare result parameters --------------------------
