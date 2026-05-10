

*-HD: Reporting for Kenya Paper on Food Security
*prepare study specific tables

*-Production: Only agricultural

Parameter ProductionCommodity(restype,c,%resElem1%);
Parameter ProductionRegion(restype,a,%resElem1%);


ProductionCommodity(restype,cagr,%resElem1%) = result(restype,"QXC",cagr,"Nan","NaN","NaN",%resElem1%) ;

ProductionCommodity("perBase",cagr,%resElem1%)$ProductionCommodity("Level",cagr,%resElemBS%)
                                           = ProductionCommodity("Level",cagr,%resElem1%)
                                           /ProductionCommodity("Level",cagr,%resElemBS%)*100-100;

ProductionRegion(restype,aagr,%resElem1%) = SUM(cagr,result(restype,"QXAC",aagr,cagr,"NaN","NaN",%resElem1%) );

ProductionRegion("perBase",aagr,%resElem1%)= ProductionRegion("Level",aagr,%resElem1%)
                                      /ProductionRegion("Level",aagr,%resElemBS%)*100-100;


SET
ferdim
/
Production
Consumption
"Supply Price"
"Purchaser Price"
Export
Import
ExpProSh
ImpConSh
/
;
Parameter
FertilizerResult(ferdim,restype,%resElem1%) ;

FertilizerResult("Production","Level",%resElem1%) = SUM(cfer,result("Level","QXC",cfer,"Nan","NaN","NaN",%resElem1%)) ;
FertilizerResult("Production","PerBase",%resElem1%) = FertilizerResult("Production","Level",%resElem1%)/FertilizerResult("Production","Level",%resElemBs%)*100-100;
FertilizerResult("Production","DiffBase",%resElem1%) = FertilizerResult("Production","Level",%resElem1%)-FertilizerResult("Production","Level",%resElemBs%);

FertilizerResult("Consumption","Level",%resElem1%) = SUM(cfer,result("Level","QQ",cfer,"Nan","NaN","NaN",%resElem1%)) ;
FertilizerResult("Consumption","PerBase",%resElem1%) = FertilizerResult("Consumption","Level",%resElem1%)/FertilizerResult("Consumption","Level",%resElemBs%)*100-100 ;
FertilizerResult("Consumption","DiffBase",%resElem1%) = FertilizerResult("Consumption","Level",%resElem1%) - FertilizerResult("Consumption","Level",%resElemBs%);


FertilizerResult("Supply Price","Level",%resElem1%) = SUM(cfer,result("Level","PXC",cfer,"Nan","NaN","NaN",%resElem1%)*result("Level","QXC",cfer,"Nan","NaN","NaN",%resElem1%))
                                                      / SUM(cfer,result("Level","QXC",cfer,"Nan","NaN","NaN",%resElem1%));

FertilizerResult("Supply Price","PerBase",%resElem1%) = FertilizerResult("Supply Price","Level",%resElem1%) /FertilizerResult("Supply Price","Level",%resElem1%) * 100-100;
FertilizerResult("Supply Price","DiffBase",%resElem1%) = FertilizerResult("Supply Price","Level",%resElem1%) - FertilizerResult("Supply Price","Level",%resElem1%);

FertilizerResult("Purchaser Price","Level",%resElem1%) = SUM(cfer,result("Level","PQD",cfer,"Nan","NaN","NaN",%resElem1%)*result("Level","QD",cfer,"Nan","NaN","NaN",%resElem1%))
                                                         / SUM(cfer,result("Level","QD",cfer,"Nan","NaN","NaN",%resElem1%)) ;

FertilizerResult("Purchaser Price","PerBase",%resElem1%) = FertilizerResult("Purchaser Price","Level",%resElem1%)/FertilizerResult("Purchaser Price","Level",%resElemBs%) *100-100;
FertilizerResult("Purchaser Price","DiffBase",%resElem1%) = FertilizerResult("Purchaser Price","Level",%resElem1%) - FertilizerResult("Purchaser Price","Level",%resElemBs%);


FertilizerResult("Export","Level",%resElem1%) = SUM(cfer,result("Level","QE",cfer,"Nan","NaN","NaN",%resElem1%)) ;
FertilizerResult("Export","PerBase",%resElem1%) =  FertilizerResult("Export","Level",%resElem1%)/FertilizerResult("Export","Level",%resElem1%)*100-100;
FertilizerResult("Export","DiffBase",%resElem1%) =  FertilizerResult("Export","Level",%resElem1%) - FertilizerResult("Export","Level",%resElem1%);



