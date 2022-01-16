import pandas as pd
import schedule
import time
from datetime import date, timedelta
from settings import api_key
from entsoe import EntsoePandasClient

e = EntsoePandasClient(api_key=api_key, retry_count=20, retry_delay=30)

start_pd = pd.Timestamp('20211201', tz='Europe/Brussels')
end_pd = pd.Timestamp('20220101', tz='Europe/Brussels')

#s = e.query_imbalance_prices(country_code='BE', start=start, end=end, as_dataframe=True)

domains = ["DK_CA","NO","DE_50HZ","SE"]

#for cntr in domains:
    #df = e.query_generation_per_plant(country_code=cntr, start=start_pd, end=end_pd)
    #df.to_csv('GenerationPerPlant_Dec21' + cntr + '.csv', sep=';', header=True)
df = e.query_crossborder_flows(country_code_from="NO", country_code_to="DE_50HZ", start=start_pd, end=end_pd)
df.to_csv('CrossBorderFlow_Dec21_NO-DE_50HZ.csv', sep=';', header=True)    

def day_ahead_prices(start, end, country_code):
    today = pd.Timestamp(date.fromtimestamp(time.time()), tz='Europe/Brussels')
    if start is None:
        start = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)
    s = e.query_day_ahead_prices(country_code, start=start, end=day_after_tomorrow)
    for i in range(0,s.count()):
	    #print(str(s.index[i]) + "  " + country_code + "  " + str("%.02f" % s[i]) + "NOK/kWh")
        print("Entsoe ; " + "DayAheadPrice[" + country_code + "]" + " ; " +  str("%.02f" % s[i]) + " ; " +  str(s.index[i]))
    # hi.post("Entsoe", "DayAheadPrice[" + country_code + "]" , "%.02f" % s[i], hass_name="Energy Price",  hass_unit="NOK/kWh", ts=s.index[i])
	#print(s)
    return

#day_ahead_prices(start_pd,end_pd, 'NO_2')
#schedule.every().day.at("13:10").do(day_ahead_prices, start=start_pd, end=end_pd, country_code='NO_2')

