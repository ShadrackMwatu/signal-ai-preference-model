* ----------------- DEMETRA Macroeconomic Tables ------------------------
$ontext
The layout of this files is

   * ------- 1. Assign Macroeconomic Totals
             *---- 1a. Nominal Macroeconomic Totals
             *---- 1b. Real Macroeconomic Totals
   * ------- 2. Assign Macroeconomic Shares
             *---- 2a. Nominal Macroeconomic Shares in GDPEXP
             *---- 2b. Nominal Macroeconomic Shares in ABSORP
   * ------- 3. Assign Percentage Changes in Macroeconomic Totals
             *---- 3a. Percentage Change in Real Macroeconomic Totals
             *---- 3b. Percentage Change in Nominal Macroeconomic Totals
   * ------- 4. Exporting Macroeconomic Tables to GDX
$offtext
*-------- Exporting Macroeconomic Tables to GDX -----------------------------

*-------- 1. Assign Macroeconomic Totals ---------------------------------

*---- 1a. Nominal Macroeconomic Totals

*-Value of household consumption
 ResultMACRO("Level","Nominal","stQCDTOT",%resElem1%)
            = SUM((c,h), PQDres(c,%resElem1%) *QCDres(c,h,%resElem1%))
                + SUM((cag,c,h),PQDres(c,%resElem1%) *QCD2res(cag,c,h,%resElem1%)$cces(c));

*-Value of enterprise consumption
 ResultMACRO("Level","Nominal","stQEDTOT",%resElem1%)
            = SUM((c,e),PQDres(c,%resElem1%) *QEDres(c,e,%resElem1%)) ;

*-Value of government consumption
 ResultMACRO("Level","Nominal","stQGDTOT",%resElem1%)
            = SUM(c,PQDres(c,%resElem1%) *QGDres(c,%resElem1%)) ;

*-Value of investment consumption
 ResultMACRO("Level","Nominal","stQINVTOT",%resElem1%)
            = SUM((c,i),PQDres(c,%resElem1%) *QINVDres(c,i,%resElem1%)) ;

*-Value of Domestic final demand
 ResultMACRO("Level","Nominal","stQABSORP",%resElem1%)
            = SUM((c,h), PQDres(c,%resElem1%) *QCDres(c,h,%resElem1%))
              + SUM((cag,cces,h),PQDres(cces,%resElem1%) *QCD2res(cag,cces,h,%resElem1%))
              + SUM((c,e),PQDres(c,%resElem1%) *QEDres(c,e,%resElem1%))
              + SUM(c,PQDres(c,%resElem1%) *QGDres(c,%resElem1%))
              + SUM((c,i),PQDres(c,%resElem1%) *QINVDres(c,i,%resElem1%)) ;

*-Value of import demand
 ResultMACRO("Level","Nominal","stIMPORT",%resElem1%)
            = SUM(c,PMres(c,%resElem1%) *QMres(c,%resElem1%)) ;

*-Value of export supply
 ResultMACRO("Level","Nominal","stEXPORT",%resElem1%)
            = SUM(c,PEres(c,%resElem1%) *QEres(c,%resElem1%)) ;

*-GDP from Expenditure side - C + I + G + E - M
 ResultMACRO("Level","Nominal","stGDP",%resElem1%)
            = SUM((c,h), (1+TVres(c,%resElem1%)) * PQDres(c,%resElem1%) *QCDres(c,h,%resElem1%))
                + SUM((cag,c,h),(1+TVres(c,%resElem1%)) * PQDres(c,%resElem1%) *QCD2res(cag,c,h,%resElem1%)$cces(c))
                + SUM(c,PQDres(c,%resElem1%) *QGDres(c,%resElem1%))
                + SUM((c,i),PQDres(c,%resElem1%) *QINVDres(c,i,%resElem1%))
*-               + SUM(c,PQDres(c,%resElem1%) * dstocconst(c))
                + SUM(c,PEres(c,%resElem1%)  *QEres(c,%resElem1%))
                - SUM(c,PMres(c,%resElem1%)  *QMres(c,%resElem1%)) ;

