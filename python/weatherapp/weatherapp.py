import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter Country Name", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get weather", self)
        self.forecast_label = QLabel(self)
        self.forecast_label.setWordWrap(True)
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather app")
        self.setMinimumSize(600, 400)  

        vbox = QVBoxLayout()
        vbox.setSpacing(5)  
        vbox.setContentsMargins(20, 15, 20, 15) 
        
        
        vbox.addWidget(self.city_label, alignment=Qt.AlignCenter)
        vbox.addSpacing(5)  
        vbox.addWidget(self.city_input)
        vbox.addSpacing(10)  
        vbox.addWidget(self.get_weather_button)
        vbox.addSpacing(15)  #
        vbox.addWidget(self.forecast_label)
        
        
        vbox.addStretch(1)
        
        self.setLayout(vbox)

        
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.forecast_label.setAlignment(Qt.AlignLeft)

        self.setStyleSheet("""
            QWidget { background-color: #ffffff; }
            QLabel, QPushButton, QLineEdit { font-family: Calibri; }
            QLabel { font-size: 40px; font-style: italic; color: #000000; }
            QLineEdit { 
                font-size: 30px; 
                padding: 8px;  /* Reduced padding */
                border-radius: 10px; 
                background-color: #ADD8E6; 
                color: #ffffff; 
                border: none; 
                min-height: 40px;  /* Added minimum height */
            }
            QPushButton { 
                font-size: 25px; 
                font-weight: bold; 
                background-color: #ADD8E6; 
                color: #ffffff; 
                border-radius: 10px; 
                padding: 8px;  /* Added padding */
                min-height: 40px;  /* Added minimum height */
            }
            QPushButton:hover { background-color: #87CEEB; }
            QLabel#forecast_label { 
                font-size: 25px; 
                color: #000000; 
                line-height: 1.2;  /* Reduced line height */
                margin: 0px;  /* Remove margins */
                padding: 0px;  /* Remove padding */
            }
        """)
        
        
        self.forecast_label.setObjectName("forecast_label")

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "db915ddb2dd46241df13ee8a8a8e87eb"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == "200":
                self.display_forecast(data)
        except requests.exceptions.HTTPError as http_Error:
            self.display_error(f"HTTP error: {http_Error}")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error: {req_error}")

    def display_error(self, message):
        self.forecast_label.setText(message)

    def display_forecast(self, data):
        forecast_text = ""
        for i in range(0, 40, 8):
            day_data = data["list"][i]
            temp_c = day_data["main"]["temp"] - 273.15
            description = day_data["weather"][0]["description"]
            emoji = self.get_weather_emoji(day_data["weather"][0]["id"])
            date = day_data['dt_txt'].split(' ')[0]
            forecast_text += f"{date}: {temp_c:.0f}℃ {emoji} {description}\n"

        self.forecast_label.setText(forecast_text)

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232: return "⛈️"
        elif 300 <= weather_id <= 321: return "🌦️"
        elif 500 <= weather_id <= 531: return "🌧️"
        elif 600 <= weather_id <= 622: return "🌨️"
        elif 701 <= weather_id <= 741: return "🌫️"
        elif weather_id == 762: return "🌋💨"
        elif weather_id == 771: return "🌬️"
        elif weather_id == 781: return "🌪️"
        elif weather_id == 801: return "🌤️"
        elif weather_id == 802: return "⛅"
        elif weather_id == 803: return "🌥️"
        elif weather_id == 804: return "☁️"
        elif weather_id == 800: return "☀️"
        else: return "❔"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())