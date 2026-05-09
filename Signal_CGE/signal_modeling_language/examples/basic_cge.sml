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

CLOSURE:
  government_savings = endogenous
  exchange_rate = fixed
  numeraire = consumer_price_index

SHOCKS:
  increase_vat = tax_rate + 0.02
  productivity_growth = productivity[agriculture] + 0.05

SOLVE:
  model = kenya_cge
  backend = gams
  solver = path

OUTPUT:
  gdx = "outputs/results.gdx"
  excel = "outputs/results.xlsx"
  report = "outputs/policy_report.md"
  gams = "outputs/kenya_cge.gms"
