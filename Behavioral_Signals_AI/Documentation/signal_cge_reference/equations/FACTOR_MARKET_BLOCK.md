# Factor Market Block

The factor market block allocates labor, capital, and other factors across activities.

Placeholder structure:

```text
factor_demand(f,a) = calibrated_factor_share(f,a) * activity_output(a)
factor_market_residual(f) = factor_supply(f) - sum_a factor_demand(f,a)
```

Factor-market closure determines whether wages, employment, or factor supplies adjust.
