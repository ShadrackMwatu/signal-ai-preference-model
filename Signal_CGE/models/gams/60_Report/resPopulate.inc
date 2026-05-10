*------------------------------------------------------------------------------
*------------------------------------------------------------------------------
*-
*-
*-   GAMS file : resassign.inc
*-
*-   @purpose  : Assigns values in result container to individial parameters
*-   @author   :
*-   @date     :
*-   @since    :
*-   @refDoc   :
*-   @seeAlso  :
*-   @calledBy : report.inc
*------------------------------------------------------------------------------
*------------------------------------------------------------------------------


*-#### ASSIGN THE PERCENTAGE CHANGES
 SCALres("sERX",%resElem1%)               = result("%resType%","sERX","NaN","Nan","NaN","NaN",%resElem1%)      ;
 SCALres("sCPI",%resElem1%)               = result("%resType%","sCPI","NaN","Nan","NaN","NaN",%resElem1%)     ;
 SCALres("sPPI",%resElem1%)               = result("%resType%","sPPI","NaN","Nan","NaN","NaN",%resElem1%)     ;
 SCALres("sMTAX",%resElem1%)              = result("%resType%","sMTAX","NaN","Nan","NaN","NaN",%resElem1%)    ;
 SCALres("sETAX",%resElem1%)              = result("%resType%","sETAX","NaN","Nan","NaN","NaN",%resElem1%)    ;
 SCALres("sSTAX",%resElem1%)              = result("%resType%","sSTAX","NaN","Nan","NaN","NaN",%resElem1%)    ;
 SCALres("sEXTAX",%resElem1%)             = result("%resType%","sEXTAX","NaN","Nan","NaN","NaN",%resElem1%)   ;
 SCALres("sVTAX",%resElem1%)              = result("%resType%","sVTAX","NaN","Nan","NaN","NaN",%resElem1%)    ;
 SCALres("sITAX",%resElem1%)              = result("%resType%","sITAX","NaN","Nan","NaN","NaN",%resElem1%)    ;
 SCALres("sITAXA",%resElem1%)             = result("%resType%","sITAXA","NaN","Nan","NaN","NaN",%resElem1%)   ;
 SCALres("sFTAX",%resElem1%)              = result("%resType%","sFTAX","NaN","Nan","NaN","NaN",%resElem1%)    ;
 SCALres("sDTAX",%resElem1%)              = result("%resType%","sDTAX","NaN","Nan","NaN","NaN",%resElem1%)    ;
 SCALres("sFYTAX",%resElem1%)             = result("%resType%","sFYTAX","NaN","Nan","NaN","NaN",%resElem1%)   ;
 SCALres("sINTAX",%resElem1%)             = result("%resType%","sINTAX","NaN","Nan","NaN","NaN",%resElem1%)   ;
 SCALres("sYG",%resElem1%)                = result("%resType%","sYG","NaN","Nan","NaN","NaN",%resElem1%)      ;
 SCALres("sEG",%resElem1%)                = result("%resType%","sEG","NaN","Nan","NaN","NaN",%resElem1%)      ;
 SCALres("sGBUDG",%resElem1%)             = result("%resType%","sGBUDG","NaN","Nan","NaN","NaN",%resElem1%)   ;
 SCALres("sINVEST",%resElem1%)            = result("%resType%","sINVEST","NaN","Nan","NaN","NaN",%resElem1%)  ;
 SCALres("sTOTSAV",%resElem1%)            = result("%resType%","sTOTSAV","NaN","Nan","NaN","NaN",%resElem1%)  ;
 SCALres("sKAPGOV",%resElem1%)            = result("%resType%","sKAPGOV","NaN","Nan","NaN","NaN",%resElem1%)  ;
 SCALres("sKAPWOR",%resElem1%)            = result("%resType%","sKAPWOR","NaN","Nan","NaN","NaN",%resElem1%)  ;
 SCALres("sVFDOMD",%resElem1%)            = result("%resType%","sVFDOMD","NaN","Nan","NaN","NaN",%resElem1%)  ;
 SCALres("sVGD",%resElem1%)               = result("%resType%","sVGD","NaN","Nan","NaN","NaN",%resElem1%)     ;
 SCALres("sINVESTSH",%resElem1%)          = result("%resType%","sINVESTSH","NaN","Nan","NaN","NaN",%resElem1%);
 SCALres("sVGDSH",%resElem1%)             = result("%resType%","sVGDSH","NaN","Nan","NaN","NaN",%resElem1%)   ;
 SCALres("sGDP",%resElem1%)               = result("%resType%","sGDP","NaN","Nan","NaN","NaN",%resElem1%)     ;
 SCALres("sRGDP",%resElem1%)              = result("%resType%","sRGDP","NaN","Nan","NaN","NaN",%resElem1%)    ;
 SCALres("sRGDPFC",%resElem1%)            = result("%resType%","sRGDPFC","NaN","Nan","NaN","NaN",%resElem1%)  ;
 SCALres("sWALRAS",%resElem1%)            = result("%resType%","sWALRAS","NaN","Nan","NaN","NaN",%resElem1%)  ;
 SCALres('MODEL-STAT',%resElem1%)         = result("%resType%",'MODEL-STAT',"NaN","Nan","NaN","NaN",%resElem1%)   ;
 SCALres('SOLVE-STAT',%resElem1%)         = result("%resType%",'SOLVE-STAT',"NaN","Nan","NaN","NaN",%resElem1%)   ;
 SCALres('NUM-REDEFQ',%resElem1%)         = result("%resType%",'NUM-REDEFQ',"NaN","Nan","NaN","NaN",%resElem1%)   ;
 SCALres('iterUsd',%resElem1%)            = result("%resType%",'iterUsd',"NaN","Nan","NaN","NaN",%resElem1%)      ;



 ADJres("aADXADJ",%resElem1%)             = result("%resType%","aADXADJ","NaN","Nan","NaN","NaN",%resElem1%)  ;
 ADJres("aDADX",%resElem1%)               = result("%resType%","aDADX","NaN","Nan","NaN","NaN",%resElem1%)    ;
 ADJres("aADVAADJ",%resElem1%)            = result("%resType%","aADVAADJ","NaN","Nan","NaN","NaN",%resElem1%) ;
 ADJres("aDADVA",%resElem1%)              = result("%resType%","aDADVA","NaN","Nan","NaN","NaN",%resElem1%)   ;
 ADJres("aQEDADJ",%resElem1%)             = result("%resType%","aQEDADJ","NaN","Nan","NaN","NaN",%resElem1%)  ;
 ADJres("aHEADJ",%resElem1%)              = result("%resType%","aHEADJ","NaN","Nan","NaN","NaN",%resElem1%)   ;
 ADJres("aTEADJ",%resElem1%)              = result("%resType%","aTEADJ","NaN","Nan","NaN","NaN",%resElem1%)   ;
 ADJres("aTMADJ",%resElem1%)              = result("%resType%","aTMADJ","NaN","Nan","NaN","NaN",%resElem1%)   ;
 ADJres("aTSADJ",%resElem1%)              = result("%resType%","aTSADJ","NaN","Nan","NaN","NaN",%resElem1%)   ;
 ADJres("aTEXADJ",%resElem1%)             = result("%resType%","aTEXADJ","NaN","Nan","NaN","NaN",%resElem1%)  ;
 ADJres("aTVADJ",%resElem1%)              = result("%resType%","aTVADJ","NaN","Nan","NaN","NaN",%resElem1%)   ;
 ADJres("aTXADJ",%resElem1%)              = result("%resType%","aTXADJ","NaN","Nan","NaN","NaN",%resElem1%)   ;
 ADJres("aTFADJ",%resElem1%)              = result("%resType%","aTFADJ","NaN","Nan","NaN","NaN",%resElem1%)   ;
 ADJres("aTYFADJ",%resElem1%)             = result("%resType%","aTYFADJ","NaN","Nan","NaN","NaN",%resElem1%)  ;
 ADJres("aTYHADJ",%resElem1%)             = result("%resType%","aTYHADJ","NaN","Nan","NaN","NaN",%resElem1%)  ;
 ADJres("aTYADJ",%resElem1%)              = result("%resType%","aTYADJ","NaN","Nan","NaN","NaN",%resElem1%)   ;
 ADJres("aTYEADJ",%resElem1%)             = result("%resType%","aTYEADJ","NaN","Nan","NaN","NaN",%resElem1%)  ;
 ADJres("aTINADJ",%resElem1%)             = result("%resType%","aTINADJ","NaN","Nan","NaN","NaN",%resElem1%)  ;
 ADJres("aTHCADJ",%resElem1%)             = result("%resType%","aTHCADJ","NaN","Nan","NaN","NaN",%resElem1%)  ;
 ADJres("aDTE",%resElem1%)                = result("%resType%","aDTE","NaN","Nan","NaN","NaN",%resElem1%)     ;
 ADJres("aDTM",%resElem1%)                = result("%resType%","aDTM","NaN","Nan","NaN","NaN",%resElem1%)     ;
 ADJres("aDTS",%resElem1%)                = result("%resType%","aDTS","NaN","Nan","NaN","NaN",%resElem1%)     ;
 ADJres("aDTEX",%resElem1%)               = result("%resType%","aDTEX","NaN","Nan","NaN","NaN",%resElem1%)    ;
 ADJres("aDTV",%resElem1%)                = result("%resType%","aDTV","NaN","Nan","NaN","NaN",%resElem1%)     ;
 ADJres("aDTX",%resElem1%)                = result("%resType%","aDTX","NaN","Nan","NaN","NaN",%resElem1%)     ;
 ADJres("aDTXA",%resElem1%)               = result("%resType%","aDTXA","NaN","Nan","NaN","NaN",%resElem1%)    ;
 ADJres("aDTF",%resElem1%)                = result("%resType%","aDTF","NaN","Nan","NaN","NaN",%resElem1%)     ;
 ADJres("aDTYF",%resElem1%)               = result("%resType%","aDTYF","NaN","Nan","NaN","NaN",%resElem1%)    ;
 ADJres("aDTYH",%resElem1%)               = result("%resType%","aDTYH","NaN","Nan","NaN","NaN",%resElem1%)    ;
 ADJres("aDTY",%resElem1%)                = result("%resType%","aDTY","NaN","Nan","NaN","NaN",%resElem1%)     ;
 ADJres("aDTYE",%resElem1%)               = result("%resType%","aDTYE","NaN","Nan","NaN","NaN",%resElem1%)    ;
 ADJres("aDTIN",%resElem1%)               = result("%resType%","aDTIN","NaN","Nan","NaN","NaN",%resElem1%)    ;
 ADJres("aDTHC",%resElem1%)               = result("%resType%","aDTHC","NaN","Nan","NaN","NaN",%resElem1%)    ;
 ADJres("aQGDADJ",%resElem1%)             = result("%resType%","aQGDADJ","NaN","Nan","NaN","NaN",%resElem1%)  ;
 ADJres("aQGDADJceh",%resElem1%)          = result("%resType%","aQGDADJceh","NaN","Nan","NaN","NaN",%resElem1%)  ;
 ADJres("aQGDADJoth",%resElem1%)          = result("%resType%","aQGDADJoth","NaN","Nan","NaN","NaN",%resElem1%)  ;
 ADJres("aQGDADJext",%resElem1%)          = result("%resType%","aQGDADJext","NaN","Nan","NaN","NaN",%resElem1%)  ;
 ADJres("aHGADJ",%resElem1%)              = result("%resType%","aHGADJ","NaN","Nan","NaN","NaN",%resElem1%)   ;
 ADJres("aDHOGOV",%resElem1%)             = result("%resType%","aDHOGOV","NaN","Nan","NaN","NaN",%resElem1%) ;
 ADJres("aEGADJ",%resElem1%)              = result("%resType%","aEGADJ","NaN","Nan","NaN","NaN",%resElem1%)   ;
 ADJres("aSADJ",%resElem1%)               = result("%resType%","aSADJ","NaN","Nan","NaN","NaN",%resElem1%)    ;
 ADJres("aSHADJ",%resElem1%)              = result("%resType%","aSHADJ","NaN","Nan","NaN","NaN",%resElem1%)   ;
 ADJres("aSEADJ",%resElem1%)              = result("%resType%","aSEADJ","NaN","Nan","NaN","NaN",%resElem1%)   ;
 ADJres("aDSHH",%resElem1%)               = result("%resType%","aDSHH","NaN","Nan","NaN","NaN",%resElem1%)    ;
 ADJres("aDS",%resElem1%)                 = result("%resType%","aDS","NaN","Nan","NaN","NaN",%resElem1%)      ;
 ADJres("aDSEN",%resElem1%)               = result("%resType%","aDSEN","NaN","Nan","NaN","NaN",%resElem1%)    ;
 ADJres("aIADJ",%resElem1%)               = result("%resType%","aIADJ","NaN","Nan","NaN","NaN",%resElem1%)    ;

 QGDADJcres(cc,%resElem1%)                = result("%resType%","QGDADJc",cc,"Nan","NaN","NaN",%resElem1%)     ;
 ERres(w,%resElem1%)                      = result("%resType%","sER",w,"Nan","NaN","NaN",%resElem1%)          ;
 KAPREGres(w,%resElem1%)                  = result("%resType%","sKAPREG",w,"Nan","NaN","NaN",%resElem1%)      ;
 PWEres(cc,%resElem1%)                    = result("%resType%","PWE",cc,"NaN","NaN","NaN",%resElem1%)         ;
 PWSEres(cc,%resElem1%)                   = result("%resType%","PWSE",cc,"NaN","NaN","NaN",%resElem1%)        ;
 PEres(cc,%resElem1%)                     = result("%resType%","PE",cc,"NaN","NaN","NaN",%resElem1%)          ;
 COMTOTSHres(cc,%resElem1%)               = result("%resType%","COMTOTSH",cc,"NaN","NaN","NaN",%resElem1%)    ;
 VQCDres(cc,%resElem1%)                   = result("%resType%","VQCD",cc,"NaN","NaN","NaN",%resElem1%)        ;
 PERres(cc,w,%resElem1%)                  = result("%resType%","PER",cc,w,"NaN","NaN",%resElem1%)             ;
 PDres(cc,%resElem1%)                     = result("%resType%","PD",cc,"NaN","NaN","NaN",%resElem1%)          ;
 QEres(cc,%resElem1%)                     = result("%resType%","QE",cc,"NaN","NaN","NaN",%resElem1%)          ;
 QERres(cc,w,%resElem1%)                  = result("%resType%","QER",cc,w,"NaN","NaN",%resElem1%)             ;
 QDres(cc,%resElem1%)                     = result("%resType%","QD",cc,"NaN","NaN","NaN",%resElem1%)          ;
 PWMres(cc,%resElem1%)                    = result("%resType%","PWM",cc,"NaN","NaN","NaN",%resElem1%)         ;
 PMres(cc,%resElem1%)                     = result("%resType%","PM",cc,"NaN","NaN","NaN",%resElem1%)          ;
 PMRres(w,cc,%resElem1%)                  = result("%resType%","PMR",w,cc,"NaN","NaN",%resElem1%)             ;
 QMres(cc,%resElem1%)                     = result("%resType%","QM",cc,"NaN","NaN","NaN",%resElem1%)          ;
 QMRres(w,cc,%resElem1%)                  = result("%resType%","QMR",w,cc,"NaN","NaN",%resElem1%)             ;
 QQres(cc,%resElem1%)                     = result("%resType%","QQ",cc,"NaN","NaN","NaN",%resElem1%)          ;
 PTTres(m,%resElem1%)                     = result("%resType%","PTT",m,"NaN","NaN","NaN",%resElem1%)          ;
 IOQTTQQres(m,c,%resElem1%)               = result("%resType%","IOQTTQQ",m,c,"NaN","NaN",%resElem1%)          ;
 QTTres(m,%resElem1%)                     = result("%resType%","QTT",m,"NaN","NaN","NaN",%resElem1%)          ;
 QTTDres(cc,%resElem1%)                   = result("%resType%","QTTD",cc,"NaN","NaN","NaN",%resElem1%)        ;
 PQSres(cc,%resElem1%)                    = result("%resType%","PQS",cc,"NaN","NaN","NaN",%resElem1%)         ;
 PQDres(cc,%resElem1%)                    = result("%resType%","PQD",cc,"NaN","NaN","NaN",%resElem1%)         ;
 PQCDres(cc,h,%resElem1%)                 = result("%resType%","PQCD",cc,h,"NaN","NaN",%resElem1%)            ;
 PQCres(cc,h,%resElem1%)                  = result("%resType%","PQC",cc,h,"NaN","NaN",%resElem1%)            ;

 PXres(a,%resElem1%)                      = result("%resType%","PX",a,"NaN","NaN","NaN",%resElem1%)           ;
 PVAres(a,%resElem1%)                     = result("%resType%","PVA",a,"NaN","NaN","NaN",%resElem1%)          ;
 PINTres(a,%resElem1%)                    = result("%resType%","PINT",a,"NaN","NaN","NaN",%resElem1%)         ;
 ADXres(a,%resElem1%)                     = result("%resType%","ADX",a,"NaN","NaN","NaN",%resElem1%)          ;
 ADres(ff,a,%resElem1%)                   = result("%resType%","AD",ff,a,"NaN","NaN",%resElem1%)              ;
 ADFDres(ff,a,%resElem1%)                 = result("%resType%","ADFD",ff,a,"NaN","NaN",%resElem1%)            ;
 ADFHres(ff,h,%resElem1%)                 = result("%resType%","ADFH",ff,h,"NaN","NaN",%resElem1%)            ;
 QXres(a,%resElem1%)                      = result("%resType%","QX",a,"NaN","NaN","NaN",%resElem1%)           ;
 QVAres(a,%resElem1%)                     = result("%resType%","QVA",a,"NaN","NaN","NaN",%resElem1%)          ;
 VVAres(a,%resElem1%)                     = result("%resType%","VVA",a,"NaN","NaN","NaN",%resElem1%)          ;
 QINTres(a,%resElem1%)                    = result("%resType%","QINT",a,"NaN","NaN","NaN",%resElem1%)         ;
 ADVAres(a,%resElem1%)                    = result("%resType%","ADVA",a,"NaN","NaN","NaN",%resElem1%)         ;
 WFres(ff,%resElem1%)                     = result("%resType%","WF",ff,"NaN","NaN","NaN",%resElem1%)          ;
 WFDISTres(ff,a,%resElem1%)               = result("%resType%","WFDIST",ff,a,"NaN","NaN",%resElem1%)          ;
 WFAres(ff,a,%resElem1%)                  = result("%resType%","WFA",ff,a,"NaN","NaN",%resElem1%)             ;
 PQDDISTres(cc,a,%resElem1%)              = result("%resType%","PQDDIST",cc,a,"NaN","NaN",%resElem1%)         ;
 FDres(ff,a,%resElem1%)                   = result("%resType%","FD",ff,a,"NaN","NaN",%resElem1%)              ;
 FSres(ff,%resElem1%)                     = result("%resType%","FS",ff,"NaN","NaN","NaN",%resElem1%)          ;
 UNEMPres(ff,%resElem1%)                  = result("%resType%","UNEMP",ff,"NaN","NaN","NaN",%resElem1%)          ;
 UNEMPRATEres(ff,%resElem1%)              = result("%resType%","UNEMPRATE",ff,"NaN","NaN","NaN",%resElem1%)          ;
 FSIres(insw,ff,%resElem1%)               = result("%resType%","FSI",insw,ff,"NaN","NaN",%resElem1%)          ;
 FSILres(insw,ff,%resElem1%)              = result("%resType%","FSIL",insw,ff,"NaN","NaN",%resElem1%)         ;
 FSIMres(ff,insw,ffp,inswp,%resElem1%)    = result("%resType%","FSIM",ff,insw,ffp,inswp,%resElem1%)           ;
 MIGCONSres(ff,h,ffp,hp,%resElem1%)= result("%resType%","MIGCONS",ff,h,ffp,hp,%resElem1%)           ;
 SHMIGres(ff,h,ffp,hp,%resElem1%)= result("%resType%","SHMIG",ff,h,ffp,hp,%resElem1%)           ;
 URBNRATEres(%resElem1%)= result("%resType%","URBNRATE","NaN","NaN","NaN","NaN",%resElem1%)           ;

 FMIGDRVres(f,fp,%resElem1%)              = result("%resType%","FMIGDRV",f,fp,"NaN","NaN",%resElem1%)             ;
 HMIGDRVres(ins,insp,%resElem1%)          = result("%resType%","HMIGDRV",ins,insp,"NaN","NaN",%resElem1%)         ;
 PMIGDRVres(ins,insp,%resElem1%)          = result("%resType%","PMIGDRV",ins,insp,"NaN","NaN",%resElem1%)         ;


 QINTDres(cc,a,%resElem1%)                = result("%resType%","QINTD",cc,a,"NaN","NaN",%resElem1%)           ;
 PXCres(cc,%resElem1%)                    = result("%resType%","PXC",cc,"NaN","NaN","NaN",%resElem1%)         ;
 QXCres(cc,%resElem1%)                    = result("%resType%","QXC",cc,"NaN","NaN","NaN",%resElem1%)         ;
 IOQXACQXVres(a,cc,%resElem1%)            = result("%resType%","IOQXACQXV",a,cc,"NaN","NaN",%resElem1%)       ;
 PXACres(a,cc,%resElem1%)                 = result("%resType%","PXAC",a,cc,"NaN","NaN",%resElem1%)            ;
 QXACres(a,cc,%resElem1%)                 = result("%resType%","QXAC",a,cc,"NaN","NaN",%resElem1%)            ;
 YFres(ff,%resElem1%)                     = result("%resType%","YF",ff,"NaN","NaN","NaN",%resElem1%)          ;
 YFDISPres(ff,%resElem1%)                 = result("%resType%","YFDISP",ff,"NaN","NaN","NaN",%resElem1%)      ;
 YFINSres(ff,%resElem1%)                  = result("%resType%","YFINS",ff,"NaN","NaN","NaN",%resElem1%)       ;
 FSISHres(insw,ff,%resElem1%)             = result("%resType%","FSISH",insw,ff,"NaN","NaN",%resElem1%)        ;
 INSVAres(insw,ff,%resElem1%)             = result("%resType%","INSVA",insw,ff,"NaN","NaN",%resElem1%)        ;
 YHres(h,%resElem1%)                      = result("%resType%","YH",h,"NaN","NaN","NaN",%resElem1%)           ;
 HOGOVRes(h,%resElem1%)                   = result("%resType%","HOGOV",h,"NaN","NaN","NaN",%resElem1%)           ;
 HOHOres(h,hp,%resElem1%)                 = result("%resType%","HOHO",h,hp,"NaN","NaN",%resElem1%)            ;
 HOWORres(h,w,%resElem1%)                 = result("%resType%","HOWOR",h,w,"NaN","NaN",%resElem1%)            ;
 HEXPres(h,%resElem1%)                    = result("%resType%","HEXP",h,"NaN","NaN","NaN",%resElem1%)         ;
 QCDres(cc,h,%resElem1%)                  = result("%resType%","QCD",cc,h,"NaN","NaN",%resElem1%)             ;
 QCD2res(cc,ccp,h,%resElem1%)             = result("%resType%","QCD2",cc,ccp,h,"NaN",%resElem1%)              ;
 QCDTotalres(cc,h,%resElem1%)             = result("%resType%","QCDTotal",cc,"NaN",h,"NaN",%resElem1%)        ;
 YMIGRres(insw,inswp,%resElem1%)          = result("%resType%","YMIGR",insw,inswp,"NaN","NaN",%resElem1%)     ;
 WMIGRres(ff,ffp,insw,%resElem1%)         = result("%resType%","WMIGR",ff,ffp,"Nan","Nan",%resElem1%)         ;
 YEres(e,%resElem1%)                      = result("%resType%","YE",e,"NaN","NaN","NaN",%resElem1%)           ;
 HOENTres(h,e,%resElem1%)                 = result("%resType%","HOENT",h,e,"NaN","NaN",%resElem1%)            ;
 GOVENTres(e,%resElem1%)                  = result("%resType%","GOVENT",e,"NaN","NaN","NaN",%resElem1%)       ;
 QEDres(cc,e,%resElem1%)                  = result("%resType%","QED",cc,e,"NaN","NaN",%resElem1%)             ;
 VEDres(e,%resElem1%)                     = result("%resType%","VED",e,"NaN","NaN","NaN",%resElem1%)          ;
 TEres(cc,w,%resElem1%)                   = result("%resType%","TE",cc,w,"NaN","NaN",%resElem1%)              ;
 TMres(w,cc,%resElem1%)                   = result("%resType%","TM",w,cc,"NaN","NaN",%resElem1%)              ;
 TSres(cc,%resElem1%)                     = result("%resType%","TS",cc,"NaN","NaN","NaN",%resElem1%)          ;
 TVres(cc,%resElem1%)                     = result("%resType%","TV",cc,"NaN","NaN","NaN",%resElem1%)          ;
 TEXres(cc,%resElem1%)                    = result("%resType%","TEX",cc,"NaN","NaN","NaN",%resElem1%)         ;
 TXres(a,%resElem1%)                      = result("%resType%","TX",a,"NaN","NaN","NaN",%resElem1%)           ;
 TXAres(a,%resElem1%)                     = result("%resType%","TXA",a,"NaN","NaN","NaN",%resElem1%)          ;
 TFres(ff,a,%resElem1%)                   = result("%resType%","TF",ff,a,"NaN","NaN",%resElem1%)              ;
 TYFres(ff,%resElem1%)                    = result("%resType%","TYF",ff,"NaN","NaN","NaN",%resElem1%)         ;
 TYHres(h,%resElem1%)                     = result("%resType%","TYH",h,"NaN","NaN","NaN",%resElem1%)          ;
 TYEres(e,%resElem1%)                     = result("%resType%","TYE",e,"NaN","NaN","NaN",%resElem1%)          ;
 TINres(a,%resElem1%)                     = result("%resType%","TIN",a,"NaN","NaN","NaN",%resElem1%)          ;
 THCres(h,c,%resElem1%)                   = result("%resType%","THC",h,c,"NaN","NaN",%resElem1%)          ;
 QGDres(cc,%resElem1%)                    = result("%resType%","QGD",cc,"NaN","NaN","NaN",%resElem1%)         ;
 SHHres(h,%resElem1%)                     = result("%resType%","SHH",h,"NaN","NaN","NaN",%resElem1%)          ;
 SENres(e,%resElem1%)                     = result("%resType%","SEN",e,"NaN","NaN","NaN",%resElem1%)          ;
 QINVDres(cc,i,%resElem1%)                = result("%resType%","QINVD",cc,i,"NaN","NaN",%resElem1%)           ;
 QINVres(i,%resElem1%)                    = result("%resType%","QINV",i,"NaN","NaN","NaN",%resElem1%)         ;
 INVSH_Ires(i,%resElem1%)                 = result("%resType%","INVSH_I",i,"NaN","NaN","NaN",%resElem1%)      ;
 YFWORres(ff,%resElem1%)                  = result("%resType%","YFWOR",ff,"NaN","NaN","NaN",%resElem1%)       ;
 VEDSHres(e,%resElem1%)                   = result("%resType%","VEDSH",e,"NaN","NaN","NaN",%resElem1%)        ;

 EXTENSres(ff,a,%resElem1%)               = result("%resType%","EXTENS",ff,a,"NaN","NaN",%resElem1%)    ;
 ADFExtres(ff,a,%resElem1%)               = result("%resType%","ADFExt",ff,a,"NaN","NaN",%resElem1%)    ;
 EDUCres(h,%resElem1%)                    = result("%resType%","EDUC",h,"NaN","NaN","NaN",%resElem1%)     ;
 HEALres(h,%resElem1%)                    = result("%resType%","HEAL",h,"NaN","NaN","NaN",%resElem1%)     ;
 BRATEres(h,%resElem1%)                   = result("%resType%","BRATE",h,"NaN","NaN","NaN",%resElem1%)    ;
 DRATEres(h,%resElem1%)                   = result("%resType%","DRATE",h,"NaN","NaN","NaN",%resElem1%)    ;
 DEATHres(h,%resElem1%)                   = result("%resType%","DEATH",h,"NaN","NaN","NaN",%resElem1%)    ;
 BIRTHres(h,%resElem1%)                   = result("%resType%","BIRTH",h,"NaN","NaN","NaN",%resElem1%)    ;
 POPNres(h,%resElem1%)                    = result("%resType%","POPN",h,"NaN","NaN","NaN",%resElem1%)     ;
 POPCHNGres(h,%resElem1%)                 = result("%resType%","POPCHNG",h,"NaN","NaN","NaN",%resElem1%)  ;

 AgBuRecurrres(c,%resElem1%)              = result("%resType%","AgBuRecurr",c,"NaN","NaN","NaN",%resElem1%)   ;
 AgBuInvestres(i,%resElem1%)              = result("%resType%","AgBuInvest",i,"NaN","NaN","NaN",%resElem1%)   ;
 AgBuInpSubres(ff,a,%resElem1%)           = result("%resType%","AgBuInpSub",ff,a,"NaN","NaN",%resElem1%)      ;
 AgBuRevFundres(ff,a,%resElem1%)          = result("%resType%","AgBuRevFund",ff,a,"NaN","NaN",%resElem1%)      ;
 AgBuOutSubres(a,%resElem1%)              = result("%resType%","AgBuOutSub",a,"NaN","NaN","NaN",%resElem1%)   ;
 AgBuComSubres(c,h,%resElem1%)            = result("%resType%","AgBuComSub",c,h,"NaN","NaN",%resElem1%)       ;
 AgBuIncSubres(h,%resElem1%)              = result("%resType%","AgBuIncSub",h,"NaN","NaN","NaN",%resElem1%)   ;

 AgBuTotres("Recurr",%resElem1%)          = result("%resType%","AgBuTotRecurr","NaN","NaN","NaN","NaN",%resElem1%)  ;
 AgBuTotres("Invest",%resElem1%)          = result("%resType%","AgBuTotInvest","NaN","NaN","NaN","NaN",%resElem1%)  ;
 AgBuTotres("InpSub",%resElem1%)          = result("%resType%","AgBuTotInpSub","NaN","NaN","NaN","NaN",%resElem1%)  ;
 AgBuTotres("OutSub",%resElem1%)          = result("%resType%","AgBuTotOutSub","NaN","NaN","NaN","NaN",%resElem1%)  ;
 AgBuTotres("ComSub",%resElem1%)          = result("%resType%","AgBuTotComSub","NaN","NaN","NaN","NaN",%resElem1%)  ;
 AgBuTotres("IncSub",%resElem1%)          = sum(h, result("%resType%","AgBuTotIncSub","NaN","NaN","NaN","NaN",%resElem1%))  ;
 AgBuTotres("Total",%resElem1%)           = result("%resType%","AgBuTotalx","NaN","NaN","NaN","NaN",%resElem1%)     ;
 AgBuTotres("Share",%resElem1%)           = result("%resType%","AgBuTotShr","NaN","NaN","NaN","NaN",%resElem1%)     ;

