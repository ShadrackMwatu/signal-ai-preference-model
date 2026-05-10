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
Parameter
 ASAM%samNo%(ss,ss)   Macro Social Accounting Matrix(1&2 are calibration 3 is postsim)


OPTION DECIMALS = 6 ;

 ASAM%samNo%("COMMDTY","MARG")     = SUM(c,QTTD.L(c)*PQD.L(c)) ;
 ASAM%samNo%("COMMDTY","ACTIVITY") = SUM((c,a),QINTD.L(c,a)*PQD.L(c)) ;
*- ASAM%samNo%("COMMDTY","HHOLDS")   = SUM((c,h),QCD.L(c,h)*PQD.L(c)*(1+TV.L(c))) ;
 ASAM%samNo%("COMMDTY","HHOLDS")   = SUM((c,h),PQD.L(c)*(1+TV.L(c))*QCD.L(c,h)$ccesn(c))
                                  + SUM((cag,c,h),PQD.L(c) * (1+TV.L(c))
                                         * QCD2.L(cag,c,h)$cces(c)) ;
 ASAM%samNo%("COMMDTY","ENTP")     = SUM((c,e),QED.L(c,e)*PQD.L(c)) ;
 ASAM%samNo%("COMMDTY","GOVTN")    = SUM(c,QGD.L(c)*PQD.L(c)) ;
 ASAM%samNo%("COMMDTY","KAPITAL")  = SUM((c,i),QINVD.L(c,i)*PQD.L(c)) ;
 ASAM%samNo%("COMMDTY","WORLD")    = SUM(c,PWE.L(c)*QE.L(c)*ER.L) ;
 ASAM%samNo%("MARG","COMMDTY")     = SUM((m,c),ioqttqe(m,c) * PTT.L(m) * QE.L(c))
                                + SUM((m,c),ioqttqq(m,c) * PTT.L(m) * QQ.L(c)) ;

 ASAM%samNo%("ACTIVITY","COMMDTY") = SUM(a,PX.L(a)*QX.L(a)) ;

 ASAM%samNo%("VALUAD","ACTIVITY")  = SUM((f,a),WF.L(f)*WFDIST.L(f,a)*FD.L(f,a)) ;
 ASAM%samNo%("VALUAD","WORLD")     = SUM(f,factwor(f)*ER.L) ;

 ASAM%samNo%("HHOLDS","VALUAD")    = SUM((h,f),INSVA.L(h,f)) ;
 ASAM%samNo%("HHOLDS","HHOLDS")    = SUM((h,hp),hohosh(h,hp)
                                *((YH.L(h)*(1-TYH.L(h)))*(1-SHH.L(h)))) ;
 ASAM%samNo%("HHOLDS","ENTP")      = SUM((h,e),HOENT.L(h,e)) ;
 ASAM%samNo%("HHOLDS","GOVTN")     = SUM(h,hogovconst(h)*CPI.L*HGADJ.L) ;
 ASAM%samNo%("HHOLDS","WORLD")     = SUM(h,HOWOR.L(h)*ER.L) ;

 ASAM%samNo%("ENTP","VALUAD")      = SUM((e,f),INSVA.L(e,f)) ;
 ASAM%samNo%("ENTP","GOVTN")       = SUM(e,EGADJ.L*entgovconst(e)*CPI.L) ;
 ASAM%samNo%("ENTP","WORLD")       = SUM(e,entwor(e)*ER.L) ;

 ASAM%samNo%("GOVTN","COMMDTY")    = SUM(c,TM.L(c)*PWM.L(c)*QM.L(c)*ER.L)
                              + SUM(c,TE.L(c)*PWE.L(c)*ER.L*QE.L(c))
                              + SUM(c,TS.L(c)*PQS.L(c)*QQ.L(c))
                              + SUM((c,h),TV.L(c)*PQD.L(c)*(QCD.L(c,h)+SUM(cag,QCD2.L(cag,c,h))))
                              + SUM(c,TEX.L(c)*PQS.L(c)*QQ.L(c)) ;

 ASAM%samNo%("GOVTN","ACTIVITY")   = SUM(a,TX.L(a)*PX.L(a)*QX.L(a))
                              + SUM((f,a),TF.L(f,a)*WF.L(f)*WFDIST.L(f,a)
                                *FD.L(f,a)) ;
 ASAM%samNo%("GOVTN","VALUAD")     = SUM(f,govvash(f)*YFDISP.L(f))
                              + SUM(f,TYF.L(f)*(YF.L(f)*(1- deprec(f)))) ;
 ASAM%samNo%("GOVTN","HHOLDS")     = SUM(h,TYH.L(h)*YH.L(h)) ;
 ASAM%samNo%("GOVTN","ENTP")       = SUM(e,GOVENT.L(e))
                              + SUM(e,TYE.L(e)*YE.L(e)) ;
 ASAM%samNo%("GOVTN","WORLD")      = (govwor*ER.L) ;

 ASAM%samNo%("KAPITAL","VALUAD")   = SUM(f,deprec(f)*YF.L(f)) ;
 ASAM%samNo%("KAPITAL","HHOLDS")   = SUM(h,(YH.L(h)*(1-TYH.L(h)))*SHH.L(h)) ;
 ASAM%samNo%("KAPITAL","ENTP")     = SUM(e,(YE.L(e)*(1-TYE.L(e)))*SEN.L(e)) ;
 ASAM%samNo%("KAPITAL","GOVTN")    = KAPGOV.L ;
 ASAM%samNo%("KAPITAL","WORLD")    = (KAPREG.L*ER.L) ;

 ASAM%samNo%("WORLD","COMMDTY")    = SUM(c,PWM.L(c)*QM.L(c)*ER.L) ;
 ASAM%samNo%("WORLD","VALUAD")     = SUM(f,YFWOR.L(f)) ;

 ASAM%samNo%("totals",ssnp)        = SUM(ssn,ASAM%samNo%(ssn,ssnp)) ;
 ASAM%samNo%(ssn,"totals")         = SUM(ssnp,ASAM%samNo%(ssn,ssnp)) ;


