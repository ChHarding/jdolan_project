🌦 WeatherWise

WeatherWise is a lightweight weather dashboard built using Streamlit and the free Open-Meteo API. It lets you view:
	•	Current weather conditions
	•	7–10 day forecasts
	•	Historical monthly weather trends across multiple years

All data is visualized with interactive graphs and clean summaries.

⸻

🔧 Installation & Setup

Prerequisites
	•	Python 3.10 or higher
	•	Git (optional)
	•	Internet connection

Step 1: Install Dependencies

Open your terminal and navigate to the project folder. Then run:

pip install -r requirements.txt

💡 You do not need to sign up for an API key — Open-Meteo is free and keyless!

⸻

🚀 How to Run the App

From the project folder, simply run:

streamlit run main-dashboard.py

This will open the app in your browser at http://localhost:8501.

⸻

🧭 How to Use the App

The app has three screens, selectable via the sidebar:

1. Current Weather

Displays the latest weather conditions (temperature, windspeed, and description) for a location of your choice.
	•	🏙 Enter any city name (e.g., “Denver”, “Chicago”, “Tokyo”) in the input box (Note: no need for the state or country)
	•	🌡 All temperature values are shown in Fahrenheit
	•	⚠️ If the city name can’t be found, an error will be displayed — try refining your input

⸻

2. Forecast

Shows a line chart and daily data table for the next 7–16 days.
	•	📅 Use the slider to adjust the number of forecast days
	•	🏙 Enter a city name to update the forecast for that location
	•	📈 Hover on graph points to view exact temperatures

⸻

3. Historical Data

Explore average high/low temperatures for any month, across up to 20 years of data.
	•	📆 Select the month
	•	🔢 Adjust the number of years (1–20)
	•	🏙 Enter the name of the city to analyze historical trends in that location
	•	📊 View a graph of temperature trends

⸻

🧩 Common Errors

MESSAGE: ModuleNotFoundError: No module named 'streamlit'	
	FIX: Run pip install -r requirements.txt
MESSAGE: ModuleNotFoundError: No module named 'weather'	
	FIX: Make sure you’re running main-dashboard.py from the root folder
MESSAGE: Blank screen	
	FIX: Refresh browser and check Streamlit log for errors
MESSAGE: Could not locate city	
	FIX: Make sure the city name is spelled correctly and is a valid location



⸻

⚠️ Caveats & Known Limitations
	•	🌡 Only Fahrenheit supported for temperature (no unit toggle yet)
	•	⌛ Historical data can load slowly when more than 10 years are selected
	•	📉 No precipitation data shown on the forecast screen (yet)
	•	🌍 City search is global, but some very small or obscure locations may not return results

⸻

🤝 Want to Contribute?

If you’re interested in improving WeatherWise, see the Developer Guide for an overview of the code structure and suggestions for future enhancements.

⸻

📄 License

This project is free and open source under the MIT License.