FertilizerResult("Import","Level",%resElem1%) = SUM(cfer,result("Level","QM",cfer,"Nan","NaN","NaN",%resElem1%)) ;
FertilizerResult("Import","PerBase",%resElem1%) = FertilizerResult("Import","Level",%resElem1%) / FertilizerResult("Import","Level",%resElem1%)*100-100;
FertilizerResult("Import","DiffBase",%resElem1%) = FertilizerResult("Import","Level",%resElem1%) / FertilizerResult("Import","Level",%resElem1%)*100-100;


FertilizerResult("ExpProSh","Level",%resElem1%)$FertilizerResult("Production","Level",%resElem1%)
                                = FertilizerResult("Export","Level",%resElem1%)/FertilizerResult("Production","Level",%resElem1%);
FertilizerResult("ImpConSh","Level",%resElem1%)$FertilizerResult("Consumption","Level",%resElem1%)
                                = FertilizerResult("Import","Level",%resElem1%)/FertilizerResult("Consumption","Level",%resElem1%);

FertilizerResult("ExpProSh","PerBase",%resElem1%) = FertilizerResult("ExpProSh","Level",%resElem1%) - FertilizerResult("ExpProSh","Level",%resElemBS%);

FertilizerResult("ImpConSh","PerBase",%resElem1%) = FertilizerResult("ImpConSh","Level",%resElem1%) - FertilizerResult("ImpConSh","Level",%resElemBS%);


SET
cfood(c)            food commodities
reg                 regions
hhtype
map_a_reg(a,reg)    mapping between activities and regions
map_h_reg(h,reg)    mapping between households and regions
map_h_hhtype(h,hhtype) mapping between  households and hh type (rural vs urban)
ahhld(a)              household activities
amark(a)
chhld(c)
cmark(c)
map_chhld_cmark(c,c)  mapping between hh comms and marktd comms

SET
nutelement
/
kcal
prot
fat
/
;

Parameter NutConv(c,nutElement);

$gdxin %gdxF%\exp_in.gdx
$loaddc cfood reg hhtype map_a_reg map_h_reg map_h_hhtype ahhld chhld map_chhld_cmark NutConv
$gdxin


amark(a)$(NOT ahhld(a))=YES;
cmark(c)$(NOT chhld(c))=YES;

Parameter
CPIAgr(restype,%resElem1%)               CPI in agricultural commodities
CPIFood(restype,%resElem1%)              CPI in Food commodities
CPIReg(restype,reg,%resElem1%)           CPI in regions
CPIHHtype(restype,hhtype,%resElem1%)     CPI for HH types
CPIContainer(restype,*,reg,hhtype,%resElem1%)
comtotshAGRI(c,%resElem1%)
comtotshFOOD(c,%resElem1%)
comtotshREG(reg,c,%resElem1%)
comtotshHHtype(hhtype,c,%resElem1%)
;


ALIAS (cfood,cfoodp),(cagr,cagrp);


comtotshAGRI(cagr,%resElem1%) $(SUM(cagrp,SUM(h,result("Level","QCD",cagrp,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cagr,"Nan","NaN","NaN",%resElem1%) )
       + SUM((h,cag)$map_cag_c(cag,cagrp),result("Level","QCD2",cag,cagrp,h,"NaN",%resElem1%)*result("Level","PQD",cagrp,"Nan","NaN","NaN",%resElem1%) )))

    = (SUM(h,result("Level","QCD",cagr,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cagr,"Nan","NaN","NaN",%resElem1%) )
       + SUM((h,cag)$map_cag_c(cag,cagr),result("Level","QCD2",cag,cagr,h,"NaN",%resElem1%)*result("Level","PQD",cagr,"Nan","NaN","NaN",%resElem1%) ))
       / (SUM(cagrp,SUM(h,result("Level","QCD",cagrp,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cagr,"Nan","NaN","NaN",%resElem1%) )
       + SUM((h,cag)$map_cag_c(cag,cagrp),result("Level","QCD2",cag,cagrp,h,"NaN",%resElem1%)*result("Level","PQD",cagrp,"Nan","NaN","NaN",%resElem1%) )));

comtotshFOOD(cfood,%resElem1%) $(SUM(cfoodp,SUM(h,result("Level","QCD",cfoodp,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) )
       + SUM((h,cag)$map_cag_c(cag,cfoodp),result("Level","QCD2",cag,cfoodp,h,"NaN",%resElem1%)*result("Level","PQD",cfoodp,"Nan","NaN","NaN",%resElem1%) )))

    = (SUM(h,result("Level","QCD",cfood,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) )
       + SUM((h,cag)$map_cag_c(cag,cfood),result("Level","QCD2",cag,cfood,h,"NaN",%resElem1%)*result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) ))
       / (SUM(cfoodp,SUM(h,result("Level","QCD",cfoodp,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) )
       + SUM((h,cag)$map_cag_c(cag,cfoodp),result("Level","QCD2",cag,cfoodp,h,"NaN",%resElem1%)*result("Level","PQD",cfoodp,"Nan","NaN","NaN",%resElem1%) )));



