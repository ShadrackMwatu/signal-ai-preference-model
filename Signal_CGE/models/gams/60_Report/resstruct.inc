*------------------------------------------------------------------------------
*-------------------------------------------------------------------------------
*--   DEMETRA v1.0-alpha
*--
*--   GAMS file : resstruct.inc
*--
*--   @purpose  : prepare structural tavles
*--   @author   : 
*--   @date     :
*--   @since    :
*--   @refDoc   :
*--   @seeAlso  :
*--   @calledBy : report.inc, dynamic simulations
*-------------------------------------------------------------------------------
*-------------------------------------------------------------------------------

* ----------------- Structural Tables --------------------------------====

* ------- 2. Assign Structural Tables ------------------------------------

* Commodity account shares - indexed on stab3

* Demand Structures

 nCOMMODSH("stPRIVregDEM",c,%resElem1%)$(PQDres(c,%resElem1%)*(SUM(h,QCDres(c,h,%resElem1%)) + QGDres(c,%resElem1%)
                                          + sum(i,QINVDres(c,i,%resElem1%)) + sum(a,QINTDres(c,a,%resElem1%))))
           = SUM(h,(PQDres(c,%resElem1%)* QCDres(c,h,%resElem1%)))
               /(PQDres(c,%resElem1%)*(SUM(h,QCDRes(c,h,%resElem1%)) + QGDres(c,%resElem1%)
                       + sum(i,QINVDres(c,i,%resElem1%)) + sum(a,QINTDres(c,a,%resElem1%))))  ;

 nCOMMODSH("stPRIVcomDEM",c,%resElem1%)$SUM((cp,h),PQDres(cp,%resElem1%)* QCDRes(cp,h,%resElem1%))
           = SUM(h,(PQDres(c,%resElem1%)* QCDRes(c,h,%resElem1%)))
               /SUM((cp,h),PQDres(cp,%resElem1%)* QCDRes(cp,h,%resElem1%)) ;

 nCOMMODSH("stGOVTregDEM",c,%resElem1%)$(PQDres(c,%resElem1%)*(SUM(h,QCDRes(c,h,%resElem1%)) + QGDres(c,%resElem1%)
                                          + sum(i,QINVDres(c,i,%resElem1%)) + sum(a,QINTDres(c,a,%resElem1%))))
           = (PQDres(c,%resElem1%)* QGDres(c,%resElem1%))
               /(PQDres(c,%resElem1%)*(SUM(h,QCDRes(c,h,%resElem1%)) + QGDres(c,%resElem1%)
                            + sum(i,QINVDres(c,i,%resElem1%)) + sum(a,QINTDres(c,a,%resElem1%))))  ;

 nCOMMODSH("stGOVTcomDEM",c,%resElem1%)$SUM(cp,PQDres(cp,%resElem1%)* QGDres(cp,%resElem1%))
           = (PQDres(c,%resElem1%)* QGDres(c,%resElem1%))
               /SUM(cp,PQDres(cp,%resElem1%)* QGDres(cp,%resElem1%)) ;

 nCOMMODSH("stINVDregDEM",c,%resElem1%)$(PQDres(c,%resElem1%)*(SUM(h,QCDRes(c,h,%resElem1%)) + QGDres(c,%resElem1%)
                                          + sum(i,QINVDres(c,i,%resElem1%)) + sum(a,QINTDres(c,a,%resElem1%))))
           = (PQDres(c,%resElem1%)* sum(i,QINVDres(c,i,%resElem1%)))
               /(PQDres(c,%resElem1%)*(SUM(h,QCDRes(c,h,%resElem1%)) + QGDres(c,%resElem1%)
                            + sum(i,QINVDres(c,i,%resElem1%)) + sum(a,QINTDres(c,a,%resElem1%))))  ;

 nCOMMODSH("stINVDcomDEM",c,%resElem1%)$SUM(cp,PQDres(cp,%resElem1%)* sum(i,QINVDres(cp,i,%resElem1%)))
           = (PQDres(c,%resElem1%)* sum(i,QINVDres(c,i,%resElem1%)))
               /SUM(cp,PQDres(cp,%resElem1%)* sum(i, QINVDres(cp,i,%resElem1%))) ;

 nCOMMODSH("stINTDregDEM",c,%resElem1%)$(PQDres(c,%resElem1%)*(SUM(h,QCDRes(c,h,%resElem1%)) + QGDres(c,%resElem1%)
                                          + sum(i,QINVDres(c,i,%resElem1%)) + sum(a,QINTDres(c,a,%resElem1%))))
           = (PQDres(c,%resElem1%)* sum(a,QINTDres(c,a,%resElem1%)))
               /(PQDres(c,%resElem1%)*(SUM(h,QCDRes(c,h,%resElem1%)) + QGDres(c,%resElem1%)
                            + sum(i,QINVDres(c,i,%resElem1%)) + sum(a,QINTDres(c,a,%resElem1%))))  ;

 nCOMMODSH("stINTDcomDEM",c,%resElem1%)$SUM(cp,PQDres(cp,%resElem1%)* sum(a,QINTDres(cp,a,%resElem1%)))
           = (PQDres(c,%resElem1%)* sum(a,QINTDres(c,a,%resElem1%)))
               /SUM(cp,PQDres(cp,%resElem1%)* sum(a,QINTDres(cp,a,%resElem1%))) ;

