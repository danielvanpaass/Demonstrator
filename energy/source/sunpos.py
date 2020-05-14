import pandas as pd
import pvlib


index = pd.date_range(start='2019-01-01 01:00', freq='1h', periods=24)
solar_position = pvlib.solarposition.get_solarposition(index,51.998827,4.373471)
