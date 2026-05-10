*-------------------- DEMETRA model calibration -------------------------
$ontext
   Calibration proceeds by reference to the blocks of equations
each block contains all the related parameter declarations and assignments
$offtext

*- Considerations for future developments:
$ontext

    1.  Should the elasticities be time period specific?
    2.  Is it OK to leave the numeraire or does it need resetting, noting
        that the weights change each period?
    3.  Does ioqxacqx need updating?
    4.  Does the factor block need updating?

$offtext

*-------- NORMALISED PRICE BLOCK -----------------------------------------

*-------- TRADE AND TRANSPORT TRANSACTIONS -------------------------------

*-------- TRADE BLOCK ----------------------------------------------------

*- #### Exports Block

*- ## Parameters for CET functions

*- rhot(c)$(cd(c) AND ce(c))    = (1/ELASTC(c,"omega")) + 1 ;

 gamma(c)$(cd(c) AND ce(c))
              = 1/(1+PD.L(c)/PE.L(c)*(QE.L(c)/QD.L(c))**(rhot(c)-1));

 at(c)$(cd(c) AND ce(c))
              = (QXC.L(c))
                 /(gamma(c)*QE.L(c)**rhot(c) + (1-gamma(c))*
                       QD.L(c)**rhot(c))**(1/rhot(c));

 gammaR(c,w)$(ceR(c,w))
                = (PER0(c,w)*(ZETAER0(c,w)*QER0(c,w))**(1+rhotR(c)) ) /
                SUM(wp$cer(c,wp), PER0(c,wp)*(ZETAER0(c,w)*QER0(c,wp))**(1+rhotR(c)));


*---  Using {QXC0(c) = (SUM(a,SAM(a,c))/PXC0(c))} in statement for at(c)
 atR(c)$(cd(c) AND ce(c))  = QE0(c)/SUM(w$gammar(c,w), gammar(c,w)*(ZETAER0(c,w)*QER0(c,w))**(-rhotR(c)) )**(-1/(rhotR(c))) ;

*- ## Parameters for Export Demand functions

 econ(c,w)         = QE.L(c) ;
*- eta(c)          = ELASTC(c,"exdem") ;

 pwse(c,w)$QE.L(c)  = PWE.L(c) ;

*- #### Imports Block

*- ## Parameters for Armington/CES functions

*- rhoc(c)$(cx(c) AND cm(c))    = (1/ELASTC(c,"sigma")) - 1 ;

 delta(c)$(cd(c) AND cm(c))
               = (PM.L(c)*QM.L(c)**(rhoc(c)+1))
                  /(PM.L(c)*QM.L(c)**(rhoc(c)+1) + PD.L(c)*QD.L(c)**(rhoc(c)+1)) ;

 ac(c)$(cd(c) AND cm(c))
               = QQ.L(c)/(delta(c)*QM.L(c)**(-rhoc(c))
                         +(1-delta(c))*QD.L(c)**(-rhoc(c)))**(-1/rhoc(c)) ;

 deltaR(w,c)$SUM(wp, PMR.L(wp,c)*QMR.L(wp,c)**(1+rhocR(c)))
           =    (PMR0(w,c)*QMR.L(w,c)**(1+rhocR(c)))
                 / SUM(wp$cmR(wp,c), PMR.L(wp,c)*QMR.L(wp,c)**(1+rhocR(c)));

 acR(c)$(cd(c) AND cm(c) AND SUM(w$deltaR(w,c), deltaR(w,c)*QMR.L(w,c))) = QM.L(c)/SUM(w$deltaR(w,c), deltaR(w,c)*QMR.L(w,c)**(-rhocR(c)))**(-1/rhocR(c));

display acr ;
*-------- TRADE AND TRANSPORT MARGINS BLOCK ------------------------------


*-------- COMMODITY PRICE BLOCK ------------------------------------------


*-------- NUMERAIRE PRICE BLOCK ------------------------------------------

*- ## Price index weights

*- note that the CPI weights are based on household expenditure shares ONLY
*- alternate 1 - CPI weights based on household final demand expenditure shares


* comtotsh(c)$(SUM((cp,hp),(PQD.L(cp)*(1+TV.L(cp))*QCD.L(cp,hp))))
*              = SUM(h,(PQD.L(c)*(1+TV.L(c))*QCD.L(c,h)))
*                      /(SUM((cp,hp),(PQD.L(cp)*(1+TV.L(cp))*QCD.L(cp,hp)))) ;

*COMTOTSH.FX(c) = VQCD.L(c)/SUM(cp,VQCD.L(cp)) ;


