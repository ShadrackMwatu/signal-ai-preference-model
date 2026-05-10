*------------------------------------------------------------------------------
*------------------------------------------------------------------------------
*-
*-
*-   GAMS file : resassign.inc
*-
*-   @purpose  : Assigns results to the main container
*-   @author   :
*-   @date     :
*-   @since    :
*-   @refDoc   :
*-   @seeAlso  :
*-   @calledBy : *_experiment_*.gms
*------------------------------------------------------------------------------
*------------------------------------------------------------------------------


*-------- assign result parameters ----------------------------------
$onDotL
result("Level","sER",w,"Nan","NaN","NaN",%resElem1%)           = ER(w)                            ;
result("Level","sERX","NaN","Nan","NaN","NaN",%resElem1%)      = ERX                              ;
result("Level","sCPI","NaN","Nan","NaN","NaN",%resElem1%)      = CPI                              ;
result("Level","sPPI","NaN","Nan","NaN","NaN",%resElem1%)      = PPI                              ;
result("Level","sMTAX","NaN","Nan","NaN","NaN",%resElem1%)     = MTAX                             ;
result("Level","sETAX","NaN","Nan","NaN","NaN",%resElem1%)     = ETAX                             ;
result("Level","sSTAX","NaN","Nan","NaN","NaN",%resElem1%)     = STAX                             ;
result("Level","sVTAX","NaN","Nan","NaN","NaN",%resElem1%)     = VTAX + DVTAX*vtax01              ;
result("Level","sITAX","NaN","Nan","NaN","NaN",%resElem1%)     = ITAX                             ;
result("Level","sFTAX","NaN","Nan","NaN","NaN",%resElem1%)     = FTAX                             ;
result("Level","sDTAX","NaN","Nan","NaN","NaN",%resElem1%)     = DTAX                             ;
result("Level","sFYTAX","NaN","Nan","NaN","NaN",%resElem1%)    = FYTAX                            ;
result("Level","sYG","NaN","Nan","NaN","NaN",%resElem1%)       = YG                               ;
result("Level","sEG","NaN","Nan","NaN","NaN",%resElem1%)       = EG                               ;
result("Level","sGBUDG","NaN","Nan","NaN","NaN",%resElem1%)    = GBUDG                            ;
result("Level","sINVEST","NaN","Nan","NaN","NaN",%resElem1%)   = INVEST                           ;
result("Level","sTOTSAV","NaN","Nan","NaN","NaN",%resElem1%)   = TOTSAV                           ;
result("Level","sKAPGOV","NaN","Nan","NaN","NaN",%resElem1%)   = KAPGOV                           ;
result("Level","sKAPWOR","NaN","Nan","NaN","NaN",%resElem1%)   = KAPWOR                           ;
result("Level","sKAPREG",w,"Nan","NaN","NaN",%resElem1%)       = KAPREG(w)                        ;
result("Level","sVFDOMD","NaN","Nan","NaN","NaN",%resElem1%)   = VFDOMD                           ;
result("Level","sVGD","NaN","Nan","NaN","NaN",%resElem1%)      = VGD                              ;
result("Level","sINVESTSH","NaN","Nan","NaN","NaN",%resElem1%) = INVESTSH                         ;
result("Level","sVGDSH","NaN","Nan","NaN","NaN",%resElem1%)    = VGDSH                            ;
result("Level","sGDP","NaN","Nan","NaN","NaN",%resElem1%)      = GDP                              ;
result("Level","sRGDP","NaN","Nan","NaN","NaN",%resElem1%)     = RGDP                             ;
result("Level","sRGDPFC","NaN","Nan","NaN","NaN",%resElem1%)   = RGDPFC                           ;
result("Level","sWALRAS","NaN","Nan","NaN","NaN",%resElem1%)   = WALRAS                           ;

*-solution statistics
result("Level",'MODEL-STAT',"NaN","Nan","NaN","NaN",%resElem1%)= demetra.MODELSTAT                ;
result("Level",'SOLVE-STAT',"NaN","Nan","NaN","NaN",%resElem1%)= demetra.SOLVESTAT                ;
result("Level",'NUM-REDEFQ',"NaN","Nan","NaN","NaN",%resElem1%)= demetra.NUMREDEF                 ;
result("Level",'iterUsd',"NaN","Nan","NaN","NaN",%resElem1%)   = demetra.iterUsd                  ;


result("Level","aQEDADJ","NaN","Nan","NaN","NaN",%resElem1%)   = QEDADJ                           ;
result("Level","aHEADJ","NaN","Nan","NaN","NaN",%resElem1%)    = HEADJ                            ;
result("Level","aTEADJ",w,"Nan","NaN","NaN",%resElem1%)        = TEADJ(w)                         ;
result("Level","aTMADJ",c,w,"NaN","NaN",%resElem1%)            = TMADJ(w,c)                       ;
result("Level","aTSADJ","NaN","Nan","NaN","NaN",%resElem1%)    = TSADJ                            ;
result("Level","aTVADJ","NaN","Nan","NaN","NaN",%resElem1%)    = TVADJ                            ;
result("Level","aTXADJ","NaN","Nan","NaN","NaN",%resElem1%)    = TXADJ                            ;
result("Level","aTFADJ","NaN","Nan","NaN","NaN",%resElem1%)    = TFADJ                            ;
result("Level","aTYFADJ","NaN","Nan","NaN","NaN",%resElem1%)   = TYFADJ                           ;
result("Level","aTYHADJ","NaN","Nan","NaN","NaN",%resElem1%)   = TYHADJ                           ;
result("Level","aTYADJ","NaN","Nan","NaN","NaN",%resElem1%)    = TYADJ                            ;
result("Level","aTYEADJ","NaN","Nan","NaN","NaN",%resElem1%)   = TYEADJ                           ;
result("Level","aTHCADJ","NaN","Nan","NaN","NaN",%resElem1%)   = THCADJ                           ;
result("Level","aDTE",w,"Nan","NaN","NaN",%resElem1%)          = DTE(w)                           ;
result("Level","aDTM",w,"Nan","NaN","NaN",%resElem1%)          = DTM(w)                           ;
result("Level","aDTS","NaN","Nan","NaN","NaN",%resElem1%)      = DTS                              ;
result("Level","aDTV","NaN","Nan","NaN","NaN",%resElem1%)      = DTV                              ;
result("Level","aDTX","NaN","Nan","NaN","NaN",%resElem1%)      = DTX                              ;
result("Level","aDTF","NaN","Nan","NaN","NaN",%resElem1%)      = DTF                              ;
result("Level","aDTYF","NaN","Nan","NaN","NaN",%resElem1%)     = DTYF                             ;
result("Level","aDTYH","NaN","Nan","NaN","NaN",%resElem1%)     = DTYH                             ;
result("Level","aDTY","NaN","Nan","NaN","NaN",%resElem1%)      = DTY                              ;
result("Level","aDTYE","NaN","Nan","NaN","NaN",%resElem1%)     = DTYE                             ;
result("Level","aDTHC","NaN","Nan","NaN","NaN",%resElem1%)     = DTHC                             ;
result("Level","aQGDADJ","NaN","Nan","NaN","NaN",%resElem1%)   = QGDADJ                           ;
result("Level","aQGDADJceh","NaN","Nan","NaN","NaN",%resElem1%)= QGDADJceh                        ;
result("Level","aQGDADJoth","NaN","Nan","NaN","NaN",%resElem1%)= QGDADJoth                        ;
result("Level","aQGDADJext","NaN","Nan","NaN","NaN",%resElem1%)= QGDADJext                        ;
result("Level","QGDADJc",c,"Nan","NaN","NaN",%resElem1%)       = QGDADJc(c)                       ;
result("Level","aHGADJ","NaN","Nan","NaN","NaN",%resElem1%)    = HGADJ                            ;
result("Level","aEGADJ","NaN","Nan","NaN","NaN",%resElem1%)    = EGADJ                            ;
result("Level","aSADJ","NaN","Nan","NaN","NaN",%resElem1%)     = SADJ                             ;
result("Level","aSHADJ","NaN","Nan","NaN","NaN",%resElem1%)    = SHADJ                            ;
result("Level","aSEADJ","NaN","Nan","NaN","NaN",%resElem1%)    = SEADJ                            ;
result("Level","aDSHH","NaN","Nan","NaN","NaN",%resElem1%)     = DSHH                             ;
result("Level","aDS","NaN","Nan","NaN","NaN",%resElem1%)       = DS                               ;
result("Level","aDSEN","NaN","Nan","NaN","NaN",%resElem1%)     = DSEN                             ;
result("Level","aIADJ","NaN","Nan","NaN","NaN",%resElem1%)     = IADJ                             ;

