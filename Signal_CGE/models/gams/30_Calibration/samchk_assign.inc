* -------------- DEMETRA SAM%samNo% checks ----------------------------------------
$ontext
  This file checks that the model is calibrated correctly by checking that
the claibrated values for variables and parameters produce balanced Macro
and Micro SAM.

  The programme aborts IF checks are failed and reports are displayed.
$offtext

*- ------- MACRO SAM ------------------------------------------------------
$ontext
  This section checks that the model is calibrated with a balanced SAM,
by using a Macro SAM.

  The programme aborts IF
           - ROW AND COLUMN SUMS FOR ASAM%samNo% NOT EQUAL
           - ALL ASAM%samNo% CELL ENTRIES DO NOT EQUAL ASAM0 ENTRIES

  Reports are produced for
      i)   the ratio of ASAM%samNo% to ASAM0 (all should equal 1)
      ii)  the differences between the Macro SAMs
      iii) a count of the number of differences.
$offtext

 ASAM%samNo%("COMMDTY","MARG")     = SUM(c,QTTD.L(c)*PQD.L(c)) ;
 ASAM%samNo%("COMMDTY","ACTIVITY") = SUM((c,a),QINTD.L(c,a)*PQD.L(c)) ;
*- ASAM%samNo%("COMMDTY","HHOLDS")   = SUM((c,h),QCD.L(c,h)*PQD.L(c)*(1+TV.L(c))) ;
 ASAM%samNo%("COMMDTY","HHOLDS")   = SUM((c,h),PQD.L(c)*(1+TV.L(c))*QCD.L(c,h)$ccesn(c))
                                  + SUM((cag,c,h),PQD.L(c) * (1+TV.L(c))
                                         * QCD2.L(cag,c,h)$cces(c)) ;
 ASAM%samNo%("COMMDTY","ENTP")     = SUM((c,e),QED.L(c,e)*PQD.L(c)) ;
 ASAM%samNo%("COMMDTY","GOVTN")    = SUM(c,QGD.L(c)*PQD.L(c)) ;
 ASAM%samNo%("COMMDTY","KAPITAL")  = SUM((c,i),QINVD.L(c,i)*PQD.L(c)) ;
 ASAM%samNo%("COMMDTY","WORLD")    = SUM((w,c),PWE.L(c)*QER.L(c,w)*ER.L(w)) ;
 ASAM%samNo%("MARG","COMMDTY")     = SUM((m,c,w),ioqttqe(m,c,w) * PTT.L(m) * QER.L(c,w))
                                + SUM((m,c),IOQTTQQ.L(m,c) * PTT.L(m) * QQ.L(c)) ;

 ASAM%samNo%("ACTIVITY","COMMDTY") = SUM(a,PX.L(a)*QX.L(a)) ;

 ASAM%samNo%("VALUAD","ACTIVITY")  = SUM((f,a),WF.L(f)*WFDIST.L(f,a)*FD.L(f,a)) ;
 ASAM%samNo%("VALUAD","WORLD")     = SUM((w,f),factwor(f,w)*ER.L(w)) ;

 ASAM%samNo%("HHOLDS","VALUAD")    = SUM((h,f),INSVA.L(h,f)) ;
 ASAM%samNo%("HHOLDS","HHOLDS")    = SUM((h,hp),hohosh(h,hp)
                                *((YH.L(h)*(1-TYH.L(h)))*(1-SHH.L(h)))) ;
 ASAM%samNo%("HHOLDS","ENTP")      = SUM((h,e),HOENT.L(h,e)) ;
 ASAM%samNo%("HHOLDS","GOVTN")     = SUM(h,HOGOV.L(h)) ;
 ASAM%samNo%("HHOLDS","WORLD")     = SUM((h,w),HOWOR.L(h,w)*ER.L(w)) ;

 ASAM%samNo%("ENTP","VALUAD")      = SUM((e,f),INSVA.L(e,f)) ;
 ASAM%samNo%("ENTP","GOVTN")       = SUM(e,EGADJ.L*entgovconst(e)*CPI.L) ;
 ASAM%samNo%("ENTP","WORLD")       = SUM((w,e),entwor(e,w)*ER.L(w)) ;

 ASAM%samNo%("GOVTN","COMMDTY")    = SUM((w,c),TM.L(w,c)*PWM.L(c)*QMR.L(w,c)*ER.L(w))
                              + SUM((w,c),TE.L(c,w)*PWE.L(c)*ER.L(w)*QER.L(c,w))
                              + SUM(c,TS.L(c)*PQS.L(c)*QQ.L(c))
                              + SUM((c,h),TV.L(c)*PQD.L(c)*(QCD.L(c,h)+SUM(cag,QCD2.L(cag,c,h))));

 ASAM%samNo%("GOVTN","ACTIVITY")   = SUM(a,(TX.L(a))*PX.L(a)*QX.L(a))
                              + SUM((ff,a),TF.L(ff,a)*WF.L(ff)*WFDIST.L(ff,a)
                                *FD.L(ff,a))+SUM(a,QINT.L(a)*PINT.L(a)) ;
 ASAM%samNo%("GOVTN","VALUAD")     = SUM(f,govvash(f)*YFDISP.L(f))
                              + SUM(f,TYF.L(f)*(YF.L(f)*(1- deprec(f)))) ;
 ASAM%samNo%("GOVTN","HHOLDS")     = SUM(h,TYH.L(h)*YH.L(h)) ;
 ASAM%samNo%("GOVTN","ENTP")       = SUM(e,GOVENT.L(e))
                              + SUM((w,e),TYE.L(e)*YE.L(e)) ;
 ASAM%samNo%("GOVTN","WORLD")      = SUM(w,govwor(w)*ER.L(w)) ;

 ASAM%samNo%("KAPITAL","VALUAD")   = SUM(f,deprec(f)*YF.L(f)) ;
 ASAM%samNo%("KAPITAL","HHOLDS")   = SUM(h,(YH.L(h)*(1-TYH.L(h)))*SHH.L(h)) ;
 ASAM%samNo%("KAPITAL","ENTP")     = SUM(e,(YE.L(e)*(1-TYE.L(e)))*SEN.L(e)) ;
 ASAM%samNo%("KAPITAL","GOVTN")    = KAPGOV.L ;
 ASAM%samNo%("KAPITAL","WORLD")    = SUM(w,KAPREG.L(w)*ER.L(w)) ;

 ASAM%samNo%("WORLD","COMMDTY")    = SUM((w,c),PWM.L(c)*QMR.L(w,c)*ER.L(w)) ;
 ASAM%samNo%("WORLD","VALUAD")     = SUM((w,f),YFWOR.L(w,f)) ;

 ASAM%samNo%("totals",ssnp)        = SUM(ssn,ASAM%samNo%(ssn,ssnp)) ;
 ASAM%samNo%(ssn,"totals")         = SUM(ssnp,ASAM%samNo%(ssn,ssnp)) ;


