# WeatherWise Developer Guide

## Overview

**WeatherWise** is a weather dashboard built using [Streamlit](https://streamlit.io) and the [Open-Meteo API](https://open-meteo.com/). It allows users to view current, forecasted, and historical weather data for a selected location, displayed in both tabular and graphical formats.

This developer guide is intended for contributors or maintainers who are taking over the codebase. It assumes you’ve already read the User’s Guide and have the project running locally.

---

## Final Specs vs Original Plan

| Feature                    | Planned | Implemented |
|---------------------------|---------|-------------|
| Current Weather Data      | ✅      | ✅          |
| Forecast Weather Graph    | ✅      | ✅          |
| Historical Data (monthly) | ✅      | ✅          |
| Location Selector         | ✅      | 🔜 (default is hardcoded) |
| Unit Toggle (F/C)         | ✅      | 🔜 (Fahrenheit default only) |

---

## Install / Deployment / Admin Notes

### Requirements

- Python 3.10+
- Streamlit
- Pandas
- Altair
- Requests

Install dependencies via:

```bash
pip install -r requirements.txt

Run the app with:

streamlit run main-dashboard.py

API Access

The app uses Open-Meteo’s free, no-auth APIs for current, forecast, and historical weather data. No API key is required.

⸻

Code Structure and Flow

Main Script: main-dashboard.py

The main entry point. It presents a sidebar with screen navigation:

screen = st.sidebar.radio("Choose a screen:", ["Current Weather", "Forecast", "Historical Data"])

Depending on the selected screen, it calls different modules:
	•	"Current Weather" → uses weather.py
	•	"Forecast" → uses forecast.py
	•	"Historical Data" → uses weather_history.py

Module Overview

weather.py
	•	get_current_weather(location: str)
	•	Makes a request to Open-Meteo’s current weather endpoint.
	•	Returns a summary dictionary of temperature, wind, and weather code.

forecast.py
	•	get_forecast(location: str, days: int)
	•	Converts a city name to lat/lon using Open-Meteo’s geocoding API.
	•	Gets forecasted temperature data for a given number of days.
	•	Graphs the data using Altair.
	•	Handles date parsing and formatting for the X-axis.

weather_history.py
	•	get_history_summary(location: str, month: str, num_years: int)
	•	Fetches historical weather data for a selected month across multiple past years.
	•	Returns structured data used to create line graphs of temp highs/lows.

⸻

UX Flow Summary
	•	Sidebar navigation allows switching between views.
	•	Each view has a clearly labeled st.title().
	•	The Forecast and Historical Data views use:
	•	st.slider() and st.selectbox() for user input.
	•	st.altair_chart() to visualize data.
	•	st.dataframe() to show tabular data.

⸻

Known Issues

Minor
	•	❗ Tooltip for Altair chart in historical data uses raw strings ('year') which may display strangely unless explicitly cast/formatted.
	•	❗ No ability to switch between Fahrenheit and Celsius.

Major
	•	⚠️ Currently hardcoded to "Orem" as location for all data.
	•	Workaround: Modify function calls to include st.text_input() or location lookup logic.

⸻

Inefficiencies
	•	Historical data is fetched year-by-year via separate API calls — this may be slow for large year ranges.
	•	Open-Meteo limits temporal resolution; no hourly breakdown for historical data.
	•	No caching or memoization — reloading a screen re-fetches data each time.

⸻

Future Work
	•	🌎 Add full location search and validation (via geocoding API).
	•	🌡 Toggle for Celsius vs Fahrenheit.
	•	📆 Option to view daily historical temperatures rather than monthly summaries.
	•	📊 Overlay precipitation data on temperature graphs.
	•	💾 Add caching for repeated location queries.
	•	📱 Optimize layout for mobile/tablet views.
	•	🧠 Consider implementing local data storage or offline capabilities for demo purposes.

⸻

Quick Start for New Developers
	1.	Clone the repo.
	2.	Run pip install -r requirements.txt.
	3.	Launch the app via streamlit run main-dashboard.py.
	4.	Explore each screen to understand flow.
	5.	View module code (weather.py, forecast.py, weather_history.py) to understand API structure.
