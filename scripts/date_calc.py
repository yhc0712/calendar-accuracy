#!/usr/bin/env python3
"""
Date and Calendar Calculation Utility

Provides accurate date calculations for:
- Day of week for any date
- Days between dates
- Date arithmetic (add/subtract days, weeks, months, years)
- Week numbers and quarter information
- Relative date descriptions
- Holiday awareness (100+ countries via holidays library)
- Leap year handling

Usage:
    python date_calc.py info 2025-01-29
    python date_calc.py add 2025-01-29 30 days
    python date_calc.py diff 2025-01-01 2025-12-31
    python date_calc.py range 2025-01-01 2025-01-07
    python date_calc.py relative today
    python date_calc.py holidays              # Current year, default country (TW)
    python date_calc.py holidays 2025         # Specific year
    python date_calc.py holidays --country US # Different country
    python date_calc.py holidays 2025 --country JP
"""

import argparse
import sys
from datetime import datetime, timedelta, date
from typing import Optional, Tuple, List
import calendar

try:
    import holidays as holidays_lib
    HOLIDAYS_AVAILABLE = True
except ImportError:
    HOLIDAYS_AVAILABLE = False

# Default country for holidays (can be overridden with --country)
DEFAULT_COUNTRY = "TW"


def parse_date(date_str: str) -> date:
    """Parse a date string in various formats."""
    date_str = date_str.lower().strip()
    
    today = date.today()
    
    # Handle relative dates
    if date_str == "today":
        return today
    elif date_str == "yesterday":
        return today - timedelta(days=1)
    elif date_str == "tomorrow":
        return today + timedelta(days=1)
    
    # Try various date formats
    formats = [
        "%Y-%m-%d",      # 2025-01-29
        "%m/%d/%Y",      # 01/29/2025
        "%d/%m/%Y",      # 29/01/2025
        "%B %d, %Y",     # January 29, 2025
        "%b %d, %Y",     # Jan 29, 2025
        "%Y%m%d",        # 20250129
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse date: {date_str}")


def get_holidays(year: int, country: str = DEFAULT_COUNTRY) -> List[Tuple[date, str]]:
    """Get all holidays for a year and country using the holidays library."""
    if not HOLIDAYS_AVAILABLE:
        return []
    
    try:
        country_holidays = holidays_lib.country_holidays(country, years=year)
        return sorted([(d, name) for d, name in country_holidays.items()])
    except NotImplementedError:
        print(f"Warning: Country '{country}' not supported", file=sys.stderr)
        return []


def is_holiday(d: date, country: str = DEFAULT_COUNTRY) -> Optional[str]:
    """Check if a date is a holiday in the specified country."""
    if not HOLIDAYS_AVAILABLE:
        return None
    
    try:
        country_holidays = holidays_lib.country_holidays(country, years=d.year)
        return country_holidays.get(d)
    except NotImplementedError:
        return None


def list_supported_countries() -> List[str]:
    """List all supported country codes."""
    if not HOLIDAYS_AVAILABLE:
        return []
    return sorted(holidays_lib.list_supported_countries().keys())


def is_leap_year(year: int) -> bool:
    """Check if a year is a leap year."""
    return calendar.isleap(year)


def days_in_month(year: int, month: int) -> int:
    """Get the number of days in a month."""
    return calendar.monthrange(year, month)[1]


def get_quarter(d: date) -> int:
    """Get the quarter (1-4) for a date."""
    return (d.month - 1) // 3 + 1


def get_week_number(d: date) -> Tuple[int, int]:
    """Get ISO week number and year."""
    iso_cal = d.isocalendar()
    return iso_cal[0], iso_cal[1]


def date_info(d: date, country: str = DEFAULT_COUNTRY) -> dict:
    """Get comprehensive information about a date."""
    week_year, week_num = get_week_number(d)
    
    info = {
        "date": d.isoformat(),
        "formatted": d.strftime("%A, %B %d, %Y"),
        "day_of_week": d.strftime("%A"),
        "day_of_week_num": d.weekday(),  # 0=Monday, 6=Sunday
        "day_of_month": d.day,
        "month": d.strftime("%B"),
        "month_num": d.month,
        "year": d.year,
        "quarter": get_quarter(d),
        "week_number": week_num,
        "week_year": week_year,
        "day_of_year": d.timetuple().tm_yday,
        "days_in_month": days_in_month(d.year, d.month),
        "is_leap_year": is_leap_year(d.year),
        "is_weekend": d.weekday() >= 5,
        "holiday": is_holiday(d, country),
    }
    
    # Days from today
    today = date.today()
    delta = (d - today).days
    if delta == 0:
        info["relative"] = "today"
    elif delta == 1:
        info["relative"] = "tomorrow"
    elif delta == -1:
        info["relative"] = "yesterday"
    elif delta > 0:
        info["relative"] = f"in {delta} days"
    else:
        info["relative"] = f"{-delta} days ago"
    
    return info


def add_to_date(d: date, amount: int, unit: str) -> date:
    """Add time to a date."""
    unit = unit.lower().rstrip('s')  # Normalize: days -> day
    
    if unit == "day":
        return d + timedelta(days=amount)
    elif unit == "week":
        return d + timedelta(weeks=amount)
    elif unit == "month":
        new_month = d.month + amount
        new_year = d.year + (new_month - 1) // 12
        new_month = ((new_month - 1) % 12) + 1
        # Handle day overflow (e.g., Jan 31 + 1 month)
        new_day = min(d.day, days_in_month(new_year, new_month))
        return date(new_year, new_month, new_day)
    elif unit == "year":
        new_year = d.year + amount
        # Handle Feb 29 in non-leap years
        new_day = min(d.day, days_in_month(new_year, d.month))
        return date(new_year, d.month, new_day)
    else:
        raise ValueError(f"Unknown unit: {unit}. Use day, week, month, or year.")


def date_diff(d1: date, d2: date) -> dict:
    """Calculate the difference between two dates."""
    if d1 > d2:
        d1, d2 = d2, d1
        swapped = True
    else:
        swapped = False
    
    delta = d2 - d1
    
    # Calculate years, months, days
    years = d2.year - d1.year
    months = d2.month - d1.month
    days = d2.day - d1.day
    
    if days < 0:
        months -= 1
        days += days_in_month(d2.year, d2.month - 1 if d2.month > 1 else 12)
    
    if months < 0:
        years -= 1
        months += 12
    
    # Calculate weeks
    weeks = delta.days // 7
    remaining_days = delta.days % 7
    
    return {
        "total_days": delta.days * (-1 if swapped else 1),
        "total_weeks": round(delta.days / 7, 2),
        "weeks_and_days": f"{weeks} weeks, {remaining_days} days",
        "years_months_days": f"{years} years, {months} months, {days} days",
        "calendar_months": years * 12 + months,
        "from": d1.isoformat(),
        "to": d2.isoformat(),
    }


def date_range(start: date, end: date) -> List[dict]:
    """Get information for each date in a range."""
    if start > end:
        start, end = end, start
    
    dates = []
    current = start
    while current <= end:
        info = date_info(current)
        dates.append({
            "date": info["date"],
            "day": info["day_of_week"][:3],
            "holiday": info["holiday"],
            "weekend": info["is_weekend"],
        })
        current += timedelta(days=1)
    
    return dates


def format_output(data, verbose: bool = False) -> str:
    """Format output for display."""
    if isinstance(data, dict):
        lines = []
        for key, value in data.items():
            if value is not None and value != "":
                lines.append(f"  {key}: {value}")
        return "\n".join(lines)
    elif isinstance(data, list):
        lines = []
        for item in data:
            if isinstance(item, dict):
                parts = [f"{item.get('date', '')}"]
                if item.get('day'):
                    parts.append(f"({item['day']})")
                if item.get('holiday'):
                    parts.append(f"[{item['holiday']}]")
                if item.get('weekend'):
                    parts.append("[weekend]")
                lines.append(" ".join(parts))
            else:
                lines.append(str(item))
        return "\n".join(lines)
    return str(data)


def main():
    parser = argparse.ArgumentParser(description="Date and calendar calculations")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Get date information")
    info_parser.add_argument("date", help="Date (YYYY-MM-DD, today, tomorrow, etc.)")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add time to a date")
    add_parser.add_argument("date", help="Start date")
    add_parser.add_argument("amount", type=int, help="Amount to add (negative to subtract)")
    add_parser.add_argument("unit", choices=["days", "weeks", "months", "years"], help="Unit")
    
    # Diff command
    diff_parser = subparsers.add_parser("diff", help="Difference between two dates")
    diff_parser.add_argument("date1", help="First date")
    diff_parser.add_argument("date2", help="Second date")
    
    # Range command
    range_parser = subparsers.add_parser("range", help="List dates in a range")
    range_parser.add_argument("start", help="Start date")
    range_parser.add_argument("end", help="End date")
    
    # Relative command
    rel_parser = subparsers.add_parser("relative", help="Get relative date info")
    rel_parser.add_argument("date", help="Date to describe")
    
    # Holidays command
    hol_parser = subparsers.add_parser("holidays", help="List holidays for a year")
    hol_parser.add_argument("year", type=int, nargs="?", default=None, help="Year (defaults to current year)")
    hol_parser.add_argument("--country", "-c", default=DEFAULT_COUNTRY, help=f"Country code (default: {DEFAULT_COUNTRY}). Use 'list' to see all supported countries.")
    
    # Weekday command
    wd_parser = subparsers.add_parser("weekday", help="Get day of week for a date")
    wd_parser.add_argument("date", help="Date")
    
    args = parser.parse_args()
    
    try:
        if args.command == "info":
            d = parse_date(args.date)
            print(f"\n📅 Date Information for {d.strftime('%B %d, %Y')}")
            print("-" * 40)
            print(format_output(date_info(d)))
            
        elif args.command == "add":
            d = parse_date(args.date)
            result = add_to_date(d, args.amount, args.unit)
            info = date_info(result)
            print(f"\n📅 {d} + {args.amount} {args.unit} = {result}")
            print(f"   → {info['formatted']}")
            
        elif args.command == "diff":
            d1 = parse_date(args.date1)
            d2 = parse_date(args.date2)
            diff = date_diff(d1, d2)
            print(f"\n📅 Difference: {d1} → {d2}")
            print("-" * 40)
            print(format_output(diff))
            
        elif args.command == "range":
            start = parse_date(args.start)
            end = parse_date(args.end)
            dates = date_range(start, end)
            print(f"\n📅 Date Range: {start} to {end}")
            print("-" * 40)
            print(format_output(dates))
            
        elif args.command == "relative":
            d = parse_date(args.date)
            info = date_info(d)
            print(f"\n📅 {info['formatted']} is {info['relative']}")
            
        elif args.command == "holidays":
            if args.country.lower() == "list":
                countries = list_supported_countries()
                print(f"\n📅 Supported Countries ({len(countries)} total)")
                print("-" * 40)
                # Print in columns
                for i in range(0, len(countries), 8):
                    print("  " + "  ".join(countries[i:i+8]))
            else:
                if not HOLIDAYS_AVAILABLE:
                    print("Error: 'holidays' library not installed.", file=sys.stderr)
                    print("Install with: pip install holidays", file=sys.stderr)
                    sys.exit(1)
                year = args.year if args.year else date.today().year
                holidays = get_holidays(year, args.country)
                print(f"\n📅 Holidays in {args.country} for {year}")
                print("-" * 40)
                if holidays:
                    for hdate, name in holidays:
                        day = hdate.strftime("%A")
                        print(f"  {hdate} ({day[:3]}): {name}")
                else:
                    print(f"  No holidays found for country code '{args.country}'")
                    print(f"  Use 'holidays --country list' to see supported countries")
                
        elif args.command == "weekday":
            d = parse_date(args.date)
            info = date_info(d)
            print(f"\n📅 {d} is a {info['day_of_week']}")
            
        else:
            parser.print_help()
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