*-total domestic production
 ResultMACRO("Level","Nominal","stSUPPLY",%resElem1%)
            = SUM(c,PXCres(c,%resElem1%)*QXCres(c,%resElem1%)) ;

*-total intermediate inputs
 ResultMACRO("Level","Nominal","stUSE",%resElem1%)
            = SUM((c,a),PQDres(c,%resElem1%)* QINTDres(c,a,%resElem1%)) ;

*-household income
 ResultMACRO("Level","Nominal","stYHTOT",%resElem1%)
            = SUM(h,YHres(h,%resElem1%)) ;

*-government income
 ResultMACRO("Level","Nominal","stYGTOT",%resElem1%)      = SCALres("sYG",%resElem1%) ;

*-factor income
 ResultMACRO("Level","Nominal","stYFTOT",%resElem1%)      = SUM(f,YFres(f,%resElem1%)) ;

*-distributed factor income
 ResultMACRO("Level","Nominal","stYFDISPTOT",%resElem1%)  = SUM(f,YFDISPres(f,%resElem1%)) ;

*-Labour income
 ResultMACRO("Level","Nominal","stYFLABTOT",%resElem1%)   = SUM(l,YFres(l,%resElem1%)) ;

*-total savings
 ResultMACRO("Level","Nominal","stTOTSAV",%resElem1%)     = SCALres("sTOTSAV",%resElem1%) ;

*-household savings
 ResultMACRO("Level","Nominal","stHOSAV",%resElem1%)
            = SUM(h,YHres(h,%resElem1%) * (1-TYHres(h,%resElem1%))
                 *SHHres(h,%resElem1%)) ;

*-government savings
 ResultMACRO("Level","Nominal","stGOVSAV",%resElem1%)     = SCALres("sKAPGOV",%resElem1%) ;

*-foreign savings
 ResultMACRO("Level","Nominal","stFSAV",%resElem1%)       = SUM(w,ERres(w,%resElem1%) * KAPREGres(w,%resElem1%));

*-Depreciation
 ResultMACRO("Level","Nominal","stDEPREC",%resElem1%)     = SUM(f,deprec(f)*YFres(f,%resElem1%)) ;

*-Import tariff revenue
 ResultMACRO("Level","Nominal","stMTAX",%resElem1%)       = SCALres("sMTAX",%resElem1%) ;

*-Export tax revenue
 ResultMACRO("Level","Nominal","stETAX",%resElem1%)       = SCALres("sETAX",%resElem1%) ;

*-Sales tax revenue
 ResultMACRO("Level","Nominal","stSTAX",%resElem1%)       = SCALres("sSTAX",%resElem1%) ;

*-Indirect tax revenue
 ResultMACRO("Level","Nominal","stITAX",%resElem1%)       = SCALres("sITAX",%resElem1%) ;

*-Factor use tax revenue
 ResultMACRO("Level","Nominal","stFTAX",%resElem1%)       = SCALres("sFTAX",%resElem1%) ;

*-Factor income tax revenue
 ResultMACRO("Level","Nominal","stFYTAX",%resElem1%)      = SCALres("sFYTAX",%resElem1%) ;

*-Value added tax revenue
 ResultMACRO("Level","Nominal","stVTAX",%resElem1%)      = SCALres("sVTAX",%resElem1%) ;

*-Direct income tax revenue
 ResultMACRO("Level","Nominal","stDTAX",%resElem1%)       = SCALres("sDTAX",%resElem1%) ;
*-Intermediate input tax revenue
 ResultMACRO("Level","Nominal","stINTAX",%resElem1%)       = SCALres("sINTAX",%resElem1%) ;