* Supply Structures

 nCOMMODSH("stMAKEcomSUP",c,%resElem1%)$SUM(cp,PXCres(cp,%resElem1%)* QXCres(cp,%resElem1%))
           = (PXCres(c,%resElem1%)* QXCres(c,%resElem1%))
              /SUM(cp,PXCres(cp,%resElem1%)* QXCres(cp,%resElem1%)) ;

 nCOMMODSH("stQMcomSUP",c,%resElem1%)$SUM(cp,PMres(cp,%resElem1%)* QMres(cp,%resElem1%))
           = (PMres(c,%resElem1%)* QMres(c,%resElem1%))
              /SUM(cp,PMres(cp,%resElem1%)* QMres(cp,%resElem1%)) ;

 nCOMMODSH("stQDcomSUP",c,%resElem1%)$SUM(cp,PDres(cp,%resElem1%)* QDres(cp,%resElem1%))
           = (PDres(c,%resElem1%)* QDres(c,%resElem1%))
              /SUM(cp,PDres(cp,%resElem1%)* QDres(cp,%resElem1%)) ;

 nCOMMODSH("stSUPPcomSUP",c,%resElem1%)$SUM(cp,(PDres(cp,%resElem1%)* QDres(cp,%resElem1%))
                                      + (PMres(c,%resElem1%)* QMres(c,%resElem1%)))
           = ((PDres(c,%resElem1%)* QDres(c,%resElem1%))+(PMres(c,%resElem1%)* QMres(c,%resElem1%)))
               /SUM(cp,(PDres(cp,%resElem1%)* QDres(cp,%resElem1%))
                 + (PMres(c,%resElem1%)* QMres(c,%resElem1%))) ;

 nCOMMODSH("stQEconSUP",c,%resElem1%)$SUM(cp,PEres(cp,%resElem1%)* QEres(cp,%resElem1%))
           = (PEres(c,%resElem1%)* QEres(c,%resElem1%))
               /SUM(cp,PEres(cp,%resElem1%)* QEres(cp,%resElem1%)) ;

