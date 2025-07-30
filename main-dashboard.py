
import streamlit as st
import pydeck as pdk
import pandas as pd
import requests
import argparse
import sys
from datetime import datetime
import weather
import weather_history
import forecast
import altair as alt

# Sidebar navigation
screen = st.sidebar.radio("Choose a screen:", ["Current Weather", "Forecast", "Historical Data"])

# Display content based on selection
if screen == "Current Weather":
    st.title("Current Weather")
    st.write("Welcome to the Current Weather screen.")

    # Example coordinates
    latitude = 40.314448
    longitude = -111.718667

    #To display the current location, which has been hard coded for me
    city_name = "Orem, UT"
    st.subheader(f"Weather for {city_name}")

    # Display current date and time
    now = datetime.now()
    st.subheader(f"{now.strftime('%A, %B %d, %Y')}")
    st.caption(f"Local time: {now.strftime('%I:%M %p')}")

    # Get and show current weather (assuming your `weather.get_current_weather` works like this)
    current = weather.get_current_weather("Orem")  # Replace with actual function if different

    if current:
        st.markdown("### Current Conditions")
        st.write({
            "Temperature (°F)": current.get("temperature"),
            "Weather": current.get("description"),
            "Humidity (%)": current.get("humidity"),
            "Wind Speed (mph)": current.get("wind_speed"),
        })
    else:
        st.error("Couldn't fetch current weather data.")

    # Create a DataFrame with the coordinates
    df = pd.DataFrame({
        'lat': [latitude],
        'lon': [longitude]
    })

    # Display the map
    st.map(df)


#Added for dataframe
elif screen == "Forecast":
    st.title("Forecast Screen")

     # 👇 Add a slider for number of forecast days
    num_days = st.slider("Select number of forecast days", min_value=1, max_value=16, value=7)

    # Get coordinates (or set city statically if only Orem supported)
    latitude = 40.2969
    longitude = -111.6946

    # 👇 Call the API with the number of days
    forecast_data = forecast.get_forecast_weather(latitude, longitude, days=num_days)

    # 👇 Display the data
    st.subheader(f"{num_days}-Day Forecast for Orem")
    for day in forecast_data["time"]:
        st.write(day)  # You can customize this further
    
    summary = forecast.get_forecast_summary("Orem")

    if summary:
        st.markdown("### 7-Day Forecast for Orem")

        # Convert to DataFrame
        df = pd.DataFrame(summary)

        # ✅ Parse date column correctly
        df["date"] = pd.to_datetime(df["date"])

        # Create an Altair chart
        chart = alt.Chart(df).transform_fold(
            ['temp_high', 'temp_low'],
            as_=['Type', 'Temperature']
        ).mark_line(point=True).encode(
            x=alt.X('date:T', title="Date"),
            y=alt.Y('Temperature:Q', title="°F"),
            color=alt.Color('Type:N', title='Temperature'),
            tooltip=['date', 'temp_high', 'temp_low', 'description']
        ).properties(
            width=600,
            height=400,
            title="High & Low Temperatures"
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.error("Forecast data not available.")

elif screen == "Historical Data":
    st.title("Historical Data Screen")

    # User selects month and number of years
    month = st.selectbox("Select a month", [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ])

    num_years = st.slider("Select number of years", min_value=1, max_value=20, value=5)

    city, month, history = weather_history.get_history_summary("Orem", month, num_years)

    st.subheader(f"Historical Weather for {city} - {month} (Past {num_years} Years)")

    # Transform data to DataFrame
    records = []
    for year, data in history:
        records.append({
            "year": year,
            "avg_rainfall": data["avg_rainfall"],
            "rainy_days": data["rainy_days"],
            "temp_low": data["temp_range"][0],
            "temp_high": data["temp_range"][1],
        })

    
    df_hist = pd.DataFrame(records)
    st.write(df_hist.dtypes)
    df_hist["temp_high"] = pd.to_numeric(df_hist["temp_high"], errors="coerce")
    df_hist["temp_low"] = pd.to_numeric(df_hist["temp_low"], errors="coerce")

    # Show raw data
    st.dataframe(df_hist)

    # Plot temp_high and temp_low
    df_long = df_hist.melt(id_vars=["year"], value_vars=["temp_high", "temp_low"],
                           var_name="Temperature Type", value_name="Temperature")
    df_long["Temperature"] = pd.to_numeric(df_long["Temperature"], errors="coerce")

    chart = alt.Chart(df_long).mark_line(point=True).encode(
        x=alt.X('year:O', title="Year"),
        y=alt.Y('Temperature:Q', title="°F"),
        color=alt.Color('Temperature Type:N', title="Temperature"),
        tooltip=["year", "Temperature Type", "Temperature"]
    ).properties(
        width=600,
        height=400,
        title=f"Temperature Range in {month} for Past {num_years} Years"
    )

    st.altair_chart(chart, use_container_width=True)