comtotshREG(reg,cfood,%resElem1%) $(SUM(cfoodp,SUM(h$map_h_reg(h,reg),result("Level","QCD",cfoodp,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) )
       + SUM((h,cag)$(map_h_reg(h,reg) AND map_cag_c(cag,cfoodp)),result("Level","QCD2",cag,cfoodp,h,"NaN",%resElem1%)*result("Level","PQD",cfoodp,"Nan","NaN","NaN",%resElem1%) )))

    = (SUM(h$map_h_reg(h,reg),result("Level","QCD",cfood,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) )
       + SUM((h,cag)$(map_h_reg(h,reg) AND map_cag_c(cag,cfood)),result("Level","QCD2",cag,cfood,h,"NaN",%resElem1%)*result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) ))
       / (SUM(cfoodp,SUM(h$map_h_reg(h,reg),result("Level","QCD",cfoodp,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) )
       + SUM((h,cag)$(map_h_reg(h,reg) AND map_cag_c(cag,cfoodp)),result("Level","QCD2",cag,cfoodp,h,"NaN",%resElem1%)*result("Level","PQD",cfoodp,"Nan","NaN","NaN",%resElem1%) )));


comtotshHHtype(hhtype,cfood,%resElem1%) $(SUM(cfoodp,SUM(h$map_h_hhtype(h,hhtype),result("Level","QCD",cfoodp,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) )
       + SUM((h,cag)$(map_h_hhtype(h,hhtype) AND map_cag_c(cag,cfoodp)),result("Level","QCD2",cag,cfoodp,h,"NaN",%resElem1%)*result("Level","PQD",cfoodp,"Nan","NaN","NaN",%resElem1%) )))

    = (SUM(h$map_h_hhtype(h,hhtype),result("Level","QCD",cfood,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) )
       + SUM((h,cag)$(map_h_hhtype(h,hhtype) AND map_cag_c(cag,cfood)),result("Level","QCD2",cag,cfood,h,"NaN",%resElem1%)*result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) ))
       / (SUM(cfoodp,SUM(h$map_h_hhtype(h,hhtype),result("Level","QCD",cfoodp,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) )
       + SUM((h,cag)$(map_h_hhtype(h,hhtype) AND map_cag_c(cag,cfoodp)),result("Level","QCD2",cag,cfoodp,h,"NaN",%resElem1%)*result("Level","PQD",cfoodp,"Nan","NaN","NaN",%resElem1%) )));


CPIAgr("Level",%resElem1%) = SUM(cagr,comtotshAGRI(cagr,%resElem1%)* result("Level","PQD",cagr,"Nan","NaN","NaN",%resElem1%)  * (1 + result("Level","TV",cagr,"Nan","NaN","NaN",%resElem1%) )) ;
CPIFood("Level",%resElem1%) = SUM(cfood,comtotshFOOD(cfood,%resElem1%)* (result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%)  * (1 + result("Level","TV",cfood,"Nan","NaN","NaN",%resElem1%) )) ) ;
CPIReg("Level",reg,%resElem1%) = SUM(cfood,comtotshREG(reg,cfood,%resElem1%)* (result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%)  * (1 + result("Level","TV",cfood,"Nan","NaN","NaN",%resElem1%) )) ) ;
CPIhhtype("Level",hhtype,%resElem1%) = SUM(cfood,comtotshhhtype(hhtype,cfood,%resElem1%)* (result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%)  * (1 + result("Level","TV",cfood,"Nan","NaN","NaN",%resElem1%) )) ) ;

CPIAgr("perBase",%resElem1%)          $CPIAgr("Level",%resElemBs%)          =CPIAgr("Level",%resElem1%)          /CPIAgr("Level",%resElemBs%)          *100-100;
CPIFood("perBase",%resElem1%)         $CPIFood("Level",%resElemBs%)         =CPIFood("Level",%resElem1%)         /CPIFood("Level",%resElemBs%)         *100-100;
CPIREG("perBase",reg,%resElem1%)      $CPIREG("Level",reg,%resElemBs%)      =CPIReg("Level",reg,%resElem1%)      /CPIREG("Level",reg,%resElemBs%)      *100-100;
CPIhhtype("perBase",hhtype,%resElem1%)$CPIhhtype("Level",hhtype,%resElemBs%)=CPIhhtype("Level",hhtype,%resElem1%)/CPIhhtype("Level",hhtype,%resElemBs%)*100-100;


