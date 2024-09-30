import feedparser
import pandas as pd
import requests

feed_url = "https://www.boomlive.in/rss"
feed = feedparser.parse(feed_url)

if not feed.entries:
    print("No entries found in the RSS feed.")
    exit()

data = []
api_key = 'YOUR_GOOGLE_API_KEY'  # Replace with your actual Google API key

for entry in feed.entries:
    address = "London, UK"  # Example address; replace with actual addresses from your data if available
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(geocode_url)
    geocode_data = response.json()

    if geocode_data['status'] == 'OK':
        latitude = geocode_data['results'][0]['geometry']['location']['lat']
        longitude = geocode_data['results'][0]['geometry']['location']['lng']
    else:
        print(f"Geocoding failed for address: {address}")
        latitude = None
        longitude = None

    data.append({
        "title": entry.title,
        "link": entry.link,
        "published": entry.published,
        "summary": entry.summary,
        "latitude": latitude,
        "longitude": longitude
    })

df = pd.DataFrame(data)

# Remove rows with missing geolocation data
df = df.dropna(subset=['latitude', 'longitude'])

if df.empty:
    print("DataFrame is empty. No data to save.")
else:
    df.to_csv('fake_news_data.csv', index=False)
    print("Data fetched and saved to fake_news_data.csv")