*--------- Checking that a balanced and equal ASAM is produced

PARAMETER
 ASAM%samNo%CHK(ss,ss)    Ratio of ASAM%samNo% to ASAM0 should be 1
 ASAM%samNo%BAL(ss)             Differences in Row and Column totals of ASAM%samNo%

 ASAM%samNo%DIFF(ss,ss)   Differences between ASAM and ASAM%samNo%

 ASAM%samNo%CNT           Count of non zero entries in DIFFASAM%samNo%

 ;

 ASAM%samNo%BAL(ss) = ASAM%samNo%(ss,"totals")-ASAM%samNo%("totals",ss) ;
 ASAM%samNo%BAL(ss)$(ABS(ASAM%samNo%BAL(ss) LT 1E-6)) = 0;
 ASAM%samNo%CHK(ss,ssp)$ASAM0(ss,ssp)
                   = (ASAM%samNo%(ss,ssp))/ASAM0(ss,ssp) ;

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

PARAMETER
 SAM%samNo%(sac,sacp)      Micro SAM for checking model calibration

 SAM%samNo%CHK(sac,sac)    Ratio of SAM%samNo% to SAM should be 1
 SAM%samNo%DIFF(sac,sac)   Differences between SAM and SAM%samNo%
 SAM%samNo%CNT             Count of non zero entries in SAM%samNo%DIFF
 SAM%samNo%BAL(sac)        Balance of SAM%samNo%
 ;

