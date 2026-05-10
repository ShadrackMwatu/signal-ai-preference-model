*-SDGs
*-------------------------------------------------------------------------------
*- Sets for SDGs
*-------------------------------------------------------------------------------
SET
 enEl1(sac)    Energy indicator elements
 /
 Export
 Import
 "Domestic Demand"
 /
 enEl2(sac)        Energy indicator elements 2
 /
 Transport
 Industry
 Other
 Exports
 /

 egEl(sac)        Government income indicator elements
 /
 MTAX
 ETAX
 DTAX
* DTAXA
 FYTAX
 ITAX
 STAX
 FTAX
 VTAX
 HCTAX
 /
 ;

Parameters
*-SDGs
*- Goal 1: No poverty
 g01UtilPC0(h)              Per capita utility from private expenditure
 g01UtilPCAg0              Per capita utility from private expenditure
 g01WageCerRt0              Rural wage rate

*- Goal 2: Zero hunger
 g02TFP0                    Total factor productivity: endowment enhancing technical change
 g02TMAv0                   Average import tariffs on agricultural food products (ad valorem rate)
 g02FdProdInd0              Index of Food production
 g02FdFsProdInd0            Index of Food production
 g02Fdimp0                  food import value
 g02Fdexp0                 Food export value
 g02NutPC0(nutElem,h)      nutrition values per capita
 g02NutPCAg0(nutElem)      nutrition values per capita
*g02CalPCPD0               calories per capita per day    IRRELEVANT
 g02CalCerSh0(h)              share of calories per capita in total calories pc
 g02CalCerShAg0              share of calories per capita in total calories pc
 g02ProLvsFs0(h)              Protein from livestock and fish and livestock  products
 g02ProLvsFsAg0              Protein from livestock and fish and livestock  products
 g02ProLvs0(h)                Protein from livestock and livestock  products (no fish)
 g02ProLvsAg0                Protein from livestock and livestock  products (no fish)
 g02YDAv0(h)                  Average household disposable income
 g02YDAvAg0                  Average household disposable income
 g02FdPriInd0(h)              food price index
 g02FdPriIndAg0              food price index
 g02FdYDSh0(h)                Share of food expenditure in total disposable income
 g02FdYDShAg0                Share of food expenditure in total disposable income
 g02FdCons0(h)                food consumption
 g02FdConsAg0                food consumption
 g02FdConsPC0(h)              food consumption per capita
 g02FdConsPCAg0              food consumption per capita
 g02CalFrVSh0(h)              Share of calories from fruit and vegetables
 g02CalFrVShAg0              Share of calories from fruit and vegetables
 g02TMInd0                 index of import tariffs on agricultural goods products
 g02ExpSubInd0             index of export subsidies on agricultural goods products
 g02TFP0                   Total factor productivity: endowment enhancing technical change (AD)


*- Goal 6:  Clean water and sanitation
 g06WatUse0                index of total abstracted irrigation water volumes


*- Goal 7: Affordable and clean energy, difficult to insert here
 g07EnerPrim0              Primary Energy
 g07EnerClnSh0             Share of clean energy in total energy
 g07EnerProd0              Energy production (Final Energy)
 g07EnerSfSu0              Energy Self sufficiency
 g07EnerPriInd0(c)               Energy price
 g07EnerPriIndAg0               Energy price
 g07FosComp0               Relative competitiveness of  fossil    (PD over PWM)
 g07RenComp0               Relative competitiveness of  fossil    (PD over PWM)
 g07FosRenRt0              Relative competitiveness of  fossil
 g07EnerSec0               Energy security: value-added contribution
 g07EnerVaRt0(a)           Ratio of value added to net domestic energy use by industry
 g07EnerVaRtAg0           Ratio of value added to net domestic energy use by industry
 g07EnerPrimStk0(enEl1)  Primary energy stock: mining
 g07EnerRefn0             Refining transformation and power station usage (perto-chem & electricity)
 g07EnerUse0(enEl2)                Energy use by transportation industry other export of refined
 g07PrimGdpRt0(enEl1)             PrimaryEnergy intensity measured in terms of GDP
 g07RefnGdpRt0             Refining Energy intensity measured in terms of GDP
 g07UseGdpRt0(enEl2)              Energy use intensity measured in terms of GDP
 g07RefnPrimRt0            Refining Energy intensity measured in terms of Primary energy
 g07UsePrimRt0(enEl2)             Energy use intensity measured in terms of Primary energy


*- Goal 8 Economic growth
 g08GDPPCGr0               GDP per capita growth
 g08NetTrade0              net trade position
 g08RevComp0(c)               Revealed Comparative Advantage (if >1 country has RCA in that comm. export more compared to other sectors)
 g08RevCompAg0               Revealed Comparative Advantage (if >1 country has RCA in that comm. export more compared to other sectors)
*g08DivInd0                Diversification index (IRRELEVANT)
 g08FosGDPSh0              Share of fossil fuels in GDP


*- Goal 9.  Industry, innovation and infrastructure
 g09ManVaSh0               Manufacturing value added as a share of total value
 g09ManVaPC0               Manufacturing value added per capita
 g08ManEmpSh0              Manufacturing employment as a percentage of total employment
 g08Exp0                   Total Exports
 g08Imp0                   Total Imports
 g08Open0                  Trade Opennes


