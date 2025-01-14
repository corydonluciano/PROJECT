import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, \
    QFrame, QLabel
from PyQt5.QtGui import QFont, QPixmap

from diary import DiaryPage
from meditations import MeditationPage
from trackers import TrackerPage
from information_page import InformationPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Психологическая поддержка")
        self.setGeometry(100, 100, 1024, 768)


        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)


        main_layout = QHBoxLayout(central_widget)


        self.nav_panel = self.create_nav_panel()
        main_layout.addWidget(self.nav_panel)


        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area)


        self.add_pages()


        self.active_button = None

    def create_nav_panel(self):

        nav_panel = QFrame()
        nav_panel.setFixedWidth(200)
        nav_panel.setStyleSheet("background-color: #f7f7f7; border-right: 1px solid #ccc;")

        nav_layout = QVBoxLayout(nav_panel)


        self.buttons = {
            "Главная": QPushButton("Главная"),
            "Медитации": QPushButton("Медитации"),
            "Информация": QPushButton("Информация"),
            "Дневник": QPushButton("Дневник"),
            "Трекеры": QPushButton("Трекеры"),
        }

        for name, button in self.buttons.items():
            button.setFont(QFont("Arial", 14))
            button.setStyleSheet("background-color: #0078D7; border: none; padding: 10px; margin: 5px; color: white;")
            button.clicked.connect(lambda checked, name=name, button=button: self.switch_page(name, button))
            nav_layout.addWidget(button)

        nav_layout.addStretch()
        return nav_panel

    def add_pages(self):


        self.home_page = self.create_home_page()
        self.content_area.addWidget(self.home_page)


        self.meditations_page = MeditationPage()
        self.content_area.addWidget(self.meditations_page)


        self.info_page = InformationPage()
        self.content_area.addWidget(self.info_page)


        self.diary_page = DiaryPage()
        self.content_area.addWidget(self.diary_page)


        self.trackers_page = TrackerPage()
        self.content_area.addWidget(self.trackers_page)

    def create_home_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)


        image_label = QLabel()
        pixmap = QPixmap("static/image/image2.jpg")
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        layout.addStretch()
        return page

    def switch_page(self, page_name, button):

        if self.active_button:
            self.active_button.setStyleSheet(
                "background-color: #0078D7; border: none; padding: 10px; margin: 5px; color: white;")


        button.setStyleSheet(self.darken_button_color(button.styleSheet()))


        self.active_button = button

        pages = {
            "Главная": self.home_page,
            "Медитации": self.meditations_page,
            "Информация": self.info_page,
            "Дневник": self.diary_page,
            "Трекеры": self.trackers_page,
        }
        self.content_area.setCurrentWidget(pages[page_name])

    def darken_button_color(self, style):

        import re
        color_match = re.search(r'background-color: (\#\w+);', style)
        if color_match:
            color = color_match.group(1)
            # Преобразуем цвет в RGB
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            # Темним цвет
            r = max(r - 30, 0)
            g = max(g - 30, 0)
            b = max(b - 30, 0)

            darkened_color = f"background-color: #{r:02X}{g:02X}{b:02X};"
            return style.replace(f"background-color: {color};", darkened_color)
        return style


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
