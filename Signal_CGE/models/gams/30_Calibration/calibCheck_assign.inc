*------------------------------------------------------------------------------
*------------------------------------------------------------------------------
*-   DEMETRA v1.0-alpha
*-
*-   GAMS file : calibcheck_assign.inc
*-
*-   @purpose  : assignment file to check if the baseline scenario can replicate
*-                 dynamic calibration
*-   @author   : Hasan Dudu
*-   @date     : 10 February 2017
*-   @since    :
*-   @refDoc   :
*-   @seeAlso  :
*-   @calledBy :
*------------------------------------------------------------------------------
*------------------------------------------------------------------------------
$onDotL
CalibCheck("FSIL",ins,f,"NaN","NaN")          = FSIL(ins,f) - FSIL0(ins,f)                       ;
CalibCheck("FSIM",f,ins,fp,insp)              = FSIM(f,ins,fp,insp)- FSIM0(f,ins,fp,insp)        ;
CalibCheck("PWE",c,"NaN","NaN","NaN")         = PWE(c) - PWE0(c)                                 ;
CalibCheck("PE",c,"NaN","NaN","NaN")          = PE(c) - PE0(c)                                   ;
CalibCheck("PER",c,w,"NaN","NaN")             = PER(c,w) - PER0(c,w)                             ;
CalibCheck("PD",c,"NaN","NaN","NaN")          = PD(c) - PD0(c)                                   ;
CalibCheck("QE",c,"NaN","NaN","NaN")          = QE(c) - QE0(c)                                   ;
CalibCheck("QER",c,w,"NaN","NaN")             = QER(c,w) - QER0(c,w)                             ;
CalibCheck("QD",c,"NaN","NaN","NaN")          = QD(c) - QD0(c)                                   ;
CalibCheck("PWM",c,"NaN","NaN","NaN")         = PWM(c) - PWM0(c)                                 ;
CalibCheck("PM",c,"NaN","NaN","NaN")          = PM(c) - PM0(c)                                   ;
CalibCheck("PMR",w,c,"NaN","NaN")             = PMR(w,c) - PMR0(w,c)                             ;
CalibCheck("QM",c,"NaN","NaN","NaN")          = QM(c) - QM0(c)                                   ;
CalibCheck("QQ",c,"NaN","NaN","NaN")          = QQ(c) - QQ0(c)                                   ;
CalibCheck("PTT",m,"NaN","NaN","NaN")         = PTT(m) - PTT0(m)                                 ;
CalibCheck("QTT",m,"NaN","NaN","NaN")         = QTT(m) - QTT0(m)                                 ;
CalibCheck("QTTD",c,"NaN","NaN","NaN")        = QTTD(c) - QTTD0(c)                               ;
CalibCheck("PQS",c,"NaN","NaN","NaN")         = PQS(c) - PQS0(c)                                 ;
CalibCheck("PQD",cc,"NaN","NaN","NaN")        = PQD(cc) - PQD0(cc)                               ;
CalibCheck("PQCD",cc,h,"NaN","NaN")           = PQCD(cc,h) - PQCD0(cc,h)                         ;
CalibCheck("PX",a,"NaN","NaN","NaN")          = PX(a) - PX0(a)                                   ;
CalibCheck("PVA",a,"NaN","NaN","NaN")         = PVA(a) - PVA0(a)                                 ;
CalibCheck("PINT",a,"NaN","NaN","NaN")        = PINT(a) - PINT0(a)                               ;
CalibCheck("ADFD",ff,a,"NaN","NaN")           = ADFD(ff,a) - ADFD0(ff,a)                         ;
CalibCheck("ADFAG",ff,a,"NaN","NaN")          = ADFAG(ff,a) - ADFAG0(ff,a)                       ;
CalibCheck("ADFAGfADJ",ff,"NaN","NaN","NaN")  = ADFAGfADJ(ff) - ADFAGfADJ0(ff)                   ;
CalibCheck("ADFAGaADJ",a,"NaN","NaN","NaN")   = ADFAGaADJ(a) - ADFAGaADJ0(a)                     ;
CalibCheck("QX",a,"NaN","NaN","NaN")          = QX(a) - QX0(a)                                   ;
CalibCheck("QVA",a,"NaN","NaN","NaN")         = QVA(a) - QVA0(a)                                 ;
CalibCheck("QINT",a,"NaN","NaN","NaN")        = QINT(a) - QINT0(a)                               ;
CalibCheck("WF",ff,"NaN","NaN","NaN")         = WF(ff) - WF0(ff)                                 ;
CalibCheck("WFDIST",ff,a,"NaN","NaN")         = WFDIST(ff,a) - WFDIST0(ff,a)                     ;
CalibCheck("PQDDIST",c,a,"NaN","NaN")         = PQDDIST(c,a) - PQDDIST0(c,a)                     ;
CalibCheck("FD",ff,a,"NaN","NaN")             = FD(ff,a) - FD0(ff,a)                             ;
CalibCheck("FSI",ins,f,"NaN","NaN")           = FSI(ins,f) - FSI0(ins,f)                         ;
CalibCheck("FS",ff,"NaN","NaN","NaN")         = FS(ff) - FS0(ff)                                 ;
CalibCheck("QINTD",c,a,"NaN","NaN")           = QINTD(c,a) - QINTD0(c,a)                         ;
CalibCheck("PXC",c,"NaN","NaN","NaN")         = PXC(c) - PXC0(c)                                 ;
CalibCheck("QXC",c,"NaN","NaN","NaN")         = QXC(c) - QXC0(c)                                 ;
CalibCheck("PXAC",a,c,"NaN","NaN")            = PXAC(a,c) - PXAC0(a,c)                           ;
CalibCheck("QXAC",a,c,"NaN","NaN")            = QXAC(a,c) - QXAC0(a,c)                           ;
CalibCheck("IOQXACQXV",a,c,"NaN","NaN")       = IOQXACQXV(a,c) - IOQXACQXV0(a,c)                 ;
CalibCheck("YF",f,"NaN","NaN","NaN")          = YF(f) - YF0(f)                                   ;
CalibCheck("YFDISP",f,"NaN","NaN","NaN")      = YFDISP(f) - YFDISP0(f)                           ;
CalibCheck("YFINS",f,"NaN","NaN","NaN")       = YFINS(f) - YFINS0(f)                             ;
CalibCheck("FSISH",ins,f,"NaN","NaN")         = FSISH(ins,f) - FSISH0(ins,f)                     ;
CalibCheck("INSVA",ins,f,"NaN","NaN")         = INSVA(ins,f) - INSVA0(ins,f)                     ;
CalibCheck("YH",h,"NaN","NaN","NaN")          = YH(h) - YH0(h)                                   ;
CalibCheck("HOHO",h,hp,"NaN","NaN")           = HOHO(h,hp) - HOHO0(h,hp)                         ;
CalibCheck("HEXP",h,"NaN","NaN","NaN")        = HEXP(h) - HEXP0(h)                               ;
CalibCheck("QCD",cc,h,"NaN","NaN")            = QCD(cc,h) - QCD0(cc,h)                           ;
CalibCheck("QCD2",cag,cc,h,"NaN")             = QCD2(cag,cc,h) - QCD20(cag,cc,h)                 ;
CalibCheck("YE",e,"NaN","NaN","NaN")          = YE(e) - YE0(e)                                   ;
CalibCheck("HOENT",h,e,"NaN","NaN")           = HOENT(h,e) - HOENT0(h,e)                         ;
CalibCheck("GOVENT",e,"NaN","NaN","NaN")      = GOVENT(e) - GOVENT0(e)                           ;
CalibCheck("QED",c,e,"NaN","NaN")             = QED(c,e) - QED0(c,e)                             ;
CalibCheck("VED",e,"NaN","NaN","NaN")         = VED(e) - VED0(e)                                 ;
CalibCheck("TE",c,w,"NaN","NaN")              = TE(c,w) - TE0(c,w)                               ;
CalibCheck("TM",w,c,"NaN","NaN")              = TM(w,c) - TM0(w,c)                               ;
CalibCheck("TS",c,"NaN","NaN","NaN")          = TS(c) - TS0(c)                                   ;
CalibCheck("TV",cc,"NaN","NaN","NaN")         = TV(cc) - TV0(cc)                                 ;
CalibCheck("TX",a,"NaN","NaN","NaN")          = TX(a) - TX0(a)                                   ;
CalibCheck("TF",ff,a,"NaN","NaN")             = TF(ff,a) - TF0(ff,a)                             ;
CalibCheck("TYF",f,"NaN","NaN","NaN")         = TYF(f) - TYF0(f)                                 ;
CalibCheck("TYH",h,"NaN","NaN","NaN")         = TYH(h) - TYH0(h)                                 ;
CalibCheck("TYE",e,"NaN","NaN","NaN")         = TYE(e) - TYE0(e)                                 ;
CalibCheck("QGD",c,"NaN","NaN","NaN")         = QGD(c) - QGD0(c)                                 ;
CalibCheck("SHH",h,"NaN","NaN","NaN")         = SHH(h) - SHH0(h)                                 ;
CalibCheck("SEN",e,"NaN","NaN","NaN")         = SEN(e) - SEN0(e)                                 ;
CalibCheck("QINVD",c,i,"NaN","NaN")           = QINVD(c,i) - QINVD0(c,i)                         ;
CalibCheck("QINV",i,"NaN","NaN","NaN")        = QINV(i) - QINV0(i)                               ;
CalibCheck("INVSH_I",i,"NaN","NaN","NaN")     = INVSH_I(i) - INVSH_I0(i)                         ;
CalibCheck("YFWOR",w,f,"NaN","NaN")           = YFWOR(w,f) - YFWOR0(w,f)                         ;
CalibCheck("VEDSH",e,"NaN","NaN","NaN")       = VEDSH(e) - VEDSH0(e)                             ;
CalibCheck("QEDADJ","NaN","NaN","NaN","NaN")  = QEDADJ - QEDADJ0                                 ;
CalibCheck("HEADJ","NaN","NaN","NaN","NaN")   = HEADJ - HEADJ0                                   ;
CalibCheck("MTAX","NaN","NaN","NaN","NaN")    = MTAX - MTAX0                                     ;
CalibCheck("ETAX","NaN","NaN","NaN","NaN")    = ETAX - ETAX0                                     ;
CalibCheck("DTAX","NaN","NaN","NaN","NaN")    = DTAX - DTAX0                                     ;
CalibCheck("FYTAX","NaN","NaN","NaN","NaN")   = FYTAX - FYTAX0                                   ;
CalibCheck("ITAX","NaN","NaN","NaN","NaN")    = ITAX - ITAX0                                     ;
CalibCheck("STAX","NaN","NaN","NaN","NaN")    = STAX - STAX0                                     ;
CalibCheck("FTAX","NaN","NaN","NaN","NaN")    = FTAX - FTAX0                                     ;
CalibCheck("VTAX","NaN","NaN","NaN","NaN")    = VTAX - VTAX0                                     ;
CalibCheck("TEADJ",w,"NaN","NaN","NaN")       = TEADJ(w) - TEADJ0(w)                             ;
CalibCheck("TMADJ",w,c,"NaN","NaN")           = TMADJ(w,c) - TMADJ0(w,c)                         ;
CalibCheck("TSADJ","NaN","NaN","NaN","NaN")   = TSADJ - TSADJ0                                   ;
CalibCheck("TVADJ","NaN","NaN","NaN","NaN")   = TVADJ - TVADJ0                                   ;
CalibCheck("TXADJ","NaN","NaN","NaN","NaN")   = TXADJ - TXADJ0                                   ;
CalibCheck("TFADJ","NaN","NaN","NaN","NaN")   = TFADJ - TFADJ0                                   ;
CalibCheck("TYFADJ","NaN","NaN","NaN","NaN")  = TYFADJ - TYFADJ0                                 ;
CalibCheck("TYHADJ","NaN","NaN","NaN","NaN")  = TYHADJ - TYHADJ0                                 ;
CalibCheck("TYADJ","NaN","NaN","NaN","NaN")   = TYADJ - TYADJ0                                   ;
CalibCheck("TYEADJ","NaN","NaN","NaN","NaN")  = TYEADJ - TYEADJ0                                 ;
CalibCheck("DTE",w,"NaN","NaN","NaN")         = DTE(w) - DTE0(w)                                 ;
CalibCheck("DTM",w,"NaN","NaN","NaN")         = DTM(w) - DTM0(w)                                 ;
CalibCheck("DTS","NaN","NaN","NaN","NaN")     = DTS - DTS0                                       ;
CalibCheck("DTV","NaN","NaN","NaN","NaN")     = DTV - DTV0                                       ;
CalibCheck("DTX","NaN","NaN","NaN","NaN")     = DTX - DTX0                                       ;
CalibCheck("DTF","NaN","NaN","NaN","NaN")     = DTF - DTF0                                       ;
CalibCheck("DTYF","NaN","NaN","NaN","NaN")    = DTYF - DTYF0                                     ;
CalibCheck("DTYH","NaN","NaN","NaN","NaN")    = DTYH - DTYH0                                     ;
CalibCheck("DTY","NaN","NaN","NaN","NaN")     = DTY - DTY0                                       ;
CalibCheck("DTYE","NaN","NaN","NaN","NaN")    = DTYE - DTYE0                                     ;
CalibCheck("YG","NaN","NaN","NaN","NaN")      = YG - YG0                                         ;
CalibCheck("QGDADJ","NaN","NaN","NaN","NaN")  = QGDADJ - QGDADJ0                                 ;
CalibCheck("HGADJ","NaN","NaN","NaN","NaN")   = HGADJ - HGADJ0                                   ;
CalibCheck("HOGOV",h,"NaN","NaN","NaN")       = HOGOV(h) - HOGOV0(h)                             ;
CalibCheck("DHOGOV","NaN","NaN","NaN","NaN")  = DHOGOV - DHOGOV0                                 ;
CalibCheck("EGADJ","NaN","NaN","NaN","NaN")   = EGADJ - EGADJ0                                   ;
CalibCheck("VGD","NaN","NaN","NaN","NaN")     = VGD - VGD0                                       ;
CalibCheck("EG","NaN","NaN","NaN","NaN")      = EG - EG0                                         ;
CalibCheck("SADJ","NaN","NaN","NaN","NaN")    = SADJ - SADJ0                                     ;
CalibCheck("SHADJ","NaN","NaN","NaN","NaN")   = SHADJ - SHADJ0                                   ;
CalibCheck("SEADJ","NaN","NaN","NaN","NaN")   = SEADJ - SEADJ0                                   ;
CalibCheck("DSHH","NaN","NaN","NaN","NaN")    = DSHH - DSHH0                                     ;
CalibCheck("DS","NaN","NaN","NaN","NaN")      = DS - DS0                                         ;
CalibCheck("DSEN","NaN","NaN","NaN","NaN")    = DSEN - DSEN0                                     ;
CalibCheck("TOTSAV","NaN","NaN","NaN","NaN")  = TOTSAV - TOTSAV0                                 ;
CalibCheck("IADJ","NaN","NaN","NaN","NaN")    = IADJ  - IADJ0                                    ;
CalibCheck("IADJTy",i,"NaN","NaN","NaN")      = IADJTy(i)  - IADJTy0(i)                          ;
CalibCheck("INVEST","NaN","NaN","NaN","NaN")  = INVEST - INVEST0                                 ;
CalibCheck("KAPGOV","NaN","NaN","NaN","NaN")  = KAPGOV - KAPGOV0                                 ;
CalibCheck("KAPREG",w,"NaN","NaN","NaN")      = KAPREG(w) - KAPREG0(w)                           ;
CalibCheck("VFDOMD","NaN","NaN","NaN","NaN")  = VFDOMD - VFDOMD0                                 ;
CalibCheck("INVESTSH","NaN","NaN","NaN","NaN")= INVESTSH - INVESTSH0                             ;
CalibCheck("VGDSH","NaN","NaN","NaN","NaN")   = VGDSH - VGDSH0                                   ;
CalibCheck("GDP","NaN","NaN","NaN","NaN")     = GDP - GDP0                                       ;
CalibCheck("WALRAS","NaN","NaN","NaN","NaN")  = WALRAS - WALRAS0                                 ;
CalibCheck("ER",w,"NaN","NaN","NaN")          = ER(w) - ER0(w)                                   ;
CalibCheck("CPI","NaN","NaN","NaN","NaN")     = CPI - CPI0                                       ;
CalibCheck("PPI","NaN","NaN","NaN","NaN")     = PPI - PPI0                                       ;
CalibCheck("UNEMP",ff,"NaN","NaN","NaN")      = UNEMP(ff) - UNEMP0(ff)                           ;
calibCheck("PQC",cc,h,"NaN","NaN")            = PQC(cc,h)      - PQC0(cc,h)                      ;
calibCheck("EXTENS",ff,a,"NaN","NaN")         = EXTENS(ff,a)   - EXTENS0(ff,a)                   ;
calibCheck("EXTENSSHR",ff,a,"NaN","NaN")      = EXTENSSHR(ff,a)- EXTENSSHR0(ff,a)                ;
calibCheck("ADFH",ff,h,"NaN","NaN")           = ADFH(ff,h)     - ADFH0(ff,h)                     ;
CalibCheck(var,sac,sacp,sacpp,sacppp)$(abs(CalibCheck(var,sac,sacp,sacpp,sacppp)) LT 0.000000001)=0;

$offDotL