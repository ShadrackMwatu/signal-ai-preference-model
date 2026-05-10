Parameter
 ASAM%samNo%(ss,ss)         Macro Social Accounting Matrix(1&2 are calibration 3 is postsim)
 ASAM%samNo%CHK(ss,ss)      Ratio of ASAM%samNo% to ASAM0 should be 1
 ASAM%samNo%BAL(ss)         Differences in Row and Column totals of ASAM%samNo%
 ASAM%samNo%DIFF(ss,ss)     Differences between ASAM and ASAM%samNo%
 ASAM%samNo%CNT             Count of non zero entries in DIFFASAM%samNo%

 SAM%samNo%(sac,sacp)      Micro SAM for checking model calibration

 SAM%samNo%CHK(sac,sac)    Ratio of SAM%samNo% to SAM should be 1
 SAM%samNo%DIFF(sac,sac)   Differences between SAM and SAM%samNo%
 SAM%samNo%CNT             Count of non zero entries in SAM%samNo%DIFF
 SAM%samNo%BAL(sac)        Balance of SAM%samNo%

*- #### Exports Block

 PWE_nchk%samNo%(c)       World price of exports in dollars
 PER_nchk%samNo%(c,w)     Domestic price of exports by activity a
 PD_nchk%samNo%(c)        Consumer price for domestic supply of commodity c

*- #### Imports Block

 PWM_nchk%samNo%(c)       World price of imports in dollars
 PMR_nchk%samNo%(w,c)        Domestic price of competitive imports of commodity c

*- ------- TRADE AND TRANSPORT MARGINS BLOCK ------------------------------

 PTT_nchk%samNo%(m)       Price of trade and transport margin m

*- ------- COMMODITY PRICE BLOCK ------------------------------------------

 PQS_nchk%samNo%(c)       Supply price of composite commodity c
 PQD_nchk%samNo%(cc)      Purchaser price of composite commodity c
 PQCD_nchk%samNo%(cc,h)   Purchaser price of aggregate commodity cag

*- ------- PRODUCTION BLOCK -----------------------------------------------

 PX_nchk%samNo%(a)        Composite price of output by activity a

*- CES aggregation functions for Level 1 of production nest

 PVA_nchk%samNo%(a)       Value added price for activity a
 PINT_nchk%samNo%(a)      Price of aggregate intermediate input

 WF_nchk%samNo%(ff)        Price of factor f

*- Commodity Output

 PXC_nchk%samNo%(c)       Producer price of composite domestic output

*- Activity Output

 PXAC_nchk%samNo%(a,c)    Activity commodity prices
;
