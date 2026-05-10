*------------------------------------------------------------------------------
*-------------------------------------------------------------------------------
*--   DEMETRA v1.0-alpha
*--
*--   GAMS file : calibchk_declare.inc
*--
*--   @purpose  : Declares the parameters for calibration
*--   @author   :
*--   @date     :
*--   @since    :
*--   @refDoc   :
*--   @seeAlso  :
*--   @calledBy : model.gms, dynamic simulations
*-------------------------------------------------------------------------------
*-------------------------------------------------------------------------------


SET
dest                destinations for margins
/
domes
expo
/
;
PARAMETERS

*-- ------- NORMALISED PRICE BLOCK -----------------------------------------
ER0(w)              Exchange rate for each trade partner (domestic per partners'unit)
ERX0                Trade weighted overall exchange rate (domestic per partners'unit)
PD0(c)              Consumer price for domestic supply of commodity c
PE0(c)              Domestic price of exports by commodity c
PER0(c,w)           Domestic price of exports by commodity c from trade part. w
PM0(c)              Domestic price of competitive imports c
PMR0(w,c)           Domestic price of competitive imports c from trade part. w
PX0(a)              Composite price of output by activity a
PXC0(c)             Producer price of composite domestic output
PXAC0(a,c)          Activity commodity prices
PQS0(c)             Supply price of composite commodity c

TTTRANS(m,c,sac,dest) Trade and transport margin transactions by destination
TTTRANSCHK(m,c)     CHECK on TTTRANS
totsupp(c)          total commodity supply at basic prices
totdemd(c)          total commodity demand at purchaser prices
ZETAE0(c)           Preference shifter for exports
ZETAER0(c,w)        Preference shifter for exports
ZETAM0(w,c)          Preference shifter for imports

*-- ## Initial values for variables
PWE0(c)             World price of exports in dollars
QE0(c)              Domestic output exported by commodity c
QER0(c,w)              Domestic output exported by commodity c to trade part. w
QD0(c)              Domestic demand for commodity c

*-- ## for CET function 1st level nest
atR(c)               Shift for Armington CET function
gammaR(c,w)            Share for Armington CET function
rhotR(c)             Elasticity for Output Armington CET function


*-- ## for CET function 2nd level nest
at(c)               Shift for Armington CET function
gamma(c)            Share for Armington CET function
rhot(c)             Elasticity for Output Armington CET function

*-- ## for Export Demand functions
econ(c,w)             constant for export demand equations
pwse(c,w)             world price of export substitutes
eta(c,w)              export demand elasticity

*-- ## Initial values for variables
PWM0(c)             World price of imports in dollars
QM0(c)              Imports of commodity c
QMR0(w,c)           Imports of commodity c from trade part. w
QQ0(c)              Supply of composite commodity c

*-- ## for Armington/CES functions Level 1
acR(c)               Shift for Armington CES function
deltaR(w,c)          Share for Armington CES function
rhocR(c)             Elasticity for Armington CES function

*-- ## for Armington/CES functions Level 2
ac(c)               Shift for Armington CES function
delta(c)            Share for Armington CES function
rhoc(c)             Elasticity for Armington CES function

*-- ## Initial values for variables
PTT0(m)             Price of trade and transport margin m
QTT0(m)             Quantity of trade and transport margin m
QTTD0(c)            Intermediate input use for trade and transport margin m

*-- ## input output coefficients
IOQTTQQ0(m,c)       quantity of margin m used per unit of domestic demand QQ
ioqttqe(m,c,w)      quantity of margin m used per unit of export demand QE
ioqtdqtt(c,m)       quantity of commodity c used to produce a unit of margin m


etatr               elasticity of trade margin wrt infrastructure investment

PQD02(cc)           Purchaser price of composite commodity c
PQD0(cc)            Purchaser price of composite commodity c
PQDDIST0(cc,a)      Sectoral proportion for factor prices in r
PQCD0(cc,h)         Purchaser price of aggregate commodity cag by h
PQC0(cc,h)    price paid by consumers for consumed commodities
pqd2dist(cc,cc,h)   Distribution parameter for PQD2


*-- ## Initial values for variables
CPI0                Consumer price index
PPI0                Producer (domestic) price index
VQCD0(c)            Value of HH consumption

*-- ## Price index weights
COMTOTSH0(cc)       Share of commodity c in total commodity demand
comthhsh(c,h)       Share of commodity c in commodity demand by hhold h
vddtotsh0(c)         Share of value of domestic output for the domestic market
comtotshCHK         CHECK on comtotsh

*-- ## tax rates for initialisation
tv02(cc)            VAT rates for initialisation


*-- ## Initial values for variables
QX0(a)              Domestic production by activity a
QXC0(c)             Domestic production by commodity c
PVA0(a)             Value added price for activity a
PINT0(a)            Price of aggregate intermediate input
QINT0(a)            Aggregate quantity of intermediates used by activity a
QVA0(a)             Quantity of aggregate value added for level 1 production
VVA0(a)             Value of Value added (sum of value of natural factors)
QXAC0(a,c)          Domestic commodity output by each activity
QINTD0(c,a)         Intermediate input demand by activity a for commodity c
WF0(ff)             Price of factor f
WFA0(ff,a)          Sectoral price of factor f
WFDIST0(ff,a)       Sectoral proportion for factor prices
FD0(ff,a)           Demand for factor f by activity a
FSI0(ins,ff)        Factor supplies from institution ins by factor f
fsia(ins,ff)        Factor supplies from institution ins by factor f for updating
FS0(ff)             Supply of factor f
UNEMP0(ff)          Unemployment

FDTOT0(f)          total demand for a factor by activity
FSI0_bsh(ins,f)    base share for factor supply by institution
factuse_chk(f)   check on labor force

chk_fd(f)            Check on FD

*-- Rates of return on factors
ror_f(f)            Rates of return by factors type f

*-- Technology and Adjustment factors
AD0(ff,a)           Total efficiency Shifter
ADFD0(ff,a)         Shift for factor and activity specific efficiency
ADFDA(ff,a)         Shift for factor and activity specific efficiency to transfer between periods
ADFH0(ff,h)         Shift for factor and household specific efficiency
ADFHA(ff,h)         Shift for factor and household specific efficiency to transfer between periods
numHH(ff)           number of Households that own factor type ff - used for ADFH calculations

*-- CES aggregation functions 
adfag0(ff,a)        Shift for factor and activity specific efficiency
rhofd(ff,a)         Elasticity for CES prodn fns for Aggregated FD
iofdfag(ff,ff,a)    CES Share for Aggregated FD fag using ff by a
deltafd(ff,ff,a)    CES Share for Aggregated FD fag using ff by a

*-- ### adding efficiency varaiable for aggr at all levels of production nest
adfagb(ff,a)        Shift for land-water aggr at all levels of production nest
dadfag(ff,a)        Change in base shift for land-water aggr at all levels of production nest
ADFAGfADJ0(ff)      Scaling Factor for Shift for aggregate
ADFAGaADJ0(a)       Scaling Factor for Shift for activities
ADFAGADJ0           Scaling Factor for Shift for

*-- Intermediate Input Demand
ioqtdqd(c,a)        intermediate input output coefficients

*-- Commodity Output
adxc(c)             Shift for commodity output CES aggregation
deltaxc(a,c)        Share for commodity output CES aggregation
rhocxc(c)           Elasticity for commodity output CES aggregation

*-- Activity Output
ioqxacqx(a,c)       Share of commodity c in output by activity a
IOQXACQXV0(a,c)     Share of commodity c in output by activity a

*-- CET output functions
ati(a)              Shift for Armington CET function
gammai(a,c)         Share for Armington CET function per activity
rhoti(a)            Elasticity for Output Armington CET function
cti(a,c)            Shift for Armington CET function for commodity
FSL0(f)             Factors supplied for leisure
FSIL0(ins,f)        Factors supplied for leisure by institution
FSM0(f)             Factors supplied to the market
FSIM0(f,ins,fp,insp)        Factors supplied to the market by institution

NutVal0(nutElem,h)  Nutrition indicator values

tf02(ff,a)          tf for calibration of production functions
deltaxcchk(c)       CHECK on deltaxc

*-- ## Initial values for variables
YF0(f)              Income to factor f
YFDISP0(f)          Factor income for distribution after depreciation
YFINS0(f)           Factor income distributed to domestic non govt institutions
FSISH0(ins,f)       Shares of factor f supplied by institution insw
FSISH0chk(f)        CHECK on FSISH0
INSVA0(ins,f)       Factor income after deprecn distribution to institn insw

*-- ## FACTOR MOBILITY BLOCK
*WMIGR0(f,fp)    Wage ratio for factor mobility
*WMIGRA(f,fp)    Wage ratio for factor mobility for updating

*-- ## Savings Expenditures
deprec(ff)          depreciation rate by factor f

*-- ## Transfer Expenditures
hovash(h,f)         Share of income from factor f to household h
entvash(e,f)        Share of income from factor f to enterprise e
govvash(f)          Share of income from factor f to government
worvash(w,f)        Share of income from factor f to RoW
hovashchk(h,f)      Share of income from factor f to household h
entvashchk(e,f)     Share of income from factor f to enterprise e

*-- ## Initial values for variables
YH0(h)              Income to household h
YH_cap0(h)          Income per capita adult equiv to household h
HOHO0(h,hp)         Inter household transfer
HEXP0(ins)          Household consumption expenditure
HEXP_cap0(h)        Household consumption expenditure per capita adult equiv
QCD0(cc,h)          Household consumption by commodity cc
QCD20(cag,cc,h)     Household consumption by com'dy cces used in com'dy cag

*-- ## Transfer Expenditures
hohosh(h,hp)        Share of hhold h after tax and saving income transferred to hp
hohoconst(h,hp)     interhousehold transfers

*Remittances from migration
hohosh_mig(f,h,hp)  Remittances from migration

*-- ## Consumption Expenditures

*-- # Cobb Douglas Utility function
comhoav(cc,h)       Household consumption shares
comhoav1(c,h)       Household consumption shares
alphah(cc,h)        Expenditure share by commodity c for household h
alphah1(c,h)        Expenditure share by commodity c for household h

*-- # Stone-Geary Utility function
sumelast(h)         Weighted sum of income elasticities
yhelast(cc,h)       Normalised  household income elasticities
beta(cc,h)          Marginal budget shares
hexps(h)            Subsistence consumption expenditure
frisch(h)           Elasticity of the marginal utility of income
qcdconst(cc,h)      Volume of subsistence consumption

*-- # CES Utility function
rhocd(cc,h)         Elasticity for CES utility fns for Aggregated QCD
deltacd(cc,cc,h)    CES share Aggregated QCD
deltacdCHK(cc,h)    Check on CES share Aggregated QCD
accd(cc,h)          Shift for CES aggregated QCD

*-- # Institution and Household Migration


comhoav1chk(h)      Check on comhoav1
comhoavchk(h)       Check on comhoav
elasttest(cc,h)     Checking elasticities as intended
betaCHK(h)          CHECK on beta
hexpsCHK(h)         CHECK on hexps
alphahCHK(cc,h)     CHECK on alphah
alphahCHK2(h)       CHECK on sum of alphah
PQD20(cag,cces,h)
deltacd2(cc,cc,h)
deltacd2CHK(cc,cc,h)

*-- ## Initial values for scaling variables
QEDADJ0       Enterprise demand volume Scaling Factor
HEADJ0        Scaling factor for enterprise transfers to households

*-- ## Initial values for variables
YE0(e)              Enterprise income
HOENT0(h,e)         Household Income from enterprise e
GOVENTSH0           Share of entp. income after tax save and consump to govt
GOVENT0(e)          Government income from enterprise e
QED0(c,e)           Enterprise consumption by commodity c
VED0(e)             Value of enterprise consumption expenditure

*-- ## Transfer Expenditures
hoentconst(h,e)     transfers to hhold h from enterprise e (nominal)
hoentsh(h,e)        Share of entp. income after tax save and consump to hhold
goventsh(e)         Share of entp. income after tax save and consump to govt

*-- ## Consumption Expenditures
qedconst(c,e)       Enterprise demand volume

*-- ## Initial values for overall scaling variables
TEADJ0(w)           Export subsidy Scaling Factor
TMADJ0(w,cc)        Tarrif rate Scaling Factor
TSADJ0              Sales tax rate scaling factor
THCADJ0             HH specific sales tax scaling factor
TVADJ0              Value added tax rate scaling factor
TXADJ0              Indirect Tax Scaling Factor
TXAADJ0             Indirect Tax Scaling Factor
TFADJ0              Factor Use Tax Scaling Factor
TYFADJ0             Factor Tax Scaling Factor
TYHADJ0             Household Income Tax Scaling Factor
TYADJ0              Household and Enterprise Income Tax Scaling Factor
TYEADJ0             Enterprise income tax Scaling Factor
THCADJ0             HH specific comm tax (for food aid)

*-- ## Initial values for partial scaling variables
DTE0(w)             Partial Export tax rate scaling factor
DTM0(w)             Partial Tariff rate scaling factor
DTS0                Partial Sales tax rate scaling factor
DTHC0               Partial HH specific sales tax
DTV0                Partial Value added tax rate scaling factor
DTX0                Partial Indirect tax rate scaling factor
DTF0                Partial adjustment to factor use tax by activity
DTYF0               Partial direct tax on factor rate scaling factor
DTYH0               Partial direct tax on household rate scaling factor
DTY0                Partial direct tax on hhold and enterprise rate scaling factor
DTYE0               Partial direct tax on enterprise rate scaling factor
DVTAX0              Partial Value added tax scaling factor


*-- ## Initial tax revenues
MTAX0               Tariff revenue
ETAX0               Export tax revenue
DTAX0               Direct Income tax revenue
FYTAX0              Factor Income tax revenue
ITAX0               Indirect tax revenue
FTAX0               Factor use tax revenue
STAX0               Sales tax revenue
VTAX0               Value added tax revenue
HCTAX0              HH specific comm tax (for food aid)

*-- ## Initial tax rates
TE0(c,w)            Export subsidy rate
TM0(w,c)            Tariff rates
TS0(c)              Sales tax rates
THC0(h,c)           HH specific sales tax
TV0(cc)             Value added tax rates
TYF0(f)             Factor Income tax rate
TX0(a)              Indirect tax rate on activity a
TF0(ff,a)           Factor use tax rate
TYH0(h)             Direct tax rate on household h
TYE0(e)             Direct tax rate on enterprises
THC0(h,c)           Household specific commodity tax (for food aid)

*-- ## base tax rates
teb(c,w)            Export subsidy rate
tmb(w,c)            Tariff rate on commodity c
tsb(c)              Sales tax rates
thcb(h,c)           HH specific sales tax
tvb(cc)             Value added tax rates
tyfb(f)             Factor Income tax rate
txb(a)              Indirect tax rate on activity a
txab(a)             Indirect tax rate on activity a
tfb(ff,a)           Factor use tax rate
tyhb(h)             Direct tax rate on household h
tyeb(e)             Direct tax rate on enterprises
thcb(h,c)           Household specific commodity tax (for food aid)
*-- ## absolute changes in base tax rates
dabte(c,w)          Change in base export taxes on commy imported from region w
dabtm(w,c)          Change in base tariff rates on commy imported from region w
dabts(c)            Change in base sales tax rate
dabthc(h,c)         Change in HH specific sales tax
dabtv(cc)           Change in base value added tax rate
dabtx(a)            Change in base indirect tax rate
dabtxa(a)           Change in base indirect tax rate
dabtf(ff,a)         Change in base factor us tax rate on activities
dabtyf(f)           Change in base direct tax rate on factors
dabtyh(h)           Change in base direct tax rate on households
dabtye(e)           Change in base direct tax rate on enterprises
dabthc(h,c)         HH specific comm tax (for food aid)
*-- ## partial changes in tax rates
te01(c,w)           0-1 par for potential flexing of export taxes on comm.ies
tm01(w,c)           0-1 par for potential flexing of Tariff rates on comm.ies
ts01(c)             0-1 par for potential flexing of sales tax rates  (for food aid)
thc01(h,c)          0-1 par for potential flexing of HH specific sales tax
tv01(cc)            0-1 par for potential flexing of value added tax rates
tx01(a)             0-1 par for potential flexing of indirect tax rates
tf01(ff,a)          0-1 par for potential flexing of factor use tax rates
tyf01(f)            0-1 par for potential flexing of direct tax rates on factors
tyh01(h)            0-1 par for potential flexing of direct tax rates on h.holds
tye01(e)            0-1 par for potential flexing of direct tax rates on e.rises
vtax01              0-1 par for potential flexing of value added tax rates
dmd_PP(c)           Domestic absorption at purchasing prices
dmd_BP(c)           Domestic absorption at basic prices



*-- ## Initial values for scaling variables
QGDADJ0             Government consumption demand scaling factor
EGADJ0              Transfers to enterprises by government Scaling Factor
HGADJ0              Scaling factor for government transfers to households
HOGOV0(h)           Government transfers to HHs
hogovb(h)           Initial government transfer to the households
dabhogov(h)         additive change for all HHs in government transfer to the households
DHOGOV0             additive change adjuster for selected HHs in government transfer to the households
hogov01(h)          HH selector for  additive change for selected HHs

*-- ## Initial values for variables
YG0                 Government income
YGADJ0              Government income adjuster
QGD0(c)             Government consumption demand
EG0                 Expenditure by government
VGD0                Value of Government consumption expenditure
GBUDG0              Government budget for current spendings and investments

*-- ## Transfer Expenditures
hurbgovconst(h)     Transfers to urban hhold h from government (nominal but scalable)
hrurgovconst(h)     Transfers to rural hhold h from government (nominal but scalable)
entgovconst(e)      Government transfers to enterprise e

*-- ## Consumption Expenditures
qgdconst(c)         Government demand volume

*-- ## Initial values for scaling variables
SADJ0               Savings rate scaling factor for BOTH households and enterprises
SHADJ0              Savings rate scaling factor for households
SEADJ0              Savings rate scaling factor for enterprises
IADJ0               Investment scaling factor
IADJTy0(i)          Investment scaling factor for investment type i
DSHH0               Partial household savings rate scaling factor
DS0                 Partial household and enterprise savings rate scaling factor
DSEN0               Partial enterprise savings rate scaling factor

*-- ## Initial values for variables
QINVD0(c,i)         Investment consumption by commodity c for investment of type i
QINV0(i)            Investment volume by investment type i
INVSH_I0(i)         Shares of savings to investment of type i
INVEST0             Total investment expenditure
TOTSAV0             Total savings

*-- ## base and initial savings rates
shh0(h)             Initial Household saving rates
shhb(h)             Base Household saving rates
sen0(e)             Initial Enterprise saving rates
senb(e)             Base Enterprise saving rates

*-- ## absolute changes in base savings rates
dabshh(h)           Change in base Household saving rates
dabsen(e)           Change in base Enterprise saving rates

*-- ## partial changes in savings rates
shh01(h)            0-1 par for potential flexing of Household saving rates
sen01(e)            0-1 par for potential flexing of Enterprise saving rates

*-- ## Consumption Expenditures
invconst(c,i)       Investment demand volume for investment of type i
ioqinvd(c,i)        Input of commodity c per unit of investment of type i
ioqinvdCHK(i)       Check on Input of commodity c per unit of investment of type i
qinvb(i)            Investment volume by investment type i in base
SAVCHK              CHECK on equality of Savings and Investmemts in data

*-- ## Initial values for variables
YFWOR0(w,f)         Foreign factor income

*-- ## Savings Expenditures

*-- ## Transfer Expenditures
factwor(f,w)        Factor payments from RoW (constant in foreign currency)
entwor(e,w)         Transfers to enterprise e from world (constant in foreign currency)
govwor(w)           Transfers to government from world (constant in foreign currency)
HOWOR0(h,w)         Transfers to household from world (constant in foreign currency)

*-- ## Initial values for variables

*-- # Account Closure
KAPGOV0             Government Savings
KAPREG0(w)          Current account balance
KAPWOR0             Current account balance

*-- # Absorption Closure
VFDOMD0             Value of final domestic demand
INVESTSH0           Value share of investment in total final domestic demand
VGDSH0              Value share of Govt consumption in total final domestic demand
VEDSH0(e)           Value share of Ent consumption in total final domestic demand


*-------------------------------------------------------------------------------
*-$EMISSIONS COefficients
*-------------------------------------------------------------------------------
coefco2Q(c,a)          CO2 emission coeeficients per unit of quantity of energy input used by activities
coefco2H(c,h)          CO2 emission coeeficients per unit of quantity of energy input used by households
coefnco2Q(NCO,a)       Output-based non-combustive emission coeeficients
coefnco2H(NCO,c,h)     Household based non-combustive emission coefficients
coefnco2IO(NCO,c,a)    Process non-combustive emission coefficients based on intermediate demand
coefnco2FS(NCO,c,a)    NCO2 emission coefficients based on fossil fuel combustion in production
coefnco2EN(NCO,f,a)    Endowment based non-combustive emission coefficients

*-Initial emission levels

 CO2EM_Q0(c,a)
 CO2EM_H0(c,h)
 CO2EMIS_Q0(a)
 CO2EMIS_H0(h)
 CO2EMIS0
 NCO2EM_Q0(nco,a)
 NCO2EM_FS0(nco,c,a)
 NCO2EM_IO0(nco,c,a)
 NCO2EM_EN0(nco,f,a)
 NCO2EM_H0(nco,c,h)
 NCO2EM_FS_SUM0(nco,a)
 NCO2EM_IO_SUM0(nco,a)
 NCO2EM_EN_SUM0(nco,a)
 NCO2EM_H_SUM0(nco,h)
 NCO2EM_A_SUM0(nco,a)
 NCO2EM_SUM0(nco)
 GHGEM0

*-- ##### GDP
GDP0                GDP from Value Added

*-- # Slack
WALRAS0             Slack variable for Walras Law


*----------Parameters for Calibration Check
*-------- TRADE BLOCK ----------------------------------------------------

 QQ0chk(c)          check on QQ0
 QQ0chkcount        Count on QQ0chk
 QXC0chk(c)         check on QXC0
 QXC0chkcount       Count on QXC0chk

 QE0neg(c)          Negative Values for QE0
 QD0neg(c)          Negative Values for QD0
 QM0neg(c)          Negative Values for QM0

 QE0negcount        Negatives count for QD0
 QD0negcount        Negatives count for QD0
 QM0negcount        Negatives count for QD0

*-------- NUMERAIRE PRICE BLOCK ------------------------------------------

 comtotshCHK        check on CPI weights
 vddtotshCHK        check on PPI weights
 QXACchk(a,c)       Check for COMOUT
 QXchk(a)           check on QX aggregation
 deltaxcCHK(c)      check on deltaxc

*-------- HOUSEHOLD BLOCK ------------------------------------------------

 FRISCHchk(h)       Check for non negative FRISCH parameters
 FRISCHcount        Count of non negative FRISCH parameters

 hexpschk(h)        Check on subsistence expenditure
 hexpschkcount      Count on hholdsheck with NO subsistence expenditure

 hohototalCHK(h)    interhousehold transfer totals income
 hohototal2CHK(h)   interhousehold transfer totals expenditure

 AgBuRecurr0(c)     Recurrent budget
 AgBuInvest0(i)     Investment budget
 AgBuInpSub0(ff,a)  Input subsidy budget
 AgBuRevFund0(ff,a) Revolving fund budget
 AgBuOutSub0(a)     Output subsidy budget
 AgBuComSub0(cc,h)  Commodity subsidies (i.e. food aid)
 AgBuIncSub0(h)     Income subsidies & transfers
 AgBuTotRecurr0     Total Recurrent budget
 AgBuTotInvest0     Total Investment budget
 AgBuTotInpSub0     Total Input subsidy budget
 AgBuTotOutSub0     Total Output subsidy budget
 AgBuTOTALx0        Total Agricultural budget
 AgBuTOTShr0        Total Agricultural budget
 AgBuTotComSub0     Total Commodity subsudies
 AgBuTotIncSub0     Total Income subsidies & transfers

*--------------DYNAMIC VARIABLES

mu_ext(ff,a)        Elasticity of productivity to the spendings on extension services
EXTENS0(ff,a)       Spending on extension services
EXTENSSHR0(ff,a)    Share of each factor in extension spending
ADFExt0(ff,a)       Productivity change due to extension services
POPN0(h)            Population
;
