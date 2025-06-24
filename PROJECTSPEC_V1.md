**Project Title: WeatherWise — Your Personal Weather Dashboard**

WeatherWise is a simple yet powerful desktop application designed to bring real-time weather forecasting and historical weather data directly to your screen. Built with Python and powered by the Open-Meteo API, this app makes weather tracking both accessible and user-friendly—even for those who aren’t particularly tech-savvy.

The primary goal of this project is to deliver an intuitive interface for viewing current weather, hourly and daily forecasts, and historical climate trends in any location worldwide. Users will be able to input a city or coordinates, and the application will display up-to-date information like temperature, precipitation, wind speed, and even UV index. For weather enthusiasts and casual users alike, this tool provides everything needed to plan their day—or week—accordingly.

In version 1, WeatherWise will be developed as a Command Line Interface (CLI) tool, allowing users to enter commands like weather --location "New York" or forecast --days 5 --location "Los Angeles". It will fetch data from the Open-Meteo API and output clean, human-readable summaries in the terminal. This minimal version ensures rapid development and testing without needing to design a user interface initially.

Eventually, the application will evolve into a full-featured desktop GUI using Python’s tkinter library, providing a clickable interface with maps, charts, and forecast timelines. For a more modern experience, a web version may be considered, using Flask as the backend and a lightweight frontend framework such as Streamlit or plain HTML/CSS templates enhanced with Bootstrap for responsiveness and design consistency.

WeatherWise will rely on external mechanisms such as RESTful API calls to Open-Meteo, JSON parsing, and optional email integration for daily weather summaries. With the flexibility of Python and the robustness of open weather APIs, this app aims to be both a practical daily tool and a stepping stone into more advanced data visualization projects.

**Vignettes**

⸻

**Vignette 1: Checking Today’s Weather**

Maria opens her laptop and wants to know if she should bring an umbrella before leaving for work. She opens the terminal and types:

weather --location "Chicago"

Within seconds, the app responds with a summary:
“Today in Chicago: 67°F, light rain, winds 10 mph NE. UV index: 4. Carry an umbrella just in case.”
Satisfied, she grabs her umbrella and heads out the door.

Technical Details:
	•	User inputs a location as a string (city or coordinates).
	•	The system sends a request to the Open-Meteo API /forecast endpoint with current weather data parameters.
	•	JSON data is parsed and formatted for clean CLI display.
	•	Future GUI version will show weather in cards with icons and background illustrations.
	•	Geolocation logic will later be added to allow for default location detection.

⸻

**Vignette 2: Viewing a 7-Day Forecast**

Later in the evening, Maria wants to plan a weekend hike. She types:

forecast --location "Denver" --days 7

A simple table appears in the terminal showing daily high/low temperatures, precipitation chances, and wind speeds for the next week. She sees sunny skies ahead and confirms her plans.

Technical Details:
	•	CLI command triggers API call to Open-Meteo’s 7-day forecast endpoint.
	•	Daily data is looped through and formatted as a simple table in terminal output.
	•	Units (Fahrenheit/Celsius, MPH/KPH) configurable via optional flag.
	•	Future GUI version will use line graphs or scrollable cards for day-by-day forecast.
	•	Backend caching can be added to reduce repeated API calls for same location.

⸻

**Vignette 3: Checking Historical Weather Trends**

Carlos is a data nerd planning a garden. He wants to know how rainy May was in his city over the past 3 years. He enters:

history --location "Seattle" --month "May" --years 3

The app returns average rainfall, number of rainy days, and temperature ranges for each year. He compares and starts planning the perfect planting schedule.

Technical Details:
	•	Command queries Open-Meteo’s historical weather data endpoints.
	•	App calculates averages and displays basic stats for comparison.
	•	Requires date parsing and possibly multiple requests (for each year).
	•	Future versions could offer CSV export or basic charts.
	•	CLI version outputs plain text, GUI might show bar charts or plots.

⸻

**Vignette 4: Receiving Daily Email Summaries**

Avery prefers to check weather via email. During setup, she types:

weather --subscribe --location "San Diego" --email "avery@email.com"

The app confirms: “Subscribed! You’ll receive daily weather summaries at 7 AM.”
Each morning, an email lands in her inbox with a forecast and outfit suggestion.

Technical Details:
	•	Requires basic user input validation for email and location.
	•	Will use a third-party email API (e.g., SendGrid, SMTP).
	•	Scheduler (e.g., cron, apscheduler) needed to automate daily job.
	•	For MVP, email body is plaintext; future enhancement may include rich HTML templates.
	•	User preferences stored in local JSON or SQLite DB.

⸻

**Vignette 5: Getting Severe Weather Alerts**

Jamal is a cyclist who needs real-time alerts about storms. He activates alert mode:

weather --alerts --location "Austin"

The app starts monitoring hourly forecast data and, upon detecting high winds or thunderstorms, pushes a desktop notification and logs it:
“⚠️ Alert: Severe Thunderstorm expected in 2 hours.”

