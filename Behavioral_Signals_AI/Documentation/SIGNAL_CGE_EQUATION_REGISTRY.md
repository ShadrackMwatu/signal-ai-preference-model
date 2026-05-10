# Signal CGE Equation Registry

The full-CGE equation registry organizes the model into transparent blocks:

- production
- intermediate demand
- value added
- household demand
- government demand
- investment demand
- imports
- exports
- Armington aggregation
- CET transformation
- factor markets
- commodity markets
- price equations
- income-expenditure balance
- savings-investment balance
- government balance
- external balance
- numeraire condition

Each block currently stores its economic role and placeholder equation. The next implementation step is to convert each placeholder into residual functions that can be passed to a numerical solver.
