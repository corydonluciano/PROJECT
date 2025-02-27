import pygame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QTime, QTimer


class MeditationPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)


        label = QLabel("Категории медитаций:")
        label.setFont(QFont("Arial", 18))
        layout.addWidget(label)


        self.start_stress_relief_button = QPushButton("Медитация для снятия стресса")
        self.start_stress_relief_button.setStyleSheet(
            "padding: 10px; margin: 5px; background-color: #0078D7; color: white; border-radius: 5px;")
        self.start_stress_relief_button.clicked.connect(self.start_stress_relief)
        layout.addWidget(self.start_stress_relief_button)


        self.start_mood_boost_button = QPushButton("Медитация для поднятия настроения")
        self.start_mood_boost_button.setStyleSheet(
            "padding: 10px; margin: 5px; background-color: #28A745; color: white; border-radius: 5px;")
        self.start_mood_boost_button.clicked.connect(self.start_mood_boost)
        layout.addWidget(self.start_mood_boost_button)

        layout.addStretch()


        pygame.mixer.init()


        self.original_button_styles = {
            'stress': self.start_stress_relief_button.styleSheet(),
            'mood': self.start_mood_boost_button.styleSheet()
        }

    def start_stress_relief(self):

        self.meditation_window = MeditationTimerWindow(duration=60, music_file="static/music/calming_music.mp3",
                                                       title="Снятие стресса")
        self.meditation_window.show()
        self.dim_button(self.start_stress_relief_button)


        self.meditation_window.destroyed.connect(lambda: self.restore_button_style('stress'))

    def start_mood_boost(self):

        self.meditation_window = MeditationTimerWindow(duration=120, music_file="static/music/mood_boost_music.mp3",
                                                       title="Поднятие настроения")
        self.meditation_window.show()
        self.dim_button(self.start_mood_boost_button)


        self.meditation_window.destroyed.connect(lambda: self.restore_button_style('mood'))

    def dim_button(self, button):

        current_color = self.get_button_color(button)
        darker_color = self.darken_color(current_color, 0.2)  # Уменьшаем яркость на 20%
        button.setStyleSheet(
            f"padding: 10px; margin: 5px; background-color: {darker_color}; color: white; border-radius: 5px;")
        button.setEnabled(False)

    def get_button_color(self, button):

        style = button.styleSheet()
        color_code = style.split('background-color: ')[1].split(';')[0]
        return color_code.strip()

    def darken_color(self, color_code, factor):

        color = QColor(color_code)
        color.setRed(int(color.red() * (1 - factor)))
        color.setGreen(int(color.green() * (1 - factor)))
        color.setBlue(int(color.blue() * (1 - factor)))
        return color.name()

    def restore_button_style(self, button_type):

        if button_type == 'stress':
            self.start_stress_relief_button.setStyleSheet(self.original_button_styles['stress'])
            self.start_stress_relief_button.setEnabled(True)
        elif button_type == 'mood':
            self.start_mood_boost_button.setStyleSheet(self.original_button_styles['mood'])
            self.start_mood_boost_button.setEnabled(True)


class MeditationTimerWindow(QWidget):
    def __init__(self, duration, music_file, title):
        super().__init__()

        self.setWindowTitle(f"Медитация: {title}")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout(self)


        self.time_duration = duration
        self.time_left = duration
        self.timer_label = QLabel(f"Оставшееся время: {self.time_left} секунд")
        self.timer_label.setFont(QFont("Arial", 18))
        layout.addWidget(self.timer_label)


        self.text_label = QLabel(
            "Закрой глаза и сделай глубокий вдох через нос, задержи дыхание на несколько секунд, затем медленно выдохни через рот. Почувствуй, как тело расслабляется, а ум успокаивается. Позволь себе отпустить все мысли и заботы этого дня. Ты здесь, в этом моменте, и ничто другое не имеет значения."
        )
        self.text_label.setFont(QFont("Arial", 12))
        self.text_label.setWordWrap(True)
        layout.addWidget(self.text_label)


        self.start_button = QPushButton("Начать медитацию")
        self.start_button.setStyleSheet(
            "padding: 10px; margin: 5px; background-color: #28A745; color: white; border-radius: 5px;"
        )
        self.start_button.clicked.connect(self.start_timer)
        layout.addWidget(self.start_button)


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        layout.addStretch()


        self.music_file = music_file
        self.title = title

    def closeEvent(self, event):

        pygame.mixer.music.stop()
        super().closeEvent(event)

    def play_meditation_music(self):

        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play(-1)

    def start_timer(self):

        self.timer.start(1000)
        self.start_button.setEnabled(False)
        self.play_meditation_music()

    def update_timer(self):

        self.time_left -= 1
        self.timer_label.setText(f"Оставшееся время: {self.time_left} секунд")


        if self.time_left == self.time_duration / 2:  # Середина медитации
            self.text_label.setText(
                "Продолжай дышать глубоко и ровно. Если мысли начинают блуждать, мягко верни внимание к дыханию. Ощущай каждый вдох и выдох, как они наполняют тебя энергией и спокойствием. Позволь своему телу быть тяжелым и неподвижным, словно оно сливается с землей под тобой."
            )
        elif self.time_left == 0:
            self.timer.stop()
            self.timer_label.setText("Медитация закончилась")
            self.text_label.setText(
                "Постепенно возвращайся к осознанию своего тела. Сделай еще пару глубоких вдохов и выдохов. Когда будешь готов, открой глаза. Посмотри вокруг себя с новым восприятием, почувствуй благодарность за этот момент тишины и покоя. Пусть это состояние останется с тобой на протяжении всего дня."
            )
            pygame.mixer.music.stop()
            self.start_button.setVisible(False)
            self.show_feedback_dialog()

    def show_feedback_dialog(self):

        reply = QMessageBox.question(
            self,
            "Вы молодец!",
            "Вам понравилась медитация?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )

        if reply == QMessageBox.Yes:
            print("Пользователь сказал 'Да'")
        else:
            print("Пользователь сказал 'Нет'")