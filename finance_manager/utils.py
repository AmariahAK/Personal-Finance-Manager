from datetime import datetime, timedelta

def parse_date(date_str):
    """
    Parse a date string in the format YYYY-MM-DD and return a datetime.date object.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")

def format_date(date_obj):
    """
    Format a datetime.date object to a string in the format YYYY-MM-DD.
    """
    return date_obj.strftime("%Y-%m-%d")

def get_end_of_month(year, month):
    """
    Return the last day of the month for a given year and month.
    """
    if month == 12:
        return datetime(year, 12, 31).date()
    else:
        return (datetime(year, month + 1, 1) - timedelta(days=1)).date()

def get_frequency_timedelta(frequency):
    """
    Return a timedelta object corresponding to the frequency string.
    """
    if frequency == 'daily':
        return timedelta(days=1)
    elif frequency == 'weekly':
        return timedelta(weeks=1)
    elif frequency == 'monthly':
        return timedelta(days=30)  # Approximation
    elif frequency == 'yearly':
        return timedelta(days=365)
    else:
        raise ValueError("Unknown frequency, should be 'daily', 'weekly', 'monthly', or 'yearly'")

def generate_recurring_dates(start_date, frequency, end_date=None):
    """
    Generate dates for recurring transactions from start_date with given frequency until end_date.
    """
    dates = []
    current_date = start_date
    while not end_date or current_date <= end_date:
        dates.append(current_date)
        current_date += get_frequency_timedelta(frequency)
    return dates
