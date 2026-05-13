import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Movie Recommendation App",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown("""
<style>

.main {
    background: linear-gradient(to right, #141E30, #243B55);
    color: white;
}

h1, h2, h3 {
    color: white;
}

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(12px);
}

.movie-card {
    padding: 20px;
    border-radius: 20px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    text-align: center;
    color: white;
    transition: 0.5s;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

.movie-card:hover {
    transform: scale(1.08);
    box-shadow: 0px 0px 30px cyan;
}

.metric-card {
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    color: white;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# MOVIE DATA
# -----------------------------------
movies = {
    "Movie Name": [
        "Avengers",
        "Iron Man",
        "The Conjuring",
        "Insidious",
        "Titanic",
        "The Notebook",
        "John Wick",
        "Extraction",
        "Interstellar",
        "Inception"
    ],

    "Category": [
        "Action",
        "Action",
        "Horror",
        "Horror",
        "Romance",
        "Romance",
        "Action",
        "Action",
        "Sci-Fi",
        "Sci-Fi"
    ],

    "Rating": [
        4.8,
        4.7,
        4.5,
        4.3,
        4.9,
        4.2,
        4.6,
        4.4,
        4.9,
        4.8
    ]
}

df = pd.DataFrame(movies)

# -----------------------------------
# TITLE
# -----------------------------------
st.title("🎬 AI Movie Recommendation Dashboard")

st.write("Explore movies with animated visualizations ✨")

# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.header("🎭 Filter Movies")

category = st.sidebar.selectbox(
    "Choose Category",
    df["Category"].unique()
)

filtered_df = df[df["Category"] == category]

# -----------------------------------
# KPI CARDS
# -----------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h2>🎥 Movies</h2>
        <h1>{len(filtered_df)}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h2>⭐ Avg Rating</h2>
        <h1>{round(filtered_df['Rating'].mean(),2)}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:

    top_movie = filtered_df.sort_values(
        by="Rating",
        ascending=False
    ).iloc[0]

    st.markdown(f"""
    <div class="metric-card">
        <h2>🔥 Top Movie</h2>
        <h1>{top_movie['Movie Name']}</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------
# MOVIE CARDS
# -----------------------------------
st.subheader(f"🍿 {category} Movies")

cols = st.columns(len(filtered_df))

for i, row in filtered_df.iterrows():

    with cols[i % len(filtered_df)]:

        st.markdown(f"""
        <div class="movie-card">
            <h2>{row['Movie Name']}</h2>
            <h3>⭐ {row['Rating']}</h3>
            <p>{row['Category']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------
# ADVANCED BAR CHART
# -----------------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=filtered_df["Movie Name"],
        y=filtered_df["Rating"],

        text=filtered_df["Rating"],
        textposition='outside',

        marker=dict(
            color=filtered_df["Rating"],
            colorscale='Turbo',

            line=dict(
                color='white',
                width=2
            )
        ),

        hovertemplate=
        "<b>%{x}</b><br><br>" +
        "⭐ Rating: %{y}<br>" +
        "🎭 Category: " + category +
        "<extra></extra>"
    )
)

fig.update_layout(

    title={
        'text': f'🎬 {category} Movie Ratings',
        'x':0.5
    },

    template="plotly_dark",

    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',

    xaxis=dict(
        title="Movies",
        showgrid=False
    ),

    yaxis=dict(
        title="Ratings",
        range=[0,5.5],
        showgrid=True,
        gridcolor='rgba(255,255,255,0.1)'
    ),

    hoverlabel=dict(
        bgcolor="black",
        font_size=16
    ),

    transition={
        'duration': 2000,
        'easing': 'cubic-in-out'
    },

    height=550
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# ANIMATED SCATTER PLOT
# -----------------------------------
scatter_fig = px.scatter(

    filtered_df,

    x="Movie Name",
    y="Rating",

    size="Rating",

    color="Rating",

    color_continuous_scale="Rainbow",

    hover_name="Movie Name",

    hover_data=["Category"],

    template="plotly_dark",

    title="✨ Interactive Movie Analysis",

    size_max=70
)

scatter_fig.update_traces(

    mode='markers+lines',

    marker=dict(

        line=dict(
            width=3,
            color='white'
        ),

        opacity=0.9
    ),

    hovertemplate=
    "<b>%{hovertext}</b><br><br>" +
    "⭐ Rating: %{y}<br>" +
    "🎭 Category: %{customdata[0]}" +
    "<extra></extra>"
)

scatter_fig.update_layout(

    title_x=0.25,

    height=550,

    transition_duration=2000,

    paper_bgcolor='rgba(0,0,0,0)',

    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(
    scatter_fig,
    use_container_width=True
)

# -----------------------------------
# DONUT CHART
# -----------------------------------
donut_fig = px.pie(

    filtered_df,

    names="Movie Name",

    values="Rating",

    hole=0.6,

    template="plotly_dark",

    title="🎭 Rating Distribution"
)

donut_fig.update_traces(
    textinfo='percent+label'
)

st.plotly_chart(
    donut_fig,
    use_container_width=True
)

# -----------------------------------
# LINE CHART
# -----------------------------------
line_fig = px.line(

    filtered_df,

    x="Movie Name",

    y="Rating",

    markers=True,

    template="plotly_dark",

    title="📈 Movie Rating Trend"
)

line_fig.update_traces(

    line=dict(width=5),

    marker=dict(size=12)
)

line_fig.update_layout(

    height=500,

    transition_duration=2000
)

st.plotly_chart(
    line_fig,
    use_container_width=True
)

# -----------------------------------
# DATAFRAME
# -----------------------------------
st.subheader("📋 Movie Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("""
---
<center>
<h3>🎬 Built using Streamlit + Plotly</h3>
</center>
""", unsafe_allow_html=True)