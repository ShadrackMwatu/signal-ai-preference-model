$ontext
--------------------------------------------------------------------------------
 JRC.DEMETRA  version 1.0-alpha
 Dynamic Equilibrium Model for Economic developmenT, Environement & Agriculture

 GAMS file : parmcalib_assign.inc
 @purpose  : Assign calibrated parameter values
 @author   :
 @date     :
 @since    :
 @refDoc   :
 @seeAlso  :
 @calledBy :
--------------------------------------------------------------------------------
$offtext

*---------- NORMALISED PRICE BLOCK -----------------------------------------

*---  #### Assignments
 ER0(w) = 1;
 PD0(c)$cd(c)      = 1 ;
 PE0(c)            = 0 ;
 PE0(c)$ce(c)      = 1 ;
 PER0(c,w)$ceR(c,w)      = 1 ;
 PXC0(c)$cx(c)     = 1 ;

*---------- TRADE AND TRANSPORT TRANSACTIONS -------------------------------

*---  ## Commodity quantities
 totsupp(c)         = SUM(a,SAM(a,c)) + SUM(w,SAM(w,c)+ SUM(gt$map_mtax_w(gt,w),SAM(gt,c)));
 totdemd(c)         = SUM(sacn,SAM(sacn,c)) ;
 TTTRANS(md,c,"NaN","domes")  = SAM(md,c) ;


*---------- TRADE BLOCK ----------------------------------------------------

*---  #### Exports Block

*- currently assuming that trade margin in export commodity is distributed according to export value
TTTRANS(mw,c,w,"expo")$SUM(cp,SAM(cp,w)) = SAM(mw,c);
*---  #### Assignments

*---  ## Initial values for variables

 ZETAE0(c)   = 1 ;
 ZETAER0(c,w)= 1 ;

 QER0(c,w)$ceR(c,w)      = (SAM(c,w) - SUM(gt$map_etax_w(gt,w),SAM(gt,c))
                             - SUM(mw,TTTRANS(mw,c,w,"expo")))/PER0(c,w)/ZETAER0(c,w) ;
 QE0(c) = SUM(w,QER0(c,w)) ;

*---  QD0(c) = QXC0(c) - QE0(c) ;
 QD0(c)$cd(c)      = (SUM(a,SAM(a,c))/PXC0(c)) - QE0(c) ;

 PWE0(c)$QE0(c)
              = SUM(w,SAM(c,w)/ER0(w))/QE0(c) ;

 ERX0 = SUM(w,SUM(c,PER0(c,w)*QER0(c,w))/SUM((cp,wp),PER0(cp,wp)*QER0(cp,wp))*ER0(w));


*---  ## Parameters for CET functions 1st level nest
 rhotR(c)$(cd(c) AND ce(c))    = (1/(2*ELASTC(c,"omega"))) - 1 ;
 gammaR(c,w)$(ceR(c,w))
                = (PER0(c,w)*(ZETAER0(c,w)*QER0(c,w))**(1+rhotR(c)) ) /
                SUM(wp$cer(c,wp), PER0(c,wp)*(ZETAER0(c,w)*QER0(c,wp))**(1+rhotR(c)));


 atR(c)$(cd(c) AND ce(c))
                          = QE0(c)/SUM(w$gammar(c,w), gammar(c,w)*(ZETAER0(c,w)*QER0(c,w))**(-rhotR(c)) )**(-1/(rhotR(c))) ;

*---  ## Parameters for CET functions 2nd level nest
 rhot(c)$(cd(c) AND ce(c))    = (1/ELASTC(c,"omega")) + 1 ;
 gamma(c)$(cd(c) AND ce(c))
              = 1/(1+PD0(c)/PE0(c)*(QE0(c)/QD0(c))**(rhot(c)-1));

*---  Using {QXC0(c) = (SUM(a,SAM(a,c))/PXC0(c))} in statement for at(c)
 at(c)$(cd(c) AND ce(c))
              = (SUM(a,SAM(a,c))/PXC0(c))
                 /(gamma(c)*QE0(c)**rhot(c) + (1-gamma(c))*
                       QD0(c)**rhot(c))**(1/rhot(c));

*---  ## Parameters for Export Demand functions
 econ(c,w)         = QER0(c,w) ;
 eta(c,w)          = ELASTEXDEM(c,w) ;
 pwse(c,w)$QER0(c,w)  = PER0(c,w)/ER0(w) ;

*---  #### Imports Block
*--- First level Armington Nest
 PWM0(c)$SUM(w,SAM(w,c)) = 1;
 TM0(w,c)$cmR(w,c) =  SUM(gt$map_mtax_w(gt,w),SAM(gt,c))/SAM(w,c) ;
 PMR0(w,c) = (PWM0(c) * (1 + TM0(w,c))) * ER0(w);

 ZETAM0(w,c)=1 ;
 QMR0(w,c)$cmR(w,c)      = (SAM(w,c) + SUM(gt$map_mtax_w(gt,w),SAM(gt,c)))/PMR0(w,c)/ZETAM0(w,c)  ;

*-total imports is sum of imports from trading partners
 QM0(c)$cm(c)      =  SUM(w,QMR0(w,c));        ;

 PM0(c)$QM0(c) = SUM(w,PMR0(w,c)*QMR0(w,c))/QM0(c) ;

 rhocR(c)$cm(c)    = (1/(2*ELASTC(c,"sigmaR"))) - 1;

 deltaR(w,c)$SUM(wp, PMR0(wp,c)*(ZETAM0(w,c)*QMR0(wp,c))**(1+rhocR(c)))
            =    (PMR0(w,c)*(ZETAM0(w,c)*QMR0(w,c))**(1+rhocR(c)))
                  / SUM(wp$cmR(wp,c), PMR0(wp,c)*(ZETAM0(w,c)*QMR0(wp,c))**(1+rhocR(c)));


 acR(c)$(cm(c)) = QM0(c)/SUM(w$deltaR(w,c), deltaR(w,c)*(ZETAM0(w,c)*QMR0(w,c))**(-rhocR(c)))**(-1/rhocR(c));

*--- Second level Armington Nest

 QQ0(c)      = QD0(c) + QM0(c) ;

 PQS0(c)$QQ0(c)=(PD0(c)*QD0(c)+PM0(c)*QM0(c))/QQ0(c);


*---  ## Parameters for Armington/CES functions
 rhoc(c)$(cx(c) AND cm(c))    = (1/ELASTC(c,"sigma")) - 1 ;
 delta(c)$(cd(c) AND cm(c))
               = (PM0(c)*QM0(c)**(rhoc(c)+1))
                  /(PM0(c)*QM0(c)**(rhoc(c)+1) + PD0(c)*QD0(c)**(rhoc(c)+1)) ;
 ac(c)$(cd(c) AND cm(c))
               = QQ0(c)/(delta(c)*QM0(c)**(-rhoc(c))
                         +(1-delta(c))*QD0(c)**(-rhoc(c)))**(-1/rhoc(c)) ;

