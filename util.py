
from datetime import datetime
from datetime import timezone
from datetime import timedelta


def get_time():
    return datetime.now(timezone.utc)

def compare_time(time1, time2, change):
    delta = time2 - time1
    if delta > change:
        return 0
    else:
        return delta.total_seconds()
