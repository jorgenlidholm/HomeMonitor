"""This modules reads sunup and sun down from a webservice if possible."""

import re
import json
import time
import datetime as dt

def utc2local(utc):
    """Converts utc datetime to local time"""
    epoch = time.mktime(utc.timetuple())
    offset = dt.datetime.fromtimestamp(epoch) - dt.datetime.utcfromtimestamp(epoch)
    return utc + offset

def get_sunset_for_today():
    """Fetches sun rise and sunset time from free api."""
    import requests
    url = "http://api.sunrise-sunset.org/json?lat=60.5869432&lng=15.6841269&date=today"

    response = requests.get(url)
    if not response.ok:
        print("Failed to read sunset/sunup from API.")

    data = json.loads(response.text)

    # cdt_uppgang = dt.datetime.combine(dt.datetime.now().date(), \
    #  dt.datetime.strptime(data['results']['sunrise'], '%I:%M:%S %p').time())
    cdt_nedgang = dt.datetime.combine(dt.datetime.now().date(), \
     dt.datetime.strptime(data['results']['sunset'], '%I:%M:%S %p').time())
    # soluppgang = utc2local(cdt_uppgang)
    solnedgang = utc2local(cdt_nedgang)
    #print("Solen går upp {} solen går ner {}".format(soluppgang, solnedgang))
    return solnedgang

def test_method():
    """Test method that prints information"""
    sun_set = get_sunset_for_today()
    current_time = dt.datetime.now()

    print("Nu är klockan {}, solen går ner {}".format(current_time, sun_set))

