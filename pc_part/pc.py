from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

from PyQt5.QtWidgets import *
# use the QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import *
# Only needed for access to command line arguments
import sys

import urllib.request, json
from datetime import datetime

def timestamp_hmin_format(t):
    return str(datetime.fromtimestamp(t).hour) + ":"+ str(datetime.fromtimestamp(t).minute)

def load_appid():
    with open('secret.txt', 'r') as file:
        return file.read().strip()

APPID = load_appid()

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("Drone control station")
        
        web_view_layout = QVBoxLayout()
        toolbar = QToolBar("Tool bar title")
        toolbar.setOrientation(Qt.Vertical)
        # Web view
        web_view = QWebEngineView()
        web_view.load(QUrl("http://192.168.2.80/v.html"))

        web_view_layout.addWidget(web_view)

        # Weather section

        self.location_input = QLineEdit()
 
        self.location_input.setMaxLength(50)
        #self.location_input.setPlaceholderText("Fribourg")
        self.location_input.setText("Fribourg")

        self.location_input.returnPressed.connect(self.getWeatherData)

        toolbar.addWidget(self.location_input)

        self.getWeatherDataBtn = QPushButton("Get weather data")
        self.getWeatherDataBtn.clicked.connect(self.getWeatherData)

        toolbar.addWidget(self.getWeatherDataBtn)


        ##### Weather data labels #############
        self.weather_description_label = QLabel()

        self.temperature_label = QLabel()
        self.pressure_label = QLabel()
        self.humidity_label = QLabel()
        self.wind_speed_label = QLabel()
        self.wind_deg_label = QLabel()
        self.cloud_coverage_label = QLabel()
        self.sunrise_hmin_label = QLabel()
        self.sunset_hmin_label = QLabel()
        self.location_label = QLabel()


        # General description
        toolbar.addWidget(self.location_label)
        toolbar.addWidget(self.weather_description_label)

        # Measurements
        toolbar.addWidget(self.temperature_label)
        toolbar.addWidget(self.pressure_label)
        toolbar.addWidget(self.humidity_label)
        toolbar.addWidget(self.wind_speed_label)
        toolbar.addWidget(self.wind_deg_label)


        toolbar.addWidget(self.cloud_coverage_label)

        # Sunrise / sunset
        toolbar.addWidget(self.sunrise_hmin_label)
        toolbar.addWidget(self.sunset_hmin_label)

        ##################################################
        widget = QWidget()
        widget.setLayout(web_view_layout)
        
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        

    def getWeatherData(self):
        l = self.location_input.text()
        req_url = f"http://api.openweathermap.org/data/2.5/weather?q={l},ch&APPID={APPID}"
        print("Requesting : "+req_url)
        with urllib.request.urlopen(req_url) as url:
            data = json.loads(url.read().decode())

            # General description
            self.location_label.setText("Weather station location : "+data["name"])
            self.weather_description_label.setText("Weather situation : "+data["weather"][0]["description"])

            self.temperature_label.setText("Temperature : "+format(data["main"]["temp"] - 273.15, '.2f')+" C°")
            self.pressure_label.setText("Pressure : "+str(data["main"]["pressure"])+" Pa")
            self.humidity_label.setText("Humidity : "+str(data["main"]["humidity"])+" %")
            self.wind_speed_label.setText("Wind speed : "+str(data["wind"]["speed"])+" m/s")
            
            WIND_DEG_TITLE = "Wind direction : "
            if "deg" in data["wind"]:
                self.wind_deg_label.setText(WIND_DEG_TITLE+str(data["wind"]["deg"])+" °")
            
            else:
                self.wind_deg_label.setText(WIND_DEG_TITLE+"not available")

            self.cloud_coverage_label.setText("Cloud coverage : "+str(data["clouds"]["all"])+" %")

            # Sunrise / sunset
            self.sunrise_hmin_label.setText("Sunrise : "+timestamp_hmin_format(data["sys"]["sunrise"]))
            self.sunset_hmin_label.setText("Sunset : "+timestamp_hmin_format(data["sys"]["sunset"]))
           

app = QApplication(sys.argv)
window = MainWindow()
window.resize(3000, 2000)
window.show()
app.exec_()
