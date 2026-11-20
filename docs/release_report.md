# Release Report: 1.1.0-rc1

Date: 2026-11-20

## Recommendation

Do not release 1.1.0-rc1. Keep 1.0.0 in the field until the bugs below are fixed and
the full suite passes on a new release candidate.

## Results

| Version | Tests | Passed | Failed |
|---------|-------|--------|--------|
| 1.0.0 | 35 | 35 | 0 |
| 1.1.0-rc1 | 35 | 31 | 4 |

## Open bugs

| Bug | Requirement | Severity | Summary |
|-----|-------------|----------|---------|
| BUG-001 | REQ-03 | Medium | `SET 30.0` rejected with `ERR RANGE` |
| BUG-002 | REQ-07 | High | No overheat alarm at exactly 35.0 C |
| BUG-003 | REQ-07 | High | `RESET` clears the alarm below 32.0 C instead of 30.0 C |

## Reasons

- Two of the three bugs are in the overheat protection, which is a safety function.
  Together they allow the heater to run at the overheat limit and to be re-enabled
  while the device is still too hot.
- BUG-001 is a regression: a setting that works in 1.0.0 is rejected.
- The pass criterion in the test plan (100 % pass) is not met.

## Next steps

Fix the three bugs, add the fixed version to the simulator, and re-run the full suite.
