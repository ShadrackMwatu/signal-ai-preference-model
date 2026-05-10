*------------------------------------------------------------------------------
*------------------------------------------------------------------------------
*-
*-
*-   GAMS file : resassign.inc
*-
*-   @purpose  : Declares parameters used for reporting
*-   @author   :
*-   @date     :
*-   @since    :
*-   @refDoc   :
*-   @seeAlso  :
*-   @calledBy : *_experiment_*.gms.inc
*------------------------------------------------------------------------------
*------------------------------------------------------------------------------
*---------------  results analysis -------------------------------
$ontext
The various files for the analysis of results can be called here or by using
programme analyse.gms to carry out the same actions using results stored
in GDX

EACH COMPONENT IS INDEPENDENT, i.e., each component only makes use of the
results saved into the standard GDX results file that is produced by the
simulations module. This includes the levels values for the model varibales,
all the initial values of variables, all the model parameter values, all the
model and simulation sets
$offtext

*------- 1. Write out Levels results -----------------------------------
If(flow_cont("reslevel") = 1,

$SETGLOBAL resType Level
$INCLUDE 60_Report\resPopulate.inc
$INCLUDE 60_Report\resPopulateAggr.inc

  ) ;

*----------- 2. Macroeconomic Results ------------------------------------
*---- 3. Assign and Export Macroeconomic Tables

If(flow_cont("resmacro") = 1,

$INCLUDE 60_Report\resmacro.inc

  ) ;


*------------ 3. Structural Results -------------------------------------

$include 60_Report/resstruct.inc

*------------ 4. Welfare Results Analysis -------------------------------
*---- 5b. Assign and Export Welfare Results

If(flow_cont("reswelf") = 1,
$INCLUDE 60_Report\reswelf.inc
  ) ;

*---------- 5. Value Added Results --------------------------------------



