import sqlite3


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QDialog, QDialogButtonBox, QScrollArea
from PyQt5.QtGui import QFont, QPixmap


class InformationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Статьи и информация")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout(self)

        label = QLabel("Информация и статьи:")
        label.setFont(QFont("Arial", 18))
        layout.addWidget(label)

        # Создаем список статей
        self.articles_list = QListWidget()
        self.articles_list.setStyleSheet("font-size: 16px; padding: 5px;")
        self.articles_list.clicked.connect(self.show_article_details)  # Подключаем событие клика
        layout.addWidget(self.articles_list)

        # Загружаем статьи из базы данных
        self.load_articles()

        layout.addStretch()

    def load_articles(self):
        """Загружает статьи из базы данных и отображает их в списке."""
        conn = sqlite3.connect('db/articles.db')
        cursor = conn.cursor()

        # Извлекаем все статьи
        cursor.execute('SELECT title FROM articles')
        articles = cursor.fetchall()

        # Добавляем статьи в QListWidget
        for article in articles:
            self.articles_list.addItem(article[0])

        conn.close()

    def show_article_details(self):
        """Показывает подробности статьи, включая изображение."""
        selected_item = self.articles_list.currentItem().text()

        conn = sqlite3.connect('db/articles.db')
        cursor = conn.cursor()

        # Извлекаем контент и изображение статьи по названию
        cursor.execute('SELECT content, image FROM articles WHERE title = ?', (selected_item,))
        article_data = cursor.fetchone()
        conn.close()

        if not article_data:
            return

        article_content, article_image = article_data

        # Открываем окно с подробностями статьи
        article_window = QDialog(self)
        article_window.setWindowTitle(f"Статья: {selected_item}")
        article_window.setGeometry(200, 200, 1600, 980)

        article_layout = QVBoxLayout(article_window)

        # Создаем область прокрутки для длинного текста
        scroll_area = QScrollArea(article_window)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Заголовок статьи
        article_title = QLabel(selected_item)
        article_title.setFont(QFont("Arial", 20))
        scroll_layout.addWidget(article_title)

        # Текст статьи
        article_text = QLabel(article_content)
        article_text.setFont(QFont("Arial", 16))
        article_text.setWordWrap(True)
        scroll_layout.addWidget(article_text)

        # Изображение статьи, если оно есть
        if article_image:
            pixmap = QPixmap()
            pixmap.loadFromData(article_image)
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            scroll_layout.addWidget(image_label)

        # Добавляем содержимое в область прокрутки
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        article_layout.addWidget(scroll_area)

        # Кнопка закрытия
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(article_window.reject)
        article_layout.addWidget(button_box)

        article_window.exec_()
