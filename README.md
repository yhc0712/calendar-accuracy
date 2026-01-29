# calendar-accuracy

A Claude skill that ensures accurate calendar and date calculations. Prevents common LLM errors with days of week, date arithmetic, leap years, and relative date expressions.

## Installation

### Claude Code
```bash
/plugin install calendar-accuracy@yhc0712/calendar-accuracy
```

### Manual
Copy the `calendar-accuracy` folder to your skills directory.

### Dependencies
```bash
pip install holidays
```

## Features

- **Day of week** — Accurate lookup for any date
- **Date arithmetic** — Add/subtract days, weeks, months, years
- **Date difference** — Days between two dates
- **Holidays** — 100+ countries supported (defaults to Taiwan)
- **Leap year handling** — Correctly handles Feb 29 edge cases

## Usage

```bash
# Date information
python scripts/date_calc.py info 2025-01-29

# Add/subtract time
python scripts/date_calc.py add today 30 days
python scripts/date_calc.py add 2025-01-31 1 months

# Days between dates
python scripts/date_calc.py diff 2025-01-01 2025-12-31

# Holidays (defaults to current year + Taiwan)
python scripts/date_calc.py holidays
python scripts/date_calc.py holidays 2025 --country US
python scripts/date_calc.py holidays --country JP
python scripts/date_calc.py holidays --country list

# Day of week
python scripts/date_calc.py weekday "March 15, 2025"
```

## Supported Countries

The script uses the [holidays](https://github.com/vacanza/holidays) library, supporting 100+ countries including:

`TW` `US` `JP` `KR` `CN` `HK` `SG` `GB` `DE` `FR` `CA` `AU` and many more.

Run `python scripts/date_calc.py holidays --country list` for the full list.

## License

MIT
