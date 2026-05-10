* -------------- DEMETRA reset closure variables -------------------------
$ontext
 If closure rules are to be changed when running experiments in LOOPS
 it is necessary to first free all variables that are involved in ANY
 closure rule or the equation variable count will be lost.
$offtext

*-## FOREIGN EXCHANGE MARKET CLOSURE

 ER.LO(w)                 = -inf ;  ER.UP(w)                 = +inf ;
 KAPWOR.LO                = -inf ;  KAPWOR.UP                = +inf ;
 KAPREG.LO(w)             = -inf ;  KAPREG.UP(w)             = +inf ;

 PWM.LO(c)                = -inf ;  PWM.UP(c)                = +inf ;
 PWE.LO(c)$SUM(w,cedn(c,w)) = -inf ;  PWE.UP(c)$SUM(w,cedn(c,w))  = +inf ;

*-## INVESTMENT-SAVINGS CLOSURE

 SADJ.LO                  = -inf ;  SADJ.UP                  = +inf ;
 SHADJ.LO                 = -inf ;  SHADJ.UP                 = +inf ;
 SEADJ.LO                 = -inf ;  SEADJ.UP                 = +inf ;

 DSHH.LO                  = -inf ;  DSHH.UP                  = +inf ;
 DS.LO                    = -inf ;  DS.UP                    = +inf ;
 DSEN.LO                  = -inf ;  DSEN.UP                  = +inf ;

 IADJ.LO                  = -inf ;  IADJ.UP                  = +inf ;
 IADJTy.LO(i)             = -inf ;  IADJTy.UP(i)             = +inf ;
 QINV.LO(i)               = -inf ;  QINV.UP(i)               = +inf ;

 INVEST.LO                = -inf ;  INVEST.UP                = +inf ;
 INVESTSH.LO              = -inf ;  INVESTSH.UP              = +inf ;
 INVSH_I.LO(i)            = -inf ;  INVSH_I.UP(i)            = +inf ;

*-## ENTERPRISE CLOSURE RULES

 QEDADJ.LO                = -inf ;  QEDADJ.UP                = +inf ;
 VED.LO(e)                = -inf ;  VED.UP(e)                = +inf ;
 VEDSH.LO(e)              = -inf ;  VEDSH.UP(e)              = +inf ;

 HEADJ.LO                 = -inf ;  HEADJ.UP                 = +inf ;

*-## GOVT CLOSURE RULES

*- Closure rule for Government savings is part of the Govt Closure Rules

 TEADJ.LO(w)             = -inf ;   TEADJ.UP(w)              = +inf ;
 TMADJ.LO(w,c)           = -inf ;   TMADJ.UP(w,c)            = +inf ;
 TSADJ.LO                = -inf ;   TSADJ.UP                 = +inf ;
 TVADJ.LO                = -inf ;   TVADJ.UP                 = +inf ;
 TXADJ.LO                = -inf ;   TXADJ.UP                 = +inf ;
 TFADJ.LO                = -inf ;   TFADJ.UP                 = +inf ;
 TYFADJ.LO               = -inf ;   TYFADJ.UP                = +inf ;
 TYHADJ.LO               = -inf ;   TYHADJ.UP                = +inf ;
 TYADJ.LO                = -inf ;   TYADJ.UP                 = +inf ;
 TYEADJ.LO               = -inf ;   TYEADJ.UP                = +inf ;


 DTE.LO(w)               = -inf ;   DTE.UP(w)                = +inf ;
 DTM.LO(w)               = -inf ;   DTM.UP(w)                = +inf ;
 DTS.LO                  = -inf ;   DTS.UP                   = +inf ;
 DTV.LO                  = -inf ;   DTV.UP                   = +inf ;
 DTX.LO                  = -inf ;   DTX.UP                   = +inf ;
 DTF.LO                  = -inf ;   DTF.UP                   = +inf ;
 DTYF.LO                 = -inf ;   DTYF.UP                  = +inf ;
 DTYH.LO                 = -inf ;   DTYH.UP                  = +inf ;
 DTY.LO                  = -inf ;   DTY.UP                   = +inf ;
 DTYE.LO                 = -inf ;   DTYE.UP                  = +inf ;

 ETAX.LO                  = -inf;   ETAX.UP                  = +inf ;
 MTAX.LO                  = -inf;   MTAX.UP                  = +inf ;
 STAX.LO                  = -inf;   STAX.UP                  = +inf ;
 DTAX.LO                  = -inf;   DTAX.UP                  = +inf ;
 FYTAX.LO                 = -inf;   FYTAX.UP                 = +inf ;
 ITAX.LO                  = -inf;   ITAX.UP                  = +inf ;
 VTAX.LO                  = -inf;   VTAX.UP                  = +inf ;
 FTAX.LO                  = -inf;   FTAX.UP                  = +inf ;


 QGDADJ.LO                = -inf ;  QGDADJ.UP                = +inf ;