*-Goal 10. Reduced inequalities
 g10LabSh0                 Labour share of GDP comprising wages
 g10AgrEmp0                Change in agricultural employment
 g10AgrEmpSh0              Agricultural employment as a percentage of total employment
 g10Skil0                  Skills composition
 g10WageDifSkl0            Wage differential skilled:unskilled
 g10WageDifAgr0            Wage differential agriculture:non-agriculture
 g10IncDiffHH0(h,hp)       Income differential households (ratio of inc per capita minus one)
 g10IncDiffHHAg0           Average Income differential households

*- Goal 12. Responsible consumption and production
 g12RenSh0                 Share of renewables in total energy production
*g12FosSub0                Amount of fossil fuel subsidies per unit of GDP (IRRELEVANT)
*g12FosSubExpRt0           Amount of fossil fuel subsidies as a share of national expenditure on fossil fuels (IRRELEVANT)

*- Goal 13. Climate action
 g13RenSh0                 Share of renewables in total energy production

*-Goal 14. Life below water
 g14FsSh0                  Fisheries as a value share of GDP

*- Goal 15. Life on land
 g15NonAgri0               Share of non-agricultural land (1 - change in agri land) (or forest area ???)


*-Goal 17. Partnership for the goals
 g17GDPPc0                 GDP per capita
 g17EGSh0(egEl)                  Total government revenue (by source) as a percentage of GDP
 g17EGShAg0                  Total government revenue (by source) as a percentage of GDP
;

*- Goal 1: No poverty
 g01UtilPC0(h)$POPN0(h) = SUM(cc$QCD0(cc,h),beta(cc,h)*log((QCD0(cc,h)-qcdconst(cc,h)))/POPN0(h));

 g01UtilPCAg0$SUM(h,POPN0(h))= SUM((h,cc)$QCD0(cc,h),beta(cc,h)*log(QCD0(cc,h)-qcdconst(cc,h)))/SUM(h,POPN0(h));

 g01WageCerRt0$(SUM(l$lRuUs(l),FS0(l)) and SUM((ccer),PQD0(ccer)*QD0(ccer)) AND SUM((ccer),QD0(ccer))) = (SUM(l$lRuUs(l),WF0(l)*FS0(l))/SUM(l$lRuUs(l),FS0(l)))
                               /(SUM((ccer),PQD0(ccer)*QD0(ccer))/SUM((ccer),QD0(ccer))) ;

*- Goal 2: Zero hunger
 g02TFP0 = SUM(aagr,AD0("ftop",aagr))/SUM(aagr,1);

 g02TMAv0$SUM((w,c)$cfdh(c),QMR0(w,c)*PMR0(w,c)) = SUM((w,c)$cfdh(c),QMR0(w,c)*PQD0(c))/SUM((w,c)$cfdh(c),QMR0(w,c)*PMR0(w,c));

 g02FdProdInd0 = SUM(c$(cfd(c) AND cfdh(c)),QXC0(c)*PXC0(c))/SUM(c$cfd(c),QXC0(c)*PXC0(c))*100;

 g02FdFsProdInd0  =SUM(c$(cfdh(c) OR cfs(c)),QXC0(c)*PXC0(c))
                                        /SUM(c$(cfs(c) OR cfdh(c)),QXC0(c)*PXC0(c))*100;
 g02Fdimp0 =  SUM(c$cfdh(c),PM0(c)*QM0(c))   ;

 g02Fdexp0 =  SUM(c$cfdh(c),PE0(c)*QE0(c))   ;

 g02NutPC0(nutElem,h) =  nutVal0(nutElem,h)/POPN0(h)  ;
 g02NutPCAg0(nutElem) =  SUM(h,nutVal0(nutElem,h))/SUM(h,POPN0(h))  ;

 g02CalCerSh0(h)$nutVal0("cal",h) =  SUM(c$ccer(c),nutTable(c,"cal")*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))/ nutVal0("cal",h);
 g02CalCerShAg0 $(SUM(h,nutVal0("cal",h))) =  SUM((c,h)$ccer(c),nutTable(c,"cal")*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))/ SUM(h,nutVal0("cal",h));

 g02ProLvsFs0(h)$nutVal0("pro",h) =  SUM(c$(cliv(c) or cfs(c)),nutTable(c,"pro")*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))/ nutVal0("pro",h);
 g02ProLvsFsAg0 $(SUM(h,nutVal0("pro",h)))=  SUM((c,h)$(cliv(c) or cfs(c)),nutTable(c,"pro")*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))/ SUM(h,nutVal0("pro",h));

 g02ProLvs0(h)$(nutVal0("pro",h))        =   SUM(c$(cliv(c)),nutTable(c,"pro")*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))    / nutVal0("pro",h);
 g02ProLvsAg0 $(SUM(h,nutVal0("pro",h))) =    SUM((c,h)$(cliv(c)),nutTable(c,"pro")*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))/ SUM(h,nutVal0("pro",h));


 g02YDAv0(h) =      YH0(h) * (1 - TYH0(h)) * (1 - SHH0(h)) ;
 g02YDAvAg0 =      SUM(H,YH0(h) * (1 - TYH0(h)) * (1 - SHH0(h))) ;

 g02FdPriInd0(h)$(SUM(c$cfdh(c)    ,PQD0(c)*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))) =     SUM(c$cfdh(c),PQD0(c)*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))/(SUM(c$cfdh(c),PQD0(c)*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h)))))*100;
 g02FdPriIndAg0 $(SUM((c,h)$cfdh(c),PQD0(c)*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))) =     SUM((h,c)$cfdh(c),PQD0(c)*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))/(SUM((c,h)$cfdh(c),PQD0(c)*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h)))))*100;

 g02FdYDSh0(h)$HEXP0(h) =       SUM(c$cfdh(c),PQD0(c)*QCD0(c,h)+SUM(cag,QCD20(cag,c,h)))/HEXP0(h) ;
 g02FdYDShAg0 =       SUM((c,h)$cfdh(c),PQD0(c)*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))/SUM(h,HEXP0(h)) ;

 g02FdCons0(h) =       SUM(c$cfdh(c),PQD0(c)*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h)))) ;
 g02FdConsAg0 =       SUM((h,c)$cfdh(c),PQD0(c)*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h)))) ;

 g02FdConsPC0(h) =        SUM(c$cfdh(c),PQD0(c)*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))/POPN0(h) ;
 g02FdConsPCAg0 =        SUM((c,h)$cfdh(c),PQD0(c)*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))/SUM(h,POPN0(h)) ;

 g02CalFrVSh0(h)$nutVal0("cal",h) =     SUM(c$cfv(c),nutTable(c,"cal")*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))/ nutVal0("cal",h);
 g02CalFrVShAg0$(SUM(h,nutVal0("cal",h))) =     SUM((c,h)$cfv(c),nutTable(c,"cal")*(QCD0(c,h)+SUM(cag,QCD20(cag,c,h))))/ SUM(h,nutVal0("cal",h));

 g02TMInd0 =       g02TMAv0 / g02TMAv0*100 ;

 g02ExpSubInd0 =    SUM((w,c)$cfdh(c),QER0(c,w)*PWE0(c)*ER0(w))/SUM((w,c)$cfdh(c),QER0(c,w)*PER0(c,w))
                          / SUM((w,c)$cfdh(c),QER0(c,w)*PWE0(c)*ER0(w))/SUM((w,c)$cfdh(c),QER0(c,w)*PER0(c,w))*100;

 g02TFP0 =          SUM(aagr,AD0("ftop",aagr))/SUM(aagr,1);

