* ----------------- welfare results -----------------------------

*- Per capita household incomes and consumption expenditures

*- YHRes_cap(h,%resElem1%)          = YH.L(h)/pop(h) ;

*- HEXPres_cap(h,%resElem1%)        = HEXP.L(h)/pop(h) ;

*- YHRes_cap(h,%resElem1%)$YH_cap0(h)
*-                                = (YHRes_cap(h,%resElem1%)/YH_cap0(h)-1)*100 ;

*- HEXPres_cap(h,%resElem1%)$HEXP_cap0(h)
*-                                 = (HEXPres_cap(h,%resElem1%)/HEXP_cap0(h)-1)*100 ;

*---------- SUMMARY WELFARE MEASURES -------------
$ontext
 EV0(h,%resElem1%)$HEXPres(h,%resElem1%)
                = PROD(c,(PQD0(c)/PQDres(c,%resElem1%))**beta(c,h))
                      *(HEXPres(h,%resElem1%)
                        -SUM(cc,qcdconst(cc,h)
                                *(PQCResD(cc,h,%resElem1%)
                                  +PQDres(cc,%resElem1%))))
                  -(HEXP0(h)-SUM(cc,qcdconst(cc,h)
                      * (PQCD0(cc,h)+PQD0(cc))));
$offtext


 EV0(h,%resElem1%)$HEXPres(h,%resElem1%)
                = PROD(cc$(PQC0(cc,h)),(PQC0(cc,h)/PQCRes(cc,h,%resElem1%))**beta(cc,h))
                  *(HEXPres(h,%resElem1%)
                    -SUM(cc,qcdconst(cc,h) * PQCRes(cc,h,%resElem1%)))
                  -(HEXP0(h) - SUM(cc,qcdconst(cc,h) * PQC0(cc,h))) ;


 EV1("Level","Deflat",h,"Nan",%resElem1%)     =  PROD(cc$PQC0(cc,h),(PQC0(cc,h)/PQCRes(cc,h,%resElem1%))**beta(cc,h));

 EV1("Level","evTotal",h,"Nan",%resElem1%)    =  EV0(h,%resElem1%);
 EV1("Level","evHEXP",h,"Nan",%resElem1%)       =  EV1("Level","Deflat",h,"Nan",%resElem1%) *HEXPres(h,%resElem1%);
 EV1("Level","evQCD",h,cc,%resElem1%)           =  EV1("Level","Deflat",h,"Nan",%resElem1%) *QCDRes(cc,h,%resElem1%)* PQCRes(cc,h,%resElem1%) ;
 EV1("Level","evqcdconst",h,cc,%resElem1%)      = -EV1("Level","Deflat",h,"Nan",%resElem1%) *qcdconst(cc,h)*PQCRes(cc,h,%resElem1%);
 EV1("Level","evqcdconstTot",h,"Nan",%resElem1%)=  SUM(cc,EV1("Level","evqcdconst",h,cc,%resElem1%)) ;

 EV1("Level","evYH",h,"Nan",%resElem1%)         =  EV1("Level","Deflat",h,"Nan",%resElem1%) *YHRes(h,%resElem1%)           ;
 EV1("Level","evTYH",h,"Nan",%resElem1%)        = -EV1("Level","Deflat",h,"Nan",%resElem1%) *TYHRes(h,%resElem1%)*YHRes(h,%resElem1%);
 EV1("Level","evSHH",h,"Nan",%resElem1%)        = -EV1("Level","Deflat",h,"Nan",%resElem1%) *SHHres(h,%resElem1%)*YHRes(h,%resElem1%);
 EV1("Level","evHOHOout",h,hp,%resElem1%)       = -EV1("Level","Deflat",h,"Nan",%resElem1%) *HOHOres(hp,h,%resElem1%) ;

 EV1("Level","evINSVA",h,f,%resElem1%)          =  EV1("Level","Deflat",h,"Nan",%resElem1%) *INSVAres(h,f,%resElem1%);
 EV1("Level","evINSVATotal",h,"Nan",%resElem1%) =  SUM(f,EV1("Level","evINSVA",h,f,%resElem1%));
 EV1("Level","evHOHOHin",h,"Nan",%resElem1%)    =  EV1("Level","Deflat",h,"Nan",%resElem1%) *SUM(hp,HOHORes(h,hp,%resElem1%));
 EV1("Level","evHOENTin",h,"Nan",%resElem1%)    =  EV1("Level","Deflat",h,"Nan",%resElem1%) *SUM(e,HOENTres(h,e,%resElem1%));
 EV1("Level","evHOGOVin",h,"Nan",%resElem1%)    =  EV1("Level","Deflat",h,"Nan",%resElem1%) *HOGOVRes(h,%resElem1%);
 EV1("Level","evHOROWin",h,w,%resElem1%)    =  EV1("Level","Deflat",h,"Nan",%resElem1%) *HOWORres(h,w,%resElem1%)*SCALRes("sER",%resElem1%);