CPIAgr("perBase",%resElemBs%)           =  CPIAgr("Level",%resElemBs%)           ;
CPIFood("perBase",%resElemBs%)          =  CPIFood("Level",%resElemBs%)          ;
CPIREG("perBase",reg,%resElemBs%)       =  CPIREG("Level",reg,%resElemBs%)       ;
CPIhhtype("perBase",hhtype,%resElemBs%) =  CPIhhtype("Level",hhtype,%resElemBs%) ;


CPIContainer(restype,"Agricultural",'Nan','Nan',%resElem1%) = CPIAgr(restype,%resElem1%);
CPIContainer(restype,"Food",'Nan','Nan',%resElem1%) = CPIFood(restype,%resElem1%)       ;
CPIContainer(restype,"Regions",reg,'Nan',%resElem1%) = CPIReg(restype,reg,%resElem1%) ;
CPIContainer(restype,"HHType",'Nan',hhtype,%resElem1%) = CPIhhtype(restype,hhtype,%resElem1%) ;



*---------------- end of stg2_dev results analysis ------------------------

*-self sufficiency: dom/imp

*-prod/imports

Parameter shImports(*,restype,c,%resElem1%) Share of imports in total food supply;
Parameter shExports(*,restype,c,%resElem1%) Share of imports in total food supply;

shImports("agri","Level",cagr,%resElem1%)$result("Level","QQ",cagr,"Nan","NaN","NaN",%resElem1%)
                           = result("Level","QM",cagr,"Nan","NaN","NaN",%resElem1%)
                              /result("Level","QQ",cagr,"Nan","NaN","NaN",%resElem1%) *100;


shExports("agri","Level",cagr,%resElem1%)$result("Level","QXC",cagr,"Nan","NaN","NaN",%resElem1%)
                           = result("Level","QE",cagr,"Nan","NaN","NaN",%resElem1%)
                              /result("Level","QXC",cagr,"Nan","NaN","NaN",%resElem1%) *100;


shImports("agri","perBase",cagr,%resElem1%)$shImports("agri","Level",cagr,%resElemBs%)=shImports("agri","Level",cagr,%resElem1%)/shImports("agri","Level",cagr,%resElemBs%)*100-100;
shExports("agri","perBase",cagr,%resElem1%)$shExports("agri","Level",cagr,%resElemBs%)=shExports("agri","Level",cagr,%resElem1%)/shExports("agri","Level",cagr,%resElemBs%)*100-100
;

shImports("agri","perBase",cfood,%resElemBs%) =shImports("agri","Level",cfood,%resElemBs%);
shExports("agri","perBase",cfood,%resElemBs%) =shExports("agri","Level",cfood,%resElemBs%);


shImports("food","Level",cfood,%resElem1%)$result("Level","QQ",cfood,"Nan","NaN","NaN",%resElem1%)
                           = result("Level","QM",cfood,"Nan","NaN","NaN",%resElem1%)
                              /result("Level","QQ",cfood,"Nan","NaN","NaN",%resElem1%) *100;


shExports("food","Level",cfood,%resElem1%)$result("Level","QXC",cfood,"Nan","NaN","NaN",%resElem1%)
                           = result("Level","QE",cfood,"Nan","NaN","NaN",%resElem1%)
                              /result("Level","QXC",cfood,"Nan","NaN","NaN",%resElem1%) *100;


shImports("food","perBase",cfood,%resElem1%)$shImports("food","Level",cfood,%resElemBs%)=shImports("food","Level",cfood,%resElem1%)/shImports("food","Level",cfood,%resElemBs%)*100-100;
shExports("food","perBase",cfood,%resElem1%)$shExports("food","Level",cfood,%resElemBs%)=shExports("food","Level",cfood,%resElem1%)/shExports("food","Level",cfood,%resElemBs%)*100-100;

shImports("food","perBase",cfood,%resElemBs%) =shImports("food","Level",cfood,%resElemBs%);
shExports("food","perBase",cfood,%resElemBs%) =shExports("food","Level",cfood,%resElemBs%);

*-home prod/marktd prod
Parameter
shHPHC(restype,c,h,%resElem1%)   HPHC share in total consumption for each commodity and HH
shHPHCperBase(restype,c,%resElem1%) HPHC share in total consumption for each commodity
shHPHCperH(restype,h,%resElem1%) HPHC share in total consumption for each HH
shHPHCperHtype(restype,hhtype,%resElem1%) HPHC share in total consumption for each HH type (rur vs urb)
;