*- Goal 6:  Clean water a
 g06WatUse0 =     SUM((a,f)$nirr(f),FD0(f,a))/SUM((a,f),FD0(f,a))*100;

*- Goal 7: Affordable and
 g07EnerPrim0 =   SUM((cener,ff,a)$map_c_f_a(cener,ff,a),FD0(ff,a)*WFA0(ff,a));

 g07EnerClnSh0$SUM(cener,QXC0(cener)) =  SUM(crenw,QXC0(crenw))/SUM(cener,QXC0(cener));

 g07EnerProd0 =   SUM(cener,QXC0(cener))    ;

 g07EnerSfSu0$SUM(cener,QQ0(cener)) =   SUM(cener,QD0(cener)) /SUM(cener,QQ0(cener))  ;

 g07EnerPriInd0(cener)$(QD0(cener)*PD0(cener)) =    QD0(cener)*PD0(cener)/QD0(cener)*PD0(cener)*100   ;

 g07EnerPriIndAg0$SUM(cener,QD0(cener)*PD0(cener)) =    SUM(cener,QD0(cener)*PD0(cener))/SUM(cener,QD0(cener)*PD0(cener))*100   ;

 g07FosComp0$SUM(cfoss,QD0(cfoss)*PD0(cfoss)) = (1/ERX0)*(SUM(cfoss,QD0(cfoss)*PD0(cfoss))
                                                       /SUM(cfoss,QD0(cfoss)*PD0(cfoss)))*100                   ;

 g07RenComp0$SUM(crenw,QD0(crenw)*PD0(crenw)) = (1/ERX0)*(SUM(crenw,QD0(crenw)*PD0(crenw))
                                                       /SUM(crenw,QD0(crenw)*PD0(crenw)))*100                ;

 g07FosRenRt0$g07RenComp0 =       g07FosComp0/g07RenComp0*100    ;

 g07EnerSec0 =        SUM(cener,QXC0(cener))/SUM(c,QXC0(c)) ;

 g07EnerVaRt0(a)$VVA0(a) =    SUM((cener,ff)$map_c_f_a(cener,ff,a),FD0(ff,a)*WFA0(ff,a))/VVA0(a);
 g07EnerVaRtAg0 =    SUM((cener,ff,a)$map_c_f_a(cener,ff,a),FD0(ff,a)*WFA0(ff,a))/SUM(a,VVA0(a));

 g07EnerPrimStk0("Export") =  SUM(cener,QE0(cener)*PE0(cener))                        ;

 g07EnerPrimStk0("Import") =  SUM(cener,QM0(cener)*PM0(cener))                        ;

 g07EnerPrimStk0("Domestic Demand") =  SUM(cener,QD0(cener)*PD0(cener))                       ;

 g07EnerRefn0 = SUM((cener,ff,aener)$map_c_f_a(cener,ff,aener),FD0(ff,aener)*WFA0(ff,aener));

 g07EnerUse0('Transport') = SUM((cener,ff,atrn)$map_c_f_a(cener,ff,atrn),FD0(ff,atrn)*WFA0(ff,atrn));

 g07EnerUse0('Industry') = SUM((cener,ff,aind)$map_c_f_a(cener,ff,aind),FD0(ff,aind)*WFA0(ff,aind));

 g07EnerUse0('Other') =  SUM((cener,ff,a)$(NOT (aind(a) OR atrn(a)) AND map_c_f_a(cener,ff,a)),FD0(ff,a)*WFA0(ff,a));

 g07EnerUse0('Exports') =   SUM(cener,QE0(cener));

 g07PrimGdpRt0(enEl1)$g07EnerPrimStk0(enEl1) =  (g07EnerPrimStk0(enEl1) /GDP0);

 g07RefnGdpRt0 = (g07EnerRefn0/GDP0)                       ;

 g07UseGdpRt0(enel2)$g07EnerUse0(enel2)  =   (g07EnerUse0(enel2) /GDP0)                      ;

 g07RefnPrimRt0$g07EnerPrim0 =  g07EnerRefn0/g07EnerPrim0;

 g07UsePrimRt0(enEl2)$g07EnerUse0(enEl2) =   (g07EnerUse0(enEl2)/g07EnerPrim0) ;


