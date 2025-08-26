from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget

class CalendarPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.calendar = QCalendarWidget()
        layout.addWidget(self.calendar)
        self.setLayout(layout)