*--------- Checking that a balanced and equal ASAM is produced



 ASAM%samNo%BAL(ss) = ASAM%samNo%(ss,"totals")-ASAM%samNo%("totals",ss) ;
 ASAM%samNo%BAL(ss)$(ABS(ASAM%samNo%BAL(ss) LT 1E-6)) = 0;
 ASAM%samNo%CHK(ss,ssp)$ASAM0(ss,ssp)
                   = (ASAM%samNo%(ss,ssp))/ASAM0(ss,ssp)-mod_cont("numerchk") ;

 ASAM%samNo%DIFF(ss,ssp)  = ASAM0(ss,ssp) - ASAM%samNo%(ss,ssp) ;

 ASAM%samNo%DIFF(ss,ssp)$(ABS(ASAM%samNo%DIFF(ss,ssp)
                  lt (10*mod_cont("toldiffsam")))) = 0.0 ;

 ASAM%samNo%DIFF("totals","totals")   = 0.0 ;

 ASAM%samNo%CNT  = SUM((ssn,ssnp)$ASAM%samNo%DIFF(ssn,ssnp), 1) ;


*-Display ASAM%samNo%, ASAM2, DIFFASAM2 ;


*- ------- Micro SAM ------------------------------------------------------
$ontext
  This section checks that the model is calibrated with a balanced SAM,
