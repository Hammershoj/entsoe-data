# Script to read energy day ahead price values from Entsoe and forward it to Home Assistant and InfluxDB
# Requires token obtained from Entsoe - token is stored in settings.py
#
# Version 0.2  02.01.2022
# by hammershoj


import pandas as pd
from settings import api_key
from entsoe import EntsoePandasClient

e = EntsoePandasClient(api_key=api_key, retry_count=20, retry_delay=30)

start_pd = pd.Timestamp('20220110', tz='Europe/Brussels')
end_pd = pd.Timestamp('20220111', tz='Europe/Brussels')

domains = ["NO_1", "NO_2", "NO_3", "NO_4", "NO_5", "DK_1", "DK_2", "DE_LU", "SE_1", "SE_2", "SE_3", "SE_4"]

def day_ahead_prices(start, end):
    # query day ahead prices for a given country in a given time range
    for bzn in domains:
        s = e.query_day_ahead_prices(bzn, start=start, end=end)
        for index, value in s.iteritems():
             #print("Entsoe ; " + "DayAheadPrice[" + bzn + "]" + " ; " +  str("%.02f" % value) + " ; " +  str(index.timestamp()))
             print(value)
    return

def load_pr_bzn(bzn, start, end):
    s = e.query_load(country_code=bzn, start=start, end=end)
    for index, value in s.iteritems():
        #print("Entsoe ; " + "Load[" + bzn + "]" + " ; " +  str(value) + " ; " +  str(pd.to_datetime(index).timestamp()))
        print(value)
    return

def test_load_pr_bzn(bzn, start, end):
    s = e.query_load(country_code=bzn, start=start, end=end)
    for index, value in s.iteritems():
        print("Entsoe ; " + "Load[" + bzn + "]" + " ; " +  str(value) + " ; " +  str(pd.to_datetime(index).timestamp()))
        #print(value)
    return
def query_load_forecast(country_code, start, end):
    s = e.query_load_forecast(country_code=country_code, start=start, end=end)
    for index, value in s.iteritems():
        print("Entsoe ; " + "LoadForecast[" + country_code + "]" + " ; " +  str(value) + " ; " +  str(pd.to_datetime(index).timestamp()))
        #print(value)
    return


def query_generation_forecast(country_code, start, end):
    s = e.query_generation_forecast(country_code=country_code, start=start, end=end)
    for index, value in s.iteritems():
        print("Entsoe ; " + "GenerationForecast[" + country_code + "]" + " ; " +  str(value) + " ; " +  str(pd.to_datetime(index).timestamp()))
        #print(value)
    return

def query_day_ahead_generation_forecast(country_code, start, end):
    s = e.query_day_ahead_generation_forecast(country_code=country_code, start=start, end=end)
    for index, value in s.iteritems():
        print("Entsoe ; " + "DayAheadGenerationForecast[" + country_code + "]" + " ; " +  str(value) + " ; " +  str(pd.to_datetime(index).timestamp()))
        #print(value)
    return

# Extract day_ahead_prices from Entsoe for today and one day ahead and set it up as a scheduled job at 13:00 store the data to pandas dataframe and store it to my influxdb instance
# Path: entsoe_my_data.py
# Script to read energy day ahead price values from Entsoe and forward it to Home Assistant and InfluxDB

# Requires token obtained from Entsoe - token is stored in settings.py
# Requires schedule to be installed

#schedule.every().day.at("00:00").do(day_ahead_prices, start_pd, end_pd)
#schedule.every().day.at("00:00").do(load_pr_bzn, "NO_1", start_pd, end_pd)
#schedule.every().day.at("00:00").do(query_load_forecast, "NO_1", start_pd, end_pd)
#schedule.every().day.at("00:00").do(query_generation_forecast, "NO_1", start_pd, end_pd)
#schedule.every().day.at("00:00").do(query_day_ahead_generation_forecast, "NO_1", start_pd, end_pd)




#day_ahead_prices(start_pd, end_pd)
#load_pr_bzn("NO_1", start_pd, end_pd)
query_load_forecast("NO_1", start_pd, end_pd)
#entsoe_function_list = str(dir(EntsoePandasClient))
#entsoe_function_list_newline = entsoe_function_list.replace(",", ",\n")
#print(entsoe_function_list_newline)