*---------- TRADE AND TRANSPORT MARGINS BLOCK ------------------------------

*---  #### Assignments

*---  ## Initial values for variables

*---  NB: PQD0 not yet defined so using PQD02(c)
 PQD02(c)  = 1.0 ;
 PQD02(c)$QQ0(c)
             = (SAM(c,total) - SUM(w,SAM(c,w)) - SAM(vattax,c))
                /QQ0(c);
* controlling for pqd since there can be commodities that are completely exported
 QTT0(m)$SUM(c,SAM(c,m))
         = SUM(c$PQD02(c),SAM(c,m)/PQD02(c)) ;

 PTT0(m)$(QTT0(m))
         = SUM(c$PQD02(c),(SAM(c,m)/PQD02(c)/QTT0(m)) * PQD02(c)) ;
 QTTD0(c)$(QQ0(c))
         = SUM(m,SAM(c,m)/((SAM(c,total) - SUM(w,SAM(c,w))  - SAM(vattax,c))
                          /QQ0(c))) ;

*---  ## input output coefficients
 IOQTTQQ0(md,c)$TTTRANS(md,c,"Nan","domes")
         = (TTTRANS(md,c,"Nan","domes")/PTT0(md))/QQ0(c) ;

 ioqttqe(mw,c,w)$TTTRANS(mw,c,w,"expo")
         = (TTTRANS(mw,c,w,"expo")/PTT0(mw))/QER0(c,w) ;
 ioqtdqtt(c,m)$SAM(c,m)
         = (SAM(c,m)/((SAM(c,total) - SUM(w,SAM(c,w))  - SAM(vattax,c))
                     /QQ0(c)))/QTT0(m) ;
 etatr=0.19;

*---------- COMMODITY PRICE BLOCK ------------------------------------------

*---  #### Assignments

*---  ## Initial values for variables
 PQD0(c)$QQ0(c)         = (SAM(c,total) - SUM(w,SAM(c,w)) - SAM(vattax,c))
                             /QQ0(c) ;

 pqd2dist(cc,cc,h)      = 1.0 ;

*---------- NUMERAIRE PRICE BLOCK ------------------------------------------

*---  #### Assignments
 tv02(c)$(SUM(h,SAM(c,h)) - SAM(vattax,c))
             = SAM(vattax,c)/(SUM(h,SAM(c,h)) - SAM(vattax,c)) ;

*---  VAT rates on aggregate commodities are by definiton ZERO
 tv02(cag)  = 0.0 ;



*---------- PRODUCTION BLOCK -----------------------------------------------

*---  #### Assignments
* Calibrate FACTUSE for intermediate with the right price
 FACTUSE(ff,a)$(sum(c$map_c_f_a(c,ff,a),1)) =
                         sum(c$(PQD0(c) AND map_c_f_a(c,ff,a)),SAM(c,a)/PQD0(c));
 FD0(ff,a)     = FACTUSE(ff,a) ;

 FDTOT0(f)  = SUM(a, FACTUSE(f,a)) ;
 FS0(f)         = FDTOT0(f)/(1-UNEMPRATE0(f));
 FSI0_bsh(ins,f)$(SUM(insp, SAM(insp,f)))
            = SAM(ins,f)/SUM(insp, SAM(insp,f)) ;

 UNEMP0(ff) =  FS0(ff)*unempRate0(ff);

*- Redefine factinsw using base shares to distribute total demand for factors
 factins(ins,f)     = FSI0_bsh(ins,f)*FS0(f) ;

*- check if factuse and factins are consistent

 factuse_chk(f) =  SUM(ins,factins(ins,f)) -  SUM(a,factuse(f,a)) - UNEMP0(f);

 FSI0(ins,f)  = factins(ins,f) ;

 FSIL0(ins,f)   = SUM(alei$map_hh_alei(ins,alei),FD0(f,alei)) ;
 FSL0(f)        = SUM(ins,SUM(alei$map_hh_alei(ins,alei),FD0(f,alei))) ;
 FSM0(f)        = SUM(alein,FD0(f,alein)) ;
 FSIM0(f,ins,fp,insp)   = 0 ;
 WF0(f)$(FS0(f))              = SUM(a,SAM(f,a))/FS0(f) ;

*--- wage for Int inp in the VA equals to average price
*--- the control is for cases where a factor is declared as factor but not assigned to a commodity
 WF0(fc)$(not f(fc) AND SUM((c,a)$(map_c_f_a(c,fc,a)), 1)) =  SUM((c,a)$(map_c_f_a(c,fc,a)),PQD0(c))
                              /SUM((c,a)$(map_c_f_a(c,fc,a)), 1);

*-fix wage for commodities that are not used as intermediates

 WF0(fc)$(not f(fc)AND not SUM(a,FD0(fc,a))) = 0;

*---  assign values for the un-natural factors

 WFDIST0(fc,a)$FD0(fc,a) = ((SAM(fc,a)+SUM(c$map_c_f_a(c,fc,a),SAM(c,a)))
                                                         /FD0(fc,a))/WF0(fc) ;
 QINTD0(c,a)$(SAM(c,a) AND PQD0(c))    = SAM(c,a)/PQD0(c)  ;
 PQDDIST0(c,a)$(PQD0(c) AND QINTD0(c,a)) = (SAM(c,a)/QINTD0(c,a))/PQD0(c) ;


