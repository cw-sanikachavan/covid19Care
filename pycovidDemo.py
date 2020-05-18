from geopy.geocoders import Nominatim
import pandas as pd
import time

geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
df = pd.read_csv("testingCentres.csv")
hospital = df['NamesofHospitals'].tolist()
lat = []
long = []
try:
    for h in hospital:
        lstHosp = h.split(',')[-1]
        loc = geolocator.geocode(lstHosp)
        df['latitude']=loc.latitude
        df['longitude']=loc.longitude
        print(lstHosp,loc.latitude,loc.longitude)
        lat.append(tuple([loc.latitude,loc.longitude]))
        time.sleep(2)
finally:
    dfN=pd.DataFrame(lat)
    dfN.to_csv("final.csv")