*-Nutrition values

 NutValRes(nutElem,h,%reselem1%)          = result("%resType%","NutVal",nutElem,h,"NaN","NaN",%resElem1%)              ;

*-SDG Indicators
 g01UtilPCRes(h,%resElem1%)          = sdgResult("%resType%","g01","UtilPC",h,"NaN",%resElem1%)                    ;
 g01WageCerRtRes(%resElem1%)         = sdgResult("%resType%","g01","WageCerRt","NaN","NaN",%resElem1%)             ;
 g02TFPRes(%resElem1%)               = sdgResult("%resType%","g02","TFP","NaN","NaN",%resElem1%)                   ;
 g02TMAvRes(%resElem1%)              = sdgResult("%resType%","g02","TMAv","NaN","NaN",%resElem1%)                  ;
 g02FdProdIndRes(%resElem1%)         = sdgResult("%resType%","g02","FdProdInd","NaN","NaN",%resElem1%)             ;
 g02FdFsProdIndRes(%resElem1%)       = sdgResult("%resType%","g02","FdFsProdInd","NaN","NaN",%resElem1%)           ;
 g02FdimpRes(%resElem1%)             = sdgResult("%resType%","g02","Fdimp","NaN","NaN",%resElem1%)                 ;
 g02FdexpRes(%resElem1%)             = sdgResult("%resType%","g02","Fdexp","NaN","NaN",%resElem1%)                 ;
 g02NutPCRes(nutElem,h,%resElem1%)   = sdgResult("%resType%","g02","NutPC",nutElem,h,%resElem1%)                   ;
 g02CalCerShRes(h,%resElem1%)        = sdgResult("%resType%","g02","CalCerSh",h,"NaN",%resElem1%)                  ;
 g02ProLvsFsRes(h,%resElem1%)        = sdgResult("%resType%","g02","ProLvsFs",h,"NaN",%resElem1%)                  ;
 g02ProLvsRes(h,%resElem1%)          = sdgResult("%resType%","g02","ProLvs",h,"NaN",%resElem1%)                    ;
 g02YDAvRes(h,%resElem1%)            = sdgResult("%resType%","g02","YDAv",h,"NaN",%resElem1%)                      ;
 g02FdPriIndRes(h,%resElem1%)        = sdgResult("%resType%","g02","FdPriInd",h,"NaN",%resElem1%)                  ;
 g02FdYDShRes(h,%resElem1%)          = sdgResult("%resType%","g02","FdYDSh",h,"NaN",%resElem1%)                    ;
 g02FdConsRes(h,%resElem1%)          = sdgResult("%resType%","g02","FdCons",h,"NaN",%resElem1%)                    ;
 g02FdConsPCRes(h,%resElem1%)        = sdgResult("%resType%","g02","FdConsPC",h,"NaN",%resElem1%)                  ;
 g02CalFrVShRes(h,%resElem1%)        = sdgResult("%resType%","g02","CalFrVSh",h,"NaN",%resElem1%)                  ;
 g02TMIndRes(%resElem1%)             = sdgResult("%resType%","g02","TMInd","NaN","NaN",%resElem1%)                 ;
 g02ExpSubIndRes(%resElem1%)         = sdgResult("%resType%","g02","ExpSubInd","NaN","NaN",%resElem1%)             ;
 g02TFPRes(%resElem1%)               = sdgResult("%resType%","g02","TFP","NaN","NaN",%resElem1%)                   ;
 g06WatUseRes(%resElem1%)            = sdgResult("%resType%","g06","WatUse","NaN","NaN",%resElem1%)                ;
 g07EnerPrimRes(%resElem1%)          = sdgResult("%resType%","g07","EnerPrim","NaN","NaN",%resElem1%)              ;
 g07EnerClnShRes(%resElem1%)         = sdgResult("%resType%","g07","EnerClnSh","NaN","NaN",%resElem1%)             ;
 g07EnerProdRes(%resElem1%)          = sdgResult("%resType%","g07","EnerProd","NaN","NaN",%resElem1%)              ;
 g07EnerSfSuRes(%resElem1%)          = sdgResult("%resType%","g07","EnerSfSu","NaN","NaN",%resElem1%)              ;
 g07EnerPriIndRes(c,%resElem1%)      = sdgResult("%resType%","g07","EnerPriInd",c,"NaN",%resElem1%)                ;
 g07FosCompRes(%resElem1%)           = sdgResult("%resType%","g07","FosComp","NaN","NaN",%resElem1%)               ;
 g07RenCompRes(%resElem1%)           = sdgResult("%resType%","g07","RenComp","NaN","NaN",%resElem1%)               ;
 g07FosRenRtRes(%resElem1%)          = sdgResult("%resType%","g07","FosRenRt","NaN","NaN",%resElem1%)              ;
 g07EnerSecRes(%resElem1%)           = sdgResult("%resType%","g07","EnerSec","NaN","NaN",%resElem1%)               ;
 g07EnerVaRtRes(a,%resElem1%)        = sdgResult("%resType%","g07","EnerVaRt",a,"NaN",%resElem1%)                  ;
 g07EnerPrimStkRes(enEl1,%resElem1%) = sdgResult("%resType%","g07","EnerPrimStk",enEl1,"NaN",%resElem1%)           ;
 g07EnerRefnRes(%resElem1%)          = sdgResult("%resType%","g07","EnerRefn","NaN","NaN",%resElem1%)              ;
 g07EnerUseRes(enEl2,%resElem1%)     = sdgResult("%resType%","g07","EnerUse",enEl2,"NaN",%resElem1%)               ;
 g07PrimGdpRtRes(enEl1,%resElem1%)   = sdgResult("%resType%","g07","PrimGdpRt",enEl1,"NaN",%resElem1%)             ;
 g07RefnGdpRtRes(%resElem1%)         = sdgResult("%resType%","g07","RefnGdpRt","NaN","NaN",%resElem1%)             ;
 g07UseGdpRtRes(enEl2,%resElem1%)    = sdgResult("%resType%","g07","UseGdpRt",enEl2,"NaN",%resElem1%)              ;
 g07RefnPrimRtRes(%resElem1%)        = sdgResult("%resType%","g07","RefnPrimRt","NaN","NaN",%resElem1%)            ;
 g07UsePrimRtRes(enEl2,%resElem1%)   = sdgResult("%resType%","g07","UsePrimRt",enEl2,"NaN",%resElem1%)             ;
 g08GDPPCGrRes(%resElem1%)           = sdgResult("%resType%","g08","GDPPCGr","NaN","NaN",%resElem1%)               ;
 g08NetTradeRes(%resElem1%)          = sdgResult("%resType%","g08","NetTrade","NaN","NaN",%resElem1%)              ;
 g08RevCompRes(c,%resElem1%)         = sdgResult("%resType%","g08","RevComp",c,"NaN",%resElem1%)                   ;
 g08FosGDPShRes(%resElem1%)          = sdgResult("%resType%","g08","FosGDPSh","NaN","NaN",%resElem1%)              ;
 g09ManVaShRes(%resElem1%)           = sdgResult("%resType%","g09","ManVaSh","NaN","NaN",%resElem1%)               ;
 g09ManVaPCRes(%resElem1%)           = sdgResult("%resType%","g09","ManVaPC","NaN","NaN",%resElem1%)               ;
 g08ManEmpShRes(%resElem1%)          = sdgResult("%resType%","g08","ManEmpSh","NaN","NaN",%resElem1%)              ;
 g08ExpRes(%resElem1%)               = sdgResult("%resType%","g08","Exp","NaN","NaN",%resElem1%)                   ;
 g08ImpRes(%resElem1%)               = sdgResult("%resType%","g08","Imp","NaN","NaN",%resElem1%)                   ;
 g08OpenRes(%resElem1%)              = sdgResult("%resType%","g08","Open","NaN","NaN",%resElem1%)                  ;
 g10LabShRes(%resElem1%)             = sdgResult("%resType%","g10","LabSh","NaN","NaN",%resElem1%)                 ;
 g10AgrEmpRes(%resElem1%)            = sdgResult("%resType%","g10","AgrEmp","NaN","NaN",%resElem1%)                ;
 g10AgrEmpShRes(%resElem1%)          = sdgResult("%resType%","g10","AgrEmpSh","NaN","NaN",%resElem1%)              ;
 g10SkilRes(%resElem1%)              = sdgResult("%resType%","g10","Skil","NaN","NaN",%resElem1%)                  ;
 g10WageDifSklRes(%resElem1%)        = sdgResult("%resType%","g10","WageDifSkl","NaN","NaN",%resElem1%)            ;
 g10WageDifAgrRes(%resElem1%)        = sdgResult("%resType%","g10","WageDifAgr","NaN","NaN",%resElem1%)            ;
 g10IncDiffHHRes(h,hp,%resElem1%)    = sdgResult("%resType%","g10","IncDiffHH",h,hp,%resElem1%)                    ;
 g12RenShRes(%resElem1%)             = sdgResult("%resType%","g12","RenSh","NaN","NaN",%resElem1%)                 ;
 g13RenShRes(%resElem1%)             = sdgResult("%resType%","g13","RenSh","NaN","NaN",%resElem1%)                 ;
 g14FsShRes(%resElem1%)              = sdgResult("%resType%","g14","FsSh","NaN","NaN",%resElem1%)                  ;
 g15NonAgriRes(%resElem1%)           = sdgResult("%resType%","g15","NonAgri","NaN","NaN",%resElem1%)               ;
 g17GDPPcRes(%resElem1%)             = sdgResult("%resType%","g17","GDPPc","NaN","NaN",%resElem1%)                 ;
 g17EGShRes(egEl,%resElem1%)         = sdgResult("%resType%","g17","EGSh",egEl,"NaN",%resElem1%)                   ;


 CO2EM_Qres(c,a,%resElem1%)         = result("%resType%","CO2EM_Q",c,a,"NaN","NaN",%resElem1%)          ;
 CO2EM_Hres(c,h,%resElem1%)         = result("%resType%","CO2EM_H",c,h,"NaN","NaN",%resElem1%)          ;
 CO2EMIS_Qres(a,%resElem1%)         = result("%resType%","CO2EMIS_Q",a,"NaN","NaN","NaN",%resElem1%)    ;
 CO2EMIS_Hres(h,%resElem1%)         = result("%resType%","CO2EMIS_H",h,"NaN","NaN","NaN",%resElem1%)    ;
 CO2EMISres(%resElem1%)             = result("%resType%","CO2EMIS","NaN","NaN","NaN","NaN",%resElem1%)  ;
 NCO2EM_Qres(ghg,a,%resElem1%)      = result("%resType%","NCO2EM_Q",ghg,a,"NaN","NaN",%resElem1%)       ;
 NCO2EM_FSres(ghg,c,a,%resElem1%)   = result("%resType%","NCO2EM_FS",ghg,c,a,"NaN",%resElem1%)          ; 
 NCO2EM_IOres(ghg,c,a,%resElem1%)   = result("%resType%","NCO2EM_IO",ghg,c,a,"NaN",%resElem1%)          ;
 NCO2EM_ENres(ghg,f,a,%resElem1%)   = result("%resType%","NCO2EM_EN",ghg,f,a,"NaN",%resElem1%)          ;
 NCO2EM_Hres(ghg,c,h,%resElem1%)    = result("%resType%","NCO2EM_H",ghg,c,h,"NaN",%resElem1%)           ;
 NCO2EM_A_SUMres(ghg,a,%resElem1%)  = result("%resType%","NCO2EM_A_SUM",ghg,a,"NaN","NaN",%resElem1%)   ;
 NCO2EM_SUMres(ghg,%resElem1%)      = result("%resType%","NCO2EM_SUM",ghg,"NaN","NaN","NaN",%resElem1%) ;
 NCO2EM_FS_SUMres(ghg,a,%resElem1%) = result("%resType%","NCO2EM_FS_SUM",ghg,a,"NaN","NaN",%resElem1%)  ;
 NCO2EM_IO_SUMres(ghg,a,%resElem1%) = result("%resType%","NCO2EM_IO_SUM",ghg,a,"NaN","NaN",%resElem1%)  ;
 NCO2EM_EN_SUMres(ghg,a,%resElem1%) = result("%resType%","NCO2EM_EN_SUM",ghg,a,"NaN","NaN",%resElem1%)  ;
 NCO2EM_H_SUMres(ghg,h,%resElem1%)  = result("%resType%","NCO2EM_H_SUM",ghg,h,"NaN","NaN",%resElem1%)   ;
 NCO2EM_SUMres(NCO,%resElem1%)      = result("%resType%","NCO2EM_SUM",NCO,"NaN","NaN","NaN",%resElem1%) ;
  