*--- WFDIST for fag is calibrated below, after tf02 is caluclated
 WFDIST0(fc,a)$(not FD0(fc,a)) = 0.0 ;
 WFA0(fc,a) = WF0(fc)*WFDIST0(fc,a);
 
 tf02(f,a)$SAM(f,a)     = ((SUM(tff$map_f_tff(f,tff),SAM(tff,a)))
                                 /SAM(f,a)) ;
 tf02(fag,a)$SUM(f$map_fag_ffall_a(fag,f,a),SAM(f,a))
                = SUM(f$map_fag_ffall_a(fag,f,a),(SUM(tff$map_f_tff(f,tff),SAM(tff,a))))
                   /(SUM(f$map_fag_ffall_a(fag,f,a),SAM(f,a))  + SUM(c$map_c_fag(fag,c,a),SAM(c,a)));

 WF0(fag)      = 1.0 ;
 FD0(fag,a)    = SUM(fc$(map_fag_ffall_a(fag,fc,a) AND (WFA0(fc,a)*(1+tf02(fc,a))) AND f(fc)), SAM(fc,a)
                                                                                        / (WFA0(fc,a)*(1+tf02(fc,a)))) +
                 SUM(fc$map_fag_ffall_a(fag,fc,a), SUM(c$(map_c_f_a(c,fc,a) AND PQD0(c)),SAM(c,a)/PQD0(c)))  ;                         
                                                                                        


 FD0("ftop",a) = SUM(f$map_fag_ffall_a("ftop",f,a) , SAM(f,a)) + SUM(fc$map_fag_ffall_a("ftop",fc,a), SUM(c$map_c_f_a(c,fc,a),SAM(c,a)))  ;
 WFDIST0(fag,a)$(FD0(fag,a)) = SUM(fc$map_fag_ffall_a(fag,fc,a),SUM(c$map_c_f_a(c,fc,a),SAM(c,a)) + SAM(fc,a))  /FD0(fag,a)  ;
 WFA0(fag,a) = WF0(fag)*WFDIST0(fag,a);

 FS0(ff)$(NOT FS0(ff)) = SUM(a, FD0(ff,a));

 FSI0(ins,f)$SUM(insp,FSI0(insp,f)) = FS0(f)*FSI0(ins,f)/SUM(insp,FSI0(insp,f)) ;

 fsia(ins,f)     = FSI0(ins,f) ;

*---  Rates of return on factors
 ror_f(f)$WF0(f)      = 1.0/[FS0(f)/WF0(f)] ;


*---  ## Initial values for variables
  QXC0(c)$PXC0(c)     = SUM(a,SAM(a,c))/PXC0(c) ;
  QINT0(a)= SUM(fc$map_fag_ffall_a("ftop",fc,a), SUM(c$(map_c_f_a(c,fc,a) AND PQD0(c)),SAM(c,a)/PQD0(c)));
  QVA0(a) =SUM(fc$(map_fag_ffall_a("ftop",fc,a) AND (WFA0(fc,a)*(1+tf02(fc,a))) AND f(fc)), SAM(fc,a)
                                                                                        / (WFA0(fc,a)*(1+tf02(fc,a))));
  QX0(a)  = FD0("ftop",a);
  
  PX0(a)  $ QX0(a)   = SAM(total,a)/QX0(a) ;
  PINT0(a)$ QINT0(a) = (SUM(c,(SAM(c,a))))/QINT0(a);
  PVA0(a) $ QVA0(a)  = (SUM(f,SAM(f,a)) + SUM(tff,SAM(tff,a)))/QVA0(a) ;

  VVA0(a)     = SUM(f,SAM(f,a));
  TX0(a)$SAM("total",a)  = (SAM("indtax",a))/SAM("total",a) ;


 ioqxacqx(a,c)$SUM(cp,SAM(a,cp))  = SAM(a,c)/SUM(cp,SAM(a,cp)) ;
 QXAC0(a,c) =  QX0(a)*ioqxacqx(a,c) ;
 PXAC0(a,c)$QXAC0(a,c)= SAM(a,c)/QXAC0(a,c);

*---  Technology Parameters and Adjustment factors
 ADFD0(ff,a)     = 1 ;
 ADFDA(ff,a)     = 1 ;
 ADFH0(ff,h)     = 0 ;
 ADFHA(ff,h)     = 0 ;

*-calculate # of HHs that own factor ff from data
 numHH(ff)=SUM(h$FSI0(h,ff),1);
 numHH(ff)$(NOT numHH(ff))= 1;

 AD0(ff,a) = (1+SUM(h$FSI0(h,ff),ADFH0(ff,h))/numHH(ff))*ADFD0(ff,a) ;

*---  CES aggregation functions for Level 2 of production nest

*---  CES aggregation functions
 rhofd(fag,a)$ELASTFD(fag,a)   = (1/ELASTFD(fag,a)) - 1 ;

 deltafd(fag,ff,a)$(map_fag_ff_a(fag,ff,a) AND SUM((ffp)$ (map_fag_ff_a(fag,ffp,a) ),WFDIST0(ffp,a)*WF0(ffp)))
             = (WFDIST0(ff,a)*WF0(ff)*(1+tf02(ff,a))*(ADFD0(ff,a)*FD0(ff,a))
                        **(1+rhofd(fag,a)))
     / SUM((ffp)$ (map_fag_ff_a(fag,ffp,a)),WFDIST0(ffp,a)*WF0(ffp)*(1+tf02(ffp,a))
                 *(ADFD0(ffp,a)*FD0(ffp,a))**(1+rhofd(fag,a))) ;

 iofdfag(fag,ff,a)$(map_fag_ff_a(fag,ff,a) AND SUM((ffp)$ (map_fag_ff_a(fag,ffp,a)),FD0(ffp,a)))
             = FD0(ff,a)
     / SUM((ffp)$ (map_fag_ff_a(fag,ffp,a)),(FD0(ffp,a))) ;

*--- efficiency varaiable for aggr at all levels of production nest
 adfag0(fag,a)$FD0(fag,a) = FD0(fag,a)
                        /(SUM(ff$(FD0(ff,a)) ,deltafd(fag,ff,a)*FD0(ff,a)
                         **(-rhofd(fag,a))))**(-1/rhofd(fag,a)) ;
 adfagb(ff,a)       =  ADFAG0(ff,a)  ;
 dadfag(ff,a)       =  0             ;
 ADFAGfADJ0(ff)     =  1             ;
 ADFAGaADJ0(a)      =  1             ;
 ADFAGADJ0          =  1             ;

*---  Intermediate Input Demand
 ioqtdqd(c,a)$(QINT0(a) AND PQD0(c))
            = (SAM(c,a)- SUM(ff$map_c_f_a(c,ff,a),SAM(c,a))) /PQD0(c)/QINT0(a) ;

*---  Commodity Output
 rhocxc(c) $ELASTC(c,"sigmaxc")  = (1/ELASTC(c,"sigmaxc")) - 1 ;
 deltaxc(a,c)$SAM(a,c)
               = (PXAC0(a,c)*QXAC0(a,c)**(1+rhocxc(c)))
                 /SUM(ap,PXAC0(ap,c)*QXAC0(ap,c)**(1+rhocxc(c))) ;
 adxc(c)$(QXC0(c) AND rhocxc(c))
               = QXC0(c)/(SUM(a,deltaxc(a,c)*QXAC0(a,c)
                    **(-rhocxc(c)))**(-1/rhocxc(c)));


*---  Activity Output

*---  parameter is defined in the data_load.inc file because it is used for set controls
 IOQXACQXV0(a,c)$SUM(cp,QXAC0(a,cp)) =  QXAC0(a,c)/SUM(cp,QXAC0(a,cp)) ;