* --- Activity Tables ---

 nACTIVSH("stQINTQX",a,%resElem1%)$(SUM(ap,PXres(ap,%resElem1%)*QXres(ap,%resElem1%)))
                    = (pINTres(a,%resElem1%)*QINTres(a,%resElem1%))/SUM(ap,PXres(ap,%resElem1%)*QXres(ap,%resElem1%)) ;

 nACTIVSH("stQINT",a,%resElem1%)$(SUM(ap,pINTres(ap,%resElem1%)*QINTres(ap,%resElem1%)))
                    = (pINTres(a,%resElem1%)*QINTres(a,%resElem1%))/SUM(ap,pINTres(ap,%resElem1%)*QINTres(ap,%resElem1%)) ;

 nACTIVSH("stVAQX",a,%resElem1%)$(SUM(ap,PXres(ap,%resElem1%)*QXres(ap,%resElem1%)))
                    = (VVAres(a,%resElem1%))/SUM(ap,PXres(ap,%resElem1%)*QXres(ap,%resElem1%)) ;

 nACTIVSH("stVA",a,%resElem1%)$(SUM(ap,PVAres(ap,%resElem1%)*QVAres(ap,%resElem1%)))
                    = (VVAres(a,%resElem1%))/SUM(ap,VVAres(ap,%resElem1%)) ;

 nACTIVSH("stQX",a,%resElem1%)$(SUM(ap,PXres(ap,%resElem1%)*QXres(ap,%resElem1%)))
                     = (PXres(a,%resElem1%)*QXres(a,%resElem1%))/SUM(ap,PXres(ap,%resElem1%)*QXres(ap,%resElem1%)) ;

 nACTIVSH("stLAB",a,%resElem1%)$(VVAres(a,%resElem1%))
                     = (SUM(l,WFres(l,%resElem1%)*WFDISTres(l,a,%resElem1%)*FDres(l,a,%resElem1%)))
                           /(VVAres(a,%resElem1%)) ;

 nACTIVSH("stUskLAB",a,%resElem1%)$(VVAres(a,%resElem1%))
                    = (SUM(lu,WFres(lu,%resElem1%)*WFDISTres(lu,a,%resElem1%)*FDres(lu,a,%resElem1%)))
                           /(VVAres(a,%resElem1%)) ;

 nACTIVSH("stSkLAB",a,%resElem1%)$(VVAres(a,%resElem1%))
                     = (SUM(ls,WFres(ls,%resElem1%)*WFDISTres(ls,a,%resElem1%)*FDres(ls,a,%resElem1%)))
                           /(VVAres(a,%resElem1%)) ;

 nACTIVSH("stSekLAB",a,%resElem1%)$(VVAres(a,%resElem1%))
                     = (SUM(lm,WFres(lm,%resElem1%)*WFDISTres(lm,a,%resElem1%)*FDres(lm,a,%resElem1%)))
                          /(VVAres(a,%resElem1%)) ;

 nACTIVSH("stCAP",a,%resElem1%)$(VVAres(a,%resElem1%))
                     = (SUM(k,WFres(k,%resElem1%)*WFDISTres(k,a,%resElem1%)*FDres(k,a,%resElem1%)))
                          /(VVAres(a,%resElem1%)) ;

 nACTIVSH("stLND",a,%resElem1%)$(VVAres(a,%resElem1%))
                     = (SUM(n,WFres(n,%resElem1%)*WFDISTres(n,a,%resElem1%)*FDres(n,a,%resElem1%)))
                           /(VVAres(a,%resElem1%)) ;

 nACTIVSH("stFTAX",a,%resElem1%)$(VVAres(a,%resElem1%))
              = (SUM(f,TFres(f,a,%resElem1%)*WFres(f,%resElem1%)*WFDISTres(f,a,%resElem1%)*FDres(f,a,%resElem1%)))
                          /(VVAres(a,%resElem1%)) ;

 nACTIVSH("stFACTchk",a,%resElem1%)
                     = nACTIVSH("stUskLAB",a,%resElem1%) + nACTIVSH("stSkLAB",a,%resElem1%)
                       + nACTIVSH("stCAP",a,%resElem1%) + nACTIVSH("stLND",a,%resElem1%)
                       + nACTIVSH("stFTAX",a,%resElem1%) ;

* --- Factor Tables ---

* Assigning factor tables

 nFACTUSESH("stTRANS",f,a,%resElem1%)
                    = (WFres(f,%resElem1%) * WFDISTres(f,a,%resElem1%) * FDres(f,a,%resElem1%)) ;

 nFACTUSESH("stACTSH",f,a,%resElem1%)$(SUM(fp,nFACTUSESH("stTRANS",fp,a,%resElem1%)))
                    = nFACTUSESH("stTRANS",f,a,%resElem1%)
                         /(SUM(fp,nFACTUSESH("stTRANS",fp,a,%resElem1%))) ;

 nFACTUSESH("stFFSH",f,a,%resElem1%)$(SUM(ap,nFACTUSESH("stTRANS",f,ap,%resElem1%)))
                     = nFACTUSESH("stTRANS",f,a,%resElem1%)
                          /(SUM(ap,nFACTUSESH("stTRANS",f,ap,%resElem1%))) ;

* --- Factor adjustment

 FACTADJ(f,%resElem1%)$FSres(f,%resElem1%)
                   = (SUM(a, ABS(FDres(f,a,%resElem1%)-FD0(f,a)))/2)
                          /FSres(f,%resElem1%) ;

