from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QHBoxLayout
from PyQt5.QtGui import QFont
import sqlite3

from db.database import add_note_to_db, delete_note_from_db, update_note_in_db, get_all_notes_from_db

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

        # Кнопка для редактирования выбранной заметки
        edit_note_button = QPushButton("Редактировать заметку")
        edit_note_button.setStyleSheet(
            "padding: 10px; margin: 5px; background-color: #FFC107; color: white; border-radius: 5px;")
        edit_note_button.clicked.connect(self.edit_note)
        layout.addWidget(edit_note_button)

        layout.addStretch()

        # Загрузка заметок из базы данных
        self.load_notes()

    def add_note(self):
        """Добавляет новую заметку в базу данных и в начало списка."""
        note_text = self.note_input.text().strip()
        if note_text:
            # Добавляем заметку в базу данных
            conn = sqlite3.connect('db/articles.db')  # Подключаемся к базе данных articles.db
            cursor = conn.cursor()
            cursor.execute("INSERT INTO notes (text) VALUES (?)", (note_text,))
            conn.commit()
            conn.close()

            # Добавляем заметку в начало списка
            self.notes_list.insertItem(0, note_text)
            self.note_input.clear()  # Очищаем поле ввода после добавления заметки

    def load_notes(self):
        """Загружает заметки из базы данных в список."""
        conn = sqlite3.connect('db/articles.db')  # Подключаемся к базе данных articles.db
        cursor = conn.cursor()
        cursor.execute("SELECT text FROM notes")
        notes = cursor.fetchall()
        conn.close()

        for note in notes:
            self.notes_list.insertItem(0, note[0])  # Добавляем каждую заметку в начало списка

    def delete_note(self):
        """Удаляет выбранную заметку из базы данных и списка."""
        selected_item = self.notes_list.currentItem()
        if selected_item:
            note_text = selected_item.text()

            # Удаляем заметку из базы данных
            delete_note_from_db(note_text)

            # Удаляем заметку из списка
            self.notes_list.takeItem(self.notes_list.row(selected_item))

    def edit_note(self):
        """Редактирует выбранную заметку."""
        selected_item = self.notes_list.currentItem()
        if selected_item:
            note_text = selected_item.text()

            # Открываем поле для редактирования
            self.note_input.setText(note_text)

            # Кнопка для сохранения изменений
            save_button = QPushButton("Сохранить изменения")
            save_button.setStyleSheet(
                "padding: 10px; margin: 5px; background-color: #007BFF; color: white; border-radius: 5px;")
            save_button.clicked.connect(lambda: self.save_edited_note(selected_item, save_button))
            self.layout().addWidget(save_button)

    def save_edited_note(self, selected_item, save_button):
        """Сохраняет изменения редактируемой заметки."""
        new_text = self.note_input.text().strip()
        if new_text:
            # Обновляем заметку в базе данных
            note_id = self.get_note_id(selected_item.text())  # Получаем ID заметки
            update_note_in_db(note_id, new_text)

            # Обновляем заметку в списке
            selected_item.setText(new_text)
            self.note_input.clear()

            # Скрываем кнопку после сохранения изменений
            save_button.hide()

    def get_note_id(self, note_text):
        """Возвращает ID заметки по её тексту."""
        conn = sqlite3.connect('db/articles.db')  # Подключаемся к базе данных
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM notes WHERE text = ?", (note_text,))
        note_id = cursor.fetchone()[0]
        conn.close()
        return note_id