*---  CET output function parameter
 rhoti(a)$(acet(a) AND ELASTX(a,"omegaout"))     = (1/ELASTX(a,"omegaout")) + 1 ;
 gammai(a,c)$(QXAC0(a,c)and acet(a))
                        = (PXAC0(a,c)*QXAC0(a,c)**(1-rhoti(a)) ) /
                             SUM(cp$QXAC0(a,cp), PXAC0(a,cp)*QXAC0(a,cp)
                                **(1-rhoti(a)) );
 ati(a)$(acet(a))     =  QX0(a)/SUM(c, gammai(a,c)*QXAC0(a,c)
                           **(rhoti(a)) )**(1/(rhoti(a))) ;
 cti(a,c) = 1;

*---------- FACTOR BLOCK ---------------------------------------------------

*---  #### Assignments

*---  ## Initial values for variables
 YF0(f)      = SAM(total,f) ;
 YFDISP0(f)  = (SAM(total,f) - SAM(is,f) - SAM(facttax,f)) ;
 YFINS0(f)   = YFDISP0(f) - SAM(govert,f) - SUM(w,SAM(w,f)) ;
 FSISH0(ins,f)$SUM(insp,FSI0(insp,f))
             = FSI0(ins,f)/SUM(insp,FSI0(insp,f)) ;


*---  ## Savings Expenditures
 deprec(f)$(SAM(total,f))
               = SAM(is,f)/SAM(total,f) ;

*---  ## Transfer Expenditures

*---   make insva0 consistent with initialization

 INSVA0(ins,f)    = FSISH0(ins,f) * YFINS0(f) ;

 hovash(h,f)      = FSISH0(h,f) ;
 entvash(e,f)     = FSISH0(e,f) ;
 govvash(f)$YFDISP0(f)  = SAM(govert,f)/YFDISP0(f) ;
 worvash(w,f)$YFDISP0(f)  = SAM(w,f)/YFDISP0(f) ;



*---------- HOUSEHOLD BLOCK ------------------------------------------------

*---  #### Assignments

*---  ## Initial values for variables
 YH0(h)          = SAM(total,h) ;
 HOHO0(h,hp)     = SAM(h,hp) ;
 HEXP0(h)        = SUM(c,SAM(c,h)) ;
 QCD0(ccesn,h)$SAM(ccesn,h) = SAM(ccesn,h)/(PQD0(ccesn) * (1+tv02(ccesn))) ;

*---  Assign values for the aggregate commodities - tv02(c) = 0.0 but kept
 QCD20(cag,cces,h)$(PQD0(cces) AND map_cag_c(cag,cces))  = SAM(cces,h)/(PQD0(cces) * (1+tv02(cces)))  ;

 QCD0(cag,h)= SUM(cces,QCD20(cag,cces,h)) ;

 PQCD0(cag,h)$(qcag(cag,h) AND QCD0(cag,h)) =SUM(c$map_cag_c(cag,c),SAM(c,h)) /QCD0(cag,h) ;

 PQC0(cc,h)$(ccesn(cc) OR cag(cc)) = (PQD0(cc)*(1+TV02(cc)))+PQCD0(cc,h);

 VQCD0(c)  = SUM(h,(PQD0(c)*(1+TV02(c))*QCD0(c,h)$ccesn(c))
                           + SUM(cag,PQD0(c)*(1+TV02(c))*QCD20(cag,c,h)$cces(c)));


*---  ## Price index weights

*---  note that the CPI weights are based on household expenditure shares ONLY

*---  CPI weights based on household final demand expenditure shares
 COMTOTSH0(c)$SUM(cp,VQCD0(cp)) = VQCD0(c)/SUM(cp,VQCD0(cp));

 comthhsh(c,h)$(SUM(cp,SAM(cp,h))) = SAM(c,h)/SUM(cp,SAM(cp,h)) ;

*---  alternate 2 - CPI weights based on total final demand expenditure shares
$ontext
 comtotsh(c)   = (SUM(h,SAM(c,h)) + SAM(c,govert) + SAM(c,"kap"))
                 /(SUM((cp,hp),SAM(cp,hp))
                  + SUM(cp,SAM(cp,govert))
                  + SUM(cp,SAM(cp,"kap")))  ;
$offtext

*---  PPI weights are based on the value of domestic output for the domestic market
 vddtotsh0(c)$(SUM((ap,cp),SAM(ap,cp)))
               = SUM(a,SAM(a,c))/SUM((ap,cp),SAM(ap,cp)) ;

*---  ## Initial values for variables

 PPI0         = SUM(c,(SUM(a,SAM(a,c))/SUM((ap,cp),SAM(ap,cp)))*PD0(c)) ;
 CPI0         = SUM(c,comtotsh0(c) * (PQD0(c)*(1+tv02(c))) ) ;

*---  ## Transfer Expenditures
 hohosh(h,hp)$(SAM(total,h) - SAM(dirtax,h) - SAM(is,h))
             = SAM(h,hp)/(SAM(total,h) - SAM(dirtax,h) - SAM(is,h)) ;

 hohoconst(h,hp) = SAM(h,hp) ;

 hohosh_mig(f,h,hp)=0.0;

*---  ## Consumption Expenditures

*---  # Cobb Douglas Utility function
 comhoav1(c,h)$SUM(cp,SAM(cp,h))
                 = SAM(c,h)/SUM(cp,SAM(cp,h)) ;
 alphah1(c,h)$SUM(cp,SAM(cp,h))
                 = SAM(c,h)/(SUM(cp,SAM(cp,h))) ;
 comhoav(cag,h)$SUM(cp,SAM(cp,h))    = SUM(c$map_cag_c(cag,c),SAM(c,h))/SUM(cp,SAM(cp,h)) ;
 comhoav(ccesn,h)$SUM(cp,SAM(cp,h))  = SAM(ccesn,h)/SUM(cp,SAM(cp,h)) ;
 alphah(cc,h)$(cles(cc)) = comhoav(cc,h) ;
 elasttest(cles,h)  = elasty(cles,h) ;
$ontext
# Stone-Geary Utility function
  Weighted sum of the expenditures elasticities must equal one.
  Weights are average budget shares. Normalised elasticities will satisfy
  Engel aggregation
$offtext
 sumelast(h)   = SUM(cles, alphah(cles,h)*ELASTY(cles,h)) ;
 yhelast(cc,h)$(sumelast(h) AND cles(cc))
               = ELASTY(cc,h)/sumelast(h) ;
 yhelast(cc,h)$((alphah(cc,h) eq 0) AND cles(cc))  = 0 ;

 beta(cc,h)$(cles(cc))     = yhelast(cc,h)*alphah(cc,h) ;

 frisch(h)     = ELASTMU(h,"frisc") ;
 qcdconst(ccesn,h)$(PQD0(ccesn) AND frisch(h) AND beta(ccesn,h))
               = (HEXP0(h)/(PQD0(ccesn)*(1+tv02(ccesn))) )
                    *(alphah(ccesn,h)+(beta(ccesn,h)/frisch(h))) ;
 qcdconst(cag,h)$(PQCD0(cag,h) AND frisch(h) AND beta(cag,h))
               = (HEXP0(h)/(PQCD0(cag,h)) )
                    *(alphah(cag,h)+(beta(cag,h)/frisch(h))) ;
 hexps(h)      = SUM(cc$cles(cc),qcdconst(cc,h) * PQD0(cc)*(1+tv02(cc))) ;


