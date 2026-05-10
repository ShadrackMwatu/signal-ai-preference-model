*------------------------------------------------------------------------------
*------------------------------------------------------------------------------
*-
*-
*-   GAMS file : structSets.gms
*-
*-   @purpose  : Defines sets used in structure tables
*-   @author   :
*-   @date     :
*-   @since    :
*-   @refDoc   :
*-   @seeAlso  :
*-   @calledBy : struct.inc
*------------------------------------------------------------------------------
*------------------------------------------------------------------------------


SET

structElem1
/
stQCDTOT         private consumption
stQEDTOT         entrise consumption
stQGDTOT         government consumption
stQINVTOT        investment consumption
stQABSORP        absorption
stIMPORT         import demand
stEXPORT         export supply
stGDP            GDP from expenditure
stSUPPLY         total domestic production
stUSE            total intermediate inputs
stYHTOT          household income
stYGTOT          government income
stYFTOT          factor income
stYFDISPTOT      distributed factor income
stYFLABTOT       labour factor income
stTOTSAV         total savings
stHOSAV          household savings
stGOVSAV         government savings
stFSAV           foreign savings
stDEPREC         depreciation
stMTAX           Import tariff revenue
stETAX           Export tax revenue
stVTAX           VAT revenue
stSTAX           Sales tax revenue
stEXTAX          Excise tax revenue
stITAX           Indirect tax revenue
stFTAX           Factor use tax revenue
stFYTAX          Factor income tax revenue
stINTAX          Int inp tax revenue
stDTAX           Direct or income tax revenue
stTOTTAX         Total tax revenue
/

structElem3
/
stPRIVregDEM    private domestic demand by total domestic demand
stPRIVcomDEM    private domestic demand by total commodity demand
stGOVTregDEM    government domestic demand by total domestic demand
stGOVTcomDEM    government domestic demand by total commodity demand
stINVDregDEM    investment domestic demand by total domestic demand
stINVDcomDEM    investment domestic demand by total commodity demand
stINTDregDEM    intermediate domestic demand by total domestic demand
stINTDcomDEM    intermediate domestic demand by total commodity demand
stMAKEcomSUP    domestic make by commodity shares
stSUPPcomSUP    total domestic supply by commodity shares
stQMcomSUP      aggregate import supply by commodity shares
stQDcomSUP      domestic output to domestic market by commodity shares
stQEconSUP      domestic ouptut to export market by commodity shares
stregCHK        Check on regional shares
stcomCHK        Check on commodity shares
stLAB
stCAP
stVA
EXP-OUTshr
IMP-DEMshr
/

structElem4
/
stQINTQX         shares of intermediate input in GO by activity
stQINT           shares of intermediate input use by activity
StVAQX           shares of value added in GO by activity
stVA             shares of value added by activity
stQX             shares of gross output by activity
stLAB            shares of labour income in value added
stUskLAB         shares of unskilled labour income in value added
stSkLAB          shares of semi skilled labour income in value added
stSekLAB         shares of skilled labour income in value added
stCAP            shares of capital income in value added
stLND            shares of land income in value added
stFTAX           factor use taxes or subsidies in value added
stFACTchk        CHECK on factor shares addition
stSUB            If subsitution possible at Level 1
stELASTX         Elasticity of subsitution at Level 1
stELASTVA        Elasticity of subsitution at Level 2
stFSUB           Share of subsidies over production
/

structElem5
/
stTRANS Transactions values in models
stACTSH Factor mix by activity
stFFSH  Factor use by factor
/
;