*-Total tax revenue
 ResultMACRO("Level","Nominal","stTOTTAX",%resElem1%)     = SCALres("sMTAX",%resElem1%)
                                      + SCALres("sETAX",%resElem1%)
                                      + SCALres("sSTAX",%resElem1%)
                                      + SCALres("sEXTAX",%resElem1%)
                                      + SCALres("sITAX",%resElem1%)
                                      + SCALres("sFTAX",%resElem1%)
                                      + SCALres("sFYTAX",%resElem1%)
                                      + SCALres("sDTAX",%resElem1%)
                                      + SCALres("sVTAX",%resElem1%)
                                      + SCALres("sINTAX",%resElem1%)
*-                                    + SCALres("sASUBEQV",%resElem1%)
  ;

*-Real results
*-Value of government consumption
 ResultMACRO("Level","Real","stQCDTOT",%resElem1%)
            = SUM((c,h), PQD0(c) *QCDres(c,h,%resElem1%))
                + SUM((cag,c,h),PQD0(c) *QCD2res(cag,c,h,%resElem1%)$cces(c));

*-Value of enterprise consumption
 ResultMACRO("Level","Real","stQEDTOT",%resElem1%)
            = SUM((c,e),PQD0(c) *QEDres(c,e,%resElem1%)) ;

*-Value of government consumption

 ResultMACRO("Level","Real","stQGDTOT",%resElem1%)
            = SUM(c,PQD0(c) *QGDres(c,%resElem1%)) ;

*-Value of investment consumption
 ResultMACRO("Level","Real","stQINVTOT",%resElem1%)
            = SUM((c,i),PQD0(c) *QINVDres(c,i,%resElem1%)) ;

*-Value of Domestic final demand
 ResultMACRO("Level","Real","stQABSORP",%resElem1%)
            = SUM((c,h), PQD0(c) *QCDres(c,h,%resElem1%))
                + SUM((cag,c,h),PQD0(c) *QCD2res(cag,c,h,%resElem1%)$cces(c))
              + SUM((c,e),PQD0(c) *QEDres(c,e,%resElem1%))
              + SUM(c,PQD0(c) *QGDres(c,%resElem1%))
              + SUM((c,i),PQD0(c) *QINVDres(c,i,%resElem1%)) ;

*-Value of import demand
 ResultMACRO("Level","Real","stIMPORT",%resElem1%)
            = SUM(c,PM0(c) *QMres(c,%resElem1%)) ;

*-Value of export supply
 ResultMACRO("Level","Real","stEXPORT",%resElem1%)
            = SUM(c,PE0(c) *QEres(c,%resElem1%)) ;

*-GDP from Expenditure side - C + I + G + E - M
 ResultMACRO("Level","Real","stGDP",%resElem1%)
            = SUM((c,h), PQD0(c) *QCDres(c,h,%resElem1%))
                + SUM((cag,c,h),PQD0(c) *QCD2res(cag,c,h,%resElem1%)$cces(c))
                + SUM((c,e),PQD0(c) *QEDres(c,e,%resElem1%))
                + SUM(c,PQD0(c) *QGDres(c,%resElem1%))
                + SUM((c,i),PQD0(c) *QINVDres(c,i,%resElem1%))
*-               + SUM(c,PQD0(c) * dstocconst(c))
                + SUM(c,PE0(c)  *QEres(c,%resElem1%))
                - SUM(c,PM0(c)  *QMres(c,%resElem1%)) ;

*-total domestic production
 ResultMACRO("Level","Real","stSUPPLY",%resElem1%)
            = SUM(c,PXC0(c)*QXCres(c,%resElem1%)) ;

*-total intermediate inputs
 ResultMACRO("Level","Real","stUSE",%resElem1%)
            = SUM((c,a),PQD0(c)*QINTDres(c,a,%resElem1%)) ;


*-------- 2. Assign Macroeconomic Shares ---------------------------------

*---- 2a. Nominal Macroeconomic Shares in GDPEXP

