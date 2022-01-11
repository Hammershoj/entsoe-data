import pandas as pd
import schedule
import time, argparse
from hass_influx import *
from aidon_obis import *
from datetime import date, timedelta
from settings import api_key
from entsoe import EntsoePandasClient

e = EntsoePandasClient(api_key=api_key, retry_count=20, retry_delay=30)

start_pd = pd.Timestamp('20211228', tz='Europe/Brussels')
end_pd = pd.Timestamp('20211229', tz='Europe/Brussels')

#s = e.query_imbalance_prices(country_code='BE', start=start, end=end, as_dataframe=True)

domains = ["NO_1","NO_2"]

lst = list()


for bzn in domains:
    s = e.query_day_ahead_prices(country_code='NO_2', start=start_pd, end=end_pd)
    if s is not None:
        lst.append(s)

def day_ahead_prices(start, end, country_code):
    today = pd.Timestamp(date.fromtimestamp(time.time()), tz='Europe/Brussels')
    if start is None:
        start = today + timedelta(days=1)
    if end is None:
        end = today + timedelta(days=2)
    s = e.query_day_ahead_prices(country_code, start=start, end=end)
    for i in range(0,s.count()):
        print("Entsoe ; " + "DayAheadPrice[" + country_code + "]" + " ; " +  str("%.02f" % s[i]) + " ; " +  str(s.index[i]))
    # hi.post("Entsoe", "DayAheadPrice[" + country_code + "]" , "%.02f" % s[i], hass_name="Energy Price",  hass_unit="NOK/kWh", ts=s.index[i])
	#print(s)
    return

day_ahead_prices(start_pd, None,'NO_2')
schedule.every().day.at("13:10").do(day_ahead_prices, start=start_pd, end=end_pd, country_code='NO_2')
result = pd.concat(lst)
#print(lst)
result.to_csv('result.csv', sep=';', header=False)
