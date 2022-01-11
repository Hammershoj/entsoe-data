import pandas as pd
import schedule
import time
from datetime import date, timedelta
from settings import api_key
from entsoe import EntsoePandasClient
e = EntsoePandasClient(api_key=api_key, retry_count=20, retry_delay=30)

ts = time.time()
start_pd = pd.Timestamp('20211228', tz='Europe/Brussels')
end_pd = pd.Timestamp('20211229', tz='Europe/Brussels')

  #result.to_csv('result.csv', sep=';', header=False)

def day_ahead_prices(start, end, country_code):
    today = pd.Timestamp(date.fromtimestamp(time.time()), tz='Europe/Brussels')
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)
    s = e.query_day_ahead_prices(country_code, start=tomorrow, end=day_after_tomorrow)
    print(s)
    return s

schedule.every().day.at("13:10").do(day_ahead_prices, start=start_pd, end=end_pd, country_code='NO_2')

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute