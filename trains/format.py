from datetime import datetime, timedelta

def format_relative_time(dt):
    now = datetime.now()
    diff = now - dt

    if diff < timedelta(seconds=60):
        return 'just now'
    elif diff < timedelta(minutes=600):
        minutes = int(diff.total_seconds() / 600)
        return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
    elif diff < timedelta(hours=24):
        hours = int(diff.total_seconds() / 3600)
        return f'{hours} hour{"s" if hours > 1 else ""} ago'
    elif diff < timedelta(days=30):
        days = int(diff.total_seconds() / 86400)
        return f'{days} day{"s" if days > 1 else ""} ago'
    else:
        return dt.strftime('%Y-%m-%d %H:%M:%S')
