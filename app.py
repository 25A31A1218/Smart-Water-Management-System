import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Smart Water Management",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Smart Water Management System")
st.write(
    "Monitor water consumption, identify unusual usage patterns, "
    "and explore opportunities for water conservation."
)

# Load data
data = pd.read_csv("water_data.csv")
data["Date"] = pd.to_datetime(data["Date"])

# Sidebar filters
st.sidebar.header("Filters")

locations = ["All"] + sorted(data["Location"].unique().tolist())

selected_location = st.sidebar.selectbox(
    "Select Location",
    locations
)

if selected_location != "All":
    filtered_data = data[data["Location"] == selected_location]
else:
    filtered_data = data.copy()

# -------------------------------------------------
# Key statistics
# -------------------------------------------------

total_usage = filtered_data["Water_Usage_Liters"].sum()
average_usage = filtered_data["Water_Usage_Liters"].mean()
leak_events = filtered_data["Leak_Detected"].sum()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Water Usage",
    f"{total_usage:,.0f} L"
)

col2.metric(
    "Average Daily Usage",
    f"{average_usage:,.0f} L"
)

col3.metric(
    "Possible Leak Events",
    int(leak_events)
)

st.divider()

# -------------------------------------------------
# Water usage trend
# -------------------------------------------------

st.subheader("📈 Water Consumption Trend")

daily_usage = (
    filtered_data
    .groupby("Date", as_index=False)["Water_Usage_Liters"]
    .sum()
)

fig = px.line(
    daily_usage,
    x="Date",
    y="Water_Usage_Liters",
    markers=True,
    title="Daily Water Consumption"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# Location comparison
# -------------------------------------------------

st.subheader("🏢 Water Usage by Location")

location_usage = (
    filtered_data
    .groupby("Location", as_index=False)["Water_Usage_Liters"]
    .sum()
    .sort_values("Water_Usage_Liters", ascending=False)
)

fig2 = px.bar(
    location_usage,
    x="Location",
    y="Water_Usage_Liters",
    title="Total Water Consumption by Location"
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------
# Leak detection
# -------------------------------------------------

st.subheader("🚨 Possible Water Leakage")

leaks = filtered_data[
    filtered_data["Leak_Detected"] == 1
]

if len(leaks) > 0:
    st.warning(
        f"{len(leaks)} possible abnormal water-usage event(s) detected."
    )

    st.dataframe(
        leaks,
        use_container_width=True
    )
else:
    st.success("No possible leakage events detected.")

# -------------------------------------------------
# Conservation recommendations
# -------------------------------------------------

st.subheader("💡 Conservation Recommendations")

if average_usage > 2500:
    st.write(
        "• Average consumption is relatively high. "
        "Consider reducing unnecessary water usage."
    )

if leak_events > 0:
    st.write(
        "• Investigate locations with abnormal usage "
        "to identify possible leaks."
    )

if average_usage <= 2500 and leak_events == 0:
    st.success(
        "Water usage appears relatively stable. "
        "Continue monitoring consumption regularly."
    )

# -------------------------------------------------
# Raw data
# -------------------------------------------------

with st.expander("View Water Usage Data"):
    st.dataframe(
        filtered_data,
        use_container_width=True
    )
