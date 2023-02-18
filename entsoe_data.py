import pandas as pd
from settings import api_key
from entsoe import EntsoePandasClient

e = EntsoePandasClient(api_key=api_key, retry_count=20, retry_delay=30)

start_pd = pd.Timestamp('20221201', tz='Europe/Brussels')
end_pd = pd.Timestamp('20221231', tz='Europe/Brussels')

domains = ["DK_1"]

for cntr in domains:
    df = e.query_wind_and_solar_forecast(country_code=cntr, start=start_pd, end=end_pd, psr_type=None)
    df.to_csv('WindandSolarForecast_Dec22' + cntr + '.csv', sep=';', header=True)
# df = e.query_generation_per_plant(country_code=cntr, start=start_pd, end=end_pd, psr_type=None)
# df.to_csv('GenerationPerPlant_Oct22a' + cntr + '.csv', sep=';', header=True)

