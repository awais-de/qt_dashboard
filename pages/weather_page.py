
import requests
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListView, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex

class WeatherListModel(QAbstractListModel):
    def __init__(self, weather=None):
        super().__init__()
        self.weather = weather or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.weather[index.row()]

    def rowCount(self, index=QModelIndex()):
        return len(self.weather)

    def setWeather(self, weather):
        self.beginResetModel()
        self.weather = weather
        self.endResetModel()

class WeatherPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.model = WeatherListModel([])
        self.list_view = QListView()
        self.list_view.setModel(self.model)

        self.fetch_btn = QPushButton("Fetch Weather for Ilmenau")
        self.fetch_btn.clicked.connect(self.fetch_weather)

        layout.addWidget(self.fetch_btn)
        layout.addWidget(self.list_view)
        self.setLayout(layout)

        # Fetch weather for Ilmenau on startup
        self.fetch_weather()

    def fetch_weather(self):
        api_key = "2b13be4ef9198c4444cf1a4573fddc77"  # Replace with your OpenWeatherMap API key
        city = "Ilmenau"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("cod") == 200:
                weather_info = [
                    f"City: {data['name']}",
                    f"Temperature: {data['main']['temp']} °C",
                    f"Weather: {data['weather'][0]['description']}",
                    f"Humidity: {data['main']['humidity']}%",
                    f"Wind Speed: {data['wind']['speed']} m/s"
                ]
                self.model.setWeather(weather_info)
            else:
                self.model.setWeather([f"Failed to fetch weather: {data.get('message', 'Unknown error')}"])
        except Exception as e:
            self.model.setWeather([f"Error: {e}"])
            QMessageBox.critical(self, "Error", f"Failed to fetch weather: {e}")