result("Level","PWE",c,"NaN","NaN","NaN",%resElem1%)           = PWE(c)                           ;
result("Level","PE",c,"NaN","NaN","NaN",%resElem1%)            = PE(c)                            ;
result("Level","COMTOTSH",c,"NaN","NaN","NaN",%resElem1%)      = COMTOTSH(c)                      ;
result("Level","VQCD",c,"NaN","NaN","NaN",%resElem1%)          = VQCD(c)                          ;
result("Level","PER",c,w,"NaN","NaN",%resElem1%)               = PER(c,w)                         ;
result("Level","PD",c,"NaN","NaN","NaN",%resElem1%)            = PD(c)                            ;
result("Level","QE",c,"NaN","NaN","NaN",%resElem1%)            = QE(c)                            ;
result("Level","QER",c,w,"NaN","NaN",%resElem1%)               = QER(c,w)                         ;
result("Level","QD",c,"NaN","NaN","NaN",%resElem1%)            = QD(c)                            ;
result("Level","PWM",c,"NaN","NaN","NaN",%resElem1%)           = PWM(c)                           ;
result("Level","PM",c,"NaN","NaN","NaN",%resElem1%)            = PM(c)                            ;
result("Level","PMR",w,c,"NaN","NaN",%resElem1%)               = PMR(w,c)                         ;
result("Level","QM",c,"NaN","NaN","NaN",%resElem1%)            = QM(c)                            ;
result("Level","QMR",w,c,"NaN","NaN",%resElem1%)               = QMR(w,c)                         ;
result("Level","QQ",c,"NaN","NaN","NaN",%resElem1%)            = QQ(c)                            ;
result("Level","PTT",m,"NaN","NaN","NaN",%resElem1%)           = PTT(m)                           ;
result("Level","IOQTTQQ",m,c,"NaN","NaN",%resElem1%)           = IOQTTQQ(m,c)                     ;
result("Level","QTT",m,"NaN","NaN","NaN",%resElem1%)           = QTT(m)                           ;
result("Level","QTTD",c,"NaN","NaN","NaN",%resElem1%)          = QTTD(c)                          ;
result("Level","PQS",c,"NaN","NaN","NaN",%resElem1%)           = PQS(c)                           ;
result("Level","PQD",cc,"NaN","NaN","NaN",%resElem1%)          = PQD(cc)                          ;
result("Level","PQCD",cc,h,"NaN","NaN",%resElem1%)             = PQCD(cc,h)                       ;
result("Level","PQC",cc,h,"NaN","NaN",%resElem1%)              = PQC(cc,h)                        ;
result("Level","PX",a,"NaN","NaN","NaN",%resElem1%)            = PX(a)                            ;
result("Level","PVA",a,"NaN","NaN","NaN",%resElem1%)           = PVA(a)                           ;
result("Level","PINT",a,"NaN","NaN","NaN",%resElem1%)          = PINT(a)                          ;
result("Level","AD",ff,a,"NaN","NaN",%resElem1%)               = AD(ff,a)                         ;
result("Level","ADFD",ff,a,"NaN","NaN",%resElem1%)             = ADFD(ff,a)-1                     ;
result("Level","ADFH",ff,h,"NaN","NaN",%resElem1%)             = ADFH(ff,h)                       ;
result("Level","QX",a,"NaN","NaN","NaN",%resElem1%)            = QX(a)                            ;
result("Level","QVA",a,"NaN","NaN","NaN",%resElem1%)           = QVA(a)                           ;
result("Level","VVA",a,"NaN","NaN","NaN",%resElem1%)           = VVA(a)                           ;
result("Level","QINT",a,"NaN","NaN","NaN",%resElem1%)          = QINT(a)                          ;
result("Level","WF",ff,"NaN","NaN","NaN",%resElem1%)           = WF(ff)                           ;
result("Level","WFDIST",ff,a,"NaN","NaN",%resElem1%)           = WFDIST(ff,a)                     ;
result("Level","WFA",ff,a,"NaN","NaN",%resElem1%)              = WFA(ff,a)                        ;
result("Level","PQDDIST",c,a,"NaN","NaN",%resElem1%)           = PQDDIST(c,a)                     ;
result("Level","FD",ff,a,"NaN","NaN",%resElem1%)               = FD(ff,a)                         ;
result("Level","FS",ff,"NaN","NaN","NaN",%resElem1%)           = FS(ff)                           ;
result("Level","UNEMP",ff,"NaN","NaN","NaN",%resElem1%)        = UNEMP(ff)                        ;
result("Level","UNEMPRATE",ff,"NaN","NaN","NaN",%resElem1%)    = UNEMPRATE(ff)                    ;
result("Level","FSI",ins,ff,"NaN","NaN",%resElem1%)            = FSI(ins,ff)                      ;
result("Level","FSIM",f,ins,fp,insp,%resElem1%)                = FSIM(f,ins,fp,insp)              ;



