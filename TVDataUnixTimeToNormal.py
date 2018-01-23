from datetime import datetime
from pytz import timezone
import pytz
import time

def convert_to_specified_time_zone(value,tz):
    date_format = '%m/%d/%Y %H:%M:%S %Z'
    date = datetime.fromtimestamp(int(value))


    req_timezone = timezone(tz)
    date = req_timezone.localize(date)
    date = date.astimezone(req_timezone)

    return date.strftime(date_format)

def get_current_time():

    return int(time.time())