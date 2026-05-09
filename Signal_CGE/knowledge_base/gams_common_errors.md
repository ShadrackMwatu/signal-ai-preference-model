# GAMS Common Errors

## Uncontrolled Set Entered As Constant

Evidence requirement:

- source run
- generated equation or GAMS log line
- corrected indexing
- validation status

Typical fix: ensure every indexed symbol appears under a controlling set domain
in the equation definition.

## Infeasible Model

Typical checks:

- closure consistency
- SAM balance
- calibration bounds
- shock magnitude
- variable initialization and scaling
