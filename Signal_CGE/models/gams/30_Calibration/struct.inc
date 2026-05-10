* ----------------- DEMETRA Structural Tables ---------------------------
$ontext
   The tables produced here provided descriptive statistics relating to
the macroeconomy and structural characterisitics of the database.

   The structure of this routine is
     *------- 1. Load Sets Used in this Module ---------------------------
     *------- 2. Define Structural Tables --------------------------------
                 * --- Macroeconomic Tables ---
                 * --- Commodity Tables ---
                 * --- Activity Tables ---
                 * --- Factor Tables ---
     * ------- 3. Assign Structural Tables -------------------------------
                 *---- 3a. Macroeconomic Tables ---
                 *---- 3b. Macroeconomic Shares ---
                 *---- 3c. Commodity account shares - indexed on stab3
                       * Demand Structures
                       * Supply Structures
                 *---- 3d. Aggregate Commodity account shares
                                 - indexed on stab3 and cagg
                       * Demand Structures
                       * Supply Structures
                 *---- 3e. Activity Tables ---
                 *---- 3f. Factor Tables ---
     * ------- 4. Exporting Structural Tables to GDX ---------------------
$offtext

*-------- 1. Load Sets Used in this Module --------------------------------
*-moved to proper places

*-------- 2. Define Structural Tables -------------------------------------

*- This section defines the structural tables that are used to report
*- descriptive statistics for the database used for this model
*$ontext


$include 30_Calibration\structSets.inc

PARAMETERS
*- --- Macroeconomic Tables ---

*-Macroeconomic tables - indexed on structElem1

 bMACROTOT(structElem1)      Base Macroeconomic totals
 bMACROSH1(structElem1)      Base Macroeconomic shares in GDP Expenditure
 bMACROSH2(structElem1)      Base Macroeconomic shares in Domestic Absorption

*- --- Commodity Tables ---

*- - Commodity account shares - indexed on structElem3

 bCOMMODST(structElem3,sac)     Base Commodity shares in c
 bCOMMODST2(structElem3,cagg)   Base Commodity shares in cagg
 bACTIVST2 (structElem3,aagg)   Base Commodity shares in cagg

*- --- Activity Tables ---

 bACTIVST(structElem4,a)      Base Activity shares in a

*- --- Factor Tables ---

 bFACTUSEST(structElem5,f,a)  Base factor use by activities and region

  ;

*- ------- 3. Assign Structural Tables ------------------------------------

*----- 3a. Macroeconomic Tables ---

*- Value of household consumption
 bMACROTOT("stQCDTOT")
            = SUM((c,h),PQD.L(c) * QCD.L(c,h)) ;

*- Value of government consumption
 bMACROTOT("stQGDTOT")
            = SUM(c,PQD.L(c) * QGD.L(c)) ;

*- Value of investment consumption
 bMACROTOT("stQINVTOT")
            = SUM((c,i),PQD.L(c) * QINVD.L(c,i)) ;

*- Value of Domestic final demand
 bMACROTOT("stQABSORP")
            = SUM((c,h),PQD.L(c) * QCD.L(c,h))
              + SUM(c,PQD.L(c) * QGD.L(c))
              + SUM((c,i),PQD.L(c) * QINVD.L(c,i)) ;

*- Value of import demand
 bMACROTOT("stIMPORT")
            = SUM(c,PM.L(c) * QM.L(c)) ;

*- Value of export supply
 bMACROTOT("stEXPORT")
            = SUM(c,PE.L(c) * QE.L(c)) ;

*- GDP from Expenditure side - C + I + G + E - M
 bMACROTOT("stGDP")
            = SUM((c,h),PQD.L(c) * QCD.L(c,h))
                + SUM(c,PQD.L(c) * QGD.L(c))
                + SUM((c,i),PQD.L(c) * QINVD.L(c,i))
                + SUM(c,PE.L(c) * QE.L(c))
                - SUM(c,PM.L(c) * QM.L(c)) ;

