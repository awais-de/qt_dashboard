import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QListWidgetItem, QWidget, QGridLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QAction, QPixmap

from main_ui import Ui_MainWindow  
from pages.todo_page import ToDoPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Initalize the UI from the generated UI File
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.main_content = self.ui.stck_wdgt_main


        #Initialize the UI Items
        self.lbl_title = self.ui.lbl_title
        self.lbl_title.setText('Dashboard')

        # Initialize the ToDoPage
        self.todo_page = ToDoPage()


        self.lbl_title_icon = self.ui.lbl_title_icon
        self.lbl_title_icon.setText('')
        self.lbl_title_icon.setPixmap(QPixmap('icons/logo.png'))
        self.lbl_title_icon.setScaledContents(True)

        self.side_menu = self.ui.lst_wdgt_menu
        self.side_menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.side_menu_icon_only = self.ui.lst_wdgt_menu_icons_only
        self.side_menu_icon_only.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.side_menu_icon_only.hide()

        self.btnMenu = self.ui.pushButton
        self.btnMenu.setObjectName("btnMenu")
        self.btnMenu.setText('')
        self.btnMenu.setIcon(QIcon('icons/menu.svg'))
        self.btnMenu.setIconSize(QSize(30, 30))
        self.btnMenu.setCheckable(True)


        #Define a list of menu items with names and icons
        self.menu_list = [
            {
                "name": "ToDo",
                "icon": "./icons/todo.svg"
            },
            {
                "name": "Weather",
                "icon": "./icons/weather.svg"
            },
            {
                "name": "News",
                "icon": "./icons/news.svg"
            },
            {
                "name": "Calendar",
                "icon": "./icons/calendar.svg"
            },
        ]



        # Initialize the UI elements and slots
        self.init_list_widget()
        self.init_stackwidget()
        self.init_single_slot()

        


    def init_single_slot(self):
        # Connect signals and slots for menu button and side menu
        self.btnMenu.toggled['bool'].connect(self.side_menu.setHidden)
        self.btnMenu.toggled['bool'].connect(self.lbl_title_icon.setHidden)
        self.btnMenu.toggled['bool'].connect(self.side_menu_icon_only.setVisible)
        self.btnMenu.toggled['bool'].connect(self.lbl_title_icon.setHidden)

        # Connect signals and slots for switching between menu items
        self.side_menu.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)
        self.side_menu_icon_only.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)
        self.side_menu.currentRowChanged['int'].connect(self.side_menu_icon_only.setCurrentRow)
        self.side_menu_icon_only.currentRowChanged['int'].connect(self.side_menu.setCurrentRow)
        self.btnMenu.toggled.connect(self.button_icon_change)

    def init_list_widget(self):
        # Initialize the side menu and side menu with icons only
        self.side_menu_icon_only.clear()
        self.side_menu.clear()

        for menu in self.menu_list:
            # Set items for the side menu with icons only
            item = QListWidgetItem()
            item.setIcon(QIcon(menu.get("icon")))
            item.setSizeHint(QSize(40, 40))
            self.side_menu_icon_only.addItem(item)
            self.side_menu_icon_only.setCurrentRow(0)

            # Set items for the side menu with icons and text
            item_new = QListWidgetItem()
            item_new.setIcon(QIcon(menu.get("icon")))
            item_new.setText(menu.get("name"))
            self.side_menu.addItem(item_new)
            self.side_menu.setCurrentRow(0)

    def init_stackwidget(self):
        # Remove all existing widgets from the stacked widget
        widget_list = self.main_content.findChildren(QWidget)
        for widget in widget_list:
            self.main_content.removeWidget(widget)

        # Import all custom page classes
        from pages.dashboard_page import DashboardPage
        from pages.todo_page import ToDoPage
        from pages.weather_page import WeatherPage
        from pages.news_page import NewsPage
        from pages.calendar_page import CalendarPage
        from pages.settings_page import SettingsPage

        # Create and add each page in the order of menu_list
        self.pages = [
            #DashboardPage(),
            ToDoPage(),
            WeatherPage(),
            NewsPage(),
            CalendarPage(),
            #sSettingsPage(),
        ]
        for page in self.pages:
            self.main_content.addWidget(page)

    def button_icon_change(self, status):
        # Change the menu button icon based on its status
        if status:
            self.btnMenu.setIcon(QIcon("./icons/open.svg"))
        else:
            self.btnMenu.setIcon(QIcon("./icons/close.svg"))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load style file
    with open("style.qss") as f:
        style_str = f.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
