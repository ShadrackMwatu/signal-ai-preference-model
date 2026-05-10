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

SHOCKS:
  increase_vat = tax_rate + 0.02

SOLVE:
  model = signal_template_cge
  backend = gams
  solver = path