*- total domestic production
 bMACROTOT("stSUPPLY")     = SUM(c,PXC.L(c)* QXC.L(c)) ;

*- total intermediate inputs
 bMACROTOT("stUSE")        = SUM((c,a),PQD.L(c)* QINTD.L(c,a)) ;

*- household income
 bMACROTOT("stYHTOT")      = SUM(h,YH.L(h)) ;

*- government income
 bMACROTOT("stYGTOT")      = YG.L ;

*- factor income
 bMACROTOT("stYFTOT")      = SUM(f,YF.L(f)) ;

*- distributed factor income
 bMACROTOT("stYFDISPTOT")  = SUM(f,YFDISP.L(f)) ;

*- Labour income
 bMACROTOT("stYFLABTOT")   = SUM(l,YF.L(l)) ;

*- total savings
 bMACROTOT("stTOTSAV")     = TOTSAV.L ;

*- household savings
 bMACROTOT("stHOSAV")      = SUM(h,YH.L(h) * (1-TYH.L(h)) * SHH.L(h)) ;

*- government savings
 bMACROTOT("stGOVSAV")     = KAPGOV.L ;

*- foreign savings
 bMACROTOT("stFSAV")       = SUM(w,KAPREG.L(w)*ER.L(w)) ;

*- Depreciation
 bMACROTOT("stDEPREC")     = SUM(f,deprec(f)*YF.L(f)) ;

*- Import tariff revenue
 bMACROTOT("stMTAX")       = MTAX.L ;

*- Export tax revenue
 bMACROTOT("stETAX")       = ETAX.L ;

*- Sales tax revenue
 bMACROTOT("stSTAX")       = STAX.L ;

*- Indirect tax revenue
 bMACROTOT("stITAX")       = ITAX.L ;

*- Factor tax revenue
 bMACROTOT("stFTAX")       = FTAX.L ;

*- Factor Income tax revenue
 bMACROTOT("stFYTAX")      = FYTAX.L ;

*- Direct Household and enterprise income tax revenue
 bMACROTOT("stDTAX")       = DTAX.L ;

*- Total Tax revenue
 bMACROTOT("stTOTTAX")     = MTAX.L + ETAX.L + STAX.L + ITAX.L
                             + FTAX.L + FYTAX.L + DTAX.L ;

*----- 3b. Macroeconomic Shares ---

*- Share of household consumption in GDPEXP
 bMACROSH1("stQCDTOT")$bMACROTOT("stGDP")
                         = SUM((c,h),PQD.L(c) * QCD.L(c,h))
                                /bMACROTOT("stGDP") ;

*- Share of government consumption in GDPEXP
 bMACROSH1("stQGDTOT")$bMACROTOT("stGDP")
            = SUM(c,PQD.L(c) * QGD.L(c))
                                /bMACROTOT("stGDP") ;

*- Share of investment consumption in GDPEXP
 bMACROSH1("stQINVTOT")$bMACROTOT("stGDP")
            = SUM((c,i),PQD.L(c) * QINVD.L(c,i))
                     /bMACROTOT("stGDP") ;

*- Ratio of import demand to GDPEXP
 bMACROSH1("stIMPORT")$bMACROTOT("stGDP")
            = SUM(c,PM.L(c) * QM.L(c))
                                /bMACROTOT("stGDP") ;

*- Ratio of export supply to GDPEXP
 bMACROSH1("stEXPORT")$bMACROTOT("stGDP")
            = SUM(c,PE.L(c) * QE.L(c))
                                /bMACROTOT("stGDP") ;

*- Share of household consumption in ABSORP
 bMACROSH2("stQCDTOT")$bMACROTOT("stQABSORP")
            = SUM((c,h),PQD.L(c) * QCD.L(c,h))
                                /bMACROTOT("stQABSORP") ;

*- Share of government consumption in ABSORP
 bMACROSH2("stQGDTOT")$bMACROTOT("stQABSORP")
            = SUM(c,PQD.L(c) * QGD.L(c))
                                /bMACROTOT("stQABSORP") ;

