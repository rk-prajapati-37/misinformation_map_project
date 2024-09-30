import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="Misinformation Map", layout="wide")

# Load the CSV files
try:
    df = pd.read_csv('fake_news_data.csv')
except pd.errors.EmptyDataError:
    st.error("Fake news data file is empty or not found.")
    df = pd.DataFrame()

try:
    df_factcheck = pd.read_csv('fact_check_data.csv')
except pd.errors.EmptyDataError:
    st.error("Fact check data file is empty or not found.")
    df_factcheck = pd.DataFrame()

st.title('Misinformation Map')
st.write('Visualize fake news incidents geographically')

if not df.empty:
    # Initialize the map
    map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    # Add markers to the map
    for index, row in df.iterrows():
        if not pd.isna(row['latitude']) and not pd.isna(row['longitude']):
            folium.Marker([row['latitude'], row['longitude']], popup=row['title']).add_to(map)

    # Display the map
    folium_static(map)
else:
    st.error("No data available to display on the map.")

# Display Fact Check Data
if not df_factcheck.empty:
    st.write("Fact Check Data")
    st.write(df_factcheck)
else:
    st.error("No fact check data available to display.")

# Additional features: graphs, heat map, etc.
import plotly.express as px

# Graphs by Theme (example)
st.write("Graphs by Theme")
if 'theme' in df.columns:
    theme_counts = df['theme'].value_counts().reset_index()
    theme_counts.columns = ['theme', 'count']
    fig = px.bar(theme_counts, x='theme', y='count', title="Fake News by Theme")
    st.plotly_chart(fig)

# Heat Map
st.write("Heat Map")
from folium.plugins import HeatMap
if not df.empty:
    heat_data = [[row['latitude'], row['longitude']] for index, row in df.iterrows() if not pd.isna(row['latitude']) and not pd.isna(row['longitude'])]
    HeatMap(heat_data).add_to(map)
    folium_static(map)

# Top Personalities (assuming 'personality' column exists)
st.write("Top Personalities in Fake News")
if 'personality' in df.columns:
    top_personalities = df['personality'].value_counts().head(10)
    st.write(top_personalities)

# Top Stories by Theme
st.write("Top Stories by Theme")
if 'theme' in df.columns:
    theme_selected = st.selectbox('Select Theme', df['theme'].unique())
    top_stories_theme = df[df['theme'] == theme_selected]
    st.write(top_stories_theme)
