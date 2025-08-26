from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListView, QPushButton, QHBoxLayout, QLineEdit
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex

class ToDoListModel(QAbstractListModel):
    def __init__(self, todos=None):
        super().__init__()
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.todos[index.row()]

    def rowCount(self, index=QModelIndex()):
        return len(self.todos)

    def addItem(self, item):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.todos.append(item)
        self.endInsertRows()

    def removeItem(self, row):
        if 0 <= row < len(self.todos):
            self.beginRemoveRows(QModelIndex(), row, row)
            self.todos.pop(row)
            self.endRemoveRows()

class ToDoPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.model = ToDoListModel([
            "Buy groceries",
            "Finish project report",
            "Call Alice",
            "Read a book"
        ])

        self.list_view = QListView()
        self.list_view.setModel(self.model)

        # Input and buttons
        input_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.add_btn = QPushButton("Add")
        self.remove_btn = QPushButton("Remove Selected")
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.add_btn)
        input_layout.addWidget(self.remove_btn)

        layout.addWidget(self.list_view)
        layout.addLayout(input_layout)
        self.setLayout(layout)

        self.add_btn.clicked.connect(self.add_item)
        self.remove_btn.clicked.connect(self.remove_item)

    def add_item(self):
        text = self.input.text().strip()
        if text:
            self.model.addItem(text)
            self.input.clear()

    def remove_item(self):
        selected = self.list_view.selectedIndexes()
        if selected:
            self.model.removeItem(selected[0].row())