*-Share of household consumption in GDPEXP
 ResultMACRO("ShareGDP","Nominal","stQCDTOT",%resElem1%)$ResultMACRO("Level","Nominal","stGDP",%resElem1%)
                         = (SUM((c,h), PQDres(c,%resElem1%) *QCDres(c,h,%resElem1%))
                            + SUM((cag,c,h),PQDres(c,%resElem1%) *QCD2res(cag,c,h,%resElem1%)$cces(c)))
                                /ResultMACRO("Level","Nominal","stGDP",%resElem1%) ;

*-Share of enterprise consumption in GDPEXP
 ResultMACRO("ShareGDP","Nominal","stQEDTOT",%resElem1%)$ResultMACRO("Level","Nominal","stGDP",%resElem1%)
            = SUM((c,e),PQDres(c,%resElem1%) *QEDres(c,e,%resElem1%))
                                /ResultMACRO("Level","Nominal","stGDP",%resElem1%) ;

*-Share of government consumption in GDPEXP
 ResultMACRO("ShareGDP","Nominal","stQGDTOT",%resElem1%)$ResultMACRO("Level","Nominal","stGDP",%resElem1%)
            = SUM(c,PQDres(c,%resElem1%) *QGDres(c,%resElem1%))
                                /ResultMACRO("Level","Nominal","stGDP",%resElem1%) ;

*-Share of investment consumption in GDPEXP
 ResultMACRO("ShareGDP","Nominal","stQINVTOT",%resElem1%)$ResultMACRO("Level","Nominal","stGDP",%resElem1%)
            = SUM((c,i),PQDres(c,%resElem1%) *QINVDres(c,i,%resElem1%))
                                /ResultMACRO("Level","Nominal","stGDP",%resElem1%) ;

*-Ratio of import demand to GDPEXP
 ResultMACRO("ShareGDP","Nominal","stIMPORT",%resElem1%)$ResultMACRO("Level","Nominal","stGDP",%resElem1%)
            = SUM(c,PMres(c,%resElem1%) *QMres(c,%resElem1%))
                                /ResultMACRO("Level","Nominal","stGDP",%resElem1%) ;

*-Ratio of export supply to GDPEXP
 ResultMACRO("ShareGDP","Nominal","stEXPORT",%resElem1%)$ResultMACRO("Level","Nominal","stGDP",%resElem1%)
            = SUM(c,PEres(c,%resElem1%) *QEres(c,%resElem1%))
                                /ResultMACRO("Level","Nominal","stGDP",%resElem1%) ;


*---- 2b. Nominal Macroeconomic Shares in ABSORP
*-Share of household consumption in ABSORP
 ResultMACRO("ShareABS","Nominal","stQCDTOT",%resElem1%)$resultMACRO("Level","Nominal","stQABSORP",%resElem1%)
            = (SUM((c,h), PQDres(c,%resElem1%) *QCDres(c,h,%resElem1%))
                + SUM((cag,c,h),PQDres(c,%resElem1%) *QCD2res(cag,c,h,%resElem1%)$cces(c)))
                                /resultMACRO("Level","Nominal","stQABSORP",%resElem1%) ;

*-Share of enterprise consumption in ABSORP
 ResultMACRO("ShareABS","Nominal","stQEDTOT",%resElem1%)$resultMACRO("Level","Nominal","stQABSORP",%resElem1%)
            = SUM((c,e),PQDres(c,%resElem1%) *QEDres(c,e,%resElem1%))
                                /resultMACRO("Level","Nominal","stQABSORP",%resElem1%) ;

*-Share of government consumption in ABSORP
 ResultMACRO("ShareABS","Nominal","stQGDTOT",%resElem1%)$resultMACRO("Level","Nominal","stQABSORP",%resElem1%)
            = SUM(c,PQDres(c,%resElem1%) *QGDres(c,%resElem1%))
                                /resultMACRO("Level","Nominal","stQABSORP",%resElem1%) ;

*-Share of investment consumption in ABSORP
 ResultMACRO("ShareABS","Nominal","stQINVTOT",%resElem1%)$resultMACRO("Level","Nominal","stQABSORP",%resElem1%)
            = SUM((c,i),PQDres(c,%resElem1%) *QINVDres(c,i,%resElem1%))
                                /resultMACRO("Level","Nominal","stQABSORP",%resElem1%) ;