$ontext 
 GHGres("Households",c,h,"NaN","Combustion","CO2",%resElem1%)                           =   CO2EM_Hres(c,h,%resElem1%)          ;
 GHGres("Households","Total",h,"NaN","Combustion","CO2",%resElem1%)                     =   CO2EMIS_Hres(h,%resElem1%)          ;

 GHGres("Households",c,h,"NaN","Non-combustion-all-exclLULUCF",GHG,%resElem1%)          =   NCO2EM_Hres(ghg,c,h,%resElem1%)     ;
 GHGres("Households","Total",h,"NaN","Non-combustion-all-exclLULUCF",GHG,%resElem1%)    =   NCO2EM_H_SUMres(ghg,h,%resElem1%)   ;

 GHGres("Activities",c,a,"Intermediate","Combustion","CO2",%resElem1%)                  =   CO2EM_Qres(c,a,%resElem1%)          ;
 GHGres("Activities","Total",a,"NaN","Combustion","CO2",%resElem1%)                     =   CO2EMIS_Qres(a,%resElem1%)          ;

 GHGres("Activities","NaN",a,"Output","Non-combustion-process",GHG,%resElem1%)          =   NCO2EM_Qres(ghg,a,%resElem1%)       ;
       
 GHGres("Activities",c,a,"Intermediate","Non-combustion-process",GHG,%resElem1%)        =   NCO2EM_FSres(ghg,c,a,%resElem1%)    ;  
 GHGres("Activities","Total",a,"Intermediate","Non-combustion-process",GHG,%resElem1%)  =   NCO2EM_IO_SUMres(ghg,a,%resElem1%)  ;

 GHGres("Activities",c,a,"Intermediate","Non-combustion-fossil",GHG,%resElem1%)         =   NCO2EM_IOres(ghg,c,a,%resElem1%)    ;          
 GHGres("Activities","Total",a,"Intermediate","Non-combustion-fossil",GHG,%resElem1%)   =   NCO2EM_FS_SUMres(ghg,a,%resElem1%)  ;          
 
 GHGres("Activities",f,a,"Endowment","Non-combustion-process",GHG,%resElem1%)           =   NCO2EM_ENres(ghg,f,a,%resElem1%)    ;          
 GHGres("Activities","Total",a,"Endowment","Non-combustion-process",GHG,%resElem1%)     =   NCO2EM_EN_SUMres(ghg,a,%resElem1%)  ;          


 GHGres("Total","Total","NaN","Total","Combustion","CO2",%resElem1%)                    =   CO2EMISres(%resElem1%)              ;          
 GHGres("Total","Total","NaN","Total","Non-combustion-all-exclLULUCF",GHG,%resElem1%)   =   NCO2EM_SUMres(GHG,%resElem1%)       ;          

 GHGres("Total","Total","NaN","Total","Total","CO2eq",%resElem1%)                       =   GHGEMres(%resElem1%)                ;          