*If(flow_cont("micSAM%samNo%") = 1,

 SAM%samNo%(c,m)              = ioqtdqtt(c,m)*QTT.L(m)*PQD.L(c) ;

 SAM%samNo%(c,a)              = ioqtdqd(c,a)*QINT.L(a)*PQD.L(c)+ SUM((fc)$map_c_f_a(c,fc,a),FD.L(fc,a)*WF.L(fc)*WFDIST.L(fc,a));

*- SAM%samNo%(c,h)              = QCD.L(c,h)*PQD.L(c)*(1+TV.L(c)) ;

 SAM%samNo%(c,h)              = (PQD.L(c)*(1+TV.L(c))*QCD.L(c,h)$ccesn(c))
                           + SUM(cag,PQD.L(c)*(1+TV.L(c))*QCD2.L(cag,c,h)$cces(c)) ;

 SAM%samNo%(c,e)              = QED.L(c,e)*PQD.L(c) ;

 SAM%samNo%(c,"govt")         = QGD.L(c)*PQD.L(c) ;

 SAM%samNo%(c,i)              = QINVD.L(c,i)*PQD.L(c) ;

 SAM%samNo%(in,"i_s")         = SUM(c,QINVD.L(c,in)*PQD.L(c)) ;
*- SAM%samNo%("DSTOC","i_s")    = SUM(c,PQD.L(c)*dstocconst(c)) ;

*- SAM%samNo%(c,"i_s")          = QINVD.L(c)*PQD.L(c) ;
*- SAM%samNo%(c,"DSTOC")        = PQD.L(c)*dstocconst(c) ;
*- SAM%samNo%("DSTOC","i_s")    = SUM(c,PQD.L(c)*dstocconst(c)) ;

 SAM%samNo%(c,"row")          = PWE.L(c)*QE.L(c)*ER.L ;

 SAM%samNo%(m,c)              = (ioqttqe(m,c) * PTT.L(m) * QE.L(c))
                           +(ioqttqq(m,c) * PTT.L(m) * QQ.L(c)) ;

 SAM%samNo%(a,c)              = PXAC.L(a,c)*QXAC.L(a,c) ;

 SAM%samNo%(f,a)              = WF.L(f)*WFDIST.L(f,a)*FD.L(f,a) ;

 SAM%samNo%(f,"row")          = factwor(f)*ER.L ;

 SAM%samNo%(h,f)              = INSVA.L(h,f) ;
* SAM%samNo%(h,f)              = SUM(a,WFA.L(f,a)*FSI.L(ins,f)) ;
*- SAM%samNo%(h,f)              = hovash(h,f)*YFDISP.L(f) ;

 SAM%samNo%(h,hp)             = hohosh(h,hp)
                                * ((YH.L(h)*(1-TYH.L(h)))*(1-SHH.L(h))) ;

 SAM%samNo%(h,e)              = HOENT.L(h,e) ;

 SAM%samNo%(h,"govt")         = hogovconst(h)*CPI.L*HGADJ.L ;

 SAM%samNo%(h,"row")          = HOWOR.L(h)*ER.L ;

 SAM%samNo%(e,f)              = INSVA.L(e,f) ;
*- SAM%samNo%(e,f)              = entvash(e,f)*YFDISP.L(f) ;

 SAM%samNo%(e,"govt")         = EGADJ.L*entgovconst(e)*CPI.L ;

 SAM%samNo%(e,"row")          = entwor(e)*ER.L ;

 SAM%samNo%("govt","imptax")  = SUM(c,TM.L(c)*PWM.L(c)*QM.L(c)*ER.L) ;
 SAM%samNo%("imptax",c)       = TM.L(c)*PWM.L(c)*QM.L(c)*ER.L ;

 SAM%samNo%("govt","exptax")  = SUM(c,TE.L(c)*PWE.L(c)*ER.L*QE.L(c)) ;
 SAM%samNo%("exptax",c)       = TE.L(c)*PWE.L(c)*ER.L*QE.L(c) ;

 SAM%samNo%("govt","saltax")  = SUM(c,TS.L(c)*PQS.L(c)*QQ.L(c)) ;
 SAM%samNo%("saltax",c)       = TS.L(c)*PQS.L(c)*QQ.L(c) ;

 SAM%samNo%("govt","vattax")  = SUM(c,SUM(h,TV.L(c)*PQD.L(c)*QCD.L(c,h))+ SUM((cag,h),TV.L(c)*PQD.L(c)*QCD2.L(cag,c,h))) ;
 SAM%samNo%("vattax",c)       = SUM(h,TV.L(c)*PQD.L(c)*QCD.L(c,h))+ SUM((cag,h),TV.L(c)*PQD.L(c)*QCD2.L(cag,c,h));

 SAM%samNo%("govt","ectax")   = SUM(c,TEX.L(c)*PQS.L(c)*QQ.L(c)) ;
 SAM%samNo%("ectax",c)        = TEX.L(c)*PQS.L(c)*QQ.L(c) ;

 SAM%samNo%("govt","indtax")  = SUM(a,TX.L(a)*PX.L(a)*QX.L(a)) ;
 SAM%samNo%("indtax",a)       = TX.L(a)*PX.L(a)*QX.L(a) ;

 SAM%samNo%("govt",tff)       = SUM(a,SUM(f$map_tff_f(tff,f),
                             TF.L(f,a)*WF.L(f)*WFDIST.L(f,a)*FD.L(f,a))) ;
 SAM%samNo%(tff,a)            = SUM(f$map_tff_f(tff,f),
                             TF.L(f,a)*WF.L(f)*WFDIST.L(f,a)*FD.L(f,a)) ;

 SAM%samNo%("facttax",f)      = TYF.L(f)*(YF.L(f)*(1- deprec(f))) ;
 SAM%samNo%("govt","facttax") = SUM(f,TYF.L(f)*(YF.L(f)*(1- deprec(f)))) ;

 SAM%samNo%("dirtax",h)       = TYH.L(h)*YH.L(h) ;

 SAM%samNo%("dirtax",e)       = TYE.L(e)*YE.L(e) ;

 SAM%samNo%("govt","dirtax")  = SUM(h,TYH.L(h)*YH.L(h)) +
                                SUM(e,(TYE.L(e)*YE.L(e))) ;

 SAM%samNo%("govt",f)         = govvash(f)*YFDISP.L(f) ;

 SAM%samNo%("govt","row")     = (govwor*ER.L) ;

 SAM%samNo%("i_s",f)          = deprec(f)*YF.L(f) ;

 SAM%samNo%("i_s",h)          = (YH.L(h)*(1-TYH.L(h)))*SHH.L(h) ;

 SAM%samNo%("i_s",e)          = (YE.L(e) * (1-TYE.L(e)))*SEN.L(e) ;
 SAM%samNo%("i_s","govt")     = KAPGOV.L ;

 SAM%samNo%("i_s","row")      = (KAPREG.L*ER.L) ;
 SAM%samNo%("row",c)          = PWM.L(c)*QM.L(c)*ER.L ;
 SAM%samNo%("row",f)          = YFWOR.L(f) ;

 SAM%samNo%("total",SAC)      = SUM(SACNP, SAM%samNo%(SACNP,SAC)) ;
 SAM%samNo%(SAC,"total")      = SUM(SACNP, SAM%samNo%(SAC,SACNP)) ;

*- SAM%samNo%(SAC,SACP)         = SAM%samNo%(SAC,SACP) * samscal ;

*--------- Checking that a balanced and equal SAM is produced

*- Testing for differences between base (adjusted) SAM and MICROSAM%samNo%

 SAM%samNo%CHK(sac,sacp)$SAM(sac,sacp)
                    = SAM%samNo%(sac,sacp)/SAM(sac,sacp) ;

 SAM%samNo%DIFF(sac,sacp) = SAM(sac,sacp) - SAM%samNo%(sac,sacp) ;

 SAM%samNo%DIFF(sac,sacp)$(ABS(SAM%samNo%DIFF(sac,sacp)) lt mod_cont("toldiffsam"))
                    = 0 ;

 SAM%samNo%DIFF("total","total")   = 0.0 ;

 SAM%samNo%CNT  = SUM((sac,sacp)$SAM%samNo%DIFF(sac,sacp), 1) ;

 SAM%samNo%BAL(sac) =  SAM%samNo%(sac,"total")- SAM%samNo%("total",sac);

 SAM%samNo%BAL(sac)$(ABS(SAM%samNo%BAL(sac)) LT 1E-7) =  0;
*----- Abort Statements

 OPTION decimals = 3 ;

$ifthene.samChk %samNo%<2
 ABORT$(SAM%samNo%CNT GT 0.0)
         "ALL SAM%samNo% CELL ENTRIES DO NOT EQUAL SAM ENTRIES: Check SAM%samNo%CNT" ;

*- No totals check required since SAM has already been checked

*- End of IF
*) ;

 ABORT$(ASAM%samNo%CNT GT 0.0)
         "ALL ASAM%samNo% CELL ENTRIES DO NOT EQUAL ASAM0 ENTRIES: CHECK ASAM%samNo%CNT " ;
