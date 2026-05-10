
*------------------------------------------------------------------------------
*-------------------------------------------------------------------------------
*--   DEMETRA v1.0-alpha
*--
*--   GAMS file : emissions.inc
*--
*--   @purpose  : Declares the parameters for emissions
*--   @calledBy : Model.GMS
*-------------------------------------------------------------------------------
*-------------------------------------------------------------------------------

***** ENDOGENIZING EMISSIONS in the Model

$ontext
*Combustive emissions of CO2 from energy use from energy energy use by activities and households
*Non-combustive emissions may include CO2 besides CH4, N2O, NH3, other

$offtext

* the file is used with $batinclude for both initial calibration ("init") and resetting values in the dynamic runs ("assign")
$goto %1


$label init
Parameter

coefco2Q_aux(c,a)           CO2 emission coeeficients per unit of quantity of energy input used by activities
coefco2H_aux(c,h)           CO2 emission coeeficients per unit of quantity of energy input used by households
coefnco2Q_aux(NCO,a)        Output-based non-combustive emission coeeficients
coefnco2H_aux(NCO,c,h)      Household based non-combustive emission coefficients
coefnco2IO_aux(NCO,c,a)     Process non-combustive emission coefficients based on intermediate demand
coefnco2FS_aux(NCO,c,a)     NCO2 emission coefficients based on fossil fuel combustion in production
coefnco2EN_aux(NCO,f,a)     Endowment based non-combustive emission coefficients

gwp(NCO)                  Global warming potential

TNCO2EM_EN
;

$onMultiR
$GDXIN %gdxF%\emissions_Coeff_DEMETRA_%DEMETRA_REG%.gdx
$LOADdc cener_ghg
$LOADdc coefco2Q_aux=coefco2Q coefco2H_aux=coefco2H coefnco2Q_aux=coefnco2Q coefnco2IO_aux=coefnco2IO coefnco2FS_aux=coefnco2FS coefnco2H_aux=coefnco2H coefnco2EN_aux=coefnco2EN

set nonGHG(NCO) / BC, CO, NH3,NMVOC, NOX, OC,PM10, PM2_5, SO2, C2F6, C3F8, C4F10, C5F12, C6F14, CC4F8, CF4, HCFC141b, HCFC142b, HFC125, HFC134, HFC134a, HFC143,
HFC143a, HFC152a, HFC227ea, HFC23, HFC236fa, HFC245fa, HFC32, HFC365mfc, HFC41, HFC4310mee, NF3, SF6/;

$label assign

 gwp(NCO)   = 1   ;
 gwp(nonGHG)= 0   ;
 gwp("CO2") = 1   ;
 gwp("CH4") = 25  ;
 gwp("N2O") = 298 ;

 coefco2Q(cener_ghg,a)            = coefco2Q_aux(cener_ghg,a)          ;
 coefco2H(cener_ghg,h)            = coefco2H_aux(cener_ghg,h)          ;
 coefnco2Q(NCO,a)         = gwp(NCO) * coefnco2Q_aux(NCO,a)       ;
 coefnco2H(NCO,c,h)       = gwp(NCO) * coefnco2H_aux(NCO,c,h)     ;
 coefnco2IO(NCO,c,a)      = gwp(NCO) * coefnco2IO_aux(NCO,c,a)    ;
 coefnco2FS(NCO,c,a)      = gwp(NCO) * coefnco2FS_aux(NCO,c,a)    ;
 coefnco2EN(NCO,f,a)      = gwp(NCO) * coefnco2EN_aux(NCO,f,a)    ;


 CO2EM_Q0(c,a)          = coefco2Q(c,a)*QINTD0(c,a);
 CO2EM_H0(c,h)          = coefco2H(c,h)*QCD0(c,h);
 CO2EMIS_Q0(a)          = SUM(cener_ghg,CO2EM_Q0(cener_ghg,a));
 CO2EMIS_H0(h)          = SUM(cener_ghg,CO2EM_H0(cener_ghg,h));
 CO2EMIS0               = sum(a,CO2EMIS_Q0(a)) + sum(h,CO2EMIS_H0(h)) ;

 NCO2EM_Q0(nco,a)       = coefnco2Q(nco,a)*QX0(a);
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

 GHGEM0                 = CO2EMIS0 + SUM(NCO,NCO2EM_SUM0(NCO)) ;


TNCO2EM_EN     = sum((nco,f,a),coefnco2EN(nco,f,a)*FD0(f,a));

display TNCO2EM_EN;