*---  # CES Utility function
 rhocd(cc,h)$(cag(cc) AND ELASTCES(cc,h))   = (1/ELASTCES(cc,h)) - 1 ;
 PQD20(cag,cces,h) = ((PQD0(cces)*(1+tv02(cces))) * pqd2dist(cag,cces,h)) ;
*-control for existence of consumption
 deltacd(cag,cces,h)$(rhocd(cag,h) AND SUM(ccesp$map_cag_c(cag,ccesp),
                     (((PQD0(ccesp)*(1+tv02(ccesp))) )
                               * QCD20(cag,ccesp,h)**(1+rhocd(cag,h)))))
              = (((PQD0(cces)*(1+tv02(cces))) )
                               * QCD20(cag,cces,h)**(1+rhocd(cag,h)))
                / SUM(ccesp$map_cag_c(cag,ccesp),
                     (((PQD0(ccesp)*(1+tv02(ccesp))) )
                               * QCD20(cag,ccesp,h)**(1+rhocd(cag,h))))  ;
 deltacd2(cc,cces,h)$(map_cag_c(cc,cces) and QCD0(cces,h) )
            = (PQD0(cces) * (1+tv02(cces)) * (QCD0(cces,h))
                    **(1+rhocd(cc,h)))
                     / SUM(ccp$map_cag_c(ccp,cces),PQD0(cces)
                      * (1+tv02(cces)) * (QCD0(cces,h))**(1+rhocd(ccp,h))) ;
 accd(cag,h)$(SUM(cces$map_cag_c(cag,cces), QCD20(cag,cces,h)) and SUM(cces$map_cag_c(cag,cces),deltacd(cag,cces,h)))
           = QCD0(cag,h)
             /(SUM(cces$(QCD20(cag,cces,h) NE 0 ),deltacd(cag,cces,h)*QCD20(cag,cces,h)
             **(-rhocd(cag,h))))**(-1/rhocd(cag,h)) ;


*---  in the base, the only factors are those factors to themselves, i.e. the

*---------- ENTERPRISE BLOCK -----------------------------------------------

*---  #### Assignments

*---  ## Initial values for scaling variables
 QEDADJ0 = 1 ;
 HEADJ0    = 1 ;

*---  ## Initial values for variables
 YE0(e)      = SAM(total,e) ;
 HOENT0(h,e) = SAM(h,e) ;
 GOVENT0(e)  = SAM(govert,e) ;
 GOVENTSH0(e)$(SAM(total,e) - SAM(dirtax,e) - SAM(is,e) - SUM(c,SAM(c,e)))
             = SAM(govert,e)/
                (SAM(total,e) - SAM(dirtax,e)
                       - SAM(is,e) - SUM(c,SAM(c,e))) ;
 QED0(c,e)$PQD0(c) = SAM(c,e)/PQD0(c) ;
 VED0(e)   = SUM(c,SAM(c,e)) ;

*---  ## Transfer Expenditures
 hoentconst(h,e) = SAM(h,e)/CPI0 ;
 hoentsh(h,e)$(SAM(total,e) - SAM(dirtax,e) - SAM(is,e) - SUM(c,SAM(c,e)))
                 = SAM(h,e)/
                    (SAM(total,e) - SAM(dirtax,e)
                       - SAM(is,e) - SUM(c,SAM(c,e))) ;
 goventsh(e)$(SAM(total,e) - SAM(dirtax,e) - SAM(is,e) - SUM(c,SAM(c,e)))
                 = SAM(govert,e)/
                      (SAM(total,e) - SAM(dirtax,e)
                        - SAM(is,e) - SUM(c,SAM(c,e))) ;





*---  ## Consumption Expenditures
 qedconst(c,e)$PQD0(c)   = SAM(c,e)/PQD0(c) ;

*---------- GOVERNMENT BLOCK -----------------------------------------------

*---  #### Government Taxes Block

*---  #### Assignments

*---  ## Initial values for scaling variables
 TEADJ0(w)     = 1.0 ;
 TMADJ0(w,c)   = 1.0 ;
 TYFADJ0       = 1.0 ;
 TSADJ0        = 1.0 ;
 TVADJ0        = 1.0 ;
 TXADJ0        = 1.0 ;
 TXAADJ0       = 1.0 ;
 TFADJ0        = 1.0 ;
 TYHADJ0       = 1.0 ;
 TYADJ0        = 1.0 ;
 TYEADJ0       = 1.0 ;
 THCADJ0       = 1.0 ;
*---  ## Initial values for partial scaling variables
 DTE0(w)       = 0.0 ;
 DTM0(w)       = 0.0 ;
 DTS0          = 0.0 ;
 DTV0          = 0.0 ;
 DTX0          = 0.0 ;
 DTF0          = 0.0 ;
 DTYF0         = 0.0 ;
 DTYH0         = 0.0 ;
 DTY0          = 0.0 ;
 DTYE0         = 0.0 ;
 DTHC0         = 0.0 ;
*---  ## Initial tax revenues
 MTAX0         = SUM((c,gt,w)$map_mtax_w(gt,w),SAM(gt,c)) ;
 STAX0         = SUM(c,SAM(saltax,c)) ;
 VTAX0         = SUM(c,SAM(vattax,c)) ;
 ETAX0         = SUM((c,w,gt)$map_etax_w(gt,w),SAM(gt,c)) ;
 ITAX0         = SUM(a,SAM(indtax,a)) ;
 FTAX0         = SUM((f,a),SUM(tff$map_f_tff(f,tff),SAM(tff,a))) ;
 FYTAX0        = SUM(f,SAM(facttax,f)) ;
 DTAX0         = SUM(h,SAM(dirtax,h)) + SUM(e,SAM(dirtax,e)) ;
 HCTAX0        = 0;

