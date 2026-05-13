import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# -------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------
st.set_page_config(
    page_title="AI Movie Recommender",
    layout="wide",
    page_icon="🎬"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #0f0c29, #302b63, #24243e);
    color: white;
}

h1, h2, h3 {
    color: white;
}

.movie-card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    transition: 0.4s;
}

.movie-card:hover {
    transform: scale(1.03);
    background: rgba(255,255,255,0.15);
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# DATASET
# -------------------------------------------------
movies = {
    "Movie Name": [
        "Avengers", "Iron Man", "John Wick",
        "Extraction", "The Conjuring", "Insidious",
        "Titanic", "The Notebook", "Interstellar",
        "Inception", "Avatar", "Doctor Strange"
    ],

    "Category": [
        "Action", "Action", "Action",
        "Action", "Horror", "Horror",
        "Romance", "Romance", "Sci-Fi",
        "Sci-Fi", "Sci-Fi", "Fantasy"
    ],

    "Rating": [
        4.8, 4.7, 4.6,
        4.4, 4.5, 4.3,
        4.9, 4.2, 4.9,
        4.8, 4.7, 4.6
    ],

    "Year": [
        2012, 2008, 2019,
        2020, 2013, 2010,
        1997, 2004, 2014,
        2010, 2009, 2016
    ],

    "Votes": [
        950, 850, 780,
        650, 720, 600,
        980, 550, 990,
        920, 890, 760
    ]
}

df = pd.DataFrame(movies)

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.title("🎬 AI Movie Recommendation Dashboard")

st.write("### Smart recommendations with interactive animated analytics")

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.header("🎥 Filter Movies")

category = st.sidebar.selectbox(
    "Select Genre",
    ["All"] + list(df["Category"].unique())
)

rating = st.sidebar.slider(
    "Minimum Rating",
    1.0,
    5.0,
    4.0
)

# -------------------------------------------------
# FILTERING
# -------------------------------------------------
filtered_df = df[df["Rating"] >= rating]

if category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category]

# -------------------------------------------------
# MOVIE CARDS
# -------------------------------------------------
st.subheader("🔥 Recommended Movies")

col1, col2 = st.columns(2)

for i, row in filtered_df.iterrows():

    card = f"""
    <div class="movie-card">
        <h2>🎞️ {row['Movie Name']}</h2>
        <h4>🎭 Genre: {row['Category']}</h4>
        <h4>⭐ Rating: {row['Rating']}</h4>
        <h4>📅 Year: {row['Year']}</h4>
        <h4>👍 Votes: {row['Votes']}K</h4>
    </div>
    """

    if i % 2 == 0:
        col1.markdown(card, unsafe_allow_html=True)
    else:
        col2.markdown(card, unsafe_allow_html=True)

# -------------------------------------------------
# ANIMATED BAR CHART
# -------------------------------------------------
st.subheader("📊 Animated Ratings Chart")

bar_fig = px.bar(
    filtered_df,
    x="Movie Name",
    y="Rating",
    color="Category",
    text="Rating",
    hover_data=["Year", "Votes"],
    animation_frame="Movie Name",
    template="plotly_dark",
)

bar_fig.update_layout(
    title="Movie Ratings Animation",
    xaxis_title="Movies",
    yaxis_title="Ratings",
    height=600
)

bar_fig.update_traces(
    textposition="outside"
)

st.plotly_chart(bar_fig, use_container_width=True)

# -------------------------------------------------
# BUBBLE CHART
# -------------------------------------------------
st.subheader("🎈 Interactive Bubble Chart")

bubble_fig = px.scatter(
    filtered_df,
    x="Year",
    y="Rating",
    size="Votes",
    color="Category",
    hover_name="Movie Name",
    hover_data=["Votes"],
    size_max=60,
    animation_frame="Year",
    template="plotly_dark"
)

bubble_fig.update_layout(
    height=650
)

st.plotly_chart(bubble_fig, use_container_width=True)

# -------------------------------------------------
# DONUT CHART
# -------------------------------------------------
st.subheader("🍩 Category Distribution")

pie_fig = px.pie(
    filtered_df,
    names="Category",
    values="Votes",
    hole=0.55,
    color_discrete_sequence=px.colors.sequential.Rainbow
)

pie_fig.update_layout(
    template="plotly_dark",
    height=550
)

st.plotly_chart(pie_fig, use_container_width=True)

# -------------------------------------------------
# RADAR CHART
# -------------------------------------------------
st.subheader("🕸️ Movie Performance Radar")

radar_fig = go.Figure()

radar_fig.add_trace(go.Scatterpolar(
    r=filtered_df["Rating"],
    theta=filtered_df["Movie Name"],
    fill='toself',
    name='Movie Ratings'
))

radar_fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5]
        )
    ),
    template="plotly_dark",
    height=650
)

st.plotly_chart(radar_fig, use_container_width=True)

# -------------------------------------------------
# LINE CHART
# -------------------------------------------------
st.subheader("📈 Movie Trends Over Years")

line_fig = px.line(
    filtered_df,
    x="Year",
    y="Rating",
    color="Category",
    markers=True,
    hover_name="Movie Name",
    template="plotly_dark"
)

line_fig.update_layout(
    height=600
)

st.plotly_chart(line_fig, use_container_width=True)

# -------------------------------------------------
# HEATMAP
# -------------------------------------------------
st.subheader("🔥 Ratings Heatmap")

heat_data = filtered_df.pivot_table(
    values="Rating",
    index="Category",
    columns="Year"
)

heat_fig = go.Figure(
    data=go.Heatmap(
        z=heat_data.values,
        x=heat_data.columns,
        y=heat_data.index,
        colorscale="Rainbow"
    )
)

heat_fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(heat_fig, use_container_width=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("""
---
# 🚀 Features Included

✅ AI Movie Recommendation System  
✅ Beautiful Dark UI  
✅ Animated Plotly Graphs  
✅ Hover Effects  

✅ Interactive Dashboard  
✅ Bubble Charts  
✅ Radar Charts  
✅ Heatmaps  
✅ Donut Charts  
✅ Smart Filtering  
""")