*-Ration of import demand consumption to ABSORP
 ResultMACRO("ShareABS","Nominal","stIMPORT",%resElem1%)$resultMACRO("Level","Nominal","stQABSORP",%resElem1%)
            = SUM(c,PMres(c,%resElem1%) *QMres(c,%resElem1%))
                                /resultMACRO("Level","Nominal","stQABSORP",%resElem1%) ;

*-Ratio of export supply to ABSORP
 ResultMACRO("ShareABS","Nominal","stEXPORT",%resElem1%)$resultMACRO("Level","Nominal","stQABSORP",%resElem1%)
            = SUM(c,PEres(c,%resElem1%) *QEres(c,%resElem1%))
                                /resultMACRO("Level","Nominal","stQABSORP",%resElem1%) ;

*-------- 3. Assign Percentage Changes in Macroeconomic Totals -----------

*---- 3a. Percentage Change in Real Macroeconomic Totals

$iftheni.dyna %Mode% == dyna
 resultMacro("perc","Nominal",stab1,%resElem1%)$SUM(tp$(ord(tp)=1),resultMacro("Level","Nominal",stab1,%resElemTp%))
                              =  resultMacro("Level","Nominal",stab1,%resElem1%)
                                     / SUM(tp$(ord(tp)=1),resultMacro("Level","Nominal",stab1,%resElemTp%))*100 - 100;

 resultMacro("perc","Real",stab1,%resElem1%)$SUM(tp$(ord(tp)=1),resultMacro("Level","Real",stab1,%resElemTp%))
                              =  resultMacro("Level","Real",stab1,%resElem1%)
                                    / SUM(tp$(ord(tp)=1),resultMacro("Level","Real",stab1,%resElemTp%))*100 - 100;
$endif.dyna
 resultMacro("PerBase","Nominal",stab1,%resElem1%)$resultMacro("Level","Nominal",stab1,%resElemBs%)
                               = resultMacro("Level","Nominal",stab1,%resElem1%)
                                    / resultMacro("Level","Nominal",stab1,%resElemBs%)*100 - 100;

 resultMacro("PerBase","Real",stab1,%resElem1%)$resultMacro("Level","Real",stab1,%resElemBs%)
                               =  resultMacro("Level","Real",stab1,%resElem1%)
                                    / resultMacro("Level","Real",stab1,%resElemBs%)*100 - 100;

 nMACROTOT(stab1,%resElem1%) = resultMacro("Level","Nominal",stab1,%resElem1%)   ;

 rMACROTOT(stab1,%resElem1%) = resultMacro("Level","Real",stab1,%resElem1%)    ;

 nMACROSH1(stab1,%resElem1%) = resultMacro("ShareGDP","Nominal",stab1,%resElem1%)    ;

 nMACROSH2(stab1,%resElem1%) = resultMacro("ShareGDP","Nominal",stab1,%resElem1%)    ;

 rperMACROTOT(stab1,%resElem1%) = resultMacro("Perc","Real",stab1,%resElem1%) ;

 nperMACROTOT(stab1,%resElem1%) = resultMacro("Perc","Real",stab1,%resElem1%);

 nBasMACROTOT(stab1,%resElem1%) = resultMacro("PerBase","Nominal",stab1,%resElem1%);

 rBasMACROTOT(stab1,%resElem1%) = resultMacro("PerBase","Real",stab1,%resElem1%);

*------- 4. Exporting Macroeconomic Tables to GDX -----------------------

*-This writes the results data to GDX

Execute_Unload  '%resultF%/%mode%_%exp%_resmacro.gdx',
                   resultMacro
                   nMACROTOT,
                   nMACROSH1,
                   nMACROSH2,
                   rMACROTOT,
                   rperMACROTOT,
                   nperMACROTOT
   ;

*----------------- end of DEMETRA Macroeconomic Tables -----------------