*---  ## initial tax rates
 TM0(w,c)$cmR(w,c) =  SUM(gt$map_mtax_w(gt,w),SAM(gt,c))/SAM(w,c) ;
 TE0(c,w)$ceR(c,w) = SUM(gt$map_etax_w(gt,w),SAM(gt,c))/SAM(c,w) ;
 dmd_PP(c)  = SUM(m,SAM(c,m)) + SUM(a,SAM(c,a)) + SUM(h,SAM(c,h))
              + SUM(e,SAM(c,e))+ SUM(g,SAM(c,g))
              + SUM(i,SAM(c,i)) ;
 dmd_BP(c)  = dmd_PP(c)
                 - (SUM(md,SAM(md,c)) + SAM(saltax,c)  + SAM(vattax,c)
                      + SAM(ectax,c) )   ;
 TS0(c)$dmd_BP(c)
              = SAM(saltax,c)/dmd_BP(c) ;
 TV0(c)$(SUM(h,SAM(c,h)) - SAM(vattax,c))
             = SAM(vattax,c)/(SUM(h,SAM(c,h)) - SAM(vattax,c)) ;
 TV0(cag)    = 0.0 ;
 TYF0(f)$(SAM(total,f) - SAM(is,f))
              = SAM(facttax,f)/(SAM(total,f) - SAM(is,f)) ;
 TX0(a)$SAM(total,a)
              = (SAM(indtax,a))/SAM(total,a) ;
 TF0(f,a)$SAM(f,a)
              = SUM(tff$map_f_tff(f,tff),SAM(tff,a))/SAM(f,a);
 THC0(h,c) = 0 ;

 TYH0(h)$SAM(total,h)
              = SAM(dirtax,h)/SAM(total,h) ;
 TYE0(e)$SAM(total,e)
              = SAM(dirtax,e)/SAM(total,e) ;

*---  ## base tax rates
 teb(c,w)     = TE0(c,w) ;
 tmb(w,c)     = TM0(w,c) ;
 tsb(c)       = TS0(c) ;
 tvb(cc)      = TV0(cc) ;
 tyfb(f)      = TYF0(f) ;
 txb(a)       = TX0(a) ;
 txab(a)      = 0 ;
 tfb(ff,a)    = TF0(ff,a) ;
 tyhb(h)      = TYH0(h) ;
 tyeb(e)      = TYE0(e) ;
 thcb(h,c)    = THC0(h,c) ;


*---  ## absolute changes in base tax rates
 dabte(c,w)   = 0.0 ;
 dabtm(w,c)   = 0.0 ;
 dabts(c)     = 0.0 ;
 dabtv(cc)    = 0.0 ;
 dabtx(a)     = 0.0 ;
 dabtxa(a)    = 0.0 ;
 dabtf(ff,a)  = 0.0 ;
 dabtyf(f)    = 0.0 ;
 dabtyh(h)    = 0.0 ;
 dabtye(e)    = 0.0 ;
 dabthc(h,c)  = 0.0 ;

*---  ## partial changes in tax rates
 te01(c,w)    = 0 ;
 tm01(w,c)    = 0 ;
 ts01(c)      = 0 ;
 tv01(cc)     = 0 ;
 tx01(a)      = 0 ;
 tf01(ff,a)   = 0 ;
 tyf01(f)     = 0 ;
 tyh01(h)     = 0 ;
 tye01(e)     = 0 ;

 vtax01       = 0 ;
 dvtax0       = 0 ;
 thc01(h,c)   = 0 ;
*---  #### Government Income and Expenditure Block

*---  #### Assignments

*---  ## Initial values for scaling variables
 QGDADJ0   = 1 ;
 EGADJ0    = 1 ;

*---  ## Initial values for variables
 YGADJ0 = 1;
 YG0         = SAM(total,govert) ;
 QGD0(c)$PQD0(c)     = SAM(c,govert)/PQD0(c) ;
 EG0         = SAM(total,govert) - SAM(is,govert) ;
 VGD0        = SUM(c,SAM(c,govert)) ;


*---  ## Transfer Expenditures
 HGADJ0    = 1 ;
 hogovb(h) =  SAM(h,govert)/CPI0;
 dabhogov(h) = 0 ;
 DHOGOV0     = 0 ;
 hogov01(h)  = 0;
 HOGOV0(h) = ((hogovb(h)+dabhogov(h))*HGADJ0
                 +DHOGOV0 * hogov01(h))*CPI0;
 entgovconst(e)  = SAM(e,govert)/CPI0 ;

*---  ## Consumption Expenditures
 qgdconst(c)$PQD0(c)     = SAM(c,govert)/PQD0(c) ;

*---------- KAPITAL BLOCK --------------------------------------------------

*---  #### Assignments

*---  ## Initial values for scaling variables
 SADJ0     = 1.0 ;
 SHADJ0    = 1.0 ;
 SEADJ0    = 1.0 ;
 IADJ0     = 1.0 ;
 IADJTy0(i)= 1.0 ;
 DSHH0     = 0.0 ;
 DS0       = 0.0 ;
 DSEN0     = 0.0 ;

*---  ## Initial values for variables
 QINV0(i)$SUM(c,SAM(c,i))
              = SUM(c$PQD0(c),SAM(c,i)/PQD0(c)) ;
 QINVD0(c,i)$PQD0(c)  = SAM(c,i)/PQD0(c) ;

 INVEST0      = SUM((c,i),PQD0(c)*QINVD0(c,i)) ;
 INVSH_I0(i)  = SUM(c,PQD0(c)*QINVD0(c,i)) / INVEST0 ;

 TOTSAV0      = SAM(is,total)  ;

 GBUDG0      = VGD0 + SUM((iGov,c),PQD0(c)*QINVD0(c,iGov)) ;

*---  ## initial savings rates
 shh0(h)$(SAM(total,h) - SAM(dirtax,h))
              = SAM(is,h)/(SAM(total,h) - SAM(dirtax,h)) ;
 sen0(e)$(YE0(e) - SAM(dirtax,e))
              = SAM(is,e)/(YE0(e) - SAM(dirtax,e)) ;

*---  ## base savings rates
 shhb(h)      = shh0(h) ;
 senb(e)      = sen0(e) ;

*---  ## absolute changes in base savings rates
 dabshh(h)    = 0.0 ;
 dabsen(e)    = 0.0 ;

*---  ## partial changes in savings rates
 shh01(h)     = 0.0 ;
 sen01(e)     = 0.0 ;

*---  ## Consumption Expenditures
 invconst(c,i)$PQD0(c)   = SAM(c,i)/PQD0(c) ;
 ioqinvd(c,i)$(QINV0(i) AND PQD0(c))
                = SAM(c,i)/PQD0(c)/QINV0(i) ;

 qinvb(i)       = QINV0(i) ;

*---------- FOREIGN INSTITUTIONS BLOCK -------------------------------------

*---  #### Assignments

*---  ## Initial values for variables
 YFWOR0(w,f)    = SAM(w,f) ;

*---  ## Transfer Expenditures
 factwor(f,w)   = SAM(f,w)/ER0(w) ;
 howor0(h,w)       = SAM(h,w)/ER0(w) ;
 entwor(e,w)       = SAM(e,w)/ER0(w) ;
 govwor(w)          = SAM(govert,w)/ER0(w) ;