*- PPI weights are based on the value of domestic output for the domestic market

*- vddtotsh(c)$(SUM(cp,(PXC.L(cp)*QXC.L(cp))))
*-               = (PXC.L(c)*QXC.L(c))/(SUM(cp,(PXC.L(cp)*QXC.L(cp)))) ;

*- vddtotsh(c)$(SUM(cp,(PD.L(cp)*QD.L(cp))))
*-               = (PD.L(c)*QD.L(c))/(SUM(cp,(PD.L(cp)*QD.L(cp)))) ;

*-------- PRODUCTION BLOCK -----------------------------------------------

*- CES aggregation functions for Level 1 of production nest

*- rhocx(a)    = (1/ELASTX(a,"sigmax")) - 1 ;

* predeltax(a)$(QINT.L(a))
*               = (PVA.L(a)/PINT.L(a))*(QVA.L(a)/QINT.L(a))**(1+rhocx(a)) ;
* deltax(a)
*               = predeltax(a)/(1.0+predeltax(a)) ;

* adxb(a)$deltax(a)
*               = QX.L(a)/(deltax(a)*QVA.L(a)**(-rhocx(a))
*                      +(1-deltax(a))*QINT.L(a)**(-rhocx(a)))**(-1/rhocx(a)) ;


*- Leontief aggregation functions for Level 1 of production nest

*- ioqintqx(a)$QX.L(a)   = QINT.L(a)/QX.L(a) ;

*- ioqvaqx(a)$QX.L(a)    = QVA.L(a)/QX.L(a) ;

*- CES aggregation functions for Level 2 of production nest

*- rhocva(a)   = (1/ELASTX(a,"sigmava")) - 1 ;


*- share parameters WITH factor use taxes - tf0(f,a)
$ontext
 deltava(ff,a)$(FD.L(ff,a) AND map_a_ftop(a,ff))
          = (WFDIST.L(ff,a)*WF.L(ff)*(1+tf02(ff,a))*(FD.L(ff,a))**(1+rhocva(a)))
            /SUM(ffp,WFDIST.L(ffp,a)*WF.L(ffp)*(1+tf02(ffp,a))*(FD.L(ffp,a))
             **(1+rhocva(a))) ;


 advab(a)  = QVA.L(a)/(SUM(ff$(FD.L(ff,a) AND map_a_ftop(a,ff)),
                   deltava(ff,a)*FD.L(ff,a)**(-rhocva(a))))**(-1/rhocva(a));;


*- rhofd(fag,a)   = (1/ELASTFD(fag,a)) - 1 ;

 deltafd(fag,ff,a)$(map_fag_ff_a(fag,ff,a) AND SUM((ffp)$ (map_fag_ff_a(fag,ffp,a) ),WFDIST.L(ffp,a)*WF.L(ffp)))

             = (WFDIST.L(ff,a)*WF.L(ff)*(1+tf02(ff,a))*(ADFD.L(ff,a)*FD.L(ff,a))
                        **(1+rhofd(fag,a)))
     / SUM((ffp)$ (map_fag_ff_a(fag,ffp,a)),WFDIST.L(ffp,a)*WF.L(ffp)*(1+tf02(ffp,a))

                 *(ADFD.L(ffp,a)*FD.L(ffp,a))**(1+rhofd(fag,a))) ;

*- iofdfag(fag,ff,a)$(map_fag_ff_a(fag,ff,a) AND SUM((ffp)$ (map_fag_ff_a(fag,ffp,a)),WFDIST.L(ffp,a)*WF.L(ffp)))
*-             = FD.L(ff,a)
*-     / SUM((ffp)$ (map_fag_ff_a(fag,ffp,a)),(FD.L(ffp,a))) ;

*- adfag0(fag,a)$FD.L(fag,a) = FD.L(fag,a)
*-                        /(SUM(ff$(FD.L(ff,a)) ,deltafd(fag,ff,a)*FD.L(ff,a)
*-                         **(-rhofd(fag,a))))**(-1/rhofd(fag,a)) ; ;
*- adfagb(ff,a)       =  ADFAG0(ff,a)  ;

*- Intermediate Input Demand

*- ioqtdqd(c,a)$(QINT.L(a))
*-            = (QINTD.L(c,a) -  SUM((fc)$map_c_f_a(c,fc,a),FD.L(fc,a)))/QINT.L(a)   ;

$offtext
*- Commodity Output

