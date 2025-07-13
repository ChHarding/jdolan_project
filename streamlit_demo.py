
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

    # Create a DataFrame with the coordinates
    df = pd.DataFrame({
        'lat': [latitude],
        'lon': [longitude]
    })

    # Display the map
    st.map(df)


elif screen == "Forecast":
    st.title("Forecast Screen")
    summary = forecast.get_forecast_summary ("Orem") #Added for V2 to display in Streamlit
    st.write("Here is the weather forecast.")

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