shHPHC("Level",chhld,h,%resElem1%)$(result("Level","QCDTotal",chhld,h,"NaN","NaN",%resElem1%) +SUM(c$map_chhld_cmark(chhld,c),result("Level","QCDTotal",c,h,"NaN","NaN",%resElem1%) ))
                                  = result("Level","QCDTotal",chhld,h,"NaN","NaN",%resElem1%)
                                      /(result("Level","QCDTotal",chhld,h,"NaN","NaN",%resElem1%)
                                         +SUM(c$map_chhld_cmark(chhld,c),result("Level","QCDTotal",c,h,"NaN","NaN",%resElem1%) )
                                        );





shHPHCperBase("Level",chhld,%resElem1%)= SUM(h,result("Level","QCDTotal",chhld,h,"NaN","NaN",%resElem1%) )
                                      /SUM(h,(result("Level","QCDTotal",chhld,h,"NaN","NaN",%resElem1%)
                                               +SUM(c$map_chhld_cmark(chhld,c),result("Level","QCDTotal",c,h,"NaN","NaN",%resElem1%) )
                                              )
                                           );

shHPHCperH("Level",h,%resElem1%)$SUM(cfood,(result("Level","QCDTotal",cfood,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) ))
                                    = SUM(chhld,result("Level","QCDTotal",chhld,h,"NaN","NaN",%resElem1%) *result("Level","PQD",chhld,"Nan","NaN","NaN",%resElem1%) *(1+result("Level","TV",chhld,"Nan","NaN","NaN",%resElem1%) ))
                                      /SUM(cfood,(result("Level","QCDTotal",cfood,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) *(1+result("Level","TV",cfood,"Nan","NaN","NaN",%resElem1%) )
                                                  )
                                           );



shHPHCperHtype("Level",hhtype,%resElem1%)$SUM(h$map_h_hhtype(h,hhtype),SUM(cfood,(result("Level","QCDTotal",cfood,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) *(1+result("Level","TV",cfood,"Nan","NaN","NaN",%resElem1%) ))))
                        =  SUM(h$map_h_hhtype(h,hhtype),SUM(chhld,result("Level","QCDTotal",chhld,h,"NaN","NaN",%resElem1%) *result("Level","PQD",chhld,"Nan","NaN","NaN",%resElem1%) *(1+result("Level","TV",chhld,"Nan","NaN","NaN",%resElem1%) )))
                                           /SUM(h$map_h_hhtype(h,hhtype),SUM(cfood,(result("Level","QCDTotal",cfood,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) *(1+result("Level","TV",cfood,"Nan","NaN","NaN",%resElem1%) )
                                                                                    )
                                                                             )
                                                );


shHPHC("perBase",chhld,h,%resElem1%)  $shHPHC("Level",chhld,h,%resElemBs%)  = shHPHC("Level",chhld,h,%resElem1%) /shHPHC("Level",chhld,h,%resElemBs%)  *100-100;
shHPHCperBase("perBase",chhld,%resElem1%)$shHPHCperBase("Level",chhld,%resElemBs%)= shHPHCperBase("Level",chhld,%resElem1%)/shHPHCperBase("Level",chhld,%resElemBs%)*100-100;
shHPHCperH("perBase",h,%resElem1%)    $shHPHCperH("Level",h,%resElemBs%)    = shHPHCperH("Level",h,%resElem1%)    /shHPHCperH("Level",h,%resElemBs%)    *100-100;
shHPHCperHtype("perBase",hhtype,%resElem1%)$shHPHCperHtype("Level",hhtype,%resElemBs%)    = shHPHCperHtype("Level",hhtype,%resElem1%)    /shHPHCperHtype("Level",hhtype,%resElemBs%)    *100-100;


shHPHC("perBase",chhld,h,%resElemBs%)        = shHPHC("Level",chhld,h,%resElemBs%)*100 ;
shHPHCperBase("perBase",chhld,%resElemBs%)      = shHPHCperBase("Level",chhld,%resElemBs%)*100;
shHPHCperH("perBase",h,%resElemBs%)          = shHPHCperH("Level",h,%resElemBs%)*100    ;
shHPHCperHtype("perBase",hhtype,%resElemBs%) = shHPHCperHtype("Level",hhtype,%resElemBs%)*100 ;

*-composition of food consumption & share of consumption foods in total cosunmption (value)
Parameter shConsStruct(*,restype,h,*,%resElem1%) share of  foods consumptionin total cosunmption (value);