$offtext

*################## EXPORT OF RESULT FILES TO GDX ###################

* This writes the results data to GDX

Execute_Unload  '%resultF%/%mode%_%exp%_res%resType%.gdx',


* Data
 SAM, ASAM0,
*SolRep  ,

* Table of scalar ults
 SCALres,
* Table of adjuster ults
 ADJres,
 QGDADJcres
* ------- TRADE BLOCK ----------------------------------------------------
* #### Exports Blockres
 PWEres
 PWSEres
 PEres
 PERres
 PDres
 QEres
 QERres
 QDres
* #### Imports Blockres
 PWMres
 PMres
 PMRres
 QMres
 QMRres
 QQres
* ------- TRADE AND TRANSPORT MARGINS BLOCK -----------------------------
 PTTres
 QTTres
 QTTDres
 IOQTTQQres
* ------- COMMODITY PRICE BLOCK -----------------------------------------
 PQSres
 PQDres
 PQCDres
 PQCres
* ------- PRODUCTION BLOCK ----------------------------------------------
 PXres
 PVAres
 PINTres
 ADXres
 ADres
 ADFDres
 ADFHres
 QXres
 QVAres
 VVAres
 QINTres
 ADVAres
 WFres
 WFAres
 WFDISTres
 FDres
 FSIres
 FSres
 UNEMPres
 UNEMPRATEres
 FSILres
 FSIMres
 MIGCONSres
 SHMIGres
 URBNRATEres
 FMIGDRVres
 HMIGDRVres
 PMIGDRVres
 QINTDres
 PXCres
 QXCres
 PXACres
 QXACres
 IOQXACQXVres