*- Share of investment consumption in ABSORP
 bMACROSH2("stQINVTOT")$bMACROTOT("stQABSORP")
            = SUM((c,i),PQD.L(c) * QINVD.L(c,i))
                                /bMACROTOT("stQABSORP") ;

*- Ration of import demand consumption to ABSORP
 bMACROSH2("stIMPORT")$bMACROTOT("stQABSORP")
            = SUM(c,PM.L(c) * QM.L(c))
                                /bMACROTOT("stQABSORP") ;

*- Ratio of export supply to ABSORP
 bMACROSH2("stEXPORT")$bMACROTOT("stQABSORP")
            = SUM(c,PE.L(c) * QE.L(c))
                                /bMACROTOT("stQABSORP") ;


*----- 3c. Commodity account shares - indexed on stab3

*- Demand Structures

 bCOMMODST("stPRIVregDEM",c)$(PQD.L(c)*(SUM(h,QCD.L(c,h)) + QGD.L(c)
                                          + sum(i,QINVD.L(c,i))) + sum(a,QINTD.L(c,a)))
           = SUM(h,(PQD.L(c)* QCD.L(c,h)))
               /(PQD.L(c)*(SUM(h,QCD.L(c,h)) + QGD.L(c)
                       + sum(i,QINVD.L(c,i))  + sum(a,QINTD.L(c,a))))  ;

 bCOMMODST("stGOVTregDEM",c)$(PQD.L(c)*(SUM(h,QCD.L(c,h)) + QGD.L(c)
                                          + sum(i,QINVD.L(c,i))   + sum(a,QINTD.L(c,a))))
           = (PQD.L(c)* QGD.L(c))
               /(PQD.L(c)*(SUM(h,QCD.L(c,h)) + QGD.L(c)
                            + sum(i,QINVD.L(c,i))  + sum(a,QINTD.L(c,a))))  ;

 bCOMMODST("stINVDregDEM",c)$(PQD.L(c)*(SUM(h,QCD.L(c,h)) + QGD.L(c)
                                          + sum(i,QINVD.L(c,i))  + sum(a,QINTD.L(c,a))))
           = (PQD.L(c)* (sum(i,QINVD.L(c,i)) ))
               /(PQD.L(c)*(SUM(h,QCD.L(c,h)) + QGD.L(c)
                            + sum(i,QINVD.L(c,i)))  + sum(a,QINTD.L(c,a)))  ;

 bCOMMODST("stINTDregDEM",c)$(PQD.L(c)*(SUM(h,QCD.L(c,h)) + QGD.L(c)
                                          + sum(i,QINVD.L(c,i)) + sum(a,QINTD.L(c,a))))
           = (PQD.L(c)* sum(a,QINTD.L(c,a)))
               /(PQD.L(c)*(SUM(h,QCD.L(c,h)) + QGD.L(c)
                            + sum(i,QINVD.L(c,i)) + sum(a,QINTD.L(c,a))))  ;

 bCOMMODST("stregCHK",c)  = (bCOMMODST("stPRIVregDEM",c)
                              + bCOMMODST("stGOVTregDEM",c)
                              + bCOMMODST("stINVDregDEM",c)
                              + bCOMMODST("stINTDregDEM",c)) - 1 ;

 bCOMMODST("stPRIVcomDEM",c)$SUM((cp,h),PQD.L(cp)* QCD.L(cp,h))
           = SUM(h,(PQD.L(c)* QCD.L(c,h)))
               /SUM((cp,h),PQD.L(cp)* QCD.L(cp,h)) ;

 bCOMMODST("stGOVTcomDEM",c)$SUM(cp,PQD.L(cp)* QGD.L(cp))
           = (PQD.L(c)* QGD.L(c))
               /SUM(cp,PQD.L(cp)* QGD.L(cp)) ;

 bCOMMODST("stINVDcomDEM",c)$SUM(cp,PQD.L(cp)* (sum(i,QINVD.L(cp,i)) ))
           = (PQD.L(c)* (sum(i,QINVD.L(c,i)) ))
               /SUM((cp,i),PQD.L(cp)* QINVD.L(cp,i) ) ;

 bCOMMODST("stINTDcomDEM",c)$SUM((cp,a),PQD.L(cp)* QINTD.L(cp,a))
           = (PQD.L(c)* sum(a,QINTD.L(c,a)))
               /SUM((cp,a),PQD.L(cp)* QINTD.L(cp,a)) ;


 bCOMMODST("stPRIVcomDEM","total")  = SUM(c,bCOMMODST("stPRIVcomDEM",c)) - 1 ;
 bCOMMODST("stGOVTcomDEM","total")  = SUM(c,bCOMMODST("stGOVTcomDEM",c)) - 1 ;
 bCOMMODST("stINVDcomDEM","total")  = SUM(c,bCOMMODST("stINVDcomDEM",c)) - 1 ;
 bCOMMODST("stINTDcomDEM","total")  = SUM(c,bCOMMODST("stINTDcomDEM",c)) - 1 ;

 bCOMMODST('EXP-OUTshr',c)$(PXC.L(C)*QXC.L(C))
  = PE.L(C)*QE.L(C)/(PXC.L(C)*QXC.L(C));

 bCOMMODST('IMP-DEMshr',c)$(PQS.L(C)*(1 - TS.L(C))*QQ.L(C))
  = PM.L(C)*QM.L(C)/(PQS.L(C)*(1 - TS.L(C))*QQ.L(C));