*- Goal 8 Economic growth
 g08GDPPCGr0 =   GDP0/SUM(h,POPN0(h))                          ;

 g08NetTrade0 =  SUM(c,PE0(c)*QE0(c))-SUM(c,PM0(c)*QM0(c))  ;

 g08RevComp0(c)$(ce(c) AND cx(c)) =  (PE0(c)*QE0(c)/PXC0(c)*QXC0(c)) /(SUM(cp,PE0(cp)*QE0(cp))/SUM(cp,PXC0(cp)*QXC0(cp)))            ;
 g08RevCompAg0 = SUM(c$(ce(c) AND cx(c)), g08RevComp0(c))/SUM(c$(ce(c) AND cx(c)),1);

*g08DivInd0 =                               ;

 g08FosGDPSh0 =   SUM(cfoss,QXC0(cfoss))/SUM(c,QXC0(c)) ;

*- Goal 9.  Industry, inn
 g09ManVaSh0 = SUM(aind,VVA0(aind))/SUM(a,VVA0(a)) ;

 g09ManVaPC0 =  SUM(aind,VVA0(aind))/SUM(h,POPN0(h))  ;

 g08ManEmpSh0 = SUM((l,aind),FD0(l,aind))/SUM((l,a),FD0(l,a)) ;

 g08Exp0 =     SUM(c,PE0(c)*QE0(c))                          ;

 g08Imp0 =      SUM(c,PM0(c)*QM0(c))                          ;

 g08Open0 =     (SUM(c,PE0(c)*QE0(c))+SUM(c,PM0(c)*QM0(c)))/GDP0  ;


*-Goal 10. Reduced inequa
 g10LabSh0 = SUM((l,a),FD0(l,a)*WFA0(l,a))/SUM((f,a),FD0(f,a)*WFA0(f,a))  ;

 g10AgrEmp0 =  SUM((l,aagr),FD0(l,aagr))  ;

 g10AgrEmpSh0 = SUM((l,aagr),FD0(l,aagr))/SUM((l,a),FD0(l,a))                          ;

 g10Skil0$SUM((lu,a),FD0(lu,a)) =     SUM((ls,a),FD0(ls,a))/SUM((lu,a),FD0(lu,a))                          ;

 g10WageDifSkl0 $(sum((ls,a), FD0(ls,a)) and sum((lu,a), FD0(lu,a))) = (SUM((ls,a),FD0(ls,a)*WFA0(ls,a))/SUM((ls,a),FD0(ls,a)))
                  /(SUM((lu,a),FD0(lu,a)*WFA0(lu,a))/SUM((lu,a),FD0(lu,a))) ;

 g10WageDifAgr0 = (SUM((l,aagr),FD0(l,aagr)*WFA0(l,aagr))/SUM((l,aagr),FD0(l,aagr)))
                  /(SUM((l,a),FD0(l,a)*WFA0(l,a))/SUM((l,a),FD0(l,a))) ;

 g10IncDiffHH0(h,hp)$(YH0(hp) AND POPN0(h) AND POPN0(hp)) =  (YH0(h)/POPN0(h))/(YH0(hp)/POPN0(hp))-1                        ;
 g10IncDiffHHAg0$(sum((h,hp),g10IncDiffHH0(h,hp))) =   SUM((h,hp)$(ord(h)<card(hp)),g10IncDiffHH0(h,hp))/ SUM((h,hp)$(ord(H)<card(hp)),1) ;

*- Goal 12. Responsible c
 g12RenSh0$SUM(cener,QXC0(cener)) = SUM(crenw,QXC0(crenw))/SUM(cener,QXC0(cener)) ;

*- Goal 13. Climate actio
 g13RenSh0$SUM(cener,QXC0(cener)) = SUM(crenw,QXC0(crenw))/SUM(cener,QXC0(cener)) ;

*-Goal 14. Life below wat
 g14FsSh0 = SUM(cfs,QXC0(cfs))/GDP0 ;

*- Goal 15. Life on land
 g15NonAgri0$(SUM((n,a),FD0(n,a))) =  SUM((n,a)$(NOT aagr(a)),FD0(n,a))/SUM((n,a),FD0(n,a))  ;


