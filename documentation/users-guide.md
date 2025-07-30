Here is a complete README.md file written as a User’s Guide for your weather dashboard app, designed according to your assignment instructions. It focuses on helping a non-technical user get the app running and understand how to use it step-by-step.

⸻



# 🌦 WeatherWise

WeatherWise is a lightweight weather dashboard built using [Streamlit](https://streamlit.io) and the free [Open-Meteo API](https://open-meteo.com/). It lets you view:

- Current weather conditions
- 7–16 day forecasts
- Historical monthly weather trends across multiple years

All data is visualized with interactive graphs and clean summaries.

---

## 🔧 Installation & Setup

### Prerequisites

- Python 3.10 or higher
- Git (optional)
- Internet connection

### Step 1: Install Dependencies

Open your terminal and navigate to the project folder. Then run:

```bash
pip install -r requirements.txt

Note: You do not need to sign up for an API key — Open-Meteo is free and keyless!

⸻

🚀 How to Run the App

From the project folder, simply run:

streamlit run streamlit_demo.py

This will open the app in your browser at http://localhost:8501.

⸻

🧭 How to Use the App

The app has three screens, selectable via the sidebar:

1. Current Weather

Displays the latest weather conditions (temperature, windspeed, and description) for a default location.
	•	⚠️ Currently hardcoded to Orem, UT
	•	🌡 Outputs are in Fahrenheit

⸻

2. Forecast

Shows a line chart and daily data table for the next 7–16 days.
	•	📅 Use the slider to adjust the number of forecast days
	•	🧭 Location is fixed to Orem for now
	•	📈 Hover on graph points to view exact temps


⸻

3. Historical Data

Explore average high/low temperatures for any month, across up to 20 years of data.
	•	📆 Select the month
	•	🔢 Adjust the number of years (1–20)
	•	📊 View a graph of temperature trends


⸻

🧩 Common Errors

Message	Fix
ModuleNotFoundError: No module named 'streamlit'	Run pip install -r requirements.txt
ModuleNotFoundError: No module named 'weather'	Make sure you’re running streamlit_demo.py from the root folder
Blank screen	Refresh browser and check Streamlit log for traceback



⸻

⚠️ Caveats & Known Limitations
	•	🌎 Location is hardcoded to “Orem” where I reside — code would need to be updated if this was deployed
	•	🌡 Only Fahrenheit supported for temperature (no unit toggle yet)
	•	⌛ Historical data can load slowly when more than 10 years are selected
	•	📉 No precipitation data shown on the forecast screen (yet)

⸻

🤝 Want to Contribute?

If you’re interested in improving WeatherWise, see the Developer Guide for an overview of the code structure and suggestions for future enhancements.

⸻

📄 License

This project is free and open source under the MIT License.