*---------- MARKET CLEARING BLOCK ------------------------------------------

*---  #### Assignments

*---  ## Initial values for variables

*---  # Account Closure
 KAPGOV0     = SAM(is,govert) ;
 KAPREG0(w)  = SAM(is,w)/ER0(w) ;
 KAPWOR0 = SUM(w,KAPREG0(w));

*---  # Absorption Closure
 VFDOMD0     = SUM((clein,h),SAM(clein,h))
                  + SUM((c,e),SAM(c,e))
                  + SUM(c,SAM(c,govert))
                  + SUM((c,i),SAM(c,i))  ;
 INVESTSH0$VFDOMD0
             = SUM((c,i),SAM(c,i))/VFDOMD0 ;
 VGDSH0$VFDOMD0
             = SUM(c,SAM(c,govert))/VFDOMD0 ;
 VEDSH0(e)$VFDOMD0
             = SUM(c,SAM(c,e))/VFDOMD0 ;


*---------- DYNAMIC VARIABLES
EXTENSSHR0(ff,a)$(SUM(ffp$SUM(c,map_ff_qgd(ff,c)),FD0(ffp,a)*WFA0(ffp,a)))= FD0(ff,a)*WFA0(ff,a)/SUM(ffp$SUM(c,map_ff_qgd(ffP,c)),FD0(ffp,a)*WFA0(ffp,a)) ;
EXTENS0(ff,a) = SUM(c$map_ff_qgd(ff,c),QGD0(c)) * EXTENSSHR0(ff,a);
mu_ext(ff,aagr)$(EXTENS0(ff,aagr) AND FD0(ff,aagr)) = 0.142;
mu_ext(ff,aliv)$(EXTENS0(ff,aliv) AND FD0(ff,aliv)) = 0.142;
mu_ext(flivst,a)$(EXTENS0(flivst,a) AND FD0(flivst,a))= 0.001;


*mu_ext(ff,a)$(EXTENS0(ff,a) AND FD0(ff,a)) = 0.0001;
POPN0(h)= sum(l,fsia(h,l));

ADFExt0(ff,a) = 1;

*------------------- Emissions--------------------------------------------------


 coefco2Q(c,a)          = 0 ;
 coefco2H(c,h)          = 0 ;
 coefnco2Q(NCO,a)       = 0 ;
 coefnco2H(NCO,c,h)     = 0 ;
 coefnco2IO(NCO,c,a)    = 0 ;
 coefnco2FS(NCO,c,a)    = 0 ;
 coefnco2EN(NCO,f,a)    = 0 ;


*** all below will be initially zero
 CO2EM_Q0(c,a)          = coefco2Q(c,a)*QINTD0(c,a) ;
 CO2EM_H0(c,h)          = coefco2H(c,h)*QCD0(c,h)   ;
 CO2EMIS_Q0(a)          = SUM(c,CO2EM_Q0(c,a))  ;
 CO2EMIS_H0(h)          = SUM(c,CO2EM_H0(c,h))  ;
 CO2EMIS0               = sum(a,CO2EMIS_Q0(a)) + sum(h,CO2EMIS_H0(h)) ;
 NCO2EM_Q0(nco,a)       = coefnco2Q(nco,a)*QX0(a)           ;
 NCO2EM_FS0(nco,c,a)    = coefnco2FS(nco,c,a)*QINTD0(c,a)   ;
 NCO2EM_IO0(nco,c,a)    = coefnco2IO(nco,c,a)*QINTD0(c,a)   ;
 NCO2EM_EN0(nco,f,a)    = coefnco2EN(nco,f,a)*FD0(f,a)      ;
 NCO2EM_H0(nco,c,h)     = coefnco2H(nco,c,h)*QCD0(c,h)      ;

 NCO2EM_FS_SUM0(nco,a)  = sum(c,coefnco2FS(nco,c,a)*QINTD0(c,a));
 NCO2EM_IO_SUM0(nco,a)  = sum(c,coefnco2IO(nco,c,a)*QINTD0(c,a));
 NCO2EM_EN_SUM0(nco,a)  = sum(f,coefnco2EN(nco,f,a)*FD0(f,a))   ;
 NCO2EM_H_SUM0(nco,h)   = sum(c,coefnco2H(nco,c,h)*QCD0(c,h))   ;

 NCO2EM_A_SUM0(NCO,a)   = NCO2EM_FS_SUM0(NCO,a) + NCO2EM_Q0(NCO,a) + sum(f,coefnco2EN(NCO,f,a)*FD0(f,a)) ;
 NCO2EM_SUM0(nco)       = sum(a,NCO2EM_Q0(nco,a) + NCO2EM_FS_SUM0(nco,a) + NCO2EM_IO_SUM0(nco,a) + NCO2EM_EN_SUM0(nco,a))
                            +sum(h,NCO2EM_H_SUM0(nco,h));

 GHGEM0                   = CO2EMIS0 + SUM(NCO,NCO2EM_SUM0(NCO)) ;


*---  ##### GDP
 GDP0      = SUM((clein,h)$ccesn(clein),PQD0(clein) * (1+TV0(clein)) * QCD0(clein,h))
              + SUM((cag,clein,h)$cces(clein) ,PQD0(clein) * (1+TV0(clein))* QCD20(cag,clein,h))
                             + SUM(c,PQD0(c)*QGD0(c))
                             + SUM((c,i), PQD0(c)*QINVD0(c,i))

*---                             + SUM(c,PQD(c)*dstocconst(c))
                             + SUM(c, PE0(c)*QE0(c))
                             - SUM(c, PM0(c)*QM0(c)) ;

*---  # Slack
 WALRAS0   = 0 ;
*----------------- end of DEMETRA model calibration -----------------------------

*---------Calibration Check

*---------------- DEMETRA Calibration check ----------------------------------

*---------- TRADE BLOCK ----------------------------------------------------
 TTTRANSCHK(m,c)    = SAM(m,c) - SUM((sac,dest),TTTRANS(m,c,sac,dest)) ;


*-------- Supply and Demand Quantities

 QQ0chk(c)      = QM0(c) + QD0(c) - QQ0(c) ;
 QQ0chkcount    = SUM(c$QQ0chk(c),1) ;

 QXC0chk(c)     = QE0(c) + QD0(c) - QXC0(c) ;
 QXC0chkcount   = SUM(c$QXC0chk(c),1) ;

ABORT $(QQ0chkcount NE 0.0)
 "NOT All QQ0chk equal to zero" ;

*--- ABORT $(QXC0chkcount NE 0.0)
*---  "NOT All QXC0chk equal to zero" ;