*-Goal 17. Partnership fo
 g17GDPPc0 = GDP0/SUM(h,POPN0(h))  ;

 g17EGSh0("MTAX") =  MTAX0/YG0     ;
 g17EGSh0("ETAX") =  ETAX0/YG0     ;
 g17EGSh0("DTAX") =  DTAX0/YG0     ;
 g17EGSh0("FYTAX") =  FYTAX0/YG0   ;
 g17EGSh0("ITAX") =  ITAX0/YG0     ;
 g17EGSh0("STAX") =  STAX0/YG0     ;
 g17EGSh0("FTAX") =  FTAX0/YG0     ;
 g17EGSh0("VTAX") =  VTAX0/YG0     ;
 g17EGSh0("HCTAX") =  HCTAX0/YG0   ;
 g17EGShAg0 =  SUM(egEl,g17EGSh0(egEl));

*-------------------------------------------------------------------------------
*- Sustainable Development Goals
*-------------------------------------------------------------------------------
Parameters
*- Goal 1: No poverty
 g01UtilPC(h)              Per capita utility from private expenditure for each HH
 g01UtilPCAg               Per capita utility from private expenditure for all HHS
 g01WageCerRt              Per capita household expenditure

*- Goal 2: Zero hunger
 g02TFP                     Total factor productivity: endowment enhancing technical change
 g02TMAv                    Average import tariffs on agricultural food products (ad valorem rate) -
 g02FdProdInd               Index of Food production
 g02FdFsProdInd             Index of Food and fish production
 g02Fdimp                   Food import value
 g02Fdexp                   Food export value
 g02NutPC(nutElem,h)        calories per capita for each HH
 g02NutPCAG(nutElem)        calories per capita for all HHs
* g02CalPCPD                 calories per capita per day   IRRELEVANT
 g02CalCerSh(h)             share of calories per capita in total calories pc for each HH
 g02CalCerShAg              share of calories per capita in total calories pc for all HHs
 g02ProLvsFs(h)             Protein from livestock and fish and livestock  products for each HH
 g02ProLvsFsAg              Protein from livestock and fish and livestock  products for all HHs
 g02ProLvs(h)               Protein from livestock and livestock  products (no fish) for each HH
 g02ProLvsAg                Protein from livestock and livestock  products (no fish) for all HHs
 g02YDAv(h)                 Average household disposable income for each HH
 g02YDAvAg                  Average household disposable income for all HHs
 g02FdPriInd(h)             food price index for each HH
 g02FdPriIndAg              food price index for all HHs
 g02FdYDSh(h)               Share of food expenditure in total disposable income for each HH
 g02FdYDShAg                Share of food expenditure in total disposable income for all HHs
 g02FdCons(h)               food consumption for each HH
 g02FdConsAg                food consumption for all HHs
 g02FdConsPC(h)             food consumption per capita  for each HH
 g02FdConsPCAg              food consumption per capita  for all HHs
 g02CalFrVSh(h)             Share of calories from fruit and vegetables for each HH
 g02CalFrVShAg              Share of calories from fruit and vegetables for all HHs
 g02TMInd                   index of import tariffs on agricultural goods products
 g02ExpSubInd               index of export subsidies on agricultural goods products
 g02TFP                     Total factor productivity: endowment enhancing technical change (AD)


*- Goal 6:  Clean water and sanitation
 g06WatUse                index of total abstracted irrigation water volumes


*- Goal 7: Affordable and clean energy
 g07EnerPrim              Average energy price
 g07EnerClnSh             Share of clean energy in total energy
 g07EnerProd              Energy production (Final Energy)
 g07EnerSfSu              Energy self sufficiency
 g07EnerPriInd(c)         Energy Price for each energy commodity
 g07EnerPriIndAg          Energy Price for aggregate energy commodity
 g07FosComp               Relative competitiveness of  fossil    (PD over PWM)
 g07RenComp               Relative competitiveness of  fossil    (PD over PWM)
 g07FosRenRt              Relative competitiveness of  fossil
 g07EnerSec               Energy security: value-added contribution
 g07EnerVaRt(a)           Ratio of value added to net domestic energy use by industry
 g07EnerVaRtAg            Ratio of value added to net domestic energy for all industries
 g07EnerPrimStk(enEl1)    Primary energy stock
 g07EnerRefn              Refining transformation and power station usage (perto-chem & electricity)
 g07EnerUse(enEl2)        Energy use by transportation - industry -other -export or -refined
 g07PrimGdpRt(enEl1)      PrimaryEnergy intensity measured in terms of GDP
 g07RefnGdpRt             Refining Energy intensity measured in terms of GDP
 g07UseGdpRt(enEl2)       Energy use intensity measured in terms of GDP
 g07RefnPrimRt            Refining Energy intensity measured in terms of Primary energy
 g07UsePrimRt(enEl2)             Energy use intensity measured in terms of Primary energy


*- Goal 8 Economic growth
 g08GDPPCGr               GDP per capita growth
 g08NetTrade              Net trade position
 g08RevComp(c)            Revealed Comparative Advantage for each commodity
 g08RevCompAg             Average Revealed Comparative Advantage  of all sectors
*g08DivInd                Diversification index (IRRRELAVANT)
 g08FosGDPSh              Share of fossil fuels in GDP


