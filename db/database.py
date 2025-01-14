import os
import sqlite3


def create_database():
    conn = sqlite3.connect('db/articles.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            image BLOB
        )
    ''')
    conn.commit()
    conn.close()

def insert_article_with_image(title, content, image_path):
    conn = sqlite3.connect('db/articles.db')
    cursor = conn.cursor()
    with open(image_path, 'rb') as file:
        image_data = file.read()
    cursor.execute('INSERT INTO articles (title, content, image) VALUES (?, ?, ?)', (title, content, image_data))
    conn.commit()
    conn.close()

def get_article_by_id(article_id):
    conn = sqlite3.connect('db/articles.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, content, image FROM articles WHERE id = ?', (article_id,))
    article = cursor.fetchone()
    conn.close()
    return article

def create_test_tables():
    conn = sqlite3.connect('db/articles.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_questions (
            id INTEGER PRIMARY KEY,
            tracker_type TEXT NOT NULL,
            question TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_history (
            id INTEGER PRIMARY KEY,
            tracker_type TEXT NOT NULL,
            result_text TEXT NOT NULL,
            score REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_test_question(tracker_type, question):
    conn = sqlite3.connect('db/articles.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO test_questions (tracker_type, question) VALUES (?, ?)', (tracker_type, question))
    conn.commit()
    conn.close()

def get_test_questions(tracker_type):
    conn = sqlite3.connect('db/articles.db')
    cursor = conn.cursor()
    cursor.execute('SELECT question FROM test_questions WHERE tracker_type = ?', (tracker_type,))
    questions = cursor.fetchall()
    conn.close()
    return [q[0] for q in questions]

def save_test_result_to_db(tracker_type, result_text, score):
    conn = sqlite3.connect('db/articles.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO test_history (tracker_type, result_text, score) VALUES (?, ?, ?)', (tracker_type, result_text, score))
    conn.commit()
    conn.close()

def get_test_results_from_db():
    conn = sqlite3.connect('db/articles.db')
    cursor = conn.cursor()
    cursor.execute('SELECT tracker_type, result_text, score, timestamp FROM test_history ORDER BY timestamp DESC')
    results = cursor.fetchall()
    conn.close()
    return results

def create_notes_table():
    conn = sqlite3.connect('db/articles.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()


def add_note_to_db(note_text):
    conn = sqlite3.connect('db/articles.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (text) VALUES (?)", (note_text,))
    conn.commit()
    conn.close()


def delete_note_from_db(note_text):
    conn = sqlite3.connect('db/articles.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE text = ?", (note_text,))
    conn.commit()
    conn.close()


def update_note_in_db(note_id, new_text):
    try:
        conn = sqlite3.connect('db/articles.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE notes SET text = ? WHERE id = ?", (new_text, note_id))
        conn.commit()
        conn.close()
        print(f"Заметка с ID {note_id} успешно обновлена.")
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении заметки: {e}")


def get_all_notes_from_db():
    conn = sqlite3.connect('db/articles.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return notes


def get_all_articles():
    conn = sqlite3.connect('db/articles.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title FROM articles')
    articles = [row[0] for row in cursor.fetchall()]
    conn.close()
    return articles


def get_article_details(title):
    conn = sqlite3.connect('db/articles.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content, image FROM articles WHERE title = ?', (title,))
    article_data = cursor.fetchone()
    conn.close()
    return article_data


# Создаем таблицы (если еще не созданы)
# create_test_tables()

# # Вопросы для теста на стресс
# stress_questions = [
#     "Я делаю однообразные, бессмысленные действия снова и снова, либо меня тянет к саморазрушающему поведению.",
#     "В последнее время я беспокоюсь о своём будущем больше, чем когда-либо.",
#     "В последнее время я слишком чувствительно реагирую на привычные раздражители.",
#     "К концу дня я совершенно эмоционально истощён, как будто ничего не чувствую.",
#     "Все, на что меня хватает после работы, – это сёрфинг в интернете и просмотр бесполезных видео.",
#     "У меня появились проблемы с засыпанием, сном или пробуждением, которых не было раньше.",
#     "Мое тело стало сдавать, появились заболевания или боли, которых раньше не было, приходится чаще посещать врача, легко могу заразиться чем-то, чем недавно переболел.",
#     "Просыпаюсь уставшим, как будто всю ночь не отдыхал, а работал. Или это похоже на состояние похмелья.",
#     "Повседневные дела вызывают у меня большее раздражение, чем обычно.",
#     "Не могу остановить мыслительную «жвачку», замечаю, что постоянно прокручиваю в голове одни и те же тревожные мысли.",
#     "В моей семье отношения стали более напряженными, чем раньше.",
#     "Я совершенно выведен из себя. Чувствую постоянную тревогу, отчаяние, панику.",
#     "Я потерял аппетит или стал переедать.",
#     "В последнее время я часто чувствую беспокойство о том, что находится вне моего контроля.",
#     "Быстро ли переходите к состоянию гнева или ярости, из-за чего вы кричите или с трудом сдерживаете себя?",
#     "У Вас случаются провалы в памяти или ощущение рассеянности, потери концентрации, особенно под давлением или в стрессе?",
#     "Замечаете ли Вы прилив сил, который заставляет Вас поздно ложиться спать?",
#     "Вам присущи трудности с засыпанием или прерванный сон?",
#     "У Вас есть пристрастие к сладкому (после каждого приема пищи Вам нужно съесть что-то сладкое, чаще всего конфету, печенье или шоколадку)?",
#     "Вы замечаете у себя ухудшение состояния кожи - сухость, истончение?"
# ]
#
# # Добавляем вопросы в таблицу
# for question in stress_questions:
#     add_test_question("Стресс", question)
#
# print("Вопросы для теста на стресс успешно добавлены в базу данных.")