*- Supply Structures

 bCOMMODST("stMAKEcomSUP",c)$SUM(cp,PXC.L(cp)* QXC.L(cp))
           = (PXC.L(c)* QXC.L(c))
              /SUM(cp,PXC.L(cp)* QXC.L(cp)) ;

 bCOMMODST("stQMcomSUP",c)$SUM(cp,PM.L(cp)* QM.L(cp))
           = (PM.L(c)* QM.L(c))
              /SUM(cp,PM.L(cp)* QM.L(cp)) ;

 bCOMMODST("stQDcomSUP",c)$SUM(cp,PD.L(cp)* QD.L(cp))
           = (PD.L(c)* QD.L(c))
              /SUM(cp,PD.L(cp)* QD.L(cp)) ;

 bCOMMODST("stSUPPcomSUP",c)$SUM(cp,(PD.L(cp)* QD.L(cp))
                                      + (PM.L(cp)* QM.L(cp)))
           = ((PD.L(c)* QD.L(c))+(PM.L(c)* QM.L(c)))
               /SUM(cp,(PD.L(cp)* QD.L(cp))
                 + (PM.L(cp)* QM.L(cp))) ;

 bCOMMODST("stQEconSUP",c)$SUM(cp,PE.L(cp)* QE.L(cp))
           = (PE.L(c)* QE.L(c))
               /SUM(cp,PE.L(cp)* QE.L(cp)) ;

*----- 3d. Aggregate Commodity account shares - indexed on stab3 and cagg