$endif.samChk

 ABORT $(SUM(sac,ABS(SAM%samNo%BAL(sac))) GT 0.000005)
         "SAM ROW AND COLUMN SUMS NOT EQUAL: Check SAM%samNo%BAL " ;


*- -------------- end of DEMETRA SAM%samNo% checks --------------------------------

*--------- Checking price changes for numeraire tests

Parameter

*- #### Exports Block

 PWE_nchk%samNo%(c)       World price of exports in dollars
 PE_nchk%samNo%(c)        Domestic price of exports by activity a
 PD_nchk%samNo%(c)        Consumer price for domestic supply of commodity c

*- #### Imports Block

 PWM_nchk%samNo%(c)       World price of imports in dollars
 PM_nchk%samNo%(c)        Domestic price of competitive imports of commodity c

*- ------- TRADE AND TRANSPORT MARGINS BLOCK ------------------------------

 PTT_nchk%samNo%(m)       Price of trade and transport margin m

*- ------- COMMODITY PRICE BLOCK ------------------------------------------

 PQS_nchk%samNo%(c)       Supply price of composite commodity c
 PQD_nchk%samNo%(cc)      Purchaser price of composite commodity c
 PQCD_nchk%samNo%(cc,h)   Purchaser price of aggregate commodity cag

*- ------- PRODUCTION BLOCK -----------------------------------------------

 PX_nchk%samNo%(a)        Composite price of output by activity a

*- CES aggregation functions for Level 1 of production nest

 PVA_nchk%samNo%(a)       Value added price for activity a
 PINT_nchk%samNo%(a)      Price of aggregate intermediate input

 WF_nchk%samNo%(ff)        Price of factor f

*- Commodity Output

 PXC_nchk%samNo%(c)       Producer price of composite domestic output

*- Activity Output

 PXAC_nchk%samNo%(a,c)    Activity commodity prices

 ;

IF (mod_cont("numerchk") NE 1.00,


 PWE_nchk%samNo%(c)$PWE0(c)             =  PWE.L(c)/PWE0(c) ;
 PE_nchk%samNo%(c)$PE0(c)               =  PE.L(c)/PE0(c) ;
 PD_nchk%samNo%(c)$PD0(c)               =  PD.L(c)/PD0(c) ;

 PWM_nchk%samNo%(c)$PWM0(c)             =  PWM.L(c)/PWM0(c) ;
 PM_nchk%samNo%(c)$PM0(c)               =  PM.L(c)/PM0(c) ;

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
