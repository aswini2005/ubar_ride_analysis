import streamlit as st
import pandas as pd
import plotly.express as px


# Page Configuration
st.set_page_config(
    page_title="Uber Ride Performance Analytics Dashboard",
    page_icon="🚖",
    layout="wide"
)

# Custom CSS Styling
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Load Dataset
df = pd.read_csv(
    r"C:\Users\Aswini0905\Desktop\ubar_ride_analysis\source\cleaned_uber_data.csv"
)

# Remove spaces from column names
df.columns = df.columns.str.strip()

# Convert Time to Hour
df["Hour"] = pd.to_datetime(
    df["Time"],
    errors="coerce"
).dt.hour


# Sidebar Filters
st.sidebar.image(
    "https://img.icons8.com/color/96/taxi.png",
    width=100
)

st.sidebar.title("Filters")

vehicle_filter = st.sidebar.multiselect(
    "Vehicle Type",
    options=df["Vehicle Type"].dropna().unique(),
    default=df["Vehicle Type"].dropna().unique()
)

status_filter = st.sidebar.multiselect(
    "Booking Status",
    options=df["Booking Status"].dropna().unique(),
    default=df["Booking Status"].dropna().unique()
)

payment_filter = st.sidebar.multiselect(
    "Payment Method",
    options=df["Payment Method"].dropna().unique(),
    default=df["Payment Method"].dropna().unique()
)

filtered_df = df[
    (df["Vehicle Type"].isin(vehicle_filter)) &
    (df["Booking Status"].isin(status_filter)) &
    (df["Payment Method"].isin(payment_filter))
]