*- Demand Structures

 bCOMMODST2("stPRIVregDEM",cagg)$SUM(c$map_cagg_c(cagg,c),(PQD.L(c)*(SUM(h,QCD.L(c,h)) + QGD.L(c)
                       + sum(i,QINVD.L(c,i))  + sum(a,QINTD.L(c,a)))))
           = SUM(c$map_cagg_c(cagg,c),SUM(h,(PQD.L(c)* QCD.L(c,h))))
               /SUM(c$map_cagg_c(cagg,c),(PQD.L(c)*(SUM(h,QCD.L(c,h)) + QGD.L(c)
                       + sum(i,QINVD.L(c,i))  + sum(a,QINTD.L(c,a)))))  ;

 bCOMMODST2("stGOVTregDEM",cagg)$SUM(c$map_cagg_c(cagg,c),(PQD.L(c)*(SUM(h,QCD.L(c,h))
                     + QGD.L(c) + sum(i,QINVD.L(c,i))  + sum(a,QINTD.L(c,a)))))
           = SUM(c$map_cagg_c(cagg,c),(PQD.L(c)* QGD.L(c)))
              /SUM(c$map_cagg_c(cagg,c),(PQD.L(c)*(SUM(h,QCD.L(c,h))
                     + QGD.L(c) + sum(i,QINVD.L(c,i)) + sum(a,QINTD.L(c,a)))))  ;

 bCOMMODST2("stINVDregDEM",cagg)$SUM(c$map_cagg_c(cagg,c),(PQD.L(c)*(SUM(h,QCD.L(c,h))
                     + QGD.L(c) + sum(i,QINVD.L(c,i))  + sum(a,QINTD.L(c,a)))))
           = SUM(c$map_cagg_c(cagg,c),(PQD.L(c)* (sum(i,QINVD.L(c,i)) )))
              /SUM(c$map_cagg_c(cagg,c),(PQD.L(c)*(SUM(h,QCD.L(c,h))
                     + QGD.L(c) + sum(i,QINVD.L(c,i))  + sum(a,QINTD.L(c,a)))))  ;

 bCOMMODST2("stINTDregDEM",cagg)$SUM(c$map_cagg_c(cagg,c),(PQD.L(c)*(SUM(h,QCD.L(c,h)) + QGD.L(c)
                            + sum(i,QINVD.L(c,i)) + sum(a,QINTD.L(c,a)))))
           = SUM(c$map_cagg_c(cagg,c),(PQD.L(c)* sum(a,QINTD.L(c,a))))
               /SUM(c$map_cagg_c(cagg,c),(PQD.L(c)*(SUM(h,QCD.L(c,h)) + QGD.L(c)
                            + sum(i,QINVD.L(c,i))  + sum(a,QINTD.L(c,a)))))  ;

 bCOMMODST2("stregCHK",cagg)  = (bCOMMODST2("stPRIVregDEM",cagg)
                              + bCOMMODST2("stGOVTregDEM",cagg)
                              + bCOMMODST2("stINVDregDEM",cagg)
                              + bCOMMODST2("stINTDregDEM",cagg)) - 1 ;

 bCOMMODST2("stPRIVcomDEM",cagg)$SUM((cp,h),PQD.L(cp)* QCD.L(cp,h))
           = SUM(c$map_cagg_c(cagg,c),SUM(h,(PQD.L(c)* QCD.L(c,h))))
               /SUM((cp,h),PQD.L(cp)* QCD.L(cp,h)) ;

 bCOMMODST2("stGOVTcomDEM",cagg)$SUM(cp,PQD.L(cp)* QGD.L(cp))
           = SUM(c$map_cagg_c(cagg,c),(PQD.L(c)* QGD.L(c)))
               /SUM(cp,PQD.L(cp)* QGD.L(cp)) ;

 bCOMMODST2("stINVDcomDEM",cagg)$SUM((cp,i),PQD.L(cp)* QINVD.L(cp,i)  )
           = SUM(c$map_cagg_c(cagg,c),(PQD.L(c)* (sum(i,QINVD.L(c,i)) )))
               /SUM((cp,i),PQD.L(cp)* QINVD.L(cp,i)) ;

 bCOMMODST2("stINTDcomDEM",cagg)$SUM((cp,a),PQD.L(cp)* QINTD.L(cp,a))
           = SUM(c$map_cagg_c(cagg,c),(PQD.L(c)* sum(a,QINTD.L(c,a))))
               /SUM((cp,a),PQD.L(cp)* QINTD.L(cp,a)) ;

