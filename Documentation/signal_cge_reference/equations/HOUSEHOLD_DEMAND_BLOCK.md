# Household Demand Block

The household block maps factor income, transfers, taxes, savings, and consumption demand.

Placeholder structure:

```text
household_income(h) = factor_income(h) + transfers(h)
household_consumption(c,h) = expenditure_share(c,h) * disposable_income(h) / consumer_price(c)
```

Calibration uses household expenditure shares and income flows from the SAM. Distributional outputs should report household income, welfare proxies, and gender-care effects where accounts support them.