*- EG.LO                    = -inf ;  EG.UP                    = +inf ;
 VGD.LO                   = -inf ;  VGD.UP                   = +inf ;
 VGDSH.LO                 = -inf ;  VGDSH.UP                 = +inf ;

 HGADJ.LO                 = -inf ;  HGADJ.LO                 = +inf ;
 HOGOV.LO(h)              = -inf ;  HOGOV.UP(h)              = +inf ;
 DHOGOV.LO                = -inf ;  DHOGOV.LO                = +inf ;
 EGADJ.LO                 = -inf ;  EGADJ.UP                 = +inf ;
 YGADJ.LO                 = -inf ;  YGADJ.UP                 = +inf ;
 YG.LO                    = -inf ;  YG.UP                    = +inf ;

 KAPGOV.LO                = -inf ;  KAPGOV.UP                = +inf ;



*-## FACTOR MARKET CLOSURE

 FSI.LO(ins,ff)            = -inf ;  FSI.UP(ins,ff)            = +inf ;
 WF.LO(ff)                 = -inf ;  WF.UP(ff)                 = +inf ;
 WFDIST.LO(ff,a)           = -inf ;  WFDIST.UP(ff,a)           = +inf ;
* WFA.LO(ff,a)              = -inf ;  WFA.UP(ff,a)              = +inf ;

 FD.LO(ff,a)               = -inf ;  FD.UP(ff,a)               = +inf ;

*-## TECHNOLOGY CLOSURES

 ADFD.LO(ff,a)            = -inf ;  ADFD.UP(ff,a)            = +inf ;
 ADFH.LO(ff,h)            = -inf ;  ADFH.UP(ff,h)            = +inf ;
 ADFAGfADJ.LO(ff)         = -inf ;  ADFAGfADJ.UP(ff)         = +inf ;
 ADFAGaADJ.LO(a)          = -inf ;  ADFAGaADJ.UP(a)          = +inf ;
 ADFAGADJ.LO              = -inf ;  ADFAGADJ.UP              = +inf ;
*-## GDP CLOSURES

 GDP.LO                    = -inf ;  GDP.UP                  = +inf ;

*-## MISCELLANEOUS FIXED VARIABLES

 CPI.LO                   = -inf ;  CPI.UP                   = +inf ;
 PPI.LO                   = -inf ;  PPI.UP                   = +inf ;

*-## Dynamic variables

 EXTENS.LO(ff,a) = -inf;   EXTENS.UP(ff,a) = +inf;
 ADFExt.LO(ff,a) = -inf;   ADFExt.UP(ff,a) = +inf;

*-## Agricultural budget

 AgBuRecurr.LO(c)      = -inf; AgBuRecurr.UP(c)      = +inf;
 AgBuInvest.LO(i)      = -inf; AgBuInvest.UP(i)      = +inf;
 AgBuInpSub.LO(ff,a)   = -inf; AgBuInpSub.UP(ff,a)   = +inf;
 AgBuOutSub.LO(a)      = -inf; AgBuOutSub.UP(a)      = +inf;
 AgBuTotRecurr.LO      = -inf; AgBuTotRecurr.UP      = +inf;
 AgBuTotInvest.LO      = -inf; AgBuTotInvest.UP      = +inf;
 AgBuTotInpSub.LO      = -inf; AgBuTotInpSub.UP      = +inf;
 AgBuTotOutSub.LO      = -inf; AgBuTotOutSub.UP      = +inf;
 AgBuTOTALx.LO         = -inf; AgBuTOTALx.UP         = +inf;
 AgBuTOTShr.LO         = -inf; AgBuTOTShr.UP         = +inf;

*--------------- end of DEMETRA reset closure variables ------------------
