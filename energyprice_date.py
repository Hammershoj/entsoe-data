# Script to read energy day ahead price values from Entsoe and forward it to Home Assistant and InfluxDB
# Requires token obtained from Entsoe - token is stored in settings.py
#
# Version 0.2  02.01.2022
# by hammershoj


import pandas as pd
import schedule
import time, argparse
from hass_influx import *
from aidon_obis import *
from datetime import date, timedelta
from settings import api_key, hass_token
from entsoe import EntsoePandasClient

e = EntsoePandasClient(api_key=api_key, retry_count=20, retry_delay=30)

#lst = list()
start_pd = pd.Timestamp('20220110', tz='Europe/Brussels')
end_pd = pd.Timestamp('20220111', tz='Europe/Brussels')

parser = argparse.ArgumentParser(description='Forward Entsoe day ahead price data to Home Assistant and InfluxDB')
parser.add_argument('--influx_host')
parser.add_argument('--influx_db')
parser.add_argument('--hass_host')
args = parser.parse_args()

# Class used to forward data to Home Assistant and InfluxDB
hi = hass_influx(
	inf_host=args.influx_host,
	inf_db=args.influx_db,
	hass_host=args.hass_host,
	hass_token=hass_token)

domains = ["NO_1", "NO_2", "NO_3", "NO_4", "NO_5", "DK_1", "DK_2", "DE_LU", "SE_1", "SE_2", "SE_3", "SE_4"]

def day_ahead_prices(start, end):
    today = pd.Timestamp(date.fromtimestamp(time.time()), tz='Europe/Brussels')
    if start is None:
        start = today + timedelta(days=1)
    if end is None:
        end = today + timedelta(days=2)
   
    for bzn in domains:
        s = e.query_day_ahead_prices(bzn, start=start, end=end)
        for i in range(0,s.count()):
             print("Entsoe ; " + "DayAheadPrice[" + bzn + "]" + " ; " +  str("%.02f" % s[i]) + " ; " +  str(s.index[i].timestamp()))
             #hi.post("Entsoe", "DayAheadPrice[" + bzn + "]" , "%.02f" % s[i], hass_name="Energy Price",  hass_unit="NOK/kWh", ts=s.index[i].timestamp())
    return

def load_pr_bzn(bzn, start, end):
    s = e.query_load(bzn, start=start, end=end)
    for i in range(0,s.count()):
        print("Entsoe ; " + "Load[" + bzn + "]" + " ; " +  str("%.02f" % s[i]) + " ; " +  str(s.index[i].timestamp()))
        #hi.post("Entsoe", "Load[" + bzn + "]" , "%.02f" % s[i], hass_name="Load",  hass_unit="MW", ts=s.index[i].timestamp())
    return



day_ahead_prices(start_pd, end_pd)
load_pr_bzn("NO_2", start_pd, end_pd)

#schedule.every().day.at("13:10").do(day_ahead_prices, start=None, end=None)

while True:
    #schedule.run_pending()
    time.sleep(60) # wait one minute

#schedule.every().day.at("13:10").do(day_ahead_prices, start=start_pd, end=end_pd, country_code='NO_2')
#result = pd.concat(lst)
#print(lst)
#result.to_csv('result.csv', sep=';', header=False)