*- Supply Structures

 bCOMMODST2("stMAKEcomSUP",cagg)$SUM(cp,PXC.L(cp)* QXC.L(cp))
           = SUM(c$map_cagg_c(cagg,c),(PXC.L(c)* QXC.L(c)))
              /SUM(cp,PXC.L(cp)* QXC.L(cp)) ;

 bCOMMODST2("stQMcomSUP",cagg)$SUM(cp,PM.L(cp)* QM.L(cp))
           = SUM(c$map_cagg_c(cagg,c),(PM.L(c)* QM.L(c)))
              /SUM(cp,PM.L(cp)* QM.L(cp)) ;

 bCOMMODST2("stQDcomSUP",cagg)$SUM(cp,PD.L(cp)* QD.L(cp))
           = SUM(c$map_cagg_c(cagg,c),(PD.L(c)* QD.L(c)))
              /SUM(cp,PD.L(cp)* QD.L(cp)) ;

 bCOMMODST2("stSUPPcomSUP",cagg)$SUM(cp,(PD.L(cp)* QD.L(cp))
                                      + (PM.L(cp)* QM.L(cp)))
           = SUM(c$map_cagg_c(cagg,c),((PD.L(c)* QD.L(c))+(PM.L(c)* QM.L(c))))
               /SUM(cp,(PD.L(cp)* QD.L(cp))
                 + (PM.L(cp)* QM.L(cp))) ;

 bCOMMODST2("stQEconSUP",cagg)$SUM(cp,PE.L(cp)* QE.L(cp))
           = SUM(c$map_cagg_c(cagg,c),(PE.L(c)* QE.L(c)))
               /SUM(cp,PE.L(cp)* QE.L(cp)) ;

 bCOMMODST2('EXP-OUTshr',cagg)$SUM(c$map_cagg_c(cagg,c),(PXC.L(C)*QXC.L(C)))
*SUM(cp,(PXC.L(Cp)*QXC.L(Cp)))
           = SUM(c$map_cagg_c(cagg,c), PE.L(C)*QE.L(C))
             /SUM(c$map_cagg_c(cagg,c),(PXC.L(C)*QXC.L(C)));

 bCOMMODST2('IMP-DEMshr',cagg)$sum(c$map_cagg_c(cagg,c),(PQS.L(C)*(1 - TS.L(C))*QQ.L(C)))
*SUM(cp,(PQS.L(Cp)*(1 - TS.L(Cp))*QQ.L(Cp)))
          = sum(c$map_cagg_c(cagg,c), PM.L(C)*QM.L(C))
            /sum(c$map_cagg_c(cagg,c),(PQS.L(C)*(1 - TS.L(C))*QQ.L(C)));

