*--------------------- DEMETRA variable initialisation ----------------------
*----------------------varinit.inc----------------------------------------

$onDotL
*- #### Factor supplies

 FSIL(ins,f)        = FSIL0(ins,f) ;

 FSIM(f,ins,fp,insp) = FSIM0(f,ins,fp,insp) ;


*-## INITIAL VALUES OF VARIABLES FROM PARAMETER SPECIFICATION

*- ------- NORMALISED PRICE BLOCK -----------------------------------------

 PD(c)      = PD0(c) ;

 PM(c)      = PM0(c) ;
 PMR(w,c)   = PMR0(w,c) ;
 PE(c)      = PE0(c) ;
 PER(c,w)   = PER0(c,w) ;

 PQS(c)     = PQS0(c) ;

 PXC(c)     = PXC0(c) ;
 PXAC(a,c)  = PXAC0(a,c) ;
 PX(a)      = PX0(a) ;

 ER(w)         = ER0(w) ;

 ERX          = SUM(w,SUM(c,PER0(c,w)*QER0(c,w))/SUM((cp,wp),PER0(cp,wp)*QER0(cp,wp))*ER0(w));


*- ------- TRADE BLOCK ---------------------------------------------------

*- #### Exports Block

 PWE(c)     = PWE0(c) ;

 QD(c)$cd(c)      = (SUM(a,SAM(a,c)/PXC(c))) - QE0(c) ;

 QER(ce,w)  =  QER0(ce,w);

 ZETAER(c,w)  = ZETAER0(c,w);
 ZETAE (c)    = ZETAE0(c);

 QE(ce)     = QD(ce)*((PE(ce)/PD(ce))*((1-gamma(ce))
                                 /gamma(ce)))**(1/(rhot(ce)-1)) ;

*- #### Imports Block

 PWM(c)     = PWM0(c) ;

 QQ(c)      = QQ0(c) ;

 QMR(w,c)   = QMR0(w,c) ;

 ZETAM(w,c)  = ZETAM0(w,c);


 QM(c)$(cd(c) AND cm(c))
              = QD(c)*((PD(c)/PM(c))
                        *(delta(c)/(1-delta(c))))**(1/(1+rhoc(c))) ;

 QM(c)$(cm(c)) = acR(c)*(SUM(w$deltaR(w,c), deltaR(w,c)*(ZETAM(w,c)*QMR(w,c))**(-rhocR(c))))**(-1/rhocR(c));

*- ------- TRADE AND TRANSPORT MARGINS BLOCK ------------------------------

 PTT(m)       = PTT0(m) ;
 QTT(m)       = QTT0(m) ;
 QTTD(c)      = QTTD0(c) ;
 IOQTTQQ(m,c) = IOQTTQQ0(m,c);
*- ------- COMMODITY PRICE BLOCK ------------------------------------------

 PQD(c)     = PQS0(c) * (1 + ts0(c))
                  + SUM(m,ioqttqq0(m,c) * PTT(m)) ;

 PQCD(cag,h) =  PQCD0(cag,h) ;

 PQC(cc,h) = PQC0(cc,h)  ;

*-Display PQCD ;

*- ------- NUMERAIRE PRICE BLOCK ------------------------------------------
 VQCD(c)       = VQCD0(c) ;
 COMTOTSH(c)   = COMTOTSH0(c);
 CPI           = CPI0 ;
 VDDTOTSH(c)   = VDDTOTSH0(c)  ;
 PPI           = PPI0 ;

*- ------- PRODUCTION BLOCK -----------------------------------------------

*- CES aggregation functions for Level 1 of production nest

 PVA(a)     = PVA0(a) ;

 PINT(a)    = PINT0(a) ;

 QX(a)      = QX0(a) ;

 QINT(a)    = QINT0(a);

 QVA(a)     = QVA0(a) ;
 VVA(a)     = VVA0(a) ;

