from datetime import date, timedelta

from django.conf import settings


def get_weather_url(location):

    # This is the core visual crossing weather query URL
    BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/'

    ApiKey = settings.WEATHER_DATA_API_KEY

    # UnitGroup sets the units of the output - us or metric
    UnitGroup = 'us'

    # Locations for the weather data. Multiple locations separated by pipe (|)
    Locations = location

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

    return url
