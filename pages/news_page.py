
import requests
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListView, QPushButton, QMessageBox
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex

class NewsListModel(QAbstractListModel):
    def __init__(self, news=None):
        super().__init__()
        self.news = news or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.news[index.row()]

    def rowCount(self, index=QModelIndex()):
        return len(self.news)

    def setNews(self, news):
        self.beginResetModel()
        self.news = news
        self.endResetModel()

class NewsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.model = NewsListModel([])
        self.list_view = QListView()
        self.list_view.setModel(self.model)

        self.refresh_btn = QPushButton("Refresh News")
        self.refresh_btn.clicked.connect(self.fetch_news)

        layout.addWidget(self.list_view)
        layout.addWidget(self.refresh_btn)
        self.setLayout(layout)

        self.fetch_news()

    def fetch_news(self):
        api_key = "8afccf204a8b4b00b6ccc58662aa6216"  # Replace with your NewsAPI key
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "ok":
                headlines = [article["title"] for article in data.get("articles", [])]
                self.model.setNews(headlines)
            else:
                self.model.setNews(["Failed to fetch news: " + data.get("message", "Unknown error")])
        except Exception as e:
            self.model.setNews([f"Error: {e}"])
            QMessageBox.critical(self, "Error", f"Failed to fetch news: {e}")
