# Calendar Reference Guide

## Quick Verification Methods

### Day of Week - Doomsday Algorithm
For any date, use these anchor dates (all fall on the same day of week, the "Doomsday"):
- 4/4, 6/6, 8/8, 10/10, 12/12
- Last day of February (28 or 29)
- 5/9 and 9/5
- 7/11 and 11/7

2024 Doomsday: Thursday | 2025 Doomsday: Friday | 2026 Doomsday: Saturday | 2027 Doomsday: Sunday

### Month Day Counts
- 31 days: Jan, Mar, May, Jul, Aug, Oct, Dec
- 30 days: Apr, Jun, Sep, Nov
- 28/29 days: Feb (29 in leap years)

### Leap Year Rules
A year is a leap year if:
1. Divisible by 4, AND
2. NOT divisible by 100, UNLESS
3. Also divisible by 400

Examples: 2024 ✓, 2000 ✓, 1900 ✗, 2100 ✗

## Common Calculation Errors

### Month Arithmetic Pitfalls
- Adding 1 month to Jan 31 → Feb 28/29 (not Feb 31)
- Adding 1 month to Jan 30 → Feb 28/29 in non-leap/leap years
- "Next month same date" may not exist

### Week Number Edge Cases
- ISO weeks: Week 1 contains the first Thursday of the year
- Some years have 53 weeks (2020, 2026)
- Dec 31 can be in Week 1 of the next year
- Jan 1 can be in Week 52/53 of the previous year

### Business Day Calculations
Remember:
- Weekends: Saturday (day 5) and Sunday (day 6) where Monday=0
- Holidays vary by country/region
- "Next business day" rules vary by context

## US Federal Holiday Calculations

### Fixed Date Holidays
| Holiday | Date |
|---------|------|
| New Year's Day | January 1 |
| Juneteenth | June 19 |
| Independence Day | July 4 |
| Veterans Day | November 11 |
| Christmas Day | December 25 |

### Floating Holidays
| Holiday | Rule |
|---------|------|
| MLK Day | 3rd Monday of January |
| Presidents' Day | 3rd Monday of February |
| Memorial Day | Last Monday of May |
| Labor Day | 1st Monday of September |
| Columbus Day | 2nd Monday of October |
| Thanksgiving | 4th Thursday of November |

## Time Period Calculations

### Days in Common Periods
- 1 week = 7 days
- 2 weeks = 14 days
- 30 days ≠ 1 month (months vary: 28-31 days)
- 365 days = 1 common year
- 366 days = 1 leap year
- 1 quarter ≈ 91-92 days

### Fiscal Quarters (Calendar Year)
- Q1: Jan 1 - Mar 31 (90/91 days)
- Q2: Apr 1 - Jun 30 (91 days)
- Q3: Jul 1 - Sep 30 (92 days)
- Q4: Oct 1 - Dec 31 (92 days)

## Date Format Reference

### ISO 8601
- Date: YYYY-MM-DD (2025-01-29)
- Week: YYYY-Www (2025-W05)
- Ordinal: YYYY-DDD (2025-029)

### Common Formats by Region
- US: MM/DD/YYYY
- Europe: DD/MM/YYYY
- ISO: YYYY-MM-DD

## Relative Date Language

### Precise Meanings
- "Next [day]": The coming occurrence (even if today is that day, typically means the following week)
- "This [day]": The occurrence in the current week
- "In X days": X * 24 hours from now
- "X days from now": Same as "in X days"
- "A week from [day]": 7 days after that day
- "Fortnight": 14 days

### Ambiguous Terms (Clarify When Used)
- "End of week": Friday? Sunday? Saturday?
- "End of month": Last day? Last business day?
- "Biweekly": Every 2 weeks? Twice a week?
- "Bimonthly": Every 2 months? Twice a month?