*- CES aggregation functions for Level 2 of production nest

 ADFD(ff,a)  = ADFD0(ff,a) ;
 ADFH(ff,h)  = ADFH0(ff,h) ;
 AD(ff,a)    = (1+SUM(h$FSI0(h,ff),ADFH(ff,h))/numHH(ff))*ADFD(ff,a) ;

 FD(ff,a)    = FD0(ff,a) ;

 FSI(ins,f)  = FSI0(ins,f) ;

 ADFAG(ff,a)    = adfag0(ff,a);
 ADFAGfADJ(ff)  = ADFAGfADJ0(ff);
 ADFAGaADJ(a)   = ADFAGaADJ0(a);
 PQDDIST(c,a)   = PQDDIST0(c,a);


 UNEMP(ff) = UNEMP0(ff);
 UNEMPRATE(f) = UNEMPRATE0(f);

 FS(ff)      = SUM(a,FD(ff,a))+UNEMP(ff) ;
 FS(fag)     = FS0(fag) ;

 WF(f)$sum(a,SAM(f,a))      = WF0(f) ;


 WF(fc)$ sum((a,c)$ map_c_f_a(c,fc,a),SAM(c,a))
          = SUM((c,a)$map_c_f_a(c,fc,a),PQD(c))
                         /SUM((c,a)$ map_c_f_a(c,fc,a), 1);

 WFDIST(f,a)$FD(f,a)
              = (SAM(f,a)/FD(f,a))/WF(f) ;

 WFDIST(fc,a)$sum(c$ map_c_f_a(c,fc,a),SAM(c,a))
         = (SUM(c$map_c_f_a(c,fc,a),SAM(c,a))/FD(fc,a))/WF(fc) ;


 WFDIST(fc,a)$FD0(fc,a) = ((SAM(fc,a)+SUM(c$map_c_f_a(c,fc,a),SAM(c,a)))
                                                         /FD(fc,a))/WF(fc) ;


 WFDIST(fc,a)$(FD(fc,a) EQ 0) = 0.0 ;

 WF(fag)  = WF0(fag) ;
 WFDIST(fag,a) = WFDIST0(fag,a) ;

 WFA(ff,a) = WFDIST0(ff,a)*WF0(ff);

*- Intermediate Input Demand

 QINTD(c,a)   =  QINTD0(c,a) ;

*- Commodity Output

 QXC (c)= QXC0(c);

*- Activity Output

 QXAC(a,c)  = ioqxacqx(a,c) * QX(a) ;

 IOQXACQXV(a,c)$SUM(cp,QXAC(a,cp)) =  QXAC(a,c)/SUM(cp,QXAC(a,cp)) ;

*- ------- FACTOR BLOCK ---------------------------------------------------

 YF(f)      = SUM(a,WF(f)*WFDIST(f,a)*FD(f,a))
                             + SUM(w,factwor(f,w)*ER(w)) ;

 YFDISP(f)  = (YF(f) * (1- deprec(f)))*(1- tYf0(f)) ;

 YFINS(f)   = YFDISP(f) - [(govvash(f)*YFDISP(f))
                                + SUM(w,worvash(w,f)*YFDISP(f))] ;

 FSISH(ins,f)$SUM(insp,FSI(insp,f))
                   = FSI(ins,f)/SUM(insp,FSI(insp,f)) ;

 INSVA(ins,f)    = FSISH(ins,f) * YFINS(f) ;


*- ------- HOUSEHOLD BLOCK ------------------------------------------------
*- ## Government transfers
 HGADJ   = HGADJ0 ;
 DHOGOV   = DHOGOV0;
 HOGOV(h)   = ((hogovb(h) + dabhogov(h)) * HGADJ
                                 +DHOGOV * hogov01(h)) * CPI ;
*- ## Household Income

 YH(h)      = SUM(f,INSVA(h,f))
                             + SUM(hp,HOHO0(h,hp))
                             + SUM(e,HEADJ0*hoentconst(h,e) * CPI)
                             + HOGOV(h)
                             + SUM(w,HOWOR0(h,w)*ER(w))  ;

*- ## Household Expenditure

 HOHO(h,hp) = hohosh(h,hp)
                *((YH(h) * (1 - tyh0(h))) * (1 - shh0(h))) ;

 HOWOR(h,w) =HOWOR0(h,w);

 HEXP(h)   = ((YH(h) * (1 - tyh0(h))) * (1 - shh0(h)))
                    - SUM(hp,HOHO(hp,h)) ;

 QCD(cc,h) = QCD0(cc,h) ;

 QCD2(cag,cces,h)= QCD20(cag,cces,h) ;

*- ######## ENTERPRISE BLOCK
*- ## Enterprise Income

 YE(e)      = SUM(f,INSVA(e,f))
                             + (EGADJ0*entgovconst(e)*CPI)
                             + SUM(w,entwor(e,w)*ER(w))   ;