shConsStruct("all","Level",h,c,%resElem1%)$SUM(cp,result("Level","QCDTotal",cp,h,"NaN","NaN",%resElem1%) )
                           =   result("Level","QCDTotal",c,h,"NaN","NaN",%resElem1%) *result("Level","PQD",c,"Nan","NaN","NaN",%resElem1%) *(1+result("Level","TV",c,"Nan","NaN","NaN",%resElem1%) )
                                  /SUM(cp,result("Level","QCDTotal",cp,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cp,"Nan","NaN","NaN",%resElem1%) *(1+result("Level","TV",cp,"Nan","NaN","NaN",%resElem1%) ));


shConsStruct("foodAll","Level",h,cfood,%resElem1%)$SUM(c,result("Level","QCDTotal",cfood,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) *(1+result("Level","TV",cfood,"Nan","NaN","NaN",%resElem1%) ))
                           =   result("Level","QCDTotal",cfood,h,"NaN","NaN",%resElem1%)
                                  /SUM(c,result("Level","QCDTotal",cfood,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) *(1+result("Level","TV",cfood,"Nan","NaN","NaN",%resElem1%) ));


shConsStruct("foodsh","Level",h,"FOOD",%resElem1%)$SUM(c,result("Level","QCDTotal",c,h,"NaN","NaN",%resElem1%) *result("Level","PQD",c,"Nan","NaN","NaN",%resElem1%) *(1+result("Level","TV",c,"Nan","NaN","NaN",%resElem1%) ))
                           =   100*SUM(cfood,result("Level","QCDTotal",cfood,h,"NaN","NaN",%resElem1%) *result("Level","PQD",cfood,"Nan","NaN","NaN",%resElem1%) *(1+result("Level","TV",cfood,"Nan","NaN","NaN",%resElem1%) ))
                                  /SUM(c,result("Level","QCDTotal",c,h,"NaN","NaN",%resElem1%) *result("Level","PQD",c,"Nan","NaN","NaN",%resElem1%) *(1+result("Level","TV",c,"Nan","NaN","NaN",%resElem1%) ));


shConsStruct("all","perBase",h,c,%resElem1%)$shConsStruct("all","Level",h,c,%resElemBs%)=shConsStruct("all","Level",h,c,%resElem1%)/shConsStruct("all","Level",h,c,%resElemBs%)*100-100;
shConsStruct("foodall","perBase",h,c,%resElem1%)$shConsStruct("foodall","Level",h,c,%resElemBs%)=shConsStruct("foodall","Level",h,c,%resElem1%)/shConsStruct("foodall","Level",h,c,%resElemBs%)*100-100;
shConsStruct("foodsh","perBase",h,"FOOD",%resElem1%)$shConsStruct("foodsh","Level",h,"FOOD",%resElemBs%)=shConsStruct("foodsh","Level",h,"FOOD",%resElem1%)/shConsStruct("foodsh","Level",h,"FOOD",%resElemBs%)*100-100;

shConsStruct("all","perBase",h,c,%resElem1%)          =shConsStruct("all","Level",h,c,%resElemBs%)          ;
shConsStruct("foodall","perBase",h,c,%resElem1%)      =shConsStruct("foodall","Level",h,c,%resElemBs%)      ;
shConsStruct("foodsh","perBase",h,"FOOD",%resElemBs%)=shConsStruct("foodsh","Level",h,"FOOD",%resElemBs%)  ;


*-  nutrition

Parameter NutritionCH(restype,nutElement,c,h,%resElem1%);
Parameter NutritionH(restype,nutElement,h,%resElem1%);
Parameter NutritionHperBase(restype,nutElement,h,%resElem1%);

NutritionCH("Level",nutElement,c,h,%resElem1%)=NutConv(c,nutElement)*result("Level","QCDTotal",c,h,"NaN","NaN",%resElem1%) ;
NutritionH("Level",nutElement,h,%resElem1%)=SUM(C,NutConv(c,nutElement)*result("Level","QCDTotal",c,h,"NaN","NaN",%resElem1%) );

NutritionCH("perBase",nutElement,c,h,%resElem1%)$NutritionCH("Level",nutElement,c,h,%resElemBs%)=NutritionCH("Level",nutElement,c,h,%resElem1%)/NutritionCH("Level",nutElement,c,h,%resElemBs%)*100-100;
NutritionH("perBase",nutElement,h,%resElem1%)$NutritionH("Level",nutElement,h,%resElemBs%)=NutritionH("Level",nutElement,h,%resElem1%)/NutritionH("Level",nutElement,h,%resElemBs%)*100-100;

