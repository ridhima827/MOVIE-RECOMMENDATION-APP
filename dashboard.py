import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Titanic Data Analytics Dashboard")

# Read CSV File
data = pd.read_csv("titanic.csv")

# Show Dataset
st.subheader("Dataset")
st.dataframe(data)

# KPI Metrics
st.subheader("KPI Metrics")

total_passengers = data.shape[0]
survived = data["Survived"].sum()
average_age = round(data["Age"].mean(), 2)

col1, col2, col3 = st.columns(3)

col1.metric("Total Passengers", total_passengers)
col2.metric("Survived", survived)
col3.metric("Average Age", average_age)

# Sidebar Filter
st.sidebar.header("Filter Data")

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    options=data["Sex"].unique(),
    default=data["Sex"].unique()
)

filtered_data = data[data["Sex"].isin(selected_gender)]

# Show Filtered Data
st.subheader("Filtered Data")
st.dataframe(filtered_data)

# Line Chart
st.subheader("Line Chart")

line_chart = px.line(
    filtered_data,
    x=filtered_data.index,
    y="Age",
    title="Age Line Chart"
)

st.plotly_chart(line_chart)

# Bar Chart
st.subheader("Bar Chart")

bar_chart = px.bar(
    filtered_data,
    x="Pclass",
    color="Survived",
    title="Passenger Class vs Survival"
)

st.plotly_chart(bar_chart)

# Pie Chart
st.subheader("Pie Chart")

pie_chart = px.pie(
    filtered_data,
    names="Sex",
    title="Gender Distribution"
)

st.plotly_chart(pie_chart)

# Histogram
st.subheader("Histogram")

histogram = px.histogram(
    filtered_data,
    x="Age",
    nbins=20,
    title="Age Histogram"
)

st.plotly_chart(histogram)

# Scatter Plot
st.subheader("Scatter Plot")

scatter_chart = px.scatter(
    filtered_data,
    x="Age",
    y="Fare"
)