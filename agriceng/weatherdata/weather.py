import requests
from requests.exceptions import HTTPError
# import urllib.request
# import json
from datetime import date, timedelta


def query_nairobi_weather():

    # This is the core visual crossing weather query URL
    BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/'

    ApiKey = 'K3YVFFUCWT3SRNJKWJT9V3S47'

    # UnitGroup sets the units of the output - us or metric
    UnitGroup = 'metric'

    # Locations for the weather data. Multiple locations separated by pipe (|)
    Locations = 'Nairobi,KE'

    # FORECAST or HISTORY
    QueryType = 'HISTORY'

    # 1=hourly, 24=daily
    AggregateHours = '24'

    # Params for history only
    this_week = date.today()
    last_week = this_week - timedelta(days=6)
    StartDate = str(last_week)
    EndDate = str(this_week)

    # Set up the specific parameters based on the type of query
    if QueryType == 'FORECAST':
        print(' - Fetching forecast data')
        QueryParams = 'forecast?aggregateHours=' + AggregateHours + '&unitGroup=' + UnitGroup + '&shortColumnNames=true'
    else:
        print(' - Fetching history for the last 1 week')

        # History requests require a date.  We use the same date for start and end since we only want to query a single date in this example
        QueryParams = 'history?aggregateHours=' + AggregateHours + '&unitGroup=' + UnitGroup + '&startDateTime=' + StartDate + 'T00%3A00%3A00&endDateTime=' + EndDate + 'T00%3A00%3A00'

    Locations = '&locations=' + Locations

    ApiKey = '&key=' + ApiKey

    # Build the entire query
    url = BaseURL + QueryParams + Locations + ApiKey + "&contentType=json"

    print(' - Running query URL: ', url)
    print()

    try:
        response = requests.get(url)
        # A successful request will raise no error
        response.raise_for_status()
    except HTTPError as http_err:
        response = "HTTP error occurred: {}"
        return response.format(http_err)
    except Exception as err:
        response = "An error occurred: {}"
        return response.format(err)
    else:
        return response.json()




# def query_location_weather(location):
#     locations = '&locations=' + location
#     # Build the entire query
#     url = BaseURL + QueryParams + Locations + ApiKey+"&contentType=json"
#     print(' - Running query URL: ', url)
#     print()
#     response = requests.get(url)
#         # A successful response will raise no error
#         response.raise_for_status()
#     except HTTPError as http_err:
#         print(f'HTTP error occurred: {http_err}')
#     except Exception as err:
#         print(f'Other error occurred: {err}')
#     else:
#         response = response.json()