by using a Micro SAM.

  The programme aborts IF
           - ALL SAM%samNo% CELL ENTRIES DO NOT EQUAL SAM0 ENTRIES

  Reports are produced for
      i)   the ratio of ASAM%samNo% to ASAM0 (all should equal 1)
      ii)  the differences between the Macro SAMs
      iii) a count of the number of differences.
$offtext
display map_c_f_a ;

*If(flow_cont("micSAM%samNo%") = 1,

 SAM%samNo%(c,m)              = ioqtdqtt(c,m)*QTT.L(m)*PQD.L(c) ;

 SAM%samNo%(c,a)              = ioqtdqd(c,a)*QINT.L(a)*PQD.L(c)+ SUM((fc)$map_c_f_a(c,fc,a),FD.L(fc,a)*WF.L(fc)*WFDIST.L(fc,a));

*- SAM%samNo%(c,h)              = QCD.L(c,h)*PQD.L(c)*(1+TV.L(c)) ;

 SAM%samNo%(c,h)              = (PQD.L(c)*(1+TV.L(c))*QCD.L(c,h)$ccesn(c))
                           + SUM(cag,PQD.L(c)*(1+TV.L(c))*QCD2.L(cag,c,h)$cces(c)) ;

 SAM%samNo%(c,e)              = QED.L(c,e)*PQD.L(c) ;

 SAM%samNo%(c,govert)         = QGD.L(c)*PQD.L(c) ;

 SAM%samNo%(c,i)              = QINVD.L(c,i)*PQD.L(c) ;

 SAM%samNo%(in,is)         = SUM(c,QINVD.L(c,in)*PQD.L(c)) ;
*- SAM%samNo%("DSTOC",is)    = SUM(c,PQD.L(c)*dstocconst(c)) ;

*- SAM%samNo%(c,is)          = QINVD.L(c)*PQD.L(c) ;
*- SAM%samNo%(c,"DSTOC")        = PQD.L(c)*dstocconst(c) ;
*- SAM%samNo%("DSTOC",is)    = SUM(c,PQD.L(c)*dstocconst(c)) ;

 SAM%samNo%(c,w)          = PWE.L(c)*QER.L(c,w)*ER.L(w) ;

 SAM%samNo%(m,c)              = SUM(w,ioqttqe(m,c,w) * PTT.L(m) * QER.L(c,w))
                           +(IOQTTQQ.L(m,c) * PTT.L(m) * QQ.L(c)) ;

 SAM%samNo%(a,c)              = PXAC.L(a,c)*QXAC.L(a,c) ;

 SAM%samNo%(f,a)              = WF.L(f)*WFDIST.L(f,a)*FD.L(f,a) ;

 SAM%samNo%(f,w)          = factwor(f,w)*ER.L(w) ;

 SAM%samNo%(h,f)              = INSVA.L(h,f) ;
*- SAM%samNo%(h,f)              = hovash(h,f)*YFDISP.L(f) ;

 SAM%samNo%(h,hp)             = hohosh(h,hp)
                                * ((YH.L(h)*(1-TYH.L(h)))*(1-SHH.L(h))) ;

 SAM%samNo%(h,e)              = HOENT.L(h,e) ;

 SAM%samNo%(h,govert)         = HOGOV.L(h) ;

 SAM%samNo%(h,w)          = HOWOR.L(h,w)*ER.L(w) ;

 SAM%samNo%(e,f)              = INSVA.L(e,f) ;
*- SAM%samNo%(e,f)              = entvash(e,f)*YFDISP.L(f) ;

 SAM%samNo%(e,govert)         = EGADJ.L*entgovconst(e)*CPI.L ;

 SAM%samNo%(e,w)          = entwor(e,w)*ER.L(w) ;

 SAM%samNo%(govert,gt)$SUM((w,c),map_mtax_w(gt,w))  = SUM((w,c)$map_mtax_w(gt,w),TM.L(w,c)*PWM.L(c)*QMR.L(w,c)*ER.L(w)) ;
 SAM%samNo%(gt,c)$SUM(w,map_mtax_w(gt,w))       = SUM(w$map_mtax_w(gt,w),TM.L(w,c)*PWM.L(c)*QMR.L(w,c)*ER.L(w)) ;

 SAM%samNo%(govert,gt)$SUM((w,c),map_etax_w(gt,w))  = SUM((w,c)$map_etax_w(gt,w),TE.L(c,w)*PWE.L(c)*ER.L(w)*QER.L(c,w)) ;
 SAM%samNo%(gt,c)$SUM(w,map_etax_w(gt,w))       = SUM(w$map_etax_w(gt,w),TE.L(c,w)*PWE.L(c)*ER.L(w)*QER.L(c,w)) ;

 SAM%samNo%(govert,saltax)  = SUM(c,TS.L(c)*PQS.L(c)*QQ.L(c)) ;
 SAM%samNo%(saltax,c)       = TS.L(c)*PQS.L(c)*QQ.L(c) ;

 SAM%samNo%(govert,vattax)  = SUM(c,SUM(h,TV.L(c)*PQD.L(c)*QCD.L(c,h))+ SUM((cag,h),TV.L(c)*PQD.L(c)*QCD2.L(cag,c,h))) ;
 SAM%samNo%(vattax,c)       = SUM(h,TV.L(c)*PQD.L(c)*QCD.L(c,h))+ SUM((cag,h),TV.L(c)*PQD.L(c)*QCD2.L(cag,c,h));

 SAM%samNo%(govert,indtax)  = SUM(a,(TX.L(a))*PX.L(a)*QX.L(a)) ;
 SAM%samNo%(indtax,a)       = (TX.L(a))*PX.L(a)*QX.L(a) ;

 SAM%samNo%(govert,tff)       = SUM(a,SUM(ff$map_tff_f(tff,ff),
                             TF.L(ff,a)*WF.L(ff)*WFDIST.L(ff,a)*FD.L(ff,a))) ;
 SAM%samNo%(tff,a)            = SUM(ff$map_tff_f(tff,ff),
                             TF.L(ff,a)*WF.L(ff)*WFDIST.L(ff,a)*FD.L(ff,a)) ;

 SAM%samNo%(facttax,f)      = TYF.L(f)*(YF.L(f)*(1- deprec(f))) ;
 SAM%samNo%(govert,facttax) = SUM(f,TYF.L(f)*(YF.L(f)*(1- deprec(f)))) ;

 SAM%samNo%(dirtax,h)       = TYH.L(h)*YH.L(h) ;

 SAM%samNo%(dirtax,e)       = TYE.L(e)*YE.L(e) ;

 SAM%samNo%(govert,dirtax)  = SUM(h,TYH.L(h)*YH.L(h)) +
                                SUM(e,(TYE.L(e)*YE.L(e))) ;

 SAM%samNo%(govert,f)         = govvash(f)*YFDISP.L(f) ;

 SAM%samNo%(govert,w)     = (govwor(w)*ER.L(w)) ;

 SAM%samNo%(is,f)          = deprec(f)*YF.L(f) ;

 SAM%samNo%(is,h)          = (YH.L(h)*(1-TYH.L(h)))*SHH.L(h) ;

 SAM%samNo%(is,e)          = (YE.L(e) * (1-TYE.L(e)))*SEN.L(e) ;
 SAM%samNo%(is,govert)     = KAPGOV.L ;

 SAM%samNo%(is,w)      = ER.L(w)*(SUM(cm,PWM.L(cm)*QMR.L(w,cm))
                             + (SUM(f,YFWOR.L(w,f))/ER.L(w))
                             - SUM(ce,PWE.L(ce)*QER.L(ce,w))
                             - SUM(h,HOWOR.L(h,w))
                             - SUM(e,entwor(e,w))
                             - govwor(w)
                             - SUM(f,factwor(f,w))) ;

 SAM%samNo%(w,c)          = PWM.L(c)*QMR.L(w,c)*ER.L(w);

*/(1+TM.L(w,c)) ;
 SAM%samNo%(w,f)          = YFWOR.L(w,f) ;

 SAM%samNo%(total,SAC)      = SUM(SACNP, SAM%samNo%(SACNP,SAC)) ;
 SAM%samNo%(SAC,total)      = SUM(SACNP, SAM%samNo%(SAC,SACNP)) ;

*- SAM%samNo%(SAC,SACP)         = SAM%samNo%(SAC,SACP) * samscal ;

*--------- Checking that a balanced and equal SAM is produced

*- Testing for differences between base (adjusted) SAM and MICROSAM%samNo%

 SAM%samNo%CHK(sac,sacp)$SAM(sac,sacp)
                    = SAM%samNo%(sac,sacp)/SAM(sac,sacp)-mod_cont("numerchk") ;

  SAM%samNo%CHK(sac,sacp)$(ABS( SAM%samNo%CHK(sac,sacp)) lt mod_cont("toldiffsam")) = 0;

 SAM%samNo%DIFF(sac,sacp) = SAM(sac,sacp) - SAM%samNo%(sac,sacp) ;

 SAM%samNo%DIFF(sac,sacp)$(ABS(SAM%samNo%DIFF(sac,sacp)) lt mod_cont("toldiffsam"))
                    = 0 ;

 SAM%samNo%DIFF(total,total)   = 0.0 ;

 SAM%samNo%CNT  = SUM((sac,sacp)$SAM%samNo%DIFF(sac,sacp), 1) ;

 SAM%samNo%BAL(sac) =  SAM%samNo%(sac,total)- SAM%samNo%(total,sac);

 SAM%samNo%BAL(sac)$(ABS(SAM%samNo%BAL(sac)) LT 1E-7) =  0;
*----- Abort Statements
display SAM%samNo%CNT, SAM%samNo%CHK ;

$ifthene.samChk %samNo%<2
 ABORT$(SAM%samNo%CNT GT 0.0)
         "ALL SAM%samNo% CELL ENTRIES DO NOT EQUAL SAM ENTRIES: Check SAM%samNo%CNT" ;

*- No totals check required since SAM has already been checked

*- End of IF
*) ;

 ABORT$(ASAM%samNo%CNT GT 0.0)
         "ALL ASAM%samNo% CELL ENTRIES DO NOT EQUAL ASAM0 ENTRIES: CHECK ASAM%samNo%CNT " ;