* bACTIVST2("stLAB",aagg)$sum(ap,VVA.L(ap))
*                     = SUM((a$(map_aagg_a(aagg,a),l),(WF.L(l)*WFDIST.L(l,a)*FD.L(l,a))
*                            /sum(a$map_aagg_a(aagg,a),(VVA.L(a))) ;

* bACTIVST2("stCAP",aagg)$sum(ap,VVA.L(ap))
*                     = SUM((a$map_aagg_a(aagg,a),k), (WF.L(k)*WFDIST.L(k,a)*FD.L(k,a))
*                           /sum(a$map_aagg_a(aagg,a),(VVA.L(a))) ;


 bACTIVST2("stVA",aagg)$(SUM(ap,VVA.L(ap)))
                    = sum(a$map_aagg_a(aagg,a),(VVA.L(a))/SUM(ap,VVA.L(ap))) ;


*-DISPLAY bCOMMODST, bCOMMODST2, map_cagg_c ;

*----- 3e. Activity Tables ---

 bACTIVST("stQINTQX",a)$(SUM(ap,PX.L(ap)*QX.L(ap)))
                    = (PINT.L(a)*QINT.L(a))/SUM(ap,PX.L(ap)*QX.L(ap)) ;

 bACTIVST("stQINT",a)$(SUM(ap,PINT.L(ap)*QINT.L(ap)))
                    = (PINT.L(a)*QINT.L(a))/SUM(ap,PINT.L(ap)*QINT.L(ap)) ;

 bACTIVST("stVAQX",a)$(SUM(ap,PX.L(ap)*QX.L(ap)))
                    = (VVA.L(a))/SUM(ap,PX.L(ap)*QX.L(ap)) ;

 bACTIVST("stVA",a)$(SUM(ap,PVA.L(ap)*QVA.L(ap)))
                    = (VVA.L(a))/SUM(ap,PVA.L(ap)*QVA.L(ap)) ;

 bACTIVST("stQX",a)$(SUM(ap,PX.L(ap)*QX.L(ap)))
                     = (PX.L(a)*QX.L(a))/SUM(ap,PX.L(ap)*QX.L(ap)) ;

 bACTIVST("stLAB",a)$(VVA.L(a))
                     = (SUM(l,WF.L(l)*WFDIST.L(l,a)*FD.L(l,a)))
                           /(VVA.L(a)) ;

 bACTIVST("stUskLAB",a)$(VVA.L(a))
                     = (SUM(lu,WF.L(lu)*WFDIST.L(lu,a)*FD.L(lu,a)))
                           /(VVA.L(a)) ;

 bACTIVST("stSkLAB",a)$(VVA.L(a))
                     = (SUM(ls,WF.L(ls)*WFDIST.L(ls,a)*FD.L(ls,a)))
                           /(VVA.L(a)) ;

 bACTIVST("stSekLAB",a)$(VVA.L(a))
                     = (SUM(lm,WF.L(lm)*WFDIST.L(lm,a)*FD.L(lm,a)))
                           /(VVA.L(a)) ;


 bACTIVST("stCAP",a)$(VVA.L(a))
                     = (SUM(k,WF.L(k)*WFDIST.L(k,a)*FD.L(k,a)))
                           /(VVA.L(a)) ;

 bACTIVST("stLND",a)$(VVA.L(a))
                     = (SUM(n,WF.L(n)*WFDIST.L(n,a)*FD.L(n,a)))
                           /(VVA.L(a)) ;

 bACTIVST("stFTAX",a)$(VVA.L(a))
              = (SUM(f,TF.L(f,a)*WF.L(f)*WFDIST.L(f,a)*FD.L(f,a)))
                          /(VVA.L(a)) ;

*- bACTIVST("stFSUB",a)$(PX.L(a)*QX.L(a))
*-              = (TAAG1.L(a)+(TASUBEQV.L(a)*PX.L(a)*QX.L(a)))
*-                          /(PX.L(a)*QX.L(a)) ;

 bACTIVST("stFACTchk",a)
                     = bACTIVST("stLAB",a)
                       + bACTIVST("stCAP",a) + bACTIVST("stLND",a)
                       + bACTIVST("stFTAX",a) ;

 bACTIVST("stSUB",a)$aqx(a)    = 1 ;


*----- 3f. Factor Tables ---

*- Assigning factor tables

 bFACTUSEST("stTRANS",f,a)
                     = (WF.L(f) * WFDIST.L(f,a) * FD.L(f,a)) ;

 bFACTUSEST("stACTSH",f,a)$(SUM(fp,bFACTUSEST("stTRANS",fp,a)))
                     = bFACTUSEST("stTRANS",f,a)
                          /(SUM(fp,bFACTUSEST("stTRANS",fp,a))) ;

 bFACTUSEST("stFFSH",f,a)$(SUM(ap,bFACTUSEST("stTRANS",f,ap)))
                     = bFACTUSEST("stTRANS",f,a)
                          /(SUM(ap,bFACTUSEST("stTRANS",f,ap))) ;



*- ------- 4. Exporting Structural Tables to GDX --------------------------

*- This writes the results data to GDX

Execute_Unload  '%gdxF%\DEMETRA_struct_info.gdx',

bMACROTOT,
bMACROSH1,
bMACROSH2

bCOMMODST,
bCOMMODST2,
bACTIVST2,

bACTIVST,

bFACTUSEST

   ;

*$offtext
*- ----------------- end of DEMETRA Structural Tables ------------------------
