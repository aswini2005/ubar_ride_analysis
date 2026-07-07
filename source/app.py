import pandas as pd
import plotly.express as px
import streamlit as st


# PAGE CONFIG

st.set_page_config(
    page_title=" Uber Ride Analytics Dashboard",
    page_icon="🚖",
    layout="wide"
)


# DATA LOADING

DATA_PATH = r"C:\Users\Aswini0905\Desktop\ubar_ride_analysis\dataset\ncr_ride_bookings.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    df.columns = df.columns.str.strip()

    df["Hour"] = pd.to_datetime(
        df["Time"],
        errors="coerce"
    ).dt.hour

    return df


df = load_data()


# SIDEBAR

st.sidebar.title("Dashboard Filters")

vehicle_filter = st.sidebar.multiselect(
    "Vehicle Type",
    sorted(df["Vehicle Type"].dropna().unique()),
    default=sorted(df["Vehicle Type"].dropna().unique())
)

status_filter = st.sidebar.multiselect(
    "Booking Status",
    sorted(df["Booking Status"].dropna().unique()),
    default=sorted(df["Booking Status"].dropna().unique())
)

payment_filter = st.sidebar.multiselect(
    "Payment Method",
    sorted(df["Payment Method"].dropna().unique()),
    default=sorted(df["Payment Method"].dropna().unique())
)

filtered_df = df[
    (df["Vehicle Type"].isin(vehicle_filter)) &
    (df["Booking Status"].isin(status_filter)) &
    (df["Payment Method"].isin(payment_filter))
]

# CHART STYLING FUNCTION

def style_chart(fig, title, x_title="", y_title=""):

    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            x=0.5,
            xanchor="center",
            font=dict(size=22)
        ),

        xaxis_title=f"<b>{x_title}</b>",
        yaxis_title=f"<b>{y_title}</b>",

        xaxis=dict(
            title_font=dict(size=16),
            tickfont=dict(
                size=13,
                family="Arial Black"
            )
        ),

        yaxis=dict(
            title_font=dict(size=16),
            tickfont=dict(
                size=13,
                family="Arial Black"
            )
        ),

        height=450
    )

    return fig


# HEADER
st.markdown(
"""
<h1 style='text-align:center;color:#1f77b4'>
🚖  Uber Ride Analytics Dashboard
</h1>
""",
unsafe_allow_html=True
)

st.markdown("---")

# KPI SECTION

total_bookings = len(filtered_df)

total_revenue = int(filtered_df["Booking Value"].sum())

avg_distance = filtered_df["Ride Distance"].mean()

avg_rating = filtered_df["Driver Ratings"].mean()

completed = len(
    filtered_df[
        filtered_df["Booking Status"] == "Completed"
    ]
)

completion_rate = (
    completed / total_bookings * 100
    if total_bookings > 0 else 0
)

failure_rate = (
    (total_bookings - completed) / total_bookings * 100
    if total_bookings > 0 else 0
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "🚖 Customer Ride Demand",
    f"{total_bookings:,}"
)

c2.metric(
    "💰 Business Revenue Generated",
    f"₹{total_revenue:,}"
)

c3.metric(
    "📍 Average Trip Distance",
    f"{avg_distance:.2f} km"
)

c4, c5, c6 = st.columns(3)

c4.metric(
    "⭐ Customer Service Score",
    f"{avg_rating:.2f}"
)

c5.metric(
    "✅ Trip Success Rate",
    f"{completion_rate:.1f}%"
)

c6.metric(
    "⚠️ Operational Failure Rate",
    f"{failure_rate:.1f}%"
)

st.markdown("---")

# ROW 1

col1, col2 = st.columns(2)


# CHART 1

with col1:

  peak = (
    filtered_df.groupby("Hour")["Booking ID"]
    .count()
    .reset_index()
)

# Average bookings per hour
avg_bookings = peak["Booking ID"].mean()

