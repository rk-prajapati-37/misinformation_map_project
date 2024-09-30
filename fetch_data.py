import feedparser
import pandas as pd

feed_url = "https://www.boomlive.in/rss"
feed = feedparser.parse(feed_url)

if not feed.entries:
    print("No entries found in the RSS feed.")
    exit()

data = []
for entry in feed.entries:
    data.append({
        "title": entry.title,
        "link": entry.link,
        "published": entry.published,
        "summary": entry.summary
        # Add "location" if available
    })

df = pd.DataFrame(data)
df.to_csv('fake_news_data.csv', index=False)
print("Data fetched and saved to fake_news_data.csv")
