import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv( r"C:\Users\Aswini0905\Desktop\ubar_ride_analysis\source\cleaned_uber_data.csv")

st.title("Ride Sharing Analytics Dashboard")

# KPI calculations
total_bookings = len(df)
total_revenue = df['Booking Value'].sum()
avg_distance = df['Ride Distance'].mean()
avg_driver_rating = df['Driver Ratings'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Bookings", total_bookings)
col2.metric("Revenue", f"₹{total_revenue:,.0f}")
col3.metric("Avg Distance", round(avg_distance,2))
col4.metric("Driver Rating", round(avg_driver_rating,2))


# Peak Booking Hours

df['Hour'] = pd.to_datetime(df['Time']).dt.hour

peak_hours = df.groupby('Hour')['Booking ID'].count().reset_index()

fig = px.bar(
    peak_hours,
    x='Hour',
    y='Booking ID',
    title='Peak Booking Hours'
)

st.plotly_chart(fig, use_container_width=True)


#Add Booking Status Distribution
fig = px.pie(
    df,
    names='Booking Status',
    title='Booking Status Distribution'
)

st.plotly_chart(fig, use_container_width=True)




#Add Revenue by Vehicle Type
vehicle_revenue = df.groupby(
    'Vehicle Type'
)['Booking Value'].sum().reset_index()

fig = px.bar(
    vehicle_revenue,
    x='Vehicle Type',
    y='Booking Value',
    title='Revenue by Vehicle Type'
)

st.plotly_chart(fig, use_container_width=True)


#Add Top Pickup Locations
pickup_locations = (
    df['Pickup Location']
    .value_counts()
    .head(10)
    .reset_index()
)

pickup_locations.columns = ['Pickup Location', 'Bookings']

fig = px.bar(
    pickup_locations,
    x='Pickup Location',
    y='Bookings',
    title='Top 10 Pickup Locations'
)

st.plotly_chart(fig, use_container_width=True)


#Add Payment Method Analysis
fig = px.pie(
    df,
    names='Payment Method',
    title='Payment Method Usage'
)

st.plotly_chart(fig, use_container_width=True)

#Add Driver Rating Distribution
fig = px.histogram(
    df,
    x='Driver Ratings',
    nbins=20,
    title='Driver Rating Distribution'
)

st.plotly_chart(fig, use_container_width=True)


#Add Customer Rating Distribution
fig = px.histogram(
    df,
    x='Customer Rating',
    nbins=20,
    title='Customer Rating Distribution'
)

st.plotly_chart(fig, use_container_width=True)


#Add Customer Cancellation Reasons
customer_cancel = (
    df['Reason for cancelling by Customer']
    .dropna()
    .value_counts()
    .reset_index()
)

customer_cancel.columns = ['Reason', 'Count']

fig = px.bar(
    customer_cancel,
    x='Reason',
    y='Count',
    title='Customer Cancellation Reasons'
)

st.plotly_chart(fig, use_container_width=True)


#Add Driver Cancellation Reasons
driver_cancel = (
    df['Driver Cancellation Reason']
    .dropna()
    .value_counts()
    .reset_index()
)

driver_cancel.columns = ['Reason', 'Count']

fig = px.bar(
    driver_cancel,
    x='Reason',
    y='Count',
    title='Driver Cancellation Reasons'
)
st.plotly_chart(fig, use_container_width=True)
