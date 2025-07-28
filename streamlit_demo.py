
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


#elif screen == "Forecast": This is V1, look below for V2. Didn't delete yet to make sure this worked
    #st.title("Forecast Screen")
    #summary = forecast.get_forecast_summary ("Orem") #Added for V2 to display in Streamlit
    #st.write("Here is the weather forecast.")

#Added to V2 to display
elif screen == "Forecast":
    st.title("Forecast Screen")
    summary = forecast.get_forecast_summary("Orem")  # This should return a dict or list of forecast data
    if summary:
        st.markdown("### 7-Day Forecast for Orem")
        for day in summary:
            st.write({
                "Date": day.get("date"),
                "Temperature High (°F)": day.get("temp_high"),
                "Temperature Low (°F)": day.get("temp_low"),
                "Description": day.get("description")
            })
    else:
        st.error("Forecast data not available.")

elif screen == "Historical Data": #Expanded on in V2 in Streamlit
    st.title("Historical Data Screen")
    city, month, history = weather_history.get_history_summary("Orem", "May", 3)

    st.subheader(f"Historical Weather for {city} - {month}")
    for year, data in history:
        st.markdown(f"**{year}**")
        st.write({
            "Average Rainfall (in)": data["avg_rainfall"],
            "Rainy Days": data["rainy_days"],
            "Temperature Range": data["temp_range"]
        })


    
#elif screen == "Historical Data":
    #st.title("Historical Data Screen")
    #st.write("View historical weather data here.")



