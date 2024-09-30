import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="Misinformation Map", layout="wide")

# Load data
df = pd.read_csv('fake_news_data.csv')

st.title('Misinformation Map')
st.write('Visualize fake news incidents geographically')

# Initialize map
map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

for index, row in df.iterrows():
    if not pd.isna(row['latitude']) and not pd.isna(row['longitude']):
        folium.Marker([row['latitude'], row['longitude']], popup=row['title']).add_to(map)

folium_static(map)

# Add search and filters
# Add date range filter, category filter etc.
import plotly.express as px

# Example theme data, replace with actual data
df_themes = pd.DataFrame({
    "theme": ["Politics", "Health", "Environment"],
    "count": [10, 20, 15]
})

st.write("Graphs by Theme")
fig = px.bar(df_themes, x='theme', y='count', title="Fake News by Theme")
st.plotly_chart(fig)


from folium.plugins import HeatMap

st.write("Heat Map")
heat_data = [[row['latitude'], row['longitude']] for index, row in df.iterrows() if not pd.isna(row['latitude']) and not pd.isna(row['longitude'])]
HeatMap(heat_data).add_to(map)
folium_static(map)


st.write("Top Personalities in Fake News")
df_personalities = pd.DataFrame({
    "personality": ["Person1", "Person2", "Person3"],
    "fake_news_count": [15, 25, 40]
})
st.write(df_personalities)


st.write("Top Stories by Theme")
theme_selected = st.selectbox('Select Theme', df['theme'].unique())
top_stories_theme = df[df['theme'] == theme_selected]
st.write(top_stories_theme)

st.write("Top Stories by Category")
category_selected = st.selectbox('Select Category', df['category'].unique())
top_stories_category = df[df['category'] == category_selected]
st.write(top_stories_category)

import datetime

st.write("Select Date Range")
start_date = st.date_input("Start date", datetime.date(2020, 1, 1))
end_date = st.date_input("End date", datetime.date(2023, 1, 1))

filtered_df = df[(df['published'] >= str(start_date)) & (df['published'] <= str(end_date))]
st.write(filtered_df)