Technical Details:
	•	Monitors forecast API for hourly data.
	•	Uses thresholds (wind speed, rain probability, storm warning flags) to trigger alerts.
	•	Desktop notifications via plyer, toast, or native OS hooks.
	•	Background process with polling logic.
	•	Configurable frequency and severity filters.

⸻
**Technical Flow**

Here’s a technical data flow breakdown and early architecture draft for WeatherWise, including a flow description in words, modular component breakdowns, and data types. This will help bridge the gap from user task → code structure.

⸻

🌩️ WeatherWise: Technical Flow Overview

🔁 Data Flow Summary
	1.	User Input (CLI)
→ Location and command-line flags (--location, --days, --subscribe, etc.)
	2.	Input Parser
→ Parses command line input and calls corresponding function
	3.	Weather Query Manager
→ Sends request to appropriate Open-Meteo API endpoint
→ Waits for JSON response
	4.	Response Handler
→ Validates and extracts required fields
→ Converts raw JSON into Python dicts/lists with clean structure
	5.	Output Formatter
→ Takes clean data and prints it to CLI (or returns it to GUI module later)
→ Optionally generates and sends emails or desktop alerts

⸻

🧱 Modules and Responsibilities

Module / Class Name	Purpose	Key Methods	Input / Output Types
CLIInputHandler	Parses and validates user commands	parse_args(), validate()	sys.argv[] → Python dict
WeatherAPIClient	Handles API requests to Open-Meteo	get_current(), get_forecast(), get_history()	Input: dict / Output: JSON
DataParser	Cleans and processes raw JSON	extract_current(), format_forecast()	Input: JSON → dict/list
OutputManager	Formats and displays CLI text	print_summary(), print_forecast_table()	Input: dict/list → string
SubscriptionManager	Handles email subscriptions	add_subscriber(), send_daily_email()	Input: email/location → logs/email
AlertSystem	Triggers desktop alerts on conditions	monitor_conditions(), push_alert()	Input: forecast dict → system notification
Scheduler	Sets up timed jobs for emails or alerts	schedule_email()	Input: user settings → job object



⸻

🧭 Data Flow (Sequential Description)

[User Input]
   ↓ (e.g. "forecast --location Denver --days 5")

→ [CLIInputHandler]
   ↓ (Parsed arguments: {"command": "forecast", "location": "Denver", "days": 5})

→ [WeatherAPIClient]
   ↓ (GET request to Open-Meteo /forecast?location=Denver&days=5)
   ↓ (JSON response: raw weather data)

→ [DataParser]
   ↓ (Extracts fields: {"daily": [{"day": "Mon", "temp": 72, ...}, ...]})

→ [OutputManager]
   ↓ (Formats forecast summary table)

→ [CLI Output]
   ↓ (User sees 7-day forecast in terminal)

[Optionally…]
→ [SubscriptionManager] (if user subscribed)
   ↓ [Scheduler]
   ↓ [send_daily_email()] via SendGrid or SMTP

→ [AlertSystem] (if user enabled alerts)
   ↓ (Checks hourly data for thresholds)
   ↓ (Sends desktop push if needed)



⸻

🔧 Sample Class Sketch (Python / OOP-Style Pseudocode)

class WeatherAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_forecast(self, location, days=7):
        params = {"latitude": ..., "longitude": ..., "daily": "..."}
        response = requests.get(self.base_url + "/forecast", params=params)
        return response.json()

class DataParser:
    def parse_forecast(self, json_data):
        daily_data = json_data.get("daily", [])
        return [{"day": d["date"], "high": d["temp_max"], "low": d["temp_min"]}
                for d in daily_data]

class OutputManager:
    def print_forecast_table(self, forecast_list):
        for day in forecast_list:
            print(f"{day['day']}: {day['high']}° / {day['low']}°")

# Main controller flow
cli_args = CLIInputHandler().parse_args()
api_client = WeatherAPIClient(BASE_URL)
data = api_client.get_forecast(cli_args["location"], cli_args["days"])
parsed_data = DataParser().parse_forecast(data)
OutputManager().print_forecast_table(parsed_data)

⸻

📄 Data Types in Flow

Step	Data Type
User input	str from sys.argv[]
Parsed args	dict
API response	JSON → dict
Parsed weather data	list[dict]
CLI table output	str
Email payload	str or HTML
Scheduled job	function reference / job ID
Desktop alert	OS call (string + icon)


 ![image](https://github.com/user-attachments/assets/21d3d5d0-70ca-4eea-ac9e-4638a96c04d8)


⸻

**Self Assessment**

● **After working through the spec, what was the biggest or most unexpected change you
had to make from your sketch?** Likely the amount of integration needed between different apps. This clearly isn't all in Python but knowing the actual necessary inputs was eye opening. 

**● How confident do you feel that you can implement the spec as it's written right now?** I feel like as long as I take this step by step, I shoudl be ok.

**● What is the biggest potential problem that you NEED to solve (or you’ll fail)?** If some integrations or APIs end up not being free, I'll have to find viable work arounds. 

**● What parts are you least familiar with and might need my help?** Uhhh probably anything not named Python