*- -result("Level","UNEMP",ff,"NaN","NaN","NaN",%resElem1%)    = UNEMP(f)                         ;
result("Level","QINTD",c,a,"NaN","NaN",%resElem1%)             = QINTD(c,a)                       ;
result("Level","PXC",c,"NaN","NaN","NaN",%resElem1%)           = PXC(c)                           ;
result("Level","QXC",c,"NaN","NaN","NaN",%resElem1%)           = QXC(c)                           ;
result("Level","IOQXACQXV",a,c,"NaN","NaN",%resElem1%)         = IOQXACQXV(a,c)                   ;
result("Level","PXAC",a,c,"NaN","NaN",%resElem1%)              = PXAC(a,c)                        ;
result("Level","QXAC",a,c,"NaN","NaN",%resElem1%)              = QXAC(a,c)                        ;
result("Level","YF",f,"NaN","NaN","NaN",%resElem1%)            = YF(f)                            ;
result("Level","YFDISP",f,"NaN","NaN","NaN",%resElem1%)        = YFDISP(f)                        ;
result("Level","YFINS",f,"NaN","NaN","NaN",%resElem1%)         = YFINS(f)                         ;
result("Level","FSISH",ins,f,"NaN","NaN",%resElem1%)           = FSISH(ins,f)                     ;
result("Level","INSVA",ins,f,"NaN","NaN",%resElem1%)           = INSVA(ins,f)                     ;
result("Level","YH",h,"NaN","NaN","NaN",%resElem1%)            = YH(h)                            ;
result("Level","aDHOGOV","NaN","Nan","NaN","NaN",%resElem1%)   = DHOGOV                           ;
result("Level","HOGOV",h,"Nan","NaN","NaN",%resElem1%)         = HOGOV(h)                         ;
result("Level","HOHO",h,hp,"NaN","NaN",%resElem1%)             = HOHO(h,hp)                       ;
result("Level","HOWOR",h,w,"NaN","NaN",%resElem1%)             = HOWOR(h,w)                       ;
result("Level","HEXP",h,"NaN","NaN","NaN",%resElem1%)          = HEXP(h)                          ;
result("Level","QCD",c,h,"NaN","NaN",%resElem1%)               = QCD(c,h)                         ;
result("Level","QCD2",cc,ccp,h,"NaN",%resElem1%)               = QCD2(cc,ccp,h)                   ;
result("Level","QCDTotal",c,h,"NaN","NaN",%resElem1%)          = QCD(c,h) + SUM(cc,QCD2(cc,c,h));


result("Level","YE",e,"NaN","NaN","NaN",%resElem1%)            = YE(e)                            ;
result("Level","HOENT",h,e,"NaN","NaN",%resElem1%)             = HOENT(h,e)                       ;
result("Level","GOVENT",e,"NaN","NaN","NaN",%resElem1%)        = GOVENT(e)                        ;
result("Level","QED",c,e,"NaN","NaN",%resElem1%)               = QED(c,e)                         ;
result("Level","VED",e,"NaN","NaN","NaN",%resElem1%)           = VED(e)                           ;
result("Level","TE",c,w,"NaN","NaN",%resElem1%)                = TE(c,w)                          ;
result("Level","TM",w,c,"NaN","NaN",%resElem1%)                = TM(w,c)                          ;
result("Level","TS",c,"NaN","NaN","NaN",%resElem1%)            = TS(c)                            ;
*- result("Level","TQS",c,"NaN","NaN","NaN",%resElem1%)        = TQS(c)                           ;
result("Level","TV",c,"NaN","NaN","NaN",%resElem1%)            = TV(c)                            ;
result("Level","TX",a,"NaN","NaN","NaN",%resElem1%)            = TX(a)                            ;
result("Level","TF",ff,a,"NaN","NaN",%resElem1%)               = TF(ff,a)                         ;
result("Level","TYF",ff,"NaN","NaN","NaN",%resElem1%)          = TYF(ff)                          ;
result("Level","TYH",h,"NaN","NaN","NaN",%resElem1%)           = TYH(h)                           ;
result("Level","TYE",e,"NaN","NaN","NaN",%resElem1%)           = TYE(e)                           ;
result("Level","THC",h,c,"NaN","NaN",%resElem1%)               = THC(h,c)                         ;
result("Level","QGD",c,"NaN","NaN","NaN",%resElem1%)           = QGD(c)                           ;
result("Level","SHH",h,"NaN","NaN","NaN",%resElem1%)           = SHH(h)                           ;
result("Level","SEN",e,"NaN","NaN","NaN",%resElem1%)           = SEN(e)                           ;
result("Level","QINVD",c,i,"NaN","NaN",%resElem1%)             = QINVD(c,i)                       ;
result("Level","QINV",i,"NaN","NaN","NaN",%resElem1%)          = QINV(i)                          ;
result("Level","INVSH_I",i,"NaN","NaN","NaN",%resElem1%)       = INVSH_I(i)                       ;
result("Level","YFWOR",w,f,"NaN","NaN",%resElem1%)             = YFWOR(w,f)                       ;
result("Level","VEDSH",e,"NaN","NaN","NaN",%resElem1%)         = VEDSH(e)                         ;
result("Level","EXTENS",ff,a,"NaN","NaN",%resElem1%)           = EXTENS(ff,a)                     ;
result("Level","ADFExt",ff,a,"NaN","NaN",%resElem1%)           = ADFExt(ff,a)                     ;

*- assign agricultural budget
result("Level","AgBuRecurr",c,"NaN","NaN","NaN",%resElem1%)         =    AgBuRecurr(c)         ;
result("Level","AgBuInvest",i,"NaN","NaN","NaN",%resElem1%)         =    AgBuInvest(i)         ;
result("Level","AgBuInpSub",ff,a,"NaN","NaN",%resElem1%)            =    AgBuInpSub(ff,a)      ;
result("Level","AgBuRevFund",ff,a,"NaN","NaN",%resElem1%)           =    AgBuRevFund(ff,a)     ;
result("Level","AgBuOutSub",a,"NaN","NaN","NaN",%resElem1%)         =    AgBuOutSub(a)         ;
result("Level","AgBuComSub",c,h,"NaN","NaN",%resElem1%)             =    AgBuComSub(c,h)       ;
result("Level","AgBuIncSub",h,"NaN","NaN","NaN",%resElem1%)         =    AgBuIncSub(h)         ;
result("Level","AgBuTotRecurr","NaN","NaN","NaN","NaN",%resElem1%)  =    AgBuTotRecurr         ;
result("Level","AgBuTotInvest","NaN","NaN","NaN","NaN",%resElem1%)  =    AgBuTotInvest         ;
result("Level","AgBuTotInpSub","NaN","NaN","NaN","NaN",%resElem1%)  =    AgBuTotInpSub         ;
result("Level","AgBuTotOutSub","NaN","NaN","NaN","NaN",%resElem1%)  =    AgBuTotOutSub         ;
result("Level","AgBuTotalx","NaN","NaN","NaN","NaN",%resElem1%)     =    AgBuTotalx            ;
result("Level","AgBuTotShr","NaN","NaN","NaN","NaN",%resElem1%)     =    AgBuTotShr            ;

*-Nutrition values
result("Level","NutVal",nutElem,h,"NaN","NaN",%resElem1%)     =    NutVal(nutElem,h)            ;

