---
name: calendar-accuracy
description: Ensure accurate calendar and date calculations in responses. Use for ANY query involving dates, days of week, date arithmetic, scheduling, holidays, time periods, countdowns, or relative date expressions. Triggers on questions like "what day is [date]", "how many days until", "when is [event]", "X days/weeks/months from [date]", calendar planning, and scheduling tasks.
license: MIT
---

# Calendar Accuracy

Verify all date-related claims before including them in responses. Never guess dates or days of week—calendar calculations are error-prone for LLMs.

## Examples

- "What day of the week is January 29, 2025?" → Run `python scripts/date_calc.py weekday 2025-01-29`
- "What's the date 30 days from now?" → Run `python scripts/date_calc.py add today 30 days`
- "How many days until Christmas?" → Run `python scripts/date_calc.py diff today 2025-12-25`
- "When are the holidays this year?" → Run `python scripts/date_calc.py holidays`
- "What are US holidays in 2025?" → Run `python scripts/date_calc.py holidays 2025 --country US`
- "List the dates for next week" → Run `python scripts/date_calc.py range 2025-02-03 2025-02-09`

## Guidelines

- Always verify date claims using `scripts/date_calc.py` before responding
- State full dates with day of week: "Wednesday, January 29, 2025"
- For countdowns, show both the count and the target date
- Acknowledge ambiguity in relative expressions ("next Friday" can mean different things)
- Double-check edge cases: leap years, month-end arithmetic, week numbers

## Script Usage

```bash
# Full date information
python scripts/date_calc.py info 2025-01-29

# Add/subtract time
python scripts/date_calc.py add 2025-01-29 30 days
python scripts/date_calc.py add 2025-01-29 -2 weeks
python scripts/date_calc.py add 2025-01-29 3 months

# Difference between dates
python scripts/date_calc.py diff 2025-01-01 2025-12-31

# Date range listing
python scripts/date_calc.py range 2025-01-01 2025-01-07

# Holidays (defaults to current year, TW)
python scripts/date_calc.py holidays
python scripts/date_calc.py holidays 2025
python scripts/date_calc.py holidays --country US
python scripts/date_calc.py holidays 2025 --country JP
python scripts/date_calc.py holidays --country list  # Show all supported countries

# Day of week only
python scripts/date_calc.py weekday "March 15, 2025"
```

## Common Errors to Avoid

- **Month arithmetic overflow**: Jan 31 + 1 month → Feb 28/29, not Feb 31
- **Leap year assumptions**: Always verify if Feb 29 exists in the year
- **Week number confusion**: ISO weeks don't align with calendar months
- **Day-of-week guessing**: Never estimate—always calculate

## Quick Reference

- Days in months: Jan=31, Feb=28/29, Mar=31, Apr=30, May=31, Jun=30, Jul=31, Aug=31, Sep=30, Oct=31, Nov=30, Dec=31
- 2025 Doomsday: Friday (4/4, 6/6, 8/8, 10/10, 12/12 are all Fridays)
- See `references/calendar_rules.md` for leap year rules, holiday calculations, and verification methods