$ontext
 EV1("Level","evYFINS",h,f,%resElem1%)  $EV1("Level","evINSVA",h,f,%resElem1%)   =  EV1("Level","Deflat",h,"Nan",%resElem1%) *YFINSres(f,%resElem1%) ;
 EV1("Level","evgovvash",h,f,%resElem1%)$EV1("Level","evINSVA",h,f,%resElem1%) = -EV1("Level","Deflat",h,"Nan",%resElem1%) *govvash(f)*YFDISPres(f,%resElem1%) ;
 EV1("Level","evworvash",h,f,%resElem1%)$EV1("Level","evINSVA",h,f,%resElem1%) = -EV1("Level","Deflat",h,"Nan",%resElem1%) *worvash(f)*YFDISPres(f,%resElem1%) ;

 EV1("Level","evYFDISP",h,f,%resElem1%) $EV1("Level","evINSVA",h,f,%resElem1%)  =  EV1("Level","Deflat",h,"Nan",%resElem1%) *YFDISPres(f,%resElem1%) ;
 EV1("Level","evdeprec",h,f,%resElem1%) $EV1("Level","evINSVA",h,f,%resElem1%)  = -EV1("Level","Deflat",h,"Nan",%resElem1%) *deprec(f)*YFres(f,%resElem1%) ;
 EV1("Level","evTYF",h,f,%resElem1%)    $EV1("Level","evINSVA",h,f,%resElem1%)     = -EV1("Level","Deflat",h,"Nan",%resElem1%) *resTYF(f,%resElem1%)*YFres(f,%resElem1%) ;

 EV1("Level","evYF",h,f,%resElem1%)     $EV1("Level","evINSVA",h,f,%resElem1%)      =  EV1("Level","Deflat",h,"Nan",%resElem1%) *YFres(f,%resElem1%) ;
 EV1("Level","evFDxWF",h,f,%resElem1%)  $EV1("Level","evINSVA",h,f,%resElem1%)   =  EV1("Level","Deflat",h,"Nan",%resElem1%) *SUM(a,WFres(f,%resElem1%)*WFDISTres(f,a,%resElem1%)*FDRes(f,a,%resElem1%))  ;
 EV1("Level","evfactwor",h,f,%resElem1%)$EV1("Level","evINSVA",h,f,%resElem1%) =  EV1("Level","Deflat",h,"Nan",%resElem1%) *factwor(f)*SCALres("sER",%resElem1%);
$offtext