*-Population values
*result("Level","EDUC",h,"NaN","NaN","NaN",%resElem1%)        =    EDUC   (h)             ;
*result("Level","HEAL",h,"NaN","NaN","NaN",%resElem1%)        =    HEAL   (h)             ;
*result("Level","BRATE",h,"NaN","NaN","NaN",%resElem1%)       =    bratep  (h)            ;
*result("Level","DRATE",h,"NaN","NaN","NaN",%resElem1%)       =    dratep  (h)            ;
*result("Level","DEATH",h,"NaN","NaN","NaN",%resElem1%)       =    deathp  (h)            ;
*result("Level","BIRTH",h,"NaN","NaN","NaN",%resElem1%)       =    birthp  (h)            ;
*result("Level","POPN",h,"NaN","NaN","NaN",%resElem1%)        =    popnp   (h)            ;
*result("Level","POPCHNG",h,"NaN","NaN","NaN",%resElem1%)     =    popchngp(h)            ;



result("Level","CO2EM_Q",c,a,"NaN","NaN",%resElem1%)           =    CO2EM_Q(c,a)            ;
result("Level","CO2EM_H",c,h,"NaN","NaN",%resElem1%)           =    CO2EM_H(c,h)            ;
result("Level","CO2EMIS_Q",a,"NaN","NaN","NaN",%resElem1%)     =    CO2EMIS_Q(a)            ;
result("Level","CO2EMIS_H",h,"NaN","NaN","NaN",%resElem1%)     =    CO2EMIS_H(h)            ;
result("Level","CO2EMIS","NaN","NaN","NaN","NaN",%resElem1%)   =    CO2EMIS                 ;
result("Level","NCO2EM_Q",nco,a,"NaN","NaN",%resElem1%)        =    NCO2EM_Q(nco,a)         ;
result("Level","NCO2EM_FS",nco,c,a,"NaN",%resElem1%)           =    NCO2EM_FS(nco,c,a)      ;
result("Level","NCO2EM_IO",nco,c,a,"NaN",%resElem1%)           =    NCO2EM_IO(nco,c,a)      ;
result("Level","NCO2EM_EN",nco,f,a,"NaN",%resElem1%)           =    NCO2EM_EN(nco,f,a)      ;
result("Level","NCO2EM_H",nco,c,h,"NaN",%resElem1%)            =    NCO2EM_H(nco,c,h)       ;
result("Level","NCO2EM_A_SUM",nco,a,"NaN","NaN",%resElem1%)    =    NCO2EM_A_SUM(nco,a)     ;
result("Level","NCO2EM_SUM",nco,"NaN","NaN","NaN",%resElem1%)  =    NCO2EM_SUM(nco)         ;
result("Level","GHGEM","NaN","NaN","NaN","NaN",%resElem1%)     =    GHGEM                   ;
result("Level","NCO2EM_FS_SUM",nco,a,"NaN","NaN",%resElem1%)   =    NCO2EM_FS_SUM(nco,a)    ;
result("Level","NCO2EM_IO_SUM",nco,a,"NaN","NaN",%resElem1%)   =    NCO2EM_IO_SUM(nco,a)    ;
result("Level","NCO2EM_EN_SUM",nco,a,"NaN","NaN",%resElem1%)   =    NCO2EM_EN_SUM(nco,a)    ;
result("Level","NCO2EM_H_SUM",nco,h,"NaN","NaN",%resElem1%)    =    NCO2EM_H_SUM(nco,h)     ;



$offDotL

*-assign post-sim SAMs
*-store postsim SAMs

$INCLUDE 30_Calibration\samchk_assign.inc

*$ontext
*-controls to halt the process:
abort$(demetra.MODELSTAT > 2) "Infeasible Solution. Use reportOnly.gms to see the results for debugging " ;

abort$(demetra.SOLVESTAT > 1) "Infeasible Solution. Use reportOnly.gms to see the results for debugging ";

*-controls to halt the process:
abort$(ABS(WALRAS.L) > 1E-3)
"WALRAS>0. Model is not in equilibrium so results will not be reported!Use reportOnly.gms to see the results for debugging", WALRAS.L            ;
*$offtext
*-calculate aggregated results
$ontext
 resultAg(resType,resVar,sacag,sacagp,sacagpp,sacagppp,%resElem%) =
        SUM(sacppp$map_sac_sacAG(sacppp,sacAgppp),
            SUM(sacpp$map_sac_sacAG(sacpp,sacAgpp),
                SUM(sacp$map_sac_sacAG(sacp,sacAgp),
                    SUM(sac$map_sac_sacAG(sac,sacAg),
                        result(resType,resVar,sac,sacp,sacpp,sacppp,%resElem%)
                        )
                    )
                )
            );

$offtext

*-------- assign result parameters -------------------------------


 $$macro qAggr0(q)      \
    resultAg("Level",&&q&&,"Nan","Nan","NaN","NaN",%resElem1%) = \
      result("Level",&&q&&,"Nan","Nan","NaN","NaN",%resElem1%);

 $$macro qAggr1(q)      \
    resultAg("Level",&&q&&,sacAg,"Nan","NaN","NaN",%resElem1%) = \
      SUM(sac$map_sac_sacAg(sac,sacag),result("Level",&&q&&,sac,"Nan","NaN","NaN",%resElem1%) );

 $$macro qAggr2(q)      \
    resultAg("Level",&&q&&,sacAg,sacAgp,"NaN","NaN",%resElem1%) = \
        SUM((sacp,sac)$(map_sac_sacAg(sacp,sacagp) AND map_sac_sacAg(sac,sacag)),\
                 result("Level",&&q&&,sac,sacp,"NaN","NaN",%resElem1%)     );

qAggr0('"AgBuTotRecurr"')
qAggr0('"AgBuTotInvest"')
qAggr0('"AgBuTotInpSub"')
qAggr0('"AgBuTotOutSub"')
qAggr0('"AgBuTotComSub"')
qAggr0('"AgBuTotIncSub"')
qAggr0('"AgBuTotalx"')
qAggr0('"sERX"')
qAggr0('"sCPI"')
qAggr0('"sPPI"')
qAggr0('"sMTAX"')
qAggr0('"sETAX"')
qAggr0('"sSTAX"')
qAggr0('"sVTAX"')
qAggr0('"sITAX"')
qAggr0('"sFTAX"')
qAggr0('"sDTAX"')
qAggr0('"sFYTAX"')
qAggr0('"sYG"')
qAggr0('"sEG"')
qAggr0('"sGBUDG"')
qAggr0('"sINVEST"')
qAggr0('"sTOTSAV"')
qAggr0('"sKAPGOV"')
qAggr0('"sKAPWOR"')
qAggr0('"sVFDOMD"')
qAggr0('"sVGD"')
qAggr0('"sINVESTSH"')
qAggr0('"sVGDSH"')
qAggr0('"sGDP"')
qAggr0('"sWALRAS"')
qAggr0('"aDADX"')
qAggr0('"aADVAADJ"')
qAggr0('"aDADVA"')
qAggr0('"aQEDADJ"')
qAggr0('"aHEADJ"')
qAggr0('"aQGDADJ"')
qAggr0('"aQGDADJceh"')
qAggr0('"aQGDADJoth"')
qAggr0('"aQGDADJext"')
qAggr0('"QGDADJc"')
qAggr0('"aHGADJ"')
qAggr0('"aDHOGOV"')
qAggr0('"aEGADJ"')
qAggr0('"aSADJ"')
qAggr0('"aSHADJ"')
qAggr0('"aSEADJ"')
qAggr0('"aDSHH"')
qAggr0('"aDS"')
qAggr0('"aDSEN"')
qAggr0('"aIADJ"')
qAggr0('"MODEL-STAT"')
qAggr0('"SOLVE-STAT"')
qAggr0('"NUM-REDEFQ"')
qAggr0('"iterUsd"')

