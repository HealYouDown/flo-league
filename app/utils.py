import datetime


# https://stackoverflow.com/questions/6558535/find-the-date-for-the-first-monday-after-a-given-date
def next_weekday(
    d: datetime.datetime = datetime.datetime.utcnow(),
    weekday: int = 0,
) -> datetime.datetime:
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7

    # Flatten the current time to just the date
    date = datetime.datetime(d.year, d.month, d.day)
    return date + datetime.timedelta(days_ahead)