*- ## Enterprise Expenditure

 QEDADJ   = QEDADJ0 ;

 QED(c,e) = QEDADJ*qedconst(c,e) ;

 HOENT(h,e) = hoentsh(h,e)
                 * (((YE(e) * (1 - tye0(e))) * (1 - sen0(e)))
                    - SUM(c,QED(c,e)*PQD(c))) ;

 GOVENT(e)  = goventsh(e)
                 * (((YE(e) * (1 - tye0(e))) * (1 - sen0(e)))
                    - SUM(c,QED(c,e)*PQD(c))) ;

 VED(e)      = SUM(c,QED(c,e)*PQD(c)) ;

*- ------- GOVERNMENT BLOCK -----------------------------------------------

*- #### Government Income Block

*- ## Government Taxes

 TEADJ(w)   = TEADJ0(w) ;
 TMADJ(w,c) = TMADJ0(w,c) ;
 TSADJ      = TSADJ0 ;
 TVADJ      = TVADJ0 ;
 TXADJ      = TXADJ0 ;
 TFADJ      = TFADJ0 ;
 TYFADJ     = TYFADJ0 ;
 TYHADJ     = TYHADJ0 ;
 TYADJ      = TYADJ0 ;
 TYEADJ     = TYEADJ0 ;
 THCADJ     = THCADJ0;

 DTE(w)     = DTE0(w) ;
 DTM(w)     = DTM0(w) ;
 DTS        = DTS0 ;
 DTV        = DTV0 ;
 DTX        = DTX0 ;
 DTF        = DTF0 ;
 DTYF       = DTYF0 ;
 DTYH       = DTYH0 ;
 DTY        = DTY0 ;
 DTYE       = DTYE0 ;

 DVTAX      = DVTAX0;
 DTHC       = DTHC0;

 TM(w,c)     = ((tmb(w,c) + dabtm(w,c)) * TMADJ(w,c))
                                      + (DTM(w) * tm01(w,c)) ;

 TE(c,w)      = ((teb(c,w) + dabte(c,w))* TEADJ(w))
                       + (DTE(w)*te01(c,w)) ;

 TS(c)      = ((tsb(c) + dabts(c))* TSADJ)
                         + (DTS*ts01(c)*ts0(c)) ;

 TV(cc)     = ((tvb(cc) + dabtv(cc))* TVADJ)
                         + (DTV*tv01(cc)*tv0(cc)) ;

 TX(a)      = ((txb(a) + dabtx(a))* TXADJ)
                         + (DTX*tx01(a)*tx0(a)) ;

 TF(f,a)    = ((tfb(f,a) + dabtf(f,a))* TFADJ)
                         + (DTF*tf01(f,a)) ;

 TYF(f)     = ((tyfb(f) + dabtyf(f))* TYFADJ)
                      + (DTYF*tyf01(f)*tyf0(f)) ;

 TYH(h)     = ((tyhb(h) + dabtyh(h))* TYHADJ * TYADJ)
                      + (DTYH*DTY*tyh01(h)*tyh0(h)) ;

 TYE(e)     = ((tyeb(e) + dabtye(e))* TYEADJ * TYADJ)
                        + (DTYE*DTY*tye01(e)*tye0(e)) ;
 THC(h,c)     =   ((thcb(h,c) + dabthc(h,c)) * THCADJ)
                                      + (DTHC * thc01(h,c)) ;;

 MTAX       = SUM((w,c),TM(w,c)*PWM(c)*ER(w)*QMR(w,c)) ;

 ETAX       = SUM((w,c),TE(c,w)*PWE(c)*ER(w)*QER(c,w)) ;

 STAX       = SUM(c,TS(c)*PQS(c)*QQ(c)) ;

 VTAX       = SUM((c,h),TV(c)*PQD(c)*QCD(c,h))+SUM((cag,c,h),TV(c)*PQD(c)*QCD2(cag,c,h)) ;

 ITAX       = SUM(a,TX(a)*PX(a)*QX(a)) ;

 FTAX       = SUM((f,a), TF(f,a)*WF(f)*WFDIST(f,a)*FD(f,a)) ;

 FYTAX      = SUM(f,TYF(f)*(YF(f) * (1- deprec(f)))) ;

 DTAX       = SUM(h,TYH(h)*YH(h))
                 + SUM(e,TYE(e)*YE(e)) ;

 HCTAX      =  SUM((c,h),THC(h,c)*PQD(c)*QCD(c,h))
                              + SUM((cag,c,h),THC(h,c)*PQD(c)*QCD2(cag,c,h));
