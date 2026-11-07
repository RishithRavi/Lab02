# This creates the page for displaying data visualizations.

import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
st.header("Part 1: My Weekly Study Hours (data.json)")

# open the json file and load it into a dictionary
with open("data.json", "r") as f:
    json_data = json.load(f)

# make lists of the labels and values
subjects = []
hours = []
for point in json_data["data_points"]:
    subjects.append(point["label"])
    hours.append(point["value"])

# STATIC GRAPH - pie chart with matplotlib (advanced chart)
st.subheader("Static: Share of Study Time by Subject")
fig1, ax1 = plt.subplots()
ax1.pie(hours, labels=subjects, autopct="%1.1f%%")
ax1.set_title(json_data["chart_title"])
st.pyplot(fig1)

# DYNAMIC GRAPH - bar chart that changes with a multiselect
st.subheader("Dynamic: Compare Subjects")

# set up session state so the selection is remembered
if "chosen_subjects" not in st.session_state:
    st.session_state.chosen_subjects = subjects

st.multiselect("Pick subjects to show:", subjects, key="chosen_subjects")

json_df = pd.DataFrame({"Subject": subjects, "Hours": hours})
filtered_json_df = json_df[json_df["Subject"].isin(st.session_state.chosen_subjects)]

if len(filtered_json_df) > 0:
    st.bar_chart(filtered_json_df, x="Subject", y="Hours")

    # EXTRA CREDIT - mean and median that update with the chart
    json_mean = filtered_json_df["Hours"].mean()
    json_median = filtered_json_df["Hours"].median()

    # remember the last values in session state so we can show the change
    if "prev_json_mean" not in st.session_state:
        st.session_state.prev_json_mean = json_mean
        st.session_state.prev_json_median = json_median

    col1, col2 = st.columns(2)
    col1.metric("Mean Hours", round(json_mean, 2), delta=round(json_mean - st.session_state.prev_json_mean, 2))
    col2.metric("Median Hours", round(json_median, 2), delta=round(json_median - st.session_state.prev_json_median, 2))

    st.session_state.prev_json_mean = json_mean
    st.session_state.prev_json_median = json_median
else:
    st.write("Pick at least one subject to see the chart.")


# PART 2: GRAPHS FROM data.csv
st.divider()
st.header("Part 2: Sleep Survey Results (data.csv)")

csv_df = pd.read_csv("data.csv")
# fix capitalization so "biology" and "BIOLOGY" count as the same major
csv_df["Category"] = csv_df["Category"].str.strip().str.title()

# STATIC GRAPH - bar chart of average sleep per major with matplotlib (advanced chart)
st.subheader("Static: Average Sleep by Major")
avg_sleep = csv_df.groupby("Category")["Value"].mean()

fig2, ax2 = plt.subplots()
ax2.bar(avg_sleep.index, avg_sleep.values)
ax2.set_title("Average Hours of Sleep by Major")
ax2.set_xlabel("Major")
ax2.set_ylabel("Average Hours of Sleep")
plt.xticks(rotation=45)
st.pyplot(fig2)

# DYNAMIC GRAPH - line chart of responses for the major the user picks
st.subheader("Dynamic: Sleep Responses for One Major")

majors = list(csv_df["Category"].unique())

if "chosen_major" not in st.session_state:
    st.session_state.chosen_major = majors[0]

st.radio("Pick a major:", majors, key="chosen_major")

major_df = csv_df[csv_df["Category"] == st.session_state.chosen_major]
major_df = major_df.reset_index(drop=True)
st.line_chart(major_df["Value"])
st.write("Each point is one person's answer (x = response number, y = hours of sleep).")

# EXTRA CREDIT - mean and median that update with the chart
csv_mean = major_df["Value"].mean()
csv_median = major_df["Value"].median()

if "prev_csv_mean" not in st.session_state:
    st.session_state.prev_csv_mean = csv_mean
    st.session_state.prev_csv_median = csv_median

col3, col4 = st.columns(2)
col3.metric("Mean Sleep (hrs)", round(csv_mean, 2), delta=round(csv_mean - st.session_state.prev_csv_mean, 2))
col4.metric("Median Sleep (hrs)", round(csv_median, 2), delta=round(csv_median - st.session_state.prev_csv_median, 2))

st.session_state.prev_csv_mean = csv_mean
st.session_state.prev_csv_median = csv_median