# Dashboard Title
st.markdown(
    "<h1 style='text-align:center;color:#1f77b4;'> Uber Ride Analytics Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown("---")


# KPI Cards
total_bookings = len(filtered_df)
total_revenue = filtered_df["Booking Value"].sum()
avg_distance = filtered_df["Ride Distance"].mean()
avg_rating = filtered_df["Driver Ratings"].mean()

k1, k2, k3, k4 = st.columns(4)

k1.metric("🚖 Total Bookings", f"{total_bookings:,}")
k2.metric("💰 Revenue", f"₹{total_revenue:,.0f}")
k3.metric("📍 Avg Distance", f"{avg_distance:.2f} km")
k4.metric("⭐ Driver Rating", f"{avg_rating:.2f}")

st.markdown("---")

# Row 1
c1, c2 = st.columns(2)
with c1:

    peak = (
        filtered_df.groupby("Hour")["Booking ID"]
        .count()
        .reset_index()
    )

    # Create time slots like 8-9 AM
    peak["Time Slot"] = peak["Hour"].apply(
        lambda x: f"{x%12 if x%12 != 0 else 12}-"
                  f"{(x+1)%12 if (x+1)%12 != 0 else 12} "
                  f"{'AM' if x < 12 else 'PM'}"
    )

    # Mark peak hours
    avg_bookings = peak["Booking ID"].mean()

    peak["Demand Type"] = peak["Booking ID"].apply(
        lambda x: "Peak Hour" if x > avg_bookings else "Normal Hour"
    )

    fig1 = px.bar(
        peak,
        x="Time Slot",
        y="Booking ID",
        color="Demand Type",
        text="Booking ID",
        title="📊 Peak Booking Hours"
    )

    fig1.update_traces(
        textposition="outside"
    )

    fig1.update_layout(
    height=400,      
    width=1000,     
    title={'text':'<b>📊 Peak Booking Hours</b>', 'x':0.5},
    xaxis_title='<b>Time Slot</b>',
    yaxis_title='<b>Number of Bookings</b>',
    xaxis_tickangle=-45,
    font=dict(size=14)
)

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# Peak Booking Hours
peak = (
    df.groupby("Hour")["Booking ID"]
    .count()
    .reset_index()
)

# Create Time Slot column
peak["Time Slot"] = peak["Hour"].apply(
    lambda x: f"{int(x):02d}:00 - {int(x)+1:02d}:00"
)

peak["Time Slot"] = peak["Hour"].apply(
    lambda x: pd.to_datetime(str(int(x)), format='%H').strftime('%I %p')
)

# Create Demand Category
avg_booking = peak["Booking ID"].mean()

peak["Demand Type"] = peak["Booking ID"].apply(
    lambda x: "Peak Hour" if x > avg_booking else "Normal Hour"
)



# Row 2
c3, c4 = st.columns(2)

with c3:
    revenue = (
        filtered_df.groupby("Vehicle Type")["Booking Value"]
        .sum()
        .reset_index()
    )

    fig3 = px.bar(
        revenue,
        x="Vehicle Type",
        y="Booking Value",
        title="💰 Revenue by Vehicle Type",
        text_auto=True
    )

    fig3.update_traces(
    texttemplate='₹%{y:,.0f}',
    textposition='outside'
)

fig3.update_layout(
    title={'text':'<b>💰 Revenue by Vehicle Type</b>', 'x':0.5},
    xaxis_title='<b>Vehicle Type</b>',
    yaxis_title='<b>Booking Value</b>'
)

fig3.update_xaxes(
    tickfont=dict(size=12, family="Arial Black")
)

fig3.update_yaxes(
    tickfont=dict(size=12, family="Arial Black")
)
fig3.update_layout(height=350)
st.plotly_chart(fig3, use_container_width=True)

with c4:
    fig4 = px.pie(
        filtered_df,
        names="Payment Method",
        hole=0.5,
        title="💳 Payment Method Usage"
    )

    fig4.update_layout(
    title={'text':'<b>💳 Payment Method Usage</b>', 'x':0.5},

)

fig4.update_xaxes(
    tickfont=dict(size=12, family="Arial Black")
)

fig4.update_yaxes(
    tickfont=dict(size=12, family="Arial Black")
)

fig4.update_layout(height=350)
st.plotly_chart(fig4, use_container_width=True)


# Row 3
c5, c6 = st.columns(2)

with c5:
    fig5 = px.histogram(
        filtered_df,
        x="Driver Ratings",
        nbins=20,
        title="⭐ Driver Rating Distribution"
    )
    fig5.update_layout(
    title={'text':'<b>⭐ Driver Rating Distribution</b>', 'x':0.5},
    xaxis_title='<b>Driver Rating</b>',
    yaxis_title='<b>Number of Drivers</b>'
)

fig5.update_xaxes(
    tickfont=dict(size=12, family="Arial Black")
)

fig5.update_yaxes(
    tickfont=dict(size=12, family="Arial Black")
)

fig5.update_layout(height=350)
st.plotly_chart(fig5, use_container_width=True)

with c6:
    fig6 = px.histogram(
        filtered_df,
        x="Customer Rating",
        nbins=20,
        title="😊 Customer Rating Distribution"
    )

    fig6.update_layout(
    title={'text':'<b>😊 Customer Rating Distribution</b>', 'x':0.5},
    xaxis_title='<b>Customer Rating</b>',
    yaxis_title='<b>YNumber of Customers</b>'
)

fig6.update_xaxes(
    tickfont=dict(size=12, family="Arial Black")
)

fig6.update_yaxes(
    tickfont=dict(size=12, family="Arial Black")
)

fig6.update_layout(height=350)
st.plotly_chart(fig6, use_container_width=True)


# Row 4
c7, c8 = st.columns(2)

with c7:
    pickup = (
        filtered_df["Pickup Location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    pickup.columns = ["Pickup Location", "Bookings"]

    fig7 = px.bar(
        pickup,
        x="Pickup Location",
        y="Bookings",
        title="📍 Top Pickup Locations",
        text_auto=True
    )

    fig7.update_layout(
    title={'text':'<b>📍 Top Pickup Locations</b>', 'x':0.5},
    xaxis_title='<b>Pickup Location</b>',
    yaxis_title='<b>Bookings</b>'
)

fig7.update_xaxes(
    tickfont=dict(size=12, family="Arial Black")
)

fig7.update_yaxes(
    tickfont=dict(size=12, family="Arial Black")
)

fig7.update_layout(height=350)
st.plotly_chart(fig7, use_container_width=True)

with c8:
    drop = (
        filtered_df["Drop Location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    drop.columns = ["Drop Location", "Bookings"]

    fig8 = px.bar(
        drop,
        x="Drop Location",
        y="Bookings",
        title="🏁 Top Drop Locations",
        text_auto=True
    )

    fig8.update_layout(
    title={'text':'<b>🏁 Top Drop Locations</b>', 'x':0.5},
    xaxis_title='<b>Drop Location</b>',
    yaxis_title='<b>Bookings</b>'
)

fig8.update_xaxes(
    tickfont=dict(size=12, family="Arial Black")
)

fig8.update_yaxes(
    tickfont=dict(size=12, family="Arial Black")
)

fig8.update_layout(height=350)
st.plotly_chart(fig8, use_container_width=True)


# Business Insights
st.markdown("---")

st.subheader("📌 Key Business Insights")

st.success("Peak booking demand occurs during office commute hours.")
st.success("Premium vehicle categories generate higher revenue.")
st.success("Digital payment methods dominate customer transactions.")
st.success("High-demand locations require better driver allocation.")
st.success("Driver ratings indicate strong service quality.")


# Footer

st.markdown("---")
st.markdown(
    "<center><b>Developed by Aswini B | Uber Ride Analytics Project</b></center>",
    unsafe_allow_html=True
)