qAggr1('"sKAPREG"')
qAggr1('"QE"')
qAggr1('"QD"')
qAggr1('"QM"')
qAggr1('"QQ"')
qAggr1('"QTT"')
qAggr1('"QTTD"')
qAggr1('"QX"')
qAggr1('"QVA"')
qAggr1('"VVA"')
qAggr1('"QINT"')
qAggr1('"FS"')
qAggr1('"QXC"')
qAggr1('"YF"')
qAggr1('"YFDISP"')
qAggr1('"YFINS"')
qAggr1('"YH"')
qAggr1('"HEXP"')
qAggr1('"YE"')
qAggr1('"GOVENT"')
qAggr1('"VED"')
qAggr1('"QGD"')
qAggr1('"QINV"')
qAggr1('"AgBuRecurr"')
qAggr1('"AgBuInvest"')
qAggr1('"AgBuOutSub"')
qAggr1('"AgBuIncSub"')


qAggr2('"AgBuInpSub"')
qAggr2('"AgBuRevFund"')
qAggr2('"AgBuComSub"')
qAggr2('"YFWOR"')
qAggr2('"QINVD"')
qAggr2('"QED"')
qAggr2('"HOENT"')
qAggr2('"INSVA"')
qAggr2('"QCDTotal"')
qAggr2('"QCD"')
qAggr2('"QMR"')
qAggr2('"QER"')
qAggr2('"FD"')
qAggr2('"FSI"')
qAggr2('"QINTD"')
qAggr2('"QXAC"')
qAggr2('"HOHO"')
qAggr2('"HOWOR"')
qAggr2('"EXTENS"')

qAggr1('"ADFExt"')
qAggr1('"EDUC"')
qAggr1('"HEAL"')
qAggr1('"DEATH"')
qAggr1('"BIRTH"')
qAggr1('"POPN"')
qAggr1('"POPCHNG"')



resultAg("Level","QCD2",sacAg,sacAgp,sacAgpp,"NaN",%resElem1%)             =  SUM((sac,sacp,sacpp)$(map_sac_sacAg(sac,sacag) AND map_sac_sacAg(sacp,sacagp) AND map_sac_sacAg(sacpp,sacagpp)),result("Level","QCD2",sac,sacp,sacpp,"NaN",%resElem1%)  );
resultAg("Level","QCDTotal",sacAg,sacAgp,sacAgpp,"NaN",%resElem1%)             =  SUM((sac,sacp,sacpp)$(map_sac_sacAg(sac,sacag) AND map_sac_sacAg(sacp,sacagp) AND map_sac_sacAg(sacpp,sacagpp)),result("Level","QCDTotal",sac,sacp,sacpp,"NaN",%resElem1%)  );



  $$macro pAggr1d1e(p,q)    \
    resultAg("Level",&&p&&,sacAg,"NaN","NaN","NaN",%resElem1%)$sum(sac$map_sac_sacAg(sac,sacag),result("Level",&&q&&,sac,"NaN","NaN","NaN",%resElem1%)) \
                              =  SUM(sac$map_sac_sacAg(sac,sacag),\
                                 result("Level",&&p&&,sac,"NaN","NaN","NaN",%resElem1%)              \
                                 *result("Level",&&q&&,sac,"NaN","NaN","NaN",%resElem1%))         \
                                 /sum(sac$map_sac_sacAg(sac,sacag),result("Level",&&q&&,sac,"NaN","NaN","NaN",%resElem1%));

   $$macro pAggr2d1e(p,q)    \
    resultAg("Level",&&p&&,sacAg,sacAgp,"NaN","NaN",%resElem1%)$sum((sac,sacp)$(map_sac_sacAg(sac,sacAg) AND map_sac_sacAg(sacp,sacAgp)),result("Level",&&q&&,sac,sacp,"NaN","NaN",%resElem1%)) \
                              =  SUM((sac,sacp)$(map_sac_sacAg(sac,sacAg) AND map_sac_sacAg(sacp,sacAgp)),\
                                 result("Level",&&p&&,sac,sacp,"NaN","NaN",%resElem1%)              \
                                 *result("Level",&&q&&,sac,sacp,"NaN","NaN",%resElem1%))         \
                                 /sum((sac,sacp)$(map_sac_sacAg(sac,sacAg) AND map_sac_sacAg(sacp,sacAgp)),\
                                         result("Level",&&q&&,sac,sacp,"NaN","NaN",%resElem1%));


    $$macro pAggr1d2e(t,p,q)    \
    resultAg("Level",&&t&&,sacAg,"NaN","NaN","NaN",%resElem1%)$sum(sac$map_sac_sacAg(sac,sacag),result("Level",&&p&&,sac,"NaN","NaN","NaN",%resElem1%)\
                                                                 * result("Level",&&q&&,sac,"NaN","NaN","NaN",%resElem1%)) \
                              =  SUM(sac$map_sac_sacAg(sac,sacag),\
                                   result("Level",&&t&&,sac,"NaN","NaN","NaN",%resElem1%)            \
                                 * result("Level",&&p&&,sac,"NaN","NaN","NaN",%resElem1%)            \
                                 * result("Level",&&q&&,sac,"NaN","NaN","NaN",%resElem1%))         \
                                 /sum(sac$map_sac_sacAg(sac,sacag),result("Level",&&p&&,sac,"NaN","NaN","NaN",%resElem1%)   \
                                                                 * result("Level",&&q&&,sac,"NaN","NaN","NaN",%resElem1%));

   $$macro pAggr2d2e(t,p,q)    \
    resultAg("Level",&&t&&,sacAg,sacAgp,"NaN","NaN",%resElem1%)$sum((sac,sacp)$(map_sac_sacAg(sac,sacAg) AND map_sac_sacAg(sacp,sacAgp)),\
                                         result("Level",&&p&&,sac,sacp,"NaN","NaN",%resElem1%) \
                                         *result("Level",&&q&&,sac,sacp,"NaN","NaN",%resElem1%))\
                              =  SUM((sac,sacp)$(map_sac_sacAg(sac,sacAg) AND map_sac_sacAg(sacp,sacAgp)),\
                                 result("Level",&&t&&,sac,sacp,"NaN","NaN",%resElem1%)              \
                                 *result("Level",&&p&&,sac,sacp,"NaN","NaN",%resElem1%)              \
                                 *result("Level",&&q&&,sac,sacp,"NaN","NaN",%resElem1%))         \
                                 /sum((sac,sacp)$(map_sac_sacAg(sac,sacAg) AND map_sac_sacAg(sacp,sacAgp)),\
                                         result("Level",&&p&&,sac,sacp,"NaN","NaN",%resElem1%) \
                                         *result("Level",&&q&&,sac,sacp,"NaN","NaN",%resElem1%));