*NutritionCH("perBase",nutElement,c,h,%resElemBs%)=NutritionCH("Level",nutElement,c,h,%resElemBs%)  ;
*NutritionH("perBase",nutElement,h,%resElemBs%)   =NutritionH("Level",nutElement,h,%resElemBs%)    ;

*-perBaseapita values

*-calculate populations
Parameter Population(h,%resElem1%);

Population(h,%resElem1%) = SUM(l,result("Level","FSI",h,l,"NaN","NaN",%resElem1%) );

NutritionHperBase("Level",nutElement,h,%resElem1%)= NutritionH("Level",nutElement,h,%resElem1%)/SUM(l,result("Level","FSI",h,l,"NaN","NaN",%resElem1%) );
NutritionHperBase("perBase",nutElement,h,%resElem1%)$NutritionHperBase("Level",nutElement,h,%resElemBs%)
                                               =NutritionHperBase("Level",nutElement,h,%resElem1%)/NutritionHperBase("Level",nutElement,h,%resElemBs%)*100-100;
NutritionHperBase("perBase",nutElement,h,%resElemBs%)=0;



*-Production

PArameter Production(restype,*,sac,%resElem1%);

Production("Level","HPHC",cmark,%resElem1%)$(cagr(cmark) OR cfood(cmark))=SUM((a,chhld)$map_chhld_cmark(chhld,cmark),result("Level","QXAC",a,chhld,"NaN","NaN",%resElem1%) );
Production("Level","Marketed",cmark,%resElem1%)$(cagr(cmark) OR cfood(cmark))=SUM(a,result("Level","QXAC",a,cmark,"NaN","NaN",%resElem1%) );

Production("Level","Total",cmark,%resElem1%)$(cagr(cmark) OR cfood(cmark))=Production("Level","HPHC",cmark,%resElem1%)+Production("Level","Marketed",cmark,%resElem1%);

*-correct water
*Production("Level","MArketed","chwatr",%resElem1%)=Production("Level","HPHC","c_watr",%resElem1%);
*Production("Level","HPHC","c_watr",%resElem1%)=0;
*Production("Level","Total","chwatr",%resElem1%)=0;

Production("Level","Total","c_watr",%resElem1%)=Production("Level","HPHC","c_watr",%resElem1%)+Production("Level","Marketed","c_watr",%resElem1%);

*-column sums
Production("Level","HPHC","total",%resElem1%)     =SUM(c,Production("Level","HPHC",c,%resElem1%)    )   ;
Production("Level","Marketed","total",%resElem1%) =SUM(c,Production("Level","Marketed",c,%resElem1%))   ;
Production("Level","Total","total",%resElem1%)    =SUM(c,Production("Level","Total",c,%resElem1%)   )   ;

Production("Level","HPHC","Foodtotal",%resElem1%)     =SUM(c$(NOT (cagr(c) OR cliv(c))),Production("Level","HPHC",c,%resElem1%)    )   ;
Production("Level","Marketed","Foodtotal",%resElem1%) =SUM(c$(NOT (cagr(c) OR cliv(c))),Production("Level","Marketed",c,%resElem1%))   ;
Production("Level","Total","Foodtotal",%resElem1%)    =SUM(c$(NOT (cagr(c) OR cliv(c))),Production("Level","Total",c,%resElem1%)   )   ;

SET cCropC(c) commodities with only commercial production
/
c_cott
c_sugr
c_coff
c_tea
c_toba
c_ocrp
/;

*-agriproduction
Production("Level","HPHC","Croptotal",%resElem1%)     =SUM(cagr,Production("Level","HPHC",cagr,%resElem1%)    )   ;
Production("Level","Marketed","Croptotal",%resElem1%) =SUM(cagr,Production("Level","Marketed",cagr,%resElem1%))   ;
Production("Level","Total","Croptotal",%resElem1%)    =SUM(cagr,Production("Level","Total",cagr,%resElem1%)   )   ;


Production("Level","HPHC","CropCtotal",%resElem1%)     =SUM(cCropC,Production("Level","HPHC",cCropC,%resElem1%)    )   ;
Production("Level","Marketed","CropCtotal",%resElem1%) =SUM(cCropC,Production("Level","Marketed",cCropC,%resElem1%))   ;
Production("Level","Total","CropCtotal",%resElem1%)    =SUM(cCropC,Production("Level","Total",cCropC,%resElem1%)   )   ;

