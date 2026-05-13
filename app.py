import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Titanic Data Analytics Dashboard")

# Read Dataset

data = pd.read_csv("titanic.csv")

# Show Dataset
st.subheader("Titanic Dataset")
st.dataframe(data)

# KPI Metrics
st.subheader("KPI Metrics")

total_passengers = data.shape[0]
total_survived = data["Survived"].sum()
average_age = round(data["Age"].mean(), 2)

col1, col2, col3 = st.columns(3)

col1.metric("Total Passengers", total_passengers)
col2.metric("Total Survived", total_survived)
col3.metric("Average Age", average_age)

# Filter Data
st.sidebar.header("Filter Data")

selected_class = st.sidebar.multiselect(
    "Select Passenger Class",
    options=data["Pclass"].unique(),
    default=data["Pclass"].unique()
)

filtered_data = data[data["Pclass"].isin(selected_class)]

# Show Filtered Data
st.subheader("Filtered Data")
st.dataframe(filtered_data)

# Line Chart
st.subheader("Line Chart")

line_chart = px.line(
    filtered_data,
    x=filtered_data.index,
    y="Age",
    title="Age Distribution"
)

st.plotly_chart(line_chart)

# Bar Chart
st.subheader("Bar Chart")

bar_chart = px.bar(
    filtered_data,
    x="Sex",
    color="Survived",
    title="Survival Count by Gender"
)

st.plotly_chart(bar_chart)

# Area Chart
st.subheader("Area Chart")

area_chart = px.area(
    filtered_data,
    x=filtered_data.index,
    y="Fare",
    title="Fare Distribution"
)

st.plotly_chart(area_chart)

# Pie Chart
st.subheader("Pie Chart")

pie_chart = px.pie(
    filtered_data,
    names="Survived",
    title="Survival Percentage"
)

st.plotly_chart(pie_chart)

# Histogram
st.subheader("Histogram")

histogram = px.histogram(
    filtered_data,
    x="Age",
    title="Age Histogram"
)

st.plotly_chart(histogram)
