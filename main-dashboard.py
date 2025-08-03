
import streamlit as st
import pydeck as pdk
import pandas as pd
import requests
from datetime import datetime
from all_operating_files.utility import get_coordinates
from all_operating_files import weather
from all_operating_files import weather_history
from all_operating_files import forecast
import altair as alt

# Sidebar navigation
screen = st.sidebar.radio("Choose a screen:", ["Current Weather", "Forecast", "Historical Data"])

# --- user-entered location (defaults to Orem) -----------
location_input = st.sidebar.text_input(
    label="📍 Location (city, state or city, country)",
    value="Orem"
).strip()                # <- what we'll use everywhere

#st.write("🔍 Looking up coordinates for:", location_input)
coords = get_coordinates(location_input)
# st.write("📦 Raw result from get_coordinates:", coords)

if not coords or not all(coords):
    st.error(f"❌ Could not locate **{location_input}** – please try a different city name.")
    st.stop()
lat, lon, city_display = coords

# Display content based on selection
if screen == "Current Weather":
    st.title("Current Weather")
    st.subheader(f"Weather for {city_display}")

    now = datetime.now()

    # Example coordinates
    # Use previously defined lat, lon from get_coordinates()
    latitude = lat
    longitude = lon

    # Display current date and time
    now = datetime.now()
    st.subheader(f"{now.strftime('%A, %B %d, %Y')}")
    st.caption(f"Local time: {now.strftime('%I:%M %p')}")

    # Get and show current weather (assuming your `weather.get_current_weather` works like this)
    current = weather.get_current_weather(city_display, lat, lon)

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
    df = pd.DataFrame({'lat': [lat], 'lon': [lon]})

    # Display the map
    st.map(df)


#Added for dataframe
elif screen == "Forecast":
    st.title("Forecast Screen")

    # 👇 Add a slider for number of forecast days (not implemented in API yet)
    num_days = st.slider("Select number of forecast days", min_value=1, max_value=10, value=7)

    # Get forecast data
    forecast_data = forecast.get_forecast_summary(city_display, lat, lon)

    if forecast_data:
        # Show daily data
        st.subheader(f"{num_days}-Day Forecast for {city_display}")
        for i in range(min(num_days, len(forecast_data["dates"]))):
            st.markdown(f"📅 **{forecast_data['dates'][i]}**")
            st.write(f"🌡️ High: {forecast_data['temp_max'][i]}°F / Low: {forecast_data['temp_min'][i]}°F")
            st.write(f"🌧️ Precipitation: {forecast_data['precip'][i]} in")
            st.markdown("---")

        # Prepare for chart
        df = pd.DataFrame({
            "date": forecast_data["dates"],
            "temp_high": forecast_data["temp_max"],
            "temp_low": forecast_data["temp_min"]
        })

        df["date"] = pd.to_datetime(df["date"])

        # Create Altair chart
        chart = alt.Chart(df).transform_fold(
            ['temp_high', 'temp_low'],
            as_=['Type', 'Temperature']
            ).mark_line(point=True).encode(
            x=alt.X('date:T', title="Date"),
            y=alt.Y('Temperature:Q', title="°F"),
            color=alt.Color('Type:N', title='Temperature Type'),
            tooltip=[
            alt.Tooltip('date:T', title='Date'),
            alt.Tooltip('Type:N', title='Type'),
            alt.Tooltip('Temperature:Q', title='°F')
            ]
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

    city, month, history = weather_history.get_history_summary(
        city_display, month, num_years
    )

    st.subheader(
        f"Historical Weather for {city_display} - {month} "
        f"(Past {num_years} Years)"
    )

    # Transform data to DataFrame
    records = []
    for year, data in history:
        records.append({
        "year": year,
        "avg_rainfall": data["avg_rainfall"],
        "rainy_days": data["rainy_days"],
        "temp_low": data["min_temp"],
        "temp_high": data["max_temp"],
        })


    
    df_hist = pd.DataFrame(records)


    # Show raw data
    st.dataframe(df_hist)

    # Plot temp_high and temp_low
    df_long = df_hist.melt(id_vars=["year"], value_vars=["temp_high", "temp_low"],
                           var_name="Temperature Type", value_name="Temperature")
    df_long["Temperature"] = pd.to_numeric(df_long["Temperature"], errors="coerce")

    chart = alt.Chart(df_long).mark_line(point=True).encode(
        x=alt.X('year:O', title="Year"),
        y=alt.Y(
            'Temperature:Q',
            title="°F",
            axis=alt.Axis(
                format='.0f',
                labelExpr="datum.value + '°F'"
            )
        ),
        color=alt.Color('Temperature Type:N', title="Temperature"),
        tooltip=["year", "Temperature Type", "Temperature"]
    ).properties(
        width=600,
        height=400,
        title=f"Temperature Range in {month} for Past {num_years} Years"
    )

    st.altair_chart(chart, use_container_width=True)


