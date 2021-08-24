import urllib.request
import json
from datetime import date, timedelta

from django.conf import settings

# This is the core visual crossing weather query URL
BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/'

ApiKey = 'K3YVFFUCWT3SRNJKWJT9V3S47'


#UnitGroup sets the units of the output - us or metric
UnitGroup = 'metric'

#Locations for the weather data. Multiple locations separated by pipe (|)
Locations='tropez'

#FORECAST or HISTORY
QueryType='HISTORY'

#1=hourly, 24=daily
AggregateHours='24'

#Params for history only
this_week = date.today()
last_week = this_week - timedelta(days=0)
StartDate = str(last_week)
EndDate = str(this_week)

# Set up the specific parameters based on the type of query
if QueryType == 'FORECAST':
    print(' - Fetching forecast data')
    QueryParams = 'forecast?aggregateHours=' + AggregateHours + '&unitGroup=' + UnitGroup + '&shortColumnNames=true'
else:
    print(' - Fetching history for the last 1 week')

    # History requests require a date.  We use the same date for start and end since we only want to query a single date in this example
    QueryParams = 'history?aggregateHours=' + AggregateHours + '&unitGroup=' + UnitGroup +'&startDateTime=' + StartDate + 'T00%3A00%3A00&endDateTime=' + EndDate + 'T00%3A00%3A00'

Locations='&locations='+Locations

ApiKey='&key='+ApiKey

# Build the entire query
URL = BaseURL + QueryParams + Locations + ApiKey+"&contentType=json"

print(' - Running query URL: ', URL)
print()


response = urllib.request.urlopen(URL)
data = response.read()
weatherData = json.loads(data.decode('utf-8'))
print(weatherData)

for measurement, metrics in weatherData['columns'].items():
    print("{}: {}".format(metrics['name'], metrics['unit']))
    print("++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
for location, details in weatherData['locations'].items():
    print("{}. Coordinates: {}, {}. Timezone: {}.".format(
        details['address'], details['latitude'], details['longitude'], details['tz']
        ,))
    for detail in details['values']:
        print(detail)
    print('-------------------------------------------------')
    print()

errorCode=weatherData["errorCode"] if 'errorCode' in weatherData else 0

if (errorCode>0):
    print("An error occurred retrieving the data:"+weatherData["message"])

print(response)
