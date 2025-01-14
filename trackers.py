import random
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QRadioButton, QButtonGroup, QListWidget, QListWidgetItem
)
from db.database import get_test_questions, get_test_results_from_db, save_test_result_to_db

class TrackerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Трекеры настроения")
        layout = QVBoxLayout(self)


        self.stress_button = QPushButton("Стресс")
        self.stress_button.clicked.connect(lambda: self.open_tracker_window("Стресс"))
        layout.addWidget(self.stress_button)

        self.mood_button = QPushButton("Настроение")
        self.mood_button.clicked.connect(lambda: self.open_tracker_window("Настроение"))
        layout.addWidget(self.mood_button)

        self.energy_button = QPushButton("Уровень энергии")
        self.energy_button.clicked.connect(lambda: self.open_tracker_window("Уровень энергии"))
        layout.addWidget(self.energy_button)


        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        self.load_test_results()
        layout.addStretch()


        self.tracker_windows = []

    def load_test_results(self):

        results = get_test_results_from_db()
        for tracker_type, result_text, score, timestamp in results:
            result_item = QListWidgetItem(
                f"Тип теста: {tracker_type} | Результат: {result_text} | "
                f"Баллы: {score:.1f} | Время: {timestamp}"
            )
            self.results_list.addItem(result_item)

    def open_tracker_window(self, tracker_type):

        tracker_window = TrackerWindow(tracker_type, self.add_test_result)
        self.tracker_windows.append(tracker_window)  # Сохраняем ссылку
        tracker_window.show()

    def add_test_result(self, tracker_type, result_text, score):

        save_test_result_to_db(tracker_type, result_text, score)
        self.results_list.clear()
        self.load_test_results()


class TrackerWindow(QWidget):
    def __init__(self, tracker_type, result_callback):
        super().__init__()
        self.setWindowTitle(f"Трекер: {tracker_type}")
        self.setGeometry(200, 200, 400, 400)
        self.tracker_type = tracker_type
        self.result_callback = result_callback

        self.layout = QVBoxLayout(self)


        self.questions = self.get_random_questions()


        self.scores = []


        self.create_ui()

    def get_random_questions(self):

        if self.tracker_type == "Настроение":
            all_questions = get_test_questions("Счастье")
        elif self.tracker_type == "Уровень энергии":
            all_questions = get_test_questions("Энергия")
        else:
            all_questions = get_test_questions(self.tracker_type)
        return random.sample(all_questions, 5) if len(all_questions) >= 5 else all_questions

    def create_ui(self):

        self.radio_buttons = []

        for i, question in enumerate(self.questions):
            label = QLabel(question)
            self.layout.addWidget(label)


            group = QButtonGroup(self)
            answers = [
                ("Точно да", 1),
                ("Возможно да", 0.5),
                ("Не знаю", 0.2),
                ("Возможно нет", 0),
                ("Точно нет", 0)
            ]
            for text, score in answers:
                radio_button = QRadioButton(text)
                self.radio_buttons.append((radio_button, score))
                group.addButton(radio_button)
                self.layout.addWidget(radio_button)


        submit_button = QPushButton("Завершить тест")
        submit_button.clicked.connect(self.calculate_score)
        self.layout.addWidget(submit_button)


        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        self.layout.addWidget(close_button)

    def calculate_score(self):

        total_score = 0

        for radio_button, score in self.radio_buttons:
            if radio_button.isChecked():
                total_score += score


        if self.tracker_type == "Стресс":
            if total_score >= 4:
                result_text = "Высокий уровень стресса"
            elif total_score >= 3:
                result_text = "Повышенный уровень стресса"
            elif total_score >= 2:
                result_text = "Умеренный уровень стресса"
            elif total_score >= 1:
                result_text = "Лёгкий уровень стресса"
            else:
                result_text = "Нет стресса"
        elif self.tracker_type == "Настроение":
            if total_score >= 4:
                result_text = "Очень позитивное настроение"
            elif total_score >= 3:
                result_text = "Позитивное настроение"
            elif total_score >= 2:
                result_text = "Нейтральное настроение"
            elif total_score >= 1:
                result_text = "Негативное настроение"
            else:
                result_text = "Очень негативное настроение"
        elif self.tracker_type == "Уровень энергии":
            if total_score >= 4:
                result_text = "Очень высокий уровень энергии"
            elif total_score >= 3:
                result_text = "Высокий уровень энергии"
            elif total_score >= 2:
                result_text = "Средний уровень энергии"
            elif total_score >= 1:
                result_text = "Низкий уровень энергии"
            else:
                result_text = "Очень низкий уровень энергии"


        self.result_callback(self.tracker_type, result_text, total_score)


        result_label = QLabel(f"Ваш результат: {result_text} | Баллы: {total_score:.1f}")
        self.layout.addWidget(result_label)