* ------- FACTOR BLOCK --------------------------------------------------
 YFres
 YFDISPres
 FSISHres
 INSVAres
 WMIGRres
* ------- HOUSEHOLD BLOCK -----------------------------------------------
* ## Household Income
 YHres
 HOGOVres
* Household Expenditure
 HOHOres
 HEXPres
 QCDres
 QCD2res
 QCDTotalres
 YMIGRres
* ------- ENTERPRISE BLOCK ----------------------------------------------
* ## Enterprise Income
 YEres
* ## Enterprise Expenditure
 HOENTres
 GOVENTres
 QEDres
 VEDres
* ------- GOVERNMENT BLOCK ----------------------------------------------
* #### Government Income Block
 TEres
 TMres
 TSres
 TVres
 TEXres
 TXres
 TXAres
 TFres
 TYFres
 TYHres
 TYEres
 TINres
 THCres
* #### Government Expenditure Block
 QGDres
 AgBuRecurrres
 AgBuInvestres
 AgBuInpSubres
 AgBuRevFundres
 AgBuOutSubres
 AgBuComSubres
 AgBuIncSubres
 AgBuTotres
* ------- KAPITAL BLOCK -------------------------------------------------
* ## Savings Block
 SHHres
 SENres
* ## Investment Block
 QINVDres
 QINVres