*- Goal 9.  Industry, innovation and infrastructure
 g09ManVaSh               Manufacturing value added as a share of total value
 g09ManVaPC               Manufacturing value added per capita
 g08ManEmpSh              Manufacturing employment as a percentage of total employment
 g08Exp                   Total Exports
 g08Imp                   Total Imports
 g08Open                  Trade Opennes


*-Goal 10. Reduced inequalities
 g10LabSh                 Labour share of GDP comprising wages
 g10AgrEmp                Change in agricultural employment
 g10AgrEmpSh              Agricultural employment as a percentage of total employment
 g10Skil                  Skills composition
 g10WageDifSkl            Wage differential skilled:unskilled
 g10WageDifAgr            Wage differential agriculture:non-agriculture
 g10IncDiffHH(h,hp)       Income differential households (ratio of inc per capita)
 g10IncDiffHHAg           Average of income differential across households

*- Goal 12. Responsible consumption and production
 g12RenSh                 Share of renewables in total energy production
*-g12FosSub                Amount of fossil fuel subsidies per unit of GDP (IRRELEVANT)
*g12FosSubExpRt           Amount of fossil fuel subsidies as a share of national expenditure on fossil fuels (IRRELEVANT)

*- Goal 13. Climate action
 g13RenSh                 Share of renewables in total energy production

*-Goal 14. Life below water
 g14FsSh                  Fisheries as a value share of GDP

*- Goal 15. Life on land
 g15NonAgri               Share of non-agricultural land (1 - change in agri land) (or forest area ???)


*-Goal 17. Partnership for the goals
 g17GDPPc                 GDP per capita
 g17EGSh(egEl)            Total government revenue by source as a percentage of GDP
 g17EGShAg                Total government revenue as a percentage of GDP

;

$onDotL
*- Goal 1:
 g01UtilPC(h) = SUM(cc$QCD0(cc,h),beta(cc,h)*log(QCD(cc,h)-qcdconst(cc,h)))/POPN0(h)  ;

 g01UtilPCAg = SUM((cc,h)$QCD0(cc,h),beta(cc,h)*log(QCD(cc,h)-qcdconst(cc,h)))/SUM(h,POPN0(h))  ;


 g01WageCerRt$(SUM(l$lRuUs(l),FS(l)) and SUM((ccer),QD(ccer)) ) = (SUM(l$lRuUs(l),WF(l)*FS(l))/SUM(l$lRuUs(l),FS(l))) /(SUM((ccer),PQD(ccer)*QD(ccer))/SUM((ccer),QD(ccer)));

*- Goal 2:
 g02TFP = SUM(aagr,AD("ftop",aagr))/SUM(aagr,1);

 g02TMAv$SUM((w,c)$cfdh(c),QMR0(w,c)*PMR0(w,c)) = SUM((w,c)$cfdh(c),QMR(w,c)*PQD(c))
                              /SUM((w,c)$cfdh(c),QMR(w,c)*PMR(w,c))  ;

 g02FdProdInd = SUM(c$(cfd(c) AND cfdh(c)),QXC(c)*PXC(c))
                                        /SUM(c$cfd(c),QXC0(c)*PXC(c))*100;

 g02FdFsProdInd = SUM(c$(cfdh(c) OR cfs(c)),QXC(c)*PXC(c))
                                        /SUM(c$(cfs(c) OR cfdh(c)),QXC0(c)*PXC(c))*100 ;

               g02Fdimp = SUM(c$cfdh(c),PM(c)*QM(c))   ;

               g02Fdexp = SUM(c$cfdh(c),PE(c)*QE(c))   ;

                g02NutPC(nutElem,h) = nutVal(nutElem,h)/POPN0(h);

                g02NutPCAg(nutElem) = SUM(h,nutVal(nutElem,h))/SUM(h,POPN0(h));


