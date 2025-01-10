from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QHBoxLayout
from PyQt5.QtGui import QFont
import sqlite3

class DiaryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ваши заметки")
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

        # Загрузка заметок из базы данных
        self.load_notes()

    def add_note(self):
        """Добавляет новую заметку в базу данных и список."""
        note_text = self.note_input.text().strip()
        if note_text:
            # Добавляем заметку в базу данных articles.db
            conn = sqlite3.connect('articles.db')  # Подключаемся к базе данных articles.db
            cursor = conn.cursor()
            cursor.execute("INSERT INTO notes (text) VALUES (?)", (note_text,))
            conn.commit()
            conn.close()

            # Добавляем заметку в список
            self.notes_list.addItem(note_text)
            self.note_input.clear()  # Очищаем поле ввода после добавления заметки

    def delete_note(self):
        """Удаляет выбранную заметку из базы данных и списка."""
        selected_item = self.notes_list.currentItem()
        if selected_item:
            note_text = selected_item.text()

            # Удаляем заметку из базы данных
            conn = sqlite3.connect('articles.db')  # Подключаемся к базе данных articles.db
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes WHERE text = ?", (note_text,))
            conn.commit()
            conn.close()

            # Удаляем заметку из списка
            self.notes_list.takeItem(self.notes_list.row(selected_item))

    def load_notes(self):
        """Загружает заметки из базы данных в список."""
        conn = sqlite3.connect('articles.db')  # Подключаемся к базе данных articles.db
        cursor = conn.cursor()
        cursor.execute("SELECT text FROM notes")
        notes = cursor.fetchall()
        conn.close()

        for note in notes:
            self.notes_list.addItem(note[0])  # Добавляем каждую заметку в список
