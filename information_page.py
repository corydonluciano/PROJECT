from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QDialog, QDialogButtonBox, QScrollArea
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from db.database import get_all_articles, get_article_details


class InformationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Статьи и информация")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout(self)

        label = QLabel("Информация и статьи:")
        label.setFont(QFont("Arial", 18))
        layout.addWidget(label)


        self.articles_list = QListWidget()
        self.articles_list.setStyleSheet("font-size: 16px; padding: 5px;")
        self.articles_list.clicked.connect(self.show_article_details)
        layout.addWidget(self.articles_list)


        self.load_articles()

        layout.addStretch()

    def load_articles(self):

        articles = get_all_articles()
        for article in articles:
            self.articles_list.addItem(article)

    def show_article_details(self):

        selected_item = self.articles_list.currentItem().text()
        article_data = get_article_details(selected_item)

        if not article_data:
            return

        article_content, article_image = article_data


        article_window = QDialog(self)
        article_window.setWindowTitle(f"Статья: {selected_item}")
        article_window.setGeometry(200, 200, 1600, 980)

        article_layout = QVBoxLayout(article_window)


        scroll_area = QScrollArea(article_window)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)


        article_title = QLabel(selected_item)
        article_title.setFont(QFont("Arial", 24))
        article_title.setAlignment(Qt.AlignCenter)
        article_title.setStyleSheet("margin-bottom: 15px; color: #333;")
        scroll_layout.addWidget(article_title)


        if article_image:
            pixmap = QPixmap()
            pixmap.loadFromData(article_image)
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setStyleSheet("margin-bottom: 20px;")
            scroll_layout.addWidget(image_label)


        article_text = QLabel(article_content)
        article_text.setFont(QFont("Arial", 16))
        article_text.setWordWrap(True)
        article_text.setAlignment(Qt.AlignJustify)
        article_text.setStyleSheet("color: #555; padding: 10px; line-height: 1.6;")
        scroll_layout.addWidget(article_text)


        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        article_layout.addWidget(scroll_area)


        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.setStyleSheet("""
            QDialogButtonBox {
                margin-top: 10px;
            }
            QPushButton {
                font-size: 14px;
                background-color: #007BFF;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        button_box.rejected.connect(article_window.reject)
        article_layout.addWidget(button_box)

        article_window.exec_()