*g02CalPCPDDef.         g02CalPC(h) = nutValue("cal",h)/POPN0(h);

    g02CalCerSh(h)$ nutVal0("cal",h) = SUM(c$ccer(c),nutTable(c,"cal")*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ nutVal("cal",h)  ;
     
    g02CalCerShAg $(SUM(h,nutVal0("cal",h)))= SUM((c,h)$ccer(c),nutTable(c,"cal")*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ SUM(h,nutVal("cal",h))  ;

    g02ProLvsFs(h)$nutVal0("pro",h) = SUM(c$(cliv(c) or cfs(c)),nutTable(c,"pro")
                                           * (QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ nutVal("pro",h)  ;

 g02ProLvsFsAg$(SUM(h,nutVal0("pro",h))) = SUM((c,h)$(cliv(c) or cfs(c)),nutTable(c,"pro")
                                           * (QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ SUM(h,nutVal("pro",h))  ;


          g02ProLvs(h)$nutVal0("pro",h) = SUM(c$(cliv(c)),nutTable(c,"pro")*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ nutVal("pro",h);
          g02ProLvsAg$(SUM(h,nutVal0("pro",h))) = SUM((h,c)$(cliv(c)),nutTable(c,"pro")*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ SUM(h,nutVal("pro",h));

 g02YDAv(h) = YH(h) * (1 - TYH(h)) * (1 - SHH(h))  ;
 g02YDAvAg  = SUM(h,YH(h) * (1 - TYH(h)) * (1 - SHH(h)))  ;

 g02FdPriInd(h)$(SUM(c$cfdh(c),PQD0(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))) =
                                                SUM(c$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h)))) /(SUM(c$cfdh(c),PQD0(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h)))))*100 ;
 g02FdPriIndAg $ (SUM((h,c)$cfdh(c),PQD0(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))) =
                                                SUM((h,c)$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/(SUM((h,c)$cfdh(c),PQD0(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h)))))*100 ;

 g02FdYDSh(h) = SUM(c$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/HEXP(h);
 g02FdYDShAg = SUM((h,c)$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/SUM(h,HEXP(h));

 g02FdCons(h) = SUM(c$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))));
 g02FdConsAg = SUM((h,c)$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))));

 g02FdConsPC(h) = SUM(c$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/POPN0(h);
 g02FdConsPCAg = SUM((h,c)$cfdh(c),PQD(c)*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/SUM(h,POPN0(h));

 g02CalFrVSh(h)$nutVal0("cal",h) = SUM(c$cfv(c),nutTable(c,"cal")*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ nutVal("cal",h)   ;
 g02CalFrVShAg$(SUM(h,nutVal0("cal",h)))= SUM((h,c)$cfv(c),nutTable(c,"cal")*(QCD(c,h)+SUM(cag,QCD2(cag,c,h))))/ SUM(h,nutVal("cal",h))   ;

 g02TMInd = g02TMAv / g02TMAv0*100   ;

 g02ExpSubInd = SUM((w,c)$cfdh(c),QER(c,w)*PWE(c)*ER(w))/SUM((w,c)$cfdh(c),QER(c,w)*PER(c,w))
                                         / SUM((w,c)$cfdh(c),QER0(c,w)*PWE0(c)*ER0(w))/SUM((w,c)$cfdh(c),QER0(c,w)*PER0(c,w))*100;
*- Goal 6:
 g06WatUse = SUM((a,f)$nirr(f),FD(f,a))/SUM((a,f),FD(f,a))*100;

*- Goal 7:
 g07EnerPrim = SUM((cener,ff,a)$map_c_f_a(cener,ff,a),FD(ff,a)*WFA(ff,a))   ;

 g07EnerClnSh$SUM(cener,QXC(cener)) = SUM(crenw,QXC(crenw))/SUM(cener,QXC(cener))  ;

 g07EnerProd = SUM(cener,QXC(cener));

 g07EnerSfSu$SUM(cener,QQ(cener)) = SUM(cener,QD(cener)) / SUM(cener,QQ(cener))   ;

 g07EnerPriInd(cener)$(QD0(cener)*PD0(cener)) = QD(cener)*PD(cener)/(QD(cener)*PD0(cener))*100  ;

 g07EnerPriIndAg$SUM(cener,QD0(cener)*PD0(cener)) = SUM(cener,QD(cener)*PD(cener))/SUM(cener,QD(cener)*PD0(cener))*100  ;

 g07FosComp$SUM(cfoss,QD0(cfoss)*PD0(cfoss)) = (1/ERX)*SUM(cfoss,QD(cfoss)*PD(cfoss))
                                          /SUM(cfoss,QD(cfoss)*PD0(cfoss))*100;

 g07RenComp$SUM(crenw,QD0(crenw)*PD0(crenw)) = (1/ERX)*SUM(crenw,QD(crenw)*PD(crenw))
                                         /SUM(crenw,QD(crenw)*PD0(crenw))*100 ;

 g07FosRenRt $ g07RenComp0 = g07FosComp/g07RenComp*100;

 g07EnerSec = SUM(cener,QXC(cener)*PXC(cener))/SUM(c,QXC(c)*PXC(c))  ;

 g07EnerVaRt(a)$VVA0(a) = SUM((cener,ff)$map_c_f_a(cener,ff,a),FD(ff,a)*WFA(ff,a))/VVA(a)  ;
 
 g07EnerVaRtAg$SUM(a,VVA0(a)) = SUM((cener,ff,a)$map_c_f_a(cener,ff,a),FD(ff,a)*WFA(ff,a))/SUM(a,VVA(a))  ;
 
 g07EnerPrimStk("Export") = SUM(cener,QE(cener)*PE(cener))   ;

 g07EnerPrimStk("Import") = SUM(cener,QM(cener)*PM(cener))   ;

 g07EnerPrimStk("Domestic Demand") = SUM(cener,QD(cener)*PD(cener))   ;

 g07EnerRefn = SUM((cener,ff,aener)$map_c_f_a(cener,ff,aener),FD(ff,aener)*WFA(ff,aener))   ;

 g07EnerUse('Transport') = SUM((cener,ff,atrn)$map_c_f_a(cener,ff,atrn),FD(ff,atrn)*WFA(ff,atrn))   ;

 g07EnerUse('Industry') = SUM((cener,ff,aind)$map_c_f_a(cener,ff,aind),FD(ff,aind)*WFA(ff,aind))   ;

 g07EnerUse('Other') = SUM((cener,ff,a)$(NOT (aind(a) OR atrn(a)) AND map_c_f_a(cener,ff,a)),FD(ff,a)*WFA(ff,a))  ;

 g07EnerUse('Exports') = SUM(cener,QE(cener)*PE(cener))   ;

 g07PrimGdpRt(enEl1) $g07EnerPrimStk0(enEl1)= (g07EnerPrimStk(enEl1) /GDP);

 g07RefnGdpRt = (g07EnerRefn/GDP);

 g07UseGdpRt(enEl2)$g07EnerUse0(enel2) = (g07EnerUse(enel2) /GDP) ;

 g07RefnPrimRt$g07EnerPrim = g07EnerRefn/g07EnerPrim;

 g07UsePrimRt(enEl2)$g07EnerUse0(enEl2) = (g07EnerUse(enEl2)/g07EnerPrim);

*- Goal 8
 g08GDPPCGr = GDP/SUM(h,POPN0(h))   ;

 g08NetTrade = SUM(c,PE(c)*QE(c))-SUM(c,PM(c)*QM(c));

 g08RevComp(c)$(ce(c) AND cx(c)) = g08RevComp0(c) ;

 g08RevCompAg = SUM(c$(ce(c) AND cx(c)), g08RevComp(c))/SUM(c$(ce(c) AND cx(c)),1);

 g08FosGDPSh = SUM(cfoss,PXC(cfoss)*QXC(cfoss))/SUM(c,QXC(c))  ;

*- Goal 9
 g09ManVaSh = SUM(aind,VVA(aind))/SUM(a,VVA(a));

 g09ManVaPC =SUM(aind,VVA(aind))/SUM(h,POPN0(h));

 g08ManEmpSh = SUM((l,aind),FD(l,aind))/SUM((l,a),FD(l,a))  ;

 g08Exp = SUM(c,PE(c)*QE(c))   ;

 g08Imp = SUM(c,PM(c)*QM(c))   ;

 g08Open = (SUM(c,PE(c)*QE(c))+SUM(c,PM(c)*QM(c)))/GDP  ;

*-Goal 10
 g10LabSh = SUM((l,a),FD(l,a)*WFA(l,a))/SUM((f,a),FD(f,a)*WFA(f,a))  ;

 g10AgrEmp = SUM((l,aagr),FD(l,aagr)) ;

 g10AgrEmpSh = SUM((l,aagr),FD(l,aagr))/SUM((l,a),FD(l,a))  ;

 g10Skil$(SUM((lu,a),FD0(lu,a))) = SUM((ls,a),FD(ls,a))/SUM((lu,a),FD(lu,a));

 g10WageDifSkl$(SUM((lu,a),FD0(lu,a))) = (SUM((ls,a),FD(ls,a)*WFA(ls,a))/SUM((ls,a),FD(ls,a)))
                    /(SUM((lu,a),FD(lu,a)*WFA(lu,a))/SUM((lu,a),FD(lu,a)))  ;

 g10WageDifAgr = (SUM((l,aagr),FD(l,aagr)*WFA(l,aagr))/SUM((l,aagr),FD(l,aagr)))
                   /(SUM((l,a),FD(l,a)*WFA(l,a))/SUM((l,a),FD(l,a))) ;

 g10IncDiffHH(h,hp)$(YH(hp) AND POPN0(h) AND POPN0(hp)) = (YH(h)/POPN0(h))/(YH(hp)/POPN0(hp))-1;

 g10IncDiffHHAg$ (sum((h,hp), g10IncDiffHH0(h,hp))) = SUM((h,hp)$(ord(h)<card(hp)),g10IncDiffHH(h,hp))/ SUM((h,hp)$(ord(h)<card(hp)),1) ;

*- Goal 12
 g12RenSh$SUM(cener,QXC(cener)) = SUM(crenw,QXC(crenw))/SUM(cener,QXC(cener))  ;

*- Goal 13
 g13RenSh$SUM(cener,QXC(cener)) = SUM(crenw,QXC(crenw))/SUM(cener,QXC(cener))  ;

*-Goal 14
 g14FsSh = SUM(cfs,QXC(cfs))/GDP;

*- Goal 15
 g15NonAgri$SUM((n,a),FD(n,a)) = SUM((n,a)$(NOT aagr(a)),FD(n,a))/SUM((n,a),FD(n,a))  ;

*-Goal 17
 g17GDPPc = GDP/SUM(h,POPN0(h))   ;

 g17EGSh("MTAX") = MTAX    /YG  ;

 g17EGSh("ETAX") = ETAX    /YG  ;

 g17EGSh("DTAX") = DTAX    /YG  ;

 g17EGSh("FYTAX") = FYTAX   /YG  ;

 g17EGSh("ITAX") = ITAX    /YG  ;

 g17EGSh("STAX") = STAX    /YG  ;

 g17EGSh("FTAX") = FTAX    /YG  ;

 g17EGSh("VTAX") = VTAX    /YG  ;

 g17EGSh("HCTAX") = HCTAX   /YG  ;

 g17EGShAg = SUM(egEl,g17EGSh(egEl));
$offDotL

$ontext
*-Dictionary
 ag: aggregate
 sh: share
 av: average
 Rt: ratio
 ind:index
 fd: food
 fs: fish
 cal: calories
 pro: protein
 YD: disposable income
 Exp: export
 Imp: Import
 Tm:  tariff
 Cons: sonsumption
 Prod: production
 Sub: Subsidy
 FrV: Fruit and Vegetables
 Wat:  Water
 Use:  Use
 Ener: Energy
 SfSu: Self Sufficiency
 Fos: Fossil fuel
 Comp: Competitiveness
 Va: Value Added
$offtext