Production("Level","HPHC","CropHtotal",%resElem1%)     =  Production("Level","HPHC","Croptotal",%resElem1%)     - Production("Level","HPHC","CropCtotal",%resElem1%)    ;
Production("Level","Marketed","CropHtotal",%resElem1%) =  Production("Level","Marketed","Croptotal",%resElem1%) - Production("Level","Marketed","CropCtotal",%resElem1%);
Production("Level","Total","CropHtotal",%resElem1%)    =  Production("Level","Total","Croptotal",%resElem1%)    - Production("Level","Total","CropCtotal",%resElem1%)   ;

Production("Level","HPHC","Livetotal",%resElem1%)     =SUM(cliv,Production("Level","HPHC",cliv,%resElem1%)    )   ;
Production("Level","Marketed","Livetotal",%resElem1%) =SUM(cliv,Production("Level","Marketed",cliv,%resElem1%))   ;
Production("Level","Total","Livetotal",%resElem1%)    =SUM(cliv,Production("Level","Total",cliv,%resElem1%)   )   ;

Production("Level","HPHC","AgriTotal",%resElem1%)     = Production("Level","HPHC","Croptotal",%resElem1%)     + Production("Level","HPHC","Livetotal",%resElem1%)     ;
Production("Level","Marketed","AgriTotal",%resElem1%) = Production("Level","Marketed","Croptotal",%resElem1%) + Production("Level","Marketed","Livetotal",%resElem1%) ;
Production("Level","Total","AgriTotal",%resElem1%)    = Production("Level","Total","Croptotal",%resElem1%)    + Production("Level","Total","Livetotal",%resElem1%)    ;

Production("perBase","HPHC",sac,%resElem1%)    $Production("Level","HPHC",sac,%resElemBs%)    =100*Production("Level","HPHC",sac,%resElem1%)    /Production("Level","HPHC",sac,%resElemBs%)    -100 ;
Production("perBase","Marketed",sac,%resElem1%)$Production("Level","Marketed",sac,%resElemBs%)=100*Production("Level","Marketed",sac,%resElem1%)/Production("Level","Marketed",sac,%resElemBs%)-100 ;
Production("perBase","Total",sac,%resElem1%)   $Production("Level","Total",sac,%resElemBs%)   =100*Production("Level","Total",sac,%resElem1%)   /Production("Level","Total",sac,%resElemBs%)   -100 ;

Production("perBase","HPHC",sac,%resElemBs%)     =Production("Level","HPHC",sac,%resElemBs%)    ;
Production("perBase","Marketed",sac,%resElemBs%) =Production("Level","Marketed",sac,%resElemBs%);
Production("perBase","Total",sac,%resElemBs%)    =Production("Level","Total",sac,%resElemBs%)   ;




*-migration
Parameter FacSup(restype,h,%resElem1%);

FacSup('Level',h,%resElem1%)=SUM(l,result('level',"FSI",l,h,"NaN","NaN",%resElem1%))*samscal*7.715629268;
FacSup('perBase',h,%resElem1%)$FacSup('Level',h,%resElemBs%)=FacSup('level',h,%resElem1%)/FacSup('Level',h,%resElemBs%)*100-100 ;

*-unload tables
Execute_Unload  '%resultF%\tables.gdx',

CPIAgr
CPIFood
CPIReg
CPIHHtype
CPIContainer
shImports
shExports
shHPHC
shHPHCperBase
shHPHCperH
shHPHCperHtype
shConsStruct
NutritionH
NutritionCH
NutritionHperBase
Production
resultMacro
FacSup
Population
FertilizerResult
;

*Execute 'Gdxxrw i=%resultF%\tables.gdx o=%resultF%\AfrEcoTables9_Fert5.xlsx index=layoutTable!a2'
*Execute 'Gdxxrw i=%resultF%\%mode%_%exp%_resLevel.gdx o=%resultF%\AfrEcoTables9_Fert5.xlsx index=layoutLev!a2'
*Execute 'Gdxxrw i=%resultF%\%mode%_%exp%_reswelf.gdx o=%resultF%\AfrEcoTables9_Fert5.xlsx index=layoutWelf!a2'
$exit
Execute 'Gdxxrw i=%resultF%\tables.gdx o=%resultF%\AfrEcoTables9_%exp%4.xlsx index=layoutTable!a2'
Execute 'Gdxxrw i=%resultF%\%mode%_%exp%_resLevel.gdx o=%resultF%\AfrEcoTables9_%exp%4.xlsx index=layoutLev!a2'
Execute 'Gdxxrw i=%resultF%\%mode%_%exp%_reswelf.gdx o=%resultF%\AfrEcoTables9_%exp%4.xlsx index=layoutWelf!a2'