*- here we are assumning that the distribution of income at different level is same as the distribution of INSVA
 EV1("Level","evYFINS",h,f,%resElem1%)  $EV1("Level","evINSVA",h,f,%resElem1%)   =  EV1("Level","Deflat",h,"Nan",%resElem1%) * FSISHres(h,f,%resElem1%) * YFINSres(f,%resElem1%) ;
 EV1("Level","evgovvash",h,f,%resElem1%)$EV1("Level","evINSVA",h,f,%resElem1%) = -EV1("Level","Deflat",h,"Nan",%resElem1%) * FSISHres(h,f,%resElem1%) * govvash(f)*YFDISPres(f,%resElem1%) ;
 EV1("Level","evworvash",h,f,%resElem1%)$EV1("Level","evINSVA",h,f,%resElem1%) = -EV1("Level","Deflat",h,"Nan",%resElem1%) * SUM(w,FSISHres(h,f,%resElem1%) * worvash(w,f)*YFDISPres(f,%resElem1%)) ;

 EV1("Level","evYFDISP",h,f,%resElem1%) $EV1("Level","evINSVA",h,f,%resElem1%)  =  EV1("Level","Deflat",h,"Nan",%resElem1%) * FSISHres(h,f,%resElem1%) * YFDISPres(f,%resElem1%) ;
 EV1("Level","evdeprec",h,f,%resElem1%) $EV1("Level","evINSVA",h,f,%resElem1%)  = -EV1("Level","Deflat",h,"Nan",%resElem1%) * FSISHres(h,f,%resElem1%) * deprec(f)*YFres(f,%resElem1%) ;
 EV1("Level","evTYF",h,f,%resElem1%)    $EV1("Level","evINSVA",h,f,%resElem1%)     = -EV1("Level","Deflat",h,"Nan",%resElem1%) * FSISHres(h,f,%resElem1%) * TYFres(f,%resElem1%)*YFres(f,%resElem1%) ;

 EV1("Level","evYF",h,f,%resElem1%)     $EV1("Level","evINSVA",h,f,%resElem1%)      =  EV1("Level","Deflat",h,"Nan",%resElem1%) * FSISHres(h,f,%resElem1%) * YFres(f,%resElem1%) ;
 EV1("Level","evFDxWF",h,f,%resElem1%)  $EV1("Level","evINSVA",h,f,%resElem1%)   =  EV1("Level","Deflat",h,"Nan",%resElem1%) *  FSISHres(h,f,%resElem1%) * SUM(a,WFres(f,%resElem1%)*WFDISTres(f,a,%resElem1%)*FDRes(f,a,%resElem1%))  ;
 EV1("Level","evfactwor",h,f,%resElem1%)$EV1("Level","evINSVA",h,f,%resElem1%) =  EV1("Level","Deflat",h,"Nan",%resElem1%) * SUM(w,FSISHres(h,f,%resElem1%) * factwor(f,w)*SCALres("sER",%resElem1%));