pAggr1d1e('"PE"','"QE"')
pAggr1d1e('"PWE"','"QE"')
pAggr1d1e('"PWM"','"QM"')
pAggr1d1e('"PD"','"QD"')
pAggr1d1e('"PM"','"QM"')
pAggr1d1e('"PTT"','"QTT"')
pAggr1d1e('"PQS"','"QD"')
pAggr1d1e('"PQD"','"QD"')
pAggr1d1e('"PX"','"QX"')
pAggr1d1e('"PVA"','"QVA"')
pAggr1d1e('"PINT"','"QINT"')
pAggr1d1e('"PXC"','"QXC"')
pAggr1d1e('"TV"','"VVA"')
pAggr1d1e('"TYF"','"YF"')
pAggr1d1e('"TYH"','"YH"')
pAggr1d1e('"TYE"','"YE"')
pAggr1d1e('"SHH"','"YH"')
pAggr1d1e('"SEN"','"YE"')
pAggr1d1e('"INVSH_I"','"sVFDOMD"')
pAggr1d1e('"VEDSH"','"sVFDOMD"')

pAggr2d1e('"PXAC"','"QXAC"')
pAggr2d1e('"PMR"','"QMR"')
pAggr2d1e('"PER"','"QER"')
pAggr2d1e('"PQCD"','"QCD"')
pAggr2d1e('"WFA"','"FD"')

pAggr1d2e('"TS"','"PQS"','"QQ"')
pAggr1d2e('"TEX"','"PQS"','"QQ"')
pAggr1d2e('"TX"','"QX"','"PX"')
pAggr1d2e('"TIN"','"QINT"','"PINT"')
pAggr1d2e('"TXA"','"QX"','"PX"')
pAggr1d2e('"TF"','"FS"','"WF"')
pAggr1d2e('"THC"','"QCD"','"PQD"')

pAggr2d2e('"TM"','"QMR"','"PMR"')
pAggr2d2e('"TE"','"QER"','"PER"')

resultAg("Level","PQC",sacag,sacagp,"NaN","NaN",%resElem1%) =  resultAg("Level","PQD",sacag,"NaN","NaN","NaN",%resElem1%)
                                                                 * (1+resultAg("Level","TV",sacag,"NaN","NaN","NaN",%resElem1%))
                                                                 + resultAg("Level","PQCD",sacag,sacagp,"NaN","NaN",%resElem1%)   ;

*-  )                                                                                               ;

