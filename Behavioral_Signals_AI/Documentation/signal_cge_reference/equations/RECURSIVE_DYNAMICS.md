# Recursive Dynamics

Recursive dynamics update the economy between solution years.

Placeholder structure:

```text
capital_stock(t+1) = (1 - depreciation) * capital_stock(t) + investment(t)
labor_supply(t+1) = labor_supply(t) * (1 + labor_growth_rate)
productivity(t+1) = productivity(t) * (1 + productivity_growth_rate)
```

Future dynamic experiments should record baseline projections, annual shocks, update rules, and year-by-year diagnostics.