*- delete small numbers
 EV1("Level",welfDim,h,sac,%resElem%)$(ABS(EV1("Level",welfDim,h,sac,%resElem%))<1E-7 ) = 0;

 EV1("Share","evHEXP",h,"Nan",%resElem1%)$EV1("Level","EVTotal",h,"Nan",%resElem1%)= EV1("Level","evHEXP",h,"Nan",%resElem1%)/EV1("Level","evTotal",h,"Nan",%resElem1%)*100;
 EV1("Share","evqcdconstTot",h,sac,%resElem1%)$EV1("Level","EVTotal",h,"Nan",%resElem1%)= EV1("Level","evqcdconstTot",h,sac,%resElem1%) /EV1("Level","evTotal",h,"Nan",%resElem1%)*100;

 EV1("Share","evQCD",h,cc,%resElem1%)$EV1("Level","evHEXP",h,"Nan",%resElem1%)  = EV1("Level","evQCD",h,cc,%resElem1%) /EV1("Level","evHEXP",h,"Nan",%resElem1%) *100;

 EV1("Share","evqcdconst",h,cc,%resElem1%)$EV1("Level","evqcdconstTot",h,"Nan",%resElem1%) = EV1("Share","evqcdconst",h,cc,%resElem1%) / EV1("Level","evqcdconstTot",h,"Nan",%resElem1%)*100;


 EV1("Share","evINSVA",h,f,%resElem1%)         $EV1("Level","evINSVATotal",h,"Nan",%resElem1%)=  EV1("Level","evINSVA",h,f,%resElem1%)          / EV1("Level","evINSVATotal",h,"Nan",%resElem1%)*100;
 EV1("Share","evINSVATotal",h,"Nan",%resElem1%)$EV1("Level","evYH",h,"Nan",%resElem1%)        =  EV1("Level","evINSVATotal",h,"Nan",%resElem1%) / EV1("Level","evYH",h,"Nan",%resElem1%)*100        ;
 EV1("Share","evHOHOHin",h,"Nan",%resElem1%)   $EV1("Level","evYH",h,"Nan",%resElem1%)        =  EV1("Level","evHOHOHin",h,"Nan",%resElem1%)    / EV1("Level","evYH",h,"Nan",%resElem1%)*100        ;
 EV1("Share","evHOENTin",h,"Nan",%resElem1%)   $EV1("Level","evYH",h,"Nan",%resElem1%)        =  EV1("Level","evHOENTin",h,"Nan",%resElem1%)    / EV1("Level","evYH",h,"Nan",%resElem1%)*100        ;
 EV1("Share","evHOGOVin",h,"Nan",%resElem1%)   $EV1("Level","evYH",h,"Nan",%resElem1%)        =  EV1("Level","evHOGOVin",h,"Nan",%resElem1%)    / EV1("Level","evYH",h,"Nan",%resElem1%)*100        ;
 EV1("Share","evHOROWin",h,"Nan",%resElem1%)   $EV1("Level","evYH",h,"Nan",%resElem1%)        =  EV1("Level","evHOROWin",h,"Nan",%resElem1%)    / EV1("Level","evYH",h,"Nan",%resElem1%)*100        ;

 EV1("Share","evYFINS",h,f,%resElem1%)  $EV1("Level","evYFDISP",h,f,%resElem1%)  =  EV1("Level","evYFINS",h,f,%resElem1%)  /EV1("Level","evYFDISP",h,f,%resElem1%)*100  ;
 EV1("Share","evgovvash",h,f,%resElem1%)$EV1("Level","evYFDISP",h,f,%resElem1%)  =  EV1("Level","evgovvash",h,f,%resElem1%)/EV1("Level","evYFDISP",h,f,%resElem1%)*100  ;
 EV1("Share","evworvash",h,f,%resElem1%)$EV1("Level","evYFDISP",h,f,%resElem1%)  =  EV1("Level","evworvash",h,f,%resElem1%)/EV1("Level","evYFDISP",h,f,%resElem1%)*100  ;

 EV1("Share","evYFDISP",h,f,%resElem1%) $EV1("Level","evYF",h,f,%resElem1%)  = EV1("Level","evYFDISP",h,f,%resElem1%) / EV1("Level","evYF",h,f,%resElem1%)*100 ;
 EV1("Share","evdeprec",h,f,%resElem1%) $EV1("Level","evYF",h,f,%resElem1%)  = EV1("Level","evdeprec",h,f,%resElem1%) / EV1("Level","evYF",h,f,%resElem1%)*100 ;
 EV1("Share","evTYF",h,f,%resElem1%)    $EV1("Level","evYF",h,f,%resElem1%)  = EV1("Level","evTYF",h,f,%resElem1%)    / EV1("Level","evYF",h,f,%resElem1%)*100 ;

 EV1("Share","evFDxWF",h,f,%resElem1%)  $EV1("Level","evYF",h,f,%resElem1%)  =EV1("Level","evFDxWF",h,f,%resElem1%)  / EV1("Level","evYF",h,f,%resElem1%)*100   ;
 EV1("Share","evfactwor",h,f,%resElem1%)$EV1("Level","evYF",h,f,%resElem1%)  =EV1("Level","evfactwor",h,f,%resElem1%)/ EV1("Level","evYF",h,f,%resElem1%)*100  ;

 EV1Base("Level",welfDim,h,sac,%resElem1%) =  EV1("Level",welfDim,h,sac,%resElem1%)-EV1("Level",welfDim,h,sac,%resElemBs%);
 EV1Base("Share",welfDim,h,sac,%resElem1%) =  EV1("Share",welfDim,h,sac,%resElem1%);
 EV1Base("PerBase",welfDim,h,sac,%resElem1%)$EV1("Level",welfDim,h,sac,%resElemBs%) =  EV1("Level",welfDim,h,sac,%resElem1%)/EV1("Level",welfDim,h,sac,%resElemBs%)*100-100;

