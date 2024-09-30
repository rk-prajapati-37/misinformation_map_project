import feedparser
import pandas as pd
import requests

# BoomLive RSS Feed URL
feed_url = "https://www.boomlive.in/feeds.xml"
feed = feedparser.parse(feed_url)

if not feed.entries:
    print("No entries found in the RSS feed.")
    exit()

data = []
api_key = 'AIzaSyCM4vOEEbwzgPmOCMd9X2jh_JBISTGEHOs'  # New API key

for entry in feed.entries:
    # Example address
    address = "New York, USA"  # Replace with dynamic addresses if available
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

if df.empty:
    print("DataFrame is empty. No data to save.")
else:
    print(df.head())  # Debug print to check data
    df.to_csv('fake_news_data.csv', index=False)
    print("Data fetched and saved to fake_news_data.csv")

# Additional part to fetch data from Google's Fact Check API
query = 'Covid-19'  # Example search query
url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={api_key}"
response = requests.get(url)
fact_checks = response.json().get('claims', [])

if not fact_checks:
    print("No data found.")
else:
    print("Fact checks found:", len(fact_checks))

data = []
for fact in fact_checks:
    claim_review = fact.get('claimReview', [{}])[0]
    data.append({
        "title": fact.get('text', 'N/A'),
        "url": claim_review.get('url', 'N/A'),
        "source": claim_review.get('publisher', {}).get('name', 'N/A'),
        "reviewDate": claim_review.get('reviewDate', 'N/A')
    })

df_factcheck = pd.DataFrame(data)

if df_factcheck.empty:
    print("DataFrame is empty. No data to save.")
else:
    print(df_factcheck.head())
    df_factcheck.to_csv('fact_check_data.csv', index=False)
    print("Fact check data fetched and saved to fact_check_data.csv")