*- ## Government Income
 YGADJ       = YGADJ0;

 YG         = (MTAX + STAX + VTAX + ITAX
                + ETAX
                + FYTAX + DTAX + FTAX
                + SUM(f,govvash(f)*YFDISP(f))
                + SUM(e,GOVENT0(e)) + SUM(w,govwor(w)*ER(w)))*YGADJ
;

*- #### Government Expenditure Block

 QGDADJ     = QGDADJ0 ;
 QGDADJc(c) = 0;
 HEADJ      = HEADJ0 ;
 EGADJ      = EGADJ0 ;

 QGD(c)     = QGDADJ*qgdconst(c) ;

 VGD       = SUM(c,QGD(c)*PQD(c)) ;


 EG         = SUM(c,QGD(c)*PQD(c))
                 + SUM(h,HOGOV(h))
                 + SUM(e,EGADJ*entgovconst(e)*CPI) ;

 KAPGOV     = KAPGOV0 ;
*- ------- KAPITAL BLOCK --------------------------------------------------

*- ## Savings Block

 SADJ       = SADJ0 ;
 SHADJ      = SHADJ0 ;
 SEADJ      = SEADJ0 ;

 DSHH       = DSHH0 ;
 DS         = DS0 ;
 DSEN       = DSEN0 ;

 SHH(h)     = ((shh0(h) + dabshh(h)) * SHADJ * SADJ)
                   + (DSHH * DS * shh01(h)) ;

 SEN(e)     = ((sen0(e) + dabsen(e)) * SEADJ * SADJ)
                   + (DSEN * DS * sen01(e)) ;

 TOTSAV     = SUM(f,(deprec(f)*YF(f)))
                 + SUM(h,(YH(h) * (1 - TYH(h))) * SHH(h))
                 + SUM(e,(YE(e) * (1 - TYE(e))) * SEN(e))
                 + KAPGOV
                 + SUM(w,KAPREG0(w)*ER(w)) ;

*- ## Investment Block

 IADJ        = IADJ0  ;
 IADJTy(i)   = IADJTy0(i) ;

 QINV(i)     = qinvb(i) * IADJ0*IADJTy0(i) ;


*- INVEST     = TOTSAV ;

 QINVD(c,i) = (QINV(i)*ioqinvd(c,i)) ;

 INVSH_I(i) = INVSH_I0(i) ;

 INVEST      = SUM((c,i),PQD(c)*QINVD(c,i))  ;

 GBUDG     = VGD + SUM((iGov,c),PQD(c)*QINVD(c,iGov));

*- ------- FOREIGN INSTITUTIONS BLOCK -------------------------------------

 YFWOR(w,f)   = worvash(w,f)*YFDISP(f) ;

*- ------- MARKET CLEARING BLOCK ------------------------------------------

*- ##### Account Closure

 KAPGOV     = KAPGOV0 ;

 KAPREG(w)     = SUM(cm,PWM(cm)*QMR(w,cm))
                + (SUM(f,YFWOR(w,f))/ER(w))
                  - SUM(ce,PWE(ce)*QER(ce,w))
                  - SUM(h,howor(h,w))
                  - SUM(e,entwor(e,w))
                  - govwor(w)
                  - SUM(f,factwor(f,w))   ;

 KAPWOR    = SUM(w,KAPREG(w)) ;
*- #### Absorption Closure

 VFDOMD     =  SUM((ccesn1,h),PQD(ccesn1) * (1+THC(h,ccesn1))*(1+TV(ccesn1)) * QCD(ccesn1,h))
                             + SUM((cag,cces,h),PQD(cces)* (1+THC(h,cces)) * (1+TV(cces)) * QCD2(cag,cces,h))
                             + SUM(c,PQD(c)*QGD(c))
                             + SUM((c,e),PQD(c)*QED(c,e))
                             + SUM((c,i),PQD(c)*QINVD(c,i));

 INVESTSH   = INVEST/VFDOMD ;

 VGDSH      = VGD/VFDOMD ;

 VEDSH(e)   = VED(e)/VFDOMD ;

*-dynamic variables

 EXTENS(ff,a) =  SUM(c$map_ff_qgd(ff,c),QGD0(c)*EXTENSSHR0(ff,a));
 EXTENSSHR(ff,a)$SUM(ffp,FD0(ffp,a)*WFA0(ffp,a) and sum(c,map_ff_qgd(ff,c))) = FD0(ff,a)*WFA0(ff,a)/SUM(ffp$SUM(c,map_ff_qgd(ffP,c)),FD0(ffp,a)*WFA0(ffp,a));
 ADFExt(ff,a) = ADFExt0(ff,a);
 
