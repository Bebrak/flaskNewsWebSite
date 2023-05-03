import datetime
import os
import sqlite3
from flask import Flask, render_template, g
from fdatabase import FDataBase
from config import Config
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fdb.db')))
app.permanent_session_lifetime = datetime.timedelta(seconds=60)

# def update_news(url='https://www.bragazeta.ru/', count_of_news=3):
#     db = connect_db()
#     db = FDataBase(db)
#     # time.sleep(5)
#     response = requests.get(url)
#     bs = BeautifulSoup(response.text, "lxml")
#     n_title = bs.find('h1', 'title-small')
#     n_text = bs.find('p', 'card-text')
#     db.addMenu(n_title.text, n_text.text)
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        return g.link_db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена')

if __name__ == "__main__":
    app.run()