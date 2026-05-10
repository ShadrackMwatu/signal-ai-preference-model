$ontext
--------------------------------------------------------------------------------
 JRC.DEMETRA  version 1.0-alpha
 Dynamic Equilibrium Model for Economic developmenT, Environement & Agriculture

 GAMS file : contVar.inc
 @purpose  : Assign control variable values
 @author   : 
 @date     :
 @since    :
 @refDoc   :
 @seeAlso  :
 @calledBy :
--------------------------------------------------------------------------------
$offtext
*-------Control variables and parameters--------------------------------------

*- set experiment file name
$SETGLOBAL country Kenya

$SETGLOBAL experiment  experiment_%country%.xlsx

*-this is added to the result file names
$SETGLOBAL Mode dyna

*- this is the standard set elements for the results files
$SETGLOBAL resElem t,sim

*-this is used to write the results in every iteration of loop
$SETGLOBAL resElem1  t1,sim1
$SETGLOBAL resElemBs  t1,"base"
$SETGLOBAL resElemTp  tp,sim1
$SETGLOBAL resElemTpre  tp-1,sim1

$SETGLOBAL exp naip

*-this interactively asks if to run the BaU
*$call =ask T=radiobuttons M="Do you want to run the BaU simulation"  D="No|Yes" E=1|2 R="$SETGLOBAL runBaU %s-1" o=ask.inc
*$include ask.inc

*-this controls if BaU sim is run(=1) or not (=0) manually
$SETGLOBAL runBaU 1