*-populate parameters


 EV_cap(h,%resElem1%)$(POPNres(h,%resElem1%))
                   = EV0(h,%resElem1%)/POPNres(h,%resElem1%) ;

 EVBase(h,%resElem1%)$HEXPres(h,%resElem1%) = PROD(cc$PQCRes(cc,h,%resElem1%),(PQCRes(cc,h,%resElemBs%)/PQCRes(cc,h,%resElem1%))**beta(cc,h))
                      *(HEXPres(h,%resElem1%) - SUM(cc,qcdconst(cc,h)*PQCRes(cc,h,%resElem1%)))
                      -(HEXPres(h,%resElemBs%) - SUM(cc,qcdconst(cc,h)*PQCRes(cc,h,%resElemBs%))) ;


 EVBase_cap(h,%resElem1%)$(POPNres(h,%resElem1%))
                   = EVBase(h,%resElem1%)/POPNres(h,%resElem1%) ;

 EVBasePerc(h,%resElem1%)$EV0(h,%resElemBs%) = EVBase(h,%resElem1%)/EV0(h,%resElemBs%)*100;


$ontext
IC and EV formulas from Blonigen, Bruce A., Joseph E. Flynn, and
Kenneth A. Reinert (1997) Sector-Focused General Equilibrium Modeling,
in eds. Joseph F. Francois and Kenneth A. Reinert, Applied Methods
for Trade Policy Analysis. Cambridge, MA: Cambridge University Press,
pp. 189-230.
$offtext

 IC(h,%resElem1%)$HEXPres(h,%resElem1%)  = ((HEXPres(h,%resElem1%)
                         - SUM(cc,PQCRes(cc,h,%resElem1%)*qcdconst(cc,h)))
                              /(PROD(cc,PQCRes(cc,h,%resElem1%)**beta(cc,h))))
                                 * (PROD(cc,PQC0(cc,h)**beta(cc,h)))
                                   + (SUM(cc,PQC0(cc,h)*qcdconst(cc,h))) ;

 IC_cap(h,%resElem1%)$POPNres(h,%resElem1%)
                    =  IC(h,%resElem1%)/POPNres(h,%resElem1%) ;

*-!!!HD: this is not working!!!!!!!!!
 ICBase(h,%resElem1%)$HEXPres(h,%resElem1%)  = ((HEXPres(h,%resElem1%)
                         - SUM(cc,PQCRes(cc,h,%resElem1%)*qcdconst(cc,h)))
                              /(PROD(cc,PQCRes(cc,h,%resElem1%)**beta(cc,h))))
                                 * (PROD(cc,PQCRes(cc,h,%resElemBs%)**beta(cc,h)))
                                   + (SUM(cc,PQCRes(cc,h,%resElemBs%)*qcdconst(cc,h))) ;


 ICBase_cap(h,%resElem1%)$POPNres(h,%resElem1%)
                    =  ICBase(h,%resElem1%)/POPNres(h,%resElem1%) ;
 EV_alt(h,%resElem1%)
                    = IC(h,%resElem1%) - HEXP0(h) ;
 EV_alt_cap(h,%resElem1%)$POPNres(h,%resElem1%)
                    =  EV_alt(h,%resElem1%)/POPNres(h,%resElem1%) ;

 EVBase_alt(h,%resElem1%)
                    = ICBase(h,%resElem1%) - HEXPres(h,%resElemBs%) ;

 EVBase_alt_cap(h,%resElem1%)$POPNres(h,%resElem1%)
                    =  EVBase_alt(h,%resElem1%)/POPNres(h,%resElem1%) ;

