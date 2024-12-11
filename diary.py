from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QHBoxLayout
from PyQt5.QtGui import QFont

class DiaryPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # Заголовок страницы
        label = QLabel("Ваши заметки:")
        label.setFont(QFont("Arial", 18))
        layout.addWidget(label)

        # Поле для ввода новой заметки
        self.note_input = QLineEdit(self)
        self.note_input.setPlaceholderText("Введите новую заметку...")
        self.note_input.setFont(QFont("Arial", 14))
        self.note_input.setStyleSheet("padding: 10px; margin-bottom: 10px;")
        layout.addWidget(self.note_input)

        # Кнопка для добавления заметки
        add_note_button = QPushButton("Добавить заметку")
        add_note_button.setStyleSheet(
            "padding: 10px; margin: 5px; background-color: #28A745; color: white; border-radius: 5px;")
        add_note_button.clicked.connect(self.add_note)
        layout.addWidget(add_note_button)

        # Список заметок
        self.notes_list = QListWidget(self)
        self.notes_list.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.notes_list)

        # Кнопка для удаления выбранной заметки
        delete_note_button = QPushButton("Удалить заметку")
        delete_note_button.setStyleSheet(
            "padding: 10px; margin: 5px; background-color: #D9534F; color: white; border-radius: 5px;")
        delete_note_button.clicked.connect(self.delete_note)
        layout.addWidget(delete_note_button)

        layout.addStretch()

    def add_note(self):
        """Добавляет новую заметку в список."""
        note_text = self.note_input.text().strip()
        if note_text:
            self.notes_list.addItem(note_text)
            self.note_input.clear()  # Очищаем поле ввода после добавления заметки

    def delete_note(self):
        """Удаляет выбранную заметку из списка."""
        selected_item = self.notes_list.currentItem()
        if selected_item:
            self.notes_list.takeItem(self.notes_list.row(selected_item))