*- ##### GDP

 GDP     = SUM((clein,h)$ccesn(clein),PQD0(clein) * (1+TV0(clein)) * QCD0(clein,h))
              + SUM((cag,clein,h)$cces(clein) ,PQD0(clein) * (1+TV0(clein))* QCD20(cag,clein,h))
                             + SUM(c,PQD0(c)*QGD0(c))
                             + SUM((c,i), PQD0(c)*QINVD0(c,i))
*-                            + SUM(c,PQD(c)*dstocconst(c))
                             + SUM(c, PE0(c)*QE0(c))
                               - SUM(c, PM0(c)*QM0(c)) ;
 RGDP    = GDP ;

 RGDPFC  = SUM((alein,f),WFA0(f,alein)*(1 + TF0(f,alein))*FD0(f,alein)) + SUM(clein,TS0(clein)*PQS0(clein)*QQ0(clein)) + SUM(alein,TX0(alein)*PX0(alein)*QX0(alein)) + SUM((clein,h),TV0(clein)*PQD0(clein)*QCD0(clein,h))  ;

*-Nutrition


*-##### Emissions

 CO2EM_Q(c,a)           = CO2EM_Q0(c,a)         ;
 CO2EM_H(c,h)           = CO2EM_H0(c,h)         ;
 CO2EMIS_Q(a)           = CO2EMIS_Q0(a)         ;
 CO2EMIS_H(h)           = CO2EMIS_H0(h)         ;
 CO2EMIS                = CO2EMIS0              ;
 NCO2EM_Q(nco,a)        = NCO2EM_Q0(nco,a)      ;
 
 NCO2EM_FS(nco,c,a)     = NCO2EM_FS0(nco,c,a)   ;
 NCO2EM_IO(nco,c,a)     = NCO2EM_IO0(nco,c,a)   ;
 NCO2EM_EN(nco,f,a)     = NCO2EM_EN0(nco,f,a)   ;
 NCO2EM_H(nco,c,h)      = NCO2EM_H0(nco,c,h)    ;

 NCO2EM_FS_SUM(nco,a)   = NCO2EM_FS_SUM0(nco,a) ;
 NCO2EM_IO_SUM(nco,a)   = NCO2EM_IO_SUM0(nco,a) ;
 NCO2EM_EN_SUM(nco,a)   = NCO2EM_EN_SUM0(nco,a) ;
 NCO2EM_H_SUM(nco,h)    = NCO2EM_H_SUM0(nco,h)  ;

 NCO2EM_A_SUM(NCO,a)    = NCO2EM_A_SUM0(NCO,a)  ;
 NCO2EM_SUM(nco)        = NCO2EM_SUM0(nco)      ;
 GHGEM                  = GHGEM0                ;

*- ##### Slack

 WALRAS     = TOTSAV - INVEST ;

 OBJ = WALRAS*WALRAS;

*- Agricultural budget

 AgBuRecurr(cGovAgr)           = AgBuRecurr0(cGovAgr)      ;
 AgBuInvest(iGovAgr)           = AgBuInvest0(iGovAgr)      ;
 AgBuInpSub(fGovAgr,aGovAgr)   = AgBuInpSub0(fGovAgr,aGovAgr) ;
 AgBuRevFund(ff,a)             = AgBuRevFund0(ff,a) ;
 AgBuOutSub(aGovAgr)           = AgBuOutSub0(aGovAgr)         ;
 AgBuComSub(cc,h)              = AgBuComSub0(cc,h);
 AgBuIncSub(h)                 = AgBuIncSub0(h);

 AgBuTotRecurr = AgBuTotRecurr0;
 AgBuTotInvest = AgBuTotInvest0;
 AgBuTotInpSub = AgBuTotInpSub0;
 AgBuTotOutSub = AgBuTotOutSub0;
 AgBuTotComSub = AgBuTotComSub0;
 AgBuTotIncSub = AgBuTotIncSub0;
 AgBuTOTALx    = AgBuTOTALx0;
 AgBuTOTALx    = AgBuTOTALx0;
 AgBuTOTShr    = AgBuTOTShr0;

 NutVal(nutElem,h) = NutVal0(nutElem,h);

*- gov't consumption adjusters
 QGDADJceh=1;
 QGDADJoth=1;
 QGDADJext=1;


$offDotL


*------------------end of DEMETRA variable initialisation --------------------