*- rhocxc(c)   = (1/ELASTC(c,"sigmaxc")) - 1 ;

 deltaxc(a,c)$SAM(a,c)
               = (PXAC.L(a,c)*QXAC.L(a,c)**(1+rhocxc(c)))
                 /SUM(ap,PXAC.L(ap,c)*QXAC.L(ap,c)**(1+rhocxc(c))) ;

 adxc(c)$QXC.L(c)
               = QXC.L(c)/(SUM(a,deltaxc(a,c)*QXAC.L(a,c)
                    **(-rhocxc(c)))**(-1/rhocxc(c)));

*- Activity Output

*- ioqxacqx(a,c)$(QX.L(a)*cti(a,c))
*-               = QXAC.L(a,c)/(QX.L(a)*cti(a,c) );

*-------- FACTOR BLOCK ---------------------------------------------------


*-------- HOUSEHOLD BLOCK ------------------------------------------------

 deltacd(cag,cces,h)$deltacd(cag,cces,h)
              = (((PQD.L(cces)*(1+tv.L(cces))) )
                               * QCD2.L(cag,cces,h)**(1+rhocd(cag,h)))
                / SUM(ccesp$map_cag_c(cag,ccesp),
                     (((PQD.L(ccesp)*(1+tv02(ccesp))) )
                               * QCD2.L(cag,ccesp,h)**(1+rhocd(cag,h))))  ;
 deltacd2(cc,cces,h)$(SUM(ccp$map_cag_c(ccp,cces),PQD.L(cces)
                      * (1+tv02(cces)) * (QCD.L(cces,h))**(1+rhocd(ccp,h))))
            = (PQD.L(cces) * (1+tv02(cces)) * (QCD.L(cces,h))
                    **(1+rhocd(cc,h)))
                     / SUM(ccp$map_cag_c(ccp,cces),PQD.L(cces)
                      * (1+tv02(cces)) * (QCD.L(cces,h))**(1+rhocd(ccp,h))) ;

 accd(cag,h)$accd(cag,h)
           = QCD.L(cag,h)
             /(SUM(cces$(QCD2.L(cag,cces,h) NE 0 ),deltacd(cag,cces,h)*QCD2.L(cag,cces,h)
             **(-rhocd(cag,h))))**(-1/rhocd(cag,h)) ;



*- ## Consumption Expenditures
*- # Cobb Douglas Utility function
$ontext
 comhoav(c,h)$(SUM(cp,(PQD.L(cp)*(1+TV.L(cp))*QCD.L(cp,h))))
                 = (PQD.L(c)*(1+TV.L(c))*QCD.L(c,h))
                     /(SUM(cp,(PQD.L(cp)*(1+TV.L(cp))*QCD.L(cp,h)))) ;

 alphah(c,h)$(SUM(cp,(PQD.L(cp)*(1+TV.L(cp))*QCD.L(cp,h))))
                 = (PQD.L(c)*(1+TV.L(c))*QCD.L(c,h))
                     /(SUM(cp,(PQD.L(cp)*(1+TV.L(cp))*QCD.L(cp,h)))) ;

*- # Stone-Geary Utility function
*- Weighted sum of the expenditures elasticities must equal one.
*- Weights are average budget shares. Normalised elasticities will satisfy
*- Engel aggregation

 sumelast(h)   = SUM(c, alphah(c,h)*ELASTY(c,h)) ;

 yhelast(c,h)$sumelast(h)
               = ELASTY(c,h)/sumelast(h) ;

 yhelast(c,h)$(alphah(c,h) eq 0)  = 0 ;

 beta(c,h)     = yhelast(c,h)*alphah(c,h) ;

 frisch(h)     = ELASTMU(h,"frisc") ;

 qcdconst(c,h)$(PQD.L(c) and frisch(h) and beta(c,h))
               = (HEXP.L(h)/(PQD.L(c)*(1+tv.L(c))) )
                    *(alphah(c,h)+(beta(c,h)/frisch(h))) ;

 hexps(h)      = SUM(c,qcdconst(c,h) * PQD.L(c)*(1+tv.L(c))) ;

$offtext

*-------- ENTERPRISE BLOCK -----------------------------------------------



*-------- GOVERNMENT BLOCK -----------------------------------------------

*- #### Government Taxes Block

*- #### Government Income and Expenditure Block


*-------- KAPITAL BLOCK --------------------------------------------------


*-------- FOREIGN INSTITUTIONS BLOCK -------------------------------------



*-------- MARKET CLEARING BLOCK ------------------------------------------



*--------------------- end of DEMETRA model calibration ------------------