$endif.samChk

* ABORT $(SUM(sac,ABS(SAM%samNo%BAL(sac))) GT 0.000005)
*         "SAM ROW AND COLUMN SUMS NOT EQUAL: Check SAM%samNo%BAL " ;


*- -------------- end of DEMETRA SAM%samNo% checks --------------------------------

*--------- Checking price changes for numeraire tests



IF (mod_cont("numerchk") NE 1.00,


 PWE_nchk%samNo%(c)$PWE0(c)             =  PWE.L(c)/PWE0(c) ;
 PER_nchk%samNo%(c,w)$PER0(c,w)               =  PER.L(c,w)/PER0(c,w) ;
 PD_nchk%samNo%(c)$PD0(c)               =  PD.L(c)/PD0(c) ;

 PWM_nchk%samNo%(c)$PWM0(c)             =  PWM.L(c)/PWM0(c) ;
 PMR_nchk%samNo%(w,c)$PMR0(w,c)         =  PMR.L(w,c)/PMR0(w,c) ;

 PTT_nchk%samNo%(m)$PTT0(m)             =  PTT.L(m)/PTT0(m) ;

 PQS_nchk%samNo%(c)$PQS0(c)             =  PQS.L(c)/PQS0(c) ;
 PQD_nchk%samNo%(cc)$PQD0(cc)           =  PQD.L(cc)/PQD0(cc) ;

 PQCD_nchk%samNo%(cag,h)$PQCD0(cag,h)   =  PQCD.L(cag,h)/PQCD0(cag,h) ;

 PX_nchk%samNo%(a)$PX0(a)               =  PX.L(a)/PX0(a) ;

 PVA_nchk%samNo%(a)$PVA0(a)             =  PVA.L(a)/PVA0(a) ;
 PINT_nchk%samNo%(a)$PINT0(a)           =  PINT.L(a)/PINT0(a) ;

 WF_nchk%samNo%(ff)$WF0(ff)             =  WF.L(ff)/WF0(ff) ;

 PXC_nchk%samNo%(c)$PXC0(c)             =  PXC.L(c)/PXC0(c) ;

 PXAC_nchk%samNo%(a,c)$PXAC0(a,c)       =  PXAC.L(a,c)/PXAC0(a,c) ;

  ) ;