*---------- SLUTSKY WELFARE MEASURES -------------

 EV_H_slut(h,%resElem1%)
                     = SUM(cc,PQC0(cc,h) * QCDRes(cc,h,%resElem1%))
                         - HEXP0(h) ;
 EVBase_H_slut(h,%resElem1%)
                     = SUM(cc,PQCRes(cc,h,%resElemBs%) * QCDRes(cc,h,%resElem1%))
                         - HEXPres(h,%resElemBs%) ;
 EV_R_slut(%resElem1%)
                     = SUM((cc,h),PQC0(cc,h)*QCDRes(cc,h,%resElem1%))
                     + SUM(c,PQD0(c) * QGDres(c,%resElem1%))
                     + SUM(c,PQD0(c) * SUM(i,QINVDres(c,i,%resElem1%)))
                         - (SUM(h,HEXP0(h))
                           + SUM((c,i),PQD0(c) * (QGD0(c) + QINVD0(c,i)))) ;

 EVBase_R_slut(%resElem1%)
                     = SUM((cc,h),PQCRes(cc,h,%resElemBs%) * QCDRes(cc,h,%resElem1%))
                     + SUM(c,PQDres(c,%resElemBs%) *  QGDres(c,%resElem1%))
                     + SUM(c,PQDres(c,%resElemBs%) *  SUM(i,QINVDres(c,i,%resElem1%)))
                         - (SUM(h,HEXPres(h,%resElemBs%))
                           + SUM((c,i),PQDres(c,%resElemBs%) * (QGDres(c,%resElemBs%) + QINVDres(c,i,%resElemBs%)))) ;

EVBase        (h,%resElem%)$(ABS(EVBase        (h,%resElem%)) LT 1E-8)=0;
EVBase_cap    (h,%resElem%)$(ABS(EVBase_cap    (h,%resElem%)) LT 1E-8)=0;
ICBase        (h,%resElem%)$(ABS(ICBase        (h,%resElem%)) LT 1E-8)=0;
ICBase_cap    (h,%resElem%)$(ABS(ICBase_cap    (h,%resElem%)) LT 1E-8)=0;
EVBase_alt    (h,%resElem%)$(ABS(EVBase_alt    (h,%resElem%)) LT 1E-8)=0;
EVBase_alt_cap(h,%resElem%)$(ABS(EVBase_alt_cap(h,%resElem%)) LT 1E-8)=0;
EVBase_H_slut (h,%resElem%)$(ABS(EVBase_H_slut (h,%resElem%)) LT 1E-8)=0;
EVBase_R_slut (  %resElem%)$(ABS(EVBase_R_slut (  %resElem%)) LT 1E-8)=0;


*- ------- Exporting Welfare Results to GDX -------------------------------

*- This writes the results data to GDX

Execute_Unload  '%resultF%/%mode%_%exp%_reswelf.gdx',
                   YH_cap
                   HEXP_cap
                   EV0
                   EV1
                   EV1Base
                   EVBasePerc
                   EV_cap
                   IC
                   IC_cap
                   EV_alt
                   EV_alt_cap
                   EV_H_slut
                   EV_R_slut
                   EVBase
                   EVBase_cap
                   ICBase
                   ICBase_cap
                   EVBase_alt
                   EVBase_alt_cap
                   EVBase_H_slut
                   EVBase_R_slut
           ;

*- ----------------- end of DEMETRA welfare results ----------------------
