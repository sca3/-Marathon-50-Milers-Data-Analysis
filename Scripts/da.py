import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.extra.rate_limiter import RateLimiter

# Load dataset
df = pd.read_csv('ff_race_50.csv')

# Drop NA columns and explicitly copy to avoid SettingWithCopyWarning
df2 = df.dropna(axis=1).copy()

# Add new columns safely
df2['full name'] = df2['First'] + ' ' + df2['Last']
df2['Time'] = pd.to_timedelta(df2['Time'])
df2['Total_Minutes'] = (df2['Time'].dt.total_seconds() / 60).round().astype(int)

# Rename column
df2.rename(columns={'Division': 'Gender'}, inplace=True)

# Function to get latitude/longitude
def get_lat_long(city, state):
    address = f"{city}, {state}"
    try:
        geolocator = Nominatim(user_agent="running", timeout=10)
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        return None, None

# Apply function to get coordinates
df2['latitude'], df2['longitude'] = zip(
    *df2.apply(lambda x: get_lat_long(x['City'], x['State']), axis=1)
)

df2['latlong'] = df2['latitude'].astype(str) + ', ' + df2['longitude'].astype(str)

print(df2.head())
df2.to_csv('ultracleanedupdata_output.csv', index=False)
