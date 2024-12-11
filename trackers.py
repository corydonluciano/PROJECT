import random

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QRadioButton, QButtonGroup
)

from db.database import get_test_questions
from db.database import get_test_results_from_db, save_test_result_to_db


class TrackerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Трекеры настроения")
        layout = QVBoxLayout(self)

        # Кнопки для выбора трекера
        self.stress_button = QPushButton("Стресс")
        self.stress_button.clicked.connect(lambda: self.open_tracker_window("Стресс"))
        layout.addWidget(self.stress_button)

        self.mood_button = QPushButton("Настроение")
        self.mood_button.clicked.connect(lambda: self.open_tracker_window("Настроение"))
        layout.addWidget(self.mood_button)

        self.energy_button = QPushButton("Уровень энергии")
        self.energy_button.clicked.connect(lambda: self.open_tracker_window("Уровень энергии"))
        layout.addWidget(self.energy_button)

        # Список для отображения истории тестов
        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        self.load_test_results()
        layout.addStretch()

        # Храним ссылки на открытые окна, чтобы они не закрывались
        self.tracker_windows = []

    def load_test_results(self):
        """Загружает историю тестов из базы данных."""
        results = get_test_results_from_db()
        for tracker_type, result_text, score, timestamp in results:
            result_item = QListWidgetItem(
                f"Тип теста: {tracker_type} | Результат: {result_text} | "
                f"Баллы: {score:.1f} | Время: {timestamp}"
            )
            self.results_list.addItem(result_item)

    def open_tracker_window(self, tracker_type):
        """Открывает отдельное окно для трекера."""
        tracker_window = TrackerWindow(tracker_type, self.add_test_result)
        self.tracker_windows.append(tracker_window)  # Сохраняем ссылку
        tracker_window.show()

    def add_test_result(self, tracker_type, result_text, score):
        """Добавляет результат прохождения теста в список и сохраняет в базу данных."""
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

        # Загружаем вопросы из базы данных
        self.questions = self.get_random_questions()

        # Переменная для хранения оценок
        self.scores = []

        # Создаем интерфейс
        self.create_ui()

    def get_random_questions(self):
        """Получает 5 случайных вопросов из базы данных."""
        all_questions = get_test_questions(self.tracker_type)
        return random.sample(all_questions, 5) if len(all_questions) >= 5 else all_questions

    def create_ui(self):
        """Создает интерфейс для отображения вопросов."""
        self.radio_buttons = []  # Список для кнопок выбора ответов

        for i, question in enumerate(self.questions):
            label = QLabel(question)
            self.layout.addWidget(label)

            # Создаем радиокнопки для ответов
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

        # Кнопка для подсчёта результата
        submit_button = QPushButton("Завершить тест")
        submit_button.clicked.connect(self.calculate_score)
        self.layout.addWidget(submit_button)

        # Кнопка для закрытия
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        self.layout.addWidget(close_button)

    def calculate_score(self):
        """Вычисляет итоговый балл и выводит результат стресса."""
        total_score = 0

        for radio_button, score in self.radio_buttons:
            if radio_button.isChecked():
                total_score += score

        # Оценка стресса по баллам
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

        # Сохраняем результат в базу данных
        self.result_callback(self.tracker_type, result_text, total_score)

        # Показываем результат пользователю
        result_label = QLabel(f"Ваш результат: {result_text} | Баллы: {total_score:.1f}")
        self.layout.addWidget(result_label)
