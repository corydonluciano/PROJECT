from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget
from PyQt5.QtGui import QFont
from db.database import add_note_to_db, delete_note_from_db, update_note_in_db, get_all_notes_from_db

class DiaryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ваши заметки")
        layout = QVBoxLayout(self)

        label = QLabel("Ваши заметки:")
        label.setFont(QFont("Arial", 18))
        layout.addWidget(label)

        self.note_input = QLineEdit(self)
        self.note_input.setPlaceholderText("Введите новую заметку...")
        self.note_input.setFont(QFont("Arial", 14))
        self.note_input.setStyleSheet("padding: 10px; margin-bottom: 10px;")
        layout.addWidget(self.note_input)

        add_note_button = QPushButton("Добавить заметку")
        add_note_button.setStyleSheet(
            "padding: 10px; margin: 5px; background-color: #28A745; color: white; border-radius: 5px;")
        add_note_button.clicked.connect(self.add_note)
        layout.addWidget(add_note_button)

        self.notes_list = QListWidget(self)
        self.notes_list.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.notes_list)

        edit_note_button = QPushButton("Редактировать заметку")
        edit_note_button.setStyleSheet(
            "padding: 10px; margin: 5px; background-color: #FFC107; color: white; border-radius: 5px;")
        edit_note_button.clicked.connect(self.edit_note)
        layout.addWidget(edit_note_button)

        delete_note_button = QPushButton("Удалить заметку")
        delete_note_button.setStyleSheet(
            "padding: 10px; margin: 5px; background-color: #D9534F; color: white; border-radius: 5px;")
        delete_note_button.clicked.connect(self.delete_note)
        layout.addWidget(delete_note_button)



        layout.addStretch()
        self.load_notes()

    def add_note(self):
        note_text = self.note_input.text().strip()
        if note_text:
            add_note_to_db(note_text)
            self.notes_list.insertItem(0, note_text)
            self.note_input.clear()

    def load_notes(self):
        notes = get_all_notes_from_db()
        for note in notes:
            self.notes_list.insertItem(0, note[1])

    def edit_note(self):
        selected_item = self.notes_list.currentItem()
        if selected_item:
            note_text = selected_item.text()
            self.note_input.setText(note_text)

            save_button = QPushButton("Сохранить изменения")
            save_button.setStyleSheet(
                "padding: 10px; margin: 5px; background-color: #007BFF; color: white; border-radius: 5px;")
            save_button.clicked.connect(lambda: self.save_edited_note(selected_item, save_button))
            self.layout().addWidget(save_button)

    def delete_note(self):
        selected_item = self.notes_list.currentItem()
        if selected_item:
            note_text = selected_item.text()
            delete_note_from_db(note_text)
            self.notes_list.takeItem(self.notes_list.row(selected_item))



    def save_edited_note(self, selected_item, save_button):
        new_text = self.note_input.text().strip()
        if new_text:
            note_id = self.get_note_id(selected_item.text())
            update_note_in_db(note_id, new_text)
            selected_item.setText(new_text)
            self.note_input.clear()
            save_button.hide()

    def get_note_id(self, note_text):
        notes = get_all_notes_from_db()
        for note_id, text in notes:
            if text == note_text:
                return note_id
        return None