* ---- Aggregate export structure

 EXPORT_TOT(%resElem1%)  = SUM(c,
           PWEres(c,%resElem1%)*QEres(c,%resElem1%)) ;

 EXPORT_DIF(%resElem1%) = EXPORT_TOT(%resElem1%) -
                            EXPORT_TOT(%resElemBs%);
$ontext
 EXPORT_DIF_AGG(wagg,ragg,%resElem1%)
                         = SUM((w)$(MAP_RAGG_R(ragg,r)and MAP_WAGG_W(wagg,w)),
                           (EXPORT_TOT(%resElem1%) -
                            EXPORT_TOT(clos,"base")) );
 EXPORT_TOT_SH(wgn,%resElem1%)$(SUM(wgnp, EXPORT_TOT(wgnp,%resElem1%))) =
            EXPORT_TOT(wgn,%resElem1%)/ SUM(wgnp, EXPORT_TOT(wgnp,%resElem1%));
$offtext

* intermediate aggregation steps to compute export totals over aggregate
* commodity, region and trade partner
* to compute shares of aggregate exports to aggregate non-globe regions
* use the totals and construct shares in EXCEL
* (or define a non-globe subset of rm and wm)

 EXP_CAGG_TOT(cagg,%resElem1%)  = SUM(c$map_cagg_c(cagg,c),
           PWEres(c,%resElem1%)*QEres(c,%resElem1%)) ;

 IMP_CAGG_TOT(cagg,%resElem1%)  = SUM(c$map_cagg_c(cagg,c),
           PWMres(c,%resElem1%)*QMres(c,%resElem1%)) ;

* ---- Aggregate import structure

 IMPORT_TOT(%resElem1%)  = SUM(c,
           PWMres(c,%resElem1%)*QMres(c,%resElem1%)) ;

 EXP_OUTshr(cagg,%resElem1%)$SUM(c$map_cagg_c(cagg,c),(PXCres(C,%resElem1%)*QXCres(C,%resElem1%)))
*SUM(cp,(PXC.L(Cp)*QXC.L(Cp)))
           = SUM(c$map_cagg_c(cagg,c), PEres(C,%resElem1%)*QEres(C,%resElem1%))
             /SUM(c$map_cagg_c(cagg,c),(PXCres(C,%resElem1%)*QXCres(C,%resElem1%)));

 IMP_DEMshr(cagg,%resElem1%)$sum(c$map_cagg_c(cagg,c),(PQSres(C,%resElem1%)*(1 - TSres(C,%resElem1%))*QQRes(C,%resElem1%)))
*SUM(cp,(PQS.L(Cp)*(1 - TS.L(Cp))*QQ.L(Cp)))
          = sum(c$map_cagg_c(cagg,c), PMres(C,%resElem1%)*QMres(C,%resElem1%))
            /sum(c$map_cagg_c(cagg,c),(PQSres(C,%resElem1%)*(1 - TSres(C,%resElem1%))*QQRes(C,%resElem1%)));

$ontext
 IMPORT_TOT_SH(wgn,%resElem1%)$(SUM(wgnp, IMPORT_TOT(wgnp,%resElem1%))) =
            IMPORT_TOT(wgn,%resElem1%)/ SUM(wgnp, IMPORT_TOT(wgnp,%resElem1%));
$offtext

* intermediate aggregation steps to compute import totals over aggregate
* commodity, region and trade partner
* to compute shares of aggregate imports to aggregate non-globe regions
* use the totals and construct shares in EXCEL
* (or define a non-globe subset of rm and wm)

* ---- Total Trade by aggregate commodities and/or regions


* ------- Exporting Structural Tables to GDX -----------------------------

* This writes the results data to GDX

Execute_Unload '%resultF%/%mode%_%exp%_resstruct.gdx'

*                       nIMPORTSH,
*                       nEXPORTSH,
                       nCOMMODSH,
                       nACTIVSH,
                       nFACTUSESH,
                       FACTADJ,
                       EXPORT_TOT,
                       EXPORT_DIF,
*                       EXPORT_DIF_AGG,
*                       EXPORT_TOT_SH,
                       EXP_CAGG_TOT,
                       IMPORT_TOT
*                       IMPORT_TOT_SH
                       IMP_CAGG_TOT
                       EXP_OUTshr
                       IMP_DEMshr
   ;
