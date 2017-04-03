"""This modules reads sunup and sun down from a webservice if possible."""

import re
import json
import datetime as dt
import requests as http


def sun_setts():
    """Returns sunset and sunup"""
    from_regex = \
     "Sunrise Today: </span><span class=three>([0-2][0-9]:[0-6][0-9])</span>"
    to_regex = \
     "Sunset Today: </span><span class=three>([0-2][0-9]:[0-6][0-9])</span>"

    response = http.get("https://www.timeanddate.com/astronomy/sweden/stockholm")
    if not response.ok:
        print("Failed to read sunset/sunup")
        return

    from_time = re.search(from_regex, response.text)
    to_time = re.search(to_regex, response.text)
    print("Solen går upp {}".format(from_time.group(1)))
    print("Solen går ner {}".format(to_time.group(1)))

#sun_setts()

def sun_rise_sets():
    """Fetches sun rise and sunset time from free api."""
    url = "http://api.sunrise-sunset.org/json?lat=60.5869432&lng=15.6841269&date=today"

    response = http.get(url)
    if not response.ok:
        print("Failed to read sunset/sunup from API.")

    data = json.loads(response.text)
    soluppgang_utc = data['results']['sunrise']
    solnedgang_utc = data['results']['sunset']

    cdt = dt.datetime.combine(dt.datetime.now().date(), dt.datetime.strptime(soluppgang_utc, '%I:%M:%S %p').time())
    soluppgang = cdt.replace(tzinfo=dt.timezone.utc).replace(tzinfo=None)
    solnedgang = dt.datetime.strptime(solnedgang_utc, '%I:%M:%S %p').time()
    print("Solen går upp {} solen går ner {}".format(soluppgang, solnedgang))


sun_rise_sets()
#sun_setts()
current_time = dt.datetime.now()

print("Nu är klockan {}".format(current_time.time()))