* ------- FOREIGN INSTITUTIONS BLOCK ------------------------------------
 YFWORres
* ------- MARKET CLEARING BLOCK -----------------------------------------
* #### Absorption Closure
 VEDSHres
 EXTENSres
 ADFExtres
 EDUCres
 HEALres
 BRATEres
 DRATEres
 DEATHres
 BIRTHres
 POPNres
 POPCHNGres

*-aggregate ults
* ultAgres
 COMTOTSHres
 VQCDres

*-Nutrition Elements
 NutValRes

*-SDG Indicators
 g01UtilPCRes
 g01WageCerRtRes
 g02TFPRes
 g02TMAvRes
 g02FdProdIndRes
 g02FdFsProdIndRes
 g02FdimpRes
 g02FdexpRes
 g02NutPCRes
 g02CalCerShRes
 g02ProLvsFsRes
 g02ProLvsRes
 g02YDAvRes
 g02FdPriIndRes
 g02FdYDShRes
 g02FdConsRes
 g02FdConsPCRes
 g02CalFrVShRes
 g02TMIndRes
 g02ExpSubIndRes
 g02TFPRes
 g06WatUseRes
 g07EnerPrimRes
 g07EnerClnShRes
 g07EnerProdRes
 g07EnerSfSuRes
 g07EnerPriIndRes
 g07FosCompRes
 g07RenCompRes
 g07FosRenRtRes
 g07EnerSecRes
 g07EnerVaRtRes
 g07EnerPrimStkRes
 g07EnerRefnRes
 g07EnerUseRes
 g07PrimGdpRtRes
 g07RefnGdpRtRes
 g07UseGdpRtRes
 g07RefnPrimRtRes
 g07UsePrimRtRes
 g08GDPPCGrRes
 g08NetTradeRes
 g08RevCompRes
 g08FosGDPShRes
 g09ManVaShRes
 g09ManVaPCRes
 g08ManEmpShRes
 g08ExpRes
 g08ImpRes
 g08OpenRes
 g10LabShRes
 g10AgrEmpRes
 g10AgrEmpShRes
 g10SkilRes
 g10WageDifSklRes
 g10WageDifAgrRes
 g10IncDiffHHRes
 g10IncDiffHHAgRes
 g12RenShRes
 g13RenShRes
 g14FsShRes
 g15NonAgriRes
 g17GDPPcRes
 g17EGShRes
 
***$$$Emissions*****

 CO2EM_Qres
 CO2EM_Hres
 CO2EMIS_Qres
 CO2EMIS_Hres
 CO2EMISres
 NCO2EM_Qres
 NCO2EM_FSres
 NCO2EM_IOres
 NCO2EM_ENres
 NCO2EM_Hres
 NCO2EM_A_SUMres
 NCO2EM_SUMres
 GHGEMres

 NCO2EM_FS_SUMres
 NCO2EM_IO_SUMres
 NCO2EM_EN_SUMres
 NCO2EM_H_SUMres

 GHGres
;
* ----------------- end of DEMETRA percentage change ults -----------
