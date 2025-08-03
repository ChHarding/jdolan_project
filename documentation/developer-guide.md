Here is your updated Developer Guide, revised to reflect that city name input is now supported across all modules (current, forecast, and historical data):

⸻

🌦 WeatherWise Developer Guide

Overview

WeatherWise is a weather dashboard built using Streamlit and the Open-Meteo API. It allows users to view current, forecasted, and historical weather data for any valid city name, displayed in both tabular and graphical formats.

This guide is intended for contributors or maintainers of the codebase. It assumes you’ve read the User Guide and have the project running locally.

⸻

✅ Final Specs vs Original Plan

Feature						Planned	Implemented
Current Weather Data		✅		✅
Forecast Weather Graph		✅		✅
Historical Data (monthly)	✅		✅
Location Selector			✅		✅ (via city input)
Unit Toggle (F/C)			✅		🔜 (Fahrenheit default only)



⸻

⚙️ Install / Deployment / Admin Notes

Requirements
	•	Python 3.10+
	•	Streamlit
	•	Pandas
	•	Altair
	•	Requests

Install dependencies via:

pip install -r requirements.txt

Then launch the app:

streamlit run main-dashboard.py

API Access

The app uses Open-Meteo’s free, keyless APIs for current, forecast, and historical weather data.

⸻

🧠 Code Structure and Flow

Main Script: main-dashboard.py

Main entry point. It shows a sidebar with navigation:

screen = st.sidebar.radio("Choose a screen:", ["Current Weather", "Forecast", "Historical Data"])

Each view prompts the user for a city name via st.text_input(), and then delegates logic to the appropriate module:

Screen	Module	Input Type
Current Weather	weather.py	location: str
Forecast	forecast.py	location: str + days
Historical Data	weather_history.py	location: str + month + years



⸻

🔍 Module Overview

weather.py

get_current_weather(location: str)

	•	Uses Open-Meteo’s geocoding API to convert the city name to lat/lon.
	•	Fetches current weather from Open-Meteo.
	•	Returns a dict with temperature, wind, and weather description.

⸻

forecast.py

get_forecast_weather(location: str, days: int)

	•	Geocodes city name → latitude/longitude.
	•	Fetches temperature max/min over the next n days.
	•	Returns structured time-series data for visualization.

⸻

weather_history.py

get_history_summary(location: str, month: str, num_years: int)

	•	Converts location to coordinates via geocoding.
	•	Pulls historical weather by year using Open-Meteo’s archive API.
	•	Returns averaged monthly highs and lows.

⸻

🧭 UX Flow Summary
	•	The sidebar handles screen switching and all city-based input.
	•	User enters a city name in each view.
	•	Visuals use st.altair_chart() and data tables use st.dataframe().
	•	Forecast and history use st.slider() for selecting date ranges.

⸻

🐞 Known Issues

Minor
	•	🧪 Altair chart in historical data may need string formatting ('year').
	•	ℹ️ Units are fixed to Fahrenheit — no toggle yet.

Major
	•	⚠️ No error handling yet for invalid city names (e.g. typos, unrecognized inputs).
	•	📡 Each geocoding and weather request is live (no caching or rate-limiting).

⸻

⏳ Inefficiencies
	•	Historical data is fetched in a loop (1 call per year) — slow if selecting 10+ years.
	•	No st.cache_data or memoization currently applied.
	•	Redundant lat/lon lookups could be minimized with session-level caching.

⸻

🔮 Future Work
	•	🌎 Add auto-complete or map-based location input.
	•	🌡 Implement Fahrenheit ↔ Celsius toggle.
	•	📊 Overlay forecast data with precipitation, wind, etc.
	•	📅 Add option for daily historical summaries (not just monthly).
	•	💾 Add caching (st.cache_data, st.session_state) for repeated city queries.
	•	📱 Improve mobile responsiveness of layout.
	•	🧠 Add fallback behavior if geocoding or weather API fails (e.g., invalid input).

⸻

🚀 Quick Start for New Developers
	1.	Clone the repo.
	2.	Run pip install -r requirements.txt.
	3.	Launch with streamlit run main-dashboard.py.
	4.	Try each screen, test with various city names.
	5.	Dive into weather.py, forecast.py, and weather_history.py for API logic.

⸻

Let me know if you’d like a visual code map or detailed class/function diagram next.