*-------- 'ILLEGAL' Negativies

 QE0neg(c)$(QE0(c) LT 0.0)  = QE0(c) ;
 QE0negcount                = SUM(c$QE0neg(c),1) ;

 QD0neg(c)$(QD0(c) LT 0.0)  = QD0(c) ;
 QD0negcount                = SUM(c$QD0neg(c),1) ;

 QM0neg(c)$(QM0(c) LT 0.0)  = QM0(c) ;
 QM0negcount                = SUM(c$QM0neg(c),1) ;


ABORT $(QE0negcount NE 0.0)
 "NOT All QE0 greater than zero" ;

ABORT $(QD0negcount NE 0.0)
 "NOT All QD0 greater than zero" ;

ABORT $(QM0negcount NE 0.0)
 "NOT All QM0 greater than zero" ;


*---------- NORMALISED PRICE BLOCK -----------------------------------------



*---------- COMMODITY PRICE BLOCK ------------------------------------------


*---------- NUMERAIRE PRICE BLOCK ------------------------------------------


*---  #### Assignments

 comtotshCHK  = SUM(c,comtotsh0(c)) ;
 vddtotshCHK = SUM(c,vddtotsh0(c)) ;

*---------- PRODUCTION BLOCK -----------------------------------------------

 QXACchk(a,c)   = ioqxacqx(a,c)*QX0(a) ;
 QXchk(a)    = QINT0(a) + QVA0(a) - QX0(a) ;
 deltaxcCHK(c)  = SUM(a,deltaxc(a,c)) ;
 deltaxcchk(c) = SUM(a,deltaxc(a,c));

*---------- FACTOR BLOCK ---------------------------------------------------
 FSISH0chk(f)  = SUM(ins,FSISH0(ins,f)) ;
 chk_fd(f) =   SUM(a, FD0(f,a)) ;

*---------- HOUSEHOLD BLOCK ------------------------------------------------

 FRISCHchk(h)$(frisch(h) GT 0.0)
                            = frisch(h) ;
 FRISCHcount                = SUM(h$FRISCHchk(h),1) ;

 QM0neg(c)$(QM0(c) LT 0.0)  = QM0(c) ;
 QM0negcount                = SUM(c$QM0neg(c),1) ;

ABORT $(FRISCHcount NE 0.0)
 "NOT all frisch less than zero" ;

 hexpschk(h)$(hexps(h) GT HEXP0(h))
                            = hexps(h) ;

 hexpschkcount              = SUM(h$hexpschk(h),1) ;

ABORT $(hexpschkcount NE 0.0)
 "NOT all subsistence expenditures greater than HEXP0" ;

 hohototalCHK(h)     = SUM(hp,hohoconst(h,hp)) ;
 hohototal2CHK(h)    = SUM(hp,hohoconst(hp,h)) ;

 entvashchk(e,f)$(YFDISP0(f))
                 = (SAM(e,f)/YFDISP0(f)) - entvash(e,f) ;

 hovashchk(h,f)$(YFDISP0(f))
                 = (SAM(h,f)/YFDISP0(f)) - hovash(h,f) ;
 comhoav1chk(h)    = SUM(c,comhoav1(c,h)) ;
 comhoavchk(h)     = SUM(cles,comhoav(cles,h)) ;
 betaCHK(h)    = SUM(cc$cles(cc),beta(cc,h)) ;
 alphahCHK(cc,h)$beta(cc,h)    = alphah(cc,h) ;
 alphahCHK2(h) = Sum(cc, alphahCHK(cc,h)) ;
 deltacd2CHK(cc,cc,h) = deltacd(cc,cc,h) -  deltacd2(cc,cc,h) ;
 deltacdCHK(cag,h)  = SUM(cces$map_cag_c(cag,cces),deltacd(cag,cces,h)) ;



*---  CET output function parameter


*---------- ENTERPRISE BLOCK -----------------------------------------------



*---------- AGRI BUDGET BLOCK -----------------------------------------------
*-calibration
 AgBuRecurr0(cGovAgr)            = PQD0(cGovAgr)*QGD0(cGovAgr) ;
 AgBuInvest0(iGovAgr)            = SUM(c,PQD0(c)*QINVD0(c,iGovAgr)) ;
 AgBuInpSub0(fGovAgr,aGovAgr)    = TF0(fGovAgr,aGovAgr)*WF0(fGovAgr)*WFDIST0(fGovAgr,aGovAgr)*FD0(fGovAgr,aGovAgr) ;
 AgBuRevFund0(ff,a)              = TF0(ff,a)*WF0(ff)*WFDIST0(ff,a)*FD0(ff,a) ;
 AgBuOutSub0(aGovAgr)            = TX0(aGovAgr)*PX0(aGovAgr)*QX0(aGovAgr);
 AgBuComSub0(cc,h)               = 0;
 AgBuIncSub0(h)$hrur(h)          = HOGOV0(h);

 AgBuIncSub0(h)$(NOT hrur(h))    = 0 ;

 AgBuTotRecurr0 = SUM((cGovAgr)      ,AgBuRecurr0(cGovAgr)     );
 AgBuTotInvest0 = SUM((iGovAgr)      ,AgBuInvest0(iGovAgr)     );
 AgBuTotInpSub0 = SUM((fGovAgr,aagr) ,AgBuInpSub0(fGovAgr,aagr)) +
                  SUM((ff,a) ,AgBuRevFund0(ff,a))         ;
 AgBuTotOutSub0 = SUM((aagr)         ,AgBuOutSub0(aagr)        );
 AgBuTotComSub0 = 0;
 AgBuTotIncSub0 = SUM(h,AgBuIncSub0(h));
 AgBuTOTALx0    =      AgBuTotRecurr0
                     + AgBuTotInvest0
                     + AgBuTotInpSub0
                     + AgBuTotOutSub0
                     + AgBuTotComSub0
                     + AgBuTotIncSub0 ;

 AgBuTOTShr0   = AgBuTOTALx0/GBUDG0;

*-nutrition
NutVal0(nutElem,h) = SUM(c,nutTable(c,nutElem)*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))));


*---------- KAPITAL BLOCK --------------------------------------------------
 SAVCHK  = INVEST0 - TOTSAV0 ;
 ABORT $(ABS(SAVCHK) GT mod_cont("toldiffsam"))
 "SAVINGS AND INVESTMENTS NOT EQUAL IN THE DATA", INVEST0, TOTSAV0, SAVCHK ;
 ioqinvdCHK(i) = SUM(c,ioqinvd(c,i)) ;
*---------- FOREIGN INSTITUTIONS BLOCK -------------------------------------

*---------- MARKET CLEARING BLOCK ------------------------------------------




*---------- End of DEMETRA Calibration check ----------------------------------