*---------- 6. Percentage Changes in Variables --------------------------
If(flow_cont("resperc") = 1,

$IfTheni.dyna %mode% == dyna
$SETGLOBAL resType perc
result("%resType%",resVar,sac,sacp,sacpp,sacppp,%resElem1%)$SUM(tp$(ord(tp)=1),result("Level",resVar,sac,sacp,sacpp,sacppp,%resElemTp%))
                                         = result("Level",resVar,sac,sacp,sacpp,sacppp,%resElem1%)
                                                  /SUM(tp$(ord(tp)=1),result("Level",resVar,sac,sacp,sacpp,sacppp,%resElemTp%)) *100-100;
result("%resType%",resVar,sac,sacp,sacpp,sacppp,%resElem1%)$(ABS(result("%resType%",resVar,sac,sacp,sacpp,sacppp,%resElem1%))<1E-06) = 0;

sdgResult("%resType%",sdgGoal,sdgVar,sac,sacp,%resElem1%)$SUM(tp$(ord(tp)=1),sdgResult("Level",sdgGoal,sdgVar,sac,sacp,%resElemTp%))
                                         = sdgResult("Level",sdgGoal,sdgVar,sac,sacp,%resElem1%)
                                                  /SUM(tp$(ord(tp)=1),sdgResult("Level",sdgGoal,sdgVar,sac,sacp,%resElemTp%)) *100-100;
sdgResult("%resType%",sdgGoal,sdgVar,sac,sacp,%resElem1%)$(ABS(sdgResult("%resType%",sdgGoal,sdgVar,sac,sacp,%resElem1%))<1E-06) = 0;


resultAg("%resType%",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElem1%)$SUM(tp$(ord(tp)=1),resultAg("Level",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElemTp%))
                                         = resultAg("Level",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElem1%)
                                                  /SUM(tp$(ord(tp)=1),resultAg("Level",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElemTp%)) *100-100;
resultAg("%resType%",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElem1%)$(ABS(resultAg("%resType%",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElem1%))<1E-06) = 0;


$INCLUDE 60_Report\resPopulate.inc
$INCLUDE 60_Report\resPopulateAggr.inc
$endif.dyna
*---------- 7. Percentage Changes from baseline --------------------------

$SETGLOBAL resType PerBase
result("%resType%",resVar,sac,sacp,sacpp,sacppp,%resElem1%)$(result("Level",resVar,sac,sacp,sacpp,sacppp,%resElemBs%))
                                              = result("Level",resVar,sac,sacp,sacpp,sacppp,%resElem1%)
                                                  /result("Level",resVar,sac,sacp,sacpp,sacppp,%resElemBs%) *100-100;
*for the GHG set - not part of sac but hardcoded in model.gms
result("%resType%",resVar,ghg,sacp,sacpp,sacppp,%resElem1%)$(result("Level",resVar,ghg,sacp,sacpp,sacppp,%resElemBs%))
                                              = result("Level",resVar,ghg,sacp,sacpp,sacppp,%resElem1%)
                                                  /result("Level",resVar,ghg,sacp,sacpp,sacppp,%resElemBs%) *100-100;

result("%resType%",resVar,sac,sacp,sacpp,sacppp,%resElem1%)$(ABS(result("%resType%",resVar,sac,sacp,sacpp,sacppp,%resElem1%))<1E-06) = 0;

sdgResult("%resType%",sdgGoal,sdgVar,sac,sacp,%resElem1%)$sdgResult("Level",sdgGoal,sdgVar,sac,sacp,%resElemBs%)
                                         = sdgResult("Level",sdgGoal,sdgVar,sac,sacp,%resElem1%)
                                                  /sdgResult("Level",sdgGoal,sdgVar,sac,sacp,%resElemBs%) *100-100;
sdgResult("%resType%",sdgGoal,sdgVar,sac,sacp,%resElem1%)$(ABS(sdgResult("%resType%",sdgGoal,sdgVar,sac,sacp,%resElem1%))<1E-06) = 0;

resultAg("%resType%",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElem1%)$(resultAg("Level",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElemBs%))
                                              = resultAg("Level",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElem1%)
                                                  /resultAg("Level",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElemBs%) *100-100;

resultAg("%resType%",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElem1%)$(ABS(resultAg("%resType%",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElem1%))<1E-06) = 0;



$INCLUDE 60_Report\resPopulate.inc
$INCLUDE 60_Report\resPopulateAggr.inc

*---------- 8. Level Changes from baseline --------------------------
$SETGLOBAL resType DiffBase
result("%resType%",resVar,sac,sacp,sacpp,sacppp,%resElem1%)
                                              = result("Level",resVar,sac,sacp,sacpp,sacppp,%resElem1%)
                                                  - result("Level",resVar,sac,sacp,sacpp,sacppp,%resElemBs%);
*for the GHG set - not part of sac but hardcoded in model.gms
result("%resType%",resVar,ghg,sacp,sacpp,sacppp,%resElem1%)
                                              = result("Level",resVar,ghg,sacp,sacpp,sacppp,%resElem1%)
                                                  - result("Level",resVar,ghg,sacp,sacpp,sacppp,%resElemBs%);


result("%resType%",resVar,sac,sacp,sacpp,sacppp,%resElem1%)$(abs(result("%resType%",resVar,sac,sacp,sacpp,sacppp,%resElem1%))<1E-09) = 0;

sdgResult("%resType%",sdgGoal,sdgVar,sac,sacp,%resElem1%)
                                         = sdgResult("Level",sdgGoal,sdgVar,sac,sacp,%resElem1%)
                                                  -sdgResult("Level",sdgGoal,sdgVar,sac,sacp,%resElemBs%);
sdgResult("%resType%",sdgGoal,sdgVar,sac,sacp,%resElem1%)$(ABS(sdgResult("%resType%",sdgGoal,sdgVar,sac,sacp,%resElem1%))<1E-06) = 0;


$INCLUDE 60_Report\resPopulate.inc


*-reports that are relevant only for dynamic version
*---------- 9. Percentage Changes from baseline for the last year --------------------------
$ifthen.dyna1 %Mode% == dyna

$SETGLOBAL resType PerBaseLastYear

result("%resType%",resVar,sac,sacp,sacpp,sacppp,%resElem%)$(tlast(t)) = result("PerBase",resVar,sac,sacp,sacpp,sacppp,%resElem%);

sdgResult("%resType%",sdgGoal,sdgVar,sac,sacp,%resElem%)$(tlast(t))  = sdgResult("PerBase",sdgGoal,sdgVar,sac,sacp,%resElem%);


resultAg("%resType%",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElem%)$(tlast(t)) = resultAg("PerBase",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElem%);

resultAg("%resType%",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElem1%)$(ABS(resultAg("%resType%",resVar,sacAg,sacAgp,sacAgpp,sacAgppp,%resElem1%))<1E-06) = 0;


$INCLUDE 60_Report\resPopulate.inc
$INCLUDE 60_Report\resPopulateAggr.inc

*---------- 10. Percentage Changes from previuos period --------------------------
$SETGLOBAL resType YearPerc
result("%resType%",resVar,sac,sacp,sacpp,sacppp,%resElemTp%)$(ord(tp)>1 AND t1(tp) AND result("Level",resVar,sac,sacp,sacpp,sacppp,%resElemTpre%))
                                                             = result("Level",resVar,sac,sacp,sacpp,sacppp,%resElemTp%)
                                                              / result("Level",resVar,sac,sacp,sacpp,sacppp,%resElemTpre%)*100-100;

result("%resType%",resVar,sac,sacp,sacpp,sacppp,%resElem1%)$(abs(result("%resType%",resVar,sac,sacp,sacpp,sacppp,%resElem1%))<1E-09) = 0;

sdgResult("%resType%",sdgGoal,sdgVar,sac,sacp,%resElemTp%)$(ord(tp)>1 AND t1(tp) AND sdgResult("Level",sdgGoal,sdgVar,sac,sacp,%resElemTpre%))
                                         = sdgResult("Level",sdgGoal,sdgVar,sac,sacp,%resElemTp%)
                                                  / sdgResult("Level",sdgGoal,sdgVar,sac,sacp,%resElemTpre%)*100-100;

sdgResult("%resType%",sdgGoal,sdgVar,sac,sacp,%resElem1%)$(ABS(sdgResult("%resType%",sdgGoal,sdgVar,sac,sacp,%resElem1%))<1E-06) = 0;

$INCLUDE 60_Report\resPopulate.inc

$endif.dyna1

  ) ;




*-calculate percentage change from baseline



*--------------- end of DEMETRA results analysis ------------------------