*-ASSIGN SDG INDICATORS
$onDotL
sdgResult("Level","g01","UtilPC",h,"NaN",%resElem1%)                    = SUM(cc$QCD0(cc,h),beta(cc,h)*log(QCD(cc,h)-qcdconst(cc,h)))/POPN0(h)             ;
sdgResult("Level","g01","UtilPCAg","NaN","NaN",%resElem1%)              = SUM((cc,h)$QCD0(cc,h),beta(cc,h)*log(QCD(cc,h)-qcdconst(cc,h)))/SUM(h,POPN0(h))             ;
sdgResult("Level","g01","WageCerRt","NaN","NaN",%resElem1%)$(SUM(l$lRuUs(l),FS(l)))             = (SUM(l$lRuUs(l),WF(l)*FS(l))/SUM(l$lRuUs(l),FS(l))) /(SUM((ccer),PQD(ccer)*QD(ccer))/SUM((ccer),QD(ccer)))            ;
sdgResult("Level","g02","TFP","NaN","NaN",%resElem1%)                   = SUM(aagr,AD("ftop",aagr))/SUM(aagr,1)                  ;
sdgResult("Level","g02","TMAv","NaN","NaN",%resElem1%)                  = SUM((w,c)$cfdh(c),QMR(w,c)*PQD(c))/SUM((w,c)$cfdh(c),QMR(w,c)*PMR(w,c))                 ;
sdgResult("Level","g02","FdProdInd","NaN","NaN",%resElem1%)             = SUM(c$(cfd(c) AND cfdh(c)),QXC(c)*PXC(c))/SUM(c$cfd(c),QXC0(c)*PXC(c))*100            ;
sdgResult("Level","g02","FdFsProdInd","NaN","NaN",%resElem1%)           = SUM(c$(cfdh(c) OR cfs(c)),QXC(c)*PXC(c))/SUM(c$(cfs(c) OR cfdh(c)),QXC0(c)*PXC(c))*100          ;
sdgResult("Level","g02","Fdimp","NaN","NaN",%resElem1%)                 = SUM(c$cfdh(c),PM(c)*QM(c))                ;
sdgResult("Level","g02","Fdexp","NaN","NaN",%resElem1%)                 = SUM(c$cfdh(c),PE(c)*QE(c))                ;
sdgResult("Level","g02","NutPCAg",nutElem,"NaN",%resElem1%)             = SUM(h,nutVal(nutElem,h))/SUM(h,POPN0(h))     ;
sdgResult("Level","g02","CalCerSh",h,"NaN",%resElem1%)$nutVal0("cal",h) = SUM(c$ccer(c),nutTable(c,"cal")*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ nutVal("cal",h)      ;
sdgResult("Level","g02","CalCerShAg","NaN","NaN",%resElem1%)$(SUM(h,nutVal0("cal",h))) = SUM((c,h)$ccer(c),                nutTable(c,"cal")*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ sum(h,nutVal("cal",h))         ;
sdgResult("Level","g02","ProLvsFs",h,"NaN",%resElem1%)$nutVal0("pro",h) = SUM(c$(cliv(c) or cfs(c)),nutTable(c,"pro")* (QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ nutVal("pro",h)          ;
sdgResult("Level","g02","ProLvsFsAg","NaN","NaN",%resElem1%)$(SUM(h,nutVal0("pro",h))) = SUM((c,h)$(cliv(c) or cfs(c)),nutTable(c,"pro")*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ SUM(h,nutVal("pro",h))          ;
sdgResult("Level","g02","ProLvs",h,"NaN",%resElem1%)$nutVal0("pro",h)   = SUM(c$(cliv(c)),nutTable(c,"pro")*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ nutVal("pro",h)            ;
sdgResult("Level","g02","ProLvsAg","NaN","NaN",%resElem1%)$(SUM(h,nutVal0("pro",h)))              = SUM((h,c)$(cliv(c)),nutTable(c,"pro")*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ SUM(h,nutVal("pro",h))            ;
sdgResult("Level","g02","YDAv",h,"NaN",%resElem1%)                      = YH(h) * (1 - TYH(h)) * (1 - SHH(h))              ;
sdgResult("Level","g02","YDAvAg","NaN","NaN",%resElem1%)                = SUM(h,YH(h) * (1 - TYH(h)) * (1 - SHH(h)))              ;
sdgResult("Level","g02","FdPriInd",h,"NaN",%resElem1%)$(SUM(c$cfdh(c),PQD0(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h)))))      = SUM(c$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/(SUM(c$cfdh(c),PQD0(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h)))))*100          ;
sdgResult("Level","g02","FdPriIndAg","NaN","NaN",%resElem1%)$(SUM((h,c)$cfdh(c),PQD0(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h)))))            = SUM((h,c)$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/(SUM((h,c)$cfdh(c),PQD0(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h)))))*100          ;
sdgResult("Level","g02","FdYDSh",h,"NaN",%resElem1%)                    = SUM(c$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/HEXP(h)            ;
sdgResult("Level","g02","FdYDShAg","NaN","NaN",%resElem1%)              = SUM((h,c)$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/SUM(h,HEXP(h))            ;
sdgResult("Level","g02","FdCons",h,"NaN",%resElem1%)                    = SUM(c$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))            ;
sdgResult("Level","g02","FdConsAg","NaN","NaN",%resElem1%)              = SUM((h,c)$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))            ;
sdgResult("Level","g02","FdConsPC",h,"NaN",%resElem1%)                  = SUM(c$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/POPN0(h)          ;
sdgResult("Level","g02","FdConsPCAg","NaN","NaN",%resElem1%)            = SUM((h,c)$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/SUM(h,POPN0(h))          ;
sdgResult("Level","g02","CalFrVSh",h,"NaN",%resElem1%)$nutVal0("cal",h) = SUM(c$cfv(c),nutTable(c,"cal")*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ nutVal("cal",h)            ;
sdgResult("Level","g02","CalFrVShAg","NaN","NaN",%resElem1%)$(SUM(h,nutVal0("cal",h)))            = SUM((h,c)$cfv(c),nutTable(c,"cal")*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ SUM(h,nutVal("cal",h))          ;
sdgResult("Level","g02","TMInd","NaN","NaN",%resElem1%)                 = g02TMAv / g02TMAv0*100                ;
sdgResult("Level","g02","ExpSubInd","NaN","NaN",%resElem1%)             = SUM((w,c)$cfdh(c),QER(c,w)*PWE(c)*ER(w))/SUM((w,c)$cfdh(c),QER(c,w)*PER(c,w))/ SUM((w,c)$cfdh(c),QER0(c,w)*PWE0(c)*ER0(w))/SUM((w,c)$cfdh(c),QER0(c,w)*PER0(c,w))*100            ;
sdgResult("Level","g06","WatUse","NaN","NaN",%resElem1%)                = SUM((a,f)$nirr(f),FD(f,a))/SUM((a,f),FD(f,a))*100               ;
sdgResult("Level","g07","EnerPrim","NaN","NaN",%resElem1%)              = SUM((cener,ff,a)$map_c_f_a(cener,ff,a),FD(ff,a)*WFA(ff,a))             ;
sdgResult("Level","g07","EnerClnSh","NaN","NaN",%resElem1%)$(SUM(cener,QXC(cener)))             = SUM(crenw,QXC(crenw))/SUM(cener,QXC(cener))              ;
sdgResult("Level","g07","EnerProd","NaN","NaN",%resElem1%)              = SUM(cener,QXC(cener))             ;
sdgResult("Level","g07","EnerSfSu","NaN","NaN",%resElem1%)$SUM(cener,QQ(cener))   = SUM(cener,QD(cener)) /SUM(cener,QQ(cener))             ;
sdgResult("Level","g07","EnerPriInd",cener,"NaN",%resElem1%)$(QD(cener)*PD0(cener)) = QD(cener)*PD(cener)/(QD(cener)*PD0(cener))*100        ;
sdgResult("Level","g07","EnerPriIndAg","NaN","NaN",%resElem1%)$SUM(cener,QD0(cener)*PD0(cener))          = SUM(cener,QD(cener)*PD(cener))/SUM(cener,QD(cener)*PD0(cener))*100        ;
sdgResult("Level","g07","FosComp","NaN","NaN",%resElem1%)$SUM(cfoss,QD0(cfoss)*PD0(cfoss))                = (1/ERX)*SUM(cfoss,QD(cfoss)*PD(cfoss))/SUM(cfoss,QD(cfoss)*PD0(cfoss))*100              ;
sdgResult("Level","g07","RenComp","NaN","NaN",%resElem1%)$SUM(crenw,QD0(crenw)*PD0(crenw))               = (1/ERX)*SUM(crenw,QD(crenw)*PD(crenw))/SUM(crenw,QD(crenw)*PD0(crenw))*100              ;
sdgResult("Level","g07","FosRenRt","NaN","NaN",%resElem1%)$ g07RenComp0 = g07FosComp/g07RenComp*100             ;
sdgResult("Level","g07","EnerSec","NaN","NaN",%resElem1%)               = SUM(cener,QXC(cener)*PXC(cener))/SUM(c,QXC(c)*PXC(c))                ;
sdgResult("Level","g07","EnerVaRt",a,"NaN",%resElem1%)                  = SUM((cener,ff)$map_c_f_a(cener,ff,a),FD(ff,a)*WFA(ff,a))/VVA(a)          ;
sdgResult("Level","g07","EnerVaRtAg","NaN","NaN",%resElem1%)$SUM(a,VVA(a))  = SUM((cener,ff,a)$map_c_f_a(cener,ff,a),FD(ff,a)*WFA(ff,a))/SUM(a,VVA(a))           ;
sdgResult("Level","g07","EnerPrimStk","Export","NaN",%resElem1%)        = SUM(cener,QE(cener)*PE(cener))   ;
sdgResult("Level","g07","EnerPrimStk","Import","NaN",%resElem1%)        = SUM(cener,QM(cener)*PM(cener))   ;
sdgResult("Level","g07","EnerPrimStk","Domestic Demand","NaN",%resElem1%)           = SUM(cener,QD(cener)*PD(cener))   ;
sdgResult("Level","g07","EnerRefn","NaN","NaN",%resElem1%)              = SUM((cener,ff,aener)$map_c_f_a(cener,ff,aener),FD(ff,aener)*WFA(ff,aener))             ;
sdgResult("Level","g07","EnerUse",'Transport',"NaN",%resElem1%)         = SUM((cener,ff,atrn)$map_c_f_a(cener,ff,atrn),FD(ff,atrn)*WFA(ff,atrn))   ;                  
sdgResult("Level","g07","EnerUse",'Industry',"NaN",%resElem1%)          = SUM((cener,ff,aind)$map_c_f_a(cener,ff,aind),FD(ff,aind)*WFA(ff,aind))   ;                  
sdgResult("Level","g07","EnerUse",'Other',"NaN",%resElem1%)             = SUM((cener,ff,a)$(NOT (aind(a) OR atrn(a)) AND map_c_f_a(cener,ff,a)),FD(ff,a)*WFA(ff,a))  ;
sdgResult("Level","g07","EnerUse",'Exports',"NaN",%resElem1%)           = SUM(cener,QE(cener)*PE(cener))   ;                                                          
sdgResult("Level","g07","PrimGdpRt",enEl1,"NaN",%resElem1%)$g07EnerPrimStk0(enEl1)= (g07EnerPrimStk(enEl1) /GDP)     ;
sdgResult("Level","g07","RefnGdpRt","NaN","NaN",%resElem1%)             = ( SUM((cener,ff,aener)$map_c_f_a(cener,ff,aener),FD(ff,aener)*WFA(ff,aener)) /GDP)            ;
sdgResult("Level","g07","UseGdpRt",enEl2,"NaN",%resElem1%) $g07EnerUse0(enel2) = (g07EnerUse(enel2) /GDP)      ;
sdgResult("Level","g07","RefnPrimRt","NaN","NaN",%resElem1%)$g07EnerPrim            = (g07EnerRefn/g07EnerPrim)           ;
sdgResult("Level","g07","UsePrimRt",enEl2,"NaN",%resElem1%)$g07EnerUse0(enEl2) = (g07EnerUse(enEl2)/g07EnerPrim)     ;
sdgResult("Level","g08","GDPPCGr","NaN","NaN",%resElem1%)               = GDP/SUM(h,POPN0(h))              ;
sdgResult("Level","g08","NetTrade","NaN","NaN",%resElem1%)              = SUM(c,PE(c)*QE(c))-SUM(c,PM(c)*QM(c))             ;
sdgResult("Level","g08","RevComp",c,"NaN",%resElem1%) $(ce(c) AND cx(c)) = g08RevComp0(c)        ;
sdgResult("Level","g08","RevCompAg","NaN","NaN",%resElem1%)             = SUM(c$(ce(c) AND cx(c)), g08RevComp(c))/SUM(c$(ce(c) AND cx(c)),1)            ;
sdgResult("Level","g08","FosGDPSh","NaN","NaN",%resElem1%)              = SUM(cfoss,PXC(cfoss)*QXC(cfoss))/SUM(c,QXC(c))             ;
sdgResult("Level","g09","ManVaSh","NaN","NaN",%resElem1%)               = SUM(aind,VVA(aind))/SUM(a,VVA(a))              ;
sdgResult("Level","g09","ManVaPC","NaN","NaN",%resElem1%)               = SUM(aind,VVA(aind))/SUM(h,POPN0(h))              ;
sdgResult("Level","g08","ManEmpSh","NaN","NaN",%resElem1%)              = SUM((l,aind),FD(l,aind))/SUM((l,a),FD(l,a))             ;
sdgResult("Level","g08","Exp","NaN","NaN",%resElem1%)                   = SUM(c,PE(c)*QE(c))                  ;
sdgResult("Level","g08","Imp","NaN","NaN",%resElem1%)                   = SUM(c,PM(c)*QM(c))                   ;
sdgResult("Level","g08","Open","NaN","NaN",%resElem1%)                  = (SUM(c,PE(c)*QE(c))+SUM(c,PM(c)*QM(c)))/GDP                 ;
sdgResult("Level","g10","LabSh","NaN","NaN",%resElem1%)                 = SUM((l,a),FD(l,a)*WFA(l,a))/SUM((f,a),FD(f,a)*WFA(f,a))                ;
sdgResult("Level","g10","AgrEmp","NaN","NaN",%resElem1%)                = SUM((l,aagr),FD(l,aagr))               ;
sdgResult("Level","g10","AgrEmpSh","NaN","NaN",%resElem1%)              = SUM((l,aagr),FD(l,aagr))/SUM((l,a),FD(l,a))              ;
sdgResult("Level","g10","Skil","NaN","NaN",%resElem1%) $(SUM((ls,a),FD0(ls,a))) = SUM((ls,a),FD(ls,a))/SUM((lu,a),FD(lu,a))             ;
sdgResult("Level","g10","WageDifSkl","NaN","NaN",%resElem1%)$(SUM((ls,a),FD0(ls,a)))= (SUM((ls,a),FD(ls,a)*WFA(ls,a))/SUM((ls,a),FD(ls,a))) /(SUM((lu,a),FD(lu,a)*WFA(lu,a))/SUM((lu,a),FD(lu,a)))           ;
sdgResult("Level","g10","WageDifAgr","NaN","NaN",%resElem1%)            = (SUM((l,aagr),FD(l,aagr)*WFA(l,aagr))/SUM((l,aagr),FD(l,aagr)))/(SUM((l,a),FD(l,a)*WFA(l,a))/SUM((l,a),FD(l,a)))           ;
sdgResult("Level","g10","IncDiffHH",h,hp,%resElem1%)$ (POPN0(h) and (YH(hp)/POPN0(hp)))    = (YH(h)/POPN0(h))/(YH(hp)/POPN0(hp))-1      ;
sdgResult("Level","g10","IncDiffHHAg","NaN","NaN",%resElem1%)$ (sum((h,hp), g10IncDiffHH0(h,hp))) = SUM((h,hp)$(ord(h)<card(hp)),g10IncDiffHH(h,hp))/ SUM((h,hp)$(ord(h)<card(hp)),1) ;
sdgResult("Level","g12","RenSh","NaN","NaN",%resElem1%)$SUM(cener,QXC(cener))   = SUM(crenw,QXC(crenw))/SUM(cener,QXC(cener))                ;
sdgResult("Level","g13","RenSh","NaN","NaN",%resElem1%)$SUM(cener,QXC(cener))   = SUM(crenw,QXC(crenw))/SUM(cener,QXC(cener))                ;
sdgResult("Level","g14","FsSh","NaN","NaN",%resElem1%)                  = SUM(cfs,QXC(cfs))/GDP                ;
sdgResult("Level","g15","NonAgri","NaN","NaN",%resElem1%)$SUM((n,a),FD(n,a)) = SUM((n,a)$(NOT aagr(a)),FD(n,a))/SUM((n,a),FD(n,a))              ;
sdgResult("Level","g17","GDPPc","NaN","NaN",%resElem1%)                 = GDP/SUM(h,POPN0(h))                ;
sdgResult("Level","g17","EGSh","MTAX","NaN",%resElem1%)$YG                 = MTAX    /YG  ;
sdgResult("Level","g17","EGSh","ETAX","NaN",%resElem1%)$YG                 = ETAX    /YG  ;
sdgResult("Level","g17","EGSh","DTAX","NaN",%resElem1%)$YG                 = DTAX    /YG  ;
sdgResult("Level","g17","EGSh","FYTAX","NaN",%resElem1%)$YG                = FYTAX   /YG  ;  
sdgResult("Level","g17","EGSh","ITAX","NaN",%resElem1%)$YG                 = ITAX    /YG  ;              
sdgResult("Level","g17","EGSh","STAX","NaN",%resElem1%)$YG                 = STAX    /YG  ; 
sdgResult("Level","g17","EGSh","FTAX","NaN",%resElem1%)$YG                 = FTAX    /YG  ;              
sdgResult("Level","g17","EGSh","VTAX","NaN",%resElem1%)$YG                 = VTAX    /YG  ;
sdgResult("Level","g17","EGSh","HCTAX","NaN",%resElem1%)$YG                = HCTAX   /YG  ;             
sdgResult("Level","g17","EGShAg","NaN","NaN",%resElem1%)                = MTAX/YG + ETAX/YG + DTAX/YG + FYTAX/YG + ITAX/YG + STAX/YG + FTAX/YG + VTAX/YG + HCTAX/YG;




$offDotL

*- -------- end of assign result parameters ---------------------------
