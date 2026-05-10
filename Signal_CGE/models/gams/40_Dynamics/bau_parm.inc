*-------- DEMETRA declare BaU parameters ---------------------------------
$ontext
 This section declares the parameter that are used to store the BaU
 results for calibrating the recursive dynamic (beseline) version.

 These parameter are used to record the values of variables from the
 calibration of the baseline that are then used as parameters when
 running simulations.

 All variables available in the closure file are declared with matching
 parameters

$offtext

PARAMETERS

*- ADVAADJ_BL(t) = ADVAADJ.L ;

*-## FOREIGN EXCHANGE MARKET CLOSURE

 ER_BL(t)          Exchange rate(domestic per world unit)

 QX_BL(a,t)        Output
 QXAC_BL(a,c,t)    Output by product

 QE_BL(c,t)       Exports
 QER_BL(c,w,t)    Exports from regions
 QM_BL(c,t)       Imports
 QMR_BL(w,c,t)    Imports from regions

 KAPWOR_BL(t)      Current account balance
 KAPREG_BL(w,t)      Current account balance  with each region

*- Fixing of world prices
 PWM_BL(c,t)       World price of imports in dollars
 PWE_BL(c,t)       World price of exports in dollars
 PQD_BL(c,t)       Domestic prices

*-## INVESTMENT-SAVINGS CLOSURE
*- Savings Rate adjustments

 SADJ_BL(t)        Savings rate scaling factor for BOTH households and enterprises
 SHADJ_BL(t)       Savings rate scaling factor for households
 SEADJ_BL(t)       Savings rate scaling factor for enterprises

 DSHH_BL(t)        Partial household savings rate scaling factor
 DS_BL(t)          Partial household and enterprise savings rate scaling factor
 DSEN_BL(t)        Partial enterprise savings rate scaling factor

*- Investment 'level' adjustments

 IADJ_BL(t)        Investment scaling factor for investment of type i

 QINV_BL(i,t)      Investment volume by investment type i

 INVSH_I_BL(i,t)   Shares of savings to investment of type i

 INVEST_BL(t)      Total investment expenditure
 INVESTSH_BL(t)    Value share of investment in total final domestic demand


*-## ENTERPRISE CLOSURE RULES

 QEDADJ_BL(t)      Enterprise demand volume Scaling Factor
 VED_BL(e,t)       Value of enterprise e consumption expenditure
 VEDSH_BL(e,t)     Value share of Ent consumption in total final domestic demand

*- Enterprise transfers to households

 HEADJ_BL(t)       Scaling factor for enterprise transfers to households

*-## GOVT CLOSURE RULES
 FTAX_BL(t)        Factor tax revenue
 ITAXA_BL(t)       Indirect tax
 TF_BL(ff,a,t)       Factor tax rate
 TXA_BL(a,t)       Activity tax
*- Tax rate scaling factors

 TEADJ_BL(w,t)       Export subsidy Scaling Factor
 TMADJ_BL(w,t)       Tarrif rate Scaling Factor
 TSADJ_BL(t)       Sales tax rate scaling factor
 TVADJ_BL(t)       Value added tax rate scaling factor
 TEXADJ_BL(t)      Excise tax rate scaling factor
 TYFADJ_BL(t)      Factor Tax Scaling Factor
 TXADJ_BL(t)       Indirect Tax Scaling Factor
 TFADJ_BL(t)       Factor Use Tax Scaling Factor
 TYHADJ_BL(t)      Household Income Tax Scaling Factor
 TYADJ_BL(t)       Household and Enterprise Income Tax Scaling Factor
 TYEADJ_BL(t)      Enterprise income tax Scaling Factor

 DTE_BL(w,t)         Partial Export tax rate scaling factor
 DTM_BL(w,t)         Partial Tariff rate scaling factor
 DTS_BL(t)         Partial Sales tax rate scaling factor
 DTV_BL(t)         Partial value added tax rate scaling factor
 DTEX_BL(t)        Partial Excise tax rate scaling factor
 DTX_BL(t)         Partial Indirect tax rate scaling factor
 DTF_BL(t)         Partial factor use tax scaling factor
 DTYF_BL(t)        Partial direct tax on factor rate scaling factor
 DTYH_BL(t)        Partial direct tax on household rate scaling factor
 DTY_BL(t)         Partial direct tax on hold and enterprise rate scaling factor
 DTYE_BL(t)        Partial direct tax on enterprise rate scaling factor

*- Government expenditure scaling factor

 QGDADJ_BL(t)      Government consumption demand scaling factor
 VGD_BL(t)         Value of Government consumption expenditure
 VGDSH_BL(t)       Value share of Govt consumption in total final domestic demand
 QGD_BL(c,t)       government expenditure on comm c
*- Government transfers scaling factors are fixed

 HGADJ_BL(t)       Scaling factor for government transfers to households
 EGADJ_BL(t)       Transfers to enterprises by government Scaling Factor

*- alternatively the internal balance / Govt savings can be fixed

 KAPGOV_BL(t)      Government Savings
 EG_BL(T)          Government spending
 YG_BL(T)          Government income

*-## FACTOR MARKET CLOSURE

*- Factor supplies by institution (FSI)

 FSI_BL(ins,ff,t)   Factor supplies from institution ins by factor f

 WFDIST_BL(f,a,t)  Sectoral proportion for factor prices
 WF_BL(ff,t)        Price of factor f

 FS_BL(f,t)        Supply of factor f

 FD_BL(ff,a,t)      Demand for factor f by activity a

*- # Technology Closures for Factor Market
*- Technology for CES production functions for Level 1 of production nest

 ADXADJ_BL(t)      Scaling Factor for Shift parameter on CES functions for Q

*- Technology for CES aggregation functions for Level 2 of production nest

 ADVAADJ_BL(t)     Scaling Factor for Shift parameter on CES functions for QVA
 ADFAGfADJ_BL(ff,t)  Scaling Factor for Shift parameter on CES functions for specific nests
 QVA_BL(a,t)       Quantity of value added
 VVA_BL(a,t)       Value of value added
*- Technology for factor activity and region specific factor efficiency

 ADFD_BL(ff,a,t)   Shift parameter for factor and activity specific efficiency

*-## GDP

 GDP_BL2(t)         GDP from Expenditure

*-## MISCELLANEOUS FIXED VARIABLES

 CPI_BL(t)         Consumer price index
 PPI_BL(t)         Producer (domestic) price index
 AgBuRecurr_BL(c,t)
 AgBuInvest_BL(i,t)        Investment budget
 AgBuInpSub_BL(ff,a,t)     Input subsidy budget
 AgBuOutSub_BL(a,t)        Output subsidy budget
 AgBuTotRecurr_BL(t)       Total Recurrent budget
 AgBuTotInvest_BL(t)       Total Investment budget
 AgBuTotInpSub_BL(t)       Total Input subsidy budget
 AgBuTotOutSub_BL(t)       Total Output subsidy budget
 AgBuTOTALx_BL(t)          Total agricultural budget
 AgBuTOTShr_BL(t)         Share of agricultural budget in total gov't budget

 MIGCONS_BL(f,h,fp,hp,t)   Constant part of the share of population migrating
;



*--------- end of DEMETRA declare baseline parameters --------------------------
