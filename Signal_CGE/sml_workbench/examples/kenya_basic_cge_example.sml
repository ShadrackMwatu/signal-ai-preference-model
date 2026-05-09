SETS:
  sectors = [agriculture, manufacturing, services]
  factors = [labour, capital]
  households = [rural, urban]

PARAMETERS:
  SAM = "Behavioral_Signals_AI/data/sample_sam.csv"
  elasticity_armington = 2.0
  elasticity_cet = 2.0

VARIABLES:
  output[sectors]
  price[sectors]
  consumption[households,sectors]
  imports[sectors]
  exports[sectors]

EQUATIONS:
  market_clearing[sectors]
  household_income[households]
  armington_demand[sectors]
  cet_supply[sectors]
  government_balance
  savings_investment_balance

SHOCKS:
  solar_import_push = imports[services] + 0.03
  productivity_growth = productivity[agriculture] + 0.05

SOLVE:
  model = kenya_basic_cge
  backend = gams
  solver = path