# Peak vs Non-Peak classification
peak["Demand Category"] = peak["Booking ID"].apply(
    lambda x:"Peak Hour"
    if x >= avg_bookings
    else "Non-Peak Hour"
)

# Create time ranges like 8-9 AM
def create_time_range(hour):

    next_hour = (hour + 1) % 24

    start_period = (
        "AM" if hour < 12 else "PM"
    )

    display_hour = (
        hour if 1 <= hour <= 12
        else 12 if hour == 0
        else hour - 12
    )

    display_next_hour = (
        next_hour if 1 <= next_hour <= 12
        else 12 if next_hour == 0
        else next_hour - 12
    )

    return (
        f"{display_hour}-{display_next_hour} "
        f"{start_period}"
    )

peak["Time Range"] = peak["Hour"].apply(
    create_time_range
)

fig = px.bar(
    peak,
    x="Time Range",
    y="Booking ID",
    color="Demand Category",
    text="Booking ID",

    color_discrete_map={
        "Peak Hour": "#EF553B",
        "Non-Peak Hour": "#636EFA"
    }
)

fig.update_traces(
    textposition="outside"
)

fig = style_chart(
    fig,
    "🕒 Hourly Ride Demand",
    "Time Interval",
    "Number of Ride Requests"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# CHART 2

revenue = (
        filtered_df.groupby(
            "Vehicle Type"
        )["Booking Value"]
        .sum()
        .astype(int)
        .reset_index()
    )

fig = px.bar(
        revenue,
        x="Vehicle Type",
        y="Booking Value",
        text="Booking Value"
    )

fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside"
    )

fig = style_chart(
        fig,
        "💰 Revenue by Vehicle Catagory",
        "Vehicle Category",
        "Revenue Generated (₹)"
    )
fig.update_layout(height=350)

col1,col2,col3=st.columns([2,3,2])

st.plotly_chart(
        fig,
        use_container_width=True
    )


# ROW 2

col3, col4 = st.columns(2)

with col3:

    fig = px.pie(
        filtered_df,
        names="Payment Method",
        hole=0.5
    )

    fig.update_traces(
        textfont_size=13
    )

    fig = style_chart(
        fig,
        "💳 Payment Method Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col4:

    fig = px.histogram(
        filtered_df,
        x="Driver Ratings",
        nbins=20
    )

    fig = style_chart(
        fig,
        "⭐ Driver Rating Distributions",
        "Driver Rating",
        "Number of Trips"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
 
# ROW 3

col5, col6 = st.columns(2)

with col5:

    pickup = (
        filtered_df["Pickup Location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    pickup.columns = [
        "Pickup Location",
        "Bookings"
    ]

    fig = px.bar(
        pickup,
        x="Pickup Location",
        y="Bookings",
        text_auto=True
    )

    fig = style_chart(
        fig,
        "📍 Top Pickup Locations",
        "Pickup Location",
        "Number of Bookings"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col6:

    drop = (
        filtered_df["Drop Location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    drop.columns = [
        "Drop Location",
        "Bookings"
    ]

    fig = px.bar(
        drop,
        x="Drop Location",
        y="Bookings",
        text_auto=True
    )

    fig = style_chart(
        fig,
        "🏁Top Drop Locations",
        "Destination",
        "Number of Trips"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# BUSINESS INSIGHTS


st.markdown("---")

st.subheader("🎯 Strategic Recommendations")

st.success(
    "Increase driver availability during commuting hours to improve ride fulfillment rates."
)

st.success(
    "Deploy additional drivers near high-demand pickup zones to reduce waiting times."
)

st.success(
    "Expand premium vehicle categories that contribute significantly to revenue growth."
)

st.success(
    "Promote digital payment options to align with customer preferences."
)

st.success(
    "Monitor service quality metrics continuously to maintain customer satisfaction."
)

st.markdown("---")

st.markdown(
"""
<center>
<b>Developed by Aswini B | Ride Analytics Project</b>
</center>
""",
unsafe_allow_html=True
)